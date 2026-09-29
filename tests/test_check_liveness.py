import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from check_liveness import apply_dead_from_report, classify_liveness, probe_url


class _FakeResponse:
    def __init__(self, status_code: int, url: str):
        self.status_code = status_code
        self.url = url


class _FakeSession:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def request(self, method, url, timeout=None, allow_redirects=None):
        self.calls.append((method, url))
        if not self._responses:
            raise RuntimeError("no fake responses left")
        action = self._responses.pop(0)
        if isinstance(action, Exception):
            raise action
        return action


def test_classify_live():
    assert classify_liveness(200) == "live"


def test_classify_redirect():
    assert classify_liveness(301) == "redirect"


def test_classify_inconclusive_for_403():
    assert classify_liveness(403) == "inconclusive"


def test_classify_dead_for_timeout():
    assert classify_liveness(None, "timeout: read timed out") == "dead"


def test_classify_dead_for_404():
    assert classify_liveness(404) == "dead"


def test_probe_url_head_success():
    session = _FakeSession([_FakeResponse(200, "https://example.gov")])
    code, error, final_url = probe_url("https://example.gov", session)
    assert code == 200
    assert error is None
    assert final_url == "https://example.gov"
    assert session.calls[0][0] == "HEAD"


def test_probe_url_head_404_falls_back_to_get():
    session = _FakeSession(
        [
            _FakeResponse(404, "https://app.example.cz/city"),
            _FakeResponse(200, "https://app.example.cz/city"),
        ]
    )
    code, error, final_url = probe_url("https://app.example.cz/city", session)
    assert code == 200
    assert error is None
    assert final_url == "https://app.example.cz/city"
    assert [call[0] for call in session.calls] == ["HEAD", "GET"]


def test_probe_url_get_fallback():
    import requests

    session = _FakeSession(
        [
            requests.exceptions.RequestException("405 Method Not Allowed"),
            _FakeResponse(200, "https://example.gov"),
        ]
    )
    code, error, final_url = probe_url("https://example.gov", session)
    assert code == 200
    assert error is None
    assert [call[0] for call in session.calls] == ["HEAD", "GET"]


def test_probe_url_retries_on_503():
    session = _FakeSession(
        [
            _FakeResponse(503, "https://example.gov"),
            _FakeResponse(503, "https://example.gov"),
            _FakeResponse(200, "https://example.gov"),
        ]
    )
    code, error, final_url = probe_url("https://example.gov", session, retries=2)
    assert code == 200
    assert error is None


def test_apply_dead_dry_run_does_not_write(tmp_path):
    entities = tmp_path / "entities" / "XX" / "opendata"
    entities.mkdir(parents=True)
    yaml_path = entities / "examplegov.yaml"
    yaml_path.write_text(
        "id: examplegov\nuid: cdi00009999\nstatus: active\napi: true\napi_status: active\nlink: https://example.gov\n",
        encoding="utf-8",
    )
    report = tmp_path / "liveness_report.jsonl"
    report.write_text(
        '{"uid": "cdi00009999", "link": "https://example.gov", "liveness_status": "dead", "http_code": 404, "checked_at": "2026-09-16T00:00:00Z"}\n'
        '{"uid": "cdi00009999", "link": "https://example.gov", "liveness_status": "inconclusive", "http_code": 403, "checked_at": "2026-09-16T00:00:00Z"}\n',
        encoding="utf-8",
    )
    applied = apply_dead_from_report(report, tmp_path / "entities", dry_run=True)
    assert any(item["action"] == "would_inactivate" for item in applied)
    assert "status: active" in yaml_path.read_text(encoding="utf-8")

    applied = apply_dead_from_report(report, tmp_path / "entities", dry_run=False)
    text = yaml_path.read_text(encoding="utf-8")
    assert any(item["action"] == "inactivated" for item in applied)
    assert "status: inactive" in text
    assert "api: false" in text
