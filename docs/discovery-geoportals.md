# Discovering geoportals

How to find **geoportal** installations (`catalog_type: Geoportal`). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). If a site is both a map viewer and a dataset portal, pick the **primary** product ([catalog-types.md](catalog-types.md)). One public catalog UI = one registry record — see [one catalog per host](discovery.md#one-catalog-per-public-product).

Fingerprints live on two pages so this overview stays short:

| Page | Use when |
|------|----------|
| [SDI platforms](discovery-geoportals-sdi.md) | GeoNetwork, GeoNode, Palapa, GeoServer, ArcGIS, Experience Builder, Web AppBuilder, STAC, openEO, Sentinel Hub, Lizmap, QGIS Server, G3W-SUITE, CubeWerx, M.App Enterprise, mviewer, Isogeo, Geocortex, MapServer, and other catalog/service stacks |
| [Regional viewers](discovery-geoportals-viewers.md) | Wagmap, SonicWeb, GeDA-Public, ALANDIS+, Geolonia スマートマップ, EWMAPA, e-mapa.net, Loftmyndir, Alta Vefsjá, Tianditu, Masterportal, GeoMapFish, NetGIS Server, NetGIS Runtime, cardo, MapGIS IGServer, HyG Mapgis, Trimble Locus / Louhi / Landfolio, dmCity, InfoGIS, Spatial Suite, Hajk, myCarta, AddSpatial, KortInfo, IntraMaps Public, Spectrum Spatial Analyst, Exponare, LocalMaps, GEUSMAP, GISApp, GeneGIS PAGIS, GisMaster, SmartMap, VKOMAP, ISY Map, Avinet Adaptive, MAP+, EnviMAP, PISO, GDi Visios, MapGuide, SeaSketch, iObčina, iShare, Cadcorp, Visor Urbano, Dobles Visor de Mapas, and municipal GIS viewers |

All `software.id` values: [software-index.md](software-index.md). Harvest grain (layers vs tiles): [harvest-geoportals.md](harvest-geoportals.md), [harvest-viewers.md](harvest-viewers.md).

## Core SDI (short list)

Confirm with a GET on the candidate host only. Stop on `401`/`403`.

| If you see | `software.id` | Full fingerprints |
|------------|---------------|-------------------|
| `/srv/eng/csw` or `/srv/api` | `geonetwork` | [SDI](discovery-geoportals-sdi.md#geonetwork) |
| `/api/layers/` or `/api/datasets/` | `geonode` | [SDI](discovery-geoportals-sdi.md#geonode) |
| Title “Geoportal Palapa” / `/main/` or `/gspalapa/` | `palapa` | [SDI](discovery-geoportals-sdi.md#palapa) |
| `/geoserver/ows` GetCapabilities | `geoserver` | [SDI](discovery-geoportals-sdi.md#geoserver) |
| Hub search / `opendata-ui` / `/portal/apps/sites/` | `arcgishub` | [SDI](discovery-geoportals-sdi.md#arcgishub) |
| `/arcgis/rest/info?f=pjson` | `arcgisserver` | [SDI](discovery-geoportals-sdi.md#arcgisserver) |
| `experience.arcgis.com/experience/` or `jimu-core/init.js` | `experiencebuilder` | [SDI](discovery-geoportals-sdi.md#experiencebuilder) |
| `/apps/webappviewer/` or self-hosted `env.js` + Jimu | `webappbuilder` | [SDI](discovery-geoportals-sdi.md#webappbuilder) |
| `/apps/dashboards/{item-id}` | `arcgisdashboards` | [SDI](discovery-geoportals-sdi.md#arcgisdashboards) |
| `/apps/instant/{template}/?appid=` | `instantapps` | [SDI](discovery-geoportals-sdi.md#instantapps) |
| STAC `/collections` JSON | `stacserver` | [SDI](discovery-geoportals-sdi.md#stacserver) |
| STAC Browser HTML only | `stacbrowser` | [SDI](discovery-geoportals-sdi.md#stacbrowser) |
| `/.well-known/openeo` | `openeo` | [SDI](discovery-geoportals-sdi.md#openeo) |
| `qgis_mapserv.fcgi` as the public catalog | `qgisserver` | [SDI](discovery-geoportals-sdi.md#qgisserver) |
| mviewer `/apps/*.xml` | `mviewer` | [SDI](discovery-geoportals-sdi.md#mviewer) |
| Finnish `/IMS/` karttapalvelu | `trimblelocus` | [viewers](discovery-geoportals-viewers.md#trimblelocus) |
| Sitowise Louhi karttapalvelu | `louhi` | [viewers](discovery-geoportals-viewers.md#louhi) |
| `portals.landfolio.com` cadastre map | `landfolio` | [viewers](discovery-geoportals-viewers.md#landfolio) |
| SpatialMap `webkort` | `spatialsuite` | [viewers](discovery-geoportals-viewers.md#spatialsuite) |
| Hajk `appConfig.json` / `mapserviceBase` | `hajk` | [viewers](discovery-geoportals-viewers.md#hajk) |
| Origo `origo.min.js` / `Origo(` | `origo` | [viewers](discovery-geoportals-viewers.md#origo) |
| myCarta WebMap title / `/webmap/` / `/mycartawebmap/` | `mycarta` | [viewers](discovery-geoportals-viewers.md#mycarta) |
| AddSpatial title / `/smart/?profile=` | `addspatial` | [viewers](discovery-geoportals-viewers.md#addspatial) |
| `drift.kortinfo.net/Map.aspx` | `kortinfo` | [viewers](discovery-geoportals-viewers.md#kortinfo) |
| IntraMaps Public `project=` / `*.spatial.t1cloud.com` | `intramaps` | [viewers](discovery-geoportals-viewers.md#intramaps) |
| `/connect/analyst/` Spectrum Spatial Analyst | `spectrumspatial` | [viewers](discovery-geoportals-viewers.md#spectrumspatial) |
| `/exponare/` RestPublicApplication | `exponare` | [viewers](discovery-geoportals-viewers.md#exponare) |
| LocalMaps `/localmaps/gallery` | `localmaps` | [viewers](discovery-geoportals-viewers.md#localmaps) |
| `/geusmap/?mapname=` | `geusmap` | [viewers](discovery-geoportals-viewers.md#geusmap) |
| `*.gisapp.ro` or PortalPublic `logo_fida.png` | `gisapp` | [viewers](discovery-geoportals-viewers.md#gisapp) |
| Argenmap `src/js/app.js` and retained IGN template | `argenmap` | [viewers](discovery-geoportals-viewers.md#argenmap) |
| `/AvanMap/` plus `initAvanMap.js` | `avanmap` | [viewers](discovery-geoportals-viewers.md#avanmap) |
| Title `WebEWID` / Portal Mapowy | `webewid` | [viewers](discovery-geoportals-viewers.md#webewid) |
| `gms*.kc-systemhaus.de/BMApp/` | `kcwebgis` | [viewers](discovery-geoportals-viewers.md#kcwebgis) |
| `{comune}.servizigis.it` or “GeneGis Site Creator” / App PAGIS | `genegis` | [viewers](discovery-geoportals-viewers.md#genegis) |
| `geoportale.sportellounicodigitale.it/GisMaster` `IdCliente=` | `gismaster` | [viewers](discovery-geoportals-viewers.md#gismaster) |
| `{district}.smartmap.kz` | `smartmap` | [viewers](discovery-geoportals-viewers.md#smartmap) |
| KZ `/vkomap/` Leaflet + Esri | `vkomap` | [viewers](discovery-geoportals-viewers.md#vkomap) |
| KZ `{host}/map/` Angular Leaflet RGIS | `rgis` | [viewers](discovery-geoportals-viewers.md#rgis) |
| ISY Map `/geoinnsyn/` or `/webkart/` | `isymap` | [viewers](discovery-geoportals-viewers.md#isymap) |
| Avinet Adaptive ExtJS atlas | `avinet` | [viewers](discovery-geoportals-viewers.md#avinet) |
| TYDAC MAP+ `/mapplus-lib/` | `mapplus` | [viewers](discovery-geoportals-viewers.md#mapplus) |
| EnviMAP / GeoForte | `envimap` | [viewers](discovery-geoportals-viewers.md#envimap) |
| PISO geoprostor.net | `piso` | [viewers](discovery-geoportals-viewers.md#piso) |
| GDi Visios `/visios/` | `gdivisios` | [viewers](discovery-geoportals-viewers.md#gdivisios) |
| MapGuide `/mapguide/` | `mapguide` | [viewers](discovery-geoportals-viewers.md#mapguide) |
| SeaSketch `/{project}/app` | `seasketch` | [viewers](discovery-geoportals-viewers.md#seasketch) |
| `maps.xymaps.com/{city}` or `/xymaps/Map` title XY MAPS | `xymaps` | [viewers](discovery-geoportals-viewers.md#xymaps) |
| Kaliopa iObčina / iOpćina | `iobcina` | [viewers](discovery-geoportals-viewers.md#iobcina) |
| `{city}.gisplan.sk` / T-MAPY Spinbox / GIS4U / tmapserver | `gisplan` | [viewers](discovery-geoportals-viewers.md#gisplan) |
| `mobec.sk/{slug}` T-MAPY mOBEC | `mobec` | [viewers](discovery-geoportals-viewers.md#mobec) |
| `webgis.{city}.sk` CG WebGIS | `cgwebgis` | [viewers](discovery-geoportals-viewers.md#cgwebgis) |
| `gis.{city}.sk` title Geodeticca WEB GIS | `geodeticca` | [viewers](discovery-geoportals-viewers.md#geodeticca) |
| `{city}.obce.gepro.cz` / Geoportál GEPRO | `gepro` | [viewers](discovery-geoportals-viewers.md#gepro) |
| `evald.ee/{slug}/` KOVGIS EVALD | `evald` | [viewers](discovery-geoportals-viewers.md#evald) |
| `{tenant}.tergis.lv` terGIS | `tergis` | [viewers](discovery-geoportals-viewers.md#tergis) |
| `{council}.pozi.com` title Pozi Web Map | `pozi` | [viewers](discovery-geoportals-viewers.md#pozi) |
| `/JMapWeb/` or JMap NG `jmapserver-ng` | `jmap` | [viewers](discovery-geoportals-viewers.md#jmap) |
| `{city}.giscloud.com` GIS Cloud | `giscloud` | [viewers](discovery-geoportals-viewers.md#giscloud) |
| `{county}.mrf.com` / `js/lib/mrf/` MRF Web Map | `mrf` | [viewers](discovery-geoportals-viewers.md#mrf) |
| `web.munisight.com/{Tenant}` Catalis Login.aspx | `munisight` | [viewers](discovery-geoportals-viewers.md#munisight) |
| `/pmapper/` or `{city}.geo-portale.it` p.mapper | `pmapper` | [viewers](discovery-geoportals-viewers.md#pmapper) |
| `VECommunityView/cities/{city}/` CommunityView | `communityview` | [viewers](discovery-geoportals-viewers.md#communityview) |
| `{city}.msgis.net` title GeoInformation | `msgis` | [viewers](discovery-geoportals-viewers.md#msgis) |
| Title `Weave Map` webpack `app.*.js` | `weave` | [viewers](discovery-geoportals-viewers.md#weave) |
| OVIE `/js/libs/OpenLayers/OL.js` + Materialize | `ovie` | [viewers](discovery-geoportals-viewers.md#ovie) |
| `{city}.cadastre.com.ua` or SOFTPRO `/js/locale/ua.js` | `softpro` | [viewers](discovery-geoportals-viewers.md#softpro) |
| `/mdm6/` or `/mxsig2/` amplify.js Mapa Digital | `mxsig` | [viewers](discovery-geoportals-viewers.md#mxsig) |
| `app.gisonline.cz/{city}` TopGis | `gisonline` | [viewers](discovery-geoportals-viewers.md#gisonline) |
| `{muni}.k5mapserver.cz` MK Consult | `k5mapserver` | [viewers](discovery-geoportals-viewers.md#k5mapserver) |
| Marushka `zipped.js` / `js/marushka.js` | `marushka` | [viewers](discovery-geoportals-viewers.md#marushka) |
| `{dtm|geoportal}.{kraj}.cz/portal/` Georeal.Cards | `georeal` | [viewers](discovery-geoportals-viewers.md#georeal) |
| `portal.mapotip.cz/{obec}` | `mapotip` | [viewers](discovery-geoportals-viewers.md#mapotip) |
| `www.gisserver.de/{city}/` ibb giscity | `giscity` | [viewers](discovery-geoportals-viewers.md#giscity) |
| `vianovis.net/{tenant}/` touvia.MAPS | `touviamaps` | [viewers](discovery-geoportals-viewers.md#touviamaps) |
| `INGRADA online` / `Softplan.Ingrada.Mobile` | `ingrada` | [viewers](discovery-geoportals-viewers.md#ingrada) |
| `html.vcs-ui` title VC Map | `vcmap` | [viewers](discovery-geoportals-viewers.md#vcmap) |
| G3W-CLIENT / `/map/{group}/` QGIS WebGIS | `g3wsuite` | [SDI](discovery-geoportals-sdi.md#g3wsuite) |
| MapCentia `/apps/viewer` or `/mapcache/` WMTS | `gc2` | [SDI](discovery-geoportals-sdi.md#gc2) |
| hale»connect CSW `/csw` or `/ows/services/` | `haleconnect` | [SDI](discovery-geoportals-sdi.md#haleconnect) |
| “Powered by iShare” / `mymaps.aspx` | `ishare` | [viewers](discovery-geoportals-viewers.md#ishare) |
| Cadcorp SIS WebMap / GeognoSIS | `cadcorp` | [viewers](discovery-geoportals-viewers.md#cadcorp) |
| Hexagon M.App `/Apps/` | `mappenterprise` | [SDI](discovery-geoportals-sdi.md#mappenterprise) |
| `/cubewerx/cubeserv` GetCapabilities | `cubewerx` | [SDI](discovery-geoportals-sdi.md#cubewerx) |
| Sentinel Hub STAC `/api/v1/catalog` | `sentinelhub` | [SDI](discovery-geoportals-sdi.md#sentinelhub) |
| Isogeo OpenCatalog `/api` | `isogeo` | [SDI](discovery-geoportals-sdi.md#isogeo) |
| `/Geocortex/Essentials/REST/sites` | `geocortex` | [SDI](discovery-geoportals-sdi.md#geocortex) |
| `/vertigisstudio/web/?app=` or `/gcx/WebViewer/` | `vertigisstudioweb` | [SDI](discovery-geoportals-sdi.md#vertigisstudioweb) |
| `/igs/rest/mrcs/docs` | `mapgisigserver` | [viewers](discovery-geoportals-viewers.md#mapgisigserver) |
| `/mapgis/mapa.jsp` or `/mapgis9/mapa.jsp` (HyG footer) | `hygmapgis` | [viewers](discovery-geoportals-viewers.md#hygmapgis) |
| `www2.wagmap.jp` | `wagmap` | [viewers](discovery-geoportals-viewers.md#wagmap) |
| `www.sonicweb-asp.jp/{slug}/` | `sonicweb` | [viewers](discovery-geoportals-viewers.md#sonicweb) |
| `webgis.alandis.jp/{tenant}/` | `alandis` | [viewers](discovery-geoportals-viewers.md#alandis) |
| `{city}.geogeo.jp` | `geogeo` | [viewers](discovery-geoportals-viewers.md#geogeo) |
| `{org}.tottori-geomap.jp` | `geoloniagis` | [viewers](discovery-geoportals-viewers.md#geoloniagis) |
| `{powiat}.e-mapa.net` | `emapa` | [viewers](discovery-geoportals-viewers.md#emapa) |
| `www.map.is/{muni}/` | `loftmyndir` | [viewers](discovery-geoportals-viewers.md#loftmyndir) |
| `geo.alta.is/{tenant}/` viewer | `alta` | [viewers](discovery-geoportals-viewers.md#alta) |
| `visorurbano.{city}.gob.mx` or `{city}.visorurbano.com` | `visorurbano` | [viewers](discovery-geoportals-viewers.md#visorurbano) |
| CR `/comun/js/leaflet.js` + Leaflet.GoogleMutant | `doblesvisor` | [viewers](discovery-geoportals-viewers.md#doblesvisor) |
| `geonube.com.ar/visor/{slug}` | `geonube` | [viewers](discovery-geoportals-viewers.md#geonube) |
| `{city}.geoportal.geopixel.com.br` | `geopixel` | [viewers](discovery-geoportals-viewers.md#geopixel) |
| `{city}.ctmgeo.com.br/mapa/` | `ctmgeo` | [viewers](discovery-geoportals-viewers.md#ctmgeo) |
| `{city}.gisplan.sk` or T-MAPY Spinbox / GIS4U / `tmapy.svg` | `gisplan` | [viewers](discovery-geoportals-viewers.md#gisplan) |
| `mobec.sk/{slug}` T-MAPY mOBEC / `tmapyn.svg` | `mobec` | [viewers](discovery-geoportals-viewers.md#mobec) |
| `web.dmcity.fi/{city}/public/` | `dmcity` | [viewers](discovery-geoportals-viewers.md#dmcity) |
| `www.infogis.fi/{muni}/` | `infogis` | [viewers](discovery-geoportals-viewers.md#infogis) |
| `/sigimweb/` title SIGimWeb or `/gomap_web/` | `sigimweb` | [viewers](discovery-geoportals-viewers.md#sigimweb) |
| `/NetGISRuntime/basis/index.jsp` title WSP NetGIS | `netgisruntime` | [viewers](discovery-geoportals-viewers.md#netgisruntime) |
| `/CartoVistaServer/maps/view` / `cartovistawebportal-*` | `cartovista` | [viewers](discovery-geoportals-viewers.md#cartovista) |
| Exact IGO2 title and JSON contexts | `igo2` | [viewers](discovery-geoportals-viewers.md#igo2) |
| Title `InfoMap Map Portal` / Emtel header | `infomap` | [viewers](discovery-geoportals-viewers.md#infomap) |
| `/bios/dpwebmap/` / `DPWebApp.nocache.js` | `dpwebmap` | [viewers](discovery-geoportals-viewers.md#dpwebmap) |
| 3MAP `GISProjectListing_mini.js` / `/desk/` assets | `3map` | [viewers](discovery-geoportals-viewers.md#3map) |
| Title `Facta WebGIS 4.0` plus `facta.css` | `factawebgis` | [viewers](discovery-geoportals-viewers.md#factawebgis) |
| `inkasPortal - GeoNet Online GmbH` / `inkas-portal.js` | `inkasportal` | [viewers](discovery-geoportals-viewers.md#inkasportal) |
| `geoviewer.io/css/nobel-style.css` | `geoviewer` | [viewers](discovery-geoportals-viewers.md#geoviewer) |
| `my.floodreport.com.au/{authority}` Water Technology iframe | `floodintelligenceportal` | [viewers](discovery-geoportals-viewers.md#floodintelligenceportal) |
| `*.pgis.lv`, title `pGIS`, layer-classifier API | `pgis` | [viewers](discovery-geoportals-viewers.md#pgis) |
| `*-visorpublico.geoambiental.co/content-layout` | `geoambiental` | [viewers](discovery-geoportals-viewers.md#geoambiental) |
| `apps.nazcacatastro.com/public/{code}/` cadastral viewer | `nazca` | [viewers](discovery-geoportals-viewers.md#nazca) |
| `*.xiltriongeoservicio.com/map`, shared Xiltrion bundle | `xiltrion` | [viewers](discovery-geoportals-viewers.md#xiltrion) |
| V&G `thirdparty/soda/soda.js` header and `/1/system/` LifeMap | `gtmap` | [viewers](discovery-geoportals-viewers.md#gtmap) |
| `/js/base/MapSave.js` plus `BaseMap.js` / `SeeMap.js` | `myeongji` | [viewers](discovery-geoportals-viewers.md#myeongji) |
| HTML comment `DIGITAL TWIN CLOUD - NEWLAYER` | `digitaltwincloud` | [viewers](discovery-geoportals-viewers.md#digitaltwincloud) |
| SHK municipal city guide plus confirmed SHK customer | `shkkbs` | [viewers](discovery-geoportals-viewers.md#shkkbs) |
| `storymaps.arcgis.com/stories/{item-id}` | `arcgisstorymaps` | [SDI](discovery-geoportals-sdi.md#arcgisstorymaps) |

## Generic geospatial probes

On a **named** mapping-agency or city GIS host:

```text
/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities
/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities
/cgi-bin/mapserv?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
/cgi-bin/qgis_mapserv.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
/.well-known/openeo
/collections
/gvsigonline/
/synserver
/vertigisstudio/web/
/gcx/WebViewer/
/Geocortex/Essentials/REST/sites?f=pjson
/Html5Viewer/
/cadenza/
/arcgis/rest/services?f=pjson
/rest/info?f=pjson
/igs/rest/mrcs/docs?f=json
/igs/rest/services?f=json
/cubewerx/cubeserv?SERVICE=WMS&REQUEST=GetCapabilities
/api/v1/catalog/1.0.0/
```

Google patterns: ``geoportal {agency}``, ``INSPIRE {country}``, ``IDE {country}`` (infraestructura de datos espaciales), ``GDI {land}``, ``géoportail {région}``.

Also try `/themes` (GeoMapFish), `/demo/` (MapProxy), `/net3/public/` (cardo), `/mapapps/` (map.apps), and tenant hosts `www2.wagmap.jp`, `www.sonicweb-asp.jp`, `webgis.alandis.jp`, `geogeo.jp`, `tottori-geomap.jp`, `geoportal2.pl`, `geocloud.jp`.

## Named geospatial indexes {#named-geospatial-indexes}

Prefer these bounded lists over unscoped “missing geoportals” searches. After v1.20.0, `Which {country} cities geoportals are missing?` is the wrong first move in Poland, Czechia, Slovakia, Italy, Japan, or Brazil — use the product tenant list instead.

| Source | Use |
|--------|-----|
| [GeoNetwork gallery](https://github.com/geonetwork/doc/blob/develop/source/annexes/gallery/gallery-urls.csv) | Leftovers after the first pass — few live hosts remain |
| [GeoNode](https://geonode.org/) gallery / showcase | Leftovers still yield live nodes (Sardinia, Neuquén, INTA, …) |
| [STAC Index](https://stacindex.org/catalogs) | Public STAC catalogs not already registered |
| [WMO WIS2 GDC](https://gdc.wis.cma.cn/) | Meteorological node catalogs (not MQTT topics). Software: `wis20box` / pygeoapi |
| [MappingSupport GIS servers](https://mappingsupport.com/p/surf_gis/list-federal-state-county-city-GIS-servers.txt) | US ArcGIS Server REST roots — only unmatched *live* roots |
| [FGDC Service Status Checker](https://statuschecker.fgdc.gov/) | US federal/state geospatial service hosts |
| [Geoseer](https://www.geoseer.net/) | Indexed OGC services that actually have layers |
| [ODIS catalogue](https://catalogue.odis.org/) | Ocean/coastal catalogs (often ERDDAP, GeoNetwork, CKAN) |
| Vendor viewer lists | Hajk, Aveki myCarta, Origo / Origosamverkan, Icebound AddSpatial, KortInfo, GISApp, GisMaster, SeaSketch `/app`, GDi Visios, PISO hub, EnviMAP tenants, Geoinfo VKOMAP, KAZGISA RGIS, T-MAPY GISPLAN / GIS4U / tmapserver, T-MAPY mOBEC, CORA GEO CG WebGIS, Geoportál GEPRO, TopGis GisOnline, MK Consult K5 MapServer, GEOVAP Marushka, Mapotip, ibb giscity, vianovis touvia.MAPS, EOMAP KOVGIS EVALD, Pozi `{council}.pozi.com`, GIS Cloud, MRF Web Map, Catalis MuniSight, K2 JMap, Digital Map Products CommunityView, Cohga Weave Map, INEGI OVIE, SOFTPRO MBK, INEGI MxSIG, WebEWID `*.webewid.pl`, Argenmap, Instant Apps Filter Gallery |

**One catalog per public product** still applies: do not add PISO municipal copies when `wwwgeoprostornet` is the hub; do not add `data.seasketch.org` ArcGIS REST next to a SeaSketch `/app`; do not add GISApp REST adaptors as a second city catalog; do not add both `maps.xymaps.com/{city}` and `www.xymaps.com/{city}`.

Custom-geoportal review (1 September 2026) extracted ArcGIS Experience Builder (`experiencebuilder`) from hosted `experience.arcgis.com` apps, Portal `/portal/apps/experiencebuilder/` tenants, Swedish Länsstyrelsen WebbGIS on `ext-webbgis.lansstyrelsen.se`, Mustasaari `kartta.mustasaari.fi`, plus CMS wrappers that embed Jimu (Klosterneuburg, AMVA, INSTAT); ArcGIS Web AppBuilder (`webappbuilder`) from `/apps/webappviewer/` apps; Esri Finland dmCity (`dmcity`) from `web.dmcity.fi/{city}/public/`; Infokartta InfoGIS (`infogis`) from `www.infogis.fi/{municipality}/`; WSP NetGIS Runtime (`netgisruntime`) from Danish `/NetGISRuntime/basis/index.jsp` viewers; Origosamverkan Origo (`origo`) from Swedish `origo.min.js` / `origo.js` municipal kartan viewers; T-MAPY GISPLAN (`gisplan`) from Slovak `{city}.gisplan.sk` plus Czech GIS4U / `{city}.tmapserver.cz` / T-WIST galleries; Geoportál GEPRO (`gepro`) from `{city}.obce.gepro.cz`; TopGis GisOnline (`gisonline`) from `app.gisonline.cz/{city}`; MK Consult K5 MapServer (`k5mapserver`) from `{muni}.k5mapserver.cz`; GEOVAP Marushka (`marushka`) from `zipped.js` / `js/marushka.js` clients; Mapotip (`mapotip`) from `portal.mapotip.cz/{municipality}`; ibb giscity (`giscity`) from `www.gisserver.de/{city}/`; vianovis touvia.MAPS (`touviamaps`) from `vianovis.net/{tenant}/` and city hosts loading `loadTouviaMaps()`; and CORA GEO CG WebGIS (`cgwebgis`) from `webgis.{city}.sk`; Geodeticca WEB GIS (`geodeticca`) from `gis.{city}.sk` titled Geodeticca WEB GIS; Georeal (`georeal`) from Czech kraj `/portal/Georeal.Cards` DTM and geoportal CMS; INGRADA online (`ingrada`) from Softplan `Softplan.Ingrada.Mobile` BürgerGIS; and VC Map (`vcmap`) from Virtual City Systems `html.vcs-ui` digital twins. Custom-geoportal review (2 September 2026) extracted Pozi (`pozi`) from `{council}.pozi.com` (title Pozi Web Map); ArcGIS Instant Apps (`instantapps`) from `/apps/instant/{template}/?appid=`; K2 Geospatial JMap (`jmap`) from `/JMapWeb/` and JMap NG `jmapserver-ng`; GIS Cloud (`giscloud`) from `{city}.giscloud.com`; MRF Web Map (`mrf`) from `{county}.mrf.com` and `js/lib/mrf/`; MuniSight (`munisight`) from Catalis `web.munisight.com/{Tenant}` Login.aspx; p.mapper (`pmapper`) from `{city}.geo-portale.it/pmapper-4.2.0/` and other p.mapper SIT; Digital Map Products CommunityView (`communityview`) from `VECommunityView/cities/{city}/`; MS-GIS (`msgis`) from `{city}.msgis.net` titled GeoInformation; Cohga Weave (`weave`) from HTML title `Weave Map` and webpack `app.*.js`; INEGI OVIE (`ovie`) from municipal OpenLayers `/js/libs/OpenLayers/OL.js` + Materialize economic viewers; SOFTPRO (`softpro`) from Ukrainian `{city}.cadastre.com.ua` and city MBK hosts that mention SOFTPRO; and INEGI MxSIG (`mxsig`) from `/mdm6/` and `/mxsig2/` amplify.js Mapa Digital viewers. `/portal/home/` ArcGIS Enterprise catalogs retag to `arcgishub`. Remaining custom geoportals are mostly one-off `.gov` map roots or mixed municipal viewers without a named shared product. Do not invent IDs for one-off national `.gov` map roots. Do **not** reuse `smartmap` for Geolonia — that ID is Kazakhstan `{district}.smartmap.kz`. Do **not** tag `www.visorguadalupe.com` as `visorurbano` (Proaxis Leaflet). Do **not** set `ctmgeo` from a generic “SIGWeb” title on a non-ctmgeo host. Do **not** set `experiencebuilder` on dmCity tenants (`dmcity`) or on Web AppBuilder `/apps/webappviewer/` (`webappbuilder`) or Instant Apps `/apps/instant/` (`instantapps`). Do **not** set `instantapps` on Experience Builder or Web AppBuilder. Do **not** set `netgisserver` on Danish `/NetGISRuntime/` viewers (`netgisruntime`). Do **not** set `origo` on Hajk (`appConfig.json`), myCarta, MapGuide Fusion, or GeoServer `/geoserver` catalogs on the same host. Do **not** set `gisplan` on Georeal `/portal/Georeal.*` kraj CMS (`georeal`), on T-MAPY MapProxy (`services7.tmapserver.cz`), on ArcGIS Hub, on CORA GEO CG WebGIS (`cgwebgis`), or on Geodeticca WEB GIS (`geodeticca`). Do **not** set `mapserver` on `{muni}.k5mapserver.cz` (`k5mapserver`) or on p.mapper UIs (`pmapper`). Do **not** set `jmap` from a hostname that merely contains `jmap` (Gyeongju `gjmap`, Rutgers NJMaps). Do **not** set `mrf` from MuniSight/Catalis `web.munisight.com` login portals (`munisight`). Do **not** set `geomediawebmap` from `web.munisight.com`. Do **not** set `gepro` from desktop MISYS. Do **not** set `geoserver` on `evald.ee/{slug}/` or `service.eomap.ee/{slug}/` tenants (`evald`). Do **not** add `service.eomap.ee` as a second copy of the same EVALD tenant. Do **not** set `giscity` from US/GR `gis.cityof*` ArcGIS hosts. Do **not** set `masterportal` on touvia.MAPS (`touviamaps`) or `touviamaps` on Masterportal (`masterportal.js`, `lgv-config`). Do **not** set `vcmap` from Masterportal or touvia.MAPS, or `ingrada` from a BürgerGIS hostname that is WebOffice or ArcGIS. Do **not** set `georeal` from `/portal/` shells without `Georeal.Cards`, or `geodeticca` from CG WebGIS or `michalovce.web-gis.sk`. Do **not** set `weave` from GeneWeaver or hosts that merely contain the word weave. Do **not** set `ovie` from Mission Viejo `geoviewer.io`, SNIGRD, or INEGI Mapa Digital de México `/mdm6/` (`mxsig`). Do **not** set `mxsig` on OVIE OpenLayers/Materialize viewers (`ovie`). Do **not** set `softpro` on the state Urban Planning Cadastre `kadastr.gov.ua` or StateGeoCadastre `map.land.gov.ua`. Do **not** add HydroNET (`my.floodreport.com.au`) until a third independent public tenant matches the iframe shell (North Central CMA Flood Eye is a different Angular/Leaflet stack).

Custom-geoportal review (7 September 2026) classified 39 records: 13 additional T-MAPY T-WIST galleries as `gisplan`, six exported self-hosted Jimu builds as `webappbuilder`, four Hub/Sites shells as `arcgishub`, four Ukrainian MBK clients as `softpro`, two WebClient-handler portals as `geomediawebmap`, and two records each for new `argenmap`, `avanmap`, `webewid`, `kcwebgis`, and `arcgisdashboards` definitions. Unattributed Korean municipal templates and two routes from one HydroGuam deployment remain `custom` because product provenance or independent-installation evidence is insufficient. Do **not** identify Argenmap from Leaflet alone, AvanMap from generic Avansis pages without `initAvanMap.js`, WebEWID from authenticated role portals, KC WebGIS from `/BMApp/` alone off the KC host family, or ArcGIS Dashboards from arbitrary dashboards outside `/apps/dashboards/`.

Second-pass review on 7 September 2026 classified 11 more records into ten new definitions: `cartovista`, `igo2`, `infomap`, `dpwebmap`, `3map`, `factawebgis`, `inkasportal`, `geoviewer`, `floodintelligenceportal` (two tenants), and `arcgisstorymaps`. First-party product pages, repositories, manuals, or vendor deployment lists establish that these are reusable products even where only one installation was already present in the registry. This second-pass evidence supersedes the earlier HydroNET caution: the two `my.floodreport.com.au` tenants are documented deployments of the shared SaaS Flood Intelligence Portal; North Central CMA Flood Eye remains `custom` because it is a different Angular/Leaflet application.

Third-pass review on 7 September 2026 resolved eight more records into four definitions: `pgis` for two TOPODATI municipal tenants with a public layer API and documented WMS/WFS service; `geoambiental` for two SIGMA Ingeniería environmental-authority viewers backed by a documented multi-client SaaS product; `nazca` for two Soltesoft municipal cadastral tenants with a shared client and tenant-specific configuration; and `xiltrion` for two Dataxil/CATASIG cadastral viewers with identical product bundles and first-party product/owner strings.

Fourth-pass review on 7 September 2026 resolved ten more records into two definitions that meet the three-installation rule. `gtmap` covers seven South Korean municipal viewers whose live `soda.js` header identifies V&G and whose shared application layout matches the vendor's GT Map LifeMap product. `shkkbs` covers the Gölbaşı, Pursaklar, and Üsküdar city guides: all three municipalities appear in SHK Bilişim's official customer references, the product page documents the same parcel/zoning and thematic-map functions, and the Pursaklar client displays the SHK mark directly. Other Korean and Turkish city guides remain `custom` unless one of these product-specific signals is present.

Custom-software review on 9 September 2026 retagged leftover `soda.js` LifeMaps onto `gtmap` (Gyeongju, Seongnam, Siheung, Gimpo, Gwangyang) and leftover `/js/base/MapSave.js` clients onto `myeongji` (Iksan, Gimje, Namwon, Jeongeup, Naju). It also applied pending IDs that already had software YAML but catalogs still on `custom` (`shkkbs`, `berryict`, `floodintelligenceportal`, `arcgisdashboards`, `arcgisstorymaps`) and added `digitaltwincloud` for EGIS DIGITAL TWIN CLOUD after the Ulsan smart map kept the `DIGITAL TWIN CLOUD - NEWLAYER` HTML comment. Indonesian `satudata.*` hostnames, Turkish `acikveri.*` / generic Kent Rehberi titles, Korean `/cyber/map/` 우리동네 생활지도 (two Chungnam counties), and `/map/main.do` 종합지도서비스 shells stay `custom`: they are naming conventions or unnamed CMS templates, not a single named product.

A second custom-software pass the same day remapped further leftover viewers onto existing IDs (`gtmap` Pohang / Wonju / Jeonju; `origo` Södertälje; `dpwebmap` Sollentuna `/bios/dpwebmap/`; `mycarta` Norrtälje; `instantapps` Lund Filter Gallery; `xiltrion` Yopal and Sabanalarga) and added `addspatial` for Icebound AddSpatial after Falkenberg’s public karta iframe kept title `AddSpatial` and `/smart/?profile=`. Taiwan `webMain.aspx` statistical query UIs (nstatdb, Exam Yuan, MOF, MOE, banking) stay `custom`: they share an ASPX query pattern, not a named product distinct from DGBAS Web (`dgbasweb`). Open SDG is not inferred from `sdg.` hostnames. NextGIS Drupal sites without `/resource/` or `/api/resource/` stay `custom`, not `nextgisweb`.

A third pass remapped Düren onto `inkasportal`, two `gms*.kc-systemhaus.de/BMApp/` tenants onto `kcwebgis`, Odenwaldkreis BürgerGIS onto `weboffice`, Nová Paka onto `marushka`, Armenia and Soacha onto `nazca`, CARDER and Corpoboyacá onto `geoambiental`, and Yongin onto `gtmap`. Do **not** set `webewid` from `gis.walbrzych.pl` (e-usługi hub titled WebEWID, not Portal Mapowy).

A fourth pass remapped Drobeta-Turnu Severin and Giurgiu onto `avanmap` (`initAvanMap.js`), Gulbene and Jēkabpils onto `pgis`, Ruapehu onto `infomap` (title `InfoMap Map Portal`, `X-Powered-By: Emtel NZ Ltd`), Mission Viejo onto `geoviewer`, Koper onto `3map` (`GISProjectListing_mini.js`), Prostějov onto `marushka`, Uherské Hradiště onto `gisplan` (T-WIST / `tmapy.svg`), Forêt ouverte onto `igo2` (title `IGO2`), and the Public Health Scotland metadata catalogue plus ScotPHO Profiles onto `shiny`. PolarWatch `catalog/list.php` stays `custom` because `polarwatch.noaa.gov/erddap/` is already registered. Bucheon and Busan LifeMaps stay `custom` until a live `soda.js` header can be confirmed. GeoPortal.VG remains `custom` (CMS hub, not a Masterportal viewer URL).

A fifth pass remapped Géo Val-de-Marne onto `onegeosuite` (`data-theme="onegeo"` on `/portal/`), the University of Guam collection portal onto `specify`, and the Hunter J. François Library onto `greenstone` (`xmlns:gs3`, `/greenstone3/oaiserver`). Do **not** set `lkod` from Slovak `{city}.twinmap.ai` DCAT `/api/opendata/set/catalog/lkod` (SKYMOVE TwinMap / od-portal shells, not Golemio LKOD). Do **not** set `pxstat` on NISRA Flexible Table Builder (`build.nisra.gov.uk`; distinct from `data.nisra.gov.uk`). Do **not** set `opensciencesi` on the national `openscience.si` aggregator. WormQTL `molgenis.do` URLs stay `custom` while they return 403.

A sixth pass remapped the ESIMO central portal (`esimo.ru`, live `esimo-user` / `esimo-central` / `portal-ajax` assets) and the AARI and FERHRI regional nodes (`portal.esimo.{org}.ru/portal`) onto `esimo`; ASTRON VO onto `dachs` (`gavo_dc.css`, `gavo.js`); and the Finnish Cancer Registry statistics app plus Statistics Estonia `tooturg.stat.ee` onto `shiny`. UMCG `/UMCG/ssr-catalogue/` stays `custom` while it returns 403. Do **not** set `lovd` on `www.lovd.nl` (network/software entry page). Do **not** set `dkan` on `opendata.by` (current site is not DKAN). Do **not** set `geonetwork` on Rocha `/geoportal/` (former `/metadata` path 404).

A seventh pass remapped Neckar-Odenwald-Kreis `/terratwin/` and Hohenlohekreis `/m/hokis/` onto `terratwin` (live title `TerraTwin`, `alkis-*.js` bundle) and the Mauritius Herbarium `/bol/MAU` onto `brahmsonline` (live title `BRAHMS: Mauritius Herbarium online`). ArVO stays `custom` while `arvo-registry.sci.am` times out. Do **not** set `molgenis` on `catalog.hda.belgium.be` (DataHub SPA with `urn:li:` URNs, not “Created with MOLGENIS”). Do **not** set `ingrid` on BAW `datenrepository.baw.de` (InGrid layout, but the record is a scientific repository and `ingrid` would force Geoportal). Do **not** set `mwmb` from a generic “Metadata Browser” title (GeoFind Namibia has no MetadataWorks mark). Do **not** set `massbank` on Shin-MassBank Human / MB-POST hosts. Do **not** set `visorurbano` on `www.visorguadalupe.com`.

An eighth pass remapped DataSud (`data-theme="onegeo"` on `/portal/`), PIGMA, and Data Grand Lyon onto `onegeosuite` (shared OneGeo Explorer shell with GéoJura, including hashed `scripts.67c7ffafa4109ce3890b.js`); DatARA onto `prodige` (operator tutorials on the catalog host name PRODIGE); Rennes Métropole onto `rudi` (title `Rudi`, documented first-party deployment); Tvrdošín and Nové Mesto nad Váhom onto `gisopendataportal` (`/developer` cites `gis-open-data-portal/od-portal`); and Universidad de La Rioja onto `dialnetcris` (Fundación Dialnet attribution; the discovery heading already names this portal). UNT Digital Library `/explore/collections/UNTDRD/` stays `custom` while the host times out. Do **not** set `lkod` on the TwinMap shells; `gisopendataportal` is the matching id.

A ninth pass remapped Lund Humanities Lab Archive onto `flat` (`flat_bootstrap_theme`, `/flat/oai2?verb=Identify`); Royal Greenwich, Oxfordshire, Kingston, and Ealing onto `esridataobservatory` (`/wp-content/themes/ia-theme/` with `ia-map.js` / `ia-quickprofile.js` / `ia-stat.js` and Esri UK credit); and Oxford Brookes RADAR onto `openequella` (`com.equella.core`). Do **not** set `islandora` on the Lund FLAT install. Do **not** set `simaiopendata` on `opendata.demo.simai.ru` (inactive vendor placeholder). UNT Digital Library stays `custom` while `digital.library.unt.edu` times out.

A tenth pass remapped GAVO Data Center (`dc.g-vo.org` and `dc.zah.uni-heidelberg.de`, live `Server: DaCHS/2.12.2` plus `gavo_dc` / `gavo.js`) onto `dachs`; SNSB `/dwb_biocase.html` onto `diversityworkbench` (title `DWB BioCASe Data Publication Services`); Gaia@AIP, CARS, MUSE-Wide, RAVE, APPLAUSE, CosmoSim, and CLUES onto `daiquiri` (`Proudly powered by Daiquiri`); Biodiversity Exploratories onto `bexis2` (root redirects to `/home/Start`); and eNanoMapper onto `ambit` (`meta name="description" content="AMBIT"`). Matching software on the two GAVO host records does not prove two deployments. Do **not** set `lovd` on DEB Register or CHD7 while they return 403. GeoNature-atlas Guyane and the named PnX-SI atlas list use `geonature`. Belgian HDA DataHub uses `datahubproject`.

An eleventh pass remapped INFOMED `tesis.sld.cu` and Artemisa `repotesis.art.sld.cu` onto `cwis` (live CWIS JavaScript and a `scout.wisc.edu/cwis` credit) and IRI/LDEO Climate Data Library onto `datalibrary` (title `Climate Data Library`, maproom ontologies). The IRI record was moved to Geoportal because `datalibrary` is not allowed as an Open data portal. Do **not** set `geomapfish` on Liechtenstein `service.geo.llv.li` (CMS hub; the GeoMapFish viewer is `map.geo.llv.li`). Do **not** set `mfgeoadmin3` on `map.geo.admin.ch` — use `webmapviewer`. Do **not** set `opengov` on `opengov.brandon.ca`. Do **not** set `edatos` on institute CMS homes (`ibestat.es`, `madrid.org/iestadis`). Do **not** set `landfolio` on Mali SICAM (JHipster, not Trimble). Do **not** set `resourcecontracts` on the current PH-EITI contracts app.

A twelfth pass remapped Nitra `gis.nitra.sk` onto `experiencebuilder` (full-page iframe to `experience.arcgis.com/experience/{id}`; the hosted app keeps title `Experience`, `jimu-core`, and `exb.ico`) and leftover Czech city-domain T-MAPY galleries onto `gis4u` (`/mapa/` application routes plus `/theme/square/` assets and a tmapy.cz credit: Třebíč, Uherský Brod, Valašské Meziříčí, Žďár nad Sázavou, Velké Meziříčí, Nové Město na Moravě, Nový Bydžov, Hranice, Domažlice, Jindřichův Hradec, Jihlava, Bohumín, Kopřivnice, Bruntál). Choceň onto `marushka` (gallery launches `/marushka/default.aspx`). Do **not** set `gisplan` on those city-domain GIS4U square-theme portals (`gis4u`). Do **not** set `nextgisweb` on `ooptaari.nextgis.ru` (Drupal; `/resource/0` and `/api/resource/` 404). Do **not** set `ckan` from mixed Spanish CMS endpoint types when `status_show` is empty. Do **not** set `webewid` or `webappbuilder` on `gisbialystok.pl` (CMS hub). Do **not** set `experiencebuilder` on Murcia `geoportal.murcia.es` (Drupal hub; SITAM ExB apps are separate URLs).

A thirteenth pass remapped Havířov and Pardubice GEOVAP MyCity galleries onto `marushka` (`/MarushkaPublic/default.aspx`; `/MarushkaGP4/` title `Marushka - Mapový aplikační server` and `zipped.js`), Mendel University `repozitar.mendelu.cz` onto `dspace` (`/server/api` reports DSpace 9.1), and Oradea `harta.oradea.ro/hartagisoradea/` onto `geomediawebmap` (`Intergraph.WebSolutions`, `WebClient.ashx`, `$GP`). Do **not** set `eprints` on the ASEP dataset-info CMS (`preprints` menu). Do **not** set `georeal` on Kadaň `/portal/Themes/GeorealKadan/` without `Georeal.Cards`. Do **not** set `qwc2` on Prague’s Nuxt geoportal hub. Do **not** set `arcgishub` or `webappbuilder` on Trenčín `gis.tsk.sk` (ArcGIS Web ADF `mapviewer.jsf`). Romanian `xportal*` urbanism shells stay `custom` until a named product page is confirmed.

A fourteenth pass remapped leftover scientific catalogs onto existing IDs: University of Ostrava EDUO, Universitas Medan Area, and UNESP `dspace`; Molecular Biophysics Database `inveniordm`; Aleia, Deposita Dados, and Repo4Cat `dataverse`. Do **not** set `inveniordm` on EOSC CZ `nma.eosc.cz` while it remains a Metadata catalog (`inveniordm` only allows Scientific data repository / General research repository). Do **not** invent an `easydb` id for HilData.

A fifteenth pass remapped leftover scientific catalogs onto existing IDs: SADAR Halle `dspace`; HCU Hamburg repOS `dspacecris`; PTB OAR and Nülan UNMDP `eprints`; TUL `rdb.p.lodz.pl` `dataverse`; University of Wrocław `dlibra`; eLTER DAR `invenio`. Do **not** set `yoda` on `data.ru.nl` without a public Yoda landing. Do **not** set `dlibra` on Lublin UP (`/dlibra` 404). Do **not** set `inveniordm` from `generator` Invenio alone when there is no InvenioRDM / `invenio-rdm` branding (use `invenio`).

A sixteenth pass remapped leftover catalogs onto existing IDs: InDoRES `dataverse`; Offenbach `mapbender` (`/mapbender/application/geoportal_offenbach`); Schaumburg `qwc2` (`assets/css/qwc2.css`); Kronach 360° `touviamaps`; Landkreis Osnabrück WebInfo `weboffice` (`synserver`). Do **not** set `mapbender` on Merzig-Wadern or Trier-Saarburg BürgerGIS hubs that only link Saarland/RLP Mapbender. Do **not** set `weboffice` on the Radolfzell CMS Bürgerportal (the VertiGIS client is already `wo-hosting.vertigis.com`). Do **not** set `geonetwork` on Szczecin’s SIP CMS hub. Do **not** set `nada` on Quetelet-Progedo from a country-list false positive.

A seventeenth pass remapped leftover catalogs onto existing IDs: SDIS 04 OpenSIS `lizmap` (`lizmapPopup`, `/index.php/view/`); Géo Pays de Brest `arcgishub` (`/portal/apps/sites/` with `hub-site` / `opendata-ui`). Do **not** set `arcgishub` from `/portal/home/` alone (ArcGIS Enterprise Portal). Do **not** set `g3wsuite` from GisClient `?mapset=` (`widgetGisClient.js`). Do **not** invent `opensis`, `sitmun`, or `gisclient` from a single leftover install.

A eighteenth pass remapped leftover catalogs onto existing IDs: BAW HENRY and AERADE Cranfield `dspace`; RWTH Publications `invenio` (JOIN2); GALENOS `inveniordm`; Warwick WRAP `eprints`; Eisenbahn-Bundesamt GeoPortal `ingrid` (`/user/themes/ingrid/`, `ingrid.js`). Do **not** set `ingrid` on BAW `datenrepository.baw.de` (scientific; `ingrid` would force Geoportal). Do **not** set `dataverse` on the EUR library CMS page. Do **not** set `tergis` on German TerraWeb (`terragis.de` / `terraweb.js`).

A nineteenth pass remapped leftover catalogs onto existing IDs: Rice Research Repository `dspace` (`/server/api` DSpace 9.3); AuScope Data Repository `ckan` (`status_show`); Lancaster datasets portal `pure`; RIT `elsevierdigitalcommons`. Do **not** set `figshare` on ReDATA (`redata.arizona.edu` is a library GitHub Pages hub; the Figshare catalog is already `arizona.figshare.com`). Do **not** set `dlibra` from a Cloudflare “Verifying…” page. Do **not** set `hyrax` on `hydra.hull.ac.uk` (redirects to the library CMS).

A twentieth pass remapped leftover catalogs onto existing IDs: SJSU ScholarWorks `elsevierdigitalcommons`; UNAM IIEc `eprints` (`generator` EPrints 3.3.16); UNCo RDI `dspace` (`/server/api` DSpace 8.4). Do **not** set `contentdm` on Claremont CCDL (campus photo/manuscript library). Do **not** set `argenmap` on IGN `mapamuni.ign.gob.ar` without Argenmap source-tree signals. Do **not** set `eprints` from Digital Commons OAI Identify that only mentions an `eprints` metadata prefix.

A twenty-first pass remapped leftover catalogs onto existing IDs: Città Metropolitana di Torino `geonetwork` (root redirects to `catalog.search`, live CSW); RSDI Basilicata `geonetwork` (`/geonetwork/srv/eng/catalog.search`, live CSW); uBibliorum `dspace` (`/server/api` DSpace 7.6.1). Do **not** set `geonetwork` on Liguria, Sicily, Lombardy, Veneto, or Bergamo geoportal homes when `/geonetwork/srv` 404s. Do **not** set `dspace` on UGM ETD (`/server/api` 404).

A twenty-second pass remapped leftover catalogs onto existing IDs: GéoArdèche and Atmo Nouvelle-Aquitaine `geonetwork` (`/geonetwork/srv/eng/catalog.search`, live CSW); Observatorio Medioambiental La Plata `ckan` (`status_show` 2.7.3). Do **not** set `lizmap` from `/index.php/view/` when it serves the same CMS homepage (SIG Cévennes). Do **not** set `geonetwork` on Géo Vendée or InfoGéo 47 (`/geonetwork/srv` 404). Do **not** set `dataverse` on UBA Sociales (Omeka Classic). Do **not** invent `dlcm` or `cspace` from Yareta or UM Scholars.

A twenty-third pass remapped leftover catalogs onto existing IDs: Bloemendaal `arcgishub` (`hubcdn` / `opendata-ui`, `/api/search/v1`); Lille Métropole `geonetwork` (`gn_search_georchestra` `catalog.search`, live CSW). Do **not** set `mapapps` on Ulm Daten (`datenportal.ulm.de` is an Open data portal; `mapapps` would force Geoportal — the geoportal app is already `portalulmde`). Do **not** invent `geocms` from two brain-SCC leftovers (Nordhessen, Vogelsberg). Do **not** invent `gajamatrix` or `georchestra` (Lille’s catalog is GeoNetwork; Gera’s viewer is not the already-tagged vendor CSW).

A twenty-fourth pass remapped leftover catalogs onto existing IDs: Knowledge@UChicago `inveniordm`; UCL Discovery, NORA, LSE Research Online, and LSHTM Research Online `eprints`; Surrey Research Insight `esploro`. Do **not** set `geonetwork` on EPA Maps GIS (`gis.epa.ie` is the maps landing; live GeoNetwork is `/geonetwork` and is a different product) or on the IDEE geoportal hub (CODSI is already `wwwideeescswcodsiidee`). Do **not** set `atmmaggioli` on Italian Municipium open-data shells. Do **not** invent `goobi` from two Goobi viewer heritage libraries.

A twenty-fifth pass remapped leftover catalogs onto existing IDs: UAL Research Online `eprints`; GlobeData `dataverse`; BBAW edoc `opus`; WU Vienna Research `pure`. Do **not** invent `easydb` from heidICON. Do **not** set `radar` on Atlanta University Center RADAR when the homepage and `/radar/` paths 403. Do **not** set `geonetwork` on Georgia NSDI or Montenegro Geoportal (`/geonetwork/srv` 404).

A twenty-sixth pass found no further remaps onto existing IDs. Do **not** set `ckan` from an `og:url` pointing at `ckan-archive-test` when `status_show` 404s (NIRD `archive.sigma2.no`). Do **not** set `geonetwork` on leftover Spanish IDE hubs when `/geonetwork/srv` 404s (IDEEX, Gran Canaria, IDERIOJA, Cartagena, Pontevedra). Do **not** invent a WAF software id from two `cmd=wafdownload` leftovers (Aurich, Worms). Do **not** set `figshare` on the SciLifeLab Hugo hub. FRDR, PutraRepo (timeout), and leftover UK `data.*` portals behind Incapsula or custom SPAs stay `custom`.


## OneGeo Suite (`onegeosuite`) {#onegeosuite}

[Neogeo's modular platform](https://www.onegeosuite.fr/) combines Core, Explorer,
Maps and Portal. [Vendor references](https://neogeo.fr/references-projets/) explicitly
name PIGMA and Data Grand Lyon. [DataSud documentation](https://www.datasud.fr/portal/documentation/)
links the same product, and its login shell names `onegeo-suite-site-login-vuejs`.
The [white-label guide](https://www.datasud.fr/portal/services/marque-blanche/) describes
OneGeo catalog integration. Use these product-specific credits together with the linked
Explorer catalog; generic Angular or Gatsby bundles are insufficient. Search
`"OneGeo Suite" "catalogue"` and the vendor's references. Keep separately registered
GeoNetwork/GeoServer components classified as their own software.


| Tool | Query |
|------|-------|
| Google | `"OneGeo Suite" (catalogue OR catalog)` |
| Censys | `web.endpoints.http.body: "onegeo-suite-site-login-vuejs"` |
| FOFA | `body="onegeo-suite-site-login-vuejs"` |


## PRODIGE (`prodige`) {#prodige}

A reusable geographic data-sharing infrastructure, with
[project metadata](https://adullact.net/projects/prodige/) and
[source projects](https://gitlab.adullact.net/prodige).
[DatARA's tutorials](https://www.open-datara.fr/accueil/ressources/tutoriels-et-videos-de-prise-en-main)
explicitly document PRODIGE V5. Its catalog host exposes `/api/doc/` with the title
`API PRODIGE Ressources`, a stronger fingerprint than GeoNetwork or generic PHP assets.
Search `"PRODIGE" "plateforme" "données"` and confirm a deployment through its own
operator documentation. The complete portal and its GeoNetwork component can have
separate registry records and software assignments.


| Tool | Query |
|------|-------|
| Google | `"PRODIGE" plateforme données OR "API PRODIGE"` |
| Censys | `web.endpoints.http.body: "API PRODIGE"` |
| FOFA | `body="API PRODIGE"` |

## Related

- [discovery-geoportals-sdi.md](discovery-geoportals-sdi.md)
- [discovery-geoportals-viewers.md](discovery-geoportals-viewers.md)
- [discovery.md](discovery.md)
- [discovery.md](discovery.md#hunt-patterns) — session hunt patterns
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-opendata.md](discovery-opendata.md)
- [harvest-geoportals.md](harvest-geoportals.md)
- [harvest-viewers.md](harvest-viewers.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [software-taxonomy.md](software-taxonomy.md)

