#!/usr/bin/env python3
"""Discovery hunt toolkit: prior / budget / search / dedupe / probe / ingest / log.

One tested implementation of the plumbing discovery sessions used to rebuild as
throwaway scripts. Each loop command ends with a ``next:`` line.

- ``prior --target`` — stop when this slice was completed in the last 14 days.
- ``budget`` — FOFA ``remain_api_data``; stop when it is 0.
- ``search fofa|censys QUERY`` — query internet-map APIs, optional ``--dedupe``.
- ``dedupe candidates.jsonl`` — batch duplicate-check against dataset exports.
- ``probe candidates.jsonl`` — liveness plus one capability URL and a verdict.
- ``ingest probed.jsonl`` — ``add-batch``, promote, ``validate-yaml --id``.
- ``next`` — up to five suggestions when the user did not name a target.
- ``log`` — append one validated row to dataquality/hunts.jsonl.

Scope: this is a local maintainer/agent CLI, not a scanner. It queries the
documented search APIs and probes only candidate hosts produced by a search or
list step. No authentication bypass, no internet-wide sweeps.
"""

from __future__ import annotations

import base64
import html
import json
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
import typer

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from check_liveness import classify_liveness  # noqa: E402
from url_utils import canonicalize_url, host_from_url, normalize_host_for_id  # noqa: E402

_REPO_ROOT = _SCRIPT_DIR.parent
DATASETS_DIR = _REPO_ROOT / "data" / "datasets"
HUNTS_LOG = _REPO_ROOT / "dataquality" / "hunts.jsonl"

FOFA_API_URL = "https://fofa.info/api/v1/search/all"
FOFA_INFO_URL = "https://fofa.info/api/v1/info/my"
FOFA_FIELDS = "host,ip,port,protocol,title,domain"
HUNT_TMP_ROOT = Path("/tmp/hunts")
SLICE_WINDOW_DAYS = 14
MAX_QUERY_FILE = 25

# One capability URL per software id. Probe must not walk the full apidetect map.
CAPABILITY_PROBES = {
    "geoserver": {
        "url": "/geoserver/ows?service=WMS&version=1.1.1&request=GetCapabilities",
        "parser": "wms",
    },
    "arcgisserver": {
        "url": "/rest/services?f=json",
        "parser": "arcgis",
    },
    "ckan": {
        "url": "/api/3/action/package_search?rows=0",
        "parser": "ckan",
    },
    "panelapp": {
        "url": "/api/v1/panels/?page_size=1",
        "expected_mime": "application/json",
    },
    "vizier": {
        "url": "/viz-bin/VizieR",
        "expected_mime": "text/html",
    },
    "nbia": {
        "url": "/nbia-api/services/v1/getCollectionValues",
        "expected_mime": "application/json",
    },
}
PREFERRED_NEXT_KINDS = ("named-directory", "country-indicators")
CENSYS_API_URL = "https://api.platform.censys.io/v3/global/search/query"

DEFAULT_USER_AGENT = "dataportals-registry-hunt/1.0 (+https://github.com/datenoio/dataportals-registry)"

# Hunt kinds observed in dataquality/hunts.jsonl plus the hunt types documented
# in docs/agents/discover.md.
HUNT_KINDS = {
    "software-instance",
    "national-harvest-sources",
    "university-ir",
    "country-indicators",
    "country-geoportals",
    "country-opendata",
    "country-scientific",
    "country-shape",
    "country-gap",
    "country-review",
    "named-directory",
    "igo-organization",
    "municipal-gis",
    "custom-review",
    "scheduled-review",
    "single-add",
    "analysis",
    "process",
}

HUNT_STATUSES = {"complete", "partial", "blocked"}

app = typer.Typer(help="Discovery hunt toolkit: search / dedupe / probe / log.")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _default_out(input_path: Path, suffix: str) -> Path:
    return input_path.with_name(input_path.name.replace(".jsonl", "") + suffix)


def _emit_next(command: str) -> None:
    """Last stdout line of a loop command. Agents follow this instead of re-reading docs."""
    typer.echo(f"next: {command}")


def _today() -> date:
    return date.today()


def _require_fofa_credentials() -> Tuple[str, str]:
    email = os.environ.get("FOFA_EMAIL")
    key = os.environ.get("FOFA_KEY")
    if not email or not key:
        raise ValueError("FOFA requires FOFA_EMAIL and FOFA_KEY environment variables")
    return email, key


def _fofa_account_info(session: Optional[requests.Session] = None) -> Dict[str, Any]:
    """Return the FOFA account payload. Does not run a search query."""
    email, key = _require_fofa_credentials()
    sess = session or requests.Session()
    response = sess.get(
        FOFA_INFO_URL, params={"email": email, "key": key}, timeout=30
    )
    data = response.json()
    if data.get("error"):
        raise ValueError(f"FOFA error: {data.get('errmsg') or data}")
    return data


def _remain_api_data(account: Dict[str, Any]) -> int:
    """Return a positive search balance.

    FOFA still reports ``remain_api_data`` as 0 after the F-point migration
    while ``fofa_point`` and ``remain_free_point`` hold the usable balance.
    """
    for key in ("remain_api_data", "fofa_point", "remain_free_point"):
        try:
            value = int(account.get(key) or 0)
        except (TypeError, ValueError):
            continue
        if value > 0:
            return value
    return 0


def _load_queries(
    query: Optional[str],
    query_file: Optional[Path],
    allow_wide: bool,
) -> List[str]:
    queries: List[str] = []
    if query_file is not None:
        if not query_file.exists():
            raise ValueError(f"Query file not found: {query_file}")
        for line in query_file.read_text(encoding="utf8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                queries.append(stripped)
    if query:
        queries.append(query)
    if not queries:
        raise ValueError("Provide a query argument or --query-file")
    if len(queries) > MAX_QUERY_FILE and not allow_wide:
        raise ValueError(
            f"{len(queries)} queries exceeds {MAX_QUERY_FILE}; pass --allow-wide to continue"
        )
    return queries


def _search_slug(provider: str, queries: List[str]) -> str:
    raw = queries[0] if queries else provider
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    return (slug or provider)[:48]


def _search_out_path(explicit: Optional[Path], slug: str) -> Path:
    if explicit is not None:
        return explicit
    directory = HUNT_TMP_ROOT / slug
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "candidates.jsonl"


def _software_id_set() -> set:
    root = _REPO_ROOT / "data" / "software"
    found = set()
    if not root.exists():
        return found
    for path in root.rglob("*.yaml"):
        if path.name != "types.yaml":
            found.add(path.stem)
    return found


def _split_target(target: str, software_ids: set) -> Tuple[str, Optional[str]]:
    """Return (software id or whole target, suffix). Suffix splits on '.' or '-'."""
    for sep in (".", "-"):
        if sep not in target:
            continue
        prefix, suffix = target.split(sep, 1)
        if prefix in software_ids and suffix:
            return prefix, suffix
    if target in software_ids:
        return target, None
    return target, None


def _notes_have_token(notes: str, token: str) -> bool:
    if not token:
        return False
    parts = re.split(r"[^A-Za-z0-9]+", notes.lower())
    return token.lower() in parts


def _recent_complete(row: Dict[str, Any], today: date) -> bool:
    if row.get("status") != "complete":
        return False
    raw = row.get("date") or ""
    try:
        logged = datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return False
    delta = (today - logged).days
    return 0 <= delta <= SLICE_WINDOW_DAYS


def _load_hunts(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _request_with_backoff(
    session: requests.Session,
    method: str,
    url: str,
    max_retries: int = 5,
    base_delay: float = 2.0,
    cap: float = 120.0,
    **kwargs,
) -> requests.Response:
    """HTTP request with exponential backoff + jitter on 429 and transient 5xx."""
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        try:
            response = session.request(method, url, **kwargs)
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < max_retries:
                time.sleep(min(cap, base_delay * (2**attempt)) + random.uniform(0, 1))
                continue
            raise
        if response.status_code == 429 or response.status_code in (500, 502, 503, 504):
            if attempt < max_retries:
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = float(retry_after) if retry_after else None
                except ValueError:
                    delay = None
                if delay is None:
                    delay = min(cap, base_delay * (2**attempt)) + random.uniform(0, 1)
                time.sleep(delay)
                continue
        return response
    if last_exc is not None:
        raise last_exc
    return response


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------


def _fofa_search(
    session: requests.Session,
    query: str,
    size: int,
    max_pages: int,
    max_retries: int,
) -> List[Dict[str, Any]]:
    email = os.environ.get("FOFA_EMAIL")
    key = os.environ.get("FOFA_KEY")
    if not email or not key:
        raise ValueError("FOFA requires FOFA_EMAIL and FOFA_KEY environment variables")

    results: List[Dict[str, Any]] = []
    for page in range(1, max_pages + 1):
        params = {
            "email": email,
            "key": key,
            "qbase64": base64.b64encode(query.encode()).decode(),
            "fields": FOFA_FIELDS,
            "size": size,
            "page": page,
        }
        response = _request_with_backoff(
            session, "GET", FOFA_API_URL, params=params, timeout=30, max_retries=max_retries
        )
        data = response.json()
        if data.get("error"):
            raise ValueError(f"FOFA error: {data.get('errmsg') or data}")
        for row in data.get("results") or []:
            record = dict(zip(FOFA_FIELDS.split(","), row))
            host = record.get("host") or ""
            protocol = record.get("protocol") or ""
            if host.startswith("http://") or host.startswith("https://"):
                url = host
                host = host_from_url(url) or host
            elif protocol in ("http", "https"):
                url = f"{protocol}://{host}"
            else:
                url = f"https://{host}"
            results.append(
                {
                    "host": host,
                    "url": url,
                    "title": record.get("title") or "",
                    "source": "fofa",
                    "query": query,
                    "extra": {
                        "ip": record.get("ip"),
                        "port": record.get("port"),
                        "domain": record.get("domain"),
                    },
                }
            )
        if len(data.get("results") or []) < size:
            break
        time.sleep(1.2)
    return results


def _censys_extract(hit: Dict[str, Any]) -> Dict[str, Any]:
    """Best-effort extraction of host/title from a Censys Platform v3 hit."""

    def _walk(obj: Any, keys: tuple) -> Optional[str]:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in keys and isinstance(v, str) and v:
                    return v
                found = _walk(v, keys)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = _walk(item, keys)
                if found:
                    return found
        return None

    host = _walk(hit, ("host", "name", "domain")) or _walk(hit, ("ip", "ip_str"))
    title = _walk(hit, ("html_title", "title")) or ""
    return {"host": host, "title": title}


def _censys_search(
    session: requests.Session,
    query: str,
    size: int,
    max_pages: int,
    max_retries: int,
) -> List[Dict[str, Any]]:
    token = os.environ.get("CENSYS_API_TOKEN") or os.environ.get("CENSYS_PAT")
    org = os.environ.get("CENSYS_ORGANIZATION_ID") or os.environ.get("CENSYS_ORG_ID")
    if not token:
        raise ValueError(
            "Censys requires CENSYS_API_TOKEN (or CENSYS_PAT) environment variable"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.censys.api.v3.vndel+json",
    }
    if org:
        headers["X-Organization-ID"] = org

    results: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    for _page in range(max_pages):
        body: Dict[str, Any] = {"query": query, "page_size": min(size, 100)}
        if cursor:
            body["cursor"] = cursor
        response = _request_with_backoff(
            session,
            "POST",
            CENSYS_API_URL,
            data=json.dumps(body),
            headers=headers,
            timeout=60,
            max_retries=max_retries,
        )
        if response.status_code >= 400:
            raise ValueError(f"Censys HTTP {response.status_code}: {response.text[:300]}")
        data = response.json()
        result = data.get("result", data)
        hits = result.get("hits") or []
        for hit in hits:
            extracted = _censys_extract(hit if isinstance(hit, dict) else {})
            host = extracted.get("host")
            if not host:
                continue
            url = host if host.startswith(("http://", "https://")) else f"https://{host}"
            results.append(
                {
                    "host": host_from_url(url) or host,
                    "url": url,
                    "title": extracted.get("title") or "",
                    "source": "censys",
                    "query": query,
                    "extra": {"hit": hit},
                }
            )
        cursor = result.get("next") or result.get("next_cursor") or result.get("nextCursor")
        if not cursor or not hits:
            break
    return results


@app.command()
def budget():
    """Print FOFA remain_api_data. Does not run a search query."""
    try:
        account = _fofa_account_info()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    remaining = _remain_api_data(account)
    if remaining <= 0:
        typer.echo("decision: stop-budget")
        typer.echo("remain_api_data: 0")
        _emit_next("none")
        raise typer.Exit(2)
    typer.echo("decision: continue")
    typer.echo(f"remain_api_data: {remaining}")
    _emit_next("python scripts/hunt.py search fofa QUERY --dedupe")


@app.command()
def search(
    provider: str = typer.Argument(..., help="Search provider: fofa or censys"),
    query: Optional[str] = typer.Argument(None, help="Query in the provider's syntax"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output JSONL path (default: /tmp/hunts/<slug>/candidates.jsonl)"),
    query_file: Optional[Path] = typer.Option(None, "--query-file", help="One query per line"),
    allow_wide: bool = typer.Option(False, "--allow-wide", help="Allow a query file longer than 25 lines"),
    dedupe_flag: bool = typer.Option(False, "--dedupe", help="Annotate candidates against exports before writing"),
    size: int = typer.Option(100, "--size", help="Results per page"),
    max_pages: int = typer.Option(1, "--max-pages", help="Maximum pages to fetch"),
    max_retries: int = typer.Option(5, "--max-retries", help="Retries on 429/5xx with backoff"),
):
    """Query FOFA or Censys and write normalized candidate JSONL rows."""
    try:
        queries = _load_queries(query, query_file, allow_wide)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)

    if provider not in ("fofa", "censys"):
        typer.echo(f"Unknown provider '{provider}': use fofa or censys", err=True)
        raise typer.Exit(1)

    if provider == "fofa":
        try:
            _require_fofa_credentials()
            account = _fofa_account_info()
        except ValueError as e:
            typer.echo(str(e), err=True)
            raise typer.Exit(1)
        if _remain_api_data(account) <= 0:
            typer.echo("decision: stop-budget")
            typer.echo("remain_api_data: 0")
            _emit_next("none")
            raise typer.Exit(2)

    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    results: List[Dict[str, Any]] = []
    try:
        for index, one in enumerate(queries):
            if index:
                time.sleep(1.2)
            if provider == "fofa":
                results.extend(_fofa_search(session, one, size, max_pages, max_retries))
            else:
                results.extend(_censys_search(session, one, size, max_pages, max_retries))
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)

    if dedupe_flag:
        try:
            ids, urls, hosts = _build_export_indexes()
        except ValueError as e:
            typer.echo(str(e), err=True)
            raise typer.Exit(1)
        results = dedupe_rows(results, ids, urls, hosts)

    out_path = _search_out_path(out, _search_slug(provider, queries))
    _write_jsonl(out_path, results)
    typer.echo(f"Wrote {len(results)} candidates to {out_path}")
    if dedupe_flag:
        _emit_next(f"python scripts/hunt.py probe {out_path}")
    else:
        _emit_next(f"python scripts/hunt.py dedupe {out_path}")


# ---------------------------------------------------------------------------
# dedupe
# ---------------------------------------------------------------------------


def _load_export_links() -> List[Dict[str, Any]]:
    """Load id/link/uid from exports: DuckDB read-only, parquet fallback on lock."""
    db_path = DATASETS_DIR / "datasets.duckdb"
    parquet_path = DATASETS_DIR / "full.parquet"
    import duckdb

    if db_path.exists():
        try:
            con = duckdb.connect(str(db_path), read_only=True)
            try:
                return con.execute("SELECT id, link, uid FROM catalogs").fetchall()
            finally:
                con.close()
        except Exception as exc:
            typer.echo(f"DuckDB locked or unreadable ({exc}); falling back to parquet")
    if parquet_path.exists():
        con = duckdb.connect(":memory:")
        try:
            return con.execute(
                "SELECT id, link, uid FROM read_parquet(?)", [str(parquet_path)]
            ).fetchall()
        finally:
            con.close()
    raise ValueError(f"No export found at {db_path} or {parquet_path}")


def _build_export_indexes() -> tuple:
    """Return (ids, canonical-url map, host map) from the exports."""
    ids = set()
    urls: Dict[str, Optional[str]] = {}
    hosts: Dict[str, Optional[str]] = {}
    for rid, link, _uid in _load_export_links():
        if rid:
            ids.add(rid)
        if link:
            canon = canonicalize_url(link)
            if canon:
                urls.setdefault(canon, rid)
            host = host_from_url(link)
            if host:
                hosts.setdefault(host, rid)
    return ids, urls, hosts


def dedupe_rows(
    candidates: List[Dict[str, Any]],
    ids: set,
    urls: Dict[str, Optional[str]],
    hosts: Dict[str, Optional[str]],
) -> List[Dict[str, Any]]:
    """Annotate candidates with exists/existing_id against export indexes."""
    annotated = []
    for row in candidates:
        url = row.get("url") or ""
        host = row.get("host") or host_from_url(url) or ""
        rid = row.get("id") or normalize_host_for_id(host.split(":", 1)[0])
        canon = canonicalize_url(url)
        is_root = (urlparse(url).path or "") in ("", "/")

        existing = None
        if canon and canon in urls:
            existing = urls[canon]
        elif rid and rid in ids:
            existing = rid
        elif is_root and host and host in hosts:
            existing = hosts[host]

        out_row = dict(row)
        out_row["exists"] = existing is not None
        if existing is not None:
            out_row["existing_id"] = existing
        annotated.append(out_row)
    return annotated


@app.command()
def dedupe(
    candidates: Path = typer.Argument(..., help="Candidate JSONL from search/probe"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output path (default: <input>.deduped.jsonl)"),
):
    """Batch duplicate-check candidates against dataset exports."""
    rows = _read_jsonl(candidates)
    try:
        ids, urls, hosts = _build_export_indexes()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    annotated = dedupe_rows(rows, ids, urls, hosts)
    out_path = out or _default_out(candidates, ".deduped.jsonl")
    _write_jsonl(out_path, annotated)
    existing = sum(1 for r in annotated if r.get("exists"))
    typer.echo(f"{len(annotated)} candidates: {existing} already registered, {len(annotated) - existing} new")
    typer.echo(f"Wrote {out_path}")
    _emit_next(f"python scripts/hunt.py probe {out_path}")


# ---------------------------------------------------------------------------
# probe
# ---------------------------------------------------------------------------

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_probe_lock = threading.Lock()


def _load_fingerprints(software_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """Return {software_id: first URL-map entry} from apidetect's CATALOGS_URLMAP."""
    from apidetect import CATALOGS_URLMAP

    fingerprints = {}
    for sw in software_ids:
        entries = CATALOGS_URLMAP.get(sw)
        if not entries:
            continue
        entry = next((e for e in entries if e.get("id") == sw), entries[0])
        fingerprints[sw] = entry
    return fingerprints


def _decode_response_text(response: requests.Response) -> str:
    """Decode response text honoring charset headers and apparent encoding (GBK etc.)."""
    if response.encoding:
        return response.text
    apparent = response.apparent_encoding
    if apparent:
        response.encoding = apparent
        return response.text
    return response.text


def _extract_title(text: str) -> str:
    match = _TITLE_RE.search(text or "")
    if not match:
        return ""
    return html.unescape(re.sub(r"\s+", " ", match.group(1))).strip()


def _transport_dead(http_code: Optional[int], error: Optional[str]) -> bool:
    if error:
        lowered = error.lower()
        if any(token in lowered for token in ("timeout", "timed out", "connection")):
            return True
    return http_code is not None and http_code >= 500


def _parse_collection_count(parser: str, response: requests.Response) -> Optional[int]:
    """Return a collection size for the three capability parsers, or None if unparsed."""
    if parser == "wms":
        text = _decode_response_text(response)
        return len(re.findall(r"<Layer[\s>]", text, flags=re.IGNORECASE))
    try:
        data = response.json()
    except ValueError:
        return None
    if not isinstance(data, dict):
        return None
    if parser == "arcgis":
        services = data.get("services")
        if not isinstance(services, list):
            return None
        return len(services)
    if parser == "ckan":
        result = data.get("result")
        if isinstance(result, dict) and isinstance(result.get("count"), int):
            return result["count"]
    return None


def _probe_one(
    row: Dict[str, Any],
    session: requests.Session,
    timeout: float,
    fingerprints: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Probe one candidate: root GET, at most one capability URL, then a verdict."""
    url = row.get("url") or ""
    out = dict(row)
    http_code: Optional[int] = None
    error: Optional[str] = None
    text = ""
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True)
        http_code = response.status_code
        text = _decode_response_text(response)[:200000]
        out["final_url"] = response.url if response.url != url else None
    except requests.exceptions.Timeout as exc:
        error = f"timeout: {exc}"
    except requests.exceptions.ConnectionError as exc:
        error = f"connection error: {exc}"
    except requests.exceptions.RequestException as exc:
        error = str(exc)

    out["http_code"] = http_code
    out["liveness"] = classify_liveness(http_code, error)
    if error:
        out["error"] = error
    if http_code and 200 <= http_code < 400:
        title = _extract_title(text)
        if title:
            out["title"] = title

    # Never bypass 401/403: record and do not request the capability URL.
    if http_code in (401, 403):
        out["auth_required"] = True
        out["verdict"] = "auth"
        return out
    if _transport_dead(http_code, error):
        out["verdict"] = "dead"
        return out

    entry: Optional[Dict[str, Any]] = None
    software_id: Optional[str] = None
    if fingerprints:
        software_id, entry = next(iter(fingerprints.items()))

    collection_count: Optional[int] = None
    parser_used = False
    if entry is not None:
        base = url if url.endswith("/") else url + "/"
        probe_url = urljoin(base, str(entry["url"]).lstrip("/"))
        fp_response = None
        try:
            fp_response = session.get(probe_url, timeout=timeout, allow_redirects=True)
        except requests.exceptions.RequestException:
            fp_response = None
        if fp_response is not None and fp_response.status_code in (401, 403):
            out["auth_required"] = True
            out["verdict"] = "auth"
            return out
        if fp_response is not None and fp_response.status_code >= 500:
            out["verdict"] = "dead"
            return out
        if fp_response is not None:
            parser = entry.get("parser")
            if parser:
                parser_used = True
                collection_count = _parse_collection_count(parser, fp_response)
                if collection_count is not None:
                    out["collection_count"] = collection_count
                if isinstance(collection_count, int) and collection_count > 0:
                    out["software_id"] = software_id
                    out["fingerprint_url"] = probe_url
            else:
                matched = fp_response.status_code == 200
                expected = entry.get("expected_mime")
                if matched and expected:
                    expected_list = expected if isinstance(expected, list) else [expected]
                    content_type = (fp_response.headers.get("Content-Type") or "").split(";")[0].strip()
                    if content_type not in expected_list:
                        matched = False
                if matched:
                    out["software_id"] = software_id
                    out["fingerprint_url"] = probe_url

    if out.get("software_id") or (isinstance(collection_count, int) and collection_count > 0):
        out["verdict"] = "catalog"
    elif parser_used and collection_count == 0:
        out["verdict"] = "empty"
    else:
        out["verdict"] = "unknown"
    return out


def _fingerprints_for(software: Optional[List[str]]) -> Dict[str, Dict[str, Any]]:
    """At most one capability URL. Known ids use CAPABILITY_PROBES, not the full map."""
    if not software:
        return {}
    software_id = software[0]
    if software_id in CAPABILITY_PROBES:
        return {software_id: dict(CAPABILITY_PROBES[software_id])}
    return _load_fingerprints([software_id])


def probe_rows(
    candidates: List[Dict[str, Any]],
    concurrency: int = 8,
    timeout: float = 10.0,
    delay: float = 0.5,
    software: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Probe candidates with per-host serialization and host-level parallelism."""
    fingerprints = _fingerprints_for(software)

    by_host: Dict[str, List[Dict[str, Any]]] = {}
    for row in candidates:
        host = row.get("host") or host_from_url(row.get("url") or "") or ""
        by_host.setdefault(host, []).append(row)

    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

    results: List[Dict[str, Any]] = []

    def _probe_host(host_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        host_results = []
        for row in host_rows:
            host_results.append(_probe_one(row, session, timeout, fingerprints))
            if len(host_rows) > 1:
                time.sleep(delay)
        return host_results

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        for host_results in pool.map(_probe_host, by_host.values()):
            results.extend(host_results)
    return results


@app.command()
def probe(
    candidates: Path = typer.Argument(..., help="Candidate JSONL from search/dedupe"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output path (default: <input>.probed.jsonl)"),
    concurrency: int = typer.Option(8, "--concurrency", help="Max hosts probed in parallel"),
    timeout: float = typer.Option(10.0, "--timeout", help="Per-request timeout seconds"),
    delay: float = typer.Option(0.5, "--delay", help="Delay between requests to the same host"),
    software: Optional[List[str]] = typer.Option(None, "--software", help="Software id(s) to fingerprint-probe (repeatable)"),
    skip_existing: bool = typer.Option(True, "--skip-existing/--include-existing", help="Skip rows marked exists:true by dedupe"),
):
    """Probe candidate hosts: liveness, title (encoding-safe), software fingerprints."""
    rows = _read_jsonl(candidates)
    if skip_existing:
        rows = [r for r in rows if not r.get("exists")]
    probed = probe_rows(
        rows,
        concurrency=concurrency,
        timeout=timeout,
        delay=delay,
        software=list(software) if software else None,
    )
    out_path = out or _default_out(candidates, ".probed.jsonl")
    _write_jsonl(out_path, probed)
    live = sum(1 for r in probed if r.get("liveness") == "live")
    matched = sum(1 for r in probed if r.get("software_id"))
    typer.echo(f"Probed {len(probed)} candidates: {live} live, {matched} fingerprint matches")
    typer.echo(f"Wrote {out_path}")
    _emit_next(f"python scripts/hunt.py ingest {out_path}")


# ---------------------------------------------------------------------------
# log
# ---------------------------------------------------------------------------


def append_hunt_log(
    kind: str,
    target: str,
    added: int,
    skipped_dupes: int = 0,
    status: str = "complete",
    notes: str = "",
    list_url: Optional[str] = None,
    date: Optional[str] = None,
    path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Validate and append one hunt row to hunts.jsonl. Returns the row."""
    if kind not in HUNT_KINDS:
        raise ValueError(
            f"Unknown hunt kind '{kind}'. Known kinds: {', '.join(sorted(HUNT_KINDS))}"
        )
    if status not in HUNT_STATUSES:
        raise ValueError(
            f"Unknown status '{status}'. Known statuses: {', '.join(sorted(HUNT_STATUSES))}"
        )
    if not target:
        raise ValueError("target is required")
    if added < 0 or skipped_dupes < 0:
        raise ValueError("added and skipped_dupes must be >= 0")
    if date is None:
        from datetime import date as _date

        date = _date.today().isoformat()
    elif not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        raise ValueError(f"date must be YYYY-MM-DD, got '{date}'")

    row = {
        "date": date,
        "kind": kind,
        "target": target,
        "list_url": list_url,
        "added": added,
        "skipped_dupes": skipped_dupes,
        "status": status,
        "notes": notes,
    }
    log_path = path or HUNTS_LOG
    with open(log_path, "a", encoding="utf8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


@app.command()
def log(
    kind: str = typer.Option(..., "--kind", help="Hunt kind (e.g. software-instance)"),
    target: str = typer.Option(..., "--target", help="Hunt target (software id, country, list name)"),
    added: int = typer.Option(..., "--added", help="Records added"),
    skipped_dupes: int = typer.Option(0, "--skipped-dupes", help="Duplicates skipped"),
    status: str = typer.Option("complete", "--status", help="complete | partial | blocked"),
    notes: str = typer.Option("", "--notes", help="Free-form hunt notes"),
    list_url: Optional[str] = typer.Option(None, "--list-url", help="Source list URL when applicable"),
    date: Optional[str] = typer.Option(None, "--date", help="YYYY-MM-DD (default: today)"),
):
    """Append one validated row to dataquality/hunts.jsonl."""
    try:
        row = append_hunt_log(
            kind=kind,
            target=target,
            added=added,
            skipped_dupes=skipped_dupes,
            status=status,
            notes=notes,
            list_url=list_url,
            date=date,
        )
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    typer.echo(f"Logged hunt: {row['kind']}/{row['target']} (+{row['added']})")


# ---------------------------------------------------------------------------
# prior / next
# ---------------------------------------------------------------------------


def decide_prior(
    target: str,
    rows: List[Dict[str, Any]],
    software_ids: set,
    today: date,
) -> Dict[str, Any]:
    """Decide stop vs continue for one hunt slice."""
    base, suffix = _split_target(target, software_ids)
    related: List[Tuple[Dict[str, Any], Optional[str]]] = []
    for row in rows:
        row_target = row.get("target") or ""
        row_base, row_suffix = _split_target(row_target, software_ids)
        notes = row.get("notes") or ""
        same = row_base == base
        notes_hit = bool(suffix) and same and _notes_have_token(notes, suffix)
        if same or row_target == target or notes_hit:
            related.append((row, row_suffix))

    def _is_this_slice(row: Dict[str, Any], row_suffix: Optional[str]) -> bool:
        row_target = row.get("target") or ""
        if suffix is None:
            return row_target == target
        if row_suffix == suffix or row_target == target:
            return True
        row_base, _ignored = _split_target(row_target, software_ids)
        return row_base == base and _notes_have_token(row.get("notes") or "", suffix or "")

    finished = [
        row
        for row, row_suffix in related
        if _recent_complete(row, today) and _is_this_slice(row, row_suffix)
    ]
    covered = sorted(
        {
            row_suffix
            for row, row_suffix in related
            if row_suffix and row.get("status") == "complete"
        }
    )
    latest = max(finished, key=lambda item: item.get("date") or "") if finished else None
    return {
        "decision": "stop" if latest else "continue",
        "base": base,
        "suffix": suffix,
        "covered": covered,
        "latest": latest,
    }


def suggest_hunts(
    rows: List[Dict[str, Any]],
    today: date,
) -> List[Dict[str, Any]]:
    """Up to five suggestions. Recently completed slices are omitted."""
    latest: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for row in rows:
        key = (row.get("kind") or "", row.get("target") or "")
        prev = latest.get(key)
        if prev is None or (row.get("date") or "") >= (prev.get("date") or ""):
            latest[key] = row

    def _tier(kind: str) -> int:
        if kind == "named-directory":
            return 0
        if kind == "country-indicators":
            return 1
        if kind == "custom-review":
            return 9
        return 5

    candidates = [row for row in latest.values() if not _recent_complete(row, today)]
    candidates.sort(key=lambda row: row.get("date") or "", reverse=True)
    candidates.sort(key=lambda row: _tier(row.get("kind") or ""))
    return candidates[:5]


def _format_suggestion(row: Dict[str, Any]) -> str:
    mark = " deprioritized" if row.get("kind") == "custom-review" else ""
    return (
        f"{row.get('kind')} {row.get('target')}{mark} "
        f"status={row.get('status')} date={row.get('date')}"
    )


@app.command()
def prior(
    target: str = typer.Option(..., "--target", help="Hunt target, optionally with a . or - slice suffix"),
):
    """Stop when this slice was completed within the last 14 days."""
    decision = decide_prior(target, _load_hunts(HUNTS_LOG), _software_id_set(), _today())
    typer.echo(f"decision: {decision['decision']}")
    if decision["covered"]:
        typer.echo("covered: " + ", ".join(decision["covered"]))
    latest = decision["latest"]
    if latest is not None:
        typer.echo(f"date: {latest.get('date')}")
        typer.echo(f"added: {latest.get('added')}")
        typer.echo(f"notes: {latest.get('notes') or ''}")
        _emit_next("none")
        return
    if decision["base"] in _software_id_set():
        _emit_next(f"python scripts/hunt.py search fofa {target}")
    else:
        _emit_next("python scripts/hunt.py budget")


@app.command("next")
def next_hunt():
    """Print up to five hunt suggestions. Does not write catalog files."""
    suggestions = suggest_hunts(_load_hunts(HUNTS_LOG), _today())
    if not suggestions:
        typer.echo("No hunt suggestions.")
        _emit_next("none")
        return
    for row in suggestions:
        typer.echo(_format_suggestion(row))
    _emit_next(f"python scripts/hunt.py prior --target {suggestions[0].get('target')}")


# ---------------------------------------------------------------------------
# ingest
# ---------------------------------------------------------------------------

_MANIFEST_KEYS = (
    "catalog_type",
    "country",
    "subregion",
    "owner_name",
    "owner_type",
    "owner_link",
    "langs",
    "description",
    "id",
)


def partition_ingest_rows(
    rows: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Keep verdict=catalog rows that are not already in the registry."""
    kept: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    for row in rows:
        verdict = row.get("verdict")
        if verdict != "catalog":
            skipped.append({"url": row.get("url"), "reason": verdict or "missing-verdict"})
            continue
        if row.get("exists") is True:
            skipped.append(
                {
                    "url": row.get("url"),
                    "reason": "exists",
                    "existing_id": row.get("existing_id"),
                }
            )
            continue
        kept.append(row)
    return kept, skipped


def manifest_from_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build an add-batch manifest. Never sets is_national."""
    manifest = []
    for row in rows:
        item: Dict[str, Any] = {"url": row.get("url")}
        title = row.get("title") or row.get("name")
        if title:
            item["name"] = title
        software = row.get("software_id") or row.get("software")
        if software:
            item["software"] = software
        for key in _MANIFEST_KEYS:
            value = row.get(key)
            if value not in (None, ""):
                item[key] = value
        manifest.append(item)
    return manifest


def _add_batch(manifest_path: Path) -> Dict[str, Any]:
    from builder import _add_batch_manifest

    return _add_batch_manifest(str(manifest_path), scheduled=True, detect=False)


def _promote_ids(ids: List[str]) -> None:
    from promote_scheduled import promote_records

    if ids:
        promote_records(dry_run=False, ids=ids, probe=True)


def _validate_ids(ids: List[str]) -> None:
    from builder import validate_yaml

    for record_id in ids:
        validate_yaml(file=None, id=record_id, changed=False)


def _ids_from_summary(summary: Dict[str, Any]) -> List[str]:
    return [Path(path).stem for path in summary.get("written_files") or []]


@app.command()
def ingest(
    probed: Path = typer.Argument(..., help="Probed JSONL with verdict and exists fields"),
):
    """Write catalog verdicts via add-batch, promote them, and validate by id."""
    rows = _read_jsonl(probed)
    kept, skipped = partition_ingest_rows(rows)
    for item in skipped:
        extra = ""
        if item.get("existing_id"):
            extra = f" existing={item['existing_id']}"
        typer.echo(f"skip {item.get('url')} reason={item['reason']}{extra}")
    written_ids: List[str] = []
    if kept:
        manifest_path = probed.with_name(probed.stem + ".manifest.jsonl")
        _write_jsonl(manifest_path, manifest_from_rows(kept))
        summary = _add_batch(manifest_path)
        written_ids = _ids_from_summary(summary)
        if written_ids:
            _promote_ids(written_ids)
            _validate_ids(written_ids)
    typer.echo(f"Ingest wrote {len(written_ids)} records")
    _emit_next(
        "python scripts/hunt.py log --kind software-instance --target TARGET --added "
        + str(len(written_ids))
    )


if __name__ == "__main__":
    app()
