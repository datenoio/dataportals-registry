#!/usr/bin/env python3
"""
Script to fix COUNTRY_NAME_ID_MISMATCH issues from MEDIUM.txt.

Sets country.name to the canonical name for its country code
(COUNTRIES in constants.py) in owner.location.country and
coverage[].location.country across all entity YAML files.
"""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from constants import COUNTRIES

BASE_DIR = Path(__file__).parent.parent
ENTITIES_DIR = BASE_DIR / "data" / "entities"


def normalize_country(country):
    """Set country.name to the canonical name for country.id. Returns True if changed."""
    if not isinstance(country, dict):
        return False
    country_id = country.get("id")
    if country_id not in COUNTRIES:
        return False
    canonical = COUNTRIES[country_id]
    if country.get("name") == canonical:
        return False
    country["name"] = canonical
    return True


def fix_record_countries(record):
    """Normalize country names in owner.location and coverage entries. Returns count of fixes."""
    fixed = 0

    owner = record.get("owner")
    if isinstance(owner, dict):
        location = owner.get("location")
        if isinstance(location, dict) and normalize_country(location.get("country")):
            fixed += 1

    coverage = record.get("coverage")
    if isinstance(coverage, list):
        for entry in coverage:
            if not isinstance(entry, dict):
                continue
            location = entry.get("location")
            if isinstance(location, dict) and normalize_country(location.get("country")):
                fixed += 1

    return fixed


def main():
    files_fixed = 0
    fields_fixed = 0
    for yaml_path in sorted(ENTITIES_DIR.rglob("*.yaml")):
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: could not parse {yaml_path}: {e}")
            continue
        if not isinstance(data, dict):
            continue

        fixed = fix_record_countries(data)
        if fixed:
            with open(yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            files_fixed += 1
            fields_fixed += fixed

    print(f"Normalized country names in {fields_fixed} fields across {files_fixed} files")


if __name__ == "__main__":
    main()
