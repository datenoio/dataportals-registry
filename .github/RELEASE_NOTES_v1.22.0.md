# dataportals-registry v1.22.0

**Release date:** September 24, 2026

## Summary

This release adds 3,997 net new catalogs and 179 software platform definitions. Coverage expands with municipal GIS and open-data SaaS (Map2Web, Municipium, BODIK ODCS, LDP SIT, GFMaplet, GajaMatrix, and related products), custom-catalog retags onto named software IDs, and maintainer tooling for hunts, batch ingestion, and scheduled promotion. Dataset exports match source YAML. Quality analysis reports 0 CRITICAL and 0 IMPORTANT issues.

## What's in this release

### Added
- **3,997 net new catalog entries**; registry source now **41,167** entities (**1** scheduled) across **224** country/territory folders.
- **179 software definitions**; software catalog now **665** platforms. Highest-count new IDs include Map2Web (`map2web`, **258**), Municipium (`municipium`, **153**), BODIK ODCS (`bodikodcs`, **143**), OPUS (**107** new files), LDP SIT (`ldpgis`, **94**), GeoNode (**81**), GeoServer (**80**), GFMaplet (`gfmaplet`, **73**), and CKAN (**58**).
- GajaMatrix (`gajamatrix`, **35**), Go GIS (`gogis`, **25**), CityViz (`cityviz`, **24**), EKAN (`ekan`, **20**), R3GIS (`r3gis`, **16**), KaartViewer, enMapa, Nexus Public Portal, and further municipal Web GIS products.
- `scripts/hunt.py` discovery hunt toolkit, `builder.py add-batch` / `enrich-batch` / `set-field`, incremental `assign --new` and `validate-yaml --changed`, and a reworked scheduled-promotion flow.

### Changed
- Custom-catalog and platform review retagged **504** catalogs onto a named `software.id` (largest moves: CKAN to BODIK ODCS **143**, `custom` to Drupal **100** and WordPress **80**).
- Dropped two unreachable scheduled hosts. One Czech GISPLAN cemetery map remains scheduled. Renamed the Marburg-Biedenkopf geoportal so the filename matches `id`.
- Rebuilt dataset exports: **41,167** catalogs, **1** scheduled, **665** software (`full.jsonl`: **41,168**).
- Quality analysis: **0** CRITICAL and **0** IMPORTANT across **41,167** records (**158** MEDIUM and **53** LOW enrichment gaps). Refreshed `dataquality/baseline_counts.json`.

## Data exports (2026-09-24)

| Export | Count |
|--------|--------|
| `catalogs.jsonl.zst` | 41,167 catalog records |
| `software.jsonl` (+ `.zst`) | 665 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 1 scheduled source |
| `full.jsonl` (+ `.zst`) | 41,168 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
