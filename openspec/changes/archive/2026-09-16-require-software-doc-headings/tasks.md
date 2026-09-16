## 1. OpenSpec

- [x] 1.1 Scaffold proposal, tasks, and documentation-site delta
- [x] 1.2 Run `openspec validate require-software-doc-headings --strict`

## 2. Discovery headings

- [x] 2.1 Convert leftover-table IDs in `docs/discovery-indicators.md`
- [x] 2.2 Convert leftover-table IDs in `docs/discovery-scientific.md`
- [x] 2.3 Convert leftover-table IDs in `docs/discovery-opendata.md`
- [x] 2.4 Convert leftover-table IDs in geoportal viewer/SDI guides
- [x] 2.5 Add `openmlorg` H2 in `docs/discovery-other.md`
- [x] 2.6 Mark converted leftover-table rows as `see above`

## 3. Harvest headings

- [x] 3.1 Add harvest H2s for `bicontour`, `datainsight`, `datavavt` in `docs/harvest-indicators.md`

## 4. CI guard

- [x] 4.1 Add `missing_headings()` in `scripts/docs_software_coverage.py`
- [x] 4.2 Assert no empty discovery/harvest headings in `tests/test_docs_software_coverage.py`
- [x] 4.3 Regenerate `docs/software-index.md`
- [x] 4.4 Update heading-required wording in `software-taxonomy.md` and `agents/improve.md`

## 5. Extras

- [x] 5.1 Clarify `MISSING_CONTACT_INFO` as `owner.link` in quality-rules and data-model
- [x] 5.2 Fill known `documentation_url` values on software YAML (do not invent)

## 6. Verification

- [x] 6.1 `openspec validate require-software-doc-headings --strict`
- [x] 6.2 `python scripts/docs_software_coverage.py`
- [x] 6.3 `pytest tests/test_docs_software_coverage.py -q`
