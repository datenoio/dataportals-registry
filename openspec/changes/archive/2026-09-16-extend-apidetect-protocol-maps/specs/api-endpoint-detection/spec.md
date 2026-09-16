## ADDED Requirements

### Requirement: Protocol and catalog dump probes
URL maps MUST probe harvest-documented catalog protocols and dumps for the matching `software.id`, including OAI-PMH Identify, DCAT RDF/XML/Turtle/JSON-LD dumps, SPARQL, CSW GetCapabilities, OGC API Records collections, and OGC SensorThings, when those paths are stable relative to the catalog link.

#### Scenario: CKAN OAI-PMH and RDF dump
- **WHEN** `api_identifier` runs for `software.id` `ckan` and `/oai?verb=Identify` or `/catalog.rdf` returns a matching MIME type
- **THEN** the result includes an `oaipmh20` and/or `dcat` endpoint for that URL

#### Scenario: GeoNetwork GeoDCAT and OGC API Records
- **WHEN** `api_identifier` runs for `geonetwork` and a GeoDCAT RDF or OGC API Records collections path succeeds
- **THEN** the result includes a DCAT and/or `ogcrecordsapi` endpoint

#### Scenario: FROST-Server SensorThings type
- **WHEN** `api_identifier` runs for `frostserver` and `/v1.1/` or `/FROST-Server/v1.1/` succeeds
- **THEN** each matching probe is typed `sensorthings`

#### Scenario: DaCHS and ESA TAP capabilities type
- **WHEN** `api_identifier` runs for `dachs` or `esasciencearchive` and `/tap/capabilities` succeeds
- **THEN** the matching probe is typed `tap:capabilities`

#### Scenario: Copernicus DHuS OData type
- **WHEN** `api_identifier` runs for `copernicusdhus` and `/odata/v1/Products?$top=1` succeeds
- **THEN** the matching probe is typed `odata`

#### Scenario: pygeoapi collections type
- **WHEN** `api_identifier` runs for `pygeoapi` and `/collections/?f=json` succeeds
- **THEN** the matching probe is typed `ogc:features`

#### Scenario: OpenDataSoft API type and DCAT export
- **WHEN** `api_identifier` runs for `opendatasoft` and the explore catalog API or `/api/v2/catalog/exports/dcat` succeeds
- **THEN** catalog API probes are typed `opendatasoftapi`
- **AND** the DCAT export is typed `dcat:xml`

#### Scenario: Hyrax OAI-PMH Identify
- **WHEN** `api_identifier` runs for `hyrax` or `samvera` and `/catalog/oai?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: CKAN SPARQL dump
- **WHEN** `api_identifier` runs for `ckan` and `/sparql` returns a SPARQL MIME type
- **THEN** the result includes a `sparql` endpoint for that URL

#### Scenario: Islandora OAI-PMH Identify
- **WHEN** `api_identifier` runs for `islandora` and `/oai/request?verb=Identify`, `/oai2?verb=Identify`, or `/oai?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: Archipelago OAI-PMH and JSON:API
- **WHEN** `api_identifier` runs for `archipelago` and `/api/oai_pmh/oai?verb=Identify` or `/jsonapi/node/digital_object` succeeds
- **THEN** OAI is typed `oaipmh20` and JSON:API is typed `drupal:jsonapi`

#### Scenario: DataPress SPARQL dump
- **WHEN** `api_identifier` runs for `datapress` and `/sparql` returns a SPARQL MIME type
- **THEN** the result includes a `sparql` endpoint for that URL

#### Scenario: Data Fair API type
- **WHEN** `api_identifier` runs for `datafair` and `/data-fair/api/v1/datasets` succeeds
- **THEN** the matching probe is typed `datafairapi`

#### Scenario: DataEye CKAN-compatible paths
- **WHEN** `api_identifier` runs for `dataeye` and `/api/3/action/status_show` or `/ckan_api/package_search` succeeds
- **THEN** those probes are typed `ckan:status-show` or `ckan:package-search`

#### Scenario: Our Open Data package list type
- **WHEN** `api_identifier` runs for `ouropendata` and `/api/package_list` succeeds
- **THEN** the matching probe is typed `ouropendata:packages`

#### Scenario: cBioPortal studies type
- **WHEN** `api_identifier` runs for `cbioportal` and `/api/studies` succeeds
- **THEN** the matching probe is typed `cbioportal:studies`

#### Scenario: Hugging Face Hub API type
- **WHEN** `api_identifier` runs for `huggingface` and `/api/datasets?limit=1` succeeds
- **THEN** the matching probe is typed `huggingface:api`

#### Scenario: Omega-PSIR OAI-PMH Identify
- **WHEN** `api_identifier` runs for `omegapsir` and `/oai?verb=Identify` or `/oai/request?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: OMERO projects type
- **WHEN** `api_identifier` runs for `omero` and `/api/v0/m/projects/` succeeds
- **THEN** the matching probe is typed `omero:projects`

#### Scenario: SciCat datasets type
- **WHEN** `api_identifier` runs for `scicat` and `/api/v3/datasets` succeeds
- **THEN** the matching probe is typed `scicat:datasets`

#### Scenario: Kadi4Mat records type
- **WHEN** `api_identifier` runs for `kadi4mat` and `/api/records` succeeds
- **THEN** the matching probe is typed `kadi4mat:records`

#### Scenario: hale»connect WMS
- **WHEN** `api_identifier` runs for `haleconnect` and `/ows/services/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities` succeeds
- **THEN** the result includes a `wms130` endpoint for that URL

#### Scenario: MyTardis dataset list
- **WHEN** `api_identifier` runs for `mytardis` and `/api/v1/dataset/` succeeds
- **THEN** the matching probe is typed `mytardis:datasets`

#### Scenario: InterMine version type
- **WHEN** `api_identifier` runs for `intermine` and `/service/version` succeeds
- **THEN** the matching probe is typed `intermine:version`

#### Scenario: XNAT projects type
- **WHEN** `api_identifier` runs for `xnat` and `/data/projects` succeeds
- **THEN** the matching probe is typed `xnat:projects`

#### Scenario: InvenioRDM OAI-PMH Identify
- **WHEN** `api_identifier` runs for `inveniordm` or `invenio` and `/oai2d?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: Dataverse version
- **WHEN** `api_identifier` runs for `dataverse` and `/api/info/version` succeeds
- **THEN** the matching probe is typed `dataverseapi`

#### Scenario: PxWeb API root
- **WHEN** `api_identifier` runs for `pxweb` and `/api/v1/` succeeds
- **THEN** the matching probe is typed `pxwebapi`

#### Scenario: eDatos indicators rest type
- **WHEN** `api_identifier` runs for `edatos` and `/indicators/v1.0/indicators` succeeds
- **THEN** the matching probe is typed `rest`

#### Scenario: OPeNDAP catalog XML
- **WHEN** `api_identifier` runs for `opendap` or `opendaphyrax` and `/opendap/catalog.xml` succeeds
- **THEN** the result includes an `opendap:catalog` endpoint for that URL

#### Scenario: DSpace 7 server OAI-PMH Identify
- **WHEN** `api_identifier` runs for `dspace` and `/server/oai/request?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: Invenio OAI-PMH Identify
- **WHEN** `api_identifier` runs for `invenio` or `inveniordm` and `/oai?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: PxWeb language tree
- **WHEN** `api_identifier` runs for `pxweb` and `/api/v1/sv/` succeeds
- **THEN** the matching probe is typed `pxwebapi`

#### Scenario: GC2 configuration rest type
- **WHEN** `api_identifier` runs for `gc2` and `/api/v2/configuration` succeeds
- **THEN** the matching probe is typed `rest`

#### Scenario: VuFind Dataset search
- **WHEN** `api_identifier` runs for `vufind` or `librecat` and Dataset Search/Results succeeds
- **THEN** the matching probe is typed `index`

#### Scenario: Islandora Solr Dataset
- **WHEN** `api_identifier` runs for `islandora` and `/solr/select` with a Dataset content-model query succeeds
- **THEN** the matching probe is typed `rest`

#### Scenario: Figshare dataset listing
- **WHEN** `api_identifier` runs for `figshare` and `/articles/dataset/` succeeds
- **THEN** the matching probe is typed `index`

#### Scenario: Palapa GeoServer WMS
- **WHEN** `api_identifier` runs for `palapa` and `/geoserver/ows` WMS 1.3.0 GetCapabilities succeeds
- **THEN** the matching probe is typed `wms130`

#### Scenario: TalkBank data listing
- **WHEN** `api_identifier` runs for `talkbank` and `/data.html` succeeds
- **THEN** the matching probe is typed `index`

#### Scenario: Materials Cloud Explore listing
- **WHEN** `api_identifier` runs for `materialscloud` and `/explore` succeeds
- **THEN** the matching probe is typed `index`

#### Scenario: ICAT portlet listing
- **WHEN** `api_identifier` runs for `icat` and `/icat/portlet/` succeeds
- **THEN** the matching probe is typed `index`

#### Scenario: PHAIDRA Dataset Solr
- **WHEN** `api_identifier` runs for `phaidra` and `/api/search/select` with a Dataset cmodel query succeeds
- **THEN** the matching probe is typed `rest`

#### Scenario: GRIN-Global catalog root
- **WHEN** `api_identifier` runs for `gringlobal` and `/gringlobal/` succeeds
- **THEN** the matching probe is typed `index`

#### Scenario: Esri Geoportal CSW GetCapabilities
- **WHEN** `api_identifier` runs for `esrigeo` and `/csw` CSW 2.0.2 GetCapabilities succeeds
- **THEN** the matching probe is typed `csw202`

#### Scenario: Islandora Dataset Solr accepts text/plain
- **WHEN** `api_identifier` runs for `islandora` and `/solr/select?q=RELS_EXT_hasModel_uri_ms:*Dataset*&wt=json&rows=25` returns JSON with Content-Type `text/plain`
- **THEN** the matching probe is typed `rest`

#### Scenario: RAMADDA repository root
- **WHEN** `api_identifier` runs for `ramadda` against a catalog link that already ends in `/repository` and `/repository/entry/show?output=json` succeeds
- **THEN** the result includes that URL once, without `/repository/repository/`

#### Scenario: FROST-Server Things list
- **WHEN** `api_identifier` runs for `frostserver` and `/v1.1/Things?$top=1&$count=true` succeeds
- **THEN** the matching probe is typed `sensorthings`

#### Scenario: FROST-Server servlet root
- **WHEN** `api_identifier` runs for `frostserver` against a catalog link that already ends in `/FROST-Server/` and `/FROST-Server/v1.1/Things?$top=1&$count=true` succeeds
- **THEN** the result includes that URL once, without `/FROST-Server/FROST-Server/`

#### Scenario: ERDAS APOLLO Image Web Server root
- **WHEN** `api_identifier` runs for `erdasapollo` against a catalog link that already ends in `/erdas-iws/` and `/erdas-iws/ogc/wms/` WMS 1.3.0 GetCapabilities succeeds
- **THEN** the result includes that URL once, without `/erdas-iws/erdas-iws/`

#### Scenario: CubeWerx CubeSERV root
- **WHEN** `api_identifier` runs for `cubewerx` against a catalog link that already ends in `/cubewerx/cubeserv` and `/cubewerx/cubeserv` WMS GetCapabilities succeeds
- **THEN** the result includes that URL once, without `/cubewerx/cubeserv/cubewerx/`

#### Scenario: Greenstone library root
- **WHEN** `api_identifier` runs for `greenstone` against a catalog link that already includes `/greenstone3/library` and `/greenstone3/oaiserver?verb=Identify` succeeds
- **THEN** the result includes that URL once, without `/greenstone3/library/greenstone3/`

#### Scenario: Bitrix open-data root
- **WHEN** `api_identifier` runs for `bitrix` against a catalog link that already ends in `/opendata/` and `/opendata/opendata.json` succeeds
- **THEN** the result includes that URL once, without `/opendata/opendata/opendata.json`

#### Scenario: MassBank servlet root
- **WHEN** `api_identifier` runs for `massbank` against a catalog link that already ends in `/MassBank/` and `/MassBank/api/records` succeeds
- **THEN** the result includes that URL once, without `/MassBank/MassBank/`

#### Scenario: NADA index.php root
- **WHEN** `api_identifier` runs for `nada` against a catalog link that already ends in `/index.php` and `/index.php/api/catalog/search` succeeds
- **THEN** the result includes that URL once, without `/index.php/index.php/`

#### Scenario: STAC Browser catalog.json root
- **WHEN** `api_identifier` runs for `stacbrowser` against a catalog link that already ends in `/catalog.json` and `/catalog.json` succeeds
- **THEN** the result includes that URL once, without `/catalog.json/catalog.json`

#### Scenario: Micka CSW root
- **WHEN** `api_identifier` runs for `micka` against a catalog link that already ends in `/micka/` and `/micka/csw` CSW GetCapabilities succeeds
- **THEN** the result includes that URL once, without `/micka/micka/`

#### Scenario: WIS2 Box oapi root
- **WHEN** `api_identifier` runs for `wis20box` against a catalog link that already ends in `/oapi` and `/oapi/collections/?f=json` succeeds
- **THEN** the result includes that URL once, without `/oapi/oapi/`

#### Scenario: Symbiota portal root
- **WHEN** `api_identifier` runs for `symbiota` against a catalog link that already ends in `/portal/` and a collections RSS path succeeds
- **THEN** the result includes that URL once, without `/portal/portal/`

#### Scenario: LKOD open-data dump root
- **WHEN** `api_identifier` runs for `lkod` against a catalog link that already is `/opendata/set/lkod` and that dump succeeds
- **THEN** the result includes that URL once, without `/opendata/opendata/`

#### Scenario: deegree webservices root
- **WHEN** `api_identifier` runs for `deegree` against a catalog link that already ends in `/deegree-webservices/` and `/deegree-webservices/services` CSW GetCapabilities succeeds
- **THEN** the result includes that URL once, without `/deegree-webservices/deegree-webservices/`

#### Scenario: FLAT OAI root
- **WHEN** `api_identifier` runs for `flat` against a catalog link that already ends in `/flat/` and `/flat/oai2?verb=Identify` succeeds
- **THEN** the result includes that URL once, without `/flat/flat/`

#### Scenario: Tianditu city-node tree
- **WHEN** `api_identifier` runs for `tianditu` and `/api/cityNode/queryByTree.json` succeeds
- **THEN** the result includes that URL as a `rest` endpoint

#### Scenario: ECB SDMX dataflow host
- **WHEN** `api_identifier` runs for `ecb` and `https://data-api.ecb.europa.eu/service/dataflow` succeeds
- **THEN** the result includes that URL typed `sdmx:dataflows`
- **AND** it does not concatenate `/service/dataflow` onto `data.ecb.europa.eu`

#### Scenario: World Bank indicator API host
- **WHEN** `api_identifier` runs for `dataworldbankorg` and `https://api.worldbank.org/v2/indicator?format=json&per_page=1000` succeeds
- **THEN** the result includes that URL as a `rest` endpoint

#### Scenario: DANDI and CELLxGENE hub API hosts
- **WHEN** `api_identifier` runs for `dandi` or `cellxgene` and the harvest-documented API host succeeds
- **THEN** the result includes `https://api.dandiarchive.org/api/dandisets/` or `https://api.cellxgene.cziscience.com/curation/v1/datasets` as `rest`

#### Scenario: EPrints OpenSearch description
- **WHEN** `api_identifier` runs for `eprints` and `/cgi/opensearchdescription` succeeds
- **THEN** the result includes that URL typed `opensearch`

#### Scenario: GeoBlacklight catalog OpenSearch
- **WHEN** `api_identifier` runs for `geoblacklight` and `/catalog/opensearch.xml` succeeds
- **THEN** the result includes that URL typed `opensearch`

#### Scenario: Micka OpenSearch
- **WHEN** `api_identifier` runs for `micka` and `/opensearch` or `/micka/opensearch` succeeds
- **THEN** the result includes that URL typed `opensearch`

#### Scenario: Piveau API SPARQL
- **WHEN** `api_identifier` runs for `piveau` and `/api/sparql` succeeds
- **THEN** the result includes that URL typed `sparql`

#### Scenario: DaCHS OAI-PMH Identify
- **WHEN** `api_identifier` runs for `dachs` and `/oai.xml?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: hale»connect CSW OAI-PMH Identify
- **WHEN** `api_identifier` runs for `haleconnect` and `/csw?mode=oaipmh&verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: TriplyDB OpenSearch
- **WHEN** `api_identifier` runs for `triplydb` and `/opensearch.xml` succeeds
- **THEN** the result includes that URL typed `opensearch`

#### Scenario: Socrata OpenSearch
- **WHEN** `api_identifier` runs for `socrata` and `/opensearch.xml` succeeds
- **THEN** the result includes that URL typed `opensearch`

#### Scenario: GeoNode catalogue OpenSearch and v2 datasets
- **WHEN** `api_identifier` runs for `geonode` and `/catalogue/opensearch` or `/api/v2/datasets/` succeeds
- **THEN** the result includes that URL typed `opensearch` or `geonode:datasets`

#### Scenario: ArcGIS Hub data.json
- **WHEN** `api_identifier` runs for `arcgishub` and `/data.json` succeeds
- **THEN** the result includes that URL typed `dcatus11`

#### Scenario: SuperMap iPortal maps and datas JSON
- **WHEN** `api_identifier` runs for `supermapiportal` against a catalog link that already ends in `/iportal` and `/iportal/web/maps.json` succeeds
- **THEN** the result includes that URL once, without `/iportal/iportal/`

#### Scenario: dLibra OAI-PMH Identify
- **WHEN** `api_identifier` runs for `dlibra` against a catalog link that already ends in `/dlibra` and `/dlibra/oai-pmh-repository.xml?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL once, without `/dlibra/dlibra/`

#### Scenario: Gipuzkoa Irekia tenant DCAT dumps
- **WHEN** `api_identifier` runs for `gipuzkoairekia` against a subdomain catalog whose path includes `datu-irekien-katalogoa` and origin `/catalog.xml` succeeds
- **THEN** the result includes the origin dump URL, not a path doubled under `/es/datu-irekien-katalogoa/`
- **AND** when the catalog link is on `www.gipuzkoairekia.eus/es/web/{tenant}/datu-irekien-katalogoa` and `/catalogo.rdf` succeeds
- **THEN** the result keeps the tenant path and does not copy the provincial hub origin dump

#### Scenario: OpenDataSoft data.json
- **WHEN** `api_identifier` runs for `opendatasoft` and `/data.json` succeeds
- **THEN** the result includes that URL typed `dcatus11`

#### Scenario: Esri Geoportal OpenSearch description
- **WHEN** `api_identifier` runs for `esrigeo` against a catalog link that already ends in `/geoportal` and `/geoportal/openSearchDescription` succeeds
- **THEN** the result includes that URL typed `opensearch` once, without `/geoportal/geoportal/`
- **AND** when the catalog link ends in `/search` and `/openSearchDescription` succeeds
- **THEN** the result includes `{link}/openSearchDescription` typed `opensearch`

#### Scenario: Elsevier Digital Commons root OAI-PMH Identify
- **WHEN** `api_identifier` runs for `elsevierdigitalcommons` and `/oai?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: WEKO3 OAI-PMH Identify
- **WHEN** `api_identifier` runs for `weko3` and `/oai?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: pycsw OAI-PMH mode Identify
- **WHEN** `api_identifier` runs for `pycsw` and `/?mode=oaipmh&verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint for that URL

#### Scenario: DKAN Drupal JSON:API dataset entity
- **WHEN** `api_identifier` runs for `dkan` and `/jsonapi/dataset/dataset` succeeds
- **THEN** the result includes that URL typed `drupal:jsonapi`

#### Scenario: LibreCat OAI-PMH Identify from search mount
- **WHEN** `api_identifier` runs for `librecat` against a catalog link that ends in `/search` and origin `/oai?verb=Identify` succeeds
- **THEN** the result includes an `oaipmh20` endpoint at origin, not under `/search/oai`

#### Scenario: pygeoapi collections without trailing slash
- **WHEN** `api_identifier` runs for `pygeoapi` and `/collections?f=json` succeeds
- **THEN** the result includes that URL typed `ogc:features`

#### Scenario: DataPress CKAN package_search
- **WHEN** `api_identifier` runs for `datapress` and `/api/3/action/package_search` succeeds
- **THEN** the result includes that URL typed `ckan:package-search`

#### Scenario: VuFind OpenAPI on /vufind mount
- **WHEN** `api_identifier` runs for `vufind` against a catalog link that already ends in `/vufind` and `/api?openapi` succeeds
- **THEN** the result includes that URL typed `openapi` once, without `/vufind/vufind/`

#### Scenario: PHAIDRA OpenAPI root
- **WHEN** `api_identifier` runs for `phaidra` and `/api/openapi` succeeds
- **THEN** the result includes that URL typed `openapi`

#### Scenario: OpenSDG reporting-status trailing slash
- **WHEN** `api_identifier` runs for `opensdg` and `/reporting-status/` succeeds
- **THEN** the result includes that URL typed `opensdg:reporting-status`

#### Scenario: OpenSDG indicators.json catalog dump
- **WHEN** `api_identifier` runs for `opensdg` and `/indicators.json` succeeds
- **THEN** the result includes that URL typed `opensdg:catalog`

#### Scenario: DKAN CKAN Action API root
- **WHEN** `api_identifier` runs for `dkan` and `/api/3` succeeds
- **THEN** the result includes that URL typed `ckan`

#### Scenario: Aristotle metadata without trailing slash
- **WHEN** `api_identifier` runs for `aristotlemdr` and `/api/v4/metadata` succeeds
- **THEN** the result includes that URL typed `aristotlemdr:metadata`

#### Scenario: GeoNetwork origin portal OpenSearch
- **WHEN** `api_identifier` runs for `geonetwork` and `/portal.opensearch` succeeds
- **THEN** the result includes that URL typed `opensearch`

#### Scenario: GET SDI GeoNetwork CSW
- **WHEN** `api_identifier` runs for `getsdiportal` or `gvsigonline` and `/geonetwork/srv/eng/csw` GetCapabilities succeeds
- **THEN** the result includes that URL typed `csw202`

#### Scenario: MapStore GeoServer CSW
- **WHEN** `api_identifier` runs for `mapstore` and `/geoserver/csw` GetCapabilities succeeds
- **THEN** the result includes that URL typed `csw202`

#### Scenario: Bitrix HTML open-data catalog
- **WHEN** `api_identifier` runs for `bitrix` against a catalog link that already ends in `/opendata` and `/opendata/` succeeds
- **THEN** the result includes that URL typed `bitrix:catalog` once, without `/opendata/opendata/`
- **AND** when the catalog link is a `.php` page without `/opendata` and origin `/opendata/` succeeds
- **THEN** the result includes origin `/opendata/`, not `{php-path}/opendata/`

#### Scenario: STAC Planetary Computer extra mount
- **WHEN** `api_identifier` runs for `stacserver` against an origin catalog link and `/api/stac/v1/` succeeds
- **THEN** the result includes that URL typed `stacserverapi`

#### Scenario: stac-fastapi OpenAPI
- **WHEN** `api_identifier` runs for `stacserver` and `/api` succeeds as JSON
- **THEN** the result includes that URL typed `openapi`

#### Scenario: BIS SDMX dataflow on stats.bis.org
- **WHEN** `api_identifier` runs for `databisorg` against `https://data.bis.org` and `https://stats.bis.org/api/v1/dataflow` succeeds
- **THEN** the result includes that API-host URL typed `sdmx:dataflows`
- **AND** it does not concatenate `/api/v1/dataflow` onto `data.bis.org`

#### Scenario: ILOSTAT SDMX dataflow on sdmx.ilo.org
- **WHEN** `api_identifier` runs for `ilostat` against `https://ilostat.ilo.org` and `https://sdmx.ilo.org/rest/dataflow` succeeds
- **THEN** the result includes that API-host URL typed `sdmx:dataflows`

#### Scenario: UNICEF SDMX dataflow on sdmx.data.unicef.org
- **WHEN** `api_identifier` runs for `datauniceforg` against `https://data.unicef.org` and `https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/dataflow` succeeds
- **THEN** the result includes that API-host URL typed `sdmx:dataflows`

#### Scenario: PxWeb table-tree cleanup
- **WHEN** `api_identifier` runs for `pxweb` against a catalog link that ends in `/PxWeb/pxweb/sv/{db}` and `/PxWeb/api/v1/sv/` succeeds
- **THEN** the result includes that URL typed `pxwebapi`
- **AND** it does not concatenate `/api/v1/` onto `/pxweb/sv/{db}`

#### Scenario: ESGF Metagrid search cleanup
- **WHEN** `api_identifier` runs for `esgf` against a catalog link that ends in `/search` and `/esg-search/search` succeeds
- **THEN** the result includes that origin URL typed `esgf:search`
- **AND** it does not concatenate `/esg-search/search` onto `/search`

#### Scenario: RADAR language home cleanup
- **WHEN** `api_identifier` runs for `radar` against a catalog link that ends in `/radar/en/home` and `/radar/api/datasets` succeeds
- **THEN** the result includes that origin URL typed `radar:datasets`
- **AND** it does not concatenate `/radar/api/datasets` onto `/radar/en/home`

#### Scenario: Fusion Registry origin from mount
- **WHEN** `api_identifier` runs for `fusionregistry` against a catalog link that ends in `/FusionRegistry` and origin `/ws/rest` succeeds
- **THEN** the result includes that origin URL

#### Scenario: pycsw GetCapabilities on a CSW catalog link
- **WHEN** `api_identifier` runs for `pycsw` against a catalog link that ends in `/csw` or `/pycsw` and `?service=CSW&version=2.0.2&request=GetCapabilities` succeeds
- **THEN** the result includes that URL typed `csw202`
- **AND** it does not concatenate `/csw?service=CSW` onto `/csw` or `/pycsw`

#### Scenario: Rasdaman GetCapabilities on an OWS catalog link
- **WHEN** `api_identifier` runs for `rasdaman` against a catalog link that ends in `/rasdaman/ows` and `?service=WCS` succeeds
- **THEN** the result includes that URL typed `wcs201`
- **AND** it does not concatenate `/rasdaman/ows?service=WCS` onto `/rasdaman/ows`

#### Scenario: MapServer GetCapabilities on an OWS catalog link
- **WHEN** `api_identifier` runs for `mapserver` against a catalog link that ends in `/geomet` and `?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities` succeeds
- **THEN** the result includes that URL typed `wms130`
- **AND** it does not concatenate `/geomet` onto `/geomet`

#### Scenario: QGIS Server GetCapabilities on an OWS catalog link
- **WHEN** `api_identifier` runs for `qgisserver` against a catalog link that ends in `/belb` and `?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities` succeeds
- **THEN** the result includes that URL typed `wms130`
- **AND** it does not concatenate `/ows` or `/cgi-bin/qgis_mapserv.fcgi` onto `/belb`

### Requirement: Custom dump map is opt-in
The widened custom dump map MUST NOT be used by quality-fixer inference. CLI detection MUST probe `custom` catalogs only when `--include-custom` is set.

#### Scenario: Quality fixer skips custom
- **WHEN** `infer_endpoints_verified` is called with `software.id` `custom`
- **THEN** it returns an empty list without HTTP probes of dump paths

#### Scenario: CLI requires include-custom
- **WHEN** a detect command processes a `custom` record without `--include-custom`
- **THEN** the record is skipped
- **AND** with `--include-custom` the widened `CUSTOM_URLMAP` is probed

### Requirement: Preferred endpoint type names
New probes MUST use types already common in catalog records: `oaipmh20`, `csw202`, `dcatus11`, `dcatap201`, `dcat:xml`, `dcat:ttl`, `dcat:jsonld`, `stacserverapi`, `socrata:views`, `sparql`, `sensorthings`, `ogcrecordsapi`, `ogc:features`, `tap:capabilities`, `odata`, `opendatasoftapi`, `datafairapi`, `ouropendata:packages`, `ckan:package-search`, `drupal:jsonapi`, `cbioportal:studies`, `huggingface:api`, `inveniordmapi:records`, `omero:projects`, `scicat:datasets`, `kadi4mat:records`, `mytardis:datasets`, `intermine:version`, `xnat:projects`, `dataverseapi`, `pxwebapi`.

#### Scenario: Vocabularies document live types
- **WHEN** a contributor reads `docs/vocabularies.md` endpoint types
- **THEN** preferred names match types used in records
- **AND** unused aliases (`geonetwork:csw`, `socrata:opendata`, bare `oaipmh`, bare `stac`) are listed only as "prefer instead" notes
