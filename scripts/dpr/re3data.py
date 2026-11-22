"""re3data helpers shared by the registry scripts."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import yaml
from requests.exceptions import RequestException, Timeout

from dpr.yaml_io import Loader

logger = logging.getLogger(__name__)

RE3DATA_BASE_URL = "https://www.re3data.org"
ENTITIES_DIR = str(Path(__file__).resolve().parents[2] / "data" / "entities")


def get_re3data_identifier(catalog: Dict[str, Any]) -> Optional[str]:
    """Return the re3data identifier of a catalog record, or None."""
    for identifier in catalog.get("identifiers", []):
        if isinstance(identifier, dict) and identifier.get("id") == "re3data":
            return identifier.get("value")
    return None


def get_re3data_url(re3data_id: str) -> str:
    """Return the re3data.org page URL for a re3data identifier."""
    return f"{RE3DATA_BASE_URL}/repository/{re3data_id}"


def fetch_re3data_page(re3data_id: str, timeout: int = 10) -> Optional[str]:
    """Fetch the re3data.org repository page HTML, or None on a request error."""
    url = get_re3data_url(re3data_id)
    try:
        response = requests.get(
            url,
            timeout=timeout,
            verify=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; dataportals-registry/1.0)"},
        )
        response.raise_for_status()
        return response.text
    except (RequestException, Timeout) as e:
        logger.warning("Could not fetch re3data page for %s: %s", re3data_id, e)
        return None


def collect_re3data_identifiers(root_dir: str = ENTITIES_DIR) -> Dict[str, str]:
    """Return {re3data identifier: YAML file path} for every catalog under root_dir."""
    re3data_ids = {}
    logger.info("Collecting re3data identifiers from catalogs...")
    for root, _dirs, files in os.walk(root_dir):
        for name in files:
            if not name.endswith(".yaml"):
                continue
            filepath = os.path.join(root, name)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    catalog = yaml.load(f, Loader=Loader)
                if not catalog:
                    continue
                re3data_id = get_re3data_identifier(catalog)
                if re3data_id:
                    re3data_ids[re3data_id] = filepath
            except Exception as e:
                logger.debug("Error reading %s: %s", filepath, e)
    logger.info("Found %d catalogs with re3data identifiers", len(re3data_ids))
    return re3data_ids
