# Custom open-data software review — 2026-09-07

## Scope and method

Reviewed the **1,157 verified-entity records** with `catalog_type: Open data portal`
and `software.id: custom`. The initial `catalogs.jsonl` export had 33,579 records;
a source-YAML check independently confirmed the 1,157-record subset. It covers 105
country/territory/group codes: 1,098 active, 56 inactive, and three deprecated records.
Scheduled catalogs and other catalog types are outside this review.

The largest groups are China (155), United States (147), Spain (124), Indonesia (81),
Russia (73), World (60), South Korea (39), Italy (36), United Kingdom (31), and France (29).

This is a complete **local metadata pattern review**, followed by a targeted live review
of promising examples, not a live crawl of all 1,157 portals. Grouping considered hostnames,
URL path prefixes, descriptions, and endpoint types. Product candidates were compared with
all existing software definitions, including aliases in their descriptions. First-party
product documentation and targeted HTTPS GETs supplied confirmation. Failed requests were
not interpreted as evidence that a catalog uses particular software.

The companion `custom-opendata-software-review-2026-09-07.json` retains the initial cohort
IDs, source paths, links, country and status counts, candidate memberships, decisions,
and evidence URLs. Existing unrelated workspace changes were preserved. These edits are
reference-data additions and corrections under the existing schema, not a new runtime
capability or a schema change.

## First-pass results

The second pass below supersedes the unresolved UK candidate decisions and remaining count.

| Product / pattern | Initial custom records | Decision |
|---|---:|---|
| GIS Open Data Portal, deployed on TwinMap | 2 | Created `gisopendataportal`; reclassified both records |
| Esri UK Data Observatory / InstantAtlas Data Observatory | 3 strong candidates | Created `esridataobservatory` from documented independent deployments; left these candidates unchanged pending product-specific confirmation |
| SHIRASAGI open-data sample | 1 | Reused existing `ouropendata`; no duplicate SHIRASAGI definition |
| Chinese `/extranet/openportal/` application | 3 | Retained `custom`; canonical product identity remains unresolved |
| Chinese `/open-data-web/` application | 2 | Retained `custom`; shared route needs vendor/source verification |
| `/wps/portal/` routes | 3 | Retained `custom`; framework-level clue only |
| `/Paginas/` or `/paginas/` routes | 7 | Retained `custom`; weak CMS clue, not a verified catalog platform |
| Conflicting CKAN/Socrata/Opendatasoft endpoint families | 9 | Retained `custom`; validate response bodies before classification |

After the three software corrections, **1,154** records in this cohort remain `custom`.
The Esri definition deliberately has no records reassigned in this change: proof that a
shared product exists is stronger than proof of its use by each local candidate.

### GIS Open Data Portal (`gisopendataportal`)

Records: `tvrdosintwinmapai`, `novemestotwinmapai`.

Both the [Tvrdošín developer page](https://tvrdosin.twinmap.ai/developer) and
[Nové Mesto developer page](https://nove-mesto.twinmap.ai/developer) identify the same
`gis-open-data-portal/od-portal` project. Each documents the same REST feature route,
GraphQL route, CSV distributions, and DCAT-AP-SK catalog. Their municipal frontends share
the dataset/map/developer structure. Attribution to a shared project plus an identical API
contract is stronger evidence than the common hosting domain or Next.js assets alone.

Live checks returned HTTP 200 with JSON catalog bodies from:

- <https://tvrdosin.twinmap.ai/api/opendata/set/catalog/lkod> — 12 dataset references.
- <https://nove-mesto.twinmap.ai/api/opendata/set/catalog/lkod> — 13 dataset references.
- <https://tvrdosin.twinmap.ai/api/open-api/features?limit=1&page=1> — feature JSON.

The definition uses the source-project identity rather than assuming “TwinMap” is the
canonical catalog product name. The [advertised repository](https://gitlab.com/gis-open-data-portal/od-portal)
redirected to sign-in and its project API returned 404. Thus source availability, vendor,
and license are unverified; no open-source license is asserted.

An upstream quality issue is worth preserving in the harvest guidance: Tvrdošín's catalog
title and description name Nové Mesto, while its contact and dataset links name Tvrdošín.
Do not copy that title into registry ownership or merge the two municipal records.

### Esri UK Data Observatory (`esridataobservatory`)

Candidates: `dataoxfordshiregovuk`, `datakingstongovuk`, `dataealinggovuk`.

Their local descriptions attribute development to Esri UK, and web-accessible pages share
Quick Ward Profile, topic reports, and (for Oxfordshire/Ealing) Data Explorer and Custom
Area Reporter. This is a strong candidate cluster, but those modules can also be embedded
in independently built websites. Direct HTTP requests returned 403, preventing raw theme
and application-configuration verification. The records therefore retain `custom`.

The product itself meets the shared-platform requirement:

- The [Esri product page](https://www.esriuk.com/en-gb/arcgis/products/instantatlas/products/data-observatory)
  describes the managed WordPress/ArcGIS service and identifies Suffolk.
- The [Hounslow customer case study](https://resource.esriuk.com/esri-resources/london-borough-of-hounslow/)
  explicitly attributes its managed hub to InstantAtlas Data Observatory.
- The [vendor documentation](https://help.instantatlas.com/category/data-observatory/)
  confirms the branding transition, a shared WordPress theme, and Data Explorer embedding.

Use a single `esridataobservatory` ID for the current and former brand. The public guides
now explain its fingerprints and how to resolve dataset sources from published application
configuration. No universal standalone API endpoint is assumed. Hounslow's existing CKAN
classification is a separate review candidate, outside this custom-only edit set.

### SHIRASAGI: existing definition, not a new product

`data/software/opendata/ouropendata.yaml` already explicitly represents SHIRASAGI's
open-data catalog UI, with seven assigned records before this change. The upstream
[deployment list](https://www.ss-proj.org/case/) and
[Kagawa case study](https://www.ss-proj.org/case/583.html) corroborate independent use.

The sample at <https://opendata.demo.ss-proj.org> serves the expected CMS assets,
data/application/idea sections, and a JSON response at `/api/package_list`. Reclassified
`opendatademossprojorg` to `ouropendata`. Its existing inactive/demo status and other fields
were preserved; API metadata may be enriched separately. This is one demo correction,
not a newly discovered production deployment.

The other two Japanese hosts checked were not reassigned. Ibaraki serves a different
`skin/common/js/` asset family without confirmed SHIRASAGI attribution. Hirosaki's hostname
returns a JavaScript redirect to `/lander`, which is not usable platform evidence.

## Remaining patterns and priorities

1. **Chinese application families.** Zhangjiakou, Tongliao, and Yichun share
   `/extranet/openportal/`; Bozhou and Hefei share `/open-data-web/index/` and `.do` pages.
   The earlier general custom-software review associated the former with a Huawei solution
   guide, but did not establish a canonical reusable catalog product. This review does not
   upgrade that earlier hypothesis to a confirmed vendor attribution. Inspect live bundle
   banners, copyright owners, and dataset-list API contracts next.
2. **Indonesia's 81 custom records.** Satu Data branding and national harvest-source
   descriptions provide useful grouping, but identify an initiative, not an implementation.
   Compare actual APIs and application assets before creating a generic “Satu Data” ID.
3. **CMS routes.** `/wps/portal/`, `/Paginas/`, and the single `/opencms/` route are framework
   clues. Generic framework software can be represented under the taxonomy, but these
   routes alone do not justify creating or assigning a product definition.
4. **Endpoint false positives.** Nine records carry two or more of the CKAN, Socrata, and
   Opendatasoft endpoint families. Their exact IDs are in the companion JSON. Treat these
   as an endpoint-cleanup queue; status codes and endpoint labels alone are insufficient.
5. **Generic URL patterns.** The leading nonempty first-two-segment groups are `opendata`
   (26), `data` (20), `datasets` (12), and `dataset` (9). None is a software fingerprint.

## Validation

- Both new software definitions pass Cerberus schema validation; no software-profile issues.
- All three edited catalogs pass `builder.py validate-yaml --file`.
- A comparison with the pre-edit cohort verifies exactly three changed records and only
  their `software` fields changed.
- `docs_software_coverage.py` regenerated the software index successfully.
- `builder.py build` succeeded. The rebuilt exports contain 33,620 catalogs and 406 software
  records, with both new definitions and all three corrections verified in JSONL. The
  broader catalog-count increase reflects pre-existing source additions in the workspace;
  this review added no catalogs. There are 1,154 custom open-data records in the export.
- `python -m pytest --no-cov -q`: **314 passed, one failed**. The failure is the existing
  `test_llms_txt_static_copies_match_root` mismatch between root and website static copies;
  neither file was edited in this review.
- The full `validate-software` gate still fails on the unrelated existing STAC Browser
  value `rights_management.licensing_type: Varies`, version coverage 13.8% versus a 25%
  minimum, and repository-URL coverage 43.1% versus a 55% minimum. These coverage gaps
  already exist independently of the two additions. All referenced software IDs resolve.
- Scoped whitespace checks pass. No changes were committed.


## Second pass — confirmed installations and broader sampling

Four additional software corrections bring the cumulative result to **seven reclassified
records**, leaving **1,150** custom open-data portals. No additional software definitions
were necessary in this pass.

### UK cluster resolved

Oxfordshire, Kingston, and Ealing now have directly observed product evidence. Their
rendered homepages explicitly credit Esri UK and load the same WordPress theme directory
`/wp-content/themes/ia-theme/`, including `ia-reports-embedded-style.css`, `ia-map.js`,
`ia-quickprofile.js`, and `ia-stat.js`. Browser inspection succeeded for all three;
Oxfordshire also returned full HTML to a direct GET in this pass. Kingston's footer links
to Esri's InstantAtlas product family. Together, these signals identify the shared
Data Observatory application rather than merely an embedded ArcGIS map.

Reclassified `dataoxfordshiregovuk`, `datakingstongovuk`, and `dataealinggovuk` to
`esridataobservatory`. The discovery guide now includes the stronger theme fingerprint.

Evidence: [Oxfordshire](https://data.oxfordshire.gov.uk/),
[Kingston](https://data.kingston.gov.uk/), [Ealing](https://data.ealing.gov.uk/).

### Indonesia: 81 targeted homepage checks

Requested each of the 81 registered custom open-data URLs once, using certificate
verification and bounded timeouts. Results: **55 HTTP 200, 16 HTTP 403, one HTTP 500,
and nine connection errors**. HTTP 200 is not a liveness or classification verdict: some
responses are application shells, a parked domain, or unreadable content. No catalog
status changes were inferred from this sample.

`databengkuluprovgoid` is confirmed CKAN: the homepage declares `ckan 2.9.11`, loads
CKAN core JavaScript and CKAN extension styles for scheming, harvest, and geoview.
Reclassified it to existing `ckan`. The status API returns an explicit 403 authorization
error, so API-access fields were preserved rather than claiming anonymous API access.
Evidence: [Bengkulu portal](https://data.bengkuluprov.go.id/).

Remaining similarities do not establish a reusable catalog product. Examples include
Next.js polyfills shared by Pekanbaru/Makassar/Sulawesi Utara, a Next.js chunk shared by
Bogor/Konawe Selatan, generic `assets/js/main.js`, Livewire assets, and the Kint debugger
embedded in Pangkep/Takalar. A Laravel Starter generator on Badan Pangan identifies an
application scaffold rather than a demonstrated shared open-data application. Semarang
links to a separate `/ckan` catalog, which does not establish the homepage's software.
These are follow-up clues; no generic “Satu Data” definition or bulk classification was made.

### Chinese families: stronger lead, no assignment

- Bozhou's recorded application returned a WAF 405 page; Hefei failed DNS resolution.
- Zhangjiakou and Yichun timed out. No new platform conclusions follow from those failures.
- Tongliao's HTML loads `../../js/boot/boot.min.js`; that file sets
  `basePath: /extranet/openportal`, uses `ResBoot`, and contains an Epoint development
  mock-service URL (`fe.epoint.com.cn/yapi/mock/220/`). The page also declares
  `tldataOpen/getResourceList` and related service names.

This is an **Epoint implementation lead**, not proof of a canonical standalone catalog
product or of identical software on the other two hosts. Epoint's
[first-party January 2025 bulletin](https://www.epoint.com.cn/eweb/UploadFile/29ab49d0-49dd-4f22-838c-fc00c2287a9c/20250207172723630.pdf)
corroborates its work on Tongliao's data platform. The earlier Huawei-guide route match
therefore must not be treated as exclusive vendor attribution. The next useful evidence
would be Epoint product documentation naming the open-data component and a second
installation with matching application-specific assets or API behavior.

Second-pass evidence and the complete 81-host status inventory are retained in
`custom-opendata-software-review-pass2-2026-09-07.json`. No visitor identifiers, full
page bodies, or dataset contents are included in that inventory.

### Second-pass validation

- All four edited records pass the single-file Cerberus validator.
- Documentation coverage/index generation and scoped whitespace checks pass.
- Full test suite: **314 passed, one existing failure** in
  `test_llms_txt_static_copies_match_root`, unchanged from the first pass.
- Dataset build succeeded; all four software assignments are verified in `catalogs.jsonl`.
  The rebuilt export contains 33,645 catalogs and 1,150 custom open-data portals.
- No new software definitions, API endpoints, or catalog status changes were introduced
  in this pass. No changes were committed.

## Third pass: deployable products and France/Russia review

Created **RUDI** (`rudi`) and **SIMAI Open Data Portal** (`simaiopendata`). Both meet
software-taxonomy criteria through independently installable distributions/products,
even though each currently resolves one record in the initial custom cohort.

- RUDI's [official repository](https://github.com/rudi-platform/rudi-portal) explicitly
  identifies Rennes and its EUPL-1.2 license. The
  [Docker Compose distribution](https://github.com/rudi-platform/rudi-out-of-the-box)
  demonstrates replication beyond a bespoke single site. Reclassified
  `rudirennesmetropolefr` and replaced its generic description.
- SIMAI's [product page](https://simai.ru/solution/gosudarstvennye-organizatsii/simai-portal-otkrytykh-dannykh/)
  offers a dedicated Bitrix open-data application and links a working
  [demo](https://opendata.sf2.simai.ru/), with matching `simai.opendata` assets and
  product credits. Reclassified `opendatademosimairu`, updated its obsolete URL and
  misleading display name, and corrected the vendor URL. Retained its inactive status
  and explicit demonstration description. The replacement URL was duplicate-checked
  against catalog exports; identifiers are unchanged.

The additional 102-host France/Russia homepage review returned 51 HTTP 200, 10 HTTP 403,
one HTTP 503 and 40 connection errors. This is a targeted evidence inventory, not a
liveness audit. CMS and frontend-framework matches alone were not promoted into new
portal products. The sanitized status inventory is in
`custom-opendata-software-review-pass3-2026-09-07.json`.

Epoint's [product catalog](https://www.epoint.com.cn/eweb/cpyfw/042001/042001003/?kind=dsj)
describes a broader integrated public-data platform, but does not establish an exclusive
openportal fingerprint across the three Chinese candidates. Those records remain custom.

Cumulative result: **four definitions created, nine records reclassified, 1,148 of the
original 1,157 custom records remaining**. API-access fields were preserved in this pass;
software documentation distinguishes RUDI portal and producer-node interfaces.

### Third-pass validation

Both new definitions and both edited catalog records pass Cerberus schema validation.
Documentation coverage/index generation and scoped whitespace checks pass. Full tests:
314 passed, one existing `test_llms_txt_static_copies_match_root` failure. Full software
validation retains the existing STAC Browser `licensing_type: Varies` schema error and
version/repository coverage threshold failures (13.7% and 43.1% respectively).
Dataset build succeeded. The export contains 33,645 catalogs, including 1,148 custom
open-data records; both new assignments and the updated SIMAI URL were verified.

## Fourth pass: OneGeo Suite and PRODIGE

Created two geospatial platform definitions discovered through the custom open-data
cohort. Shared source distributions and operator/vendor documentation establish products,
not merely common frontend frameworks.

| Product | Reclassified records | Evidence |
|---|---|---|
| OneGeo Suite | `datasudfr`, `wwwpigmaorg`, `datagrandlyoncom` | [Vendor references](https://neogeo.fr/references-projets/) name PIGMA and Grand Lyon; [DataSud documentation](https://www.datasud.fr/portal/documentation/) explicitly links OneGeo Suite. |
| PRODIGE | `wwwopendatarafr` | [DatARA tutorials](https://www.open-datara.fr/accueil/ressources/tutoriels-et-videos-de-prise-en-main) document V5; its live API documentation is titled `API PRODIGE Ressources`. |

Grand Lyon is a **Geoportal** record outside the original open-data cohort. Three of
these four corrections therefore reduce the original custom-open-data count. Existing
GeoNetwork and GeoServer component records were preserved. All four changes alter only
`software.id` and `software.name`; no endpoint, access, status or URL changes were inferred.

OneGeo Suite's [product site](https://www.onegeosuite.fr/) documents a modular application
family; its public API documentation link currently resolves to an unfinished/general
page, so the new definition leaves API support uncertain. The DataSud white-label
component's MIT license is not generalized to the whole suite.

PRODIGE's [project metadata](https://adullact.net/projects/prodige/) identifies CeCILL V2
and reusable catalog/storage/mapping functionality. Its [source group](https://gitlab.adullact.net/prodige)
corroborates the product. DatARA's API documentation returned HTTP 200 and an embedded
OpenAPI specification describing resource operations and authentication. Its advertised
open-data CSW capabilities URL returned HTTP 500 (`Service not found`), so no working
endpoint was added. Generic GeoNetwork fingerprints alone were not used for PRODIGE.

Cumulative result: **six software definitions created, 12 original open-data records
reclassified, plus one related geoportal**. The original cohort has **1,145 custom records
remaining**. See the product groups in the accompanying JSON for machine-readable decisions.

### Fourth-pass validation

Both definitions and all four edited catalog records pass schema validation. Documentation
coverage/index generation and scoped whitespace checks pass. Full tests: 314 passed,
one pre-existing `test_llms_txt_static_copies_match_root` failure. Full software validation
retains the existing STAC Browser licensing error and global coverage failures
(version 13.7%, repository URL 43.4%). Dataset build succeeded: 33645 catalogs and
410 software definitions; all four assignments are verified in exports. The custom
open-data count is 1,145. No changes were committed.
