## ADDED Requirements

### Requirement: Rule-Based Fix Command

The registry SHALL provide `python scripts/builder.py apply-fixes`. The command reads quality issues from `dataquality/primary_priority.jsonl`, or from the file given with `--issues`, and applies the registered fix rule for each selected issue type. The selection options SHALL be:

- `--rule` (repeatable);
- `--priority`;
- `--country`;
- `--id`.

#### Scenario: Fix one issue type

- **WHEN** a contributor runs `python scripts/builder.py apply-fixes --rule MISSING_TAGS`
- **THEN** only records with a `MISSING_TAGS` issue are changed
- **AND** the command reports how many records it changed, skipped and failed

#### Scenario: List rules

- **WHEN** a contributor runs `python scripts/builder.py apply-fixes --list-rules`
- **THEN** the command prints each rule's issue type, priority and description, and changes no file

### Requirement: Dry Run Writes Nothing

With `--dry-run`, `apply-fixes` SHALL print the change it would make to each file and SHALL NOT write any file.

#### Scenario: Dry run on the full registry

- **WHEN** a contributor runs `python scripts/builder.py apply-fixes --dry-run`
- **THEN** the output shows a diff for each file that would change
- **AND** `git status` shows no modified YAML afterwards

### Requirement: Validated Writes

`apply-fixes` SHALL validate every changed record against `data/schemes/catalog.json` before it writes the file. When validation fails, the command SHALL leave the file unchanged and report the error.

#### Scenario: Rule output fails the schema

- **WHEN** a rule produces a record that fails schema validation
- **THEN** the original YAML file is left unchanged
- **AND** the command reports the file, the rule and the validation error, and exits with code 1 at the end

### Requirement: One Tested Rule per Issue Type

Each issue type SHALL have at most one registered fix rule. Each rule SHALL have at least one unit test that checks a record before and after the fix. A rule that cannot fix a record safely SHALL leave it unchanged.

#### Scenario: Duplicate registration rejected

- **WHEN** two rules register the same issue type
- **THEN** importing the rule registry raises an error that names both rules

#### Scenario: Unfixable record left alone

- **WHEN** the `MISSING_OWNER_TYPE` rule finds no owner-type mapping that matches a record
- **THEN** the record is not changed and the command counts it as skipped

### Requirement: Legacy Fix Scripts Deprecated

For one minor release after `apply-fixes` ships, each legacy `fix_*.py` script SHALL log a deprecation warning and run `apply-fixes` with its rules. The scripts SHALL be removed in the following minor release.

#### Scenario: Legacy script still works during deprecation

- **WHEN** a contributor runs `python scripts/fix_low_issues.py`
- **THEN** a warning names the replacement command
- **AND** the same issue types are fixed through `apply-fixes`
