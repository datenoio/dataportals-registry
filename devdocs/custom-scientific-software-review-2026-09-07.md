# Scientific repositories with custom software — 7 September 2026

## Scope and method

Reviewed all **3,186** scientific repository records marked `software.id: custom`
in the working-tree `catalogs.jsonl` export. Cross-checked the ID set against source
YAML: no differences before this change. Of these records, 3,152 were active,
27 inactive and 7 deprecated. This was a metadata-wide review with targeted live
verification, not a live fingerprint crawl of all 3,186 sites.

Grouped URLs by hostname and first path segment, searched names/descriptions/tags
for reusable product identities, and inspected endpoint-type frequencies. Compared
candidates against existing definitions, including pre-existing uncommitted additions
(MOLGENIS, BEXIS2, Diversity Workbench, Greenstone, VIVO, CWIS and OPeNDAP Hyrax).
Those additions are not results of this review. Checked first-party product documentation
and deployment lists for the strongest new candidates, then issued targeted GETs.

## New definitions and classifications

| ID | Matching registry record | Verification | Shared-product evidence |
|---|---|---|---|
| `specify` | `specifyportaluogedu` — GCBR Specify Portal, Guam | Homepage HTTP 200 with Specify branding; registered fishvouchers Solr search HTTP 200 with `numFound` | [Maintainer instance list](https://speciforum.org/t/specify-web-portal-examples/723) documents Kansas, Florida, Texas and other deployments; [source and installer](https://github.com/specify/webportal-installer) |
| `brahmsonline` | `herbariaplantsoxacukbolmau` — Mauritius Herbarium | [Live project](https://herbaria.plants.ox.ac.uk/bol/MAU) HTTP 200, explicit BRAHMS attribution | [Official online-site list](https://herbaria.plants.ox.ac.uk/bol/brahms/Websites) includes Oxford projects and independently hosted Embrapa and New Zealand servers; [FAQ](https://herbaria.plants.ox.ac.uk/bol/brahms/support/faq) identifies the separately installed BOL server |
| `lovd` | `wwwlovdnl` — Leiden Open Variation Database | [Homepage](https://www.lovd.nl/) HTTP 200, identifies LOVD and links to its databases | [Registered installations](https://lovd.nl/3.0/public_list) includes independent operators; [source](https://github.com/LOVDnl/LOVD3) and [FAQ](https://www.lovd.nl/3.0/faq) confirm reusable software |

Each new definition has **one directly attributable record in this subset**. Their
qualification as shared software rests on independently documented deployments outside
this subset, not on three large newly discovered clusters within the registry.

`specify` describes the public Specify Web Portal, not an assumed staff-facing Specify 7
installation. `brahmsonline` identifies the online publishing component rather than the
BRAHMS desktop application. The LOVD record currently points to the software/network
entry page: its classification is explicit, but it is not a verified installation-level
harvest seed. No URL or endpoint was invented or changed for that record.

Added discovery fingerprints, search queries and harvest guidance to the scientific-domain
guides, registered canonical IDs, and regenerated the software index. Existing API flags
were preserved; uncertain capabilities remain `Uncertain` in the new definitions.

## Repeated patterns that do not justify automatic reclassification

| Pattern | Observed count | Interpretation |
|---|---:|---|
| Empty/root URL path | 2,060 | No product-specific routing evidence; bespoke sites and front pages are mixed together. |
| First path segment `en` | 110 | Language routing, not a software fingerprint. |
| First path segment `data` | 36 | Generic content organization. |
| First path segment `home` | 25 | Generic landing page route. |
| First path segment `index.php` | 19 | PHP alone cannot identify a catalog product. |
| `www.ebi.ac.uk` hostname | 19 | Same organization hosts distinct domain databases; do not assign a common platform by owner. |
| `www.ncbi.nlm.nih.gov` hostname | 7 | Shared infrastructure does not establish a single reusable catalog frontend. |
| `sitemap` endpoint entries | 214 | Discovery mechanism, not software evidence. |
| `rest` endpoint entries | 41 | Generic transport/API label. |
| `oaipmh20` endpoint entries | 25 | Many repository packages implement OAI-PMH; requires live Identify/UI evidence. |
| GBrowse mentioned in descriptions | 2 | SalmoBase and cicer.info describe a genome-viewer component; insufficient evidence that it powers the entire catalog. |
| VAMDC named in identity/URL | 2 | BASECOL node and central VAMDC portal are different roles. Protocol membership does not prove common node software. |

Endpoint counts count endpoint objects, not necessarily distinct records. URL counts
use the original working export before reclassification. Patterns overlap.

## Follow-up candidates

- **BioMart:** sORFs.org explicitly describes a BioMart query interface. Verify the live
  interface and whether it merits a separate catalog entry or is subordinate to the
  custom sORFs application before assigning its main software field.
- **JACQ:** the registered JACQ portal describes a multi-herbarium management system.
  Establish the reusable product boundary and deployment evidence, rather than inferring
  multiple installations from participating collections in a shared service.
- **BioCASe:** distinguish the BioCASe Provider Software from the BioCASe network portal
  and GeoCASe aggregator. Shared protocol support is insufficient for a portal-wide ID.
- **BacDive / PhageDive:** PhageDive's description says it follows the BacDive model.
  Confirm shared source or maintainers' platform documentation; a common data model alone
  is not enough to create or assign software.
- **OAI-PMH repositories:** prioritize the 25 `oaipmh20` endpoint entries for targeted
  reclassification into existing repository definitions after checking response bodies.

No blanket reassignment was made for these candidates. An exhaustive live audit remains
outside this metadata review. This change reduces scientific `custom` records by three,
from **3,186 to 3,183**.

## Validation

- All three edited catalog YAML files pass `builder.py validate-yaml --file`.
- All three new software definitions pass the Cerberus schema and software-profile checks.
- Documentation coverage generator succeeds, including unique headings and valid anchors.
- `builder.py build` succeeds; JSONL, DuckDB and Parquet contain all three classifications.
- Full pytest run: **314 passed, 1 failed**. The failure is
  `test_llms_txt_static_copies_match_root`, involving existing root/static documentation
  copies that this change does not edit.
- Global `validate-software` reports no missing definition references or profile issues,
  but does not pass: existing `geo/stacbrowser.yaml` uses disallowed licensing type `Varies`,
  and aggregate version/repository-URL coverage is below the configured thresholds
  (14.1% versus 25%, and 42.6% versus 55%). These are registry-wide issues outside this review.

## Second pass: astronomy and language archives

Continued from **3,183** scientific `custom` records. Created three more definitions and
reclassified **11 records**, leaving **3,172**. These totals count registry records, not
unique deployments. No new catalog records were added.

### DaCHS (`dachs`) — four records

| Record | Live evidence on 7 September 2026 |
|---|---|
| `dcgvoorg` | TAP capabilities HTTP 200; `Server: DaCHS/2.12.2 twistedWeb/22.4.0` |
| `dczahuniheidelbergde` | Homepage HTTP 200; same explicit DaCHS server identification |
| `voastronnl` | Homepage GAVO CSS/JavaScript plus TAP capabilities containing characteristic `gavo_*` functions |
| `arvoregistrysciam` | GAVO assets plus the legacy `/__system__/tap/run/tap/capabilities` route and characteristic GAVO functions |

[DaCHS documentation](https://docs.g-vo.org/DaCHS/) identifies the reusable publication
package and links to its source and deployment instructions. The GAVO, ASTRON and ArVO
sites provide independent deployment evidence. `dc.g-vo.org` and
`dc.zah.uni-heidelberg.de` appear to be aliases of the same GAVO service; both existing
records are correctly reclassified, but should be reviewed for deduplication separately.
The matching assets and implementation-specific functions distinguish this cluster from
arbitrary TAP servers. Existing endpoints and URLs were preserved.

### Daiquiri (`daiquiri`) — six records

All six sites returned HTTP 200 and expose a footer explicitly naming Daiquiri and linking
to its project. The [upstream documentation](https://django-daiquiri.github.io/docs/)
explains the reusable data-publication framework and lists deployments.

- `gaiaaipde` — Gaia@AIP, footer reports Daiquiri 1.4.0.
- `wwwravesurveyorg` — RAVE query service, Daiquiri attribution.
- `wwwcosmosimorg` — CosmoSim, footer reports Daiquiri 1.3.8.
- `wwwplatearchiveorg` — APPLAUSE, registered path redirects to `/cms/home/`, footer
  reports Daiquiri 1.3.6 and release notes name the software.
- `musewideaipde` — MUSE-Wide, Daiquiri attribution and release/table metadata navigation.
- `carsaipde` — CARS, Daiquiri attribution and release/table metadata navigation.

This is product evidence across several separately published scientific projects, not a
classification inferred solely from shared AIP ownership. AIP also documents the shared
software in its [research infrastructure description](https://www.aip.de/en/research/escience/).
The definition covers the Daiquiri family; individual deployed versions were not promoted
into an unsupported claim about the latest software release.

The CARS record's name was corrected from “CARS Archaeological Research Database” to
“Close AGN Reference Survey (CARS)”. Its description already correctly described astronomy;
the [live homepage](https://cars.aip.de/) confirms the survey identity. Other metadata was
preserved.

### FLAT (`flat`) — one record

`archivehumlabluse` now identifies Fedora Language Archiving Technology. The live Lund
archive serves FLAT-specific `flat_bootstrap_theme` assets, Islandora modules and routes,
and attribution to The Language Archive. Its registered `/flat/oai2?verb=Identify` endpoint
returns OAI-PMH metadata naming Lund University Humanities Lab Archive.

The [FLAT source and deployment package](https://github.com/TLA-FLAT/FLAT) document the
Fedora/Islandora-based reusable repository. The developers' [CLARIN paper](https://pure.mpg.de/rest/items/item_3159108_1/component/file_3159109/content)
explains its use for The Language Archive and Meertens Institute. This supports a specific
FLAT classification rather than falling back to its underlying Islandora component.

### Candidates investigated but left unchanged

- **AMBIT / eNanoMapper:** [first-party model documentation](https://enanomapper.adma.ai/datamodel/)
  explicitly identifies AMBIT as the implementation, and the [AMBIT project](https://ambit.sourceforge.net/)
  provides reusable software and separate deployments. However, the registered
  `data.enanomapper.net` host timed out on two targeted attempts; the documented
  `apps.ideaconsult.net/enanomapper/` entry redirects there and also timed out. AMBIT is a
  strong definition candidate, but this pass did not confirm the current live catalog.
- **SnoVault / ENCODE / Fourfront:** live ENCODE and 4DN portals work, and
  [DCIC's account of the codebase](https://github.com/4dn-dcic) confirms shared ancestry
  and common infrastructure with CGAP/SMaHT. They are distinct portal implementations
  over related SnoVault backends, so a single portal software ID was not assigned just
  from the shared JSON-LD/database framework. A taxonomy decision should distinguish
  the reusable backend from product-specific frontends.
- **BioMart / sORFs:** the registered sORFs host now serves a live interface without a
  BioMart marker in its homepage. Its older description of a secondary BioMart interface
  is insufficient to classify the current whole site as BioMart.
- **JACQ:** the live central service and API are identifiable, but participating herbaria
  do not alone demonstrate separately deployable portal software. No ID was created.
- **BacDive / PhageDive:** no new evidence established a named shared software product
  for these related services; both remain unchanged.

Discovery and harvest recipes were added for all three accepted products, and the software
index was regenerated. Product-level capabilities are kept distinct from the availability
of individual catalog APIs; unverified catalog endpoints were not added.

Second-pass validation: all 11 edited catalogs pass schema validation; the three new
definitions pass schema and profile validation; the dataset build succeeds. Entity JSONL,
DuckDB and Parquet agree on 3,172 remaining scientific `custom` entity records when
scheduled records are excluded. The combined exports additionally include the existing
scheduled `seamapenvdukeedu` record, giving 3,173 if scheduled records are counted.
Full pytest again reports 314 passed and the same unrelated static `llms.txt`
synchronization failure. Global software validation still reports the existing STAC
Browser licensing-type error and aggregate coverage shortfalls (version 14.0%, repository
URL 43.0%).

## Third pass: digital repositories, CRIS and chemical data

Continued from **3,172** scientific `custom` entity records. Probed the homepages and
registered OAI-PMH endpoints of 24 selected records (excluding the already identified
products and the suspicious cross-institution Kielipankki endpoint). The machine-readable
[probe log](custom-scientific-oai-probes-2026-09-07.json) records URLs, status codes,
redirects, errors and candidate markers. This is bounded candidate verification, not a
scan of every remaining host. HTTP success by itself is not protocol validation.

Created four additional definitions, each with one confirmed registry match:

| Software | Record | Attribution and reuse evidence |
|---|---|---|
| `openequella` | `radarbrookesacuk` | Live RADAR HTML serves `p/r/2025.2.1/com.equella.core/` assets. [Vendor use cases](https://www.edalex.com/openequella/) and [source](https://github.com/openequella/openEQUELLA) identify the shared repository product. |
| `aubrey` | `digitallibraryuntedu` | UNT's [infrastructure documentation](https://library.unt.edu/digital-libraries/trusted-digital-repository/) identifies the public access system, and its [2024 deployment presentation](https://digital.library.unt.edu/ark:/67531/metadc2405129/m1/7/) explicitly describes separate instances for UNT, Texas History and Oklahoma History. The registered UNTDRD collection and OAI endpoint both respond successfully. |
| `dialnetcris` | `investigacionuniriojaes` | Live research portal attributes the software to Fundacion Dialnet. The [provider's product page](https://fundaciondialnet.unirioja.es/servicios/dialnet-cris/) identifies a shared SaaS with an institutional deployment directory; [REBIUN's CRIS survey](https://repositorio.rebiun.org/bitstream/handle/20.500.11967/1445/Encuesta%20CRIS_%20informe.pdf?isAllowed=y&sequence=1) associates La Rioja with Dialnet CRIS. |
| `ambit` | `dataenanomappernet` | The site now responds: explicit `Accept: text/html` reveals `AMBIT v4.1.0-SNAPSHOT` and a statement that eNanoMapper customizes AMBIT. A bounded substance request returns RDF/XML under default negotiation. [Project documentation](https://ambit.sourceforge.net/) and [eNanoMapper's user guidance](https://enanomapper.net/deliverables/d1/D1.4_UserGuidance.pdf) corroborate the product identity and reusable implementation. |

This resolves the previous AMBIT timeout uncertainty without changing the catalog's
status based on a transient failure. The observed snapshot version is instance evidence,
not a claimed stable release of the software. Aubrey's GitHub repository is empty, so the
new definition does not claim downloadable source or assign an inferred open-source license.
Dialnet CRIS is distinct from the central Dialnet bibliographic database; dataset support
is left uncertain because a bibliographic research portal does not automatically demonstrate
dataset holdings. Its harvest recipe requires explicit dataset types.

All four records have only their software identity changed. Discovery fingerprints and
harvest recipes were added, with guidance to distinguish collections, datasets and member
records. These four edits alone reduce the reviewed set to **3,168** scientific `custom` records. Cumulatively, these three passes create **10 definitions** and reclassify
**18 existing records**.

### Findings that should not become software guesses

- **Oxford Brookes RADAR:** the institution's name is not the existing RADAR product;
  live `com.equella.core` assets identify openEQUELLA.
- **OhioLINK and Cocoon:** an `<eprints>` element in the Open Archives namespace is a
  generic OAI repository-description schema, not proof that EPrints software is installed.
- **DEIMS:** the recorded OAI URL returns a JSON pycsw landing document. The homepage is
  Drupal. Neither the protocol label nor a subordinate pycsw endpoint justifies identifying
  the whole bespoke portal as an OAI repository or a pycsw installation.
- **ESA Open Science Catalog:** its recorded OAI URL returns a pycsw/STAC JSON catalog,
  not an OAI-PMH Identify response. This merits endpoint correction after resolving the
  frontend/backend boundary, rather than assigning software from the old endpoint type.
- **UCAR RDA:** the homepage redirects to GDEX; the recorded OAI route redirects and
  returns 404. The old OAI route is not current platform evidence.
- **CERIC:** both candidate requests failed certificate verification; TLS checks were
  not disabled, and no software inference was made.
- **PORTULAN CLARIN:** both candidate requests timed out. No classification was inferred.
- **ARCHE / DaSCH:** live services are identifiable, but this pass did not establish the
  separate deployment evidence required to introduce a platform definition confidently.

These endpoint findings are documented for follow-up; endpoint URLs, types, and API flags
were not rewritten during this classification pass.

Third-pass validation: the four new definitions and four edited catalogs pass schema
validation; the software profiles pass. Documentation coverage and the dataset build succeed.
The final software JSONL, compressed JSONL and DuckDB software table include the conservative
Dialnet CRIS capability setting. Full pytest reports 314 passed and the same existing static
`llms.txt` synchronization failure. Global software validation reports the pre-existing STAC
Browser licensing error and aggregate coverage shortfalls, with no missing references or
software profile issues.

At final export verification, the shared working tree also contains two classifications
made outside this pass: `meertensknawnl` to FLAT and `wwwcluesprojectorg` to Daiquiri. They
are not included in this review's 18 reclassifications. With those additional changes,
entity JSONL, DuckDB and Parquet agree on **3,166** remaining scientific `custom` entity
records. The four classifications from this pass each appear once in every export.
