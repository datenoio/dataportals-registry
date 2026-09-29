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
| `kaggle` | Kaggle Datasets hub | Site: [kaggle.com/datasets](https://www.kaggle.com/datasets). Confirm the datasets catalog. One hub, not per notebook. |
| `codalab` | CodaLab Competitions hub | Site: [competitions.codalab.org](https://competitions.codalab.org). Confirm the public competitions list. One hub, not per competition. Distinct from `codabench`. |
| `codabench` | Codabench hub | Site: [codabench.org](https://www.codabench.org). Confirm title `Codabench`. One hub, not per benchmark. Distinct from `codalab`. |
| `grandchallenge` | Grand Challenge hub | Site: [grand-challenge.org](https://grand-challenge.org). Confirm the public challenges/archives UI. One hub, not per challenge. |
| `evalai` | EvalAI hub | Site: [eval.ai](https://eval.ai). Confirm title includes `EvalAI`. One hub, not per challenge. |
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

## Kaggle (`kaggle`) {#kaggle}

Kaggle Datasets hub: [kaggle.com/datasets](https://www.kaggle.com/datasets). Distinct from OpenML (`openmlorg`) and Hugging Face (`huggingface`).

**Signals:** host `kaggle.com/datasets`; Kaggle Datasets chrome.

**Confirm:** GET the public datasets catalog. One hub, not per notebook, competition, or user dataset page.

| Tool | Query |
|------|-------|
| Google | `site:kaggle.com/datasets` |
| Censys | `web.names: "kaggle.com"` |
| FOFA | `host="kaggle.com"` |

## CodaLab Competitions (`codalab`) {#codalab}

Open-source ML competition platform. Public hub: [competitions.codalab.org](https://competitions.codalab.org). Source: [github.com/codalab/codalab-competitions](https://github.com/codalab/codalab-competitions). Use `software.id: codalab`. Register the hub once, not per competition. The successor product is Codabench (`codabench`).

**Confirm:** GET the public competitions list. Title includes `CodaLab`.

[base.html](https://github.com/codalab/codalab-competitions/blob/develop/codalab/apps/web/templates/base.html) titles every page `CodaLab - …` (1,027 hosts in September 2026, including `competitions.codalab.org` and `141.5.101.228` titled CodaLab - Home). Keep the host query for the canonical hub.

| Tool | Query |
|------|-------|
| Google | `"CodaLab" competitions datasets -site:github.com` |
| Censys | `web.endpoints.http.body: "<title>CodaLab -"` |
| FOFA | `body="<title>CodaLab -"` |
| Censys | `web.names: "competitions.codalab.org"` |
| FOFA | `host="competitions.codalab.org"` |

## Codabench (`codabench`) {#codabench}

Open-source successor to CodaLab Competitions. Public hub: [codabench.org](https://www.codabench.org). Source: [github.com/codalab/codabench](https://github.com/codalab/codabench). Use `software.id: codabench`. Register the hub once, not per benchmark. `/api/datasets/` is often `403`; the public HTML catalog is the product.

**Confirm:** GET the home. Title `Codabench`.

[base.html](https://github.com/codalab/codabench/blob/develop/src/templates/base.html) sets the default title `Codabench` (26 hosts in September 2026, including `www.codabench.org` and `qtim-challenges.southcentralus.cloudapp.azure.com`). Keep the domain query for the canonical hub.

| Tool | Query |
|------|-------|
| Google | `"Codabench" (benchmark OR competition OR datasets) -site:github.com` |
| Censys | `web.endpoints.http.html_title: "Codabench"` |
| FOFA | `title="Codabench"` |
| Censys | `web.names: "codabench.org"` |
| FOFA | `domain="codabench.org"` |

## Grand Challenge (`grandchallenge`) {#grandchallenge}

Apache-2.0 biomedical-imaging challenge platform. Public hub: [grand-challenge.org](https://grand-challenge.org). Source: [DIAGNijmegen/rse-grand-challenge](https://github.com/DIAGNijmegen/rse-grand-challenge) (the `comic/grand-challenge.org` repository redirects here). Register **one catalog per installation**, not each challenge, archive, algorithm, or track subdomain. Bot walls on `/api/v1/` are common — use the HTML catalog.

**Confirm:** GET the homepage and `/challenges/` or `/data/`. Keep the install when those pages list challenges or datasets. Drop empty clones, test hosts, and hosts that no longer resolve. Track subdomains of one install (`frame.example.org`, `procedure.example.org`) are the same catalog.

[script.html](https://github.com/DIAGNijmegen/rse-grand-challenge/blob/main/app/grandchallenge/core/templates/grandchallenge/partials/script.html) serves `js/datatables.defaults.mjs`. The footer links `github.com/DIAGNijmegen/rse-grand-challenge/`; older installs still link `github.com/comic/grand-challenge.org`. `<h6>Grand Challenge</h6>` matches challenge subdomains of the public hub (445 hosts in September 2026) and **zero** independent installs (24 September 2026). `body="Grand Challenge"` matched 6,183 unrelated hosts.

GitHub code search skips forks. Fork homepages of `DIAGNijmegen/rse-grand-challenge` still say `https://grand-challenge.org`. Code search `datatables.defaults.mjs` and `public.ecr.aws/diag-nijmegen/grand-challenge` hit the upstream repo and [NBISweden/gc-bp-helm](https://github.com/NBISweden/gc-bp-helm) (`domainName: storprovning.test`, not a public catalog).

| Tool | Query |
|------|-------|
| GitHub | forks of `DIAGNijmegen/rse-grand-challenge`; code search `datatables.defaults.mjs` and `public.ecr.aws/diag-nijmegen/grand-challenge` |
| Google | `"grand-challenge.org" (challenge OR archive OR algorithm) biomedical` |
| FOFA | `body="js/datatables.defaults.mjs" && domain!="grand-challenge.org"` |
| FOFA | `body="github.com/DIAGNijmegen/rse-grand-challenge/" && domain!="grand-challenge.org"` |
| FOFA | `body="github.com/comic/grand-challenge.org" && domain!="grand-challenge.org"` |
| Censys | `web.endpoints.http.body: "js/datatables.defaults.mjs" and not web.hostname: "grand-challenge.org"` |
| FOFA | `host="grand-challenge.org"` |

On 24 September 2026 the independent `datatables.defaults.mjs` query returned `orena-focus-challenge.org` (public HeiCo-FOCUS VQA and LapChole-FOCUS VQA datasets), `zodiac-observatory.org` and `test-zodiac-observatory.org` (HTTP 403), and `fraunhofer-mevis-showroom.de` (DNS dead). The older comic footer also returned `vlm3dchallenge.com` task hosts (DNS dead).

## EvalAI (`evalai`) {#evalai}

BSD-licensed AI challenge evaluation platform. Public hub: [eval.ai](https://eval.ai). Source: [Cloud-CV/EvalAI](https://github.com/Cloud-CV/EvalAI). Docker Compose installs are documented. Register the hub once, not each challenge or leaderboard.

**Confirm:** GET `https://eval.ai`. Page title binds `EvalAI`. One catalog for that hub.

[base.html](https://github.com/Cloud-CV/EvalAI/blob/master/frontend/base.html) sets `ng-app="evalai"` (50 hosts in September 2026, including `competition.aiforgood.itu.int` and `labs.scientechresearch.io`) and the meta description `EvalAI is an open-source web platform` (40 hosts, including `health.aiaudit.org`). Keep the host query for the canonical hub.

| Tool | Query |
|------|-------|
| Google | `"EvalAI" (challenge OR evaluation OR leaderboard) -site:github.com` |
| Censys | `web.endpoints.http.body: "ng-app=\"evalai\""` |
| FOFA | `body="ng-app=\"evalai\""` |
| Censys | `web.endpoints.http.body: "EvalAI is an open-source web platform"` |
| FOFA | `body="EvalAI is an open-source web platform"` |
| Censys | `web.names: "eval.ai"` |
| FOFA | `host="eval.ai"` |

Regional challenge platforms (Zindi, AIcrowd, SIGNATE, and national Chinese hubs such as Baidu AI Studio, BAAI, OpenXLab) are typically `software.id: custom`. Register **one catalog per hub**, not per competition or dataset.

| Tool | Query |
|------|-------|
| Google | `"OpenML" (datasets OR tasks) -site:openml.org -site:github.com` |
| Google | `"machine learning" ("data catalog" OR "dataset catalog")` plus an institution name |

## API catalogs (`api/`)

Directories of APIs (developer portals that list many APIs with docs and keys), not a CKAN Action API on an open-data site.

Use a named platform when the portal matches it. A CKAN, Socrata, or OpenDataSoft site stays **Open data portal** even if it has an API, except a CKAN site whose product is the API directory itself (Suomi.fi Liityntäkatalogi is `ckan` with `catalog_type: API Catalog`).

**Confirm:** a browsable list of APIs is the product. Skip a single REST endpoint with no catalog.

| Tool | Query |
|------|-------|
| Google | `"API catalog" OR "API directory" OR "developer portal" (datasets OR government)` plus a country name |

## Azure API Management (`azureapim`) {#azureapim}

Microsoft Azure API Management developer portal. Docs: [developer portal](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-developer-portal). `catalog_type` is **API Catalog**.

**Confirm:** the HTML title contains `Microsoft Azure API Management - developer portal`. Hosts may be a custom domain or `*.developer.azure-api.net`. Register each public developer portal. Do not add each API operation as its own catalog.

| Tool | Query |
|------|-------|
| Google | `"Microsoft Azure API Management - developer portal"` |
| Censys | `web.endpoints.http.title: "Microsoft Azure API Management - developer portal"` |
| FOFA | `title="Microsoft Azure API Management - developer portal"` |

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

## Squarespace (`squarespace`) {#squarespace}

Squarespace hosted website builder; small research groups and foundations publish data and indicator pages as Squarespace sites (Kentucky Health Facts, Freedom on the Move, SAIS CARI Data).

**Signals:** `Server: Squarespace` response header; `static1.squarespace.com` assets; `end of squarespace headers` HTML comment.

**Confirm:** GET the data page and match the header or asset host. One record per site. Do not tag Squarespace marketing pages with no data content.

| Tool | Query |
|------|-------|
| Censys | `web.endpoints.http.headers: "Squarespace"` |
| FOFA | `server="Squarespace" && body="data"` |
| FOFA | `body="static1.squarespace.com" && body="dataset"` |

## Jekyll (`jekyll`) {#jekyll}

Jekyll static site generator, often on GitHub Pages; research projects publish dataset catalogs as Jekyll sites (Open Graph Benchmark, Therapeutics Data Commons, Gene Ontology, BridgeDb). Source: [github.com/jekyll/jekyll](https://github.com/jekyll/jekyll).

**Signals:** `begin jekyll seo tag` / `end jekyll seo tag` HTML comments; generator meta `Jekyll vX.Y.Z`.

**Confirm:** GET the catalog page and match the comments or generator meta. One record per project site. Do not tag custom repository applications that only keep a Jekyll docs frame (for example a Chaise/PhysioNet app behind a Jekyll home).

| Tool | Query |
|------|-------|
| Google | `"jekyll seo tag" (datasets OR "data catalog")` |
| Censys | `web.endpoints.http.body: "jekyll seo tag"` |
| FOFA | `body="jekyll seo tag" && body="dataset"` |

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
