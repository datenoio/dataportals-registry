# record-enrichment Specification

## Purpose
TBD - created by archiving change add-record-update-tooling. Update Purpose after archive.
## Requirements
### Requirement: Single-Record Field Update

The CLI SHALL provide `set-field --id ID --path dotted.path --value VALUE` that updates one field
on an existing record, parses typed values, and re-validates the record against the catalog schema
before saving.

#### Scenario: Typed value set on nested path

- **WHEN** `set-field --id example --path owner.location.level --value 30` runs
- **THEN** the record's `owner.location.level` is the integer `30`, not the string `"30"`
- **AND** intermediate dicts are created when missing

#### Scenario: Append to list field

- **WHEN** `set-field --id example --path tags --value openbudget --append` runs
- **THEN** `openbudget` is appended to the existing `tags` list rather than replacing it

#### Scenario: Protected fields refused

- **WHEN** `--path` targets `uid` or `id`
- **THEN** the command fails with an error explaining these fields are managed by dedicated
  commands
- **AND** the file is unchanged

#### Scenario: Schema-invalid update refused

- **WHEN** an update would make the record fail catalog schema validation
- **THEN** the command prints the validation errors
- **AND** the file on disk is unchanged

### Requirement: Bulk Field Update Manifest

The CLI SHALL provide `enrich-batch manifest.jsonl` that applies `{id, set: {path: value}}` or
`{id, merge: {field: value}}` updates across many records, dry-run by default with a `--write`
apply mode.

#### Scenario: Dry-run shows diff without writing

- **WHEN** `enrich-batch manifest.jsonl` runs without `--write`
- **THEN** a per-record diff summary (field, old value, new value) is printed
- **AND** no YAML file is modified

#### Scenario: Write applies valid updates only

- **WHEN** `enrich-batch manifest.jsonl --write` processes 50 rows where 2 target unknown ids and
  1 would fail schema validation
- **THEN** 47 records are updated
- **AND** the summary lists the 2 unknown ids and the 1 invalid row with its validation error

#### Scenario: uid never modified by bulk updates

- **WHEN** a manifest row attempts to set `uid`
- **THEN** the row is rejected with an error
- **AND** remaining valid rows still apply

