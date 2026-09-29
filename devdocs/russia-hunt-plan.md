# Russia (RU) catalog hunt — plan and prompt pack

Generated 2026-09-29 from past-session review. Working note, not published docs.

## 1. Session sources reviewed

| Source | What was found |
|--------|----------------|
| Cursor CLI/desktop chats (`~/.cursor/chats/9ae7e5d1…`, 85 stores, Nov 2025 era) | RU work was scheduled-record processing, not discovery: `process_ru_scheduled_to_entities.py` promotion runs, owner/location metadata fixes, scheduled/RU geo batch (6 files → entities/RU/Federal/geo). No FOFA/Censys dorks in this era. |
| Cursor workspaceStorage `state.vscdb` (dataportals-registry) | Same era, same workflow — promotion and metadata scripts. |
| ZCode tasks (`~/.zcode/v2/tasks-index.sqlite`, 73 tasks for this workspace) | Russian-software hunts: **esimo** (federation topology mapped: central Obninsk node + SPb + Vladivostok; `portal.esimo.ru` is an alias of the registered central portal; `data.esimo.ru` is a live lead), **geocadgsee** (Tomsk/Sakhalin/Kemerovo GSEE portals — all three already registered but mis-tagged `software.id: custom`), **sputnikweb** (Geoscan captcha-walled; Wayback CDX of vendor blog + paced DuckDuckGo HTML endpoint worked). Also the IN/PK/PH hunt-plan sessions used as the template for this file. |
| Kimi conversations (`kimi-agent` conversations.sqlite, 78 for this workspace) | **Russian Data Catalog Pattern Analysis** (2026-09-28): 241 RU `custom` entries clustered; created `biouml` def (3 instances re-tagged); ISOGD/GISOGD family (~12 entries, competing vendors, mostly geo-blocked) and Инвестиционная карта family (~8 entries, identical title pattern, fingerprints disagree) identified but unresolved; NetCat/MODX deferred (1 instance each). Plus FOFA hunts: geomixer (+6, Sep 17), sputnikweb (+1, Sep 16), geoserver .ru (+5, Sep 26), regis (0, Sep 18). |
| ChatGPT | No usable local history (server-side; local cache blobs from Oct 2025 are unrelated). Prompts below follow the documented browser-agent recipe in `docs/discovery-agent-tools.md`. |
| Repo knowledge | 24 `devdocs/russian-*` pass files (14 passes / **98 additions** on 2026-09-07), `dataquality/hunts.jsonl` (766 rows), `docs/agents/discover.md`, `docs/agents/improve.md`. |

## 2. Current RU state (2026-09-29)

**570 entities, 1 scheduled.** By type (DuckDB, owner country = RU):

| Type | n | Notes |
|------|--:|-------|
| Geoportal | 280 | 97 federal-level; heavy vendor mix (below) |
| Open data portal | 161 | bitrix 36, gosweb 13, ckan 8, wordpress 9, custom majority |
| Scientific data repository | 76 | 73 federal-level; ipt 11, academy-heavy |
| Indicators catalog | 40 | fedstat (ЕМИСС), cbr.ru, minfin NSDP, bi.gks.ru, showdata.gks.ru, rosstat munst, ksopenbudget 6, imonitoring 12 |
| API Catalog | 3 | apiportal.ru, api-list.ru, api.petersburg.ru |
| Machine learning | 3 | mosmed, medicaldatahub, registry.cit.gov.ru |
| Microdata | 2 | isras databank, eurasiamonitor |
| Data marketplace | 2 | tenderdatahub, datamarkup |
| Metadata / Search / Other | 1 / 1 / 1 | niron, openurbandata, openngo |

Software spread (top): custom **238**, bitrix 36, nextgisweb 35, arcgisserver 27, activemapgis 25, geoserver 22, geometa 18, gosweb 13, imonitoring 12, ipt 11, orbismap 10.

`is_national` set: data.gov.ru (opendata — **record is deprecated/inactive**, successor product unresolved), minfin NSDP + cbr.ru (indicators). **No national-flagged geoportal** — NSPD (`nspdrosreestrgovru`) is the formal national spatial-data system, flag question open for the review slice.

**Zero-entity federal subjects (2):** RU-KRS (Kursk), RU-SE (North Ossetia). All other 77 in-use subregions have ≥1 entity. Crimea/Sevastopol stay out (ISO UA).

## 3. Already hunted — do not repeat

- **datacatalogs.ru directory**: fully reviewed (322 embedded entries, 160 unmatched leads worked through) in the Sep 7 all-types series — 98 additions across 14 passes. Do not re-review the directory.
- **Directories swept**: GISGeo federal/regional/municipal geoportal lists, ICM SB RAS geoportal directory (gis.krasn.ru), ORBISmap and NextGIS vendor project lists.
- **FOFA subdomain-keyword country-shape hunt (Sep 20, +6):** 164 curated keywords (`data/reference/subdomain_keywords_curated.csv`), 4,274 FOFA rows → 2,350 unique hosts, 70 already registered. High-yield keywords: `opendata`, `geoportal`, `gisogd`, `isogd`, `geoserver`, `dspace`. Generic `map`/`wms`/`catalog`/`iris`/`atlas` were noise (shops, warehouse WMS). Re-runs are dedupe-blocked by `hunt.py prior` until ~Oct 4.
- **FOFA geoserver .ru (Sep 26, +5):** documented title fingerprints are empty on .ru (FOFA stores `GeoServer: Redirecting` / `欢迎`); productive query was `body=geoserver && host=.ru` (140). 17 .ru geoserver hosts were already registered.
- **Software-instance hunts done:** geomixer (Sep 17, +6), sputnikweb (Sep 16, +1), reinformregis (Sep 18, 0 — vendor list exhausted), esimo + geocadgsee + sputnikweb tenant hunts (ZCode, Sep 2026). Per improve.md, do not repeat a software-instance hunt within two weeks of the last one.
- **Municipal `/opendata` Russian-language sweeps:** 48 opendata additions over 4 passes covered Leningrad, Irkutsk, Tver, Sverdlovsk, Novgorod, Samara, Bashkortostan, Krasnoyarsk, Vladimir, Krasnodar, Pskov, Tyumen, Khabarovsk oblast queries. Yield dropped to ~2 per pass by pass 10 — classic own-domain municipal sweep is close to saturation; the remaining municipal market is migrating to Gosweb/gosuslugi (slice 2 below).
- **Known rejects (do not re-add):** dataverse.datah.ru (alias of dataverse.pushdom.ru), gisogd.kbr.ru (GeoMeta OIDC login), geoportal.vologda-portal.ru (staff GIS), opendata.tpu.ru (registration-gated), nesday.tmweb.ru (vendor template host for fake municipal catalogs), indorsoft/orbismap/simai demo hosts, publication-only DSpace/ePrints IRs, empty ArcGIS Server instances (SampleWorldCities), zero-dataset catalogs (adm-nurma, Верхний Баскунчак-class single-table pages), placeholders (opendata.ocean.ru), NORA/CyberLeninka (no dataset collections), WCIOM (sign-in).

### Network/vantage notes (from ZCode + pass ledgers)

- Many RU gov sites are **HTTP-only or time out on HTTPS**; try plain HTTP before declaring failure (esimo.ru case).
- **Geo-blocking is common** (geo.sakhalin.gov.ru, most ISOGD hosts) — mark *unresolved*, never flip to `inactive` from this vantage point.
- Vendor sites may be captcha-walled (geoscan.aero): use **Wayback CDX index** of the vendor blog and **static-asset paths** (brochure PDFs) to enumerate tenants; pace DuckDuckGo HTML queries to avoid the HTTP 202 anomaly wall.
- HTTP 200 alone never establishes a catalog: several municipal "CSV downloads" returned HTML bodies (Novopavlovka) or another municipality's data (Sorum, centerapktver.ru).

## 4. Hunt sequence (ordered by expected yield)

One slice per session; run `python scripts/hunt.py prior --target RU.<slice>` first (14-day dedupe), follow the command card (`budget` → `search fofa|censys --dedupe` → `probe` → `ingest` → `log`), promote in the same session, `validate-yaml --id`, log to `dataquality/hunts.jsonl`.

| # | Slice (hunt kind) | Why | Angle |
|---|-------------------|-----|-------|
| 1 | **Zero-entity subjects** (`country-shape`) | RU-KRS and RU-SE are the only federal subjects with 0 records | Kursk: admkursk.ru open-data section, Kurskstat tables, ISOGD Kursk. North Ossetia: alania.gov.ru / rso-a.ru open data, sevosstat. Expect bitrix/gosweb/custom `/opendata` pages and one ISOGD geoportal each. |
| 2 | **Gosweb/gosuslugi municipal tenants** (`software-instance`, target `gosweb`) | Municipal open data is migrating to `{muni}.gosweb.gosuslugi.ru` / `{muni}.gosuslugi.ru/ofitsialno/statistika/otkrytye-dannye/`; only 13 gosweb + a few gosuslugi tenants registered; Irbeysky pass-4 record announces exactly this move | FOFA `host=".gosweb.gosuslugi.ru"` and `body="ofitsialno/statistika/otkrytye-dannye" && host=".gosuslugi.ru"`; crt.sh `%.gosuslugi.ru` wildcard dump filtered to municipal names. Accept only tenants whose `/otkrytye-dannye` page lists ≥1 dataset; reject empty constructor pages. |
| 3 | **Microdata depth** (`country-gap`) | Only 2 records — the thinnest RU type | RLMS-HSE (HSE longitudinal monitoring), HSE Data Culture collections, Rosstat census/survey microdata access (RMDA-class), Levada/FOM public tables (likely restricted — record access_mode accordingly), INION RAN beyond niron. Reject sign-in-only archives (WCIOM stays rejected). |
| 4 | **University IRs, dataset-bearing** (`university-ir`) | 76 scientific but academy/IPT-heavy; university DSpace/Dataverse coverage untested with the dataset-bearing test | OpenDOAR/re3data/OpenAIRE `country:RU`, HSE/SPbU/MSU/URFU/KFU/NSU/ITMO/TPU (opendata.tpu.ru stays rejected — registration wall), `.ac.ru`/`.edu.ru` DSpace 7 `/server/api` Dataset entityType. Publication-only IRs stay rejected (established rule). |
| 5 | **Indicators depth** (`country-indicators`) | 40 records; regional stat branches and regional budget portals under-covered | Regional Rosstat web tables for subjects with none; regional minfin budget portals beyond the 6 ksopenbudget tenants; regional ЕМИС-like nodes; reject PDF-publication pages and PxWeb already covered by fedstat. |
| 6 | **ISOGD/GISOGD municipal urban-planning GIS** (`municipal-gis`) | Mandated system type — every municipality must run one; ~12 entries known, vendors partially identified (farvatergisogd, geometa defs exist) | Vendor-by-vendor: enumerate Farvater (ifrigate.ru) and Gems Geometa tenant lists, then unknown-vendor ISOGD hosts via `host="gisogd."`/`host="isogd."` FOFA patterns (already high-yield Sep 20). Geo-blocked = unresolved, not inactive. Identify the vendor from footer credits before proposing new defs. |
| 7 | **Invest-map family** (`custom-review`) | ~8 entries share the title «Инвестиционная карта \<региона\>» but fingerprints disagree (one is Bitrix) | Open each, fingerprint vendor/standard; if one vendor confirmed → new software def + re-tag; else document as heterogeneous and close. |
| 8 | **Thin types leftovers** (`country-gap`) | api 3, ml 3, marketplace 2, metadata 1, search 1 | Gosuslugi/gov API directories (developer portals on `.gov.ru`, swagger), successor of the deprecated data.gov.ru as a **research question** — if a public national open-data catalog UI exists it belongs as the national product; university ML dataset pages; DCAT/SDMX registries. |
| 9 | **Custom-software review pass 2** (`custom-review`) | 238 `custom` RU entries; Sep 28 pass created biouml and left ISOGD/invest-map families open | Cluster remaining custom by title/footer/vendor credit; re-tag the 3 geocadgsee entries (Tomsk `mapadmintomskru`, Sakhalin, Kemerovo) from `custom` — confirmed GSEE in the ZCode session; watch NetCat/MODX for second instances. |
| 10 | **Country review** (`country-review`) | 570 records never reviewed as a set | improve.md checklist: live link, status for dead hosts (geo-blocked ≠ dead — verify via web tool), software.id from probe, owner from site, is_national only for the official national product per type (resolve the NSPD geoportal flag and the data.gov.ru successor), endpoints only after 200. |

Skip broad geo sweeps — 280 geoportals, market is dense; only opportunistic re-checks of unresolved hosts (minsport.gov.ru, bayanday.irkmo.ru 403, tusp14.msp.midural.ru, admsud.ru, Sudogda, Staropolye).

## 5. Prompt pack

### 5.1 ZCode / Cursor (repo open — the hunt sessions)

Paste one per session, in slice order. FOFA creds must be in the user env (`FOFA_EMAIL`/`FOFA_KEY`); Censys usually out of credits.

```text
Which Kursk (RU-KRS) and North Ossetia (RU-SE) data catalogs are missing? Both federal
subjects have zero registry entities.
Follow docs/agents/discover.md. Run scripts/hunt.py prior --target RU.zero-subjects first.
Duplicate-check data/datasets/datasets.duckdb for RU. For each subject find: the regional
government open-data page (admkursk.ru, alania.gov.ru/rso-a.ru), the Rosstat branch
statistics tables (Kurskstat, Sevosstat), and the mandated ISOGD urban-planning geoportal.
Try plain HTTP when HTTPS times out; geo-blocked = unresolved, not inactive. Promote finds
in this session, validate-yaml --id, log hunt kind country-shape.
```

```text
Which gosweb catalogs are missing?
Gosweb (software def data/software/opendata/gosweb.yaml) is the Gosuslugi constructor
hosting municipal open-data at {muni}.gosweb.gosuslugi.ru and
{muni}.gosuslugi.ru/ofitsialno/statistika/otkrytye-dannye/. Only ~14 tenants registered.
Run scripts/hunt.py prior --target gosweb, then FOFA host=".gosweb.gosuslugi.ru" and
body="ofitsialno/statistika/otkrytye-dannye" && host=".gosuslugi.ru" with --dedupe, plus
a crt.sh %.gosuslugi.ru wildcard dump filtered to municipal names. Probe, keep only
tenants whose open-data page lists at least one dataset; reject empty constructor pages.
Ingest, log hunt kind software-instance.
```

```text
Which Russia microdata catalogs are missing? Only 2 are registered (isras databank,
eurasiamonitor).
Follow docs/agents/discover.md. Check RLMS-HSE (HSE Russia Longitudinal Monitoring
Survey), HSE data collections, Rosstat survey/census microdata access products, Levada
and FOM public table archives, INION RAN beyond the registered niron. Accept public
catalog UIs with study/variable listings; record restricted access_mode honestly for
registration-gated archives; reject sign-in-only walls (WCIOM stays rejected).
Log hunt kind country-gap, target RU-microdata.
```

```text
There are a lot of Russian universities and research organizations that could have
scientific data repositories that are not yet listed. Which of them are missing?
Follow docs/agents/discover.md (country university IRs). Baseline: 76 RU scientific
records, academy/IPT-heavy. Sources: OpenDOAR and re3data country facet, OpenAIRE Graph
country:RU, Dataverse installations JSON, DSpace 7 /server/api Dataset entityType on
.ac.ru/.edu.ru and university domains (HSE, SPbU, MSU, NSU, KFU, URFU, ITMO). Accept only
IRs that list datasets. Publication-only DSpace/ePrints stay rejected; opendata.tpu.ru
stays rejected (registration wall); dataverse.datah.ru is an alias of the registered
dataverse.pushdom.ru. Log hunt kind university-ir.
```

```text
Which Russia indicators catalogs are missing? 40 are registered; fedstat (ЕМИСС), cbr.ru,
minfin NSDP, bi.gks.ru, showdata.gks.ru and 6 ksopenbudget tenants are covered.
Follow docs/agents/discover.md (country indicators). Target: regional Rosstat branch
table databases for subjects with none, regional finance-ministry budget portals beyond
ksopenbudget tenants (iMonitoring is NPO Krista — check npo.krista.ru customer list),
regional EMIS-like statistical nodes. Reject PDF publication pages and agency PxWeb
already covered by fedstat. is_national stays on minfin NSDP and cbr.ru only.
Log hunt kind country-indicators.
```

```text
Which Russian ISOGD/GISOGD municipal urban-planning geoportals are missing?
This is a mandated system type — every municipality runs one. Registered: ~12 entries;
software defs exist for farvatergisogd and geometa. Enumerate vendor tenant lists
(Farvater ifrigate.ru/solution/gisogd, Gems geometa.ru), then FOFA host="gisogd." and
host="isogd." with --dedupe (both were high-yield keywords in the Sep 20 hunt).
Identify the vendor from footer credits («Разработано») before creating any new software
definition. Geo-blocked hosts (most ISOGD) = unresolved, not inactive. gisogd.kbr.ru
stays rejected (OIDC login). Log hunt kind municipal-gis.
```

```text
Review the Russian «Инвестиционная карта» records (investmap.tatarstan.ru,
investmap.nashsever51.ru, map.invest-ivanovo.ru, invest32.ru, zab-investportal.ru and
siblings — grep entities/RU for invest). Fingerprint each for a common vendor/standard
(the Sep 28 pattern review found identical titles but conflicting fingerprints, one is
Bitrix). If one vendor is confirmed, create the software definition per
docs/software-taxonomy.md and re-tag; if heterogeneous, document and close.
Log hunt kind custom-review, target RU-investmap.
```

```text
Which Russia API catalogs, ML catalogs, data marketplaces, metadata catalogs and data
search engines are missing? Counts are api 3, ml 3, marketplace 2, metadata 1, search 1.
Follow docs/agents/improve.md thin-types guidance. Check government developer portals and
API directories on .gov.ru (swagger/api-docs), university and corporate ML dataset pages
beyond mosmed/medicaldatahub/registry.cit.gov.ru, DCAT/SDMX registries. Separately, as a
research question: identify the successor national open-data product after data.gov.ru
(deprecated in the registry) — if a public national catalog UI exists, propose it as the
national product. Reject per-service gateways and login walls. Log hunt kind
country-gap, target RU-thin-types.
```

```text
Review data catalogs with custom software in Russia (238 entries), pass 2.
The Sep 28 pass created biouml and left two families open. Now: (1) re-tag the three
confirmed Geocad GSEE portals from custom — mapadmintomskru (Tomsk, title ИС «Геокад»
Томск), geo.sakhalin.gov.ru, and the Kemerovo entry; (2) cluster the remaining custom
entries by title pattern, footer vendor credits («Разработано», «Платформа») and asset
paths; (3) propose software definitions only where a reusable product with ≥2 instances
or a first-party product page exists (taxonomy rules); NetCat and MODX stay deferred
until a second instance appears. Run sync-software-maps and validate-software after
re-tags. Log hunt kind custom-review, target RU-custom-pass2.
```

```text
Review records at data/entities/RU and fix them
Use the country-review checklist in docs/agents/improve.md: live link (try HTTP when
HTTPS times out), status for dead hosts but geo-blocked ≠ dead (verify via web tool
before touching status), software.id from a probe, owner name/link from the site,
coverage country/path match, endpoints only after a 200 on that path, api flag
consistent, properties.is_national only for the official national product of a type —
resolve two open questions: whether nspd.rosreestr.gov.ru is the national geoportal, and
what replaces the deprecated data.gov.ru as national open-data product. assign +
validate-yaml --id on touched files. Log hunt kind country-review.
```

### 5.2 Cursor (FOFA pass, after the above — only if slices are thin)

```text
FOFA hunt for Russian catalog hosts not yet registered. Censys is out of credits; use FOFA.
Run scripts/hunt.py budget, then one query at a time with --dedupe:
  host="gisogd." && country="RU"
  host="isogd." && country="RU"
  host=".gosweb.gosuslugi.ru"
  body="ofitsialno/statistika/otkrytye-dannye" && host=".gosuslugi.ru"
  body="/server/api" && (host=".ac.ru" || host=".edu.ru")      (DSpace 7)
  title="Dataverse" && country="RU"
  body="GeoNode" && host=".ru"
  title="CKAN" && country="RU"
Skip: the Sep 20 subdomain-keyword sweep (dedupe-blocked), the Sep 26 geoserver .ru
queries, geomixer/sputnikweb/regis (hunted within two weeks). Probe candidates per
docs/agents/discover.md — try HTTP when HTTPS times out; geo-blocked = unresolved.
Reject nesday.tmweb.ru template hosts, vendor demos, bare-IP servers without a public
UI, and Crimea/Sevastopol hosts (ISO UA). Ingest, log kind country-gap.
```

### 5.3 ChatGPT (browser/web search, no repo — candidate tables only)

Start the thread with (per `docs/discovery-agent-tools.md`):

```text
Read https://datenoio.github.io/dataportals-registry/llms.txt
and https://datenoio.github.io/dataportals-registry/docs/discovery-opendata
Find open-data catalogs in the two Russian federal subjects with no registered catalogs:
Kursk oblast and North Ossetia–Alania. Look for the regional government open-data
section, municipal /opendata pages, the Rosstat branch statistics tables (Kurskstat,
Sevosstat), and the mandated ISOGD/GISOGD urban-planning geoportal for each.
Return a markdown table: name | url | evidence | proposed catalog_type | likely software.
Do not invent registry uids. I will duplicate-check in the repo myself.
```

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-scientific
Which Russian universities run data repositories that list datasets (not publications)?
Check HSE, SPbU, MSU, NSU, KFU, URFU, ITMO, and .ac.ru DSpace/Dataverse installations.
Known: opendata.tpu.ru is registration-gated (rejected), dataverse.datah.ru is an alias
of an already-registered host. Return: name | url | evidence of a dataset listing |
why not publication-only.
```

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-indicators
Find Russian microdata and survey-data catalogs beyond the registered Institute of
Sociology databank (isras.ru) and Eurasian Monitor. Check RLMS-HSE, HSE data
collections, Rosstat survey/census microdata access, Levada Center and FOM public
tables. Return: name | url | evidence | public vs registration-gated.
```

Paste an RU CSV slice (`id`, `name`, `link`, `software`) into the thread so it stops proposing registered hosts.

### 5.4 Kimi (browser-capable, no repo — research + verification pass)

```text
You help maintain dataportals-registry, a registry of open data portals, geoportals,
scientific repositories, and indicators catalogs. Read
https://datenoio.github.io/dataportals-registry/llms.txt first.

Task: research Russian government data infrastructure and return a candidate table of
data catalogs NOT in this list of already-registered hosts (I will paste it).
Focus: (1) Kursk and North Ossetia regional open-data and statistics sites; (2) municipal
open data hosted on *.gosuslugi.ru / *.gosweb.gosuslugi.ru; (3) university repositories
that list datasets; (4) ISOGD/GISOGD urban-planning geoportals with a named vendor;
(5) any national API directory or the successor of the shut-down data.gov.ru.

For each candidate open the site in the browser and verify: public catalog UI or
harvestable API, no login wall, not a PDF library or project page. Russian sites are
often HTTP-only and sometimes geo-block foreign networks — note which. Return:
name | url | what is listed there | owner agency | why it is a catalog.
Do not invent uids. Already-rejected (do not propose): dataverse.datah.ru (alias),
gisogd.kbr.ru (login), opendata.tpu.ru (registration), nesday.tmweb.ru (vendor
template), WCIOM (sign-in), NORA and CyberLeninka (no dataset collections).
```

Follow-up Kimi prompt once a shortlist exists:

```text
For each URL in this shortlist, open it and check whether it actually lists datasets
(browsable catalog or API), who owns it, and what software it runs (CKAN
/api/3/action/status_show, DSpace /server/api, Dataverse /api/info/version, Bitrix
/bitrix/ assets, gosweb constructor chrome, vendor footer credits «Разработано …»).
Return only the ones that pass, with the probe evidence. Stop on 401/403 and mark them
rejected; mark geo-blocked ones unresolved.
```

## 6. RU-specific accept / reject

**Accept:** public catalog UI or harvestable API on `.ru` / `.su` / `.xn--p1ai` / gov domains; HTTP-only sites (common for RU gov); Gosweb/gosuslugi municipal tenants with ≥1 dataset; dataset-bearing IRs (DSpace Dataset type, Dataverse); native statistical table DBs (queryable, not PDF); subregion placement for regional owners (`owner.location.level` 30); mixed open/restricted access recorded honestly (Roszdravnadzor/Mintrud ESIA-gated datasets precedent).

**Reject:** geo-blocked ≠ inactive (mark unresolved); Crimea/Sevastopol hosts (ISO UA); vendor template/demo hosts (nesday.tmweb.ru, orbismap/indorsoft/simai demos); login walls (GeoMeta OIDC, ESIA-only, WCIOM); zero-dataset catalogs and single-table pages; publication-only DSpace/ePrints; empty ArcGIS (SampleWorldCities); bare-IP GeoServer/GeoMixer without public UI; aliases of registered hosts (dataverse.datah.ru); placeholders and "under construction" pages; HTTP 200 with HTML body where a CSV was promised — verify downloads, not status codes.

## 7. Done when

Every slice logged in `dataquality/hunts.jsonl` (0 missing is a complete row and means "stop, report completeness"); accepted URLs have YAML + UID + `validate-yaml --id`; skipped duplicates listed with existing `id`; the two zero-entity subjects are non-zero or explicitly reported exhausted; `country-review` closes the sequence with the NSPD and data.gov.ru-successor flag questions answered.
