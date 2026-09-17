# discovery-hunt-toolkit Specification

## Purpose
TBD - created by archiving change add-hunt-toolkit. Update Purpose after archive.
## Requirements
### Requirement: Search API Query Command

The toolkit SHALL provide `hunt.py search fofa|censys QUERY` that queries the documented search
APIs using credentials from environment variables, paginates results, and writes a normalized
candidate JSONL file. Rate-limited responses SHALL be retried with exponential backoff and jitter.

#### Scenario: FOFA query writes normalized candidates

- **WHEN** `hunt.py search fofa 'title="GeoScene"' --out candidates.jsonl` runs with
  `FOFA_EMAIL`/`FOFA_KEY` set
- **THEN** `candidates.jsonl` contains one row per result with `host`, `url`, `title`,
  `source: fofa`, and the originating `query`
- **AND** pagination fetches up to `--max-pages` pages

#### Scenario: Missing credentials fail fast

- **WHEN** a search runs without the required environment variables
- **THEN** the command exits with an error naming the missing variables
- **AND** no output file is written

#### Scenario: Rate limit handled with backoff

- **WHEN** the search API returns HTTP 429
- **THEN** the request is retried with exponential backoff and jitter up to `--max-retries`
- **AND** no fixed multi-minute sleep stalls the session

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

### Requirement: Candidate Probing with Fingerprint Detection

The toolkit SHALL provide `hunt.py probe candidates.jsonl` that GETs each candidate with bounded
concurrency, per-host politeness delay, short timeouts, and response-encoding detection, and
annotates liveness, HTTP status, page title, and matched `software_id` from published apidetect
fingerprints.

#### Scenario: Live candidate classified

- **WHEN** a candidate returns HTTP 200
- **THEN** the output row records `liveness: live`, the status code, and the decoded `title`

#### Scenario: Non-UTF-8 title decoded

- **WHEN** a candidate responds with a GBK-encoded page
- **THEN** the recorded `title` is correctly decoded rather than garbled

#### Scenario: Fingerprint match annotates software

- **WHEN** a candidate response matches a published fingerprint (e.g. `/api/3/action/status_show`)
- **THEN** the row is annotated with the matching `software_id` (e.g. `ckan`)

#### Scenario: Authentication walls respected

- **WHEN** a candidate returns 401 or 403
- **THEN** the status is recorded and no attempt is made to bypass authentication

### Requirement: Hunt Log Append Command

The toolkit SHALL provide `hunt.py log` that appends one schema-validated row to
`dataquality/hunts.jsonl`.

#### Scenario: Valid hunt row appended

- **WHEN** `hunt.py log --kind software-instance --target geoscene --added 5 --status complete
  --notes "..."` runs
- **THEN** one JSONL row with `date` (defaulting to today), `kind`, `target`, `added`,
  `skipped_dupes`, `status`, and `notes` is appended to `dataquality/hunts.jsonl`

#### Scenario: Invalid row rejected

- **WHEN** a required field is missing or `kind` is not a recognized hunt kind
- **THEN** the command fails with a validation error
- **AND** `dataquality/hunts.jsonl` is not modified

