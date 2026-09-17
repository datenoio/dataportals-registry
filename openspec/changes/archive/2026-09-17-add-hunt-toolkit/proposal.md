# Change: Add hunt toolkit CLI for discovery sessions

## Why

Discovery hunts are ~95% of recent agent sessions, and each one re-implements the same plumbing
as throwaway Python heredocs: 769 ad-hoc HTTP-probe scripts, 350 ad-hoc DuckDB dedupe queries,
and 96 hand-crafted `dataquality/hunts.jsonl` appends in 150 sessions. FOFA/Censys authentication,
pagination, and 429 backoff are re-written per session (with literal `sleep 60`/`sleep 180` waits
in transcripts), DuckDB lock errors force manual parquet fallbacks, and hand-appended hunt-log rows
risk malformed JSONL. One shared, tested CLI removes this per-session re-implementation.

## What Changes

- New `scripts/hunt.py` (typer) with four subcommands:
  - `search fofa|censys QUERY --out candidates.jsonl` — credentials from environment
    (`FOFA_EMAIL`/`FOFA_KEY`, `CENSYS_API_TOKEN`), pagination, and exponential backoff with jitter
    on HTTP 429; writes a normalized candidate JSONL (`host`, `url`, `title`, `source`, `query`).
  - `dedupe candidates.jsonl` — batch duplicate check of candidate hosts/URLs against dataset
    exports; DuckDB read-only first, automatic `full.parquet` fallback on lock; annotates each
    candidate with `exists: true/false` and the existing record `id`.
  - `probe candidates.jsonl` — bounded-concurrency GET with per-host politeness delay, short
    timeouts, response-encoding detection (e.g. GBK titles), and software fingerprint matching
    against the published apidetect URL maps; annotates `http_code`, `liveness`, matched
    `software_id`, and page `title`.
  - `log --kind K --target T --added N ...` — appends one schema-validated row to
    `dataquality/hunts.jsonl`.
- No internet-wide scanning: the toolkit only queries the documented search APIs and probes
  candidate hosts already produced by a search or list step.

## Impact

- Affected specs: `discovery-hunt-toolkit` (new capability)
- Affected code: `scripts/hunt.py` (new), `scripts/url_utils.py` (reuse), `scripts/apidetect.py`
  (reuse published URL maps), `dataquality/hunts.jsonl`, `tests/test_hunt.py` (new),
  `docs/discovery-search-tools.md`, `docs/agents/discover.md`
