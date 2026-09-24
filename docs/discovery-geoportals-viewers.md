# Discovering geoportal viewers

Regional and municipal map viewers (`catalog_type: Geoportal`). These are **viewers**: harvest the layer list, not PNG tiles ([harvest-viewers.md](harvest-viewers.md)). Overview: [discovery-geoportals.md](discovery-geoportals.md). SDI catalogs: [discovery-geoportals-sdi.md](discovery-geoportals-sdi.md). Internet-map queries: Censys, or [FOFA](discovery-search-tools.md#fofa) when Censys is unavailable (`host=` for SaaS tenants, `title=` / `body=` for fingerprints).

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
| FOFA | `host="www2.wagmap.jp"` |
| FOFA | `body="GeoAccessJS"` |
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
| FOFA | `domain="geoportal2.pl"` |
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
| FOFA | `domain="e-mapa.net"` |
| FOFA | `body="/application/system/pandora/"` |
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
| FOFA | `domain="map.is"` |
| crt.sh | `map.is` |

## Alta Vefsjá (`alta`) {#alta}

Alta ehf. OpenLayers municipal planning viewer. Tenants under `geo.alta.is/{tenant}/` load `altacode` vefsja assets.

**Signals:** `geo.alta.is` path that is **not** `/geoserver`; scripts from `storage.googleapis.com/altacode/js/vefsja/`; title Kortasjá.

**Confirm:** GET the viewer path. Keep the GeoServer root as a separate `geoserver` record.

| Tool | Query |
|------|-------|
| Google | `site:geo.alta.is kortasjá OR vefsjá` |
| Censys | `web.names: "geo.alta.is"` |
| FOFA | `host="geo.alta.is"` |

## Bulplan UNIMAP (`bulplan`) {#bulplan}

Bulgarian municipal integrated geoportal. Tenants at `{municipality}.bulplan.eu` (UNIMAP branding).

**Signals:** hostname `*.bulplan.eu`; title or chrome UNIMAP / Bulplan.

**Confirm:** GET the public map. One record per municipality. Skip dead Apache default pages.

| Tool | Query |
|------|-------|
| Google | `site:bulplan.eu` |
| Google | `"UNIMAP" OR Bulplan (геопортал OR geoportal) site:.bg` |
| Censys | `web.names: "bulplan.eu"` |
| FOFA | `domain="bulplan.eu"` |
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
| FOFA | `domain="tobel.bg"` |
| crt.sh | `%.tobel.bg` |

## geoportal.ch (`geoportalch`) {#geoportalch}

Hosted Swiss cantonal geoportal. Tenants share `www.geoportal.ch/{canton}` (ktzg, ktai, ktar, …).

**Signals:** hostname `www.geoportal.ch` with a canton path; title Geoportal.

**Confirm:** GET the canton path. Distinct from swisstopo **mf-geoadmin3** (`mfgeoadmin3`) and **web-mapviewer** (`webmapviewer`).

| Tool | Query |
|------|-------|
| Google | `site:geoportal.ch` |
| Google | `"geoportal.ch" (Kanton OR geoportal) site:.ch` |
| Censys | `web.names: "geoportal.ch"` |
| FOFA | `domain="geoportal.ch"` |
| crt.sh | `geoportal.ch` |

## web-mapviewer (`webmapviewer`) {#webmapviewer}

swisstopo Vue/OpenLayers successor to mf-geoadmin3. Repo: [geoadmin/web-mapviewer](https://github.com/geoadmin/web-mapviewer). `map.geo.admin.ch` ships `/v1.x.x/assets/index-*.js` (live v1.61.3 matched the GitHub release). Distinct from mf-geoadmin3 cantonal forks (`mfgeoadmin3`).

**Confirm:** GET the viewer HTML for versioned `/v1.` asset paths. Do **not** set `mfgeoadmin3` on map.geo.admin.ch.

[index.html](https://github.com/geoadmin/web-mapviewer/blob/develop/packages/mapviewer/index.html) titles the app `Maps of Switzerland - Swiss Confederation - map.geo.admin.ch` (2 hosts in September 2026, both `map.geo.admin.ch`). The shorter `Maps of Switzerland - Swiss Confederation` also matches an embedding site, so use the full title.

| Tool | Query |
|------|-------|
| Google | `"map.geo.admin.ch" OR "web-mapviewer" (swisstopo OR geoadmin)` |
| Censys | `web.endpoints.http.body: "Maps of Switzerland - Swiss Confederation - map.geo.admin.ch"` |
| FOFA | `body="Maps of Switzerland - Swiss Confederation - map.geo.admin.ch"` |
| Censys | `web.names: "map.geo.admin.ch"` |
| FOFA | `host="map.geo.admin.ch"` |

## GIS4Smart (`gis4smart`) {#gis4smart}

DOTSOFT municipal Web GIS (Y.Ge.P. / DotSpatial branding). Common in Greek municipalities.

**Signals:** title or body `GIS4Smart`; Y.Ge.P. / DotSpatial chrome.

**Confirm:** GET the public map UI and match GIS4Smart. Do not also register a bundled GeoServer on the same host. One municipality = one harvest scope.

| Tool | Query |
|------|-------|
| Google | `"GIS4Smart" geoportal` |
| Censys | `web.endpoints.http.body: "GIS4Smart"` |
| FOFA | `body="GIS4Smart"` |

## Evrymap (`evrymap`) {#evrymap}

Consortis Geospatial municipal map portal. SPA titled Evrymap; MapServer WMS/WFS behind the viewer. Common in Greek municipalities (sometimes on `*.open1.eu`).

**Signals:** HTML title “Evrymap”; `/mapserver/mapserv` GetCapabilities; Consortis branding.

**Confirm:** GET the public map UI and match Evrymap. Harvest WMS layers when GetCapabilities is XML. Do not also register the bundled MapServer as a second catalog on the same host.

| Tool | Query |
|------|-------|
| Google | `"Evrymap" (Δήμος OR geoportal OR MapServer) site:.gr` |
| Censys | `web.endpoints.http.html_title: "Evrymap"` |
| FOFA | `title="Evrymap"` |

## GeoMapFish (`geomapfish`) {#geomapfish}

Open-source WebGIS (c2cgeoportal + ngeo). Common in Swiss cantons and other European public geoportals. Site: [geomapfish.org](https://geomapfish.org). Distinct from TYDAC MAP+ (`mapplus`).

**Signals:** `ngeo` / `gmf-` CSS classes; `/themes` JSON; WMS/WMTS theme tree; `c2cgeoportal` in HTML or JS bundles.

**Confirm:** GET `/themes` (or the documented theme API) and a public map UI. One record per public geoportal, not per theme.

[index.html.ejs](https://github.com/camptocamp/ngeo/blob/master/contribs/gmf/apps/desktop/index.html.ejs) uses the class `gmf-app-data-panel` (392 hosts in September 2026, including `carto.aprona.net`). `body="c2cgeoportal"` is not usable: it matched 4 hosts, including `doc.geogirafe.org`.

| Tool | Query |
|------|-------|
| Google | `"GeoMapFish" OR c2cgeoportal (geoportail OR geoportal) -site:github.com` |
| Google | `inurl:/themes ngeo OR geomapfish` |
| Censys | `web.endpoints.http.body: "gmf-app-data-panel"` |
| FOFA | `body="gmf-app-data-panel"` |
| Censys | `web.endpoints.http.body: "gmf-"` |
| FOFA | `body="gmf-"` |

## GeoMoose (`geomoose`) {#geomoose}

Open-source WebGIS JavaScript framework (OSGeo community project, [geomoose.org](https://www.geomoose.org)), MapServer-backed. Common for US county parcel viewers (Minnesota-origin) and agency map portals; also deployed in Mongolia, Latin America, and Europe. Version 2 serves `geomoose.html` + `geomoose.js`; version 3 is a React app loading `geomoose/dist/geomoose.min.js` with `config.js` (`mapserver_url`, mapbook) and services (`identify`, `search`, `select`, `geocode-osm`).

**Signals:** `geomoose/config.js`, `geomoose/geomoose.js`, or `geomoose/dist/geomoose.min.js` script tags; `/geomoose2/geomoose.html` paths; title `GeoMoose`; MIT license header `Copyright (c) 2016 Dan "Ducky" Little` in the app HTML.

**Confirm:** GET the viewer root and match a `geomoose` script/config reference. One record per public viewer. Do **not** register MS4W landing pages (titles `MS4W - MapServer for Windows` list GeoMoose as a bundled package), the geomoose.org project sites, vendor demos built on `gm3-demo-data`, or bare-IP test instances. A retired GeoMoose replaced by ArcGIS Hub on the same host is not a find.

[index.html](https://github.com/geomoose/gm3/blob/main/examples/desktop/index.html) loads `geomoose/dist/geomoose.min.js` (30 hosts in September 2026, including `maps.glifwc.org` and `mapeamento.salvador.ba.gov.br`). `body="geomoose.css"` matched 36, including `www.geomoose.org`. `body="/geomoose2/"` matched 20, and the first hits are MS4W. `title="GeoMoose"` matched the project site and the docs.

GitHub code search does not index most forks. Forks of [geomoose/gm3](https://github.com/geomoose/gm3) (65 in September 2026) and [geomoose/geomoose-js](https://github.com/geomoose/geomoose-js) (6) keep the upstream homepage or none, and none publish GitHub Pages. `mapfile_root filename:config.js` and `loadMapbook filename:app.js` hit the upstream repo, `fwazeter/geomoose-test-env` (no public site), and `pinotronic/SigObras` (a SAPAL mobile client, not a public viewer).

New strings from that desktop `index.html` and from [geomoose.html](https://github.com/geomoose/geomoose-js/blob/master/geomoose.html): `body="geocode-osm.js"` matched 28, including `gis.garcia-consulting.com`. `body="Dan \"Ducky\" Little"` matched 42. `body="jump-to-extent"` matched 29. `body="geomoose/dist/css/geomoose.css"` matched 26. `body="user_catalog.css"` matched 14 (version 2). `body="GeoMOOSE.org"` matched 78, and the first hits are MS4W. `body="skins/grey/grey.css"` is not a fingerprint. Keep a host only when `mapbook.xml` lists data layers (parcels, sewers, survey features). Drop basemap-only tools (`usngmarker.org`) and bare IPs whose mapfiles sit under `gm3-demo-data`.

| Tool | Query |
|------|-------|
| Google | `"geomoose.min.js" OR inurl:/geomoose2/geomoose.html (county OR parcel OR GIS)` |
| Google | `inurl:geomoose "config.js" -site:github.com -site:geomoose.org` |
| Censys | `web.endpoints.http.body: "geomoose.min.js"` |
| FOFA | `body="geomoose.min.js"` |
| GitHub | forks of `geomoose/gm3` and `geomoose/geomoose-js`; `mapfile_root filename:config.js`; `loadMapbook filename:app.js` |
| Censys | `web.endpoints.http.body: "geocode-osm.js"` |
| FOFA | `body="geocode-osm.js"` |
| FOFA | `body="Dan \"Ducky\" Little"` |
| FOFA | `body="jump-to-extent"` |
| FOFA | `body="geomoose/dist/css/geomoose.css"` |
| FOFA | `body="user_catalog.css"` |

## MiraMon (`miramon`) {#miramon}

MiraMon Map Server + Map Browser ([miramon.cat](https://www.miramon.cat)), developed by CREAF / Universitat Autònoma de Barcelona (GRUMETS). Deployed mainly in Catalonia and Andorra as thematic geoportals, climatic atlases, and Earth-observation data cubes. The server root often shows a Catalan listing page titled `Navegadors i Servidors de Mapes disponibles en aquest servidor`; the browser is a JS app loading `miramon.js` with a declarative `config.json`. Vendor example list: [miramon.cat/ENG/Servidors.htm](https://www.miramon.cat/ENG/Servidors.htm).

**Signals:** `<script src="miramon.js">` + `StartMiraMonMapBrowser(` in the page; title `Navegadors i Servidors de Mapes disponibles en aquest servidor` on server roots; `cgi-bin/{collection}/MiraMon.cgi?REQUEST=GetCapabilities&SERVICE=WMS` endpoints; legacy browsers use `createLayer(` + `CadenaMultiIdioma(` JS.

**Confirm:** GET the host root or viewer path and match a MiraMon script or the Catalan server-listing title. One record per public server catalog or distinct thematic browser (own domain/subdomain), not per collection inside a server listing. Do **not** register the miramon.cat vendor site, `datacube.uab.cat` / `creaf-46-60.uab.cat` style aliases of an already-registered server, or pages where `Miramón` is a person's name or the San Sebastián district (heavy FOFA noise in `country="ES"`).

[index.htm](https://github.com/grumets/MiraMonMapBrowser/blob/master/src/index.htm) calls `StartMiraMonMapBrowser` (6 hosts in September 2026, including `maps.ecopotential-project.eu`). `body="MiraMon Map Browser"` matched 12, including `datacube.cat`. `body="miramon.cgi"` matched 9, including `www.opengis.grumets.cat`. Server listings omit the browser call, so keep all three.

GitHub code search does not index most forks. Forks of [grumets/MiraMonMapBrowser](https://github.com/grumets/MiraMonMapBrowser) (2 in September 2026) have no GitHub Pages site. `StartMiraMonMapBrowser` and `VersioConfigMMN` hit only the upstream repo. Read `ServidorLocal` in `src/examples/*.json`: that pass found `maps.oemc.grumets.cat`, which the body queries had not indexed. Keep a host only when `config.json` `capa[]` lists data layers (not a basemap-only demo). `body="CadenaMultiIdioma"` is not a fingerprint (Spanish event sites). `body="VersioConfigMMN"` matches nothing because FOFA does not index the JSON config.

| Tool | Query |
|------|-------|
| Google | `"Navegadors i Servidors de Mapes" OR "MiraMon Map Browser" -site:miramon.cat` |
| Google | `inurl:miramon.cgi OR inurl:"cgi-bin/miramon"` |
| Censys | `web.endpoints.http.body: "StartMiraMonMapBrowser"` |
| FOFA | `body="StartMiraMonMapBrowser"` |
| Censys | `web.endpoints.http.body: "MiraMon Map Browser"` |
| FOFA | `body="MiraMon Map Browser"` |
| FOFA | `body="miramon.cgi"` |
| FOFA | `title="Navegadors i Servidors de Mapes"` |
| GitHub | forks of `grumets/MiraMonMapBrowser`; `VersioConfigMMN`; `ServidorLocal` in `src/examples/*.json` |
| FOFA | `body="Loading MiraMon Map Browser. Please wait"` |
| FOFA | `body="miramon.js"` |
| FOFA | `body="cgi-bin/MiraMon.cgi"` |
| FOFA | `domain="grumets.cat"` |

## Tianditu (`tianditu`) {#tianditu}

China National Geographic Information Public Service Platform (Map World). National, provincial, and municipal nodes share NGCC APIs and branding. Site: [tianditu.gov.cn](https://www.tianditu.gov.cn).

**Signals:** `tianditu` in hostname or HTML; 天地图 branding; Map World API keys / `tianditu.gov.cn` tile or widget hosts.

**Confirm:** GET the public node (province or city) and match 天地图 / Tianditu. One record per public node, not per map API key. Skip pure tile endpoints with no catalog UI.

| Tool | Query |
|------|-------|
| Google | `"天地图" (省 OR 市 OR 地理信息) -site:tianditu.gov.cn` |
| Google | `inurl:tianditu OR "Map World" 地理` |
| Censys | `web.endpoints.http.body: "tianditu"` |
| FOFA | `body="tianditu" && country="CN"` |

## GEOVIS (`geovis`) {#geovis}

Geovis Technology (中科星图) digital-earth platform family (GEOVIS Earth / 星图地球). Vendor cloud portals run on `geovisearth.com` subdomains; customer installations exist (AIRCAS national civil-space infrastructure portal). Site: [geovis.com.cn](https://www.geovis.com.cn).

**Signals:** `geovis-mapbox-sdk.js` script asset; Cesium + mapbox-gl bundle; 星图地球 / GEOVIS branding; `geovisearth.com` hostnames.

**Confirm:** GET the portal and match `geovis-mapbox-sdk` or 星图地球 branding plus a public imagery/dataset catalog. One record per public portal. Skip vendor marketing pages and OBS object-storage hosts (`*-obs.piesat.cn`-style infra).

| Tool | Query |
|------|-------|
| Google | `"geovis-mapbox-sdk" OR "星图地球" 影像` |
| Censys | `web.endpoints.http.body: "geovis-mapbox-sdk"` |
| FOFA | `body="GEOVIS" && country="CN"` |

## CityMaker (`citymaker`) {#citymaker}

Gvitech (伟景行科技股份有限公司) 3D GIS platform (CityMaker Server / Builder) used for three-dimensional city and industrial-park geoinformation systems. Site: [gvitech.com](https://www.gvitech.com).

**Signals:** page title `{name}三维地理信息系统`; `CityMaker` in page body; legacy XHTML/IE-era 3D viewer chrome.

**Confirm:** GET the viewer and match the 三维地理信息系统 title plus a CityMaker reference. One record per public 3D GIS site. Skip vendor pages (`gvitech.com`, `developer.gvitech.com`) and login-only systems.

| Tool | Query |
|------|-------|
| Google | `"CityMaker" "三维地理信息系统"` |
| Censys | `web.endpoints.http.body: "CityMaker"` |
| FOFA | `body="CityMaker" && country="CN"` |

## PIE-Engine (`pieengine`) {#pieengine}

Piesat (航天宏图) remote-sensing and geoinformation cloud service platform. Flagship portal at [engine.piesat.cn](https://engine.piesat.cn); thematic nodes on other `piesat.cn` subdomains.

**Signals:** title `PIE-Engine 遥感与地理信息云服务平台`; `PIE-Engine` in page body; `piesat.cn` hostnames (skip `*-obs.piesat.cn` object-storage infra).

**Confirm:** GET the portal and match the PIE-Engine title plus a public dataset/imagery catalog. Note: `engine.piesat.cn` is CN-geo-fenced and times out from many non-CN networks — FOFA title evidence is acceptable for a scheduled record pending CN-network verification.

| Tool | Query |
|------|-------|
| Google | `"PIE-Engine" 遥感 site:piesat.cn OR intitle:"PIE-Engine"` |
| Censys | `web.endpoints.http.html_title: "PIE-Engine"` |
| FOFA | `body="PIE-Engine" && country="CN"` |

## Masterportal (`masterportal`) {#masterportal}

Hamburg LGV open-source map viewer used by German federal, state, and municipal agencies. Site: [masterportal.org](https://www.masterportal.org).

**Signals:** `Masterportal` in title or footer; `lgv-config` / `config.js` portal JSON; OGC WMS/WFS/CSW theme tree.

**Confirm:** GET the viewer URL and match Masterportal config plus a public layer tree. One record per public portal instance. Do **not** set `masterportal` from vianovis touvia.MAPS tenants (`loadTouviaMaps()`, `touvia.de/scripts/loader.js`) — those are `touviamaps`. Do **not** set `masterportal` from VC Map (`html.vcs-ui`, title `VC Map`).

[index.html](https://bitbucket.org/geowerkstatt-hamburg/masterportal/src/dev/portal/master/index.html) mounts `<div id="masterportal-root">` (205 hosts in September 2026, including `stadtplan.esslingen.de` and `geoportal-niederrhein.de`). The same file's `<title>Masterportal</title>` matched 4, including `addon.smartcity-paderborn.de`. Branded portals retitle the page but keep the root div, so use the div.

| Tool | Query |
|------|-------|
| Google | `"Masterportal" (Geoportal OR Kartendienst) site:.de -site:masterportal.org` |
| Censys | `web.endpoints.http.body: "masterportal-root"` |
| FOFA | `body="masterportal-root"` |
| Censys | `web.endpoints.http.body: "Masterportal"` |
| FOFA | `body="Masterportal"` |
| Censys | `web.endpoints.http.body: "lgv-config"` |
| FOFA | `body="lgv-config"` |

## touvia.MAPS (`touviamaps`) {#touviamaps}

vianovis GmbH hosted municipal web GIS. Product: [touvia.MAPS](https://www.vianovis.de/). Public tenants live at `vianovis.net/{tenant}/` or a city/county host that still loads `touvia.de/scripts/loader.js`. Distinct from Hamburg Masterportal (`masterportal`) even when the same vendor also offers touvia.MASTERPORTAL.

**Signals:** `loadTouviaMaps()`; script `touvia.de/scripts/loader.js`; `meta` copyright `vianovis GmbH`; assets under `touvia.de/uploads/{id}/config/`; title `… - Geoportal` / `… - Stadtplan` / `… - BürgerGIS`.

**Confirm:** GET the public portal and match `loadTouviaMaps` plus vianovis/touvia credits (Kronach `360grad.landkreis-kronach.de` uses `touvia.de/uploads/{id}/config/` on a district host). One record per municipality or Landkreis tenant. Skip the marketing site `vianovis.de`. Do **not** set `touviamaps` from Masterportal (`masterportal.js`, `lgv-config`) or VC Map (`html.vcs-ui`). Do **not** set `masterportal` from touvia.MAPS.

| Tool | Query |
|------|-------|
| Google | `site:vianovis.net Geoportal OR BürgerGIS` |
| Google | `"vianovis GmbH" (Geoportal OR Stadtplan OR BürgerGIS) site:.de` |
| Censys | `web.names: "vianovis.net"` |
| FOFA | `domain="vianovis.net"` |
| FOFA | `body="loadTouviaMaps"` |
| FOFA | `body="touvia.de/scripts/loader.js"` |
| crt.sh | `%.vianovis.net` |

## INGRADA online (`ingrada`) {#ingrada}

Softplan Informatik municipal web GIS. Product: [INGRADA](https://www.ingrada.de/startseite.html). Distinct from VertiGIS WebOffice (`weboffice`), MapGuide (`mapguide`), generic German BürgerGIS landing pages, and CAIGOS Globe (`caigos`).

**Signals:** title `INGRADA online {project}`; iframe `#ingrada`; script `/mobile/message-channel.js`; path `Softplan.Ingrada.Mobile` with `ProductId=IngradaOnline`; optional host `ingradaweb.org/{city}/online`.

**Confirm:** GET the public BürgerGIS / online viewer and match `ProductId=IngradaOnline` plus the mobile message-channel client. One record per municipality or Landkreis. Do **not** set `ingrada` from a BürgerGIS hostname that is WebOffice, ArcGIS, or a CMS landing page (Pforzheim, Böblingen `lrabb.de`). Do **not** set `mapguide` from INGRADA Mobile.

| Tool | Query |
|------|-------|
| Google | `"INGRADA online" (BürgerGIS OR Geoportal) site:.de` |
| Google | `inurl:Softplan.Ingrada.Mobile OR site:ingradaweb.org` |
| Censys | `web.endpoints.http.html_title: "INGRADA online"` |
| FOFA | `title="INGRADA online"` |
| FOFA | `host="ingradaweb.org"` |
| FOFA | `body="IngradaOnline"` |
| crt.sh | `ingradaweb.org` |

## CAIGOS Globe (`caigos`) {#caigos}

CAIGOS GmbH (Kirkel) WebGIS client and municipal Geoportal product. Products: [CAIGOS Globe](https://www.caigos.de/produkte/betriebsmittel/caigos-globe/), [CAIGOS Geoportal](https://www.caigos.de/produkte/portal/caigos-geoportal/). Distinct from GeoPortal.rlp (`geoportalrlp`), INGRADA online (`ingrada`), and untitled utility Online-Planauskunft logins.

**Signals:** title `CAIGOS-Globe` or a municipal `Geoportal …` splash; body `CAIGOS-Globe`; query `cmd=wafdownload` (`WAF_Globe32.ico`, `GlobeFormCss`, `GlobeFormCssPortal`); version `v. 19-x-x`; optional `Copyright … CAIGOS GmbH`.

**Confirm:** GET the public Geoportal / Globe home and match `cmd=wafdownload` plus a CAIGOS-Globe credit. One record per municipality, Landkreis, or Land public viewer. Do **not** register `www.caigos.de`, `intern.ris.rlp.de` (use `extern.ris.rlp.de`), SBL/staff copies, `raumplusschulung.*` training tenants, `*-map` aliases of the same tenant, IP-only hosts, or Stadtwerke/WBV Planauskunft shells that only title `CAIGOS-Globe` with no public catalog branding.

| Tool | Query |
|------|-------|
| Google | `"CAIGOS-Globe" (Geoportal OR GlobeFormCss) site:.de` |
| Google | `"cmd=wafdownload" "CAIGOS-Globe"` |
| Censys | `web.endpoints.http.html: "CAIGOS-Globe"` |
| FOFA | `body="CAIGOS-Globe"` |
| FOFA | `body="cmd=wafdownload" && country="DE"` |

## VC Map (`vcmap`) {#vcmap}

Virtual City Systems open-source 2D/3D web GIS. Product: [VC Map](https://github.com/virtualcitySYSTEMS/map-ui) / [vc.systems](https://vc.systems/). Distinct from Hamburg Masterportal (`masterportal`) and vianovis touvia.MAPS (`touviamaps`).

**Signals:** `html.vcs-ui`; title `VC Map`; script `./assets/start.js`; optional host `{city}.virtualcitymap.de`.

**Confirm:** GET the public app and match `vcs-ui` plus `assets/start.js`. One record per city or Landkreis digital twin. Do **not** set `vcmap` from Masterportal (`masterportal.js`, `lgv-config`), touvia.MAPS (`loadTouviaMaps()`), or a generic Cesium 360 viewer without `vcs-ui` (Kronach Geoportal).

[index.html](https://github.com/virtualcitySYSTEMS/map-ui/blob/main/index.html) sets `class="vcs-ui"` (129 hosts in September 2026, including `hohen-neuendorf.virtualcitymap.de` and `dz.forchheim.de`). `title="VC Map"` matched 121, the same product, so keep both.

| Tool | Query |
|------|-------|
| Google | `"VC Map" OR virtualcitymap (digitaler Zwilling OR Stadtmodell) site:.de` |
| Google | `site:virtualcitymap.de` |
| Censys | `web.endpoints.http.body: "vcs-ui"` |
| FOFA | `body="vcs-ui"` |
| Censys | `web.endpoints.http.html_title: "VC Map"` |
| FOFA | `title="VC Map"` |
| crt.sh | `%.virtualcitymap.de` |

## PopGIS (`popgis`) {#popgis}

Pacific Community (SPC) population / census GIS. Site: [spc.int PopGIS](https://www.spc.int/our-work/geospatial/popgis).

**Confirm:** GET the public map/layer catalog for a country or territory node.

| Tool | Query |
|------|-------|
| Google | `"PopGIS" (census OR geospatial) (Pacific OR SPC)` |
| Censys | `web.endpoints.http.body: "PopGIS"` |
| FOFA | `body="PopGIS"` |

## MangoMap (`mangomap`) {#mangomap}

Hosted map galleries. Tenants are path URLs on `mangomap.com` or a custom domain. Site: [mangomap.com](https://mangomap.com).

**Signals:** inline `MangoGis.MapPortalInit`, stylesheet/script `application_one_page_app`, `_CLIENT_PORTAL_URL`, cookie `_mango_gis_v2_session`. Custom domains still set `_GEO_HOST` to `mangomap.com`.

**Confirm:** GET `/{tenant}/maps` (or `/{tenant}/data` when the map gallery is empty). Keep the tenant when the public gallery lists maps or the data tab lists datasets. One record per tenant, not per map. Drop sign-in-only galleries (“does not currently have any publicly available maps”) and empty data tabs. `domain="mangomap.com"` only returns the SaaS host, not each path tenant.

| Tool | Query |
|------|-------|
| Google | `site:mangomap.com` |
| crt.sh | `%.mangomap.com` |
| Censys | `web.names: "mangomap.com"` |
| FOFA | `body="MangoGis.MapPortalInit"` |
| FOFA | `body="application_one_page_app"` |
| FOFA | `body="_CLIENT_PORTAL_URL"` |
| FOFA | `header="_mango_gis_v2_session"` |
| FOFA | `domain="mangomap.com"` |
| FOFA | `body="mangomap.com"` |

## NetGIS Server (`netgisserver`) {#netgisserver}

Netcad GIS server, common in Turkish municipalities. Product: [NetGIS Server](https://www.netcad.com/tr/urunler/netgis-server).

**Signals:** `/Netgis7`, `/keos/` city guide, title `NetGIS Server 7`.

**Confirm:** GET the KEOS viewer or `/Netgis7` title page. Optional WMS: `wms.ashx` GetCapabilities. Do not confuse with Sampaş `/KentrehberiApp/` or GiSoftGis Angular city guides. Do **not** set `netgisserver` on Danish `/NetGISRuntime/` viewers (`netgisruntime`).

| Tool | Query |
|------|-------|
| Google | `intitle:"NetGIS Server 7" OR inurl:/Netgis7 OR inurl:/keos/` |
| Censys | `web.endpoints.http.html_title: "NetGIS Server"` |
| FOFA | `title="NetGIS Server"` |

## NetGIS Runtime (`netgisruntime`) {#netgisruntime}

WSP Danmark municipal WebGIS. Product: [WSP Informatik / NetGIS](https://www.wsp.com/da-dk/hubs/informatik). Distinct from Turkish Netcad NetGIS Server (`netgisserver`) and from German `netgis.de` MapServer clients.

**Signals:** path `/NetGISRuntime/basis/index.jsp`; title `NetGIS - © WSP Danmark`; scripts `netgis_logo2.svg`, `../js/jquery-1.10.2.js`; query params `custid=` or `alias=`. Hosts are typically `netgis.{kommune}.dk`, `gis.{kommune}.dk`, or `webgis.{kommune}.dk`.

**Confirm:** GET the viewer with the municipality's `custid` or `alias` (bare `/NetGISRuntime/basis/index.jsp` may 500). One record per municipal viewer. Keep an existing `arcgisserver` REST directory on another host in the same kommune as a separate catalog. Do **not** set `netgisserver`.

| Tool | Query |
|------|-------|
| Google | `inurl:/NetGISRuntime/basis/index.jsp site:.dk` |
| Google | `"NetGIS - © WSP Danmark" OR "NetGISRuntime" kommune` |
| Censys | `web.endpoints.http.html_title: "NetGIS"` |
| FOFA | `title="NetGIS"` |

## Netigma (`netigma`) {#netigma}

Netcad low-code municipal platform, deployed as BELNET portals by Turkish municipalities. Product: [Netigma](https://www.netcad.com/tr/urunler/netigma).

**Signals:** path `/BELNET/LoginFW/Login.aspx` (or lowercase `/belnet/`); login asset `netigma-logo.png`; text `Netcad Hesabınızla Giriş Yapabilirsiniz`; title `Netigma`, `NETCAD`, or `BELNET - {municipality} Belediyesi`; version footer like `6.10.0`. Hosts are typically `keos.{city}.bel.tr`, `webgis.{city}.bel.tr`, `eimar.{city}.bel.tr`, or `keos.{city}-bld.gov.tr`.

**Confirm:** GET the BELNET login page and check for `netigma-logo.png`. One record per municipal BELNET portal. The same host often serves a NetGIS Server KEOS city guide at `/keos/` — keep that as a separate `netgisserver` catalog. Not BelsisIMS KRH (`ims.*/Projects/*/Pages/KRH.aspx`, `belsisims`).

| Tool | Query |
|------|-------|
| Google | `inurl:/BELNET/LoginFW/ OR inurl:/belnet/ "Netcad Hesabınızla"` |
| Google | `"netigma-logo" OR intitle:"BELNET" belediyesi` |
| Censys | `web.endpoints.http.html_title: "Netigma"` |
| FOFA | `body="netigma-logo"` |

## cardo (`cardo`) {#cardo}

IDU IT geospatial platform (Germany and neighbours). Site: [cardogis.com](https://cardogis.com).

**Signals:** `/net3/public/`, cardo.Map, `cardo` in HTML/JS.

**Confirm:** GET the public map/catalog UI under `/net3/public/` (or the branded geoportal home). Skip intranet-only cardo installs.

| Tool | Query |
|------|-------|
| Google | `"cardo.Map" OR inurl:/net3/public/` |
| Censys | `web.endpoints.http.body: "cardo.Map"` |
| FOFA | `body="cardo.Map"` |

## GC Navi (`gcnavi`) {#gcnavi}

Informatix GeoCloud WebGIS for Japanese local governments. Product: [GC Navi](https://www.informatix.co.jp/gc/navi/).

**Signals:** `geocloud.jp/webgis/`, GC Navi, `bt=` / `p=` query parameters.

**Confirm:** GET the tenant WebGIS home (org subdomain on `geocloud.jp`). Distinct from internal GC Planets. One record per municipality tenant.

| Tool | Query |
|------|-------|
| Google | `"GC Navi" OR inurl:geocloud.jp/webgis/` |
| Censys | `web.names: "geocloud.jp"` |
| FOFA | `domain="geocloud.jp"` |
| FOFA | `body="GC Navi"` |
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
| FOFA | `host="webgis.alandis.jp"` |
| FOFA | `body="autologin_jswebgis"` |
| FOFA | `body="/alandis/portal/"` |
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
| FOFA | `host="www.sonicweb-asp.jp"` |
| FOFA | `body="sonicweb.js"` |
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
| FOFA | `domain="geogeo.jp"` |
| crt.sh | `%.geogeo.jp` |

## Geolonia スマートマップ (`geoloniagis`) {#geoloniagis}

Geolonia public WebGIS (公開型GIS「スマートマップ」), Digital Agency model-spec. Vendor: [geolonia.com/smartmap](https://www.geolonia.com/smartmap/). Multi-tenant brands include とっとりジオマップ (`{org}.tottori-geomap.jp`) and 香川県 公開型GIS -BRIDGES- (`map.pref.kagawa.lg.jp`). **Do not** set `software.id: smartmap` — that is the Kazakhstan `{district}.smartmap.kz` product.

**Signals:** Next.js style name `geolonia-smartmap/`; sprite `geolonia.github.io/custom-smartmap-sprite`; thematic layers under `/data/{id}/latest/`; とっとりジオマップ / BRIDGES branding. SaaS viewers are `{tenant}.smartmap.geolonia.com` (often an alias of a custom domain). Tile buckets are `{org}.smartcity.geolonia.com` and are not a second catalog. `body="geolonia"` and `cdn.geolonia.com/embed` match the Maps embed library, not this product.

**Confirm:** GET the public tenant map UI (not the Tottori hub, vendor marketing, or a citizen-report form). Keep the record only when the page lists thematic `/data/{id}/latest/` layers. One record per public tenant. Skip considering/unpublished municipalities on the hub map, `*.preview.smartmap.geolonia.com`, and prefecture hosts that return an empty 404.

| Tool | Query |
|------|-------|
| Google | `site:tottori-geomap.jp` |
| Google | `"とっとりジオマップ" OR "公開型GIS -BRIDGES-" OR "Geolonia" スマートマップ (GIS OR 地図) site:.jp` |
| Censys | `web.names: "tottori-geomap.jp"` |
| FOFA | `body="geolonia-smartmap"` |
| FOFA | `body="custom-smartmap-sprite"` |
| FOFA | `host="smartmap.geolonia.com"` |
| FOFA | `host="smartcity.geolonia.com"` |
| FOFA | `title="スマートマップ" && body="cdn.geolonia.com"` |
| FOFA | `domain="tottori-geomap.jp"` |
| crt.sh | `%.tottori-geomap.jp` |

## NOL-IS (`nolis`) {#nolis}

German municipal WebGIS. Site: [nol-is.de](https://www.nol-is.de).

**Signals:** assets from `maps.nol-is.de` or `static.nol-is.de`; NOL-IS / NOLIS branding.

**Confirm:** GET the public geoportal home. Skip vendor marketing pages.

| Tool | Query |
|------|-------|
| Google | `"NOL-IS" OR "NOLIS" Geoportal site:.de` |
| Censys | `web.names: "nol-is.de"` |
| FOFA | `domain="nol-is.de"` |

## GiSoftGis (`gisoftgis`) {#gisoftgis}

Turkish municipal Angular city guide. Path `/GiSoftGis/` with hash `#/cityguidepublic`.

**Signals:** `gi-ajax-loading-indicator`; meta “Kent Rehberi Uygulaması”.

**Confirm:** GET `/GiSoftGis/`. Distinct from NetGIS `/keos/` and Sampaş `/KentrehberiApp/`.

| Tool | Query |
|------|-------|
| Google | `inurl:/GiSoftGis/` |
| Censys | `web.endpoints.http.body: "GiSoftGis"` |
| FOFA | `body="GiSoftGis"` |

## Sampaş WebGIS (`sampaswebgis`) {#sampaswebgis}

AKOS municipal city-guide map. Typical path `/KentrehberiApp/Index`.

**Signals:** page title `SAMPAŞ WEBGIS`; `/KentrehberiApp/`.

**Confirm:** GET that path. One municipality tenant = one catalog. Do not also register a bundled ArcGIS REST root as a second catalog unless it is a distinct public product.

| Tool | Query |
|------|-------|
| Google | `"SAMPAŞ WEBGIS" OR inurl:/KentrehberiApp/` |
| Censys | `web.endpoints.http.html_title: "SAMPA"` |
| FOFA | `title="SAMPA"` |

## ActiveMap GIS (`activemapgis`) {#activemapgis}

Gradoservice municipal GIS (often Russian cities). Product: [ActiveMap](https://gradoservice.ru/products/activemap/).

**Confirm:** GET the public map portal home. Skip desktop-only marketing.

| Tool | Query |
|------|-------|
| Google | `"ActiveMap" GIS (портал OR Gradoservice)` |
| Censys | `web.endpoints.http.body: "ActiveMap"` |
| FOFA | `body="ActiveMap"` |

## Sputnik Web (`sputnikweb`) {#sputnikweb}

Geoscan platform for publishing georeferenced 3D city models, terrain, raster and
vector layers, panoramas and attachments. It is available as a hosted or on-premises
server product. Confirm the product from several signals, not from Cesium alone.

**Signals:** numbered `/location/{id}` pages; `/resources/css_min/main.min.css`;
`/resources/dist/common.entry.js`; matching feedback, login and theme bundles; explicit
Sputnik Web or Geoscan attribution. Confirmed municipal installations include Tomsk 3D
and the Nizhnevartovsk 3D portal.

| Tool | Query |
|------|-------|
| Google | `"Sputnik Web" (geoportal OR геопортал OR "3D портал")` |
| Google | `inurl:/location/ "resources/css_min/main.min.css"` |
| Censys | `web.endpoints.http.body: "/resources/dist/common.entry.js"` |
| FOFA | `body="/resources/dist/common.entry.js"` |

Register one record per public installation. Do not register individual numbered
locations as separate catalogs, and do not classify generic Cesium viewers as Sputnik Web.

## ZuluGIS Online (`zulugisonline`) {#zulugisonline}

Politerm (Политерм) browser client for ZuluServer, also called ZuluWeb. Product:
[ZuluGIS Online](https://www.politerm.com/products/geo/zulugisonline/). Typical URL
`http://{host}:{port}/ZuluWeb/` (default port **6473**). Distinct from the ZuluGIS
desktop app and from unrelated sites titled ZuluWeb (Italian agency, cinema, zoo login).

**Signals:** path `/ZuluWeb/` serving `js/compiled.min.js` plus `custom.js`; root
title `404 ZuluServer Request`; ZWS XML at `/zws` (`<zulu-server service="zws">`);
WMS `title` `WMS ZuluServer`; GetLayerList at `/zws/getlayerlist`.

**Confirm:** GET `/ZuluWeb/` (200 SPA) and unauthenticated POST `/zws` `GetZMMapList`
(or GET `/zws/getlayerlist`) returning named maps/layers. One record per public
ZuluServer, not per web map. Skip Politerm's demo `zs.zulugis.ru`, login-walled
utility GIS (`GetZMMapList` `401`), vendor multi-tenant workspaces
(`gis.yanenergo.online`), empty map lists, and IP-only hosts with no identifiable
owner.

| Tool | Query |
|------|-------|
| Google | `"ZuluGIS Online" OR inurl:ZuluWeb -politerm.com` |
| Censys | `web.endpoints.http.body: "/ZuluWeb/"` |
| FOFA | `title="404 ZuluServer Request"` |
| FOFA | `body="/ZuluWeb/" && country="RU"` |

## Геопортал RuMap (`rumap`) {#rumap}

Geocenter-Consulting (Digimap) web GIS on the RUMAP-GIS platform. Product: [Геопортал RuMap](https://digimap.ru/produkty/geoportal-rumap/). The public hosted portal is [rumap.ru](https://rumap.ru/) (open-access layer catalog, routing, geocoding, isochrones). Distinct from the licensed transport-analysis SPA on `transport.digimap.ru` (JWT login), from RoadNetworkBuilder (no public catalog UI), from the vendor shop `digimap.ru`, and from tile/mail/VPN hosts.

**Signals:** title `RuMap: геопортал, интерактивная карта, сервисы для анализа данных - Геоцентр-Консалтинг`; copyright `ЗАО Геоцентр-Консалтинг`; keywords `RuMapGIS`; v3 scripts `/shpjs/dist/shp.js`, `/shpwrite.bundle.min.js`, `/assets/index-*.js` plus OpenLayers modulepreload; v2 `ng-app="digimap"` at `/v2/`. Host `rumap.ru` (wildcard aliases `www` / `maps` / `api` / `tiles` / `pro` / `beta` serve the same SPA).

**Confirm:** GET `https://rumap.ru/` and match the title plus shpwrite/OpenLayers (or `/v2/` Angular `digimap` app). One record for the hosted portal. Skip `/v2` as a second catalog, skip bare-IP eAtlas consumer maps, skip `401`/`403` PRO workspaces, and do **not** set `rumap` from Digimap marketing pages or from `tile.digimap.ru` Apache test pages.

| Tool | Query |
|------|-------|
| Google | `"Геопортал RuMap" OR "RuMap: геопортал" site:.ru` |
| Google | `"RuMapGIS" OR ng-app="digimap"` |
| Censys | `web.endpoints.http.html_title: "RuMap: геопортал"` |
| FOFA | `title="RuMap: геопортал"` |
| FOFA | `body="RuMapGIS"` |
| FOFA | `body="/shpwrite.bundle.min.js"` |
| crt.sh | `%.rumap.ru` |

## map.apps (`mapapps`) {#mapapps}

con terra WebGIS framework. Product: [map.apps](https://www.conterra.de/portfolio/mapapps). Often paired with smart.finder SDI (`smartfindersdi`).

**Signals:** `/mapapps/`; con terra / map.apps in HTML.

**Confirm:** GET the public `/mapapps/` viewer (not a login-only intranet). If smart.finder is the catalog UI, prefer `smartfindersdi` for that catalog. Do **not** set `mapapps` on an Open data portal (`datenportal.ulm.de` redirects to a map.apps app, but the software map would force Geoportal; Ulm’s geoportal is already `portalulmde`). Do **not** set `mapapps` on IP SYSCON MapSolution (`/MapSolution/`, title `Home MapSolution`, `ipsyscon` packages).

| Tool | Query |
|------|-------|
| Google | `inurl:/mapapps/ (Geoportal OR "map.apps")` |
| Censys | `web.endpoints.http.body: "/mapapps/"` |
| FOFA | `body="/mapapps/"` |

## MapSolution (`mapsolution`) {#mapsolution}

IP SYSCON browser WebGIS for ArcGIS Enterprise. Product: [MapSolution](https://www.ipsyscon.de/produkte/mapsolution). German Kreis and city geoportals typically publish a Home MapSolution app catalog.

**Signals:** path `/MapSolution/apps/home/welcome`; title `Home MapSolution` plus a version; `/MapSolution/client/scripts/lib/ipsyscon`; Dojo `ipsyscon/login/Home`. Guest maps may also live at `/MapSolution/apps/app/client/public` or `/MapSolution/apps/app/client/000` (title `Öffentlicher Zugang`). Distinct from con terra `mapapps` (`/mapapps/`).

**Confirm:** GET the public welcome/app catalog (guest maps listed without a staff login). One record per public installation, not per named map client. Do **not** add login-only ALKIS/Geoportal-Plus tenants (`geo6.kreis-warendorf.de`) or MapSolution Kommunal staff viewers when a public geoportal already exists on another product.

| Tool | Query |
|------|-------|
| Google | `intitle:"Home MapSolution" inurl:/MapSolution/` |
| Censys | `web.endpoints.http.html_title: "Home MapSolution"` |
| FOFA | `title="Home MapSolution"` |
| FOFA | `body="/MapSolution/client/scripts/lib/ipsyscon"` |

## CoGIS (`cogis`) {#cogis}

Data East geoportal stack. Site: [cogis.dataeast.com](https://cogis.dataeast.com). Map services may be CoGIS Server, eLiteGIS (`elitegis`), or ArcGIS Server — register the **public catalog UI**.

**Confirm:** GET CoGIS Portal home. Prefer `elitegis` only when that is the branded viewer with no CoGIS Portal.

Legacy/custom-domain CoGIS portals may retain `/CoGIS/Map` routes or the shared
`/dist/base.min.js` and `/dist/main.min.js` client together with `/api/providers` and
`/api/image/linked`. This combination is stronger than any one generic asset or API route.

| Tool | Query |
|------|-------|
| Google | `"CoGIS" (портал OR Portal OR geoportal) -site:dataeast.com` |
| Censys | `web.endpoints.http.body: "CoGIS"` |
| FOFA | `body="CoGIS"` |

## Geocad System Enterprise Edition (`geocadgsee`) {#geocadgsee}

Russian regional and municipal GIS platform from Geocad plus, also abbreviated GSEE or
Geocad GEE. Government system inventories may list “Geocad System Enterprise Edition” as
the application server and spatial information system. The public web client publishes
thematic worksets, layer trees, object semantics and spatial search.

**Signals:** explicit GSEE attribution or system-inventory evidence; a shared Vue/
OpenLayers client under `/app/assets/` with `Platform-*`, `api-*`, `BaseVector-*` and
`WebMercatorProjection-*` modules; GSEE REST concepts such as worksets, `ids/filter` and
`graph_ids`. Confirmed deployments include Novosibirsk Oblast GISOGD, Krasnoyarsk's
interactive municipal map and the Tomsk urban-planning atlas at `map.admtomsk.ru`
(titled “ИС Геокад”; the older `map.admin.tomsk.ru` domain redirects there). Sakhalin's
`geo.sakhalin.gov.ru` is a probable GSEE deployment via Geocad's digital-twin project,
but the host drops non-Russian connections — verify from an in-RU vantage point before
attributing.

| Tool | Query |
|------|-------|
| Google | `"Geocad System Enterprise Edition" OR "Geocad GEE"` |
| Google | `"платформы ГЕОКАД" (ГИСОГД OR МГИС OR РГИС)` |
| Censys | `web.endpoints.http.body: "WebMercatorProjection" AND web.endpoints.http.body: "BaseVector"` |
| FOFA | `body="WebMercatorProjection" && body="BaseVector"` |

Do not classify from “ЕМГИС”, “ГИСОГД”, or a Geocad vendor mention alone: those terms can
describe a government system or bespoke project rather than this product.

## OpenGeoPortal (`opengeoportal`) {#opengeoportal}

Federated academic geoportal (Tufts and partners).

**Confirm:** GET the search/home UI that lists layers across institutions. Do not add a single layer preview URL.

[ogp_home.html](https://github.com/OpenGeoportal/OGP2/blob/master/geoportal/src/main/resources/templates/ogp_home.html) sets `OpenGeoportal.Config` (6 hosts in September 2026, including `geodata.tufts.edu` and `geodata.lib.purdue.edu`). `body="OpenGeoPortal"` matched 19 hosts, including `hgis.club`.

| Tool | Query |
|------|-------|
| Google | `"OpenGeoPortal" OR "Open Geoportal" (layers OR geodata)` |
| Censys | `web.endpoints.http.body: "OpenGeoportal.Config"` |
| FOFA | `body="OpenGeoportal.Config"` |

## smart.finder SDI (`smartfindersdi`) {#smartfindersdi}

con terra metadata/search portal. Product: [smart.finder SDI](https://www.conterra.de/portfolio/smartfinder-sdi). Often sits next to `mapapps`.

**Confirm:** GET the public catalog search (CSW or finder UI). If only `/mapapps/` is public, use `mapapps`.

| Tool | Query |
|------|-------|
| Google | `"smart.finder SDI" OR "smart.finder" Geoportal site:.de` |
| Censys | `web.endpoints.http.body: "smart.finder"` |
| FOFA | `body="smart.finder"` |

## GIS WebServer SE (`giswebse`) {#giswebse}

KB Panorama web GIS. Site: [gisweb.ru](https://www.gisweb.ru).

**Confirm:** GET the public geoportal (layer tree / map). Skip desktop GIS marketing.

| Tool | Query |
|------|-------|
| Google | `"GIS WebServer SE" (геопортал OR geoportal)` |
| Censys | `web.endpoints.http.body: "GIS WebServer SE"` |
| FOFA | `body="GIS WebServer SE"` |

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
| FOFA | `body="HyG Consultores" && body="mapa.jsp"` |

## Trimble Locus IMS (`trimblelocus`) {#trimblelocus}

Finnish municipal karttapalvelu from Trimble Locus (formerly Tekla GIS). Vendor: [Trimble UPA](https://upa.trimble.com/fi/toimialat/julkishallinto). Distinct from Turkish BelsisIMS (`belsisims`) and Sitowise Louhi (`louhi`).

**Signals:** path `/IMS/` or `/ims/`; ASP.NET MVC; scripts `/IMS/bundles/imscore` and `/IMS/bundles/tekla-mvc-common`; footer link to `upa.trimble.com`. Some cities host the viewer on `*.asiointi.fi`.

**Confirm:** GET the public map UI and match IMS bundles or Trimble branding. One record per city tenant, not per layer. Skip staff-only Locus back-office.

| Tool | Query |
|------|-------|
| Google | `inurl:/IMS/ karttapalvelu site:.fi` |
| Google | `"karttapalvelu" IMS OR "tekla-mvc" site:.fi` |
| Censys | `web.endpoints.http.body: "tekla-mvc-common"` |
| FOFA | `body="tekla-mvc-common"` |
| Censys | `web.endpoints.http.body: "/IMS/bundles/imscore"` |
| FOFA | `body="/IMS/bundles/imscore"` |

## Sitowise Louhi (`louhi`) {#louhi}

Sitowise municipal GIS public map viewer. Site: [sitowise.com Louhi](https://www.sitowise.com/digital-solutions/louhi-gis-platform-municipalities). Distinct from Trimble Locus IMS (`trimblelocus`); Louhi maps may still attribute some layers as Locus data.

**Signals:** OpenLayers `/Scripts/integration/openlayers/ol.js`; Sitowise snoobi `partner=stw`; Finnish municipal `kartta.` host without `/IMS/`.

**Confirm:** GET the public karttapalvelu. One record per municipality. Do not also tag the same UI as `trimblelocus`.

| Tool | Query |
|------|-------|
| Google | `"karttapalvelu" Sitowise OR Louhi site:.fi -inurl:/IMS` |
| Censys | `web.endpoints.http.body: "partner=stw"` |
| FOFA | `body="partner=stw"` |

## NieuwlandGeo Onemap (`nieuwlandonemap`) {#nieuwlandonemap}

Dutch municipal map SaaS from [NieuwlandGeo](https://www.nieuwlandgeo.nl/producten/onemap/). Public tenants live at `{org}.webgis.nl`. Distinct from Singapore OneMap, NC OneMap, Maldives OneMap, Chinese OneMapServer, and from GeoServer backends on the same organisation (`geoserver`).

**Signals:** hostname `*.webgis.nl`; Onemap / WebGIS chrome.

**Confirm:** GET the tenant and match the Onemap viewer. One record per public tenant. Skip `webgis.nl`, `onemap.nl`, `gemeenten.webgis.nl` marketing/demo, test tenants, and login-only hosts.

| Tool | Query |
|------|-------|
| Google | `site:webgis.nl Onemap OR WebGIS` |
| Google | `"Onemap" NieuwlandGeo (gemeente OR geoportaal) site:.nl` |
| Censys | `web.names: "webgis.nl"` |
| FOFA | `host="webgis.nl"` |
| crt.sh | `%.webgis.nl` |

## R3GIS (`r3gis`) {#r3gis}

Italian municipal WebGIS SaaS from [R3GIS](https://www.r3gis.com/). Public cartographic portals live at `{city}.r3gis.com` or `{city}-app.r3gis.com`. A city hostname counts when it redirects from an `r3gis.com` tenant. Distinct from login-only GreenSpaces, WorkSpaces, and RoadSpaces asset modules.

**Signals:** hostname `*.r3gis.com`; public mapset; green-census shell `life_public_portal`; GisClient `js/R3layout/js/R3layout.js`; chooser `public_mapset`.

**Confirm:** GET the public map portal and a layer, tree, or green-area list. One record per public tenant. Customer domains count when the page is that shell. Skip vendor marketing at r3gis.com, login-walled GreenSpaces / UrbanTools / RoadSpaces modules, and empty shells.

| Tool | Query |
|------|-------|
| Google | `site:r3gis.com (WebGIS OR mapset OR cartograf)` |
| Censys | `web.names: "r3gis.com"` |
| FOFA | `host="r3gis.com"` |
| FOFA | `body="R3-GIS"` |
| FOFA | `body="life_public_portal"` |
| FOFA | `body="ic-studied-trees.svg"` |
| FOFA | `body="js/R3layout/js/R3layout.js"` |
| FOFA | `body="public_mapset"` |
| FOFA | `body="www.r3-gis.com"` |
| crt.sh | `%.r3gis.com` |

## WebGIS Publisher (`webgispublisher`) {#webgispublisher}

NieuwlandGeo municipal map manager, predecessor of [Onemap](#nieuwlandonemap). Product: [nieuwlandgeo.nl/producten/webgis-publisher](https://www.nieuwlandgeo.nl/producten/webgis-publisher/). Public catalogs are themakaart choosers, often `Choosemap.aspx` on a municipal host. Distinct from Onemap (`{org}.webgis.nl`) and from GeoServer on `webgispublisher.nl` (`geoserver`).

**Signals:** `Choosemap.aspx`; title WebGIS Publisher. Hostname `*.webgispublisher.nl` alone is the GeoServer estate, not this id.

**Confirm:** GET the public chooser. One record per municipality. Do not also tag the same UI as `nieuwlandonemap` or the GeoServer as `webgispublisher`.

| Tool | Query |
|------|-------|
| Google | `"Choosemap.aspx" (gemeente OR WebGIS)` |
| Google | `"WebGIS Publisher" Nieuwland (gemeente OR geoportaal) -Onemap` |
| Censys | `web.endpoints.http.body: "Choosemap.aspx"` |
| FOFA | `body="Choosemap.aspx"` |

## KaartViewer (`kaartviewer`) {#kaartviewer}

GeoSquare / GeoNovation municipal GIS. Product: [geosquare.nl/kaartviewer](https://www.geosquare.nl/kaartviewer/). Tenants at `{org}.kaartviewer.nl` or a city hostname (`kaart.utrecht.nl`, `kaartviewer.maastricht.nl`). Distinct from GeoServer on the same estate (`geoserver`).

**Signals:** hostname `*.kaartviewer.nl` or title KaartViewer; `/admin/rest/kaartviewerapi/menu`; custom element `<kaart-viewer>`; menu shell `@geonovationbv/menu_new`; `/?@Openbaar`.

**Confirm:** GET the public viewer or `/admin/rest/kaartviewerapi/menu`. One record per tenant, not per menu map. Keep a tenant only when an unsecured bookmark tree (`/admin/v2/kaartviewerapi/bookmark/{id}/tree`) lists data layers (WMS/WFS), not a login wall, vendor demo, or basemap-only map. Skip acceptatie/test hostnames.

| Tool | Query |
|------|-------|
| Google | `site:kaartviewer.nl` |
| Google | `"KaartViewer" (gemeente OR omgevingsdienst) site:.nl` |
| Censys | `web.names: "kaartviewer.nl"` |
| FOFA | `host="kaartviewer.nl"` |
| FOFA | `host="kaartviewer"` |
| FOFA | `title="KaartViewer"` |
| FOFA | `title="KaartViewer - Menu"` |
| FOFA | `body="kaartviewerapi"` |
| FOFA | `body="@geonovationbv/menu_new"` |
| FOFA | `body="<kaart-viewer>"` |
| crt.sh | `%.kaartviewer.nl` |

## GeoApps (`geoapps`) {#geoapps}

Dutch hosted map-app SaaS. Product: [geoapps.nl](https://www.geoapps.nl/). Public viewers use `{org}.geoapps.nl` or a branded host. Most `{org}.geoapps.nl` tenants are staff login — register only unauthenticated public maps. Distinct from generic “geo apps” pages.

**Signals:** hostname `*.geoapps.nl`; GeoApps chrome; public project map without SSO.

**Confirm:** GET the map and confirm it lists layers without login. One record per public viewer. Skip login walls.

| Tool | Query |
|------|-------|
| Google | `site:geoapps.nl (kaart OR projectenkaart)` |
| Google | `"GeoApps" (gemeente OR regio) site:.nl` |
| Censys | `web.names: "geoapps.nl"` |
| FOFA | `host="geoapps.nl"` |
| FOFA | `body="geoapps"` |
| crt.sh | `%.geoapps.nl` |

## SITMUN (`sitmun`) {#sitmun}

Diputació de Barcelona municipal GIS. Public catalog: [sitmun.diba.cat](https://sitmun.diba.cat/). Distinct from ArcGIS REST on the same estate.

**Signals:** classic viewer CSS `library/dojo/themes/sitmun` (themes `sitmun-diba`, `sitmun-dipta`, `sitmun-dille`, `sitmun-inspire`); path `/sitmun/inicio.jsp` or `/visorSitmun/`; DWR `ConfigManager.listAplicaciones`. SITMUN 3 default title `SitmunViewerApp` and `SITMUN Service worker registered` in `index.html`.

**Confirm:** GET the public viewer and confirm a public application or layer list (public access, or `listAplicaciones` for the public user). One record per public SITMUN catalog, not per municipality overlay (`idelocals`, `?ter=`). Skip login-only homes and the network site `sitmun.org`.

| Tool | Query |
|------|-------|
| Google | `site:sitmun.diba.cat` |
| Google | `"SITMUN" (Diputació OR municipi) site:.cat` |
| Censys | `web.names: "sitmun.diba.cat"` |
| FOFA | `host="sitmun.diba.cat"` |
| FOFA | `host="sitmun"` |
| FOFA | `body="/sitmun/"` |
| FOFA | `body="library/dojo/themes/sitmun"` |
| FOFA | `body="/sitmun/inicio.jsp"` |
| FOFA | `body="visorSitmun/"` |
| FOFA | `body="SITMUN Service worker registered"` |
| FOFA | `title="SitmunViewerApp"` |

## dmCity (`dmcity`) {#dmcity}

Esri Finland municipal digital-city SaaS. Product: [esri.fi/tuotteet/dmcity](https://www.esri.fi/fi-fi/tuotteet/dmcity/intro). Public map tenants wrap Experience Builder. Distinct from generic Experience Builder (`experiencebuilder`) and from `{city}.dmcity.fi/server` REST (`arcgisserver`).

**Signals:** hostname `web.dmcity.fi`; path `/{city}/public/`; title `dmCity Web App`; `jimu-core/init.js`.

**Confirm:** GET the tenant URL and match the dmCity title. One record per city path. Skip the Esri Finland marketing pages. Do **not** set `software.id: experiencebuilder` on these tenants.

| Tool | Query |
|------|-------|
| Google | `site:web.dmcity.fi/public` |
| Google | `"dmCity Web App" OR "web.dmcity.fi" karttapalvelu site:.fi` |
| Censys | `web.names: "web.dmcity.fi"` |
| FOFA | `host="web.dmcity.fi"` |
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
| FOFA | `domain="infogis.fi"` |
| crt.sh | `infogis.fi` |

## Trimble Landfolio (`landfolio`) {#landfolio}

Spatial Dimension / Trimble mining and land cadastre map portals (formerly FlexiCadastre). Directory: [spatialdimension.com/portals](https://www.spatialdimension.com/portals/).

**Signals:** host `portals.landfolio.com/{country}/`; title “Spatial Dimension Landfolio” or “Cadastre Map Portal”. Classic map HTML loads `javascript/sd/sd.spatial.area.js` and embeds `SearchResultHtmlTemplatePath` / `LayerName`. eGov shells load `javascript/emcascriptfunctions.js` and `spatialdimension/js/sd.translation.js`. The Angular framework shell (`data-beasties-container`) exposes `GET /api/config/map` (`MapLayerName` on each `MapServices[].MapLayers[]`). `body="GetLandfolioLookupTable"` is not indexed. `body="data-beasties-container" && body="Cadastre"` is not usable (Portuguese “cadastro” sites).

**Confirm:** GET the public map portal (not `/arcgis/rest/services`). ArcGIS REST on Landfolio infrastructure stays `arcgisserver`. One record per country portal. Keep the record only when the public layer list names licence or cadastre layers. Drop tile basemaps (World Imagery, World Topo), login-only eGov homes, and “Cadastre Map - Coming Soon” pages.

| Tool | Query |
|------|-------|
| Google | `site:portals.landfolio.com` |
| Google | `"Landfolio" OR FlexiCadastre ("mining cadastre" OR "map portal")` |
| Censys | `web.names: "portals.landfolio.com"` |
| FOFA | `host="portals.landfolio.com"` |
| FOFA | `title="Landfolio"` |
| FOFA | `body="Cadastre Map Portal"` |
| FOFA | `body="javascript/sd/sd.spatial.area.js"` |
| FOFA | `body="SearchResultHtmlTemplatePath"` |
| FOFA | `body="javascript/emcascriptfunctions.js"` |
| FOFA | `body="spatialdimension/js/sd.translation.js"` |
| FOFA | `domain="cadastreminier.org"` |
| FOFA | `domain="miningcadastre.com"` |
| FOFA | `host="miningcadastre"` |
| crt.sh | `%.landfolio.com` |

## SHOGun (`shogun`) {#shogun}

Open-source Spring Boot WebGIS framework by terrestris. Product: [terrestris.de/en/software/shogun](https://terrestris.de/en/software/shogun/). Source: [terrestris/shogun](https://github.com/terrestris/shogun). Default map UI: [shogun-gis-client](https://github.com/terrestris/shogun-gis-client). Distinct from GeoServer (`geoserver`), GeoNetwork (`geonetwork`), and Masterportal (`masterportal`) on the same estate.

**Signals:** HTML title `SHOGun` or `SHOGun Client`; HTML comment `SHOGun` / `terrestris.github.io/shogun`; `gis-client-config.js`; `/client/?applicationId=`; public JSON `GET /applications` with `clientConfig` / `layerTree`.

**Confirm:** GET the public client and `/applications` (or `/applications/{id}` when the list is empty but the viewer URL carries `applicationId=`). One record per public map hostname, not per `applicationId` on the same host and not `maps2.` aliases of `maps.`. Skip vendor demos (`bdp-webgis.terrestris.de`, empty application lists with “Welcome to SHOGun”), `*-test` / `*-dev` / `*-staging` hosts, Keycloak-only landings (EO-Lab), and private company staff GIS with no public application.

[index.html](https://github.com/terrestris/shogun/blob/main/shogun-boot/src/main/resources/templates/index.html) comments `terrestris.github.io/shogun` (22 hosts in September 2026, including `webgis.sparkassen-it.de`). `shogun_logo.png` is not usable: it matched the machine-learning toolbox at `www.shogun-toolbox.org`. `body="SHOGun"` matched 78,928 unrelated hosts. The map client still matches `gis-client-config.js`, so keep that query.

| Tool | Query |
|------|-------|
| Google | `"SHOGun Client" (Geoportal OR WebGIS) -site:github.com` |
| Google | `inurl:/client/?applicationId= SHOGun` |
| Censys | `web.endpoints.http.body: "terrestris.github.io/shogun"` |
| FOFA | `body="terrestris.github.io/shogun"` |
| Censys | `web.endpoints.http.html_title: "SHOGun Client"` |
| FOFA | `title="SHOGun Client"` |
| FOFA | `body="gis-client-config.js"` |

## Hajk (`hajk`) {#hajk}

Open-source Swedish web GIS (React, Material UI, OpenLayers). Site: [hajkmap.github.io/Hajk](https://hajkmap.github.io/Hajk/). Source: [hajkmap/Hajk](https://github.com/hajkmap/Hajk). Installation gallery: [hajkmap.se användare](https://hajkmap.se/valkommen-till-hajk/exempelsamling/).

**Signals:** HTML title “Hajk - open source webGIS”; `appConfig.json` with `mapserviceBase` (`/api/v1`, `/api/v2`, or `/mapservice`); `appName` Hajk.

**Confirm:** GET `/appConfig.json` (or `/publik/appConfig.json`). One record per public map application, not the GeoServer/ArcGIS backend on the same municipality. Skip login-only Hajk (Örebro staff GIS, Partille). Skip the Netlify demo.

[apps/client/index.html](https://github.com/hajkmap/Hajk/blob/master/apps/client/index.html) titles the shell `Hajk - open source webGIS` (31 hosts in September 2026, including `vgpv.vgregion.se`).

| Tool | Query |
|------|-------|
| Google | `"Hajk - open source webGIS" OR "mapserviceBase" karta site:.se` |
| Google | `inurl:appConfig.json Hajk` |
| Censys | `web.endpoints.http.body: "Hajk - open source webGIS"` |
| FOFA | `body="Hajk - open source webGIS"` |
| Censys | `web.endpoints.http.html_title: "Hajk - open source webGIS"` |
| FOFA | `title="Hajk - open source webGIS"` |

## ScalarGIS (`scalargis`) {#scalargis}

Open-source Flask / OpenLayers WebGIS from WKT-SI. Product: [wkt.pt](https://www.wkt.pt/). Source: [scalargis/scalargis-server](https://github.com/scalargis/scalargis-server) and [scalargis/scalargis-client](https://github.com/scalargis/scalargis-client). Distinct from older WKT CartoMapas viewers (`cartomapas`) and from GeoServer (`geoserver`) backends on the same estate (DGT `geo2.dgterritorio.gov.pt/geoserver`).

**Signals:** HTML title `ScalarGIS` or DGT “WebSIG” chrome that loads `/scalargis/static/viewer/` or `/static/viewer/`; splash `logo-splash.png`; cookie page `/static/viewer/rgpd.html`. Viewer paths include `/mapa/geoportal`, `/mapa/`, `/visualizadorCadastro`, `/vi-smos`, `/dgt`, `/portugal-visto-ceu`. Hosts are typically `geoportal.cm-{muni}.pt`, `*.dgterritorio.gov.pt`, or `geosifor.sgifr.gov.pt`.

**Confirm:** GET the public viewer and match title `ScalarGIS` or `/static/viewer/` assets. One record per public tenant, not per named map path on the same hub (SMOS viSMOS / COScid / COSvgi stay one catalog; Algarve Acolhe is a map on IDEAlg). Skip WKT CartoMapas (`cartomapas`) without the ScalarGIS splash, Contabo demos, and `/backoffice` login. Do **not** set `scalargis` from GeoServer `/geoserver` already registered on the same host, or from SNIG GeoNetwork (`geonetwork`).

[SplashScreen.js](https://github.com/scalargis/scalargis-client/blob/main/packages/viewer/src/core/components/SplashScreen.js) references `logo-splash.png`. That filename is not usable as a body query: it matched 2,649 hosts in September 2026, including `www.liveone.com`. `title="ScalarGIS"` matched 26, including `geoportal.cm-castroverde.pt`.

| Tool | Query |
|------|-------|
| Google | `intitle:ScalarGIS geoportal site:.pt` |
| Google | `"logo-splash.png" OR inurl:/static/viewer/rgpd.html ScalarGIS` |
| Censys | `web.endpoints.http.html_title: "ScalarGIS"` |
| FOFA | `title="ScalarGIS"` |
| crt.sh | `%.wkt.pt` |

## CartoMapas (`cartomapas`) {#cartomapas}

Older WKT-SI municipal WebGIS (also branded WKTApp Arade). Product lineage: [wkt.pt](https://www.wkt.pt/) (vendor now markets ScalarGIS). Documented tenants include Alcoutim, Alcácer do Sal, Faro, and Albufeira. Distinct from ScalarGIS (`scalargis`) viewers with title `ScalarGIS` / `/static/viewer/`, and from GeoNetwork (`geonetwork`) on the same host (Portimão).

**Signals:** HTML title `CartoMapas`; credits “WKTApp Arade” or “WKT / Sistemas de Informação, Lda”; script `/static/build/js/bundle-map-app.js` (or `/geoportal/static/build/js/bundle-map-app.js`); Sphinx docs `wktapp-arade-cm-{muni}-doc`. Older Faro-class viewers load `/geoportal/static/bower_components/openlayers/` plus WKT credits instead of the webpack bundle. Paths include `/mapa/cartomapas`, `/mapa/pdm`, `/mapa/publico`, `/geoportal/mapa/pmot`.

**Confirm:** GET the public viewer and match `bundle-map-app.js`, title `CartoMapas`, or WKTApp Arade credits. One record per public tenant, not per named map path (`/mapa/pdm`, `/mapa/floresta`). Skip ScalarGIS splash hosts, Contabo demos, `/backoffice` login, and a second CartoMapas row on a host already registered as GeoNetwork. Do **not** set `cartomapas` from title `ScalarGIS` or `/static/viewer/`.

`bundle-map-app.js` matched 5 hosts in September 2026, including `geoportal.cm-alcoutim.pt` and `geoportal.cm-alcacer.wkt.pt` (title `PDM`). `title="CartoMapas"` matched 3.

| Tool | Query |
|------|-------|
| Google | `intitle:CartoMapas geoportal site:.pt` |
| Google | `"WKTApp Arade" OR "wktapp-arade-cm-" geoportal` |
| Google | `"bundle-map-app.js" geoportal site:.pt` |
| Censys | `web.endpoints.http.body: "bundle-map-app.js"` |
| FOFA | `body="bundle-map-app.js"` |
| Censys | `web.endpoints.http.html_title: "CartoMapas"` |
| FOFA | `title="CartoMapas"` |
| crt.sh | `%.wkt.pt` |

## MapFusion (`mapfusion`) {#mapfusion}

GeoPlan (Ourém, Portugal) Yii2 / OpenLayers municipal WebSIG. Product: [MapFusion](https://geoplan.pt/). Public hubs title `Infraestrutura de Dados Espaciais` and credit “Desenvolvido por: GeoPlan”. Distinct from MapGuide Fusion (`mapguide`), from QGIS Server (`qgisserver`) CGI on the same host, and from older GeoPlan PHP landings (`index.php?page=`) without Yii2 (Albergaria-a-Velha).

**Signals:** Yii2 `yii.js` plus `csrf-param`; path `/page/viewer?id=`; QGIS Server `cgi-bin/qgis_mapserv.fcgi?map=/var/www/MapFusion/Projetos/Visualizadores/{map}.qgz`; OpenLayers `/libs/ol/`; footer link geoplan.pt.

**Confirm:** GET `/page/viewer?id=` (or the IDE landing) and match the `/var/www/MapFusion/` QGIS map path or Yii2 plus GeoPlan credit. One record per public municipal hub, not per named viewer id (`eploc`, `planos-online`). Skip `demo.geoplan.pt`, `/site/login`, and GeoPlan marketing. Do **not** set `mapfusion` from MapGuide Fusion, from Águeda CKAN / GeoNetwork / GeoServer already registered on `*.sig.cm-agueda.pt`, or from `index.php?page=` GeoPlan shells without Yii2.

| Tool | Query |
|------|-------|
| Google | `"Desenvolvido por" GeoPlan "Infraestrutura de Dados Espaciais"` |
| Google | `" /var/www/MapFusion/" qgis_mapserv site:.pt` |
| Google | `inurl:/page/viewer?id= GeoPlan OR MapFusion` |
| Censys | `web.endpoints.http.body: "/var/www/MapFusion/"` |
| FOFA | `body="/var/www/MapFusion/"` |
| crt.sh | `%.geoplan.pt` |

## Origo (`origo`) {#origo}

Open-source OpenLayers web GIS from Origosamverkan. Product: [origomap.se](https://origomap.se/). Source: [origo-map/origo](https://github.com/origo-map/origo). Docs: [origo-map.github.io/origo-documentation](https://origo-map.github.io/origo-documentation/latest/). Distinct from Hajk (`hajk`), myCarta (`mycarta`), MapGuide Fusion (`mapguide`), and GeoServer (`geoserver`) catalogs on the same host.

**Signals:** script `origo.min.js`, `origo.js`, or `/origo2client/dist/origo.min.js`; `Origo(` initializer; Origosamverkan / origomap.se credits. Hosts are typically `karta.{kommun}.se`, `karta-ext.{kommun}.se/{kartan}/`, or `kartor.{kommun}.se/{kartan}/`.

**Confirm:** GET the public map UI (not `/geoserver`). One record per municipality viewer, not per themed map path on a gallery host (Sundsvall `karta.sundsvall.se/{map}/` stays one gallery record). Skip login-only internal Origo. Do **not** set `origo` from `appConfig.json` Hajk or from MapGuide `/mapguide/fusion/`.

[build/index.html](https://github.com/origo-map/origo/blob/master/build/index.html) loads `origo.min.js` (15 hosts in September 2026, including `karta.koping.se`) and starts the viewer with `var origo = Origo` (22 hosts, including `karta.koping.se`). Deployments change the JSON argument, so the initializer prefix is the wider query.

| Tool | Query |
|------|-------|
| Google | `"origo.min.js" OR "origo.js" karta OR kartan site:.se` |
| Google | `"Origosamverkan" OR origomap webbkarta` |
| Censys | `web.endpoints.http.body: "origo.min.js"` |
| FOFA | `body="origo.min.js"` |
| Censys | `web.endpoints.http.body: "var origo = Origo"` |
| FOFA | `body="var origo = Origo"` |

## Tailormap (`tailormap`) {#tailormap}

Open-source Angular / OpenLayers GIS viewer from B3Partners. Product: [tailormap.com](https://www.tailormap.com/). Source: [B3Partners/tailormap-viewer](https://github.com/B3Partners/tailormap-viewer). API: [B3Partners/tailormap-api](https://github.com/B3Partners/tailormap-api). Distinct from GeoServer (`geoserver`) catalogs on the same estate and from GeoSquare KaartViewer / NieuwlandGeo Onemap on other Dutch municipal hosts.

**Signals:** HTML title `Tailormap`; Angular `data-beasties-container`; path `/nl/app/{app}` or `/nl/page/`; JSON `GET /api/app/{app}`; older B3P portal `/portal/page/extern`. Hosts are typically `{org}.tailormap.nl`, `{org}.tailormap.com`, or a city GIS host that redirects there (Lelystad `kaart.lelystad.nl`).

**Confirm:** GET the public viewer or `/nl/page/startpagina` and match the title or `/api/app/{app}` JSON. One record per public tenant, not per named app path. Skip `demo.tailormap.com`, `snapshot.tailormap.nl`, workshop/cursus/temp hosts, `luchtfoto-*` tile CDNs, and login-only staff GIS. Do **not** set `tailormap` from GeoServer `/geoserver/web/` on a Warmteatlas/WIBON host that is already registered as `geoserver`.

[index.html](https://github.com/B3Partners/tailormap-viewer/blob/main/projects/app/src/index.html) titles the shell `Tailormap` and mounts `<tm-root></tm-root>`. The bare token `tm-root` is not usable (600 hosts, including `www.hgacg6.org`). The element plus the title is the served fingerprint: FOFA `body="<tm-root></tm-root>" && title="Tailormap"` returned 57 hosts in September 2026. `body="<tm-root></tm-root>"` alone returned 225, including TemplateMaker. Older builds use `data-critters-container`; current builds use `data-beasties-container`. Both keep the same element and title.

GitHub forks of [Tailormap/tailormap-viewer](https://github.com/Tailormap/tailormap-viewer) and [Tailormap/tailormap-api](https://github.com/Tailormap/tailormap-api) keep the upstream homepage `snapshot.tailormap.nl`. Code search `"<title>Tailormap</title>" "<tm-root></tm-root>"` and `ghcr.io/tailormap/tailormap` only hit the upstream repos, not municipal tenants. Use FOFA (and `domain="tailormap.nl"` / crt.sh `%.tailormap.nl`) for instances.

Keep a host only when a public app lists layers: walk `GET /api/page` tiles with `requiresLogin: false`, then `GET /api/app/{name}/map` and count `appLayers`. A shell whose `/api/app` is 401 and whose `/api/page` is 404 is login-only staff GIS.

| Tool | Query |
|------|-------|
| Google | `intitle:Tailormap site:.nl -snapshot -demo` |
| Google | `site:tailormap.nl OR site:tailormap.com gemeente OR viewer` |
| GitHub | `"<title>Tailormap</title>" "<tm-root></tm-root>"` (index.html; upstream only) |
| GitHub | forks of `Tailormap/tailormap-viewer` (homepage stays `snapshot.tailormap.nl`) |
| Censys | `web.endpoints.http.body: "<tm-root></tm-root>" and web.endpoints.http.html_title: "Tailormap"` |
| FOFA | `body="<tm-root></tm-root>" && title="Tailormap"` |
| FOFA | `domain="tailormap.nl"` |
| crt.sh | `%.tailormap.nl` |

## myCarta (`mycarta`) {#mycarta}

Aveki municipal web GIS (myCarta WebMap). Product: [Aveki Webb & App](https://www.aveki.se/Produkter/Geografisk_informationsplattform/WebbApp.aspx). Distinct from Hajk (`hajk`) and Origo (`origo`) on other Swedish `karta.*` hosts.

**Signals:** HTML title `myCarta WebMap` or `myCarta - WebMap`; meta description “myCarta WebMap, a client map application from Aveki AB”; path `/webmap/` or `/mycartawebmap/`; older clients load `js/emap.js` / `js/config.js` / `js/vendor.js` with `myCartaServerURL`; some hosts also serve `/myCartaServer/`. Hosts are typically `karta.{kommun}.se`, `{kommun}karta.{kommun}.se`, or `maps.{kommun}.se`.

**Confirm:** GET the public viewer and match the title or Aveki meta tag. One record per municipality viewer, not per `#m=` map. Skip login-only myCarta GO and the Aveki marketing site. Do **not** set `mycarta` from a Swedish `karta.*` host that is Hajk (`appConfig.json`) or Origo (`origo.min.js`).

| Tool | Query |
|------|-------|
| Google | `intitle:"myCarta WebMap" OR intitle:"myCarta - WebMap" site:.se` |
| Google | `inurl:mycartawebmap OR inurl:/webmap/ myCarta site:.se` |
| Censys | `web.endpoints.http.html_title: "myCarta WebMap"` |
| FOFA | `title="myCarta WebMap"` |

## AddSpatial (`addspatial`) {#addspatial}

Icebound web GIS (formerly Sokigo GLS). Product: [AddSpatial GIS](https://www.icebound.com/vara-produkter/addspatial-gis/). Distinct from Hajk (`hajk`), Origo (`origo`), myCarta (`mycarta`), and Digpro dpWebmap (`dpwebmap`).

**Signals:** HTML title `AddSpatial`; path `/smart/?profile=`; `LoginService/Brands`; `images/addspatial.svg`; Icebound copy in the SMART start page JSON. Municipal wrappers often iframe `atlas.{kommun}.se/smart/` from `karta.{kommun}.se`.

**Confirm:** GET the public `/smart/` client (follow the iframe target) and match the AddSpatial title or `addspatial.svg`. One record per municipality viewer. Skip `addspatial.icebound.com/SMART` (vendor login) and Icebound marketing pages. Do **not** set `addspatial` from a generic Swedish “smart karta” plugin, Hajk, Origo, or myCarta viewer.

| Tool | Query |
|------|-------|
| Google | `intitle:AddSpatial inurl:/smart/ site:.se` |
| Google | `"images/addspatial.svg" OR "LoginService/Brands" karta` |
| Censys | `web.endpoints.http.html_title: "AddSpatial"` |
| FOFA | `title="AddSpatial"` |

## ISY Map (`isymap`) {#isymap}

Norconsult Digital municipal web GIS (ISY Map, ISY Map Server, GeoInnsyn). Product: [norconsult.digital/produkter/isy-map](https://norconsult.digital/produkter/isy-map/). Distinct from Avinet Adaptive (`avinet`) and from ArcGIS Hub Nordlandsatlas.

**Signals:** title ISYMap or ISY Map Server; path `/geoinnsyn/` or `/webkart/`; host `*.isy.no`; WinMap.ico on Map Server.

**Confirm:** GET the public viewer. One record per municipality or inter-municipal application, not per map project query string. Skip staff-only WinMap.

| Tool | Query |
|------|-------|
| Google | `"ISY Map" OR ISYMap OR GeoInnsyn (kart OR kommune) site:.no` |
| Google | `inurl:/geoinnsyn/ OR inurl:/webkart/ ISY` |
| Censys | `web.names: "isy.no"` |
| FOFA | `domain="isy.no"` |
| crt.sh | `%.isy.no` |

## Avinet Adaptive (`avinet`) {#avinet}

Avinet Adaptive / Webatlas thematic map platform. Vendor: [avinet.no](https://www.avinet.no/). Distinct from ISY Map (`isymap`).

**Signals:** ExtJS 4.2.2 plus OpenLayers 2.13.1; `__guuid__` on the atlas home; scripts from `a3.avinet.no` or a local `jsLibs/` tree; HTML “Adaptive kartløsning”. Norwegian county “atlas”, temakart, and `*.aveg.no` road maps.

**Confirm:** GET the atlas home and match `__guuid__` with ExtJS 4.2.2 / OpenLayers 2.13.1 (scripts may be local or loaded from `a3.avinet.no`). Dataset check: POST `WebServices/client/Configuration.asmx/ReadAppConfig` with `{"guuid":"<__guuid__>"}` and keep the atlas when `layers` has named entries with `is_base_layer` false. Root `wms.ashx` often returns the HTML shell. One record per `__guuid__`. Skip `test.` / `-dev.` hosts, `*.avadaptive.no` Wayfinder shells, vendor templates such as `asplanviak.aveg.no`, and viewers whose thematic layers require login. Do **not** set `avinet` on nordlandsatlas.nfk.no (that is `arcgishub`).

| Tool | Query |
|------|-------|
| Google | `"Developed by Avinet" OR a3.avinet.no (atlas OR temakart) site:.no` |
| Google | `inurl:wms.ashx fylkesatlas OR nordatlas` |
| Censys | `web.names: "avinet.no"` |
| FOFA | `domain="avinet.no"` |
| FOFA | `body="avinet"` |
| FOFA | `body="a3.avinet.no"` |
| FOFA | `body="Adaptive kartløsning"` |
| FOFA | `body="__extjs__" && body="OpenLayers/2.13.1"` |
| FOFA | `body="adaptive-logo-ms.png"` |
| FOFA | `domain="aveg.no"` |

## Norkart Kommunekart (`kommunekart`) {#kommunekart}

Norkart Kommunekart municipal map platform (successor to the legacy Norkart WebAtlas). Vendor: [norkart.no](https://www.norkart.no/). Distinct from Avinet Adaptive (`avinet`) and ISY Map (`isymap`).

**Signals:** HTML title `Kommunekart`; page script `new Norkart({... appId: 'Kommunekart' ...})`; `Scripts/Kommunekart.min.js`; Cesium shell titled `Kommunekart 3D` on `3dx.kommunekart.com`; municipal viewer hosts with `kommunekart` in the body. Single national tenant at `www.kommunekart.com` — municipalities are in-app tenants, not subdomains.

**Confirm:** GET the viewer home and match the Norkart app script or Kommunekart title. One record per public viewer host (the national platform plus branded municipal hosts such as kart.harstad.kommune.no). Skip municipal CMS front pages that merely link or iframe Kommunekart, vendor login products (`kdv.norkart.no`, `renovasjonsportal.norkart.no`, `eiendomsomsetninger.norkart.no`), and the legacy `webatlas.no` root when it answers “No route found”. Bare IPs titled `WebAtlas` serving a Silverlight `WebAtlas.xap` are the unrelated Avo Bell business product, not Norkart.

| Tool | Query |
|------|-------|
| Google | `"Kommunekart" inurl:kart site:.kommune.no` |
| Google | `"new Norkart" OR "Kommunekart.min.js"` |
| Censys | `web.endpoints.http.html_title: "Kommunekart"` |
| FOFA | `title="Kommunekart"` or `body="kommunekart" && country="NO"` |
| FOFA | `domain="kommunekart.com"` |

## MAP+ (`mapplus`) {#mapplus}

TYDAC AG WebGIS (sold in Germany as GeoAS Web). Product: [tydac.ch/en/mapplus](https://www.tydac.ch/en/mapplus/). Distinct from GeoMapFish (`geomapfish`) and from mf-geoadmin3 (`mfgeoadmin3`).

**Signals:** path `/mapplus/` or `/mapplus-lib/`; tydac in HTML or script hosts; OpenLayers city-map UI (Chur, St. Gallen, Biel, geoJura bernois).

**Confirm:** GET the public Stadtplan / map UI and match `mapplus-lib` or tydac. One record per municipality or regional conference viewer. Do **not** set `mapplus` from a Swiss `map.` hostname alone (Winterthur, Uri, Schaffhausen, and map.geo.admin.ch are other stacks). Bern `map.bern.ch/arcgis/rest/services` stays `arcgisserver`.

| Tool | Query |
|------|-------|
| Google | `"mapplus-lib" OR inurl:/mapplus/ (stadtplan OR GIS) site:.ch` |
| Google | `"MAP+" OR tydac (WebGIS OR Stadtplan) site:.ch` |
| Censys | `web.endpoints.http.body: "mapplus-lib"` |
| FOFA | `body="mapplus-lib"` |

## EnviMAP (`envimap`) {#envimap}

Envirosense Hungary municipal zoning-plan GIS (GeoForte viewer also hosted on intermap.hu). Site: [envimap.hu](https://envimap.hu/). Distinct from Autodesk MapGuide and from old MapFish.

**Signals:** host `*.envimap.hu`; title EnviMAP; path `/hu/Admin/GeoForte/GeoEdit` on envimap.hu or intermap.hu.

**Confirm:** GET the public zoning viewer. One record per municipality tenant. On GeoForte, keep the host only when `/hu/Admin/GeoForte/GeoEdit` embeds a non-empty `FXConfig.Layers` map whose names are not only `*_TESZT` templates. On the szabterv SPA, `GET /api/public/companies` lists tenants and `GET /api/public/layer-groups/company/{id}` lists WMS layers; drop a tenant whose groups are only basemaps. Do **not** set `envimap` from a Hungarian `/mapguide/` (`mapguide`) or ExtJS MapFish terinfo site.

| Tool | Query |
|------|-------|
| Google | `site:envimap.hu (szabterv OR GeoForte OR HÉSZ)` |
| Google | `inurl:/Admin/GeoForte/GeoEdit` |
| Censys | `web.names: "envimap.hu"` |
| FOFA | `domain="envimap.hu"` |
| FOFA | `domain="intermap.hu"` |
| FOFA | `title="EnviMAP"` |
| FOFA | `body="GeoForte"` |
| FOFA | `body="forteadmin.css"` |
| FOFA | `body="forteMenu.min.css"` |
| crt.sh | `%.envimap.hu` |

## imapTOO iMap (`imaptoo`) {#imaptoo}

Comox Valley Regional District's hosted iMap municipal web GIS for itself and neighbouring BC local governments. Product page: [comoxvalleyrd.ca iMap](https://www.comoxvalleyrd.ca/about/about-cvrd/imap). Distinct from generic "iMap"-named viewers on other platforms (Maryland iMap, King County iMap) and from 1Map (`1map`, Brazil).

**Signals:** host `*.imaptoo.ca` (or alias `imap2.comoxvalleyrd.ca`); viewer title `ArcGIS Web Application` with `jimu.js` Web AppBuilder assets at `/imap/`, `/imapviewer/`, or `/secure/`; shared ArcGIS Server directory at `mapviewer.imaptoo.ca/imap87320977492837458/rest/services` with tenant folders (`Cumberland`, `RDMW`) and `CVRD_*` / `VOC_*` services.

**Confirm:** GET the viewer and match `jimu.js` on an imaptoo.ca host, then GET the shared REST services directory. One record per municipal tenant viewer. Do **not** set `imaptoo` from unrelated "iMap" branding, and do not register stale tenant hosts that resolve but no longer serve (`cvrdimap`, `cumberlandimap`, `rdmw` on 207.102.200.93-98).

| Tool | Query |
|------|-------|
| Google | `site:imaptoo.ca` |
| Google | `"imaptoo" (iMap OR "regional district")` |
| Censys | `web.names: "imaptoo.ca"` |
| FOFA | `domain="imaptoo.ca"` |
| crt.sh | `%.imaptoo.ca` |

## PISO (`piso`) {#piso}

Realis municipal GIS for Slovenian občine. Hub: [geoprostor.net](https://www.geoprostor.net). Distinct from Kaliopa iObčina (`iobcina`).

**Signals:** host `geoprostor.net` or `piso.si`; title PISO / Prostorski informacijski sistem občin; path `/PisoPortal/`.

**Confirm:** GET the public hub. One registry record for the national hub (municipality selector), not one row per občina unless that municipality publishes a separate public catalog UI.

| Tool | Query |
|------|-------|
| Google | `"PISO" (občin OR geoprostor) site:.si` |
| Google | `site:geoprostor.net PisoPortal` |
| Censys | `web.names: "geoprostor.net"` |
| FOFA | `domain="geoprostor.net"` |

## GDi Visios (`gdivisios`) {#gdivisios}

GDi Ensemble (formerly LOCALIS) Web GIS viewer. Product: [gdi.net Ensemble Smart Portal](https://gdi.net/ensemble/ensemble-smart-portal/). Distinct from ArcGIS Hub/Server on other `gdi.net` hosts.

**Signals:** path `/visios/` or `/Visios/`; HTML title `GDi Visios`; scripts `VisiosAPI/gdi_js`; hosts `ensmartportal.gdi.net` or `localismarket.gdi.net`.

**Confirm:** GET the public viewer (not a CMS landing page that only mentions GDi). One record per municipality or county application. Do **not** set `gdivisios` from a GDi marketing page or from `arcgis-azure.gdi.net` REST. Skip GDi marketplace demo tenants unless that URL is the official public catalog.

| Tool | Query |
|------|-------|
| Google | `"GDi Visios" OR inurl:/visios/ (geoportal OR preglednik) site:.hr` |
| Google | `inurl:/visios/ site:gdi.net` |
| Censys | `web.endpoints.http.body: "GDi Visios"` |
| FOFA | `body="GDi Visios"` |

## MapGuide (`mapguide`) {#mapguide}

Autodesk MapGuide Open Source / MapGuide Enterprise. Hungarian CityScape E-GOV city viewers wrap MapGuide. Distinct from EnviMAP (`envimap`) and from old ExtJS MapFish terinfo sites.

**Signals:** path `/mapguide/` or `/mapguide2010/`; `mapviewerphp/ajaxviewer.php`; Fusion `fusionSF.js`; CityScape E-GOV / Arkance Twigis branding.

**Confirm:** GET the public `internet.php` or MapGuide viewer. Fusion `/mapguide/fusion/` clients (for example Umeåkartan) are `mapguide`, not `origo`. One record per municipality. Do **not** set `mapguide` from a Hungarian `/Admin/GeoForte/` EnviMAP tenant. Do **not** set `mapguide` on Indixio SIGim Web (`sigimweb`), Geo-IT GIS Touch Viewer (`geoitgis`), or Zeljko GIS (`zeljkogis`).

| Tool | Query |
|------|-------|
| Google | `inurl:/mapguide/ internet.php site:.hu` |
| Google | `"CityScape E-GOV" OR mapviewerphp MapGuide` |
| Censys | `web.endpoints.http.body: "mapviewerphp/ajaxviewer.php"` |
| FOFA | `body="mapviewerphp/ajaxviewer.php"` |

## Zeljko GIS (`zeljkogis`) {#zeljkogis}

Zeljko d.o.o. municipal and county Web GIS for Croatia and Bosnia and Herzegovina. Product: [zeljko.hr/webgis.html](https://www.zeljko.hr/webgis.html). Distinct from generic MapGuide (`mapguide`) even though Fusion tenants load `/mapguide25/fusion/`, `/mapguide252/fusion/`, or `/mapguide26/fusion/`.

**Signals:** hostname `zeljko-gis.com` or `zopcina.zeljko-gis.com`; Fusion `ApplicationDefinition=Library://` on mapguide25/252/26 templates (GradZadar, Psz, slate, obz, Vsz, Bpz); cadastral search UI at `zopcina.zeljko-gis.com/{tenant}/` or `/eki/`; footer `Izrada: Zeljko d.o.o.`; county host that still loads the same Fusion `ApplicationDefinition` (for example `gis.bpzzpu.hr:8008/mapguide/fusion/`).

**Confirm:** GET the public Fusion viewer or cadastral UI. One record per public tenant (city or county), not a second cadastral path of the same county map (`/eki/zadar/` with Grad Zadar Fusion, `zopcina.zeljko-gis.com/vsz/` with VSZ Fusion). Skip gas-utility ports (`Termoplin.GIS`), `Gis.Administrator`, Apache “It works!” on `:8008`, and Ajax Viewer layouts that only say “Cannot establish connection” (Jablanica). Do **not** set `mapguide` from `zeljko-gis.com` or `zopcina.zeljko-gis.com`.

| Tool | Query |
|------|-------|
| Google | `site:zeljko-gis.com fusion OR GIS` |
| Google | `site:zopcina.zeljko-gis.com GIS` |
| Censys | `web.names: "zeljko-gis.com"` |
| FOFA | `host="zeljko-gis.com"` |
| FOFA | `body="Izrada: Zeljko"` |
| crt.sh | `%.zeljko-gis.com` |

## Geo-IT GIS Touch Viewer (`geoitgis`) {#geoitgis}

Geo-IT hosted Flemish municipal GIS. Product: [Geo-IT GIS Raadplegen](https://geoit.be/nl/producten/geo-it-gis/geo-it-gistm-module-raadplegen-0). Distinct from generic MapGuide (`mapguide`) even though tenants pass `Library://Gemeenten/{City}/Maps/*.MapDefinition` query strings.

**Signals:** hostname `geoitgis.geo-it.be`; path `/touchviewer/`; title `Geo-IT GIS™ Touch Viewer`; scripts `Content/js/jquery/geoit.widgets.js`, `mg-api.js`, `mg-viewer-base-widget.js`; OpenLayers 4.

**Confirm:** GET the public Touch Viewer (not the Geo-IT marketing site). One record per municipality tenant, not per themed MapDefinition. Skip cemetery-only and campaign maps. Do **not** set `mapguide` from `/touchviewer/` or `MapDefinition` query strings.

| Tool | Query |
|------|-------|
| Google | `site:geoitgis.geo-it.be/touchviewer` |
| Google | `"Geo-IT GIS" "Touch Viewer" geoloket` |
| Censys | `web.names: "geoitgis.geo-it.be"` |
| FOFA | `host="geoitgis.geo-it.be"` |
| crt.sh | `geoitgis.geo-it.be` |

## SIGimWeb (`sigimweb`) {#sigimweb}

Indixio SIGim Web municipal GIS for Quebec MRCs and cities. Product: [indixio.com/fr/sigim](https://indixio.com/fr/sigim/). Distinct from generic MapGuide (`mapguide`), GOnet (`goazimut.com`), and JP Cadrin CIF assessment viewers.

**Signals:** HTML title `SIGimWeb`; path `/sigimweb/` or `/sigim/`; ExtJS; scripts `/gomap_web/`; municipality picker; older tenants may load `gplusload.ashx`.

**Confirm:** GET the public viewer (not the Indixio marketing site). One record per public MRC or city tenant. Do **not** add a second catalog for each municipality in the picker. Do **not** set `sigimweb` from a GOnet URL or from `jpcadrin.ca/CIF/`. Skip intranet `/sigimweb/intranet.htm` (login). MRC des Laurentides migrated off SIGimWeb to JP Cadrin CIF.

| Tool | Query |
|------|-------|
| Google | `inurl:/sigimweb/ OR intitle:SIGimWeb site:.qc.ca` |
| Google | `"SIGimWeb" OR "SIGim Web" (MRC OR municipalité) cartographie` |
| Censys | `web.endpoints.http.html_title: "SIGimWeb"` |
| FOFA | `title="SIGimWeb"` |

## GoMap (`gomap`) {#gomap}

Indixio GoMap web GIS platform (MapGuide Open Source + FDO), formerly Geomap GIS Amérique. SaaS tenants are hosted on `{client}.geomapguide.ca` (hosting brand iGeoMapGuide / "Service d'hébergement - GEOMAP GIS Amérique"); on-premise tenants use paths such as `/gomap/` or `/map/` on the owner domain. Product: [indixio.com/gomap](https://indixio.com/gomap/). Distinct from SIGimWeb (`sigimweb`), the Indixio Quebec municipal assessment viewer on the same engine, and from generic MapGuide (`mapguide`) sites.

**Signals:** HTML title `GoMap - {tenant}`; scripts under `/gomap_web/`; MapGuide `mapagent/mapagent.fcgi` backend or `mgosSession.ashx`; hostname `*.geomapguide.ca`.

**Confirm:** GET the public viewer. One record per public tenant. Skip dead legacy tenants (the 2016-2017 `saeiv-*.geomapguide.ca` transit sites are gone from DNS) and the vendor marketing pages. Do **not** set `gomap` from a `/sigimweb/` title page (use `sigimweb`), from unrelated "GoMap" products (gomap.in, Unity GO Map asset, gomap.dk), or from SunGIS Go GIS (`gogis`) on `{org}.gis.sungis.lv`.

| Tool | Query |
|------|-------|
| Google | `intitle:"GoMap -" -in -dk` |
| Google | `site:geomapguide.ca` |
| Censys | `web.names: "geomapguide.ca"` |
| FOFA | `domain="geomapguide.ca"` |
| FOFA | `body="/gomap_web/"` |
| crt.sh | `%.geomapguide.ca` |
| urlscan | `filename:gomap_web` |

## Go GIS (`gogis`) {#gogis}

SunGIS (SIA SunGIS, Latvia) municipal and utility WebGIS. Product: [Go GIS](https://www.sungis.lv/our-products/go-gis/). Public tenants are `{org}.gis.sungis.lv`. Distinct from Indixio GoMap (`gomap`) on `geomapguide.ca`, from Latvian terGIS (`tergis`) and pGIS (`pgis`), and from Stellenbosch University's `sungis08` GeoServer.

**Signals:** HTML title `Gogis V2` or `GogisFrontendV3`; Angular `data-beasties-container`; logo `/assets/images/gogis_logo_white-min.png`; OpenLayers under `/assets/ol/`; hostname `{tenant}.gis.sungis.lv`.

**Confirm:** GET `https://{tenant}.gis.sungis.lv/` and match the Gogis V2 / GogisFrontendV3 title. One record per public tenant subdomain. Do **not** add the marketing homepage `sungis.lv`. Do **not** set `gomap` or `tergis` from a `*.gis.sungis.lv` host. Skip login-walled tenants and NXDOMAIN names. A municipality may already have terGIS/pGIS/ArcGIS catalogs — Go GIS is a separate product.

| Tool | Query |
|------|-------|
| Google | `site:gis.sungis.lv Gogis` |
| Google | `"Gogis V2" OR "GogisFrontendV3" sungis` |
| Censys | `web.names: "gis.sungis.lv"` |
| FOFA | `host=".gis.sungis.lv"` |
| FOFA | `title="Gogis V2"` |
| crt.sh | `%.gis.sungis.lv` |

## Geocentriq (`geocentriq`) {#geocentriq}

CIM hosted Quebec municipal GIS for graphic matrices, assessment rolls, cadastre, and orthophotos. Product: [Geocentriq](https://geocentriq.com/). Distinct from GeoCentralis (`geocentralis`), SIGimWeb (`sigimweb`), GOnet (`goazimut.com/GOnet6`), and SIGALE (`sigale.ca`).

**Signals:** host `app.geocentriq.com`; path `/mrc/{mrc}`; title `{MRC} - Geocentriq`; scripts `geocentriq.min.js`. Confirm the product assets, not a hostname containing only `geo`.

**Confirm:** GET the MRC tenant URL and match Geocentriq branding plus a municipality picker or public map. One record per public MRC tenant, not per `/municipalite/` path. Skip the marketing homepage and `/login`.

| Tool | Query |
|------|-------|
| Google | `site:app.geocentriq.com/mrc` |
| Google | `"Geocentriq" (MRC OR municipalité) (matrice OR cadastre)` |
| Censys | `web.names: "app.geocentriq.com"` |
| FOFA | `host="app.geocentriq.com"` |
| crt.sh | `app.geocentriq.com` |

## GeoCentralis (`geocentralis`) {#geocentralis}

Évimbec hosted Quebec municipal GIS for graphic matrices, assessment rolls, cadastre, and zoning. Product: [GeoCentralis](https://www.geocentralis.com/). Distinct from Geocentriq (`geocentriq`), SIGimWeb (`sigimweb`), GOnet (`goazimut.com/GOnet6`), and SIGALE (`sigale.ca`).

**Signals:** host `portail.geocentralis.com`; path `/public/sig-web/{mrc}/{code}/` or `/public/sig-web-zonage/{slug}/{code}/`; title `GeoCentralis`; assets on `geocentralis-evaluationapp-prod.s3.amazonaws.com`. Confirm the product branding, not a hostname containing only `geo`.

**Confirm:** GET a municipality path under the MRC or city slug and match GeoCentralis branding plus a municipality picker or public map. One record per public MRC or city slug, not per geo-code path. Skip the marketing homepage, staff `/core/login/`, and a second zonage URL for the same tenant.

| Tool | Query |
|------|-------|
| Google | `site:portail.geocentralis.com/public/sig-web` |
| Google | `"GeoCentralis" (MRC OR municipalité) (matrice OR cadastre OR zonage)` |
| Censys | `web.names: "portail.geocentralis.com"` |
| FOFA | `host="portail.geocentralis.com"` |
| crt.sh | `portail.geocentralis.com` |

## SIGALE (`sigale`) {#sigale}

Fédération québécoise des municipalités graphic-matrix GIS (Altus). Product: [SIGALE](https://sigale.ca/). Distinct from Geocentriq (`geocentriq`), GeoCentralis (`geocentralis`), SIGimWeb (`sigimweb`), and GOnet (`goazimut.com/GOnet6`).

**Signals:** host `sigale.ca`; path `Main.aspx?mrc={code}`, `Map.aspx?mrc={code}`, or `/?mrc={code}`; title `Sigale - Fédération Québécoise des municipalités`; Contribuable municipality picker.

**Confirm:** GET the MRC-coded URL and match SIGALE branding plus a public map or assessment form. One record per public MRC code, not per municipality in the picker. Skip the hub without an `mrc` parameter.

| Tool | Query |
|------|-------|
| Google | `site:sigale.ca Main.aspx mrc=` |
| Google | `"sigale.ca" (MRC OR matrice) (contribuable OR cadastre)` |
| Censys | `web.names: "sigale.ca"` |
| FOFA | `host="sigale.ca"` |
| crt.sh | `sigale.ca` |

## SeaSketch (`seasketch`) {#seasketch}

UCSB/NCEAS marine spatial planning SaaS. Product: [seasketch.org](https://www.seasketch.org/). Distinct from ArcGIS REST on `data.seasketch.org` (`arcgisserver`).

**Signals:** host `www.seasketch.org`; path `/{project}/app`; HTML title SeaSketch.

**Confirm:** GET the project `/app` URL (overlay layers public without sign-in counts). One record per public project app, not the marketing homepage. Do **not** set `seasketch` from `data.seasketch.org/arcgis/rest/services`.

| Tool | Query |
|------|-------|
| Google | `site:seasketch.org/app` |
| Google | `"SeaSketch" "marine spatial" OR MSP` |
| Censys | `web.names: "seasketch.org"` |
| FOFA | `domain="seasketch.org"` |

## XY Maps (`xymaps`) {#xymaps}

Eckersall municipal GIS (XY • MAPS). Product: [xymaps.com](https://www.xymaps.com/) / [Eckersall XY Maps](https://www.eckersall.com/xy-maps/). Distinct from Geocortex and ArcGIS viewers Eckersall also builds for the same cities.

**Signals:** host `maps.xymaps.com` or `www.xymaps.com` with path `/{city}`; **or** city host path `/xymaps/Map`; HTML title City Maps powered by XY MAPS or Welcome to XY MAPS; `/Content/themes/themesAll/xymaps.css`.

**Confirm:** GET the public tenant map (parcel search / layer list without sign-in counts). One record per public city tenant, not the marketing homepage. `www.xymaps.com/{city}` is the same SaaS as `maps.xymaps.com/{city}` — do not add both. Do **not** set `xymaps` from an Eckersall Geocortex/ArcGIS URL, from `/Register` login, or from a private floorplan directory.

| Tool | Query |
|------|-------|
| Google | `intitle:"powered by XY" MAPS site:maps.xymaps.com` |
| Google | `inurl:/xymaps/Map "XY" GIS` |
| Censys | `web.names: "maps.xymaps.com"` |
| FOFA | `host="maps.xymaps.com"` |
| FOFA | `title="XY MAPS"` |
| FOFA | `body="xymaps.css"` |

## Spatial Suite (`spatialsuite`) {#spatialsuite}

Sweco web GIS; public client is SpatialMap. Vendor: [Sweco Spatial Suite](https://www.sweco.dk/ydelser/digitale-loesninger/spatial-suite/). Distinct from NIRAS KortInfo.

**Signals:** `/js/standard/browserdetect.js?ver=` SpatialMap version; Danish `webkort.` or `*kort*` municipal hosts; title SpatialMap.

**Confirm:** GET the public webkort. One record per municipality viewer, not the GeoServer backend on the same city.

| Tool | Query |
|------|-------|
| Google | `"SpatialMap" OR "Spatial Suite" webkort site:.dk` |
| Google | `inurl:webkort kommune site:.dk` |
| Censys | `web.endpoints.http.body: "browserdetect.js?ver="` |
| FOFA | `body="browserdetect.js?ver="` |

## KortInfo (`kortinfo`) {#kortinfo}

NIRAS hosted web GIS. Vendor: [NIRAS KortInfo](https://www.niras.dk/sektorer/data-digitalisering/webgis-kortinfo/). Distinct from Sweco Spatial Suite (`spatialsuite`).

**Signals:** host `drift.kortinfo.net`; path `/Map.aspx` with `Site=` tenant; titles or help on `help.kortinfo.net`; Danish municipal “KortInfo” / Kortviseren pages.

**Confirm:** GET the public `Map.aspx` tenant (Borgersite, kortHjemmeside, or the city’s documented page). One record per municipality `Site`, not per map page on the same tenant. Skip login-only sagsbehandling maps.

| Tool | Query |
|------|-------|
| Google | `site:drift.kortinfo.net Map.aspx` |
| Google | `"KortInfo" (kommune OR webkort OR kortviser) site:.dk` |
| Censys | `web.names: "kortinfo.net"` |
| FOFA | `domain="kortinfo.net"` |
| crt.sh | `%.kortinfo.net` |

## IntraMaps Public (`intramaps`) {#intramaps}

TechnologyOne Spatial municipal web GIS (IntraMaps Public). Product: [TechnologyOne Spatial](https://www.technology1.com/products/spatial). Used by Australian and New Zealand councils. Distinct from ArcGIS Hub / ArcGIS Server on the same council and from TechnologyOne eProperty.

**Signals:** HTML title `IntraMaps`; `ApplicationEngine/Frontend/images/poweredByLogo.png`; `ApplicationEngine/API/javascripts/spatial.min.js`; query `project=Public` or `project=*Public`; on-prem paths `/intramaps90/default.htm`, `/IntraMaps80/`, `/Public90/`, `/Public80/`; cloud tenants `{council}.spatial.t1cloud.com/spatial/intramaps/` with `configId=`.

**Confirm:** GET the public IntraMaps URL and match title IntraMaps plus ApplicationEngine assets. One record per public `project=` tenant (typically Public / *Public), not per module (Property, Planning, Aerial). Keep a tenant only when an anonymous public project returns selection layers (`/ApplicationEngine/layers/GetNumberOfNonGroupOrUploadedLayers` greater than 0). Skip login-only staff IntraMaps (Azure AD or Active Directory enterprise projects), `*-upgrade` / `*-origin` / `*-redirect` aliases of a registered tenant, and eProperty map pages.

| Tool | Query |
|------|-------|
| Google | `"IntraMaps" (council OR shire) (maps OR GIS) site:.gov.au` |
| Google | `inurl:/intramaps90/ OR inurl:/IntraMaps80/ OR inurl:spatial.t1cloud.com` |
| Google | `"poweredByLogo" IntraMaps ApplicationEngine` |
| Censys | `web.names: "spatial.t1cloud.com"` |
| FOFA | `host="spatial.t1cloud.com"` |
| FOFA | `title="IntraMaps"` |
| FOFA | `body="ApplicationEngine/Frontend/images/poweredByLogo.png"` |
| FOFA | `body="ApplicationEngine/API/javascripts/spatial.min.js"` |
| FOFA | `body="intramaps_canvas"` |
| FOFA | `body="mapcontrol.min.css"` |
| FOFA | `body="intramaps_base_url"` |
| FOFA | `body="basemap-split-screen-slider"` |
| FOFA | `body="intramaps90" \|\| body="intramaps96" \|\| body="intramaps98" \|\| body="intramapspublic" \|\| body="IntraMaps80"` |
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
| FOFA | `body="/connect/analyst/mobile"` |

## Exponare (`exponare`) {#exponare}

MapInfo / Pitney Bowes municipal web GIS, superseded by Precisely Spectrum Spatial Analyst. Remaining public tenants are Australian councils. Distinct from Spectrum Spatial Analyst (`/connect/analyst/`), IntraMaps, and ArcGIS Hub / REST on the same owner.

**Signals:** path `/exponare/RestPublicApplication.aspx`, `/exponare/PublicApplication.aspx`, `/exponare/Mobile.aspx`, or `/exponare/publicinvoker.aspx`; HTML title `Exponare Public` / `Willoughby Mapping` / `PublicInvoker`; ASP.NET Exponare assets; sometimes a council `mapping.aspx` wrapper that still loads `/exponare/`.

**Confirm:** GET the public Exponare URL and match `/exponare/` plus RestPublicApplication or PublicApplication. One record per public tenant, not a second copy of Public vs REST vs Mobile on the same host. Skip staff-only Exponare Enquiry and PDF “Exponare Enquiry Print” exports.

| Tool | Query |
|------|-------|
| Google | `inurl:/exponare/RestPublicApplication.aspx` |
| Google | `"Exponare Public" OR inurl:/exponare/publicinvoker site:.gov.au` |
| Censys | `web.endpoints.http.body: "/exponare/RestPublicApplication"` |
| FOFA | `body="/exponare/RestPublicApplication"` |

## LocalMaps (`localmaps`) {#localmaps}

Eagle Technology web GIS for New Zealand councils, on ArcGIS. Product: [LocalMaps](https://www.eagle.co.nz/gis-solutions/industry-solutions/localmaps). Public tenants show title **LocalMaps Gallery**.

**Signals:** path `/localmaps/gallery`; title `LocalMaps Gallery`; sometimes a branded `/{Council}Maps/Gallery/` path (Invercargill `ICCMaps/Gallery`) that still says LocalMaps in the HTML.

**Confirm:** GET the gallery and match LocalMaps. One record per council gallery, not per map in the gallery. Do **not** set `localmaps` on the ArcGIS REST `/arcgis/rest/services` directory on the same host (`arcgisserver`), on IntraMaps, Geocortex, Ruapehu InfoMap, or generic Experience Builder apps. Do not bulk-add guessed `{city}.govt.nz/localmaps/` hosts.

| Tool | Query |
|------|-------|
| Google | `inurl:/localmaps/gallery site:.govt.nz` |
| Google | `"LocalMaps Gallery" (council OR district) site:.nz` |
| Censys | `web.endpoints.http.html_title: "LocalMaps Gallery"` |
| FOFA | `title="LocalMaps Gallery"` |
| FOFA | `body="/localmaps/gallery"` |
| FOFA | `body="LocalMaps"` |

## GEUSMAP (`geusmap`) {#geusmap}

Geological Survey of Denmark and Greenland map application. Home: [data.geus.dk/geusmap](https://data.geus.dk/geusmap/). Named databases share `/geusmap/?mapname=`.

**Signals:** `/geusmap/?mapname=`; Jupiter, GERDA, or Greenland Mineral Resources branding; WMS/WFS export controls.

**Confirm:** GET `https://host/geusmap/?mapname={name}`. One record per public mapname. GEUS ArcGIS REST and GeoNetwork on other hosts stay those software ids.

| Tool | Query |
|------|-------|
| Google | `inurl:/geusmap/?mapname=` |
| Google | `"GEUSMAP" OR "geusmap" (Jupiter OR GERDA)` |
| Censys | `web.endpoints.http.body: "geusmap"` |
| FOFA | `body="geusmap"` |

## GISApp (`gisapp`) {#gisapp}

Fida Solutions / Urbanova municipal GIS. Tenants: `{city}.gisapp.ro` and city-owned hosts. Distinct from Kaliopa iObčina (`iobcina`) and from EQWC.

**Signals:** host `*.gisapp.ro`, **or** HTML title PortalPublic plus `logo_fida.png` / Fida branding on `gis.primaria*.ro` and similar city domains; urbanism certificate UI.

**Confirm:** GET the public city tenant and match PortalPublic / Fida. One record per municipality. ArcGIS REST on `webadaptor.gisapp.ro` stays `arcgisserver`. Do **not** set `gisapp` from a `gis.` hostname alone.

| Tool | Query |
|------|-------|
| Google | `site:gisapp.ro` |
| Google | `"PortalPublic" OR "logo_fida" (GIS OR urbanism) site:.ro` |
| Censys | `web.names: "gisapp.ro"` |
| FOFA | `domain="gisapp.ro"` |
| FOFA | `title="PortalPublic"` |
| FOFA | `body="logo_fida.png"` |
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
| FOFA | `domain="servizigis.it"` |
| FOFA | `body="GeneGis Site Creator"` |
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
| FOFA | `host="geoportale.sportellounicodigitale.it"` |

## GeoPortale.cloud (`geoportalecloud`) {#geoportalecloud}

Andreani Tributi (Gruppo Andreani) hosted municipal Web GIS. Product: [GeoPortale.cloud](https://www.geoportale.cloud/). Public tenants are `{comune}.geoportale.cloud` (sometimes `{comune}.andreanitributi.geoportale.cloud`). Distinct from GisMaster (`gismaster`) on `sportellounicodigitale.it`, GeneGIS PAGIS (`genegis`), LDP SIT (`ldpgis`), and p.mapper (`pmapper`) on `geo-portale.it`.

**Signals:** host `*.geoportale.cloud`; title “GeoPortale Comune di …”; **Accesso libero** / **Urbanistica** card; `apps/js/geo.js`; guest `login_start.php` then `map.php`; footer “Andreani Tributi”.

**Confirm:** GET the tenant home and match a public Accesso libero or Urbanistica map card (id `freemap` / `go_mapFree`). One record per comune tenant. Prefer `{comune}.geoportale.cloud` over the Andreani alias of the same comune. Skip `www.geoportale.cloud` (vendor hub / portfolio), login-only branded landings with no public map card, `test.` hosts, cPanel/mail infra, and default-vhost names whose certificate SAN does not match (they replay the marketing homepage).

| Tool | Query |
|------|-------|
| Google | `site:geoportale.cloud "GeoPortale Comune di"` |
| Google | `"geoportale.cloud" ("Accesso libero" OR "Visualizza Mappa")` |
| Censys | `web.names: "geoportale.cloud"` |
| FOFA | `domain="geoportale.cloud"` |
| FOFA | `title="GeoPortale Comune di"` |
| FOFA | `body="Andreani Tributi"` |
| crt.sh | `%.geoportale.cloud` |

## UrbisMap (`urbismap`) {#urbismap}

UrbisMap S.r.l.s. hosted national Web GIS for Italian urban-planning, cadastre, constraint, and regulatory layers. Product: [urbismap.com](https://www.urbismap.com/). Public catalog is the **single hub** at `www.urbismap.com` (Vue `/v2` app). Affiliated comuni (Ulassai, Cabras, Portoscuso, and sitemap `/territorio/{slug}` pages) deep-link that hub; they are not separate tenants. Distinct from GeoPortale.cloud (`geoportalecloud`), GisMaster (`gismaster`), GeneGIS PAGIS (`genegis`), LDP SIT (`ldpgis`), and p.mapper (`pmapper`).

**Signals:** host `www.urbismap.com` or `urbismap.com`; HTML title Urbismap; `/assets/index-*.js` Vue bundle; `/api/` JSON index (`territorio`, `wms`); path `/territorio/{slug}`.

**Confirm:** GET `https://www.urbismap.com/` and match the public map UI. One registry record for the national hub, not one row per `/territorio/{comune}` path, city alias (`/aosta`, `/venezia`), or municipal CMS page that only links the hub. Skip `www.urbismap.it` (marketing WordPress), `crm.urbismap.it`, `tiles`/`tiler`/`status`/`posthog`/`jenkins`, `401` beta hosts, dead `archivio.*` / `catasto` certificate leftovers, and Accesso agli Atti FOIA.

| Tool | Query |
|------|-------|
| Google | `site:urbismap.com geoportale` |
| Google | `"UrbisMap" (geoportale OR webgis) (Comune OR "pubblica amministrazione")` |
| Censys | `web.names: "urbismap.com"` |
| FOFA | `domain="urbismap.com"` |
| crt.sh | `%.urbismap.com` |

## LDP SIT (`ldpgis`) {#ldpgis}

LDP Progetti GIS hosted municipal territorial information system (SIT) with **LdP Viewer**. Product: [LDP GIS](https://www.ldpgis.it/). Tenants: `cloud.ldpgis.it/{slug}/`, `sct-*.ldpgis.it`, `maps1.ldpgis.it/{slug}/`, and city-owned hosts such as `maps.comune.arezzo.it`. Distinct from Drupal as the public catalog (`drupal` is only the CMS shell), from GeneGIS PAGIS (`genegis`), and from Maggioli GFMaplet (`gfmaplet`).

**Signals:** host `*.ldpgis.it`; title “Sistema Informativo Territoriale”; **LdP Viewer** / `ldpviewer`; `helpdesk@ldpgis.it`; OpenLayers map on `/maps/` or similar.

**Confirm:** GET the public municipal SIT and match LdP Viewer / ldpgis.it. One record per comune or union slug. Skip the vendor marketing hub `cloud.ldpgis.it/` with no slug and empty placeholder tenants that only repeat the LDP product homepage. Do **not** set `ldpgis` from a generic Drupal SIT title without LdP Viewer / ldpgis.it / helpdesk signals. Do not add MapCreator as a second catalog of the same comune.

| Tool | Query |
|------|-------|
| Google | `site:cloud.ldpgis.it` |
| Google | `"LdP Viewer" OR "helpdesk@ldpgis.it" (SIT OR "Sistema Informativo Territoriale") site:.it` |
| Censys | `web.names: "ldpgis.it"` |
| FOFA | `domain="ldpgis.it"` |
| FOFA | `body="ldpviewer"` |
| FOFA | `body="helpdesk@ldpgis.it"` |
| crt.sh | `%.ldpgis.it` |

## GFMaplet (`gfmaplet`) {#gfmaplet}

GLOBO S.r.l. (Gruppo Maggioli) Web GIS for Italian municipal and provincial geoportals, often embedded in Sportello Telematico Unificato (STU) Drupal pages. Product: [Cartografia Online](https://www.sportellotelematicopolifunzionale.it/cartografia-online). Tenants: `{comune}.prod.globogis.com` and city sportello hosts with a geoportale page. Distinct from GisMaster (`gismaster`) on `sportellounicodigitale.it`, from ATM Maggioli (`atmmaggioli`) Spanish open data, and from ArcGIS Server as the public catalog.

**Signals:** path `/page:s_italia:geoportale` or a comune-specific `/page:*:geoportale`; `/stu-geoportale-cartography`; `/gfmaplet/`; host `*.prod.globogis.com`; “Powered by GFMaplet”; Maggioli STU geoportale branding.

**Confirm:** GET the geoportale page (not the sportello form home) and match GFMaplet / Maggioli STU cartography. One record per geoportale tenant. Do **not** add `cartografia*.maggioli.cloud` ArcGIS REST as a second catalog of the same STU geoportale. Do **not** set `gfmaplet` from a Drupal geoportal that only links a GFMaplet user manual when the registered catalog is ArcGIS REST. Do not set `gfmaplet` on GisMaster `IdCliente=` pages.

| Tool | Query |
|------|-------|
| Google | `site:prod.globogis.com geoportale` |
| Google | `"Powered by GFMaplet" OR inurl:/page:s_italia:geoportale` |
| Censys | `web.names: "globogis.com"` |
| FOFA | `domain="globogis.com"` |
| FOFA | `body="/gfmaplet/"` |
| FOFA | `body="Powered by GFMaplet"` |
| FOFA | `body="stu-geoportale-cartography"` |
| FOFA | `body="GFMaplet()"` |
| FOFA | `host=".prod.globogis.com" && body="geoportale"` |
| crt.sh | `%.prod.globogis.com` |

The Drupal STU geoportale page does not contain “Powered by GFMaplet” or `/gfmaplet/`. `body="stu-geoportale-cartography"` and `body="GFMaplet()"` find custom-domain geoportals (checked 24 September 2026: 31 and 48 hosts). `host=".prod.globogis.com" && body="geoportale"` finds hosted tenants whose public page is the geoportale (111 hosts), not every sportello home. `body="js/gfmaplet/styles/app.css"` is not indexed. Keep a host only when `/stu-geoportale-cartography` or `/gfmaplet/` embeds `serviceLayers` with named thematic layers. Drop sportello homes, aliases of an existing tenant, and a viewer whose only layer is an administrative boundary.

## SmartMap (`smartmap`) {#smartmap}

Hosted Kazakh district investment geoportals. Tenants share `{district}.smartmap.kz`. Distinct from Geonomics (`geonomics`) akimat regional portals.

**Signals:** hostname `*.smartmap.kz`; Leaflet plus Google Maps; `stylse.css`; district/akimat investment layers.

**Confirm:** GET the tenant URL and match the Leaflet/Google Maps bundle. One record per district tenant. Skip unrelated SMARTMap finance products. Do **not** set `geonomics` from a `/map/` path on other KZ hosts — those Angular Leaflet `/map/` SPAs are `rgis`.

| Tool | Query |
|------|-------|
| Google | `site:smartmap.kz` |
| Google | `"smartmap.kz" (геопортал OR инвестиц)` |
| Censys | `web.names: "smartmap.kz"` |
| FOFA | `domain="smartmap.kz"` |
| crt.sh | `%.smartmap.kz` |

## SmartGIS (`smartgis`) {#smartgis}

GEO municipal Web GIS (2D/3D viewer). Product: [smartgis.geo.rs](https://smartgis.geo.rs). Docs: [smartgis-docs.geo.rs](https://smartgis-docs.geo.rs). Distinct from Kazakhstan SmartMap (`smartmap`), Greek GIS4Smart (`gis4smart`), GDi Visios (`gdivisios`), Indonesian GeoNode hosts named smartgis, Malaysian ArcGIS smartGIS portals, and unrelated SmartGIS brands (`smartgis.cz`, `smartgis.id`, `gis.smartview.hr`).

**Signals:** HTML title exactly `SmartGIS`; Angular `<app-root></app-root>`; `var point_cloud = null;` / `var viewer = null;`; `base href="/"`; hosts `{tenant}.geo.rs` or a city GIS hostname (`gis.topola.rs`, `suboticagis.rs`).

**Confirm:** GET the public viewer (not the marketing homepage). One record per public tenant, not per project map. Do **not** set `smartgis` from a title that only contains the word SmartGIS. Skip `smartgis.geo.rs`, `smartgis-docs.geo.rs`, `*-beta*` hosts, `www.`/`beta.` aliases of an existing tenant, and vendor demos (`smartgis-app.geo.rs`, `smartgis-gf.geo.rs`, `smartgis-geoput.geo.rs`).

| Tool | Query |
|------|-------|
| Google | `intitle:SmartGIS (geoportal OR GIS) site:.rs` |
| Google | `site:geo.rs SmartGIS -docs -beta` |
| Censys | `web.endpoints.http.html_title: "SmartGIS"` |
| FOFA | `title="SmartGIS" && country="RS"` |
| crt.sh | `%.geo.rs` |

## KAZGISA RGIS (`rgis`) {#rgis}

Regional Geographic Information System used by Kazakhstani akimats. Product page: [kazgisa.kz/rgis](https://kazgisa.kz/rgis/). Distinct from Geonomics (`geonomics`) Vue/Mapbox portals, SmartMap (`smartmap`) `{district}.smartmap.kz` tenants, and VKOMAP (`vkomap`) `/vkomap/` Leaflet+Esri viewers.

**Signals:** public path `{host}/map/`; Angular bundles `runtime.js`, `polyfills.js`, `vendor.js`, `main.js`; Leaflet 1.7.1 from unpkg; HTML titles `E-SQO`, `E-JAMBYL`, or `РГИС`.

**Confirm:** GET `{host}/map/` and match the Angular Leaflet SPA. One record per akimat or city geoportal. Do **not** set `rgis` from the older KAZGISA OpenLayers stack (`eatyrau.kz`). Do **not** set `geonomics`, `smartmap`, or `vkomap` from this `/map/` viewer.

| Tool | Query |
|------|-------|
| Google | `inurl:/map/ (E-SQO OR E-JAMBYL OR "РГИС") site:.kz` |
| Google | `"РГИС" геопортал (Шымкент OR Жамбыл OR СКО) Leaflet` |
| Censys | `web.endpoints.http.body: "/map/runtime.js"` |
| FOFA | `body="/map/runtime.js"` |

## KAZGISA OpenLayers WebGIS (`kazgisaopenlayers`) {#kazgisaopenlayers}

Legacy KAZGISA regional WebGIS generation used by Kazakhstani public authorities.
It is distinct from the current Angular/Leaflet KAZGISA RGIS (`rgis`).

**Signals:** OpenLayers client assets below `Components/openlayers/`; Knockout
`knockout-3.4.0.js`; shared `src/viewmodel/` modules; and application scripts such
as `Scripts/left-panel.js`, `Scripts/editing-layers.js`, and `Scripts/search.js`.
Deployments may expose a GeoServer WMS/WFS on the same parent host.

**Confirm:** require the OpenLayers asset tree plus either the Knockout or
`src/viewmodel/` fingerprint. Do not infer this product from OpenLayers alone, and
do not assign it to the Angular bundles used by `rgis`.

| Tool | Query |
|------|-------|
| Google | `"Components/openlayers/js/ol-new.js"` |
| Google | `"src/viewmodel/addressesvm.js" geoportal` |
| Censys | `web.endpoints.http.body: "Components/openlayers/js/ol-new.js"` |
| FOFA | `body="Components/openlayers/js/ol-new.js"` |

## Gharysh Geoportal Platform (`gharyshgeoportal`) {#gharyshgeoportal}

Modern sectoral government geoportal family developed by Kazakhstan Gharysh Sapary.
Confirmed independent deployments include HydroGOV (`test-gidro.gharysh.kz`) and the
Tabigat natural-resources map (`tabigat.gov.kz`).

**Signals:** bilingual Russian/Kazakh Next.js application; attribution or footer link
to `www.gharysh.kz`; and several shared hashed application chunks. Known strong
fingerprints include `29107295-1453a3860b50f70e.js`,
`c16184b3-d2d4d32abbeddd2d.js`, `6261-7c8973ad91cc0427.js`, and
`7914-8f223fa34cea4570.js`.

**Confirm:** require Gharysh attribution plus at least two of the shared non-runtime
chunks. Next.js alone is insufficient. Do not assign older Gharysh ArcGIS Web
AppBuilder deployments or the separate Angular flood viewer to this product.

| Tool | Query |
|------|-------|
| Google | `"www.gharysh.kz" "_next/static/chunks" geoportal` |
| Google | `"29107295-1453a3860b50f70e.js"` |
| Censys | `web.endpoints.http.body: "c16184b3-d2d4d32abbeddd2d.js"` |
| FOFA | `body="c16184b3-d2d4d32abbeddd2d.js"` |

## eKMap Cloud (`ekmap`) {#ekmap}

Vietnamese provincial planning GIS from eKGIS. Product: [ekgis.com.vn/ekmap-platform](https://ekgis.com.vn/ekmap-platform/). Docs: [docs.ekgis.vn](https://docs.ekgis.vn/). Distinct from Hanoi city planning `quyhoach.hanoi.gov.vn` (Next.js), Vinh Phuc OpenLayers 6 planning, and HCMC VLAB Leaflet planning.

**Signals:** `assets/ekmapboxgl/ekmap-mapboxgl.js` and `assets/ekmapboxgl/common.js`; Mapbox GL JS 1.13 plus `mapbox-gl-compare`; title often `eKMap Cloud` or provincial `Quy hoạch`. Hosts include `qhkhsdd.hanoi.gov.vn`, `quyhoach.haiphong.gov.vn`, `quyhoach.dienbien.gov.vn`, `quyhoach.langson.gov.vn`.

**Confirm:** GET the public planning viewer and match `ekmap-mapboxgl.js`. One record per province or city geoportal. Do **not** set `ekmap` from Mapbox GL alone, from `quyhoach.hanoi.gov.vn`, or from Vinh Phuc / HCMC planning maps.

| Tool | Query |
|------|-------|
| Google | `"eKMap Cloud" OR inurl:ekmap-mapboxgl (quy hoạch OR "Quy hoạch") site:.gov.vn` |
| Google | `"assets/ekmapboxgl/ekmap-mapboxgl.js"` |
| Censys | `web.endpoints.http.body: "ekmap-mapboxgl.js"` |
| FOFA | `body="ekmap-mapboxgl.js"` |

## VKOMAP (`vkomap`) {#vkomap}

Geoinfo (ТОО Геоинфо) municipal and regional geoportal. Vendor: [geoinfo.kz](https://geoinfo.kz/). Distinct from Geonomics (`geonomics`) Vue/Mapbox akimat portals and from SmartMap (`smartmap`) district tenants.

**Signals:** `/vkomap/` in CSS or HTML; Leaflet plus Esri; `/Public/GetKatoList` and `/Public/GetLayers` JSON; language path `/Kaz`. Hosts include `vkomap.kz`, `temirmap.kz`, `abaimap.kz`.

**Confirm:** GET the public map UI and match `/vkomap/` plus Leaflet/Esri. One record per akimat or city tenant. Do **not** set `vkomap` from a generic KZ `/map/` Angular viewer (`rgis`: e-sqo, geo-shym) or from Geonomics `map*.kz` hosts.

| Tool | Query |
|------|-------|
| Google | `"vkomap" (геопортал OR геопорталы) site:.kz` |
| Google | `inurl:/Public/GetKatoList site:.kz` |
| Censys | `web.endpoints.http.body: "/vkomap/"` |
| FOFA | `body="/vkomap/"` |
| crt.sh | `vkomap.kz` |

## Visor Urbano (`visorurbano`) {#visorurbano}

Guadalajara municipal urban-management GIS, replicated in other Mexican cities with Bloomberg Philanthropies support. Product: [visorurbano.com](https://www.visorurbano.com). Distinct from unrelated Leaflet visors that reuse the “Visor Urbano” label.

**Signals:** hostname `visorurbano.{city}.gob.mx` or `{city}.visorurbano.com`; title Visor Urbano; `/logos/visor-urbano.svg` or Bloomberg philanthropies logo; Angular or Vite hashed app bundles. Classic Fuse installs also have `fuse-splash-screen`, meta author `sergio@visorurbano.com`, and a public layer list at `/django/rest/v1/capas-mapa/`. Remix installs preload `/logos/visor-urbano.svg` and set `apple-mobile-web-app-title` to Visor Urbano. Newer Angular city builds use `<title>VisorUrbano {City}</title>` and `map/get_layers` (that path is in JavaScript, which FOFA does not index).

**Confirm:** GET the public map/licence UI and match Visor Urbano branding. Keep a tenant only when the public layer list names thematic datasets (WMS GetCapabilities, `/django/rest/v1/capas-mapa/`, or the map loader). One record per municipality tenant. Skip `www.visorguadalupe.com` (Proaxis Leaflet, not this product), `www.visorurbano.com` (marketing), `tramitesdigitales.guadalajara.gob.mx` (licence desk of the Guadalajara tenant), and Geoportal CAME on `geoportal.datacities.org` (same author email, different product title). The Guadalajara origin `visorurbano.guadalajara.gob.mx` is the reference install when it responds.

**FOFA** (checked 24 September 2026). `domain="visorurbano.com"` returned 6. `host="visorurbano"` returned 30 and is still the hostname sweep. `cert="visorurbano"` returned 0. `body="visor-urbano.svg"` and `body="logos/visor-urbano.svg"` returned 7 (La Cruz plus a bare IP and a hostname whose certificate does not match). `body="sergio@visorurbano.com"` returned 13. It confirmed Puerto Cortés and surfaced Chihuahua (`sigmun-visorurbano.mpiochih.gob.mx`), which `host="visorurbano"` did not return. `body="fuse-splash-screen" && title="Visor Urbano"` returned 9. `body="En Visor Urbano podrás conocer"` returned 4. `title="VisorUrbano"` returned 5 (Tepatitlán). `body="Logo Visor Urbano"`, `body="media/visor.png"`, and `body="django/rest/v1/capas-mapa"` returned 0 because those strings are in JavaScript. `body="/vutepa/"` and `body="municipal-layers"` are unrelated noise.

| Tool | Query |
|------|-------|
| Google | `"Visor Urbano" (catastro OR "uso de suelo" OR licencias) site:.gob.mx` |
| Google | `site:visorurbano.com` |
| Censys | `web.names: "visorurbano.com"` |
| FOFA | `domain="visorurbano.com"` |
| FOFA | `host="visorurbano"` |
| FOFA | `body="visor-urbano.svg"` |
| FOFA | `body="logos/visor-urbano.svg"` |
| FOFA | `body="sergio@visorurbano.com"` |
| FOFA | `body="fuse-splash-screen" && title="Visor Urbano"` |
| FOFA | `body="En Visor Urbano podrás conocer"` |
| FOFA | `title="VisorUrbano"` |
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
| FOFA | `body="Leaflet.GoogleMutant"` |

## GeoNube (`geonube`) {#geonube}

Cooperativa Cambalache hosted Leaflet/bootleaf map platform. Product: [cambalache.coop.ar/geonube](https://cambalache.coop.ar/geonube/). Distinct from Argentine municipal IDEs that do not load GeoNube assets.

**Signals:** hostname `geonube.com.ar` with path `/visor/{slug}`; scripts from `/bootleaf/` and `/leaflet/`; title often `Visor` or GeoNube. Custom domains (for example `nw.mercedes.gob.ar/geoportal`) count when they embed or link those visors.

**Confirm:** GET the visor slug (not `/visor/` with no slug, and not `/auth` alone). One record per municipality or organisation tenant, not one row per map inside the same tenant. Skip login-only private visors.

| Tool | Query |
|------|-------|
| Google | `site:geonube.com.ar/visor` |
| Google | `"GeoNube" (visor OR geoportal) (municipio OR municipalidad) site:.gob.ar` |
| Censys | `web.names: "geonube.com.ar"` |
| FOFA | `host="geonube.com.ar"` |
| FOFA | `body="geonube.com.ar/visor"` |
| crt.sh | `geonube.com.ar` |

## Sistema Geodados SaaS (`geodados`) {#geodados}

Brazilian municipal GIS SaaS. Vendor: [geodados.com.br/sistema](https://www.geodados.com.br/sistema). Distinct from ArcGIS Hub sites titled Geodados (Portugal) and from GeoNode `geodados.daee.sp.gov.br`.

**Signals:** hostname `{city}.geodados.com.br`; public catalog at `/Publico`; OpenLayers `/lib/ol/css/ol.css`; `acessoAnonimo = true`; “Sistema Geodados”; optional “Mapas Temáticos” / “Consulta de Viabilidade”.

**Confirm:** GET `/Publico` and match OpenLayers plus anonymous access. Staff login at the tenant root is not a catalog — skip it. Nonexistent city hosts fail DNS. One record per municipality. Skip `oracle.geodados.com.br` (internal) and `www.geodados.com.br` (marketing). Do **not** guess cities from the vendor’s “+200 municípios geoprocessados” mapping-services claim.

| Tool | Query |
|------|-------|
| Google | `site:geodados.com.br/Publico` |
| Google | `"Sistema Geodados" (Publico OR "Mapas Temáticos")` |
| Censys | `web.names: "geodados.com.br"` |
| FOFA | `host="geodados.com.br"` |
| FOFA | `body="acessoAnonimo"` |
| FOFA | `body="Sistema Geodados"` |
| crt.sh | `%.geodados.com.br` |

## Geopixel Cidades (`geopixel`) {#geopixel}

Brazilian municipal geointelligence SaaS. Vendor: [geopixel.com.br](https://geopixel.com.br/produtos/geopixel-cidades/). Distinct from ArcGIS Hub `geo.{city}.*.gov.br` portals.

**Signals:** hostname `{city}.geoportal.geopixel.com.br`; Next.js `/_next/static/` shell; `/api/pages` city config when the API is healthy. Older tenants: `{city}.geopixel.com.br/geopixelcidades-{city}/` (often a login wall). The current public app is `{city}.geopixel.com.br/geopixelcidades3/` or `{city}.geopx.com.br/geopixelcidades3/`, with `configurations.json` `serverPath` pointing at `geopixelcidades3_server`.

**Confirm:** The geoportal hostname is a **DNS wildcard** that returns the same Next.js HTML for nonexistent cities. Add a municipality only when `{city}.geopixel.com.br/geopixelcidades3/` or `{city}.geopx.com.br/geopixelcidades3/` is a live tenant whose public `/library` lists non-basemap themes. One record per city. Do not add arbitrary `*.geoportal.geopixel.com.br` hosts from HTTP 200 alone. Drop `*-alvara` permit apps, `flow.*` build hosts, anonymous-login failures, and libraries that contain only the Base Tree.

**FOFA** (checked 24 September 2026). `host="geoportal.geopixel.com.br"` returned 1 row. `domain="geopx.com.br"` returned 22. `domain="geopixel.com.br"` returned 331 and is the query that finds `{city}.geopixel.com.br` tenants; drop `flow.`, `client.`, `server.`, and bare IPs (the wildcard certificate). `cert="geopixel.com.br"` returned 336 and was the same wildcard, not extra catalogs. `body="geopixelcidades3"` returned 68 and mostly matched municipal websites that mention the product. `body="geopixelcidades"` returned 27 and included GeoSIAP login panels.

| Tool | Query |
|------|-------|
| Google | `site:geoportal.geopixel.com.br` |
| Google | `"Geopixel Cidades" (geoportal OR cadastro) site:.gov.br` |
| Censys | `web.names: "geoportal.geopixel.com.br"` |
| FOFA | `host="geoportal.geopixel.com.br"` |
| FOFA | `domain="geopx.com.br"` |
| FOFA | `domain="geopixel.com.br"` |
| FOFA | `body="geopixelcidades3"` |
| FOFA | `body="geopixelcidades"` |
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
| FOFA | `host="ctmgeo.com.br"` |
| FOFA | `body="index.ctm"` |
| crt.sh | `%.ctmgeo.com.br` |

## MapMap (`mapmap`) {#mapmap}

Brazilian municipal GIS SaaS (cadastre, master plan, citizen geoportal). Vendor: [mapmap.com.br](https://mapmap.com.br/). Distinct from [mapmap.ai](https://mapmap.ai/) routing APIs and from MapMap Cidadão civic-reporting PWAs.

**Signals:** hostname `{city}.mapmap.com.br`; Laravel `data-framework="laravel"` plus MapMap branding; public `/geo-portal`; citizen hub title/copy “Portal de atendimento ao cidadão”; optional `/plano-diretor` and `/portal-contribuinte/pvgi`.

**Confirm:** GET the tenant root or `/geo-portal` and match the Laravel MapMap shell plus a public geoportal. One record per municipality. Tenant list: [cidadao.mapmap.com.br/api/organizacoes-ativas](https://cidadao.mapmap.com.br/api/organizacoes-ativas). Skip `www.mapmap.com.br` (marketing), `app.mapmap.com.br` (staff cadastre), `tributario.mapmap.com.br`, `{city}.cidadao.mapmap.com.br` (issue reporter, not a catalog), `teste` / `demonstracao` / `staging` / `poc`, and `geoserver.mapmap.com.br`. HTTP 403 with title `Licença Suspensa` is not a catalog. The `*.mapmap.com.br` certificate is a wildcard — do **not** guess city hostnames.

| Tool | Query |
|------|-------|
| Google | `site:mapmap.com.br/geo-portal` |
| Google | `"Portal de atendimento ao cidadão" MapMap geoportal` |
| Censys | `web.names: "mapmap.com.br"` |
| FOFA | `host="mapmap.com.br"` |
| FOFA | `title="Portal de atendimento ao cidadão"` |
| crt.sh | `%.mapmap.com.br` |
| Vendor API | `https://cidadao.mapmap.com.br/api/organizacoes-ativas` |

## DRZ WebGIS (`drzwebgis`) {#drzwebgis}

Brazilian municipal cadastral WebGIS from DRZ Territórios Inteligentes (Plataforma SIG Web). Vendor: [drz.com.br](https://www.drz.com.br/). Public tenants live at `webgis.drz.com.br/{city}/`. Distinct from CTMGEO SigWEB (`ctmgeo`), Geodados SaaS (`geodados`), and Geopixel Cidades (`geopixel`).

**Signals:** path `webgis.drz.com.br/{city}/`; title `WebGIS | {City} - {UF}` or JS-set `WebGis - {City} - {UF}`; meta `Rodolfo` / `DRZ Geotecnologia`; OpenLayers plus lot/quadra/bairro search.

**Confirm:** GET the city path (HTTP; the hostname certificate does not match HTTPS) and match DRZ OpenLayers chrome plus a public cadastral layer list. Nonexistent slugs return nginx 404. One record per municipality. `add-single` builds `id` from hostname only, so write YAML with the city slug in `id` (pattern `webgisdrzcombr{city}`). Skip the nginx default root, `/drz/` clients map, Tomcat `/manager`, and `demo` / `docs` / `examples`. Do **not** brute-force Brazilian city names; use indexed paths (Wayback `webgis.drz.com.br/*`) and live GET.

| Tool | Query |
|------|-------|
| Google | `site:webgis.drz.com.br "WebGis" OR "WEBGIS"` |
| Google | `"webgis.drz.com.br" (cadastro OR lote OR zoneamento)` |
| Wayback | `webgis.drz.com.br/*` |
| Censys | `web.names: "webgis.drz.com.br"` |
| FOFA | `host="webgis.drz.com.br"` |

## GAUSS WebCity (`gausswebcity`) {#gausswebcity}

Gauss d.o.o. Tuzla MapStore-based municipal and cantonal geoportal (also marketed as GAUSS WebPresenter). Product: [gauss.ba/en/solutions/gauss-webcity](https://gauss.ba/en/solutions/gauss-webcity/). Public tenants live at `{org}.gis.ba` or a city host with `/webcity/` loading `dist/mapstore2.js`. Distinct from generic MapStore (`mapstore`) and from VertiGIS WebOffice tenants branded WebCity (`weboffice`).

**Signals:** title `WebCity` or `WebPresenter` plus GAUSS landing (`logo_gauss.png`, “Pristup za javnost”); path `/webcity/`; `dist/mapstore2.js`; hostname `*.gis.ba` (not `gis.ba` vendor home).

**Confirm:** GET the public tenant home or `/webcity/` and match MapStore2 plus GAUSS branding. One record per public tenant. Skip `https://gis.ba/webcity/` vendor demo, hiking/forum/edu hosts, and login-only `/registered/` shells. Do **not** set `mapstore` or `weboffice` on these tenants.

| Tool | Query |
|------|-------|
| Google | `"GAUSS WebCity" OR "logo_gauss" geoportal site:.ba` |
| Google | `inurl:/webcity/ (općina OR kantona) site:.ba` |
| Censys | `web.names: "gis.ba"` |
| FOFA | `domain="gis.ba"` |
| crt.sh | `%.gis.ba` |

## GISPLAN (`gisplan`) {#gisplan}

T-MAPY municipal web GIS (Spinbox / T-WIST gallery) for Slovak and Czech cities. Vendor: [tmapy.sk](https://www.tmapy.sk/verejna-sprava/mesta) / [tmapy.cz/gis4u](https://www.tmapy.cz/gis4u). Slovak tenants usually live at `{city}.gisplan.sk`, or a city custom domain that still loads `tmapy.svg` / Spinbox and public `/mapa/` apps (`gis.zilina.sk`, `mapy.banskabystrica.sk`, `gisplan.kosice.sk`). Czech GIS4U tenants live at `{muni}.gis4u.cz`; T-WIST galleries also live at `{city}.tmapserver.cz` and on city hosts (Nymburk Spinbox, Děčín, Chomutov, Frýdek-Místek, Mladá Boleslav, Hradec Králové, Jablonec) that load `ost/filebox/ug_hm.php` with `t-wist_ren` / `tmapy.svg` icons. Distinct from Romanian GISApp (`gisapp`), Kaliopa iObčina (`iobcina`), Geoportál GEPRO (`gepro`), TopGis GisOnline (`gisonline`), Mapotip (`mapotip`), CORA GEO CG WebGIS (`cgwebgis`), T-MAPY mOBEC (`mobec`), Georeal (`georeal`), and Geodeticca WEB GIS (`geodeticca`). Do **not** set `gisplan` on T-MAPY MapProxy (`services7.tmapserver.cz/mapproxy` is `mapproxy`).

**Signals:** title `GISPLAN mesta …`, `GIS mesta …`, or GIS4U geoportál; scripts/logo `tmapy.svg` / `008_t-wist_ren_g.svg` / Spinbox footer `© T-MAPY`; `ost/filebox/ug_hm.php`; or the newer T-WIST `/theme/square/scripts/lock.min.js`, `filterApps.js`, and `check-login.js` gallery; public app cards linking to `/mapa/`; optional staff login on the same gallery.

**Confirm:** GET the public tenant home and match T-MAPY / Spinbox / T-WIST plus at least one public map app. One record per municipality. Prefer the city custom domain when it serves the same gallery as `{slug}.gisplan.sk`. Skip login-only shells with no public app list. Do **not** set `gisplan` from a `gis.` hostname that is ArcGIS Hub or Experience Builder (Pezinok, Nitra `gis.nitra.sk`), from Georeal `/portal/Georeal.*` kraj CMS (`georeal`), from Geodeticca WEB GIS (`gis.{city}.sk` titled Geodeticca WEB GIS), from CORA GEO CG WebGIS (`webgis.{city}.sk`, title `WebGIS v2, CG`), from T-MAPY mOBEC (`mobec.sk/{slug}`), or from Czech city-domain `/theme/square/` + `/mapa/` GIS4U galleries (`gis4u`).

| Tool | Query |
|------|-------|
| Google | `"GISPLAN mesta" OR "GIS mesta" site:gisplan.sk` |
| Google | `site:gis4u.cz geoportál OR "T-WIST"` |
| Google | `"T-MAPY" (geoportál OR "mapový portál") site:.sk OR site:.cz` |
| Censys | `web.names: "gisplan.sk"` |
| FOFA | `domain="gisplan.sk"` |
| FOFA | `domain="gis4u.cz"` |
| FOFA | `domain="tmapserver.cz"` |
| FOFA | `body="tmapy.svg"` |
| FOFA | `body="ost/filebox/ug_hm.php"` |
| FOFA | `body="/theme/square/scripts/lock.min.js"` |
| FOFA | `body="tw-homeAppItem"` |
| FOFA | `body="008_t-wist_ren_g.svg"` |
| FOFA | `body="asyncProcessChecker.min.js"` |
| FOFA | `title="GISPLAN"` |
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
| FOFA | `domain="mobec.sk"` |
| FOFA | `body="tmapyn.svg"` |
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
| FOFA | `title="WebGIS v2, CG"` |
| Censys | `web.names: "webgis.trnava.sk"` |
| FOFA | `host="webgis.trnava.sk"` |

## Geodeticca WEB GIS (`geodeticca`) {#geodeticca}

GEODETICCA VISION municipal map client. Product: [geoinformatika](https://geodeticca.sk/index.php/produkty/geoinformatika/). Distinct from CORA GEO CG WebGIS (`cgwebgis`) and T-MAPY GISPLAN (`gisplan`).

**Signals:** title `Geodeticca WEB GIS`; host `gis.{city}.sk`; scripts `/js/config.js`, `/js/build/libs.js`, `/js/build/jquery-ext-min.js`.

**Confirm:** GET the public viewer and match the Geodeticca WEB GIS title plus `/js/build/libs.js`. One record per municipality. Do **not** set `geodeticca` from CG WebGIS (`webgis.{city}.sk`, title `WebGIS v2, CG`), GISPLAN Spinbox, or Michalovce `michalovce.web-gis.sk` (`app.bundle.js`).

| Tool | Query |
|------|-------|
| Google | `"Geodeticca WEB GIS" site:.sk` |
| Google | `site:gis.modra.sk OR site:gis.trebisov.sk OR site:gis.samorin.sk` |
| Censys | `web.endpoints.http.html_title: "Geodeticca WEB GIS"` |
| FOFA | `title="Geodeticca WEB GIS"` |
| FOFA | `body="Geodeticca"` |

## Geoportál GEPRO (`gepro`) {#gepro}

GEPRO municipal web GIS. Product: [Geoportál GEPRO](https://www.gepro.cz/produkty/geoportal/). Distinct from desktop MISYS and from T-MAPY GISPLAN (`gisplan`).

**Signals:** host `{city}.obce.gepro.cz`, `{city}.gepro.cz`, or `geoportal.gepro.cz/obce/{slug}`; title `Geoportál {City}`; scripts `/OUT/HTML/files/js/conf/start.min.js`, `/OUT/HTML/OL3/`, `gp.ol-ext`.

**Confirm:** GET the public viewer and match the `/OUT/HTML/` OpenLayers client. One record per municipality. Skip login-only intranet Geoportál GEPRO.

| Tool | Query |
|------|-------|
| Google | `site:obce.gepro.cz Geoportál` |
| Google | `"Geoportál" GEPRO (obec OR město) site:.cz` |
| Censys | `web.names: "gepro.cz"` |
| FOFA | `domain="gepro.cz"` |
| FOFA | `body="/OUT/HTML/OL3/"` |
| FOFA | `body="gp.ol-ext"` |
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
| FOFA | `domain="evald.ee"` |
| crt.sh | `evald.ee` |

## terGIS (`tergis`) {#tergis}

Latvian territorial-planning and public-engagement GIS (METRUM / TOPO DATI). Product: [tergis.lv](https://tergis.lv/). Distinct from generic QWC2 (`qwc2`) off `tergis.lv` and from the sibling pGIS product (`pgis.lv`).

**Signals:** host `{tenant}.tergis.lv`; HTML title `terGIS`, `TerGIS kartes`, or `Tergis.lv`; Angular SPA footer `terGIS v` plus `/api/v1/classifiers/layers`; some territorial-plan tenants use a QWC2 frontend (`/themes.json`, `QWC2App.js`) on the same domain.

**Confirm:** GET `https://{tenant}.tergis.lv/` and match the terGIS title or `/api/v1/classifiers/layers` JSON, or `/themes.json` on QWC2-frontend tenants. One record per public tenant subdomain. Do **not** add the marketing homepage `tergis.lv`. Do **not** set `qwc2` from a `*.tergis.lv` host (use `tergis`). Skip `401` (Ķekava) and `502` tenants until they recover.

| Tool | Query |
|------|-------|
| Google | `site:tergis.lv terGIS OR "teritorijas plānojums"` |
| Censys | `web.names: "tergis.lv"` |
| FOFA | `domain="tergis.lv"` |
| crt.sh | `%.tergis.lv` |

## TerraWeb (`terraweb`) {#terraweb}

Terraplan German municipal WebGIS. Product: [TerraWeb](https://www.terraplan.com/webgis/). Public tenants at `{tenant}.terragis.de` and on custom Kreis domains (`geoportal.lklg.net`, `geoportal.landkreisgoettingen.de`). Distinct from Latvian terGIS (`tergis`) and from Terria (`terria`).

**Signals:** hostname `*.terragis.de` or a custom domain loading `terraweb.js` / `terraweb-ol.js`; title `TerraWeb`, `TERRAWEB Geoportal`, or `Stadtplan Geoportal`; guest viewer `login-ol.htm?login=gast` (or a named public account such as `buergerauskunft`).

**Confirm:** GET the public launcher or `login-ol.htm?login=gast` and match TerraWeb / Terraplan branding plus an OpenLayers map. One record per public tenant, not per theme tile or desktop/tablet launcher. Do **not** add the marketing homepage `terragis.de`. Do **not** set `tergis` from `terragis.de`. Skip `auth.terragis.de` Keycloak, TerraSchüler / TerraIndividual apps, dead `*-qwc.terragis.de`, and staff `anmelden.htm` without a guest map. Wesermarsch aliases (`lkbra`, `lkwema`, `wesermarsch`) are one tenant.

| Tool | Query |
|------|-------|
| Google | `site:terragis.de TerraWeb OR Geoportal` |
| Google | `"Anmeldung TerraWeb" OR "TERRAWEB Geoportal" OR terraweb.js site:.de` |
| Censys | `web.names: "terragis.de"` |
| FOFA | `domain="terragis.de"` |
| FOFA | `body="terraweb.js"` |
| crt.sh | `%.terragis.de` |

## TerraVisu (`terravisu`) {#terravisu}

Open-source territorial map observatory from Makina Corpus / Autonomens (Terralego). Product: [TerraVisu](https://makina-corpus.com/sig-cartographie/terravisu-organisez-vos-donnees-territoriales), source: [Terralego/TerraVisu](https://github.com/Terralego/TerraVisu), docs: [terravisu.readthedocs.io](https://terravisu.readthedocs.io/). Public examples on the GitHub README and Makina Corpus [TerraVisu references](https://makina-corpus.com/references?tag=TerraVisu). Distinct from older Terralego Angular apps on `*.terralego.com` (CCHA, DDT65) that do not expose `/api/settings/frontend`.

**Signals:** JSON `/api/settings/frontend` with a TerraVisu title; `/env.json` (`API_HOST`, `VIEW_ROOT_PATH`); `/api/geolayer/scene/` scene list; Next.js `/view/{slug}` paths; `/config/` Django admin titled “TerraVisu: Configuration”.

**Confirm:** GET `/api/settings/frontend` and `/api/geolayer/scene/` on the public origin. One record per public tenant, not per `/view/` theme or data.gouv.fr reuse of the same demo. Skip vendor demos (`demo-terravisu-territoires.makina-corpus.com`, `demo-*.solutions-territoriales.fr`, TerraObs demo), `/config/` login, `401` observatories (Vallée Sud), dead SeineYonne hosts, cultural/non-catalog maps (Le Son Unique), and tile CDNs (`*-tiles-visu.sud-foncier-eco.fr`).

| Tool | Query |
|------|-------|
| Google | `"TerraVisu" (observatoire OR cartographie) site:.fr -site:github.com -site:makina-corpus.com` |
| Google | `"Makina Corpus" TerraVisu (observatoire OR "Sud Foncier")` |
| Censys | `web.endpoints.http.body: "/api/geolayer/scene/"` |
| FOFA | `body="/api/geolayer/scene/"` |
| FOFA | `host="sud-foncier-eco.fr"` |

## Mon Territoire Carto (`monterritoirecarto`) {#monterritoirecarto}

SOGEFI French municipal web GIS (cadastre, urbanisme, fibre, thematic public maps). Product: [Mon Territoire Carto](https://www.sogefi-sig.com/accueil/mon-territoire/carto/). Public examples: [Ils nous font confiance](https://www.sogefi-sig.com/presentation-et-valeurs/ils-nous-font-confiance/). Distinct from Solutions & Territoire (Atelier Fiscal / Atelier Économique) and from GeoNetwork on `smiddest-catalogue.monterritoire.fr`.

**Signals:** host `carto.monterritoire.fr` with `map.php?instance=` or `?instance=`; branded `{org}.monterritoire.fr` loading `cdn.sogefi-web.com` Carto assets; title `Mon Territoire Carto` / `Instance Carto` / `Guyane SIG - MonTerritoire Carto`; user guide `/static/manuel/manuel-carto.pdf`.

**Confirm:** GET the public instance URL and match the Carto viewer (layer tree / legend, SOGEFI assets) without a login form. One record per public `instance=` or branded host, not per lat/lng/zoom share link. Skip `carto.monterritoire.fr` with no instance (staff login), Mon Territoire Voirie / TLPE logins, Martell/private tenants, preprod/stats/fonts hosts, partner Découverte skins (`cosoluce.monterritoire.fr`), empty EPF shells (`gisementfoncier.monterritoire.fr`), and fibre testers that are not Carto (`carte.numerique28.fr`). `www.monterritoire.fr` / `decouverte.monterritoire.fr` are one national Découverte catalog.

| Tool | Query |
|------|-------|
| Google | `"carto.monterritoire.fr/map.php?instance="` |
| Google | `"Mon Territoire Carto" site:.fr (urbanisme OR PLU OR cadastre)` |
| Google | `site:sogefi-sig.com "instances" Carto` |
| Censys | `web.names: "monterritoire.fr"` |
| FOFA | `host="carto.monterritoire.fr"` |
| FOFA | `domain="monterritoire.fr"` |
| FOFA | `body="cdn.sogefi-web.com"` |
| crt.sh | `%.monterritoire.fr` |

## Pozi (`pozi`) {#pozi}

Australian-owned council web GIS (Groundtruth / Pozi). Product: [pozi.com](https://pozi.com/). Distinct from IntraMaps Public (`intramaps`), Exponare (`exponare`), and Spectrum Spatial Analyst (`spectrumspatial`).

**Signals:** host `{council}.pozi.com`; HTML title `Pozi Web Map`; shared CloudFront SPA `assets/entry-app-*.js`.

**Confirm:** GET `https://{council}.pozi.com/` and match the Pozi Web Map title. One record per public council subdomain (`{name}-public` is the public tenant). Do **not** add the marketing homepage `pozi.com`. Do **not** set `intramaps` or `exponare` from a `pozi.com` host.

| Tool | Query |
|------|-------|
| Google | `site:pozi.com "Pozi Web Map"` |
| Google | `"Pozi" (council OR shire) map site:.gov.au` |
| Censys | `web.names: "pozi.com"` |
| FOFA | `domain="pozi.com"` |
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
| FOFA | `body="jmap.min.js"` |
| Censys | `web.names: "jmaponline.net"` |
| FOFA | `domain="jmaponline.net"` |

## GIS Cloud (`giscloud`) {#giscloud}

Hosted web GIS. Product: [giscloud.com](https://www.giscloud.com/). Distinct from generic Leaflet viewers and from MuniSight (`web.munisight.com`).

**Signals:** host `{city}.giscloud.com`; scripts `assets.giscloud.com` (`compiled-smart.js`, `api.js`).

**Confirm:** GET `https://{city}.giscloud.com/` and match GIS Cloud assets. One record per public tenant subdomain. Do **not** add the marketing homepage. Skip Map Editor login, product/demo tenants (`mapportal`, `maplim`, `crowdsource-demo`, `dashboard`, `graphs`, `geocoding`), empty test maps, and login-walled orgs.

| Tool | Query |
|------|-------|
| Google | `site:giscloud.com (GIS OR map) -www.giscloud.com` |
| Censys | `web.names: "giscloud.com"` |
| FOFA | `domain="giscloud.com"` |
| crt.sh | `%.giscloud.com` |

## MRF Web Map (`mrf`) {#mrf}

MRF Geosystems municipal GIS. Product: [MRF Web Map](https://www.mrf.com/product-details/MRF-Municipal-Solutions/MRF-Web-Map-Platform.html). Distinct from GIS Cloud (`giscloud`) and from MuniSight/Catalis login portals.

**Signals:** host `{county}.mrf.com` or a city host loading `js/lib/mrf/`; title `MRF Web Disclaimer`.

**Confirm:** GET the public map (guest / disclaimer) and match `js/lib/mrf/`. One record per public tenant. Do **not** set `mrf` from `web.munisight.com` Login.aspx (`munisight`). Skip the marketing homepage.

| Tool | Query |
|------|-------|
| Google | `"MRF Web Disclaimer" OR site:mrf.com Map` |
| Censys | `web.names: "mrf.com"` |
| FOFA | `domain="mrf.com"` |
| FOFA | `title="MRF Web Disclaimer"` |
| FOFA | `body="js/lib/mrf/"` |

## MuniSight (`munisight`) {#munisight}

Catalis GIS WebMap (formerly MuniSight). Product: [catalisgov.com](https://catalisgov.com/public-works/geographic-information-system/). Distinct from MRF Web Map (`mrf`) and from generic GeoMedia WebMap (`geomediawebmap`).

**Signals:** `web.munisight.com/{Tenant}`, `app.munisight.com/{Tenant}`, or `{tenant}.gis.catalisgov.ca`; `Login.aspx`; `App_Themes/Catalis`; CloudFront JS `3.9.x`.

**Confirm:** GET the tenant URL and match Catalis/MuniSight Login.aspx. Keep the record only when a public guest map lists layers (parcels, roads, utilities, land use). One record per municipality tenant. Do **not** set `mrf` or `geomediawebmap` from this host. Skip the marketing homepage, `*.web.catalisgov.ca` municipal CMS sites, and `MunisightDemo`.

**FOFA** (checked 24 September 2026). `host="munisight.com"` and `domain="munisight.com"` (54) list the platform hosts, not `{Tenant}` paths. `cert="munisight.com"` (48) was the wildcard certificate on bare IPs. `domain="gis.catalisgov.ca"` (10) and `cert="gis.catalisgov.ca"` (7) are the queries that find `{tenant}.gis.catalisgov.ca` catalogs. `domain="catalisgov.ca"` (107) is mostly `*.web.catalisgov.ca` city websites. `body="App_Themes/Catalis"`, `body="catalisLogo.png"`, `body="AAGUtility.min.js"`, and `body="dlzdsy0pvzhif.cloudfront.net"` returned 0. `body="app.munisight.com"` (17) and `body="web.munisight.com"` (5) match municipal pages that link to path tenants; `body="MuniSight"` (12) is the same kind of mention search.

| Tool | Query |
|------|-------|
| Google | `site:web.munisight.com Login GIS` |
| Google | `"Log in as guest" MuniSight` |
| crt.sh | `%.munisight.com` |
| crt.sh | `%.gis.catalisgov.ca` |
| Censys | `web.names: "munisight.com"` |
| FOFA | `domain="gis.catalisgov.ca"` |
| FOFA | `cert="gis.catalisgov.ca"` |
| FOFA | `body="app.munisight.com"` |
| FOFA | `body="web.munisight.com"` |
| FOFA | `body="MuniSight"` |

## GeoMedia SmartClient Public Maps (`publicmaps`) {#publicmaps}

GIS Quadrat hosted Hexagon GeoMedia SmartClient public viewer. Product: [gisquadrat.com/gis-software/public-maps](https://www.gisquadrat.com/gis-software/public-maps/). Distinct from GeoMedia WebMap Geospatial Portal (`geomediawebmap`) and from GIS Quadrat ERDAS APOLLO (`erdasapollo`) on `apollo.gisquadrat.com`.

**Signals:** `publicmaps.gisquadrat.com/BP/WEPM.aspx?site=GMSC&project={TOWN}`; title `GeoMedia SmartClient Public Maps`; `ig.publicmaps.application.min.js`; `/GMSC/PUBLIC/Configuration`.

**Confirm:** GET the WEPM.aspx tenant URL and match the Public Maps title plus `ig.publicmaps`. One record per municipal `project=` tenant. Do **not** set `geomediawebmap` or `erdasapollo` from this host. Skip the marketing homepage and the retired `gis-klagenfurt.at` WEPM host (replaced by Klagenfurt’s HxDR digital twin).

| Tool | Query |
|------|-------|
| Google | `"GeoMedia SmartClient Public Maps" OR inurl:WEPM.aspx site:publicmaps.gisquadrat.com` |
| Google | `"ig.publicmaps.application.min.js"` |
| Censys | `web.names: "publicmaps.gisquadrat.com"` |
| FOFA | `host="publicmaps.gisquadrat.com"` |
| FOFA | `title="GeoMedia SmartClient Public Maps"` |
| FOFA | `body="ig.publicmaps.application.min.js"` |

## SIT WebGis (`sitwebgis`) {#sitwebgis}

SIT Servizi di Informazione Territoriale municipal GIS hosted at `webgis.sit-puglia.it`. Distinct from Regione Puglia GeoNetwork (`geonetwork` on `repertorio.sit.puglia.it`), Lizmap (`lizmap`), Spectrum Spatial Analyst (`spectrumspatial`), and GeneGIS PAGIS (`genegis`).

**Signals:** `webgis.sit-puglia.it/{comune}/`; title `WebGis {Town}` with `ng-app="WebApp"` and `core/lib/openlayers/js/ol.js`; or title `SIT-{TOWN}` / `SIT - {TOWN}` with Angular CLI bundles and `ol-attribution-hotfix.js`.

**Confirm:** GET the comune path and match the SIT WebGis title plus OpenLayers/Angular assets. One record per municipal tenant. Do **not** set `geonetwork` from this host. Skip the marketing homepage and stale slugs (`/mola`, `/potenza`) that 404.

| Tool | Query |
|------|-------|
| Google | `site:webgis.sit-puglia.it "WebGis" OR "SIT-"` |
| Google | `"ng-app=\"WebApp\"" ol.js site:webgis.sit-puglia.it` |
| Censys | `web.names: "webgis.sit-puglia.it"` |
| FOFA | `host="webgis.sit-puglia.it"` |

## p.mapper (`pmapper`) {#pmapper}

Open-source PHP/MapScript frontend for MapServer. Project: [p.mapper](https://sourceforge.net/projects/pmapper/). Distinct from UMN MapServer as the public catalog (`mapserver`), Lizmap (`lizmap`), and Mapbender (`mapbender`).

**Signals:** path `/pmapper/` or `/pmapper-4.2.0/`; Calabria SETIN tenants `{city}.geo-portale.it`; HTML mentioning p.mapper.

**Confirm:** GET the public UI and match `/pmapper`. One record per municipality or SIT, not per layer. Do **not** set `mapserver` from a p.mapper UI. Do not add a second MapServer catalog on the same host.

| Tool | Query |
|------|-------|
| Google | `inurl:pmapper-4.2.0 OR inurl:/pmapper/ (geoportale OR WebGIS)` |
| Google | `site:geo-portale.it Geoportale` |
| Censys | `web.endpoints.http.body: "pmapper-4.2.0"` |
| FOFA | `body="pmapper-4.2.0"` |
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
| FOFA | `domain="digitalmapcentral.com"` |

## MS-GIS (`msgis`) {#msgis}

Lower Austria municipal GeoInformation viewer. Distinct from Masterportal (`masterportal`), touvia.MAPS (`touviamaps`), and VC Map (`vcmap`).

**Signals:** host `{city}.msgis.net`; HTML title `{City} GeoInformation`.

**Confirm:** GET `https://{city}.msgis.net/` and match the GeoInformation title. One record per municipality subdomain. Do not add the marketing homepage.

| Tool | Query |
|------|-------|
| Google | `site:msgis.net GeoInformation` |
| Censys | `web.names: "msgis.net"` |
| FOFA | `domain="msgis.net"` |
| crt.sh | `%.msgis.net` |

## Weave (`weave`) {#weave}

Cohga municipal HTML5 web GIS used by Australian councils. Product: [cohga.com](https://www.cohga.com/solutions/council-information-management/). Distinct from IntraMaps Public (`intramaps`), Exponare (`exponare`), Pozi (`pozi`), and Spectrum Spatial Analyst (`spectrumspatial`).

**Signals:** HTML title `Weave Map`; webpack `app.*.js` client (often with `vendor-ol.*.js`). Hosted on the council domain, not a shared SaaS hostname.

**Confirm:** GET the public map and match title Weave Map. One record per council viewer. Do **not** set `weave` from GeneWeaver, “weaves together” copy, or IntraMaps/Pozi.

| Tool | Query |
|------|-------|
| Google | `intitle:"Weave Map" (council OR GIS) site:.gov.au` |
| Google | `"Weave Map" Cohga OR Geoplex` |
| Censys | `web.endpoints.http.html_title: "Weave Map"` |
| FOFA | `title="Weave Map"` |

## OVIE (`ovie`) {#ovie}

INEGI Oficina Virtual de Información Económica municipal economic GIS. Source: [git.inegi.org.mx/ovie/ovie-client](https://git.inegi.org.mx/ovie/ovie-client). Distinct from Mapa Digital de México / MxSIG (`mxsig`, product page [inegi.org.mx/servicios/mxsig.html](https://www.inegi.org.mx/servicios/mxsig.html)) and from generic OpenLayers copies.

**Signals:** title OVIE or Oficina Virtual de Información Económica; scripts `js/libs/OpenLayers/OL.js`, Materialize, html2canvas, canvg, jsPdf.

**Confirm:** GET the public viewer and match the OpenLayers `/js/libs/` stack. One record per municipality or state OVIE. Do **not** set `ovie` from Mission Viejo `geoviewer.io` or hostnames that merely contain `ovie`. Do **not** set `ovie` on INEGI Gaia `/mdm6/` (`mxsig`).

[index.html](https://git.inegi.org.mx/ovie/ovie-client/-/blob/master/index.html) titles the app `Oficina Virtual de Información Económica CDMX`. The client is published on INEGI GitLab, not GitHub, so code search for `js/libs/jquery.ntm/js/jquery.ntm.js` returns no repositories. GitHub code search for the title phrase finds municipal sites that link a deployment (IMPLAN Torreón points at `http://177.244.42.17/ovie-torreon/`).

`body="js/libs/jquery.ntm/js/jquery.ntm.js"` is the index.html script that only this client ships (24 hosts in September 2026). `body="js/libs/jsPdf/jsPdf.js"` is the same file but also matches unrelated apps (Monsieur Store, Gini, Provalert). `body="js/libs/OpenLayers/OL.js"` matches German museum databases — do not use that path alone. The title phrase also matches marketing pages that are not the viewer (IIEG, SEDECO CDMX, Morelia’s citizen portal).

| Tool | Query |
|------|-------|
| GitHub | `"Oficina Virtual de Información Económica"` (deployment links in municipal sites; the client repo is not on GitHub) |
| GitHub | `js/libs/jquery.ntm/js/jquery.ntm.js filename:index.html` |
| Google | `"OVIE" OR "Oficina Virtual de Información Económica" IMPLAN (visor OR mapa)` |
| Google | `intitle:OVIE OpenLayers site:.gob.mx` |
| Censys | `web.endpoints.http.body: "js/libs/jquery.ntm/js/jquery.ntm.js"` |
| FOFA | `body="js/libs/jquery.ntm/js/jquery.ntm.js"` |
| FOFA | `body="Oficina Virtual de Información Económica"` |
| FOFA | `title="OVIE" && country="MX"` |

## SOFTPRO (`softpro`) {#softpro}

Ukrainian urban-planning cadastre GIS (SOFTPRO: Містобудівний кадастр). Product: [cadastre.com.ua](https://cadastre.com.ua/). Distinct from the state Urban Planning Cadastre (`kadastr.gov.ua`) and StateGeoCadastre (`map.land.gov.ua`).

**Signals:** host `{city}.cadastre.com.ua`; page text or footer link identifying SOFTPRO; Tailwind `/assets/index-*.js` geoportal or older `/js/locale/ua.js` client (sometimes with `/assets/image/intro-icon.svg`).

**Confirm:** GET the public geoportal and match SOFTPRO in HTML. One record per community or oblast portal. Do **not** set `softpro` from `kadastr.gov.ua` or `map.land.gov.ua`.

| Tool | Query |
|------|-------|
| Google | `site:cadastre.com.ua` OR `"SOFTPRO" "містобудівний" геопортал` |
| Google | `"SOFTPRO·Містобудівний кадастр" OR "платформі SOFTPRO"` |
| Censys | `web.names: "cadastre.com.ua"` |
| FOFA | `domain="cadastre.com.ua"` |

## MxSIG (`mxsig`) {#mxsig}

INEGI Mapa Digital de México V6 / MxSIG. Product: [inegi.org.mx/servicios/mxsig.html](https://www.inegi.org.mx/servicios/mxsig.html). Distinct from OVIE (`ovie`).

**Signals:** path `/mdm6/` or `/mxsig2/`; title `Mapa Digital de México`; scripts `js/frameworks/amplify/amplify.js`, `lz-string`, jquery 1.9.

**Confirm:** GET the viewer and match amplify.js + MDM title. One record per public MDM6/MxSIG map, not the indicators CMS on the same host. Do **not** set `mxsig` on OVIE.

[index.html](https://github.com/MxSIG/mxsig/blob/master/mxsig/index.html) links `mdm6ico.png` (52 hosts in September 2026, including a page titled SMIEG Valle de Santiago). `body="Mapa Digital de México"` matched 61. The first hits are real viewers; a later hit is the directory `www.allabord.com`, so keep the title as the wider query.

| Tool | Query |
|------|-------|
| Google | `inurl:/mdm6/ OR inurl:/mxsig2/ "Mapa Digital"` |
| Google | `"MxSIG" OR "Mapa Digital de México V6" visor` |
| Censys | `web.endpoints.http.body: "mdm6ico.png"` |
| FOFA | `body="mdm6ico.png"` |
| Censys | `web.endpoints.http.body: "Mapa Digital de México"` |
| FOFA | `body="Mapa Digital de México"` |

## GisOnline (`gisonline`) {#gisonline}

TopGis municipal map application. Product: [gisonline.cz](https://www.gisonline.cz/). Distinct from T-MAPY GISPLAN (`gisplan`) and Geoportál GEPRO (`gepro`).

**Signals:** host `app.gisonline.cz/{city}`; title `{City} | Mapová aplikace GisOnline.cz`; script `/app-*.min.js`; copyright TopGis.

**Confirm:** GET `https://app.gisonline.cz/{city}` and match the GisOnline title (not the branded error page alone). One record per city slug. Skip the TopGis marketing site.

| Tool | Query |
|------|-------|
| Google | `site:app.gisonline.cz "Mapová aplikace GisOnline"` |
| Google | `"GisOnline.cz" (město OR obec) mapa` |
| Censys | `web.names: "gisonline.cz"` |
| FOFA | `domain="gisonline.cz"` |
| FOFA | `title="Mapová aplikace GisOnline"` |
| FOFA | `body="GisOnline.cz"` |
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
| FOFA | `domain="k5mapserver.cz"` |
| FOFA | `body="K5MapServer"` |
| crt.sh | `%.k5mapserver.cz` |

## Marushka (`marushka`) {#marushka}

GEOVAP map application server. Product: [Marushka](https://www.geovap.com/cs/marushka). Distinct from T-MAPY GISPLAN (`gisplan`), Geoportál GEPRO (`gepro`), and Georeal kraj CMS (`georeal`).

**Signals:** HTML title `Marushka - Mapový aplikační server`; script `js/zipped.js`; path `/marushka/` or `/marushka_ver/`; newer HTML clients load Blazor plus `js/marushka.js`.

**Confirm:** GET the public map UI and match Marushka in the title or `zipped.js` / `marushka.js`. One record per city installation, not per themed project. Skip GEOVAP marketing pages. GEOVAP MyCity / webportal galleries that launch `/MarushkaPublic/default.aspx` or `/MarushkaGP4/` (title `Marushka - Mapový aplikační server`) are `marushka`.

| Tool | Query |
|------|-------|
| Google | `intitle:"Marushka - Mapový aplikační server"` |
| Google | `inurl:marushka OR inurl:marushka_ver (geoportál OR GIS) site:.cz` |
| Censys | `web.endpoints.http.html_title: "Marushka - Mapový aplikační server"` |
| FOFA | `title="Marushka - Mapový aplikační server"` |

## Georeal (`georeal`) {#georeal}

GEOREAL OrchardCore CMS for Czech kraj DTM and geoportal sites. Product: [georeal.cz GIS](https://www.georeal.cz/sluzby/gis). Distinct from T-MAPY GISPLAN (`gisplan`), Geoportál GEPRO (`gepro`), and GEOVAP Marushka (`marushka`).

**Signals:** path `/portal/`; script `/portal/Georeal.Cards/Apps/card-container.min.js`; optional `Georeal.UzemniPlanovani` and `IsDTMKraj*` theme.

**Confirm:** GET `{host}/portal/` and match `Georeal.Cards`. One record per public DTM or geoportal product (Plzeň has both). Do **not** set `georeal` from an older `/portal/Themes/Metro/` city CMS without `Georeal.Cards` (Kadaň), from Nuxt DTM shells (`portal.dtm-praha-sck.cz`), from JSF `dmvs-gateway` (`uap.olkraj.cz`), or from ArcGIS REST kraj maps (Vysočina). Do **not** set `gisplan` or `marushka` from `Georeal.Cards`.

| Tool | Query |
|------|-------|
| Google | `"Georeal.Cards" OR "IsDTMKraj" (geoportál OR DTM) site:.cz` |
| Google | `inurl:/portal/ (DTM OR geoportál) (kraj OR kraje) site:.cz` |
| Censys | `web.html: "Georeal.Cards"` |
| FOFA | `body="Georeal.Cards"` |

## Mapotip (`mapotip`) {#mapotip}

Czech municipal web map portal (cadastre, DTM, pasports). Product: [mapotip.cz](https://www.mapotip.cz/). Distinct from T-MAPY GISPLAN (`gisplan`), Geoportál GEPRO (`gepro`), and TopGis GisOnline (`gisonline`).

**Signals:** host `portal.mapotip.cz/{municipality}`; HTML title `Mapotip`; script `/map/index-*.js`.

**Confirm:** GET the public tenant and match title Mapotip plus `/map/index-`. One record per municipality slug. Skip `portal.mapotip.cz/demo` and the marketing site.

| Tool | Query |
|------|-------|
| Google | `site:portal.mapotip.cz Mapotip` |
| Google | `"Mapotip" (obec OR město) (geoportál OR "mapový portál")` |
| Censys | `web.names: "mapotip.cz"` |
| FOFA | `domain="mapotip.cz"` |
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
| FOFA | `domain="gisserver.de"` |
| crt.sh | `gisserver.de` |

## iObčina (`iobcina`) {#iobcina}

Kaliopa cloud municipal GIS (Croatian brand iOpćina). Site: [kaliopa.si/iobcina](https://www.kaliopa.si/iobcina/). Distinct from Romanian GISApp (`gisapp`).

**Signals:** host `gis.iobcina.si` or `www.iopcina.hr`; ASP.NET `/gisapp/Default.aspx?a={tenant}`. The public viewer loads `/mapguide/js/ext3/resources/css/xtheme-iobcina.css`. The login shell loads `Content/Prijava-iobcina.css` and posts `#ddlSelApp`.

**Confirm:** GET `/gisapp/Default.aspx?a={tenant}` and keep the tenant only when the response stays on that viewer (title is the municipal GIS, not `login.aspx`). One record per municipality or county tenant, plus the Kaliopa hub if it is a separate public catalog. Drop login-only tenants (`Makarska`, `geogrupa` on 24 September 2026) and the sibling Kaliopa login portals iKomunala (`ikomunala.si`) and iSlovenija (`islovenija.si`).

Tenant lists, not FOFA host rows: [gis.iobcina.si/gisapp/Vstopna.aspx](https://gis.iobcina.si/gisapp/Vstopna.aspx) (212 Slovenian municipalities) and [www.iopcina.hr/gisapp/Vstopna.aspx](https://www.iopcina.hr/gisapp/Vstopna.aspx) (Croatian `#ddlSelApp`). FOFA indexes the login host, not each `?a=` tenant.

`body="xtheme-iobcina.css"` matched 3 hosts on 24 September 2026, all `iobcina.si`. `body="Prijava-iobcina.css"` matched the same 3. `body="kaliopa_logo/style.css"` matched 8, adding only the iKomunala and iSlovenija login portals. `host="www.iopcina.hr"` matched 0; `domain="iopcina.hr"` matched 5 and every row was `mail.iopcina.hr`. `body="Kaliopa"` is not usable (213 hosts, mostly hotels and news sites). `body="/gisapp/Default.aspx"` (72) and `body="gisapp/login.aspx?a="` (150) are municipal homepages that link to an already-registered tenant.

| Tool | Query |
|------|-------|
| Google | `inurl:/gisapp/Default.aspx iobcina OR iopcina` |
| Google | `"iObčina" OR iOpćina GIS` |
| Censys | `web.names: "iobcina.si"` |
| FOFA | `body="xtheme-iobcina.css"` |
| FOFA | `body="Prijava-iobcina.css"` |
| FOFA | `body="kaliopa_logo/style.css"` |
| FOFA | `body="gisapp/login.aspx?a="` |
| crt.sh | `%.iobcina.si` |

## Astun iShare (`ishare`) {#ishare}

UK local-government public mapping portal (Astun Technology). Product: [astuntechnology.com/ishare](https://www.astuntechnology.com/ishare/). Distinct from Cadcorp SIS WebMap (`cadcorp`) and from the INDEPTH iShare **microdata** catalog. Live examples: [maps.trafford.gov.uk/mycouncil.aspx](https://maps.trafford.gov.uk/mycouncil.aspx), [maps.easthants.gov.uk/mycouncil.aspx](https://maps.easthants.gov.uk/mycouncil.aspx), [mymaps.walsall.gov.uk](https://mymaps.walsall.gov.uk/).

**Signals:** footer “Powered by iShare”; paths `/mymaps.aspx`, `/mycouncil.aspx`, `/myhouse.aspx`; Astun branding.

**Confirm:** GET the public My Maps / Find my nearest UI. One record per authority portal, not per map layer. Skip intranet-only iShare GIS.

| Tool | Query |
|------|-------|
| Google | `"Powered by iShare" (maps OR "my house" OR geoportal) site:.gov.uk` |
| Google | `inurl:mymaps.aspx OR inurl:myhouse.aspx iShare` |
| Censys | `web.endpoints.http.body: "Powered by iShare"` |
| FOFA | `body="Powered by iShare"` |

## Cadcorp SIS WebMap (`cadcorp`) {#cadcorp}

Cadcorp (NEC) public web GIS. Product: [cadcorp.com](https://www.cadcorp.com). Distinct from disy Cadenza (`cadenza`) and from Astun iShare (`ishare`).

**Signals:** SIS WebMap / Web Map Layers / GeognoSIS branding; Cadcorp in HTML or GetCapabilities.

**Confirm:** GET the public web map and match Cadcorp/GeognoSIS. One record per public portal. Skip intranet WebMap Editor.

| Tool | Query |
|------|-------|
| Google | `"Cadcorp" OR "SIS WebMap" OR GeognoSIS (geoportal OR "web map") site:.gov.uk` |
| Google | `"Web Map Layers" Cadcorp` |
| Censys | `web.endpoints.http.body: "Cadcorp"` |
| FOFA | `body="Cadcorp"` |

## StatMap Earthlight (`earthlight`) {#earthlight}

UK local-government browser GIS (StatMap). Product: [evo.statmap.co.uk/earthlight-evo](https://evo.statmap.co.uk/earthlight-evo/). Public Earthlight Portal / Earthlight Public tenants (and Aurora embeds of the same stack). Distinct from Astun iShare (`ishare`) and Cadcorp SIS WebMap (`cadcorp`). Live examples: [miltonkeynes.statmap.co.uk/map/map.html?login=ExternalELP](https://miltonkeynes.statmap.co.uk/map/map.html?login=ExternalELP), [maps.bcpcouncil.gov.uk/map/map.html?login=ExternalELP](https://maps.bcpcouncil.gov.uk/map/map.html?login=ExternalELP).

**Signals:** HTML title `StatMap Earthlight`; path `/map/map.html` with `login=ExternalELP`; host `{authority}.statmap.co.uk` or council `maps.{council}.gov.uk/map/`; Aurora.svc embeds on the same `/map/` app.

**Confirm:** GET `/map/map.html?login=ExternalELP` and match the Earthlight title. One record per public tenant, not per Aurora script or map layer. Skip intranet-only Earthlight Enterprise, HorizoNext planning/case portals (`*-publicportal.statmap.co.uk/horizonext`), and hosts that only serve the IIS default page.

| Tool | Query |
|------|-------|
| Google | `"StatMap Earthlight" OR inurl:statmap.co.uk/map/map.html` |
| Google | `"login=ExternalELP" Earthlight (maps OR GIS) site:.gov.uk` |
| Censys | `web.endpoints.http.html_title: "StatMap Earthlight"` |
| FOFA | `title="StatMap Earthlight"` |
| crt.sh | `%.statmap.co.uk` (wildcard cert; still probe named tenants) |

## Geometa (`geometa`) {#geometa}

Gems Development urban-planning GIS and public GIS OGD geoportals (Agate). Product: [geometa.ru](https://geometa.ru/), module docs [geometa.ru/module/agate](https://geometa.ru/module/agate/). Distinct from unrelated “GeoMeta” catalog products. Typical Russian regional tenants: `portal-gisogd.*`, `agate.*`.

**Signals:** HTML title «Портал ГИСОГД»; short body “agat doesn’t work without JavaScript”; `/agate_` paths; Geometa / Agate / Gems Development branding.

**Confirm:** GET the public portal and match Agate. One record per public tenant. Skip login-only document workflows. Do **not** set `software.id: geometa` from a `gisogd.` hostname alone — sites without Agate strings stay `custom`.

| Tool | Query |
|------|-------|
| Google | `"Портал ГИСОГД" OR inurl:portal-gisogd OR inurl:agate (геопортал OR ГИСОГД) site:.ru` |
| Google | `"agat doesn’t work without JavaScript" OR "agat doesn't work without JavaScript"` |
| Censys | `web.endpoints.http.body: "agat doesn’t work without JavaScript"` |
| FOFA | `body="agat doesn’t work without JavaScript"` |
| Censys | `web.names: "portal-gisogd"` |
| FOFA | `host="portal-gisogd"` |

## Argenmap (`argenmap`) {#argenmap}

Open-source Leaflet viewer from Argentina's Instituto Geográfico Nacional. Product and source: [ign-argentina/argenmap](https://github.com/ign-argentina/argenmap).

**Signals:** self-hosted `src/js/app.js` plus the Argenmap `src/js/` modules and JSON layer configuration; `constants.js` may retain the `Argenmap - Instituto Geográfico Nacional` title or an `ign-geoportal-*` template name.

**Confirm:** GET the viewer and match the Argenmap source tree or retained template identifiers, not Leaflet alone. One record per public institutional deployment. Do **not** set `argenmap` on generic Leaflet viewers that only share common libraries. Do **not** set `argenmap` on IGN `mapamuni.ign.gob.ar` without those source-tree signals.

[index.html](https://github.com/ign-argentina/argenmap/blob/master/index.html) loads `src/js/components/openfiles/openfiles.css` (16 hosts in September 2026, including `remonta.ign.gob.ar` and `mapa.idera.gob.ar`). The same file describes the viewer as `Argenmap es un visor de mapas interactivo` (5 hosts, including `mapa.ign.gob.ar`). `body="Argenmap - Instituto Geográfico Nacional"` matched 0.

| Tool | Query |
|------|-------|
| Google | `"Argenmap" (IDE OR geoportal OR visualizador) -site:github.com` |
| Google | `"ign-geoportal-basic" OR "src/js/openfiles"` |
| Censys | `web.endpoints.http.body: "src/js/components/openfiles/openfiles.css"` |
| FOFA | `body="src/js/components/openfiles/openfiles.css"` |
| Censys | `web.endpoints.http.body: "Argenmap es un visor de mapas interactivo"` |
| FOFA | `body="Argenmap es un visor de mapas interactivo"` |

## AvanMap (`avanmap`) {#avanmap}

Integrisoft Solutions' browser client for [Avansis.Hartă GIS](https://www.integrisoft.ro/solutii/avansis-bdu/avansis-harta-gis/), used by Romanian municipalities.

**Signals:** path `/AvanMap/`; title `AvanMap {version}`; scripts `AvanMap.js` and `initAvanMap.js`.

**Confirm:** GET the public map and match both named scripts. One record per municipality deployment. Do not infer AvanMap from generic Avansis municipal pages without a public map.

| Tool | Query |
|------|-------|
| Google | `inurl:/AvanMap/ "AvanMap"` |
| Google | `"initAvanMap.js"` |
| Censys | `web.endpoints.http.body: "initAvanMap.js"` |
| FOFA | `body="initAvanMap.js"` |

## WebEWID (`webewid`) {#webewid}

GEOMATYKA-KRAKÓW's public map module for the EWID 2007 land and property system. Vendor: [WebEWID](https://geomatyka-krakow.pl/portal/index.php/oprogramowanie); map-module manual: [Portal Mapowy](https://gdanski.webewid.pl/dokuweb/portal-mapowy/portal-mapowy.html).

**Signals:** title or page text `WebEWID`; a municipal GIS landing page linking to a `webewid.*` public map; EWID 2007 / GEOMATYKA-KRAKÓW branding.

**Confirm:** GET the actual public Portal Mapowy and match WebEWID. One record per authority deployment, not per WebEWID role portal. Do not add surveyor or valuation portals that require authentication.

| Tool | Query |
|------|-------|
| Google | `intitle:WebEWID (geoportal OR "portal mapowy" OR SIP)` |
| Google | `site:webewid.pl "Portal Mapowy"` |
| Censys | `web.endpoints.http.html_title: "WebEWID"` |
| FOFA | `title="WebEWID"` |
| FOFA | `host="webewid"` |
| FOFA | `body="WebEWID"` |

## KC WebGIS (`kcwebgis`) {#kcwebgis}

Kommunal-Consult Becker hosted municipal web GIS. Product: [KC WebGIS](https://kc-systemhaus.de/ihre-geodaten-mobil-verfuegbar-on-offline-mit-dem-neuen-kc-webgis/).

**Signals:** `/BMApp/` on numbered `gms*.kc-systemhaus.de` hosts; Angular application shell loading `settings.js`, `polyfills-*.js`, and `main-*.js`; Bürgerportal project parameter may be present.

**Confirm:** GET the public BMApp and match the shared KC application shell. One record per public municipality or Landkreis project. Skip private field apps and bare hosts without a public layer list.

| Tool | Query |
|------|-------|
| Google | `site:kc-systemhaus.de/BMApp/` |
| Google | `"KC WebGIS" BürgerGIS OR Bürgerportal` |
| Censys | `web.names: "kc-systemhaus.de" and web.endpoints.http.body: "settings.js"` |
| FOFA | `domain="kc-systemhaus.de" && body="settings.js"` |
| FOFA | `domain="kcwebgis.de"` |
| FOFA | `body="/BMApp/"` |

## BelsisIMS (`belsisims`) {#belsisims}

Turkish municipal Internet Map Server (KRH city guide). Vendor: [Belsis IMS/KRH](https://www.belsis.com.tr/Sayfa/Index/Cozumlerimiz/IMS/KRH). Distinct from Trimble Locus (`trimblelocus`).

**Signals:** `ims.{municipality}.bel.tr/Projects/{NAME}/Pages/KRH.aspx`; Belsis KRH chrome.

**Confirm:** GET the public KRH map. One catalog per municipality. Skip login staff GIS.

| Tool | Query |
|------|-------|
| Google | `KRH.aspx Belsis` |
| Censys | `web.endpoints.http.body: "KRH.aspx"` |
| FOFA | `body="KRH.aspx"` |

## CARTO (`carto`) {#carto}

Cloud spatial analytics and Builder maps. Site: [carto.com](https://carto.com). Docs: [docs.carto.com](https://docs.carto.com). Distinct from CartoVista (`cartovista`).

**Confirm:** GET a **government/nonprofit tenant** map catalog, not carto.com marketing. One catalog per public organization. Skip Builder demos.

| Tool | Query |
|------|-------|
| Google | `site:carto.com` government tenants only |
| Censys | `web.names: "carto.com"` |
| FOFA | `domain="carto.com"` |

## Copernicus DHuS (`copernicusdhus`) {#copernicusdhus}

ESA Data Hub System for Sentinel catalogs. Source: [SentinelDataHub/DHuS](https://github.com/SentinelDataHub/DHuS). Distinct from CDS (`copernicuscds`).

**Signals:** `/dhus/` web UI; DHuS OData; national hubs such as ESTHub.

**Confirm:** GET the DHuS catalog UI or OData product list. One catalog per public hub.

| Tool | Query |
|------|-------|
| Google | `"DHuS" Copernicus (catalogue OR odata)` |
| Censys | `web.endpoints.http.body: "DHuS"` |
| FOFA | `body="DHuS"` |

## DATUM GIS (`datumgis`) {#datumgis}

DATUM Soft regional/municipal web GIS. Product: [datum-gis](https://datum-soft.ru/products/datum-gis/).

**Signals:** DATUM GIS chrome; Russian municipal geoportal.

**Confirm:** GET the public map catalog. One catalog per deployment.

| Tool | Query |
|------|-------|
| Google | `"DATUM GIS" геопортал` |
| Censys | `web.endpoints.http.body: "DATUM GIS"` |
| FOFA | `body="DATUM GIS"` |

## eLiteGIS (`elitegis`) {#elitegis}

Atemiko ArcGIS-compatible GIS portal. Vendor: [atemiko.com](https://atemiko.com).

**Signals:** eLiteGIS branding; ArcGIS-compatible REST.

**Confirm:** GET a public REST/info or map catalog. One catalog per portal.

| Tool | Query |
|------|-------|
| Google | `"eLiteGIS" OR elitegis REST` |
| Censys | `web.endpoints.http.body: "eLiteGIS"` |
| FOFA | `body="eLiteGIS"` |

## EverGIS (`evergis`) {#evergis}

Everpoint web GIS (ЭверГИС). Site: [evergis.ai](https://evergis.ai). API: [everpoint.github.io/api](https://everpoint.github.io/api/).

**Signals:** EverGIS / ЭверГИС chrome; EverGIS Online or on-prem.

**Confirm:** GET the public map/table catalog. Skip EverGIS marketing. One catalog per public tenant.

| Tool | Query |
|------|-------|
| Google | `"EverGIS" OR "ЭверГИС"` |
| Censys | `web.endpoints.http.body: "EverGIS"` |
| FOFA | `body="EverGIS"` |

## Farvater GIS OGD (`farvatergisogd`) {#farvatergisogd}

Internet-Fregat urban-planning GIS OGD. Product: [gisogd](https://ifrigate.ru/solution/gisogd).

**Signals:** Farvater GISdoc; ГИСОГД document registry + map.

**Confirm:** GET the public GIS OGD catalog. One catalog per region/municipality. Do not also register a bundled GeoServer or ArcGIS REST root on the same host unless it is a distinct public product.

| Tool | Query |
|------|-------|
| Google | `"Farvater" ГИСОГД` |
| Censys | `web.endpoints.http.body: "Farvater"` |
| FOFA | `body="Farvater"` |

## IndorRoad Geoportal (`indorgeo`) {#indorgeo}

ИндорСофт road-authority geoportal on top of GIS IndorRoad. Product: [IndorRoad Geoportal](https://indorsoft.ru/products/road/geoportal/). HTML title is usually **IndorGeo**. Distinct from French INDORES GeoNetwork hosts (`indores.fr`).

**Signals:** title `IndorGeo: Геопортал автомобильных дорог` or SPA title `IndorRoad Geoportal: Геопортал автомобильных дорог`; React app at `/geo3/` (`base href="/geo3"`, `/geo3/static/js/main.*.js`, krpano); older tenants `/dashboard/` plus `/assets/indorgeo/ig1.js` and OpenLayers. Landing pages share `/assets/css/main.css`, `/assets/krpano/embedpano.js`, and PHPSESSID.

**Confirm:** GET the public landing page or `/geo3/` (200, no login wall). One catalog per public tenant. Skip vendor marketing/docs (`geo.indorsoft.ru`, `help.indorsoft.ru`), IndorCurator/IndorField, integrator sandboxes, and bare IP:port hits.

| Tool | Query |
|------|-------|
| Google | `intitle:"IndorGeo: Геопортал автомобильных дорог"` |
| Censys | `web.endpoints.http.html_title: "IndorGeo"` |
| FOFA | `title="IndorGeo"` |
| FOFA | `body="/assets/indorgeo/ig1.js"` |

## Geonomics (`geonomics`) {#geonomics}

Regional geoportal (Vue SSR + Mapbox). Vendor: [geonomix.kz](https://www.geonomix.kz).

**Signals:** Geonomics / geonomix chrome; Mapbox GL Vue app.

**Confirm:** GET the public geoportal. One catalog per deployment.

| Tool | Query |
|------|-------|
| Google | `"Geonomics" OR geonomix геопортал` |
| Censys | `web.endpoints.http.body: "geonomix"` |
| FOFA | `body="geonomix"` |

## GP Atlas (`gpatlas`) {#gpatlas}

Komi Republic web GIS «Атлас». Viewer: [geo.rkomi.ru/viewer](https://geo.rkomi.ru/viewer/).

**Signals:** GP Atlas / геоинформационная платформа «Атлас» chrome.

**Confirm:** GET the public viewer/catalog. One catalog per public Atlas.

| Tool | Query |
|------|-------|
| Google | `"GP Atlas" GIS` |
| Censys | `web.names: "rkomi.ru"` |
| FOFA | `domain="rkomi.ru"` |

## InGeo (`ingeo`) {#ingeo}

CSI Integro municipal GIS (ГИС ИнГео / InGeo-Web). Product: [GIS ИнГео](https://projects.integro.ru/%D0%B3%D0%B8%D1%81-%D0%B8%D0%BD%D0%B3%D0%B5%D0%BE/).

**Signals:** ИнГео chrome; InGeo-Web general-plan maps.

**Confirm:** GET the public InGeo-Web map. Skip desktop-only installs. One catalog per municipality.

| Tool | Query |
|------|-------|
| Google | `"ИнГео" GIS` |
| Censys | `web.endpoints.http.body: "InGeo"` |
| FOFA | `body="InGeo"` |

## IsiGéo (`isigeo`) {#isigeo}

Geomatika geoportal (not Isogeo SaaS `isogeo`). Product: [IsiGéo](https://www.geomatika.fr/systeme-information-isigeo/).

**Signals:** IsiGéo / Isigeo (Geomatika) chrome. Do not set this id on an Isogeo OpenCatalog.

**Confirm:** GET the public geoportal. One catalog per deployment.

| Tool | Query |
|------|-------|
| Google | `"IsiGéo" OR Isigeo géoportail` |
| Censys | `web.endpoints.http.body: "IsiGéo"` |
| FOFA | `body="IsiGéo"` |

## MetaGIS (`metagis`) {#metagis}

Swedish geospatial catalog/map publishing. Site: [metagis.se](https://www.metagis.se).

**Signals:** MetaGIS chrome; Swedish geoportal.

**Confirm:** GET the public map/metadata catalog. One catalog per portal.

| Tool | Query |
|------|-------|
| Google | `"MetaGIS" geoportal site:.se` |
| Censys | `web.names: "metagis.se"` |
| FOFA | `domain="metagis.se"` |

## mf-geoadmin3 (`mfgeoadmin3`) {#mfgeoadmin3}

swisstopo map viewer (map.geo.admin.ch) and cantonal forks. Source: [geoadmin/mf-geoadmin3](https://github.com/geoadmin/mf-geoadmin3). Distinct from `webmapviewer`.

**Signals:** geoadmin3 frontend; `mf-geoadmin3` assets; cantonal forks of map.geo.admin.ch.

**Confirm:** GET the public map viewer. One catalog per public fork, not every map theme.

[index.mako.html](https://github.com/geoadmin/mf-geoadmin3/blob/master/src/index.mako.html) sets `ng-controller="GaMainController"` (9 hosts in September 2026, including `map.geo.tg.ch`, `kartiskolen.no`, and `mapa.lokalneo.pl`). `body="geoadmin3"` is not usable: it matched 28 hosts, including `kantonthurgau.opendatasoft.com`.

| Tool | Query |
|------|-------|
| Google | `"geoadmin3" OR mf-geoadmin3` |
| Censys | `web.endpoints.http.body: "GaMainController"` |
| FOFA | `body="GaMainController"` |

## ORBISMap (`orbismap`) {#orbismap}

Russian high-load web GIS. Site: [orbismap.ru](https://www.orbismap.ru).

**Signals:** ORBISMap chrome; regional GIS portal.

**Confirm:** GET the public geoportal and match ORBISMap. One catalog per deployment, not per map layer. Do not also register a bundled GeoServer on the same host unless it is a distinct public product.

| Tool | Query |
|------|-------|
| Google | `"ORBISMap" геопортал` |
| Censys | `web.endpoints.http.body: "ORBISMap"` |
| FOFA | `body="ORBISMap"` |

## Re:Earth (`reearth`) {#reearth}

Cesium WebGIS / PLATEAU VIEW. Site: [reearth.io](https://reearth.io). Docs: [documents.reearth.io](https://documents.reearth.io).

**Signals:** Re:Earth chrome; PLATEAU VIEW 2.0+; Cesium digital-twin catalog.

**Confirm:** GET the public 3D/map catalog. One catalog per public project, not every scene. Keep a project only when `GET /data.json` returns a `layers` list with named entries. Skip `*.test.reearth.dev`, `*.dev.reearth.io`, bare IPs, the Visualizer/CMS editor login, and the CMS host that only backs an already registered viewer (`cms.plateauview.mlit.go.jp` is PLATEAU VIEW).

Published projects set a custom `<title>` and do not contain `Re:Earth Visualizer`. The served shell loads `/static/publishedAppProvider-*.js`. CMS shells use `<title>Re:Earth CMS</title>` from [reearth-cms `web/index.html`](https://github.com/reearth/reearth-cms/blob/main/web/index.html). Both apps also serve `/reearth_config.json` (not linked from `index.html`, so a homepage `body=` search misses it).

GitHub code search does not index most forks. Forks of [reearth/reearth-visualizer](https://github.com/reearth/reearth-visualizer) (65 in September 2026) and [reearth/reearth-cms](https://github.com/reearth/reearth-cms) (13) still point at `reearth.io` marketing pages. `filename:reearth_config.json` `"https://api."` finds templates and `*.dev.reearth.io` only.

September 2026: FOFA `body="Re:Earth Visualizer"` matched the editor shell (11 hosts). `body="Re:Earth CMS"` matched 16 hosts (vendor CMS, PLATEAU CMS, dead DNS, bare IPs). `body="publishedAppProvider"` matched 37 hosts; keep the ones whose `/data.json` lists layers.

| Tool | Query |
|------|-------|
| Google | `"Re:Earth" OR "PLATEAU VIEW"` |
| GitHub | forks of `reearth/reearth-visualizer` and `reearth/reearth-cms`; `filename:reearth_config.json` |
| Censys | `web.endpoints.http.body: "publishedAppProvider"` |
| FOFA | `body="publishedAppProvider"` |
| FOFA | `body="Re:Earth CMS"` |

## SuperMap iPortal (`supermapiportal`) {#supermapiportal}

SuperMap GIS portal/catalog hub. Docs: [help.supermap.com/iPortal](https://help.supermap.com/iPortal). Distinct from iServer (`supermapiserver`).

**Signals:** SuperMap iPortal web-ui shell. The homepage sets `window.iportal` and loads `css/iportal-components.*.css`. The default Vue noscript is `iportal-webui doesn't work properly`. Custom titles replace `<title>iportal-webui</title>` and sometimes the noscript, so prefer `window.iportal`.

**Confirm:** GET `/iportal/web/datas.json` (catalog links usually end in `/iportal`). Keep the portal only when `total` is greater than 0 and `content` is a non-empty list. One catalog per portal: the same dataset ids on another hostname are a duplicate (`a.`/`b.` nodes, `www`). Skip bare IPs, `help.supermap.com`, license-generator pages (`SuperMap许可生成`), and vhosts that only share an IP with an iPortal. `body="iPortal"` and `body="SuperMap iPortal"` match docs, blogs, and product mentions.

September 2026: `body="window.iportal"` matched 112 hosts, `body="iportal-webui doesn't work properly"` matched 80, and `body="css/iportal-components"` matched 36. `body="/iportal/web-ui/"` matched 67 and pulled in unrelated vhosts on the same IP.

| Tool | Query |
|------|-------|
| Google | `"SuperMap iPortal"` |
| Censys | `web.endpoints.http.body: "window.iportal"` |
| FOFA | `body="window.iportal"` |
| FOFA | `body="iportal-webui doesn't work properly"` |
| FOFA | `body="css/iportal-components"` |

## SuperMap iServer (`supermapiserver`) {#supermapiserver}

SuperMap enterprise GIS server (REST/OGC). Site: [supermap.com](https://www.supermap.com/en). Distinct from iPortal.

**Signals:** SuperMap iServer REST; `/iserver/` services.

**Confirm:** GET REST or OGC GetCapabilities. One catalog per public service root, not every layer.

| Tool | Query |
|------|-------|
| Google | `"SuperMap iServer" rest` |
| Censys | `web.endpoints.http.body: "iServer"` |
| FOFA | `body="iServer"` |

## EV-Globe (`evglobe`) {#evglobe}

Beijing Guotu Xintiandi (国遥新天地) 3D GIS platform family (EarthView brand): EV-Globe Desktop/WebGL viewers plus the EV-Server cloud GIS server (currently EV-Server 7). Product: [ev-image.com/column135](https://www.ev-image.com/column135). Distinct from SuperMap iServer (`supermapiserver`), MapGIS IGServer (`mapgisigserver`), and Tianditu (`tianditu`).

**Signals:** title `EV-Server`; root 303-redirects to `/earthview/server/manager/index.html` (v7) or `/ev-server/manager/index.html` (older); manager SPA loads `umi.js` plus Cesium/OpenLayers bundles; `manager/config/config.js` sets `appName="EV-Server 7"` and `company="北京国遥新天地信息技术股份有限公司"`.

**Confirm:** GET the root, follow the redirect, and match title `EV-Server`. The manager is a login-gated admin console — register only tenants with a public unauthenticated service or catalog view. Do **not** register bare-IP consoles, the manager login itself, the vendor site `ev-image.com`, or `bbs.ev-image.com`. Most deployments are CN government, energy, or intranet systems; FOFA `title="EV-Server"` without a country filter is dominated by German "InterAktiv eV Server" and Synology false positives.

| Tool | Query |
|------|-------|
| Google | `"EV-Server" (三维 OR 地理信息) -ev-image.com` |
| Censys | `web.endpoints.http.html_title: "EV-Server" and web.location.country_code = "CN"` |
| FOFA | `title="EV-Server" && country="CN"` |

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
| `geodados` | `{city}.geodados.com.br/Publico` | `site:geodados.com.br/Publico` |
| `geopixel` | see above | |
| `ctmgeo` | see above | |
| `drzwebgis` | `webgis.drz.com.br/{city}/` | `site:webgis.drz.com.br "WebGis"` |
| `mapmap` | `{city}.mapmap.com.br/geo-portal` | `site:mapmap.com.br/geo-portal` |
| `dmcity` | `web.dmcity.fi/{city}/public/` | `site:web.dmcity.fi` |
| `gausswebcity` | `{org}.gis.ba` / `/webcity/` | `domain="gis.ba"` |
| `infogis` | `www.infogis.fi/{muni}/` | `site:infogis.fi` |
| `experiencebuilder` | see [SDI](discovery-geoportals-sdi.md#experiencebuilder) | |
| `webappbuilder` | see [SDI](discovery-geoportals-sdi.md#webappbuilder) | |
| `arcgisdashboards` | see [SDI](discovery-geoportals-sdi.md#arcgisdashboards) | |
| `instantapps` | see [SDI](discovery-geoportals-sdi.md#instantapps) | |
| `activemapgis` | see above | |
| `mapapps` | see above | |
| `mapsolution` | `/MapSolution/apps/home/welcome` | `intitle:"Home MapSolution" inurl:/MapSolution/` |
| `belsisims` | see above | |
| `orbismap` | see above | |
| `opengeoportal` | see above | |
| `geonomics` | see above | |
| `rgis` | KZ `{host}/map/` Angular Leaflet | `inurl:/map/ (E-SQO OR "РГИС") site:.kz` |
| `emapa` | `*.e-mapa.net` Pandora | `site:e-mapa.net` |
| `loftmyndir` | `www.map.is/{muni}/` | `site:map.is loftmyndir` |
| `alta` | `geo.alta.is/{tenant}/` vefsja | `site:geo.alta.is kortasjá` |
| `bulplan` | `{muni}.bulplan.eu` UNIMAP | `site:bulplan.eu` |
| `tobel` | `{city}.tobel.bg` | `site:tobel.bg` |
| `geoportalch` | `www.geoportal.ch/{canton}` | `site:geoportal.ch` |
| `cogis` | see above | |
| `elitegis` | see above | |
| `smartfindersdi` | see above | |
| `giswebse` | see above | |
| `ingrid` | see [SDI](discovery-geoportals-sdi.md#ingrid) | |
| `metagis` | see above | |
| `isigeo` | see above | |
| `isogeo` | see above | |
| `mviewer` | see above | |
| `qgisserver` | see above | |
| `openeo` | see above | |
| `gis4smart` | GIS4Smart municipal | `"GIS4Smart" geoportal` |
| `evrymap` | Consortis Evrymap municipal | `"Evrymap" (Δήμος OR geoportal) site:.gr` |
| `geoportalrlp` | see [SDI](discovery-geoportals-sdi.md#geoportalrlp) | |
| `copernicusdhus` | see above | |
| `popgis` | see above | |
| `ncwms` | see above | |
| `mangomap` | see above | |
| `opendatacube` | see above | |
| `datacubews` | see [SDI](discovery-geoportals-sdi.md#datacubews) | |
| `supermapiserver` | see above | |
| `supermapiportal` | see above | |
| `evglobe` | see above | |
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
| `urbismap` | `www.urbismap.com` national hub | `site:urbismap.com geoportale` |
| `ldpgis` | `cloud.ldpgis.it/{slug}/` / LdP Viewer | `site:cloud.ldpgis.it` |
| `gfmaplet` | `*.prod.globogis.com` / `/page:s_italia:geoportale` | `site:prod.globogis.com geoportale` |
| `smartgis` | title `SmartGIS` Angular `<app-root>` `point_cloud` | `title="SmartGIS" && country="RS"` |
| `smartmap` | `{district}.smartmap.kz` Leaflet | `site:smartmap.kz` |
| `vkomap` | `/vkomap/` Leaflet + Esri, Geoinfo | `"vkomap" геопортал site:.kz` |
| `isymap` | ISY Map / GeoInnsyn `/geoinnsyn/` | `"ISY Map" OR GeoInnsyn site:.no` |
| `avinet` | Adaptive ExtJS atlas, `a3.avinet.no` | `"Developed by Avinet" atlas site:.no` |
| `mapplus` | `/mapplus-lib/` TYDAC Stadtplan | `inurl:/mapplus/ OR mapplus-lib site:.ch` |
| `envimap` | `*.envimap.hu` / GeoForte | `site:envimap.hu GeoForte` |
| `piso` | geoprostor.net PisoPortal | `site:geoprostor.net PISO` |
| `gdivisios` | `/visios/` GDi Ensemble viewer | `"GDi Visios" OR inurl:/visios/` |
| `mapguide` | `/mapguide/` CityScape / ajaxviewer | `inurl:/mapguide/ internet.php` |
| `zeljkogis` | `zeljko-gis.com` Fusion / `zopcina.zeljko-gis.com` | `site:zeljko-gis.com fusion` |
| `geoitgis` | `geoitgis.geo-it.be/touchviewer/` title Geo-IT GIS Touch Viewer | `site:geoitgis.geo-it.be/touchviewer` |
| `sigimweb` | `/sigimweb/` title SIGimWeb / `/gomap_web/` | `inurl:/sigimweb/ site:.qc.ca` |
| `gomap` | `{client}.geomapguide.ca` / title `GoMap - {tenant}` | `site:geomapguide.ca` |
| `geocentriq` | `app.geocentriq.com/mrc/{mrc}` | `site:app.geocentriq.com/mrc` |
| `geocentralis` | `portail.geocentralis.com/public/sig-web/{mrc}/{code}/` | `site:portail.geocentralis.com/public/sig-web` |
| `sigale` | `sigale.ca/Main.aspx?mrc={code}` | `site:sigale.ca Main.aspx mrc=` |
| `seasketch` | `seasketch.org/{project}/app` | `site:seasketch.org/app` |
| `xymaps` | `maps.xymaps.com/{city}` / `/xymaps/Map` | `intitle:"powered by XY" MAPS` |
| `pozi` | `{council}.pozi.com` title Pozi Web Map | `site:pozi.com "Pozi Web Map"` |
| `jmap` | `/JMapWeb/` / JMap NG `jmapserver-ng` | `intitle:JMapWeb OR site:jmaponline.net` |
| `giscloud` | `{city}.giscloud.com` | `site:giscloud.com` |
| `mrf` | `{county}.mrf.com` / `js/lib/mrf/` | `"MRF Web Disclaimer"` |
| `munisight` | `app.munisight.com/{Tenant}` or `{tenant}.gis.catalisgov.ca` Login.aspx | `body="app.munisight.com"` |
| `pmapper` | `/pmapper/` / `{city}.geo-portale.it` | `inurl:pmapper-4.2.0` |
| `communityview` | `VECommunityView/cities/{city}/` | `site:maps.digitalmapcentral.com VECommunityView` |
| `msgis` | `{city}.msgis.net` GeoInformation | `site:msgis.net GeoInformation` |
| `weave` | title Weave Map webpack `app.*.js` | `intitle:"Weave Map" site:.gov.au` |
| `ovie` | OVIE `/js/libs/OpenLayers/OL.js` Materialize | `"OVIE" IMPLAN OpenLayers site:.gob.mx` |
| `softpro` | `{city}.cadastre.com.ua` / SOFTPRO `/js/locale/ua.js` | `site:cadastre.com.ua` OR `"SOFTPRO" геопортал` |
| `mxsig` | `/mdm6/` `/mxsig2/` amplify.js | `inurl:/mdm6/ "Mapa Digital"` |
| `iobcina` | Kaliopa `/gisapp/Default.aspx?a=` | `body="xtheme-iobcina.css"` |
| `ishare` | Astun iShare / `mymaps.aspx` | `"Powered by iShare" site:.gov.uk` |
| `cadcorp` | Cadcorp SIS WebMap / GeognoSIS | `"SIS WebMap" OR GeognoSIS Cadcorp` |
| `reearth` | see above | |
| `gpatlas` | see above | |
| `geometa` | see above | |
| `argenmap` | `src/js/app.js` plus Argenmap modules | `"Argenmap" (IDE OR geoportal)` |
| `avanmap` | `/AvanMap/`, `initAvanMap.js` | `inurl:/AvanMap/ "AvanMap"` |
| `webewid` | title `WebEWID` / Portal Mapowy | `intitle:WebEWID "Portal Mapowy"` |
| `kcwebgis` | `gms*.kc-systemhaus.de/BMApp/` | `site:kc-systemhaus.de/BMApp/` |
| `pgis` | `*.pgis.lv`, title `pGIS`, `/api/v1/classifiers/layers` | `site:pgis.lv intitle:pGIS` |
| `geoambiental` | `*-visorpublico.geoambiental.co/content-layout` | `site:geoambiental.co intitle:Geoambiental` |
| `nazca` | `apps.nazcacatastro.com/public/{municipality-code}/` | `site:apps.nazcacatastro.com/public "Visor Catastral"` |
| `xiltrion` | `*.xiltriongeoservicio.com/map`, shared Vite bundle | `site:xiltriongeoservicio.com/map` |
| `gtmap` | V&G `thirdparty/soda/soda.js` header, often `/1/system/` | `"Copyright(C) V&G" "SODA" map` |
| `myeongji` | `/js/base/MapSave.js` + `BaseMap.js`/`SeeMap.js` client | `"js/base/MapSave.js"` |
| `digitaltwincloud` | HTML comment `DIGITAL TWIN CLOUD - NEWLAYER` / `assets/css/IDE.css` | `"DIGITAL TWIN CLOUD - NEWLAYER"` |
| `addspatial` | title `AddSpatial` / `/smart/?profile=` / `images/addspatial.svg` | `intitle:AddSpatial inurl:/smart/` |
| `berryict` | `gis.berryict.com/gis/gis/{assembly}/propertyidentification.php` | `site:gis.berryict.com` |
| `vbgis` | `{tenant}.vbgis.vn` urban-management or land-information viewers | `site:vbgis.vn` |
| `terratwin` | `/terratwin/` route, shared Vite bundles with `alkis-*.js`, `*.terratwin.net` | `site:terratwin.net` |
| `gis4u` | `/mapa/zakladni-aplikace/` routes, `/theme/square/` theme, tmapy.cz credit | `inurl:"/mapa/zakladni-aplikace"` |
| `shkkbs` | SHK municipal city guide and confirmed customer reference | `site:shkbilisim.com "Kent Bilgi Sistemi"` |
| `carto` | see above | |
| `mfgeoadmin3` | see above | |
| `webmapviewer` | swisstopo web-mapviewer / map.geo.admin.ch | `"web-mapviewer" OR inurl:/v1. map.geo.admin` |
| `datumgis` | see above | |
| `evergis` | see above | |
| `ingeo` | see above | |
| `farvatergisogd` | see above | |
| `indorgeo` | title `IndorGeo` / `/geo3/` / `/assets/indorgeo/ig1.js` | `intitle:"IndorGeo: Геопортал автомобильных дорог"` |
| `nexuspublicportal` | `/NexusPublicPortal/PublicPortal/Map` INS Nexus GIS | `inurl:/NexusPublicPortal/PublicPortal/Map` |

## CartoVista (`cartovista`) {#cartovista}

Commercial interactive map publishing platform with cloud and self-hosted options. Product: [CartoVista](https://cartovista.com/).

**Signals:** title `CartoVista Portal`; `/CartoVistaServer/maps/view`; versioned `cartovistawebportal-*` scripts and styles. Confirm the product assets, not a hostname containing only `carto`.

| Tool | Query |
|------|-------|
| Google | `inurl:/CartoVistaServer/maps/view "CartoVista Portal"` |
| Censys | `web.endpoints.http.body: "cartovistawebportal"` |
| FOFA | `body="cartovistawebportal"` |

## IGO2 (`igo2`) {#igo2}

Quebec-origin open-source Open GIS Infrastructure 2.0 viewer. Project: [igouverte.org](https://www.igouverte.org/english/) and [GitHub](https://github.com/infra-geo-ouverte/igo2).

**Signals:** exact title or branding `IGO2`; IGO2 Angular assembly; JSON context files; optional WMS/WFS/WPS/CSW services. Do not infer IGO2 from Angular, Material, or OpenLayers alone.

[src/index.html](https://github.com/infra-geo-ouverte/igo2/blob/next/src/index.html) sets `id="igoManifestByConfig"` and `#splash-screen__filmstrip`. In September 2026 `body="igoManifestByConfig"` matched the default-title hosts (including `immeubles.sqi.gouv.qc.ca`). Deployments that rewrite the title drop the manifest link; `body="splash-screen__filmstrip"` still matches them (`gestion.territoire.gouv.qc.ca`). `title="IGO2"` matched 22 and includes unrelated sites. Keep the splash query with the manifest query.

GitHub: forks of [infra-geo-ouverte/igo2](https://github.com/infra-geo-ouverte/igo2) keep the upstream demo homepage, so they are not a tenant list. Code search for `splash-screen__filmstrip` or `igoManifestByConfig` (code search skips forks) hits the upstream `index.html` and HTML snapshots of the already registered `apercu-qc` hub. Read `public/config/config.json` and `public/contexts/_default.json` on a live host, or `assets/config/config.json` when the SPA returns `index.html` for unknown paths. Keep a host only when the default context or a public WFS/WMS capabilities document names operational layers. One record per public viewer; skip the same app on a raw IP or a hosting alias (`sqi-prod.yulcom.net` serves the SQI building tiles).

| Tool | Query |
|------|-------|
| Google | `"IGO2" (geoportal OR cartographie) -site:github.com` |
| GitHub | forks of `infra-geo-ouverte/igo2`; code search `splash-screen__filmstrip` |
| Censys | `web.endpoints.http.body: "igoManifestByConfig"` |
| Censys | `web.endpoints.http.body: "splash-screen__filmstrip"` |
| FOFA | `body="igoManifestByConfig"` |
| FOFA | `body="splash-screen__filmstrip"` |
| Censys | `web.endpoints.http.html_title: "IGO2"` |
| FOFA | `title="IGO2"` |

## vMap2 (`vmap2`) {#vmap2}

Veremes open-source web GIS (successor to Veremap and vMap) used by French collectivités. Product: [vMap 2](https://www.veremes.com/produits/vmap). Docs: [documentation.veremes.net/vmap2](http://documentation.veremes.net/vmap2/). Source: [gitlab.veremes.net/open-source/vmap-2](https://gitlab.veremes.net/open-source/vmap-2). Distinct from Lizmap (`lizmap`), mviewer (`mviewer`), and generic MapServer (`mapserver`) catalogs.

**Signals:** HTML title `vMap` or login copy `Bienvenue sur vMap2`; path `/vmap`, `/vmap/login`, `/vmap2/`, or `/vmap/widget/vmap`; version string `vMap 2025.` / `vMap 2026.`; footer or docs link to `documentation.veremes.net/vmap2`; hosted tenants on `{org}.veremes.net`. Confirm the Veremes vMap chrome, not an unrelated `vmap.*` hostname (Haiberg vMAP Portal, Virginia VMAP, video VMAP).

**Confirm:** GET `/vmap` or `/vmap/login` and match the title, version string, or vMap2 login page. Public catalogs are the SIG hub, a guest `/vmap` map, or an unauthenticated `/vmap/widget/vmap` embed. One record per public tenant, not per widget token or thematic map. Skip vendor demos, consultant marketing (BreizhMapping), private-company GIS (Nexun), and login-only staff instances with no public widget.

| Tool | Query |
|------|-------|
| Google | `"Bienvenue sur vMap2" OR intitle:vMap inurl:/vmap site:.fr` |
| Google | `inurl:/vmap/widget/vmap OR inurl:/vmap/login Veremes OR vMap2` |
| Censys | `web.endpoints.http.html_title: "vMap"` |
| FOFA | `title="vMap" && country="FR"` |
| FOFA | `host="vmap" && country="FR"` |
| FOFA | `cert="veremes.net"` |

## InfoMap (`infomap`) {#infomap}

Emtel hosted New Zealand map portal. Product: [InfoMap](https://www.infomap.co.nz/products/infomap-pro-web-mapping/).

**Signals:** title `InfoMap Map Portal`; `*.infomap.co.nz` or a council custom domain; `X-Powered-By: Emtel NZ Ltd`; map portal backed by QGIS Server. One record per tenant, not per map.

| Tool | Query |
|------|-------|
| Google | `intitle:"InfoMap Map Portal" site:.nz` |
| Google | `site:infomap.co.nz "Map Portal"` |
| Censys | `web.endpoints.http.html_title: "InfoMap Map Portal"` |
| FOFA | `title="InfoMap Map Portal"` |
| FOFA | `header="Emtel NZ"` |

## dpWebmap (`dpwebmap`) {#dpwebmap}

Digpro dpSpatial browser client used for municipal and utility maps. Vendor: [Digpro](https://digpro.com/).

**Signals:** title `dpWebmap` or `dpSpatial - dpWebmap`; `/bios/dpwebmap/`; `app.htmlclient.gwt.DPWebApp.nocache.js`. Do not match generic OpenLayers map clients.

| Tool | Query |
|------|-------|
| Google | `intitle:dpWebmap OR inurl:/bios/dpwebmap/` |
| Censys | `web.endpoints.http.body: "DPWebApp.nocache.js"` |
| FOFA | `body="DPWebApp.nocache.js"` |

## 3MAP (`3map`) {#3map}

3 PORT IT municipal GIS viewer in the 3OIS suite. Product: [3MAP](https://3-port.si/nase-resitve/javne-e-storitve/).

**Signals:** 3MAP / GIS pregledovalnik branding; `/desk/js/Translations_mini.js`; `GISProjectListing_mini.js`; help under `/trimap/_common/resource/help/`. Confirm the vendor assets because `3map` alone is too broad.

| Tool | Query |
|------|-------|
| Google | `"GIS pregledovalnik 3MAP" OR "GISProjectListing_mini.js"` |
| Censys | `web.endpoints.http.body: "GISProjectListing_mini.js"` |
| FOFA | `body="GISProjectListing_mini.js"` |

## 1Map (`1map`) {#1map}

1Doc Tecnologia municipal geoportal module (1Doc suite, Brazil). Product: [go.1doc.com.br/1map](https://go.1doc.com.br/1map/). Distinct from the South African 1map platform ([1map.co.za](https://www.1map.co.za/)) and from lookalike hostnames (`1map.pl` is Mapbender, `map.gov.hk` is ArcGIS Server).

**Signals:** host `{municipio}.1map.com.br`; HTML title `1Map` with meta description `1Map app`; Next.js shell (`/_next/static/`) redirecting to `/auth/unauthenticated?callbackUrl=...`.

**Confirm:** GET `https://{municipio}.1map.com.br/` and match the `1Map` title plus the auth redirect. Tenants are sign-in only (`access_mode: restricted`); `/geoserver/...` paths return the SPA shell, not OGC XML. One record per municipal tenant. Skip `demonstracao`/`demostracao` (vendor demo), `argo` (Argo CD), and dead subdomains (404). Do **not** add the 1Doc marketing pages.

| Tool | Query |
|------|-------|
| Google | `site:1map.com.br` |
| Censys | `web.names: "1map.com.br"` |
| FOFA | `domain="1map.com.br"` |
| FOFA | `body="1map.com.br"` |
| crt.sh | `%.1map.com.br` |

## CGI WebGIS / Facta WebGIS (`factawebgis`) {#factawebgis}

Finnish municipal WebGIS in CGI's Facta/KuntaNet product family. Product: [CGI Facta](https://www.cgi.com/fi/fi/tuoteratkaisut/facta).

**Signals:** exact title `Facta WebGIS 4.0`; `facta.css` plus `bundle.js`; path `/karttapalvelu.{tenant}/`. Do not infer the product from a generic Finnish `karttapalvelu` name.

| Tool | Query |
|------|-------|
| Google | `intitle:"Facta WebGIS" site:.fi` |
| Censys | `web.endpoints.http.html_title: "Facta WebGIS"` |
| FOFA | `title="Facta WebGIS"` |

## inkasPortal (`inkasportal`) {#inkasportal}

GeoNet Online German public geoinformation viewer and successor to inkasWeb.

**Signals:** title `inkasPortal - GeoNet Online GmbH`; `static/js/inkas-portal.js`; `inkas-themenctrl.js`; optional `inkas@work` and `inkasDokument` modules. Do not confuse it with the DWD climate-adaptation tool also named INKAS.

| Tool | Query |
|------|-------|
| Google | `"inkasPortal" "GeoNet Online"` |
| Censys | `web.endpoints.http.body: "inkas-portal.js"` |
| FOFA | `body="inkas-portal.js"` |

## GeoViewer Online (`geoviewer`) {#geoviewer}

Nobel Systems cloud GIS and utility-operations platform. Product: [GeoViewer Online](https://www.nobel-systems.com/geoviewer-online).

**Signals:** customer subdomain on `geoviewer.io`; styles from `geoviewer.io/css/nobel-style.css`; Nobel Systems branding. Do not match unrelated products whose page title merely says GeoViewer.

| Tool | Query |
|------|-------|
| Google | `site:geoviewer.io GIS` |
| Censys | `web.endpoints.http.body: "nobel-style.css"` |
| FOFA | `body="nobel-style.css"` |

## Flood Intelligence Portal (`floodintelligenceportal`) {#floodintelligenceportal}

Water Technology and Hydrologic hosted Australian flood-risk portal. Product evidence: [Flood Intelligence Portal overview](https://www.hydronet.com.au/wp-content/uploads/2024/05/Water-Technology-Waterlines-2023-2_HydroNET-article.pdf).

**Signals:** tenant path `my.floodreport.com.au/{authority}/`; iframe to a Water Technology application; property flood report and event/gauge selection. North Central CMA's older `floodreports.nccma.vic.gov.au` Angular/Leaflet service is a different stack.

| Tool | Query |
|------|-------|
| Google | `site:my.floodreport.com.au` |
| Censys | `web.names: "my.floodreport.com.au"` |
| FOFA | `host="my.floodreport.com.au"` |

## pGIS (`pgis`) {#pgis}

TOPODATI hosted geographic-information viewer for Latvian municipalities. Product: [TOPODATI services](https://topodati.lv/pakalpojumi/).

**Signals:** customer subdomain of `pgis.lv`; exact title `pGIS`; matching Angular `main.*.js` and `styles.*.css` bundles; public JSON layer list at `/api/v1/classifiers/layers`. Distinct from TOPODATI's `terGIS` planning platform.

| Tool | Query |
|------|-------|
| Google | `site:pgis.lv intitle:pGIS` |
| Google | `"Ģeogrāfiskās informācijas pārlūkošanas platforma" pgis` |
| Censys | `web.names: "pgis.lv" and web.endpoints.http.html_title: "pGIS"` |
| FOFA | `domain="pgis.lv" && title="pGIS"` |

## Geoambiental (`geoambiental`) {#geoambiental}

SIGMA Ingeniería environmental-management and GIS platform for Colombian environmental authorities. Product: [SIGMA Ingeniería](https://www.sigmaingenieria.com.co/).

**Signals:** organization-specific `*-visorpublico.geoambiental.co` host; route `/content-layout`; exact title `Geoambiental`; shared Angular `scripts.58129861d17e94a7969e.js` and `styles.f15e2f1c3cc94445a8d2.css`. Do not match generic uses of the Spanish word *geoambiental* without the product host or SIGMA attribution.

| Tool | Query |
|------|-------|
| Google | `site:geoambiental.co intitle:Geoambiental` |
| Google | `"Software GEOAMBIENTAL" "SIGMA INGENIERIA"` |
| Censys | `web.endpoints.http.body: "styles.f15e2f1c3cc94445a8d2.css"` |
| FOFA | `body="styles.f15e2f1c3cc94445a8d2.css"` |

## NAZCA (`nazca`) {#nazca}

Soltesoft hosted cadastral-management software. Product root: [NAZCA Software](https://apps.nazcacatastro.com/).

**Signals:** `/public/{five-digit municipality-code}/` on `apps.nazcacatastro.com`; title `Visor Catastral Municipal {name}`; shared `main.js` plus municipality-specific `config_{name}.js`; OpenLayers 7 and Proj4. Do not infer NAZCA from a cadastral viewer using only OpenLayers.

| Tool | Query |
|------|-------|
| Google | `site:apps.nazcacatastro.com/public "Visor Catastral Municipal"` |
| Google | `"NAZCA Software" "Gestion Catastral"` |
| Censys | `web.names: "apps.nazcacatastro.com" and web.endpoints.http.body: "Visor Catastral"` |
| FOFA | `host="apps.nazcacatastro.com" && body="Visor Catastral"` |

## Xiltrion (`xiltrion`) {#xiltrion}

Dataxil hosted multipurpose-cadastre platform used by CATASIG municipal services. The authenticated product identifies itself as Xiltrion and credits Dataxil S.A.S.

**Signals:** municipal subdomain of `xiltriongeoservicio.com`; route `/map`; identical `assets/index-B0d7aah_.js` and `assets/index-d2T-uJnb.css` bundles; bundle strings `xiltrioncatastro`, `Logo_GEO_blanco.svg`, a first-party `/api`, and `Dataxil S.A.S.`. Confirm product strings because a generic Vite/Mapbox shell is insufficient.

| Tool | Query |
|------|-------|
| Google | `site:xiltriongeoservicio.com/map` |
| Google | `"software Xiltrion" catastro` |
| Censys | `web.endpoints.http.body: "index-B0d7aah_.js"` |
| FOFA | `body="index-B0d7aah_.js"` |

## GT Map (`gtmap`) {#gtmap}

V&G municipal spatial-information platform and LifeMap public-viewer solution. Product: [GT Map](https://www.vng.co.kr/product/platform/gtmap.do).

**Signals:** a client asset below `/resources/common/thirdparty/soda/soda.js`; header `SODA {version} OpenLayers based javascript map client library` and `Copyright(C) V&G`; common `/1/system/`, `/lifemap/system/`, or equivalent tenant route; `/gs-gate/` service configuration. The SODA header is required because Korean “Life Map” and `/system/` names are generic.

| Tool | Query |
|------|-------|
| Google | `"Copyright(C) V&G" "OpenLayers based javascript map client library"` |
| Google | `"thirdparty/soda/soda.js" (생활지리 OR 공간정보)` |
| Censys | `web.endpoints.http.body: "thirdparty/soda/soda.js"` |
| FOFA | `body="thirdparty/soda/soda.js"` |

## SHK Kent Bilgi Sistemi (`shkkbs`) {#shkkbs}

SHK Bilişim Teknolojileri municipal city-information and public mapping product. Product: [Kent Bilgi Sistemi](https://www.shkbilisim.com/kbs.html); deployment ownership can be checked against the vendor's [references](https://www.shkbilisim.com/).

**Signals:** public parcel/zoning and thematic city guide using municipality-hosted ArcGIS REST services, plus either an SHK logo/link in the client or an exact municipality match in SHK's official references. Do not identify generic Turkish `Kent Rehberi` pages from the title or ArcGIS JavaScript alone; many unrelated vendors and in-house teams use those conventions.

| Tool | Query |
|------|-------|
| Google | `site:shkbilisim.com "Kent Bilgi Sistemi"` |
| Google | `"shkbilisim.com" "Kent Rehberi"` |
| Censys | `web.endpoints.http.body: "shkbilisim.com"` |
| FOFA | `body="shkbilisim.com"` |

## Myeongji WebGIS (`myeongji`) {#myeongji}

Myeongji Information Technology (명지정보기술) municipal living-information WebGIS for Korean local authorities, concentrated in Jeollabuk-do. Vendor: [mjinfo.co.kr](https://www.mjinfo.co.kr/).

**Signals:** shared client assets `/js/base/MapSave.js`, `/js/base/BaseMap.js`, `/js/base/SeeMap.js`, or `/js/base/mapsave/MapSaveTool.js`; OpenLayers 2 with `proj4js-compressed.js`; titles like 생활지리정보시스템 or 생활공간정보안내시스템; Iksan credits 명지정보기술 in its footer. The shared base JS assets are required — Korean "Life Map" titles and the public-sector `/common/` web template are generic and shared by many unrelated vendors (including V&G GT Map).

| Tool | Query |
|------|-------|
| Google | `"js/base/MapSave.js"` |
| Google | `"SeeMap.js" "BaseMap.js" site:.go.kr` |
| Censys | `web.endpoints.http.body: "/js/base/mapsave/MapSaveTool.js"` |
| FOFA | `body="/js/base/mapsave/MapSaveTool.js"` |

## Berry GIS (`berryict`) {#berryict}

Berry ICT (BerryBath Solutions & Cutting Edge Technologies) hosted municipal GIS for Ghanaian assemblies. Vendor: [berryict.com](https://berryict.com/).

**Signals:** `gis.berryict.com/gis/gis/{assembly}/propertyidentification.php` tenant paths; Leaflet client; property-identification, street-addressing, and block/sub-metro layers. One record per assembly tenant.

| Tool | Query |
|------|-------|
| Google | `site:gis.berryict.com` |
| Google | `"berryict.com" (GIS OR "property identification") Ghana` |
| Censys | `web.names: "gis.berryict.com"` |
| FOFA | `host="gis.berryict.com"` |

## VB GIS (`vbgis`) {#vbgis}

Vietnamese municipal and provincial WebGIS platform hosted on tenant subdomains of the vendor domain vbgis.vn. Vendor root: [vbgis.vn](https://vbgis.vn/) (intermittently unreachable).

**Signals:** `{tenant}.vbgis.vn` subdomains, e.g. urban-management GIS (gismytho) and land information systems (`...lis`). Confirm the subdomain belongs to vbgis.vn before assigning; do not infer from Vietnamese "LIS" or "quy hoạch" naming alone.

| Tool | Query |
|------|-------|
| Google | `site:vbgis.vn` |
| Censys | `web.names: "vbgis.vn"` |
| FOFA | `domain="vbgis.vn"` |
| crt.sh | `%.vbgis.vn` |

## Terratwin (`terratwin`) {#terratwin}

Terratwin is an ArcGIS-based digital-twin and geoportal platform for German municipalities and districts. Product root: [terratwin.de](https://terratwin.de/); manual: [manual.terratwin.de](https://manual.terratwin.de/).

**Signals:** a `/terratwin/` route or a TerraTwin module inside a county GDI (e.g. `/m/hokis/`); an identical hashed Vite bundle set including `alkis-*.js` modules; vendor-hosted tenants under `*.terratwin.net` (e.g. Landkreis Calw on `lracw.terratwin.net`). Do not confuse with the EU research project terratwin.eu.

**Confirm:** many `*.terratwin.net` hosts in certificate logs are vendor demos or pre-launch pilots — render the app before adding. Production tenants have a customized welcome dialog and a county-branded HTML title (Calw "Geoportal Kreis Calw", Landkreis Karlsruhe "KARLA.maps | …"); unbranded hosts showing the generic "Willkommen bei der TERRATWIN-Demo!" dialog (gis-bgl, geoportal-ostalbmap), "… | Terratwin Demoprojekt" titles (lralb, also login-walled), or branded pilots not yet linked from the county site (lrabb, lra-rastatt) are demos/pilots, not catalogs. Skip `hokis.terratwin.net` (401) and NXDOMAIN hosts (lrahn, lrasbk, lranok, …).

| Tool | Query |
|------|-------|
| Google | `site:terratwin.net` |
| Google | `"Terratwin" (Landkreis OR Geoportal) -site:terratwin.eu` |
| Censys | `web.names: "terratwin.net"` |
| FOFA | `domain="terratwin.net"` |
| FOFA | `body="/terratwin/"` |

## GIS4U (`gis4u`) {#gis4u}

T-MAPY spol. s r.o. municipal web map portal for Czech municipalities. Vendor: [tmapy.cz/gis4u](https://www.tmapy.cz/gis4u); vendor example portals on `cr.gis4u.cz`. Tenants also run on city custom domains (`gis.trebic.cz`, `mapy.bohumin.cz`, `portal.mubruntal.cz`, …) with the same `/mapa/` + `/theme/square/` stack.

**Signals:** Czech application routes under `/mapa/` (e.g. `/mapa/zakladni-aplikace/`, `/mapa/technicka-mapa/`, `/mapa/pasport-*/`); shared `/theme/square/` assets (`sg.js`, `filterapps.js`); a `tmapy.cz` credit link. The `/mapa/` routes plus the square theme are required — a tmapy.cz link alone is insufficient because T-MAPY sells several distinct products. Do **not** set `gisplan` on this square-theme stack (`gis4u`).

| Tool | Query |
|------|-------|
| Google | `inurl:"/mapa/zakladni-aplikace"` |
| Google | `site:cr.gis4u.cz` |
| Censys | `web.endpoints.http.body: "theme/square/scripts/sg.js"` |
| FOFA | `body="theme/square/scripts/sg.js"` |

## DIGITAL TWIN CLOUD (`digitaltwincloud`) {#digitaltwincloud}

EGIS Co., Ltd. 3D GIS digital-twin SaaS (XDWorld), also white-labeled by NEWLAYER. Product: [egiscloud.com](https://egiscloud.com/main/main.do). OGC-compliant WMS/WFS/WCS.

**Signals:** HTML comment `<!--<title>DIGITAL TWIN CLOUD - NEWLAYER</title>-->`; `assets/css/IDE.css`; vendor tenants on `egiscloud.com` / `*.egiscloud.com`. Confirm the comment or an EGIS/NEWLAYER tenant. Do **not** set `digitaltwincloud` from a generic Korean "smart map" or "digital twin" title (Seoul S-Map, LH twins, and many municipal templates). Skip `newlayer.egiscloud.com/member/login.do` (login).

| Tool | Query |
|------|-------|
| Google | `"DIGITAL TWIN CLOUD - NEWLAYER"` |
| Google | `"DIGITAL TWIN CLOUD" (스마트맵 OR geoportal) site:.go.kr` |
| Censys | `web.endpoints.http.body: "DIGITAL TWIN CLOUD - NEWLAYER"` |
| FOFA | `body="DIGITAL TWIN CLOUD - NEWLAYER"` |

## brain-GeoCMS (`braingeocms`) {#braingeocms}

brain-SCC GmbH municipal geoportal CMS. Vendor: [brain-scc.de](https://www.brain-scc.de/). Use `software.id: braingeocms`. Nordhessen and Vogelsbergkreis geoportals are in-scope.

**Signals:** `meta name="generator" content="GeoCMS Version:…"` with a `brain-SCC` suffix and a site-root `base href`. Keep `api: false` unless a public CSW/WMS catalog is confirmed on the same host. Do **not** invent `geocms` from an unbranded GeoCMS title.

| Tool | Query |
|------|-------|
| Google | `"GeoCMS" (brain-SCC OR Nordhessen OR Vogelsberg) geoportal` |
| Censys | `web.endpoints.http.body: "brain-SCC"` |
| FOFA | `body="brain-SCC"` |

## DMAPS (`dmaps`) {#dmaps}

NAXA municipal house-numbering GIS for Nepal palikas. Product: [dmaps.org](https://dmaps.org/). Distinct from Kathmandu `gis.kathmandu.gov.np` (custom), GeoNep `p.mapper`, and Bheemdatta `munportal.naxa.com.np`.

**Signals:** HTML title `Digital Metric Addressing System` (or older `Changu Metric` / `SuryaBinayak Metric System`); shared Vite SPA `/assets/index-*.js`; host `{palika}.dmaps.org` or municipal `dmaps.` / `metric.` / `imas.` / `gis.` on `.gov.np`.

**Confirm:** GET the public viewer and match the DMAPS title plus the Vite shell. One record per public municipal tenant. Do **not** add the marketing homepage `dmaps.org` or `app.dmaps.org`. Skip `*-dev` / `*-stag` / `dma-dev.naxa.com.np`.

| Tool | Query |
|------|-------|
| Google | `intitle:"Digital Metric Addressing System"` |
| Google | `site:dmaps.org` |
| Censys | `web.endpoints.http.html_title: "Digital Metric Addressing System"` |
| FOFA | `title="Digital Metric Addressing System"` |
| FOFA | `domain="dmaps.org"` |
| crt.sh | `%.dmaps.org` |

## Map2Web (`map2web`) {#map2web}

Schubert & Franzke municipal town-plan viewer. AT/DE/IT/LI tenants at `{city}.map2web.eu`; RO at `{region}-city.map2web.eu` / `{region}-county.map2web.eu`. One record per tenant; do not register the vendor marketing homepage.

**Signals:** title `Map2Web` on the Vue shell (`/js/app.*.js`, noscript `We're sorry but Map2Web doesn't work properly`, keywords `map, online map, map2web`). Older tenants still serve the mapclient shell: title is the place name and the page loads `/static/mapclient/map/css/m2w.css`. `body="static.maptoolkit.net/mtk"` without `map2web.eu` is maptoolkit tourism pages, not this product. `body="m2w.css"` without the `/static/mapclient/` path matches unrelated site builders.

**Confirm:** GET `https://{tenant}.map2web.eu/` and `https://map.map2web.eu/apiv2/project/{tenant}.map2web.eu/pois` plus `/streets`. Keep a tenant when the POI tree has `item` records or `/streets` lists geometries. Drop project `404`s, `backend` / `frontend` / `cityapp` / `static` / `www`, UUID and `test` hosts, and `stadtonline.map2web.eu` (Inseratkunden aggregate of other towns). Distinct from MS-GIS `{city}.msgis.net` title `{City} GeoInformation`. There is no `map2web.ro` tenant host (the app treats that suffix as a staging alias).

| Tool | Query |
|------|-------|
| Google | `site:map2web.eu` |
| FOFA | `domain="map2web.eu"` |
| FOFA | `title="Map2Web"` |
| FOFA | `body="We're sorry but Map2Web doesn't work properly"` |
| FOFA | `body="online map, map2web"` |
| FOFA | `body="/static/mapclient/map/css/m2w.css"` |
| crt.sh | `%.map2web.eu` |

## EnMapa (`enmapa`) {#enmapa}

Nexus Geographics hosted municipal web GIS for Spanish town councils. Product: [enMapa](https://www.nexusgeographics.com/enmapa). Public tenants live at `{city}.enmapa.com` (Cloudflare in front) and on city hosts such as `geoportal.{city}.cat/visor/guia`. The same product’s **Geoportal Urbanístic** module is a planning viewer titled `{municipality}. Geoportal Urbanístic` at city paths like `/geoportal/` or `/{city}gp/` (for example `mapes.{city}.cat/geoportal/`, `piu.{city}.cat/geoportal/`). Do not create a second record for the Geoportal Urbanístic module when that municipality already has an enMapa visor.

**Signals:** HTML title `Enmapa` or `EnMapa v4.x`; `/visor/guia` or `visor-guia.jsp` paths; title `{city}. Geoportal Urbanístic`; Matomo at `matomo.nexusgeographics.com` or `stats.nexusgeographics.com`; OpenLayers bundle plus `nexus` asset references; tenant cert hostnames on `enmapa.com`.

**Confirm:** GET the public viewer and match the EnMapa title/shell. One record per municipality tenant. Skip `*.dev.enmapa.com`, `admin.*`, `demo.*`, `common.*`, and the CKAN open-data tenants on the same host family (`{city}-opendata.enmapa.com`, `opendata.{city}.enmapa.com` — those are `ckan` open data portals, not geoportals).

| Tool | Query |
|------|-------|
| Google | `site:enmapa.com` |
| Google | `"EnMapa" geoportal ajuntament` |
| Google | `"Geoportal Urbanístic" mapes. OR piu. OR sig.` |
| crt.sh | `%.enmapa.com` |
| Censys | `web.endpoints.http.html_title: "EnMapa"` |
| FOFA | `title="EnMapa"` |
| FOFA | `body="visor-guia.jsp"` |
| FOFA | `body="nexusgeographics"` |

## Nexus Public Portal (`nexuspublicportal`) {#nexuspublicportal}

INS (Skopje) municipal public web GIS, the public-portal module of Nexus GIS. Product: [Nexus GIS](https://nexus.ins.com.mk/). Public tenants live at `{city}.ins.com.mk/NexusPublicPortal/PublicPortal/Map` and on city hosts such as `gis.{city}.gov.mk/NexusPublicPortal/PublicPortal/Map`. Distinct from Spanish enMapa (`enmapa`, Nexus Geographics) and from Nexus Twin (`twin.{city}.gov.mk`).

**Signals:** path `/NexusPublicPortal/PublicPortal/Map`; HTML title `Map - Public GIS Portal` or `Мапа - Јавен ГИС портал`; OpenLayers viewer with cadastral / GUP / DUP layer lists; tenant cert hostnames on `ins.com.mk`.

**Confirm:** GET the public Map URL and match the Public GIS Portal title plus urban-plan or cadastre layers. One record per municipality. Prefer the official `gis.{city}.gov.mk` host when both that and `{city}.ins.com.mk` serve the same tenant. Skip `nexus.ins.com.mk` marketing, `nexusgis.ins.com.mk` demo, Field GIS, Nexus Twin, and AppCreator login workflows.

| Tool | Query |
|------|-------|
| Google | `inurl:/NexusPublicPortal/PublicPortal/Map` |
| Google | `"Јавен ГИС портал" OR "Public GIS Portal" site:.gov.mk` |
| crt.sh | `%.ins.com.mk` |
| Censys | `web.endpoints.http.html_title: "Public GIS Portal"` |
| FOFA | `title="Public GIS Portal" && body="NexusPublicPortal"` |

## Nazca4U Rapportagemodule (`nazca4u`) {#nazca4u}

Nazca hosted soil-information reporting application for Dutch provinces, omgevingsdiensten, and municipalities. Vendor: [nazca4u.nl](https://nazca4u.nl/). Tenants at `{tenant}.nazca4u.nl/rapportage/` (for example `delft.nazca4u.nl/rapportage/`). Distinct from NAZCA, Soltesoft's Colombian cadastral viewer (`nazca`).

**Signals:** hostname `*.nazca4u.nl` with route `/rapportage/`; ASP.NET assets `/Rapportage/Geolocator/{Map,Toolbar,Legend}/` and `App_Themes/RapportageModule/*.css`; page title `Rapportagemodule`; bodeminformatie lookup by address, parcel, or map selection with PDF report delivery by e-mail.

**Confirm:** GET the tenant `/rapportage/` page and check the `/Rapportage/Geolocator/` asset family. One record per public tenant. Skip the vendor marketing site.

| Tool | Query |
|------|-------|
| Google | `site:nazca4u.nl/rapportage` |
| Google | `"Rapportagemodule" bodeminformatie nazca` |
| Censys | `web.names: "nazca4u.nl"` |
| FOFA | `host="nazca4u.nl" && body="Rapportagemodule"` |

## ClimSeries (`climseries`) {#climseries}

FAO SWALIM climate time-series application (Somalia Climate TimeSeries Data) for hydrometeorological station data. Product: [climseries.faoswalim.org](https://climseries.faoswalim.org/). Tenants: FAO SWALIM plus the Puntland and Somaliland Information Management Centers (`climseries.imcpuntland.so`, `www.imcsomaliland.org/climseries/station/`).

**Signals:** hostname `climseries.*` or route `/climseries/station/`; title `Dashboard :: Somalia Climate TimeSeries Data`; AdminBSB theme assets (`/static/css/themes/all-themes.css`, `node-waves`, morrisjs); station-group routes `/station/map/{aws,mrs,ss,gws}/`; per-station tables with CSV download.

**Confirm:** GET the tenant dashboard and check the title plus `/station/` routes. One record per public tenant. SWIMS and FRRIMS on the same hosts are separate SWALIM-family applications, not ClimSeries.

| Tool | Query |
|------|-------|
| Google | `"Somalia Climate TimeSeries Data" OR "ClimSeries"` |
| Google | `inurl:climseries (faoswalim OR imcpuntland OR imcsomaliland)` |
| Censys | `web.endpoints.http.html_title: "Somalia Climate TimeSeries Data"` |
| FOFA | `title="Somalia Climate TimeSeries Data"` |

## GISNET V5 (`gisnet`) {#gisnet}

Complot's hosted municipal GIS platform for Israeli municipalities, local and regional councils. Product: [v5.gis-net.co.il](https://v5.gis-net.co.il/). Tenants at `v5.gis-net.co.il/v5/{authority}/` plus the older `mg{1,2}.gis-net.co.il/{Authority}Gis` generation; some cities run dedicated hosts (`gisn.tel-aviv.gov.il`). Hebrew interface.

**Signals:** page title `GISNET V5 By Complot - {city}`; hostname `v5.gis-net.co.il` or `mg{1,2}.gis-net.co.il`; user guide at `gis.mavo.co.il/v5/GIS.pdf`; parcel, planning, and engineering layer searches.

**Confirm:** GET the tenant page and check the title. The host geo-blocks some non-IL networks (connect timeouts) — in that case confirm via search-result titles (`"GISNET V5 By Complot"`). One record per public tenant.

| Tool | Query |
|------|-------|
| Google | `"GISNET V5 By Complot"` |
| Google | `site:v5.gis-net.co.il/v5` |
| Censys | `web.endpoints.http.html_title: "GISNET V5"` |
| FOFA | `title="GISNET V5"` |
| FOFA | `host="gis-net.co.il"` |
| FOFA | `body="GISNET"` |

## Taldor MapExpert (`mapexpert`) {#mapexpert}

Taldor Group's hosted municipal GIS platform for Israeli local authorities. Vendor: [taldor.co.il](https://www.taldor.co.il/). Tenants at `gis{NN}.taldor.co.il/{City}Gis` (for example `gis01.taldor.co.il/KiryatTivonGis`). Hebrew interface covering parcels, planning, and infrastructure.

**Signals:** hostname `gis{NN}.taldor.co.il` with a `{City}Gis` path; Taldor municipal GIS deployments documented for dozens of authorities (Haifa, Herzliya, Ra'anana, Afula, Ness Ziona, Givatayim, Netanya).

**Confirm:** GET the tenant page (a WAF may answer 403 to non-browser clients — confirm via the host pattern plus municipal branding). One record per public tenant.

| Tool | Query |
|------|-------|
| Google | `site:taldor.co.il inurl:Gis` |
| Google | `טלדור MapExpert GIS עירייה` |
| Censys | `web.names: "taldor.co.il"` |
| FOFA | `host="taldor.co.il"` |

## SWIMS (`swims`) {#swims}

FAO SWALIM's Water Sources Information Management System for Somali water-point inventory and monitoring. Product: [swims.faoswalim.org](https://swims.faoswalim.org/). Replicated to the Puntland IMC as PWIMS (`pwsims.imcpuntland.so`).

**Signals:** title `Dashboard :: SWIMS` (or `PWIMS`); route `/dashboard/view`; AdminBSB theme assets (`/static/css/themes/all-themes.css`) with calcite-maps Leaflet; `Water Sources Information Management System` branding; water-source WFS/WMS layers and a tabular borehole/well/dam inventory.

**Confirm:** GET the tenant dashboard and check the title plus `/dashboard/view` route. One record per public tenant. ClimSeries and FRRIMS on the same hosts are separate SWALIM-family applications.

| Tool | Query |
|------|-------|
| Google | `"Water Sources Information Management System" (SWIMS OR PWIMS)` |
| Google | `inurl:dashboard/view (faoswalim OR imcpuntland)` |
| Censys | `web.endpoints.http.html_title: "Dashboard :: SWIMS"` |
| FOFA | `title="Dashboard :: SWIMS"` |

## GovPilot GIS Map (`govpilot`) {#govpilot}

GovPilot's public interactive mapping module for US municipalities. Vendor: [govpilot.com](https://www.govpilot.com/). Tenants at `map.govpilot.com/map/{state}/{city}` (for example `map.govpilot.com/map/NJ/newark`).

**Signals:** page title `Interactive GIS Map of {CITY}, {STATE} | Powered by GovPilot`; Telerik Kendo ASP.NET assets; municipal parcels, zoning, and administrative layers.

**Confirm:** GET the tenant page and check the `Powered by GovPilot` title. One record per public tenant. Skip the vendor marketing site.

| Tool | Query |
|------|-------|
| Google | `"Powered by GovPilot" "Interactive GIS Map"` |
| Google | `site:map.govpilot.com/map` |
| Censys | `web.endpoints.http.html_title: "Powered by GovPilot"` |
| FOFA | `title="Powered by GovPilot"` |
| FOFA | `host="govpilot.com"` |
| FOFA | `body="Powered by GovPilot"` |

## Lightship Works (`lightship`) {#lightship}

Hosted mapping platform from [Lightship Works](https://www.lightshipworks.com/). Public map catalogs live at `{tenant}.lightship.works/v2/public`. Registered tenants: FNESS and the City of Quesnel (British Columbia).

**Signals:** hostname `*.lightship.works`; path `/v2/public`.

**Confirm:** GET the public map. One record per public workspace. Skip login-only field-operations tenants and the vendor site.

| Tool | Query |
|------|-------|
| Google | `site:lightship.works/v2/public` |
| Censys | `web.names: "lightship.works"` |
| FOFA | `host="lightship.works"` |
| crt.sh | `%.lightship.works` |

## MapSifter (`mapsifter`) {#mapsifter}

TerraScan's hosted county parcel-map viewer, paired with the TaxSifter assessment search. Tenants historically at `{county}.mapsifter.com` and now county-branded ASP.NET applications at `{county}-mapsifter.publicaccessnow.com` (for example `adamswa-mapsifter.publicaccessnow.com`). Washington-only footprint; live tenants as of 2026-09: Adams, Douglas, Ferry, Garfield, Lincoln, Pacific, Skamania (all registered). Okanogan moved to MapGeo, Klickitat runs its own viewer; Whitman/Franklin/Mason run TaxSifter only.

**Signals:** hostname `*.mapsifter.com` or `*-mapsifter.publicaccessnow.com`; `Disclaimer.aspx` gateway; parcel, owner, and address search with assessment and zoning layers; `TerraScan MapSifter` branding on print pages.

**Confirm:** GET the tenant page; bare subdomain guesses may hit an AWS ALB `Target Group Heartbeat` default — treat that as not-a-tenant. One record per public tenant. Keep a tenant only when `GET https://mapsifter.publicaccessnow.com/MapDotNetUX9.3/REST/9.0/Map/{mapId}/DefinitionMapJSON` lists data layers (`Parcels`, zoning, districts). That map index is the tenant list (11 ids in September 2026). Drop the IIS default at `mapsifter.publicaccessnow.com`, vendor redirects of `*.mapsifter.com` to aumentumtech.com, and maps whose public host is NXDOMAIN or a heartbeat (Franklin, Grant, Grays Harbor, Okanogan still have layer JSON; their viewers are gone).

| Tool | Query |
|------|-------|
| Google | `"MapSifter" county assessor parcels` |
| Google | `site:publicaccessnow.com mapsifter` |
| Censys | `web.names: "mapsifter.com"` |
| FOFA | `host="mapsifter.com"` |
| FOFA | `host="mapsifter"` |
| FOFA | `body="Mapsifter"` |
| FOFA | `body="images/terrascan.ico"` |
| FOFA | `domain="publicaccessnow.com"` |

`body="css/MapSifterHTML5.css"`, `title="TerraScan MapSifter"`, and `body="MapDotNetUX9.3"` match nothing: FOFA indexes the disclaimer page, not `defaultHTML5.aspx`. `body="js/loadmap.js"` is not a fingerprint (83 unrelated hosts). `body="txtDisclaimer"` and `body="id=\"countyName\""` also match TaxSifter.

## Civil Solutions Tax Map Viewer (`civiltmv`) {#civiltmv}

Civil Solutions / ARH Associates hosted tax-map application for New Jersey municipalities and counties. Tenants at `tmv.civilsolutions.biz/viewer/{tenant-id}` (for example Wall Township, Hudson County, Teaneck, Howell, Washington Township, Jersey City, Edison).

**Signals:** hostname `tmv.civilsolutions.biz` with route `/viewer/{24-hex-id}`; titles `{Municipality} Tax Maps` or `{County} Tax Map Viewer`; Mazer-based viewer; block/lot, address, and map-sheet search; contact `gisinfo@arh-us.com`.

**Confirm:** GET the tenant viewer page and check the title plus the Civil Solutions / ARH disclaimer. One record per public tenant. The tenant id is an opaque hash — find tenants via search, not by guessing.

| Tool | Query |
|------|-------|
| Google | `site:tmv.civilsolutions.biz/viewer` |
| Google | `"Tax Map Viewer" "Civil Solutions" ARH` |
| Censys | `web.names: "civilsolutions.biz"` |
| FOFA | `host="civilsolutions.biz"` |

## IDEBA Visualizador (`ideba`) {#ideba}

Buenos Aires Province IDE hosted municipal map-viewer platform. Tenants at `visualizador.ideba.gba.gob.ar/{municipio}` (19+ municipalities: Marcos Paz, Balcarce, Bragado, Azul, and others). Platform: [ideba.gba.gob.ar](https://ideba.gba.gob.ar/).

**Signals:** hostname `visualizador.ideba.gba.gob.ar`; title `IDEBA`; Leaflet assets `./src/leaflet/plugins/*` plus `map-toolbar.css`; per-tenant GeoServer workspaces at `geoserver-nodo2.ideba.gba.gob.ar/geoserver/{municipio}/wfs|wms`.

**Confirm:** GET the tenant page and check the title plus the per-municipio GeoServer WFS/WMS references. One record per public municipal tenant. The province-level GeoNetwork (`geonetwork`) and GeoServer nodes on other ideba.gba.gob.ar hosts are separate records.

| Tool | Query |
|------|-------|
| Google | `site:visualizador.ideba.gba.gob.ar` |
| Google | `"Visor geográfico" "plataforma IDEBA" municipio` |
| Censys | `web.names: "visualizador.ideba.gba.gob.ar"` |
| FOFA | `host="visualizador.ideba.gba.gob.ar"` |

## Intertown UP (`intertownup`) {#intertownup}

Intertown's hosted GIS platform for Israeli regional councils, local councils, and planning committees. Public tenants at `up.intertown.co.il/{code}/public/` (nsk, hya, hvm, mhg, mgd, srk, and more). Hebrew interface.

**Signals:** hostname `up.intertown.co.il` with route `/{code}/public/`; title `GIS Intertown`; per-tenant "UP by Intertown" branding; React SPA (`/assets/index-*.js`, `vendor-react`, `vendor-redux`); `/org/` paths are login-only internal systems.

**Confirm:** GET the `/{code}/public/` page (HTTP 200 + `GIS Intertown` title); tenant identity comes from the page content or search results ("UP by Intertown {council}"). One record per public tenant. The `ags20.intertown.co.il` ArcGIS Server endpoints are a separate `arcgisserver` stack.

| Tool | Query |
|------|-------|
| Google | `"UP by Intertown"` |
| Google | `site:up.intertown.co.il inurl:public` |
| Censys | `web.names: "up.intertown.co.il"` |
| FOFA | `host="up.intertown.co.il"` |

## Atlas (`atlas`) {#atlas}

Open-source (EUPL 1.2) Common Ground municipal geoportal started by Gemeente Purmerend, developed with Delta10 and the Atlas community. Repository: [gitlab.com/purmerend/atlas](https://gitlab.com/purmerend/atlas). Tenants on municipal hosts (atlas.apeldoorn.nl, geodata.zutphen.nl, datalab.purmerend.nl/atlas); documented users include Purmerend, Utrecht, Zutphen, Apeldoorn, and SED.

**Signals:** title `Atlas · Gemeente {name}`; Vue SPA assets under `/atlas/static/assets/` (`_plugin-vue_export-helper-*.js`); Django backend; WMS/WFS/WMTS/MVT layers.

**Confirm:** GET the tenant page and check the `Atlas · Gemeente` title plus the `/atlas/static/` asset path. One record per public tenant. Distinct from InstantAtlas (`instantatlas`) and unrelated "Atlas" products.

| Tool | Query |
|------|-------|
| Google | `"Atlas · Gemeente"` |
| Google | `inurl:/atlas/static/assets` |
| Censys | `web.endpoints.http.html_title: "Atlas · Gemeente"` |
| FOFA | `title="Atlas · Gemeente"` |

## Mappi (`mappi`) {#mappi}

Swis's hosted map platform for Dutch municipalities ("het kaartenplatform voor organisaties"). Product: [mappi.nl](https://www.mappi.nl/). Tenants on city hostnames: kaart.leiden.nl, kaart.kampen.nl, kaart.amsterdam.nl, kaart.katwijk.nl, kaart.westerkwartier.nl, kaartlaag.rotterdam.nl, kaart.halle.be (Belgium).

**Signals:** Laravel/Vue SPA with `<meta name="tenant-id" content="{city}">` and a shared `<meta name="app-version">` build hash across tenants; map GeoJSON at `/api/maps/{id}.json`; `/build/assets/app-*.css` (Laravel Mix) assets.

**Confirm:** GET the tenant page and check the `tenant-id` meta plus the shared `app-version` hash. One record per public tenant. Event maps (kaart.marathon.nl) and project maps (kaart.groningenbereikbaar.nl) are out of scope.

| Tool | Query |
|------|-------|
| Google | `mappi.nl kaart gemeente` |
| Google | `inurl:kaart "tenant-id" gemeente` |
| Censys | `web.endpoints.http.body: "tenant-id" and web.endpoints.http.body: "app-version"` |
| FOFA | `body="tenant-id" && body="app-version"` |

## GajaMatrix GeoPortal (`gajamatrix`) {#gajamatrix}

Gingko.Systeme's municipal GIS GeoPortal / GDI-Knoten for small and medium-sized German municipalities. Product: [geoinformationssystem.net](https://geoinformationssystem.net/). Public GeoPortal frontends run on city or utility hostnames (geoportal.merseburg.de, geoportal.gera.de, geoportal.wassernord.de).

**Signals:** page title `GajaMatrix GeoPortal`; response header `x-powered-by: GajaMatrix GIS` (WildFly backend). The vendor-hosted `{tenant}.gajamatrix.de/geoserver` and `gdi.gajamatrix.de/geonetwork` backends are tagged `geoserver` / `geonetwork`, not `gajamatrix`.

**Confirm:** GET the public GeoPortal UI and match the title or the `x-powered-by` header. One record per GeoPortal frontend. Do **not** set `gajamatrix` on the `*.gajamatrix.de` GeoServer/GeoNetwork backends, and do **not** confuse with disy Cadenza (`cadenza`).

| Tool | Query |
|------|-------|
| Google | `"GajaMatrix GeoPortal"` |
| Google | `inurl:geoportal "GajaMatrix"` |
| Censys | `web.endpoints.http.headers: "GajaMatrix GIS"` |
| FOFA | `header="GajaMatrix GIS"` |

## GBD WebSuite (`gbdwebsuite`) {#gbdwebsuite}

gbd-consult's open-source WebGIS platform (server + responsive client + OGC services + 1:1 QGIS Server rendering), deployed as Docker containers. Product: [gbd-websuite.de](https://gbd-websuite.de/). Source: [gbd-consult/gbd-websuite](https://github.com/gbd-consult/gbd-websuite). Used by German municipalities and water boards (webgis.schmallenberg.de, webgis.hase-wasseracht.de).

**Signals:** client loads `/_/webSystemAsset/path/{app,vendor,util}.js`; `gc/main` React module; `gwsLogin` / `gwsOptions` globals.

**Confirm:** GET the public map client and match `/_/webSystemAsset/` or `/gws-client/gws-start-`. One record per public viewer. Do **not** set `gbdwebsuite` from a bare QGIS Server or GeoServer backend on the same host. Keep a viewer only when `POST /_/projectInfo` with `{"projectUid":"..."}` returns at least one layer whose type is not `tile` or `xyz`. Project uids are `GWS_PROJECT_UID`, `gwsOptions.projectUid`, or `/project/{uid}` links on the home page. Drop login-only shells, the stock Düsseldorf restaurant demo, `*.gbd-websuite.de` staging and `qfield-demo`, and projects whose only layer is a basemap.

[demo.html](https://github.com/gbd-consult/gbd-websuite/blob/master/data/web/demo.html) loads `/_/webSystemAsset/path/vendor.js` (64 hosts in September 2026, including `webgis.schmallenberg.de`). The install landing’s `gws_logo.svg` and `Welcome to GBD WebSuite` matched 0. `body="gwsUsername"` (the login input id from the client docs) matched 60 and includes hosts whose home page never mentions `webSystemAsset`. GBD WebSuite 6/7 login pages load `/gws-client/gws-start-{version}.js` instead (`body="/gws-client/gws-start"`, 5 hosts). `body="gws-start-"` alone is noisy (hosting sites and spam). `body="gwsOptions"` matched 5 project pages that use the stock template.

Deployments are Docker images (`gbdconsult/gws-server` in [INSTALL.md](https://github.com/gbd-consult/gbd-websuite/blob/master/INSTALL.md)), not GitHub Pages. Forks of `gbd-consult/gbd-websuite` and code search for `gbdconsult/gws-server` returned no public catalog URL in September 2026 (upstream, a FOSSGIS workshop, and three forks without homepages).

| Tool | Query |
|------|-------|
| Google | `"GBD WebSuite" webgis` |
| Censys | `web.endpoints.http.body: "webSystemAsset"` |
| FOFA | `body="webSystemAsset"` |
| FOFA | `body="gwsUsername"` |
| FOFA | `body="/gws-client/gws-start"` |
| FOFA | `body="gwsOptions"` |
| GitHub | `"gbdconsult/gws-server"` |
| GitHub | forks of `gbd-consult/gbd-websuite` |

## INVENT WebGIS (`inventwebgis`) {#inventwebgis}

INVENT ltd's browser-based WebGIS for Albanian public authorities (Tirana), with editing, SDI, and INSPIRE/ASIG support. Product: [invent.al](https://invent.al/en/index.html). Public viewers run on `*.gov.al` hosts (webgis.arrsh.gov.al, webgis.atp.gov.al) and on INVENT's own hosting (`maps.gc-al.com`, `apps.invent.al`).

**Signals:** loads `invent.css` / `r/i/resources/appinvent.css`; OpenLayers/dojo client (`i/ui/form/ApplicationContainer`, `requireLogin` in `dojoConfig`); viewer URL `/aps/?name={tenant}` or `/apps/?name={tenant}`. Newer apps (e.g. KQZ elections) use a Lit `mg-*` client on `apps.invent.al/p/?name={tenant}`.

**Confirm:** GET the public viewer and match `invent.css`/`appinvent.css` or the `/aps|/apps/?name=` path; `requireLogin : false` means the viewer loads without login. One record per public viewer. The vendor gallery at [apps.invent.al](https://apps.invent.al/) (webpack chunk `1.source.js`) lists all tenants, but its `login_required` flags are unreliable — probe each viewer. Skip `cloud.invent.al/*` and `qc.invent.al` (login redirect), `maps.gc-al.com/meta-app/*` (broken `db.get_conn`), and vendor demo tenants (olives, dashcam, solar panels, RPP demos). Do **not** set `inventwebgis` on the IKTK heritage viewers (arkeologjia/monumente.iktk.gov.al), which are a separate OpenLayers/GeoExt build.

| Tool | Query |
|------|-------|
| Google | `inurl:aps OR inurl:apps "?name=" webgis gov.al` |
| Censys | `web.endpoints.http.body: "invent.css"` |
| FOFA | `body="invent.css"` |

## uMap (`umap`) {#umap}

Open-source (WTFPL) collaborative map creator built on OpenStreetMap (Django + Leaflet). Project: [umap-project.org](https://umap-project.org), repository: [github.com/umap-project/umap](https://github.com/umap-project/umap). Each public instance is a map catalog: users publish maps with their own GeoJSON datalayers, browsable on the home page and via `/{lang}/search/`. Self-hosted by OSM chapters (umap.openstreetmap.fr/.de, umap.osm.ch), French public bodies (umap.incubateur.anct.gouv.fr), municipalities, universities, and associations. Community instance list: [wiki.openstreetmap.org/wiki/UMap#Instances](https://wiki.openstreetmap.org/wiki/UMap#Instances).

**Signals:** title `uMap` or `uMap - Online map creator` (often customized, e.g. `uMap Occitanie en scène`); assets under `/static/umap/` (`base.*.css`, `umap.js`); meta `content="uMap lets you create maps with OpenStreetMap layers in a minute and embed them in your site."`; home redirects to `/{lang}/`; map URLs `/{lang}/map/{slug}_{id}`.

**Confirm:** GET `/` and match `/static/umap/` assets, then GET `/{lang}/search/?q=map` (or count `/{lang}/map/` links on the home page) and require at least one public map. One record per public instance. Skip login-walled instances (home redirects to `/login/`), single-map sites (home redirects to one `/map/`), instances with zero public maps, dev/staging hosts, and bare-IP installs. Heavy name-collision noise: UMAP dimensionality-reduction visualizations (umap-learn), `umap.jp` marketing platform, `Utah Mortality Application Portal`, DOMImaps real-estate (`umap.css` collision), and people named Umap — none are this software.

[base.html](https://github.com/umap-project/umap/blob/master/umap/templates/base.html) links `umap/favicons` (242 hosts in September 2026, including `map.obiezionerespinta.info`). `body="/static/umap/"` matched 316. Instances that drop the favicon path still match the static prefix, so keep both.

| Tool | Query |
|------|-------|
| Google | `intitle:"uMap" "Online map creator" -site:github.com` |
| Google | `"uMap lets you create maps with OpenStreetMap layers"` |
| Censys | `web.endpoints.http.body: "umap/favicons"` |
| FOFA | `body="umap/favicons"` |
| Censys | `web.endpoints.http.body: "/static/umap/"` |
| Censys | `web.endpoints.http.html_title: "uMap"` |
| FOFA | `body="/static/umap/"` |
| FOFA | `title="uMap"` |

## GISQuick (`gisquick`) {#gisquick}

Open-source (GPL-2.0+) QGIS-project publishing platform by OpenGeoLabs (CZ): QGIS plugin + Go/Django server + QGIS Server + Vue.js web client. Product: [gisquick.org](https://gisquick.org), repository: [github.com/gisquick/gisquick](https://github.com/gisquick/gisquick). Each published project is a map application with OGC WMS/WFS/WMTS services; the server REST API exposes public project metadata. Self-hosted by research projects (rain1.fsv.cvut.cz) and NGOs (mnk-gisquick.dopracenakole.net). Distinct from Lizmap (`lizmap`) and QGIS Web Client 2 (`qwc2`), the other QGIS Server viewers.

**Signals:** HTML title `Gisquick` (customizable, e.g. `MNK`); client assets under `/map/js/` (`app.*.js`, `chunk-vendors.*.js`) and `/map/icons/`; noscript text `gisquick-web doesn't work properly without JavaScript`; meta description `Gisquick web map application`; public `GET /api/app` returns `{"app": {...}, "user": {...,"is_guest":true}}` (may include `landing_project`).

**Confirm:** GET `/` and match `/map/js/app.` or `/map/static/js/app.` assets, then GET `/api/app` (200, guest user JSON). Public projects are readable at `/api/map/project/{user}/{name}` and OGC services at `/api/map/ows/{user}/{name}?SERVICE=WMS&REQUEST=GetCapabilities`; `/api/projects` requires login on most deployments. One record per instance with at least one public project. Skip the vendor demo `demo.gisquick.org`, the vendor homepage, and login-only instances with no landing project. Note: `projects.gisquick.org` (the former hosted publishing service) and several `*.gisquick.org` subdomains were hijacked by gambling spam in 2026 — do not register them.

[index.html](https://github.com/gisquick/gisquick/blob/master/clients/gisquick-web/public/index.html) says `gisquick-web doesn't work properly` (28 hosts in September 2026, including `rain1.fsv.cvut.cz`). `body="/map/js/chunk-vendors"` matched 32. `title="Gisquick"` matched 29. Keep all three.

Installs whose Caddy root is `/map/` emit Vue’s default asset dir instead: `/map/static/js/chunk-vendors.*.js` and `/map/favicon.ico` (skansen.fsv.cvut.cz, www.glnet.nu). AND that path with the noscript string; `body="/map/static/js/chunk-vendors"` alone is ordinary Vue CLI noise. A public project is a `302` from `/` to `/?PROJECT={user}/{name}`, or `landing_project` on `GET /api/app`. Confirm `GET /api/map/project/{user}/{name}` returns layer JSON. The [gisquick.org](https://gisquick.org) showcase links are a second list (they named `mapy.agrometeorologie.cz`, which FOFA had not indexed).

| Tool | Query |
|------|-------|
| Google | `intitle:"Gisquick" -site:gisquick.org -site:github.com` |
| Google | `"Gisquick web map application"` |
| Censys | `web.endpoints.http.body: "gisquick-web doesn't work properly"` |
| FOFA | `body="gisquick-web doesn't work properly"` |
| Censys | `web.endpoints.http.html_title: "Gisquick"` |
| FOFA | `title="Gisquick"` |
| FOFA | `body="/map/js/chunk-vendors"` |
| FOFA | `body="/map/static/js/chunk-vendors" && body="gisquick-web doesn't work properly"` |
| crt.sh | `%.gisquick.org` |
| GitHub | `"gisquick/qgis-server" OR "gisquick/web-map" (docker-compose)` |
| GitHub | `GISQUICK_LANDING_PROJECT` or `image: gisquick/server` or `gisquick/nginx` (v1 GIS.lab role) |

## MapMint (`mapmint`) {#mapmint}

Open-source geoportal platform by GeoLabs SARL (FR) built on ZOO-Project WPS + MapServer. Product: [mapmint.com](https://mapmint.com), repository: [github.com/mapmint/mapmint](https://github.com/mapmint/mapmint). MapMint 3.0 deployments expose OGC API and STAC collection endpoints (e.g. `{host}:8080/ogc-api/`). Distinct from plain MS4W MapServer landing pages, which bundle ZOO-Project's `zoo_loader.cgi` but are not MapMint catalogs.

**Signals:** HTML title `MapMint` or `STAC Browser - MapMint 3.0`; body references `zoo_loader.cgi` together with MapMint branding; OGC API root at `/ogc-api/` with `/ogc-api/collections` STAC.

**Confirm:** GET `/ogc-api/collections` (or the STAC browser) and require at least one collection. One record per live deployment. Skip the vendor site `mapmint.com`, dead demo tenants (`demo.mapmint.com`, `dgi-bf`, `earthgeo`, `ravi`, `efoncier` subdomains are dead or repurposed), and MS4W default pages on bare IPs (`zoo_loader.cgi` link without MapMint UI).

| Tool | Query |
|------|-------|
| Google | `intitle:"MapMint" -site:mapmint.com` |
| Censys | `web.endpoints.http.html_title: "MapMint"` |
| FOFA | `title="MapMint"` |
| FOFA | `body="zoo_loader.cgi"` (heavy MS4W noise — review one by one) |
| crt.sh | `%.mapmint.com` |

## QGIS Cloud (`qgiscloud`) {#qgiscloud}

Hosted QGIS map publishing (SaaS by Sourcepole). Public tenant maps live at `www.qgiscloud.com/{account}/{map}`; Pro maps may use custom domains (page title still mentions QGIS Cloud). Site: [qgiscloud.com](https://qgiscloud.com).

**Confirm:** GET the map URL — page title is `QGIS Cloud - {map}` and the WMS endpoint is `{link}/wms?SERVICE=WMS&REQUEST=GetCapabilities` (may answer `401`/`404` when the owner disabled public OGC; the viewer is still a catalog). One record per public tenant map, not per embedding page. `domain="qgiscloud.com"` returns only platform infrastructure — tenants are paths on one host, so hunt **embedding sites** with `body=` and extract the `qgiscloud.com/{account}/{map}` URL from the iframe.

| Tool | Query |
|------|-------|
| Google | `inurl:qgiscloud.com map -site:qgiscloud.com` |
| FOFA | `title="QGIS Cloud"` (custom domains) |
| FOFA | `body="qgiscloud.com"` (embedding sites — extract tenant map URLs) |
| Censys | `web.endpoints.http.body: "qgiscloud.com"` |

## Septima Search (`septimasearch`) {#septimasearch}

Hosted geodata search component from Septima (Denmark), embedded in Danish public map applications. Product: [septima.dk](https://septima.dk/). Known deployments: Danmarks Miljøportal map clients (`*.miljoeportal.dk`) and SGAV's MARS.

**Signals:** page loads `https://septima.dk/septima-search-dmp/v1.js` (Danmarks Miljøportal build) or assets from `search.cdn.septima.dk`; title or footer mentions Septima. The simpler Septima Widget embed (`widget.cdn.septima.dk/latest/widgetapi.js`, e.g. findvej.dk) is an address/map widget, not a catalog — skip it. Skip Septima's own infra (`map.septima.dk`, `widgetadmin.septima.dk`), `*.test.`/`*.demo.`/`*.udv.` staging hosts, and workflow apps that only embed the search (rat reporting, area editing).

| Tool | Query |
|------|-------|
| Google | `"septima-search" OR "septima.dk/septima-search" -site:septima.dk` |
| Censys | `web.endpoints.http.body: "septima-search"` |
| FOFA | `body="septima.dk"` (broad; includes widget embeds) or `body="Septima Search"` |

## AtlasMapper (`atlasmapper`) {#atlasmapper}

AIMS open-source research-atlas framework (Ext JS/GeoExt) behind the eAtlas family. Source: [github.com/aims-ks/atlasmapper](https://github.com/aims-ks/atlasmapper). Known deployments: eAtlas (`maps.eatlas.org.au`), North West Atlas (`maps.northwestatlas.org`), Ningaloo Atlas.

**Signals:** static JS assets carry an `atlasmapperVer={version}` query parameter (e.g. `Ext-ux/CompositeFieldAnchor.js?atlasmapperVer=2.4.7`); `Ext-ux/` and `GeoExt-ux/` script paths; Australian Institute of Marine Science attribution. Usually paired with a GeoNetwork catalogue (`catalogue.{domain}/geonetwork`) and GeoServer/THREDDS service backends.

**Confirm:** GET the map root and match the `atlasmapperVer` asset parameter. One record per atlas viewer; record the paired GeoNetwork catalogue and GeoServer/THREDDS services as separate records. Do **not** set `atlasmapper` on the Drupal/WordPress front page of an atlas site.

[index.html.ftl](https://github.com/aims-ks/atlasmapper/blob/master/clientResources/amcTemplates/index.html.ftl) appends `atlasmapperVer` to every script and stylesheet (8 hosts in September 2026, including `maps.eatlas.org.au`).

| Tool | Query |
|------|-------|
| Google | `"atlasmapperVer"` |
| Censys | `web.endpoints.http.body: "atlasmapperVer"` |
| FOFA | `body="atlasmapperVer"` |

## Elvis (`elvis`) {#elvis}

Geoscience Australia's national elevation and depth download service under the Foundation Spatial Data Framework. Single instance: [elevation.fsdf.org.au](https://elevation.fsdf.org.au).

**Signals:** exact title `Elvis - Elevation and Depth - Foundation Spatial Data`; host `elevation.fsdf.org.au`; area-of-interest order/download workflow for LiDAR point clouds, DEMs, and bathymetry.

**Confirm:** GET the root and match the Elvis title and FSDF branding. One record only — there is a single national instance. Do **not** set `elvis` on unrelated sites that merely mention Elvis.

| Tool | Query |
|------|-------|
| Google | `intitle:Elvis "Foundation Spatial Data"` |
| Censys | `web.names: "elevation.fsdf.org.au"` |
| FOFA | `host="elevation.fsdf.org.au"` |

## North Australian Fire Information (`nafi`) {#nafi}

Charles Darwin University hosted fire-mapping service for northern Australia. Site: [firenorth.org.au](https://firenorth.org.au). Single instance with the viewer at `firenorth.org.au/nafi3/`.

**Signals:** title `Northern Australian Fire Information`; NAFI branding; OpenLayers client; GeoServer-backed public WMS feeds for current fires, fire scars, and fire-history layers.

**Confirm:** GET `/nafi3/` and match the NAFI title and branding. One record only — there is a single hosted instance.

| Tool | Query |
|------|-------|
| Google | `"North Australian Fire Information" OR "NAFI" firenorth` |
| Censys | `web.names: "firenorth.org.au"` |
| FOFA | `host="firenorth.org.au"` |

## GoMap (`gomap`) {#gomap}

Indixio web GIS platform (formerly Geomap GIS Amérique, hosting brand iGeoMapGuide) built on MapGuide Open Source and FDO. Product: [indixio.com/gomap](https://indixio.com/gomap/). SaaS tenants live on `{client}.geomapguide.ca`; on-premise tenants use paths such as `/gomap/` or `/map/` on the owner domain.

**Signals:** viewer title pattern `GoMap - {tenant}`; scripts under `/gomap_web/`; MapGuide `mapagent` backend. Distinct from SIGimWeb (`sigimweb`, the Indixio Quebec municipal assessment viewer on the same engine) and from generic MapGuide (`mapguide`) sites.

**Confirm:** GET the tenant viewer and match the `GoMap -` title or `/gomap_web/` scripts. One record per public tenant.

| Tool | Query |
|------|-------|
| Google | `intitle:"GoMap -" (geomapguide OR Indixio)` |
| Google | `site:geomapguide.ca` |
| Censys | `web.endpoints.http.html_title: "GoMap -"` |
| FOFA | `title="GoMap -"` |
| FOFA | `body="/gomap_web/"` |

## GeoView (`geoview`) {#geoview}

Canadian Geospatial Platform embeddable map viewer for geoCore content
([source](https://github.com/Canadian-Geospatial-Platform/geoview), React + TypeScript +
OpenLayers). Production use is the app.geo.ca map browser (`geocore`); the viewer is also
embeddable in any page via the published bundle.

**Signals:** script `cgpv-main.js` (hosted or self-hosted); `div` elements with class
`geoview-map` and a `data-config` JSON attribute; `cgpv.init()` in page scripts; bilingual
EN/FR UI. Distinct from Nobel Systems GeoViewer Online (`geoviewer`, `geoviewer.io`
subdomains) and from the older RAMP / FGP Viewer (`fgpv-vpgf`) used on open.canada.ca.

**Confirm:** GET the page and match `cgpv-main.js` or `geoview-map`. A GeoView embed alone
is a viewer, not a catalog — register the backing catalog (usually `geocore`) instead,
unless the page is the owner's primary data-discovery surface.

The repo ships `cgpv-main-1.0.0.js` and `cgpv-main-2.0.0.js`. `body="cgpv-main.js"` matched 0 hosts in September 2026. `body="geoview-map"` matched 15, including the Lee County property appraiser, which is not this viewer.

| Tool | Query |
|------|-------|
| Google | `"cgpv-main.js" OR "geoview-map"` |
| Censys | `web.endpoints.http.body: "cgpv-main.js"` |
| FOFA | `body="cgpv-main.js"` |

## iMap (imapTOO) (`imaptoo`) {#imaptoo}

Hosted municipal web-GIS platform operated by the Comox Valley Regional District (British Columbia, Canada) for itself and neighbouring local governments. Product: [comoxvalleyrd.ca iMap](https://www.comoxvalleyrd.ca/about/about-cvrd/imap). Known tenants: Comox Valley RD (`mapviewer.imaptoo.ca/secure/`), Alberni-Clayoquot RD (`acrdimap.imaptoo.ca/imap/`), Village of Cumberland (`imapcumberland.imaptoo.ca/imapviewer/`), and Regional District of Mount Waddington (`imaprdmw.imaptoo.ca/secure/`).

**Signals:** `*.imaptoo.ca` host with `/imap/`, `/imapviewer/`, or `/secure/` path; ArcGIS Web AppBuilder viewer (`jimu.js`, title `ArcGIS Web Application`); backing ArcGIS Server at `mapviewer.imaptoo.ca/imap.../rest/services` (alias `imap2.comoxvalleyrd.ca`). Distinct from generic "iMap"-named viewers on other platforms (Maryland iMap, King County iMap) and from 1Map (`1map`, Brazil).

**Confirm:** GET the tenant viewer and match the `imaptoo.ca` host and Web AppBuilder stack. One record per tenant viewer.

| Tool | Query |
|------|-------|
| Google | `site:imaptoo.ca` |
| Censys | `web.names: "*.imaptoo.ca"` |
| FOFA | `domain="imaptoo.ca"` |

## GSI Maps (`gsimaps`) {#gsimaps}

国土地理院 GSI's open-source national geoportal (地理院地図), Leaflet-based with `layers.txt` layer definitions. Site: [maps.gsi.go.jp](https://maps.gsi.go.jp/). Source: [github.com/gsi-cyberjapan/gsimaps](https://github.com/gsi-cyberjapan/gsimaps).

**Signals:** `js/gsimaps.js`, `GSI.GLOBALS`, `layers.txt` layer manifest, gsimaps chrome. Do not confuse with sites that merely embed 地理院タイル basemaps (those stay `custom`).

**Confirm:** GET the page and match `gsimaps` script/globals. One record per independent deployment.

[index.html](https://github.com/gsi-cyberjapan/gsimaps/blob/gh-pages/index.html) links `css/gsimaps.css` (31 hosts in September 2026, including `town-fuchu-webmap.jp`). `body="gsimaps"` matched 38. Keep both.

| Tool | Query |
|------|-------|
| Google | `"gsimaps" OR "地理院地図" ソース site:jp -site:gsi.go.jp` |
| Censys | `web.endpoints.http.body: "css/gsimaps.css"` |
| FOFA | `body="css/gsimaps.css"` |
| Censys | `web.endpoints.http.body: "gsimaps"` |
| FOFA | `body="gsimaps"` |

## open-hinata (`openhinata`) {#openhinata}

Open-source edition of ひなたGIS (Miyazaki Prefecture) and the OH3 / open-hinata3 surveyor fork. Source: [github.com/kenzkenz/open-hinata](https://github.com/kenzkenz/open-hinata).

**Signals:** OpenLayers 5 + Vue bundle, `js/layers.js` layer list, ひなたGIS / open-hinata branding, `oh3lab.jp/oh3/` for the OH3 fork.

**Confirm:** GET the viewer and match open-hinata branding or `layers.js`. One record per public deployment.

| Tool | Query |
|------|-------|
| Google | `"open-hinata" OR "ひなたGIS" OR "open-hinata3"` |
| Censys | `web.endpoints.http.body: "open-hinata"` |
| FOFA | `body="open-hinata"` |

## Maplat (`maplat`) {#maplat}

Code for History's FOSS4G historical-map viewer (絵地図 rubber-sheeting). Site: [maplat.jp](https://www.maplat.jp/). Source: [github.com/code4history/Maplat](https://github.com/code4history/Maplat). Hosted tenants under `s.maplat.jp/r/{tenant}/`; custom domains possible (e.g. `onkochishinmap.com`).

**Signals:** `maplat` JS/CSS bundle, Maplat splash, `s.maplat.jp/r/` tenant paths, "Powered by Maplat".

**Confirm:** GET the tenant viewer and match the Maplat bundle. One record per public tenant (municipality / archive), not the maplat.jp marketing home.

| Tool | Query |
|------|-------|
| Google | `site:s.maplat.jp` or `"Powered by Maplat"` |
| Censys | `web.names: "*.maplat.jp"` |
| FOFA | `domain="maplat.jp"` |

## Stroly (`stroly`) {#stroly}

Kyoto-based hosted platform for georeferenced historical / illustrated maps. Site: [stroly.com](https://stroly.com/).

**Signals:** stroly.com viewer chrome; museum/library old-map collections published on Stroly.

**Confirm:** GET stroly.com. One platform-level record; do not register each uploaded map collection as a separate catalog.

| Tool | Query |
|------|-------|
| Google | `"Stroly" 古地図 OR "ストローリー"` |
| Censys | `web.names: "stroly.com"` |
| FOFA | `domain="stroly.com"` |

## eコミマップ (`ecommap`) {#ecommap}

NIED's open-source participatory WebGIS (eコミュニティ・プラットフォーム), basis of the 官民協働危機管理クラウド. Site: [ecom-plat.jp](https://ecom-plat.jp/).

**Signals:** eコミマップ / eコミュニティ・プラットフォーム chrome, `ecom-plat.jp` host, NIED 防災科学技術研究所 branding, WMS/XYZ/KML overlay map-making UI.

**Confirm:** GET the platform UI. One record per independent deployment.

| Tool | Query |
|------|-------|
| Google | `"eコミマップ" OR "eコミュニティ・プラットフォーム"` |
| Censys | `web.endpoints.http.body: "eコミマップ"` |
| FOFA | `body="eコミマップ"` |
