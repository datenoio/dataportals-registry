# Philippines (PH) catalog hunt — plan and prompt pack

Generated 2026-09-29 from past-session review. Working note, not published docs.

## 1. Session sources reviewed

| Source | What was found |
|--------|----------------|
| Cursor conversation index (`conversation-search.db`, ~3,900 indexed chats) | 4 PH sessions: *Missing geoportals in Philippines* (Aug 31, Sep 2), *Philippines local government geoportals* (Sep 13), *Philippines data catalog review* (Sep 20). Full transcripts recovered. |
| `dataquality/hunts.jsonl` (754 hunts) | 1 PH hunt: `country-gap / PH-subdomain-keywords` (Sep 20, +6). Recent country-review reference hunts: PK (Sep 29), IN (Sep 28–29), NG (Sep 29) — used as the template for slice-by-slice country reviews. |
| ZCode sessions (`~/.zcode/cli/rollout`, 2 recent + artifacts) | Sep 29 country-review sessions (PK/NG hunts in the log); model-io files hold tool traffic, verbatim user prompts not extractable. |
| ChatGPT desktop local cache | 23 conversation blobs, all Oct 2025, none registry-related — history is server-side. |
| Kimi desktop local storage | One unrelated conversation title. History is server-side. |
| Repo knowledge | `docs/agents/discover.md`, `docs/agents/improve.md`, `docs/discovery-agent-tools.md`, `.cursor/rules/catalog-discovery.mdc`. |

Because ChatGPT/Kimi keep no usable local history, their prompts below follow the repo's documented browser-agent recipe (`docs/discovery-agent-tools.md`) armed with the extracted Cursor/hunt-log knowledge.

## 2. Current PH state (2026-09-29)

68 entities, 0 scheduled. By type / software (DuckDB):

| Type | n | Software spread |
|------|--:|-----------------|
| Geoportal | 42 | arcgisserver 11, geonode 11, geoserver 4, custom 4, terria 3, stacserver 2, seasketch 2, others 5 |
| Scientific | 10 | ipt 3, custom 3, dataverse, dspace, gringlobal, opendaphyrax |
| Open data portal | 9 | custom 4, ckan 2 (data.gov.ph, ckandiplab), wordpress 2, dkan 1 |
| Indicators | 4 | pxweb 2 (OpenSTAT), custom 1 (BSP), imfnsdp 1 (NSDP) |
| Microdata | 3 | nada 2 (PSA DAP, LabStat), drupal 1 (PopArchive) |

**Thin types are all zero:** api, ml, search, metadata, marketplace, other.

Subregions in use: Federal, PH-00 (NCR), PH-01, PH-06, PH-09, PH-10, PH-11, PH-15, PH-40, PH-BUK, PH-BTG, PH-CAS, PH-PLW.

## 3. Already hunted — do not repeat

**LGU/municipal geoportals are saturated.** Sep 2 + Sep 13 sessions checked: FOFA GeoNode/GIS-portal/NextGIS + `gis.`/`geoportal.`/`gisportal.`/`maps.` title/host queries on `.gov.ph`; `geoportal.`/`gis.`/`cgis.`/`gismap.`/`maps.` across ~100 province and HUC domains (864 URLs); remaining RGIN regions; Ilocos Sur/Norte; Cagayan de Oro ULIS; Bacolod; Baguio maps; AcuGIS `*.webgis1.com`. Result: **0 missing**. Registered LGU set: Davao (gismap), Muntinlupa (cgis), Naga (NextGIS), Carmona (carmonagis.org), Bukidnon (gisportal+geonodetagabukid), Batangas (arcgis.com), plus RGIN regions 1/6/9 and Quezon City DRRIS. Do not re-run unless a new product/tenant list appears.

**Subdomain-keyword sweep done (Sep 20, +6):** crt.sh zone dumps (`%.gov.ph/.edu.ph/...` + 14 scoped agency base domains), urlscan `page.domain:{kw}.*.ph` for 89 keywords, ~75 hosts probed.

**Dead / do-not-reprobe (from that hunt):** dspace.dlsu.edu.ph, dhis2.ncp.org.ph, opendata.upd.edu.ph, sdg.neda.gov.ph, arcgis.up.edu.ph, repo.asti.dost.gov.ph, atlas.doh.gov.ph, map.doh.gov.ph, data.phl-microsat.upd.edu.ph (502), geo.bfar.da.gov.ph (502), data.research.philsa.gov.ph (403 WAF), archive.sws.org.ph (empty), gismaps.cagayandeoro.gov.ph (CMS), dataverse.ph (BPO company, not Dataverse).

**Permanent rejects:** SEAFDEC/UMIR/CPU/UPD-mainlib IRs (publication-only), GeoAnalyticsPH / HazardHunter / PlanSmart (analysis tools, not catalogs), DENR Databank + data.georisk.gov.ph 3DPH (login walls — stop on 401/403), `sdg.{earist,lyceum,unp,mpsc}` (campus info pages), osm.dswd.gov.ph.

## 4. Hunt sequence (ordered by expected yield)

One slice per session; run `python scripts/hunt.py prior --target PH.<slice>` first (14-day dedupe), follow the command card (`budget` → `search fofa|censys` → `probe` → `ingest` → `log`), promote in the same session, `validate-yaml --id`, log to `dataquality/hunts.jsonl`.

| # | Slice (hunt kind) | Why | Angle |
|---|--------------------|-----|-------|
| 1 | **Indicators depth** (`country-indicators`) | Only 4 records; recipe targets native products beyond OpenSTAT/NSDP/BSP | PSA SDG Watch / PSA provincial profiles, DOH health tables (FHSIS dashboards), DepEd education statistics, DOLE labor explorers, PIDS, NEDA, DTI, PHAP/private health; subnational (NCR, highly urbanized cities). Reject PDF-publication CMS sites. |
| 2 | **University IRs, dataset-bearing** (`university-ir`) | 10 scientific but IPT/herbaria-heavy; DSpace coverage untested with the Dataset-type test | OpenDOAR + re3data + OpenAIRE Graph `country:PH`, DSpace 7 `/server/api` with Dataset entityType/browse; Dataverse installations JSON. Past rejects (SEAFDEC etc.) stay rejected unless a dataset browse exists. dspace.dlsu is dead — skip. |
| 3 | **data.gov.ph harvest sources** (`national-harvest-sources`) | National CKAN exists (`datagovph`, is_national) but its harvest/organisations API was never swept — the single highest-yield recipe per improve.md | CKAN `package_search`/`harvest`/`organizations` API on data.gov.ph → origin hostnames → probe the **origin catalog UI**, not the harvest row. Accept independent CKAN/GeoNode/agency `/opendata` lists; reject XML feeds and slices of data.gov.ph itself. |
| 4 | **Thin types** (`country-gap`) | api/ml/metadata/search/other all 0 | DICT/eGov API directories, agency developer portals (`/developer`, swagger on `.gov.ph`), AI/ML dataset pages (DOST-AIDA?), DCAT/SDMX registries, agency "datasets" HTML lists (`Datasets list` type). FOFA: `title="swagger" && country="PH"`, `body="api-docs" && host=".gov.ph"`. |
| 5 | **Microdata leftovers** (`country-gap`) | 3 records; NADA/IHSN list may have more PH tenants | IHSN NADA catalog list, DOH/NEDA/OP-run surveys with public catalog UI. Reject login-gated survey systems (SurveySolutions-class). |
| 6 | **Country record review** (`country-review`) | PH was filled across many hunts; owners/is_national/endpoints never reviewed as a set | `Review records at data/entities/PH and fix them` checklist from improve.md (live link, software match, owner from site, is_national only for official products, endpoints only after 200). |

Skip geo except opportunistic re-checks of the two 502s (geo.bfar.da.gov.ph, data.phl-microsat) — one GET each, no sweep.

## 5. Prompt pack

### 5.1 ZCode / Cursor (repo open — the hunt sessions)

Paste one per session, in order. FOFA creds must be in the user env (`FOFA_EMAIL`/`FOFA_KEY`); Censys usually out of credits.

```text
Which Philippines indicators catalogs are missing?
Follow docs/agents/discover.md. Run scripts/hunt.py prior --target PH.indicators first.
Duplicate-check data/datasets/datasets.duckdb (or full.parquet if locked) for PH.
Existing: OpenSTAT (pxweb), BSP, IMF NSDP, eNutrition. Hunt native products:
PSA SDG Watch and provincial profile tables, DOH FHSIS/health dashboards, DepEd
education statistics, DOLE labor, PIDS, NEDA, DTI, plus city-level explorers.
Reject PDF-publication CMS pages and login dashboards. Promote finds in this
session, validate-yaml --id, and log hunt kind country-indicators.
```

```text
There are a lot of Philippines universities and research organizations that could
have scientific data repositories that are not yet listed. Which of them are missing?
Follow docs/agents/discover.md (country university IRs). Baseline: 10 PH scientific
records. Sources: OpenDOAR country facet, re3data, OpenAIRE Graph, Dataverse
installations JSON. Accept only IRs that list datasets (DSpace Dataset type browse,
Dataverse, research-data community). Previously rejected as publication-only:
SEAFDEC, UMIR, CPU, UPD main library — do not re-add unless a dataset browse exists.
dspace.dlsu.edu.ph is dead. Log hunt kind university-ir.
```

```text
Which data sources harvested by data.gov.ph are missing?
Follow docs/agents/discover.md (national harvest sources). Use the CKAN
harvest/organizations API on data.gov.ph, match origin hostnames against exports,
then probe the origin catalog UI (not the harvest row). Accept independent
CKAN/GeoNode/agency open-data lists. Reject XML dataset feeds and slices of
data.gov.ph itself. Log hunt kind national-harvest-sources.
```

```text
Which Philippines API catalogs, ML catalogs, and metadata catalogs are missing? All three types are 0 for PH.
Follow docs/agents/improve.md thin-types guidance. Check DICT and eGov API
directories, agency developer portals on .gov.ph, FOFA title="swagger" && country="PH"
and body="api-docs" && host=".gov.ph", plus any DCAT/SDMX registry UI. Also accept
agency "datasets" HTML lists as Datasets list. Reject per-service gateways and login
walls. Log hunt kind country-gap, target PH-thin-types.
```

```text
Which Philippines microdata catalogs are missing?
Baseline: PSA Data Archive and LabStat (NADA), Population Archive. Check the IHSN
NADA installation list and DOH/NEDA survey catalogs with public UI. Reject
login-gated survey collection systems. Log hunt kind country-gap, target PH-microdata.
```

```text
Review records at data/entities/PH and fix them
Use the country-review checklist in docs/agents/improve.md: live link (HTTPS),
status for dead hosts, software.id from a probe, owner name/link from the site,
coverage country/path match, endpoints only after a 200 on that path, api flag
consistent, properties.is_national only for the official national product of a type
(data.gov.ph, NAMRIA geoportal, PSA products). assign + validate-yaml --id on
touched files. Log hunt kind country-review.
```

### 5.2 Cursor (FOFA pass, after the above — only if slices 1–4 are thin)

```text
FOFA hunt for Philippine catalog hosts not yet registered. Censys is out of credits; use FOFA.
Run scripts/hunt.py budget, then one query at a time with --dedupe:
  title="CKAN" && country="PH"
  body="name=\"generator\" content=\"ckan" && country="PH"
  title="GeoNode" && country="PH"
  app="GeoServer" && country="PH"
  title="ArcGIS" && country="PH"
  body="OpenDataSoft" && country="PH"
  title="Dataverse" && country="PH"
  body="/server/api" && host=".edu.ph"   (DSpace 7)
Skip geo sweep conclusions already logged (LGU geoportals saturated Sep 13).
Probe candidates per docs/agents/discover.md, ingest, log kind country-gap.
```

### 5.3 ChatGPT (browser/web search, no repo — candidate tables only)

Start the thread with (per `docs/discovery-agent-tools.md`):

```text
Read https://datenoio.github.io/dataportals-registry/llms.txt
and https://datenoio.github.io/dataportals-registry/docs/discovery-indicators
Find indicator catalogs and statistical databases in the Philippines beyond the
national OpenSTAT (openstat.psa.gov.ph), Bangko Sentral, IMF NSDP, and eNutrition.
Look for PSA SDG Watch, DOH FHSIS/field health tables, DepEd education statistics,
DOLE labor statistics, PIDS, NEDA, and city-level (NCR, Cebu, Davao) data explorers.
Return a markdown table: name | url | evidence | proposed catalog_type | likely software.
A table of numbers users can query beats a PDF library. Do not invent registry uids.
I will duplicate-check in the repo myself.
```

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-scientific
Which Philippine universities or research agencies run data repositories that list
datasets (not publications)? Check DLSU, UP system (beyond the registered UP
Dataverse), Ateneo, UST, DOST-ASTI, SEAFDEC, PCAARRD. Return: name | url | evidence
of a dataset listing | why not publication-only. Known dead: dspace.dlsu.edu.ph,
repo.asti.dost.gov.ph, opendata.upd.edu.ph. dataverse.ph is a BPO company — not Dataverse.
```

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-opendata
List the organizations publishing into data.gov.ph (the national CKAN) that run their
own separate open-data or geodata site. Also check DICT/eGov API directories and any
Philippine government developer portal. Return: name | url | evidence. I will
duplicate-check against the registry exports.
```

Paste a PH CSV slice (`id`, `name`, `link`, `software`) into the thread so it stops proposing registered hosts.

### 5.4 Kimi (browser-capable, no repo — research + verification pass)

```text
You help maintain dataportals-registry, a registry of open data portals, geoportals,
scientific repositories, and indicators catalogs. Read
https://datenoio.github.io/dataportals-registry/llms.txt first.

Task: research Philippine government data infrastructure and return a candidate
table of data catalogs NOT in this list of already-registered hosts (I will paste it).
Focus: (1) statistical tables/dashboards of DOH, DepEd, DOLE, PSA beyond OpenSTAT;
(2) university repositories that list datasets; (3) agency GIS/data portals beyond
NAMRIA, DENR, DAR, DA, DSWD, PHIVOLCS, PhilSA, NHA (all registered); (4) any national
API directory or developer portal.

For each candidate open the site in the browser and verify: public catalog UI or
harvestable API, no login wall, not a PDF library or project page. Return:
name | url | what is listed there | owner agency | why it is a catalog.
Do not invent uids. Already-rejected (do not propose): GeoAnalyticsPH, HazardHunter,
PlanSmart, DENR Databank, data.georisk.gov.ph 3DPH, SEAFDEC/UMIR/CPU/UPD-mainlib
repositories, dataverse.ph.
```

Follow-up Kimi prompt once a shortlist exists:

```text
For each URL in this shortlist, open it and check whether it actually lists datasets
(browsable catalog or API), who owns it, and what software it runs (CKAN /api/3/action/
status_show, GeoNetwork /srv/eng/csw, ArcGIS /arcgis/rest/info?f=pjson, DSpace
/server/api, Dataverse /api/info/version). Return only the ones that pass, with the
probe evidence. Stop on 401/403 and mark them rejected.
```

## 6. PH-specific accept / reject

**Accept:** public catalog UI or harvestable API on `.gov.ph`/`.edu.ph`/agency domains; independent agency CKAN/GeoNode/`/opendata` lists; native statistical table DBs (queryable, not PDF); subregion placement for regional owners (`PH-00` NCR, `PH-01`..`PH-13`, `PH-40`, `PH-BUK` etc., `owner.location.level` 30).

**Reject:** PDF publication libraries and press-release CMS; analysis tools (GeoAnalyticsPH-class); login walls (DENR Databank, 3DPH) — stop on 401/403; campus SDG info pages; harvest rows inside data.gov.ph (probe the origin instead); publication-only IRs; city guesses — LGU geoportal market is already tenant-complete.

## 7. Done when

Every slice logged in `dataquality/hunts.jsonl` (0 missing is a complete row and means "stop, report completeness"); accepted URLs have YAML + UID + `validate-yaml --id`; skipped duplicates listed with existing `id`; final `country-review` pass closes the sequence.
