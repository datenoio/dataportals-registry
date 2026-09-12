"""
URLMAP entries for API-capable software merged into apidetect.py.

Imported by scripts/apidetect.py (DRAFT_CATALOGS_URLMAP, OPENDAP_URLMAP_DRAFT).

Research date: 2026-06-17
Sources: official docs, existing catalog endpoint patterns, registry records.

Confidence tiers:
  A – stable, widely deployed path (recommended for apidetect)
  B – common but deployment-specific (try multiple paths)
  C – auth-required, POST-only, or host-specific (document only / deep mode)
  D – no standard relative API on catalog link (skip or sitemap-only)
"""

# Re-use MIME lists from apidetect.py when merging:
# from apidetect import JSON_MIMETYPES, XML_MIMETYPES, HTML_MIMETYPES

JSON_MIMETYPES = ["application/json", "text/json"]
XML_MIMETYPES = ["application/xml", "text/xml"]
HTML_MIMETYPES = ["text/html"]
PLAIN_MIMETYPES = ["text/plain"]
SPARQL_MIMETYPES = JSON_MIMETYPES + XML_MIMETYPES + [
    "application/sparql-results+json",
    "application/sparql-results+xml",
    "application/sparql-query",
]
SDMX_STRUCTURE_MIMETYPES = XML_MIMETYPES + JSON_MIMETYPES + [
    "application/vnd.sdmx.structure+xml",
    "application/vnd.sdmx.structure+json",
]
OPENSEARCH_MIMETYPES = XML_MIMETYPES + ["application/opensearchdescription+xml"]

# ---------------------------------------------------------------------------
# Tier A – high-confidence probes
# ---------------------------------------------------------------------------

STACSERVER_URLMAP = [
    # STAC API Core (OGC 25-005 / stac-api-spec)
    {
        "id": "stacserverapi",
        "url": "/",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "stacserverapi:collections",
        "url": "/collections",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "stacserverapi:conformance",
        "url": "/conformance",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    # Common when STAC is mounted under /stac
    {
        "id": "stacserverapi:stac-root",
        "url": "/stac",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "stacserverapi:stac-collections",
        "url": "/stac/collections",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

GALAXY_URLMAP = [
    # https://docs.galaxyproject.org/ – GET /api/version (anonymous)
    {
        "id": "galaxy:api",
        "url": "/api/version",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "galaxy:api:configuration",
        "url": "/api/configuration",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "galaxy:libraries",
        "url": "/api/libraries",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

UDATA_URLMAP = [
    # Etalab uData – https://udata.readthedocs.io/
    {
        "id": "udataapi",
        "url": "/api/1/datasets/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "udataapi:organizations",
        "url": "/api/1/organizations/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "dcatap21",
        "url": "/api/1/site/catalog.rdf",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

RASDAMAN_URLMAP = [
    # https://doc.rasdaman.com/stable/05_geo-services-guide.html
    {
        "id": "wcs201",
        "url": "/rasdaman/ows?service=WCS&version=2.0.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.1",
    },
    {
        "id": "wms130",
        "url": "/rasdaman/ows?service=WMS&version=1.3.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
]

FUSIONREGISTRY_URLMAP = [
    # https://fmrwiki.sdmx.io/ – public SDMX REST
    {
        "id": "sdmx:dataflows",
        "url": "/ws/public/sdmxapi/rest/dataflow/all/all/latest?detail=allstubs",
        "accept": "application/vnd.sdmx.structure+json",
        "expected_mime": JSON_MIMETYPES + ["application/vnd.sdmx.structure+json"],
        "is_json": True,
        "version": "2.1",
    },
    {
        "id": "fusionregistry:rest",
        "url": "/ws/rest",
        "expected_mime": JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "fusionregistry:sdmxapi",
        "url": "/ws/public/sdmxapi/rest",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

ARISTOTLEMDR_URLMAP = [
    # https://docs.aristotlemetadata.com/api/rest
    {
        "id": "aristotlemdr:api",
        "url": "/api/v4/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": False,
        "version": "4",
    },
    {
        "id": "aristotlemdr:metadata",
        "url": "/api/v4/metadata/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "4",
    },
]

EVERGIS_URLMAP = [
    # https://everpoint.github.io/api/resources/layer_list.html
    {
        "id": "evergis:layers",
        "url": "/sp/layers?group=public",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "evergis:projects",
        "url": "/sp/projects?group=public",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "evergis:tables",
        "url": "/sp/tables?group=public",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

NEXTGISWEB_URLMAP = [
    # https://docs.nextgis.com/docs_ngweb_dev/doc/developer/
    {
        "id": "nextgisweb:api",
        "url": "/api/resource/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "nextgisweb:pkg-version",
        "url": "/api/component/pyramid/pkg_version",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "nextgisweb:routes",
        "url": "/api/component/pyramid/route",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

VUFIND_URLMAP = [
    # VuFind 9+ REST API; legacy installs use /Search/API
    {
        "id": "vufind:api",
        "url": "/api/v1/search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "vufind:api:legacy",
        "url": "/Search/API?method=search&lookfor=test&type=AllFields",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "openapi",
        "url": "/api?openapi",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

WORDPRESS_URLMAP = [
    {
        "id": "rest",
        "url": "/wp-json/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest:posts",
        "url": "/wp-json/wp/v2/posts",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
    {
        "id": "rest:dataset",
        "url": "/wp-json/wp/v2/dataset",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
]

ONTOPORTAL_URLMAP = [
    # BioPortal / OntoPortal REST – https://data.bioontology.org/documentation
    {
        "id": "rest",
        "url": "/ontologies",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest:search",
        "url": "/search?q=test",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

GBIFPLATFORM_URLMAP = [
    # Registry entries often point at gbif.org data portal; API is on api.gbif.org
    # Probe only works when link host is api.gbif.org
    {
        "id": "gbif:dataset",
        "url": "/v1/dataset",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "gbif:organization",
        "url": "/v1/organization",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

OPENMLORG_URLMAP = [
    {
        "id": "openmlorgapi",
        "url": "/api/v1/json/data/list/data_name/iris/limit/1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

DSPACECRIS_URLMAP = [
    # DSpace 7+ REST (CRIS builds on DSpace)
    {
        "id": "dspace",
        "url": "/server/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "7",
    },
    {
        "id": "dspace:discover",
        "url": "/server/api/discover/search/objects",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "7",
    },
    {
        "id": "oaipmh20",
        "url": "/oai/request?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/server/oai/request?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

# Fill existing empty map in apidetect.py
OPENDAP_URLMAP_DRAFT = [
    {
        "id": "opendap:catalog",
        "url": "/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opendap:dds",
        "url": "/dds/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opendap:opendap",
        "url": "/opendap/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opendap:catalog",
        "url": "/catalog.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opendap:catalog",
        "url": "/opendap/catalog.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

# ---------------------------------------------------------------------------
# Tier B – common patterns with deployment variance
# ---------------------------------------------------------------------------

LIZMAP_URLMAP = [
    # Lizmap proxies QGIS Server – paths vary by install prefix
    {
        "id": "lizmap:service:wms",
        "url": "/index.php/lizmap/service/?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "lizmap:service:wms:alt",
        "url": "/lizmap/www/index.php/lizmap/service/?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wms111",
        "url": "/index.php/lizmap/service/?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.1.1",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
]

MAPBENDER_URLMAP = [
    # https://docs.mapbender.org/current/en/customization/api.html
    {
        "id": "mapbender:api-doc",
        "url": "/api/doc/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "mapbender:api-doc:mb3",
        "url": "/mapbender3/api/doc/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

ALA_URLMAP = [
    # Living Atlases / ALA stack – https://docs.ala.org.au/
    {
        "id": "ala:api",
        "url": "/ws/species/search/auto?q=test&idxType=TAXON&limit=1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ala:collections",
        "url": "/ws/registry/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ala:occurrences",
        "url": "/ws/occurrences/search?q=test&pageSize=1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

OBIBAMICA_URLMAP = [
    # Mica REST – https://micadoc.obiba.org/en/latest/rest/
    {
        "id": "obibamica:api",
        "url": "/studies",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "mica:api",
        "url": "/api/studies",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

COLECTICA_URLMAP = [
    # Swagger UI is the reliable unauthenticated probe; search is POST+auth
    {
        "id": "colectica:api",
        "url": "/swagger/ui",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": "1",
    },
    {
        "id": "colectica:api:swagger",
        "url": "/swagger/v1/swagger.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

GISWEBSE_URLMAP = [
    {
        "id": "wms130",
        "url": "/GISWebServiceSE/service.php?SERVICE=WMS&REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wfs200",
        "url": "/GISWebServiceSE/service.php?SERVICE=WFS&REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.0",
    },
    {
        "id": "wmts100",
        "url": "/GISWebServiceSE/service.php?SERVICE=WMTS&REQUEST=GetCapabilities&VERSION=1.0.0",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
]

POPGIS_URLMAP = [
    # SPC PopGIS deployments expose /api on same host
    {
        "id": "customapi",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "customapi:layers",
        "url": "/api/layers",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

ISIGEO_URLMAP = [
    {
        "id": "openapi",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES + HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

ENTRYSCAPE_URLMAP = [
    {
        "id": "entrystore:search",
        "url": "/store/search",
        "expected_mime": JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "entrystore:search",
        "url": "/store/search?type=dcat:Dataset",
        "expected_mime": JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcatap21",
        "url": "/all.rdf",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

PUBLISHMYDATA_URLMAP = [
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.1",
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

DATAPRESS_URLMAP = [
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.1",
    },
    {
        "id": "ckan",
        "url": "/api/3",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "ckan:package-search",
        "url": "/api/3/action/package_search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "ckan:package-list",
        "url": "/api/3/action/package_list",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "ckan",
        "url": "/api/3/action/package_search?rows=0",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "dcat",
        "url": "/catalog.rdf",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

ISLANDORA_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES
ISLANDORA_URLMAP = [
    # Drupal JSON:API + REST – https://islandora.github.io/documentation/
    {
        "id": "drupal:jsonapi",
        "url": "/jsonapi",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "islandora:rest",
        "url": "/node?_format=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai/request?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai2?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "rest",
        "url": "/solr/select?q=RELS_EXT_hasModel_uri_ms:*Dataset*&wt=json&rows=25",
        "accept": "application/json",
        "expected_mime": ISLANDORA_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

NESSTAR_URLMAP = [
    {
        "id": "nesstar:webview",
        "url": "/webview/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "nesstar:api",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

STATTECH_URLMAP = [
    # .Stat Technology (SDMX/OData varies by agency)
    {
        "id": "stattech:api",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "sdmx-json",
        "url": "/sdmx-json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "sdmx:datastructure",
        "url": "/restsdmx/sdmx.ashx/GetDataStructure/all",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

EUROSTAT_URLMAP = [
    {
        "id": "eurostat:json",
        "url": "/api/dissemination/statistics/1.0/data",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

ECB_URLMAP = [
    {
        "id": "sdmx:data",
        "url": "/service/data",
        "expected_mime": XML_MIMETYPES + JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sdmx:dataflows",
        "url": "/service/dataflow",
        "accept": "application/vnd.sdmx.structure+xml, application/xml, application/json",
        "expected_mime": SDMX_STRUCTURE_MIMETYPES,
        "is_json": False,
        "version": None,
        "absolute_url": "https://data-api.ecb.europa.eu/service/dataflow",
    },
]

DATABISORG_URLMAP = [
    {
        "id": "databisorgapi",
        "url": "/api/v0/search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "0",
    },
]

RAMADDA_URLMAP = [
    # https://ramadda.geoscience.xyz/ – repository API
    {
        "id": "ramadda:api",
        "url": "/repository/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ramadda:entries",
        "url": "/repository/entries?output=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ramadda:entry-show",
        "url": "/repository/entry/show?output=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

HAPLO_URLMAP = [
    {
        "id": "haplo:api",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oaiprovider?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

TABLION_URLMAP = [
    {
        "id": "tablion:api",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

MWMB_URLMAP = [
    # Metadata Browser (MWMB) – typical OAI/REST installs
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "mwmb:api",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

# ---------------------------------------------------------------------------
# Tier C – limited / auth / host-specific (optional deep probes)
# ---------------------------------------------------------------------------

CARTO_URLMAP = [
    # Legacy Carto Builder – only when link is {user}.carto.com
    {
        "id": "carto:sql",
        "url": "/api/v2/sql?q=SELECT%201",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
    {
        "id": "carto:v1",
        "url": "/api/v1/map",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

STRAPI_URLMAP = [
    # Content-type slug unknown – probe common bootstrap endpoints
    {
        "id": "strapi:api",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "strapi:users-permissions",
        "url": "/api/users-permissions/roles",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "strapi:datasets",
        "url": "/api/datasets",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

BITRIX_URLMAP = [
    {
        "id": "bitrix:rest",
        "url": "/rest/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opendata:json",
        "url": "/opendata/opendata.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

CONVERIS_URLMAP = [
    {
        "id": "converis:api",
        "url": "/ws/public/v1/projects",
        "expected_mime": JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": "1",
    },
]

DATALAD_URLMAP = []  # git/annex only – see NO_STANDARD_PROBE

SURVEYSOLUTIONS_URLMAP = [
    {
        "id": "surveysolutions:api",
        "url": "/api/v1/questionnaires",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

OGC_XML_MIMETYPES = XML_MIMETYPES + [
    "application/vnd.ogc.wms_xml",
    "application/vnd.ogc.wfs_xml",
    "application/vnd.ogc.se_xml",
]

GEOMAPFISH_URLMAP = [
    # https://camptocamp.github.io/c2cgeoportal/master/
    {
        "id": "geomapfish:themes",
        "url": "/themes",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "wms111",
        "url": "/mapserv_proxy?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wms130",
        "url": "/mapserv_proxy?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wfs200",
        "url": "/mapserv_proxy?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.0",
    },
    {
        "id": "wmts100",
        "url": "/tiles/1.0.0/WMTSCapabilities.xml",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
]

GETSDIPORTAL_URLMAP = [
    {
        "id": "wms111",
        "url": "/geoserver/ows?service=WMS&version=1.1.1&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wms130",
        "url": "/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wfs100",
        "url": "/geoserver/ows?service=WFS&version=1.0.0&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wfs110",
        "url": "/geoserver/ows?service=WFS&version=1.1.0&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wfs200",
        "url": "/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.0",
    },
    {
        "id": "wcs111",
        "url": "/geoserver/ows?service=WCS&version=1.1.1&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wcs201",
        "url": "/geoserver/ows?service=WCS&version=2.0.1&request=GetCapabilities",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.1",
    },
]

REDATAM_URLMAP = [
    {
        "id": "redatam",
        "url": "/redbin/RpWebEngine.exe/Portal",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "redatam",
        "url": "/RpWebEngine.exe/Portal",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

SCICAT_URLMAP = [
    {
        "id": "scicat:datasets",
        "url": "/api/v3/datasets",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "scicat:datasets",
        "url": "/api/v3/Datasets",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
]

# MapStore2 often sits next to GeoServer; GeoStore REST is on the viewer path.
MAPSTORE_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES + ["application/octet-stream"]
MAPSTORE_URLMAP = GETSDIPORTAL_URLMAP + [
    {
        "id": "mapstore:geostore",
        "url": "/rest/geostore/misc/categories/",
        "expected_mime": XML_MIMETYPES + JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "mapstore:config",
        "url": "/configs/localConfig.json",
        "expected_mime": MAPSTORE_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

# Open SDG publishes indicator JSON at documented, language-prefixed paths:
# https://open-sdg.readthedocs.io/en/latest/faq/
OPENSDG_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES + ["application/octet-stream"]
OPENSDG_URLMAP = [
    {
        "id": "opensdg:data",
        "url": "/data/1-1-1.json",
        "expected_mime": OPENSDG_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensdg:data",
        "url": "/en/data/1-1-1.json",
        "expected_mime": OPENSDG_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensdg:data",
        "url": "/sdg-data/en/data/1-1-1.json",
        "expected_mime": OPENSDG_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensdg:data",
        "url": "/data/1-2-1.json",
        "expected_mime": OPENSDG_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensdg:data",
        "url": "/en/data/1-2-1.json",
        "expected_mime": OPENSDG_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensdg:reporting",
        "url": "/data/reporting.json",
        "expected_mime": OPENSDG_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensdg:reporting-status",
        "url": "/reporting-status",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

TERRIA_URLMAP = [
    {
        "id": "terria:config",
        "url": "/config.json",
        "expected_mime": JSON_MIMETYPES + PLAIN_MIMETYPES + ["application/octet-stream"],
        "is_json": True,
        "version": None,
    },
]

SEEK_URLMAP = [
    {
        "id": "rest",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES + HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "seek:data-files",
        "url": "/data_files.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "seek:assays",
        "url": "/assays.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

SUPERMAPISERVER_URLMAP = [
    {
        "id": "supermap:services",
        "url": "/services.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "supermap:services",
        "url": "/iserver/services.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

# MapGIS IGServer (.NET often :6163, Java often :8089). IGS 1.0 catalog is
# /igs/rest/mrcs/docs; IGS 2.0 lists services at /igs/rest/services.
MAPGIS_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES
MAPGISIGSERVER_URLMAP = [
    {
        "id": "mapgis:docs",
        "url": "/rest/mrcs/docs?f=json",
        "expected_mime": MAPGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "mapgis:docs",
        "url": "/igs/rest/mrcs/docs?f=json",
        "expected_mime": MAPGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "mapgis:services",
        "url": "/rest/services?f=json",
        "expected_mime": MAPGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "mapgis:services",
        "url": "/igs/rest/services?f=json",
        "expected_mime": MAPGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

# Provincial 天地图 nodes sit on SuperMap iServer/iPortal or ArcGIS Server.
# Viewer paths (/map, /jiaozuo/, *.html) are stripped to origin in apidetect.
# Do not probe national t0.tianditu.gov.cn tiles or token-gated JS APIs here.
TIANDITU_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES
TIANDITU_URLMAP = [
    {
        "id": "supermap:services",
        "url": "/iserver/services.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "supermapiportal:services",
        "url": "/iportal/web/services.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:services",
        "url": "/arcgis/rest/services?f=pjson",
        "expected_mime": TIANDITU_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:info",
        "url": "/arcgis/rest/info?f=pjson",
        "expected_mime": TIANDITU_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:services",
        "url": "/OneMapServer/rest/services?f=pjson",
        "expected_mime": TIANDITU_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/api/cityNode/queryByTree.json",
        "expected_mime": TIANDITU_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

GVSIGONLINE_URLMAP = GETSDIPORTAL_URLMAP

INGRID_URLMAP = [
    {
        "id": "csw202",
        "url": "/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "csw202",
        "url": "/interface/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
]

ERDASAPOLLO_URLMAP = [
    {
        "id": "wms130",
        "url": "/erdas-iws/ogc/wms/?service=WMS&request=GetCapabilities&version=1.3.0",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wms111",
        "url": "/erdas-iws/ogc/wms/?service=WMS&request=GetCapabilities&version=1.1.1",
        "expected_mime": OGC_XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
]

DRUPAL_JSONAPI_MIMETYPES = JSON_MIMETYPES + ["application/vnd.api+json"]
DRUPAL_URLMAP = [
    {
        "id": "drupal:jsonapi",
        "url": "/jsonapi",
        "accept": "application/vnd.api+json, application/json",
        "expected_mime": DRUPAL_JSONAPI_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "drupal:jsonapi:dataset",
        "url": "/jsonapi/node/dataset",
        "accept": "application/vnd.api+json, application/json",
        "expected_mime": DRUPAL_JSONAPI_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "drupal:jsonapi:dataset",
        "url": "/jsonapi/node/open_data",
        "accept": "application/vnd.api+json, application/json",
        "expected_mime": DRUPAL_JSONAPI_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "drupal:jsonapi:dataset",
        "url": "/jsonapi/node/ckan_dataset",
        "accept": "application/vnd.api+json, application/json",
        "expected_mime": DRUPAL_JSONAPI_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

ICAT_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/oaipmh/request?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "icat:datagateway-api",
        "url": "/datagateway-api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "index",
        "url": "/icat/portlet/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

COGIS_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES
COGIS_URLMAP = [
    {
        "id": "arcgis:rest:services",
        "url": "/elitegis/rest/services?f=pjson",
        "accept": "application/json",
        "expected_mime": COGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:services",
        "url": "/arcgis3/rest/services?f=pjson",
        "accept": "application/json",
        "expected_mime": COGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:services",
        "url": "/arcgisserver/rest/services?f=pjson",
        "accept": "application/json",
        "expected_mime": COGIS_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

GIN_URLMAP = [
    {
        "id": "gogs:api",
        "url": "/api/v1/version",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "gogs:repos-search",
        "url": "/api/v1/repos/search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

OSF_JSONAPI_MIMETYPES = JSON_MIMETYPES + ["application/vnd.api+json"]
OSF_URLMAP = [
    {
        "id": "osf:api",
        "url": "/v2/",
        "absolute_url": "https://api.osf.io/v2/",
        "expected_mime": OSF_JSONAPI_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
]

SAMVERA_URLMAP = [
    {
        "id": "hyrax:catalog",
        "url": "/catalog.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "hyrax:catalog",
        "url": "/catalog",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/catalog/oai?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

SMW_URLMAP = [
    {
        "id": "mediawiki:api",
        "url": "/w/api.php?action=query&meta=siteinfo&format=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "mediawiki:api",
        "url": "/api.php?action=query&meta=siteinfo&format=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "smw:ask",
        "url": "/api.php?action=askargs&format=json&conditions=[[Category:+]]&printouts=Category&parameters=limit=1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "smw:ask",
        "url": "/w/api.php?action=ask&query=[[Category:Dataset]]&format=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "smw:ask",
        "url": "/api.php?action=ask&query=[[Category:Dataset]]&format=json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

ENSEMBL_URLMAP = [
    {
        "id": "rest",
        "url": "/rest/info/ping",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest:species",
        "url": "/rest/info/species",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

PHAIDRA_JSON_MIMETYPES = JSON_MIMETYPES + PLAIN_MIMETYPES
PHAIDRA_URLMAP = [
    {
        "id": "rest",
        "url": "/api/search/select",
        "expected_mime": PHAIDRA_JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/api/search/select?q=cmodel:*Dataset*&wt=json&rows=25",
        "accept": "application/json",
        "expected_mime": PHAIDRA_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/api/search/select?q=dc_type:dataset&wt=json&rows=25",
        "accept": "application/json",
        "expected_mime": PHAIDRA_JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/api/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "openapi",
        "url": "/api/openapi/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "openapi",
        "url": "/api/openapi",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

MAPTILERSERVER_URLMAP = [
    {
        "id": "openapi",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

MYTARDIS_URLMAP = [
    {
        "id": "rest",
        "url": "/api/v1/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "mytardis:datasets",
        "url": "/api/v1/dataset/",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

NYUDATACATALOG_URLMAP = []  # schema.org DataCatalog JSON-LD on the homepage

BREEDBASE_URLMAP = [
    {
        "id": "brapi:serverinfo",
        "url": "/brapi/v2/serverinfo",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
    {
        "id": "brapi:studies",
        "url": "/brapi/v2/studies?page=0&pageSize=1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
    {
        "id": "brapi:trials",
        "url": "/brapi/v2/trials?page=0&pageSize=1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
]

TRIPAL_URLMAP = [
    {
        "id": "tripal:webservices",
        "url": "/web-services/",
        "expected_mime": HTML_MIMETYPES + JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

VEUPATHDB_URLMAP = [
    {
        "id": "veupathdb:webservices",
        "url": "/webservices/",
        "expected_mime": HTML_MIMETYPES + JSON_MIMETYPES + XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

MASSBANK_URLMAP = [
    {
        "id": "massbank:api",
        "url": "/MassBank/api/records",
        "expected_mime": JSON_MIMETYPES + HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "mona:spectra",
        "url": "/rest/spectra",
        "expected_mime": JSON_MIMETYPES + HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

IOCHEMBD_URLMAP = [
    {
        "id": "dspace:items",
        "url": "/rest/items",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "6",
    },
    {
        "id": "oaipmh20",
        "url": "/oai/request?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

ESGF_URLMAP = [
    {
        "id": "esgf:search",
        "url": "/esg-search/search?format=application%2Fsolr%2Bjson&limit=0",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

JSONLD_MIMETYPES = JSON_MIMETYPES + ["application/ld+json"]
TURTLE_MIMETYPES = ["text/turtle", "application/turtle", "application/x-turtle"]
RSS_MIMETYPES = XML_MIMETYPES + ["application/rss+xml", "application/rdf+xml"]

RESOURCECONTRACTS_URLMAP = [
    {
        "id": "custom_api",
        "url": "/contract/resources",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

PIVEAU_URLMAP = [
    {
        "id": "customapi",
        "url": "/api/hub/search",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "customapi",
        "url": "/api/hub/search/search",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "customapi",
        "url": "/api/hub/search/search?q=&filter=dataset",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "customapi",
        "url": "/api/hub/repo/datasets",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "customapi",
        "url": "/api/hub/repo/catalogues",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ckan:package-search",
        "url": "/api/hub/search/ckan/package_search",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "docs",
        "url": "/api/hub/search/",
        "expected_mime": HTML_MIMETYPES + JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sparql",
        "url": "/api/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:ttl",
        "url": "/catalog.ttl",
        "expected_mime": TURTLE_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:xml",
        "url": "/catalog.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

FAIRDATAPOINT_URLMAP = [
    {
        "id": "dcat:ttl",
        "url": "/",
        "accept": "text/turtle",
        "expected_mime": TURTLE_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:jsonld",
        "url": "/",
        "accept": "application/ld+json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "openapi",
        "url": "/v3/api-docs",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3",
    },
    {
        "id": "docs",
        "url": "/swagger-ui.html",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

OMEKAS_URLMAP = [
    {
        "id": "rest",
        "url": "/api",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/api/items",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/api/items?resource_class_label=Dataset",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/api-context",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/omeka/api",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rest",
        "url": "/omeka/api/items",
        "accept": "application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

CONTENTDM_URLMAP = [
    {
        "id": "customapi",
        "url": "/digital/api/collections",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "customapi",
        "url": "/digital/bl/dmwebservices/index.php?q=dmGetCollectionList/json",
        "expected_mime": JSON_MIMETYPES + HTML_MIMETYPES + PLAIN_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai/oai.php?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/digital/oai/oai.php?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

SYMBIOTA_URLMAP = [
    {
        "id": "rss",
        "url": "/collections/datasets/rsshandler.php",
        "expected_mime": RSS_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "rss",
        "url": "/portal/collections/datasets/rsshandler.php",
        "expected_mime": RSS_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "symbiota:collections",
        "url": "/collections/index.php",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "symbiota:collections",
        "url": "/portal/collections/index.php",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "docs",
        "url": "/api/v2/documentation",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": "2",
    },
    {
        "id": "docs",
        "url": "/portal/api/v2/documentation",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": "2",
    },
]

IDRA_URLMAP = [
    {
        "id": "customapi",
        "url": "/Idra/api/v1/administration/version",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "customapi",
        "url": "/Idra/api/v1/catalogues",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]


def _json_probe(url, endpoint_id="customapi", version=None, absolute_url=None, mimes=None):
    item = {
        "id": endpoint_id,
        "url": url,
        "accept": "application/json",
        "expected_mime": mimes or JSON_MIMETYPES,
        "is_json": True,
        "version": version,
    }
    if absolute_url:
        item["absolute_url"] = absolute_url
    return item


def _xml_probe(url, endpoint_id="customapi", version=None, mimes=None, absolute_url=None):
    item = {
        "id": endpoint_id,
        "url": url,
        "expected_mime": mimes or XML_MIMETYPES,
        "is_json": False,
        "version": version,
    }
    if absolute_url:
        item["absolute_url"] = absolute_url
    return item


def _html_probe(url, endpoint_id="customapi", version=None):
    return {
        "id": endpoint_id,
        "url": url,
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": version,
    }


VUFIND_DATASET_SEARCH = (
    '/Search/Results?type=AllFields&filter[]=format%3A"Dataset"'
)
VUFIND_URLMAP.extend(
    [
        _html_probe(VUFIND_DATASET_SEARCH, "index"),
    ]
)
LIBRECAT_URLMAP = list(VUFIND_URLMAP[-1:]) + [
    _xml_probe("/oai?verb=Identify", "oaipmh20", "2.0"),
]


# Harvest-documented relative APIs (2026-09-10). Paths come from harvest-*.md
# GET recipes; do not add hub-only or placeholder URLs.

FROSTSERVER_URLMAP = [
    _json_probe("/v1.1/", "sensorthings", version="1.1"),
    _json_probe("/FROST-Server/v1.1/", "sensorthings", version="1.1"),
    _json_probe("/v1.1/Datastreams?$top=1&$count=true", "sensorthings", version="1.1"),
    _json_probe("/v1.1/Things?$top=1&$count=true", "sensorthings", version="1.1"),
    _json_probe(
        "/FROST-Server/v1.1/Things?$top=1&$count=true", "sensorthings", version="1.1"
    ),
]

GISOPENDATAPORTAL_URLMAP = [
    {
        "id": "dcat:jsonld",
        "url": "/api/opendata/set/catalog/lkod",
        "accept": "application/ld+json, application/json",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

BEXIS2_URLMAP = [_json_probe("/api/dataset", "bexis2:datasets")]

HYDROSHARE_URLMAP = [_json_probe("/hsapi/resource/", "rest")]

CBIOPORTAL_URLMAP = [
    _json_probe("/api/info", "cbioportal:info"),
    _json_probe("/api/studies", "cbioportal:studies"),
]

BIODARE2_URLMAP = [
    _json_probe("/api/experiments?showPublic=true", "rest"),
]

TEMPLATEFLOW_URLMAP = [
    _html_probe("/browse/", "index"),
]

TALKBANK_URLMAP = [
    _html_probe("/data.html", "index"),
]

MATERIALSCLOUD_URLMAP = [
    _html_probe("/explore", "index"),
]

COPERNICUSDHUS_URLMAP = [
    _xml_probe(
        "/odata/v1/Products?$top=1",
        "odata",
        "1",
        XML_MIMETYPES + JSON_MIMETYPES + ["application/atom+xml"],
    ),
]

CUBEWERX_URLMAP = [
    _xml_probe(
        "/cubewerx/cubeserv?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/cubewerx/cubeserv?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
]

CWIS_URLMAP = [
    _xml_probe("/?verb=Identify", "oaipmh20", "2.0"),
]

DJEHUTY_URLMAP = [
    _json_probe("/api/records?size=1", "inveniordmapi:records"),
    _json_probe("/v2/articles", "rest"),
]

OMEGAPSIR_URLMAP = [
    _xml_probe("/oai?verb=Identify", "oaipmh20", "2.0"),
    _xml_probe("/oai/request?verb=Identify", "oaipmh20", "2.0"),
]

EDATOS_URLMAP = [
    _json_probe("/indicators/v1.0/indicators", "rest", version="1.0"),
]

ESASCIENCEARCHIVE_URLMAP = [
    _xml_probe("/tap/capabilities", "tap:capabilities"),
    _xml_probe("/tap-server/tap/capabilities", "tap:capabilities"),
    _xml_probe("/tap/tables", "tap:tables"),
]

GEN3_URLMAP = [
    _json_probe("/_status"),
    _json_probe("/index/ga4gh/drs/v1/service-info"),
]

GIPUZKOAIREKIA_URLMAP = [
    _xml_probe("/catalogo.rdf", "dcat", mimes=XML_MIMETYPES + ["application/rdf+xml"]),
    _xml_probe("/catalog.rdf", "dcatap", mimes=XML_MIMETYPES + ["application/rdf+xml"]),
    _xml_probe("/catalog.xml", "dcat:xml", mimes=XML_MIMETYPES + ["application/rdf+xml"]),
    _json_probe(
        "/catalog.jsonld",
        "dcat:jsonld",
        mimes=JSON_MIMETYPES + ["application/ld+json"],
    ),
    {
        "id": "dcatap201",
        "url": "/api/feed/dcat",
        "expected_mime": XML_MIMETYPES
        + JSON_MIMETYPES
        + ["application/rdf+xml", "application/ld+json"],
        "is_json": False,
        "version": None,
    },
]

DLIBRA_URLMAP = [
    _xml_probe(
        "/dlibra/oai-pmh-repository.xml?verb=Identify",
        "oaipmh20",
        "2.0",
    ),
]

GREENSTONE_URLMAP = [
    _xml_probe("/greenstone3/oaiserver?verb=Identify", "oaipmh20", "2.0"),
    _xml_probe(
        "/greenstone/cgi-bin/oaiserver.cgi?verb=Identify", "oaipmh20", "2.0"
    ),
]

HALECONNECT_URLMAP = [
    _xml_probe(
        "/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/csw?mode=oaipmh&verb=Identify",
        "oaipmh20",
        "2.0",
    ),
    _xml_probe(
        "/ows/services/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
]

INTERMINE_URLMAP = [
    _json_probe("/service/version", "intermine:version"),
]

KADI4MAT_URLMAP = [
    _json_probe("/api/records", "kadi4mat:records"),
    _json_probe("/api/collections", "kadi4mat:collections"),
]

LINKAHEAD_URLMAP = [
    _json_probe("/api/v1/", "rest", version="1"),
]

NOMAD_URLMAP = [
    _json_probe("/prod/v1/api/v1/info", "rest"),
    _json_probe("/prod/v1/api/v1/entries", "rest"),
]

OMERO_URLMAP = [
    _json_probe("/api/v0/m/projects/", "omero:projects", version="0"),
    _html_probe("/webclient/", "omero:webclient"),
]

PALAPA_URLMAP = [
    _xml_probe(
        "/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
]

STACBROWSER_URLMAP = [
    {
        "id": "stac",
        "url": "/catalog.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

SUPERSET_URLMAP = [
    _json_probe("/api/v1/dataset/", "rest", version="1"),
]

VKOMAP_URLMAP = [
    _json_probe("/Public/GetKatoList"),
]

XNAT_URLMAP = [
    _json_probe("/data/projects", "xnat:projects"),
    _json_probe("/xnat/data/projects", "xnat:projects"),
]

ARCHIPELAGO_URLMAP = [
    _xml_probe("/rss.xml", "rss", "2.0", RSS_MIMETYPES),
    _xml_probe("/api/oai_pmh/oai?verb=Identify", "oaipmh20", "2.0"),
    _json_probe("/jsonapi/node/digital_object", "drupal:jsonapi"),
    _html_probe(
        "/search?f[0]=descriptive_metadata_object_types:Dataset", "index"
    ),
]

AVINET_URLMAP = [
    _xml_probe(
        "/wms.ashx?service=WMS&request=GetCapabilities",
        "wms",
        mimes=OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/wfs.ashx?service=WFS&request=GetCapabilities",
        "wfs",
        mimes=OGC_XML_MIMETYPES,
    ),
]

WIKIBASE_URLMAP = [
    _json_probe("/w/api.php?action=query&meta=siteinfo&format=json"),
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sparql",
        "url": "/query/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

DATAFAIR_URLMAP = [_json_probe("/data-fair/api/v1/datasets", "datafairapi")]

QGISSERVER_URLMAP = [
    _xml_probe(
        "/cgi-bin/qgis_mapserv.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/ows?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
]

GC2_URLMAP = [_json_probe("/api/v2/configuration", "rest", version="2")]

DEEGREE_URLMAP = [
    _xml_probe(
        "/services?service=WMS&version=1.3.0&request=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/services?service=CSW&version=2.0.2&request=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/deegree-webservices/services?service=WMS&version=1.3.0&request=GetCapabilities",
        "wms130",
        "1.3.0",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/deegree-webservices/services?service=CSW&version=2.0.2&request=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
]

MICKA_URLMAP = [
    _xml_probe(
        "/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe(
        "/micka/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "csw202",
        "2.0.2",
        OGC_XML_MIMETYPES,
    ),
    _xml_probe("/opensearch", "opensearch", "1.1", OPENSEARCH_MIMETYPES),
    _xml_probe("/micka/opensearch", "opensearch", "1.1", OPENSEARCH_MIMETYPES),
]

LKOD_URLMAP = [
    _xml_probe(
        "/opendata/set/lkod",
        "dcat",
        mimes=XML_MIMETYPES + ["text/turtle", "application/rdf+xml"],
    ),
]

FLAT_URLMAP = [
    _xml_probe("/flat/oai2?verb=Identify", "oaipmh20", "2.0"),
]

OPENEQUELLA_URLMAP = [
    _xml_probe("/oai?verb=Identify", "oaipmh20", "2.0"),
]

DATALIBRARY_URLMAP = [
    _xml_probe("/SOURCES/.catalog"),
]

MVIEWER_URLMAP = [
    _xml_probe("/apps/default.xml"),
]

HUGGINGFACE_URLMAP = [
    _json_probe("/api/datasets?limit=1", "huggingface:api"),
]

OPENALEX_URLMAP = [
    _json_probe(
        "/works?per-page=1",
        absolute_url="https://api.openalex.org/works?per-page=1",
    ),
]

DANDI_URLMAP = [
    _json_probe(
        "/api/dandisets/",
        "rest",
        absolute_url="https://api.dandiarchive.org/api/dandisets/",
    ),
]

CELLXGENE_URLMAP = [
    _json_probe(
        "/curation/v1/datasets",
        "rest",
        absolute_url="https://api.cellxgene.cziscience.com/curation/v1/datasets",
    ),
]

DATAWORLDBANKORG_URLMAP = [
    _json_probe(
        "/v2/indicator?format=json&per_page=1000",
        "rest",
        absolute_url="https://api.worldbank.org/v2/indicator?format=json&per_page=1000",
    ),
    _json_probe(
        "/v2/sources?format=json",
        "rest",
        absolute_url="https://api.worldbank.org/v2/sources?format=json",
    ),
]

OPENAIRE_URLMAP = [
    _json_probe(
        "/search/datasets",
        absolute_url="https://api.openaire.eu/search/datasets",
    ),
]

NEXTSTRAIN_URLMAP = [
    _json_probe("/charon/getAvailable", "rest"),
]

PLUTOF_URLMAP = [
    _json_probe(
        "/v1/",
        version="1",
        absolute_url="https://api.plutof.ut.ee/v1/",
    ),
]

IDIGBIO_URLMAP = [
    _json_probe(
        "/v2/search/records",
        version="2",
        absolute_url="https://search.idigbio.org/v2/search/records",
    ),
]

INATURALIST_URLMAP = [
    _json_probe(
        "/v1/observations?per_page=1",
        version="1",
        absolute_url="https://api.inaturalist.org/v1/observations?per_page=1",
    ),
]

CHECKLISTBANK_URLMAP = [
    _json_probe(
        "/dataset",
        absolute_url="https://api.checklistbank.org/dataset",
    ),
]

BIOSTUDIES_URLMAP = [
    _json_probe(
        "/biostudies/api/v1/search",
        version="1",
        absolute_url="https://www.ebi.ac.uk/biostudies/api/v1/search",
    ),
]

METABOLIGHTS_URLMAP = [
    _json_probe(
        "/metabolights/ws/studies",
        absolute_url="https://www.ebi.ac.uk/metabolights/ws/studies",
    ),
]

MGNIFY_URLMAP = [
    _json_probe(
        "/metagenomics/api/v1/studies",
        version="1",
        absolute_url="https://www.ebi.ac.uk/metagenomics/api/v1/studies",
    ),
]

SENTINELHUB_URLMAP = [
    _json_probe(
        "/api/v1/catalog/1.0.0/collections",
        version="1.0.0",
        absolute_url="https://services.sentinel-hub.com/api/v1/catalog/1.0.0/collections",
    ),
]

UCSCGENOMEBROWSER_URLMAP = [
    _json_probe(
        "/list/ucscGenomes",
        absolute_url="https://api.genome.ucsc.edu/list/ucscGenomes",
    ),
]

SUPERMAPIPORTAL_URLMAP = SUPERMAPISERVER_URLMAP + [
    _json_probe("/iportal/web/services.json", "supermapiportal:services"),
    _json_probe("/iportal/web/maps.json", "supermapiportal:maps"),
    _json_probe("/iportal/web/datas.json", "supermapiportal:datas"),
]

DACHS_URLMAP = [
    _xml_probe("/tap/capabilities", "tap:capabilities"),
    _xml_probe("/__system__/tap/capabilities", "tap:capabilities"),
    _xml_probe("/oai.xml?verb=Identify", "oaipmh20", "2.0"),
]

DIVAPORTAL_URLMAP = [
    _xml_probe("/smash/oai?verb=Identify", "oaipmh20", "2.0"),
    _html_probe("/smash/search.jsf", "index"),
]

DIALNETCRIS_URLMAP = [
    _xml_probe("/oai/openaire?verb=Identify", "oaipmh20", "2.0"),
]

OUROPENDATA_URLMAP = [
    _json_probe("/api/package_list", "ouropendata:packages"),
]

DATAEYE_URLMAP = [
    _json_probe("/api/3/action/status_show", "ckan:status-show"),
    _json_probe("/api/3/action/package_search?rows=0", "ckan:package-search"),
    _json_probe("/ckan_api/package_search", "ckan:package-search"),
    _json_probe("/ckan_api/package_list", "ckan:package-list"),
]

DATABUS_URLMAP = [
    _json_probe(
        "/system/api/search?query=*",
        absolute_url="https://databus.dbpedia.org/system/api/search?query=*",
    ),
]

REACTOME_URLMAP = [
    _json_probe(
        "/ContentService/data/pathways/top/9606",
        absolute_url="https://reactome.org/ContentService/data/pathways/top/9606",
    ),
]

WEBMAPVIEWER_URLMAP = [
    _json_probe(
        "/rest/services/api/MapServer/layersConfig",
        absolute_url="https://api3.geo.admin.ch/rest/services/api/MapServer/layersConfig",
    ),
]

MFGEOADMIN3_URLMAP = [
    _json_probe("/rest/services/api/MapServer/layersConfig"),
    _json_probe("/layersConfig"),
]

DATAHUBPROJECT_URLMAP = [
    {
        "id": "graphql",
        "url": "/api/graphql",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES + ["application/graphql-response+json"],
        "is_json": True,
        "version": None,
    },
]

G3WSUITE_URLMAP = [
    _json_probe("/api/", "g3wsuite:api"),
    _json_probe("/api/group/", "g3wsuite:api"),
    _json_probe("/api/infodata/", "g3wsuite:api"),
    _json_probe("/group/api/", "g3wsuite:group-api"),
]

HUBZERO_URLMAP = [
    _html_probe("/resources?sortby=date"),
]

DGBASWEB_URLMAP = [
    _html_probe("/DgbasWeb/"),
]

SWING_URLMAP = [
    _html_probe("/databank", "swing:databank"),
    _html_probe("/viewer/", "swing:viewer"),
]

IBISPH_URLMAP = [
    _html_probe("/indicator/index/alphabetical"),
]

HAJK_URLMAP = [
    _json_probe("/appConfig.json", "api"),
    _json_probe("/publik/appConfig.json", "api"),
]

CLLD_URLMAP = [
    _json_probe("/parameters.json", "api"),
    _html_probe("/parameters", "index"),
    _html_probe("/download", "index"),
]

MINERVA_URLMAP = [
    _json_probe("/api/projects/", "rest"),
    _json_probe("/minerva/api/projects/", "rest"),
]

TERGIS_URLMAP = [
    _json_probe("/api/v1/classifiers/layers", "other"),
    _json_probe("/themes.json", "qwc2:layers"),
]

AUBREY_URLMAP = [
    _xml_probe("/oai/?verb=Identify", "oaipmh20", "2.0"),
    _json_probe("/api/", "custom_api"),
]

GEONATURE_URLMAP = [
    _json_probe("/api/searchTaxon", "geonature:api"),
    _json_probe("/api/searchCommune", "geonature:api"),
]

GEOCORTEX_URLMAP = [
    {
        "id": "geocortex:catalog",
        "url": "/Geocortex/Essentials/REST/sites?f=pjson",
        "accept": "application/json",
        "expected_mime": PLAIN_MIMETYPES + JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

ACTIVEMAPGIS_URLMAP = [
    _json_probe("/groups/withLayers", "activemapgis:groups"),
]

GRINGLOBAL_URLMAP = [
    _json_probe("/gringlobal/api/v1", "gringlobal:api"),
    _html_probe("/gringlobal/search", "gringlobal:search"),
    _html_probe("/gringlobal/", "index"),
]

SYNAPSE_URLMAP = [
    _json_probe(
        "/repo/v1/version",
        "synapse:api",
        absolute_url="https://repo-prod.prod.sagebase.org/repo/v1/version",
    ),
]

YODA_URLMAP = [
    _xml_probe("/oai/oai?verb=Identify", "oaipmh20", "2.0"),
]

SUPERSTAR_URLMAP = [
    _json_probe("/webapi/rest/v1/schema", "superweb:schema", "1"),
]

DATACUBEWS_URLMAP = [
    _json_probe("/collections", "stacserverapi:collections", "1.0"),
    _json_probe("/collections?f=json", "stacserverapi:collections", "1.0"),
]

CODALAB_URLMAP = [
    _html_probe("/competitions/", "codalab:competitions"),
]

ATMMAGGIOLI_URLMAP = [
    _html_probe("/transparencia/datos/catalogo", "atmmaggioli:catalog"),
]

OPENDATAENTE_URLMAP = [
    {
        "id": "dcat:xml",
        "url": "/backend/api/catalog/",
        "accept": "application/rdf+xml",
        "expected_mime": ["application/rdf+xml", "application/xml", "text/xml"],
        "is_json": False,
        "version": None,
    },
]

ODWEB_URLMAP = [
    _html_probe("/odweb/", "odweb:catalog"),
]

SIMAIOPENDATA_URLMAP = [
    _html_probe("/datasets/", "simaiopendata:catalog"),
]

DUVA_URLMAP = [
    _html_probe("/Informationsportal/", "duva:portal"),
]

BEYOND2020_URLMAP = [
    _html_probe("/ReportFolders/reportFolders.aspx", "beyond2020:reports"),
]

TR32DB_URLMAP = [
    _html_probe("/site/index.php", "tr32db:site"),
]

ORIGO_URLMAP = [
    _json_probe("/index.json", "origo:config"),
    _json_probe("/index_ssl.json", "origo:config"),
]

DATASETTE_URLMAP = [
    _json_probe("/-/databases.json", "datasette:databases"),
]

DATAONE_URLMAP = [
    _xml_probe("/metacat/d1/mn/v2", "rest", "2"),
    _xml_probe("/mn", "rest"),
    _xml_probe("/d1/mn/v2", "rest", "2"),
    _xml_probe("/metacat/sitemaps/sitemap_index.xml", "sitemap"),
]

OPENDATACUBE_URLMAP = [
    _json_probe("/stac", "stacserverapi", "1.0"),
    _json_probe("/stac/", "stacserverapi", "1.0"),
    _json_probe("/stac/collections", "stacserverapi:stac-collections", "1.0"),
    _json_probe("/collections", "stacserverapi:collections", "1.0"),
    _json_probe("/collections?f=json", "stacserverapi:collections", "1.0"),
]

OPENGOV_URLMAP = [
    {
        "id": "opengov:catalog",
        "url": "/transparency",
        "expected_mime": HTML_MIMETYPES + JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opengov:catalog",
        "url": "/data/",
        "expected_mime": HTML_MIMETYPES + JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

# ---------------------------------------------------------------------------
# Proposed CATALOGS_URLMAP additions (merge into apidetect.py)
# ---------------------------------------------------------------------------

DRAFT_CATALOGS_URLMAP = {
    # Tier A
    "stacserver": STACSERVER_URLMAP,
    "galaxy": GALAXY_URLMAP,
    "udata": UDATA_URLMAP,
    "rasdaman": RASDAMAN_URLMAP,
    "fusionregistry": FUSIONREGISTRY_URLMAP,
    "aristotlemdr": ARISTOTLEMDR_URLMAP,
    "nextgisweb": NEXTGISWEB_URLMAP,
    "evergis": EVERGIS_URLMAP,
    "vufind": VUFIND_URLMAP,
    "librecat": LIBRECAT_URLMAP,
    "wordpress": WORDPRESS_URLMAP,
    "ontoportal": ONTOPORTAL_URLMAP,
    "gbifplatform": GBIFPLATFORM_URLMAP,
    "openmlorg": OPENMLORG_URLMAP,
    "dspacecris": DSPACECRIS_URLMAP,
    "geomapfish": GEOMAPFISH_URLMAP,
    "getsdiportal": GETSDIPORTAL_URLMAP,
    "redatam": REDATAM_URLMAP,
    "scicat": SCICAT_URLMAP,
    "mapstore": MAPSTORE_URLMAP,
    "opensdg": OPENSDG_URLMAP,
    "terria": TERRIA_URLMAP,
    "seek": SEEK_URLMAP,
    "supermapiserver": SUPERMAPISERVER_URLMAP,
    "mapgisigserver": MAPGISIGSERVER_URLMAP,
    "tianditu": TIANDITU_URLMAP,
    "gvsigonline": GVSIGONLINE_URLMAP,
    "ingrid": INGRID_URLMAP,
    "erdasapollo": ERDASAPOLLO_URLMAP,
    "drupal": DRUPAL_URLMAP,
    "icat": ICAT_URLMAP,
    "cogis": COGIS_URLMAP,
    "elitegis": COGIS_URLMAP,
    "gin": GIN_URLMAP,
    "osf": OSF_URLMAP,
    "samvera": SAMVERA_URLMAP,
    "smw": SMW_URLMAP,
    "ensembl": ENSEMBL_URLMAP,
    "phaidra": PHAIDRA_URLMAP,
    "maptilerserver": MAPTILERSERVER_URLMAP,
    "mytardis": MYTARDIS_URLMAP,
    "nyudatacatalog": NYUDATACATALOG_URLMAP,
    # Tier B
    "lizmap": LIZMAP_URLMAP,
    "mapbender": MAPBENDER_URLMAP,
    "ala": ALA_URLMAP,
    "obibamica": OBIBAMICA_URLMAP,
    "colectica": COLECTICA_URLMAP,
    "giswebse": GISWEBSE_URLMAP,
    "popgis": POPGIS_URLMAP,
    "isigeo": ISIGEO_URLMAP,
    "entryscape": ENTRYSCAPE_URLMAP,
    "publishmydata": PUBLISHMYDATA_URLMAP,
    "datapress": DATAPRESS_URLMAP,
    "islandora": ISLANDORA_URLMAP,
    "nesstar": NESSTAR_URLMAP,
    "stattech": STATTECH_URLMAP,
    "eurostat": EUROSTAT_URLMAP,
    "ecb": ECB_URLMAP,
    "databisorg": DATABISORG_URLMAP,
    "ramadda": RAMADDA_URLMAP,
    "haplo": HAPLO_URLMAP,
    "tablion": TABLION_URLMAP,
    "mwmb": MWMB_URLMAP,
    # Tier C
    "carto": CARTO_URLMAP,
    "strapi": STRAPI_URLMAP,
    "bitrix": BITRIX_URLMAP,
    "converis": CONVERIS_URLMAP,
    "surveysolutions": SURVEYSOLUTIONS_URLMAP,
    "breedbase": BREEDBASE_URLMAP,
    "tripal": TRIPAL_URLMAP,
    "veupathdb": VEUPATHDB_URLMAP,
    "massbank": MASSBANK_URLMAP,
    "iochembd": IOCHEMBD_URLMAP,
    "esgf": ESGF_URLMAP,
    "resourcecontracts": RESOURCECONTRACTS_URLMAP,
    "piveau": PIVEAU_URLMAP,
    "fairdatapoint": FAIRDATAPOINT_URLMAP,
    "omekas": OMEKAS_URLMAP,
    "contentdm": CONTENTDM_URLMAP,
    "symbiota": SYMBIOTA_URLMAP,
    "idra": IDRA_URLMAP,
    "frostserver": FROSTSERVER_URLMAP,
    "gisopendataportal": GISOPENDATAPORTAL_URLMAP,
    "bexis2": BEXIS2_URLMAP,
    "hydroshare": HYDROSHARE_URLMAP,
    "cbioportal": CBIOPORTAL_URLMAP,
    "biodare2": BIODARE2_URLMAP,
    "templateflow": TEMPLATEFLOW_URLMAP,
    "talkbank": TALKBANK_URLMAP,
    "materialscloud": MATERIALSCLOUD_URLMAP,
    "copernicusdhus": COPERNICUSDHUS_URLMAP,
    "cubewerx": CUBEWERX_URLMAP,
    "cwis": CWIS_URLMAP,
    "djehuty": DJEHUTY_URLMAP,
    "omegapsir": OMEGAPSIR_URLMAP,
    "edatos": EDATOS_URLMAP,
    "esasciencearchive": ESASCIENCEARCHIVE_URLMAP,
    "gen3": GEN3_URLMAP,
    "gipuzkoairekia": GIPUZKOAIREKIA_URLMAP,
    "dlibra": DLIBRA_URLMAP,
    "greenstone": GREENSTONE_URLMAP,
    "haleconnect": HALECONNECT_URLMAP,
    "intermine": INTERMINE_URLMAP,
    "kadi4mat": KADI4MAT_URLMAP,
    "linkahead": LINKAHEAD_URLMAP,
    "nomad": NOMAD_URLMAP,
    "omero": OMERO_URLMAP,
    "palapa": PALAPA_URLMAP,
    "stacbrowser": STACBROWSER_URLMAP,
    "superset": SUPERSET_URLMAP,
    "vkomap": VKOMAP_URLMAP,
    "xnat": XNAT_URLMAP,
    "archipelago": ARCHIPELAGO_URLMAP,
    "avinet": AVINET_URLMAP,
    "wikibase": WIKIBASE_URLMAP,
    "datafair": DATAFAIR_URLMAP,
    "qgisserver": QGISSERVER_URLMAP,
    "gc2": GC2_URLMAP,
    "deegree": DEEGREE_URLMAP,
    "micka": MICKA_URLMAP,
    "lkod": LKOD_URLMAP,
    "flat": FLAT_URLMAP,
    "openequella": OPENEQUELLA_URLMAP,
    "datalibrary": DATALIBRARY_URLMAP,
    "mviewer": MVIEWER_URLMAP,
    "huggingface": HUGGINGFACE_URLMAP,
    "openalex": OPENALEX_URLMAP,
    "dandi": DANDI_URLMAP,
    "cellxgene": CELLXGENE_URLMAP,
    "dataworldbankorg": DATAWORLDBANKORG_URLMAP,
    "openaire": OPENAIRE_URLMAP,
    "nextstrain": NEXTSTRAIN_URLMAP,
    "plutof": PLUTOF_URLMAP,
    "idigbio": IDIGBIO_URLMAP,
    "inaturalist": INATURALIST_URLMAP,
    "checklistbank": CHECKLISTBANK_URLMAP,
    "biostudies": BIOSTUDIES_URLMAP,
    "metabolights": METABOLIGHTS_URLMAP,
    "mgnify": MGNIFY_URLMAP,
    "sentinelhub": SENTINELHUB_URLMAP,
    "ucscgenomebrowser": UCSCGENOMEBROWSER_URLMAP,
    "supermapiportal": SUPERMAPIPORTAL_URLMAP,
    "dachs": DACHS_URLMAP,
    "divaportal": DIVAPORTAL_URLMAP,
    "dialnetcris": DIALNETCRIS_URLMAP,
    "ouropendata": OUROPENDATA_URLMAP,
    "dataeye": DATAEYE_URLMAP,
    "databus": DATABUS_URLMAP,
    "reactome": REACTOME_URLMAP,
    "webmapviewer": WEBMAPVIEWER_URLMAP,
    "mfgeoadmin3": MFGEOADMIN3_URLMAP,
    "datahubproject": DATAHUBPROJECT_URLMAP,
    "g3wsuite": G3WSUITE_URLMAP,
    "hubzero": HUBZERO_URLMAP,
    "dgbasweb": DGBASWEB_URLMAP,
    "swing": SWING_URLMAP,
    "ibisph": IBISPH_URLMAP,
    "hajk": HAJK_URLMAP,
    "clld": CLLD_URLMAP,
    "minerva": MINERVA_URLMAP,
    "tergis": TERGIS_URLMAP,
    "aubrey": AUBREY_URLMAP,
    "geonature": GEONATURE_URLMAP,
    "geocortex": GEOCORTEX_URLMAP,
    "activemapgis": ACTIVEMAPGIS_URLMAP,
    "gringlobal": GRINGLOBAL_URLMAP,
    "synapse": SYNAPSE_URLMAP,
    "yoda": YODA_URLMAP,
    "dataone": DATAONE_URLMAP,
    "opendatacube": OPENDATACUBE_URLMAP,
    "opengov": OPENGOV_URLMAP,
    "superstar": SUPERSTAR_URLMAP,
    "datacubews": DATACUBEWS_URLMAP,
    "codalab": CODALAB_URLMAP,
    "atmmaggioli": ATMMAGGIOLI_URLMAP,
    "opendataente": OPENDATAENTE_URLMAP,
    "odweb": ODWEB_URLMAP,
    "simaiopendata": SIMAIOPENDATA_URLMAP,
    "duva": DUVA_URLMAP,
    "beyond2020": BEYOND2020_URLMAP,
    "tr32db": TR32DB_URLMAP,
    "origo": ORIGO_URLMAP,
    "datasette": DATASETTE_URLMAP,
}

# Software reviewed for auto-fill: do not invent relative API paths.
# Entries that now have a URLMAP were removed from this list.
NO_STANDARD_PROBE = {
    "aodn": "AODN portal search API path varies (/portal/search/api).",
    "axiomportal": "Axiom Data Science portals; instance-specific ERDDAP/API hosts.",
    "cadenza": "disy Cadenza; JSF workbook paths, no stable anonymous catalog API.",
    "chemotion": "Public repository listing is HTML (/home/welcome); no stable relative catalog API.",
    "cardo": "cardo GIS viewers; no shared REST path on the portal URL.",
    "copernicuscds": "CDS retrieve API needs a personal access token, not on catalog link.",
    "d4science": "VRE platform; API behind auth, no stable relative path.",
    "codabench": "Hub /api/datasets/ is 403; homepage HTML is not a catalog dump.",
    "evalai": "Single hub eval.ai; harvest is the challenges UI, not a relative catalog API on other hosts.",
    "grandchallenge": "Single hub grand-challenge.org; /api/v1/ may 403, harvest HTML challenges/archives.",
    "goaltracker": "No verified anonymous list API; catalog link is the tenant homepage.",
    "brahmsonline": "BOL project paths are per-herbarium, not a relative list on every catalog link.",
    "ibdc": "IBDC archive paths are per-archive placeholders, not a relative hub list.",
    "datagovmy": "Static site generators; mostly sitemap-only in records.",
    "datauniceforg": "UNICEF data site; external API not on catalog link.",
    "datavavt": "Custom /analytic/api/v1 on Russian portals.",
    "datawheel": "DataWheel sites; frontend-only, no common /api.",
    "datalad": "DataLad/git annex – no HTTP API on portal link; git-only.",
    "ewmapa": "geoportal2.pl HTML viewers; WMS often 403 and path is instance-specific.",
    "fedora": "Fedora LDP/OAI is behind a public UI; leftover links are not Fedora roots.",
    "gcnavi": "GC Navi municipal viewers; no documented catalog API on the viewer URL.",
    "geogeo": "GeDA-Public / geogeo.jp municipal viewers; no documented catalog API on the viewer URL.",
    "geoloniagis": "Geolonia スマートマップ (Tottori GeoMap, Kagawa BRIDGES); Next.js viewer, no catalog harvest API.",
    "genesisonline": "GENESIS-Online web services are POST-only (Destatis as of mid-2025).",
    "hdc": "Thai HDC public pages are tenant HTML dashboards; no shared relative catalog API on /public/.",
    "brainlife": "Single SaaS hub; harvest is the /datasets UI, not a relative catalog API on other hosts.",
    "cedar": "CEDAR Workbench is a single hub; no relative anonymous catalog dump on the workbench URL.",
    "opencontext": "Open Context is a single hub; harvest is the published project catalog, not a relative list API.",
    "geonomics": "Kazakh municipal GIS; no shared REST path.",
    "geomediawebmap": "Hexagon GeoMedia WebMap; no standard relative catalog API.",
    "geoportalrlp": "Custom geoportal CMS; sitemap only in records.",
    "gisoftgis": "GISoft GIS viewers; no documented public REST on portal URL.",
    "hygmapgis": "HyG Mapgis JSP viewer; layers over ArcGIS REST/WMS, no shared catalog API on mapa.jsp.",
    "ilostat": "ILOSTAT bulk download; no API on www host.",
    "instdb": "Institutional CRIS; generic /api per site.",
    "jacq": "Herbarium REST is on api.jacq.org, not each Virtual Herbaria catalog link.",
    "jdop": "Zhejiang JDOP portals; no documented anonymous default API path.",
    "mangomap": "MangoMap hosted maps; no shared catalog API on /maps URLs.",
    "mapapps": "con terra map.apps; OWS service names are instance-specific.",
    "mapbiomas": "MapBiomas country platforms; no shared catalog API on plataforma URLs.",
    "mapserver": "MapServer CGI/OWS path is instance-specific (not a generic /geomet).",
    "masterportal": "Masterportal config/service JSON names are instance-specific.",
    "modaopendata": "Taiwan MODA OpenAPI swagger path is not present on all city portals.",
    "netgisserver": "NetCAD KEOS/NetGIS; no documented public REST on /keos URLs.",
    "nolis": "NOL-IS municipal viewers; no documented catalog API on the viewer URL.",
    "ogdindia": "OGD Platform India dataset APIs require a registered API key.",
    "opengeoportal": "Legacy OGP; OAI and Solr paths vary.",
    "oportal": "Inspur oPortal; no verified anonymous default API on /oportal URLs.",
    "oracleapex": "APEX apps; no standard API on portal URL.",
    "pomosam": "Slovak eGov CMS; sitemap only, no public API documentation found.",
    "pydap": "PyDAP server root; overlap with opendap/thredds.",
    "reearth": "Re:Earth/PLATEAU VIEW; 3D viewer, no catalog harvest API on the viewer URL.",
    "seoulopendataplaza": "Open API developer space requires a key; sitemaps only on some tenants.",
    "seue": "Catalan seu-e.cat HTML transparency pages, not a machine catalog API.",
    "smartfindersdi": "Custom SDI portals; CSW path varies, sitemap only on most records.",
    "sonicweb": "SonicWeb-Cloud HTML geoportals on sonicweb-asp.jp; no documented catalog API on the viewer URL.",
    "wagmap": "わが街ガイド HTML geoportals; /opendata/ is HTML, not a harvest API.",
    "weboffice": "VertiGIS WebOffice; no standard relative catalog API on the viewer URL.",
    "vertigisstudioweb": "VertiGIS Studio Web viewer; no standard relative catalog API on the viewer URL.",
    "whoint": "WHO website; not a data API on link.",
    "easydb": "easydb 5 / fylr; /api/v1/session is session metadata, not a catalog dump.",
    "rudi": "RUDI portal metadata search needs an authenticate token; node /api/v1/resources is not on the portal host.",
    "onegeosuite": "Explorer catalog UI; no verified anonymous metadata API on the catalog link.",
    "prodige": "GeoNetwork/CSW path is instance-specific; resource API is authenticated.",
    "dlcm": "OAI-PMH lives on the access module host, not the Angular UI link.",
    "molgenis": "EMX2 catalog listing is GraphQL POST; no stable anonymous GET list on the catalog link.",
    "labkey": "Public studies sit behind folder paths; /login/begin.view is not a catalog API.",
    "ipums": "IPUMS collection APIs are collection-specific, not a relative path on the catalog link.",
    "fenix": "FAOSTAT groupsanddomains is one FENIX app; other FENIX UIs have no shared list API.",
    "sparkmap": "No anonymous layer-list API on the public Map Room.",
    "imfnsdp": "NSDP is an HTML country page linking SDMX; no relative catalog API on the page.",
    "datawarehousepro": "Guest databank URLs are tenant-specific paths.",
    "esridataobservatory": "ArcGIS catalog IDs are per InstantAtlas deployment; no universal /api.",
    "liferay": "Open-data module paths vary by Liferay site; no single relative catalog API.",
    "openspending": "Fiscal Data Package list is hub HTML, not a stable relative API on every tenant.",
    "rdfrepository": "Public license tables are HTML; no documented anonymous catalog API.",
    "cadcorp": "Cadcorp SIS WebMap viewer; WMS/layer list is instance-specific.",
    "evrymap": "Evrymap SPA; MapServer map= URL is instance-specific.",
    "geusmap": "GEUSMAP ows path includes a map name; no shared catalog API.",
    "giscloud": "GIS Cloud hosted maps; no shared catalog API on /maps URLs.",
    "gtmap": "GT Map Korean LifeMap viewers; no shared catalog API on the viewer URL.",
    "ishare": "Astun iShare viewer; layer/service paths are instance-specific.",
    "jmap": "JMap viewer; no shared relative catalog API on the viewer URL.",
    "mappenterprise": "M.App Enterprise /Apps/ paths are instance-specific.",
    "pgis": "pGIS Latvian municipal viewers; no shared catalog API.",
    "piso": "PISO municipal GIS; no shared relative catalog API.",
    "shkkbs": "SHK Kent Bilgi Sistemi viewers; no shared catalog API.",
    "xiltrion": "Xiltrion visor; no shared relative catalog API.",
    "geocadgsee": "Geocad System Enterprise Edition; no documented public REST on the portal URL.",
    "ambit": "AMBIT dataset list URL is deployment-specific (eNanoMapper /substance is not portable).",
    "birdmap": "BirdMap API is api.birdmap.africa/{project}/v2/; not on the country portal link.",
    "cyverse": "CyVerse Data Commons listing is HTML; APIs are on separate hosts.",
    "daiquiri": "Daiquiri TAP/OAI paths vary by version; resolve from the live site.",
    "diversityworkbench": "DWB BioCASe/RDF publication paths vary by installation.",
    "edal": "e!DAL list is the HTML home; no stable relative catalog API.",
    "esimo": "ESIMO node APIs are instance-specific.",
    "flybase": "FlyBase downloads are HTML; no relative catalog API on the catalog link.",
    "jgi": "/portal/ is HTML workspace; genome APIs are host-specific.",
    "korp": "Korp corpus list is the instance UI; no shared relative catalog API on every /korp/ path.",
    "loris": "LORIS study portals are HTML; no shared relative catalog API.",
    "lovd": "LOVD public_list is HTML; path varies by install.",
    "metashare": "META-SHARE listing is HTML.",
    "nmrshiftdb2": "REST is documented at /api-docs/ on the Cologne reference install; lab WAR paths vary.",
    "openkim": "OpenKIM catalog is the HTML hub; no relative list API on the catalog link.",
    "pathwaytools": "Pathway Tools web server listing is HTML.",
    "proteosafe": "ProteoSAFe/GNPS/MassIVE list URLs are hub-specific, not on every tenant link.",
    "shanoir": "/shanoir-ng/welcome is HTML, not a catalog API.",
    "specify": "Specify Solr core names are per collection; no shared relative list API.",
    "vivo": "VIVO dataset listing is SPARQL POST; no stable anonymous GET list.",
    "wikipathways": "BrowsePathwaysList is HTML.",
    "wormbase": "WormBase release pages are HTML.",
    "ibmcognos": "IBM Cognos BI package list is login or instance-specific.",
    "statplanet": "StatPlanet data.csv / settings.csv paths are instance-specific.",
    "datainsight": "Public insight dataset lists are rare; most tenants are login-only BI.",
    "bicontour": "Contour BI report catalog paths are instance-specific.",
}

# Map UIs reviewed for auto-fill: no shared relative catalog API on the viewer URL.
NO_STANDARD_PROBE.update(
    {
        sid: "Map UI; no shared catalog API on the viewer URL (harvest-viewers.md)."
        for sid in (
            "3map",
            "addspatial",
            "alandis",
            "alta",
            "arcgisdashboards",
            "argenmap",
            "avanmap",
            "belsisims",
            "berryict",
            "braingeocms",
            "bulplan",
            "cartovista",
            "cgwebgis",
            "communityview",
            "ctmgeo",
            "datumgis",
            "digitaltwincloud",
            "dmcity",
            "doblesvisor",
            "dpwebmap",
            "ekmap",
            "emapa",
            "envimap",
            "evald",
            "experiencebuilder",
            "exponare",
            "factawebgis",
            "farvatergisogd",
            "floodintelligenceportal",
            "gdivisios",
            "genegis",
            "geoambiental",
            "geodeticca",
            "geometa",
            "geonube",
            "geopixel",
            "geoportalch",
            "georeal",
            "geoviewer",
            "gepro",
            "gharyshgeoportal",
            "gis4smart",
            "gis4u",
            "gisapp",
            "giscity",
            "gismaster",
            "gisonline",
            "gisplan",
            "gpatlas",
            "igo2",
            "infogis",
            "infomap",
            "ingeo",
            "ingrada",
            "inkasportal",
            "instantapps",
            "intramaps",
            "iobcina",
            "isymap",
            "k5mapserver",
            "kazgisaopenlayers",
            "kcwebgis",
            "kortinfo",
            "landfolio",
            "localmaps",
            "loftmyndir",
            "louhi",
            "mapguide",
            "mapotip",
            "mapplus",
            "marushka",
            "mobec",
            "mrf",
            "msgis",
            "munisight",
            "mxsig",
            "mycarta",
            "myeongji",
            "nazca",
            "netgisruntime",
            "orbismap",
            "ovie",
            "pmapper",
            "pozi",
            "publicmaps",
            "rgis",
            "sampaswebgis",
            "seasketch",
            "sigimweb",
            "sitwebgis",
            "smartmap",
            "softpro",
            "spatialsuite",
            "spectrumspatial",
            "sputnikweb",
            "terratwin",
            "tobel",
            "touviamaps",
            "trimblelocus",
            "vbgis",
            "vcmap",
            "visorurbano",
            "weave",
            "webappbuilder",
            "webewid",
            "xymaps",
        )
    }
)

# Indicator / BI / story UIs: harvest is the published UI, not a relative list API.
NO_STANDARD_PROBE.update(
    {
        "arcgisstorymaps": "Referenced Feature/Map/Image services are per story item, not a relative catalog API.",
        "cancerrates": "No anonymous REST list API; harvest is the public query UI.",
        "geoclip": "No anonymous list API; indicator tree is the harvest UI.",
        "gxopendata": "Dataset list lives on tenant hostnames; no shared relative catalog API.",
        "hci": "No anonymous list API; harvest public indicator pages.",
        "ihkfachkraeftemonitor": "No anonymous list API; harvest occupation/industry views.",
        "imonitoring": "Krista Open Budget UI; no shared relative catalog API.",
        "instantatlas": "No anonymous list API; harvest InstantAtlas indicators/themes.",
        "jaxi": "No anonymous list API; harvest PC-Axis tables from the menu.do tree.",
        "mats": "MATS Datenportal dashboards; no shared relative catalog API.",
        "powerbi": "Embedded Power BI has no list API; harvest surrounding downloads.",
        "qlik": "Qlik hubs are dashboards; no dataset catalog API on the portal URL.",
        "sharepoint": "Statistics pages are document libraries; no dataset catalog API.",
        "shiny": "Bespoke Shiny apps; no platform catalog API.",
        "tableau": "Tableau vizzes are not a catalog; harvest parent-page downloads.",
        "tabnet": "No REST list API; harvest HTML .def table menus.",
        "webmain": "webMain.aspx sys=/funid= trees are instance-specific; no relative catalog API.",
        "terristory": "Regional hub UI; no shared relative catalog API.",
        "virtuallmi": "No anonymous list API; harvest VLMI profile tables.",
    }
)
