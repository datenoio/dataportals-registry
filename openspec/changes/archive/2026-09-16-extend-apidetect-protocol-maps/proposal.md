# Change: Extend apidetect protocol, API, and dump maps

## Why

Harvest docs already describe OAI-PMH, DCAT RDF dumps, SPARQL, SensorThings, CSW, and OGC API Records. Detection and catalog records lag: CKAN has no OAI probes, GeoNetwork has no GeoDCAT/OGC API Records probes, FROST probes would be typed `customapi`, quality fixers skip `custom` catalogs, and `catalog_export` is unused. Harvestable dumps belong in `endpoints[]`.

## What Changes

- Widen `CUSTOM_URLMAP` with common catalog dumps (DCAT RDF/XML/JSON-LD/Turtle, OAI-PMH Identify, CSW, SPARQL, OpenSearch, RSS/Atom). Quality fixers still skip `custom`.
- Gate CLI probing of `custom` (and unknown software falling back to the custom map) behind `--include-custom`.
- Add CKAN/DataPress OAI-PMH and `/catalog.rdf` / `/feeds/dcat` probes.
- Add GeoNetwork GeoDCAT RDF and OGC API Records collection probes.
- Add SPARQL/DCAT dump probes for GET-able `rdf_sparql: Yes` software (Piveau, Wikibase, FAIR Data Point, Idra, TriplyDB, PublishMyData).
- Type FROST-Server probes as `sensorthings`.
- Add deegree `/deegree-webservices/` CSW/WMS path variants.
- Put `hdc` in `NO_STANDARD_PROBE`.
- Document preferred `endpoints[].type` values and that `catalog_export` is an unused leftover.
- Add optional `metadata_support` keys (`sensorthings`, `odata`, `tap`, `graphql`, `jsonstat`, `openapi`, `wmts`).

No breaking catalog schema change. Default `--action insert` is unchanged; protocol backfill on records that already have endpoints uses `--action update`.

## Impact

- Affected specs: `api-endpoint-detection`
- Affected code:
  - `scripts/apidetect.py`
  - `scripts/apidetect_urlmaps_draft.py`
  - `tests/test_apidetect.py`
  - `docs/apidetect.md`, `docs/vocabularies.md`, `docs/data-model.md`
  - `data/schemes/software.json` (optional keys)
  - selected `data/software/**/*.yaml`
  - catalog YAML only after mocked tests pass, via `detect-software` insert/update
