"""One-off fix: fill rights.license_* for national open-data portals (LOW MISSING_RIGHTS).

Values were researched from official portal terms/license pages, CKAN license
facets, and government policy documents (see dataquality fix notes 2026-09-29).
"""

import pathlib

import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent / "data" / "entities"

# path suffix -> (license_id, license_name, license_url, rights_type)
FIXES = {
    "IN/Federal/opendata/datagovin.yaml": (
        "godl-india",
        "Government Open Data License - India (GODL)",
        "https://data.gov.in/government-open-data-license-india",
        "global",
    ),
    "KR/Federal/opendata/datagokr.yaml": (
        "korea-ogl",
        "Korea Open Government License (KOGL)",
        "https://www.kogl.or.kr/info/introduce.do",
        "global",
    ),
    "TW/Federal/opendata/datagovtw.yaml": (
        "ogdl-taiwan-1.0",
        "Open Government Data License v1.0 (Taiwan)",
        "https://data.gov.tw/license",
        "global",
    ),
    "MX/Federal/opendata/datosgobmx.yaml": (
        "libre-uso-mx",
        "Terminos de Libre Uso de los Datos Abiertos de Mexico",
        "https://datos.gob.mx/libreusomx",
        "global",
    ),
    "HR/Federal/opendata/datagovhr.yaml": (
        None,
        "Otvorena dozvola / Open Licence Republic of Croatia",
        "https://narodne-novine.nn.hr/clanci/sluzbeni/2017_07_67_1577.html",
        "global",
    ),
    "PL/Federal/opendata/danegovpl.yaml": (
        "cc0-1.0",
        "Creative Commons CC0 1.0 (predominant; per-dataset licenses vary)",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        "granular",
    ),
    "PE/Federal/opendata/catalogodatosabiertosgobpe.yaml": (
        "odc-by",
        "Open Data Commons Attribution License (predominant per CKAN license facet)",
        "https://opendatacommons.org/licenses/by/",
        "granular",
    ),
    "PE/Federal/opendata/datosabiertosgobpe.yaml": (
        "odc-by",
        "Open Data Commons Attribution License (predominant per CKAN license facet)",
        "https://opendatacommons.org/licenses/by/",
        "granular",
    ),
    "PY/Federal/opendata/datosgovpy.yaml": (
        None,
        "Licencia de Uso de la Informacion y los Datos Abiertos Publicos propiedad del Estado Paraguayo (Decreto 4064/2015, Anexo II)",
        "https://informacionpublica.paraguay.gov.py/#!/license",
        "global",
    ),
    "DO/Federal/opendata/datosgobdo.yaml": (
        "odc-odbl",
        "Open Data Commons Open Database License (predominant per CKAN license facet)",
        "https://opendatacommons.org/licenses/odbl/1-0/",
        "granular",
    ),
    "LV/Federal/opendata/datagovlv.yaml": (
        "cc0-1.0",
        "Creative Commons CC0 1.0 (predominant per CKAN license facet)",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        "granular",
    ),
    "AR/Federal/opendata/datosgobar.yaml": (
        "cc-by-4.0",
        "Creative Commons Attribution 4.0 (predominant per CKAN license facet)",
        "https://creativecommons.org/licenses/by/4.0/",
        "granular",
    ),
    "KG/Federal/opendata/datagovkg.yaml": (
        "cc-by",
        "Creative Commons Attribution (predominant per CKAN license facet)",
        "https://creativecommons.org/licenses/by/4.0/",
        "granular",
    ),
    "JE/Federal/opendata/opendatagovje.yaml": (
        "ogl-j-1.0",
        "Open Government Licence - Jersey v1.0",
        None,
        "granular",
    ),
    "BE/Federal/opendata/datagovbe.yaml": (
        "cc0-1.0",
        "Creative Commons CC0 1.0 (default per data.gov.be documentation)",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        "granular",
    ),
    "BH/Federal/opendata/datagovbh.yaml": (
        None,
        "Bahrain Open Government Data License v1.0",
        None,
        "global",
    ),
    "GT/Federal/opendata/catalogosenacytgobgt.yaml": (
        None,
        "ODC PDDL / ODC-By / ODbL / GFDL (per SENACYT open data manual)",
        None,
        "granular",
    ),
    "GR/Federal/opendata/datagovgr.yaml": (
        None,
        "CC0 / CC BY 4.0 (standardized reuse licenses per data.gov.gr FAQ)",
        "https://data.gov.gr/pages/terms-of-use",
        "granular",
    ),
    "IL/Federal/opendata/datagovil.yaml": (
        None,
        "Data.gov.il license for use of government databases (default; per-dataset overrides)",
        "https://data.gov.il/terms-of-use",
        "granular",
    ),
    "CL/Federal/opendata/datosgobcl.yaml": (
        None,
        "PDDL-1.0 / CC BY 4.0 / ODC-By-1.0 (per Chile Secretaria de Gobierno Digital standard)",
        "https://wikiguias.digital.gob.cl/Est%C3%A1ndares/Datos-Abiertos",
        "granular",
    ),
    "ES/Federal/opendata/datosgobes.yaml": (
        None,
        "Aviso legal tipo para la reutilizacion de la informacion del sector publico (RD 1495/2011, Ley 37/2007)",
        "https://datos.gob.es/es/aviso-legal",
        "granular",
    ),
    "PT/Federal/opendata/dadosgovpt.yaml": (
        None,
        "Per-dataset license (dados.gov.pt termos de utilizacao)",
        "https://dados.gov.pt/pt/termos-de-utilizacao",
        "granular",
    ),
    "NL/Federal/opendata/dataoverheidnl.yaml": (
        None,
        "Per-dataset license (CC0 recommended; Publiek Domein, CC-BY, CC-BY-SA, Geo Gedeeld)",
        "https://data.overheid.nl/ondersteuning/data-publiceren/licentie-keuze",
        "granular",
    ),
    "DK/Federal/opendata/datavejviserdk.yaml": (
        None,
        "Per-dataset license (DCAT-AP-DK license field; CC licenses per Digitaliseringsstyrelsen guidance)",
        "https://datavejviser.dk/om-datavejviser",
        "granular",
    ),
    "HK/Federal/opendata/datagovhk.yaml": (
        None,
        "DATA.GOV.HK Terms and Conditions of Use",
        "https://data.gov.hk/en/terms-and-conditions",
        "global",
    ),
    "MO/opendata/datagovmo.yaml": (
        None,
        "Terms of Use of the Macao SAR Government Data Open Platform",
        "https://data.gov.mo/Terms",
        "global",
    ),
    "SE/Federal/opendata/dataportalse.yaml": (
        None,
        "License set by each providing organization (CC0 1.0 recommended by DIGG/PRV)",
        "https://www.dataportal.se/sa-har-fungerar-sveriges-dataportal",
        "granular",
    ),
    "SK/Federal/opendata/dataslovenskosk.yaml": (
        None,
        "Per-dataset licenses (CC0 / CC BY recommended per MIRRI open data methodology)",
        None,
        "granular",
    ),
    "MY/Federal/opendata/datagovmy.yaml": (
        "cc-by-4.0",
        "Creative Commons Attribution 4.0 International (per data.gov.my FAQ)",
        "https://developer.data.gov.my/faq",
        "global",
    ),
    "TH/Federal/opendata/datagoth.yaml": (
        None,
        "DGA Open Government License (Thailand); per-dataset licenses vary",
        "https://data.go.th/en/pages/dga-open-government-license",
        "granular",
    ),
    "ID/Federal/opendata/katalogdatagoid.yaml": (
        "cc-by-4.0",
        "Creative Commons Attribution 4.0 (recommended under Satu Data Indonesia policy)",
        "https://creativecommons.org/licenses/by/4.0/",
        "granular",
    ),
    "JM/Federal/opendata/datagovjm.yaml": (
        None,
        "Open Government Licence - Jamaica (GOJ Open Data Policy, July 2021)",
        "https://www.mset.gov.jm/wp-content/uploads/2019/09/GOJ-Open-Data-Policy-July-2021.pdf",
        "global",
    ),
    "BN/Federal/opendata/datagovbn.yaml": (
        None,
        "Data Policy and Terms of Use (data.gov.bn)",
        "https://www.data.gov.bn/data-policy-terms-of-use/",
        "global",
    ),
    "CH/Federal/opendata/opendataswiss.yaml": (
        None,
        "opendata.swiss terms of use (per-dataset conditions: open use / source attribution / commercial use with permission)",
        "https://opendata.swiss/en/terms-of-use",
        "granular",
    ),
    "CH/Federal/opendata/databfsadminch.yaml": (
        None,
        "FSO Terms of Use (open government data: open use, source attribution required)",
        "https://www.bfs.admin.ch/bfs/en/home/fso/swiss-federal-statistical-office/terms-of-use.html",
        "global",
    ),
    "PH/Federal/opendata/datagovph.yaml": (
        None,
        "Open Data Philippines Data Policy Statement (free with attribution; per-dataset overrides)",
        None,
        "granular",
    ),
    "BR/Federal/opendata/dadosgovbr.yaml": (
        None,
        "Per-dataset open licenses (CC0 / PDDL / CC BY 4.0 / ODbL per INDA guidance)",
        "https://www.gov.br/governodigital/pt-br/dados-abertos",
        "granular",
    ),
}


def main() -> None:
    changed = 0
    for rel, (lid, lname, lurl, rtype) in FIXES.items():
        path = BASE / rel
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        rights = data.get("rights") or {}
        rights["license_id"] = rights.get("license_id") or lid
        rights["license_name"] = rights.get("license_name") or lname
        rights["license_url"] = rights.get("license_url") or lurl
        rights["rights_type"] = rights.get("rights_type") or rtype
        if rights.get("rights_type") in (None, "unknown"):
            rights["rights_type"] = rtype
        data["rights"] = rights
        path.write_text(
            yaml.dump(data, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        changed += 1
        print(f"updated {rel}")
    print(f"done: {changed} files")


if __name__ == "__main__":
    main()
