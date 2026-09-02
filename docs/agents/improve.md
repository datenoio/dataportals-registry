# Improve the registry (session playbook)

How to grow coverage and quality, based on **~3,200 Cursor sessions** (November 2025–30 August 2026) and the releases they produced. This is the *what to work on next* guide. Mechanics live in [discover.md](discover.md), [contribute.md](contribute.md), [scheduled.md](../scheduled.md), and [metadata-quality.md](../metadata-quality.md). Hunt-pattern table: [discovery.md](../discovery.md#hunt-patterns).

Working tree after those sessions: **29,816** verified catalogs, **0** scheduled, **366** software IDs, **222** country folders. Published snapshot: v1.19.0 (29,816 catalogs, 0 scheduled, 366 software). YAML matches exports.

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

Volume came from a **small number of session types**, not from the 1,500 one-off URL adds:

| Release / cycle | Net catalogs | Software IDs | What drove it |
|-----------------|-------------:|-------------:|---------------|
| v1.16.0 | +1,002 | +24 | Platform instance lists (DSpace, Figshare, Nordic viewers, TabNet, FENIX, …) |
| v1.17.0 | +2,608 | +15 | OpenAIRE Graph harvest (2,409 promoted; 664 dropped) + IMF NSDP + domain science |
| v1.18.0 | +2,243 | +20 | Viewer products (e-mapa, Kortasjá, Swing, Hajk), DSpace IRs, MappingSupport ArcGIS, India/Nigeria depth |
| v1.19.0 | +4,823 | +84 | Municipal GIS viewers (Experience Builder, Mapotip, GisMaster, GISPLAN, IntraMaps, SonicWeb, …), harvest-source dumps, university IRs, named directories |

**Lesson:** one bounded vendor list, harvest-source dump, or named directory outperforms dozens of “missing {country}” chats. After v1.18.0 the high-yield *prompts* shifted: `Which {country} indicators…`, `There are a lot of {country} universities…`, `Which data sources harvested by {national portal}…`, `Which catalogs from {list URL}…`. Country hunts still matter when the hole is *shape* (no scientific IRs with datasets, no native NSO table DB), not *count*.

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

Do not commit `.tmp_aq/` probe scripts or JSON. Rebuild `data/datasets/` only when the user asked for a release or the YAML/export counts have diverged.

## What moved the needle (do more of this)

### 1. Software-first discovery

Highest catalogs-per-hour. Pattern that worked:

1. Confirm the product is shared → add `data/software/{category}/{id}.yaml` ([software-taxonomy.md](../software-taxonomy.md)).
2. Add fingerprints + harvest recipe in the same change ([software-index.md](../software-index.md) is CI-guarded).
3. Take the **vendor/government list**, not a web-wide crawl: OpenAIRE Graph, re3data, OpenDOAR, Dataverse installations, CKAN ecosystem, IMF DSBB, IHSN/NADA, DHIS2 country list, MappingSupport, national harvest source APIs (`data.gov.*` harvest endpoints), named directories (ODIS, CoreTrustSeal, WIS2 GDC, STAC Index, GeoNode gallery).
4. Duplicate-check **exports** on hostname. Probe `/api/…` fingerprints from [discover.md](discover.md).
5. Stage, then promote only hosts that respond.

v1.16–v1.17 software definitions (Trimble Locus, Spatial Suite, G3W-SUITE, IMF NSDP, InterMine, GRIN-Global, LabKey, …) each unlocked a clean instance batch. Retag existing `software.id: custom` rows onto the new id in the same PR.

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

Deprioritize: another US county ArcGIS Server, another French/Spanish commune geoportal, Open Data Inception rows that are PDFs or election pages, tiny territories that already have an IMF NSDP stub, university IR hunts for Monaco/Liechtenstein/Kiribati-class stubs, guessed HCI/Virtual LMI county hostnames.

**Exception:** a *bounded, high-precision* list in a saturated geography is still worth it (MappingSupport live REST roots, Cadcorp council WebMaps, SeaSketch public `/app` tenants, GDi Visios county viewers). Unscoped “missing US catalogs” is not.

### 4. Country record reviews

`Review records at data/entities/{CC} and fix them` was run across **~216** folders. That is how owners, HTTPS, dead hosts, harvest URLs, topics, and `is_national` got cleaned. It is still the right quality pass when a country was filled quickly from OpenAIRE or a vendor list.

Probe the live site before editing. Do not invent `/csw` or `/api/3` paths. Inactive catalogs must not keep `api: true` or live harvest endpoints.

### 5. `is_national` as official product, not federal owner

A dedicated classifier (`scripts/national_catalog.py`, `scripts/fix_is_national_flags.py`) unset the flag on **988** agency/thematic/scientific/subnational records. Rule: `true` only for that country’s official catalog **of that type** (national open-data portal, NSDI/geoportal, or NSO product). File path `Federal/` and `.gov` are not enough. Full rule: [data-model.md](../data-model.md#propertiesis_national).

### 6. Scheduled as a staging area, then empty it

Successful cycles grew `data/scheduled/`, live-checked URLs, promoted hundreds, and dropped the rest (duplicates, HTTP 502, empty dashboards, hijacked domains). Prefer `--scheduled` on discovery; promote only after a GET. Script: [scheduled.md](../scheduled.md). Keep the queue near **zero** between releases so `catalogs.jsonl` and YAML counts stay explainable.

## What wasted time (do less of this)

| Anti-pattern | What happened |
|--------------|----------------|
| Walk `data/entities/**/*.yaml` to search | Slow, misses scheduled, duplicates slip through. Use DuckDB / Parquet. |
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
| Leave YAML ahead of exports | README/docs quote stale counts; CI quality baseline drifts. Rebuild before release. |
| Commit `.tmp_aq/` probes | Scratch only. |
| New `software.id` for a single site | Keep `custom` until several independent installations exist. |
| Implement query APIs / MCP in this repo | Out of scope. Reference data only. |

## Priority queue

Re-check counts in DuckDB (and YAML if exports lag) before starting. India/Nigeria/DHIS2/DSpace, the 29–30 August country-indicators wave, and the university-IR country wave already landed after the 26 August 2026 gap analysis.

| Rank | Hunt | Why | How |
|-----:|------|-----|-----|
| 1 | National harvest-source leftovers | data.go.id added 112 origin catalogs in one pass; other national portals still have unmatched harvest URLs | Harvest/organisations API → probe origin UI ([discovery-opendata.md](../discovery-opendata.md#national-harvest-sources)) |
| 2 | Dataset-bearing scientific IRs | Shape hole after the university-IR wave: OpenDOAR hosts that list **datasets**, not publications | OpenDOAR + re3data + OpenAIRE, filter DSpace Dataset type / Dataverse; skip microstates |
| 3 | Native NSO / health / education indicators leftovers | OECD+Asia indicators mostly filled; Africa and some subnational explorers remain | PxWeb / .Stat / STATcube / DHIS2 / TabNet; skip IMF NSDP already present |
| 4 | Named directories | Bounded lists still convert: ODIS 28, CoreTrustSeal 5, STAC leftovers, WIS2 GDC, GeoNode gallery | One list URL per session ([discovery.md](../discovery.md#existing-lists-start-here)) |
| 5 | India remaining depth | Population × empty states/cities after the first 48 | State SDI, city CKAN, university IRs with datasets, MOSPI/state statistics. Duplicate-check `*.data.gov.in` |
| 6 | DHIS2 + NADA leftovers | Short lists, high precision | dhis2.org implementations + IHSN ADP; probe `/api/system/info` and `/index.php/catalog` |
| 7 | Africa national + capital open data | UN members that still have **zero** open-data YAML | National CKAN/DKAN/uData, then capital city. Skip more DHIS2 if already added |
| 8 | Microdata in OECD countries | Spain, Italy, Poland, Australia often show 0 NADA | IHSN list; do not refile indicator table builders as microdata |
| 9 | Custom-software retag | Pozi, Instant Apps, JMap, GIS Cloud, MRF Web Map, MuniSight, p.mapper, CommunityView, MS-GIS, Weave, OVIE, SOFTPRO, MxSIG, and Cologne TR32DB extracted from custom catalogs; remaining custom geoportals are mostly one-off `.gov` roots | Hostname/path clusters with ≥3 installs; one-off `.gov` roots stay `custom` |
| — | More US ArcGIS Hub/Server | Already thousands of US geo rows | Only if a named authoritative list remains unmatched (MappingSupport, FGDC SSC) |

## Recipes

### Software-instance hunt

```text
Which {software.name} catalogs are missing?
```

Agent steps:

1. Read the software YAML and [software-index.md](../software-index.md) row.
2. `SELECT link, owner.location.country.id FROM catalogs WHERE software.id = '{id}'` on `datasets.duckdb`.
3. Fetch the vendor list / gallery (not a scanner).
4. Match on hostname; probe fingerprints; `add-single --scheduled`.
5. If ≥3 `custom` rows are clearly this product, retag them and add the software definition first.

### Country-shape hunt

```text
Missing {country} data catalogs
```

Agent steps:

1. Count YAML by type for that ISO folder (opendata / geo / scientific / indicators / microdata).
2. Hunt the **missing type**, not the type already in the hundreds.
3. Sources: national harvest API, re3data country facet, OpenDOAR, NSO site, university IR lists, local-language open-data terms (`datos abiertos`, `data terbuka`, `mở dữ liệu`).
4. Place local owners in `{CC}/{ISO-3166-2}/{type}/` with `owner.location.level` 30.

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

Do not hunt instances of a product that has no `software.id`. Add the definition + discovery/harvest headings + `docs_software_coverage` in **one** change, then the instance hunt. CI fails if a published ID is missing from the guides (`tests/test_docs_software_coverage.py`).

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

If YAML and `catalogs.jsonl` disagree, say so and prefer YAML counts (`data/entities/**/*.yaml`) for “what is already added,” exports for hostname duplicate checks until the next `build`.

## Session prompts that work

Copy these; they match the loops above.

- `Which {software} catalogs are missing?` — instance hunt
- `Which data sources harvested by {national portal} are missing?` — harvest-source hunt
- `There are a lot of {country} universities… Which scientific repositories are missing?` — IR hunt (dataset-bearing only)
- `Which {country} indicators catalogs are missing?` — then skip IMF NSDP / national StatBank already registered
- `Which catalogs from {list URL} are missing?` — named directory
- `Missing {country} data catalogs` — then follow the type-shape table, do not add more geo if geo is already 70%
- `Which {country} cities and counties have data catalogs that are missing?` — subnational; use the national harvest list first
- `Review custom {type} catalogs and identify new software definitions`
- `Review records at data/entities/{CC} and fix them` — quality
- `Review scheduled and promote if they are ok, otherwise remove them`
- `Find popular {type} software not yet in software records` — taxonomy
- `Update README and CHANGELOG` — after a batch, with rebuilt exports

Avoid: `Find all missing catalogs in the world`, `Search the internet for ArcGIS`, `Mark every Federal catalog as national`, university IR hunts for microstates, guessed county HCI hostnames.

## Done when

A discovery session is done when every accepted URL has YAML, UID, and `validate-yaml --id`, and skipped duplicates are listed with their existing `id`.

A country review is done when `validate-yaml` passes for that folder and live probes match `status` / `api` / endpoints.

A release session is done when YAML count = export count, scheduled is 0 (or explained), quality baseline is refreshed, and README / CHANGELOG / `llms.txt` quote the same numbers.

## Related

- [discover.md](discover.md) — probe order, accept/reject, no scanners
- [contribute.md](contribute.md) — YAML checklist
- [harvest.md](../harvest.md) — dataset crawl is **out of this repo**; do not write dataset YAML here
- [discovery.md](../discovery.md) — vendor lists
- [scheduled.md](../scheduled.md) / [software-taxonomy.md](../software-taxonomy.md) / [quality-rules.md](../quality-rules.md)
- [data-model.md](../data-model.md#propertiesis_national)
