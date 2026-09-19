# Harvesting datasets from geoportals

Geoportals expose **layers, collections, and ISO metadata records**, not journal articles. You still must pick the right object: a CSW record, a STAC collection, or an ArcGIS service — not a map tile, a GetMap image, or a viewer theme.

Overview: [harvest.md](harvest.md). Finding installations: [discovery-geoportals.md](discovery-geoportals.md). CSW / STAC / OGC grain: [harvest-protocols.md](harvest-protocols.md). Replace `https://host` with the catalog origin. GET only. Stop on `401`/`403`. Prefer `endpoints[]`.

## What to keep

| Keep | Drop |
|------|------|
| ISO / DCAT **dataset** or **series** metadata | `hierarchyLevel` = `service` (unless you index services separately) |
| STAC **collection** (or items if that is the catalog grain) | Individual map tiles, GetMap/GetTile images |
| GeoNode **dataset** / layer | GeoNode **maps**, geoapps, user documents |
| ArcGIS Feature/Map/Image **service** | GPServer, geocode, print, geometry, NAServer |
| OGC API / pygeoapi **collection** | `/conformance`, OpenAPI UI, HTML themes |
| One record per published dataset | The same layer again via WMS *and* WFS *and* CSW |

If GeoNetwork (or CSW) and GeoServer share a host, harvest the **catalog** (CSW/STAC), not every OWS layer as a duplicate. Viewer-only stacks: [harvest-viewers.md](harvest-viewers.md).

## One catalog per host {#one-catalog-per-host}

Match discovery: [discovery.md](discovery.md#one-catalog-per-public-product).

| Stack | Harvest this | Skip as extra datasets |
|-------|----------------|------------------------|
| GeoNetwork + GeoServer | CSW `GetRecords` dataset/series | WMS layers already in CSW |
| Palapa + GeoServer | Palapa CSW `/csw` or Palapa catalog layers | A second `geoserver` crawl of `/geoserver` |
| Lizmap / QWC2 / mviewer + QGIS Server | Viewer config or the viewer’s WMS | A second crawl of `qgis_mapserv.fcgi` |
| ArcGIS Hub + Server | Hub DCAT or Hub search | REST services already listed as Hub items |
| STAC API + Browser | `/collections` on the API | Browser HTML as a second catalog |
| openEO | `/collections` | `/processes`, jobs, a parallel `stacserver` crawl |
| MapGIS IGServer | `/igs/rest/mrcs/docs` or `/igs/rest/services` | `/igs/manager`, tiles |
| G3W-SUITE + QGIS Server | Published project WMS on the G3W portal | A second `qgisserver` crawl |
| Landfolio + ArcGIS REST | Landfolio layer/license list | REST already harvested as `arcgisserver` |
| CubeWerx CubeSERV | WMS/CSW GetCapabilities | Per-layer duplicates |
| Sentinel Hub | STAC `/api/v1/catalog` collections | Parallel `stacserver` crawl, EO Browser tiles |

## GeoNetwork (`geonetwork`) {#geonetwork}

CSW is the portable harvest. Path may be `/geonetwork/srv/eng/csw` or `/srv/eng/csw`.

```text
GET https://host/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
GET https://host/geonetwork/srv/eng/csw?service=CSW&version=2.0.2&request=GetRecords&resultType=results&outputSchema=http://www.isotc211.org/2005/gmd&typeNames=gmd:MD_Metadata&elementSetName=summary&maxRecords=50&startPosition=1
GET https://host/geonetwork/srv/eng/portal.opensearch
GET https://host/geonetwork/portal.opensearch
```

Page with `startPosition`. Keep records whose ISO `hierarchyLevel` is `dataset` or `series`. Drop `service`, `application`, and harvested **remote** catalogs listed as sources.

JSON search (GeoNetwork 3/4): `/srv/eng/q` (see `endpoints[]`) or `/srv/api/records`. Do not POST huge Elasticsearch bodies unless the user asked for GN4 search.

OAI: `/srv/eng/oaipmh?verb=Identify`. OpenSearch description is `/srv/eng/portal.opensearch` or `/portal.opensearch` on the GeoNetwork mount (and sometimes the catalog origin). Prefer CSW for harvest; OpenSearch is a dump of the same metadata.

**Keep:** ISO `hierarchyLevel` `dataset` or `series`. **Drop:** `service`, `application`, and harvested **remote** catalogs listed as sources.

## OpenWIS (`openwis`) {#openwis}

WMO OpenWIS catalogs share CSW with GeoNetwork. Harvest CSW `GetRecords` as above. Drop broker/admin HTML.

```text
GET https://host/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
GET https://host/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
```

**Keep:** CSW `GetRecords` dataset/series (same grain as GeoNetwork). **Drop:** broker/admin HTML.

## GeoNode (`geonode`) {#geonode}

```text
GET https://host/api/datasets/?limit=100&offset=0
GET https://host/api/v2/datasets/
GET https://host/catalogue/opensearch
```

GeoNode 3 uses `/api/layers/` instead of `/api/datasets/`. GeoNode 4 uses `/api/v2/datasets/`. Follow `meta.total_count`. OpenSearch description is `/catalogue/opensearch` (distinct from CSW `mode=opensearch`).

**Drop:** `/api/maps/` (compositions), `/api/geoapps/`, `/api/documents/` unless those documents are the data product, `/api/profiles/`. CSW at `/catalogue/csw` duplicates REST layers — pick one.

**Keep:** GeoNode **dataset** / layer REST objects (`/api/datasets/`, GeoNode 4 `/api/v2/datasets/`, or GeoNode 3 `/api/layers/`).

## Palapa (`palapa`) {#palapa}

Indonesian BIG simpul jaringan catalog. Prefer pycsw CSW when it answers; otherwise harvest GeoServer layers on the same host. Do not also register `/geoserver` as a second catalog.

```text
GET https://host/csw?service=CSW&version=2.0.2&request=GetCapabilities
GET https://host/csw?service=CSW&version=2.0.2&request=GetRecords&resultType=results&outputSchema=http://www.isotc211.org/2005/gmd&typeNames=gmd:MD_Metadata&elementSetName=summary&maxRecords=50&startPosition=1
GET https://host/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities
```

Keep ISO `dataset` / `series` from CSW, or WMS Layer names if CSW is absent. Drop `/gspalapa/` login, `/main/` HTML as datasets, and GeoNode `/api/datasets/` (that is `geonode`, not Palapa).

Type `/geoserver/ows` WMS 1.3.0 as `wms130`. Attach to the catalog `link`; do not prefix `/geoserver` again when the link already includes that mount.

**Keep:** ISO `dataset` / `series` from Palapa CSW (or WMS Layer names if CSW is absent). **Drop:** `/gspalapa/` login, `/main/` HTML, and GeoNode REST.

## GeoServer (`geoserver`) {#geoserver}

Register GeoServer only when it is the public catalog, not the backend behind GeoNode or Palapa. Harvest **Layer** names from WMS GetCapabilities (or REST `/geoserver/rest/layers.json` if public).

```text
GET https://host/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities
```

One Layer (or LayerGroup) = one dataset-like object. Do not also ingest every WFS FeatureType and WCS Coverage of the same name. Skip `/geoserver/web` login. OGC API: `/geoserver/ogc/features/collections` and `/geoserver/ogc/stac/v1/collections` when those endpoints exist.

**Keep:** WMS **Layer** / LayerGroup names (or OGC API collections). **Drop:** duplicate WFS FeatureTypes and WCS Coverages of the same name, and `/geoserver/web` login.

## istSOS (`istsos`) {#istsos}

OGC Sensor Observation Service. Harvest **offerings** (or procedures/stations) from SOS GetCapabilities; the service name is per-installation (`/istsos/{service}`), so take it from the registry record's `endpoints[]` or the viewer `/config/config.json` (`apiBaseUrl`, `defaultService`).

```text
GET https://host/istsos/{service}?service=SOS&version=1.0.0&request=GetCapabilities
```

One ObservationOffering (or procedure, when offerings are absent) = one dataset-like object. Do not ingest every `GetObservation` time series as a dataset. Some instances protect the raw SOS API with HTTP basic auth while serving a public istSOS-viewer front-end; register the viewer as `link` and keep the SOS URL in `endpoints[]`.

**Keep:** ObservationOffering / procedure identifiers and names. **Drop:** individual observations, `/istsos/admin` login, viewer static assets.

## CubeWerx CubeSERV (`cubewerx`) {#cubewerx}

```text
GET https://host/cubewerx/cubeserv?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
GET https://host/cubewerx/cubeserv?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
```

Typical catalog links already end in `/cubewerx/cubeserv`. Cleanup strips `/cubewerx` so those GetCapabilities query strings attach at origin and are not doubled.

Harvest **named layers** from WMS/WMTS or **ISO dataset/series** from CSW. Prefer CSW when both exist. Do not ingest the same layer from WMS and WMTS. Skip the CubeWerx demo and login-only Stratos admin.

**Keep:** ISO dataset/series from CSW, or named WMS/WMTS layers if CSW is absent. **Drop:** the same layer from both WMS and WMTS, CubeWerx demo, and Stratos admin.

## Hexagon M.App Enterprise (`mappenterprise`) {#mappenterprise}

Public `/Apps/` portal. Harvest WMS/WFS GetCapabilities or the portal’s published app/layer list. One named layer (or published app catalog entry) = one dataset analog. Do not scrape M.App tiles. Distinct from GeoMedia WebMap (`geomediawebmap`) and ERDAS APOLLO (`erdasapollo`). Viewer grain: [harvest-viewers.md](harvest-viewers.md).

**Keep:** published `/Apps/` or WMS layers. **Drop:** M.App tiles.

## ArcGIS Hub (`arcgishub`) {#arcgishub}

```text
GET https://host/api/search/v1
GET https://host/api/feed/dcat-us/1.1.json
GET https://host/data.json
```

Keep Feature Layer, Table, Shapefile, CSV, and similar **data** items. Drop Hub Site, StoryMap, Dashboard, Web Mapping Application, Domain, and people. DCAT-US `dataset` entries are the preferred grain. Same software as open data — see [harvest-opendata.md](harvest-opendata.md#arcgishub).

**Keep:** Feature Layer, Table, Shapefile, CSV, and DCAT-US **dataset** items. **Drop:** Hub Site, StoryMap, Dashboard, Web Mapping Application, Domain, and people.

## ArcGIS Server (`arcgisserver`) {#arcgisserver}

```text
GET https://host/arcgis/rest/services?f=pjson
GET https://host/arcgis/rest/info?f=pjson
```

Walk folders. Keep `FeatureServer`, `MapServer`, `ImageServer` (and `SceneServer` if you index 3D). **Drop** `GPServer`, `GeometryServer`, `NAServer`, `GeocodeServer`, `IndexingServer`, `PrintingTools`. One service URL is one dataset-like object; do not explode every layer id unless the user wants layer-level records.

**Keep:** `FeatureServer`, `MapServer`, `ImageServer` (and `SceneServer` if you index 3D).

**Drop:** `GPServer`, `GeometryServer`, `NAServer`, `GeocodeServer`, `IndexingServer`, and `PrintingTools`.

## ArcGIS Experience Builder (`experiencebuilder`) {#experiencebuilder}

Map UI first. Harvest public CSW/WMS/REST on the same host when present. Do not scrape Jimu tiles or treat each widget as a dataset. One harvest scope per public app (Experience item id or Länsstyrelsen tenant). Distinct from `webappbuilder` and `dmcity`. Viewer grain: [harvest-viewers.md](harvest-viewers.md#experiencebuilder).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#experiencebuilder)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## ArcGIS Web AppBuilder (`webappbuilder`) {#webappbuilder}

Map UI first. Harvest public REST/WMS on the same host when present. Do not scrape Web AppViewer tiles. One harvest scope per public `?id=` app. Distinct from `experiencebuilder` and `instantapps`. Viewer grain: [harvest-viewers.md](harvest-viewers.md#webappbuilder).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#webappbuilder)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## ArcGIS Dashboards (`arcgisdashboards`) {#arcgisdashboards}

Resolve the public dashboard item and harvest its referenced ArcGIS feature/map services. Charts and indicators are presentation elements, not datasets. Deduplicate services already covered by a broader Hub or REST catalog. Viewer grain: [harvest-viewers.md](harvest-viewers.md#arcgisdashboards).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#arcgisdashboards)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## ArcGIS StoryMaps (`arcgisstorymaps`) {#arcgisstorymaps}

Resolve the public story item and its referenced web maps, scenes, and ArcGIS data services. Harvest the underlying FeatureServer, MapServer, or ImageServer resources when the story is the catalog interface. Narrative blocks, images, videos, express-map annotations, and presentation sections are not datasets. Deduplicate services already covered by a broader Hub or REST catalog.

**Keep:** FeatureServer, MapServer, or ImageServer resources the story references. **Drop:** narrative blocks, images, videos, express-map annotations, and presentation sections.

## ArcGIS Instant Apps (`instantapps`) {#instantapps}

Map UI first. Harvest public REST/WMS on the same host when present. Do not scrape Instant App tiles or treat each template widget as a dataset. One harvest scope per public `appid`. Distinct from `experiencebuilder` and `webappbuilder`. Viewer grain: [harvest-viewers.md](harvest-viewers.md#instantapps).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#instantapps)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## STAC API (`stacserver`) {#stacserver}

```text
GET https://host/
GET https://host/collections
GET https://host/collections/{id}
GET https://host/api/stac/v1/
GET https://host/api/stac/v1/collections
GET https://host/api
```

Confirm STAC: landing JSON has `"conformsTo"` (or `stac_version`) and a `collections` link. Default grain: each **collection** is a dataset. Origin-link catalogs (Planetary Computer, DestinE) often mount the API at `/api/stac/v1/`. stac-fastapi `/api` is OpenAPI, not the STAC landing — type it `openapi`.

STAC **items** are granules/scenes. Harvest `/collections/{id}/items` only when the catalog’s product is item-level (small archives, not global satellite catalogs). Cap volume. `/search` is for filtered queries, not a full dump — always send `limit` and follow `links` rel `next`.

**Drop:** `conformance`, `queryables`, item assets (COGs, tiles) as datasets, and a second crawl of a STAC Browser on the same origin ([discovery.md](discovery.md#one-catalog-per-public-product)).

**Keep:** STAC **collections** (items only when that is the catalog grain).

If openEO and STAC share a host, harvest [openEO](harvest-earthdata.md#openeo) `/collections` once.

## STAC Browser (`stacbrowser`) {#stacbrowser}

HTML UI over a STAC API. Harvest the **API** `href` from the catalog JSON the browser loads (`catalog.json` / `config.js`), not the Browser HTML. If the API is already registered as `stacserver` on that origin, do not harvest twice.

**Keep:** the STAC API the browser points at (`catalog.json` / `config.js` `href`).
**Drop:** Browser HTML. Do not harvest twice if `stacserver` is already on that origin.

```text
GET https://host/catalog.json
```

Typical catalog links already end in `/catalog.json`. Cleanup strips that filename so the harvest path attaches at origin and is not doubled.


## pygeoapi (`pygeoapi`) {#pygeoapi}

OGC API Features / Records. Each collection is a dataset. Protocol grain: [harvest-protocols.md](harvest-protocols.md).

**Keep:** OGC API **collections**.
**Drop:** items as datasets unless that is the catalog grain.

```text
GET https://host/collections?f=json
GET https://host/collections/?f=json
GET https://host/openapi
```

Store `/collections?f=json` (and the trailing-slash twin) as `ogc:features` (OGC API collections grain). OpenAPI stays `pygeoapi:openapi`.

## pycsw (`pycsw`) {#pycsw}

Prefer CSW `GetRecords` or `/collections?f=json` (same grain as [pygeoapi](#pygeoapi)). Skip installer HTML. Optional OAI-PMH Identify is `/?mode=oaipmh&verb=Identify` (and `/oaipmh` on some installs). Prefer CSW for harvest; OAI is a dump.

```text
GET https://host/csw?service=CSW&version=2.0.2&request=GetCapabilities
GET https://host/collections?f=json
GET https://host/?mode=oaipmh&verb=Identify
```

Detection concatenates `?service=CSW&version=2.0.2&request=GetCapabilities` (and `?mode=oaipmh&verb=Identify`) onto catalog links that already are the CSW path (`/csw`, `/pycsw`, `/csw/v1`) so GetCapabilities is not doubled as `/csw/csw`.

**Keep:** CSW records or OGC API **collections**. **Drop:** installer HTML.

## WIS2 Box (`wis20box`) {#wis20box}

Often wraps pygeoapi. Harvest **collections**, not MQTT broker messages. Same `/collections?f=json` as [pygeoapi](#pygeoapi).

**Keep:** OGC API **collections** (`/collections?f=json`).
**Drop:** MQTT broker messages.

```text
GET https://host/collections?f=json
```

Typical catalog links already end in `/oapi`. Cleanup strips that mount so `/oapi/openapi` and `/oapi/collections/?f=json` attach at origin and are not doubled. Origin `/collections?f=json` still concatenates onto catalogs whose link is the box root.


## Lizmap (`lizmap`) {#lizmap}

```text
GET https://host/index.php/lizmap/service?repository=REPO&project=PROJECT&SERVICE=WMS&REQUEST=GetCapabilities
```

Harvest **layers in published projects**. Skip `/admin.php`. One Lizmap site may have many repositories — use the catalog `link` repository, not every sibling.

**Keep:** layers in published Lizmap projects. **Drop:** `/admin.php` and sibling repositories that are not the catalog `link`.

## Geotrek (`geotrek`) {#geotrek}

```text
GET https://host/api/v2/trek/?page_size=1
GET https://host/api/trek/json/
```

Keep **treks** (and outdoor sites / touristic contents when listed as catalog objects) from Geotrek-admin API v2 or the rando v2 `/api/trek/json/` proxy. The public catalog is Geotrek-rando; the API is often on a separate Geotrek-admin host — resolve it from the live rando config, do not guess `/admin`. Drop Geotrek-admin login, mobile apps, and widget embeds. One harvest scope per public rando portal. Viewer grain: [harvest-viewers.md](harvest-viewers.md).

**Keep:** published **treks** (and outdoor/tourism catalog objects). **Drop:** Geotrek-admin login, mobile apps, and widget embeds.

## GeoNature (`geonature`) {#geonature}

```text
GET https://host/api/searchTaxon
GET https://host/api/searchCommune
GET https://host/atlas/api/searchTaxon
GET https://host/atlas/api/searchCommune
```

Keep **species / taxon sheets** from the public GeoNature-atlas (taxon search JSON, then `/espece` sheets). Drop individual observation points, TaxHub media files, and the authenticated GeoNature back-office. One harvest scope per public atlas. Occurrence grain: [harvest-biodiversity.md](harvest-biodiversity.md).

**Keep:** public GeoNature-atlas **species / taxon sheets**. **Drop:** observation points, TaxHub media, and the authenticated back-office.

## G3W-SUITE (`g3wsuite`) {#g3wsuite}

```text
GET https://host/api/
GET https://host/group/api/
```

**Keep:** **layers in published QGIS projects** (or the portal’s public project/group list from `/api/` / `/group/api/`). **Drop:** `/admin`, G3W-ADMIN login, and guessed `/ows/{group}/{project}/` paths. Resolve group/project names from the live list; do not invent them. One portal = one harvest scope. Distinct from Lizmap (`lizmap`) and QWC2 (`qwc2`). Viewer grain: [harvest-viewers.md](harvest-viewers.md).

## GeoMapFish (`geomapfish`) {#geomapfish}

```text
GET https://host/themes
```

Theme JSON lists layers. Keep data layers; drop background/basemap-only entries if the theme is a viewer chrome. Do not scrape MapFish print.

**Keep:** data layers from `/themes`. **Drop:** background/basemap-only entries and MapFish print.

## QWC2 (`qwc2`) {#qwc2}

```text
GET https://host/themes.json
```

The theme/layer tree is the catalog. One theme is not automatically one dataset — harvest **layers** (or the documented QGIS Server WMS). Skip viewer HTML. `{tenant}.tergis.lv` QWC2 frontends are `tergis` ([harvest-viewers.md](harvest-viewers.md#tergis)).

**Keep:** **layers** in `themes.json` (or QGIS Server WMS). **Drop:** viewer HTML; `{tenant}.tergis.lv` is `tergis`.

## Mapbender (`mapbender`) {#mapbender}

Harvest WMS GetCapabilities of **published applications**, not `/application/` admin. Named layers are the dataset analog.

**Keep:** named layers in published Mapbender applications. **Drop:** `/application/` admin.

## MapServer (`mapserver`) {#mapserver}

```text
GET https://host?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
```

Detection concatenates `?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities` onto the catalog `link` (the MapServer CGI or OWS path, for example `/geomet`). Do not prefix a generic `/geomet` onto HTML viewer homepages. Origin HTML catalogs that are not the CGI return HTML and are not written.

Named layers. Do not harvest every CLASS as a dataset. If a parent CSW exists, prefer CSW. If a p.mapper UI is the public catalog (`pmapper`), harvest that instead of a second MapServer record.

**Keep:** WMS **named layers**. **Drop:** MapServer CLASS entries and a second crawl when p.mapper or CSW is the public catalog.

## p.mapper (`pmapper`) {#pmapper}

Harvest WMS GetCapabilities of the MapServer mapfile behind `/pmapper/` when public, or the p.mapper layer tree. Named layers are the dataset analog. Do not scrape map images. One harvest scope per municipality or SIT. Distinct from UMN `mapserver` as the public catalog. Viewer grain: [harvest-viewers.md](harvest-viewers.md#pmapper).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#pmapper)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## QGIS Server (`qgisserver`) {#qgisserver}

```text
GET https://host/cgi-bin/qgis_mapserv.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
GET https://host/ows?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
```

Detection concatenates `?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities` onto catalog links that already are the OWS path (for example `/belb`) so GetCapabilities is not doubled as `/belb/ows` or `/belb/cgi-bin/qgis_mapserv.fcgi`. Origin-link catalogs still use the fcgi and `/ows` probes.

Named layers from the published QGIS project. Do not harvest every style/theme as a dataset. If Lizmap, QWC2, or mviewer on the same host is the public catalog, harvest that instead.

**Keep:** named layers from the published QGIS project. **Drop:** styles/themes as extra datasets, and a second crawl when Lizmap/QWC2/mviewer is the public catalog.

## mviewer (`mviewer`) {#mviewer}

Harvest the application config XML layer list (`/apps/*.xml`) or the WMS GetCapabilities those layers point at. One named layer = one dataset analog. Skip mviewerstudio admin. Viewer grain: [harvest-viewers.md](harvest-viewers.md).

**Keep:** named layers from `/apps/*.xml` or WMS GetCapabilities. **Drop:** mviewerstudio admin.

## Isogeo (`isogeo`) {#isogeo}

```text
GET https://host/api
```

OpenAPI lists resources. Prefer ISO dataset/series records (or CSW `GetRecords` when present). Drop user accounts and empty workgroups. Distinct from IsiGéo (`isigeo`).

**Keep:** ISO dataset/series records (or CSW `GetRecords`). **Drop:** user accounts and empty workgroups.

## Geocortex Essentials (`geocortex`) {#geocortex}

```text
GET https://host/Geocortex/Essentials/REST/sites?f=pjson
```

Each Essentials **site** is one application/catalog analog. Do not scrape Html5Viewer tiles or explode every layer unless the user asked for layer-level harvest. Distinct from VertiGIS WebOffice (`weboffice`) and VertiGIS Studio Web (`vertigisstudioweb`). Viewer grain: [harvest-viewers.md](harvest-viewers.md).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Esri Geoportal (`esrigeo`) {#esrigeo}

```text
GET https://host/rest/metadata/search
GET https://host/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
GET https://host/openSearchDescription
```

Keep ISO dataset/series. OpenSearch `/opensearch?f=json` paginates with `from` / `size`. The OSDD is `{mount}/openSearchDescription` (catalog link plus `/openSearchDescription`, or `/geoportal/openSearchDescription` when the app is mounted at `/geoportal`). Drop service records.

Type `/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities` as `csw202`. Type the OSDD as `opensearch`. Attach to the catalog `link`.

**Keep:** ISO dataset/series (REST search or CSW). **Drop:** service records.

## GET SDI Portal (`getsdiportal`) {#getsdiportal}

Often a GeoServer/MapStore stack. Harvest GeoServer OWS GetCapabilities or the portal CSW, not the MapStore UI. Same OWS grain as [GeoServer](#geoserver).

```text
GET https://host/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities
GET https://host/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
```

**Keep:** GeoServer OWS GetCapabilities or portal CSW. **Drop:** MapStore UI chrome.

## Oskari (`oskari`) {#oskari}

```text
GET https://host/action?action_route=GetMapLayers&lang=en&epsg=EPSG:3067
```

Keep map layers. Hierarchical groups (`GetHierarchicalMapLayerGroups`) are folders, not extra datasets.

**Keep:** Oskari map layers. **Drop:** hierarchical groups as extra datasets.

## IRI Data Library (`datalibrary`) {#datalibrary}

Ingrid/THREDDS-style climate catalogs. Harvest dataset nodes in the library tree (`/SOURCES/` or catalog XML), not every statistic view.

**Keep:** dataset nodes in `/SOURCES/` or catalog XML.
**Drop:** maproom statistic views and every derived plot.

```text
GET https://host/SOURCES/.catalog
```


## Wagmap (`wagmap`) {#wagmap}

Japanese わが街ガイド viewers. Public GetCapabilities is often **missing or `403`**. Harvest only when a CSW/WMS/REST catalog is public. Do not scrape map tiles. Detail: [harvest-viewers.md](harvest-viewers.md#wagmap).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#wagmap)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## SonicWeb (`sonicweb`) {#sonicweb}

Japanese SonicWeb-Cloud viewers on `www.sonicweb-asp.jp/{slug}/`. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#sonicweb).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#sonicweb)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## ALANDIS+ (`alandis`) {#alandis}

Japanese ALANDIS+ public WebGIS on `webgis.alandis.jp/{tenant}/`. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#alandis).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#alandis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## GeDA-Public (`geogeo`) {#geogeo}

Japanese Geogeo.jp / GeDA-Public viewers. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geogeo).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geogeo)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Geolonia スマートマップ (`geoloniagis`) {#geoloniagis}

Japanese Geolonia スマートマップ viewers (とっとりジオマップ, 香川 BRIDGES). Distinct from Kazakhstan `smartmap`. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geoloniagis).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geoloniagis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Visor Urbano (`visorurbano`) {#visorurbano}

Mexican Visor Urbano municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#visorurbano).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#visorurbano)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Dobles Visor de Mapas (`doblesvisor`) {#doblesvisor}

Costa Rican `/comun/` Leaflet cadastral visors. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#doblesvisor).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#doblesvisor)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## GeoNube (`geonube`) {#geonube}

Argentine GeoNube Leaflet/bootleaf visors. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geonube).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geonube)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Sistema Geodados SaaS (`geodados`) {#geodados}

Brazilian Geodados SaaS municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geodados).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geodados)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Geopixel Cidades (`geopixel`) {#geopixel}

Brazilian Geopixel Cidades municipal geoportals. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geopixel).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geopixel)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## CTMGEO SigWEB (`ctmgeo`) {#ctmgeo}

Brazilian CTMGEO SigWEB municipal cadastral maps. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#ctmgeo).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#ctmgeo)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## MapMap (`mapmap`) {#mapmap}

Brazilian MapMap municipal citizen geoportals. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#mapmap). Distinct from `geodados`, `ctmgeo`, `geopixel`, and `drzwebgis`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#mapmap)). **Drop:** tiles, print PDFs, basemaps, citizen-issue reports, and login walls.

## DRZ WebGIS (`drzwebgis`) {#drzwebgis}

Brazilian DRZ WebGIS municipal cadastral maps. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#drzwebgis). Distinct from `ctmgeo`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#drzwebgis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## NieuwlandGeo Onemap (`nieuwlandonemap`) {#nieuwlandonemap}

Dutch `{org}.webgis.nl` Onemap tenants. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#nieuwlandonemap). Distinct from Singapore/NC OneMap and from `geoserver`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#nieuwlandonemap)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## KaartViewer (`kaartviewer`) {#kaartviewer}

GeoSquare `{org}.kaartviewer.nl` (and city-host) viewers. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#kaartviewer). Distinct from `geoserver` on the same estate.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#kaartviewer)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## GeoApps (`geoapps`) {#geoapps}

Dutch `{org}.geoapps.nl` public maps. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geoapps). Skip staff-login tenants.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geoapps)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## SITMUN (`sitmun`) {#sitmun}

Diputació de Barcelona `sitmun.diba.cat`. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#sitmun).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#sitmun)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## dmCity (`dmcity`) {#dmcity}

Esri Finland `web.dmcity.fi/{city}/public/` tenants. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#dmcity). Distinct from `experiencebuilder`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#dmcity)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## InfoGIS (`infogis`) {#infogis}

Infokartta `www.infogis.fi/{municipality}/` tenants. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#infogis). Distinct from `louhi` and `trimblelocus`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#infogis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Geo-IT GIS Touch Viewer (`geoitgis`) {#geoitgis}

Geo-IT `geoitgis.geo-it.be/touchviewer/` Flemish municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geoitgis). Distinct from `mapguide`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geoitgis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Zeljko GIS (`zeljkogis`) {#zeljkogis}

Zeljko d.o.o. `zeljko-gis.com` / `zopcina.zeljko-gis.com` Croatian and Bosnian municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#zeljkogis). Distinct from `mapguide`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#zeljkogis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## SIGimWeb (`sigimweb`) {#sigimweb}

Indixio SIGim Web Quebec municipal GIS (`/sigimweb/`, `/sigim/`, title `SIGimWeb`). Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#sigimweb). Distinct from `mapguide`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#sigimweb)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Geocentriq (`geocentriq`) {#geocentriq}

CIM `app.geocentriq.com/mrc/{mrc}` Quebec municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geocentriq). Distinct from `sigimweb` and `geocentralis`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geocentriq)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## GeoCentralis (`geocentralis`) {#geocentralis}

Évimbec `portail.geocentralis.com/public/sig-web/{mrc}/{code}/` Quebec municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geocentralis). Distinct from `geocentriq` and `sigale`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geocentralis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## SIGALE (`sigale`) {#sigale}

FQM/Altus `sigale.ca/Main.aspx?mrc={code}` Quebec municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#sigale). Distinct from `geocentriq` and `geocentralis`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#sigale)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## NetGIS Runtime (`netgisruntime`) {#netgisruntime}

WSP Danmark `/NetGISRuntime/basis/index.jsp` municipal viewers. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#netgisruntime). Distinct from `netgisserver`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#netgisruntime)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## GISPLAN (`gisplan`) {#gisplan}

T-MAPY `{city}.gisplan.sk`, Czech GIS4U `{muni}.gis4u.cz`, `{city}.tmapserver.cz`, or city-host Spinbox / T-WIST municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#gisplan). Distinct from `gisapp`, `iobcina`, `gepro`, `gisonline`, `mapotip`, `cgwebgis`, `mobec`, `georeal`, and `geodeticca`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#gisplan)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## mOBEC (`mobec`) {#mobec}

T-MAPY `mobec.sk/{slug}` municipal map portal. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#mobec). Distinct from `gisplan`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#mobec)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## CG WebGIS (`cgwebgis`) {#cgwebgis}

CORA GEO `webgis.{city}.sk` municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#cgwebgis). Distinct from `gisplan` and `geodeticca`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#cgwebgis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Geodeticca WEB GIS (`geodeticca`) {#geodeticca}

GEODETICCA VISION `gis.{city}.sk` municipal map client. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#geodeticca). Distinct from `cgwebgis` and `gisplan`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geodeticca)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Geoportál GEPRO (`gepro`) {#gepro}

GEPRO `{city}.obce.gepro.cz` municipal web GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#gepro). Distinct from `gisplan`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#gepro)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## KOVGIS EVALD (`evald`) {#evald}

EOMAP `evald.ee/{slug}/` municipal GIS for Estonian local governments, plus nationwide `eesti` and ELVL tenants. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#evald). Distinct from `arcgisserver` city portals. Do not harvest `service.eomap.ee` aliases or `evald2_*` session URLs.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#evald)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## terGIS (`tergis`) {#tergis}

TOPO DATI / METRUM `{tenant}.tergis.lv` territorial-planning GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#tergis). Distinct from generic `qwc2` off `tergis.lv`. Do not harvest the marketing homepage.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#tergis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## GisOnline (`gisonline`) {#gisonline}

TopGis `app.gisonline.cz/{city}` municipal map apps. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#gisonline). Distinct from `gisplan` and `gepro`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#gisonline)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## K5 MapServer (`k5mapserver`) {#k5mapserver}

MK Consult `{muni}.k5mapserver.cz` municipal geoportals. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#k5mapserver). Distinct from UMN `mapserver`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#k5mapserver)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Marushka (`marushka`) {#marushka}

GEOVAP Marushka map application server. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#marushka). Distinct from `gisplan`, `gepro`, and `georeal`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#marushka)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Georeal (`georeal`) {#georeal}

GEOREAL `{dtm|geoportal}.{kraj}.cz/portal/` kraj CMS (`Georeal.Cards`). Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#georeal). Distinct from `gisplan`, `gepro`, and `marushka`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#georeal)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Mapotip (`mapotip`) {#mapotip}

Czech `portal.mapotip.cz/{municipality}` municipal map portal. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#mapotip). Distinct from `gisplan`, `gepro`, and `gisonline`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#mapotip)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## giscity (`giscity`) {#giscity}

ibb DV-Systems `www.gisserver.de/{city}/` municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#giscity). Distinct from ArcGIS Hub `gis.cityof*` catalogs.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#giscity)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## touvia.MAPS (`touviamaps`) {#touviamaps}

vianovis `vianovis.net/{tenant}/` municipal GIS. Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#touviamaps). Distinct from `masterportal` and `vcmap`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#touviamaps)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## INGRADA online (`ingrada`) {#ingrada}

Softplan INGRADA online BürgerGIS (`Softplan.Ingrada.Mobile`). Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#ingrada). Distinct from `weboffice` and `mapguide`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#ingrada)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## VC Map (`vcmap`) {#vcmap}

Virtual City Systems VC Map (`html.vcs-ui`). Same grain as [Wagmap](#wagmap). [harvest-viewers.md](harvest-viewers.md#vcmap). Distinct from `masterportal` and `touviamaps`.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#vcmap)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## ScalarGIS (`scalargis`) {#scalargis}

WKT-SI ScalarGIS viewers (`title ScalarGIS`, `/static/viewer/`). Same grain as [Origo](harvest-viewers.md#origo). [harvest-viewers.md](harvest-viewers.md#scalargis). Distinct from older WKT CartoMapas and from `geoserver` / `geonetwork` on DGT hosts.

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#scalargis)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Origo (`origo`) {#origo}

Origosamverkan OpenLayers municipal viewers (`origo.min.js`). Same grain as [Hajk](harvest-viewers.md#hajk). [harvest-viewers.md](harvest-viewers.md#origo). Distinct from `hajk`, `mycarta`, and `geoserver` on the same host.

```text
GET https://host/index.json
GET https://host/{mapdir}/index.json
```

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#hajk)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## EWMAPA (`ewmapa`) {#ewmapa}

Polish geoportal2.pl viewers. Same grain as [Wagmap](#wagmap): harvest only public CSW/WMS/REST. Do not scrape tiles. [harvest-viewers.md](harvest-viewers.md#ewmapa).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#ewmapa)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## e-mapa.net (`emapa`) {#emapa}

Polish `*.e-mapa.net` viewers (Geo-System). Same grain as [EWMAPA](#ewmapa). Distinct from GEOBID `ewmapa`. [harvest-viewers.md](harvest-viewers.md#emapa).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#emapa)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Loftmyndir (`loftmyndir`) {#loftmyndir}

Icelandic Loftmyndir Kortasjá (`www.map.is`). Harvest public layers only. [harvest-viewers.md](harvest-viewers.md#loftmyndir).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#loftmyndir)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Alta Vefsjá (`alta`) {#alta}

Alta municipal viewers on `geo.alta.is/{tenant}/`. Not the GeoServer root. [harvest-viewers.md](harvest-viewers.md#alta).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#alta)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Bulplan UNIMAP (`bulplan`) {#bulplan}

Bulgarian `{muni}.bulplan.eu` geoportals. [harvest-viewers.md](harvest-viewers.md#bulplan).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#bulplan)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## Tobel (`tobel`) {#tobel}

Bulgarian `{city}.tobel.bg` municipal GIS. [harvest-viewers.md](harvest-viewers.md#tobel).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#tobel)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## geoportal.ch (`geoportalch`) {#geoportalch}

Swiss cantonal `www.geoportal.ch/{canton}` viewers. Distinct from mf-geoadmin3. [harvest-viewers.md](harvest-viewers.md#geoportalch).

**Keep:** public **layer / theme** list ([harvest-viewers.md](harvest-viewers.md#geoportalch)). **Drop:** tiles, print PDFs, basemaps, and login walls.

## gvSIG Online (`gvsigonline`) {#gvsigonline}

Municipal SDI over GeoServer (optional GeoNetwork). Harvest **published project layers** or GeoServer GetCapabilities on that host. Prefer CSW if GeoNetwork is public. Do not register/harvest a second GeoServer catalog for the same portal. Skip `/gvsigonline/` admin.

```text
GET https://host/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities
GET https://host/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
```

**Keep:** published project layers or GeoServer GetCapabilities. **Drop:** `/gvsigonline/` admin and a second GeoServer catalog on the same portal.

## Micka (`micka`) {#micka}

```text
GET https://host/csw?service=CSW&version=2.0.2&request=GetCapabilities
GET https://host/micka/csw?service=CSW&version=2.0.2&request=GetCapabilities
GET https://host/opensearch
GET https://host/micka/opensearch
```

Typical catalog links already end in `/micka/`. Cleanup strips `/micka` (keeping any path prefix such as `/php`) so the prefixed CSW probe is not doubled. Origin `/csw` still concatenates onto those mounts. OpenSearch is `/opensearch` or `/micka/opensearch`.

CSW GetRecords. Keep ISO `dataset` / `series`. Same grain as GeoNetwork ([harvest-protocols.md](harvest-protocols.md#csw)).

**Keep:** ISO `dataset` / `series` from Micka CSW. **Drop:** service records and installer HTML.

## HSLayers NG (`hslayersng`) {#hslayersng}

```text
GET https://host/layman-proxy/rest/workspaces/{workspace}/maps
GET https://host/rest/workspaces/{workspace}/maps
GET https://host/rest/workspaces/{workspace}/layers
```

HSLayers NG is a client framework; the harvestable catalog is the Layman backend it ships with. Typical catalog links end in `/map/` or `/mapy/`. Cleanup strips those app paths so the origin `/rest/...` and `/layman-proxy/rest/...` probes are not doubled. Workspace names are deployment-specific (`browser`, user accounts); discover them from composition URLs embedded in the hub home page (`/map?composition=https://host/rest/workspaces/<workspace>/maps/<name>`).

Map and layer listings return JSON with `access_rights`, `bounding_box`, `title`, and WMS/WFS service references. Grain: one record per map composition or per layer, not per WMS feature type. If a sibling Micka CSW (`/micka/`) exists on the same host, prefer CSW for metadata-rich records and use Layman only for the composition list.

**Keep:** Layman `maps` and `layers` items readable by `EVERYONE`. **Drop:** login-walled workspaces, the WordPress/Wagtail marketing pages around the app, and QGIS-plugin-only drafts.

## Layman (`layman`) {#layman}

```text
GET https://host/rest/workspaces/{workspace}/maps
GET https://host/rest/workspaces/{workspace}/layers
GET https://host/layman-proxy/rest/workspaces/{workspace}/maps
```

Bare Layman servers expose the same REST API without the HSLayers client. Root `/rest/` may answer 404 — probe item paths directly. Public workspaces list `read: ["EVERYONE"]` in `access_rights`. Layer items carry `file`, `db`, `wms`/`wfs` blocks; map items carry composition JSON.

**Keep:** public `maps` and `layers` items. **Drop:** the “Layman Test Client” HTML, authentication endpoints, and empty workspaces.

## deegree (`deegree`) {#deegree}

```text
GET https://host/services?service=WMS&version=1.3.0&request=GetCapabilities
GET https://host/services?service=CSW&version=2.0.2&request=GetCapabilities
GET https://host/deegree-webservices/services?service=WMS&version=1.3.0&request=GetCapabilities
GET https://host/deegree-webservices/services?service=CSW&version=2.0.2&request=GetCapabilities
```

Typical catalog links already end in `/deegree-webservices/`. Cleanup strips that servlet (keeping any path prefix) so the prefixed `/services` probes are not doubled. Leave other mounts (`/m4eu/`, `/geoproxy/`, xPlanBox) so origin `/services` concatenates onto those catalog links.

Harvest metadata records or feature types that are published datasets. Skip installer/demo and xPlanBox admin HTML.

**Keep:** published metadata records or feature types. **Drop:** installer/demo and xPlanBox admin HTML.

## ERDAS APOLLO (`erdasapollo`) {#erdasapollo}

```text
GET https://host/erdas-iws/ogc/wms/?service=WMS&request=GetCapabilities&version=1.3.0
```

Typical catalog links already end in `/erdas-iws/` or `/erdas-apollo` (sometimes with an Esri REST suffix). Cleanup strips those mounts so the harvest WMS path attaches at origin and is not doubled.

Also CSW when listed in `endpoints[]`. Keep catalog/coverage records. Drop Image Manager login and the installer.

**Keep:** catalog/coverage records (WMS or CSW). **Drop:** Image Manager login and the installer.

## NextGIS Web (`nextgisweb`) {#nextgisweb}

REST resource tree (`/api/resource/`). Keep vector/raster **layers**. Skip lookup tables, styles, and webmaps unless the user asked for maps as datasets.

```text
GET https://host/api/resource/
```

**Keep:** vector/raster **layers** from `/api/resource/`. **Drop:** lookup tables, styles, and webmaps unless the user asked for maps as datasets.

## GC2 (`gc2`) {#gc2}

MapCentia GC2 / Vidi.

```text
GET https://host/api/v2/configuration
```

Type `/api/v2/configuration` as `rest`. Harvest MapCache WMTS or WMS GetCapabilities named layers (often `/mapcache/{tenant}/wmts`). Do not treat SQL API query rows (`/api/v1/sql/{db}`) or Vidi saved projects as datasets. Skip `/admin` and the MapCentia demo.

**Keep:** MapCache WMTS or WMS named layers. **Drop:** SQL API query rows, Vidi saved projects, `/admin`, and the MapCentia demo.

## hale»connect (`haleconnect`) {#haleconnect}

CSW GetRecords (ISO `dataset` / `series`) on `/csw`. If CSW is missing, harvest published WMS/WFS feature types under `/ows/services/`. The CSW engine is often pycsw — do not harvest it as a second `pycsw` catalog on the same host. Optional OAI-PMH is `/csw?mode=oaipmh&verb=Identify`. Skip transformation projects and hale studio files.

```text
GET https://host/csw?service=CSW&version=2.0.2&request=GetCapabilities
GET https://host/ows/services/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
GET https://host/csw?mode=oaipmh&verb=Identify
```

**Keep:** ISO `dataset` / `series` from `/csw` (or WMS/WFS feature types if CSW is missing). **Drop:** a second `pycsw` catalog, transformation projects, and hale studio files.

## CoGIS (`cogis`) {#cogis}

ArcGIS-style REST under `/elitegis/rest/services`, `/arcgis3/rest/services`, or `/arcgisserver/rest/services` (`f=pjson`). Same keep/drop as [ArcGIS Server](#arcgisserver).

```text
GET https://host/elitegis/rest/services?f=pjson
GET https://host/arcgis3/rest/services?f=pjson
GET https://host/arcgisserver/rest/services?f=pjson
```

**Keep:** Feature/Map/Image services (same grain as ArcGIS Server). **Drop:** GPServer, geocode, print, and geometry.

## eLiteGIS (`elitegis`) {#elitegis}

Same REST grain as [CoGIS](#cogis) when the branded viewer is eLiteGIS.

## Other geo platforms (short)

| `software.id` | List | Filter |
|---------------|------|--------|
| `mapstore` | GeoStore `/rest/geostore/` or backend CSW (`/geoserver/csw` GetCapabilities) | Maps vs catalogs — keep catalog/dataset resources |
| `gausswebcity` | GeoServer OWS or `/geoserver/csw` on the tenant host | Same grain as MapStore; one public tenant |
| `koordinates` | `/services/api/v1.x/data/` | Data sets, not tiles |
| `terria` | init catalog JSON | Catalog members typed as data, not Magda UI chrome |
| `opendatacube` | STAC or OWS collections | Datasets/cubes, not indexer admin |
| `rasdaman` | WCS GetCapabilities | Coverages |
| `ncwms` | WMS GetCapabilities | Layers (Godiva is a viewer) |
| `pycsw` | CSW GetRecords | Dataset metadata |
| `geoblacklight` | `/catalog.json` | Geospatial items; drop books/images if mixed |
| `opengeoportal` | search API / Solr | Layers, not institutions |
| `mapapps` | `/mapapps/` is a **viewer** | Harvest the CSW/ArcGIS backend if public |
| `geocortex` | `.../REST/sites?f=pjson` | Each Essentials **site** is one application; do not scrape Html5Viewer tiles or explode every layer |
| `vertigisstudioweb` | Map UI first; `?app=` GUID is the viewer, not a dataset list | Harvest public CSW/WMS/REST on the same host; do not explode every app GUID |
| `qgisserver` | WMS GetCapabilities | Named layers; skip if Lizmap/QWC2/mviewer is the public catalog |
| `mviewer` | `/apps/*.xml` or WMS | Layers in the config, not tiles |
| `isogeo` | `/api` or CSW | ISO dataset/series, not workgroups |
| `openeo` | `/collections` | Collections, not process graphs or job results |
| `cubewerx` | `/cubewerx/cubeserv` WMS or CSW | Named layers or ISO records; not tiles |
| `mappenterprise` | `/Apps/` or WMS | Published apps/layers, not M.App tiles |
| `g3wsuite` | QGIS/OWS GetCapabilities | Layers in published projects; skip `/admin` |
| `gc2` | `/mapcache/{tenant}/wmts` GetCapabilities | Named layers, not SQL rows or Vidi projects |
| `haleconnect` | CSW GetRecords or `/ows/services/` WMS/WFS | ISO dataset/series or named layers; not pycsw as a second catalog |
| `mapgisigserver` | `/igs/rest/mrcs/docs?f=json` or `/igs/rest/services?f=json` | Map documents / services; not tiles or `/igs/manager` |
| `hygmapgis` | Mapgis layer list / OWS URL in the UI | Named layers; not tiles, not a second ArcGIS Server harvest on the same host |

Municipal viewers (cardo, NetGIS, GC Navi, NOL-IS, Masterportal, touvia.MAPS, Tianditu, Wagmap, GiSoftGis, PopGIS, ActiveMap, Geonomics, ORBISMap, HyG Mapgis, GISApp, GisMaster, LDP SIT, GFMaplet, VertiGIS Studio Web, T-MAPY GISPLAN, brain-GeoCMS): [harvest-viewers.md](harvest-viewers.md). SuperMap iServer/iPortal, MapGIS IGServer, and HyG Mapgis recipes are also on [harvest-viewers.md](harvest-viewers.md). MapProxy (`mapproxy`) is a cache — do not treat every cached layer as a new dataset if a parent SDI already lists it. Gridded EO (STAC, ODC, Rasdaman, Copernicus, ncWMS): [harvest-earthdata.md](harvest-earthdata.md). smart.finder: [harvest-viewers.md](harvest-viewers.md#smartfindersdi).

## Pagination and duplicates

- CSW: `maxRecords` + `startPosition` (or `nextRecord`).
- STAC / OGC API: `links` with `rel=next`.
- ArcGIS: folder recursion; do not follow `extent` queries as extra datasets.
- Deduplicate on fileIdentifier, layer name + host, or service URL plus catalog `uid` ([harvest-identifiers.md](harvest-identifiers.md)).

**Keep:** Feature/Map/Image services (same grain as CoGIS). **Drop:** GPServer, geocode, print, and geometry.

## OneGeo Suite (`onegeosuite`) {#onegeosuite}

Follow the deployment's linked Explorer catalog, such as
[DataSud Explorer](https://www.datasud.fr/explorer/), and retain one record per dataset,
with publisher, source identifier, license and downloadable resources. Exclude editorial
posts, map compositions and individual feature rows. The
[DataSud white-label guide](https://www.datasud.fr/portal/services/marque-blanche/)
links integration source and explains catalog filtering by organization and other facets.
Resolve actual service URLs from the deployment's published configuration or integration
code. A universal anonymous metadata API was not verified in this review; older OneGeo
API projects and component versions must not be assumed to match every installation.
Preserve access restrictions and deduplicate catalog entries shown in multiple portals.

**Keep:** one Explorer **dataset** record (publisher, source id, license, downloads). **Drop:** editorial posts, map compositions, and individual feature rows.

## PRODIGE (`prodige`) {#prodige}

Use the deployment's linked metadata catalog rather than harvesting editorial pages.
[DatARA's reuse guide](https://www.open-datara.fr/accueil/reutilisation/comment-reutiliser-les-donnees)
lists GeoNetwork CSW catalogs, an Atom download feed, WMS/WFS services and the
[PRODIGE resource API](https://catalogue.open-datara.fr/api/doc/). Keep one metadata
record per dataset identifier; distributions and spatial features belong beneath it.
The resource API documents authenticated operations and is not evidence of an anonymous
catalog listing. Only use public read operations or explicitly authorized access.
DatARA's advertised `/geonetwork/srv/fre/csw-opendata?service=CSW&request=GetCapabilities`
returned HTTP 500, `Service not found`, on 2026-09-07; do not add it as a verified working
endpoint. Discover the current metadata service from the linked catalog and apply the
[shared protocol guidance](harvest-protocols.md). No catalog API fields were changed.

**Keep:** one metadata record per dataset identifier (CSW / Atom / public read API). **Drop:** editorial pages, authenticated resource-API writes, and spatial features as extra datasets.

## Nazca4U Rapportagemodule (`nazca4u`) {#nazca4u}

Nazca soil-information tenants at `{tenant}.nazca4u.nl/rapportage/`. One harvest scope per
public tenant. The ASP.NET application has no documented public list API: bodeminformatie is
queried by address, parcel, or map selection and delivered as a PDF report by e-mail, with
linked bodemonderzoek reports where available.

**Keep:** the tenant's soil-investigation report index (linked `bodemonderzoek` documents per
parcel/layer) as dataset analogs. **Drop:** the PDF report-order flow, e-mail forms, account
pages, and basemap tiles. Do not harvest the vendor marketing site.

## ClimSeries (`climseries`) {#climseries}

FAO SWALIM climate time-series tenants (`climseries.faoswalim.org`,
`climseries.imcpuntland.so`, `www.imcsomaliland.org/climseries/station/`). One harvest scope
per tenant. Station groups are listed under `/station/map/{aws,mrs,ss,gws}/` with per-station
tables and CSV downloads.

**Keep:** each **station** (with its time-series download) as one dataset analog; station-group
pages as the list source. **Drop:** dashboard charts, map tiles, and the download request form
itself. Keep the three tenants as separate catalogs; do not merge them into the FAO SWALIM record.

## GISNET V5 (`gisnet`) {#gisnet}

Complot municipal GIS tenants at `v5.gis-net.co.il/v5/{authority}/` and `mg{1,2}.gis-net.co.il/{Authority}Gis`.
One harvest scope per public tenant. The JS viewer has no documented public list API: layers are
browsed in the TOC and queried by parcel, address, or plan.

**Keep:** the tenant's published layer list (parcels, plans, engineering layers) as map-layer
dataset analogs. **Drop:** basemap tiles, print/share tools, and the embedded Google Street View.
The host geo-blocks some non-IL networks; harvest from an IL-reachable network.

## Taldor MapExpert (`mapexpert`) {#mapexpert}

Taldor municipal GIS tenants at `gis{NN}.taldor.co.il/{City}Gis`. One harvest scope per public
tenant. The viewer has no documented public list API; a WAF answers 403 to non-browser clients.

**Keep:** the tenant's published layer list as map-layer dataset analogs. **Drop:** basemap tiles
and UI chrome. Harvest needs a browser-like client or an IL-reachable network.

## SWIMS (`swims`) {#swims}

FAO SWALIM water-source tenants (`swims.faoswalim.org`, `pwsims.imcpuntland.so`). One harvest
scope per tenant. The dashboard pairs an operational LiveMap with a tabular water-source
inventory (boreholes, dug wells, dams, berkads, springs).

**Keep:** each **water-source record** in the inventory table (with functioning status, quality
analytics, and survey metadata) as one dataset analog; the inventory table as the list source.
**Drop:** dashboard charts, map tiles, and user-account pages. ClimSeries and FRRIMS on the same
hosts are separate applications — do not merge.

## GovPilot GIS Map (`govpilot`) {#govpilot}

GovPilot tenants at `map.govpilot.com/map/{state}/{city}`. One harvest scope per public tenant.
The Kendo ASP.NET viewer has no documented public list API.

**Keep:** the tenant's published layer list (parcels, zoning, administrative layers) as map-layer
dataset analogs. **Drop:** basemap tiles and UI chrome. Do not harvest the vendor marketing site.

## MapSifter (`mapsifter`) {#mapsifter}

TerraScan county parcel tenants at `{county}-mapsifter.publicaccessnow.com` (and legacy
`{county}.mapsifter.com`). One harvest scope per public tenant. The ASP.NET application sits
behind a `Disclaimer.aspx` gateway and has no documented public list API.

**Keep:** parcel search results (parcel number, owner, address, assessment, zoning) as dataset
analogs where bulk terms allow. **Drop:** the disclaimer gateway, print pages, and basemap tiles.
Bare subdomain guesses may hit an AWS ALB `Target Group Heartbeat` default — not a tenant.

## Civil Solutions Tax Map Viewer (`civiltmv`) {#civiltmv}

Civil Solutions / ARH tenants at `tmv.civilsolutions.biz/viewer/{tenant-id}`. One harvest scope
per public tenant. The Mazer viewer has no documented public list API: tax maps are searched by
block/lot, address, or map sheet and parcel details render in a side panel.

**Keep:** each **tax map sheet** (with its parcel detail extract) as one dataset analog; the
map-sheet index as the list source. **Drop:** the viewer UI, key-map navigation, and basemap
tiles. Do not harvest the vendor site.

## IDEBA Visualizador (`ideba`) {#ideba}

IDEBA municipal tenants at `visualizador.ideba.gba.gob.ar/{municipio}`. One harvest scope per
tenant. The Leaflet viewer is backed by per-tenant GeoServer workspaces at
`geoserver-nodo2.ideba.gba.gob.ar/geoserver/{municipio}/wfs|wms` — use the standard GeoServer
layer listing as the list source.

**Keep:** each **GeoServer layer** in the tenant workspace as one map-layer dataset analog.
**Drop:** basemap tiles, measure/locate tools, and the province-level portal pages.

## Intertown UP (`intertownup`) {#intertownup}

Intertown UP tenants at `up.intertown.co.il/{code}/public/`. One harvest scope per public
tenant. The React SPA has no documented public list API; layers load from the tenant config.

**Keep:** the tenant's published layer list as map-layer dataset analogs. **Drop:** the
login-only `/org/` systems, basemap tiles, and UI chrome.

## GeoMixer / Kosmosnimki (`geomixer`) {#geomixer}

One harvest scope per GeoMixer map (the `window.defaultMapID` in `config.js`, or the map
loaded by `index.html`). The layer tree is available from the GeoMixer REST API
(`/api/` on the portal host); ScanEx portals such as `www.kosmosnimki.ru` and `fires.ru`
publish many layers, while thematic sites (warfly.ru, huntmap.kz, оопт.рф) serve a
single curated layer set. `search.kosmosnimki.ru` is an imagery archive catalog: scene
footprints and acquisition metadata, not downloadable rasters.

**Keep:** each **layer in the map's layer tree** as one map-layer dataset analog; for
`search.kosmosnimki.ru`, each **satellite program catalog** (GeoEye, Ikonos, QuickBird,
WorldView, Eros) as one dataset analog. **Drop:** basemap tiles, the geomixer.js client,
and vendor demo maps.

## Atlas (`atlas`) {#atlas}

Atlas (Purmerend Common Ground geoportal) tenants on municipal hosts. One harvest scope per
tenant. The Vue/Django app serves WMS, WFS, WMTS, and vector-tile layers; there is no
documented catalog list API on the tenant URL.

**Keep:** the tenant's published layer list as map-layer dataset analogs. **Drop:** basemap
tiles and UI chrome.

## Mappi (`mappi`) {#mappi}

Mappi (Swis) tenants at `kaart.{city}.nl`. One harvest scope per tenant. Each published map is
a GeoJSON FeatureCollection at `/api/maps/{id}.json`; there is no documented map-index list
API, so enumerate map ids from the tenant's page or menu config.

**Keep:** each **published map** (`/api/maps/{id}.json`) as one dataset analog. **Drop:** the
editorial page chrome and basemap tiles. Do not harvest event maps (kaart.marathon.nl).

## geoCore (`geocore`) {#geocore}

One harvest scope per geoCore portal (the deployment's `GEOCORE_API_DOMAIN`, e.g.
`https://geocore.api.geo.ca` for GEO.ca). The REST API is enumerable: bbox search
`GET /geo?north=90&south=-90&east=180&west=-180&lang=en&min={offset}&max={limit}` returns
`Items` with `total` for paging; record detail is `GET /id?id={uuid}&lang=en`. Records are
extended GeoJSON; `options` is a doubly-escaped JSON string of `{protocol, name, url}`
distribution links (HTTPS downloads, WMS, ESRI REST, HTML pages). Avoid `GET /featured`
(Lambda payload limit). [API docs](https://canadian-geospatial-platform.github.io/geocore/docs/api-documentation/).

**Keep:** each **metadata record** (`id` UUID) as one dataset analog; use `options[].url`
as distributions and `topicCategory` as theme. **Drop:** `/analytics/*` endpoints,
saved-search/community endpoints (API-key only), and the GeoView viewer chrome.

## Related

- [harvest.md](harvest.md)
- [harvest-opendata.md](harvest-opendata.md) (ArcGIS Hub as open data)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-viewers.md](harvest-viewers.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [harvest-incremental.md](harvest-incremental.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [discovery-geoportals.md](discovery-geoportals.md)
- [apidetect.md](apidetect.md)

