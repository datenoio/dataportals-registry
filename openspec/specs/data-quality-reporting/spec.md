# data-quality-reporting Specification

## Purpose
Quality reports separate integrity issues from enrichment debt so CI can fail on coherence regressions without blocking endpoint backlog.
## Requirements
### Requirement: Integrity Versus Enrichment Priority Tracks
The quality pipeline MUST distinguish integrity issues from enrichment-debt issues when assigning priority.

#### Scenario: API-capable software without endpoints and api not true
- **WHEN** a record has API-capable `software.id`, empty `endpoints`, and `api` is not `true`
- **AND** the catalog `link` is not already a recognized service root
- **THEN** the issue is classified as enrichment debt at MEDIUM priority
- **AND** the issue type remains `SOFTWARE_EXPECTED_ENDPOINTS_MISSING_*`

#### Scenario: Explicit api true without endpoints
- **WHEN** a record has `api: true` and empty `endpoints`
- **THEN** `MISSING_ENDPOINTS` is flagged at IMPORTANT priority as an integrity/coherence issue

#### Scenario: Service-root link exemption retained
- **WHEN** `software.id` is GeoServer or ArcGIS Server and `link` already points at a service root
- **THEN** no software-expected-endpoints issue is emitted

### Requirement: National Catalog Flag Is Type-Official Not Owner-Federal
`analyze-quality` MUST flag `properties.is_national: true` when the catalog is not the country's official catalog of that type.

#### Scenario: Agency scientific repository flagged national
- **WHEN** a record has `properties.is_national: true`
- **AND** `catalog_type` is Scientific data repository
- **THEN** `IS_NATIONAL_AGENCY_OR_TOPIC` is emitted at MEDIUM priority as enrichment debt

#### Scenario: Official national open-data portal
- **WHEN** a record is the country's official open-data portal (for example `https://catalog.data.gov`)
- **AND** `properties.is_national` is `true`
- **THEN** no `IS_NATIONAL_AGENCY_OR_TOPIC` issue is emitted

### Requirement: Complete Quality Report Aggregation
The `analyze-quality` command MUST include issues from every registered check in all primary report outputs.

#### Scenario: Multiple rule families produce issues
- **WHEN** `python scripts/builder.py analyze-quality` completes
- **THEN** `dataquality/full_report.txt` lists issues grouped by every issue type that has at least one finding
- **AND** `dataquality/full_report.jsonl` contains one JSON object per issue across all rule families

#### Scenario: Single rule family has zero issues
- **WHEN** a registered check finds no issues
- **THEN** that rule type is omitted from the issues-by-type section
- **AND** no stale rule file with non-zero count remains in `dataquality/rules/`

### Requirement: Report Output Consistency
Quality report outputs MUST remain internally consistent after each analysis run.

#### Scenario: Post-run consistency validation
- **WHEN** quality analysis completes successfully
- **THEN** the total issue count in `full_report.jsonl` equals the sum of per-rule issue counts written to `dataquality/rules/*.txt`
- **AND** `primary_priority.jsonl` contains a deduplicated subset of issues at CRITICAL and IMPORTANT priority

### Requirement: No Deprecated Stub Checks in Pipeline
The quality pipeline MUST NOT execute checks that always return `None`.

#### Scenario: Deprecated stubs removed
- **WHEN** the checks list in `analyze_quality` is inspected
- **THEN** `check_path_country_consistency`, `check_id_host_correlation`, and `check_owner_coverage_coherence` are not registered
- **AND** the documented active check count matches the registered list

