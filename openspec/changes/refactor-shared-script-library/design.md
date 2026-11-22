## Context

Measured on 22 November 2026, branch `claude/tech-debt-phase2-proposals`, active scripts only (not `scripts/archive/`):

| Function | Copies | Distinct bodies | Lines | Files |
|---|---|---|---|---|
| `fix_yaml_file` | 7 | 7 | 381 | each `fix_*.py`; handled by `add-deterministic-fix-rules` |
| `infer_country_from_link` | 2 | 2 | 242 | `fix_important_issues.py`, `promote_scheduled.py` |
| `_probe_one` | 2 | 2 | 199 | `apidetect.py`, `hunt.py` |
| `process_record`, `call_cursor_agent`, `build_prompt`, `calculate_file_hash` | 2 each | 1–2 | 340 | `builder.py`, `fix_all_issues.py` |
| `parse_report_file` | 3 | 3 | 156 | `fix_api_status_mismatch.py`, `fix_duplicate_tags.py`, `fix_tag_hygiene.py` |
| `get_re3data_identifier`, `get_re3data_url`, `fetch_re3data_page`, `collect_re3data_identifiers` | 2–3 | 1–2 | 111 | `re3data_enrichment.py`, `re3data_integration.py`, `calculate_trust_scores.py` |
| `normalize_url`, `normalize_domain` | 2 each | 1 | 34 | `remove_scheduled_duplicates.py`, `sync_ckan_ecosystem.py` |
| `load_jsonl`, `load_jsonl_dict`, `load_csv_dict`, `read_jsonl_issues` | 2 each | 1–2 | 93 | `builder.py`, `stats.py`, `enrich.py`, `enrich_ai.py`, `fix_all_priority_issues.py` |
| `load_software_definitions` | 2 | 1 | 40 | `fix_important_issues.py`, `fix_software_id.py` |
| `is_enrichment_issue_type` | 2 | 1 | 14 | `builder.py`, `quality_regression.py` |

`hunt.py` and `promote_scheduled.py` depend on each other:

- `hunt.py` imports `promote_records` inside its ingest step (`scripts/hunt.py:1169`);
- `promote_scheduled.py` imports `_build_export_indexes`, `dedupe_rows` and `probe_rows` from `hunt` inside a function (`scripts/promote_scheduled.py:512`).

Both imports are lazy, so the cycle works at runtime.

## Goals / Non-Goals

- Goals:
  - One definition per shared helper.
  - No `sys.path` manipulation.
  - One CLI and logging convention.
  - No change to command options or outputs.
- Non-Goals:
  - Splitting `builder.py` into modules (phase 3).
  - Replacing the `fix_*.py` scripts (`add-deterministic-fix-rules`).
  - Moving data out of `constants.py` (`refactor-constants-into-reference-data`).
  - Publishing the package to PyPI.

## Decisions

- **Decision:** The package lives at `scripts/dpr/` and is imported with `scripts/` on the path. It is not installed with `pip install -e .`.
  - Why: every script already runs with `scripts/` on `sys.path[0]`. pytest gets the same through the `pythonpath` ini option (pytest ≥ 7, already required). Contributors keep a single `pip install -r requirements-dev.txt`, and no build backend is needed.
  - Alternative: `src/dpr` with `[project]` metadata and `pip install -e .`. This is useful only if other repositories import the code, and the API/MCP repos consume exports, not code. It can be added later without moving files again.
- **Decision:** `dpr` is the name: short, and not used by the standard library or by installed dependencies. `registry` was rejected as too generic, since PyPI distributions with that name exist.
- **Decision:** Where copies differ, the version used by the most-run command wins, after characterization tests pin its behaviour. For `infer_country_from_link` that is the `promote_scheduled.py` version. It runs through `infer_country_for_unknown` in `promote_records`, which `hunt.py ingest` calls. The tests run 14 of its 19 statements. The 184-line variant in `fix_important_issues.py` has 0% test coverage. Each difference is listed in the PR that resolves it.
- **Decision:** `_probe_one` in `apidetect.py` and `hunt.py` stays duplicated for now. The two copies return different shapes (endpoint dict versus probe verdict), so merging them needs its own design. The duplicate-name guard allowlists it with a comment.
- **Decision:** `fix_all_issues.py` is deleted. It is an older copy of the `builder.py fix` command, which runs `cursor-agent` on `primary_priority.jsonl`. The `builder.py` copy has since changed: it passes the prompt as an argument rather than on stdin, and reports errors better. The `AGENTS.md` fix-script table and `devdocs/quality-fix-workflow.md` pointed at the script; they now point at `builder.py fix`.

## Risks / Trade-offs

- **Diverged copies hide behaviour differences.** Choosing one version can change results for the script that used the other.
  - Mitigation: characterization tests on both callers before the switch, and a per-function note in the PR.
- **Import churn conflicts with open branches.**
  - Mitigation: land the change in small PRs, one module at a time. Start with the identical copies, which are pure moves.
- **Moving output from `print()` (stdout) to logging (stderr)** can break shell pipelines that parse that output.
  - Mitigation: `docs_software_coverage.py` and `update_quality_baseline.py` print results; keep those on stdout through `typer.echo`.

## Migration Plan

1. Create `scripts/dpr/` and move `yaml_io.py` and `url_utils.py` into it. Update the imports and `pytest.ini`, and remove the test path hacks.
2. Move the identical helpers (pure moves).
3. Characterize, then unify, the diverged helpers, one per PR.
4. Convert the argparse and `__main__`-only entry points that stay after `add-deterministic-fix-rules` to typer, and move `print()` calls to logging.
5. Turn on the guard tests.

Rollback: each step is a separate PR and can be reverted on its own.
