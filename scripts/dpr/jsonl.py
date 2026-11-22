"""JSONL and delimited-file readers shared by the registry scripts."""

import csv
import json


def load_jsonl(filepath):
    """Return the records of a JSONL file as a list of dicts."""
    data = []
    with open(filepath, "r", encoding="utf8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def load_csv_dict(filepath, key, delimiter="\t"):
    """Return the rows of a delimited file as {row[key]: row}.

    The default delimiter is a tab: the reference tables in data/reference/
    are tab-separated, whatever their extension.
    """
    data = {}
    with open(filepath, "r", encoding="utf8") as f:
        for row in csv.DictReader(f, delimiter=delimiter):
            data[row[key]] = row
    return data
