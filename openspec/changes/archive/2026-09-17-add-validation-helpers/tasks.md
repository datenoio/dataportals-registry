## 1. schema-values command

- [x] 1.1 Implement `builder.py schema-values FIELD` printing allowed values for schema enum fields (catalog_type, status, access_mode) from `data/schemes/catalog.json`
- [x] 1.2 Map open fields to reference vocabularies: `owner.type` → `owner_types.yaml`, `langs` → `langs.csv`, `owner.location.subregion` → `subregions/iso3166-2.csv` (with `--country` filter), `software.id` → `data/software/`
- [x] 1.3 Unknown field names exit with an error listing supported fields

## 2. Git-scoped validation

- [x] 2.1 Add `--changed` to `validate-yaml`: collect untracked + modified `*.yaml` under `data/entities/` and `data/scheduled/` from `git status --porcelain`
- [x] 2.2 Validate exactly that set with the existing Cerberus validator and report per-file errors
- [x] 2.3 Make `--changed` mutually exclusive with `--file`/`--id`

## 3. Tests and docs

- [x] 3.1 Tests: schema-values output for enum and vocabulary-backed fields, unknown-field error, --changed validates only touched files, flag exclusivity
- [x] 3.2 Update `docs/cli.md`
- [x] 3.3 Run `pytest`
