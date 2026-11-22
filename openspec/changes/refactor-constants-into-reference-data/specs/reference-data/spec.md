## ADDED Requirements

### Requirement: Software Facts Live in Software YAML

Per-software facts SHALL be stored only in that software's `data/software/**/*.yaml` file:

- documentation URL;
- repository URL;
- export formats;
- name aliases;
- allowed catalog types.

`scripts/constants.py` SHALL derive `SOFTWARE_NAME_ALIASES` and `MAP_SOFTWARE_ALLOWED_CATALOG_TYPES` from those files.

#### Scenario: New alias added in YAML

- **WHEN** a contributor adds `aliases: ["Open Data Portal X"]` to `data/software/opendata/examplesoftware.yaml`
- **THEN** `constants.SOFTWARE_NAME_ALIASES["Open Data Portal X"]` equals `examplesoftware` without any edit to `constants.py`

#### Scenario: Invalid catalog type rejected

- **WHEN** a software YAML has `allowed_catalog_types: ["Not a type"]`
- **THEN** `python scripts/builder.py validate-software` reports the value as not allowed

### Requirement: Lookup Tables Live in data/reference

Registry lookup tables SHALL be stored as files under `data/reference/`, and `scripts/constants.py` SHALL load them. This covers the domain-to-location map, top-level-domain languages, registry country names and bloc folders. Each table SHALL exist in exactly one file.

#### Scenario: Domain location added without code change

- **WHEN** a contributor adds an entry to `data/reference/domain_locations.yaml`
- **THEN** `constants.DOMAIN_LOCATIONS` contains it on the next import

#### Scenario: No duplicate reference copies

- **WHEN** the test suite runs
- **THEN** it fails if two files in `data/reference/` share a base name (for example `langs.csv` and `langs.tsv`)

### Requirement: Stable Constants Interface

Moving a table out of `constants.py` SHALL NOT change the name or the value of any public constant, unless the change is listed in the snapshot fixture together with a reason. `constants.py` SHALL NOT contain a literal dict or list with more than 50 entries.

#### Scenario: Value preserved after a move

- **WHEN** `DOMAIN_LOCATIONS` moves to `data/reference/domain_locations.yaml`
- **THEN** the snapshot test shows that `constants.DOMAIN_LOCATIONS` is equal to its previous value

#### Scenario: Large literal rejected

- **WHEN** a pull request adds a 60-entry dict literal to `constants.py`
- **THEN** the guard test fails and names the file in `data/reference/` or `data/software/` that should hold the data
