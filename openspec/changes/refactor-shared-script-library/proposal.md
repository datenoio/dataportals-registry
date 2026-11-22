# Change: Move shared script helpers into one library package

## Why

Scripts in `scripts/` copy helpers from each other instead of sharing them.

- 23 module-level function names are defined in two or more active scripts, about 870 lines in all. Keeping the longest copy of each would remove that many lines.
  - Some copies are byte-for-byte identical: `load_software_definitions`, `get_re3data_identifier` (3 copies), `normalize_url`, `normalize_domain`, `load_jsonl`, `load_jsonl_dict`, `load_csv_dict`, `calculate_file_hash`, `build_prompt`, `is_enrichment_issue_type`.
  - Others have drifted apart. `infer_country_from_link` is 184 lines in `fix_important_issues.py` and 58 lines in `promote_scheduled.py`. `parse_report_file` exists in 3 variants.
- Tests reach scripts through 21 `sys.path.insert` calls, and scripts add 7 more.
- Script style is mixed:
  - 12 scripts have no CLI framework, only a `__main__` block;
  - 5 use argparse;
  - 201 `print()` calls bypass logging.

A fix made in one copy does not reach the others.

## What Changes

- Add a package `scripts/dpr/` with these modules:
  - `yaml_io` (moved from `scripts/yaml_io.py`);
  - `jsonl` (JSONL/CSV readers, `load_dataset_jsonl`);
  - `urls` (moved from `url_utils.py`, plus `normalize_url` / `normalize_domain`);
  - `geo` (`infer_country_from_link`, `get_country_from_record`, `infer_subregion`);
  - `software` (`load_software_definitions`, software YAML iteration);
  - `re3data` (the five helpers shared by `re3data_enrichment.py` and `re3data_integration.py`);
  - `reports` (quality-report readers, `is_enrichment_issue_type`).
- Replace every duplicated definition with an import from `dpr`. Where copies differ, keep one implementation, add characterization tests first, and list each resolved difference in `design.md`.
- Set `pythonpath = scripts` in `pytest.ini` and delete the 21 `sys.path` hacks in tests. The 7 hacks in scripts go away too: a script run as `python scripts/x.py` already has `scripts/` on its path.
- Entry-point conventions for every script that a person runs:
  - typer for the CLI, keeping existing option names, so `.github/workflows/liveness.yml` and the docs keep working;
  - `logging` for progress and diagnostics;
  - `typer.echo` only for the result a command is run to produce.
- **BREAKING (internal)** The `yaml_io` and `url_utils` imports change to `dpr.yaml_io` and `dpr.urls`. No shim modules stay behind.
- Guard tests fail when:
  - a module-level function name is defined in two active scripts, unless it is on a short allowlist;
  - a script or test calls `sys.path.insert` / `sys.path.append`;
  - a CLI module calls `print()`.

## Impact

- Affected specs: new `script-library`.
- Affected code:
  - every active script in `scripts/` (imports only, for most);
  - `tests/` (path hacks);
  - `pytest.ini`;
  - `tests/test_yaml_safety.py` (new module path);
  - `AGENTS.md` and `docs/cli.md` (conventions).
- Command-line behaviour does not change. Option names and outputs stay the same, except that `print()` messages move to logging on stderr.
