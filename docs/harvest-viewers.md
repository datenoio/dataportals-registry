# Harvesting map viewers and tile caches

Many geoportals in this registry are **viewers** (QWC2, Masterportal, Lizmap, mviewer, Wagmap, Tianditu, Trimble Locus / Louhi / Landfolio, dmCity, InfoGIS, Spatial Suite, Spectrum Spatial Analyst, Exponare, KortInfo, IntraMaps Public, LocalMaps, GEUSMAP, GISApp, GeneGIS PAGIS, GisMaster, HyG Mapgis, SmartMap, VKOMAP, Visor Urbano, Dobles Visor de Mapas, ISY Map, Avinet Adaptive, iObčina, iShare, Cadcorp, VertiGIS Studio Web, ArcGIS Experience Builder, ArcGIS Web AppBuilder, ArcGIS Instant Apps, Hajk, myCarta, T-MAPY GISPLAN, CG WebGIS, Geodeticca WEB GIS, Geoportál GEPRO, GisOnline, K5 MapServer, Marushka, Georeal, Mapotip, giscity, touvia.MAPS, INGRADA online, VC Map, XY Maps, Pozi, JMap, GIS Cloud, MRF Web Map, MuniSight, p.mapper, CommunityView, MS-GIS, Weave, OVIE, SOFTPRO, MxSIG). The catalog of datasets is the **layer list** (GetCapabilities, `themes.json`, REST services) — not PNG tiles, print PDFs, or the basemap.

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

## touvia.MAPS (`touviamaps`) {#touviamaps}

`vianovis.net/{tenant}/` or a city host loading `touvia.de/scripts/loader.js`. Harvest the public **theme / layer tree** if unauthenticated. Do not scrape Cesium/Google 3D tiles. One harvest scope per municipality or Landkreis. Distinct from `masterportal` and `vcmap`.

## INGRADA online (`ingrada`) {#ingrada}

Softplan `INGRADA online` BürgerGIS (`Softplan.Ingrada.Mobile`, `/mobile/message-channel.js`). Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per municipality or Landkreis. Distinct from `weboffice` and `mapguide`. Skip CMS BürgerGIS landing pages.

## VC Map (`vcmap`) {#vcmap}

Virtual City Systems `html.vcs-ui` / title `VC Map`. Harvest the public **layer / theme tree** if unauthenticated. Do not scrape Cesium 3D tiles or point clouds. One harvest scope per city or Landkreis app. Distinct from `masterportal` and `touviamaps`.

## MapStore (`mapstore`) {#mapstore}

GeoStore `/rest/geostore/` or backend CSW. Keep catalog/dataset resources. Drop saved **maps** and the MapStore UI chrome unless the user asked for maps.

## Terria (`terria`) {#terria}

Init `catalog.json` / `config.json` **members typed as data**. If Magda or CKAN on the same host already lists those datasets, harvest CKAN/Magda instead.

## GeoBlacklight (`geoblacklight`) {#geoblacklight}

```text
GET https://host/catalog.json
```

Geospatial items. Drop books/images when the Solr mix includes them. Page `start` / `rows` as in Blacklight.

## OpenGeoPortal (`opengeoportal`) {#opengeoportal}

Search/Solr **layers**, not institutions. Legacy paths vary — use `endpoints[]`.

## Koordinates (`koordinates`) {#koordinates}

```text
GET https://host/services/api/v1.x/data/
```

Data sets, not tile URLs.

## MapTiler Server (`maptilerserver`) {#maptilerserver}

```text
GET https://host/api
```

Harvest **maps / styles** the public catalog lists. Bare `/api/maps` 404s on some versions. Skip `/admin` and `logoOnly` tile backends. Do not harvest every XYZ tile.

## MapProxy (`mapproxy`) {#mapproxy}

WMTS/WMS GetCapabilities on the cache. Treat layers as datasets **only** if no parent SDI lists them. Most MapProxy instances duplicate GeoServer/MapServer — prefer the origin catalog.

## Tianditu (`tianditu`) {#tianditu}

Provincial/municipal 天地图 nodes. Harvest the node’s **layer/catalog API** if public. Skip pure tile hosts (`t0.tianditu.gov.cn` … `t7`), JS API keys (`tk=`), and `api.tianditu.gov.cn` token calls. One node = one harvest scope.

Backends vary; use `endpoints[]` when present. Common public catalogs:

```text
GET https://host/iserver/services.json
GET https://host/iportal/web/services.json
GET https://host/arcgis/rest/services?f=pjson
GET https://host/api/cityNode/queryByTree.json
```

Keep SuperMap services, iPortal maps/services, ArcGIS Map/Feature/Image services, or the city-node tree. Drop SSO, `console.tianditu.gov.cn` developer pages, and WMTS GetTile URLs.

## VertiGIS WebOffice (`weboffice`) {#weboffice}

Map UI first. Harvest CSW/WMS/REST when public. Do not scrape city-plan tiles.

## VertiGIS Studio Web (`vertigisstudioweb`) {#vertigisstudioweb}

Map UI first. App configuration is an ArcGIS Online / Portal item launched with `?app={guid}`. Harvest public CSW/WMS/REST on the same host when present. Do not treat each `?app=` GUID as a dataset, and do not scrape tiles. Distinct from Geocortex Essentials (`geocortex`) Sites Directory / Html5Viewer and VertiGIS WebOffice (`weboffice`). One harvest scope per public tenant.

## Geocortex Essentials (`geocortex`) {#geocortex}

List sites from the Essentials REST Sites Directory (`GET .../REST/sites?f=pjson`). Keep public sites as catalog applications. Drop Html5Viewer tiles, print PDFs, and per-layer identify results. If ArcGIS REST on the same host is already harvested, do not duplicate those services.

## ArcGIS Experience Builder (`experiencebuilder`) {#experiencebuilder}

Map UI first. App configuration is an ArcGIS Online / Portal item (or a Länsstyrelsen WebbGIS tenant). Harvest public CSW/WMS/REST on the same host when present. Do not scrape Jimu tiles or treat each widget as a dataset. One harvest scope per public app. Distinct from `webappbuilder` and `dmcity`.

## ArcGIS Web AppBuilder (`webappbuilder`) {#webappbuilder}

Map UI first. Harvest public REST/WMS on the same host when present. Do not scrape Web AppViewer tiles. One harvest scope per public `?id=` app. Distinct from `experiencebuilder` and `instantapps`.

## ArcGIS Instant Apps (`instantapps`) {#instantapps}

Map UI first. Harvest public REST/WMS on the same host when present. Do not scrape Instant App tiles. One harvest scope per public `appid`. Distinct from `experiencebuilder` and `webappbuilder`.

## Cadenza (`cadenza`) {#cadenza}

Map UI first. Harvest CSW/WMS/REST when public. Do not scrape workbook tiles.

## MangoMap (`mangomap`) {#mangomap}

Public MangoMap layer/catalog list if unauthenticated. Stop on `401`. Do not scrape map tiles.

## map.apps (`mapapps`) {#mapapps}

`/mapapps/` is a viewer — follow the backend catalog (CSW/ArcGIS). Do not scrape city-plan tiles.

## Wagmap (`wagmap`) {#wagmap}

GetCapabilities often missing or `403`. Harvest only a public CSW/WMS/REST catalog. Do not scrape わが街ガイド tiles.

## EWMAPA (`ewmapa`) {#ewmapa}

Polish geoportal2.pl. Same grain as [Wagmap](#wagmap): harvest only public CSW/WMS/REST. Do not scrape tiles.

## e-mapa.net (`emapa`) {#emapa}

Polish `*.e-mapa.net` SIP viewers (Geo-System Pandora). Same grain as [EWMAPA](#ewmapa): harvest only public CSW/WMS/REST. Do not scrape tiles. Distinct from `ewmapa`.

## Loftmyndir (`loftmyndir`) {#loftmyndir}

Icelandic `www.map.is/{muni}/` viewers. Harvest a public layer list or GetCapabilities if present. Do not scrape map tiles.

## Alta Vefsjá (`alta`) {#alta}

`geo.alta.is/{tenant}/` OpenLayers viewers. Harvest the public layer list. Do not harvest the GeoServer root here — that record is `geoserver`.

## Bulplan UNIMAP (`bulplan`) {#bulplan}

`{muni}.bulplan.eu` municipal geoportals. Harvest public layers or GetCapabilities. Do not scrape tiles.

## Tobel (`tobel`) {#tobel}

`{city}.tobel.bg` municipal GIS. Same grain as [Bulplan UNIMAP](#bulplan).

## geoportal.ch (`geoportalch`) {#geoportalch}

Swiss `www.geoportal.ch/{canton}` viewers. Harvest a public layer list or WMS. Distinct from [mf-geoadmin3](#mfgeoadmin3).

## InGrid (`ingrid`) {#ingrid}

German InGrid. CSW:

```text
GET https://host/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
GET https://host/interface/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
```

Keep ISO dataset/series. [harvest-protocols.md](harvest-protocols.md#csw).

## IsiGéo (`isigeo`) {#isigeo}

Geomatika SDI. Harvest `/api` if it lists layers/datasets; otherwise WMS GetCapabilities on the published workspace.

## MetaGIS (`metagis`) {#metagis}

```text
GET https://host/ResultJSONGNServlet
```

JSON layer/search results. Skip HTML search chrome.

## smart.finder SDI (`smartfindersdi`) {#smartfindersdi}

CSW or finder search. Keep ISO dataset/series metadata. Skip admin and the installer.

## MapBiomas (`mapbiomas`) {#mapbiomas}

Harvest annual land-cover **collections** on the country/program node. Do not treat every map click or year slider state as a dataset.

## CARTO (`carto`) {#carto}

Government/org Builder tenants only. Public named maps/datasets if the SQL or Maps API is unauthenticated. Stop on API keys (`401`). Do not `SELECT` every table. Skip carto.com marketing.

## SuperMap iServer (`supermapiserver`) {#supermapiserver}

```text
GET https://host/services.json
GET https://host/iserver/services.json
```

Keep published **datasets/services**. Drop tiles and admin.

## SuperMap iPortal (`supermapiportal`) {#supermapiportal}

Same `services.json` grain as [iServer](#supermapiserver) when the public product is iPortal. Drop tiles and admin.

## MapGIS IGServer (`mapgisigserver`) {#mapgisigserver}

```text
GET https://host/igs/rest/mrcs/docs?f=json
GET https://host/igs/rest/services?f=json
```

Keep published **map documents** (IGS 1.0) or **services** (IGS 2.0). Drop tiles, `/igs/manager` admin, and GetMap images. IGS 2.0 `/igs/rest/services` looks like ArcGIS REST — harvest it as MapGIS when the path is `/igs/rest/`, not `/arcgis/rest/`. Colombian HyG `/mapgis/mapa.jsp` is [`hygmapgis`](#hygmapgis), not this recipe.

## HyG Mapgis (`hygmapgis`) {#hygmapgis}

H&G Consultores `/mapgis/mapa.jsp?aplicacion=` or `/mapgis9/mapa.jsp?aplicacion=` viewer. Harvest the public **layer list** or OWS/ArcGIS URL exposed in the UI. Do not scrape map tiles. One harvest scope per `aplicacion=` on that host. If ArcGIS REST on the same Mapgis host is already harvested as `arcgisserver`, do not duplicate those services. Do not harvest Medellín `/mapgis9/` as a second catalog when GeoNetwork on `www.medellin.gov.co` is the public product. Not Zondy `/igs/rest/` (`mapgisigserver`).

## cardo (`cardo`) {#cardo}

Public UI under `/net3/public/`; WMS if published. Skip intranet cardo. Harvest GetCapabilities **layers** when that is the catalog.

## NetGIS Server (`netgisserver`) {#netgisserver}

`/Netgis7` or `/keos/`; optional `wms.ashx` GetCapabilities. Not Sampaş or GiSoftGis. Not WSP `/NetGISRuntime/` (`netgisruntime`).

## NetGIS Runtime (`netgisruntime`) {#netgisruntime}

Danish `/NetGISRuntime/basis/index.jsp` (often `?custid=` / `?alias=`). Harvest the public **theme / layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipal viewer. If ArcGIS REST on another host in the same kommune is already harvested as `arcgisserver`, do not duplicate those services. Distinct from Turkish `netgisserver`.

## GC Navi (`gcnavi`) {#gcnavi}

Tenant on `geocloud.jp/webgis/`. One municipality. Often no open GetCapabilities — stop rather than scraping tiles.

## ALANDIS+ (`alandis`) {#alandis}

`webgis.alandis.jp/{tenant}/` (or a custom host with `/alandis.jp/` assets). One municipality or prefecture per tenant. Often no open GetCapabilities — stop rather than scraping tiles.

## SonicWeb (`sonicweb`) {#sonicweb}

`www.sonicweb-asp.jp/{slug}/`. One municipality (or prefecture) per path tenant. Often no open GetCapabilities — stop rather than scraping tiles.

## GeDA-Public (`geogeo`) {#geogeo}

`{city}.geogeo.jp` or `{city}.e-map.geogeo.jp`. One municipality. Often no open GetCapabilities — stop rather than scraping tiles.

## Geolonia スマートマップ (`geoloniagis`) {#geoloniagis}

Tottori GeoMap `{org}.tottori-geomap.jp` or Kagawa BRIDGES. One public tenant. Distinct from Kazakhstan `smartmap`. Often no open GetCapabilities — stop rather than scraping tiles.

## NOL-IS (`nolis`) {#nolis}

Municipal WebGIS; harvest WMS/CSW if public.

## GiSoftGis (`gisoftgis`) {#gisoftgis}

Turkish city guide (`/GiSoftGis/`). Harvest WMS/REST if public. Do not treat the Angular hash router as a dataset list.

## Sampaş WebGIS (`sampaswebgis`) {#sampaswebgis}

`/KentrehberiApp/`. Same grain as [GiSoftGis](#gisoftgis).

## PopGIS (`popgis`) {#popgis}

SPC population/census GIS. Harvest the node’s **layer / table catalog**, not every map click. One country/territory node = one scope.

## ActiveMap (`activemapgis`) {#activemapgis}

Municipal map portal. Harvest the public layer tree or GetCapabilities. Skip Gradoservice / Panorama marketing.

## GIS WebServer SE (`giswebse`) {#giswebse}

Same grain as [ActiveMap](#activemapgis): public layer tree or GetCapabilities. Skip vendor marketing.

## Geonomics (`geonomics`) {#geonomics}

Viewer / local SDI. WMS or REST if public. Do not scrape Mapbox tiles.

## ORBISMap (`orbismap`) {#orbismap}

Same grain as [Geonomics](#geonomics).

## GeoPortal.rlp (`geoportalrlp`) {#geoportalrlp}

Open-source SDI (mrmap / Rheinland-Pfalz). Harvest **CSW** or published OWS **layers**, not the map HTML. Prefer CSW when both exist ([harvest-geoportals.md](harvest-geoportals.md), [harvest-protocols.md](harvest-protocols.md#csw)).

## GeoMedia WebMap (`geomediawebmap`) {#geomediawebmap}

Geospatial Portal under `/geoportal01/`, `/cdngiportal/`, or similar. Harvest WMS/WFS GetCapabilities or the portal’s layer list. Skip Intergraph marketing.

## mf-geoadmin3 (`mfgeoadmin3`) {#mfgeoadmin3}

Swiss geoadmin3 forks. Harvest `layersConfig` JSON (or WMS the config points at). Do not scrape map.geo.admin.ch tiles. Skip swisstopo marketing if you only needed an existing registry row.

## Re:Earth (`reearth`) {#reearth}

Cesium / PLATEAU VIEW. Harvest the public **catalog / scene dataset** API (CityGML or documented REST), not every 3D tile. One project = one harvest scope.

## GIS4Smart (`gis4smart`) {#gis4smart}

Municipal viewer (Y.Ge.P.). Harvest WMS/REST **layers** if public. Often no GetCapabilities — stop rather than scraping tiles.

## Evrymap (`evrymap`) {#evrymap}

Consortis Geospatial municipal map portal (often titled Evrymap; MapServer behind the SPA). Harvest public WMS GetCapabilities **layers** when the MapServer `map=` URL works. Do not scrape the Angular viewer tiles. Do not also register the bundled MapServer as a second catalog on the same host.

## BelsisIMS (`belsisims`) {#belsisims}

KRH city guide. Same grain as [GIS4Smart](#gis4smart). Not NetGIS or Sampaş.

## GP Atlas (`gpatlas`) {#gpatlas}

Regional web GIS. Harvest the public **layer / catalog** JSON or WMS. Skip login editors and vendor marketing.

## Geometa (`geometa`) {#geometa}

Gems Development GIS OGD public geoportal (Agate). Same grain as [GP Atlas](#gpatlas): harvest the public **document / layer catalog** JSON behind the SPA, not map tiles.

**Keep:** public planning-document lists, map-layer catalogs, and any documented GeoServer WMS/WFS GetCapabilities on the same tenant.

**Drop:** `/agate_` document-workflow screens that require login; the short “agat doesn’t work without JavaScript” stub as a catalog in itself; vendor marketing at geometa.ru.

Set `software.id: geometa` only when the public HTML matches Agate (title «Портал ГИСОГД», `agat` JS stub, `/agate_` paths, or `portal-gisogd.` / `agate.` hosts). Other `gisogd.*` sites without those signals stay `custom`.

## DATUM GIS (`datumgis`) {#datumgis}

Same grain as [GP Atlas](#gpatlas).

## EverGIS (`evergis`) {#evergis}

Same grain as [GP Atlas](#gpatlas).

## Ingeo (`ingeo`) {#ingeo}

Public GISOGD / layer list if any. Skip tiles and vendor marketing.

## Farvater GIS OGD (`farvatergisogd`) {#farvatergisogd}

Same grain as [Ingeo](#ingeo).

## Trimble Locus IMS (`trimblelocus`) {#trimblelocus}

Finnish `/IMS/` viewer. One harvest scope per city tenant.

Harvest public WMS/WFS GetCapabilities if the city publishes them. Do not scrape map tiles or the Locus back-office. Distinct from `belsisims` and from Sitowise Louhi (`louhi`). If a municipal GeoServer/ArcGIS catalog on the same city is already harvested, do not duplicate those layers.

## Sitowise Louhi (`louhi`) {#louhi}

Same grain as [Trimble Locus IMS](#trimblelocus): public layer list or WMS, not tiles.

## dmCity (`dmcity`) {#dmcity}

`web.dmcity.fi/{city}/public/`. Harvest the public **layer list** from the Experience Builder app if unauthenticated. Do not scrape Jimu tiles. One harvest scope per city tenant. Distinct from generic `experiencebuilder`. If `{city}.dmcity.fi/server` REST is already harvested as `arcgisserver`, do not duplicate those services.

## InfoGIS (`infogis`) {#infogis}

`www.infogis.fi/{municipality}/`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape OpenLayers tiles. One harvest scope per municipality path. Distinct from `louhi` and `trimblelocus`.

## Trimble Landfolio (`landfolio`) {#landfolio}

Harvest the public cadastre map-portal layer/license list if unauthenticated. If ArcGIS REST on the same estate is already harvested as `arcgisserver`, do not duplicate those services. Stop on login-only eGov modules.

## Hajk (`hajk`) {#hajk}

Swedish Hajk webGIS. Harvest the public layer/map list from the mapservice API documented in `appConfig.json` (`mapserviceBase`). Do not scrape map tiles. One harvest scope per public Hajk application. If GeoServer or ArcGIS REST on the same estate is already harvested as `geoserver` / `arcgisserver`, do not duplicate those services.

## Origo (`origo`) {#origo}

Origosamverkan Origo web GIS. Harvest the public layer list from the viewer JSON config or from WMS/WFS on the same host if already published as GeoServer. Do not scrape OpenLayers tiles. One harvest scope per municipality viewer, not per themed map path. Distinct from Hajk (`hajk`) and myCarta (`mycarta`). If GeoServer on the same host is already harvested as `geoserver`, do not duplicate those services.

## myCarta (`mycarta`) {#mycarta}

Aveki myCarta WebMap. Harvest the public layer list from the viewer (or WMS GetCapabilities if myCarta Server publishes it on the same host). Do not scrape map tiles. One harvest scope per municipality viewer, not per `#m=` map hash. Distinct from Hajk (`hajk`) on other Swedish `karta.*` hosts. Skip login-only myCarta GO.

## Spatial Suite (`spatialsuite`) {#spatialsuite}

Danish SpatialMap webkort. Harvest WMS/WFS GetCapabilities when public. Do not scrape webkort tiles. Prefer a city GeoServer/ArcGIS catalog on the same municipality if that is the dataset list.

## KortInfo (`kortinfo`) {#kortinfo}

NIRAS `drift.kortinfo.net/Map.aspx?Site=` tenant. Harvest the public layer list if unauthenticated. Do not scrape map tiles. One harvest scope per municipality `Site`, not per Map.aspx page. Distinct from `spatialsuite`.

## IntraMaps Public (`intramaps`) {#intramaps}

TechnologyOne IntraMaps Public tenant. Harvest the public **module / layer tree** from the viewer if unauthenticated. ApplicationEngine API paths often return `412` without a session — do not treat that as a catalog. Do not scrape map tiles (Google Maps or ApplicationEngine images). One harvest scope per public `project=` (typically `Public` / `*Public`), not per module. If ArcGIS REST or Hub on the same council is already harvested, do not duplicate those services. Skip login-only staff IntraMaps and eProperty maps.

## Spectrum Spatial Analyst (`spectrumspatial`) {#spectrumspatial}

Precisely Spectrum Spatial Analyst tenant (`/connect/analyst/` or `/connect/analyst/mobile/`). Harvest the public **map project / layer list** if unauthenticated. Named Feature Service tables may appear at `/connect/analyst/controller/connectProxy/rest/Spatial/FeatureService`. Do not scrape map tiles. One harvest scope per public Analyst tenant, not per `mapcfg=` project. Skip Spectrum Spatial Manager, login-only staff maps, and vendor demos. Do not harvest Exponare `/exponare/` as `spectrumspatial`.

## Exponare (`exponare`) {#exponare}

MapInfo Exponare public tenant (`/exponare/RestPublicApplication.aspx` or `/exponare/publicinvoker.aspx`). Harvest the public **layer list** from the viewer if unauthenticated. Do not scrape map tiles. One harvest scope per public tenant, not a second copy of Public vs REST vs Mobile on the same host. Skip staff-only Exponare Enquiry and PDF print exports.

## LocalMaps (`localmaps`) {#localmaps}

Eagle Technology NZ `/localmaps/gallery`. Harvest the **gallery map list**, not tiles and not the ArcGIS REST directory on the same host. One harvest scope per council gallery.

## GEUSMAP (`geusmap`) {#geusmap}

```text
GET https://host/geusmap/ows/25832.jsp?mapname={name}&SERVICE=WMS&REQUEST=GetCapabilities
GET https://host/geusmap/ows/25832.jsp?mapname={name}&SERVICE=WFS&REQUEST=GetCapabilities
```

One named layer = one dataset analog. Do not scrape map tiles. One harvest scope per `mapname`.

## GISApp (`gisapp`) {#gisapp}

Romanian `{city}.gisapp.ro` or PortalPublic / Fida city-host viewer. Harvest the public layer list if unauthenticated. Do not scrape map tiles or urbanism-permit forms. If ArcGIS REST on `webadaptor.gisapp.ro` is already harvested as `arcgisserver`, do not duplicate those services.

## PAGIS (`genegis`) {#genegis}

Italian `{comune}.servizigis.it` or city-host PAGIS SIT. Harvest the public cartographic **layer list** if unauthenticated. Do not scrape map tiles, CDU certificate forms, or civil-protection alert widgets. One harvest scope per municipality. Skip `services.servizigis.it` / `pagis.it`. Distinct from Pulaski `www.pagis.org` (`arcgisserver`).

## GisMaster (`gismaster`) {#gismaster}

Technical Design GeoPortale on `geoportale.sportellounicodigitale.it/GisMaster` with `IdCliente=`. Harvest the public layer list (cadastre, PRGC) or linked WMS/WFS GetCapabilities if unauthenticated. Do not scrape map tiles. One harvest scope per `IdCliente` tenant, not `Default.aspx` as a second copy of VisualDesc, and not cemetery `VisualCim` totems.

## SmartMap (`smartmap`) {#smartmap}

`{district}.smartmap.kz` investment viewer. Harvest the public **layer / object list** if unauthenticated. Do not scrape Google/Leaflet tiles. One harvest scope per district tenant. Distinct from `geonomics` and `rgis`.

## KAZGISA RGIS (`rgis`) {#rgis}

`{host}/map/` Angular Leaflet open-contour viewer. Harvest public **WMS GetCapabilities** when GeoServer is exposed, or the public layer tree if unauthenticated. Do not scrape Leaflet tiles. One harvest scope per akimat or city geoportal. Distinct from `geonomics`, `smartmap`, and `vkomap`. Skip the older KAZGISA OpenLayers stack (`eatyrau.kz`).

## eKMap Cloud (`ekmap`) {#ekmap}

Provincial `{host}` planning viewer with `assets/ekmapboxgl/ekmap-mapboxgl.js`. Harvest the public **planning-layer / dossier list** if unauthenticated. Do not scrape Mapbox tiles. One harvest scope per province or city geoportal. Distinct from Hanoi `quyhoach.hanoi.gov.vn`, Vinh Phuc OpenLayers planning, and HCMC VLAB.

## VKOMAP (`vkomap`) {#vkomap}

```text
GET https://host/Public/GetKatoList
GET https://host/Public/GetLayers?kato={code}
```

Keep named layers from `GetLayers` (pass a `kato` from `GetKatoList`; bare `GetLayers` returns an empty list). Do not scrape Leaflet/Esri tiles. One harvest scope per akimat or city tenant. Distinct from `geonomics`, `smartmap`, and `rgis`.

## Visor Urbano (`visorurbano`) {#visorurbano}

`visorurbano.{city}.gob.mx` or `{city}.visorurbano.com`. Harvest the public **parcel / zoning layer list** if unauthenticated. Do not scrape map tiles or scrape licence-application forms. One harvest scope per municipality tenant. Skip `www.visorguadalupe.com`. Distinct from `doblesvisor`.

## Dobles Visor de Mapas (`doblesvisor`) {#doblesvisor}

Costa Rican `/comun/` Leaflet visor. Harvest the public **layer list** from the visor UI if unauthenticated. Do not scrape Leaflet/Google tiles. One harvest scope per municipality. Distinct from CR ArcGIS Experience visors and from MapStore/GeoNetwork.

## GeoNube (`geonube`) {#geonube}

`geonube.com.ar/visor/{slug}` or a custom domain that embeds those visors. Harvest the public **layer list** from the visor if unauthenticated. Do not scrape Leaflet tiles. One harvest scope per municipality or organisation tenant, not per map inside the same tenant. Distinct from `doblesvisor`.

## Geopixel Cidades (`geopixel`) {#geopixel}

`{city}.geoportal.geopixel.com.br`. Harvest `/api/pages` city config and the public **map/layer list** when the API responds. Do not scrape map tiles. One harvest scope per municipality. Do not treat the DNS wildcard as extra catalogs.

## CTMGEO SigWEB (`ctmgeo`) {#ctmgeo}

`{city}.ctmgeo.com.br/mapa/`. Harvest the public **cadastral lot / layer list**. Do not scrape map tiles. One harvest scope per municipality. Distinct from unrelated SIGWeb titles on other hosts.

## ISY Map (`isymap`) {#isymap}

Norconsult ISY Map / GeoInnsyn / ISY Map Server. Harvest public WMS/WFS GetCapabilities or the viewer layer tree. Do not scrape `/webkart/` PNG/SVG tiles. One harvest scope per municipality application (`application=` / `project=`), not per coordinate permalink.

## Avinet Adaptive (`avinet`) {#avinet}

```text
GET https://host/wms.ashx?service=WMS&request=GetCapabilities
GET https://host/wfs.ashx?service=WFS&request=GetCapabilities
```

Keep named WMS/WFS layers. Do not scrape ExtJS map tiles. One harvest scope per public atlas. Distinct from `isymap`.

## MAP+ (`mapplus`) {#mapplus}

TYDAC `/mapplus/` or `/mapplus-lib/` Stadtplan. Harvest the public **layer list** if unauthenticated. Do not scrape OpenLayers tiles. One harvest scope per municipality viewer. Distinct from `geomapfish` and `mfgeoadmin3`.

## EnviMAP (`envimap`) {#envimap}

`*.envimap.hu` or `/hu/Admin/GeoForte/GeoEdit` zoning viewer. Harvest the public layer / parcel query if unauthenticated. Do not scrape Leaflet tiles. One harvest scope per municipality tenant.

## PISO (`piso`) {#piso}

geoprostor.net / PisoPortal hub. Harvest public WMS or the municipality layer list. Do not scrape map tiles. One harvest scope for the hub (not per občina in the selector) unless a municipality exposes a separate catalog API.

## GDi Visios (`gdivisios`) {#gdivisios}

`/visios/{app}` or GDi-hosted Ensemble Smart Portal viewer. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality or county application. Distinct from ArcGIS REST on `gdi.net`.

## MapGuide (`mapguide`) {#mapguide}

`/mapguide/` CityScape or `mapviewerphp/ajaxviewer.php`. Harvest the public **layer / legend catalog** if unauthenticated. Do not scrape MapGuide tiles. One harvest scope per municipality. Distinct from `envimap` and `sigimweb`.

## SIGimWeb (`sigimweb`) {#sigimweb}

`/sigimweb/` or `/sigim/` with title `SIGimWeb`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape ExtJS / GoMap tiles. One harvest scope per public MRC or city tenant, not per municipality in the picker. Distinct from `mapguide`. Skip intranet and JP Cadrin CIF replacements.

## SeaSketch (`seasketch`) {#seasketch}

`www.seasketch.org/{project}/app`. Harvest public overlay **layer groups** if unauthenticated. Do not scrape map tiles or require a sketching account. One harvest scope per project slug. Distinct from `data.seasketch.org` ArcGIS REST (`arcgisserver`).

## XY Maps (`xymaps`) {#xymaps}

`maps.xymaps.com/{city}` or city-host `/xymaps/Map`. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per public city tenant. `www.xymaps.com/{city}` is the same SaaS host. Distinct from Geocortex/ArcGIS that Eckersall also deploys. Skip the marketing homepage and private floorplan dumps.

## GISPLAN (`gisplan`) {#gisplan}

T-MAPY `{city}.gisplan.sk`, Czech `{muni}.gis4u.cz`, `{city}.tmapserver.cz`, or city-host Spinbox / T-WIST gallery. Harvest the public `/mapa/` or T-WIST application list if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per municipality. Distinct from `gisapp`, `iobcina`, `gepro`, `gisonline`, `mapotip`, `cgwebgis`, `mobec`, `georeal`, and `geodeticca`. T-MAPY MapProxy on `services7.tmapserver.cz` is `mapproxy`.

## mOBEC (`mobec`) {#mobec}

`mobec.sk/{slug}`. Harvest the public **Všeobecná mapa** / layer list if unauthenticated. Do not scrape map tiles or require a staff login. One harvest scope per municipality slug. Distinct from `gisplan`. Skip the marketing home.

## CG WebGIS (`cgwebgis`) {#cgwebgis}

`webgis.{city}.sk` or a city host with title `WebGIS v2, CG`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality. Distinct from `gisplan` and `geodeticca`.

## Geodeticca WEB GIS (`geodeticca`) {#geodeticca}

`gis.{city}.sk` titled `Geodeticca WEB GIS`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality. Distinct from `cgwebgis` and `gisplan`. Skip Michalovce `michalovce.web-gis.sk`.

## Geoportál GEPRO (`gepro`) {#gepro}

`{city}.obce.gepro.cz` or `{city}.gepro.cz`. Harvest the public **layer / theme list** from the `/OUT/HTML/` viewer if unauthenticated, or WMS/WFS GetCapabilities when those are public. Do not scrape OpenLayers tiles. One harvest scope per municipality. Distinct from `gisplan`. Skip login-only intranet tenants.

## KOVGIS EVALD (`evald`) {#evald}

`evald.ee/{slug}/` (not `service.eomap.ee` aliases). Harvest the public **layer / module catalog** (detailplaneeringud, geoarhiiv, munitsipaalmaad, teemainfo) if unauthenticated. Do not scrape map tiles or authenticated geoarchive file downloads. One harvest scope per public tenant slug (municipalities, nationwide `eesti`, ELVL). Distinct from `arcgisserver` `gis.{muni}.ee` portals. Skip `403` tenants (Ruhnu) and `evald2_*` session URLs.

## terGIS (`tergis`) {#tergis}

`{tenant}.tergis.lv`. Harvest `/api/v1/classifiers/layers` on Angular SPA tenants, or `/themes.json` layers on QWC2-frontend tenants, if unauthenticated. Do not scrape map tiles or follow the login form. One harvest scope per public tenant. Distinct from generic `qwc2` off `tergis.lv`. Skip `tergis.lv` marketing, `401`, and `502` tenants.

## Pozi (`pozi`) {#pozi}

`{council}.pozi.com`. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per public council subdomain. Distinct from `intramaps` and `exponare`. Skip the marketing homepage.

## JMap (`jmap`) {#jmap}

`/JMapWeb/` or JMap NG `/services/ng/`. Harvest the public **layer / project list** if unauthenticated. Do not scrape map tiles or require JMap Admin. One harvest scope per public tenant or project. Distinct from ArcGIS viewers. Skip hostnames that merely contain `jmap`.

## GIS Cloud (`giscloud`) {#giscloud}

`{city}.giscloud.com`. Harvest the public **layer list** if unauthenticated. Do not scrape tiles or require Map Editor login. One harvest scope per public tenant. Distinct from generic Leaflet.

## MRF Web Map (`mrf`) {#mrf}

`{county}.mrf.com` or a host loading `js/lib/mrf/`. Harvest the public **layer list** after the guest disclaimer if unauthenticated. Do not scrape tiles or require staff login. One harvest scope per public tenant. Distinct from `giscloud`. Skip `web.munisight.com` (`munisight`).

## MuniSight (`munisight`) {#munisight}

`web.munisight.com/{Tenant}`. Harvest only if a public guest map exists. Do not scrape tiles or follow staff Login.aspx. One harvest scope per municipality tenant. Distinct from `mrf` and `geomediawebmap`. Skip the marketing homepage.

## GeoMedia SmartClient Public Maps (`publicmaps`) {#publicmaps}

`publicmaps.gisquadrat.com/BP/WEPM.aspx?site=GMSC&project={TOWN}`. Harvest the public **layer / map-view list** from `/GMSC/PUBLIC/Configuration` if unauthenticated. Do not scrape map tiles. One harvest scope per municipal `project=` tenant. Distinct from `geomediawebmap` and `erdasapollo`. Skip the marketing homepage and retired `gis-klagenfurt.at`.

## SIT WebGis (`sitwebgis`) {#sitwebgis}

`webgis.sit-puglia.it/{comune}/`. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipal tenant. Distinct from Regione Puglia `geonetwork` on `repertorio.sit.puglia.it`. Skip the marketing homepage and stale `/mola` and `/potenza` slugs.

## p.mapper (`pmapper`) {#pmapper}

`/pmapper/` or `{city}.geo-portale.it`. Harvest WMS GetCapabilities or the p.mapper layer tree. Do not scrape map images. One harvest scope per municipality or SIT. Distinct from UMN `mapserver` as the public catalog.

## CommunityView (`communityview`) {#communityview}

`maps.digitalmapcentral.com/production/VECommunityView/cities/{city}/`. Harvest the public **layer list** if unauthenticated. Do not scrape Bing basemap tiles. One harvest scope per city slug.

## MS-GIS (`msgis`) {#msgis}

`{city}.msgis.net`. Harvest the public **layer / theme list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality. Distinct from `masterportal` and `touviamaps`.

## Weave (`weave`) {#weave}

Title `Weave Map` on Australian council domains. Harvest the public **layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per council viewer. Distinct from `intramaps`, `exponare`, and `pozi`. Skip GeneWeaver and other hosts that merely contain the word weave.

## OVIE (`ovie`) {#ovie}

INEGI municipal economic GIS (`/js/libs/OpenLayers/OL.js`). Harvest the public **layer / indicator list** if unauthenticated. Do not scrape map tiles or print PDFs. One harvest scope per municipality or state OVIE. Distinct from INEGI Gaia `/mdm6/` (`mxsig`). Skip Mission Viejo `geoviewer.io`.

## SOFTPRO (`softpro`) {#softpro}

`{city}.cadastre.com.ua` or city MBK hosts that mention SOFTPRO. Harvest the public **layer / cadastre list** if unauthenticated. Do not scrape map tiles. One harvest scope per community or oblast portal. Distinct from `kadastr.gov.ua` and `map.land.gov.ua`.

## MxSIG (`mxsig`) {#mxsig}

`/mdm6/` or `/mxsig2/` Mapa Digital de México. Harvest public **WMS / layer list** if unauthenticated. Do not scrape map tiles. One harvest scope per MDM6 viewer, not an indicators CMS on the same host. Distinct from `ovie`.

## GisOnline (`gisonline`) {#gisonline}

`app.gisonline.cz/{city}`. Harvest the public **layer / pasport list** if unauthenticated. Do not scrape map tiles or panorama imagery. One harvest scope per city slug. Distinct from `gisplan` and `gepro`.

## K5 MapServer (`k5mapserver`) {#k5mapserver}

`{muni}.k5mapserver.cz`. Harvest the public map / pasport catalog from the GEOPORTÁL home if unauthenticated. Do not scrape map tiles. One harvest scope per municipality subdomain. Distinct from UMN `mapserver`.

## Marushka (`marushka`) {#marushka}

GEOVAP Marushka HTML client. Harvest WMS/WFS GetCapabilities when Marushka publishes them, or the public project/layer list. Do not scrape map tiles. One harvest scope per city installation. Distinct from `gisplan`, `gepro`, and `georeal`.

## Georeal (`georeal`) {#georeal}

Czech kraj `{host}/portal/` CMS with `Georeal.Cards`. Harvest the public **application / map-card catalog** if unauthenticated, or WMS/WMTS GetCapabilities when those are public. Do not scrape map tiles. One harvest scope per DTM or geoportal product. Distinct from `gisplan`, `gepro`, and `marushka`. Skip `/portal/` shells without `Georeal.Cards`.

## Mapotip (`mapotip`) {#mapotip}

`portal.mapotip.cz/{municipality}`. Harvest the public **layer / pasport list** if unauthenticated. Do not scrape map tiles. One harvest scope per municipality slug. Distinct from `gisplan`, `gepro`, and `gisonline`. Skip the demo tenant.

## giscity (`giscity`) {#giscity}

`www.gisserver.de/{city}/`. Harvest the public **theme / map catalog** if unauthenticated. Do not scrape map tiles. One harvest scope per city path. Distinct from ArcGIS Hub catalogs whose hostname contains `giscityof`.

## iObčina (`iobcina`) {#iobcina}

Kaliopa `/gisapp/Default.aspx?a={tenant}` viewer. Harvest public layers for that tenant. Do not scrape tiles. Distinct from `gisapp`.

## Astun iShare (`ishare`) {#ishare}

UK My Maps / My House portal. Harvest the public **layer / local-info catalog** if unauthenticated, or WMS/WFS GetCapabilities when those are public. Do not scrape map tiles or address-search HTML. Distinct from `cadcorp`.

## Cadcorp SIS WebMap (`cadcorp`) {#cadcorp}

Public SIS WebMap / Web Map Layers. Harvest WMS/WFS GetCapabilities or the published layer list. Do not scrape tiles. Distinct from disy Cadenza (`cadenza`) and from Astun iShare (`ishare`).

## Related

- [harvest.md](harvest.md)
- [harvest-geoportals.md](harvest-geoportals.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [discovery-geoportals.md](discovery-geoportals.md)
- [agents/harvest.md](agents/harvest.md)
