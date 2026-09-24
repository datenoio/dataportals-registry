"""Unit tests for quality rules added in the September 2026 review."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from builder import (  # noqa: E402
    check_access_mode_preferred,
    check_api_status_coherence,
    check_content_type_values,
    check_coverage_level_values,
    check_endpoint_type_aliases,
    check_gov_coverage_country_mismatch,
    check_language_reference,
    check_missing_rights_open_data,
    check_owner_level_missing,
    check_status_api_status_coherence_extended,
    check_topic_type_values,
    get_priority_level,
    iter_boilerplate_description_issues,
    iter_is_national_excess_issues,
)
from constants import ENRICHMENT_ISSUE_TYPES  # noqa: E402


def _types(result):
    if not result:
        return []
    if isinstance(result, dict):
        return [result["issue_type"]]
    return [item["issue_type"] for item in result]


def test_coverage_level_nonstandard():
    flagged = check_coverage_level_values(
        {"coverage": [{"location": {"level": 0}}, {"location": {"level": 2}}]}
    )
    assert _types(flagged) == [
        "COVERAGE_LEVEL_NONSTANDARD",
        "COVERAGE_LEVEL_NONSTANDARD",
    ]
    assert check_coverage_level_values(
        {"coverage": [{"location": {"level": 20}}, {"location": {"country": {"id": "US"}}}]}
    ) is None
    assert get_priority_level("COVERAGE_LEVEL_NONSTANDARD") == "IMPORTANT"
    assert "COVERAGE_LEVEL_NONSTANDARD" not in ENRICHMENT_ISSUE_TYPES


def test_deprecated_catalog_cannot_claim_active_api():
    flagged = check_status_api_status_coherence_extended(
        {"status": "deprecated", "api_status": "active", "endpoints": []}
    )
    assert _types(flagged) == ["STATUS_API_STATUS_MISMATCH"]
    assert check_status_api_status_coherence_extended(
        {"status": "inactive", "api_status": "active"}
    )
    assert check_status_api_status_coherence_extended(
        {"status": "deprecated", "api_status": "inactive"}
    ) is None
    retired = check_api_status_coherence(
        {
            "status": "deprecated",
            "api": True,
            "api_status": "inactive",
            "endpoints": [{"type": "ckan", "url": "https://example.org/api"}],
        }
    )
    assert retired is None or "API_STATUS_MISMATCH" not in _types(retired)


def test_owner_level_missing_is_central_and_federal_only():
    assert _types(
        check_owner_level_missing(
            {"owner": {"type": "Central government", "location": {"country": {"id": "US"}}}}
        )
    ) == ["OWNER_LEVEL_MISSING"]
    assert check_owner_level_missing(
        {"owner": {"type": "Central government", "location": {"level": 20}}}
    ) is None
    assert check_owner_level_missing(
        {"owner": {"type": "Local government", "location": {}}}
    ) is None


def test_gov_coverage_country_mismatch_is_single_sovereign_only():
    mismatch = {
        "owner": {
            "type": "Central government",
            "location": {"country": {"id": "MA"}},
        },
        "coverage": [{"location": {"country": {"id": "CM"}}}],
    }
    assert _types(check_gov_coverage_country_mismatch(mismatch)) == [
        "GOV_COVERAGE_COUNTRY_MISMATCH"
    ]
    world = {
        "owner": {
            "type": "Central government",
            "location": {"country": {"id": "SE"}},
        },
        "coverage": [{"location": {"country": {"id": "World"}}}],
    }
    assert check_gov_coverage_country_mismatch(world) is None
    multi = {
        "owner": {
            "type": "Central government",
            "location": {"country": {"id": "SE"}},
        },
        "coverage": [
            {"location": {"country": {"id": "NO"}}},
            {"location": {"country": {"id": "FI"}}},
        ],
    }
    assert check_gov_coverage_country_mismatch(multi) is None
    academy = {
        "owner": {"type": "Academy", "location": {"country": {"id": "SE"}}},
        "coverage": [{"location": {"country": {"id": "World"}}}],
    }
    assert check_gov_coverage_country_mismatch(academy) is None


def test_endpoint_type_alias_names_replacement():
    flagged = check_endpoint_type_aliases(
        {"endpoints": [{"type": "opendatasoft"}, {"type": "ckan"}, {"type": "api"}]}
    )
    assert _types(flagged) == ["ENDPOINT_TYPE_ALIAS", "ENDPOINT_TYPE_ALIAS"]
    assert "opendatasoftapi" in flagged[0]["suggested_action"]
    assert "ENDPOINT_TYPE_ALIAS" in ENRICHMENT_ISSUE_TYPES


def test_topic_type_and_language_and_access_and_content_and_rights():
    assert _types(
        check_topic_type_values(
            {"topics": [{"type": "general"}, {"type": "eudatatheme"}]}
        )
    ) == ["TOPIC_TYPE_NONCANONICAL"]

    langs = check_language_reference(
        {
            "langs": [
                {"id": "DE", "name": "Deutsch"},
                {"id": "EN", "name": "English"},
                {"id": "CN", "name": "Chinese"},
                {"id": "BE", "name": "Belarusian"},
            ]
        }
    )
    assert _types(langs) == ["LANGUAGE_NAME_NONCANONICAL", "LANGUAGE_CODE_UNKNOWN"]

    assert _types(check_access_mode_preferred({"access_mode": ["open", "limited"]})) == [
        "ACCESS_MODE_NONPREFERRED"
    ]
    assert check_access_mode_preferred({"access_mode": ["not-a-mode"]}) is None

    assert _types(check_content_type_values({"content_types": ["dataset", "software"]})) == [
        "CONTENT_TYPE_NONCANONICAL"
    ]

    portal = {
        "status": "active",
        "catalog_type": "Open data portal",
        "access_mode": ["open"],
        "owner": {"type": "Federal government"},
        "properties": {"is_national": True},
        "rights": {},
    }
    assert _types(check_missing_rights_open_data(portal)) == ["MISSING_RIGHTS"]
    agency = dict(portal)
    agency["properties"] = {"is_national": False}
    assert check_missing_rights_open_data(agency) is None
    assert check_missing_rights_open_data({**portal, "properties": {}}) is None
    portal["rights"] = {"license_id": "CC-BY-4.0"}
    assert check_missing_rights_open_data(portal) is None
    portal["catalog_type"] = "Geoportal"
    portal["rights"] = {}
    assert check_missing_rights_open_data(portal) is None


def _meta(record_id, **extra):
    base = {
        "record_id": record_id,
        "file_path": f"US/Federal/opendata/{record_id}.yaml",
        "country_codes": ["US"],
        "description": "",
        "catalog_type": "Indicators catalog",
        "owner_country": "US",
        "is_national": False,
    }
    base.update(extra)
    return base


def test_is_national_excess_flags_groups_larger_than_two():
    metas = [
        _meta("a", is_national=True),
        _meta("b", is_national=True),
        _meta("c", is_national=True),
        _meta("d", is_national=True, owner_country="CA"),
        _meta("e", is_national=True, owner_country="CA"),
    ]
    issues = list(iter_is_national_excess_issues(metas))
    assert len(issues) == 3
    assert {pair[1]["record_id"] for pair in issues} == {"a", "b", "c"}
    assert issues[0][0]["issue_type"] == "IS_NATIONAL_EXCESS"
    assert get_priority_level("IS_NATIONAL_EXCESS") == "MEDIUM"


def test_boilerplate_description_shared_text_and_template_phrase():
    copied = "GeoPortale.cloud municipal geoportal for public consultation of cadastre and planning data."
    metas = [_meta(f"m{i}", description=copied) for i in range(5)]
    metas.append(
        _meta(
            "demo",
            description="ArcGIS Hub demonstration or template site. Not a production catalog.",
        )
    )
    metas.append(_meta("ok", description="City of Oslo open data portal for municipal datasets."))
    issues = list(iter_boilerplate_description_issues(metas))
    ids = {pair[1]["record_id"] for pair in issues}
    assert ids == {"m0", "m1", "m2", "m3", "m4", "demo"}
    demo = next(issue for issue, meta in issues if meta["record_id"] == "demo")
    assert "not a production" in demo["current_value"]["reasons"][0] or any(
        "not a production" in reason for reason in demo["current_value"]["reasons"]
    )
