# dataportals-registry v1.20.0

**Release date:** September 8, 2026

## Summary

This release adds 5,450 net new catalogs and 57 software platform definitions. Coverage expands with municipal GIS viewers (e-mapa.net, GISPLAN, GisOnline, Mapotip, GEPRO, mOBEC, GisMaster, GeoMapFish, CTMGEO, WagMap), new platform IDs (WebEWID, DaCHS, Argenmap, Dialnet CRIS, ArcGIS Dashboards, BEXIS2, Specify), and first entity roots for Curaçao and Wallis and Futuna. The scheduled queue is empty. Dataset exports are rebuilt to match source YAML. Quality analysis reports 0 issues.

## What's in this release

### Added
- **5,450 net new catalog entries**; registry source now **35,266** entities (**0** scheduled) across **224** country/territory folders (added Curaçao `CW` and Wallis and Futuna `WF`).
- **57 software definitions**; software catalog now **423** platforms. Highest-count new IDs: WebEWID (`webewid`, **66**), DaCHS (`dachs`, **33**), Argenmap (`argenmap`, **16**), Dialnet CRIS (`dialnetcris`, **13**), ArcGIS Dashboards (`arcgisdashboards`, **11**), BEXIS2 (`bexis2`, **11**), Esri UK Data Observatory (`esridataobservatory`, **10**), and Specify Web Portal (`specify`, **10**).
- **1,802** Polish Geo-System e-mapa.net municipal geoportals; **288** GISPLAN, **244** GisOnline, **121** Mapotip, and **116** Geoportál GEPRO catalogs.
- **162** Slovak mOBEC and **115** Geodeticca WEB GIS; **133** Italian GisMaster comune catalogs; **122** GeoMapFish geoportals; **94** Brazilian CTMGEO SigWEB; **84** Japanese WagMap.
- **70** GBIF platform catalogs, **66** Elsevier Digital Commons repositories, **64** THREDDS servers, **61** SeaSketch project maps, **53** Croatian DABAR IRs, and **36** Knoema indicator catalogs.
- Russian open-data and geoportal coverage (**149** catalogs), including Bitrix, WordPress, NextGIS Web, and Sputnik Web tenants.

### Changed
- Recategorized THREDDS and ERDDAP endpoints from `opendata/` into `scientific/`, and Nesstar catalogs into `microdata/`.
- Discovery and harvest guides (viewers, scientific-domain, open data, geoportals, indicators) plus `docs/software-index.md` now cover the new software IDs.
- Regenerated dataset exports: **35,266** catalog records; 423 software definitions; 0 scheduled. Quality analysis reports **0** issues across **35,266** records.

### Removed
- **133** records relative to v1.19.0. Most are path recategorization (THREDDS/ERDDAP/Nesstar moved to `scientific/` or `microdata/`).
- Dropped unreachable or out-of-scope records including dead US ArcGIS Server / Hub directories, FRED, PNDB OpenDataSoft, generic dataX.io country sites, and duplicate THREDDS/ERDDAP adaptor URLs.

## Data exports (2026-09-08)

| Export | Count |
|--------|--------|
| `catalogs.jsonl` (+ `.zst`) | 35,266 catalog records |
| `software.jsonl` (+ `.zst`) | 423 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 0 scheduled sources |
| `full.jsonl` (+ `.zst`) | 35,266 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
