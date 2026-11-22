"""Helpers shared by the registry scripts in ``scripts/``.

A helper that two or more scripts use belongs here, not in a script.
``tests/test_script_library.py`` fails when two scripts define the same
module-level function.

Scripts run as ``python scripts/<name>.py`` have ``scripts/`` on their import
path, and pytest adds it through ``pythonpath = scripts`` in ``pytest.ini``,
so ``import dpr`` works in both without changing ``sys.path``.

Modules:

- ``dpr.yaml_io``: safe YAML ``Loader`` and ``Dumper``
- ``dpr.urls``: URL canonicalization and host helpers
- ``dpr.jsonl``: JSONL and delimited-file readers
- ``dpr.software``: software definition loading
- ``dpr.re3data``: re3data identifier helpers
- ``dpr.reports``: quality-report helpers
"""
