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
```

Each JSON object with `type: t` (table) is a dataset. `type: l` is a folder — recurse. Do not treat a POST of table cells as a new dataset. Cap depth; some NSOs have thousands of tables.

**Keep:** PxWeb **tables** (`type: t`). **Drop:** subject **folders** (`type: l`) and POST observation cubes.

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

## OpenSDG (`opensdg`) {#opensdg}

Each SDG indicator is one dataset. List from reporting status or `data/` JSON.

```text
GET https://host/reporting-status
GET https://host/data/1-1-1.json
```

Language prefixes (`/en/data/…`) vary. Harvest every indicator id the site publishes, not only `1-1-1`. Drop goal/target **pages** without a data file.

**Keep:** OpenSDG **indicator** JSON. **Drop:** goal/target **pages** without a data file.

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

Keep **indicators** and **indicator systems** from that JSON-stat API (or the public ODS catalog listing). Drop institute CMS chrome and each time-series observation cube. ISTAC Open SDG is a different catalog (`opensdg`).

**Keep:** JSON-stat **indicators** and indicator systems. **Drop:** institute CMS chrome and time-series observation cubes.

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

Keep public **occupation / industry / area profile** tables the VLMI UI lists. Drop job-board postings, case-management VOS modules, and state LMI sites that are not VLMI. Stop on `401`/`403`.

**Keep:** public occupation / industry / area **profile tables**. **Drop:** job-board postings, VOS case-management, and non-VLMI state LMI sites.

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

**Keep:** public **budget / socio-economic views** and listed open-data files. **Drop:** iminfin.ru region rows as separate catalogs, login/admin, and non-Krista open-budget CMS.

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


## DHIS2 (`dhis2`) {#dhis2}

National HMIS / public health indicator portals. Filter exports on `software.id = 'dhis2'`.

```text
GET https://host/api/system/info
GET https://host/api/dataSets.json?fields=id,displayName&pageSize=50
GET https://host/api/indicators.json?fields=id,displayName&pageSize=50
```

Keep **data sets** and public **indicators**. Drop user accounts, org-unit trees as datasets, and login-only analytics. Stop on `401`/`403`. Many ministries expose no anonymous API — then harvest only the public portal’s documented indicator list. Skip dhis2.org marketing.

**Keep:** DHIS2 **data sets** and public **indicators**. **Drop:** user accounts, org-unit trees as datasets, and login-only analytics.

## TabNet (`tabnet`) {#tabnet}

Brazilian DATASUS CGI tabulators. Filter exports on `software.id = 'tabnet'`. There is no REST list API.

Keep each public **`.def` table** (query form) as one dataset analog: title from the form heading, URL the `deftohtm.exe` / `cgi-bin/dh?` / `tabcgi.exe` link. Harvest from the installation’s table menu (HTML index), not by guessing `.def` paths.

**Drop** CGI `Mostre` query results, `Copia para Tabwin` files, CSV cell dumps, TabWin desktop packages, and every `.def` on `tabnet.datasus.gov.br` when harvesting the national catalog already listed from the DATASUS TabNet landing page. One harvest scope per installation (national, SES, municipal, ANS). Stop on `401`/`403`.

**Keep:** each public **`.def` table** (query form). **Drop:** CGI `Mostre` results, TabWin files, CSV cell dumps, and every `.def` on the national landing when harvesting that catalog.

## FENIX (`fenix`) {#fenix}

Filter exports on `software.id = 'fenix'`. One harvest scope per public FENIX app (FAOSTAT, AMIS, AIDmonitor, DAD-IS, WIEWS, GIFT), not per CountrySTAT dataset dumped into FAO CKAN.

FAOSTAT list:

```text
GET https://fenixservices.fao.org/faostat/api/v1/en/groupsanddomains
```

Keep **domains / datasets** from that JSON. Observation queries (`/faostat/api/v1/{lang}/data/{domain}`) are not new catalogs. Prefer `endpoints[]` on the FAOSTAT record. Other FENIX UIs often have no anonymous list API — harvest the public dataset/indicator list from the UI, then stop. Skip dead `countrystat.org` hosts and GitHub UI repos.

**Keep:** FENIX **domains / datasets** (FAOSTAT groupsanddomains or the public UI list). **Drop:** observation cubes, dead CountrySTAT hosts, and GitHub UI repos.

## DataWarehousePro (`datawarehousepro`) {#datawarehousepro}

```text
GET https://app.datawarehousepro.com/guest/getDatabanksWithMnemonics/{tenant}
GET https://app.datawarehousepro.com/guest/export/{tenant}
```

Keep **databanks / series catalogs** for that tenant. Drop admin paste-from-Excel UI and other tenants on the same host. One portal = one harvest scope.

**Keep:** tenant **databanks / series catalogs**. **Drop:** admin paste-from-Excel UI and other tenants on the same host.

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


## World Bank (`dataworldbankorg`) {#dataworldbankorg}

```text
GET https://api.worldbank.org/v2/indicator?format=json&per_page=1000
GET https://api.worldbank.org/v2/sources?format=json
```

Keep **indicators** (or **sources** if the user asked for catalogs-of-catalogs). Drop country pages, WDI observation queries (`/v2/country/.../indicator/...`), and data.worldbank.org marketing.

**Keep:** World Bank **indicators** (or **sources** if asked). **Drop:** country pages, WDI observation queries, and marketing.

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

**Keep:** ILOSTAT SDMX **dataflows**. **Drop:** ilostat.ilo.org article pages.

## BIS (`databisorg`) {#databisorg}

```text
GET https://stats.bis.org/api/v1/dataflow
```

Keep SDMX **dataflows**. The registered `https://data.bis.org/api/v0/search` is **POST** (not a GET list) and is not a dataset catalog. Drop help HTML and observation queries.

**Keep:** BIS SDMX **dataflows**. **Drop:** help HTML, POST search, and observation queries.

## UNICEF (`datauniceforg`) {#datauniceforg}

```text
GET https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow
```

Keep **dataflows**. Do not treat every country profile on data.unicef.org as a dataset. The HTML site may be Cloudflare-blocked; SDMX is the harvest.

**Keep:** UNICEF SDMX **dataflows**. **Drop:** every country profile on data.unicef.org as a dataset.

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

SharePoint statistics pages publish documents/lists, not dataset records. Harvest documented Excel/CSV **files** the page links (statistics tables, data dictionaries). Drop `Authenticate.aspx`, `/_vti_bin/`, and any login wall. Stop on `401`.

**Keep:** documented Excel/CSV files the statistics page links.
**Drop:** `Authenticate.aspx`, `/_vti_bin/`, and login walls. Stop on `401`.


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
