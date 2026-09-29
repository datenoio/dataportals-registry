# Pakistan data-catalog hunt — plan and prompt set

Written 2026-09-28 from a review of past sessions (Cursor conversation DB, Kimi and
ZCode session stores, the 741-row hunt log, CHANGELOG, and the session knowledge
distilled in `docs/agents/improve.md`), plus a fresh gap analysis of the exports.

## 1. What the session review found

| Source | What it contributes |
|---|---|
| Cursor conversation DB (`conversation-search.db`, ~3,900 sessions) | Three dedicated Pakistan sessions: two geoportal hunts (2026-08-31, 09-02) and one keyword/certificate hunt (2026-09-22), plus Pakistan mentions in the 09-25 ArcGIS hunt, 09-22 indicators review, and the 09-24 geographic/topical gap analyses. |
| "Missing geoportals in Pakistan" (Aug 31 + Sep 2, five passes) | Filled the provincial geo layer: added PULSE (`lispulsegoppk`), Punjab Planning Support System (`pmulgcddgoppk`), Sindh Irrigation GIS (`apphicsindhpk`), Balochistan GLIS (`glisssbachanet`), KP Forest Monitoring (`kpfmspakorg`), GB mines map, Koh-e-Atlas Karachi. **Concluded the city/district geoportal layer is empty**: Karachi (KMC/KDA), Lahore (LDA), Islamabad (CDA), Rawalpindi, Faisalabad, Multan, Gujranwala, Quetta, Hyderabad, Sialkot, Gwadar have no independent public municipal GIS — local GIS is either a provincial hub, login-only (CDA IPVS, dmis.pdma), PDFs (PMDFC), or dead hosts. Do not re-walk the metros. |
| "Missing data catalogs in Pakistan" (Sep 22) | Curated-subdomain-keyword + crt.sh certificate pass. Added the 8 public PBS dashboards under `*.data.gov.pk` (economic, trade, na, dashboards, social, pslm-sdgs, migration, naagri) + `mc2020pbosgovpk`. **Unfinished thread**: broad crt.sh queries for `gis`, `opendata`, `maps`, `geoportal`, `repository` labels on `.pk` timed out and were never enumerated. FOFA had no credits that day — crt.sh + urlscan were the substitutes. |
| "Missing ArcGIS server catalogs" (Sep 25) | Added `wrisbwrdspgobpk` (Balochistan WRIS, `:6443/arcgis/rest/services`) and `emsiescocompk` (IESCO grid, same pattern). **Technique**: the documented services-directory query does not see `.pk` hosts — use the manager title, the admin stylesheet, and the ArcGIS response header with `country="PK"`; bare PK IPs reverse to ISP names, skip them; some .pk ArcGIS TLS certs omit an intermediate (curl warns, directory is still public). |
| "Indicators catalog review" (Sep 22) / "Record pattern analysis" | The 8 `data.gov.pk` dashboards are one publisher (PBS) on a **single-tenant custom platform (Bootstrap + Highcharts + DataTables)** — not a shared product, no software definition warranted; they stay `custom`. |
| "Data catalog geographic gaps" + "Registry topical gaps analysis" (Sep 24) | Pakistan flagged twice: missing **types**, not just volume (37 rows then, 39 now), and named in the dataset-bearing-repository wave: "Dataset-bearing repositories for Vietnam, **Pakistan**, Indonesia, Iran, Iraq, Myanmar, Uzbekistan. Keep publication-only university repositories out." Recommended prompt shape: *Which Pakistan scientific repositories are missing?* |
| Hunt log `dataquality/hunts.jsonl` (741 rows) | **Zero rows logged for any PK target** — the Cursor sessions predate/didn't use the hunt loop. `hunt.py prior --target PK` and `--target pakistan` both return `decision: continue` (clean 14-day window). Every phase below must log its row. |
| Kimi sessions (`~/.kimi/sessions`, 20) | No Pakistan work; Kimi Code CLI runs inside this repo (deep repo-analysis + docs sessions) — it can execute the full hunt loop, not just web research. |
| ZCode sessions (`~/.zcode/cli/agents`, 38) | No Pakistan work; parallel web-research subagent pattern (e.g. NJ county geoportals, returning evidence tables with HTTP status + software evidence) — the shape to reuse for ChatGPT/Kimi research prompts. |
| ChatGPT (no local store; wiring in `docs/discovery-agent-tools.md`) | ChatGPT = no repo access: Projects/Custom GPT with the shared system instructions + web search, returns a candidate table (name, URL, software.id guess, duplicate suspicion); the repo agent does dedupe + YAML. |
| CHANGELOG.md | v1.18.0 (2026-08-28) added 4 Pakistan catalogs: KP Bureau of Statistics (`kpbosgovpk`), NIPS public microdata (`wwwnipsorgpk`), SDPI Data for Development (`d4dpakcom`), Forman Digital Repository; **36 India/Nigeria/Pakistan scheduled records promoted** the same cycle. |

**Do-not-repeat knowledge (rejections that cost past sessions time):**

Hosts and pages (do not re-probe): `data.gov.pk` root and `datafest` (404) — the live
layer is the `*.data.gov.pk` dashboard subdomains, all 8 registered; `dssi`, `dcrates`,
`erp.data.gov.pk` (login/survey-entry); `lmis.gov.pk` (sign-in); `portal.nsd.gov.pk`
(signup gateway); `census23.pbos.gov.pk`, `psi.pbos.gov.pk` (dead);
`repository.lahoreschool.edu.pk` (publication-only IR); `gismaps.pulse.gop.pk`,
`arcsrv.pulse.gop.pk` (dead; same PULSE product); `gismaps.punjab-zameen.gov.pk`
(PLRA/PULSE stack, empty folders); `askfortaqseem.pulse.gop.pk` (PULSE viewer);
`giss1.mineral.gov.pk` (every folder token-walled); `emsgis.fesco.com.pk` (timeout);
`click.gos.pk/gis` (CMS page); `pndkp.gov.pk/gis-hub` (HTTP 500 project page);
`pmdfc.punjab.gov.pk` (PDF maps); `geotagging.wasafaisalabad.gop.pk` (Odoo staff page);
`sindhzameen.gos.pk` (static images); `dmis.pdma.gos.pk` (login); KMC/KDA/SBCA/QDA/LDA
homepages (no GIS catalog); `geonode.pakistangis.org` (timeout ×3);
`tbttp.gov.pk` (dead/500); `ehsaaseshajar.kp.gov.pk` (timeout); `nfmspak.org`
(national, same stack as KPMS); `punjabeforest.gop.pk` locality maps (static PNG);
`sindhforests.gov.pk` GIS page (links to .bmp); `ftms.punjabeforest.gop.pk` (login);
PBS `/gis/` (about page); CDA IPVS (login); KWSSIP GIS (password); WSSP Peshawar
(static); RUDA maps (PDF gazettes); FDA schemes ("Map" column in a table);
`emap.pk` / Zameen PlotFinder (commercial property maps); Survey of Pakistan / NSDI
geoportal (internal/LAN — a 2026–2027 plan as of Aug 2026, worth one re-check now);
AJK Web AppBuilder links on `lupajk.gov.pk` (items inaccessible; same LUP catalog).
`agrigis.kp.gov.pk` and `pdaapp.kp.gov.pk/find-plot` were scheduled on Sep 2 but never
promoted (agrigis timed out twice before; pdaapp is a single-plot lookup) — one final
re-probe each is allowed, then close them.
Sindh HIC contour/crop/ACWA apps are the same irrigation product as `apphicsindhpk`.
The 16 PMDFC Punjab Cities Program municipalities have PDF service maps only.

## 2. Pakistan shape today (2026-09-28)

39 YAML entries. By type / software:

| Type | Rows | `custom` | Read |
|---|---:|---:|---|
| Indicators catalog | 17 | 12 | 8 PBS `data.gov.pk` dashboards (single-tenant custom), NSDP (imfnsdp), SBP EasyData (oracleapex), KP BOS, NODP education, Karandaaz, StatSilk, 2× DHIS2 |
| Geoportal | 14 | 6 | 5 ArcGIS Server (incl. 2 on `:6443`), landfolio KP cadastre, seasketch MSP, PULSE/PSS provincial hubs |
| Scientific data repository | 4 | 0 | 2 DSpace (PASTIC, Forman), 2 Elsevier Digital Commons (AKU, IBA) — **all publication-leaning; flagged as a shape hole** |
| Open data portal | 3 | 1 | opendata.com.pk (CKAN, LUMS NCBC), opendata.kp.gov.pk (CKAN), d4dpak.com (SDPI) |
| Microdata catalog | 1 | 1 | NIPS only |
| API / ML / Metadata / Search / Marketplace / Datasets list | 0 | — | All six types empty |

Subregions: Federal 24, PK-KP 5, PK-PB 3 (PULSE, PSS, DHIS2 — for ~110M people),
PK-BA 2, PK-SD 2 (for ~48M people), PK-JK 1, PK-GB 1, PK-IS 1. Only KP has both a
statistical-bureau portal and an open-data portal. Punjab has no Punjab Bureau of
Statistics root portal registered (only the `mc2020` subdomain — and that YAML is
filed under `Federal/` with a Punjab owner). Sindh and Balochistan bureaus of
statistics are absent entirely.

## 3. Hunt plan (priority order)

Every phase is a **new slice name** — `hunts.jsonl` has no PK rows at all, so nothing
collides; `prior --target PK` / `pakistan` return `decision: continue`.

| # | Phase | Slice / kind | Why | Expected yield |
|---|---|---|---|---|
| 1 | Provincial statistics layer | `PK-provincial-stats` / country-indicators | Punjab (~110M) has 3 rows, Sindh (~48M) 2, Balochistan 2. Punjab Bureau of Statistics root portal (only `mc2020.pbos.gov.pk` is in), Sindh Bureau of Statistics, Balochistan Bureau of Statistics, provincial EMIS (nodp.gov.pk is federal-education only), PDMA dashboards, PMD/IRSA water-climate data portals | 5–15 |
| 2 | Dataset-bearing scientific IRs | `PK-university-irs` / country-university-irs | Named in the Sep 24 gap wave ("Pakistan has 4 out of 37"). ~200 HEC universities, 4 repos. Filter OpenDOAR/re3data/OpenAIRE to Dataset-type collections | 5–15 |
| 3 | Geo leftovers | `PK-geo-leftovers` / country-geoportals + software-instance | Two explicitly unfinished threads: (a) crt.sh broad labels `gis`/`opendata`/`maps`/`geoportal`/`repository` on `.pk` timed out Sep 22 and were never enumerated; (b) FOFA `.pk` technique from Sep 25 (manager title / admin stylesheet / ArcGIS response header — services-directory search is blind on .pk). Plus one NSDI/Survey-of-Pakistan re-check and the two closed re-probes (agrigis, pdaapp). City/district layer is verified empty — do not re-walk | 0–8 |
| 4 | Open-data depth | `PK-opendata-depth` / country-opendata | opendata.com.pk is one CKAN with orgs — check whether Punjab/Sindh org layers are separate portals; KP is the only provincial portal registered; national portal is dead (do not re-probe `data.gov.pk` root) | 2–8 |
| 5 | Thin types | `PK-thin-types` / country-gap | API, ML, metadata, datasets-list all 0. Candidates: SBP Raast developer portal, government API directories, GitHub dataset inventories (Datasets list type), NCBC-LUMS AI dataset pages | 0–5 |
| 6 | Custom confirmation | `PK-custom-confirm` / custom-review | 17 `custom` rows. The 12 custom indicators are the PBS single-tenant platform (Sep 22 conclusion: no shared product — stays custom). Confirm geo customs cluster to nothing new; expected mostly a documented no-op | 0 + retags ≤ 2 |

Sequencing: separate sessions (repo rule: one hunt loop per pass), phases 1–3 first
(indicators and IRs are the flagged shape holes; geo has the unfinished threads).
Phase 6 runs last so it covers any new `custom` rows phases 1–5 added.

## 4. Preflight (run before every hunt)

In the repo shell that has `FOFA_EMAIL`/`FOFA_KEY` (they are **not** in a bare shell;
past sessions ran FOFA from the Cursor terminal):

```bash
python scripts/hunt.py prior --target PK-<slice>   # 14-day block check
python scripts/hunt.py budget                      # FOFA remain_api_data
```

If FOFA has no balance/keys: the Sep 22 session's substitutes were crt.sh hostname
patterns (`%.gov.pk`, `%.gos.pk`, `%.gop.pk`, `%.gob.pk`) and urlscan searches — both
worked without keys (crt.sh broad queries rate-limit; query one label at a time).
If `datasets.duckdb` is locked, fall back to `full.parquet`. Do not run `pytest` or
`build` inside a hunt.

Owner conventions for new provincial rows (copy `kpbosgovpk`): `owner.type: Regional
government`, `owner.location.level: 30` + `subregion: PK-PB / PK-SD / PK-BA / PK-KP /
PK-GB / PK-JK / PK-IS`, same in `coverage`. Federal PBS products stay level 20 and
`is_national: false` (thematic dashboards; the NSO summary is `nsdppbsgovpk`).

## 5. Prompt set

### Shared footer (append to every repo-agent prompt)

```text
Follow docs/agents/discover.md exactly: prior → budget → search fofa → probe →
ingest → log. Duplicate-check exports on hostname before probing. One GET per
path, stop on 401/403. software.id only with two matching signals, else custom.
is_national only for the official national product of that type (for PK that is
nsdppbsgovpk-class NSO products, not the thematic data.gov.pk dashboards).
Promote scheduled finds in the same session. Log one row in dataquality/hunts.jsonl
(0 missing is a complete hunt) — PK has zero logged rows, so log even a 0-find.
Do not re-probe: data.gov.pk root/datafest, dssi/dcrates/erp.data.gov.pk, lmis.gov.pk,
portal.nsd.gov.pk, census23/psi.pbos.gov.pk, repository.lahoreschool.edu.pk,
gismaps+arcsrv.pulse.gop.pk, gismaps.punjab-zameen.gov.pk, askfortaqseem.pulse.gop.pk,
giss1.mineral.gov.pk, emsgis.fesco.com.pk, click.gos.pk/gis, pndkp.gov.pk/gis-hub,
pmdfc.punjab.gov.pk, geotagging.wasafaisalabad.gop.pk, sindhzameen.gos.pk,
dmis.pdma.gos.pk, geonode.pakistangis.org, tbttp.gov.pk, ehsaaseshajar.kp.gov.pk,
nfmspak.org, punjabeforest locality maps, sindhforests.gov.pk GIS page,
ftms.punjabeforest.gop.pk, PBS /gis/, CDA IPVS, KWSSIP, WSSP, RUDA, FDA schemes,
emap.pk/Zameen, AJK Web AppBuilder items, the Sindh HIC sibling apps.
```

### Phase 1 — Provincial statistics layer

**Repo agent (Cursor / ZCode / Kimi CLI):**

```text
Which Pakistan provincial statistics portals are missing? Target slice
PK-provincial-stats. Count existing PK indicators YAML first: the 8 *.data.gov.pk
PBS dashboards, nsdppbsgovpk, easydatasbporgpk, mc2020pbosgovpk, kpbosgovpk,
nodpgovpk, portalkarandaazcompk, statsilkcompakistan, dhispbcom, dhiscmugovpk are
in — skip them. Hunt: Punjab Bureau of Statistics main portal (pbos.gov.pk root,
only the mc2020 subdomain is registered), Sindh Bureau of Statistics,
Balochistan Bureau of Statistics, provincial EMIS (Punjab/Sindh/Balochistan/KP —
nodp.gov.pk is federal education only), provincial PDMA flood/disaster data,
Pakistan Meteorological Department and IRSA public data portals, provincial SDG
support-unit dashboards. Accept live table databases / data banks / indicator
dashboards with a browsable catalog. Reject PDF-only publications, CMS pages,
login dashboards. Provincial owners: Regional government, level 30, subregion
PK-PB/PK-SD/PK-BA/PK-KP. Run the hunt.py loop and log kind country-indicators.
```

**ChatGPT / Kimi web-research (no repo):**

```text
Read https://datenoio.github.io/dataportals-registry/docs/discovery-indicators
and https://datenoio.github.io/dataportals-registry/llms.txt
Find Pakistani provincial and federal statistics data portals not in this list
(already registered: economic/trade/na/dashboards/social/pslm-sdgs/migration/
naagri.data.gov.pk, mc2020.pbos.gov.pk, nsdp.pbs.gov.pk, easydata.sbp.org.pk,
kpbos.gov.pk, nodp.gov.pk, portal.karandaaz.com.pk, pakistan.statsilk.com,
dhis.pb.com.pk, dhis.cmu.gov.pk). Focus on: Punjab Bureau of Statistics main
portal, Sindh Bureau of Statistics, Balochistan Bureau of Statistics, provincial
EMIS portals, PDMA / PMD / IRSA public data. Return a markdown table: name | url |
owner | what tables or datasets are visible | likely duplicate of any listed
portal (by hostname)? Do not invent registry uids or software ids. I will
duplicate-check in the repo.
```

### Phase 2 — Dataset-bearing university IRs

**Repo agent:**

```text
Which Pakistan scientific data repositories are missing? Target slice
PK-university-irs. Count existing scientific YAML for PK first (4 rows:
repositorypasticgovpk, digitalrepositoryfccollegeedupk, ecommonsakuedu,
iribaedupk). Sources: OpenDOAR country facet filtered to Dataset content type,
re3data country=Pakistan, OpenAIRE. Pakistan has ~200 HEC-recognized universities
plus PARC/PAEC/SUPARCO research institutes — check NUST, Quaid-i-Azam, Punjab
University, LUMS, UET, GCU Lahore, COMSATS, Aga Khan (beyond eCommons), NARC/
PARC agriculture data, PAEC INIS class repos. Accept ONLY repositories that list
datasets (DSpace Dataset-type browse, Dataverse, a research-data community, a
data deposit service). Reject publication-only IRs — repository.lahoreschool.edu.pk
was rejected for exactly that; HEC Pakistan Research Repository is thesis-only
EPrints, same class. Probe DSpace /server/api. Log kind country-university-irs.
```

**ChatGPT / Kimi web-research:**

```text
Find Pakistani university and research-institute repositories that host RESEARCH
DATASET collections (not just publication PDFs or theses) — DSpace with a Dataset
type browse, Dataverse, or a named research-data community. Return name | url |
institution | evidence that datasets (not only eprints/theses) are deposited.
Do not list: repository.pastic.gov.pk, Forman Digital Repository, eCommons AKU,
IBA repository, anything on data.gov.pk, NIPS — already registered. Do not list
thesis/publication-only repositories (e.g. HEC Pakistan Research Repository,
repository.lahoreschool.edu.pk).
```

### Phase 3 — Geo leftovers (unfinished threads only)

**Repo agent:**

```text
Missing Pakistan geoportals — leftovers only. Target slice PK-geo-leftovers.
The city/district layer was verified empty over five passes in late August/early
September; do NOT re-walk Karachi/Lahore/Islamabad/other metros. Do exactly four
things: (1) finish the crt.sh enumeration that timed out on 22 September — query
%.gov.pk, %.gos.pk, %.gop.pk, %.gob.pk, %.gkp.pk for the labels gis, opendata,
maps, geoportal, repository, one label at a time (broad queries rate-limit);
(2) FOFA with country="PK" using the technique that worked on 25 September — the
services-directory query is blind on .pk, so search the ArcGIS manager title, the
admin stylesheet, and the ArcGIS response header; skip bare IPs (they reverse to
ISP names); (3) one live check whether Survey of Pakistan / NSDI geoportal went
public (it was internal/LAN, planned 2026–2027); (4) single re-probe of
agrigis.kp.gov.pk and pdaapp.kp.gov.pk/find-plot (scheduled once, never promoted),
then close them either way. Accept public REST/viewer catalogs; reject
login/token hosts. Log kind country-geoportals.
```

**ChatGPT / Kimi web-research:**

```text
Find public GIS / geoportal deployments in Pakistan that launched or became
public since September 2026. I already track: lis.pulse.gop.pk (Punjab PULSE),
pmu-lgcdd.gop.pk (Punjab PSS), app.hicsindh.pk, glis.ssbacha.net, KP minerals
cadastre, KP Forest Monitoring, AJK LUP GIS portal, wris.bwrdsp.gob.pk and
ems.iesco.com.pk ArcGIS REST, cybgis.net.pk, GB mines map, seasketch.org
Pakistan MSP. Especially check: Survey of Pakistan NSDI geoportal status,
Islamabad CDA open GIS, Karachi metropolitan GIS, any new provincial ArcGIS Hub.
Return name | url | owner | evidence it is a public catalog (not a project page).
Only report URLs you actually saw in search results or pages.
```

### Phase 4 — Open-data depth

**Repo agent:**

```text
Which Pakistan open-data portals are missing? Target slice PK-opendata-depth.
Registered: opendatacompk (CKAN, LUMS NCBC), opendatakpgovpk (CKAN),
d4dpakcom (SDPI). The national portal data.gov.pk is dead — its live layer is
the 8 dashboard subdomains already registered as indicators; do not re-probe.
Hunt: opendata.com.pk organizations/datasets — are there Punjab, Sindh, or city
collections that are substantial separate portals rather than one CKAN tenant?
Punjab IT Board / e-Governance data initiatives, Sindh IT department portals,
Digital Pakistan Authority data pages, city portals (Lahore, Karachi, Islamabad
municipal open data). Accept CKAN/DKAN/uData-class catalogs with dataset
listings; reject single-page download lists and PDF libraries. Log kind
country-opendata.
```

**ChatGPT / Kimi web-research:**

```text
Find Pakistani open-data portals with public dataset listings. Already known:
opendata.com.pk, opendata.kp.gov.pk, d4dpak.com. Look for: Punjab open data
(Punjab IT Board / e-Punjab), Sindh open data, city-level portals (Lahore,
Karachi, Islamabad), Digital Pakistan Authority dataset pages, university civic
data projects. Return name | url | owner | number of datasets visible |
duplicate suspicion vs the three known hosts. Do not guess hosts; only report
URLs you actually saw.
```

### Phase 5 — Thin types (API, ML, metadata, datasets lists)

**Repo agent:**

```text
Missing Pakistan data catalogs — thin types only. Target slice PK-thin-types.
Current: API Catalog 0, ML 0, Metadata 0, Datasets list 0. Hunt: (a) government
API directories — SBP Raast developer portal, any public API catalog UI on
gov.pk hosts (gateways without a browsable catalog are rejects); (b) ML/AI
dataset catalogs — NCBC LUMS AI initiatives, national AI program dataset pages;
(c) DCAT/SDMX metadata registries with a public UI; (d) Datasets lists — GitHub
inventories of Pakistan datasets (the darlabpakistangithubio pattern), curated
data lists on research/NGO sites. Accept public listings only. Log kind
country-gap.
```

**ChatGPT / Kimi web-research:**

```text
Find Pakistani government API directories, AI/ML dataset catalogs, and curated
Pakistan dataset lists (GitHub or NGO-maintained inventories count). Return
name | url | owner | what is listed | public without login (yes/no). Do not list
opendata.com.pk, opendata.kp.gov.pk, d4dpak.com — already registered.
```

### Phase 6 — Custom confirmation (run last)

**Repo agent:**

```text
Review custom Pakistan catalogs and confirm or retag. Target slice
PK-custom-confirm. 17 custom rows. Known conclusions to respect: the 12 custom
indicators include the 8 *.data.gov.pk PBS dashboards, a single-tenant
Bootstrap+Highcharts+DataTables platform — one publisher, no shared product,
stays custom (22 September indicators review). Cluster the geo customs
(apphicsindhpk, darlabpakistangithubio, kpfmspakorg, pmulgcddgoppk,
lispulsegoppk, glisssbachanet, portalminesandmineralsgbgogpk) by fingerprint;
add a software YAML only when ≥3 independent installations share a named product
or a first-party vendor page names it. If nothing qualifies, report that and log
kind custom-review with 0 added — that is a complete hunt.
```

### Utility prompts (session playbook, Pakistan-flavored)

```text
Review records at data/entities/PK and fix them
```
(live links, software probes vs guesses, owner names; also fix `mc2020pbosgovpk`
filed under `Federal/` though its owner is Punjab Bureau of Statistics, and the
`is_national: None` on `opendatakpgovpk`)

```text
Review scheduled and promote if they are ok, otherwise remove them
```
(keep the queue at zero between releases — the exact prompt shape the Cursor
scheduled-review sessions used; the 36-record India/Nigeria/Pakistan promotion in
v1.18.0 ran this way)

```text
Update README and CHANGELOG
```
(after a batch, with exports rebuilt — only when you ask for a release)

## 6. Done-when

Each phase: every accepted URL has YAML + UID + `validate-yaml --id`, skipped
duplicates listed with existing ids, exhausted sources reported complete
(0 missing), and one `hunts.jsonl` row with the slice name from section 3 —
remember PK currently has zero logged rows, so even a 0-find phase must log.
Whole plan done when phases 1–5 have logged rows and the type table in section 2
has moved: indicators ≥ 25 with all four provincial bureaus covered, scientific
≥ 10 dataset-bearing, geo grown only via the leftover threads, thin types ≥ 2,
and the crt.sh `gis`/`opendata`/`maps`/`geoportal`/`repository` labels on `.pk`
enumerated at least once.
