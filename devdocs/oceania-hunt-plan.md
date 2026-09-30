# Oceania hunt plan (working note, 2026-09-30)

Plan and prompt set for hunting data catalogs across Oceania, distilled from:

- `docs/agents/improve.md` — playbook distilled from ~3,900 past Cursor sessions (what moved the needle, anti-patterns, prompt templates that work).
- `dataquality/hunts.jsonl` — 795 logged hunts (2026-09-16 → 2026-09-30), including all prior Oceania passes.
- Past Kimi/Codex sessions of 2026-09-15 → 2026-09-19 (AU indicators ×5 passes, PG indicators/geoportals/opendata/scientific, AU FOFA subdomain gap hunt).
- Live DuckDB gap queries against `data/datasets/datasets.duckdb` (2026-09-30).

## What past sessions already did in Oceania (do not repeat blindly)

| Date | Hunt | Result |
|------|------|--------|
| 2026-09-17 | `country-indicators AU` ×5 passes | +43 (My School, ComparED, AEDC, SEIFA, JSA, NCVER, AIHW, PBS/MBS dashboards, …) |
| 2026-09-17 | `country-indicators PG` ×2 passes | +6 (PNG SDG OpenSDG, BPNG QEB, PNG Elections Database) |
| 2026-09-17 | `country-geoportals PG` ×2 passes | +1; crt.sh enumerated 869 `gov.pg` hosts — most geo-looking hosts dead |
| 2026-09-17 | `country-opendata PG` | 0 — `data.gov.pg` / `opendata.gov.pg` do not resolve; OGP commitment portal still in development |
| 2026-09-17 | `country-scientific PG` (university IRs) | +1 (re3data 0, Dataverse 0, OpenAIRE journals only) |
| 2026-09-19 | `country-gap AU` FOFA subdomain hunt (`subdomain_keywords_curated.csv`, `host=<kw>.` on `.au`) | +2 |

Lessons carried over from past sessions:

- Vendor/tenant lists and graph dumps beat "Google every city". For Oceania the equivalent lists are: SPC Pacific Data Hub tenants, SPREP `*-data.sprep.org` country portals, POPGIS `*.popgis.spc.int` tenants, Digital Earth Pacific, national harvest APIs (data.gov.au, data.govt.nz).
- Microstates: skip university-IR hunts (Kiribati-class rule in improve.md); yield is regional products (SPREP/POPGIS) already registered, plus NSO pages and SDG portals.
- A 0-missing logged hunt is a complete result — PG opendata is done until `data.gov.pg` goes live.
- Don't repeat a software-instance hunt from the last two weeks; the AU FOFA subdomain pass was 2026-09-19.

## Current coverage (DuckDB, 2026-09-30)

| CC | Total | Shape (type:count) | Gap read |
|----|------:|--------------------|----------|
| AU | 881 | geo 534, scientific 181 (76 custom!), indicators 83 (55 custom!), opendata 71, metadata 5, api 3, microdata 1, ml 1 | Dense. Real work = **custom retags** (131 custom rows), thin microdata/api/ml |
| NZ | 278 | geo 203, scientific 51, indicators 11, opendata 5, api 4 | **Shape hole**: geo-heavy, indicators/opendata thin for a Tier-1 open-data country |
| PG | 15 | geo 6, indicators 6, scientific 2 (custom), opendata 1 | Thin everywhere; scientific custom retag; NSO/central bank depth |
| FJ | 23 | geo 17, indicators 3, opendata/microdata/scientific 1 each | Shape hole: indicators + scientific (USP!) |
| WS | 11, VU 9, NC 18, TO 6, CK 6, FM 6, PW 6, SB 3, KI 4, TV 4, NR 3, MH 2, NU 1, PF 1, WF 0 | mostly SPREP/POPGIS regional products | Microstate pass: NSO sites, SDG portals, climate/disaster portals |
| Oceania (regional folder) | 31 | SPC/SPREP/Digital Earth Pacific | Quality issues found (below) |

Data-quality issues spotted while gap-querying (Phase 0 disposition):

1. ~~**POPGIS tenants misfiled under `NC`**~~ — **checked 2026-09-30: not a bug.** `coverage` is per-country and correct; `owner.location.country = NC` is SPC's HQ (Nouméa). No action.
2. **Staging/test hosts registered**: `geonode-uat.pacificdata.org` (UAT), `tds-test.pacificdata.org` — **removed 2026-09-30**.
3. `geoserver.sprep.org` placeholder name/owner — **fixed 2026-09-30** ("SPREP GeoServer", owner SPREP; `validate-yaml` passes).
4. Scheduled queue stale Oceania entries — **cleared 2026-09-30** (both were duplicates of existing entities; 16 dupes removed queue-wide).
5. US-affiliated Pacific (AS, GU, MP) filed under `US/` (e.g. `geohubepaasgov` American Samoa EPA GeoHub) — correct per registry convention; hunt them as US subregions if at all.

## Phase 0 — Hygiene first (one session) — ✅ DONE 2026-09-30

Results (logged in `dataquality/hunts.jsonl` as `country-review/Oceania` and `scheduled-review/queue`):

- **Scheduled queue**: both Oceania entries (`accessnricatalogue`, `datasetsoceanumio`) probed live but were already in entities — duplicates. `remove_scheduled_duplicates.py` cleared them plus 14 more stale records queue-wide (49 country folders remain).
- **Staging/test entries removed**: `data/entities/Oceania/geo/geonodeuatpacificdataorg.yaml` (self-described UAT staging copy of the registered production NEXUS `geonodepacificdataorg`) and `data/entities/Oceania/scientific/tdstestpacificdataorg.yaml` (test server, DNS dead).
- **`geoserverspreporg` fixed**: placeholder name ("GeoServer Project / deploying organization not specified") and owner replaced with SPREP — "SPREP GeoServer", owner Secretariat of the Pacific Regional Environment Programme. Site is live but behind a Cloudflare bot wall (403 to scripted GETs); `validate-yaml --id geoserverspreporg` passes. Note: `geoserverapiaspreporg` (Apia host) is `status: inactive` — possible same deployment, unverifiable through the bot wall; revisit with a real browser.
- **POPGIS "misassignment" was NOT a bug** (plan corrected): the ten `*.popgis.spc.int` rows have `coverage` in their own countries; `owner.location.country = NC` is correct because SPC is an international organization headquartered in Nouméa, New Caledonia. No file moves needed. Lesson for future gap queries: use `coverage`, not `owner.location.country.id`, for country-shape reads.

Original task list (kept for the record):

```text
Review scheduled and promote if they are ok, otherwise remove them
```
(scope: `data/scheduled/AU/scientific/accessnricatalogue.yaml` and `data/scheduled/NZ/scientific/datasetsoceanumio.yaml`)

~~Review records at data/entities/NC~~ — **not needed**: POPGIS owner=NC is correct (SPC HQ); coverage countries already right.

~~Review records at data/entities/Oceania~~ — **done 2026-09-30** (results above). Remaining follow-up: verify in a real browser whether `geoserver.sprep.org` and inactive `geoserver-apia.sprep.org` are the same deployment (Cloudflare bot wall blocks scripted checks).

## Phase 1 — Australia (dense: quality and thin types, not more geo)

AU is 61% geoportal. Past indicators passes landed +43; a 6th indicators pass only if a *new product* appears. Highest yield now:

1. Custom retag (131 custom rows: 76 scientific, 55 indicators):

```text
Review custom scientific catalogs and identify new software definitions
```
(scope: `data/entities/AU` — cluster 76 custom scientific rows by hostname/path; AU research sector uses named platforms: Figshare institutional, Dataverse, Omeka, REDCap-adjacent, AARNet/CloudStor, ARDC products. Add a software YAML only for named products with ≥3 installs or a first-party product page.)

```text
Review custom indicators catalogs and identify new software definitions
```
(scope: `data/entities/AU` — 55 custom indicator rows; look for shared dashboard products: Power BI embedded NSW/VIC/QLD explorers, .Stat Suite, PxWeb, InstantAtlas.)

2. National harvest-source hunt (never run for AU):

```text
Which data sources harvested by data.gov.au are missing?
```
(data.gov.au is CKAN — use its harvest/organization listing; probe origin catalog UIs, not dataset feeds. Expect state CKANs, agency data hubs, council open-data sites.)

3. Thin types:

```text
Missing Australia data catalogs
```
(then follow the type-shape table: hunt **microdata** (ADA/Dataverse at ANU, ABS DataLab-adjacent public catalogs), **API catalogs** (api.gov.au, state API directories), **ML catalogs** — do not add more geo.)

4. Optional repeat (only after 2026-10-03, two weeks since the FOFA pass):

```text
Missing Australia data catalogs — FOFA subdomain hunt, second sweep
```
(`python scripts/hunt.py search fofa 'host="data." && country="AU"' --dedupe` style; reuse `data/reference/subdomain_keywords_curated.csv` keywords with new host prefixes; log as `country-gap AU`.)

## Phase 2 — New Zealand (shape hole: indicators + opendata) — 🟡 IN PROGRESS

**Session 1 done 2026-09-30** (logged `country-shape/NZ`, +7): added `educationcountsgovtnz` (MoE), `nzhealthsurveyexplorer` + `whakamauadashboard` (MoH Shiny), `lawaorgnz`, `data1850nz` (NZIER), `communityinsightsorgnz` (Tableau), `transportgovtnzstats` (MoT Tableau). Dupe skipped: `data.mfe.govt.nz`. Rejected: `knowledgeauckland.org.nz` (publication hub), `healthspace.ac.nz` (DNS dead), `nzdotstat.stats.govt.nz` (retired). Blocker: data.govt.nz CKAN API sits behind an Incapsula wall — harvest-source hunt below needs a real-browser session or a different mirror. NZ indicators went 11 → 18.

Remaining prompts:

```text
Missing New Zealand data catalogs
```
(type-shape: hunt opendata + indicators, stop on geo. Local-government open data beyond the registered ArcGIS Hubs; Stats NZ native table products; MBIE/MoH/MoE sector dashboards.)

```text
Which New Zealand indicators catalogs are missing?
```
(Stats NZ Tatauranga Aotearoa products, Infoshare/ASEAN-style table DBs, NZ.Stat successors, Wellbeing/Child Poverty dashboards, Reserve Bank of NZ, subnational council indicator explorers. Skip IMF NSDP if present.)

```text
Which data sources harvested by data.govt.nz are missing?
```
(data.govt.nz harvests agency and council catalogs — probe origin UIs.)

```text
There are a lot of New Zealand universities and research organizations that could have scientific data repositories that are not yet listed. Which of them are missing?
```
(8 universities + CRIs: check each for a dataset-bearing IR — Figshare/DSpace Dataset type only; publication-only IRs are out of scope. e.g. Lincoln, Waikato, NIWA, GNS, Landcare, Plant & Food.)

## Phase 3 — PNG + Fiji (depth where institutions exist)

PNG (15 total) and Fiji (23) have real NSOs, central banks, and universities — past passes only scratched indicators.

```text
Missing Papua New Guinea data catalogs
```
(NSO PNG native tables, Bank of PNG beyond QEB (was Cloudflare-403 — retry from browser or skip), UPNG research repository, NARI agricultural data, IMF eLibrary/NSDP check, climate portals. `data.gov.pg` is confirmed dead — do not re-add; note in log.)

```text
Which Papua New Guinea indicators catalogs are missing?
```
(third pass: only new products — Treasury 2025 budget dashboards if live, DHIS2 health, education EMIS.)

```text
There are a lot of Fiji universities and research organizations that could have scientific data repositories that are not yet listed. Which of them are missing?
```
(**USP — University of the South Pacific** is regional (12 member countries) and the single biggest Pacific IR target; also Fiji National University. Dataset-bearing only. Place USP regional outputs under `FJ/` with coverage notes or `Oceania/` if multi-country.)

```text
Which Fiji indicators catalogs are missing?
```
(Fiji Bureau of Statistics native tables, RBF statistics, FHIS/DHIS2, SDG OpenSDG portal if distinct from registered.)

## Phase 4 — Pacific microstates (one combined pass, regional products already registered)

WS, VU, TO, CK, FM, PW, SB, KI, TV, NR, MH, NU, PF, WF. SPREP environment portals and POPGIS tenants are already in; per improve.md, **skip university-IR hunts** here. What remains: NSO sites, SDG portals, central bank bulletins with data catalogs, climate/disaster (NDMO) portals, fisheries (FFA) country pages.

```text
Missing Samoa data catalogs
```
```text
Missing Vanuatu data catalogs
```
```text
Missing Tonga data catalogs
```
(one country per session; for each: count YAML by type first, hunt the missing type — typically a native NSO table DB or an SDG OpenSDG instance. Accept public catalog UIs only; reject PDF publication pages.)

```text
Which data catalogs from https://stats.pacificdata.org are missing?
```
(named-directory pass over the Pacific Data Hub — its per-country stats tenants `stats-{cc}.pacificdata.org` beyond the registered Nauru one; dedupe against exports first.)

```text
Which data catalogs from https://pacific-data.sprep.org are missing?
```
(SPREP regional portal directory — leftover country/sector portals beyond the 20 `*-data.sprep.org` already registered.)

Combined microstate sweep (single session, bounded):

```text
Missing Pacific microstate data catalogs: Solomon Islands, Kiribati, Tuvalu, Nauru, Marshall Islands, Niue, French Polynesia, Wallis and Futuna
```
(For each: SDG OpenSDG portal, NSO site catalog, NDMO/geohazard viewer. PF/WF are French collectivities — check INSEE/ISPF PF native products and French harvest (data.gouv.fr) origins. Expect 0–3 per country; log 0-missing as complete. Do not add gazettes or legislation portals.)

## Phase 5 — Regional Oceania / IGO-style

The `Oceania/` folder (31 YAML) covers SPC/SPREP cores; regional IGOs still have leftovers. Treat like the Sep-15 IGO wave:

```text
Which Pacific Community (SPC) data catalogs are missing?
```
(division-level: Geoscience GEM beyond registered GeoServers, PCCOS ocean portals, SDD statistics leftovers, educational/PHD data portals.)

```text
Which Pacific Islands Forum Secretariat (forumsec.org) data catalogs are missing?
```
```text
Which FFA (Pacific Islands Forum Fisheries Agency) data catalogs are missing?
```
```text
Which USP (University of the South Pacific) data catalogs are missing?
```
(USP library IR, Pacific research data collections — regional; place under `Oceania/` or `FJ/`.)

```text
Which data catalogs from https://www.pacificgeoportal.com are missing?
```
(named directory; already registered itself — hunt its member/node links for unregistered national SDI nodes.)

## Operating rules for every session (from past-session anti-patterns)

1. Start with `python scripts/hunt.py prior --target TARGET` and follow the `next:` command card (`budget` → `search` → `probe` → `ingest` → `log`). Do not write ad-hoc FOFA clients or probe scripts.
2. Dedupe against exports (`hunt.py dedupe` / DuckDB; fall back to `full.parquet` on lock). Never walk YAML to search.
3. Stage with `add-single --scheduled` / `add-batch`, **promote in the same session** after a live GET; don't leave the queue full.
4. `is_national: true` only for the country's official catalog of that type — not for every `.gov` host.
5. Accept public catalog UIs / harvest APIs. Reject: gazettes/legislation portals, PDF publication pages, login walls (401/403 → stop), staging/UAT hosts, dataset-level records, directory-only hubs.
6. Log every hunt to `dataquality/hunts.jsonl` via `python scripts/hunt.py log --kind … --target … --added N` — including 0-missing (it documents completeness).
7. Don't repeat a hunt kind+target from the last two weeks unless a new list URL exists (check `hunts.jsonl` first).
8. After any batch touching YAML ahead of exports, note it; rebuild `data/datasets/` only at release time.

## Suggested execution order

1. Phase 0 hygiene (fixes + scheduled emptying) — 1 session.
2. Phase 2 NZ shape (biggest structural hole) — 3–4 sessions.
3. Phase 3 PG/FJ depth — 3–4 sessions.
4. Phase 1 AU custom retags + harvest sources — 3–5 sessions.
5. Phase 4 microstates — 3–4 sessions.
6. Phase 5 regional IGOs — 2–3 sessions.
