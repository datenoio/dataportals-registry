# Change: Add set-field and enrich-batch record update commands

## Why

Updating existing records is entirely manual today: agents hand-edit YAML or write throwaway
scripts for routine changes like setting a subregion, correcting an owner type, or flipping
`is_national` — owner-type and subregion edits account for 164 and 134 friction mentions across
150 recent sessions, and bulk-update heredocs are a recurring pattern. There is no CLI that
updates a single field on one record with schema validation, and no manifest-driven bulk update
command.

## What Changes

- Add `builder.py set-field --id ID --path dotted.field.path --value VALUE`:
  - Resolves the record in entities or scheduled by id.
  - Sets the dotted path (creating intermediate dicts; `--append` for list fields).
  - Parses `--value` as YAML scalars (`true`, `30`, lists) so typed values land correctly.
  - Re-validates the record against the catalog schema before saving; refuses invalid updates.
- Add `builder.py enrich-batch manifest.jsonl`:
  - One JSONL row per update: `{id, set: {path: value, ...}}` or `{id, merge: {...}}`.
  - Dry-run by default (`--write` to apply), printing a per-record diff summary.
  - Schema-validates every updated record; invalid updates are reported and skipped.
- Both commands preserve existing file formatting as much as the current YAML writer allows and
  never touch `uid`.

## Impact

- Affected specs: `record-enrichment` (new capability)
- Affected code: `scripts/builder.py` (new commands), `tests/test_builder.py`, `docs/cli.md`,
  `docs/agents/contribute.md`
