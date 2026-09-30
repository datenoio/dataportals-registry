# Scheduled entries

Unverified catalogs live under `data/scheduled/` with `status: scheduled` and `uid` values like `temp########`. They are included in `full.jsonl` / `full.parquet` / DuckDB, not in `catalogs.jsonl.zst`.

Current queue size is in [exports.md](exports.md#record-counts) (**49** YAML / **49** JSONL, as of 30 September 2026). After a discovery pass the queue grows; after `promote_scheduled.py` it shrinks.

Prefer `--scheduled` when adding finds you have not fully reviewed: [discovery.md](discovery.md), [agents/contribute.md](agents/contribute.md).

## Promote with the script

```bash
python scripts/promote_scheduled.py --dry-run          # preview all moves
python scripts/promote_scheduled.py --id reca --id recb # promote only these records
python scripts/promote_scheduled.py --probe            # probe liveness first; dead stay in scheduled
python scripts/promote_scheduled.py
python scripts/builder.py assign
python scripts/builder.py validate-yaml
```

`scripts/promote_scheduled.py`:

- Moves each YAML to `data/entities/{country}/{Federal|SUBREGION}/{type}/` — records with a valid `owner.location.subregion.id` (or coverage subregion) go to the subregion folder and get `level: 30`; unknown subregion codes warn and fall back to `Federal/`
- Sets `status` to `active`, or `inactive` when the host looks like staging/demo
- Infers country for `Unknown/` paths from coverage, owner, URL TLD, then `data/reference/country_hints.yaml`
- With `--probe`, classifies each `link` with the shared liveness vocabulary: `dead` records stay in scheduled untouched; `inconclusive`/`error` (403 bot protection, timeouts) promote with a warning
- Deletes the scheduled copy if the same `id` already exists as an entity
- `--id` limits the run to specific records and errors when an id matches no scheduled file

## Review the queue without moving anything

```bash
python scripts/promote_scheduled.py review-scheduled                 # probe + dedupe report
python scripts/promote_scheduled.py review-scheduled --no-probe      # fast, dedupe only
python scripts/promote_scheduled.py review-scheduled --country CN    # one inferred country
```

`review-scheduled` batch-checks every scheduled record against the entity exports (DuckDB, parquet fallback), probes liveness with bounded concurrency, shows the inferred country/subregion, and buckets each record as `promote-ready`, `needs-review`, `dead`, or `duplicate`. It writes a JSONL report (default `dataquality/scheduled_review.jsonl`, override with `--out`) and never moves or modifies files.

## Country hints

One-off country heuristics for `Unknown/` records live in `data/reference/country_hints.yaml`, not in code. Rules are evaluated in file order; the first match wins. Matching is case-insensitive substring matching against the record id + link:

```yaml
hints:
  - pattern: brasilio
    country: BR
  - all: [opendatasoft, zastrug]   # every substring must appear
    country: RS
```

Add new heuristics to that file; do not patch `promote_scheduled.py` for one-off cases.

## Manual promotion

1. Review the YAML (`link`, `catalog_type`, `software.id`, owner, coverage).
2. Move it to `data/entities/{COUNTRY}/{Federal|SUBREGION}/{type}/{id}.yaml`.
3. Filename must match `id`.
4. Run `assign` then `validate-yaml --id {id}`.

Without options, `validate-yaml` validates `data/entities/` only; `--id` also searches `data/scheduled/`. Rebuild exports after a batch: `python scripts/builder.py build`.

Duplicates: `python scripts/remove_scheduled_duplicates.py`.
