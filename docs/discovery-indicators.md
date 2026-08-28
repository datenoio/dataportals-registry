# Discovering indicators and microdata catalogs

How to find **indicators catalogs** (`catalog_type: Indicators catalog`) and **microdata catalogs** (`catalog_type: Microdata catalog`). Search-engine syntax: [discovery-search-tools.md](discovery-search-tools.md).

Statistical offices, central banks, SDG reporting sites, and survey archives are the usual owners. Search the agency name plus the local word for “statistics” / “indicators” / “microdata”, then confirm the platform. High-count stacks with their own recipes: PxWeb, PxStat, OpenSDG, Goal Tracker, IMF NSDP, .Stat Suite, Istat Data Browser, Swing, Knoema (portal homes only), SDMX-RI, GENESIS-Online, IBIS-PH, DHIS2, FENIX / CountrySTAT, TabNet, SparkMap, DataWarehousePro, Beyond 20/20, NADA, NESSTAR, REDATAM, Colectica, OBiBa Mica, IPUMS. Related PC-Axis stack: PxStat (CSO Ireland; not PxWeb).

## PxWeb (`pxweb`) {#pxweb}

PC-Axis web tables, widely used by Nordic and other NSOs. Examples: [SCB PxWeb examples](https://www.scb.se/en/services/statistical-programs-for-px-files/px-web/pxweb-examples/).

**Confirm:** `https://host/api/v1/` (language segment may be `/api/v1/en/` or `/api/v1/{lang}/`). UI often `/pxweb/` or titled “PxWeb”.

| Tool | Query |
|------|-------|
| Google | `intitle:PxWeb OR inurl:/pxweb` |
| Google | `inurl:/api/v1 "px" statistics` |
| Google | `"PxWeb" (statistik OR statistics OR tilastot)` |
| Censys | `web.endpoints.http.html_title: "PxWeb"` |
| Censys | `web.endpoints.http.body: "PxWeb"` |
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
| Censys | `web.endpoints.http.html_title: "PxStat"` |

**False positives:** PxWeb (`/api/v1/`, title “PxWeb”); the CSO demo (`demo-pxstat.cso.ie`); `visual.cso.ie` maps over the same tables; GitHub wiki. Irish public bodies that publish **on** data.cso.ie are not separate catalogs.

## OpenSDG (`opensdg`) {#opensdg}

Static SDG reporting sites (often GitHub Pages). Community: [open-sdg.org/community](https://open-sdg.org/community).

**Signals:** `/reporting-status`, indicator pages `/\{goal\}-\{target\}-\{indicator\}`, “Open SDG” in footer or `open-sdg` JS.

| Tool | Query |
|------|-------|
| Google | `"Open SDG" OR "open-sdg" indicators` |
| Google | `inurl:reporting-status "sustainable development"` |
| Google | `site:github.io "Open SDG"` |
| Censys | `web.endpoints.http.body: "open-sdg"` |

Start from the community list; use Google for national translations (`indicadores ODS`, `indicateurs ODD`).

## .Stat Suite (`statsuite`) {#statsuite}

SIS-CC / OECD .Stat. **Confirm:** `/api/search` or SDMX endpoints; UI “.Stat Suite” / Data Explorer.

| Tool | Query |
|------|-------|
| Google | `".Stat Suite" OR "SIS-CC" "data explorer"` |
| Google | `inurl:/nsi OR "DotStat" SDMX` |
| Censys | `web.endpoints.http.body: ".Stat"` |

**False positives:** Istat **Data Browser** / StatKit (`databrowserhub/api/core`, `istatdatabrowser`) — that is not .Stat Suite.

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

## Swing (`swing`) {#swing}

ABF Research statistical databank (Swing Viewer / Swing Jive). Vendor: [swingsoftware.eu](https://swingsoftware.eu/). Flemish public tenants live at `{city}.incijfers.be` and `provincies.incijfers.be`.

**Signals:** hostname `*.incijfers.be`; “Powered by Swing”; Swing Viewer / databank UI.

**Confirm:** GET the public databank (not `/Admin/Studio/`). One record per municipal or provincial tenant. Dutch “in cijfers” / waarstaatjegemeente sites on other hosts are the same product when Swing-branded.

| Tool | Query |
|------|-------|
| Google | `site:incijfers.be` |
| Google | `"Powered by Swing" OR "Swing Viewer" (incijfers OR databank)` |
| Censys | `web.names: "incijfers.be"` |
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
| Censys | `web.names: "engagementnetwork.org"` |

## SDMX-RI (`sdmxri`) {#sdmxri}

Eurostat SDMX Reference Infrastructure (NSI web service). Site: [sdmx.org](https://sdmx.org/?page_id=4666).

**Signals:** `NSIWebService`, SDMX-RI; `/NSIStdV20Service` or SDMX REST 2.1.

**Confirm:** GET a working SDMX query or the public NSI page that lists dataflows. If PxWeb or .Stat is the human UI, register that catalog instead of a raw SOAP URL.

| Tool | Query |
|------|-------|
| Google | `"SDMX-RI" OR "NSI Web Service" OR NSIStdV20Service` |
| Censys | `web.endpoints.http.body: "NSIWebService"` |

## GENESIS-Online (`genesisonline`) {#genesisonline}

Destatis / Länder statistical database. Example: [www-genesis.destatis.de](https://www-genesis.destatis.de). Table retrieval is often **POST-only** — do not invent GET API paths.

**Signals:** GENESIS-Online; `genesisclient`; `/genesis/online`.

**Confirm:** GET the public table catalog. One record per statistical-office instance (Bund vs Land).

| Tool | Query |
|------|-------|
| Google | `"GENESIS-Online" (Statistik OR Destatis) site:.de` |
| Google | `inurl:/genesis/online` |
| Censys | `web.endpoints.http.body: "GENESIS-Online"` |

## IBIS-PH (`ibisph`) {#ibisph}

US state public-health indicator system. Community: [Adopt IBIS](https://ibis.utah.gov/ibisph-view/resource/AdoptIBIS.html).

**Signals:** IBIS-PH / IBIS-Q; `/ibisph-view/`; XML-driven indicator pages.

**Confirm:** GET a public indicator home or query module. Skip login-only health department tools.

| Tool | Query |
|------|-------|
| Google | `"IBIS-PH" OR "IBIS PH" (indicators OR "public health") site:.gov` |
| Censys | `web.endpoints.http.body: "ibisph"` |

## DHIS2 (`dhis2`) {#dhis2}

Open-source health management information system (HISP / University of Oslo). More than 70 ministries run national HMIS instances. Docs: [docs.dhis2.org](https://docs.dhis2.org). Public FlexiPortal front-ends also count when they publish indicators from a DHIS2 backend. Use `software.id: dhis2`. Do not label a CKAN health document site DHIS2 from a tag alone.

**Signals:** `/dhis-web-commons/`, `/dhis-web-dashboard/`, login chrome “DHIS 2”; REST `/api/system/info`.

**Confirm:** `GET https://host/api/system/info` JSON with a `version` field, or a public portal that is documented as DHIS2. Skip staff-only logins with no public indicator catalog.

| Tool | Query |
|------|-------|
| Google | `"DHIS2" OR "DHIS 2" (HMIS OR "health information" OR portal) -site:dhis2.org -site:github.com` |
| Google | `inurl:/dhis-web-commons OR inurl:/api/system/info` |
| Censys | `web.endpoints.http.body: "dhis-web-commons"` |
| Censys | `web.endpoints.http.html_title: "DHIS 2"` |

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
| Censys | `web.endpoints.http.body: "deftohtm.exe"` |

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
| Censys | `web.names: "fenixservices.fao.org"` |

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
| Censys | `web.endpoints.http.body: "/webapi/jsf/login.xhtml"` |

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
| Censys | `web.endpoints.http.body: "ReportFolders/reportFolders.aspx"` |

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
| Censys | `web.endpoints.http.body: "StatPlanet Cloud"` |

**False positives:** statsilk.com marketing, GitHub `StatSilk/StatPlanet`, Flash-only dead maps, a single thematic poster, StatPlanet World Bank / EdStats viewers of [data.worldbank.org](https://data.worldbank.org) (already `dataworldbankorg`). Skip login-only corporate dashboards.

## Other indicator platforms

| `software.id` | Where to look | Typical query |
|---------------|---------------|---------------|
| `statplanet` | see above | |
| `superstar` | see above | |
| `statsuite` | see above | |
| `istatdatabrowser` | see above | |
| `stattech` | SIS-CC .Stat technology / SDMX APIs | `"Stat Technology" OR "SIS-CC" SDMX` |
| `oracleapex` | Oracle APEX **indicator apps** | `"Oracle APEX" (statistika OR indicators)` (skip generic APEX sites) |
| `datavavt` | Data VAVT economic indicators | `"data.vavt.ru"` |
| `superset` | Apache Superset **public indicator dashboards** | `"Apache Superset" (open data OR indicators)` |
| `ibmcognos` | Cognos **public stat portals** | `"Cognos" (statistics OR open data)` |
| `bicontour` | BI Contour dashboards | `"Contour BI" OR "BI Contour" portal` |
| `whoint` | WHO data hub | do not re-add who.int; add only distinct regional hubs |
| `eurostat` | Eurostat | do not re-add the EU hub |
| `ecb` | ECB Data Portal | do not re-add data.ecb.europa.eu |
| `dataworldbankorg` | World Bank Data | do not re-add data.worldbank.org |
| `datauniceforg` | UNICEF data | do not re-add data.unicef.org |
| `ilostat` | ILOSTAT | do not re-add ilostat.ilo.org |
| `databisorg` | BIS Data Portal | do not re-add data.bis.org |
| `datainsight` | Veritas Data Insight **as a public catalog** | rare; skip enterprise-only |

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
| Censys | `web.endpoints.http.body: "IHSN"` |

**False positives:** nada.ihsn.org itself (the software site), WordPress blogs named NADA. Need a **study list** with DDI-style metadata.

## IPUMS (`ipums`) {#ipums}

University of Minnesota extract platform for harmonized census and survey microdata. Collections share one API and extract engine: IPUMS USA, International, CPS, DHS, NHIS, Higher Ed, PMA, MICS, Time Use, plus geographic NHGIS and IHGIS. Developer docs: [developer.ipums.org](https://developer.ipums.org).

**Signals:** `*.ipums.org` or `idhsdata.org` / `nhgis.org`; extract-system UI; “IPUMS” branding. Use `software.id: ipums`.

**Confirm:** GET the **collection home** (variable/sample selector), not a completed extract download. One registry record per public collection. Do not add every extract or variable page.

| Tool | Query |
|------|-------|
| Google | `"IPUMS" (extract OR microdata OR census) site:.org -site:github.com` |
| Google | `site:ipums.org (USA OR International OR CPS OR NHIS)` |
| Censys | `web.names: "ipums.org"` |

## NESSTAR (`nesstar`) {#nesstar}

Older microdata publisher. Many instances are inactive; still record working public catalogs.

| Tool | Query |
|------|-------|
| Google | `"Nesstar" (microdata OR "webview")` |
| Google | `inurl:/webview nesstar` |
| Censys | `web.endpoints.http.body: "Nesstar"` |

## REDATAM (`redatam`) {#redatam}

ECLAC census/survey online processing. Site: [redatam.org](https://www.redatam.org).

| Tool | Query |
|------|-------|
| Google | `"REDATAM" (censos OR census OR "en línea")` |
| Google | `inurl:redatam OR "Redatam Web Server"` |
| Censys | `web.endpoints.http.body: "REDATAM"` |

## Colectica (`colectica`) {#colectica}

DDI metadata catalogs / portals.

| Tool | Query |
|------|-------|
| Google | `"Colectica" (portal OR repository OR DDI)` |
| Censys | `web.endpoints.http.body: "Colectica"` |

## OBiBa Mica (`obibamica`) {#obibamica}

Epidemiological / population-health study catalog (OBiBa). Often paired with Opal; register the **public Mica** discovery UI.

**Signals:** Mica / OBiBa branding; study and network search; `/ws/` REST.

**Confirm:** GET the public study catalog. Skip login-only research networks.

| Tool | Query |
|------|-------|
| Google | `"Mica" OBiBa (studies OR catalog) -site:github.com` |
| Censys | `web.endpoints.http.body: "obiba"` |
| Censys | `web.endpoints.http.body: "Mica"` |

## Survey Solutions (`surveysolutions`) {#surveysolutions}

World Bank survey suite. Register only a **public Data Browser** of microdata, not a data-collection server.

| Tool | Query |
|------|-------|
| Google | `"Survey Solutions" ("data browser" OR microdata) -site:mysurvey.solutions` |

## DataWarehousePro (`datawarehousepro`) {#datawarehousepro}

Central-bank macroeconomic warehouse. Site: [datawarehousepro.com](https://datawarehousepro.com). Tenants: `app.datawarehousepro.com/go/{tenant}` (sometimes a custom domain).

**Signals:** DataWarehousePro chrome; `/guest/getDatabanksWithMnemonics/` API.

**Confirm:** GET `/go/{tenant}` and `/guest/getDatabanksWithMnemonics/{tenant}`. One record per institutional tenant, not per series.

| Tool | Query |
|------|-------|
| Google | `site:app.datawarehousepro.com/go` |
| Google | `"DataWarehousePro" ("central bank" OR statistics)` |
| Censys | `web.names: "app.datawarehousepro.com"` |
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

## Goal Tracker (`goaltracker`) {#goaltracker}

Data Act Lab SDG country platforms. Site: [goaltracker.org](https://goaltracker.org). Distinct from Open SDG (`opensdg`).

**Signals:** host `*.goaltracker.org`; title “Goal Tracker”; Data Act Lab branding.

**Confirm:** GET the country tenant home. One record per country site. Skip the vendor marketing page if a country tenant is already registered.

| Tool | Query |
|------|-------|
| Google | `site:goaltracker.org` |
| Google | `"Goal Tracker" (SDG OR "Global Goals") -site:goaltracker.org/about` |
| Censys | `web.names: "goaltracker.org"` |
| crt.sh | `%.goaltracker.org` |

## Generic statistics-office patterns

```text
site:.gov {country} (statbank OR "statistical database" OR pxweb OR sdmx)
"microdata" (catalog OR archive OR "data archive") {NSO name}
"DDI" "survey catalog" {country}
```

Central banks (`indicators` more often than microdata): `site:{bank-domain} (statistics OR SDMX OR "statistical warehouse")`. Only add a catalog when there is a queryable database, not a PDF publications page.

## Related

- [discovery.md](discovery.md)
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-metadata.md](discovery-metadata.md)
- [harvest-indicators.md](harvest-indicators.md)
- [harvest.md](harvest.md)
- [harvest-protocols.md](harvest-protocols.md)
- [catalog-types.md](catalog-types.md)
- [software-taxonomy.md](software-taxonomy.md)
