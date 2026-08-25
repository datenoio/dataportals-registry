# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.17.0] - 2026-08-25

**GitHub Release**: [v1.17.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.17.0) - Published August 25, 2026

### Added
- **2,608 net new catalog entries**; registry source now **22,750** entities (**0** scheduled) across **219** country/territory folders, including first entity roots for **Jersey (JE)** and **Saint Helena (SH)**.
- **15 software definitions**; software catalog now **262** platforms: IMF National Summary Data Page (`imfnsdp`), ODWeb (`odweb`), LabKey Server (`labkey`), Synapse (`synapse`), XNAT (`xnat`), OMERO (`omero`), Kadi4Mat (`kadi4mat`), e!DAL (`edal`), NOMAD (`nomad`), InterMine (`intermine`), GRIN-Global (`gringlobal`), PlutoF (`plutof`), JGI Genome Portal (`jgi`), cBioPortal (`cbioportal`), and ESA Science Archive (`esasciencearchive`).
- Five South Korean catalogs promoted from scheduled review: KOSIS North Korea Statistics, the Ministry of Unification North Korea Information Portal, NGII National Land Information Platform, KINU DSpace, and NKHR Larchiveum.
- CRITICAL quality rule `INVALID_NESTED_TYPE` for mixed nested leaf types that break DuckDB/Parquet STRUCT and LIST inference (country/macroregion ids, tags, `dataset_count_reported`).
- Eswatini NDMA Digital Risk Database GeoNode (`geonodendmaorgsz`), the national disaster-risk SDI also served at `geonode.ndrma.org.sz`.
- SISALRIL Portal Estadístico (`redatamsisalrilgobdo`), the REDATAM-backed health-insurance catalog of the Dominican Republic Superintendency of Health and Occupational Risks listed on CELADE's online-process index.
- OpenAIRE Graph data-source harvest (`scripts/extract_openaire_portals.py`): list dataset-publishing portals from the Graph v3 API, dedup on host against DuckDB, and add misses under `data/scheduled/` ([docs/openaire-sync.md](docs/openaire-sync.md)).
- **2,409** scientific repositories promoted from the OpenAIRE Graph harvest after live URL review (data repositories and dataset-publishing IRs, each with an `identifiers[]` row `id: openaire`).
- **9** UK local-government Cadcorp SIS WebMap geoportals (Barnet, Charnwood, Derby, Medway, North Norfolk, Sefton, Stoke-on-Trent, West Northamptonshire, West Lothian).
- **105** IMF National Summary Data Page catalogs from the DSBB directory (**118** `imfnsdp` records in total).
- First entity roots for **Jersey (JE)** (Open Data Jersey) and **Saint Helena (SH)** (St Helena Data Portal, inactive).
- Domain scientific catalogs on the new software IDs: **25** InterMine, **13** GRIN-Global, **10** ESA Science Archive, **10** Synapse, **6** each LabKey / XNAT / OMERO, plus cBioPortal, Kadi4Mat, and JGI.

### Changed
- Remapped leftover `software.id: custom` catalogs onto existing products: IPT (`wwwgbifes`), OntoPortal (SIFR BioPortal, MedPortal), DSpace (RIULL, RIUBU, Cambridge), dLibra (UJK, KPBC), DataLad (registry and hubs), Oracle APEX (IPK Gatersleben), ArcGIS Server (Geology Cloud), Open SDG (Serbia), plus 13 IMF NSDP pages onto `imfnsdp` and 3 Chinese `/odweb/` portals onto `odweb`.
- Serbia catalogs reviewed: quoted UN M49 `039`; marked dead hosts inactive (Zastrugis OpenDataSoft/Huwise, srsrb ArcGIS Hub, OpenShift IPT, MRE ArcGIS REST, SEPA CKAN); moved faculty/city catalogs into ISO subregions (RS-00, RS-07, RS-10, RS-12, RS-20); corrected DSpace names/owners from OAI Identify; documented live harvest endpoints.
- Sierra Leone IGIS ArcGIS Hub (`igisdatahubdstihubarcgiscom`) and DSTI Education Data Hub (`educationdatahubdstigovsl`) marked inactive; Open Data Sierra Leone (`opendataslgovsl`) notes DNS/TLS timeouts. NaSIS retagged as WordPress with `wp-json`/`feed`; Njala DSpace gained OAI-PMH and sitemap; SSL NADA gained catalog/CSV export endpoints (13 studies); EPA GRS portal title and DHIS2 login-wall notes updated.
- South Sudan WIS 2.0 in a box (`wis2meteosouthsudancomss`) now uses HTTPS for the node and pygeoapi endpoints, with harvest tags and SYNOP holdings noted.
- South Sudan CLiMIS (`climissouthsudanorg`) description now covers the public dashboard domains (markets, CPI, rainfall, IPC); the NBS NADA (`ssnbsmicrodatahubcom`) is documented as a HugeDomains park with no replacement archive on nbs.gov.ss.
- Eswatini Drought Monitor (`cdiendmaorgsz`) now records its public OpenAPI and monthly CDI maps API; the Meteorological Service WIS2 node is marked national with harvest tags.
- Chile INE REDATAM (`redataminegobcl`) now records the related `redatam-ine.ine.cl` Webserver host; Ecuador INEC REDATAM (`redataminecgobec`) records the CELADE-listed `/redecu/` portal path.
- Scheduled queue cleared (**0** remaining). Source YAML is **22,750** entities across **219** country/territory folders. Working-tree JSONL, Parquet, and DuckDB exports rebuilt to match (**22,750** catalogs, **0** scheduled, **262** software).
- National catalogs moved under `{CC}/Federal/`, with type and subregion path corrections. Jersey open data moved out of GB into `JE/`; the St Helena CKAN moved into `SH/` and marked inactive.
- Discovery and harvest hub pages, agent checklists, identifiers, incremental recipes, and search-tool starters now surface the v1.16.0 software IDs (G3W-SUITE, Trimble Locus / Louhi / Landfolio, Spatial Suite, GEUSMAP, GISApp, iObčina, Cadcorp, iShare, M.App Enterprise, CubeWerx, Sentinel Hub, PxStat, TabNet, FENIX, SparkMap, Goal Tracker, DataWarehousePro, Beyond 20/20, StatPlanet, RDF Online Repository, ResourceContracts, Guangxi) plus Converis, OpenAIRE, IMF NSDP, ODWeb, LabKey, Synapse, XNAT, OMERO, Kadi4Mat, e!DAL, NOMAD, InterMine, GRIN-Global, PlutoF, JGI, cBioPortal, and ESA Science Archive. Harvest docs state **262** software definitions.
- Quality analysis reports **0** issues across **22,750** records. Harvest endpoints written onto IMF NSDP, InterMine, ESA Science Archive, GRIN-Global, Synapse, LabKey, and other API-capable software.
- Catalog schema now requires string country/macroregion ids, string tags, and integer `dataset_count_reported` (no mixed scalar types).
- Singapore catalogs moved under `SG/Federal/`; data.gov.sg harvest APIs and GovTech ownership recorded; LTA DataMall and SingStat Table Builder APIs documented; SG-MDH API fields aligned with deprecated status. OpenAIRE scientific records cleaned (AlloMAPS, Interfil, WOVOdat, 2DMatPedia); TTD moved to China (`dbidrblabnet`); Model Zoo retagged as an ML catalog and Nexdata as a marketplace. NUS SHGIS ArcGIS REST and Yale-NUS Dataverse marked inactive; NParks TRSGIS described as a UAT host.

### Fixed
- IMPORTANT quality issues: set `api: true` / `api_status: active` on **120** catalogs that already had harvest endpoints (plus **3** Kadi4Mat REST catalogs); moved **14** files into `scientific/` or `opendata/` to match `catalog_type`; merged duplicate University of Granada and ERMIS-F geoportal records; set Integrity GIS owner subregion to Missouri; retagged the IPC Administración Local ArcGIS Hub template as Community.
- Mixed nested YAML types that collapsed DuckDB/Parquet nested columns to `JSON`: Norway `country.id` parsed as boolean `false` (unquoted `NO`), integer tag `911`, `{tag: ...}` tag mappings, string `dataset_count_reported`, and unquoted M49 macroregion id `155`.
- MEDIUM quality sweep: inactive catalogs aligned to `api: false` / `api_status: inactive`; placeholder titles replaced; software-expected harvest endpoints filled; short tags and a Wales subregion name corrected.

### Removed
- Duplicate catalog records merged into keepers: Cyprus ERMIS-F geoportal (`ermisgeoportalcyiaccy`, same URL as `geoportalermisfeu`) and University of Granada Open Data (`opendataugresdataset`, same URL as `opendataugres`).
- Cocos (Keeling) Islands (`CC`) and `Unknown` country folders (records recategorized or dropped).
- **3** Cadcorp scheduled viewers that did not respond (Wirral WebMap9, Bury ExternalWebMap, Inverclyde Maps).
- **664** OpenAIRE scheduled sources that were dead, duplicate of an existing entity, a staging host, a hijacked/parked domain, or not a catalog (software forges, journal pages, single publications).

## [1.16.0] - 2026-08-24

**GitHub Release**: [v1.16.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.16.0) - Published August 24, 2026

### Added
- **1,002 net new catalog entries** (1,010 new IDs; 8 removed after v1.15.0); registry source now **20,142** entities (**12** scheduled) across **218** country/territory folders, including a first entity root for **Isle of Man (IM)**.
- **24 software definitions**; software catalog now **247** platforms: Trimble Locus IMS (`trimblelocus`), Sitowise Louhi (`louhi`), Trimble Landfolio (`landfolio`), Spatial Suite (`spatialsuite`), GEUSMAP (`geusmap`), GISApp (`gisapp`), iObčina (`iobcina`), G3W-SUITE (`g3wsuite`), Cadcorp SIS WebMap (`cadcorp`), Astun iShare (`ishare`), Hexagon M.App Enterprise (`mappenterprise`), CubeWerx CubeSERV (`cubewerx`), Sentinel Hub (`sentinelhub`), DataWarehousePro (`datawarehousepro`), Goal Tracker (`goaltracker`), RDF Online Repository (`rdfrepository`), ResourceContracts (`resourcecontracts`), the Guangxi Public Data Open Platform (`gxopendata`), PxStat (`pxstat`), TabNet (`tabnet`), FENIX (`fenix`), Beyond 20/20 Web Data Server (`beyond2020`), SparkMap (`sparkmap`), and StatPlanet (`statplanet`).
- **376 scientific repositories**, including **135 DSpace** (Spain, Finland, Zambia, Argentina, Colombia, Germany, Uganda, Malawi, Botswana, Mongolia, and others), **118 Figshare** (US, UK, World event/org tenants, New Zealand, Australia, Germany, Singapore), **23 Hyrax** (British Library Independent Research Organisation repositories and US campuses), **13 Elsevier Pure** (Israel and Hong Kong), **7 DSpace-CRIS**, **5 Atlas of Living Australia** collection portals, **4 Converis**, **4 Elsevier Digital Commons**, **4 WEKO3**, and **3 Omega-PSIR**.
- Geoportal products: **22 Spatial Suite** webkort sites (Denmark, plus two in Sweden), **19 Sitowise Louhi** Finnish municipal and regional viewers, **18 Trimble Landfolio** mining cadastre map portals, **15 GEUSMAP** geology viewers (Denmark and Greenland), **12 Trimble Locus IMS** Finnish city map services, **12 G3W-SUITE** Italian WebGIS (Trento, Roma Capitale, Palermo, Gran Paradiso, ARPA Lombardia, and others), **22 GeoNetwork**, **27 ArcGIS Server**, **17 ArcGIS Hub**, **11 GeoServer**, **8 GeoNode**, **8 Open Data Cube** OGC Web Services (Digital Earth Australia/Africa/Pacific/Sweden, CSIRO EASI, Swiss Data Cube, WFP), and **5 DMI pygeoapi** Open Data APIs.
- Open data and contracts: **24 CKAN** portals, **18 RDF Online Repository** mineral and petroleum transparency sites, **5 ResourceContracts** / OpenLandContracts portals, **29 Indonesian** Satu Data and ministry portals, plus national and local portals in Mexico, Paraguay, Argentina, Taiwan, and **12 Mongolian** catalogs (Glass Account, EITI, procurement, SDG dashboard, iMORI/UFE DSpace).
- Indicators: **15 Open SDG** country and city sites, **11 SparkMap** US community and health data hubs, **9 DHIS2** HMIS sites, **9 DATASUS TabNet** (`tabnet`) installations (national hub plus ANS, six state, and two municipal), **8 Goal Tracker** SDG platforms, **8 PxWeb** statistical databases (mostly Sweden), **7 SuperSTAR / SuperWEB2** table builders (ABS TableBuilder, AIHW Data Explorer, VOCSTATS, TRA Online, Health Workforce Data, Stat-Xplore, Scotland’s Census), **7 SDMX-RI** APIs, **6 DataWarehousePro** central-bank warehouses, **6 Open Data for Africa / Knoema** NSDP hubs, **5 FENIX** FAO indicator catalogs (AMIS, AIDmonitor, DAD-IS, WIEWS, FAO/WHO GIFT), **7 ASEAN** regional dashboards, Beyond 20/20 (Castilla-La Mancha IES and JODI), and EC-OECD STIP Compass (StatPlanet).
- **76 US catalogs**, including **59** scientific repositories (Figshare, Hyrax, Digital Commons) and **10** SparkMap indicator hubs; **50 Finnish** catalogs (31 geoportals and 18 scientific repositories); **48 Danish** catalogs (Spatial Suite, GEUSMAP, DMI pygeoapi); **43 UK** catalogs (**41** scientific: Figshare and British Library IRO Hyrax).
- **33 Brazilian** catalogs (16 geoportals including GeoSampa, IDE-Sisema, IEDE/RS, PRODEMGE, ANEEL SIGEL, Army BDGEx, INEA, and TCE-RO, plus TabNet); **28 Spanish** (**21 DSpace**, Open SDG, Beyond 20/20); **23 Italian** (12 G3W-SUITE plus Lombardia, Veneto, Sicilia, Emilia-Romagna, Torino, Lecce CKAN, DASSI, Earth-prints, ISPRA, MiC, data.CNR.it); **23 Mexican**, **21 Peruvian**, **20 Argentine**, **20 Swedish**, **18 German**, and **15 Australian** catalogs (SuperSTAR, ALA, Digital Earth / EASI OWS).
- **16 polar / Arctic / Greenland catalogs** promoted from scheduled (SIOS, NunaGIS, Asiaq, PGC FRIDGE, GTN-G, WGMS, BarentsWatch, INTERACT GIS, and related hosts).
- **6 Mauritius catalogs**: MOI Ocean Database (GeoNetwork), Mauritius Ocean Observatory E-Platform (GeoNode), Mauritius Research Repository, National OER Repository of Mauritius (DSpace), Observatoire de l'Environnement Data ODE portal, and the Mauritius ICT Indicators Portal.
- **2 Eswatini catalogs**: the NDMA Eswatini Drought Monitor and the Ministry of Finance Open Data for Africa hub (distinct from the CSO country portal).
- **14 catalogs promoted** from the remaining Africa/Asia/Latin America scheduled queue: Mali SICAM mining cadastre; Senegal petroleum cadastre, PGIIS flood geoportal, and Géorépertoire; Tunisia national public-data register; Burkina Faso NENDO school map; Botswana DSpace IRs at BUAN, BIUST, and Botho University; Myanmar MERAL (WEKO3) and marine MSP geoportal; Kuala Lumpur DBKL City Planning System; Surat Municipal GIS; and Lima SIM.
- **12 scheduled** Cadcorp SIS WebMap viewers pending live confirmation (UK councils: Barnet, Bury, Charnwood, Derby, Inverclyde, Medway, North Norfolk, Sefton, Stoke-on-Trent, West Lothian, West Northamptonshire, Wirral).
- Discovery fingerprints and harvest recipes for the 24 new software IDs (`docs/discovery-geoportals.md`, `docs/discovery-geoportals-viewers.md`, `docs/discovery-geoportals-sdi.md`, `docs/discovery-opendata.md`, `docs/discovery-indicators.md`, `docs/harvest-viewers.md`, `docs/harvest-geoportals.md`, `docs/harvest-earthdata.md`, `docs/harvest-indicators.md`).

### Changed
- Drop Python 3.9; supported and CI-tested versions are **3.10–3.12**. Remove the `pyorc<0.11` pin that existed only for 3.9 wheels.
- SuperSTAR (`superstar`) software definition rewritten: WingArc Australia SuperWEB2 statistical table builder (not the STR hotel-benchmarking product). Website, owner, country, SDMX support, and capabilities updated.
- Mauritius OpenData portal (`datagovmuorg`) migrated from DKAN to CKAN 2.11; catalog URL is now `https://data.govmu.org`. Statistics Mauritius NSDP description updated from e-GDDS to SDDS Plus.
- Recategorized **46** catalogs into the correct country, Federal/subregion, or type folder (including Buenos Aires city open data → AR-C, MinCyT datasets → AR Federal, Edo State open data → NG-ED, and US Other ArcGIS Hubs into Qatar, Sudan, and Uganda).
- Retagged existing catalogs onto the new software IDs: **15** Guangxi public-data tenants (`gxopendata`), **5** Romanian GISApp viewers, **3** iObčina/iOpćina viewers, **5** CKAN (including 4 OpenEI repositories), **2** PxStat (CSO Ireland, NISRA), national DATASUS TabNet, FAOSTAT onto FENIX, All Things Missouri onto SparkMap, Almada GeoPortal onto M.App Enterprise, JODI World Database onto Beyond 20/20, and Sentinel Hub Catalog from `stacserver`. Replaced FAOSTAT’s generic fao.org sitemaps with the FENIX `/faostat/api/v1/` groups-and-domains endpoint.
- Moved Eswatini national catalogs under `SZ/Federal/`; pointed the WIS2 owner to the Meteorological Service site and the CSO Open Data for Africa owner to the Central Statistical Office page.
- Clarified names, coverage, and owners on existing GeoSampa, IEDE/RS, and IDE-Sisema Brazil geoportal records, and corrected Italy coverage, owner, and names on Umbria open data (IT-55), Lombardia ArcGIS REST, ACS Beni Culturali CKAN, Emilia-Romagna GeoNetwork, Veneto IDT GeoServer, Sicilia SITR ArcGIS REST, Comune di Udine, MUR USTAT HTTPS, and UniData Bicocca.
- Refreshed metadata on **992** existing catalogs. HTTP-verified endpoints written onto **209** records and `api: true` onto **61**. Marked **35** catalogs inactive and **21** deprecated.
- Cleared the polar/Arctic scheduled queue (**16** promoted, **1** removed), then the remaining Africa/Asia/Latin America queue (**14** promoted, **1** removed). New scheduled queue is **12** Cadcorp UK viewers.
- Regenerated dataset exports: **20,142** catalog records (entities); **247** software definitions; **12** scheduled (**20,154** in `full.jsonl`). Quality regression baseline refreshed after the catalog additions.

### Removed
- **8 catalog entries** removed as superseded or duplicate: Cameroon SDG Hub, Finland Paikkatietohakemisto, Guinea-Bissau Open Data for Africa at the old hostname, Vytautas Magnus University CRIS at the old host, the Nigeria NBS NADA catalog, the NZ Open Data Network GeoServer copy at the Federal geo path, Togo `sigm.tg` ArcGIS REST, and the World-folder Côte d'Ivoire mining-cadastre ArcGIS copy.
- Greenland Mineral Resources geoportal dropped from scheduled without promotion.
- WASCAL Hydromet Network (`wascal-hydromet-net.org`) dropped from scheduled without promotion: the hostname now redirects to an empty WordPress site, and station data remains on the existing WASCAL Data Discovery Portal.

## [1.15.0] - 2026-08-22

**GitHub Release**: [v1.15.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.15.0) - Published August 22, 2026

### Added
- **720 net new catalog entries** (809 new IDs; 89 removed after v1.14.0); registry source now **19,140** entities (**17** scheduled) across **217** country/territory folders.
- **12 software definitions**; software catalog now **223** platforms: mviewer (`mviewer`), Geocortex Essentials (`geocortex`), Isogeo (`isogeo`), QGIS Server (`qgisserver`), openEO (`openeo`), MapGIS IGServer (`mapgisigserver`), Breedbase (`breedbase`), Tripal (`tripal`), VEuPathDB (`veupathdb`), MassBank (`massbank`), ioChem-BD (`iochembd`), and ESGF (`esgf`).
- **471 scientific repositories**, including domain coverage for bioinformatics and genomics, chemistry, materials and engineering, astronomy, linguistics, agriculture, and biodiversity (NCBI/EMBL-EBI, NASA/ESA, CLARIN, USDA, NIST, and related hosts).
- Crop, pathogen, chemistry, and climate databases on new shared-product IDs: **19 Tripal** (CottonGen, SoyBase, GDR, TreeGenes, PeanutBase, Citrus, CarrotOmics, PulseDB, Vaccinium, SpinachBase, i5k Workspace, CorkOakDB, Kiwifruit, LiceBase, and others), **15 VEuPathDB** organism and project sites (PlasmoDB, FungiDB, VectorBase, AmoebaDB, CryptoDB, ToxoDB, ClinEpiDB, MicrobiomeDB, OrthoMCL, and others; TriTrypDB retagged from `custom`), **8 ESGF** Metagrid/CoG portals (LLNL, ORNL, NERSC, DKRZ, CEDA, NCI, IPSL, LIU; Earth System Grid Federation retagged from `custom`), **6 Breedbase** (CassavaBase, MusaBase, YamBase, SweetPotatoBase, Triticeae Toolbox, Sol Genomics Network), **5 ioChem-BD** Browse nodes (ICIQ hub, Girona, Toronto Matter Lab, Jagiellonian; BSC node retagged from `custom`), and **4 MassBank** instances (Europe, IPB Halle, Japan, MoNA).
- **220 US catalogs**, including **190** scientific repositories, **12** geoportals, and **11** machine-learning catalogs (TCIA, Civitai, UCI KDD, MLCommons, DrivenData, Open Graph Benchmark, EvalAI, Foundry, TDC, PMLB, Wolfram Neural Net Repository).
- **90 World catalogs**, including **33** UN / IGO indicators portals (WHO, FAO AQUASTAT/FRA/EMPRES-i, UNAIDS, UNDP HDR, UN-Water SDG 6, WTO, ITC Trade Map/MacMap, WITS, UIS, UN Tourism, WFP HungerMap, and others).
- **80 German catalogs**, including **62** scientific repositories, plus IOER Monitor, SMARD, SurvStat@RKI, Thru.de, IPB MassBank, and the FAIRagro Search Hub.
- **66 French catalogs**, including **42** geoportals (**31 mviewer**, **9 Isogeo** OpenCatalogs) and the ESGF IPSL CoG node.
- **74 UK catalogs**, including **55** scientific repositories, **8 MetadataWorks Metadata Browser** (`mwmb`) catalogues (SDR UK, Genomics England, HASP, Research Data Scotland, Nottingham City Data Connector, and NHS SDE catalogues for London, East Midlands, and Kent/Medway/Sussex), plus Cefas, UK EPB, National Library of Scotland Data Foundry, Scottish Parliament open data, and the ESGF CEDA Metagrid.
- **36 Canadian catalogs**, including **24** geoportals (**14 ArcGIS Hub**, **6 Geocortex** provincial and municipal viewers, plus Manitoba Land Initiative, PEI GIS, and a Shawinigan Isogeo OpenCatalog) and the Toronto Matter Lab ioChem-BD node.
- **27 machine-learning catalogs**, including Zindi, AIcrowd, SIGNATE, Grand Challenge, CodaLab/Codabench, and **7 Chinese** platforms (Baidu AI Studio, BAAI, OpenXLab, DataFountain, HeyWhale, OpenI, WiseModel).
- **59 indicators catalogs**, including African regional systems (ECOWAS, SADC, AfCFTA, BCEAO, BEAC, African Trade Observatory), Latin American trade observatories (ALADI, MERCOSUR, SIECA, Pacific Alliance), ASEAN Energy Database System, and EU Access2Markets / TARIC / Easy Comext.
- Geoportal products: **34 mviewer** (Brittany, Rennes Métropole, Géo2France, Santégraphie, GeoRhena, and Slovak regions), **15 Geocortex** (Canada, Australia, US), **10 Isogeo** OpenCatalogs (French départements plus Shawinigan), **3 openEO** backends, **2 QGIS Server** catalogs, plus **17 Romanian** municipal GIS viewers and **7 Saudi** municipal/regional geoportals.
- **17 Irish catalogs** (CKAN open data, ArcGIS Hub county geoportals, Oireachtas and EPA APIs) and **13 Portuguese** municipal geoportals and CKAN sites.
- **17 scheduled** polar / Arctic / Greenland catalogs pending live promotion (SIOS, NunaGIS, Asiaq, PGC FRIDGE, GTN-G, WGMS, and related hosts).
- Discovery fingerprints and harvest recipes for mviewer, Isogeo, Geocortex, QGIS Server, openEO, and MapGIS IGServer (`docs/discovery-geoportals.md`, `docs/harvest-geoportals.md`, `docs/harvest-earthdata.md`, `docs/agents/discover.md`).

### Changed
- Recategorized Embrapa GeoInfo (`geoinfodadosembrapabr`) from open data to geoportal.
- Discovery and harvest guides treat `radar`, `yoda`, `dhis2`, `ipums`, `openaire`, and `symbiota` as published `software.id` values (no longer `custom` placeholders), and index mviewer, Isogeo, Geocortex, QGIS Server, openEO, MapGIS IGServer, Breedbase, Tripal, VEuPathDB, MassBank, ioChem-BD, and ESGF in the same recipes.
- Documentation navigability and harvest depth: generated [software-index.md](docs/software-index.md) (including an `apidetect` column); split geoportal and scientific discovery mega-pages; split scientific harvest into IRs ([harvest-scientific.md](docs/harvest-scientific.md)) vs domain stacks ([harvest-scientific-domain.md](docs/harvest-scientific-domain.md)); unique `{#id}` headings (CI fails on combined software H2s, stale auto-slug links, and a stale index file); custom/host-collision/STAC/DSpace/Drupal playbooks; agent indexes link the software index instead of pasting every probe; harvest-output recipe schema (not a reaper contract); CI test `tests/test_docs_software_coverage.py`. Record-count contract: [exports.md](docs/exports.md#record-counts).
- Retagged **25** existing catalogs onto new or corrected software IDs, including **7** openEO backends from `stacserver`, **4** Isogeo OpenCatalogs from IsiGéo (`isigeo`), **3** QGIS Server sites from MapServer, plus ESGF, ioChem-BD, and VEuPathDB retags from `custom`.
- IsiGéo (`isigeo`) software description now distinguishes it from Isogeo (`isogeo`), the French GIS metadata SaaS.
- Refreshed metadata on **871** existing catalogs; HTTP-verified endpoints and `api: true` written onto **716** records. Marked **10** catalogs inactive and **1** deprecated.
- Regenerated dataset exports: **19,140** catalog records (entities); **223** software definitions; **17** scheduled (**19,157** in `full.jsonl`). Quality regression baseline refreshed after the catalog additions.

### Fixed
- Quality regression after the v1.14.0 catalog imports: completed owner, coverage, and API metadata so integrity CRITICAL/IMPORTANT counts are back to zero, and refreshed `dataquality/baseline_counts.json`.

### Removed
- **89 catalog entries** removed after v1.14.0 as duplicate recategorized records (mostly US Federal/Other geoportals and ArcGIS Hub copies, plus Ukraine, Iceland, Syria, Brazil IPT, and World placeholders).

## [1.14.0] - 2026-08-21

**GitHub Release**: [v1.14.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.14.0) - Published August 21, 2026

### Added
- **702 net new catalog entries**; registry source now **18,420** entities (0 scheduled) across **217** country/territory folders, including a first entity root for **Grenada (GD)**.
- **19 software definitions**; software catalog now **211** platforms: MapServer, MapTiler Server, gvSIG Online, deegree, VertiGIS WebOffice, GeoMedia WebMap, disy Cadenza, FAIR Data Point, Idra, CONTENTdm, Omeka S, Fedora, OPUS, RADAR (`radar`), Symbiota (`symbiota`), DHIS2 (`dhis2`), Yoda (`yoda`), OpenAIRE (`openaire`), and IPUMS (`ipums`).
- **20 DHIS2** national HMIS/indicator portals (Bangladesh, Benin, CAR, Djibouti, Ethiopia, Ghana, Kenya, Malawi, Nigeria, Palestine, Rwanda, Sierra Leone, Somalia, South Sudan, Chad, Tanzania, Uganda, Zambia). Retagged Nepal HMIS from `custom`.
- **33 OpenAIRE** Explore gateways (EU university alliances and thematic hubs). Retagged 2 existing OpenAIRE gateways from `custom`.
- **58 Symbiota** biodiversity collection portals from the [official Symbiota directory](https://symbiota.org/symbiota-portals/). Retagged Ecuador BNDB and Illinois Natural History Survey from `custom`.
- **6 RADAR** research-data repositories (ÖAW Datathek, RADAR-BB, KonDATA, WueData, OstData, FoDaSi) and **4 Dutch Yoda** data-publication platforms (Tilburg, Leiden, VU, WUR), plus Utrecht Yoda retagged from `custom`.
- **9 DSpace 7** institutional / research-data repositories (Kyoto KURENAI, Alicante RUA, THM data.THM, JLU Giessen JLUpub, Imperial Spiral, Toronto TSpace, University of Aruba, UMass Amherst ScholarWorks, University of Rzeszów RDB).
- **2 IPUMS** collections (CDOH, MEPS). Retagged **12** existing IPUMS collections from `custom`; remapped **6** Albanian U-CRIS portals to `dspacecris`.
- **205 US catalogs** in the first wave, including **143** geoportals (**90 ArcGIS Hub**, **26 ArcGIS Server**, **12 MapServer**), plus later Symbiota and IPUMS scientific/microdata additions.
- **81 German catalogs**, including **16 QWC2** viewers, **12 Mapbender** geoportals, **10 OPUS** publication servers, **10 disy Cadenza** environmental geoportals, **7 VertiGIS WebOffice** city plans, **7 MapServer**, **6 deegree** xPlanBox/ISK services, **5 RADAR**, and **4 Fedora** CLARIN language-resource repositories.
- **52 QWC2** geoportals (Germany, Switzerland, France, Latvia, Austria, Czechia, and others).
- **45 MapServer** geoportals (USGS MRDATA, MSC GeoMet, Buenos Aires city map, Québec flood zones, INGV Vesuvius, CIMEC, and others).
- **34 Ukrainian catalogs**, including **12 municipal CKAN** open data portals (Kyiv, Kharkiv, Odesa, Vinnytsia, Kryvyi Rih, Mariupol, and others).
- **33 FAIR Data Point** metadata catalogs (Health-RI and Dutch university medical centers, Spanish research FDPs, EJP-RD / EGA / EATRIS / INFRAFRONTIER, SPHN, FAIRVASC, and the EJP-RD Virtual Platform index).
- **25 Chinese catalogs**, including **24** municipal and provincial public-data open platforms.
- **21 Esploro** research repositories and **18 InvenioRDM** repositories (CERN, IAEA NDS, CaltechAUTHORS, BAOBAB, Imperial Helix, and others).
- Scientific coverage: **21 DSpace**, **14 Elsevier Digital Commons**, **10 Fedora**, **10 OPUS**, **6 PHAIDRA**, plus UAE, Albania U-CRIS, and Georgian repositories.
- Geoportal products: **13 Mapbender**, **11 VertiGIS WebOffice**, **10 Cadenza**, **9 deegree**, **8 NextGIS Web**, **7 gvSIG Online**, **5 MapTiler Server**, **2 GeoMedia WebMap**.
- Open data and indicators for Albania, Georgia, the UAE, Iceland, Maldives, Bahamas, Barbados, Syria, Tajikistan, and Caribbean OECS/ECCB.
- CONTENTdm software definition and two dataset catalogs (Stats NZ Digital Library, IU Climate Data Indianapolis). Omeka S (`gisiuedu` retag, Gouda Tijdmachine). Idra federation platform and **4 inactive** Idra catalogs.
- MapTiler Server geoportals: San Francisco, Martínez de la Torre, EMERCOM Atlas tiles, Zurich Airport DDS, and CGC Slovakia.
- HTTP-verified default API probes for GeoMapFish, GET SDI Portal, REDATAM, SciCat, MapStore, Open SDG, SuperMap iServer, gvSIG Online, InGrid, ERDAS APOLLO, Drupal JSON:API, ICAT OAI-PMH, CoGIS/eLiteGIS REST, GIN/Gogs, OSF JSON:API, Samvera/Hyrax, Semantic MediaWiki, Ensembl, PHAIDRA, MapTiler Server, MyTardis, and NYU Data Catalog, written onto `endpoints[]` only when a GET succeeds.
- Catalog discovery guides (Google / Censys / Shodan / FOFA), per-platform queries, agent/LLM client setup, fingerprints for remaining `software.id` values, [docs/enrichment.md](docs/enrichment.md), [docs/apidetect.md](docs/apidetect.md), [docs/liveness.md](docs/liveness.md).
- Harvest guides for crawling **datasets** from catalog APIs (`docs/harvest.md` and related pages). Agent checklist: `docs/agents/harvest.md`.
- Published docs for quality issue codes, vocabularies, scheduled promotion, releases, Re3Data enrichment, CKAN sync, CLI, software taxonomy, and JSON-LD/DCAT export mapping.

### Changed
- Harvest/discovery docs treat `radar`, `yoda`, `dhis2`, `ipums`, `openaire`, and `symbiota` as published `software.id` values. Corrected the scheduled-queue count in `ai-consumers.md`. Filled harvest indexes in `llms.txt` and `when-to-use.md`.
- Cleared the scheduled queue (**80** promoted, **8** removed in the first wave; later **67** Symbiota/DSpace promotions). `data/scheduled/` is empty.
- Recategorized **199** misplaced catalogs (**140** from `Unknown/`, **40** from `World/`) into country folders (largest batches: United States, United Kingdom, Japan, Canada, Germany).
- Refreshed metadata on **270** existing catalogs (179, then 91 more for IPUMS/OpenAIRE/Yoda/DHIS2 retags and the Symbiota / RADAR / DSpace wave).
- Drupal software definition now matches WordPress: `has_api: Yes` and `custom_api: Yes`. Quality-fixer `infer_endpoints` helpers probe `apidetect` URL maps over HTTP and write only endpoints that respond.
- Documented platforms that must not get guessed API paths (`NO_STANDARD_PROBE`).
- Regenerated dataset exports: **18,420** catalog records (entities); 211 software definitions; 0 scheduled.
- Quality regression baseline refreshed after the catalog additions (`dataquality/baseline_counts.json`).

### Removed
- **7 catalog entries** removed (placeholder or private Unknown/World geoportals: numeric hosts, `geomapmaker.online`, `geonode.hydrotechsolutions.biz`, `kmkgis.com`, `maps.dsm.city`, and `qwc2.thelabsv.org`).

## [1.13.0] - 2026-08-20

**GitHub Release**: [v1.13.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.13.0) - Published August 20, 2026

### Added
- **1,442 net new catalog entries**; registry source now **17,718** entities (0 scheduled).
- **44 software definitions**; software catalog now **192** platforms.
- Docusaurus documentation site (`website/`) publishing `docs/` to GitHub Pages at `https://datenoio.github.io/dataportals-registry/`, with internals docs for humans and agents (query, contribute, OpenSpec).
- Catalog discovery instructions for humans (`docs/discovery.md`) and coding agents (`docs/agents/discover.md`).
- Relocated working notes `geoseer-analysis.md`, `metadata-quality.md`, and `trust_score_methodology.md` from `docs/` to `devdocs/`.
- **546 US catalogs**, including **213** geoportals (ArcGIS Hub/Server, MangoMap), **129** scientific repositories (**57 Elsevier Digital Commons**, **27 DSpace**), **121** state and local indicators catalogs (including **6 IBIS-PH**), and **79** open data portals (including Socrata).
- **197 Japanese catalogs**, including **166 わが街ガイド (`wagmap`)** municipal and prefectural geoportals, **15 GC Navi** viewers, national GSI/MLIT/JAXA geoportals, and PLATEAU VIEW on Re:Earth (Saitama City and Osaka City).
- **178 Chinese catalogs**, including **109** municipal and provincial open data portals, **48 Tianditu** geoportals (national, provincial, and municipal, including 8 Guangdong and 8 Henan city viewers plus Chengdu), **9** Inspur oPortal sites, national indicators (Customs, PBOC, SAFE, ChinaBond, exchanges), and microdata (CFPS, CHARLS, NBS, CNSDA).
- **98 German catalogs**, including **34 Masterportal** community-gallery geoportals, **17 cardo** viewers, **13 NOL-IS** municipal portals, **6 map.apps**, and **5 GENESIS-Online** statistical databases.
- **76 GeoMapFish geoportals**, mostly Swiss cantonal and Vaud geocommunes viewers, plus Liechtenstein, Saint-Pierre (Réunion), Grand Châtellerault, and Pro Natura.
- **56 Turkish municipal geoportals**: **20** NetGIS Server / KEOS city guides, **12 GiSoftGis**, **7 Sampaş WebGIS**, and **3 BelsisIMS**, after live checks against vendor reference lists.
- **32 NADA microdata catalogs** (national statistical archives in Africa, Latin America, and Asia, including AFRISTAT, LSB Lao, Lesotho BOS, ENADA, LISGIS, and INE Honduras).
- **30 Greek geoportals**: **25 GET SDI Portal** municipal and regional viewers (Crete, Heraklion, Chania, Corfu, Piraeus, DAFNI island SDI, Central Macedonia, HNMS Climatic Atlas, and others) and **4 GIS4Smart** Epirus municipal viewers.
- **26 Brazil geoportals** from INDE geoservices and related SDI lists (ANATEL, SGB/CPRM, IPHAN, IBGE Censo 2022, FUNAI, IDE-MS, IDEA-SP, Minas Gerais, Fortaleza, IDE Bahia, Projeto Brumadinho, IDE-DF) plus **22 MapBiomas** land-cover platforms across Brazil, Latin America, and Antarctica.
- **24 Italian catalogs**, including Regione Marche and Calabria CKAN, Napoli and Modena open data, Liguria/Calabria/Basilicata RSDI, AGEA, and **6 MapStore** geoportals (Bolzano, Genova, Arno basin, Toscana).
- **18 ERDAS Apollo** image-catalog geoportals (Madrid, Aragón, BRIN SpaceMap, Sachsenforst, CONABIO, and others).
- **16 MapStore** geoportals (Italy, Portugal Azores municipalities, CRAIG, Moldova GEODATA, Austro Control, Regionalverband Ruhr).
- **16 Seoul Open Data Plaza** district catalogs (Jongno-gu through Seocho-gu).
- **5 Czech LKOD** open data catalogs (ČHMÚ, Liberec, Zlín, Ústecký kraj, and Orlová).
- **12 SciCat** scientific catalogs (ESS, MAX IV, ALS, DESY, RFI, HZDR, ILL) and **7 FAIRDOM-SEEK** instances (FAIRDOMHub, ELIXIR Belgium, IBISBA, LiSyM, Leipzig Health Atlas, MeDIZ.Rostock, ArmLifeBank).
- **10 Omega-PSIR** Polish scientific catalogs that publish research datasets, **10 Axiom Data Science Portal** catalogs (IOOS, MBON, CeNCOOS, SCCOOS, CalOOS-related, AOOS, SoundCoop, ADAC), and **7 InvenioRDM** repositories (Münster, Tübingen, Freiburg, Bamberg, KTH, plus existing CU Anschutz retag).
- **9 ActiveMap GIS** geoportals in Russia and Kirov Oblast GP Atlas; **3 Geometa** GIS OGD portals (Omsk, Murmansk, Tyumen); EverGIS Online.
- **3 SuperMap iPortal** geoportals: SuperMap Online, the official iPortal demo, and the Heilongjiang Tianditu iPortal resource catalog.
- **3 Copernicus DHuS** national Sentinel catalogs: Finland FINHub, Greece Hellenic National Sentinel Data Hub, and Poland IMGW Copernicus hub.
- Additional catalogs for **Canada** (British Columbia, Ontario, Nunavut geoportals; CMHC housing-market indicators), **Nicaragua**, **Venezuela**, **Mongolia**, **Azerbaijan**, **United Kingdom** (verified geoportals promoted from scheduled), and Moscow city GIS, open data, and budget sites.
- Promoted **22 verified catalogs** from scheduled to entities after live checks, including UK geoportals, DataLad catalogs and hubs, GIS OGD portals for Omsk, Murmansk, and Tyumen, UFMG Projeto Brumadinho GeoNode, IDE-DF ArcGIS Server, and the Slovak GeoMINV geoportal.
- Software definitions for shared geoportal products: わが街ガイド (`wagmap`), GC Navi (`gcnavi`), Re:Earth (`reearth`), GET SDI Portal (`getsdiportal`), GIS4Smart (`gis4smart`), GeoMapFish (`geomapfish`), MapBiomas (`mapbiomas`), NOL-IS (`nolis`), mf-geoadmin3 (`mfgeoadmin3`), cardo (`cardo`), map.apps (`mapapps`), InGrid (`ingrid`), MangoMap (`mangomap`), Copernicus DHuS (`copernicusdhus`), MapStore (`mapstore`), Masterportal (`masterportal`), SuperMap iPortal (`supermapiportal`), Tianditu (`tianditu`), NetGIS Server (`netgisserver`), Sampaş WebGIS (`sampaswebgis`), GiSoftGis (`gisoftgis`), BelsisIMS (`belsisims`), CoGIS (`cogis`), GP Atlas (`gpatlas`), Geonomics (`geonomics`), DATUM GIS (`datumgis`), InGeo (`ingeo`), Farvater GIS OGD (`farvatergisogd`), EverGIS (`evergis`), Geometa (`geometa`).
- Software definitions for shared scientific, open data, and indicators products: NYU Data Catalog (`nyudatacatalog`), Axiom Data Science Portal (`axiomportal`), SciCat (`scicat`), FAIRDOM-SEEK (`seek`), Open Science Framework (`osf`), GIN (`gin`), PHAIDRA (`phaidra`), Seoul Open Data Plaza (`seoulopendataplaza`), Our Open Data (`ouropendata`), MODA Open Data Platform (`modaopendata`), LKOD (`lkod`), JDOP (`jdop`), GENESIS-Online (`genesisonline`), IBIS-PH (`ibisph`).

### Changed
- Moved the GitHub repository from `commondataio/dataportals-registry` to `datenoio/dataportals-registry`. Old GitHub URLs redirect.
- Cleared the scheduled queue (22 promoted, 31 removed). `data/scheduled/` is now empty.
- Recategorized **252** misplaced catalogs, mostly US state, Federal, Other, Unknown, and World path corrections (including a large Oregon `.org` geoportal batch that belonged in other states; NPGeo Corona → Germany; MLIT data hub → Japan; IGG-CIGEO Hub → Nicaragua; GRID Nigeria GeoNetwork → Nigeria).
- Recategorized catalog types where needed (THREDDS/OPeNDAP and academic repositories → scientific; Lexington/Louisville → open data; Maine public health → indicators).
- Refreshed metadata on **485** existing catalogs.
- Retagged 15 Japan geoportals from custom to わが街ガイド (`wagmap`), Shizuoka Prefecture GIS to GC Navi, and PLATEAU VIEW to Re:Earth.
- Retagged seven CoGIS Portal catalogs from eLiteGIS to CoGIS and pointed `link` at the portal catalog. eLiteGIS REST endpoints are kept.
- Retagged RAE GeoPortal and Thessaloniki SDI to GET SDI Portal; Arkhangelsk forest dispatcher, Komi geoportal, and GIS OGD sites onto GP Atlas / Geometa; RGIS Novosibirsk region and Yamal ЕКС to CoGIS.
- Reclassified nine Kazakhstan regional geoportals from custom to Geonomics, and four Russia geoportals previously tagged custom to NextGIS Web, ORBISMap, and DATUM GIS.
- Reclassified custom catalogs onto existing and new shared-product IDs across geoportals (GeoMapFish, MapBiomas, NOL-IS, mf-geoadmin3, cardo, map.apps, InGrid, MangoMap, Copernicus DHuS, MapStore, Masterportal), scientific repositories (NYU Data Catalog, Axiom, SciCat, FAIRDOM-SEEK, OSF, GIN, PHAIDRA, DSpace, Dataverse, Hyrax, InvenioRDM, DataONE), and open data portals (Seoul Open Data Plaza, Our Open Data, MODA, LKOD, JDOP, CKAN, OpenDataSoft).
- Retagged three Taiwan MODA catalogs (Taoyuan URL updated from dead `data.tycg.gov.tw`), Prague open data from CKAN to LKOD, and Shizuoka/Ehime/Kakegawa from CKAN to Our Open Data.
- Merged the duplicate Zhejiang provincial JDOP catalog `datazjgovcn` (`data.zj.gov.cn`, which redirects to `data.zjzwfw.gov.cn`) into `datazjzwfwgovcn`.
- Regenerated dataset exports: **17,718** catalog records (entities); 192 software definitions; 0 scheduled.

### Fixed
- Rehomed four Ohio geoportals that were filed under the wrong place: CAGIS Open Data Hub (`data-cagisportal.opendata.arcgis.com`) from Unknown/California, Lorain County GIS Open Data from California, Butler County Auditor GIS REST from Oregon, and NEORSD GIS REST from South Dakota.

### Removed
- **16 catalog entries** removed (ArcGIS Hub templates and copies, Socrata demo sites, duplicate or inactive Hawaii GIS endpoints, and the duplicate Zhejiang JDOP catalog `datazjgovcn`).
- Dropped **31 scheduled catalogs** that timed out, returned 403, required login for listing, or could not be verified as a public catalog: Turkish municipal Sampaş WebGIS and GiSoftGis city guides, remaining Brazilian INDE candidates, several Russian GIS OGD/InGeo/CoGIS sites (including Terrascop, Yakutsk, and Bashkortostan), ATRIS, DataLad Edu Hub, and the Sainsbury Wellcome Centre GIN instance.

## [1.12.0] - 2026-08-18

**GitHub Release**: [v1.12.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.12.0) - Published August 18, 2026

### Added
- **1,304 net new catalog entries** (1,318 YAML files added; 14 removed); registry source now **16,276** entities (1 scheduled).
- **166 Polish eWMAPA** county and city geoportals, plus **91 Swedish EntryScape** open data catalogs and **62 Lizmap** geoportals (mostly French).
- **151 CKAN** open data portals, including **80 Thai** government catalogs and **34 Indonesian** Satu Data sites.
- **73 GBIF IPT** scientific catalogs, **59 Chinese InstDB** research-data repositories, **32 Japanese data eye** municipal portals, and **25 Chinese Inspur oPortal** sites.
- **101 indicators catalogs**, including **29 Open Data for Africa / Knoema** portals, **18 Datawheel** observatories, and additional national statistical systems.
- **26 microdata catalogs**, including **19 REDATAM** census/survey sites, with first entity roots for **Aruba (AW), Cayman Islands (KY), and Montserrat (MS)**; Kosovo (**XK**) ASKdata recategorized from Serbia.
- Scientific and geospatial coverage: **25 WMO WIS 2.0 in a box** nodes, **21 DataONE** repositories, **20 NASA GES DISC OPeNDAP/Hyrax** endpoints, **22 NextGIS Web** geoportals, **17 Japanese WEKO3** repositories, and **12 rasdaman** datacube services.
- **6 API catalogs** (Tallinn, Estonia RIHA and X-tee, Latvia VISS, Malaysia Kijang, Taiwan TDX) plus additional ArcGIS Hub/Server (50), OpenDataSoft (22), JKAN (14), and Piveau (8) sites.
- **12 software definitions**: Micka, Knoema, REDATAM, Copernicus Data Stores, data eye, Gipuzkoa Irekia, Liferay, OGD Platform India, Inspur oPortal, Piveau, SEU-e, and Ensembl.

### Changed
- Recategorized misplaced catalogs: Lithuania SDG ArcGIS hubs (`Unknown` → `LT/Federal`), American Samoa GIS (`US-AR` → `US-AS`), Bakersfield GIS (`US-DC` → `US-CA`), St. Petersburg stats (`US-TN` → `US-FL`), Guam geoportals (`US/Federal` → `US-GU`), Northern Mariana BECQ (`US-CA` → `US-MP`), Dazhou open data (`CN-NX` → `CN-SC`), and Kosovo ASKdata (`RS` → `XK`).
- Reassigned software IDs on existing records after new platform definitions: Liferay (104), Knoema (41), OGD Platform India (37), SEU-e (18), REDATAM (16), Data Fair (12), Gipuzkoa Irekia (7), oPortal (6), Micka (5), Piveau (4), and others.
- Refreshed metadata (names, links, endpoints, API status) across **327** existing catalogs, including large Spanish and Indian batches.
- Regenerated dataset exports: **16,276** catalog records (entities); 148 software definitions; 1 scheduled.

### Removed
- **14 catalog entries** removed (inactive, duplicate, or replaced), including misplaced WIS 2.0 nodes, US ArcGIS Hub copies, and retired Chinese open-data URLs.

### Fixed
- Quality regression baseline now matches current `analyze-quality` output after the v1.11.0 catalog additions.
- Pin `pyorc<0.11` on Python 3.9 so CI can install `iterabledata` without building dropped 3.9 wheels.
- Make `tests/test_schema_parity.py` collect on Python 3.9 (`from __future__ import annotations`).
- Allow CKAN, WordPress, OpenDataSoft, and Drupal to use additional catalog types they actually host (geoportals, scientific, indicators).

## [1.11.0] - 2026-08-17

**GitHub Release**: [v1.11.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.11.0) - Published August 17, 2026

### Added
- **444 net new catalog entries** (450 YAML files added; 5 existing records recategorized or replaced); registry source now **14,972** entities (1 scheduled).
- **64 THREDDS** scientific catalogs, including **48 ESGF** climate-data nodes (DKRZ, NASA NCCS, LLNL, CMCC, DIAS Japan, CEDA, and others).
- **49 indicators catalogs**, including national SDG portals, statistical databases, and central-bank, health, and finance indicator systems.
- New catalogs across 64 countries, including **CKAN** (28), **ArcGIS Hub/Server** (39), **Dataverse** (11), **GeoNetwork** (10), **OpenDataSoft** (10), and additional DKAN, Figshare, Pure, and ERDDAP sites.
- **6 metadata catalogs** (including HDA Belgium, I14Y Switzerland, LETZDATA Luxembourg) and **8 API catalogs** (including Datafordeler, Digitraffic, GUS API, Brønnøysund).
- **Apache Superset** software definition (`data/software/indicators/superset.yaml`) with catalog-type mapping in `scripts/constants.py`.

### Changed
- Recategorized or replaced five existing catalogs: Flanders VMM portal (`opendatawsevlaanderenbe` → `opendatawewisvlaanderenbe`), Olomouc geoportal (`EU/CZ-71` → `CZ/CZ-71`), Bordeaux Métropole (`opendatabordeauxmetropolefr` → `datahubbordeauxmetropolefr`), Incheon iMap (`KR-11` → `KR-28`), and Muntinlupa GIS (`muntinlupacitywebgis1com` → `cgismuntinlupacitygovph`).
- Refreshed metadata for selected Brazilian, Estonian, Italian, Korean, Liechtenstein, Maltese, Montenegrin, and Portuguese catalogs (URL/name updates; some status and software corrections).
- Regenerated dataset exports: **14,972** catalog records (entities); 136 software definitions; 1 scheduled.

## [1.10.0] - 2026-08-16

**GitHub Release**: [v1.10.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.10.0) - Published August 16, 2026

### Added
- **92 net new catalog entries** (95 YAML files added, 3 recategorized); registry source now **14,528** entities (0 scheduled).
- **39 Open Data for Africa** indicators catalogs (country portals plus the continental `dataportal.opendataforafrica.org`), covering many previously missing African countries.
- **15 REDATAM / RpWebEngine** microdata catalogs across Latin America and the Caribbean.
- National statistics and open data portals for countries and territories with little or no prior coverage, including first entity roots for **CF, DJ, ER, GQ, GW, MC, SD, SM, ST, SZ, TL, TM, VC** (plus new Andorra, Bhutan, Brunei, Hungary, Iran, Iraq, Jordan, Liechtenstein, Monaco, Mongolia, Oman open data, Palau indicators, Romania TEMPO, San Marino, Timor-Leste, Turkmenistan, and others).
- Caribbean OECS geoportal (`gis.oecs.int`) and Haiti data search engine (`ayitistats.org`).
- Language and geography reference support for new coverage: Turkmen (`TK`) in `data/reference/langs.csv` / `langs.tsv`; country entries and domain maps for Eritrea, Eswatini, Monaco, Timor-Leste, and Turkmenistan in `scripts/constants.py`.

### Changed
- Regenerated dataset exports: **14,528** catalog records (entities); 135 software definitions; 0 scheduled.
- Recategorized three existing catalogs: New Caledonia `data.gouv.nc` (`FR/FR-NC` → `NC/Federal`), OPT maps portal (`opendata` → `geo`), and NZ PAM geodata (`opendata` → `geo`).
- Refreshed metadata for Pacific SPREP country portals and selected Australian, Oman, Tajikistan, Samoa, and Minnesota entries (including HTTPS/name updates; Minnesota state portal marked deprecated; Samoa MNRE RIO portal marked inactive).
- Extended TLD-to-language defaults (`.sz` → English, `.mc` → French, `.tl` → Portuguese, `.tm` → Turkmen).

## [1.9.0] - 2026-08-10

**GitHub Release**: [v1.9.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.9.0) - Published August 10, 2026

### Added
- Canonical `owner.type` vocabulary (`data/reference/owner_types.yaml`) with synonym map and quality rules (`OWNER_TYPE_NONCANONICAL` / `INVALID_OWNER_TYPE`).
- Path/country consistency check (`PATH_COUNTRY_MISMATCH`) with allowlisted multinational roots.
- OpenSpec proposals for owner-type/path consistency and endpoint quality priority recalibration.

### Changed
- Regenerated dataset exports and quality reports after integrity cleanup: **14,436** catalog records (entities); 135 software definitions; 0 scheduled.
- Normalized **240** non-canonical `owner.type` values to the canonical vocabulary (e.g. `University` → `Academy`, `Private` → `Business`).
- Corrected path/country placement and metadata for misfiled catalogs (e.g. OpenSLR → `World/`, SoDaNet → `GR/`, SAERI → `FK/`, Gibraltar geoportal → `GI/`, New Caledonia SPREP portal → `NC/`, Italian cadastre geoportal → `IT/`, ITIE Sénégal → `SN/`; Esri China HK and Uruguay INE metadata aligned with path).
- Recalibrated quality priorities so integrity failures remain CRITICAL/IMPORTANT for CI while enrichment-track endpoint gaps stay MEDIUM/warning-only.
- Added missing runtime dependencies to `requirements.txt`; aligned catalog-type keys and re3data HTML parsing with tests.

### Fixed
- Cleared all **CRITICAL** and **IMPORTANT** integrity-track quality issues (remaining open issues are MEDIUM enrichment-track `SOFTWARE_EXPECTED_ENDPOINTS_MISSING_*` only).
- Resolved `DUPLICATE_RECORD_ID` collisions (kept one record or renamed distinct same-domain services such as GeoServer vs IPT).
- Resolved `DUPLICATE_LINK_NORMALIZED` pairs (29 groups): kept preferred keepers (https / non-www / non-Unknown), merged useful metadata, deleted www/duplicate copies.
- Fixed `PATH_COUNTRY_MISMATCH`, `OWNER_LOCATION_SUBREGION_REQUIRED`, `COVERAGE_NORMALIZATION`, and `API_STATUS_MISMATCH` findings.

### Removed
- Consolidated duplicate catalog YAML entries (duplicate ids and normalized-link twins), net reducing the registry from 14,470 to **14,436** entities.

## [1.8.0] - 2026-06-17

**GitHub Release**: [v1.8.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.8.0) - Published June 17, 2026

### Added
- **124 net new catalog entries** (560 added, 460 removed vs v1.7.0); export snapshot: **14,470** catalog records (entities).
- Quality regression guard (`tests/test_quality_regression.py`) and CI job to prevent quality-issue count regressions.
- Software taxonomy discovery guidance in `README.md` (`category`, `subtype` fields).
- Agent and governance documentation links (`llms.txt`, `DATASHEET.md`, `CITATION.cff`, `SECURITY.md`, `CODE_OF_CONDUCT.md`).
- Expanded `devdocs/quality-fix-workflow.md` and API detection regression tests.

### Changed
- **3,312 catalog entries updated** with refreshed metadata; regenerated datasets and quality reports.
- Export snapshots: 14,470 catalog records in `catalogs.jsonl` / `full.jsonl`; 135 software definitions; 0 scheduled.
- Builder, apidetect, enrichment, and fix scripts improved; scope boundary documented in `AGENTS.md`.

### Removed
- **460 catalog entries** removed (inactive, duplicate, or consolidated).

## [1.7.0] - 2026-02-24

**GitHub Release**: [v1.7.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.7.0) - Published February 24, 2026

### Added
- **1,647 new catalog entries** (net from v1.6.0); export snapshot: **14,346** catalog records (entities).

### Changed
- **3,432 catalog entries updated** with refreshed metadata; regenerated datasets and quality reports.
- Export snapshots: 14,346 catalog records in `catalogs.jsonl` / `full.jsonl`; 136 software definitions; 0 scheduled (all promoted or removed).

### Removed
- **3,472 catalog entries** removed (inactive, duplicate, or consolidated).

### Fixed
- Data quality rules and fixes (including API status mismatch handling).
- Subregion name/ID mismatch fixes (`fix_subregion_name_id_mismatch.py`).

## [1.6.0] - 2026-02-21

**GitHub Release**: [v1.6.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.6.0) - Published February 21, 2026

### Added
- **95 new catalog entries** (including Community Statistics Yukon — community-statistics.service.yukon.ca).

### Changed
- **156 catalog entries updated** with refreshed metadata and regenerated datasets and quality reports.
- Export snapshots: **12,699** catalog records (entities); 136 software definitions; combined entities + scheduled in `full.jsonl`.

### Removed
- **1 catalog entry** removed.

### Fixed
- Improved API detection reliability; added regression coverage for apidetect.

## [1.5.0] - 2026-02-12

**GitHub Release**: [v1.5.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.5.0) - Published February 12, 2026

### Changed
- Refreshed catalog metadata across entity YAML records and rebuilt generated dataset artifacts.
- Updated export snapshots in `README.md` to reflect the latest dataset counts (12,697 catalogs; 136 software definitions; 677 scheduled; 13,374 combined entities + scheduled records).
- Refined release documentation in `CHANGELOG.md` and `README.md`.

### Removed
- Removed legacy `History.md`; changelog history is maintained in `CHANGELOG.md`.

## [1.4.0] - 2026-02-09

**GitHub Release**: [v1.4.0](https://github.com/datenoio/dataportals-registry/releases/tag/v1.4.0) - Published February 9, 2026

### Added
- **208 new catalog entries** (12,489 total catalogs, up from 12,281)
- **Many new CKAN data catalogs** from ecosystem.ckan.org synchronization
- **Reference data files** for validation and consistency:
  - `data/reference/access_modes.yaml` - Standardized access mode values
  - `data/reference/catalog_types.yaml` - Allowed catalog type values
  - `data/reference/software_ids.yaml` - Comprehensive software ID mappings
  - `data/reference/status.yaml` - Status value definitions
- **New documentation**:
  - `devdocs/quality-fix-workflow.md` - Guide for fixing data quality issues
  - `devdocs/scheduled-to-entities.md` - Process for promoting scheduled entries to entities
  - `docs/metadata-quality.md` - Metadata quality standards and guidelines
- **OpenSpec proposal** for schema allowed values enhancement

### Changed
- **Schema validation enhanced** with allowed values validation for key fields (access_mode, catalog_type, software.id, status)
- **Raw JSONL files restored** - Both compressed (.zst) and uncompressed versions now available
- **Updated entity metadata** across multiple catalog entries
- Rebuilt JSONL/Parquet exports and type/software slices (12,489 catalogs; 134 software platforms; 758 scheduled sources; 12,623 combined records)
- **Documentation improvements**:
  - Enhanced AGENTS.md with OpenSpec workflow instructions
  - Expanded CONTRIBUTING.md with quality fix workflow and scheduled-to-entities process
  - Updated README.md with latest statistics and data export information

### Fixed
- Various metadata gaps and inconsistencies in catalog entries
- Improved data quality through enhanced validation rules

### Removed
- Legacy files cleaned up from repository

## [1.3.0] - 2025-12-10

### Added
- Zstandard-compressed exports for `catalogs.jsonl`, `software.jsonl`, `scheduled.jsonl`, and `full.jsonl` plus a `datasets.duckdb` snapshot for analytics-friendly queries
- New scientific and API catalogs across Switzerland, EU, France, Germany, Great Britain, and Italy (e.g., Agroportal, TechnoPortal HEVS, EarthPortal, W3C Linked Open Vocabularies, BiodivPortal, MATPortal, OLS4)
- New API registry entry for `api.gov.it` and additional international research repositories
- Generated data quality reports in `dataquality/` with helper scripts (`fix_*_issues.py`) for resolving flagged items

### Changed
- Refreshed and expanded metadata for hundreds of catalog records across Americas, Europe, Asia, and Oceania
- Rebuilt JSONL/Parquet exports and type/software slices (12,281 catalogs; 134 software platforms; 749 scheduled sources; 13,030 combined records)
- Simplified CI test invocation to run from the repository root in `tests.yml`

## [1.2.0] - 2025-11-21

### Added
- **1,993 new data catalog records** across multiple countries and regions
- **1,515 ArcGIS Server instances** - massive expansion of geoportal coverage
- **293 World-level catalogs** - international and global data repositories
- **97 French data catalogs** - significant expansion of French open data coverage
- **Geospatial infrastructure expansion**:
  - 83 GeoServer instances
  - 37 GeoNode installations
  - 33 GeoNetwork catalogs
  - 8 Lizmap instances
  - 3 MapProxy instances
  - 2 MapBender instances
- **Open data platforms**:
  - 47 OpenDataSoft instances
  - 42 CKAN portals
  - 5 DKAN installations
- **Scientific data repositories**:
  - 38 Figshare-based repositories
  - 6 DSpace installations
  - 6 NADA microdata catalogs
- **Additional platforms**: 9 THREDDS servers, 5 Drupal-based catalogs, 3 DataFair instances

### Changed
- **363 records updated** with improved metadata
- Updated API endpoints for IPT-based data catalogs
- Enhanced metadata completeness across multiple records
- Improved catalog endpoints and identifiers
- Better geographic and administrative region coverage

### Fixed
- Multiple data errors and inconsistencies
- Metadata gaps in existing records
- Various catalog identifier issues
- Endpoint validation and corrections

### Statistics

#### Record Changes
- **New records**: 1,993
- **Modified records**: 363
- **Deleted records**: 0

#### Software Types (Top 15)
- ArcGIS Server: 1,515
- Custom/Unknown: 89
- GeoServer: 83
- OpenDataSoft: 47
- CKAN: 42
- Figshare: 38
- GeoNode: 37
- GeoNetwork: 33
- ArcGIS Hub: 26
- THREDDS: 9
- Lizmap: 8
- DSpace: 6
- NADA: 6
- Drupal: 5
- DKAN: 5

#### Catalog Types
- Geoportal: 1,726 (86.6%)
- Open data portal: 181 (9.1%)
- Scientific data repository: 68 (3.4%)
- Microdata catalog: 7
- Indicators catalog: 6
- Datasets list: 3
- Metadata catalog: 2

#### Geographic Coverage

**Countries (Top 20)**:
- United States: 1,472
- World-level: 293
- France: 97
- Netherlands: 11
- Unknown/Unspecified: 11
- Germany: 8
- Italy: 8
- South Africa: 8
- Uganda: 7
- United Kingdom: 6
- Belarus: 5
- Colombia: 5
- Hong Kong: 4
- Croatia: 4
- Iceland: 4
- Japan: 4
- Brazil: 3
- Spain: 3
- European Union: 3
- Thailand: 3

**United States - State Breakdown (Top 20)**:
- Minnesota: 54
- California: 51
- Wisconsin: 43
- Ohio: 42
- Texas: 39
- Florida: 34
- Oregon: 34
- Illinois: 26
- Washington: 26
- District of Columbia: 25
- North Carolina: 24
- Virginia: 23
- Pennsylvania: 20
- Utah: 19
- Colorado: 17
- Indiana: 17
- Michigan: 16
- Georgia: 15
- Missouri: 15
- North Dakota: 12

**Regional Coverage**:
- Federal-level records: 1,138
- US state-level records: 500+
- French regions (Île-de-France): 25
- Additional subregional coverage across multiple countries

## [1.1.0] - 2025-11-15

### Added
- Comprehensive data quality analysis tool (`devdocs/analyze_duplicates_and_errors.py`)
  - Detects duplicate UID's and ID's across all records
  - Identifies missing required fields
  - Finds filename mismatches (where `id` field doesn't match filename)
  - Reports empty files and YAML parsing errors
  - Generates detailed reports in JSON, Markdown, and text formats

### Changed
- Updated README.md with data quality and validation section
- Added documentation for analysis tools in `devdocs/` directory

### Fixed
- Identified 7 duplicate ID's (same ID in both entities and software directories)
- Identified 204 records missing required `uid` field
- Identified 63 files with filename mismatches
- Identified 1 empty file requiring attention

## [2024-04-13]

### Added
- Several scientific and geo data catalogs
- Changelog (History.md)

### Fixed
- Malawi geoportal uid
- API endpoint errors
- Schema mistakes and updated validation
- Various catalog identifiers and metadata

### Changed
- Major updates to Finnish data portals
- Updated many scientific data catalogs
- Updated API endpoints for multiple platforms

