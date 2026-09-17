# validation-helpers Specification

## Purpose
TBD - created by archiving change add-validation-helpers. Update Purpose after archive.
## Requirements
### Requirement: Schema Enum Introspection Command

The CLI SHALL provide `schema-values FIELD` that prints the allowed values for a catalog schema
field, combining schema enums with reference vocabularies for fields the schema leaves open.

#### Scenario: Enum field values listed

- **WHEN** `schema-values catalog_type` runs
- **THEN** the allowed catalog types from `data/schemes/catalog.json` are printed, one per line

#### Scenario: Vocabulary-backed field values listed

- **WHEN** `schema-values owner.type` runs
- **THEN** the canonical owner types from `data/reference/owner_types.yaml` are printed

#### Scenario: Subregion values filtered by country

- **WHEN** `schema-values owner.location.subregion --country PT` runs
- **THEN** only `PT-*` codes from `data/reference/subregions/iso3166-2.csv` are printed

#### Scenario: Unknown field rejected

- **WHEN** `schema-values` is given a field with no known enum or vocabulary
- **THEN** the command exits with an error listing supported fields

### Requirement: Git-Scoped YAML Validation

`validate-yaml` SHALL provide a `--changed` mode that validates only YAML files reported as
untracked or modified by git.

#### Scenario: Only touched files validated

- **WHEN** `validate-yaml --changed` runs with 3 modified and 2 untracked YAML files
- **THEN** exactly those 5 files are validated
- **AND** the summary reports totals for that set only

#### Scenario: Changed mode excludes other selectors

- **WHEN** `--changed` is combined with `--file` or `--id`
- **THEN** the command fails with an error explaining the flags are mutually exclusive

#### Scenario: Clean tree validates nothing

- **WHEN** `validate-yaml --changed` runs on a clean git tree
- **THEN** it reports zero files and exits successfully

