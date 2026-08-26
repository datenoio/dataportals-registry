import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from builder import check_is_national_flag, get_priority_level
from constants import ENRICHMENT_ISSUE_TYPES
from national_catalog import classify_is_national


def _opendata(name, link, owner_name, owner_type="Central government"):
    return {
        "name": name,
        "link": link,
        "catalog_type": "Open data portal",
        "owner": {"name": owner_name, "type": owner_type},
        "software": {"id": "ckan", "name": "CKAN"},
        "properties": {"is_national": True},
    }


def test_keep_catalog_data_gov():
    rec = _opendata(
        "The Home of the U.S. Government Open Data",
        "https://catalog.data.gov",
        "GSA Technology Transformation Services",
    )
    keep, reason = classify_is_national(rec, "US/Federal/opendata/catalogdatagov.yaml")
    assert keep is True
    assert reason == "national_open_data"
    rec["_file_path"] = "US/Federal/opendata/catalogdatagov.yaml"
    assert check_is_national_flag(rec) is None


def test_unset_ncbi_biosample():
    rec = {
        "name": "NCBI BioSample",
        "link": "https://www.ncbi.nlm.nih.gov/biosample/",
        "catalog_type": "Scientific data repository",
        "owner": {
            "name": "National Library of Medicine",
            "type": "Central government",
        },
        "software": {"id": "custom", "name": "Custom software"},
        "properties": {"is_national": True},
        "_file_path": "US/Federal/scientific/wwwncbinlmnihgovbiosample.yaml",
    }
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is False
    assert reason in {"scientific_repo", "thematic_or_domain", "agency_or_ministry"}
    issue = check_is_national_flag(rec)
    assert issue is not None
    assert issue["issue_type"] == "IS_NATIONAL_AGENCY_OR_TOPIC"


def test_unset_agency_opendata():
    rec = _opendata(
        "NASA Open Data Portal",
        "https://data.nasa.gov",
        "NASA",
    )
    rec["_file_path"] = "US/Federal/opendata/datanasagov.yaml"
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is False
    assert reason == "agency_or_ministry"
    assert check_is_national_flag(rec) is not None


def test_unset_subnational_path():
    rec = _opendata(
        "Open Government Data Portal of Kerala",
        "https://kerala.data.gov.in",
        "Government of Kerala",
        owner_type="Regional government",
    )
    rec["_file_path"] = "IN/IN-KL/opendata/keraladatagovin.yaml"
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is False
    assert reason in {"subnational_path", "non_central_owner"}


def test_keep_nso_indicators():
    rec = {
        "name": "United States National Summary Data Page",
        "link": "https://www.treasury.gov/nsdp",
        "catalog_type": "Indicators catalog",
        "owner": {
            "name": "U.S. Department of the Treasury",
            "type": "Central government",
        },
        "properties": {"is_national": True},
        "_file_path": "US/Federal/indicators/nsdptreasurygov.yaml",
    }
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is True
    assert reason == "national_statistics"
    assert check_is_national_flag(rec) is None


def test_keep_nsdi_geoportal():
    rec = {
        "name": "Ethiopia National Spatial Data Infrastructure (Ethio-NSDI)",
        "link": "https://nsdi.gov.et",
        "catalog_type": "Geoportal",
        "owner": {"name": "Government of Ethiopia", "type": "Central government"},
        "properties": {"is_national": True},
        "_file_path": "ET/Federal/geo/nsdigovet.yaml",
    }
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is True
    assert check_is_national_flag(rec) is None


def test_unset_false_is_not_an_issue():
    rec = _opendata(
        "NASA Open Data Portal",
        "https://data.nasa.gov",
        "NASA",
    )
    rec["properties"] = {"is_national": False}
    rec["_file_path"] = "US/Federal/opendata/datanasagov.yaml"
    assert check_is_national_flag(rec) is None


def test_missing_flag_is_not_an_issue():
    rec = _opendata(
        "The Home of the U.S. Government Open Data",
        "https://catalog.data.gov",
        "GSA Technology Transformation Services",
    )
    rec["properties"] = {}
    rec["_file_path"] = "US/Federal/opendata/catalogdatagov.yaml"
    assert check_is_national_flag(rec) is None


def test_keep_nso_microdata_and_translated_geoportal():
    rec = {
        "name": "Statistics Sierra Leone microdata catalog (NADA)",
        "link": "https://microdata.statistics.sl/index.php",
        "catalog_type": "Microdata catalog",
        "owner": {"name": "Statistics Sierra Leone", "type": "Central government"},
        "properties": {"is_national": True},
        "_file_path": "SL/Federal/microdata/microdatastatisticssl.yaml",
    }
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is True, reason

    geo = {
        "name": "Národný geoportál",
        "description": "National Geoportal of Slovakia (Národný geoportál).",
        "link": "https://geoportal.gov.sk/",
        "catalog_type": "Geoportal",
        "owner": {"name": "Geodesy, Cartography and Cadastre Authority", "type": "Central government"},
        "properties": {"is_national": True},
        "_file_path": "SK/Federal/geo/geoportalgovsk.yaml",
    }
    keep, reason = classify_is_national(geo, geo["_file_path"])
    assert keep is True, reason


def test_issue_is_medium_enrichment():
    assert get_priority_level("IS_NATIONAL_AGENCY_OR_TOPIC") == "MEDIUM"
    assert "IS_NATIONAL_AGENCY_OR_TOPIC" in ENRICHMENT_ISSUE_TYPES


def test_unset_nga_and_geoplatform_themes():
    nga = {
        "name": "National Geospatial-Intelligence Agency (NGA) Geoportal",
        "link": "https://geoint.nga.mil",
        "catalog_type": "Geoportal",
        "owner": {
            "name": "National Geospatial-Intelligence Agency",
            "type": "Central government",
        },
        "properties": {"is_national": True},
        "_file_path": "US/Federal/geo/ngageoportal.yaml",
    }
    keep, reason = classify_is_national(nga, nga["_file_path"])
    assert keep is False, reason

    theme = {
        "name": "United States | Address Data Theme",
        "link": "https://address.geoplatform.gov",
        "description": "FGDC address theme on GeoPlatform",
        "catalog_type": "Geoportal",
        "owner": {"name": "FGDC", "type": "Central government"},
        "properties": {"is_national": True},
        "_file_path": "US/Federal/geo/addressgeoplatform.yaml",
    }
    keep, reason = classify_is_national(theme, theme["_file_path"])
    assert keep is False
    assert reason in {"geoplatform_thematic_node", "thematic_or_domain"}


def test_keep_fgdc_geoplatform():
    rec = {
        "name": "U.S. Federal Geographic Data Committee (FGDC) Geoportal",
        "link": "https://geonetwork.geoplatform.gov/geonetwork",
        "catalog_type": "Geoportal",
        "owner": {
            "name": "Federal Geographic Data Committee",
            "type": "Central government",
        },
        "properties": {"is_national": True},
        "_file_path": "US/Federal/geo/geonetworkgeoplatformgov.yaml",
    }
    keep, reason = classify_is_national(rec, rec["_file_path"])
    assert keep is True, reason
