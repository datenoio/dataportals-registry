#!/usr/bin/env python
"""Align properties.is_national with the national-catalog definition.

See scripts/national_catalog.py and docs/data-model.md.

Only records that currently have is_national: true are rewritten. Catalogs that
never had the flag are left unchanged. Do not bulk-set true from Federal/ or
.gov hostnames.

Usage:
    python scripts/fix_is_national_flags.py --dry-run
    python scripts/fix_is_national_flags.py
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from national_catalog import classify_is_national, is_legacy_open_data_name

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
ENTITIES_DIR = os.path.join(_REPO_ROOT, "data", "entities")

IS_NATIONAL_TRUE = re.compile(r"^([ \t]*)is_national:\s*true\s*$", re.M)


def _load(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            rec = yaml.load(f, Loader=Loader)
        return rec if isinstance(rec, dict) else None
    except (OSError, yaml.YAMLError):
        return None


def _set_false(text: str) -> tuple[str, bool]:
    new, n = IS_NATIONAL_TRUE.subn(r"\1is_national: false", text, count=1)
    return new, n == 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print counts and sample paths without writing files",
    )
    args = parser.parse_args()

    flagged = []
    for root, _dirs, files in os.walk(ENTITIES_DIR):
        for name in files:
            if not name.endswith(".yaml"):
                continue
            full = os.path.join(root, name)
            rec = _load(full)
            if not rec:
                continue
            props = rec.get("properties") or {}
            if not isinstance(props, dict) or props.get("is_national") is not True:
                continue
            rel = os.path.relpath(full, ENTITIES_DIR)
            keep, reason = classify_is_national(rec, rel)
            flagged.append(
                {
                    "full": full,
                    "rel": rel,
                    "rec": rec,
                    "keep": keep,
                    "reason": reason,
                }
            )

    od_by_country = defaultdict(list)
    for row in flagged:
        if row["keep"] and row["rec"].get("catalog_type") == "Open data portal":
            country = row["rel"].split(os.sep)[0]
            od_by_country[country].append(row)

    cap_n = 0
    for _country, rows in od_by_country.items():
        if len(rows) <= 2:
            continue
        legacy = [
            r for r in rows if is_legacy_open_data_name(r["rec"].get("name") or "")
        ]
        primary = [r for r in rows if r not in legacy]
        keep_ids = set()
        if primary:
            keep_ids.add(id(primary[0]))
        if legacy:
            keep_ids.add(id(legacy[0]))
        elif len(primary) > 1:
            keep_ids.add(id(primary[1]))
        for row in rows:
            if id(row) not in keep_ids:
                row["keep"] = False
                row["reason"] = "opendata_per_country_cap"
                cap_n += 1

    to_unset = [r for r in flagged if not r["keep"]]
    kept = [r for r in flagged if r["keep"]]

    print(f"Currently is_national true: {len(flagged)}")
    print(f"Keep true: {len(kept)}")
    print(f"Set false: {len(to_unset)} (including {cap_n} open-data caps)")
    print("Unset reasons:")
    for reason, n in Counter(r["reason"] for r in to_unset).most_common():
        print(f"  {reason}: {n}")
    print("Keep reasons:")
    for reason, n in Counter(r["reason"] for r in kept).most_common():
        print(f"  {reason}: {n}")

    if args.dry_run:
        print("\nDry run — no files written. Samples to unset:")
        for row in to_unset[:30]:
            print(f"  [{row['reason']}] {row['rel']} | {row['rec'].get('name')}")
        return 0

    written = 0
    missing = 0
    for row in to_unset:
        with open(row["full"], encoding="utf-8") as f:
            text = f.read()
        new, ok = _set_false(text)
        if not ok:
            missing += 1
            print(f"  skip (no is_national: true line): {row['rel']}")
            continue
        with open(row["full"], "w", encoding="utf-8") as f:
            f.write(new)
        written += 1
    print(f"Updated {written} files; {missing} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
