# Discovering metadata catalogs

How to find **metadata catalog** installations (`catalog_type: Metadata catalog`). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). Overview: [discovery.md](discovery.md).

These sites publish **catalog/dataset metadata** (often RDF / DCAT or SDMX structural metadata), not a full open-data CMS and not a research-data file store. If the public product is CKAN, Dataverse, or GeoNetwork, use those `software.id` values and types instead.

## FAIR Data Point (`fairdatapoint`) {#fairdatapoint}

Open-source REST API and web client for FAIR metadata as RDF (DCAT + the [FAIR Data Point specification](https://specs.fairdatapoint.org/)). Docs: [docs.fairdatapoint.org](https://docs.fairdatapoint.org). Index of public points: [home.fairdatapoint.org](https://home.fairdatapoint.org).

**Signals:** HTML client `fdp-client`; JSON-LD or Turtle DCAT at the catalog root; paths such as `/catalog`, `/dataset`, `/swagger-ui`; hostname often `fdp.` or path `/fairdatapoint`.

**Confirm:** GET the catalog URL with `Accept: text/turtle` or `application/ld+json` and check for DCAT `Catalog` / FAIR Data Point metadata. The HTML UI alone is not enough if it is only a marketing page.

[public/index.html](https://github.com/FAIRDataTeam/FAIRDataPoint-client/blob/develop/public/index.html) noscript says “fdp-client doesn't work properly” (196 hosts in September 2026, including `fdp.envri.eu`). `body="fdp-client"` matched 206. Keep both.

| Tool | Query |
|------|-------|
| Google | `"FAIR Data Point" OR "fairdatapoint" (catalog OR DCAT) -site:github.com` |
| Google | `inurl:fairdatapoint OR intitle:"FAIR Data Point"` |
| Censys | `web.endpoints.http.body: "fdp-client doesn't work properly"` |
| FOFA | `body="fdp-client doesn't work properly"` |
| Censys | `web.endpoints.http.body: "fdp-client"` |
| FOFA | `body="fdp-client"` |
| Censys | `web.endpoints.http.body: "fairdatapoint"` |
| FOFA | `body="fairdatapoint"` |
| crt.sh | `fdp.%` |

Start from the public index, then fill gaps with search. Skip points that require login for any catalog listing. Register the FDP root, not a single dataset IRI. Do not duplicate the index (`home.fairdatapoint.org`) if it is already in the registry.

## Aristotle Metadata Registry (`aristotlemdr`) {#aristotlemdr}

Open-source metadata registry for models and controlled vocabularies. Site: [aristotlemetadata.com](https://www.aristotlemetadata.com) (product branding varies by deployment).

**Signals:** Aristotle MDR; `/api/v4/` or browsable registry of object classes / data elements; stewardship workflows.

**Confirm:** GET the public registry home and an API listing when unauthenticated access exists. Skip staff-only stewardship tools.

| Tool | Query |
|------|-------|
| Google | `"Aristotle" ("Metadata Registry" OR MDR) (vocabulary OR "data element") -site:github.com` |
| Censys | `web.endpoints.http.body: "Aristotle"` |
| FOFA | `body="Aristotle"` |

## Fusion Metadata Registry (`fusionregistry`) {#fusionregistry}

SDMX-native structural metadata registry (code lists, DSDs, REST). Often branded Fusion Registry / FMR.

**Signals:** Fusion Registry; SDMX REST (`/sdmx/v2/` or `/ws/public/sdmxapi/`); structural metadata browser.

**Confirm:** GET the public registry or SDMX REST catalog. Do not confuse with a PxWeb/.Stat **data** portal — those stay `pxweb` / `statsuite` under indicators. A public series UI titled Fusion Data Browser stays `fusiondatabrowser`.

| Tool | Query |
|------|-------|
| Google | `"Fusion Registry" OR "Fusion Metadata Registry" SDMX -site:github.com` |
| Google | `inurl:/sdmx/v2/ "Fusion"` |
| Censys | `web.endpoints.http.body: "Fusion Registry"` |
| FOFA | `body="Fusion Registry"` |

## Metadata Browser (`mwmb`) {#mwmb}

MetadataWorks catalog UI for datasets, standards, and terminologies. Site: [metadataworks.ai](https://metadataworks.ai/metadata-browser).

**Signals:** Metadata Browser / MetadataWorks; federated metadata search.

**Confirm:** GET the public browser. One record per public deployment.

| Tool | Query |
|------|-------|
| Google | `"Metadata Browser" MetadataWorks (catalog OR terminology)` |
| Censys | `web.endpoints.http.body: "MetadataWorks"` |
| FOFA | `body="MetadataWorks"` |

## DataHub (`datahubproject`) {#datahubproject}

LinkedIn/Acryl DataHub metadata platform. Site: [datahubproject.io](https://datahubproject.io). Distinct from datahub.io (CKAN).

**Signals:** HTML title `DataHub`; meta description “A Metadata Platform for the Modern Data Stack”; `/api/graphql`; `assets/index-*.css` SPA. GraphQL is often `401` without a token — the public UI is enough to confirm.

**Confirm:** GET the catalog home. Stop on login-only tenants with no public dataset list. Do not invent this id from a generic “data hub” heading.

[index.html](https://github.com/datahub-project/datahub/blob/master/datahub-web-react/index.html) describes “A Metadata Platform for the Modern Data Stack” (1,556 hosts in September 2026, including `89.58.44.88:9002`). `title="DataHub"` matched 5,058 hosts, including a Chinese data-hub system (`1.94.188.107`). Installs that change the description still match the title, so keep both.

| Tool | Query |
|------|-------|
| Google | `"DataHub" "Metadata Platform for the Modern Data Stack"` |
| Censys | `web.endpoints.http.body: "A Metadata Platform for the Modern Data Stack"` |
| FOFA | `body="A Metadata Platform for the Modern Data Stack"` |
| Censys | `web.endpoints.http.title: "DataHub"` |
| FOFA | `title="DataHub"` |

## CEDAR Workbench (`cedar`) {#cedar}

Stanford metadata-template workbench. App: [cedar.metadatacenter.org](https://cedar.metadatacenter.org). Docs: [cedar-docs](https://metadatacenter.github.io/cedar-docs/). Distinct from the metadatacenter.org marketing homepage.

**Confirm:** GET `https://cedar.metadatacenter.org` (title `Project Cedar`). Register the workbench, not each template or filled instance.

| Tool | Query |
|------|-------|
| Google | `"CEDAR Workbench" OR "Project Cedar" (metadata OR template)` |
| Censys | `web.names: "cedar.metadatacenter.org"` |
| FOFA | `host="cedar.metadatacenter.org"` |

## CBD Clearing-House (`cbdchm`) {#cbdchm}

Secretariat application for the Convention on Biological Diversity clearing-houses. Repository: [scbd/absch.cbd.int](https://github.com/scbd/absch.cbd.int). API notes: [docs.cbddev.xyz](https://docs.cbddev.xyz/).

**Signals:** `/app/css/template.css` and `/app/components/scbd-branding/`. Public realms are `chm.cbd.int`, `absch.cbd.int`, and `bch.cbd.int`.

**Confirm:** GET the realm home and check for `/app/css/template.css`. Register each public realm once. Skip `api.cbd.int`, `accounts.cbd.int`, `oasis.cbd.int` (staff manage UI), `*.cbddev.xyz`, training hosts, and the developer docs portal. The Online Reporting Tool at `ort.cbd.int` is a separate Nuxt app ([scbd/online-reporting-tool](https://github.com/scbd/online-reporting-tool)), not this software. National Bioland sites (`github.com/scbd/bioland`) are a different product.

Checked 25 September 2026. Live realm HTML no longer contains `scbd/angular-flex`. That FOFA query still returns nine hosts from an older index (the three realms, `training-absch.cbd.int`, `accounts.cbd.int`, `oasis.cbd.int`, plus `accounts`, `bch`, and `oasis` on `cbddev.xyz`). `body="scbd-branding"` and `body="@scbd/ckeditor5"` return 0 because FOFA has not indexed the current shell. Unscoped `body="/app/css/template.css"` is noise (hundreds of unrelated shops). Scope it with `domain="cbd.int"`: four hosts, the three public realms plus `training-absch.cbd.int` (times out; training copy). `domain="cbd.int"` itself is about 90 hosts and is the sibling check; no other host on that domain serves this app. `body="scbd/angular-flex" && domain!="cbd.int" && domain!="cbddev.xyz"` is 0.

| Tool | Query |
|------|-------|
| Google | `"Clearing-House" (ABSCH OR BCH OR CHM) site:cbd.int` |
| Censys | `web.endpoints.http.body: "scbd/angular-flex"` |
| FOFA | `body="/app/css/template.css" && domain="cbd.int"` |
| FOFA | `body="scbd/angular-flex"` |

## WMO OSCAR (`oscar`) {#oscar}

WMO Observing Systems Capability Analysis and Review Tool. Product home: [space.oscar.wmo.int](https://space.oscar.wmo.int/). API notes: [space.oscar.wmo.int/apidoc](https://space.oscar.wmo.int/apidoc/).

**Signals:** OSCAR/Space sets cookie `Oscar-release-diag` and title “WMO OSCAR” at `space.oscar.wmo.int`. OSCAR/Surface (`oscar.wmo.int/surface`, `/surface/rest/api`) and GAWSIS (`gawsis.meteoswiss.ch/GAWSIS/`) share an Angular shell with `Application.OSCAR` in the HTML. The Surface `<title>` is empty until that app boots.

**Confirm:** GET the module home. One record per public module (Surface, Space). GAWSIS is the same shell and is already registered on its own. Skip OSCAR/Requirements pages on the Space host. Skip staging hosts `space-test.oscar.wmo.int`, `oscardepl.wmo.int`, `gawsisdepl.meteoswiss.ch`, and `gawsisdevt.meteoswiss.ch`. Skip the WMO Weather Radar Database, the OSCAR speech corpus, university repositories named Oscar, and OSCAR-CEL (`oscar-cel.com`, title “Bienvenue sur OSCAR”).

Checked 25 September 2026. `body="Observing Systems Capability Analysis and Review Tool"` is 17 rows: Space, `space-test`, GAWSIS production and staging, plus a Japanese meteorology blog and weathernco.com. It misses production Surface, because `oscar.wmo.int/` is a 301 to Space and FOFA does not store `/surface/`. `title="WMO OSCAR"` is 4 rows (Space and `space-test` only). `body="css/oscar.css"` is 108 and is mostly other products named OSCAR. `body="favicon_oscar.ico"` also matches OSCAR-CEL.

| Tool | Query |
|------|-------|
| Google | `"Observing Systems Capability Analysis and Review Tool" OSCAR` |
| Censys | `web.endpoints.http.body: "Oscar-release-diag"` |
| FOFA | `body="Oscar-release-diag"` |
| Censys | `web.endpoints.http.body: "Application.OSCAR"` |
| FOFA | `body="Application.OSCAR"` |
| FOFA | `body="Oscar-release-diag" \|\| body="Application.OSCAR"` |
| FOFA | `host=".oscar.wmo.int"` |
| crt.sh | `%.oscar.wmo.int` |

## Related

- [discovery.md](discovery.md)
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-opendata.md](discovery-opendata.md) (DCAT portals that are not FDP)
- [discovery-indicators.md](discovery-indicators.md) (Fusion Registry vs PxWeb/.Stat)
- [harvest-metadata.md](harvest-metadata.md)
- [harvest.md](harvest.md)
- [discovery-scientific.md](discovery-scientific.md)
- [software-taxonomy.md](software-taxonomy.md)
- [catalog-types.md](catalog-types.md)
