"""Check which UN system agencies have data catalogs in the registry."""
import duckdb

con = duckdb.connect("data/datasets/datasets.duckdb", read_only=True)

# agency -> distinctive domain/name patterns
agencies = {
    "UN Secretariat (data.un.org / UNSD)": ["data.un.org", "unstats.un.org", "onemap.un.org", "geoservices.un.org", "publicadministration.un.org", "comtrade.un.org", "comtradeplus.un.org", "population.un.org"],
    "UNDP": ["undp.org"],
    "UNEP": ["unep.org", "unepgrid.ch", "unep-wcmc.org", "info-rac.org", "uneplive.org"],
    "UNICEF": ["unicef.org", "washdata.org"],
    "UNFPA": ["unfpa.org"],
    "UNHCR": ["unhcr.org"],
    "WFP": ["wfp.org"],
    "UN-Habitat": ["unhabitat.org"],
    "UNODC": ["unodc.org"],
    "UN Women": ["unwomen.org", "un-women.org"],
    "UNAIDS": ["unaids.org"],
    "UNCTAD": ["unctad.org"],
    "UNIDO": ["unido.org"],
    "UNOPS": ["unops.org"],
    "UNESCO (incl. UIS, IOC/IODE)": ["unesco.org", "iode.org", "obis.org"],
    "WHO (incl. regional offices, PAHO, IARC)": ["who.int", "paho.org", "iarc.fr"],
    "FAO": ["fao.org", "faoswalim.org", "d4science.org"],
    "ILO": ["ilo.org"],
    "IAEA": ["iaea.org"],
    "ICAO": ["icao.int"],
    "IMO": ["imo.org"],
    "ITU": ["itu.int"],
    "UPU": ["upu.int"],
    "WIPO": ["wipo.int"],
    "WMO": ["wmo.int"],
    "UNWTO": ["unwto.org", "unwto.int", "e-unwto.org"],
    "IFAD": ["ifad.org"],
    "World Bank Group": ["worldbank.org", "energydata.info", "enterprisesurveys.org", "wbwaterdata.org", "ifc.org", "miga.org"],
    "IMF": ["imf.org"],
    "ITC (International Trade Centre)": ["intracen.org"],
    "UNU (UN University)": ["unu.edu"],
    "UNITAR / UNOSAT": ["unitar.org", "unosat.org"],
    "UNRISD": ["unrisd.org"],
    "UNSSC": ["unssc.org"],
    "UNICRI": ["unicri.org"],
    "UNIDIR": ["unidir.org"],
    "UNV": ["unv.org"],
    "UNCDF": ["uncdf.org"],
    "UN Global Compact": ["unglobalcompact.org"],
    "UNOOSA": ["unoosa.org"],
    "UN-OCHA (HDX, FTS, ReliefWeb)": ["unocha.org", "humdata.org", "reliefweb.int"],
    "UNDRR (incl. PreventionWeb)": ["undrr.org", "preventionweb.net"],
    "OHCHR": ["ohchr.org"],
    "UNFCCC": ["unfccc.int"],
    "UNCCD": ["unccd.int"],
    "CBD Secretariat": ["cbd.int"],
    "UN regional commissions (UNECE/ECA/ESCAP/ESCWA/ECLAC)": ["unece.org", "uneca.org", "unescap.org", "unescwa.org", "escwa.un.org", "cepal.org", "eclac.org"],
    "IOM (related org)": ["iom.int", "migrationdataportal.org"],
    "WTO (related org)": ["wto.org"],
    "CTBTO": ["ctbto.org"],
    "OPCW": ["opcw.org"],
    "IOM GMDAC": ["gmdac.iom.int"],
    "UNCCD (dup guard)": [],
}

for agency, pats in agencies.items():
    if not pats:
        continue
    clauses = " OR ".join(f"lower(link) LIKE '%{p.lower()}%'" for p in pats)
    rows = con.execute(
        f"SELECT name, link, catalog_type, status FROM catalogs WHERE {clauses} ORDER BY link"
    ).fetchall()
    if rows:
        print(f"FOUND  {agency}: {len(rows)}")
        for r in rows:
            print(f"       - {r[0]} | {r[1]} | {r[2]} | {r[3]}")
    else:
        print(f"MISSING {agency}")
    print()
