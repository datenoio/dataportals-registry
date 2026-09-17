# Change: Add schema introspection and git-scoped validation helpers

## Why

Session transcripts show agents repeatedly grepping `data/schemes/catalog.json` and reference
files to discover allowed enum values (`owner.type`, `catalog_type`, `langs` shape) while writing
records — a discoverability gap that also caused schema violations. And while
`validate-yaml --id` covers single records, there is no fast pre-commit check for "the files I
just touched": full `validate-yaml` walks all 38k+ files, so agents either wait for it or skip it.

## What Changes

- Add `builder.py schema-values FIELD`: print the allowed values for a schema field
  (`catalog_type`, `status`, `access_mode`, …) combining `data/schemes/catalog.json` enums with
  reference vocabularies (`data/reference/owner_types.yaml`, `data/reference/langs.csv`,
  `data/reference/subregions/iso3166-2.csv`) for fields the schema leaves open.
- Add `validate-yaml --changed`: validate only YAML files reported as untracked or modified by
  `git status --porcelain`, for fast pre-commit checks during add/update sessions.
- Both commands are read-only.

## Impact

- Affected specs: `validation-helpers` (new capability)
- Affected code: `scripts/builder.py` (`validate_yaml`, new `schema_values`),
  `scripts/constants.py` (reference loaders), `tests/test_builder.py`, `docs/cli.md`
