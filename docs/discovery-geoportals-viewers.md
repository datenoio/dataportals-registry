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

Open-source WebGIS (c2cgeoportal + ngeo). Common in Swiss cantons and other European public geoportals. Site: [geomapfish.org](https://geomapfish.org). Distinct from TYDAC MAP+ (`mapplus`).

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

**Confirm:** GET the viewer URL and match Masterportal config plus a public layer tree. One record per public portal instance. Do **not** set `masterportal` from vianovis touvia.MAPS tenants (`loadTouviaMaps()`, `touvia.de/scripts/loader.js`) — those are `touviamaps`. Do **not** set `masterportal` from VC Map (`html.vcs-ui`, title `VC Map`).

| Tool | Query |
|------|-------|
| Google | `"Masterportal" (Geoportal OR Kartendienst) site:.de -site:masterportal.org` |
| Censys | `web.endpoints.http.body: "Masterportal"` |
| Censys | `web.endpoints.http.body: "lgv-config"` |

## touvia.MAPS (`touviamaps`) {#touviamaps}

vianovis GmbH hosted municipal web GIS. Product: [touvia.MAPS](https://www.vianovis.de/). Public tenants live at `vianovis.net/{tenant}/` or a city/county host that still loads `touvia.de/scripts/loader.js`. Distinct from Hamburg Masterportal (`masterportal`) even when the same vendor also offers touvia.MASTERPORTAL.

**Signals:** `loadTouviaMaps()`; script `touvia.de/scripts/loader.js`; `meta` copyright `vianovis GmbH`; assets under `touvia.de/uploads/{id}/config/`; title `… - Geoportal` / `… - Stadtplan` / `… - BürgerGIS`.

**Confirm:** GET the public portal and match `loadTouviaMaps` plus vianovis/touvia credits. One record per municipality or Landkreis tenant. Skip the marketing site `vianovis.de`. Do **not** set `touviamaps` from Masterportal (`masterportal.js`, `lgv-config`) or VC Map (`html.vcs-ui`). Do **not** set `masterportal` from touvia.MAPS.

| Tool | Query |
|------|-------|
| Google | `site:vianovis.net Geoportal OR BürgerGIS` |
| Google | `"vianovis GmbH" (Geoportal OR Stadtplan OR BürgerGIS) site:.de` |
| Censys | `web.names: "vianovis.net"` |
| crt.sh | `%.vianovis.net` |

## INGRADA online (`ingrada`) {#ingrada}

Softplan Informatik municipal web GIS. Product: [INGRADA](https://www.ingrada.de/startseite.html). Distinct from VertiGIS WebOffice (`weboffice`), MapGuide (`mapguide`), and generic German BürgerGIS landing pages.

**Signals:** title `INGRADA online {project}`; iframe `#ingrada`; script `/mobile/message-channel.js`; path `Softplan.Ingrada.Mobile` with `ProductId=IngradaOnline`; optional host `ingradaweb.org/{city}/online`.

**Confirm:** GET the public BürgerGIS / online viewer and match `ProductId=IngradaOnline` plus the mobile message-channel client. One record per municipality or Landkreis. Do **not** set `ingrada` from a BürgerGIS hostname that is WebOffice, ArcGIS, or a CMS landing page (Pforzheim, Böblingen `lrabb.de`). Do **not** set `mapguide` from INGRADA Mobile.

| Tool | Query |
|------|-------|
| Google | `"INGRADA online" (BürgerGIS OR Geoportal) site:.de` |
| Google | `inurl:Softplan.Ingrada.Mobile OR site:ingradaweb.org` |
| Censys | `web.endpoints.http.html_title: "INGRADA online"` |
| crt.sh | `ingradaweb.org` |

## VC Map (`vcmap`) {#vcmap}

Virtual City Systems open-source 2D/3D web GIS. Product: [VC Map](https://github.com/virtualcitySYSTEMS/map-ui) / [vc.systems](https://vc.systems/). Distinct from Hamburg Masterportal (`masterportal`) and vianovis touvia.MAPS (`touviamaps`).

**Signals:** `html.vcs-ui`; title `VC Map`; script `./assets/start.js`; optional host `{city}.virtualcitymap.de`.

**Confirm:** GET the public app and match `vcs-ui` plus `assets/start.js`. One record per city or Landkreis digital twin. Do **not** set `vcmap` from Masterportal (`masterportal.js`, `lgv-config`), touvia.MAPS (`loadTouviaMaps()`), or a generic Cesium 360 viewer without `vcs-ui` (Kronach Geoportal).

| Tool | Query |
|------|-------|
| Google | `"VC Map" OR virtualcitymap (digitaler Zwilling OR Stadtmodell) site:.de` |
| Google | `site:virtualcitymap.de` |
| Censys | `web.endpoints.http.html_title: "VC Map"` |
| crt.sh | `%.virtualcitymap.de` |

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

**Confirm:** GET the KEOS viewer or `/Netgis7` title page. Optional WMS: `wms.ashx` GetCapabilities. Do not confuse with Sampaş `/KentrehberiApp/` or GiSoftGis Angular city guides. Do **not** set `netgisserver` on Danish `/NetGISRuntime/` viewers (`netgisruntime`).

| Tool | Query |
|------|-------|
| Google | `intitle:"NetGIS Server 7" OR inurl:/Netgis7 OR inurl:/keos/` |
| Censys | `web.endpoints.http.html_title: "NetGIS Server"` |

## NetGIS Runtime (`netgisruntime`) {#netgisruntime}

WSP Danmark municipal WebGIS. Product: [WSP Informatik / NetGIS](https://www.wsp.com/da-dk/hubs/informatik). Distinct from Turkish Netcad NetGIS Server (`netgisserver`) and from German `netgis.de` MapServer clients.

**Signals:** path `/NetGISRuntime/basis/index.jsp`; title `NetGIS - © WSP Danmark`; scripts `netgis_logo2.svg`, `../js/jquery-1.10.2.js`; query params `custid=` or `alias=`. Hosts are typically `netgis.{kommune}.dk`, `gis.{kommune}.dk`, or `webgis.{kommune}.dk`.

**Confirm:** GET the viewer with the municipality's `custid` or `alias` (bare `/NetGISRuntime/basis/index.jsp` may 500). One record per municipal viewer. Keep an existing `arcgisserver` REST directory on another host in the same kommune as a separate catalog. Do **not** set `netgisserver`.

| Tool | Query |
|------|-------|
| Google | `inurl:/NetGISRuntime/basis/index.jsp site:.dk` |
| Google | `"NetGIS - © WSP Danmark" OR "NetGISRuntime" kommune` |
| Censys | `web.endpoints.http.html_title: "NetGIS"` |

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

## ALANDIS+ (`alandis`) {#alandis}

Asia Air Survey hosted public WebGIS (ALANDIS⁺ 公開型GIS) for Japanese prefectures and municipalities. Vendor: [ajiko.co.jp](https://www.ajiko.co.jp/products/detail/99/). Tenants commonly live under `webgis.alandis.jp/{tenant}/`. A few public forest/planning GIS use a custom host that still loads `/alandis.jp/` assets. Distinct from staff-only ALANDIS NEO / LGWAN GIS.

**Signals:** hostname `webgis.alandis.jp`; path `/alandis.jp/` or `/alandis/portal/`; `autologin_jswebgis`; tenant slug often ends with a prefecture number (`chiba12`, `suwa20`).

**Confirm:** GET the public portal (`/{tenant}/portal/` or `/webgis/`). One record per public tenant — `add-single` builds `id` from hostname only, so write YAML with the tenant slug in `id` (pattern `webgisalandisjp{tenant}`). Skip 401/403 and login-only staff GIS. Do not brute-force tenant slugs.

| Tool | Query |
|------|-------|
| Google | `site:webgis.alandis.jp 地図` |
| Google | `"webgis.alandis.jp" (公開型GIS OR 地図情報)` |
| Censys | `web.names: "webgis.alandis.jp"` |
| crt.sh | `alandis.jp` |

## SonicWeb (`sonicweb`) {#sonicweb}

Kokusai Kogyo hosted public WebGIS (SonicWeb-Cloud) for Japanese prefectures and municipalities. Vendor: [kkc.co.jp](https://www.kkc.co.jp/service/item/200/). Tenants live under `www.sonicweb-asp.jp/{slug}/`. Distinct from internal SonicWeb-i / SonicWeb-EXT.

**Signals:** hostname `www.sonicweb-asp.jp`; `sonicweb.js`; title 地図情報サービス / SonicWeb; footer Kokusai Kogyo.

**Confirm:** GET the tenant home (`/{slug}/`). One record per public path tenant — `add-single` builds `id` from hostname only, so write YAML with the path slug in `id` (pattern `wwwsonicwebaspjp{slug}`). Skip login-only SonicWeb-i.

| Tool | Query |
|------|-------|
| Google | `site:www.sonicweb-asp.jp 地図` |
| Google | `"sonicweb-asp.jp" (地図情報 OR GIS)` |
| Censys | `web.names: "www.sonicweb-asp.jp"` |
| crt.sh | `sonicweb-asp.jp` |

## GeDA-Public (`geogeo`) {#geogeo}

Nakano AI System public WebGIS (住民公開GIS「GeDA-Public」), hosted as Geogeo.jp. Vendor: [nais21.co.jp](https://www.nais21.co.jp/municipality/gis/opengis/). Tenants are `{city}.geogeo.jp` or `{city}.e-map.geogeo.jp`.

**Signals:** hostname `*.geogeo.jp`; branding eマップ / Geogeo; assets under `/assets/img/top/` and `mbmaps_dgn`.

**Confirm:** GET the tenant home. One record per municipality tenant. Skip internal GeDA (staff GIS).

| Tool | Query |
|------|-------|
| Google | `site:geogeo.jp (eマップ OR 地図)` |
| Google | `"geogeo.jp" (公開型 OR GIS)` |
| Censys | `web.names: "geogeo.jp"` |
| crt.sh | `%.geogeo.jp` |

## Geolonia スマートマップ (`geoloniagis`) {#geoloniagis}

Geolonia public WebGIS (公開型GIS「スマートマップ」), Digital Agency model-spec. Vendor: [geolonia.com/smartmap](https://www.geolonia.com/smartmap/). Multi-tenant brands include とっとりジオマップ (`{org}.tottori-geomap.jp`) and 香川県 公開型GIS -BRIDGES- (`map.pref.kagawa.lg.jp`). **Do not** set `software.id: smartmap` — that is the Kazakhstan `{district}.smartmap.kz` product.

**Signals:** Next.js `/_next/static/chunks/`; とっとりジオマップ / BRIDGES branding; Geolonia vector basemaps; hub list at `tottori-geomap.jp`.

**Confirm:** GET the public tenant map UI (not the Tottori hub marketing page alone). One record per public tenant. Skip considering/unpublished municipalities on the hub map.

| Tool | Query |
|------|-------|
| Google | `site:tottori-geomap.jp` |
| Google | `"とっとりジオマップ" OR "公開型GIS -BRIDGES-" OR "Geolonia" スマートマップ (GIS OR 地図) site:.jp` |
| Censys | `web.names: "tottori-geomap.jp"` |
| crt.sh | `%.tottori-geomap.jp` |

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

**False positives:** hostnames containing `mapgis` that are actually ArcGIS Server (`/arcgis/rest/services`, e.g. some South Asian `mapgis.*` sites). IGS 2.0 REST resembles ArcGIS REST — still `mapgisigserver` when the path is `/igs/rest/`, not `/arcgis/rest/`. Do not also register a second ArcGIS Server record on the same IGServer host. Colombian `/mapgis/mapa.jsp` or `/mapgis9/mapa.jsp` with footer HyG Consultores is **`hygmapgis`**, not IGServer.

| Tool | Query |
|------|-------|
| Google | `"MapGIS IGServer" OR inurl:/igs/rest/mrcs/docs -site:mapgis.com -site:github.com` |
| Google | `inurl:/igs/rest/services "MapGIS"` |
| Censys | `web.endpoints.http.body: "/igs/rest/mrcs"` |
| FOFA | `body="/igs/rest/" && title="MapGIS"` |

## HyG Mapgis (`hygmapgis`) {#hygmapgis}

H&G Consultores Suite MapGIS municipal/regional viewer (Colombia). Vendor: [hyg.com.co](https://hyg.com.co). Distinct from Zondy Cyber MapGIS IGServer (`mapgisigserver`).

**Signals:** path `/mapgis/mapa.jsp?aplicacion=` or `/mapgis9/mapa.jsp?aplicacion=`; footer “Desarrollado por: HyG Consultores S.A.S”; ArcGIS Server/Java backend.

**Confirm:** GET the public `mapa.jsp` viewer and match the HyG footer. One record per public application on a host. ArcGIS REST on the same Mapgis host stays with this viewer — do not add `arcgisserver`. Do **not** add Mapgis as a second catalog on a host that already has GeoNetwork as the public product (e.g. Medellín `www.medellin.gov.co/giscatalogacion`). Skip Zondy `/igs/rest/`, Bangladesh `mapgis.lged.gov.bd`, and Macau `webmapgis.gov.mo`.

| Tool | Query |
|------|-------|
| Google | `"Desarrollado por: HyG Consultores" (mapgis OR mapa.jsp) site:.gov.co` |
| Google | `inurl:/mapgis/mapa.jsp OR inurl:/mapgis9/mapa.jsp aplicacion site:.gov.co -site:mapgis.com` |
| Censys | `web.endpoints.http.body: "HyG Consultores" and web.endpoints.http.body: "mapa.jsp"` |

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

## dmCity (`dmcity`) {#dmcity}

Esri Finland municipal digital-city SaaS. Product: [esri.fi/tuotteet/dmcity](https://www.esri.fi/fi-fi/tuotteet/dmcity/intro). Public map tenants wrap Experience Builder. Distinct from generic Experience Builder (`experiencebuilder`) and from `{city}.dmcity.fi/server` REST (`arcgisserver`).

**Signals:** hostname `web.dmcity.fi`; path `/{city}/public/`; title `dmCity Web App`; `jimu-core/init.js`.

**Confirm:** GET the tenant URL and match the dmCity title. One record per city path. Skip the Esri Finland marketing pages. Do **not** set `software.id: experiencebuilder` on these tenants.

| Tool | Query |
|------|-------|
| Google | `site:web.dmcity.fi/public` |
| Google | `"dmCity Web App" OR "web.dmcity.fi" karttapalvelu site:.fi` |
| Censys | `web.names: "web.dmcity.fi"` |
| crt.sh | `web.dmcity.fi` |

## InfoGIS (`infogis`) {#infogis}

Infokartta Oy municipal map SaaS. Vendor: [infokartta.fi/palvelut](https://www.infokartta.fi/palvelut/). Distinct from Sitowise Louhi (`louhi`) and Trimble Locus IMS (`trimblelocus`).

**Signals:** hostname `www.infogis.fi/{municipality}/`; title `InfoGIS …`; scripts `/codebase-infogis/`; OpenLayers; meta author `Infokartta Oy`.

**Confirm:** GET the municipality path (not the Infokartta marketing site). One record per path tenant. A city may also have a Louhi viewer on another host — register both when they are distinct public products.

| Tool | Query |
|------|-------|
| Google | `site:infogis.fi` |
| Google | `"InfoGIS" Infokartta karttapalvelu site:.fi` |
| Censys | `web.names: "infogis.fi"` |
| crt.sh | `infogis.fi` |

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

## Origo (`origo`) {#origo}

Open-source OpenLayers web GIS from Origosamverkan. Product: [origomap.se](https://origomap.se/). Source: [origo-map/origo](https://github.com/origo-map/origo). Docs: [origo-map.github.io/origo-documentation](https://origo-map.github.io/origo-documentation/latest/). Distinct from Hajk (`hajk`), myCarta (`mycarta`), MapGuide Fusion (`mapguide`), and GeoServer (`geoserver`) catalogs on the same host.

**Signals:** script `origo.min.js`, `origo.js`, or `/origo2client/dist/origo.min.js`; `Origo(` initializer; Origosamverkan / origomap.se credits. Hosts are typically `karta.{kommun}.se`, `karta-ext.{kommun}.se/{kartan}/`, or `kartor.{kommun}.se/{kartan}/`.

**Confirm:** GET the public map UI (not `/geoserver`). One record per municipality viewer, not per themed map path on a gallery host (Sundsvall `karta.sundsvall.se/{map}/` stays one gallery record). Skip login-only internal Origo. Do **not** set `origo` from `appConfig.json` Hajk or from MapGuide `/mapguide/fusion/`.

| Tool | Query |
|------|-------|
| Google | `"origo.min.js" OR "origo.js" karta OR kartan site:.se` |
| Google | `"Origosamverkan" OR origomap webbkarta` |
| Censys | `web.endpoints.http.body: "origo.min.js"` |

## myCarta (`mycarta`) {#mycarta}

Aveki municipal web GIS (myCarta WebMap). Product: [Aveki Webb & App](https://www.aveki.se/Produkter/Geografisk_informationsplattform/WebbApp.aspx). Distinct from Hajk (`hajk`) and Origo (`origo`) on other Swedish `karta.*` hosts.

**Signals:** HTML title `myCarta WebMap` or `myCarta - WebMap`; meta description “myCarta WebMap, a client map application from Aveki AB”; path `/webmap/` or `/mycartawebmap/`; older clients load `js/emap.js` / `js/config.js` / `js/vendor.js` with `myCartaServerURL`; some hosts also serve `/myCartaServer/`. Hosts are typically `karta.{kommun}.se`, `{kommun}karta.{kommun}.se`, or `maps.{kommun}.se`.

**Confirm:** GET the public viewer and match the title or Aveki meta tag. One record per municipality viewer, not per `#m=` map. Skip login-only myCarta GO and the Aveki marketing site. Do **not** set `mycarta` from a Swedish `karta.*` host that is Hajk (`appConfig.json`) or Origo (`origo.min.js`).

| Tool | Query |
|------|-------|
| Google | `intitle:"myCarta WebMap" OR intitle:"myCarta - WebMap" site:.se` |
| Google | `inurl:mycartawebmap OR inurl:/webmap/ myCarta site:.se` |
| Censys | `web.endpoints.http.html_title: "myCarta WebMap"` |

## ISY Map (`isymap`) {#isymap}

Norconsult Digital municipal web GIS (ISY Map, ISY Map Server, GeoInnsyn). Product: [norconsult.digital/produkter/isy-map](https://norconsult.digital/produkter/isy-map/). Distinct from Avinet Adaptive (`avinet`) and from ArcGIS Hub Nordlandsatlas.

**Signals:** title ISYMap or ISY Map Server; path `/geoinnsyn/` or `/webkart/`; host `*.isy.no`; WinMap.ico on Map Server.

**Confirm:** GET the public viewer. One record per municipality or inter-municipal application, not per map project query string. Skip staff-only WinMap.

| Tool | Query |
|------|-------|
| Google | `"ISY Map" OR ISYMap OR GeoInnsyn (kart OR kommune) site:.no` |
| Google | `inurl:/geoinnsyn/ OR inurl:/webkart/ ISY` |
| Censys | `web.names: "isy.no"` |
| crt.sh | `%.isy.no` |

## Avinet Adaptive (`avinet`) {#avinet}

Avinet Adaptive / Webatlas thematic map platform. Vendor: [avinet.no](https://www.avinet.no/). Distinct from ISY Map (`isymap`).

**Signals:** ExtJS 4.2.2 plus OpenLayers 2.13.1; scripts from `a3.avinet.no`; HTML “adaptive”; WMS/WFS `wms.ashx` / `wfs.ashx`. Norwegian county “atlas” and temakart sites.

**Confirm:** GET the atlas home and match ExtJS/OpenLayers Adaptive. One record per public atlas. Do **not** set `avinet` on nordlandsatlas.nfk.no (that is `arcgishub`).

| Tool | Query |
|------|-------|
| Google | `"Developed by Avinet" OR a3.avinet.no (atlas OR temakart) site:.no` |
| Google | `inurl:wms.ashx fylkesatlas OR nordatlas` |
| Censys | `web.names: "avinet.no"` |

## MAP+ (`mapplus`) {#mapplus}

TYDAC AG WebGIS (sold in Germany as GeoAS Web). Product: [tydac.ch/en/mapplus](https://www.tydac.ch/en/mapplus/). Distinct from GeoMapFish (`geomapfish`) and from mf-geoadmin3 (`mfgeoadmin3`).

**Signals:** path `/mapplus/` or `/mapplus-lib/`; tydac in HTML or script hosts; OpenLayers city-map UI (Chur, St. Gallen, Biel, geoJura bernois).

**Confirm:** GET the public Stadtplan / map UI and match `mapplus-lib` or tydac. One record per municipality or regional conference viewer. Do **not** set `mapplus` from a Swiss `map.` hostname alone (Winterthur, Uri, Schaffhausen, and map.geo.admin.ch are other stacks). Bern `map.bern.ch/arcgis/rest/services` stays `arcgisserver`.

| Tool | Query |
|------|-------|
| Google | `"mapplus-lib" OR inurl:/mapplus/ (stadtplan OR GIS) site:.ch` |
| Google | `"MAP+" OR tydac (WebGIS OR Stadtplan) site:.ch` |
| Censys | `web.endpoints.http.body: "mapplus-lib"` |

## EnviMAP (`envimap`) {#envimap}

Envirosense Hungary municipal zoning-plan GIS (GeoForte viewer also hosted on intermap.hu). Site: [envimap.hu](https://envimap.hu/). Distinct from Autodesk MapGuide and from old MapFish.

**Signals:** host `*.envimap.hu`; title EnviMAP; path `/hu/Admin/GeoForte/GeoEdit` on envimap.hu or intermap.hu.

**Confirm:** GET the public zoning viewer. One record per municipality tenant. Do **not** set `envimap` from a Hungarian `/mapguide/` (`mapguide`) or ExtJS MapFish terinfo site.

| Tool | Query |
|------|-------|
| Google | `site:envimap.hu (szabterv OR GeoForte OR HÉSZ)` |
| Google | `inurl:/Admin/GeoForte/GeoEdit` |
| Censys | `web.names: "envimap.hu"` |
| crt.sh | `%.envimap.hu` |

## PISO (`piso`) {#piso}

Realis municipal GIS for Slovenian občine. Hub: [geoprostor.net](https://www.geoprostor.net). Distinct from Kaliopa iObčina (`iobcina`).

**Signals:** host `geoprostor.net` or `piso.si`; title PISO / Prostorski informacijski sistem občin; path `/PisoPortal/`.

**Confirm:** GET the public hub. One registry record for the national hub (municipality selector), not one row per občina unless that municipality publishes a separate public catalog UI.

| Tool | Query |
|------|-------|
| Google | `"PISO" (občin OR geoprostor) site:.si` |
| Google | `site:geoprostor.net PisoPortal` |
| Censys | `web.names: "geoprostor.net"` |

## GDi Visios (`gdivisios`) {#gdivisios}

GDi Ensemble (formerly LOCALIS) Web GIS viewer. Product: [gdi.net Ensemble Smart Portal](https://gdi.net/ensemble/ensemble-smart-portal/). Distinct from ArcGIS Hub/Server on other `gdi.net` hosts.

**Signals:** path `/visios/` or `/Visios/`; HTML title `GDi Visios`; scripts `VisiosAPI/gdi_js`; hosts `ensmartportal.gdi.net` or `localismarket.gdi.net`.

**Confirm:** GET the public viewer (not a CMS landing page that only mentions GDi). One record per municipality or county application. Do **not** set `gdivisios` from a GDi marketing page or from `arcgis-azure.gdi.net` REST. Skip GDi marketplace demo tenants unless that URL is the official public catalog.

| Tool | Query |
|------|-------|
| Google | `"GDi Visios" OR inurl:/visios/ (geoportal OR preglednik) site:.hr` |
| Google | `inurl:/visios/ site:gdi.net` |
| Censys | `web.endpoints.http.body: "GDi Visios"` |

## MapGuide (`mapguide`) {#mapguide}

Autodesk MapGuide Open Source / MapGuide Enterprise. Hungarian CityScape E-GOV city viewers wrap MapGuide. Distinct from EnviMAP (`envimap`) and from old ExtJS MapFish terinfo sites.

**Signals:** path `/mapguide/` or `/mapguide2010/`; `mapviewerphp/ajaxviewer.php`; Fusion `fusionSF.js`; CityScape E-GOV / Arkance Twigis branding.

**Confirm:** GET the public `internet.php` or MapGuide viewer. Fusion `/mapguide/fusion/` clients (for example Umeåkartan) are `mapguide`, not `origo`. One record per municipality. Do **not** set `mapguide` from a Hungarian `/Admin/GeoForte/` EnviMAP tenant. Do **not** set `mapguide` on Indixio SIGim Web (`sigimweb`).

| Tool | Query |
|------|-------|
| Google | `inurl:/mapguide/ internet.php site:.hu` |
| Google | `"CityScape E-GOV" OR mapviewerphp MapGuide` |
| Censys | `web.endpoints.http.body: "mapviewerphp/ajaxviewer.php"` |

## SIGimWeb (`sigimweb`) {#sigimweb}

Indixio SIGim Web municipal GIS for Quebec MRCs and cities. Product: [indixio.com/fr/sigim](https://indixio.com/fr/sigim/). Distinct from generic MapGuide (`mapguide`), GOnet (`goazimut.com`), and JP Cadrin CIF assessment viewers.

**Signals:** HTML title `SIGimWeb`; path `/sigimweb/` or `/sigim/`; ExtJS; scripts `/gomap_web/`; municipality picker; older tenants may load `gplusload.ashx`.

**Confirm:** GET the public viewer (not the Indixio marketing site). One record per public MRC or city tenant. Do **not** add a second catalog for each municipality in the picker. Do **not** set `sigimweb` from a GOnet URL or from `jpcadrin.ca/CIF/`. Skip intranet `/sigimweb/intranet.htm` (login). MRC des Laurentides migrated off SIGimWeb to JP Cadrin CIF.

| Tool | Query |
|------|-------|
| Google | `inurl:/sigimweb/ OR intitle:SIGimWeb site:.qc.ca` |
| Google | `"SIGimWeb" OR "SIGim Web" (MRC OR municipalité) cartographie` |
| Censys | `web.endpoints.http.html_title: "SIGimWeb"` |

## SeaSketch (`seasketch`) {#seasketch}

UCSB/NCEAS marine spatial planning SaaS. Product: [seasketch.org](https://www.seasketch.org/). Distinct from ArcGIS REST on `data.seasketch.org` (`arcgisserver`).

**Signals:** host `www.seasketch.org`; path `/{project}/app`; HTML title SeaSketch.

**Confirm:** GET the project `/app` URL (overlay layers public without sign-in counts). One record per public project app, not the marketing homepage. Do **not** set `seasketch` from `data.seasketch.org/arcgis/rest/services`.

| Tool | Query |
|------|-------|
| Google | `site:seasketch.org/app` |
| Google | `"SeaSketch" "marine spatial" OR MSP` |
| Censys | `web.names: "seasketch.org"` |

## XY Maps (`xymaps`) {#xymaps}

Eckersall municipal GIS (XY • MAPS). Product: [xymaps.com](https://www.xymaps.com/) / [Eckersall XY Maps](https://www.eckersall.com/xy-maps/). Distinct from Geocortex and ArcGIS viewers Eckersall also builds for the same cities.

**Signals:** host `maps.xymaps.com` or `www.xymaps.com` with path `/{city}`; **or** city host path `/xymaps/Map`; HTML title City Maps powered by XY MAPS or Welcome to XY MAPS; `/Content/themes/themesAll/xymaps.css`.

**Confirm:** GET the public tenant map (parcel search / layer list without sign-in counts). One record per public city tenant, not the marketing homepage. `www.xymaps.com/{city}` is the same SaaS as `maps.xymaps.com/{city}` — do not add both. Do **not** set `xymaps` from an Eckersall Geocortex/ArcGIS URL, from `/Register` login, or from a private floorplan directory.

| Tool | Query |
|------|-------|
| Google | `intitle:"powered by XY" MAPS site:maps.xymaps.com` |
| Google | `inurl:/xymaps/Map "XY" GIS` |
| Censys | `web.names: "maps.xymaps.com"` |

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

## IntraMaps Public (`intramaps`) {#intramaps}

TechnologyOne Spatial municipal web GIS (IntraMaps Public). Product: [TechnologyOne Spatial](https://www.technology1.com/products/spatial). Used by Australian and New Zealand councils. Distinct from ArcGIS Hub / ArcGIS Server on the same council and from TechnologyOne eProperty.

**Signals:** HTML title `IntraMaps`; `ApplicationEngine/Frontend/images/poweredByLogo.png`; `ApplicationEngine/API/javascripts/spatial.min.js`; query `project=Public` or `project=*Public`; on-prem paths `/intramaps90/default.htm`, `/IntraMaps80/`, `/Public90/`, `/Public80/`; cloud tenants `{council}.spatial.t1cloud.com/spatial/intramaps/` with `configId=`.

**Confirm:** GET the public IntraMaps URL and match title IntraMaps plus ApplicationEngine assets. One record per public `project=` tenant (typically Public / *Public), not per module (Property, Planning, Aerial). Skip login-only staff IntraMaps and eProperty map pages.

| Tool | Query |
|------|-------|
| Google | `"IntraMaps" (council OR shire) (maps OR GIS) site:.gov.au` |
| Google | `inurl:/intramaps90/ OR inurl:/IntraMaps80/ OR inurl:spatial.t1cloud.com` |
| Google | `"poweredByLogo" IntraMaps ApplicationEngine` |
| Censys | `web.names: "spatial.t1cloud.com"` |
| crt.sh | `%.spatial.t1cloud.com` |

## Spectrum Spatial Analyst (`spectrumspatial`) {#spectrumspatial}

Precisely Spectrum Spatial Analyst (formerly Pitney Bowes / MapInfo). Product: [Spectrum Spatial](https://www.precisely.com/product/precisely-spectrum-spatial/spectrum-spatial/). Used by UK and Australian councils and other public bodies as a public web GIS. Distinct from IntraMaps, ArcGIS Hub / ArcGIS Server, and Experience Builder on the same owner.

**Signals:** path `/connect/analyst/` or `/connect/analyst/mobile/`; HTML title `Spectrum Spatial` (sometimes a local brand such as Camden Maps or KOMPASS); Precisely favicon / `assets/images/precisely.png`; query `mapcfg=` for a named map project; Feature Service proxy `/connect/analyst/controller/connectProxy/rest/Spatial/FeatureService`.

**Confirm:** GET the public Analyst URL and match `/connect/analyst/` plus Spectrum Spatial or Precisely assets. One record per public tenant, not per `mapcfg=` project. Skip login-only staff Analyst, Spectrum Spatial Manager, and vendor demos (`analyst.spectrumspatial.com`, `spatialdemo.com`). Do **not** set `spectrumspatial` on Exponare `/exponare/` paths (`exponare`).

| Tool | Query |
|------|-------|
| Google | `inurl:/connect/analyst/mobile/` |
| Google | `"Spectrum Spatial Analyst" (council OR maps OR GIS)` |
| Google | `"Spectrum Spatial" inurl:/connect/analyst/` |
| Censys | `web.endpoints.http.body: "/connect/analyst/mobile"` |

## Exponare (`exponare`) {#exponare}

MapInfo / Pitney Bowes municipal web GIS, superseded by Precisely Spectrum Spatial Analyst. Remaining public tenants are Australian councils. Distinct from Spectrum Spatial Analyst (`/connect/analyst/`), IntraMaps, and ArcGIS Hub / REST on the same owner.

**Signals:** path `/exponare/RestPublicApplication.aspx`, `/exponare/PublicApplication.aspx`, `/exponare/Mobile.aspx`, or `/exponare/publicinvoker.aspx`; HTML title `Exponare Public` / `Willoughby Mapping` / `PublicInvoker`; ASP.NET Exponare assets; sometimes a council `mapping.aspx` wrapper that still loads `/exponare/`.

**Confirm:** GET the public Exponare URL and match `/exponare/` plus RestPublicApplication or PublicApplication. One record per public tenant, not a second copy of Public vs REST vs Mobile on the same host. Skip staff-only Exponare Enquiry and PDF “Exponare Enquiry Print” exports.

| Tool | Query |
|------|-------|
| Google | `inurl:/exponare/RestPublicApplication.aspx` |
| Google | `"Exponare Public" OR inurl:/exponare/publicinvoker site:.gov.au` |
| Censys | `web.endpoints.http.body: "/exponare/RestPublicApplication"` |

## LocalMaps (`localmaps`) {#localmaps}

Eagle Technology web GIS for New Zealand councils, on ArcGIS. Product: [LocalMaps](https://www.eagle.co.nz/gis-solutions/industry-solutions/localmaps). Public tenants show title **LocalMaps Gallery**.

**Signals:** path `/localmaps/gallery`; title `LocalMaps Gallery`; sometimes a branded `/{Council}Maps/Gallery/` path that still says LocalMaps in the HTML.

**Confirm:** GET the gallery and match LocalMaps. One record per council gallery, not per map in the gallery. Do **not** set `localmaps` on the ArcGIS REST `/arcgis/rest/services` directory on the same host (`arcgisserver`), on IntraMaps, Geocortex, Ruapehu InfoMap, or generic Experience Builder apps. Do not bulk-add guessed `{city}.govt.nz/localmaps/` hosts.

| Tool | Query |
|------|-------|
| Google | `inurl:/localmaps/gallery site:.govt.nz` |
| Google | `"LocalMaps Gallery" (council OR district) site:.nz` |
| Censys | `web.endpoints.http.html_title: "LocalMaps Gallery"` |

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

Fida Solutions / Urbanova municipal GIS. Tenants: `{city}.gisapp.ro` and city-owned hosts. Distinct from Kaliopa iObčina (`iobcina`) and from EQWC.

**Signals:** host `*.gisapp.ro`, **or** HTML title PortalPublic plus `logo_fida.png` / Fida branding on `gis.primaria*.ro` and similar city domains; urbanism certificate UI.

**Confirm:** GET the public city tenant and match PortalPublic / Fida. One record per municipality. ArcGIS REST on `webadaptor.gisapp.ro` stays `arcgisserver`. Do **not** set `gisapp` from a `gis.` hostname alone.

| Tool | Query |
|------|-------|
| Google | `site:gisapp.ro` |
| Google | `"PortalPublic" OR "logo_fida" (GIS OR urbanism) site:.ro` |
| Censys | `web.names: "gisapp.ro"` |
| crt.sh | `%.gisapp.ro` |

## PAGIS (`genegis`) {#genegis}

GeneGIS GI hosted municipal SIT / WebGIS. Product: [PAGIS](https://www.pagis.it/). Tenants: `{comune}.servizigis.it` and city-owned hosts. Distinct from Pulaski Area GIS (`www.pagis.org`, `arcgisserver`) and from Emilia-Romagna ArcGIS hosts named `servizigis.*`.

**Signals:** host `*.servizigis.it`, **or** “GeneGis Site Creator” / App PAGIS / schema.org `headline: PAGIS` on a city SIT (`Index.aspx`); ASP.NET `Home.aspx` cartographic portal.

**Confirm:** GET the public municipal tenant and match PAGIS / GeneGIS. One record per municipality. Skip `services.servizigis.it` and `pagis.it` marketing hubs. Do **not** set `genegis` from a `servizigis` hostname that is ArcGIS REST, or from US PAGIS.

| Tool | Query |
|------|-------|
| Google | `site:servizigis.it` |
| Google | `"GeneGis Site Creator" OR "App PAGIS" (SIT OR "portale cartografico") site:.it` |
| Censys | `web.names: "servizigis.it"` |
| crt.sh | `%.servizigis.it` |

## GisMaster (`gismaster`) {#gismaster}

Technical Design S.r.l. municipal Web GIS (GeoPortale GisMaster / GisMasterWeb). Product: [GisMaster](https://www.technicaldesign.it/gismaster/). Public tenants are Maggioli Sportello Unico Digitale pages with `IdCliente=`. Distinct from GISApp (`gisapp`), Masterportal (`masterportal`), and MapGIS IGServer (`mapgisigserver`).

**Signals:** host `geoportale.sportellounicodigitale.it`; path `/GisMaster/GisMaster/VisualDesc.aspx` or `VisualDescNR.aspx` with `IdCliente=`; title “GeoPortale GisMaster”; footer “Technical Design S.r.l.”; cadastre / P.R.G.C. layer lists and WMS/WFS links.

**Confirm:** GET the VisualDesc (or VisualDescNR) URL and match GisMaster plus cadastre/PRGC content. One record per `IdCliente` tenant, not `Default.aspx` as a second copy of the same comune, not the Maggioli hub home, and not cemetery `VisualCim.aspx` totems. Skip boilerplate pages with no layers.

| Tool | Query |
|------|-------|
| Google | `site:geoportale.sportellounicodigitale.it/GisMaster` |
| Google | `"GeoPortale GisMaster" "Technical Design" (Comune OR PRGC)` |
| Common Crawl CDX | `geoportale.sportellounicodigitale.it/GisMaster*` |
| Censys | `web.names: "geoportale.sportellounicodigitale.it"` |

## SmartMap (`smartmap`) {#smartmap}

Hosted Kazakh district investment geoportals. Tenants share `{district}.smartmap.kz`. Distinct from Geonomics (`geonomics`) akimat regional portals.

**Signals:** hostname `*.smartmap.kz`; Leaflet plus Google Maps; `stylse.css`; district/akimat investment layers.

**Confirm:** GET the tenant URL and match the Leaflet/Google Maps bundle. One record per district tenant. Skip unrelated SMARTMap finance products. Do **not** set `geonomics` from a `/map/` path on other KZ hosts — those Angular Leaflet `/map/` SPAs are `rgis`.

| Tool | Query |
|------|-------|
| Google | `site:smartmap.kz` |
| Google | `"smartmap.kz" (геопортал OR инвестиц)` |
| Censys | `web.names: "smartmap.kz"` |
| crt.sh | `%.smartmap.kz` |

## KAZGISA RGIS (`rgis`) {#rgis}

Regional Geographic Information System used by Kazakhstani akimats. Product page: [kazgisa.kz/rgis](https://kazgisa.kz/rgis/). Distinct from Geonomics (`geonomics`) Vue/Mapbox portals, SmartMap (`smartmap`) `{district}.smartmap.kz` tenants, and VKOMAP (`vkomap`) `/vkomap/` Leaflet+Esri viewers.

**Signals:** public path `{host}/map/`; Angular bundles `runtime.js`, `polyfills.js`, `vendor.js`, `main.js`; Leaflet 1.7.1 from unpkg; HTML titles `E-SQO`, `E-JAMBYL`, or `РГИС`.

**Confirm:** GET `{host}/map/` and match the Angular Leaflet SPA. One record per akimat or city geoportal. Do **not** set `rgis` from the older KAZGISA OpenLayers stack (`eatyrau.kz`). Do **not** set `geonomics`, `smartmap`, or `vkomap` from this `/map/` viewer.

| Tool | Query |
|------|-------|
| Google | `inurl:/map/ (E-SQO OR E-JAMBYL OR "РГИС") site:.kz` |
| Google | `"РГИС" геопортал (Шымкент OR Жамбыл OR СКО) Leaflet` |
| Censys | `web.endpoints.http.body: "/map/runtime.js"` |

## eKMap Cloud (`ekmap`) {#ekmap}

Vietnamese provincial planning GIS from eKGIS. Product: [ekgis.com.vn/ekmap-platform](https://ekgis.com.vn/ekmap-platform/). Docs: [docs.ekgis.vn](https://docs.ekgis.vn/). Distinct from Hanoi city planning `quyhoach.hanoi.gov.vn` (Next.js), Vinh Phuc OpenLayers 6 planning, and HCMC VLAB Leaflet planning.

**Signals:** `assets/ekmapboxgl/ekmap-mapboxgl.js` and `assets/ekmapboxgl/common.js`; Mapbox GL JS 1.13 plus `mapbox-gl-compare`; title often `eKMap Cloud` or provincial `Quy hoạch`. Hosts include `qhkhsdd.hanoi.gov.vn`, `quyhoach.haiphong.gov.vn`, `quyhoach.dienbien.gov.vn`, `quyhoach.langson.gov.vn`.

**Confirm:** GET the public planning viewer and match `ekmap-mapboxgl.js`. One record per province or city geoportal. Do **not** set `ekmap` from Mapbox GL alone, from `quyhoach.hanoi.gov.vn`, or from Vinh Phuc / HCMC planning maps.

| Tool | Query |
|------|-------|
| Google | `"eKMap Cloud" OR inurl:ekmap-mapboxgl (quy hoạch OR "Quy hoạch") site:.gov.vn` |
| Google | `"assets/ekmapboxgl/ekmap-mapboxgl.js"` |
| Censys | `web.endpoints.http.body: "ekmap-mapboxgl.js"` |

## VKOMAP (`vkomap`) {#vkomap}

Geoinfo (ТОО Геоинфо) municipal and regional geoportal. Vendor: [geoinfo.kz](https://geoinfo.kz/). Distinct from Geonomics (`geonomics`) Vue/Mapbox akimat portals and from SmartMap (`smartmap`) district tenants.

**Signals:** `/vkomap/` in CSS or HTML; Leaflet plus Esri; `/Public/GetKatoList` and `/Public/GetLayers` JSON; language path `/Kaz`. Hosts include `vkomap.kz`, `temirmap.kz`, `abaimap.kz`.

**Confirm:** GET the public map UI and match `/vkomap/` plus Leaflet/Esri. One record per akimat or city tenant. Do **not** set `vkomap` from a generic KZ `/map/` Angular viewer (`rgis`: e-sqo, geo-shym) or from Geonomics `map*.kz` hosts.

| Tool | Query |
|------|-------|
| Google | `"vkomap" (геопортал OR геопорталы) site:.kz` |
| Google | `inurl:/Public/GetKatoList site:.kz` |
| Censys | `web.endpoints.http.body: "/vkomap/"` |
| crt.sh | `vkomap.kz` |

## Visor Urbano (`visorurbano`) {#visorurbano}

Guadalajara municipal urban-management GIS, replicated in other Mexican cities with Bloomberg Philanthropies support. Product: [visorurbano.com](https://www.visorurbano.com). Distinct from unrelated Leaflet visors that reuse the “Visor Urbano” label.

**Signals:** hostname `visorurbano.{city}.gob.mx` or `{city}.visorurbano.com`; title Visor Urbano; `/logos/visor-urbano.svg` or Bloomberg philanthropies logo; Angular or Vite hashed app bundles.

**Confirm:** GET the public map/licence UI and match Visor Urbano branding. One record per municipality tenant. Skip `www.visorguadalupe.com` (Proaxis Leaflet, not this product). The Guadalajara origin `visorurbano.guadalajara.gob.mx` is the reference install when it responds.

| Tool | Query |
|------|-------|
| Google | `"Visor Urbano" (catastro OR "uso de suelo" OR licencias) site:.gob.mx` |
| Google | `site:visorurbano.com` |
| Censys | `web.names: "visorurbano.com"` |
| crt.sh | `visorurbano` |

## Dobles Visor de Mapas (`doblesvisor`) {#doblesvisor}

Packaged Costa Rican municipal Leaflet cadastral viewer (Leonardo Dobles). Distinct from ArcGIS Experience Builder visors on `experience.arcgis.com` and from MapStore / GeoNetwork on other CR hosts.

**Signals:** `/comun/jquery-ui-1.12.1/`; `/comun/js/leaflet.js`; `/comun/js/Leaflet.GoogleMutant.js`; title `Visor de Mapas`. Hosts include `visorcatastral.{muni}.go.cr`, `visor.munipalmares.go.cr`, `mapas.municoya.go.cr`, `catastro.sarapiqui.go.cr`, `corredores.go.cr`.

**Confirm:** GET the public visor and match the `/comun/` Leaflet + GoogleMutant stack. One record per municipality. Do **not** set `doblesvisor` from Santa Cruz `/gjs/` OpenLayers, Orotina `ol3gm.js`, Cañas `visorcartografico`, or CR ArcGIS Experience apps.

| Tool | Query |
|------|-------|
| Google | `inurl:/comun/js/leaflet.js (visor OR catastral) site:.go.cr` |
| Google | `"Visor de Mapas" (catastral OR cantón) site:.go.cr` |
| Censys | `web.endpoints.http.body: "Leaflet.GoogleMutant"` |

## GeoNube (`geonube`) {#geonube}

Cooperativa Cambalache hosted Leaflet/bootleaf map platform. Product: [cambalache.coop.ar/geonube](https://cambalache.coop.ar/geonube/). Distinct from Argentine municipal IDEs that do not load GeoNube assets.

**Signals:** hostname `geonube.com.ar` with path `/visor/{slug}`; scripts from `/bootleaf/` and `/leaflet/`; title often `Visor` or GeoNube. Custom domains (for example `nw.mercedes.gob.ar/geoportal`) count when they embed or link those visors.

**Confirm:** GET the visor slug (not `/visor/` with no slug, and not `/auth` alone). One record per municipality or organisation tenant, not one row per map inside the same tenant. Skip login-only private visors.

| Tool | Query |
|------|-------|
| Google | `site:geonube.com.ar/visor` |
| Google | `"GeoNube" (visor OR geoportal) (municipio OR municipalidad) site:.gob.ar` |
| Censys | `web.names: "geonube.com.ar"` |
| crt.sh | `geonube.com.ar` |

## Geopixel Cidades (`geopixel`) {#geopixel}

Brazilian municipal geointelligence SaaS. Vendor: [geopixel.com.br](https://geopixel.com.br/produtos/geopixel-cidades/). Distinct from ArcGIS Hub `geo.{city}.*.gov.br` portals.

**Signals:** hostname `{city}.geoportal.geopixel.com.br`; Next.js `/_next/static/` shell; `/api/pages` city config when the API is healthy. Older tenants: `{city}.geopixel.com.br/geopixelcidades-{city}/`.

**Confirm:** The geoportal hostname is a **DNS wildcard** that returns the same Next.js HTML for nonexistent cities. Add a municipality only when it is a documented Geopixel client or `{city}.geopixel.com.br/geopixelcidades-{city}/` is a live tenant. One record per city. Do not add arbitrary `*.geoportal.geopixel.com.br` hosts from HTTP 200 alone.

| Tool | Query |
|------|-------|
| Google | `site:geoportal.geopixel.com.br` |
| Google | `"Geopixel Cidades" (geoportal OR cadastro) site:.gov.br` |
| Censys | `web.names: "geoportal.geopixel.com.br"` |
| crt.sh | `geoportal.geopixel.com.br` |

## CTMGEO SigWEB (`ctmgeo`) {#ctmgeo}

Brazilian municipal cadastral WebGIS. Vendor: [ctmgeo.com.br](https://www.ctmgeo.com.br/empresa/software). Distinct from unrelated “SIGWeb” viewers on other hosts.

**Signals:** hostname `{city}.ctmgeo.com.br`; public map at `/mapa/`; title `SIGWeb`; meta description about cadastral lots.

**Confirm:** GET `/mapa/` and match SIGWeb branding. Nonexistent city hosts fail (not a DNS wildcard). One record per municipality. Do **not** set `ctmgeo` from a generic SIGWeb title on a `.gov.br` or other vendor host.

| Tool | Query |
|------|-------|
| Google | `site:ctmgeo.com.br/mapa/` |
| Google | `"SIGWeb" CTMGEO (geoportal OR cadastro) site:.gov.br` |
| Censys | `web.names: "ctmgeo.com.br"` |
| crt.sh | `%.ctmgeo.com.br` |

## GISPLAN (`gisplan`) {#gisplan}

T-MAPY municipal web GIS (Spinbox / T-WIST gallery) for Slovak and Czech cities. Vendor: [tmapy.sk](https://www.tmapy.sk/verejna-sprava/mesta) / [tmapy.cz/gis4u](https://www.tmapy.cz/gis4u). Slovak tenants usually live at `{city}.gisplan.sk`, or a city custom domain that still loads `tmapy.svg` / Spinbox and public `/mapa/` apps (`gis.zilina.sk`, `mapy.banskabystrica.sk`, `gisplan.kosice.sk`). Czech GIS4U tenants live at `{muni}.gis4u.cz`; T-WIST galleries also live at `{city}.tmapserver.cz` and on city hosts (Nymburk Spinbox, Děčín, Chomutov, Frýdek-Místek, Mladá Boleslav, Hradec Králové, Jablonec) that load `ost/filebox/ug_hm.php` with `t-wist_ren` / `tmapy.svg` icons. Distinct from Romanian GISApp (`gisapp`), Kaliopa iObčina (`iobcina`), Geoportál GEPRO (`gepro`), TopGis GisOnline (`gisonline`), Mapotip (`mapotip`), CORA GEO CG WebGIS (`cgwebgis`), T-MAPY mOBEC (`mobec`), Georeal (`georeal`), and Geodeticca WEB GIS (`geodeticca`). Do **not** set `gisplan` on T-MAPY MapProxy (`services7.tmapserver.cz/mapproxy` is `mapproxy`).

**Signals:** title `GISPLAN mesta …`, `GIS mesta …`, or GIS4U geoportál; scripts/logo `tmapy.svg` / `008_t-wist_ren_g.svg` / Spinbox footer `© T-MAPY`; `ost/filebox/ug_hm.php`; public app cards linking to `/mapa/`; optional `Prihlásiť sa` staff login on the same gallery.

**Confirm:** GET the public tenant home and match T-MAPY / Spinbox / T-WIST plus at least one public map app. One record per municipality. Prefer the city custom domain when it serves the same gallery as `{slug}.gisplan.sk`. Skip login-only shells with no public app list. Do **not** set `gisplan` from a `gis.` hostname that is ArcGIS Hub or Experience Builder (Pezinok, Nitra `gis.nitra.sk`), from Georeal `/portal/Georeal.*` kraj CMS (`georeal`), from Geodeticca WEB GIS (`gis.{city}.sk` titled Geodeticca WEB GIS), from CORA GEO CG WebGIS (`webgis.{city}.sk`, title `WebGIS v2, CG`), or from T-MAPY mOBEC (`mobec.sk/{slug}`).

| Tool | Query |
|------|-------|
| Google | `"GISPLAN mesta" OR "GIS mesta" site:gisplan.sk` |
| Google | `site:gis4u.cz geoportál OR "T-WIST"` |
| Google | `"T-MAPY" (geoportál OR "mapový portál") site:.sk OR site:.cz` |
| Censys | `web.names: "gisplan.sk"` |
| crt.sh | `%.gisplan.sk` |
| crt.sh | `%.gis4u.cz` |
| crt.sh | `%.tmapserver.cz` |

## mOBEC (`mobec`) {#mobec}

T-MAPY municipal map portal for smaller Slovak towns. Product: [mOBEC](https://www.tmapy.sk/mobec). Distinct from GISPLAN Spinbox galleries (`gisplan`).

**Signals:** host `mobec.sk/{slug}`; title `mOBEC`; script `var ido = {tenant}`; logo `/img/tmapyn.svg`; public map heading `Všeobecná mapa` / `mesto {City}`.

**Confirm:** GET `https://mobec.sk/{slug}` (optional `#base`) and match the SPA plus a public general map. One record per municipality. Skip the marketing home (`mobec.sk/` with no slug). Do **not** set `gisplan` from `mobec.sk` hosts. Do **not** bulk-add village tenants from a slug dictionary; confirm a public map. Staff login chrome on the same SPA is normal.

| Tool | Query |
|------|-------|
| Google | `site:mobec.sk "Všeobecná mapa" OR "mapový portál"` |
| Google | `"mobec.sk" (mesto OR obec) (GIS OR mapa)` |
| Censys | `web.names: "mobec.sk"` |
| crt.sh | `mobec.sk` |

## CG WebGIS (`cgwebgis`) {#cgwebgis}

CORA GEO municipal geographic web portal (WebGIS v2). Product: [CG WebGIS](https://www.corageo.sk/produkty/cg-webgis-geograficky-webovy-portal-samospravy/). Distinct from T-MAPY GISPLAN (`gisplan`).

**Signals:** host `webgis.{city}.sk` or a city host; title `WebGIS v2, CG` or `WebGIS {city}`; scripts `jquery-1.10.2.min.js`, `jquery.tabSlideOut`, `jquery.checkradios.js`.

**Confirm:** GET the public viewer and match the jQuery 1.10 / tabSlideOut client plus WebGIS title. One record per municipality. Do **not** set `cgwebgis` from GISPLAN Spinbox galleries, from Geodeticca WEB GIS (`geodeticca`), or from Nitra ArcGIS Hub (`gis.nitra.sk`).

| Tool | Query |
|------|-------|
| Google | `"WebGIS v2, CG" OR "CG WebGIS" site:.sk` |
| Google | `site:webgis.*.sk` |
| Censys | `web.endpoints.http.html_title: "WebGIS v2, CG"` |
| Censys | `web.names: "webgis.trnava.sk"` |

## Geodeticca WEB GIS (`geodeticca`) {#geodeticca}

GEODETICCA VISION municipal map client. Product: [geoinformatika](https://geodeticca.sk/index.php/produkty/geoinformatika/). Distinct from CORA GEO CG WebGIS (`cgwebgis`) and T-MAPY GISPLAN (`gisplan`).

**Signals:** title `Geodeticca WEB GIS`; host `gis.{city}.sk`; scripts `/js/config.js`, `/js/build/libs.js`, `/js/build/jquery-ext-min.js`.

**Confirm:** GET the public viewer and match the Geodeticca WEB GIS title plus `/js/build/libs.js`. One record per municipality. Do **not** set `geodeticca` from CG WebGIS (`webgis.{city}.sk`, title `WebGIS v2, CG`), GISPLAN Spinbox, or Michalovce `michalovce.web-gis.sk` (`app.bundle.js`).

| Tool | Query |
|------|-------|
| Google | `"Geodeticca WEB GIS" site:.sk` |
| Google | `site:gis.modra.sk OR site:gis.trebisov.sk OR site:gis.samorin.sk` |
| Censys | `web.endpoints.http.html_title: "Geodeticca WEB GIS"` |

## Geoportál GEPRO (`gepro`) {#gepro}

GEPRO municipal web GIS. Product: [Geoportál GEPRO](https://www.gepro.cz/produkty/geoportal/). Distinct from desktop MISYS and from T-MAPY GISPLAN (`gisplan`).

**Signals:** host `{city}.obce.gepro.cz`, `{city}.gepro.cz`, or `geoportal.gepro.cz/obce/{slug}`; title `Geoportál {City}`; scripts `/OUT/HTML/files/js/conf/start.min.js`, `/OUT/HTML/OL3/`, `gp.ol-ext`.

**Confirm:** GET the public viewer and match the `/OUT/HTML/` OpenLayers client. One record per municipality. Skip login-only intranet Geoportál GEPRO.

| Tool | Query |
|------|-------|
| Google | `site:obce.gepro.cz Geoportál` |
| Google | `"Geoportál" GEPRO (obec OR město) site:.cz` |
| Censys | `web.names: "gepro.cz"` |
| crt.sh | `%.obce.gepro.cz` |

## KOVGIS EVALD (`evald`) {#evald}

EOMAP / Geodata Arendus municipal web GIS for Estonian local governments. Product: [eomap.ee](https://eomap.ee/). Distinct from ArcGIS Enterprise `gis.{muni}.ee` portals, Geoveeb survey archives, and login-only GeoBaas.

**Signals:** path `evald.ee/{slug}/` (title `EVALD`); `service.eomap.ee/{slug}/` redirects there; footer Geodata Arendus / EOMAP; modules for detailplaneeringud, geoarhiiv, munitsipaalmaad.

**Confirm:** GET `https://evald.ee/{slug}/` and match the EVALD map UI (HTML title `EVALD`). One record per public tenant slug: municipalities plus nationwide `eesti` and association `elvl`. Do **not** add `service.eomap.ee` as a second copy, diacritic aliases (`lääneharjuvald`, `häädemeestevald_uus`), `evald2` / `evald2_*` session URLs, `tuljak` (TULJAK, not EVALD), `redmine`, or `evalddocs`. Do **not** set `geoserver` from EVALD HTML. Skip Ruhnu if the tenant returns `403`. Rae vald uses ArcGIS, not EVALD.

| Tool | Query |
|------|-------|
| Google | `site:evald.ee KOVGIS OR kaardirakendus` |
| Google | `"KOVGIS EVALD" (vald OR linn) kaardirakendus` |
| Censys | `web.names: "evald.ee"` |
| crt.sh | `evald.ee` |

## terGIS (`tergis`) {#tergis}

Latvian territorial-planning and public-engagement GIS (METRUM / TOPO DATI). Product: [tergis.lv](https://tergis.lv/). Distinct from generic QWC2 (`qwc2`) off `tergis.lv` and from the sibling pGIS product (`pgis.lv`).

**Signals:** host `{tenant}.tergis.lv`; HTML title `terGIS`, `TerGIS kartes`, or `Tergis.lv`; Angular SPA footer `terGIS v` plus `/api/v1/classifiers/layers`; some territorial-plan tenants use a QWC2 frontend (`/themes.json`, `QWC2App.js`) on the same domain.

**Confirm:** GET `https://{tenant}.tergis.lv/` and match the terGIS title or `/api/v1/classifiers/layers` JSON, or `/themes.json` on QWC2-frontend tenants. One record per public tenant subdomain. Do **not** add the marketing homepage `tergis.lv`. Do **not** set `qwc2` from a `*.tergis.lv` host (use `tergis`). Skip `401` (Ķekava) and `502` tenants until they recover.

| Tool | Query |
|------|-------|
| Google | `site:tergis.lv terGIS OR "teritorijas plānojums"` |
| Censys | `web.names: "tergis.lv"` |
| crt.sh | `%.tergis.lv` |

## Pozi (`pozi`) {#pozi}

Australian-owned council web GIS (Groundtruth / Pozi). Product: [pozi.com](https://pozi.com/). Distinct from IntraMaps Public (`intramaps`), Exponare (`exponare`), and Spectrum Spatial Analyst (`spectrumspatial`).

**Signals:** host `{council}.pozi.com`; HTML title `Pozi Web Map`; shared CloudFront SPA `assets/entry-app-*.js`.

**Confirm:** GET `https://{council}.pozi.com/` and match the Pozi Web Map title. One record per public council subdomain (`{name}-public` is the public tenant). Do **not** add the marketing homepage `pozi.com`. Do **not** set `intramaps` or `exponare` from a `pozi.com` host.

| Tool | Query |
|------|-------|
| Google | `site:pozi.com "Pozi Web Map"` |
| Google | `"Pozi" (council OR shire) map site:.gov.au` |
| Censys | `web.names: "pozi.com"` |
| crt.sh | `%.pozi.com` |

## JMap (`jmap`) {#jmap}

K2 Geospatial map-based integration platform (JMap Web and JMap NG). Product: [k2geospatial.com](https://k2geospatial.com/). Distinct from ArcGIS viewers.

**Signals:** path `/JMapWeb/` with `jmap.min.js` / title `JMapWeb`; JMap NG `/services/ng/` loading `jmapserver-ng`; hosted tenants on `*.jmaponline.net`.

**Confirm:** GET the public map and match JMap Web or JMap NG. One record per public project or tenant, not per layer. Do **not** set `jmap` from a hostname that merely contains `jmap` (Gyeongju `gjmap`, Rutgers NJMaps). Skip JMap Admin login.

| Tool | Query |
|------|-------|
| Google | `intitle:JMapWeb OR "JMap NG" (cadastre OR zonage)` |
| Google | `site:jmaponline.net` |
| Censys | `web.endpoints.http.body: "jmap.min.js"` |
| Censys | `web.names: "jmaponline.net"` |

## GIS Cloud (`giscloud`) {#giscloud}

Hosted web GIS. Product: [giscloud.com](https://www.giscloud.com/). Distinct from generic Leaflet viewers and from MuniSight (`web.munisight.com`).

**Signals:** host `{city}.giscloud.com`; scripts `assets.giscloud.com` (`compiled-smart.js`, `api.js`).

**Confirm:** GET `https://{city}.giscloud.com/` and match GIS Cloud assets. One record per public tenant subdomain. Do **not** add the marketing homepage. Skip Map Editor login.

| Tool | Query |
|------|-------|
| Google | `site:giscloud.com (GIS OR map) -www.giscloud.com` |
| Censys | `web.names: "giscloud.com"` |
| crt.sh | `%.giscloud.com` |

## MRF Web Map (`mrf`) {#mrf}

MRF Geosystems municipal GIS. Product: [MRF Web Map](https://www.mrf.com/product-details/MRF-Municipal-Solutions/MRF-Web-Map-Platform.html). Distinct from GIS Cloud (`giscloud`) and from MuniSight/Catalis login portals.

**Signals:** host `{county}.mrf.com` or a city host loading `js/lib/mrf/`; title `MRF Web Disclaimer`.

**Confirm:** GET the public map (guest / disclaimer) and match `js/lib/mrf/`. One record per public tenant. Do **not** set `mrf` from `web.munisight.com` Login.aspx (`munisight`). Skip the marketing homepage.

| Tool | Query |
|------|-------|
| Google | `"MRF Web Disclaimer" OR site:mrf.com Map` |
| Censys | `web.names: "mrf.com"` |

## MuniSight (`munisight`) {#munisight}

Catalis GIS WebMap (formerly MuniSight). Product: [catalisgov.com](https://catalisgov.com/public-works/geographic-information-system/). Distinct from MRF Web Map (`mrf`) and from generic GeoMedia WebMap (`geomediawebmap`).

**Signals:** host `web.munisight.com/{Tenant}`; `Login.aspx`; `App_Themes/Catalis`; CloudFront JS `3.9.x`.

**Confirm:** GET the tenant URL and match Catalis/MuniSight Login.aspx. One record per municipality tenant. Do **not** set `mrf` or `geomediawebmap` from this host. Skip the marketing homepage.

| Tool | Query |
|------|-------|
| Google | `site:web.munisight.com Login GIS` |
| crt.sh | `%.munisight.com` |

## GeoMedia SmartClient Public Maps (`publicmaps`) {#publicmaps}

GIS Quadrat hosted Hexagon GeoMedia SmartClient public viewer. Product: [gisquadrat.com/gis-software/public-maps](https://www.gisquadrat.com/gis-software/public-maps/). Distinct from GeoMedia WebMap Geospatial Portal (`geomediawebmap`) and from GIS Quadrat ERDAS APOLLO (`erdasapollo`) on `apollo.gisquadrat.com`.

**Signals:** `publicmaps.gisquadrat.com/BP/WEPM.aspx?site=GMSC&project={TOWN}`; title `GeoMedia SmartClient Public Maps`; `ig.publicmaps.application.min.js`; `/GMSC/PUBLIC/Configuration`.

**Confirm:** GET the WEPM.aspx tenant URL and match the Public Maps title plus `ig.publicmaps`. One record per municipal `project=` tenant. Do **not** set `geomediawebmap` or `erdasapollo` from this host. Skip the marketing homepage and the retired `gis-klagenfurt.at` WEPM host (replaced by Klagenfurt’s HxDR digital twin).

| Tool | Query |
|------|-------|
| Google | `"GeoMedia SmartClient Public Maps" OR inurl:WEPM.aspx site:publicmaps.gisquadrat.com` |
| Google | `"ig.publicmaps.application.min.js"` |
| Censys | `web.names: "publicmaps.gisquadrat.com"` |

## SIT WebGis (`sitwebgis`) {#sitwebgis}

SIT Servizi di Informazione Territoriale municipal GIS hosted at `webgis.sit-puglia.it`. Distinct from Regione Puglia GeoNetwork (`geonetwork` on `repertorio.sit.puglia.it`), Lizmap (`lizmap`), Spectrum Spatial Analyst (`spectrumspatial`), and GeneGIS PAGIS (`genegis`).

**Signals:** `webgis.sit-puglia.it/{comune}/`; title `WebGis {Town}` with `ng-app="WebApp"` and `core/lib/openlayers/js/ol.js`; or title `SIT-{TOWN}` / `SIT - {TOWN}` with Angular CLI bundles and `ol-attribution-hotfix.js`.

**Confirm:** GET the comune path and match the SIT WebGis title plus OpenLayers/Angular assets. One record per municipal tenant. Do **not** set `geonetwork` from this host. Skip the marketing homepage and stale slugs (`/mola`, `/potenza`) that 404.

| Tool | Query |
|------|-------|
| Google | `site:webgis.sit-puglia.it "WebGis" OR "SIT-"` |
| Google | `"ng-app=\"WebApp\"" ol.js site:webgis.sit-puglia.it` |
| Censys | `web.names: "webgis.sit-puglia.it"` |

## p.mapper (`pmapper`) {#pmapper}

Open-source PHP/MapScript frontend for MapServer. Project: [p.mapper](https://sourceforge.net/projects/pmapper/). Distinct from UMN MapServer as the public catalog (`mapserver`), Lizmap (`lizmap`), and Mapbender (`mapbender`).

**Signals:** path `/pmapper/` or `/pmapper-4.2.0/`; Calabria SETIN tenants `{city}.geo-portale.it`; HTML mentioning p.mapper.

**Confirm:** GET the public UI and match `/pmapper`. One record per municipality or SIT, not per layer. Do **not** set `mapserver` from a p.mapper UI. Do not add a second MapServer catalog on the same host.

| Tool | Query |
|------|-------|
| Google | `inurl:pmapper-4.2.0 OR inurl:/pmapper/ (geoportale OR WebGIS)` |
| Google | `site:geo-portale.it Geoportale` |
| Censys | `web.endpoints.http.body: "pmapper-4.2.0"` |
| crt.sh | `%.geo-portale.it` |

## CommunityView (`communityview`) {#communityview}

Digital Map Products (LightBox) municipal web GIS. Distinct from ArcGIS Instant Apps (`instantapps`).

**Signals:** path `/production/VECommunityView/cities/{city}/` on `maps.digitalmapcentral.com`; title `CommunityView`; “Powered By Digital Map Products”.

**Confirm:** GET the city index and match CommunityView. One record per city slug. Do not add the vendor homepage as a catalog.

| Tool | Query |
|------|-------|
| Google | `site:maps.digitalmapcentral.com VECommunityView` |
| Google | `"Powered By Digital Map Products" CommunityView` |
| Censys | `web.names: "digitalmapcentral.com"` |

## MS-GIS (`msgis`) {#msgis}

Lower Austria municipal GeoInformation viewer. Distinct from Masterportal (`masterportal`), touvia.MAPS (`touviamaps`), and VC Map (`vcmap`).

**Signals:** host `{city}.msgis.net`; HTML title `{City} GeoInformation`.

**Confirm:** GET `https://{city}.msgis.net/` and match the GeoInformation title. One record per municipality subdomain. Do not add the marketing homepage.

| Tool | Query |
|------|-------|
| Google | `site:msgis.net GeoInformation` |
| Censys | `web.names: "msgis.net"` |
| crt.sh | `%.msgis.net` |

## Weave (`weave`) {#weave}

Cohga municipal HTML5 web GIS used by Australian councils. Product: [cohga.com](https://www.cohga.com/solutions/council-information-management/). Distinct from IntraMaps Public (`intramaps`), Exponare (`exponare`), Pozi (`pozi`), and Spectrum Spatial Analyst (`spectrumspatial`).

**Signals:** HTML title `Weave Map`; webpack `app.*.js` client (often with `vendor-ol.*.js`). Hosted on the council domain, not a shared SaaS hostname.

**Confirm:** GET the public map and match title Weave Map. One record per council viewer. Do **not** set `weave` from GeneWeaver, “weaves together” copy, or IntraMaps/Pozi.

| Tool | Query |
|------|-------|
| Google | `intitle:"Weave Map" (council OR GIS) site:.gov.au` |
| Google | `"Weave Map" Cohga OR Geoplex` |

## OVIE (`ovie`) {#ovie}

INEGI Oficina Virtual de Información Económica municipal economic GIS. Distinct from Mapa Digital de México / MxSIG (`mxsig`) and from generic OpenLayers copies.

**Signals:** title OVIE or Oficina Virtual de Información Económica; scripts `js/libs/OpenLayers/OL.js`, Materialize, html2canvas, canvg, jsPdf.

**Confirm:** GET the public viewer and match the OpenLayers `/js/libs/` stack. One record per municipality or state OVIE. Do **not** set `ovie` from Mission Viejo `geoviewer.io` or hostnames that merely contain `ovie`. Do **not** set `ovie` on INEGI Gaia `/mdm6/` (`mxsig`).

| Tool | Query |
|------|-------|
| Google | `"OVIE" OR "Oficina Virtual de Información Económica" IMPLAN (visor OR mapa)` |
| Google | `intitle:OVIE OpenLayers site:.gob.mx` |

## SOFTPRO (`softpro`) {#softpro}

Ukrainian urban-planning cadastre GIS (SOFTPRO: Містобудівний кадастр). Product: [cadastre.com.ua](https://cadastre.com.ua/). Distinct from the state Urban Planning Cadastre (`kadastr.gov.ua`) and StateGeoCadastre (`map.land.gov.ua`).

**Signals:** host `{city}.cadastre.com.ua`; page text SOFTPRO; Tailwind `/assets/index-*.js` geoportal or older `/js/locale/ua.js` with `/assets/image/intro-icon.svg`.

**Confirm:** GET the public geoportal and match SOFTPRO in HTML. One record per community or oblast portal. Do **not** set `softpro` from `kadastr.gov.ua` or `map.land.gov.ua`.

| Tool | Query |
|------|-------|
| Google | `site:cadastre.com.ua` OR `"SOFTPRO" "містобудівний" геопортал` |
| Google | `"SOFTPRO·Містобудівний кадастр" OR "платформі SOFTPRO"` |

## MxSIG (`mxsig`) {#mxsig}

INEGI Mapa Digital de México V6 / MxSIG. Product: [inegi.org.mx/servicios/mxsig.html](https://www.inegi.org.mx/servicios/mxsig.html). Distinct from OVIE (`ovie`).

**Signals:** path `/mdm6/` or `/mxsig2/`; title `Mapa Digital de México`; scripts `js/frameworks/amplify/amplify.js`, `lz-string`, jquery 1.9.

**Confirm:** GET the viewer and match amplify.js + MDM title. One record per public MDM6/MxSIG map, not the indicators CMS on the same host. Do **not** set `mxsig` on OVIE.

| Tool | Query |
|------|-------|
| Google | `inurl:/mdm6/ OR inurl:/mxsig2/ "Mapa Digital"` |
| Google | `"MxSIG" OR "Mapa Digital de México V6" visor` |

## GisOnline (`gisonline`) {#gisonline}

TopGis municipal map application. Product: [gisonline.cz](https://www.gisonline.cz/). Distinct from T-MAPY GISPLAN (`gisplan`) and Geoportál GEPRO (`gepro`).

**Signals:** host `app.gisonline.cz/{city}`; title `{City} | Mapová aplikace GisOnline.cz`; script `/app-*.min.js`; copyright TopGis.

**Confirm:** GET `https://app.gisonline.cz/{city}` and match the GisOnline title (not the branded error page alone). One record per city slug. Skip the TopGis marketing site.

| Tool | Query |
|------|-------|
| Google | `site:app.gisonline.cz "Mapová aplikace GisOnline"` |
| Google | `"GisOnline.cz" (město OR obec) mapa` |
| Censys | `web.names: "gisonline.cz"` |
| crt.sh | `app.gisonline.cz` |

## K5 MapServer (`k5mapserver`) {#k5mapserver}

MK Consult municipal geoportal for Kompas 5. Product: [K5 MapServer](https://mkconsult.cz/k5-mapserver/). Distinct from UMN MapServer (`mapserver`) and from T-MAPY GISPLAN (`gisplan`).

**Signals:** host `{muni}.k5mapserver.cz`; title `GEOPORTÁL`; scripts `/core/Page.js`, `/core/constant.js`, `/core/util.js`; footer K5MapServer / MK Consult.

**Confirm:** GET the public tenant home and match `/core/Page.js`. One record per municipality subdomain. Nonexistent city hosts fail (not a DNS wildcard). Do **not** set `mapserver` from the k5mapserver hostname alone.

| Tool | Query |
|------|-------|
| Google | `site:k5mapserver.cz GEOPORTÁL` |
| Google | `"K5 MapServer" OR K5MapServer (obec OR město)` |
| Censys | `web.names: "k5mapserver.cz"` |
| crt.sh | `%.k5mapserver.cz` |

## Marushka (`marushka`) {#marushka}

GEOVAP map application server. Product: [Marushka](https://www.geovap.com/cs/marushka). Distinct from T-MAPY GISPLAN (`gisplan`), Geoportál GEPRO (`gepro`), and Georeal kraj CMS (`georeal`).

**Signals:** HTML title `Marushka - Mapový aplikační server`; script `js/zipped.js`; path `/marushka/` or `/marushka_ver/`; newer HTML clients load Blazor plus `js/marushka.js`.

**Confirm:** GET the public map UI and match Marushka in the title or `zipped.js` / `marushka.js`. One record per city installation, not per themed project. Skip GEOVAP marketing pages.

| Tool | Query |
|------|-------|
| Google | `intitle:"Marushka - Mapový aplikační server"` |
| Google | `inurl:marushka OR inurl:marushka_ver (geoportál OR GIS) site:.cz` |
| Censys | `web.endpoints.http.html_title: "Marushka - Mapový aplikační server"` |

## Georeal (`georeal`) {#georeal}

GEOREAL OrchardCore CMS for Czech kraj DTM and geoportal sites. Product: [georeal.cz GIS](https://www.georeal.cz/sluzby/gis). Distinct from T-MAPY GISPLAN (`gisplan`), Geoportál GEPRO (`gepro`), and GEOVAP Marushka (`marushka`).

**Signals:** path `/portal/`; script `/portal/Georeal.Cards/Apps/card-container.min.js`; optional `Georeal.UzemniPlanovani` and `IsDTMKraj*` theme.

**Confirm:** GET `{host}/portal/` and match `Georeal.Cards`. One record per public DTM or geoportal product (Plzeň has both). Do **not** set `georeal` from an older `/portal/Themes/Metro/` city CMS without `Georeal.Cards` (Kadaň), from Nuxt DTM shells (`portal.dtm-praha-sck.cz`), from JSF `dmvs-gateway` (`uap.olkraj.cz`), or from ArcGIS REST kraj maps (Vysočina). Do **not** set `gisplan` or `marushka` from `Georeal.Cards`.

| Tool | Query |
|------|-------|
| Google | `"Georeal.Cards" OR "IsDTMKraj" (geoportál OR DTM) site:.cz` |
| Google | `inurl:/portal/ (DTM OR geoportál) (kraj OR kraje) site:.cz` |
| Censys | `web.html: "Georeal.Cards"` |

## Mapotip (`mapotip`) {#mapotip}

Czech municipal web map portal (cadastre, DTM, pasports). Product: [mapotip.cz](https://www.mapotip.cz/). Distinct from T-MAPY GISPLAN (`gisplan`), Geoportál GEPRO (`gepro`), and TopGis GisOnline (`gisonline`).

**Signals:** host `portal.mapotip.cz/{municipality}`; HTML title `Mapotip`; script `/map/index-*.js`.

**Confirm:** GET the public tenant and match title Mapotip plus `/map/index-`. One record per municipality slug. Skip `portal.mapotip.cz/demo` and the marketing site.

| Tool | Query |
|------|-------|
| Google | `site:portal.mapotip.cz Mapotip` |
| Google | `"Mapotip" (obec OR město) (geoportál OR "mapový portál")` |
| Censys | `web.names: "mapotip.cz"` |
| crt.sh | `portal.mapotip.cz` |

## giscity (`giscity`) {#giscity}

ibb DV-Systems municipal GIS. Product: [giscity](https://www.ibbgdv.de/giscity/). Hosted public tenants live at `www.gisserver.de/{city}/`. Distinct from US `gis.cityof*` ArcGIS catalogs and from ArcGIS Hub (`arcgishub`).

**Signals:** host `www.gisserver.de/{city}/`; script `portal.js`; GIScity Service Hosting / ibb Grafische Datenverarbeitung footer; logo `giscity_small.png`.

**Confirm:** GET the public portal home and match portal.js plus ibb/GIScity credits. One record per city path. Do **not** set `giscity` from a hostname that merely contains `giscityof` (US/GR ArcGIS).

| Tool | Query |
|------|-------|
| Google | `site:gisserver.de GIScity OR giscity` |
| Google | `"GIScity Service Hosting" OR "giscity_small.png"` |
| Censys | `web.names: "gisserver.de"` |
| crt.sh | `gisserver.de` |

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
| `sonicweb` | see above | |
| `geogeo` | see above | |
| `geoloniagis` | see above | |
| `nolis` | see above | |
| `cardo` | see above | |
| `netgisserver` | see above | |
| `netgisruntime` | `/NetGISRuntime/basis/index.jsp` | `inurl:/NetGISRuntime/basis site:.dk` |
| `origo` | `origo.min.js` / `origo.js` / `Origo(` | `"origo.min.js" karta site:.se` |
| `sampaswebgis` | see above | |
| `gisoftgis` | see above | |
| `visorurbano` | see above | |
| `doblesvisor` | see above | |
| `geonube` | see above | |
| `geopixel` | see above | |
| `ctmgeo` | see above | |
| `dmcity` | `web.dmcity.fi/{city}/public/` | `site:web.dmcity.fi` |
| `infogis` | `www.infogis.fi/{muni}/` | `site:infogis.fi` |
| `experiencebuilder` | see [SDI](discovery-geoportals-sdi.md#experiencebuilder) | |
| `webappbuilder` | see [SDI](discovery-geoportals-sdi.md#webappbuilder) | |
| `instantapps` | see [SDI](discovery-geoportals-sdi.md#instantapps) | |
| `activemapgis` | see above | |
| `mapapps` | see above | |
| `belsisims` | `ims.*/Projects/*/Pages/KRH.aspx` | `KRH.aspx Belsis` |
| `orbismap` | ORBISMap Russian GIS | `"ORBISMap" геопортал` |
| `opengeoportal` | see above | |
| `geonomics` | Vue/Mapbox, geonomix.kz | `"Geonomics" OR geonomix геопортал` |
| `rgis` | KZ `{host}/map/` Angular Leaflet | `inurl:/map/ (E-SQO OR "РГИС") site:.kz` |
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
| `hygmapgis` | see above | |
| `trimblelocus` | Finnish `/IMS/` karttapalvelu | `inurl:/IMS/ karttapalvelu site:.fi` |
| `louhi` | Sitowise Louhi viewer | `"Louhi" karttapalvelu Sitowise` |
| `landfolio` | `portals.landfolio.com` cadastre maps | `site:portals.landfolio.com` |
| `hajk` | Hajk `appConfig.json` / `mapserviceBase` | `"Hajk - open source webGIS" site:.se` |
| `mycarta` | title myCarta WebMap / `/webmap/` / `/mycartawebmap/` | `intitle:"myCarta WebMap" site:.se` |
| `spatialsuite` | Sweco SpatialMap webkort | `"SpatialMap" webkort site:.dk` |
| `kortinfo` | NIRAS `drift.kortinfo.net/Map.aspx` | `site:drift.kortinfo.net Map.aspx` |
| `intramaps` | IntraMaps Public `project=` / t1cloud | `"IntraMaps" ApplicationEngine site:.gov.au` |
| `spectrumspatial` | `/connect/analyst/` Spectrum Spatial Analyst | `inurl:/connect/analyst/mobile/` |
| `exponare` | `/exponare/` RestPublicApplication | `inurl:/exponare/RestPublicApplication.aspx` |
| `localmaps` | `/localmaps/gallery` LocalMaps Gallery | `inurl:/localmaps/gallery site:.govt.nz` |
| `geusmap` | `/geusmap/?mapname=` | `inurl:geusmap mapname` |
| `gisapp` | see above | |
| `gisplan` | `{city}.gisplan.sk` / T-MAPY Spinbox | `"GISPLAN mesta" site:gisplan.sk` |
| `genegis` | `{comune}.servizigis.it` / GeneGis Site Creator | `site:servizigis.it` |
| `gismaster` | Maggioli `/GisMaster/` `IdCliente=` | `site:geoportale.sportellounicodigitale.it/GisMaster` |
| `smartmap` | `{district}.smartmap.kz` Leaflet | `site:smartmap.kz` |
| `vkomap` | `/vkomap/` Leaflet + Esri, Geoinfo | `"vkomap" геопортал site:.kz` |
| `isymap` | ISY Map / GeoInnsyn `/geoinnsyn/` | `"ISY Map" OR GeoInnsyn site:.no` |
| `avinet` | Adaptive ExtJS atlas, `a3.avinet.no` | `"Developed by Avinet" atlas site:.no` |
| `mapplus` | `/mapplus-lib/` TYDAC Stadtplan | `inurl:/mapplus/ OR mapplus-lib site:.ch` |
| `envimap` | `*.envimap.hu` / GeoForte | `site:envimap.hu GeoForte` |
| `piso` | geoprostor.net PisoPortal | `site:geoprostor.net PISO` |
| `gdivisios` | `/visios/` GDi Ensemble viewer | `"GDi Visios" OR inurl:/visios/` |
| `mapguide` | `/mapguide/` CityScape / ajaxviewer | `inurl:/mapguide/ internet.php` |
| `sigimweb` | `/sigimweb/` title SIGimWeb / `/gomap_web/` | `inurl:/sigimweb/ site:.qc.ca` |
| `seasketch` | `seasketch.org/{project}/app` | `site:seasketch.org/app` |
| `xymaps` | `maps.xymaps.com/{city}` / `/xymaps/Map` | `intitle:"powered by XY" MAPS` |
| `pozi` | `{council}.pozi.com` title Pozi Web Map | `site:pozi.com "Pozi Web Map"` |
| `jmap` | `/JMapWeb/` / JMap NG `jmapserver-ng` | `intitle:JMapWeb OR site:jmaponline.net` |
| `giscloud` | `{city}.giscloud.com` | `site:giscloud.com` |
| `mrf` | `{county}.mrf.com` / `js/lib/mrf/` | `"MRF Web Disclaimer"` |
| `munisight` | `web.munisight.com/{Tenant}` Login.aspx Catalis | `site:web.munisight.com Login` |
| `pmapper` | `/pmapper/` / `{city}.geo-portale.it` | `inurl:pmapper-4.2.0` |
| `communityview` | `VECommunityView/cities/{city}/` | `site:maps.digitalmapcentral.com VECommunityView` |
| `msgis` | `{city}.msgis.net` GeoInformation | `site:msgis.net GeoInformation` |
| `weave` | title Weave Map webpack `app.*.js` | `intitle:"Weave Map" site:.gov.au` |
| `ovie` | OVIE `/js/libs/OpenLayers/OL.js` Materialize | `"OVIE" IMPLAN OpenLayers site:.gob.mx` |
| `softpro` | `{city}.cadastre.com.ua` / SOFTPRO `/js/locale/ua.js` | `site:cadastre.com.ua` OR `"SOFTPRO" геопортал` |
| `mxsig` | `/mdm6/` `/mxsig2/` amplify.js | `inurl:/mdm6/ "Mapa Digital"` |
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

