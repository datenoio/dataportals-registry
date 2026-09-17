## Context

`scripts/builder.py` `_add_single_entry` (line 924) is the only programmatic record-creation path.
Session analysis shows agents bypass it with throwaway YAML writers whenever they add more than a
handful of records, because (a) it reloads the full export per call, (b) it cannot express
subregion/owner-type/is_national/custom id, and (c) two latent bugs make its output fail the
catalog schema. The registry adds ~1,000–5,000 records per release, nearly all through this path.

Constraints: Python 3.10–3.12, typer CLI, Cerberus schema (`data/schemes/catalog.json`), no new
heavy dependencies. Records remain individual YAML files; filename must equal `id`.

## Goals / Non-Goals

- Goals:
  - Every record written by the CLI validates against the catalog schema at write time.
  - One CLI command ingests a multi-record hunt result without per-record export reloads.
  - All metadata agents currently hand-edit (subregion, owner type, is_national, id) is expressible
    as CLI/manifest input.
- Non-Goals:
  - No changes to the YAML storage layout or the catalog schema itself.
  - No removal of `add-list` (kept for legacy lists; documented as superseded by `add-batch`).
  - No network probing by default in batch mode (`--no-detect` default).

## Decisions

- Decision: Manifest format is JSONL, one record per line, field names mirroring YAML keys
  (`url`, `name`, `software`, `catalog_type`, `country`, `subregion`, `owner_name`, `owner_type`,
  `owner_link`, `langs`, `description`, `is_national`, `id`).
  Alternatives considered: CSV (rejected — nested/list fields like `langs` encode poorly); YAML
  stream (rejected — agents already produce JSONL from probe steps, and JSONL streams append
  cleanly).
- Decision: Dedupe on canonical URL first (via `url_utils.canonicalize_url`), then host, then id;
  load `full.jsonl` once into memory (~0.5 s measured) instead of per record.
  Alternatives considered: DuckDB export queries per candidate (rejected — lock contention forced
  parquet fallbacks in sessions; a single in-memory set is faster and lock-free).
- Decision: Validate-then-write per batch: all rows are schema-checked before any file is written;
  invalid rows are reported and skipped, valid rows are written.
  Alternatives considered: fail-fast on first invalid row (rejected — hunts routinely have one or
  two bad rows; skipping them keeps the batch moving while still surfacing errors).
- Decision: UID assignment reuses `assign_by_dir` scoped to affected country directories after the
  batch writes, so `add-batch` output is immediately valid without a separate full-tree `assign`.
- Decision: `--subregion` writes both `owner.location.subregion` and
  `coverage[].location.subregion` with `level: 30` and places the file under `{CC}/{SUB}/{type}/`,
  matching the convention agents currently apply by hand.

## Risks / Trade-offs

- Risk: Write-time validation rejects records that legacy flows used to write (e.g. bare-string
  langs) → Mitigation: this is the intent; error messages name the failing field and the expected
  shape, and `add-list` legacy behavior is covered by tests before the stricter path lands.
- Risk: In-memory dedupe set grows with registry size → Mitigation: 38.8k records ≈ 70 MB JSONL
  parses in ~0.5 s; a set of canonical URLs/ids is a few MB — fine for a CLI batch run.
- Trade-off: `add-batch` duplicates some `_add_single_entry` logic → both share the same record
  assembly function so fixes apply to both paths.

## Migration Plan

No data migration. Existing YAML is untouched; only newly written records benefit. Docs updates
point agent workflows at `add-batch`; `add-single` remains for one-off adds.

## Open Questions

- Should `add-batch` support a `--promote` flag chaining into scheduled promotion once
  `improve-scheduled-promotion` lands? (Deferred — keep this change ingestion-only.)
