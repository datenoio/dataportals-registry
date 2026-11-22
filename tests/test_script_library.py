"""Guards for the shared script library (openspec: refactor-shared-script-library).

- A helper used by two scripts lives once, in scripts/dpr/.
- Scripts and tests do not edit sys.path; pytest.ini sets ``pythonpath``.

scripts/archive/ is exempt: archived scripts are not maintained.
"""

import ast
from collections import defaultdict
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# Names that are still defined in more than one active script, with the reason.
# Remove an entry when its duplicates are gone: the test fails on stale entries.
DUPLICATE_ALLOWLIST = {
    "main": "Entry-point name of each script, not a shared helper.",
    "report": "Typer command name in apidetect.py and builder.py, not a shared helper.",
    "_probe_one": (
        "apidetect.py returns endpoints, hunt.py returns a probe verdict; "
        "merging them needs its own design."
    ),
    "fix_yaml_file": "Replaced by apply-fixes (openspec: add-deterministic-fix-rules).",
    "fix_owner_link": "Replaced by apply-fixes (openspec: add-deterministic-fix-rules).",
    "parse_report_file": "Replaced by apply-fixes (openspec: add-deterministic-fix-rules).",
}


def _library_and_scripts():
    return sorted(SCRIPTS.glob("*.py")) + sorted((SCRIPTS / "dpr").glob("*.py"))


def _checked_sources():
    return _library_and_scripts() + sorted((REPO_ROOT / "tests").glob("*.py"))


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_bytes().decode("utf-8"), filename=str(path))


def _module_level_functions():
    defined = defaultdict(list)
    for path in _library_and_scripts():
        for node in _parse(path).body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined[node.name].append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")
    return defined


@pytest.mark.unit
def test_no_new_duplicate_helpers():
    duplicates = {
        name: places
        for name, places in _module_level_functions().items()
        if len(places) > 1 and name not in DUPLICATE_ALLOWLIST
    }
    assert not duplicates, (
        "These functions are defined in more than one script. Move the helper to "
        f"scripts/dpr/ and import it: {duplicates}"
    )


@pytest.mark.unit
def test_duplicate_allowlist_has_no_stale_entries():
    defined = _module_level_functions()
    stale = sorted(name for name in DUPLICATE_ALLOWLIST if len(defined.get(name, [])) < 2)
    assert not stale, f"Remove these names from DUPLICATE_ALLOWLIST, they are no longer duplicated: {stale}"


@pytest.mark.unit
@pytest.mark.parametrize("path", _checked_sources(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_no_sys_path_manipulation(path):
    calls = [
        node.lineno
        for node in ast.walk(_parse(path))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"insert", "append"}
        and isinstance(node.func.value, ast.Attribute)
        and node.func.value.attr == "path"
        and isinstance(node.func.value.value, ast.Name)
        and node.func.value.value.id == "sys"
    ]
    assert not calls, (
        f"{path.relative_to(REPO_ROOT)} changes sys.path on lines {calls}. Scripts run with "
        "scripts/ on their path, and pytest.ini sets pythonpath = scripts."
    )


# Entry points that keep their own CLI and print() until apply-fixes replaces
# them (openspec: add-deterministic-fix-rules).
ENTRY_POINT_EXEMPT = {
    "fix_all_priority_issues.py",
    "fix_api_status_mismatch.py",
    "fix_catalog_software_mismatch.py",
    "fix_critical_issues.py",
    "fix_duplicate_tags.py",
    "fix_es_unk_subregions.py",
    "fix_important_issues.py",
    "fix_is_national_flags.py",
    "fix_low_issues.py",
    "fix_medium_issues.py",
    "fix_software_id.py",
    "fix_tag_hygiene.py",
}


def _is_entry_point(tree: ast.Module) -> bool:
    for node in tree.body:
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
        ):
            return True
    return False


def _entry_points():
    return [
        p
        for p in sorted(SCRIPTS.glob("*.py"))
        if p.name not in ENTRY_POINT_EXEMPT and _is_entry_point(_parse(p))
    ]


@pytest.mark.unit
@pytest.mark.parametrize("path", _entry_points(), ids=lambda p: p.name)
def test_entry_point_uses_typer(path):
    source = path.read_bytes().decode("utf-8")
    assert "import typer" in source, (
        f"{path.name} is run from the command line but does not use typer; "
        "define its CLI with typer and keep the existing option names."
    )


@pytest.mark.unit
@pytest.mark.parametrize("path", _library_and_scripts(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_no_print_calls(path):
    if path.name in ENTRY_POINT_EXEMPT:
        pytest.skip("replaced by apply-fixes")
    lines = [
        node.lineno
        for node in ast.walk(_parse(path))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print"
    ]
    assert not lines, (
        f"{path.relative_to(REPO_ROOT)} calls print() on lines {lines}. Use logging for "
        "progress and diagnostics, and typer.echo for the command's output."
    )


@pytest.mark.unit
def test_entry_point_exemptions_are_current():
    missing = sorted(name for name in ENTRY_POINT_EXEMPT if not (SCRIPTS / name).exists())
    assert not missing, f"Remove these deleted scripts from ENTRY_POINT_EXEMPT: {missing}"
