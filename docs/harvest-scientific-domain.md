# Harvesting domain scientific repositories

Biodiversity, crop, chemistry, facility, and earth-system APIs (`catalog_type: Scientific data repository`). Institutional IRs and CRIS: [harvest-scientific.md](harvest-scientific.md). Overview: [harvest.md](harvest.md). Finding installations: [discovery-scientific-domain.md](discovery-scientific-domain.md).

GET only. Stop on `401`/`403`. Prefer `endpoints[]`.

| Page | Use when |
|------|----------|
| This page | IPT, Symbiota, THREDDS, ERDDAP, Breedbase, Tripal, VEuPathDB, MassBank, ioChem-BD, ESGF, ALA, Galaxy, SEEK, ICAT, MyTardis, InterMine, GRIN-Global, PlutoF, JGI, cBioPortal, CLLD, TalkBank, Pathway Tools, IBDC |
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

## THREDDS (`thredds`) {#thredds}

```text
GET https://host/thredds/catalog.xml
GET https://host/thredds/catalog.html
```

The catalog XML is a **tree**. Recurse `catalogRef`; harvest `dataset` elements that have an ID or OPeNDAP/WMS service — not every nested directory. Do not treat NetCDF files inside a datasetScan as separate catalog records unless they are independently cited. Prefer THREDDS over `opendap` when both exist on the same TDS. Earth-observation grain: [harvest-earthdata.md](harvest-earthdata.md).

## ERDDAP (`erddap`) {#erddap}

```text
GET https://host/erddap/info/index.json
GET https://host/erddap/index.json
```

Each row in `info/index.json` is a dataset (`datasetID`). Drop the `allDatasets` helper table if present. Grid vs table datasets are both in scope.

## Symbiota (`symbiota`) {#symbiota}

Biodiversity collections CMS. Official directory: [symbiota.org/symbiota-portals](https://symbiota.org/symbiota-portals/). Filter exports on `software.id = 'symbiota'`.

```text
GET https://host/collections/index.php
GET https://host/collections/datasets/rsshandler.php
```

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

Path prefixes differ per instance (`/MassBank/` vs MoNA `/rest/`). **Keep:** spectral **records** (or record accessions) as the dataset grain. **Drop:** peak lists inside a record as extra datasets.

## ioChem-BD (`iochembd`) {#iochembd}

Computational chemistry nodes. Browse is DSpace-based; Find is the central index.

```text
GET https://host/rest/items
GET https://host/oai/request?verb=Identify
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

## DataONE (`dataone`) {#dataone}

Harvest the **member node** dataset search (`formatType=DATA` when supported). Do not crawl CN-wide duplicates of nodes already in this registry unless the user asked for the coordinating-node view.

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

## BEXIS2 (`bexis2`) {#bexis2}

Use the public BEXIS2 API when the installation enables anonymous access:

```text
GET https://host/api/dataset
GET https://host/api/dataset/{id}
GET https://host/api/metadata/{id}
GET https://host/api/data/{id}
```

Keep one record per released public **dataset**. Attach its metadata, current version,
data structure, files, and download package as child information or distributions. Do
not emit variables, rows, attachments, metadata schemas, tags, or dataset versions as
independent datasets. Stop when the API requires authentication rather than enumerating
private project data.

## Diversity Workbench (`diversityworkbench`) {#diversityworkbench}

DWB publication interfaces vary by installation. Prefer the catalog's `endpoints[]`, an
operator-provided dataset overview, or a documented BioCASe/ABCD or RDF publication
service. The SNSB pipeline, for example, exposes multiple DWB projects as BioCASe
datasources with stable unit identifiers.

Keep the published **dataset/project** description when the portal provides that grain.
Treat specimens, occurrences, observations, taxon names, agents, measurements, and
stable unit URIs as records within a dataset, not as separate datasets. Do not turn each
DiversityCollection database module or BioCASe mapping into another catalog.

## Greenstone (`greenstone`) {#greenstone}

Greenstone 3 normally exposes OAI-PMH through the `oaiserver` servlet:

```text
GET https://host/greenstone3/oaiserver?verb=Identify
GET https://host/greenstone3/oaiserver?verb=ListSets
GET https://host/greenstone3/oaiserver?verb=ListRecords&metadataPrefix=oai_dc&set={set}
```

For Greenstone 2, test `/greenstone/cgi-bin/oaiserver.cgi` instead. Map OAI sets to
Greenstone collections, then keep resource records at the catalog's declared document or
dataset grain. Do not emit search-result pages, classifiers, sections, or files belonging
to the same record as additional datasets. Follow `resumptionToken` pagination.

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

## OPeNDAP (`opendap`) {#opendap}

OPeNDAP directory or implementation-specific catalog. Harvest dataset nodes in the catalog, not every `.nc` URL. If the same host is THREDDS, ERDDAP, Pydap, or OPeNDAP Hyrax, use that more specific software ID and recipe instead.

## OPeNDAP Hyrax (`opendaphyrax`) {#opendaphyrax}

Start with the root directory and its machine-readable catalog:

```text
GET https://host/opendap/
GET https://host/opendap/catalog.xml
```

Recurse catalog or `contents.html` directory nodes and keep data-bearing dataset nodes. Do not emit directory containers, metadata/response variants, or every `.nc` URL as separate datasets. DAP2 and DAP4 response URLs for the same dataset are access distributions, not additional dataset records. If Hyrax is only an alternate service behind a THREDDS or ERDDAP catalog, harvest the primary catalog instead.

## Axiom portal (`axiomportal`) {#axiomportal}

Axiom Data Science catalogs often sit in front of ERDDAP. Harvest the portal dataset list or the ERDDAP `info/index.json` on that host. Do not scrape map tiles.

## OntoPortal (`ontoportal`) {#ontoportal}

```text
GET https://host/ontologies
```

This is an **ontology** catalog (BioPortal-style), not research-data files. Harvest ontology ids only when the user wants vocabularies. Do not treat `/search` term hits as datasets.

## RAMADDA (`ramadda`) {#ramadda}

Folder/entry repository. Harvest **entry** types that are data collections, not every file under a folder. Skip a single file URL as the crawl seed.

## Galaxy (`galaxy`) {#galaxy}

Public **data libraries** are the dataset catalog. Histories, workflows, and job outputs are not. Stop on `401` for user workspaces.

## FAIRDOM-SEEK (`seek`) {#seek}

```text
GET https://host/data_files.json
GET https://host/assays.json
GET https://host/api
```

Keep **data files** / assays / studies that deposit data. Drop SOP-only pages, documents, and presentations. WorkflowHub uses the same stack — still keep data assets, not every CWL workflow, unless the user asked for workflows. Skip seek4science.org marketing.

## ICAT (`icat`) {#icat}

Facility catalog (REST and/or OAI in `endpoints[]`). Harvest **datasets** / investigations that are data. Skip icatproject.org itself and login-only metadata. Stop on `401`.

## MyTardis (`mytardis`) {#mytardis}

```text
GET https://host/api/v1/dataset/
```

TastyPie `dataset` objects. Drop `datafile` rows when a parent dataset exists. Stop on `401`.

## InterMine (`intermine`) {#intermine}

```text
GET https://host/service/version
GET https://host/service/query/results?query=...
```

Keep **experiments, publications-with-data, and list/template results that represent datasets**. Drop gene report pages and `/begin.do` UI crawls. Prefer the mine root from the catalog `link`. Skip intermine.org itself.

## GRIN-Global (`gringlobal`) {#gringlobal}

```text
GET https://host/gringlobal/
```

Keep accession/taxonomy **catalog exports** (CSV/Excel) and documented web-service lists. Drop individual accession HTML pages as datasets unless the user asked for accession-level harvest. One genebank instance = one harvest scope.

## PlutoF (`plutof`) {#plutof}

```text
GET https://api.plutof.ut.ee/v1/
```

Keep published **datasets / DOI records**. Drop occurrence rows, sequences, and taxon pages. Do not harvest UNITE (`unite.ut.ee`) as PlutoF. Stop on `401`.

## JGI Genome Portal (`jgi`) {#jgi}

```text
GET https://host/portal/
```

Keep **genome / transcriptome / comparative projects** listed in the portal download workspace. Drop gene pages, BLAST hits, and login-only workspaces. Do not harvest IMG, GOLD, or `data.jgi.doe.gov` under this id.

## cBioPortal (`cbioportal`) {#cbioportal}

```text
GET https://host/api/info
GET https://host/api/studies
```

Keep **studies**. Drop mutation/CNA rows, patient samples, and a single study view as a crawl seed. One public instance = one harvest scope.

## CLLD (`clld`) {#clld}

Cross-Linguistic Linked Data apps (`{project}.clld.org`). Harvest the **parameter / dataset catalog** or the published bulk download. Drop individual language-value cells and language report pages. One CLLD app = one harvest scope.

```text
GET https://host/parameters
GET https://host/download
```

Prefer `endpoints[]` when present.

## TalkBank (`talkbank`) {#talkbank}

Spoken-language transcript banks (`{bank}.talkbank.org`). Harvest the **corpus / collection catalog** or published bulk download. Drop individual CHAT transcripts, media files, and speaker pages. One TalkBank collection = one harvest scope.

```text
GET https://host/
GET https://host/data.html
```

Prefer `endpoints[]` when present. AphasiaBank and similar clinical banks may be login-walled (`401`/`403`) — stop; do not guess credentials.

## Pathway Tools (`pathwaytools`) {#pathwaytools}

BioCyc-family Pathway/Genome Databases. Harvest the **organism / PGDB catalog** or published bulk export. Drop gene pages, individual pathway diagrams, and reaction records.

```text
GET https://host/
```

Prefer `endpoints[]` when present. One harvest scope per BioCyc collection or organism database (EcoCyc, MetaCyc, YeastCyc, biocyc.org).

## IBDC (`ibdc`) {#ibdc}

IBDC domain archives on `ibdc.dbt.gov.in`. Harvest the archive **study / accession catalog**, not sequences, spectra, or image files.

```text
GET https://ibdc.dbt.gov.in/{archive}/
```

Keep submitted studies or datasets listed by the archive UI. Drop a single accession landing page as a crawl seed. One harvest scope per archive path already in the registry.

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

## BRAHMS Online (`brahmsonline`) {#brahmsonline}

Start at the registered project, for example
`GET https://herbaria.plants.ox.ac.uk/bol/MAU`, and follow its collection/search links.
The [BRAHMS FAQ](https://herbaria.plants.ox.ac.uk/bol/brahms/support/faq)
distinguishes the separately installed online server from the desktop application.

Keep published collection or taxonomic-project metadata and explicitly advertised downloads.
Dataset grain is the collection/project; specimens, taxa, photographs and map points are member
records. No stable generic public list API was established in this review: inspect actual
public search requests before constructing pagination, and respect project-specific reuse terms.

## LOVD (`lovd`) {#lovd}

Use `GET https://lovd.nl/3.0/public_list` to resolve installation URLs; the software homepage
is not a variant-list API. Start at the selected installation root and its published gene list.
The [LOVD FAQ](https://www.lovd.nl/3.0/faq) documents that installation APIs can be disabled;
verify API availability and consult the linked version-specific manual before harvesting.

Keep database/gene-collection descriptions and public export links. Individual variants and
patient records are not separate datasets. Drop login, submission and curation screens.
A submission API is not evidence of a public harvesting endpoint. No API endpoint is added to
the registry's LOVD network-entry record by this classification change.

## DaCHS (`dachs`) {#dachs}

Start at the registered homepage and follow the published service roster. For example,
`GET https://dc.g-vo.org/` lists collection services. Verify an advertised TAP endpoint with
`GET https://vo.astron.nl/tap/capabilities` before using it.

Prefer the publishing registry's OAI-PMH resource metadata, or TAP table metadata from
`TAP_SCHEMA.tables` after resolving the site's advertised TAP base URL. Keep published
collections, tables and dataset services with stable IVO identifiers. Drop individual stars,
measurements and image pixels as independent dataset records. Service endpoints and tables
can describe the same collection: preserve their relationship rather than double-counting.
Follow [DaCHS registry guidance](https://docs.g-vo.org/DaCHS/opguide.html) and
[shared protocol recipes](harvest-protocols.md) for paging and metadata formats.

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

## ESIMO (`esimo`) {#esimo}

Start with the node's public information-resource catalog under
`/portal/portal/esimo-user/data`. Prefer an advertised CSW or OAI-PMH endpoint when it is
available and returns metadata records. Keep stable marine and hydrometeorological
resources, their responsible organizations, spatial/temporal coverage, access conditions
and service/download links. Drop portal news, software-register entries, map tiles,
individual measurements and internal application components. Harvest each regional node
as its own source, then deduplicate federated records by the ESIMO resource identifier or
canonical source URL rather than title alone.

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
