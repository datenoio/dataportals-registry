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

## PxStat (`pxstat`) {#pxstat}

List live tables from the Cube API (often on a `ws.` / `ws-data.` host recorded in `endpoints[]`). Prefer REST ReadCollection; JSON-RPC is equivalent.

```text
GET https://ws-host/public/api.restful/PxStat.Data.Cube_API.ReadCollection/{datefrom}/en
```

Each JSON-stat **collection item** is a dataset. Grain is the **matrix / table code**. Drop subject folders, PxWidget embeds, and the CSO demo. Do not harvest `visual.cso.ie` as a second catalog of the same tables. Date-from filters recently updated tables; omit or use an early date for a full list.

## DGBAS Web (`dgbasweb`) {#dgbasweb}

Taiwan `/DgbasWeb/` statistical query UI. Harvest the public **table / indicator tree**, not yearbook PDFs or login-only WINSTA admin. One harvest scope per county or city tenant. Distinct from `nstatdb.dgbas.gov.tw` and from Taiwan PxWeb.

## OpenSDG (`opensdg`) {#opensdg}

Each SDG indicator is one dataset. List from reporting status or `data/` JSON.

```text
GET https://host/reporting-status
GET https://host/data/1-1-1.json
```

Language prefixes (`/en/data/…`) vary. Harvest every indicator id the site publishes, not only `1-1-1`. Drop goal/target **pages** without a data file.

## .Stat Suite (`statsuite`) {#statsuite}

```text
GET https://host/api/search
```

SDMX REST: list **dataflows** (the dataset analog). Pair with the Data Explorer UI only to confirm labels. If PxWeb is the public UI on the same office, harvest one catalog — do not double-count the same table. Do not harvest **Istat Data Browser** hubs (`istatdatabrowser`) as .Stat Suite.

## Istat Data Browser (`istatdatabrowser`) {#istatdatabrowser}

Filter exports on `software.id = 'istatdatabrowser'`. One harvest scope per public hub (IstatData, Coeweb, Sistan Hub, AstatData, IRIS, KNBS Open Data, INPS observatories as one catalog with several nodes).

```text
GET https://host/databrowserhub/api/core/hub/minimalInfo
GET https://host/databrowserhub/api/core/nodes
GET https://host/databrowserhub/api/core/nodes/{nodeId}/catalog
```

Some installs nest the API under `/databrowser/api/core/` (Astat, INPS) or a path prefix (`/coeweb/`, `/beta/`, `/DBrowser/`). Prefer `endpoints[]`. Each catalog item is an SDMX **dataflow**. Keep dataflow id + title + hub URL. Drop hub chrome, news, and dashboard pages. If the same office also has a public SDMX-RI `/SDMXWS/rest/dataflow` endpoint, harvest dataflows once — do not double-count the hub catalog and the NSI list.

**Drop** observation cubes unless the user asked for data files. Stop on `401`/`403`. Grain: [harvest-protocols.md](harvest-protocols.md#sdmx).

## Swing (`swing`) {#swing}

ABF Research Swing Viewer / inCijfers databanks (`{city}.incijfers.be`, `provincies.incijfers.be`). Harvest **indicator tables / reports** from the public databank. Drop dashboard chrome, map tiles, and login-only Studio admin (`/Admin/Studio/`). One tenant = one harvest scope.

```text
GET https://host/databank
```

Keep table/report identifiers + title + URL. Do not download full observation cubes unless the user asked for data files.

## Stat Technology (`stattech`) {#stattech}

Same dataflow grain as [.Stat Suite](#statsuite) when the product is Stat Technology. Keep SDMX **dataflows**, not observation cubes.

## Knoema (`knoema`) {#knoema}

Portal REST (`/api/1.0/` or `/api/3.0/`) lists **datasets** for that hub. Page the dataset catalog. Do not crawl every resource URL or the global knoema.com search. One portal = one harvest scope.

## SparkMap (`sparkmap`) {#sparkmap}

Filter exports on `software.id = 'sparkmap'`. One harvest scope per public hub (SparkMap national, All Things state sites, hospital and Community Action hubs). Do not harvest CARES HQ Map Room as a second copy of SparkMap.

There is no anonymous layer-list API on the public Map Room. Harvest the hub’s public **Map Room data list** (layer catalog page or downloadable layer list) and public **community needs assessment / indicator reports**. Grain is the map layer or report, not a choropleth screenshot.

**Drop** saved user maps, login-only assessment builder sessions, SparkMap marketing and pricing pages, and paid API extracts unless the user asked for those files. Stop on `401`/`403`.

## eDatos (`edatos`) {#edatos}

Filter exports on `software.id = 'edatos'`. One harvest scope per public hub.

```text
GET https://host/indicators/v1.0/indicators
```

Keep **indicators** and **indicator systems** from that JSON-stat API (or the public ODS catalog listing). Drop institute CMS chrome and each time-series observation cube. ISTAC Open SDG is a different catalog (`opensdg`).

## Cancer-Rates.info (`cancerrates`) {#cancerrates}

Filter exports on `software.id = 'cancerrates'`. There is no anonymous REST list API.

Keep the public **query UI** as the catalog (county incidence/mortality maps and tables). Grain for dataset harvest is a documented query (site × geography × year), not every map tile. Drop login-walled tenant paths and the KCR marketing/support pages.

## Conduent Healthy Communities Institute (`hci`) {#hci}

Filter exports on `software.id = 'hci'`. One harvest scope per public community site.

Keep public **indicator** pages (and CSV downloads linked from indicator detail). Drop CHNA PDF report libraries as if they were the catalog, login-only assessment builders, and SparkMap sites.

## Virtual LMI (`virtuallmi`) {#virtuallmi}

Filter exports on `software.id = 'virtuallmi'`. One harvest scope per state tenant.

Keep public **occupation / industry / area profile** tables the VLMI UI lists. Drop job-board postings, case-management VOS modules, and state LMI sites that are not VLMI. Stop on `401`/`403`.

## SDMX-RI (`sdmxri`) {#sdmxri}

List dataflows from the NSI REST/SOAP endpoint in `endpoints[]` (`/rest/dataflow` or documented NSI path). Keep dataflows. Drop structure-only resources. If the human catalog is PxWeb/.Stat, harvest that UI’s table list instead of raw SOAP. REST grain: [harvest-protocols.md](harvest-protocols.md#sdmx).

## GENESIS-Online (`genesisonline`) {#genesisonline}

Table **retrieval** is often POST-only. There is no reliable public GET “list all tables” API. Harvest the public research/catalog UI identifiers if documented; do not invent GET paths. Stop on login walls.

## IBIS-PH (`ibisph`) {#ibisph}

Indicator pages and IBIS-Q query modules. Harvest public **indicator** home records (XML/HTML indicator ids). Skip query-builder sessions and PDF fact sheets as separate datasets.

## DHIS2 (`dhis2`) {#dhis2}

National HMIS / public health indicator portals. Filter exports on `software.id = 'dhis2'`.

```text
GET https://host/api/system/info
GET https://host/api/dataSets.json?fields=id,displayName&pageSize=50
GET https://host/api/indicators.json?fields=id,displayName&pageSize=50
```

Keep **data sets** and public **indicators**. Drop user accounts, org-unit trees as datasets, and login-only analytics. Stop on `401`/`403`. Many ministries expose no anonymous API — then harvest only the public portal’s documented indicator list. Skip dhis2.org marketing.

## TabNet (`tabnet`) {#tabnet}

Brazilian DATASUS CGI tabulators. Filter exports on `software.id = 'tabnet'`. There is no REST list API.

Keep each public **`.def` table** (query form) as one dataset analog: title from the form heading, URL the `deftohtm.exe` / `cgi-bin/dh?` / `tabcgi.exe` link. Harvest from the installation’s table menu (HTML index), not by guessing `.def` paths.

**Drop** CGI `Mostre` query results, `Copia para Tabwin` files, CSV cell dumps, TabWin desktop packages, and every `.def` on `tabnet.datasus.gov.br` when harvesting the national catalog already listed from the DATASUS TabNet landing page. One harvest scope per installation (national, SES, municipal, ANS). Stop on `401`/`403`.

## FENIX (`fenix`) {#fenix}

Filter exports on `software.id = 'fenix'`. One harvest scope per public FENIX app (FAOSTAT, AMIS, AIDmonitor, DAD-IS, WIEWS, GIFT), not per CountrySTAT dataset dumped into FAO CKAN.

FAOSTAT list:

```text
GET https://fenixservices.fao.org/faostat/api/v1/en/groupsanddomains
```

Keep **domains / datasets** from that JSON. Observation queries (`/faostat/api/v1/{lang}/data/{domain}`) are not new catalogs. Prefer `endpoints[]` on the FAOSTAT record. Other FENIX UIs often have no anonymous list API — harvest the public dataset/indicator list from the UI, then stop. Skip dead `countrystat.org` hosts and GitHub UI repos.

## DataWarehousePro (`datawarehousepro`) {#datawarehousepro}

```text
GET https://app.datawarehousepro.com/guest/getDatabanksWithMnemonics/{tenant}
GET https://app.datawarehousepro.com/guest/export/{tenant}
```

Keep **databanks / series catalogs** for that tenant. Drop admin paste-from-Excel UI and other tenants on the same host. One portal = one harvest scope.

## IMF National Summary Data Page (`imfnsdp`) {#imfnsdp}

The NSDP HTML page is the catalog. Follow the SDMX 2.0 XML (and CSV where published) links for each **category / series**. Drop the IMF DSBB directory, the NSO homepage, and Knoema/WordPress wrappers (harvest those as `knoema` / `wordpress`). One country page = one harvest scope.

## Goal Tracker (`goaltracker`) {#goaltracker}

Harvest public **indicator / goal** pages the country tenant lists. Drop About/marketing HTML. There is no verified anonymous list API on every tenant — stop rather than scraping every visualization. Distinct from [Open SDG](#opensdg).

## NADA (`nada`) {#nada}

Survey microdata catalog.

```text
GET https://host/index.php/api/catalog/search
```

Page the JSON study list. Keep survey / microdata / geospatial studies. **Drop** `dtype` values that are document, video, or news when present. CSV export (`/index.php/catalog/export/csv`) is a bulk study list — still one row per study, not per file.

## IPUMS (`ipums`) {#ipums}

Filter exports on `software.id = 'ipums'`. One harvest scope per **collection** (USA, International, CPS, …). Use the IPUMS API metadata endpoints ([developer.ipums.org](https://developer.ipums.org)) with the collection name. Keep samples / datasets in that collection. **Drop** completed extract files, variable codebooks as separate catalogs, and the IPUMS marketing homepage. Do not download person-level microdata.

## NESSTAR (`nesstar`) {#nesstar}

```text
GET https://host/webview/
GET https://host/api
```

Harvest the **study** list in WebView. Many instances are dead — skip `401`/`404`. Do not scrape the vendor site.

## REDATAM (`redatam`) {#redatam}

```text
GET https://host/redbin/RpWebEngine.exe/Portal
```

HTML census/survey portals with little REST. Harvest the published **database/project** names from the portal home. Do not run interactive tabulations as a crawl.

## Colectica (`colectica`) {#colectica}

DDI repository. Public probe is often `/swagger/ui` or `/swagger/v1/swagger.json`. Search may be POST and/or authenticated — stop on `401`. Harvest **StudyUnit** / dataset items when a public API exists, not every DDI fragment (variables, questions) as a dataset.

## OBiBa Mica (`obibamica`) {#obibamica}

```text
GET https://host/studies
GET https://host/api/studies
```

Keep studies and Mica **datasets**. Drop networks, persons, and collected-dataset-empty shells. Docs: [micadoc.obiba.org](https://micadoc.obiba.org/en/latest/rest/).

## Survey Solutions (`surveysolutions`) {#surveysolutions}

Headquarters survey catalogs are often login-only. Harvest only a **public** questionnaire/data listing. Stop on `401`.

## SuperSTAR (`superstar`) {#superstar}

Census and official SuperWEB2 table-builder catalogs. Harvest the published **table / database** list from the SuperWEB2 catalogue or Open Data API (`/webapi/rest/v1/schema`), not every cube cell. Skip vendor demos, marketing, and login-only staff builders.

## Beyond 20/20 Web Data Server (`beyond2020`) {#beyond2020}

Filter exports on `software.id = 'beyond2020'`. There is no public REST catalog API.

Keep each public **report** (cube) listed under `ReportFolders/reportFolders.aspx` as one dataset analog: title from the report name, URL the `TableViewer/tableView.aspx?ReportId=` link. Walk the folder tree on that installation only.

**Drop** language-selection pages, `TableViewer` cell extracts, IVT/Excel/CSV downloads as separate catalogs, Crime Insight tenants, login WDS, and every `ReportId` on `www.jodidb.org` / `difusion.jccm.es` when harvesting the installation already registered as a catalog. One harvest scope per WDS host. Stop on `401`/`403`.

## Official international hubs {#official-international-hubs}

These `software.id` values are **one registered catalog each**. Harvest **contents** when the user asked for that hub. Do not add them again as new registry YAML.

Grain is still **dataflow / indicator**, not observation cells. SDMX protocol: [harvest-protocols.md](harvest-protocols.md#sdmx). Prefer `endpoints[]` on the live record when present.

## Eurostat (`eurostat`) {#eurostat}

```text
GET https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/all/latest
```

Each **dataflow** is one dataset analog. The registered observation URL (`/api/dissemination/statistics/1.0/data`) is **not** a catalog list — do not page cubes as datasets.

## ECB (`ecb`) {#ecb}

```text
GET https://data-api.ecb.europa.eu/service/dataflow
```

List **dataflows**. The UI host `data.ecb.europa.eu` is not the SDMX root; `/service/data` is observations. The registered observation endpoint is not a catalog list.

## World Bank (`dataworldbankorg`) {#dataworldbankorg}

```text
GET https://api.worldbank.org/v2/indicator?format=json&per_page=1000
GET https://api.worldbank.org/v2/sources?format=json
```

Keep **indicators** (or **sources** if the user asked for catalogs-of-catalogs). Drop country pages, WDI observation queries (`/v2/country/.../indicator/...`), and data.worldbank.org marketing.

## WHO GHO (`whoint`) {#whoint}

```text
GET https://ghoapi.azureedge.net/api/Indicator
```

Keep **indicators**. Drop Dimension / country lists and every GHO observation row.

## ILOSTAT (`ilostat`) {#ilostat}

```text
GET https://sdmx.ilo.org/rest/dataflow
```

Keep **dataflows**. `www.ilo.org/sdmx/` is often Cloudflare-blocked from scripts — use `sdmx.ilo.org`. Drop ilostat.ilo.org article pages.

## BIS (`databisorg`) {#databisorg}

```text
GET https://stats.bis.org/api/v1/dataflow
```

Keep SDMX **dataflows**. The registered `https://data.bis.org/api/v0/search` is **POST** (not a GET list) and is not a dataset catalog. Drop help HTML and observation queries.

## UNICEF (`datauniceforg`) {#datauniceforg}

```text
GET https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow
```

Keep **dataflows**. Do not treat every country profile on data.unicef.org as a dataset. The HTML site may be Cloudflare-blocked; SDMX is the harvest.

## StatPlanet (`statplanet`) {#statplanet}

Public StatPlanet Cloud / HTML5 **indicator explorer**. Grain is the **indicator** (row in `data.csv` / Cloud indicator list), not every map animation frame.

```text
GET https://host/.../data.csv
GET https://host/.../settings.csv
```

Keep named indicators the dashboard can select. One catalog per host/explorer — do not harvest each `*-StatTrends.html` layout as a separate catalog. Drop vendor demos on statsilk.com, Flash SWF-only pages, and viewers that only chart another registered catalog (World Bank Open Data API). Stop on `401`/`403`. CSV is the list; do not scrape tiles.

## Oracle APEX (`oracleapex`) {#oracleapex}

Public statistical **apps** that list indicators or tables. Harvest the documented public REST/ORDS feed if it returns a dataset list. Skip generic APEX sites, login builders, and `/apex/f?p=` session URLs as identifiers.

## Apache Superset (`superset`) {#superset}

Public BI that sometimes **is** the indicator catalog. Harvest public **datasets** / charts the catalog documents. Drop internal dashboards and login-only `/superset/dashboard/`. Stop on `401`. Do not scrape every dashboard tile.

## IBM Cognos (`ibmcognos`) {#ibmcognos}

Harvest published **packages / reports** that are statistical tables. Drop intranet Cognos. Stop on `401`.

## Other indicator IDs

| `software.id` | Harvest | Skip |
|---------------|---------|------|
| `statplanet` | see above | Vendor demos; World Bank viewers |
| `datavavt` | VA/VT public indicator tables | Intranet |
| `bicontour` | Public contour/indicator catalog | Viewer-only |
| `datainsight` | Public insight **datasets** | Internal BI |

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
