# Spain `custom` software review (2026-09-28)

Scope: all 192 entries under `data/entities/ES/` with `software.id: custom`
(91 open data portals, 38 geoportals, 37 scientific repositories, 24 indicator
catalogs, 1 microdata catalog, 1 API catalog).

Method: live fingerprinting of every `link` (HTTP fetch, 171/192 responded after
retry with HTTPS upgrade), meta-generator/header/HTML fingerprint matching, CKAN
API probing (`/api/3/action/status_show`), and clustering by owner/domain.

## A. Entries misclassified as `custom` — existing software definitions apply

### Confirmed

| Entry | Current | Should be | Evidence |
|---|---|---|---|
| `datosabiertosbneescatalogodataset` (BNE) | custom | `ckan` | `/catalogo/api/3/action/status_show` returns `"success": true`, "ckan-docker *spatial Open Data portal" |
| `datosabiertosaguasdealicante` (`datosabiertos-aguasdealicante.pre.apsl.io`) | custom | `ckan` | meta generator `ckan 2.10.5`. NOTE: link is a staging (`*.pre.*`) domain — needs a production URL |
| `datosabiertosmitecogobes` (MITECO open data) | custom | `drupal` | Drupal fingerprint on datosabiertos.miteco.gob.es |
| `sicawebmitecogobes` (MITECO SICA) | custom | `wordpress` | meta generator `WordPress 7.1.2` |
| `datospfcyles` (JCyL PF) | custom | `drupal` | Drupal fingerprint |
| `valledemenaesparticipaciondatosabiertoscatalogoded` | custom | `drupal` | Drupal fingerprint |
| `aytovillaviciosadeodonesportaldetransparenciadatos` | custom | `drupal` | Drupal fingerprint |
| `dodibacat` (Diputació de Barcelona open data API) | custom | `drupal` | Drupal fingerprint |
| `wwwcoreses` (CORES estadísticas) | custom | `drupal` | Drupal fingerprint |
| `observatoriosaudepublicasergasgal` | custom | `drupal` | Drupal fingerprint |
| `losbarrioseselconsistorioayuntamientoparticipacion` | custom | `wordpress` | WordPress fingerprint |
| `bimcvcipfes` | custom | `wordpress` | WordPress fingerprint |
| `wwwproteoredorg`, `evolclustdborg`, `wwwlifewatcheu`, `wwwyeastidorg` | custom | `wordpress` | WordPress fingerprints (scientific repos on WordPress) |
| `idedipujaenes` (IDE Cádiz/Jaén geoportal) | custom | `joomla` | Joomla fingerprint |
| `idechgchguadalquiviresnodocatalogodatoshtml` (CHG) | custom | `liferay` | Liferay fingerprint |
| `minhapgobesesesdatos20abiertospaginasdatosabiertos`, `sedepuertosgobespaginascatalogorispaspx`, `portalminecogobesesesministeriopaginascontactoaspx`, `chjesesesciudadanoreutilizacionpaginasreutilizacio` | custom | `sharepoint` | Classic SharePoint publishing paths (`/Paginas/*.aspx`, `/es-ES/...`) on ministerial sedes |

### Suspected, needs verification (sites block automated probes — Cloudflare/WAF/timeouts)

| Entries | Suspected | Why |
|---|---|---|
| `opendataterrassacat`… (terrassa 403), `dadesobertessabadellcat`, `opendatasabadellcat`, `datosabiertostorrentes`, `opendatamanresacat` | `ckan` | CKAN-style paths `/es/dataset`, `/dataset`; all block bots (Cloudflare "Just a moment" / timeouts) |
| `datosabiertoslaspalmasgcesdata` | `ckan` (behind WordPress front) | WordPress 4.9.8 front page that embeds/links a CKAN catalog |
| `ideaytoecija` (94.130.11.214:5000), `serviciopescamapamaes` (acuivisor), `b5mgipuzkoanet` | `geonetwork`/`geoserver` | HTML references; b5m is likely Gipuzkoa's own SDI — check before reclassifying |
| `geoportalmadrides` (`IDEAM_WBGEOPORTAL/index.iam`) | MapGuide (new def?) | `.iam` pages = Autodesk MapGuide, not ArcGIS |

## B. Repeating platform families — candidates for NEW software definitions

Registry precedent for owner-specific platforms already exists
(`gipuzkoairekia`, `dataworldbankorg`, `seoulopendataplaza`, `twtovopendata`-style defs).

1. **Open Data Euskadi** (`opendataeuskadi`) — strongest candidate.
   Basque Government open data platform with its own API and DCAT feed.
   Entries: `opendataeuskadieus` + `opendataeuskadieuscatalogodatos`
   (**these two are duplicates of the same portal — merge first**).
   The wider euskadi.eus stack also covers `wwwgeoeuskadieus` (geoEuskadi) and
   `wwweuskadieusindicadoresmunicipales` (Udalmap) — could share one
   `euskadi` platform family def or keep the geo/indicators ones separate.
   Precedent: `gipuzkoairekia` already covers Gipuzkoa's platform.

2. **Idescat** (`idescat`) — Catalan statistics institute platform with a public
   API (api.idescat.cat). 3 entries, all custom today:
   `wwwidescatcatestad`, `wwwidescatcatemex`, `wwwidescatcatods`.

3. **INEbase / INE dyngs** (`inebase`) — INE's dissemination platform
   (dyngs/INEbase + JSON API). 4 entries:
   `wwwinees` (microdata), `wwwineesinebase`, `wwwineesdyngsods`,
   `ineessssatellitel0cpagecid1259942408928p1259942408`.

4. **IECA statistical systems, Andalucía** (`sima`/`ieca`) — 5 entries
   (ARGOS, BADEA, SIMA, INDEA, ODS-Andalucía). The newer SIMA/INDEA/ODS portal
   pages are Drupal-based, so either reclassify those three to `drupal` or
   define one IECA platform def. Weaker than 1–3 because the products differ.

5. **Zaragoza "sede" platform** (`zaragozasede`) — 2 entries
   (`wwwzaragozaes` catalog + `zaragozaesciudadrisp`), well-known custom city
   platform with a public API. Optional.

6. **CAIB GUSITE** — Balearic Government CMS (meta generator `CAIB GUSITE v1.6`).
   Only 1–2 entries (`wwwcaibcat`); below the bar unless more CAIB sites appear.

NOT candidates: the 37 scientific repositories are almost all unique one-off
research databases (bioinformatics, astronomy) — `custom` is correct there.

## C. Data-quality issues surfaced during the review

1. **Fabricated endpoint bundles**: 8 entries carry an identical templated
   endpoint set (`/api/3`, `/api/3/action/package_list`, `/api/v2/catalog`,
   `/api/views`, `/api/feed/dcat`, `catalog.xml|rdf|jsonld`) that does not
   exist on the target (e.g. mites.gob.es/api/3 → 302 to error page):
   `gobiernoabiertocuencaescatalogo`, `losbarrioseselconsistorioayuntamientoparticipacion`,
   `datosabiertostorrentesesdataset`, `opendatasantfeliucatescatalogodatos`,
   `mitesgobesesdatosabiertosindexhtm`, `idechgchguadalquiviresnodocatalogodatoshtml`,
   `datosapces`, `getxoeusesgobiernoabiertoopndata`. These endpoints should be
   removed or verified individually.
2. **Truncated links** (`…` in the URL) in 12 entries, incl. `valladolides…`,
   `chjesesesciudadano…`, `sedesepegobes…`, `ineessssatellite…`.
3. **Duplicate**: `opendataeuskadieus` vs `opendataeuskadieuscatalogodatos`.
4. **21 URLs unreachable** in two probe rounds (timeouts/resets) — candidates
   for status review (e.g. `opendata.pamplona.es`, `idemap.es`, `datos.apc.es`,
   `catastro.gisdata.es`).
5. **Staging URL**: `datosabiertos-aguasdealicante.pre.apsl.io` is a
   pre-production APSL domain.

Raw probe data: `/tmp/es_custom/merged.json` (per-URL status, fingerprints),
`/tmp/es_custom/entries.json` (parsed YAML index).

---

## Applied changes (2026-09-28)

- **New software definitions**: `opendataeuskadi` (opendata), `idescat` (indicators),
  `inebase` (indicators), with URL maps in `scripts/apidetect_urlmaps_draft.py`
  (`opendataeuskadi` in `NO_STANDARD_PROBE`), discovery/harvest guide sections, and
  regenerated `docs/software-index.md` + `data/reference/software_ids.yaml`.
- **Reclassified 30 entries** from `custom`: ckan ×2 (BNE, Aguas de Alicante — link
  fixed to the production domain and real CKAN endpoint recorded), drupal ×7,
  wordpress ×7, joomla ×1, liferay ×1, sharepoint ×4, opendataeuskadi ×1,
  idescat ×3, inebase ×4.
- **Merged** the duplicate Open Data Euskadi entries (kept `opendataeuskadieus`,
  canonical uid `cdi00010936`).
- **Stripped fabricated templated endpoint bundles** from 8 entries; kept verified
  sitemaps (Los Barrios, MITES, CHG).
- **Constants**: `inebase` allowed under Microdata/Open data portal; allowed-type sets
  added for `governmentsitebuilder` and `craftcms`; 7 entries fixed `Redbox` → `ReDBox`.
- ES entries with `software.id: custom`: 192 → 161.

Pre-existing failures left untouched (not from this change): 87 unmapped software ids
in `test_apidetect`, quality baseline drift from the uncommitted registry-wide WIP
(`scripts/update_quality_baseline.py` is the sanctioned follow-up), and 3
bs4/parser-related enrichment tests.

## Follow-up changes (2026-09-29)

Verified the Cloudflare/geoblock cluster via Wayback Machine evidence:

- **CKAN confirmed**: Open Data Terrassa (meta generator `ckan 2.11.2`),
  Manresa (`ckan 2.3.2`), Torrent (historic `/base/images/ckan-logo-footer.png`
  assets; live site geoblocks). Reclassified to `ckan`.
- **Joomla confirmed**: Sabadell (Joomla + `com_iasmetadadesarticles` component on
  both old and new domains). Reclassified `dadesobertessabadellcat` to `joomla`.
- **WordPress confirmed**: Las Palmas de Gran Canaria (WordPress since 2015 — the
  older `ckan` tag was wrong) and La Pobla de Vallbona (WordPress 4.7 + qTranslate).
- **Duplicates merged** (3 more): Terrassa (kept uid cdi00010801), Las Palmas
  (kept cdi00000554), Sabadell old domain (kept cdi00010192).
- **Status → inactive (dead DNS, NXDOMAIN/SERVFAIL via 1.1.1.1 and 8.8.8.8)**:
  `datosuaes` (no A record), `opendatasantfeliucatescatalogodatos` (successor on
  seu-e.cat already registered), `transparencialapobladevallbonaesesdatosabiertoscat`
  (successor dadesobertes.* entry active), `catastrogisdataes`. `sedempr` was
  already inactive.
- All other unreachable URLs resolve DNS and have 2025-2026 Wayback snapshots —
  they geoblock foreign/cloud IPs but are alive; kept `status: active`.

ES entries with `software.id: custom`: 161 → 150 (this follow-up removed 6;
parallel in-tree WIP between sessions reclassified 5 more, e.g. `datosapces` → ckan,
`wwwopendatabizkaiaeus` → ckan, `wwwideandaluciaes` → geonetwork).
