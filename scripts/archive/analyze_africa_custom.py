#!/usr/bin/env python3
"""One-off analysis: Africa-owned catalogs with software=custom.

Scans data/entities for entries whose software.id == 'custom' and whose
owner.location.country.id is an African country. Groups them by domain and
by detected platform hints to surface repeating patterns that could justify
new software definitions.
"""
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "data" / "entities"

AFRICA = {
    "DZ", "AO", "BJ", "BW", "BF", "BI", "CV", "CM", "CF", "TD", "KM", "CG",
    "CD", "CI", "DJ", "EG", "GQ", "ER", "SZ", "ET", "GA", "GM", "GH", "GN",
    "GW", "KE", "LS", "LR", "LY", "MG", "MW", "ML", "MR", "MU", "MA", "MZ",
    "NA", "NE", "NG", "RW", "ST", "SN", "SC", "SL", "SO", "ZA", "SS", "SD",
    "TZ", "TG", "TN", "UG", "ZM", "ZW", "EH",
}

# Known existing software ids/names (lowercase) used to flag obvious misses
SOFTWARE_DIR = ROOT / "data" / "software"


def load_existing_software():
    ids = set()
    names = set()
    for f in SOFTWARE_DIR.rglob("*.yaml"):
        try:
            d = yaml.safe_load(f.read_text())
        except Exception:
            continue
        if isinstance(d, dict):
            if d.get("id"):
                ids.add(str(d["id"]).lower())
            if d.get("name"):
                names.add(str(d["name"]).lower())
    return ids, names


def domain_of(url):
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return ""
    host = host.split(":")[0]
    return host


def detect_hints(entry):
    """Return list of platform hints found in text fields/URLs."""
    text_parts = [
        entry.get("name", "") or "",
        entry.get("description", "") or "",
    ]
    link = entry.get("link", "") or ""
    text_parts.append(link)
    for ep in entry.get("endpoints") or []:
        if isinstance(ep, dict):
            text_parts.append(str(ep.get("url", "")))
            text_parts.append(str(ep.get("type", "")))
    text = " ".join(text_parts).lower()

    hints = []
    patterns = {
        "geonode": r"geonode",
        "geoserver": r"geoserver",
        "geowebcache": r"geowebcache",
        "arcgis": r"arcgis|arcgisonline|hub\.arcgis|storymaps?\.arcgis|experience\.arcgis",
        "ckan": r"ckan|/api/3/action|/dataset/",
        "dspace": r"dspace|oai/request",
        "eprints": r"eprints",
        "fedora/islandora": r"islandora|fedora",
        "invenio/zenodo-like": r"invenio",
        "wordpress": r"wordpress|wp-content|wp-json",
        "joomla": r"joomla",
        "drupal": r"drupal",
        "moodle": r"moodle",
        "koha": r"koha",
        "geoportal_server": r"geoportal server|esri geoportal",
        "geonetwork": r"geonetwork",
        "deegree": r"deegree",
        "thredds": r"thredds",
        "ihs/ipt (gbif)": r"/ipt/",
        "dhis2": r"dhis2",
        "odk/ona": r"ona\.io|opendatakit|getodk",
        "kobo": r"kobotoolbox|kobo\.humanitarian",
        "datahub(.io/oss)": r"datahub",
        "opendatasoft": r"opendatasoft|explore/dataset",
        "socrata": r"socrata|/api/1/metastore",
        "grafana": r"grafana",
        "ckantoolkit/ckanext": r"ckanext",
        "nuxt/next custom": r"\b(react|next\.js|nuxt|vue)\b",
        "tableau": r"tableau",
        "powerbi": r"powerbi|app\.powerbi",
        "metabase": r"metabase",
        "redash": r"redash",
        "superset": r"superset",
        "geonetwork-un": r"geonetwork",
        "mapstore": r"mapstore",
        "openlayers/leaflet": r"openlayers|leaflet",
        "csw server": r"\bcsw\b",
        "wms/wfs server": r"\bwms\b|\bwfs\b",
        "postgres/postgis api": r"postgis",
        "django": r"django",
        "angular": r"angular",
    }
    for name, pat in patterns.items():
        if re.search(pat, text):
            hints.append(name)
    return hints


def main():
    existing_ids, existing_names = load_existing_software()
    print(f"Existing software definitions: {len(existing_ids)} ids")

    rows = []
    for f in ENTITIES.rglob("*.yaml"):
        try:
            d = yaml.safe_load(f.read_text())
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        sw = d.get("software") or {}
        if str(sw.get("id", "")).lower() != "custom":
            continue
        owner = d.get("owner") or {}
        loc = (owner.get("location") or {})
        cc = ((loc.get("country") or {}).get("id") or "").upper()
        if cc not in AFRICA:
            continue
        rows.append({
            "file": str(f.relative_to(ROOT)),
            "id": d.get("id"),
            "name": d.get("name"),
            "link": d.get("link"),
            "domain": domain_of(d.get("link", "")),
            "catalog_type": d.get("catalog_type"),
            "country": cc,
            "owner_name": owner.get("name"),
            "endpoints": d.get("endpoints") or [],
            "description": d.get("description", "") or "",
            "tags": d.get("tags") or [],
            "hints": detect_hints(d),
            "status": d.get("status"),
        })

    print(f"Africa-owned custom-software catalogs: {len(rows)}\n")

    # Summary by country and catalog type
    print("== By country ==")
    for cc, n in Counter(r["country"] for r in rows).most_common():
        print(f"  {cc}: {n}")
    print("\n== By catalog type ==")
    for ct, n in Counter(r["catalog_type"] for r in rows).most_common():
        print(f"  {ct}: {n}")
    print("\n== By status ==")
    for st, n in Counter(r["status"] for r in rows).most_common():
        print(f"  {st}: {n}")

    # Repeat domain patterns
    print("\n== Repeated registrable domains (>=2 catalogs) ==")
    dom_counter = Counter(r["domain"] for r in rows)
    for dom, n in dom_counter.most_common():
        if n >= 2:
            print(f"  {dom}: {n}")

    # Hint frequency
    print("\n== Platform hint frequency ==")
    hint_counter = Counter()
    for r in rows:
        for h in set(r["hints"]):
            hint_counter[h] += 1
    for h, n in hint_counter.most_common():
        already = " (already a software id)" if h.lower() in existing_ids else ""
        print(f"  {h}: {n}{already}")

    # Dump details per entry for manual review
    out = ROOT / "devdocs" / "africa_custom_analysis.json"
    import json
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"\nDetails written to {out}")

    # Per-hint, list entries with that hint as ONLY hint or strong hint
    print("\n== Entries per strong hint (first 60) ==")
    by_hint = defaultdict(list)
    for r in rows:
        for h in set(r["hints"]):
            by_hint[h].append(r)
    for h in sorted(by_hint, key=lambda k: -len(by_hint[k])):
        print(f"\n--- {h} ({len(by_hint[h])}) ---")
        for r in by_hint[h][:15]:
            print(f"  {r['country']}  {r['id']:40s} {r['domain']:40s} {r['catalog_type']}")
        if len(by_hint[h]) > 15:
            print(f"  ... and {len(by_hint[h]) - 15} more")


if __name__ == "__main__":
    main()
