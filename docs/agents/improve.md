# Improve the registry (session playbook)

How to grow coverage and quality, based on **~3,900 Cursor sessions** (November 2025–8 September 2026) and the releases they produced. This is the *what to work on next* guide. Mechanics live in [discover.md](discover.md), [contribute.md](contribute.md), [scheduled.md](../scheduled.md), and [metadata-quality.md](../metadata-quality.md). Hunt-pattern table: [discovery.md](../discovery.md#hunt-patterns).

Working tree (10 September 2026): **36,873** verified catalogs, **0** scheduled YAML, **470** software IDs, **224** country folders. Published snapshot: v1.20.0 (35,266 catalogs, 0 scheduled, 423 software). Rebuild exports when YAML and `data/datasets/` diverge.

## What those sessions actually did

First-user-message mix across 3,027 indexed chats (through v1.18.0):

| Session type | Share | Typical prompt |
|--------------|------:|----------------|
| Add a single URL | 50% | `Add https://…` / `Adding URL to entities` |
| Country or topic gap hunt | 18% | `Missing India data catalogs` |
| Software taxonomy | 11% | `Popular geoportal software` / add a `software.id` |
| Country record review | 7% | `Review records at data/entities/XX and fix them` |
| Metadata / endpoint repair | 3% | `Update {id} metadata` |
| Software-instance hunt | 1% | `Which DSpace catalogs are missing?` |
| Docs, changelog, release | 1% | `Update README and CHANGELOG` |

**31 August–8 September 2026** (~547 chats, covering v1.19.0 and v1.20.0) inverted that mix: **~82%** were software-instance or subnational municipal-GIS hunts (`Which {software} catalogs are missing?`, `Which {country} cities and counties geoportals are missing?`). Custom-software reviews on 1–2 and 7 September extracted dozens of new `software.id` values, then instance hunts filled them. A 0-missing result is a valid done state — it documents completeness.

Volume came from a **small number of session types**, not from the 1,500 one-off URL adds:

| Release / cycle | Net catalogs | Software IDs | What drove it |
|-----------------|-------------:|-------------:|---------------|
| v1.16.0 | +1,002 | +24 | Platform instance lists (DSpace, Figshare, Nordic viewers, TabNet, FENIX, …) |
| v1.17.0 | +2,608 | +15 | OpenAIRE Graph harvest (2,409 promoted; 664 dropped) + IMF NSDP + domain science |
| v1.18.0 | +2,243 | +20 | Viewer products (e-mapa, Kortasjá, Swing, Hajk), DSpace IRs, MappingSupport ArcGIS, India/Nigeria depth |
| v1.19.0 | +4,823 | +84 | Municipal GIS viewers (Experience Builder, Mapotip, GisMaster, GISPLAN, IntraMaps, SonicWeb, …), harvest-source dumps, university IRs, named directories |
| v1.20.0 | +5,450 | +57 | Polish e-mapa.net, Czech/Slovak municipal GIS (GISPLAN, GisOnline, Mapotip, GEPRO, mOBEC), Italian GisMaster, Swiss GeoMapFish, Brazilian CTMGEO, Japanese WagMap, new software IDs (WebEWID, DaCHS, Argenmap, …) |

**Lesson:** one bounded **vendor tenant list** or hostname pattern (e-mapa.net, `{city}.gisplan.sk`, GisMaster `IdCliente=`) outperforms Google for every city in the country. After v1.18.0 the high-yield *prompts* were harvest sources, university IRs, country indicators, and named directories. After v1.19.0 they shifted again: define the municipal GIS product, then hunt its tenants. Country hunts still matter when the hole is *shape* (no dataset-bearing scientific IRs, no native NSO table DB, UN members with zero open-data YAML), not *count*. Do not repeat “which France/Spain/Texas cities geoportals” now that those markets are dense.

## Operating loop

Run these in order. Skipping a step is how duplicates, dead hosts, and `custom` sprawl get in.

```
1. Scope     DuckDB gap query or a vendor list (not a YAML walk)
2. Discover  software-first, then country-shape. Probe candidate hosts only
3. Stage     add-single --scheduled  (temp UIDs)
4. Probe     live GET; 401/403 stop; dead → drop or inactive
5. Promote   promote_scheduled.py or manual move; assign; validate-yaml
6. Enrich    country review: owner, endpoints, is_national, type path
7. Release   analyze-quality, build, README/CHANGELOG, software-index
```

If `datasets.duckdb` is locked (another session writing), query `data/datasets/full.parquet` instead — it is read-only and enough for hostname duplicate checks. Do not walk YAML because DuckDB failed.

Reuse a prior hunt transcript for the same `software.id` or country before starting a second pass. If that hunt already exhausted the vendor list, report completeness and stop unless a new list URL exists.

Do not commit `.tmp_aq/` probe scripts or JSON. Rebuild `data/datasets/` only when the user asked for a release or the YAML/export counts have diverged.

## What moved the needle (do more of this)

### 1. Software-first discovery

Highest catalogs-per-hour. Pattern that worked:

1. Confirm the product is shared → add `data/software/{category}/{id}.yaml` ([software-taxonomy.md](../software-taxonomy.md)).
2. Add fingerprints + harvest recipe in the same change ([software-index.md](../software-index.md) is CI-guarded).
3. Take the **vendor/government list**, not a web-wide crawl: OpenAIRE Graph, re3data, OpenDOAR, Dataverse installations, CKAN ecosystem, IMF DSBB, IHSN/NADA, DHIS2 country list, MappingSupport, national harvest source APIs (`data.gov.*` harvest endpoints), named directories (ODIS, CoreTrustSeal, WIS2 GDC, STAC Index, GeoNode gallery).
4. Duplicate-check **exports** on hostname. Probe `/api/…` fingerprints from [discover.md](discover.md).
5. Stage, then promote only hosts that respond.

v1.16–v1.17 software definitions (Trimble Locus, Spatial Suite, G3W-SUITE, IMF NSDP, InterMine, GRIN-Global, LabKey, …) each unlocked a clean instance batch. v1.19–v1.20 municipal GIS IDs (e-mapa, GISPLAN, GisMaster, IntraMaps, SonicWeb, WebEWID, …) did the same at country scale: **product first, then the vendor tenant list**, not “Google every city”. Retag existing `software.id: custom` rows onto the new id in the same PR.

After v1.20.0, prefer instance hunts for IDs that still have **pending vendor lists** (changelog “instance hunts pending”) over re-running products already hunted on 3–5 September 2026. A Censys or FOFA title/body pass is worth it when Google and the gallery are exhausted and the product has a distinctive HTML fingerprint — not as a replacement for the vendor list. Use FOFA when Censys search is unavailable, or for East Asian hosts.

Branded products with a first-party product page or vendor deployment list may get a `software.id` even with one or two registry rows, **then** the instance hunt. Unnamed one-off `.gov` map roots stay `custom`. Rule: [software-taxonomy.md](../software-taxonomy.md#adding-a-software-definition).

### 2. Graph and harvest-source dumps

OpenAIRE (`scripts/extract_openaire_portals.py`) added thousands of scientific IRs in one cycle — and also produced **664 rejects** (dead, parked, journals, software forges, staging). CKAN ecosystem is now ~10 unmatched sites; do not re-run it as a volume hunt.

Accept only public catalog UIs / harvest APIs. Journals, forges, single publications, and login walls are out of scope ([discover.md](discover.md#accept--reject)).

National **harvest source lists** (data.gouv.fr, data.gov.uk, dados.gov.pt, data.europa.eu, dataportal.se EntryStore, **data.go.id**, govdata.de, datos.gob.es, data.go.kr, data.gov.ru, opendata.swiss, dane.gov.pl, search.open.canada.ca) beat Google for municipal open data in countries that already have a national CKAN. data.go.id yielded **112** origin catalogs in one pass; dane.gov.pl’s 7,477 institutions were almost all XML dataset feeds — only the six CKAN harvests were catalogs. Probe the origin UI, not the harvest-source row.

### 3. Country *shape* hunts (not more US ArcGIS)

The registry is dense in the US (~29% of rows) and Western Europe, and **geoportal-heavy** (~half of YAML). The remaining high-yield holes are:

- Populous countries with few catalogs relative to known ecosystems (India remaining states/cities after the first depth pass).
- Countries that already have CKAN/geo but **almost no dataset-bearing scientific IRs** (filter OpenDOAR/DSpace to Dataset type; publication-only IRs are out of scope).
- Native NSO table databases still missing after the 29–30 August indicators wave (Africa, some Pacific) vs IMF NSDP proxies already present.
- DHIS2 / NADA / REDATAM remaining countries (short vendor lists).
- Types that barely exist: microdata, metadata, API catalogs, ML catalogs.
- Named directories not yet exhausted: national harvest leftovers, ODIS/WIS2/CLARIN follow-ups.

Deprioritize: another US county ArcGIS Server, another French/Spanish/Czech/Slovak/Polish/Italian commune geoportal, Open Data Inception rows that are PDFs or election pages, tiny territories that already have an IMF NSDP stub, university IR hunts for Monaco/Liechtenstein/Kiribati-class stubs, guessed HCI/Virtual LMI county hostnames, repeating a software-instance hunt from the last two weeks unless a new gallery appeared.

**Exception:** a *bounded, high-precision* list in a saturated geography is still worth it (MappingSupport live REST roots, Cadcorp council WebMaps, SeaSketch public `/app` tenants, GDi Visios county viewers, Instant Apps Filter Gallery hosts). Unscoped “missing US catalogs” or “all 400 Iranian counties” is not — public catalogs are the few cities that publish a REST/GeoServer/GeoNode UI, not every administrative unit.

### 4. Country record reviews

`Review records at data/entities/{CC} and fix them` was run across **~216** folders. That is how owners, HTTPS, dead hosts, harvest URLs, topics, and `is_national` got cleaned. It is still the right quality pass when a country was filled quickly from OpenAIRE or a vendor list.

Probe the live site before editing. Do not invent `/csw` or `/api/3` paths. Inactive catalogs must not keep `api: true` or live harvest endpoints.

### 5. `is_national` as official product, not federal owner

A dedicated classifier (`scripts/national_catalog.py`, `scripts/fix_is_national_flags.py`) unset the flag on **988** agency/thematic/scientific/subnational records. Rule: `true` only for that country’s official catalog **of that type** (national open-data portal, NSDI/geoportal, or NSO product). File path `Federal/` and `.gov` are not enough. Full rule: [data-model.md](../data-model.md#propertiesis_national).

### 6. Scheduled as a staging area, then empty it

Successful cycles grew `data/scheduled/`, live-checked URLs, promoted hundreds, and dropped the rest (duplicates, HTTP 502, empty dashboards, hijacked domains). Prefer `--scheduled` on discovery; promote only after a GET. Script: [scheduled.md](../scheduled.md). Keep the queue near **zero** between releases so `catalogs.jsonl.zst` and YAML counts stay explainable.

## What wasted time (do less of this)

| Anti-pattern | What happened |
|--------------|----------------|
| Walk `data/entities/**/*.yaml` to search | Slow, misses scheduled, duplicates slip through. Use DuckDB / Parquet. |
| Treat DuckDB lock as a blocker | Parallel hunts lock `datasets.duckdb`. Query `full.parquet`. |
| Guess harvest endpoints from software docs | Quality rules then fire `SOFTWARE_EXPECTED_ENDPOINTS_MISSING`; inactive sites get fake APIs. Probe, then write. |
| Treat every federal/agency catalog as national | 988 false `is_national: true` flags. |
| Add OpenAIRE / re3data rows without accept/reject | Journals, forges, parked domains, staging hosts. |
| Login-walled CRIS (hosted Symplectic, SSO Pure) | Stop on 401/403; do not add. |
| “Missing catalogs” for Nauru / San Marino-class stubs | Already have indicator pages; yield is one PDF. |
| University IR hunt for Monaco / Liechtenstein / Kiribati | No dataset-bearing IR; waste a session. |
| Add every OpenDOAR / DSpace host | Publication-only IRs (Kazakhstan: 10 later removed). Require Dataset type or a research-data community. |
| Treat national harvest *rows* as catalogs | dane.gov.pl: 7,477 institutions, almost all XML feeds; opendata.swiss geocat/I14Y slices. Probe the origin UI. |
| Guess HCI / Virtual LMI / Cancer-Rates county hosts | Timeouts and login loops. Use the vendor tenant list, not DNS guesses. |
| Register every PISO / SeaSketch / GISApp copy | One catalog per public product; skip marketplace demos and REST adaptors. |
| Google every city after a tenant list exists | Iran/Texas-class sweeps. Use `{country}` + the **product** hostname pattern. |
| Repeat a software hunt from this week | Sept 3–5 already covered most IDs. 0 missing is done. |
| Directory hubs and survey platforms | IPUMS Health Surveys (lists collections), SurveySolutions (data collection, not a catalog), Oskari RPC embeds of Suomi.fi. |
| Mix ArcGIS product IDs on one org | Hub vs Experience Builder vs Web AppBuilder vs Instant Apps vs Dashboards vs StoryMaps vs Server — one public catalog UI unless they are distinct products. |
| Leave YAML ahead of exports | README/docs quote stale counts; CI quality baseline drifts. Rebuild before release. |
| Commit `.tmp_aq/` probes | Scratch only. |
| New `software.id` for an unnamed `.gov` root | Keep `custom` until a named product (vendor page or ≥3 independent installs) exists. |
| Implement query APIs / MCP in this repo | Out of scope. Reference data only. |

## Priority queue

Re-check counts in DuckDB (and YAML if exports lag) before starting. India/Nigeria/DHIS2/DSpace, the 29–30 August country-indicators wave, the university-IR country wave, and the 31 August–5 September municipal-GIS / software-instance wave already landed. After v1.20.0, PL/CZ/SK/IT/CH/JP/BR municipal GIS is dense — do not start another commune sweep there.

| Rank | Hunt | Why | How |
|-----:|------|-----|-----|
| 1 | Pending instance lists for new v1.20 IDs | Custom reviews added IDs (CartoVista, IGO2, InfoMap, dpWebmap, Flood Intelligence Portal, GeoViewer, …) with hunts still pending | Vendor page / crt.sh hostname pattern → probe ([discover.md](discover.md#software-instance)) |
| 2 | Dataset-bearing scientific IRs | Shape hole after the university-IR wave: OpenDOAR hosts that list **datasets**, not publications | OpenDOAR + re3data + OpenAIRE, filter DSpace Dataset type / Dataverse; skip microstates |
| 3 | Native NSO / health / education indicators leftovers | OECD+Asia indicators mostly filled; Africa and some subnational explorers remain | PxWeb / .Stat / STATcube / DHIS2 / TabNet; skip IMF NSDP already present |
| 4 | Named directories | Bounded lists still convert: ODIS, CoreTrustSeal leftovers, STAC, WIS2 GDC, GeoNode gallery, Instant Apps Filter Gallery | One list URL per session ([discovery.md](../discovery.md#existing-lists-start-here)) |
| 5 | National harvest-source leftovers | data.go.id added 112 origin catalogs in one pass; other national portals still have unmatched harvest URLs | Harvest/organisations API → probe origin UI ([discovery-opendata.md](../discovery-opendata.md#national-harvest-sources)) |
| 6 | Africa national + capital open data | UN members that still have **zero** open-data YAML | National CKAN/DKAN/uData, then capital city. Skip more DHIS2 if already added |
| 7 | India remaining depth | Population × empty states/cities after the first 48 | State SDI, city CKAN, university IRs with datasets, MOSPI/state statistics. Duplicate-check `*.data.gov.in` |
| 8 | DHIS2 + NADA leftovers | Short lists, high precision | dhis2.org implementations + IHSN ADP; probe `/api/system/info` and `/index.php/catalog` |
| 9 | Microdata in OECD countries | Spain, Italy, Poland, Australia often show 0 NADA | IHSN list; do not refile indicator table builders as microdata |
| 10 | Custom-software retag | Sept 7 four-pass review already extracted Argenmap, WebEWID, Dashboards, GT Map, SHK KBS, …; remaining custom geoportals are mostly one-off `.gov` roots | Hostname/path clusters with a named product; one-off `.gov` roots stay `custom` |
| — | More US/EU commune ArcGIS or e-mapa-class GIS | Already thousands of geo rows; PL e-mapa, CZ GISPLAN, IT GisMaster, JP WagMap filled | Only if a named authoritative list remains unmatched (MappingSupport, FGDC SSC, a new vendor gallery) |

## Recipes

### Software-instance hunt

```text
Which {software.name} catalogs are missing?
```

Agent steps:

1. Read the software YAML and [software-index.md](../software-index.md) row.
2. `SELECT link, owner.location.country.id FROM catalogs WHERE software.id = '{id}'` on `datasets.duckdb` (or `full.parquet` if DuckDB is locked).
3. Fetch the vendor list / gallery / crt.sh hostname pattern (not a scanner). Skip if a hunt in the last two weeks already exhausted that list.
4. Match on hostname; probe fingerprints; `add-single --scheduled`.
5. If the vendor list is exhausted and probes found nothing new, **stop and report completeness** (0 missing is done).
6. If ≥3 `custom` rows are clearly this product, or a first-party product page names it, retag them and add the software definition first.
7. Optional second pass: Censys `html_title` / body fingerprint when Google and the gallery are silent, or the FOFA equivalent (`title=` / `body=` / `country=`) when Censys is not configured.

### Country-shape hunt

```text
Missing {country} data catalogs
```

Agent steps:

1. Count YAML by type for that ISO folder (opendata / geo / scientific / indicators / microdata).
2. Hunt the **missing type**, not the type already in the hundreds.
3. Sources: national harvest API, re3data country facet, OpenDOAR, NSO site, university IR lists, local-language open-data terms (`datos abiertos`, `data terbuka`, `mở dữ liệu`).
4. Place local owners in `{CC}/{ISO-3166-2}/{type}/` with `owner.location.level` 30.
5. For geoportals, use the **municipal GIS product list** for that country (e-mapa, GISPLAN, GisMaster, IntraMaps, SonicWeb, …). Do not Google every city name.

### Subnational municipal GIS hunt

```text
Which {country} cities and counties have geoportals that are missing?
```

Agent steps:

1. Count existing `geo/` YAML for that ISO folder. If geo is already the majority type, stop unless a named product list remains unmatched.
2. Identify the dominant viewer product(s) from [software-index.md](../software-index.md) / prior country hunts.
3. Hunt that product's tenant list or hostname pattern — not every administrative unit.
4. Accept live public viewers. Reject REST adaptors of an existing Hub, marketplace demos, login staff GIS, and “all 400 counties” guesses (Iran: only cities with a public ArcGIS/GeoServer/GeoNode UI).

### National harvest-source hunt

```text
Which data sources harvested by {national portal} are missing?
```

Agent steps: [discover.md](discover.md#national-harvest-sources). Full accept/reject: [discovery-opendata.md](../discovery-opendata.md#national-harvest-sources).

### Country university IR hunt

```text
There are a lot of {country} universities and research organizations that could have scientific data repositories that are not yet listed. Which of them are missing?
```

Agent steps: [discover.md](discover.md#country-university-irs). Require Dataset type: [discovery-scientific.md](../discovery-scientific.md#country-university-irs).

### Country indicators hunt

```text
Which {country} indicators catalogs are missing?
```

Agent steps: [discover.md](discover.md#country-indicators). Skip IMF NSDP already present: [discovery-indicators.md](../discovery-indicators.md#country-indicators-hunt).

### Named directory hunt

```text
Which data catalogs from {list URL} are missing?
```

One bounded URL. Duplicate-check hostname. Probe live. Skip preservation-only systems and org homepages. Lists: [discovery.md](../discovery.md#existing-lists-start-here).

### Country review

```text
Review records at data/entities/{CC} and fix them
```

Checklist that reviews actually used:

- Live `link` (HTTPS, no trailing slash unless required); `status: inactive` if dead/parked
- `software.id` matches a probe, not the old guess
- `catalog_type` matches the directory (`scientific/` vs `opendata/`)
- Owner name + `owner.link` from the site, not a generic ministry string
- Coverage country matches path; quote UN M49 macroregion ids (`'155'`) so they stay strings
- Harvest endpoints only after a 200 on that path; set `api` to match
- `properties.is_national` only for the official product of that type
- `assign` + `validate-yaml --id` on touched files

### Quality batch

Integrity-track issues (invalid enums, duplicates, path mismatches) block CI. Enrichment-track gaps (`MISSING_TAGS`, expected endpoints) can wait. Workflow: [metadata-quality.md](../metadata-quality.md), [quality-rules.md](../quality-rules.md). After OpenAIRE-scale adds, run `analyze-quality` before the next hunt or the baseline explodes.

### Software definition multiplier

Do not hunt instances of a product that has no `software.id`. Add the definition + discovery/harvest headings + `docs_software_coverage` in **one** change, then the instance hunt. CI fails unless both guides have a unique `{#id}` heading (`tests/test_docs_software_coverage.py`).

## DuckDB checks before a hunt

```sql
-- Type mix for a country (working-tree export; rebuild if YAML is ahead)
SELECT catalog_type, count(*) n
FROM catalogs
WHERE owner.location.country.id = 'IN'
GROUP BY 1 ORDER BY n DESC;

-- Custom share (retag candidates)
SELECT catalog_type,
       count(*) n,
       sum(CASE WHEN software.id = 'custom' THEN 1 ELSE 0 END) AS custom_n
FROM catalogs
GROUP BY 1;

-- National open-data flag coverage
SELECT owner.location.country.id AS cc, count(*)
FROM catalogs
WHERE catalog_type = 'Open data portal'
  AND properties.is_national = true
GROUP BY 1;
```

If YAML and `catalogs.jsonl.zst` disagree, say so and prefer YAML counts (`data/entities/**/*.yaml`) for “what is already added,” exports for hostname duplicate checks until the next `build`.

## Session prompts that work

Copy these; they match the loops above.

- `Which {software} catalogs are missing?` — instance hunt (0 missing is done)
- `Which data sources harvested by {national portal} are missing?` — harvest-source hunt
- `There are a lot of {country} universities… Which scientific repositories are missing?` — IR hunt (dataset-bearing only)
- `Which {country} indicators catalogs are missing?` — then skip IMF NSDP / national StatBank already registered
- `Which catalogs from {list URL} are missing?` — named directory
- `Missing {country} data catalogs` — then follow the type-shape table, do not add more geo if geo is already 70%
- `Which {country} cities and counties have geoportals that are missing?` — subnational; use the municipal GIS **product tenant list**, not every city name
- `Review custom {type} catalogs and identify new software definitions`
- `Review records at data/entities/{CC} and fix them` — quality
- `Review scheduled and promote if they are ok, otherwise remove them`
- `Find popular {type} software not yet in software records` — taxonomy
- `Update README and CHANGELOG` — after a batch, with rebuilt exports

Avoid: `Find all missing catalogs in the world`, `Search the internet for ArcGIS`, `Mark every Federal catalog as national`, university IR hunts for microstates, guessed county HCI hostnames, `Which {saturated country} cities geoportals are missing?` when that country's municipal GIS product is already tenant-complete, repeating `Which {software} catalogs are missing?` for an ID hunted in the last two weeks.

## Done when

A discovery session is done when every accepted URL has YAML, UID, and `validate-yaml --id`, skipped duplicates are listed with their existing `id`, **and** exhausted vendor lists are reported as complete (including 0 missing).

A country review is done when `validate-yaml` passes for that folder and live probes match `status` / `api` / endpoints.

A release session is done when YAML count = export count, scheduled is 0 (or explained), quality baseline is refreshed, and README / CHANGELOG / `llms.txt` quote the same numbers.

## Related

- [discover.md](discover.md) — probe order, accept/reject, no scanners
- [contribute.md](contribute.md) — YAML checklist
- [harvest.md](../harvest.md) — dataset crawl is **out of this repo**; do not write dataset YAML here
- [discovery.md](../discovery.md) — vendor lists
- [scheduled.md](../scheduled.md) / [software-taxonomy.md](../software-taxonomy.md) / [quality-rules.md](../quality-rules.md)
- [data-model.md](../data-model.md#propertiesis_national)
