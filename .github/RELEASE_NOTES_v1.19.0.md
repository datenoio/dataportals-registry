# dataportals-registry v1.19.0

**Release date:** September 3, 2026

## Summary

This release adds 4,823 net new catalogs and 84 software platform definitions. Coverage expands with municipal GIS viewers (Experience Builder, Mapotip, GisMaster, GISPLAN, Web AppBuilder, IntraMaps, SonicWeb, GEPRO, EVALD, Pozi, ALANDIS+, Public Maps), country-depth geoportal and institutional-repository hunts, and first entity roots for Bermuda, French Polynesia, and Réunion. The scheduled queue is empty. Dataset exports are rebuilt to match source YAML. Quality analysis reports 0 issues.

## What's in this release

### Added
- **4,823 net new catalog entries**; registry source now **29,816** entities (**0** scheduled) across **222** country/territory folders (added Bermuda `BM`, French Polynesia `PF`, and Réunion `RE`).
- **84 software definitions**; software catalog now **366** platforms. Highest-count new IDs: ArcGIS Experience Builder (`experiencebuilder`, **193**), Mapotip (`mapotip`, **137**), GisMaster (`gismaster`, **135**), GISPLAN (`gisplan`, **128**), ArcGIS Web AppBuilder (`webappbuilder`, **114**), IntraMaps Public (`intramaps`, **107**), SonicWeb (`sonicweb`, **105**), Geoportál GEPRO (`gepro`, **99**), KOVGIS EVALD (`evald`, **80**), Pozi (`pozi`, **78**), ALANDIS+ (`alandis`, **76**), and GeoMedia SmartClient Public Maps (`publicmaps`, **69**).
- **291** ArcGIS Hub and **278** ArcGIS Server geoportals; **159** Slovenian iObčina municipal GIS portals.
- **77** Finnish Sitowise Louhi, **72** Finnish QWC2, and **20** Finnish Trimble Locus IMS geoportals; **36** Romanian GISApp viewers and **31** Turkish NetGIS Server catalogs.
- **65** Indonesian open-data portals plus Palapa geoportals; **17** Taiwan DGBAS Web statistical databases and **25** South Korean indicator catalogs.
- Scientific coverage including **30** Belarusian institutional repositories, **22** Croatian DABAR IRs, **10** Indian Biological Data Centre archives, **7** South African DSpace IRs promoted from scheduled review, and further Global South / small-state repositories.

### Changed
- Retagged existing catalogs onto the new software IDs (Experience Builder, Web AppBuilder, Nesstar, Pure, D4Science, and others).
- Promoted the remaining **7** scheduled South African institutional repositories and **135** Italian GisMaster comuni to entities. Scheduled queue is now empty (**0**).
- Discovery and harvest guides include hunt patterns from post-v1.18.0 sessions (national harvest sources, dataset-bearing university IRs, country indicators, named directories).
- Regenerated dataset exports: **29,816** catalog records; 366 software definitions; 0 scheduled. Quality analysis reports **0** issues across **29,816** records.

### Removed
- **10** Kazakhstan university institutional repositories with no dataset records (publication-only IRs).
- Duplicate US ArcGIS Server records for Fort Bend County and Will County GIS REST.
- IBESTAT Open Data Service after the Balearic indicators catalog moved to the eDatos record.

## Data exports (2026-09-03)

| Export | Count |
|--------|--------|
| `catalogs.jsonl` (+ `.zst`) | 29,816 catalog records |
| `software.jsonl` (+ `.zst`) | 366 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 0 scheduled sources |
| `full.jsonl` (+ `.zst`) | 29,816 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
