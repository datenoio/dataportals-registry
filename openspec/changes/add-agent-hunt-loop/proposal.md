# Change: Close the agent hunt loop on hunt.py

## Why

From 16–26 September 2026, 650 discovery sessions added 3,622 catalogs across 625 hunt-log rows, but the median session made 102 tool calls. About 9,602 of those calls were one-off Python: 1,738 hand-written FOFA clients and 3,940 hand-written HTTP probes, against 530 uses of `hunt.py search`. Agents re-read `scripts/builder.py` (2,071 reads) to recover `add-single` flags and opened `docs/agents/discover.md` in 473 sessions without following the toolkit. Repeated GeoServer (19) and ArcGIS Server (26) hunts still found catalogs; the waste was rebuilding the pipeline per country. FOFA balance hit zero on 22 September while keyword sweeps continued as `partial`.

`scripts/hunt.py` already implements search, dedupe, probe, and log (`specs/discovery-hunt-toolkit`). Agents bypass it because the CLI does not answer “already hunted?”, does not reject an empty FOFA balance, does not score a host as a catalog, and does not print the next command. Long guides are not a reliable control surface. The always-loaded `AGENTS.md` task and the command’s own stdout are.

## What Changes

- Extend `scripts/hunt.py` with `prior`, `budget`, `next`, inline `--dedupe`, a query-file guard, a catalog verdict on `probe`, and `ingest` that calls existing `add-batch` and `promote_scheduled.py`.
- Default hunt artifacts to `/tmp/hunts/<slug>/` when `--out` is omitted. Explicit `--out` is unchanged.
- Every loop command prints a final `next:` line naming the following command, or `next: none` when the hunt must stop.
- Put the same six-command card in `AGENTS.md` (always injected), `.cursor/rules/catalog-discovery.mdc`, the top of `docs/agents/discover.md`, and the discovery bullet in `llms.txt`.
- Sync the hunt-kind list in `docs/agents/improve.md` with `HUNT_KINDS` in `scripts/hunt.py`.

## Impact

- Affected specs: `discovery-hunt-toolkit`, `agent-documentation`
- Affected code: `scripts/hunt.py`, `tests/test_hunt.py`, `AGENTS.md`, `.cursor/rules/catalog-discovery.mdc`, `docs/agents/discover.md`, `docs/agents/improve.md`, `llms.txt`, `.gitignore`
- Unchanged: catalog schema, `add-single` / `add-batch` behavior, apidetect URL maps, production APIs
