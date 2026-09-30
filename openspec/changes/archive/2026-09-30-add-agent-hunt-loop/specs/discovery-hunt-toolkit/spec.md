## ADDED Requirements

### Requirement: Prior-hunt gate

The toolkit SHALL provide `hunt.py prior --target TARGET` that reads `dataquality/hunts.jsonl` and prints a single `decision` of `stop` or `continue`. Targets that share a software id SHALL be reported together. A software id is the prefix of `TARGET` before the first `.` or `-` when that prefix matches a file under `data/software/`. A slice is `TARGET` itself plus any logged target or `notes` token with the same software id and the same suffix.

#### Scenario: Recent complete slice stops

- **WHEN** `prior --target geoserver.es` runs and a row for that slice has `status: complete` with a `date` within the last 14 days
- **THEN** stdout contains `decision: stop`, the row date, `added`, and `notes`
- **AND** the command exits 0
- **AND** stdout ends with `next: none`

#### Scenario: Uncovered country slice continues

- **WHEN** `prior --target geoserver.fr` runs and the log has a complete `geoserver.es` row but no `fr` slice
- **THEN** stdout contains `decision: continue` and lists `es` as a covered slice
- **AND** stdout ends with a `next:` line that runs `hunt.py search` for the `fr` slice

#### Scenario: Software aliases collapse

- **WHEN** the log contains `arcgisserver.org` and `arcgisserver.edu` and both prefixes match the `arcgisserver` software id
- **THEN** `prior --target arcgisserver` lists both rows as slices of `arcgisserver`

#### Scenario: No history continues

- **WHEN** no row matches the target or its software id
- **THEN** stdout contains `decision: continue`
- **AND** stdout ends with a `next:` line that runs `hunt.py search` or `hunt.py budget`

### Requirement: FOFA budget command

The toolkit SHALL provide `hunt.py budget` that prints the FOFA `remain_api_data` value. When the value is 0, the command SHALL print `decision: stop-budget` and exit non-zero. When the value is greater than 0, the command SHALL print `decision: continue` and exit 0. The command SHALL NOT run a search query.

#### Scenario: Zero balance stops before search

- **WHEN** `budget` runs and the FOFA account reports `remain_api_data` of 0
- **THEN** stdout contains `decision: stop-budget`
- **AND** the command exits non-zero
- **AND** stdout ends with `next: none`

#### Scenario: Positive balance continues to search

- **WHEN** `budget` runs and `remain_api_data` is greater than 0
- **THEN** stdout contains `decision: continue` and the remaining value
- **AND** stdout ends with a `next:` line that runs `hunt.py search`

### Requirement: Search budget guard and inline dedupe

`hunt.py search` SHALL check the FOFA account balance before any FOFA query. When `remain_api_data` is 0, the command SHALL refuse the search. A `--query-file` with more than 25 queries SHALL be rejected unless `--allow-wide` is set. `search --dedupe` SHALL annotate candidates against dataset exports using the same DuckDB-then-parquet behavior as `hunt.py dedupe`. When `--out` is omitted, artifacts SHALL be written under `/tmp/hunts/<slug>/` and SHALL NOT be written into the repository tree.

#### Scenario: Empty FOFA balance stops the search

- **WHEN** `search fofa` runs and the FOFA account reports `remain_api_data` of 0
- **THEN** the command exits non-zero with `decision: stop-budget`
- **AND** no candidate file is written
- **AND** stdout ends with `next: none`

#### Scenario: Long query file rejected

- **WHEN** `--query-file` contains 26 or more queries and `--allow-wide` is absent
- **THEN** the command exits non-zero before any search API call
- **AND** the error names the query count and `--allow-wide`

#### Scenario: Inline dedupe marks known hosts

- **WHEN** `search --dedupe` returns a host already present in the exports
- **THEN** that row has `exists: true` and `existing_id` set to the matching record id
- **AND** hosts absent from the exports have `exists: false`

#### Scenario: Default output stays outside the repo

- **WHEN** `search` runs without `--out`
- **THEN** the candidate file is created under `/tmp/hunts/`
- **AND** no `candidates.jsonl` is created in the repository working tree

#### Scenario: Explicit output path is honored

- **WHEN** `search` runs with `--out candidates.jsonl`
- **THEN** the file is written at the given path

### Requirement: Probe catalog verdict

`hunt.py probe --software ID` SHALL set `verdict` on each row to one of `catalog`, `auth`, `empty`, `dead`, or `unknown`. The command SHALL request the root URL and at most one capability URL from the published apidetect map. GeoServer SHALL use a WMS GetCapabilities URL, ArcGIS Server SHALL use `/rest/services?f=json`, and CKAN SHALL use `package_search`. When that response exposes a collection size, the row SHALL include `collection_count`. The command SHALL NOT run a full per-endpoint apidetect sweep.

#### Scenario: Capability document with layers is a catalog

- **WHEN** `--software geoserver` probes a host whose WMS GetCapabilities document lists one or more layers
- **THEN** the row has `verdict: catalog` and `collection_count` greater than 0

#### Scenario: ArcGIS REST services are a catalog

- **WHEN** `--software arcgisserver` probes a host whose `/rest/services?f=json` body lists one or more services
- **THEN** the row has `verdict: catalog` and `collection_count` greater than 0

#### Scenario: Authentication wall is not bypassed

- **WHEN** the root or capability URL returns 401 or 403
- **THEN** the row has `verdict: auth`
- **AND** no further request is made to that host

#### Scenario: Live page without a catalog is empty

- **WHEN** a candidate returns HTTP 200, no published fingerprint matches, and the capability collection size is 0
- **THEN** the row has `verdict: empty`

#### Scenario: Unreachable host is dead

- **WHEN** the candidate connection fails, times out, or returns HTTP 5xx
- **THEN** the row has `verdict: dead`

#### Scenario: Unparsed software stays unknown

- **WHEN** `--software` is an id other than `geoserver`, `arcgisserver`, or `ckan` and no fingerprint matches
- **THEN** the row has `verdict: unknown`
- **AND** `collection_count` is absent

### Requirement: Ingest verified candidates

The toolkit SHALL provide `hunt.py ingest PROBED.jsonl` that writes only rows with `verdict: catalog` and `exists` not true. Writing SHALL call `add-batch` in scheduled mode with per-row detection off. The command SHALL then run `promote_scheduled.py --id --probe` and `validate-yaml --id` for the ids written. It SHALL NOT set `properties.is_national` to true. It SHALL NOT invoke `pytest` or `builder.py build`.

#### Scenario: Catalog rows are staged and promoted

- **WHEN** ingest runs on a probed file with two `verdict: catalog` rows that are not duplicates
- **THEN** both records are written as scheduled YAML and promoted when the promotion probe classifies them live
- **AND** each written id is passed to `validate-yaml --id`
- **AND** stdout ends with a `next:` line that runs `hunt.py log`

#### Scenario: Auth, empty, and duplicate rows are skipped

- **WHEN** a probed file contains rows with `verdict: auth`, `verdict: empty`, and `exists: true`
- **THEN** no YAML file is written for those rows
- **AND** the summary names each skip reason

#### Scenario: National flag is left unset

- **WHEN** ingest writes a record
- **THEN** the record does not contain `properties.is_national: true`

### Requirement: Unscoped next-hunt hint

The toolkit SHALL provide `hunt.py next` that prints at most five hunt suggestions from `dataquality/hunts.jsonl`. Suggestions SHALL prefer `named-directory` and `country-indicators`. Software targets whose latest row is `status: complete` within 14 days SHALL be omitted. `custom-review` SHALL be labeled deprioritized. The command SHALL NOT add, edit, or delete catalog files.

#### Scenario: Recently finished software is omitted

- **WHEN** `geoserver.es` was logged `complete` within the last 14 days
- **THEN** `next` does not suggest that slice

#### Scenario: Higher-yield kinds are listed first

- **WHEN** the log contains both unfinished `named-directory` work and `custom-review` work
- **THEN** the `named-directory` suggestion appears before any `custom-review` line
- **AND** the `custom-review` line is marked deprioritized

### Requirement: Next-command steering line

Every successful `prior`, `budget`, `search`, `dedupe`, `probe`, `ingest`, and `next` invocation SHALL end stdout with one line beginning with `next: `. Stop decisions SHALL use `next: none`.

#### Scenario: Continue prints the following command

- **WHEN** `prior` prints `decision: continue`
- **THEN** the last stdout line starts with `next: python scripts/hunt.py`

#### Scenario: Stop prints no follow-up search

- **WHEN** `prior` prints `decision: stop`
- **THEN** the last stdout line is `next: none`
