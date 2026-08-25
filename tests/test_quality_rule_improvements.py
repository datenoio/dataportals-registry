import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from builder import (
    check_coverage_normalization,
    check_nested_field_types,
    check_owner_type_values,
    check_path_country_consistency,
    check_software_expected_endpoints,
    check_title_quality,
    check_urls,
    choose_duplicate_keeper,
    get_priority_level,
    link_serves_as_api_endpoint,
    score_duplicate_keeper,
)


def test_link_serves_as_api_endpoint_geoserver():
    assert link_serves_as_api_endpoint(
        "geoserver", "https://maps.example.gov/geoserver/web/"
    )
    assert not link_serves_as_api_endpoint(
        "geoserver", "https://maps.example.gov/portal"
    )


def test_link_serves_as_api_endpoint_arcgis():
    assert link_serves_as_api_endpoint(
        "arcgisserver", "https://gis.example.gov/arcgis/rest/services"
    )
    assert link_serves_as_api_endpoint(
        "arcgisserver", "https://gis.example.gov/server/rest/services/Base/MapServer"
    )
    assert link_serves_as_api_endpoint(
        "arcgisserver", "https://gis.example.gov/arcgis/services"
    )
    assert not link_serves_as_api_endpoint(
        "arcgisserver", "https://gis.example.gov/opendata"
    )


def test_link_serves_as_api_endpoint_mapserver_cgi():
    assert link_serves_as_api_endpoint(
        "mapserver", "https://maps.example.gov/cgi-bin/mapserv"
    )
    assert not link_serves_as_api_endpoint(
        "mapserver", "https://maps.example.gov/viewer"
    )


def test_software_expected_endpoints_skips_when_link_is_service_root(monkeypatch):
    monkeypatch.setattr(
        "builder.get_cached_software_map",
        lambda: {"geoserver": {"has_api": "Yes", "name": "GeoServer"}},
    )
    record = {
        "software": {"id": "geoserver", "name": "GeoServer"},
        "status": "active",
        "link": "https://example.org/geoserver",
        "endpoints": [],
    }
    assert check_software_expected_endpoints(record) is None


def test_software_expected_endpoints_flags_non_service_link(monkeypatch):
    monkeypatch.setattr(
        "builder.get_cached_software_map",
        lambda: {"ckan": {"has_api": "Yes", "name": "CKAN"}},
    )
    record = {
        "software": {"id": "ckan", "name": "CKAN"},
        "status": "active",
        "link": "https://data.example.gov",
        "endpoints": [],
    }
    issue = check_software_expected_endpoints(record)
    assert issue is not None
    assert issue["issue_type"] == "SOFTWARE_EXPECTED_ENDPOINTS_MISSING_CKAN"
    assert get_priority_level(issue["issue_type"]) == "MEDIUM"


def test_software_expected_endpoints_skips_when_api_true(monkeypatch):
    monkeypatch.setattr(
        "builder.get_cached_software_map",
        lambda: {"ckan": {"has_api": "Yes", "name": "CKAN"}},
    )
    record = {
        "software": {"id": "ckan", "name": "CKAN"},
        "status": "active",
        "api": True,
        "link": "https://data.example.gov",
        "endpoints": [],
    }
    assert check_software_expected_endpoints(record) is None


def test_software_expected_endpoints_skips_deprecated(monkeypatch):
    monkeypatch.setattr(
        "builder.get_cached_software_map",
        lambda: {"stattech": {"has_api": "Yes", "name": ".Stat Technology"}},
    )
    record = {
        "software": {"id": "stattech", "name": ".Stat Technology"},
        "status": "deprecated",
        "api": False,
        "link": "https://stats.example.org",
        "endpoints": [],
    }
    assert check_software_expected_endpoints(record) is None


def test_owner_type_noncanonical_and_invalid(monkeypatch):
    monkeypatch.setattr(
        "builder._load_owner_type_vocab",
        lambda: (
            frozenset({"Academy", "Business"}),
            {"University": "Academy", "Company": "Business"},
        ),
    )
    assert check_owner_type_values({"owner": {"type": "Academy"}}) is None
    noncanon = check_owner_type_values({"owner": {"type": "University"}})
    assert noncanon["issue_type"] == "OWNER_TYPE_NONCANONICAL"
    invalid = check_owner_type_values({"owner": {"type": "Guild"}})
    assert invalid["issue_type"] == "INVALID_OWNER_TYPE"


def test_path_country_consistency_allowlist_and_mismatch():
    ok = check_path_country_consistency(
        {
            "_file_path": "EU/Federal/opendata/example.yaml",
            "owner": {"location": {"country": {"id": "FR", "name": "France"}}},
        }
    )
    assert ok is None
    mismatch = check_path_country_consistency(
        {
            "_file_path": "FR/Federal/opendata/example.yaml",
            "owner": {"location": {"country": {"id": "DE", "name": "Germany"}}},
            "coverage": [{"location": {"country": {"id": "DE", "name": "Germany"}}}],
        }
    )
    assert mismatch["issue_type"] == "PATH_COUNTRY_MISMATCH"


def test_check_urls_validates_catalog_export():
    record = {
        "link": "https://data.example.gov",
        "catalog_export": "not-a-url",
        "owner": {},
        "endpoints": [],
    }
    issues = check_urls(record)
    assert issues
    assert any(i["issue_type"] == "INVALID_CATALOG_EXPORT_URL" for i in issues)


def test_choose_duplicate_keeper_prefers_https_non_www():
    metas = [
        {
            "record_id": "wwwexample",
            "link": "http://www.example.gov/data",
            "file_path": "US/Federal/opendata/wwwexample.yaml",
        },
        {
            "record_id": "example",
            "link": "https://example.gov/data",
            "file_path": "US/Federal/opendata/example.yaml",
        },
    ]
    keeper = choose_duplicate_keeper(metas)
    assert keeper["record_id"] == "example"
    assert score_duplicate_keeper(metas[1]) > score_duplicate_keeper(metas[0])


def test_choose_duplicate_keeper_penalizes_unknown_path():
    metas = [
        {
            "record_id": "portal",
            "link": "https://portal.example.gov",
            "file_path": "Unknown/opendata/portal.yaml",
        },
        {
            "record_id": "portalus",
            "link": "https://portal.example.gov",
            "file_path": "US/Federal/opendata/portalus.yaml",
        },
    ]
    keeper = choose_duplicate_keeper(metas)
    assert keeper["record_id"] == "portalus"


def _coverage_entry(country_id, country_name, level, subregion_id=None, subregion_name=None):
    location = {
        "country": {"id": country_id, "name": country_name},
        "level": level,
        "macroregion": {"id": "021", "name": "Northern America"},
    }
    if subregion_id:
        location["subregion"] = {"id": subregion_id, "name": subregion_name or subregion_id}
    return {"location": location}


def test_duplicate_coverage_allows_distinct_subregions():
    record = {
        "coverage": [
            _coverage_entry("US", "United States", 30, "US-NJ", "New Jersey"),
            _coverage_entry("US", "United States", 30, "US-NY", "New York"),
            _coverage_entry("US", "United States", 30, "US-PA", "Pennsylvania"),
        ]
    }
    result = check_coverage_normalization(record)
    duplicate_issues = [
        issue for issue in (result or []) if issue["issue_type"] == "DUPLICATE_COVERAGE"
    ]
    assert duplicate_issues == []


def test_duplicate_coverage_flags_repeated_subregion():
    record = {
        "coverage": [
            _coverage_entry("US", "United States", 30, "US-NJ", "New Jersey"),
            _coverage_entry("US", "United States", 30, "US-NJ", "New Jersey"),
        ]
    }
    result = check_coverage_normalization(record)
    duplicate_issues = [
        issue for issue in (result or []) if issue["issue_type"] == "DUPLICATE_COVERAGE"
    ]
    assert len(duplicate_issues) == 1
    assert duplicate_issues[0]["field"] == "coverage[1]"


def test_duplicate_coverage_flags_repeated_national_entry():
    record = {
        "coverage": [
            _coverage_entry("US", "United States", 20),
            _coverage_entry("US", "United States", 20),
        ]
    }
    result = check_coverage_normalization(record)
    duplicate_issues = [
        issue for issue in (result or []) if issue["issue_type"] == "DUPLICATE_COVERAGE"
    ]
    assert len(duplicate_issues) == 1


def test_title_quality_iso_footnote_does_not_raise():
    """ISO 3166 names like 'Congo (the) [h]' must not crash urlparse."""
    record = {
        "name": "Congo (the) \u200a [h] - WIS 2.0 in a box",
        "link": "https://wis.dirmet.cg",
    }
    assert check_title_quality(record) is None


def test_title_quality_accepts_human_readable_name():
    record = {
        "name": "Congo - WIS 2.0 in a box",
        "link": "https://wis.dirmet.cg",
    }
    assert check_title_quality(record) is None


def test_title_quality_flags_bare_domain():
    record = {
        "name": "wis.dirmet.cg",
        "link": "https://wis.dirmet.cg",
    }
    issues = check_title_quality(record)
    assert issues
    assert all(i["issue_type"] == "PLACEHOLDER_TITLE" for i in issues)


def test_duplicate_coverage_allows_multi_country():
    record = {
        "coverage": [
            _coverage_entry("US", "United States", 20),
            _coverage_entry("CA", "Canada", 20),
        ]
    }
    result = check_coverage_normalization(record)
    duplicate_issues = [
        issue for issue in (result or []) if issue["issue_type"] == "DUPLICATE_COVERAGE"
    ]
    assert duplicate_issues == []


def _nested_type_record(**overrides):
    record = {
        "id": "example",
        "uid": "cdi00000001",
        "name": "Example",
        "link": "https://example.gov",
        "catalog_type": "Open data portal",
        "status": "active",
        "api": True,
        "access_mode": ["open"],
        "content_types": ["dataset"],
        "tags": ["government"],
        "langs": [{"id": "EN", "name": "English"}],
        "software": {"id": "ckan", "name": "CKAN"},
        "owner": {
            "name": "Example Org",
            "type": "Central government",
            "location": {
                "country": {"id": "US", "name": "United States"},
                "level": 20,
            },
        },
        "coverage": [
            {
                "location": {
                    "country": {"id": "US", "name": "United States"},
                    "level": 20,
                    "macroregion": {"id": "021", "name": "Northern America"},
                }
            }
        ],
        "topics": [
            {"id": "GOVE", "name": "Government and public sector", "type": "eudatatheme"}
        ],
        "properties": {"has_doi": False, "dataset_count_reported": 12},
    }
    record.update(overrides)
    return record


def test_nested_type_clean_record_has_no_issues():
    assert check_nested_field_types(_nested_type_record()) is None


def test_nested_type_priority_is_critical():
    assert get_priority_level("INVALID_NESTED_TYPE") == "CRITICAL"


def test_nested_type_flags_yaml_boolean_country_id():
    import yaml

    parsed = yaml.safe_load(
        """
owner:
  location:
    country:
      id: NO
      name: Norway
    level: 20
coverage:
- location:
    country:
      id: NO
      name: Norway
    level: 20
    macroregion:
      id: '154'
      name: Northern Europe
"""
    )
    assert parsed["owner"]["location"]["country"]["id"] is False
    issues = check_nested_field_types(_nested_type_record(**parsed))
    fields = {issue["field"] for issue in issues}
    assert "owner.location.country.id" in fields
    assert "coverage[0].location.country.id" in fields
    norway_issue = next(
        i for i in issues if i["field"] == "owner.location.country.id"
    )
    assert norway_issue["issue_type"] == "INVALID_NESTED_TYPE"
    assert "quoted string 'NO'" in norway_issue["suggested_action"]


def test_nested_type_flags_integer_tag_and_tag_mapping():
    issues = check_nested_field_types(
        _nested_type_record(tags=["water", 911, {"tag": "sanitation"}])
    )
    by_field = {issue["field"]: issue for issue in issues}
    assert by_field["tags[1]"]["current_value"]["python_type"] == "integer"
    assert "'911'" in by_field["tags[1]"]["suggested_action"]
    assert by_field["tags[2]"]["current_value"]["python_type"] == "object"
    assert "sanitation" in by_field["tags[2]"]["suggested_action"]


def test_nested_type_flags_string_dataset_count_and_integer_m49():
    record = _nested_type_record(
        properties={"has_doi": False, "dataset_count_reported": "14"},
        coverage=[
            {
                "location": {
                    "country": {"id": "EU", "name": "European Union"},
                    "level": 20,
                    "macroregion": {"id": 155, "name": "Western Europe"},
                }
            }
        ],
    )
    issues = check_nested_field_types(record)
    by_field = {issue["field"]: issue for issue in issues}
    assert (
        by_field["properties.dataset_count_reported"]["current_value"]["python_type"]
        == "string"
    )
    assert (
        by_field["coverage[0].location.macroregion.id"]["current_value"]["python_type"]
        == "integer"
    )
    assert "'155'" in by_field["coverage[0].location.macroregion.id"]["suggested_action"]


def test_schema_rejects_mixed_nested_types():
    import json
    from pathlib import Path

    from cerberus import Validator

    schema_path = (
        Path(__file__).resolve().parent.parent / "data" / "schemes" / "catalog.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Validator(schema)
    record = _nested_type_record(
        tags=["water", 911],
        properties={"dataset_count_reported": "14"},
    )
    record["owner"]["location"]["country"]["id"] = False
    assert validator.validate(record) is False
    errors = validator.errors
    assert "tags" in errors or "owner" in errors or "properties" in errors
