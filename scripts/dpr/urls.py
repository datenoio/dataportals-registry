"""URL helpers shared by builder quality checks, the hunt toolkit and tests."""

import re
from urllib.parse import urlparse


def canonicalize_url(url):
    """Normalize URL for duplicate comparison."""
    if not url or not isinstance(url, str):
        return None
    raw = url.strip()
    if not raw:
        return None
    try:
        parsed = urlparse(raw)
    except Exception:
        return None
    if not parsed.scheme or not parsed.netloc:
        return None

    scheme = (parsed.scheme or "").lower()
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if not host:
        return None

    port = parsed.port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        host = f"{host}:{port}"

    path = parsed.path or ""
    if path == "/":
        path = ""
    elif path.endswith("/"):
        path = path.rstrip("/")

    query = f"?{parsed.query}" if parsed.query else ""
    return f"{scheme}://{host}{path}{query}"


def host_from_url(url):
    """Extract host from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower() if parsed.netloc else None
    except Exception:
        return None


def normalize_host_for_id(host):
    """Normalize host to match ID format (remove dots, dashes, underscores)."""
    if not host:
        return ""
    return host.replace(".", "").replace("-", "").replace("_", "").lower()


def validate_url_format(url, field_path, issue_type):
    """Return a quality issue dict when URL lacks a scheme and netloc."""
    if not url:
        return None
    try:
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return None
        return {
            "issue_type": issue_type,
            "field": field_path,
            "current_value": url,
            "suggested_action": f"Fix URL format for {field_path} (must include scheme and host)",
        }
    except Exception:
        return {
            "issue_type": issue_type,
            "field": field_path,
            "current_value": url,
            "suggested_action": f"Fix invalid URL in {field_path}",
        }


def normalize_url(url: str) -> str:
    """Lowercase a URL and strip its scheme, leading ``www.`` and trailing slashes.

    Used for duplicate detection against scheduled records and the CKAN
    ecosystem list. Use ``canonicalize_url`` when the scheme matters.
    """
    if not url:
        return ""
    url = url.lower().strip()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url.rstrip("/")


def normalize_domain(url: str) -> str:
    """Return the host of ``normalize_url(url)``, without a port."""
    normalized = normalize_url(url)
    if not normalized:
        return ""
    return normalized.split("/")[0].split(":")[0]
