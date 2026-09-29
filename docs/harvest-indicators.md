# Harvesting indicators and microdata

Statistical catalogs list **tables, dataflows, indicators, or survey studies**. Harvest those objects — not every observation, PDF yearbook, or news page.

Overview: [harvest.md](harvest.md). Finding catalogs: [discovery-indicators.md](discovery-indicators.md). GET only. Stop on `401`/`403`. Prefer `endpoints[]`.

## What to keep

| Keep | Drop |
|------|------|
| PxWeb **table** (leaf in the subject tree) | Subject **folders** and the API root |
| PxStat **matrix / table** (JSON-stat collection item) | Subject folders, PxWidget embeds, demo site |
| DGBAS Web **table / indicator** in `/DgbasWeb/` | Yearbook PDFs; WINSTA admin; `nstatdb` `/dgbasall/` |
| SDMX **dataflow** | Codelists, concept schemes, DSDs as if they were data (unless you harvest structural metadata on purpose — [harvest-metadata.md](harvest-metadata.md)) |
| OpenSDG **indicator** JSON | Static about/reporting HTML |
| NADA / NESSTAR **study** | Videos, documents, and news items in the same catalog |
| Mica **study** / dataset | Network chrome, person records |
| DHIS2 **data set** / public indicator | Org-unit trees, user accounts, login-only analytics |
| TabNet **`.def` table** (query form) | CGI query sessions, TabWin `.TAB` downloads, individual table cells |
| KOSIS **table / indicator** on kosis.kr | Local-government `/stat/` CMS; 지표누리; SGIS; OpenAPI calls that need a service key as if they were the catalog |
| e-Stat **statistical table** (portal / LOD / dashboard host) | RESAS; ministry pages that only link to e-Stat; every chart on the dashboard host |
| SIDRA **aggregate / table** (`/api/v3/agregados`) | IBGE Cidades@, Ipeadata, Comex Stat, BCB SGS, DATASUS TabNet |
| Fingertips **profile / indicator** | Each local-authority area value; `/api` HTML docs as a list |
| UNdata **series / table** (OpenSearch / portal tree) | SDG Global Database; Comtrade Plus; every observation cell |
| UN Comtrade Plus **trade dataset / flow** | UI chrome; WITS; concatenating `/api` onto comtradeplus.un.org |
| Our World in Data **indicator / chart topic** | Every chart URL; Gapminder WordPress download pages |
| FENIX **domain / dataset** (FAOSTAT groupsanddomains) | FAOSTAT observation cubes; dead CountrySTAT hosts |
| IPUMS **sample** / collection metadata | Completed extract files and variable pages as catalogs |
| Knoema **dataset** on a portal | Individual time-series points and knoema.com global search hits |
| SparkMap **map layer** or assessment report | Saved user maps, login-only CHNA builder sessions, sparkmap.org marketing pages |
| eDatos **indicator / cube** (JSON-stat) | Institute CMS home; Open SDG sites on the same office |
| Cancer-Rates.info **query UI** (one per registry path) | Login-walled tenants; KCR org home when the query UI is registered |
| HCI **indicator dashboard** (one per community site) | Conduent marketing; SparkMap Map Rooms |
| Virtual LMI **LMI home** (one per state tenant) | Generic state LMI pages without `/vosnet/` or virtuallmi.com |
| TerriSTORY **indicator / dashboard** on a regional hub | Commune pages of the same hub; national marketing home |
| IHK-Fachkräftemonitor **Land dashboard** | Arbeitsmarktradar Bayern; IHK-Konjunkturboard; the hub map with no tenant |
| DUVA **Informationsportal table / evaluation** | Login-only DUVA admin; Urban Audit atlas hosts without `/Informationsportal/` |
| Géoclip **indicator / map / territory report** in a public observatory | `geoclip.fr` marketing; ANCT `/donnees_ouvertes`; OCSTAT CMS home when `/atlas/` is registered |
| InstantAtlas **report / atlas** (`ia-min.js` or Dashboard viewer) | Data Observatory WordPress homes; InstantAtlas marketing; GBE table trees with IA maps as extras |
| MATS **dashboard / filterable table** on a Land Datenportal | GENESIS-Online; SIS-Dashboards; MATS press pages with no tables |
| Goal Tracker **indicator / goal** | About / marketing HTML |
| IMF NSDP **SDMX category / series** linked from the country page | NSO homepage, WordPress/Knoema wrappers, the DSBB directory |
| Istat Data Browser **dataflow** (hub catalog item) | Hub chrome, news, dashboards, and the paired SDMX-RI structure-only resources |
| Swing **indicator table / report** | Studio admin, map tiles, dashboard chrome |
| DataWarehousePro **databank / series** | Guest-portal chrome, empty mnemonic lists |
| Beyond 20/20 **report / cube** | ReportFolders chrome without a public report list |
| StatPlanet **indicator** in a live Cloud/HTML5 explorer | Flash-era demo, a single-indicator URL |

Do not download full observation cubes unless the user asked for data files. Catalog harvest = identifiers + title + URL + period.

## PxWeb (`pxweb`) {#pxweb}

Walk the JSON tree. Language segment is often `en`, `sv`, `fi`, `da`.

```text
GET https://host/api/v1/
GET https://host/api/v1/en/
GET https://host/api/v1/sv/
GET https://host/api/v1/fi/
GET https://host/api/v1/da/
```

Each JSON object with `type: t` (table) is a dataset. `type: l` is a folder — recurse. Do not treat a POST of table cells as a new dataset. Cap depth; some NSOs have thousands of tables.

**Keep:** PxWeb **tables** (`type: t`). **Drop:** subject **folders** (`type: l`) and POST observation cubes.

Detection strips `/pxweb/{lang}/...` table-tree paths and Dialog pages so `/api/v1/` attaches at the `/PXWeb` app mount or the origin. Origin `/api/v1/` is also probed when the catalog link keeps a PXWeb mount.

## PxStat (`pxstat`) {#pxstat}

List live tables from the Cube API (often on a `ws.` / `ws-data.` host recorded in `endpoints[]`). Prefer REST ReadCollection; JSON-RPC is equivalent.

```text
GET https://ws-host/public/api.restful/PxStat.Data.Cube_API.ReadCollection/{datefrom}/en
```

Each JSON-stat **collection item** is a dataset. Grain is the **matrix / table code**. Drop subject folders, PxWidget embeds, and the CSO demo. Do not harvest `visual.cso.ie` as a second catalog of the same tables. Date-from filters recently updated tables; omit or use an early date for a full list.

**Keep:** PxStat **matrix / table** collection items. **Drop:** subject folders, PxWidget embeds, the CSO demo, and `visual.cso.ie` as a second copy.

## DGBAS Web (`dgbasweb`) {#dgbasweb}

Taiwan `/DgbasWeb/` statistical query UI. Harvest the public **table / indicator tree**, not yearbook PDFs or login-only WINSTA admin. One harvest scope per county or city tenant. Distinct from WebMain (`webmain`) and from Taiwan PxWeb.

**Keep:** public table / indicator tree nodes under `/DgbasWeb/`.
**Drop:** yearbook PDFs and login-only WINSTA admin. Distinct from WebMain and Taiwan PxWeb.

```text
GET https://host/DgbasWeb/
```


## WebMain (`webmain`) {#webmain}

Filter exports on `software.id = 'webmain'`. One harvest scope per agency WebMain tenant.

There is no anonymous list API. Keep the public **tables / indicators** the single-table and cross-table trees list. Grain is the table or indicator, not each year cell or exported PX. Drop `/DgbasWeb/` local-government tenants (`dgbasweb`), PxWeb on `statdb.dgbas.gov.tw`, extra `funid=` theme URLs on the same host, MOTC Portal, and MOENV epanet.

**Keep:** WebMain **tables / indicators**. **Drop:** extra funid theme URLs on the same host, `/DgbasWeb/`, PxWeb, MOTC Portal, and MOENV epanet.

## KOSIS (`kosis`) {#kosis}

Filter exports on `software.id = 'kosis'`. Harvest each registered host as its own catalog (national hub, `/bukhan/`, agency/local `/statHtml/` tenants, ODA clones).

There is no anonymous OpenAPI list without a service key. Harvest the public **table / indicator tree** the portal lists. Grain is the statistical table or indicator, not each year cell or OpenAPI observation query.

**Keep:** KOSIS **tables / indicators** on the registered host.
**Drop:** local-government `/stat/index.do` CMS skins, 지표누리 (`index.go.kr`), SGIS, SOPORTAL, and OpenAPI calls that require a service key as if they were the catalog.

```text
GET https://kosis.kr/
GET https://kosis.kr/bukhan/
GET {host}/statHtml/statHtml.do
```

## SOPORTAL (`soportal`) {#soportal}

Filter exports on `software.id = 'soportal'`. Harvest each registered host as its own catalog. The application is mounted under a context path (`/portal/`, `/research/portal/`, `/r-one/portal/`).

There is no anonymous OpenAPI list without a service key. Harvest the public **tables / indicators** listed by `{prefix}/portal/stat/` (`easyStatPage.do`, `orgStatPage.do`, `nameStatPage.do`) and `{prefix}/portal/data/dataset/searchDatasetPage.do`. Grain is the statistical table or indicator, not each year cell or OpenAPI observation.

**Keep:** SOPORTAL **tables / indicators** on the registered host.
**Drop:** OpenAPI calls that require a service key, bulletin pages, chart-only dashboards, KOSIS `/statHtml/` tenants, and Wiseitech `commonness.js` hosts that use `mainPage.do`.

```text
GET {prefix}/portal/main/indexPage.do
GET {prefix}/portal/stat/easyStatPage.do
GET {prefix}/portal/stat/orgStatPage.do
```

## e-Stat (`estat`) {#estat}

Filter exports on `software.id = 'estat'`. Three registered hosts: the table portal (`www.e-stat.go.jp`), Statistical LOD (`data.e-stat.go.jp`), and the Statistics Dashboard (`dashboard.e-stat.go.jp`). Harvest each host as its own catalog; do not add extra table or API paths.

The e-Stat API on `api.e-stat.go.jp` needs an application ID — do not invent a relative list on the Drupal portal. Dashboard JSON (`/api/1.0/`) and LOD SPARQL are host-specific. Grain is the **statistical table / indicator**, not every chart.

**Keep:** e-Stat **statistical tables / indicators** on the registered host.
**Drop:** RESAS, ministry pages that only link to e-Stat, and every dashboard chart URL.

```text
GET https://www.e-stat.go.jp/
GET https://data.e-stat.go.jp/
GET https://dashboard.e-stat.go.jp/
```

## OpenSDG (`opensdg`) {#opensdg}

Each SDG indicator is one dataset. List from reporting status or `data/` JSON.

```text
GET https://host/reporting-status
GET https://host/reporting-status/
GET https://host/en/reporting-status/
GET https://host/indicators.json
GET https://host/data/1-1-1.json
```

Language prefixes (`/en/data/…`) vary. Harvest every indicator id the site publishes, not only `1-1-1`. Drop goal/target **pages** without a data file.

**Keep:** OpenSDG **indicator** JSON. **Drop:** goal/target **pages** without a data file.

## Klimadashboard Münster (`klimadashboardmuenster`) {#klimadashboardmuenster}

One harvest scope per municipal host. Indicator grain is the published **tile / indicator series**, not each chart interaction. Drop the Next.js shell and the national product at klimadashboard.de.

**Keep:** published **indicator** series. **Drop:** UI chrome and Klimadashboard Deutschland.

## SDG Index (`sdgindex`) {#sdgindex}

One harvest scope per dashboard host. Indicator grain is the published database, not each profile URL.

```text
GET https://dashboards.sdgindex.org/
GET https://dashboards.sdgindex.org/rankings
GET https://dashboards.sdgindex.org/profiles
GET https://dashboards.sdgindex.org/downloads/
```

Regional hosts use the same paths (`/rankings`, `/profiles` or `/profils`, `/downloads` or `/telechargements`). The bulk file is usually an `.xlsx` under `/static/downloads/`.

**Keep:** the dashboard’s indicator database (Excel or JSON) and the profile list for that host. **Drop:** chapter narrative pages, individual profile URLs as separate catalogs, and the SDSN marketing site.

## .Stat Suite (`statsuite`) {#statsuite}

```text
GET https://host/api/search
```

SDMX REST: list **dataflows** (the dataset analog). Pair with the Data Explorer UI only to confirm labels. If PxWeb is the public UI on the same office, harvest one catalog — do not double-count the same table. Do not harvest **Istat Data Browser** hubs (`istatdatabrowser`) or classic OECD.Stat / I.Stat (`stattech`) as .Stat Suite.

**Keep:** SDMX **dataflows**. **Drop:** observation cubes, Istat Data Browser hubs, and classic OECD.Stat (`stattech`) tenants.

## Istat Data Browser (`istatdatabrowser`) {#istatdatabrowser}

Filter exports on `software.id = 'istatdatabrowser'`. One harvest scope per public hub (IstatData, Coeweb, Sistan Hub, AstatData, IRIS, KNBS Open Data, INPS observatories as one catalog with several nodes).

```text
GET https://host/databrowserhub/api/core/hub/minimalInfo
GET https://host/databrowserhub/api/core/nodes
GET https://host/databrowserhub/api/core/nodes/{nodeId}/catalog
```

Some installs nest the API under `/databrowser/api/core/` (Astat, INPS) or a path prefix (`/coeweb/`, `/beta/`, `/DBrowser/`). Prefer `endpoints[]`. Each catalog item is an SDMX **dataflow**. Keep dataflow id + title + hub URL. Drop hub chrome, news, and dashboard pages. If the same office also has a public SDMX-RI `/SDMXWS/rest/dataflow` endpoint, harvest dataflows once — do not double-count the hub catalog and the NSI list.

**Keep:** Istat Data Browser **dataflows**. **Drop:** hub chrome, news, dashboards, and observation cubes.

**Drop** observation cubes unless the user asked for data files. Stop on `401`/`403`. Grain: [harvest-protocols.md](harvest-protocols.md#sdmx).

## Fusion Data Browser (`fusiondatabrowser`) {#fusiondatabrowser}

Filter exports on `software.id = 'fusiondatabrowser'`. One harvest scope per public browser (the UI at `/FusionDataBrowser/`). List SDMX **dataflows** from the attached Fusion Edge Server or Fusion Registry. Do not harvest a structural Fusion Registry (`fusionregistry`) that has no Data Browser UI.

```text
GET https://host/FusionEdgeServer/ws/public/sdmxapi/rest/dataflow/all/all/latest?detail=allstubs
GET https://host/FusionEdgeServer/sdmx/v2/
```

Some installs mount the API only under `/FusionEdgeServer/sdmx/v2/data/dataflow/`. Prefer `endpoints[]`. Keep dataflow id + name. Drop observation cubes, charts, and browser chrome unless the user asked for data files. Grain: [harvest-protocols.md](harvest-protocols.md#sdmx).

**Keep:** Fusion Data Browser **dataflows**. **Drop:** observation cubes, charts, and Fusion Registry structure-only installs.

## Swing (`swing`) {#swing}

ABF Research Swing Viewer / inCijfers databanks (`{city}.incijfers.be`, `provincies.incijfers.be`). Harvest **indicator tables / reports** from the public databank. Drop dashboard chrome, map tiles, and login-only Studio admin (`/Admin/Studio/`). One tenant = one harvest scope.

```text
GET https://host/databank
GET https://host/viewer/
```

Keep table/report identifiers + title + URL. Do not download full observation cubes unless the user asked for data files.

**Keep:** Swing **indicator tables / reports**. **Drop:** dashboard chrome, map tiles, and login-only Studio admin.

## Stat Technology (`stattech`) {#stattech}

Classic OECD.Stat / I.Stat UI (`stats.oecd.org`, `dati.istat.it`, and similar), not Data Explorer. Same SDMX **dataflow** grain as [.Stat Suite](#statsuite) when a public SDMX endpoint exists. Keep dataflows, not observation cubes. Do not harvest Data Explorer tenants as `stattech`.

**Keep:** SDMX **dataflows** when a public endpoint exists (same grain as .Stat Suite).
**Drop:** observation cubes and Data Explorer tenants (`statsuite`).

```text
GET https://host/restsdmx/sdmx.ashx/GetDataStructure/all
```


## Knoema (`knoema`) {#knoema}

Portal REST (`/api/1.0/` or `/api/3.0/`) lists **datasets** for that hub. Page the dataset catalog. Do not crawl every resource URL or the global knoema.com search. One portal = one harvest scope.

**Keep:** dataset catalog pages from portal REST (`/api/1.0/` or `/api/3.0/`).
**Drop:** every resource URL and the global knoema.com search.

```text
GET https://host/api/1.0/meta/dataset
```


## SparkMap (`sparkmap`) {#sparkmap}

Filter exports on `software.id = 'sparkmap'`. One harvest scope per public hub (SparkMap national, All Things state sites, hospital and Community Action hubs). Do not harvest CARES HQ Map Room as a second copy of SparkMap.

There is no anonymous layer-list API on the public Map Room. Harvest the hub’s public **Map Room data list** (layer catalog page or downloadable layer list) and public **community needs assessment / indicator reports**. Grain is the map layer or report, not a choropleth screenshot.

**Drop** saved user maps, login-only assessment builder sessions, SparkMap marketing and pricing pages, and paid API extracts unless the user asked for those files. Stop on `401`/`403`.

**Keep:** Map Room **layers** and public community-needs / indicator reports. **Drop:** saved user maps, login-only assessment builders, marketing pages, and paid API extracts.

## eDatos (`edatos`) {#edatos}

Filter exports on `software.id = 'edatos'`. One harvest scope per public hub.

```text
GET https://host/indicators/v1.0/indicators
```

Type `/indicators/v1.0/indicators` as `rest`. Keep **indicators** and **indicator systems** from that JSON-stat API (or the public ODS catalog listing). Drop institute CMS chrome and each time-series observation cube. ISTAC Open SDG is a different catalog (`opensdg`).

**Keep:** JSON-stat **indicators** and indicator systems. **Drop:** institute CMS chrome and time-series observation cubes.

## Idescat (`idescat`) {#idescat}

Filter exports on `software.id = 'idescat'`. One harvest scope per product family (tables, Emex, ODS).

```text
GET https://api.idescat.cat/emex/v1/nodes.json?lang=en
GET https://api.idescat.cat/taules/v2
```

Type the `api.idescat.cat` endpoints as `rest`. Keep indicator tables (`/taules/`) and municipal-profile indicators (`/emex/`) from the JSON / JSON-stat API. Drop the institute CMS pages and per-municipality HTML views.

**Keep:** indicator tables and Emex indicators via the API. **Drop:** CMS chrome and per-municipality HTML pages.

## INEbase (`inebase`) {#inebase}

Filter exports on `software.id = 'inebase'`. One harvest scope for the operations catalog.

```text
GET https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES
```

The Tempus3 API lists statistical operations; each operation expands to tables in the jaxiT3 browser (`/jaxiT3/`). Keep statistical operations and tables as the dataset grain. Drop INE website CMS pages, press releases, and the NSDP (separate catalog, `imfnsdp`).

**Keep:** statistical operations and tables (Tempus3 / jaxiT3). **Drop:** INE CMS chrome, press releases, NSDP pages.

## Cancer-Rates.info (`cancerrates`) {#cancerrates}

Filter exports on `software.id = 'cancerrates'`. There is no anonymous REST list API.

Keep the public **query UI** as the catalog (county incidence/mortality maps and tables). Grain for dataset harvest is a documented query (site × geography × year), not every map tile. Drop login-walled tenant paths and the KCR marketing/support pages.

**Keep:** the public **query UI** (documented site × geography × year queries). **Drop:** map tiles, login-walled tenant paths, and KCR marketing pages.

## Conduent Healthy Communities Institute (`hci`) {#hci}

Filter exports on `software.id = 'hci'`. One harvest scope per public community site.

Keep public **indicator** pages (and CSV downloads linked from indicator detail). Drop CHNA PDF report libraries as if they were the catalog, login-only assessment builders, and SparkMap sites.

**Keep:** public **indicator** pages (and linked CSV). **Drop:** CHNA PDF libraries as the catalog, login-only assessment builders, and SparkMap sites.

## Virtual LMI (`virtuallmi`) {#virtuallmi}

Filter exports on `software.id = 'virtuallmi'`. One harvest scope per state tenant.

Keep public **occupation / industry / area profile** tables the VLMI UI lists. Branded `/vosnet/` hosts (Colorado LMI Gateway) are the same grain. Drop job-board postings, case-management VOS modules, and state LMI sites that are not VLMI. Stop on `401`/`403`.

**Keep:** public occupation / industry / area **profile tables**. **Drop:** job-board postings, VOS case-management, and non-VLMI state LMI sites.

## Cascade CMS (`cascadecms`) {#cascadecms}

Filter exports on `software.id = 'cascadecms'`. One harvest scope per state portal.

There is no data API; pages are CMS-published HTML. Keep the public **indicator / data tables and publication pages** the portal lists (LAUS, QCEW, OEWS, projections, area profiles). Grain is the published table or report page, not each navigation or news item. Drop CMS chrome (news, carousel, contact pages) and embedded third-party dashboards (Tableau iframes) as separate records. Stop on `401`/`403`.

**Keep:** public indicator / data **tables and report pages**. **Drop:** CMS chrome, news items, and embedded third-party dashboards.

## CityViz (`cityviz`) {#cityviz}

Filter exports on `software.id = 'cityviz'`. One harvest scope per community tenant (custom domain or `*.cityviz.ca` host).

There is no anonymous list API. Keep the public **indicator datasets** the `/search` catalog lists (workforce, population, business counts, housing, real estate) and the **indicator dashboards / community profiles** they feed. Grain is the indicator dataset, not each chart, map tile, or generated Report Studio PDF/PPTX. Drop vendor marketing pages, the fictional Bellaville showcase tenant, login-gated tenants, and embed-only website widgets on municipal CMS pages. Stop on `401`/`403`.

```text
GET https://host/search
```

**Keep:** public **indicator datasets** from `/search` and community-profile dashboards. **Drop:** charts, map tiles, generated reports, marketing pages, and login-gated tenants.

## TerriSTORY (`terristory`) {#terristory}

Filter exports on `software.id = 'terristory'`. One harvest scope per regional hub (`terristory.fr/{region}`).

Keep public **indicators** and **thematic dashboards** the hub lists (energy, climate, air, mobility, socio-economic). Grain is the indicator or dashboard, not each commune polygon or scenario animation frame. Drop the national marketing home, login/admin, and other French observatories that are not TerriSTORY.

**Keep:** public **indicators** and thematic dashboards. **Drop:** commune polygons, scenario frames, national marketing, and login/admin.

## IHK-Fachkräftemonitor (`ihkfachkraeftemonitor`) {#ihkfachkraeftemonitor}

Filter exports on `software.id = 'ihkfachkraeftemonitor'`. One harvest scope per Land path.

There is no anonymous list API. Keep the public **occupation / industry / region** projection views the dashboard exposes. Drop the hub map page with no tenant, Arbeitsmarktradar Bayern, and IHK-Konjunkturboard. Stop on `401`/`403`.

**Keep:** public occupation / industry / region **projection views**. **Drop:** the hub map with no tenant, Arbeitsmarktradar Bayern, and IHK-Konjunkturboard.

## DUVA (`duva`) {#duva}

Filter exports on `software.id = 'duva'`. One harvest scope per public Informationsportal.

Keep **tables / evaluations** the Informationsportal tree lists (DUVA generates them on demand). Grain is the stored evaluation or table, not each map tile or PDF yearbook. Drop login-only DUVA admin, Urban Audit atlas hosts without `/Informationsportal/`, and open-data CKAN/CMS homes that only mention DUVA in the ETL backend.

```text
GET https://host/Informationsportal/
```

**Keep:** Informationsportal **tables / evaluations**. **Drop:** login-only DUVA admin, Urban Audit atlas hosts without `/Informationsportal/`, and CKAN/CMS homes that only mention DUVA.

## Géoclip (`geoclip`) {#geoclip}

Filter exports on `software.id = 'geoclip'`. One harvest scope per public observatory.

There is no anonymous list API. Keep the public **indicators / maps / territory reports** the observatory tree lists (`#c=indicator`, tables, charts). Grain is the indicator or report, not each commune polygon or exported PNG. Drop `geoclip.fr` marketing, login/admin, ANCT Observatoire des territoires open-data HTML, and the OCSTAT or Agreste CMS home when a dedicated Géoclip URL is registered.

**Keep:** public **indicators / maps / territory reports**. **Drop:** commune polygons, exported PNG, geoclip.fr marketing, and login/admin.

## GINES (`gines`) {#gines}

Filter exports on `software.id = 'gines'`. The public Bern atlas is the harvest scope. Login-only cantonal GINES tenants are out of scope.

Keep the **indicators and territorial views** the public atlas lists. Grain is the indicator, not each commune polygon or chart image. Drop the GINES login shell and `gines.ch` / `gines.biz` marketing. Discovery: [discovery-indicators.md](discovery-indicators.md#gines).

**Keep:** public atlas **indicators and territorial views**. **Drop:** login-only tenants, commune polygons, and product marketing.

## InstantAtlas (`instantatlas`) {#instantatlas}

Filter exports on `software.id = 'instantatlas'`. One harvest scope per public atlas/report.

There is no anonymous list API. Keep the **indicators / themes** the InstantAtlas™ report or Dashboard viewer lists. Grain is the indicator or theme, not each map polygon or exported PNG. Drop Esri UK Data Observatory WordPress homes (`esridataobservatory`), Dashboard Builder authoring, and GBE table trees that only embed an InstantAtlas Kreis map as an extra view.

**Keep:** InstantAtlas **indicators / themes**. **Drop:** map polygons, exported PNG, Esri UK Data Observatory WordPress homes, and Dashboard Builder authoring.

## MATS (`mats`) {#mats}

Filter exports on `software.id = 'mats'`. One harvest scope per Land MATS-Datenportal.

Keep public **dashboards and filterable tables** the Datenportal lists. Grain is the dashboard or table, not each filtered cell. Drop GENESIS-Online, SIS-Dashboards, and MATS FAQ/press HTML.

**Keep:** public **dashboards and filterable tables**. **Drop:** GENESIS-Online, SIS-Dashboards, and MATS FAQ/press HTML.

## Health Data Center (`hdc`) {#hdc}

Filter exports on `software.id = 'hdc'`. One harvest scope for the national `/center/public/` hub unless an official สสจ. tenant list appears.

Keep public **standard reports / indicators** the `/public/` catalog lists. Grain is the report or indicator, not each province cell, fiscal year, or 43-file upload. Drop Health KPI, DDC surveillance, login/admin, ThaiD registration, and guessed provincial `/slug/` homes as extra catalogs.

**Keep:** public **standard reports / indicators**. **Drop:** Health KPI, DDC apps, login/admin, and guessed provincial slugs.

## JAXI (`jaxi`) {#jaxi}

Filter exports on `software.id = 'jaxi'`. One harvest scope per JAXI tenant (IAEAxi, IBESTAT-JAXI).

There is no anonymous list API. Keep the public **PC-Axis tables** the `menu.do` tree lists. Grain is the table (`.px` / `tabla.do` / `Tabla.htm` file), not each selected cell or export format. Drop INEbase operations CMS pages, ibestat.es / eDatos homes, extra `nodeId=` theme URLs on the same tenant, and random INE `Tabla.htm` table IDs as extra catalogs.

**Keep:** JAXI **tables**. **Drop:** INEbase dyngs operations list, eDatos, institute CMS homes, and extra theme URLs on the same tenant.

## iMonitoring (`imonitoring`) {#imonitoring}

Filter exports on `software.id = 'imonitoring'`. One harvest scope per regional Open Budget portal (or the iminfin.ru hub).

Keep public **budget / socio-economic indicator views** and the open-data register the portal lists. Grain is the report, constructor cube, or dataset, not each municipality row or infographic frame. Drop the national comparison tree as extra catalogs, login/admin, and non-Krista open-budget CMS homes.

**Keep:** public **budget / socio-economic views** and listed open-data files. **Drop:** iminfin.ru region rows as separate catalogs, login/admin, and non-Krista open-budget CMS. Zabaykalsky and other EB/GZW portals are [KS Open Budget](#ksopenbudget).

## KS Open Budget (`ksopenbudget`) {#ksopenbudget}

Filter exports on `software.id = 'ksopenbudget'`. One harvest scope per regional or municipal finance portal.

Keep public **budget indicator pages** and the open-data register the portal lists (`/opendata/`, `list.csv`). Grain is the indicator table or dataset passport, not each municipality row or budget-law PDF.

**Keep:** budget indicator views and listed open-data files. **Drop:** news, login/admin, and iMonitoring (`ifinmon.ru`) portals.

```text
GET https://host/
GET https://host/opendata/
```

## SDMX-RI (`sdmxri`) {#sdmxri}

List dataflows from the NSI REST/SOAP endpoint in `endpoints[]` (`/rest/dataflow` or documented NSI path). Keep dataflows. Drop structure-only resources. If the human catalog is PxWeb/.Stat, harvest that UI’s table list instead of raw SOAP. REST grain: [harvest-protocols.md](harvest-protocols.md#sdmx).

**Keep:** dataflows from the NSI REST/SOAP endpoint in `endpoints[]`.
**Drop:** structure-only resources. If the human catalog is PxWeb/.Stat, harvest that table list instead.

```text
GET https://host/rest/dataflow
```


## GENESIS-Online (`genesisonline`) {#genesisonline}

Table **retrieval** is often POST-only. There is no reliable public GET “list all tables” API. Harvest the public research/catalog UI identifiers if documented; do not invent GET paths. Stop on login walls.

**Keep:** public table / research identifiers documented on the catalog UI.
**Drop:** POST-only retrieval sessions and login-walled cubes. Do not invent GET list paths.

```text
GET https://host/
```


## IBIS-PH (`ibisph`) {#ibisph}

Indicator pages and IBIS-Q query modules. Harvest public **indicator** home records (XML/HTML indicator ids). Skip query-builder sessions and PDF fact sheets as separate datasets.

**Keep:** public indicator home records (indicator ids in XML/HTML).
**Drop:** IBIS-Q query-builder sessions and PDF fact sheets as extra datasets.

```text
GET https://host/indicator/index/alphabetical
```


## Envista Web (`envista`) {#envista}

Filter exports on `software.id = 'envista'`. Public station map and report downloads. The session API (`POST /Account/GetApiFromBackToken`, then `POST /api`) is not a GET list.

```text
GET https://host/
```

**Keep:** monitoring stations and published report files. **Drop:** hourly measurement rows, guest session tokens, and the admin Web Manager. One agency network = one harvest scope. Stop on `401`/`403`.

## Fingertips (`fingertips`) {#fingertips}

Filter exports on `software.id = 'fingertips'`. One harvest scope for the national England hub.

`GET /api` is HTML documentation. List **profiles** (then indicators inside a profile) from `/api/profiles`. Grain is the profile or indicator, not each area value.

**Keep:** Fingertips **profiles / indicators**.
**Drop:** per-local-authority area values as extra datasets, IBIS-PH, Power BI embeds, and InstantAtlas reports.

```text
GET https://fingertips.phe.org.uk/api/profiles
```

## Nomis (`nomis`) {#nomis}

Filter exports on `software.id = 'nomis'`. One harvest scope for the national UK hub. API help: [www.nomisweb.co.uk/api/v01/help](https://www.nomisweb.co.uk/api/v01/help).

List datasets from the SDMX-JSON dataset definition endpoint; each `keyfamily` is one dataset. Grain is the dataset, not each geography or time value.

```text
GET https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json
```

**Keep:** Nomis **datasets** (keyfamilies). **Drop:** per-geography or per-time-series extractions as extra datasets, the ONS website (ons.gov.uk), and third-party dashboards embedding Nomis tables.

## StatsWales (`statswales`) {#statswales}

Filter exports on `software.id = 'statswales'`. One harvest scope for the national Welsh hub. API docs (OAS 3.1): [api.stats.gov.wales](https://api.stats.gov.wales/v1/docs/).

The API root returns the published dataset list as JSON `data` (id, title, first_published_at, last_updated_at); `/topic` returns the bilingual topic tree. Grain is the dataset, not each dimension value.

```text
GET https://api.stats.gov.wales/v1/
GET https://api.stats.gov.wales/v1/topic
```

**Keep:** StatsWales **datasets**. **Drop:** per-dimension filtered views as extra datasets and the retired `open.statswales.gov.wales` OData endpoints (shut down August 2024).

## DHIS2 (`dhis2`) {#dhis2}

National HMIS / public health indicator portals. Filter exports on `software.id = 'dhis2'`.

```text
GET https://host/api/system/info
GET https://host/api/dataSets.json?fields=id,displayName&pageSize=50
GET https://host/api/indicators.json?fields=id,displayName&pageSize=50
```

Keep **data sets** and public **indicators**. Drop user accounts, org-unit trees as datasets, and login-only analytics. Stop on `401`/`403`. Many ministries expose no anonymous API — then harvest only the public portal’s documented indicator list. Skip dhis2.org marketing.

**Keep:** DHIS2 **data sets** and public **indicators**. **Drop:** user accounts, org-unit trees as datasets, and login-only analytics.

## ActivityInfo (`activityinfo`) {#activityinfo}

Humanitarian 4W/5W response-monitoring dashboards on the hosted ActivityInfo SaaS. Filter exports on `software.id = 'activityinfo'`.

Two surfaces per catalog record:

- **Published report pages** on `activityinfo.org`: the standalone published page is public, but the reports API (`GET https://www.activityinfo.org/resources/reports/{reportId}/published`) requires an API token. Harvest the tables/charts exposed on the published page itself; there is no public directory of databases to enumerate.
- **API-fed portals** (R4V Activity Explorer, OCHA Ukraine response dashboards): harvest the front-end's public downloads (CSV/XLSX) or the documented HDX mirror dataset. The ActivityInfo backend requires authentication — do not probe it.

Grain: one published dashboard/report ≈ one dataset analog; keep 5W activity tables (partner, sector, location, people reached, funding requirements). Drop login-gated databases, partner contact lists, and record-level beneficiary data. Stop on `401`/`403`.

**Keep:** published 5W/indicator tables and public dashboard downloads. **Drop:** login-only databases, user/partner directories, record-level beneficiary data.

## TabNet (`tabnet`) {#tabnet}

Brazilian DATASUS CGI tabulators. Filter exports on `software.id = 'tabnet'`. There is no REST list API.

Keep each public **`.def` table** (query form) as one dataset analog: title from the form heading, URL the `deftohtm.exe` / `cgi-bin/dh?` / `tabcgi.exe` link. Harvest from the installation’s table menu (HTML index), not by guessing `.def` paths.

**Drop** CGI `Mostre` query results, `Copia para Tabwin` files, CSV cell dumps, TabWin desktop packages, and every `.def` on `tabnet.datasus.gov.br` when harvesting the national catalog already listed from the DATASUS TabNet landing page. One harvest scope per installation (national, SES, municipal, ANS). Stop on `401`/`403`.

**Keep:** each public **`.def` table** (query form). **Drop:** CGI `Mostre` results, TabWin files, CSV cell dumps, and every `.def` on the national landing when harvesting that catalog.

## SIDRA (`sidra`) {#sidra}

Filter exports on `software.id = 'sidra'`. One harvest scope for the IBGE SIDRA hub.

List **aggregates / tables** from the IBGE servicodados API (JSON, often gzip). Grain is the aggregate (table), not each observation cell or territorial breakdown. Detection uses that API host (`absolute_url`); do not concatenate `/api/v3/agregados` onto `sidra.ibge.gov.br`.

**Keep:** SIDRA **aggregates / tables**.
**Drop:** IBGE Cidades@, Ipeadata, Comex Stat, BCB SGS, and DATASUS TabNet.

```text
GET https://servicodados.ibge.gov.br/api/v3/agregados
```

Type that URL as `sidra:agregados`.

## FENIX (`fenix`) {#fenix}

Filter exports on `software.id = 'fenix'`. One harvest scope per public FENIX app (FAOSTAT, AMIS, AIDmonitor, DAD-IS, WIEWS, GIFT), not per CountrySTAT dataset dumped into FAO CKAN.

FAOSTAT list:

```text
GET https://fenixservices.fao.org/faostat/api/v1/en/groupsanddomains
```

Keep **domains / datasets** from that JSON. Observation queries (`/faostat/api/v1/{lang}/data/{domain}`) are not new catalogs. Prefer `endpoints[]` on the FAOSTAT record. Other FENIX UIs often have no anonymous list API — harvest the public dataset/indicator list from the UI, then stop. Skip dead `countrystat.org` hosts and GitHub UI repos.

**Keep:** FENIX **domains / datasets** (FAOSTAT groupsanddomains or the public UI list). **Drop:** observation cubes, dead CountrySTAT hosts, and GitHub UI repos.

## FPMA Tool (`fpmatool`) {#fpmatool}

FAO GIEWS food-price dashboards; global instance at `fpma.fao.org/giews/fpmat4/global/` plus national instances. No anonymous list API — harvest the public indicator/series list from the UI selectors, then stop.

**Keep:** monthly price **series** by country, market, and commodity (the indicator grain). **Drop:** chart images, GIEWS report PDFs, and aggregate map layers. One country instance = one harvest scope; do not merge the global instance with national ones.

## Global Cancer Observatory (`gco`) {#gco}

IARC/WHO cancer indicators (Cancer Today / Tomorrow / Over Time on gco.iarc.fr and gco.iarc.who.int). No anonymous list API — harvest the public indicator table for the chosen scope from the UI, then stop.

**Keep:** GLOBOCAN **indicator series** (incidence, mortality, prevalence) by country, cancer type, age, sex. **Drop:** fact-sheet PDFs, methodology notes, and per-cancer infographic pages. One GCO tool scope = one harvest scope.

## BRS Electronic Reporting System Dashboards (`brsers`) {#brsers}

Basel/Stockholm convention national-report dashboards (`/eRSodataReports2/...DashBoard.html`). No public API — harvest the dashboard table for the selected filters or the Excel export.

**Keep:** national-report **indicator rows** by party, year, and report section. **Drop:** convention text pages and meeting documents. One convention dashboard = one harvest scope.

## DataWarehousePro (`datawarehousepro`) {#datawarehousepro}

```text
GET https://app.datawarehousepro.com/guest/getDatabanksWithMnemonics/{tenant}
GET https://app.datawarehousepro.com/guest/export/{tenant}
```

Keep **databanks / series catalogs** for that tenant. Drop admin paste-from-Excel UI and other tenants on the same host. One portal = one harvest scope.

**Keep:** tenant **databanks / series catalogs**. **Drop:** admin paste-from-Excel UI and other tenants on the same host.

## LiveShop (`liveshop`) {#liveshop}

The `/shop` sector/category/table tree plus the `/data-browser` views are the catalog. There is no verified anonymous list API — stop rather than scraping every chart. Drop `/shop/meta-data` definitions prose and `/shop/data-calendar` schedule pages as catalog records, but use them to confirm the platform. One institutional tenant = one harvest scope.

**Keep:** **sector / category / table** time-series entries listed under `/shop` and rendered in `/data-browser`.
**Drop:** meta-data definitions prose, data-calendar pages, and country-profile marketing pages.

```text
GET https://host/shop
```

## IMF National Summary Data Page (`imfnsdp`) {#imfnsdp}

The NSDP HTML page is the catalog. Follow the SDMX 2.0 XML (and CSV where published) links for each **category / series**. Drop the IMF DSBB directory, the NSO homepage, and Knoema/WordPress wrappers (harvest those as `knoema` / `wordpress`). One country page = one harvest scope.

**Keep:** SDMX 2.0 XML (and CSV) **category / series** linked from the NSDP page.
**Drop:** IMF DSBB directory, NSO homepage, and Knoema/WordPress wrappers.

```text
GET https://host/
```


## Goal Tracker (`goaltracker`) {#goaltracker}

Harvest public **indicator / goal** pages the country tenant lists. Drop About/marketing HTML. There is no verified anonymous list API on every tenant — stop rather than scraping every visualization. Distinct from [Open SDG](#opensdg).

**Keep:** public indicator / goal pages the country tenant lists.
**Drop:** About/marketing HTML. Stop rather than scraping every visualization. Distinct from Open SDG.

```text
GET https://host/
```


## NADA (`nada`) {#nada}

Survey microdata catalog.

```text
GET https://host/index.php/api/catalog/search
```

Typical catalog links already end in `/index.php` or `/index.php/catalog`. Cleanup strips `/index.php` (keeping any path prefix) so the search API attaches at origin and is not doubled.

Page the JSON study list. Keep survey / microdata / geospatial studies. **Drop** `dtype` values that are document, video, or news when present. CSV export (`/index.php/catalog/export/csv`) is a bulk study list — still one row per study, not per file.

**Keep:** NADA survey / microdata / geospatial **studies**.

**Drop:** `dtype` document, video, or news hits; still one row per study, not per file.

## IPUMS (`ipums`) {#ipums}

Filter exports on `software.id = 'ipums'`. One harvest scope per **collection** (USA, International, CPS, …). Use the IPUMS API metadata endpoints ([developer.ipums.org](https://developer.ipums.org)) with the collection name.

**Keep:** samples / datasets in that collection. **Drop:** completed extract files, variable codebooks as separate catalogs, and the IPUMS marketing homepage. Do not download person-level microdata.

## NESSTAR (`nesstar`) {#nesstar}

```text
GET https://host/webview/
GET https://host/api
```

Harvest the **study** list in WebView. Many instances are dead — skip `401`/`404`. Do not scrape the vendor site.

**Keep:** NESSTAR **studies**. **Drop:** vendor marketing and dead `401`/`404` hosts.

## REDATAM (`redatam`) {#redatam}

```text
GET https://host/redbin/RpWebEngine.exe/Portal
```

HTML census/survey portals with little REST. Harvest the published **database/project** names from the portal home. Do not run interactive tabulations as a crawl.

**Keep:** published REDATAM **database/project** names. **Drop:** interactive tabulation sessions.

## Colectica (`colectica`) {#colectica}

DDI repository. Public probe is often `/swagger/ui` or `/swagger/v1/swagger.json`. Search may be POST and/or authenticated — stop on `401`. Harvest **StudyUnit** / dataset items when a public API exists, not every DDI fragment (variables, questions) as a dataset.

**Keep:** StudyUnit / dataset items from a public API.
**Drop:** DDI fragments (variables, questions) as separate datasets; login-only stewardship UIs.

```text
GET https://host/swagger/v1/swagger.json
```


## OBiBa Mica (`obibamica`) {#obibamica}

```text
GET https://host/studies
GET https://host/api/studies
```

Keep studies and Mica **datasets**. Drop networks, persons, and collected-dataset-empty shells. Docs: [micadoc.obiba.org](https://micadoc.obiba.org/en/latest/rest/).

**Keep:** Mica **studies** and datasets. **Drop:** networks, persons, and empty collected-dataset shells.

## Survey Solutions (`surveysolutions`) {#surveysolutions}

Headquarters survey catalogs are often login-only. Harvest only a **public** questionnaire/data listing. Stop on `401`.

**Keep:** a **public** questionnaire/data listing only.
**Drop:** Headquarters interviewer hosts and login-only catalogs. Stop on `401`.

```text
GET https://host/
```


## SuperSTAR (`superstar`) {#superstar}

Census and official SuperWEB2 table-builder catalogs. Harvest the published **table / database** list from the SuperWEB2 catalogue or Open Data API (`/webapi/rest/v1/schema`), not every cube cell. Skip vendor demos, marketing, and login-only staff builders.

```text
GET https://host/webapi/rest/v1/schema
```

**Keep:** published SuperWEB2 **table / database** list. **Drop:** every cube cell, vendor demos, and login-only staff builders.

## Beyond 20/20 Web Data Server (`beyond2020`) {#beyond2020}

Filter exports on `software.id = 'beyond2020'`. There is no public REST catalog API.

Keep each public **report** (cube) listed under `ReportFolders/reportFolders.aspx` as one dataset analog: title from the report name, URL the `TableViewer/tableView.aspx?ReportId=` link. Walk the folder tree on that installation only.

**Drop** language-selection pages, `TableViewer` cell extracts, IVT/Excel/CSV downloads as separate catalogs, Crime Insight tenants, login WDS, and every `ReportId` on `www.jodidb.org` / `difusion.jccm.es` when harvesting the installation already registered as a catalog. One harvest scope per WDS host. Stop on `401`/`403`.

```text
GET https://host/ReportFolders/reportFolders.aspx
```

**Keep:** each public **report / cube** (`TableViewer` ReportId). **Drop:** language-selection pages, cell extracts, IVT/Excel/CSV as extra catalogs, and login WDS.

## Official international hubs {#official-international-hubs}

These `software.id` values are **one registered catalog each**. Harvest **contents** when the user asked for that hub. Do not add them again as new registry YAML.

Grain is still **dataflow / indicator**, not observation cells. SDMX protocol: [harvest-protocols.md](harvest-protocols.md#sdmx). Prefer `endpoints[]` on the live record when present.

## Eurostat (`eurostat`) {#eurostat}

Each **dataflow** is one dataset analog. The registered observation URL (`/api/dissemination/statistics/1.0/data`) is **not** a catalog list — do not page cubes as datasets.

**Keep:** SDMX **dataflows**.
**Drop:** observation cubes (`/statistics/1.0/data`).

```text
GET https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/all/latest
```

## ECB (`ecb`) {#ecb}

List **dataflows**. The UI host `data.ecb.europa.eu` is not the SDMX root; `/service/data` is observations. The registered observation endpoint is not a catalog list.

**Keep:** SDMX **dataflows**.
**Drop:** `/service/data` observation cubes.

```text
GET https://data-api.ecb.europa.eu/service/dataflow
```

Detection uses that API host (`absolute_url`); do not concatenate `/service/dataflow` onto `data.ecb.europa.eu`.


## World Bank (`dataworldbankorg`) {#dataworldbankorg}

```text
GET https://api.worldbank.org/v2/indicator?format=json&per_page=1000
GET https://api.worldbank.org/v2/sources?format=json
```

Keep **indicators** (or **sources** if the user asked for catalogs-of-catalogs). Drop country pages, WDI observation queries (`/v2/country/.../indicator/...`), and data.worldbank.org marketing.

**Keep:** World Bank **indicators** (or **sources** if asked). **Drop:** country pages, WDI observation queries, and marketing.

Detection probes the documented API host (`https://api.worldbank.org/v2/indicator` and `/v2/sources`), not paths on `data.worldbank.org`.

## WHO GHO (`whoint`) {#whoint}

```text
GET https://ghoapi.azureedge.net/api/Indicator
```

Keep **indicators**. Drop Dimension / country lists and every GHO observation row.

**Keep:** GHO **indicators**. **Drop:** Dimension / country lists and every observation row.

## ILOSTAT (`ilostat`) {#ilostat}

```text
GET https://sdmx.ilo.org/rest/dataflow
```

Keep **dataflows**. `www.ilo.org/sdmx/` is often Cloudflare-blocked from scripts — use `sdmx.ilo.org`. Drop ilostat.ilo.org article pages.

Detection uses that SDMX host (`absolute_url`); do not concatenate `/rest/dataflow` onto ilostat.ilo.org.

**Keep:** ILOSTAT SDMX **dataflows**. **Drop:** ilostat.ilo.org article pages.

## BIS (`databisorg`) {#databisorg}

```text
GET https://stats.bis.org/api/v1/dataflow
```

Keep SDMX **dataflows**. The registered `https://data.bis.org/api/v0/search` is **POST** (not a GET list) and is not a dataset catalog. Drop help HTML and observation queries.

Detection uses the stats.bis.org API host (`absolute_url`); do not concatenate `/api/v1/dataflow` onto `data.bis.org`.

**Keep:** BIS SDMX **dataflows**. **Drop:** help HTML, POST search, and observation queries.

## UNICEF (`datauniceforg`) {#datauniceforg}

```text
GET https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow
```

Keep **dataflows**. Do not treat every country profile on data.unicef.org as a dataset. The HTML site may be Cloudflare-blocked; SDMX is the harvest.

Detection uses the SDMX API host (`absolute_url`); do not concatenate `/ws/public/sdmxapi/rest/dataflow` onto data.unicef.org.

**Keep:** UNICEF SDMX **dataflows**. **Drop:** every country profile on data.unicef.org as a dataset.

## UNdata (`undata`) {#undata}

Filter exports on `software.id = 'undata'`. One registered catalog for data.un.org.

List from OpenSearch (already on the catalog record). Grain is the **series / table**, not observation cells. Drop the SDG Global Database and Comtrade Plus as extra catalogs of this hub — those are separate registered products.

**Keep:** UNdata **series / tables**.
**Drop:** SDG Global Database, Comtrade Plus, and every observation cell.

```text
GET https://data.un.org/OpenSearch.xml
```

## UN Comtrade Plus (`comtradeplus`) {#comtradeplus}

Filter exports on `software.id = 'comtradeplus'`. One registered catalog for comtradeplus.un.org.

The data API lives on `comtradeapi.un.org` and needs a subscription key. Do not concatenate `/api` onto the UI host. Grain is the **trade dataset / flow** the Plus UI lists, not each reporter-partner-year cell. Distinct from WITS and UNdata.

**Keep:** Comtrade Plus **trade datasets / flows**.
**Drop:** UI chrome, WITS, UNdata series, and key-gated API observation dumps as extra catalogs.

```text
GET https://comtradeplus.un.org/
```

## Our World in Data (`ourworldindata`) {#ourworldindata}

Filter exports on `software.id = 'ourworldindata'`. One registered catalog for ourworldindata.org.

There is no relative list API on the catalog link. Harvest **indicator / chart topics** from the public sitemap or charts index. Grain is the indicator topic, not every chart URL or Grapher query. Distinct from Gapminder WordPress data-download pages.

**Keep:** OWID **indicator / chart topics**.
**Drop:** every chart URL as its own dataset, Grapher query strings, and Gapminder WordPress pages.

```text
GET https://ourworldindata.org/sitemap.xml
```

## StatPlanet (`statplanet`) {#statplanet}

Public StatPlanet Cloud / HTML5 **indicator explorer**. Grain is the **indicator** (row in `data.csv` / Cloud indicator list), not every map animation frame.

```text
GET https://host/.../data.csv
GET https://host/.../settings.csv
```

Keep named indicators the dashboard can select. One catalog per host/explorer — do not harvest each `*-StatTrends.html` layout as a separate catalog. Drop vendor demos on statsilk.com, Flash SWF-only pages, and viewers that only chart another registered catalog (World Bank Open Data API). Stop on `401`/`403`. CSV is the list; do not scrape tiles.

**Keep:** named **indicators** in `data.csv` / the Cloud indicator list. **Drop:** vendor demos, Flash SWF-only pages, and tiles.

## Oracle APEX (`oracleapex`) {#oracleapex}

Public statistical **apps** that list indicators or tables. Harvest the documented public REST/ORDS feed if it returns a dataset list. Skip generic APEX sites, login builders, and `/apex/f?p=` session URLs as identifiers.

**Keep:** documented public REST/ORDS **dataset / table lists**. **Drop:** generic APEX sites, login builders, and `/apex/f?p=` session URLs as identifiers.

## Apache Superset (`superset`) {#superset}

Public BI that sometimes **is** the indicator catalog. Harvest public **datasets** / charts the catalog documents. Drop internal dashboards and login-only `/superset/dashboard/`. Stop on `401`. Do not scrape every dashboard tile.

**Keep:** public datasets / charts the catalog documents.
**Drop:** internal dashboards and login-only `/superset/dashboard/`. Stop on `401`.

```text
GET https://host/api/v1/dataset/
```

Type `/api/v1/dataset/` as `rest`.

## IBM Cognos (`ibmcognos`) {#ibmcognos}

Harvest published **packages / reports** that are statistical tables. Drop intranet Cognos. Stop on `401`.

**Keep:** published packages / reports that are statistical tables.
**Drop:** intranet Cognos. Stop on `401`.

```text
GET https://host/ibmcognos/bi/
```


## Microsoft Power BI (`powerbi`) {#powerbi}

Embedded `app.powerbi.com/view?r=…` dashboards have **no list API**. Harvest the surrounding page's documented downloads/Excel files if offered; otherwise record-only. Drop anonymous embed URLs as identifiers (per-view tokens rotate). Stop on `401`.

**Keep:** documented downloads/Excel on the surrounding page if offered.
**Drop:** anonymous `app.powerbi.com/view?r=` embeds as identifiers (tokens rotate). Stop on `401`.


## Tableau (`tableau`) {#tableau}

Tableau Public/Server vizzes are per-visualization, not a catalog. Harvest the parent statistics page's documented data downloads (CSV crosstabs on the viz are per-chart exports). One parent record per portal — do not enumerate each viz. Drop login-only Tableau Server.

**Keep:** documented data downloads on the parent statistics page.
**Drop:** each viz as a dataset; login-only Tableau Server. One parent record per portal.


## Microsoft SharePoint (`sharepoint`) {#sharepoint}

SharePoint statistics and open-data pages publish documents/lists, not dataset records. Harvest documented Excel/CSV **files** the page links (statistics tables, data dictionaries, open-data downloads). Drop `Authenticate.aspx`, `/_vti_bin/`, and any login wall. Stop on `401`.

**Keep:** documented Excel/CSV files the statistics page links.
**Drop:** `Authenticate.aspx`, `/_vti_bin/`, and login walls. Stop on `401`.


## TYPO3 (`typo3`) {#typo3}

TYPO3 statistics pages publish documents/content elements, not dataset records. Harvest documented Excel/CSV **files** the page links (statistics tables, indicator downloads). Drop login-only intranet sections.

**Keep:** documented Excel/CSV files the statistics page links.
**Drop:** login-only sections; pages that only link to an external data platform.


## SPIP (`spip`) {#spip}

SPIP statistics pages publish articles/documents, not dataset records. Harvest documented Excel/CSV **files** the page links (indicator tables, observatory downloads).

**Keep:** documented Excel/CSV files the statistics page links.
**Drop:** article-only pages with no data files.


## Contao (`contao`) {#contao}

Contao statistics pages publish documents/content elements, not dataset records. Harvest documented Excel/CSV **files** the page links (statistics tables, indicator downloads).

**Keep:** documented Excel/CSV files the statistics page links.
**Drop:** pages that only link to an external data platform.


## R Shiny (`shiny`) {#shiny}

Shiny apps are bespoke UIs; there is no platform API. Harvest documented downloads or stable app endpoints only if they return data lists. One record per app. Skip scraping every reactive widget.

**Keep:** documented downloads or stable endpoints that return data lists.
**Drop:** scraping every reactive widget. One record per app.


## Qlik Sense (`qlik`) {#qlik}

Qlik hubs expose dashboards, not a dataset catalog. Harvest documented exports on the portal page. Drop `resources/autogenerated` assets, single-extension mashups, and login-only hubs. Stop on `401`.

**Keep:** documented exports on the portal page.
**Drop:** `resources/autogenerated` assets, single-extension mashups, and login-only hubs. Stop on `401`.


## BI Contour (`bicontour`) {#bicontour}

Public Contour BI **indicator / report catalog**. Keep listed indicators or published reports. Drop viewer-only map frames and intranet Contour. Stop on `401`/`403`.

**Keep:** listed indicators or published reports. **Drop:** viewer-only map frames and intranet Contour.

## Data Insight (`datainsight`) {#datainsight}

Harvest only a **public** insight dataset list. Drop Veritas enterprise consoles and internal BI. Stop on `401`/`403`. Public catalogs are rare — if the UI is login-only, do not harvest.

**Keep:** a public insight **dataset list**. **Drop:** Veritas enterprise consoles and internal BI.

## Data VAVT (`datavavt`) {#datavavt}

```text
GET https://data.vavt.ru/
```

Keep **public indicator tables**. Drop intranet VA/VT copies and login-only analysis workspaces. Stop on `401`/`403`.

**Keep:** public VAVT **indicator tables**. **Drop:** intranet VA/VT copies and login-only analysis workspaces.

## Other indicator IDs

| `software.id` | Harvest | Skip |
|---------------|---------|------|
| `statplanet` | see above | Vendor demos; World Bank viewers |
| `datavavt` | see above | Intranet |
| `bicontour` | see above | Viewer-only |
| `datainsight` | see above | Internal BI |

## GeCO-sys OpenData (`gecoopendata`) {#gecoopendata}

Italian cancer-registry indicator tenants on `gecoopendata.{registry-domain}`. One harvest
scope per registry. Indicator pages (`/incidenza.php`, `/sopravvivenza.php`, also under
`/web/`) are interactive calculation forms; there is no documented public list API.

**Keep:** each **indicator calculation view** (incidence, mortality, survival, prevalence,
data quality) as one dataset analog, with territory/sex/age breakdowns noted in metadata.
**Drop:** the form chrome, chart images, and session-bound query results. Do not harvest the
registry's editorial pages.

## Grafana (`grafana`) {#grafana}

Anonymous-access Grafana instances only (registry entries already require it). List dashboards
from the HTTP API; grain is the **dashboard**, not each panel or time series.

**Keep:** each public **dashboard** (`/api/search` items with `type: dash-db`) as one dataset
analog; folders (`dash-folder`) are topics, not datasets.
**Drop:** panels, snapshots, playlists, alert rules, and data-source proxies as separate
datasets. Never attempt authenticated API access — `401` on `/api/search` means the instance
is out of scope.

```text
GET https://host/api/search?limit=5000
GET https://host/api/dashboards/uid/{uid}
```

## EPS Data Platform (`epsdata`) {#epsdata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database/indicator list pages and free sample tables; grain is the statistical table or indicator series.
**Drop:** subscription-gated series values, institutional login sessions, and marketing pages.


## CNKI Economic and Social Big Data Research Platform (`cnkidata`) {#cnkidata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public yearbook/indicator catalog pages; grain is the statistical yearbook or indicator table.
**Drop:** paywalled table values, CNKI literature search results, and user account pages.


## CEInet Statistical Database (`ceinet`) {#ceinet}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator navigation and free series metadata; grain is the indicator series.
**Drop:** subscription-gated series values and the two hosts as duplicate scopes — register `db.cei.cn` and `ceidata.cei.cn` as separate catalogs of the same software.


## DRCNet Statistical Database (`drcnet`) {#drcnet}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database/indicator catalog pages; grain is the statistical table.
**Drop:** subscription-gated series values and DRCNet report full texts.


## Soshoo (`soshoo`) {#soshoo}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public statistical-table catalog pages; grain is the statistical table.
**Drop:** subscription-gated table values and China InfoBank news databases.


## MacroChina Database (`macrochina`) {#macrochina}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database introduction and indicator list pages; grain is the indicator series.
**Drop:** subscription-gated series values and the JS-redirect stub page itself.


## Pishu Database (`pishu`) {#pishu}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public yearbook/report catalog pages; grain is the blue-book volume or statistical table.
**Drop:** paywalled full texts and Social Sciences Academic Press bookshop pages.


## Wind Economic Database (`wind`) {#wind}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public EDB product/indicator documentation pages; grain is the documented indicator series.
**Drop:** terminal-only downloads, paid API extracts, and marketing pages.


## CEIC Data (`ceic`) {#ceic}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator pages (`/en/indicator/...`); grain is the indicator series.
**Drop:** subscription-gated full history, paid API extracts, and sales pages.


## CSMAR (`csmar`) {#csmar}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database/module catalog pages; grain is the research database module.
**Drop:** subscription-gated table values and the vendor marketing site as a separate catalog.


## RESSET (`resset`) {#resset}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database product list; grain is the research database.
**Drop:** subscription-gated series values and login pages.


## East Money Data Center (`eastmoneydata`) {#eastmoneydata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator tables (macro, market, company); grain is the indicator table.
**Drop:** news articles, quote pages, and the separate Choice terminal.


## East Money Choice (`choice`) {#choice}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public product/indicator documentation; grain is the documented indicator series.
**Drop:** terminal-only data, paid API extracts, and the free `data.eastmoney.com` portal (separate catalog).


## Tonghuashun Data Center (`thsdata`) {#thsdata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator tables; grain is the indicator table.
**Drop:** news articles, quote pages, and the separate iFinD terminal.


## Tonghuashun iFinD (`ifind`) {#ifind}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public product/indicator documentation; grain is the documented indicator series.
**Drop:** terminal-only data and the free `data.10jqka.com.cn` portal (separate catalog).


## Gildata (`gildata`) {#gildata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database product list; grain is the database product.
**Drop:** subscription-gated series values and Hundsun corporate pages.


## Go-Goal (`gogoal`) {#gogoal}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public product/database pages; grain is the database product.
**Drop:** subscription-gated estimates data and marketing pages.


## CNRDS (`cnrds`) {#cnrds}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public database module catalog; grain is the research database module.
**Drop:** subscription-gated table values and paper-citation pages.


## DataYes (`datayes`) {#datayes}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator and research navigation; grain is the indicator series.
**Drop:** subscription-gated data, quant tool sessions, and marketing pages.


## Qianzhan Database (`qianzhan`) {#qianzhan}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator tables; grain is the indicator series.
**Drop:** paid report pages on the main `qianzhan.com` site.


## AskCI (`askci`) {#askci}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public industry statistics pages; grain is the industry indicator table.
**Drop:** paid report pages and consulting service pages.


## Huaon (`huaon`) {#huaon}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public industry statistics pages; grain is the industry indicator table.
**Drop:** paid report pages and consulting service pages.


## Chyxx (`chyxx`) {#chyxx}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public industry statistics pages; grain is the industry indicator table.
**Drop:** paid report pages and consulting service pages.


## ChinaBgao (`chinabgao`) {#chinabgao}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public report catalog and free indicator pages; grain is the report or indicator table.
**Drop:** paid report full texts and ordering pages.


## Bosidata (`bosidata`) {#bosidata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public market data pages; grain is the indicator table.
**Drop:** paid report full texts and consulting pages.


## LeadLeo (`leadleo`) {#leadleo}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public industry indicator dashboards and report catalog; grain is the indicator dashboard.
**Drop:** paid report full texts and analyst service pages.


## iiMedia Data Center (`iimedia`) {#iimedia}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator catalog pages; grain is the indicator series.
**Drop:** subscription-gated series values and iiMedia report shop pages.


## Analysys (`analysys`) {#analysys}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator articles and data pages; grain is the indicator series.
**Drop:** paid analytics products and consulting pages.


## iResearch (`iresearch`) {#iresearch}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public indicator reports and data charts; grain is the indicator series.
**Drop:** paid report full texts and consulting pages.


## QuestMobile (`questmobile`) {#questmobile}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public metrics catalog pages; grain is the app metric series.
**Drop:** subscription-gated metric values and demo login pages.


## Baidu Index (`baiduindex`) {#baiduindex}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public product pages and published index reports; grain is the keyword index series.
**Drop:** login-only query sessions and Baidu marketing pages.


## Ocean Engine TrendInsight (`oceaninsight`) {#oceaninsight}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public trend indicator pages and published reports; grain is the trend indicator series.
**Drop:** advertiser-only dashboards and Ocean Engine ad platform pages.


## GSData (`gsdata`) {#gsdata}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public ranking lists and product pages; grain is the account metric series.
**Drop:** subscription-gated metrics and Qingbo marketing pages.


## NewRank (`newrank`) {#newrank}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public account rankings and metric pages; grain is the account metric series.
**Drop:** subscription-gated metrics and NewRank marketing pages.


## Qimai (`qimai`) {#qimai}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public app rankings and ASO indicator pages; grain is the app metric series.
**Drop:** subscription-gated historical metrics and account pages.


## Diandian (`diandian`) {#diandian}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public app rankings and market indicator pages; grain is the app metric series.
**Drop:** subscription-gated historical metrics and account pages.


## Chanmama (`chanmama`) {#chanmama}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public metric/ranking pages; grain is the product or livestream metric series.
**Drop:** subscription-gated metrics and account pages.


## Feigua (`feigua`) {#feigua}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public metric/ranking pages; grain is the account or product metric series.
**Drop:** subscription-gated metrics and account pages.


## Sunsirs (100ppi) (`sunsirs`) {#sunsirs}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public commodity price index pages; grain is the commodity price series.
**Drop:** paid data services and Sunsirs corporate pages.


## Mysteel (`mysteel`) {#mysteel}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public price index pages; grain is the price series.
**Drop:** subscription-gated series values and Mysteel corporate pages.


## SCI99 (`sci99`) {#sci99}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public price index pages; grain is the price series.
**Drop:** subscription-gated series values and Zhuochuang corporate pages.


## Oilchem (`oilchem`) {#oilchem}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public price index pages; grain is the price series.
**Drop:** subscription-gated series values and Longzhong corporate pages.


## Jinlianchuang (315i) (`jinlianchuang`) {#jinlianchuang}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public price index pages; grain is the price series.
**Drop:** subscription-gated series values and corporate pages.


## Baiinfo (`baiinfo`) {#baiinfo}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public price index pages; grain is the price series.
**Drop:** subscription-gated series values and corporate pages.


## Sxcoal (`sxcoal`) {#sxcoal}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public coal price index pages; grain is the price series.
**Drop:** subscription-gated series values and Fenwei corporate pages.


## China Data Online (`chinadataonline`) {#chinadataonline}

Vendor-hosted indicator platform; one harvest scope per registered instance. No anonymous list API is documented — harvest the public HTML indicator catalog.

**Keep:** public product/indicator documentation and free sample tables; grain is the statistical table.
**Drop:** subscription-gated yearbook tables and University of Michigan corporate pages.

## Cascade CMS (`cascadecms`) {#cascadecms}

Hannon Hill Cascade CMS indicator pages. Filter exports on `software.id = 'cascadecms'`. There is no catalog API.

```text
GET https://host/
```

**Keep:** published indicator, data-search, and dashboard pages on that host. **Drop:** news posts, staff directories, and documents that are not data pages. Data applications embedded in the CMS are site-specific; harvest the public pages the catalog record points at.

## DesInventar (`desinventar`) {#desinventar}

Filter exports on `software.id = 'desinventar'`. Harvest each registered host as its own country catalog (global DesInventar Sendai hub and national systems such as CamDi).

There is no anonymous machine-readable list API. Harvest the public **disaster event inventory**: classic installations expose the country database via `/DesInventar/main.jsp` query pages with region downloads (Excel); the Sendai web system exposes country profiles. Grain is the **national disaster loss inventory** (its event records), not each indicator cell.

**Keep:** DesInventar **disaster event / loss inventory** for the country on the registered host.
**Drop:** Sendai Framework Monitor (`sendaimonitor.undrr.org`, separate product), methodology and training documents, and reports that only cite DesInventar data.

```text
GET https://www.desinventar.net
GET {host}/DesInventar/main.jsp
```

## SORMAS (`sormas`) {#sormas}

National disease surveillance deployments with a public bulletin/dashboard. Filter exports on `software.id = 'sormas'`. One harvest scope per registered public dashboard host.

There is no anonymous list API on most deployments; the REST API (`/sormas-rest/`) requires credentials — do not probe it. Harvest only the anonymous public surface: the **bulletin/dashboard disease-count tables** (weekly counts of outbreak-prone diseases by province/district/municipality, e.g. Nepal EDCD `analysis.edcd.gov.np/bulletin`) and any documented CSV/Excel export on those pages.

Grain: one published bulletin table or indicator series ≈ one dataset analog. Drop staff login pages, case records, contact-tracing data, and any endpoint requiring authentication. Stop on `401`/`403`.

**Keep:** public bulletin/dashboard disease-count tables and their documented exports.
**Drop:** login-only surveillance apps, case/contact records, `/sormas-rest/` probing.

```text
GET https://analysis.edcd.gov.np/bulletin
```

## BOOST (`boost`) {#boost}

Country-owned BOOST open-budget portals. Filter exports on `software.id = 'boost'`. One harvest scope per country portal. There is no anonymous list API; pages are pivot-table apps with CSV/Excel export buttons and (some instances) a file library such as `/fichiersBoost/`.

Keep the published **budget tables** — expenditure/revenue pivots by administrative, economic, functional, and program classification — and the documented CSV/Excel exports linked from them. Grain: one published BOOST table or export file ≈ one dataset analog, not every pivot cell selection. Drop interactive pivot session state, chart images, and World Bank program pages.

**Keep:** published budget tables and their CSV/Excel exports.
**Drop:** pivot UI session state, chart images, WB program/documentation pages.

## Related

- [harvest.md](harvest.md)
- [harvest-metadata.md](harvest-metadata.md) (SDMX **structure** vs dataflows)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-incremental.md](harvest-incremental.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [discovery-indicators.md](discovery-indicators.md)
- [apidetect.md](apidetect.md)
- [agents/harvest.md](agents/harvest.md)
