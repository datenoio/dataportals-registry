## Context

Every discovery session currently rebuilds four pieces of plumbing as throwaway heredocs: search
API calls (FOFA base64 auth, Censys Platform API), export dedupe (DuckDB with manual parquet
fallback on lock), candidate probing (curl loops with timeouts and encoding bugs — GBK titles were
mis-decoded in sessions), and hunt-log appends (hand-written JSONL). Rate limiting is handled by
literal `sleep 60`/`sleep 180` commands, stalling sessions.

Constraints: the repository is a reference-data registry, not a runtime search service — the
toolkit is a local CLI for maintainers/agents, not a server. Scope boundary from AGENTS.md applies:
no production query API, no MCP server, no internet-wide scanner. Credentials stay in user
environment variables; nothing secret is written to the repo.

## Goals / Non-Goals

- Goals:
  - One tested implementation of FOFA/Censys query, dedupe, probe, and hunt-log append.
  - Candidates flow between steps as JSONL files so each step is composable and resumable.
  - Polite probing: bounded concurrency, per-host delay, short timeouts, no auth bypass.
- Non-Goals:
  - No crawling beyond candidate hosts; no recursive discovery.
  - No automatic record creation — `probe` output feeds `builder.py add-batch`
    (see `improve-catalog-ingestion`), keeping ingestion in one place.
  - No new third-party dependencies beyond the existing stack (`requests`); chardet only if
    already available, otherwise charset/meta heuristics.

## Decisions

- Decision: Single `scripts/hunt.py` typer CLI with `search` / `dedupe` / `probe` / `log`
  subcommands sharing a candidate JSONL schema.
  Alternatives considered: four separate scripts (rejected — shared candidate schema and HTTP
  helpers favor one module); extending `builder.py` (rejected — builder is the build/validation
  CLI; discovery is a distinct concern, consistent with `sync_ckan_ecosystem.py` being separate).
- Decision: Exponential backoff with jitter on 429 (base 2 s, cap 120 s, `--max-retries`
  default 5).
  Alternatives considered: fixed sleeps as used in sessions (rejected — 60–180 s stalls per query);
  no retry (rejected — FOFA 429s are routine).
- Decision: Dedupe reads exports, never YAML: DuckDB `read_only=True`, automatic fallback to
  `full.parquet` on `IOException` lock, matching the documented agent rule.
- Decision: Fingerprint matching reuses the published apidetect URL maps / software-index
  fingerprints instead of duplicating signature lists in hunt.py.
- Decision: `log` validates rows against a hunts schema derived from existing
  `dataquality/hunts.jsonl` conventions (`date`, `kind`, `target`, `list_url`, `added`,
  `skipped_dupes`, `status`, `notes`) before appending.

## Risks / Trade-offs

- Risk: Search API response schemas drift (FOFA/Censys) → Mitigation: isolate parsing behind one
  function per provider with tests; surface unexpected payloads verbatim for debugging.
- Risk: Concurrency accidentally floods a host → Mitigation: per-host serialization (one in-flight
  request per host) plus a global concurrency cap; defaults are conservative.
- Risk: Fingerprint false positives set wrong `software_id` → Mitigation: probe only annotates;
  the accept/reject decision stays with the agent per `docs/agents/discover.md`.

## Migration Plan

Docs updates point discovery sessions at `hunt.py`; existing heredoc recipes in
`docs/discovery-search-tools.md` are replaced by equivalent `hunt.py` commands. No data migration.

## Open Questions

- Should `probe` emit an `add-batch`-ready manifest directly (`--emit-manifest`)? Convenient but
  couples the tools; decide after `improve-catalog-ingestion` lands.
