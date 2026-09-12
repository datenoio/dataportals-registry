"""Regression tests for apidetect endpoint probing."""

import os
import sys

import pytest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import apidetect


@pytest.fixture(autouse=True)
def _serial_apidetect_workers(monkeypatch):
    """Keep existing Session-queue tests deterministic."""
    monkeypatch.setattr(apidetect, "DEFAULT_PROBE_WORKERS", 1)
    monkeypatch.setattr(apidetect, "DEFAULT_RECORD_WORKERS", 1)


class _DummyResponse:
    def __init__(self, status_code=200, content=b"{}", headers=None, text=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {"Content-Type": "application/json"}
        self.text = text if text is not None else content.decode("utf8", errors="ignore")


class _DummySession:
    def __init__(self, responses):
        self._responses = list(responses)

    def _next(self):
        if not self._responses:
            raise AssertionError("No more fake responses configured")
        return self._responses.pop(0)

    def get(self, *args, **kwargs):
        return self._next()

    def post(self, *args, **kwargs):
        return self._next()


def _patch_session(monkeypatch, responses):
    monkeypatch.setattr(apidetect.requests, "Session", lambda: _DummySession(responses))


def _patch_requests_get(monkeypatch, response):
    monkeypatch.setattr(apidetect.requests, "get", lambda *args, **kwargs: response)


def test_api_identifier_non_200_does_not_add_endpoint(monkeypatch):
    monkeypatch.setitem(
        apidetect.CATALOGS_URLMAP,
        "testsw",
        [{"id": "probe", "url": "/probe", "expected_mime": ["application/json"], "version": None}],
    )
    _patch_session(monkeypatch, [_DummyResponse(status_code=404)])

    found = apidetect.api_identifier("https://example.org", "testsw")

    assert found == []


def test_api_identifier_verify_json_decode_error_is_handled(monkeypatch):
    monkeypatch.setitem(
        apidetect.CATALOGS_URLMAP,
        "testsw",
        [
            {
                "id": "probe",
                "url": "/probe",
                "expected_mime": ["application/json"],
                "is_json": True,
                "version": None,
            }
        ],
    )
    _patch_session(monkeypatch, [_DummyResponse(content=b"{invalid-json}")])

    found = apidetect.api_identifier(
        "https://example.org", "testsw", verify_json=True
    )

    assert found == []


def test_api_identifier_accepts_string_expected_mime(monkeypatch):
    monkeypatch.setitem(
        apidetect.CATALOGS_URLMAP,
        "testsw",
        [
            {
                "id": "probe",
                "url": "/probe",
                "expected_mime": "text/turtle",
                "version": "1.0",
            }
        ],
    )
    _patch_session(
        monkeypatch,
        [
            _DummyResponse(
                headers={"Content-Type": "text/turtle; charset=utf-8"},
                content=b"@prefix ex: <https://example.org/> .",
            )
        ],
    )

    found = apidetect.api_identifier("https://example.org", "testsw")

    assert len(found) == 1
    assert found[0]["type"] == "probe"
    assert found[0]["url"] == "https://example.org/probe"


def test_api_identifier_rejects_wrong_mime_for_string_expected_mime(monkeypatch):
    monkeypatch.setitem(
        apidetect.CATALOGS_URLMAP,
        "testsw",
        [
            {
                "id": "probe",
                "url": "/probe",
                "expected_mime": "text/turtle",
                "version": None,
            }
        ],
    )
    _patch_session(
        monkeypatch,
        [_DummyResponse(headers={"Content-Type": "application/json"})],
    )

    found = apidetect.api_identifier("https://example.org", "testsw")

    assert found == []


def test_geoserver_root_url_strips_workspace_and_web():
    assert (
        apidetect.geoserver_root_url("https://maps.example.org/geoserver/web/")
        == "https://maps.example.org/geoserver"
    )
    assert (
        apidetect.geoserver_root_url("https://geo.example.org/geoserver/geo")
        == "https://geo.example.org/geoserver"
    )


def test_copernicusdhus_url_cleanup_strips_fragment_and_keeps_dhus():
    assert (
        apidetect.copernicusdhus_url_cleanup_func(
            "https://sentinels.example.int/dhus/#/home"
        )
        == "https://sentinels.example.int/dhus"
    )
    assert (
        apidetect.copernicusdhus_url_cleanup_func("https://finhub.example.int/#/home")
        == "https://finhub.example.int"
    )


def test_api_identifier_geoserver_fast_path_ows(monkeypatch):
    class _GeoSession:
        def get(self, url, **kwargs):
            if url.startswith("https://maps.example.org/geoserver/ows") and "WMS" in url and "1.3.0" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            if "/ogc/" in url or "/rest/" in url or "/gwc/" in url:
                raise AssertionError(f"fast path must not probe {url}")
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GeoSession())

    found = apidetect.api_identifier(
        "https://maps.example.org/geoserver/web/", "geoserver"
    )

    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"]
        == "https://maps.example.org/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
        for item in found
    )


def test_api_identifier_geoserver_stac_uses_display_url_for_endpoint(monkeypatch):
    """STAC probe hits collections JSON; stored URL is the API root (see GEOSERVER_URLMAP)."""
    monkeypatch.setitem(
        apidetect.CATALOGS_URLMAP,
        "testsw",
        [
            {
                "id": "stacserverapi",
                "display_url": "/ogc/stac/v1",
                "url": "/ogc/stac/v1/collections?f=json",
                "accept": "application/json",
                "expected_mime": apidetect.JSON_MIMETYPES,
                "is_json": True,
                "version": None,
            }
        ],
    )
    _patch_session(
        monkeypatch,
        [_DummyResponse(content=b'{"collections":[],"links":[]}')],
    )

    found = apidetect.api_identifier("https://example.org/geoserver", "testsw")

    assert len(found) == 1
    assert found[0]["type"] == "stacserverapi"
    assert found[0]["url"] == "https://example.org/geoserver/ogc/stac/v1"


def test_analyze_robots_returns_empty_for_non_200(monkeypatch):
    _patch_requests_get(
        monkeypatch,
        _DummyResponse(
            status_code=404,
            content=b"Not found",
            headers={"Content-Type": "text/plain"},
        ),
    )

    found = apidetect.analyze_robots("https://example.org")

    assert found == []


def test_analyze_root_continues_after_empty_jsonld_list(monkeypatch):
    html = """
    <html>
      <head>
        <script type="application/ld+json">[]</script>
        <script type="application/ld+json">{"@graph":[{"@type":"DataCatalog"}]}</script>
      </head>
      <body></body>
    </html>
    """
    _patch_session(
        monkeypatch,
        [
            _DummyResponse(
                status_code=200,
                content=html.encode("utf8"),
                headers={"Content-Type": "text/html"},
            )
        ],
    )

    found = apidetect.analyze_root("https://example.org")

    assert {"type": "schemaorg:datacatalog", "url": "https://example.org"} in found


def test_analyze_root_detects_datacatalog_in_mainentity_list(monkeypatch):
    html = """
    <html>
      <head>
        <script type="application/ld+json">
          {"@graph":[{"@type":"WebPage","mainEntity":[{"name":"no-type"},{"@type":"DataCatalog"}]}]}
        </script>
      </head>
      <body></body>
    </html>
    """
    _patch_session(
        monkeypatch,
        [
            _DummyResponse(
                status_code=200,
                content=html.encode("utf8"),
                headers={"Content-Type": "text/html"},
            )
        ],
    )

    found = apidetect.analyze_root("https://example.org")

    assert {"type": "schemaorg:datacatalog", "url": "https://example.org"} in found


def test_detect_ckan_uses_ckanapi_endpoint_base_url(monkeypatch):
    test_record = {
        "id": "testckan",
        "link": "https://catalog.example.org",
        "software": {"id": "ckan"},
        "endpoints": [{"type": "ckanapi", "url": "https://catalog.example.org/api/3"}],
    }
    calls = []

    monkeypatch.setattr(apidetect, "_resolve_root_dir", lambda mode: "/unused")
    monkeypatch.setattr(apidetect, "_iter_yaml_files", lambda root: ["fake.yaml"])
    monkeypatch.setattr(apidetect, "_load_record", lambda filepath: test_record)

    def _fake_api_identifier(base_url, software_id, **kwargs):
        calls.append((base_url, software_id))
        return []

    monkeypatch.setattr(apidetect, "api_identifier", _fake_api_identifier)

    apidetect.detect_ckan(dryrun=True, mode="entries")

    assert calls == [("https://catalog.example.org", "ckan")]


def test_catalogs_urlmap_includes_draft_software():
  expected = {
      "stacserver",
      "galaxy",
      "udata",
      "lizmap",
      "nextgisweb",
      "fusionregistry",
      "aristotlemdr",
      "geomapfish",
      "getsdiportal",
      "redatam",
      "scicat",
      "mapstore",
      "opensdg",
      "terria",
      "seek",
      "supermapiserver",
      "mapgisigserver",
      "gvsigonline",
      "ingrid",
      "erdasapollo",
      "drupal",
  }
  assert expected.issubset(apidetect.CATALOGS_URLMAP.keys())


def test_opendap_urlmap_is_not_empty():
  assert len(apidetect.OPENDAP_URLMAP) > 0


def test_api_identifier_stacserver_collections(monkeypatch):
  collections = b'{"collections":[],"links":[]}'

  class _StacSession:
      def get(self, url, **kwargs):
          if url.endswith("/collections"):
              return _DummyResponse(content=collections)
          return _DummyResponse(status_code=404)

      def post(self, *args, **kwargs):
          return _DummyResponse(status_code=404)

  monkeypatch.setattr(apidetect.requests, "Session", lambda: _StacSession())

  found = apidetect.api_identifier("https://example.org/stac/v1", "stacserver")

  assert any(item["type"] == "stacserverapi:collections" for item in found)
  assert any(
      item["url"] == "https://example.org/stac/v1/collections" for item in found
  )


def test_api_identifier_galaxy_version(monkeypatch):
  class _GalaxySession:
      def get(self, url, **kwargs):
          if url.endswith("/api/version"):
              return _DummyResponse(
                  content=b'{"version_major":"24.1","version_minor":"0"}',
              )
          return _DummyResponse(status_code=404)

      def post(self, *args, **kwargs):
          return _DummyResponse(status_code=404)

  monkeypatch.setattr(apidetect.requests, "Session", lambda: _GalaxySession())

  found = apidetect.api_identifier("https://usegalaxy.org", "galaxy")

  assert any(item["type"] == "galaxy:api" for item in found)
  assert any(item["url"] == "https://usegalaxy.org/api/version" for item in found)


def test_api_identifier_udata_datasets(monkeypatch):
  class _UdataSession:
      def get(self, url, **kwargs):
          if url.endswith("/api/1/datasets/"):
              return _DummyResponse(
                  content=b'{"data":[],"page":1,"page_size":20,"total":0}',
              )
          return _DummyResponse(status_code=404)

      def post(self, *args, **kwargs):
          return _DummyResponse(status_code=404)

  monkeypatch.setattr(apidetect.requests, "Session", lambda: _UdataSession())

  found = apidetect.api_identifier("https://www.data.gouv.fr", "udata")

  assert any(item["type"] == "udataapi" for item in found)
  assert any(
      item["url"] == "https://www.data.gouv.fr/api/1/datasets/" for item in found
  )


def test_report_writes_expected_header(tmp_path, monkeypatch):
    test_record = {
        "id": "id1",
        "uid": "cdi00000001",
        "link": "https://catalog.example.org",
        "software": {"id": "ckan"},
    }

    monkeypatch.setitem(apidetect.CATALOGS_URLMAP, "ckan", [{}])
    monkeypatch.setattr(apidetect, "_resolve_root_dir", lambda mode: "/unused")
    monkeypatch.setattr(apidetect, "_iter_yaml_files", lambda root: ["fake.yaml"])
    monkeypatch.setattr(apidetect, "_load_record", lambda filepath: test_record)

    out_file = tmp_path / "report.csv"
    apidetect.report(status="undetected", filename=str(out_file), mode="entries")

    lines = out_file.read_text(encoding="utf8").splitlines()
    assert lines[0] == "id,uid,link,software_id,status"


def test_api_identifier_geomapfish_themes(monkeypatch):
    class _GmfSession:
        def get(self, url, **kwargs):
            if url.endswith("/themes"):
                return _DummyResponse(content=b'{"themes":[]}')
            if "mapserv_proxy" in url and "WMS" in url and "1.3.0" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GmfSession())

    found = apidetect.api_identifier("https://map.example.ch/", "geomapfish")

    assert any(item["type"] == "geomapfish:themes" for item in found)
    assert any(
        item["url"] == "https://map.example.ch/themes" for item in found
    )
    assert any(item["type"] == "wms130" for item in found)


def test_api_identifier_getsdiportal_geoserver_ows(monkeypatch):
    class _GetSdiSession:
        def get(self, url, **kwargs):
            if "/geoserver/ows" in url and "WMS" in url and "1.3.0" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GetSdiSession())

    found = apidetect.api_identifier("https://gis.example.gr/", "getsdiportal")

    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"]
        == "https://gis.example.gr/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
        for item in found
    )


def test_api_identifier_redatam_uses_engine_link(monkeypatch):
    engine = "https://prod.redatam.org/binpry/RpWebEngine.exe/Portal?BASE=CPV2022"

    class _RedatamSession:
        def get(self, url, **kwargs):
            if url == engine:
                return _DummyResponse(
                    content=b"<html>REDATAM</html>",
                    headers={"Content-Type": "text/html"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _RedatamSession())

    found = apidetect.api_identifier(engine, "redatam")

    assert any(item["type"] == "redatam" and item["url"] == engine for item in found)


def test_api_identifier_scicat_datasets(monkeypatch):
    class _SciCatSession:
        def get(self, url, **kwargs):
            if url.endswith("/api/v3/datasets"):
                return _DummyResponse(content=b"[]")
            return _DummyResponse(status_code=404)

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _SciCatSession())

    found = apidetect.api_identifier("https://scicat.example.org/", "scicat")

    assert any(item["type"] == "scicat:datasets" for item in found)
    assert any(
        item["url"] == "https://scicat.example.org/api/v3/datasets" for item in found
    )


def test_api_identifier_scicat_skips_doi_host(monkeypatch):
    class _FailSession:
        def get(self, *args, **kwargs):
            raise AssertionError("DOI landing hosts must not be probed")

        def post(self, *args, **kwargs):
            raise AssertionError("DOI landing hosts must not be probed")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _FailSession())

    found = apidetect.api_identifier("https://doi.ess.eu/", "scicat")

    assert found == []


def test_api_identifier_mapstore_uses_origin_geoserver(monkeypatch):
    class _MapStoreSession:
        def get(self, url, **kwargs):
            if url.startswith("https://webgis.example.it/geoserver/ows") and "WMS" in url and "1.3.0" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _MapStoreSession())

    found = apidetect.api_identifier(
        "https://webgis.example.it/mapstore", "mapstore"
    )

    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"]
        == "https://webgis.example.it/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
        for item in found
    )


def test_api_identifier_opensdg_indicator_json(monkeypatch):
    class _OpenSdgSession:
        def get(self, url, **kwargs):
            if url.endswith("/en/data/1-1-1.json"):
                return _DummyResponse(content=b'{"data":[]}')
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OpenSdgSession())

    found = apidetect.api_identifier("https://sdg.example.gov/", "opensdg")

    assert any(item["type"] == "opensdg:data" for item in found)
    assert any(
        item["url"] == "https://sdg.example.gov/en/data/1-1-1.json" for item in found
    )


def test_opensdg_parse_remote_data_base_url():
    html = """
    var opensdg = {
      remoteDataBaseUrl: 'https://bristolsdgs.github.io/sdg-data-bristol/en',
      language: 'en',
    };
    """
    assert (
        apidetect.opensdg_parse_remote_data_base_url(
            html, "https://bristolsdgs.github.io/"
        )
        == "https://bristolsdgs.github.io/sdg-data-bristol/en"
    )
    assert (
        apidetect.opensdg_parse_remote_data_base_url(
            "var opensdg = { remoteDataBaseUrl: '/', };",
            "https://example.org/",
        )
        is None
    )


def test_api_identifier_opensdg_uses_remote_data_base_url(monkeypatch):
    html = b"""
    <script>
    var opensdg = {
      remoteDataBaseUrl: 'https://example.org/sdg-data/en',
    };
    </script>
    """

    class _OpenSdgRemoteSession:
        def get(self, url, **kwargs):
            if url.rstrip("/") == "https://sdg.example.org":
                return _DummyResponse(
                    content=html,
                    headers={"Content-Type": "text/html"},
                )
            if url == "https://example.org/sdg-data/en/data/1-1-1.json":
                return _DummyResponse(content=b'{"data":[]}')
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OpenSdgRemoteSession())

    found = apidetect.api_identifier("https://sdg.example.org/", "opensdg")

    assert any(
        item["url"] == "https://example.org/sdg-data/en/data/1-1-1.json"
        for item in found
    )


def test_api_identifier_terria_config(monkeypatch):
    class _TerriaSession:
        def get(self, url, **kwargs):
            if url.endswith("/config.json"):
                return _DummyResponse(content=b'{"catalog":[]}')
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _TerriaSession())

    found = apidetect.api_identifier("https://maps.example.org/", "terria")

    assert any(item["type"] == "terria:config" for item in found)
    assert any(
        item["url"] == "https://maps.example.org/config.json" for item in found
    )


def test_nextgisweb_url_cleanup_strips_resource_path():
    cleaned = apidetect.nextgisweb_url_cleanup_func(
        "https://ngw.example.ru/resource/0"
    )
    assert cleaned == "https://ngw.example.ru"


def test_api_identifier_giswebse_uses_origin_service(monkeypatch):
    class _GiswebSession:
        def get(self, url, **kwargs):
            if url.startswith("https://maps.example.ru/GISWebServiceSE/service.php") and "WMS" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GiswebSession())

    found = apidetect.api_identifier(
        "https://maps.example.ru/GISWebServerSE/", "giswebse"
    )

    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"].startswith("https://maps.example.ru/GISWebServiceSE/service.php")
        for item in found
    )


def test_api_identifier_oskari_tries_oskari_prefix(monkeypatch):
    class _OskariSession:
        def get(self, url, **kwargs):
            if "GetHierarchicalMapLayerGroups" in url and "/oskari/" in url:
                return _DummyResponse(content=b'{"layers":[]}')
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OskariSession())

    found = apidetect.api_identifier("https://kortagluggi.is", "oskari")

    assert any(item["type"] == "oskari:gethiermaplayers" for item in found)
    assert any(
        item["url"]
        == "https://kortagluggi.is/oskari/action?action_route=GetHierarchicalMapLayerGroups"
        for item in found
    )


def test_api_identifier_supermap_services_json(monkeypatch):
    class _SuperMapSession:
        def get(self, url, **kwargs):
            if url.endswith("/iserver/services.json"):
                return _DummyResponse(content=b'[{"name":"map-world"}]')
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _SuperMapSession())

    found = apidetect.api_identifier(
        "https://gis.example.gov/iserver/", "supermapiserver"
    )

    assert any(item["type"] == "supermap:services" for item in found)
    assert any(
        item["url"] == "https://gis.example.gov/iserver/services.json" for item in found
    )


def test_mapgisigserver_url_cleanup_keeps_igs_root():
    cleaned = apidetect.mapgisigserver_url_cleanup_func(
        "https://gis.example.gov:6163/igs/rest/mrcs/docs"
    )
    assert cleaned == "https://gis.example.gov:6163/igs"


def test_api_identifier_mapgis_docs_json(monkeypatch):
    class _MapGisSession:
        def get(self, url, **kwargs):
            if url.endswith("/igs/rest/mrcs/docs?f=json") or url.endswith(
                "/rest/mrcs/docs?f=json"
            ):
                return _DummyResponse(content=b'["WorldMap","CityMap"]')
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _MapGisSession())

    found = apidetect.api_identifier(
        "https://gis.example.gov:6163/igs/", "mapgisigserver"
    )

    assert any(item["type"] == "mapgis:docs" for item in found)
    assert any(
        item["url"] == "https://gis.example.gov:6163/igs/rest/mrcs/docs?f=json"
        for item in found
    )


def test_api_identifier_gvsigonline_uses_origin_geoserver(monkeypatch):
    class _GvSigSession:
        def get(self, url, **kwargs):
            if url.startswith("https://geoportal.example.es/geoserver/ows") and "WMS" in url and "1.3.0" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GvSigSession())

    found = apidetect.api_identifier(
        "https://geoportal.example.es/gvsigonline/", "gvsigonline"
    )

    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"]
        == "https://geoportal.example.es/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
        for item in found
    )


def test_api_identifier_ingrid_csw(monkeypatch):
    class _IngridSession:
        def get(self, url, **kwargs):
            if "/csw?" in url and "CSW" in url:
                return _DummyResponse(
                    content=b"<Capabilities/>",
                    headers={"Content-Type": "application/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _IngridSession())

    found = apidetect.api_identifier("https://metaver.example.de/", "ingrid")

    assert any(item["type"] == "csw202" for item in found)
    assert any(
        item["url"]
        == "https://metaver.example.de/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities"
        for item in found
    )


def test_api_identifier_erdasapollo_wms(monkeypatch):
    class _ErdasSession:
        def get(self, url, **kwargs):
            if "/erdas-iws/ogc/wms/" in url and "1.3.0" in url:
                return _DummyResponse(
                    content=b"<WMS_Capabilities/>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _ErdasSession())

    found = apidetect.api_identifier(
        "https://maps.example.gov/erdas-apollo", "erdasapollo"
    )

    assert any(item["type"] == "wms130" for item in found)
    assert any("/erdas-iws/ogc/wms/" in item["url"] for item in found)


def test_save_record_preserves_key_order(tmp_path):
    path = tmp_path / "catalog.yaml"
    record = {
        "access_mode": ["open"],
        "id": "example",
        "link": "https://example.org",
        "name": "Example",
    }
    apidetect._save_record(str(path), record)
    text = path.read_text(encoding="utf8")
    assert text.index("access_mode") < text.index("id")
    assert text.index("id") < text.index("name")


def test_infer_endpoints_verified_skips_unknown_software():
    found = apidetect.infer_endpoints_verified(
        {"software": {"id": "wagmap"}, "link": "https://example.org"}
    )
    assert found == []


def test_infer_endpoints_verified_skips_empty_link():
    found = apidetect.infer_endpoints_verified(
        {"software": {"id": "ckan"}, "link": ""}
    )
    assert found == []


def test_infer_endpoints_verified_uses_urlmap(monkeypatch):
    monkeypatch.setattr(
        apidetect,
        "api_identifier",
        lambda *args, **kwargs: [
            {"type": "ckan", "url": "https://example.org/api/3"}
        ],
    )
    found = apidetect.infer_endpoints_verified(
        {"software": {"id": "ckan"}, "link": "https://example.org"}
    )
    assert found == [{"type": "ckan", "url": "https://example.org/api/3"}]


def test_icat_urlmap_is_registered():
    assert "icat" in apidetect.CATALOGS_URLMAP
    urls = [item["url"] for item in apidetect.CATALOGS_URLMAP["icat"]]
    assert "/oaipmh/request?verb=Identify" in urls


def test_quality_fixer_infer_endpoints_delegates():
    from endpoints_infer import infer_endpoints

    found = infer_endpoints(
        {"software": {"id": "wagmap"}, "link": "https://example.org"}
    )
    assert found == []


def test_infer_endpoints_verified_skips_custom():
    found = apidetect.infer_endpoints_verified(
        {"software": {"id": "custom"}, "link": "https://example.org/data"}
    )
    assert found == []


def test_api_identifier_cogis_elitegis_rest(monkeypatch):
    class _CogisSession:
        def get(self, url, **kwargs):
            if url.endswith("/elitegis/rest/services?f=pjson"):
                return _DummyResponse(
                    content=b'{"currentVersion":10.8}',
                    headers={"Content-Type": "text/plain"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _CogisSession())

    found = apidetect.api_identifier(
        "https://citycloud.example.com/portal/catalog", "cogis"
    )

    assert any(item["type"] == "arcgis:rest:services" for item in found)
    assert any(
        item["url"]
        == "https://citycloud.example.com/elitegis/rest/services?f=pjson"
        for item in found
    )


def test_api_identifier_gin_skips_doi_host(monkeypatch):
    def _fail(*args, **kwargs):
        raise AssertionError("DOI GIN hosts should not be probed")

    monkeypatch.setattr(
        apidetect.requests,
        "Session",
        lambda: type("S", (), {"get": staticmethod(_fail), "post": staticmethod(_fail)})(),
    )

    found = apidetect.api_identifier("https://doi.gin.example.org/", "gin")
    assert found == []


def test_api_identifier_gin_version(monkeypatch):
    class _GinSession:
        def get(self, url, **kwargs):
            if url.endswith("/api/v1/version"):
                return _DummyResponse(
                    content=b'{"version":"1.22.0"}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GinSession())

    found = apidetect.api_identifier("https://gin.g-node.org/", "gin")

    assert any(item["type"] == "gogs:api" for item in found)
    assert any(item["url"] == "https://gin.g-node.org/api/v1/version" for item in found)


def test_api_identifier_osf_uses_jsonapi_host(monkeypatch):
    class _OsfSession:
        def get(self, url, **kwargs):
            if url == "https://api.osf.io/v2/":
                return _DummyResponse(
                    content=b'{"data":[]}',
                    headers={"Content-Type": "application/vnd.api+json"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OsfSession())

    found = apidetect.api_identifier("https://osf.io", "osf")

    assert any(item["type"] == "osf:api" for item in found)
    assert any(item["url"] == "https://api.osf.io/v2/" for item in found)


def test_api_identifier_samvera_catalog_json(monkeypatch):
    class _SamveraSession:
        def get(self, url, **kwargs):
            if url.endswith("/catalog.json"):
                return _DummyResponse(
                    content=b'{"response":{"docs":[]}}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _SamveraSession())

    found = apidetect.api_identifier("https://curate.example.edu", "samvera")

    assert any(item["type"] == "hyrax:catalog" for item in found)
    assert any(
        item["url"] == "https://curate.example.edu/catalog.json" for item in found
    )


def test_api_identifier_samvera_catalog_oai(monkeypatch):
    class _SamveraOaiSession:
        def get(self, url, **kwargs):
            if "catalog/oai?verb=Identify" in url:
                return _DummyResponse(
                    content=b"<OAI-PMH><Identify/></OAI-PMH>",
                    headers={"Content-Type": "application/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _SamveraOaiSession())

    found = apidetect.api_identifier("https://curate.example.edu", "samvera")

    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://curate.example.edu/catalog/oai?verb=Identify"
        for item in found
    )


def test_api_identifier_ensembl_rest_ping(monkeypatch):
    class _EnsemblSession:
        def get(self, url, **kwargs):
            if url.endswith("/rest/info/ping"):
                return _DummyResponse(
                    content=b'{"ping":1}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _EnsemblSession())

    found = apidetect.api_identifier("https://parasite.example.org/", "ensembl")

    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://parasite.example.org/rest/info/ping" for item in found
    )


def test_api_identifier_phaidra_search_select(monkeypatch):
    class _PhaidraSession:
        def get(self, url, **kwargs):
            if url.endswith("/api/search/select"):
                return _DummyResponse(
                    content=b"<response/>",
                    headers={"Content-Type": "application/xml"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _PhaidraSession())

    found = apidetect.api_identifier("https://phaidra.example.ac.at", "phaidra")

    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://phaidra.example.ac.at/api/search/select" for item in found
    )


def test_api_identifier_maptilerserver_api_index(monkeypatch):
    class _MapTilerSession:
        def get(self, url, **kwargs):
            if url.endswith("/api"):
                return _DummyResponse(
                    content=b'{"openapi":"3.0.0"}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(status_code=404, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _MapTilerSession())

    found = apidetect.api_identifier("https://tile.example.gov", "maptilerserver")

    assert any(item["type"] == "openapi" for item in found)
    assert any(item["url"] == "https://tile.example.gov/api" for item in found)


def test_api_identifier_nyudatacatalog_jsonld(monkeypatch):
    html = (
        b"<html><head><script type=\"application/ld+json\">"
        b'{"@type":"DataCatalog","name":"Example"}'
        b"</script></head><body></body></html>"
    )

    class _NyuSession:
        def get(self, url, **kwargs):
            return _DummyResponse(content=html, headers={"Content-Type": "text/html"})

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404)

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _NyuSession())

    found = apidetect.api_identifier(
        "https://datacatalog.example.edu", "nyudatacatalog"
    )

    assert any(item["type"] == "schemaorg:datacatalog" for item in found)
    assert any(
        item["url"] == "https://datacatalog.example.edu" for item in found
    )


def test_no_standard_probe_skip_list_is_not_in_urlmap():
    from apidetect_urlmaps_draft import NO_STANDARD_PROBE

    overlap = sorted(set(NO_STANDARD_PROBE) & set(apidetect.CATALOGS_URLMAP))
    assert overlap == [], overlap


def test_every_named_software_id_is_mapped_or_skipped():
    from apidetect_urlmaps_draft import NO_STANDARD_PROBE
    from docs_software_coverage import load_software_ids

    known = set(load_software_ids())
    mapped = set(apidetect.CATALOGS_URLMAP) - {"custom"}
    leftover = sorted(known - mapped - set(NO_STANDARD_PROBE))
    assert leftover == [], leftover


def test_tianditu_urlmap_is_registered():
    assert "tianditu" in apidetect.CATALOGS_URLMAP
    urls = [item["url"] for item in apidetect.CATALOGS_URLMAP["tianditu"]]
    assert "/iserver/services.json" in urls
    assert "/iportal/web/services.json" in urls
    assert "/arcgis/rest/services?f=pjson" in urls
    assert "/api/cityNode/queryByTree.json" in urls


def test_tianditu_url_cleanup_strips_html():
    assert (
        apidetect.tianditu_url_cleanup_func(
            "https://hunan.example.gov.cn/TDTHN/portal/homePage.html"
        )
        == "https://hunan.example.gov.cn/TDTHN/portal"
    )


def test_api_identifier_tianditu_uses_origin(monkeypatch):
    class _TdtSession:
        def get(self, url, **kwargs):
            if url == "https://henan.example.gov.cn/iserver/services.json":
                return _DummyResponse(
                    content=b'[{"componentType":"com.supermap.services.components.impl.MapImpl"}]',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _TdtSession())

    found = apidetect.api_identifier(
        "https://henan.example.gov.cn/jiaozuo/", "tianditu"
    )

    assert any(item["type"] == "supermap:services" for item in found)
    assert any(
        item["url"] == "https://henan.example.gov.cn/iserver/services.json"
        for item in found
    )


def test_recommended_urlmaps_are_registered():
    expected = {
        "resourcecontracts": ["/contract/resources"],
        "piveau": [
            "/api/hub/search",
            "/api/hub/search/search",
            "/api/hub/repo/datasets",
            "/api/hub/search/ckan/package_search",
        ],
        "fairdatapoint": ["/", "/v3/api-docs", "/swagger-ui.html"],
        "omekas": [
            "/api",
            "/api/items",
            "/api/items?resource_class_label=Dataset",
            "/api-context",
        ],
        "contentdm": ["/digital/api/collections", "/oai/oai.php?verb=Identify"],
        "symbiota": [
            "/collections/datasets/rsshandler.php",
            "/api/v2/documentation",
        ],
        "idra": ["/Idra/api/v1/administration/version", "/Idra/api/v1/catalogues"],
        "hajk": ["/appConfig.json", "/publik/appConfig.json"],
        "clld": ["/parameters.json", "/download"],
        "minerva": ["/api/projects/", "/minerva/api/projects/"],
        "tergis": ["/api/v1/classifiers/layers", "/themes.json"],
        "geonature": ["/api/searchTaxon", "/api/searchCommune"],
        "g3wsuite": ["/api/", "/api/group/", "/group/api/"],
        "geocortex": [
            "/Geocortex/Essentials/REST/sites?f=pjson",
        ],
        "activemapgis": ["/groups/withLayers"],
        "aubrey": ["/oai/?verb=Identify", "/api/"],
        "datahubproject": ["/api/graphql"],
        "gringlobal": ["/gringlobal/api/v1", "/gringlobal/search"],
        "yoda": ["/oai/oai?verb=Identify"],
        "dataone": ["/metacat/d1/mn/v2", "/metacat/sitemaps/sitemap_index.xml"],
        "opendatacube": ["/stac", "/stac/collections"],
        "opengov": ["/transparency", "/data/"],
        "origo": ["/index.json", "/index_ssl.json"],
        "atmmaggioli": ["/transparencia/datos/catalogo"],
        "odweb": ["/odweb/"],
        "duva": ["/Informationsportal/"],
        "beyond2020": ["/ReportFolders/reportFolders.aspx"],
        "tr32db": ["/site/index.php"],
        "codalab": ["/competitions/"],
        "dataverse": ["/api/info/version", "/api/search?q=*&type=dataset&sort=name&order=asc"],
        "pxweb": ["/api/v1/", "/api/v1/en/", "/api/v1/sv/", "/api/v1/fi/", "/api/v1/da/"],
        "vufind": [
            '/Search/Results?type=AllFields&filter[]=format%3A"Dataset"',
            "/api?openapi",
        ],
        "librecat": [
            '/Search/Results?type=AllFields&filter[]=format%3A"Dataset"',
            "/oai?verb=Identify",
        ],
        "islandora": [
            "/solr/select?q=RELS_EXT_hasModel_uri_ms:*Dataset*&wt=json&rows=25",
        ],
        "archipelago": [
            "/search?f[0]=descriptive_metadata_object_types:Dataset",
        ],
        "figshare": ["/articles/dataset/"],
        "divaportal": ["/smash/search.jsf"],
        "pure": [
            "/de/datasets/?search=&isCopyPasteSearch=false&format=rss",
            "/da/datasets/?search=&isCopyPasteSearch=false&format=rss",
        ],
        "drupal": [
            "/jsonapi/node/dataset",
            "/jsonapi/node/open_data",
            "/jsonapi/node/ckan_dataset",
        ],
    }
    for sid, urls in expected.items():
        assert sid in apidetect.CATALOGS_URLMAP
        mapped = [item["url"] for item in apidetect.CATALOGS_URLMAP[sid]]
        for url in urls:
            assert url in mapped


def test_api_identifier_contentdm_uses_origin(monkeypatch):
    class _CdmSession:
        def get(self, url, **kwargs):
            if url == "https://statsnz.contentdm.oclc.org/digital/api/collections":
                return _DummyResponse(
                    content=b'{"collections":[]}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _CdmSession())

    found = apidetect.api_identifier(
        "https://statsnz.contentdm.oclc.org/digital/collection/p20045coll35",
        "contentdm",
    )

    assert any(item["type"] == "customapi" for item in found)
    assert any(
        item["url"] == "https://statsnz.contentdm.oclc.org/digital/api/collections"
        for item in found
    )


def test_api_identifier_resourcecontracts_json(monkeypatch):
    class _RcSession:
        def get(self, url, **kwargs):
            if url.endswith("/contract/resources"):
                return _DummyResponse(
                    content=b'[{"resource":"Hydrocarbons","contract":1}]',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _RcSession())

    found = apidetect.api_identifier(
        "https://guinea.resourcecontracts.org", "resourcecontracts"
    )

    assert any(item["type"] == "custom_api" for item in found)
    assert any(
        item["url"] == "https://guinea.resourcecontracts.org/contract/resources"
        for item in found
    )


def test_new_urlmaps_are_not_on_skip_list():
    from apidetect_urlmaps_draft import NO_STANDARD_PROBE

    for sid in (
        "hajk",
        "clld",
        "minerva",
        "tergis",
        "aubrey",
        "geonature",
        "g3wsuite",
        "geocortex",
        "activemapgis",
        "datahubproject",
        "gringlobal",
        "synapse",
        "yoda",
        "dataone",
        "opendatacube",
        "opengov",
        "origo",
        "atmmaggioli",
        "odweb",
        "duva",
        "beyond2020",
        "tr32db",
        "codalab",
        "librecat",
    ):
        assert sid in apidetect.CATALOGS_URLMAP
        assert sid not in NO_STANDARD_PROBE


def test_geocortex_url_cleanup_strips_sites_path():
    assert (
        apidetect.geocortex_url_cleanup_func(
            "https://maps.orcity.org/Geocortex/Essentials/REST/sites"
        )
        == "https://maps.orcity.org"
    )
    assert (
        apidetect.geocortex_url_cleanup_func(
            "https://gis.example.gov/geocortex/essentials/rest/sites?f=pjson"
        )
        == "https://gis.example.gov"
    )


def test_g3wsuite_url_cleanup_strips_map_project():
    assert (
        apidetect.g3wsuite_url_cleanup_func(
            "https://geout.comune.palermo.it/map/group/project/"
        )
        == "https://geout.comune.palermo.it"
    )


def test_api_identifier_hajk_appconfig(monkeypatch):
    class _HajkSession:
        def get(self, url, **kwargs):
            if url == "https://karta.laxa.se/appConfig.json":
                return _DummyResponse(
                    content=b'{"mapserviceBase":"/mapservice"}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _HajkSession())

    found = apidetect.api_identifier("https://karta.laxa.se", "hajk")

    assert any(item["type"] == "api" for item in found)
    assert any(item["url"] == "https://karta.laxa.se/appConfig.json" for item in found)


def test_api_identifier_geocortex_sites_from_rest_link(monkeypatch):
    class _GcxSession:
        def get(self, url, **kwargs):
            if url == (
                "https://maps.orcity.org/Geocortex/Essentials/REST/sites?f=pjson"
            ):
                return _DummyResponse(
                    content=b'{"sites":[]}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GcxSession())

    found = apidetect.api_identifier(
        "https://maps.orcity.org/Geocortex/Essentials/REST/sites",
        "geocortex",
    )

    assert any(item["type"] == "geocortex:catalog" for item in found)
    assert any(
        item["url"]
        == "https://maps.orcity.org/Geocortex/Essentials/REST/sites?f=pjson"
        for item in found
    )


def test_api_identifier_geocortex_accepts_text_plain_pjson(monkeypatch):
    class _GcxPlain:
        def get(self, url, **kwargs):
            if "sites?f=pjson" in url:
                return _DummyResponse(
                    content=b'{"sites":[{"id":"TrafficCounts2011"}]}',
                    headers={"Content-Type": "text/plain; charset=utf-8"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GcxPlain())

    found = apidetect.api_identifier("https://maps.orcity.org", "geocortex")

    assert any(item["type"] == "geocortex:catalog" for item in found)
    geocortex_urls = [item["url"] for item in apidetect.CATALOGS_URLMAP["geocortex"]]
    assert "/geocortex/essentials/rest/sites?f=pjson" not in geocortex_urls


def test_api_identifier_geonature_probes_atlas_prefix(monkeypatch):
    class _GnSession:
        def get(self, url, **kwargs):
            if url == "https://atlas.example.fr/atlas/api/searchTaxon":
                return _DummyResponse(
                    content=b'[{"cd_nom":1}]',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _GnSession())

    found = apidetect.api_identifier("https://atlas.example.fr/", "geonature")

    assert any(item["type"] == "geonature:api" for item in found)
    assert any(
        item["url"] == "https://atlas.example.fr/atlas/api/searchTaxon"
        for item in found
    )


def test_origo_url_cleanup_strips_index_html():
    assert (
        apidetect.origo_url_cleanup_func(
            "https://karta.timra.se/bxkarta/index.html"
        )
        == "https://karta.timra.se/bxkarta"
    )
    assert (
        apidetect.origo_url_cleanup_func("https://karta.sodertalje.se/")
        == "https://karta.sodertalje.se"
    )


def test_api_identifier_origo_index_json(monkeypatch):
    class _OrigoSession:
        def get(self, url, **kwargs):
            if url == "https://karta.timra.se/bxkarta/index.json":
                return _DummyResponse(
                    content=b'{"controls":[],"layers":[]}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OrigoSession())

    found = apidetect.api_identifier(
        "https://karta.timra.se/bxkarta/index.html", "origo"
    )

    assert any(item["type"] == "origo:config" for item in found)
    assert any(
        item["url"] == "https://karta.timra.se/bxkarta/index.json"
        for item in found
    )


def test_origo_parse_config_urls_from_html():
    html = "<script>Origo('vas.json');</script>"
    assert apidetect.origo_parse_config_urls(
        html, "https://kartor.vasteras.se/sam/"
    ) == ["https://kartor.vasteras.se/sam/vas.json"]
    assert apidetect.origo_parse_config_urls(
        "<script>Origo('./origo/index_ssl.json');</script>",
        "https://gi.karlstad.se/",
    ) == ["https://gi.karlstad.se/origo/index_ssl.json"]


def test_origo_parse_gallery_config_urls_from_html():
    html = """
    <a href="css/bootstrap.min.css">css</a>
    <a href="sundsvall/">Sundsvall</a>
    <a href="bxkarta/">Bx</a>
    <a href="https://karta.sundsvall.se/solkarta/index.html">sol</a>
    <a href="https://www.sundsvallvaxer.se/karta">other host</a>
    <a href="mailto:geodata@sundsvall.se">mail</a>
    """
    urls = apidetect.origo_parse_gallery_config_urls(
        html, "https://karta.sundsvall.se/"
    )
    assert "https://karta.sundsvall.se/sundsvall/index.json" in urls
    assert "https://karta.sundsvall.se/bxkarta/index.json" in urls
    assert "https://karta.sundsvall.se/solkarta/index.json" in urls
    assert not any("bootstrap" in url for url in urls)
    assert not any("sundsvallvaxer" in url for url in urls)


def test_swing_url_cleanup_strips_dashboard():
    assert (
        apidetect.swing_url_cleanup_func(
            "https://arbeidsmarktmobiliteit.databank.nl/Dashboard/dashboard/"
        )
        == "https://arbeidsmarktmobiliteit.databank.nl"
    )
    assert (
        apidetect.swing_url_cleanup_func("https://wetteren.incijfers.be/")
        == "https://wetteren.incijfers.be"
    )


def test_api_identifier_origo_reads_named_config_from_html(monkeypatch):
    class _OrigoNamed:
        def get(self, url, **kwargs):
            if url.rstrip("/") == "https://kartor.vasteras.se/sam":
                return _DummyResponse(
                    content=b"<script>Origo('vas.json');</script>",
                    headers={"Content-Type": "text/html"},
                    text="<script>Origo('vas.json');</script>",
                )
            if url == "https://kartor.vasteras.se/sam/vas.json":
                return _DummyResponse(
                    content=b'{"controls":[]}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OrigoNamed())

    found = apidetect.api_identifier(
        "https://kartor.vasteras.se/sam/", "origo"
    )

    assert any(
        item["url"] == "https://kartor.vasteras.se/sam/vas.json" for item in found
    )


def test_api_identifier_origo_gallery_hrefs(monkeypatch):
    class _OrigoGallery:
        def get(self, url, **kwargs):
            if url.rstrip("/") == "https://karta.sundsvall.se":
                return _DummyResponse(
                    content=b'<a href="sundsvall/">Sundsvall</a>',
                    headers={"Content-Type": "text/html"},
                    text='<a href="sundsvall/">Sundsvall</a>',
                )
            if url == "https://karta.sundsvall.se/sundsvall/index.json":
                return _DummyResponse(
                    content=b'{"controls":[],"layers":[]}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OrigoGallery())

    found = apidetect.api_identifier("https://karta.sundsvall.se/", "origo")

    assert any(item["type"] == "origo:config" for item in found)
    assert any(
        item["url"] == "https://karta.sundsvall.se/sundsvall/index.json"
        for item in found
    )


def test_swing_urlmap_includes_viewer():
    urls = [item["url"] for item in apidetect.CATALOGS_URLMAP["swing"]]
    assert "/databank" in urls
    assert "/viewer/" in urls


def test_api_identifier_minerva_projects(monkeypatch):
    class _MinervaSession:
        def get(self, url, **kwargs):
            if url == "https://maps.example.org/minerva/api/projects/":
                return _DummyResponse(
                    content=b'[{"projectId":"pdmap"}]',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _MinervaSession())

    found = apidetect.api_identifier(
        "https://maps.example.org/minerva/", "minerva"
    )

    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://maps.example.org/minerva/api/projects/"
        for item in found
    )
    assert not any(item["type"] == "custom_api" for item in found)


def test_api_identifier_clld_parameters_json(monkeypatch):
    class _ClldSession:
        def get(self, url, **kwargs):
            if url == "https://grambank.clld.org/parameters.json":
                return _DummyResponse(
                    content=b'[{"id":"GB020"}]',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _ClldSession())

    found = apidetect.api_identifier("https://grambank.clld.org/", "clld")

    assert any(item["type"] == "api" for item in found)
    assert any(
        item["url"] == "https://grambank.clld.org/parameters.json" for item in found
    )


def test_api_identifier_synapse_absolute_url(monkeypatch):
    class _SynapseSession:
        def get(self, url, **kwargs):
            if url == "https://repo-prod.prod.sagebase.org/repo/v1/version":
                return _DummyResponse(
                    content=b'{"version":"1"}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _SynapseSession())

    found = apidetect.api_identifier("https://www.synapse.org", "synapse")

    assert any(item["type"] == "synapse:api" for item in found)
    assert any(
        item["url"] == "https://repo-prod.prod.sagebase.org/repo/v1/version"
        for item in found
    )


def test_api_identifier_yoda_oai(monkeypatch):
    class _YodaSession:
        def get(self, url, **kwargs):
            if url.endswith("/oai/oai?verb=Identify"):
                return _DummyResponse(
                    content=b"<OAI-PMH><Identify/></OAI-PMH>",
                    headers={"Content-Type": "text/xml"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _YodaSession())

    found = apidetect.api_identifier(
        "https://public.yoda.uu.nl/datasets", "yoda"
    )

    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://public.yoda.uu.nl/oai/oai?verb=Identify"
        for item in found
    )


def test_api_identifier_activemapgis_groups(monkeypatch):
    class _AmgSession:
        def get(self, url, **kwargs):
            if url.endswith("/groups/withLayers"):
                return _DummyResponse(
                    content=b'[{"id":1,"layers":[]}]',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _AmgSession())

    found = apidetect.api_identifier("https://vao.geofsm.ru", "activemapgis")

    assert any(item["type"] == "activemapgis:groups" for item in found)
    assert any(
        item["url"] == "https://vao.geofsm.ru/groups/withLayers" for item in found
    )


def test_api_identifier_opendatacube_stac(monkeypatch):
    class _OdcSession:
        def get(self, url, **kwargs):
            if url == "https://explorer.example.org/stac":
                return _DummyResponse(
                    content=b'{"type":"Catalog","stac_version":"1.0.0"}',
                    headers={"Content-Type": "application/json"},
                )
            return _DummyResponse(
                status_code=404, headers={"Content-Type": "text/html"}, content=b""
            )

        def post(self, *args, **kwargs):
            return _DummyResponse(status_code=404, content=b"")

    monkeypatch.setattr(apidetect.requests, "Session", lambda: _OdcSession())

    found = apidetect.api_identifier("https://explorer.example.org", "opendatacube")

    assert any(item["type"] == "stacserverapi" for item in found)
    assert any(item["url"] == "https://explorer.example.org/stac" for item in found)


def test_custom_urlmap_includes_dump_protocols():
    urls = {item["url"] for item in apidetect.CUSTOM_URLMAP}
    types = {item["id"] for item in apidetect.CUSTOM_URLMAP}
    assert "/catalog.xml" in urls
    assert "/catalog.rdf" in urls
    assert "/catalog.ttl" in urls
    assert "/oai?verb=Identify" in urls
    assert "/sparql" in urls
    assert "/csw?service=CSW&version=2.0.2&request=GetCapabilities" in urls
    assert "oaipmh20" in types
    assert "csw202" in types
    assert "sparql" in types


def test_infer_endpoints_verified_skips_custom_without_http(monkeypatch):
    def _fail(*args, **kwargs):
        raise AssertionError("custom must not be probed by quality fixers")

    monkeypatch.setattr(apidetect, "api_identifier", _fail)
    found = apidetect.infer_endpoints_verified(
        {"software": {"id": "custom"}, "link": "https://example.org/data"}
    )
    assert found == []


def test_detect_record_skips_custom_without_include_flag(monkeypatch):
    called = []

    def _one(*args, **kwargs):
        called.append(True)

    monkeypatch.setattr(apidetect, "__detect_one", _one)
    record = {"software": {"id": "custom"}, "link": "https://example.org"}
    apidetect._detect_record("x.yaml", "x.yaml", record, "insert", False)
    assert called == []
    apidetect._detect_record(
        "x.yaml", "x.yaml", record, "insert", False, include_custom=True
    )
    assert called == [True]


def test_detect_record_skips_unknown_software_without_include_flag(monkeypatch):
    called = []
    monkeypatch.setattr(apidetect, "__detect_one", lambda *a, **k: called.append(True))
    record = {"software": {"id": "notasoftwareid"}, "link": "https://example.org"}
    apidetect._detect_record("x.yaml", "x.yaml", record, "insert", False)
    assert called == []
    apidetect._detect_record(
        "x.yaml", "x.yaml", record, "insert", False, include_custom=True
    )
    assert called == [True]


def _xml_ok(body=b"<root/>"):
    return _DummyResponse(content=body, headers={"Content-Type": "application/xml"})


def _json_ok(body=b"{}"):
    return _DummyResponse(content=body, headers={"Content-Type": "application/json"})


def _html_404():
    return _DummyResponse(
        status_code=404, headers={"Content-Type": "text/html"}, content=b""
    )


class _SelectiveSession:
    def __init__(self, mapping):
        self._mapping = mapping

    def get(self, url, **kwargs):
        for suffix, response in self._mapping.items():
            if url.endswith(suffix) or suffix in url:
                return response
        return _html_404()

    def post(self, *args, **kwargs):
        return _html_404()


def test_ckan_oai_and_catalog_rdf(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
            "/catalog.rdf": _DummyResponse(
                content=b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'/>",
                headers={"Content-Type": "application/rdf+xml"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "ckan")
    types = {item["type"] for item in found}
    urls = {item["url"] for item in found}
    assert "oaipmh20" in types
    assert "dcat" in types
    assert "https://data.example.org/oai?verb=Identify" in urls
    assert "https://data.example.org/catalog.rdf" in urls


def test_geonetwork_dcat_and_ogc_records(monkeypatch):
    session = _SelectiveSession(
        {
            "/srv/api/records?accept=application/rdf+xml": _DummyResponse(
                content=b"<rdf:RDF/>",
                headers={"Content-Type": "application/rdf+xml"},
            ),
            "/srv/ogc/records/collections?f=json": _json_ok(
                b'{"collections":[]}'
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://geo.example.org/geonetwork", "geonetwork")
    types = {item["type"] for item in found}
    assert "dcat:xml" in types
    assert "ogcrecordsapi" in types


def test_frostserver_probes_are_sensorthings(monkeypatch):
    session = _SelectiveSession({"/v1.1/": _json_ok(b'{"value":[]}')})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://frost.example.org", "frostserver")
    assert found
    assert all(item["type"] == "sensorthings" for item in found)


def test_deegree_webservices_csw(monkeypatch):
    session = _SelectiveSession(
        {
            "/deegree-webservices/services?service=CSW&version=2.0.2&request=GetCapabilities": _xml_ok(
                b"<Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://gis.example.si", "deegree")
    assert any(item["type"] == "csw202" for item in found)
    assert any(
        item["url"].endswith(
            "/deegree-webservices/services?service=CSW&version=2.0.2&request=GetCapabilities"
        )
        for item in found
    )


def test_wikibase_sparql_probe(monkeypatch):
    session = _SelectiveSession(
        {
            "/sparql": _DummyResponse(
                content=b'{"head":{}}',
                headers={"Content-Type": "application/sparql-results+json"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://wikibase.example.org", "wikibase")
    assert any(item["type"] == "sparql" for item in found)


def test_dspacecris_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/server/oai/request?verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://cris.example.org", "dspacecris")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"].endswith("/server/oai/request?verb=Identify") for item in found
    )


def test_datasette_databases_json(monkeypatch):
    session = _SelectiveSession(
        {
            "/-/databases.json": _json_ok(b'[{"name":"data"}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "datasette")
    assert any(item["type"] == "datasette:databases" for item in found)
    assert any(item["url"].endswith("/-/databases.json") for item in found)


def test_hyrax_catalog_json(monkeypatch):
    session = _SelectiveSession(
        {
            "/catalog.json": _json_ok(b'{"response":{"docs":[]}}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://hyrax.example.edu", "hyrax")
    assert any(item["type"] == "hyrax:catalog" for item in found)
    assert any(item["url"].endswith("/catalog.json") for item in found)


def test_hyrax_catalog_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/catalog/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://hyrax.example.edu", "hyrax")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"].endswith("/catalog/oai?verb=Identify") for item in found
    )


def test_dachs_tap_capabilities_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/tap/capabilities": _xml_ok(b"<vosi:capabilities/>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://vo.example.org", "dachs")
    assert found
    assert all(item["type"] == "tap:capabilities" for item in found)
    assert any(item["url"].endswith("/tap/capabilities") for item in found)


def test_dachs_oai_xml_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai.xml?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://vo.example.org", "dachs")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://vo.example.org/oai.xml?verb=Identify" for item in found
    )


def test_esasciencearchive_tap_capabilities_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/tap/capabilities": _xml_ok(b"<vosi:capabilities/>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://gea.esac.example.esa", "esasciencearchive")
    assert any(item["type"] == "tap:capabilities" for item in found)
    assert not any(item["type"] == "customapi" for item in found)


def test_copernicusdhus_odata_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/odata/v1/Products?$top=1": _xml_ok(b"<feed xmlns='http://www.w3.org/2005/Atom'/>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://dhus.example.int", "copernicusdhus")
    assert found
    assert all(item["type"] == "odata" for item in found)
    assert any(
        item["url"].endswith("/odata/v1/Products?$top=1") for item in found
    )
    found_hash = apidetect.api_identifier(
        "https://sentinels.example.int/dhus/#/home", "copernicusdhus"
    )
    assert any(
        item["url"]
        == "https://sentinels.example.int/dhus/odata/v1/Products?$top=1"
        for item in found_hash
    )


def test_pygeoapi_collections_are_ogc_features(monkeypatch):
    session = _SelectiveSession(
        {
            "/collections/?f=json": _json_ok(b'{"collections":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://ogcapi.example.org", "pygeoapi")
    assert any(item["type"] == "ogc:features" for item in found)
    assert not any(item["type"] == "pygeoapi:collections" for item in found)


def test_opendatasoft_api_and_dcat_export(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/explore/v2.1/catalog/datasets?limit=1": _json_ok(
                b'{"total_count":0,"results":[]}'
            ),
            "/api/v2/catalog/exports/dcat": _DummyResponse(
                content=b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'/>",
                headers={"Content-Type": "application/rdf+xml"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "opendatasoft")
    types = {item["type"] for item in found}
    urls = {item["url"] for item in found}
    assert "opendatasoftapi" in types
    assert "opendatasoft" not in types
    assert "dcat:xml" in types
    assert (
        "https://data.example.org/api/explore/v2.1/catalog/datasets?limit=1" in urls
    )
    assert "https://data.example.org/api/v2/catalog/exports/dcat" in urls


def test_ckan_sparql_probe(monkeypatch):
    session = _SelectiveSession(
        {
            "/sparql": _DummyResponse(
                content=b'{"head":{}}',
                headers={"Content-Type": "application/sparql-results+json"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "ckan")
    assert any(item["type"] == "sparql" for item in found)
    assert any(item["url"].endswith("/sparql") for item in found)


def test_datapress_sparql_probe(monkeypatch):
    session = _SelectiveSession(
        {
            "/sparql": _DummyResponse(
                content=b'{"head":{}}',
                headers={"Content-Type": "application/sparql-results+json"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "datapress")
    assert any(item["type"] == "sparql" for item in found)
    assert any(item["url"].endswith("/sparql") for item in found)


def test_islandora_oai_identify_paths(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai/request?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
            "/oai2?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://islandora.example.edu", "islandora")
    urls = {item["url"] for item in found if item["type"] == "oaipmh20"}
    assert urls == {
        "https://islandora.example.edu/oai/request?verb=Identify",
        "https://islandora.example.edu/oai2?verb=Identify",
        "https://islandora.example.edu/oai?verb=Identify",
    }


def test_archipelago_oai_and_jsonapi(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/oai_pmh/oai?verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
            "/jsonapi/node/digital_object": _json_ok(b'{"data":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://archipelago.example.org", "archipelago")
    types = {item["type"] for item in found}
    urls = {item["url"] for item in found}
    assert "oaipmh20" in types
    assert "drupal:jsonapi" in types
    assert (
        "https://archipelago.example.org/api/oai_pmh/oai?verb=Identify" in urls
    )
    assert (
        "https://archipelago.example.org/jsonapi/node/digital_object" in urls
    )


def test_datafair_api_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/data-fair/api/v1/datasets": _json_ok(b'{"count":0,"results":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://opendata.example.fr", "datafair")
    assert any(item["type"] == "datafairapi" for item in found)
    assert not any(item["type"] == "customapi" for item in found)


def test_dataeye_ckan_compatible_paths(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/3/action/status_show": _json_ok(b'{"success":true,"result":{}}'),
            "/ckan_api/package_search": _json_ok(b'{"success":true,"result":{}}'),
            "/ckan_api/package_list": _json_ok(b'{"success":true,"result":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://city.dataeye.jp", "dataeye")
    by_url = {item["url"]: item["type"] for item in found}
    assert (
        by_url["https://city.dataeye.jp/api/3/action/status_show"]
        == "ckan:status-show"
    )
    assert (
        by_url["https://city.dataeye.jp/ckan_api/package_search"]
        == "ckan:package-search"
    )
    assert (
        by_url["https://city.dataeye.jp/ckan_api/package_list"]
        == "ckan:package-list"
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_ouropendata_package_list_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/package_list": _json_ok(b'["dataset-1"]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://opendata.example.jp", "ouropendata")
    assert any(item["type"] == "ouropendata:packages" for item in found)
    assert not any(item["type"] == "customapi" for item in found)
    assert not any(item["type"].startswith("ckan") for item in found)


def test_cbioportal_studies_type_uses_origin(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/studies": _json_ok(b'[{"studyId":"acc_tcga"}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://www.cbioportal.org/datasets", "cbioportal"
    )
    assert any(item["type"] == "cbioportal:studies" for item in found)
    assert any(
        item["url"] == "https://www.cbioportal.org/api/studies" for item in found
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_huggingface_api_type_uses_origin(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/datasets?limit=1": _json_ok(b'[{"id":"demo"}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://huggingface.co/datasets/", "huggingface"
    )
    assert any(item["type"] == "huggingface:api" for item in found)
    assert any(
        item["url"] == "https://huggingface.co/api/datasets?limit=1" for item in found
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_bexis2_dataset_api_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/dataset": _json_ok(b'[{"id":1}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://bexis.example.org", "bexis2")
    assert any(item["type"] == "bexis2:datasets" for item in found)
    assert not any(item["type"] == "customapi" for item in found)


def test_djehuty_records_and_articles(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/records?size=1": _json_ok(b'{"hits":{"hits":[]}}'),
            "/v2/articles": _json_ok(b'{"items":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.nl", "djehuty")
    by_url = {item["url"]: item["type"] for item in found}
    assert (
        by_url["https://data.example.nl/api/records?size=1"]
        == "inveniordmapi:records"
    )
    assert by_url["https://data.example.nl/v2/articles"] == "rest"


def test_omegapsir_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://omega.example.pl", "omegapsir")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://omega.example.pl/oai?verb=Identify" for item in found
    )


def test_omegapsir_is_mapped():
    from apidetect_urlmaps_draft import NO_STANDARD_PROBE

    assert "omegapsir" not in NO_STANDARD_PROBE
    assert "omegapsir" in apidetect.CATALOGS_URLMAP


def test_dabar_alternate_oai_path(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://repo.example.hr", "dabar")
    assert any(
        item["url"] == "https://repo.example.hr/oai?verb=Identify" for item in found
    )


def test_opensciencesi_slash_oai_path(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai/?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://repo.example.si", "opensciencesi")
    assert any(
        item["url"] == "https://repo.example.si/oai/?verb=Identify" for item in found
    )


def test_clld_parameters_index(monkeypatch):
    session = _SelectiveSession(
        {
            "/parameters": _DummyResponse(
                content=b"<html><title>Parameters</title></html>",
                headers={"Content-Type": "text/html"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://grambank.clld.org", "clld")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"] == "https://grambank.clld.org/parameters" for item in found
    )


def test_biodare2_experiments_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/experiments?showPublic=true": _json_ok(b'[{"id":1}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://biodare2.ed.ac.uk", "biodare2")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://biodare2.ed.ac.uk/api/experiments?showPublic=true"
        for item in found
    )


def test_templateflow_browse_index(monkeypatch):
    session = _SelectiveSession(
        {
            "/browse/": _DummyResponse(
                content=b"<html><title>TemplateFlow</title></html>",
                headers={"Content-Type": "text/html"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://www.templateflow.org", "templateflow")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"] == "https://www.templateflow.org/browse/" for item in found
    )


def test_intermine_version_type(monkeypatch):
    session = _SelectiveSession({"/service/version": _json_ok(b'"1.0"')})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://www.flymine.org", "intermine")
    assert any(item["type"] == "intermine:version" for item in found)
    assert any(
        item["url"] == "https://www.flymine.org/service/version" for item in found
    )


def test_xnat_projects_type(monkeypatch):
    session = _SelectiveSession({"/data/projects": _json_ok(b'{"ResultSet":{}}')})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://xnat.example.org", "xnat")
    assert any(item["type"] == "xnat:projects" for item in found)
    assert any(
        item["url"] == "https://xnat.example.org/data/projects" for item in found
    )


def test_smw_dataset_ask(monkeypatch):
    session = _SelectiveSession(
        {
            "/w/api.php?action=ask&query=[[Category:Dataset]]&format=json": _json_ok(
                b'{"query":{"results":{}}}'
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://wiki.example.org", "smw")
    assert any(item["type"] == "smw:ask" for item in found)
    assert any(
        "action=ask" in item["url"] and "Category:Dataset" in item["url"]
        for item in found
    )


def test_inveniordm_oai2d_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai2d?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://repo.example.org", "inveniordm")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://repo.example.org/oai2d?verb=Identify" for item in found
    )


def test_eprints_oai2_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai2?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://eprints.example.ac.uk", "eprints")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://eprints.example.ac.uk/oai2?verb=Identify"
        for item in found
    )


def test_eprints_opensearch_description(monkeypatch):
    session = _SelectiveSession(
        {
            "/cgi/opensearchdescription": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://eprints.example.ac.uk", "eprints")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"]
        == "https://eprints.example.ac.uk/cgi/opensearchdescription"
        for item in found
    )


def test_dspace_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://dspace.example.edu", "dspace")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://dspace.example.edu/oai?verb=Identify" for item in found
    )


def test_greenstone2_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/greenstone/cgi-bin/oaiserver.cgi?verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://gs.example.edu", "greenstone")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"].endswith("/greenstone/cgi-bin/oaiserver.cgi?verb=Identify")
        for item in found
    )


def test_dataverse_info_version(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/info/version": _json_ok(b'{"status":"OK","data":{"version":"6.0"}}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://dataverse.example.edu", "dataverse")
    assert any(item["type"] == "dataverseapi" for item in found)
    assert any(
        item["url"] == "https://dataverse.example.edu/api/info/version" for item in found
    )


def test_drupal_open_data_jsonapi_bundle(monkeypatch):
    session = _SelectiveSession(
        {
            "/jsonapi/node/open_data": _json_ok(b'{"data":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://opendata.example.gov", "drupal")
    assert any(item["type"] == "drupal:jsonapi:dataset" for item in found)
    assert any(
        item["url"] == "https://opendata.example.gov/jsonapi/node/open_data"
        for item in found
    )


def test_pxweb_api_v1_root(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v1/": _json_ok(b'[{"id":"en","type":"l"}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://statistik.example.se", "pxweb")
    assert any(item["type"] == "pxwebapi" for item in found)
    assert any(
        item["url"] == "https://statistik.example.se/api/v1/" for item in found
    )


def test_edatos_indicators_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/indicators/v1.0/indicators": _json_ok(b'{"version":"2.0","class":"collection"}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://www.example.edatos.io", "edatos")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://www.example.edatos.io/indicators/v1.0/indicators"
        for item in found
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_superset_dataset_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v1/dataset/": _json_ok(b'{"result":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://bi.example.org", "superset")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://bi.example.org/api/v1/dataset/" for item in found
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_iochembd_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://iochem.example.org", "iochembd")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://iochem.example.org/oai?verb=Identify" for item in found
    )


def test_opendap_catalog_xml(monkeypatch):
    session = _SelectiveSession(
        {
            "/opendap/catalog.xml": _xml_ok(b"<catalog xmlns='http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'/>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://dap.example.edu", "opendaphyrax")
    assert any(item["type"] == "opendap:catalog" for item in found)
    assert any(
        item["url"] == "https://dap.example.edu/opendap/catalog.xml" for item in found
    )


def test_dspace_server_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/server/oai/request?verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://dspace.example.edu", "dspace")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://dspace.example.edu/server/oai/request?verb=Identify"
        for item in found
    )


def test_invenio_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://repo.example.org", "invenio")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"] == "https://repo.example.org/oai?verb=Identify" for item in found
    )


def test_pxweb_sv_language_tree(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v1/sv/": _json_ok(b'[{"id":"AM","type":"l"}]'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://api.scb.se", "pxweb")
    assert any(item["type"] == "pxwebapi" for item in found)
    assert any(item["url"] == "https://api.scb.se/api/v1/sv/" for item in found)


def test_gc2_configuration_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v2/configuration": _json_ok(b'{"success":true}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://gc2.example.dk", "gc2")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://gc2.example.dk/api/v2/configuration" for item in found
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_nextstrain_charon_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/charon/getAvailable": _json_ok(b'{"datasets":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://nextstrain.org", "nextstrain")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://nextstrain.org/charon/getAvailable" for item in found
    )
    assert not any(item["type"] == "customapi" for item in found)


def test_nextstrain_instance_does_not_probe_hub(monkeypatch):
    session = _SelectiveSession(
        {
            "/charon/getAvailable": _json_ok(b'{"datasets":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://insaflu.insa.pt", "nextstrain")
    urls = [item["url"] for item in found]
    assert "https://insaflu.insa.pt/charon/getAvailable" in urls
    assert "https://nextstrain.org/charon/getAvailable" not in urls


def test_seek_api_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/api": _json_ok(b'{"jsonapi":{"version":"1.0"}}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://fairdomhub.org", "seek")
    assert any(item["type"] == "rest" for item in found)
    assert any(item["url"] == "https://fairdomhub.org/api" for item in found)
    assert not any(item["type"] == "customapi" for item in found)


def test_clld_download_index(monkeypatch):
    session = _SelectiveSession(
        {
            "/download": _DummyResponse(
                content=b"<html><title>Download</title></html>",
                headers={"Content-Type": "text/html"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://apics-online.info", "clld")
    assert any(item["type"] == "index" for item in found)
    assert any(item["url"] == "https://apics-online.info/download" for item in found)


def _html_ok(body=b"<html><title>ok</title></html>"):
    return _DummyResponse(content=body, headers={"Content-Type": "text/html"})


def test_vufind_dataset_search_index(monkeypatch):
    session = _SelectiveSession(
        {
            '/Search/Results?type=AllFields&filter[]=format%3A"Dataset"': _html_ok(),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://catalog.example.edu", "vufind")
    urls = [item["url"] for item in found if item["type"] == "index"]
    assert (
        'https://catalog.example.edu/Search/Results?type=AllFields&filter[]=format%3A"Dataset"'
        in urls
    )
    assert not any("/vufind/Search/Results" in item["url"] for item in found)


def test_librecat_dataset_search_index(monkeypatch):
    session = _SelectiveSession(
        {
            '/Search/Results?type=AllFields&filter[]=format%3A"Dataset"': _html_ok(),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://pub.example.edu", "librecat")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"]
        == 'https://pub.example.edu/Search/Results?type=AllFields&filter[]=format%3A"Dataset"'
        for item in found
    )


def test_islandora_solr_dataset_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/solr/select": _DummyResponse(
                content=b'{"response":{"numFound":0,"docs":[]}}',
                headers={"Content-Type": "text/plain"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://islandora.example.edu", "islandora")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"].endswith(
            "/solr/select?q=RELS_EXT_hasModel_uri_ms:*Dataset*&wt=json&rows=25"
        )
        for item in found
    )


def test_archipelago_dataset_search_index(monkeypatch):
    session = _SelectiveSession(
        {
            "descriptive_metadata_object_types:Dataset": _html_ok(),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://archipelago.example.org", "archipelago")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"]
        == "https://archipelago.example.org/search?f[0]=descriptive_metadata_object_types:Dataset"
        for item in found
    )


def test_figshare_articles_dataset_index(monkeypatch):
    session = _SelectiveSession(
        {
            "/articles/dataset/": _html_ok(),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://figshare.example.edu", "figshare")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"] == "https://figshare.example.edu/articles/dataset/" for item in found
    )


def test_divaportal_smash_search_index(monkeypatch):
    session = _SelectiveSession(
        {
            "/smash/search.jsf": _html_ok(),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://uu.diva-portal.org", "divaportal")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"] == "https://uu.diva-portal.org/smash/search.jsf" for item in found
    )


def test_pure_locale_datasets_rss(monkeypatch):
    session = _SelectiveSession(
        {
            "/de/datasets/?search=&isCopyPasteSearch=false&format=rss": _xml_ok(
                b"<rss><channel/></rss>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://pure.example.de", "pure")
    assert any(item["type"] == "rss" for item in found)
    assert any(
        item["url"]
        == "https://pure.example.de/de/datasets/?search=&isCopyPasteSearch=false&format=rss"
        for item in found
    )


def test_palapa_geoserver_wms(monkeypatch):
    session = _SelectiveSession(
        {
            "/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities": _xml_ok(
                b"<WMS_Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://geoportal.example.go.id", "palapa")
    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"]
        == "https://geoportal.example.go.id/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
        for item in found
    )


def test_palapa_geoserver_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities": _xml_ok(
                b"<WMS_Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://geoportal.example.go.id/geoserver", "palapa"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://geoportal.example.go.id/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
        in urls
    )
    assert not any("/geoserver/geoserver/" in item["url"] for item in found)


def test_talkbank_data_html_index(monkeypatch):
    session = _SelectiveSession({"/data.html": _html_ok()})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://childes.talkbank.org", "talkbank")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"] == "https://childes.talkbank.org/data.html" for item in found
    )


def test_talkbank_strips_data_html(monkeypatch):
    session = _SelectiveSession({"/data.html": _html_ok()})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://childes.talkbank.org/data.html", "talkbank"
    )
    urls = [item["url"] for item in found]
    assert "https://childes.talkbank.org/data.html" in urls
    assert not any("/data.html/data.html" in item["url"] for item in found)


def test_materialscloud_explore_index(monkeypatch):
    session = _SelectiveSession({"/explore": _html_ok()})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://www.materialscloud.org/explore", "materialscloud"
    )
    urls = [item["url"] for item in found]
    assert any(item["type"] == "index" for item in found)
    assert "https://www.materialscloud.org/explore" in urls
    assert not any("/explore/explore" in item["url"] for item in found)


def test_icat_portlet_index(monkeypatch):
    session = _SelectiveSession({"/icat/portlet/": _html_ok()})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "icat")
    assert any(item["type"] == "index" for item in found)
    assert any(
        item["url"] == "https://data.example.org/icat/portlet/" for item in found
    )


def test_icat_portlet_link_does_not_double(monkeypatch):
    session = _SelectiveSession({"/icat/portlet/": _html_ok()})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://data.example.org/icat/portlet/", "icat"
    )
    urls = [item["url"] for item in found]
    assert "https://data.example.org/icat/portlet/" in urls
    assert not any("/icat/portlet/icat/portlet" in item["url"] for item in found)


def test_phaidra_dataset_solr_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/search/select?q=cmodel:*Dataset*&wt=json&rows=25": _DummyResponse(
                content=b'{"response":{"numFound":0,"docs":[]}}',
                headers={"Content-Type": "text/plain"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://phaidra.example.ac.at", "phaidra")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"].endswith(
            "/api/search/select?q=cmodel:*Dataset*&wt=json&rows=25"
        )
        for item in found
    )


def test_gringlobal_root_index(monkeypatch):
    session = _SelectiveSession({"/gringlobal/": _html_ok()})
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://npgsweb.ars-grin.gov/gringlobal/search", "gringlobal"
    )
    urls = [item["url"] for item in found]
    assert any(item["type"] == "index" for item in found)
    assert "https://npgsweb.ars-grin.gov/gringlobal/" in urls
    assert not any("/gringlobal/gringlobal/" in item["url"] for item in found)


def test_esrigeo_csw_getcapabilities(monkeypatch):
    session = _SelectiveSession(
        {
            "/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities": _xml_ok(
                b"<csw:Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://geoportal.example.gov", "esrigeo"
    )
    assert any(item["type"] == "csw202" for item in found)
    assert any(
        item["url"]
        == "https://geoportal.example.gov/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetCapabilities"
        for item in found
    )


def test_ramadda_repository_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/repository/entry/show?output=json": _json_ok(b'{"id":"root"}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://ramadda.unidata.ucar.edu/repository", "ramadda"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://ramadda.unidata.ucar.edu/repository/entry/show?output=json" in urls
    )
    assert not any("/repository/repository/" in item["url"] for item in found)


def test_frostserver_things_sensorthings(monkeypatch):
    session = _SelectiveSession(
        {
            "/v1.1/Things?$top=1&$count=true": _json_ok(b'{"value":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://frost.example.org", "frostserver")
    assert any(item["type"] == "sensorthings" for item in found)
    assert any(
        item["url"].endswith("/v1.1/Things?$top=1&$count=true") for item in found
    )


def test_frostserver_url_cleanup_strips_only_frost_server_mount():
    assert (
        apidetect.frostserver_url_cleanup_func(
            "https://iot.example.org/FROST-Server/"
        )
        == "https://iot.example.org"
    )
    assert (
        apidetect.frostserver_url_cleanup_func(
            "https://timeseries.example.org/soop/FROST-Server/"
        )
        == "https://timeseries.example.org/soop"
    )
    assert (
        apidetect.frostserver_url_cleanup_func(
            "https://frost.iotlab.example/sensorthings/"
        )
        == "https://frost.iotlab.example/sensorthings"
    )
    assert (
        apidetect.frostserver_url_cleanup_func(
            "https://ingest.example.org/sta/"
        )
        == "https://ingest.example.org/sta"
    )
    assert (
        apidetect.frostserver_url_cleanup_func(
            "https://covidsta.example.org/server/"
        )
        == "https://covidsta.example.org/server"
    )
    assert (
        apidetect.frostserver_url_cleanup_func(
            "https://www.samenmeten.example/dataportaal/"
        )
        == "https://www.samenmeten.example/dataportaal"
    )


def test_frostserver_frost_server_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/FROST-Server/v1.1/Things?$top=1&$count=true": _json_ok(
                b'{"value":[]}'
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://iot.example.org/FROST-Server/", "frostserver"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://iot.example.org/FROST-Server/v1.1/Things?$top=1&$count=true"
        in urls
    )
    assert not any("/FROST-Server/FROST-Server/" in item["url"] for item in found)


def test_erdasapollo_iws_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/erdas-iws/ogc/wms/?service=WMS&request=GetCapabilities&version=1.3.0": _xml_ok(
                b"<WMS_Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://maps.example.gov/erdas-iws/", "erdasapollo"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://maps.example.gov/erdas-iws/ogc/wms/?service=WMS&request=GetCapabilities&version=1.3.0"
        in urls
    )
    assert not any("/erdas-iws/erdas-iws/" in item["url"] for item in found)


def test_erdasapollo_esri_rest_link_strips_to_origin():
    assert (
        apidetect.erdasapollo_url_cleanup_func(
            "https://ortos.example.es/erdas-iws/esri/rest/services/"
        )
        == "https://ortos.example.es"
    )
    assert (
        apidetect.erdasapollo_url_cleanup_func(
            "https://apollo.example.com/erdas-apollo"
        )
        == "https://apollo.example.com"
    )


def test_cubewerx_cubeserv_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/cubewerx/cubeserv?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities": _xml_ok(
                b"<WMS_Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://maps.example.ca/cubewerx/cubeserv", "cubewerx"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://maps.example.ca/cubewerx/cubeserv?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities"
        in urls
    )
    assert not any("/cubewerx/cubeserv/cubewerx/" in item["url"] for item in found)


def test_greenstone_library_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/greenstone3/oaiserver?verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://library.example.edu/greenstone3/library", "greenstone"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://library.example.edu/greenstone3/oaiserver?verb=Identify" in urls
    )
    assert not any("/greenstone3/library/greenstone3/" in item["url"] for item in found)


def test_bitrix_opendata_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/opendata/opendata.json": _json_ok(b'{"items":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://city.example.ru/opendata/", "bitrix"
    )
    urls = [item["url"] for item in found]
    assert "https://city.example.ru/opendata/opendata.json" in urls
    assert not any("/opendata/opendata/opendata.json" in item["url"] for item in found)


def test_bitrix_opendata_keeps_locale_prefix():
    assert (
        apidetect.bitrix_url_cleanup_func(
            "https://www.orel-adm.example/ru/opendata/data/"
        )
        == "https://www.orel-adm.example/ru"
    )


def test_massbank_mount_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/MassBank/api/records": _json_ok(b'{"data":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://massbank.example/MassBank/", "massbank"
    )
    urls = [item["url"] for item in found]
    assert "https://massbank.example/MassBank/api/records" in urls
    assert not any("/MassBank/MassBank/" in item["url"] for item in found)


def test_nada_index_php_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/index.php/api/catalog/search": _json_ok(b'{"result":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://microdata.example.org/index.php", "nada"
    )
    urls = [item["url"] for item in found]
    assert "https://microdata.example.org/index.php/api/catalog/search" in urls
    assert not any("/index.php/index.php/" in item["url"] for item in found)


def test_stacbrowser_catalog_json_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/catalog.json": _json_ok(b'{"type":"Catalog","stac_version":"1.0.0"}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://stac.example.org/catalog.json", "stacbrowser"
    )
    urls = [item["url"] for item in found]
    assert "https://stac.example.org/catalog.json" in urls
    assert not any("/catalog.json/catalog.json" in item["url"] for item in found)


def test_micka_mount_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/micka/csw?service=CSW&version=2.0.2&request=GetCapabilities": _xml_ok(
                b"<csw:Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://geoportal.example.cz/micka/", "micka"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://geoportal.example.cz/micka/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        in urls
    )
    assert not any("/micka/micka/" in item["url"] for item in found)


def test_micka_url_cleanup_keeps_php_prefix():
    assert (
        apidetect.micka_url_cleanup_func(
            "https://geoportal.gov.example/php/micka/"
        )
        == "https://geoportal.gov.example/php"
    )


def test_micka_opensearch_on_mount(monkeypatch):
    session = _SelectiveSession(
        {
            "/micka/opensearch": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://geoportal.example.cz/micka/", "micka"
    )
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://geoportal.example.cz/micka/opensearch"
        for item in found
    )
    assert not any("/micka/micka/" in item["url"] for item in found)


def test_wis20box_oapi_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/oapi/collections/?f=json": _json_ok(b'{"collections":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://wis2.example.gov/oapi", "wis20box"
    )
    urls = [item["url"] for item in found]
    assert "https://wis2.example.gov/oapi/collections/?f=json" in urls
    assert not any("/oapi/oapi/" in item["url"] for item in found)


def test_symbiota_portal_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/portal/collections/datasets/rsshandler.php": _xml_ok(
                b"<rss><channel/></rss>"
            ),
            "/portal/collections/index.php": _DummyResponse(
                content=b"<html><title>Collections</title></html>",
                headers={"Content-Type": "text/html"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://herbarium.example.edu/portal/", "symbiota"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://herbarium.example.edu/portal/collections/datasets/rsshandler.php"
        in urls
    )
    assert "https://herbarium.example.edu/portal/collections/index.php" in urls
    assert not any("/portal/portal/" in item["url"] for item in found)


def test_lkod_opendata_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/opendata/set/lkod": _DummyResponse(
                content=b"@prefix dcat: <http://www.w3.org/ns/dcat#> .",
                headers={"Content-Type": "text/turtle"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://opendata.example.sk/opendata/set/lkod", "lkod"
    )
    urls = [item["url"] for item in found]
    assert "https://opendata.example.sk/opendata/set/lkod" in urls
    assert not any("/opendata/opendata/" in item["url"] for item in found)


def test_tianditu_city_node_tree(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/cityNode/queryByTree.json": _json_ok(b'{"data":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://henan.example.gov.cn/jiaozuo/", "tianditu"
    )
    urls = [item["url"] for item in found]
    assert "https://henan.example.gov.cn/api/cityNode/queryByTree.json" in urls


def test_ecb_dataflow_uses_api_host(monkeypatch):
    session = _SelectiveSession(
        {
            "https://data-api.ecb.europa.eu/service/dataflow": _xml_ok(
                b"<message:Structure/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.ecb.europa.eu", "ecb")
    urls = [item["url"] for item in found]
    assert "https://data-api.ecb.europa.eu/service/dataflow" in urls
    assert any(item["type"] == "sdmx:dataflows" for item in found)
    assert not any(
        item["url"] == "https://data.ecb.europa.eu/service/dataflow" for item in found
    )


def test_world_bank_indicator_api_host(monkeypatch):
    session = _SelectiveSession(
        {
            "https://api.worldbank.org/v2/indicator?format=json&per_page=1000": _json_ok(
                b'[{"page":1,"pages":1}]'
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.worldbank.org", "dataworldbankorg")
    urls = [item["url"] for item in found]
    assert (
        "https://api.worldbank.org/v2/indicator?format=json&per_page=1000" in urls
    )


def test_dandi_and_cellxgene_hub_api_hosts(monkeypatch):
    session = _SelectiveSession(
        {
            "https://api.dandiarchive.org/api/dandisets/": _json_ok(b'{"results":[]}'),
            "https://api.cellxgene.cziscience.com/curation/v1/datasets": _json_ok(
                b"[]"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    dandi = apidetect.api_identifier("https://dandiarchive.org", "dandi")
    cellxgene = apidetect.api_identifier(
        "https://cellxgene.cziscience.com", "cellxgene"
    )
    assert "https://api.dandiarchive.org/api/dandisets/" in [
        item["url"] for item in dandi
    ]
    assert "https://api.cellxgene.cziscience.com/curation/v1/datasets" in [
        item["url"] for item in cellxgene
    ]


def test_deegree_webservices_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/deegree-webservices/services?service=CSW&version=2.0.2&request=GetCapabilities": _xml_ok(
                b"<csw:Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://gis.example.si/deegree-webservices/", "deegree"
    )
    urls = [item["url"] for item in found]
    assert (
        "https://gis.example.si/deegree-webservices/services?service=CSW&version=2.0.2&request=GetCapabilities"
        in urls
    )
    assert not any("/deegree-webservices/deegree-webservices/" in item["url"] for item in found)


def test_deegree_url_cleanup_keeps_geoproxy_prefix():
    assert (
        apidetect.deegree_url_cleanup_func(
            "https://geoproxy.example.de/geoproxy/deegree-webservices/"
        )
        == "https://geoproxy.example.de/geoproxy"
    )
    assert (
        apidetect.deegree_url_cleanup_func("https://m4eu.example.pt/m4eu/")
        == "https://m4eu.example.pt/m4eu"
    )


def test_flat_flat_link_does_not_double(monkeypatch):
    session = _SelectiveSession(
        {
            "/flat/oai2?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://archive.example.se/flat/", "flat"
    )
    urls = [item["url"] for item in found]
    assert "https://archive.example.se/flat/oai2?verb=Identify" in urls
    assert not any("/flat/flat/" in item["url"] for item in found)


def test_omero_projects_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v0/m/projects/": _json_ok(b'{"data":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://idr.example.org", "omero")
    assert any(item["type"] == "omero:projects" for item in found)
    assert any(
        item["url"] == "https://idr.example.org/api/v0/m/projects/" for item in found
    )


def test_omero_webclient_fallback(monkeypatch):
    session = _SelectiveSession(
        {
            "/webclient/": _DummyResponse(
                content=b"<html><title>OMERO.web</title></html>",
                headers={"Content-Type": "text/html"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://omero.example.org", "omero")
    assert any(item["type"] == "omero:webclient" for item in found)
    assert any(
        item["url"] == "https://omero.example.org/webclient/" for item in found
    )


def test_kadi4mat_records_type(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/records": _json_ok(b'{"items":[]}'),
            "/api/collections": _json_ok(b'{"items":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://kadi.example.org", "kadi4mat")
    types = {item["type"] for item in found}
    urls = {item["url"] for item in found}
    assert "kadi4mat:records" in types
    assert "kadi4mat:collections" in types
    assert "https://kadi.example.org/api/records" in urls
    assert "https://kadi.example.org/api/collections" in urls


def test_mytardis_dataset_list(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v1/dataset/": _json_ok(b'{"objects":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://store.example.edu.au", "mytardis")
    assert any(item["type"] == "mytardis:datasets" for item in found)
    assert any(
        item["url"] == "https://store.example.edu.au/api/v1/dataset/" for item in found
    )


def test_haleconnect_ows_wms(monkeypatch):
    session = _SelectiveSession(
        {
            "/ows/services/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities": _xml_ok(
                b"<WMS_Capabilities/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://haleconnect.example.de", "haleconnect")
    assert any(item["type"] == "wms130" for item in found)
    assert any(
        item["url"].endswith(
            "/ows/services/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities"
        )
        for item in found
    )


def test_haleconnect_csw_oaipmh_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/csw?mode=oaipmh&verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://haleconnect.example.de", "haleconnect")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"]
        == "https://haleconnect.example.de/csw?mode=oaipmh&verb=Identify"
        for item in found
    )


def test_entryscape_dataset_search(monkeypatch):
    session = _SelectiveSession(
        {
            "/store/search?type=dcat:Dataset": _json_ok(b'{"resourceCount":0}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://catalog.example.se", "entryscape")
    assert any(item["type"] == "entrystore:search" for item in found)
    assert any(
        item["url"] == "https://catalog.example.se/store/search?type=dcat:Dataset"
        for item in found
    )


def test_piveau_hub_search_harvest_path(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/hub/search/search": _html_404(),
            "/api/hub/search": _json_ok(b'{"result":{"count":0,"results":[]}}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.eu", "piveau")
    assert any(
        item["url"] == "https://data.example.eu/api/hub/search" for item in found
    )


def test_piveau_api_sparql(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/sparql": _xml_ok(b"<sparql xmlns='http://www.w3.org/2005/sparql-results#'/>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.eu", "piveau")
    assert any(item["type"] == "sparql" for item in found)
    assert any(
        item["url"] == "https://data.example.eu/api/sparql" for item in found
    )


def test_geoblacklight_catalog_opensearch(monkeypatch):
    session = _SelectiveSession(
        {
            "/catalog/opensearch.xml": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://geo.example.edu", "geoblacklight")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://geo.example.edu/catalog/opensearch.xml"
        for item in found
    )


def test_triplydb_opensearch_xml(monkeypatch):
    session = _SelectiveSession(
        {
            "/opensearch.xml": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.cc", "triplydb")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://data.example.cc/opensearch.xml" for item in found
    )


def test_socrata_opensearch_xml(monkeypatch):
    session = _SelectiveSession(
        {
            "/opensearch.xml": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.gov", "socrata")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://data.example.gov/opensearch.xml" for item in found
    )


def test_geonode_catalogue_opensearch(monkeypatch):
    session = _SelectiveSession(
        {
            "/catalogue/opensearch": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://geo.example.org", "geonode")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://geo.example.org/catalogue/opensearch" for item in found
    )


def test_geonode_api_v2_datasets(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v2/datasets/": _json_ok(b'{"total":0,"datasets":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://geo.example.org", "geonode")
    assert any(item["type"] == "geonode:datasets" for item in found)
    assert any(
        item["url"] == "https://geo.example.org/api/v2/datasets/" for item in found
    )


def test_arcgishub_data_json(monkeypatch):
    session = _SelectiveSession(
        {
            "/data.json": _json_ok(b'{"dataset":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://opendata.example.gov", "arcgishub")
    assert any(item["type"] == "dcatus11" for item in found)
    assert any(
        item["url"] == "https://opendata.example.gov/data.json" for item in found
    )


def test_supermapiportal_maps_json_not_doubled(monkeypatch):
    session = _SelectiveSession(
        {
            "/iportal/web/maps.json": _json_ok(b"[]"),
            "/iportal/web/datas.json": _json_ok(b"[]"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://nsdi.example.gov/iportal", "supermapiportal")
    assert any(item["type"] == "supermapiportal:maps" for item in found)
    assert any(
        item["url"] == "https://nsdi.example.gov/iportal/web/maps.json" for item in found
    )
    assert any(item["type"] == "supermapiportal:datas" for item in found)
    assert not any("/iportal/iportal/" in item["url"] for item in found)


def test_dlibra_oai_identify_not_doubled(monkeypatch):
    session = _SelectiveSession(
        {
            "/dlibra/oai-pmh-repository.xml?verb=Identify": _xml_ok(
                b"<OAI-PMH><Identify/></OAI-PMH>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://kpbc.example.pl/dlibra", "dlibra")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert any(
        item["url"]
        == "https://kpbc.example.pl/dlibra/oai-pmh-repository.xml?verb=Identify"
        for item in found
    )
    assert not any("/dlibra/dlibra/" in item["url"] for item in found)


def test_gipuzkoairekia_subdomain_origin_dumps(monkeypatch):
    rdf = _DummyResponse(
        content=b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'/>",
        headers={"Content-Type": "application/rdf+xml"},
    )
    session = _SelectiveSession(
        {
            "/catalog.xml": rdf,
            "/catalog.jsonld": _json_ok(b'{"@graph":[]}'),
            "/api/feed/dcat": rdf,
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "http://eibar.gipuzkoairekia.eus/es/datu-irekien-katalogoa",
        "gipuzkoairekia",
    )
    urls = {item["url"] for item in found}
    assert "http://eibar.gipuzkoairekia.eus/catalog.xml" in urls
    assert "http://eibar.gipuzkoairekia.eus/catalog.jsonld" in urls
    assert "http://eibar.gipuzkoairekia.eus/api/feed/dcat" in urls
    assert not any("/es/datu-irekien-katalogoa/catalog" in url for url in urls)


def test_gipuzkoairekia_www_tenant_keeps_path(monkeypatch):
    session = _SelectiveSession(
        {
            "/catalogo.rdf": _DummyResponse(
                content=b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'/>",
                headers={"Content-Type": "application/rdf+xml"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://www.gipuzkoairekia.eus/es/web/hernani/datu-irekien-katalogoa",
        "gipuzkoairekia",
    )
    urls = {item["url"] for item in found}
    assert (
        "https://www.gipuzkoairekia.eus/es/web/hernani/datu-irekien-katalogoa/catalogo.rdf"
        in urls
    )
    assert "https://www.gipuzkoairekia.eus/catalogo.rdf" not in urls


def test_opendatasoft_data_json(monkeypatch):
    session = _SelectiveSession(
        {
            "/data.json": _json_ok(b'{"dataset":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.com", "opendatasoft")
    assert any(item["type"] == "dcatus11" for item in found)
    assert any(item["url"] == "https://data.example.com/data.json" for item in found)


def test_esrigeo_opensearch_description_not_doubled(monkeypatch):
    session = _SelectiveSession(
        {
            "/geoportal/openSearchDescription": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://gis.example.at/geoportal", "esrigeo")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://gis.example.at/geoportal/openSearchDescription"
        for item in found
    )
    assert not any("/geoportal/geoportal/" in item["url"] for item in found)


def test_esrigeo_search_mount_opensearch_description(monkeypatch):
    session = _SelectiveSession(
        {
            "/search/openSearchDescription": _xml_ok(
                b"<OpenSearchDescription xmlns='http://a9.com/-/spec/opensearch/1.1/'/>"
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://www.coris.noaa.gov/search", "esrigeo")
    assert any(item["type"] == "opensearch" for item in found)
    assert any(
        item["url"] == "https://www.coris.noaa.gov/search/openSearchDescription"
        for item in found
    )


def test_elsevierdigitalcommons_oai_root_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://digitalcommonsdata.example.edu", "elsevierdigitalcommons"
    )
    assert any(item["type"] == "oaipmh20" for item in found)
    assert "https://digitalcommonsdata.example.edu/oai?verb=Identify" in {
        item["url"] for item in found
    }


def test_librecat_oai_identify_origin_from_search_mount(monkeypatch):
    session = _SelectiveSession(
        {
            "/search/oai": _html_404(),
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://lup.example.edu/search/", "librecat")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert "https://lup.example.edu/oai?verb=Identify" in {
        item["url"] for item in found
    }
    assert not any("/search/oai" in item["url"] for item in found)


def test_pycsw_mode_oaipmh_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/?mode=oaipmh&verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://catalogue.example.eu", "pycsw")
    assert any(item["type"] == "oaipmh20" for item in found)
    assert "https://catalogue.example.eu/?mode=oaipmh&verb=Identify" in {
        item["url"] for item in found
    }


def test_dkan_jsonapi_dataset_entity(monkeypatch):
    session = _SelectiveSession(
        {
            "/jsonapi/dataset/dataset": _DummyResponse(
                content=b'{"data":[]}',
                headers={"Content-Type": "application/vnd.api+json"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://fiji-data.example.org", "dkan")
    assert any(item["type"] == "drupal:jsonapi" for item in found)
    assert any(
        item["url"] == "https://fiji-data.example.org/jsonapi/dataset/dataset"
        for item in found
    )


def test_pygeoapi_collections_without_trailing_slash(monkeypatch):
    session = _SelectiveSession(
        {
            "/collections/?f=json": _html_404(),
            "/collections?f=json": _json_ok(b'{"collections":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://ogcapi.example.org", "pygeoapi")
    assert any(item["type"] == "ogc:features" for item in found)
    assert any(
        item["url"] == "https://ogcapi.example.org/collections?f=json" for item in found
    )
    assert not any("/collections/?f=json" in item["url"] for item in found)


def test_datapress_ckan_package_search(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/3/action/package_search": _json_ok(b'{"success":true,"result":{}}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://data.example.org", "datapress")
    assert any(item["type"] == "ckan:package-search" for item in found)
    assert any(
        item["url"] == "https://data.example.org/api/3/action/package_search"
        for item in found
    )


def test_vufind_openapi_on_vufind_mount(monkeypatch):
    session = _SelectiveSession(
        {
            "/api?openapi": _json_ok(b'{"openapi":"3.0.0"}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://silo.example.edu/vufind", "vufind")
    assert any(item["type"] == "openapi" for item in found)
    assert "https://silo.example.edu/vufind/api?openapi" in {
        item["url"] for item in found
    }
    assert not any("/vufind/vufind/" in item["url"] for item in found)


def test_phaidra_openapi_root(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/openapi/json": _html_404(),
            "/api/openapi": _json_ok(b'{"openapi":"3.0.0"}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://phaidra.example.ac.at", "phaidra")
    assert any(item["type"] == "openapi" for item in found)
    assert "https://phaidra.example.ac.at/api/openapi" in {item["url"] for item in found}


def test_omekas_dataset_class_filter(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/items?resource_class_label=Dataset": _json_ok(b"[]"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://omeka.example.org", "omekas")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"]
        == "https://omeka.example.org/api/items?resource_class_label=Dataset"
        for item in found
    )


def test_nomad_entries_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/prod/v1/api/v1/entries": _json_ok(b'{"pagination":{"total":0}}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://nomad-lab.eu", "nomad")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://nomad-lab.eu/prod/v1/api/v1/entries" for item in found
    )


def test_linkahead_api_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/api/v1/": _json_ok(b'{"Entity":"Record"}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://samples.example.de", "linkahead")
    assert any(item["type"] == "rest" for item in found)
    assert any(item["url"] == "https://samples.example.de/api/v1/" for item in found)


def test_hydroshare_hsapi_rest(monkeypatch):
    session = _SelectiveSession(
        {
            "/hsapi/resource/": _json_ok(b'{"results":[]}'),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier("https://www.hydroshare.org", "hydroshare")
    assert any(item["type"] == "rest" for item in found)
    assert any(
        item["url"] == "https://www.hydroshare.org/hsapi/resource/" for item in found
    )


def test_elsevierdigitalcommons_oai_identify(monkeypatch):
    session = _SelectiveSession(
        {
            "/do/oai/?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://digitalcommons.example.edu", "elsevierdigitalcommons"
    )
    assert any(item["type"] == "oaipmh20" for item in found)
    assert (
        "https://digitalcommons.example.edu/do/oai/?verb=Identify"
        in {item["url"] for item in found}
    )


def test_hdc_is_skipped_not_mapped():
    from apidetect_urlmaps_draft import NO_STANDARD_PROBE

    assert "hdc" in NO_STANDARD_PROBE
    assert "hdc" not in apidetect.CATALOGS_URLMAP


def test_parallel_probes_preserve_map_order(monkeypatch):
    session = _SelectiveSession(
        {
            "/oai?verb=Identify": _xml_ok(b"<OAI-PMH><Identify/></OAI-PMH>"),
            "/catalog.rdf": _DummyResponse(
                content=b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'/>",
                headers={"Content-Type": "application/rdf+xml"},
            ),
        }
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: session)
    found = apidetect.api_identifier(
        "https://data.example.org", "ckan", probe_workers=8
    )
    types = [item["type"] for item in found]
    assert "dcat" in types
    assert "oaipmh20" in types
    assert types.index("dcat") < types.index("oaipmh20")


def test_yaml_id_glob_paths_skips_urls_and_parent(tmp_path):
    yaml_path = tmp_path / "catalogdatagov.yaml"
    yaml_path.write_text("id: catalogdatagov\n", encoding="utf8")
    nested = tmp_path / "US" / "opendata"
    nested.mkdir(parents=True)
    (nested / "example.yaml").write_text("id: example\n", encoding="utf8")

    assert apidetect._yaml_id_glob_paths(str(tmp_path), "example") == [
        str(nested / "example.yaml")
    ]
    assert apidetect._yaml_id_glob_paths(str(tmp_path), "https://example.org") is None
    assert apidetect._yaml_id_glob_paths(str(tmp_path), "../secret") is None
    assert apidetect._yaml_id_glob_paths(str(tmp_path), "missing") is None


def test_run_record_jobs_parallel_invokes_each_job():
    seen = []

    def _runner(job):
        seen.append(job)

    apidetect._run_record_jobs(["a", "b", "c"], _runner, record_workers=4)
    assert sorted(seen) == ["a", "b", "c"]


def test_invalid_redirect_port_does_not_abort_probes(monkeypatch):
    class _BoomSession:
        def get(self, *args, **kwargs):
            raise apidetect.requests.exceptions.InvalidURL(
                "Port could not be cast to integer value as 'null'"
            )

        def post(self, *args, **kwargs):
            raise apidetect.requests.exceptions.InvalidURL("bad")

    monkeypatch.setitem(
        apidetect.CATALOGS_URLMAP,
        "testsw",
        [
            {
                "id": "probe",
                "url": "/probe",
                "expected_mime": ["application/json"],
                "version": None,
            }
        ],
    )
    monkeypatch.setattr(apidetect.requests, "Session", lambda: _BoomSession())
    found = apidetect.api_identifier(
        "https://example.org", "testsw", probe_workers=4
    )
    assert found == []

