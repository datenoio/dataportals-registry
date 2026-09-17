# CLI reference

All commands run from the repository root unless noted.

```bash
pip install -r requirements.txt
python scripts/builder.py --help
```

Python **3.10–3.12**. Test layout: [tests/README.md](https://github.com/datenoio/dataportals-registry/blob/main/tests/README.md).

## Essential commands

| Command | Purpose |
|---------|---------|
| `python scripts/builder.py build` | Rebuild JSONL, zstd, Parquet, and DuckDB from YAML |
| `python scripts/builder.py build --jsonld` | Also emit `data/datasets/catalogs.jsonld` |
| `python scripts/builder.py validate-yaml` | Validate entity YAML against the Cerberus schema |
| `python scripts/builder.py validate-yaml --id catalogdatafaagov` | Validate one catalog id |
| `python scripts/builder.py validate-yaml --file path/to/file.yaml` | Validate one file |
| `python scripts/builder.py validate` | Validate built `full.jsonl` against the same schema |
| `python scripts/builder.py validate-software` | Software YAML coverage/profile checks. `version` and `repository_url` thresholds apply to OSS subtypes, not SaaS/CMS/geo viewers. Fails if `software_ids.yaml` does not match `data/software/` |
| `python scripts/builder.py sync-software-maps` | Rewrite `data/reference/software_ids.yaml` from software YAML |
| `python scripts/builder.py assign` | Assign missing `cdi########` UIDs in entities (`--dryrun` to preview) |
| `python scripts/builder.py assign --new` | Incremental: only git-changed YAML (untracked/modified under `data/entities/` + `data/scheduled/`); entities get `cdi########`, scheduled `temp########`. Fast `uid:`-line scan for used numbers, no full YAML parse |
| `python scripts/builder.py assign --mode scheduled` | Assign `temp########` UIDs in scheduled |

All `assign` paths cross-check to-be-assigned UIDs against the dataset exports (`datasets.duckdb` read-only, `full.parquet` fallback on lock) and **fail without writing** on collision — a collision means exports diverged from YAML (e.g. a deleted record); rebuild exports first. When exports are absent the check is skipped with a warning.
| `python scripts/builder.py validate-yaml --changed` | Validate only git-changed YAML (untracked/modified under `data/entities/` + `data/scheduled/`) — fast pre-commit check; mutually exclusive with `--file`/`--id` |
| `python scripts/builder.py schema-values FIELD` | Print allowed values for a field: schema enums (`catalog_type`, `status`, `access_mode`) or reference vocabularies (`owner.type`, `langs`, `owner.location.subregion` with `--country`, `software.id`) |
| `python scripts/builder.py analyze-quality` | Write `dataquality/` reports |
| `python scripts/builder.py quality-control` | Terminal completeness metrics (`--mode full` or `catalogs`) |
| `pytest` | Test suite with coverage |

## Adding catalogs

```bash
python scripts/builder.py add-single "https://example.com/data" \
  --software ckan \
  --catalog-type "Open data portal" \
  --name "Example Data Portal" \
  --country US \
  --scheduled
```

Use `--no-scheduled` to write under `data/entities/`. After adding files, run `assign` then `validate-yaml`.

Additional `add-single` options: `--subregion PT-11` (ISO 3166-2 code; routes to `{CC}/{SUB}/` and sets level 30), `--owner-type "Local government"` (validated against `data/reference/owner_types.yaml`, synonyms canonicalized), `--is-national`, `--id CUSTOMID` (lowercase letters/digits, for path-based tenants), `--no-detect` (skip the apidetect probe), `--lang it` (resolved to `{id, name}` via `data/reference/langs.csv`; when omitted, the language is auto-filled from the country). Records are schema-validated before writing; invalid records are refused with an error.

For multi-record hunts, use a JSONL manifest (one record per line):

```bash
python scripts/builder.py add-batch manifest.jsonl
```

```json
{"url": "https://dados.cm-faro.pt", "name": "Faro Open Data", "software": "ckan", "catalog_type": "Open data portal", "country": "PT", "subregion": "PT-08", "owner_name": "Municipality of Faro", "owner_type": "Local government", "langs": ["pt"], "is_national": false}
```

`add-batch` loads the exports once, skips rows whose canonical URL, host (root-path URLs), or id already exist (reporting the existing id), validates every row against the schema before writing, writes valid rows only, and assigns UIDs to all new records before exiting. `--no-scheduled` writes under `data/entities/`; `--detect` runs apidetect probes (off by default).

| Command | Purpose |
|---------|---------|
| `add-single` | One URL |
| `add-batch FILENAME` | JSONL manifest, one record per line (preferred for hunts) |
| `add-list FILENAME` | One URL per line (legacy; superseded by `add-batch`) |

## Updating records

```bash
# Set one field on one record (schema-validated before saving)
python scripts/builder.py set-field --id datagov --path properties.is_national --value true
python scripts/builder.py set-field --id datagov --path tags --value transport --append

# Bulk updates from a JSONL manifest (dry-run by default)
python scripts/builder.py enrich-batch updates.jsonl          # preview diffs
python scripts/builder.py enrich-batch updates.jsonl --write  # apply
```

`set-field` resolves the record across entities and scheduled, creates intermediate dicts for dotted paths, and parses `--value` with YAML scalar rules (`true` → bool, `30` → int, `[a, b]` → list, otherwise string — quote to force a string). It refuses to touch `uid`/`id` and leaves the file unchanged when the update would break schema validation.

`enrich-batch` rows are `{"id": ..., "set": {"dotted.path": value, ...}}` or `{"id": ..., "merge": {"field": {...}}}` (recursive dict merge). Every updated record is schema-validated; invalid rows are reported and skipped. The summary counts updated / unchanged / skipped (unknown id) / invalid.
| `add-opendatasoft-catalog FILENAME` | Prepared OpenDataSoft JSONL |
| `add-socrata-catalog FILENAME` | Prepared Socrata JSONL |
| `add-arcgishub-catalog FILENAME` | Prepared ArcGIS Hub JSONL (writes entities; `--force` to overwrite) |
| `add-legacy` | Maintainer: ingest `UNPROCESSED` `.txt` lists |

Finding catalogs: [discovery.md](discovery.md), [agents/discover.md](agents/discover.md). Listing datasets inside a catalog: [harvest.md](harvest.md). CKAN bulk import: [ckan-sync.md](ckan-sync.md). OpenAIRE Graph data sources: [openaire-sync.md](openaire-sync.md). Promote scheduled: [scheduled.md](scheduled.md).

## Enrichment and monitoring

```bash
python scripts/re3data_enrichment.py enrich --dry-run
python scripts/sync_ckan_ecosystem.py --dry-run
python scripts/extract_openaire_portals.py list-sources --output /tmp/openaire_sources.json
python scripts/apidetect.py detect-single catalogdatagov --dryrun
python scripts/check_liveness.py --sample 10
python scripts/calculate_trust_scores.py --dry-run
python scripts/promote_scheduled.py --dry-run
```

Re3Data: [re3data.md](re3data.md). Endpoint maps: [apidetect.md](apidetect.md) (`detect-software`, `detect-country`; dry-run first). URL reachability: [liveness.md](liveness.md) (weekly workflow, report-only JSONL; does not change YAML `status`). Quality-fix and legacy enrich scripts: [enrichment.md](enrichment.md). Probe APIs only after a catalog YAML exists.

## Quality helpers

```bash
python scripts/fix_critical_issues.py
python scripts/fix_important_issues.py
python scripts/fix_is_national_flags.py --dry-run
python scripts/update_quality_baseline.py
python scripts/builder.py fix
python scripts/generate_cursor_commands.py
```

`builder.py fix` drives `cursor-agent` against `dataquality/primary_priority.jsonl` (requires the Cursor CLI). `fix_is_national_flags.py` unsets `properties.is_national` on agency/thematic/scientific/subnational catalogs ([data-model.md](data-model.md#propertiesis_national)). Issue codes: [quality-rules.md](quality-rules.md). Workflow: [metadata-quality.md](metadata-quality.md).

## Reports and dumps

| Command | Purpose |
|---------|---------|
| `python scripts/builder.py export` | Flattened CSV (`export.csv`) |
| `python scripts/builder.py stats` | Country × software TSV (`country_software.csv`) |
| `python scripts/builder.py report` | Legacy incomplete-field scan on `full.jsonl` |
| `python scripts/builder.py country-report` | Per-country counts from Parquet |
| `python scripts/builder.py get-countries` | Print a `COUNTRIES` map snippet |
| `python scripts/builder.py validate-typing` | Optional pydantic check (needs `cdiapi`) |
| `python scripts/builder.py build-docs` | Software stub markdown for the sibling `cdi-docs` repo |

## Tests

```bash
pytest
pytest tests/test_builder.py -v
pytest -m unit
pytest --no-cov
```

CI (`.github/workflows/tests.yml`) runs `validate-yaml`, pytest on Python 3.10–3.12, and the quality regression guard.
