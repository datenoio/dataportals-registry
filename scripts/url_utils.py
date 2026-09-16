"""URL helpers shared by builder quality checks and tests."""

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
