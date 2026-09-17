## 1. set-field command

- [x] 1.1 Implement `builder.py set-field --id ID --path dotted.path --value VALUE` resolving the record across entities and scheduled
- [x] 1.2 Parse `--value` with YAML scalar rules (`true`→bool, `30`→int, `[a, b]`→list, otherwise string)
- [x] 1.3 Create intermediate dicts for missing path segments; `--append` appends to list fields instead of replacing
- [x] 1.4 Refuse to modify `uid` and `id` (dedicated commands own those)
- [x] 1.5 Re-validate the updated record against the catalog schema; on failure print errors and leave the file unchanged

## 2. enrich-batch command

- [x] 2.1 Implement `builder.py enrich-batch manifest.jsonl` accepting rows of `{id, set: {path: value}}` or `{id, merge: {field: {...}}}`
- [x] 2.2 Default to dry-run: print a per-record diff summary (fields changed, old → new) without writing
- [x] 2.3 `--write` applies updates; schema-validate each updated record and skip-with-error rows that would become invalid
- [x] 2.4 Print a summary: updated, skipped (unknown id), invalid (with reasons)

## 3. Tests and docs

- [x] 3.1 Tests: scalar parsing, nested path creation, --append on lists, uid/id refusal, schema-refusal leaves file unchanged, enrich-batch dry-run vs --write, unknown-id skip
- [x] 3.2 Update `docs/cli.md` and `docs/agents/contribute.md`
- [x] 3.3 Run `pytest`
