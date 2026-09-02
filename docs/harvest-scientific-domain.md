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

## OPeNDAP (`opendap`) {#opendap}

Hyrax/OPeNDAP directory or `catalog.xml`. Harvest dataset nodes in the catalog, not every `.nc` URL. If the same host is THREDDS or ERDDAP, use those IDs and recipes instead.

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
