# Change: Stop committing the largest generated dataset exports

## Why

Every rebuild of `data/datasets/` adds about 20 MB to the git history, and there were 18 rebuilds in the 90 days before 22 November 2026. Most of that cost comes from binary and compressed files that git cannot store as deltas. `datasets.duckdb` alone costs about 7 MB per rebuild. A fresh checkout also carries about 108 MB of exports (`full.jsonl` 77 MB, `datasets.duckdb` 26 MB, `full.jsonl.zst` 5 MB) that GitHub releases already ship as assets.

## What Changes

- **BREAKING** Stop tracking `data/datasets/full.jsonl`, `data/datasets/full.jsonl.zst` and `data/datasets/datasets.duckdb` in git.
  - `builder.py build` still writes all three locally, and `.gitignore` lists them.
  - Releases keep attaching `full.jsonl.zst`, `full.parquet` and `datasets.duckdb`, as v1.27.0 already does.
- Keep tracking `catalogs.jsonl.zst`, `scheduled.jsonl`, `scheduled.jsonl.zst`, `software.jsonl`, `software.jsonl.zst` and `full.parquet`.
- Commands that read `full.jsonl` load it through `load_dataset_jsonl`, which already falls back to the compressed copy. When `full.jsonl` is absent, they merge `catalogs.jsonl.zst` and `scheduled.jsonl.zst`.
  - This covers `validate`, `report`, `add-single`, `add-list`, `add-legacy` and the batch manifest in `builder.py`, plus `stats.py`, `enrich_ai.py` and `sync_ckan_ecosystem.py`.
  - The same pattern already applies to `catalogs.jsonl`, which `build` deletes after compressing.
- `hunt.py dedupe` and the `assign` UID cross-check already use `full.parquet` when `datasets.duckdb` is missing. The specs now state that fallback for a missing file as well as for a locked one.
- The README quickstart, `docs/ai-consumers.md`, `docs/exports.md`, `docs/agents/query.md`, `docs/agents/discover.md`, `docs/agents/improve.md`, `docs/agents/contribute.md`, `docs/releasing.md` and `DATASHEET.md` now:
  - query `full.parquet` in a fresh clone;
  - send readers to the release assets for DuckDB and the combined JSONL.
- A test fails when one of the three local-only exports is tracked again.
- History is not rewritten. Old versions of these files stay in the existing packs.

## Impact

- Affected specs:
  - new `dataset-exports`;
  - modified `discovery-hunt-toolkit` (Candidate Deduplication Against Exports);
  - modified `uid-assignment` (UID Collision Cross-Check Against Exports).
- Affected code:
  - `scripts/builder.py`: `build`, the readers listed above, and `load_dataset_jsonl`;
  - `scripts/stats.py`, `scripts/enrich_ai.py`, `scripts/sync_ckan_ecosystem.py`;
  - `.gitignore`;
  - a new guard test.
- Affected users:
  - Anyone who opens `data/datasets/datasets.duckdb` or reads `data/datasets/full.jsonl` from a clone or a raw GitHub URL. They must run `python scripts/builder.py build`, download the release asset, or switch to `full.parquet` / `catalogs.jsonl.zst`.
  - Raw URLs for the six files that stay tracked keep working.
