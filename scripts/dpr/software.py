"""Software definition helpers shared by the registry scripts."""

import logging
from pathlib import Path
from typing import Dict

import yaml

logger = logging.getLogger(__name__)

SOFTWARE_DIR = Path(__file__).resolve().parents[2] / "data" / "software"


def load_software_definitions(software_dir: Path = SOFTWARE_DIR) -> Dict[str, Dict]:
    """Return {software id: {"id", "name"}} for every YAML file under software_dir.

    A file that cannot be parsed is logged and skipped.
    """
    software = {}
    for software_file in Path(software_dir).rglob("*.yaml"):
        try:
            with open(software_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data and "id" in data:
                software[data["id"]] = {"id": data["id"], "name": data.get("name", "")}
        except Exception as e:
            logger.warning("Error loading %s: %s", software_file, e)
    return software
