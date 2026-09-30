# agent-documentation Specification

## Purpose
Root `llms.txt`, `DATASHEET.md`, `CITATION.cff`, and `SECURITY.md` so LLM agents and researchers can find consumption contracts, citation, and disclosure paths.
## Requirements
### Requirement: LLM Agent Index File
The repository MUST provide an `llms.txt` file at the root for agent discovery.

#### Scenario: Agent loads llms.txt
- **WHEN** an LLM agent reads `/llms.txt`
- **THEN** it finds concise descriptions and links to AGENTS.md, schema files, data exports, and quality outputs
- **AND** the file is under 500 lines

### Requirement: Dataset Datasheet
The registry MUST publish a `DATASHEET.md` describing dataset characteristics and limitations.

#### Scenario: Downstream consumer assesses fitness for use
- **WHEN** a researcher or agent reads `DATASHEET.md`
- **THEN** it describes geographic coverage bias, record count, update cadence, and known limitations
- **AND** it references the CC-BY 4.0 data license

### Requirement: Citation Metadata
The repository MUST include a `CITATION.cff` file for academic attribution.

#### Scenario: Researcher cites the registry
- **WHEN** a researcher uses citation tooling on the repository
- **THEN** `CITATION.cff` provides title, authors, repository URL, and license
- **AND** includes a preferred citation string

### Requirement: Security Disclosure Policy
The repository MUST publish a `SECURITY.md` vulnerability reporting policy.

#### Scenario: Reporter finds a security issue
- **WHEN** a user reads `SECURITY.md`
- **THEN** they find instructions for responsible disclosure
- **AND** a contact method or issue label is specified

### Requirement: Valid Documentation Links
README and agent docs MUST not reference missing files.

#### Scenario: README quality report link
- **WHEN** a user follows the quality findings link in `README.md`
- **THEN** the target file exists in the repository
- **AND** is not a 404 path

### Requirement: Hunt command card on agent entry points

Discovery sessions MUST be steered by one command card that is present in the always-loaded agent guide, the discovery cursor rule, the opening of `docs/agents/discover.md`, and `llms.txt`. The card MUST name `python scripts/hunt.py prior` as the first command and MUST tell the agent to follow each `next:` line. The card MUST state that a hand-written FOFA client, an export-query heredoc, and an HTTP probe script are not used for a step `hunt.py` already covers. The hunt-kind list published for agents MUST be the same set as `HUNT_KINDS` in `scripts/hunt.py`.

#### Scenario: Always-loaded guide starts with prior

- **WHEN** an agent reads the Discover catalogs task in `AGENTS.md`
- **THEN** the first command in that task is `python scripts/hunt.py prior`
- **AND** the task tells the agent to execute the `next:` line from that command

#### Scenario: Discovery rule matches the guide

- **WHEN** an agent reads `.cursor/rules/catalog-discovery.mdc`
- **THEN** it contains the same command sequence as the Discover catalogs task in `AGENTS.md`
- **AND** it tells the agent not to write a FOFA, export-query, or HTTP-probe script for a step `hunt.py` covers

#### Scenario: Discover guide opens with the card

- **WHEN** an agent reads the start of `docs/agents/discover.md`
- **THEN** the command card appears before the hunt-type narratives
- **AND** the card includes `prior`, `search`, `probe`, `ingest`, and `log`

#### Scenario: Agent index names the gate

- **WHEN** an agent reads the discovery bullet in `llms.txt`
- **THEN** the bullet names `python scripts/hunt.py prior` as the start of a discovery session

#### Scenario: Published kinds match the CLI

- **WHEN** `docs/agents/improve.md` lists allowed hunt kinds
- **THEN** that set is equal to `HUNT_KINDS` in `scripts/hunt.py`

#### Scenario: Hunt sessions do not run the full test suite

- **WHEN** an agent follows the command card for a discovery hunt
- **THEN** validation is `validate-yaml --id` for the ids just written
- **AND** the card does not instruct the agent to run `pytest` or `builder.py build` as part of the hunt

