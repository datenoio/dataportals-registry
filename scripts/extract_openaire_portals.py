#!/usr/bin/env python
"""Extract data portals registered as OpenAIRE Graph data sources.

Uses the Graph v3 data-sources API (not HTML scrape). Filters to data-relevant
typologies and drops publication-only institutional repositories. Duplicate-
checks registry hosts in DuckDB, then can add misses under data/scheduled/.

Usage:
  python scripts/extract_openaire_portals.py list-sources --output /tmp/openaire_sources.json
  python scripts/extract_openaire_portals.py match-registry --input /tmp/openaire_sources.json
  python scripts/extract_openaire_portals.py add-scheduled --input /tmp/openaire_misses.json --dry-run
"""

from __future__ import annotations

import copy
import html
import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urlparse

import requests
import typer
import yaml
from requests.exceptions import RequestException

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
from constants import COUNTRIES, DOMAIN_LOCATIONS, ENTRY_TEMPLATE  # noqa: E402

requests.packages.urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)

app = typer.Typer()

OPENAIRE_GRAPH_DATASOURCES = "https://api.openaire.eu/graph/v3/datasources"
OPENAIRE_GRAPH_PRODUCTS = "https://api.openaire.eu/graph/v3/research-products"
OPENAIRE_EXPLORE_DATAPROVIDER = (
    "https://explore.openaire.eu/search/dataprovider?datasourceId="
)
USER_AGENT = (
    "DataPortalsRegistry/1.0 (+https://github.com/datenoio/dataportals-registry)"
)

# Issue #41: keep dataprovider / repository / journal aggregator typologies.
DATA_PROVIDER_TYPES = frozenset(
    {
        "Data Repository",
        "Data Repository Aggregator",
    }
)
REPOSITORY_TYPES = frozenset(
    {
        "Repository",
        "Institutional Repository",
        "Thematic Repository",
        "Publication Repository",
    }
)
JOURNAL_AGGREGATOR_TYPES = frozenset(
    {
        "Journal Aggregator/Publisher",
    }
)
DEFAULT_TYPES = DATA_PROVIDER_TYPES | REPOSITORY_TYPES | JOURNAL_AGGREGATOR_TYPES

DATASET_CONTENT_TOKENS = frozenset(
    {
        "dataset",
        "datasets",
        "research data",
        "researchdata",
        "raw data",
        "database",
        "databases",
        "statistical data",
        "geospatial data",
        "image",
        "images",
        "audiovisual",
    }
)
PUBLICATION_CONTENT_TOKENS = frozenset(
    {
        "journal articles",
        "bibliographic references",
        "conference and workshop papers",
        "theses and dissertations",
        "unpublished reports and working papers",
        "books, chapters and sections",
        "books",
        "patents",
        "learning objects",
    }
)
DATA_COLLECTED_FROM = frozenset(
    {
        "registry of research data repository",
        "re3data",
        "fairsharing",
    }
)
DATA_COMPATIBILITY_IDS = frozenset(
    {
        "openaire2.0_data",
        "openaire3.0_data",
        "openaire4.0_data",
    }
)
DATA_NAME_URL_RE = re.compile(
    r"(dataverse|figshare|zenodo|dryad|pangaea|fairdata|datashare|"
    r"research[\s\-]?data|opendata|/dataverse|rdm\.|radar[\.\-/]|"
    r"dataset|datarepo|data-repository)",
    re.I,
)
SKIP_HOSTS = frozenset(
    {
        "localhost",
        "127.0.0.1",
        "example.com",
        "example.org",
        "example.net",
        "test.de",
        "test.com",
        "fairsharing.org",
        "www.fairsharing.org",
        "re3data.org",
        "www.re3data.org",
        "v2.sherpa.ac.uk",
        "doi.org",
        "dx.doi.org",
        "opendoar.org",
        "www.opendoar.org",
        "arxiv.org",
        "www.arxiv.org",
        "europepmc.org",
        "www.europepmc.org",
        "public.tableau.com",
        "tableau.com",
        "www.tableau.com",
    }
)
# Forges and encyclopedia pages are not catalogs (github.io sites can be).
SKIP_HOST_SUFFIXES = (
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "wikipedia.org",
    "google.com",
    "youtube.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "linkedin.com",
    "wikidata.org",
)
COUNTRY_ALIASES = {
    "UK": "GB",
    "EL": "GR",
    "UKR": "UA",
    "XK": "XK",
}

PAGE_SIZE = 100
REQUEST_DELAY = 0.2


def normalize_host(url: Optional[str]) -> str:
    """Return a lowercase hostname without www or port."""
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = (parsed.netloc or parsed.path.split("/")[0]).lower()
    host = host.split("@")[-1].split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return host.strip(".")


def catalog_id_from_url(url: str) -> str:
    """Builder-compatible catalog id from a URL host."""
    host = urlparse(url if "://" in url else f"https://{url}").netloc.lower()
    return host.split(":", 1)[0].replace("_", "").replace("-", "").replace(".", "")


def normalize_http_url(url: Optional[str]) -> Optional[str]:
    """Ensure an http(s) URL or return None."""
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if not url or url.lower() in {"null", "none", "n/a"}:
        return None
    if url.startswith("//"):
        url = "https:" + url
    if not url.startswith(("http://", "https://")):
        if "." not in url:
            return None
        url = "https://" + url
    parsed = urlparse(url)
    if not parsed.netloc or "." not in parsed.netloc:
        return None
    return url


def is_junk_url(url: Optional[str]) -> bool:
    """Skip placeholder, registry-of-registries, and non-catalog URLs."""
    host = normalize_host(url)
    if not host or host in SKIP_HOSTS:
        return True
    if host.endswith(".invalid") or host.endswith(".local"):
        return True
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
        return True
    if host in {"openaire.eu", "www.openaire.eu", "explore.openaire.eu", "api.openaire.eu"}:
        return True
    if any(host == suffix or host.endswith("." + suffix) for suffix in SKIP_HOST_SUFFIXES):
        return True
    return False


def unescape_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return html.unescape(value).replace("&amp;", "&").strip()


def typology_name(record: Dict[str, Any]) -> str:
    type_obj = record.get("type") or {}
    if isinstance(type_obj, dict):
        return (type_obj.get("value") or "").strip()
    return str(type_obj or "").strip()


def typology_scheme(record: Dict[str, Any]) -> str:
    type_obj = record.get("type") or {}
    if isinstance(type_obj, dict):
        return (type_obj.get("scheme") or "").strip()
    return ""


def collected_from_names(record: Dict[str, Any]) -> List[str]:
    names = []
    for item in record.get("collectedFrom") or []:
        if isinstance(item, dict):
            name = item.get("value") or item.get("key") or ""
            if name:
                names.append(str(name))
        elif item:
            names.append(str(item))
    return names


def content_type_list(record: Dict[str, Any]) -> List[str]:
    values = record.get("contentTypes") or record.get("contentType") or []
    if isinstance(values, str):
        values = [values]
    return [str(v).strip() for v in values if v]


def source_country(record: Dict[str, Any]) -> Optional[str]:
    """ISO country from a related organization, if present."""
    for link in record.get("links") or []:
        if not isinstance(link, dict):
            continue
        country = link.get("country") or {}
        code = None
        if isinstance(country, dict):
            code = country.get("code") or country.get("label")
        elif isinstance(country, str):
            code = country
        if not code:
            continue
        code = str(code).upper().strip()
        if len(code) > 3 and code in COUNTRIES:
            return code
        code = COUNTRY_ALIASES.get(code, code)
        if code in COUNTRIES:
            return code
        if len(code) == 2:
            return code
    return None


def source_owner(record: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """Owner name and website from the related organization link."""
    for link in record.get("links") or []:
        if not isinstance(link, dict):
            continue
        header = link.get("header") or {}
        if header.get("relatedRecordType") not in {None, "organization"}:
            continue
        name = unescape_text(
            link.get("legalname") or link.get("legalshortname") or link.get("officialname")
        )
        owner_url = normalize_http_url(link.get("websiteurl"))
        if name or owner_url:
            return name or None, owner_url
    return None, None


def content_types_indicate_datasets(content_types: Iterable[str]) -> Optional[bool]:
    """True/False when OpenDOAR contentTypes are present; None if unknown."""
    tokens = [t.lower() for t in content_types if t]
    if not tokens:
        return None
    if any(t in DATASET_CONTENT_TOKENS or "dataset" in t or "research data" in t for t in tokens):
        return True
    if any(t in PUBLICATION_CONTENT_TOKENS for t in tokens) and not any(
        "data" in t for t in tokens
    ):
        return False
    return None


def collected_from_indicates_data(record: Dict[str, Any]) -> bool:
    for name in collected_from_names(record):
        if name.lower() in DATA_COLLECTED_FROM:
            return True
    return False


def compatibility_indicates_data(record: Dict[str, Any]) -> bool:
    compat_id = (record.get("openaireCompatibilityId") or "").lower()
    if compat_id in DATA_COMPATIBILITY_IDS or compat_id.endswith("_data"):
        return True
    compat = (record.get("openaireCompatibility") or "").lower()
    return "data" in compat and "publication" not in compat


def name_url_indicates_data(name: str, url: str) -> bool:
    blob = f"{name} {url}"
    return bool(DATA_NAME_URL_RE.search(blob))


def is_native_data_typology(typology: str, scheme: str) -> bool:
    if typology in DATA_PROVIDER_TYPES:
        return True
    return scheme.startswith("datarepository") or scheme == "aggregator::datarepository"


def publishes_datasets(
    record: Dict[str, Any], dataset_count: Optional[int] = None
) -> Tuple[bool, str]:
    """Keep sources that actually publish datasets; drop publication-only IRs."""
    typology = typology_name(record)
    scheme = typology_scheme(record)
    name = unescape_text(record.get("officialName") or record.get("englishName") or "")
    url = record.get("websiteUrl") or ""

    if is_native_data_typology(typology, scheme):
        return True, "data_repository_typology"

    content_flag = content_types_indicate_datasets(content_type_list(record))
    if content_flag is True:
        return True, "content_types"
    if content_flag is False:
        return False, "publication_content_types"

    if collected_from_indicates_data(record):
        return True, "collected_from_data_registry"
    if compatibility_indicates_data(record):
        return True, "openaire_data_compatibility"
    if name_url_indicates_data(name, url):
        return True, "name_or_url_data_signal"

    if dataset_count is not None:
        if dataset_count > 0:
            return True, "graph_dataset_count"
        return False, "no_graph_datasets"

    if typology in JOURNAL_AGGREGATOR_TYPES | REPOSITORY_TYPES:
        return False, "publication_only_default"
    return False, "unsupported_typology"


def compact_source(
    record: Dict[str, Any], keep_reason: str, dataset_count: Optional[int] = None
) -> Dict[str, Any]:
    url = normalize_http_url(record.get("websiteUrl"))
    name = unescape_text(
        record.get("officialName") or record.get("englishName") or (url or "")
    )
    owner_name, owner_link = source_owner(record)
    country = source_country(record)
    openaire_id = record.get("id") or ""
    return {
        "id": openaire_id,
        "name": name,
        "url": url,
        "host": normalize_host(url),
        "typology": typology_name(record),
        "typology_scheme": typology_scheme(record),
        "content_types": content_type_list(record),
        "country": country,
        "owner_name": owner_name,
        "owner_link": owner_link,
        "description": unescape_text(record.get("description") or "") or None,
        "collected_from": collected_from_names(record),
        "compatibility": record.get("openaireCompatibility"),
        "compatibility_id": record.get("openaireCompatibilityId"),
        "access_rights": record.get("accessRights"),
        "keep_reason": keep_reason,
        "dataset_count": dataset_count,
        "openaire_url": OPENAIRE_EXPLORE_DATAPROVIDER + openaire_id if openaire_id else None,
        "original_ids": record.get("originalIds") or [],
        "pids": record.get("pids") or [],
    }


def query_graph(url: str, params: Dict[str, Any], timeout: int = 60) -> Optional[Dict]:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error("OpenAIRE Graph request failed %s %s: %s", url, params, e)
        return None
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON from OpenAIRE Graph %s: %s", url, e)
        return None


def fetch_datasources_for_type(type_name: str, delay: float = REQUEST_DELAY) -> List[Dict[str, Any]]:
    """Page all Graph data sources of one dataSourceTypeName via cursor."""
    sources: List[Dict[str, Any]] = []
    cursor = "*"
    page = 0
    while cursor:
        page += 1
        params = {
            "pageSize": PAGE_SIZE,
            "cursor": cursor,
            "dataSourceTypeName": f'"{type_name}"',
        }
        payload = query_graph(OPENAIRE_GRAPH_DATASOURCES, params)
        if not payload:
            logger.warning("Stopping %s fetch at page %s (empty/error response)", type_name, page)
            break
        results = payload.get("results") or []
        header = payload.get("header") or {}
        sources.extend(results)
        logger.info(
            "  %s page %s: %s records (total so far %s / numFound %s)",
            type_name,
            page,
            len(results),
            len(sources),
            header.get("numFound"),
        )
        cursor = header.get("nextCursor")
        if not results:
            break
        if delay:
            time.sleep(delay)
    return sources


def fetch_dataset_count(datasource_id: str) -> Optional[int]:
    """numFound of Graph datasets collected from this data source."""
    payload = query_graph(
        OPENAIRE_GRAPH_PRODUCTS,
        {
            "type": "dataset",
            "relCollectedFromDatasourceId": datasource_id,
            "pageSize": 1,
            "page": 1,
        },
    )
    if not payload:
        return None
    header = payload.get("header") or {}
    return int(header.get("numFound") or 0)


def infer_software(url: str, name: str) -> str:
    blob = f"{url} {name}".lower()
    if "dataverse" in blob:
        return "dataverse"
    if "figshare" in blob:
        return "figshare"
    return "custom"


_SOFTWARE_NAMES: Optional[Dict[str, str]] = None


def software_display_name(software_id: str) -> str:
    global _SOFTWARE_NAMES
    if _SOFTWARE_NAMES is None:
        _SOFTWARE_NAMES = {}
        software_jsonl = os.path.join(builder.DATASETS_DIR, "software.jsonl")
        if os.path.exists(software_jsonl):
            for row in builder.load_jsonl(software_jsonl):
                if row.get("id"):
                    _SOFTWARE_NAMES[row["id"]] = row.get("name") or row["id"]
    if software_id == "custom":
        return "Custom software"
    return _SOFTWARE_NAMES.get(software_id, software_id.title())


def load_registry_hosts(
    duckdb_path: Optional[str] = None,
) -> Tuple[Set[str], Set[str], Dict[str, str]]:
    """Load registry hosts and ids from DuckDB (fallback: full.parquet / full.jsonl)."""
    hosts: Set[str] = set()
    ids: Set[str] = set()
    host_to_id: Dict[str, str] = {}
    datasets_dir = builder.DATASETS_DIR
    duckdb_path = duckdb_path or os.path.join(datasets_dir, "datasets.duckdb")
    rows: List[Tuple[str, str]] = []

    if os.path.exists(duckdb_path):
        import duckdb

        con = duckdb.connect(duckdb_path, read_only=True)
        try:
            rows = con.execute("SELECT id, link FROM catalogs WHERE link IS NOT NULL").fetchall()
        finally:
            con.close()
        logger.info("Loaded %s catalog links from DuckDB", len(rows))
    else:
        parquet_path = os.path.join(datasets_dir, "full.parquet")
        jsonl_path = os.path.join(datasets_dir, "full.jsonl")
        if os.path.exists(parquet_path):
            import duckdb

            con = duckdb.connect(":memory:")
            rows = con.execute(
                "SELECT id, link FROM read_parquet(?) WHERE link IS NOT NULL",
                [parquet_path],
            ).fetchall()
            con.close()
            logger.info("Loaded %s catalog links from full.parquet", len(rows))
        elif os.path.exists(jsonl_path):
            for row in builder.load_jsonl(jsonl_path):
                if row.get("id") and row.get("link"):
                    rows.append((row["id"], row["link"]))
            logger.info("Loaded %s catalog links from full.jsonl", len(rows))

    for record_id, link in rows:
        ids.add(record_id)
        host = normalize_host(link)
        if host:
            hosts.add(host)
            host_to_id.setdefault(host, record_id)
        generated = catalog_id_from_url(link) if link else ""
        if generated:
            ids.add(generated)
            host_to_id.setdefault(generated, record_id)

    scheduled_dir = builder.SCHEDULED_DIR
    if os.path.isdir(scheduled_dir):
        for root, _dirs, files in os.walk(scheduled_dir):
            for filename in files:
                if not filename.endswith(".yaml"):
                    continue
                path = os.path.join(root, filename)
                try:
                    with open(path, encoding="utf-8") as handle:
                        record = yaml.safe_load(handle) or {}
                except (OSError, yaml.YAMLError):
                    continue
                record_id = record.get("id") or filename[:-5]
                ids.add(record_id)
                host = normalize_host(record.get("link"))
                if host:
                    hosts.add(host)
                    host_to_id.setdefault(host, record_id)

    logger.info("Registry index: %s hosts, %s ids", len(hosts), len(ids))
    return hosts, ids, host_to_id


def match_source(
    source: Dict[str, Any],
    hosts: Set[str],
    ids: Set[str],
    host_to_id: Dict[str, str],
) -> Tuple[bool, Optional[str]]:
    """True when this OpenAIRE source is already in the registry (host or id)."""
    url = source.get("url") or ""
    host = source.get("host") or normalize_host(url)
    if host and host in hosts:
        return True, host_to_id.get(host)
    generated = catalog_id_from_url(url) if url else ""
    if generated and generated in ids:
        return True, generated
    return False, None


def in_scope_typology(typology: str) -> bool:
    return typology in DEFAULT_TYPES


def select_sources(
    raw_records: Iterable[Dict[str, Any]],
    check_datasets: bool = False,
    delay: float = REQUEST_DELAY,
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Filter Graph records to dataset-publishing portals with usable URLs."""
    kept: List[Dict[str, Any]] = []
    seen_hosts: Set[str] = set()
    stats = {
        "raw": 0,
        "out_of_scope": 0,
        "no_url": 0,
        "junk_url": 0,
        "publication_only": 0,
        "kept": 0,
        "duplicate_host": 0,
        "dataset_checked": 0,
    }
    for record in raw_records:
        stats["raw"] += 1
        typology = typology_name(record)
        if not in_scope_typology(typology) and not is_native_data_typology(
            typology, typology_scheme(record)
        ):
            stats["out_of_scope"] += 1
            continue
        url = normalize_http_url(record.get("websiteUrl"))
        if not url:
            stats["no_url"] += 1
            continue
        if is_junk_url(url):
            stats["junk_url"] += 1
            continue
        record = dict(record)
        record["websiteUrl"] = url

        dataset_count = None
        keep, reason = publishes_datasets(record)
        needs_graph_check = (
            check_datasets
            and not keep
            and reason == "publication_only_default"
            and typology in (REPOSITORY_TYPES | JOURNAL_AGGREGATOR_TYPES)
            and record.get("id")
        )
        if needs_graph_check:
            dataset_count = fetch_dataset_count(record["id"])
            stats["dataset_checked"] += 1
            keep, reason = publishes_datasets(record, dataset_count=dataset_count)
            if delay:
                time.sleep(delay)

        if not keep:
            stats["publication_only"] += 1
            continue

        compact = compact_source(record, keep_reason=reason, dataset_count=dataset_count)
        host = compact.get("host") or ""
        if host in seen_hosts:
            stats["duplicate_host"] += 1
            continue
        if host:
            seen_hosts.add(host)
        kept.append(compact)
        stats["kept"] += 1
    return kept, stats


def write_json(path: str, payload: Any) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def load_sources_file(path: str) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict) and "sources" in payload:
        return payload["sources"]
    if isinstance(payload, list):
        return payload
    raise typer.BadParameter(f"{path} must be a JSON list or an object with sources[]")


def resolve_country(source: Dict[str, Any]) -> Optional[str]:
    code = source.get("country")
    if code:
        code = COUNTRY_ALIASES.get(str(code).upper(), str(code).upper())
        if code in COUNTRIES:
            return code
    host = source.get("host") or normalize_host(source.get("url"))
    tld = host.rsplit(".", 1)[-1] if host else ""
    if tld in DOMAIN_LOCATIONS:
        loc = DOMAIN_LOCATIONS[tld].get("location") or {}
        country = (loc.get("country") or {}).get("id")
        if country and country != "Unknown":
            return country
    return None


def write_scheduled_record(
    source: Dict[str, Any],
    existing_ids: Set[str],
    detect: bool = False,
) -> Optional[str]:
    """Write one scheduled YAML using the same path layout as add-single."""
    url = source["url"]
    record_id = catalog_id_from_url(url)
    software = infer_software(url, source.get("name") or "")
    country = resolve_country(source)
    name = source.get("name") or urlparse(url).netloc
    description = source.get("description") or (
        "OpenAIRE Graph data source pending live confirmation. "
        "Probe OAI-PMH/REST before promoting."
    )
    owner_name = source.get("owner_name") or name
    owner_link = source.get("owner_link")
    owner_type = "Academy"

    if record_id in existing_ids:
        logger.info("Already in registry: %s", record_id)
        return None

    if detect:
        builder._add_single_entry(
            url,
            software,
            catalog_type="Scientific data repository",
            name=name,
            description=description,
            country=country,
            owner_name=owner_name,
            owner_link=owner_link,
            owner_type=owner_type,
            scheduled=True,
            force=False,
            preloaded=list(existing_ids),
        )
        for root, _dirs, files in os.walk(builder.SCHEDULED_DIR):
            if record_id + ".yaml" in files:
                path = os.path.join(root, record_id + ".yaml")
                _attach_openaire_identifier(path, source)
                return record_id
        return record_id

    record = copy.deepcopy(ENTRY_TEMPLATE)
    record["id"] = record_id
    record["link"] = url
    record["name"] = name
    record["description"] = description
    record["catalog_type"] = "Scientific data repository"
    record["status"] = "scheduled"
    record["owner"]["name"] = owner_name
    record["owner"]["type"] = owner_type
    if owner_link:
        record["owner"]["link"] = owner_link

    if country and country in COUNTRIES:
        location = {
            "location": {"country": {"id": country, "name": COUNTRIES[country]}}
        }
    else:
        tld = urlparse(url).netloc.rsplit(".", 1)[-1].split(":")[0]
        location = DOMAIN_LOCATIONS.get(tld, {"location": {"country": {"id": "Unknown", "name": "Unknown"}}})
    record["coverage"] = [copy.deepcopy(location)]
    record["owner"]["location"] = copy.deepcopy(location["location"])

    record["software"] = {"id": software, "name": software_display_name(software)}

    if source.get("access_rights") in {"restricted", "controlled", "closed"}:
        record["access_mode"] = ["restricted"]

    openaire_id = source.get("id")
    if openaire_id:
        record["identifiers"] = [
            {
                "id": "openaire",
                "value": openaire_id,
                "url": source.get("openaire_url")
                or OPENAIRE_EXPLORE_DATAPROVIDER + openaire_id,
            }
        ]

    country_id = location["location"]["country"]["id"]
    country_dir = os.path.join(builder.SCHEDULED_DIR, country_id)
    subdir_dir = os.path.join(country_dir, "scientific")
    os.makedirs(subdir_dir, exist_ok=True)
    filename = os.path.join(subdir_dir, record_id + ".yaml")
    if os.path.exists(filename):
        logger.info("Already processed: %s", record_id)
        return None
    with open(filename, "w", encoding="utf-8") as handle:
        handle.write(yaml.safe_dump(record, allow_unicode=True))
    logger.info("%s saved", record_id)
    return record_id


def _attach_openaire_identifier(path: str, source: Dict[str, Any]) -> None:
    openaire_id = source.get("id")
    if not openaire_id:
        return
    with open(path, encoding="utf-8") as handle:
        record = yaml.safe_load(handle) or {}
    identifiers = record.get("identifiers") or []
    if any(isinstance(item, dict) and item.get("id") == "openaire" for item in identifiers):
        return
    identifiers.append(
        {
            "id": "openaire",
            "value": openaire_id,
            "url": source.get("openaire_url") or OPENAIRE_EXPLORE_DATAPROVIDER + openaire_id,
        }
    )
    record["identifiers"] = identifiers
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(yaml.safe_dump(record, allow_unicode=True))


@app.command("list-sources")
def list_sources(
    output: str = typer.Option("openaire_sources.json", "--output", help="Output JSON path"),
    types: Optional[str] = typer.Option(
        None,
        "--types",
        help="Comma-separated dataSourceTypeName values (default: data repos + IRs + journal aggregators)",
    ),
    check_datasets: bool = typer.Option(
        False,
        "--check-datasets/--no-check-datasets",
        help="Query Graph datasets for mixed IRs/journal aggregators without a data signal",
    ),
    delay: float = typer.Option(REQUEST_DELAY, "--delay", help="Seconds between Graph API pages"),
    dryrun: bool = typer.Option(False, "--dry-run", help="Fetch and filter but do not write JSON"),
):
    """Fetch OpenAIRE Graph data sources and keep dataset-publishing portals."""
    type_names = [item.strip() for item in types.split(",")] if types else sorted(DEFAULT_TYPES)
    logger.info("Fetching OpenAIRE Graph data sources for: %s", ", ".join(type_names))
    raw: List[Dict[str, Any]] = []
    for type_name in type_names:
        logger.info("=== %s ===", type_name)
        raw.extend(fetch_datasources_for_type(type_name, delay=delay))

    kept, stats = select_sources(raw, check_datasets=check_datasets, delay=delay)
    payload = {
        "source": OPENAIRE_GRAPH_DATASOURCES,
        "types": type_names,
        "stats": stats,
        "sources": kept,
    }
    logger.info("Filter stats: %s", json.dumps(stats))
    if dryrun:
        logger.info("DRY RUN — would write %s sources to %s", len(kept), output)
        for source in kept[:15]:
            logger.info("  %s — %s [%s]", source.get("url"), source.get("name"), source.get("keep_reason"))
        return
    write_json(output, payload)
    logger.info("Wrote %s sources to %s", len(kept), output)


@app.command("match-registry")
def match_registry(
    input: str = typer.Option(..., "--input", help="JSON from list-sources"),
    output: Optional[str] = typer.Option(
        None, "--output", help="JSON of hosts not yet in the registry"
    ),
    duckdb_path: Optional[str] = typer.Option(
        None, "--duckdb", help="Override path to datasets.duckdb"
    ),
):
    """Dedup OpenAIRE sources against DuckDB catalog hosts."""
    sources = load_sources_file(input)
    hosts, ids, host_to_id = load_registry_hosts(duckdb_path=duckdb_path)
    misses: List[Dict[str, Any]] = []
    matches: List[Dict[str, Any]] = []
    for source in sources:
        is_dup, existing_id = match_source(source, hosts, ids, host_to_id)
        if is_dup:
            source = dict(source)
            source["existing_id"] = existing_id
            matches.append(source)
        else:
            misses.append(source)
    logger.info(
        "Matched %s / %s sources to the registry; %s misses",
        len(matches),
        len(sources),
        len(misses),
    )
    if output:
        write_json(
            output,
            {
                "matched": len(matches),
                "misses": len(misses),
                "sources": misses,
            },
        )
        logger.info("Wrote %s misses to %s", len(misses), output)
    else:
        for source in misses[:25]:
            logger.info("MISS %s — %s (%s)", source.get("url"), source.get("name"), source.get("country"))
        if len(misses) > 25:
            logger.info("  ... and %s more", len(misses) - 25)


@app.command("add-scheduled")
def add_scheduled(
    input: str = typer.Option(..., "--input", help="JSON of misses (match-registry output or list-sources)"),
    dryrun: bool = typer.Option(False, "--dry-run", help="Do not write YAML"),
    detect: bool = typer.Option(
        False,
        "--detect/--no-detect",
        help="Run apidetect on each new record (slow; default is YAML only)",
    ),
    limit: Optional[int] = typer.Option(None, "--limit", help="Max new records to write"),
    duckdb_path: Optional[str] = typer.Option(None, "--duckdb"),
):
    """Add unmatched OpenAIRE data sources under data/scheduled/."""
    sources = load_sources_file(input)
    hosts, ids, host_to_id = load_registry_hosts(duckdb_path=duckdb_path)
    added = 0
    skipped = 0
    for source in sources:
        if not source.get("url"):
            skipped += 1
            continue
        if is_junk_url(source.get("url")):
            logger.info("Skipping junk URL %s", source.get("url"))
            skipped += 1
            continue
        is_dup, existing_id = match_source(source, hosts, ids, host_to_id)
        if is_dup:
            logger.info("Skipping duplicate %s (existing %s)", source.get("url"), existing_id)
            skipped += 1
            continue
        if dryrun:
            logger.info(
                "DRY RUN would add %s — %s [%s / %s]",
                source.get("url"),
                source.get("name"),
                source.get("typology"),
                source.get("country") or "Unknown",
            )
            added += 1
        else:
            record_id = write_scheduled_record(source, existing_ids=ids, detect=detect)
            if record_id:
                added += 1
                hosts.add(source.get("host") or normalize_host(source["url"]))
                ids.add(record_id)
            else:
                skipped += 1
        if limit is not None and added >= limit:
            break
    logger.info("Added %s scheduled records; skipped %s", added, skipped)


@app.command("fetch-portals")
def fetch_portals(
    output_file: str = typer.Option("openaire_portals.txt", "--output"),
    dryrun: bool = typer.Option(False, "--dry-run"),
    max_pages: int = typer.Option(50, "--max-pages", hidden=True),
    method: str = typer.Option("rest", "--method", hidden=True),
):
    """Compatibility wrapper: Graph list-sources written as URL<TAB>name<TAB>id."""
    del max_pages, method
    tmp_json = output_file.rsplit(".", 1)[0] + ".json"
    list_sources(output=tmp_json, types=None, check_datasets=False, delay=REQUEST_DELAY, dryrun=dryrun)
    if dryrun:
        return
    payload = load_sources_file(tmp_json)
    with open(output_file, "w", encoding="utf-8") as handle:
        for source in payload:
            handle.write(
                f"{source.get('url', '')}\t{source.get('name', '')}\t{source.get('id', '')}\n"
            )
    logger.info("Wrote %s TSV rows to %s", len(payload), output_file)


if __name__ == "__main__":
    app()
