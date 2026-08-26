"""Semantics of properties.is_national.

`is_national` means the catalog is the country's official catalog of that
type — not that a central/federal agency owns it.

Keep true only for:
- the cross-government national open-data portal (typically one current, plus
  one documented legacy)
- the NSDI / national geoportal / INSPIRE node (typically one or two)
- NSO statistical products (indicators, microdata, IMF NSDP, Open Data for
  Africa country pages)
- a national metadata registry when that is the country MDR

Unset (false) for agency, thematic, scientific/domain, subnational, and
non-government catalogs. Federal/`Central government` ownership is already
expressed by path, owner.type, and coverage.level.

Do not bulk-set this flag from a Federal/ path or a .gov/.mil hostname.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional, Tuple

CATALOG_TYPE_FOLDERS = frozenset(
    {
        "opendata",
        "geo",
        "scientific",
        "indicators",
        "microdata",
        "ml",
        "search",
        "api",
        "marketplace",
        "metadata",
        "other",
    }
)

SPECIAL_ROOTS = frozenset(
    {
        "World",
        "EU",
        "Africa",
        "ASEAN",
        "Oceania",
        "Americas",
        "Asia",
        "Europe",
        "Antarctica",
        "Caribbean",
        "LatinAmerica",
        "CentralAmerica",
        "International",
    }
)

SCIENTIFIC_TYPES = frozenset(
    {
        "Scientific data repository",
        "General research repository",
    }
)

SCIENTIFIC_SOFTWARE = frozenset(
    {
        "dspace",
        "dataverse",
        "invenio",
        "inveniordm",
        "pure",
        "esploro",
        "eprints",
        "fedora",
        "hyrax",
        "samvera",
        "islandora",
        "opus",
        "phaidra",
        "erddap",
        "thredds",
        "ipt",
        "gbifipt",
        "converis",
        "figshare",
        "osf",
        "zenodo",
    }
)

NON_CENTRAL_OWNER_TYPES = frozenset(
    {
        "Academy",
        "Business",
        "Community",
        "Regional government",
        "Local government",
        "Civil society",
    }
)

_NAT_OD_URL = re.compile(
    r"""https?://(www\.)?(
        catalog\.data\.gov|
        data\.gov(/|$)|
        data\.gouv\.fr|
        data\.gov\.[a-z.]+|
        datos\.gob(\.[a-z.]+)?|
        dados\.gov\.[a-z.]+|
        data\.go\.id|
        katalog\.data\.go\.id|
        govdata\.de|
        data\.overheid\.nl|
        data\.public\.lu|
        opendata\.gov\.[a-z.]+|
        datosabiertos\.gob\.[a-z.]+|
        data\.europa\.eu
    )""",
    re.I | re.X,
)

_NAT_OD_NAME = re.compile(
    r"""(
        national\s+open\s+data|
        portal\s+nacional\s+de\s+datos|
        plataforma\s+nacional\s+de\s+datos|
        home\s+of\s+the\s+.+government\s+open\s+data|
        open\s+government\s+data\s+(of|portal|catalogue|catalog|platform)|
        portal\s+(brasileiro\s+de\s+)?dados\s+abiertos|
        portal\s+(brasileiro\s+de\s+)?dados\s+abertos|
        satu\s+data\s+indonesia|
        sveriges\s+dataportal|
        korea\s+public\s+data\s+portal|
        greece\s+national\s+data|
        swiss\s+open\s+government|
        malaysia\s+open\s+data\s+portal|
        portail\s+open\s+data|
        unified\s+open\s+data\s+portal|
        national\s+data\s+portal|
        open\s+data\s+portal\s+of\s+the
    )""",
    re.I | re.X,
)

_NAT_GEO_NAME = re.compile(
    r"""(
        national\s+(geo)?portal|
        geoportal(e)?\s+(nacional|national)|
        \bnsdi\b|
        national\s+spatial\s+data|
        ethio-nsdi|
        inspire\s+(geoportal|portal|node)|
        geoportail|
        g[eé]oportail|
        paikkatietoikkuna|
        n[aá]rodn[yýé]\s+geoport[aá]l|
        geoport[aá]l\s+n[aá]rodn|
        geospatial\s+information\s+sharing
    )""",
    re.I | re.X,
)

_NSO = re.compile(
    r"""(
        \bnsdp\b|
        national\s+summary\s+data|
        open\s+data\s+for\s+africa|
        opendataforafrica|
        national\s+statistical\s+(office|institute|bureau|agency|service|committee)|
        national\s+statistics\s+(office|institute|bureau|agency|service|committee)|
        statistical\s+(office|institute|bureau|agency|service|committee)|
        office\s+(for\s+)?national\s+statistics|
        bureau\s+(of\s+)?(national\s+)?statist|
        instituto\s+nacional\s+de\s+estad|
        instituto\s+brasileiro\s+de\s+geografia|
        haut\s+commissariat\s+au\s+plan|
        census\s+bureau|
        australian\s+bureau\s+of\s+statistics|
        statistics\s+(canada|south\s+africa|indonesia|korea|japan)|
        \bibge\b|\binegi\b|\binsee\b|\bistat\b|\bdestatis\b|\brosstat\b|
        \babs\.gov\b|\bons\.gov\b|\bstatcan\b|\bstats\s+sa\b|
        \bins[ée]e\b|\bcso\b|\bnso\b|\bnbs\b|\bczso\b|\bksh\b|
        lao\s+statistics\s+bureau|
        national\s+bureau\s+of\s+statistics|
        national\s+institute\s+of\s+statistics|
        central\s+statistical|
        \bstatistics\s+(?!service|division|branch|department|unit|section)[a-záéíóúäöüñ]
    )""",
    re.I | re.X,
)

_DIGITAL_GOV = re.compile(
    r"""(
        digital\s+(government|agency|service|transformation|technologies)|
        gsa\s+technology\s+transformation|
        \bdinum\b|\betalab\b|
        agency\s+for\s+digital|
        e-government|egovernment|
        ministry\s+of\s+e-government|
        ministry\s+of\s+digital|
        open\s+data\s+(office|initiative)|
        secretar[íi]a\s+de\s+gobierno\s+y\s+transformaci|
        autorit[aá].{0,40}innovaci[oó]n|
        saudi\s+data|
        agency\s+for\s+information\s+society|
        fps\s+policy\s+and\s+support|\bbosa\b
    )""",
    re.I | re.X,
)

_MAPPING = re.compile(
    r"""(
        national\s+(mapping|geospatial\s+information|geographic\s+information|land\s+survey)|
        cadastr(e|al)\s+(agency|authority|office)|
        lands?\s+and\s+surveys|
        ordnances?\s+survey|
        \bign\b|
        geospatial\s+information\s+(authority|agency)|
        spatial\s+data\s+infrastructure|
        \bnsdi\b|
        federal\s+geographic\s+data\s+committee|
        \bfgdc\b|
        lantm[aä]teriet|
        geodataportalen
    )""",
    re.I | re.X,
)

_LINE_MINISTRY = re.compile(
    r"""(
        ministry\s+of\s+(health|agriculture|education|environment|energy|
            defence|defense|transport|interior|finance|labour|labor|culture|
            tourism|mining|petroleum|water|fisheries|justice|mines|sports|
            public\s+administration)|
        minist[eè]re\s+(de|des|du)\s+|
        department\s+of\s+(health|agriculture|energy|defense|interior|
            transportation|education|labor|veterans|homeland|commerce|justice|
            state|treasury)|
        \bnasa\b|national\s+aeronautics|
        \bnoaa\b|national\s+oceanic|
        \bnih\b|national\s+institutes\s+of\s+health|
        \bnlm\b|national\s+library\s+of\s+medicine|
        \busgs\b|geological\s+survey|
        \busda\b|
        \bfaa\b|federal\s+aviation|
        \bhrsa\b|
        national\s+park\s+service|
        forest\s+service|
        national\s+(cancer|weather)\s+|
        \binps\b|\binail\b|
        \bsenat\b|\bsénat\b|assembl[eé]e\s+nationale|
        c[aá]mara\s+dos\s+deputados|
        \bparliament\b|\bdiputados\b|
        \bmedicaid\b|\bfcc\b|small\s+business\s+administration
    )""",
    re.I | re.X,
)

_THEMATIC = re.compile(
    r"""(
        resource\s+contracts|
        mapbiomas|
        mining\s+cadastre|
        cadastre\s+minier|
        health\s+workforce|
        \bhmis\b|\bemis\b|
        forest\s+monitoring|
        wis2(box|node)|
        \berddap\b|\bthredds\b|
        biosample|sequence\s+read\s+archive|\bsra\b|\bgenbank\b|
        \bmuseum\b|\bgenebank\b|
        child\s+abuse|
        grand\s+canyon|
        astrogeology|
        gbif\s+ipt|\bipt\s+of\b|\bipt\s+oficial\b|
        data\s+theme|\bngda\b
    )""",
    re.I | re.X,
)

_LEGACY_OD = re.compile(
    r"(legacy|previous|anterior|archive|catálogo anterior|catalogue anterior)",
    re.I,
)

_DIGITAL_OD_SUCCESSOR = re.compile(
    r"datavejviser|sveriges\s+dataportal|dataportal\.se",
    re.I,
)

Verdict = Tuple[bool, str]


def _text(record: dict) -> str:
    owner = record.get("owner") or {}
    return " ".join(
        [
            str(record.get("name") or ""),
            str(record.get("description") or ""),
            str(owner.get("name") or ""),
            str(record.get("link") or ""),
        ]
    )


def country_from_path(rel_path: str) -> str:
    parts = Path(rel_path.replace("\\", "/")).parts
    return parts[0] if parts else ""


def is_subnational_path(rel_path: str) -> bool:
    """True when the YAML lives under an ISO-3166-2 subregion folder."""
    parts = Path(rel_path.replace("\\", "/")).parts
    if len(parts) < 3:
        return False
    mid = parts[1]
    if mid == "Federal":
        return False
    if mid in CATALOG_TYPE_FOLDERS:
        return False
    return True


def is_national_open_data(record: dict) -> bool:
    name = record.get("name") or ""
    link = record.get("link") or ""
    return bool(_NAT_OD_URL.search(link) or _NAT_OD_NAME.search(name))


def classify_is_national(record: dict, rel_path: str = "") -> Verdict:
    """Return (should_be_true, reason_code).

    `rel_path` is the path relative to data/entities (or scheduled).
    """
    rel_path = (rel_path or record.get("_file_path") or "").replace("\\", "/")
    country = country_from_path(rel_path)
    ctype = record.get("catalog_type") or ""
    owner = record.get("owner") or {}
    otype = owner.get("type") or ""
    software = ((record.get("software") or {}).get("id") or "").lower()
    name = record.get("name") or ""
    link = record.get("link") or ""
    blob = _text(record)

    if country in SPECIAL_ROOTS:
        return False, "supranational_root"
    if is_subnational_path(rel_path):
        return False, "subnational_path"
    if otype in NON_CENTRAL_OWNER_TYPES:
        return False, "non_central_owner"
    if otype == "International" and not _NSO.search(blob):
        return False, "international_owner"
    if _THEMATIC.search(blob):
        return False, "thematic_or_domain"
    if ctype in SCIENTIFIC_TYPES:
        return False, "scientific_repo"
    if software in SCIENTIFIC_SOFTWARE and ctype in SCIENTIFIC_TYPES:
        return False, "scientific_software"

    is_nso = bool(_NSO.search(blob))
    is_digital = bool(_DIGITAL_GOV.search(blob))
    is_mapping = bool(_MAPPING.search(blob))
    is_ministry = bool(_LINE_MINISTRY.search(blob)) and not (
        is_nso or is_digital or is_mapping
    )

    if is_ministry:
        return False, "agency_or_ministry"

    if ctype in {"Indicators catalog", "Microdata catalog"}:
        if is_nso or "sdg" in name.lower():
            return True, "national_statistics"
        return False, "indicators_not_nso"

    if ctype == "Open data portal":
        if is_national_open_data(record) and not is_ministry:
            return True, "national_open_data"
        if is_nso and re.search(r"open\s+data", name, re.I) and not is_ministry:
            return True, "nso_open_data"
        if is_digital and not is_ministry:
            if re.search(r"\bpilot\b", name, re.I):
                return False, "pilot_portal"
            if (
                is_national_open_data(record)
                or "national" in name.lower()
                or _DIGITAL_OD_SUCCESSOR.search(name + " " + link)
            ):
                return True, "digital_gov_national_portal"
        return False, "federal_opendata_not_national"

    if ctype == "Geoportal":
        link_l = link.lower()
        if "geoplatform.gov" in link_l:
            if re.search(
                r"geonetwork\.geoplatform|stac\.geoplatform",
                link_l,
            ) or re.search(
                r"\bfgdc\b|federal geographic data committee",
                name,
                re.I,
            ):
                return True, "national_geoportal_or_nsdi"
            if re.search(r"^us geoplatform$", name.strip(), re.I):
                return True, "national_geoportal_or_nsdi"
            return False, "geoplatform_thematic_node"
        if _NAT_GEO_NAME.search(name) or _NAT_GEO_NAME.search(
            str(record.get("description") or "")
        ) or is_mapping:
            return True, "national_geoportal_or_nsdi"
        return False, "federal_geoportal_not_nsdi"

    if ctype == "Metadata catalog":
        if is_nso or is_digital or "national" in name.lower() or "stelsel" in name.lower():
            return True, "national_metadata"
        return False, "metadata_other"

    return False, "not_national_type"


def should_flag_is_national_true(record: dict) -> bool:
    """True when properties.is_national is set and should not be."""
    props = record.get("properties") or {}
    if not isinstance(props, dict) or props.get("is_national") is not True:
        return False
    keep, _reason = classify_is_national(record, record.get("_file_path") or "")
    return not keep


def check_is_national_flag(record: dict) -> Optional[dict]:
    """Quality-check wrapper used by analyze-quality."""
    if not should_flag_is_national_true(record):
        return None
    _keep, reason = classify_is_national(record, record.get("_file_path") or "")
    name = record.get("name")
    return {
        "issue_type": "IS_NATIONAL_AGENCY_OR_TOPIC",
        "field": "properties.is_national",
        "current_value": {
            "is_national": True,
            "reason": reason,
            "name": name,
            "catalog_type": record.get("catalog_type"),
            "owner": (record.get("owner") or {}).get("name"),
        },
        "suggested_action": (
            "Set properties.is_national to false. This flag is only for the "
            "country's official catalog of that type (national open-data portal, "
            "NSDI/geoportal, or NSO statistical product), not for agency, "
            f"thematic, scientific, or subnational catalogs ({reason})."
        ),
    }


def is_legacy_open_data_name(name: str) -> bool:
    return bool(_LEGACY_OD.search(name or ""))
