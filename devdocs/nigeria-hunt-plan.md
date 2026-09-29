# Nigeria data-catalog hunt — plan and prompt set

Written 2026-09-29 from a review of past sessions (Cursor conversation DB
`conversation-search.db`, ~3,900 sessions; Kimi `~/.kimi/sessions`, 16; ZCode
`~/.zcode/cli/agents`, 14; the 751-row hunt log `dataquality/hunts.jsonl`;
CHANGELOG; and the distilled playbook `docs/agents/improve.md`), plus a fresh
gap analysis of YAML and the DuckDB exports.

Companion documents: `devdocs/pakistan-hunt-plan.md` (same shape, PK),
`devdocs/india-hunt-plan.md` (IN).

## 1. What the session review found

| Source | What it contributes |
|---|---|
| Cursor conversation DB | Eight sessions touched Nigeria directly: a dedicated gap hunt (2026-08-23), a NG/EG/PK OD+IR+NSO sweep (08-26), the NSO table wave (08-26), the DHIS2 wave (08-21), African scientific repos (08-28), FENIX/CountrySTAT (08-24), procurement OCDS (09-22), central-bank data (09-03/09-13), geoportal coverage gaps (09-02), geographic gaps (09-24), the .ng ArcGIS TLD pass (09-26), and the custom-records-by-country review (09-27). |
| "Nigeria data catalogs missing" (Aug 23) | The foundational hunt. Had 24 NG-owned + 2 coverage-only. Added NCDC Data Portal (`dataportal.ncdc.gov.ng`, CKAN), CBN Statistics Database (`statistics.cbn.gov.ng/shop`), Nigeria SDG (`sdgs-nigeria.github.io`, Open SDG), and promoted Lagos Eko360 (`eko360.ng`). Fixed the Edo/Ogun misfile (`opendata.edostate.gov.ng` moved NG-OG → NG-ED) and the NBS NADA twin. Conclusions: `data.gov.ng` does not resolve (no national OGD portal); NASRDA "National GeoHub" is Moodle training; ~30 OpenDOAR university DSpace IRs are mostly theses/articles. |
| "Nigeria Egypt Pakistan tables" (Aug 26) | Added 5 live NG DSpace IRs (NLN `nigeriareposit.nln.gov.ng`, NgREN NIRIS, UniAbuja, UNILAG, OAU Ife) plus the NBS-linked Knoema products (`nigeriahealthatlas`, `nigeriaforeigntrade` opendataforafrica) and the NBS COVID ArcGIS Hub. Key finding: **Nigeria's advertised "Open Data Portal" is the Knoema site already registered** — no native NSO table engine (PxWeb/SuperWEB/.Stat) exists. |
| "Missing NSO table catalogs" (Aug 26) | Added `nigerianstatgovng` (NBS Data portal / eLibrary tables) as Indicators catalog. |
| "Missing DHIS2 data catalogs" (Aug 21) | Added `dhis2nigeriaorgng` (National HMIS, restricted) and `asceducationgovng` (ASC education EMIS). Both are DHIS2 logins kept as restricted per the Nepal pattern. |
| "African scientific data repositories" (Aug 28) | +3 NG IRs. ~70 vendor URLs were dead/Cloudflare-blocked/hijacked/login-walled; the session explicitly suggested **re-probing the dead Nigerian hosts** as a follow-up — never done. |
| "Missing procurement data catalogs" (Sep 22) | Named **NOCOPO (`nocopo.bpp.gov.ng`)** and the **Enugu** and **Cross River** state OCDS portals as live and unregistered — all three are still absent today (verified against YAML and exports). The Ebonyi/Osun/Anambra/Kogi e-procurement cluster was first rejected, then later extracted as software.id `bonmaximus` (5 NG rows now carry it). |
| "Geoportal coverage gaps" (Sep 2) | **Nigeria ranked #1 worldwide** on population × empty first-level units: "2 of 37 states (Ogun, Kaduna). Lagos, Abuja, Kano, Rivers empty." The session named the clean follow-up prompt: *Which Nigeria states and cities have geoportals that are missing?* — never run. |
| "ArcGIS server data catalogs" (Sep 26) | The `.ng` TLD pass. Added NIPOST Postcode GIS (`gispostcodegovng`). **FOFA technique documented**: the services-directory phrase is blind on `.ng`; the queries that returned hosts are in section 6 below. Rejected: `address.agis.fcta.gov.ng` and `geoint.dsa.mil.ng` (ArcGIS Server but token/empty folders), `gis.ncc.gov.ng` / `emaps.osgof.gov.ng` (no connect), `portal-bk.lagosstate.gov.ng` (ArcGIS cert, does not resolve), bare IPs. |
| "Data catalog geographic gaps" (Sep 24) | Nigeria 69 rows then — flagged in the "deepen national + capital open data" wave alongside Tanzania/DRC/Ethiopia, and among the largest countries with **zero local-government records** (also Sep 14). |
| "Custom records review by country" (Sep 27) | Nigeria listed among the largest countries still missing a custom-software pass: 22 custom rows then, concentrated in Open data (18). Never reviewed. |
| "Missing goaltracker" (Sep 3 + 24) | `nigeria.goaltracker.org` is 401 basic-auth — left out under the stop-on-401/403 rule. Do not retry. |
| "Missing FENIX CountrySTAT" (Aug 24) | Nigeria is a historical CountrySTAT participant; all hub URLs dead. Do not add. |
| Central-bank hunts (Sep 3 + 13) | CBN DataWarehousePro tenant (`/go/cbnstatistics`) already registered; CBN `statistics.cbn.gov.ng/shop` registered (now tagged `liveshop`). Nothing left in the CBN corner. |
| Hunt log `dataquality/hunts.jsonl` (751 rows) | **Zero `country-*` rows for NG.** Only the 2026-09-26 `software-instance | arcgisserver` row records the .ng TLD pass. `hunt.py prior --target NG` and `--target nigeria` both return `decision: continue`. Every phase below must log its row — log even a 0-find. |
| Kimi sessions (`~/.kimi/sessions`, 16) | No Nigeria work (one incidental constants-file mention). Kimi Code CLI runs inside this repo and can execute the full hunt loop, not just web research. |
| ZCode sessions (`~/.zcode/cli/agents`, 14) | No Nigeria work. Useful pattern: parallel web-research subagents returning evidence tables (HTTP status + software evidence) — the shape to reuse for the ChatGPT/Kimi research prompts below. |
| ChatGPT (no local store; wiring in `docs/discovery-agent-tools.md`) | ChatGPT has no repo access: use a Project/Custom GPT with the shared system instructions + web search; it returns a candidate table (name, URL, owner, evidence); the repo agent does dedupe + YAML. |
| CHANGELOG.md | v1.18.0 (2026-08-28) was the "India/Nigeria depth" release: the Aug 23–28 NG wave landed, and **36 India/Nigeria/Pakistan scheduled records were promoted** that cycle. |

**Do-not-repeat knowledge (rejections that cost past sessions time):**

Hosts and pages (do not re-probe, except the two explicitly allowed below):
`data.gov.ng` (does not resolve — no working national OGD portal; checked Aug 23
and Aug 26); NASRDA "National GeoHub" (Moodle training site, not a catalog);
the NBS NADA twin — the live host is `microdata.nigerianstat.gov.ng`, already
registered as `wwwnigerianstatgovng`; do not add a third NADA copy;
`data.iita.org` (IITA CKAN) is registered with owner **World** — do not re-add
as NG; `nigeria.goaltracker.org` (401 basic-auth, checked twice);
CountrySTAT/FENIX Nigeria hubs (dead, historical only);
CBN DataWarehousePro `/go/cbnstatistics` and `statistics.cbn.gov.ng/shop`
(both registered); `portal-bk.lagosstate.gov.ng` (ArcGIS certificate, does not
resolve); bare IPs from the Sep 26 FOFA pass (`beninelectric.local`,
`starfixgeo.com`); Enketo/cPanel/WordPress hosts and the `pci.gov.ng` page that
only embeds a REST URL.
Allowed **one final re-probe each, then close**: `address.agis.fcta.gov.ng`
(FCT AGIS cadastre — ArcGIS Server with token-required folders on Sep 26),
`geoint.dsa.mil.ng` (same), `gis.ncc.gov.ng` and `emaps.osgof.gov.ng`
(no connect on Sep 26), plus the newly inactive records
`dataportal.ncdc.gov.ng` (NCDC CKAN, added Aug 23, now inactive) and
`dashboard.neitigovng` (NEITI, inactive).
GRID3 is dead across four registered hosts (`grid3.gov.ng/datasets`,
`geonetwork.grid3.gov.ng`, `geonetwork.grid-nigeria.org`,
`geoserver.grid-nigeria.org`) — if a GRID3 successor portal exists it is a new
find, otherwise leave all four inactive.
Publication-only university IRs: the ~30 OpenDOAR Nigerian DSpace hosts are
mostly theses/articles — apply the dataset-bearing filter, do not bulk-add.

FOFA gotchas proven on Sep 26: `body="ArcGIS REST Services Directory"` returns
0 on `.ng` (index gap — use the manager title / `body="esri"` / IIS title
queries instead); `host=".ng"` matches `.ngo` and `.ngrok` — always pair with
`country="NG"` or a real suffix like `.gov.ng`; slow requests down, FOFA
rate-limits this pattern.

## 2. Nigeria shape today (2026-09-29)

71 YAML entries (exports show 70 — `nigeriaafricageoportalcom` is in YAML,
not yet exported; prefer YAML for "already added", exports for hostname dedupe).
By type / software:

| Type | Rows | Software mix | Read |
|---|---:|---|---|
| Open data portal | 22 | bonmaximus 5, custom 10, ckan 4, wordpress 2, budeshi 1 | **Procurement-skewed**: ~13 of 22 are state e-procurement/OCDS portals. Genuine general portals are few: `eko360.ng` (Lagos), `openstates.ng` (BudgIT), `sproutopencontentcom` (CKAN). 4 inactive (afrischolar CKAN, NCDC CKAN, Edo opendata, Ekiti sbsopendata). `data.gov.ng` dead — no national portal. |
| Geoportal | 14 (+1 in YAML) | geonetwork 4, geoserver 3, geonode 2, arcgisserver 1, arcgishub 1, datalibrary 1, wis20box 1, custom 1 | Only **2 states have geo**: Ogun (GeoNode) and Kaduna (`ipdata.kdsg.gov.ng`). Federal: SE4ALL GeoNode, eHealth Africa GeoNetwork+GeoServer, NIPOST ArcGIS, NiMet Maproom + WIS2, NBS COVID Hub, and the new `nigeria.africageoportal.com` (Esri, DCAT/OGC endpoints — NSDI-class). 5 inactive (GRID3 ×3 + relatives, BGS geodata centre). |
| Indicators catalog | 15 | knoema 6, dhis2 4, custom 2, datawarehousepro 1, liveshop 1, opensdg 1 | NBS stack complete (site + 6 Knoema tenants + Open SDG + NADA microdata). DHIS2: HMIS, ASC EMIS, NACA ENNRIMS, Lagos `eko360.org.ng`. CBN covered twice (DWP + liveshop). NEITI dashboard inactive. |
| Scientific data repository | 16 | dspace 11, eprints 2, elsevierdigitalcommons 1, ipt 1, birdmap 1 | Publication-leaning university IRs from the Aug waves; **dataset-bearing status not systematically checked**. GBIF IPT node and birdmap are the only true data repositories. |
| Microdata catalog | 2 | nada 2 | NBS NADA (active) + UI Ibadan NADA (inactive). |
| Datasets list | 1 | custom | `grid3.gov.ng/datasets` — inactive. |
| API / ML / Metadata / Search / Marketplace | 0 | — | All five types empty. |

Subregions: **13 of 37 units have records** (Federal 50; NG-LA 3, NG-EK 3,
NG-KD 2, NG-ED 2, NG-OG 2; NG-AB/AD/AN/BA/EB/JI/KO/OS 1 each). The 24 empty
units: **NG-FC (Abuja FCT)**, NG-AK, NG-BE, NG-BO, NG-BY, NG-CR, NG-DE, NG-EN,
NG-GO, NG-IM, NG-KE, NG-KN (Kano), NG-KT, NG-KW, NG-NA, NG-NI, NG-ON, NG-OY,
NG-PL, NG-RI (Rivers), NG-SO, NG-TA, NG-YO, NG-ZA.

Quality flags a review should fix: 12 inactive records; `is_national: true`
on three records including **two** indicators catalogs (`nigerianstatgovng`
and `appdatawarehouseprocomgocbnstatistics`) — only one official product per
type; `eko360ng` vs `eko360orgng` are two different Lagos products on
lookalike domains (custom opendata vs DHIS2 indicators) — verify both owner
strings say Lagos.

## 3. Hunt plan (priority order)

Every phase is a **new slice name** — `hunts.jsonl` has zero NG country rows,
so nothing collides; `prior --target NG*` returns `decision: continue`.

| # | Phase | Slice / kind | Why | Expected yield |
|---|---|---|---|---|
| 1 | State + FCT geoportals | `NG-state-geo` / country-geoportals | Rank-1 gap worldwide since Sep 2 (2 of 37 units). Lagos, Abuja, Kano, Rivers empty. FOFA `.gov.ng` queries from Sep 26 were only partially mined (`title="IIS Windows Server" && host=".gov.ng"` = 77 hosts, `host="gis." && host=".gov.ng"` = 72 — the ArcGIS subset was worked, the rest never triaged). crt.sh state-suffix enumeration never run for NG. | 3–10 |
| 2 | State statistics / indicators | `NG-state-stats` / country-indicators | State bureaus of statistics beyond Lagos (eko360 in): Kaduna, Kano, Rivers, Oyo, Anambra… ; National Population Commission census data portal; state SDG dashboards; state EMIS/health DHIS2 beyond the two federal ones. NBS federal stack is complete — do not re-add. | 3–8 |
| 3 | Open-data depth + named procurement leftovers | `NG-opendata-depth` / country-opendata | Three named live gaps from Sep 22: **NOCOPO** (`nocopo.bpp.gov.ng`), **Enugu** and **Cross River** state OCDS portals — still unregistered. Plus remaining state OCDS portals with real dataset listings, Kano/Rivers/Oyo open-data pages, FCT. One re-probe each for NCDC CKAN and NEITI (both inactive). Do not re-probe `data.gov.ng`. | 3–8 |
| 4 | Dataset-bearing scientific IRs | `NG-university-irs` / university-ir | 16 scientific rows are publication-leaning; the dataset-bearing filter was never applied systematically. OpenDOAR/re3data/OpenAIRE NG facets + research institutes (NIMR, NIPRD, ARCN agri institutes, NASRDA R&D — not the Moodle GeoHub). One re-probe of the dead NG hosts from Aug 28. | 0–5 |
| 5 | Thin types | `NG-thin-types` / country-gap | API, ML, metadata, search, marketplace all 0; datasets list 1 (inactive). Candidates: government/developer API portals (NIBSS, NITDA, CBN developer), GitHub awesome-lists of Nigerian datasets, DCAT/SDMX registries. | 0–4 |
| 6 | Custom confirmation (run last) | `NG-custom-confirm` / custom-review | ~14 `custom` rows (10 opendata, 2 indicators, 1 geo, 1 datasets list). The Sep 27 country review wave skipped Nigeria. Confirm the remaining e-procurement customs cluster to nothing beyond bonmaximus/budeshi; NBS site and KADPPA map stay custom barring a named product. | 0 + retags ≤ 2 |

Sequencing: separate sessions (repo rule: one hunt loop per pass), phases 1–3
first (geo is the ranked hole; stats and open data have named gaps). Phase 6
runs last so it covers any new `custom` rows phases 1–5 added. A country
record review (`Review records at data/entities/NG and fix them`) fits after
phase 6 to clear the section-2 quality flags.

## 4. Preflight (run before every hunt)

In the repo shell that has `FOFA_EMAIL`/`FOFA_KEY` (they are **not** in a bare
shell; past sessions ran FOFA from the Cursor terminal):

```bash
python scripts/hunt.py prior --target NG-<slice>   # 14-day block check
python scripts/hunt.py budget                      # FOFA remain_api_data
```

If FOFA has no balance/keys: substitutes are crt.sh hostname patterns
(`%.gov.ng`, `%.%state.gov.ng` — e.g. `%.lagosstate.gov.ng`,
`%.ogunstate.gov.ng`, `%.edostate.gov.ng` — one label at a time; broad queries
rate-limit) and urlscan searches. If `datasets.duckdb` is locked, fall back to
`data/datasets/full.parquet`; remember YAML is one row ahead of exports right
now (`nigeriaafricageoportalcom`) so dedupe `.ng` hosts against YAML too.
Do not run `pytest` or `build` inside a hunt.

Owner conventions for new state rows: `owner.type: Regional government`,
`owner.location.level: 30` + `subregion: NG-XX` (ISO 3166-2, full list in
`data/reference/subregions/ISO3166-2.CSV` — note Kano is **NG-KN**, Abuja FCT
is **NG-FC**), same in `coverage`. Federal products stay level 20.
`is_national: true` only for the official national product of a type — for NG
that class is the NBS products (already flagged); state portals and the
africageoportal tenant are `false`.

## 5. Prompt set

### Shared footer (append to every repo-agent prompt)

```text
Follow docs/agents/discover.md exactly: prior → budget → search fofa → probe →
ingest → log. Duplicate-check exports on hostname before probing (YAML is one
row ahead of exports: nigeriaafricageoportalcom). One GET per path, stop on
401/403. software.id only with two matching signals, else custom. is_national
only for the official national product of that type (for NG that is the NBS
class already flagged; state portals never). Promote scheduled finds in the
same session. Log one row in dataquality/hunts.jsonl (0 missing is a complete
hunt) — NG has zero logged country rows, so log even a 0-find.
Do not re-probe: data.gov.ng, NASRDA National GeoHub (Moodle), the NBS NADA
twin (microdata.nigerianstat.gov.ng is registered), data.iita.org (owner
World), nigeria.goaltracker.org (401), CountrySTAT/FENIX NG hubs (dead),
app.datawarehousepro.com/go/cbnstatistics and statistics.cbn.gov.ng/shop
(registered), portal-bk.lagosstate.gov.ng (no DNS), bare IPs from the Sep 26
FOFA pass, Enketo/cPanel/WordPress embed-only hosts, pci.gov.ng.
One final re-probe each, then close either way: address.agis.fcta.gov.ng,
geoint.dsa.mil.ng, gis.ncc.gov.ng, emaps.osgof.gov.ng, dataportal.ncdc.gov.ng,
dashboard.neitigovng.
FOFA: body="ArcGIS REST Services Directory" is blind on .ng — use
body="esri" && host=".gov.ng", title="ArcGIS" && country="NG",
port="6443" && title="ArcGIS" && country="NG", cert="arcgis" && country="NG",
title="IIS Windows Server" && host=".gov.ng". Never use bare host=".ng"
(matches .ngo/.ngrok) — pair with country="NG" or the .gov.ng suffix.
```

### Phase 1 — State + FCT geoportals

**Repo agent (Cursor / ZCode / Kimi CLI):**

```text
Which Nigeria states and cities have geoportals that are missing? Target slice
NG-state-geo. Count existing NG geo YAML first: only Ogun
(gis.ogunstate.gov.ng, GeoNode) and Kaduna (ipdata.kdsg.gov.ng) have state geo;
federal has SE4ALL GeoNode, eHealth Africa GeoNetwork+GeoServer, NIPOST
ArcGIS, NiMet maproom+wis2box, NBS COVID Hub, nigeria.africageoportal.com —
skip them. 24 units are empty: FCT, Akwa Ibom, Benue, Borno, Bayelsa, Cross
River, Delta, Enugu, Gombe, Imo, Kebbi, Kano, Katsina, Kwara, Nasarawa, Niger,
Ondo, Oyo, Plateau, Rivers, Sokoto, Taraba, Yobe, Zamfara. Do exactly four
things: (1) triage the unworked FOFA hits from the 26 September .ng pass —
title="IIS Windows Server" && host=".gov.ng" (77) and host="gis." &&
host=".gov.ng" (72) were only checked for ArcGIS; re-run and classify the
rest; (2) crt.sh enumeration of %.{state}state.gov.ng for the empty states
plus %.fcta.gov.ng, labels gis, maps, geoportal, data, geo — one label at a
time; (3) one re-probe each of address.agis.fcta.gov.ng, geoint.dsa.mil.ng,
gis.ncc.gov.ng, emaps.osgof.gov.ng, then close them; (4) Lagos geoportal
specifically (Nigeria's largest city has zero geo records) — LASG GIS /
Lagos State GIS Authority, portal-bk.lagosstate.gov.ng stays closed (no DNS).
Accept public REST/viewer catalogs (ArcGIS Server with non-empty public
folders, GeoServer, GeoNode, Hub). Reject login/token hosts, empty folders,
CMS pages, static map images. State owners: Regional government, level 30,
subregion NG-XX (Kano=NG-KN, FCT=NG-FC). Run the hunt.py loop and log kind
country-geoportals.
```

**ChatGPT / Kimi web-research (no repo):**

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-geoportals-sdi
and https://datenoio.github.io/dataportals-registry/llms.txt
Find public GIS / geoportal deployments by Nigerian state governments and the
Abuja FCT that publish browsable map or dataset catalogs. Already tracked (do
not repeat): gis.ogunstate.gov.ng, ipdata.kdsg.gov.ng, data.nigeriase4all.gov.ng,
gis.postcode.gov.ng, nigeria.africageoportal.com, maproom.nimet.gov.ng,
wis2.nimet.gov.ng, gis-geonetwork/gis-geoserver.ehealthafrica.org, the NBS
COVID hub. Priority states: Lagos, Kano, Rivers, Oyo, FCT Abuja, Enugu, Delta,
Anambra. Return a markdown table: name | url | owner | software guess
(ArcGIS/GeoServer/GeoNode/custom) | evidence it is a public catalog (not a
project page or login). Only report URLs you actually saw in search results or
pages. Do not invent registry uids or software ids.
```

### Phase 2 — State statistics / indicators

**Repo agent:**

```text
Which Nigeria state statistics portals are missing? Target slice
NG-state-stats. Count existing NG indicators YAML first: NBS site
(nigerianstatgovng), 6 opendataforafrica Knoema tenants, sdgs-nigeria.github.io,
4 DHIS2 (dhis2nigeria.org.ng, asc.education.gov.ng, ennrims.naca.gov.ng,
eko360.org.ng), CBN ×2 — all in, skip them. Hunt: state bureaus of statistics
beyond Lagos (Kaduna, Kano, Rivers, Oyo, Anambra, Enugu, Delta…), state SDG
support dashboards, the National Population Commission census/data portal
(nationalpopulation.gov.ng family), state education/health EMIS with public
dashboards, NBS state-level products not already registered. Accept live table
databases / data banks / indicator dashboards with a browsable catalog (DHIS2
logins qualify as restricted, per the dhis2nigeriaorgng pattern). Reject
PDF-only publication pages, CMS pages, login-only staff tools. State owners:
Regional government, level 30, subregion NG-XX. Federal level 20.
is_national stays false (the NBS products hold the national flags). Log kind
country-indicators.
```

**ChatGPT / Kimi web-research:**

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-indicators
and https://datenoio.github.io/dataportals-registry/llms.txt
Find Nigerian state-level and federal statistics data portals not in this list
(already registered: nigerianstat.gov.ng, microdata.nigerianstat.gov.ng,
nigeria/nso-nigeria/mof-nigeria/nigeriahealthatlas/nigeriaforeigntrade/
nigeriainfohighway.opendataforafrica.org, sdgs-nigeria.github.io,
dhis2nigeria.org.ng, asc.education.gov.ng, ennrims.naca.gov.ng, eko360.org.ng,
app.datawarehousepro.com/go/cbnstatistics, statistics.cbn.gov.ng/shop).
Focus on: state bureaus of statistics (any of the 36 states), National
Population Commission census data, state SDG dashboards, state health/education
DHIS2 with public views. Return a markdown table: name | url | owner | what
tables or datasets are visible | likely duplicate of a listed portal (by
hostname)? Only report URLs you actually saw. Do not invent registry uids.
```

### Phase 3 — Open-data depth + procurement leftovers

**Repo agent:**

```text
Which Nigeria open-data portals are missing? Target slice NG-opendata-depth.
Registered general portals: eko360.ng, openstates.ng, db.sproutopencontent.com,
plus 13 state e-procurement/OCDS portals (5 bonmaximus, budeshi Kaduna, and
customs for Bauchi/Edo/Ogun/Ekiti×2/Adamawa/Jigawa/Lagos PPA/govspend).
data.gov.ng is dead — do not re-probe. Three named live gaps from the
22 September procurement session, still unregistered — verify and add first:
(1) NOCOPO nocopo.bpp.gov.ng (Bureau of Public Procurement national OCDS
portal); (2) Enugu state OCDS/e-procurement portal; (3) Cross River state
OCDS/e-procurement portal. Then: remaining state OCDS portals with real
dataset listings (accept only browsable data/OCDS records, reject tender-list
HTML pages), Kano/Rivers/Oyo/FCT open-data initiatives, NITDA / Digital
Economy ministry data pages. One re-probe each of the inactive
dataportal.ncdc.gov.ng (NCDC CKAN) and dashboard.neitigovng (NEITI) — promote
back to active if live, else leave inactive and close. Accept CKAN/DKAN/uData-
class catalogs and OCDS record browsers; reject PDF libraries and single-page
download lists. Log kind country-opendata.
```

**ChatGPT / Kimi web-research:**

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-opendata
Find Nigerian open-data portals with public dataset listings, especially:
NOCOPO (nocopo.bpp.gov.ng — confirm it is live and lists OCDS data), Enugu and
Cross River state open-contracting portals, any Kano / Rivers / Oyo / FCT Abuja
open-data portals, NITDA or Federal Ministry of Communications dataset pages,
and civic-tech data hubs (BudgIT openstates.ng and govspend.ng are already
registered — do not repeat). Return name | url | owner | what datasets are
listed | public without login (yes/no). Only report URLs you actually saw in
search results or pages.
```

### Phase 4 — Dataset-bearing scientific IRs

**Repo agent:**

```text
Which Nigeria scientific data repositories are missing? Target slice
NG-university-irs. Count existing scientific YAML for NG first (16 rows: 11
DSpace incl. unilag/ui/uniabuja/oauife/unn/nln/ngren/fuoye/bells, 2 EPrints,
dc.cbn.gov.ng, GBIF IPT, birdmap). These skew publication-only — the
dataset-bearing filter was never applied. Sources: OpenDOAR country facet
filtered to Dataset content type, re3data country=Nigeria, OpenAIRE Graph,
Dataverse installations JSON. Beyond universities check research institutes:
NIMR, NIPRD, ARCN/NARIs agriculture data, NASRDA research data (NOT the
National GeoHub — Moodle training, rejected), NITEC/NCC R&D, and the IITA
siblings (IITA itself is registered with owner World — do not re-add as NG).
One re-probe of the dead Nigerian hosts from the 28 August African-repos
session, then close them. Accept ONLY repositories that list datasets (DSpace
Dataset-type browse, Dataverse, a research-data community, a data deposit
service). Reject publication/thesis-only IRs. Probe DSpace /server/api. Log
kind university-ir.
```

**ChatGPT / Kimi web-research:**

```text
Find Nigerian university and research-institute repositories that host
RESEARCH DATASET collections (not just publication PDFs or theses) — DSpace
with a Dataset type browse, Dataverse, Figshare tenant, or a named
research-data community. Return name | url | institution | evidence that
datasets (not only eprints/theses) are deposited. Do not list (already
registered): ir.unilag.edu.ng, ir.library.ui.edu.ng, repository.ui.edu.ng,
repository.uniabuja.edu.ng, ir.oauife.edu.ng, www.repository.unn.edu.ng,
nigeriareposit.nln.gov.ng, niris.ngren.edu.ng, repository.fuoye.edu.ng,
ir.bellsuniversity.edu.ng, eprints.abuad.edu.ng, eprints.lmu.edu.ng,
dc.cbn.gov.ng, repo.cbn.gov.ng, ipt-nigeria.gbif.fr, nigeria.birdmap.africa,
data.iita.org. Do not list thesis/publication-only repositories.
```

### Phase 5 — Thin types (API, ML, metadata, search, marketplace)

**Repo agent:**

```text
Missing Nigeria data catalogs — thin types only. Target slice NG-thin-types.
Current: API Catalog 0, ML 0, Metadata 0, Search 0, Marketplace 0, Datasets
list 1 (grid3.gov.ng/datasets — inactive; one re-check for a GRID3 successor,
else leave). Hunt: (a) government/developer API directories — NIBSS, NITDA,
CBN developer portals, any public API catalog UI on gov.ng hosts (gateways
without a browsable catalog are rejects); (b) ML/AI dataset catalogs —
Nigeria AI collective / university AI labs dataset pages; (c) DCAT/SDMX
metadata registries with a public UI; (d) Datasets lists — GitHub inventories
of Nigerian datasets (awesome-list pattern), curated data lists on
research/NGO sites. Accept public listings only. Log kind country-gap.
```

**ChatGPT / Kimi web-research:**

```text
Find Nigerian government API directories, developer portals with browsable
API catalogs, AI/ML dataset collections about Nigeria, and curated inventories
of Nigerian datasets (GitHub awesome-lists and NGO-maintained lists count).
Return name | url | owner | what is listed | public without login (yes/no).
Do not list opendataforafrica tenants, eko360.ng, openstates.ng, govspend.ng —
already registered. Only report URLs you actually saw.
```

### Phase 6 — Custom confirmation (run last)

**Repo agent:**

```text
Review custom Nigeria catalogs and confirm or retag. Target slice
NG-custom-confirm. ~14 custom rows: 10 opendata (eko360ng, openstatesng,
wwwgovspendng, eprocurement Bauchi/Edo/Ogun, ocdsbppekitistategovng,
bigfutportalazurewebsitesnet, wwwdueprocessjggovng, wwwocdsbppadamawastategovng),
2 indicators (nigerianstatgovng, dashboardneitigovng-inactive), 1 geo
(ipdatakdsggovng), 1 datasets list (grid3govng-inactive). Known conclusions to
respect: the Bon Maximus e-procurement cluster was already extracted (5 rows
now bonmaximus) — check whether the remaining state e-procurement customs are
the same product (retag) or genuinely bespoke (stay custom); the NBS site
stays custom unless a named product is identifiable. Add a software YAML only
when ≥3 independent installations share a named product or a first-party
vendor page names it. If nothing qualifies, report that and log kind
custom-review with 0 added — that is a complete hunt.
```

### Utility prompts (session playbook, Nigeria-flavored)

```text
Review records at data/entities/NG and fix them
```
(12 inactive records to confirm; fix the double `is_national: true` on
indicators — `nigerianstatgovng` vs `appdatawarehouseprocomgocbnstatistics`,
only one official product per type; verify the two Lagos `eko360` records
carry distinct owner strings; HTTPS/trailing-slash cleanup per the review
checklist in docs/agents/improve.md)

```text
Review scheduled and promote if they are ok, otherwise remove them
```
(the queue is at ~10 records, none NG today; keep it at zero between releases)

```text
Update README and CHANGELOG
```
(after a batch, with exports rebuilt — only when you ask for a release; the
README Nigeria counts and the YAML/export divergence clear then)

## 6. Done-when

Each phase: every accepted URL has YAML + UID + `validate-yaml --id`, skipped
duplicates listed with existing ids, exhausted sources reported complete
(0 missing), and one `hunts.jsonl` row with the slice name from section 3 —
NG currently has zero logged country rows, so even a 0-find phase must log.

Whole plan done when phases 1–6 have logged rows and the type table in
section 2 has moved: geoportals ≥ 17 with at least 4 new states covered
(Lagos/Kano/Rivers/FCT resolved one way or another), indicators ≥ 18 with
≥ 2 state bureaus, the three named Sep 22 procurement gaps (NOCOPO, Enugu,
Cross River) registered or documented dead, scientific dataset-bearing status
documented (even if 0 new), thin types ≥ 1 or documented empty, and the
six allowed re-probes closed either way.
