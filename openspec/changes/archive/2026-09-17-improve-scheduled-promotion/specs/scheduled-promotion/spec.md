## ADDED Requirements

### Requirement: Selective Promotion by ID

The promotion script SHALL accept `--id ID [ID...]` to restrict processing to the named scheduled
records.

#### Scenario: Only requested records promoted

- **WHEN** `promote_scheduled.py --id cataloga catalogb` runs with three records in
  `data/scheduled/`
- **THEN** only `cataloga` and `catalogb` are moved to entities
- **AND** the third record remains in scheduled untouched

#### Scenario: Unknown id reported

- **WHEN** `--id` names a record absent from `data/scheduled/`
- **THEN** the command reports the unmatched id and continues with the matched ones

### Requirement: Subregion-Aware Placement

Promotion SHALL place records with a known `owner.location.subregion.id` under
`{CC}/{SUBREGION}/{type}/` and set `owner.location.level: 30`, instead of always using
`Federal/`.

#### Scenario: Regional record routed to subregion directory

- **WHEN** a promoted record has `owner.location.subregion.id: PT-11` and country `PT`
- **THEN** the file is moved to `data/entities/PT/PT-11/{type}/`
- **AND** `owner.location.level` is `30`

#### Scenario: Unknown subregion falls back to Federal

- **WHEN** a record's subregion code is absent from
  `data/reference/subregions/iso3166-2.csv`
- **THEN** the record is placed under `{CC}/Federal/{type}/`
- **AND** a warning names the unrecognized code

#### Scenario: National record stays in Federal

- **WHEN** a promoted record has no subregion
- **THEN** it is placed under `{CC}/Federal/{type}/` as before

### Requirement: Liveness-Gated Promotion

With `--probe`, promotion SHALL classify each candidate `link` using the shared liveness
vocabulary before moving it, and SHALL NOT promote records classified `dead`.

#### Scenario: Live record promoted

- **WHEN** a candidate's `link` returns HTTP 200 during `--probe`
- **THEN** the record is promoted with `status: active`

#### Scenario: Dead record held back

- **WHEN** a candidate is classified `dead` (connection refused, repeated timeout, or 404)
- **THEN** the record remains in `data/scheduled/` unchanged
- **AND** the summary lists it as held back

#### Scenario: Inconclusive record promoted with warning

- **WHEN** a candidate returns HTTP 403 (bot protection)
- **THEN** the record is promoted
- **AND** a warning notes the inconclusive probe

### Requirement: Data-Driven Country Hints

Country-inference heuristics for `Unknown` scheduled records SHALL be loaded from
`data/reference/country_hints.yaml` rather than hardcoded in the script.

#### Scenario: Hint file drives inference

- **WHEN** `data/reference/country_hints.yaml` contains `{pattern: brasilio, country: BR}`
- **THEN** a scheduled record whose link contains `brasilio` infers country `BR`
- **AND** editing the YAML changes inference without code changes

### Requirement: Scheduled Queue Review Report

The project SHALL provide a `review-scheduled` command that reports duplicate, liveness, and
country-inference status for the scheduled queue without modifying any files.

#### Scenario: Queue triage in one run

- **WHEN** `review-scheduled` runs against a scheduled queue containing live new records, dead
  records, and duplicates of existing entities
- **THEN** the report groups records into promote-ready, dead, duplicate, and needs-review
- **AND** no file is moved, edited, or deleted

#### Scenario: Machine-readable report

- **WHEN** `review-scheduled` completes
- **THEN** a JSONL report with per-record `id`, `link`, `liveness`, `duplicate_of`, and inferred
  country is written for follow-up tooling
