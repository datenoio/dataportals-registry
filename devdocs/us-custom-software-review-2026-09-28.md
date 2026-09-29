# US custom-software review — 2026-09-28

## Scope and method

Reviewed the **1,211 US catalog records** with `software.id: custom` in the current
DuckDB export (`data/datasets/datasets.duckdb`, catalogs table). Type shape:

| Catalog type | Records |
|---|---:|
| Scientific data repository | 840 |
| Open data portal | 134 |
| Indicators catalog | 91 |
| Geoportal | 67 |
| Machine learning catalog | 23 |
| Datasets list | 19 |
| API Catalog | 18 |
| Data marketplace | 8 |
| Metadata catalog | 5 |
| Microdata catalog | 3 |
| Data search engine | 2 |
| Other | 1 |

Method, consistent with the September global reviews
(`custom-software-pattern-analysis-2026-09.md`, `custom-scientific-software-review-2026-09-07.md`,
`custom-software-recent-additions-2026-09-16.md`, `custom-software-recent-additions-2026-09-20.md`):
clustered by hostname/registrable domain, URL path segments, description n-grams and
capitalized product tokens, then probed candidate clusters live (page titles, asset
paths, fingerprint files) and checked first-party product documentation against the
733 existing software definitions. US-specific vendor ecosystems (state report-card,
LMI, health-indicator and transparency portals; NCI data commons; IOOS regionals)
received targeted probes because the global sweeps treated US clusters only as
single-operator estates.

## Repeating patterns that stay `custom`

| Pattern | Records | Interpretation |
|---------|--------:|----------------|
| Federal single-operator estates (`nasa.gov` 43, `nih.gov` 36, `noaa.gov` 19, `nist.gov` 18, `usgs.gov` 13, `usda.gov` 11, `cancer.gov` 11) | ~150 | Same organization hosting distinct bespoke systems; no shared product identity (consistent with the 7 Sep scientific review's NCBI/EBI rulings). |
| University/lab estates (`harvard.edu` 14, `umn.edu` 8, `caltech.edu` 8, `umich.edu` 7, `lbl.gov` 7, `ucsd.edu` 6, Broad 4, JAX 4) | ~80 | Same-owner bespoke stacks; hostname reuse is not software evidence. |
| California `data.{city}.gov` municipal portals | 30 | All 30 are **DNS-dead** records retained for coverage tracking ("catalog URL does not resolve in public DNS as of 2026-08", status `inactive`). Cannot be fingerprinted; whatever platform they ran is unverifiable from here. |
| State education report cards (OH, IL, WA, PA, AR ×2, NM, AZ, MD, DE, MS, GA, MT, CO, RI, WV, IN) | ~18 | Live probes show heterogeneous bespoke stacks (Rails, jQuery, Vue/Kendo, ASP.NET). No shared vendor product (no eMetric/Double Line fingerprints). |
| State LMI portals (WisConomy, QualityInfo, PA WorkStats, Hoosiers by the Numbers, laworks.net, labor.maryland.gov) | ~7 | The discovery guide already rules these out for `virtuallmi` without `/vosnet/` fingerprints; no shared stack observed. |
| State health-indicator portals (NM, AZ, LA, PR, MS, GA, MN, KS, MI, PA EDDIE) | ~10 | Live probes show bespoke React/PHP/ASP.NET builds; no IBIS-PH (`ibisph`), Conduent HCI or SparkMap fingerprints. |
| Transit developer/GTFS portals (TriMet, CUMTD, CTA, MTA ×2, Metro LA, BART, 511, AC Transit, Metrolink, MBTA, MARTA, Duluth) | ~13 | Per-agency bespoke developer pages; GTFS is a data spec, not a software product. |
| State transparency/checkbook portals (LA, AR, NV, NM, ME, AZ, WY, MS, GA, MO, NYC, Indiana, SeeThroughNY) | ~13 | Per-state bespoke builds; no shared vendor product visible. |
| Bugwood image network (weedimages, invasive.org, insectimages, ipmimages, forestryimages) | 5 | One University of Georgia platform family, single operator — same ruling as NCBI. |
| NASA EOSDIS DAACs + Earthdata Search/CMR | ~10 | See follow-ups below; CMR is a NASA-operated service, not yet an installable catalog product (matches the 6 Sep follow-up note). |
| ML catalogs (Foundry-ML, PMLB, DrivenData, MLCommons, Epoch AI, Papers with Code, Civitai, DAGsHub, Roboflow, NGC, Keras/TF catalogs, Wolfram NN repo, UCI ×2, GroupLens, AIMI, TCIA, NAIRR) | 23 | Each is its own named single-deployment product; no shared installable platform. |
| Data marketplaces (AWS, Snowflake, Databricks, Google Cloud, Nasdaq Data Link, QuantConnect, CloudQuant, Centific) | 8 | Single-vendor proprietary services, one deployment each. |

## New software candidates

### 1. Bento (`bento`) — strong, 3 records

NCI CBIIT's Bento Framework is a reusable open-source data-commons stack
([CBIIT/bento-frontend](https://github.com/CBIIT/bento-frontend); the repo ships a
`create-bento-app` scaffolder and installation guide for independent deployments).
The canonical runtime fingerprint `public/injectEnv.js` (confirmed in the repo at
`packages/bento-frontend/public/injectEnv.js`, serving `window.injectedEnv`) plus
`/js/session.js` and `/manifest.json` appears, byte-shape identical, on three
independent NCI deployments currently tagged `custom`:

| Record | Live evidence |
|--------|---------------|
| `caninecommonscancergov` — Integrated Canine Data Commons (ICDC) | `/injectEnv.js`, `/js/session.js`, title `ICDC` |
| `clinicalcommonsccdicancergov` — Childhood Cancer Clinical Data Commons (C3DC) | `/injectEnv.js`, `/js/session.js`, title `C3DC` |
| `moleculartargetsccdicancergov` — CCDI Molecular Targets Platform (MTP) | `/injectEnv.js`, `/js/session.js` |

Suggested: `data/software/scientific/bento.yaml`, `subtype: domain_data_infrastructure`,
`has_api: yes` (Bento backend exposes a GraphQL API). `datacatalogccdicancergov`
(CCDC) shares some chrome but lacks the `injectEnv.js` fingerprint in the observed
page — keep `custom` unless confirmed. If created, add the `injectEnv.js` fingerprint
to `discovery-scientific-domain.md` and a GraphQL harvest note to
`harvest-scientific-domain.md`.

### 2. NBIA (`nbia`) — defensible, 2 records (1 retired)

The National Biomedical Imaging Archive is BSD-3-Clause open-source software
([NCIP/national-biomedical-image-archive](https://github.com/NCIP/national-biomedical-image-archive),
[product wiki](https://wiki.nci.nih.gov/display/NBIA)) designed for independent
deployments and federation between instances. Registry records:

| Record | Status |
|--------|--------|
| `wwwcancerimagingarchivenet` — The Cancer Imaging Archive (TCIA) | active; TCIA runs on NBIA (per the NCI wiki, NBIA "is now maintained on GitHub ... with the latest improvements ... for TCIA") |
| `imagingncinihgov` — National Biomedical Imaging Archive (NCIA, `/ncia/login.jsf`) | NCI-hosted instance retired March 2022; data moved to TCIA |

Suggested: `data/software/scientific/nbia.yaml`, `subtype: domain_data_infrastructure`,
metadata support NBIA REST API. The NCIA record should also be reviewed for
`status: deprecated` independently of the software retag.

### 3. VectorSurv (`vectorsurv`) — defensible, 2 records

VectorSurv is the named vector-borne disease surveillance platform operated by UC
Davis and used by many US state/local agencies. Live probe of `westnilecagov`
(California West Nile Virus Surveillance) shows VectorSurv branding,
`VectorSurv-Logo-wt.png`, and a `vectorsurvEmbedded` iframe pointing at
`vectorsurv.org/arbo/`; `vectorsurvorg` is the central system. This mirrors existing
central-service definitions (Kaggle, OpenAlex): one operator, many participating
agencies, two registry records (central + state-branded deployment). If created,
describe it as a hosted central service and add a note that state embeds count only
when the VectorSurv branding is present.

## Follow-up leads (not enough evidence today)

1. **NASA Earthdata Search / CMR** — both are open source
   (`nasa/earthdata-search`, `nasa/Common-Metadata-Repository`) but NASA is the only
   operator; matches the 6 Sep decision to treat CMR as a backend service pending a
   product boundary. Revisit if another operator deploys CMR.
2. **OceansMap (RPS)** — `oceansmapmaracoosorg` is the RPS OceansMap product used by
   IOOS regions; only one frontend record in the registry today
   (`edsdataoceansmapcom` is correctly `thredds`). Vendor multi-tenant evidence would
   make a `managed_saas_service` definition defensible.
3. **Tuva (tuvalabs.com)** — the one tenant record (`hudsonvalleydatatuvalabscom`)
   now redirects to the vendor's own `tuvalabs.com`; effectively a single live
   deployment. The tenant record likely needs a status fix rather than a software id.
4. **Radiant MLHub → Source Cooperative** — `mlhub.earth/datasets` now redirects to
   `source.coop` (Radiant Earth merged MLHub into Source Cooperative). Records
   `mlhubearth` (custom), `betasourcecoop` (custom) and `datasourcetcoop`
   (stacserver) overlap; the Source Cooperative application itself
   ([source-cooperative/source.coop](https://github.com/source-cooperative)) may
   warrant a definition once a second deployment exists. Data-quality action: mark
   `mlhubearth` deprecated/merged.

## Notes for the quality workflow

- 30 inactive California `data.*` records are deliberately unfingerprintable; exclude
  them from any automated custom-software classifier training set.
- The pool's dominant remaining structure is single-operator federal and university
  estates; further US gains should come from evidence-driven hunts (vendor tenant
  lists, FOFA/Censys body fingerprints), not another registry-internal clustering
  round — consistent with the pass-4 conclusion on 16 Sep.

## Applied changes (2026-09-28)

Created three definitions and retagged 7 records:

| Software | Records retagged |
|---|---:|
| `bento` (new) | 3 (`caninecommonscancergov`, `clinicalcommonsccdicancergov`, `moleculartargetsccdicancergov`) |
| `nbia` (new) | 2 (`wwwcancerimagingarchivenet`, `imagingncinihgov`) |
| `vectorsurv` (new) | 2 (`vectorsurvorg`, `westnilecagov`) |

Probe registrations: `BENTO_URLMAP` (`/injectEnv.js`) and `NBIA_URLMAP`
(`/nbia-api/services/v1/getCollectionValues`) added to `DRAFT_CATALOGS_URLMAP` in
`scripts/apidetect_urlmaps_draft.py`; `vectorsurv` registered in `NO_STANDARD_PROBE`
(hosted service, no relative catalog API). Discovery/harvest guide entries added to
`discovery-scientific-domain.md` and `harvest-scientific-domain.md`;
`docs/software-index.md` regenerated.

Validation: `sync-software-maps` (742 ids), `validate-software` gates pass, all 7
changed records pass `validate-yaml --id`, build succeeded (42,387 catalogs / 742
software), test suite 649 passed / 6 failed. All 6 failures reproduce at clean HEAD
or trace to the pre-existing uncommitted working-tree batch (craftcms/wordpress/
redbox mismatches), not to this change; the 7 retagged records produce zero issues
in `dataquality/full_report.jsonl`.
