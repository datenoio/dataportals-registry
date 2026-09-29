# India data-catalog hunt — plan and prompt set

Written 2026-09-28 from a review of past sessions (Cursor chat DBs, Kimi and ZCode
session stores, the 732-row hunt log, CHANGELOG, and the session knowledge already
distilled in `docs/agents/improve.md`), plus a fresh gap analysis of the exports.

## 1. What the session review found

| Source | What it contributes |
|---|---|
| ~3,900 Cursor sessions (distilled in `docs/agents/improve.md`) | Which prompt shapes produce volume; India is priority #9: "State SDI, city CKAN, dataset-bearing university IRs. Duplicate-check `*.data.gov.in`". v1.18.0 India depth pass = +48 catalogs (19 ArcGIS Server REST dirs, India-WRIS, NWIC, TGRAC, HSAC, APCRDA, Bhukosh, VEDAS, Bhoomi, KGIS, NESDR, ICAR/IMD/INCOIS/NCPOR stack, CivicDataLab CKAN, Kerala Data Portal, IIPS, AIKosh). |
| Cursor local chats (`~/.cursor/chats`, two workspace folders, ~200 chats) | The `scheduled/IN` bulk-promotion pattern ("Analyze and update metadata for all records in scheduled/IN... change status to active and move to the proper dirs in entities"), NIUA `dataspace.niua.org` and Bhubaneswar One record-fix sessions. |
| Hunt log `dataquality/hunts.jsonl` (2026-09-16 → 09-28) | India slices already completed **within the 14-day `hunt.py prior` window**: `india-gtfs-landscape-leftovers` (09-21), `IN-subdomain-keywords` (09-22, 99 dupes — keyword-shape hosts are exhausted), `iudx` (09-24, +2 ADeX/GDI), `geoserver .in` (09-26, +2), `biodiv` (09-27, India Biodiversity Portal already in). Also: IBDC software def (+10 archives), `ogdindia` def (37 retagged). |
| Kimi sessions (`~/.kimi/sessions`) | Kimi Code CLI runs inside this repo (deep repo-analysis + docs sessions) — it can execute the full hunt loop, not just web research. |
| ZCode sessions (`~/.zcode/cli/agents`) | Parallel web-research subagent pattern (county GIS research returning evidence tables with HTTP status + software evidence) — the shape to reuse for ChatGPT/Kimi research prompts. |
| ChatGPT (no local store; wiring in `docs/discovery-agent-tools.md`) | ChatGPT = no repo access: Projects/Custom GPT with the shared system instructions + web search, returns a candidate table (name, URL, software.id guess, duplicate suspicion); the repo agent does dedupe + YAML. |
| CHANGELOG.md | OGD Platform India definition and the full v1.18 India inventory (above). |

**Do-not-repeat knowledge (rejections that cost past sessions time):**
`eprints.iisc.ac.in` (403), `portal.gsi.gov.in` (403), `portal.dmg.kerala.gov.in` /
`xnat.capestart.in` (login), `ksdi.kerala.gov.in` (no connections),
`tdh.dult-karnataka.com` (NXDOMAIN), TGSRTC open-data (timeout), HMRL / Kochi Metro
(single GTFS-zip pages, not catalogs), IUDX city tenants (NXDOMAIN — the central
catalogue covers them), `dspace.in` / `geodata.in` / `geohub.in` (parked), KMDL
drone-survey app, publication-only DSpace IRs (NII, Yenepoya, college libraries).
All 36 state/UT `*.data.gov.in` OGD instances are already registered — adding more
of that layer is wasted work.

## 2. India shape today (2026-09-28)

293 YAML entries (294 rows in exports). By type / custom share:

| Type | Rows | `custom` | Read |
|---|---:|---:|---|
| Geoportal | 102 | 19 | Largest layer; ArcGIS Server 43, igis 4 |
| Scientific | 100 | 35 | DSpace 28 (dataset-bearing filter already applied once) |
| Open data | 64 | 3 | OGD state layer complete; CKANs (opencity, CivicDataLab, India Data Portal, PMC, Telangana) in |
| Indicators | 18 | 16 | **Biggest shape hole** — only eSankhyiki, RBI DBIE, NDAP, UDISE+, UPAG + a handful of subnational |
| Microdata | 6 | 1 | NADA ×4 (incl. microdata.gov.in, censusindia), IIPS, CDS |
| API Catalog | 2 | 2 | OTD Delhi, API Setu directory |
| ML catalog | 2 | 2 | AIKosh, gts.ai |
| Metadata | 0 | — | None |

Subregion rows are thin outside MH (11), UP (10), KL (7), TS/GJ (6). 190 rows are
Federal-level owners.

## 3. Hunt plan (priority order)

Every phase is a **new slice name** — none collide with the 14-day `prior` blocks
(`IN`, `india` both return `decision: continue` as of today).

| # | Phase | Slice / kind | Why | Expected yield |
|---|---|---|---|---|
| 1 | State DES indicators | `IN-indicators-des` / country-indicators | 16 of 18 indicator rows are `custom`; only ~4 subnational (Maharashtra SDB, Bihar Data Lab, Kerala). Every state has a Directorate of Economics & Statistics with a data bank / statistical handbook portal | 15–30 |
| 2 | IGiS + smart-city GIS tenants | `igis` / software-instance → `IN-smartcity-gis` | `igis` (Scanpoint Geomatics/ISRO) was defined 2026-09-27 with only 4 instances and a clean fingerprint; Smart Cities Mission is a bounded ~100-city list; 19 geo `custom` rows are retag candidates | 5–20 + retags |
| 3 | Dataset-bearing university IRs | `IN-university-irs` / country-university-irs | 100 scientific rows vs ~1,100 HEIs; OpenDOAR lists ~600 Indian IRs but most are publication-only — the session lesson is to filter to Dataset type / research-data communities | 10–25 |
| 4 | Thin types (API, ML, metadata) | `IN-thin-types` / country-gap | API 2, ML 2, metadata 0. Candidates: api.data.gov.in as API Catalog, API Setu beyond the one directory, IndiaAI/Bhashini dataset catalogs, DCAT/SDMX metadata registries | 5–10 |
| 5 | Custom retag batches | `IN-geo-custom`, `IN-scientific-custom`, `IN-indicators-custom` / custom-review | 78 custom rows total; hostname/path clustering may surface NIC/state platforms worth software definitions (definition first, then instance hunt) | retags + 0–2 defs |
| 6 | City CKAN leftovers | `IN-city-opendata` / country-opendata | opencity.in covers ~5 cities; Smart Cities Mission data portals beyond `smartcities.data.gov.in`; municipal CKANs (Surat has data.gov.in tenant already) | 3–10 |

Sequencing note: run phases as **separate sessions** (repo rule: one hunt loop per
pass), in this order. Phase 5 runs after 1–4 add rows, so retags cover the new
`custom` entries too.

## 4. Preflight (run before every hunt)

In the repo shell (the one with `FOFA_EMAIL`/`FOFA_KEY` — they are **not** in a
bare shell; past sessions ran FOFA from the Cursor terminal):

```bash
python scripts/hunt.py prior --target IN-<slice>   # 14-day block check
python scripts/hunt.py budget                      # FOFA remain_api_data
```

If FOFA has no balance/keys: skip `search fofa`, use the ChatGPT/Kimi research
prompt to produce candidates, or paste queries into en.fofa.info manually. If
`datasets.duckdb` is locked, everything falls back to `full.parquet` — do not walk
YAML. Do not run `pytest` or `build` inside a hunt.

## 5. Prompt set

### Shared footer (append to every repo-agent prompt)

```text
Follow docs/agents/discover.md exactly: prior → budget → search fofa → probe →
ingest → log. Duplicate-check exports on hostname before probing. One GET per
path, stop on 401/403. software.id only with two matching signals, else custom.
is_national only for the official national product of that type. Promote
scheduled finds in the same session. Log one row in dataquality/hunts.jsonl
(0 missing is a complete hunt). Do not re-probe: eprints.iisc.ac.in,
portal.gsi.gov.in, ksdi.kerala.gov.in, tdh.dult-karnataka.com, IUDX city
tenants, dspace.in/geodata.in/geohub.in.
```

### Phase 1 — State DES indicators

**Repo agent (Cursor / ZCode / Kimi CLI):**

```text
Which India indicators catalogs are missing? Target slice IN-indicators-des.
Count existing indicators YAML for IN first: eSankhyiki, RBI DBIE, NDAP, UDISE+,
UPAG, SDG India Index, NPP, PPAC, Jal Jeevan, India KLEMS and IMF NSDP are in —
skip them. Hunt the state layer: Directorate of Economics and Statistics /
State Data Bank portals (the Maharashtra mahasdb and Bihar statedata patterns)
for the large states: TN, KA, UP, WB, RJ, MP, GJ, AP, TS, OD, KL, HR, PB, AS,
JH, CG, UK, HP. Accept live table databases / data banks / statistical
handbooks with a browsable catalog. Reject PDF-only publications, CMS pages,
and login dashboards. Place owners under IN/{ISO-3166-2}/indicators/ with
owner.location.level 30. Run the hunt.py loop and log kind country-indicators.
```

**ChatGPT / Kimi web-research (no repo):**

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-indicators
and https://datenoio.github.io/dataportals-registry/llms.txt
Find Indian state-level indicators/statistical data portals not in this list
(already registered: esankhyiki.mospi.gov.in, datarbi.org.in, ndap.niti.gov.in,
udiseplus.gov.in, upag.gov.in, mahasdb.maharashtra.gov.in, statedata.bihar.gov.in,
datahub.kerala.gov.in, ecostat.kerala.gov.in, databank.nedfi.com, npp.gov.in,
ppac.gov.in, iced.niti.gov.in, sdgindiaindex.niti.gov.in, ejalshakti.gov.in).
Focus on state Directorates of Economics and Statistics and State Data Banks for
the 20 largest states. Return a markdown table: name | url | owner | what tables
or datasets are visible | likely duplicate of any listed portal (by hostname)?
Do not invent registry uids or software ids. I will duplicate-check in the repo.
```

### Phase 2 — IGiS and smart-city GIS

**Repo agent:**

```text
Which igis catalogs are missing? Software-instance hunt, target igis.
Read data/software/geo/igis.yaml and its docs/software-index.md row first.
Existing instances: gissuratmunicipalorg, gisnnaligarhin, gisagrasmartcityltdnet,
gissmartcitymoradabadorg. FOFA: body="IGiS_Widget" && country="IN" (also try
body="Powered by Scanpoint Geomatics"). Then the bounded Smart Cities Mission
list (~100 cities) — check each smart-city SPV site for a public GIS portal,
plus the Scanpoint deployment page. Accept live public viewers; reject
login-only internal GIS. In the same session, review the 19 software.id=custom
India geoportals and retag any that load IGiS_Widget. Log kind software-instance.
```

**ChatGPT / Kimi web-research:**

```text
I maintain a registry of data portals. Find public GIS / geoportal deployments
in India built on IGiS by Scanpoint Geomatics (fingerprint: page loads
/CommonWidget/tools/IGiS_Widget/script/IGiS_Widget.js or credits
"Powered by Scanpoint Geomatics Ltd"). Already known: gis.suratmunicipal.org,
gis.nnaligarh.in, gis.agrasmartcityltd.net, gis.smartcitymoradabad.org.
Search smart-city SPV websites and municipal corporation sites. Return:
name | url | owner (city/SPV) | evidence for IGiS. Do not guess hosts; only
report URLs you actually saw in search results or pages.
```

### Phase 3 — Dataset-bearing university IRs

**Repo agent:**

```text
There are a lot of Indian universities and research organizations that could
have scientific data repositories that are not yet listed. Which of them are
missing? Target slice IN-university-irs. Count existing scientific YAML for IN
first (100 rows; 28 dspace, 7 eprints, 2 dataverse, ibdc 10). Sources: OpenDOAR
country facet filtered to Dataset content type, re3data country=India, OpenAIRE.
Accept ONLY repositories that list datasets (DSpace Dataset-type browse,
Dataverse, a research-data community, data deposit service). Reject
publication-only IRs — that class was bulk-removed before. eprints.iisc.ac.in
403s; do not retry. Probe DSpace /server/api. Log kind country-university-irs.
```

**ChatGPT / Kimi web-research:**

```text
Find Indian university and research-institute repositories that host RESEARCH
DATASET collections (not just publication PDFs) — DSpace with a Dataset type
browse, Dataverse, or a named research-data community. Return name | url |
institution | evidence that datasets (not only eprints/theses) are deposited.
Do not list: anything on data.gov.in, Indian Biological Data Centre archives,
ICAR-NBPGR, IMD, INCOIS, NCPOR, Climateverse — already registered.
```

### Phase 4 — Thin types (API, ML, metadata)

**Repo agent:**

```text
Missing India data catalogs — thin types only. Target slice IN-thin-types.
Current: API Catalog 2 (otd.delhi.gov.in, directory.apisetu.gov.in), ML 2
(aikosh, gts.ai), Metadata 0. Hunt: (a) government API directories/catalogs —
api.data.gov.in API listing as its own API Catalog if it has a browsable UI,
API Setu services beyond the one directory, state API marketplaces (e.g.,
MahaOnline, e-Pramaan-class portals with public API catalogs); (b) ML/AI
dataset catalogs — IndiaAI datasets, Bhashini corpus/datasets pages, NLP
consortium data, Kaggle-like government ML hubs with public listings; (c) any
DCAT/SDMX metadata registry with a public UI. Accept public catalogs only;
API gateways without a browsable catalog are rejects. Log kind country-gap.
```

**ChatGPT / Kimi web-research:**

```text
Find Indian government API directories and AI/ML dataset catalogs with public
listings. Already known: otd.delhi.gov.in, directory.apisetu.gov.in,
aikosh.indiaai.gov.in, gts.ai. Look for: api.data.gov.in public API catalog UI,
API Setu full service directory, IndiaAI / Bhashini / state AI-mission dataset
pages, SEBI/RBI/IRDAI developer or API portals with a browsable API list.
Return name | url | owner | what is listed | public without login (yes/no).
```

### Phase 5 — Custom retag

**Repo agent (run last):**

```text
Review custom India catalogs and identify new software definitions. Three
batches: IN-geo-custom (19 rows), IN-scientific-custom (35), IN-indicators-custom
(16). Cluster by hostname and page fingerprints. Add a software YAML only when
≥3 independent installations share a named product or a first-party vendor page
names it (state DES platforms and NIC products are candidates; one-off .gov.in
roots stay custom). If a new id is added: software YAML + discovery/harvest
headings + sync-software-maps in one change, then retag rows and run the
instance hunt for it. Log kind custom-review.
```

### Phase 6 — City open data (optional, after 1–5)

**Repo agent:**

```text
Which India city open-data portals are missing? Target slice IN-city-opendata.
NOT the *.data.gov.in layer (all 36 registered) and NOT smartcities.data.gov.in
(already in). Hunt independent city portals: opencity.in city CKANs (Bengaluru,
Chennai already in — find the rest of their catalog list), Pune PMC (in),
municipal data portals for Mumbai (BMC), Hyderabad, Ahmedabad, Delhi bodies
(OTD in; MCD/DJB data pages?). Accept CKAN/ODK-class catalogs with dataset
listings; reject single-page download lists. Log kind country-opendata.
```

### Utility prompts (from the session playbook, India-flavored)

```text
Review records at data/entities/IN and fix them
```
(live links, software probes vs guesses, owner names, endpoints after a 200,
is_national check — eSankhyiki is the only NSO indicators product with it)

```text
Review scheduled and promote if they are ok, otherwise remove them
```
(keep the queue at zero between releases; this is the exact prompt shape the
Cursor scheduled/IN sessions used)

```text
Update README and CHANGELOG
```
(after a batch, with exports rebuilt — only when you ask for a release)

## 6. Done-when

Each phase: every accepted URL has YAML + UID + `validate-yaml --id`, skipped
duplicates listed with existing ids, exhausted vendor lists reported complete
(0 missing), and one `hunts.jsonl` row with the slice name from section 3.
Whole plan done when phases 1–5 have logged rows and the IN type table in
section 2 has moved: indicators ≥ 35 with subnational coverage for the large
states, geo custom ≤ 10, scientific custom ≤ 25, and API/ML/metadata ≥ 5 rows.
