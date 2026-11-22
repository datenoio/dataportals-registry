# Change: Replace the fix_*.py scripts with one rule-based fix command

## Why

There are 13 `fix_*.py` scripts (4,200 lines), and none of them is covered by tests. They overlap:

- `fix_all_priority_issues.py` re-implements handlers for 14 issue types that `fix_important_issues.py`, `fix_medium_issues.py` and `fix_low_issues.py` also handle, for example `MISSING_OWNER_LINK`, `MISSING_TAGS`, `MISSING_TOPICS` and `SOFTWARE_ID_UNKNOWN`. Each type therefore has two implementations that can disagree.
- Each script carries its own `fix_yaml_file`, in seven different versions.
- Eleven scripts have no CLI at all. Two use argparse, and only some have a dry-run.

The docs send contributors to these scripts: `AGENTS.md` (14 references), `docs/enrichment.md`, `docs/cli.md`, `docs/metadata-quality.md`, `docs/data-model.md` and `docs/agents/improve.md`.

## What Changes

- Add `python scripts/builder.py apply-fixes` with these options:
  - `--rule ISSUE_TYPE` (repeatable), `--priority`, `--country`, `--id`;
  - `--dry-run`, which prints a per-file diff and writes nothing;
  - `--list-rules`, which prints each rule's issue type, priority and description.

  The command reads `dataquality/primary_priority.jsonl` from `analyze-quality`, or `--issues FILE`. It applies one registered rule per issue type and runs schema validation on every file it changes.
- Add rule modules under `scripts/dpr/fixes/`, one per area: owner, tags, topics, languages, endpoints, coverage, rights, software, `is_national`. Each rule declares its issue type, its priority and a pure `fix(record, issue) -> bool`. A single writer in `dpr.yaml_io` keeps key order.
- Port each issue type once. Where two scripts disagree, write characterization tests for both, pick one behaviour, and record the choice in `design.md`.
- Every rule gets a test with a minimal record before and after.
- **BREAKING (deprecation)** The 12 legacy entry points stop doing their own work:
  - `fix_critical_issues.py`, `fix_important_issues.py`, `fix_medium_issues.py`, `fix_low_issues.py`, `fix_all_priority_issues.py`;
  - `fix_api_status_mismatch.py`, `fix_catalog_software_mismatch.py`, `fix_duplicate_tags.py`, `fix_tag_hygiene.py`, `fix_software_id.py`, `fix_is_national_flags.py`, `fix_es_unk_subregions.py`.

  Each becomes a wrapper that logs a deprecation warning and calls `apply-fixes` with the matching rules, for one minor release. After that release they are deleted.
- `builder.py fix`, which runs `cursor-agent` (an LLM agent), keeps its name and behaviour. `apply-fixes` is the deterministic counterpart.
- Update `AGENTS.md` and the five docs above to use `apply-fixes`.

## Impact

- Affected specs: new `quality-fix-rules`.
- Affected code:
  - `scripts/builder.py` (new command);
  - new `scripts/dpr/fixes/`;
  - the 12 `fix_*.py` scripts (wrappers, then deleted);
  - new `tests/test_fix_rules.py`.
- Depends on `refactor-shared-script-library` for the `dpr` package and the shared YAML writer.
