# catalog-liveness Specification

## Purpose
Scheduled HTTP probes of catalog `link` URLs, written to `dataquality/liveness_report.jsonl`.
## Requirements
### Requirement: Scheduled URL Liveness Probing
The project MUST provide a script to probe catalog URL reachability.

#### Scenario: Live portal responds successfully
- **WHEN** `check_liveness.py` probes a catalog `link` that returns HTTP 200
- **THEN** the record is classified as `live`
- **AND** the result is written to the liveness report with `checked_at` timestamp

#### Scenario: Dead portal is unreachable
- **WHEN** a probe receives connection refused or repeated timeouts after retries
- **THEN** the record is classified as `dead`
- **AND** the report includes the last HTTP status or error message

#### Scenario: Bot protection returns 403
- **WHEN** a probe receives HTTP 403 without other success signals
- **THEN** the record is classified as `inconclusive`
- **AND** it is not counted as `dead` in summary statistics

### Requirement: Weekly Automated Liveness Workflow
A GitHub Actions workflow MUST run liveness checks on a scheduled cadence.

#### Scenario: Weekly scheduled run
- **WHEN** the weekly cron trigger fires
- **THEN** the workflow executes `check_liveness.py` against the full catalog
- **AND** publishes `liveness_report.jsonl` as a workflow artifact

#### Scenario: Manual dispatch
- **WHEN** a maintainer triggers the workflow via `workflow_dispatch`
- **THEN** the same probe logic runs with optional sample/country filters

### Requirement: Machine-Readable Liveness Report
Liveness results MUST be consumable by agents and fix scripts.

### Requirement: Apply confirmed-dead catalogs
The liveness script MUST be able to mark catalogs inactive from a report without treating inconclusive probes as dead.

#### Scenario: Apply dead rows only
- **WHEN** `check_liveness.py --apply-dead --write` is run against a report
- **THEN** only rows with `liveness_status: dead` and a `cdi` UID are updated
- **AND** those YAML files set `status: inactive`
- **AND** rows classified `inconclusive` or `error` are left unchanged

