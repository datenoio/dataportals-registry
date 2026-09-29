## MODIFIED Requirements

### Requirement: Dedicated software recipe headings

Every published catalog-discovery `software.id` except `custom` MUST have a unique discovery heading and a unique harvest heading of the form `## Name (`id`) {#id}`. A product in the `Statistical production software` category that has no discoverable public catalog MUST instead have an official product documentation URL and an entry in the software index, and MUST NOT be represented as a harvestable catalog.

#### Scenario: Catalog software retains recipes

- **WHEN** a contributor adds a catalog platform such as CKAN or NADA
- **THEN** the discovery and harvest guides each have the unique heading

#### Scenario: Production software without a public catalog

- **WHEN** a contributor adds CSPro or DataSHIELD as a production product
- **THEN** software documentation links to an official product page and explains the product's function
- **AND** the coverage guard does not demand a fictitious catalog harvest recipe
