# catalog-ingestion Specification

## Purpose
TBD - created by archiving change improve-catalog-ingestion. Update Purpose after archive.
## Requirements
### Requirement: Schema-Valid Record Creation

The CLI SHALL write only records that validate against `data/schemes/catalog.json`. Language
entries SHALL be emitted as `{id, name}` objects resolved from `data/reference/langs.csv`, and
the record's primary language SHALL be auto-filled from the resolved country when not given
explicitly.

#### Scenario: Language code resolves to a schema-valid dict

- **WHEN** `add-single` is run with `--lang it`
- **THEN** the written record contains `langs: [{id: IT, name: Italian}]` per
  `data/reference/langs.csv`
- **AND** the record passes `validate-yaml --id` without manual edits

#### Scenario: Language auto-filled from country

- **WHEN** `add-single` is run with `--country DE` and no `--lang`
- **THEN** the written record contains the German language entry from the country-language
  reference

#### Scenario: Unknown language code rejected

- **WHEN** `add-single` is run with a `--lang` code absent from `data/reference/langs.csv`
- **THEN** the command fails with an error naming the unknown code
- **AND** no file is written

#### Scenario: Invalid record refused at write time

- **WHEN** assembled record content fails catalog schema validation for any field
- **THEN** the command prints the schema errors and does not write the YAML file

### Requirement: Rich Add-Single Options

`add-single` SHALL accept `--subregion`, `--owner-type`, `--is-national`, `--id`, and
`--no-detect` options so a complete record can be created without post-hoc hand edits.

#### Scenario: Subregion sets location and directory

- **WHEN** `add-single` runs with `--country PT --subregion PT-11`
- **THEN** the record sets `owner.location.subregion.id: PT-11` and
  `coverage[].location.subregion.id: PT-11` with `level: 30`
- **AND** the file is written under `data/scheduled/PT/PT-11/{type}/` (or `data/entities/` when
  `--no-scheduled`)

#### Scenario: Invalid subregion rejected

- **WHEN** `--subregion` is not present in `data/reference/subregions/iso3166-2.csv`
- **THEN** the command fails with an error referencing the reference file
- **AND** no file is written

#### Scenario: Owner type validated against vocabulary

- **WHEN** `--owner-type` is a synonym listed in `data/reference/owner_types.yaml`
- **THEN** the canonical owner type is written
- **WHEN** `--owner-type` is unknown
- **THEN** the command fails listing canonical values

#### Scenario: Custom id for path-based tenants

- **WHEN** `add-single "https://webgis.sit-puglia.it/comune/" --id webgissitpugliaitcomune`
- **THEN** the record id and filename use the given id instead of the domain-derived id

#### Scenario: Detection probe skipped

- **WHEN** `add-single` runs with `--no-detect`
- **THEN** no `detect_single` network probe runs and the record is still written

### Requirement: Batch Manifest Ingestion

The CLI SHALL provide `add-batch manifest.jsonl` that creates one record per manifest row, where
each row MAY set `url`, `name`, `software`, `catalog_type`, `country`, `subregion`,
`owner_name`, `owner_type`, `owner_link`, `langs`, `description`, `is_national`, and `id`.

#### Scenario: Batch of verified finds ingested in one run

- **WHEN** a manifest with 20 valid rows is ingested
- **THEN** 20 schema-valid YAML files are written under the correct country/subregion/type
  directories
- **AND** export datasets are loaded at most once during the run

#### Scenario: Per-row validation errors do not block valid rows

- **WHEN** a manifest contains 18 valid rows and 2 rows failing schema validation
- **THEN** the 18 valid records are written
- **AND** the summary lists the 2 invalid rows with their validation errors

### Requirement: Batch Deduplication

`add-batch` SHALL skip rows whose canonical URL, host, or id already exists in the exports or
earlier in the manifest, and SHALL report each skip with the existing record id.

#### Scenario: Duplicate URL skipped

- **WHEN** a manifest row's URL canonicalizes to an existing record's `link`
- **THEN** no file is written for that row
- **AND** the summary names the existing record id

#### Scenario: Duplicate id inside the manifest skipped

- **WHEN** two manifest rows resolve to the same id
- **THEN** only the first is written
- **AND** the second is reported as an in-manifest duplicate

### Requirement: Batch UID Assignment

`add-batch` SHALL assign `uid` values to all newly written records before exiting, scoped to the
affected directories rather than a full-tree walk.

#### Scenario: UIDs present after batch

- **WHEN** `add-batch` completes with records written
- **THEN** every written file contains a `uid` in `cdi########` (entities) or `temp########`
  (scheduled) format
- **AND** no `uid` collides with an existing record

