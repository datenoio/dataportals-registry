## 1. Selective promotion

- [x] 1.1 Add `--id ID [ID...]` filter to `promote_scheduled.py`; only matching scheduled files are processed
- [x] 1.2 Error clearly when a given `--id` matches no scheduled file

## 2. Subregion-aware placement

- [x] 2.1 When a record has `owner.location.subregion.id`, place it under `{CC}/{SUBREGION}/{type}/` and ensure `owner.location.level: 30`
- [x] 2.2 Keep `Federal/` placement for records without subregion
- [x] 2.3 Validate the subregion code against `data/reference/subregions/iso3166-2.csv`; warn and fall back to `Federal/` when unknown

## 3. Liveness-gated promotion

- [x] 3.1 Extract the probe/classify core of `check_liveness.py` into reusable functions
- [x] 3.2 Add `--probe` to `promote_scheduled.py`: classify each candidate `link` before moving
- [x] 3.3 Promote only `live`/`redirect` records when probing; leave `dead` in scheduled unchanged, mark `inconclusive`/`error` as reported-but-promotable with a warning
- [x] 3.4 Print a per-record probe summary line during promotion

## 4. Data-driven country hints

- [x] 4.1 Move hardcoded country heuristics (brasilio→BR, axiell→NL, dakar→SN, etc.) into `data/reference/country_hints.yaml`
- [x] 4.2 Load hints at runtime; keep exact-match-on-substring semantics identical to current behavior
- [x] 4.3 Document the file in `docs/scheduled.md`

## 5. Scheduled queue review report

- [x] 5.1 Add `review-scheduled` command: for every scheduled record, batch-check duplicates against entities, probe liveness (bounded concurrency), and show inferred country/subregion
- [x] 5.2 Output a summary table (promote-ready / dead / duplicate / needs-review) plus a JSONL report; never move or modify files
- [x] 5.3 Add `--probe`/`--no-probe` (default `--probe`) and `--country` filter

## 6. Tests and docs

- [x] 6.1 Tests: --id filter, subregion routing + level 30, unknown-subregion fallback, probe gating (mocked HTTP), country_hints.yaml loading, review-scheduled report contents
- [x] 6.2 Update `docs/scheduled.md`, `docs/agents/contribute.md`, `docs/agents/discover.md`
- [x] 6.3 Run `pytest` and `python scripts/builder.py validate-yaml`
