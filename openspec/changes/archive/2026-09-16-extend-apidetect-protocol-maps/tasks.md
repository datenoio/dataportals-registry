## 1. Spec and maps

- [x] 1.1 Add OpenSpec proposal, design, tasks, and api-endpoint-detection delta
- [x] 1.2 Widen `CUSTOM_URLMAP` with DCAT dumps, OAI-PMH, CSW, SPARQL, OpenSearch, RSS/Atom
- [x] 1.3 Add `--include-custom`; keep `infer_endpoints_verified` skip for `custom`
- [x] 1.4 Add CKAN and DataPress OAI-PMH and RDF dump probes
- [x] 1.5 Add GeoNetwork GeoDCAT and OGC API Records probes
- [x] 1.6 Add SPARQL/DCAT dump probes for Piveau, Wikibase, FAIR Data Point, Idra, TriplyDB, PublishMyData
- [x] 1.7 Type FROST probes as `sensorthings`; add deegree `/deegree-webservices/` CSW/WMS
- [x] 1.8 Add `hdc` to `NO_STANDARD_PROBE`

## 2. Tests and docs

- [x] 2.1 Mocked HTTP tests for new probes, custom skip, and `--include-custom`
- [x] 2.2 Update `docs/apidetect.md`, `docs/vocabularies.md`, `docs/data-model.md`
- [x] 2.3 Optional `metadata_support` keys in `software.json`; set Yes on known software YAML
- [x] 2.4 `openspec validate extend-apidetect-protocol-maps --strict`

## 3. Live enrichment

- [x] 3.1 Dry-run then insert `detect-software` for mapped IDs with empty endpoints (lizmap, pure, palapa, dataverse, geoserver, geonature, deegree)
- [x] 3.2 `--action update` backfill CKAN OAI/RDF, GeoNetwork DCAT, IR OAI (DSpace, Dataverse, Invenio/InvenioRDM, Pure), DataPress, SPARQL stacks, deegree
- [x] 3.3 Optional sampled `detect-software custom --include-custom --dryrun`
- [x] 3.4 Validate touched YAML; regenerate `endpoint_types.yaml`
- [x] 3.5 Add harvest-documented OAI Identify for `dspacecris` and `elsevierdigitalcommons`; live `--action update`
- [x] 3.6 Retype TAP (`dachs`, `esasciencearchive`), OData (`copernicusdhus`), pygeoapi collections (`ogc:features`), OpenDataSoft (`opendatasoftapi`); add Hyrax/Samvera `/catalog/oai`, CKAN `/sparql`, ODS DCAT export
- [x] 3.7 Islandora/Archipelago OAI Identify, DataPress SPARQL, Data Fair `datafairapi`, DataEye CKAN-compatible paths, Our Open Data `ouropendata:packages`
- [x] 3.8 Retype cBioPortal (`cbioportal:studies`), Hugging Face (`huggingface:api`), BEXIS2 (`bexis2:datasets`), Djehuty records; Omega-PSIR OAI; DABAR/OpenScience.si alternate Identify; CLLD `/parameters`; HydroShare `/hsapi/resource/`
- [x] 3.9 Retype OMERO (`omero:projects`), SciCat (`scicat:datasets`), Kadi4Mat records/collections, NOMAD/LinkAhead `rest`; add MyTardis `/api/v1/dataset/`, hale»connect WMS, EntryScape Dataset search, Piveau `/api/hub/search`, Omeka S Dataset filter
- [x] 3.10 Retype InterMine (`intermine:version`) and XNAT (`xnat:projects`); add Invenio/InvenioRDM `/oai2d?verb=Identify`, EPrints `/oai2`, DSpace `/oai`, Greenstone 2 OAI, SMW Dataset ask
- [x] 3.11 Add Dataverse `/api/info/version`, Drupal `open_data`/`ckan_dataset` JSON:API, PxWeb `/api/v1/`, OPeNDAP `catalog.xml`, ioChem-BD `/oai`; retype eDatos and Superset as `rest`
- [x] 3.12 Add DSpace `/server/oai/request`, Invenio `/oai`, PxWeb `sv`/`fi`/`da`, CLLD `/download`; retype GC2, Nextstrain, SEEK `/api`, and MINERVA projects as `rest`
- [x] 3.13 Add VuFind/LibreCat Dataset search, Islandora Solr Dataset, Archipelago Dataset search, Figshare `/articles/dataset/`, DiVA smash search, and Pure `de`/`da` dataset RSS
- [x] 3.14 Add Palapa GeoServer WMS, TalkBank `/data.html`, Materials Cloud `/explore`, and ICAT `/icat/portlet/`
- [x] 3.15 Add PHAIDRA Dataset Solr, GRIN-Global `/gringlobal/`, and Esri Geoportal CSW GetCapabilities
- [x] 3.16 Add Islandora Dataset Solr `text/plain`, RAMADDA `/repository` cleanup, and FROST origin Things
- [x] 3.17 Add ERDAS `/erdas-iws`, FROST `/FROST-Server`, CubeWerx `/cubewerx`, and Greenstone `/greenstone3` cleanup
- [x] 3.18 Add Bitrix `/opendata`, MassBank `/MassBank`, NADA `/index.php`, and STAC Browser `/catalog.json` cleanup
- [x] 3.19 Add Micka `/micka`, WIS2 `/oapi`, Symbiota `/portal`, and LKOD `/opendata` cleanup
- [x] 3.20 Add deegree `/deegree-webservices` and FLAT `/flat` cleanup
- [x] 3.21 Add Tianditu city-node tree, ECB SDMX dataflow, World Bank indicator API, DANDI dandiset list, and CELLxGENE Curation datasets
- [x] 3.22 Add EPrints/GeoBlacklight/Micka/TriplyDB OpenSearch, Piveau `/api/sparql`, DaCHS `/oai.xml`, and hale»connect CSW OAI
- [x] 3.23 Add Socrata/GeoNode OpenSearch, GeoNode `/api/v2/datasets/`, ArcGIS Hub `/data.json`, and SuperMap iPortal maps/datas JSON
- [x] 3.24 Add dLibra OAI Identify, Gipuzkoa Irekia tenant DCAT dumps, OpenDataSoft `/data.json`, Esri Geoportal OSDD, Elsevier `/oai`, and WEKO3 OAI Identify
- [x] 3.25 Add pycsw `/?mode=oaipmh`, DKAN `/jsonapi/dataset/dataset`, and LibreCat `/oai` Identify
- [x] 3.26 Add pygeoapi `/collections?f=json`, DataPress CKAN Action paths, VuFind `/api?openapi`, and PHAIDRA `/api/openapi`
- [x] 3.27 Add OpenSDG `/reporting-status/` and `/indicators.json`, DKAN `/api/3`, Aristotle `/api/v4/metadata`, and skip-list `fellesdatakatalog`
- [x] 3.28 Add GeoNetwork `/portal.opensearch`, GET SDI GeoNetwork CSW, and MapStore GeoServer CSW
- [x] 3.29 Add Bitrix `/opendata/` HTML catalog, STAC `/api/stac/v1` extra mount, and stac-fastapi `/api` OpenAPI
- [x] 3.30 Add BIS/ILOSTAT/UNICEF SDMX dataflow `absolute_url` probes; keep `whoint` skip-listed
- [x] 3.31 Add PxWeb table-tree cleanup, ESGF `/search` cleanup, RADAR home cleanup, and Fusion Registry origin probes
- [x] 3.32 Add pycsw and Rasdaman query-on-link GetCapabilities so `/csw` and `/rasdaman/ows` catalog links are not doubled
- [x] 3.33 Add MapServer and QGIS Server query-on-link WMS GetCapabilities so OWS catalog links are not doubled; skip-list `dmaps`
