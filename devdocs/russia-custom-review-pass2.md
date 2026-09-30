# RU custom-software review — pass 2 (2026-09-30)

Slice 9 of `devdocs/russia-hunt-plan.md` (custom-review, target RU-custom-pass2).
Method: all 243 RU `software.id: custom` records probed live (parallel GET, browser UA,
12 s cap), bodies+headers clustered by CMS/vendor fingerprints, every candidate verified
against strict signals before re-tagging. Existing software defs used — none created.

## Re-tagged: 41 records (all pass `validate-yaml --id`)

| New tag | Count | Records | Strict signal |
|---|---|---|---|
| bitrix | 14 | baikalgisrubaikalgis, budgetlenoblru, datagov35ru, gisgcrasru, monitoringyanaoru, opendata48ru, opendataadmussuriiskru, opendatavolganetru, speleoatlasru, statmkrfru, wwwadygheyaru, wwwapiportalru, wwwopendata71ru, wwwsaratovgovru | `X-Powered-CMS: Bitrix` header and/or `/bitrix/`, `/local/templates/` asset paths |
| wordpress | 11 | baikalgisrudeltagis, datamartsroskaznaru, fishgovru, geo12rfatlas, meteoruwdcocean, mtseingru, mzkchrru, opendatasamregionru, openurbandataru, verhnekalinovomoru, wwwlevadarurindikatory | `wp-content`/`wp-includes` asset paths |
| drupal | 10 | alaniagovruopendata, geoportalrgoru, giskrasnru, hcvfru, ooptaarinextgisru, opendatarospotrebnadzorru, pskovru, tglru, wwwgobogdanovichru, wwwmintransgovru | `/sites/default/files` + `X-Generator: Drupal` / `Drupal.settings` |
| joomla | 4 | gorodelistaru, kolchadmru, minfinnoblru, wwwlabinskadminru | `content="Joomla!"` generator meta, `/media/jui/` |
| nextgisweb | 2 | arcticgisgcrasru, geologygisgcrasru | `nextgisweb`/`ngw-ol` frontend assets |

Notes on edge cases:
- **ooptaarinextgisru** (`ooptaari.nextgis.ru`) — NextGIS-hosted archive, but the public
  site itself is Drupal (`Drupal.settings`, `/sites/default/files`); tagged drupal.
- **minfinnoblru** — both Joomla generator meta and a stray `/sites/default/files`
  document path (likely a migrated legacy link); generator meta + `/media/jui/` win → joomla.
- **openurbandataru** — WordPress (`wp-content/uploads`); the "modX" match was a random
  base64 cookie, rejected.
- **gisrostovgorodru** — already re-tagged to farvatergisogd in the uncommitted working
  tree (footer «Интернет-Фрегат» confirmed live); no change needed here.

## Confirmed stays custom (documented, no def)

- **NetCat** — wwwadmobninskru (`/netcat_template/template/adm`). 1 instance → watch, no def.
- **MODX** — wwwnesru (`/assets/components/ajaxform`). 1 instance → watch, no def.
  (ekskostromagovru «ЕКС КО» matched only a random `MODx…` base64 blob — rejected.)
- **Tilda landings** — ckt38ru (from pass-1 ISOGD review), mintrudgovru open-data page.
  Website builder, not a data platform; no def.
- **Framework-only builds** — React CRA (5), Vite (4 incl. the unidentified lenobl/novreg
  GISOGD pair, see devdocs/russia-isogd-review.md), Vue (3), Angular (2), Django-cookie
  sites (13). Framework ≠ product; stays custom.
- **WAF artifact** — `hmac-token-name: Ajax-Token` meta + random-hash pre-script is an
  anti-bot injection on many RU gov hosts; never a vendor signal.
- **geo.sakhalin.gov.ru** (geosakhalingovru) — root now serves a styled 404; probable-GSEE
  attribution per docs/discovery-geoportals-viewers.md still requires an in-RU vantage.
  Left custom/active.
- The remaining ~144 NONE-cluster records show no known-platform signal (bespoke SPAs,
  server-rendered gov pages, geo-blocked hosts: 23 connect-fail, 12 mid-body fails).

## False-positive lessons (checked and rejected)

`sensorkrasnru`/`wdcaariru` mention ЕСИМО in prose; `tochnost` cites a Harvard Dataverse
DOI; `acmosru`/`statshhru` matched `/api/v1` (generic); `isogdgorodpermru` uses GeoServer
only as a layer backend behind an Ember portal — none of these justify re-tagging.

Logged: `hunt.py log --kind custom-review --target RU-custom-pass2 --added 0`.
