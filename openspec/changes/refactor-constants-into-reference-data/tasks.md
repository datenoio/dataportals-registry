## 1. Safety net

- [ ] 1.1 Add `tests/test_constants_snapshot.py`. It records the value of every public name in `constants.py` and fails on any change that the fixture does not list.
- [ ] 1.2 Measure the import time of `constants` and record it in the PR.

## 2. Software facts into the software YAML

- [ ] 2.1 Add the optional `aliases` and `allowed_catalog_types` fields to `data/schemes/software.json`, and validate them in `builder.py validate-software`.
- [ ] 2.2 Migrate `SOFTWARE_NAME_ALIASES` into `aliases` and the literal part of `MAP_SOFTWARE_ALLOWED_CATALOG_TYPES` into `allowed_catalog_types`, then build both dicts from YAML in `constants.py`.
- [ ] 2.3 Resolve the 32 disagreements between the per-software URL/format dicts and the YAML (the YAML wins unless the maintainer decides otherwise). Then delete `SOFTWARE_DOCUMENTATION_URLS`, `SOFTWARE_REPOSITORY_URLS` and `SOFTWARE_SPECIFIC_EXPORT_FORMATS`, and change `update_software.py` to read the YAML. Keep the per-category `SOFTWARE_EXPORT_FORMATS`.
- [ ] 2.4 Update `docs/software-taxonomy.md` (adding a software definition) and `sync-software-maps` if needed.

## 3. Lookup tables into data/reference

- [ ] 3.1 Move `DOMAIN_LOCATIONS` to `data/reference/domain_locations.yaml`.
- [ ] 3.2 Move `LANGS_COUNTRIES` to `data/reference/tld_langs.yaml`.
- [ ] 3.3 Add a `registry_name` column to `countries.csv` and create `path_regions.yaml`, then build `COUNTRIES` from them. Update the country-name rule in `AGENTS.md`.

## 4. Duplicate reference files

- [ ] 4.1 Keep `country_langs.tsv`, `macroregion_countries.tsv` and `langs.tsv`, and delete the `.csv` copies after merging the `langs` differences.
- [ ] 4.2 Update the readers in `builder.py`, `enrich.py`, `enrich_ai.py`, `fix_important_issues.py`, and the docs (`docs/cli.md`, `docs/quality-rules.md`, `docs/vocabularies.md`).

## 5. Guard and verify

- [ ] 5.1 Add a guard test that fails when `constants.py` has a literal dict or list with more than 50 entries.
- [ ] 5.2 Confirm that `constants.py` is under 300 lines and that import time is within budget.
- [ ] 5.3 Run `pytest`, `ruff check scripts tests`, `python scripts/builder.py validate-yaml`, `validate-software` and `analyze-quality`. The quality reports must not change except for timestamps.
- [ ] 5.4 Run `openspec validate refactor-constants-into-reference-data --strict`.
