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
    "infer_country_from_link": "Diverged copies; unify in dpr.geo (task 3.1).",
    "read_jsonl_issues": "Diverged copies; unify in dpr.reports (task 3.2).",
    "fetch_re3data_page": "Diverged copies; unify in dpr.re3data (task 3.3).",
    "get_re3data_url": "Diverged copies; unify in dpr.re3data (task 3.3).",
    "collect_re3data_identifiers": "Diverged copies; unify in dpr.re3data (task 3.3).",
    "_iter_yaml_files": "Diverged copies; unify in dpr (task 3.5).",
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
