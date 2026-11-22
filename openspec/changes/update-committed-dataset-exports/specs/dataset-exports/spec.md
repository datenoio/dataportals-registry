## ADDED Requirements

### Requirement: Committed Export Set

The repository SHALL track only these files under `data/datasets/`:

- `catalogs.jsonl.zst`
- `scheduled.jsonl`
- `scheduled.jsonl.zst`
- `software.jsonl`
- `software.jsonl.zst`
- `full.parquet`

`builder.py build` SHALL still write `full.jsonl`, `full.jsonl.zst` and `datasets.duckdb`, and `.gitignore` SHALL list those three paths.

#### Scenario: Build leaves local-only exports untracked

- **WHEN** a contributor runs `python scripts/builder.py build`
- **THEN** `full.jsonl`, `full.jsonl.zst` and `datasets.duckdb` exist in `data/datasets/`
- **AND** `git status` reports none of them as untracked or modified

#### Scenario: Guard test rejects a tracked local-only export

- **WHEN** `git ls-files data/datasets` lists `full.jsonl`, `full.jsonl.zst` or `datasets.duckdb`
- **THEN** the test suite fails and names the file

### Requirement: Combined Export Fallback

Commands that read the combined catalog export SHALL load `data/datasets/full.jsonl` when it exists. Otherwise they SHALL load the records of `catalogs.jsonl.zst` followed by those of `scheduled.jsonl.zst`.

#### Scenario: Fresh clone without a local build

- **WHEN** `full.jsonl` is absent and `catalogs.jsonl.zst` contains a record with link `https://catalog.data.gov`
- **AND** a contributor runs `python scripts/builder.py add-single https://catalog.data.gov --scheduled`
- **THEN** the command reports that the catalog already exists
- **AND** writes no YAML file

#### Scenario: Local build present

- **WHEN** `full.jsonl` exists
- **THEN** the command reads `full.jsonl` and does not decompress `catalogs.jsonl.zst`

### Requirement: Release Assets Carry Local-Only Exports

Each GitHub release of the registry SHALL attach `full.jsonl.zst`, `full.parquet` and `datasets.duckdb`, all built from the tagged commit.

#### Scenario: Consumer downloads DuckDB without cloning

- **WHEN** a consumer opens the latest GitHub release
- **THEN** `datasets.duckdb`, `full.parquet` and `full.jsonl.zst` are listed as assets
- **AND** their record counts match the counts in the release notes
