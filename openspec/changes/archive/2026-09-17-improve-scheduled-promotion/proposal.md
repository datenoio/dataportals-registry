# Change: Selective, subregion-aware, liveness-gated scheduled promotion

## Why

`scripts/promote_scheduled.py` is the final step of every discovery session, and session analysis
shows it forcing manual work: it routes every record into `Federal/` (hardcoded `admin_dir`), so
subregion records are hand-moved afterwards; it carries hardcoded one-off country heuristics
(`brasilio→BR`, `dakar→SN`, …, lines 163–199) that accumulate as tech debt; it has no liveness
gate even though `docs/agents/discover.md` requires a live GET before promotion, so agents probe
URLs one by one with curl/WebFetch (205 timeout mentions in 150 sessions); and it has no `--id`
filter, so it promotes the entire `data/scheduled/` queue and mixes records from different
sessions. Reviewing the existing scheduled queue is likewise manual: agents write throwaway review
scripts and probe records one at a time.

## What Changes

- Add `--id ID [ID...]` to promote only specific scheduled records.
- Route by subregion: when a record has `owner.location.subregion.id`, place it under
  `{CC}/{SUBREGION}/{type}/` instead of `Federal/`.
- Add `--probe`: before moving a record, classify its `link` liveness reusing the
  `check_liveness.py` status vocabulary; keep `dead` records in scheduled (or mark `inactive`),
  promote only `live`/`redirect` records.
- Move the hardcoded country heuristics into a data file
  (`data/reference/country_hints.yaml`) loaded at runtime.
- Add `review-scheduled` report command: batch duplicate check against entities, liveness probe,
  and country-inference summary for the whole scheduled queue, without moving anything.

## Impact

- Affected specs: `scheduled-promotion` (new capability)
- Affected code: `scripts/promote_scheduled.py`, `scripts/check_liveness.py` (shared classify /
  probe helpers), `data/reference/country_hints.yaml` (new), `tests/test_promote_scheduled.py`,
  `docs/scheduled.md`, `docs/agents/contribute.md`, `docs/agents/discover.md`
