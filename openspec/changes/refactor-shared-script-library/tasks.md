## 1. Package skeleton

- [x] 1.1 Create `scripts/dpr/__init__.py`. Move `scripts/yaml_io.py` to `scripts/dpr/yaml_io.py` and `scripts/url_utils.py` to `scripts/dpr/urls.py`, and update every import.
- [x] 1.2 Add `pythonpath = scripts` to `pytest.ini`, and delete the `sys.path.insert` calls in `tests/`.
- [x] 1.3 Delete the 7 `sys.path` hacks in scripts. Check that each affected script still runs as `python scripts/<name>.py --help` from the repository root.
- [x] 1.4 Point `tests/test_yaml_safety.py` and the `AGENTS.md` YAML rule at `dpr.yaml_io`.

## 2. Identical helpers

- [x] 2.1 Move the helpers that are identical in every copy into `dpr` and import them from there:
  - `dpr.jsonl`: `load_jsonl`, `load_csv_dict`;
  - `dpr.urls`: `normalize_url`, `normalize_domain`;
  - `dpr.software`: `load_software_definitions`;
  - `dpr.re3data`: `get_re3data_identifier`.

  Two copies had no callers and were deleted instead of moved: `load_jsonl_dict` (in `enrich.py` and `enrich_ai.py`) and the `builder.py` copy of `is_enrichment_issue_type`. `quality_regression.py` keeps the used copy, so `dpr.reports` is not needed yet.
- [x] 2.2 Delete `scripts/fix_all_issues.py`, an older copy of `builder.py fix`, and point `AGENTS.md` and `devdocs/quality-fix-workflow.md` at `builder.py fix`.

## 3. Diverged helpers

- [x] 3.1 Add characterization tests for both callers of `infer_country_from_link`, then keep one implementation in `dpr.geo` (`tests/test_dpr_geo.py`). The `promote_scheduled.py` version is kept unchanged. `fix_important_issues.py` now uses it and takes country names from `constants.COUNTRIES`; see the design note.
- [x] 3.2 Do the same for `read_jsonl_issues` in `dpr.reports`. `parse_report_file` exists only in `fix_*.py` scripts, so it goes with `add-deterministic-fix-rules`.
- [x] 3.3 Do the same for `fetch_re3data_page`, `get_re3data_url`, `collect_re3data_identifiers` and `RE3DATA_BASE_URL` in `dpr.re3data`.
- [ ] 3.4 Move the shared hunt/promote functions into `dpr` so that `promote_scheduled.py` no longer imports `hunt`. Deferred to its own PR; see the design note.
- [x] 3.5 Unify `_iter_yaml_files` (`apidetect.py`, `builder.py`) as `dpr.yaml_io.iter_yaml_files`. It keeps the sorted `builder.py` behaviour, so `apidetect.py` now walks files in sorted order.

## 4. Entry-point conventions

- [ ] 4.1 Convert to typer, keeping option names: `check_liveness.py`, `refresh_subregion_reference.py`, `update_quality_baseline.py`, and the `__main__`-only scripts that `add-deterministic-fix-rules` does not remove.
- [ ] 4.2 Replace `print()` with `logging`, or with `typer.echo` for primary command output.
- [ ] 4.3 Document the conventions in `AGENTS.md` (Code Style) and `docs/cli.md`.

## 5. Guards and verification

- [x] 5.1 Add guard tests for duplicate module-level function names (`tests/test_script_library.py`, with an allowlist that fails on stale entries) and for `sys.path` manipulation.
- [ ] 5.1a Add the guard test for `print()` in CLI modules, after task 4.2.
- [ ] 5.2 Run `pytest`, `ruff check scripts tests`, `python scripts/builder.py validate-yaml` and the liveness workflow command with `--sample 5`.
- [ ] 5.3 Run `openspec validate refactor-shared-script-library --strict`.
