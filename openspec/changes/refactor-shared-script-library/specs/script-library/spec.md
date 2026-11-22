## ADDED Requirements

### Requirement: Single Definition of Shared Helpers

Helpers that more than one script uses SHALL be defined once, in the `scripts/dpr/` package, and imported from there. Two active scripts in `scripts/` (outside `scripts/archive/`), or an active script and a `dpr` module, SHALL NOT define a module-level function with the same name, unless the name is on the allowlist in the guard test. Each allowlist entry SHALL carry a comment that says why.

#### Scenario: Duplicate helper rejected

- **WHEN** a pull request adds `def normalize_url(...)` to a script while `dpr.urls.normalize_url` exists
- **THEN** the duplicate-name guard test fails and names both definitions

#### Scenario: Allowlisted duplicate accepted

- **WHEN** `_probe_one` is defined in both `apidetect.py` and `hunt.py`, and the allowlist lists it with a reason
- **THEN** the guard test passes

### Requirement: No Import Path Manipulation

Active scripts (outside `scripts/archive/`), the `dpr` package and tests SHALL NOT call `sys.path.insert` or `sys.path.append`. Tests SHALL import scripts through the `pythonpath = scripts` setting in `pytest.ini`.

#### Scenario: Test imports a script module

- **WHEN** `pytest` runs `tests/test_builder.py`, which does `import builder`
- **THEN** the import succeeds without any `sys.path` change in the test file

#### Scenario: Path hack rejected

- **WHEN** a script or test contains `sys.path.insert(`
- **THEN** the guard test fails and names the file and line

### Requirement: Entry-Point Conventions

Every script that a person runs from the command line SHALL:

- define its CLI with typer;
- report progress and diagnostics through `logging`;
- not call `print()`.

Primary command output SHALL use `typer.echo`. Converting a script to these conventions SHALL keep its existing option names.

#### Scenario: Liveness workflow keeps working

- **WHEN** `.github/workflows/liveness.yml` runs `python scripts/check_liveness.py --workers 64 --delay 0.25 --sample 5`
- **THEN** the command accepts the same options as before the conversion and writes `dataquality/liveness_report.jsonl`

#### Scenario: print() rejected in a CLI module

- **WHEN** a pull request adds `print(` to a script that defines a typer app
- **THEN** the guard test fails and names the file and line
