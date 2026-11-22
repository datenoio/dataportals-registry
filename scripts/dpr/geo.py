"""Country inference helpers shared by the registry scripts."""

from urllib.parse import urlparse


def infer_country_from_link(link: str) -> str | None:
    """Infer country from domain TLD. Returns country_id or None.

    ``.gov.xx`` suffixes map to their country, a bare ``.gov`` maps to the
    United States, and two-letter country-code TLDs map to their country.
    Generic TLDs (``.org``, ``.com``, ``.edu``, ...) return None.
    """
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
