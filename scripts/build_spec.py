# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "pyyaml"]
# ///
"""
build_spec.py — fetch published behaverse/schemas artifacts and generate the BDM spec pages.

Replaces scripts/gsheets_to_quarto.py: instead of owning schema content, BDM *references* it.
This reads schemas.lock (pinned versions + content hashes), obtains each schema's
field-definitions.json, and generates Quarto spec pages (summary tables) that link out to the
full reference at behaverse.org/schemas/<name>. See BDM-redesign-spec.md §5.

It also generates the glossary data (glossary/glossary.yml) as a merge-view: cross-cutting
terms from the behaverse/schemas vocabulary (terms.jsonld) plus field terms harvested from
each fetched schema. Field names the vocabulary already defines are skipped (the vocabulary
definition is canonical); a multi-table schema contributes each field name once (first
definition wins, other tables are noted).

Source resolution per schema (in order):
  1. --local-dir DIR (or $BDM_SCHEMAS_LOCAL): read DIR/<name>/field-definitions.json.
     Dev convenience for before the schemas site is deployed; the hash is NOT verified.
  2. Fetch <schemas_base_url>/<name>/<version>/field-definitions.json and verify its
     sha256 against the lockfile (fail on mismatch; warn if no hash pinned).

Generated pages are build outputs (gitignored), never hand-edited.

Usage:
  uv run scripts/build_spec.py --check                       # validate schemas.lock, exit
  uv run scripts/build_spec.py --local-dir ../path/to/schemas  # generate from a local clone
  uv run scripts/build_spec.py                               # fetch from published URLs

TODO (upstream): remove LEGACY_LINKS once behaverse/schemas field-definitions are updated to
use the new site paths introduced in the 2026-06 BDM redesign.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import yaml  # type: ignore

REPO = Path(__file__).resolve().parent.parent
LOCK_PATH = REPO / "schemas.lock"
SPEC_DIR = REPO / "spec"
GLOSSARY_DATA = REPO / "glossary" / "glossary.yml"

REQUIREMENT_LABEL = {"required": "**required**", "recommended": "recommended", "optional": "optional"}

# Old site paths that moved in the 2026-06 redesign; upstream schema descriptions may still
# reference them. Rewrite until behaverse/schemas field-definitions catch up.
LEGACY_LINKS: dict[str, str] = {
    "/spec/general/2-dataset-cards.qmd": "/spec/dataset-cards.html",
    "/spec/general/1-folder-structure.qmd": "/spec/conventions/folder-structure.html",
    "/spec/general/3-studyflows.qmd": "/spec/studyflows.html",
    "/spec/general/4-instructions.qmd": "/spec/instructions.html",
    "/spec/general/5-questionnaires.qmd": "/spec/questionnaires.html",
}


def rewrite_legacy_links(text: str) -> str:
    """Replace stale pre-redesign site paths in fetched field text."""
    for old, new in LEGACY_LINKS.items():
        text = text.replace(old, new)
    return text


# --- lockfile -------------------------------------------------------------------------------

def load_lock(path: Path = LOCK_PATH) -> dict:
    if not path.exists():
        sys.exit(f"missing {path} — a BDM build needs a lockfile of pinned schema versions")
    data = yaml.safe_load(path.read_text()) or {}
    if "pins" not in data:
        sys.exit("schemas.lock must define 'pins'")
    if "url_template" not in (data.get("source") or {}):
        sys.exit("schemas.lock must define source.url_template")
    return data


def check_lock(data: dict) -> None:
    pins = data.get("pins") or {}
    active = {k: v for k, v in pins.items() if v}
    pending = [k for k, v in pins.items() if not v]
    print(f"schemas.lock OK — source {data['source']['url_template']}, "
          f"{len(active)} active, {len(pending)} pending {pending or ''}".rstrip())
    for name, pin in active.items():
        if "version" not in pin:
            sys.exit(f"pin '{name}' is missing 'version'")


# --- source resolution ----------------------------------------------------------------------

def _fetch_json(url: str, expected_sha: str | None, label: str) -> dict:
    import requests  # imported lazily so --local-dir / --check work offline

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    if expected_sha:  # optional: present only to freeze a release
        actual = hashlib.sha256(resp.content).hexdigest()
        if actual != expected_sha:
            sys.exit(f"  {label}: hash mismatch for {url}\n    expected {expected_sha}\n    actual   {actual}")
        print(f"  {label}: fetched {url} (sha256 ok)")
    else:
        print(f"  {label}: fetched {url}")
    return json.loads(resp.content)


def resolve_field_definitions(source: dict, name: str, pin: dict, local_dir: str | None) -> dict:
    if local_dir:
        local = Path(local_dir).expanduser() / name / "field-definitions.json"
        if local.exists():
            print(f"  {name}: local {local}  (dev — hash NOT verified)")
            return json.loads(local.read_text())
    url = source["url_template"].format(ref=source.get("ref", ""), name=name, version=pin["version"])
    return _fetch_json(url, pin.get("field_definitions_sha256"), name)


def resolve_vocabulary(vocab_cfg: dict, local_dir: str | None) -> dict:
    if local_dir:
        local = Path(local_dir).expanduser() / "vocabulary" / "terms.jsonld"
        if local.exists():
            print(f"  vocabulary: local {local}  (dev — hash NOT verified)")
            return json.loads(local.read_text())
    return _fetch_json(vocab_cfg["url"], vocab_cfg.get("sha256"), "vocabulary")


# --- rendering ------------------------------------------------------------------------------

def _md(s: str | None) -> str:
    return rewrite_legacy_links((s or "").replace("|", "\\|").replace("\n", " ").strip())


def _field_rows(fields: list[dict]) -> list[str]:
    rows = ["| Field | Type | Requirement | Description |", "|---|---|---|---|"]
    for f in fields:
        parts = [_md(f["description"])] if f.get("description") else []
        if f.get("range"):
            parts.append(f"*Range:* {_md(f['range'])}")
        for note in f.get("notes") or []:
            parts.append(f"*Note:* {_md(note)}")
        desc = " <br/>".join(parts)
        req = REQUIREMENT_LABEL.get(f.get("requirement"), f.get("requirement", ""))
        rows.append(f"| `{f['name']}` | {_md(f.get('type'))} | {req} | {desc} |")
    return rows


def _grouped_field_rows(fields: list[dict]) -> list[str]:
    """Render fields grouped under their category (Key, Context, …), as the original site did.
    Groups by each field's first category in first-appearance order; falls back to a single flat
    table when the fields carry no categories."""
    order: list[str] = []
    groups: dict[str, list[dict]] = {}
    for f in fields:
        cats = f.get("categories") or []
        key = cats[0] if cats else ""
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(f)
    if order == [""]:  # no categories present → flat table
        return _field_rows(fields)
    out: list[str] = []
    for key in order:
        out += [f"## {key or 'Other'}", ""] + _field_rows(groups[key]) + [""]
    return out


def _read_intro(schema: str) -> str:
    """Hand-written prose preamble for a generated schema page (spec/_intros/<schema>.qmd).

    Kept outside the gitignored generated dir so it survives regeneration. Any YAML
    frontmatter is stripped; the body is injected above the generated tables.
    """
    path = REPO / "spec" / "_intros" / f"{schema}.qmd"
    if not path.exists():
        return ""
    text = path.read_text()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    return text.strip()


def _vocab_section(doc: dict) -> list[str]:
    vocab = doc.get("vocabularies")
    if not vocab:
        return []
    out: list[str] = []
    if vocab.get("verbs"):
        out += ["", "## Verbs", "", "| Verb | Layer | Object types | Description |", "|---|---|---|---|"]
        for v in vocab["verbs"]:
            ots = ", ".join(f"`{o}`" for o in v.get("object_types", []))
            out.append(f"| `{v['name']}` | {v.get('layer','')} | {ots} | {_md(v.get('description'))} |")
    if vocab.get("object_types"):
        out += ["", "## Object types", "", "| Object type | Description |", "|---|---|"]
        out += [f"| `{x['name']}` | {_md(x.get('description'))} |" for x in vocab["object_types"]]
    if vocab.get("actor_types"):
        out += ["", "## Actor types", "", "| Actor type | Description |", "|---|---|"]
        out += [f"| `{x['name']}` | {_md(x.get('description'))} |" for x in vocab["actor_types"]]
    return out


def _slug(name: str) -> str:
    """CamelCase table/section name -> kebab-case slug. Mirrors the behaverse/schemas docs
    generator so the 'Full reference' link points at the right per-table page URL."""
    s = re.sub(r'(?<!^)(?=[A-Z])', '-', str(name))
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower() or 'item'


def render_table_page(schema: str, table: dict, ref_base: str) -> str:
    name = table["name"]
    out = ["---", f'title: "{name}"', "toc: true",
           "# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
    if table.get("description"):
        out += [table["description"], ""]
    for note in table.get("notes") or []:
        out += ["::: {.callout-note appearance=\"simple\"}", note, ":::", ""]
    out += [f"::: {{.callout-tip appearance=\"simple\"}}",
            f"Summary view. **[Full reference →]({ref_base}/{_slug(name)})** on behaverse.org/schemas.",
            ":::", ""]
    out += _grouped_field_rows(table["fields"])
    return "\n".join(out)


def render_index_page(schema: str, doc: dict, ref_base: str) -> str:
    out = ["---", f'title: "{schema.title()} data"', "toc: false",
           "# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
    intro = _read_intro(schema)
    if intro:
        out += [intro, ""]
    elif doc.get("description"):
        out += [doc["description"], ""]
    out += [f"*Schema version `{doc.get('version','?')}` — fetched from "
            f"[behaverse.org/schemas/{schema}]({ref_base}).*", "",
            "| Table | Fields | Description |", "|---|---:|---|"]
    for i, t in enumerate(doc["tables"], 1):
        out.append(f"| [{t['name']}]({i}-{t['name'].lower()}.qmd) "
                   f"| {len(t['fields'])} | {_md(t.get('description'))} |")
    return "\n".join(out) + "\n"


def generate_schema_pages(schema: str, doc: dict, base_url: str) -> Path:
    ref_base = f"{base_url}/{schema}"
    out_dir = SPEC_DIR / schema
    out_dir.mkdir(parents=True, exist_ok=True)
    if "tables" in doc:  # multi-table schema (trial)
        (out_dir / "index.qmd").write_text(render_index_page(schema, doc, ref_base))
        for i, table in enumerate(doc["tables"], 1):
            (out_dir / f"{i}-{table['name'].lower()}.qmd").write_text(
                render_table_page(schema, table, ref_base))
        n = sum(len(t["fields"]) for t in doc["tables"])
        print(f"  {schema}: generated index + {len(doc['tables'])} table pages ({n} fields) -> {out_dir}")
    else:  # single-object schema (dataset, event) — flat field list (+ optional vocabularies)
        heading = "Event envelope" if schema == "event" else "Fields"
        page = ["---", f'title: "{schema.title()}"', "toc: true",
                "# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
        intro = _read_intro(schema)
        if intro:
            page += [intro, ""]
        elif doc.get("description"):
            page += [doc["description"], ""]
        page += [f"*Schema version `{doc.get('version','?')}` — [full reference]({ref_base}).*", "",
                 f"## {heading}", ""]
        page += _field_rows(doc["fields"])
        page += _vocab_section(doc)
        (out_dir / "index.qmd").write_text("\n".join(page) + "\n")
        vocab = doc.get("vocabularies") or {}
        extra = f", {len(vocab.get('verbs', []))} verbs" if vocab else ""
        print(f"  {schema}: generated index ({len(doc['fields'])} fields{extra}) -> {out_dir}")
    return out_dir


# --- glossary -------------------------------------------------------------------------------

def _vocab_entries(vocab: dict) -> list[dict]:
    """Vocabulary concepts -> glossary listing entries (scheme label = category).
    Schemes/concepts with status 'internal' are reference-only and excluded."""
    scheme_label = {s["@id"]: s["label"] for s in vocab["schemes"] if s.get("status") != "internal"}
    entries = []
    for c in vocab["concepts"]:
        if c.get("status") == "internal" or c["scheme"] not in scheme_label:
            continue
        e = {"name": c["label"], "categories": [scheme_label[c["scheme"]]]}
        if c.get("data_type"):
            e["data_type"] = c["data_type"]
        e["description"] = rewrite_legacy_links(c["definition"])
        if c.get("range"):
            e["range"] = rewrite_legacy_links(c["range"])
        if c.get("notes"):
            e["notes"] = [rewrite_legacy_links(n) for n in c["notes"]]
        entries.append(e)
    return entries


def _schema_term_entries(schema: str, doc: dict, skip: set[str]) -> list[dict]:
    """Harvest one schema's field terms as glossary entries. Names in `skip` (defined by the
    vocabulary) are omitted. In a multi-table schema each name appears once: the first
    definition wins and the other tables are noted."""
    pairs = [(t["name"], f) for t in doc["tables"] for f in t["fields"]] if "tables" in doc \
        else [(None, f) for f in doc["fields"]]
    entries: dict[str, dict] = {}
    tables_of: dict[str, list[str]] = {}
    for tname, f in pairs:
        name = f["name"]
        if name in skip:
            continue
        if tname and tname not in tables_of.setdefault(name, []):
            tables_of[name].append(tname)
        if name in entries:
            continue
        e = {"name": name, "categories": [f"{schema.title()} fields"]}
        if f.get("type"):
            e["data_type"] = str(f["type"])
        e["description"] = rewrite_legacy_links(f.get("description", ""))
        if f.get("range"):
            e["range"] = rewrite_legacy_links(f["range"])
        if f.get("notes"):
            e["notes"] = [rewrite_legacy_links(n) for n in f["notes"]]
        entries[name] = e
    for name, e in entries.items():
        ts = tables_of.get(name) or []
        if len(ts) > 1:
            e.setdefault("notes", []).append(
                f"Shown as defined in the {ts[0]} table; also a field of: {', '.join(ts[1:])}.")
    return sorted(entries.values(), key=lambda e: e["name"])


def generate_glossary(vocab: dict, docs: dict[str, dict]) -> None:
    entries = _vocab_entries(vocab)
    vocab_names = {e["name"] for e in entries}
    counts = [f"{len(entries)} vocabulary terms (v{vocab.get('version', '?')})"]
    for schema, doc in docs.items():
        harvested = _schema_term_entries(schema, doc, vocab_names)
        entries += harvested
        counts.append(f"{len(harvested)} {schema} fields")
    header = ("# GENERATED by scripts/build_spec.py — do not edit.\n"
              "# Merge-view rendered by glossary/index.qmd: behaverse/schemas vocabulary terms\n"
              "# + field terms harvested from each schema's field-definitions.json.\n")
    GLOSSARY_DATA.write_text(header + yaml.safe_dump(entries, sort_keys=False,
                                                     allow_unicode=True, width=100))
    print(f"  glossary: {' + '.join(counts)} -> {GLOSSARY_DATA}")


# --- main -----------------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="validate schemas.lock and exit")
    ap.add_argument("--local-dir", default=os.environ.get("BDM_SCHEMAS_LOCAL"),
                    help="read <name>/field-definitions.json from this local schemas checkout (dev)")
    args = ap.parse_args()

    lock = load_lock()
    check_lock(lock)
    if args.check:
        return

    active = {k: v for k, v in (lock["pins"] or {}).items() if v}
    if not active:
        print("no active pins — nothing to generate (see schemas.lock).")
        return
    docs_base = lock.get("docs_base_url", "https://behaverse.org/schemas")
    print(f"generating spec pages for: {', '.join(active)}")
    docs: dict[str, dict] = {}
    for name, pin in active.items():
        doc = resolve_field_definitions(lock["source"], name, pin, args.local_dir)
        generate_schema_pages(name, doc, docs_base)
        docs[name] = doc
    vocab_cfg = lock.get("vocabulary")
    if vocab_cfg:
        print("generating glossary (vocabulary + schema field terms)")
        vocab = resolve_vocabulary(vocab_cfg, args.local_dir)
        generate_glossary(vocab, docs)
    print("done.")


if __name__ == "__main__":
    main()
