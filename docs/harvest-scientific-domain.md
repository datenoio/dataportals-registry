# Harvesting domain scientific repositories

Biodiversity, crop, chemistry, facility, and earth-system APIs (`catalog_type: Scientific data repository`). Institutional IRs and CRIS: [harvest-scientific.md](harvest-scientific.md). Overview: [harvest.md](harvest.md). Finding installations: [discovery-scientific-domain.md](discovery-scientific-domain.md).

GET only. Stop on `401`/`403`. Prefer `endpoints[]`.

| Page | Use when |
|------|----------|
| This page | IPT, Symbiota, THREDDS, ERDDAP, FROST-Server, Breedbase, Tripal, VEuPathDB, MassBank, ioChem-BD, ESGF, ALA, Galaxy, SEEK, ICAT, MyTardis, InterMine, GRIN-Global, PlutoF, JGI, cBioPortal, CLLD, TalkBank, Pathway Tools, IBDC |
| [Institutional IRs and CRIS](harvest-scientific.md) | Dataverse, DSpace, Invenio, EPrints, Pure, RADAR, Yoda, mixed publication catalogs |
| [harvest-biodiversity.md](harvest-biodiversity.md) | IPT, Symbiota, ALA — occurrence vs dataset grain |
| [harvest-earthdata.md](harvest-earthdata.md) | THREDDS, ERDDAP, ESGF data nodes, SciCat, openEO, ESA Science Archive |

All `software.id` values: [software-index.md](software-index.md).

## GBIF IPT (`ipt`) {#ipt}

Biodiversity publishing toolkit. Each Darwin Core archive is one dataset.

```text
GET https://host/inventory/dataset
GET https://host/rss.do
GET https://host/dcat
```

Keep inventory/RSS **datasets**. Do not harvest occurrence rows. Full grain: [harvest-biodiversity.md](harvest-biodiversity.md). Skip gbif.org itself if you only needed publisher IPTs already in the registry. Prefer the IPT root from the catalog `link`.

**Keep:** IPT Darwin Core **archives**. **Drop:** occurrence rows.

## THREDDS (`thredds`) {#thredds}

```text
GET https://host/thredds/catalog.xml
GET https://host/thredds/catalog.html
```

The catalog XML is a **tree**. Recurse `catalogRef`; harvest `dataset` elements that have an ID or OPeNDAP/WMS service — not every nested directory. Do not treat NetCDF files inside a datasetScan as separate catalog records unless they are independently cited. Prefer THREDDS over `opendap` when both exist on the same TDS. Earth-observation grain: [harvest-earthdata.md](harvest-earthdata.md).

**Keep:** THREDDS `dataset` with an ID / OPeNDAP service. **Drop:** nested directories and every file under `datasetScan`.

## ERDDAP (`erddap`) {#erddap}

```text
GET https://host/erddap/info/index.json
GET https://host/erddap/index.json
```

Each row in `info/index.json` is a dataset (`datasetID`). Drop the `allDatasets` helper table if present. Grid vs table datasets are both in scope.

**Keep:** ERDDAP `datasetID` rows. **Drop:** the `allDatasets` helper table.

## FROST-Server (`frostserver`) {#frostserver}

OGC SensorThings API. Filter exports on `software.id = 'frostserver'`. Prefer `endpoints[]` (`sensorthings`).

```text
GET https://host/v1.1/
GET https://host/v1.1/Things?$top=100&$count=true
GET https://host/FROST-Server/v1.1/Things?$top=100&$count=true
GET https://host/v1.1/Datastreams?$top=100&$count=true
```

Type `/v1.1/Things` as `sensorthings`. Probe both origin `/v1.1/Things` and `/FROST-Server/v1.1/Things` (default servlet). Cleanup strips `/FROST-Server` (keeping any path prefix such as `/soop`) so the prefixed probe is not doubled. Leave other mounts (`/sensorthings/`, `/sta/`, `/server/`) so origin `/v1.1/` concatenates onto those catalog links. Do not copy a `/dataportaal/` UI host onto a different API origin.

**Keep:** **Things** (stations / sensors) or **Datastreams** (observed properties), depending on the harvest ask — not both as duplicate datasets unless requested. Page with `$skip` / `$top` and `@iot.nextLink`. **Drop:** Observations, HistoricalLocations, FeaturesOfInterest rows, and the HTML start page. Stop on `401`/`403`. Skip demo/scratchpad hosts. Prefer the API root from the catalog `link` (some UIs sit on a separate dataportaal host).

## Symbiota (`symbiota`) {#symbiota}

Biodiversity collections CMS. Official directory: [symbiota.org/symbiota-portals](https://symbiota.org/symbiota-portals/). Filter exports on `software.id = 'symbiota'`.

```text
GET https://host/collections/index.php
GET https://host/collections/datasets/rsshandler.php
GET https://host/portal/collections/index.php
GET https://host/portal/collections/datasets/rsshandler.php
```

Typical catalog links already end in `/portal/` or `/collections/`. Cleanup strips those mounts so harvest collection paths attach at origin and are not doubled (`/portal/portal/`).

**Keep:** published Darwin Core **datasets** (RSS) and, if the user wants collection-level catalogs, one record per public collection (`collid`). **Drop:** individual occurrences, images, and checklists as datasets. One portal = one harvest scope (not per collection unless asked). Login-only portals: stop. Detail: [harvest-biodiversity.md](harvest-biodiversity.md#symbiota).

## Breedbase (`breedbase`) {#breedbase}

Crop breeding information systems (CassavaBase, MusaBase, YamBase, SweetPotatoBase, Sol Genomics Network, Triticeae Toolbox / T3).

```text
GET https://host/brapi/v2/serverinfo
GET https://host/brapi/v2/studies?page=0&pageSize=100
GET https://host/brapi/v2/trials?page=0&pageSize=100
```

**Keep:** trials and studies (breeding experiments). **Drop:** individual plots, samples, marker calls, and `/brapi/v2/germplasm` rows unless the user asked for accession-level harvest. One crop instance = one harvest scope.

## Tripal (`tripal`) {#tripal}

GMOD Tripal community genome databases (CottonGEN, SoyBase, PeanutBase, GDR, TreeGenes). Drupal + Chado.

```text
GET https://host/web-services/
```

**Keep:** published analyses, maps, and downloadable datasets. **Drop:** gene pages, BLAST hits, and germplasm accessions as datasets. Prefer the site root from the catalog `link`.

## VEuPathDB (`veupathdb`) {#veupathdb}

EuPathDB WDK organism sites (VEuPathDB, PlasmoDB, FungiDB, VectorBase, TriTrypDB).

```text
GET https://host/webservices/
```

**Keep:** experiment / isolate / genome **datasets** listed for download. **Drop:** gene records, search-strategy result rows, and genome-browser tracks as datasets. One organism portal = one harvest scope; do not flatten the hub and every component site into one crawl unless asked.

## MassBank (`massbank`) {#massbank}

Reference mass-spectral databases (MassBank EU, MassBank Japan, MoNA).

```text
GET https://host/MassBank/api/records
GET https://host/rest/spectra
```

Path prefixes differ per instance (`/MassBank/` vs MoNA `/rest/`). Cleanup strips `/MassBank` so `/MassBank/api/records` attaches at origin and is not doubled. Leave MoNA origin links so `/rest/spectra` concatenates there.

**Keep:** spectral **records** (or record accessions) as the dataset grain. **Drop:** peak lists inside a record as extra datasets.

## ioChem-BD (`iochembd`) {#iochembd}

Computational chemistry nodes. Browse is DSpace-based; Find is the central index.

```text
GET https://host/rest/items
GET https://host/oai/request?verb=Identify
GET https://host/oai?verb=Identify
GET https://host/oai/request?verb=ListRecords&metadataPrefix=oai_dc
```

**Keep:** published collections/items (CML datasets). **Drop:** Create-module private workspaces and unpublished items. Prefer a **node** over cloning the Find homepage unless harvesting the central index was requested. Use OAI when REST is incomplete.

## ESGF (`esgf`) {#esgf}

Metagrid / esg-search **index** portals. Do not use this recipe on ESGF **data nodes** — those are `thredds`.

```text
GET https://host/esg-search/search?format=application%2Fsolr%2Bjson&limit=100&offset=0
```

**Keep:** Solr docs that represent CMIP/obs4MIPs **datasets** (`master_id` / `dataset_id`). **Drop:** files, aggregations, and wget scripts as extra datasets. Prefer the index host from the catalog `link`. Data-node grain: [harvest-earthdata.md](harvest-earthdata.md#esgf) and [THREDDS](#thredds).

## Atlas of Living Australia (`ala`) {#ala}

Living Atlases stack.

```text
GET https://host/ws/registry/collections
```

Harvest **collections** (data resources), not `/ws/occurrences/search` hits (those are occurrence records). Species autocomplete is not a dataset list.

**Keep:** Living Atlas **collections** / data resources. **Drop:** `/ws/occurrences/search` hits and species autocomplete.

## DataONE (`dataone`) {#dataone}

Harvest the **member node** dataset search (`formatType=DATA` when supported). Do not crawl CN-wide duplicates of nodes already in this registry unless the user asked for the coordinating-node view.

**Keep:** member-node search hits with `formatType=DATA`.
**Drop:** coordinating-node copies of MNs already in this registry unless asked.

```text
GET https://host/cn/v2/query/solr/?q=formatType:DATA&rows=25
```


## MOLGENIS (`molgenis`) {#molgenis}

For current EMX2 installations, enumerate public databases and inspect their tables
through GraphQL, then export only data-catalogue entities:

```text
POST https://host/api/graphql
POST https://host/<database>/api/graphql
GET  https://host/<database>/api/csv/<table>
GET  https://host/<database>/api/rdf
```

Keep catalogue, collection, cohort, biobank, study, or dataset rows at the installation's
declared dataset grain. Treat variables, participants, samples, files, and ontology terms
as child metadata, not additional datasets. For legacy `molgenis.do` installations, use
their public data-explorer or web-service export only when it exposes a stable collection
listing; do not crawl query results or biological observations as datasets.

**Keep:** catalogue, collection, cohort, biobank, study, or dataset rows at the installation grain. **Drop:** variables, participants, samples, files, ontology terms, and query-result observations.

## BEXIS2 (`bexis2`) {#bexis2}

Use the public BEXIS2 API when the installation enables anonymous access:

```text
GET https://host/api/dataset
GET https://host/api/dataset/{id}
GET https://host/api/metadata/{id}
GET https://host/api/data/{id}
```

Type the public dataset list as `bexis2:datasets`. Keep one record per released public **dataset**. Attach its metadata, current version,
data structure, files, and download package as child information or distributions. Do
not emit variables, rows, attachments, metadata schemas, tags, or dataset versions as
independent datasets. Stop when the API requires authentication rather than enumerating
private project data.

**Keep:** one record per released public **dataset**. **Drop:** variables, rows, attachments, metadata schemas, tags, and versions as independent datasets.

## Diversity Workbench (`diversityworkbench`) {#diversityworkbench}

DWB publication interfaces vary by installation. Prefer the catalog's `endpoints[]`, an
operator-provided dataset overview, or a documented BioCASe/ABCD or RDF publication
service. The SNSB pipeline, for example, exposes multiple DWB projects as BioCASe
datasources with stable unit identifiers.

Keep the published **dataset/project** description when the portal provides that grain.
Treat specimens, occurrences, observations, taxon names, agents, measurements, and
stable unit URIs as records within a dataset, not as separate datasets. Do not turn each
DiversityCollection database module or BioCASe mapping into another catalog.

**Keep:** published **dataset/project** descriptions. **Drop:** specimens, occurrences, taxon names, and each DiversityCollection module as extra catalogs.

## Greenstone (`greenstone`) {#greenstone}

Greenstone 3 normally exposes OAI-PMH through the `oaiserver` servlet:

```text
GET https://host/greenstone3/oaiserver?verb=Identify
GET https://host/greenstone3/oaiserver?verb=ListSets
GET https://host/greenstone3/oaiserver?verb=ListRecords&metadataPrefix=oai_dc&set={set}
```

Typical catalog links already include `/greenstone3/library`. Cleanup strips `/greenstone3` (and Greenstone 2 `/greenstone`) so Identify attaches at origin and is not doubled.

For Greenstone 2, test `/greenstone/cgi-bin/oaiserver.cgi` instead. Map OAI sets to
Greenstone collections, then keep resource records at the catalog's declared document or
dataset grain. Do not emit search-result pages, classifiers, sections, or files belonging
to the same record as additional datasets. Follow `resumptionToken` pagination.

**Keep:** OAI resource records at the catalog’s document or dataset grain. **Drop:** search-result pages, classifiers, sections, and files belonging to the same record.

Greenstone 2 Identify is `/greenstone/cgi-bin/oaiserver.cgi?verb=Identify`.

## VIVO (`vivo`) {#vivo}

Use a public SPARQL Query API or the configured Data Distribution API rather than scraping
faceted HTML:

```text
POST https://host/api/sparqlQuery
GET  https://host/api/dataRequest/...    # only when the installation documents it
```

First inspect the deployment ontology and identify classes that genuinely represent
datasets, data catalogs, repositories, studies, or research objects with downloadable
data. Keep those entities and their stable URIs. Drop people, organizations, grants,
events, publications without data, and graph relationship rows. VIVO installations are
often profiles-only; stop if no dataset-bearing class exists.

**Keep:** SPARQL entities that represent datasets, data catalogs, studies, or research objects with downloadable data. **Drop:** people, organizations, grants, events, and publications without data.

## CWIS (`cwis`) {#cwis}

The included CWIS OAI-PMH plugin can auto-detect OAI requests at the site base URL:

```text
GET https://host/?verb=Identify
GET https://host/?verb=ListSets
GET https://host/?verb=ListRecords&metadataPrefix=oai_dc
```

If the base URL does not respond, use the OAI link advertised by the installation. Keep
public CWIS resource records and preserve the site-defined metadata fields as source
metadata. Drop folders, navigation pages, tags, ratings, comments, and saved-search pages.
Use `set` filters and `resumptionToken` pagination for selective or bulk harvesting.

**Keep:** public CWIS **resource records**. **Drop:** folders, navigation, tags, ratings, comments, and saved-search pages.

## OPeNDAP (`opendap`) {#opendap}

OPeNDAP directory or implementation-specific catalog. Harvest dataset nodes in the catalog, not every `.nc` URL. If the same host is THREDDS, ERDDAP, Pydap, or OPeNDAP Hyrax, use that more specific software ID and recipe instead.

**Keep:** catalog **dataset nodes**.
**Drop:** every `.nc` URL. If the host is THREDDS, ERDDAP, Pydap, or OPeNDAP Hyrax, use that recipe instead.

```text
GET https://host/opendap/
GET https://host/catalog.xml
```


## OPeNDAP Hyrax (`opendaphyrax`) {#opendaphyrax}

Start with the root directory and its machine-readable catalog:

```text
GET https://host/opendap/
GET https://host/opendap/catalog.xml
```

Recurse catalog or `contents.html` directory nodes and keep data-bearing dataset nodes. Do not emit directory containers, metadata/response variants, or every `.nc` URL as separate datasets. DAP2 and DAP4 response URLs for the same dataset are access distributions, not additional dataset records. If Hyrax is only an alternate service behind a THREDDS or ERDDAP catalog, harvest the primary catalog instead.

**Keep:** catalog dataset nodes on the Hyrax OLFS.
**Drop:** every `.nc` granule URL.

```text
GET https://host/opendap/hyrax/
```


## Axiom portal (`axiomportal`) {#axiomportal}

Axiom Data Science catalogs often sit in front of ERDDAP. Harvest the portal dataset list or the ERDDAP `info/index.json` on that host. Do not scrape map tiles.

**Keep:** portal dataset list or ERDDAP `info/index.json` on that host.
**Drop:** map tiles and individual observation rows.

```text
GET https://host/erddap/info/index.json
```


## OntoPortal (`ontoportal`) {#ontoportal}

```text
GET https://host/ontologies
```

This is an **ontology** catalog (BioPortal-style), not research-data files. Harvest ontology ids only when the user wants vocabularies. Do not treat `/search` term hits as datasets.

**Keep:** ontology ids only when the user wants vocabularies. **Drop:** `/search` term hits as datasets.

## RAMADDA (`ramadda`) {#ramadda}

Folder/entry repository. Harvest **entry** types that are data collections, not every file under a folder. Skip a single file URL as the crawl seed.

**Keep:** entry types that are data collections.
**Drop:** every file under a folder; do not seed the crawl on a single file URL.

```text
GET https://host/repository/entry/show?output=json
```

Type `/repository/entry/show?output=json` as `ramadda:entry-show`. Attach from the catalog origin; strip `/repository` when the link already includes that mount.


## Galaxy (`galaxy`) {#galaxy}

Public **data libraries** are the dataset catalog. Histories, workflows, and job outputs are not. Stop on `401` for user workspaces.

**Keep:** public data libraries.
**Drop:** histories, workflows, and job outputs. Stop on `401` for user workspaces.

```text
GET https://host/api/libraries
```


## FAIRDOM-SEEK (`seek`) {#seek}

```text
GET https://host/data_files.json
GET https://host/assays.json
GET https://host/api
```

Type `/api` as `rest`. Keep **data files** / assays / studies that deposit data. Drop SOP-only pages, documents, and presentations. WorkflowHub uses the same stack — still keep data assets, not every CWL workflow, unless the user asked for workflows. Skip seek4science.org marketing.

**Keep:** **data files** / assays / studies that deposit data. **Drop:** SOP-only pages, documents, presentations, and every CWL workflow unless asked.

## ICAT (`icat`) {#icat}

Facility catalog (REST and/or OAI in `endpoints[]`). Harvest **datasets** / investigations that are data. Skip icatproject.org itself and login-only metadata. Stop on `401`.

**Keep:** investigations / datasets from REST or OAI in `endpoints[]`.
**Drop:** icatproject.org itself, files, and login-only metadata. Stop on `401`.

```text
GET https://host/icat/portlet/
```

Type `/icat/portlet/` as `index`. Attach to the catalog `link`; strip `/icat/portlet` when the link already includes that mount.


## MyTardis (`mytardis`) {#mytardis}

```text
GET https://host/api/v1/dataset/
```

TastyPie `dataset` objects. Drop `datafile` rows when a parent dataset exists. Stop on `401`.

Type `/api/v1/dataset/` as `mytardis:datasets`.

**Keep:** TastyPie **dataset** objects. **Drop:** `datafile` rows when a parent dataset exists.

## InterMine (`intermine`) {#intermine}

```text
GET https://host/service/version
GET https://host/service/query/results?query=...
```

Keep **experiments, publications-with-data, and list/template results that represent datasets**. Drop gene report pages and `/begin.do` UI crawls. Prefer the mine root from the catalog `link`. Skip intermine.org itself.

**Keep:** experiments, publications-with-data, and list/template results that represent datasets. **Drop:** gene report pages and `/begin.do` UI crawls.

Type `/service/version` as `intermine:version`.

## GRIN-Global (`gringlobal`) {#gringlobal}

```text
GET https://host/gringlobal/
```

Type `/gringlobal/` as `index`. Attach from the catalog origin; do not prefix `/gringlobal` again when the link already includes that mount.

Keep accession/taxonomy **catalog exports** (CSV/Excel) and documented web-service lists. Drop individual accession HTML pages as datasets unless the user asked for accession-level harvest. One genebank instance = one harvest scope.

**Keep:** accession/taxonomy **catalog exports** and documented web-service lists. **Drop:** individual accession HTML pages unless accession-level harvest was asked.

## PlutoF (`plutof`) {#plutof}

```text
GET https://api.plutof.ut.ee/v1/
```

Keep published **datasets / DOI records**. Drop occurrence rows, sequences, and taxon pages. Do not harvest UNITE (`unite.ut.ee`) as PlutoF. Stop on `401`.

**Keep:** published **datasets / DOI records**. **Drop:** occurrence rows, sequences, taxon pages, and UNITE.

## JGI Genome Portal (`jgi`) {#jgi}

```text
GET https://host/portal/
```

Keep **genome / transcriptome / comparative projects** listed in the portal download workspace. Drop gene pages, BLAST hits, and login-only workspaces. Do not harvest IMG, GOLD, or `data.jgi.doe.gov` under this id.

**Keep:** genome / transcriptome / comparative **projects**. **Drop:** gene pages, BLAST hits, login-only workspaces, IMG, GOLD, and `data.jgi.doe.gov`.

## cBioPortal (`cbioportal`) {#cbioportal}

```text
GET https://host/api/info
GET https://host/api/studies
```

Type the study catalog as `cbioportal:studies`. Keep **studies**. Drop mutation/CNA rows, patient samples, and a single study view as a crawl seed. One public instance = one harvest scope.

**Keep:** cBioPortal **studies**. **Drop:** mutation/CNA rows, patient samples, and a single study view as a crawl seed.

## CLLD (`clld`) {#clld}

Cross-Linguistic Linked Data apps (`{project}.clld.org`). Harvest the **parameter / dataset catalog** or the published bulk download. Drop individual language-value cells and language report pages. One CLLD app = one harvest scope.

```text
GET https://host/parameters
GET https://host/download
```

Type `/parameters` as `index` when it is the public parameter catalog. Type `/download` as `index` when it is the published bulk-download listing. Prefer `endpoints[]` when present.

**Keep:** parameter / dataset catalog or published bulk download. **Drop:** individual language-value cells and language report pages.

## TalkBank (`talkbank`) {#talkbank}

Spoken-language transcript banks (`{bank}.talkbank.org`). Harvest the **corpus / collection catalog** or published bulk download. Drop individual CHAT transcripts, media files, and speaker pages. One TalkBank collection = one harvest scope.

```text
GET https://host/
GET https://host/data.html
```

Prefer `endpoints[]` when present. AphasiaBank and similar clinical banks may be login-walled (`401`/`403`) — stop; do not guess credentials.

Type `/data.html` as `index`. Strip `data.html` from the catalog `link`.

**Keep:** corpus / collection catalog or published bulk download. **Drop:** individual CHAT transcripts, media files, and speaker pages.

## Pathway Tools (`pathwaytools`) {#pathwaytools}

BioCyc-family Pathway/Genome Databases. Harvest the **organism / PGDB catalog** or published bulk export. Drop gene pages, individual pathway diagrams, and reaction records.

```text
GET https://host/
```

Prefer `endpoints[]` when present. One harvest scope per BioCyc collection or organism database (EcoCyc, MetaCyc, YeastCyc, biocyc.org).

**Keep:** organism / PGDB catalog or published bulk export. **Drop:** gene pages, pathway diagrams, and reaction records.

## IBDC (`ibdc`) {#ibdc}

IBDC domain archives on `ibdc.dbt.gov.in`. Harvest the archive **study / accession catalog**, not sequences, spectra, or image files.

```text
GET https://ibdc.dbt.gov.in/{archive}/
```

Keep submitted studies or datasets listed by the archive UI. Drop a single accession landing page as a crawl seed. One harvest scope per archive path already in the registry.

**Keep:** archive **study / accession catalog**. **Drop:** sequences, spectra, image files, and a single accession landing as a crawl seed.

## Specify Web Portal (`specify`) {#specify}

Start at the registered portal and enumerate its public collections from the UI/configuration.
For Guam: `GET https://specifyportal.uog.edu/`. Its existing registered Solr endpoint is
`https://specifyportal.uog.edu/solr/fishvouchers/select?wt=json&q=*&rows=1`.
Resolve other core names from published configuration; do not enumerate administrative APIs.

The [upstream deployment documentation](https://github.com/specify/webportal-installer)
explains the collection export and Solr model. Dataset-discovery grain is a published collection;
Solr rows are specimens, not independent datasets. Keep collection descriptions and advertised
exports; drop image URLs and map tiles as dataset records. For an explicitly requested specimen
harvest, page the observed public search endpoint and preserve collection and specimen identifiers.

**Keep:** published **collection** descriptions and advertised exports. **Drop:** Solr specimen rows, image URLs, and map tiles as datasets.

## BRAHMS Online (`brahmsonline`) {#brahmsonline}

Start at the registered project, for example
`GET https://herbaria.plants.ox.ac.uk/bol/MAU`, and follow its collection/search links.
The [BRAHMS FAQ](https://herbaria.plants.ox.ac.uk/bol/brahms/support/faq)
distinguishes the separately installed online server from the desktop application.

Keep published collection or taxonomic-project metadata and explicitly advertised downloads.
Dataset grain is the collection/project; specimens, taxa, photographs and map points are member
records. No stable generic public list API was established in this review: inspect actual
public search requests before constructing pagination, and respect project-specific reuse terms.

**Keep:** published collection or taxonomic-project metadata and advertised downloads. **Drop:** specimens, taxa, photographs, and map points as extra datasets.

## LOVD (`lovd`) {#lovd}

Use `GET https://lovd.nl/3.0/public_list` to resolve installation URLs; the software homepage
is not a variant-list API. Start at the selected installation root and its published gene list.
The [LOVD FAQ](https://www.lovd.nl/3.0/faq) documents that installation APIs can be disabled;
verify API availability and consult the linked version-specific manual before harvesting.

Keep database/gene-collection descriptions and public export links. Individual variants and
patient records are not separate datasets. Drop login, submission and curation screens.
A submission API is not evidence of a public harvesting endpoint. No API endpoint is added to
the registry's LOVD network-entry record by this classification change.

**Keep:** database/gene-collection descriptions and public export links. **Drop:** individual variants, patient records, login, and submission/curation screens.

## DaCHS (`dachs`) {#dachs}

Start at the registered homepage and follow the published service roster. For example,
`GET https://dc.g-vo.org/` lists collection services. Verify an advertised TAP endpoint with
`GET https://vo.astron.nl/tap/capabilities` before using it.

Prefer the publishing registry's OAI-PMH resource metadata (`GET https://host/oai.xml?verb=Identify` on DaCHS), or TAP table metadata from
`TAP_SCHEMA.tables` after resolving the site's advertised TAP base URL. Keep published
collections, tables and dataset services with stable IVO identifiers. Drop individual stars,
measurements and image pixels as independent dataset records. Service endpoints and tables
can describe the same collection: preserve their relationship rather than double-counting.
Follow [DaCHS registry guidance](https://docs.g-vo.org/DaCHS/opguide.html) and
[shared protocol recipes](harvest-protocols.md) for paging and metadata formats.

**Keep:** published collections, TAP tables, and dataset services with stable IVO identifiers. **Drop:** individual stars, measurements, and image pixels.

## Daiquiri (`daiquiri`) {#daiquiri}

Start at the registered data portal (for example `GET https://gaia.aip.de/`) and follow its
metadata/schema list and advertised TAP or OAI-PMH links. The
[upstream documentation](https://django-daiquiri.github.io/docs/) describes these interfaces;
route details vary across versions, so resolve them from the live site.

Keep data-release and table metadata, DOIs, descriptions and download links. Dataset grain
is a release or published table; astronomical source rows, query jobs and cutout files are not
separate datasets. Use bounded public queries when metadata is exposed via TAP; do not start
large asynchronous queries merely to discover datasets. Login-only workspaces are not public
catalogs. No guessed endpoints are added by software reassignment.

**Keep:** data-release and table metadata, DOIs, and download links. **Drop:** astronomical source rows, query jobs, cutout files, and login-only workspaces.

## AMBIT (`ambit`) {#ambit}

Start at the registered deployment and its advertised dataset listing. The
[AMBIT API guide](https://ambit.sourceforge.net/api.html) describes resource types;
set an explicit Accept header because HTML and RDF representations differ.

A verified bounded eNanoMapper example is
`GET https://data.enanomapper.net/substance?page=0&pagesize=1`.
This lists substances, not independent datasets. Keep published dataset/study collections
and their substance relationships; drop individual compounds, calculated properties,
prediction jobs and models when the requested output is a dataset catalog. Resolve the
actual dataset-list URL from the deployment, and check pagination response bodies before
iterating. Do not treat every nanomaterial property measurement as a dataset.

**Keep:** published dataset/study collections and their substance relationships. **Drop:** individual compounds, calculated properties, prediction jobs, and models.

## ESIMO (`esimo`) {#esimo}

Start with the node's public information-resource catalog under
`/portal/portal/esimo-user/data`. Prefer an advertised CSW or OAI-PMH endpoint when it is
available and returns metadata records. Keep stable marine and hydrometeorological
resources, their responsible organizations, spatial/temporal coverage, access conditions
and service/download links. Drop portal news, software-register entries, map tiles,
individual measurements and internal application components. Harvest each regional node
as its own source, then deduplicate federated records by the ESIMO resource identifier or
canonical source URL rather than title alone.

```text
GET https://host/portal/portal/esimo-user/data
```

**Keep:** stable marine/hydrometeorological **resources** (coverage, access, service/download links). **Drop:** portal news, software-register entries, map tiles, and individual measurements.

## MINERVA (`minerva`) {#minerva}

Prefer the MINERVA-Net registry API or the instance map list. Keep **registered pathway / disease maps**. Drop individual glyphs, reactions, and overlay files. One harvest scope per public MINERVA instance or the Net registry.

```text
GET https://host/api/projects/
GET https://host/minerva/api/projects/
GET https://minerva-net.lcsb.uni.lu/
```

Type `/api/projects/` as `rest`. Keep **registered pathway / disease maps**. Drop individual glyphs, reactions, and overlay files. One harvest scope per public MINERVA instance or the Net registry.

**Keep:** registered pathway / disease **maps**. **Drop:** individual glyphs, reactions, and overlay files.

## Nextstrain (`nextstrain`) {#nextstrain}

```text
GET https://nextstrain.org/charon/getAvailable
```

Type `/charon/getAvailable` as `rest` on the instance `link`. Do not copy `https://nextstrain.org/charon/getAvailable` onto community or tenant catalogs; that URL belongs only on the Nextstrain hub record. Keep **pathogen / community datasets** in the Nextstrain catalog. Drop individual Auspice narrative slides and per-sample FASTA. One harvest scope per public Nextstrain hub or community catalog.

**Keep:** pathogen / community **datasets**. **Drop:** Auspice narrative slides and per-sample FASTA.

## Materials Cloud (`materialscloud`) {#materialscloud}

```text
GET https://host/explore
```

Harvest the Explore work-graph / curated-dataset catalog. Do not harvest Materials Cloud Archive under this id (that record is `inveniordm`). Keep published Explore entries; drop individual AiiDA node dumps.

Type `/explore` as `index`. Strip `/explore` from the catalog `link`.

**Keep:** published Explore **entries**. **Drop:** individual AiiDA node dumps and Materials Cloud Archive (`inveniordm`).

## OpenKIM (`openkim`) {#openkim}

Keep **interatomic models and verification tests** from the OpenKIM catalog/API. Drop individual LAMMPS input decks when a parent model exists.

```text
GET https://openkim.org/
```

**Keep:** interatomic **models and verification tests**. **Drop:** individual LAMMPS input decks when a parent model exists.

## ChecklistBank (`checklistbank`) {#checklistbank}

```text
GET https://api.checklistbank.org/dataset
```

Keep **checklists / datasets**. Drop taxon pages and name-usage rows. One harvest scope for ChecklistBank (plus any independent deployment).

**Keep:** ChecklistBank **datasets**. **Drop:** taxon-name pages as extra datasets.

## ProteoSAFe (`proteosafe`) {#proteosafe}

```text
GET https://massive.ucsd.edu/ProteoSAFe/datasets.jsp
GET https://gnps.ucsd.edu/
```

Keep **MassIVE / GNPS datasets**. Drop workflow jobs, library spectra, and per-file peak lists. One harvest scope per ProteoSAFe catalog (GNPS vs MassIVE).

**Keep:** MassIVE / GNPS **datasets**. **Drop:** workflow jobs, library spectra, and per-file peak lists.

## CyVerse Data Commons (`cyverse`) {#cyverse}

Keep **DOI curated datasets and community-released collections** listed in Data Commons. Drop authenticated Discovery Environment workspaces and raw iRODS paths.

```text
GET https://datacommons.cyverse.org/
```

**Keep:** DOI curated datasets and community-released collections. **Drop:** authenticated Discovery Environment workspaces and raw iRODS paths.

## Hugging Face (`huggingface`) {#huggingface}

```text
GET https://huggingface.co/api/datasets
```

Type the Hub list as `huggingface:api`. Keep **datasets**. Drop models, Spaces, and per-user repos. One harvest scope for the Hub.

**Keep:** Hub **datasets**. **Drop:** models, Spaces, and per-user repos.

## OpenAlex (`openalex`) {#openalex}

```text
GET https://api.openalex.org/works?per-page=50
```

Keep **works** (or datasets if that was the ask). Drop author and institution entities unless requested. One harvest scope for the hub.

**Keep:** OpenAlex **works** (or datasets if that was the ask). **Drop:** author and institution entities unless requested.

## Wikibase (`wikibase`) {#wikibase}

```text
GET https://www.wikidata.org/wiki/Special:EntityData/Q1.json
GET https://query.wikidata.org/sparql
```

Keep **catalog-level collections** the user asked for (for example data-catalog items), not every Wikidata entity. One harvest scope per public Wikibase.

**Keep:** catalog-level **collections** the user asked for. **Drop:** every Wikidata entity.

## DBpedia Databus (`databus`) {#databus}

Keep **Databus artifacts / datasets**. Drop OIDC login pages and individual file bytes. Do not harvest www.dbpedia.org under this id.

**Keep:** Databus artifacts / datasets.
**Drop:** OIDC login pages, individual file bytes, and www.dbpedia.org.

```text
GET https://databus.dbpedia.org/system/api/search?query=*
```


## MGnify (`mgnify`) {#mgnify}

```text
GET https://www.ebi.ac.uk/metagenomics/api/v1/studies
```

Keep **studies / analyses**. Drop individual reads and contig pages.

**Keep:** MGnify **studies / analyses**. **Drop:** individual reads as extra datasets.

## MetaboLights (`metabolights`) {#metabolights}

```text
GET https://www.ebi.ac.uk/metabolights/ws/studies
```

Keep **studies**. Drop individual metabolite records when a parent study exists.

**Keep:** MetaboLights **studies**. **Drop:** individual assay files under a study.

## BioStudies (`biostudies`) {#biostudies}

```text
GET https://www.ebi.ac.uk/biostudies/api/v1/search
```

Keep **studies**. Drop supplementary file rows as separate datasets.

**Keep:** BioStudies **studies**. **Drop:** every file under a study as a dataset.

## Reactome (`reactome`) {#reactome}

```text
GET https://reactome.org/ContentService/data/pathways/top/9606
```

Keep **pathways**. Drop individual reactions and physical entities.

**Keep:** pathway **catalog** entries. **Drop:** every reaction as a dataset.

## WikiPathways (`wikipathways`) {#wikipathways}

Keep **pathways**. Drop gene nodes and individual GPML glyphs.

**Keep:** pathway records.
**Drop:** gene nodes and individual GPML glyphs.

```text
GET https://www.wikipathways.org/index.php/Special:BrowsePathwaysList
```


## UCSC Genome Browser (`ucscgenomebrowser`) {#ucscgenomebrowser}

Keep **assemblies / public track hubs** listed as catalogs. Drop individual gene predictions and tiles.

**Keep:** assemblies / public track hubs listed as catalogs.
**Drop:** individual gene predictions and tiles.

```text
GET https://api.genome.ucsc.edu/list/ucscGenomes
```


## FlyBase (`flybase`) {#flybase}

Keep **genome / bulk data releases**. Drop per-gene report pages.

**Keep:** genome / bulk data releases.
**Drop:** per-gene report pages.

```text
GET https://flybase.org/downloads
```


## WormBase (`wormbase`) {#wormbase}

Keep **genome / bulk data releases**. Drop per-gene report pages.

**Keep:** genome / bulk data releases.
**Drop:** per-gene report pages.

```text
GET https://wormbase.org/about/release_schedule
```


## iDigBio (`idigbio`) {#idigbio}

```text
GET https://search.idigbio.org/v2/search/records
```

Keep **datasets / collections** when listed; occurrence search hits are the wrong grain ([harvest-biodiversity.md](harvest-biodiversity.md)). Distinct from the iDigBio IPT (`ipt`).

**Keep:** iDigBio **datasets / collections**. **Drop:** occurrence search hits.

## iNaturalist (`inaturalist`) {#inaturalist}

```text
GET https://api.inaturalist.org/v1/observations
```

Keep **projects or export datasets** if that was the ask. Do not treat every observation as a dataset. One harvest scope for the hub.

**Keep:** iNaturalist **projects / export datasets**. **Drop:** per-observation API rows.

## JACQ (`jacq`) {#jacq}

Start at the Virtual Herbaria portal or a participating herbarium's public JACQ search.

```text
GET https://jacq.org/
GET https://api.jacq.org/
```

Keep published **herbarium / collection** catalogs. Drop individual specimen, image, and taxon pages. One harvest scope for the shared portal unless an institution publishes a separate JACQ instance.

**Keep:** herbarium / collection catalogs. **Drop:** specimen, image, and taxon pages.

## NMRShiftDB2 (`nmrshiftdb2`) {#nmrshiftdb2}

Start at the public database instance. Swagger UI is at `/api-docs/` on the Cologne reference install.

```text
GET https://nmrshiftdb.nmr.uni-koeln.de/
GET https://nmrshiftdb.nmr.uni-koeln.de/api-docs/
```

Keep **compound / assigned-spectrum records** as listed by the instance. Drop prediction jobs and per-peak rows as extra datasets.

**Keep:** compound / assigned-spectrum records. **Drop:** prediction jobs and per-peak rows.

## Chemotion Repository (`chemotion`) {#chemotion}

Harvest the public repository, not Chemotion ELN notebooks.

```text
GET https://www.chemotion-repository.net/home/welcome
```

Keep published **samples, reactions, and analytical datasets**. Drop ELN lab notebooks, login, and individual spectrum image files as extra datasets.

**Keep:** published samples, reactions, and analytical datasets. **Drop:** ELN notebooks, login, and spectrum image files.

## Korp (`korp`) {#korp}

Harvest the public Korp UI for one installation. Corpus collections are the dataset grain; KWIC hits are not datasets.

```text
GET https://spraakbanken.gu.se/korp/
GET https://korp.eki.ee/
```

**Keep:** published **corpus collections** in that Korp instance. **Drop:** concordance/KWIC rows, word-picture widgets, and login-only corpora listings that are not a public catalog.

## DANDI Archive (`dandi`) {#dandi}

```text
GET https://api.dandiarchive.org/api/dandisets/
```

Keep **dandisets**. Drop individual NWB assets, blobs, and per-file download URLs as extra datasets. One harvest scope for the archive hub.

**Keep:** dandisets. **Drop:** individual NWB assets and blob download URLs.

Detection uses the documented API host (`https://api.dandiarchive.org/api/dandisets/`); do not concatenate that path onto `dandiarchive.org`.

## CELLxGENE Discover (`cellxgene`) {#cellxgene}

```text
GET https://api.cellxgene.cziscience.com/curation/v1/datasets
```

Keep curated **datasets** from the Discover/Curation API. Drop explorer sessions, embeddings, and Census snapshot files as extra catalogs.

**Keep:** curated Discover datasets. **Drop:** explorer sessions, embeddings, and Census snapshot files.

Detection uses the documented Curation API host (`https://api.cellxgene.cziscience.com/curation/v1/datasets`); do not concatenate that path onto the Discover UI host.

## HydroShare (`hydroshare`) {#hydroshare}

```text
GET https://www.hydroshare.org/hsapi/resource/
```

Type `/hsapi/resource/` as `rest`. Keep **resources** (datasets, models, collections). Drop user profiles, group pages, and the companion THREDDS catalog (`threddshydroshareorg`) as extra HydroShare datasets.

**Keep:** HydroShare **resources**. **Drop:** user/group pages and THREDDS service rows.

## Brainlife (`brainlife`) {#brainlife}

```text
GET https://brainlife.io/datasets
```

Keep published **datasets**. Drop processing-app runs, JWT-only warehouse dumps, and per-object provenance events.

**Keep:** published datasets. **Drop:** app runs and login-only warehouse dumps.

## Open Context (`opencontext`) {#opencontext}

```text
GET https://opencontext.org/
```

Keep **projects / published datasets**. Drop individual media items, images, and map points as extra datasets.

**Keep:** projects / published datasets. **Drop:** per-item media, images, and map points.

## BioDare2 (`biodare2`) {#biodare2}

```text
GET https://biodare2.ed.ac.uk/api/experiments?showPublic=true
```

Keep public **experiments** (`isOpenAccess`). Drop period-analysis jobs, rhythmicity jobs, attachments, and login-only drafts.

Type `/api/experiments?showPublic=true` as `rest`. One community hub (`biodare2.ed.ac.uk`).

**Keep:** public experiments. **Drop:** analysis jobs, attachments, and login-only drafts.

## TemplateFlow (`templateflow`) {#templateflow}

```text
GET https://www.templateflow.org/browse/
```

Keep **templates / atlases** in the archive. Drop Python-client cache files, DataLad submodule clones, and individual NIfTI derivatives as extra datasets.

Type `/browse/` as `index`. One archive hub (`templateflow.org`).

**Keep:** templates / atlases. **Drop:** client cache files and per-file NIfTI derivatives.

## Related

- [harvest.md](harvest.md)
- [harvest-scientific.md](harvest-scientific.md)
- [harvest-biodiversity.md](harvest-biodiversity.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [discovery-scientific-domain.md](discovery-scientific-domain.md)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [agents/harvest.md](agents/harvest.md)
