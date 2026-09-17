## Context

`promote_scheduled.py` (352 lines) moves every scheduled YAML into `data/entities/` but hardcodes
`admin_dir = "Federal"` at lines 270 and 301, embeds ~20 one-off country heuristics inline
(lines 163–199), and performs no liveness check. The documented agent loop requires "live GET,
promote in the same session", so agents currently probe manually before running the script, and
hand-move subregion records afterwards. `check_liveness.py` already implements a probe/classify
core with a stable status vocabulary (`live`, `dead`, `redirect`, `inconclusive`, `error`) defined
by the `catalog-liveness` spec.

## Goals / Non-Goals

- Goals:
  - Promotion of exactly the records a session added (`--id`), into the correct directory
    (subregion-aware), gated by an automated liveness probe (`--probe`).
  - A read-only `review-scheduled` report so the scheduled queue can be triaged in one command.
  - Country heuristics editable as data, not code.
- Non-Goals:
  - No changes to the liveness classification rules themselves (owned by `catalog-liveness`).
  - No automatic deletion of dead scheduled records — review stays human/agent-driven.
  - No YAML round-trip formatting preservation work (existing safe_dump rewrite is accepted).

## Decisions

- Decision: Reuse `check_liveness.py` classification by extracting its probe core into importable
  functions, keeping one liveness vocabulary across the repo.
  Alternatives considered: duplicating a small probe in promote_scheduled (rejected — two
  vocabularies would drift); calling check_liveness as a subprocess per record (rejected —
  process-per-record overhead and report-file coupling).
- Decision: Subregion routing reads `owner.location.subregion.id` first, then
  `coverage[].location.subregion.id`; unknown codes warn and fall back to `Federal/` rather than
  failing the batch.
  Alternatives considered: hard fail on unknown subregion (rejected — a typo shouldn't block
  promoting the rest of a session's records).
- Decision: With `--probe`, `dead` records stay in scheduled untouched; `inconclusive` (403/bot
  protection) and `error` records are promoted with a warning, because 403 is frequently bot
  protection on otherwise healthy portals (per `catalog-liveness` semantics).
- Decision: Country hints move to `data/reference/country_hints.yaml` as a list of
  `{pattern, country}` rules evaluated in file order, preserving current substring semantics.
- Decision: `review-scheduled` is a separate read-only command (not a `--dry-run` flag) because it
  adds dedupe and country-inference reporting beyond promotion's move preview.

## Risks / Trade-offs

- Risk: `--probe` adds network time to promotion → Mitigation: bounded concurrency, short timeouts,
  and probing is opt-in per run.
- Risk: Moving heuristics to data changes behavior if patterns reorder → Mitigation: tests pin the
  current mapping outcomes before and after the move.
- Trade-off: `inconclusive` promotion with warning may promote bot-protected dead sites → accepted,
  matches existing liveness semantics that 403 is not `dead`.

## Migration Plan

No data migration. Existing entities are untouched; only future promotions use the new routing.
`country_hints.yaml` starts with exactly the rules currently hardcoded.

## Open Questions

- Should `review-scheduled` also propose `software.id` from fingerprints (overlap with
  `add-hunt-toolkit` probe)? Deferred to keep this change focused on placement and liveness.
