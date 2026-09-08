"""Tests for constants.py"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from constants import (
    reverse_langs,
    COUNTRIES_LANGS,
    DOMAIN_LOCATIONS,
    DEFAULT_LOCATION,
    MAP_CATALOG_TYPE_SUBDIR,
    MAP_SOFTWARE_ALLOWED_CATALOG_TYPES,
    MAP_SOFTWARE_OWNER_CATALOG_TYPE,
    CUSTOM_SOFTWARE_KEYS,
    CUSTOM_SOFTWARE_ALIAS_CATALOG_TYPE,
    SOFTWARE_MAP_SKIP_IDS,
    SOFTWARE_IDS_PATH,
    software_ids_from_yaml,
    render_software_ids_yaml,
    ENTRY_TEMPLATE,
    COUNTRIES,
)


class TestReverseLangs:
    """Tests for reverse_langs function"""

    def test_reverse_langs_structure(self):
        """Test that reverse_langs returns correct structure"""
        reversed = reverse_langs()
        assert isinstance(reversed, dict)
        # Check that some known mappings exist
        assert "us" in reversed
        assert "uk" in reversed
        assert "de" in reversed

    def test_reverse_langs_values(self):
        """Test that reverse_langs returns correct language codes"""
        reversed = reverse_langs()
        assert reversed.get("us") == "EN"
        assert reversed.get("uk") == "EN"
        assert reversed.get("de") == "DE"
        assert reversed.get("fr") == "FR"


class TestConstants:
    """Tests for constant values"""

    def test_countries_langs_exists(self):
        """Test that COUNTRIES_LANGS is populated"""
        assert isinstance(COUNTRIES_LANGS, dict)
        assert len(COUNTRIES_LANGS) > 0
        assert "us" in COUNTRIES_LANGS
        assert COUNTRIES_LANGS["us"] == "EN"

    def test_domain_locations_structure(self):
        """Test that DOMAIN_LOCATIONS has correct structure"""
        assert isinstance(DOMAIN_LOCATIONS, dict)
        assert "us" in DOMAIN_LOCATIONS
        location = DOMAIN_LOCATIONS["us"]
        assert "location" in location
        assert "country" in location["location"]
        assert location["location"]["country"]["id"] == "US"

    def test_default_location(self):
        """Test DEFAULT_LOCATION structure"""
        assert isinstance(DEFAULT_LOCATION, dict)
        assert "location" in DEFAULT_LOCATION
        assert DEFAULT_LOCATION["location"]["country"]["id"] == "Unknown"

    def test_map_catalog_type_subdir(self):
        """Test MAP_CATALOG_TYPE_SUBDIR mappings"""
        assert isinstance(MAP_CATALOG_TYPE_SUBDIR, dict)
        # Test keys that actually exist in the dictionary
        assert "Geoportal" in MAP_CATALOG_TYPE_SUBDIR
        assert MAP_CATALOG_TYPE_SUBDIR["Geoportal"] == "geo"
        assert "Metadata catalog" in MAP_CATALOG_TYPE_SUBDIR
        assert MAP_CATALOG_TYPE_SUBDIR["Metadata catalog"] == "metadata"
        assert "Scientific data repository" in MAP_CATALOG_TYPE_SUBDIR
        assert MAP_CATALOG_TYPE_SUBDIR["Scientific data repository"] == "scientific"
        assert "Indicators catalog" in MAP_CATALOG_TYPE_SUBDIR
        assert MAP_CATALOG_TYPE_SUBDIR["Indicators catalog"] == "indicators"
        assert "Open data portal" in MAP_CATALOG_TYPE_SUBDIR
        assert MAP_CATALOG_TYPE_SUBDIR["Open data portal"] == "opendata"

    def test_map_software_owner_catalog_type(self):
        """Test MAP_SOFTWARE_OWNER_CATALOG_TYPE mappings"""
        assert isinstance(MAP_SOFTWARE_OWNER_CATALOG_TYPE, dict)
        assert "ckan" in MAP_SOFTWARE_OWNER_CATALOG_TYPE
        assert MAP_SOFTWARE_OWNER_CATALOG_TYPE["ckan"] == "Open data portal"
        assert MAP_SOFTWARE_OWNER_CATALOG_TYPE["arcgishub"] == "Geoportal"
        for software_id in (
            "bexis2",
            "cwis",
            "diversityworkbench",
            "greenstone",
        ):
            assert (
                MAP_SOFTWARE_OWNER_CATALOG_TYPE[software_id]
                == "Scientific data repository"
            )
        assert MAP_SOFTWARE_OWNER_CATALOG_TYPE["vivo"] == "Scientific data repository"

    def test_map_software_owner_catalog_type_from_yaml(self):
        """Primary catalog_type comes from software YAML category, not a hand list."""
        assert "custom" not in MAP_SOFTWARE_OWNER_CATALOG_TYPE
        for software_id in SOFTWARE_MAP_SKIP_IDS:
            assert software_id not in MAP_SOFTWARE_OWNER_CATALOG_TYPE
        for software_id in software_ids_from_yaml():
            if software_id in SOFTWARE_MAP_SKIP_IDS:
                continue
            assert software_id in MAP_SOFTWARE_OWNER_CATALOG_TYPE
        assert MAP_SOFTWARE_OWNER_CATALOG_TYPE["stattech"] == "Indicators catalog"
        for alias, catalog_type in CUSTOM_SOFTWARE_ALIAS_CATALOG_TYPE.items():
            assert MAP_SOFTWARE_OWNER_CATALOG_TYPE[alias] == catalog_type

    def test_software_ids_yaml_matches_software_dir(self):
        actual = Path(SOFTWARE_IDS_PATH).read_text(encoding="utf8")
        assert actual == render_software_ids_yaml()

    def test_map_software_allowed_catalog_types(self):
        """Multi-type software must list every allowed catalog_type pair used in QA."""
        assert "drupal" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES
        assert "Geoportal" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["drupal"]
        assert "Indicators catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["drupal"]
        assert "publishmydata" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES
        assert "Metadata catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["publishmydata"]
        assert "Geoportal" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["ckan"]
        assert "Scientific data repository" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["ckan"]
        assert "Geoportal" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["opendatasoft"]
        assert "Geoportal" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["wordpress"]
        assert "Indicators catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["wordpress"]
        assert "Microdata catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["nada"]
        assert "Scientific data repository" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["nada"]
        assert "Metadata catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["molgenis"]
        assert (
            "Scientific data repository"
            in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["molgenis"]
        )
        assert "Data search engine" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["vivo"]
        assert (
            "Scientific data repository"
            in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["vivo"]
        )
        assert "General research repository" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES[
            "worktribe"
        ]
        assert "Indicators catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES["datawheel"]
        assert "Machine learning catalog" in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES[
            "openmlorg"
        ]
        for software_id, allowed in MAP_SOFTWARE_ALLOWED_CATALOG_TYPES.items():
            primary = MAP_SOFTWARE_OWNER_CATALOG_TYPE.get(software_id)
            if primary:
                assert primary in allowed, software_id

    def test_custom_software_keys(self):
        """Test CUSTOM_SOFTWARE_KEYS list"""
        assert isinstance(CUSTOM_SOFTWARE_KEYS, list)
        assert "searchengines" in CUSTOM_SOFTWARE_KEYS
        assert "ml" in CUSTOM_SOFTWARE_KEYS

    def test_entry_template_structure(self):
        """Test ENTRY_TEMPLATE has required fields"""
        assert isinstance(ENTRY_TEMPLATE, dict)
        required_fields = [
            "id",
            "name",
            "link",
            "catalog_type",
            "access_mode",
            "content_types",
            "coverage",
            "owner",
            "software",
            "status",
        ]
        for field in required_fields:
            assert field in ENTRY_TEMPLATE

    def test_entry_template_defaults(self):
        """Test ENTRY_TEMPLATE default values"""
        assert ENTRY_TEMPLATE["api"] is False
        assert ENTRY_TEMPLATE["api_status"] == "uncertain"
        assert ENTRY_TEMPLATE["status"] == "scheduled"
        assert isinstance(ENTRY_TEMPLATE["access_mode"], list)
        assert isinstance(ENTRY_TEMPLATE["content_types"], list)
        assert isinstance(ENTRY_TEMPLATE["coverage"], list)

    def test_countries_dict(self):
        """Test COUNTRIES dictionary"""
        assert isinstance(COUNTRIES, dict)
        assert "US" in COUNTRIES
        assert COUNTRIES["US"] == "United States"
        assert "GB" in COUNTRIES
        assert COUNTRIES["GB"] == "United Kingdom"
