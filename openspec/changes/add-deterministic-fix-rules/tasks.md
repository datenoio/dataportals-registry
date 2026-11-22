## 1. Framework

- [ ] 1.1 Add the `Rule` type and registry in `scripts/dpr/fixes/__init__.py`, and the shared writer in `dpr.yaml_io`, which keeps key order and `allow_unicode`.
- [ ] 1.2 Add `builder.py apply-fixes` with `--rule`, `--priority`, `--country`, `--id`, `--issues`, `--dry-run` and `--list-rules`. Every changed file is validated against `data/schemes/catalog.json`.
- [ ] 1.3 Add tests for selection, dry-run (no file written) and validation failure (the file is restored and the error is reported).

## 2. Rules, one PR per area

- [ ] 2.1 Owner: `MISSING_OWNER_LINK`, `MISSING_OWNER_NAME`, `MISSING_OWNER_TYPE`.
- [ ] 2.2 Tags and topics: `MISSING_TAGS`, `TAG_HYGIENE`, `DUPLICATE_TAGS`, `MISSING_TOPICS`.
- [ ] 2.3 Languages and descriptions: `MISSING_LANGS`, plus the deterministic parts of `MISSING_DESCRIPTION` and `SHORT_DESCRIPTION`.
- [ ] 2.4 Software and API: `SOFTWARE_ID_UNKNOWN`, catalog-software mismatch, `MISSING_API_STATUS`, API status mismatch, `MISSING_ENDPOINTS`. Endpoint probing runs only behind an explicit option.
- [ ] 2.5 Coverage, rights and national flags: `COVERAGE_NORMALIZATION`, `INCONSISTENT_LICENSE`, `IS_NATIONAL_AGENCY_OR_TOPIC`, and the Spanish subregion table.
- [ ] 2.6 For each issue type that two scripts implement: characterization tests for both versions, and a note in the PR on which behaviour was kept.

## 3. Deprecation

- [ ] 3.1 Turn each legacy `fix_*.py` into a wrapper that logs a deprecation warning and calls `apply-fixes` with its rules.
- [ ] 3.2 Update `AGENTS.md`, `docs/enrichment.md`, `docs/cli.md`, `docs/metadata-quality.md`, `docs/data-model.md` and `docs/agents/improve.md`.
- [ ] 3.3 Add a CHANGELOG entry that lists the wrappers and the release in which they will be removed.

## 4. Verify

- [ ] 4.1 Run `apply-fixes --dry-run` on the full registry, and compare it with the legacy scripts on the same `primary_priority.jsonl`.
- [ ] 4.2 Run `pytest`, `ruff check scripts tests` and `python scripts/builder.py validate-yaml`.
- [ ] 4.3 Run `openspec validate add-deterministic-fix-rules --strict`.
