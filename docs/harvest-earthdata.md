# Harvesting earth-observation and gridded data

THREDDS, ERDDAP, STAC, Open Data Cube, Sentinel Hub, ESA Science Archive TAP, and similar catalogs list **coverages, collections, TAP tables, and datasetIDs** — not journal articles. The usual mistake is harvesting every NetCDF file, STAC **item**, FITS cutout, or map tile as a dataset.

Overview: [harvest.md](harvest.md). OGC/STAC grain: [harvest-protocols.md](harvest-protocols.md). Finding installations: [discovery-geoportals.md](discovery-geoportals.md), [discovery-scientific.md](discovery-scientific.md). GET only. Stop on `401`/`403`.

## What to keep

| Keep | Drop |
|------|------|
| THREDDS `dataset` with an ID / OPeNDAP service | Nested **directories** and every file under `datasetScan` |
| ERDDAP `datasetID` row | `allDatasets` helper; every time-step query |
| STAC / ODC **collection** | Granules/items unless that is the product |
| openEO **collection** | `/processes`, jobs, process-graph examples |
| Rasdaman **coverage** (WCS) | WCPS query results as extra datasets |
| Copernicus **collection** / product type | Individual scenes when a collection exists |
| Sentinel Hub **STAC collection** | Process API jobs, EO Browser tiles, items/granules |
| ESA Science Archive **TAP tables / observations** | Individual FITS files and cutouts |
| DataONE MN **DATA** objects | CN-wide duplicates of nodes you already harvest |

Replace `https://host` with the catalog origin. Prefer `endpoints[]`.

## THREDDS (`thredds`) {#thredds}

```text
GET https://host/thredds/catalog.xml
```

Recurse `catalogRef`. Harvest `dataset` elements that expose OPeNDAP, WMS, or a durable ID. Prefer `thredds` over `opendap` on the same TDS. Detail also in [harvest-scientific-domain.md](harvest-scientific-domain.md#thredds).

**Keep:** THREDDS `dataset` with an ID / OPeNDAP service. **Drop:** nested directories and every file under `datasetScan`.

## ERDDAP (`erddap`) {#erddap}

```text
GET https://host/erddap/info/index.json
```

Each `datasetID` is one dataset. Grid and table datasets are both in scope. Do not page `tabledap` rows as datasets.

**Keep:** ERDDAP `datasetID` rows. **Drop:** `allDatasets` helper and every time-step query.

## OPeNDAP (`opendap`) {#opendap}

OPeNDAP directory or implementation-specific catalog. Harvest catalog **dataset nodes**, not every `.nc` URL. For an OPeNDAP Hyrax server, use the [Hyrax recipe](harvest-scientific-domain.md#opendaphyrax). If THREDDS or ERDDAP is on the same host, use those recipes.

**Keep:** catalog **dataset nodes**.
**Drop:** every `.nc` URL. If the host is THREDDS, ERDDAP, Pydap, or OPeNDAP Hyrax, use that recipe instead.

```text
GET https://host/opendap/
```


## PyDAP (`pydap`) {#pydap}

Same catalog-node grain as [OPeNDAP](#opendap) when the public product is PyDAP.

**Keep:** catalog dataset nodes (same grain as OPeNDAP).
**Drop:** every NetCDF URL as a dataset.

```text
GET https://host/
```


## STAC API (`stacserver`) {#stacserver}

```text
GET https://host/collections
```

Default grain is **collections**. `/search` is a query API — set `limit` and follow `rel=next`. Items are granules. Full recipe: [harvest-geoportals.md](harvest-geoportals.md#stacserver).

**Keep:** STAC **collections**. **Drop:** granules/items unless that is the product.

## STAC Browser (`stacbrowser`) {#stacbrowser}

Harvest the STAC API the browser points at, not Browser HTML. [harvest-geoportals.md](harvest-geoportals.md#stacbrowser).

**Keep:** the STAC API the browser points at (`catalog.json` / `config.js` `href`).
**Drop:** Browser HTML. Do not harvest twice if `stacserver` is already on that origin.

```text
GET https://host/catalog.json
```


## Open Data Cube (`opendatacube`) {#opendatacube}

Prefer the public **STAC** or OWS `/collections` on that host. The explorer UI is not a dump. Do not harvest indexer/admin. If `software.id` is `stacserver` on the same cube, harvest STAC once.

**Keep:** public STAC or OWS `/collections`.
**Drop:** explorer UI dumps and indexer/admin. Harvest STAC once if `stacserver` is on the same cube.

```text
GET https://host/stac/collections
GET https://host/collections?f=json
```


## Data Cube OWS (`datacubews`) {#datacubews}

Same `/collections` grain as [Open Data Cube](#opendatacube) when the public product is OWS.

```text
GET https://host/collections?f=json
```

**Keep:** OWS `/collections`. **Drop:** explorer UI dumps.

## Rasdaman (`rasdaman`) {#rasdaman}

```text
GET https://host/rasdaman/ows?SERVICE=WCS&REQUEST=GetCapabilities
```

Each CoverageId is a dataset analog. Skip petascope HTML chrome and one-off WCPS plots.

**Keep:** Rasdaman **coverage** (WCS CoverageId). **Drop:** WCPS query results and petascope HTML.

## ncWMS (`ncwms`) {#ncwms}

WMS GetCapabilities layers (Godiva is a viewer). If a parent THREDDS catalog lists the same datasets, harvest THREDDS.

```text
GET https://host/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
```

**Keep:** WMS GetCapabilities layers. **Drop:** Godiva viewer chrome, and a second crawl when THREDDS lists the same datasets.

## Copernicus DHuS (`copernicusdhus`) {#copernicusdhus}

Sentinel **DHuS** OData (`/odata/v1/Products` or documented search). Prefer **product types / collections** over every granule. Many nodes need a guest account — stop on `401`. Do not scrape the map.

**Keep:** Sentinel **product types / collections**.
**Drop:** every granule as a dataset. Stop on `401` (guest accounts are common).

```text
GET https://host/odata/v1/Products?$top=1
```


## Copernicus CDS (`copernicuscds`) {#copernicuscds}

Climate/Atmosphere Data Store. Harvest the public **dataset** catalogue (CDS dataset ids), not every retrieve job. API keys are common — stop on `401`. Do not clone cds.climate.copernicus.eu if you only needed the existing registry record.

**Keep:** CDS **dataset** catalogue ids.
**Drop:** retrieve jobs, map tiles, and cds.climate.copernicus.eu if you only needed the existing registry record. Stop on `401`.

```text
GET https://cds.climate.copernicus.eu/api/catalogue/v1/collections
```


## openEO (`openeo`) {#openeo}

```text
GET https://host/collections
GET https://host/.well-known/openeo
```

Each **collection** is a dataset analog (STAC-compatible). Do not harvest `/processes` as datasets, job results, or process-graph examples. Items/granules only when that is the product. Prefer `openeo` over `stacserver` on the same API. Hub (`hub.openeo.org`) lists backends — harvest `/collections` on the backend URL.

**Keep:** openEO **collections**. **Drop:** `/processes`, jobs, and process-graph examples.

## Sentinel Hub (`sentinelhub`) {#sentinelhub}

```text
GET https://services.sentinel-hub.com/api/v1/catalog/1.0.0/collections
```

STAC **collections** (and documented OGC WMS/WMTS layer lists) are the dataset analog. Do not harvest every STAC item/granule, Process API jobs, or EO Browser tiles. Prefer `sentinelhub` over `stacserver` on `*.sentinel-hub.com`. Sentinel Hub **openEO** backends stay `openeo` ([openEO](#openeo)).

**Keep:** Sentinel Hub **STAC collections**. **Drop:** Process API jobs, EO Browser tiles, and items/granules.

## AODN (`aodn`) {#aodn}

Australian Ocean Data Network portal search (`/portal/search` or the API path in `endpoints[]`). Keep **dataset** hits. Drop individual file downloads and the national map chrome.

```text
GET https://host/portal/search
```

**Keep:** AODN **dataset** hits. **Drop:** individual file downloads and the national map chrome.

## DataONE (`dataone`) {#dataone}

Member-node search with `formatType=DATA`. Do not crawl the coordinating node for copies of MNs already in this registry unless asked.

**Keep:** member-node search hits with `formatType=DATA`.
**Drop:** coordinating-node copies of MNs already in this registry unless asked.

```text
GET https://host/cn/v2/query/solr/?q=formatType:DATA&rows=25
```


## SciCat (`scicat`) {#scicat}

```text
GET https://host/api/v3/datasets
```

Facility datasets. Stop on `401` for complete metadata; a public list may still exist.

**Keep:** SciCat **datasets**. **Drop:** login-only complete metadata when `401`.

## IRI Data Library (`datalibrary`) {#datalibrary}

Harvest dataset nodes in `/SOURCES/` or catalog XML, not every maproom statistic view. [harvest-geoportals.md](harvest-geoportals.md#datalibrary).

**Keep:** dataset nodes in `/SOURCES/` or catalog XML.
**Drop:** maproom statistic views and every derived plot.

```text
GET https://host/SOURCES/.catalog
```


## WIS2 Box (`wis20box`) {#wis20box}

`/collections?f=json` — collections, not MQTT broker messages. [harvest-geoportals.md](harvest-geoportals.md#wis20box).

**Keep:** OGC API **collections** (`/collections?f=json`).
**Drop:** MQTT broker messages.

```text
GET https://host/collections?f=json
```


## pygeoapi (`pygeoapi`) {#pygeoapi}

Same OGC API collections grain. [harvest-geoportals.md](harvest-geoportals.md#pygeoapi).

**Keep:** OGC API **collections**.
**Drop:** items as datasets unless that is the catalog grain.

```text
GET https://host/collections?f=json
GET https://host/openapi
```


## ESGF (`esgf`) {#esgf}

Metagrid / esg-search **index** portals. Not THREDDS data nodes.

```text
GET https://host/esg-search/search?format=application%2Fsolr%2Bjson&limit=100&offset=0
```

Keep Solr **dataset** docs (`master_id` / `dataset_id`). Drop files and wget scripts. ESGF data nodes with `/thredds/catalog.xml` use the THREDDS recipe. Detail: [harvest-scientific-domain.md](harvest-scientific-domain.md#esgf).

**Keep:** Solr **dataset** docs (`master_id` / `dataset_id`). **Drop:** files, aggregations, and wget scripts.

## ESA Science Archive (`esasciencearchive`) {#esasciencearchive}

ESA Science Data Centre mission archives (Gaia, XMM-Newton, Herschel, and related ESAC TAP services).

```text
GET https://host/tap/capabilities
GET https://host/tap-server/tap/capabilities
GET https://host/tap/tables
```

Harvest TAP **tables / observation catalogs**, not every FITS file or postage-stamp cutout. Prefer VOSI `capabilities` and `tables` from `endpoints[]`. One mission archive = one harvest scope. Stop on `401`.

**Keep:** TAP **tables / observation catalogs**. **Drop:** every FITS file and postage-stamp cutout.

## Related

- [harvest.md](harvest.md)
- [harvest-geoportals.md](harvest-geoportals.md)
- [harvest-scientific.md](harvest-scientific.md)
- [harvest-scientific-domain.md](harvest-scientific-domain.md)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-incremental.md](harvest-incremental.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [agents/harvest.md](agents/harvest.md)
