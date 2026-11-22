# Change: Move lookup tables out of constants.py into data files

## Why

`scripts/constants.py` has 2,640 lines, and 2,123 of them are literal data tables. It is the most-changed script: 28 commits in the six months to 22 November 2026, which makes it a frequent source of merge conflicts. Several tables are second copies of data that already exists elsewhere, and the copies have drifted:

- `SOFTWARE_DOCUMENTATION_URLS` (344 entries), `SOFTWARE_REPOSITORY_URLS` (144) and `SOFTWARE_SPECIFIC_EXPORT_FORMATS` (87) repeat the `documentation_url`, `repository_url` and `export_formats` fields of `data/software/*.yaml`. 20 documentation URLs, 6 repository URLs and 6 export-format lists disagree with the YAML. Only `update_software.py` reads these tables.
- `COUNTRIES` (199 entries) partly repeats `data/reference/countries.csv`. 147 names match, and 52 entries differ or are regional blocs (`EU`, `ASEAN`, `World`, …). `AGENTS.md` tells contributors to use either one.
- `data/reference/` holds two copies each of `country_langs` and `macroregion_countries`: the `.csv` and `.tsv` files are byte-identical, and both are tab-separated. `langs.csv` and `langs.tsv` have diverged. `builder.py` reads the `.csv` files, while `enrich.py` and `enrich_ai.py` read the `.tsv` files.

## What Changes

- Software metadata has one source: `data/software/*.yaml`.
  - Delete `SOFTWARE_DOCUMENTATION_URLS`, `SOFTWARE_REPOSITORY_URLS` and `SOFTWARE_SPECIFIC_EXPORT_FORMATS`. `SOFTWARE_EXPORT_FORMATS` stays: it holds per-category defaults (14 lines), not per-software data.
  - Change `update_software.py` to read the YAML.
  - The maintainer resolves the 32 disagreeing values once (listed in `design.md`), with the YAML value as the default.
- Add two optional fields to `data/schemes/software.json`:
  - `aliases` (list of names): replaces `SOFTWARE_NAME_ALIASES` (782 aliases for 294 software ids);
  - `allowed_catalog_types` (list): replaces the hand-written part of `MAP_SOFTWARE_ALLOWED_CATALOG_TYPES` (87 entries).

  `constants.py` builds both dicts from the YAML at import time, the same way it already loads `MAP_SOFTWARE_OWNER_CATALOG_TYPE`.
- Move the remaining lookup tables to `data/reference/`:
  - `DOMAIN_LOCATIONS` (343 lines) → `domain_locations.yaml`;
  - `LANGS_COUNTRIES` (top-level domain → language, 121 lines) → `tld_langs.yaml`;
  - `COUNTRIES` → a `registry_name` column in `countries.csv`, plus `path_regions.yaml` for the bloc folders.
- Keep one copy of each reference table. Use the `.tsv` name for the three tab-separated pairs, merge the `langs` entries that differ, and update every reader.
- `constants.py` keeps its public names. Importers do not change. The goal is under 300 lines of loading code and small enums.
- A snapshot test checks that every public constant has the same value before and after the move. A guard test fails when `constants.py` gains a literal dict or list with more than 50 entries.
- **BREAKING (data contributors)** New software aliases and allowed catalog types go in the software YAML, not in `constants.py`.

## Impact

- Affected specs: new `reference-data`.
- Affected code and data:
  - `scripts/constants.py`, `scripts/update_software.py`;
  - `scripts/builder.py`, `scripts/enrich.py`, `scripts/enrich_ai.py`, `scripts/fix_important_issues.py` (reference file paths);
  - `data/schemes/software.json`, `data/software/**/*.yaml` (new fields);
  - `data/reference/` (new and merged files);
  - `AGENTS.md`, `docs/software-taxonomy.md`, `docs/vocabularies.md`.
- Independent of `refactor-shared-script-library`. It can land before or after.
