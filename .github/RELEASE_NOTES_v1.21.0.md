# dataportals-registry v1.21.0

**Release date:** September 12, 2026

## Summary

This release adds 1,904 net new catalogs and 63 software platform definitions. Coverage expands with custom-catalog OSS IDs (Géoclip, GeoNature, FROST-Server, MINERVA, Datasette, TerriSTORY, InstantAtlas, OPENDATAENTE), harvest and apidetect recipes for those platforms, and an empty scheduled queue. Dataset exports are rebuilt to match source YAML. Quality analysis reports 0 issues.

## What's in this release

### Added
- **1,904 net new catalog entries**; registry source now **37,170** entities (**0** scheduled) across **224** country/territory folders.
- **63 software definitions**; software catalog now **486** platforms. Highest-count new IDs: Géoclip (`geoclip`, **47**), GeoNature (`geonature`, **29**), FROST-Server (`frostserver`, **22**), MINERVA (`minerva`, **16**), Datasette (`datasette`, **14**), TerriSTORY (`terristory`, **13**), InstantAtlas (`instantatlas`, **13**), and OPENDATAENTE (`opendataente`, **13**).
- **47** Géoclip observatories, **29** GeoNature-atlas instances, and **22** public FROST-Server SensorThings APIs.
- **16** MINERVA pathway-map servers, **14** Datasette sites, **13** TerriSTORY regional hubs, **13** InstantAtlas report sites, and **13** OPENDATAENTE comuni.
- WebMain, LORIS, iMonitoring, IHK-Fachkräftemonitor, DUVA, JAXI, MATS, DANDI, CEDAR, EvalAI, and further scientific/metadata IDs remapped from `custom`.

### Changed
- Emptied the scheduled queue (promoted live finds; dropped unreachable or out-of-scope hosts).
- Discovery and harvest guides plus `docs/software-index.md` now cover the new software IDs; apidetect URL maps were filled for documented list APIs.
- Stop publishing uncompressed `data/datasets/catalogs.jsonl` (GitHub size); keep `catalogs.jsonl.zst`.
- Regenerated dataset exports: **37,170** catalog records; 486 software definitions; 0 scheduled. Quality analysis reports **0** issues across **37,170** records.

### Removed
- **1** record path relative to v1.20.0: IRI Climate Data Library recategorized from `opendata/` to `geo/`.

## Data exports (2026-09-12)

| Export | Count |
|--------|--------|
| `catalogs.jsonl.zst` | 37,170 catalog records |
| `software.jsonl` (+ `.zst`) | 486 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 0 scheduled sources |
| `full.jsonl` (+ `.zst`) | 37,170 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
