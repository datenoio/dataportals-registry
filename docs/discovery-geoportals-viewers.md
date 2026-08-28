# Discovering geoportal viewers

Regional and municipal map viewers (`catalog_type: Geoportal`). These are **viewers**: harvest the layer list, not PNG tiles ([harvest-viewers.md](harvest-viewers.md)). Overview: [discovery-geoportals.md](discovery-geoportals.md). SDI catalogs: [discovery-geoportals-sdi.md](discovery-geoportals-sdi.md).

One record per public application (config / tenant), not per layer.

## Wagmap / わが街ガイド (`wagmap`) {#wagmap}

PASCO hosted public WebGIS for Japanese prefectures and municipalities. Vendor: [pasco.co.jp](https://www.pasco.co.jp/biz/app-soft/wagamachiguide/). Tenants usually live under `www2.wagmap.jp` plus a city path, or a city custom domain loading GeoAccessJS portal assets.

**Signals:** hostname `www2.wagmap.jp`; title or branding わが街ガイド / Wagmap; GeoAccessJS; optional open-data catalog alongside the map gallery.

**Confirm:** GET the tenant URL and match Wagmap / GeoAccessJS branding. One record per public tenant, not per map layer. Skip staff-only municipal GIS that requires login for any map list.

| Tool | Query |
|------|-------|
| Google | `site:www2.wagmap.jp` |
| Google | `"わが街ガイド" OR Wagmap (オープンデータ OR 地図) site:.jp` |
| Censys | `web.names: "www2.wagmap.jp"` |
| crt.sh | `%.wagmap.jp` |

## EWMAPA (`ewmapa`) {#ewmapa}

GEOBID GIS used for Polish cadastral, utility, and municipal map publication. Vendor: [geobid.pl](https://geobid.pl/). Many public viewers are hosted on `*.geoportal2.pl`.

**Signals:** `geoportal2.pl` host; EWMAPA / GEOBID branding; municipal SIP / geoportal UI.

**Confirm:** GET the public map catalog (not a single WMS layer URL). Duplicate-check the same gmina under GeoServer or ArcGIS before adding a second record.

| Tool | Query |
|------|-------|
| Google | `site:geoportal2.pl` |
| Google | `"EWMAPA" OR "GEOBID" (geoportal OR SIP) site:.pl` |
| Censys | `web.names: "geoportal2.pl"` |
| crt.sh | `%.geoportal2.pl` |

## e-mapa.net (`emapa`) {#emapa}

Geo-System hosted Polish county/municipal SIP. Vendor: [geo-system.com.pl](https://www.geo-system.com.pl/). Public tenants live at `{powiat}.e-mapa.net` and load Pandora JS from `polska.e-mapa.net`.

**Signals:** hostname `*.e-mapa.net`; title “System Informacji Przestrzennej” / e-mapa.net; `/application/system/pandora/pandora.js`.

**Confirm:** GET the tenant URL and match e-mapa.net / Pandora branding. One record per powiat/gmina tenant. **Do not** set `software.id: ewmapa` — that is GEOBID on `geoportal2.pl`.

| Tool | Query |
|------|-------|
| Google | `site:e-mapa.net` |
| Google | `"e-mapa.net" OR "System Informacji Przestrzennej" (powiat OR gmina) site:.pl` |
| Censys | `web.names: "e-mapa.net"` |
| crt.sh | `%.e-mapa.net` |

## Loftmyndir (`loftmyndir`) {#loftmyndir}

Loftmyndir Kortasjá municipal map viewers in Iceland. Vendor: [loftmyndir.is](https://www.loftmyndir.is/). Tenants share `www.map.is/{municipality}/`.

**Signals:** hostname `www.map.is`; title “Kortasjá” plus Loftmyndir branding.

**Confirm:** GET the path tenant. **Do not** label Alta Vefsjá (`geo.alta.is/{tenant}/`, `alta`) or other Icelandic kortasjá sites as Loftmyndir. Skip `geo.alta.is/geoserver` (`geoserver`).

| Tool | Query |
|------|-------|
| Google | `site:map.is kortasjá OR loftmyndir` |
| Google | `"Loftmyndir" (kortasjá OR geoportal) site:.is` |
| Censys | `web.names: "map.is"` |
| crt.sh | `map.is` |

## Alta Vefsjá (`alta`) {#alta}

Alta ehf. OpenLayers municipal planning viewer. Tenants under `geo.alta.is/{tenant}/` load `altacode` vefsja assets.

**Signals:** `geo.alta.is` path that is **not** `/geoserver`; scripts from `storage.googleapis.com/altacode/js/vefsja/`; title Kortasjá.

**Confirm:** GET the viewer path. Keep the GeoServer root as a separate `geoserver` record.

| Tool | Query |
|------|-------|
| Google | `site:geo.alta.is kortasjá OR vefsjá` |
| Censys | `web.names: "geo.alta.is"` |

## Bulplan UNIMAP (`bulplan`) {#bulplan}

Bulgarian municipal integrated geoportal. Tenants at `{municipality}.bulplan.eu` (UNIMAP branding).

**Signals:** hostname `*.bulplan.eu`; title or chrome UNIMAP / Bulplan.

**Confirm:** GET the public map. One record per municipality. Skip dead Apache default pages.

| Tool | Query |
|------|-------|
| Google | `site:bulplan.eu` |
| Google | `"UNIMAP" OR Bulplan (геопортал OR geoportal) site:.bg` |
| Censys | `web.names: "bulplan.eu"` |
| crt.sh | `%.bulplan.eu` |

## Tobel (`tobel`) {#tobel}

Bulgarian municipal Web GIS. Tenants at `{city}.tobel.bg` (and hosts such as `shumenweb.tobel.bg`).

**Signals:** hostname `*.tobel.bg`; municipal GIS / кадастър UI.

**Confirm:** GET the public map. One record per city tenant.

| Tool | Query |
|------|-------|
| Google | `site:tobel.bg` |
| Google | `"tobel" (GIS OR геопортал OR кадастър) site:.bg` |
| Censys | `web.names: "tobel.bg"` |
| crt.sh | `%.tobel.bg` |

## geoportal.ch (`geoportalch`) {#geoportalch}

Hosted Swiss cantonal geoportal. Tenants share `www.geoportal.ch/{canton}` (ktzg, ktai, ktar, …).

**Signals:** hostname `www.geoportal.ch` with a canton path; title Geoportal.

**Confirm:** GET the canton path. Distinct from swisstopo **mf-geoadmin3** (`mfgeoadmin3`).

| Tool | Query |
|------|-------|
| Google | `site:geoportal.ch` |
| Google | `"geoportal.ch" (Kanton OR geoportal) site:.ch` |
| Censys | `web.names: "geoportal.ch"` |
| crt.sh | `geoportal.ch` |

## GIS4Smart (`gis4smart`) {#gis4smart}

DOTSOFT municipal Web GIS (Y.Ge.P. / DotSpatial branding). Confirm the public map UI. Do not also register a bundled GeoServer on the same host.

| Tool | Query |
|------|-------|
| Google | `"GIS4Smart" geoportal` |
| Censys | `web.endpoints.http.body: "GIS4Smart"` |

## Evrymap (`evrymap`) {#evrymap}

Consortis Geospatial municipal map portal. SPA titled Evrymap; MapServer WMS/WFS behind the viewer. Common in Greek municipalities (sometimes on `*.open1.eu`).

**Signals:** HTML title “Evrymap”; `/mapserver/mapserv` GetCapabilities; Consortis branding.

**Confirm:** GET the public map UI and match Evrymap. Harvest WMS layers when GetCapabilities is XML. Do not also register the bundled MapServer as a second catalog on the same host.

| Tool | Query |
|------|-------|
| Google | `"Evrymap" (Δήμος OR geoportal OR MapServer) site:.gr` |
| Censys | `web.endpoints.http.html_title: "Evrymap"` |

## GeoMapFish (`geomapfish`) {#geomapfish}

Open-source WebGIS (c2cgeoportal + ngeo). Common in Swiss cantons and other European public geoportals. Site: [geomapfish.org](https://geomapfish.org).

**Signals:** `ngeo` / `gmf-` CSS classes; `/themes` JSON; WMS/WMTS theme tree; `c2cgeoportal` in HTML or JS bundles.

**Confirm:** GET `/themes` (or the documented theme API) and a public map UI. One record per public geoportal, not per theme.

| Tool | Query |
|------|-------|
| Google | `"GeoMapFish" OR c2cgeoportal (geoportail OR geoportal) -site:github.com` |
| Google | `inurl:/themes ngeo OR geomapfish` |
| Censys | `web.endpoints.http.body: "c2cgeoportal"` |
| Censys | `web.endpoints.http.body: "gmf-"` |

## Tianditu (`tianditu`) {#tianditu}

China National Geographic Information Public Service Platform (Map World). National, provincial, and municipal nodes share NGCC APIs and branding. Site: [tianditu.gov.cn](https://www.tianditu.gov.cn).

**Signals:** `tianditu` in hostname or HTML; 天地图 branding; Map World API keys / `tianditu.gov.cn` tile or widget hosts.

**Confirm:** GET the public node (province or city) and match 天地图 / Tianditu. One record per public node, not per map API key. Skip pure tile endpoints with no catalog UI.

| Tool | Query |
|------|-------|
| Google | `"天地图" (省 OR 市 OR 地理信息) -site:tianditu.gov.cn` |
| Google | `inurl:tianditu OR "Map World" 地理` |
| Censys | `web.endpoints.http.body: "tianditu"` |

## Masterportal (`masterportal`) {#masterportal}

Hamburg LGV open-source map viewer used by German federal, state, and municipal agencies. Site: [masterportal.org](https://www.masterportal.org).

**Signals:** `Masterportal` in title or footer; `lgv-config` / `config.js` portal JSON; OGC WMS/WFS/CSW theme tree.

**Confirm:** GET the viewer URL and match Masterportal config plus a public layer tree. One record per public portal instance.

| Tool | Query |
|------|-------|
| Google | `"Masterportal" (Geoportal OR Kartendienst) site:.de -site:masterportal.org` |
| Censys | `web.endpoints.http.body: "Masterportal"` |
| Censys | `web.endpoints.http.body: "lgv-config"` |

## PopGIS (`popgis`) {#popgis}

Pacific Community (SPC) population / census GIS. Site: [spc.int PopGIS](https://www.spc.int/our-work/geospatial/popgis).

**Confirm:** GET the public map/layer catalog for a country or territory node.

| Tool | Query |
|------|-------|
| Google | `"PopGIS" (census OR geospatial) (Pacific OR SPC)` |
| Censys | `web.endpoints.http.body: "PopGIS"` |

## MangoMap (`mangomap`) {#mangomap}

Hosted map galleries. Tenants on `mangomap.com`. Site: [mangomap.com](https://mangomap.com).

**Confirm:** GET the organization portal. One record per tenant, not per map.

| Tool | Query |
|------|-------|
| Google | `site:mangomap.com` |
| crt.sh | `%.mangomap.com` |

## NetGIS Server (`netgisserver`) {#netgisserver}

Netcad GIS server, common in Turkish municipalities. Product: [NetGIS Server](https://www.netcad.com/tr/urunler/netgis-server).

**Signals:** `/Netgis7`, `/keos/` city guide, title `NetGIS Server 7`.

**Confirm:** GET the KEOS viewer or `/Netgis7` title page. Optional WMS: `wms.ashx` GetCapabilities. Do not confuse with Sampaş `/KentrehberiApp/` or GiSoftGis Angular city guides.

| Tool | Query |
|------|-------|
| Google | `intitle:"NetGIS Server 7" OR inurl:/Netgis7 OR inurl:/keos/` |
| Censys | `web.endpoints.http.html_title: "NetGIS Server"` |

## cardo (`cardo`) {#cardo}

IDU IT geospatial platform (Germany and neighbours). Site: [cardogis.com](https://cardogis.com).

**Signals:** `/net3/public/`, cardo.Map, `cardo` in HTML/JS.

**Confirm:** GET the public map/catalog UI under `/net3/public/` (or the branded geoportal home). Skip intranet-only cardo installs.

| Tool | Query |
|------|-------|
| Google | `"cardo.Map" OR inurl:/net3/public/` |
| Censys | `web.endpoints.http.body: "cardo.Map"` |

## GC Navi (`gcnavi`) {#gcnavi}

Informatix GeoCloud WebGIS for Japanese local governments. Product: [GC Navi](https://www.informatix.co.jp/gc/navi/).

**Signals:** `geocloud.jp/webgis/`, GC Navi, `bt=` / `p=` query parameters.

**Confirm:** GET the tenant WebGIS home (org subdomain on `geocloud.jp`). Distinct from internal GC Planets. One record per municipality tenant.

| Tool | Query |
|------|-------|
| Google | `"GC Navi" OR inurl:geocloud.jp/webgis/` |
| Censys | `web.names: "geocloud.jp"` |
| crt.sh | `%.geocloud.jp` |

## NOL-IS (`nolis`) {#nolis}

German municipal WebGIS. Site: [nol-is.de](https://www.nol-is.de).

**Signals:** assets from `maps.nol-is.de` or `static.nol-is.de`; NOL-IS / NOLIS branding.

**Confirm:** GET the public geoportal home. Skip vendor marketing pages.

| Tool | Query |
|------|-------|
| Google | `"NOL-IS" OR "NOLIS" Geoportal site:.de` |
| Censys | `web.names: "nol-is.de"` |

## GiSoftGis (`gisoftgis`) {#gisoftgis}

Turkish municipal Angular city guide. Path `/GiSoftGis/` with hash `#/cityguidepublic`.

**Signals:** `gi-ajax-loading-indicator`; meta “Kent Rehberi Uygulaması”.

**Confirm:** GET `/GiSoftGis/`. Distinct from NetGIS `/keos/` and Sampaş `/KentrehberiApp/`.

| Tool | Query |
|------|-------|
| Google | `inurl:/GiSoftGis/` |
| Censys | `web.endpoints.http.body: "GiSoftGis"` |

## Sampaş WebGIS (`sampaswebgis`) {#sampaswebgis}

AKOS municipal city-guide map. Typical path `/KentrehberiApp/Index`.

**Confirm:** GET that path; page title contains `SAMPAŞ WEBGIS`.

| Tool | Query |
|------|-------|
| Google | `"SAMPAŞ WEBGIS" OR inurl:/KentrehberiApp/` |
| Censys | `web.endpoints.http.html_title: "SAMPA"` |

## ActiveMap GIS (`activemapgis`) {#activemapgis}

Gradoservice municipal GIS (often Russian cities). Product: [ActiveMap](https://gradoservice.ru/products/activemap/).

**Confirm:** GET the public map portal home. Skip desktop-only marketing.

| Tool | Query |
|------|-------|
| Google | `"ActiveMap" GIS (портал OR Gradoservice)` |
| Censys | `web.endpoints.http.body: "ActiveMap"` |

## map.apps (`mapapps`) {#mapapps}

con terra WebGIS framework. Product: [map.apps](https://www.conterra.de/portfolio/mapapps). Often paired with smart.finder SDI (`smartfindersdi`).

**Signals:** `/mapapps/`; con terra / map.apps in HTML.

**Confirm:** GET the public `/mapapps/` viewer (not a login-only intranet). If smart.finder is the catalog UI, prefer `smartfindersdi` for that catalog.

| Tool | Query |
|------|-------|
| Google | `inurl:/mapapps/ (Geoportal OR "map.apps")` |
| Censys | `web.endpoints.http.body: "/mapapps/"` |

## CoGIS (`cogis`) {#cogis}

Data East geoportal stack. Site: [cogis.dataeast.com](https://cogis.dataeast.com). Map services may be CoGIS Server, eLiteGIS (`elitegis`), or ArcGIS Server — register the **public catalog UI**.

**Confirm:** GET CoGIS Portal home. Prefer `elitegis` only when that is the branded viewer with no CoGIS Portal.

| Tool | Query |
|------|-------|
| Google | `"CoGIS" (портал OR Portal OR geoportal) -site:dataeast.com` |
| Censys | `web.endpoints.http.body: "CoGIS"` |

## OpenGeoPortal (`opengeoportal`) {#opengeoportal}

Federated academic geoportal (Tufts and partners).

**Confirm:** GET the search/home UI that lists layers across institutions. Do not add a single layer preview URL.

| Tool | Query |
|------|-------|
| Google | `"OpenGeoPortal" OR "Open Geoportal" (layers OR geodata)` |
| Censys | `web.endpoints.http.body: "OpenGeoPortal"` |

## smart.finder SDI (`smartfindersdi`) {#smartfindersdi}

con terra metadata/search portal. Product: [smart.finder SDI](https://www.conterra.de/portfolio/smartfinder-sdi). Often sits next to `mapapps`.

**Confirm:** GET the public catalog search (CSW or finder UI). If only `/mapapps/` is public, use `mapapps`.

| Tool | Query |
|------|-------|
| Google | `"smart.finder SDI" OR "smart.finder" Geoportal site:.de` |
| Censys | `web.endpoints.http.body: "smart.finder"` |

## GIS WebServer SE (`giswebse`) {#giswebse}

KB Panorama web GIS. Site: [gisweb.ru](https://www.gisweb.ru).

**Confirm:** GET the public geoportal (layer tree / map). Skip desktop GIS marketing.

| Tool | Query |
|------|-------|
| Google | `"GIS WebServer SE" (геопортал OR geoportal)` |
| Censys | `web.endpoints.http.body: "GIS WebServer SE"` |

## MapGIS IGServer (`mapgisigserver`) {#mapgisigserver}

Zondy Cyber GIS server, common in Chinese government and natural-resources SDIs. Product: [MapGIS IGServer](https://www.mapgis.com/index.php?a=shows&catid=310&id=331). .NET installs often listen on **6163**; Java on **8089**.

**Signals:** `/igs/rest/` in the URL or HTML; title or footer “MapGIS IGServer”; IGS 1.0 `/igs/rest/mrcs/docs`, IGS 2.0 `/igs/rest/services`.

**Confirm:** GET `https://host/igs/rest/mrcs/docs?f=json` (IGS 1.0 map-document list) or `https://host/igs/rest/services?f=json` (IGS 2.0 service catalog). Register the public `/igs` root (or the node that exposes that REST), not `/igs/manager` admin. Skip MapGIS Desktop marketing.

**False positives:** hostnames containing `mapgis` that are actually ArcGIS Server (`/arcgis/rest/services`, e.g. some South Asian `mapgis.*` sites). IGS 2.0 REST resembles ArcGIS REST — still `mapgisigserver` when the path is `/igs/rest/`, not `/arcgis/rest/`. Do not also register a second ArcGIS Server record on the same IGServer host.

| Tool | Query |
|------|-------|
| Google | `"MapGIS IGServer" OR inurl:/igs/rest/mrcs/docs -site:mapgis.com -site:github.com` |
| Google | `inurl:/igs/rest/services "MapGIS"` |
| Censys | `web.endpoints.http.body: "/igs/rest/mrcs"` |
| FOFA | `body="/igs/rest/" && title="MapGIS"` |

## Trimble Locus IMS (`trimblelocus`) {#trimblelocus}

Finnish municipal karttapalvelu from Trimble Locus (formerly Tekla GIS). Vendor: [Trimble UPA](https://upa.trimble.com/fi/toimialat/julkishallinto). Distinct from Turkish BelsisIMS (`belsisims`) and Sitowise Louhi (`louhi`).

**Signals:** path `/IMS/` or `/ims/`; ASP.NET MVC; scripts `/IMS/bundles/imscore` and `/IMS/bundles/tekla-mvc-common`; footer link to `upa.trimble.com`. Some cities host the viewer on `*.asiointi.fi`.

**Confirm:** GET the public map UI and match IMS bundles or Trimble branding. One record per city tenant, not per layer. Skip staff-only Locus back-office.

| Tool | Query |
|------|-------|
| Google | `inurl:/IMS/ karttapalvelu site:.fi` |
| Google | `"karttapalvelu" IMS OR "tekla-mvc" site:.fi` |
| Censys | `web.endpoints.http.body: "tekla-mvc-common"` |
| Censys | `web.endpoints.http.body: "/IMS/bundles/imscore"` |

## Sitowise Louhi (`louhi`) {#louhi}

Sitowise municipal GIS public map viewer. Site: [sitowise.com Louhi](https://www.sitowise.com/digital-solutions/louhi-gis-platform-municipalities). Distinct from Trimble Locus IMS (`trimblelocus`); Louhi maps may still attribute some layers as Locus data.

**Signals:** OpenLayers `/Scripts/integration/openlayers/ol.js`; Sitowise snoobi `partner=stw`; Finnish municipal `kartta.` host without `/IMS/`.

**Confirm:** GET the public karttapalvelu. One record per municipality. Do not also tag the same UI as `trimblelocus`.

| Tool | Query |
|------|-------|
| Google | `"karttapalvelu" Sitowise OR Louhi site:.fi -inurl:/IMS` |
| Censys | `web.endpoints.http.body: "partner=stw"` |

## Trimble Landfolio (`landfolio`) {#landfolio}

Spatial Dimension / Trimble mining and land cadastre map portals (formerly FlexiCadastre). Directory: [spatialdimension.com/portals](https://www.spatialdimension.com/portals/).

**Signals:** host `portals.landfolio.com/{country}/`; title “Spatial Dimension Landfolio” or “Cadastre Map Portal”.

**Confirm:** GET the public map portal (not `/arcgis/rest/services`). ArcGIS REST on Landfolio infrastructure stays `arcgisserver`. One record per country portal.

| Tool | Query |
|------|-------|
| Google | `site:portals.landfolio.com` |
| Google | `"Landfolio" OR FlexiCadastre ("mining cadastre" OR "map portal")` |
| Censys | `web.names: "portals.landfolio.com"` |
| crt.sh | `%.landfolio.com` |

## Hajk (`hajk`) {#hajk}

Open-source Swedish web GIS (React, Material UI, OpenLayers). Site: [hajkmap.github.io/Hajk](https://hajkmap.github.io/Hajk/). Source: [hajkmap/Hajk](https://github.com/hajkmap/Hajk). Installation gallery: [hajkmap.se användare](https://hajkmap.se/valkommen-till-hajk/exempelsamling/).

**Signals:** HTML title “Hajk - open source webGIS”; `appConfig.json` with `mapserviceBase` (`/api/v1`, `/api/v2`, or `/mapservice`); `appName` Hajk.

**Confirm:** GET `/appConfig.json` (or `/publik/appConfig.json`). One record per public map application, not the GeoServer/ArcGIS backend on the same municipality. Skip login-only Hajk (Örebro staff GIS, Partille). Skip the Netlify demo.

| Tool | Query |
|------|-------|
| Google | `"Hajk - open source webGIS" OR "mapserviceBase" karta site:.se` |
| Google | `inurl:appConfig.json Hajk` |
| Censys | `web.endpoints.http.html_title: "Hajk - open source webGIS"` |

## Spatial Suite (`spatialsuite`) {#spatialsuite}

Sweco web GIS; public client is SpatialMap. Vendor: [Sweco Spatial Suite](https://www.sweco.dk/ydelser/digitale-loesninger/spatial-suite/). Distinct from NIRAS KortInfo.

**Signals:** `/js/standard/browserdetect.js?ver=` SpatialMap version; Danish `webkort.` or `*kort*` municipal hosts; title SpatialMap.

**Confirm:** GET the public webkort. One record per municipality viewer, not the GeoServer backend on the same city.

| Tool | Query |
|------|-------|
| Google | `"SpatialMap" OR "Spatial Suite" webkort site:.dk` |
| Google | `inurl:webkort kommune site:.dk` |
| Censys | `web.endpoints.http.body: "browserdetect.js?ver="` |

## KortInfo (`kortinfo`) {#kortinfo}

NIRAS hosted web GIS. Vendor: [NIRAS KortInfo](https://www.niras.dk/sektorer/data-digitalisering/webgis-kortinfo/). Distinct from Sweco Spatial Suite (`spatialsuite`).

**Signals:** host `drift.kortinfo.net`; path `/Map.aspx` with `Site=` tenant; titles or help on `help.kortinfo.net`; Danish municipal “KortInfo” / Kortviseren pages.

**Confirm:** GET the public `Map.aspx` tenant (Borgersite, kortHjemmeside, or the city’s documented page). One record per municipality `Site`, not per map page on the same tenant. Skip login-only sagsbehandling maps.

| Tool | Query |
|------|-------|
| Google | `site:drift.kortinfo.net Map.aspx` |
| Google | `"KortInfo" (kommune OR webkort OR kortviser) site:.dk` |
| Censys | `web.names: "kortinfo.net"` |
| crt.sh | `%.kortinfo.net` |

## GEUSMAP (`geusmap`) {#geusmap}

Geological Survey of Denmark and Greenland map application. Home: [data.geus.dk/geusmap](https://data.geus.dk/geusmap/). Named databases share `/geusmap/?mapname=`.

**Signals:** `/geusmap/?mapname=`; Jupiter, GERDA, or Greenland Mineral Resources branding; WMS/WFS export controls.

**Confirm:** GET `https://host/geusmap/?mapname={name}`. One record per public mapname. GEUS ArcGIS REST and GeoNetwork on other hosts stay those software ids.

| Tool | Query |
|------|-------|
| Google | `inurl:/geusmap/?mapname=` |
| Google | `"GEUSMAP" OR "geusmap" (Jupiter OR GERDA)` |
| Censys | `web.endpoints.http.body: "geusmap"` |

## GISApp (`gisapp`) {#gisapp}

Fida Solutions / Urbanova hosted municipal GIS. Tenants: `{city}.gisapp.ro`. Distinct from Kaliopa iObčina (`iobcina`) and from EQWC.

**Signals:** host `*.gisapp.ro`; urbanism certificate / PortalPublic UI; Romanian municipal GIS.

**Confirm:** GET the public city tenant. One record per municipality. ArcGIS REST on `webadaptor.gisapp.ro` stays `arcgisserver`.

| Tool | Query |
|------|-------|
| Google | `site:gisapp.ro` |
| Google | `"gisapp.ro" (geoportal OR urbanism)` |
| Censys | `web.names: "gisapp.ro"` |
| crt.sh | `%.gisapp.ro` |

## iObčina (`iobcina`) {#iobcina}

Kaliopa cloud municipal GIS (Croatian brand iOpćina). Site: [kaliopa.si/iobcina](https://www.kaliopa.si/iobcina/). Distinct from Romanian GISApp (`gisapp`).

**Signals:** host `gis.iobcina.si` or `iopcina.hr`; ASP.NET `/gisapp/Default.aspx?a={tenant}`.

**Confirm:** GET the public viewer. One record per municipality or county tenant, plus the Kaliopa hub if it is a separate public catalog.

| Tool | Query |
|------|-------|
| Google | `inurl:/gisapp/Default.aspx iobcina OR iopcina` |
| Google | `"iObčina" OR iOpćina GIS` |
| Censys | `web.names: "iobcina.si"` |
| crt.sh | `%.iobcina.si` |

## Astun iShare (`ishare`) {#ishare}

UK local-government public mapping portal (Astun Technology). Product: [astuntechnology.com/ishare](https://www.astuntechnology.com/ishare/). Distinct from Cadcorp SIS WebMap (`cadcorp`) and from the INDEPTH iShare **microdata** catalog.

**Signals:** footer “Powered by iShare”; paths `/mymaps.aspx`, `/myhouse.aspx`; Astun branding.

**Confirm:** GET the public My Maps / Find my nearest UI. One record per authority portal, not per map layer. Skip intranet-only iShare GIS.

| Tool | Query |
|------|-------|
| Google | `"Powered by iShare" (maps OR "my house" OR geoportal) site:.gov.uk` |
| Google | `inurl:mymaps.aspx OR inurl:myhouse.aspx iShare` |
| Censys | `web.endpoints.http.body: "Powered by iShare"` |

## Cadcorp SIS WebMap (`cadcorp`) {#cadcorp}

Cadcorp (NEC) public web GIS. Product: [cadcorp.com](https://www.cadcorp.com). Distinct from disy Cadenza (`cadenza`) and from Astun iShare (`ishare`).

**Signals:** SIS WebMap / Web Map Layers / GeognoSIS branding; Cadcorp in HTML or GetCapabilities.

**Confirm:** GET the public web map and match Cadcorp/GeognoSIS. One record per public portal. Skip intranet WebMap Editor.

| Tool | Query |
|------|-------|
| Google | `"Cadcorp" OR "SIS WebMap" OR GeognoSIS (geoportal OR "web map") site:.gov.uk` |
| Google | `"Web Map Layers" Cadcorp` |
| Censys | `web.endpoints.http.body: "Cadcorp"` |

## Geometa (`geometa`) {#geometa}

Gems Development urban-planning GIS and public GIS OGD geoportals (Agate). Product: [geometa.ru](https://geometa.ru/), module docs [geometa.ru/module/agate](https://geometa.ru/module/agate/). Distinct from unrelated “GeoMeta” catalog products. Typical Russian regional tenants: `portal-gisogd.*`, `agate.*`.

**Signals:** HTML title «Портал ГИСОГД»; short body “agat doesn’t work without JavaScript”; `/agate_` paths; Geometa / Agate / Gems Development branding.

**Confirm:** GET the public portal and match Agate. One record per public tenant. Skip login-only document workflows. Do **not** set `software.id: geometa` from a `gisogd.` hostname alone — sites without Agate strings stay `custom`.

| Tool | Query |
|------|-------|
| Google | `"Портал ГИСОГД" OR inurl:portal-gisogd OR inurl:agate (геопортал OR ГИСОГД) site:.ru` |
| Google | `"agat doesn’t work without JavaScript" OR "agat doesn't work without JavaScript"` |
| Censys | `web.endpoints.http.body: "agat doesn’t work without JavaScript"` |
| Censys | `web.names: "portal-gisogd"` |

## Other geoportal platforms

Search the product title with the country TLD. One record per public catalog UI.

| `software.id` | Signals / confirm | Typical query |
|---------------|-------------------|---------------|
| `gcnavi` | see above | |
| `nolis` | see above | |
| `cardo` | see above | |
| `netgisserver` | see above | |
| `sampaswebgis` | see above | |
| `gisoftgis` | see above | |
| `activemapgis` | see above | |
| `mapapps` | see above | |
| `belsisims` | `ims.*/Projects/*/Pages/KRH.aspx` | `KRH.aspx Belsis` |
| `orbismap` | ORBISMap Russian GIS | `"ORBISMap" геопортал` |
| `opengeoportal` | see above | |
| `geonomics` | Vue/Mapbox, geonomix.kz | `"Geonomics" OR geonomix геопортал` |
| `emapa` | `*.e-mapa.net` Pandora | `site:e-mapa.net` |
| `loftmyndir` | `www.map.is/{muni}/` | `site:map.is loftmyndir` |
| `alta` | `geo.alta.is/{tenant}/` vefsja | `site:geo.alta.is kortasjá` |
| `bulplan` | `{muni}.bulplan.eu` UNIMAP | `site:bulplan.eu` |
| `tobel` | `{city}.tobel.bg` | `site:tobel.bg` |
| `geoportalch` | `www.geoportal.ch/{canton}` | `site:geoportal.ch` |
| `cogis` | see above | |
| `elitegis` | ArcGIS-compatible REST (Atemiko) | `"eLiteGIS" OR elitegis REST` |
| `smartfindersdi` | see above | |
| `giswebse` | see above | |
| `ingrid` | German InGrid CSW/OpenSearch | `"InGrid" (CSW OR Geoportal) site:.de` |
| `metagis` | MetaGIS (SE) | `"MetaGIS" geoportal site:.se` |
| `isigeo` | IsiGéo / Geomatika (not Isogeo SaaS) | `"IsiGéo" OR Isigeo géoportail` |
| `isogeo` | see above | |
| `mviewer` | see above | |
| `qgisserver` | see above | |
| `openeo` | see above | |
| `gis4smart` | GIS4Smart municipal | `"GIS4Smart" geoportal` |
| `evrymap` | Consortis Evrymap municipal | `"Evrymap" (Δήμος OR geoportal) site:.gr` |
| `geoportalrlp` | Rhineland-Palatinate stack | `geoportal.rlp.de` (do not re-add known nodes) |
| `copernicusdhus` | Copernicus DHuS | `"DHuS" Copernicus (catalogue OR odata)` |
| `popgis` | see above | |
| `ncwms` | see above | |
| `mangomap` | see above | |
| `opendatacube` | see above | |
| `datacubews` | ODC OWS WMS/WCS | `"datacube-ows" OR "datacube_ows"` |
| `supermapiserver` | SuperMap iServer REST | `"SuperMap iServer" rest` |
| `supermapiportal` | SuperMap iPortal | `"SuperMap iPortal"` |
| `mapgisigserver` | see above | |
| `trimblelocus` | Finnish `/IMS/` karttapalvelu | `inurl:/IMS/ karttapalvelu site:.fi` |
| `louhi` | Sitowise Louhi viewer | `"Louhi" karttapalvelu Sitowise` |
| `landfolio` | `portals.landfolio.com` cadastre maps | `site:portals.landfolio.com` |
| `spatialsuite` | Sweco SpatialMap webkort | `"SpatialMap" webkort site:.dk` |
| `kortinfo` | NIRAS `drift.kortinfo.net/Map.aspx` | `site:drift.kortinfo.net Map.aspx` |
| `geusmap` | `/geusmap/?mapname=` | `inurl:geusmap mapname` |
| `gisapp` | `{city}.gisapp.ro` municipal GIS | `site:gisapp.ro` |
| `iobcina` | Kaliopa `/gisapp/Default.aspx?a=` | `inurl:/gisapp/Default.aspx` |
| `ishare` | Astun iShare / `mymaps.aspx` | `"Powered by iShare" site:.gov.uk` |
| `cadcorp` | Cadcorp SIS WebMap / GeognoSIS | `"SIS WebMap" OR GeognoSIS Cadcorp` |
| `reearth` | Re:Earth / PLATEAU VIEW | `"Re:Earth" OR "PLATEAU VIEW"` |
| `gpatlas` | GP Atlas | `"GP Atlas" GIS` |
| `geometa` | see above | |
| `carto` | CARTO Builder / cloud maps | `site:carto.com` government tenants only |
| `mfgeoadmin3` | swisstopo geoadmin3 forks | `"geoadmin3" OR mf-geoadmin3` |
| `datumgis` | DATUM GIS | `"DATUM GIS" геопортал` |
| `evergis` | EverGIS / ЭверГИС | `"EverGIS" OR "ЭверГИС"` |
| `ingeo` | InGeo / ГИС ИнГео | `"ИнГео" GIS` |
| `farvatergisogd` | Farvater GIS OGD | `"Farvater" ГИСОГД` |

