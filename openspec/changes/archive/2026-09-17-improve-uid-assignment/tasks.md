## 1. Incremental assignment

- [x] 1.1 Add `--new` flag to `assign`: collect candidate files from `git status --porcelain` (untracked + modified `*.yaml` under `data/entities/` and `data/scheduled/`)
- [x] 1.2 Within the candidate set, assign UIDs only to files missing a valid-format `uid`; never rewrite existing valid UIDs
- [x] 1.3 Determine the next free UID numbers from the full existing UID set (still computed from a fast full scan of `uid:` lines only, not full YAML parses)

## 2. Export collision cross-check

- [x] 2.1 After allocation, query `data/datasets/datasets.duckdb` read-only for the assigned UIDs; on lock, fall back to `full.parquet`
- [x] 2.2 Fail with a clear error listing colliding UIDs and their export record ids when a collision is detected; do not write any files in that case
- [x] 2.3 Skip the cross-check gracefully (with a warning) when exports are absent

## 3. Tests and docs

- [x] 3.1 Tests: --new limits writes to changed files, valid existing UIDs untouched, collision detection aborts before writes, missing exports warn-and-continue
- [x] 3.2 Update `docs/cli.md` assign section
- [x] 3.3 Run `pytest`
