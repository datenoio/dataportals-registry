## MODIFIED Requirements

### Requirement: Dedicated software recipe headings

Every published catalog-discovery `software.id` except `custom` MUST have a unique discovery heading and a unique harvest heading of the form `## Name (`id`) {#id}`. A product in the `Statistical production software` category that has no discoverable public catalog MUST instead have an official product documentation URL and an entry in the software index, and MUST NOT be represented as a harvestable catalog.

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

#### Scenario: Catalog software retains recipes

- **WHEN** a contributor adds a catalog platform such as CKAN or NADA
- **THEN** the discovery and harvest guides each have the unique heading

#### Scenario: Production software without a public catalog

- **WHEN** a contributor adds CSPro or DataSHIELD as a production product
- **THEN** software documentation links to an official product page and explains the product's function
- **AND** the coverage guard does not demand a fictitious catalog harvest recipe
