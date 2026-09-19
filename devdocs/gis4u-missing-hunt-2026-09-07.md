# GIS4U missing-catalog hunt — 7 September 2026

Question: which GIS4U (T-MAPY, `gis4u`) catalogs are missing from the registry?

## Context

- Registry has 152 GIS4U-platform entries: 150 `{muni}.gis4u.cz` + `mapy.bohumin.cz` + `mapy.novybydzov.cz`.
- Taxonomy note: the 150 subdomain tenants are tagged `software: gisplan`; only the 2 city-domain
  entries are tagged `gis4u` (new uncommitted software def `data/software/geo/gis4u.yaml`).
  Retagging the 150 to `gis4u` looks pending.

## Method

1. Enumeration: Wayback CDX `*.gis4u.cz` (387 hosts) + Common Crawl CDX (5 indexes, 80 hosts)
   + `gp.geodata.cz/*` partner redirect stubs (Wayback 70 paths, CC 14) → `{slug}.gis4u.cz`.
   CT logs useless (single wildcard cert `*.gis4u.cz`). Google `inurl:"/mapa/zakladni-aplikace"`
   and `"geoportál GIS4U" -site:gis4u.cz` surfaced no new custom-domain tenants beyond known ones.
2. Diff against all `full.jsonl` link hosts.
3. Verification: targeted GET per candidate host; GIS4U confirmed only on `/theme/square/` theme
   + public `/mapa/` app routes (per software definition).

## Result: 277 verified-live missing municipal tenants

All return HTTP 200 with square theme + public `/mapa/` apps. Software: `gis4u`; catalog_type:
Geoportal; owner: the municipality (or microregion); country CZ.

- https://bechyne.gis4u.cz/
- https://bela-pod-pradedem.gis4u.cz/
- https://bela-u-jevicka.gis4u.cz/
- https://bila-lhota.gis4u.cz/
- https://bilsko-u-horic.gis4u.cz/
- https://biskoupky.gis4u.cz/
- https://blazice.gis4u.cz/
- https://blesno.gis4u.cz/
- https://bobrova.gis4u.cz/
- https://bobruvka.gis4u.cz/
- https://bochor.gis4u.cz/
- https://boleradice.gis4u.cz/
- https://borenovice.gis4u.cz/
- https://boretice.gis4u.cz/
- https://borovnice-trutnov.gis4u.cz/
- https://bouzov.gis4u.cz/
- https://brazec.gis4u.cz/
- https://brezina-brno-venkov.gis4u.cz/
- https://brezina.gis4u.cz/
- https://brezsko.gis4u.cz/
- https://bucina.gis4u.cz/
- https://budislav.gis4u.cz/
- https://bukov.gis4u.cz/
- https://bukovina-nad-labem.gis4u.cz/
- https://bystre-rychnov-nad-kneznou.gis4u.cz/
- https://castolovice.gis4u.cz/
- https://casy.gis4u.cz/
- https://cehovice.gis4u.cz/
- https://ceska-kubice.gis4u.cz/
- https://ceska-rybna.gis4u.cz/
- https://ceske-hermanice.gis4u.cz/
- https://charvaty.gis4u.cz/
- https://chlumetin.gis4u.cz/
- https://chmelik.gis4u.cz/
- https://choltice.gis4u.cz/
- https://chroustovice.gis4u.cz/
- https://chuderov.gis4u.cz/
- https://chvojenec.gis4u.cz/
- https://chyst.gis4u.cz/
- https://cista-svitavy.gis4u.cz/
- https://damnikov.gis4u.cz/
- https://daskabat.gis4u.cz/
- https://dobrenice.gis4u.cz/
- https://dobrochov.gis4u.cz/
- https://dobromerice.gis4u.cz/
- https://dolany-nachod.gis4u.cz/
- https://dolce.gis4u.cz/
- https://dolni-morava.gis4u.cz/
- https://dolni-prim.gis4u.cz/
- https://dolni-vestonice.gis4u.cz/
- https://dolni-zandov.gis4u.cz/
- https://domasov-nad-bystrici.gis4u.cz/
- https://domasov-u-sternberka.gis4u.cz/
- https://drahonin.gis4u.cz/
- https://drinov-kromeriz.gis4u.cz/
- https://dub-nad-moravou.gis4u.cz/
- https://dzbanov.gis4u.cz/
- https://frantiskov-nad-ploucnici.gis4u.cz/
- https://hacky.gis4u.cz/
- https://halenkovice.gis4u.cz/
- https://hejnice-usti-nad-orlici.gis4u.cz/
- https://hermanice-liberec.gis4u.cz/
- https://herspice.gis4u.cz/
- https://hlasna-treban.gis4u.cz/
- https://hlinka.gis4u.cz/
- https://hlohovec.gis4u.cz/
- https://hlusovice.gis4u.cz/
- https://holcovice.gis4u.cz/
- https://hora-svateho-sebestiana.gis4u.cz/
- https://horni-lapac.gis4u.cz/
- https://horni-ujezd-prerov.gis4u.cz/
- https://horni-ujezd-svitavy.gis4u.cz/
- https://hospriz.gis4u.cz/
- https://hradcany-prerov.gis4u.cz/
- https://hradecno.gis4u.cz/
- https://hrivinuv-ujezd.gis4u.cz/
- https://hysly.gis4u.cz/
- https://ivan.gis4u.cz/
- https://jaromerice.gis4u.cz/
- https://jenikovice-pardubice.gis4u.cz/
- https://jenikovice.gis4u.cz/
- https://jenisovice-chrudim.gis4u.cz/
- https://jesenec.gis4u.cz/
- https://jezborice.gis4u.cz/
- https://jezdkovice.gis4u.cz/
- https://jilovice.gis4u.cz/
- https://jimramov.gis4u.cz/
- https://jindrichov-bruntal.gis4u.cz/
- https://josefov.gis4u.cz/
- https://kamenec-u-policky.gis4u.cz/
- https://kamenna-horka.gis4u.cz/
- https://kanovice-zlin.gis4u.cz/
- https://karle.gis4u.cz/
- https://kasnice.gis4u.cz/
- https://knezmost.gis4u.cz/
- https://kobyli.gis4u.cz/
- https://kostany.gis4u.cz/
- https://kostelany.gis4u.cz/
- https://kostelec-u-holesova.gis4u.cz/
- https://kounov-rychnov-nad-kneznou.gis4u.cz/
- https://kralice-na-hane.gis4u.cz/
- https://krasikov.gis4u.cz/
- https://kraslice.gis4u.cz/
- https://kratonohy.gis4u.cz/
- https://krepice.gis4u.cz/
- https://kridla.gis4u.cz/
- https://kruzberk.gis4u.cz/
- https://kunvald.gis4u.cz/
- https://kunzak.gis4u.cz/
- https://kurimska-nova-ves.gis4u.cz/
- https://lesna-tachov.gis4u.cz/
- https://libina.gis4u.cz/
- https://liblin.gis4u.cz/
- https://linhartice.gis4u.cz/
- https://lipoltice.gis4u.cz/
- https://lisov-plzen-jih.gis4u.cz/
- https://litencice.gis4u.cz/
- https://litosice.gis4u.cz/
- https://lobodice.gis4u.cz/
- https://lochousice.gis4u.cz/
- https://lostice.gis4u.cz/
- https://loukov.gis4u.cz/
- https://lozice.gis4u.cz/
- https://lubenice.gis4u.cz/
- https://lucina.gis4u.cz/
- https://lutopecny.gis4u.cz/
- https://luzice-olomouc.gis4u.cz/
- https://male-brezno.gis4u.cz/
- https://malhotice.gis4u.cz/
- https://mas-holicko.gis4u.cz/
- https://melcany.gis4u.cz/
- https://mestecko-trnavka.gis4u.cz/
- https://mesto-albrechtice.gis4u.cz/
- https://milikov-cheb.gis4u.cz/
- https://milotice-nad-becvou.gis4u.cz/
- https://milovice-breclav.gis4u.cz/
- https://mladejovice.gis4u.cz/
- https://mnetes.gis4u.cz/
- https://mokra-horakov.gis4u.cz/
- https://mokrovousy.gis4u.cz/
- https://moravska-nova-ves.gis4u.cz/
- https://morice.gis4u.cz/
- https://mrakotin-chrudim.gis4u.cz/
- https://myslejovice.gis4u.cz/
- https://nasedlovice.gis4u.cz/
- https://nebovidy.gis4u.cz/
- https://nedvezi.gis4u.cz/
- https://nemcice.gis4u.cz/
- https://neslovice.gis4u.cz/
- https://nezdice-na-sumave.gis4u.cz/
- https://niva.gis4u.cz/
- https://nova-ves.gis4u.cz/
- https://nove-sedlo-sokolov.gis4u.cz/
- https://novy-hrozenkov.gis4u.cz/
- https://novy-kramolin.gis4u.cz/
- https://ochoz-u-brna.gis4u.cz/
- https://ohnic.gis4u.cz/
- https://oldris.gis4u.cz/
- https://olomucany.gis4u.cz/
- https://oplocany.gis4u.cz/
- https://osicko.gis4u.cz/
- https://pavlovice-u-prerova.gis4u.cz/
- https://pocenice-tetetice.gis4u.cz/
- https://podivin.gis4u.cz/
- https://podoli-uherske-hradiste.gis4u.cz/
- https://pokrikov.gis4u.cz/
- https://polkovice.gis4u.cz/
- https://pomezi.gis4u.cz/
- https://popovice-uherske-hradiste.gis4u.cz/
- https://pradlo.gis4u.cz/
- https://premyslovice.gis4u.cz/
- https://prestanov.gis4u.cz/
- https://pribice.gis4u.cz/
- https://prilepy.gis4u.cz/
- https://prostejovicky.gis4u.cz/
- https://prusinovice.gis4u.cz/
- https://prusy-boskuvky.gis4u.cz/
- https://radhost-usti-nad-orlici.gis4u.cz/
- https://rajnochovice.gis4u.cz/
- https://rakov.gis4u.cz/
- https://rana.gis4u.cz/
- https://rebesovice.gis4u.cz/
- https://retova.gis4u.cz/
- https://ricky-v-orlickych-horach.gis4u.cz/
- https://rohovladova-bela.gis4u.cz/
- https://ronov-nad-doubravou.gis4u.cz/
- https://rosec.gis4u.cz/
- https://rosice-chrudim.gis4u.cz/
- https://rozdrojovice.gis4u.cz/
- https://rusin.gis4u.cz/
- https://rybitvi.gis4u.cz/
- https://rychnov-na-morave.gis4u.cz/
- https://rymice.gis4u.cz/
- https://sadek.gis4u.cz/
- https://salas.gis4u.cz/
- https://semanin.gis4u.cz/
- https://semin.gis4u.cz/
- https://sindelova.gis4u.cz/
- https://siroky-dul.gis4u.cz/
- https://skripov-prostejov.gis4u.cz/
- https://skuhrov-nad-belou.gis4u.cz/
- https://smidary.gis4u.cz/
- https://soprec.gis4u.cz/
- https://sosnova.gis4u.cz/
- https://srbska-kamenice.gis4u.cz/
- https://stara-ves.gis4u.cz/
- https://stepanov-nad-svratkou.gis4u.cz/
- https://strachotin.gis4u.cz/
- https://strakov.gis4u.cz/
- https://stribrnice-prerov.gis4u.cz/
- https://studlov.gis4u.cz/
- https://svatava.gis4u.cz/
- https://svratouch.gis4u.cz/
- https://tasov.gis4u.cz/
- https://teleci.gis4u.cz/
- https://teplice-nad-becvou.gis4u.cz/
- https://teplice-nad-metuji.gis4u.cz/
- https://tesovice-sokolov.gis4u.cz/
- https://tetov.gis4u.cz/
- https://tisa.gis4u.cz/
- https://tri-studne.gis4u.cz/
- https://troubky-zdislavice.gis4u.cz/
- https://trpin.gis4u.cz/
- https://uhricice.gis4u.cz/
- https://usti.gis4u.cz/
- https://vavrinec.gis4u.cz/
- https://velka-kras.gis4u.cz/
- https://velke-karlovice.gis4u.cz/
- https://velky-orechov.gis4u.cz/
- https://velky-tynec.gis4u.cz/
- https://vendoli.gis4u.cz/
- https://vernerice.gis4u.cz/
- https://verovany.gis4u.cz/
- https://veselicko-prerov.gis4u.cz/
- https://vezky.gis4u.cz/
- https://vilemov-olomouc.gis4u.cz/
- https://vlci-habrina.gis4u.cz/
- https://volec.gis4u.cz/
- https://vracovice-orlov.gis4u.cz/
- https://vranovice-kelcice.gis4u.cz/
- https://vrbatky.gis4u.cz/
- https://vrcen.gis4u.cz/
- https://vsechovice.gis4u.cz/
- https://vseradov.gis4u.cz/
- https://vykleky.gis4u.cz/
- https://vysoka-bruntal.gis4u.cz/
- https://vysoke-popovice.gis4u.cz/
- https://zachlumi.gis4u.cz/
- https://zampach.gis4u.cz/
- https://zaravice.gis4u.cz/
- https://zarecka-lhota.gis4u.cz/
- https://zarici.gis4u.cz/
- https://zerotin.gis4u.cz/
- https://zitenice.gis4u.cz/
- https://zivotice-u-noveho-jicina.gis4u.cz/
- https://blsany.gis4u.cz/
- https://bukova.gis4u.cz/
- https://detrichov.gis4u.cz/
- https://dolni-rychnov.gis4u.cz/
- https://hroznetin.gis4u.cz/
- https://jarov.gis4u.cz/
- https://josefov-sokolov.gis4u.cz/
- https://kocin.gis4u.cz/
- https://krabcice.gis4u.cz/
- https://libavske-udoli.gis4u.cz/
- https://lipova-cheb.gis4u.cz/
- https://loveckovice.gis4u.cz/
- https://mala-velen.gis4u.cz/
- https://mecholupy.gis4u.cz/
- https://mladejov.gis4u.cz/
- https://pliskov.gis4u.cz/
- https://rana-louny.gis4u.cz/
- https://stara-voda.gis4u.cz/
- https://svrkyne.gis4u.cz/
- https://valkerice.gis4u.cz/
- https://velka-hledsebe.gis4u.cz/
- https://vochov.gis4u.cz/

### Platform-confirmed but app list appears login-gated (review before adding)

- https://dlouha-trebova.gis4u.cz/ (square theme + tmapy credit; app cards JS/login-gated)

### Tenant exists (DNS+TLS, HTTP 500 app error) — add as inactive or skip

- https://babice-olomouc.gis4u.cz/
- https://bustehrad.gis4u.cz/
- https://ceska-kamenice.gis4u.cz/
- https://doupovske-hradiste.gis4u.cz/
- https://otvovice.gis4u.cz/
- https://podoli-u-brna.gis4u.cz/
- https://stare-misto.gis4u.cz/
- https://stare-sedlo.gis4u.cz/
- https://tvarozna.gis4u.cz/
- https://dehtare.gis4u.cz/
- https://golf-tepla.gis4u.cz/
- https://jarov-plzen-sever.gis4u.cz/
- https://libochovany.gis4u.cz/
- https://lobendava.gis4u.cz/
- https://merklin-prestice.gis4u.cz/

Aliases/artifacts to ignore: `po-povice-uherske-hradiste`, `povice-uherske-hradiste` (= popovice-uherske-hradiste),
`rajecjestrebi` (= registered rajec-jestrebi), `gp.geodata.cz/{slug}/` redirect stubs, `robots.txt.gis4u.cz`.

### Vendor specials (maintainer decision)

- https://cr.gis4u.cz/ — T-MAPY national portal (election maps), public apps, GIS4U platform.
- https://demo-server.gis4u.cz/ — vendor demo shell; skip.

### Possible same-village duplicate pairs (check identity before adding both)

- jenikovice.gis4u.cz vs jenikovice-pardubice.gis4u.cz (identical title "Obec Jeníkovice")
- brezina.gis4u.cz vs brezina-brno-venkov.gis4u.cz
- Disambiguated pairs that are genuinely different villages: rana vs rana-louny,
  horni-ujezd-prerov vs horni-ujezd-svitavy, mladejov vs mladejov-na-morave (registered).

## Coverage caveats

- Vendor claims 1,200+ customers across all T-MAPY products; not all have public GIS4U web portals.
- Wayback/CC only see linked/visited hosts; more live tenants likely exist but need another referral
  source (e.g., municipal-site links "geoportál GIS4U", the Zlatý erb awards list) to enumerate.

---

## Outcome (2026-09-08): all missing tenants added

Added **276 new GIS4U entity records** (`data/entities/CZ/{kraj}/geo/{id}gis4ucz.yaml`), one per verified-live
municipal portal. The 277th (`mladejov.gis4u.cz`) was a duplicate of an existing HEAD record and was not re-added.

- **Kraj resolution:** each municipality mapped to its kraj (NUTS3 code) via Czech Wikipedia extracts (batched
  `action=query&prop=extracts`, redirect-following, disambiguation by `(okres …)` title and by slug hint). 255/277
  resolved automatically; 9 hand-mapped after checking extracts (Bucina CZ-53, Kraslice/Josefov/MAS Holicko CZ-41,
  Salas CZ-72, Usti CZ-53, Siroky Dul CZ-53, Nova Ves CZ-32, Osicko CZ-72). The two `mladejov` hosts are distinct
  villages (CZ-52 Královéhradecký existing; the CZ-71 one is `mladejovice`).
- **Owner type:** `Město`/`Městys`/`Obec` prefix from the Wikipedia first-sentence status (17 město, 15 městys,
  243 obec, 2 microregion MAS Holicko + Osicko). `owner.link` set to the municipal website when the portal footer
  exposed one (vendor/partner domains filtered out).
- **Software tag:** kept `software.id: gisplan` to match the sibling entries and the current build; the new
  `gis4u` software definition remains uncommitted, so a future retag of all `*.gis4u.cz` tenants is still pending.
- **UIDs:** assigned `cdi100002463`–`cdi100002738`.
- **Restore:** the working tree had 66 of the 67 previously-registered gis4u.cz entries deleted (uncommitted) even
  though those tenants are still live; restored all 67 from HEAD to avoid data loss.
- **Verification:** `validate-yaml` — all 34,293 files valid except 13 pre-existing unrelated SeaSketch owner-schema
  errors (not from this change). `build` → catalogs 34,293 rows, 343 `*.gis4u.cz` hosts (276 new + 67 restored),
  full/parquet/duckdb regenerated. `pytest` → 295 passed; the 2 `test_quality_regression` failures are pre-existing
  baseline drift (562 IMPORTANT issues from unrelated working-tree churn vs a stale 0 baseline; 0 involve gis4u).

Coverage caveat: still not exhaustive — more live tenants likely exist behind hostnames not yet linked anywhere
(vendor claims 1,200+ customers). Next enumeration pass should mine municipal-site "geoportál GIS4U" backlinks and
the Zlatý erb award lists.
