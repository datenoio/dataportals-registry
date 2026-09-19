# Custom-software pattern analysis (2026-09-06)

## Scope and method

The source YAML contained 6,821 records with `software.id: custom` before this review:
6,820 verified entities and one scheduled record. The largest catalog groups were 3,201
scientific repositories, 1,157 open-data portals, 1,116 indicator catalogs, and 1,028
geoportals.

The review clustered local records by catalog type, hostname, URL path fragments,
structured endpoint types, and product names or fingerprints in descriptions. Candidate
clusters were checked against first-party product documentation and public-instance lists.
A new software ID was accepted only when the evidence identified a reusable product rather
than a protocol, organization, one-off implementation, or generic framework route.

## Created: MOLGENIS (`molgenis`)

MOLGENIS is a reusable open-source FAIR scientific data platform with catalogue and
registry applications. The strongest local signature is the legacy `molgenis.do` route;
the current EMX2 generation advertises “Created with MOLGENIS” and exposes GraphQL, CSV,
Excel, and RDF interfaces. The first-party [MOLGENIS tools page](https://molgenis.org/tools.html)
also identifies public catalogues and registry examples by name.

Seven records were reassigned from `custom`:

| Record | Evidence |
|--------|----------|
| WormQTL | `molgenis.do` route and first-party example list |
| WormQTL HD | `molgenis.do` route |
| UMCG Research Data Catalogue | First-party public catalogue list |
| BBMRI-ERIC Directory | First-party public catalogue list |
| DEB Register | First-party registry example list |
| International MVID Patient Registry | First-party registry example list |
| CHD7 Database | First-party registry example list |

After this first pass, 6,814 source records remained `custom`.

## Second pass: five additional definitions

A second pass searched non-boilerplate descriptions for explicit product attribution,
ranked repeated platform and route signatures, checked the live sites with targeted GETs,
and compared the results with first-party product documentation.

| New ID | Reclassified records | Evidence |
|--------|----------------------|----------|
| `bexis2` | 1 | Biodiversity Exploratories redirects to the standard `/home/Start` route and serves BEXIS2 assets; the upstream project documents the dataset, metadata, and data APIs. |
| `diversityworkbench` | 3 | LIAS and IndExs explicitly identify Diversity Workbench; the SNSB catalog is the documented DWB BioCASe/RDF publication pipeline. |
| `greenstone` | 1 | The SALCC library uses `/greenstone3/library`, Greenstone XML namespaces, standard interface assets, and the product's collection route. |
| `vivo` | 1 | HUN-REN ARP search explicitly says it is powered by VIVO, and the live HTML contains both VIVO and Vitro application markers. |
| `cwis` | 1 | The live Cuban thesis catalog identifies CWIS in its rendered HTML; its record description and the upstream project identify the full Collection Workflow Integration System product. |

These products meet the shared-software rule even where only one registry record is
currently classified: BEXIS2 documents multiple research deployments, Greenstone has an
official public-library showcase, VIVO is a self-hosted research-discovery platform, and
CWIS is distributed specifically for independent metadata-collection sites. Diversity
Workbench already has three directly attributable registry records and documents many
independent server/database installations.

After both passes, 6,807 source records remain `custom` (14 records reclassified across
six new definitions, including MOLGENIS).

## Repeated patterns retained as `custom`

| Pattern | Records | Decision |
|---------|---------|----------|
| `/extranet/openportal/pages/...` | 3 | Huawei's government data-enablement deployment guide documents this route, but it describes a solution template with project-specific components rather than a stable standalone software product. Keep `custom` pending a canonical product identity and API contract. |
| Same owner hostname | 2–20 per repeated host | Multiple catalogs on one publisher host do not demonstrate shared software. No definition follows from hostname reuse alone. |
| CKAN, Opendatasoft, and Socrata endpoint types on the same record | 9 | These mutually incompatible product probes are discovery artifacts, not product evidence. Do not classify from endpoint labels without validating response bodies. |

## Follow-up candidates

1. Investigate the three Huawei-style open-portal deployments for a consistent product
   banner, vendor name, and machine-readable list API. A new definition should use the
   product name, not the broad solution name.
2. Evaluate Dtechtive separately as a managed search service. Its Scottish Government
   deployment is explicit, but the current evidence does not yet show multiple catalog
   tenants or an interoperable catalog API.
3. Treat NASA Common Metadata Repository (CMR) as a candidate backend service, not yet a
   shared installable catalog product; determine whether a software ID should represent
   the CMR service or the broader Earthdata catalog stack.
4. Audit the nine multi-product endpoint records and remove false-positive endpoints before
   using them in any automated software classifier.
