# Custom-software pattern analysis of recent additions — 2026-09-20

## Scope and method

Reviewed the **255 uncommitted verified-entity records** added after the 16 September
four-pass review (`custom-software-recent-additions-2026-09-16.md`), of which **145** carry
`software.id: custom`. Type shape: 87 Geoportals, 29 Open data portals, 20 Indicators
catalogs, 8 Scientific repositories, 1 Datasets list. Country shape: DE (24), CL (21),
IT (15), PT (13), FR (11), GR/AT (7 each), RU/AL (6 each), RO/CH (5 each).

Method: grouped by country/hostname/URL-path, mined descriptions for product tokens, then
confirmed candidate clusters with targeted live GETs (title, `generator`/`x-powered-by`
headers, asset paths) and first-party vendor/product pages. Cross-checked against the
16 September review to avoid re-proposing exhausted leads. Most of the batch is genuinely
bespoke one-off stacks (Drupal, WordPress, TYPO3, plain Leaflet/OpenLayers, Angular/React
SPAs) and stays `custom`.

## New definitions created and records retagged

| Software | Records | Evidence |
|---|---:|---|
| `gajamatrix` (new) | 3 | Merseburg title "GajaMatrix GeoPortal"; Wasser Nord header `x-powered-by: GajaMatrix GIS` (WildFly); Gera. Vendor product page geoinformationssystem.net (Gingko.Systeme) lists municipal tenants. |
| `gbdwebsuite` (new) | 2 | Schmallenberg + Hase-Wasseracht share `/_/webSystemAsset/path/{app,vendor,util}.js`, `gc/main` React module, `gwsLogin`/`gwsOptions`. OSS product page gbd-websuite.de + GitHub gbd-consult/gbd-websuite. |
| `inventwebgis` (new) | 2 | ARRSH `/aps/?name=arrsh` + ATP `/apps/?name=atp` serve `invent.css`. Vendor invent.al confirms the WebGIS product line. |
| `mapguide` (existing) | 3 | Sabugal, Monção, Castro Marim serve `Mapguide.redraw(true)` + `dhtmlx36` under a PH Informática shell — the pass-3 (16 Sep) pattern over `mapviewerajax/ajaxviewer.aspx`. |

GajaMatrix note: the four `*.gajamatrix.de/geoserver` and `gdi.gajamatrix.de/geonetwork`
records stay `geoserver`/`geonetwork` (backend endpoints); only the three GeoPortal **UI**
frontends (Merseburg, Gera, Wasser Nord) take `gajamatrix`.

INVENT note: the two IKTK heritage viewers (arkeologjia/monumente.iktk.gov.al) are a
separate OpenLayers/GeoExt build, **not** INVENT — they stay `custom`.

## Follow-up leads (insufficient evidence today)

- **geOrchestra Datahub** — `sig.grandbeauvaisis.fr` serves `georchestra.css` +
  `datahub-root`. Real OSS product (georchestra.org), but one registry record; watch for
  more tenants before a `georchestra`/`datahub` definition.
- **MapGate** (Havelland `geoportal.hvlnet.de/mapgate/`), **CartoMapas** (Alcoutim),
  **Assec Sim!** (AMCB), **GeoPlan** (Albergaria) — single records, no multi-customer
  product page confirmed. Keep `custom`.
- Chilean IDE portals, Italian SPARQL/LOD portals (Drupal/WordPress/interact mixed),
  Greek/Romanian/Austrian sites — heterogeneous one-off stacks; no shared product.

## Validation

`sync-software-maps` (638 ids), `validate-software` gates pass, the 10 changed records pass
`validate-yaml --id`, discovery/harvest guide entries added (`discovery-geoportals-viewers.md`,
`harvest-geoportals.md`), the three new ids registered in `NO_STANDARD_PROBE`
(`apidetect_urlmaps_draft.py`), `docs/software-index.md` regenerated, build succeeded
(39,371 catalogs / 638 software), full test suite 622 passed.

Pre-existing failure unrelated to this change: `test_quality_regression.py::
test_current_report_matches_baseline_when_unchanged` (committed `full_report.jsonl` shows 0
CRITICAL vs Sep 17 baseline 3; both files predate and are unmodified by this change —
confirmed by stashing). The new batch still needs `analyze-quality` + baseline refresh as
part of the normal quality workflow.
