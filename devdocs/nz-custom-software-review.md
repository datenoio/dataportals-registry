# New Zealand `custom`-software review (2026-09-28)

Review of the 22 NZ entries carrying `software.id: custom` (out of 274 NZ entries), with
live probing of each site to find repeating patterns and candidates for new software
definitions. Method: `requests` fetch of each `link`, fingerprinting headers
(`Server`, `X-Powered-By`, meta generator), body keywords, and API endpoints.

## NZ software landscape (for context)

Top platforms: ArcGIS Server (65), ArcGIS Hub (58), LocalMaps (17), Koordinates (15),
Figshare (11), IntraMaps (9), DSpace (8), GBIF IPT (7), GeoNode (7), GeoNetwork (6),
CKAN (5). NZ local-government geoportals are dominated by Esri stacks plus two NZ
vendors already in the taxonomy (LocalMaps, Koordinates) — nothing new to define there.

## Findings per custom entry

### Bespoke one-offs — keep `custom` (17)

| Entry | Probe evidence |
|---|---|
| `infosharestatsgovtnz`, `ariastatsgovtnz`, `portalapisstatsgovtnz` | Stats NZ suite: ASP.NET WebForms / IIS / Cloudflare front — bespoke, single-org |
| `wwwrbnzgovtnz` | RBNZ statistics pages, Cloudflare — bespoke |
| `wwwemieagovtnz` | Electricity Authority EMI, bespoke |
| `figurenz` | Figure NZ Trust React/nginx civic-stats platform — bespoke charity product, one instance |
| `dataniwaconz` | NIWA DataHub, React SPA on Vercel — bespoke |
| `geonetorgnz` | GeoNet data pages — bespoke |
| `nvslandcareresearchconz`, `biotanzlandcareresearchconz` | Manaaki Whenua databanks — bespoke |
| `wwwepagovtnz` (CCID) | EPA database search — bespoke |
| `phrcautacnz` | AUT Pacific Islands Families study page — one-off |
| `wwwmathaucklandacnz` | Polytopes atlas — one-off academic page |
| `openifcmodelcsaucklandacnz` | Rails/Phusion Passenger one-off |
| `datasetscmswaikatoacnz` | Static hand-written HTML list of Waikato datasets — one-off |
| `devportalatgovtnz`, `apidevelopersmetroinfoconz` | Hand-built GTFS developer portals, no framework fingerprints |
| `opendatametlinkorgnz` | Vue SPA on Amazon S3 + AWS API Gateway SDK (`/apigateway-js-sdk/`) — bespoke |
| `dataecangovtnz` | ECan Open Data Portal: ASP.NET (Azure App Gateway affinity cookies `ASLBSA`) front page pointing at ArcGIS Server services — bespoke composite |

### Watch item — `datanapiergovtnz` (Napier City Council Data Downloads)

- Front page is a custom "Data Downloads" app served by Apache with the distinctive
  header `X-Powered-By: Powered by Local Government`.
- Backend is GeoServer (Jetty; `/geo/ows` WFS GetCapabilities, full GeoServer output
  format list: shape-zip, geopkg, dxf, excel).
- The header looks like a deliberate product/vendor signature, and the pattern
  (council-branded open-data download front over GeoServer) could repeat across NZ
  councils. Probed `data.hastingsdc.govt.nz`, `opendata.dunedin.govt.nz`,
  `data.pncc.govt.nz`, `data.wcc.govt.nz` — none resolved, so no second instance
  confirmed from here.
- Action: keep `custom` for now; run a FOFA/Censys hunt `header="Powered by Local
  Government"` (+ `title="Data Downloads"`, country=NZ) before defining a product.

## Candidates for new software definitions

### 1. PMR2 — Physiome Model Repository 2 (`models.physiomeproject.org`) — strong candidate

- Named, installable open-source product (tri-licensed GPL/LGPL/MPL; Plone CMS + Git
  DVCS). Code: https://github.com/PMR2 ; docs/install: cellml.org/tools/pmr ; tracker:
  tracker.physiomeproject.org.
- Multiple independent instances: official instance `models.physiomeproject.org`
  (registry entry `modelsphysiomeprojectorg`), the CellML Model Repository
  `models.cellml.org` (live, PMR2-based), and the documented teaching instance
  `teaching.physiomeproject.org` (currently 503, mirrors main).
- Reference: Yu et al. 2011, Bioinformatics 27(5):743, doi:10.1093/bioinformatics/btq723.
- Proposed record: `data/software/scientific/pmr2.yaml` — `category: Scientific`,
  `subtype: scientific_repository_platform` (or `domain_data_infrastructure`,
  CellML/FieldML modelling domain), `has_api: true` (web services + Git),
  `repository_url: https://github.com/PMR2`.
- Discovery guide: add `## Physiome Model Repository 2 (pmr2) {#pmr2}` to
  `docs/discovery-scientific.md` + harvest recipe (`docs/harvest-scientific.md`);
  generator signature: Plone (`<meta name="generator" content="Plone...">`) plus
  `/cellml_models`, `/pmr2_search`, workspace/exposure URL patterns
  (`/e/`, `/w/` paths, `@@generate_view`).

### 2. enviPath (`envipath.org`) — borderline candidate

- Genuine reusable product: biotransformation pathway database + prediction system,
  REST API, RDF store; successor of EAWAG-BBD/UM-BBD (Wicker et al. 2016,
  NAR 44(D1):D502). Now maintained by the enviPath spin-off (envipath.org/community,
  LinkedIn NZ presence), with a 2026 platform redesign and commercial bespoke
  deployments via the company.
- Only one public installation exists (envipath.org), and the registry row's owner is
  the product itself. Per `docs/software-taxonomy.md` the "first-party product page /
  vendor" rule can apply, but unlike the 2026-09-07 viewer examples there is no
  deployment list to hunt from.
- Verdict: definable as `envipath` (`category: Scientific`,
  `subtype: domain_data_infrastructure`, `has_api: true`, REST + planned SPARQL), but
  low discovery value — hold until a second installation or a vendor deployment list
  appears.

### Not candidates

- Stats NZ suite, Figure.NZ, NIWA DataHub, GeoNet, EMI, RBNZ, Manaaki Whenua sites:
  single-instance bespoke systems → stay `custom`.
- Auckland Transport / Metlink / Metroinfo developer portals: bespoke GTFS/API portals,
  no shared named product.

## Suggested next steps

1. ~~Add the `pmr2` software definition~~ **Done 2026-09-28**: `data/software/scientific/pmr2.yaml`
   (subtype `domain_data_infrastructure`, version 0.14.1), catalog entry
   `modelsphysiomeprojectorg` switched from `custom` to `pmr2`, discovery/harvest
   sections added to `docs/discovery-scientific-domain.md` /
   `docs/harvest-scientific-domain.md`, `sync-software-maps` + `validate-software` +
   `build` + `docs_software_coverage.py` all green.
   **`models.cellml.org` added as a second PMR2 row 2026-09-29**
   (`data/entities/NZ/NZ-AUK/scientific/modelscellmlorg.yaml`, uid `cdi00010077`,
   status active, owner Auckland Bioengineering Institute). The teaching mirror
   `teaching.physiomeproject.org` was left out — it returned 503 during review and
   mirrors the main repository rather than holding distinct content.
2. Run a hunt for `header="Powered by Local Government"` (FOFA/Censys, NZ-focused) to
   test whether the Napier stack is a shared NZ council product; define it only if ≥2
   independent installs surface.
3. Leave enviPath as `custom` pending evidence of reuse.
