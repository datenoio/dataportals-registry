"""Registry YAML must be parsed with a safe loader.

Catalog YAML comes from outside contributors and CI validates it on every pull
request. PyYAML's full loaders run code from tags such as
``!!python/object/apply``, so every script takes ``Loader`` and ``Dumper``
from ``scripts/dpr/yaml_io.py``.
"""

import ast
import json
from pathlib import Path

import pytest
import yaml


from dpr import yaml_io  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "data" / "schemes" / "catalog.json"

# PyYAML names that construct arbitrary Python objects, or emit tags only
# those loaders accept.
UNSAFE_YAML_NAMES = {
    "Loader",
    "CLoader",
    "FullLoader",
    "CFullLoader",
    "UnsafeLoader",
    "CUnsafeLoader",
    "Dumper",
    "CDumper",
    "unsafe_load",
    "unsafe_load_all",
    "full_load",
    "full_load_all",
}


def _python_sources():
    paths = sorted((REPO_ROOT / "scripts").rglob("*.py"))
    paths += sorted((REPO_ROOT / "tests").glob("*.py"))
    return [p for p in paths if p.name != "yaml_io.py"]


def _unsafe_yaml_uses(path: Path):
    tree = ast.parse(path.read_bytes().decode("utf-8"), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "yaml":
            found += [
                f"line {node.lineno}: from yaml import {alias.name}"
                for alias in node.names
                if alias.name in UNSAFE_YAML_NAMES
            ]
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "yaml"
            and node.attr in UNSAFE_YAML_NAMES
        ):
            found.append(f"line {node.lineno}: yaml.{node.attr}")
    return found


@pytest.mark.unit
def test_yaml_io_exports_safe_classes():
    assert issubclass(yaml_io.Loader, yaml.constructor.SafeConstructor)
    assert not issubclass(yaml_io.Loader, yaml.constructor.FullConstructor)
    assert issubclass(yaml_io.Dumper, yaml.representer.SafeRepresenter)
    assert not issubclass(yaml_io.Dumper, yaml.representer.Representer)


@pytest.mark.unit
def test_yaml_io_loader_rejects_python_tags():
    with pytest.raises(yaml.constructor.ConstructorError):
        yaml.load("x: !!python/object/apply:os.getcwd []", Loader=yaml_io.Loader)


@pytest.mark.unit
def test_yaml_io_round_trips_registry_types():
    record = {
        "id": "x",
        "tags": ["a", "b"],
        "api": True,
        "level": 20,
        "date": "2026-01-01",
    }
    text = yaml.dump(record, Dumper=yaml_io.Dumper, allow_unicode=True, sort_keys=False)
    assert yaml.load(text, Loader=yaml_io.Loader) == record


@pytest.mark.unit
@pytest.mark.parametrize(
    "path", _python_sources(), ids=lambda p: str(p.relative_to(REPO_ROOT))
)
def test_no_unsafe_yaml_loader(path):
    uses = _unsafe_yaml_uses(path)
    assert not uses, (
        f"{path.relative_to(REPO_ROOT)} uses an unsafe PyYAML loader or dumper: "
        f"{uses}. Import Loader and Dumper from dpr.yaml_io instead."
    )


@pytest.mark.unit
def test_validate_yaml_reports_python_tag_without_running_it(tmp_path):
    from cerberus import Validator

    import builder

    marker = tmp_path / "marker"
    payload = tmp_path / "evil.yaml"
    # An unsafe loader calls os.mkdir(marker) while parsing this file.
    payload.write_text(
        f"id: evil\nname: !!python/object/apply:os.mkdir [{json.dumps(str(marker))}]\n",
        encoding="utf-8",
    )
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    errors, total, valid = builder._validate_yaml_files(
        [str(payload)], schema, Validator(schema)
    )

    assert not marker.exists()
    assert (total, valid) == (1, 0)
    assert len(errors) == 1
    assert "YAML parsing error" in errors[0][1]
