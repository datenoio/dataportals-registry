"""Quality-report readers shared by the registry scripts."""

import json
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def read_jsonl_issues(file_path) -> List[Dict[str, Any]]:
    """Return the records of a quality-issues JSONL file that list at least one issue.

    A missing file is logged and yields an empty list. A line that is not
    valid JSON is logged and skipped.
    """
    records = []
    if not os.path.exists(file_path):
        logger.error("Error: File not found: %s", file_path)
        return records
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as e:
                    logger.warning("Failed to parse JSON at line %d: %s", line_num, e)
                    continue
                if record.get("issues", []):
                    records.append(record)
    except Exception as e:
        logger.error("Error reading file %s: %s", file_path, e)
    return records
