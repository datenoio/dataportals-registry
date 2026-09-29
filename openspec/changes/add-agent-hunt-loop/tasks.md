## 1. Prior gate and next hint

- [x] 1.1 Add `prior --target` to `scripts/hunt.py`: collapse software-id suffixes, read `dataquality/hunts.jsonl`, print `decision: stop|continue`, exit 0
- [x] 1.2 Treat a slice as finished when `status` is `complete` and `date` is within 14 days; list covered suffixes on `continue`
- [x] 1.3 Add `next`: at most five lines, `named-directory` and `country-indicators` before other kinds, omit slices completed within 14 days, mark `custom-review` deprioritized, write no catalog files

## 2. Search guard

- [x] 2.1 Add `budget` that prints FOFA `remain_api_data`; on 0 print `decision: stop-budget` and exit non-zero; on a positive balance print `decision: continue`
- [x] 2.2 Check the same balance at the start of `search fofa`; on 0 write no file and exit non-zero
- [x] 2.3 Add `--query-file` and reject files with more than 25 queries unless `--allow-wide`
- [x] 2.4 Add `--dedupe` on `search` using the existing DuckDB-then-parquet path
- [x] 2.5 When `--out` is omitted, write under `/tmp/hunts/<slug>/`; honor an explicit `--out`

## 3. Probe verdict

- [x] 3.1 On `probe --software`, GET the root plus one capability URL: GeoServer WMS GetCapabilities, ArcGIS Server `/rest/services?f=json`, CKAN `package_search`
- [x] 3.2 Set `verdict` to `catalog`, `auth`, `empty`, `dead`, or `unknown` and set `collection_count` only when the capability body exposes a size
- [x] 3.3 On 401 or 403 set `verdict: auth` and do not send another request to that host
- [x] 3.4 Do not call the full apidetect sweep from `probe`

## 4. Ingest

- [x] 4.1 Add `ingest` that keeps `verdict: catalog` rows with `exists` not true
- [x] 4.2 Call `add-batch` in scheduled mode with per-row detection off, without setting `is_national`
- [x] 4.3 Call `promote_scheduled.py --id --probe` and `validate-yaml --id` for written ids
- [x] 4.4 Do not invoke `pytest` or `builder.py build`

## 5. Next-command line

- [x] 5.1 End successful `prior`, `budget`, `search`, `dedupe`, `probe`, `ingest`, and `next` stdout with one `next:` line
- [x] 5.2 Use `next: none` for `decision: stop` and `decision: stop-budget`

## 6. Agent entry points

- [x] 6.1 Replace the Discover catalogs task in `AGENTS.md` with the command card: `prior` first, then follow `next:`; no FOFA, export, or probe heredoc when `hunt.py` covers the step; `validate-yaml --id` only
- [x] 6.2 Put the same card in `.cursor/rules/catalog-discovery.mdc` without setting `alwaysApply: true`
- [x] 6.3 Put the card at the top of `docs/agents/discover.md`, before hunt-type narratives
- [x] 6.4 Point the discovery bullet in `llms.txt` at `python scripts/hunt.py prior`
- [x] 6.5 Make the hunt-kind list in `docs/agents/improve.md` equal `HUNT_KINDS`

## 7. Tests and ignore rules

- [x] 7.1 Extend `tests/test_hunt.py` for prior stop/continue, alias collapse, budget refusal, query-file limit, default `/tmp` output, probe verdicts, ingest skip rules, and the `next:` line
- [x] 7.2 Ignore `.hunt_*` scratch scripts at the repo root in `.gitignore`
- [x] 7.3 Run `pytest tests/test_hunt.py` and `openspec validate add-agent-hunt-loop --strict`
