## MODIFIED Requirements

### Requirement: Candidate Deduplication Against Exports

The toolkit SHALL provide `hunt.py dedupe candidates.jsonl` that batch-checks candidate hosts and
canonical URLs against dataset exports and annotates each row with `exists` and `existing_id`.

#### Scenario: Existing host annotated

- **WHEN** a candidate host matches a `link` host in the exports
- **THEN** the output row has `exists: true` and the matching record's `id` in `existing_id`

#### Scenario: DuckDB lock falls back to parquet

- **WHEN** `data/datasets/datasets.duckdb` cannot be opened due to a lock
- **THEN** dedupe automatically queries `data/datasets/full.parquet` instead
- **AND** completes without manual intervention

#### Scenario: Missing DuckDB falls back to parquet

- **WHEN** `data/datasets/datasets.duckdb` does not exist, as in a fresh clone without a local build
- **THEN** dedupe queries `data/datasets/full.parquet`
- **AND** completes without manual intervention
