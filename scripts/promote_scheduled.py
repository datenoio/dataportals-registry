#!/usr/bin/env python3
"""Promote scheduled records to entities: selective, subregion-aware, liveness-gated.

For each scheduled file:
- Known country (EU, CN, FR, World, etc.): move to entities/{country}/{Federal|SUBREGION}/{type}/
- Unknown: infer country from coverage, owner, link, and data/reference/country_hints.yaml
- Records with a valid owner/coverage subregion are routed to {CC}/{SUBREGION}/{type}/
- Update status to active (unless staging/dev)
- With --probe, classify link liveness first: dead records stay in scheduled

Commands:
- (default)            promote records (--dry-run, --id, --probe)
- review-scheduled     read-only triage report for the whole queue
"""

from __future__ import annotations

import os
import sys

# Allow importing from scripts/
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
import typer
import yaml

from check_liveness import classify_liveness, probe_url

BASE_DIR = Path(__file__).parent.parent
SCHEDULED_DIR = BASE_DIR / "data" / "scheduled"
ENTITIES_DIR = BASE_DIR / "data" / "entities"
COUNTRY_HINTS_PATH = BASE_DIR / "data" / "reference" / "country_hints.yaml"
DEFAULT_REVIEW_OUT = BASE_DIR / "dataquality" / "scheduled_review.jsonl"

# Staging/dev sites - keep as inactive
STAGING_PATTERNS = ("staging", "dev.", "demo.", "test.", "derilinx.com", "klldev", "disldev")

# catalog_type -> subdir mapping (from constants.MAP_CATALOG_TYPE_SUBDIR + opendata default)
TYPE_TO_SUBDIR = {
    "Geoportal": "geo",
    "Open data portal": "opendata",
    "Scientific data repository": "scientific",
    "Indicators catalog": "indicators",
    "Microdata catalog": "microdata",
    "Machine learning catalog": "ml",
    "Metadata catalog": "metadata",
    "API Catalog": "api",
    "Data search engine": "search",
    "Data marketplace": "marketplace",
    "Other": "other",
    "Datasets list": "opendata",
    "General research repository": "scientific",
}

app = typer.Typer(help="Promote scheduled records to entities (selective, subregion-aware, liveness-gated).")


def get_subdir_from_path(rel_path: str) -> str:
    """Extract type subdir from scheduled path like EU/geo/ or Unknown/opendata/."""
    parts = Path(rel_path).parts
    if len(parts) >= 2:
        return parts[1]  # geo, opendata, scientific, etc.
    return "opendata"


def get_country_from_path(rel_path: str) -> str | None:
    """Extract country from scheduled path like EU/geo/ or Unknown/opendata/."""
    parts = Path(rel_path).parts
    if len(parts) >= 1:
        return parts[0]  # EU, CN, Unknown, World, etc.
    return None


def get_country_from_record(record: dict) -> tuple[str | None, str | None]:
    """Return (country_id, country_name) from coverage or owner. None if Unknown."""
    cov = record.get("coverage") or []
    if cov:
        loc = cov[0].get("location", {})
        country = loc.get("country", {})
        cid = country.get("id")
        cname = country.get("name")
        if cid and str(cid) not in ("Unknown", ""):
            return (str(cid), cname or cid)

    owner = record.get("owner") or {}
    owner_loc = owner.get("location") or {}
    owner_country = owner_loc.get("country") or {}
    oid = owner_country.get("id")
    oname = owner_country.get("name")
    if oid and str(oid) not in ("Unknown", ""):
        return (str(oid), oname or oid)

    return (None, None)


def infer_country_from_link(link: str) -> str | None:
    """Infer country from domain TLD. Returns country_id or None."""
    if not link:
        return None
    try:
        parsed = urlparse(link if "://" in link else f"https://{link}")
        domain = (parsed.netloc or link).lower().replace("www.", "").split("/")[0]

        gov_tlds = {
            ".gov.uk": "GB", ".gov.au": "AU", ".gov.ca": "CA", ".gov.nz": "NZ",
            ".gov.sg": "SG", ".gov.in": "IN", ".gov.br": "BR", ".gov.mx": "MX",
            ".gov.ar": "AR", ".gov.fr": "FR", ".gov.de": "DE", ".gov.nl": "NL",
            ".gov.be": "BE", ".gov.es": "ES", ".gov.it": "IT", ".gov.pl": "PL",
            ".gov.cn": "CN", ".gov.jp": "JP", ".gov.kr": "KR", ".gov.ru": "RU",
            ".gov.ua": "UA", ".gov.tr": "TR", ".gov.gr": "GR", ".gov.pt": "PT",
            ".gov.fi": "FI", ".gov.se": "SE", ".gov.no": "NO", ".gov.dk": "DK",
            ".gov.ie": "IE", ".gov.at": "AT", ".gov.ch": "CH", ".gov.il": "IL",
            ".gov.za": "ZA", ".gov.ke": "KE", ".gov.pk": "PK", ".gov.bd": "BD",
            ".gov.vn": "VN", ".gov.id": "ID", ".gov.th": "TH", ".gov.my": "MY",
            ".gov.co": "CO", ".gov.cl": "CL", ".gov.pe": "PE", ".gov.ec": "EC",
            ".gov.mk": "MK", ".gov.me": "ME", ".gov.ge": "GE", ".gov.mn": "MN",
        }
        for suffix, cid in gov_tlds.items():
            if domain.endswith(suffix):
                return cid

        if domain.endswith(".gov") and not any(
            domain.endswith(f".gov.{tld}") for tld in ["uk", "au", "ca", "nz", "sg", "in", "br", "mx", "ar"]
        ):
            return "US"

        tld_2letter = domain.split(".")[-1] if "." in domain else ""
        tld_to_country = {
            "uk": "GB", "au": "AU", "ca": "CA", "nz": "NZ", "sg": "SG", "in": "IN",
            "br": "BR", "mx": "MX", "ar": "AR", "fr": "FR", "de": "DE", "nl": "NL",
            "be": "BE", "es": "ES", "it": "IT", "pl": "PL", "cz": "CZ", "at": "AT",
            "ch": "CH", "se": "SE", "no": "NO", "dk": "DK", "fi": "FI", "ie": "IE",
            "jp": "JP", "kr": "KR", "cn": "CN", "tw": "TW", "hk": "HK", "mo": "MO",
            "ru": "RU", "ua": "UA", "by": "BY", "kz": "KZ", "tr": "TR", "il": "IL",
            "gr": "GR", "pt": "PT", "ro": "RO", "hu": "HU", "bg": "BG", "hr": "HR",
            "si": "SI", "sk": "SK", "rs": "RS", "ba": "BA", "me": "ME", "mk": "MK",
            "al": "AL", "ee": "EE", "lv": "LV", "lt": "LT", "eu": "EU",
            "co": "CO", "cl": "CL", "pe": "PE", "ec": "EC", "uy": "UY", "py": "PY",
            "bo": "BO", "cr": "CR", "pa": "PA", "gt": "GT", "hn": "HN", "ni": "NI",
            "vn": "VN", "ph": "PH", "my": "MY", "id": "ID", "pk": "PK", "bd": "BD",
            "th": "TH", "kh": "KH", "la": "LA", "mm": "MM", "np": "NP", "lk": "LK",
            "sn": "SN", "ci": "CI", "gh": "GH", "ng": "NG", "eg": "EG", "ma": "MA",
            "tn": "TN", "dz": "DZ", "ly": "LY", "sd": "SD", "et": "ET", "tz": "TZ",
            "ug": "UG", "rw": "RW", "cm": "CM", "cd": "CD", "ao": "AO", "mz": "MZ",
            "zw": "ZW", "bw": "BW", "na": "NA", "ls": "LS", "mu": "MU", "sc": "SC",
            "km": "KM", "mg": "MG", "mv": "MV", "af": "AF", "uz": "UZ", "tm": "TM",
            "tj": "TJ", "kg": "KG", "ge": "GE", "am": "AM", "az": "AZ", "ir": "IR",
        }
        if tld_2letter in tld_to_country:
            return tld_to_country[tld_2letter]
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Data-driven country hints
# ---------------------------------------------------------------------------


def load_country_hints(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Load substring country hints from data/reference/country_hints.yaml."""
    hint_path = path or COUNTRY_HINTS_PATH
    if not hint_path.exists():
        return []
    with open(hint_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("hints") or []


def match_country_hint(haystack: str, hints: List[Dict[str, Any]]) -> Optional[str]:
    """Return the country of the first matching hint, evaluated in file order.

    Hint forms:
      - {pattern: "brasilio", country: BR}   # substring match
      - {all: ["opendatasoft", "zastrug"], country: RS}  # every substring must appear
    """
    for hint in hints:
        if "all" in hint:
            if all(str(p).lower() in haystack for p in hint["all"]):
                return hint["country"]
        elif hint.get("pattern") and str(hint["pattern"]).lower() in haystack:
            return hint["country"]
    return None


def infer_country_for_unknown(record: dict, hints: Optional[List[Dict[str, Any]]] = None) -> str:
    """Infer country for Unknown records. Returns country_id, default World."""
    country_id, _ = get_country_from_record(record)
    if country_id:
        return country_id

    link = record.get("link") or ""
    cid = infer_country_from_link(link)
    if cid:
        return cid

    rid = (record.get("id") or "").lower()
    haystack = f"{rid} {link.lower()}"
    if hints is None:
        hints = load_country_hints()
    matched = match_country_hint(haystack, hints)
    if matched:
        return matched

    return "World"


# ---------------------------------------------------------------------------
# Subregion routing
# ---------------------------------------------------------------------------


def resolve_subregion(record: dict, country_id: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Return (subregion_id, warning) for records carrying a subregion.

    Reads owner.location.subregion.id first, then coverage[].location.subregion.id.
    Unknown codes produce a warning and a Federal/ fallback (None).
    """
    from builder import validate_subregion  # lazy: builder is a heavy import

    candidates: List[str] = []
    owner_loc = (record.get("owner") or {}).get("location") or {}
    owner_sub = (owner_loc.get("subregion") or {}).get("id")
    if owner_sub:
        candidates.append(str(owner_sub))
    for cov in record.get("coverage") or []:
        cov_sub = ((cov.get("location") or {}).get("subregion") or {}).get("id")
        if cov_sub and str(cov_sub) not in candidates:
            candidates.append(str(cov_sub))

    if not candidates:
        return None, None
    for sid in candidates:
        try:
            validate_subregion(sid, country_id if country_id not in (None, "World", "Unknown") else None)
            return sid.strip().upper(), None
        except ValueError:
            continue
    return None, f"unknown subregion(s) {candidates}; falling back to Federal/"


def apply_subregion_level(record: dict, subregion_id: str) -> None:
    """Ensure owner/coverage locations carrying the subregion have level 30."""
    owner = record.get("owner") or {}
    owner_loc = owner.get("location")
    if isinstance(owner_loc, dict) and (owner_loc.get("subregion") or {}).get("id"):
        owner_loc["level"] = 30
    for cov in record.get("coverage") or []:
        loc = cov.get("location")
        if isinstance(loc, dict) and (loc.get("subregion") or {}).get("id"):
            loc["level"] = 30


def is_staging_or_dev(record: dict) -> bool:
    """True if record appears to be a staging/dev environment."""
    link = (record.get("link") or "").lower()
    rid = (record.get("id") or "").lower()
    desc = (record.get("description") or "").lower()
    for p in STAGING_PATTERNS:
        if p in link or p in rid or p in desc:
            return True
    return False


def get_subdir_from_catalog_type(catalog_type: str, path_type: str) -> str:
    """Get target subdir from catalog_type or path fallback."""
    if catalog_type and catalog_type in TYPE_TO_SUBDIR:
        return TYPE_TO_SUBDIR[catalog_type]
    return path_type if path_type in TYPE_TO_SUBDIR.values() else "opendata"


def collect_scheduled(scheduled_dir: Optional[Path] = None) -> List[Tuple[Path, str, str]]:
    """Collect (path, country_from_path, type_from_path) for every scheduled YAML."""
    base = scheduled_dir or SCHEDULED_DIR
    scheduled_files: List[Tuple[Path, str, str]] = []
    for yaml_path in sorted(base.rglob("*.yaml")):
        try:
            rel = yaml_path.relative_to(base)
            country = get_country_from_path(str(rel))
            subdir = get_subdir_from_path(str(rel))
            if country and subdir:
                scheduled_files.append((yaml_path, country, subdir))
        except ValueError:
            continue
    return scheduled_files


# ---------------------------------------------------------------------------
# Promotion
# ---------------------------------------------------------------------------


def promote_records(
    dry_run: bool = False,
    ids: Optional[List[str]] = None,
    probe: bool = False,
    timeout: float = 10.0,
    scheduled_dir: Optional[Path] = None,
    entities_dir: Optional[Path] = None,
) -> Dict[str, int]:
    """Promote scheduled records. Returns counters."""
    base = scheduled_dir or SCHEDULED_DIR
    entities = entities_dir or ENTITIES_DIR

    if not base.exists():
        typer.echo(f"Directory not found: {base}")
        return {"promoted": 0, "skipped_dup": 0, "dead": 0, "errors": 0}

    scheduled_files = collect_scheduled(base)

    if ids:
        wanted = set(ids)
        by_id: Dict[str, Tuple[Path, str, str]] = {}
        for entry in scheduled_files:
            by_id[entry[0].stem] = entry
        missing = wanted - set(by_id)
        if missing:
            typer.echo(
                f"Error: --id value(s) not found in {base}: {', '.join(sorted(missing))}",
                err=True,
            )
            raise typer.Exit(1)
        scheduled_files = [by_id[i] for i in ids]

    if not scheduled_files:
        typer.echo("No YAML files in data/scheduled/")
        return {"promoted": 0, "skipped_dup": 0, "dead": 0, "errors": 0}

    if dry_run:
        typer.echo("DRY RUN - no files will be moved\n")
    typer.echo(f"Processing {len(scheduled_files)} scheduled records\n")

    hints = load_country_hints()
    session = None
    if probe:
        session = requests.Session()
        session.headers.update({"User-Agent": "dataportals-registry-promote/1.0"})

    promoted = 0
    skipped_dup = 0
    dead_count = 0
    updated_coverage = 0
    errors: List[Tuple[Path, str]] = []

    for yaml_path, path_country, path_type in scheduled_files:
        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append((yaml_path, str(e)))
            continue
        if not isinstance(data, dict):
            errors.append((yaml_path, "Invalid YAML structure"))
            continue

        rid = data.get("id", "unknown")
        catalog_type = data.get("catalog_type", "")
        target_subdir = get_subdir_from_catalog_type(catalog_type, path_type)

        # Liveness gate
        if probe:
            link = (data.get("link") or "").strip()
            http_code, error, _final = probe_url(link, session, timeout=timeout)
            liveness = classify_liveness(http_code, error)
            if liveness == "dead":
                dead_count += 1
                typer.echo(f"  [dead] {rid} stays in scheduled ({error or f'HTTP {http_code}'})")
                continue
            if liveness in ("inconclusive", "error"):
                typer.echo(f"  [warn] {rid} liveness={liveness}; promoting anyway")
            else:
                typer.echo(f"  [probe] {rid} {liveness} (HTTP {http_code})")

        if path_country == "Unknown":
            country_id = infer_country_for_unknown(data, hints)

            # Update coverage if it was Unknown
            cov = data.get("coverage") or []
            if cov:
                loc = cov[0].get("location", {})
                curr_country = loc.get("country", {})
                curr_id = (curr_country.get("id") or "").strip()
                if curr_id in ("Unknown", "") and country_id:
                    try:
                        from constants import COUNTRIES
                        cname = COUNTRIES.get(country_id, country_id)
                    except ImportError:
                        cname = country_id
                    cov[0]["location"]["country"] = {"id": country_id, "name": cname}
                    updated_coverage += 1

            # Update owner location if Unknown
            owner = data.get("owner") or {}
            owner_loc = owner.get("location") or {}
            owner_country = owner_loc.get("country") or {}
            if (owner_country.get("id") or "").strip() in ("Unknown", "") and country_id:
                try:
                    from constants import COUNTRIES
                    cname = COUNTRIES.get(country_id, country_id)
                except ImportError:
                    cname = country_id
                owner["location"] = owner.get("location") or {}
                owner["location"]["country"] = {"id": country_id, "name": cname}
                data["owner"] = owner
        else:
            country_id = path_country

        # Subregion-aware routing
        subregion_id, sub_warn = resolve_subregion(data, country_id)
        if sub_warn:
            typer.echo(f"  [warn] {rid}: {sub_warn}")
        if subregion_id:
            admin_dir = subregion_id
            apply_subregion_level(data, subregion_id)
        else:
            admin_dir = "Federal"

        # Update status
        if is_staging_or_dev(data):
            data["status"] = "inactive"
        elif (data.get("status") or "").strip() == "scheduled":
            data["status"] = "active"

        target_dir = entities / country_id / admin_dir / target_subdir
        target_path = target_dir / yaml_path.name

        if target_path.exists() and target_path != yaml_path:
            # Duplicate - entity already exists, remove scheduled copy
            if not dry_run:
                yaml_path.unlink()
            skipped_dup += 1
            typer.echo(f"  [skip dup] {rid} -> already in entities")
            continue

        if dry_run:
            typer.echo(f"  {rid} -> {country_id}/{admin_dir}/{target_subdir}/ (status={data.get('status')})")
            promoted += 1
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        target_path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        yaml_path.unlink()
        promoted += 1
        typer.echo(f"  {rid} -> {country_id}/{admin_dir}/{target_subdir}/ (status={data.get('status')})")

    if errors:
        typer.echo(f"\nErrors ({len(errors)}):")
        for path, err in errors[:10]:
            typer.echo(f"  {path}: {err}")
        if len(errors) > 10:
            typer.echo(f"  ... and {len(errors) - 10} more")

    typer.echo(
        f"\nPromoted: {promoted}, updated coverage: {updated_coverage}, "
        f"skipped (dup): {skipped_dup}, kept dead: {dead_count}"
    )

    if not dry_run and promoted > 0:
        typer.echo("\nNext steps:")
        typer.echo("  python scripts/builder.py assign")
        typer.echo("  python scripts/builder.py validate-yaml")
        typer.echo("  python scripts/builder.py build")

    return {
        "promoted": promoted,
        "skipped_dup": skipped_dup,
        "dead": dead_count,
        "errors": len(errors),
    }


@app.callback(invoke_without_command=True)
def promote(
    ctx: typer.Context,
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview moves without writing"),
    ids: Optional[List[str]] = typer.Option(None, "--id", help="Promote only these record ids (repeatable)"),
    probe: bool = typer.Option(False, "--probe", help="Probe link liveness before moving; dead records stay"),
    timeout: float = typer.Option(10.0, "--timeout", help="Per-request probe timeout seconds"),
):
    """Promote scheduled records to entities (default command)."""
    if ctx.invoked_subcommand is not None:
        return
    promote_records(dry_run=dry_run, ids=ids, probe=probe, timeout=timeout)


# ---------------------------------------------------------------------------
# review-scheduled
# ---------------------------------------------------------------------------


def review_queue(
    probe: bool = True,
    country: Optional[str] = None,
    concurrency: int = 8,
    timeout: float = 10.0,
    scheduled_dir: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Build a triage report for the scheduled queue. Never moves or modifies files."""
    from hunt import _build_export_indexes, dedupe_rows, probe_rows

    base = scheduled_dir or SCHEDULED_DIR
    hints = load_country_hints()
    rows: List[Dict[str, Any]] = []

    for yaml_path, path_country, path_type in collect_scheduled(base):
        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except Exception as e:
            rows.append({"id": yaml_path.stem, "path": str(yaml_path), "bucket": "needs-review",
                         "notes": f"YAML error: {e}"})
            continue
        if not isinstance(data, dict):
            rows.append({"id": yaml_path.stem, "path": str(yaml_path), "bucket": "needs-review",
                         "notes": "invalid YAML structure"})
            continue

        rid = data.get("id", yaml_path.stem)
        if path_country == "Unknown":
            country_id = infer_country_for_unknown(data, hints)
        else:
            country_id = path_country
        subregion_id, sub_warn = resolve_subregion(data, country_id)

        row: Dict[str, Any] = {
            "id": rid,
            "link": data.get("link"),
            "path": str(yaml_path.relative_to(base)),
            "country": country_id,
            "subregion": subregion_id,
            "catalog_type": data.get("catalog_type"),
            "staging": is_staging_or_dev(data),
        }
        notes = []
        if sub_warn:
            notes.append(sub_warn)
        if row["staging"]:
            notes.append("staging/dev host; promotes as inactive")
        row["notes"] = "; ".join(notes)
        rows.append(row)

    if country:
        wanted = country.upper()
        rows = [r for r in rows if (r.get("country") or "").upper() == wanted]

    # Batch duplicate check against entities exports
    try:
        ids, urls, hosts = _build_export_indexes()
        candidates = [
            {"url": r.get("link") or "", "host": "", "id": r.get("id")} for r in rows
        ]
        deduped = dedupe_rows(candidates, ids, urls, hosts)
        for row, dup in zip(rows, deduped):
            row["exists"] = dup.get("exists", False)
            if dup.get("existing_id"):
                row["existing_id"] = dup["existing_id"]
    except ValueError as e:
        typer.echo(f"Warning: duplicate check skipped ({e})")
        for row in rows:
            row["exists"] = False

    # Liveness probe (bounded concurrency, per-host politeness)
    if probe:
        to_probe = [r for r in rows if not r.get("exists")]
        probed = probe_rows(
            [{"url": r.get("link") or "", "host": "", "id": r.get("id")} for r in to_probe],
            concurrency=concurrency,
            timeout=timeout,
            delay=0.5,
        )
        by_id = {p.get("id"): p for p in probed}
        for row in rows:
            p = by_id.get(row.get("id"))
            if p:
                row["liveness"] = p.get("liveness")
                row["http_code"] = p.get("http_code")

    # Buckets
    for row in rows:
        if row.get("exists"):
            row["bucket"] = "duplicate"
        elif probe and row.get("liveness") == "dead":
            row["bucket"] = "dead"
        elif probe and row.get("liveness") in ("inconclusive", "error"):
            row["bucket"] = "needs-review"
        elif row.get("staging"):
            row["bucket"] = "needs-review"
        else:
            row["bucket"] = "promote-ready"
    return rows


@app.command("review-scheduled")
def review_scheduled(
    probe: bool = typer.Option(True, "--probe/--no-probe", help="Probe link liveness"),
    country: Optional[str] = typer.Option(None, "--country", help="Only review records inferred for this country"),
    out: Optional[Path] = typer.Option(None, "--out", help=f"JSONL report path (default: {DEFAULT_REVIEW_OUT})"),
    concurrency: int = typer.Option(8, "--concurrency", help="Max hosts probed in parallel"),
    timeout: float = typer.Option(10.0, "--timeout", help="Per-request probe timeout seconds"),
):
    """Read-only triage report for the scheduled queue (never moves files)."""
    rows = review_queue(probe=probe, country=country, concurrency=concurrency, timeout=timeout)

    buckets: Dict[str, int] = {}
    for row in rows:
        buckets[row["bucket"]] = buckets.get(row["bucket"], 0) + 1

    for row in rows:
        live = f", {row['liveness']}" if row.get("liveness") else ""
        dup = f", dup of {row['existing_id']}" if row.get("existing_id") else ""
        notes = f" — {row['notes']}" if row.get("notes") else ""
        typer.echo(f"  [{row['bucket']}] {row['id']} ({row.get('country')}{live}{dup}){notes}")

    typer.echo("\nSummary:")
    for bucket in ("promote-ready", "needs-review", "dead", "duplicate"):
        if bucket in buckets:
            typer.echo(f"  {bucket}: {buckets[bucket]}")
    typer.echo(f"  total: {len(rows)}")

    out_path = out or DEFAULT_REVIEW_OUT
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    typer.echo(f"\nWrote {out_path}")


def main() -> None:
    """Backward-compatible entry point: python scripts/promote_scheduled.py [--dry-run]."""
    app()


if __name__ == "__main__":
    main()
