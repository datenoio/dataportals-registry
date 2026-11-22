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
