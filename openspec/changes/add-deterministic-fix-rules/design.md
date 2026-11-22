## Context

Measured on 22 November 2026, active scripts only:

| Script | Lines | CLI | Coverage | Input |
|---|---|---|---|---|
| `fix_all_priority_issues.py` | 725 | none | 0% | `primary_priority.jsonl`, 19 issue types |
| `fix_important_issues.py` | 759 | none | 0% | 9 issue types |
| `fix_medium_issues.py` | 443 | argparse | 0% | 9 issue types |
| `fix_low_issues.py` | 344 | none | 0% | `priorities/LOW` |
| `fix_critical_issues.py` | 191 | none | 0% | `priorities/CRITICAL` |
| `fix_es_unk_subregions.py` | 504 | none | 0% | Spain-specific subregion fixes |
| `fix_tag_hygiene.py` | 239 | none | 0% | report file |
| `fix_duplicate_tags.py` | 172 | none | 0% | report file |
| `fix_api_status_mismatch.py` | 168 | none | 0% | report file |
| `fix_software_id.py` | 154 | none | 0% | software YAML |
| `fix_is_national_flags.py` | 147 | argparse (`--dry-run`) | 0% | `national_catalog.py` rule |
| `fix_catalog_software_mismatch.py` | 117 | none | 0% | `MAP_SOFTWARE_ALLOWED_CATALOG_TYPES` |
| `fix_all_issues.py` | 265 | none | 0% | copy of `builder.py fix`; deleted by `refactor-shared-script-library` |

These issue types have two implementations, one in `fix_all_priority_issues.py` and one in the per-priority script named after the arrow:

- `fix_important_issues.py`: `COVERAGE_NORMALIZATION`, `INCONSISTENT_LICENSE`, `MISSING_API_STATUS`, `MISSING_OWNER_NAME`, `MISSING_OWNER_TYPE`, `SOFTWARE_ID_UNKNOWN`
- `fix_medium_issues.py`: `MISSING_DESCRIPTION`, `MISSING_ENDPOINTS`, `MISSING_LANGS`, `SHORT_DESCRIPTION`, `TAG_HYGIENE`
- `fix_low_issues.py`: `MISSING_OWNER_LINK`, `MISSING_TAGS`, `MISSING_TOPICS`

## Goals / Non-Goals

- Goals:
  - One tested implementation per issue type.
  - One command with selection and dry-run.
  - The same YAML output format for every rule.
- Non-Goals:
  - Rules that need network access or an LLM: description writing and endpoint probing stay in `enrich_ai.py` and `apidetect.py`. A rule may only call them behind an explicit option.
  - Changing `analyze-quality` issue types or priorities.

## Decisions

- **Decision:** The command is `apply-fixes`, not `fix --rule`.
  - Why: `builder.py fix` already exists and runs `cursor-agent`. Reusing the name would change what an existing command does.
- **Decision:** A rule is a pure function from a record to a changed record. The command owns I/O, selection, dry-run diffs and validation.
  - Why: pure rules can be tested with a dict in and a dict out, with no files and no network.
- **Decision:** A rule that cannot fix a record safely returns `False` and leaves it unchanged. It never guesses.
  - Example: `MISSING_OWNER_TYPE` is left alone when no owner-type rule matches.
- **Decision:** `fix_es_unk_subregions.py` becomes a data-driven rule. Its Spanish city-to-subregion table moves to `data/reference/` (with `refactor-constants-into-reference-data`). The script is not kept as country-specific code.
- **Decision:** Legacy scripts become wrappers for one minor release, then they are deleted.
  - Why: the docs and contributors' shell history call them. One release of warnings is enough notice for an internal tool.

## Risks / Trade-offs

- **The two implementations of a shared issue type can give different results.** Choosing one changes the output for users of the other script.
  - Mitigation: characterization tests on both. The PR that ports a rule lists every difference and which behaviour won.
- **Large one-time diff.**
  - Mitigation: port rules one area at a time (owner, tags, topics, …), one PR each. The wrapper for a script switches only when all of its rules are ported.

## Migration Plan

1. Add `apply-fixes`, the rule registry and the shared writer, with no rules yet and with tests.
2. Port rules area by area, each with tests. Run `apply-fixes --dry-run` on the full registry and compare it with the legacy script on the same report.
3. Turn the legacy scripts into wrappers. Update the docs.
4. Next minor release: delete the wrappers.

Rollback: until step 4, the legacy code is in git history and any wrapper can be reverted on its own.

## Open Questions

- Should `apply-fixes` run `analyze-quality` first when `primary_priority.jsonl` is older than the newest YAML change, or only warn?
