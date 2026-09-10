# Harvesting datasets from open data portals

CKAN, OpenDataSoft, Socrata, and similar portals already treat **datasets** (packages, views) as the primary object. ResourceContracts and RDF Online Repository list **contracts / licenses**; Guangxi tenants and ODWeb catalogs list **open datasets**. You rarely need the publication-type filters used for [scientific repositories](harvest-scientific.md). You still must avoid harvesting the wrong object (resources, showcases, harvest sources, individual files, login-only filings).

Overview: [harvest.md](harvest.md). Finding portals: [discovery-opendata.md](discovery-opendata.md). Shared DCAT/CKAN grain: [harvest-protocols.md](harvest-protocols.md).

Replace `https://host` with the catalog origin. GET only. Stop on `401`/`403`. Prefer URLs already in `endpoints[]`.

## What to keep

| Keep | Drop |
|------|------|
| Dataset / package / view / explore dataset | A file **resource** (CSV) as if it were a separate catalog record |
| ResourceContracts **contract** / RDF Online Repository **license** | Vendor About page, per-clause chrome, login-only company filing |
| Guangxi tenant **open dataset** | Login-only apply / API-gateway flows |
| ODWeb `/odweb/` **dataset** | Parent government homepage, login-only apply flows |
| OpenGov **report / story** on `{org}.opengov.com` | Vendor marketing; Highcharts series as separate catalogs |
| The dataset landing API object | Harvest **source** metadata (the remote catalog CKAN is pulling from) |
| | Showcase, article, blog, app gallery, idea box |
| | Organization or group objects without a dataset list |

One dataset with five CSV resources is **one** dataset.

## CKAN (`ckan`) {#ckan}

**Search (preferred):**

```text
GET https://host/api/3/action/package_search?q=&rows=100&start=0
```

Use `start` += `rows` until `count` is reached. Each `results[]` element is a dataset.

**Optional filter** when the site mixes types:

```text
GET https://host/api/3/action/package_search?fq=dataset_type:dataset&rows=100
```

Drop `dataset_type:showcase` (ckanext-showcase), harvest objects, and `type:harvest`.

`package_list` returns names only and is painful on large sites — prefer `package_search`.

DataPress (`datapress`) is CKAN plus CMS — harvest `package_search`, not CMS pages. Do not also harvest the same host as `ckan`.

OpenAIRE Graph/CONNECT gateways are **data search engines**, not open-data CMSs. Recipe: [harvest-other.md](harvest-other.md#openaire).

**Keep:** `package_search` **packages** (`results[]`). **Drop:** `dataset_type:showcase`, harvest source objects, `type:harvest`, and individual resources.

## DKAN (`dkan`) {#dkan}

Same Action API as [CKAN](#ckan) when enabled; also `/api/1/search`. Confirm JSON `"success": true`. If only Drupal JSON:API is public, see [Drupal](#drupal) and prefer `dkan` when the product is DKAN.

**Keep:** packages from CKAN-compatible Action API or `/api/1/search`.
**Drop:** Drupal nodes that are not datasets. Prefer `dkan` over `drupal` when the product is DKAN.

```text
GET https://host/api/3/action/package_search?rows=25
GET https://host/api/1/search
```


## OpenDataSoft (`opendatasoft`) {#opendatasoft}

Already a dataset catalog:

```text
GET https://host/api/explore/v2.1/catalog/datasets?limit=100&offset=0
```

Follow `links` / offset until `total_count`. Do not harvest the vendor academy or `www.opendatasoft.com`.

**Keep:** explore **datasets**. **Drop:** the vendor academy, `www.opendatasoft.com`, and individual records as extra catalogs.

## Socrata (`socrata`) {#socrata}

Views include charts, maps, files, and stories.

```text
GET https://host/api/catalog/v1?only=datasets&limit=100&offset=0
```

Legacy: `/api/views.json` mixes types — filter `viewType` / `displayType` to tabular datasets, or use the catalog API `only=datasets`. Drop `only=stories`, `only=filters`.

**Keep:** catalog API views with `only=datasets`. **Drop:** `only=stories`, `only=filters`, charts-as-datasets, and mixed `/api/views.json` without a type filter.

## uData (`udata`) {#udata}

```text
GET https://host/api/1/datasets/?page_size=100&page=1
```

Do not page `/api/1/reuses/` or `/api/1/posts/` as datasets.

**Keep:** `/api/1/datasets/` dataset objects. **Drop:** `/api/1/reuses/` and `/api/1/posts/`.

## Magda (`magda`) {#magda}

Catalog search API from `endpoints[]`. Keep datasets, not portal chrome.

**Keep:** datasets from the catalog search API in `endpoints[]`.
**Drop:** portal chrome, organisations, and distributions as extra datasets.

```text
GET https://host/api/v0/search/datasets
```


## JKAN (`jkan`) {#jkan}

Often static JSON in the repo.

```text
GET https://host/data.json
GET https://host/datasets.json
```

**Keep:** published dataset entries. **Drop:** GitHub issues and the JKAN docs site.

## Junar (`junar`) {#junar}

Dataset API on the tenant, not junar.com marketing.

**Keep:** tenant dataset API records.
**Drop:** junar.com marketing and individual visualization embeds.

```text
GET https://host/api/v2/datasets
```


## EntryScape (`entryscape`) {#entryscape}

DCAT-AP. Harvest **Dataset** / `dcat:Dataset` only. Public DCAT/search API on the tenant.

**Keep:** `dcat:Dataset` from the tenant DCAT/search API.
**Drop:** catalog chrome, documents that are not datasets, and EntryStore admin.

```text
GET https://host/store/search?type=dcat:Dataset
```


## Piveau (`piveau`) {#piveau}

DCAT-AP search; skip the hub UI chrome. Keep `dcat:Dataset` only.

**Keep:** `dcat:Dataset` from DCAT-AP search.
**Drop:** hub UI chrome and harvested copies of catalogs already in this registry.

```text
GET https://host/api/hub/search
```


## Idra (`idra`) {#idra}

Federation of other catalogs (`catalog_type` is often Data search engine). Harvesting Idra duplicates member catalogs — prefer harvesting the **source** portals from this registry unless you need the federation view.

**Keep:** federation dataset records only if the user asked for the hub view.
**Drop:** member catalogs already in this registry (harvest those origins instead).

```text
GET https://host/Idra/api/v1/catalogues
```


## ArcGIS Hub (`arcgishub`) as open data {#arcgishub}

```text
GET https://host/api/search/v1
```

Keep dataset / feature layer **items** that are public data. Drop StoryMaps, sites, and applications unless you have a separate apps index.

**Keep:** public dataset / feature layer **items**. **Drop:** StoryMaps, Hub sites, and applications unless you have a separate apps index.

## Data Fair (`datafair`) {#datafair}

Koumoul portals. Typical list:

```text
GET https://host/data-fair/api/v1/datasets
```

Page the JSON dataset collection. Drop applications and remote-service catalog chrome. Paths vary — use `endpoints[]` when present.

**Keep:** Data Fair **datasets**. **Drop:** applications and remote-service catalog chrome.

## Datawheel (`datawheel`) {#datawheel}

Front-end data/economic-complexity sites. There is often **no** common `/api`. Harvest a documented JSON/CSV catalog if the portal publishes one; otherwise stop rather than scraping every visualization.

**Keep:** a documented JSON/CSV catalog if the portal publishes one.
**Drop:** every visualization tile. Stop when there is no catalog API.

```text
GET https://host/api
```


## TriplyDB (`triplydb`) {#triplydb}

```text
GET https://host/_api/facets/datasets
```

Keep **datasets**, not every named graph or SPARQL binding. One instance, not one graph per harvest record. See [harvest-protocols.md](harvest-protocols.md#sparql--linked-data).

**Keep:** TriplyDB **datasets**. **Drop:** named graphs and SPARQL bindings as extra datasets.

## LKOD (`lkod`) {#lkod}

Czech local DCAT-AP-CZ. Harvest `dcat:Dataset` from the municipal LKOD UI/API. Slovak clones often expose Turtle at `/opendata/set/lkod`:

```text
GET https://host/opendata/set/lkod
```

Harvest that graph, not POMOSAM disclosure pages on the same city. Do not also harvest NKOD or data.slovensko.sk for the same datasets.

**Keep:** `dcat:Dataset` from the municipal LKOD UI/API or `/opendata/set/lkod`. **Drop:** POMOSAM disclosure pages, NKOD, and data.slovensko.sk copies.

## OGD Platform India (`ogdindia`) {#ogdindia}

Ministry/state tenants on data.gov.in. Catalog APIs often **require a registered key** — stop on `401`.

**Keep:** the public CKAN-style or HTML catalog list when it is available without a key. **Drop:** the national hub when you only needed a tenant, and every dataset behind a developer-key Open API.

## data eye (`dataeye`) {#dataeye}

Japanese municipal SaaS. Some tenants speak CKAN-compatible metadata.

```text
GET https://host/api/3/action/status_show
GET https://host/api/3/action/package_search?rows=0
```

**Keep:** tenant **datasets** from `package_search` or the public catalog JSON. **Drop:** idea-box posts and the vendor homepage. One tenant = one scope (`%.dataeye.jp`). If `status_show` 404s, harvest the HTML catalog list only.

## Seoul Open Data Plaza (`seoulopendataplaza`) {#seoulopendataplaza}

`/openinf/` JSP catalogs. Open API developer space often needs a key.

```text
GET https://host/openinf/
```

**Keep:** the public dataset listing / sitemap when unauthenticated access exists. **Drop:** developer-key Open API calls and the Seoul homepage. One `gu` tenant = one scope.

## oPortal (`oportal`) {#oportal}

Inspur `/oportal/` catalogs. There is no verified anonymous default API on every tenant.

```text
GET https://host/oportal/
```

**Keep:** `/oportal/` dataset listing or DCAT if public. **Drop:** the application gallery and login-only 数据开放 admin.

## Liferay (`liferay`) {#liferay}

Spanish RISP / datos abiertos modules on Liferay. Harvest only the **dataset list** (often a JSON/CSV/XML table or `/documents/` open-data folder).

**Keep:** rows that are datasets (title + landing or file URL). **Drop:** `/web/guest/` CMS homepages, news, and generic document libraries.

If the list is HTML-only with no machine table, stop. Do not crawl every Liferay page.

## POMOSAM (`pomosam`) {#pomosam}

Slovak municipal disclosure platforms.

**Keep:** the open-data / dataset module. **Drop:** procurement and contracts-only pages unless that module **is** the data catalog. If the list is HTML-only with no machine table, stop.

## SEU-e (`seue`) {#seue}

`seu-e.cat` e-office tenants.

**Keep:** **dades obertes** listings. **Drop:** the rest of the electronic office (procedures, notifications, sede chrome). If the list is HTML-only with no machine table, stop.

## ATM Maggioli (`atmmaggioli`) {#atmmaggioli}

Spanish sede electrónica tenants. Harvest the **dataset list** on `/transparencia/datos/catalogo` only.

```text
GET https://host/transparencia/datos/catalogo
```

**Keep:** rows that are datasets (title + landing or file URL). **Drop:** the rest of the e-office, transparency obligation pages, and guessed CKAN/OpenDataSoft/Socrata paths (they are HTML). If the list is HTML-only with no machine table, stop. One municipality tenant = one harvest scope.

## OpenGov (`opengov`) {#opengov}

US `{org}.opengov.com` financial transparency.

```text
GET https://host/transparency
GET https://host/data/
```

**Keep:** named **reports / stories** on `/transparency` or `/data/`. **Drop:** every Highcharts breakdown row and `www.opengov.com` marketing. One government tenant = one harvest scope. Distinct from the city’s CKAN/Socrata/ArcGIS Hub open-data portal.

## Drupal (`drupal`) {#drupal}

Only when the public product is a dataset catalog (not a news CMS).

```text
GET https://host/jsonapi/node/dataset
GET https://host/data.json
```

Bundle names vary (`dataset`, `open_data`, `ckan_dataset`). Inspect `/jsonapi` once for dataset-like bundles. **Keep:** those dataset nodes. **Drop:** `article`, `page`, `media`, and user accounts.

DKAN on Drupal: use the [DKAN](#dkan) Action API when enabled — prefer `dkan` as `software.id`.

## WordPress (`wordpress`) {#wordpress}

```text
GET https://host/wp-json/
GET https://host/wp-json/wp/v2/dataset
```

`/wp-json/` only for a **datasets** custom post type (`/wp-json/wp/v2/dataset` or the type the catalog documents). **Keep:** dataset posts. **Drop:** `/wp/v2/posts`, media, and ordinary WordPress homepages.

## Bitrix (`bitrix`) {#bitrix}

1C-Bitrix government portals. Harvest only a published **open-data / dataset** module (JSON/CSV/DCAT list). Skip the rest of the CMS, news, and `/bitrix/admin/`.

**Keep:** records from a published open-data / dataset module (JSON, CSV, or DCAT list).
**Drop:** CMS news, `/bitrix/admin/`, and the rest of the government site.

```text
GET https://host/opendata/
GET https://host/opendata/opendata.json
```


## DataPress (`datapress`) {#datapress}

CKAN plus CMS. Harvest `package_search` as in [CKAN](#ckan). Do not harvest CMS pages or double-count the host as `ckan`.

**Keep:** CKAN packages via `package_search` (same grain as CKAN).
**Drop:** CMS pages. Do not double-count the host as `ckan`.

```text
GET https://host/api/3/action/package_search?rows=25
```


## Our Open Data (`ouropendata`) {#ouropendata}

Japanese Our Open Data / SHIRASAGI catalog.

```text
GET https://host/api/package_list
```

**Keep:** datasets from `/api/package_list` or the catalog home / numeric dataset list. **Drop:** idea-box posts. Do not treat `/api/package_list` as CKAN.

## Gipuzkoa Irekia (`gipuzkoairekia`) {#gipuzkoairekia}

Tenant DCAT. Keep datasets, not the rest of the Irekia CMS.

**Keep:** tenant DCAT datasets.
**Drop:** the rest of the Irekia CMS.

```text
GET https://host/catalogo.rdf
```


## MODA (`modaopendata`) {#modaopendata}

Tenant catalog API, not a second national data.gov.tw clone.

**Keep:** tenant catalog API datasets.
**Drop:** a second copy of national data.gov.tw.

```text
GET https://host/api/v2/rest/dataset/od{limit}
```


## PublishMyData (`publishmydata`) {#publishmydata}

Linked-data publishing (Swirrl).

```text
GET https://host/data.json
```

**Keep:** the **DCAT dataset list** or SPARQL that the catalog documents — named datasets. **Drop:** every triple in the graph ([harvest-protocols.md](harvest-protocols.md#sparql--linked-data)).

## data.gov.my (`datagovmy`) {#datagovmy}

Malaysia national / agency tenants on the data.gov.my stack.

```text
GET https://api.data.gov.my/data-catalogue?id=fuelprice
```

`id` is required. That response is **observations** for one catalogue dataset — treat each `id` as one dataset analog; do not page rows as datasets. There is no verified anonymous GET that lists all catalogue ids; collect ids from the public catalogue UI or [developer.data.gov.my](https://developer.data.gov.my/). Drop dashboards and documentation pages. Agency sites (`open.dosm.gov.my`, `data.moh.gov.my`) are separate registry rows — harvest each tenant once.

**Keep:** each catalogue `id` as one dataset analog. **Drop:** observation rows, dashboards, and documentation pages.

## JDOP (`jdop`) {#jdop}

Zhejiang public-data open platform (`/jdop_front/`, `/dopServer/`).

```text
GET https://host/jdop_front/
```

**Keep:** the tenant **dataset catalog** API when public. **Drop:** the Zhejiang government homepage and login-only 数据开放 admin.

## Open Data Registry (`opendatareg`) {#opendatareg}

AWS Open Data Registry style catalogs (`catalog.json` / YAML dataset files, optional STAC). Keep **dataset** entries. Drop bucket listings and every STAC **item**. Skip cloning registry.opendata.aws if you only needed the existing registry row.

```text
GET https://host/catalog.json
```

**Keep:** **dataset** entries. **Drop:** bucket listings and every STAC **item**.

## D4Science (`d4science`) {#d4science}

**Keep:** **public catalogue items** on the VRE (gCat / documented dataset list). **Drop:** workspace files, private VREs, and d4science.org marketing. Stop on `401`.

## Semantic MediaWiki (`smw`) {#smw}

```text
GET https://host/w/api.php?action=ask&query=[[Category:Dataset]]
```

Keep pages typed as Dataset (or the site’s equivalent category). Drop ordinary wiki articles. `api.php` without a dataset query is not a harvest.

**Keep:** pages typed as Dataset (or the site’s equivalent category). **Drop:** ordinary wiki articles and unfiltered `api.php`.

## Strapi (`strapi`) {#strapi}

```text
GET https://host/api/datasets
```

Public **dataset** content-type REST only (`/api/datasets` or the type the catalog documents). **Keep:** dataset entries. **Drop:** posts, users, and admin.

## Tablion (`tablion`) {#tablion}

Aristotle’s data-portal product.

**Keep:** the public **dataset** API. **Drop:** every MDR object (concepts, classifications, quality statements) unless the user asked for metadata catalogs ([harvest-metadata.md](harvest-metadata.md)).

Copernicus CDS (`copernicuscds`): [harvest-earthdata.md](harvest-earthdata.md#copernicuscds). Discovery fingerprints: [discovery-opendata.md](discovery-opendata.md).

## RDF Online Repository (`rdfrepository`) {#rdfrepository}

Public license/workspace tables on `*.revenuedev.org`. Filter exports on `software.id = 'rdfrepository'`.

```text
GET https://host/
```

**Keep:** the published **dataset / license list** if unauthenticated. **Drop:** login-only company filing modules. One harvest scope per country tenant. Distinct from W3C RDF.

## ResourceContracts (`resourcecontracts`) {#resourcecontracts}

```text
GET https://host/contract/resources
```

Keep **contracts** (documents). Drop the vendor About page and per-clause annotation chrome unless that is the catalog. One hub or country tenant = one harvest scope.

**Keep:** ResourceContracts **contracts**. **Drop:** vendor About page and per-clause chrome.

## OpenSpending (`openspending`) {#openspending}

```text
GET https://openspending.org/
```

Keep **budget / fiscal datasets** (Fiscal Data Packages). Drop individual treemap visualizations and the OKF About page. One harvest scope per OpenSpending hub or independent deployment.

**Keep:** budget / fiscal **datasets**. **Drop:** treemap visualizations and the OKF About page.

## ODWeb (`odweb`) {#odweb}

Public dataset list under `/odweb/`. Filter exports on `software.id = 'odweb'`.

Keep **open datasets** for that tenant. Drop login-only apply flows and the parent government homepage. One `/odweb/` host = one harvest scope. Not CKAN; not [oPortal](#oportal); not [JDOP](#jdop).

```text
GET https://host/odweb/
```

**Keep:** ODWeb `/odweb/` **datasets**. **Drop:** login-only apply flows and the parent government homepage.

## Guangxi Public Data Open Platform (`gxopendata`) {#gxopendata}

Public dataset / directory list on `data.gxzf.gov.cn` or `{city}.data.gxzf.gov.cn`. Filter exports on `software.id = 'gxopendata'`.

Keep **open datasets** for that tenant. Drop login-only apply/API-gateway flows. One tenant = one harvest scope. Not CKAN.

**Keep:** Guangxi tenant **open datasets**. **Drop:** login-only apply/API-gateway flows.

## OpenGDC (`opengdc`) {#opengdc}

Dutch municipal catalog. Harvest datasets only:

```text
GET https://host/api/datasets
GET https://host/openapi.json
```

JSON:API collection (`data[].type == "dataset"`, `meta.total`). Page with the API’s start/rows (or follow `links`). **Keep:** dataset objects. **Drop:** `/api/documents` and `/api/dossiers` (Woo files), CMS pages, and idea boxes. One municipality tenant = one harvest scope. Some hosts return `403` from a WAF — stop; do not scrape HTML as a substitute.

## Portals without a dataset API

Liferay, POMOSAM, ATM Maggioli, oPortal, OGD India, Seoul plaza, Drupal, and WordPress are covered above when a list exists. If there is still no machine-readable catalog, stop. Generic DCAT paths: `/catalog.xml`, `/data.json` ([harvest-protocols.md](harvest-protocols.md#dcat)).


## GIS Open Data Portal (`gisopendataportal`) {#gisopendataportal}

Start at `/api/opendata/set/catalog/lkod`: the DCAT-AP-SK JSON-LD catalog contains a
`dataset` array of metadata URLs under `/api/opendata/set/{uuid}`. Keep one record per
dataset URL, retaining the source IRI, publisher, description, and distributions. Resolve
its declared JSON-LD context; do not assume English JSON property names. Follow dataset
metadata to CSV downloads. Drop site navigation and individual spatial features from the
catalog inventory.

```text
GET https://host/api/opendata/set/catalog/lkod
```

**Keep:** one DCAT-AP-SK **dataset** per metadata URL. **Drop:** site navigation and individual spatial features. Feature retrieval is a separate operation at
`/api/open-api/features?limit=1&page=1`, with `filter.featureClass.id` or
`filter.featureClass.code`; coordinates may use EPSG:5514. GraphQL is documented at
`/api/open-api`. Both municipal catalog responses were verified on 2026-09-07.

Use [Tvrdošín](https://tvrdosin.twinmap.ai/developer) or
[Nové Mesto](https://nove-mesto.twinmap.ai/developer) for the deployment's API contract.
Tvrdošín's catalog currently copies Nové Mesto's title: retain provenance and do not infer
publisher identity from that title alone.

## Esri UK Data Observatory (`esridataobservatory`) {#esridataobservatory}

Start at the deployment's linked Data Explorer page (for example, the
[Suffolk explorer](https://www.suffolkobservatory.info/data-explorer/)). Read its published
application configuration to resolve the ArcGIS data catalog and backing service URLs;
there is no assumed universal `/api/3/action` or DCAT endpoint. The
[vendor embedding guide](https://help.instantatlas.com/category/data-observatory/)
documents `dataCatalogExplorer.launch` with an ArcGIS application ID. Keep discoverable
source datasets or indicator tables and their metadata; drop WordPress posts, ward-profile
pages, rendered charts, and per-area observation rows from the catalog inventory.

**Keep:** discoverable source datasets or indicator tables. **Drop:** WordPress posts, ward-profile pages, rendered charts, and per-area observation rows.
Deduplicate repeated references to the same source item/table across reports. Use only
publicly accessible services, retaining source IDs and licensing information. API URLs
and access vary by deployment; a single standalone harvest endpoint was not verified in
this review.

## RUDI (`rudi`) {#rudi}

Use the deployment's [documented API](https://doc.rudi.fr/api/api_exposees/).
Portal metadata search uses `/konsult/v1/datasets/metadatas`; the documented anonymous
session requires a token from `/authenticate`. Follow the published public-access flow
and preserve access restrictions. Producer nodes instead expose `/api/v1/resources`
and `/api/v1/resources/{id}`, as documented in the
[node catalog source](https://github.com/rudi-platform/rudi-node-catalog). Do not assume
node routes exist on the portal host. Keep one metadata record per `global_id`, follow
pagination and producer provenance, and distinguish catalog visibility from permission to
retrieve the underlying data.

**Keep:** one RUDI metadata record per `global_id`. **Drop:** guessed node `/api/v1/resources` on the portal host, and login-only search. No anonymous API access was verified on the registered
Rennes portal in this review; its existing access fields are preserved.

## SIMAI Open Data Portal (`simaiopendata`) {#simaiopendata}

Start from the deployment's `/datasets/` directory and follow dataset detail links.
Keep one dataset passport with its publisher, description and linked downloads; exclude
category pages, organization indexes, news and individual table rows.

```text
GET https://host/datasets/
```

**Keep:** one SIMAI dataset passport per `/datasets/` detail page. **Drop:** category pages, organization indexes, news, and individual table rows. Consult the
[product manual](https://support.simai.ru/learn/courses/course/12/index). No stable
public metadata API was verified; do not infer one from the underlying Bitrix CMS.
The [vendor demo](https://opendata.sf2.simai.ru/datasets/) contains demonstration data
and must remain distinguishable from production holdings.

## Related

- [harvest.md](harvest.md)
- [harvest-scientific.md](harvest-scientific.md)
- [harvest-geoportals.md](harvest-geoportals.md)
- [discovery-opendata.md](discovery-opendata.md)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-incremental.md](harvest-incremental.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [apidetect.md](apidetect.md)
- [agents/harvest.md](agents/harvest.md)

