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
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import yaml  # type: ignore

REPO = Path(__file__).resolve().parent.parent
LOCK_PATH = REPO / "schemas.lock"
SPEC_DIR = REPO / "spec"

REQUIREMENT_LABEL = {"required": "**required**", "recommended": "recommended", "optional": "optional"}


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
    ref = (data["source"].get("ref") or "-")
    print(f"schemas.lock OK — source ref {ref}, "
          f"{len(active)} active, {len(pending)} pending {pending or ''}".rstrip())
    for name, pin in active.items():
        for req in ("version", "field_definitions_sha256"):
            if req not in pin:
                sys.exit(f"pin '{name}' is missing '{req}'")


# --- source resolution ----------------------------------------------------------------------

def resolve_field_definitions(source: dict, name: str, pin: dict, local_dir: str | None) -> dict:
    if local_dir:
        local = Path(local_dir).expanduser() / name / "field-definitions.json"
        if local.exists():
            print(f"  {name}: local {local}  (dev — hash NOT verified)")
            return json.loads(local.read_text())
    import requests  # imported lazily so --local-dir / --check work offline

    url = source["url_template"].format(ref=source.get("ref", ""), name=name, version=pin["version"])
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    expected = pin.get("field_definitions_sha256")
    actual = hashlib.sha256(resp.content).hexdigest()
    if not expected:
        sys.exit(f"  {name}: no field_definitions_sha256 pinned in schemas.lock")
    if actual != expected:
        sys.exit(f"  {name}: hash mismatch for {url}\n    expected {expected}\n    actual   {actual}")
    print(f"  {name}: fetched {url.split('@')[-1] if '@' in url else url} (sha256 ok)")
    return json.loads(resp.content)


# --- rendering ------------------------------------------------------------------------------

def _md(s: str | None) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def _field_rows(fields: list[dict]) -> list[str]:
    rows = ["| Field | Type | Requirement | Description |", "|---|---|---|---|"]
    for f in fields:
        desc = _md(f.get("description"))
        if f.get("range"):
            desc = f"{desc} <br/>*Range:* {_md(f['range'])}" if desc else f"*Range:* {_md(f['range'])}"
        req = REQUIREMENT_LABEL.get(f.get("requirement"), f.get("requirement", ""))
        rows.append(f"| `{f['name']}` | {_md(f.get('type'))} | {req} | {desc} |")
    return rows


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


def render_table_page(schema: str, table: dict, ref_base: str) -> str:
    name = table["name"]
    out = ["---", f'title: "{name}"', "toc: true",
           "# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
    if table.get("description"):
        out += [table["description"], ""]
    for note in table.get("notes") or []:
        out += ["::: {.callout-note appearance=\"simple\"}", note, ":::", ""]
    out += [f"::: {{.callout-tip appearance=\"simple\"}}",
            f"Summary view. **[Full reference →]({ref_base}#{name.lower()})** on behaverse.org/schemas.",
            ":::", ""]
    out += _field_rows(table["fields"]) + [""]
    return "\n".join(out)


def render_index_page(schema: str, doc: dict, ref_base: str) -> str:
    out = ["---", f'title: "{schema.title()} data"', "toc: false",
           "# GENERATED by scripts/build_spec.py — do not edit.", "---", ""]
    if doc.get("description"):
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
        if doc.get("description"):
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
    for name, pin in active.items():
        doc = resolve_field_definitions(lock["source"], name, pin, args.local_dir)
        generate_schema_pages(name, doc, docs_base)
    print("done.")


if __name__ == "__main__":
    main()
