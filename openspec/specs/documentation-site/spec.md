# documentation-site Specification

## Purpose
Publish internals documentation from `docs/` via Docusaurus on GitHub Pages, keeping `devdocs/` as working notes only.
## Requirements
### Requirement: Published documentation source
The repository MUST keep human- and agent-facing internals documentation as Markdown under `docs/`, separate from working notes in `devdocs/`.

#### Scenario: Agent reads internals docs without Node
- **WHEN** an agent opens `docs/getting-started.md` or `docs/agents/query.md` from the repository
- **THEN** the files exist as Markdown at those paths
- **AND** they describe exports, schema, and contribution rules without requiring the Docusaurus build

#### Scenario: Analysis notes are not the site source
- **WHEN** a contributor looks for GeoSeer analysis or similar working notes
- **THEN** those files live under `devdocs/`
- **AND** they are not required to build the documentation site

### Requirement: Docusaurus GitHub Pages site
The repository MUST provide a Docusaurus site that publishes `docs/` to GitHub Pages.

#### Scenario: Local site build
- **WHEN** a maintainer runs `npm ci` and `npm run build` in `website/`
- **THEN** a static site is written to `website/build`
- **AND** the site uses base URL `/dataportals-registry/`

#### Scenario: GitHub Pages deploy workflow
- **WHEN** documentation files under `docs/` or `website/` change on `main`
- **THEN** `.github/workflows/deploy-docs.yml` builds the site and deploys it with GitHub Pages actions

### Requirement: Agent discovery from the site
The documentation site MUST serve the repository `llms.txt` index at a stable URL.

#### Scenario: Agent fetches hosted llms.txt
- **WHEN** an agent requests `llms.txt` from the GitHub Pages origin
- **THEN** the file is available at `/dataportals-registry/llms.txt`
- **AND** a copy is available at `/dataportals-registry/.well-known/llms.txt`

### Requirement: Catalog discovery instructions
The published documentation MUST explain how humans and agents find catalogs that are not yet in the registry, including duplicate checks against exports.

#### Scenario: Human reads discovery guide
- **WHEN** a contributor opens `docs/discovery.md`
- **THEN** the page distinguishes querying existing records from finding unregistered catalogs
- **AND** it lists high-yield external lists, software probe patterns, and the add-single / scheduled handoff

#### Scenario: Agent follows discovery workflow
- **WHEN** an agent opens `docs/agents/discover.md`
- **THEN** the page requires an export duplicate check before probing the web
- **AND** it forbids internet-wide scanning and authentication bypass
- **AND** it hands off accepted finds to the contribute workflow

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

