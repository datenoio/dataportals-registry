## Context

The top-level items of `scripts/constants.py`, measured on 22 November 2026:

| Name | Lines | Users (active scripts and tests) | Existing copy |
|---|---|---|---|
| `SOFTWARE_NAME_ALIASES` | 784 | builder, fix_software_id | none |
| `SOFTWARE_DOCUMENTATION_URLS` | 346 | update_software | `documentation_url` in software YAML (20 of 344 differ) |
| `DOMAIN_LOCATIONS` | 343 | builder, extract_openaire_portals, stats, 2 tests | none |
| `MAP_SOFTWARE_ALLOWED_CATALOG_TYPES` | 324 | builder, fix_all_priority_issues, test_constants | none |
| `COUNTRIES` | 201 | 7 scripts and tests | `data/reference/countries.csv` (147 of 199 names match) |
| `SOFTWARE_REPOSITORY_URLS` | 146 | update_software | `repository_url` in software YAML (6 of 144 differ, 3 missing) |
| `LANGS_COUNTRIES` | 121 | constants only, through `COUNTRIES_LANGS` | none |
| `SOFTWARE_SPECIFIC_EXPORT_FORMATS` | 89 | update_software | `export_formats` in software YAML (6 of 87 differ) |
| everything else | ≈280 | — | small enums, loaders, paths |

Some lists are already computed from `data/reference/*.yaml` and stay as they are: `CATALOG_TYPE_ALLOWED`, `STATUS_ALLOWED`, `ACCESS_MODE_ALLOWED`, `MAP_SOFTWARE_OWNER_CATALOG_TYPE` and the others whose value is a call.

## Goals / Non-Goals

- Goals:
  - One source for each table.
  - `constants.py` under 300 lines.
  - The same values for every public constant.
  - Software facts kept next to the software they describe.
- Non-Goals:
  - Changing catalog YAML.
  - Changing country names in existing records.
  - Merging the Cerberus and JSON Schema definitions (phase 4).

## Decisions

- **Decision:** Per-software facts become fields in that software's YAML: aliases, allowed catalog types, documentation and repository URLs, export formats.
  - Why: `docs/software-taxonomy.md` already makes the software YAML the place to add a platform. A new platform then needs one file, not a YAML file plus four dict edits.
- **Decision:** `constants.py` keeps exporting the same names, built at import time.
  - Why: 7–13 modules import these names. Keeping the interface makes the change data-only for them, and the snapshot test can prove equality.
- **Decision:** Conflicting software values default to the YAML value.
  - Why: `update_software.py` is the only reader of the dicts, and it writes into the YAML, so the YAML was edited after the dicts. The 32 conflicts are listed in the PR for review, not changed silently.
- **Decision:** Country names: `countries.csv` gains a `registry_name` column, filled from `COUNTRIES`. Bloc folders (`Africa`, `ASEAN`, `Caribbean`, `EU`, `LatinAmerica`, `Oceania`, `World`) go to `path_regions.yaml`, next to the source of `PATH_COUNTRY_ALLOWLIST`.
  - Why: the 52 differences are deliberate registry spellings or blocs, so they need their own column, not an overwrite of the ISO name.
- **Decision:** Keep the `.tsv` name for tab-separated reference files and delete the `.csv` duplicates. For `langs`, merge both files' entries into `langs.tsv` and report codes that appear in only one file.

## Risks / Trade-offs

- **Import-time I/O.** Reading about 800 YAML files at import would slow every script.
  - Mitigation: `constants.py` already parses the software YAML for `MAP_SOFTWARE_OWNER_CATALOG_TYPE`. Build all software-derived dicts in that same single pass. Measure import time before and after; the budget is no more than 100 ms slower.
- **Merge conflicts during the move.** `constants.py` is the most-changed script.
  - Mitigation: move one table per PR, smallest consumer set first.
- **A data contributor edits the old dict out of habit.**
  - Mitigation: the guard test fails on large literals in `constants.py`, and its error message names the new file.

## Migration Plan

1. Add the snapshot test, which records the current value of every public constant.
2. Software: schema fields, then a migration script that writes `aliases` and `allowed_catalog_types` into the YAML, then the dicts built from YAML. Then remove the four URL/format dicts and point `update_software.py` at the YAML.
3. Move `DOMAIN_LOCATIONS`, `LANGS_COUNTRIES` and `COUNTRIES` to `data/reference/`, one PR each.
4. Remove the duplicate reference files and update their readers.
5. Add the size guard and update the docs.

Rollback: each step is a separate PR. The snapshot test shows whether a revert restores the old values.

## Open Questions

- Should `update_software.py` keep filling YAML fields from remote sources? If not, the script can be removed together with its tables.
