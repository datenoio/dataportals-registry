# Custom-software pattern analysis of recent additions — 2026-09-16

## Scope and method

Reviewed **547 verified-entity records** with `software.id: custom` that were added after
the 6–7 September custom-software reviews: the `d06d9b2292` (1,904 catalogs) and
`06415041b6` (1,174 catalogs) bulk commits plus uncommitted working-tree additions.
The cohort is 280 Indicators catalogs, 154 Geoportals, 44 Scientific repositories,
29 Open data portals, 19 Data marketplaces, and smaller groups; 467 records have curated
descriptions and 80 carry thin hunt-generated text ("powered by Custom software").

Method: grouped by catalog type, hostname, URL path prefix, description product tokens
and bigrams, and endpoint types; then verified candidate clusters with targeted GETs and
first-party documentation. Description mentions were checked for **disambiguation traps**:
many curated German/Brazilian records name a well-known product only to say the record is
*distinct from* it. Those mentions are not attributions and must not feed a classifier.

## Confirmed new-software candidates

### 1. Nazca4U Rapportagemodule — 21 records (strongest cluster)

All 21 Dutch "Bodeminformatie …" geoportals live on `{tenant}.nazca4u.nl/rapportage/`
(provinces, omgevingsdiensten, municipalities: OFGV, Friesland, Gelderland, Groningen,
Limburg, Maastricht, Sittard-Geleen, Venlo, Eindhoven, Noord-Brabant, Tilburg, Hilversum,
OD NHN, ODNZKG, Almelo, Overijssel, Utrecht, Zeeland, DCMR, Delft, OZHZ).

- Live GETs on two tenants return an identical ASP.NET application:
  `/Rapportage/Geolocator/{Map,Toolbar,Legend}/…` assets, `App_Themes/RapportageModule/*.css`,
  versioned `?v=13` asset URLs.
- Vendor site [nazca4u.nl](https://nazca4u.nl/) ("Nazca – Milieudata voor een beter beheer
  van de leefomgeving"); tenant pages call the product the *Rapportagemodule* and link the
  manual on nazca.solutions.
- **ID note:** `nazca` already exists for Soltesoft's Colombian cadastral SaaS — a different
  product. Use a distinct ID such as `nazca4u`.

### 2. GeCO-sys OpenData — 3 records

`gecoopendata.registrotumoriveneto.it/incidenza.php`,
`gecoopendata.puntozeroscarl.it/web/incidenza.php`,
`gecoopendata.registrotumorinapoli3sud.it/web/incidenza.php` — cancer incidence/survival
explorers of three independent Italian cancer registries (Veneto, Umbria, ASL Napoli 3 Sud).

- A [Registro Tumori Veneto poster](https://www.registrotumoriveneto.it/english/publications/meetings/posters/2018-posters/territorial-extension-of-the-veneto-tumour-registry-and-data-usability-in-the-new-web-portal/)
  names the application "GeCO-sys OpenData ©", describes its scalable architecture and
  AIRTUM record-layout integration, and states it is applicable to other registries.
- Live pages share the AdminBSB-based UI, `incidenza.php`/`sopravvivenza` pages, and
  `GeCOsys` strings. Suggested ID: `gecoopendata` or `gecosysopendata`.

### 3. ClimSeries (Somalia Climate TimeSeries Data) — 3 records

`climseries.faoswalim.org`, `climseries.imcpuntland.so`,
`www.imcsomaliland.org/climseries/station/` — hydromet station time-series apps for
FAO SWALIM, IMC Puntland, and IMC Somaliland.

- The [about page](https://climseries.faoswalim.org/about/) describes SCTD/ClimSeries as a
  reusable web application that "agencies that manage weather information can use"; the two
  IMC records explicitly call themselves ClimSeries *tenants*.
- All three serve the same AdminBSB dashboard (`/static/plugins/node-waves/`, morrisjs,
  `/station/map/{aws,mrs,ss,gws}/` routes). Suggested ID: `climseries`.
- Related FAO SWALIM family: SWIMS has two tenants (`swims.faoswalim.org`,
  `pwsims.imcpuntland.so` self-describes as "SWIMS-family"); FRRIMS has one. Possible
  follow-up `swims` definition once the Puntland tenant fingerprint is confirmed identical.

### 4. EIDA WFCatalog — 9 records

Nine ORFEUS EIDA nodes (ETH Zürich, BGR, LMU Munich, ICGC, NOA, INGV, Bergen/NORSAR,
NIEP, KOERI) each expose `/fdsnws/station/1/`, `/fdsnws/dataselect/1/`,
`/fdsnws/availability/1/`, and `/eidaws/wfcatalog/1/` endpoints.

- WFCatalog is a named, versioned EIDA web-service product with an official
  [specification](https://www.orfeus-eu.org/documents/WFCatalog_Specification-v0.22.pdf),
  [ORFEUS service page](https://orfeus-eu.org/data/eida/webservices/wfcatalog/), and EIDA
  source repository; every EIDA data centre deploys it.
- FDSN dataselect/station are protocol interfaces with multiple implementations, so the
  catalog-specific shared product is WFCatalog. Suggested ID: `wfcatalog`, with the
  description noting the accompanying FDSN/availability services.

## Reclassification candidates (existing definitions)

| Records | Target ID | Evidence |
|---|---|---|
| `statistiksachsendeschuelerabsolventenprognose`, `statistiksachsendevgrkreisergebnisse` | `cadenza` | Descriptions explicitly say "public Cadenza dashboard/workbook"; `cadenza` (Disy) definition exists with other Sachsen tenants |
| 6+ Ukrainian `mbk.*.gov.ua` hosts (`geombkdpgovua`, `zakarpatmbkgovua`, `mbkkradmingovua`, `ombkodessaua`, `mbktegovua`, `mbkcggovua`) | `softpro` | Existing `softpro` definition already documents "city MBK hosts"; SOFTPRO's own docs name the MBK geoportal product. Live fingerprint check still needed — Cloudflare returned 403 from this network |

## Single-record vendor SaaS (create only with first-party multi-customer evidence)

- **GovPilot** — `map.govpilot.com/map/NJ/atlanticcity`; live title "… | Powered by GovPilot",
  Telerik Kendo ASP.NET app, path-based municipal tenants. Vendor site lists many municipal
  customers, so a definition is defensible even with one registry record.
- **MapSifter** — `adamswa-mapsifter.publicaccessnow.com`; subdomain-tenant ASP.NET app
  (Disclaimer.aspx redirect).
- **Civil Solutions TMV** — `tmv.civilsolutions.biz/viewer/{id}`; "Howell Tax Maps",
  Mazer-based viewer on a vendor host.

## Follow-up leads (insufficient evidence today)

- **EMN DataHub** — four DOE Energy Materials Network consortia data hubs
  (`datahub-{chemcatbio,duramat,h2awsm,electrocat}.nlr.gov`) serve an identical Webpack
  module-federation shell ("Datahub {consortium} app", `js/remote-app-entry.js`). Shared
  platform, but no public product name/vendor page found; distinct from existing
  `datahubproject`.
- **Dutch municipal geoportals** — Apeldoorn (Vite SPA, `map-layer-tree` bundle) and Leiden
  (Laravel/Vite, `/api/maps/2.json`) are different stacks; no shared product in this sample.
- **Portuguese municipal SIG** — mixed vendors: Bragança credits "PH informática SA"
  (dhtmlx 3.6 client); Anadia runs an OpenLayers 4 build. No dominant shared product.
- **IDEBA viewer** — 18 records are per-municipality routes of one Province of Buenos Aires
  deployment; one host does not demonstrate shared software.
- **ARIC (ADB)** — 9 records are sub-catalogs of one ADB platform.

## Deliberate non-candidates (disambiguation traps)

Token matching on descriptions produces false positives here; do not reclassify:

- **GENESIS-Online (11), TabNet (6), GBE-Bund (7), LiKi (6), ThOnSA, IntMK, RTA-IS** —
  every mention is "Distinct from …" disambiguation text, or the record is the single
  official instance (e.g. `wwwlikinrwde`, `rtaiswtoorg`).
- **Carif-Oref (4)** — each region runs a differently named product (DataScope, ISEO,
  DAT@DECISION, Repères); no shared software shown.
- **DashkoN** — an advisory programme; sites are adaptations of the Münster Klimadashboard,
  not one installable product.
- **Satu Data Indonesia (6)** — initiative branding, not an implementation (consistent with
  the 7 September open-data review).
- **Mexico PED state monitors (8)** — MonitorBC, SIMEG, SICIP, SIG are per-state named
  systems.
- **CBD Clearing-House (2)** — two central CBD Secretariat hosts, one operator.
- **WTO databases (5), NISRA (5), WHO platform (3), IMF, UNStats, FAO pairs** — multiple
  routes of single-operator platforms.

## Applied changes (2026-09-16)

All four confirmed definitions were created and 44 records retagged:

| Software | Records retagged |
|---|---:|
| `nazca4u` (new) | 21 |
| `wfcatalog` (new) | 9 |
| `gecoopendata` (new) | 3 |
| `climseries` (new) | 3 |
| `cadenza` (existing) | 2 |
| `softpro` (existing) | 6 |

The SOFTPRO retag rests on the existing definition's documented "city MBK hosts" pattern
plus SOFTPRO's own geoportal gallery listing municipal MBK deployments; live fingerprint
checks were blocked by Cloudflare from this network. Discovery/harvest guide entries were
added (`discovery-geoportals-viewers.md`, `harvest-geoportals.md`, `discovery-indicators.md`,
`harvest-indicators.md`, `discovery-scientific-domain.md`, `harvest-scientific-domain.md`),
`software_ids.yaml` regenerated (527 ids), `wfcatalog` registered with a real probe map in
`apidetect_urlmaps_draft.py`, and the other three new IDs added to `NO_STANDARD_PROBE`.
Validation: `validate-software` gates pass, all 44 changed records pass `validate-yaml`,
build succeeded (38,459 catalogs / 527 software), full test suite 529 passed.

## Remaining follow-ups

1. Add GovPilot/MapSifter/TMV definitions only with vendor customer-list evidence; hunt for
   more tenants (`site:govpilot.com`, `*-mapsifter.publicaccessnow.com`) to raise value.
2. Probe the 80 thin-description records with the GET-only fingerprint workflow from the
   geoportal review — they are the least-analyzed pool.
3. EMN DataHub (`datahub-*.nlr.gov`, 4 tenants, identical module-federation shell) needs a
   public product identity before a definition.
4. SWIMS (FAO SWALIM family) has two tenants; confirm the Puntland tenant fingerprint is
   identical before a `swims` definition.

---

## Second pass (2026-09-16, evening)

Scope: the remaining ~503 recent custom records **plus** the Israeli municipal viewer
families committed earlier the same day (87 records from the IL hunts that were not in the
original two-commit window). Base-domain clustering of 586 records put two vendor families
on top that the first pass had missed because they sat outside the commit window:

| Cluster | Records | Outcome |
|---|---:|---|
| `gis-net.co.il` (v5 + mg1/mg2) | 64 | new `gisnet` (GISNET V5 by Complot) |
| `taldor.co.il` (`gis{NN}` hosts) | 19 | new `mapexpert` (Taldor MapExpert) |
| `faoswalim.org` / `imcpuntland.so` SWIMS | 2 | new `swims` |
| `map.govpilot.com` | 1 + 3 added | new `govpilot` |
| `*-mapsifter.publicaccessnow.com` | 1 | new `mapsifter` |
| `tmv.civilsolutions.biz` | 1 + 3 added | new `civiltmv` |

Both Israeli products were already named in the curated record descriptions from the
morning hunts ("GIS-NET v5 platform", "Taldor MapExpert platform"); the pass-1 host
analysis missed them because the files were committed before the analyzed window. Live
probing from this network is blocked (gis-net geo-blocks non-IL traffic, Taldor's WAF
answers 403), so attribution rests on the curated descriptions plus external evidence:
page titles `GISNET V5 By Complot - {city}` and the Complot user guide
(`gis.mavo.co.il/v5/GIS.pdf`) for GISNET; Taldor's documented municipal GIS practice
(Haifa, Herzliya, Ra'anana, Afula, Ness Ziona, Givatayim, Netanya) for MapExpert. One
`taldor.co.il` record stays `geoserver` (different stack).

SWIMS was confirmed by live GET on both tenants: identical AdminBSB/calcite-maps app,
`/dashboard/view` route, "Water Sources Information Management System" branding (PWIMS on
the Puntland IMC tenant).

The three single-record US vendor SaaS from the pass-1 follow-up list were resolved with
vendor evidence plus a bounded instance hunt (live GET per tenant):

- **GovPilot** — "Powered by GovPilot" titles; added Newark, Elizabeth, Trenton
  (Paterson and Hoboken 404 — rejected).
- **MapSifter** (TerraScan) — documented WA-county deployments (Pacific, Okanogan,
  Skamania, Klickitat, Adams); legacy `{county}.mapsifter.com` hosts time out and guessed
  `{county}wa-mapsifter.publicaccessnow.com` subdomains answer an AWS ALB
  `Target Group Heartbeat` default page, so no unverified tenants were added.
- **Civil Solutions TMV** — added Wall Township, Hudson County, Teaneck from search-result
  viewer URLs (tenant ids are opaque hashes; Washington Township, Jersey City, Edison
  remain documented but unadded).

Also fixed 14 stale `powered by Custom software` description strings on records retagged
in both passes and older hunts (softpro, localmaps, infomap, seoulopendataplaza, drupal,
geonetwork, rudi, arcgishub, ckan).

Totals for pass 2: **6 new software definitions** (`gisnet`, `mapexpert`, `swims`,
`govpilot`, `mapsifter`, `civiltmv`), **88 existing records retagged**, **6 new tenant
records added** (uids cdi00006949–cdi00006954), 14 description fixes. All six IDs
registered in `NO_STANDARD_PROBE` (viewer products without standard list APIs).
Discovery/harvest guide entries added to `discovery-geoportals-viewers.md` and
`harvest-geoportals.md`. Validation: `validate-software` gates pass, new/changed records
pass `validate-yaml`, build succeeded (533 software), full test suite 529 passed.

### Remaining follow-ups after pass 2

1. EMN DataHub (`datahub-*.nlr.gov`, 4 tenants, identical module-federation shell) still
   lacks a public product identity — the 10 KB loader bundle carries no attribution.
2. The ~80 thin-description records remain the least-analyzed pool; probe with the
   GET-only fingerprint workflow.
3. Dedicated-host GISNET cities (`gisn.tel-aviv.gov.il`) and documented-but-unadded TMV
   tenants (Washington Township, Jersey City, Edison) are bounded instance-hunt leads.
4. Spanish/Catalan municipal viewers (7 records) and the Ukrainian gov.ua remainder are
   mixed vendor stacks; no shared product confirmed yet.

---

## Third pass (2026-09-16, late evening)

Scope: the 498 records still custom after pass 2, prioritizing the 36-record
thin-description pool with the GET-only fingerprint workflow, plus a fresh token sweep
(which confirmed the German indicators cluster is all disambiguation mentions —
"Distinct from GENESIS-Online / TabNet / PxWeb / MATS / LiKi / HESIS / ThOnSA" — no
retags there; DashkoN is a SKEW consulting program, not software).

### New definitions and retags

| Software | Records | Evidence |
|---|---:|---|
| `ideba` (new) | 19 retagged | Live GET: Leaflet app, title `IDEBA`, per-tenant GeoServer workspaces (`geoserver-nodo2.../geoserver/{municipio}/wfs\|wms`) |
| `intertownup` (new) | 2 retagged + 4 added | "UP by Intertown" branding; all tenants live (HTTP 200, `GIS Intertown` title) |
| `atlas` (new) | 2 retagged | Title `Atlas · Gemeente X`, Vue SPA at `/atlas/static/assets/`; product identified via VNG/GitLab (Purmerend, EUPL 1.2) |
| `mappi` (new) | 2 retagged + 3 added | `tenant-id` meta + shared `app-version` build hash `bad0af65083`; vendor product page mappi.nl (Swis) with customer list |
| `mapguide` (existing) | 5 retagged | PH Informática shell (phinformatica.pt credit) over `mapguide/mapviewerajax/ajaxviewer.aspx`, dhtmlx36+bjqs |
| `kaartviewer` (existing) | 1 retagged | Helmond page exposes `/admin/rest/kaartviewerapi/menu` + `geonovationbv` assets |
| `liferay` (existing) | 1 retagged | IDEBarcelona on Liferay (`DibaProducte-theme`, `/o/frontend-js-aui-web`) |
| `wordpress` (existing) | 1 retagged | Castellar del Vallès map gallery on WordPress |
| `joomla` (new) | 1 retagged | abn.ne generator meta + `/media/`/`/components/com_*` |

New tenant records: Intertown UP ×4 (Hevel Modi'in, Merom HaGalil, Megiddo, Shur kot —
uids cdi00007001–7004), Mappi ×3 (Amsterdam, Katwijk, Westerkwartier — uids
cdi00007005–7007). Rejected: kaart.rotterdam.nl (timeout), kaart.marathon.nl and
kaart.groningenbereikbaar.nl (event/project maps, out of scope), Anadia (ol3 custom),
Amadora (redirect stub).

### Still custom after pass 3 (~460)

- Ukrainian gov.ua viewers: Cloudflare 403 / timeouts from this network (kyivcity,
  kr-rada, mkadastr, tmrada, rv); forestry.org.ua (Django), gisrr.gov.ua (Vue SPA),
  map.vmr.gov.ua, smart.khmr.gov.ua (ArcGIS JS 3.39) are bespoke government builds.
- Spanish/Catalan remainder: Mataró (custom Leaflet), Manresa (sigmap React), Cáceres
  (Angular), cime.es Menorca (custom), b5m Gipuzkoa (custom) — all one-off stacks.
- US county one-offs: atlantic-county (ArcGIS JS 3.10 aerial viewer), pip.mercercounty
  (Angular PIP), imap.klickitatcounty (allegro.js), maps.co.jefferson.or.us (timeout).
- zamwis.zambezicommission.org (empty shell), sig.cm-anadia.pt, geoportal.cm-amadora.pt.
- The long tail of single-operator IGO/government databases (wto.org, who.int, adb.org,
  nisra.gov.uk, brandenburg.de, bayern.de, nrw.de, sachsen.de, iom.int, unu.edu...).

Validation: `validate-software` gates pass, changed records pass `validate-yaml`,
`software_ids.yaml` at 538 ids, build succeeded, full test suite 529 passed.

### Remaining follow-ups after pass 3

1. EMN DataHub (`datahub-*.nlr.gov`) still lacks a public product identity.
2. Atlas instance hunt: Utrecht and Purmerend (datalab.purmerend.nl/atlas) are
   documented tenants not yet registered.
3. Mappi: kaart.rotterdam.nl needs a retry from another network; mappi.nl customer
   list may name more municipalities.
4. GISArts COOK GIS Viewer (~50 NL municipalities) and GeoApps (mapgear.nl) surfaced
   as vendor leads during the Mappi hunt — no registry records matched their
   fingerprints yet; worth a dedicated tenant-list hunt.
5. Ukrainian remainder needs probing from a non-blocked network.

---

## Fourth pass (2026-09-16, night)

Scope: pass-3 follow-ups plus a full-pool sweep of all 7,101 remaining custom records.

1. **Atlas instance hunt** — added `datalabpurmerendnlatlas` (uid cdi00007025), the product's
   home-municipality tenant. Utrecht checked: `kaartutrechtnl` is already `kaartviewer`
   (correct — Utrecht's public map is KaartViewer, not Atlas), `geodatautrechtnl` is
   `geoserver` (correct).
2. **EMN DataHub resolved (stays custom)** — the 2021 NLR paper documents the EMN hubs as
   CKAN-based, but the current module-federation React frontend answers SPA fallback on
   `/api/3/action/*`; no CKAN API is exposed on tenant hosts and no public product name
   exists ("Datahub {consortium} app"). Not CKAN-taggable today.
3. **Ukrainian `*.mapa.gov.ua` lead (blocked)** — the dnipro-map open-source project (MIT,
   multi-city) suggests a city-map family, but all mapa.gov.ua hosts time out from this
   network and the upstream repo is stale (2022). No records added.
4. **Full-pool fingerprint sweep** — zero remaining custom records match any product defined
   in passes 1–3. Top base-domain clusters are single-operator estates (go.kr, go.id,
   nasa.gov, nih.gov, go.jp, europa.eu); path clusters are generic; the Chinese `/sjkf`
   cluster is bespoke municipal CMS sections.

**Conclusion:** registry-internal pattern mining of the custom pool is exhausted. Future
passes should be evidence-driven hunts (vendor tenant lists like GISArts COOK and GeoApps,
FOFA/Censys fingerprint queries, per-country reviews) rather than another clustering round.

Validation: build succeeded, 529 tests pass.
