"""Safe YAML loader and dumper classes for the registry scripts.

Catalog YAML comes from outside contributors, and CI parses it on every pull
request. PyYAML's full loaders (``yaml.Loader``, ``yaml.CLoader``,
``yaml.FullLoader``, ``yaml.UnsafeLoader``) build Python objects from tags
such as ``!!python/object/apply:os.system``, so parsing a crafted file with
them runs code. Import ``Loader`` and ``Dumper`` from this module instead of
from ``yaml``::

    from dpr.yaml_io import Loader, Dumper

    record = yaml.load(handle, Loader=Loader)

Both names are the libyaml (C) safe classes when PyYAML was built with
libyaml, and the pure-Python safe classes otherwise.
``tests/test_yaml_safety.py`` fails if a script imports an unsafe loader.
"""

try:
    from yaml import CSafeDumper as Dumper
    from yaml import CSafeLoader as Loader
except ImportError:  # PyYAML built without libyaml
    from yaml import SafeDumper as Dumper
    from yaml import SafeLoader as Loader

__all__ = ["Dumper", "Loader"]
