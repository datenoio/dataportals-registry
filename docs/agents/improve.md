# Improve the registry (session playbook)

How to grow coverage and quality, based on **~3,000 Cursor sessions** (November 2025–August 2026) and the releases they produced. This is the *what to work on next* guide. Mechanics live in [discover.md](discover.md), [contribute.md](contribute.md), [scheduled.md](../scheduled.md), and [metadata-quality.md](../metadata-quality.md).

Working tree after those sessions: **24,993** verified catalogs, **7** scheduled, **282** software IDs, **219** country folders. Published snapshot: v1.18.0 (24,993 catalogs).

## What those sessions actually did

First-user-message mix across 3,027 indexed chats:

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

**Lesson:** one bounded vendor list or graph dump outperforms dozens of “missing {country}” chats. Country hunts still matter when the hole is *shape* (no scientific IRs, no native NSO table DB), not *count*.

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
3. Take the **vendor/government list**, not a web-wide crawl: OpenAIRE Graph, re3data, Dataverse installations, CKAN ecosystem, IMF DSBB, IHSN/NADA, DHIS2 country list, MappingSupport, national harvest source APIs (`data.gov.*` harvest endpoints).
4. Duplicate-check **exports** on hostname. Probe `/api/…` fingerprints from [discover.md](discover.md).
5. Stage, then promote only hosts that respond.

v1.16–v1.17 software definitions (Trimble Locus, Spatial Suite, G3W-SUITE, IMF NSDP, InterMine, GRIN-Global, LabKey, …) each unlocked a clean instance batch. Retag existing `software.id: custom` rows onto the new id in the same PR.

### 2. Graph and harvest-source dumps

OpenAIRE (`scripts/extract_openaire_portals.py`) added thousands of scientific IRs in one cycle — and also produced **664 rejects** (dead, parked, journals, software forges, staging). CKAN ecosystem is now ~10 unmatched sites; do not re-run it as a volume hunt.

Accept only public catalog UIs / harvest APIs. Journals, forges, single publications, and login walls are out of scope ([discover.md](discover.md#accept--reject)).

National **harvest source lists** (data.gouv.fr, data.gov.uk, dados.gov.pt, data.europa.eu, dataportal.se EntryStore) beat Google for municipal open data in countries that already have a national CKAN.

### 3. Country *shape* hunts (not more US ArcGIS)

The registry is dense in the US (~29% of rows) and Western Europe, and **geoportal-heavy** (~half of YAML). The remaining high-yield holes are:

- Populous countries with few catalogs relative to known ecosystems (India states/cities, Nigeria, Pakistan, Egypt, Bangladesh).
- Countries that already have CKAN/geo but **almost no scientific IRs** (Vietnam, Indonesia, Thailand, Türkiye, Egypt, Pakistan).
- Native NSO table databases (PxWeb, .Stat, STATcube, custom) vs IMF NSDP proxies already present.
- DHIS2 / NADA / REDATAM remaining countries (short vendor lists).
- Types that barely exist: microdata (~240), metadata (~96), API catalogs, ML catalogs.

Deprioritize: another US county ArcGIS Server, another French/Spanish commune geoportal, Open Data Inception rows that are PDFs or election pages, tiny territories that already have an IMF NSDP stub.

**Exception:** a *bounded, high-precision* list in a saturated geography is still worth it (MappingSupport live REST roots, Cadcorp council WebMaps). Unscoped “missing US catalogs” is not.

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
| Leave YAML ahead of exports | README/docs quote stale counts; CI quality baseline drifts. Rebuild before release. |
| Commit `.tmp_aq/` probes | Scratch only. |
| New `software.id` for a single site | Keep `custom` until several independent installations exist. |
| Implement query APIs / MCP in this repo | Out of scope. Reference data only. |

## Priority queue

Re-check counts in DuckDB before starting; India/Nigeria/DHIS2/DSpace passes already landed after the 26 August 2026 gap analysis.

| Rank | Hunt | Why | How |
|-----:|------|-----|-----|
| 1 | Scientific IRs in Asia and Africa | Shape hole: OD/geo exist, DSpace/Dataverse/EPrints do not | re3data + OpenAIRE Graph, filter to `dspace` / `eprints` / `dataverse` / `inveniordm`, skip countries already thick (US, DE, GB, ZA Figshare) |
| 2 | India remaining depth | Population × empty states/cities after the first 48 | State SDI, city CKAN, university IRs, MOSPI/state statistics. Duplicate-check `*.data.gov.in` |
| 3 | Egypt / Algeria / Bangladesh / Iran compact sprints | Almost no open-data and/or scientific rows | National portal + NSO table DB + 2–3 university IRs |
| 4 | Native NSO table catalogs | Indicators *pages* (IMF NSDP) are done; table DBs are not | PxWeb / PxStat / .Stat / STATcube / custom warehouses; Africa, Central Asia, Pacific |
| 5 | DHIS2 + NADA leftovers | Short lists, high precision | dhis2.org implementations + IHSN ADP; probe `/api/system/info` and `/index.php/catalog` |
| 6 | Africa national + capital open data | 19 UN members still had **zero** open-data YAML at last gap pass | National CKAN/DKAN/uData, then capital city. Skip more DHIS2 if already added |
| 7 | China geo / ODWeb / SuperMap | OD and science are decent; geo is thin vs ArcGIS-shaped countries | ODWeb path `/odweb/`, SuperMap iServer, provincial SDI |
| 8 | Microdata in OECD countries | Spain, Italy, Poland, Australia often show 0 NADA | IHSN list; do not refile indicator table builders as microdata |
| 9 | Metadata (FAIR Data Point) and API directories | Tiny types, clean accept/reject | FDP index; government API catalogs (API Setu-style) |
| — | More US ArcGIS Hub/Server | Already ~4,400 of ~6,900 US rows | Only if a named authoritative list remains unmatched |

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
3. Sources: national harvest API, re3data country facet, NSO site, university IR lists, local-language open-data terms (`datos abiertos`, `data terbuka`, `mở dữ liệu`).
4. Place local owners in `{CC}/{ISO-3166-2}/{type}/` with `owner.location.level` 30.

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
- `Missing {country} data catalogs` — then follow the type-shape table, do not add more geo if geo is already 70%
- `Review records at data/entities/{CC} and fix them` — quality
- `Review scheduled and promote if they are ok, otherwise remove them`
- `Find popular {type} software not yet in software records` — taxonomy
- `Update README and CHANGELOG` — after a batch, with rebuilt exports

Avoid: `Find all missing catalogs in the world`, `Search the internet for ArcGIS`, `Mark every Federal catalog as national`.

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
