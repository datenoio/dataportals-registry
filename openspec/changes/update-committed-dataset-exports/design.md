## Context

`builder.py build` writes nine files to `data/datasets/`, and git tracks all of them. The table below was measured on 22 November 2026 with `git rev-list --objects --all -- data/datasets` and `git cat-file --batch-check='%(objectsize:disk)'`.

| File | Size now | Versions in history | Packed size, all versions | Packed cost per rebuild |
|---|---|---|---|---|
| `full.parquet` | 7.2 MB | 93 | 319 MB | ≈7.2 MB (no deltas) |
| `datasets.duckdb` | 26 MB | 53 | 193 MB | ≈6.8 MB (no deltas) |
| `catalogs.jsonl.zst` | 5.2 MB | 52 | 190 MB | ≈5.1 MB (no deltas) |
| `full.jsonl.zst` | 5.2 MB | 38 | 50 MB | 0 while it equals `catalogs.jsonl.zst` (same blob), otherwise ≈5 MB |
| `full.jsonl` | 77 MB | 234 | 120 MB | ≈0.5 MB (text deltas) |
| `software.jsonl` + `.zst` | 1.4 MB | 105 | 4.5 MB | ≈0.3 MB |

A full rebuild costs about 20 MB of packed history. While `data/scheduled/` is empty, `full.jsonl.zst` is byte-identical to `catalogs.jsonl.zst`, so git stores them as one blob.

The exports are read in four places:

- `hunt.py dedupe` and the `assign` UID cross-check open `datasets.duckdb` read-only, and fall back to `full.parquet` when the file is locked or missing. The fallback is already in the code.
- `builder.py` commands, `stats.py`, `enrich_ai.py` and `sync_ckan_ecosystem.py` read `full.jsonl` directly.
- `extract_openaire_portals.py` tries DuckDB, then parquet, then JSONL.
- The README, `docs/ai-consumers.md` and the agent guides tell people to open `datasets.duckdb` from the clone.

## Goals / Non-Goals

- Goals:
  - Cut the history growth caused by `datasets.duckdb`.
  - Remove about 108 MB from every checkout.
  - Keep all exports available to consumers.
  - Keep every command working in a fresh clone without a local build.
- Non-Goals:
  - Rewriting git history (`git filter-repo`). That is a separate decision: it needs a force-push and every clone must re-clone.
  - Changing the export formats or their columns.
  - Moving `full.parquet` or `catalogs.jsonl.zst` out of git. These are the remaining large costs, which the alternatives below discuss.

## Decisions

- **Decision:** Untrack `full.jsonl`, `full.jsonl.zst` and `datasets.duckdb`. Keep `catalogs.jsonl.zst`, `scheduled.jsonl(.zst)`, `software.jsonl(.zst)` and `full.parquet` tracked.
  - Why: this keeps every in-repo tool working with no download or build step. Parquet serves analytics and dedupe; the zstd JSONL serves record-level reads.
  - The maintainer chose this set over the alternatives below on 22 November 2026.
- **Decision:** A fresh clone reads the combined JSONL through `load_dataset_jsonl("full.jsonl")`. When the file is absent, the helper merges `catalogs.jsonl.zst` and `scheduled.jsonl.zst`.
  - Why: `load_dataset_jsonl` already implements the `.zst` fallback for `catalogs.jsonl`. Extending it keeps one code path.
- **Decision:** `build` keeps writing the three untracked files, and `.gitignore` lists them.
  - Why: local tools that prefer DuckDB still find it after a build, and the release step still has files to attach.

## Alternatives considered

- **Text only:** track `full.jsonl`, `software.jsonl` and `scheduled.jsonl`; move parquet, DuckDB and every `.zst` to releases.
  - About 0.7 MB per rebuild (−96%), and export changes stay visible in diffs.
  - Rejected for now: dedupe, UID checks and the README queries would need a local build or a download first.
- **Text plus parquet:** track `full.jsonl`, `software.jsonl` and `full.parquet`.
  - About 8 MB per rebuild (−60%).
  - Not chosen. It remains the next step if history growth is still a problem after this change.
- **Everything to releases:** cleanest history, but it breaks the README quickstart and the agent workflows that query the clone.

## Risks / Trade-offs

- **Raw GitHub URLs for the three files stop updating.** External scripts would read stale data.
  - Mitigation: delete the files from `main` rather than leave a frozen copy, so the URLs return 404 instead of stale data.
  - Mitigation: list the release-asset URLs in `docs/exports.md` and the CHANGELOG.
- **A contributor runs `build` and force-adds an ignored file.**
  - Mitigation: a test fails when `git ls-files data/datasets` lists any of the three files.
- **Savings are about a third of the per-rebuild cost.** `full.parquet` and `catalogs.jsonl.zst` remain the largest costs.
  - Mitigation: the "text plus parquet" alternative stays open as a follow-up.

## Migration Plan

1. Run `git rm --cached` on the three files and add them to `.gitignore` in the same commit.
2. Change the readers and `load_dataset_jsonl`, and add tests that run them with only the tracked files present.
3. Update the docs and the CHANGELOG, including the release-asset URLs.
4. Release notes for the next version list the breaking change and where to get the files.

Rollback: re-add the three files with `git add -f` and remove them from `.gitignore`. The code fallbacks can stay.

## Open Questions

- Should the release step upload the assets automatically, with a workflow on tag push? Today a maintainer attaches them by hand (`docs/releasing.md`, step 5).
