# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "pyyaml"]
# ///
"""
build_spec.py — fetch published behaverse/schemas artifacts and generate the BDM spec pages.

This replaces scripts/gsheets_to_quarto.py (which read a private Google Sheet). Instead of
owning schema content, BDM *references* it: this script reads schemas.lock (pinned versions +
content hashes), fetches each schema's published field-definitions.json from
behaverse.org/schemas, verifies the content hashes, and generates the Quarto spec pages plus
the glossary merge-view. See BDM-redesign-spec.md §5 and BDM-schemas-side-spec.md.

STATUS: scaffold. The fetch/generate steps are intentionally stubbed because behaverse/schemas
does not yet publish trial/event/vocabulary artifacts (BDM-schemas-side-spec.md §8). Until those
versioned URLs resolve, the site still builds from assets/auto-generated/ via the old pipeline,
and this script is NOT wired into .github/workflows/publish.yml.

Usage:
  uv run scripts/build_spec.py --check    # validate schemas.lock format, then exit
  uv run scripts/build_spec.py            # (future) fetch + verify + generate
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml  # type: ignore

LOCK_PATH = Path("schemas.lock")


def load_lock(path: Path = LOCK_PATH) -> dict:
    """Read and minimally validate schemas.lock."""
    if not path.exists():
        sys.exit(f"missing {path} — a BDM build needs a lockfile of pinned schema versions")
    data = yaml.safe_load(path.read_text()) or {}
    for key in ("schemas_base_url", "pins"):
        if key not in data:
            sys.exit(f"schemas.lock must define '{key}'")
    return data


def check_lock(data: dict) -> None:
    """Validate pin shapes. Null pins are treated as 'pending' (not yet published upstream)."""
    pins = data.get("pins") or {}
    active = {k: v for k, v in pins.items() if v}
    pending = [k for k, v in pins.items() if not v]
    print(
        f"schemas.lock OK — base={data['schemas_base_url']}, "
        f"{len(active)} active pin(s), {len(pending)} pending {pending or ''}".rstrip()
    )
    for name, pin in active.items():
        missing = [k for k in ("version", "field_definitions_sha256") if k not in pin]
        if missing:
            sys.exit(f"pin '{name}' is missing required keys: {missing}")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch_and_verify(base_url: str, name: str, pin: dict) -> dict:
    """Fetch <base_url>/<name>/<version>/field-definitions.json and verify its hash."""
    raise NotImplementedError(
        "blocked: behaverse/schemas does not yet publish field-definitions.json. "
        "Implement once the versioned URLs resolve — see BDM-schemas-side-spec.md §8."
    )


def generate_pages(name: str, field_definitions: dict) -> None:
    """Render Quarto spec pages (summary tables) from a fetched field-definitions doc."""
    raise NotImplementedError(
        "blocked: implement once fetch_and_verify returns real artifacts "
        "(BDM-redesign-spec.md §5)."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate schemas.lock and exit")
    args = parser.parse_args()

    lock = load_lock()
    check_lock(lock)
    if args.check:
        return

    print("fetch/generate not yet implemented — see STATUS in this file's module docstring.")
    # for name, pin in (lock["pins"] or {}).items():
    #     if not pin:
    #         continue  # pending schema, skip
    #     field_definitions = fetch_and_verify(lock["schemas_base_url"], name, pin)
    #     generate_pages(name, field_definitions)


if __name__ == "__main__":
    main()
