## MODIFIED Requirements

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

#### Scenario: Missing DuckDB falls back to parquet

- **WHEN** `data/datasets/datasets.duckdb` does not exist, as in a fresh clone without a local build
- **THEN** the cross-check queries `data/datasets/full.parquet`

#### Scenario: Missing exports degrade gracefully

- **WHEN** neither the DuckDB nor the parquet export exists
- **THEN** the cross-check is skipped with a warning and assignment proceeds
