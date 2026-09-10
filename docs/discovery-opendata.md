# Discovering open data portals

How to find **open data portal** installations (`catalog_type: Open data portal`) that are not yet in this registry. Search-engine syntax (Google, Censys, Shodan, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). Overview and accept/reject rules: [discovery.md](discovery.md). Also covered here: Idra (`idra`), a DCAT-AP federation layer that is usually typed as a **Data search engine**; Piveau, Our Open Data, Gipuzkoa Irekia, DataPress, Taiwan MODA, ResourceContracts, RDF Online Repository, the Guangxi Public Data Open Platform, ODWeb, ATM Maggioli, and OpenGov.

Set `software.id` from `data/software/` only when a probe or page signal matches. Otherwise `custom`. After YAML exists: `python scripts/apidetect.py detect-single {id} --dryrun` (replace `{id}` with the catalog id).

## CKAN (`ckan`) {#ckan}

Most common self-hosted open-data CMS. Gallery: [CKAN ecosystem](https://ecosystem.ckan.org/dataset/ckan-sites-metadata) (automated: `python scripts/sync_ckan_ecosystem.py --dry-run`) and [Datashades](https://datashades.info/).

**Signals:** footer “Powered by CKAN”; `/dataset` or `/dataset/` listing; HTML includes `ckan.js` or `ckanext-`; cookie `ckan_`.

**Confirm (GET):** `https://host/api/3/action/status_show` and/or `/api/3/action/package_list`. JSON with `"success": true` is enough. Scientific data repositories may also be `ckan` when that API matches (AuScope Data Repository, `generator` CKAN 2.10.1; Observatorio Medioambiental La Plata, `generator` CKAN 2.7.3). HTML that mentions “ckan” is not enough when `status_show` returns HTML or 503 (INAIL `dati.inail.it`). An `og:url` pointing at a CKAN test host is not enough when `status_show` 404s (NIRD `archive.sigma2.no`).

| Tool | Query |
|------|-------|
| Google | `"Powered by CKAN" inurl:/dataset -site:github.com -site:ckan.org` |
| Google | `inurl:/api/3/action/status_show` |
| Google | `"CKAN" "open data" site:.gov` |
| Censys (web) | `web.endpoints.http.body: "Powered by CKAN"` |
| FOFA | `body="Powered by CKAN"` |
| Censys (web) | `web.endpoints.http.html_title: "CKAN"` |
| FOFA | `title="CKAN" && country="PT"` |
| Shodan | `http.html:"Powered by CKAN"` |
| PublicWWW | `"Powered by CKAN"` or `"ckan.js"` |

**False positives:** ckan.org, docs, GitHub, demo.ckan.org, CKAN extensions that are not a portal, harvest *sources* listed inside another CKAN. Prefer the catalog homepage, not `/dataset/{slug}`.

**Paths:** `/dataset`, `/organization`, `/api/3`, `/data.json`, `/catalog.xml`. Some installs live under `/data` or `/opendata` — probe `https://host/data/api/3/action/status_show` as well.

## DKAN (`dkan`) {#dkan}

Drupal-based portal with a CKAN-compatible Action API plus DKAN’s own `/api/1/` routes. Community: [getdkan.org/community](https://getdkan.org/community).

**Confirm:** CKAN-style `/api/3/action/package_search` **and** `/api/1/search` or `/api/1/metastore`. Often `/data.json` (DCAT-US).

| Tool | Query |
|------|-------|
| Google | `"powered by DKAN" OR inurl:/api/1/metastore` |
| Google | `"DKAN" "open data" site:.gov` |
| Censys | `web.endpoints.http.body: "DKAN"` |
| FOFA | `body="DKAN"` |
| Shodan | `http.html:"dkan"` |

Do not label a site `dkan` from the CKAN API alone — that is usually `ckan`.

## OpenDataSoft (`opendatasoft`) {#opendatasoft}

SaaS and self-hosted Explore portals. Many hosts end in `*.opendatasoft.com` or use a custom domain with `/explore`.

**Confirm:** `https://host/api/explore/v2.1/catalog/datasets` (or legacy `/api/v2/catalog/datasets/`). UI path `/explore`.

| Tool | Query |
|------|-------|
| Google | `inurl:/explore "opendatasoft" -site:opendatasoft.com/blog` |
| Google | `site:opendatasoft.com/explore` |
| Google | `"Powered by OpenDataSoft" OR "ods-explore"` |
| Censys | `web.names: "opendatasoft.com"` |
| FOFA | `domain="opendatasoft.com"` |
| Censys | `web.endpoints.http.body: "OpenDataSoft"` |
| FOFA | `body="OpenDataSoft"` |
| FOFA | `body="OpenDataSoft" && country="BE"` |
| crt.sh | `%.opendatasoft.com` |

**False positives:** the vendor homepage, academy, and blog. Register the **portal** (`{org}.opendatasoft.com` or the city’s custom domain), not `www.opendatasoft.com`. List: [Open Data Inception](https://data.opendatasoft.com/explore/dataset/open-data-sources%40public/information/).

## Socrata (`socrata`) {#socrata}

Tyler / Socrata Open Data. UI often `/browse` or `/datasets`. SODA API under `/api/views`. Network: [opendatanetwork.com](https://www.opendatanetwork.com/search?q=).

**Confirm:** `https://host/api/views.json?limit=1` or `/api/views`. Many sites also serve `/data.json`. Headers may include `X-Socrata-*`.

| Tool | Query |
|------|-------|
| Google | `inurl:/browse "socrata" OR "open data network"` |
| Google | `"Powered by Socrata" OR inurl:/api/views` |
| Google | `site:*.socrata.com` (custom domains are more interesting) |
| Censys | `web.endpoints.http.body: "socrata"` |
| FOFA | `header="X-Socrata"` |
| Shodan | `http.html:"X-Socrata" OR http.html:"soda.demo"` |

Skip `soda.demo.socrata.com` and Tyler marketing sites. Prefer the city’s production domain.

## uData (`udata`) {#udata}

French-origin portal (data.gouv.fr lineage). Dataset UI `/datasets/`. API `/api/1/datasets/`.

**Confirm:** `https://host/api/1/datasets/?page_size=1` returns JSON with `data` / `total`.

| Tool | Query |
|------|-------|
| Google | `"opendata" inurl:/datasets site:.gouv.fr` |
| Google | `"udata" "jeux de données" OR inurl:/api/1/datasets` |
| Censys | `web.endpoints.http.body: "udata"` |
| FOFA | `body="udata"` |
| Censys | `web.names: "data.gouv"` |
| FOFA | `domain="data.gouv"` |

Local clones exist outside France. Do not assume every `/api/1/datasets` is uData — check the JSON shape.

## Magda (`magda`) {#magda}

Search-centric catalog (data.gov.au and derivatives). API `/api/v0/search/datasets` or `/search/api/v0/search/datasets`.

**Confirm:** that search endpoint returns JSON datasets. UI often `/search` or `/dataset`.

| Tool | Query |
|------|-------|
| Google | `"magda" "data catalog" OR inurl:/api/v0/search/datasets` |
| Google | `inurl:/search/api/v0/search/datasets` |
| Censys | `web.endpoints.http.body: "magda"` |
| FOFA | `body="magda"` |

## JKAN (`jkan`) {#jkan}

Jekyll + CKAN-like static portal. Often GitHub Pages. Datasets as Markdown in `/datasets`.

**Confirm:** HTML “JKAN” / `_config.yml` mentions; dataset list at `/datasets/`. No CKAN Action API.

| Tool | Query |
|------|-------|
| Google | `"JKAN" "open data" OR "jkan" inurl:/datasets` |
| Google | `site:github.io "JKAN"` |
| Censys | `web.endpoints.http.body: "JKAN"` |
| FOFA | `body="JKAN"` |

Skip the [jkan.io](https://jkan.io) project site unless it is a real catalog instance.

## Junar (`junar`) {#junar}

SaaS open-data CMS used in Latin America. Customer list: [junar.com/customers](https://junar.com/customers/). Often `/data.json`.

| Tool | Query |
|------|-------|
| Google | `"powered by Junar" OR "junar" "datos abiertos"` |
| Censys | `web.endpoints.http.body: "Junar"` |
| FOFA | `body="Junar"` |

## EntryScape (`entryscape`) {#entryscape}

DCAT-AP catalogs, especially Sweden and Nordics. Customers: [entryscape.com/en/customers](https://entryscape.com/en/customers/). UI may be Blocks/Catalog; API under `/store/`.

| Tool | Query |
|------|-------|
| Google | `"EntryScape" (catalog OR "öppna data" OR dcat)` |
| Google | `inurl:/store "entryscape"` |
| Censys | `web.endpoints.http.body: "EntryScape"` |
| FOFA | `body="EntryScape"` |

## ArcGIS Hub as an open-data site (`arcgishub`) {#arcgishub}

Many Hub sites are **open data** first (dataset search, DCAT) rather than a map viewer. If the primary UI is a dataset catalog, use `catalog_type: Open data portal` and `software.id: arcgishub`. If it is a GIS hub / map gallery, use **Geoportal** — see [discovery-geoportals-sdi.md](discovery-geoportals-sdi.md#arcgishub).

**Confirm:** `/api/search/v1` or `/api/feed/dcat-us/1.1.json`. Hosts often `*.hub.arcgis.com` or `opendata.arcgis.com`. Custom-domain example: Bloemendaal (`hubcdn.arcgis.com/opendata-ui`).

| Tool | Query |
|------|-------|
| Google | `site:hub.arcgis.com "open data"` |
| Google | `site:opendata.arcgis.com` |
| Google | `inurl:hub.arcgis.com` |
| Censys | `web.names: "hub.arcgis.com"` |
| FOFA | `host="hub.arcgis.com"` |
| FOFA | `body="opendata-ui"` |
| crt.sh | `%.hub.arcgis.com` |

Gallery: [hub.arcgis.com](https://hub.arcgis.com/).


## Idra (`idra`) {#idra}

Open Data Federation Platform (FIWARE / Engineering Ingegneria Informatica). It harvests CKAN, DKAN, Socrata, OpenDataSoft, NGSI, and DCAT-AP sources into one search UI. Docs: [idra.readthedocs.io](https://idra.readthedocs.io). Source: [OPSILab/Idra](https://github.com/OPSILab/Idra).

Typical `catalog_type` is **Data search engine** (folder `search/`), not Open data portal: Idra is an aggregator over other ODMS catalogues.

**Signals:** path `/IdraPortal/`; REST under `/Idra/api/v1/`; SPARQL; DCAT-AP / DCAT-AP_IT branding.

**Confirm:** GET `https://host/IdraPortal/` (or `/Idra/api/v1/` JSON). Prefer a live production federation. The public demos (`idra.site`, `idra.opsilab.it`, `idra.eng.it`, sandbox hosts) are already registered and mostly **inactive** — do not re-add them.

| Tool | Query |
|------|-------|
| Google | `"Idra" ("Open Data Federation" OR IdraPortal OR "DCAT-AP_IT") -site:github.com -site:readthedocs.io` |
| Google | `inurl:/IdraPortal/ OR inurl:/Idra/api/v1/` |
| Censys | `web.endpoints.http.body: "IdraPortal"` |
| FOFA | `body="IdraPortal"` |
| Censys | `web.endpoints.http.body: "Idra"` |
| FOFA | `body="Idra"` |

Do not register harvested source catalogs a second time as Idra. Duplicate-check the underlying CKAN/Socrata/OpenDataSoft `link` as well.

## Liferay (`liferay`) {#liferay}

Digital experience CMS. **Only** register when a public Open Data / RISP dataset listing exists (common on Spanish provincial sites), not a generic Liferay intranet.

**Signals:** Liferay portal paths (`/web/guest/`); “datos abiertos” / RISP module; Excel/XML/JSON/CSV dataset tables.

**Confirm:** GET the open-data page and verify a reusable dataset list. Skip city hall homepages that only mention open data in a news article.

| Tool | Query |
|------|-------|
| Google | `"datos abiertos" Liferay OR RISP (ayuntamiento OR diputación) site:.es` |
| Google | `inurl:/web/guest/ "datos abiertos"` |
| Censys | `web.endpoints.http.body: "Liferay"` |
| FOFA | `body="Liferay"` |

## ATM Maggioli (`atmmaggioli`) {#atmmaggioli}

Spanish municipal sede electrónica / Portal de Transparencia with an open-data catalog (ATM Grupo Maggioli / Galileo IyS). Common on Canary Islands `eadmin.*` and `sede.*` tenants. Product: [administración electrónica](https://www.atm-maggioli.es/software-y-consultoria/administracion-electronica/).

**Signals:** path `/transparencia/datos/catalogo`; Maggioli / Galileo IyS / ATM branding; title “Sede Electrónica”; dataset list under transparencia.

**Confirm:** GET `https://host/transparencia/datos/catalogo` and match a reusable dataset listing. One record per municipality tenant. Do **not** set `ckan`, `opendatasoft`, or `socrata` from guessed `/api/3`, `/api/v2/catalog`, or `/api/views` paths — those URLs return the HTML shell. Do **not** set `atmmaggioli` on Italian Municipium / Maggioli “Portale Opendata” shells (`municipiumapp.it` civic CMS); that is a different product and has no dedicated software id.

| Tool | Query |
|------|-------|
| Google | `inurl:/transparencia/datos/catalogo (Maggioli OR Galileo OR "sede electrónica")` |
| Google | `"grupo ATM-Maggioli" OR "ATM Maggioli" ("datos abiertos" OR catálogo)` |
| Censys | `web.endpoints.http.body: "Maggioli"` |
| FOFA | `body="Maggioli"` |

Skip the vendor homepage and Galileo demo sede. Prefer the municipal catalog path, not the whole e-office.

## OpenGov (`opengov`) {#opengov}

Tyler / OpenGov financial transparency SaaS for US cities and states. Public tenants are `{org}.opengov.com` with `/transparency` and `/data` report views.

**Signals:** hostname `*.opengov.com`; path `/transparency` or `/data/`; Highcharts budget explorer; “Transparency Home”.

**Confirm:** GET the tenant home or `/transparency` and match OpenGov report navigation. One record per government tenant. Do **not** set `opengov` from the word “OpenGov” on ArcGIS Hub, `wyopen.gov`, `opengov.brandon.ca`, or other checkbooks that are not `*.opengov.com`.

| Tool | Query |
|------|-------|
| Google | `site:opengov.com/transparency (budget OR financial)` |
| Google | `inurl:.opengov.com/data` |
| Censys | `web.names: "opengov.com"` |
| FOFA | `domain="opengov.com"` |

Skip `www.opengov.com` marketing. Do not bulk-add every guessed city subdomain.

## POMOSAM (`pomosam`) {#pomosam}

CORA GEO municipal eGovernment / open-data publisher used by Slovak cities (contracts, invoices, orders, public datasets). Vendor: [pomosam.sk](http://www.pomosam.sk).

**Signals:** POMOSAM / CG eGOV branding; municipal zverejňovanie / open-data modules.

**Confirm:** GET the public dataset or disclosure catalog. One record per municipality tenant.

| Tool | Query |
|------|-------|
| Google | `"POMOSAM" OR "CG eGOV" (otvorené OR zverejňovanie) site:.sk` |
| Censys | `web.endpoints.http.body: "POMOSAM"` |
| FOFA | `body="POMOSAM"` |

## oPortal (`oportal`) {#oportal}

Inspur Chinese government open-data product. Deployments share `/oportal/` catalogs, a developer center, and an application gallery.

**Signals:** path `/oportal/`; 浪潮 / Inspur; data-service / API gallery pages.

**Confirm:** GET `/oportal/` (or the documented catalog path) and match a dataset listing. One record per government tenant.

| Tool | Query |
|------|-------|
| Google | `inurl:/oportal/ (数据 OR 开放)` |
| Google | `"浪潮" 开放数据 oportal` |
| Censys | `web.endpoints.http.body: "/oportal/"` |
| FOFA | `body="/oportal/"` |

## OGD Platform India (`ogdindia`) {#ogdindia}

NIC SaaS on data.gov.in for ministries and states. Site: [data.gov.in](https://data.gov.in).

**Signals:** `data.gov.in` tenant host or path; OGD Platform India; CKAN-like catalog UI on NIC hosting.

**Confirm:** GET the ministry/state catalog home. Do not re-add the national portal if it is already registered; add only distinct tenant catalogs.

| Tool | Query |
|------|-------|
| Google | `site:data.gov.in (catalog OR dataset)` |
| Google | `"OGD Platform" OR "Open Government Data" site:.gov.in` |
| crt.sh | `%.data.gov.in` |
| Censys | `web.names: "data.gov.in"` |
| FOFA | `host="data.gov.in"` |

## data eye (`dataeye`) {#dataeye}

Japanese municipal open-data SaaS (Data Cradle). Site: [dataeye.jp](https://dataeye.jp). Some tenants expose a CKAN-compatible metadata API.

**Confirm:** GET the prefecture/city catalog. One record per tenant (including joint prefecture-municipality group portals).

| Tool | Query |
|------|-------|
| Google | `site:dataeye.jp` |
| Google | `"data eye" オープンデータ (市 OR 県)` |
| crt.sh | `%.dataeye.jp` |
| Censys | `web.names: "dataeye.jp"` |
| FOFA | `domain="dataeye.jp"` |

## Seoul Open Data Plaza (`seoulopendataplaza`) {#seoulopendataplaza}

Shared catalog used by Seoul Metropolitan Government district (`gu`) portals. Titles of the form 열린 데이터 광장; `/openinf/` JSP pages.

**Confirm:** GET the district plaza home. One record per `gu` tenant, plus the city portal if it is a distinct catalog.

| Tool | Query |
|------|-------|
| Google | `"열린 데이터 광장" site:.go.kr` |
| Google | `inurl:/openinf/ seoul` |
| Censys | `web.endpoints.http.body: "openinf"` |
| FOFA | `body="openinf"` |

## Data Fair (`datafair`) {#datafair}

Koumoul open-source data portals. Docs: [data-fair.github.io](https://data-fair.github.io/3/en/).

**Signals:** Data Fair / Koumoul; `/data-fair/` or dataset explorer APIs.

**Confirm:** GET the public portal and a dataset list API. Skip the vendor docs site.

| Tool | Query |
|------|-------|
| Google | `"Data Fair" (Koumoul OR datasets) -site:github.com` |
| Censys | `web.endpoints.http.body: "data-fair"` |
| FOFA | `body="data-fair"` |

## Datawheel (`datawheel`) {#datawheel}

Datawheel-hosted open-data / economic-complexity portals. Site: [datawheel.us](https://datawheel.us).

**Confirm:** GET the public data portal (not a marketing page). One record per government or international-organization catalog.

| Tool | Query |
|------|-------|
| Google | `"Datawheel" (open data OR "data portal") -site:datawheel.us` |
| Censys | `web.endpoints.http.body: "datawheel"` |
| FOFA | `body="datawheel"` |

## SEU-e (`seue`) {#seue}

Consorci AOC electronic office / transparency / open-data service for Catalan administrations. Hosts under `seu-e.cat`.

**Confirm:** GET the municipality’s open-data or transparency dataset listing on `seu-e.cat`. One record per public-administration tenant that publishes datasets.

| Tool | Query |
|------|-------|
| Google | `site:seu-e.cat (dades OR datasets OR "dades obertes")` |
| crt.sh | `%.seu-e.cat` |
| Censys | `web.names: "seu-e.cat"` |
| FOFA | `domain="seu-e.cat"` |

## TriplyDB (`triplydb`) {#triplydb}

Linked-data / knowledge-graph publishing with SPARQL. Site: [triplydb.com](https://triplydb.com).

**Confirm:** GET the public dataset catalog or SPARQL UI. One record per public instance, not per named graph.

| Tool | Query |
|------|-------|
| Google | `site:triplydb.com` |
| Google | `"TriplyDB" (SPARQL OR datasets) -site:triplydb.com` |
| crt.sh | `%.triplydb.com` |
| Censys | `web.names: "triplydb.com"` |
| FOFA | `domain="triplydb.com"` |

## Drupal (`drupal`) {#drupal}

Use `drupal` only when the **public product is a dataset catalog** (open-data nodes, JSON:API dataset bundle). Do not register ordinary CMS homepages. If the site is DKAN, use `dkan`. Dutch municipal OpenGDC tenants (`/openapi.json` + `/api/datasets`) use [`opengdc`](#opengdc), not `drupal`.

**Confirm:** `/jsonapi/node/dataset` (or the site’s dataset bundle) or a public `data.json`.

| Tool | Query |
|------|-------|
| Google | `"powered by Drupal" ("open data" OR datasets) inurl:/data` |
| Censys | `web.endpoints.http.body: "/jsonapi/node/dataset"` |
| FOFA | `body="/jsonapi/node/dataset"` |

## WordPress (`wordpress`) {#wordpress}

Use `wordpress` only for a **datasets** custom post type or CKAN-theme WP catalog. Ordinary WordPress homepages are out of scope.

| Tool | Query |
|------|-------|
| Google | `"open data" WordPress (CKAN OR dataset) -site:wordpress.org` |
| Censys | `web.endpoints.http.body: "wp-content"` |
| FOFA | `body="wp-content" && body="open data" && body="dataset"` |

## Piveau (`piveau`) {#piveau}

DCAT-AP microservice catalog (Fraunhofer FOKUS). Site: [piveau.de](https://www.piveau.de). Powers several European public-sector portals (including patterns used by data.europa.eu).

**Signals:** Piveau / DCAT-AP; Sparql or Hub-UI; `piveau` in HTML or API paths.

**Confirm:** GET the public catalog and a DCAT/search API. Do not re-add data.europa.eu if it is already registered.

| Tool | Query |
|------|-------|
| Google | `"Piveau" (DCAT-AP OR "open data") -site:github.com -site:piveau.de` |
| Censys | `web.endpoints.http.body: "piveau"` |
| FOFA | `body="piveau"` |

## LKOD (`lkod`) {#lkod}

Czech local DCAT-AP-CZ catalogs (Golemio / Operátor ICT). Harvests into NKOD. Site: [lkod.cz](https://lkod.cz). Slovak municipal clones use `/opendata/set/lkod` (DCAT-AP-SK TTL) on city `opendata.*` hosts — still `lkod`, not POMOSAM.

**Confirm:** GET the municipal/local catalog (Next.js LKOD UI or `/opendata/set/lkod`), not the national NKOD/data.slovensko.sk record twice.

| Tool | Query |
|------|-------|
| Google | `"LKOD" OR "lokální katalog otevřených dat" site:.cz` |
| Google | `inurl:/opendata/set/lkod site:.sk` |
| Censys | `web.endpoints.http.body: "lkod"` |
| FOFA | `body="lkod"` |

## Aleph (`aleph`) {#aleph}

OCCRP investigative document/dataset search. Site: [aleph.occrp.org](https://aleph.occrp.org). Often `catalog_type: Data search engine` or Open data portal depending on whether it hosts datasets or searches collections.

**Confirm:** GET a public Aleph instance. Skip login-only investigations.

| Tool | Query |
|------|-------|
| Google | `"Aleph" OCCRP (datasets OR documents) -site:occrp.org` |
| Censys | `web.endpoints.http.body: "aleph"` |
| FOFA | `body="aleph"` |

## Our Open Data (`ouropendata`) {#ouropendata}

Japanese prefecture/city open-data CMS (Tokushima, Kagawa, Aomori, and others). This is the SHIRASAGI (シラサギ) catalog UI. Shared assets: `/assets/cms/public.css`, numeric `/dataset/` HTML pages, plus an application market and idea box. API: `/api/package_list` (not CKAN `/api/3/action/status_show`).

**Confirm:** GET the catalog home (not a single dataset HTML page). Distinct from CKAN and data.go.jp. Do not add a separate `shirasagi` software id.

| Tool | Query |
|------|-------|
| Google | `"Our Open Data" オープンデータ OR inurl:/assets/cms/public.css` |
| Censys | `web.endpoints.http.body: "assets/cms/public.css"` |
| FOFA | `body="assets/cms/public.css"` |

## Gipuzkoa Irekia (`gipuzkoairekia`) {#gipuzkoairekia}

Shared open-government / open-data platform for Gipuzkoa municipalities. Hub: [gipuzkoairekia.eus](https://www.gipuzkoairekia.eus).

**Confirm:** GET a **tenant** catalog (municipality or foral entity), not only the provincial hub if that hub is already registered. DCAT feeds are a plus.

| Tool | Query |
|------|-------|
| Google | `site:gipuzkoairekia.eus (datos OR datuak OR catalog)` |
| Google | `"Gipuzkoa Irekia" (opendata OR "datos abiertos")` |
| Censys | `web.names: "gipuzkoairekia.eus"` |
| FOFA | `domain="gipuzkoairekia.eus"` |

## DataPress (`datapress`) {#datapress}

Managed CKAN plus CMS. Site: [datapress.com](https://datapress.com). Prefer `datapress` when the public product is branded DataPress; otherwise `ckan` if only the CKAN API is visible.

**Confirm:** CKAN `status_show` **and** DataPress chrome (or vendor docs naming DataPress). Do not double-register the same host as both `ckan` and `datapress`.

| Tool | Query |
|------|-------|
| Google | `"DataPress" ("open data" OR CKAN)` |
| Censys | `web.endpoints.http.body: "datapress"` |
| FOFA | `body="datapress"` |

## MODA Open Data Platform (`modaopendata`) {#modaopendata}

Taiwan Nuxt/Vue open-data frontend (national data.gov.tw family plus local clones). Source: moda-gov-tw/opendata-frontend.

**Confirm:** GET a **tenant** catalog (city/ministry), not a duplicate of the national hub if that hub is already registered. Shared `_nuxt` stack plus catalog API.

| Tool | Query |
|------|-------|
| Google | `"data.gov.tw" OR inurl:_nuxt (opendata OR 開放資料) site:.tw` |
| Google | `"moda-gov-tw" opendata` |
| Censys | `web.names: "data.gov.tw"` |
| FOFA | `host="data.gov.tw"` |

## RDF Online Repository (`rdfrepository`) {#rdfrepository}

Revenue Development Foundation license-transparency portals. Docs: [Online Repository](https://revenuedevelopment.org/online-repository/). Tenants: `*.revenuedev.org`. Distinct from W3C RDF.

**Signals:** host `*.revenuedev.org`; title Repository; RDF/MCAS branding.

**Confirm:** GET the country tenant home. One record per country portal, not the vendor site.

| Tool | Query |
|------|-------|
| Google | `site:revenuedev.org` |
| Google | `"Online Repository" ("Revenue Development" OR mining) -site:revenuedevelopment.org` |
| Censys | `web.names: "revenuedev.org"` |
| FOFA | `domain="revenuedev.org"` |
| crt.sh | `%.revenuedev.org` |

## ResourceContracts (`resourcecontracts`) {#resourcecontracts}

NRGI oil/gas/mining contract repository. Hub: [resourcecontracts.org](https://resourcecontracts.org). Source: [NRGI/resourcecontracts.org](https://github.com/NRGI/resourcecontracts.org).

**Signals:** ResourceContracts chrome; country hosts `{country}.resourcecontracts.org`.

**Confirm:** GET the public contract search (hub or country tenant). One record per public catalog, not per contract PDF.

| Tool | Query |
|------|-------|
| Google | `site:resourcecontracts.org` |
| Google | `"ResourceContracts" (mining OR petroleum) contract` |
| Censys | `web.names: "resourcecontracts.org"` |
| FOFA | `domain="resourcecontracts.org"` |
| crt.sh | `%.resourcecontracts.org` |

## OpenSpending (`openspending`) {#openspending}

Open Knowledge Foundation public-finance catalog. Hub: [openspending.org](https://openspending.org). Fiscal Data Packages with a public search UI and API.

**Confirm:** GET the public dataset search. One record for the hub (and any independent OpenSpending deployment). Skip individual budget visualizations as catalogs.

| Tool | Query |
|------|-------|
| Google | `"OpenSpending" (budget OR "fiscal data" OR "open spending")` |
| Censys | `web.names: "openspending.org"` |
| FOFA | `domain="openspending.org"` |

## ODWeb (`odweb`) {#odweb}

Chinese municipal and provincial public-data catalog under `/odweb/`. Distinct from Inspur oPortal (`oportal`) and Zhejiang JDOP (`jdop`).

**Signals:** path `/odweb/`; script roots `/odweb/{city}/libs/`; page title 公共数据开放平台.

**Confirm:** GET `http(s)://host/odweb/`. One record per city or provincial catalog, not per dataset. Skip hosts that redirected off `/odweb/` onto an unrelated government CMS.

| Tool | Query |
|------|-------|
| Google | `inurl:/odweb/ 数据开放` |
| Google | `"odweb" 公共数据开放平台` |
| Censys | `web.endpoints.http.body: "/odweb/"` |
| FOFA | `body="/odweb/" && title="数据开放"` |

## Guangxi Public Data Open Platform (`gxopendata`) {#gxopendata}

Guangxi Zhuang Autonomous Region public data portal. Provincial hub: [data.gxzf.gov.cn](https://data.gxzf.gov.cn). City tenants: `{city}.data.gxzf.gov.cn`. Not CKAN.

**Signals:** host `data.gxzf.gov.cn` or `{city}.data.gxzf.gov.cn`; 公共数据开放平台 chrome.

**Confirm:** GET the tenant home. One record per city or provincial tenant, not per dataset.

| Tool | Query |
|------|-------|
| Google | `site:data.gxzf.gov.cn` |
| Google | `"公共数据开放平台" site:gxzf.gov.cn` |
| Censys | `web.names: "data.gxzf.gov.cn"` |
| FOFA | `host="data.gxzf.gov.cn"` |
| crt.sh | `%.data.gxzf.gov.cn` |

## OpenGDC (`opengdc`) {#opengdc}

Dutch municipal open-data and Woo catalog (Drupal / Dexes). Product site: [opengdc.nl](https://www.opengdc.nl). Live tenants include Utrecht, Groningen, Nijmegen, Oss, Hilversum, and Land van Cuijk. Not the genomic OpenGDC (GDC/BED) tool.

**Signals:** `/datasets` catalog UI; `/api` titled “Open API Specification”; `/openapi.json` OpenAPI 3 with paths `/api/datasets`, `/api/documents`, `/api/dossiers`; JSON:API `type: dataset`. Title often “Datacatalogus” or “Dataportaal”.

**Confirm:** GET `https://host/openapi.json` and `https://host/api/datasets` (JSON:API, `meta.total`). Some tenants sit behind a WAF (`403`). Prefer `opengdc` over generic `drupal`. One municipality = one catalog.

| Tool | Query |
|------|-------|
| Google | `"OpenGDC" (dataportaal OR datacatalogus) site:.nl` |
| Google | `inurl:/openapi.json "api/datasets" (Datacatalogus OR Dataportaal)` |
| Censys | `web.endpoints.http.body: "api/dossiers"` |
| FOFA | `body="api/dossiers"` |

## Bitrix (`bitrix`) {#bitrix}

1C-Bitrix CMS used for government dataset catalogs. Site: [1c-bitrix.ru](https://www.1c-bitrix.ru). Skip ordinary Bitrix homepages.

**Signals:** Bitrix chrome; a **datasets** catalog section (открытые данные), not a news CMS.

**Confirm:** GET the public dataset listing. One catalog per dataset portal.

| Tool | Query |
|------|-------|
| Google | `"Битрикс" открытые данные` |
| Censys | `web.endpoints.http.body: "bitrix"` |
| FOFA | `body="bitrix"` |

## Copernicus Data Stores (`copernicuscds`) {#copernicuscds}

ECMWF Climate / Atmosphere / CEMS data stores. Hub: [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu).

**Confirm:** do **not** clone the CDS hub. Register only a distinct CDS/ADS/CEMS catalog UI. Harvest recipes: [harvest-earthdata.md](harvest-earthdata.md#copernicuscds).

| Tool | Query |
|------|-------|
| Google | `"Climate Data Store" Copernicus` |
| Censys | `web.names: "cds.climate.copernicus.eu"` |
| FOFA | `host="cds.climate.copernicus.eu"` |

## D4Science (`d4science`) {#d4science}

CNR virtual research environments with a gCube CKAN data-catalogue. Site: [d4science.org](https://www.d4science.org).

**Signals:** `/web/{lab}/data-catalogue`; `gcube-ckan-datacatalog`; D4Science VRE chrome.

**Confirm:** GET the public data-catalogue for that VRE. One catalog per lab catalogue, not the D4Science marketing home.

| Tool | Query |
|------|-------|
| Google | `"D4Science" (catalog OR "open data")` OR `inurl:d4science.org/web` |
| Censys | `web.names: "d4science.org"` |
| FOFA | `domain="d4science.org"` |

## data.gov.my (`datagovmy`) {#datagovmy}

Malaysia national open-data stack. Hub: [data.gov.my](https://www.data.gov.my).

**Confirm:** register **tenant** catalogs on the stack, not a second copy of the national hub. Duplicate-check `*.data.gov.my`.

| Tool | Query |
|------|-------|
| Google | `site:data.gov.my` tenant catalogs only |
| Censys | `web.names: "data.gov.my"` |
| FOFA | `host="data.gov.my"` |

## JDOP (`jdop`) {#jdop}

Zhejiang public-data open platform (浙江•数据开放). Distinct from Inspur oPortal (`oportal`) and ODWeb (`odweb`).

**Signals:** `/jdop_front/` or `/dopServer/`; 浙江•数据开放 chrome.

**Confirm:** GET the public dataset catalog. One record per provincial/municipal JDOP tenant.

| Tool | Query |
|------|-------|
| Google | `"JDOP" オープンデータ` OR `"jdop_front"` |
| Censys | `web.endpoints.http.body: "jdop_front"` |
| FOFA | `body="jdop_front"` |

## Open Data Registry (`opendatareg`) {#opendatareg}

AWS Labs YAML registry of public datasets (and regional IT clones named OpenData.reg). Source: [awslabs/open-data-registry](https://github.com/awslabs/open-data-registry).

**Confirm:** GET a public dataset registry UI or the published catalog files. Skip a GitHub clone with no catalog UI. One catalog per public registry.

| Tool | Query |
|------|-------|
| Google | `"opendata.reg"` OR `"Open Data Registry" awslabs` |
| Censys | `web.endpoints.http.body: "open-data-registry"` |
| FOFA | `body="open-data-registry"` |

## PublishMyData (`publishmydata`) {#publishmydata}

Swirrl linked-data publisher for official statistics. Site: [publishmydata.com](https://publishmydata.com). Docs: [publishmydata.com/docs](https://publishmydata.com/docs).

**Signals:** PublishMyData chrome; SPARQL / linked-data catalog UI.

**Confirm:** GET the public dataset/SPARQL catalog. One catalog per deployment.

| Tool | Query |
|------|-------|
| Google | `"PublishMyData" OR publishmydata` |
| Censys | `web.endpoints.http.body: "PublishMyData"` |
| FOFA | `body="PublishMyData"` |

## Semantic MediaWiki (`smw`) {#smw}

MediaWiki with semantic queries used as a dataset catalog. Site: [semantic-mediawiki.org](https://www.semantic-mediawiki.org). Skip ordinary MediaWiki encyclopedias.

**Signals:** Semantic MediaWiki / `#ask` catalog pages; RDF export of datasets.

**Confirm:** GET a public dataset/category listing. One catalog per wiki that publishes datasets.

| Tool | Query |
|------|-------|
| Google | `"Semantic MediaWiki" (dataset OR catalog)` |
| Censys | `web.endpoints.http.body: "Semantic MediaWiki"` |
| FOFA | `body="Semantic MediaWiki"` |

## Strapi (`strapi`) {#strapi}

Headless CMS. Site: [strapi.io](https://strapi.io). Docs: [strapi.io/docs](https://strapi.io/docs). Use only with a **public dataset API**, not a blog CMS.

**Signals:** `/api/` content-types that list datasets; Strapi admin is not the catalog.

**Confirm:** GET a public dataset collection. Skip login-only Strapi. One catalog per public API.

| Tool | Query |
|------|-------|
| Google | `"Strapi" ("open data" OR datasets)` |
| Censys | `web.endpoints.http.body: "strapi"` |
| FOFA | `body="strapi"` |

## Tablion (`tablion`) {#tablion}

Aristotle Metadata data portal. Product: [Tablion Data Portal](https://www.aristotlemetadata.com/products/tablion-data-portal/).

**Signals:** Tablion chrome; Aristotle metadata/data portal UI.

**Confirm:** GET the public dataset search. One catalog per portal.

| Tool | Query |
|------|-------|
| Google | `"Tablion" "data portal"` |
| Censys | `web.endpoints.http.body: "Tablion"` |
| FOFA | `body="Tablion"` |

## Other open-data platforms

| `software.id` | Signals | Typical query |
|---------------|---------|---------------|
| `ouropendata` | see above | |
| `gipuzkoairekia` | see above | |
| `datapress` | see above | |
| `modaopendata` | see above | |
| `bitrix` | see above | |
| `jdop` | see above | |
| `publishmydata` | see above | |
| `opendatareg` | see above | |
| `datagovmy` | see above | |
| `copernicuscds` | see above | |
| `tablion` | see above | |
| `strapi` | see above | |
| `smw` | see above | |
| `d4science` | see above | |
| `rdfrepository` | see above | |
| `resourcecontracts` | see above | |
| `openspending` | see above | |
| `gxopendata` | see above | |

## Generic open-data URL patterns

Try these on a **named** government or city host only (not as an internet-wide scan):

- `/data`, `/opendata`, `/datasets`, `/catalog`, `/datos`, `/donnees`
- `/data.json`, `/catalog.json`, `/catalog.xml` (DCAT)
- `/api/3/action/status_show` (CKAN)
- `/api/explore/v2.1/catalog/datasets` (OpenDataSoft)
- `/IdraPortal/` and `/Idra/api/v1/` (Idra)
- `/oportal/` (Inspur oPortal)
- `/openinf/` (Seoul Open Data Plaza)
- `/assets/cms/public.css` (Our Open Data)
- `*.revenuedev.org` tenant home (RDF Online Repository)
- `/contract/resources` (ResourceContracts)
- `{city}.data.gxzf.gov.cn` (Guangxi tenant)
- `/transparencia/datos/catalogo` (ATM Maggioli)
- `/opendata/set/lkod` (LKOD, including Slovak municipal clones)

Search with local terms plus the city: `datos abiertos "Rosario"`, `offene Daten "Leipzig"`, `开放数据 市`.

## National harvest sources {#national-harvest-sources}

When a country already has a national open-data portal, its **harvest / organisations / catalogues API** is a better candidate list than Google. Prompt: `Which data sources harvested by {national portal} are missing?`

Portals that produced origin catalogs in 28–30 August 2026 sessions:

| National portal | What to pull | Typical origin catalogs |
|-----------------|--------------|-------------------------|
| [data.go.id](https://data.go.id/) | Harvest-source list | Provincial/city CKAN and GeoServer (112 scheduled in one pass) |
| [datos.gob.es](https://datos.gob.es/) | Harvest sources | City/province CKAN and custom `/datos` |
| [opendata.swiss](https://opendata.swiss) | Harvest sources | Cantonal votes, BAG indicator DBs, Viageo — not geocat/I14Y/LINDAS slices |
| [data.gov.ru](https://data.gov.ru/) | Organisations with `/opendata` | Federal agency `list.csv` catalogs (Rosstat, Minenergo, …) |
| [search.open.canada.ca](https://search.open.canada.ca/opendata/) | Harvested origin URLs | Provincial geo/scientific portals not already in the registry |
| [data.gouv.fr](https://www.data.gouv.fr/) | Harvest sources | Local CKAN / uData / OpenDataSoft |
| [www.govdata.de](https://www.govdata.de/) | Harvest sources | Länder / municipal CKAN |
| [www.data.go.kr](https://www.data.go.kr/) | Harvest sources | Ministry/local portals |
| [dane.gov.pl](https://dane.gov.pl) | Institutions API | CKAN city catalogs only — thousands of XML dataset feeds are not catalogs |
| [data.europa.eu catalogues](https://data.europa.eu/data/catalogues) | Catalogue list | Member-state catalogs |

**Accept:** a live independent catalog UI on the origin host (CKAN `/api/3`, GeoNetwork CSW, ArcGIS Hub, agency `/opendata` dataset list). `is_national: false` on those origin catalogs.

**Reject:** harvest-source *rows* inside the national CKAN; XML/CSV dataset feeds and developer price files; slices of the same national catalog (geocat, I14Y, LINDAS); scientific IR dumps already registered; login walls; a private ArcGIS org when a public Hub exists (register the Hub).

Duplicate-check the origin hostname, then GET the origin homepage. Do not invent harvest API paths — use the portal’s documented organisations/harvest endpoint.


## GIS Open Data Portal (`gisopendataportal`) {#gisopendataportal}

Shared municipal catalog deployed at `tvrdosin.twinmap.ai` and `nove-mesto.twinmap.ai`.
Both `/developer` pages identify the same `gis-open-data-portal/od-portal` source project
and document `/api/open-api/features`, GraphQL at `/api/open-api`, and DCAT-AP-SK at
`/api/opendata/set/catalog/lkod`. Confirm this combination and the repository attribution;
a `twinmap.ai` hostname or a Next.js bundle alone is insufficient. The advertised GitLab
repository redirected to sign-in on 2026-09-07, so do not assume a verified open-source license.

Search: `"gis-open-data-portal/od-portal"`, `site:twinmap.ai "OpenAPI"`.
First-party examples: [Tvrdošín developer guide](https://tvrdosin.twinmap.ai/developer),
[Nové Mesto developer guide](https://nove-mesto.twinmap.ai/developer).


| Tool | Query |
|------|-------|
| Google | `"gis-open-data-portal/od-portal" OR site:twinmap.ai OpenAPI` |
| Censys | `web.names: "twinmap.ai"` |
| FOFA | `host="twinmap.ai"` |


## Esri UK Data Observatory (`esridataobservatory`) {#esridataobservatory}

Managed local-data service, formerly InstantAtlas Data Observatory. Confirm vendor or
operator attribution to the product, with supporting Data Explorer / Quick Ward Profile /
Custom Area Reporter features. Technical corroboration includes
`hub.instantatlas.com/data-catalog-explorer/` assets and `window.dataCatalogExplorer.launch`.
WordPress, ArcGIS maps, or an embedded report alone do not establish this product.
Confirmed Oxfordshire, Kingston, and Ealing deployments load `/wp-content/themes/ia-theme/`
with `ia-map.js`, `ia-quickprofile.js`, and `ia-stat.js`, and explicitly credit Esri UK.
Use this combination of theme assets and attribution as a stronger installation fingerprint.
The [vendor product page](https://www.esriuk.com/en-gb/arcgis/products/instantatlas/products/data-observatory)
identifies Suffolk; the [Hounslow case study](https://resource.esriuk.com/esri-resources/london-borough-of-hounslow/)
confirms another independent deployment. See the [branding and theme documentation](https://help.instantatlas.com/category/data-observatory/).

Search: `"Esri UK Data Observatory"`, `"InstantAtlas Data Observatory"`,
`"hub.instantatlas.com/data-catalog-explorer"`.


| Tool | Query |
|------|-------|
| Google | `"Esri UK Data Observatory" OR "InstantAtlas Data Observatory"` |
| Censys | `web.endpoints.http.body: "hub.instantatlas.com/data-catalog-explorer"` |
| FOFA | `body="dataCatalogExplorer"` |


## RUDI (`rudi`) {#rudi}

An independently deployable, distributed data-sharing platform. The
[portal source](https://github.com/rudi-platform/rudi-portal) identifies the
[Rennes deployment](https://rudi.rennesmetropole.fr/); the
[out-of-the-box distribution](https://github.com/rudi-platform/rudi-out-of-the-box)
provides Docker Compose installation. Match explicit RUDI branding and project provenance,
not generic Angular bundles. Producer nodes and the central metadata portal have different
interfaces. See [API documentation](https://doc.rudi.fr/api/api_exposees/).


| Tool | Query |
|------|-------|
| Google | `"RUDI" (données OR "data sharing") -site:github.com` |
| Censys | `web.endpoints.http.body: "rudi-portal"` |
| FOFA | `body="RUDI" && body="rudi"` |


## SIMAI Open Data Portal (`simaiopendata`) {#simaiopendata}

The [vendor product page](https://simai.ru/solution/gosudarstvennye-organizatsii/simai-portal-otkrytykh-dannykh/)
markets a dedicated 1C-Bitrix open-data application and links its
[current demo](https://opendata.sf2.simai.ru/). Strong fingerprints are explicit
«SIMAI: Портал открытых данных» credit plus `simai.opendata` template/cache asset paths.
Generic `/bitrix/` assets alone do not identify this product. The Bashkortostan-branded
vendor demo is not a production government portal; the old `opendata.demo.simai.ru`
host currently serves a hosting placeholder.


| Tool | Query |
|------|-------|
| Google | `"SIMAI" "Портал открытых данных" OR simai.opendata` |
| Censys | `web.endpoints.http.body: "simai.opendata"` |
| FOFA | `body="simai.opendata"` |

## Related

- [discovery.md](discovery.md)
- [discovery.md](discovery.md#hunt-patterns) — session hunt patterns
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-metadata.md](discovery-metadata.md)
- [discovery-indicators.md](discovery-indicators.md)
- [discovery-other.md](discovery-other.md)
- [harvest-opendata.md](harvest-opendata.md)
- [harvest.md](harvest.md)
- [harvest-protocols.md](harvest-protocols.md)
- [apidetect.md](apidetect.md)
- [ckan-sync.md](ckan-sync.md)
- [catalog-types.md](catalog-types.md)
- [software-taxonomy.md](software-taxonomy.md)

