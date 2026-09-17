## 1. Fix add-single record creation

- [x] 1.1 Emit `langs` as `{id, name}` dicts resolved via `data/reference/langs.csv`; reject unknown codes with a clear error
- [x] 1.2 Fix the `COUNTRIES_LANGS` auto-language condition to key on the resolved country code (covers both explicit `--country` and TLD-inferred locations)
- [x] 1.3 Add `--subregion` (validated against `data/reference/subregions/iso3166-2.csv`, sets `owner.location.subregion` + `coverage[].location.subregion`, level 30, and targets the `{CC}/{SUB}/` directory)
- [x] 1.4 Add `--owner-type` (validated against `data/reference/owner_types.yaml` canonical values and synonyms)
- [x] 1.5 Add `--is-national` flag writing `properties.is_national` (default omitted)
- [x] 1.6 Add `--id` override for path-based tenants; validate lowercase-alphanumeric and filename match
- [x] 1.7 Add `--no-detect` to skip the per-record `detect_single` network probe
- [x] 1.8 Self-validate the assembled record against `data/schemes/catalog.json` before writing; on failure print errors and do not write the file

## 2. Add batch manifest ingestion

- [x] 2.1 Implement `builder.py add-batch manifest.jsonl` with per-record fields (url, name, software, catalog_type, country, subregion, owner_name, owner_type, owner_link, langs, description, is_national, id)
- [x] 2.2 Load `full.jsonl` and `software.jsonl` once per batch; dedupe candidates in memory by canonical URL (reuse `url_utils.canonicalize_url`), host, and id; report skipped duplicates with existing ids
- [x] 2.3 Validate every manifest row against the catalog schema before writing any file; report per-row errors and write only valid rows
- [x] 2.4 Add `--detect/--no-detect` (default `--no-detect`) running one detect pass for written records when enabled
- [x] 2.5 Assign UIDs to all written records at the end of the batch (reuse `assign_by_dir` on affected directories)
- [x] 2.6 Print a batch summary: written, skipped duplicates, invalid rows with reasons

## 3. Tests and docs

- [x] 3.1 Tests: langs dict emission, auto-lang from country, subregion/owner-type validation errors, --id override, write-time validation refusal, add-batch dedupe/summary/UID assignment
- [x] 3.2 Update `docs/cli.md` and `docs/agents/contribute.md` with add-batch and the new add-single options
- [x] 3.3 Update `docs/agents/discover.md` "After a valid find" loop to use add-batch
- [x] 3.4 Run `python scripts/builder.py validate-yaml` and `pytest`
