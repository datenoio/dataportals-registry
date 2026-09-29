# Discovering indicators and microdata catalogs

How to find **indicators catalogs** (`catalog_type: Indicators catalog`) and **microdata catalogs** (`catalog_type: Microdata catalog`). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md).

Statistical offices, central banks, SDG reporting sites, and survey archives are the usual owners. Search the agency name plus the local word for “statistics” / “indicators” / “microdata”, then confirm the platform. High-count stacks with their own recipes: PxWeb, PxStat, DGBAS Web, OpenSDG, SDG Index, Goal Tracker, IMF NSDP, .Stat Suite, .Stat Technology, Istat Data Browser, Swing, Knoema (portal homes only), SDMX-RI, GENESIS-Online, IBIS-PH, DHIS2, Envista Web, FENIX / CountrySTAT, TabNet, SparkMap, eDatos, Cancer-Rates.info, Conduent HCI, Virtual LMI, TerriSTORY, IHK-Fachkräftemonitor, DUVA, Géoclip, InstantAtlas, MATS, DataWarehousePro, Beyond 20/20, NADA, NESSTAR, REDATAM, Colectica, OBiBa Mica, IPUMS, KOSIS, SOPORTAL, e-Stat, SIDRA, Fingertips, UNdata, UN Comtrade Plus, Our World in Data. Related PC-Axis stack: PxStat (CSO Ireland; not PxWeb).

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

**False positives:** local-government `/DgbasWeb/` (`dgbasweb`); PxWeb `statdb.dgbas.gov.tw/pxweb` and Taipei public-works PxWeb `pwbstat.taipei.gov.tw/pxweb2007p/` (the dialog only links out to WebMain); MOTC `/motc/Portal/`; MOENV `/epanet/`; MOA `moasdweb`; tourism `stat.taiwan.net.tw`; gender.ey.gov.tw GECdb. The same `webMain.aspx` engine also serves non-catalog apps: Executive Yuan interpellation case systems (`inquery.ey.gov.tw`, `query.ey.gov.tw`), MOTC trucking-survey filing (`survey.motc.gov.tw`), and the freight-insurance login (`statap.motc.gov.tw`). CMS homepages that only link a WebMain tree (household offices, `www.mol.gov.tw`, `dbas.gov.taipei`, `statistics.health.gov.tw`) are not separate catalogs. `home.gotac168.com` is the vendor site.

Checked 24 September 2026. FOFA often indexes a one-line `location.replace("…/webMain.aspx")` that does not contain `funid`, so `body="webMain.aspx" && body="funid"` (59 hosts) misses those shells and also matches Taiwantrade, university personnel offices, and unrelated pages. `body="webMain.aspx"` alone is 144 and includes ASP.NET pages outside Taiwan. Scope with `host=".gov.tw"` (23 hosts) or `host=".gov.tw" || host=".gov.taipei"` (29). The vendor HTML comment is tighter: `body="系統開發:金諄"` is 7 hosts, `body="webMain.aspx" && body="金諄"` is 11, and `body="2759-6506"` is 9 (that phone number also hits `home.gotac168.com`). `body="統計資料動態查詢"`, `body="webtemp/usr"`, `body="usrdgbasJS"`, and `body="kendo.common.mintmp"` are 0 because those strings sit in frames or stylesheets FOFA does not index. `title="共通性查詢"` is 1. `host="dgbas.gov.tw"` is 157 and is mostly DGBAS Web. FOFA did not return the live MOI, MOF `njswww`, MOE `edust`, or Taipei TSIS tenants. `census.dgbas.gov.tw` and `dtable.dgbas.gov.tw` (三大普查) match the `.gov.tw` query, but a live GET stops at Cloudflare 403.

| Tool | Query |
|------|-------|
| Google | `inurl:webMain.aspx (funid OR "統計資料動態查詢") site:.gov.tw` |
| Google | `"統計資料動態查詢" OR "共通性查詢" (webMain OR funid) site:.gov.tw` |
| Censys | `web.endpoints.http.body: "webMain.aspx"` |
| FOFA | `body="webMain.aspx" && host=".gov.tw"` |
| FOFA | `body="webMain.aspx" && (host=".gov.tw" \|\| host=".gov.taipei")` |
| FOFA | `body="系統開發:金諄"` |
| FOFA | `body="webMain.aspx" && body="金諄"` |
| FOFA | `body="2759-6506" && host=".gov.tw"` |

## KOSIS (`kosis`) {#kosis}

Statistics Korea statistical table platform. Hub: [kosis.kr](https://kosis.kr). OpenAPI: [kosis.kr/openapi/](https://kosis.kr/openapi/). Agency and local tenants reuse `/statHtml/statHtml.do`. ODA clones include MMSIS, LAOSIS, and ASIS.

**Signals:** path `/statHtml/statHtml.do`; title “KOSIS” / “국가통계포털” / “통계표조회”; `kosisTitle.gif` / `dbsearchTitle.gif`; current skin `/ext/newKosis/css/main.css`; agency 통계포털 shell `vw_cd=MT_DTITLE` / `TblInfoListResult.html`; older ODA JSP tree `statDbList.jsp` / `fileDb.jsp`; NSIST hosting on `stat.kosis.kr` (`statHtml_host/statHtml.do`).

**Confirm:** GET a public table tree or a live `/statHtml/statHtml.do?orgId=&tblId=` table that returns a named statistical table. One catalog per public tenant. The `/bukhan/` tree is already a separate registered catalog. Keep a host only when that table is served on the host. City pages that only deep-link `stat.kosis.kr/statHtml_host` are link-outs.

**False positives:** local-government `/stat/index.do` CMS skins that only link out to KOSIS (Paju `stat.paju.go.kr` is this case); 지표누리 (`index.go.kr`); SGIS; SOPORTAL (`indexPage.do` with `/soportal/` stylesheets); English/mobile/SSO aliases of `kosis.kr` (`edu`, `sso`, `mgmk`); `stat.kosis.kr/nsistN` agency hosting console; IP-only COLSIS hits; `body="dbsearchTitle"` without `.gif` (library guides). LankaSIS (`sis.statistics.gov.lk`) matches `statDbList.jsp` but did not answer on GET in September 2026.

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

## SOPORTAL (`soportal`) {#soportal}

Wiseitech agency statistical-table portal. Vendor: [wise.co.kr](https://www.wise.co.kr/). Live tenants: [stat.mcee.go.kr](https://stat.mcee.go.kr/portal/main/indexPage.do), [houstat.hf.go.kr](https://houstat.hf.go.kr/research/portal/main/indexPage.do), [reb.or.kr/r-one](https://www.reb.or.kr/r-one/portal/main/indexPage.do).

**Signals:** `indexPage.do` together with `/soportal/` stylesheets (`/css/{skin}/soportal/`) and `/js/portal/lib/`; table browsers `easyStatPage.do`, `orgStatPage.do`, or `nameStatPage.do`; OpenAPI routes `openApiActKeyPage.do` and `openApiIntroPage.do`. The application is mounted under a context path (`/portal/`, `/research/portal/`, `/r-one/portal/`).

**Confirm:** GET the public `indexPage.do` and check for a `soportal` stylesheet or a `/portal/stat/easyStatPage.do` link. One catalog per agency host.

**False positives:** `commonness.js` or `COPYRIGHT (C) 2013 WISEITECH` alone (Gyeonggi Data Dream `data.gg.go.kr` and Open National Assembly `open.assembly.go.kr` use `mainPage.do`); IBSheet on MOLIT 통계누리, 문화셈터, or K-stat; KOSIS `/statHtml/statHtml.do`; 지표누리; SGIS.

| Tool | Query |
|------|-------|
| Google | `inurl:easyStatPage.do (통계 OR statistics)` |
| Google | `inurl:openApiActKeyPage.do` |
| Censys | `web.endpoints.http.body: "soportal"` |
| FOFA | `body="soportal" && body="indexPage.do"` |
| FOFA | `body="easyStatPage.do"` |
| FOFA | `body="openApiActKeyPage.do"` |

## e-Stat (`estat`) {#estat}

Japan portal site for official statistics (政府統計の総合窓口). Hub: [e-stat.go.jp](https://www.e-stat.go.jp). API: [e-Stat API](https://www.e-stat.go.jp/en/api/).

**Signals:** host `e-stat.go.jp`; title “政府統計の総合窓口”; Statistical LOD on `data.e-stat.go.jp`; Statistics Dashboard on `dashboard.e-stat.go.jp`.

**Confirm:** GET the public table portal, LOD home, or dashboard. The three hosts are already registered as distinct catalogs — do **not** add extra table/API paths. Skip RESAS and ministry pages that only link to e-Stat.

| Tool | Query |
|------|-------|
| Google | `site:e-stat.go.jp (統計 OR "official statistics")` |
| Censys | `web.names: "e-stat.go.jp"` |
| FOFA | `domain="e-stat.go.jp"` |

## IDDS (`idds`) {#idds}

Hong Kong Census and Statistics Department Interactive Data Dissemination Service. Each themed tenant runs on its own host: Common-IDDS ([idds.censtatd.gov.hk](https://idds.censtatd.gov.hk/)), Trade IDDS ([tradeidds.censtatd.gov.hk](https://tradeidds.censtatd.gov.hk/)) with a JSON GET API (spec at `/PageID/ApiSpec`), and census-round tenants such as the 2021 Population Census IDDS ([idds.census2021.gov.hk](https://idds.census2021.gov.hk/app/idds.html)).

**Signals:** hostname `idds.{org}.gov.hk` or `{theme}idds.censtatd.gov.hk`; title “Interactive Data Dissemination Service” or “Common-IDDS”; ASP.NET MVC bundles `/Content/bundles/js` plus DevExpress `DXR.axd` on the trade tenant; jQuery-i18n app at `/app/idds.html` on census tenants.

**Confirm:** GET the portal home and match the IDDS custom-table builder UI. One catalog per themed tenant host — the three hosts above are already registered; do not add per-table or per-theme URLs on the same host. C&SD pages that only link to an IDDS host are link-outs.

| Tool | Query |
|------|-------|
| Google | `"Interactive Data Dissemination Service" site:gov.hk` |
| Google | `inurl:idds site:censtatd.gov.hk` |
| Censys | `web.names: "censtatd.gov.hk"` |
| FOFA | `title="Interactive Data Dissemination Service"` |
| FOFA | `body="/PageID/ApiSpec"` |

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

## Klimadashboard Münster (`klimadashboardmuenster`) {#klimadashboardmuenster}

Municipal climate and local-indicator dashboard first built by the City of Münster and adapted by other cities. Source: [Open CoDE](https://gitlab.opencode.de/smart-city-muenster/klimadashboard-muenster/klimadashboard-muenster). Live copies include [klimadashboard.ms](https://www.klimadashboard.ms/) and Aschaffenburg’s Smart Data Dashboard.

**Signals:** credit to `klimadashboard.ms` or `klimadashboard-muenster`; Reedu GmbH in the AGPL notice; Next.js app shell.

**Confirm:** GET the city dashboard and match a Münster/Open CoDE credit. One record per municipal host. Do **not** set `klimadashboardmuenster` on [klimadashboard.de](https://klimadashboard.de/) (Klimadashboard Deutschland, a different product).

| Tool | Query |
|------|-------|
| Google | `"klimadashboard.ms" OR "klimadashboard-muenster" (Dashboard OR Klima)` |
| Google | `"adaptiert von" Klimadashboard Münster` |
| Censys | `web.endpoints.http.body: "klimadashboard-muenster"` |
| FOFA | `body="klimadashboard-muenster"` |
| FOFA | `body="klimadashboard.ms" && body="AGPL"` |

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

## Fusion Data Browser (`fusiondatabrowser`) {#fusiondatabrowser}

Metadata Technology SDMX dissemination UI. Docs: [Fusion Data Browser](https://wiki.sdmxcloud.org/Fusion_Data_Browser). Live example: [Bank of Israel](https://edge.boi.gov.il/FusionDataBrowser/) (title `Fusion Data Browser`, assets `dist/assets/css/all.min.css`). The UI reads Fusion Edge Server or Fusion Registry at `/FusionEdgeServer/ws/public/sdmxapi/rest` and `/FusionEdgeServer/sdmx/v2/`.

**Signals:** HTML title `Fusion Data Browser`; path `/FusionDataBrowser/`; stylesheet `dist/assets/css/all.min.css`; sibling API `/FusionEdgeServer/ws/public/sdmxapi/rest/dataflow`.

**Confirm:** GET `/FusionDataBrowser/` and check the title, then GET the dataflow list. One record per public browser, not per dataflow. A structural registry at `/FusionRegistry` with no Data Browser UI stays `fusionregistry`.

| Tool | Query |
|------|-------|
| Google | `inurl:FusionDataBrowser "Fusion Data Browser"` |
| Google | `inurl:FusionEdgeServer SDMX` |
| Censys | `web.endpoints.http.html_title: "Fusion Data Browser"` |
| FOFA | `title="Fusion Data Browser"` |
| FOFA | `body="FusionEdgeServer"` |

## Swing (`swing`) {#swing}

ABF Research statistical databank (Swing Viewer / Swing Jive / Swing Mosaic / Ballroom). Vendor: [swingsoftware.eu](https://swingsoftware.eu/). Flemish public tenants live at `{city}.incijfers.be` and `provincies.incijfers.be`. Dutch municipal tenants use `{city}.incijfers.nl`, with older neighbourhood monitors on `*.buurtmonitor.nl` and some thematic databanks on `*.databank.nl` or a custom domain.

**Signals:** hostname `*.incijfers.be`, `*.incijfers.nl`, or `*.buurtmonitor.nl`; Ballroom shell `/script/ballroom.js`; Mosaic footer link `swingsoftware.eu/modules/swing-mosaic`; chart assets `cdn.abf.nl/abfcharts`; `SwingLogoutButton`.

The Mosaic footer is `Powered by <a …>Swing Mosaic</a>`, so the words are not adjacent in the HTML. A live Alkmaar page writes `ABF_Model.JiveTimestamps` and `ABF_Model.Settings` in an inline script; FOFA does not index those dotted identifiers.

**FOFA** (checked September 2026):

| Query | Rows | Use |
|-------|------|-----|
| `body="swingsoftware.eu/modules/swing-mosaic"` | 295 (92 hosts) | Mosaic dashboards, including custom domains |
| `body="SwingLogoutButton"` | 301 | Same dashboard shell |
| `body="cdn.abf.nl/abfcharts"` | 307 | Chart bundle; overlaps the Mosaic footer |
| `body="/script/ballroom.js"` | 80 | Ballroom shell. Catches custom domains the footer query misses (`brabantscan.nl`, `datawonen.nl`, `findo.nl`, `*.inzicht.nl`) |
| `body="keepalive_ballroom.js"` | 80 | Same Ballroom set |
| `body="ballroomstatic.ashx"` | 73 | Same Ballroom set |
| `domain="incijfers.nl"` | 582 (328 hosts) | Municipal zone. Most rows are wildcard DNS (`mail.`, `*-plus`, `test.`, random labels) titled “Document Moved” |
| `domain="incijfers.be"` | 44 | Flemish zone. Smaller than the registry: many live `.be` tenants are not in the FOFA crawl |
| `domain="buurtmonitor.nl"` | 18 | Older neighbourhood-monitor hostnames. Some now redirect to `*.incijfers.nl` |
| `domain="databank.nl"` | 45 | Mostly hosting backends (`test.`, `admin.`, `cname.`). Keep a row only when the title is a databank |
| `body="Powered by Swing"` | 28 | Weak. Misses the split Mosaic footer and matches unrelated “swing” sites |
| `body="ABF_Model.Settings"` | 0 | Dotted script identifiers are not in the FOFA index |
| `body="ABF_Model.JiveTimestamps"` | 0 | Same |
| `body="/Jive"` | ~60,000 | Path token, not a fingerprint |
| `domain="inzahlen.be"` | 0 | `ostbelgien.inzahlen.be` is not in this domain index |

Do not register the vendor template (`incijfers.nl`, `incijfers.be`, `ginc-abf.incijfers.nl`, `demo.swingsoftware.eu`), `AvailableDomains.aspx` pickers, `*-plus` / `beta` / `test` labels, or a short alias of a tenant already registered (`vls.incijfers.nl` is Velsen, `lv.incijfers.nl` is Leidschendam-Voorburg, `zp.incijfers.nl` is Zutphen).

**Confirm:** GET the public databank or Mosaic dashboard (not `/Admin/Studio/`, not a login-only `/login.aspx?returnurl=/home`). One record per municipal, provincial, or named thematic tenant. A second hostname that redirects to a registered catalog is the same record. Dutch “in cijfers” / waarstaatjegemeente sites on other hosts are the same product when Swing-branded.

| Tool | Query |
|------|-------|
| Google | `site:incijfers.be` |
| Google | `site:incijfers.nl` |
| Google | `"Powered by Swing" OR "Swing Mosaic" OR "Swing Viewer" (incijfers OR databank)` |
| Censys | `web.names: "incijfers.be"` |
| Censys | `web.names: "incijfers.nl"` |
| FOFA | `body="/script/ballroom.js"` |
| FOFA | `body="swingsoftware.eu/modules/swing-mosaic"` |
| FOFA | `body="cdn.abf.nl/abfcharts"` |
| FOFA | `domain="incijfers.nl"` |
| FOFA | `domain="incijfers.be"` |
| FOFA | `domain="buurtmonitor.nl"` |
| crt.sh | `%.incijfers.be` |
| crt.sh | `%.incijfers.nl` |

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

## Idescat (`idescat`) {#idescat}

Statistical Institute of Catalonia dissemination platform. Hub: [idescat.cat](https://www.idescat.cat). Public REST APIs on `api.idescat.cat` return JSON / JSON-stat (`/emex/v1/`, `/taules/v2`).

**Signals:** host `idescat.cat` or `api.idescat.cat`; paths `/estad/`, `/emex/`, `/dades/ods/`; chrome "Idescat".

**Confirm:** GET `https://api.idescat.cat/emex/v1/nodes.json?lang=en` (200 JSON) or the `/estad/` operations list. One catalog per product family (statistical tables, Emex municipal profiles, ODS indicators), not per table. The Idescat CMS home is not a separate catalog.

| Tool | Query |
|------|-------|
| Google | `site:idescat.cat (estad OR emex OR indicadors)` |
| Google | `site:api.idescat.cat` |
| Censys | `web.names: "idescat.cat"` |
| FOFA | `domain="idescat.cat"` |

## INEbase (`inebase`) {#inebase}

Spain's National Statistics Institute (INE) dissemination platform. Hub: [ine.es/dyngs/INEbase](https://www.ine.es/dyngs/INEbase/es/listaoperaciones.htm). jaxiT3 table browser plus the Tempus3 JSON REST API on `servicios.ine.es/wstempus/`.

**Signals:** paths `/dyngs/INEbase/`, `/dyngs/ODS/`, `/jaxiT3/`; host `servicios.ine.es/wstempus/`; chrome "INEbase".

**Confirm:** GET `https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES` (200 JSON) or the INEbase operations list. One catalog per product (INEbase operations, Agenda 2030 ODS, microdata), not per statistical operation. The IMF NSDP page is `imfnsdp`.

| Tool | Query |
|------|-------|
| Google | `site:ine.es/dyngs INEbase` |
| Google | `inurl:/jaxiT3/ ine.es` |
| Censys | `web.names: "ine.es"` |
| FOFA | `domain="ine.es"` |

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

**Signals:** host `*.virtuallmi.com`; path `/vosnet/` on the LMI UI itself; “Virtual LMI”.

**Confirm:** GET the public LMI home or `/vosnet/Default.aspx`. One catalog per state tenant. Branded custom domains count when `/vosnet/` is the UI (Colorado LMI Gateway). Do not retag QualityInfo, WisConomy, `/analyzer` ALMIS, or other LMI sites without those fingerprints.

Checked 24 September 2026. `domain="virtuallmi.com"` and `cert="virtuallmi.com"` are unindexed, so a hostname FOFA query misses the tenants. `body="Virtual LMI"` is the vendor site only. `body="vosnet"` (590 hosts) and `body="/vosnet/Default.aspx"` (458) are pages that link Virtual OneStop job boards, not LMI dataset UIs. `body="vosnet" && body="QCEW"` hits CMS sites that link out (Nevada LMI, Alabama Labor). Use `crt.sh` `%.virtuallmi.com`, then GET the public LMI home. Imperva blocks many neighboring job-board hosts.

| Tool | Query |
|------|-------|
| Google | `site:virtuallmi.com OR inurl:/vosnet "labor market"` |
| Google | `"Virtual LMI" (QCEW OR LAUS OR workforce)` |
| Censys | `web.names: "virtuallmi.com"` |
| crt.sh | `%.virtuallmi.com` |

## Cascade CMS (`cascadecms`) {#cascadecms}

Hannon Hill Cascade CMS, a general web CMS that several US state labor-market information portals publish through. Vendor: [hannonhill.com/products/cascade-cms](https://www.hannonhill.com/products/cascade-cms/index.html).

**Signals:** HTML comments with Cascade template regions such as `<system-region name="CAROUSEL"/>`; state LMI tenants share a `_files/css` + `_files/js` asset layout (`scripts.js`, `news-gallery.js`, `random-background.js`, sometimes `lmi.js`) with jQuery 3.5.1 and Bootstrap 4.5.2 from stackpath; Google CSE search.

**Confirm:** GET the LMI home and look for `system-region` comments or the `_files/` asset layout. One catalog per state LMI portal. Do not retag sites that merely link Cascade-hosted pages, Oregon's QualityInfo (custom), or Virtual LMI `/vosnet/` tenants.

| Tool | Query |
|------|-------|
| Google | `"_files/js/lmi.js" OR "_files/js/news-gallery.js" labor market` |
| Censys | `web.endpoints.http.body: "system-region"` |
| FOFA | `body="system-region" && body="labor market"` |

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

**Signals:** `window.GCO5` (current Air bootstrap); `GC_loadCss.php?output=user` (stylesheet on most Air shells); hash routes `#c=indicator` / `#c=home`; shared meta “Explorez et visualisez sous forme de cartes, graphiques et tableaux interactifs”. Older chrome (`Logo geoclip`, class `gc_logo`, path `/geoclipair/`) is rare on live Air HTML.

**Confirm:** GET the public observatory (not login/admin) and match `window.GCO5` or `GC_loadCss.php`. One catalog per observatory / tenant, not each indicator or each commune report. Skip `geoclip.fr` marketing, `*-decouverte` and other vendor vitrines, `preprod` / `gcpreprod` hosts, and a second hostname of an observatory already registered.

**False positives:** Articque Platform / Cartes & Données; ANCT Observatoire des territoires `/donnees_ouvertes` Drupal catalog (keep `custom`); OCSTAT `statistique.ge.ch/` CMS home (the atlas is `/atlas/`); INSEE `insee.fr` search pages that mention GeoClip; French energy observatories (OPTEER, CIGALE, TrACE) that are not Géoclip; TerritoireAngular (`reperes-paysdelaloire.fr`); the GeoCLIP image-geolocation model (`geoclip.xyz` and research homepages); PopGIS3 (`*.popgis.spc.int`) which loads `GC_loadCss.php` but is already `popgis`.

**FOFA** (checked 24 September 2026). There is no `app="Geoclip"`. `body="GC_loadCss.php"` and `body="GC_loadCss.php?output=user"` are the same 192 hosts. `body="window.GCO5"` is 222 and is the query that still hits Air shells whose indexed HTML has no `GC_loadCss.php` (31 extra hosts, including `demographie.medecin.fr`, `statrhena.statabs.ch`, and `mapadasaude.saude.go.gov.br`). `body="GCO5"` alone is 449 and too broad. `body="Explorez et visualisez sous forme de cartes, graphiques et tableaux interactifs"` is 145 and only the French default meta; every hit is already inside the two shell queries.

Do **not** hunt with `body="geoclip"` or `body="/geoclip/"` (82 each): they miss most Air shells and match the GeoCLIP model, vendor marketing, and unrelated pages. `body="gc_logo"` is 1,742 and is not this product. `body="geoclipair"` and `body="/geoclipair/"` return 1. `body="Geoclip Air"`, `title="Geoclip Air"`, `cert="geoclip"`, `header="geoclip"`, and `js_name="GC_loadCss.php"` return 0 — tenants replace the title, and FOFA does not index that phrase from the script block. `title="Geoclip"` is 5 and `title="Géoclip"` is 3. `host="geoclip"` (49) includes `geoclip.xyz`, `geoclip.ru`, `geoclip.com.mx`, and S3 buckets. `domain="geoclip.fr"` (21) is the vendor: `www.geoclip.fr`, découverte demos, and homemade vitrines (Observatoire des Votes, télécoms). `body="Logo geoclip"` is 2.

The same observatory is often indexed on port 80 and 443, on `www`, and as a bare IP. Deduplicate by hostname. `statatlas.bfs.admin.ch` is the same catalog as `www.mapexplorer.bfs.admin.ch`. `atlasau.mitma.gob.es` is the same atlas as `atlasau.mivau.gob.es`. `geoclip.aua-toulouse.org` and `gcpreprod.aua-toulouse.org` are the registered Portail Carto.

| Tool | Query |
|------|-------|
| Google | `inurl:GC_loadCss.php OR inurl:/geoclipair/` |
| Google | `"Géoclip" (observatoire OR atlas OR "statistiques locales")` |
| Censys | `web.endpoints.http.body: "GC_loadCss.php"` |
| Censys | `web.endpoints.http.body: "window.GCO5"` |
| FOFA | `body="GC_loadCss.php"` |
| FOFA | `body="window.GCO5"` |
| FOFA | `body="GC_loadCss.php" \|\| body="window.GCO5"` |

## GINES (`gines`) {#gines}

Hosted Swiss indicator and spatial-monitoring platform from GINES GmbH. Product: [gines.ch](https://www.gines.ch/). The public Canton of Bern statistical atlas embeds [bern.gines.ch](https://bern.gines.ch/). Vendor references also name Aargau, Graubünden, Schaffhausen, Solothurn, and Uri. Distinct from Géoclip (`geoclip`) cantonal atlases.

**Signals:** hostname `*.gines.ch`; title `GINES`; login shell that names GINES; Bern atlas pages that embed `bern.gines.ch`.

**Confirm:** GET a public atlas that loads GINES without a login wall. Register that public atlas, not each indicator. Skip login-only cantonal tenants and the product sites `gines.ch` and `gines.biz`.

| Tool | Query |
|------|-------|
| Google | `"GINES" (Raumbeobachtung OR Statistik OR Atlas) site:.ch` |
| Google | `inurl:gines.ch` |
| Censys | `web.endpoints.http.body: "GINES"` |
| FOFA | `host="gines.ch"` |

## InstantAtlas (`instantatlas`) {#instantatlas}

Esri UK geostatistical HTML reports and Dashboard Builder. Help: [help.instantatlas.com](https://help.instantatlas.com/). Distinct from Esri UK Data Observatory (`esridataobservatory`).

**Signals:** title “InstantAtlas™ Bericht” / “Rapport InstantAtlas™”; `ia-min.js` or `ia-max.js`; `iaInitReport()`; footer “Powered By InstantAtlas™”; path `/imagemap/instantatlas/` or `atlas.html` report; `dashboards.instantatlas.com/viewer/report?appid=`.

**Confirm:** GET the public atlas/report (not a CMS homepage that only links to one chart). One catalog per public atlas, not each indicator or each year of the same atlas. Skip `instantatlas.com` marketing and Dashboard Builder authoring. `structuraldataatlas.urbanaudit.de` is the English host of the registered Urban Audit Strukturdatenatlas.

**False positives:** Esri UK Data Observatory WordPress (`/wp-content/themes/ia-theme/` without an InstantAtlas report as the catalog — those are `esridataobservatory`); Report Builder for ArcGIS; a GBE table tree that only mentions InstantAtlas Kreis maps as extras (Sachsen-Anhalt GBE-net); Urban Audit hosts that are DUVA Informationsportale.

**FOFA** (checked 25 September 2026). There is no `app="InstantAtlas"`. The noscript line is `This <a …>InstantAtlas™</a> report requires JavaScript`, so `body="This InstantAtlas"` is 0. The footer text is adjacent: `body="Powered By InstantAtlas"` is 22 rows (FOFA `body` is case-insensitive, so `body="powered by InstantAtlas"` is the same 22). `body="ia-min.js"` is 21 and misses the HTML5 shell that loads `ia-max.js` (1 row, bare IP `194.24.230.194`, Herne HiTS). Together, `body="Powered By InstantAtlas" || body="ia-min.js"` is 24 rows and 11 hostnames. That union is the hunt query: it is the only one that still includes both the self-hosted reports and the older ECDC ASP.NET atlas (`atlas.ecdc.europa.eu`, footer only, no `ia-min.js`).

`body="iaInitReport"`, `body="atlas-unsupported.html"`, and `body="ia.supportsCanvas"` are 20 rows / 9 hostnames, the same self-hosted shells, and they miss ECDC. `js_name="ia-min.js"` is 15, a subset; `js_name="ia-max.js"` is 0. `body="ia-report-container"` is 23 and also matches unrelated dashboards (TaoSageVision, ScorePulse). `body="wurde mit InstantAtlas"` and `body="mit InstantAtlas"` are 8, the German meta, already inside the footer query. `body="erstellt mit InstantAtlas"` and `body="basé sur InstantAtlas"` are 0 because the trademark and word order split those phrases. `body="report requires JavaScript"` is 34 and wider than this product. `body="Geowise Ltd"` is 20 and the same reports. `body="GeoWise"` is 111.

`title="InstantAtlas"` is 14 and mixes report shells with Dashboard Builder and Data Observatory titles (`www.durhaminsight.info`). `body="InstantAtlas"` is 49 and is a mention search (training pages, `doctoral.co.jp`, Data Observatory homes). `body="/imagemap/instantatlas/"` is 0. `domain="instantatlas.com"` is 20 and is the vendor (help, hub, dashboards, reports, online, cdn). `host="instantatlas"` is 27 and adds `instantatlas.statistik-berlin-brandenburg.de:8885`, which did not answer on HTTPS. `cert="instantatlas.com"` is 1 (`www2.instantatlas.com`, a 301). `body="dashboards.instantatlas.com/viewer/report"` is 5 and is pages that link a hosted dashboard (Gesundheitsatlas BW, EHINZ), not separate installs.

Do **not** hunt with `body="ia-theme"` (1,725; the Data Observatory WordPress theme), `title="Dashboard Builder"` (519), `title="Statistikatlas"` (5; NRW and Westfalen-Lippe map apps with no InstantAtlas shell), `body="Ce rapport"`, or `body="Dieser Bericht"`.

FOFA indexes the report when that HTML is the page it crawled. Deep `atlas.html` paths on a municipal CMS (Dresden, Kassel, Braunschweig, Heidelberg, Gloucestershire, Statistikamt Nord Kreismonitor and Hamburger Stadtteilprofile) are absent. Deduplicate port 80/443 and `www`. `www.statistik.wuerzburg.de` is a stale hit: live HTTPS redirects to the registered OpenDataSoft Statistikatlas. The Herne HiTS shell on `194.24.230.194` has no hostname; the public portal is the Shiny app at `hits.herne.de/portal/`.

| Tool | Query |
|------|-------|
| Google | `intitle:"InstantAtlas" (Bericht OR Rapport OR report)` |
| Google | `"ia-min.js" OR "ia-max.js" OR "Powered By InstantAtlas"` |
| Censys | `web.endpoints.http.html_title: "InstantAtlas"` |
| Censys | `web.endpoints.http.body: "Powered By InstantAtlas"` |
| FOFA | `body="Powered By InstantAtlas" \|\| body="ia-min.js"` |
| FOFA | `body="iaInitReport"` |
| FOFA | `body="ia-max.js"` |

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

**Signals:** path `/jaxi/Tabla.htm`, `/jaxi/Datos.htm`, `/jaxiT3/Tabla.htm`, `/jaxiPx/Tabla.htm`; Struts `menu.do` / `tabla.do` on `iaeaxi` or `*-jaxi` apps; `./css/jaxi.css` and `./js/jaxi.js`; `theme/custom_jaxi_css/` or `bundles/customjaxi.js`; table HTML `var pathJaxi` and `/menus/plantillas/jaxiT3/js/jaxi.js` (jaxiPx uses `var pathJaxi = "/jaxiPx/"`); Magnolia shell `portalEstadisticoPlantilla` with `datos.html?type=jaxi` embedding `dynPx/inebase` and `jaxiPx/Tabla.htm`.

**Confirm:** GET the public table-browser menu (not a CMS home that only links out) and match JAXI paths or chrome. One catalog per tenant. Bare `/iaeaxi/` may redirect to the institute CMS — use `menu.do`. IBESTAT needs `menu.do?nodeId=0` (`/ibestat-jaxi/` alone is a not-found page). A `portalEstadistico` home is JAXI when a public page embeds `jaxiPx` or `dynPx/inebase`, not when the title merely says “Portal Estadístico”.

**False positives:** INEbase operations CMS (`/dyngs/INEbase/`); ibestat.es institute portal; eDatos ODS tenants (`edatos`); PxWeb `/api/v1/`; PxStat; other CCAA `/jaxi/` guesses that 404.

Do **not** add a second INE catalog for a random `Tabla.htm` URL, and do **not** retag INEbase as `jaxi` — the registered INEbase home is the operations list, not the table UI.

Search the application HTML, not pages that only link to `www.ine.es/jaxiT3/Tabla.htm`. FOFA `body` is case-insensitive, so `jaxi.js` also matches an unrelated `jAxi.js`.

| Tool | Query |
|------|-------|
| Google | `inurl:/jaxi/Tabla.htm OR inurl:/jaxiT3/Tabla.htm site:.es` |
| Google | `"herramienta JAXI" OR IAEAxi OR inurl:ibestat-jaxi` |
| Censys | `web.endpoints.http.body: "var pathJaxi"` |
| Censys | `web.endpoints.http.body: "plantillas/jaxiT3/js/jaxi.js"` |
| Censys | `web.endpoints.http.body: "./css/jaxi.css"` |
| Censys | `web.endpoints.http.body: "theme/custom_jaxi_css"` |
| Censys | `web.endpoints.http.body: "portalEstadisticoPlantilla"` |
| FOFA | `body="var pathJaxi"` |
| FOFA | `body="plantillas/jaxiT3/js/jaxi.js"` |
| FOFA | `body="./css/jaxi.css"` |
| FOFA | `body="theme/custom_jaxi_css"` |
| FOFA | `body="portalEstadisticoPlantilla"` |
| FOFA | `body="datos.html?type=jaxi"` |

`body="var pathJaxi"` and `body="plantillas/jaxiT3/js/jaxi.js"` are the jaxiT3 / jaxiPx table page (served on the app host). `body="./css/jaxi.css"` is the ceded Struts UI (IAEAxi). `body="theme/custom_jaxi_css"` is the IBESTAT skin. `body="portalEstadisticoPlantilla"` and `body="datos.html?type=jaxi"` are the Magnolia shell that embeds jaxiPx (the crime-statistics portal). Prefer these over a bare product-name search.

**FOFA false positives (24 September 2026):** `body="jaxi.css"` and `body="css/jaxi.css"` returned 0 hosts. The live Aragón, IBESTAT, and INE table pages are not in that body index (`host="iaeaxi"`, `host="ibestat-jaxi"`, `host="jaxiT3"`, and `host="jaxiPx"` were also 0). `body="js/jaxi.js"` and `body="./js/jaxi.js"` match `assets/js/jAxi.js` on `analisi-rischi.vitanuova.it` (an insurance landing page). `body="jaxiT3"` (39 hosts) and `body="/jaxi/Tabla.htm"` (6) are pages that link to `www.ine.es/jaxiT3/Tabla.htm`. `body!="ine.es"` does not drop those `www.ine.es` links; `body="jaxiT3/Tabla.htm" && body!="www.ine.es"` returned 0. `body="jaxiPx"`, `body="JaxiPx"`, and `body="IAEAxi"` match Chinese spam. `title="JAXI"` (19) is a plumbing brand, a Japanese jobs site, and companies. `title="IAEAxi"` returned 0. `cert="jaxi"` is about 108 substring certificates; `cert="jaxi" && country="ES"` is 0. `body="dynPx"` is thousands of unrelated GraphQL Playground pages. `body="jaxi" && country="ES"` is 4 rows: the registered SES portal, plus GlobalSuite (the letters `jaxi` inside a base64 blob) and its IP. `title="Portal Estadístico" && country="ES"` also hits the Universidad de La Laguna statistics portal and the Notariado property-price portal, which do not serve JAXI. The only catalog host these queries returned is `estadisticasdecriminalidad.ses.mir.es`, already registered.

## iMonitoring (`imonitoring`) {#imonitoring}

NPO Krista public-finance and socio-economic indicator platform (KristaBI). Product: [npo.krista.ru/products/imonitoring](https://npo.krista.ru/products/imonitoring/). Comparative hub: [iminfin.ru](https://www.iminfin.ru/). Regional Open Budget tenants sit on `*.ifinmon.ru` or branded hosts.

**Signals:** host `*.ifinmon.ru` or `iminfin.ru`; title “Открытый бюджет …” / “iMonitoring”; path `/servisy/konstruktor-dannyx/` or `/konstruktor-dannykh`; `fm@krista.ru` / `fmsupport@krista.ru`; chrome “конструктор данных”.

**Confirm:** GET the public Open Budget home (not login/admin) and match Krista support, the data constructor, or an `ifinmon.ru` tenant. One catalog per regional portal. Do **not** add a catalog per subject listed on the iminfin.ru comparison tree — that is one hub.

**False positives:** other Russian open-budget CMS sites without Krista fingerprints (Leningrad Oblast `budget.lenobl.ru`, Moscow city `budget.mos.ru`). Zabaykalsky `budgetzab.75.ru` is Keysystems Open Budget (`ksopenbudget`). Krasnodar `openbudget23region.ru/otkrytye-dannye` is a Joomla open-data catalog. `ifinmon.ru` apex with an expired certificate is not a new tenant.

## KS Open Budget (`ksopenbudget`) {#ksopenbudget}

Keysystems public-finance portal «КС Открытый бюджет. Бюджет для граждан». Product: [keysystems.ru](https://www.keysystems.ru/products/Internet-solutions/ks-otkrtyy-byudzhet-byudzhet-dlya-grazhdan/). Regional portals use their own hosts, with per-region skins under `/Content/Skin*/`.

**Signals:** `/Scripts/Site.js` defining `EB` and `GZW`; `/Menu/Page/` and `/Show/Category/`; `/Content/BudgetCalculator/`; `jquery.ks.multichoicer.js`; title «Единый портал бюджетной системы».

**Confirm:** GET the public budget home and match those paths. One catalog per finance-portal host. An `/opendata/` register on the same host is the same product and may stay an open-data catalog. Do not tag iMonitoring (`*.ifinmon.ru`), `budget.lenobl.ru`, or `budget.mos.ru`.

| Tool | Query |
|------|-------|
| Google | `"Единый портал бюджетной системы" "Открытый бюджет"` |
| Censys | `web.endpoints.http.body: "jquery.ks.multichoicer.js"` |
| FOFA | `body="jquery.ks.multichoicer.js"` |
| FOFA | `body="/Content/BudgetCalculator/"` |

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

The classic catalog HTML loads `genesis-online.css` and `recherchehilfe.js` from the installation context (`/genesis/`, `/genesisonline/`, `/genonline/`, `/ldbnrw/`, `/bildung/`). The 2025 shell is a separate page at `/datenbank/online`: title `GENESIS-Online`, `class="gor-webapp"`, and assets `gor-webapp.*.js`. That page is the same catalog as the classic UI on the same host.

**Signals:** `genesis-online.css`; `recherchehilfe.js`; `gor-webapp`; paths `/genesis/online` and `/datenbank/online`.

**Confirm:** GET a page that serves the classic stylesheet or the `gor-webapp` shell and lists tables. One record per statistical-office installation (Bund vs Land vs a thematic database such as the census or the education monitor). Host aliases are the same catalog (`ldb.nrw.de`, `landesdatenbank.nrw`, `newsletter.landesdatenbank.nrw.de`, `newsletter.regionalstatistik.de`). `genesis.destatis.de` and `www-genesis.destatis.de` are the federal front door, not a second catalog. Skip newsletter hosts, bare IPs, and pages that only link to Destatis or Regionalstatistik.

Checked 24 September 2026. `body="genesis-online.css"` returned 26 rows and 9 hosts: the NRW aliases, `regionalstatistik.de` and its newsletter host, `bildungsmonitoring.de`, and `genesis.sachsen-anhalt.de`. The same 26 rows came back for `body="css/genesis-online.css"`, `body="genesis-online-colors.css"`, `body="AmtsLogo.svg"`, `body="js/fokus.js" && body="GENESIS"`, and `body="Menu=Anmeldung" && body="genesis-online"`. Prefer the stylesheet name. `AmtsLogo.svg` is a generic asset filename that happened to match this set.

`body="recherchehilfe.js"` returned 29 rows and 12 hosts. It adds the Destatis links page (`genesis.destatis.de`, `www-genesis.destatis.de`) and the bare IP `194.95.119.21`. `body="genesis-online.css" || body="recherchehilfe.js"` is that same 29. `body="tief gegliederte Ergebnisse der amtlichen Statistik"` is also 29 (the classic meta description). `js_name="recherchehilfe.js"` returned 0.

FOFA has not indexed the catalog HTML of several live installations. `host="statistikdaten.bayern.de"` is 2 rows titled `禁止访问！`. `host="daten.statistik-bw.de"` is a 301. `host="statistik.sachsen.de"` is the office homepage plus `collab-edge` ports, not `/genonline/online`. `host="ergebnisse.zensus2022.de"` is a 400. GET still shows the classic shell on Bayern, Baden-Württemberg, and Sachsen, and those records are already registered.

The 2025 shell is not in the index. `body="gor-webapp.1"`, `body="gor-webapp-custom"`, and `body="gor-webapp" && country="DE"` returned 0. `body="Statis Sans" && title="GENESIS-Online"` and `body="sequenz=statistikTabellen"` returned 0. `body="gor-webapp"` alone is 4 unrelated hosts (`rutasdemoteros.es`, `show.kostecky.cz`). `body="searchInputRoot"` is 3 unrelated sites. Live `/datenbank/online` pages on Regionalstatistik, the NRW Landesdatenbank, and the education monitor still serve `gor-webapp`.

These are not usable as the catalog query. `body="GENESIS-Online"` and `body="/genesis/online"` both returned 435, and `body="GENESIS-Online" && country="DE"` returned 159: office homepages, Datenguide (`datengui.de` and `ernte-teilen.org` vhosts), API wrappers, and other brands. `title="GENESIS-Online"` is 23 and is mostly games and schools (`silkroadgenesis.com`, `genesisonlineschool.com`, `star-genesis.com`), plus the Destatis links page. `body="genesisclient"` is 6 (bioinformatics and a fintech site), so drop that token. `body="Gemeinsames Neues Statistisches Informations-System"` is 0. `body="operation=themes"` is 41 and includes unrelated hosts; `body="GENESIS-Online" && body="operation=themes"` is 30 and adds link-out pages (`statistik.thueringen.de`, `mobilitydatamap.iis.fraunhofer.de`), not extra installations. `body="genesisonline"` is 34 and includes the Baden-Württemberg office homepage plus unrelated sites. `body="OpenSearch_de.xml"` is 2,016. `body="datenbank/online"` is 241. `host="genesis" && country="DE"` is 837 and `cert="genesis" && country="DE"` is 636 (CAS genesisWorld, the car brand, and other agencies).

| Tool | Query |
|------|-------|
| Google | `"GENESIS-Online" (Statistik OR Destatis) site:.de` |
| Google | `inurl:/genesis/online` |
| Censys | `web.endpoints.http.body: "genesis-online.css"` |
| FOFA | `body="genesis-online.css"` |
| Censys | `web.endpoints.http.body: "recherchehilfe.js"` |
| FOFA | `body="recherchehilfe.js"` |

## IBIS-PH (`ibisph`) {#ibisph}

US state public-health indicator system. Community: [Adopt IBIS](https://ibis.utah.gov/ibisph-view/resource/AdoptIBIS.html).

**Signals:** IBIS-PH / IBIS-Q; `/ibisph-view/`; XML-driven indicator pages.

**Confirm:** GET a public indicator home or query module. Skip login-only health department tools.

| Tool | Query |
|------|-------|
| Google | `"IBIS-PH" OR "IBIS PH" (indicators OR "public health") site:.gov` |
| Censys | `web.endpoints.http.body: "ibisph"` |
| FOFA | `body="ibisph"` |

## Envista Web (`envista`) {#envista}

Envitech public air-quality and environmental monitoring sites. Product: [Envista Web](https://www.envitechsoftware.com/Software). Flagship in this registry: [SAAQIS](https://saaqis.environment.gov.za/). The desktop Envista ARM client is not a catalog.

**Signals:** script `/scripts/layers/envitechIndex/envitechIndex.js`; `/Scripts/utils/Kendo/KendoSettingsOverride.js`; API path `v1/envista`. Asset query `v=3.24x.16.*` matches the Envista ARM Web revision series and changes between builds.

**Confirm:** GET the public station home and match `envitechIndex.js`. One record per agency network, not per station or hourly measurement. A page that only loads Kendo UI is not Envista. Skip the Envitech marketing site.

| Tool | Query |
|------|-------|
| Google | `"envitechIndex.js" OR "KendoSettingsOverride.js" air quality` |
| Google | `"v1/envista" (AQI OR "air quality" OR stations)` |
| Censys | `web.endpoints.http.body: "envitechIndex.js"` |
| FOFA | `body="envitechIndex.js"` |
| Censys | `web.endpoints.http.body: "KendoSettingsOverride.js"` |
| FOFA | `body="KendoSettingsOverride.js"` |
| FOFA | `body="v1/envista"` |

## Fingertips (`fingertips`) {#fingertips}

OHID public health profiles for England. Hub: [fingertips.phe.org.uk](https://fingertips.phe.org.uk/). API docs: [Fingertips API](https://fingertips.phe.org.uk/profile/guidance/supporting-information/api). The home page sets `FT.url.corews` to [fingertipsws.phe.org.uk](https://fingertipsws.phe.org.uk/), which returns the same `/api/profiles` JSON. That host is the API of this hub.

**Signals:** stylesheet `/css-fingertips`, script `/js-fingertips1`, classes `app-masthead-fingertips` and `app-width-container-fingertips`; title `Fingertips | Department of Health and Social Care`; REST `/api/profiles`.

**Confirm:** GET `/api/profiles` JSON (profile `Id`, `Name`, `Key`) or the public profiles home. One national hub — do **not** add a catalog per local authority or per profile. Skip the bare-IP “Fingertips CMS - Login” shell. Distinct from IBIS-PH, Power BI embeds, and InstantAtlas reports.

Checked 24 September 2026. `body="css-fingertips"` is 3 rows: `fingertips.phe.org.uk` on ports 80 and 443, plus `172.187.234.240:8081` (title “Fingertips CMS - Login”, no domain; connect timeout, login shell). `body="js-fingertips1"`, `body="app-masthead-fingertips"`, `body="app-width-container-fingertips"`, `body="fingertipsws.phe.org.uk"`, and `title="Fingertips | Department of Health and Social Care"` are 2 rows, both the public hub. `host="fingertipsws"` is 1 (`fingertipsws.phe.org.uk`). `host="fingertips.phe.org.uk"` is 3 and only restates that hub.

These strings are not usable as instance queries: `title="Fingertips"` (9,871 hosts, the idiom “at your fingertips”), `body="fingertips-title"` (7,339; FOFA splits the hyphen), `host="fingertips"` (640, including `*.fingertips.alarislabs.com` and `fingertips.kr`), `body="FT.url"` (444), `body="js-fingertips"` and `body="/js-fingertips"` (4, including Jean Yip salon admin hosts whose live HTML does not contain that path — prefer `js-fingertips1`), `cert="fingertips"` (27 company sites; `cert="fingertips.phe.org.uk"` is 0), `body="corews"` (94), `body="Public health profiles"` (28, including ScotPHO and the Leeds Observatory), and `body="Fingertips CMS"` (2, including `www.aspey-lawrence.co.uk`). `host="fingertips" && country="GB"` is 11 and adds `fingertips.org.uk` (Myth:Auth login) and `fingertips.online`.

| Tool | Query |
|------|-------|
| Google | `"css-fingertips" OR "js-fingertips1" OR "app-masthead-fingertips"` |
| Google | `"Fingertips" ("public health profiles" OR OHID) site:phe.org.uk` |
| Censys | `web.endpoints.http.body: "css-fingertips"` |
| FOFA | `body="css-fingertips"` |
| Censys | `web.endpoints.http.body: "js-fingertips1"` |
| FOFA | `body="js-fingertips1"` |
| Censys | `web.endpoints.http.body: "app-masthead-fingertips"` |
| FOFA | `body="app-masthead-fingertips"` |
| FOFA | `body="app-width-container-fingertips"` |
| FOFA | `title="Fingertips \| Department of Health and Social Care"` |
| FOFA | `host="fingertipsws"` |

## Nomis (`nomis`) {#nomis}

ONS official labour market and census statistics service, run under contract by Durham University. Hub: [www.nomisweb.co.uk](https://www.nomisweb.co.uk/). API help: [Nomis API](https://www.nomisweb.co.uk/api/v01/help). Use `software.id: nomis`.

**Signals:** host `www.nomisweb.co.uk`; title `Nomis - Official Census and Labour Market Statistics`; REST `/api/v01/dataset/def.sdmx.json` returns the SDMX-JSON dataset list with sender `NOMIS`.

**Confirm:** GET `/api/v01/dataset/def.sdmx.json` (header sender id `NOMIS`). One national hub — do **not** add a catalog per dataset or per geography. Distinct from the ONS website (ons.gov.uk), from NISRA and StatsWales products, and from Power BI or InstantAtlas labour-market dashboards.

Checked 28 September 2026. `host="www.nomisweb.co.uk"` restates the single hub; branded look-alikes are third-party sites embedding Nomis tables, not instances.

| Tool | Query |
|------|-------|
| Google | `"Nomis" "Official Census and Labour Market Statistics"` |
| Google | `site:nomisweb.co.uk "api/v01"` |
| Censys | `web.endpoints.http.body: "support@nomisweb.co.uk"` |
| FOFA | `body="support@nomisweb.co.uk"` |
| FOFA | `title="Nomis - Official Census and Labour Market Statistics"` |

## StatsWales (`statswales`) {#statswales}

Welsh Government official statistics dissemination service. Hub: [statswales.gov.wales](https://statswales.gov.wales/). Public API (OAS 3.1): [api.stats.gov.wales/v1](https://api.stats.gov.wales/v1/docs/). Use `software.id: statswales`.

**Signals:** host `statswales.gov.wales`; bilingual English/Welsh catalog chrome; API docs at `api.stats.gov.wales/v1/docs`.

**Confirm:** GET `https://api.stats.gov.wales/v1/datasets` (list of published datasets) or the bilingual catalog home. One national hub — do **not** add a catalog per topic or per dataset. The legacy OData service on `open.statswales.gov.wales` was retired in August 2024; do not add it as an instance. Distinct from InfoBaseCymru local authority profiles.

Checked 28 September 2026. `host="statswales.gov.wales"` and `host="api.stats.gov.wales"` restate the single hub and its API.

| Tool | Query |
|------|-------|
| Google | `site:statswales.gov.wales "Catalogue"` |
| Google | `"StatsWales" "api.stats.gov.wales"` |
| FOFA | `host="statswales.gov.wales"` |
| FOFA | `host="api.stats.gov.wales"` |

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

## FPMA Tool (`fpmatool`) {#fpmatool}

FAO GIEWS Food Price Monitoring and Analysis Tool, version 4. Global instance: [fpma.fao.org/giews/fpmat4/global/](https://fpma.fao.org/giews/fpmat4/global/). National instances run on FAO hosts (`fpma.fao.org/giews/fpmat4/{iso3}/`, `fpma.review.fao.org/giews/fpmat4/{iso3}/`) or on national statistical-office and agriculture-ministry sites (Kyrgyzstan, Tajikistan, Uzbekistan, El Salvador, Guatemala are in the registry).

**Signals:** URL path `/giews/fpmat4/`; “Food Price Monitoring and Analysis (FPMA) Tool” branding with the GIEWS logo; country/market/commodity selector with monthly price charts.

**Confirm:** public price dashboard loads with selectable markets and commodities and CSV/Excel download. Use `software.id: fpmatool`. One record per country instance.

| Tool | Query |
|------|-------|
| Google | `"Food Price Monitoring and Analysis" tool (GIEWS OR FAO) -site:fao.org` |
| Google | `inurl:/giews/fpmat4/` |
| Censys | `web.endpoints.http.body: "fpmat4"` |
| FOFA | `body="fpmat4"` |

**False positives:** FAOSTAT and other FENIX-family FAO apps (use `fenix`); GIEWS country briefs and price-analysis PDF reports; WFP VAM price tools (different stack).

## Global Cancer Observatory (`gco`) {#gco}

IARC/WHO cancer indicators platform (GLOBOCAN). Mirrored on [gco.iarc.fr](https://gco.iarc.fr) and [gco.iarc.who.int](https://gco.iarc.who.int); tools include Cancer Today, Cancer Tomorrow, and Cancer Over Time.

**Signals:** GCO branding with IARC/WHO logos; `/today/`, `/tomorrow/`, `/overtime/` tool paths on `gco.iarc.*` hosts; "Global Cancer Observatory" title.

**Confirm:** public Cancer Today data table loads with country and cancer-type selectors. Use `software.id: gco`. One record per GCO host or tool scope; do not add each cancer-type page.

| Tool | Query |
|------|-------|
| Google | `"Global Cancer Observatory" (GLOBOCAN OR "Cancer Today")` |
| Censys | `web.names: "gco.iarc.fr" OR web.names: "gco.iarc.who.int"` |
| FOFA | `body="Global Cancer Observatory"` |

**False positives:** IARC publications portal; CanScreen5 (separate IARC screening repository); national cancer registries that only cite GLOBOCAN numbers.

## BRS Electronic Reporting System Dashboards (`brsers`) {#brsers}

Basel, Rotterdam and Stockholm Conventions national-report dashboards, one eRSodataReports app per convention. Live instances: [Basel](https://ers.basel.int/eRSodataReports2/ReportBC_DashBoard.html) and [Stockholm](https://ers.pops.int/eRSodataReports2/ReportSC_DashBoard.html).

**Signals:** URL path `/eRSodataReports2/` with `Report{BC,SC}_DashBoard.html`; "Electronic Reporting System" branding on `ers.*.int` hosts.

**Confirm:** public dashboard loads with year/region/country filters and Excel export. Use `software.id: brsers`. One record per convention dashboard.

| Tool | Query |
|------|-------|
| Google | `inurl:eRSodataReports2` |
| Censys | `web.endpoints.http.body: "eRSodataReports"` |
| FOFA | `body="eRSodataReports"` |

**False positives:** convention main sites (basel.int / pops.int homepages are not data catalogs); PIC Rotterdam Convention pages without the eRS dashboard.

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

**Signals:** HTML title `Beyond 20/20 WDS`; language-selection page assets `Common/Images/biglogo125.gif`, `WDS.resources.js`, `Common/Styles/Style_NS.css`, `initWdsFormObj`; paths `/ReportFolders/reportFolders.aspx`, `/TableViewer/tableView.aspx`; reports-page logo `Common/Images/wds.gif`; IVT downloads.

**Confirm:** GET the language page or `ReportFolders/reportFolders.aspx` without login. One catalog per public WDS **installation** (the folder tree), not per `ReportId`. Skip Crime Insight / Perspective (`*.beyond2020.com` NIBRS tenants), OSFI `osfi.beyond2020.com` (self-registration), the vendor demo `wds.beyond2020.com`, IEA `wds.iea.org` (login; product retired for public data), and Statistics Canada’s unrelated **Web Data Service** REST API.

Checked 24 September 2026. FOFA indexes the **language-selection page**, not the reports page. That page titles itself `Beyond 20/20 WDS - Language Selection` and loads `biglogo125.gif`, `WDS.resources.js`, `Common/Styles/Style_NS.css`, and `initWdsFormObj` (`UILangRedirect` is the same page). Each of those queries, and `title="Beyond 20/20 WDS"`, returned the same 5 rows: `wds.beyond2020.com`, bare IP `54.217.191.97`, `tradestats.thedti.gov.za`, and `www.jodidb.org` (scheme duplicates). Subpath installs such as `difusion.jccm.es/wds/` are absent from that set.

`title="Beyond 20/20 WDS - Reports"`, `body="Common/Images/wds.gif"`, `body="wdsAPI.js"`, and `js_name="WDS.resources.js"` returned 0: those strings live on the reports page. `body="ReportFolders/reportFolders.aspx"` matched 16 hosts that **link** the path (`jodidata.org`, `thedtic.gov.za`, `estadistica.castillalamancha.es`, blogs, `osfi.beyond2020.com`), so use it to find a parent page and then open the installation URL. These are not usable as the catalog query: `body="wds.gif"` (92 unrelated hosts), `body="tableView.aspx"` (37, blogs and other ASP.NET apps), `body="G_strLanguage"` (28,441, Yealink phones), `title="Beyond 20/20"` (23, mostly optometry), `body="Beyond 20/20 Inc."` (Crime Insight marketing; the reports-page generator meta matched 0), and `domain="beyond2020.com"` (99: Crime Insight, Perspective, and SIDEARM Sports, plus the vendor WDS host).

| Tool | Query |
|------|-------|
| Google | `"Beyond 20/20 WDS" (Reports OR Informes OR "Language Selection")` |
| Google | `inurl:ReportFolders/reportFolders.aspx` |
| Google | `"Beyond 20/20 WDS - Table view"` |
| Censys | `web.endpoints.http.html_title: "Beyond 20/20 WDS"` |
| FOFA | `title="Beyond 20/20 WDS"` |
| Censys | `web.endpoints.http.body: "biglogo125.gif"` |
| FOFA | `body="biglogo125.gif"` |
| Censys | `web.endpoints.http.body: "WDS.resources.js"` |
| FOFA | `body="WDS.resources.js"` |
| Censys | `web.endpoints.http.body: "ReportFolders/reportFolders.aspx"` |
| FOFA | `body="ReportFolders/reportFolders.aspx"` |

**False positives:** Beyond 20/20 Professional Browser / IVT file downloads with no WDS UI; Crime Insight; SIDEARM Sports (`sidearm.beyond2020.com`, a different “Beyond 2020”); vendor demo `wds.beyond2020.com` (sample cubes under “This is the new server WDS01”); bare IPs with an empty tree; login-only WDS; UNCTADstat `/wds/` redirects (now Data Centre); UNESCO UIS Data Browser (migrated off WDS).

## StatPlanet (`statplanet`) {#statplanet}

StatSilk interactive maps and dashboards (StatPlanet Cloud / HTML5, older Flash). Site: [statsilk.com](https://www.statsilk.com). Gallery: [statsilk.com/gallery](https://www.statsilk.com/gallery). Live example: [EC-OECD STIP Compass statistics](https://stip.oecd.org/Stats/STIP-StatTrends.html).

**Signals:** `id="statsilk-container"`; HTML title `StatPlanet`; `StatPlanet Cloud`; `StatPlanet_Cloud.html`; `data.csv` / `settings.csv`; StatSilk footer or logo; URL params `i=` `v=` `t=` on Cloud dashboards.

**Confirm:** GET the dashboard HTML and a public `data.csv` (or SDMX-backed Cloud instance). One record per public explorer, not per indicator or per `*-StatTrends.html` file on the same host.

[StatPlanet_Cloud.html](https://github.com/StatSilk/StatPlanet/blob/master/StatPlanet_Cloud.html) sets `id="statsilk-container"` (5 hosts in September 2026, including `unicefdashboard.netlify.app` and `statplanet.itcloud.pt`). The same file writes `StatPlanet Cloud` (4 hosts, all `statplanet.itcloud.pt`). `title="StatPlanet"` matched 7; three of those rows are `statplanet.org`, a business site titled “Statplanet — Premium Business”, not a StatSilk dashboard. `body="statplanet-cloud.js"` and `body="js/splashscreen.css"` only hit `statplanet.itcloud.pt` (the stock ICT sample). `body="cloud.statsilk.com"` is the public tenant bucket index, not a catalog homepage. Keep `body="statsilk-container"`.

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

Statistics/indicator sections published on Microsoft SharePoint sites (ministries, central banks, planning agencies) instead of a data platform. The same id covers open-data catalog pages on SharePoint, including Spanish ministry sedes and university catalogs.

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

## LiveShop (`liveshop`) {#liveshop}

Central-bank / monetary-institute statistics database on the tenant's own domain. Known tenants: [statistics.cbn.gov.ng](https://statistics.cbn.gov.ng) (Central Bank of Nigeria), [wami-data.org](https://wami-data.org) (West African Monetary Institute). No first-party vendor site is known.

**Signals:** HTML title `Home Page - LiveShop`; `/shop` landing page with `/shop/meta-data` and `/shop/data-calendar`; `/data-browser` chart/table view; ASP.NET layout with `/lib/bootstrap/dist/...` asset paths.

**Confirm:** GET `/` and `/shop` — title must be `Home Page - LiveShop`. Distinct from DataWarehousePro (`datawarehousepro`), which hosts tenants on the vendor domain `app.datawarehousepro.com/go/{tenant}`. One record per institutional tenant.

| Tool | Query |
|------|-------|
| Google | `"Home Page - LiveShop"` |
| Google | `inurl:"shop/meta-data" (statistics OR "data browser")` |
| Censys | `web.endpoints.http.body: "Home Page - LiveShop"` |
| FOFA | `body="Home Page - LiveShop"` |
| FOFA | `title="LiveShop"` |

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

**Signals:** title `Goal Tracker`; header classes `bg-goals-1` … `bg-goals-17` (the 17-stripe SDG bar). Current Strapi builds also embed `hasOwnData` on each indicator. Tenant HTML does not contain “Data Act Lab”, so `body="Data Act Lab"` returned 0 (24 September 2026). `body="gt-heading-v6-latin"`, `body="api.goaltracker.org"`, `body="calc(100% / 17)"`, and `body="available_indicators"` also returned 0. `body="giorgio-sans-bold.woff2"` and `body="dataAvailabilityDescription"` are noisy. `host="goaltracker"` matches unrelated goal-tracking apps.

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

## Cascade CMS (`cascadecms`) {#cascadecms}

Hannon Hill Cascade CMS, used by US state agencies and universities to publish indicator and data pages. Product: [hannonhill.com/products/cascade-cms](https://www.hannonhill.com/products/cascade-cms/index.html).

**Signals:** template comments `<system-region name="CAROUSEL"/>`; state labor-market sites share `_files/css`, `_files/js`, `news-gallery.js`, and `random-background.js`.

**Confirm:** the system-region comment or that shared `_files` layout on a public indicator or data page. One host = one catalog. Do not assign `cascadecms` to a page that only links out to a Cascade site, or to a custom data application that does not carry the CMS template.

| Tool | Query |
|------|-------|
| Google | `"system-region" Cascade (LMI OR statistics OR indicators)` |
| Google | `inurl:_files/js "news-gallery.js"` |
| Censys | `web.endpoints.http.body: "system-region name=\"CAROUSEL\""` |
| FOFA | `body="system-region name=\"CAROUSEL\""` |

## DesInventar (`desinventar`) {#desinventar}

UNDRR disaster loss and damage database methodology and software. Global hub: [desinventar.net](https://www.desinventar.net) (DesInventar Sendai). National installations are typically ministry or disaster-management agency hosts, e.g. CamDi at [camdi.ncdm.gov.kh/DesInventar/main.jsp](https://camdi.ncdm.gov.kh/DesInventar/main.jsp).

**Signals:** path `/DesInventar/main.jsp` (classic Java webapp); title or body "DesInventar" with "disaster loss" / "Sendai" wording; UNDRR / UNDRR DesInventar Sendai branding; country-coded database profiles.

**Confirm:** GET the public query page (`main.jsp` or the Sendai web system) and check it serves a named national disaster loss inventory. One catalog per country database host.

**False positives:** Sendai Framework Monitor (`sendaimonitor.undrr.org`, a separate UNDRR product, registered on its own); academic papers and NGO reports that merely cite DesInventar data; EM-DAT.

| Tool | Query |
|------|-------|
| Google | `inurl:/DesInventar/main.jsp` |
| Google | `"DesInventar" ("disaster loss" OR "damage and loss") database` |
| Censys | `web.endpoints.http.body: "DesInventar"` |
| FOFA | `body="/DesInventar/main.jsp"` |
| FOFA | `title="DesInventar"` |

## SORMAS (`sormas`) {#sormas}

Open-source disease surveillance and outbreak response platform (SORMAS Foundation, GPL-3.0). National deployments are run by ministries of health — e.g. Nepal EDCD at [analysis.edcd.gov.np/bulletin](https://analysis.edcd.gov.np/bulletin). Registered catalogs are the **public dashboards/bulletins** a deployment chooses to publish, not the staff-facing case-management app. Docs and code: [github.com/SORMAS-Foundation/SORMAS-Project](https://github.com/SORMAS-Foundation/SORMAS-Project). Use `software.id: sormas`.

**Signals:** "SORMAS" branding on a login page or public bulletin; paths `/sormas-ui/`, `/sormas-rest/`; ministry of health / epidemiology division hosts publishing weekly counts of outbreak-prone diseases (AGE, SARI, dengue) by district.

**Confirm:** the public dashboard or bulletin loads without login and shows disease counts by administrative unit. Skip staff-only surveillance logins with no public data surface — most SORMAS deployments publish nothing anonymous. One catalog per public dashboard host, not per disease module.

| Tool | Query |
|------|-------|
| Google | `"SORMAS" (dashboard OR bulletin OR "public") (surveillance OR outbreak) site:gov.*` |
| Google | `inurl:/sormas-ui OR inurl:/sormas-rest` |
| Censys | `web.endpoints.http.body: "sormas-ui"` |
| FOFA | `body="sormas-ui"` |

## BOOST (`boost`) {#boost}

World Bank BOOST open-budget portals: country-owned fiscal transparency sites publishing line-item expenditure/revenue extracted from national FMIS systems (90+ country engagements since 2010). Product page: [worldbank.org/en/programs/boost-portal](https://www.worldbank.org/en/programs/boost-portal). Registered instances: Paraguay [boostvep.mef.gov.py](https://boostvep.mef.gov.py/gastos_anual/), Cameroon [boostcameroon.cm](https://www.boostcameroon.cm/), Mauritania [boost.budget.mr](http://boost.budget.mr/), Tunisia Mizaniatouna [mizaniatouna.gov.tn](http://www.mizaniatouna.gov.tn/tunisia/template_fr/).

**Signals:** “BOOST” branding in the page title or footer; finance-ministry hosts; paths like `/gastos_anual/`, `/fichiersBoost/`; JS globals `boost.boost_options` and `boost-pivot`; interactive pivot tables of budget execution with CSV/Excel download.

**Confirm:** the public pivot/download UI loads without login and shows budget expenditure or revenue tables with a CSV/Excel export. One catalog per country portal. Skip the World Bank BOOST program pages and the WB-hosted Open Budgets Portal itself — those are program/documentation surfaces, not country catalogs.

| Tool | Query |
|------|-------|
| Google | `"BOOST" (budget OR gastos OR dépenses) (finance OR hacienda) (pivot OR download) -site:worldbank.org` |
| Google | `inurl:boost (budget OR finance OR gastos) site:gov.*` |
| Google | `"boost-pivot" OR "boost_options"` |
| Censys | `web.endpoints.http.body: "boost_options"` |
| FOFA | `body="boost-pivot"` |
| FOFA | `body="boost_options"` |

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
