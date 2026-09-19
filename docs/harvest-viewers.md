# Harvesting map viewers and tile caches

Many geoportals in this registry are **viewers** (QWC2, Masterportal, Lizmap, mviewer, Wagmap, Tianditu, Trimble Locus / Louhi / Landfolio, dmCity, InfoGIS, Spatial Suite, Spectrum Spatial Analyst, Exponare, KortInfo, IntraMaps Public, LocalMaps, GEUSMAP, GISApp, GeneGIS PAGIS, GisMaster, LDP SIT, GFMaplet, HyG Mapgis, SmartMap, SmartGIS, VKOMAP, Visor Urbano, Dobles Visor de Mapas, ISY Map, Avinet Adaptive, iObčina, iShare, Cadcorp, StatMap Earthlight, VertiGIS Studio Web, ArcGIS Experience Builder, ArcGIS Web AppBuilder, ArcGIS Dashboards, ArcGIS Instant Apps, Argenmap, AvanMap, WebEWID, KC WebGIS, Hajk, Origo, Tailormap, myCarta, AddSpatial, T-MAPY GISPLAN, CG WebGIS, Geodeticca WEB GIS, Geoportál GEPRO, GisOnline, K5 MapServer, Marushka, Georeal, Mapotip, giscity, touvia.MAPS, INGRADA online, CAIGOS Globe, VC Map, XY Maps, Pozi, JMap, GIS Cloud, MRF Web Map, MuniSight, p.mapper, CommunityView, MS-GIS, Weave, OVIE, SOFTPRO, MxSIG, DIGITAL TWIN CLOUD). The catalog of datasets is the **layer list** (GetCapabilities, `themes.json`, REST services) — not PNG tiles, print PDFs, or the basemap.

Use this page when `software.id` is a viewer or cache. Full SDI catalogs (GeoNetwork, GeoNode, ArcGIS Server): [harvest-geoportals.md](harvest-geoportals.md). Protocol grain: [harvest-protocols.md](harvest-protocols.md). GET only. Stop on `401`/`403`. Do not scrape tiles.

## Rule

1. If CSW, STAC, or ArcGIS REST exists on the same host, harvest **that** ([harvest-geoportals.md](harvest-geoportals.md)).
2. Else harvest WMS/WMTS/WFS **GetCapabilities** named layers, or the viewer’s JSON theme/layer tree.
3. One named layer (or published service) = one dataset analog. Do not ingest the same layer from WMS and WMTS.
4. Stop if GetCapabilities is `403` or missing — common for Wagmap and EWMAPA.

## Lizmap, QWC2, GeoMapFish, Mapbender, MapServer, QGIS Server, mviewer

Published project/theme **layers**. Recipes: [harvest-geoportals.md](harvest-geoportals.md) (`lizmap`, `qwc2`, `geomapfish`, `mapbender`, `mapserver`, `qgisserver`, `mviewer`). Skip `/admin.php`, mviewerstudio, and MapFish print.

## Masterportal (`masterportal`) {#masterportal}

Hamburg LGV viewer. Harvest `config.js` / portal JSON **layer tree** (or the WMS the config points at). One theme is not automatically one dataset. Do not scrape `lgv-config` tiles. Distinct from vianovis touvia.MAPS (`touviamaps`) and VC Map (`vcmap`).

**Keep:** config.js / portal JSON **layer tree** (or the WMS it points at). **Drop:** `lgv-config` tiles; one theme is not automatically one dataset.

## touvia.MAPS (`touviamaps`) {#touviamaps}

`vianovis.net/{tenant}/` or a city host loading `touvia.de/scripts/loader.js`. Harvest the public **theme / layer tree** if unauthenticated. Do not scrape Cesium/Google 3D tiles. One harvest scope per municipality or Landkreis. Distinct from `masterportal` and `vcmap`.

**Keep:** public **theme / layer tree** if unauthenticated. **Drop:** Cesium/Google 3D tiles.

## INGRADA online (`ingrada`) {#ingrada}

Softplan `INGRADA online` BürgerGIS (`Softplan.Ingrada.Mobile`, `/mobile/message-channel.js`). Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per municipality or Landkreis. Distinct from `weboffice`, `mapguide`, and CAIGOS Globe (`caigos`). Skip CMS BürgerGIS landing pages.

**Keep:** public **layer / theme list** if unauthenticated. **Drop:** map tiles and staff-login walls.

## CAIGOS Globe (`caigos`) {#caigos}

CAIGOS GmbH Globe / Geoportal splash (`cmd=wafdownload`, `CAIGOS-Globe`). Harvest the public **layer / theme list** if unauthenticated, or WMS GetCapabilities when the tenant publishes it. Do not scrape `wafdownload` map tiles or require a staff login. One harvest scope per municipality, Landkreis, or Land public viewer. Distinct from `geoportalrlp` and `ingrada`. Skip intern/SBL copies, training RAUM+Monitor, and utility Planauskunft logins.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## VC Map (`vcmap`) {#vcmap}

Virtual City Systems `html.vcs-ui` / title `VC Map`. Harvest the public **layer / theme tree** if unauthenticated. Do not scrape Cesium 3D tiles or point clouds. One harvest scope per city or Landkreis app. Distinct from `masterportal` and `touviamaps`.

**Keep:** public **layer / theme tree** if unauthenticated. **Drop:** Cesium 3D tiles and point clouds.

## MapStore (`mapstore`) {#mapstore}

GeoStore `/rest/geostore/` or backend CSW. Keep catalog/dataset resources. Drop saved **maps** and the MapStore UI chrome unless the user asked for maps.

**Keep:** catalog/dataset resources from GeoStore or backend CSW. **Drop:** saved maps and MapStore UI chrome unless asked.

## GAUSS WebCity (`gausswebcity`) {#gausswebcity}

GAUSS MapStore tenants (`{org}.gis.ba`, city hosts with `/webcity/`). Harvest GeoServer OWS GetCapabilities or CSW on the same host. Do not scrape MapStore UI chrome or treat each saved map as a dataset. One harvest scope per public tenant. Distinct from generic `mapstore` and from VertiGIS WebOffice branded WebCity (`weboffice`). Skip `gis.ba/webcity/` vendor demo.

**Keep:** GeoServer OWS GetCapabilities or portal CSW. **Drop:** MapStore UI chrome, saved maps, and login-only `/registered/` shells.

## Terria (`terria`) {#terria}

Init `catalog.json` / `config.json` **members typed as data**. If Magda or CKAN on the same host already lists those datasets, harvest CKAN/Magda instead.

**Keep:** init `catalog.json` / `config.json` members typed as data. **Drop:** Magda UI chrome; harvest CKAN/Magda instead when they already list those datasets.

## GeoBlacklight (`geoblacklight`) {#geoblacklight}

```text
GET https://host/catalog.json
GET https://host/catalog/opensearch.xml
```

Geospatial items. Drop books/images when the Solr mix includes them. Page `start` / `rows` as in Blacklight.

**Keep:** geospatial **items** from `/catalog.json`. OpenSearch is `/catalog/opensearch.xml`. **Drop:** books/images when the Solr mix includes them.

## OpenGeoPortal (`opengeoportal`) {#opengeoportal}

Search/Solr **layers**, not institutions. Legacy paths vary — use `endpoints[]`.

**Keep:** search/Solr **layers**. **Drop:** institutions; use `endpoints[]` when legacy paths vary.

## Koordinates (`koordinates`) {#koordinates}

```text
GET https://host/services/api/v1.x/data/
```

Data sets, not tile URLs.

**Keep:** Koordinates **data sets** (`/services/api/v1.x/data/`). **Drop:** tile URLs.

## MapTiler Server (`maptilerserver`) {#maptilerserver}

```text
GET https://host/api
```

Harvest **maps / styles** the public catalog lists. Bare `/api/maps` 404s on some versions. Skip `/admin` and `logoOnly` tile backends. Do not harvest every XYZ tile.

**Keep:** public **maps / styles**. **Drop:** `/admin`, `logoOnly` tile backends, and every XYZ tile.

## MapProxy (`mapproxy`) {#mapproxy}

WMTS/WMS GetCapabilities on the cache. Treat layers as datasets **only** if no parent SDI lists them. Most MapProxy instances duplicate GeoServer/MapServer — prefer the origin catalog.

**Keep:** WMTS/WMS GetCapabilities layers only when no parent SDI lists them. **Drop:** duplicate GeoServer/MapServer origin catalogs.

## Tianditu (`tianditu`) {#tianditu}

Provincial/municipal 天地图 nodes. Harvest the node’s **layer/catalog API** if public. Skip pure tile hosts (`t0.tianditu.gov.cn` … `t7`), JS API keys (`tk=`), and `api.tianditu.gov.cn` token calls. One node = one harvest scope.

Backends vary; use `endpoints[]` when present. Common public catalogs:

```text
GET https://host/iserver/services.json
GET https://host/iportal/web/services.json
GET https://host/arcgis/rest/services?f=pjson
GET https://host/api/cityNode/queryByTree.json
```

Keep SuperMap services, iPortal maps/services, ArcGIS Map/Feature/Image services, or the city-node tree. Detection probes `/api/cityNode/queryByTree.json` on the node origin (plus the SuperMap/ArcGIS paths above). Drop SSO, `console.tianditu.gov.cn` developer pages, and WMTS GetTile URLs.

**Keep:** node **layer/catalog API** (iServer/iPortal/ArcGIS/city-node tree). **Drop:** pure tile hosts (`t0`–`t7`), `tk=` keys, SSO, and GetTile URLs.

## VertiGIS WebOffice (`weboffice`) {#weboffice}

Map UI first. Harvest CSW/WMS/REST when public. Do not scrape city-plan tiles.

**Keep:** public CSW/WMS/REST on the same host. **Drop:** city-plan tiles.

## VertiGIS Studio Web (`vertigisstudioweb`) {#vertigisstudioweb}

Map UI first. App configuration is an ArcGIS Online / Portal item launched with `?app={guid}`. Harvest public CSW/WMS/REST on the same host when present. Do not treat each `?app=` GUID as a dataset, and do not scrape tiles. Distinct from Geocortex Essentials (`geocortex`) Sites Directory / Html5Viewer and VertiGIS WebOffice (`weboffice`). One harvest scope per public tenant.

**Keep:** public CSW/WMS/REST on the same host. **Drop:** each `?app=` GUID as a dataset, and tiles.

## Geocortex Essentials (`geocortex`) {#geocortex}

List sites from the Essentials REST Sites Directory (`GET .../REST/sites?f=pjson`). Keep public sites as catalog applications. Drop Html5Viewer tiles, print PDFs, and per-layer identify results. If ArcGIS REST on the same host is already harvested, do not duplicate those services.

**Keep:** public Essentials **sites** (`/REST/sites?f=pjson`). **Drop:** Html5Viewer tiles, print PDFs, per-layer identify, and duplicate ArcGIS REST already harvested.

## ArcGIS Experience Builder (`experiencebuilder`) {#experiencebuilder}

Map UI first. App configuration is an ArcGIS Online / Portal item (or a Länsstyrelsen WebbGIS tenant). Harvest public CSW/WMS/REST on the same host when present. Do not scrape Jimu tiles or treat each widget as a dataset. One harvest scope per public app. Distinct from `webappbuilder` and `dmcity`.

**Keep:** public CSW/WMS/REST on the same host. **Drop:** Jimu tiles and each widget as a dataset.

## ArcGIS Web AppBuilder (`webappbuilder`) {#webappbuilder}

Map UI first. Hosted apps and exported self-hosted Jimu builds use the same grain. Harvest public REST/WMS on the same host when present. Do not scrape Web AppViewer tiles. One harvest scope per public app. Distinct from `experiencebuilder` and `instantapps`.

**Keep:** public REST/WMS on the same host. **Drop:** Web AppViewer tiles.

## ArcGIS Dashboards (`arcgisdashboards`) {#arcgisdashboards}

Dashboard UI first. Resolve the public ArcGIS dashboard item, then harvest the referenced public feature/map services through ArcGIS REST. Do not turn charts, indicators, selectors, or widgets into datasets. One harvest scope per dashboard item; deduplicate services already harvested from a broader `arcgisserver` or `arcgishub` catalog.

**Keep:** referenced public Feature/Map services. **Drop:** charts, indicators, selectors, widgets, and services already harvested as `arcgisserver`/`arcgishub`.

## ArcGIS Instant Apps (`instantapps`) {#instantapps}

Map UI first. Harvest public REST/WMS on the same host when present. Do not scrape Instant App tiles. One harvest scope per public `appid`. Distinct from `experiencebuilder` and `webappbuilder`.

**Keep:** public REST/WMS on the same host. **Drop:** Instant App tiles.

## Argenmap (`argenmap`) {#argenmap}

Read the public JSON layer configuration used by the Argenmap `src/js/` client. Harvest named overlay layers or their WMS/WMTS service metadata; omit the IGN basemap, drawing tools, and tile requests. One harvest scope per institutional deployment.

**Keep:** named overlay layers or their WMS/WMTS metadata. **Drop:** IGN basemap, drawing tools, and tile requests.

## AvanMap (`avanmap`) {#avanmap}

Harvest the public municipal layer tree exposed through the `/AvanMap/` client, or WMS/WFS GetCapabilities when published. Do not scrape tiles, cadastral identify responses, or generated report documents. One harvest scope per municipality deployment.

**Keep:** public municipal layer tree (`/AvanMap/`) or WMS/WFS GetCapabilities. **Drop:** tiles, cadastral identify responses, and generated reports.

## WebEWID (`webewid`) {#webewid}

Harvest the public Portal Mapowy layer list or an authority's public WFS GetCapabilities. Prefer the WFS feature-type catalog when available. Do not crawl authenticated surveyor, appraiser, or document portals, and do not ingest individual cadastral parcels as datasets. One harvest scope per authority.

**Keep:** public Portal Mapowy layer list or WFS feature-type catalog. **Drop:** authenticated surveyor/document portals and individual cadastral parcels.

## KC WebGIS (`kcwebgis`) {#kcwebgis}

Harvest the public BürgerGIS theme/layer list from the `/BMApp/` configuration, or public WMS/WFS GetCapabilities when present. Do not scrape tiles, offline packages, field-edit endpoints, or citizen-report records. One harvest scope per public municipality or Landkreis project.

**Keep:** public BürgerGIS theme/layer list or WMS/WFS GetCapabilities. **Drop:** tiles, offline packages, field-edit endpoints, and citizen-report records.

## Cadenza (`cadenza`) {#cadenza}

Map UI first. Harvest CSW/WMS/REST when public. Do not scrape workbook tiles.

**Keep:** public CSW/WMS/REST. **Drop:** workbook tiles.

## MangoMap (`mangomap`) {#mangomap}

Public MangoMap layer/catalog list if unauthenticated. Stop on `401`. Do not scrape map tiles.

**Keep:** public MangoMap layer/catalog list if unauthenticated. **Drop:** map tiles; stop on `401`.

## map.apps (`mapapps`) {#mapapps}

`/mapapps/` is a viewer — follow the backend catalog (CSW/ArcGIS). Do not scrape city-plan tiles.

**Keep:** the backend CSW/ArcGIS catalog the viewer points at. **Drop:** city-plan tiles and `/mapapps/` chrome as datasets.

## MapSolution (`mapsolution`) {#mapsolution}

`/MapSolution/apps/home/welcome` is a viewer catalog — harvest public guest map/layer lists or the ArcGIS/WMS backend. Do not scrape tiles or login-only ALKIS clients.

**Keep:** public guest map/layer lists or backend WMS/REST. **Drop:** tiles, print PDFs, and staff-only MapSolution Kommunal / Geoportal-Plus apps.

## GeoMoose (`geomoose`) {#geomoose}

GeoMoose viewers are MapServer-backed. Harvest the layer catalog from the app config (`config.js` mapbook / map-sources) or the backend WMS GetCapabilities (`/cgi-bin/mapserv`). Do not scrape tiles.

**Keep:** mapbook map-source/layer list and WMS GetCapabilities layers. **Drop:** base-map tiles and viewer chrome (identify/search/select services are not datasets).

## MiraMon (`miramon`) {#miramon}

MiraMon Map Browser instances are configured by a declarative `config.json` (layer list, WMS/WMTS/SOS sources); server roots list collections as `cgi-bin/{collection}/MiraMon.cgi`. Harvest the `config.json` layer catalog or the per-collection WMS GetCapabilities (`cgi-bin/{collection}/MiraMon.cgi?REQUEST=GetCapabilities&SERVICE=WMS`). Do not scrape map tiles.

**Keep:** `config.json` layer/service list and WMS/WMTS GetCapabilities layers. **Drop:** base-map tiles, storymap chrome, and `index.htm` viewer scaffolding.

## Wagmap (`wagmap`) {#wagmap}

GetCapabilities often missing or `403`. Harvest only a public CSW/WMS/REST catalog. Do not scrape わが街ガイド tiles.

**Keep:** public CSW/WMS/REST when GetCapabilities is present. **Drop:** わが街ガイド tiles; stop if GetCapabilities is `403` or missing.

## EWMAPA (`ewmapa`) {#ewmapa}

Polish geoportal2.pl. Same grain as [Wagmap](#wagmap): harvest only public CSW/WMS/REST. Do not scrape tiles.

**Keep:** public CSW/WMS/REST. **Drop:** geoportal2.pl tiles.

## e-mapa.net (`emapa`) {#emapa}

Polish `*.e-mapa.net` SIP viewers (Geo-System Pandora). Same grain as [EWMAPA](#ewmapa): harvest only public CSW/WMS/REST. Do not scrape tiles. Distinct from `ewmapa`.

**Keep:** public CSW/WMS/REST. **Drop:** e-mapa.net tiles.

## Loftmyndir (`loftmyndir`) {#loftmyndir}

Icelandic `www.map.is/{muni}/` viewers. Harvest a public layer list or GetCapabilities if present. Do not scrape map tiles.

**Keep:** public layer list or GetCapabilities if present. **Drop:** map tiles.

## Alta Vefsjá (`alta`) {#alta}

`geo.alta.is/{tenant}/` OpenLayers viewers. Harvest the public layer list. Do not harvest the GeoServer root here — that record is `geoserver`.

**Keep:** public layer list on `geo.alta.is/{tenant}/`. **Drop:** the GeoServer root (`geoserver`).

## Bulplan UNIMAP (`bulplan`) {#bulplan}

`{muni}.bulplan.eu` municipal geoportals. Harvest public layers or GetCapabilities. Do not scrape tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Tobel (`tobel`) {#tobel}

`{city}.tobel.bg` municipal GIS. Same grain as [Bulplan UNIMAP](#bulplan).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## geoportal.ch (`geoportalch`) {#geoportalch}

Swiss `www.geoportal.ch/{canton}` viewers. Harvest a public layer list or WMS. Distinct from [mf-geoadmin3](#mfgeoadmin3).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## InGrid (`ingrid`) {#ingrid}

German InGrid. **Confirm:** `/user/themes/ingrid/` plus `ingrid.js` on a Geoportal (Eisenbahn-Bundesamt GeoPortal). Do **not** set `ingrid` on a Scientific data repository even when the chrome matches (BAW `datenrepository.baw.de` — `ingrid` would force Geoportal).

CSW:

```text
GET https://host/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
GET https://host/interface/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
```

Keep ISO dataset/series. [harvest-protocols.md](harvest-protocols.md#csw).

**Keep:** ISO `dataset` / `series` from InGrid CSW. **Drop:** service records, installer HTML, and scientific IRs that only share InGrid chrome.

## IsiGéo (`isigeo`) {#isigeo}

Geomatika SDI. Harvest `/api` if it lists layers/datasets; otherwise WMS GetCapabilities on the published workspace.

**Keep:** `/api` layer/dataset list or WMS GetCapabilities on the published workspace. **Drop:** admin HTML.

## MetaGIS (`metagis`) {#metagis}

```text
GET https://host/ResultJSONGNServlet
```

JSON layer/search results. Skip HTML search chrome.

**Keep:** JSON layer/search results (`ResultJSONGNServlet`). **Drop:** HTML search chrome.

## smart.finder SDI (`smartfindersdi`) {#smartfindersdi}

CSW or finder search. Keep ISO dataset/series metadata. Skip admin and the installer.

**Keep:** ISO `dataset` / `series` from CSW or finder search. **Drop:** admin and installer HTML.

## MapBiomas (`mapbiomas`) {#mapbiomas}

Harvest annual land-cover **collections** on the country/program node. Do not treat every map click or year slider state as a dataset.

**Keep:** annual land-cover **collections** on the country/program node. **Drop:** every map click or year-slider state.

## CARTO (`carto`) {#carto}

Government/org Builder tenants only. Public named maps/datasets if the SQL or Maps API is unauthenticated. Stop on API keys (`401`). Do not `SELECT` every table. Skip carto.com marketing.

**Keep:** public named maps/datasets when SQL/Maps API is unauthenticated. **Drop:** every SQL table, API-key `401` walls, and carto.com marketing.

## SuperMap iServer (`supermapiserver`) {#supermapiserver}

```text
GET https://host/services.json
GET https://host/iserver/services.json
```

Keep published **datasets/services**. Drop tiles and admin.

**Keep:** published **datasets/services** from `/services.json`. **Drop:** tiles and admin.

## SuperMap iPortal (`supermapiportal`) {#supermapiportal}

```text
GET https://host/services.json
GET https://host/iserver/services.json
GET https://host/iportal/web/services.json
GET https://host/iportal/web/maps.json
GET https://host/iportal/web/datas.json
```

Typical catalog links already end in `/iportal`. Cleanup strips `/iportal` so those JSON paths attach at origin and are not doubled.

Same `services.json` grain as [iServer](#supermapiserver) when the public product is iPortal. Maps and datasets lists are `/iportal/web/maps.json` and `/iportal/web/datas.json`. Drop tiles and admin.

**Keep:** iPortal/iServer **maps/services**. **Drop:** tiles and admin.

## EV-Globe (`evglobe`) {#evglobe}

```text
GET https://host/earthview/server/manager/index.html
```

EV-Server 7 manager is a login-gated admin SPA (umi + Cesium). There is no known unauthenticated service-list JSON. Harvest only when a tenant publishes public OGC endpoints from its `ogcserver` microservice — then keep **WMS/WFS GetCapabilities layers**. Drop the manager console, tile services (`etmserver`, `emvtserver`, `arctileserver`, `mbtileserver`), and bare-IP instances.

**Keep:** public OGC **layers** when exposed. **Drop:** manager console, tiles, bare IPs.

## MapGIS IGServer (`mapgisigserver`) {#mapgisigserver}

```text
GET https://host/igs/rest/mrcs/docs?f=json
GET https://host/igs/rest/services?f=json
```

Keep published **map documents** (IGS 1.0) or **services** (IGS 2.0). Drop tiles, `/igs/manager` admin, and GetMap images. IGS 2.0 `/igs/rest/services` looks like ArcGIS REST — harvest it as MapGIS when the path is `/igs/rest/`, not `/arcgis/rest/`. Colombian HyG `/mapgis/mapa.jsp` is [`hygmapgis`](#hygmapgis), not this recipe.

**Keep:** `/igs/rest/mrcs/docs` or `/igs/rest/services` documents. **Drop:** `/igs/manager` and tiles.

## GEOVIS (`geovis`) {#geovis}

GEOVIS Earth / 星图地球 portals are Cesium + mapbox-gl SPAs (`geovis-mapbox-sdk.js`). Harvest the portal's public **imagery/dataset catalog entries** when a catalog JSON is exposed; keep dataset and imagery-scene records. Drop Cesium tile/terrain endpoints, basemaps, and vendor marketing pages.

**Keep:** imagery/dataset **catalog entries**. **Drop:** tiles, terrain, basemaps.

## CityMaker (`citymaker`) {#citymaker}

Legacy Gvitech 3D GIS viewers titled `{name}三维地理信息系统`. No known public list API; harvest the viewer's **layer/scene list** only when exposed in a public config or menu. Drop ActiveX/plugin installers, tiles, and login-gated admin.

**Keep:** public **layer/scene list**. **Drop:** plugin installers, tiles, admin.

## PIE-Engine (`pieengine`) {#pieengine}

Piesat remote-sensing cloud platform. Harvest the public **dataset catalog** of a PIE-Engine portal when reachable; keep satellite imagery and geospatial datasets. Drop processing-job/user consoles and `*-obs.piesat.cn` object-storage infra. The flagship `engine.piesat.cn` is CN-geo-fenced — harvest from a CN network.

**Keep:** **datasets** / imagery scenes. **Drop:** job consoles, OBS storage, tiles.

## HyG Mapgis (`hygmapgis`) {#hygmapgis}

H&G Consultores `/mapgis/mapa.jsp?aplicacion=` or `/mapgis9/mapa.jsp?aplicacion=` viewer. Harvest the public **layer list** or OWS/ArcGIS URL exposed in the UI. Do not scrape map tiles. One harvest scope per `aplicacion=` on that host. If ArcGIS REST on the same Mapgis host is already harvested as `arcgisserver`, do not duplicate those services. Do not harvest Medellín `/mapgis9/` as a second catalog when GeoNetwork on `www.medellin.gov.co` is the public product. Not Zondy `/igs/rest/` (`mapgisigserver`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## cardo (`cardo`) {#cardo}

Public UI under `/net3/public/`; WMS if published. Skip intranet cardo. Harvest GetCapabilities **layers** when that is the catalog.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## NetGIS Server (`netgisserver`) {#netgisserver}

`/Netgis7` or `/keos/`; optional `wms.ashx` GetCapabilities. Not Sampaş or GiSoftGis. Not WSP `/NetGISRuntime/` (`netgisruntime`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## NetGIS Runtime (`netgisruntime`) {#netgisruntime}

Danish `/NetGISRuntime/basis/index.jsp` (often `?custid=` / `?alias=`). Harvest the public **theme / layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipal viewer. If ArcGIS REST on another host in the same kommune is already harvested as `arcgisserver`, do not duplicate those services. Distinct from Turkish `netgisserver`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Netigma (`netigma`) {#netigma}

Turkish municipal BELNET portals (`/BELNET/LoginFW/Login.aspx`, Netcad). Most content sits behind Netcad-account or e-Devlet login; harvest only guest-visible (misafir) map layers, reports, and forms. Do not scrape login walls. The `/keos/` city guide on the same host is `netgisserver` — a separate harvest scope.

**Keep:** guest-accessible **layer / theme** lists and public reports. **Drop:** login walls, session pages, map tiles, print PDFs, basemaps.

## GC Navi (`gcnavi`) {#gcnavi}

Tenant on `geocloud.jp/webgis/`. One municipality. Often no open GetCapabilities — stop rather than scraping tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## ALANDIS+ (`alandis`) {#alandis}

`webgis.alandis.jp/{tenant}/` (or a custom host with `/alandis.jp/` assets). One municipality or prefecture per tenant. Often no open GetCapabilities — stop rather than scraping tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SonicWeb (`sonicweb`) {#sonicweb}

`www.sonicweb-asp.jp/{slug}/`. One municipality (or prefecture) per path tenant. Often no open GetCapabilities — stop rather than scraping tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeDA-Public (`geogeo`) {#geogeo}

`{city}.geogeo.jp` or `{city}.e-map.geogeo.jp`. One municipality. Often no open GetCapabilities — stop rather than scraping tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geolonia スマートマップ (`geoloniagis`) {#geoloniagis}

Tottori GeoMap `{org}.tottori-geomap.jp` or Kagawa BRIDGES. One public tenant. Distinct from Kazakhstan `smartmap`. Often no open GetCapabilities — stop rather than scraping tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## NOL-IS (`nolis`) {#nolis}

Municipal WebGIS; harvest WMS/CSW if public.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GiSoftGis (`gisoftgis`) {#gisoftgis}

Turkish city guide (`/GiSoftGis/`). Harvest WMS/REST if public. Do not treat the Angular hash router as a dataset list.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Sampaş WebGIS (`sampaswebgis`) {#sampaswebgis}

`/KentrehberiApp/`. Same grain as [GiSoftGis](#gisoftgis).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## PopGIS (`popgis`) {#popgis}

SPC population/census GIS. Harvest the node’s **layer / table catalog**, not every map click. One country/territory node = one scope.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## ActiveMap (`activemapgis`) {#activemapgis}

Municipal map portal. Harvest the public layer tree or GetCapabilities. Skip Gradoservice / Panorama marketing.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GIS WebServer SE (`giswebse`) {#giswebse}

Same grain as [ActiveMap](#activemapgis): public layer tree or GetCapabilities. Skip vendor marketing.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geonomics (`geonomics`) {#geonomics}

Viewer / local SDI. WMS or REST if public. Do not scrape Mapbox tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## ORBISMap (`orbismap`) {#orbismap}

Same grain as [Geonomics](#geonomics).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoPortal.rlp (`geoportalrlp`) {#geoportalrlp}

Open-source SDI (mrmap / Rheinland-Pfalz). Harvest **CSW** or published OWS **layers**, not the map HTML. Prefer CSW when both exist ([harvest-geoportals.md](harvest-geoportals.md), [harvest-protocols.md](harvest-protocols.md#csw)).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoMedia WebMap (`geomediawebmap`) {#geomediawebmap}

Geospatial Portal under `/geoportal01/`, `/cdngiportal/`, or similar. Harvest WMS/WFS GetCapabilities or the portal’s layer list. Skip Intergraph marketing.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## mf-geoadmin3 (`mfgeoadmin3`) {#mfgeoadmin3}

Swiss geoadmin3 forks.

```text
GET https://host/rest/services/api/MapServer/layersConfig
GET https://host/layersConfig
```

Harvest `layersConfig` JSON (or WMS the config points at). Do not scrape map.geo.admin.ch tiles. Skip swisstopo marketing if you only needed an existing registry row. The current federal viewer is [web-mapviewer](#webmapviewer).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## web-mapviewer (`webmapviewer`) {#webmapviewer}

```text
GET https://api3.geo.admin.ch/rest/services/api/MapServer/layersConfig
```

Harvest **layers** from layersConfig (or WMS/WMTS those ids point at). Do not scrape map tiles. One harvest scope for map.geo.admin.ch; cantonal mf-geoadmin3 forks stay under `mfgeoadmin3`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Re:Earth (`reearth`) {#reearth}

Cesium / PLATEAU VIEW. Harvest the public **catalog / scene dataset** API (CityGML or documented REST), not every 3D tile. One project = one harvest scope.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GIS4Smart (`gis4smart`) {#gis4smart}

Municipal viewer (Y.Ge.P.). Harvest WMS/REST **layers** if public. Often no GetCapabilities — stop rather than scraping tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Evrymap (`evrymap`) {#evrymap}

Consortis Geospatial municipal map portal (often titled Evrymap; MapServer behind the SPA). Harvest public WMS GetCapabilities **layers** when the MapServer `map=` URL works. Do not scrape the Angular viewer tiles. Do not also register the bundled MapServer as a second catalog on the same host.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## BelsisIMS (`belsisims`) {#belsisims}

KRH city guide. Same grain as [GIS4Smart](#gis4smart). Not NetGIS or Sampaş.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GP Atlas (`gpatlas`) {#gpatlas}

Regional web GIS. Harvest the public **layer / catalog** JSON or WMS. Skip login editors and vendor marketing.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geometa (`geometa`) {#geometa}

Gems Development GIS OGD public geoportal (Agate). Same grain as [GP Atlas](#gpatlas): harvest the public **document / layer catalog** JSON behind the SPA, not map tiles.

**Keep:** public planning-document lists, map-layer catalogs, and any documented GeoServer WMS/WFS GetCapabilities on the same tenant.

**Drop:** `/agate_` document-workflow screens that require login; the short “agat doesn’t work without JavaScript” stub as a catalog in itself; vendor marketing at geometa.ru.

Set `software.id: geometa` only when the public HTML matches Agate (title «Портал ГИСОГД», `agat` JS stub, `/agate_` paths, or `portal-gisogd.` / `agate.` hosts). Other `gisogd.*` sites without those signals stay `custom`.

## DATUM GIS (`datumgis`) {#datumgis}

Same grain as [GP Atlas](#gpatlas).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## EverGIS (`evergis`) {#evergis}

Same grain as [GP Atlas](#gpatlas).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Ingeo (`ingeo`) {#ingeo}

Public GISOGD / layer list if any. Skip tiles and vendor marketing.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Farvater GIS OGD (`farvatergisogd`) {#farvatergisogd}

Same grain as [Ingeo](#ingeo).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## IndorRoad Geoportal (`indorgeo`) {#indorgeo}

Harvest the public **object-type / road catalog** behind the IndorGeo landing page or `/geo3/` SPA (tables of signs, bridges, accidents, and other IndorRoad layers). Do not scrape map tiles or krpano panoramas.

**Keep:** public object/layer lists and any documented WMS/WFS. **Drop:** tiles, panoramic video, vendor marketing at geo.indorsoft.ru, and login-walled staff GIS.

## Trimble Locus IMS (`trimblelocus`) {#trimblelocus}

Finnish `/IMS/` viewer. One harvest scope per city tenant.

Harvest public WMS/WFS GetCapabilities if the city publishes them. Do not scrape map tiles or the Locus back-office. Distinct from `belsisims` and from Sitowise Louhi (`louhi`). If a municipal GeoServer/ArcGIS catalog on the same city is already harvested, do not duplicate those layers.

**Keep:** public WMS/WFS GetCapabilities if the city publishes them. **Drop:** map tiles, Locus back-office, and layers already harvested as GeoServer/ArcGIS.

## Sitowise Louhi (`louhi`) {#louhi}

Same grain as [Trimble Locus IMS](#trimblelocus): public layer list or WMS, not tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## NieuwlandGeo Onemap (`nieuwlandonemap`) {#nieuwlandonemap}

`{org}.webgis.nl`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per public tenant. Distinct from GeoServer (`geoserver`) on the same organisation. Skip demo and login-only hosts.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## KaartViewer (`kaartviewer`) {#kaartviewer}

`{org}.kaartviewer.nl` or a city KaartViewer host. Harvest `/admin/rest/kaartviewerapi/menu` or the public layer list. Do not scrape tiles. One harvest scope per tenant, not per menu map. If GeoServer on the same estate is already harvested as `geoserver`, do not duplicate those services.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoApps (`geoapps`) {#geoapps}

`{org}.geoapps.nl` public maps. Harvest the public **layer / theme list** if unauthenticated. Stop on SSO. One harvest scope per public viewer. Most GeoApps tenants are staff-only — do not harvest login walls.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SITMUN (`sitmun`) {#sitmun}

`sitmun.diba.cat`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape tiles. One harvest scope per public SITMUN catalog.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## dmCity (`dmcity`) {#dmcity}

`web.dmcity.fi/{city}/public/`. Harvest the public **layer list** from the Experience Builder app if unauthenticated. Do not scrape Jimu tiles. One harvest scope per city tenant. Distinct from generic `experiencebuilder`. If `{city}.dmcity.fi/server` REST is already harvested as `arcgisserver`, do not duplicate those services.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## InfoGIS (`infogis`) {#infogis}

`www.infogis.fi/{municipality}/`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape OpenLayers tiles. One harvest scope per municipality path. Distinct from `louhi` and `trimblelocus`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Trimble Landfolio (`landfolio`) {#landfolio}

Harvest the public cadastre map-portal layer/license list if unauthenticated. If ArcGIS REST on the same estate is already harvested as `arcgisserver`, do not duplicate those services. Stop on login-only eGov modules.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SHOGun (`shogun`) {#shogun}

terrestris SHOGun WebGIS. Harvest the public application / layer tree from `GET /applications` JSON (Spring `content[]` with `layerTree` / `layerConfig`). When the list is empty, `GET /applications/{id}` for the `applicationId` on the public client URL. Do not scrape OpenLayers tiles. One harvest scope per public map hostname, not per `applicationId` and not `maps2.` aliases. Distinct from GeoServer (`geoserver`) and GeoNetwork (`geonetwork`) on the same estate (Kreis Recklinghausen). Skip vendor demos and login-walled boots (`401` on `/applications`).

```text
GET https://host/applications
GET https://host/applications/{id}
```

**Keep:** public **application / layer** list. **Drop:** map tiles, print PDFs, Keycloak login, and empty demo landings.

## Hajk (`hajk`) {#hajk}

Swedish Hajk webGIS. Harvest the public layer/map list from the mapservice API documented in `appConfig.json` (`mapserviceBase`). Do not scrape map tiles. One harvest scope per public Hajk application. If GeoServer or ArcGIS REST on the same estate is already harvested as `geoserver` / `arcgisserver`, do not duplicate those services.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## ScalarGIS (`scalargis`) {#scalargis}

WKT-SI ScalarGIS WebGIS. Harvest the public layer / theme list from the viewer (or WMS/WFS on the same estate if already published as GeoServer). Do not scrape OpenLayers tiles or print PDFs. One harvest scope per public tenant, not per named map path on the same hub (SMOS viSMOS / COScid / COSvgi). Distinct from older WKT CartoMapas viewers and from GeoServer (`geoserver`) / GeoNetwork (`geonetwork`) already harvested on DGT hosts. Skip `/backoffice` login.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Origo (`origo`) {#origo}

Origosamverkan Origo web GIS. Harvest the public layer list from the viewer JSON config (`/index.json`, or `{mapdir}/index.json` when the catalog link is a themed map path) or from WMS/WFS on the same host if already published as GeoServer. Do not scrape OpenLayers tiles. One harvest scope per municipality viewer, not per themed map path. Distinct from Hajk (`hajk`) and myCarta (`mycarta`). If GeoServer on the same host is already harvested as `geoserver`, do not duplicate those services. Gallery landings (Ånge, Sundsvall) stay one catalog: harvest each `{mapdir}/index.json` linked from the landing page as endpoints on that record.

```text
GET https://host/index.json
GET https://host/index_ssl.json
GET https://host/{mapdir}/index.json
```

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Tailormap (`tailormap`) {#tailormap}

B3Partners Tailormap web GIS. Harvest the public application / layer list from `GET /api/app/{app}` JSON (or the `/nl/page/` gallery) if unauthenticated. Do not scrape OpenLayers tiles. One harvest scope per public tenant, not per `/nl/app/{app}` path. Distinct from GeoServer (`geoserver`) on the same estate (Warmteatlas, WIBON). Skip `demo.tailormap.com`, `snapshot.tailormap.nl`, and login-only staff viewers.

```text
GET https://host/api/app/{app}
GET https://host/nl/page/startpagina
GET https://host/nl/page/viewers
```

**Keep:** public **application / layer** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## myCarta (`mycarta`) {#mycarta}

Aveki myCarta WebMap. Harvest the public layer list from the viewer (or WMS GetCapabilities if myCarta Server publishes it on the same host). Do not scrape map tiles. One harvest scope per municipality viewer, not per `#m=` map hash. Distinct from Hajk (`hajk`) on other Swedish `karta.*` hosts. Skip login-only myCarta GO.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## AddSpatial (`addspatial`) {#addspatial}

Icebound AddSpatial web GIS. Harvest the public layer / profile list from the `/smart/` client (or WMS/WFS on the same estate if already published). Do not scrape map tiles. One harvest scope per municipality viewer, not per SMART profile hash. Distinct from Hajk (`hajk`), Origo (`origo`), myCarta (`mycarta`), and `dpwebmap`. Skip `addspatial.icebound.com/SMART` login.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Spatial Suite (`spatialsuite`) {#spatialsuite}

Danish SpatialMap webkort. Harvest WMS/WFS GetCapabilities when public. Do not scrape webkort tiles. Prefer a city GeoServer/ArcGIS catalog on the same municipality if that is the dataset list.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## KortInfo (`kortinfo`) {#kortinfo}

NIRAS `drift.kortinfo.net/Map.aspx?Site=` tenant. Harvest the public layer list if unauthenticated. Do not scrape map tiles. One harvest scope per municipality `Site`, not per Map.aspx page. Distinct from `spatialsuite`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## IntraMaps Public (`intramaps`) {#intramaps}

TechnologyOne IntraMaps Public tenant. Harvest the public **module / layer tree** from the viewer if unauthenticated. ApplicationEngine API paths often return `412` without a session — do not treat that as a catalog. Do not scrape map tiles (Google Maps or ApplicationEngine images). One harvest scope per public `project=` (typically `Public` / `*Public`), not per module. If ArcGIS REST or Hub on the same council is already harvested, do not duplicate those services. Skip login-only staff IntraMaps and eProperty maps.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Spectrum Spatial Analyst (`spectrumspatial`) {#spectrumspatial}

Precisely Spectrum Spatial Analyst tenant (`/connect/analyst/` or `/connect/analyst/mobile/`). Harvest the public **map project / layer list** if unauthenticated. Named Feature Service tables may appear at `/connect/analyst/controller/connectProxy/rest/Spatial/FeatureService`. Do not scrape map tiles. One harvest scope per public Analyst tenant, not per `mapcfg=` project. Skip Spectrum Spatial Manager, login-only staff maps, and vendor demos. Do not harvest Exponare `/exponare/` as `spectrumspatial`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Exponare (`exponare`) {#exponare}

MapInfo Exponare public tenant (`/exponare/RestPublicApplication.aspx` or `/exponare/publicinvoker.aspx`). Harvest the public **layer list** from the viewer if unauthenticated. Do not scrape map tiles. One harvest scope per public tenant, not a second copy of Public vs REST vs Mobile on the same host. Skip staff-only Exponare Enquiry and PDF print exports.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## LocalMaps (`localmaps`) {#localmaps}

Eagle Technology NZ `/localmaps/gallery`. Harvest the **gallery map list**, not tiles and not the ArcGIS REST directory on the same host. One harvest scope per council gallery.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GEUSMAP (`geusmap`) {#geusmap}

```text
GET https://host/geusmap/ows/25832.jsp?mapname={name}&SERVICE=WMS&REQUEST=GetCapabilities
GET https://host/geusmap/ows/25832.jsp?mapname={name}&SERVICE=WFS&REQUEST=GetCapabilities
```

One named layer = one dataset analog. Do not scrape map tiles. One harvest scope per `mapname`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GISApp (`gisapp`) {#gisapp}

Romanian `{city}.gisapp.ro` or PortalPublic / Fida city-host viewer. Harvest the public layer list if unauthenticated. Do not scrape map tiles or urbanism-permit forms. If ArcGIS REST on `webadaptor.gisapp.ro` is already harvested as `arcgisserver`, do not duplicate those services.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## PAGIS (`genegis`) {#genegis}

Italian `{comune}.servizigis.it` or city-host PAGIS SIT. Harvest the public cartographic **layer list** if unauthenticated. Do not scrape map tiles, CDU certificate forms, or civil-protection alert widgets. One harvest scope per municipality. Skip `services.servizigis.it` / `pagis.it`. Distinct from Pulaski `www.pagis.org` (`arcgisserver`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GisMaster (`gismaster`) {#gismaster}

Technical Design GeoPortale on `geoportale.sportellounicodigitale.it/GisMaster` with `IdCliente=`. Harvest the public layer list (cadastre, PRGC) or linked WMS/WFS GetCapabilities if unauthenticated. Do not scrape map tiles. One harvest scope per `IdCliente` tenant, not `Default.aspx` as a second copy of VisualDesc, and not cemetery `VisualCim` totems.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoPortale.cloud (`geoportalecloud`) {#geoportalecloud}

Andreani Tributi `{comune}.geoportale.cloud` municipal viewer. Harvest the public cadastre / planning **layer list** after the unauthenticated Accesso libero / Urbanistica guest session (`login_start.php` then `map.php`) if that guest path works. Do not scrape map tiles, IMU value tables, or the staff login. One harvest scope per comune tenant, not `www.geoportale.cloud` and not the Andreani hostname alias of the same tenant. Distinct from `gismaster`, `genegis`, `ldpgis`, and `pmapper`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## UrbisMap (`urbismap`) {#urbismap}

`www.urbismap.com` national hub. Harvest the public **layer / piano / territorio** list from the map UI or unauthenticated `/api/` JSON (`territorio`, `tipo-piano`) if it returns without login. Do not scrape map tiles, CDU/RDU certificate PDFs, cadastre visure, or authenticated `/api/wms/`. One harvest scope for the hub, not per `/territorio/{slug}` city page. Distinct from `geoportalecloud`, `gismaster`, `genegis`, `ldpgis`, and `pmapper`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## LDP SIT (`ldpgis`) {#ldpgis}

Italian `cloud.ldpgis.it/{slug}/` or city-host LDP SIT with LdP Viewer. Harvest the public cartographic **layer list** (or WMS/WFS GetCapabilities if exposed) if unauthenticated. Do not scrape map tiles or Drupal CMS chrome. One harvest scope per comune or union slug. Skip the vendor hub `cloud.ldpgis.it/` with no slug. Distinct from `genegis` and `gfmaplet`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GFMaplet (`gfmaplet`) {#gfmaplet}

Maggioli / GLOBO STU geoportale (`/page:s_italia:geoportale`, `{comune}.prod.globogis.com`, `/stu-geoportale-cartography`, `/gfmaplet/`). If ArcGIS REST on `cartografia*.maggioli.cloud` is already recorded as an endpoint on the same catalog, harvest **that**. Else harvest the public GFMaplet **layer list** if unauthenticated. Do not scrape map tiles or sportello forms. One harvest scope per geoportale tenant — do not add Maggioli ArcGIS REST as a second catalog of the same STU geoportale. Distinct from `gismaster` and `atmmaggioli`.

**Keep:** public **layer / theme** list (or ArcGIS REST / WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, sportello forms, and login walls.

## SmartMap (`smartmap`) {#smartmap}

`{district}.smartmap.kz` investment viewer. Harvest the public **layer / object list** if unauthenticated. Do not scrape Google/Leaflet tiles. One harvest scope per district tenant. Distinct from `geonomics` and `rgis`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SmartGIS (`smartgis`) {#smartgis}

GEO `{tenant}.geo.rs` or city-host Angular Web GIS (title `SmartGIS`). Harvest the public **layer / project list** if unauthenticated. Do not scrape vector/raster tiles, point clouds, or panoramic images. One harvest scope per public tenant, not per project map. Distinct from `smartmap`, `gis4smart`, `gdivisios`, and unrelated hosts that only use the word SmartGIS. Skip the marketing homepage `smartgis.geo.rs`, docs, `*-beta*` hosts, and vendor demos (`smartgis-app`, `smartgis-gf`, `smartgis-geoput`).

**Keep:** public **layer / theme** list if unauthenticated. **Drop:** map tiles, print PDFs, basemaps, point clouds, and login walls.

## KAZGISA RGIS (`rgis`) {#rgis}

`{host}/map/` Angular Leaflet open-contour viewer. Harvest public **WMS GetCapabilities** when GeoServer is exposed, or the public layer tree if unauthenticated. Do not scrape Leaflet tiles. One harvest scope per akimat or city geoportal. Distinct from `geonomics`, `smartmap`, and `vkomap`. Skip the older KAZGISA OpenLayers stack (`eatyrau.kz`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## KAZGISA OpenLayers WebGIS (`kazgisaopenlayers`) {#kazgisaopenlayers}

Harvest the deployment's public GeoServer WMS/WFS GetCapabilities when available.
Otherwise retain named thematic layers exposed by the public OpenLayers layer tree.
Do not scrape rendered tiles, individual features, analysis results, alerts, or
editing forms. One harvest scope per regional portal; do not duplicate its GeoServer
as a second catalog record. This is the legacy OpenLayers/Knockout product, not the
Angular/Leaflet `rgis` generation.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Gharysh Geoportal Platform (`gharyshgeoportal`) {#gharyshgeoportal}

Harvest named public thematic layers and their dataset metadata from the platform's
layer catalog or backing API. Prefer public WMS/WFS capabilities when a deployment
exposes them. Keep the layer title, theme, responsible authority, spatial coverage,
update date, and service/download URL. Drop rendered tiles, individual map features,
dashboard totals, user submissions, and transactional government-service forms. Use
one harvest scope per independently branded sectoral deployment.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## eKMap Cloud (`ekmap`) {#ekmap}

Provincial `{host}` planning viewer with `assets/ekmapboxgl/ekmap-mapboxgl.js`. Harvest the public **planning-layer / dossier list** if unauthenticated. Do not scrape Mapbox tiles. One harvest scope per province or city geoportal. Distinct from Hanoi `quyhoach.hanoi.gov.vn`, Vinh Phuc OpenLayers planning, and HCMC VLAB.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## VKOMAP (`vkomap`) {#vkomap}

```text
GET https://host/Public/GetKatoList
GET https://host/Public/GetLayers?kato={code}
```

Keep named layers from `GetLayers` (pass a `kato` from `GetKatoList`; bare `GetLayers` returns an empty list). Do not scrape Leaflet/Esri tiles. One harvest scope per akimat or city tenant. Distinct from `geonomics`, `smartmap`, and `rgis`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Visor Urbano (`visorurbano`) {#visorurbano}

`visorurbano.{city}.gob.mx` or `{city}.visorurbano.com`. Harvest the public **parcel / zoning layer list** if unauthenticated. Do not scrape map tiles or scrape licence-application forms. One harvest scope per municipality tenant. Skip `www.visorguadalupe.com`. Distinct from `doblesvisor`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Dobles Visor de Mapas (`doblesvisor`) {#doblesvisor}

Costa Rican `/comun/` Leaflet visor. Harvest the public **layer list** from the visor UI if unauthenticated. Do not scrape Leaflet/Google tiles. One harvest scope per municipality. Distinct from CR ArcGIS Experience visors and from MapStore/GeoNetwork.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoNube (`geonube`) {#geonube}

`geonube.com.ar/visor/{slug}` or a custom domain that embeds those visors. Harvest the public **layer list** from the visor if unauthenticated. Do not scrape Leaflet tiles. One harvest scope per municipality or organisation tenant, not per map inside the same tenant. Distinct from `doblesvisor`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Sistema Geodados SaaS (`geodados`) {#geodados}

`{city}.geodados.com.br/Publico`. Harvest the public **thematic map / layer list** (and viability themes) when `acessoAnonimo = true`. Do not scrape OpenLayers tiles. One harvest scope per municipality. Skip staff login at the tenant root.

**Keep:** public **layer / theme** list. **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geopixel Cidades (`geopixel`) {#geopixel}

`{city}.geoportal.geopixel.com.br`. Harvest `/api/pages` city config and the public **map/layer list** when the API responds. Do not scrape map tiles. One harvest scope per municipality. Do not treat the DNS wildcard as extra catalogs.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## CTMGEO SigWEB (`ctmgeo`) {#ctmgeo}

`{city}.ctmgeo.com.br/mapa/`. Harvest the public **cadastral lot / layer list**. Do not scrape map tiles. One harvest scope per municipality. Distinct from unrelated SIGWeb titles on other hosts.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## MapMap (`mapmap`) {#mapmap}

`{city}.mapmap.com.br/geo-portal`. Harvest the public **layer / theme** list in the citizen geoportal when unauthenticated. Do not scrape Mapbox tiles. One harvest scope per municipality. Skip `{city}.cidadao.mapmap.com.br` PWAs, staff `app.mapmap.com.br`, and HTTP 403 `Licença Suspensa` tenants.

**Keep:** public **layer / theme** list. **Drop:** map tiles, print PDFs, basemaps, citizen-issue reports, and login walls.

## DRZ WebGIS (`drzwebgis`) {#drzwebgis}

`webgis.drz.com.br/{city}/`. Harvest the public **cadastral lot / layer list** in the OpenLayers viewer. Do not scrape map tiles or IPTU/print HTML. One harvest scope per municipality. Distinct from CTMGEO SigWEB (`ctmgeo`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers when the GeoServer is public). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## ISY Map (`isymap`) {#isymap}

Norconsult ISY Map / GeoInnsyn / ISY Map Server. Harvest public WMS/WFS GetCapabilities or the viewer layer tree. Do not scrape `/webkart/` PNG/SVG tiles. One harvest scope per municipality application (`application=` / `project=`), not per coordinate permalink.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Avinet Adaptive (`avinet`) {#avinet}

```text
GET https://host/wms.ashx?service=WMS&request=GetCapabilities
GET https://host/wfs.ashx?service=WFS&request=GetCapabilities
```

Keep named WMS/WFS layers. Do not scrape ExtJS map tiles. One harvest scope per public atlas. Distinct from `isymap`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Norkart Kommunekart (`kommunekart`) {#kommunekart}

Norkart Kommunekart viewer (`new Norkart(...)` JS app; Cesium on `3dx.`). No public catalog API or WMS GetCapabilities on the viewer host — harvest the in-app **layer / theme tree** only if it loads unauthenticated. Do not scrape vector/image tiles or Norkart basemap services. One harvest scope per viewer host (national platform or one municipal host).

**Keep:** public **layer / theme** list. **Drop:** map tiles, aerial imagery, print output, and login walls.

## MAP+ (`mapplus`) {#mapplus}

TYDAC `/mapplus/` or `/mapplus-lib/` Stadtplan. Harvest the public **layer list** if unauthenticated. Do not scrape OpenLayers tiles. One harvest scope per municipality viewer. Distinct from `geomapfish` and `mfgeoadmin3`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## EnviMAP (`envimap`) {#envimap}

`*.envimap.hu` or `/hu/Admin/GeoForte/GeoEdit` zoning viewer. Harvest the public layer / parcel query if unauthenticated. Do not scrape Leaflet tiles. One harvest scope per municipality tenant.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## imapTOO iMap (`imaptoo`) {#imaptoo}

`*.imaptoo.ca` Web AppBuilder viewer (`/imap/`, `/imapviewer/`, or `/secure/`). Harvest the shared ArcGIS Server **MapServer layer catalog** at `mapviewer.imaptoo.ca/imap87320977492837458/rest/services` (tenant folders `Cumberland`, `RDMW`; `CVRD_*` / `VOC_*` services at root). Do not scrape viewer tiles or Web AppBuilder app configs. One harvest scope per municipal tenant. Distinct from `webappbuilder` one-offs on other hosts.

**Keep:** public **layer / theme** list (or ArcGIS REST service/layer metadata). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## PISO (`piso`) {#piso}

geoprostor.net / PisoPortal hub. Harvest public WMS or the municipality layer list. Do not scrape map tiles. One harvest scope for the hub (not per občina in the selector) unless a municipality exposes a separate catalog API.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GDi Visios (`gdivisios`) {#gdivisios}

`/visios/{app}` or GDi-hosted Ensemble Smart Portal viewer. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality or county application. Distinct from ArcGIS REST on `gdi.net`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## MapGuide (`mapguide`) {#mapguide}

`/mapguide/` CityScape or `mapviewerphp/ajaxviewer.php`. Harvest the public **layer / legend catalog** if unauthenticated. Do not scrape MapGuide tiles. One harvest scope per municipality. Distinct from `envimap`, `sigimweb`, `geoitgis`, and `zeljkogis`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Zeljko GIS (`zeljkogis`) {#zeljkogis}

`zeljko-gis.com` MapGuide Fusion tenants or `zopcina.zeljko-gis.com/{tenant}/` cadastral UIs. Harvest the public **layer / legend catalog** if unauthenticated. Do not scrape MapGuide tiles. One harvest scope per public city or county tenant, not a second cadastral UI of the same map. Distinct from `mapguide`. Skip gas-utility and administrator ports.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geo-IT GIS Touch Viewer (`geoitgis`) {#geoitgis}

`geoitgis.geo-it.be/touchviewer/` with `Library://Gemeenten/{City}/Maps/*.MapDefinition`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape OpenLayers tiles. One harvest scope per municipality tenant, not per themed MapDefinition. Distinct from `mapguide`. Skip cemetery-only and campaign maps.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SIGimWeb (`sigimweb`) {#sigimweb}

`/sigimweb/` or `/sigim/` with title `SIGimWeb`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape ExtJS / GoMap tiles. One harvest scope per public MRC or city tenant, not per municipality in the picker. Distinct from `mapguide`. Skip intranet and JP Cadrin CIF replacements.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GoMap (`gomap`) {#gomap}

`{client}.geomapguide.ca` or `/gomap/` with title `GoMap - {tenant}`. Harvest the public **layer / theme list** (or the MapGuide mapagent resource listing if unauthenticated). Do not scrape map tiles or session-based `mgosSession.ashx` output. One harvest scope per public tenant.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print output, basemaps, and login walls.

## Geocentriq (`geocentriq`) {#geocentriq}

`app.geocentriq.com/mrc/{mrc}`. Harvest the public **layer / theme list** from a municipality map if unauthenticated. Do not scrape map tiles or require `/login`. One harvest scope per public MRC tenant, not per `/municipalite/` path. Distinct from `sigimweb` and `geocentralis`. Skip the marketing homepage.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoCentralis (`geocentralis`) {#geocentralis}

`portail.geocentralis.com/public/sig-web/{mrc}/{code}/`. Harvest the public **layer / theme list** from a municipality map if unauthenticated. Do not scrape map tiles or require `/core/login/`. One harvest scope per public MRC or city slug, not per geo-code path. Distinct from `geocentriq` and `sigale`. Skip the marketing homepage.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SIGALE (`sigale`) {#sigale}

`sigale.ca/Main.aspx?mrc={code}`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles or Silverlight viewers. One harvest scope per public MRC code, not per municipality in the picker. Distinct from `geocentriq` and `geocentralis`. Skip the hub without an `mrc` parameter.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SeaSketch (`seasketch`) {#seasketch}

`www.seasketch.org/{project}/app`. Harvest public overlay **layer groups** if unauthenticated. Do not scrape map tiles or require a sketching account. One harvest scope per project slug. Distinct from `data.seasketch.org` ArcGIS REST (`arcgisserver`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## XY Maps (`xymaps`) {#xymaps}

`maps.xymaps.com/{city}` or city-host `/xymaps/Map`. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per public city tenant. `www.xymaps.com/{city}` is the same SaaS host. Distinct from Geocortex/ArcGIS that Eckersall also deploys. Skip the marketing homepage and private floorplan dumps.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GISPLAN (`gisplan`) {#gisplan}

T-MAPY `{city}.gisplan.sk`, Czech `{muni}.gis4u.cz`, `{city}.tmapserver.cz`, or city-host Spinbox / T-WIST gallery. Harvest the public `/mapa/` or T-WIST application list if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per municipality. Distinct from `gisapp`, `iobcina`, `gepro`, `gisonline`, `mapotip`, `cgwebgis`, `mobec`, `georeal`, and `geodeticca`. T-MAPY MapProxy on `services7.tmapserver.cz` is `mapproxy`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## mOBEC (`mobec`) {#mobec}

`mobec.sk/{slug}`. Harvest the public **Všeobecná mapa** / layer list if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per municipality slug. Distinct from `gisplan`. Skip the marketing home.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## CG WebGIS (`cgwebgis`) {#cgwebgis}

`webgis.{city}.sk` or a city host with title `WebGIS v2, CG`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality. Distinct from `gisplan` and `geodeticca`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geodeticca WEB GIS (`geodeticca`) {#geodeticca}

`gis.{city}.sk` titled `Geodeticca WEB GIS`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality. Distinct from `cgwebgis` and `gisplan`. Skip Michalovce `michalovce.web-gis.sk`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geoportál GEPRO (`gepro`) {#gepro}

`{city}.obce.gepro.cz` or `{city}.gepro.cz`. Harvest the public **layer / theme list** from the `/OUT/HTML/` viewer if unauthenticated, or WMS/WFS GetCapabilities when those are public. Do not scrape OpenLayers tiles. One harvest scope per municipality. Distinct from `gisplan`. Skip login-only intranet tenants.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## KOVGIS EVALD (`evald`) {#evald}

`evald.ee/{slug}/` (not `service.eomap.ee` aliases). Harvest the public **layer / module catalog** (detailplaneeringud, geoarhiiv, munitsipaalmaad, teemainfo) if unauthenticated. Do not scrape map tiles or authenticated geoarchive file downloads. One harvest scope per public tenant slug (municipalities, nationwide `eesti`, ELVL). Distinct from `arcgisserver` `gis.{muni}.ee` portals. Skip `403` tenants (Ruhnu) and `evald2_*` session URLs.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## terGIS (`tergis`) {#tergis}

`{tenant}.tergis.lv`. Harvest `/api/v1/classifiers/layers` on Angular SPA tenants, or `/themes.json` layers on QWC2-frontend tenants, if unauthenticated. Do not scrape map tiles or follow the login form. One harvest scope per public tenant. Distinct from generic `qwc2` off `tergis.lv`. Skip `tergis.lv` marketing, `401`, and `502` tenants.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## TerraWeb (`terraweb`) {#terraweb}

Terraplan `{tenant}.terragis.de` and custom-domain Kreis geoportals. Harvest the public **theme / layer tree** from the guest OpenLayers viewer (`login-ol.htm?login=gast` or the named public account on the launcher), or WMS/WFS GetCapabilities when the tenant publishes them (Lüneburg does). Do not scrape map tiles. One harvest scope per public tenant. Distinct from Latvian `tergis`. Skip the vendor homepage, Keycloak, and `anmelden.htm` staff logins.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## TerraVisu (`terravisu`) {#terravisu}

Makina Corpus / Autonomens territorial observatory. Harvest **scenes** from `GET /api/geolayer/scene/`, then the **layer tree** at each scene `layers_tree_url` (`/api/geolayer/view/{slug}/`). Do not scrape Mapbox/vector tiles. One harvest scope per public tenant, not per `/view/{slug}` theme or data.gouv.fr reuse. Distinct from older Terralego Angular apps on `*.terralego.com`. Skip `/config/` admin, vendor demos, and `401` origins.

```text
GET https://host/api/settings/frontend
GET https://host/api/geolayer/scene/
GET https://host/api/geolayer/view/{slug}/
GET https://host/env.json
```

**Keep:** public **scenes** and their **layer trees**. **Drop:** map tiles, `/config/` admin, `/api/geolayer/` collection endpoints that return 401, and login-only private layers.

## Mon Territoire Carto (`monterritoirecarto`) {#monterritoirecarto}

SOGEFI `carto.monterritoire.fr/map.php?instance=` public instances and branded `{org}.monterritoire.fr` Carto hosts. Harvest the public **layer / theme tree** of that instance. Do not scrape map tiles, parcel/owner MAJIC queries, or the staff login hub. One harvest scope per public instance or branded host. Skip Voirie/TLPE logins and partner Découverte skins.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Pozi (`pozi`) {#pozi}

`{council}.pozi.com`. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per public council subdomain. Distinct from `intramaps` and `exponare`. Skip the marketing homepage.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## JMap (`jmap`) {#jmap}

`/JMapWeb/` or JMap NG `/services/ng/`. Harvest the public **layer / project list** if unauthenticated. Do not scrape map tiles or require JMap Admin. One harvest scope per public tenant or project. Distinct from ArcGIS viewers. Skip hostnames that merely contain `jmap`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GIS Cloud (`giscloud`) {#giscloud}

`{city}.giscloud.com`. Harvest the public **layer list** if unauthenticated. Do not scrape tiles or require Map Editor login. One harvest scope per public tenant. Distinct from generic Leaflet.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## MRF Web Map (`mrf`) {#mrf}

`{county}.mrf.com` or a host loading `js/lib/mrf/`. Harvest the public **layer list** after the guest disclaimer if unauthenticated. Do not scrape tiles or require staff login. One harvest scope per public tenant. Distinct from `giscloud`. Skip `web.munisight.com` (`munisight`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## MuniSight (`munisight`) {#munisight}

`web.munisight.com/{Tenant}`. Harvest only if a public guest map exists. Do not scrape tiles or follow staff Login.aspx. One harvest scope per municipality tenant. Distinct from `mrf` and `geomediawebmap`. Skip the marketing homepage.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoMedia SmartClient Public Maps (`publicmaps`) {#publicmaps}

`publicmaps.gisquadrat.com/BP/WEPM.aspx?site=GMSC&project={TOWN}`. Harvest the public **layer / map-view list** from `/GMSC/PUBLIC/Configuration` if unauthenticated. Do not scrape map tiles. One harvest scope per municipal `project=` tenant. Distinct from `geomediawebmap` and `erdasapollo`. Skip the marketing homepage and retired `gis-klagenfurt.at`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SIT WebGis (`sitwebgis`) {#sitwebgis}

`webgis.sit-puglia.it/{comune}/`. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipal tenant. Distinct from Regione Puglia `geonetwork` on `repertorio.sit.puglia.it`. Skip the marketing homepage and stale `/mola` and `/potenza` slugs.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## p.mapper (`pmapper`) {#pmapper}

`/pmapper/` or `{city}.geo-portale.it`. Harvest WMS GetCapabilities or the p.mapper layer tree. Do not scrape map images. One harvest scope per municipality or SIT. Distinct from UMN `mapserver` as the public catalog.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## CommunityView (`communityview`) {#communityview}

`maps.digitalmapcentral.com/production/VECommunityView/cities/{city}/`. Harvest the public **layer list** if unauthenticated. Do not scrape Bing basemap tiles. One harvest scope per city slug.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## MS-GIS (`msgis`) {#msgis}

`{city}.msgis.net`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality. Distinct from `masterportal` and `touviamaps`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Weave (`weave`) {#weave}

Title `Weave Map` on Australian council domains. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per council viewer. Distinct from `intramaps`, `exponare`, and `pozi`. Skip GeneWeaver and other hosts that merely contain the word weave.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## OVIE (`ovie`) {#ovie}

INEGI municipal economic GIS (`/js/libs/OpenLayers/OL.js`). Harvest the public **layer / indicator list** if unauthenticated. Do not scrape map tiles or print PDFs. One harvest scope per municipality or state OVIE. Distinct from INEGI Gaia `/mdm6/` (`mxsig`). Skip Mission Viejo `geoviewer.io`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SOFTPRO (`softpro`) {#softpro}

`{city}.cadastre.com.ua` or city MBK hosts that mention SOFTPRO. Harvest the public **layer / cadastre list** if unauthenticated. Do not scrape map tiles. One harvest scope per community or oblast portal. Distinct from `kadastr.gov.ua` and `map.land.gov.ua`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## MxSIG (`mxsig`) {#mxsig}

`/mdm6/` or `/mxsig2/` Mapa Digital de México. Harvest public **WMS / layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per MDM6 viewer, not an indicators CMS on the same host. Distinct from `ovie`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GisOnline (`gisonline`) {#gisonline}

`app.gisonline.cz/{city}`. Harvest the public **layer / pasport list** if unauthenticated. Do not scrape map tiles or panorama imagery. One harvest scope per city slug. Distinct from `gisplan` and `gepro`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## K5 MapServer (`k5mapserver`) {#k5mapserver}

`{muni}.k5mapserver.cz`. Harvest the public map / pasport catalog from the GEOPORTÁL home if unauthenticated. Do not scrape map tiles. One harvest scope per municipality subdomain. Distinct from UMN `mapserver`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Marushka (`marushka`) {#marushka}

GEOVAP Marushka HTML client. Harvest WMS/WFS GetCapabilities when Marushka publishes them, or the public project/layer list. Do not scrape map tiles. One harvest scope per city installation. Distinct from `gisplan`, `gepro`, and `georeal`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Georeal (`georeal`) {#georeal}

Czech kraj `{host}/portal/` CMS with `Georeal.Cards`. Harvest the public **application / map-card catalog** if unauthenticated, or WMS/WMTS GetCapabilities when those are public. Do not scrape map tiles. One harvest scope per DTM or geoportal product. Distinct from `gisplan`, `gepro`, and `marushka`. Skip `/portal/` shells without `Georeal.Cards`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Mapotip (`mapotip`) {#mapotip}

`portal.mapotip.cz/{municipality}`. Harvest the public **layer / pasport list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality slug. Distinct from `gisplan`, `gepro`, and `gisonline`. Skip the demo tenant.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## giscity (`giscity`) {#giscity}

`www.gisserver.de/{city}/`. Harvest the public **theme / map catalog** if unauthenticated. Do not scrape map tiles. One harvest scope per city path. Distinct from ArcGIS Hub catalogs whose hostname contains `giscityof`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## iObčina (`iobcina`) {#iobcina}

Kaliopa `/gisapp/Default.aspx?a={tenant}` viewer. Harvest public layers for that tenant. Do not scrape tiles. Distinct from `gisapp`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Astun iShare (`ishare`) {#ishare}

UK My Maps / My House portal. Harvest the public **layer / local-info catalog** if unauthenticated, or WMS/WFS GetCapabilities when those are public. Do not scrape map tiles or address-search HTML. Distinct from `cadcorp`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Cadcorp SIS WebMap (`cadcorp`) {#cadcorp}

Public SIS WebMap / Web Map Layers. Harvest WMS/WFS GetCapabilities or the published layer list. Do not scrape tiles. Distinct from disy Cadenza (`cadenza`) and from Astun iShare (`ishare`).

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## StatMap Earthlight (`earthlight`) {#earthlight}

Public Earthlight Portal / Earthlight Public (`/map/map.html?login=ExternalELP`) and Aurora embeds of the same StatMap GIS. Harvest WMS/WFS GetCapabilities or the published public layer list. Do not scrape tiles. Distinct from Astun iShare (`ishare`) and Cadcorp SIS WebMap (`cadcorp`). Skip HorizoNext case-management portals.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, Aurora script variants of the same tenant, and login walls.

## CartoVista (`cartovista`) {#cartovista}

Start from `/CartoVistaServer/maps/view?page=mapGallery` and enumerate public maps in the gallery. For each map, use its published configuration or documented CartoVista Server API to resolve data layers. Keep named public data layers; drop basemaps, UI themes, thumbnails, and rendered tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## IGO2 (`igo2`) {#igo2}

Read the deployment's JSON contexts (`contexts.json`, `_default.json`, or the context API) and resolve configured WMS/WFS/GeoJSON sources. Keep named operational layers or CSW dataset records. Deduplicate the same source exposed through more than one OGC protocol.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## vMap2 (`vmap2`) {#vmap2}

Veremes vMap2 web GIS. Harvest the public map / layer list from an unauthenticated `/vmap` guest session or `/vmap/widget/vmap` embed, then resolve published MapServer WMS/WFS on the same host. One harvest scope per public tenant, not per widget token or `map_id`. Skip login-only staff GIS, vendor demos, and consultant marketing hosts.

```text
GET https://host/vmap
GET https://host/vmap/login
GET https://host/vmap/widget/vmap
```

**Keep:** public **map / layer** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## InfoMap (`infomap`) {#infomap}

Enumerate public maps from the InfoMap Map Portal, then resolve the QGIS Server WMS behind each map. Harvest named WMS layers, not rendered tiles or saved map views. Treat one tenant portal as one harvest scope.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## dpWebmap (`dpwebmap`) {#dpwebmap}

Harvest the public layer tree or configured WMS/WFS services. Keep named operational layers; drop dpWebmap UI modules, cached basemap tiles, print jobs, and organizer/login applications.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## 3MAP (`3map`) {#3map}

Harvest the public project and layer list exposed by the GIS viewer. Prefer linked WMS/WFS capabilities when available. Do not treat the 3OIS document modules, help pages, or rendered tiles as datasets.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## 1Map (`1map`) {#1map}

`{municipio}.1map.com.br`. Known tenants are sign-in only (`/auth/unauthenticated` redirect), so there is usually nothing public to harvest — record the tenant and stop at the login wall. If a tenant ever exposes a public layer list, harvest that list only. One harvest scope per municipal tenant. Skip the `demonstracao` demo and the 1Doc marketing pages.

**Keep:** public **layer / theme** list if one is ever exposed without login. **Drop:** map tiles, print PDFs, basemaps, and login walls.

## CGI WebGIS / Facta WebGIS (`factawebgis`) {#factawebgis}

Harvest the public map's layer list and any exposed WMS/WFS services. Keep municipal register-derived thematic layers; drop address-search responses, basemaps, print output, and the application bundle.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## inkasPortal (`inkasportal`) {#inkasportal}

Harvest public themes/layers or their WMS capabilities. Keep named geodata layers; drop `inkas@work` forms, cadastral-order workflows, drawing output, login-only data, and map tiles.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoViewer Online (`geoviewer`) {#geoviewer}

Harvest only layers explicitly published in the public map. Do not crawl work orders, billing, SCADA, IoT, customer, or staff-only asset-management functions. Drop vector/raster tiles and UI configuration.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Flood Intelligence Portal (`floodintelligenceportal`) {#floodintelligenceportal}

Treat published flood scenarios, historical events, gauges, and downloadable flood-study layers as dataset-like objects when the tenant exposes a list. Property reports are generated views, not independent datasets. Do not enumerate addresses or properties.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## pGIS (`pgis`) {#pgis}

Start with `GET /api/v1/classifiers/layers` and keep enabled named leaf layers as the tenant's public layer catalog. Preserve parent groups as topics, not datasets. When the deployment publishes WMS/WFS, prefer GetCapabilities for stable identifiers and service metadata. Do not harvest Google basemaps, suggestions, or feature responses one object at a time.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geoambiental (`geoambiental`) {#geoambiental}

Harvest the public viewer's named environmental layer tree and resolve its configured ArcGIS REST or OGC services when exposed. Keep thematic layers and public reports with stable definitions; drop basemaps, permit case records, user-specific workflows, rendered tiles, and Angular assets. One harvest scope per environmental authority tenant.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## NAZCA (`nazca`) {#nazca}

Read the municipality-specific `config_{name}.js` and shared `main.js` to identify the public cadastral and thematic services. Keep named public layers; drop individual parcel-query results, addresses, Street View content, user-loaded local overlays, basemaps, and rendered tiles. One harvest scope per numeric municipal route.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Xiltrion (`xiltrion`) {#xiltrion}

Use only unauthenticated public `/api` responses required by the `/map` client to enumerate named municipal or cadastral layers. Keep stable public layer definitions; drop individual parcels, owners, addresses, authenticated cadastral cases, generated certificates, Mapbox styles, and tiles. One harvest scope per municipality subdomain.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GT Map (`gtmap`) {#gtmap}

Use the public LifeMap layer tree and the `/gs-gate/` WMS configuration referenced by the client. Keep named municipal thematic layers and stable WMS layers; drop address and parcel-query responses, weather and air-quality readings, basemaps, road-view imagery, print jobs, and SODA application assets. One harvest scope per municipality.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Terratwin (`terratwin`) {#terratwin}

Harvest the county GDI layer tree and the TerraTwin module's published map services. Keep named district and cadastral layers; drop individual parcel lookups, 3D scene tiles, and Vite application assets. One harvest scope per county deployment.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GIS4U (`gis4u`) {#gis4u}

Harvest the /mapa/ application catalogue and each application's layer configuration. Keep named cadastral, technical-map, and register layers; drop per-feature queries and square-theme application assets. One harvest scope per municipal domain.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Myeongji WebGIS (`myeongji`) {#myeongji}

Harvest the living-information layer tree and cadastral/aerial search panels exposed by the shared client. Keep named thematic and cadastral layers; drop address and parcel-query responses, aerial-image tiles, print/save jobs, and `/js/base/` application assets. One harvest scope per municipal deployment.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Berry GIS (`berryict`) {#berryict}

Harvest the per-assembly layer list behind `propertyidentification.php`. Keep named street, building, parcel, block, community, and sub-metro layers; drop individual property lookups and Leaflet application assets. One harvest scope per assembly tenant.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## VB GIS (`vbgis`) {#vbgis}

Harvest the tenant's public construction-planning and infrastructure layer endpoints referenced by the viewer. Keep named planning and infrastructure layers; drop parcel-record queries, certificates, and tiles. One harvest scope per tenant subdomain.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## SHK Kent Bilgi Sistemi (`shkkbs`) {#shkkbs}

Enumerate the public city-guide themes and their municipality-hosted ArcGIS REST services. Keep stable thematic map layers and zoning/plan layers intended for public reuse; drop individual parcel lookups, address-search responses, generated zoning certificates, basemaps, panorama imagery, and private staff modules. One harvest scope per municipality.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## CoGIS (`cogis`) {#cogis}

Enumerate the public map and application catalog exposed by CoGIS Portal. Keep named maps,
stable thematic layers and their service metadata; drop application bundles, basemaps,
tiles, search suggestions, individual features and user tasks. Legacy portals may expose
the catalog through `/CoGIS/Map` or custom `/api/providers` routes. One public portal is
one harvest scope even when it contains several map applications.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Geocad System Enterprise Edition (`geocadgsee`) {#geocadgsee}

Resolve the public workset and layer catalog used by the registered portal. Keep named
thematic layers and stable service metadata; preserve workset/group hierarchy as topics.
Drop individual `graph_ids`, object-semantic responses, address searches, basemaps,
application modules and rendered tiles. Use bounded REST requests and do not enumerate
features through spatial `ids/filter` calls unless a documented dataset export requires
them. One regional or municipal portal is one harvest scope.

**Keep:** named thematic layers and stable service metadata. **Drop:** individual `graph_ids`, address searches, basemaps, application modules, and tiles.

## Sputnik Web (`sputnikweb`) {#sputnikweb}

Start from the registered installation and enumerate only public locations and the named
layers, models or attachments exposed inside them. Keep stable city models, terrain,
planning layers and downloadable project resources as dataset-like records. Drop Cesium
tiles, textures, thumbnails, application bundles, authentication routes and generated
views. Do not crawl numeric `/location/{id}` values; follow locations linked by the public
installation. Treat a public installation as one harvest scope.

**Keep:** stable city models, terrain, planning layers, and downloadable project resources. **Drop:** Cesium tiles, textures, thumbnails, authentication routes, and numeric `/location/{id}` crawls.

## ZuluGIS Online (`zulugisonline`) {#zulugisonline}

POST `/zws` `GetZMMapList` for published web maps (one map = one dataset analog) and
`GetLayerList` or WMS GetCapabilities `{link}/../ws?service=WMS&version=1.1.1&request=GetCapabilities`
for named layers. `GetZMMap` returns the map JSON (layer list). Do not scrape OpenLayers
tiles, `/ZuluWeb/js/compiled.min.js`, or login-only ZWS (`401`). One harvest scope per
public ZuluServer, not per named map.

**Keep:** public web maps and named ZWS/WMS layers. **Drop:** tiles, demo maps on
`zs.zulugis.ru`, and authenticated utility GIS.

## Геопортал RuMap (`rumap`) {#rumap}

`rumap.ru` (not `/v2`, not wildcard aliases). Harvest the public **layer / theme catalog** (`tab=catalog`) if unauthenticated. Do not scrape `tile.digimap.ru` PNG/vector tiles, routing geometries, or PRO login workspaces. One harvest scope for the hosted portal. Distinct from `transport.digimap.ru` (licensed traffic GIS) and from the Digimap marketing site.

**Keep:** public **layer / theme** list (or named RuMap data layers). **Drop:** map tiles, traffic rasters, print PDFs, basemaps, and login walls.

## DIGITAL TWIN CLOUD (`digitaltwincloud`) {#digitaltwincloud}

Harvest the public layer / workset tree of the municipal smart-map or EGIS tenant. Keep named thematic and 3D city-model layers and any public WMS/WFS/WCS services; drop Cesium/3D Tiles, Appwork chrome, `IDE.css` application assets, login (`/member/login.do`), and individual feature queries. One harvest scope per public city or SaaS tenant.

**Keep:** named thematic and 3D city-model layers and public WMS/WFS/WCS. **Drop:** Cesium/3D Tiles, Appwork chrome, login, and individual feature queries.

## brain-GeoCMS (`braingeocms`) {#braingeocms}

Harvest the municipal GeoCMS theme/layer catalog exposed by the public geoportal. Keep named planning, environment, and infrastructure map themes; drop CMS chrome, login, and rendered tiles. One harvest scope per Kreis or shared GDI portal. Public GetCapabilities is often missing — do not scrape map images.

**Keep:** named planning, environment, and infrastructure map themes. **Drop:** CMS chrome, login, and rendered tiles.

## DMAPS (`dmaps`) {#dmaps}

`{palika}.dmaps.org` or a municipal `dmaps.` / `metric.` / `imas.` / `gis.` host. Harvest the public **building / road / address layer list** if unauthenticated. Do not scrape map tiles, drone orthophoto, or require staff login. One harvest scope per public municipal tenant. Distinct from Kathmandu custom house-numbering GIS. Skip the marketing homepage and `app.dmaps.org`.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Related

- [harvest.md](harvest.md)
- [harvest-geoportals.md](harvest-geoportals.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [discovery-geoportals.md](discovery-geoportals.md)
- [agents/harvest.md](agents/harvest.md)

## Map2Web (`map2web`) {#map2web}

Schubert & Franzke `*.map2web.eu` town-plan viewers. Browser-only Vue app; export formats include GeoJSON. Harvest only public WFS/OGC or the site's own export; do not scrape map tiles.

**Keep:** public WFS/OGC exports. **Drop:** map tiles.

## EnMapa (`enmapa`) {#enmapa}

Nexus Geographics municipal viewers at `{city}.enmapa.com` and city-host `/visor/guia` installs. Harvest the public theme/layer tree the viewer loads (or WMS GetCapabilities when the tenant exposes one). Do not scrape map tiles, print PDFs, or the Cloudflare admin/dev hosts. One harvest scope per municipality tenant.

**Keep:** public theme/layer tree or WMS GetCapabilities. **Drop:** map tiles, print PDFs, basemaps, and dev/admin/demo subdomains.

## Nexus Public Portal (`nexuspublicportal`) {#nexuspublicportal}

INS Nexus GIS public viewers at `{city}.ins.com.mk/NexusPublicPortal/PublicPortal/Map` and city-host `gis.{city}.gov.mk` installs. Harvest the public layer tree the Map page loads (cadastral parcels, GUP/DUP, business entities) or WMS GetCapabilities when the tenant exposes one. Do not scrape map tiles, print PDFs, or AppCreator login workflows. One harvest scope per municipality tenant.

**Keep:** public layer tree or WMS GetCapabilities. **Drop:** map tiles, print PDFs, basemaps, vendor demo (`nexusgis.ins.com.mk`), and Nexus Twin portals.

## uMap (`umap`) {#umap}

Self-hosted OSM map creator; each instance is a catalog of user-published maps. List public maps via `/{lang}/search/?q=` (HTML) or the home-page browse section; each map at `/{lang}/map/{slug}_{id}` exposes datalayers as GeoJSON at `/datalayer/{id}/`. One map = one dataset analog; datalayers = its resources. Do not scrape basemap tiles, and skip anonymous-edit / secret-link flows.

**Keep:** public maps and their GeoJSON datalayers. **Drop:** basemap tiles, user accounts, edit links, login-only instances.

## GISQuick (`gisquick`) {#gisquick}

QGIS-project publishing platform; each published project is one map application over OGC services. `GET /api/app` is anonymous and may name a `landing_project` (`{user}/{name}`); `GET /api/projects` usually requires login, so enumerate public projects from the landing page, known project slugs, or the operator's site. Per project, `GET /api/map/project/{user}/{name}` returns the full JSON project description (layers, topics, extent, print composers) and `GET /api/map/ows/{user}/{name}?SERVICE=WMS&REQUEST=GetCapabilities` (WFS/WMTS likewise) lists the published layers. One project = one dataset analog; its layers = resources.

**Keep:** public projects, their layer list and WMS/WFS/WMTS endpoints. **Drop:** login-only instances with no public project, user accounts, upload/edit endpoints, tile caches.

## MapMint (`mapmint`) {#mapmint}

ZOO-Project/MapServer geoportal; MapMint 3.0 deployments publish STAC + OGC API. Harvest `{link}/collections` (STAC collection search) and `{link}/conformance`; one collection = one dataset analog, collection items/assets = resources. Older MapMint 2.x portals expose WMS/WFS/WCS/WPS GetCapabilities per map — harvest layer lists, not tiles.

**Keep:** STAC/OGC API collections and their items; OGC service layer lists. **Drop:** WPS job endpoints, admin UI, tile caches, MS4W default pages that merely link `zoo_loader.cgi`.

## QGIS Cloud (`qgiscloud`) {#qgiscloud}

Per-map OGC services from QGIS Server: GET `{link}/wms?SERVICE=WMS&REQUEST=GetCapabilities`. A `401`/`404` on `/wms` means the owner restricted OGC — record the map without an endpoint; do not brute-force project paths.

**Keep:** named WMS/WFS layers of the tenant map. **Drop:** platform pages (`/en/maps/`, pricing, signup), embed iframes on third-party sites, and the QGIS Cloud plugin/admin UI.

## Septima Search (`septimasearch`) {#septimasearch}

Bespoke Danish map applications embedding the Septima Search component (`septima.dk/septima-search-dmp/v1.js`). There is no catalog API of its own; enumerate the app's published layer/theme list (in-page layer tree or config JSON) and resolve the backing WMS/WFS services where documented. Danmarks Miljøportal layers are served from the portal's own ArcGIS/OGC infrastructure — harvest those service endpoints, not the Septima CDN.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, address-search requests, staging hosts (`*.test.`/`*.demo.`/`*.udv.`), and login-only modules (e.g. MARS Ansøgning/Administration).

## AtlasMapper (`atlasmapper`) {#atlasmapper}

Ext JS/GeoExt research-atlas client (`atlasmapperVer` asset parameter). Harvest the viewer's published layer tree from its JSON client configuration; when the deployment pairs the viewer with a GeoNetwork catalogue (`catalogue.{domain}/geonetwork`) or GeoServer/THREDDS services, prefer CSW/OAI-PMH records and WMS/WFS GetCapabilities for stable layer identifiers. One harvest scope per atlas viewer.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## Elvis (`elvis`) {#elvis}

National elevation and depth download service. The orderable product list (LiDAR surveys, DEMs, bathymetry collections) is the dataset grain; do not enumerate generated order downloads, tiles, or user jobs. One harvest scope for the single national instance.

**Keep:** published orderable product / survey list. **Drop:** map tiles, print PDFs, basemaps, generated order artefacts, and login walls.

## North Australian Fire Information (`nafi`) {#nafi}

Fire-history viewer backed by GeoServer WMS. Prefer WMS GetCapabilities for the named fire-scar and fire-frequency layers; treat each published fire-scar year layer as the dataset grain. One harvest scope for the single hosted instance.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GoMap (`gomap`) {#gomap}

MapGuide-based tenant viewers (`/gomap_web/` scripts, `mapagent` backend). Harvest the tenant's published layer tree from the viewer configuration; when the MapAgent or a backing WMS service is exposed, prefer its layer list or GetCapabilities for stable identifiers. One harvest scope per tenant.

**Keep:** public **layer / theme** list (or WMS GetCapabilities named layers). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GeoView (`geoview`) {#geoview}

Embeddable NRCan viewer (`cgpv-main.js`, `div.geoview-map`, `cgpv.init()`). The viewer
itself holds no catalog: harvest the backing source instead — for app.geo.ca that is the
geoCore REST API (`geocore`); for standalone embeds, harvest the WMS/WFS/ESRI REST
endpoints named in the map's `data-config` JSON layer list.

**Keep:** the **configured layer list** from `data-config` as map-layer dataset analogs
when no backing catalog exists. **Drop:** map tiles, PNG/PDF exports, basemaps, and the
viewer bundle itself.

## iMap (imapTOO) (`imaptoo`) {#imaptoo}

ArcGIS Web AppBuilder tenants on `*.imaptoo.ca` (`/imap/`, `/imapviewer/`, `/secure/`) backed by a shared ArcGIS Server (`mapviewer.imaptoo.ca/imap.../rest/services`). The viewer URL holds no catalog API; harvest the tenant's configured layer list from the Web AppBuilder config JSON, or enumerate the shared ArcGIS Server services directory once per server, not per tenant. One harvest scope per tenant viewer.

**Keep:** public **layer / theme** list (or ArcGIS REST service/layer entries). **Drop:** map tiles, print PDFs, basemaps, and login walls.

## GSI Maps (`gsimaps`) {#gsimaps}

地理院地図 deployments. Harvest the `layers.txt` layer manifest (and `layers/*.txt` topic files) as the layer list; the viewer itself holds no dataset API. One harvest scope per deployment.

**Keep:** public **layer / theme** list from `layers.txt`. **Drop:** map tiles, 3D terrain tiles, print output, basemaps.

## open-hinata (`openhinata`) {#openhinata}

ひなたGIS / OH3 viewers. Harvest the `js/layers.js` layer definitions as the layer list. No dataset API — stop rather than scraping tiles.

**Keep:** public **layer / theme** list. **Drop:** map tiles, basemaps, SIMA/CAD exports.

## Maplat (`maplat`) {#maplat}

Historical-map viewers (s.maplat.jp tenants and custom domains). Harvest the tenant's published map list (old-map layers with thumbnails) as the layer list. No dataset API.

**Keep:** public **layer / theme** list (georeferenced old maps). **Drop:** map tiles, basemaps, app binaries.

## Stroly (`stroly`) {#stroly}

Hosted old-map platform. Harvest the public map collection list per publisher page. Platform-level harvest only; do not enumerate every user upload as separate catalogs.

**Keep:** public **layer / theme** list (map collections). **Drop:** map tiles, basemaps, login walls.

## eコミマップ (`ecommap`) {#ecommap}

NIED participatory WebGIS. Harvest public user-published maps / overlay layer lists (WMS, KML) where exposed. No dataset API — stop rather than scraping tiles.

**Keep:** public **layer / theme** list. **Drop:** map tiles, basemaps, print PDFs, login walls.
