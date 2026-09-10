# Discovering domain scientific repositories

Biodiversity, facility, crop, chemistry, and earth-system repositories (`catalog_type: Scientific data repository`). Institutional IRs: [discovery-scientific.md](discovery-scientific.md). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). Harvest: [harvest-scientific-domain.md](harvest-scientific-domain.md).

High-count domain stacks with their own recipes: IPT, Symbiota, THREDDS, ERDDAP, FROST-Server, Breedbase, Tripal, VEuPathDB, MassBank, ioChem-BD, ESGF, ALA, BirdMap Africa, SciCat, InterMine, GRIN-Global, PlutoF, JGI Genome Portal, cBioPortal, ESA Science Archive, CLLD, TalkBank, Pathway Tools, IBDC.

One portal / node = one registry record. Do not add gene pages, occurrences, or ESGF data nodes as extra catalogs.

Ocean and earth **directories** (not software): [ODIS](https://catalogue.odis.org/), [PANGAEA harvest sources](https://www.pangaea.de/), [WMO WIS2 GDC](https://gdc.wis.cma.cn/), DataONE member nodes, [CLARIN](https://www.clarin.eu/) / VLO. Treat each as a named-list hunt ([discovery.md](discovery.md#hunt-patterns)); skip org homepages and hijacked hosts.

## GBIF IPT (`ipt`) {#ipt}

Integrated Publishing Toolkit for biodiversity data. List: [gbif.org/ipt](https://www.gbif.org/ipt).

**Confirm:** `/rss.do`, `/inventory/dataset`, or the IPT homepage with installation name.

| Tool | Query |
|------|-------|
| Google | `"Integrated Publishing Toolkit" IPT GBIF` |
| Google | `inurl:/ipt "GBIF"` |
| Censys | `web.endpoints.http.body: "Integrated Publishing Toolkit"` |
| FOFA | `body="Integrated Publishing Toolkit"` |

Prefer GBIF’s official installation list, then fill gaps with search.

## Symbiota (`symbiota`) {#symbiota}

Open-source biodiversity collections CMS. Official portal directory: [symbiota.org/symbiota-portals](https://symbiota.org/symbiota-portals/). Docs: [docs.symbiota.org](https://docs.symbiota.org/).

Theme-based portals (SEINet, MyCoPortal, CCH2, Ecdysis, and others) publish specimen occurrences, images, checklists, and Darwin Core datasets. Register **one catalog per portal**, not per collection or GBIF IPT mirror. Use `software.id: symbiota`.

**Confirm:** public collection search (`/collections/index.php` or `/portal/collections/`) and/or dataset RSS at `/collections/datasets/rsshandler.php`. Page signals include “Symbiota”, `collid=`, and “Search Collections”. Skip login-only portals and the vendor homepage.

| Tool | Query |
|------|-------|
| Google | `"Powered by Symbiota" OR "Symbiota portal" (collections OR occurrences) -site:symbiota.org -site:github.com` |
| Google | `inurl:/collections/datasets/rsshandler.php` |
| Censys | `web.endpoints.http.body: "Symbiota"` |
| FOFA | `body="Symbiota"` |

## THREDDS (`thredds`) {#thredds}

Scientific data servers (often climate/ocean). **Confirm:** `/thredds/catalog.html` or `/thredds/catalog.xml`.

| Tool | Query |
|------|-------|
| Google | `inurl:/thredds/catalog.html` |
| Google | `"THREDDS Data Server" catalog` |
| Censys | `web.endpoints.http.body: "THREDDS"` |
| FOFA | `body="THREDDS"` |
| Shodan | `http.html:"THREDDS Data Server"` |

## ERDDAP (`erddap`) {#erddap}

NOAA-style tabular/gridded data server. **Confirm:** `/erddap/index.html` or `/erddap/info/index.json`.

| Tool | Query |
|------|-------|
| Google | `inurl:/erddap "ERDDAP"` |
| Censys | `web.endpoints.http.body: "ERDDAP"` |
| FOFA | `body="ERDDAP"` |

## FROST-Server (`frostserver`) {#frostserver}

Fraunhofer IOSB open-source OGC SensorThings API server. Product: [FROST-Server](https://www.iosb.fraunhofer.de/en/projects-and-products/frost-server.html); source: [github.com/FraunhoferIOSB/FROST-Server](https://github.com/FraunhoferIOSB/FROST-Server). Register one public SensorThings catalog per independently operated instance. Typical `catalog_type` is Scientific data repository (urban IoT and groundwater stations are still a Things/Datastreams catalog, not a map viewer). Distinct from THREDDS, ERDDAP, and a SensorThings endpoint that is only a download option on another catalog.

**Confirm:** JSON at `/v1.1/`, `/v1.0/`, or `/FROST-Server/v1.1/` listing `Things` / `Datastreams` / `Locations`, or the default HTML start page titled `Start Page` with heading `FROST-Server`. `Things?$top=1&$count=true` returns `@iot.count`. Skip Fraunhofer k8s demos, SensorUp scratchpads, login-walled hydrometry, and hosts with only a single Thing.

| Tool | Query |
|------|-------|
| Google | `"FROST-Server" (SensorThings OR Things OR Datastreams) -site:github.com` |
| Google | `inurl:/FROST-Server/ "Start Page"` |
| Censys | `web.endpoints.http.body: "FROST-Server"` |
| FOFA | `body="FROST-Server"` |

## OPeNDAP (`opendap`) {#opendap}

Remote subsetting protocol and server ecosystem. Site: [opendap.org](https://www.opendap.org). Use `opendap` for a public OPeNDAP catalog whose server implementation is not identified as Hyrax, Pydap, THREDDS, or ERDDAP. Do not register OPeNDAP only as a download option on a THREDDS (`thredds`) or ERDDAP (`erddap`) catalog.

**Confirm:** GET a DAP catalog or directory listing and verify that it exposes multiple datasets.

| Tool | Query |
|------|-------|
| Google | `"OPeNDAP" ("catalog.xml" OR DODS) -Hyrax -site:opendap.org -site:github.com` |
| Censys | `web.endpoints.http.body: "OPeNDAP"` |
| FOFA | `body="OPeNDAP"` |

## OPeNDAP Hyrax (`opendaphyrax`) {#opendaphyrax}

The OPeNDAP 4 Data Server, unrelated to the Samvera repository product that uses `software.id: hyrax`. Register one public Hyrax server per independently operated dataset catalog. Prefer `thredds` or `erddap` when Hyrax is only an alternate access service for one of those catalogs.

**Confirm:** the directory page title starts with `OPeNDAP Hyrax: Contents of`, the footer reports `Hyrax (version)`, or `/opendap/catalog.xml` returns the server catalog.

| Tool | Query |
|------|-------|
| Google | `"OPeNDAP Hyrax: Contents of" -site:opendap.org -site:github.com` |
| Google | `inurl:/opendap/ "Hyrax development sponsored by"` |
| Censys | `web.endpoints.http.body: "OPeNDAP Hyrax"` |
| FOFA | `body="OPeNDAP Hyrax"` |

## DataONE (`dataone`) {#dataone}

Earth-science member-node network. Site: [dataone.org](https://www.dataone.org). Prefer the **member node** catalog URL, not every harvested dataset.

**Confirm:** GET the member-node home. Duplicate-check before adding nodes already in re3data / this registry.

| Tool | Query |
|------|-------|
| Google | `"DataONE" ("member node" OR MN) repository` |
| Censys | `web.endpoints.http.body: "DataONE"` |
| FOFA | `body="DataONE"` |

## MOLGENIS (`molgenis`) {#molgenis}

Configurable FAIR scientific data platform used for research catalogues, biobank
directories, and registries. Site and public-instance list: [molgenis.org/tools](https://molgenis.org/tools.html).

**Signals:** current EMX2 catalogues say “Created with MOLGENIS” and expose
`/api/graphql`, `/api/rdf`, or `/<database>/api/csv/<table>`. Legacy installations
use `molgenis.do`, often below a project path. A generic University of Groningen
page is not sufficient evidence.

**Confirm:** GET the public catalogue/search UI and one read-only API surface when
available. Register one public catalogue or registry per installation, not each
database table, cohort, biobank, or variable.

| Tool | Query |
|------|-------|
| Google | `"Created with MOLGENIS" (catalogue OR registry OR collections)` |
| Google | `inurl:molgenis.do (data OR database OR repository)` |
| Censys | `web.endpoints.http.body: "Created with MOLGENIS"` |
| FOFA | `body="Created with MOLGENIS"` |

## BEXIS2 (`bexis2`) {#bexis2}

Open-source research data management and repository platform for structured and
unstructured data. Site: [bexis2.uni-jena.de](https://bexis2.uni-jena.de/). Public
instances can be heavily themed, so confirm both the application route and assets.

**Signals:** root redirects to `/home/Start`; BEXIS2 name or footer; `/Content/`
assets and ASP.NET application; read-only `/api/dataset`, `/api/metadata/{id}`, or
`/api/data/{id}` endpoints.

**Confirm:** GET the public search and a read-only dataset API. Register one BEXIS2
installation, not each project, metadata schema, or dataset.

| Tool | Query |
|------|-------|
| Google | `"BEXIS2" (repository OR "research data") -site:github.com` |
| Google | `inurl:/home/Start BEXIS` |
| Censys | `web.endpoints.http.body: "BEXIS2"` |
| FOFA | `body="BEXIS2"` |

## Diversity Workbench (`diversityworkbench`) {#diversityworkbench}

Modular bio- and geodiversity research-data environment maintained by the SNSB IT
Center and partners. Site: [diversityworkbench.net](https://www.diversityworkbench.net/).
Deployments often publish through project-specific web interfaces or the SNSB
BioCASe/RDF pipeline rather than a uniform DWB homepage.

**Signals:** explicit “Diversity Workbench” or “DWB” attribution; modules such as
DiversityCollection, DiversityDescriptions, DiversityTaxonNames, or DiversityProjects;
BioCASe/ABCD publication backed by a DWB cache database; `id.snsb.info` RDF identifiers.

**Confirm:** require an explicit DWB attribution from the portal or its operator. One
public catalog or publication pipeline = one registry record; do not register every DWB
module, project database, BioCASe datasource, or occurrence record separately.

| Tool | Query |
|------|-------|
| Google | `"Diversity Workbench" (database OR repository OR data)` |
| Google | `"DiversityCollection" (BioCASe OR RDF OR dataset)` |
| Censys | `web.endpoints.http.body: "Diversity Workbench"` |
| FOFA | `body="Diversity Workbench"` |

## Greenstone (`greenstone`) {#greenstone}

Open-source digital-library collection software from the University of Waikato. The
[official examples page](https://www.greenstone.org/examples) lists independent public
libraries built with Greenstone 2 and Greenstone 3.

**Signals:** Greenstone 3 uses `/greenstone3/<library>/collection/<collection>/...`,
`xmlns:gs3`, `greenstone.org/gs3`, or an `/greenstone3/oaiserver` endpoint. Legacy
Greenstone 2 installations commonly use `/greenstone/cgi-bin/library.cgi`.

**Confirm:** GET the library home and, when enabled, the OAI Identify response. Register
one independently operated library/catalog, not every collection inside it.

| Tool | Query |
|------|-------|
| Google | `inurl:/greenstone3/library/collection` |
| Google | `inurl:/greenstone/cgi-bin/library.cgi (collection OR library)` |
| Censys | `web.endpoints.http.body: "greenstone.org/gs3"` |
| FOFA | `body="greenstone.org/gs3"` |

## VIVO (`vivo`) {#vivo}

Open-source semantic web platform for research discovery. Site:
[vivo.lyrasis.org](https://vivo.lyrasis.org/). VIVO normally catalogs people and
research activity, but some deployments also index datasets and repository records.

**Signals:** VIVO attribution together with `vitro`/`vivo` assets; RDF entity pages;
faceted classes for datasets or data records; `/api/sparqlQuery`, `/reconcile`, or a
configured Data Distribution API.

**Confirm:** the installation must expose a public dataset or research-object catalog.
Do not register a profiles-only VIVO deployment, individual researcher pages, or the
project website itself.

| Tool | Query |
|------|-------|
| Google | `"Powered by VIVO" (dataset OR repository OR data)` |
| Google | `"VIVO" "research data" (search OR repository)` |
| Censys | `web.endpoints.http.body: "vitro" AND web.endpoints.http.body: "VIVO"` |
| FOFA | `body="vitro" && body="VIVO"` |

## CWIS (`cwis`) {#cwis}

The Collection Workflow Integration System is an open-source metadata collection and
digital-library platform from Internet Scout. Site:
[scout.wisc.edu/cwis](https://scout.wisc.edu/cwis).

**Signals:** “Powered by CWIS” or the expanded product name; CWIS PHP assets; a root
OAI-PMH response using `?verb=Identify`; qualified Dublin Core and RSS links.

**Confirm:** GET the public resource search and OAI Identify response. Avoid the unrelated
Chest Wall Injury Society acronym. One CWIS collection site = one registry record.
INFOMED `tesis.sld.cu` and the Artemisa provincial node are verified CWIS catalogs
(CWIS JavaScript and a `scout.wisc.edu/cwis` credit).

| Tool | Query |
|------|-------|
| Google | `"Powered by CWIS" (repository OR collection OR resources)` |
| Google | `"Collection Workflow Integration System" -site:scout.wisc.edu` |
| Censys | `web.endpoints.http.body: "Powered by CWIS"` |
| FOFA | `body="Powered by CWIS"` |

## Galaxy (`galaxy`) {#galaxy}

Usable-analysis platform that sometimes publishes public data libraries. Site: [usegalaxy.org](https://usegalaxy.org). Register **public Galaxy instances with a data library / shared histories catalog**, not every private analysis server.

**Confirm:** GET the instance and a public data-library or toolshed-adjacent dataset listing.

| Tool | Query |
|------|-------|
| Google | `"Galaxy" ("data libraries" OR usegalaxy) -site:galaxyproject.org` |
| Censys | `web.endpoints.http.body: "usegalaxy"` |
| FOFA | `body="usegalaxy"` |

## Atlas of Living Australia (`ala`) {#ala}

Biodiversity occurrence catalogs (ALA and national living-atlas forks). Site: [ala.org.au](https://www.ala.org.au).

**Confirm:** GET the public occurrence/search portal. One record per national atlas, not per collection.

| Tool | Query |
|------|-------|
| Google | `"Atlas of Living Australia" OR "Living Atlas" (occurrences OR biocache)` |
| Censys | `web.endpoints.http.body: "biocache"` |
| FOFA | `body="biocache"` |

## BirdMap Africa (`birdmap`) {#birdmap}

Citizen-science bird atlas platform of the African Bird Atlas Project. Site: [birdmap.africa](https://www.birdmap.africa/). Country portals share `{project}.birdmap.africa` (SABAP2, Nigeria, Kenya, Senegal, and others). Distinct from BirdLasser (the mobile submission app) and from Living Atlases (`ala`).

**Signals:** host `*.birdmap.africa`; pentad coverage maps; SABAP2 protocol; API `api.birdmap.africa/{project}/v2/`.

**Confirm:** GET the country portal home. One record per country project, not per pentad or species page. Skip `symbiota.birdmap.africa` when it is already a Symbiota catalog.

| Tool | Query |
|------|-------|
| Google | `site:birdmap.africa (atlas OR pentad OR SABAP)` |
| Google | `"Bird Atlas" (SABAP2 OR Nigeria OR Kenya) birdmap` |
| Censys | `web.names: "birdmap.africa"` |
| FOFA | `domain="birdmap.africa"` |
| crt.sh | `%.birdmap.africa` |

## CLLD (`clld`) {#clld}

Cross-Linguistic Linked Data web apps. Site: [clld.org](https://clld.org). Public databases such as Grambank, Lexibank, and Pofatu run on `{project}.clld.org` with `clld-static` assets.

**Signals:** hostname `*.clld.org`; `clld-static` JS; Cross-Linguistic Linked Data branding.

**Confirm:** GET the project home. One record per CLLD app, not per language or parameter page. Skip clld.org marketing.

| Tool | Query |
|------|-------|
| Google | `site:clld.org (Grambank OR Lexibank OR Pofatu OR "Cross-Linguistic")` |
| Google | `"Cross-Linguistic Linked Data" OR "clld-static"` |
| Censys | `web.names: "clld.org"` |
| FOFA | `domain="clld.org"` |
| crt.sh | `%.clld.org` |

## TalkBank (`talkbank`) {#talkbank}

Shared spoken-language transcript banks. Site: [talkbank.org](https://talkbank.org). Collections such as CHILDES, AphasiaBank, and FluencyBank run on `{bank}.talkbank.org` with the CHAT format and a common browser.

**Signals:** hostname `*.talkbank.org`; CHAT / CLAN; TalkBank, CHILDES, AphasiaBank, or FluencyBank branding.

**Confirm:** GET the bank home. One record per TalkBank collection, not per transcript or speaker. Skip talkbank.org manuals and software-download pages as extra catalogs.

| Tool | Query |
|------|-------|
| Google | `site:talkbank.org (CHILDES OR AphasiaBank OR FluencyBank OR CHAT)` |
| Google | `"TalkBank" (CHILDES OR "AphasiaBank") -site:github.com` |
| Censys | `web.names: "talkbank.org"` |
| FOFA | `domain="talkbank.org"` |
| crt.sh | `%.talkbank.org` |

## SciCat (`scicat`) {#scicat}

Metadata catalogue for photon/neutron facilities. Docs: [scicatproject.github.io](https://scicatproject.github.io).

**Signals:** SciCat Angular UI; `/api/v3/` or dataset DOI landing pages (PSI, ESS, MAX IV).

**Confirm:** GET the public dataset search. One record per facility catalogue.

| Tool | Query |
|------|-------|
| Google | `"SciCat" (dataset OR catalogue) (ESS OR PSI OR "MAX IV") -site:github.com` |
| Censys | `web.endpoints.http.body: "scicat"` |
| FOFA | `body="scicat"` |

## Axiom Data Science Portal (`axiomportal`) {#axiomportal}

IOOS-style ocean observing explorer (Axiom). Distinct from ERDDAP/THREDDS backends.

**Signals:** Axiom portal chrome; sensor time series; compiled data views.

**Confirm:** GET the public portal home. Do not also register the bundled ERDDAP as a second catalog unless it is a separate public product.

| Tool | Query |
|------|-------|
| Google | `"Axiom" ("Data Science" OR IOOS) portal` |
| Censys | `web.endpoints.http.body: "axiomdatascience"` |
| FOFA | `body="axiomdatascience"` |

## OntoPortal (`ontoportal`) {#ontoportal}

Ontology repositories (BioPortal-style). Site: [ontoportal.org](https://ontoportal.org).

**Confirm:** GET the public ontology browser / REST. One record per public OntoPortal appliance.

| Tool | Query |
|------|-------|
| Google | `"OntoPortal" OR "BioPortal" (ontology repository) -site:bioontology.org` |
| Censys | `web.endpoints.http.body: "ontoportal"` |
| FOFA | `body="ontoportal"` |

## Breedbase (`breedbase`) {#breedbase}

Crop breeding information systems. Site: [breedbase.org](https://breedbase.org). Instances include CassavaBase, MusaBase, YamBase, SweetPotatoBase, Sol Genomics Network, and Triticeae Toolbox (T3).

**Signals:** Breedbase chrome; `/brapi/v2/serverinfo`; crop “Base” branding.

**Confirm:** GET `https://host/brapi/v2/serverinfo` JSON, or the public trial/search UI. One record per crop instance, not per trial.

| Tool | Query |
|------|-------|
| Google | `"Breedbase" OR CassavaBase OR MusaBase OR YamBase OR SweetPotatoBase (breeding OR BrAPI)` |
| Google | `inurl:/brapi/v2/serverinfo` |
| Censys | `web.endpoints.http.body: "Breedbase"` |
| FOFA | `body="Breedbase"` |

## Tripal (`tripal`) {#tripal}

GMOD Tripal genome databases (Drupal + Chado). Site: [tripal.info](https://tripal.info).

**Signals:** “Powered by Tripal”; `/web-services/`; Chado/Tripal footer.

**Confirm:** GET the public organism/dataset home or Tripal web services. Skip generic Drupal sites without Chado biological content. Prefer Tripal over `drupal` when the catalog is a genome database.

| Tool | Query |
|------|-------|
| Google | `"Powered by Tripal" OR "Tripal" (genome OR germplasm OR Chado) -site:tripal.info -site:github.com` |
| Censys | `web.endpoints.http.body: "Tripal"` |
| FOFA | `body="Tripal"` |

## VEuPathDB (`veupathdb`) {#veupathdb}

EuPathDB WDK organism sites. Hub: [veupathdb.org](https://veupathdb.org). Component sites include PlasmoDB, FungiDB, VectorBase, and TriTrypDB.

**Signals:** VEuPathDB / EuPathDB chrome; search-strategy UI; `/webservices/`.

**Confirm:** GET the public search home. One record per organism portal (plus the hub if it is a distinct catalog UI). Do not add every gene page.

| Tool | Query |
|------|-------|
| Google | `"VEuPathDB" OR EuPathDB OR PlasmoDB OR FungiDB OR VectorBase OR TriTrypDB (genome OR "data set")` |
| Censys | `web.endpoints.http.body: "VEuPathDB"` |
| FOFA | `body="VEuPathDB"` |

## MassBank (`massbank`) {#massbank}

Community reference mass-spectral databases. Instances: MassBank Europe, MassBank Japan, MoNA.

**Signals:** MassBank record IDs; `/MassBank/` UI; MoNA `/rest/spectra`.

**Confirm:** GET the public spectral search. One record per instance, not per spectrum.

| Tool | Query |
|------|-------|
| Google | `"MassBank" (spectra OR "mass spectral") (database OR repository) -site:github.com` |
| Google | `"MassBank of North America" OR MoNA spectra` |
| Censys | `web.endpoints.http.body: "MassBank"` |
| FOFA | `body="MassBank"` |

## ioChem-BD (`iochembd`) {#iochembd}

Distributed computational-chemistry repository. Site: [iochem-bd.org](https://www.iochem-bd.org). Browse modules are DSpace-based; use `iochembd` (not `dspace`) when the product is ioChem-BD.

**Signals:** ioChem-BD branding; `/rest/items`; `/oai/request?verb=Identify`; CML datasets.

**Confirm:** GET the public Browse collections or OAI Identify. Register each **public node** and the central Find index as distinct catalogs. Skip Create-only private workspaces.

| Tool | Query |
|------|-------|
| Google | `"ioChem-BD" (repository OR "computational chemistry") -site:github.com` |
| Censys | `web.endpoints.http.body: "ioChem-BD"` |
| FOFA | `body="ioChem-BD"` |

## ESGF (`esgf`) {#esgf}

Earth System Grid Federation **search/index** (Metagrid, esg-search). Site: [esgf.llnl.gov](https://esgf.llnl.gov).

**Signals:** Metagrid UI; `/esg-search/search`; CMIP dataset index.

**Confirm:** GET a working esg-search query or the public Metagrid home. Use `thredds` for ESGF **data nodes** that expose `/thredds/catalog.xml`. Do not clone every data node as `esgf`.

| Tool | Query |
|------|-------|
| Google | `"ESGF" OR Metagrid ("esg-search" OR CMIP) (catalog OR search)` |
| Censys | `web.endpoints.http.body: "esg-search"` |
| FOFA | `body="esg-search"` |

## ICAT (`icat`) {#icat}

Facility scientific catalog. Site: [icatproject.org](https://icatproject.org).

**Confirm:** GET the public dataset search UI or documented ICAT REST/OAI. Skip facility login-only stores. Do not clone icatproject.org itself.

| Tool | Query |
|------|-------|
| Google | `"ICAT" (facility OR "data catalog" OR "scientific data") -site:icatproject.org -site:github.com` |
| Censys | `web.endpoints.http.body: "icat"` |
| FOFA | `body="icat"` |

## InterMine (`intermine`) {#intermine}

Biological data warehouse. Site: [intermine.org](https://intermine.org). Organism mines (FlyMine, HumanMine, WheatMine, and others) share `/begin.do` and `/service/version`. Register **each public mine**, not the InterMine project hub.

**Confirm:** GET `/begin.do` or `/service/version`. Skip intermine.org marketing and a single gene report.

| Tool | Query |
|------|-------|
| Google | `"InterMine" OR FlyMine OR HumanMine ("begin.do" OR "web service") -site:intermine.org -site:github.com` |
| Censys | `web.endpoints.http.body: "InterMine"` |
| FOFA | `body="InterMine"` |

## GRIN-Global (`gringlobal`) {#gringlobal}

Genebank information system (USDA NPGS, AAFC, and other centres). Site: [grin-global.org](https://www.grin-global.org).

**Confirm:** GET a public `/gringlobal/` accession or taxonomy search. One record per national/centre installation. Skip the vendor homepage.

| Tool | Query |
|------|-------|
| Google | `"GRIN-Global" OR inurl:/gringlobal/ (accession OR germplasm) -site:grin-global.org` |
| Censys | `web.endpoints.http.body: "GRIN-Global"` |
| FOFA | `body="GRIN-Global"` |

## PlutoF (`plutof`) {#plutof}

University of Tartu biodiversity workbench. Site: [plutof.ut.ee](https://plutof.ut.ee). Public API at `https://api.plutof.ut.ee/v1/`. Do **not** remap UNITE (`unite.ut.ee`) — UNITE is a sequence database that uses PlutoF as a companion workbench.

**Confirm:** GET the public PlutoF catalog or `/v1/` API. One record per PlutoF product (workbench vs DOI landing), not per UNITE taxon page.

| Tool | Query |
|------|-------|
| Google | `"PlutoF" (repository OR biodiversity OR DOI) site:.ee` |
| Censys | `web.endpoints.http.body: "PlutoF"` |
| FOFA | `body="PlutoF"` |

## JGI Genome Portal (`jgi`) {#jgi}

DOE Joint Genome Institute portal family (MycoCosm, PhycoCosm, Phytozome). Confirm the Genome Portal UI, not IMG, GOLD, or `data.jgi.doe.gov` (those stay `custom`).

**Confirm:** GET `https://genome.jgi.doe.gov/portal/` or a MycoCosm/Phytozome organism catalog. Skip gene pages and login-only workspaces.

| Tool | Query |
|------|-------|
| Google | `"JGI Genome Portal" OR MycoCosm OR Phytozome OR PhycoCosm (genome OR catalog) site:jgi.doe.gov` |
| Censys | `web.endpoints.http.body: "JGI Genome Portal"` |
| FOFA | `body="JGI Genome Portal"` |

## cBioPortal (`cbioportal`) {#cbioportal}

Cancer genomics study portal. Site: [cbioportal.org](https://www.cbioportal.org). Independent hospital/consortium instances share `/api/info`. Not OntoPortal.

**Confirm:** GET `/api/info` (`portalVersion`) or the public study list. One record per public instance. Skip a single study landing page.

| Tool | Query |
|------|-------|
| Google | `"cBioPortal" ("cancer genomics" OR studies) -site:github.com` |
| Censys | `web.endpoints.http.body: "cBioPortal"` |
| FOFA | `body="cBioPortal"` |

## ESA Science Archive (`esasciencearchive`) {#esasciencearchive}

ESA Science Data Centre archives (Gaia, XMM-Newton, Herschel, Planck, Euclid, and related ESAC hosts). TAP/VOSI is the shared catalog protocol.

**Confirm:** GET TAP `/tap/capabilities` or `/tap-server/tap/capabilities`. One record per mission archive, not per observation or FITS file.

| Tool | Query |
|------|-------|
| Google | `"ESA Science Archive" OR ESAC (TAP OR VOSI OR Gaia OR XMM) site:esac.esa.int` |
| Censys | `web.endpoints.http.body: "ESA Science Archive"` |
| FOFA | `body="ESA Science Archive"` |

## Pathway Tools (`pathwaytools`) {#pathwaytools}

SRI International Pathway/Genome Database software. Site: [bioinformatics.ai.sri.com/ptools](https://bioinformatics.ai.sri.com/ptools/). BioCyc family hosts (EcoCyc, MetaCyc, YeastCyc, biocyc.org) share the Pathway Tools web UI.

**Signals:** “Pathway Tools” / SRI International in the page; BioCyc organism/PGDB switcher; pathway and genome browsers.

**Confirm:** GET the public organism or collection home with Pathway Tools branding. One catalog per **PGDB / collection host**, not per gene or pathway page.

| Tool | Query |
|------|-------|
| Google | `"Pathway Tools" (BioCyc OR EcoCyc OR MetaCyc) (database OR PGDB) -site:github.com` |
| Google | `site:biocyc.org OR site:ecocyc.org OR site:metacyc.org` |
| Censys | `web.endpoints.http.body: "Pathway Tools"` |
| FOFA | `body="Pathway Tools"` |

## IBDC (`ibdc`) {#ibdc}

Indian Biological Data Centre archives. Hub: [ibdc.dbt.gov.in](https://ibdc.dbt.gov.in/). Domain archives (INDA, IPD, IMDA, IADA, IBIA, IPR, ISDA, GenomeIndia, ICPD) share that host.

**Signals:** hostname `ibdc.dbt.gov.in`; IBDC / Indian Biological Data Centre branding; archive-specific paths (`/inda/`, `/ipd/`, `/imda/`).

**Confirm:** GET the archive home. One catalog per **archive path**, not per accession. Do not add the hub marketing page as a separate catalog if it only links to archives already registered.

| Tool | Query |
|------|-------|
| Google | `"Indian Biological Data Centre" OR IBDC (INDA OR "proteome databank") site:ibdc.dbt.gov.in` |
| Censys | `web.names: "ibdc.dbt.gov.in"` |
| FOFA | `host="ibdc.dbt.gov.in"` |

## Specify Web Portal (`specify`) {#specify}

Shared public collection frontend from the Specify Collections Consortium. Start with the
[maintainer's instance list](https://speciforum.org/t/specify-web-portal-examples/723),
which includes independent university and museum deployments.

**Signals:** Specify branding, collection selectors, specimen/image/map views and configured
Solr collection cores. Confirm the product in HTML and collection configuration; Solr alone
is not a Specify fingerprint. Example: `https://specifyportal.uog.edu/`.

**Search:** `"Specify Web Portal" (museum OR collection OR university)`.
Register the public collection portal, not a staff login or each specimen page.


| Tool | Query |
|------|-------|
| Google | `"Specify Web Portal" (museum OR collection OR university)` |
| Censys | `web.endpoints.http.body: "Specify Web Portal"` |
| FOFA | `body="Specify Web Portal"` |


## BRAHMS Online (`brahmsonline`) {#brahmsonline}

Web publishing component of BRAHMS, distinct from its desktop collection-management client.
The [official website list](https://herbaria.plants.ox.ac.uk/bol/brahms/Websites)
includes Oxford-hosted projects and independently hosted servers.

**Signals:** `/bol/{project}` routes together with BRAHMS Online attribution and collection
search pages. A `/bol/` path alone is insufficient. Confirm the public project's branding;
Mauritius Herbarium explicitly attributes its database to BRAHMS.

**Search:** `"BRAHMS Online" (herbarium OR specimens)` and `inurl:/bol/ "BRAHMS"`.
Count distinct published collections, not botanical species pages or product documentation.


| Tool | Query |
|------|-------|
| Google | `"BRAHMS Online" (herbarium OR specimens)` |
| Censys | `web.endpoints.http.body: "/bol/"` |
| FOFA | `body="BRAHMS Online"` |


## LOVD (`lovd`) {#lovd}

Reusable Leiden Open Variation Database software. The maintainer's
[installation directory](https://lovd.nl/3.0/public_list) identifies independent deployments.

**Signals:** LOVD version banner and gene/variant database navigation; corroborate with the
installation directory or [upstream source](https://github.com/LOVDnl/LOVD3).
Do not classify arbitrary variant databases or every link in the broader LSDB directory as LOVD.

**Search:** `"LOVD" "variants" "genes" -site:lovd.app`.
The registered `www.lovd.nl` URL is a network/software entry page linking to databases;
resolve the intended installation before harvesting or adding an API endpoint.


| Tool | Query |
|------|-------|
| Google | `"LOVD" variants genes -site:lovd.app` |
| Censys | `web.endpoints.http.body: "Leiden Open Variation Database"` |
| FOFA | `body="LOVD" && body="variants"` |


## DaCHS (`dachs`) {#dachs}

[GAVO DaCHS](https://docs.g-vo.org/DaCHS/) is a reusable Virtual Observatory publishing stack.
**Signals:** a `Server: DaCHS/...` response header, or the combined GAVO stylesheet/scripts
(`gavo_dc.css`, `gavo.js`) and characteristic GAVO functions in TAP capability responses.
Legacy routes can include `/__system__/tap/run/tap/capabilities`. TAP support alone is not
specific: Daiquiri and other products also implement it.

**Confirm:** GET the registered homepage and advertised TAP capabilities; check XML response
content, not merely HTTP 200. GAVO, ASTRON and ArVO are verified examples.
**Search:** `"gavo_dc.css"` or `"DaCHS" "data center"`.
Treat GAVO's `dc.g-vo.org` and `dc.zah.uni-heidelberg.de` as a potential alias pair during
new-record discovery; matching software on two registry records does not prove two deployments.


| Tool | Query |
|------|-------|
| Google | `"gavo_dc.css" OR "DaCHS" "data center"` |
| Censys | `web.endpoints.http.body: "gavo_dc.css"` |
| FOFA | `body="gavo_dc.css"` |
| FOFA | `header="DaCHS"` |


## Daiquiri (`daiquiri`) {#daiquiri}

[AIP's publication framework](https://django-daiquiri.github.io/docs/) is used for Gaia@AIP,
RAVE, CosmoSim, APPLAUSE, MUSE-Wide, CARS, and CLUES. The documentation links to actual deployments.
**Signals:** a “Proudly powered by Daiquiri” footer linking to the upstream project;
query interfaces and `/metadata/` schema/table pages corroborate the product identity.
**Search:** `"Proudly powered by" "Daiquiri"`.
Confirm the data portal itself: an AIP hostname, astronomical subject or TAP endpoint alone
is insufficient. Legacy and current generations can have different routes.


| Tool | Query |
|------|-------|
| Google | `"Proudly powered by" Daiquiri` |
| Censys | `web.endpoints.http.body: "Proudly powered by Daiquiri"` |
| FOFA | `body="Proudly powered by Daiquiri"` |


## AMBIT (`ambit`) {#ambit}

[AMBIT](https://ambit.sourceforge.net/) is reusable cheminformatics software supporting
OpenTox and eNanoMapper interfaces. **Signals:** an AMBIT version banner, links to the
upstream installation guide, and substance/dataset/compound routes. The eNanoMapper site
explicitly identifies itself as a customized AMBIT deployment.

**Confirm:** request the homepage with `Accept: text/html` to see its product attribution,
then inspect a small advertised substance search response. RDF content negotiation can hide
HTML branding. A previous timeout alone does not establish inactivity.
**Search:** `"AMBIT" "eNanoMapper" "database"` or `"AMBIT REST web services"`.
Avoid confusing this product with unrelated software also named Ambit.


| Tool | Query |
|------|-------|
| Google | `"AMBIT" ("eNanoMapper" OR "REST web services") database -site:sourceforge.net` |
| Censys | `web.endpoints.http.body: "AMBIT REST"` |
| FOFA | `body="AMBIT REST web services"` |


## ESIMO (`esimo`) {#esimo}

Russia's Unified State System of Information on the World Ocean is a federated marine
data infrastructure with a central portal and regional information-technology nodes.
Typical installations use `/portal/portal/esimo-user/` routes, ESIMO-specific
`/portal-ajax/jquery/esimo.*.js` files, and an `esimo-central` portal theme. Regional
operator documentation may identify a RITU or ESIMO centre and the shared distributed
database and metadata technologies.

**Confirm:** match the ESIMO name and common portal assets or official node documentation.
A marine institute hostname or a JBoss portal alone is insufficient. Register the central
catalog and independently operated regional nodes, not individual applications or data
resources within a node.

**Search:** `"Портал ЕСИМО"`, `inurl:/portal/portal/esimo-user/`, or
`"portal-ajax" "esimo.resources.js"`.


| Tool | Query |
|------|-------|
| Google | `"Портал ЕСИМО" OR inurl:/portal/portal/esimo-user/` |
| Censys | `web.endpoints.http.body: "esimo.resources.js"` |
| FOFA | `body="esimo.resources.js"` |


## MINERVA (`minerva`) {#minerva}

LCSB Luxembourg pathway-map platform. Docs: [minerva.pages.uni.lu](https://minerva.pages.uni.lu/). MINERVA-Net ([minerva-net.lcsb.uni.lu](https://minerva-net.lcsb.uni.lu/)) is the public registry of hosted maps. Independent instances serve `/minerva/` UIs and a REST API.

**Confirm:** GET the instance home or MINERVA-Net. Title/body `MINERVA`. One catalog per **public instance or the Net registry**, not per disease-map diagram. Skip login-only lab tenants.

| Tool | Query |
|------|-------|
| Google | `"MINERVA" (pathway OR "disease map" OR SBGN) (platform OR registry) -site:github.com` |
| Censys | `web.endpoints.http.body: "MINERVA"` |
| FOFA | `body="MINERVA"` |

## Nextstrain (`nextstrain`) {#nextstrain}

Pathogen phylodynamics platform. Hub: [nextstrain.org](https://nextstrain.org). Community instances share Auspice JSON datasets.

**Confirm:** GET the public dataset catalog (`nextstrain.org` or a documented community host). One record per public Nextstrain/Auspice catalog, not per pathogen narrative page.

| Tool | Query |
|------|-------|
| Google | `"Nextstrain" (pathogen OR phylogeny OR Auspice) (dataset OR catalog)` |
| Censys | `web.endpoints.http.title: "Nextstrain"` |
| FOFA | `title="Nextstrain"` |

## Materials Cloud (`materialscloud`) {#materialscloud}

EPFL/MARVEL computational materials platform (AiiDA Explore UI). Distinct from Materials Cloud Archive, which is InvenioRDM (`inveniordm`).

**Confirm:** GET `/explore` or the Explore work-graph catalog. Do **not** retag `archive.materialscloud.org`.

| Tool | Query |
|------|-------|
| Google | `"Materials Cloud" (Explore OR AiiDA) -archive.materialscloud.org` |
| Censys | `web.endpoints.http.body: "Materials Cloud"` |
| FOFA | `body="Materials Cloud"` |

## OpenKIM (`openkim`) {#openkim}

Open Knowledgebase of Interatomic Models. Site: [openkim.org](https://openkim.org).

**Confirm:** GET the public model/test catalog. One record for the hub; skip individual potential landing pages as catalogs.

| Tool | Query |
|------|-------|
| Google | `"OpenKIM" ("interatomic" OR potential OR "force field")` |
| Censys | `web.names: "openkim.org"` |
| FOFA | `domain="openkim.org"` |

## ChecklistBank (`checklistbank`) {#checklistbank}

Catalogue of Life checklist platform. Site: [checklistbank.org](https://www.checklistbank.org). REST API at `api.checklistbank.org`.

**Confirm:** GET the dataset catalog or `/api`. One record for the hub (and any independent ChecklistBank deployments). Not GBIF IPT; not Catalogue of Life’s public website alone.

| Tool | Query |
|------|-------|
| Google | `"ChecklistBank" ("Catalogue of Life" OR taxonomy OR checklist)` |
| Censys | `web.names: "checklistbank.org"` |
| FOFA | `domain="checklistbank.org"` |

## ProteoSAFe (`proteosafe`) {#proteosafe}

UCSD CCMS mass-spectrometry catalog UI shared by GNPS and MassIVE (`/ProteoSAFe/datasets.jsp`).

**Confirm:** GET `/ProteoSAFe/datasets.jsp` or the GNPS/MassIVE dataset list. One record per public ProteoSAFe catalog (GNPS metabolomics vs MassIVE proteomics), not per dataset or workflow job.

| Tool | Query |
|------|-------|
| Google | `"ProteoSAFe" (GNPS OR MassIVE OR datasets.jsp)` |
| Censys | `web.endpoints.http.body: "ProteoSAFe"` |
| FOFA | `body="ProteoSAFe"` |

## CyVerse Data Commons (`cyverse`) {#cyverse}

CyVerse public data-publication catalog (DOI curated data and community collections). Site: [datacommons.cyverse.org](https://datacommons.cyverse.org). iRODS is storage, not the catalog id.

**Confirm:** GET the Data Commons catalog home. One record for the public Commons; skip authenticated DE workspaces and raw iRODS endpoints.

| Tool | Query |
|------|-------|
| Google | `"CyVerse" "Data Commons" (DOI OR dataset OR repository)` |
| Censys | `web.names: "datacommons.cyverse.org"` |
| FOFA | `host="datacommons.cyverse.org"` |

## Hugging Face (`huggingface`) {#huggingface}

ML dataset hub at [huggingface.co/datasets](https://huggingface.co/datasets/). One catalog for the Hub; do not add per-user spaces. Catalog type is often Machine learning catalog (`openmlorg` pattern).

**Confirm:** GET `/datasets/`. Title `Datasets – Hugging Face`.

| Tool | Query |
|------|-------|
| Google | `"Hugging Face" datasets (hub OR catalog)` |
| Censys | `web.names: "huggingface.co"` |
| FOFA | `domain="huggingface.co"` |

## OpenAlex (`openalex`) {#openalex}

OurResearch bibliographic catalog. Site: [openalex.org](https://openalex.org). Cloudflare may return 403 to bots; the registry row is the unique hub.

**Confirm:** GET the home or `https://api.openalex.org/`. Do not add per-work landing pages.

| Tool | Query |
|------|-------|
| Google | `"OpenAlex" (API OR catalog) OurResearch` |
| Censys | `web.names: "openalex.org"` |
| FOFA | `domain="openalex.org"` |

## Wikibase (`wikibase`) {#wikibase}

MediaWiki knowledge-base software. Wikidata ([wikidata.org](https://www.wikidata.org)) is the primary public catalog. Independent Wikibase instances share the Wikibase API and often a SPARQL endpoint.

**Confirm:** GET the wiki home. Title/body `Wikidata` / `Wikibase`. One record per public instance, not per entity.

| Tool | Query |
|------|-------|
| Google | `"powered by Wikibase" OR "Special:ListDatatypes" Wikibase` |
| Censys | `web.endpoints.http.body: "wikibase"` |
| FOFA | `body="wikibase"` |

## DBpedia Databus (`databus`) {#databus}

DBpedia dataset catalog/versioning bus. Site: [databus.dbpedia.org](https://databus.dbpedia.org). Distinct from the DBpedia Association WordPress homepage (`www.dbpedia.org` stays `custom`).

**Confirm:** GET Databus (OIDC login on the SPA is OK if the product is Databus). Do not retag www.dbpedia.org.

| Tool | Query |
|------|-------|
| Google | `"DBpedia Databus" (dataset OR catalog)` |
| Censys | `web.names: "databus.dbpedia.org"` |
| FOFA | `host="databus.dbpedia.org"` |

## MGnify (`mgnify`) {#mgnify}

EMBL-EBI microbiome archive (formerly EBI Metagenomics). Site: [ebi.ac.uk/metagenomics](https://www.ebi.ac.uk/metagenomics).

**Confirm:** GET `/metagenomics`. Title `MGnify`.

| Tool | Query |
|------|-------|
| Google | `"MGnify" (metagenomics OR microbiome) EBI` |
| Censys | `web.endpoints.http.title: "MGnify"` |
| FOFA | `title="MGnify"` |

## MetaboLights (`metabolights`) {#metabolights}

EMBL-EBI metabolomics study archive. Site: [ebi.ac.uk/metabolights](https://www.ebi.ac.uk/metabolights/).

**Confirm:** GET `/metabolights`. Title `MetaboLights`.

| Tool | Query |
|------|-------|
| Google | `"MetaboLights" (metabolomics OR study) EBI` |
| Censys | `web.endpoints.http.title: "MetaboLights"` |
| FOFA | `title="MetaboLights"` |

## BioStudies (`biostudies`) {#biostudies}

EMBL-EBI archive for studies that do not fit a dedicated archive. Site: [ebi.ac.uk/biostudies](https://www.ebi.ac.uk/biostudies/).

**Confirm:** GET `/biostudies`. Title `BioStudies`.

| Tool | Query |
|------|-------|
| Google | `"BioStudies" EBI (archive OR study)` |
| Censys | `web.endpoints.http.title: "BioStudies"` |
| FOFA | `title="BioStudies"` |

## Reactome (`reactome`) {#reactome}

Curated pathway knowledgebase. Site: [reactome.org](https://reactome.org).

**Confirm:** GET the home. Title `Reactome Pathway Database`.

| Tool | Query |
|------|-------|
| Google | `"Reactome" "Pathway Database"` |
| Censys | `web.names: "reactome.org"` |
| FOFA | `domain="reactome.org"` |

## WikiPathways (`wikipathways`) {#wikipathways}

Community pathway database. Site: [wikipathways.org](https://www.wikipathways.org).

**Confirm:** GET the home. Title `WikiPathways`.

| Tool | Query |
|------|-------|
| Google | `"WikiPathways" (pathway OR GPML)` |
| Censys | `web.names: "wikipathways.org"` |
| FOFA | `domain="wikipathways.org"` |

## UCSC Genome Browser (`ucscgenomebrowser`) {#ucscgenomebrowser}

UCSC genome annotation catalog and viewer. Site: [genome.ucsc.edu](https://genome.ucsc.edu).

**Confirm:** GET the home. Title `UCSC Genome Browser`. One record for the public browser, not per assembly hub unless it is an independent catalog.

| Tool | Query |
|------|-------|
| Google | `"UCSC Genome Browser" (hub OR downloads)` |
| Censys | `web.names: "genome.ucsc.edu"` |
| FOFA | `host="genome.ucsc.edu"` |

## FlyBase (`flybase`) {#flybase}

Drosophila model-organism knowledgebase. Site: [flybase.org](https://flybase.org). CloudFront may return 403 to bots; the registry row is the unique hub.

**Confirm:** GET flybase.org when reachable. Do not add per-gene pages.

| Tool | Query |
|------|-------|
| Google | `"FlyBase" Drosophila (database OR genome)` |
| Censys | `web.names: "flybase.org"` |
| FOFA | `domain="flybase.org"` |

## WormBase (`wormbase`) {#wormbase}

C. elegans / nematode knowledgebase. Site: [wormbase.org](https://wormbase.org). Cloudflare may return 403 to bots.

**Confirm:** GET wormbase.org when reachable. Do not add per-gene pages.

| Tool | Query |
|------|-------|
| Google | `"WormBase" "C. elegans" (database OR genome)` |
| Censys | `web.names: "wormbase.org"` |
| FOFA | `domain="wormbase.org"` |

## iDigBio (`idigbio`) {#idigbio}

US digitized biodiversity-collections portal. Public catalog: [portal.idigbio.org](https://portal.idigbio.org/). Distinct from the iDigBio IPT (`ipt`).

**Confirm:** GET the Portal (www.idigbio.org currently redirects). Title `iDigBio Portal`.

| Tool | Query |
|------|-------|
| Google | `"iDigBio Portal" (specimen OR collections)` |
| Censys | `web.names: "portal.idigbio.org"` |
| FOFA | `host="portal.idigbio.org"` |

## iNaturalist (`inaturalist`) {#inaturalist}

Open-source citizen-science observation platform. Site: [inaturalist.org](https://www.inaturalist.org). Register the hub (and documented independent iNaturalist Network nodes), not per-user feeds.

**Confirm:** GET the home. Title includes `iNaturalist`. API `api.inaturalist.org/v1`.

| Tool | Query |
|------|-------|
| Google | `"iNaturalist" (API OR "open source") -site:inaturalist.org` |
| Censys | `web.names: "inaturalist.org"` |
| FOFA | `domain="inaturalist.org"` |

## Related

- [discovery-scientific.md](discovery-scientific.md)
- [discovery.md](discovery.md)
- [discovery-search-tools.md](discovery-search-tools.md)
- [harvest-scientific-domain.md](harvest-scientific-domain.md)
- [harvest-biodiversity.md](harvest-biodiversity.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [software-index.md](software-index.md)
