"""re3data helpers shared by the registry scripts."""

from typing import Any, Dict, Optional


def get_re3data_identifier(catalog: Dict[str, Any]) -> Optional[str]:
    """Return the re3data identifier of a catalog record, or None."""
    for identifier in catalog.get("identifiers", []):
        if isinstance(identifier, dict) and identifier.get("id") == "re3data":
            return identifier.get("value")
    return None
