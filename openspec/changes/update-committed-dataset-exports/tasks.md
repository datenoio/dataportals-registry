## 1. Readers

- [ ] 1.1 Extend `load_dataset_jsonl` in `scripts/builder.py`. When `full.jsonl` is absent, it returns `catalogs.jsonl.zst` merged with `scheduled.jsonl.zst`.
- [ ] 1.2 Switch these readers to `load_dataset_jsonl("full.jsonl")`:
  - in `builder.py`: `validate`, `report`, `add-legacy`, `add-single`, `add-list` and `_add_batch_manifest`;
  - `stats.py` (3 call sites);
  - `enrich_ai.py` (2 call sites);
  - `sync_ckan_ecosystem.py`.
- [ ] 1.3 Add tests that run `add-single`'s duplicate check and `report` with only the tracked exports in a temporary `DATASETS_DIR`.

## 2. Tracked files

- [ ] 2.1 Run `git rm --cached` on `data/datasets/full.jsonl`, `data/datasets/full.jsonl.zst` and `data/datasets/datasets.duckdb`, and add the three paths to `.gitignore`.
- [ ] 2.2 Add a test that fails when `git ls-files data/datasets` lists any of the three files.
- [ ] 2.3 Check that `python scripts/builder.py build` still writes all export files, and that `git status` then shows only tracked exports as changed.

## 3. Docs

- [ ] 3.1 README quickstart and table: query `data/datasets/full.parquet`, and point to the release assets for DuckDB and `full.jsonl.zst`.
- [ ] 3.2 Update these docs to the same file set:
  - `docs/ai-consumers.md`, `docs/exports.md`, `docs/releasing.md`;
  - `docs/agents/query.md`, `docs/agents/discover.md`, `docs/agents/improve.md`, `docs/agents/contribute.md`;
  - `DATASHEET.md` and `llms.txt`.
- [ ] 3.3 CHANGELOG: add a **BREAKING** entry with the release-asset URLs.

## 4. Verify

- [ ] 4.1 Run `pytest`, `ruff check scripts tests` and `python scripts/builder.py validate-yaml`.
- [ ] 4.2 In a fresh clone without a build:
  - `hunt.py dedupe` and `builder.py assign --dry-run` use `full.parquet`;
  - `builder.py add-single URL --scheduled` detects an existing link.
- [ ] 4.3 Run `openspec validate update-committed-dataset-exports --strict`.
