## Context

`add-hunt-toolkit` (archived 2026-09-17) added `hunt.py search|dedupe|probe|log` so sessions would stop rewriting FOFA clients, DuckDB queries, and hunt-log lines. Ten days of transcripts show the CLI is present and still bypassed. Sessions follow the last tool result and the always-injected `AGENTS.md` block. They do not reliably execute a procedure buried in the middle of `docs/agents/discover.md`.

Constraints from `AGENTS.md`: this repository is a reference-data registry. No production query API, no MCP server, no internet-wide scanner. Credentials stay in the environment. Record writing stays in `builder.py`; promotion stays in `promote_scheduled.py`.

## Goals / Non-Goals

- Goals:
  - A discovery session can run prior → search → probe → ingest → log without a custom script.
  - A repeated slice stops after one `prior` invocation.
  - An empty FOFA balance stops the search before another country sweep starts.
  - The next command is printed by the tool, so the agent does not re-read `builder.py` or the platform guides to recover flags.
  - The same command card is what `AGENTS.md`, the discovery cursor rule, and `llms.txt` tell the agent to run.
- Non-Goals:
  - Replacing `add-batch` or `promote_scheduled.py`. `ingest` only calls them.
  - A full apidetect sweep per candidate. Probe uses the root GET plus one capability URL.
  - Clustering `software.id: custom` into new software definitions. That stays a separate change. This change only stops agents from opening that work as a hunt.
  - Choosing the user’s hunt for them when they named a target. `next` applies only when no target was given.
  - Rebuilding `data/datasets/` or running `pytest` as part of ingest.

## Decisions

- Decision: Steer agents from tool stdout and from `AGENTS.md`, which the workspace rule always injects. Mirror the card in `.cursor/rules/catalog-discovery.mdc` (still requestable, not `alwaysApply`) and in the first section of `docs/agents/discover.md`.
  Alternatives considered: a longer discovery guide (rejected — 473 sessions already opened it and still wrote heredocs); `alwaysApply: true` on the cursor rule (rejected — it would load discovery instructions into unrelated code sessions; `AGENTS.md` is already always present).

- Decision: `prior` collapses targets to a software id by stripping a `.` or `-` suffix when the prefix is an id under `data/software/`. `arcgisserver.org` and `arcgisserver.edu` report as slices of `arcgisserver`. A slice logged `complete` within 14 days yields `decision: stop`. A new suffix yields `decision: continue` and lists covered suffixes. No history yields `decision: continue`.
  Alternatives considered: treating any `complete` row as global exhaustion (rejected — GeoServer’s 19 country passes still added 156 catalogs).

- Decision: `budget` prints FOFA `remain_api_data` and does not search. `search fofa` checks the same value before queries. `remain_api_data == 0` exits with `decision: stop-budget` and writes nothing. A `--query-file` longer than 25 lines is rejected unless `--allow-wide` is set.
  Alternatives considered: letting the agent check balance in a heredoc (rejected — that is the script this change removes); a hard ban on keyword files (rejected — a short vendor list is legitimate).

- Decision: Omitted `--out` writes under `/tmp/hunts/<slug>/`. An explicit `--out` path is honored, including `candidates.jsonl` in the working directory, so the existing search scenario stays valid.
  Alternatives considered: changing the default to a repo-local `.tmp_aq/` path (rejected — those files are already accumulating in the tree).

- Decision: `probe --software ID` GETs the root and one capability URL taken from the published apidetect map: GeoServer WMS GetCapabilities, ArcGIS Server `/rest/services?f=json`, CKAN `package_search`. `verdict` is `catalog` when the capability body has a collection size greater than zero or the existing fingerprint matches; `auth` on 401/403 with no further requests; `empty` on HTTP 200 with no fingerprint and a zero count; `dead` on connection failure, timeout, or 5xx; `unknown` when no capability parser applies and no fingerprint matches. `collection_count` is omitted when the body is not a shape this command parses.
  Alternatives considered: shelling out to full `detect_single` per host (rejected — per-row detection is why batch ingest already defaults detection off); inventing parsers for every software id (rejected — the heredoc volume is concentrated on these three).

- Decision: `ingest` keeps rows with `verdict: catalog` and `exists` not true, writes them with `add-batch` in scheduled mode and per-row detection off, promotes those ids with `promote_scheduled.py --id --probe`, then runs `validate-yaml --id` for each written id. It does not set `is_national`. It does not run `pytest` or `builder.py build`.
  Alternatives considered: writing entities directly (rejected — the scheduled gate and liveness-gated promotion already exist); leaving promotion to the agent (rejected — sessions stop after scheduled YAML).

- Decision: `next` prints at most five suggestions. It prefers `named-directory` and `country-indicators`, omits software targets whose latest row is `complete` within 14 days, and labels `custom-review` as deprioritized. It does not add catalogs.

- Decision: Each successful loop command ends with one `next:` line. `prior` stop and `budget` exhaustion print `next: none`.

## Risks / Trade-offs

- A country suffix encoded only in free-text `notes` can be missed, so `prior` may say continue for a finished slice. Mitigation: `prior` also scans `notes` for the suffix token; `log` from `ingest` records the target the agent passed, including the suffix.
- Capability parsers can mark a tile-only GeoServer as `catalog` if GetCapabilities lists layers. That matches current accept rules for a public OGC catalog. Empty viewers stay `empty`.
- `ingest` promotes on the probe’s verdict plus `promote_scheduled.py --probe`. A host that dies between the two probes stays scheduled. That is the existing hold-back behavior.
- Agents can still paste a heredoc. Mitigation is the card in `AGENTS.md` plus `next:` lines, not a runtime lock.

## Migration Plan

1. Land CLI commands and tests behind the existing `hunt.py` entry point.
2. Update `AGENTS.md`, the cursor rule, `discover.md`, `improve.md`, and `llms.txt` in the same change so the card matches the commands.
3. Leave existing `search --out` behavior in place. New defaults apply only when `--out` is omitted.
4. Rollback is reverting the change. `hunts.jsonl` rows written by `log` stay valid; no schema migration.

## Open Questions

- None. Collection parsing stays limited to GeoServer, ArcGIS Server, and CKAN until a later change names another family.
