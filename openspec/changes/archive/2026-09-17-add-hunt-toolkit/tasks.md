## 1. Search subcommand

- [x] 1.1 Implement `hunt.py search fofa QUERY` using `FOFA_EMAIL`/`FOFA_KEY` from the environment, base64 query encoding, `host,ip,port,protocol,title,domain` fields, and pagination via `--size`/`--max-pages`
- [x] 1.2 Implement `hunt.py search censys QUERY` using `CENSYS_API_TOKEN` from the environment with the documented Platform API query endpoint
- [x] 1.3 Add exponential backoff with jitter on HTTP 429 and transient 5xx (configurable `--max-retries`), instead of fixed sleeps
- [x] 1.4 Write normalized candidate JSONL rows: `host`, `url`, `title`, `source` (fofa|censys), `query`, plus raw fields under `extra`
- [x] 1.5 Fail with a clear message when required environment credentials are missing

## 2. Dedupe subcommand

- [x] 2.1 Implement `hunt.py dedupe candidates.jsonl` checking canonical URL and host against `data/datasets/datasets.duckdb` opened read-only
- [x] 2.2 Fall back to `data/datasets/full.parquet` automatically when DuckDB is locked
- [x] 2.3 Annotate each candidate with `exists` and `existing_id`; write `<input>.deduped.jsonl` and print a summary (new vs existing counts)

## 3. Probe subcommand

- [x] 3.1 Implement `hunt.py probe candidates.jsonl` with bounded concurrency (`--concurrency`, default 8), per-host minimum delay, and short connect/read timeouts
- [x] 3.2 Detect response encoding (charset header, meta tag, chardet fallback) so non-UTF-8 titles (e.g. GBK) decode correctly
- [x] 3.3 Match responses against published apidetect URL-map fingerprints and annotate `software_id` when a fingerprint matches
- [x] 3.4 Classify liveness per candidate reusing the `check_liveness.py` status vocabulary (live/dead/redirect/inconclusive/error)
- [x] 3.5 Never follow login forms or bypass 401/403; record the status and move on

## 4. Log subcommand

- [x] 4.1 Implement `hunt.py log --kind --target --added --skipped-dupes --status --notes [--list-url]` appending one row to `dataquality/hunts.jsonl`
- [x] 4.2 Validate the row against a hunts schema (required keys, ISO date defaulting to today, kind enum matching prior hunts) before appending

## 5. Tests and docs

- [x] 5.1 Tests: mocked FOFA/Censys pagination and 429 backoff, dedupe with parquet fallback, probe encoding/fingerprint/liveness classification, log validation
- [x] 5.2 Update `docs/discovery-search-tools.md` and `docs/agents/discover.md` to use `hunt.py` instead of heredoc recipes
- [x] 5.3 Run `pytest`
