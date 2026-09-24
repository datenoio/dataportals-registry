# Discovering geoportal SDI platforms

Shared catalog and service stacks (`catalog_type: Geoportal`). Overview and short probe table: [discovery-geoportals.md](discovery-geoportals.md). Regional / municipal viewers: [discovery-geoportals-viewers.md](discovery-geoportals-viewers.md). Search-engine syntax (Google, Censys, Shodan, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md).

Do not add dataset-level records (a single CSW UUID, a STAC item, an ArcGIS layer id). One public catalog UI = one registry record.

## GeoNetwork (`geonetwork`) {#geonetwork}

ISO 19115 / CSW catalog. Gallery: [gallery-urls.csv](https://github.com/geonetwork/doc/blob/develop/source/annexes/gallery/gallery-urls.csv). European nodes also appear in the [INSPIRE geoportal](https://inspire-geoportal.ec.europa.eu/).

**Signals:** title “GeoNetwork”, path `/geonetwork` or `/srv/eng/catalog.search`, footer “GeoNetwork opensource”. The English catalog locale [en-core.json](https://github.com/geonetwork/core-geonetwork/blob/main/web-ui/src/main/resources/catalog/locales/en-core.json) sets `poweredBy` to “Powered by GeoNetwork opensource” (895 hosts in September 2026, including `catalogo.idegrancanaria.es`).

**Confirm:** `https://host/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities` (drop `/geonetwork` if the app is at the site root). Also `/srv/api` or `/srv/api/site`. A site-root redirect to `/geonetwork/.../catalog.search` (Città Metropolitana di Torino) or a live `/geonetwork/srv/eng/catalog.search` catalog (RSDI Basilicata Catalogo RSDI; GéoArdèche `/q` reports 143 records; Atmo Nouvelle-Aquitaine branded title; Lille Métropole `gn_search_georchestra`) is enough when CSW also matches. The default title “My GeoNetwork catalogue” still counts when CSW and search JSON match. GeoOrchestra-themed GeoNetwork stays `geonetwork` (no `georchestra` software id). Do **not** set `geonetwork` on a CMS geoportal landing when `/geonetwork/srv` 404s (also leftover Spanish IDE hubs: IDEEX, Gran Canaria, IDERIOJA, Cartagena, Pontevedra). Do **not** set `geonetwork` on EPA Maps GIS (`gis.epa.ie`): the maps landing is a different product from live GeoNetwork at `/geonetwork` (`EPA Ireland Catalogue`). Do **not** set `geonetwork` on the IDEE geoportal hub (`www.idee.es`); CODSI is already tagged.

| Tool | Query |
|------|-------|
| Google | `intitle:"GeoNetwork" "opensource" -site:github.com` |
| Google | `inurl:/srv/eng/catalog.search` |
| Google | `inurl:geonetwork "CSW" site:.europa.eu` |
| Censys (web) | `web.endpoints.http.html_title: "GeoNetwork"` |
| FOFA | `title="GeoNetwork"` |
| Censys | `web.endpoints.http.body: "GeoNetwork opensource"` |
| FOFA | `body="GeoNetwork opensource"` |
| FOFA | `body="gn_search_default"` |
| FOFA | `body="gn-bottom-bar"` |
| FOFA | `body="datahub-root"` |
| Shodan | `http.title:"GeoNetwork"` |
| GitHub | `geonetwork4_api_url https filename:toml` |

`gn_search_default` is the default search bundle in `catalog/views/api/index.html` (`/static/gn_search_default.js`). `gn-bottom-bar` is the footer class in the default search template. Use those when a site drops the “GeoNetwork opensource” footer. `datahub-root` is the [geonetwork-ui](https://github.com/geonetwork/geonetwork-ui) Datahub element (`apps/datahub/src/index.html`). Confirm CSW `numberOfRecordsMatched` > 0; drop stock samples (“Sample record, please remove”), sandboxes, and a second hostname of a catalog already registered (same `system/site/siteId`).

GitHub code search does not turn core-geonetwork forks into a portal list. `geonetwork4_api_url` in `default.toml` is usually a relative `/geonetwork/srv/api`. The absolute-URL form (`geonetwork4_api_url https filename:toml`) is the deployment-config pass; in September 2026 the only public absolute URL was `https://data.geopf.fr/catalog`, already an endpoint of `cartes.gouv.fr`.

**False positives:** documentation, GeoNetwork GitHub, harvested remote catalogs listed *inside* another GeoNetwork. Register the catalog root (`https://host/geonetwork` or `https://host/`), not a single metadata UUID.

## OpenWIS (`openwis`) {#openwis}

WMO meteorological metadata catalog. Source: [OpenWIS/openwis](https://github.com/OpenWIS/openwis). Reuses GeoNetwork-style CSW paths.

**Signals:** OpenWIS branding (not generic GeoNetwork footer); meteorological/WIS catalog chrome.

**Confirm:** GET CSW GetCapabilities or the OpenWIS catalog UI. Only set `openwis` when the product branding says OpenWIS; otherwise use `geonetwork`.

[banner.jsp](https://github.com/OpenWIS/openwis/blob/master/openwis-metadataportal/openwis-portal/src/main/webapp/jsp/banner.jsp) loads `images/openwis/header-left.jpg` (2 hosts in September 2026, both `dcpc-nwp.meteo.fr` titled OpenWIS Home). `body="OpenWIS"` matched 28, and the first hits are bare-IP 302 redirects.

| Tool | Query |
|------|-------|
| Google | `"OpenWIS" (catalogue OR CSW OR WIS)` |
| Censys | `web.endpoints.http.body: "images/openwis/header-left.jpg"` |
| FOFA | `body="images/openwis/header-left.jpg"` |
| Censys | `web.endpoints.http.body: "OpenWIS"` |
| FOFA | `body="OpenWIS"` |

## GeoNode (`geonode`) {#geonode}

Layer/map catalog, often with a bundled GeoServer.

**Confirm:** `/api/layers/` or `/api/datasets/` (GeoNode 4). CSW at `/catalogue/csw?service=CSW&version=2.0.2&request=GetCapabilities`.

| Tool | Query |
|------|-------|
| Google | `"GeoNode" (layers OR maps) inurl:/layers -site:geonode.org` |
| Google | `inurl:/api/layers/ geonode` |
| Censys | `web.endpoints.http.body: "geonode/css/base.css"` |
| FOFA | `body="geonode/css/base.css"` |
| Censys | `web.endpoints.http.body: "GeoNode"` |
| FOFA | `body="GeoNode"` |
| Shodan | `http.html:"GeoNode"` |

`geonode/templates/base.html` links `geonode/css/base.css` (564 hosts in September 2026). Skip demo.geonode.org and the project docs. Forks of `geonode/geonode` are the software, not a portal list.

## Palapa (`palapa`) {#palapa}

Indonesian simpul jaringan geoportal from Badan Informasi Geospasial (GSPalapa). Open source (GPL). GitHub: [agrisoft/gspalapa](https://github.com/agrisoft/gspalapa).

**Signals:** title “Geoportal Palapa”; path `/main/`; login `/gspalapa/`; footer Palapa V.x / BIG; pycsw CSW at `/csw`; bundled GeoServer at `/geoserver`.

**Confirm:** GET the catalog UI (often `/main/`) and match the Palapa title or `/gspalapa/` login. CSW: `https://host/csw?service=CSW&version=2.0.2&request=GetCapabilities` (pycsw). One record per public Palapa node, not a second copy of `/geoserver` on the same host.

| Tool | Query |
|------|-------|
| Google | `intitle:"Geoportal Palapa" site:.go.id` |
| Google | `inurl:/gspalapa/ OR inurl:/main/ "Geoportal Palapa"` |
| Censys | `web.endpoints.http.html_title: "Geoportal Palapa"` |
| FOFA | `title="Geoportal Palapa"` |
| Shodan | `http.title:"Geoportal Palapa"` |

**False positives:** GeoNode JIGN nodes (`/api/datasets/`); standalone GeoServer catalogs with no Palapa UI; Ina-Geoportal (`tanahair.indonesia.go.id`); provincial `/WebPortal/` Vue shells unless the Palapa title or `/gspalapa/` is present; CKAN Satu Data hosts named Palapa (for example `satudatapalapa.*`).

## GeoServer (`geoserver`) {#geoserver}

OGC service middleware. Register it when it is the **catalog** (layer list / GetCapabilities as the public product), not merely the backend behind GeoNode, Palapa, or ArcGIS.

**Confirm:** `https://host/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities` (sometimes `/ows` without `/geoserver`). Web admin title “GeoServer: Welcome”.

[index.html](https://github.com/geoserver/geoserver/blob/main/src/web/app/src/main/webapp/index.html) says “GeoServer admin console” on the redirect page (1,159 hosts in September 2026, including `geoserver.gz-ce.si`). `app="GeoServer"` still finds the service when that page is not indexed, so keep both.

| Tool | Query |
|------|-------|
| Google | `intitle:"GeoServer: Welcome" OR inurl:/geoserver/web` |
| Google | `inurl:/geoserver/ows GetCapabilities` |
| Censys | `web.endpoints.http.body: "GeoServer admin console"` |
| FOFA | `body="GeoServer admin console"` |
| Censys (hosts) | `host.services.software.product = "GeoServer"` |
| FOFA | `app="GeoServer"` |
| FOFA | `app="GeoServer" && country="ID"` |
| Shodan | `product:GeoServer` or `http.title:"GeoServer"` |

Do not register the `/geoserver/web` login as a catalog if a public WMS/WFS catalog is already represented by a parent GeoNode, Palapa, or GeoNetwork record on the same host. Prefer one record per public catalog UI.

## CubeWerx CubeSERV (`cubewerx`) {#cubewerx}

Commercial OGC server (WMS, WMTS, WFS, WCS, CSW, OGC API) in the Stratos platform. Vendor: [cubewerx.com](https://www.cubewerx.com). Register when CubeSERV is the **public catalog**, not a hidden backend.

**Signals:** path `/cubewerx/cubeserv`; GetCapabilities `ServiceProvider` or title CubeWerx / CubeSERV; Stratos catalogue CSW.

**Confirm:** GET WMS or CSW GetCapabilities that names CubeWerx. One record per public service root, not per layer.

| Tool | Query |
|------|-------|
| Google | `inurl:/cubewerx/cubeserv (WMS OR CSW OR GetCapabilities)` |
| Google | `"CubeWerx" OR CubeSERV (WMS OR geoportal OR CSW) -site:cubewerx.com` |
| Censys | `web.endpoints.http.body: "CubeWerx"` |
| FOFA | `body="CubeWerx"` |

## Hexagon M.App Enterprise (`mappenterprise`) {#mappenterprise}

Hexagon geoportal / browser GIS. Vendor: [hexagon.com/products/m-app-enterprise](https://hexagon.com/products/m-app-enterprise). Distinct from GeoMedia WebMap (`geomediawebmap`) and ERDAS APOLLO (`erdasapollo`).

**Signals:** path `/Apps/`; M.App Enterprise or Hexagon Geospatial branding; OGC WMS/WFS from the same estate.

**Confirm:** GET the public Apps portal and match M.App / Hexagon Geospatial. One record per public portal, not per app.

| Tool | Query |
|------|-------|
| Google | `"M.App Enterprise" OR "M.App" (geoportal OR Apps) Hexagon -site:hexagon.com` |
| Google | `inurl:/Apps/ (geoportal OR "M.App")` |
| Censys | `web.endpoints.http.body: "M.App Enterprise"` |
| FOFA | `body="M.App Enterprise"` |

## ArcGIS Hub (`arcgishub`) {#arcgishub}

Hub sites and Open Data sites on ArcGIS Online. Gallery: [hub.arcgis.com](https://hub.arcgis.com/). Hosts: `*.hub.arcgis.com`, `*opendata.arcgis.com`, plus custom domains.

**Signals:** `/api/search/v1`; `/api/feed/dcat-us/1.1.json`; `hubcdn.arcgis.com/opendata-ui`; or ArcGIS Enterprise `/portal/apps/sites/` with `opendata-ui` / `hub-site` assets.

**Confirm:** match a Hub/Sites signal and a public content or data gallery. Map-first hubs stay `catalog_type: Geoportal`; dataset-first hubs may be Open data portal ([discovery-opendata.md](discovery-opendata.md#arcgishub)). Custom-domain examples include Bloemendaal (`hubcdn.arcgis.com/opendata-ui`, `/api/search/v1`, DCAT-US). Do **not** set `arcgishub` from ArcGIS Enterprise `/portal/home/` alone; confirm `/portal/apps/sites/` (or a custom-domain Hub) with `opendata-ui` / `hub-site`.

| Tool | Query |
|------|-------|
| Google | `site:hub.arcgis.com` |
| Google | `site:opendata.arcgis.com "{city or agency}"` |
| Google | `"ArcGIS Hub" "open data" -site:esri.com` |
| Censys | `web.names: "hub.arcgis.com"` |
| FOFA | `host="hub.arcgis.com"` |
| FOFA | `body="opendata-ui"` |
| crt.sh | `%.hub.arcgis.com` |

## ArcGIS Server / Enterprise (`arcgisserver`) {#arcgisserver}

REST services directory. **Confirm:** `https://host/arcgis/rest/info?f=pjson` or `/arcgis/rest/services?f=pjson` (path may be `/server/rest/services` or `/rest/services`).

| Tool | Query |
|------|-------|
| Google | `intitle:"Folder: /" "ArcGIS REST Services Directory"` |
| Google | `inurl:/arcgis/rest/services` |
| Censys | `host.services.software.product = "ArcGIS"` |
| FOFA | `app="ArcGIS"` |
| Shodan | `http.html:"ArcGIS REST Services Directory"` |

Skip internal-only servers that return `401`/`403` for the services list. One record per public services root, not per map service.

## ArcGIS Experience Builder (`experiencebuilder`) {#experiencebuilder}

Esri configurable web app (Jimu). Product: [ArcGIS Experience Builder](https://www.esri.com/en-us/arcgis/products/arcgis-experience-builder/overview). Distinct from ArcGIS Hub (`arcgishub`), ArcGIS Server REST (`arcgisserver`), ArcGIS Web AppBuilder (`webappbuilder`), ArcGIS Instant Apps (`instantapps`), and Esri Finland dmCity (`dmcity`).

**Signals:** `experience.arcgis.com/experience/{id}`; Portal `/portal/apps/experiencebuilder/experience/?id=`; `jimu-core/init.js`; title `Experience`; favicon `exb.ico`. Swedish county WebbGIS on `ext-webbgis.lansstyrelsen.se/{tenant}/` is this product.

**Confirm:** GET the app URL and match Jimu / Experience Builder. One record per public app (item id or Länsstyrelsen tenant path), not per widget. Do **not** set `experiencebuilder` on `web.dmcity.fi/{city}/public/` (`dmcity`), on `/apps/webappviewer/` (`webappbuilder`), or on `/apps/instant/` (`instantapps`). Keep an existing `arcgisserver` REST directory on the same host as a separate catalog.

| Tool | Query |
|------|-------|
| Google | `site:experience.arcgis.com/experience` |
| Google | `inurl:/portal/apps/experiencebuilder/experience` |
| Google | `site:ext-webbgis.lansstyrelsen.se` |
| Censys | `web.endpoints.http.body: "jimu-core/init.js"` |
| FOFA | `body="jimu-core/init.js"` |

Skip Experience Builder samples on developers.arcgis.com and login-only drafts.

## ArcGIS Web AppBuilder (`webappbuilder`) {#webappbuilder}

Esri Web AppViewer (predecessor of Experience Builder). Docs: [Web AppBuilder](https://doc.arcgis.com/en/web-appbuilder/). Distinct from Experience Builder (`experiencebuilder`), Instant Apps (`instantapps`), and ArcGIS Hub (`arcgishub`).

**Signals:** `/apps/webappviewer/index.html?id=` on `*.maps.arcgis.com` or `/portal/apps/webappviewer/`. Exported self-hosted builds load `env.js`, `simpleLoader.js`, `init.js`, and Jimu assets such as `jimu.js/css` or `#jimu-layout-manager`.

**Confirm:** GET the viewer URL. One record per public app id. Do not also register the same host’s REST `/arcgis/rest/services` as a second Web AppBuilder catalog; keep `arcgisserver` if that directory is already the catalog.

| Tool | Query |
|------|-------|
| Google | `inurl:/apps/webappviewer/index.html` |
| Google | `inurl:/portal/apps/webappviewer/` |
| Censys | `web.endpoints.http.body: "/apps/webappviewer/"` |
| FOFA | `body="/apps/webappviewer/"` |

## ArcGIS Dashboards (`arcgisdashboards`) {#arcgisdashboards}

Esri location-analytics dashboards with maps, indicators, charts, gauges, and lists. Product: [ArcGIS Dashboards](https://www.esri.com/en-us/arcgis/products/arcgis-dashboards/overview). Distinct from ArcGIS Hub (`arcgishub`), Experience Builder (`experiencebuilder`), Web AppBuilder (`webappbuilder`), and Instant Apps (`instantapps`).

**Signals:** `/apps/dashboards/{item-id}` on `www.arcgis.com`, `*.maps.arcgis.com`, or an ArcGIS Enterprise portal; title `ArcGIS Dashboards`; dashboard JavaScript application shell.

**Confirm:** GET the public dashboard and match the exact `/apps/dashboards/` route. One record per public dashboard item when it functions as the catalog interface. Keep an existing ArcGIS Server REST directory as a separate catalog only when it exposes a broader service catalog.

| Tool | Query |
|------|-------|
| Google | `inurl:/apps/dashboards/ (GIS OR map OR data)` |
| Google | `site:maps.arcgis.com/apps/dashboards` |
| Censys | `web.endpoints.http.body: "ArcGIS Dashboards"` |
| FOFA | `body="ArcGIS Dashboards"` |

## ArcGIS Instant Apps (`instantapps`) {#instantapps}

Esri template-based public map apps (Basic, Sidebar, Lookup, Filter Gallery, Minimalist). Product: [ArcGIS Instant Apps](https://www.esri.com/en-us/arcgis/products/arcgis-instant-apps/overview). Distinct from Experience Builder (`experiencebuilder`), Web AppBuilder (`webappbuilder`), ArcGIS Hub (`arcgishub`), and ArcGIS Server REST (`arcgisserver`).

**Signals:** `/apps/instant/{template}/index.html?appid=` on `*.maps.arcgis.com` or Portal `/portal/apps/instant/`. Templates include `basic`, `sidebar`, `lookup`, `filtergallery`, `minimalist`.

**Confirm:** GET the Instant App URL. One record per public `appid`. Filter Gallery and org galleries are **hunt sources** (lists of apps), not a second catalog. Do **not** set `instantapps` on `/apps/webappviewer/` (`webappbuilder`) or `experience.arcgis.com` / `jimu-core/init.js` (`experiencebuilder`). Keep an existing `arcgisserver` REST directory on the same host as a separate catalog.

| Tool | Query |
|------|-------|
| Google | `inurl:/apps/instant/ basic OR sidebar OR lookup site:maps.arcgis.com` |
| Google | `inurl:/apps/instant/index.html?appid=` |
| Censys | `web.endpoints.http.body: "/apps/instant/"` |
| FOFA | `body="/apps/instant/"` |

## Lizmap (`lizmap`) {#lizmap}

QGIS Server web client. **Signals:** `/index.php/view/`, `lizMap`, project list. Vendor: [lizmap.com](https://www.lizmap.com/en/). OpenSIS / pgMetadata DCAT wrappers that still serve Lizmap (`lizmapPopup`, dock CSS, `/index.php/view/`) stay `lizmap`; do **not** invent `opensis`. Do **not** set `lizmap` from `/index.php/view/` when the HTML is the same CMS homepage (SIG Cévennes).

[lizmap/modules/view/templates/map.tpl](https://github.com/3liz/lizmap-web-client/blob/master/lizmap/modules/view/templates/map.tpl) includes the custom element `lizmap-navbar` (47 hosts in September 2026). `body="lizMap"` matched 4,192 and still covers older clients that do not ship that element.

| Tool | Query |
|------|-------|
| Google | `"Lizmap" (webgis OR geoportail OR "qgis") -site:github.com` |
| Google | `inurl:lizmap inurl:index.php/view` |
| Censys | `web.endpoints.http.body: "lizmap-navbar"` |
| FOFA | `body="lizmap-navbar"` |
| Censys | `web.endpoints.http.body: "lizMap"` |
| FOFA | `body="lizMap"` |

## Geotrek (`geotrek`) {#geotrek}

French outdoor/trail suite (GeotrekCE). Public catalogs are **Geotrek-rando** sites (v2 or v3). Docs: [geotrek.fr](https://geotrek.fr), instance list: [Liste des Geotrek connus](https://github.com/GeotrekCE/Geotrek-website/wiki/Liste-des-Geotrek-connus), map: [utilisateurs.geotrek.fr](https://geotrek.fr/utilisateurs.html). Distinct from GeoNature-atlas on the same park.

**Signals:** `--color-primary1-default` (v3); `ng-app="geotrekRando"` (v2); title `Geotrek-rando`; `__NEXT_DATA__` / `/_next/` (v3); Geotrek-admin `/api/v2/trek/`. Hosts often `rando.*`, `destination.*`, or `*rando*`.

**Confirm:** GET the public rando home. One record per public rando portal, not Geotrek-admin `/login/`, not geotrek.fr, not mobile apps, not Geotrek-rando-widget embeds on a tourism CMS, and not district search URLs of the same hub (Via Columbani, Chemins des Parcs, Rando IdF).

[_document.tsx](https://github.com/GeotrekCE/Geotrek-rando-v3/blob/main/frontend/src/pages/_document.tsx) writes `--color-primary1-default` (322 hosts in September 2026, including `rando.parcdumorvan.org` and `www.rando-aubrac.fr`). v2 [public/index.html](https://github.com/GeotrekCE/Geotrek-rando/blob/master/public/index.html) sets `ng-app="geotrekRando"` (14 hosts, including `rando-pnropf.pnr-idf.fr` and `randotectec.reunion-parcnational.fr`). `body="Geotrek-rando"` matched 181, including `www.terresdecorreze.com`. `body="geotrekApp"` matched nothing.

| Tool | Query |
|------|-------|
| Google | `"Geotrek-rando" OR "Geotrek rando" (randonnée OR trek) -site:github.com -site:geotrek.fr` |
| Google | `inurl:rando geotrek OR "geotrek-rando" site:.fr` |
| Censys | `web.endpoints.http.body: "--color-primary1-default"` |
| FOFA | `body="--color-primary1-default"` |
| Censys | `web.endpoints.http.body: "geotrekRando"` |
| FOFA | `body="geotrekRando"` |
| Censys | `web.endpoints.http.body: "Geotrek-rando"` |
| FOFA | `body="Geotrek-rando"` |

## GeoNature (`geonature`) {#geonature}

French biodiversity suite (PnX-SI). Public catalogs are **GeoNature-atlas** sites. Docs: [geonature.fr](https://geonature.fr), [GeoNature-atlas](https://github.com/PnX-SI/GeoNature-atlas). Distinct from Lizmap cartothèques on the same park.

**Signals:** `/static/css/atlas.css`; TaxHub media URLs (`/geonature/api/taxhub/`); gunicorn + Leaflet species sheets. Title often `Biodiv'…`.

**Confirm:** GET the public atlas home. One record per public atlas, not the authenticated GeoNature back-office (`/geonature/`) and not the project site geonature.fr.

[assets_header.html](https://github.com/PnX-SI/GeoNature-atlas/blob/master/atlas/templates/core/assets_header.html) links `/static/css/atlas.css` (409 hosts in September 2026). Indexed pages include GeoNature-atlas homes such as Biodiv'Mercantour.

| Tool | Query |
|------|-------|
| Google | `"GeoNature-atlas" OR "GeoNature atlas" (biodiversité OR biodiv) -site:github.com` |
| Google | `inurl:biodiversite "atlas.css" site:.fr` |
| Censys | `web.endpoints.http.body: "/static/css/atlas.css"` |
| FOFA | `body="/static/css/atlas.css"` |

## G3W-SUITE (`g3wsuite`) {#g3wsuite}

Open-source QGIS WebGIS (G3W-ADMIN + G3W-CLIENT). Site: [g3wsuite.it](https://g3wsuite.it). Distinct from Lizmap (`lizmap`) and QWC2 (`qwc2`).

**Signals:** title or footer “G3W-SUITE”; `g3w-client` / `g3wsdk` in JS; path `/map/{group}/{project}/`; REST `/api/` or `/group/api/`.

**Confirm:** GET the public portal or `/map/` client and match G3W-CLIENT. One record per public portal (tenant), not per QGIS project. Skip `/admin` login. If QGIS Server on the same host is only the OGC backend, do not also register `qgisserver`. Do **not** set `g3wsuite` from GisClient (`widgetGisClient.js`, `gcTool`, `?mapset=`) — that is a different product.

[index.html](https://github.com/g3w-suite/g3w-admin/blob/dev/g3w-admin/client/templates/client/index.html) serves `/static/client/images/g3wsuite_logo.png` (12 hosts in September 2026, including `map.geo.lea-ti.ch`). `body="g3w-client"` matched 8, the same maps. `body="startingspinner"` is not usable: the first hits are chocolate shops. `body="G3W-SUITE"` matched 248, including `erp.kartoza.com`.

| Tool | Query |
|------|-------|
| Google | `"G3W-SUITE" OR "G3W-CLIENT" (webgis OR geoportale) -site:github.com -site:g3wsuite.it` |
| Google | `inurl:/map/ g3w (webgis OR qgis) site:.it` |
| Censys | `web.endpoints.http.body: "g3wsuite_logo.png"` |
| FOFA | `body="g3wsuite_logo.png"` |
| Censys | `web.endpoints.http.body: "g3w-client"` |
| FOFA | `body="g3w-client"` |

## NextGIS Web (`nextgisweb`) {#nextgisweb}

**Signals:** `/resource/0`, NextGIS Web UI, `/api/resource/`.

| Tool | Query |
|------|-------|
| Google | `"NextGIS Web" OR inurl:/resource/0 "nextgis"` |
| Censys | `web.endpoints.http.body: "NextGIS"` |
| FOFA | `body="NextGIS"` |

## GC2 (`gc2`) {#gc2}

MapCentia GC2 (GeoCloud 2) spatial-data platform, often with the Vidi viewer. OSGeo: [GC2/Vidi](https://www.osgeo.org/projects/gc2-vidi/). Distinct from Japanese GC Navi (`gcnavi`) on `geocloud.jp`.

**Signals:** title “MapCentia GeoCloud”; path `/apps/viewer`; `/mapcache/{tenant}/wmts`; `/api/v1/sql/{db}`; `/api/v2/configuration`; hosts `*.mapcentia.com` or `*.gc2.io`.

**Confirm:** GET `/apps/viewer` or MapCache WMTS GetCapabilities. One record per public tenant, not the MapCentia marketing site or `map.gc2.io` demo.

[index.html](https://github.com/mapcentia/geocloud2/blob/master/public/apps/viewer/index.html) sets `window.MapCentia` (45 hosts in September 2026, including `vidi.swarm.gc2.io`). The static title `MapCentia GeoCloud` is not in the indexed HTML. Hosted tenants that drop the viewer script still match `mapcentia.com`, so keep that query.

| Tool | Query |
|------|-------|
| Google | `"MapCentia" OR GC2 (geoportal OR GeoCloud) (inurl:mapcentia.com OR inurl:gc2.io) -site:github.com` |
| Google | `inurl:/apps/viewer MapCentia OR inurl:/mapcache/` |
| Censys | `web.endpoints.http.body: "window.MapCentia"` |
| FOFA | `body="window.MapCentia"` |
| Censys | `web.names: "mapcentia.com"` |
| FOFA | `domain="mapcentia.com"` |
| crt.sh | `%.mapcentia.com` OR `%.gc2.io` |

## hale»connect (`haleconnect`) {#haleconnect}

wetransform INSPIRE/SDI publishing platform. Product: [hale»connect](https://wetransform.to/haleconnect/). CSW is often pycsw-backed — still set `haleconnect`, not `pycsw`, when hale»connect is the public catalog.

**Signals:** “hale connect” / hale»connect branding; `/csw?service=CSW`; `/ows/services/org.` WMS/WFS; hosts `haleconnect.com`, GovConnect, Komm.ONE, and other tenants.

**Confirm:** GET CSW GetCapabilities or the public geoportal home. One record per public cloud or on-prem tenant, not per WMS layer.

| Tool | Query |
|------|-------|
| Google | `"hale connect" OR haleconnect OR "hale»connect" (INSPIRE OR CSW OR geoportal) -site:wetransform.to` |
| Google | `inurl:haleconnect.com/csw OR "powered by hale"` |
| Censys | `web.endpoints.http.body: "hale connect"` |
| FOFA | `body="hale connect"` |

## STAC API (`stacserver`) {#stacserver}

Static catalogs (`catalog.json`) and STAC API. Index: [stacindex.org/catalogs](https://stacindex.org/catalogs).

**Confirm:** GET `https://host/stac` or `/catalog.json` with `"type": "Catalog"` or STAC API `"/conformance"` plus `/collections`. Register the **API root**, not every collection.

| Tool | Query |
|------|-------|
| Google | `"stac" "catalog.json" OR inurl:/stac filetype:json` |
| Censys | `web.endpoints.http.body: "stac_version"` |
| FOFA | `body="stac_version"` |

Do not add STAC **items** as catalogs.

## STAC Browser (`stacbrowser`) {#stacbrowser}

Radiant Earth STAC Browser (or a fork) as the **public catalog UI**. Confirm the HTML app title/footer mentions STAC Browser and that it points at a STAC API.

If that API is already registered as `stacserver` on the same host, do **not** add a second record unless the browser is the only public product (API is private or on another origin already listed). Prefer `stacserver` when both are public on the same origin.

**GitHub, do both.** Code search does not index most forks. Upstream is [radiantearth/stac-browser](https://github.com/radiantearth/stac-browser). `index.html` contains the noscript “STAC Browser doesn't work properly”. `config.js` holds `catalogUrl` — that value is the catalog to consider. A null `catalogUrl` is a generic browser, not a catalog.

| Tool | Query |
|------|-------|
| GitHub forks | `repos/radiantearth/stac-browser/forks` |
| GitHub code | `"STAC Browser doesn't work properly" filename:index.html` |
| Google | `"stac-browser" OR "radiantearth" catalog` |
| Censys | `web.endpoints.http.body: "stac-browser"` |
| FOFA | `body="stac-browser"` |
| FOFA | `body="STAC Browser doesn't work properly"` |

## openEO (`openeo`) {#openeo}

EO cloud-processing API with a STAC-compatible collection catalog. Site: [openeo.org](https://openeo.org). Backends include Copernicus Data Space, VITO, EODC, mundialis Actinia, and the Google Earth Engine driver.

**Confirm:** GET the API landing page (often `/openeo/1.2/` or `/v1.0/`) JSON with `api_version` plus `endpoints` for `GET /collections` and `GET /processes`. `/.well-known/openeo` lists versions.

| Tool | Query |
|------|-------|
| Google | `"openeo" ("api_version" OR /collections OR /processes) -site:github.com -site:openeo.org` |
| Google | `inurl:/openeo/ (collections OR processes)` |
| Censys | `web.endpoints.http.body: "openeo"` |
| FOFA | `body="openeo"` |

Register the **backend API** root, not Hub HTML alone, unless Hub is the public product (`hub.openeo.org`). Prefer `openeo` over `stacserver` when `/processes` is part of the same API. Skip process-graph playgrounds with no collection list.

## Sentinel Hub (`sentinelhub`) {#sentinelhub}

Earth-observation catalog and processing API (Sinergise / Planet). Docs: [docs.sentinel-hub.com](https://docs.sentinel-hub.com). Official STAC: `https://services.sentinel-hub.com/api/v1/catalog/1.0.0/`. Distinct from generic STAC (`stacserver`) and from Sentinel Hub **openEO** backends (`openeo`).

**Signals:** hostname `*.sentinel-hub.com`; STAC `/api/v1/catalog`; Process API `/api/v1/process`; EO Browser / Copernicus Browser UI.

**Confirm:** GET the STAC catalog root JSON (`type` Catalog/STAC API) or the documented OGC WMS/WMTS. One record per public catalog API (not every collection, not EO Browser as a second catalog if the STAC API is already registered). Prefer `sentinelhub` over `stacserver` on Sentinel Hub hosts.

| Tool | Query |
|------|-------|
| Google | `"Sentinel Hub" (STAC OR catalog OR "EO Browser") -site:github.com` |
| Google | `site:services.sentinel-hub.com catalog` |
| Censys | `web.names: "sentinel-hub.com"` |
| FOFA | `domain="sentinel-hub.com"` |

## pygeoapi (`pygeoapi`) {#pygeoapi}

OGC API Features / Records. **Confirm:** `/` or `/openapi` JSON with `pygeoapi` in generator/headers; `/collections`.

The HTML shell [pygeoapi/templates/_base.html](https://github.com/geopython/pygeoapi/blob/master/pygeoapi/templates/_base.html) serves `static/img/pygeoapi.png` (381 hosts in September 2026). `body="pygeoapi"` matched 476 and includes documentation hosts (`docs.georama.io`). Operators copy `pygeoapi-config.yml` from the repo root. Forks of `geopython/pygeoapi` are the software, not a portal list.

| Tool | Query |
|------|-------|
| GitHub code | `filename:pygeoapi-config.yml` |
| Google | `"pygeoapi" (collections OR "ogc api") -site:github.com` |
| Censys | `web.endpoints.http.body: "static/img/pygeoapi.png"` |
| FOFA | `body="static/img/pygeoapi.png"` |
| Censys | `web.endpoints.http.body: "pygeoapi"` |
| FOFA | `body="pygeoapi"` |

## SmartMet Server (`smartmetserver`) {#smartmetserver}

FMI open-source MetOcean data server ([fmidev/smartmet-server](https://github.com/fmidev/smartmet-server)). **Confirm:** HTTP `Server` header `SmartMet Server`, plus a live plugin: `/wms?service=WMS&request=GetCapabilities` titled SmartMet, `/edr/collections` JSON, `/wfs?service=WFS&request=GetCapabilities`, or `/timeseries` (HTTP 400 without params still means the plugin is loaded). Typical `catalog_type` is Geoportal. Register **one public tenant per independently operated host**. Do **not** add a second copy of the same cluster: `data.fmi.fi` is the API-key twin of `opendata.fmi.fi`; `harmonia.geoss.space` and `urban.geoss.space` alias `data.geoss.space`. Skip SmartMet **Workstation** / SmartMet **Alert** forecast-production installs (no public catalog API). The site root often 404s — probe plugins, not `/`.

[AsyncConnection.cpp](https://github.com/fmidev/smartmet-server/blob/master/source/AsyncConnection.cpp) sets the `Server` header to `SmartMet Server` (48 hosts in September 2026, including `opendata.fmi.fi` and FMI address-space IPs). The document root on many installs is the plain text `SmartMet Server`. That body string is what FOFA still sees when nginx replaces the `Server` header (`modelo.aviamet.com.co`). Hosts whose root is a 404 HTML page match the header query and not the body query, so run both. `body="Web Map Service Powered by SmartMet Server"` (the default `abstract` in [docker-smartmetserver `wms.conf`](https://github.com/fmidev/docker-smartmetserver/blob/master/smartmetconf/plugins/wms.conf)) returned 0 FOFA hits because GetCapabilities URLs are not crawled.

FMI country installs are GitHub organizations named `smartmet-{iso2}` (14 orgs in September 2026: `bt`, `co`, `ee`, `et`, `ge`, `jm`, `ke`, `kg`, `rw`, `tj`, `tz`, `ua`, `uz`, `vn`) plus [`meteofi/portainer`](https://github.com/meteofi/portainer). The public hostname is the Traefik label `traefik.http.routers.smartmetserver.rule=Host(...)` in `smartmetserver/docker-compose.yml`. Code search misses orgs that commit `docker-compose.yaml` (Uzbekistan); read `APPDOMAIN` in `portainer/docker-compose.yaml` (`data.${APPDOMAIN}` → `data.apps.meteo.uz`). Forks of `fmidev/smartmet-server` are the software, not a portal list. Keep a host only when `/edr/collections` or WMS `GetCapabilities` lists datasets, or `/timeseries` returns values (`X-TimeSeriesPlugin-Error: The 'param' option is required!` on a bare GET only proves the plugin is loaded).

| Tool | Query |
|------|-------|
| GitHub code | `routers.smartmetserver.rule` |
| GitHub orgs | `smartmet-{iso2}` portainer compose `Host()` |
| Google | `"SmartMet Server" (WMS OR EDR OR timeseries OR WFS) -site:github.com` |
| Censys | `web.endpoints.http.body: "SmartMet Server"` |
| FOFA | `header="SmartMet Server"` |
| FOFA | `body="SmartMet Server"` |
| urlscan | `page.server:SmartMet` |

## MapStore (`mapstore`) {#mapstore}

GeoSolutions MapStore. **Signals:** `/mapstore`, `MapStore2`. The splash in `web/client/indexTemplate.html` uses the class `_ms2_init_text` (507 hosts in September 2026). `body="Loading MapStore"` in the same file matched 218.

Do **not** set `mapstore` on GAUSS WebCity / WebPresenter tenants (`{org}.gis.ba`, `/webcity/`, `logo_gauss.png`) — use `gausswebcity` ([viewers](discovery-geoportals-viewers.md#gausswebcity)).

| Tool | Query |
|------|-------|
| Google | `"MapStore" geoportal OR inurl:/mapstore -site:github.com` |
| Censys | `web.endpoints.http.body: "_ms2_init_text"` |
| FOFA | `body="_ms2_init_text"` |
| Censys | `web.endpoints.http.body: "MapStore"` |
| FOFA | `body="MapStore"` |

## QWC2 (`qwc2`) {#qwc2}

QGIS Web Client 2. **Signals:** `qwc2`, `qwc-services`, `/theme/` map UI, `assets/css/qwc2.css` (Schaumburg `/maps/`). That stylesheet path is the `<link>` in upstream `index.html` (430 hosts in September 2026). Do **not** set `qwc2` from `{tenant}.tergis.lv` (use `tergis`).

| Tool | Query |
|------|-------|
| Google | `"QWC2" OR "QGIS Web Client" geoportal` |
| Censys | `web.endpoints.http.body: "assets/css/qwc2.css"` |
| FOFA | `body="assets/css/qwc2.css"` |
| Censys | `web.endpoints.http.body: "qwc2"` |
| FOFA | `body="qwc2"` |

## Mapbender (`mapbender`) {#mapbender}

Open-source geoportal framework (WhereGroup). **Signals:** Mapbender application UI, `/mapbender/application/` or `/mapbender/app.php/application/`, configurable map viewers on OGC services. Symfony publishes `src/Mapbender/CoreBundle/Resources/public` at `/bundles/mapbendercore/` (189 hosts in September 2026, including `harmonisiert.geoportal-suedhessen.de`). `Mapbender.MapModelBase` in `frontend.js` is minified out of the served page. A homepage that JS-redirects to `/mapbender/application/{name}` (Offenbach) counts. Vendor: [mapbender.org](https://mapbender.org). Do **not** set `mapbender` on a CMS hub that only links another agency’s Mapbender (Merzig-Wadern → Saarland; Trier-Saarburg → GeoPortal.rlp).

| Tool | Query |
|------|-------|
| Google | `"Mapbender" (geoportal OR Anwendung OR "map application") -site:github.com -site:mapbender.org` |
| Google | `inurl:/application/ mapbender` |
| Censys | `web.endpoints.http.body: "bundles/mapbendercore"` |
| FOFA | `body="bundles/mapbendercore"` |
| Censys | `web.endpoints.http.body: "Mapbender"` |
| FOFA | `body="Mapbender"` |

Do not register a Mapbender app that is only a login shell with no public map list.

## MapTiler Server (`maptilerserver`) {#maptilerserver}

Self-hosted tile and map-style catalog. Default port **3650**; production sites often sit behind HTTPS on 443. **Signals:** HTML title `MapTiler Server`, `/admin` login, Next.js `__NEXT_DATA__` `pageProps` (`serverName`, `rasterizationEnabled`, `type`). `type: list` is a public catalog page. `type: logoOnly` hides that page behind a logo, but the catalog API can still list data.

The homepage does not embed the dataset list. **Confirm datasets** with `GET https://host/api/frontpage`, which returns `{maps, activeTileSets}`. Keep a host when either list is non-empty. Skip staging hostnames (`dev`, `qa`, `demo`) and vendor-sample installs whose only tileset is `MapTiler Data (Zurich sample)` or `MapTiler Satellite Demo Zürich`. Register one record per `instanceId` (Dawonia housing hostnames share `e8bce03b` with `www.maptiler.dawonia.de`). Register the public catalog root, not `/admin`. A `logoOnly` host with a non-empty frontpage is still a catalog. Bare `/api/maps` 404s; a style check is `GET /api/maps/{mapId}/style.json`.

`body="rasterizationEnabled"` is the stable HTML fingerprint (170 hosts in September 2026, all titled MapTiler Server). `body="AUTH_FAKE_TOKEN"` matches newer Next.js builds only (185 hosts) and misses older shells such as `tiles.atlas.mchs.gov.ru`. `body="/api/frontpage"` is not a fingerprint.

| Tool | Query |
|------|-------|
| Google | `intitle:"MapTiler Server" -site:maptiler.com -site:github.com` |
| Censys | `web.endpoints.http.html_title: "MapTiler Server"` |
| FOFA | `title="MapTiler Server"` |
| Censys | `web.endpoints.http.body: "rasterizationEnabled"` |
| FOFA | `body="rasterizationEnabled"` |
| Censys | `web.endpoints.http.body: "AUTH_FAKE_TOKEN"` |
| FOFA | `body="AUTH_FAKE_TOKEN"` |
| FOFA | `body="MapTiler Server"` |
| Shodan | `http.title:"MapTiler Server"` |

## MapServer (`mapserver`) {#mapserver}

OGC service middleware (WMS/WFS/WCS from a mapfile). Register it when MapServer is the **public catalog** (GetCapabilities or a map list as the product), not merely the renderer behind Lizmap, QWC2, GeoNetwork, or p.mapper.

**Confirm:** WMS `GetCapabilities` whose service metadata mentions MapServer (`cgi-bin/mapserv`, `mapserv.exe`, or a `MapServer` keyword). Typical paths: `/cgi-bin/mapserv`, `/cgi-bin/mapserv.cgi`, or a named `.map` URL.

[maperror.c](https://github.com/MapServer/MapServer/blob/main/src/maperror.c) writes `MapServer version` into the server message (47 hosts in September 2026, including `map.feltgis.no`). `body="MapServer"` is not usable: it matched 30,476 unrelated hosts.

| Tool | Query |
|------|-------|
| Google | `inurl:cgi-bin/mapserv (WMS OR GetCapabilities)` |
| Google | `"MapServer" GetCapabilities -site:mapserver.org -site:github.com` |
| Censys | `web.endpoints.http.body: "MapServer version"` |
| FOFA | `body="MapServer version"` |
| Shodan | `http.html:"MapServer version"` |

Do not add a second record for MapServer on a host that already has a Lizmap, QWC2, GeoNetwork, or p.mapper catalog pointing at the same services. Do **not** set `mapserver` on `{city}.geo-portale.it` `/pmapper-4.2.0/` UIs (`pmapper`).

## QGIS Server (`qgisserver`) {#qgisserver}

OGC service middleware from a QGIS project (WMS/WFS/WCS, OGC API). Register it when QGIS Server is the **public catalog** (GetCapabilities as the product), not merely the renderer behind Lizmap, QWC2, or mviewer.

**Confirm:** WMS `GetCapabilities` whose service metadata mentions QGIS Server (`qgis_mapserv.fcgi`, `MAP=` `.qgs` / `.qgz`, or a `QGIS` keyword). Typical paths: `/cgi-bin/qgis_mapserv.fcgi`, `/ows`, or a named `.qgs` URL.

| Tool | Query |
|------|-------|
| Google | `inurl:qgis_mapserv.fcgi (WMS OR GetCapabilities)` |
| Google | `"QGIS Server" GetCapabilities -site:qgis.org -site:github.com` |
| Censys | `web.endpoints.http.body: "QGIS Server"` |
| FOFA | `body="QGIS Server"` |
| Shodan | `http.html:"QGIS Server"` |

Do not add a second record for QGIS Server on a host that already has a Lizmap, QWC2, or mviewer catalog pointing at the same services.

## mviewer (`mviewer`) {#mviewer}

GéoBretagne thematic map viewer (OpenLayers). Common in French régions, départements, and communes. Site: [mviewer.github.io](https://mviewer.github.io). Distinct from Lizmap (`lizmap`) and QWC2 (`qwc2`).

**Signals:** `mviewer` in HTML/JS; config XML under `/apps/` (often `default.xml`); optional mviewerstudio; GéoBretagne / Kartenn branding.

**Confirm:** GET the viewer URL and match mviewer JS plus a public layer/theme config. One record per public application (config), not per layer.

**GitHub, do both.** Code search does not index most forks. Upstream is [geobretagne/mviewer](https://github.com/geobretagne/mviewer). `index.html` links `css/mviewer.css` (88 hosts in September 2026).

| Tool | Query |
|------|-------|
| GitHub forks | `repos/geobretagne/mviewer/forks` |
| GitHub code | `css/mviewer.css filename:index.html` |
| Google | `"mviewer" (géoportail OR geoportail OR "openlayers") -site:github.com -site:mviewer.github.io` |
| Google | `inurl:mviewer (apps OR config.xml) site:.fr` |
| Censys | `web.endpoints.http.body: "css/mviewer.css"` |
| FOFA | `body="css/mviewer.css"` |
| Censys | `web.endpoints.http.body: "mviewer"` |
| FOFA | `body="mviewer"` |

Skip mviewerstudio admin and demo configs on mviewer.github.io unless the task is to record them.

## Isogeo (`isogeo`) {#isogeo}

French SaaS GIS metadata catalog (OpenCatalog / App). Vendor: [isogeo.com](https://www.isogeo.com). Distinct from IsiGéo (`isigeo`, Geomatika).

**Signals:** title or footer “Isogeo” / OpenCatalog; path `/api` OpenAPI; ISO 19115 inventory; often CSW.

**Confirm:** GET `/api` (OpenAPI mentioning Isogeo) or the public OpenCatalog search UI. One record per public catalog, not per metadata sheet.

| Tool | Query |
|------|-------|
| Google | `"Isogeo" (OpenCatalog OR géocatalogue OR "catalogue de données") site:.fr -site:isogeo.com` |
| Google | `"powered by Isogeo" OR "OpenCatalog Isogeo"` |
| Censys | `web.endpoints.http.body: "Isogeo"` |
| FOFA | `body="Isogeo"` |

Do not set `isigeo` (IsiGéo) for an Isogeo OpenCatalog.

## gvSIG Online (`gvsigonline`) {#gvsigonline}

Municipal / regional SDI built by the gvSIG Association. Demo and docs: [demo.gvsigonline.com](https://demo.gvsigonline.com/gvsigonline/core/documentation/). GeoServer is required underneath; optionally GeoNetwork.

**Signals:** path `/gvsigonline/`; public project picker `select_public_project`; title or footer “gvSIG Online”.

**Confirm:** GET `https://host/gvsigonline/` (or the catalog `link`) and match the gvSIG Online UI. Prefer the public viewer root, not `/geoserver/web`. Skip the demo unless the task is to record it.

[base.html](https://github.com/gvSIGAssociation/gvsig-online/blob/master/gvsigol/gvsigol_core/templates/base.html) links `css/gvsigOL.css` (63 hosts in September 2026, including `visualizador.ide.uy`). `body="select_public_project"` matched 53. `body="gvSIG Online"` matched 73, the same product, so keep both.

| Tool | Query |
|------|-------|
| Google | `"gvSIG Online" (geoportal OR visor OR IDE) -site:gvsig.com -site:github.com` |
| Google | `inurl:/gvsigonline/ select_public_project` |
| Censys | `web.endpoints.http.body: "gvsigOL.css"` |
| FOFA | `body="gvsigOL.css"` |
| Censys | `web.endpoints.http.body: "select_public_project"` |
| FOFA | `body="select_public_project"` |
| Censys | `web.endpoints.http.body: "gvSIG Online"` |
| FOFA | `body="gvSIG Online"` |

One record per public SDI UI. Do not also register the bundled GeoServer as a separate catalog on the same host.

## deegree (`deegree`) {#deegree}

Open-source Java SDI stack (WMS, WFS, WMTS, CSW, WPS, and deegree ogcapi). Used as INSPIRE service middleware.

**Confirm:** GetCapabilities on `/deegree-webservices`, `/services`, or a documented service path whose XML mentions deegree. CSW and OGC API Features are enough to treat it as a catalog when that is the public product.

| Tool | Query |
|------|-------|
| Google | `"deegree" (CSW OR WMS OR "ogcapi") GetCapabilities -site:github.com -site:deegree.org` |
| Censys | `web.endpoints.http.body: "deegree"` |
| FOFA | `body="deegree"` |
| Shodan | `http.html:"deegree"` |

## VertiGIS WebOffice (`weboffice`) {#weboffice}

Commercial web GIS (formerly SynerGIS WebOffice) on ArcGIS Enterprise. Vendor: [vertigis.com](https://www.vertigis.com). Multi-tenant hosts: `wo-hosting.vertigis.com`, `map.geoportal.at`.

**Signals:** `/synserver` or `/WebOffice/synserver`; HTML title `VertiGIS WebOffice`; `weboffice_packed.css`; core, flex, or mobile clients. A WebInfo landing that POSTs to `./synserver` and loads `weboffice_modern_user.css` (Landkreis Osnabrück) also counts.

**Confirm:** GET the synserver URL and match the title plus `weboffice_packed.css`, or the WebInfo guest landing plus `synserver`. One record per public client (tenant), not per map project. Do **not** set `weboffice` on a CMS Bürgerportal that only links an already-registered `wo-hosting.vertigis.com` client (Radolfzell).

| Tool | Query |
|------|-------|
| Google | `intitle:"VertiGIS WebOffice" OR inurl:/synserver WebOffice` |
| Google | `site:wo-hosting.vertigis.com OR site:map.geoportal.at` |
| Censys | `web.endpoints.http.html_title: "VertiGIS WebOffice"` |
| FOFA | `title="VertiGIS WebOffice"` |
| Censys | `web.endpoints.http.body: "weboffice_packed.css"` |
| FOFA | `body="weboffice_packed.css"` |

## Geocortex Essentials (`geocortex`) {#geocortex}

Commercial web GIS (Latitude Geographics, now VertiGIS Studio) on ArcGIS. Vendor: [geocortex.com](https://www.geocortex.com). Hosted tenants: `*.geocortex.com`. Distinct from VertiGIS WebOffice (`weboffice`) and VertiGIS Studio Web (`vertigisstudioweb`).

**Signals:** title `Geocortex Essentials Sites Directory` or `Geocortex Viewer for HTML5`; path `/Geocortex/Essentials/` (sometimes `/ess/`) plus `/REST/sites`; `/Html5Viewer/`; footer “licensed Geocortex Essentials”. The HTML5 host page (`Index.html`) loads `Resources/Compiled/loader.js` and mentions `geocortexUseLocalEsriApi`, including when the title is rewritten.

**Confirm:** GET `https://host/Geocortex/Essentials/REST/sites?f=pjson` (instance path may include `/public/`, `/EXT/`, or a named instance). `ViewerSettings.json.js` beside the viewer lists site ids when the folder is not `/Html5Viewer/`. JSON `sites` array is the catalog. Keep a record only when a public site’s `.../sites/{id}/map?f=pjson` lists operational layers. HTML5 viewers are the public map UI, not extra catalogs. One record per Essentials instance, not per site or viewer. Do not also register the bundled ArcGIS REST root as a second Geocortex catalog; keep an existing `arcgisserver` record on the same host if that is already the services directory.

| Tool | Query |
|------|-------|
| Google | `intitle:"Geocortex Essentials Sites Directory"` |
| Google | `intitle:"Geocortex Viewer for HTML5" -site:github.com` |
| Google | `inurl:/Geocortex/Essentials/REST/sites OR inurl:/Html5Viewer/` |
| Google | `site:geocortex.com Html5Viewer OR Essentials -www -shop -accounts` |
| Censys | `web.endpoints.http.html_title: "Geocortex Essentials Sites Directory"` |
| FOFA | `title="Geocortex Essentials Sites Directory"` |
| Censys | `web.endpoints.http.html_title: "Geocortex Viewer for HTML5"` |
| FOFA | `title="Geocortex Viewer for HTML5"` |
| FOFA | `body="Geocortex Essentials"` |
| FOFA | `body="/Html5Viewer/" && body="Geocortex"` |
| FOFA | `body="Resources/Compiled/loader.js"` |
| FOFA | `body="geocortexUseLocalEsriApi"` |
| FOFA | `body="Resources/Images/Icons/iOS/apple-touch-icon-ipad-retina.png"` |
| FOFA | `domain="geocortex.com"` |

`loader.js` and `geocortexUseLocalEsriApi` are in the HTML5 viewer host page, so they match rewritten titles (50 and 52 hosts in September 2026). The apple-touch icon path is the same page (50). `body="Resources/Styles/splash.css"` (68) also matches unrelated sites. `domain="geocortex.com"` (64) is the hosted-tenant list and includes vendor mail, docs, and status hosts.

Skip `gedemo.geocortex.com`, test and dev hosts, empty Sites Directories, and sites whose map JSON is only `403`.

## VertiGIS Studio Web (`vertigisstudioweb`) {#vertigisstudioweb}

Configurable web GIS viewer (formerly Geocortex Web / GXW) on ArcGIS Online or Portal for ArcGIS. Vendor: [vertigis.com](https://www.vertigis.com/studio/web/). SaaS: `apps.vertigisstudio.com`, `apps.vertigisstudio.eu`. Distinct from Geocortex Essentials (`geocortex`) and VertiGIS WebOffice (`weboffice`).

**Signals:** `/vertigisstudio/web/?app=`; `/gcx/WebViewer/?app=`; `/Geocortex/WebViewer/?app=` (not `/Html5Viewer/` and not `/Geocortex/Essentials/REST/sites`); HTML `#gcx-app`; GA title `VertiGIS Studio Web`; SaaS shells are often ~728 bytes.

**Confirm:** GET the viewer URL and match `#gcx-app` plus VertiGIS Studio Web branding. One record per public tenant, not every `?app=` GUID. Keep an existing `arcgisserver` or `geocortex` record on the same host if that is already the services directory or Html5Viewer.

| Tool | Query |
|------|-------|
| Google | `inurl:vertigisstudio/web/?app=` |
| Google | `inurl:/gcx/WebViewer/?app= OR inurl:/Geocortex/WebViewer/?app=` |
| Google | `site:apps.vertigisstudio.com/web OR site:apps.vertigisstudio.eu/web` |
| Censys | `web.endpoints.http.html_title: "VertiGIS Studio Web"` |
| FOFA | `title="VertiGIS Studio Web"` |
| FOFA | `body="gcx-app"` |
| FOFA | `body="/vertigisstudio/web/"` |

Skip vendor Designer samples, login-only Designer, and extra app GUIDs on a tenant already registered.

## GeoMedia WebMap (`geomediawebmap`) {#geomediawebmap}

Hexagon / Intergraph Geospatial Portal (GeoMedia WebMap Publisher Portal). Typical paths: `/geoportal01/`, `/cdngiportal/`, `/msip/Full.aspx`, `/Online_Mapping/`, `/hartagisoradea/`.

**Signals:** `Version:` and `Licensed to:` in the UI; `Intergraph.WebSolutions`; `$GP.` JavaScript; `Compositor.WebClient.ashx`, `CRSNames.WebClient.ashx`, or related `WebClient.ashx` handlers; title may say Geospatial Portal or GeoMedia WebMap Publisher Portal.

**Confirm:** GET the portal URL and match at least two of those fingerprints. Skip staff-only intranet portals that require authentication for any map list.

| Tool | Query |
|------|-------|
| Google | `"Geospatial Portal" ("Licensed to" OR Intergraph) -site:hexagon.com` |
| Google | `"GeoMedia WebMap" (portal OR geoportal)` |
| Google | `inurl:/geoportal01/ OR inurl:/cdngiportal/ OR inurl:/msip/Full.aspx` |
| Censys | `web.endpoints.http.body: "Intergraph.WebSolutions"` |
| FOFA | `body="Intergraph.WebSolutions"` |

## Micka (`micka`) {#micka}

Czech/Slovak metadata catalog. **Signals:** `/micka`, HSLayers, “Micka”.

The catalog layout [@layout.latte](https://github.com/hsrs-cz/Micka/blob/master/php/app/modules/Catalog/templates/default/@layout.latte) links `micka.css` (9 hosts in September 2026, including `metadata.vumop.cz`). `body="micka"` is not usable: it matched 3,301 unrelated hosts, including `ranstatradgard.se`.

| Tool | Query |
|------|-------|
| Google | `"Micka" (metadata OR geoportal OR CSW) site:.cz OR site:.sk` |
| Censys | `web.endpoints.http.body: "micka.css"` |
| FOFA | `body="micka.css"` |

## HSLayers NG (`hslayersng`) {#hslayersng}

Czech open-source web mapping framework (Angular + OpenLayers + CesiumJS) used for map-composition catalogs; usually paired with a [Layman](#layman) backend and often a Micka CSW sibling. Typical deployments: Hub4Everybody-platform hubs (`/map/`, `/mapy/` pages with composition galleries). **Signals:** `hslayers` / `hslayers-ng` JS bundles, `layman-proxy` or `/rest/workspaces/{workspace}/maps` composition URLs, “Hub4Everybody” platform links.

**Confirm:** GET the map app and match `hslayers` in the page, then verify the Layman REST listing (`/rest/workspaces/<workspace>/maps` or `/layman-proxy/rest/workspaces/<workspace>/maps`) returns a JSON array with `access_rights`. One record per public map hub. **Skip** ISP network-coverage viewers (HsOptika portals such as `hsoptika.*` / `optika.*`), single-map embeds on municipal pages, the dead official demo (`ng.hslayers.org` redirects to the GitHub wiki), and WordPress front pages that merely link to the platform.

| Tool | Query |
|------|-------|
| Google | `"hslayers" (geoportal OR map OR compositions) -site:github.com` |
| Google | `inurl:/mapy/ OR inurl:/map/ "hub4everybody"` |
| Censys | `web.endpoints.http.body: "hslayers-ng"` |
| FOFA | `body="hslayers"` (expect HsOptika ISP noise) or `body="hub4everybody"` |

## Layman (`layman`) {#layman}

Open-source geodata publication server (Layer Manager) by CCSS / Plan4all: REST API for layers and map compositions over GeoServer / PostGIS / QGIS Server with Micka metadata. Almost always reached through an [HSLayers NG](#hslayersng) client, so hunt the client fingerprints above; the server itself answers JSON at `/rest/workspaces/...` (root `/rest/` may 404 while item paths resolve). **Signals:** `/rest/workspaces/`, `/layman-proxy`, “Layman Test Client”.

**Confirm:** GET `/rest/workspaces/<workspace>/maps/<name>` or the workspace maps listing and match Layman JSON (`access_rights` with `EVERYONE`, `bounding_box`, `file.path`). Public workspaces are readable without login.

| Tool | Query |
|------|-------|
| Google | `inurl:/rest/workspaces/ maps layman` |
| Censys | `web.endpoints.http.body: "/rest/workspaces/"` |
| FOFA | `body="/layman/rest"` or `title="Layman Test Client"` |

## GeoBlacklight (`geoblacklight`) {#geoblacklight}

Library geoportals (often US universities). Showcase: [geoblacklight.org/showcase](https://geoblacklight.org/showcase/). The home partial `app/views/catalog/_home_text.html.erb` includes `id="geoblacklight-version"` (62 hosts in September 2026). That div is on the home page, so keep `body="geoblacklight"` for record pages FOFA indexed without the home markup.

| Tool | Query |
|------|-------|
| Google | `"GeoBlacklight" OR inurl:/catalog geoblacklight site:.edu` |
| Censys | `web.endpoints.http.body: "geoblacklight-version"` |
| FOFA | `body="geoblacklight-version"` |
| Censys | `web.endpoints.http.body: "geoblacklight"` |
| FOFA | `body="geoblacklight"` |

## Oskari (`oskari`) {#oskari}

Finnish SDI map client. **Signals:** `Oskari`, `/Oskari/`, map full-screen UI.

**Confirm:** GET the public map UI. One record per independent portal. **Reject** Oskari RPC embeds of another catalog (Suomi.fi Maps / HKP `hkp.maanmittauslaitos.fi` embeds on Kalastusrajoitus.fi and similar) and login-walled publishers (API 403).

[servlet-map/.../spring-map-jsp/index.jsp](https://github.com/oskariorg/oskari-server/blob/master/servlet-map/src/main/resources/META-INF/resources/spring-map-jsp/index.jsp) links `oskari.min.css` (39 hosts in September 2026, including `kartta.museoverkko.fi`). `body="Oskari"` matched 2,044 hosts, including pages that use the Finnish name and are not the map client.

| Tool | Query |
|------|-------|
| Google | `"Oskari" (geoportal OR kartta) -site:oskari.org` |
| Censys | `web.endpoints.http.body: "oskari.min.css"` |
| FOFA | `body="oskari.min.css"` |
| Censys | `web.endpoints.http.body: "Oskari"` |
| FOFA | `body="Oskari"` |

## Esri Geoportal Server (`esrigeo`) {#esrigeo}

Older Esri metadata catalog (not Hub). **Signals:** `/geoportal`, Geoportal Server, CSW.

| Tool | Query |
|------|-------|
| Google | `"Geoportal Server" Esri OR inurl:/geoportal/csw` |
| Censys | `web.endpoints.http.body: "Geoportal Server"` |
| FOFA | `body="Geoportal Server"` |

## disy Cadenza (`cadenza`) {#cadenza}

German public-sector geoanalytics / geoportal (Cadenza Web and Cadenza Workbooks). Vendor: [disy.net](https://www.disy.net/en/products/disy-cadenza/overview/).

**Signals:** path `/cadenza/`, `/public/`, `/pages/map/`, or `/fachauswertungweb/`; HTML/JS contains `cadenza` and often `disy`; workbook navigator or JSF `*.xhtml` map pages; guest login before the public theme tree. Root may return HTTP 401 with an HTML login/guest page — that is still a public catalog if guest access exists.

**Confirm:** GET the catalog URL and match at least two of: `cadenza` in HTML, `disy` branding, Cadenza Web/Workbooks UI, or a working public map permalink. Do not add staff-only Cadenza (police, intranet Energieatlas, bathing-water ops tools). One record per public catalog UI, not per workbook or theme on the same host.

| Tool | Query |
|------|-------|
| Google | `"Cadenza Web" OR "disy Cadenza" (Umwelt OR Kartendienst OR Geoportal) site:.de` |
| Google | `inurl:/cadenza/ (UDO OR iDA OR Kartendienst)` |
| Censys | `web.endpoints.http.body: "cadenza"` |
| FOFA | `body="cadenza"` |

## WIS 2.0 Box (`wis20box`) {#wis20box}

WMO WIS2 reference node for publishing meteorological and related geospatial data. Source: [wmo-im/wis2box](https://github.com/wmo-im/wis2box).

**Signals:** `wis2box` in HTML or API; pygeoapi / OGC API Features alongside WIS2 messaging; WMO WIS2 branding.

**Confirm:** GET the public discovery UI or OGC API landing page. Register the node catalog, not an individual dataset or MQTT topic. The [WMO WIS2 Global Discovery Catalogue](https://gdc.wis.cma.cn/) (CMA instance) is a named-list hunt for *other* WIS2 nodes — duplicate-check before adding.

[index.html](https://github.com/wmo-im/wis2box-ui/blob/main/index.html) sets the Open Graph title `WIS 2.0 node in a box` (321 hosts in September 2026, including `wis2.meteo.gov.gh`). `body="wis2box"` matched 445, the same product, so keep both.

| Tool | Query |
|------|-------|
| Google | `"wis2box" OR "WIS 2.0 Box" (pygeoapi OR "OGC API") -site:github.com` |
| Censys | `web.endpoints.http.body: "WIS 2.0 node in a box"` |
| FOFA | `body="WIS 2.0 node in a box"` |
| Censys | `web.endpoints.http.body: "wis2box"` |
| FOFA | `body="wis2box"` |

## GET SDI Portal (`getsdiportal`) {#getsdiportal}

Geospatial Enabling Technologies SDI client over GeoServer / GeoNetwork. Common in Greek municipal and regional SDIs.

**Signals:** tabbed UI (map, metadata, files, services); GET SDI / GETMAP branding; CSW plus WMS/WFS.

**Confirm:** GET the portal home and match the tabbed SDI UI. Do not also register the bundled GeoServer on the same host.

[index.php](https://github.com/GeospatialEnablingTechnologies/GET-SDI-Portal/blob/master/index.php) only loads `js/loader.js`. `body="GET SDI"` matched 30 hosts in September 2026, and the first hits are `www.sdipresence.com` and `www.getmap.eu`. `body="GET SDI Portal"` matched 3: the vendor site and `84.205.223.98` (Athens GIS). The version banner lives in `license.txt`, not an HTML template.

| Tool | Query |
|------|-------|
| Google | `"GET SDI Portal" OR "GETMAP" (geoportal OR CSW) -site:getmap.eu` |

## MapProxy (`mapproxy`) {#mapproxy}

Open-source map cache/proxy. Register only when MapProxy is the **public catalog** (demo viewer + service list), not a silent cache behind another geoportal.

**Confirm:** GET `/demo/` or WMTS/WMS GetCapabilities whose service title mentions MapProxy.

[static.html](https://github.com/mapproxy/mapproxy/blob/master/mapproxy/service/templates/demo/static.html) titles the catalog page `MapProxy Demo` (56 hosts in September 2026, including `188.68.223.69`). `body="MapProxy"` matched 1,990, including tile caches such as `tiles.trafimage.ch`. Keep both.

| Tool | Query |
|------|-------|
| Google | `intitle:"MapProxy" (demo OR WMTS) -site:github.com -site:mapproxy.org` |
| Censys | `web.endpoints.http.body: "MapProxy Demo"` |
| FOFA | `body="MapProxy Demo"` |
| Censys | `web.endpoints.http.body: "MapProxy"` |
| FOFA | `body="MapProxy"` |

## Terria (`terria`) {#terria}

Open-source catalog-driven map portal (TerriaJS). Site: [terria.io](https://terria.io).

**Signals:** TerriaJS / National Map-style catalog tree; `config.json` + `catalog.json`; Magda or CKAN-backed catalogs behind the viewer.

**Confirm:** GET the viewer and a working catalog JSON. If the same datasets are already a CKAN/Magda catalog on that host, prefer the dataset CMS unless the map is the primary product.

[index.ejs](https://github.com/TerriaJS/terriajs/blob/main/apps/terriamap/wwwroot/index.ejs) sets `class="terria"` on the root element (461 hosts in September 2026, including `map.geo-rapp.org`). `body="Terria"` matched 1,314. Branded shells can omit the class, so keep both.

| Tool | Query |
|------|-------|
| Google | `"Terria" (catalog OR "National Map") -site:github.com` |
| Censys | `web.endpoints.http.body: "class=\"terria\""` |
| FOFA | `body="class=\"terria\""` |
| Censys | `web.endpoints.http.body: "Terria"` |
| FOFA | `body="Terria"` |

## MapBiomas (`mapbiomas`) {#mapbiomas}

Land-cover collections and map viewers. Country nodes (Brazil, Indonesia, and others) share the MapBiomas web app. Site: [mapbiomas.org](https://mapbiomas.org).

**Confirm:** GET the country node and match MapBiomas collections UI. One record per public country/program portal.

| Tool | Query |
|------|-------|
| Google | `"MapBiomas" (coleções OR collections OR geoportal)` |
| Censys | `web.endpoints.http.body: "MapBiomas"` |
| FOFA | `body="MapBiomas"` |

## ERDAS APOLLO (`erdasapollo`) {#erdasapollo}

Hexagon geospatial content management. Vendor: [hexagon.com](https://hexagon.com/products/erdas-apollo).

**Signals:** APOLLO Image Manager / Web Client; ERDAS APOLLO in HTML; WMS/WMTS/CSW from an APOLLO catalog.

**Confirm:** GET the public discovery client (not an intranet Image Manager). Skip login-only enterprise catalogs.

| Tool | Query |
|------|-------|
| Google | `"ERDAS APOLLO" (WMS OR catalog OR geoportal) -site:hexagon.com` |
| Censys | `web.endpoints.http.body: "ERDAS APOLLO"` |
| FOFA | `body="ERDAS APOLLO"` |

## pycsw (`pycsw`) {#pycsw}

OGC CSW and OGC API – Records server. Site: [pycsw.org](https://pycsw.org/). Register when pycsw is the public catalog, not only the CSW backend of GeoNode/GeoNetwork.

**Confirm:** CSW `GetCapabilities` or OGC API Records landing page mentioning pycsw.

[_base.html](https://github.com/geopython/pycsw/blob/master/pycsw/templates/_base.html) loads `pycsw-logo-vertical.png` (37 hosts in September 2026, including `pycsw.studiogis.eu`). `body="pycsw"` matched 700, including MS4W pages that only mention the server. Keep both.

| Tool | Query |
|------|-------|
| Google | `"pycsw" (CSW OR "OGC API" Records) -site:github.com -site:pycsw.org` |
| Censys | `web.endpoints.http.body: "pycsw-logo-vertical.png"` |
| FOFA | `body="pycsw-logo-vertical.png"` |
| Censys | `web.endpoints.http.body: "pycsw"` |
| FOFA | `body="pycsw"` |

## Koordinates (`koordinates`) {#koordinates}

Cloud geospatial data platform. Hosts: `*.koordinates.com` plus custom government domains. Site: [koordinates.com](https://koordinates.com).

**Confirm:** GET `/services/api/v1.x/data/` and keep the host only when `X-Resource-Range` reports a count above 0. One record per tenant catalog. Publisher pages on `koordinates.com` (`/from/{org}/data/`) are the hub, not a second catalog. Login hosts (`id.koordinates.com`) and `Warehouse Not Found` redirects are not catalogs.

Every public portal’s HTML preloads `https://assets.koordinates.com/fe/boot.js` and sets `kx_boot_file` (19 hosts on 24 September 2026, all already registered, including `data.linz.govt.nz` and `lris.scinfo.org.nz`). `body="Powered by Koordinates"` matched 0. `server="Koordinates"` matched 363, mostly wildcard-certificate noise, 401s, and dead warehouses. `domain="koordinates.com"` matched the same 295-host certificate noise and did not include live tenants such as `scion.koordinates.com`. Keep the boot-script query; use `server="Koordinates"` only to catch a custom domain the body index missed, then require the data API.

| Tool | Query |
|------|-------|
| Google | `site:koordinates.com (data OR layers)` |
| crt.sh | `%.koordinates.com` |
| Censys | `web.endpoints.http.body: "assets.koordinates.com/fe/boot.js"` |
| FOFA | `body="assets.koordinates.com/fe/boot.js"` |
| FOFA | `body="kx_boot_file"` |
| FOFA | `server="Koordinates" && status_code="200"` |

## IRI Data Library (`datalibrary`) {#datalibrary}

Climate / maproom portals (IRI Columbia and meteorological services). Site: [iridl.ldeo.columbia.edu](https://iridl.ldeo.columbia.edu).

**Signals:** Data Library / maproom; gridded download; IRI-style dataset URLs.

**Confirm:** GET a public maproom or dataset browser. One record per public library, not per maproom view.

| Tool | Query |
|------|-------|
| Google | `"Data Library" (maproom OR IRI) (climate OR geospatial) -site:columbia.edu` |
| Censys | `web.endpoints.http.body: "maproom"` |
| FOFA | `body="maproom"` |

## Rasdaman (`rasdaman`) {#rasdaman}

Array database with OGC WCS/WMS/WCPS. Site: [rasdaman.com](https://rasdaman.com). Register the **public service/catalog UI**, not a silent WCS behind another geoportal.

**Confirm:** GetCapabilities or WCPS endpoint that names rasdaman.

| Tool | Query |
|------|-------|
| Google | `"rasdaman" (WCS OR WCPS OR petascope) -site:github.com -site:rasdaman.com` |
| Censys | `web.endpoints.http.body: "rasdaman"` |
| FOFA | `body="rasdaman"` |

## Open Data Cube (`opendatacube`) {#opendatacube}

Earth-observation data cube. Site: [opendatacube.org](https://www.opendatacube.org). Often paired with STAC or `datacubews` (OWS). Prefer STAC/`stacserver` if that is the public catalog; use `opendatacube` when the cube explorer is the product.

**Confirm:** GET the explorer or ODC-indexed catalog UI.

[base.html](https://github.com/opendatacube/datacube-explorer/blob/develop/cubedash/templates/layout/base.html) writes `Open Data Cube v` next to `<span id="datacube-version">` (36 hosts in September 2026, including `explorer.swissdatacube.org` and `explorer.digitalearth.se`). `body="opendatacube"` is not usable: it matched 71 hosts, including `www.opendatacube.org` and the AWS open-data registry.

Forks of [opendatacube/datacube-explorer](https://github.com/opendatacube/datacube-explorer) keep an empty homepage, and code search skips most of them. Read Ingress `host:` values (`filename:ingress.yaml datacube-explorer`). In September 2026 that found `explorer.piksel.big.go.id`, which the footer query had not indexed. Keep a site only when About or a product page reports datasets (`Exploring N datasets`). A staging or `*-dev` host with the same product list is the same catalog.

`body="id=\"datacube-version\""`, `body="datacube-product-name"`, and `body="/audit/dataset-counts"` each returned that same 36-host set on 24 September 2026, including `twodc.colife.org.tw` (`twdc.colife.org.tw` does not connect). `body="cubedash"` and the vendored Font Awesome paths are not usable.

| Tool | Query |
|------|-------|
| Google | `"Open Data Cube" (explorer OR datacube) -site:opendatacube.org -site:github.com` |
| Censys | `web.endpoints.http.body: "Open Data Cube v"` |
| FOFA | `body="Open Data Cube v"` |
| FOFA | `body="id=\"datacube-version\""` |
| FOFA | `body="datacube-product-name"` |
| GitHub | forks of `opendatacube/datacube-explorer`; `filename:ingress.yaml datacube-explorer` |

## Datacube OWS (`datacubews`) {#datacubews}

OGC service layer for Open Data Cube (`datacube-ows`). Docs: [datacube-core.readthedocs.io](https://datacube-core.readthedocs.io). Use when WMS/WCS OWS is the public product, not the cube explorer (`opendatacube`) or a STAC API (`stacserver`).

**Signals:** `datacube-ows` / `datacube_ows`; ODC WMS/WCS GetCapabilities.

**Confirm:** GET WMS or WCS GetCapabilities that names datacube-ows. Same `/collections` grain as Open Data Cube when OWS is the public product.

[index.html](https://github.com/opendatacube/datacube-ows/blob/develop/datacube_ows/templates/index.html) titles the landing page `(datacube-ows)` (51 hosts in September 2026, including `datacube.icc.mn:5000`).

| Tool | Query |
|------|-------|
| Google | `"datacube-ows" OR "datacube_ows"` |
| Censys | `web.endpoints.http.body: "datacube-ows"` |
| FOFA | `body="datacube-ows"` |

## InGrid (`ingrid`) {#ingrid}

German environmental/spatial metadata catalog. Site: [ingrid-oss.eu](https://ingrid-oss.eu). Source: [informationgrid](https://github.com/informationgrid).

**Signals:** InGrid chrome; CSW and OpenSearch; German environmental SDI.

**Confirm:** GET CSW GetCapabilities or the InGrid search UI. One catalog per public node.

| Tool | Query |
|------|-------|
| Google | `"InGrid" (CSW OR Geoportal) site:.de` |
| Censys | `web.endpoints.http.body: "InGrid"` |
| FOFA | `body="InGrid"` |

## GeoPortal.rlp (`geoportalrlp`) {#geoportalrlp}

Rhineland-Palatinate SDI suite (OWS, ISO 19139, map viewer). Source: [mrmap-community/GeoPortal.rlp](https://github.com/mrmap-community/GeoPortal.rlp). Help: [geoportal.rlp.de](https://www.geoportal.rlp.de/article/Hilfe/).

**Confirm:** do **not** re-add known RLP nodes already in the registry. GET CSW or the catalog UI on a distinct node.

| Tool | Query |
|------|-------|
| Google | `geoportal.rlp.de` |
| Censys | `web.names: "geoportal.rlp.de"` |
| FOFA | `host="geoportal.rlp.de"` |

## ncWMS (`ncwms`) {#ncwms}

WMS for NetCDF / multidimensional environmental data. Docs: [ncwms](https://reading-escience-centre.github.io/ncwms/). Register when ncWMS is the public map catalog, not a layer inside THREDDS.

**Confirm:** WMS GetCapabilities mentioning ncWMS / Godiva.

| Tool | Query |
|------|-------|
| Google | `"ncWMS" OR Godiva (WMS OR NetCDF) -site:github.com` |
| Censys | `web.endpoints.http.body: "ncWMS"` |
| FOFA | `body="ncWMS"` |

## istSOS (`istsos`) {#istsos}

OGC Sensor Observation Service (SOS) server for sensor and observation time series (hydrology, meteorology, environmental monitoring), developed by SUPSI Istituto scienze della Terra. Project: [istsos.org](https://istsos.org). Register the public viewer or SOS service root when it is the data catalog, not a login-only `/istsos/admin`.

**Confirm:** `https://host/istsos/{service}?service=SOS&request=GetCapabilities` returns `sos:Capabilities` titled "IST Sensor Observation Service" (default installs ship a `demo` service). Web admin / viewer HTML title `istSOS` or `istSOS-viewer`; the viewer's `/config/config.json` reveals `apiBaseUrl` and service names.

| Tool | Query |
|------|-------|
| Google | `intitle:"istSOS" OR inurl:/istsos/ -site:github.com` |
| Censys | `web.endpoints.http.html_title: "istSOS"` |
| FOFA | `title="istSOS"` |
| Shodan | `http.title:"istSOS"` |

SOS paths carry a per-installation service name (`/istsos/{service}`), so a root or guessed-path GET may 404/401 while the catalog is alive — check the viewer (`/`, title `istSOS-viewer`) before discarding. One SOS server can back several viewer vhosts; register one catalog per server.

## ArcGIS StoryMaps (`arcgisstorymaps`) {#arcgisstorymaps}

Esri's current geospatial storytelling product. Product: [ArcGIS StoryMaps](https://www.esri.com/en-us/arcgis/products/arcgis-storymaps/overview).

**Signals:** `storymaps.arcgis.com/stories/{item-id}` or an ArcGIS Enterprise equivalent; ArcGIS StoryMaps application shell; a public story item. Register only when the story is the primary interface for discovering or exploring a coherent data collection, not every narrative that embeds a map.

| Tool | Query |
|------|-------|
| Google | `site:storymaps.arcgis.com/stories (data OR atlas OR catalog)` |
| Censys | `web.endpoints.http.body: "ArcGIS StoryMaps"` |
| FOFA | `body="ArcGIS StoryMaps"` |
