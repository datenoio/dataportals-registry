"""Tests for extract_openaire_portals.py (OpenAIRE Graph harvest)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from extract_openaire_portals import (
    catalog_id_from_url,
    compact_source,
    infer_software,
    is_junk_url,
    match_source,
    normalize_host,
    normalize_http_url,
    publishes_datasets,
    select_sources,
)


class TestNormalizeHost:
    def test_strips_www_and_scheme(self):
        assert normalize_host("https://www.Example.com/path") == "example.com"

    def test_strips_port(self):
        assert normalize_host("https://data.example.edu:8080") == "data.example.edu"

    def test_empty(self):
        assert normalize_host("") == ""
        assert normalize_host(None) == ""


class TestNormalizeHttpUrl:
    def test_adds_https(self):
        assert normalize_http_url("data.example.org") == "https://data.example.org"

    def test_rejects_empty(self):
        assert normalize_http_url("") is None
        assert normalize_http_url("null") is None


class TestJunkUrl:
    def test_skips_placeholders(self):
        assert is_junk_url("http://test.de") is True
        assert is_junk_url("https://example.com/repo") is True
        assert is_junk_url("https://fairsharing.org/FAIRsharing.abc") is True

    def test_skips_forges(self):
        assert is_junk_url("https://github.com/DiscreteZOO") is True
        assert is_junk_url("https://docs.google.com/spreadsheets/d/abc") is True

    def test_skips_ip_literals(self):
        assert is_junk_url("http://150.216.56.64/index.php") is True

    def test_keeps_real_hosts(self):
        assert is_junk_url("https://opendata.cern.ch/") is False
        assert is_junk_url("https://org.github.io/data/") is False


class TestPublishesDatasets:
    def test_data_repository_always_kept(self):
        record = {
            "type": {"scheme": "datarepository::unknown", "value": "Data Repository"},
            "officialName": "Example Data Repo",
            "websiteUrl": "https://data.example.org",
        }
        keep, reason = publishes_datasets(record)
        assert keep is True
        assert reason == "data_repository_typology"

    def test_publication_only_ir_dropped(self):
        record = {
            "type": {
                "scheme": "pubsrepository::institutional",
                "value": "Institutional Repository",
            },
            "officialName": "University of Example Repository",
            "websiteUrl": "https://repo.example.edu",
            "collectedFrom": [{"value": "OpenDOAR"}],
            "contentTypes": ["Journal articles", "Theses and dissertations"],
        }
        keep, reason = publishes_datasets(record)
        assert keep is False
        assert reason == "publication_content_types"

    def test_ir_with_dataset_content_types_kept(self):
        record = {
            "type": {
                "scheme": "pubsrepository::institutional",
                "value": "Institutional Repository",
            },
            "officialName": "Campus IR",
            "websiteUrl": "https://ir.example.edu",
            "contentTypes": ["Journal articles", "Datasets"],
        }
        keep, reason = publishes_datasets(record)
        assert keep is True
        assert reason == "content_types"

    def test_ir_from_re3data_kept(self):
        record = {
            "type": {
                "scheme": "pubsrepository::institutional",
                "value": "Institutional Repository",
            },
            "officialName": "Campus IR",
            "websiteUrl": "https://ir.example.edu",
            "collectedFrom": [{"value": "Registry of Research Data Repository"}],
        }
        keep, reason = publishes_datasets(record)
        assert keep is True
        assert reason == "collected_from_data_registry"

    def test_dataverse_name_signal(self):
        record = {
            "type": {
                "scheme": "pubsrepository::institutional",
                "value": "Institutional Repository",
            },
            "officialName": "CIRAD Dataverse",
            "websiteUrl": "https://dataverse.cirad.fr/",
        }
        keep, reason = publishes_datasets(record)
        assert keep is True
        assert reason == "name_or_url_data_signal"

    def test_journal_aggregator_without_signal_dropped(self):
        record = {
            "type": {
                "scheme": "aggregator::pubsrepository::journals",
                "value": "Journal Aggregator/Publisher",
            },
            "officialName": "Example Press",
            "websiteUrl": "https://press.example.org",
        }
        keep, reason = publishes_datasets(record)
        assert keep is False
        assert reason == "publication_only_default"

    def test_graph_dataset_count_overrides_default(self):
        record = {
            "type": {
                "scheme": "pubsrepository::institutional",
                "value": "Institutional Repository",
            },
            "officialName": "Campus IR",
            "websiteUrl": "https://ir.example.edu",
        }
        keep, reason = publishes_datasets(record, dataset_count=12)
        assert keep is True
        assert reason == "graph_dataset_count"
        keep, reason = publishes_datasets(record, dataset_count=0)
        assert keep is False
        assert reason == "no_graph_datasets"


class TestMatchSource:
    def test_matches_host_without_www(self):
        source = {"url": "https://www.example.org/data", "host": "example.org"}
        is_dup, existing = match_source(
            source,
            hosts={"example.org"},
            ids=set(),
            host_to_id={"example.org": "exampleorg"},
        )
        assert is_dup is True
        assert existing == "exampleorg"

    def test_matches_generated_id(self):
        source = {"url": "https://data.example.edu", "host": "data.example.edu"}
        is_dup, existing = match_source(
            source, hosts=set(), ids={"dataexampleedu"}, host_to_id={}
        )
        assert is_dup is True
        assert existing == "dataexampleedu"

    def test_miss(self):
        source = {"url": "https://new-repo.example", "host": "new-repo.example"}
        is_dup, existing = match_source(
            source, hosts={"other.org"}, ids={"otherorg"}, host_to_id={}
        )
        assert is_dup is False
        assert existing is None


class TestSelectSources:
    def test_keeps_data_repo_and_drops_junk(self):
        raw = [
            {
                "id": "openaire____::one",
                "type": {"scheme": "datarepository::unknown", "value": "Data Repository"},
                "officialName": "CERN Open Data Portal",
                "websiteUrl": "https://opendata.cern.ch/",
            },
            {
                "id": "openaire____::junk",
                "type": {"scheme": "datarepository::unknown", "value": "Data Repository"},
                "officialName": "Test",
                "websiteUrl": "http://test.de",
            },
            {
                "id": "openaire____::pub",
                "type": {
                    "scheme": "pubsrepository::institutional",
                    "value": "Institutional Repository",
                },
                "officialName": "Papers only",
                "websiteUrl": "https://papers.example.edu",
                "contentTypes": ["Journal articles"],
            },
        ]
        kept, stats = select_sources(raw)
        assert stats["kept"] == 1
        assert stats["junk_url"] == 1
        assert stats["publication_only"] == 1
        assert kept[0]["url"] == "https://opendata.cern.ch/"
        assert kept[0]["id"] == "openaire____::one"
        assert kept[0]["openaire_url"].endswith("datasourceId=openaire____::one")


class TestHelpers:
    def test_catalog_id(self):
        assert catalog_id_from_url("https://data.example.edu/") == "dataexampleedu"

    def test_infer_software(self):
        assert infer_software("https://dataverse.cirad.fr/", "CIRAD") == "dataverse"
        assert infer_software("https://repo.example.edu/", "IR") == "custom"

    def test_compact_unescapes_name(self):
        record = {
            "id": "x",
            "type": {"scheme": "datarepository::unknown", "value": "Data Repository"},
            "officialName": "Foo &amp; Bar",
            "websiteUrl": "https://foo.example.org/",
        }
        compact = compact_source(record, keep_reason="data_repository_typology")
        assert compact["name"] == "Foo & Bar"
        assert compact["host"] == "foo.example.org"
