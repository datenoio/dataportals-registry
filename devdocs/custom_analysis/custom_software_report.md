# Custom-software catalog review — repeating patterns and candidate software definitions

Date: 2026-09-28
Scope: all active `data/entities` catalogs with `software.id: custom` (6,471 of 6,597 total; 109 inactive / 17 deprecated excluded).
Source: `data/datasets/datasets.duckdb` (catalogs table), export at `devdocs/custom_analysis/custom_catalogs.json`.

## Method

Five independent pattern detectors were run over the 6,471 active records:

1. URL first-path-segment frequency across distinct hosts — only generic words (`data`, `opendata`, `portal`, …), no product fingerprints.
2. Full URL token frequency across distinct hosts (≥3 hosts, ≥4 chars) — 144 tokens, all generic vocabulary; no hidden platform signature.
3. Description mining for "powered by / built with / based on" — no platform mentions (descriptions describe the data, not the stack).
4. Shared registrable-domain clustering (vendor-hosted SaaS detection) — no vendor multi-tenant hosting found; every multi-entry domain is institutional (nasa.gov 43, nih.gov 33, europa.eu 23, gc.ca 21, wto.org 18, ebi.ac.uk 18 …).
5. Subdomain-label repetition across distinct parent domains + name bigram clustering — this is where the real patterns are.

Additional checks: hostnames containing existing software names (no material misclassification; `massbank`, `sciencedb` hits are correct same-brand instances), endpoint types (generic REST/sitemap/OGC, no vendor signal), tags.

Conclusion of detectors 1–4: the `custom` bucket is genuinely dominated by bespoke portals. Repeating patterns exist only at the **national template / national programme** level, where one government platform is instantiated per ministry, province, or municipality under a standardized subdomain scheme. This matches the existing registry convention of national-platform software definitions (`ogdindia`, `datagovmy`, `twgovopendata`, `tggovopendata`-style entries).

## Candidate new software definitions

### 1. Satu Data Indonesia — STRONG (52 instances)

- Pattern: `satudata.{regency/city/ministry}.go.id`, names "Satu Data Kabupaten/Kota/Kementerian X".
- Count: 46 by subdomain + 6 more by name = **52 active Open data portals** (ID has 105 custom entries total; this is half).
- Context: Indonesia's national "Satu Data Indonesia" (One Data) programme; regional and ministerial nodes share the mandated `satudata.` subdomain scheme and a common portal template.
- Suggested id: `satudata`. Type: Software, category: open data portal platform (national programme template).
- Discovery fingerprint: hostname starts with `satudata.` and ends `.go.id`.

### 2. Turkish municipal open data portal "Açık Veri" — MEDIUM (10 instances)

- Pattern: `acikveri.{municipality}.bel.tr` (Ankara variant: `seffaf.ankara.bel.tr`).
- Count: 10 active Open data portals.
- Caveat: needs verification that the portals share one vendor build rather than just a naming convention; a spot check of 2–3 sites (e.g. acikveri.kayseri.bel.tr, acikveri.manisa.bel.tr) for identical page structure/assets would confirm.
- Suggested id: `acikveri` (name: "Açık Veri Portalı").

### 3. Kent Rehberi (Turkish municipal city-guide geoportal) — MEDIUM (8 instances)

- Pattern: `kentrehberi.{municipality}.bel.tr` subdomains (5) + names "Kent Rehberi" (8 total incl. `kbs.yalova-kadikoy.bel.tr/?sistem=kent_rehberi`).
- Type: Geoportal. Standardized municipal "city guide" map product.
- Suggested id: `kentrehberi`. Same vendor-verification caveat as #2.

### 4. Korean municipal "Living Map" / smart map — MEDIUM-WEAK (7+ instances)

- Pattern: names "… Living Map (Service)" across `*.go.kr` municipal sites (Yesan, Seocheon, Gijang, Gangneung, Yangsan, Yeosu, Yangpyeong).
- KR has 145 custom entries, 39 of them geoportals; the living-map product family is the only visibly repeating one, but Korean local-gov GIS is split across several vendors (jmap, gxo already exist). Treat as one product family only after checking 2–3 sites.

### 5. Paraguay agency open data template (`datos.*.gov.py`) — WEAK (8 instances)

- 8 agencies under `datos.{agency}.gov.py`. Common subdomain convention from the national open data decree; underlying stack not verified as one product.

### 6. Spain agency open data via Sede Electrónica (`sede.*.gob.es`) — WEAK (8 instances)

- 8 entries; these are pages inside each agency's shared e-administration site template rather than a data-catalog product per se.

## Explicit non-candidates (checked and rejected)

- **Vendor SaaS hosting**: none — no shared commercial base domain hosts multiple custom entries.
- **WTO (18), expasy.org (12), re.kr (14), nasa.gov (43), nih.gov (33)**: many entries per domain but each is a distinct bespoke database, not instances of one product.
- **`ide.*.gob.ar`, `visor.*`, `geoportal.*.pl`, `opendata.*.sk`, `gis.*.pr.gov`, `datosabiertos.*.gob.pe`**: 2–4 instances each and/or heterogeneous stacks.
- **DE (420), US (1,204), CN (312) custom entries**: heterogeneous; no repeating product fingerprint in subdomain, path, or name dimensions.
- **Misclassification sweep**: no active custom entry's hostname indicates an already-defined software (checked all 753 existing software ids against hostnames).

## Suggested next steps

1. Create software definition `satudata` (52 instances — by far the largest win), re-assign entries, run `sync-software-maps` + `validate-software` + `build`.
2. Spot-verify `acikveri` and `kentrehberi` vendor identity, then create those two definitions (18 instances combined).
3. Optionally hunt new instances of the same templates (`satudata.*.go.id` coverage looks far from complete vs. Indonesia's 500+ regencies/cities).
