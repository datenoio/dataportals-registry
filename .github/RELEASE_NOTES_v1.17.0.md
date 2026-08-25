# dataportals-registry v1.17.0

**Release date:** August 25, 2026

## Summary

This release adds 2,608 net new catalogs and 15 software platform definitions. Coverage expands with 2,409 OpenAIRE scientific repositories, 105 IMF National Summary Data Page catalogs, domain scientific stacks (InterMine, GRIN-Global, Synapse, LabKey, XNAT, OMERO, ESA Science Archive), and first entity roots for Jersey and Saint Helena. The scheduled queue is cleared. Dataset exports are rebuilt to match source YAML.

## What's in this release

### Added
- **2,608 net new catalog entries**; registry source now **22,750** entities (**0** scheduled) across **219** country/territory folders, including first entity roots for **Jersey (JE)** and **Saint Helena (SH)**.
- **15 software definitions**; software catalog now **262** platforms: IMF NSDP, ODWeb, LabKey, Synapse, XNAT, OMERO, Kadi4Mat, e!DAL, NOMAD, InterMine, GRIN-Global, PlutoF, JGI Genome Portal, cBioPortal, and ESA Science Archive.
- **2,409** scientific repositories promoted from the OpenAIRE Graph harvest after live URL review.
- **105** IMF National Summary Data Page catalogs from the DSBB directory (**118** `imfnsdp` records in total).
- Domain scientific catalogs on the new software IDs: **25** InterMine, **13** GRIN-Global, **10** ESA Science Archive, **10** Synapse, **6** each LabKey / XNAT / OMERO, plus cBioPortal, Kadi4Mat, and JGI.
- **9** UK local-government Cadcorp SIS WebMap geoportals. OpenAIRE Graph harvest script (`scripts/extract_openaire_portals.py`).

### Changed
- National catalogs moved under `{CC}/Federal/`, with type and subregion path corrections. Jersey open data moved out of GB into `JE/`; the St Helena CKAN moved into `SH/` and marked inactive.
- Scheduled queue cleared. Regenerated dataset exports: **22,750** catalog records; 262 software definitions; 0 scheduled.
- Catalog schema now requires string country/macroregion ids, string tags, and integer `dataset_count_reported`. Quality analysis reports **0** issues across **22,750** records.

### Removed
- Duplicate University of Granada Open Data and Cyprus ERMIS-F geoportal records merged into keepers.
- Cocos (Keeling) Islands (`CC`) and `Unknown` country folders (records recategorized or dropped).
- **3** Cadcorp scheduled viewers that did not respond; **664** OpenAIRE scheduled sources that were dead, duplicate, staging, parked, or not a catalog.

## Data exports (2026-08-25)

| Export | Count |
|--------|--------|
| `catalogs.jsonl` (+ `.zst`) | 22,750 catalog records |
| `software.jsonl` (+ `.zst`) | 262 software/platform definitions |
| `scheduled.jsonl` (+ `.zst`) | 0 scheduled sources |
| `full.jsonl` (+ `.zst`) | 22,750 combined entities + scheduled |
| `full.parquet`, `datasets.duckdb` | Analytics-friendly exports |

## Full changelog

See [CHANGELOG.md](../CHANGELOG.md) for full history.
