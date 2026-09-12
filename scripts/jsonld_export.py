#!/usr/bin/env python3
"""Export catalog JSONL records as JSON-LD using catalog.context.jsonld."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Optional

import zstandard as zstd

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTEXT_PATH = REPO_ROOT / "data" / "schemes" / "catalog.context.jsonld"
DEFAULT_JSONL = REPO_ROOT / "data" / "datasets" / "catalogs.jsonl"
DEFAULT_INPUT = REPO_ROOT / "data" / "datasets" / "catalogs.jsonl.zst"
DEFAULT_OUTPUT = REPO_ROOT / "data" / "datasets" / "catalogs.jsonld"


def resolve_catalogs_input(input_path: Optional[Path] = None) -> Path:
    """Prefer uncompressed catalogs.jsonl when present, else the .zst export."""
    if input_path is not None:
        return input_path
    if DEFAULT_JSONL.exists():
        return DEFAULT_JSONL
    return DEFAULT_INPUT


def iter_jsonl_records(input_path: Path) -> Iterator[dict]:
    """Yield JSON objects from uncompressed JSONL or JSONL.zst."""
    if "".join(input_path.suffixes).endswith(".jsonl.zst") or input_path.suffix == ".zst":
        dctx = zstd.ZstdDecompressor()
        with input_path.open("rb") as handle:
            with dctx.stream_reader(handle) as reader:
                text_stream = reader.read().decode("utf-8")
        for line in text_stream.splitlines():
            if line.strip():
                yield json.loads(line)
        return
    with input_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def load_context() -> dict:
    with CONTEXT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def record_to_jsonld(record: dict, context_document: dict) -> dict:
    """Frame a catalog record with JSON-LD @context and @type."""
    framed = dict(record)
    framed["@context"] = context_document["@context"]
    framed["@type"] = "dcat:DataCatalog"
    uid = record.get("uid") or record.get("id")
    if uid:
        framed["@id"] = f"urn:cdi:catalog:{uid}"
    return framed


def export_catalogs_jsonld(
    input_path: Optional[Path] = None,
    output_path: Path = DEFAULT_OUTPUT,
    context_path: Path = CONTEXT_PATH,
) -> int:
    """Write JSON-LD export; returns number of records exported."""
    with context_path.open("r", encoding="utf-8") as handle:
        context_document = json.load(handle)

    source_path = resolve_catalogs_input(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as dst:
        for record in iter_jsonl_records(source_path):
            dst.write(
                json.dumps(
                    record_to_jsonld(record, context_document),
                    ensure_ascii=False,
                )
                + "\n"
            )
            count += 1
    return count
