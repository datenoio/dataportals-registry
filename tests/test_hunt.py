"""Tests for scripts/hunt.py — the discovery hunt toolkit."""

import base64
import json
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import hunt  # noqa: E402

runner = CliRunner()


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class FakeResponse:
    """Minimal requests.Response stand-in."""

    def __init__(
        self,
        status_code=200,
        content=b"",
        url="http://example.com/",
        headers=None,
        encoding=None,
        apparent_encoding=None,
        json_data=None,
    ):
        self.status_code = status_code
        self.content = content
        self.url = url
        self.headers = headers or {}
        self.encoding = encoding
        self.apparent_encoding = apparent_encoding
        self._json_data = json_data
        self.text_content = None

    @property
    def text(self):
        enc = self.encoding or "utf-8"
        return self.content.decode(enc, errors="replace")

    def json(self):
        return self._json_data


class FakeSession:
    """Scriptable session: responses are consumed in call order."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.headers = {}

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------


class TestSearchFofa:
    def test_missing_credentials(self, monkeypatch):
        monkeypatch.delenv("FOFA_EMAIL", raising=False)
        monkeypatch.delenv("FOFA_KEY", raising=False)
        result = runner.invoke(hunt.app, ["search", "fofa", 'title="CKAN"'])
        assert result.exit_code == 1
        assert "FOFA_EMAIL" in result.output

    def test_success_normalizes_rows(self, monkeypatch, tmp_path):
        monkeypatch.setenv("FOFA_EMAIL", "a@b.c")
        monkeypatch.setenv("FOFA_KEY", "secret")
        payload = {
            "error": False,
            "size": 2,
            "results": [
                ["https://data.example.cn", "1.2.3.4", "443", "https", "数据开放平台", "example.cn"],
                ["geo.example.cn:8080", "1.2.3.5", "8080", "http", "Geo", "example.cn"],
            ],
        }
        session = FakeSession([FakeResponse(json_data=payload)])
        out = tmp_path / "candidates.jsonl"
        results = hunt._fofa_search(session, 'title="数据开放"', size=100, max_pages=1, max_retries=0)
        assert len(results) == 2
        assert results[0]["url"] == "https://data.example.cn"
        assert results[0]["host"] == "data.example.cn"
        assert results[0]["title"] == "数据开放平台"
        assert results[0]["source"] == "fofa"
        # host without scheme uses the protocol field
        assert results[1]["url"] == "http://geo.example.cn:8080"
        # query was base64-encoded in the request params
        params = session.calls[0][2]["params"]
        assert base64.b64decode(params["qbase64"]).decode() == 'title="数据开放"'
        _ = out

    def test_api_error_raises(self, monkeypatch):
        monkeypatch.setenv("FOFA_EMAIL", "a@b.c")
        monkeypatch.setenv("FOFA_KEY", "secret")
        payload = {"error": True, "errmsg": "bad query syntax"}
        session = FakeSession([FakeResponse(json_data=payload)])
        with pytest.raises(ValueError, match="FOFA error"):
            hunt._fofa_search(session, "bogus", size=100, max_pages=1, max_retries=0)

    def test_backoff_on_429(self, monkeypatch):
        monkeypatch.setenv("FOFA_EMAIL", "a@b.c")
        monkeypatch.setenv("FOFA_KEY", "secret")
        sleeps = []
        monkeypatch.setattr(hunt.time, "sleep", lambda s: sleeps.append(s))
        ok = FakeResponse(json_data={"error": False, "results": []})
        session = FakeSession([FakeResponse(status_code=429), ok])
        hunt._fofa_search(session, "q", size=100, max_pages=1, max_retries=3)
        assert len(sleeps) == 1
        assert len(session.calls) == 2


class TestSearchCensys:
    def test_missing_token(self, monkeypatch):
        monkeypatch.delenv("CENSYS_API_TOKEN", raising=False)
        monkeypatch.delenv("CENSYS_PAT", raising=False)
        result = runner.invoke(hunt.app, ["search", "censys", "web.endpoints.http.html_title: X"])
        assert result.exit_code == 1
        assert "CENSYS_API_TOKEN" in result.output

    def test_pagination_with_cursor(self, monkeypatch):
        monkeypatch.setenv("CENSYS_API_TOKEN", "tok")
        monkeypatch.delenv("CENSYS_ORGANIZATION_ID", raising=False)
        monkeypatch.delenv("CENSYS_ORG_ID", raising=False)
        page1 = {
            "result": {
                "hits": [{"web": {"endpoints": {"http": {"host": "a.example", "html_title": "A"}}}}],
                "next": "cursor-2",
            }
        }
        page2 = {
            "result": {
                "hits": [{"web": {"endpoints": {"http": {"host": "b.example"}}}}],
            }
        }
        session = FakeSession([FakeResponse(json_data=page1), FakeResponse(json_data=page2)])
        results = hunt._censys_search(session, "q", size=100, max_pages=5, max_retries=0)
        assert [r["host"] for r in results] == ["a.example", "b.example"]
        assert results[0]["title"] == "A"
        # second request carried the cursor
        body2 = json.loads(session.calls[1][2]["data"])
        assert body2["cursor"] == "cursor-2"
        # auth header present
        headers = session.calls[0][2]["headers"]
        assert headers["Authorization"] == "Bearer tok"

    def test_http_error_raises(self, monkeypatch):
        monkeypatch.setenv("CENSYS_API_TOKEN", "tok")
        session = FakeSession([FakeResponse(status_code=403, content=b"forbidden")])
        with pytest.raises(ValueError, match="Censys HTTP 403"):
            hunt._censys_search(session, "q", size=100, max_pages=1, max_retries=0)


# ---------------------------------------------------------------------------
# dedupe
# ---------------------------------------------------------------------------


class TestDedupeRows:
    INDEXES = (
        {"datagov", "geoportalx"},  # ids
        {"https://catalog.data.gov": "datagov"},  # canonical urls
        {"geo.example.org": "geoportalx"},  # hosts
    )

    def test_canonical_url_match(self):
        rows = [{"url": "https://catalog.data.gov/", "host": "catalog.data.gov"}]
        out = hunt.dedupe_rows(rows, *self.INDEXES)
        assert out[0]["exists"] is True
        assert out[0]["existing_id"] == "datagov"

    def test_id_match(self):
        rows = [{"url": "https://data.gov", "host": "data.gov", "id": "datagov"}]
        out = hunt.dedupe_rows(rows, *self.INDEXES)
        assert out[0]["exists"] is True

    def test_host_match_only_for_root_urls(self):
        root = [{"url": "https://geo.example.org", "host": "geo.example.org"}]
        deep = [{"url": "https://geo.example.org/maps/roads", "host": "geo.example.org"}]
        assert hunt.dedupe_rows(root, *self.INDEXES)[0]["exists"] is True
        assert hunt.dedupe_rows(deep, *self.INDEXES)[0]["exists"] is False

    def test_new_candidate(self):
        rows = [{"url": "https://newdata.example.gov", "host": "newdata.example.gov"}]
        out = hunt.dedupe_rows(rows, *self.INDEXES)
        assert out[0]["exists"] is False
        assert "existing_id" not in out[0]

    def test_cli(self, tmp_path, monkeypatch):
        monkeypatch.setattr(hunt, "_build_export_indexes", lambda: self.INDEXES)
        candidates = tmp_path / "candidates.jsonl"
        candidates.write_text(
            json.dumps({"url": "https://catalog.data.gov", "host": "catalog.data.gov"})
            + "\n"
            + json.dumps({"url": "https://new.example.gov", "host": "new.example.gov"})
            + "\n"
        )
        result = runner.invoke(hunt.app, ["dedupe", str(candidates)])
        assert result.exit_code == 0
        out = tmp_path / "candidates.deduped.jsonl"
        rows = [json.loads(line) for line in out.read_text().splitlines()]
        assert rows[0]["exists"] is True
        assert rows[1]["exists"] is False
        assert "1 already registered" in result.output


# ---------------------------------------------------------------------------
# probe
# ---------------------------------------------------------------------------


class TestProbe:
    CKAN_FP = {"ckan": {"id": "ckan", "url": "/api/3", "expected_mime": ["application/json"]}}

    def test_gbk_title_decoded(self):
        content = "<html><head><title>数据开放平台</title></head></html>".encode("gbk")
        session = FakeSession(
            [FakeResponse(content=content, headers={"Content-Type": "text/html"}, apparent_encoding="gbk")]
        )
        row = hunt._probe_one({"url": "http://data.example.cn"}, session, 5.0, {})
        assert row["liveness"] == "live"
        assert row["title"] == "数据开放平台"
        assert row["http_code"] == 200

    def test_timeout_is_dead(self):
        import requests as real_requests

        session = FakeSession([real_requests.exceptions.Timeout("boom")])
        row = hunt._probe_one({"url": "http://slow.example"}, session, 5.0, {})
        assert row["liveness"] == "dead"
        assert "timeout" in row["error"]

    def test_403_inconclusive_and_flagged(self):
        session = FakeSession([FakeResponse(status_code=403)])
        row = hunt._probe_one({"url": "http://blocked.example"}, session, 5.0, {})
        assert row["liveness"] == "inconclusive"
        assert row["auth_required"] is True

    def test_fingerprint_match(self):
        html_resp = FakeResponse(content=b"<title>Open Data</title>")
        api_resp = FakeResponse(
            content=b'{"success": true}',
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        session = FakeSession([html_resp, api_resp])
        row = hunt._probe_one({"url": "http://ckan.example"}, session, 5.0, self.CKAN_FP)
        assert row["software_id"] == "ckan"
        assert row["fingerprint_url"] == "http://ckan.example/api/3"

    def test_fingerprint_mime_mismatch(self):
        html_resp = FakeResponse(content=b"<title>Portal</title>")
        not_json = FakeResponse(
            content=b"<html>not found</html>", headers={"Content-Type": "text/html"}
        )
        session = FakeSession([html_resp, not_json])
        row = hunt._probe_one({"url": "http://plain.example"}, session, 5.0, self.CKAN_FP)
        assert "software_id" not in row

    def test_probe_rows_groups_by_host(self, monkeypatch):
        monkeypatch.setattr(hunt.time, "sleep", lambda s: None)
        monkeypatch.setattr(
            hunt.requests, "Session", lambda: FakeSession([FakeResponse()] * 3)
        )
        candidates = [
            {"url": "http://a.example/1", "host": "a.example"},
            {"url": "http://a.example/2", "host": "a.example"},
            {"url": "http://b.example", "host": "b.example"},
        ]
        results = hunt.probe_rows(candidates, concurrency=2, delay=0.0)
        assert len(results) == 3
        assert all(r["liveness"] == "live" for r in results)

    def test_cli_skips_existing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(hunt.time, "sleep", lambda s: None)
        monkeypatch.setattr(hunt.requests, "Session", lambda: FakeSession([FakeResponse()]))
        candidates = tmp_path / "candidates.jsonl"
        candidates.write_text(
            json.dumps({"url": "http://old.example", "host": "old.example", "exists": True})
            + "\n"
            + json.dumps({"url": "http://new.example", "host": "new.example"})
            + "\n"
        )
        result = runner.invoke(hunt.app, ["probe", str(candidates)])
        assert result.exit_code == 0
        rows = [json.loads(line) for line in (tmp_path / "candidates.probed.jsonl").read_text().splitlines()]
        assert len(rows) == 1
        assert rows[0]["host"] == "new.example"
        assert "1 live" in result.output


# ---------------------------------------------------------------------------
# log
# ---------------------------------------------------------------------------


class TestLog:
    def test_append_valid_row(self, tmp_path):
        log_path = tmp_path / "hunts.jsonl"
        row = hunt.append_hunt_log(
            kind="software-instance",
            target="hslayers",
            added=5,
            skipped_dupes=2,
            status="partial",
            notes="test hunt",
            date="2026-09-17",
            path=log_path,
        )
        assert row["added"] == 5
        loaded = json.loads(log_path.read_text().strip())
        assert loaded["kind"] == "software-instance"
        assert loaded["list_url"] is None

    def test_unknown_kind_rejected(self, tmp_path):
        with pytest.raises(ValueError, match="Unknown hunt kind"):
            hunt.append_hunt_log(kind="random-thing", target="x", added=1, path=tmp_path / "h.jsonl")

    def test_unknown_status_rejected(self, tmp_path):
        with pytest.raises(ValueError, match="Unknown status"):
            hunt.append_hunt_log(
                kind="analysis", target="x", added=0, status="done", path=tmp_path / "h.jsonl"
            )

    def test_bad_date_rejected(self, tmp_path):
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            hunt.append_hunt_log(
                kind="analysis", target="x", added=0, date="17/09/2026", path=tmp_path / "h.jsonl"
            )

    def test_negative_added_rejected(self, tmp_path):
        with pytest.raises(ValueError, match=">= 0"):
            hunt.append_hunt_log(kind="analysis", target="x", added=-1, path=tmp_path / "h.jsonl")

    def test_cli(self, tmp_path, monkeypatch):
        log_path = tmp_path / "hunts.jsonl"
        monkeypatch.setattr(hunt, "HUNTS_LOG", log_path)
        result = runner.invoke(
            hunt.app,
            ["log", "--kind", "country-indicators", "--target", "AU", "--added", "3"],
        )
        assert result.exit_code == 0
        row = json.loads(log_path.read_text().strip())
        assert row["target"] == "AU"
        assert row["status"] == "complete"
