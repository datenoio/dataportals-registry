# Discovering indicators and microdata catalogs

How to find **indicators catalogs** (`catalog_type: Indicators catalog`) and **microdata catalogs** (`catalog_type: Microdata catalog`). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md).

Statistical offices, central banks, SDG reporting sites, and survey archives are the usual owners. Search the agency name plus the local word for “statistics” / “indicators” / “microdata”, then confirm the platform. High-count stacks with their own recipes: PxWeb, PxStat, DGBAS Web, OpenSDG, Goal Tracker, IMF NSDP, .Stat Suite, .Stat Technology, Istat Data Browser, Swing, Knoema (portal homes only), SDMX-RI, GENESIS-Online, IBIS-PH, DHIS2, FENIX / CountrySTAT, TabNet, SparkMap, eDatos, Cancer-Rates.info, Conduent HCI, Virtual LMI, TerriSTORY, IHK-Fachkräftemonitor, DUVA, Géoclip, InstantAtlas, MATS, DataWarehousePro, Beyond 20/20, NADA, NESSTAR, REDATAM, Colectica, OBiBa Mica, IPUMS. Related PC-Axis stack: PxStat (CSO Ireland; not PxWeb).

## PxWeb (`pxweb`) {#pxweb}

PC-Axis web tables, widely used by Nordic and other NSOs. Examples: [SCB PxWeb examples](https://www.scb.se/en/services/statistical-programs-for-px-files/px-web/pxweb-examples/).

**Confirm:** `https://host/api/v1/` (language segment may be `/api/v1/en/` or `/api/v1/{lang}/`). UI often `/pxweb/` or titled “PxWeb”.

| Tool | Query |
|------|-------|
| Google | `intitle:PxWeb OR inurl:/pxweb` |
| Google | `inurl:/api/v1 "px" statistics` |
| Google | `"PxWeb" (statistik OR statistics OR tilastot)` |
| Censys | `web.endpoints.http.html_title: "PxWeb"` |
| FOFA | `title="PxWeb"` |
| Censys | `web.endpoints.http.body: "PxWeb"` |
| FOFA | `body="PxWeb"` |
| Shodan | `http.title:"PxWeb"` |

**False positives:** documentation for PX files, desktop PC-Axis, a single `.px` download page. Need the **table tree** UI or `/api/v1/`. Do not label a **PxStat** site (`PxStat.Data.Cube_API`) as PxWeb.

## PxStat (`pxstat`) {#pxstat}

CSO Ireland’s open-source dissemination platform (JSON-stat / PX). Live public catalogs: [data.cso.ie](https://data.cso.ie), [data.nisra.gov.uk](https://data.nisra.gov.uk). Source: [CSOIreland/PxStat](https://github.com/CSOIreland/PxStat).

**Confirm:** JSON-stat collection from `GET /public/api.restful/PxStat.Data.Cube_API.ReadCollection/{datefrom}/{lang}` or JSON-RPC method `PxStat.Data.Cube_API.ReadCollection`. UI often titled “PxStat Open Data Platform”. The API host is frequently `ws.` / `ws-data.` beside the UI host.

| Tool | Query |
|------|-------|
| Google | `"PxStat Open Data Platform" OR "PxStat.Data.Cube_API"` |
| Google | `"powered by PxStat" OR inurl:api.restful/PxStat` |
| Censys | `web.endpoints.http.body: "PxStat.Data.Cube_API"` |
| FOFA | `body="PxStat.Data.Cube_API"` |
| Censys | `web.endpoints.http.html_title: "PxStat"` |
| FOFA | `title="PxStat"` |

**False positives:** PxWeb (`/api/v1/`, title “PxWeb”); the CSO demo (`demo-pxstat.cso.ie`); `visual.cso.ie` maps over the same tables; GitHub wiki. Irish public bodies that publish **on** data.cso.ie are not separate catalogs.

## DGBAS Web (`dgbasweb`) {#dgbasweb}

Taiwan DGBAS local statistical query platform (資料庫查詢平臺 / WINSTA). Public tenants share `/DgbasWeb/` ASP.NET pages.

**Signals:** path `/DgbasWeb/index.aspx`, `/DgbasWeb/Default.aspx`, or `/dgbasweb/`; hostname `{org}.dgbas.gov.tw` or a municipal stats host; title 資料庫查詢平台.

**Confirm:** GET the DgbasWeb home and match the tree/keyword query UI. One record per county or city tenant. Do **not** set `dgbasweb` on WebMain catalogs (`webMain.aspx`, `nstatdb.dgbas.gov.tw/dgbasall`) — those are `webmain` — or on Taiwan PxWeb sites (`pxweb.kcg.gov.tw`, Taipei DOTSTAT).

| Tool | Query |
|------|-------|
| Google | `inurl:/DgbasWeb/ (統計 OR 資料庫查詢) site:.gov.tw` |
| Google | `site:dgbas.gov.tw/DgbasWeb/` |
| Censys | `web.names: "dgbas.gov.tw"` |
| FOFA | `host="dgbas.gov.tw"` |

## WebMain (`webmain`) {#webmain}

Taiwan DGBAS-family statistical dynamic query (統計資料動態查詢 / 共通性查詢). National hub: [nstatdb.dgbas.gov.tw/dgbasall](https://nstatdb.dgbas.gov.tw/dgbasall/webMain.aspx?k=dgmain). Manual: [操作教學手冊](https://nstatdb.dgbas.gov.tw/dgbasall/download/%E6%93%8D%E4%BD%9C%E6%95%99%E5%AD%B8%E6%89%8B%E5%86%8A.pdf). Ministry clones use the same `webMain.aspx` engine under branded paths.

**Signals:** path `webMain.aspx` or `WebMain.aspx`; query `sys=` and `funid=`; title or chrome “統計資料動態查詢”, “共通性查詢”, “單表查詢”, “跨表查詢”; folders `/dgbasall/`, `/micst/`, `/statiscla/`, `/njswww/`, `/exam/`, `/statis/`, `/edust/`.

**Confirm:** GET the public query home (not a CMS page that only links out) and match `webMain.aspx` plus `funid=`. One catalog per agency tenant. Do **not** add extra catalogs for each `funid=` theme on the same host (DGBAS income vs prices vs macro are one nstatdb catalog).

**False positives:** local-government `/DgbasWeb/` (`dgbasweb`); PxWeb `statdb.dgbas.gov.tw/pxweb`; MOTC `/motc/Portal/`; MOENV `/epanet/`; MOA `moasdweb`; tourism `stat.taiwan.net.tw`; gender.ey.gov.tw GECdb.

| Tool | Query |
|------|-------|
| Google | `inurl:webMain.aspx (funid OR "統計資料動態查詢") site:.gov.tw` |
| Google | `"統計資料動態查詢" OR "共通性查詢" (webMain OR funid) site:.gov.tw` |
| Censys | `web.endpoints.http.body: "webMain.aspx"` |
| FOFA | `body="webMain.aspx" && body="funid"` |

## OpenSDG (`opensdg`) {#opensdg}

Static SDG reporting sites (often GitHub Pages). Community: [open-sdg.org/community](https://open-sdg.org/community).

**Signals:** `/reporting-status`, indicator pages `/\{goal\}-\{target\}-\{indicator\}`, “Open SDG” in footer or `open-sdg` JS.

| Tool | Query |
|------|-------|
| Google | `"Open SDG" OR "open-sdg" indicators` |
| Google | `inurl:reporting-status "sustainable development"` |
| Google | `site:github.io "Open SDG"` |
| Censys | `web.endpoints.http.body: "open-sdg"` |
| FOFA | `body="open-sdg"` |

Start from the community list; use Google for national translations (`indicadores ODS`, `indicateurs ODD`).

## .Stat Suite (`statsuite`) {#statsuite}

SIS-CC .Stat Suite **Data Explorer** (current generation). Product: [siscc.org/stat-suite](https://siscc.org/stat-suite/). Live examples: [data-explorer.oecd.org](https://data-explorer.oecd.org), [explore.data.abs.gov.au](https://explore.data.abs.gov.au), [esploradati.istat.it](https://esploradati.istat.it).

**Confirm:** `/api/search` or SDMX endpoints; UI “.Stat Suite” / Data Explorer.

| Tool | Query |
|------|-------|
| Google | `".Stat Suite" OR "SIS-CC" "data explorer"` |
| Google | `inurl:/nsi OR "DotStat" SDMX` |
| Censys | `web.endpoints.http.body: ".Stat"` |
| FOFA | `body=".Stat"` |

**False positives:** classic OECD.Stat / I.Stat “Powered by .Stat technology” (`stattech`); Istat **Data Browser** / StatKit (`databrowserhub/api/core`, `istatdatabrowser`).

## .Stat Technology (`stattech`) {#stattech}

Legacy OECD.Stat / I.Stat table browser (“Powered by .Stat technology”), predecessor to .Stat Suite Data Explorer. Reference UI: [stats.oecd.org](https://stats.oecd.org). Other live catalogs: [dati.istat.it](https://dati.istat.it) (I.Stat), [stat.ine.cl](https://stat.ine.cl), [stat.nbb.be](https://stat.nbb.be), [data.uis.unesco.org](http://data.uis.unesco.org).

**Confirm:** OECD.Stat-style table browser chrome or footer “Powered by .Stat technology”. Do **not** label Data Explorer sites `stattech`.

**False positives:** .Stat Suite Data Explorer (`statsuite`); Istat Data Browser (`istatdatabrowser`, for example IstatData / Coeweb — not `dati.istat.it`).

| Tool | Query |
|------|-------|
| Google | `"Powered by .Stat technology" OR "OECD.Stat"` |
| Google | `"I.Stat" inurl:dati.istat.it` |
| Censys | `web.endpoints.http.body: "Powered by .Stat technology"` |
| FOFA | `body="Powered by .Stat technology"` |

## Istat Data Browser (`istatdatabrowser`) {#istatdatabrowser}

Istat StatKit Data Browser (EUPL). Site: [sdmxistattoolkit.github.io](https://sdmxistattoolkit.github.io/). Reference list: [Reference dissemination systems](https://sdmxistattoolkit.github.io/mydoc_RefDiss_Sys.html). Live examples: IstatData, Coeweb, Sistan Hub, AstatData, Malta IRIS, KNBS Open Data Browser, INPS.

**Signals:** SPA under `/databrowser/`; hub JSON at `/databrowserhub/api/core/hub/minimalInfo` or `/databrowser/api/core/hub/minimalInfo`; title or chrome “Data Browser”; often paired with SDMX-RI (`/SDMXWS`).

**Confirm:** GET the hub `minimalInfo` JSON (`hub` / `nodes`) **and** a public `/databrowser/` UI. Register **one catalog per public hub** (IstatData vs Coeweb vs a regional node), not each dataflow. Do not label these sites `statsuite`.

**False positives:** I.Stat / .Stat Technology (`dati.istat.it`); a raw SDMX-RI `/SDMXWS` page with no Data Browser UI (keep `sdmxri`); KNBS Census 2019 JSON-stat DataBrowser (`data.knbs.or.ke`); UNESCO UIS Data Browser; Survey Solutions Data Browser.

| Tool | Query |
|------|-------|
| Google | `"databrowserhub" OR inurl:/databrowserhub/api` |
| Google | `"Istat Data Browser" OR "StatKit" databrowser SDMX` |
| Google | `inurl:/databrowser "Data Browser" (Istat OR NSO OR statistics)` |
| Censys | `web.endpoints.http.body: "databrowserhub"` |
| FOFA | `body="databrowserhub"` |

## Swing (`swing`) {#swing}

ABF Research statistical databank (Swing Viewer / Swing Jive). Vendor: [swingsoftware.eu](https://swingsoftware.eu/). Flemish public tenants live at `{city}.incijfers.be` and `provincies.incijfers.be`.

**Signals:** hostname `*.incijfers.be`; “Powered by Swing”; Swing Viewer / databank UI.

**Confirm:** GET the public databank (not `/Admin/Studio/`). One record per municipal or provincial tenant. Dutch “in cijfers” / waarstaatjegemeente sites on other hosts are the same product when Swing-branded.

| Tool | Query |
|------|-------|
| Google | `site:incijfers.be` |
| Google | `"Powered by Swing" OR "Swing Viewer" (incijfers OR databank)` |
| Censys | `web.names: "incijfers.be"` |
| FOFA | `domain="incijfers.be"` |
| crt.sh | `%.incijfers.be` |

## Knoema (`knoema`) {#knoema}

Commercial indicator portals and country hubs. Site: [knoema.com](https://knoema.com). Ministries and banks often run a branded hub on a `knoema.com` subdomain or a custom domain.

**Signals:** Knoema chrome; `/atlas` or dataset explorer; REST under `/api/1.0/` or `/api/3.0/`.

**Confirm:** GET the **portal home** (a catalog of datasets). Do **not** add every Knoema dataset URL. Skip the global knoema.com hub if it is already registered; add only distinct institutional sites.

| Tool | Query |
|------|-------|
| Google | `site:knoema.com (atlas OR "data portal")` |
| Google | `"powered by Knoema" OR "Knoema" (statistics OR indicators) -site:knoema.com` |
| Censys | `web.names: "knoema.com"` |
| FOFA | `domain="knoema.com"` |
| crt.sh | `%.knoema.com` |

## SparkMap (`sparkmap`) {#sparkmap}

CARES (University of Missouri Extension) community mapping and assessment platform. Flagship: [sparkmap.org](https://sparkmap.org). Partner hubs reuse the same Map Room and community needs assessment UI, often on `*.engagementnetwork.org` or a custom domain.

**Signals:** title or chrome “SparkMap” / “Map Room”; path `/map-room/`; “Powered by CARES”; `engagementnetwork.org` hub host.

**Confirm:** GET the public Map Room or assessment home. Layers and reports must be listable without login. Skip CARES HQ’s own Map Room (`careshq.org/map-room`) when SparkMap is already registered — same national layer library. Skip login-only Community Action Partnership national hub, embed-only widgets, and IRI Climate Data Library “Map Room” sites.

| Tool | Query |
|------|-------|
| Google | `"SparkMap" ("Map Room" OR "community needs assessment") -site:sparkmap.org` |
| Google | `"Powered by CARES" ("Map Room" OR "community needs assessment")` |
| Google | `site:engagementnetwork.org "Map Room"` |
| Censys | `web.endpoints.http.body: "SparkMap"` |
| FOFA | `body="SparkMap"` |
| Censys | `web.names: "engagementnetwork.org"` |
| FOFA | `domain="engagementnetwork.org"` |

## eDatos (`edatos`) {#edatos}

Open-source statistical data/metadata stack from ISTAC (Canary Islands), also used by IBESTAT and IESTADIS. Partner/docs: [documentacion.edatos.io](https://documentacion.edatos.io/), [edatos.io](https://edatos.io/).

**Signals:** host `*.edatos.io`; path `/indicators/v1.0/indicators`; JSON-stat; chrome “eDatos” / e-Indicadores / e-Cubos.

**Confirm:** GET `/indicators/v1.0/indicators` JSON **or** a public ODS / indicator-browser UI. One catalog per public hub (ISTAC APIs vs IESTADIS vs IBESTAT ODS), not each indicator. Do not label IBESTAT `/ods/` as Open SDG.

**False positives:** the institute CMS home (`ibestat.es`, `madrid.org/iestadis`) when the eDatos API/UI lives on another host; ISTAC Open SDG (`/aplicaciones/appsistac/ods/`) is `opensdg`.

| Tool | Query |
|------|-------|
| Google | `"edatos.io" OR "e-Indicadores" (ISTAC OR IBESTAT OR IESTADIS)` |
| Google | `inurl:/indicators/v1.0/indicators` |
| Censys | `web.names: "edatos.io"` |
| FOFA | `domain="edatos.io"` |
| crt.sh | `%.edatos.io` |

## Cancer-Rates.info (`cancerrates`) {#cancerrates}

Kentucky Cancer Registry multi-tenant cancer incidence/mortality query. Tenant list: [cancer-rates.info/about](https://www.cancer-rates.info/about/). Live UI is often `cancer-rates.com/{code}/`.

**Signals:** title `Cancer-Rates.com \| {registry}`; path `/ky/`, `/ms/`, `/naaccr/`, `/se/`; KCR hosting.

**Confirm:** GET the public map/query UI without a login wall. One catalog per registry path. Skip tenants titled “Cancer-Rates.info Login”, pending 404s (Hawaii, Minnesota on the about page), and the KCR organizational home (`kcr.uky.edu`) when the query UI is already registered.

| Tool | Query |
|------|-------|
| Google | `site:cancer-rates.info OR site:cancer-rates.com (registry OR incidence)` |
| Google | `"Cancer-Rates.com" (county OR incidence)` |
| Censys | `web.names: "cancer-rates.com"` |
| FOFA | `domain="cancer-rates.com"` |

## Conduent Healthy Communities Institute (`hci`) {#hci}

Conduent HCI standalone community-health indicator sites (often “Health Matters” branding). Distinct from SparkMap (`sparkmap`).

**Signals:** HTML “Conduent” / “Healthy Communities Institute”; local names like Health Matters; help chrome on healthycities.org.

**Confirm:** GET the public indicator home. One catalog per county/collaborative site. Skip login-only CHNA builders, Conduent marketing, and SparkMap / CARES Map Room sites.

| Tool | Query |
|------|-------|
| Google | `"Healthy Communities Institute" (indicators OR "health matters") -site:conduent.com` |
| Google | `"Powered by Conduent" ("community health" OR indicators)` |
| Censys | `web.endpoints.http.body: "Healthy Communities Institute"` |
| FOFA | `body="Healthy Communities Institute"` |

## Virtual LMI (`virtuallmi`) {#virtuallmi}

Geographic Solutions Virtual LMI labor-market databank. Vendor: [geographicsolutions.com/VLMI](https://www.geographicsolutions.com/VLMI).

**Signals:** host `*.virtuallmi.com`; path `/vosnet/`; “Virtual LMI”.

**Confirm:** GET the public LMI home or `/vosnet/Default.aspx`. One catalog per state tenant. Do not retag QualityInfo, WisConomy, `/analyzer` ALMIS, or other LMI sites without those fingerprints.

| Tool | Query |
|------|-------|
| Google | `site:virtuallmi.com OR inurl:/vosnet "labor market"` |
| Google | `"Virtual LMI" (QCEW OR LAUS OR workforce)` |
| Censys | `web.names: "virtuallmi.com"` |
| FOFA | `domain="virtuallmi.com"` |
| crt.sh | `%.virtuallmi.com` |

## TerriSTORY (`terristory`) {#terristory}

Open-source French territorial energy/climate indicator platform. Product: [terristory.fr](https://terristory.fr/). Source: [gitlab.com/terristory/terristory](https://gitlab.com/terristory/terristory). Docs: [docs.terristory.fr](https://docs.terristory.fr/). Six regional hubs with their own governance: Auvergne-Rhône-Alpes, Bretagne, Corse, Nouvelle-Aquitaine, Occitanie, Pays de la Loire.

**Signals:** host `terristory.fr`; path `/{region}` (for example `/occitanie`, `/bretagne`); chrome “TerriSTORY”; regional indicator map/dashboard.

**Confirm:** GET the public regional hub (not `/Admin/` or login). One catalog per regional hub with its own operator. Do **not** add a second catalog for each commune on the same hub. Skip `terristory.fr/` marketing home when the six regional hubs are registered. The product’s “13 regions” figure includes deployments without separate public hubs — do not invent extra région catalogs.

**False positives:** other French energy observatories (OPTEER, CIGALE, TRACE) that are not TerriSTORY; ADEME data pages; Open SDG.

| Tool | Query |
|------|-------|
| Google | `site:terristory.fr (indicateurs OR énergie OR climat)` |
| Google | `"TerriSTORY" (région OR observatoire) (énergie OR climat)` |
| Censys | `web.names: "terristory.fr"` |
| FOFA | `domain="terristory.fr"` |
| crt.sh | `%.terristory.fr` |

## IHK-Fachkräftemonitor (`ihkfachkraeftemonitor`) {#ihkfachkraeftemonitor}

German Chamber of Industry and Commerce (IHK) multi-Land skills-shortage dashboard. Hub: [ihk-fachkraeftemonitor.de](https://www.ihk-fachkraeftemonitor.de/). Model: GWS Osnabrück.

**Signals:** host `ihk-fachkraeftemonitor.de`; path `/{land}/` (`/bw/`, `/be/`, `/hessen/`, `/nrw/`, `/sh/`); title “IHK-Fachkräftemonitor”.

**Confirm:** GET the Land dashboard without a login wall. One catalog per public Land path. The hub map lists live Länder (5 of 16 as of September 2026) — if the map has no other highlighted Land, the tenant list is complete.

**False positives:** IHK Arbeitsmarktradar Bayern (`arbeitsmarkt-radar.bihk.de`); IHK-Konjunkturboard Baden-Württemberg; BMAS/QuBe Fachkräftemonitoring PDFs; generic IHK labour reports.

| Tool | Query |
|------|-------|
| Google | `site:ihk-fachkraeftemonitor.de` |
| Google | `"IHK-Fachkräftemonitor" (Bundesland OR Branchen OR Berufe)` |
| Censys | `web.names: "ihk-fachkraeftemonitor.de"` |
| FOFA | `domain="ihk-fachkraeftemonitor.de"` |

## DUVA (`duva`) {#duva}

German KOSIS-Gemeinschaft municipal statistics information system. Product: [duva.de](https://duva.de/). Community: [KOSIS DUVA](https://www.staedtestatistik.de/arbeitsgemeinschaften/kosis/duva). Public catalog UI is the **Informationsportal**.

**Signals:** path `/Informationsportal/` or `/Informationsportal11_*/`; title “Informationsportal”; DUVA / KOSIS-Gemeinschaft chrome; some branded hosts (FR.ITZ).

**Confirm:** GET the public Informationsportal and confirm a table/evaluation tree without login. One catalog per city or county public portal. About 60 community members exist; many use DUVA only internally.

**False positives:** Korean KOSIS (`kosis.kr`); Urban Audit Strukturdatenatlas / Perception Survey hosts without a public Informationsportal; `duva-server.de` when it 504s; Freiburg `fritz.freiburg.de` when it is already registered as an open-data portal; Augsburg Statistikportal CMS pages that only mention DUVA in the backend.

| Tool | Query |
|------|-------|
| Google | `inurl:Informationsportal (Statistik OR Kommunalstatistik) site:.de` |
| Google | `"DUVA" "Informationsportal" (Stadt OR Statistik)` |
| Censys | `web.endpoints.http.body: "Informationsportal"` |
| FOFA | `body="Informationsportal"` |

## Géoclip (`geoclip`) {#geoclip}

Commercial geostatistical observatory (Géoclip Air) from Business Geografic / Ciril GROUP. Product: [geoclip.fr](https://www.geoclip.fr/). Public tenants are independent French, Swiss, and Belgian observatories (INSEE Statistiques locales, regional ORS atlases, Hainaut Stat, cantonal atlases), not one national CMS.

**Signals:** `GC_loadCss.php?output=user`; path `/geoclipair/` or `/geoclip/`; HTML comment `Logo geoclip` / class `gc_logo`; title or chrome “Géoclip”; hash routes `#c=indicator` / `#c=home`; shared meta “Explorez et visualisez sous forme de cartes, graphiques et tableaux interactifs”.

**Confirm:** GET the public observatory (not login/admin) and match `GC_loadCss.php` or the geoclip logo block. One catalog per observatory / tenant, not each indicator or each commune report. Skip `geoclip.fr` marketing and demo observatories.

**False positives:** Articque Platform / Cartes & Données; ANCT Observatoire des territoires `/donnees_ouvertes` Drupal catalog (keep `custom`); OCSTAT `statistique.ge.ch/` CMS home (the atlas is `/atlas/`); INSEE `insee.fr` search pages that mention GeoClip; French energy observatories (OPTEER, CIGALE, TrACE) that are not Géoclip; TerritoireAngular (`reperes-paysdelaloire.fr`).

| Tool | Query |
|------|-------|
| Google | `inurl:GC_loadCss.php OR inurl:/geoclipair/` |
| Google | `"Géoclip" (observatoire OR atlas OR "statistiques locales")` |
| Censys | `web.endpoints.http.body: "GC_loadCss.php"` |
| FOFA | `body="GC_loadCss.php"` |

## InstantAtlas (`instantatlas`) {#instantatlas}

Esri UK geostatistical HTML reports and Dashboard Builder. Help: [help.instantatlas.com](https://help.instantatlas.com/). Distinct from Esri UK Data Observatory (`esridataobservatory`).

**Signals:** title “InstantAtlas™ Bericht” / “Rapport InstantAtlas™”; `ia-min.js`; “Powered By InstantAtlas™”; “This InstantAtlas™ report requires JavaScript”; path `/imagemap/instantatlas/` or `atlas.html` report; `dashboards.instantatlas.com/viewer/report?appid=`.

**Confirm:** GET the public atlas/report (not a CMS homepage that only links to one chart). One catalog per public atlas, not each indicator or each year of the same atlas. Skip `instantatlas.com` marketing and Dashboard Builder authoring.

**False positives:** Esri UK Data Observatory WordPress (`/wp-content/themes/ia-theme/` without an InstantAtlas report as the catalog — those are `esridataobservatory`); Report Builder for ArcGIS; a GBE table tree that only mentions InstantAtlas Kreis maps as extras (Sachsen-Anhalt GBE-net); Urban Audit hosts that are DUVA Informationsportale.

| Tool | Query |
|------|-------|
| Google | `intitle:"InstantAtlas" (Bericht OR Rapport OR report)` |
| Google | `"ia-min.js" OR "Powered By InstantAtlas"` |
| Censys | `web.endpoints.http.html_title: "InstantAtlas"` |
| FOFA | `title="InstantAtlas"` |

## MATS (`mats`) {#mats}

Modernes Analyse Tool Statistik — shared Land statistical data-warehouse of Statistikamt Nord, Statistisches Landesamt Rheinland-Pfalz, and Amt für Statistik Berlin-Brandenburg (Oracle Analytics underneath).

**Signals:** “MATS” / “Modernes Analyse Tool Statistik”; path `/mats-datenportal`, `/publikationen/mats`, or `/datenportal` on those three offices; Logo_MATS.

**Confirm:** GET the public MATS-Datenportal (tables/dashboards), not a press article about MATS. One catalog per Land office. The three co-developers are the tenant list.

**False positives:** GENESIS-Online; SIS-Dashboards; generic Oracle APEX; Alaskan `matsugov.us`; Japanese Matsu/Matsuyama GIS hosts.

| Tool | Query |
|------|-------|
| Google | `"Modernes Analyse Tool Statistik" OR MATS-Datenportal` |
| Google | `"MATS" (Statistikamt OR "Berlin-Brandenburg" OR "Rheinland-Pfalz")` |
| Censys | `web.endpoints.http.body: "Modernes Analyse Tool Statistik"` |
| FOFA | `body="Modernes Analyse Tool Statistik"` |

## Health Data Center (`hdc`) {#hdc}

Thailand Ministry of Public Health medical and health data warehouse (ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ). Docs: [dmdmoph.github.io/hdc-docs](https://dmdmoph.github.io/hdc-docs/). National hub: [hdc.moph.go.th/center/public/](https://hdc.moph.go.th/center/public/). Provincial สสจ. tenants use `https://hdc.moph.go.th/{slug}` (docs: “HDC ประจำจังหวัด”).

**Signals:** host `hdc.moph.go.th`; path `/{tenant}/public/` or `/{tenant}/public/main`; title “HDC Service”; chrome “ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ (HDC)”; `assets/images/moph-logo.gif`; link to `dmdmoph.github.io/hdc-docs`.

**Confirm:** GET the public report home (`/public/` or `/public/main`), not the login/register flow. One catalog for the `/center/` hub. Do **not** add a catalog per guessed provincial slug — there is no official slug list, and `/center/public/` already covers the warehouse by region and province.

**False positives:** Health KPI (`healthkpi.moph.go.th`); DDC surveillance (`ddsdoe.ddc.moph.go.th`); `opendata.moph.go.th` table API wrappers; login-only 43-file upload / data-exchange screens.

| Tool | Query |
|------|-------|
| Google | `site:hdc.moph.go.th "ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ"` |
| Google | `"HDC Service" "สำนักงานสาธารณสุขจังหวัด" site:hdc.moph.go.th` |
| Censys | `web.names: "hdc.moph.go.th"` |
| FOFA | `host="hdc.moph.go.th"` |

## JAXI (`jaxi`) {#jaxi}

INE PC-Axis table browser, ceded to Spanish regional statistical offices. Product note: [IAEST difusión en PC-Axis](https://www.aragon.es/-/difusion-en-pc-axis) (“IAEAxi está basada en la herramienta JAXI que ha sido cedida por el INE”).

**Signals:** path `/jaxi/Tabla.htm`, `/jaxi/Datos.htm`, `/jaxiT3/Tabla.htm`; Struts `menu.do` / `tabla.do` on `iaeaxi` or `*-jaxi` apps; `css/jaxi.css` or `theme/custom_jaxi_css/`; branded IAEAxi.

**Confirm:** GET the public table-browser menu (not a CMS home that only links out) and match JAXI paths or chrome. One catalog per tenant. Bare `/iaeaxi/` may redirect to the institute CMS — use `menu.do`. IBESTAT needs `menu.do?nodeId=0` (`/ibestat-jaxi/` alone is a not-found page).

**False positives:** INEbase operations CMS (`/dyngs/INEbase/`); ibestat.es institute portal; eDatos ODS tenants (`edatos`); PxWeb `/api/v1/`; PxStat; other CCAA `/jaxi/` guesses that 404.

Do **not** add a second INE catalog for a random `Tabla.htm` URL, and do **not** retag INEbase as `jaxi` — the registered INEbase home is the operations list, not the table UI.

| Tool | Query |
|------|-------|
| Google | `inurl:/jaxi/Tabla.htm OR inurl:/jaxiT3/Tabla.htm site:.es` |
| Google | `"herramienta JAXI" OR IAEAxi OR inurl:ibestat-jaxi` |
| Censys | `web.endpoints.http.body: "jaxi.css"` |
| FOFA | `body="jaxi.css"` |

## iMonitoring (`imonitoring`) {#imonitoring}

NPO Krista public-finance and socio-economic indicator platform (KristaBI). Product: [npo.krista.ru/products/imonitoring](https://npo.krista.ru/products/imonitoring/). Comparative hub: [iminfin.ru](https://www.iminfin.ru/). Regional Open Budget tenants sit on `*.ifinmon.ru` or branded hosts.

**Signals:** host `*.ifinmon.ru` or `iminfin.ru`; title “Открытый бюджет …” / “iMonitoring”; path `/servisy/konstruktor-dannyx/` or `/konstruktor-dannykh`; `fm@krista.ru` / `fmsupport@krista.ru`; chrome “конструктор данных”.

**Confirm:** GET the public Open Budget home (not login/admin) and match Krista support, the data constructor, or an `ifinmon.ru` tenant. One catalog per regional portal. Do **not** add a catalog per subject listed on the iminfin.ru comparison tree — that is one hub.

**False positives:** other Russian open-budget CMS sites without Krista fingerprints (Leningrad Oblast `budget.lenobl.ru`, Zabaykalsky `budgetzab.75.ru`, Moscow city `budget.mos.ru`); Krasnodar `openbudget23region.ru/otkrytye-dannye` when it is already registered as an open-data catalog; `ifinmon.ru` apex with an expired certificate.

| Tool | Query |
|------|-------|
| Google | `site:ifinmon.ru "Открытый бюджет"` |
| Google | `"Открытый бюджет" (krista OR ifinmon OR "конструктор данных")` |
| Censys | `web.names: "ifinmon.ru"` |
| FOFA | `domain="ifinmon.ru"` |
| crt.sh | `%.ifinmon.ru` |

## SDMX-RI (`sdmxri`) {#sdmxri}

Eurostat SDMX Reference Infrastructure (NSI web service). Site: [sdmx.org](https://sdmx.org/?page_id=4666).

**Signals:** `NSIWebService`, SDMX-RI; `/NSIStdV20Service` or SDMX REST 2.1.

**Confirm:** GET a working SDMX query or the public NSI page that lists dataflows. If PxWeb or .Stat is the human UI, register that catalog instead of a raw SOAP URL.

| Tool | Query |
|------|-------|
| Google | `"SDMX-RI" OR "NSI Web Service" OR NSIStdV20Service` |
| Censys | `web.endpoints.http.body: "NSIWebService"` |
| FOFA | `body="NSIWebService"` |

## GENESIS-Online (`genesisonline`) {#genesisonline}

Destatis / Länder statistical database. Example: [www-genesis.destatis.de](https://www-genesis.destatis.de). Table retrieval is often **POST-only** — do not invent GET API paths.

**Signals:** GENESIS-Online; `genesisclient`; `/genesis/online`.

**Confirm:** GET the public table catalog. One record per statistical-office instance (Bund vs Land).

| Tool | Query |
|------|-------|
| Google | `"GENESIS-Online" (Statistik OR Destatis) site:.de` |
| Google | `inurl:/genesis/online` |
| Censys | `web.endpoints.http.body: "GENESIS-Online"` |
| FOFA | `body="GENESIS-Online"` |

## IBIS-PH (`ibisph`) {#ibisph}

US state public-health indicator system. Community: [Adopt IBIS](https://ibis.utah.gov/ibisph-view/resource/AdoptIBIS.html).

**Signals:** IBIS-PH / IBIS-Q; `/ibisph-view/`; XML-driven indicator pages.

**Confirm:** GET a public indicator home or query module. Skip login-only health department tools.

| Tool | Query |
|------|-------|
| Google | `"IBIS-PH" OR "IBIS PH" (indicators OR "public health") site:.gov` |
| Censys | `web.endpoints.http.body: "ibisph"` |
| FOFA | `body="ibisph"` |

## DHIS2 (`dhis2`) {#dhis2}

Open-source health management information system (HISP / University of Oslo). More than 70 ministries run national HMIS instances. Docs: [docs.dhis2.org](https://docs.dhis2.org). Public FlexiPortal front-ends also count when they publish indicators from a DHIS2 backend. Use `software.id: dhis2`. Do not label a CKAN health document site DHIS2 from a tag alone.

**Signals:** `/dhis-web-commons/`, `/dhis-web-dashboard/`, login chrome “DHIS 2”; REST `/api/system/info`.

**Confirm:** `GET https://host/api/system/info` JSON with a `version` field, or a public portal that is documented as DHIS2. Skip staff-only logins with no public indicator catalog.

| Tool | Query |
|------|-------|
| Google | `"DHIS2" OR "DHIS 2" (HMIS OR "health information" OR portal) -site:dhis2.org -site:github.com` |
| Google | `inurl:/dhis-web-commons OR inurl:/api/system/info` |
| Censys | `web.endpoints.http.body: "dhis-web-commons"` |
| FOFA | `body="dhis-web-commons"` |
| Censys | `web.endpoints.http.html_title: "DHIS 2"` |
| FOFA | `title="DHIS 2"` |

## TabNet (`tabnet`) {#tabnet}

DATASUS CGI tabulator for Brazilian SUS health databases. National hub: [Informações de Saúde (TABNET)](https://datasus.saude.gov.br/informacoes-de-saude-tabnet). States, municipalities, and ANS run separate installations. Use `software.id: tabnet`. Distinct from the OpenDataSUS CKAN portal.

**Signals:** HTML title “TabNet Win32”; paths `deftohtm.exe`, `tabcgi.exe`, `cgi-bin/dh?`; `.def` query forms; “Copia para Tabwin”.

**Confirm:** GET a public table menu or a `.def` form. One catalog per installation (national vs SES vs municipal vs ANS). Do not add every `.def` table as its own catalog. Skip TabWin desktop downloads and login-only intranet copies.

**False positives:** pytorch-tabnet / tabular ML libraries; a CMS page that only links to the national DATASUS TabNet.

| Tool | Query |
|------|-------|
| Google | `"TabNet Win32" site:.gov.br` |
| Google | `inurl:deftohtm.exe OR inurl:tabcgi.exe OR inurl:/cgi-bin/dh site:.gov.br` |
| Google | `"Informações de Saúde" TABNET (secretaria OR municipal) site:.gov.br` |
| Censys | `web.endpoints.http.html_title: "TabNet Win32"` |
| FOFA | `title="TabNet Win32"` |
| Censys | `web.endpoints.http.body: "deftohtm.exe"` |
| FOFA | `body="deftohtm.exe"` |

## FENIX (`fenix`) {#fenix}

FAO’s open-source statistical dissemination stack (D3S / ChaplinJS UIs). Flagship live catalog: [FAOSTAT](https://www.fao.org/faostat/en/). Related FAO apps (AMIS, AIDmonitor, DAD-IS, WIEWS, GIFT) use the same family. CountrySTAT was the national agriculture-statistics product; `countrystat.org` no longer resolves.

**Signals:** `fenixservices.fao.org` or `fenixapps.fao.org`; `/faostat/api/v1/`; HTML/JS mentioning FENIX, D3S, or CountrySTAT; GitHub `FENIX-Platform` / `FENIX-Platform-Projects`.

**Confirm:** public indicator catalog UI, or `GET https://fenixservices.fao.org/faostat/api/v1/en/groupsanddomains` JSON for FAOSTAT. Use `software.id: fenix`. Do not add dead `*.countrystat.org` hosts. CountrySTAT Philippines lives in OpenSTAT (`pxweb`), not FENIX. Do not add FAO CKAN CountrySTAT *datasets* as catalogs.

| Tool | Query |
|------|-------|
| Google | `"CountrySTAT" OR "FENIX" (FAOSTAT OR "food and agriculture") -site:github.com` |
| Google | `inurl:fenixservices.fao.org OR inurl:fenixapps.fao.org` |
| Google | `"fenixservices.fao.org/faostat/api"` |
| Censys | `web.endpoints.http.body: "fenixservices.fao.org"` |
| FOFA | `body="fenixservices.fao.org"` |
| Censys | `web.names: "fenixservices.fao.org"` |
| FOFA | `host="fenixservices.fao.org"` |

**False positives:** FAOSTAT API host as a second catalog (it belongs on the FAOSTAT record); ingested CountrySTAT tables on `data.apps.fao.org`; training PDFs; GitHub UI repos with no public catalog.

## SuperSTAR / SuperWEB2 (`superstar`) {#superstar}

WingArc Australia SuperSTAR suite (formerly Space-Time Research). The public catalog UI is **SuperWEB2**. Use `software.id: superstar`. Do not confuse with STR (CoStar) hotel SuperSTAR.

**Signals:** `/webapi/jsf/login.xhtml`; HTML title “SuperWEB2” / branded TableBuilder / Stat-Xplore / STATcube; help paths `/webapi/online-help/`; Open Data API `/webapi/rest/v1/schema`.

**Confirm:** GET the SuperWEB2 login or catalogue page. Guest or free registration still counts as a public catalog. Skip the WingArc demo (`sw2.wingarc.com.au`) and documentation hosts.

| Tool | Query |
|------|-------|
| Google | `"SuperWEB2" (statistics OR census OR "table builder") -site:github.com` |
| Google | `inurl:/webapi/jsf/login.xhtml` |
| Google | `"Stat-Xplore" OR "TableBuilder" SuperWEB2` |
| Censys | `web.endpoints.http.html_title: "SuperWEB2"` |
| FOFA | `title="SuperWEB2"` |
| Censys | `web.endpoints.http.body: "/webapi/jsf/login.xhtml"` |
| FOFA | `body="/webapi/jsf/login.xhtml"` |

**False positives:** SuperSTAR desktop SuperCROSS; vendor marketing; STR hotel benchmarking; login-only staff cubes with no public guest/register path.

## Beyond 20/20 Web Data Server (`beyond2020`) {#beyond2020}

Legacy ASP.NET cube browser (Beyond 20/20 Inc., Ottawa). Public catalogs expose a **report-folder tree**, not a REST list API. Vendor: [beyond2020.com/web-data-server](https://www.beyond2020.com/web-data-server/). Live public examples: [JODI World Database](http://www.jodidb.org), [IES Castilla-La Mancha](https://difusion.jccm.es/wds/).

**Signals:** HTML title `Beyond 20/20 WDS`; paths `/ReportFolders/reportFolders.aspx`, `/TableViewer/tableView.aspx`; `Common/Images/wds.gif`; language-selection page with the Beyond 20/20 logo; IVT downloads.

**Confirm:** GET the language page or `ReportFolders/reportFolders.aspx` without login. One catalog per public WDS **installation** (the folder tree), not per `ReportId`. Skip Crime Insight / Perspective (`*.beyond2020.com` NIBRS tenants), OSFI `osfi.beyond2020.com` (self-registration), IEA `wds.iea.org` (login; product retired for public data), and Statistics Canada’s unrelated **Web Data Service** REST API.

| Tool | Query |
|------|-------|
| Google | `"Beyond 20/20 WDS" (Reports OR Informes OR "Language Selection")` |
| Google | `inurl:ReportFolders/reportFolders.aspx` |
| Google | `"Beyond 20/20 WDS - Table view"` |
| Censys | `web.endpoints.http.html_title: "Beyond 20/20 WDS"` |
| FOFA | `title="Beyond 20/20 WDS"` |
| Censys | `web.endpoints.http.body: "ReportFolders/reportFolders.aspx"` |
| FOFA | `body="ReportFolders/reportFolders.aspx"` |

**False positives:** Beyond 20/20 Professional Browser / IVT file downloads with no WDS UI; Crime Insight; vendor marketing; login-only WDS; UNCTADstat `/wds/` redirects (now Data Centre); UNESCO UIS Data Browser (migrated off WDS).

## StatPlanet (`statplanet`) {#statplanet}

StatSilk interactive maps and dashboards (StatPlanet Cloud / HTML5, older Flash). Site: [statsilk.com](https://www.statsilk.com). Gallery: [statsilk.com/gallery](https://www.statsilk.com/gallery). Live example: [EC-OECD STIP Compass statistics](https://stip.oecd.org/Stats/STIP-StatTrends.html).

**Signals:** HTML title `StatPlanet`; `StatPlanet Cloud`; `StatPlanet_Cloud.html`; `data.csv` / `settings.csv`; StatSilk footer or logo; URL params `i=` `v=` `t=` on Cloud dashboards.

**Confirm:** GET the dashboard HTML and a public `data.csv` (or SDMX-backed Cloud instance). One record per public explorer, not per indicator or per `*-StatTrends.html` file on the same host.

| Tool | Query |
|------|-------|
| Google | `"StatPlanet Cloud" OR "StatPlanet_Cloud.html" (indicators OR statistics)` |
| Google | `"powered by StatSilk" OR intitle:StatPlanet (map OR dashboard)` |
| Censys | `web.endpoints.http.html_title: "StatPlanet"` |
| FOFA | `title="StatPlanet"` |
| Censys | `web.endpoints.http.body: "StatPlanet Cloud"` |
| FOFA | `body="StatPlanet Cloud"` |

**False positives:** statsilk.com marketing, GitHub `StatSilk/StatPlanet`, Flash-only dead maps, a single thematic poster, StatPlanet World Bank / EdStats viewers of [data.worldbank.org](https://data.worldbank.org) (already `dataworldbankorg`). Skip login-only corporate dashboards.

## Microsoft Power BI (`powerbi`) {#powerbi}

Microsoft Power BI dashboards published as public web embeds. The catalog record is the **page or portal whose indicator layer is the Power BI dashboard**, not the anonymous `app.powerbi.com/view?r=` URL itself. On-premises Power BI Report Server portals (e.g. `unidata.gv.at`) also count.

**Signals:** `app.powerbi.com/view?r=` iframe or link; `embed-powerbi`; `public.powerbi.*` Report Server hosts; CSP/frames allowing `app.powerbi.com`.

**Confirm:** GET the statistics page and confirm the interactive indicator content is a Power BI embed. One catalog per institution/theme. Skip pages that merely mention Power BI in text or CSP, screenshots of dashboards, and internal (login) workspaces.

| Tool | Query |
|-------|-------|
| Google | `site:app.powerbi.com/view` — not catalogable itself; find parents via `"app.powerbi.com" (statistics OR dashboard) site:.gov` |
| Google | `"power bi" (dashboard OR "data portal") (statistics OR indicators) site:.gov` |
| Censys | `web.endpoints.http.body: "app.powerbi.com/view"` |
| FOFA | `body="app.powerbi.com/view"` |

**False positives:** Microsoft marketing/docs; embedded single charts on generic corporate pages; Power Platform partner pages.

## Tableau (`tableau`) {#tableau}

Salesforce Tableau as the interactive statistics layer of an indicators portal — Tableau Public embeds/profiles (`public.tableau.com`), the `tableau-2.min.js` / `tableau-viz` embed API, or self-hosted Tableau Server views (`/t/…/views/…`).

**Signals:** `public.tableau.com/static/`, `/views/`, `/app/profile/…/viz/`; `<tableau-viz`; `tableau-2.min.js`; `tableau.embedding` module; `/javascripts/api/tableau_`.

**Confirm:** GET the statistics section and confirm the indicator tables/dashboards are Tableau views. One catalog per institution/theme. Skip Tableau marketing, public.tableau.com profiles themselves (not a catalog), single blog-chart embeds, and CSP-only mentions.

| Tool | Query |
|-------|-------|
| Google | `"public.tableau.com" (statistics OR indicators) site:.gov` |
| Google | `"tableau-viz" OR "tableau-2.min.js" statistics` |
| Censys | `web.endpoints.http.body: "public.tableau.com/static/"` |
| FOFA | `body="public.tableau.com/static/"` |

**False positives:** training/gallery vizzes on tableau.com; corporate annual-report charts; login-only Tableau Server.

## Microsoft SharePoint (`sharepoint`) {#sharepoint}

Statistics/indicator sections published on Microsoft SharePoint sites (ministries, central banks, planning agencies) instead of a data platform.

**Signals:** `<meta name="GENERATOR" content="Microsoft SharePoint">`; `/_layouts/15/`; `.aspx` pages with SharePoint chrome; `Authenticate.aspx` references.

**Confirm:** GET the statistics section and confirm it is SharePoint-driven (generator meta or `_layouts`). One catalog per institution. Skip pages that only link to a SharePoint document library for downloads while the catalog itself runs on another platform, and login-only intranets.

| Tool | Query |
|-------|-------|
| Google | `"Microsoft SharePoint" statistics site:.gov` |
| Censys | `web.endpoints.http.body: "_layouts/15/Authenticate.aspx"` + manual review for statistics content |
| FOFA | `body="_layouts/15/Authenticate.aspx"` |

**False positives:** SharePoint vendor content; intranets requiring login; document libraries with no indicator/tables layer.

## R Shiny (`shiny`) {#shiny}

Shiny (Posit/RStudio) web applications deployed as statistical query tools and indicator dashboards — self-hosted (`shiny.<agency>`, `/shiny/` paths) or on `*.shinyapps.io`.

**Signals:** `shared/shiny.css`, `shiny.min.js`, `shiny-javascript-*`; `shiny-connected`; `*.shinyapps.io` hosts.

**Confirm:** GET the app and confirm the app **itself** is Shiny (its HTML loads shiny.min.js), not a portal that merely links to a Shiny tool elsewhere. One catalog per app (or per tool family under one path). Skip RStudio marketing and teaching/demo apps.

| Tool | Query |
|-------|-------|
| Google | `inurl:shinyapps.io (statistics OR indicators OR dashboard)` |
| Google | `"shiny.min.js" (statistics OR "data portal") site:.gov` |
| Censys | `web.endpoints.http.body: "shared/shiny.css"` |
| FOFA | `body="shared/shiny.css"` |

**False positives:** portals linking to external Shiny apps; course projects; internal-only apps.

## Qlik Sense (`qlik`) {#qlik}

Qlik Sense hubs/mashups as public statistics platforms (customs, tourism, health).

**Signals:** `qlik-styles.css` autogenerated paths; `qlik_host` / mashup config; requires.js loading `/resources/js/qlik`; "Qlik" branding on statistics UIs.

**Confirm:** GET the statistics portal and confirm the dashboards are Qlik Sense apps. One catalog per installation. Skip Qlik marketing and internal hubs behind login.

| Tool | Query |
|-------|-------|
| Google | `"Qlik Sense" (statistics OR dashboard) site:.gov` |
| Censys | `web.endpoints.http.body: "qlik-styles.css"` |
| FOFA | `body="qlik-styles.css"` |

**False positives:** Qlik vendor pages; "qlik" inside unrelated words in other scripts; login-only enterprise hubs.

## Oracle APEX (`oracleapex`) {#oracleapex}

Low-code Oracle Database apps used as public indicator portals. Site: [apex.oracle.com](https://apex.oracle.com). Docs: [docs.oracle.com/en/database/oracle/apex/](https://docs.oracle.com/en/database/oracle/apex/). Skip generic APEX builders and login-only `/apex/f?p=` apps.

**Signals:** `/apex/` or ORDS paths; APEX session `f?p=`; public statistics/reporting UI.

**Confirm:** GET the public indicator or table list without login. One catalog per public app, not every APEX site.

| Tool | Query |
|------|-------|
| Google | `"Oracle APEX" (statistika OR indicators)` |
| Censys | `web.endpoints.http.body: "apex"` |
| FOFA | `body="apex"` |

## Data VAVT (`datavavt`) {#datavavt}

Macro- and microeconomic indicators from verified sources. Site: [data.vavt.ru](https://data.vavt.ru).

**Signals:** host `data.vavt.ru`; VAVT economic-indicator chrome.

**Confirm:** GET the public table/indicator search. One record for the public portal. Skip intranet copies.

| Tool | Query |
|------|-------|
| Google | `"data.vavt.ru"` |
| Censys | `web.names: "data.vavt.ru"` |
| FOFA | `host="data.vavt.ru"` |

## Apache Superset (`superset`) {#superset}

Open-source BI dashboards. Site: [superset.apache.org](https://superset.apache.org). Use only when a **public** indicator/dataset catalog is the product, not an internal dashboard.

**Signals:** `/superset/dashboard/`; Apache Superset chrome; public chart/dataset list.

**Confirm:** GET a public dataset or dashboard list without login. Stop on `401`. One catalog per public installation.

| Tool | Query |
|------|-------|
| Google | `"Apache Superset" (open data OR indicators)` |
| Censys | `web.endpoints.http.body: "superset"` |
| FOFA | `body="superset"` |

## IBM Cognos Analytics (`ibmcognos`) {#ibmcognos}

BI reports used as public statistical portals. Product: [IBM Cognos Analytics](https://www.ibm.com/products/cognos-analytics). Skip intranet Cognos.

**Signals:** Cognos gateway paths (`/ibmcognos/`, `/bi/v1/disp`); public statistics branding.

**Confirm:** GET published statistical packages/reports without login. Stop on `401`. One catalog per public portal.

| Tool | Query |
|------|-------|
| Google | `"Cognos" (statistics OR open data)` |
| Censys | `web.endpoints.http.body: "ibmcognos"` |
| FOFA | `body="ibmcognos"` |

## BI Contour (`bicontour`) {#bicontour}

Contour Components BI for interactive reporting. Product: [contour_bi](https://www.contourcomponents.com/contour_bi).

**Signals:** “Contour BI” / “BI Contour” chrome; public indicator catalog (not a viewer-only embed).

**Confirm:** GET a public catalog of indicators or reports. Skip intranet and viewer-only map frames. Stop on `401`.

| Tool | Query |
|------|-------|
| Google | `"Contour BI" OR "BI Contour" portal` |
| Censys | `web.endpoints.http.body: "Contour BI"` |
| FOFA | `body="Contour BI"` |

## WHO Data (`whoint`) {#whoint}

WHO global health indicators. Hub: [who.int](https://www.who.int). GHO API is the harvest surface.

**Confirm:** do **not** re-add the WHO hub. Register only a distinct **regional or thematic** WHO data catalog with its own public UI.

| Tool | Query |
|------|-------|
| Google | `"WHO" ("Global Health Observatory" OR GHO) (data OR indicators) -site:who.int` |
| Censys | `web.names: "who.int"` |
| FOFA | `domain="who.int"` |

## Eurostat (`eurostat`) {#eurostat}

EU statistical office. Hub: [ec.europa.eu/eurostat](https://ec.europa.eu/eurostat).

**Confirm:** do **not** re-add the EU Eurostat hub. Register only a distinct Eurostat-branded regional or thematic catalog with its own public UI.

| Tool | Query |
|------|-------|
| Google | `"Eurostat" (database OR "data browser") -site:ec.europa.eu` |
| Censys | `web.names: "ec.europa.eu" and web.endpoints.http.body: "Eurostat"` |
| FOFA | `host="ec.europa.eu" && body="Eurostat"` |

## ECB Data Portal (`ecb`) {#ecb}

European Central Bank statistics. Hub: [data.ecb.europa.eu](https://data.ecb.europa.eu).

**Confirm:** do **not** re-add `data.ecb.europa.eu`. Register only a distinct ECB-branded public statistics catalog.

| Tool | Query |
|------|-------|
| Google | `"ECB Data Portal" OR "data.ecb.europa.eu"` |
| Censys | `web.names: "data.ecb.europa.eu"` |
| FOFA | `host="data.ecb.europa.eu"` |

## World Bank Data (`dataworldbankorg`) {#dataworldbankorg}

World Bank development indicators. Hub: [data.worldbank.org](https://data.worldbank.org).

**Confirm:** do **not** re-add data.worldbank.org. Register only a distinct World Bank data catalog (regional hub or themed API UI).

| Tool | Query |
|------|-------|
| Google | `"World Bank" (databank OR "open data") indicators -site:data.worldbank.org` |
| Censys | `web.names: "data.worldbank.org"` |
| FOFA | `host="data.worldbank.org"` |

## Data.UNICEF.org (`datauniceforg`) {#datauniceforg}

UNICEF child-rights indicators. Hub: [data.unicef.org](https://data.unicef.org).

**Confirm:** do **not** re-add data.unicef.org. Register only a distinct UNICEF regional or SDMX catalog UI.

| Tool | Query |
|------|-------|
| Google | `"data.unicef.org" OR "UNICEF" SDMX dataflow` |
| Censys | `web.names: "data.unicef.org"` |
| FOFA | `host="data.unicef.org"` |

## ILOSTAT (`ilostat`) {#ilostat}

ILO labour statistics. Hub: [ilostat.ilo.org](https://ilostat.ilo.org). SDMX: `sdmx.ilo.org`.

**Confirm:** do **not** re-add ilostat.ilo.org. Register only a distinct ILO regional statistics catalog.

| Tool | Query |
|------|-------|
| Google | `"ILOSTAT" (dataflow OR microdata) -site:ilostat.ilo.org` |
| Censys | `web.names: "ilostat.ilo.org"` |
| FOFA | `host="ilostat.ilo.org"` |

## BIS Data Portal (`databisorg`) {#databisorg}

Bank for International Settlements statistics. Hub: [data.bis.org](https://data.bis.org). Help: [data.bis.org/help](https://data.bis.org/help).

**Confirm:** do **not** re-add data.bis.org. Register only a distinct BIS statistics UI.

| Tool | Query |
|------|-------|
| Google | `"BIS Data Portal" OR site:data.bis.org` |
| Censys | `web.names: "data.bis.org"` |
| FOFA | `host="data.bis.org"` |

## Data Insight (`datainsight`) {#datainsight}

Veritas Data Insight is enterprise unstructured-data intelligence. Product: [veritas.com](https://www.veritas.com/insights/data-insight). Public catalogs are rare.

**Confirm:** GET a **public** dataset/catalog UI. Skip enterprise-only consoles and login walls. Stop on `401`.

| Tool | Query |
|------|-------|
| Google | `"Veritas" "Data Insight" (catalog OR "open data")` |
| Censys | `web.endpoints.http.body: "Data Insight"` |
| FOFA | `body="Data Insight"` |

## Other indicator platforms

| `software.id` | Where to look | Typical query |
|---------------|---------------|---------------|
| `statplanet` | see above | |
| `superstar` | see above | |
| `statsuite` | see above | |
| `istatdatabrowser` | see above | |
| `stattech` | see above | |
| `oracleapex` | see above | |
| `datavavt` | see above | |
| `superset` | see above | |
| `ibmcognos` | see above | |
| `bicontour` | see above | |
| `whoint` | see above | |
| `eurostat` | see above | |
| `ecb` | see above | |
| `dataworldbankorg` | see above | |
| `datauniceforg` | see above | |
| `ilostat` | see above | |
| `databisorg` | see above | |
| `datainsight` | see above | |

National statistical office homepages often link “database”, “statbank”, “PC-Axis”, “SDMX”. Follow those links rather than guessing software from the NSO CMS.

## NADA (`nada`) {#nada}

IHSN National Data Archive for survey microdata. Site: [nada.ihsn.org](https://nada.ihsn.org). UI: study catalog, often `/index.php/catalog`.

**Confirm:** `https://host/index.php/api/catalog/search` (JSON) or the public catalog listing without login.

| Tool | Query |
|------|-------|
| Google | `"NADA" "microdata" OR "national data archive" IHSN` |
| Google | `inurl:/index.php/catalog "microdata"` |
| Google | `"Powered by NADA" OR "nada" "survey catalog"` |
| Censys | `web.endpoints.http.body: "NADA"` |
| FOFA | `body="NADA"` |
| Censys | `web.endpoints.http.body: "IHSN"` |
| FOFA | `body="IHSN"` |

**False positives:** nada.ihsn.org itself (the software site), WordPress blogs named NADA. Need a **study list** with DDI-style metadata.

## IPUMS (`ipums`) {#ipums}

University of Minnesota extract platform for harmonized census and survey microdata. Collections share one API and extract engine: IPUMS USA, International, CPS, DHS, NHIS, Higher Ed, PMA, MICS, Time Use, plus geographic NHGIS and IHGIS. Developer docs: [developer.ipums.org](https://developer.ipums.org).

**Signals:** `*.ipums.org` or `idhsdata.org` / `nhgis.org`; extract-system UI; “IPUMS” branding. Use `software.id: ipums`.

**Confirm:** GET the **collection home** (variable/sample selector), not a completed extract download. One registry record per public collection. Do not add every extract or variable page. **Reject** directory hubs that only list other IPUMS collections (IPUMS Health Surveys, IPUMS Global Health) — those are not catalogs.

| Tool | Query |
|------|-------|
| Google | `"IPUMS" (extract OR microdata OR census) site:.org -site:github.com` |
| Google | `site:ipums.org (USA OR International OR CPS OR NHIS)` |
| Censys | `web.names: "ipums.org"` |
| FOFA | `domain="ipums.org"` |

## NESSTAR (`nesstar`) {#nesstar}

Older microdata publisher. Many instances are inactive; still record working public catalogs.

| Tool | Query |
|------|-------|
| Google | `"Nesstar" (microdata OR "webview")` |
| Google | `inurl:/webview nesstar` |
| Censys | `web.endpoints.http.body: "Nesstar"` |
| FOFA | `body="Nesstar"` |

## REDATAM (`redatam`) {#redatam}

ECLAC census/survey online processing. Site: [redatam.org](https://www.redatam.org).

| Tool | Query |
|------|-------|
| Google | `"REDATAM" (censos OR census OR "en línea")` |
| Google | `inurl:redatam OR "Redatam Web Server"` |
| Censys | `web.endpoints.http.body: "REDATAM"` |
| FOFA | `body="REDATAM"` |

## Colectica (`colectica`) {#colectica}

DDI metadata catalogs / portals.

| Tool | Query |
|------|-------|
| Google | `"Colectica" (portal OR repository OR DDI)` |
| Censys | `web.endpoints.http.body: "Colectica"` |
| FOFA | `body="Colectica"` |

## OBiBa Mica (`obibamica`) {#obibamica}

Epidemiological / population-health study catalog (OBiBa). Often paired with Opal; register the **public Mica** discovery UI.

**Signals:** Mica / OBiBa branding; study and network search; `/ws/` REST.

**Confirm:** GET the public study catalog. Skip login-only research networks.

| Tool | Query |
|------|-------|
| Google | `"Mica" OBiBa (studies OR catalog) -site:github.com` |
| Censys | `web.endpoints.http.body: "obiba"` |
| FOFA | `body="obiba"` |
| Censys | `web.endpoints.http.body: "Mica"` |
| FOFA | `body="Mica"` |

## Survey Solutions (`surveysolutions`) {#surveysolutions}

World Bank survey suite. Register only a **public Data Browser** of microdata, not a data-collection server. **Reject** `*.mysurvey.solutions` / KNBS/INE interviewer hosts — they are survey collection platforms, not catalogs (September 2026 instance hunt).

| Tool | Query |
|------|-------|
| Google | `"Survey Solutions" ("data browser" OR microdata) -site:mysurvey.solutions` |
| Censys | `web.endpoints.http.body: "Survey Solutions"` |
| FOFA | `body="Survey Solutions" && body="Data Browser"` |

## DataWarehousePro (`datawarehousepro`) {#datawarehousepro}

Central-bank macroeconomic warehouse. Site: [datawarehousepro.com](https://datawarehousepro.com). Tenants: `app.datawarehousepro.com/go/{tenant}` (sometimes a custom domain).

**Signals:** DataWarehousePro chrome; `/guest/getDatabanksWithMnemonics/` API.

**Confirm:** GET `/go/{tenant}` and `/guest/getDatabanksWithMnemonics/{tenant}`. One record per institutional tenant, not per series.

| Tool | Query |
|------|-------|
| Google | `site:app.datawarehousepro.com/go` |
| Google | `"DataWarehousePro" ("central bank" OR statistics)` |
| Censys | `web.names: "app.datawarehousepro.com"` |
| FOFA | `host="app.datawarehousepro.com"` |
| crt.sh | `%.datawarehousepro.com` |

## IMF National Summary Data Page (`imfnsdp`) {#imfnsdp}

IMF e-GDDS / SDDS / SDDS Plus National Summary Data Page hosted by an NSO or central bank. Hub: [dsbb.imf.org](https://dsbb.imf.org). Distinct from Knoema (`knoema`) and WordPress (`wordpress`) sites that only wrap an NSDP, and from a whole NSO homepage that happens to link to one.

**Signals:** title or heading “National Summary Data Page”; IMF DSBB / e-GDDS / SDDS chrome; SDMX 2.0 XML links; path `NSDP`, `IMF_NSDP`, or `nsdp`.

**Confirm:** GET the NSDP HTML page (not the NSO home). One record per country page. Skip Open Data for Africa / Knoema NSDP hubs and WordPress ministry sites already tagged with those IDs.

| Tool | Query |
|------|-------|
| Google | `"National Summary Data Page" (e-GDDS OR SDDS OR IMF)` |
| Google | `inurl:NSDP OR inurl:IMF_NSDP "SDMX"` |
| Censys | `web.endpoints.http.body: "National Summary Data Page"` |
| FOFA | `body="National Summary Data Page"` |

## Goal Tracker (`goaltracker`) {#goaltracker}

Data Act Lab SDG country platforms. Site: [goaltracker.org](https://goaltracker.org). Distinct from Open SDG (`opensdg`).

**Signals:** host `*.goaltracker.org`; title “Goal Tracker”; Data Act Lab branding.

**Confirm:** GET the country tenant home. One record per country site. Skip the vendor marketing page if a country tenant is already registered.

| Tool | Query |
|------|-------|
| Google | `site:goaltracker.org` |
| Google | `"Goal Tracker" (SDG OR "Global Goals") -site:goaltracker.org/about` |
| Censys | `web.names: "goaltracker.org"` |
| FOFA | `domain="goaltracker.org"` |
| crt.sh | `%.goaltracker.org` |

## Generic statistics-office patterns

```text
site:.gov {country} (statbank OR "statistical database" OR pxweb OR sdmx)
"microdata" (catalog OR archive OR "data archive") {NSO name}
"DDI" "survey catalog" {country}
```

Central banks (`indicators` more often than microdata): `site:{bank-domain} (statistics OR SDMX OR "statistical warehouse")`. Only add a catalog when there is a queryable database, not a PDF publications page.

## Country indicators hunt {#country-indicators-hunt}

Prompt: `Which {country} indicators catalogs are missing?`

1. Count existing `indicators/` YAML for that ISO folder. If the only row is an IMF NSDP, hunt a **native table DB**. If PxWeb/.Stat/STATcube is already there, hunt health, education, SDG, central bank, and subnational explorers — not a second copy of the StatBank.
2. Sources: NSO site (table builder, not the CMS home), health ministry / DHIS2 / TabNet / HCI / Cancer-Rates.info, education/labour explorers, OpenSDG / Goal Tracker, central-bank warehouse, provincial/city indicator hubs.
3. **Accept:** a public table tree or indicator explorer (PxWeb `/api/v1/`, .Stat Data Explorer, Shiny profiles, SDMX, SuperWEB2). `is_national: true` only for the official NSO product of that type.
4. **Reject:** PDF publications pages; ministry CMS homes; login dashboards; agency PxWeb already harvested into the national StatBank (Finland); IMF NSDP already registered; open-data APIs that are not indicator catalogs (data.police.uk); guessed HCI / Virtual LMI / Cancer-Rates county hostnames (timeouts and login loops — use the vendor tenant list).

The 29–30 August 2026 wave covered most OECD and Asian NSO gaps. Remaining yield is Africa, some Pacific NSOs, and subnational health/education explorers.

## Related

- [discovery.md](discovery.md)
- [discovery.md](discovery.md#hunt-patterns) — session hunt patterns
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-metadata.md](discovery-metadata.md)
- [harvest-indicators.md](harvest-indicators.md)
- [harvest.md](harvest.md)
- [harvest-protocols.md](harvest-protocols.md)
- [catalog-types.md](catalog-types.md)
- [software-taxonomy.md](software-taxonomy.md)
