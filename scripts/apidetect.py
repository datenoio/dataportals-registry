#!/usr/bin/env python
# This script intended to detect data catalogs API
import logging
import sys
import glob
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
import typer
from typing import Optional
from typing_extensions import Annotated
import re
import requests
from urllib.parse import urljoin
import datetime
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import csv
import json
import os
import shutil
import pprint
from urllib.parse import urlparse, urlunparse
import lxml.html
import lxml.etree
import urllib.robotparser
from requests.exceptions import (
    ConnectionError,
    ContentDecodingError,
    InvalidURL,
    RequestException,
    TooManyRedirects,
)
from urllib3.exceptions import InsecureRequestWarning  # , ConnectionError

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
root = logging.getLogger()
root.setLevel(logging.INFO)


_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
ENTRIES_DIR = os.path.join(_REPO_ROOT, "data", "entities")
SCHEDULED_DIR = os.path.join(_REPO_ROOT, "data", "scheduled")
app = typer.Typer()

DEFAULT_TIMEOUT = 5
DEFAULT_RECORD_WORKERS = 8
DEFAULT_PROBE_WORKERS = 8
_SAVE_LOCK = threading.Lock()

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
)

KML_MIMETYPES = ["application/vnd.google-earth.kml+xml"]
HTML_MIMETYPES = ["text/html", "text/html; charset=UTF-8"]
XML_MIMETYPES = [
    "text/xml",
    "application/xml",
    "application/vnd.ogc.se_xml",
    "application/vnd.ogc.wms_xml",
    "application/rdf+xml",
    "application/rss+xml",
    "application/atom+xml",
    "application/xml;charset=UTF-8",
] + KML_MIMETYPES
JSON_MIMETYPES = [
    "text/json",
    "application/json",
    "application/hal+json",
    "application/vnd.oai.openapi+json;version=3.0; charset=utf-8",
    "application/vnd.oai.openapi+json",
]
N3_MIMETYPES = ["text/n3"]
TURTLE_MIMETYPES = ["text/turtle", "application/turtle", "application/x-turtle"]
JSONLD_MIMETYPES = JSON_MIMETYPES + ["application/ld+json"]
SPARQL_MIMETYPES = (
    JSON_MIMETYPES
    + XML_MIMETYPES
    + [
        "application/sparql-results+json",
        "application/sparql-results+xml",
        "application/sparql-query",
    ]
)
ZIP_MIMETYPES = ["application/zip"]
EXCEL_MIMETYPES = [
    "application/vnd.ms-excel",
]

CSV_MIMETYPES = ["text/csv"]
PLAIN_MIMETYPES = ["text/plain"]
KMZ_MIMETYPES = ["application/vnd.google-earth.kmz"]


GEONETWORK_SEARCH_POST_PARAMS = """{"from":0,"size":20, "bucket" : "metadata", "sort":["_score"],"query":{"function_score":{"boost":"5","functions":[{"filter":{"match":{"resourceType":"series"}},"weight":1.5},{"filter":{"exists":{"field":"parentUuid"}},"weight":0.3},{"filter":{"match":{"cl_status.key":"obsolete"}},"weight":0.2},{"filter":{"match":{"cl_status.key":"superseded"}},"weight":0.3},{"gauss":{"dateStamp":{"scale":"365d","offset":"90d","decay":0.5}}}],"score_mode":"multiply","query":{"bool":{"must":[{"terms":{"isTemplate":["n"]}}]}}}},"aggregations":{"groupOwner":{"terms":{"field":"groupOwner"},"aggs":{"sourceCatalogue":{"terms":{"field":"sourceCatalogue"}}},"meta":{"field":"groupOwner"}},"resourceType":{"terms":{"field":"resourceType"},"meta":{"decorator":{"type":"icon","prefix":"fa fa-fw gn-icon-"},"field":"resourceType"}},"availableInServices":{"filters":{"filters":{"availableInViewService":{"query_string":{"query":"+linkProtocol:/OGC:WMS.*/"}},"availableInDownloadService":{"query_string":{"query":"+linkProtocol:/OGC:WFS.*/"}}}},"meta":{"decorator":{"type":"icon","prefix":"fa fa-fw ","map":{"availableInViewService":"fa-globe","availableInDownloadService":"fa-download"}}}},"cl_topic.key":{"terms":{"field":"cl_topic.key","size":5},"meta":{"decorator":{"type":"icon","prefix":"fa fa-fw gn-icon-"},"field":"cl_topic.key"}},"th_httpinspireeceuropaeutheme-theme_tree.key":{"terms":{"field":"th_httpinspireeceuropaeutheme-theme_tree.key","size":5},"meta":{"decorator":{"type":"icon","prefix":"fa fa-fw gn-icon iti-","expression":"http://inspire.ec.europa.eu/theme/(.*)"},"field":"th_httpinspireeceuropaeutheme-theme_tree.key"}},"tag":{"terms":{"field":"tag.default","include":".*","size":5},"meta":{"caseInsensitiveInclude":true,"field":"tag.default"}},"sourceCatalogue":{"terms":{"field":"sourceCatalogue","size":5,"include":".*"},"meta":{"orderByTranslation":true,"filterByTranslation":true,"displayFilter":true,"field":"sourceCatalogue"}},"OrgForResource":{"terms":{"field":"OrgForResourceObject.default","include":".*","size":5},"meta":{"caseInsensitiveInclude":true,"field":"OrgForResourceObject.default"}},"creationYearForResource":{"terms":{"field":"creationYearForResource","size":5,"order":{"_key":"desc"}},"meta":{"field":"creationYearForResource"}},"format":{"terms":{"field":"format","size":5,"order":{"_key":"asc"}},"meta":{"field":"format"}},"cl_spatialRepresentationType.key":{"terms":{"field":"cl_spatialRepresentationType.key","size":5},"meta":{"field":"cl_spatialRepresentationType.key"}},"cl_maintenanceAndUpdateFrequency.key":{"terms":{"field":"cl_maintenanceAndUpdateFrequency.key","size":5},"meta":{"field":"cl_maintenanceAndUpdateFrequency.key"}},"cl_status.key":{"terms":{"field":"cl_status.key","size":5},"meta":{"field":"cl_status.key"}},"resolutionScaleDenominator":{"terms":{"field":"resolutionScaleDenominator","size":5,"order":{"_key":"asc"}},"meta":{"field":"resolutionScaleDenominator"}},"resolutionDistance":{"terms":{"field":"resolutionDistance","size":5,"order":{"_key":"asc"}},"meta":{"field":"resolutionDistance"}},"dateStamp":{"auto_date_histogram":{"field":"dateStamp","buckets":50}}},"_source":{"includes":["uuid","id","groupOwner","logo","cat","inspireThemeUri","inspireTheme_syn","cl_topic","resourceType","resourceTitle*","resourceAbstract*","draft","owner","link","status*","rating","geom","contact*","Org*","isTemplate","valid","isHarvested","dateStamp","documentStandard","standardNameObject.default","cl_status*","mdStatus*"]},"script_fields":{"overview":{"script":{"source":"return params['_source'].overview == null ? [] : params['_source'].overview.stream().findFirst().orElse([]);"}}},"track_total_hits":true}"""

GEONODE_URLMAP = [
    {
        "id": "geonode:layers",
        "url": "/api/layers/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "",
    },
    {
        "id": "geonode:datasets",
        "url": "/api/datasets/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "",
    },
    {
        "id": "geonode:datasets",
        "url": "/api/v2/datasets/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
    {
        "id": "geonode:documents",
        "url": "/api/documents/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "",
    },
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "",
    },
    {
        "id": "csw202",
        "url": "/catalogue/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "oaipmh20",
        "url": "/catalogue/csw?mode=oaipmh&verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "opensearch",
        "url": "/catalogue/csw?mode=opensearch&service=CSW&version=2.0.2&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "opensearch",
        "url": "/catalogue/opensearch",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
    {
        "id": "wms111",
        "url": "/geoserver/ows?service=WMS&version=1.1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wfs110",
        "url": "/geoserver/ows?service=WFS&version=1.1.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wcs111",
        "url": "/geoserver/ows?service=WCS&version=1.1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wmts100",
        "url": "/geoserver/gwc/service/wmts?service=WMTS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wms130",
        "url": "/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wfs100",
        "url": "/geoserver/ows?service=WFS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wfs200",
        "url": "/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.0",
    },
    {
        "id": "wcs100",
        "url": "/geoserver/ows?service=WCS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wcs110",
        "url": "/geoserver/ows?service=WCS&version=1.1.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wcs11",
        "url": "/geoserver/ows?service=WCS&version=1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1",
    },
    {
        "id": "wcs201",
        "url": "/geoserver/ows?service=WCS&version=2.0.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.1",
    },
    {
        "id": "wps100",
        "url": "/geoserver/ows?service=WPS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "tms100",
        "url": "/geoserver/gwc/service/tms/1.0.0",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wms-c111",
        "url": "/geoserver/gwc/service/wms?request=GetCapabilities&version=1.1.1&tiled=true",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "ogc:tiles",
        "url": "/geoserver/ogc/tiles/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogc:images",
        "url": "/geoserver/ogc/images/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogc:maps",
        "url": "/geoserver/ogc/maps/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogc:features",
        "url": "/geoserver/ogc/features/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "stacserverapi",
        "display_url": "/geoserver/ogc/stac/v1",
        "url": "/geoserver/ogc/stac/v1/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:version",
        "url": "/geoserver/rest/about/version",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:server-status",
        "url": "/geoserver/rest/about/server-status",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:settings",
        "url": "/geoserver/rest/settings",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:layers",
        "url": "/geoserver/rest/layers",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

DKAN_URLMAP = [
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
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dkan:search",
        "url": "/api/1/search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "dkan:metastore",
        "url": "/api/1/metastore",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "dkan:datastore",
        "url": "/api/1/metastore",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "dcat:n3",
        "url": "/catalog.n3",
        "expected_mime": "text/n3",
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:ttl",
        "url": "/catalog.ttl",
        "expected_mime": "text/turtle",
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:xml",
        "url": "/catalog.xml",
        "expected_mime": "application/rdf+xml",
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:jsonld",
        "url": "/catalog.jsonld",
        "expected_mime": "application/ld+json",
        "is_json": True,
        "version": None,
    },
    {
        "id": "drupal:jsonapi",
        "url": "/jsonapi/dataset/dataset",
        "accept": "application/vnd.api+json, application/json",
        "expected_mime": JSON_MIMETYPES + ["application/vnd.api+json"],
        "is_json": True,
        "version": None,
    },
]

CKAN_URLMAP = [
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
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcat:n3",
        "url": "/catalog.n3",
        "expected_mime": "text/n3",
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:ttl",
        "url": "/catalog.ttl",
        "expected_mime": "text/turtle",
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:xml",
        "url": "/catalog.xml",
        "expected_mime": "application/rdf+xml",
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:jsonld",
        "url": "/catalog.jsonld",
        "expected_mime": "application/ld+json",
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcat",
        "url": "/catalog.rdf",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:xml",
        "url": "/feeds/dcat",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
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
        "url": "/catalog/oai?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

IPT_URLMAP = [
    {
        "id": "dcat:ttl",
        "url": "/dcat",
        "expected_mime": "text/turtle",
        "is_json": False,
        "version": None,
    },
    {
        "id": "ipt:dataset",
        "url": "/inventory/dataset",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rss",
        "url": "/rss.do",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]


JUNAR_URLMAP = [
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "junar:datasets",
        "url": "/api/v2/datasets",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
]

TRIPLYDB_URLMAP = [
    {
        "id": "triplydb:datasets",
        "url": "/_api/facets/datasets",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
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
        "id": "opensearch",
        "url": "/opensearch.xml",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
]


GEONETWORK_URLMAP = [
    {
        "id": "geonetwork:api",
        "url": "/srv/api",
        "expected_mime": XML_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geonetwork:query",
        "display_url": "/srv/eng/q",
        "url": "/srv/eng/q?_content_type=json&bucket=s101&facet.q=&fast=index&resultType=details&sortBy=relevance&sortOrder=&title_OR_altTitle_OR_any=",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geonetwork:records",
        "url": "/srv/api/records",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "openapi",
        "url": "/srv/v2/api-docs",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2",
    },
    {
        "id": "csw202",
        "url": "/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "opensearch",
        "url": "/srv/eng/portal.opensearch",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "oaipmh20",
        "url": "/srv/eng/oaipmh?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "dcat:xml",
        "url": "/srv/api/records?accept=application/rdf+xml",
        "accept": "application/rdf+xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "ogcrecordsapi",
        "url": "/srv/ogc/records/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogcrecordsapi",
        "url": "/ogc/records/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    #    {'id' : 'geonetwork:search', 'url' : '/srv/api/search/records/_search?bucket=metadata', 'accept' : 'application/json', 'expected_mime' : JSON_MIMETYPES, 'is_json' : False, 'version': None, 'post_params': GEONETWORK_SEARCH_POST_PARAMS},
    {
        "id": "geonetwork:settings",
        "url": "/srv/api/settings",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "geonetwork:selections",
        "url": "/srv/api/selections",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "geonetwork:site",
        "url": "/srv/api/site",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

FIGSHARE_URLMAP = [
    {
        "id": "sitemap",
        "url": "/sitemap/siteindex.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "urlpat": "/articles/dataset/",
    },
    {
        "id": "figshare:graphql",
        "url": "/api/graphql?thirdPartyCookies=true&type=current&operation=advancedSearch",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "index",
        "url": "/articles/dataset/",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

REDIVIS_URLMAP = [
    {
        "id": "openapi",
        "url": "/api/v1/openapi.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

SOCRATA_URLMAP = [
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "socrata:views",
        "url": "/api/views",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "socrata:catalog",
        "url": "/api/catalog/v1?only=datasets&limit=1",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "opensearch",
        "url": "/opensearch.xml",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
]

PXWEB_URLMAP = [
    {
        "id": "pxwebapi",
        "url": "/api/v1/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "pxwebapi",
        "url": "/api/v1/en/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "pxwebapi",
        "url": "/api/v1/sv/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "pxwebapi",
        "url": "/api/v1/fi/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
    {
        "id": "pxwebapi",
        "url": "/api/v1/da/",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1",
    },
]

PXSTAT_URLMAP = [
    {
        "id": "pxstatapi",
        "url": "/public/api.restful/PxStat.Data.Cube_API.ReadCollection/1900-01-01/en",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    }
]

KNOEMA_URLMAP = [
    {
        "id": "knoema:search",
        "display_url": "/api/1.0/search",
        "url": "/api/1.0/search?query=test",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "sdmx:datastructure",
        "url": "/api/1.0/sdmx",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "opensearch",
        "url": "/OpenSearch.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "knoema:meta-dataset",
        "url": "/api/1.0/meta/dataset",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

STATSUITE_URLMAP = [
    {
        "id": "statsuite:search",
        "url": "/api/search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    }
]


ISTATDATABROWSER_URLMAP = [
    {
        "id": "istatdatabrowser:hub",
        "url": "/databrowserhub/api/core/hub/minimalInfo",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "istatdatabrowser:nodes",
        "url": "/databrowserhub/api/core/nodes",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "istatdatabrowser:hub-nested",
        "url": "/databrowser/api/core/hub/minimalInfo",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "istatdatabrowser:nodes-nested",
        "url": "/databrowser/api/core/nodes",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]


DATAVERSE_URLMAP = [
    {
        "id": "dataverseapi",
        "display_url": "/api/search",
        "url": "/api/search?q=*&type=dataset&sort=name&order=asc",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dataverseapi",
        "url": "/api/info/version",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]


INVENIORDM_URLMAP = [
    {
        "id": "inveniordmapi",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "inveniordmapi:records",
        "url": "/api/records",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai2d",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai2d?verb=Identify",
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
]

INVENIO_URLMAP = [
    {
        "id": "inveniordmapi",
        "url": "/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "inveniordmapi:records",
        "url": "/api/records",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai2d",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai2d?verb=Identify",
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
]


WORKTRIBE_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/oaiprovider?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "sitemap",
        "url": "/sitemap_index.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]


HYRAX_URLMAP = [
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

DSPACE_URLMAP = [
    {
        "id": "dspace",
        "url": "/server/api",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "7",
    },
    {
        "id": "dspace:objects",
        "url": "/server/api/discover/search/objects",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "7",
    },
    {
        "id": "dspace:items",
        "url": "/rest/items",
        "accept": "application/json",
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
    {
        "id": "oaipmh20",
        "url": "/server/oai/request?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "opensearch",
        "url": "/open-search/description.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "rss",
        "url": "/feed/rss_2.0/site",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "atom",
        "url": "/feed/atom_1.0/site",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "sitemap",
        "url": "/sitemap_index.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

ESPLORO_URLMAP = [
    {
        "id": "esploro:search",
        "display_url": "/esplorows/rest/research/simpleSearch",
        "url": "/esplorows/rest/research/simpleSearch?_wadl",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sitemap",
        "url": "/view/google/siteindex.xml",
        "is_json": False,
        "version": None,
        "urlpat": "/dataset/",
    },
]

PURE_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/ws/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "rss",
        "url": "/en/datasets/?search=&isCopyPasteSearch=false&format=rss",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "sitemap",
        "url": "/sitemap/datasets.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "pure:export_excel",
        "url": "/en/datasets/?export=xls",
        "expected_mime": EXCEL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "rss",
        "url": "/de/datasets/?search=&isCopyPasteSearch=false&format=rss",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "rss",
        "url": "/da/datasets/?search=&isCopyPasteSearch=false&format=rss",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

ELSEVIERDC_URLMAP = [
    {
        "id": "sitemap",
        "url": "/sitemap/index",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/do/oai/?verb=Identify",
        "accept": "application/xml",
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


NADA_URLMAP = [
    {
        "id": "nada:catalog-search",
        "url": "/index.php/api/catalog/search",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "nada:csvexport",
        "url": "/index.php/catalog/export/csv?ps=5000&collection[]",
        "expected_mime": CSV_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

GEOSERVER_URLMAP = [
    {
        "id": "wms111",
        "url": "/ows?service=WMS&version=1.1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wms130",
        "url": "/ows?service=WMS&version=1.3.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wfs100",
        "url": "/ows?service=WFS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wfs110",
        "url": "/ows?service=WFS&version=1.1.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wfs200",
        "url": "/ows?service=WFS&version=2.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.0",
    },
    {
        "id": "wcs100",
        "url": "/ows?service=WCS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wcs110",
        "url": "/ows?service=WCS&version=1.1.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wcs111",
        "url": "/ows?service=WCS&version=1.1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wcs11",
        "url": "/ows?service=WCS&version=1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1",
    },
    {
        "id": "wcs201",
        "url": "/ows?service=WCS&version=2.0.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.1",
    },
    {
        "id": "wps100",
        "url": "/ows?service=WPS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "tms100",
        "url": "/gwc/service/tms/1.0.0",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wms-c111",
        "url": "/gwc/service/wms?request=GetCapabilities&version=1.1.1&tiled=true",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wmts100",
        "url": "/gwc/service/wmts?REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "csw202",
        "url": "/csw?service=csw&version=2.0.2&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "ogc:tiles",
        "url": "/ogc/tiles/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogc:images",
        "url": "/ogc/images/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogc:maps",
        "url": "/ogc/maps/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "ogc:features",
        "url": "/ogc/features/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "stacserverapi",
        "display_url": "/ogc/stac/v1",
        "url": "/ogc/stac/v1/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:version",
        "url": "/rest/about/version",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:server-status",
        "url": "/rest/about/server-status",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:settings",
        "url": "/rest/settings",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "geoserver:layers",
        "url": "/rest/layers",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    # Non-standard GeoServer paths (e.g., /geo/wms instead of /ows)
    {
        "id": "wms111",
        "url": "/geo/wms?service=WMS&version=1.1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wms130",
        "url": "/geo/wms?service=WMS&version=1.3.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
    {
        "id": "wfs100",
        "url": "/geo/wfs?service=WFS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wfs110",
        "url": "/geo/wfs?service=WFS&version=1.1.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wfs200",
        "url": "/geo/wfs?service=WFS&version=2.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.0",
    },
    {
        "id": "wcs100",
        "url": "/geo/wms?service=WCS&version=1.0.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wcs110",
        "url": "/geo/wms?service=WCS&version=1.1.0&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.0",
    },
    {
        "id": "wcs111",
        "url": "/geo/wms?service=WCS&version=1.1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wcs11",
        "url": "/geo/wms?service=WCS&version=1.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1",
    },
    {
        "id": "wcs201",
        "url": "/geo/wms?service=WCS&version=2.0.1&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.1",
    },
]

# When the catalog link already includes /geoserver, probe WMS/WFS only.
# The full map is 34 paths and doubles against the origin, which hangs on dead hosts.
GEOSERVER_FAST_URLMAP = GEOSERVER_URLMAP[:5]

MAPPROXY_URLMAP = [
    {
        "id": "wms111",
        "url": "/service?REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wmts100",
        "url": "/service?REQUEST=GetCapabilities&SERVICE=WMTS",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "tms100",
        "url": "/tms/1.0.0/",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
    {
        "id": "wmts100",
        "url": "/wmts/1.0.0/WMTSCapabilities.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0.0",
    },
]

NCWMS_URLMAP = [
    {
        "id": "wms111",
        "url": "/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.1.1",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1.1",
    },
    {
        "id": "wms130",
        "url": "/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.3.0",
    },
]


EPRINTS_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/cgi/oai2?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai2?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "rss",
        "url": "/cgi/latest_tool?output=RSS2",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "atom",
        "url": "/cgi/latest_tool?output=Atom",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "eprints:rest",
        "url": "/rest/eprint",
        "expected_mime": HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "eprints:rdf",
        "url": "/cgi/export/repository/RDFXML/devel.rdf",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "eprints:n3",
        "url": "/cgi/export/repository/RDFN3/devel.n3",
        "expected_mime": N3_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "eprints:datasets",
        "url": "/cgi/exportview/type/dataset/JSON/dataset.js",
        "expected_mime": JSON_MIMETYPES + HTML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opensearch",
        "url": "/cgi/opensearchdescription",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
]

KOORDINATES_URLMAP = [
    {
        "id": "koordinates:data-catalog",
        "url": "/services/api/v1.x/data/",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "csw202",
        "url": "/services/csw/?service=CSW&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
]

BLACKLIGHT_URLMAP = [
    {
        "id": "blacklight:catalog",
        "url": "/catalog.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "opensearch",
        "url": "/catalog/opensearch.xml",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
]


ALEPH_URLMAP = [
    {
        "id": "aleph:collections",
        "url": "/api/2/collections",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2.0",
    },
    {
        "id": "aleph:query",
        "url": "/api/1/query",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

QWC2_URLMAP = [
    {
        "id": "qwc2:layers",
        "url": "/themes.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    }
]

PYGEOAPI_URLMAP = [
    {
        "id": "pygeoapi:openapi",
        "url": "/openapi",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "ogc:features",
        "url": "/collections/?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "ogc:features",
        "url": "/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]

OPENEO_URLMAP = [
    {
        "id": "stacserverapi",
        "url": "/collections",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "openeo:processes",
        "url": "/processes",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "openeo:well-known",
        "url": "/.well-known/openeo",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

ISOGEO_URLMAP = [
    {
        "id": "openapi",
        "url": "/api",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

PYCSW30_URLMAP = [
    {
        "id": "ogcrecords",
        "url": "/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oaipmh",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/?mode=oaipmh&verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "csw202",
        "url": "/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "csw300",
        "url": "/csw",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "3.0.0",
    },
    {
        "id": "opensearch",
        "url": "/opensearch",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "sru",
        "url": "/sru",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "openapi",
        "url": "/openapi?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "stac:collection",
        "url": "/search?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]


WIS20BOX_URLMAP = [
    {
        "id": "pygeoapi:openapi",
        "url": "/oapi/openapi",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "ogc:features",
        "url": "/oapi/collections/?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
    {
        "id": "ogcrecords",
        "url": "/collections?f=json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "1.0",
    },
]


OPENDATASOFT_URLMAP = [
    {
        "id": "opendatasoftapi",
        "display_url": "/api",
        "url": "/api/v2/catalog/datasets/",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opendatasoftapi",
        "url": "/api/explore/v2.1/catalog/datasets?limit=1",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "2.1",
    },
    {
        "id": "dcat:xml",
        "url": "/api/v2/catalog/exports/dcat",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:xml",
        "url": "/api/explore/v2.1/catalog/exports/dcat",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
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

MAGDA_URLMAP = [
    {
        "id": "magda:datasets",
        "url": "/search/api/v0/search/datasets",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "magda:organizations",
        "url": "/search/api/v0/search/organisations",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "magda:datasets",
        "url": "/api/v0/search/datasets",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "magda:organizations",
        "url": "/api/v0/search/organisations",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

ARCGISHUB_URLMAP = [
    {
        "id": "dcatap201",
        "url": "/api/feed/dcat-ap/2.0.1.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcatus11",
        "url": "/api/feed/dcat-us/1.1.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rss",
        "url": "/api/feed/rss/2.0",
        "accept": "application/json",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "ogcrecordsapi",
        "url": "/api/search/v1",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
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

ARCGISSERVER_URLMAP = [
    {
        "id": "arcgis:portals:self",
        "url": "/portal/sharing/rest/portals/self?f=pjson",
        "accept": "application/json",
        "expected_mime": PLAIN_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:info",
        "url": "/rest/info?f=pjson",
        "accept": "application/json",
        "expected_mime": PLAIN_MIMETYPES + JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:rest:services",
        "url": "/rest/services?f=pjson",
        "accept": "application/json",
        "expected_mime": PLAIN_MIMETYPES + JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "arcgis:soap",
        "url": "/services?wsdl",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "arcgis:sitemap",
        "url": "/rest/services?f=sitemap",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "arcgis:geositemap",
        "url": "/rest/services?f=geositemap",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "arcgis:kmz",
        "url": "/rest/services?f=kmz",
        "expected_mime": KMZ_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]

OSKARI_URLMAP = [
    {
        "id": "oskari:getmaplayers",
        "url": "/action?action_route=GetMapLayers&lang=en&epsg=EPSG%3A3067",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oskari:gethiermaplayers",
        "url": "/action?action_route=GetHierarchicalMapLayerGroups",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

METAGIS_URLMAP = [
    {
        "id": "metagis:layers",
        "url": "/ResultJSONGNServlet",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
        "prefetch": True,
    },
]

THREDDS_URLMAP = [
    {
        "id": "thredds:catalog",
        "url": "/catalog.xml",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "thredds:info",
        "url": "/serverInfo.xml",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "thredds:info",
        "url": "/info/serverInfo.xml",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
]

ERDDAP_URLMAP = [
    {
        "id": "erddap:index",
        "url": "/index.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "erddap:datasets",
        "url": "/info/index.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "opensearch",
        "url": "/opensearch1.1/description.xml",
        "expected_mime": "application/opensearchdescription+xml",
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "sitemap",
        "url": "/sitemap.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
]

OPUS_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "rss",
        "url": "/rss/index/index/searchtype/latest",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]


RADAR_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/oai/OAIHandler?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "radar:datasets",
        "url": "/radar/api/datasets",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "sitemap",
        "url": "/radar/sitemap",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]


DHIS2_URLMAP = [
    {
        "id": "dhis2:system-info",
        "url": "/api/system/info",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dhis2:dataSets",
        "url": "/api/dataSets.json?fields=id,displayName&pageSize=1",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dhis2:indicators",
        "url": "/api/indicators.json?fields=id,displayName&pageSize=1",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]


MYCORE_URLMAP = [
    {
        "id": "mycore:objects",
        "url": "/api/v2/objects",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/servlets/OAIDataProvider?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "sitemap",
        "url": "/sitemap_google.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]


IFREMER_URLMAP = [
    {
        "id": "ifremer:search",
        "url": "/api/full-search-response",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai/OAIHandler?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]


ESRIGEO_URLMAP = [
    {
        "id": "esrigeo:geoportal",
        "url": "/rest/geoportal",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "esrigeo:metadata:search",
        "url": "/rest/metadata/search",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "csw202",
        "url": "/csw",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "3.0.0",
    },
    {
        "id": "csw202",
        "url": "/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "atom",
        "url": "/opensearch?f=atom&from=1&size=10&sort=title.sort%3Aasc&esdsl=%7B%7D",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "esrigeo:json",
        "url": "/opensearch?f=json&from=1&size=10&sort=title.sort%3Aasc&esdsl=%7B%7D",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "rss",
        "url": "/opensearch?f=rss&from=1&size=10&sort=title.sort%3Aasc&esdsl=%7B%7D",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcatus11",
        "url": "/opensearch?f=dcat&from=1&size=10&sort=title.sort%3Aasc&esdsl=%7B%7D",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "esrigeo:csv",
        "url": "/opensearch?f=csv&from=1&size=10&sort=title.sort%3Aasc&esdsl=%7B%7D",
        "expected_mime": CSV_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "esrigeo:kml",
        "url": "/opensearch?f=kml&from=1&size=10&sort=title.sort%3Aasc&esdsl=%7B%7D",
        "expected_mime": KML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opensearch",
        "url": "/openSearchDescription",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
    {
        "id": "opensearch",
        "url": "/geoportal/openSearchDescription",
        "expected_mime": XML_MIMETYPES + ["application/opensearchdescription+xml"],
        "is_json": False,
        "version": "1.1",
    },
]

JKAN_URLMAP = [
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcatus11",
        "url": "/datasets.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

OPENGDC_URLMAP = [
    {
        "id": "openapi",
        "url": "/openapi.json",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": "3.0",
    },
    {
        "id": "opengdc:datasets",
        "url": "/api/datasets",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opensearch",
        "url": "/osdd.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "sitemap",
        "url": "/sitemap.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
]

DABAR_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/oai/?verb=Identify",
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
    {
        "id": "sitemap",
        "url": "/sitemap.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
]

OPENSCIENCESI_URLMAP = [
    {
        "id": "oaipmh20",
        "url": "/oai/oai2.php?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/oai/?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

WEKO3_URLMAP = [
    {
        "id": "weko3:records",
        "url": "/api/records/?page=1&size=20&sort=-createdate&search_type=0&q=&title=&creator=&filedate_from=&filedate_to=&fd_attr=&id=&id_attr=&srctitle=&type=17&dissno=&lang=english",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "oaipmh20",
        "url": "/oai?verb=Identify",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
]

SDMXRI_URLMAP = [
    {
        "id": "sdmx:dataflows",
        "url": "/rest/dataflow",
        "accept": "application/json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "sdmx:datastructure",
        "url": "/rest/datastructure",
        "expected_mime": "application/vnd.sdmx.structure+xml",
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "sdmx:codelist",
        "url": "/rest/codelist",
        "expected_mime": "application/vnd.sdmx.structure+xml",
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "sdmx:conceptscheme",
        "url": "/rest/conceptscheme",
        "expected_mime": "application/vnd.sdmx.structure+xml",
        "is_json": False,
        "version": "1.0",
    },
]


from apidetect_urlmaps_draft import DRAFT_CATALOGS_URLMAP, OPENDAP_URLMAP_DRAFT

OPENDAP_URLMAP = OPENDAP_URLMAP_DRAFT

OPENDATAREG_URLMAP = [
    {
        "id": "opendatareg:catalog",
        "url": "/catalog.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opendatareg:collections",
        "url": "/collections",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "opendatareg:stac",
        "url": "/stac",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
]

CUSTOM_URLMAP = [
    {
        "id": "dcatus11",
        "url": "/data.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcat:xml",
        "url": "/catalog.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "dcat:json",
        "url": "/catalog.json",
        "expected_mime": JSON_MIMETYPES,
        "is_json": True,
        "version": None,
    },
    {
        "id": "dcat:jsonld",
        "url": "/catalog.jsonld",
        "expected_mime": JSONLD_MIMETYPES,
        "is_json": True,
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
        "id": "dcat",
        "url": "/catalog.rdf",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
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
        "url": "/oai/request?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "oaipmh20",
        "url": "/cgi/oai2?verb=Identify",
        "accept": "application/xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "csw202",
        "url": "/csw?service=CSW&version=2.0.2&request=GetCapabilities",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0.2",
    },
    {
        "id": "sparql",
        "url": "/sparql",
        "expected_mime": SPARQL_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "opensearch",
        "url": "/opensearch.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.1",
    },
    {
        "id": "rss",
        "url": "/rss.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "2.0",
    },
    {
        "id": "atom",
        "url": "/feed.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": "1.0",
    },
    {
        "id": "sitemap",
        "url": "/sitemap.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "sitemap",
        "url": "/sitemap.xml.gz",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
        "prefetch": False,
    },
    {
        "id": "sitemap",
        "url": "/sitemap_google.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sitemap",
        "url": "/sitemap/index",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
    {
        "id": "sitemap",
        "url": "/sitemap_index.xml",
        "expected_mime": XML_MIMETYPES,
        "is_json": False,
        "version": None,
    },
]


def analyze_robots(root_url):
    p = urlparse(root_url)
    robots_url = p.scheme + "://" + p.netloc + "/robots.txt"
    logger = logging.getLogger(__name__)
    logger.info("Analyzing robots.txt %s", robots_url)
    try:
        r = requests.get(
            robots_url,
            timeout=DEFAULT_TIMEOUT,
            verify=False,
        )
    except Exception as e:
        logger.error("Error analyzing robots.txt: %s", e)
        return []
    if r.status_code != 200:
        logger.info("robots.txt unavailable, status=%d", r.status_code)
        return []
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(r.text)
    sitemaps = parser.site_maps()
    output = []
    logger = logging.getLogger(__name__)
    if sitemaps is not None and len(sitemaps) > 0:
        logger.info("Found sitemaps: %s", ", ".join(sitemaps))
        for s in sitemaps:
            output.append({"type": "sitemap", "url": s})
    return output


FILTER_RELS = [
    "stylesheet",
    "icon",
    "shortcut icon",
    "mask-icon",
    "apple-touch-icon",
    "manifest",
    "apple-touch-icon-precomposed",
    "preconnect",
    "shortlink",
    "canonical",
    "dns-prefetch",
    "prefetch",
    "preload",
    "terms-of-service",
]
FILTER_TYPES = ["text/css", "image/x-icon", "image/png"]


def analyze_root(root_url):
    logger = logging.getLogger(__name__)
    logger.info("Analyzing root page %s", root_url)
    output = []
    s = requests.Session()
    try:
        response = s.get(
            root_url,
            verify=False,
            headers={"User-Agent": USER_AGENT},
            timeout=(DEFAULT_TIMEOUT, DEFAULT_TIMEOUT),
        )
    except requests.exceptions.Timeout:
        logging.info("Timeout error processing root page")
        #        results.append({'url' : request_url,'error' : 'Timeout'})
        return output
    except requests.exceptions.SSLError:
        logging.info("SSL error processing root page")
        #        results.append({'url' : request_url,'error' : 'SSL Error'})
        return output
    except ConnectionError:
        logging.info("Connection error processing root page")
        #        results.append({'url' : request_url,'error' : 'no connection'})
        return output
    except TooManyRedirects:
        logging.info("Redirects error processing root page")
        #        results.append({'url' : request_url,'error' : 'no connection'})
        return output
    if response.status_code != 200:
        #        results.append({'url' : request_url, 'status' : response.status_code, 'mime' : response.headers['Content-Type'].split(';', 1)[0].lower() if 'content-type' in response.headers.keys() else '', 'error' : 'Wrong status'})
        logging.info(
            f"Status code is {response.status_code}. Error processing root page"
        )
        return output
    #    print(response.text)
    try:
        hp = lxml.etree.HTMLParser()  # encoding='utf8')
        document = lxml.html.fromstring(response.content, parser=hp)
    except ValueError:
        logging.info("Error processing root page")
        return output
    except lxml.etree.ParserError:
        logging.info("Error parsing root page")
        return output
    links = document.xpath("//head/link")
    logger = logging.getLogger(__name__)
    logger.debug("Found header links %d", len(links))
    for link in links:
        lr = dict(link.attrib)
        if "rel" in lr.keys() and lr["rel"].lower() in FILTER_RELS:
            continue
        if "type" in lr.keys() and lr["type"].lower() in FILTER_TYPES:
            continue
        logger.debug("Found link: %s", lr)
        if "rel" in lr.keys() and "href" in lr.keys():
            if lr["rel"] == "resourcesync":
                output.append(
                    {
                        "type": "resourcesync",
                        "url": (
                            lr["href"]
                            if lr["href"][0:4] == "http"
                            else urljoin(root_url, lr["href"])
                        ),
                    }
                )
            elif lr["rel"] == "Sword":
                output.append(
                    {
                        "type": "sword",
                        "url": (
                            lr["href"]
                            if lr["href"][0:4] == "http"
                            else urljoin(root_url, lr["href"])
                        ),
                    }
                )
            elif lr["rel"] == "SwordDeposit":
                output.append(
                    {
                        "type": "sword:deposit",
                        "url": (
                            lr["href"]
                            if lr["href"][0:4] == "http"
                            else urljoin(root_url, lr["href"])
                        ),
                    }
                )
            elif lr["rel"] == "SwordDeposit":
                output.append(
                    {
                        "type": "sword:deposit",
                        "url": (
                            lr["href"]
                            if lr["href"][0:4] == "http"
                            else urljoin(root_url, lr["href"])
                        ),
                    }
                )
            elif lr["rel"] == "unapi-server":
                output.append(
                    {
                        "type": "unapi",
                        "url": (
                            lr["href"]
                            if lr["href"][0:4] == "http"
                            else urljoin(root_url, lr["href"])
                        ),
                    }
                )
        if "type" in lr.keys() and "href" in lr.keys():
            if lr["type"] == "application/opensearchdescription+xml":
                output.append(
                    {
                        "type": "opensearch",
                        "url": (
                            lr["href"]
                            if lr["href"][0:4] == "http"
                            else urljoin(root_url, lr["href"])
                        ),
                    }
                )
    scripts = document.xpath("//script[@type='application/ld+json']")
    for s in scripts:
        logger = logging.getLogger(__name__)
        logger.debug("ld+json script found")
        try:
            data = json.loads(s.text)
            #            logger.debug(data)
            if isinstance(data, list):
                if len(data) > 0:
                    data = data[0]
                else:
                    continue
            logger.debug("JSON-LD keys: %s", list(data.keys()))
            if "@graph" in data.keys() and data["@graph"] is not None:
                logger.debug("graph found")
                root_item = data["@graph"]
            else:
                root_item = data
            if root_item is not None:
                slist = []
                if isinstance(root_item, dict):
                    slist.append(root_item)
                elif isinstance(root_item, list):
                    slist = root_item
                logger.debug("slist created with %d items", len(slist))
                found = False
                for stype in slist:
                    if "@type" in stype.keys():
                        if (
                            isinstance(stype["@type"], list)
                            and "DataCatalog" in stype["@type"]
                        ):
                            output.append(
                                {"type": "schemaorg:datacatalog", "url": root_url}
                            )
                            found = True
                            break
                        elif (
                            isinstance(stype["@type"], str)
                            and stype["@type"] == "DataCatalog"
                        ):
                            output.append(
                                {"type": "schemaorg:datacatalog", "url": root_url}
                            )
                            found = True
                            break
                    if "mainEntity" in stype.keys() and stype["mainEntity"] is not None:
                        mainlist = []
                        if isinstance(stype["mainEntity"], dict):
                            mainlist.append(stype["mainEntity"])
                        elif isinstance(stype["mainEntity"], list):
                            mainlist = stype["mainEntity"]
                        for entity in mainlist:
                            if "@type" not in entity.keys():
                                continue
                            if (
                                isinstance(entity["@type"], list)
                                and "DataCatalog" in entity["@type"]
                            ):
                                output.append(
                                    {"type": "schemaorg:datacatalog", "url": root_url}
                                )
                                found = True
                                break
                            elif (
                                isinstance(entity["@type"], str)
                                and entity["@type"] == "DataCatalog"
                            ):
                                found = True
                                output.append(
                                    {"type": "schemaorg:datacatalog", "url": root_url}
                                )
                                break

        except ValueError:
            continue

    return output


DEEP_SEARCH_FUNCTIONS = [analyze_robots, analyze_root]


CATALOGS_URLMAP = {
    "geonode": GEONODE_URLMAP,
    "dkan": DKAN_URLMAP,
    "ckan": CKAN_URLMAP,
    "geonetwork": GEONETWORK_URLMAP,
    "openwis": GEONETWORK_URLMAP,
    "pxweb": PXWEB_URLMAP,
    "pxstat": PXSTAT_URLMAP,
    "knoema": KNOEMA_URLMAP,
    "socrata": SOCRATA_URLMAP,
    "dataverse": DATAVERSE_URLMAP,
    "dspace": DSPACE_URLMAP,
    "pure": PURE_URLMAP,
    "nada": NADA_URLMAP,
    "geoserver": GEOSERVER_URLMAP,
    "eprints": EPRINTS_URLMAP,
    "koordinates": KOORDINATES_URLMAP,
    "aleph": ALEPH_URLMAP,
    "mycore": MYCORE_URLMAP,
    "opus": OPUS_URLMAP,
    "radar": RADAR_URLMAP,
    "dhis2": DHIS2_URLMAP,
    "magda": MAGDA_URLMAP,
    "opendatasoft": OPENDATASOFT_URLMAP,
    "arcgishub": ARCGISHUB_URLMAP,
    "arcgisserver": ARCGISSERVER_URLMAP,
    "oskari": OSKARI_URLMAP,
    "metagis": METAGIS_URLMAP,
    "esrigeo": ESRIGEO_URLMAP,
    "geoblacklight": BLACKLIGHT_URLMAP,
    "pygeoapi": PYGEOAPI_URLMAP,
    "openeo": OPENEO_URLMAP,
    "isogeo": ISOGEO_URLMAP,
    "thredds": THREDDS_URLMAP,
    "erddap": ERDDAP_URLMAP,
    "mapproxy": MAPPROXY_URLMAP,
    "statsuite": STATSUITE_URLMAP,
    "istatdatabrowser": ISTATDATABROWSER_URLMAP,
    "worktribe": WORKTRIBE_URLMAP,
    "inveniordm": INVENIORDM_URLMAP,
    "invenio": INVENIO_URLMAP,
    "esploro": ESPLORO_URLMAP,
    "hyrax": HYRAX_URLMAP,
    "ifremercatalog": IFREMER_URLMAP,
    "jkan": JKAN_URLMAP,
    "qwc2": QWC2_URLMAP,
    "weko3": WEKO3_URLMAP,
    "dabar": DABAR_URLMAP,
    "opensciencesi": OPENSCIENCESI_URLMAP,
    "wis20box": WIS20BOX_URLMAP,
    "ncwms": NCWMS_URLMAP,
    "figshare": FIGSHARE_URLMAP,
    "redivis": REDIVIS_URLMAP,
    "elsevierdigitalcommons": ELSEVIERDC_URLMAP,
    "junar": JUNAR_URLMAP,
    "custom": CUSTOM_URLMAP,
    "pycsw": PYCSW30_URLMAP,
    "opendap": OPENDAP_URLMAP,
    "opendaphyrax": OPENDAP_URLMAP,
    "triplydb": TRIPLYDB_URLMAP,
    "ipt": IPT_URLMAP,
    "sdmxri": SDMXRI_URLMAP,
    "opendatareg": OPENDATAREG_URLMAP,
    "opengdc": OPENGDC_URLMAP,
    **DRAFT_CATALOGS_URLMAP,
}


def istatdatabrowser_url_cleanup_func(url):
    """Keep StatKit path prefixes; strip the Data Browser SPA path."""
    parsed = urlparse(url)
    path = parsed.path or "/"
    lower = path.lower()
    for prefix in ("/coeweb", "/dbrowser", "/beta"):
        idx = lower.find(prefix)
        if idx != -1:
            kept = path[: idx + len(prefix)].rstrip("/") or "/"
            return urlunparse((parsed.scheme, parsed.netloc, kept, "", "", ""))
    spa = lower.find("/databrowser")
    if spa != -1 and "/databrowserhub" not in lower:
        kept = path[:spa].rstrip("/") or "/"
        return urlunparse((parsed.scheme, parsed.netloc, kept, "", "", ""))
    return url.rstrip("/")


def geoserver_url_cleanup_func(url):
    url = url.rstrip("/")
    if len(url) >= 4 and url.endswith("/web"):
        url = url[:-4]
    return url


def copernicusdhus_url_cleanup_func(url):
    """Drop SPA fragments and keep the /dhus app root when present."""
    parsed = urlparse(url)
    path = parsed.path or "/"
    lower = path.lower()
    idx = lower.find("/dhus")
    if idx != -1:
        kept = path[: idx + len("/dhus")].rstrip("/") or "/dhus"
        return urlunparse((parsed.scheme, parsed.netloc, kept, "", "", ""))
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")


def geoserver_root_url(url):
    """Return the /geoserver root when present, otherwise the cleaned URL."""
    url = geoserver_url_cleanup_func(url)
    lower = url.lower()
    idx = lower.rfind("/geoserver")
    if idx == -1:
        return url
    return url[: idx + len("/geoserver")]


def arcgisserver_url_cleanup_func(url):
    domain = urlparse(url).netloc
    if domain.find("443") > -1 or url[0:5] == "https":
        url = url.replace("http://", "https://")
    if url.find("/rest/services") > -1:
        url = url.rsplit("/rest/services", 1)[0]
    elif url.find("/services") > -1:
        url = url.rsplit("/services", 1)[0]
    return url


def geonetwork_url_cleanup_func(url):
    return url.split("/srv")[0]


def thredds_url_cleanup_func(url):
    return url.split("/catalog.html")[0]


def erddap_url_cleanup_func(url):
    return url.split("/index.html")[0]


def ala_url_cleanup_func(url):
    url = url.rstrip("/")
    if url.endswith("/datasets"):
        url = url[: -len("/datasets")]
    return url.rstrip("/")


def lizmap_url_cleanup_func(url):
    url = url.rstrip("/")
    if "/index.php" in url:
        url = url.split("/index.php", 1)[0]
    elif "/lizmap/" in url:
        url = url.split("/lizmap/", 1)[0]
    return url.rstrip("/")


def mapbender_url_cleanup_func(url):
    url = url.rstrip("/")
    for marker in ("/application/", "/mapbender3/"):
        if marker in url:
            return url.split(marker, 1)[0].rstrip("/")
    return url


def geomapfish_url_cleanup_func(url):
    url = url.rstrip("/")
    for marker in ("/theme/", "/wsgi/", "/static-ngeo/"):
        if marker in url:
            return url.split(marker, 1)[0].rstrip("/")
    return url


def getsdiportal_url_cleanup_func(url):
    url = url.rstrip("/")
    if url.endswith("/geoserver") or "/geoserver/" in url:
        return geoserver_url_cleanup_func(url)
    return url


def redatam_url_cleanup_func(url):
    parsed = urlparse(url)
    if "rpwebengine.exe" in (parsed.path or "").lower():
        return f"{parsed.scheme}://{parsed.netloc}"
    return url.rstrip("/")


def tianditu_url_cleanup_func(url):
    """Drop viewer HTML filenames; keep directory prefixes for city/portal nodes."""
    url = url.rstrip("/")
    parsed = urlparse(url)
    path = parsed.path or ""
    last = path.rsplit("/", 1)[-1]
    if last and "." in last:
        path = path.rsplit("/", 1)[0]
        return f"{parsed.scheme}://{parsed.netloc}{path}".rstrip("/")
    return url


def supermapiserver_url_cleanup_func(url):
    url = url.rstrip("/")
    if url.lower().endswith("/iserver"):
        return url
    if "/iserver/" in url.lower():
        idx = url.lower().rfind("/iserver")
        return url[: idx + len("/iserver")]
    return url


def supermapiportal_url_cleanup_func(url):
    """Strip /iportal so /iportal/web/*.json probes are not doubled."""
    if _path_has_segment(url, "iportal"):
        return _strip_path_marker(url, "/iportal")
    return url.rstrip("/")


def mapgisigserver_url_cleanup_func(url):
    """Keep /igs when present so REST probes attach under the IGServer app."""
    url = url.rstrip("/")
    lower = url.lower()
    if lower.endswith("/igs"):
        return url
    if "/igs/" in lower:
        idx = lower.rfind("/igs")
        return url[: idx + len("/igs")]
    return url


def cogis_url_cleanup_func(url):
    """Strip CoGIS portal and eLiteGIS REST suffixes down to the site root."""
    url = url.rstrip("/")
    lower = url.lower()
    for marker in ("/elitegis/rest/services", "/portal/catalog", "/cogis"):
        idx = lower.find(marker)
        if idx != -1:
            return url[:idx].rstrip("/")
    return url


def nextgisweb_url_cleanup_func(url):
    url = url.rstrip("/")
    if "/resource/" in url:
        return url.split("/resource/", 1)[0].rstrip("/")
    return url


def nesstar_url_cleanup_func(url):
    url = url.rstrip("/")
    if url.endswith("/webview"):
        return url[: -len("/webview")]
    return url


def opus_url_cleanup_func(url):
    url = url.rstrip("/")
    if url.lower().endswith("/home"):
        return url[: -len("/home")]
    return url


def _origin_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def geocortex_url_cleanup_func(url):
    """Strip Essentials REST/viewer suffixes so sites?f=pjson attaches at origin."""
    parsed = urlparse(url)
    path = (parsed.path or "").lower()
    if "/geocortex/" in path or "/essentials/" in path:
        return _origin_url(url)
    return url.rstrip("/")


def minerva_url_cleanup_func(url):
    """Always probe /api/projects/ and /minerva/api/projects/ from origin."""
    return _origin_url(url)


def gringlobal_url_cleanup_func(url):
    """Always probe /gringlobal/* from the catalog origin."""
    return _origin_url(url)


def g3wsuite_url_cleanup_func(url):
    """Strip /map/{group}/{project}/ and /admin so /api/ attaches at the portal root."""
    parsed = urlparse(url)
    path = parsed.path or ""
    lower = path.lower()
    for marker in ("/map/", "/admin"):
        idx = lower.find(marker)
        if idx != -1:
            kept = path[:idx].rstrip("/") or "/"
            if kept == "/":
                return _origin_url(url)
            return urlunparse((parsed.scheme, parsed.netloc, kept, "", "", ""))
    return url.rstrip("/")


def dataone_url_cleanup_func(url):
    return _origin_url(url)


def yoda_url_cleanup_func(url):
    return _origin_url(url)


def origo_url_cleanup_func(url):
    """Strip viewer HTML so /index.json attaches next to the map directory."""
    parsed = urlparse(url)
    path = parsed.path or ""
    lower = path.lower()
    if lower.endswith(".html") or lower.endswith(".htm"):
        path = path.rsplit("/", 1)[0]
        return urlunparse(
            (parsed.scheme, parsed.netloc, path or "/", "", "", "")
        ).rstrip("/")
    return url.rstrip("/")


def swing_url_cleanup_func(url):
    """Strip dashboard chrome so /viewer/ and /databank attach at the origin."""
    path = (urlparse(url).path or "").lower()
    if any(part in path for part in ("/databank", "/viewer", "/dashboard", "/mosaic")):
        return _origin_url(url)
    return url.rstrip("/")


ORIGO_CALL_RE = re.compile(
    r"""Origo\(\s*['\"]([^'\"]+\.json)['\"]""",
    re.I,
)
ORIGO_HREF_RE = re.compile(r"""href\s*=\s*['"]([^"'#]+)['"]""", re.I)
ORIGO_GALLERY_SKIP_PARTS = {
    "css",
    "js",
    "img",
    "images",
    "static",
    "assets",
    "fonts",
    "vendor",
    "origo2client",
    "node_modules",
    "wp-content",
}
ORIGO_GALLERY_SKIP_EXT = {
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "ico",
    "css",
    "js",
    "svg",
    "zip",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "woff",
    "woff2",
    "map",
}
ORIGO_GALLERY_MAX_DIRS = 20


def origo_parse_config_urls(html, site_url):
    """Return Origo('*.json') config URLs from a viewer HTML page."""
    if not html:
        return []
    found = []
    seen = set()
    for raw in ORIGO_CALL_RE.findall(html):
        raw = (raw or "").strip()
        if not raw:
            continue
        url = urljoin(site_url, raw)
        if url not in seen:
            seen.add(url)
            found.append(url)
    return found


def origo_parse_gallery_config_urls(html, site_url):
    """Return {mapdir}/index.json URLs from a gallery landing page."""
    if not html:
        return []
    site = urlparse(site_url)
    dirs = []
    seen_dirs = set()
    for raw in ORIGO_HREF_RE.findall(html):
        raw = (raw or "").strip()
        if not raw:
            continue
        lower = raw.lower()
        if lower.startswith(("javascript:", "mailto:", "tel:", "data:")):
            continue
        parsed = urlparse(urljoin(site_url, raw))
        if parsed.netloc.lower() != site.netloc.lower():
            continue
        path = parsed.path or "/"
        last = path.rsplit("/", 1)[-1]
        if "." in last:
            ext = last.rsplit(".", 1)[-1].lower()
            if ext in {"html", "htm"}:
                path = path.rsplit("/", 1)[0]
            elif ext in ORIGO_GALLERY_SKIP_EXT:
                continue
            else:
                continue
        parts = [p for p in path.split("/") if p]
        if not parts:
            continue
        if any(p.lower() in ORIGO_GALLERY_SKIP_PARTS for p in parts):
            continue
        dir_url = urlunparse(
            (parsed.scheme, parsed.netloc, "/" + "/".join(parts), "", "", "")
        ).rstrip("/")
        if dir_url not in seen_dirs:
            seen_dirs.add(dir_url)
            dirs.append(dir_url)
        if len(dirs) >= ORIGO_GALLERY_MAX_DIRS:
            break
    found = []
    seen = set()
    for directory in dirs:
        for name in ("index.json", "index_ssl.json"):
            url = f"{directory}/{name}"
            if url not in seen:
                seen.add(url)
                found.append(url)
    return found


def origo_config_urls_from_page(site_url, session=None, timeout=DEFAULT_TIMEOUT):
    """Fetch a viewer page and read Origo('*.json') or gallery map dirs."""
    logger = logging.getLogger(__name__)
    getter = session.get if session is not None else requests.get
    try:
        response = getter(
            site_url,
            verify=False,
            headers={"User-Agent": USER_AGENT},
            timeout=(timeout, timeout),
        )
    except (requests.exceptions.Timeout, requests.exceptions.SSLError, ConnectionError, TooManyRedirects):
        logger.info("Origo viewer unavailable for %s", site_url)
        return []
    if getattr(response, "status_code", None) != 200:
        return []
    page_url = getattr(response, "url", None) or site_url
    named = origo_parse_config_urls(response.text, page_url)
    if named:
        return named
    return origo_parse_gallery_config_urls(response.text, page_url)


def atmmaggioli_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "/transparencia/datos/catalogo" in path:
        return _origin_url(url)
    return url.rstrip("/")


def odweb_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "/odweb" in path:
        return _origin_url(url)
    return url.rstrip("/")


def duva_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "/informationsportal" in path:
        return _origin_url(url)
    return url.rstrip("/")


def beyond2020_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "reportfolders" in path:
        return _origin_url(url)
    return url.rstrip("/")


def tr32db_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "/site/index.php" in path or path.rstrip("/").endswith("/site"):
        return _origin_url(url)
    return url.rstrip("/")


def codalab_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "/competitions" in path:
        return _origin_url(url)
    return url.rstrip("/")


def dgbasweb_url_cleanup_func(url):
    path = (urlparse(url).path or "").lower()
    if "/dgbasweb" in path:
        return _origin_url(url)
    return url.rstrip("/")


def hubzero_url_cleanup_func(url):
    return _origin_url(url)


def palapa_url_cleanup_func(url):
    """Strip /geoserver, /gspalapa, and /main so CSW and WMS attach at origin."""
    parsed = urlparse(url)
    parts = [part for part in (parsed.path or "").lower().split("/") if part]
    if "geoserver" in parts or "gspalapa" in parts or "main" in parts:
        return _origin_url(url)
    return url.rstrip("/")


def talkbank_url_cleanup_func(url):
    """Strip data.html so /data.html attaches at the bank origin."""
    path = (urlparse(url).path or "").rstrip("/").lower()
    if path.endswith("data.html"):
        return _origin_url(url)
    return url.rstrip("/")


def materialscloud_url_cleanup_func(url):
    """Strip /explore so the Explore listing is not doubled."""
    path = (urlparse(url).path or "").rstrip("/").lower()
    if path.endswith("/explore") or path == "explore":
        return _origin_url(url)
    return url.rstrip("/")


def icat_url_cleanup_func(url):
    """Strip /icat/portlet so the portlet listing is not doubled."""
    path = (urlparse(url).path or "").rstrip("/").lower()
    if "/icat/portlet" in path:
        return _origin_url(url)
    return url.rstrip("/")


def ramadda_url_cleanup_func(url):
    """Strip /repository so /repository/entry/show is not doubled."""
    path = (urlparse(url).path or "").rstrip("/").lower()
    if path.endswith("/repository") or path == "repository":
        return _origin_url(url)
    return url.rstrip("/")


def _strip_path_marker(url, marker):
    """Drop marker and everything after it; keep any path prefix before marker."""
    parsed = urlparse(url)
    path = parsed.path or ""
    idx = path.lower().find(marker)
    if idx == -1:
        return url.rstrip("/")
    kept = path[:idx].rstrip("/") or "/"
    if kept == "/":
        return _origin_url(url)
    return urlunparse((parsed.scheme, parsed.netloc, kept, "", "", ""))


def erdasapollo_url_cleanup_func(url):
    """Strip /erdas-iws and /erdas-apollo so /erdas-iws/ogc/wms/ is not doubled."""
    lower = (urlparse(url).path or "").lower()
    if "/erdas-iws" in lower:
        return _strip_path_marker(url, "/erdas-iws")
    if "/erdas-apollo" in lower:
        return _strip_path_marker(url, "/erdas-apollo")
    return url.rstrip("/")


def frostserver_url_cleanup_func(url):
    """Strip /FROST-Server so /FROST-Server/v1.1/ probes are not doubled.

    Leave /sensorthings/, /sta/, /server/, and UI /dataportaal/ mounts so
    origin /v1.1/ concatenates onto those catalog links.
    """
    if "/frost-server" in (urlparse(url).path or "").lower():
        return _strip_path_marker(url, "/frost-server")
    return url.rstrip("/")


def cubewerx_url_cleanup_func(url):
    """Strip /cubewerx so harvest /cubewerx/cubeserv GetCapabilities is not doubled."""
    if "/cubewerx" in (urlparse(url).path or "").lower():
        return _strip_path_marker(url, "/cubewerx")
    return url.rstrip("/")


def greenstone_url_cleanup_func(url):
    """Strip /greenstone3 and /greenstone so OAI Identify attaches at origin."""
    lower = (urlparse(url).path or "").lower()
    if "/greenstone3" in lower:
        return _strip_path_marker(url, "/greenstone3")
    if "/greenstone" in lower:
        return _strip_path_marker(url, "/greenstone")
    return url.rstrip("/")


def bitrix_url_cleanup_func(url):
    """Strip /opendata so /opendata/opendata.json is not doubled."""
    if "/opendata" in (urlparse(url).path or "").lower():
        return _strip_path_marker(url, "/opendata")
    return url.rstrip("/")


def massbank_url_cleanup_func(url):
    """Strip /MassBank so /MassBank/api/records is not doubled."""
    if "/massbank" in (urlparse(url).path or "").lower():
        return _strip_path_marker(url, "/massbank")
    return url.rstrip("/")


def nada_url_cleanup_func(url):
    """Strip /index.php so /index.php/api/catalog/search is not doubled."""
    if "/index.php" in (urlparse(url).path or "").lower():
        return _strip_path_marker(url, "/index.php")
    return url.rstrip("/")


def stacbrowser_url_cleanup_func(url):
    """Strip trailing catalog.json so /catalog.json is not doubled."""
    path = (urlparse(url).path or "").rstrip("/").lower()
    if path.endswith("catalog.json"):
        return _strip_path_marker(url, "/catalog.json")
    return url.rstrip("/")


def _path_has_segment(url, segment):
    parts = [part for part in (urlparse(url).path or "").lower().split("/") if part]
    return segment.lower() in parts


def micka_url_cleanup_func(url):
    """Strip /micka so /micka/csw GetCapabilities is not doubled."""
    if _path_has_segment(url, "micka"):
        return _strip_path_marker(url, "/micka")
    return url.rstrip("/")


def wis20box_url_cleanup_func(url):
    """Strip /oapi so /oapi/collections probes are not doubled."""
    if _path_has_segment(url, "oapi"):
        return _strip_path_marker(url, "/oapi")
    return url.rstrip("/")


def symbiota_url_cleanup_func(url):
    """Strip /portal and /collections so harvest collection paths are not doubled."""
    if _path_has_segment(url, "portal"):
        return _strip_path_marker(url, "/portal")
    if _path_has_segment(url, "collections"):
        return _strip_path_marker(url, "/collections")
    return url.rstrip("/")


def lkod_url_cleanup_func(url):
    """Strip /opendata so /opendata/set/lkod is not doubled."""
    if _path_has_segment(url, "opendata"):
        return _strip_path_marker(url, "/opendata")
    return url.rstrip("/")


def deegree_url_cleanup_func(url):
    """Strip /deegree-webservices so prefixed /services probes are not doubled.

    Leave /m4eu/, /geoproxy/, and xPlanBox mounts so origin /services
    concatenates onto those catalog links.
    """
    if _path_has_segment(url, "deegree-webservices"):
        return _strip_path_marker(url, "/deegree-webservices")
    return url.rstrip("/")


def flat_url_cleanup_func(url):
    """Strip /flat so /flat/oai2 Identify is not doubled."""
    if _path_has_segment(url, "flat"):
        return _strip_path_marker(url, "/flat")
    return url.rstrip("/")


def dlibra_url_cleanup_func(url):
    """Strip /dlibra so /dlibra/oai-pmh-repository.xml is not doubled."""
    if _path_has_segment(url, "dlibra"):
        return _strip_path_marker(url, "/dlibra")
    return url.rstrip("/")


def gipuzkoairekia_url_cleanup_func(url):
    """Origin dumps for subdomain tenants; keep www /es/web/{tenant}/ paths."""
    host = (urlparse(url).netloc or "").lower()
    if host in {"www.gipuzkoairekia.eus", "gipuzkoairekia.eus"}:
        return url.rstrip("/")
    if _path_has_segment(url, "datu-irekien-katalogoa"):
        return _origin_url(url)
    return url.rstrip("/")


def esrigeo_url_cleanup_func(url):
    """Strip /geoportal so /geoportal/openSearchDescription is not doubled."""
    if _path_has_segment(url, "geoportal"):
        return _strip_path_marker(url, "/geoportal")
    return url.rstrip("/")


URL_CLEANUP_MAP = {
    "istatdatabrowser": istatdatabrowser_url_cleanup_func,
    "geoserver": geoserver_url_cleanup_func,
    "arcgisserver": arcgisserver_url_cleanup_func,
    "geonetwork": geonetwork_url_cleanup_func,
    "thredds": thredds_url_cleanup_func,
    "erddap": erddap_url_cleanup_func,
    "ala": ala_url_cleanup_func,
    "lizmap": lizmap_url_cleanup_func,
    "mapbender": mapbender_url_cleanup_func,
    "nesstar": nesstar_url_cleanup_func,
    "opus": opus_url_cleanup_func,
    "geomapfish": geomapfish_url_cleanup_func,
    "getsdiportal": getsdiportal_url_cleanup_func,
    "redatam": redatam_url_cleanup_func,
    "nextgisweb": nextgisweb_url_cleanup_func,
    "supermapiserver": supermapiserver_url_cleanup_func,
    "supermapiportal": supermapiportal_url_cleanup_func,
    "mapgisigserver": mapgisigserver_url_cleanup_func,
    "tianditu": tianditu_url_cleanup_func,
    "cogis": cogis_url_cleanup_func,
    "elitegis": cogis_url_cleanup_func,
    "geocortex": geocortex_url_cleanup_func,
    "minerva": minerva_url_cleanup_func,
    "gringlobal": gringlobal_url_cleanup_func,
    "g3wsuite": g3wsuite_url_cleanup_func,
    "dataone": dataone_url_cleanup_func,
    "yoda": yoda_url_cleanup_func,
    "origo": origo_url_cleanup_func,
    "swing": swing_url_cleanup_func,
    "atmmaggioli": atmmaggioli_url_cleanup_func,
    "odweb": odweb_url_cleanup_func,
    "duva": duva_url_cleanup_func,
    "beyond2020": beyond2020_url_cleanup_func,
    "tr32db": tr32db_url_cleanup_func,
    "codalab": codalab_url_cleanup_func,
    "dgbasweb": dgbasweb_url_cleanup_func,
    "hubzero": hubzero_url_cleanup_func,
    "copernicusdhus": copernicusdhus_url_cleanup_func,
    "cbioportal": _origin_url,
    "huggingface": _origin_url,
    "palapa": palapa_url_cleanup_func,
    "talkbank": talkbank_url_cleanup_func,
    "materialscloud": materialscloud_url_cleanup_func,
    "icat": icat_url_cleanup_func,
    "ramadda": ramadda_url_cleanup_func,
    "erdasapollo": erdasapollo_url_cleanup_func,
    "frostserver": frostserver_url_cleanup_func,
    "cubewerx": cubewerx_url_cleanup_func,
    "greenstone": greenstone_url_cleanup_func,
    "bitrix": bitrix_url_cleanup_func,
    "massbank": massbank_url_cleanup_func,
    "nada": nada_url_cleanup_func,
    "stacbrowser": stacbrowser_url_cleanup_func,
    "micka": micka_url_cleanup_func,
    "wis20box": wis20box_url_cleanup_func,
    "symbiota": symbiota_url_cleanup_func,
    "lkod": lkod_url_cleanup_func,
    "deegree": deegree_url_cleanup_func,
    "flat": flat_url_cleanup_func,
    "dlibra": dlibra_url_cleanup_func,
    "gipuzkoairekia": gipuzkoairekia_url_cleanup_func,
    "esrigeo": esrigeo_url_cleanup_func,
}


OPENSDG_REMOTE_DATA_RE = re.compile(
    r"remoteDataBaseUrl\s*:\s*['\"]([^'\"]+)['\"]"
)


def opensdg_parse_remote_data_base_url(html, site_url):
    """Return the Open SDG data-repo base from homepage JS, or None."""
    if not html:
        return None
    match = OPENSDG_REMOTE_DATA_RE.search(html)
    if not match:
        return None
    raw = match.group(1).strip()
    if not raw or raw in {".", "/", "./"}:
        return None
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw.rstrip("/")
    return urljoin(site_url.rstrip("/") + "/", raw).rstrip("/")


def opensdg_remote_data_base_url(site_url, session=None, timeout=DEFAULT_TIMEOUT):
    """Fetch an Open SDG homepage and read opensdg.remoteDataBaseUrl."""
    logger = logging.getLogger(__name__)
    getter = session.get if session is not None else requests.get
    try:
        response = getter(
            site_url,
            verify=False,
            headers={"User-Agent": USER_AGENT},
            timeout=(timeout, timeout),
        )
    except (requests.exceptions.Timeout, requests.exceptions.SSLError, ConnectionError, TooManyRedirects):
        logger.info("Open SDG homepage unavailable for %s", site_url)
        return None
    if getattr(response, "status_code", None) != 200:
        return None
    return opensdg_parse_remote_data_base_url(response.text, site_url)


def _probe_request_url(item, base_url, original_url):
    if item.get("absolute_url"):
        return item["absolute_url"]
    if item.get("use_original_url"):
        return original_url
    return base_url + item["url"]


def _collect_probe_jobs(base_urls, umap, original_url):
    jobs = []
    tried_urls = set()
    for base_url in base_urls:
        for item in umap:
            request_url = _probe_request_url(item, base_url, original_url)
            if request_url in tried_urls:
                continue
            tried_urls.add(request_url)
            jobs.append((len(jobs), item, request_url, base_url))
    return jobs


def _probe_one(session, item, request_url, base_url, timeout, verify_json):
    """GET/POST one URL-map item. Returns (endpoint_or_none, failure_or_none)."""
    logger = logging.getLogger(__name__)
    logger.info("Requesting %s", request_url)
    try:
        if "post_params" in item.keys():
            headers = {"User-Agent": USER_AGENT}
            if "accept" in item.keys():
                headers["Accept"] = item["accept"]
            response = session.post(
                request_url,
                verify=False,
                headers=headers,
                json=json.loads(item["post_params"]),
                timeout=(timeout, timeout),
            )
        else:
            response = None
            if "prefetch" in item and item["prefetch"]:
                response = session.get(
                    request_url,
                    headers={"User-Agent": USER_AGENT},
                    timeout=(timeout, timeout),
                )
            if response is None and "accept" in item.keys():
                response = session.get(
                    request_url,
                    verify=False,
                    headers={"User-Agent": USER_AGENT, "Accept": item["accept"]},
                    timeout=(timeout, timeout),
                )
            elif response is None:
                response = session.get(
                    request_url,
                    verify=False,
                    headers={"User-Agent": USER_AGENT},
                    timeout=(timeout, timeout),
                )
        if response.status_code != 200:
            return None, {
                "url": request_url,
                "status": response.status_code,
                "mime": (
                    response.headers["Content-Type"].split(";", 1)[0].lower()
                    if "content-type" in response.headers.keys()
                    else ""
                ),
                "error": "Wrong status",
            }
    except requests.exceptions.Timeout:
        return None, {"url": request_url, "error": "Timeout"}
    except requests.exceptions.SSLError:
        return None, {"url": request_url, "error": "SSL Error"}
    except ConnectionError:
        return None, {"url": request_url, "error": "no connection"}
    except TooManyRedirects:
        return None, {"url": request_url, "error": "no connection"}
    except ContentDecodingError:
        return None, {"url": request_url, "error": "content error"}
    except (InvalidURL, RequestException, ValueError) as e:
        return None, {"url": request_url, "error": type(e).__name__}
    logger.info("Finished request to %s", request_url)
    if (
        "expected_mime" in item.keys()
        and item["expected_mime"] is not None
        and "Content-Type" in response.headers.keys()
    ):
        if verify_json:
            if "is_json" in item.keys() and item["is_json"]:
                try:
                    json.loads(response.content)
                except (json.JSONDecodeError, ValueError, TypeError):
                    return None, {
                        "url": request_url,
                        "status": response.status_code,
                        "mime": response.headers["Content-Type"]
                        .split(";", 1)[0]
                        .lower(),
                        "error": "Error loading JSON",
                    }
        expected_mime = item["expected_mime"]
        if isinstance(expected_mime, str):
            expected_mime = [expected_mime]
        if (
            response.headers["Content-Type"].split(";", 1)[0].lower()
            not in expected_mime
        ):
            return None, {
                "url": request_url,
                "status": response.status_code,
                "mime": response.headers["Content-Type"].split(";", 1)[0].lower(),
                "error": "Wrong content type",
            }
    api = {
        "type": item["id"],
        "url": (
            base_url + item["display_url"]
            if "display_url" in item.keys()
            else request_url
        ),
    }
    if item["version"]:
        api["version"] = item["version"]
    if "urlpat" in item.keys():
        api["url_pattern"] = item["urlpat"]
    return api, None


def _run_probe_jobs(jobs, timeout, verify_json, probe_workers, session=None):
    """Run URL-map probes; preserve map order in the returned endpoint list."""
    found_slots = [None] * len(jobs)
    results = []
    workers = DEFAULT_PROBE_WORKERS if probe_workers is None else probe_workers

    def _run(job, sess):
        _idx, item, request_url, base_url = job
        return _idx, *_probe_one(
            sess, item, request_url, base_url, timeout, verify_json
        )

    if workers <= 1 or len(jobs) <= 1:
        sess = session if session is not None else requests.Session()
        for job in jobs:
            idx, api, fail = _run(job, sess)
            if api is not None:
                found_slots[idx] = api
            if fail is not None:
                results.append(fail)
    else:
        def _run_threaded(job):
            return _run(job, requests.Session())

        pool_size = max(1, min(workers, len(jobs)))
        with ThreadPoolExecutor(max_workers=pool_size) as pool:
            futures = [pool.submit(_run_threaded, job) for job in jobs]
            for fut in as_completed(futures):
                try:
                    idx, api, fail = fut.result()
                except Exception as exc:
                    logging.getLogger(__name__).exception(
                        "Probe worker failed: %s", exc
                    )
                    continue
                if api is not None:
                    found_slots[idx] = api
                if fail is not None:
                    results.append(fail)
    found = [api for api in found_slots if api is not None]
    return found, results


def api_identifier(
    website_url,
    software_id,
    verify_json=False,
    deep=False,
    timeout=DEFAULT_TIMEOUT,
    probe_workers=None,
):
    logger = logging.getLogger(__name__)
    url_map = CATALOGS_URLMAP[software_id]
    s = requests.Session()
    original_url = website_url
    if software_id in {"scicat", "gin"}:
        host = urlparse(website_url).netloc.split(":")[0].lower()
        if host.startswith("doi."):
            logger.info("Skipping %s DOI landing host %s", software_id, host)
            return []
    #
    if software_id in URL_CLEANUP_MAP:
        website_url = URL_CLEANUP_MAP[software_id](website_url)
    else:
        website_url = website_url.rstrip("/")
    
    # For GeoServer, try multiple base URL variations to handle non-standard paths
    base_urls = [website_url]
    geoserver_fast = False
    if software_id == "geoserver":
        parsed = urlparse(website_url)
        if "/geoserver" in (parsed.path or "").lower():
            gs_root = geoserver_root_url(website_url)
            base_urls = [gs_root]
            geoserver_fast = True
        else:
            # If URL doesn't end with /geoserver, try adding it
            if not website_url.endswith("/geoserver"):
                base_urls.append(website_url + "/geoserver")
    if software_id in (
        "mapstore",
        "getsdiportal",
        "giswebse",
        "gvsigonline",
        "erdasapollo",
        "cogis",
        "tianditu",
        "contentdm",
        "idra",
        "omekas",
        "piveau",
        "fairdatapoint",
        "resourcecontracts",
        "symbiota",
        "geocortex",
        "minerva",
        "g3wsuite",
        "geonature",
        "aubrey",
        "hajk",
        "activemapgis",
        "tergis",
        "opengov",
        "opendatacube",
        "origo",
        "swing",
        "atmmaggioli",
        "odweb",
        "duva",
        "beyond2020",
        "tr32db",
        "codalab",
        "dgbasweb",
        "hubzero",
        "idra",
        "librecat",
    ):
        parsed = urlparse(website_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin.rstrip("/") != website_url.rstrip("/"):
            base_urls.append(origin)
    if software_id == "origo":
        parsed = urlparse(website_url)
        origo_root = f"{parsed.scheme}://{parsed.netloc}/origo"
        if origo_root.rstrip("/") not in [item.rstrip("/") for item in base_urls]:
            base_urls.append(origo_root)
    if software_id == "geonature":
        parsed = urlparse(website_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        path = (parsed.path or "").rstrip("/").lower()
        if not path.endswith("/atlas"):
            atlas = origin.rstrip("/") + "/atlas"
            if atlas.rstrip("/") not in [item.rstrip("/") for item in base_urls]:
                base_urls.append(atlas)
    if software_id == "oskari":
        if "/oskari" not in (urlparse(website_url).path or "").lower():
            base_urls.append(website_url.rstrip("/") + "/oskari")
    if software_id == "opensdg":
        remote = opensdg_remote_data_base_url(
            original_url, session=s, timeout=timeout
        )
        if remote and remote.rstrip("/") not in [item.rstrip("/") for item in base_urls]:
            base_urls.append(remote)
    
    umap = url_map.copy()
    if geoserver_fast and not deep:
        umap = GEOSERVER_FAST_URLMAP.copy()
    if software_id == "redatam" and "rpwebengine.exe" in original_url.lower():
        umap = [
            {
                "id": "redatam",
                "url": "",
                "use_original_url": True,
                "expected_mime": HTML_MIMETYPES,
                "is_json": False,
                "version": None,
            }
        ] + umap
    if software_id != "custom" and deep:
        umap.extend(CUSTOM_URLMAP)
    if software_id == "origo":
        for abs_url in origo_config_urls_from_page(
            original_url, session=s, timeout=timeout
        ):
            umap.append(
                {
                    "id": "origo:config",
                    "url": "",
                    "absolute_url": abs_url,
                    "accept": "application/json",
                    "expected_mime": JSON_MIMETYPES,
                    "is_json": True,
                    "version": None,
                }
            )
    
    jobs = _collect_probe_jobs(base_urls, umap, original_url)
    found, results = _run_probe_jobs(
        jobs,
        timeout,
        verify_json,
        probe_workers,
        session=s,
    )
    if software_id == "nyudatacatalog":
        for item in analyze_root(original_url):
            if item.get("type") != "schemaorg:datacatalog":
                continue
            if any(
                existing.get("type") == item.get("type")
                and existing.get("url") == item.get("url")
                for existing in found
            ):
                continue
            found.append(item)
    if deep:
        logger.info("Going deep")
        for func in DEEP_SEARCH_FUNCTIONS:
            extracted = func(website_url)
            if len(extracted) > 0:
                found.extend(extracted)
    logger.info("Failures: %s", results)
    return found


def infer_endpoints_verified(record, timeout=DEFAULT_TIMEOUT):
    """Return HTTP-verified harvest endpoints for a catalog record.

    Quality-fix scripts used to construct CKAN/GeoServer/sitemap URLs without a
    GET check. Only software in CATALOGS_URLMAP is probed. The generic `custom`
    map (sitemap/data.json) is skipped so quality fixers do not crawl every
    unclassified catalog. Unknown platforms return an empty list instead of an
    unverified /sitemap.xml fallback.
    """
    software = record.get("software") or {}
    software_id = (software.get("id") or "").strip()
    link = (record.get("link") or "").strip()
    if (
        not link
        or software_id not in CATALOGS_URLMAP
        or software_id == "custom"
    ):
        return []
    try:
        return api_identifier(link.rstrip("/"), software_id, timeout=timeout)
    except Exception:
        return []


def __detect_one(
    filename,
    record,
    software,
    action,
    deep,
    filepath,
    timeout=DEFAULT_TIMEOUT,
    dryrun=False,
    probe_workers=None,
):
    logger = logging.getLogger(__name__)
    logger.info("Processing %s", os.path.basename(filename).split(".", 1)[0])
    if (
        "endpoints" in record.keys()
        and len(record["endpoints"]) > 0
        and action == "insert"
    ):
        logger.info(
            " - skip, we have endpoints already and not in replace or update mode"
        )
        return
    found = api_identifier(
        record["link"].rstrip("/"),
        software,
        deep=deep,
        timeout=timeout,
        probe_workers=probe_workers,
    )
    keys = []
    if action == "update":
        if "endpoints" in record.keys() and len(record["endpoints"]) > 0:
            for e in record["endpoints"]:
                if "url" in e.keys():
                    keys.append(e["url"])
        else:
            record["endpoints"] = []
    else:
        record["endpoints"] = []
    added = 0
    for api in found:
        if api["url"] not in keys:
            logger.info("- %s %s", api["type"], api["url"])
            record["endpoints"].append(api)
            keys.append(api["url"])
            added += 1
    logger.info("Found %d, added %d", len(found), added)
    if added > 0:
        record["api"] = True
        record["api_status"] = "active"
        if dryrun:
            logger.info("- dryrun enabled, profile not updated")
        else:
            _save_record(filepath, record)
            logger.info("- updated profile")
    else:
        logger.info("- no endpoints or no new endpoints, not updated")


def _resolve_root_dir(mode):
    return ENTRIES_DIR if mode == "entries" else SCHEDULED_DIR


def _iter_yaml_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for fi in files:
            if fi.endswith(".yaml"):
                yield os.path.join(root, fi)


def _yaml_id_glob_paths(root_dir, uniqid):
    """Return YAML paths whose filename is `{uniqid}.yaml`, or None to walk."""
    token = str(uniqid).strip()
    if (
        not token
        or "://" in token
        or os.path.basename(token) != token
        or token in {".", ".."}
    ):
        return None
    hits = glob.glob(os.path.join(root_dir, "**", f"{token}.yaml"), recursive=True)
    return hits or None


def _collect_matching_records(root_dir, match, load_workers=None):
    files = list(_iter_yaml_files(root_dir))
    workers = DEFAULT_RECORD_WORKERS if load_workers is None else load_workers

    def _load_pair(filepath):
        record = _load_record(filepath)
        if match(record):
            return filepath, record
        return None

    if workers <= 1 or len(files) <= 1:
        out = []
        for filepath in files:
            pair = _load_pair(filepath)
            if pair is not None:
                out.append(pair)
        return out
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return [pair for pair in pool.map(_load_pair, files, chunksize=32) if pair]


def _run_record_jobs(jobs, runner, record_workers):
    workers = DEFAULT_RECORD_WORKERS if record_workers is None else record_workers
    logger = logging.getLogger(__name__)

    def _safe(job):
        try:
            runner(job)
        except Exception:
            label = job[0] if isinstance(job, tuple) and job else job
            logger.exception("Catalog job failed: %s", label)

    if workers <= 1 or len(jobs) <= 1:
        for job in jobs:
            _safe(job)
        return
    with ThreadPoolExecutor(max_workers=min(workers, len(jobs))) as pool:
        list(pool.map(_safe, jobs))


def _load_record(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        return yaml.load(f, Loader=Loader)


def _save_record(filepath, record):
    with _SAVE_LOCK:
        with open(filepath, "w", encoding="utf8") as f:
            yaml.dump(
                record,
                f,
                Dumper=Dumper,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
            )


def _detect_record(
    filename,
    filepath,
    record,
    action,
    deep,
    timeout=DEFAULT_TIMEOUT,
    dryrun=False,
    include_custom=False,
    probe_workers=None,
):
    software_id = ((record.get("software") or {}).get("id") or "").strip()
    if software_id not in CATALOGS_URLMAP:
        if not include_custom:
            return
        software_id = "custom"
    elif software_id == "custom" and not include_custom:
        return
    __detect_one(
        filename,
        record,
        software_id,
        action,
        deep,
        filepath,
        timeout=timeout,
        dryrun=dryrun,
        probe_workers=probe_workers,
    )


def _replace_detected_endpoints(
    filepath, record, software_id, base_url=None, dryrun=False, probe_workers=None
):
    logger = logging.getLogger(__name__)
    detection_base = base_url if base_url else record["link"].rstrip("/")
    found = api_identifier(detection_base, software_id, probe_workers=probe_workers)
    record["endpoints"] = []
    for api in found:
        logger.info("- %s %s", api["type"], api["url"])
        record["endpoints"].append(api)
    if len(record["endpoints"]) > 0:
        if dryrun:
            logger.info("- dryrun enabled, profile not updated")
        else:
            _save_record(filepath, record)
            logger.info("- updated profile")
    else:
        logger.info("- no endpoints, not updated")


@app.command()
def detect_software(
    software,
    dryrun: Annotated[bool, typer.Option("--dryrun")] = False,
    action: Annotated[str, typer.Option("--action")] = "insert",
    mode: str = "entries",
    deep: bool = False,
    include_custom: Annotated[
        bool,
        typer.Option(
            "--include-custom",
            help="Probe custom catalogs with CUSTOM_URLMAP. Required for software id custom.",
        ),
    ] = False,
    max_endpoints: Annotated[
        Optional[int],
        typer.Option(
            "--max-endpoints",
            help="Only process records with fewer than N endpoints. Use 1 for records with no endpoints.",
        ),
    ] = None,
    workers: Annotated[
        int,
        typer.Option(
            "--workers",
            help="Parallel catalog jobs (YAML load + per-record probes). Use 1 for sequential.",
        ),
    ] = DEFAULT_RECORD_WORKERS,
    probe_workers: Annotated[
        int,
        typer.Option(
            "--probe-workers",
            help="Parallel HTTP probes per catalog. Use 1 for sequential probes.",
        ),
    ] = DEFAULT_PROBE_WORKERS,
):
    """Enrich data catalogs with API endpoints by software"""
    root_dir = _resolve_root_dir(mode)

    def _match(record):
        if record["software"]["id"] != software:
            return False
        if max_endpoints is not None:
            return len(record.get("endpoints", [])) < max_endpoints
        return True

    jobs = _collect_matching_records(root_dir, _match, load_workers=workers)

    def _run(job):
        filepath, record = job
        _detect_record(
            filepath,
            filepath,
            record,
            action,
            deep,
            dryrun=dryrun,
            include_custom=include_custom,
            probe_workers=probe_workers,
        )

    _run_record_jobs(jobs, _run, workers)


@app.command()
def detect_single(
    uniqid,
    dryrun: Annotated[bool, typer.Option("--dryrun")] = False,
    action: Annotated[str, typer.Option("--action")] = "insert",
    mode: str = "entries",
    deep: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
    include_custom: Annotated[
        bool,
        typer.Option(
            "--include-custom",
            help="Probe custom catalogs with CUSTOM_URLMAP.",
        ),
    ] = False,
    probe_workers: Annotated[
        int,
        typer.Option(
            "--probe-workers",
            help="Parallel HTTP probes. Use 1 for sequential probes.",
        ),
    ] = DEFAULT_PROBE_WORKERS,
):
    """Enrich single data catalog with API endpoints"""
    root_dir = _resolve_root_dir(mode)
    found = False
    paths = _yaml_id_glob_paths(root_dir, uniqid)
    if paths is None:
        paths = _iter_yaml_files(root_dir)
    for filepath in paths:
        record = _load_record(filepath)
        idkeys = []
        for k in ["uid", "id", "link"]:
            if k in record.keys():
                idkeys.append(record[k])
        if uniqid not in idkeys:
            continue
        found = True
        _detect_record(
            filepath,
            filepath,
            record,
            action,
            deep,
            timeout=timeout,
            dryrun=dryrun,
            include_custom=include_custom,
            probe_workers=probe_workers,
        )
    if not found:
        logging.getLogger(__name__).info("No catalog matched %s", uniqid)


@app.command()
def detect_country(
    country,
    dryrun: Annotated[bool, typer.Option("--dryrun")] = False,
    action: Annotated[str, typer.Option("--action")] = "insert",
    mode: str = "entries",
    deep: bool = False,
    include_custom: Annotated[
        bool,
        typer.Option(
            "--include-custom",
            help="Probe custom catalogs with CUSTOM_URLMAP.",
        ),
    ] = False,
    workers: Annotated[
        int,
        typer.Option(
            "--workers",
            help="Parallel catalog jobs. Use 1 for sequential.",
        ),
    ] = DEFAULT_RECORD_WORKERS,
    probe_workers: Annotated[
        int,
        typer.Option(
            "--probe-workers",
            help="Parallel HTTP probes per catalog. Use 1 for sequential probes.",
        ),
    ] = DEFAULT_PROBE_WORKERS,
):
    """Enrich data catalogs with API endpoints by country"""
    root_dir = _resolve_root_dir(mode)
    jobs = _collect_matching_records(
        root_dir,
        lambda record: record["owner"]["location"]["country"]["id"] == country,
        load_workers=workers,
    )

    def _run(job):
        filepath, record = job
        _detect_record(
            filepath,
            filepath,
            record,
            action,
            deep,
            dryrun=dryrun,
            include_custom=include_custom,
            probe_workers=probe_workers,
        )

    _run_record_jobs(jobs, _run, workers)


@app.command()
def detect_cattype(
    catalogtype,
    dryrun: Annotated[bool, typer.Option("--dryrun")] = False,
    action: Annotated[str, typer.Option("--action")] = "insert",
    mode: str = "entries",
    deep: bool = False,
    include_custom: Annotated[
        bool,
        typer.Option(
            "--include-custom",
            help="Probe custom catalogs with CUSTOM_URLMAP.",
        ),
    ] = False,
    workers: Annotated[
        int,
        typer.Option(
            "--workers",
            help="Parallel catalog jobs. Use 1 for sequential.",
        ),
    ] = DEFAULT_RECORD_WORKERS,
    probe_workers: Annotated[
        int,
        typer.Option(
            "--probe-workers",
            help="Parallel HTTP probes per catalog. Use 1 for sequential probes.",
        ),
    ] = DEFAULT_PROBE_WORKERS,
):
    """Enrich data catalogs with API endpoints by catalog type"""
    root_dir = _resolve_root_dir(mode)
    jobs = _collect_matching_records(
        root_dir,
        lambda record: record["catalog_type"] == catalogtype,
        load_workers=workers,
    )

    def _run(job):
        filepath, record = job
        _detect_record(
            filepath,
            filepath,
            record,
            action,
            deep,
            dryrun=dryrun,
            include_custom=include_custom,
            probe_workers=probe_workers,
        )

    _run_record_jobs(jobs, _run, workers)


@app.command()
def detect_ckan(
    dryrun=False,
    replace_endpoints=True,
    mode="entries",
    workers: Annotated[
        int,
        typer.Option("--workers", help="Parallel catalog jobs. Use 1 for sequential."),
    ] = DEFAULT_RECORD_WORKERS,
    probe_workers: Annotated[
        int,
        typer.Option(
            "--probe-workers",
            help="Parallel HTTP probes per catalog. Use 1 for sequential probes.",
        ),
    ] = DEFAULT_PROBE_WORKERS,
):
    """Enrich data catalogs with API endpoints by CKAN instance (special function to update all endpoints"""
    root_dir = _resolve_root_dir(mode)
    jobs = _collect_matching_records(
        root_dir,
        lambda record: record["software"]["id"] == "ckan",
        load_workers=workers,
    )

    def _run(job):
        filepath, record = job
        logger = logging.getLogger(__name__)
        logger.info("Processing %s", os.path.basename(filepath).split(".", 1)[0])
        if "endpoints" in record.keys() and len(record["endpoints"]) > 1:
            logger.info(" - skip, we have more than 2 endpoints so we skip")
            return
        if (
            "endpoints" in record.keys()
            and len(record["endpoints"]) == 1
            and record["endpoints"][0]["type"] == "ckanapi"
        ):
            base_url = record["endpoints"][0]["url"][0:-6]
        else:
            base_url = record["link"].rstrip("/")
        _replace_detected_endpoints(
            filepath,
            record,
            record["software"]["id"],
            base_url=base_url,
            dryrun=dryrun,
            probe_workers=probe_workers,
        )

    _run_record_jobs(jobs, _run, workers)


@app.command()
def detect_all(
    status="undetected",
    replace_endpoints: Annotated[bool, typer.Option("--replace")] = False,
    mode="entries",
    include_custom: Annotated[
        bool,
        typer.Option(
            "--include-custom",
            help="Include custom software.id catalogs when walking all maps.",
        ),
    ] = False,
    workers: Annotated[
        int,
        typer.Option("--workers", help="Parallel catalog jobs. Use 1 for sequential."),
    ] = DEFAULT_RECORD_WORKERS,
    probe_workers: Annotated[
        int,
        typer.Option(
            "--probe-workers",
            help="Parallel HTTP probes per catalog. Use 1 for sequential probes.",
        ),
    ] = DEFAULT_PROBE_WORKERS,
):
    """Detect all known API endpoints"""
    root_dir = _resolve_root_dir(mode)

    def _match(record):
        software_id = record["software"]["id"]
        if software_id == "custom" and not include_custom:
            return False
        if software_id not in CATALOGS_URLMAP.keys():
            return False
        if status == "undetected":
            return "endpoints" not in record.keys() or len(record["endpoints"]) == 0
        return True

    jobs = _collect_matching_records(root_dir, _match, load_workers=workers)

    def _run(job):
        filepath, record = job
        logger = logging.getLogger(__name__)
        logger.info(
            "Processing catalog %s, software %s",
            os.path.basename(filepath).split(".", 1)[0],
            record["software"]["id"],
        )
        if (
            "endpoints" in record.keys()
            and len(record["endpoints"]) > 0
            and replace_endpoints is False
        ):
            logger.info(" - skip, we have endpoints already and no replace mode")
            return
        _replace_detected_endpoints(
            filepath,
            record,
            record["software"]["id"],
            probe_workers=probe_workers,
        )

    _run_record_jobs(jobs, _run, workers)


@app.command()
def report(status="undetected", filename=None, mode="entries"):
    """Report data catalogs with undetected API endpoints"""
    out = sys.stdout if filename is None else open(filename, "w", encoding="utf8")

    root_dir = _resolve_root_dir(mode)

    if status == "undetected":
        out.write(",".join(["id", "uid", "link", "software_id", "status"]) + "\n")
    for filepath in _iter_yaml_files(root_dir):
        record = _load_record(filepath)
        if record["software"]["id"] in CATALOGS_URLMAP.keys():
            if "endpoints" not in record.keys() or len(record["endpoints"]) == 0:
                if status == "undetected":
                    out.write(
                        ",".join(
                            [
                                record["id"],
                                record["uid"],
                                record["link"],
                                record["software"]["id"],
                                "undetected",
                            ]
                        )
                        + "\n"
                    )
    if filename is not None:
        out.close()


@app.command()
def update_broken_arcgis(
    status="undetected",
    replace_endpoints: Annotated[bool, typer.Option("--replace")] = True,
    mode="entries",
):
    """Detect all broken ArcGIS portals and update endpoints"""
    root_dir = _resolve_root_dir(mode)
    for filepath in _iter_yaml_files(root_dir):
        record = _load_record(filepath)
        if record["software"]["id"] in ["arcgishub", "arcgisserver"]:
            if "endpoints" not in record.keys() or len(record["endpoints"]) < 2:
                if status == "undetected":
                    logger = logging.getLogger(__name__)
                    logger.info(
                        "Processing catalog %s, software %s",
                        os.path.basename(filepath).split(".", 1)[0],
                        record["software"]["id"],
                    )
                    if (
                        "endpoints" in record.keys()
                        and len(record["endpoints"]) > 0
                        and replace_endpoints is False
                    ):
                        logger.info(
                            " - skip, we have endpoints already and no replace mode"
                        )
                        continue
                    _replace_detected_endpoints(
                        filepath,
                        record,
                        record["software"]["id"],
                    )


if __name__ == "__main__":
    app()
