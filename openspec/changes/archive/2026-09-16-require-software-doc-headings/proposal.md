# Change: Require dedicated software recipe headings

## Why

CI only requires a backtick mention of each `software.id` in discovery and harvest guides. Leftover “Other platforms” tables pass that check, but agents cannot hunt from a one-line query: they need Signals, Confirm, and Keep/Drop on a unique `{#id}` heading. `software-index.md` also links to file tops instead of anchors when no H2 exists.

## What Changes

- Convert leftover-table software IDs into `## Name (`id`) {#id}` discovery sections, and add the three missing harvest H2s.
- Tighten `tests/test_docs_software_coverage.py` so every published `software.id` except `custom` has a unique discovery heading and a unique harvest heading.
- Clarify `MISSING_CONTACT_INFO` as `owner.link`, and fill known `documentation_url` values on software YAML.

## Impact

- Affected specs: `documentation-site`
- Affected code: `scripts/docs_software_coverage.py`, `tests/test_docs_software_coverage.py`
- Affected docs: discovery/harvest guides, `software-index.md`, `software-taxonomy.md`, `quality-rules.md`, `data-model.md`
- No breaking changes to catalog YAML schema
