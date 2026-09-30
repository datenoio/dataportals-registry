## ADDED Requirements

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
