#!/usr/bin/env python3
"""Discovery hunt toolkit: search / dedupe / probe / log.

One tested implementation of the plumbing discovery sessions used to rebuild as
throwaway scripts:

- ``search fofa|censys QUERY`` — query internet-map APIs (credentials from the
  environment), paginate, back off on rate limits, write normalized candidates.
- ``dedupe candidates.jsonl`` — batch duplicate-check against dataset exports
  (DuckDB read-only, automatic parquet fallback on lock).
- ``probe candidates.jsonl`` — polite bounded-concurrency GET with encoding
  detection, liveness classification, and optional software fingerprint probes.
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
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
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
FOFA_FIELDS = "host,ip,port,protocol,title,domain"
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
def search(
    provider: str = typer.Argument(..., help="Search provider: fofa or censys"),
    query: str = typer.Argument(..., help="Query in the provider's syntax"),
    out: Path = typer.Option(Path("candidates.jsonl"), "--out", help="Output JSONL path"),
    size: int = typer.Option(100, "--size", help="Results per page"),
    max_pages: int = typer.Option(1, "--max-pages", help="Maximum pages to fetch"),
    max_retries: int = typer.Option(5, "--max-retries", help="Retries on 429/5xx with backoff"),
):
    """Query FOFA or Censys and write normalized candidate JSONL rows."""
    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    try:
        if provider == "fofa":
            results = _fofa_search(session, query, size, max_pages, max_retries)
        elif provider == "censys":
            results = _censys_search(session, query, size, max_pages, max_retries)
        else:
            logger_error = f"Unknown provider '{provider}': use fofa or censys"
            typer.echo(logger_error, err=True)
            raise typer.Exit(1)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)

    _write_jsonl(out, results)
    typer.echo(f"Wrote {len(results)} candidates to {out}")


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


def _probe_one(
    row: Dict[str, Any],
    session: requests.Session,
    timeout: float,
    fingerprints: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Probe one candidate: root GET, liveness, title, optional fingerprint probes."""
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

    # Never bypass 401/403: record and move on.
    if http_code in (401, 403):
        out["auth_required"] = True

    if fingerprints and http_code and 200 <= http_code < 400:
        base = url if url.endswith("/") else url + "/"
        for sw, entry in fingerprints.items():
            probe_url = urljoin(base, entry["url"].lstrip("/"))
            try:
                fp_response = session.get(probe_url, timeout=timeout, allow_redirects=True)
            except requests.exceptions.RequestException:
                continue
            if fp_response.status_code != 200:
                continue
            expected = entry.get("expected_mime")
            if expected:
                expected_list = expected if isinstance(expected, list) else [expected]
                content_type = (fp_response.headers.get("Content-Type") or "").split(";")[0].strip()
                if content_type not in expected_list:
                    continue
            out["software_id"] = sw
            out["fingerprint_url"] = probe_url
            break
    return out


def probe_rows(
    candidates: List[Dict[str, Any]],
    concurrency: int = 8,
    timeout: float = 10.0,
    delay: float = 0.5,
    software: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Probe candidates with per-host serialization and host-level parallelism."""
    fingerprints = _load_fingerprints(software) if software else {}

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


if __name__ == "__main__":
    app()
