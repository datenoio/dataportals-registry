# Change: Incremental UID assignment with export collision check

## Why

`builder.py assign` walks and YAML-parses all 38k+ entity files on every run to find the handful
of records missing a `uid` — it ran 215 times in the 200 most recent agent sessions, once per
discovery hunt. Sessions also hit UID-collision concerns when newly assigned numbers diverged from
the dataset exports, with no automated way to cross-check. Assignment should be incremental and
export-aware.

## What Changes

- Add `assign --new`: restrict the scan to untracked and modified YAML files reported by
  `git status --porcelain` (plus any files whose `uid` fails the format check within that set),
  instead of walking the whole tree.
- Add an export cross-check: after allocation, compare assigned UIDs against
  `data/datasets/datasets.duckdb` (read-only, parquet fallback on lock) and fail loudly on
  collision.
- Keep the current full-tree walk as the default behavior; `--new` is opt-in for interactive
  sessions.

## Impact

- Affected specs: `uid-assignment` (new capability)
- Affected code: `scripts/builder.py` (`assign_by_dir`, `assign`), `tests/test_builder.py`,
  `docs/cli.md`
