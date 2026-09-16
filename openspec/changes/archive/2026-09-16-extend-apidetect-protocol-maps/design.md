## Context

`apidetect` GETs URL templates per `software.id` and writes `endpoints[]`. Quality fixers call `infer_endpoints_verified`, which already skips `custom`. `detect-country` / unknown IDs currently fall back to `CUSTOM_URLMAP` (`/data.json` + sitemaps). Widening that map without a gate would crawl every unclassified catalog.

## Goals / Non-Goals

- Goals: probe harvest-documented protocols and dumps; keep custom opt-in; preserve insert-skip-if-present; type SensorThings correctly.
- Non-Goals: new `catalog_export` list type; quality-fixer crawls of `custom`; viewer WMS maps; `detect-all`; datastore/row APIs.

## Decisions

- Decision: `--include-custom` on detect CLI commands. `infer_endpoints_verified` still returns `[]` for `custom`. Unknown software is not remapped to `custom` unless the flag is set.
- Decision: Dumps stay in `endpoints[]`. `catalog_export` is documented as unused.
- Decision: New `metadata_support` keys are optional (`required: false`) so existing software YAML stays valid.
- Decision: FROST probe `id` is `sensorthings`. Do not `--action replace` on existing FROST records.
- Decision: Protocol backfill on records that already have endpoints uses `--action update` (insert skips those records).
- Alternatives considered: enabling custom in quality fixers (rejected: HTTP volume and sitemap false positives); replacing `catalog_export` with a dump list (rejected: duplicates `endpoints[]`).

## Risks / Trade-offs

- MIME-loose probes can store HTML 200s as CSW/OAI → keep XML/JSON/Turtle/SPARQL MIME lists; no HTML on protocol probes.
- CKAN/DSpace/GeoNetwork live runs are large → per-software `--dryrun`, then insert (`--max-endpoints 1`) or update; stop on 401/403.

## Migration Plan

1. Land maps and tests.
2. Dry-run mapped software with empty endpoints, then insert.
3. Update-mode backfill for CKAN OAI/RDF, GeoNetwork DCAT/OGC API, IR OAI, SPARQL dumps.
4. Optional sampled `detect-software custom --include-custom --dryrun`.
5. Regenerate `data/reference/endpoint_types.yaml` after writes.

## Open Questions

- None for this change; custom probing is opt-in as approved.
