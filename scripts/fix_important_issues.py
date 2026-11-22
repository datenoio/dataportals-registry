#!/usr/bin/env python3
"""
Script to fix IMPORTANT priority issues:
- MISSING_OWNER_LOCATION
- MISSING_OWNER_NAME
- MISSING_OWNER_TYPE
- COVERAGE_NORMALIZATION (add macroregion)
- UNKNOWN_COUNTRY_OR_MACROREGION (replace Unknown with inferred or World)
- INCONSISTENT_LICENSE (add license_url)
- MISSING_API_STATUS (add api_status)
- SOFTWARE_ID_UNKNOWN (map to custom or verify)
- SOFTWARE_NAME_MISMATCH (fix name)
"""
import csv
import re
import yaml
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Optional, Tuple
from dpr.software import load_software_definitions
from dpr.geo import infer_country_from_link
from constants import COUNTRIES

# Base directories
BASE_DIR = Path(__file__).parent.parent
ENTITIES_DIR = BASE_DIR / "data" / "entities"
SOFTWARE_DIR = BASE_DIR / "data" / "software"
MACROREGION_FILE = BASE_DIR / "data" / "reference" / "macroregion_countries.tsv"

# License URL mappings
LICENSE_URL_MAP = {
    "Open Government Licence v3.0": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    "Open Government Licence": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    "OGL": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    "Creative Commons Atribuição-SemDerivações 3.0": "https://creativecommons.org/licenses/by-nd/3.0/",
    "CC BY-ND 3.0": "https://creativecommons.org/licenses/by-nd/3.0/",
    "Creative Commons Attribution-NoDerivatives 3.0": "https://creativecommons.org/licenses/by-nd/3.0/",
}

# Software ID mappings for unknown IDs (only for IDs with no software definition)
SOFTWARE_ID_MAPPING = {}

def load_macroregion_dict() -> Dict[str, Dict[str, str]]:
    """Load macroregion mapping from TSV file"""
    macroregion_dict = {}
    if MACROREGION_FILE.exists():
        with open(MACROREGION_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                alpha2 = row.get('alpha2', '').strip()
                if alpha2:
                    macroregion_dict[alpha2] = {
                        'macroregion_code': row.get('macroregion_code', '').strip(),
                        'macroregion_name': row.get('macroregion_name', '').strip(),
                    }
    return macroregion_dict


def infer_country_from_coverage(record):
    """Try to infer country from record's coverage"""
    coverage = record.get("coverage", [])
    if coverage and isinstance(coverage, list) and len(coverage) > 0:
        location = coverage[0].get("location", {})
        country = location.get("country", {})
        country_id = country.get("id")
        country_name = country.get("name")
        if country_id and country_id != "Unknown":
            return {
                "id": country_id,
                "name": country_name or country_id
            }
    return None


def infer_owner_name(record):
    """Try to infer owner name from record"""
    # Try from owner link domain
    owner_link = record.get("owner", {}).get("link", "")
    if owner_link:
        try:
            parsed = urlparse(owner_link)
            domain = parsed.netloc or owner_link
            # Remove www. prefix
            domain = re.sub(r'^www\.', '', domain.lower())
            # Remove common prefixes
            domain = re.sub(r'^(data|gis|geo|map|portal|opendata)\.', '', domain)
            # Take first part of domain
            parts = domain.split('.')
            if len(parts) > 0:
                name = parts[0].replace('-', ' ').title()
                if name and name != 'Unknown':
                    return name
        except Exception:
            pass
    
    # Try from portal name
    portal_name = record.get("name", "")
    if portal_name and portal_name != "Unknown":
        # Clean up the name
        name = portal_name.split('/')[0].split('.')[0].strip()
        if name and len(name) > 2:
            return name
    
    return None

def infer_owner_type(record, owner_link=None):
    """Try to infer owner type from context"""
    if not owner_link:
        owner_link = record.get("owner", {}).get("link", "")
    
    if owner_link:
        domain = urlparse(owner_link).netloc or owner_link
        domain = domain.lower()
        
        # Government domains (including .gov.net, .gov.com variations)
        if '.gov' in domain or '.gob' in domain or '.govt' in domain or domain.endswith('.gov.net') or domain.endswith('.gov.com'):
            # Check description for hints
            description = record.get("description", "").lower()
            if "county" in description or "municipal" in description or "local" in description:
                return "Local government"
            elif "state" in description or "province" in description or "regional" in description:
                return "Regional government"
            # Check for local/state indicators in domain
            elif any(x in domain for x in ['.city.', '.county.', '.local.', 'cityof', 'countyof', 'chippewa', 'municipal']):
                return "Local government"
            elif any(x in domain for x in ['.state.', '.province.', 'provincial', 'scgov']):
                return "Regional government"
            else:
                return "Central government"
        
        # Educational domains
        if '.edu' in domain or '.ac.' in domain or '.university' in domain or '.college' in domain:
            return "Academy"
        
        # International organizations
        if any(x in domain for x in ['.org', '.int', 'un.org', 'worldbank', 'iucn', 'iczn']):
            org_name = record.get("owner", {}).get("name", "").lower()
            if any(x in org_name for x in ['international', 'world', 'global', 'commission']):
                return "International organization"
            return "Civil society"
        
        # Business/Commercial
        if '.com' in domain or '.co.' in domain or '.biz' in domain:
            return "Business"
    
    # Check owner name for hints
    owner_name = record.get("owner", {}).get("name", "").lower()
    if any(x in owner_name for x in ['university', 'college', 'institute', 'academy']):
        return "Academy"
    if any(x in owner_name for x in ['government', 'ministry', 'department', 'agency']):
        return "Central government"
    if any(x in owner_name for x in ['city', 'municipal', 'county', 'local']):
        return "Local government"
    if any(x in owner_name for x in ['international', 'world', 'global']):
        return "International organization"
    
    # Default based on catalog type
    catalog_type = record.get("catalog_type", "").lower()
    if 'scientific' in catalog_type or 'research' in catalog_type:
        return "Academy"
    if 'government' in catalog_type or 'public' in catalog_type:
        return "Central government"
    
    return None

def fix_unknown_country_macroregion(record, macroregion_dict: Dict[str, Dict], file_path: str = "") -> Tuple[bool, str]:
    """Fix UNKNOWN_COUNTRY_OR_MACROREGION by replacing Unknown with inferred or World."""
    UNKNOWN = "Unknown"
    fixed = False
    messages = []

    # Infer country from owner or file path
    owner_country = (record.get("owner", {}) or {}).get("location", {}) or {}
    owner_country = owner_country.get("country", {}) or {}
    owner_id = (owner_country.get("id") or "").strip()
    owner_name = (owner_country.get("name") or "").strip()

    # Country from file path (e.g. US/Other/scientific/x.yaml -> US)
    path_country = ""
    if file_path and "/" in file_path:
        path_country = file_path.split("/")[0].strip()

    def _valid_country(cid):
        return cid and str(cid).strip() != UNKNOWN

    def _valid_macroregion(mid):
        return mid and str(mid).strip() != UNKNOWN

    # Macroregion paths (not ISO countries) - use World
    MACROREGION_PATHS = {"Africa", "World", "EU", "Oceania", "Americas", "Asia", "Europe"}
    if path_country in MACROREGION_PATHS:
        path_country = ""

    # Resolve replacement country: owner > path > World
    if _valid_country(owner_id):
        replacement_country = {"id": owner_id, "name": owner_name or owner_id}
    elif path_country and path_country in macroregion_dict:
        # Get country name from reference
        country_name = path_country
        countries_file = BASE_DIR / "data" / "reference" / "countries.csv"
        if countries_file.exists():
            with open(countries_file, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row.get("alpha2") == path_country:
                        country_name = row.get("name", path_country)
                        break
        replacement_country = {"id": path_country, "name": country_name}
    else:
        replacement_country = {"id": "World", "name": "World"}

    # Fix coverage entries
    coverage = record.get("coverage", [])
    for idx, cov_entry in enumerate(coverage or []):
        location = cov_entry.get("location", {}) or {}
        country = location.get("country", {}) or {}
        macroregion = location.get("macroregion", {}) or {}

        # Fix country.id or country.name = Unknown
        cid = (country.get("id") or "").strip()
        cname = (country.get("name") or "").strip()
        if cid == UNKNOWN or cname == UNKNOWN:
            location["country"] = replacement_country.copy()
            cov_entry["location"] = location
            coverage[idx] = cov_entry
            fixed = True
            messages.append(f"Set coverage[{idx}].country to {replacement_country['id']}")

        # Fix macroregion.id or macroregion.name = Unknown
        mid = (macroregion.get("id") or "").strip()
        mname = (macroregion.get("name") or "").strip()
        if mid == UNKNOWN or mname == UNKNOWN:
            # Infer from country
            loc_country = location.get("country", {}) or {}
            loc_cid = (loc_country.get("id") or "").strip()
            if loc_cid and loc_cid != UNKNOWN:
                mr_info = macroregion_dict.get(loc_cid)
                if mr_info:
                    location["macroregion"] = {
                        "id": mr_info["macroregion_code"],
                        "name": mr_info["macroregion_name"],
                    }
                else:
                    location["macroregion"] = {"id": "001", "name": "World"}
            else:
                location["macroregion"] = {"id": "001", "name": "World"}
            cov_entry["location"] = location
            coverage[idx] = cov_entry
            fixed = True
            messages.append(f"Set coverage[{idx}].macroregion")

    # Fix owner.location.country if Unknown
    owner = record.get("owner", {}) or {}
    owner_loc = owner.get("location", {}) or {}
    owner_country = owner_loc.get("country", {}) or {}
    if (owner_country.get("id") or "").strip() == UNKNOWN or (owner_country.get("name") or "").strip() == UNKNOWN:
        owner_loc["country"] = replacement_country.copy()
        owner["location"] = owner_loc
        record["owner"] = owner
        fixed = True
        messages.append("Set owner.location.country")

    if fixed:
        record["coverage"] = coverage
        return True, "; ".join(messages)
    return False, None


def fix_coverage_normalization(record, macroregion_dict: Dict[str, Dict]) -> Tuple[bool, str]:
    """Fix COVERAGE_NORMALIZATION by adding macroregion"""
    coverage = record.get("coverage", [])
    if not coverage:
        return False, None
    
    fixed = False
    messages = []
    
    for idx, cov_entry in enumerate(coverage):
        location = cov_entry.get("location", {})
        country = location.get("country", {})
        country_id = country.get("id")
        
        if country_id and ("macroregion" not in location or not location.get("macroregion")):
            if country_id == "Unknown":
                continue

            # Special macroregions for EU and World (not in UN M49 country list)
            special_macroregions = {
                "EU": {"macroregion_code": "EU", "macroregion_name": "European Union"},
                "World": {"macroregion_code": "001", "macroregion_name": "World"},
            }
            macroregion_info = special_macroregions.get(country_id) or macroregion_dict.get(country_id)
            if macroregion_info:
                location["macroregion"] = {
                    "id": macroregion_info["macroregion_code"],
                    "name": macroregion_info["macroregion_name"],
                }
                coverage[idx]["location"] = location
                fixed = True
                messages.append(f"Added macroregion {macroregion_info['macroregion_name']} for {country_id}")
    
    if fixed:
        record["coverage"] = coverage
        return True, "; ".join(messages)
    
    return False, None

def fix_inconsistent_license(record) -> Tuple[bool, str]:
    """Fix INCONSISTENT_LICENSE by adding license_url"""
    rights = record.get("rights", {})
    license_name = rights.get("license_name")
    license_url = rights.get("license_url")
    
    if license_name and not license_url:
        # Try to find URL in mapping
        for key, url in LICENSE_URL_MAP.items():
            if key.lower() in license_name.lower():
                rights["license_url"] = url
                record["rights"] = rights
                return True, f"Added license_url: {url}"
    
    return False, None

def fix_missing_api_status(record) -> Tuple[bool, str]:
    """Fix MISSING_API_STATUS by setting api_status based on api and endpoints"""
    api_status = record.get("api_status")
    
    if api_status is None or api_status == "":
        api = record.get("api", False)
        endpoints = record.get("endpoints", [])
        
        # If api=True or endpoints exist, set to active
        if api is True or len(endpoints) > 0:
            record["api_status"] = "active"
            return True, "Set api_status to 'active' (api=True or endpoints present)"
        else:
            # Otherwise set to uncertain
            record["api_status"] = "uncertain"
            return True, "Set api_status to 'uncertain' (no api or endpoints)"
    
    return False, None

def fix_owner_location(record, file_path):
    """Fix MISSING_OWNER_LOCATION"""
    owner = record.get("owner", {})
    location = owner.get("location", {})
    country = location.get("country", {})
    
    if country.get("id") == "Unknown":
        # Try to infer from coverage
        inferred_country = infer_country_from_coverage(record)
        if not inferred_country:
            # Try from owner link
            owner_link = owner.get("link", "")
            code = infer_country_from_link(owner_link) if owner_link else None
            inferred_country = {"id": code, "name": COUNTRIES.get(code, code)} if code else None
        
        if inferred_country:
            location["country"] = inferred_country
            # Preserve level if reasonable, otherwise set to 20 (country level)
            if location.get("level", 0) == 0:
                location["level"] = 20
            owner["location"] = location
            return True, f"Set owner location to {inferred_country['name']}"
        else:
            # For truly unknown, set to World
            location["country"] = {"id": "World", "name": "World"}
            location["level"] = 0
            owner["location"] = location
            return True, "Set owner location to World (truly international)"
    
    return False, None

def fix_owner_name(record, file_path):
    """Fix MISSING_OWNER_NAME"""
    owner = record.get("owner", {})
    owner_name = owner.get("name", "")
    
    if not owner_name or owner_name == "Unknown":
        inferred_name = infer_owner_name(record)
        if inferred_name:
            owner["name"] = inferred_name
            return True, f"Set owner name to '{inferred_name}'"
        else:
            # Use portal name as fallback
            portal_name = record.get("name", "")
            if portal_name and portal_name != "Unknown":
                owner["name"] = portal_name
                return True, f"Set owner name to portal name '{portal_name}'"
    
    return False, None

def fix_owner_type(record, file_path):
    """Fix MISSING_OWNER_TYPE"""
    owner = record.get("owner", {})
    owner_type = owner.get("type", "")
    
    if not owner_type or owner_type == "Unknown":
        inferred_type = infer_owner_type(record, owner.get("link"))
        if inferred_type:
            owner["type"] = inferred_type
            return True, f"Set owner type to '{inferred_type}'"
        else:
            # Default fallback
            owner["type"] = "Business"
            return True, "Set owner type to 'Business' (default)"
    
    return False, None

def fix_software_id_unknown(record, software_defs: Dict[str, Dict]) -> Tuple[bool, str]:
    """Fix SOFTWARE_ID_UNKNOWN by mapping to custom or verifying"""
    software = record.get("software", {})
    software_id = software.get("id")
    
    if not software_id:
        return False, None
    
    # Check if ID is in mapping
    if software_id in SOFTWARE_ID_MAPPING:
        new_id = SOFTWARE_ID_MAPPING[software_id]
        software["id"] = new_id
        if new_id == "custom":
            software["name"] = "Custom software"
        record["software"] = software
        return True, f"Mapped software.id from '{software_id}' to '{new_id}'"
    
    # Check if ID exists in software definitions
    if software_id not in software_defs:
        # Map to custom
        software["id"] = "custom"
        software["name"] = "Custom software"
        record["software"] = software
        return True, f"Mapped unknown software.id '{software_id}' to 'custom'"
    
    return False, None

def fix_software_name_mismatch(record, software_defs: Dict[str, Dict]) -> Tuple[bool, str]:
    """Fix SOFTWARE_NAME_MISMATCH by updating name to match ID"""
    software = record.get("software", {})
    software_id = software.get("id")
    software_name = software.get("name", "")
    
    if software_id and software_id in software_defs:
        expected_name = software_defs[software_id].get("name", "")
        if expected_name and software_name != expected_name:
            software["name"] = expected_name
            record["software"] = software
            return True, f"Updated software.name from '{software_name}' to '{expected_name}'"
    
    return False, None

def parse_important_file(important_file_path):
    """Parse IMPORTANT.txt and extract file paths and issues"""
    issues = []
    with open(important_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match file entries
    pattern = r'File: ([^\n]+)\nRecord ID: [^\n]+\nCountry: [^\n]+\nIssue: ([^\n]+)\nField: ([^\n]+)'
    
    matches = re.finditer(pattern, content)
    for match in matches:
        file_path = match.group(1)
        issue_type = match.group(2)
        field = match.group(3)
        issues.append((file_path, issue_type, field))
    
    return issues

def fix_yaml_file(file_path, issue_type, macroregion_dict: Dict[str, Dict], software_defs: Dict[str, Dict]):
    """Fix issues in a YAML file"""
    full_path = ENTITIES_DIR / file_path
    
    if not full_path.exists():
        # Try scheduled directory
        scheduled_path = BASE_DIR / "data" / "scheduled" / file_path
        if scheduled_path.exists():
            full_path = scheduled_path
        else:
            print(f"Warning: File not found: {full_path}")
            return False
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data:
            print(f"Warning: Empty file: {file_path}")
            return False
        
        fixed = False
        message = None
        
        if issue_type == "MISSING_OWNER_LOCATION":
            fixed, message = fix_owner_location(data, file_path)
        elif issue_type == "MISSING_OWNER_NAME":
            fixed, message = fix_owner_name(data, file_path)
        elif issue_type == "MISSING_OWNER_TYPE":
            fixed, message = fix_owner_type(data, file_path)
        elif issue_type == "COVERAGE_NORMALIZATION":
            fixed, message = fix_coverage_normalization(data, macroregion_dict)
        elif issue_type == "INCONSISTENT_LICENSE":
            fixed, message = fix_inconsistent_license(data)
        elif issue_type == "MISSING_API_STATUS":
            fixed, message = fix_missing_api_status(data)
        elif issue_type == "SOFTWARE_ID_UNKNOWN":
            fixed, message = fix_software_id_unknown(data, software_defs)
        elif issue_type == "SOFTWARE_NAME_MISMATCH":
            fixed, message = fix_software_name_mismatch(data, software_defs)
        elif issue_type == "UNKNOWN_COUNTRY_OR_MACROREGION":
            fixed, message = fix_unknown_country_macroregion(data, macroregion_dict, file_path)
        
        if fixed and message:
            print(f"{issue_type} in {file_path}: {message}")
            # Write back
            with open(full_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    important_file = BASE_DIR / "dataquality" / "priorities" / "IMPORTANT.txt"
    
    if not important_file.exists():
        print(f"Error: {important_file} not found")
        return
    
    print("Loading macroregion dictionary...")
    macroregion_dict = load_macroregion_dict()
    print(f"Loaded {len(macroregion_dict)} macroregion mappings")
    
    print("Loading software definitions...")
    software_defs = load_software_definitions()
    print(f"Loaded {len(software_defs)} software definitions")
    
    print("\nParsing IMPORTANT.txt...")
    issues = parse_important_file(important_file)
    print(f"Found {len(issues)} issues to fix")
    
    fixed_count = 0
    skipped_count = 0
    for file_path, issue_type, field in issues:
        result = fix_yaml_file(file_path, issue_type, macroregion_dict, software_defs)
        if result:
            fixed_count += 1
        else:
            skipped_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(issues)} files")
    if skipped_count > 0:
        print(f"Skipped {skipped_count} files (may have been already fixed or couldn't be inferred)")

if __name__ == "__main__":
    main()
