## ADDED Requirements

### Requirement: Incremental UID Assignment

The `assign` command SHALL provide a `--new` mode that restricts UID assignment to YAML files
reported as untracked or modified by git, while never rewriting existing valid-format UIDs.

#### Scenario: Only new files processed

- **WHEN** `assign --new` runs with 5 untracked YAML files and 38,000 tracked files
- **THEN** UID assignment evaluates only the 5 untracked files
- **AND** tracked files with valid UIDs are not opened for writing

#### Scenario: Existing valid UID preserved

- **WHEN** a modified file already contains a valid `cdi########` UID
- **THEN** its UID is left unchanged

### Requirement: UID Collision Cross-Check Against Exports

The `assign` command SHALL verify newly allocated UIDs against the dataset exports before writing,
and SHALL abort without writing when a collision exists.

#### Scenario: Collision aborts assignment

- **WHEN** a newly allocated UID already exists in the exports under a different record id
- **THEN** the command fails listing the colliding UIDs and their export record ids
- **AND** no YAML file is modified

#### Scenario: Locked DuckDB falls back to parquet

- **WHEN** `data/datasets/datasets.duckdb` is locked by another process
- **THEN** the cross-check queries `data/datasets/full.parquet` instead

#### Scenario: Missing exports degrade gracefully

- **WHEN** neither the DuckDB nor the parquet export exists
- **THEN** the cross-check is skipped with a warning and assignment proceeds
