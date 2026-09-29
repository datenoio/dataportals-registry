"""Tests for builder.py functions"""

import os
import json
import re
import tempfile
import pytest
import yaml
import types
from pathlib import Path

# Import builder functions
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from builder import (
    load_jsonl,
    load_dataset_jsonl,
    remove_uncompressed_jsonl,
    verify_both_formats_exist,
    build_dataset,
    merge_datasets,
    validate_software_profile,
    jsonl_has_records,
    create_table_from_jsonl,
    _software_counts_toward_coverage,
    _software_field_present,
)


class TestLoadJsonl:
    """Tests for load_jsonl function"""

    def test_load_jsonl_basic(self, temp_jsonl_file):
        """Test loading a basic JSONL file"""
        data = load_jsonl(temp_jsonl_file)
        assert len(data) == 3
        assert data[0]["id"] == "test1"
        assert data[1]["name"] == "Test Catalog 2"
        assert data[2]["link"] == "https://example.com/3"

    def test_load_jsonl_empty_file(self, temp_dir):
        """Test loading an empty JSONL file"""
        filepath = os.path.join(temp_dir, "empty.jsonl")
        with open(filepath, "w", encoding="utf8") as f:
            pass
        data = load_jsonl(filepath)
        assert data == []

    def test_load_jsonl_single_line(self, temp_dir):
        """Test loading a JSONL file with a single line"""
        filepath = os.path.join(temp_dir, "single.jsonl")
        with open(filepath, "w", encoding="utf8") as f:
            f.write('{"id": "single", "name": "Single Item"}\n')
        data = load_jsonl(filepath)
        assert len(data) == 1
        assert data[0]["id"] == "single"


class TestLoadDatasetJsonl:
    """Tests for compressed-export fallbacks."""

    def test_load_dataset_jsonl_prefers_uncompressed(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", temp_dir)
        jsonl_path = os.path.join(temp_dir, "catalogs.jsonl")
        with open(jsonl_path, "w", encoding="utf8") as handle:
            handle.write('{"id": "plain"}\n')
        data = load_dataset_jsonl("catalogs.jsonl")
        assert data == [{"id": "plain"}]

    def test_load_dataset_jsonl_falls_back_to_zst(self, temp_dir, monkeypatch):
        import builder
        import zstandard as zstd

        monkeypatch.setattr(builder, "DATASETS_DIR", temp_dir)
        payload = b'{"id": "compressed"}\n'
        zst_path = os.path.join(temp_dir, "catalogs.jsonl.zst")
        with open(zst_path, "wb") as handle:
            handle.write(zstd.ZstdCompressor().compress(payload))
        data = load_dataset_jsonl("catalogs.jsonl")
        assert data == [{"id": "compressed"}]

    def test_remove_uncompressed_jsonl_keeps_zst(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", temp_dir)
        jsonl_path = os.path.join(temp_dir, "catalogs.jsonl")
        zst_path = os.path.join(temp_dir, "catalogs.jsonl.zst")
        with open(jsonl_path, "w", encoding="utf8") as handle:
            handle.write("{}\n")
        with open(zst_path, "wb") as handle:
            handle.write(b"zst")
        remove_uncompressed_jsonl("catalogs.jsonl")
        assert not os.path.exists(jsonl_path)
        assert os.path.exists(zst_path)

    def test_verify_both_formats_exist_zst_only(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", temp_dir)
        zst_path = os.path.join(temp_dir, "catalogs.jsonl.zst")
        with open(zst_path, "wb") as handle:
            handle.write(b"zst")
        assert (
            verify_both_formats_exist("catalogs.jsonl", require_uncompressed=False)
            is True
        )
        assert verify_both_formats_exist("catalogs.jsonl") is False


class TestBuildDataset:
    """Tests for build_dataset function"""

    def test_build_dataset_from_yaml(self, temp_dir, sample_yaml_content, monkeypatch):
        """Test building a dataset from YAML files"""
        # Create a test directory with YAML files
        yaml_dir = os.path.join(temp_dir, "yaml_data")
        os.makedirs(yaml_dir, exist_ok=True)

        # Create test YAML files
        for i in range(3):
            filepath = os.path.join(yaml_dir, f"test{i}.yaml")
            with open(filepath, "w", encoding="utf8") as f:
                content = sample_yaml_content.replace("testcatalog", f"testcatalog{i}")
                f.write(content)

        # Mock DATASETS_DIR to use temp_dir
        datasets_dir = os.path.join(temp_dir, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        import builder

        # Use monkeypatch to properly mock the module-level variable
        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)

        # Build dataset
        output_filename = "output.jsonl"
        build_dataset(yaml_dir, output_filename)

        # Verify output
        output_file = os.path.join(datasets_dir, output_filename)
        assert os.path.exists(output_file)
        data = load_jsonl(output_file)
        assert len(data) == 3
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)

    def test_build_dataset_empty_directory(self, temp_dir, monkeypatch):
        """Test building dataset from empty directory"""
        yaml_dir = os.path.join(temp_dir, "empty_yaml")
        os.makedirs(yaml_dir, exist_ok=True)

        datasets_dir = os.path.join(temp_dir, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)

        output_filename = "empty_output.jsonl"
        build_dataset(yaml_dir, output_filename)

        output_file = os.path.join(datasets_dir, output_filename)
        # File should be created but empty
        assert os.path.exists(output_file)
        data = load_jsonl(output_file)
        assert len(data) == 0

    def test_build_dataset_nested_directories(
        self, temp_dir, sample_yaml_content, monkeypatch
    ):
        """Test building dataset from nested directory structure"""
        # Create nested directory structure
        base_dir = os.path.join(temp_dir, "nested")
        subdir1 = os.path.join(base_dir, "subdir1")
        subdir2 = os.path.join(base_dir, "subdir2")
        os.makedirs(subdir1, exist_ok=True)
        os.makedirs(subdir2, exist_ok=True)

        # Create YAML files in subdirectories
        for i, subdir in enumerate([subdir1, subdir2]):
            filepath = os.path.join(subdir, f"test{i}.yaml")
            with open(filepath, "w", encoding="utf8") as f:
                content = sample_yaml_content.replace("testcatalog", f"testcatalog{i}")
                f.write(content)

        datasets_dir = os.path.join(temp_dir, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)

        output_filename = "nested_output.jsonl"
        build_dataset(base_dir, output_filename)

        output_file = os.path.join(datasets_dir, output_filename)
        data = load_jsonl(output_file)
        assert len(data) == 2


class TestMergeDatasets:
    """Tests for merge_datasets function"""

    def test_merge_datasets(self, temp_dir, monkeypatch):
        """Test merging multiple JSONL files"""
        datasets_dir = os.path.join(temp_dir, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        # Create test JSONL files
        file1 = os.path.join(datasets_dir, "file1.jsonl")
        file2 = os.path.join(datasets_dir, "file2.jsonl")

        with open(file1, "w", encoding="utf8") as f:
            f.write('{"id": "1", "name": "One"}\n')
            f.write('{"id": "2", "name": "Two"}\n')

        with open(file2, "w", encoding="utf8") as f:
            f.write('{"id": "3", "name": "Three"}\n')

        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)

        output_filename = "merged.jsonl"
        merge_datasets(["file1.jsonl", "file2.jsonl"], output_filename)

        output_file = os.path.join(datasets_dir, output_filename)
        data = load_jsonl(output_file)
        assert len(data) == 3
        assert data[0]["id"] == "1"
        assert data[1]["id"] == "2"
        assert data[2]["id"] == "3"

    def test_merge_datasets_empty_files(self, temp_dir, monkeypatch):
        """Test merging empty JSONL files"""
        datasets_dir = os.path.join(temp_dir, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        file1 = os.path.join(datasets_dir, "empty1.jsonl")
        file2 = os.path.join(datasets_dir, "empty2.jsonl")

        with open(file1, "w", encoding="utf8") as f:
            pass
        with open(file2, "w", encoding="utf8") as f:
            pass

        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)

        output_filename = "merged_empty.jsonl"
        merge_datasets(["empty1.jsonl", "empty2.jsonl"], output_filename)

        output_file = os.path.join(datasets_dir, output_filename)
        data = load_jsonl(output_file)
        assert len(data) == 0

    def test_load_jsonl_invalid_json(self, temp_dir):
        """Test loading JSONL file with invalid JSON line"""
        filepath = os.path.join(temp_dir, "invalid.jsonl")
        with open(filepath, "w", encoding="utf8") as f:
            f.write('{"id": "1", "name": "Valid"}\n')
            f.write('{"id": "2", invalid json}\n')  # Invalid JSON
            f.write('{"id": "3", "name": "Valid"}\n')

        # Should raise JSON decode error
        with pytest.raises(json.JSONDecodeError):
            load_jsonl(filepath)

    def test_build_dataset_malformed_yaml(self, temp_dir, monkeypatch):
        """Test building dataset with malformed YAML file"""
        yaml_dir = os.path.join(temp_dir, "yaml_data")
        os.makedirs(yaml_dir, exist_ok=True)

        # Create a valid YAML file
        valid_file = os.path.join(yaml_dir, "valid.yaml")
        with open(valid_file, "w", encoding="utf8") as f:
            f.write("id: test\nname: Test\n")

        # Create a malformed YAML file
        invalid_file = os.path.join(yaml_dir, "invalid.yaml")
        with open(invalid_file, "w", encoding="utf8") as f:
            f.write("id: test\ninvalid: [unclosed\n")

        datasets_dir = os.path.join(temp_dir, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        import builder

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)

        # Should raise YAMLError when processing invalid file
        with pytest.raises(yaml.YAMLError):
            build_dataset(yaml_dir, "output.jsonl")


class TestBuilderApidetectIntegration:
    """Integration tests for builder -> apidetect invocation path."""

    def test_add_single_entry_calls_detect_single_scheduled(self, temp_dir, monkeypatch):
        import builder

        datasets_dir = os.path.join(temp_dir, "datasets")
        scheduled_dir = os.path.join(temp_dir, "scheduled")
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(datasets_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        os.makedirs(entries_dir, exist_ok=True)

        with open(os.path.join(datasets_dir, "software.jsonl"), "w", encoding="utf8") as f:
            f.write('{"id": "ckan", "name": "CKAN"}\n')

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)
        monkeypatch.setattr(builder, "SCHEDULED_DIR", scheduled_dir)
        monkeypatch.setattr(builder, "ROOT_DIR", entries_dir)

        calls = []

        def _fake_detect_single(uniqid, dryrun=False, mode="entries", **kwargs):
            calls.append((uniqid, dryrun, mode))

        monkeypatch.setitem(
            sys.modules, "apidetect", types.SimpleNamespace(detect_single=_fake_detect_single)
        )

        builder._add_single_entry(
            url="https://catalog.example.org",
            software="ckan",
            country="US",
            scheduled=True,
            preloaded=[],
        )

        assert calls == [("catalogexampleorg", False, "scheduled")]

    def test_add_single_entry_calls_detect_single_entries(self, temp_dir, monkeypatch):
        import builder

        datasets_dir = os.path.join(temp_dir, "datasets")
        scheduled_dir = os.path.join(temp_dir, "scheduled")
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(datasets_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        os.makedirs(entries_dir, exist_ok=True)

        with open(os.path.join(datasets_dir, "software.jsonl"), "w", encoding="utf8") as f:
            f.write('{"id": "ckan", "name": "CKAN"}\n')

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)
        monkeypatch.setattr(builder, "SCHEDULED_DIR", scheduled_dir)
        monkeypatch.setattr(builder, "ROOT_DIR", entries_dir)

        calls = []

        def _fake_detect_single(uniqid, dryrun=False, mode="entries", **kwargs):
            calls.append((uniqid, dryrun, mode))

        monkeypatch.setitem(
            sys.modules, "apidetect", types.SimpleNamespace(detect_single=_fake_detect_single)
        )

        builder._add_single_entry(
            url="https://catalog.example.org",
            software="ckan",
            country="US",
            scheduled=False,
            preloaded=[],
        )

        assert calls == [("catalogexampleorg", False, "entries")]


class TestSoftwareSubtypeValidation:
    """Tests for software subtype taxonomy checks"""

    def _base_software(self):
        return {
            "id": "sample",
            "type": "Software",
            "category": "Open data portal",
            "subtype": "data_portal_platform",
        }

    def test_validate_software_profile_requires_subtype(self):
        record = self._base_software()
        record.pop("subtype")
        issues = validate_software_profile(record)
        assert any(i["issue_type"] == "SOFTWARE_SUBTYPE_MISSING" for i in issues)

    def test_validate_software_profile_rejects_invalid_subtype(self):
        record = self._base_software()
        record["subtype"] = "invalid_subtype"
        issues = validate_software_profile(record)
        assert any(i["issue_type"] == "SOFTWARE_SUBTYPE_INVALID" for i in issues)

    def test_validate_software_profile_checks_category_compatibility(self):
        record = self._base_software()
        record["subtype"] = "scientific_repository_platform"
        issues = validate_software_profile(record)
        assert any(i["issue_type"] == "SOFTWARE_SUBTYPE_CATEGORY_MISMATCH" for i in issues)

    def test_statistical_production_subtypes_are_distinct_from_catalogs(self):
        record = self._base_software()
        record.update(category="Statistical production software", subtype="statistical_processing_system")
        assert not any(i["issue_type"].startswith("SOFTWARE_SUBTYPE") for i in validate_software_profile(record))
        record["subtype"] = "microdata_catalog_platform"
        assert any(i["issue_type"] == "SOFTWARE_SUBTYPE_CATEGORY_MISMATCH" for i in validate_software_profile(record))

    def test_coverage_includes_oss_portal_for_version_and_repo(self):
        record = self._base_software()
        assert _software_counts_toward_coverage(record, "version")
        assert _software_counts_toward_coverage(record, "repository_url")
        assert _software_counts_toward_coverage(record, "documentation_url")

    def test_coverage_excludes_saas_from_version_and_repo(self):
        record = self._base_software()
        record["subtype"] = "managed_saas_service"
        assert not _software_counts_toward_coverage(record, "version")
        assert not _software_counts_toward_coverage(record, "repository_url")
        assert _software_counts_toward_coverage(record, "license")
        assert _software_counts_toward_coverage(record, "documentation_url")

    def test_coverage_counts_domain_stack_for_repo_not_version(self):
        record = self._base_software()
        record["subtype"] = "domain_data_infrastructure"
        assert not _software_counts_toward_coverage(record, "version")
        assert _software_counts_toward_coverage(record, "repository_url")

    def test_software_field_present_treats_empty_as_missing(self):
        assert not _software_field_present({"version": None}, "version")
        assert not _software_field_present({"version": ""}, "version")
        assert _software_field_present({"version": "2.11.4"}, "version")

    def _software_schema(self):
        schema_path = (
            Path(__file__).resolve().parents[1] / "data" / "schemes" / "software.json"
        )
        return json.loads(schema_path.read_text(encoding="utf8"))

    def _complete_software(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "software"
            / "opendata"
            / "ckan.yaml"
        )
        return yaml.safe_load(path.read_text(encoding="utf8"))

    def test_schema_rejects_boolean_metadata_support(self):
        from cerberus import Validator

        record = self._complete_software()
        record["metadata_support"]["ckan_api"] = True
        assert not Validator(self._software_schema()).validate(record)

    def test_schema_requires_all_metadata_support_keys(self):
        from cerberus import Validator

        record = self._complete_software()
        del record["metadata_support"]["wms"]
        assert not Validator(self._software_schema()).validate(record)

    def test_schema_rejects_unknown_category(self):
        from cerberus import Validator

        record = self._complete_software()
        record["category"] = "Not a catalog type"
        assert not Validator(self._software_schema()).validate(record)


class TestAddSingleEntryForceBehavior:
    """Force flag semantics: existing files are skipped unless force is set."""

    def _prepare(self, temp_dir, monkeypatch):
        import builder

        datasets_dir = os.path.join(temp_dir, "datasets")
        scheduled_dir = os.path.join(temp_dir, "scheduled")
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(datasets_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        os.makedirs(entries_dir, exist_ok=True)

        with open(os.path.join(datasets_dir, "software.jsonl"), "w", encoding="utf8") as f:
            f.write('{"id": "ckan", "name": "CKAN"}\n')

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)
        monkeypatch.setattr(builder, "SCHEDULED_DIR", scheduled_dir)
        monkeypatch.setattr(builder, "ROOT_DIR", entries_dir)

        calls = []

        def _fake_detect_single(uniqid, dryrun=False, mode="entries", **kwargs):
            calls.append((uniqid, dryrun, mode))

        monkeypatch.setitem(
            sys.modules, "apidetect", types.SimpleNamespace(detect_single=_fake_detect_single)
        )
        return builder, os.path.join(scheduled_dir, "US", "opendata", "catalogexampleorg.yaml"), calls

    def test_existing_file_is_skipped_without_force(self, temp_dir, monkeypatch):
        builder, path, calls = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://catalog.example.org", software="ckan", country="US", preloaded=[]
        )
        assert os.path.exists(path)
        with open(path, "w", encoding="utf8") as f:
            f.write("sentinel: true\n")

        builder._add_single_entry(
            url="https://catalog.example.org", software="ckan", country="US", preloaded=[]
        )

        with open(path, encoding="utf8") as f:
            assert f.read() == "sentinel: true\n"
        assert calls == [("catalogexampleorg", False, "scheduled")]

    def test_existing_file_is_overwritten_with_force(self, temp_dir, monkeypatch):
        builder, path, calls = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://catalog.example.org", software="ckan", country="US", preloaded=[]
        )
        assert len(calls) == 1

        builder._add_single_entry(
            url="https://catalog.example.org",
            software="ckan",
            country="US",
            force=True,
            preloaded=[],
        )

        with open(path, encoding="utf8") as f:
            assert "sentinel" not in f.read()
        assert len(calls) == 2


class TestAddSingleEntryMetadata:
    """add-single metadata options: langs dicts, subregion, owner type, id, detect."""

    def _prepare(self, temp_dir, monkeypatch):
        import builder

        datasets_dir = os.path.join(temp_dir, "datasets")
        scheduled_dir = os.path.join(temp_dir, "scheduled")
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(datasets_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        os.makedirs(entries_dir, exist_ok=True)

        with open(os.path.join(datasets_dir, "software.jsonl"), "w", encoding="utf8") as f:
            f.write('{"id": "ckan", "name": "CKAN"}\n')

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)
        monkeypatch.setattr(builder, "SCHEDULED_DIR", scheduled_dir)
        monkeypatch.setattr(builder, "ROOT_DIR", entries_dir)

        calls = []

        def _fake_detect_single(uniqid, dryrun=False, mode="entries", **kwargs):
            calls.append((uniqid, dryrun, mode))

        monkeypatch.setitem(
            sys.modules, "apidetect", types.SimpleNamespace(detect_single=_fake_detect_single)
        )
        return builder, scheduled_dir, calls

    def _read(self, path):
        with open(path, encoding="utf8") as f:
            return yaml.safe_load(f)

    def test_lang_emitted_as_dict(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://dati.example.it", software="ckan", country="IT",
            lang="it", preloaded=[],
        )
        record = self._read(os.path.join(scheduled_dir, "IT", "opendata", "datiexampleit.yaml"))
        assert record["langs"] == [{"id": "IT", "name": "Italian"}]

    def test_lang_auto_filled_from_country(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://daten.example.de", software="ckan", country="DE", preloaded=[]
        )
        record = self._read(os.path.join(scheduled_dir, "DE", "opendata", "datenexamplede.yaml"))
        assert record["langs"] == [{"id": "DE", "name": "German"}]

    def test_unknown_lang_raises_and_writes_nothing(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="Unknown language code"):
            builder._add_single_entry(
                url="https://dati.example.it", software="ckan", country="IT",
                lang="xx", preloaded=[],
            )
        assert not os.path.exists(os.path.join(scheduled_dir, "IT"))

    def test_locale_lang_normalized(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://data.example.tw", software="ckan", country="TW",
            lang="zh-TW", preloaded=[],
        )
        record = self._read(os.path.join(scheduled_dir, "TW", "opendata", "dataexampletw.yaml"))
        assert record["langs"] == [{"id": "ZH", "name": "Chinese"}]

    def test_subregion_sets_location_and_directory(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://dados.example.pt", software="ckan", country="PT",
            subregion="PT-11", owner_type="Local government", preloaded=[],
        )
        path = os.path.join(scheduled_dir, "PT", "PT-11", "opendata", "dadosexamplept.yaml")
        record = self._read(path)
        assert record["owner"]["location"]["subregion"] == {"id": "PT-11", "name": "Lisboa"}
        assert record["owner"]["location"]["level"] == 30
        assert record["coverage"][0]["location"]["subregion"]["id"] == "PT-11"
        assert record["coverage"][0]["location"]["level"] == 30

    def test_subregion_country_mismatch_raises(self, temp_dir, monkeypatch):
        builder, _, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="does not belong to country"):
            builder._add_single_entry(
                url="https://dados.example.pt", software="ckan", country="PT",
                subregion="US-CA", preloaded=[],
            )

    def test_unknown_subregion_raises(self, temp_dir, monkeypatch):
        builder, _, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="Unknown subregion"):
            builder._add_single_entry(
                url="https://dados.example.pt", software="ckan", country="PT",
                subregion="PT-99", preloaded=[],
            )

    def test_owner_type_synonym_canonicalized(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://data.example.edu", software="ckan", country="US",
            owner_type="University", preloaded=[],
        )
        record = self._read(os.path.join(scheduled_dir, "US", "opendata", "dataexampleedu.yaml"))
        assert record["owner"]["type"] == "Academy"

    def test_unknown_owner_type_raises(self, temp_dir, monkeypatch):
        builder, _, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="Unknown owner type"):
            builder._add_single_entry(
                url="https://data.example.org", software="ckan", country="US",
                owner_type="Space agency", preloaded=[],
            )

    def test_record_id_override(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://webgis.example.it/comune-a/", software="custom",
            catalog_type="Geoportal", country="IT",
            record_id="webgisexampleitcomunea", preloaded=[],
        )
        path = os.path.join(scheduled_dir, "IT", "geo", "webgisexampleitcomunea.yaml")
        assert os.path.exists(path)
        assert self._read(path)["id"] == "webgisexampleitcomunea"

    def test_invalid_record_id_raises(self, temp_dir, monkeypatch):
        builder, _, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="Invalid id"):
            builder._add_single_entry(
                url="https://data.example.org", software="ckan", country="US",
                record_id="Bad_ID!", preloaded=[],
            )

    def test_no_detect_skips_probe(self, temp_dir, monkeypatch):
        builder, scheduled_dir, calls = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://catalog.example.org", software="ckan", country="US",
            detect=False, preloaded=[],
        )
        assert os.path.exists(os.path.join(scheduled_dir, "US", "opendata", "catalogexampleorg.yaml"))
        assert calls == []

    def test_is_national_flag(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        builder._add_single_entry(
            url="https://data.example.gov", software="ckan", country="US",
            is_national=True, preloaded=[],
        )
        record = self._read(os.path.join(scheduled_dir, "US", "opendata", "dataexamplegov.yaml"))
        assert record["properties"]["is_national"] is True

    def test_schema_invalid_record_refused(self, temp_dir, monkeypatch):
        builder, scheduled_dir, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="failed schema validation"):
            builder._add_single_entry(
                url="https://data.example.org", software="custom",
                catalog_type="Not a real type", country="US", preloaded=[],
            )
        assert not os.path.exists(os.path.join(scheduled_dir, "US"))


class TestAddBatchManifest:
    """add-batch: manifest ingestion, dedupe, validation, UID assignment."""

    def _prepare(self, temp_dir, monkeypatch):
        import builder

        datasets_dir = os.path.join(temp_dir, "datasets")
        scheduled_dir = os.path.join(temp_dir, "scheduled")
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(datasets_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        os.makedirs(entries_dir, exist_ok=True)

        with open(os.path.join(datasets_dir, "software.jsonl"), "w", encoding="utf8") as f:
            f.write('{"id": "ckan", "name": "CKAN"}\n')
        with open(os.path.join(datasets_dir, "full.jsonl"), "w", encoding="utf8") as f:
            f.write(
                '{"id": "catalogdatagov", "link": "https://catalog.data.gov", '
                '"uid": "cdi00001616"}\n'
            )

        monkeypatch.setattr(builder, "DATASETS_DIR", datasets_dir)
        monkeypatch.setattr(builder, "SCHEDULED_DIR", scheduled_dir)
        monkeypatch.setattr(builder, "ROOT_DIR", entries_dir)
        return builder, scheduled_dir

    def _write_manifest(self, temp_dir, rows):
        path = os.path.join(temp_dir, "manifest.jsonl")
        with open(path, "w", encoding="utf8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
        return path

    def test_writes_valid_rows_and_assigns_uids(self, temp_dir, monkeypatch):
        builder, scheduled_dir = self._prepare(temp_dir, monkeypatch)
        manifest = self._write_manifest(temp_dir, [
            {"url": "https://dados-faro.example.pt", "name": "Faro", "software": "ckan",
             "country": "PT", "subregion": "PT-08", "owner_type": "Local government"},
            {"url": "https://dati-milano.example.it", "name": "Milano", "software": "ckan",
             "country": "IT", "langs": ["it"]},
        ])
        summary = builder._add_batch_manifest(manifest)
        assert summary["written"] == 2
        assert summary["invalid_rows"] == []
        assert summary["skipped_dupes"] == []
        uids = sorted(summary["assigned_uids"].values())
        assert uids == ["temp00000001", "temp00000002"]
        faro = os.path.join(scheduled_dir, "PT", "PT-08", "opendata", "dadosfaroexamplept.yaml")
        with open(faro, encoding="utf8") as f:
            record = yaml.safe_load(f)
        assert record["uid"] == "temp00000001"
        assert record["langs"] == [{"id": "PT", "name": "Portuguese"}]
        assert record["owner"]["location"]["subregion"]["id"] == "PT-08"

    def test_skips_export_duplicates(self, temp_dir, monkeypatch):
        builder, _ = self._prepare(temp_dir, monkeypatch)
        manifest = self._write_manifest(temp_dir, [
            {"url": "https://catalog.data.gov", "name": "Dupe"},
            {"url": "https://new-portal.example.org", "name": "New", "country": "US"},
        ])
        summary = builder._add_batch_manifest(manifest)
        assert summary["written"] == 1
        assert summary["skipped_dupes"] == [("catalogdatagov", "catalogdatagov")]

    def test_skips_in_manifest_duplicates(self, temp_dir, monkeypatch):
        builder, _ = self._prepare(temp_dir, monkeypatch)
        manifest = self._write_manifest(temp_dir, [
            {"url": "https://portal.example.org/data", "name": "A", "country": "US"},
            {"url": "https://portal.example.org/data/", "name": "B", "country": "US"},
        ])
        summary = builder._add_batch_manifest(manifest)
        assert summary["written"] == 1
        assert len(summary["skipped_dupes"]) == 1

    def test_invalid_rows_reported_valid_rows_written(self, temp_dir, monkeypatch):
        builder, _ = self._prepare(temp_dir, monkeypatch)
        manifest = self._write_manifest(temp_dir, [
            {"url": "https://good.example.org", "name": "Good", "country": "US"},
            {"url": "https://bad.example.org", "name": "Bad", "country": "US",
             "owner_type": "Space agency"},
        ])
        summary = builder._add_batch_manifest(manifest)
        assert summary["written"] == 1
        assert len(summary["invalid_rows"]) == 1
        lineno, rid, err = summary["invalid_rows"][0]
        assert lineno == 2
        assert "Unknown owner type" in err

    def test_path_tenants_on_same_host_both_written(self, temp_dir, monkeypatch):
        builder, scheduled_dir = self._prepare(temp_dir, monkeypatch)
        manifest = self._write_manifest(temp_dir, [
            {"url": "https://webgis.example.it/comune-a/", "name": "A", "country": "IT",
             "catalog_type": "Geoportal", "id": "webgisexampleitcomunea"},
            {"url": "https://webgis.example.it/comune-b/", "name": "B", "country": "IT",
             "catalog_type": "Geoportal", "id": "webgisexampleitcomuneb"},
        ])
        summary = builder._add_batch_manifest(manifest)
        assert summary["written"] == 2
        assert os.path.exists(os.path.join(scheduled_dir, "IT", "geo", "webgisexampleitcomunea.yaml"))
        assert os.path.exists(os.path.join(scheduled_dir, "IT", "geo", "webgisexampleitcomuneb.yaml"))

    def test_missing_manifest_raises(self, temp_dir, monkeypatch):
        builder, _ = self._prepare(temp_dir, monkeypatch)
        with pytest.raises(ValueError, match="not exists"):
            builder._add_batch_manifest(os.path.join(temp_dir, "nope.jsonl"))


class TestAssignDryrun:
    """assign_by_dir dryrun mode must not touch files."""

    def test_dryrun_does_not_write(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "_query_export_uid_collisions", lambda uids: {})
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(entries_dir, exist_ok=True)
        path = os.path.join(entries_dir, "sample.yaml")
        with open(path, "w", encoding="utf8") as f:
            f.write("id: sample\nname: Sample\n")

        builder.assign_by_dir("cdi", entries_dir, dryrun=True)
        with open(path, encoding="utf8") as f:
            assert "uid" not in yaml.safe_load(f)

        builder.assign_by_dir("cdi", entries_dir, dryrun=False)
        with open(path, encoding="utf8") as f:
            record = yaml.safe_load(f)
        assert record["uid"] == "cdi00000001"
        assert record["id"] == "sample"


class TestAssignInvalidUid:
    """assign_by_dir must repair overflowed UIDs without rewriting YAML bodies."""

    def test_reassigns_nine_digit_uids_using_gaps(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "_query_export_uid_collisions", lambda uids: {})
        entries_dir = os.path.join(temp_dir, "entities")
        os.makedirs(entries_dir, exist_ok=True)

        high_path = os.path.join(entries_dir, "high.yaml")
        invalid_path = os.path.join(entries_dir, "invalid.yaml")
        missing_path = os.path.join(entries_dir, "missing.yaml")
        with open(high_path, "w", encoding="utf8") as f:
            f.write("id: high\nname: High\nuid: cdi99999999\n")
        with open(invalid_path, "w", encoding="utf8") as f:
            f.write(
                "id: invalid\n"
                "name: Invalid\n"
                "description: keep this body\n"
                "uid: cdi100000000\n"
            )
        with open(missing_path, "w", encoding="utf8") as f:
            f.write("id: missing\nname: Missing\n")

        builder.assign_by_dir("cdi", entries_dir, dryrun=False)

        with open(high_path, encoding="utf8") as f:
            high_text = f.read()
        with open(invalid_path, encoding="utf8") as f:
            invalid_text = f.read()
        with open(missing_path, encoding="utf8") as f:
            missing_text = f.read()

        assert yaml.safe_load(high_text)["uid"] == "cdi99999999"
        assert yaml.safe_load(invalid_text)["uid"] == "cdi00000001"
        assert yaml.safe_load(missing_text)["uid"] == "cdi00000002"
        assert "description: keep this body\n" in invalid_text
        assert re.search(r"^(cdi|temp)\d{8}$", yaml.safe_load(invalid_text)["uid"])


class TestAssignNew:
    """assign --new: incremental, git-scoped, export-cross-checked UID assignment."""

    def _setup_repo(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "_REPO_ROOT", temp_dir)
        monkeypatch.setattr(builder, "_query_export_uid_collisions", lambda uids: {})
        monkeypatch.setattr(builder, "_collect_used_uid_numbers", lambda dirs, prefix: set())
        entities_dir = os.path.join(temp_dir, "data", "entities", "US", "Federal", "opendata")
        scheduled_dir = os.path.join(temp_dir, "data", "scheduled", "US", "opendata")
        os.makedirs(entities_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        return builder, entities_dir, scheduled_dir

    def test_assigns_only_changed_files_and_keeps_valid_uids(self, temp_dir, monkeypatch):
        builder, entities_dir, _ = self._setup_repo(temp_dir, monkeypatch)
        has_uid = os.path.join(entities_dir, "hasuid.yaml")
        needs_uid = os.path.join(entities_dir, "needsuid.yaml")
        untouched = os.path.join(entities_dir, "untouched.yaml")
        with open(has_uid, "w", encoding="utf8") as f:
            f.write("id: hasuid\nuid: cdi00000005\n")
        with open(needs_uid, "w", encoding="utf8") as f:
            f.write("id: needsuid\n")
        with open(untouched, "w", encoding="utf8") as f:
            f.write("id: untouched\n")

        monkeypatch.setattr(builder, "_git_changed_yaml_files", lambda: [has_uid, needs_uid])
        assigned = builder.assign_new()

        assert set(assigned) == {needs_uid}
        with open(needs_uid, encoding="utf8") as f:
            # cdi00000005 is used by hasuid.yaml, so the next free number is 6
            assert yaml.safe_load(f)["uid"] == "cdi00000006"
        with open(has_uid, encoding="utf8") as f:
            assert yaml.safe_load(f)["uid"] == "cdi00000005"
        with open(untouched, encoding="utf8") as f:
            assert "uid" not in yaml.safe_load(f)

    def test_scheduled_files_get_temp_prefix(self, temp_dir, monkeypatch):
        builder, _, scheduled_dir = self._setup_repo(temp_dir, monkeypatch)
        path = os.path.join(scheduled_dir, "schedrec.yaml")
        with open(path, "w", encoding="utf8") as f:
            f.write("id: schedrec\n")

        monkeypatch.setattr(builder, "_git_changed_yaml_files", lambda: [path])
        assigned = builder.assign_new()
        assert assigned[path].startswith("temp")

    def test_collision_aborts_before_writes(self, temp_dir, monkeypatch):
        builder, entities_dir, _ = self._setup_repo(temp_dir, monkeypatch)
        monkeypatch.setattr(
            builder,
            "_query_export_uid_collisions",
            lambda uids: {"cdi00000001": "otherrecord"},
        )
        path = os.path.join(entities_dir, "needsuid.yaml")
        with open(path, "w", encoding="utf8") as f:
            f.write("id: needsuid\n")

        monkeypatch.setattr(builder, "_git_changed_yaml_files", lambda: [path])
        with pytest.raises(ValueError, match="UID collision"):
            builder.assign_new()
        with open(path, encoding="utf8") as f:
            assert "uid" not in yaml.safe_load(f)

    def test_missing_exports_warn_and_continue(self, temp_dir, monkeypatch):
        builder, entities_dir, _ = self._setup_repo(temp_dir, monkeypatch)
        monkeypatch.setattr(builder, "_query_export_uid_collisions", lambda uids: None)
        path = os.path.join(entities_dir, "needsuid.yaml")
        with open(path, "w", encoding="utf8") as f:
            f.write("id: needsuid\n")

        monkeypatch.setattr(builder, "_git_changed_yaml_files", lambda: [path])
        assigned = builder.assign_new()
        assert assigned[path] == "cdi00000001"

    def test_git_porcelain_parsing(self, temp_dir, monkeypatch):
        import builder
        import subprocess as real_subprocess

        # real files the fake git output points at
        keep = [
            "data/entities/US/Federal/opendata/new.yaml",
            "data/entities/FR/Federal/geo/mod.yaml",
            "data/scheduled/BR/opendata/sched.yaml",
            "data/entities/DE/Federal/opendata/renamed.yaml",
        ]
        for rel in keep:
            full = os.path.join(temp_dir, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf8") as f:
                f.write("id: x\n")

        porcelain = (
            "?? data/entities/US/Federal/opendata/new.yaml\n"
            " M data/entities/FR/Federal/geo/mod.yaml\n"
            "?? data/scheduled/BR/opendata/sched.yaml\n"
            "R  data/entities/DE/Federal/opendata/old.yaml -> data/entities/DE/Federal/opendata/renamed.yaml\n"
            "?? data/entities/US/Federal/opendata/deleted.yaml\n"  # not on disk -> skipped
            "?? docs/cli.md\n"  # not yaml under entities/scheduled
            "?? data/software/opendata/andino.yaml\n"  # yaml but wrong dir
        )

        class FakeResult:
            stdout = porcelain

        monkeypatch.setattr(
            real_subprocess, "run", lambda *a, **k: FakeResult()
        )
        files = builder._git_changed_yaml_files(repo_root=temp_dir)
        rels = {os.path.relpath(f, temp_dir) for f in files}
        assert rels == set(keep)

    def test_git_failure_raises_value_error(self, temp_dir, monkeypatch):
        import builder
        import subprocess as real_subprocess

        def boom(*a, **k):
            raise real_subprocess.CalledProcessError(1, "git")

        monkeypatch.setattr(real_subprocess, "run", boom)
        with pytest.raises(ValueError, match="git status"):
            builder._git_changed_yaml_files(repo_root=temp_dir)


class TestRecordUpdateTooling:
    """set-field and enrich-batch record update commands."""

    def _valid_record(self, rid):
        return {
            "id": rid,
            "uid": "cdi00000001",
            "name": f"Record {rid}",
            "link": "https://example.com",
            "catalog_type": "Open data portal",
            "access_mode": ["open"],
            "status": "active",
            "software": {"id": "custom", "name": "Custom"},
            "owner": {
                "name": "Owner",
                "type": "Central government",
                "location": {"country": {"id": "US", "name": "United States"}},
            },
        }

    def _setup(self, temp_dir, monkeypatch, records):
        import builder
        from typer.testing import CliRunner

        entities_dir = os.path.join(temp_dir, "entities")
        scheduled_dir = os.path.join(temp_dir, "scheduled")
        os.makedirs(entities_dir, exist_ok=True)
        os.makedirs(scheduled_dir, exist_ok=True)
        monkeypatch.setattr(builder, "ROOT_DIR", entities_dir)
        monkeypatch.setattr(builder, "SCHEDULED_DIR", scheduled_dir)
        paths = {}
        for record in records:
            path = os.path.join(entities_dir, f"{record['id']}.yaml")
            with open(path, "w", encoding="utf8") as f:
                f.write(yaml.safe_dump(record, sort_keys=False, allow_unicode=True))
            paths[record["id"]] = path
        return builder, CliRunner(), paths

    def test_scalar_parsing(self, temp_dir, monkeypatch):
        builder, _, _ = self._setup(temp_dir, monkeypatch, [])
        assert builder._parse_scalar("true") is True
        assert builder._parse_scalar("30") == 30
        assert builder._parse_scalar("[a, b]") == ["a", "b"]
        assert builder._parse_scalar("Central government") == "Central government"

    def test_set_field_creates_nested_path(self, temp_dir, monkeypatch):
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [self._valid_record("reca")])
        result = runner.invoke(
            builder.app,
            ["set-field", "--id", "reca", "--path", "properties.is_national", "--value", "true"],
        )
        assert result.exit_code == 0, result.output
        with open(paths["reca"], encoding="utf8") as f:
            record = yaml.safe_load(f)
        assert record["properties"]["is_national"] is True

    def test_set_field_append_to_list(self, temp_dir, monkeypatch):
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [self._valid_record("reca")])
        result = runner.invoke(
            builder.app,
            ["set-field", "--id", "reca", "--path", "tags", "--value", "transport", "--append"],
        )
        assert result.exit_code == 0, result.output
        result = runner.invoke(
            builder.app,
            ["set-field", "--id", "reca", "--path", "tags", "--value", "health", "--append"],
        )
        assert result.exit_code == 0, result.output
        with open(paths["reca"], encoding="utf8") as f:
            record = yaml.safe_load(f)
        assert record["tags"] == ["transport", "health"]

    def test_set_field_refuses_uid_and_id(self, temp_dir, monkeypatch):
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [self._valid_record("reca")])
        original = open(paths["reca"], encoding="utf8").read()
        for field in ("uid", "id"):
            result = runner.invoke(
                builder.app,
                ["set-field", "--id", "reca", "--path", field, "--value", "x"],
            )
            assert result.exit_code == 1
            assert "Refusing" in result.output
        assert open(paths["reca"], encoding="utf8").read() == original

    def test_set_field_schema_refusal_leaves_file_unchanged(self, temp_dir, monkeypatch):
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [self._valid_record("reca")])
        original = open(paths["reca"], encoding="utf8").read()
        result = runner.invoke(
            builder.app,
            ["set-field", "--id", "reca", "--path", "catalog_type", "--value", "Bogus type"],
        )
        assert result.exit_code == 1
        assert "invalid" in result.output.lower()
        assert open(paths["reca"], encoding="utf8").read() == original

    def test_set_field_unknown_id(self, temp_dir, monkeypatch):
        builder, runner, _ = self._setup(temp_dir, monkeypatch, [])
        result = runner.invoke(
            builder.app,
            ["set-field", "--id", "nosuchrec", "--path", "name", "--value", "X"],
        )
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_enrich_batch_dry_run_then_write(self, temp_dir, monkeypatch):
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [self._valid_record("reca")])
        manifest = os.path.join(temp_dir, "updates.jsonl")
        with open(manifest, "w", encoding="utf8") as f:
            f.write(json.dumps({"id": "reca", "set": {"properties.is_national": True}}) + "\n")

        original = open(paths["reca"], encoding="utf8").read()
        result = runner.invoke(builder.app, ["enrich-batch", manifest])
        assert result.exit_code == 0, result.output
        assert "would update: 1" in result.output
        assert "is_national" in result.output
        assert open(paths["reca"], encoding="utf8").read() == original  # dry-run wrote nothing

        result = runner.invoke(builder.app, ["enrich-batch", manifest, "--write"])
        assert result.exit_code == 0, result.output
        assert "updated: 1" in result.output
        with open(paths["reca"], encoding="utf8") as f:
            assert yaml.safe_load(f)["properties"]["is_national"] is True

    def test_enrich_batch_merge_deep_merges(self, temp_dir, monkeypatch):
        record = self._valid_record("reca")
        record["properties"] = {"is_national": True}
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [record])
        manifest = os.path.join(temp_dir, "updates.jsonl")
        with open(manifest, "w", encoding="utf8") as f:
            f.write(json.dumps({"id": "reca", "merge": {"properties": {"has_doi": True}}}) + "\n")
        result = runner.invoke(builder.app, ["enrich-batch", manifest, "--write"])
        assert result.exit_code == 0, result.output
        with open(paths["reca"], encoding="utf8") as f:
            props = yaml.safe_load(f)["properties"]
        assert props == {"is_national": True, "has_doi": True}

    def test_enrich_batch_unknown_id_and_invalid_rows(self, temp_dir, monkeypatch):
        builder, runner, paths = self._setup(temp_dir, monkeypatch, [self._valid_record("reca")])
        manifest = os.path.join(temp_dir, "updates.jsonl")
        with open(manifest, "w", encoding="utf8") as f:
            f.write(json.dumps({"id": "ghost", "set": {"name": "X"}}) + "\n")
            f.write(json.dumps({"id": "reca", "set": {"catalog_type": "Bogus"}}) + "\n")
            f.write(json.dumps({"id": "reca", "merge": {"uid": "cdi99999999"}}) + "\n")
        result = runner.invoke(builder.app, ["enrich-batch", manifest, "--write"])
        assert result.exit_code == 0, result.output
        assert "skipped (unknown id): 1" in result.output
        assert "invalid: 2" in result.output
        with open(paths["reca"], encoding="utf8") as f:
            record = yaml.safe_load(f)
        assert record["catalog_type"] == "Open data portal"
        assert record["uid"] == "cdi00000001"


class TestValidationHelpers:
    """schema-values command and validate-yaml --changed."""

    def _runner(self):
        from typer.testing import CliRunner

        return CliRunner()

    def test_schema_values_enum_fields(self):
        import builder

        runner = self._runner()
        result = runner.invoke(builder.app, ["schema-values", "catalog_type"])
        assert result.exit_code == 0
        assert "Open data portal" in result.output
        assert "Geoportal" in result.output

        result = runner.invoke(builder.app, ["schema-values", "status"])
        assert "active" in result.output and "deprecated" in result.output

        result = runner.invoke(builder.app, ["schema-values", "access_mode"])
        assert "open" in result.output and "restricted" in result.output

    def test_schema_values_owner_type(self):
        import builder

        result = self._runner().invoke(builder.app, ["schema-values", "owner.type"])
        assert result.exit_code == 0
        assert "Central government" in result.output

    def test_schema_values_langs(self):
        import builder

        result = self._runner().invoke(builder.app, ["schema-values", "langs"])
        assert result.exit_code == 0
        assert "IT\tItalian" in result.output

    def test_schema_values_subregion_country_filter(self):
        import builder

        result = self._runner().invoke(
            builder.app, ["schema-values", "owner.location.subregion", "--country", "US"]
        )
        assert result.exit_code == 0
        assert "US-CA" in result.output
        assert "PT-08" not in result.output

    def test_schema_values_software_id(self):
        import builder

        result = self._runner().invoke(builder.app, ["schema-values", "software.id"])
        assert result.exit_code == 0
        assert "ckan" in result.output

    def test_schema_values_unknown_field(self):
        import builder

        result = self._runner().invoke(builder.app, ["schema-values", "bogus.field"])
        assert result.exit_code == 1
        assert "Supported fields" in result.output
        assert "catalog_type" in result.output

    def _write_yaml(self, temp_dir, name, text):
        path = os.path.join(temp_dir, name)
        with open(path, "w", encoding="utf8") as f:
            f.write(text)
        return path

    def test_validate_changed_only_touched_files(self, temp_dir, monkeypatch, caplog):
        import builder
        import logging

        caplog.set_level(logging.ERROR)

        valid = self._write_yaml(
            temp_dir,
            "valid.yaml",
            "id: validrec\n"
            "uid: cdi00000001\n"
            "name: Valid\n"
            "link: https://example.com\n"
            "catalog_type: Open data portal\n"
            "access_mode:\n  - open\n"
            "status: active\n"
            "software:\n  id: custom\n  name: Custom\n"
            "owner:\n"
            "  name: Owner\n"
            "  type: Central government\n"
            "  location:\n    country:\n      id: US\n      name: United States\n",
        )
        invalid = self._write_yaml(temp_dir, "invalid.yaml", "id: brokenrec\nname: Missing fields\n")
        other = self._write_yaml(temp_dir, "other.yaml", "id: otherrec\n")

        monkeypatch.setattr(builder, "_git_changed_yaml_files", lambda: [valid, invalid])
        result = self._runner().invoke(builder.app, ["validate-yaml", "--changed"])
        assert result.exit_code == 0, result.output
        assert "Total files: 2" in result.output
        assert "Valid: 1" in result.output
        assert "Errors: 1" in result.output
        # per-file errors are reported via the logger
        assert "invalid.yaml" in caplog.text
        assert "other.yaml" not in result.output
        assert "other.yaml" not in caplog.text

    def test_validate_changed_none_changed(self, temp_dir, monkeypatch):
        import builder

        monkeypatch.setattr(builder, "_git_changed_yaml_files", lambda: [])
        result = self._runner().invoke(builder.app, ["validate-yaml", "--changed"])
        assert result.exit_code == 0
        assert "No changed YAML files" in result.output

    def test_validate_changed_exclusive_with_file_and_id(self):
        import builder

        runner = self._runner()
        result = runner.invoke(builder.app, ["validate-yaml", "--changed", "--id", "x"])
        assert result.exit_code == 1
        assert "cannot be combined" in result.output
        result = runner.invoke(builder.app, ["validate-yaml", "--changed", "--file", "x.yaml"])
        assert result.exit_code == 1


class TestSoftwareMap:
    """Quality checks should read software IDs from YAML definitions."""

    def test_includes_yaml_definitions(self):
        import builder

        builder._software_map_cache = None
        software_map = builder.get_software_map()
        assert "geoclip" in software_map
        assert software_map["geoclip"]["name"] == "Géoclip"
        assert "ckan" in software_map
        assert "opendataente" in software_map


class TestCreateTableFromJsonl:
    """DuckDB export must keep LIST and STRUCT types instead of VARCHAR JSON."""

    def _write_jsonl(self, directory, filename, records):
        path = os.path.join(directory, filename)
        with open(path, "w", encoding="utf8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path

    def test_jsonl_has_records(self, temp_dir):
        empty_path = os.path.join(temp_dir, "empty.jsonl")
        with open(empty_path, "w", encoding="utf8"):
            pass
        assert jsonl_has_records(empty_path) is False
        assert jsonl_has_records(os.path.join(temp_dir, "missing.jsonl")) is False

        filled_path = self._write_jsonl(
            temp_dir, "filled.jsonl", [{"id": "one"}]
        )
        assert jsonl_has_records(filled_path) is True

    def test_preserves_list_and_struct_types(self, temp_dir):
        import duckdb

        jsonl_path = self._write_jsonl(
            temp_dir,
            "catalogs.jsonl",
            [
                {
                    "id": "portalus",
                    "api": True,
                    "access_mode": ["open"],
                    "tags": ["government", "ckan"],
                    "software": {"id": "ckan", "name": "CKAN"},
                    "owner": {"name": "Example Agency", "type": "Central government"},
                    "coverage": [
                        {
                            "location": {
                                "country": {"id": "US", "name": "United States"},
                                "level": 20,
                            }
                        }
                    ],
                    "identifiers": [
                        {"id": "wikidata", "value": "Q1"},
                        {"id": "re3data", "value": "r3d100000001"},
                    ],
                    "endpoints": [
                        {"type": "ckan", "url": "https://example.gov/api/3"}
                    ],
                },
                {
                    "id": "portalfr",
                    "api": False,
                    "access_mode": ["open", "restricted"],
                    "tags": ["opendata"],
                    "software": {"id": "ckan", "name": "CKAN"},
                    "owner": {"name": "Ministère", "type": "Central government"},
                    "coverage": [
                        {
                            "location": {
                                "country": {"id": "FR", "name": "France"},
                                "level": 20,
                            }
                        }
                    ],
                },
            ],
        )

        conn = duckdb.connect(os.path.join(temp_dir, "test.duckdb"))
        count = create_table_from_jsonl(conn, "catalogs", jsonl_path)
        assert count == 2

        types = {
            row[0]: row[1]
            for row in conn.execute("DESCRIBE catalogs").fetchall()
        }
        assert types["access_mode"].startswith("VARCHAR")
        assert "[]" in types["access_mode"]
        assert types["tags"].startswith("VARCHAR")
        assert "[]" in types["tags"]
        assert types["software"].startswith("STRUCT")
        assert types["owner"].startswith("STRUCT")
        assert types["coverage"].startswith("STRUCT")
        assert types["coverage"].endswith("[]")
        assert types["identifiers"].startswith("STRUCT")
        assert types["api"] == "BOOLEAN"

        row = conn.execute(
            """
            SELECT id, software.id, owner.type,
                   list_contains(tags, 'government'),
                   list_contains(
                       list_transform(coverage, x -> x.location.country.id),
                       'US'
                   ),
                   list_contains(
                       list_transform(identifiers, x -> x.id),
                       'wikidata'
                   )
            FROM catalogs
            WHERE software.id = 'ckan'
              AND list_contains(
                  list_transform(coverage, x -> x.location.country.id),
                  'US'
              )
            """
        ).fetchone()
        assert row[0] == "portalus"
        assert row[1] == "ckan"
        assert row[2] == "Central government"
        assert row[3] is True
        assert row[4] is True
        assert row[5] is True
        conn.close()

    def test_skips_empty_jsonl(self, temp_dir):
        import duckdb

        empty_path = os.path.join(temp_dir, "empty.jsonl")
        with open(empty_path, "w", encoding="utf8"):
            pass
        conn = duckdb.connect(os.path.join(temp_dir, "empty.duckdb"))
        count = create_table_from_jsonl(conn, "catalogs", empty_path)
        assert count == 0
        tables = [
            row[0]
            for row in conn.execute("SHOW TABLES").fetchall()
        ]
        assert "catalogs" not in tables
        conn.close()

    def test_rejects_invalid_table_name(self, temp_dir):
        import duckdb

        jsonl_path = self._write_jsonl(temp_dir, "ok.jsonl", [{"id": "one"}])
        conn = duckdb.connect(":memory:")
        with pytest.raises(ValueError, match="Invalid DuckDB table name"):
            create_table_from_jsonl(conn, "catalogs; DROP TABLE catalogs", jsonl_path)
        conn.close()
