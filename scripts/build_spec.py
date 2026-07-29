# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "pyyaml"]
# ///
"""
build_spec.py — fetch published behaverse/schemas artifacts and generate the BDM spec pages.

Replaces scripts/gsheets_to_quarto.py: instead of owning schema content, BDM *references* it.
This reads schemas.lock (which schemas to fetch + optional content hashes), obtains each
schema's field-definitions.json, and generates Quarto spec pages (summary tables) that link
out to the full reference at behaverse.org/schemas/<name>. See BDM-redesign-spec.md §5.

It also generates the glossary data (glossary/glossary.yml) as a merge-view: cross-cutting
terms from the behaverse/schemas vocabulary (terms.jsonld) plus field terms harvested from
each fetched schema. Field names the vocabulary already defines are skipped (the vocabulary
definition is canonical); a multi-table schema contributes each field name once (first
definition wins, other tables are noted).

Source resolution per schema (in order):
  1. --local-dir DIR (or $BDM_SCHEMAS_LOCAL): read DIR/<name>/field-definitions.json.
     Dev convenience for previewing unpublished schema changes; the hash is NOT verified,
     and a missing local file is an error (no silent fallback to the network).
  2. Fetch the URL built from source.url_template ({name}, and {version} only if the
     template includes it — the canonical template tracks *current* content) and verify
     its sha256 against the lockfile (fail on mismatch; warn if no hash pinned).

Generated pages are build outputs (gitignored), never hand-edited.

Usage:
  uv run scripts/build_spec.py --check                       # validate schemas.lock, exit
  uv run scripts/build_spec.py --local-dir ../path/to/schemas  # generate from a local clone
  uv run scripts/build_spec.py                               # fetch from published URLs
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

# Upstream writes spaced em dashes; this site sets them unspaced. That is a typographic
# convention of the rendering surface, not of the schema, so it is applied on the way in rather
# than asked of upstream. Only the spacing changes, never the words. Applied to the whole
# fetched document so no call site can be missed.
_EM_DASH_SPACED = re.compile(r"[ \t]*—[ \t]*")


def apply_house_typography(node):
    """Recursively apply this site's typographic conventions to every string in a document."""
    if isinstance(node, str):
        return _EM_DASH_SPACED.sub("—", node)
    if isinstance(node, list):
        return [apply_house_typography(x) for x in node]
    if isinstance(node, dict):
        return {k: apply_house_typography(v) for k, v in node.items()}
    return node


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
    tpl = data["source"]["url_template"]
    if "{version}" in tpl:
        for name, pin in active.items():
            if "version" not in pin:
                sys.exit(f"pin '{name}' is missing 'version' (required by url_template)")


# --- source resolution ----------------------------------------------------------------------

def _fetch_json(url: str, expected_sha: str | None, label: str, attempts: int = 3) -> dict:
    import time

    import requests  # imported lazily so --local-dir / --check work offline

    resp = None
    for i in range(attempts):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            break
        except requests.RequestException as err:
            # 4xx won't heal on retry; retry only transient failures (timeouts, 5xx, conn).
            status = getattr(getattr(err, "response", None), "status_code", None)
            if (status is not None and status < 500) or i == attempts - 1:
                sys.exit(f"  {label}: failed to fetch {url}: {err}")
            wait = 2 ** (i + 1)
            print(f"  {label}: fetch failed ({err}); retrying in {wait}s ({i + 1}/{attempts - 1})")
            time.sleep(wait)
    if expected_sha:  # optional: present only to freeze a release
        actual = hashlib.sha256(resp.content).hexdigest()
        if actual != expected_sha:
            sys.exit(f"  {label}: hash mismatch for {url}\n    expected {expected_sha}\n    actual   {actual}")
        print(f"  {label}: fetched {url} (sha256 ok)")
    else:
        print(f"  {label}: fetched {url} — warning: no sha256 pinned, tracking current upstream content")
    return apply_house_typography(json.loads(resp.content))


def resolve_field_definitions(source: dict, name: str, pin: dict, local_dir: str | None) -> dict:
    if local_dir:
        local = Path(local_dir).expanduser() / name / "field-definitions.json"
        if not local.exists():
            sys.exit(f"  {name}: --local-dir given but {local} does not exist — "
                     "refusing to silently fall back to the published version")
        print(f"  {name}: local {local}  (dev — hash NOT verified)")
        return apply_house_typography(json.loads(local.read_text()))
    url = source["url_template"].format(ref=source.get("ref", ""), name=name, version=pin.get("version", ""))
    return _fetch_json(url, pin.get("field_definitions_sha256"), name)


def resolve_vocabulary(vocab_cfg: dict, local_dir: str | None) -> dict:
    if local_dir:
        local = Path(local_dir).expanduser() / "vocabulary" / "terms.jsonld"
        if not local.exists():
            sys.exit(f"  vocabulary: --local-dir given but {local} does not exist — "
                     "refusing to silently fall back to the published version")
        print(f"  vocabulary: local {local}  (dev — hash NOT verified)")
        return apply_house_typography(json.loads(local.read_text()))
    return _fetch_json(vocab_cfg["url"], vocab_cfg.get("sha256"), "vocabulary")


# --- rendering ------------------------------------------------------------------------------

def _md(s: str | None) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


# Upstream marks a note's severity with a leading marker inside the note string
# (behaverse/schemas CONTRIBUTING.md). `notes` stays a list of plain strings, so this
# parser degrades gracefully: an unrecognised marker is simply left in the text.
NOTE_LEVELS = {".warning": "warning", ".important": "important", ".tip": "tip", ".note": None}


def _split_note_level(note: object) -> tuple[str | None, str]:
    """`'.warning Do not …'` -> `('warning', 'Do not …')`; unmarked -> `(None, text)`."""
    s = str(note).strip()
    for marker, level in NOTE_LEVELS.items():
        if s == marker:
            return level, ""
        if s.startswith(marker + " "):
            return level, s[len(marker):].strip()
    return None, s


def _note_inline(note: object) -> str:
    """A note as it appears inside a table cell, where block callouts cannot be used.
    Leveled notes get a labelled span (styled in theme.scss); unmarked notes keep '*Note:*'."""
    level, text = _split_note_level(note)
    if not level:
        return f"*Note:* {_md(text)}"
    label = {"warning": "Warning", "important": "Important", "tip": "Tip"}[level]
    return f"[{label}:]{{.field-note .field-note-{level}}} {_md(text)}"


def _note_para(note: object) -> str:
    """A table-level note as a paragraph. These used to be callouts, but upstream now ships
    three to five notes per table and a stack of identical boxes flattened them to one weight —
    the reader could not tell a scope rule from a housekeeping detail. Severity rides on the
    same labelled span the field tables use, so a marked note still reads as marked."""
    level, text = _split_note_level(note)
    if not level:
        return _md(text)
    label = {"warning": "Warning", "important": "Important", "tip": "Tip"}[level]
    return f"[{label}:]{{.field-note .field-note-{level}}} {_md(text)}"


def _note_plain(note: object) -> str:
    """A note for plain-text consumers (the glossary data): marker stripped, level kept as a
    word so the severity is not silently lost."""
    level, text = _split_note_level(note)
    return f"{level.capitalize()}: {text}" if level else text


# Enum value sets (schemas ≥ v26.0803): a values-carrying field ships `values` — an authored-
# order list of {"value": ..., "description"?: ...} — always together with `values_exhaustive`.
# The presence of `values` is the signal, never `type`: three trial fields carrying values are
# type "string", and two "enum" fields carry no values at all.
_INLINE_VALUES_MAX = 140  # chars; e.g. studyflow's 22-value behaverseTask defers to the section


def _values_label(f: dict) -> str:
    """An open set must not read as the complete enumeration."""
    return "Values" if f.get("values_exhaustive") else "Known values"


def _inline_names(values: list[dict]) -> str:
    return " · ".join(f"`{v['value']}`" for v in values)


def _values_inline(f: dict) -> str | None:
    """The value names as they appear in the field's table cell; a long list defers to the
    value-definitions section rather than filling the cell with a wall of names."""
    values = f.get("values")
    if not values:
        return None
    names = _inline_names(values)
    if len(names) > _INLINE_VALUES_MAX:
        return f"*{_values_label(f)}:* {len(values)}, defined below."
    return f"*{_values_label(f)}:* {names}"


def _needs_definition_section(f: dict) -> bool:
    values = f.get("values") or []
    return bool(values) and (any(v.get("description") for v in values)
                             or len(_inline_names(values)) > _INLINE_VALUES_MAX)


def _value_definition_sections(fields: list[dict]) -> list[str]:
    """The full-width 'Value definitions' block rendered below a page's field tables.

    The inline cell carries only the value names; the definitions render here, where prose is
    not fighting a table cell's width. A field appears when at least one of its values is
    documented, or when its name list was too long to inline."""
    body: list[str] = []
    for f in fields:
        if not _needs_definition_section(f):
            continue
        body += [f"### `{f['name']}`", ""]
        if not f.get("values_exhaustive"):
            body += ["The set is open: datasets may contain values not listed here.", ""]
        body += ["| Value | Description |", "|---|---|"]
        body += [f"| `{v['value']}` | {_md(v.get('description'))} |" for v in f["values"]]
        body += [""]
    return ["## Value definitions", ""] + body if body else []


def _field_rows(fields: list[dict]) -> list[str]:
    rows = ["| Field | Type | Requirement | Description |", "|---|---|---|---|"]
    for f in fields:
        parts = [_md(f["description"])] if f.get("description") else []
        if f.get("range"):
            parts.append(f"*Range:* {_md(f['range'])}")
        if (inline := _values_inline(f)):
            parts.append(inline)
        for note in f.get("notes") or []:
            parts.append(_note_inline(note))
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


def render_table_page(schema: str, table: dict, index: int | None = None) -> str:
    name = table["name"]
    out = ["---", f'title: "{name}"', "toc: true"]
    if index is not None:  # keep the pre-padding URL working
        out.append(f'aliases: ["/spec/{schema}/{index}-{name.lower()}.html"]')
    out += ["# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
    if table.get("description"):
        out += [table["description"], ""]
    for note in table.get("notes") or []:
        out += [_note_para(note), ""]
    # Provenance line, styled like the one on the index page rather than as a sixth box.
    # The link target is the table's published docs_url — never derived here, so an upstream
    # URL-scheme change cannot silently 404 the reference links.
    out += [f"*Summary view—[full reference →]({table['docs_url']}) "
            "on behaverse.org/schemas.*", ""]
    out += _grouped_field_rows(table["fields"])
    if (sections := _value_definition_sections(table["fields"])):
        out += ["", *sections]
    return "\n".join(out)


def render_index_page(schema: str, doc: dict, ref_base: str,
                      aliases: list[str] | None = None) -> str:
    out = ["---", f'title: "{schema.title()}"', "toc: false"]
    if aliases:  # keep pre-generation URLs alive (configured per pin in schemas.lock)
        out.append(f'aliases: {json.dumps(aliases)}')
    out += ["# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
    intro = _read_intro(schema)
    if intro:
        out += [intro, ""]
    elif doc.get("description"):
        out += [doc["description"], ""]
    out += [f"*Schema version `{doc.get('version','?')}`—fetched from "
            f"[behaverse.org/schemas/{schema}]({ref_base}).*", "",
            "| Table | Fields | Description |", "|---|---:|---|"]
    for i, t in enumerate(doc["tables"], 1):
        out.append(f"| [{t['name']}]({_table_slug(i, t['name'])}.qmd) "
                   f"| {len(t['fields'])} | {_md(t.get('description'))} |")
    return "\n".join(out) + "\n"


def _table_slug(i: int, name: str) -> str:
    """Filename stem for a table page: zero-padded index + lowercased name.

    Padding matters: the sidebar picks these up with a filename glob, so an unpadded
    `10-` would sort before `2-` once a schema passes nine tables."""
    return f"{i:02d}-{name.lower()}"


def generate_schema_pages(schema: str, doc: dict, base_url: str,
                          aliases: list[str] | None = None) -> Path:
    ref_base = f"{base_url}/{schema}"
    out_dir = SPEC_DIR / schema
    out_dir.mkdir(parents=True, exist_ok=True)
    # Remove pages from a previous run: table sets change upstream (a renamed or reordered
    # table would otherwise leave a stale page behind, which the sidebar glob would pick up).
    for stale in out_dir.glob("*.qmd"):
        stale.unlink()
    if "tables" in doc:  # multi-table schema (trial, studyflow, timeseries)
        (out_dir / "index.qmd").write_text(render_index_page(schema, doc, ref_base, aliases))
        for i, table in enumerate(doc["tables"], 1):
            (out_dir / f"{_table_slug(i, table['name'])}.qmd").write_text(
                render_table_page(schema, table, i))
        n = sum(len(t["fields"]) for t in doc["tables"])
        print(f"  {schema}: generated index + {len(doc['tables'])} table pages ({n} fields) -> {out_dir}")
    else:  # single-object schema (dataset, event) — flat field list (+ optional vocabularies)
        heading = "Event envelope" if schema == "event" else "Fields"
        page = ["---", f'title: "{schema.title()}"', "toc: true"]
        if aliases:
            page.append(f'aliases: {json.dumps(aliases)}')
        page += ["# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
        intro = _read_intro(schema)
        if intro:
            page += [intro, ""]
        elif doc.get("description"):
            page += [doc["description"], ""]
        page += [f"*Schema version `{doc.get('version','?')}`—[full reference]({ref_base}).*", "",
                 f"## {heading}", ""]
        page += _field_rows(doc["fields"])
        if (sections := _value_definition_sections(doc["fields"])):
            page += ["", *sections]
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
        e["description"] = c["definition"]
        if c.get("range"):
            e["range"] = c["range"]
        if c.get("notes"):
            e["notes"] = [_note_plain(n) for n in c["notes"]]
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
        e["description"] = f.get("description", "")
        if f.get("range"):
            e["range"] = f["range"]
        if f.get("notes"):
            e["notes"] = [_note_plain(n) for n in f["notes"]]
        if f.get("values"):  # value-set docs live on the spec page; the names still belong here
            names = ", ".join(f"`{v['value']}`" for v in f["values"])
            e.setdefault("notes", []).append(f"{_values_label(f)}: {names}.")
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
    docs_base = lock.get("docs_base_url") or sys.exit("schemas.lock must define docs_base_url")
    print(f"generating spec pages for: {', '.join(active)}")
    gitignore = (REPO / ".gitignore").read_text() if (REPO / ".gitignore").exists() else ""
    docs: dict[str, dict] = {}
    for name, pin in active.items():
        doc = resolve_field_definitions(lock["source"], name, pin, args.local_dir)
        generate_schema_pages(name, doc, docs_base, aliases=pin.get("aliases"))
        if f"spec/{name}/" not in gitignore:
            print(f"  warning: spec/{name}/ is generated but not in .gitignore — "
                  "add it so build output cannot be committed")
        docs[name] = doc
    vocab_cfg = lock.get("vocabulary")
    if vocab_cfg:
        print("generating glossary (vocabulary + schema field terms)")
        vocab = resolve_vocabulary(vocab_cfg, args.local_dir)
        generate_glossary(vocab, docs)
    print("done.")


if __name__ == "__main__":
    main()
