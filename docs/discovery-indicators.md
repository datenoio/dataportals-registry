# Discovering indicators and microdata catalogs

How to find **indicators catalogs** (`catalog_type: Indicators catalog`) and **microdata catalogs** (`catalog_type: Microdata catalog`). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md).

Statistical offices, central banks, SDG reporting sites, and survey archives are the usual owners. Search the agency name plus the local word for “statistics” / “indicators” / “microdata”, then confirm the platform. High-count stacks with their own recipes: PxWeb, PxStat, DGBAS Web, OpenSDG, SDG Index, Goal Tracker, IMF NSDP, .Stat Suite, .Stat Technology, Istat Data Browser, Swing, Knoema (portal homes only), SDMX-RI, GENESIS-Online, IBIS-PH, DHIS2, FENIX / CountrySTAT, TabNet, SparkMap, eDatos, Cancer-Rates.info, Conduent HCI, Virtual LMI, TerriSTORY, IHK-Fachkräftemonitor, DUVA, Géoclip, InstantAtlas, MATS, DataWarehousePro, Beyond 20/20, NADA, NESSTAR, REDATAM, Colectica, OBiBa Mica, IPUMS, KOSIS, e-Stat, SIDRA, Fingertips, UNdata, UN Comtrade Plus, Our World in Data. Related PC-Axis stack: PxStat (CSO Ireland; not PxWeb).

## PxWeb (`pxweb`) {#pxweb}

PC-Axis web tables, widely used by Nordic and other NSOs. Examples: [SCB PxWeb examples](https://www.scb.se/en/services/statistical-programs-for-px-files/px-web/pxweb-examples/).

**Confirm:** `https://host/api/v1/` (language segment may be `/api/v1/en/` or `/api/v1/{lang}/`). UI often `/pxweb/` or titled “PxWeb”.

[PXWeb/PxWeb.Master](https://github.com/statisticssweden/PxWeb/blob/master/PXWeb/PxWeb.Master) links `Resources/Styles/main-pxweb.css` and sets `id="pxwebcontent"` (73 and 76 hosts in September 2026, including `pxweb.lansstyrelsen.se`). `body="PxWeb"` matched 646 because many offices replace that stylesheet. Keep the wider query.

| Tool | Query |
|------|-------|
| Google | `intitle:PxWeb OR inurl:/pxweb` |
| Google | `inurl:/api/v1 "px" statistics` |
| Google | `"PxWeb" (statistik OR statistics OR tilastot)` |
| Censys | `web.endpoints.http.body: "main-pxweb.css"` |
| FOFA | `body="main-pxweb.css"` |
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

## KOSIS (`kosis`) {#kosis}

Statistics Korea statistical table platform. Hub: [kosis.kr](https://kosis.kr). OpenAPI: [kosis.kr/openapi/](https://kosis.kr/openapi/). Agency and local tenants reuse `/statHtml/statHtml.do`. ODA clones include MMSIS, LAOSIS, and ASIS.

**Signals:** path `/statHtml/statHtml.do`; title “KOSIS” / “국가통계포털” / “통계표조회”; `kosisTitle.gif` / `dbsearchTitle.gif`; current skin `/ext/newKosis/css/main.css`; agency 통계포털 shell `vw_cd=MT_DTITLE` / `TblInfoListResult.html`; older ODA JSP tree `statDbList.jsp` / `fileDb.jsp`; NSIST hosting on `stat.kosis.kr` (`statHtml_host/statHtml.do`).

**Confirm:** GET a public table tree or a live `/statHtml/statHtml.do?orgId=&tblId=` table that returns a named statistical table. One catalog per public tenant. The `/bukhan/` tree is already a separate registered catalog. Keep a host only when that table is served on the host. City pages that only deep-link `stat.kosis.kr/statHtml_host` are link-outs.

**False positives:** local-government `/stat/index.do` CMS skins that only link out to KOSIS (Paju `stat.paju.go.kr` is this case); 지표누리 (`index.go.kr`); SGIS; English/mobile/SSO aliases of `kosis.kr` (`edu`, `sso`, `mgmk`); `stat.kosis.kr/nsistN` agency hosting console; IP-only COLSIS hits; `body="dbsearchTitle"` without `.gif` (library guides). LankaSIS (`sis.statistics.gov.lk`) matches `statDbList.jsp` but did not answer on GET in September 2026.

| Tool | Query |
|------|-------|
| Google | `inurl:/statHtml/statHtml.do (KOSIS OR 통계표조회 OR MMSIS OR LAOSIS OR ASIS)` |
| Google | `site:kosis.kr (국가통계포털 OR "Korean Statistical Information")` |
| Censys | `web.names: "kosis.kr"` |
| FOFA | `title="KOSIS 국가통계포털" && country="KR"` |
| FOFA | `title="MMSIS" \|\| title="LAOSIS" \|\| title="LankaSIS"` |
| FOFA | `body="/statHtml/statHtml.do"` |
| FOFA | `body="kosisTitle.gif"` |
| FOFA | `body="/ext/newKosis/css/main.css"` |
| FOFA | `body="vw_cd=MT_DTITLE"` |
| FOFA | `body="TblInfoListResult.html"` |
| FOFA | `body="statDbList.jsp"` |
| FOFA | `body="fileDb.jsp"` |
| FOFA | `body="statHtml_host/statHtml.do"` |
| FOFA | `body="statHtml/statHtml.do?orgId" && domain!="kosis.kr"` |

## e-Stat (`estat`) {#estat}

Japan portal site for official statistics (政府統計の総合窓口). Hub: [e-stat.go.jp](https://www.e-stat.go.jp). API: [e-Stat API](https://www.e-stat.go.jp/en/api/).

**Signals:** host `e-stat.go.jp`; title “政府統計の総合窓口”; Statistical LOD on `data.e-stat.go.jp`; Statistics Dashboard on `dashboard.e-stat.go.jp`.

**Confirm:** GET the public table portal, LOD home, or dashboard. The three hosts are already registered as distinct catalogs — do **not** add extra table/API paths. Skip RESAS and ministry pages that only link to e-Stat.

| Tool | Query |
|------|-------|
| Google | `site:e-stat.go.jp (統計 OR "official statistics")` |
| Censys | `web.names: "e-stat.go.jp"` |
| FOFA | `domain="e-stat.go.jp"` |

## OpenSDG (`opensdg`) {#opensdg}

Static SDG reporting sites (often GitHub Pages). Community: [open-sdg.org/community](https://open-sdg.org/community).

**Signals:** `/reporting-status`, indicator pages `/\{goal\}-\{target\}-\{indicator\}`, “Open SDG” in footer or `open-sdg` JS.

**GitHub, do both.** Code search does not index most forks. The repo operators fork is [open-sdg/open-sdg-site-starter](https://github.com/open-sdg/open-sdg-site-starter). `_config.yml` sets `remote_theme: open-sdg/open-sdg`. `Gemfile` requires `jekyll-open-sdg-plugins`. Jekyll writes that gem name into the built HTML, so FOFA sees it (`body="jekyll-open-sdg-plugins"`, 48 hosts in September 2026, including `kenya-sdg.github.io`). `body="open-sdg"` is wider (128). General method: [discovery-search-tools.md](discovery-search-tools.md#github).

| Tool | Query |
|------|-------|
| GitHub forks | `repos/open-sdg/open-sdg-site-starter/forks` |
| GitHub code | `remote_theme: open-sdg/open-sdg filename:_config.yml` |
| GitHub code | `jekyll-open-sdg-plugins filename:Gemfile` |
| Google | `"Open SDG" OR "open-sdg" indicators` |
| Google | `inurl:reporting-status "sustainable development"` |
| Google | `site:github.io "Open SDG"` |
| Censys | `web.endpoints.http.body: "open-sdg"` |
| FOFA | `body="open-sdg"` |
| FOFA | `body="jekyll-open-sdg-plugins"` |

Start from the community list; use Google for national translations (`indicadores ODS`, `indicateurs ODD`).

## SDG Index (`sdgindex`) {#sdgindex}

SDSN Sustainable Development Report dashboards and the regional or subnational editions built from the same template. Product: [dashboards.sdgindex.org](https://dashboards.sdgindex.org). Starter: [sdsna/sdgindex-starter](https://github.com/sdsna/sdgindex-starter). Editions are listed on the [Sustainable Development Report online library](https://www.sustainabledevelopment.report/).

**Signals:** host `*.sdgindex.org` (also `countries.africasdgindex.org` when it resolves); Next.js `/_next/` or `@sdgindex`; title “Sustainable Development Report” or “SDG Index”; rankings, map, and profile navigation.

**Confirm:** GET the dashboard home and match rankings or profiles. One record per public host. Do not add each country, state, or city profile on that host.

**False positives:** OpenSDG (`opensdg`, `open-sdg` / `/reporting-status`); the SDSN library and news site [sdgtransformationcenter.org](https://sdgtransformationcenter.org); PDF-only report pages; official NSO SDG portals that are not an SDSN dashboard.

| Tool | Query |
|------|-------|
| Google | `site:sdgindex.org (dashboard OR rankings OR profiles)` |
| Google | `"Sustainable Development Report" (site:sdgindex.org OR "SDG Index")` |
| Censys | `web.names: "sdgindex.org"` |
| FOFA | `domain="sdgindex.org"` |
| crt.sh | `%.sdgindex.org` |

## .Stat Suite (`statsuite`) {#statsuite}

SIS-CC .Stat Suite **Data Explorer** (current generation). Product: [siscc.org/stat-suite](https://siscc.org/stat-suite/). Live examples: [data-explorer.oecd.org](https://data-explorer.oecd.org), [explore.data.abs.gov.au](https://explore.data.abs.gov.au), [esploradati.istat.it](https://esploradati.istat.it).

**Confirm:** `/api/search` or SDMX endpoints; UI “.Stat Suite” / Data Explorer.

[en.json](https://gitlab.com/sis-cc/.stat-suite/dotstatsuite-config-data/-/blob/develop/i18n/en.json) sets the footer author `.Stat Suite` (284 hosts in September 2026, including `stathub.nso.go.th` and `dataexplorer.ukdataservice.ac.uk`). The same file titles the app `.Stat Data Explorer` (195 hosts, including `de-demo.siscc.org` and `datacube.uba.de`). `body=".Stat"` matched 14,060,434 hosts, and the first hits are unrelated sites.

| Tool | Query |
|------|-------|
| Google | `".Stat Suite" OR "SIS-CC" "data explorer"` |
| Google | `inurl:/nsi OR "DotStat" SDMX` |
| Censys | `web.endpoints.http.body: ".Stat Suite"` |
| FOFA | `body=".Stat Suite"` |
| Censys | `web.endpoints.http.body: ".Stat Data Explorer"` |
| FOFA | `body=".Stat Data Explorer"` |

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

[index.html](https://github.com/SDMXISTATTOOLKIT/DATABROWSER/blob/master/App_first_installation/databrowser/index.html) sets `webpackJsonpdata-browser` (2 hosts in September 2026, `app.databrowser.sister.it`). `body="databrowserhub"` matched 0. `lmap/lmap/css/lmap.css` in the same file matched `dati.lavoro.gov.it`, titled DataPortal.AI.

| Tool | Query |
|------|-------|
| Google | `"databrowserhub" OR inurl:/databrowserhub/api` |
| Google | `"Istat Data Browser" OR "StatKit" databrowser SDMX` |
| Google | `inurl:/databrowser "Data Browser" (Istat OR NSO OR statistics)` |
| Censys | `web.endpoints.http.body: "webpackJsonpdata-browser"` |
| FOFA | `body="webpackJsonpdata-browser"` |

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
| FOFA | `body="Powered by Swing"` |
| crt.sh | `%.incijfers.be` |

## Knoema (`knoema`) {#knoema}

Commercial indicator portals and country hubs. Site: [knoema.com](https://knoema.com). Ministries and banks often run a branded hub on a `knoema.com` subdomain or a custom domain. Most registered tenants are African country hubs on Knoema's **Open Data for Africa** platform brand (`*.opendataforafrica.org`), which `domain="knoema.com"` does not match.

**Signals:** Knoema chrome; `/atlas` or dataset explorer; REST under `/api/1.0/` or `/api/3.0/`.

The appliance homepage ([data.gov.om](https://data.gov.om)) writes a hidden `isApplianceInstance` input and `knoema-event-tracker` (92 hosts each in September 2026, including `comstat.comesa.int`). The same page links `/assets.axd/Css/Knoema/knoema.page` (81 hosts) and `/assets.axd/Knoema.Registry` (63). `header="KnoemaUserId"` matched 1,889 rows, almost all ports on one bare IP plus those same custom domains. `domain="knoema.com"` matched 1,204 rows (508 hostnames) and is not usable alone: the zone is a wildcard, so mail hosts, `no-exist-subdomain-pre.*`, and random labels dominate. `domain="knoema.org"` (2) does not resolve. Open Data for Africa tenants stay on `domain="opendataforafrica.org"`; Cloudflare hides the body strings.

**Confirm:** GET the **portal home** (a catalog of datasets). Count datasets with `GET /api/1.0/search?query=1&scope=dataset&version=2` and keep the host only when `items[].resource.type` is `Dataset`. Do **not** add every Knoema dataset URL. Skip the global knoema.com hub if it is already registered; add only distinct institutional sites. Skip the default product title “One Platform for Data Discovery…” when `communityId` is empty, login-only `/sys/login` hubs, and a custom domain that repeats an existing `communityId` (COMSTAT on `comstat.comesa.int` is the same hub as `comesa.opendataforafrica.org`).

| Tool | Query |
|------|-------|
| Google | `site:knoema.com (atlas OR "data portal")` |
| Google | `"powered by Knoema" OR "Knoema" (statistics OR indicators) -site:knoema.com` |
| Google | `site:opendataforafrica.org` |
| Censys | `web.names: "knoema.com"` |
| FOFA | `domain="knoema.com"` |
| Censys | `web.names: "opendataforafrica.org"` |
| FOFA | `domain="opendataforafrica.org"` |
| FOFA | `domain="tourismdataforafrica.org"` |
| FOFA | `body="opendataforafrica"` |
| FOFA | `body="isApplianceInstance"` |
| FOFA | `body="knoema-event-tracker"` |
| FOFA | `body="Css/Knoema/knoema.page"` |
| FOFA | `body="Knoema.Registry"` |
| crt.sh | `%.knoema.com` |
| crt.sh | `%.opendataforafrica.org` |

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
| FOFA | `body="Powered by CARES"` |
| FOFA | `body="wp-content/plugins/cares-data-tools"` |
| FOFA | `body="wp-content/plugins/cares-flexbox-grids"` |
| FOFA | `body="services.engagementnetwork.org"` |
| FOFA | `body="help@cares.missouri.edu"` |
| Censys | `web.names: "engagementnetwork.org"` |
| FOFA | `domain="engagementnetwork.org"` |
| FOFA | `domain="datahubs.org"` |

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
| FOFA | `domain="cancer-rates.info"` |
| FOFA | `title="Cancer-Rates.com"` |

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

**Confirm:** GET the public LMI home or `/vosnet/Default.aspx`. One catalog per state tenant. Branded custom domains count when `/vosnet/` is the UI (Colorado LMI Gateway). Do not retag QualityInfo, WisConomy, `/analyzer` ALMIS, or other LMI sites without those fingerprints.

| Tool | Query |
|------|-------|
| Google | `site:virtuallmi.com OR inurl:/vosnet "labor market"` |
| Google | `"Virtual LMI" (QCEW OR LAUS OR workforce)` |
| Censys | `web.names: "virtuallmi.com"` |
| FOFA | `domain="virtuallmi.com"` |
| FOFA | `body="vosnet"` |
| FOFA | `body="Virtual LMI"` |
| crt.sh | `%.virtuallmi.com` |

## CityViz (`cityviz`) {#cityviz}

CityViz Data Solutions (Calgary/Kelowna) community economic-development data platform for Canadian municipalities and regional economic development organizations. Vendor: [cityviz.ca](https://cityviz.ca/). Tenant leads: homepage “CityViz in Action” showcase, the testimonials page, and CT logs over `%.cityviz.ca` (includes decommissioned tenants — probe before adding).

**Signals:** host `*.cityviz.ca`; custom domains such as `data.choose*.ca`, `insights.medicinehat.ca`, `cityviz.penticton.ca`, `data.langleycity.ca`; title “Economic Development Data Platform” with “powered by Cityviz” chrome; R Shiny assets (`shiny-javascript-*/shiny.min.js`); paths `/economic-indicators`, `/search`, `/report-studio`.

**Confirm:** GET the portal home without a login wall; the overview must list indicator dashboards for a named community. One catalog per community tenant. Skip the vendor marketing site `cityviz.ca`, the fictional `bellaville.cityviz.ca` showcase, placeholder tenants (“Reach out to explore how CityViz can support your data requirements”), Cloudflare Access login-gated tenants, and tenants answering with nginx `50x.html` or `/not-found` (decommissioned).

| Tool | Query |
|------|-------|
| Google | `"powered by Cityviz" OR "powered by CityViz"` |
| Google | `"Economic Development Data Platform" (CityViz OR cityviz.ca)` |
| Censys | `web.names: "cityviz.ca"` |
| FOFA | `domain="cityviz.ca"` |
| FOFA | `title="Economic Development Data Platform"` |
| FOFA | `body="economic-development-data-platform-logo.png"` |
| FOFA | `body="www/js/cityviz.js"` |
| FOFA | `body="www/cityviz.css"` |
| FOFA | `body="CityViz economic development data platform"` |
| FOFA | `body="request_dataset-request_dataset_modal"` |
| crt.sh | `%.cityviz.ca` |

`www/js/cityviz.js` and `www/cityviz.css` are in the R Shiny shell, so they find custom domains (`data.invest*.ca`, `data.*county.com`) that `domain="cityviz.ca"` and CT logs miss. Confirm `/search` lists indicator datasets before adding. A vendor host that has become a CMS while the custom domain still serves `/search` is the same tenant — record the custom domain.

## TerriSTORY (`terristory`) {#terristory}

Open-source French territorial energy/climate indicator platform. Product: [terristory.fr](https://terristory.fr/). Source: [gitlab.com/terristory/terristory](https://gitlab.com/terristory/terristory). Docs: [docs.terristory.fr](https://docs.terristory.fr/). Six regional hubs with their own governance: Auvergne-Rhône-Alpes, Bretagne, Corse, Nouvelle-Aquitaine, Occitanie, Pays de la Loire.

**Signals:** host `terristory.fr`; path `/{region}` (for example `/occitanie`, `/bretagne`); chrome “TerriSTORY”; regional indicator map/dashboard.

**Confirm:** GET the public regional hub (not `/Admin/` or login). One catalog per regional hub with its own operator. Do **not** add a second catalog for each commune on the same hub. Skip `terristory.fr/` marketing home when the six regional hubs are registered. The product’s “13 regions” figure includes deployments without separate public hubs — do not invent extra région catalogs.

**False positives:** other French energy observatories (OPTEER, CIGALE, TRACE) that are not TerriSTORY; ADEME data pages; Open SDG.

[front/index.html](https://gitlab.com/terristory/terristory/-/blob/master/front/index.html) describes `base de données TerriSTORY` (2 hosts in September 2026, `128.140.74.161:3001` and `34.155.137.190:3000`, both titled TerriSTORY). `body="TerriSTORY®"` matched 15, and the first hit is `rare.fr`. The six public regional hubs stay on `terristory.fr`.

| Tool | Query |
|------|-------|
| Google | `site:terristory.fr (indicateurs OR énergie OR climat)` |
| Google | `"TerriSTORY" (région OR observatoire) (énergie OR climat)` |
| Censys | `web.endpoints.http.body: "base de données TerriSTORY"` |
| FOFA | `body="base de données TerriSTORY"` |
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

**Signals:** path `/Informationsportal/` or `/Informationsportal11_*/` or a branded path such as `/Statistikportal/`; GWT bootstrap `InformationPortal.nocache.js` (current) or `Informationsportal.nocache.js` (older); stylesheet `InformationPortal/css/domino-ui.css`; title “Informationsportal”; some branded hosts (FR.ITZ, GÖSIS). A bare `body="Informationsportal"` query is not a fingerprint.

**Confirm:** GET the public Informationsportal and confirm a table/evaluation tree without login. One catalog per city or county public portal. About 60 community members exist; many use DUVA only internally.

**False positives:** Korean KOSIS (`kosis.kr`); Urban Audit Strukturdatenatlas / Perception Survey hosts without a public Informationsportal; `duva-server.de` when it 504s; Freiburg `fritz.freiburg.de` when it is already registered as an open-data portal; Augsburg Statistikportal CMS pages that only mention DUVA in the backend.

| Tool | Query |
|------|-------|
| Google | `inurl:Informationsportal (Statistik OR Kommunalstatistik) site:.de` |
| Google | `"DUVA" "Informationsportal" (Stadt OR Statistik)` |
| Censys | `web.endpoints.http.body: "InformationPortal.nocache.js"` |
| FOFA | `body="InformationPortal.nocache.js"` |
| FOFA | `body="InformationPortal/css/domino-ui.css"` |
| FOFA | `body="Informationsportal.nocache.js"` |

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
| FOFA | `body="ia-min.js"` |
| FOFA | `body="Powered By InstantAtlas"` |

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

Thailand Ministry of Public Health medical and health data warehouse (ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ). Docs: [dmdmoph.github.io/hdc-docs](https://dmdmoph.github.io/hdc-docs/). National hub: [hdc.moph.go.th/center/public/](https://hdc.moph.go.th/center/public/). Provincial สสจ. tenants use `https://hdc.moph.go.th/{slug}` (docs: “HDC ประจำจังหวัด”). A second MOPH agency hub runs on `hdc.dms.go.th/hdc/` (Department of Medical Services), which the `hdc.moph.go.th` host query does not match.

**Signals:** host `hdc.moph.go.th`; path `/{tenant}/public/` or `/{tenant}/public/main`; title “HDC Service”; chrome “ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ (HDC)”; `assets/images/moph-logo.gif`; link to `dmdmoph.github.io/hdc-docs`.

**Confirm:** GET the public report home (`/public/` or `/public/main`), not the login/register flow. One catalog for the `/center/` hub. Do **not** add a catalog per guessed provincial slug — there is no official slug list, and `/center/public/` already covers the warehouse by region and province.

**False positives:** Health KPI (`healthkpi.moph.go.th`); DDC surveillance (`ddsdoe.ddc.moph.go.th`); `opendata.moph.go.th` table API wrappers; login-only 43-file upload / data-exchange screens.

| Tool | Query |
|------|-------|
| Google | `site:hdc.moph.go.th "ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ"` |
| Google | `"HDC Service" "สำนักงานสาธารณสุขจังหวัด" site:hdc.moph.go.th` |
| Censys | `web.names: "hdc.moph.go.th"` |
| FOFA | `host="hdc.moph.go.th"` |
| FOFA | `host="hdc.dms.go.th"` |
| FOFA | `title="HDC Service"` |

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
| FOFA | `body="@krista.ru"` |
| FOFA | `body="static-report/web/middleware"` |
| FOFA | `body="acr_reports"` |
| FOFA | `body="mdxexpert"` |
| FOFA | `body="mdx-expert"` |
| FOFA | `body="konstruktor-dannykh"` |
| crt.sh | `%.ifinmon.ru` |

`body="static-report/web/middleware"` and `body="acr_reports"` are the Krista report shell (served HTML, not the vendor email). `body="mdxexpert"` / `body="mdx-expert"` is the public data constructor — prefer it when the hunt must keep catalogs that list datasets. `body="konstruktor-dannykh"` is the alternate transliteration of the constructor path (`konstruktor-dannyx` was the earlier query).

**FOFA false positives (September 2026):** `title="iMonitoring"` matches diabetes, media-monitoring, and IT-monitoring products. `body="content=\"MYOB\""` matches unrelated Joomla sites. `body="kristaBIContext"` returned no indexed hosts. `body="themeManager.min.js"` also hits banking portals. `body="НПО Криста"` and `body="8-800-200-20-73"` hit the vendor site, branch offices, and login-only budget systems (`plan.minfinrk.ru` redirects to `/login`). Procurement GIS hosts such as `zakupki.eao.ru` share the report shell but are the regional contract system, not an Open Budget catalog. Crimea `ib.` / `shkib.` / `stib.budget.rk.ifinmon.ru` are sections of the already registered `budget.rk.ifinmon.ru` portal.

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

## Fingertips (`fingertips`) {#fingertips}

OHID public health profiles for England. Hub: [fingertips.phe.org.uk](https://fingertips.phe.org.uk/). API docs: [Fingertips API](https://fingertips.phe.org.uk/profile/guidance/supporting-information/api).

**Signals:** host `fingertips.phe.org.uk`; title “Fingertips”; REST `/api/profiles`.

**Confirm:** GET `/api/profiles` JSON or the public profiles home. One national hub — do **not** add a catalog per local authority or per profile. Distinct from IBIS-PH, Power BI embeds, and InstantAtlas reports.

| Tool | Query |
|------|-------|
| Google | `"Fingertips" ("public health profiles" OR OHID) site:phe.org.uk` |
| Censys | `web.names: "fingertips.phe.org.uk"` |
| FOFA | `host="fingertips.phe.org.uk"` |

## DHIS2 (`dhis2`) {#dhis2}

Open-source health management information system (HISP / University of Oslo). More than 70 ministries run national HMIS instances. Docs: [docs.dhis2.org](https://docs.dhis2.org). Public FlexiPortal front-ends also count when they publish indicators from a DHIS2 backend. Use `software.id: dhis2`. Do not label a CKAN health document site DHIS2 from a tag alone.

**Signals:** `/dhis-web-commons/`, `/dhis-web-dashboard/`, login chrome “DHIS 2”; REST `/api/system/info`.

**Confirm:** anonymous `GET https://host/api/dataSets.json?fields=id,displayName&pageSize=1` or `/api/indicators.json` with `pager.total` greater than 0. A login shell is not enough. Skip staff-only logins, dev/test/training/sandbox hosts, and `play.dhis2.org` / `*.im.dhis2.org` demos.

[login.html](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/dhis-web-api/src/main/resources/org/hisp/dhis/webapi/controller/login.html) loads `dhis-web-commons` (3,065 hosts in September 2026, including `sl.dhis2.org` and `dhis-pbf.moh.gov.et`). `body="DHIS2"` is not usable: it matched 5,074 hosts, including `ucb.go.ug`.

[shell/index.html](https://github.com/dhis2/app-platform/blob/master/shell/index.html) sets `<meta name="dhis2-base-url">` and mounts `#dhis2-app-root` and `#dhis2-portal-root` (798 and 779 domain hosts in September 2026 for `dhis2-app-root` and `dhis2-base-url`, including `dashboards.migeprof.gov.rw`). GitHub code search for `dhis2-base-url filename:index.html` hits the template and app skeletons; committed copies keep the placeholder `__DHIS2_BASE_URL__` and do not list instances. `dhis.conf` `server.base.url` hits are Ansible templates. These strings are not usable as FOFA queries: `body="logo_front.png"` (1,232 hosts, including `tiendaya.co`), `body="twoFAToggle"` (1,112, including SureMDM), `body="api/loginConfig"` (50, generic cloud-login pages), `body="You are logging in using the fallback login page."` (0), and `body="Powered by DHIS2."` (17, including `docs.dhis2.org`).

| Tool | Query |
|------|-------|
| Google | `"DHIS2" OR "DHIS 2" (HMIS OR "health information" OR portal) -site:dhis2.org -site:github.com` |
| Google | `inurl:/dhis-web-commons OR inurl:/api/system/info` |
| Censys | `web.endpoints.http.body: "dhis-web-commons"` |
| FOFA | `body="dhis-web-commons"` |
| Censys | `web.endpoints.http.html_title: "DHIS 2"` |
| FOFA | `title="DHIS 2"` |
| GitHub | `dhis2-base-url filename:index.html` |
| Censys | `web.endpoints.http.body: "dhis2-app-root"` |
| FOFA | `body="dhis2-app-root" && is_domain=true` |
| FOFA | `body="dhis2-base-url" && is_domain=true` |

## ActivityInfo (`activityinfo`) {#activityinfo}

Hosted M&E / humanitarian-coordination platform (BeDataDriven, Netherlands). Single SaaS at [www.activityinfo.org](https://www.activityinfo.org) — there are no independent instances to find. OCHA, UNHCR, UNICEF, WHO and NGO consortia use it for 4W/5W response monitoring; owners can publish live dashboards as standalone no-login pages or feed public Power BI / Shiny portals through the REST API. Public catalogs surface two ways: (1) published report pages on `activityinfo.org`, (2) API-fed portals on organization domains — e.g. [R4V RMRP Activity Explorer](https://www.r4v.info/en/activity_explorer) and the OCHA Ukraine response dashboards on [response.reliefweb.int/ukraine](https://response.reliefweb.int/ukraine). Use `software.id: activityinfo` for both surfaces. Raw 5W exports are often mirrored on HDX — do not register the HDX mirror as ActivityInfo.

**Signals:** standalone pages under `www.activityinfo.org/app#...`; methodology text saying data is "reported in ActivityInfo" or "collected through ActivityInfo"; cluster guidance PDFs naming an ActivityInfo database; Power BI dashboards on reliefweb.int / humanitarianresponse.info response pages.

**Confirm:** the published page or dashboard loads without login, or the portal documents ActivityInfo as the reporting backend. Skip login-only databases — most ActivityInfo databases are internal coordination tools, not public catalogs.

| Tool | Query |
|------|-------|
| Google | `"reported in ActivityInfo" OR "reporting in ActivityInfo" dashboard` |
| Google | `"ActivityInfo" ("5W" OR "4W" OR "response monitoring") (dashboard OR "data portal")` |
| Google | `site:reliefweb.int "ActivityInfo" dashboard` |
| Google | `site:humanitarianresponse.info "ActivityInfo" dashboard` |

## TabNet (`tabnet`) {#tabnet}

DATASUS CGI tabulator for Brazilian SUS health databases. National hub: [Informações de Saúde (TABNET)](https://datasus.saude.gov.br/informacoes-de-saude-tabnet). States, municipalities, and ANS run separate installations. Use `software.id: tabnet`. Distinct from the OpenDataSUS CKAN portal.

**Signals:** HTML title “TabNet Win32”; paths `deftohtm.exe`, `tabcgi.exe`, `cgi-bin/dh?`; `.def` query forms; “Copia para Tabwin”.

**Confirm:** GET a public table menu or a `.def` form. One catalog per installation (national vs SES vs municipal vs ANS). Do not add every `.def` table as its own catalog. Skip TabWin desktop downloads and login-only intranet copies.

**False positives:** pytorch-tabnet / tabular ML libraries; a CMS page that only links to the national DATASUS TabNet; IBGE SIDRA (`sidra`).

| Tool | Query |
|------|-------|
| Google | `"TabNet Win32" site:.gov.br` |
| Google | `inurl:deftohtm.exe OR inurl:tabcgi.exe OR inurl:/cgi-bin/dh site:.gov.br` |
| Google | `"Informações de Saúde" TABNET (secretaria OR municipal) site:.gov.br` |
| Censys | `web.endpoints.http.html_title: "TabNet Win32"` |
| FOFA | `title="TabNet Win32"` |
| Censys | `web.endpoints.http.body: "deftohtm.exe"` |
| FOFA | `body="deftohtm.exe"` |

## SIDRA (`sidra`) {#sidra}

IBGE automatic table-retrieval system. Hub: [sidra.ibge.gov.br](https://sidra.ibge.gov.br). Aggregates API: [servicodados.ibge.gov.br/api/v3/agregados](https://servicodados.ibge.gov.br/api/v3/agregados).

**Signals:** host `sidra.ibge.gov.br`; title “SIDRA” / “Sistema IBGE de Recuperação Automática”.

**Confirm:** GET the public table builder or `/api/v3/agregados` JSON. One catalog for the SIDRA hub. Do **not** retag IBGE Cidades@, Ipeadata, Comex Stat, BCB SGS, or DATASUS TabNet.

| Tool | Query |
|------|-------|
| Google | `site:sidra.ibge.gov.br (SIDRA OR agregados)` |
| Censys | `web.names: "sidra.ibge.gov.br"` |
| FOFA | `host="sidra.ibge.gov.br"` |

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

**Signals:** `id="statsilk-container"`; HTML title `StatPlanet`; `StatPlanet Cloud`; `StatPlanet_Cloud.html`; `data.csv` / `settings.csv`; StatSilk footer or logo; URL params `i=` `v=` `t=` on Cloud dashboards.

**Confirm:** GET the dashboard HTML and a public `data.csv` (or SDMX-backed Cloud instance). One record per public explorer, not per indicator or per `*-StatTrends.html` file on the same host.

[StatPlanet_Cloud.html](https://github.com/StatSilk/StatPlanet/blob/master/StatPlanet_Cloud.html) sets `id="statsilk-container"` (5 hosts in September 2026, including `unicefdashboard.netlify.app` and `statplanet.itcloud.pt`). The same file writes `StatPlanet Cloud` (4 hosts, all `statplanet.itcloud.pt`). `title="StatPlanet"` matched 7; three of those rows are `statplanet.org`, a business site titled “Statplanet — Premium Business”, not a StatSilk dashboard.

| Tool | Query |
|------|-------|
| Google | `"StatPlanet Cloud" OR "StatPlanet_Cloud.html" (indicators OR statistics)` |
| Google | `"powered by StatSilk" OR intitle:StatPlanet (map OR dashboard)` |
| Censys | `web.endpoints.http.body: "statsilk-container"` |
| FOFA | `body="statsilk-container"` |
| Censys | `web.endpoints.http.body: "StatPlanet Cloud"` |
| FOFA | `body="StatPlanet Cloud"` |

**False positives:** statsilk.com marketing, GitHub `StatSilk/StatPlanet`, Flash-only dead maps, a single thematic poster, StatPlanet World Bank / EdStats viewers of [data.worldbank.org](https://data.worldbank.org) (already `dataworldbankorg`), `statplanet.org` (“Premium Business”). Skip login-only corporate dashboards.

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

## TYPO3 (`typo3`) {#typo3}

Statistics/indicator sections published on TYPO3 CMS sites (statistical offices, ministries, regional monitoring portals) instead of a data platform. Used by Statistik Austria, ISTAT, and several German indicator portals.

**Signals:** `<meta name="generator" content="TYPO3 CMS">`; `/typo3conf/` and `/typo3temp/` asset paths; `tx_` extension parameters in URLs.

**Confirm:** GET the statistics section and confirm it is TYPO3-driven (generator meta or `typo3conf` assets). One catalog per institution. Skip pages that only host downloads while the catalog itself runs on another platform.

| Tool | Query |
|-------|-------|
| Google | `"TYPO3 CMS" (statistics OR indicators OR statistik) site:.gov OR site:.gv.at` |
| Censys | `web.endpoints.http.body: "content=\"TYPO3 CMS\""` + manual review for statistics content |
| FOFA | `body="content=\"TYPO3 CMS\""` |

**False positives:** TYPO3 agency showcases; government sites whose statistics section is a separate non-TYPO3 application.

## SPIP (`spip`) {#spip}

Statistics/indicator sections published on SPIP, a French open-source CMS used by French regional observatories and data portals (carif-oref networks, regional data observatories).

**Signals:** `<meta name="generator" content="SPIP">`; `spip.php?page=` URLs; `/squelettes/` and `/plugins/` asset paths.

**Confirm:** GET the statistics section and confirm it is SPIP-driven (generator meta or `spip.php` URLs). One catalog per institution.

| Tool | Query |
|-------|-------|
| Google | `"SPIP" (observatoire OR indicateurs OR statistiques) site:.fr` |
| Censys | `web.endpoints.http.body: "content=\"SPIP\""` + manual review for statistics content |
| FOFA | `body="content=\"SPIP\""` |

**False positives:** SPIP community/documentation sites; observatory pages with no indicator tables.

## Contao (`contao`) {#contao}

Statistics/indicator sections published on Contao, an open-source CMS used by statistical offices and data portals in Germany and Switzerland (cantonal statistics, federal topic portals).

**Signals:** `<meta name="generator" content="Contao Open Source CMS">`; `/contao/` asset paths; `tl_` CSS classes.

**Confirm:** GET the statistics section and confirm it is Contao-driven (generator meta). One catalog per institution.

| Tool | Query |
|-------|-------|
| Google | `"Contao Open Source CMS" (statistik OR statistique OR datenportal)` |
| Censys | `web.endpoints.http.body: "content=\"Contao Open Source CMS\""` + manual review for statistics content |
| FOFA | `body="content=\"Contao Open Source CMS\""` |

**False positives:** Contao agency showcases; sites whose data section is a separate non-Contao application.

## R Shiny (`shiny`) {#shiny}

Shiny (Posit/RStudio) web applications deployed as statistical query tools and indicator dashboards — self-hosted (`shiny.<agency>`, `/shiny/` paths) or on `*.shinyapps.io`.

**Signals:** `shared/shiny.css`, `shiny.min.js`, `shiny-javascript-*`; `shiny-connected`; `*.shinyapps.io` hosts.

**Confirm:** GET the app and confirm the app **itself** is Shiny (its HTML loads shiny.min.js), not a portal that merely links to a Shiny tool elsewhere. One catalog per app (or per tool family under one path). Skip RStudio marketing and teaching/demo apps.

[shiny.min.css](https://github.com/rstudio/shiny/blob/main/inst/www/shared/shiny.min.css) is served as `shared/shiny.min.css` (1,536 hosts in September 2026, including `amrmap.net`). That is every indexed Shiny app, so still require a statistics or indicator catalog.

| Tool | Query |
|-------|-------|
| Google | `inurl:shinyapps.io (statistics OR indicators OR dashboard)` |
| Google | `"shiny.min.js" (statistics OR "data portal") site:.gov` |
| Censys | `web.endpoints.http.body: "shared/shiny.min.css"` |
| FOFA | `body="shared/shiny.min.css"` |

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

[superset/templates/superset/spa.html](https://github.com/apache/superset/blob/master/superset/templates/superset/spa.html) sets `localStorage` key `superset-theme-mode` (4,915 hosts in September 2026). The same file sets `window.__SUPERSET_LANGUAGE_PACK__` (108 hosts). `body="Superset"` matched about 130,000 unrelated hosts.

| Tool | Query |
|------|-------|
| Google | `"Apache Superset" (open data OR indicators)` |
| Censys | `web.endpoints.http.body: "superset-theme-mode"` |
| FOFA | `body="superset-theme-mode"` |
| FOFA | `body="__SUPERSET_LANGUAGE_PACK__"` |

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

## UNdata (`undata`) {#undata}

UN Statistics Division official statistics portal. Hub: [data.un.org](https://data.un.org).

**Confirm:** do **not** re-add data.un.org. Register only a distinct UN statistical catalog UI (for example Comtrade Plus, already `comtradeplus`).

| Tool | Query |
|------|-------|
| Google | `"UNdata" (statistics OR databank) -site:data.un.org` |
| Censys | `web.names: "data.un.org"` |
| FOFA | `host="data.un.org"` |

## UN Comtrade Plus (`comtradeplus`) {#comtradeplus}

UN merchandise trade statistics. Hub: [comtradeplus.un.org](https://comtradeplus.un.org/).

**Confirm:** do **not** re-add comtradeplus.un.org. Distinct from WITS (`wits.worldbank.org`) and UNdata.

| Tool | Query |
|------|-------|
| Google | `"UN Comtrade Plus" OR site:comtradeplus.un.org` |
| Censys | `web.names: "comtradeplus.un.org"` |
| FOFA | `host="comtradeplus.un.org"` |

## Our World in Data (`ourworldindata`) {#ourworldindata}

Global Change Data Lab indicator catalog. Hub: [ourworldindata.org](https://ourworldindata.org).

**Confirm:** do **not** re-add ourworldindata.org or add every chart URL. Distinct from Gapminder WordPress data-download pages.

[SiteFooter.tsx](https://github.com/owid/owid-grapher/blob/master/site/SiteFooter.tsx) links `Teaching with OWID` (26 hosts in September 2026, including the fork `aging-data-lab.org` and the hub; `thinkdataforgovernment.com` is a copied page, not a catalog). `body="Our World in Data"` matched 2,463 unrelated sites. Keep the host query for the canonical hub.

| Tool | Query |
|------|-------|
| Google | `"Our World in Data" (indicators OR grapher) -site:ourworldindata.org` |
| Censys | `web.endpoints.http.body: "Teaching with OWID"` |
| FOFA | `body="Teaching with OWID"` |
| Censys | `web.names: "ourworldindata.org"` |
| FOFA | `host="ourworldindata.org"` |

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
| `undata` | see above | |
| `comtradeplus` | see above | |
| `ourworldindata` | see above | |
| `kosis` | see above | |
| `estat` | see above | |
| `sidra` | see above | |
| `fingertips` | see above | |
| `datainsight` | see above | |

National statistical office homepages often link “database”, “statbank”, “PC-Axis”, “SDMX”. Follow those links rather than guessing software from the NSO CMS.

## NADA (`nada`) {#nada}

IHSN National Data Archive for survey microdata. Site: [nada.ihsn.org](https://nada.ihsn.org). UI: study catalog, often `/index.php/catalog`.

**Confirm:** `https://host/index.php/api/catalog/search` (JSON) or the public catalog listing without login.

The theme footers [themes/nada/footer.php](https://github.com/ihsn/nada/blob/main/themes/nada/footer.php) and [themes/nada52/footer.php](https://github.com/ihsn/nada/blob/main/themes/nada52/footer.php) ship the class `nada-logo`. `body="NADA"` is not usable: in September 2026 it matched about 1.4 million unrelated hosts. `body="nada-logo"` matched 617, including `repositorio.um.edu.cv`. `full-row-footer-black-components` is only the nada52 footer (201 hosts) and misses the older theme.

| Tool | Query |
|------|-------|
| Google | `"NADA" "microdata" OR "national data archive" IHSN` |
| Google | `inurl:/index.php/catalog "microdata"` |
| Google | `"Powered by NADA" OR "nada" "survey catalog"` |
| Censys | `web.endpoints.http.body: "nada-logo"` |
| FOFA | `body="nada-logo"` |
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

[footer.ftl](https://github.com/obiba/mica2/blob/master/mica-webapp/src/main/resources/_templates/libs/footer.ftl) links `https://www.obiba.org` (115 hosts in September 2026, including `mica.clinicalresearch.nl`). “Powered by” is an i18n string, so the href is the contiguous token. `body="obiba"` matched 347, including `maelstrom-research.org`. Keep both.

| Tool | Query |
|------|-------|
| Google | `"Mica" OBiBa (studies OR catalog) -site:github.com` |
| Censys | `web.endpoints.http.body: "www.obiba.org"` |
| FOFA | `body="www.obiba.org"` |
| Censys | `web.endpoints.http.body: "obiba"` |
| FOFA | `body="obiba"` |
| Censys | `web.endpoints.http.body: "Mica"` |
| FOFA | `body="Mica"` |

## Survey Solutions (`surveysolutions`) {#surveysolutions}

World Bank survey suite. Register only a **public Data Browser** of microdata, not a data-collection server. **Reject** `*.mysurvey.solutions` / KNBS/INE interviewer hosts — they are survey collection platforms, not catalogs (September 2026 instance hunt).

[index.html](https://github.com/surveysolutions/surveysolutions/blob/master/src/UI/WB.UI.Frontend/index.html) defines `__setLocaleData__` (815 hosts in September 2026, including `encuestas.bch.hn`). That shell is the headquarters app, not a Data Browser. Do not use it as the catalog query.

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
| FOFA | `body="DataWarehousePro"` |
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

**Signals:** title `Goal Tracker`; header classes `bg-goals-1` … `bg-goals-17` (the 17-stripe SDG bar). Current Strapi builds also embed `hasOwnData` on each indicator. Tenant HTML does not contain “Data Act Lab”. `host="goaltracker"` matches unrelated goal-tracking apps.

**Confirm:** GET the country tenant home. Keep the record only when the page JSON lists indicators that have data (`hasData` / `hasOwnData`, or a non-empty `data` series). One record per country site. Skip the vendor marketing page (`goaltracker.org`, `test.goaltracker.org`), Strapi admin (`*.api.goaltracker.org`), and `401` hosts.

| Tool | Query |
|------|-------|
| Google | `site:goaltracker.org` |
| Google | `"Goal Tracker" (SDG OR "Global Goals") -site:goaltracker.org/about` |
| Censys | `web.names: "goaltracker.org"` |
| FOFA | `title="Goal Tracker" && body="bg-goals-17"` |
| FOFA | `title="Goal Tracker" && body="hasOwnData"` |
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

## GeCO-sys OpenData (`gecoopendata`) {#gecoopendata}

Cancer-registry epidemiological-indicator application used by Italian registries (Veneto, Umbria, ASL Napoli 3 Sud). Documented as a reusable product by the [Registro Tumori Veneto](https://www.registrotumoriveneto.it/english/publications/meetings/posters/2018-posters/territorial-extension-of-the-veneto-tumour-registry-and-data-usability-in-the-new-web-portal/). Use `software.id: gecoopendata`. Distinct from GeCo, the Lombardy regional-council management application.

**Signals:** hostname `gecoopendata.{registry-domain}`; pages `/incidenza.php`, `/sopravvivenza.php` (also under `/web/`); AdminBSB theme assets (`css/themes/all-themes.css`, `plugins/node-waves/`); `GeCOsys` strings; indicator forms for incidence, mortality, survival, prevalence by tumour site, age, sex, and territory.

**Confirm:** GET `/incidenza.php` and check for GeCOsys branding and the AIRTUM-based indicator forms. One catalog per registry tenant.

**False positives:** the Lombardy `GeCo` ASP.NET council app; generic AIRTUM monograph PDF pages.

| Tool | Query |
|------|-------|
| Google | `"GeCO-sys OpenData" OR "gecoopendata" registro tumori` |
| Google | `inurl:gecoopendata incidenza.php` |
| Censys | `web.names: "gecoopendata.*"` |
| FOFA | `body="GeCOsys" && body="incidenza"` |

## Grafana (`grafana`) {#grafana}

Open-source dashboard platform (Grafana Labs). Almost all internet-facing instances are private operations monitors — the registry only keeps the rare **anonymous-access instances that publish statistical/indicator dashboards** (energy mix, weather-station networks, IXP traffic, honeypot telemetry). Product page: [grafana.com](https://grafana.com). Use `software.id: grafana`.

**Signals:** HTML title `Grafana`; `GET /api/health` returns JSON; login chrome "Welcome to Grafana". [public/views/index.html](https://github.com/grafana/grafana/blob/main/public/views/index.html) links `grafana_mask_icon.svg` (784,980 hosts in September 2026). That icon is every Grafana install, not a catalog list, so keep the government-host filters.

**Confirm:** `GET https://host/api/search?limit=100` returns `200` with a dashboard list **without credentials** (anonymous auth enabled). `401`/`403` means login-only — reject. Then read the dashboard titles: keep instances whose dashboards publish public statistics (ministry/NSO indicators, environmental or internet-infrastructure telemetry); reject server/Kubernetes/crypto/game/service monitoring (node exporter, perfSONAR host metrics, HPC loads). One record per public tenant.

| Tool | Query |
|------|-------|
| Google | `intitle:"Grafana" site:.gov OR site:.gob.* OR site:.go.*` |
| Censys | `web.endpoints.http.html_title: "Grafana" and web.names: "grafana"` |
| FOFA | `title="Grafana" && host=".gov"` |
| FOFA | `title="Grafana" && host=".gob."` |

## EPS Data Platform (`epsdata`) {#epsdata}

Vendor-operated single-tenant SaaS. Site: [epsnet.com.cn](https://www.epsnet.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `epsnet.com.cn`; page chrome “EPS数据平台”; database list under `/index.html`.

**Confirm:** GET the platform home; the database catalog is described publicly even though series values need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:epsnet.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="epsnet.com.cn"` |


## CNKI Economic and Social Big Data Research Platform (`cnkidata`) {#cnkidata}

Vendor-operated single-tenant SaaS. Site: [data.cnki.net](https://data.cnki.net). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `data.cnki.net`; title “中国经济社会大数据研究平台”; CNKI chrome; anti-bot `418` responses are normal.

**Confirm:** GET the platform home; yearbook and indicator catalogs are listed publicly before the paywall.

| Tool | Query |
|------|-------|
| Google | `site:data.cnki.net (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="data.cnki.net"` |


## CEInet Statistical Database (`ceinet`) {#ceinet}

Vendor-operated single-tenant SaaS. Site: [cei.cn](https://db.cei.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** hosts `db.cei.cn` (中经网统计数据库) and `ceidata.cei.cn` (中经数据); titles name the platform.

**Confirm:** GET either host home; both returned `200` with indicator navigation during verification.

| Tool | Query |
|------|-------|
| Google | `site:cei.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="cei.cn"` |


## DRCNet Statistical Database (`drcnet`) {#drcnet}

Vendor-operated single-tenant SaaS. Site: [data.drcnet.com.cn](https://data.drcnet.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `data.drcnet.com.cn`; 国研网 chrome; CN geo-fencing causes timeouts from non-CN networks.

**Confirm:** GET the platform home from a CN-reachable network; title names 国研网统计数据库.

| Tool | Query |
|------|-------|
| Google | `site:data.drcnet.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="data.drcnet.com.cn"` |


## Soshoo (`soshoo`) {#soshoo}

Vendor-operated single-tenant SaaS. Site: [soshoo.com](http://www.soshoo.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.soshoo.com` over plain HTTP; title “搜数网”; `.do` Struts paths such as `/index.do`.

**Confirm:** GET `http://www.soshoo.com` (HTTPS fails); home lists the statistical database catalog.

| Tool | Query |
|------|-------|
| Google | `site:soshoo.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="soshoo.com"` |


## MacroChina Database (`macrochina`) {#macrochina}

Vendor-operated single-tenant SaaS. Site: [macrochina.com.cn](http://www.macrochina.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.macrochina.com.cn`; root serves a JS redirect to `info.shtml`; 中宏数据库 product pages.

**Confirm:** GET `http://www.macrochina.com.cn` and follow to `info.shtml`; HTTPS root returns `404` by design.

| Tool | Query |
|------|-------|
| Google | `site:macrochina.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="macrochina.com.cn"` |


## Pishu Database (`pishu`) {#pishu}

Vendor-operated single-tenant SaaS. Site: [pishu.com.cn](https://www.pishu.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.pishu.com.cn`; title “皮书数据库”; paths under `/skwx_ps/database`.

**Confirm:** GET the platform home; it redirects to the database catalog with `SiteID` parameters.

| Tool | Query |
|------|-------|
| Google | `site:pishu.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="pishu.com.cn"` |


## Wind Economic Database (`wind`) {#wind}

Vendor-operated single-tenant SaaS. Site: [wind.com.cn](https://www.wind.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.wind.com.cn`; title “万得信息网”; EDB product pages describe the economic database.

**Confirm:** GET the vendor home; the EDB indicator database is documented publicly though series need a terminal subscription.

| Tool | Query |
|------|-------|
| Google | `site:wind.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="wind.com.cn"` |


## CEIC Data (`ceic`) {#ceic}

Vendor-operated single-tenant SaaS. Site: [ceicdata.com](https://www.ceicdata.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.ceicdata.com`; title names CEIC; public indicator pages under `/en/indicator/`.

**Confirm:** GET the home or a public indicator page; indicator catalog is browsable without login.

| Tool | Query |
|------|-------|
| Google | `site:ceicdata.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="ceicdata.com"` |


## CSMAR (`csmar`) {#csmar}

Vendor-operated single-tenant SaaS. Site: [data.csmar.com](https://data.csmar.com) (moved from `data.gtadata.com`). University pages are library guides or WebVPN aliases of that host, not separate deployments. A September 2026 pass with the shell and HiDa fingerprints below found no additional host whose public response lists datasets.

**Signals:** index HTML loads `/csmar.html` and stores `solution_t` in `sessionStorage`; title `CSMAR`. Config lives in `/config/config.js` (`window.APIURL`, `/api/csmar-main`). Legacy hosts `cn.gtadata.com` and `www.gtarsc.com` only show “该域名已不再使用” and link to `data.csmar.com`. HiDa (`hida.csmar.com`, port 5003, title “希施玛 · HiDa财经终端”) is the same vendor’s terminal; the data dictionary is `hida.csmar.com:8080` (title “CSMAR财经数据说明书”).

`body="/csmar.html"`, `body="__path__full__"`, and `body="sessionStorage.setItem('solution_"` are the shell (about 18 named hosts in September 2026, all `csmar.com` / `gtadata.com` or bare IPs). `body="api/csmar-main"` and `body="js/csmar."` match nothing: those strings are in JavaScript, which FOFA does not index. `icon_hash="239425243"` (the 1,284-byte favicon) collides with hundreds of unrelated sites. `title="国泰安"` is insurance and teaching-system noise. `body="经济金融研究数据库"` is library A–Z pages. `host="csmar" && host=".edu.cn"` is WebVPN and ezproxy.

**Confirm:** Keep a host only when a public response lists datasets or tables (`tbname` or a database list with rows). `GET /api/csmar-main/single/getSeriesTree/-1` on the Vue shells returns 401. HiDa `GET /api/GetWholeTheme/` returns 269 theme folders and every `tbname` is null; `ListSearchTheme` and `TableFields` require a customer session; the `:8080` dictionary returns “缺少 token”. Skip those, skip “该域名已不再使用” notices, bare IPs of an already registered host, WebVPN and `*.sjuku.top` aliases, trading simulators (`实盘大赛`, 投资交易仿真), and `www.csmar.com` (marketing).

| Tool | Query |
|------|-------|
| Google | `site:data.csmar.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="csmar.com" \|\| domain="gtadata.com"` |
| FOFA | `body="/csmar.html"` |
| FOFA | `body="__path__full__"` |
| FOFA | `body="sessionStorage.setItem('solution_"` |
| FOFA | `title="CSMAR财经数据说明书"` |
| FOFA | `body="HiDa财经终端"` |


## RESSET (`resset`) {#resset}

Vendor-operated single-tenant SaaS. Site: [resset.com](https://www.resset.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.resset.com`; 锐思数据 chrome; database product list on the home page.

**Confirm:** GET the vendor home; the research database catalog is listed publicly.

| Tool | Query |
|------|-------|
| Google | `site:resset.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="resset.com"` |


## East Money Data Center (`eastmoneydata`) {#eastmoneydata}

Vendor-operated single-tenant SaaS. Site: [data.eastmoney.com](https://data.eastmoney.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `data.eastmoney.com`; title “数据中心 _ 东方财富网”; free indicator tables.

**Confirm:** GET the data center home; macro/market indicator tables are public.

| Tool | Query |
|------|-------|
| Google | `site:data.eastmoney.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="data.eastmoney.com"` |


## East Money Choice (`choice`) {#choice}

Vendor-operated single-tenant SaaS. Site: [choice.eastmoney.com](https://choice.eastmoney.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `choice.eastmoney.com`; title “Choice数据-智能金融终端”.

**Confirm:** GET the Choice portal home; product and indicator coverage are described publicly.

| Tool | Query |
|------|-------|
| Google | `site:choice.eastmoney.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="choice.eastmoney.com"` |


## Tonghuashun Data Center (`thsdata`) {#thsdata}

Vendor-operated single-tenant SaaS. Site: [data.10jqka.com.cn](https://data.10jqka.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `data.10jqka.com.cn`; title “同花顺数据中心”; free indicator tables.

**Confirm:** GET the data center home; market/macro indicator tables are public.

| Tool | Query |
|------|-------|
| Google | `site:data.10jqka.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="data.10jqka.com.cn"` |


## Tonghuashun iFinD (`ifind`) {#ifind}

Vendor-operated single-tenant SaaS. Site: [51ifind.com](https://www.51ifind.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.51ifind.com`; title “同花顺iFinD”; note `ifind.10jqka.com.cn` is geo-fenced.

**Confirm:** GET `https://www.51ifind.com`; the iFinD indicator databases are documented publicly.

| Tool | Query |
|------|-------|
| Google | `site:51ifind.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="51ifind.com"` |


## Gildata (`gildata`) {#gildata}

Vendor-operated single-tenant SaaS. Site: [gildata.com](https://www.gildata.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.gildata.com`; 聚源数据 chrome (GBK encoding).

**Confirm:** GET the vendor home; database products are listed publicly.

| Tool | Query |
|------|-------|
| Google | `site:gildata.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="gildata.com"` |


## Go-Goal (`gogoal`) {#gogoal}

Vendor-operated single-tenant SaaS. Site: [go-goal.com](https://www.go-goal.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.go-goal.com`; title “朝阳永续”.

**Confirm:** GET the vendor home; consensus/earnings databases are described publicly.

| Tool | Query |
|------|-------|
| Google | `site:go-goal.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="go-goal.com"` |


## CNRDS (`cnrds`) {#cnrds}

Vendor-operated single-tenant SaaS. Site: [cnrds.com](https://www.cnrds.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.cnrds.com`; title “Chinese Research Data Services Platform”; bilingual pages.

**Confirm:** GET the platform home; the research database module catalog is public.

| Tool | Query |
|------|-------|
| Google | `site:cnrds.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="cnrds.com"` |


## DataYes (`datayes`) {#datayes}

Vendor-operated single-tenant SaaS. Site: [robo.datayes.com](https://robo.datayes.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `robo.datayes.com`; 萝卜投研 chrome.

**Confirm:** GET the Robo portal home; indicator/research coverage is described publicly.

| Tool | Query |
|------|-------|
| Google | `site:robo.datayes.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="robo.datayes.com"` |


## Qianzhan Database (`qianzhan`) {#qianzhan}

Vendor-operated single-tenant SaaS. Site: [d.qianzhan.com](https://d.qianzhan.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `d.qianzhan.com`; title “前瞻数据库”; free macro/industry indicator tables.

**Confirm:** GET the database home; indicator tables are public.

| Tool | Query |
|------|-------|
| Google | `site:d.qianzhan.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="d.qianzhan.com"` |


## AskCI (`askci`) {#askci}

Vendor-operated single-tenant SaaS. Site: [askci.com](https://www.askci.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.askci.com`; title “中商情报网”; industry data navigation.

**Confirm:** GET the portal home; industry statistics sections are public.

| Tool | Query |
|------|-------|
| Google | `site:askci.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="askci.com"` |


## Huaon (`huaon`) {#huaon}

Vendor-operated single-tenant SaaS. Site: [huaon.com](https://www.huaon.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.huaon.com`; title “华经情报网”.

**Confirm:** GET the portal home; industry statistics sections are public.

| Tool | Query |
|------|-------|
| Google | `site:huaon.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="huaon.com"` |


## Chyxx (`chyxx`) {#chyxx}

Vendor-operated single-tenant SaaS. Site: [chyxx.com](https://www.chyxx.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.chyxx.com`; title “智研咨询”.

**Confirm:** GET the portal home; industry statistics sections are public.

| Tool | Query |
|------|-------|
| Google | `site:chyxx.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="chyxx.com"` |


## ChinaBgao (`chinabgao`) {#chinabgao}

Vendor-operated single-tenant SaaS. Site: [chinabgao.com](https://www.chinabgao.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.chinabgao.com`; title “报告大厅”.

**Confirm:** GET the portal home; report/indicator navigation is public.

| Tool | Query |
|------|-------|
| Google | `site:chinabgao.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="chinabgao.com"` |


## Bosidata (`bosidata`) {#bosidata}

Vendor-operated single-tenant SaaS. Site: [bosidata.com](https://www.bosidata.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.bosidata.com`; 博思数据 chrome (GBK encoding).

**Confirm:** GET the portal home; market data sections are public.

| Tool | Query |
|------|-------|
| Google | `site:bosidata.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="bosidata.com"` |


## LeadLeo (`leadleo`) {#leadleo}

Vendor-operated single-tenant SaaS. Site: [leadleo.com](https://www.leadleo.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.leadleo.com`; 头豹 chrome; JS-rendered landing (short initial body).

**Confirm:** GET the portal home; industry report/indicator navigation is public.

| Tool | Query |
|------|-------|
| Google | `site:leadleo.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="leadleo.com"` |


## iiMedia Data Center (`iimedia`) {#iimedia}

Vendor-operated single-tenant SaaS. Site: [data.iimedia.cn](https://data.iimedia.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `data.iimedia.cn`; title “艾媒智库.数据中心”.

**Confirm:** GET the data center home; indicator navigation is public though most series need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:data.iimedia.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="data.iimedia.cn"` |


## Analysys (`analysys`) {#analysys}

Vendor-operated single-tenant SaaS. Site: [analysys.cn](https://www.analysys.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.analysys.cn`; title “易观分析”.

**Confirm:** GET the portal home; analysis/indicator articles are public.

| Tool | Query |
|------|-------|
| Google | `site:analysys.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="analysys.cn"` |


## iResearch (`iresearch`) {#iresearch}

Vendor-operated single-tenant SaaS. Site: [iresearch.com.cn](https://www.iresearch.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.iresearch.com.cn`; 艾瑞咨询 chrome.

**Confirm:** GET the portal home; research/indicator sections are public.

| Tool | Query |
|------|-------|
| Google | `site:iresearch.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="iresearch.com.cn"` |


## QuestMobile (`questmobile`) {#questmobile}

Vendor-operated single-tenant SaaS. Site: [data.questmobile.com.cn](https://data.questmobile.com.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `data.questmobile.com.cn`; title “QuestMobile TRUTH-标准数据库”.

**Confirm:** GET the TRUTH database portal; the metrics catalog is described publicly.

| Tool | Query |
|------|-------|
| Google | `site:data.questmobile.com.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="data.questmobile.com.cn"` |


## Baidu Index (`baiduindex`) {#baiduindex}

Vendor-operated single-tenant SaaS. Site: [index.baidu.com](https://index.baidu.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `index.baidu.com`; title “百度指数”; login wall for queries.

**Confirm:** GET the home; the indicator product is public though queries need a Baidu account.

| Tool | Query |
|------|-------|
| Google | `site:index.baidu.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="index.baidu.com"` |


## Ocean Engine TrendInsight (`oceaninsight`) {#oceaninsight}

Vendor-operated single-tenant SaaS. Site: [trendinsight.oceanengine.com](https://trendinsight.oceanengine.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `trendinsight.oceanengine.com`; 巨量算数 chrome; JS-rendered.

**Confirm:** GET the home; trend indicator tools are public.

| Tool | Query |
|------|-------|
| Google | `site:trendinsight.oceanengine.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="trendinsight.oceanengine.com"` |


## GSData (`gsdata`) {#gsdata}

Vendor-operated single-tenant SaaS. Site: [gsdata.cn](https://www.gsdata.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.gsdata.cn`; 清博智能 chrome.

**Confirm:** GET the platform home; ranking/metrics products are described publicly.

| Tool | Query |
|------|-------|
| Google | `site:gsdata.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="gsdata.cn"` |


## NewRank (`newrank`) {#newrank}

Vendor-operated single-tenant SaaS. Site: [newrank.cn](https://www.newrank.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.newrank.cn`; title “新榜”.

**Confirm:** GET the platform home; public rankings are browsable.

| Tool | Query |
|------|-------|
| Google | `site:newrank.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="newrank.cn"` |


## Qimai (`qimai`) {#qimai}

Vendor-operated single-tenant SaaS. Site: [qimai.cn](https://www.qimai.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.qimai.cn`; title “七麦数据”.

**Confirm:** GET the platform home; app ranking pages are public.

| Tool | Query |
|------|-------|
| Google | `site:qimai.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="qimai.cn"` |


## Diandian (`diandian`) {#diandian}

Vendor-operated single-tenant SaaS. Site: [diandian.com](https://www.diandian.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.diandian.com`; title “点点数据”.

**Confirm:** GET the platform home; app ranking pages are public.

| Tool | Query |
|------|-------|
| Google | `site:diandian.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="diandian.com"` |


## Chanmama (`chanmama`) {#chanmama}

Vendor-operated single-tenant SaaS. Site: [chanmama.com](https://www.chanmama.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.chanmama.com`; 蝉妈妈 chrome.

**Confirm:** GET the platform home; e-commerce metric products are described publicly.

| Tool | Query |
|------|-------|
| Google | `site:chanmama.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="chanmama.com"` |


## Feigua (`feigua`) {#feigua}

Vendor-operated single-tenant SaaS. Site: [feigua.cn](https://www.feigua.cn). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.feigua.cn`; title “飞瓜数据”.

**Confirm:** GET the platform home; short-video metric products are described publicly.

| Tool | Query |
|------|-------|
| Google | `site:feigua.cn (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="feigua.cn"` |


## Sunsirs (100ppi) (`sunsirs`) {#sunsirs}

Vendor-operated single-tenant SaaS. Site: [100ppi.com](https://www.100ppi.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.100ppi.com`; 生意社 chrome; commodity index navigation.

**Confirm:** GET the portal home; commodity price indices are public.

| Tool | Query |
|------|-------|
| Google | `site:100ppi.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="100ppi.com"` |


## Mysteel (`mysteel`) {#mysteel}

Vendor-operated single-tenant SaaS. Site: [mysteel.com](https://www.mysteel.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.mysteel.com`; title “我的钢铁网” (GBK encoding).

**Confirm:** GET the portal home; steel price indicator navigation is public though most series need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:mysteel.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="mysteel.com"` |


## SCI99 (`sci99`) {#sci99}

Vendor-operated single-tenant SaaS. Site: [sci99.com](https://www.sci99.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.sci99.com`; title “卓创资讯”.

**Confirm:** GET the portal home; commodity price navigation is public though most series need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:sci99.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="sci99.com"` |


## Oilchem (`oilchem`) {#oilchem}

Vendor-operated single-tenant SaaS. Site: [oilchem.net](https://www.oilchem.net). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.oilchem.net`; title “隆众资讯” (GBK encoding).

**Confirm:** GET the portal home; energy/chemical price navigation is public though most series need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:oilchem.net (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="oilchem.net"` |


## Jinlianchuang (315i) (`jinlianchuang`) {#jinlianchuang}

Vendor-operated single-tenant SaaS. Site: [315i.com](https://www.315i.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.315i.com`; 金联创 chrome; short JS landing page.

**Confirm:** GET the portal home; commodity price products are described publicly.

| Tool | Query |
|------|-------|
| Google | `site:315i.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="315i.com"` |


## Baiinfo (`baiinfo`) {#baiinfo}

Vendor-operated single-tenant SaaS. Site: [baiinfo.com](https://www.baiinfo.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.baiinfo.com`; title “百川盈孚”.

**Confirm:** GET the portal home; commodity market data navigation is public though most series need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:baiinfo.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="baiinfo.com"` |


## Sxcoal (`sxcoal`) {#sxcoal}

Vendor-operated single-tenant SaaS. Site: [sxcoal.com](https://www.sxcoal.com). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `www.sxcoal.com`; title “煤炭资源网”.

**Confirm:** GET the portal home; coal price navigation is public though most series need a subscription.

| Tool | Query |
|------|-------|
| Google | `site:sxcoal.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="sxcoal.com"` |


## China Data Online (`chinadataonline`) {#chinadataonline}

Vendor-operated single-tenant SaaS. Site: [china-data-online.com](https://china-data-online.com) (moved from `chinadatacenter.umich.edu`). The vendor instance is the only catalog — no third-party deployments to hunt; discovery is complete once the vendor instance is registered.

**Signals:** host `china-data-online.com` (legacy `chinadatacenter.umich.edu`); “China Data Online” / “All China Data Center” chrome; note `china-data-online.org` is a squatted domain — do not use it.

**Confirm:** GET the current host; connection may fail from some networks — verify from a US-reachable network.

| Tool | Query |
|------|-------|
| Google | `site:china-data-online.com (数据 OR 指标 OR 数据库)` |
| FOFA | `domain="china-data-online.com" \|\| domain="chinadatacenter.umich.edu"` |

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
