# dataportals-registry

A global registry of data portals, catalogs, data repositories, and related data infrastructure.

**Working tree (26 August 2026):** **23,338** verified catalogs · **264** software platforms · **219** countries and territories · **0** scheduled records.

Last published snapshot: [v1.17.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.17.0), 25 August 2026 (**22,750** catalogs · **262** software · **0** scheduled).

This is the catalog-metadata pillar of the [Common Data Index](https://dateno.io) / open search engine. It describes **catalogs** (open data portals, geoportals, scientific repositories, indicator sites, and similar infrastructure), not the datasets those catalogs hold.

- **Source of truth:** YAML under [`data/entities/`](data/entities/)
- **Consume:** JSONL, Parquet, and DuckDB under [`data/datasets/`](data/datasets/) — do not parse thousands of YAML files
- **Out of scope:** this repository does not host a production query API or MCP server

Code is [MIT](LICENSE); data and documentation are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Inspired by [re3data](https://www.re3data.org/) and [FAIRsharing](https://fairsharing.org/), with a broader focus on open data of every kind — government, geospatial, scientific, and statistical — not only research data.

## Using the data

Python **3.10–3.12**. Install deps with `pip install -r requirements.txt`. Nested fields in DuckDB and Parquet are native `STRUCT` / `LIST` types; query them with field access, not `LIKE` on JSON text.

```bash
duckdb data/datasets/datasets.duckdb \
  -c "SELECT id, name, link FROM catalogs WHERE software.id = 'ckan' LIMIT 10;"
```

```python
import duckdb

con = duckdb.connect("data/datasets/datasets.duckdb")
con.execute(
    """
    SELECT id, name, link
    FROM catalogs
    WHERE catalog_type = 'Open data portal'
      AND list_contains(
            list_transform(coverage, x -> x.location.country.id),
            'US'
          )
    LIMIT 10
    """
).fetchall()
```

More patterns: [docs/query-examples.md](docs/query-examples.md). Join keys and column types: [docs/ai-consumers.md](docs/ai-consumers.md).

### Data exports

Last published snapshot (**v1.17.0**, 2026-08-25: 22,750 catalogs, 262 software, 0 scheduled). Working-tree dumps last rebuilt at **22,835** catalogs / **26** scheduled; source YAML is now **23,338** entities / **0** scheduled. Record-count contract: [docs/exports.md](docs/exports.md#record-counts).

| File | Contents |
|------|----------|
| `data/datasets/catalogs.jsonl` (+ `.zst`) | **22,835** verified catalog records (export lag) |
| `data/datasets/software.jsonl` (+ `.zst`) | **264** software / platform definitions |
| `data/datasets/scheduled.jsonl` (+ `.zst`) | **26** records in the last export (source YAML is empty) |
| `data/datasets/full.jsonl` (+ `.zst`) | Entities + scheduled (**22,861**) |
| `data/datasets/full.parquet`, `data/datasets/datasets.duckdb` | Analytics-friendly copies of `full.jsonl` |

Rebuild from YAML (never hand-edit `data/datasets/`):

```bash
python scripts/builder.py build
```

Decompress `.zst` with `unzstd file.zst`. Filter by `catalog_type` or `software.id` in DuckDB or Parquet; there are no pre-sliced `bytype/` or `bysoftware/` dumps.

## What is in the registry

Each record is one catalog: name, URL, owner, geographic coverage, software platform, API/harvest endpoints, and optional identifiers (Wikidata, re3data, OpenAIRE, …).

| `catalog_type` | Folder | Typical contents |
|----------------|--------|------------------|
| Open data portal | `opendata/` | Government and institutional open data |
| Geoportal | `geo/` | Spatial data, OGC services, map viewers |
| Scientific data repository | `scientific/` | Research data, CRIS, institutional repos |
| Indicators catalog | `indicators/` | Statistical indicators, SDMX, dashboards |
| Microdata catalog | `microdata/` | Survey / census microdata |
| Machine learning catalog | `ml/` | ML datasets and models |
| Data search engine | `search/` | Cross-catalog search / aggregators |
| API Catalog | `api/` | API directories |
| Data marketplace | `marketplace/` | Commercial data markets |
| Metadata catalog | `metadata/` | Metadata registries |
| Other | `other/` | Uncategorized |

Use this registry to find portals by country, type, or software, join catalogs to external identifiers, or feed a downstream harvester from `endpoints[]`. Do **not** use it to search for a dataset by title — harvest the remote catalog instead ([docs/harvest.md](docs/harvest.md)). Scope: [docs/when-to-use.md](docs/when-to-use.md).

## Documentation

Published internals for humans and coding agents:

| Goal | Start here |
|------|------------|
| Docs site | <https://datenoio.github.io/dataportals-registry/> |
| Getting started | [docs/getting-started.md](docs/getting-started.md) |
| Field reference and vocabularies | [docs/data-model.md](docs/data-model.md), [docs/vocabularies.md](docs/vocabularies.md), [docs/catalog-types.md](docs/catalog-types.md) |
| Software IDs | [docs/software-index.md](docs/software-index.md), [docs/software-taxonomy.md](docs/software-taxonomy.md) |
| Find catalogs not yet registered | [docs/discovery.md](docs/discovery.md) |
| Harvest datasets from a catalog API | [docs/harvest.md](docs/harvest.md) |
| CLI | [docs/cli.md](docs/cli.md) |
| Agent index | [`llms.txt`](llms.txt) (also `/dataportals-registry/llms.txt` on the docs site) |

Source markdown lives in [`docs/`](docs/). Local preview: `cd website && npm install && npm run start`. Working notes stay in [`devdocs/`](devdocs/) and are not on the site.

## Repository layout

Catalog YAML: `data/entities/{COUNTRY}/{Federal|SUBREGION}/{type}/{id}.yaml`. Filename must equal `id` (lowercase letters and digits only). Layout and field rules: [docs/directory-layout.md](docs/directory-layout.md), [docs/data-model.md](docs/data-model.md).

```
data/entities/{CC}/{Federal|SUBREGION}/{type}/{id}.yaml   verified catalogs
data/scheduled/                                          unverified (promote later)
data/software/                                           platform definitions
data/schemes/                                            Cerberus + JSON Schema
data/reference/                                          controlled vocabularies
data/datasets/                                           generated exports (do not edit)
```

Example — FAA Open Data Portal (`data/entities/US/Federal/opendata/catalogdatafaagov.yaml`):

```yaml
id: catalogdatafaagov
uid: cdi00005263
name: Federal Aviation Administration Open Data Portal
link: https://catalog.data.faa.gov
catalog_type: Open data portal
access_mode:
- open
status: active
api: true
api_status: active
software:
  id: ckan
  name: CKAN
owner:
  name: Federal Aviation Administration
  type: Central government
  location:
    country:
      id: US
      name: United States
    level: 20
coverage:
- location:
    country:
      id: US
      name: United States
    level: 20
```

`properties.is_national: true` only for the country’s official catalog of that type (national open-data portal, NSDI/geoportal, or NSO product) — not because the owner is a federal agency. See [docs/data-model.md](docs/data-model.md#propertiesis_national).

## Finding catalogs

**Already in this registry**

- **By geography:** `data/entities/{COUNTRY_CODE}/` (for example `US`, `FR`, `BR`). `Federal/` is national/central; subregion folders are ISO 3166-2 style (`US-CA`, `GB-SCT`, `BR-SP`).
- **By type:** under each country, `opendata/`, `geo/`, `scientific/`, `indicators/`, `microdata/`, `ml/`, `search/`, `api/`, `marketplace/`, `metadata/`, `other/`.
- **By software:** filter `software.id` in DuckDB (canonical IDs: [docs/software-index.md](docs/software-index.md)). Platform YAML in `data/software/` also has `category` and `subtype` for self-hosted vs SaaS vs protocol-first comparisons.
- **By URL / id:** query `catalogs` rather than walking YAML:

```sql
SELECT id, name, link, catalog_type, status
FROM catalogs
WHERE lower(link) LIKE '%data.faa.gov%'
   OR id = 'catalogdatafaagov';
```

**Not yet in this registry**

Vendor galleries, search-engine recipes, and per-platform fingerprints: [docs/discovery.md](docs/discovery.md) (humans) and [docs/agents/discover.md](docs/agents/discover.md) (agents). Search tools: [docs/discovery-search-tools.md](docs/discovery-search-tools.md). LLM / MCP setup: [docs/discovery-agent-tools.md](docs/discovery-agent-tools.md). Endpoint fill: [docs/apidetect.md](docs/apidetect.md). URL liveness: [docs/liveness.md](docs/liveness.md).

## Data quality

Quality analysis flags duplicate URLs, path/owner country mismatches, non-canonical owner types, schema violations, and related issues. CI guards regressions with `dataquality/baseline_counts.json`. Issue codes: [docs/quality-rules.md](docs/quality-rules.md).

```bash
python scripts/builder.py validate-yaml
python scripts/builder.py analyze-quality
```

Reports land in `dataquality/` (`full_report.txt`, `primary_priority.jsonl`, plus per-country and per-priority breakouts). Helper scripts `scripts/fix_*_issues.py` apply automated fixes by priority. Workflow: [docs/metadata-quality.md](docs/metadata-quality.md).

## Contributing

Fixes and new catalogs are welcome via [pull request](https://github.com/datenoio/dataportals-registry/pulls) or [issue](https://github.com/datenoio/dataportals-registry/issues). Full guide: [CONTRIBUTING.md](CONTRIBUTING.md). Agents: [docs/agents/contribute.md](docs/agents/contribute.md).

```bash
python scripts/builder.py add-single "https://example.com/data" \
  --software ckan \
  --catalog-type "Open data portal" \
  --name "Example Data Portal" \
  --country US \
  --scheduled

python scripts/builder.py assign
python scripts/builder.py validate-yaml --id examplecom
```

Prefer `--scheduled` for unverified finds; promote later ([docs/scheduled.md](docs/scheduled.md)). Duplicate `link` values fail quality checks.

## Enrichment pipelines

| Pipeline | Script | Docs |
|----------|--------|------|
| Re3Data metadata into `_re3data` | `python scripts/re3data_enrichment.py enrich --dry-run` | [docs/re3data.md](docs/re3data.md) |
| CKAN sites from [ecosystem.ckan.org](https://ecosystem.ckan.org/dataset/ckan-sites-metadata) | `python scripts/sync_ckan_ecosystem.py --dry-run` | [docs/ckan-sync.md](docs/ckan-sync.md) |
| OpenAIRE Graph data sources | `python scripts/extract_openaire_portals.py list-sources --output /tmp/openaire_sources.json` | [docs/openaire-sync.md](docs/openaire-sync.md) |

## Citation

See [CITATION.cff](CITATION.cff) and [DATASHEET.md](DATASHEET.md) (purpose, bias, limitations).

```
dataportals-registry: A global registry of open data portals and catalogs
(Common Data Index, 2026). CC-BY-4.0.
https://github.com/datenoio/dataportals-registry
```

## License and community

- **Code:** MIT
- **Data:** CC BY 4.0
- [SECURITY.md](SECURITY.md) — vulnerability reporting
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — community standards
