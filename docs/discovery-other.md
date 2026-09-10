# Discovering search engines, ML catalogs, API directories, and marketplaces

How to find catalog types that do not have a dedicated high-volume software page: **Data search engine**, **Machine learning catalog**, **API Catalog**, and **Data marketplace**. Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). Overview: [discovery.md](discovery.md). Type rules: [catalog-types.md](catalog-types.md).

These types are uncommon compared with open data, geo, and scientific repositories. Prefer an existing `software.id` when the product matches; otherwise use `custom`. Do not invent a new software ID for a one-off site.

## Data search engines (`search/`)

Sites whose **primary** product is search across other catalogs (aggregators). They score lower on [trust-score.md](trust-score.md).

**Idra** (`idra`) is a shared Open Data Federation Platform — fingerprints live in [discovery-opendata.md](discovery-opendata.md#idra). Typical `catalog_type` is **Data search engine**, not Open data portal.

## OpenAIRE (`openaire`) {#openaire}

EXPLORE is the global Graph UI; CONNECT hosts national and community gateways (`netherlands.openaire.eu`, Canada.EXPLORE, and similar). Docs: [graph.openaire.eu/docs](https://graph.openaire.eu/docs/). Use `software.id: openaire`. Source repositories harvested into the Graph are a separate list: [openaire-sync.md](openaire-sync.md).

**Confirm:** the UI searches the OpenAIRE Graph (publications, datasets, software, organisations). Register EXPLORE once and each distinct **national/community gateway**. Do not add a single research-product landing page.

| Tool | Query |
|------|-------|
| Google | `"OpenAIRE" (Explore OR CONNECT OR "research portal") -site:openaire.eu/about` |
| Google | `site:openaire.eu (Explore OR CONNECT)` |
| Censys | `web.names: "openaire.eu"` |
| FOFA | `domain="openaire.eu"` |

Other aggregators (national dataset search, harvested CKAN unions, commercial catalog search) are usually `software.id: custom`.

**Confirm:** the UI searches or harvests **other** catalogs. If the site hosts its own datasets as the main product, use Open data portal / Geoportal / Scientific instead.

| Tool | Query |
|------|-------|
| Google | `"open data" (search engine OR aggregator OR "dataset search")` plus a country name |
| Google | `"IdraPortal" OR "Open Data Federation"` |

Do not register harvested source catalogs a second time. Duplicate-check each underlying portal `link`.

### Earth, ocean, and facility aggregators

These are **search engines** (or scientific repositories when they host data) whose directories were used as named-list hunts. Duplicate-check each underlying catalog; register the aggregator once if it is missing.

| Source | Typical records |
|--------|-----------------|
| [ODIS catalogue](https://catalogue.odis.org/) | Ocean Data and Information System — 28 origin catalogs in one pass (CKAN, GeoNetwork, ERDDAP, custom) |
| [PANGAEA](https://www.pangaea.de/) harvest sources | Almost all live sources already registered; leftover hosts were org homepages or dead |
| [WMO WIS2 GDC](https://gdc.wis.cma.cn/) | Meteorological node catalogs |
| [EPOS Data Portal](https://www.ics-c.epos-eu.org/) | European plate-observing search |
| [GEO DAB](https://www.geodab.net/) | GEO Discovery and Access Broker |
| [ENVRI-Hub](https://envri-hub.envri.eu/) | Environmental research-infrastructure search |
| [STAC Index](https://stacindex.org/catalogs) | STAC catalog directory (also a search engine if unregistered) |
| [CLARIN VLO](https://vlo.clarin.eu/) | Linguistic data centers — keep endpoints that list datasets |

Do not add GEOSS Portal / GCMD / per-dataset Source Cooperative STAC as extra catalogs when the parent catalog is already registered.

## Machine learning catalogs (`ml/`)

Public catalogs of ML datasets or models (not a single Kaggle notebook, not a model card).

Shared software that sometimes maps here:

| `software.id` | When to use | Hunt notes |
|---------------|-------------|------------|
| `openmlorg` | see above | |
| `huggingface` | Hugging Face Datasets Hub | Site: [huggingface.co/datasets](https://huggingface.co/datasets/). Confirm the datasets catalog. Do not add per-user spaces. |
| `codalab` | CodaLab Competitions hub | Site: [competitions.codalab.org](https://competitions.codalab.org). Confirm the public competitions list. One hub, not per competition. Distinct from `codabench`. |
| `codabench` | Codabench hub | Site: [codabench.org](https://www.codabench.org). Confirm title `Codabench`. One hub, not per benchmark. Distinct from `codalab`. |
| `galaxy` | Public Galaxy with data libraries | See [discovery-scientific.md](discovery-scientific.md). Prefer Scientific unless ML datasets are the primary product. |

Hugging Face, Kaggle, Papers with Code, and similar **global** hubs are usually already in the registry as single catalogs — do not add per-user spaces or per-dataset pages.

## OpenML (`openmlorg`) {#openmlorg}

Open machine-learning dataset/task/flow repository. Hub: [openml.org](https://www.openml.org). Docs: [docs.openml.org](https://docs.openml.org). Catalog type is often Machine learning catalog.

**Signals:** OpenML chrome; `/api/v1/`; public dataset/task UI.

**Confirm:** GET `/api/v1/` or the public dataset list. Most national copies are already registered. One hub (plus independent OpenML instances). Do not add per-dataset pages.

| Tool | Query |
|------|-------|
| Google | `"OpenML" (datasets OR "machine learning") -site:github.com` |
| Censys | `web.names: "openml.org"` |
| FOFA | `domain="openml.org"` |

## CodaLab Competitions (`codalab`) {#codalab}

Open-source ML competition platform. Public hub: [competitions.codalab.org](https://competitions.codalab.org). Source: [github.com/codalab/codalab-competitions](https://github.com/codalab/codalab-competitions). Use `software.id: codalab`. Register the hub once, not per competition. The successor product is Codabench (`codabench`).

**Confirm:** GET the public competitions list. Title includes `CodaLab`.

| Tool | Query |
|------|-------|
| Google | `"CodaLab" competitions datasets -site:github.com` |
| Censys | `web.names: "competitions.codalab.org"` |
| FOFA | `host="competitions.codalab.org"` |

## Codabench (`codabench`) {#codabench}

Open-source successor to CodaLab Competitions. Public hub: [codabench.org](https://www.codabench.org). Source: [github.com/codalab/codabench](https://github.com/codalab/codabench). Use `software.id: codabench`. Register the hub once, not per benchmark. `/api/datasets/` is often `403`; the public HTML catalog is the product.

**Confirm:** GET the home. Title `Codabench`.

| Tool | Query |
|------|-------|
| Google | `"Codabench" (benchmark OR competition OR datasets) -site:github.com` |
| Censys | `web.names: "codabench.org"` |
| FOFA | `domain="codabench.org"` |

Regional challenge platforms (Zindi, AIcrowd, SIGNATE, Grand Challenge, and national Chinese hubs such as Baidu AI Studio, BAAI, OpenXLab) are typically `software.id: custom`. Register **one catalog per hub**, not per competition or dataset.

| Tool | Query |
|------|-------|
| Google | `"OpenML" (datasets OR tasks) -site:openml.org -site:github.com` |
| Google | `"machine learning" ("data catalog" OR "dataset catalog")` plus an institution name |

## API catalogs (`api/`)

Directories of APIs (developer portals that list many APIs with docs and keys), not a CKAN Action API on an open-data site.

There is no high-volume shared `software.id` for this type in `data/software/`. Use `custom` unless a named platform definition already exists. A CKAN/Socrata/OpenDataSoft site stays **Open data portal** even if it has an API.

**Confirm:** a browsable list of APIs is the product. Skip a single REST endpoint with no catalog.

| Tool | Query |
|------|-------|
| Google | `"API catalog" OR "API directory" OR "developer portal" (datasets OR government)` plus a country name |

## Data marketplaces (`marketplace/`)

Commercial markets that sell or license datasets. Access is often `restricted`.

Use `custom` unless the vendor already has a software definition. Do not scrape prices or attempt paid-only listings.

**Confirm:** a public catalog of datasets for sale or licensed reuse. Skip procurement portals and app stores.

| Tool | Query |
|------|-------|
| Google | `"data marketplace" OR "data shop" (datasets OR geospatial)` plus a country name |

## Datasets lists (`other/` with type Datasets list)

Simple pages that list datasets without a full portal CMS (spreadsheet catalogs, HTML tables, GitHub data lists). Usually `software.id: custom`.

**Confirm:** a reusable list of multiple datasets with links or files. Skip a single CSV or a blog post.

| Tool | Query |
|------|-------|
| Google | `"list of datasets" OR "data inventory" (government OR open)` plus a country or city |

## General research repositories

Broad institutional research repos that are not clearly Dataverse/DSpace/Invenio. Prefer a named `software.id` from [discovery-scientific.md](discovery-scientific.md) (including Islandora, Samvera, Haplo, Worktribe). If none match, `custom` and `catalog_type: General research repository` or Scientific data repository per the **primary** UI.

## Custom software (`custom`) {#custom}

About one catalog in eight has no shared product ID. Use `custom` when two independent fingerprints do not match a `data/software/` definition. Hunt with the generic URL patterns in the type guides, not a software name.

**Decision tree**

1. Run the probe table in [discovery.md](discovery.md#identify-the-software) (plus the type guide for the primary UI).
2. If two signals match a named ID, use that ID — do not leave `custom`.
3. If the host is a viewer wrapping GeoServer/QGIS Server, register the **viewer** ([one catalog per public product](discovery.md#one-catalog-per-public-product)).
4. If nothing matches: `custom`, `api: false` unless you found a public list (`data.json`, DCAT, OAI, CSW, STAC).
5. Do not invent a new `software.id` for a one-off. Propose a software YAML only when several independent installations share a product ([software-taxonomy.md](software-taxonomy.md)). Recent custom-geoportal clustering produced SeaSketch, PISO, GDi Visios, MapGuide, EnviMAP, MAP+, Avinet, ISY Map, and SmartMap; leftover custom rows are mostly unique `.gov` roots.

Harvest: [harvest-other.md](harvest-other.md#custom).

## Related

- [discovery.md](discovery.md)
- [discovery.md](discovery.md#hunt-patterns) — session hunt patterns
- [discovery-opendata.md](discovery-opendata.md) (Idra)
- [discovery-scientific.md](discovery-scientific.md) (OpenML, Galaxy)
- [harvest-other.md](harvest-other.md)
- [harvest.md](harvest.md)
- [catalog-types.md](catalog-types.md)
- [software-taxonomy.md](software-taxonomy.md)
