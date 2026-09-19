# Custom geoportal software review — 7 September 2026

## Scope and method

The source registry contained 1,028 `Geoportal` records with `software.id: custom`
at the start of this review. The review combined:

1. URL, hostname, title, redirect, and HTML/static-asset fingerprints from a bounded
   GET-only probe of those records (830 returned HTTP 200; 162 failed to connect or
   timed out; the remainder returned other HTTP statuses).
2. Exact and near-exact grouping of application paths and script/style assets.
3. Confirmation against first-party vendor, project, or government documentation.
4. The software-taxonomy rule that a new ID must represent a named shared product,
   not a one-off portal or an unidentified common framework.

## Applied classifications

| Fingerprint cluster | Records | Decision | Evidence used for confirmation |
|---------------------|--------:|----------|--------------------------------|
| T-MAPY T-WIST public application galleries (`lock.min.js`, `translator`, `filterApps.js`, `check-login.js`) | 13 | Retag `gisplan` | Existing GISPLAN definition already covers city-host T-WIST/Spinbox galleries; [T-WIST product](https://www.tmapy.cz/t-wist) |
| Exported ArcGIS Web AppBuilder (`env.js`, `simpleLoader.js`, `init.js`, Jimu layout/assets) | 6 | Retag `webappbuilder` | Existing Esri product; expanded the definition and discovery fingerprint for self-hosted exports |
| ArcGIS Hub/Sites (`opendata-ui`, `hubcdn.arcgis.com`, `/portal/apps/sites/`) | 4 | Retag `arcgishub` | Existing Hub definition; expanded discovery to cover custom-domain Hub and Enterprise Sites shells |
| SOFTPRO MBK (`SOFTPRO` branding plus `/js/locale/ua.js`) | 4 | Retag `softpro` | Existing SOFTPRO definition already described the older client |
| GeoMedia WebMap (`Version`/`Build`/`Licensed to` plus `WebClient.ashx` handlers) | 2 | Retag `geomediawebmap` | Existing Hexagon definition; expanded its handler fingerprint |
| Argenmap (`src/js/app.js`, Argenmap modules, retained `ign-geoportal-*` template) | 2 | Create `argenmap` | [Official IGN source and documentation](https://github.com/ign-argentina/argenmap) |
| AvanMap (`/AvanMap/`, `AvanMap.js`, `initAvanMap.js`) | 2 | Create `avanmap` | [Integrisoft Avansis.Hartă GIS product](https://www.integrisoft.ro/solutii/avansis-bdu/avansis-harta-gis/) |
| WebEWID (`WebEWID` title/branding and Portal Mapowy) | 2 | Create `webewid` | [Vendor software list](https://geomatyka-krakow.pl/portal/index.php/oprogramowanie) and [Portal Mapowy manual](https://gdanski.webewid.pl/dokuweb/portal-mapowy/portal-mapowy.html) |
| KC WebGIS (`gms*.kc-systemhaus.de/BMApp/` Angular application) | 2 | Create `kcwebgis` | [KC WebGIS product description](https://kc-systemhaus.de/ihre-geodaten-mobil-verfuegbar-on-offline-mit-dem-neuen-kc-webgis/) |
| ArcGIS Dashboards (`/apps/dashboards/{item-id}` and Dashboards shell) | 2 | Create `arcgisdashboards` | [Esri product](https://www.esri.com/en-us/arcgis/products/arcgis-dashboards/overview) and [documented URL form](https://doc.arcgis.com/en/dashboards/latest/create-and-share/dashboard-urls.htm) |

The applied set changes 39 catalog records: 29 move to existing software IDs and 10
move to the five new definitions. This reduces the reviewed custom-geoportal pool
from 1,028 to 989 without treating generic Leaflet, Angular, Drupal, or Liferay use
as product identity.

## Record groups changed

- `gisplan` (13): `mapserverkoprivnicecz`, `gisubcz`, `portalmubruntalcz`,
  `gismestouhcz`, `geoportaljhcz`, `mapymestodomazlicecz`, `geoportaljihlavacz`,
  `gismuvalmezcz`, `gistrebiccz`, `mapymestohranicecz`, `giszdarnscz`,
  `gisvelkemeziricicz`, `mapynmnmcz`.
- `webappbuilder` (6): `visorambgovco`, `webgis2artelit`,
  `geoportalgisqatarorgqa`, `mapkshhutimea`, `portalmapagoianagogovbr`,
  `mapascantabriaes`.
- `arcgishub` (4): `crcstncorg`, `dataglobalforestwatchorg`, `geodatacsugovcz`,
  `wwwmsilgojp`.
- `softpro` (4): `gissheptytskaradagovua`, `mapcitycvua`, `gisztradagovua`,
  `georadauzhgorodgovua`.
- `geomediawebmap` (2): `hartaoradearo`, `idecartagenaes`.
- `argenmap` (2): `idelasfloresnetar`, `visualizadoropisugbagobar`.
- `avanmap` (2): `gisprimariagiurgiuro`, `hartaprimariadrobetaro`.
- `webewid` (2): `giswalbrzychpl`, `gisbialystokpl`.
- `kcwebgis` (2): `gmsck09kcsystemhausdefulda`,
  `gmsck13kcsystemhausdedarmstadtdieburg`.
- `arcgisdashboards` (2): `wwwarcgiscomkentvillezoning`,
  `infraplanningowmapsarcgiscom`.

## Similar clusters deliberately left as `custom`

| Candidate | Matching records / installations | Why no definition was created |
|-----------|----------------------------------|-------------------------------|
| Other Korean municipal viewers | Several exact/near-exact script layouts | The V&G SODA/GT Map cluster is resolved in the fourth pass below; remaining templates still lack a stable named product or vendor attribution. Common municipal contractor code is not enough for a software ID. |
| HydroGuam north/south viewers | 2 routes | Two themed routes in one deployment, not independent installations of a named reusable product. |

## Follow-up discovery targets

- Search Polish authority pages and `*.webewid.pl` hosts for additional public
  WebEWID Portal Mapowy installations, avoiding authenticated role portals.
- Search Romanian municipal sites for `/AvanMap/` and `initAvanMap.js`.
- Search Argentine provincial/municipal IDE sites for retained Argenmap module and
  template fingerprints rather than the generic Leaflet library.
- Search indexed KC Systemhaus `/BMApp/` paths and confirm that each exposes a public
  BürgerGIS layer catalog.
- Identify a stable product name and responsible vendor before splitting the
  recurring Korean municipal-viewer templates from `custom`.

## Second pass — named products behind generic URLs

A second bounded GET-only pass checked 979 active records still tagged `custom`;
785 returned HTTP 200. Product-specific titles, application roots, compiled-client
names, vendor styles, and iframe targets were compared across the live set. Generic
framework assets such as Leaflet, OpenLayers, Angular, Bootstrap, and jQuery were
excluded from product identification.

| Fingerprint | Records | Decision | Product evidence |
|-------------|--------:|----------|------------------|
| `CartoVista Portal`, `/CartoVistaServer/maps/view`, `cartovistawebportal-*` | 1 | Create `cartovista` | [CartoVista product](https://cartovista.com/) and [documentation](https://knowledge.cartovista.com/) list a reusable cloud/self-hosted platform and many customers |
| Exact `IGO2` title and IGO2 Angular assembly | 1 | Create `igo2` | [Official project](https://www.igouverte.org/english/) and [source repository](https://github.com/infra-geo-ouverte/igo2) document reusable server deployments |
| `InfoMap Map Portal`, Emtel response header | 1 | Create `infomap` | [Vendor product and live-client list](https://www.infomap.co.nz/products/infomap-pro-web-mapping/) |
| `/bios/dpwebmap/`, `DPWebApp.nocache.js` | 1 | Create `dpwebmap` | Live dpSpatial installations and Stockholm documentation identify Digpro dpWebmap |
| `/desk/`, `GISProjectListing_mini.js`, 3MAP help tree | 1 | Create `3map` | [3 PORT product page](https://3-port.si/nase-resitve/javne-e-storitve/) and [3MAP manual](https://portal.3-port.si/trimap/_common/resource/help/index.htm) |
| Title `Facta WebGIS 4.0`, `facta.css` | 1 | Create `factawebgis` | [CGI Facta/WebGIS product family](https://www.cgi.com/fi/fi/tuoteratkaisut/facta), used across Finnish municipalities |
| `inkasPortal - GeoNet Online GmbH`, `inkas-portal.js` | 1 | Create `inkasportal` | Product title/code plus documented Düren and StädteRegion Aachen deployments |
| `geoviewer.io/css/nobel-style.css` | 1 | Create `geoviewer` | [Nobel Systems GeoViewer Online](https://www.nobel-systems.com/geoviewer-online) and multi-client product documentation |
| `my.floodreport.com.au/{authority}` embedding Water Technology apps | 2 | Create `floodintelligenceportal` | [Flood Intelligence Portal product overview](https://www.hydronet.com.au/wp-content/uploads/2024/05/Water-Technology-Waterlines-2023-2_HydroNET-article.pdf) identifies the shared cloud SaaS |
| `storymaps.arcgis.com/stories/{item-id}` | 1 | Create `arcgisstorymaps` | [Esri product](https://www.esri.com/en-us/arcgis/products/arcgis-storymaps/overview) and help documentation |

The second pass moves 11 more records out of `custom`, reducing the current
custom-geoportal pool from 989 to 978. New definitions with one current registry
record were accepted only where first-party evidence demonstrates multiple
deployments/customers or a reusable self-hosted product.

### Record groups changed in the second pass

- `cartovista`: `cmap2stthomasca`.
- `igo2`: `wwwforetouvertegouvqcca`.
- `infomap`: `mapsruapehudcgovtnz`.
- `dpwebmap`: `kartorstockholmse`.
- `3map`: `geoportal3portsimok`.
- `factawebgis`: `paikkatietopalvelupirnetfihameenkyro`.
- `inkasportal`: `giskreisduerende`.
- `geoviewer`: `missionviejogeoviewerio`.
- `floodintelligenceportal`: `myfloodreportcomaugbcma`,
  `myfloodreportcomaughcma`.
- `arcgisstorymaps`: `storymapsarcgiscomggmc`.

## Third pass — resolved product provenance

The unresolved repeated-host clusters were rechecked against first-party vendor
pages, public-agency procurement/architecture documents, and their live clients.
Four more shared products now have sufficient provenance and independent tenant
evidence:

| Fingerprint cluster | Records | Decision | Product evidence |
|---------------------|--------:|----------|------------------|
| `*.pgis.lv`, exact title `pGIS`, `/api/v1/classifiers/layers` | 2 | Create `pgis` | [TOPODATI services](https://topodati.lv/pakalpojumi/) identifies pGIS as its subscription geographic-information platform and includes WMS/WFS |
| `*-visorpublico.geoambiental.co/content-layout`, shared Angular bundles | 2 | Create `geoambiental` | [SIGMA Ingeniería](https://www.sigmaingenieria.com.co/) describes Geoambiental as its environmental GIS product; authority documents confirm SaaS deployments |
| `apps.nazcacatastro.com/public/{code}`, shared `main.js` plus tenant config | 2 | Create `nazca` | [NAZCA product root](https://apps.nazcacatastro.com/) identifies Soltesoft's cadastral software and the two public paths are independent municipal tenants |
| `*.xiltriongeoservicio.com/map`, identical Vite bundle with `xiltrioncatastro` and Dataxil strings | 2 | Create `xiltrion` | The first-party Xiltrion client identifies Dataxil S.A.S.; [CATASIG](https://www.catasig.gov.co/) lists both Yopal and Sabanalarga municipal services |

This pass moves eight more records out of `custom`. At the end of the third pass,
58 catalog records had been reclassified and 19 new software definitions created.
The review-only projection was therefore 1,028 to 970 custom Geoportals; the built
workspace contained 969 because another concurrent registry change also moved one
Geoportal away from `custom`.

### Record groups changed in the third pass

- `pgis`: `gulbenepgislv`, `jekabpilspgislv`.
- `geoambiental`: `cardervisorpublicogeoambientalco`,
  `corpoboyacavisorpublicogeoambientalco`.
- `nazca`: `appsnazcacatastrocom25754`, `appsnazcacatastrocom63001`.
- `xiltrion`: `sabanalargaxiltriongeoserviciocom`,
  `yopalxiltriongeoserviciocom`.

## Fourth pass — V&G and SHK municipal platforms

A country-bounded review of the remaining South Korean `custom` Geoportals found
seven live deployments loading the same V&G SODA OpenLayers client. Each
`soda.js` begins with a product/version header and a V&G copyright URL, while
[V&G's product site](https://www.vng.co.kr/product/platform/gtmap.do) names the
underlying municipal platform GT Map and its public-viewer solution GT Map
LifeMap. This is stronger than the generic Korean “Life Map” naming pattern that
was deliberately left unresolved in the first pass.

A separate Turkish `Kent Rehberi` cluster was checked against vendor evidence.
[SHK Bilişim](https://www.shkbilisim.com/) lists Gölbaşı, Pursaklar, and Üsküdar
as customers and documents its parcel, zoning, plan-note, and thematic-map
[Kent Bilgi Sistemi](https://www.shkbilisim.com/kbs.html). The Pursaklar client
also links the SHK logo directly; Gölbaşı and Üsküdar share the vendor's React
city-guide layout. Other Turkish city guides remain `custom` because the phrase
`Kent Rehberi` and use of ArcGIS JavaScript are not product-specific.

| Fingerprint cluster | Records | Decision | Product evidence |
|---------------------|--------:|----------|------------------|
| V&G `SODA {version}` header in `thirdparty/soda/soda.js`, common LifeMap layout and `/gs-gate/` | 7 | Create `gtmap` | V&G documents GT Map and GT Map LifeMap as its municipal spatial-information platform and public viewer |
| SHK-referenced Gölbaşı, Pursaklar, and Üsküdar city guides | 3 | Create `shkkbs` | SHK's product and reference pages establish the product boundary and all three customers |

This pass moves ten more records out of `custom`. Across all four passes, 68
catalog records were reclassified and 21 new software definitions were created.
The review-only projection is 1,028 to 960 custom Geoportals; the rebuilt
workspace contains 959 because of the concurrent one-record reduction noted
above.

### Record groups changed in the fourth pass

- `gtmap`: `gissuncheongokr`, `gissungokr`, `gisyongingokr`, `mapgimpogokr`,
  `wwwgyeongjugokrgjmap`, `wwwpohanggokrphgis`, `wwwsiheunggokrmap`.
- `shkkbs`: `cbsankaragolbasibeltr`, `cbspursaklarbeltr`,
  `cbsuskudarbeltr`.
