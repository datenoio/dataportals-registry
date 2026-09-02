# Discovering geoportals

How to find **geoportal** installations (`catalog_type: Geoportal`). Search-engine syntax: [discovery-search-tools.md](discovery-search-tools.md). If a site is both a map viewer and a dataset portal, pick the **primary** product ([catalog-types.md](catalog-types.md)). One public catalog UI = one registry record — see [one catalog per host](discovery.md#one-catalog-per-public-product).

Fingerprints live on two pages so this overview stays short:

| Page | Use when |
|------|----------|
| [SDI platforms](discovery-geoportals-sdi.md) | GeoNetwork, GeoNode, Palapa, GeoServer, ArcGIS, Experience Builder, Web AppBuilder, STAC, openEO, Sentinel Hub, Lizmap, QGIS Server, G3W-SUITE, CubeWerx, M.App Enterprise, mviewer, Isogeo, Geocortex, MapServer, and other catalog/service stacks |
| [Regional viewers](discovery-geoportals-viewers.md) | Wagmap, SonicWeb, GeDA-Public, ALANDIS+, Geolonia スマートマップ, EWMAPA, e-mapa.net, Loftmyndir, Alta Vefsjá, Tianditu, Masterportal, GeoMapFish, NetGIS Server, NetGIS Runtime, cardo, MapGIS IGServer, HyG Mapgis, Trimble Locus / Louhi / Landfolio, dmCity, InfoGIS, Spatial Suite, Hajk, myCarta, KortInfo, IntraMaps Public, Spectrum Spatial Analyst, Exponare, LocalMaps, GEUSMAP, GISApp, GeneGIS PAGIS, GisMaster, SmartMap, VKOMAP, ISY Map, Avinet Adaptive, MAP+, EnviMAP, PISO, GDi Visios, MapGuide, SeaSketch, iObčina, iShare, Cadcorp, Visor Urbano, Dobles Visor de Mapas, and municipal GIS viewers |

All `software.id` values: [software-index.md](software-index.md). Harvest grain (layers vs tiles): [harvest-geoportals.md](harvest-geoportals.md), [harvest-viewers.md](harvest-viewers.md).

## Core SDI (short list)

Confirm with a GET on the candidate host only. Stop on `401`/`403`.

| If you see | `software.id` | Full fingerprints |
|------------|---------------|-------------------|
| `/srv/eng/csw` or `/srv/api` | `geonetwork` | [SDI](discovery-geoportals-sdi.md#geonetwork) |
| `/api/layers/` or `/api/datasets/` | `geonode` | [SDI](discovery-geoportals-sdi.md#geonode) |
| Title “Geoportal Palapa” / `/main/` or `/gspalapa/` | `palapa` | [SDI](discovery-geoportals-sdi.md#palapa) |
| `/geoserver/ows` GetCapabilities | `geoserver` | [SDI](discovery-geoportals-sdi.md#geoserver) |
| Hub search / `opendata.arcgis.com` | `arcgishub` | [SDI](discovery-geoportals-sdi.md#arcgishub) |
| `/arcgis/rest/info?f=pjson` | `arcgisserver` | [SDI](discovery-geoportals-sdi.md#arcgisserver) |
| `experience.arcgis.com/experience/` or `jimu-core/init.js` | `experiencebuilder` | [SDI](discovery-geoportals-sdi.md#experiencebuilder) |
| `/apps/webappviewer/index.html?id=` | `webappbuilder` | [SDI](discovery-geoportals-sdi.md#webappbuilder) |
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
| `drift.kortinfo.net/Map.aspx` | `kortinfo` | [viewers](discovery-geoportals-viewers.md#kortinfo) |
| IntraMaps Public `project=` / `*.spatial.t1cloud.com` | `intramaps` | [viewers](discovery-geoportals-viewers.md#intramaps) |
| `/connect/analyst/` Spectrum Spatial Analyst | `spectrumspatial` | [viewers](discovery-geoportals-viewers.md#spectrumspatial) |
| `/exponare/` RestPublicApplication | `exponare` | [viewers](discovery-geoportals-viewers.md#exponare) |
| LocalMaps `/localmaps/gallery` | `localmaps` | [viewers](discovery-geoportals-viewers.md#localmaps) |
| `/geusmap/?mapname=` | `geusmap` | [viewers](discovery-geoportals-viewers.md#geusmap) |
| `*.gisapp.ro` or PortalPublic `logo_fida.png` | `gisapp` | [viewers](discovery-geoportals-viewers.md#gisapp) |
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

Prefer these bounded lists over unscoped “missing geoportals” searches:

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
| Vendor viewer lists | Hajk, Aveki myCarta, Origo / Origosamverkan, KortInfo, GISApp, GisMaster, SeaSketch `/app`, GDi Visios, PISO hub, EnviMAP tenants, Geoinfo VKOMAP, KAZGISA RGIS, T-MAPY GISPLAN / GIS4U / tmapserver, T-MAPY mOBEC, CORA GEO CG WebGIS, Geoportál GEPRO, TopGis GisOnline, MK Consult K5 MapServer, GEOVAP Marushka, Mapotip, ibb giscity, vianovis touvia.MAPS, EOMAP KOVGIS EVALD, Pozi `{council}.pozi.com`, GIS Cloud, MRF Web Map, Catalis MuniSight, K2 JMap, Digital Map Products CommunityView, Cohga Weave Map, INEGI OVIE, SOFTPRO MBK, INEGI MxSIG |

**One catalog per public product** still applies: do not add PISO municipal copies when `wwwgeoprostornet` is the hub; do not add `data.seasketch.org` ArcGIS REST next to a SeaSketch `/app`; do not add GISApp REST adaptors as a second city catalog; do not add both `maps.xymaps.com/{city}` and `www.xymaps.com/{city}`.

Custom-geoportal review (1 September 2026) extracted ArcGIS Experience Builder (`experiencebuilder`) from hosted `experience.arcgis.com` apps, Portal `/portal/apps/experiencebuilder/` tenants, Swedish Länsstyrelsen WebbGIS on `ext-webbgis.lansstyrelsen.se`, Mustasaari `kartta.mustasaari.fi`, plus CMS wrappers that embed Jimu (Klosterneuburg, AMVA, INSTAT); ArcGIS Web AppBuilder (`webappbuilder`) from `/apps/webappviewer/` apps; Esri Finland dmCity (`dmcity`) from `web.dmcity.fi/{city}/public/`; Infokartta InfoGIS (`infogis`) from `www.infogis.fi/{municipality}/`; WSP NetGIS Runtime (`netgisruntime`) from Danish `/NetGISRuntime/basis/index.jsp` viewers; Origosamverkan Origo (`origo`) from Swedish `origo.min.js` / `origo.js` municipal kartan viewers; T-MAPY GISPLAN (`gisplan`) from Slovak `{city}.gisplan.sk` plus Czech GIS4U / `{city}.tmapserver.cz` / T-WIST galleries; Geoportál GEPRO (`gepro`) from `{city}.obce.gepro.cz`; TopGis GisOnline (`gisonline`) from `app.gisonline.cz/{city}`; MK Consult K5 MapServer (`k5mapserver`) from `{muni}.k5mapserver.cz`; GEOVAP Marushka (`marushka`) from `zipped.js` / `js/marushka.js` clients; Mapotip (`mapotip`) from `portal.mapotip.cz/{municipality}`; ibb giscity (`giscity`) from `www.gisserver.de/{city}/`; vianovis touvia.MAPS (`touviamaps`) from `vianovis.net/{tenant}/` and city hosts loading `loadTouviaMaps()`; and CORA GEO CG WebGIS (`cgwebgis`) from `webgis.{city}.sk`; Geodeticca WEB GIS (`geodeticca`) from `gis.{city}.sk` titled Geodeticca WEB GIS; Georeal (`georeal`) from Czech kraj `/portal/Georeal.Cards` DTM and geoportal CMS; INGRADA online (`ingrada`) from Softplan `Softplan.Ingrada.Mobile` BürgerGIS; and VC Map (`vcmap`) from Virtual City Systems `html.vcs-ui` digital twins. Custom-geoportal review (2 September 2026) extracted Pozi (`pozi`) from `{council}.pozi.com` (title Pozi Web Map); ArcGIS Instant Apps (`instantapps`) from `/apps/instant/{template}/?appid=`; K2 Geospatial JMap (`jmap`) from `/JMapWeb/` and JMap NG `jmapserver-ng`; GIS Cloud (`giscloud`) from `{city}.giscloud.com`; MRF Web Map (`mrf`) from `{county}.mrf.com` and `js/lib/mrf/`; MuniSight (`munisight`) from Catalis `web.munisight.com/{Tenant}` Login.aspx; p.mapper (`pmapper`) from `{city}.geo-portale.it/pmapper-4.2.0/` and other p.mapper SIT; Digital Map Products CommunityView (`communityview`) from `VECommunityView/cities/{city}/`; MS-GIS (`msgis`) from `{city}.msgis.net` titled GeoInformation; Cohga Weave (`weave`) from HTML title `Weave Map` and webpack `app.*.js`; INEGI OVIE (`ovie`) from municipal OpenLayers `/js/libs/OpenLayers/OL.js` + Materialize economic viewers; SOFTPRO (`softpro`) from Ukrainian `{city}.cadastre.com.ua` and city MBK hosts that mention SOFTPRO; and INEGI MxSIG (`mxsig`) from `/mdm6/` and `/mxsig2/` amplify.js Mapa Digital viewers. `/portal/home/` ArcGIS Enterprise catalogs retag to `arcgishub`. Remaining custom geoportals are mostly one-off `.gov` map roots or mixed municipal viewers without a named shared product. Do not invent IDs for one-off national `.gov` map roots. Do **not** reuse `smartmap` for Geolonia — that ID is Kazakhstan `{district}.smartmap.kz`. Do **not** tag `www.visorguadalupe.com` as `visorurbano` (Proaxis Leaflet). Do **not** set `ctmgeo` from a generic “SIGWeb” title on a non-ctmgeo host. Do **not** set `experiencebuilder` on dmCity tenants (`dmcity`) or on Web AppBuilder `/apps/webappviewer/` (`webappbuilder`) or Instant Apps `/apps/instant/` (`instantapps`). Do **not** set `instantapps` on Experience Builder or Web AppBuilder. Do **not** set `netgisserver` on Danish `/NetGISRuntime/` viewers (`netgisruntime`). Do **not** set `origo` on Hajk (`appConfig.json`), myCarta, MapGuide Fusion, or GeoServer `/geoserver` catalogs on the same host. Do **not** set `gisplan` on Georeal `/portal/Georeal.*` kraj CMS (`georeal`), on T-MAPY MapProxy (`services7.tmapserver.cz`), on ArcGIS Hub, on CORA GEO CG WebGIS (`cgwebgis`), or on Geodeticca WEB GIS (`geodeticca`). Do **not** set `mapserver` on `{muni}.k5mapserver.cz` (`k5mapserver`) or on p.mapper UIs (`pmapper`). Do **not** set `jmap` from a hostname that merely contains `jmap` (Gyeongju `gjmap`, Rutgers NJMaps). Do **not** set `mrf` from MuniSight/Catalis `web.munisight.com` login portals (`munisight`). Do **not** set `geomediawebmap` from `web.munisight.com`. Do **not** set `gepro` from desktop MISYS. Do **not** set `geoserver` on `evald.ee/{slug}/` or `service.eomap.ee/{slug}/` tenants (`evald`). Do **not** add `service.eomap.ee` as a second copy of the same EVALD tenant. Do **not** set `giscity` from US/GR `gis.cityof*` ArcGIS hosts. Do **not** set `masterportal` on touvia.MAPS (`touviamaps`) or `touviamaps` on Masterportal (`masterportal.js`, `lgv-config`). Do **not** set `vcmap` from Masterportal or touvia.MAPS, or `ingrada` from a BürgerGIS hostname that is WebOffice or ArcGIS. Do **not** set `georeal` from `/portal/` shells without `Georeal.Cards`, or `geodeticca` from CG WebGIS or `michalovce.web-gis.sk`. Do **not** set `weave` from GeneWeaver or hosts that merely contain the word weave. Do **not** set `ovie` from Mission Viejo `geoviewer.io`, SNIGRD, or INEGI Mapa Digital de México `/mdm6/` (`mxsig`). Do **not** set `mxsig` on OVIE OpenLayers/Materialize viewers (`ovie`). Do **not** set `softpro` on the state Urban Planning Cadastre `kadastr.gov.ua` or StateGeoCadastre `map.land.gov.ua`. Do **not** add HydroNET (`my.floodreport.com.au`) until a third independent public tenant matches the iframe shell (North Central CMA Flood Eye is a different Angular/Leaflet stack).

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
