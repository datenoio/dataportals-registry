# dataportals-registry v1.18.0

**Release date:** August 28, 2026

## Summary

This release adds 2,243 net new catalogs and 20 software platform definitions. Coverage expands with Nordic and municipal geoportal products (e-mapa.net, Loftmyndir, Alta, Hajk, KortInfo, Swing / inCijfers), scientific repository hunts (DSpace, DiVA, CLLD, TalkBank), MappingSupport ArcGIS Server roots, and country-depth passes for India, Nigeria, and others. Dataset exports are rebuilt to match source YAML. Quality analysis reports 0 issues.

## What's in this release

### Added
- **2,243 net new catalog entries**; registry source now **24,993** entities (**7** scheduled) across **219** country/territory folders.
- **20 software definitions**; software catalog now **282** platforms: Archipelago, Redivis, MapCentia GC2, hale»connect, BirdMap Africa, Istat Data Browser, e-mapa.net, Loftmyndir Kortasjá, Alta Vefsjá, DiVA Portal, Swing / inCijfers, CLLD, Bulplan UNIMAP, Tobel GIS, geoportal.ch, Evrymap, Hajk, NIRAS KortInfo, OpenGDC, and TalkBank.
- **257** US ArcGIS Server geoportals from the MappingSupport federal/state/county/city GIS server list.
- **148** ArcGIS Hub geoportals promoted from scheduled review.
- **183** Swing / inCijfers indicator catalogs (Netherlands, Flanders, Euregional Health Atlas).
- **125** Polish e-mapa.net county and city geoportals; **77** Icelandic geoportals; **77** Thai local-government CKAN portals; **52** Slovenian iObčina sites.
- **651** scientific repositories from later coverage passes, including **354** DSpace, **41** CLLD, **39** Japanese WEKO3, and **21** Swedish DiVA Portal.

### Changed
- Clarified `properties.is_national`: `true` only for the country's official catalog of that type. Unset on **988** agency/thematic/scientific/subnational records.
- Retagged existing catalogs onto the new software IDs (GC2, hale»connect, BirdMap, CLLD, TalkBank, OpenGDC, Swing, DiVA, and others).
- Promoted **289** catalogs from scheduled review. Scheduled queue holds **7** South African institutional repositories pending live promotion.
- Regenerated dataset exports: **24,993** catalog records; 282 software definitions; 7 scheduled. Quality analysis reports **0** issues across **24,993** records.

### Fixed
- `builder.py build` writes `datasets.duckdb` with native DuckDB `LIST` and `STRUCT` types instead of VARCHAR JSON strings.
- Dropped invalid `owner.location.macroregion` on GeoRhena (`sdigeorhenaeu`).

### Removed
- Duplicate Datarade record at `datarade.com`; keeper is `datarade.ai`.
- **8** scheduled catalogs dropped without promotion (duplicates, dead hosts, empty dashboards).

## Data exports (2026-08-28)

| Export | Count |
|--------|--------|
| `catalogs.jsonl` (+ `.zst`) | 24,993 catalog records |
| `software.jsonl` (+ `.zst`) | 282 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 7 scheduled sources |
| `full.jsonl` (+ `.zst`) | 25,000 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
