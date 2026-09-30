# RU ISOGD/GISOGD family — fingerprint review (2026-09-30)

Slice 6 of `devdocs/russia-hunt-plan.md` (municipal-gis, target RU-isogd).
Trigger: Sep 28 pattern review found ~12 ISOGD/GISOGD entries with competing vendors,
mostly geo-blocked; fingerprints unresolved for the `custom` subset.

## Verdict: heterogeneous (as expected — mandated system type, regional procurements).
No new software definition created; two existing defs confirmed on live tenants.

31 RU records matched the family. 20 were already vendor-tagged (14 geometa,
1 farvatergisogd, 1 ingeo, 2 arcgisserver, 1 geocadgsee, 1 sputnikweb).
The 11 `custom` records were probed live on 2026-09-30:

| Record | Host | Fingerprint | Outcome |
|---|---|---|---|
| isogdprimorskyru | isogd.primorsky.ru | Title «Портал ГИСОГД» + noscript "agat doesn't work properly without JavaScript" — matches the Geometa/Agate signal in docs/discovery-geoportals-viewers.md | **custom → geometa** |
| gisogdnsoru | gisogd.nso.ru | `/app/logo/geocad_logo_*.png` icons; guide already lists "Novosibirsk Oblast GISOGD" as a confirmed GSEE tenant — record had never been re-tagged | **custom → geocadgsee** |
| geonngradnnru | geonn.grad-nn.ru | Domain parked at Timeweb («Домен припаркован в Timeweb») — product offline, not geo-blocked | **status: active → inactive**, note added |
| isogd42ru | isogd42.ru | TCP timeout on both HTTPS and HTTP (20 s) — geo-blocked from this vantage | unresolved, stays `custom`/`active` per "geo-blocked ≠ inactive" |
| gisogdlenoblru | gisogd.lenobl.ru | Vite SPA, `/static/logo.png`, `app-body`, `<meta name="end head">`, commented-out vite.svg favicon | `custom` — shared unidentified platform (see below) |
| gisogdnovregru | gisogd.novreg.ru | Byte-identical shell template to gisogd.lenobl.ru (same HTML skeleton, only title/bundle hash differ) | `custom` — same unidentified platform |
| gisogdmosru | gisogd.mos.ru | Bespoke Angular app (`main/polyfills/runtime/scripts` bundles), title «Портал ГИС ОГД» | `custom` — no vendor credit |
| isogdgorodpermru | isogd.gorodperm.ru | Bespoke Ember.js app (`ember-app` bundles) + GeoServer backend for layers + tinymce | `custom` — GeoServer is only the layer service, not the portal |
| geobiysk22ru | geo.biysk22.ru | Bespoke portal loader (`/portal/map/ogd/app.html`, `work/_modules/blocks/splash.js`) | `custom` — unidentified |
| fpdbashkortostanru | fpd.bashkortostan.ru | Angular app behind a WAF (`hmac-token-name: Ajax-Token` meta + tracking pixel are WAF injections, NOT vendor signals — same injection appears on the Geometa tenant) | `custom` — unidentified |
| ckt38ru | ckt38.ru/gisogd | Tilda info page («Центр компетенций», tildacdn assets); no embedded map app | `custom` — Tilda landing, no data platform fingerprint |

## Notes for future hunts

- **WAF injection caution:** `<meta name='hmac-token-name' content='Ajax-Token'/>`,
  random-named `/[a-f0-9]{32}.js?<ts>` pre-scripts and noscript pixel gifs are
  anti-bot/WAF injections seen on multiple RU gov hosts regardless of vendor.
  Never use them as software fingerprints.
- **Unidentified shared platform #1 (2 tenants):** gisogd.lenobl.ru and
  gisogd.novreg.ru run the same Vite SPA (identical HTML skeleton: `/static/logo.png`,
  `class="app-body"`, `<meta name="end head">`, backend `/api/*` with ESIA/VK/FB
  login endpoints). 5.4 MB bundle carries no vendor attribution. If a third tenant or
  a footer credit surfaces, this becomes a software-def candidate.
- geocadgsee guide note confirmed in the field: Sakhalin `geo.sakhalin.gov.ru` still
  needs an in-RU vantage; isogd42.ru (Kemerovo) is geo-blocked, not dead.
- Farvater (ifrigate.ru) tenant enumeration found nothing new beyond the registered
  Sirius tenant; per plan, Farvater/Gems vendor-list sweeps stay with slice 6 follow-ups
  and FOFA `host="gisogd."`/`host="isogd."` patterns are dedupe-blocked until ~Oct 4.

Changes: 2 records re-tagged (isogdprimorskyru → geometa, gisogdnsoru → geocadgsee),
1 record deactivated (geonngradnnru, parked domain). All pass `validate-yaml --id`.
Logged: `hunt.py log --kind municipal-gis --target RU-isogd`.
