# dataportals-registry v1.16.0

**Release date:** August 24, 2026

## Summary

This release adds 1,002 net new catalogs and 24 software platform definitions. Coverage expands across scientific repositories (DSpace, Figshare, Hyrax), geoportals (Spatial Suite, Louhi, Landfolio, G3W-SUITE, GEUSMAP), indicators (TabNet, SparkMap, Goal Tracker, FENIX, PxStat), and mineral/petroleum transparency portals. Dataset exports are rebuilt to match source YAML. Python 3.9 is no longer supported; CI tests 3.10–3.12.

## What's in this release

### Added
- **1,002 net new catalog entries**; registry source now **20,142** entities (**12** scheduled) across **218** country/territory folders, including a first entity root for **Isle of Man (IM)**.
- **24 software definitions**; software catalog now **247** platforms: Trimble Locus IMS, Sitowise Louhi, Trimble Landfolio, Spatial Suite, GEUSMAP, GISApp, iObčina, G3W-SUITE, Cadcorp SIS WebMap, Astun iShare, Hexagon M.App Enterprise, CubeWerx CubeSERV, Sentinel Hub, DataWarehousePro, Goal Tracker, RDF Online Repository, ResourceContracts, Guangxi Public Data Open Platform, PxStat, TabNet, FENIX, Beyond 20/20, SparkMap, and StatPlanet.
- **376 scientific repositories**, including **135 DSpace**, **118 Figshare**, **23 Hyrax**, **13 Elsevier Pure**, and related IRs.
- Geoportal products including **22 Spatial Suite**, **19 Louhi**, **18 Landfolio**, **15 GEUSMAP**, **12 Trimble Locus IMS**, and **12 G3W-SUITE**.
- Indicators including Open SDG, SparkMap, DHIS2, DATASUS TabNet, Goal Tracker, PxWeb, SuperSTAR/SuperWEB2, FENIX, and ASEAN dashboards.
- **16 polar / Arctic / Greenland catalogs** and **14** Africa/Asia/Latin America catalogs promoted from scheduled. **12** Cadcorp UK viewers remain in the scheduled queue.

### Changed
- Drop Python 3.9; supported and CI-tested versions are **3.10–3.12**.
- Recategorized **46** catalogs into the correct country, Federal/subregion, or type folder. Retagged existing catalogs onto the new software IDs (including 15 Guangxi public-data tenants).
- Refreshed metadata on **992** existing catalogs; HTTP-verified endpoints on **209** records.
- Regenerated dataset exports: **20,142** catalog records; 247 software definitions; 12 scheduled (**20,154** in `full.jsonl`).
- Quality regression baseline refreshed (integrity CRITICAL/IMPORTANT remain zero).

### Removed
- **8 catalog entries** removed as superseded or duplicate.
- Greenland Mineral Resources geoportal and WASCAL Hydromet Network dropped from scheduled without promotion.

## Data exports (2026-08-24)

| Export | Count |
|--------|--------|
| `catalogs.jsonl` (+ `.zst`) | 20,142 catalog records |
| `software.jsonl` (+ `.zst`) | 247 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 12 scheduled sources |
| `full.jsonl` (+ `.zst`) | 20,154 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
