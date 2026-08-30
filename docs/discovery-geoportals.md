# Discovering geoportals

How to find **geoportal** installations (`catalog_type: Geoportal`). Search-engine syntax: [discovery-search-tools.md](discovery-search-tools.md). If a site is both a map viewer and a dataset portal, pick the **primary** product ([catalog-types.md](catalog-types.md)). One public catalog UI = one registry record — see [one catalog per host](discovery.md#one-catalog-per-public-product).

Fingerprints live on two pages so this overview stays short:

| Page | Use when |
|------|----------|
| [SDI platforms](discovery-geoportals-sdi.md) | GeoNetwork, GeoNode, GeoServer, ArcGIS, STAC, openEO, Sentinel Hub, Lizmap, QGIS Server, G3W-SUITE, CubeWerx, M.App Enterprise, mviewer, Isogeo, Geocortex, MapServer, and other catalog/service stacks |
| [Regional viewers](discovery-geoportals-viewers.md) | Wagmap, EWMAPA, e-mapa.net, Loftmyndir, Alta Vefsjá, Tianditu, Masterportal, GeoMapFish, NetGIS, cardo, MapGIS IGServer, Trimble Locus / Louhi / Landfolio, Spatial Suite, Hajk, KortInfo, GEUSMAP, GISApp, SmartMap, ISY Map, Avinet Adaptive, MAP+, EnviMAP, PISO, GDi Visios, MapGuide, SeaSketch, iObčina, iShare, Cadcorp, and municipal GIS viewers |

All `software.id` values: [software-index.md](software-index.md). Harvest grain (layers vs tiles): [harvest-geoportals.md](harvest-geoportals.md), [harvest-viewers.md](harvest-viewers.md).

## Core SDI (short list)

Confirm with a GET on the candidate host only. Stop on `401`/`403`.

| If you see | `software.id` | Full fingerprints |
|------------|---------------|-------------------|
| `/srv/eng/csw` or `/srv/api` | `geonetwork` | [SDI](discovery-geoportals-sdi.md#geonetwork) |
| `/api/layers/` or `/api/datasets/` | `geonode` | [SDI](discovery-geoportals-sdi.md#geonode) |
| `/geoserver/ows` GetCapabilities | `geoserver` | [SDI](discovery-geoportals-sdi.md#geoserver) |
| Hub search / `opendata.arcgis.com` | `arcgishub` | [SDI](discovery-geoportals-sdi.md#arcgishub) |
| `/arcgis/rest/info?f=pjson` | `arcgisserver` | [SDI](discovery-geoportals-sdi.md#arcgisserver) |
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
| `drift.kortinfo.net/Map.aspx` | `kortinfo` | [viewers](discovery-geoportals-viewers.md#kortinfo) |
| `/geusmap/?mapname=` | `geusmap` | [viewers](discovery-geoportals-viewers.md#geusmap) |
| `*.gisapp.ro` or PortalPublic `logo_fida.png` | `gisapp` | [viewers](discovery-geoportals-viewers.md#gisapp) |
| `{district}.smartmap.kz` | `smartmap` | [viewers](discovery-geoportals-viewers.md#smartmap) |
| ISY Map `/geoinnsyn/` or `/webkart/` | `isymap` | [viewers](discovery-geoportals-viewers.md#isymap) |
| Avinet Adaptive ExtJS atlas | `avinet` | [viewers](discovery-geoportals-viewers.md#avinet) |
| TYDAC MAP+ `/mapplus-lib/` | `mapplus` | [viewers](discovery-geoportals-viewers.md#mapplus) |
| EnviMAP / GeoForte | `envimap` | [viewers](discovery-geoportals-viewers.md#envimap) |
| PISO geoprostor.net | `piso` | [viewers](discovery-geoportals-viewers.md#piso) |
| GDi Visios `/visios/` | `gdivisios` | [viewers](discovery-geoportals-viewers.md#gdivisios) |
| MapGuide `/mapguide/` | `mapguide` | [viewers](discovery-geoportals-viewers.md#mapguide) |
| SeaSketch `/{project}/app` | `seasketch` | [viewers](discovery-geoportals-viewers.md#seasketch) |
| Kaliopa iObčina / iOpćina | `iobcina` | [viewers](discovery-geoportals-viewers.md#iobcina) |
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
| `/igs/rest/mrcs/docs` | `mapgisigserver` | [viewers](discovery-geoportals-viewers.md#mapgisigserver) |
| `www2.wagmap.jp` | `wagmap` | [viewers](discovery-geoportals-viewers.md#wagmap) |
| `{powiat}.e-mapa.net` | `emapa` | [viewers](discovery-geoportals-viewers.md#emapa) |
| `www.map.is/{muni}/` | `loftmyndir` | [viewers](discovery-geoportals-viewers.md#loftmyndir) |
| `geo.alta.is/{tenant}/` viewer | `alta` | [viewers](discovery-geoportals-viewers.md#alta) |

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

Also try `/themes` (GeoMapFish), `/demo/` (MapProxy), `/net3/public/` (cardo), `/mapapps/` (map.apps), and tenant hosts `www2.wagmap.jp`, `geoportal2.pl`, `geocloud.jp`.

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
| Vendor viewer lists | Hajk, KortInfo, GISApp, SeaSketch `/app`, GDi Visios, PISO hub, EnviMAP tenants |

**One catalog per public product** still applies: do not add PISO municipal copies when `wwwgeoprostornet` is the hub; do not add `data.seasketch.org` ArcGIS REST next to a SeaSketch `/app`; do not add GISApp REST adaptors as a second city catalog.

Custom-geoportal review (30 August 2026) left ~587 `custom` geoportals with **no remaining shared hostname/path pattern** large enough for a new `software.id`. Do not invent IDs for one-off national `.gov` map roots.

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
