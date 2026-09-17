# Change: Fix add-single record creation and add batch manifest ingestion

## Why

Analysis of the 200 most recent agent sessions shows the add path is the hottest workflow in the
repository (`assign` ran 215 times, `add-single` 150 times) and the most manual. `add-single`
writes records that fail the project's own schema (`langs` emitted as bare strings while
`data/schemes/catalog.json` requires `{id, name}` dicts), never auto-fills language because the
`COUNTRIES_LANGS` condition at `scripts/builder.py:981` is dead code, and offers no
`--subregion` / `--owner-type` / `--is-national` / `--id` options — so agents promote into
`Federal/` and then hand-edit YAML (134 subregion-friction and 164 owner-type-friction mentions
in 150 sessions). Each `add-single` call reloads the 70 MB `full.jsonl` export and runs a
per-record network probe, and there is no batch manifest input, so agents write throwaway
YAML-writer heredocs (54 in 150 sessions) or subprocess loops around `add-single`.

## What Changes

- Fix `langs` emission in `_add_single_entry`: map language codes through
  `data/reference/langs.csv` and write `{id, name}` dicts that satisfy the schema.
- Fix the dead `COUNTRIES_LANGS` auto-language condition: key the lookup on the resolved country
  code so language is actually auto-filled.
- Add `--subregion`, `--owner-type`, `--is-national`, `--id`, and `--no-detect` options to
  `add-single`; validate subregion against `data/reference/subregions/iso3166-2.csv` and owner
  type against `data/reference/owner_types.yaml`.
- Self-validate every record against `data/schemes/catalog.json` before writing; refuse to save
  invalid records.
- Add `builder.py add-batch manifest.jsonl`: one JSONL row per record with per-record fields
  (`url`, `name`, `software`, `catalog_type`, `country`, `subregion`, `owner_name`,
  `owner_type`, `owner_link`, `langs`, `description`, `is_national`, optional `id`), a single
  export load, in-memory dedupe by canonical URL and id, one optional detect pass, and UID
  assignment at the end of the batch.
- Keep `add-list` working (URL list with shared metadata); document `add-batch` as the preferred
  path for multi-record hunts.

## Impact

- Affected specs: `catalog-ingestion` (new capability)
- Affected code: `scripts/builder.py` (`_add_single_entry`, `add_single`, `add_list`, new
  `add_batch`), `scripts/constants.py` (reference loaders), `tests/test_builder.py`,
  `docs/cli.md`, `docs/agents/contribute.md`, `docs/agents/discover.md`
