# RU «Инвестиционная карта» family — fingerprint review (2026-09-30)

Slice 7 of `devdocs/russia-hunt-plan.md` (custom-review, target RU-investmap).
Trigger: Sep 28 pattern review found ~8 records sharing the title «Инвестиционная
карта <региона>» with conflicting fingerprints (one tagged Bitrix).

## Verdict: heterogeneous — no single vendor/standard. Closed without a new software definition.

Identical titles are a naming convention (every region calls its map «Инвестиционная
карта»), not a shared platform. Four distinct vendors plus four bespoke builds:

| Record | Host | Fingerprint (2026-09-30, live probe) | Tag after review |
|---|---|---|---|
| investmap49govru | investmap.49gov.ru | `/bitrix/`, `/local/` in HTML | bitrix (unchanged) |
| wwwinvest32rumap | invest32.ru/map | `/local/templates/invest/favicon.ico` — Bitrix template path; map itself is a Vite SPA module | **custom → bitrix** |
| investmapamuroblru | investmap.amurobl.ru | `X-Powered-CMS: Bitrix Site Manager`, `P3P: /bitrix/p3p.xml` (HTTPS cert expired; site answers 200) | **custom → bitrix** |
| mapinvestugraru | map.investugra.ru | `/orbismap/extern/oms/themes/investugra/` asset paths | orbismap (unchanged) |
| investmapeaoru | investmap.eao.ru | `cdn.orbismap.ru/plugins/omjs.pkk.v2.js`, omjs 2.8 client | orbismap (unchanged) |
| maplenoblinvestru | map.lenoblinvest.ru | ORBISMap app (orbis-logo SVG, orbisystems.ru credit, `/orbismap/static/`) served inside a Bitrix CMS shell (`X-Powered-CMS`) | orbismap (unchanged — map platform, not the CMS wrapper) |
| investmapinfo | investmap.info | Landing page is Tilda (tildacdn), but the actual map app at `map.investmap.info` runs omjs 2.8 (ORBISMap client) | orbismap (unchanged) |
| admininvmaptatarstanru | admininvmap.tatarstan.ru | NextGIS Web API endpoints recorded in entry | nextgisweb (unchanged) |
| investmapapieconomygovru | investmapapi.economy.gov.ru | GeoServer OGC endpoints recorded in entry | geoserver (unchanged) |
| investmaptatarstanru | investmap.tatarstan.ru | Bespoke React SPA (create-react-app: `/static/js/main.*.js`, `id="root"`), no vendor credit | custom (unchanged) |
| investmapnashsever51ru | investmap.nashsever51.ru | Bespoke jQuery/Backbone/OpenLayers app (`/public/investmap/`); footer «Создано компанией ifrigate.ru» (Internet-Frigate) | custom (unchanged) |
| mapinvestivanovoru | map.invest-ivanovo.ru | Bespoke Vite SPA (`/assets/index.*.js`) + Yandex Maps JS API | custom (unchanged) |
| zabinvestportalru | zab-investportal.ru/ru/invest-map | Bespoke Django (django_language cookie, Phusion Passenger) with hand-written `/static/core/map.js` + data files | custom (unchanged) |

## Notes

- Bitrix def (`data/software/opendata/bitrix.yaml`) and ORBISMap def
  (`data/software/geo/orbismap.yaml`) already exist — nothing to create.
- ORBISMap tenant fingerprint for future hunts: `omjs/2.8/omjs.js`,
  `cdn.orbismap.ru`, `/orbismap/extern/oms/` or `/orbismap/static/` paths,
  orbisystems.ru footer credit.
- Bitrix fingerprint: `X-Powered-CMS: Bitrix Site Manager` header, `/local/templates/`
  or `/bitrix/` asset paths, `P3P: /bitrix/p3p.xml`.
- investmap.amurobl.ru HTTPS certificate is expired (2026-09-30); HTTP 301 → HTTPS.
  Site loads with expired cert — left `status: active`.
- Internet-Frigate (ifrigate.ru) builds bespoke regional portals; do not create a
  software def from a single instance.

Changes: 2 records re-tagged (`wwwinvest32rumap`, `investmapamuroblru`), both pass
`validate-yaml --id`. Logged: `hunt.py log --kind custom-review --target RU-investmap`.
