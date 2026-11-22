"""Unit tests for the shared helpers in scripts/dpr/."""

import json

import pytest

from dpr.jsonl import load_csv_dict, load_jsonl
from dpr.re3data import get_re3data_identifier
from dpr.software import load_software_definitions
from dpr.urls import normalize_domain, normalize_url


@pytest.mark.unit
def test_load_jsonl_reads_each_line(tmp_path):
    path = tmp_path / "records.jsonl"
    path.write_text('{"id": "a"}\n{"id": "b", "n": 1}\n', encoding="utf-8")
    assert load_jsonl(path) == [{"id": "a"}, {"id": "b", "n": 1}]


@pytest.mark.unit
def test_load_csv_dict_keys_rows_and_defaults_to_tabs(tmp_path):
    path = tmp_path / "langs.tsv"
    path.write_text("code\tname\nEN\tEnglish\nFR\tFrench\n", encoding="utf-8")
    rows = load_csv_dict(path, key="code")
    assert rows["FR"] == {"code": "FR", "name": "French"}
    assert sorted(rows) == ["EN", "FR"]


@pytest.mark.unit
def test_load_csv_dict_accepts_other_delimiters(tmp_path):
    path = tmp_path / "langs.csv"
    path.write_text("code,name\nEN,English\n", encoding="utf-8")
    assert load_csv_dict(path, key="code", delimiter=",")["EN"]["name"] == "English"


@pytest.mark.unit
@pytest.mark.parametrize(
    "url, expected",
    [
        ("HTTPS://WWW.Example.org/Data/", "example.org/data"),
        ("http://example.org", "example.org"),
        ("  example.org//  ", "example.org"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize_url(url, expected):
    assert normalize_url(url) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.example.org:8443/ckan/", "example.org"),
        ("http://data.gov.uk/dataset", "data.gov.uk"),
        ("", ""),
    ],
)
def test_normalize_domain(url, expected):
    assert normalize_domain(url) == expected


@pytest.mark.unit
def test_get_re3data_identifier():
    record = {"identifiers": [{"id": "wikidata", "value": "Q1"}, {"id": "re3data", "value": "r3d100010468"}]}
    assert get_re3data_identifier(record) == "r3d100010468"
    assert get_re3data_identifier({"identifiers": [{"id": "wikidata", "value": "Q1"}]}) is None
    assert get_re3data_identifier({}) is None


@pytest.mark.unit
def test_load_software_definitions_skips_unreadable_files(tmp_path, caplog):
    (tmp_path / "opendata").mkdir()
    (tmp_path / "opendata" / "ckan.yaml").write_text("id: ckan\nname: CKAN\ntype: Software\n", encoding="utf-8")
    (tmp_path / "broken.yaml").write_text("id: [unclosed\n", encoding="utf-8")
    (tmp_path / "noid.yaml").write_text("name: No id\n", encoding="utf-8")

    software = load_software_definitions(tmp_path)

    assert software == {"ckan": {"id": "ckan", "name": "CKAN"}}
    assert "broken.yaml" in caplog.text


@pytest.mark.unit
def test_load_software_definitions_reads_the_registry():
    software = load_software_definitions()
    assert software["ckan"]["name"] == "CKAN"
    assert len(software) > 700
    assert json.dumps(software)  # plain data, serializable


@pytest.mark.unit
def test_read_jsonl_issues_keeps_records_with_issues(tmp_path, caplog):
    from dpr.reports import read_jsonl_issues

    path = tmp_path / "primary_priority.jsonl"
    path.write_text(
        '{"id": "a", "issues": [{"issue_type": "MISSING_TAGS"}]}\n'
        "\n"
        "not json\n"
        '{"id": "b", "issues": []}\n',
        encoding="utf-8",
    )
    assert [r["id"] for r in read_jsonl_issues(path)] == ["a"]
    assert "line 3" in caplog.text
    assert read_jsonl_issues(tmp_path / "missing.jsonl") == []


@pytest.mark.unit
def test_iter_yaml_files_is_sorted_and_recursive(tmp_path):
    from dpr.yaml_io import iter_yaml_files

    for rel in ["b/z.yaml", "a/y.yaml", "a/x.yaml", "a/notes.txt", "c.yaml"]:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("id: x\n", encoding="utf-8")
    found = [p.replace(str(tmp_path) + "/", "") for p in iter_yaml_files(tmp_path)]
    assert found == ["a/x.yaml", "a/y.yaml", "b/z.yaml", "c.yaml"]


@pytest.mark.unit
def test_re3data_url_and_collector(tmp_path):
    from dpr.re3data import collect_re3data_identifiers, get_re3data_url

    assert get_re3data_url("r3d100010468") == "https://www.re3data.org/repository/r3d100010468"
    (tmp_path / "US").mkdir()
    (tmp_path / "US" / "zenodo.yaml").write_text(
        "id: zenodo\nidentifiers:\n  - id: re3data\n    value: r3d100010468\n", encoding="utf-8"
    )
    (tmp_path / "US" / "plain.yaml").write_text("id: plain\n", encoding="utf-8")
    assert collect_re3data_identifiers(str(tmp_path)) == {"r3d100010468": str(tmp_path / "US" / "zenodo.yaml")}


@pytest.mark.unit
def test_fetch_re3data_page_sends_user_agent_and_handles_errors(monkeypatch):
    import requests

    from dpr import re3data

    calls = []

    class _Response:
        text = "<html>ok</html>"

        def raise_for_status(self):
            return None

    def _get(url, **kwargs):
        calls.append((url, kwargs))
        return _Response()

    monkeypatch.setattr(re3data.requests, "get", _get)
    assert re3data.fetch_re3data_page("r3d1") == "<html>ok</html>"
    assert "dataportals-registry" in calls[0][1]["headers"]["User-Agent"]
    assert calls[0][1]["verify"] is True

    def _fail(url, **kwargs):
        raise requests.exceptions.ConnectionError("down")

    monkeypatch.setattr(re3data.requests, "get", _fail)
    assert re3data.fetch_re3data_page("r3d1") is None
