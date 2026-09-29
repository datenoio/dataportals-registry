## ADDED Requirements

### Requirement: Distinct non-catalog software category

The registry SHALL support statistical production software that is not itself a discoverable data catalog, without assigning it a catalog category.

#### Scenario: Census processing product

- **WHEN** CSPro is registered from official U.S. Census Bureau documentation
- **THEN** its software definition uses the production category
- **AND** it does not claim to be a microdata catalog
- **AND** it passes software schema and ID-map validation

#### Scenario: Controlled analysis product

- **WHEN** DataSHIELD is registered from official project documentation
- **THEN** its description distinguishes federated analysis and disclosure controls from public data download
- **AND** its definition passes software schema and ID-map validation

### Requirement: Unchanged catalog classification

Existing catalog-platform records SHALL retain their categories and validation behavior.

#### Scenario: Existing catalog software

- **WHEN** the software validator runs on existing CKAN, NADA, and PxWeb definitions
- **THEN** their category and subtype semantics remain unchanged
