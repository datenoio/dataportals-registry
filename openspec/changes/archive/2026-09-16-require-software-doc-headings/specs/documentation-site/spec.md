## ADDED Requirements

### Requirement: Dedicated software recipe headings
Every published `software.id` except `custom` MUST have a unique discovery heading and a unique harvest heading of the form `## Name (`id`) {#id}`.

#### Scenario: Table-only mention is not enough
- **WHEN** a published `software.id` appears only as a backtick in an “Other platforms” table
- **THEN** `tests/test_docs_software_coverage.py` fails
- **AND** the failure names the missing discovery or harvest heading

#### Scenario: Unique heading per software id
- **WHEN** a contributor adds a software definition that is a discovery target
- **THEN** the matching discovery guide and harvest guide each include one `## Name (`id`) {#id}` heading
- **AND** `docs/software-index.md` links to those anchors

#### Scenario: Custom stays unheaded
- **WHEN** the software id is `custom`
- **THEN** the heading coverage guard does not require a dedicated `{#custom}` recipe heading
