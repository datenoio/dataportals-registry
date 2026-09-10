# Discovering scientific data repositories

How to find **scientific data repository** installations (`catalog_type: Scientific data repository`). Search-engine syntax (Google, Censys, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). Cross-check [re3data](https://www.re3data.org/), the [OpenAIRE Graph data sources](openaire-sync.md) dump, and the Dataverse installations JSON before adding a well-known platform — many are already registered.

Do not add dataset-level records (a single Dataverse dataset, a Zenodo deposition, a STAC item).

| Page | Use when |
|------|----------|
| This page | Institutional repositories and CRIS (Dataverse, DSpace, Invenio, EPrints, OPUS, RADAR, Yoda, Hyrax, Figshare, Redivis, Pure, Converis, Omega-PSIR, Archipelago, DABAR, OpenScience.si, LabKey, Synapse, XNAT, OMERO, Kadi4Mat, e!DAL, NOMAD, DiVA Portal, META-SHARE, Gen3, …) |
| [Domain repositories](discovery-scientific-domain.md) | IPT, Symbiota, THREDDS, ERDDAP, Breedbase, Tripal, VEuPathDB, MassBank, ioChem-BD, ESGF, ALA, BirdMap Africa, SciCat, CLLD, Pathway Tools, IBDC |

All `software.id` values: [software-index.md](software-index.md). Harvest filters: [harvest-scientific.md](harvest-scientific.md), [harvest-scientific-domain.md](harvest-scientific-domain.md).

## Dataverse (`dataverse`) {#dataverse}

Installations JSON: [dataverse-installations data.json](https://iqss.github.io/dataverse-installations/data/data.json). Branding is often ``{Org} Dataverse``.

**Confirm:** `https://host/api/info/version` and/or `/api/search?q=*&type=dataset`. OAI-PMH: `/oai?verb=Identify`.

| Tool | Query |
|------|-------|
| Google | `"Dataverse" "Harvard" OR "IQSS" -site:harvard.edu` (then drop Harvard to find others) |
| Google | `inurl:/dataverse.xhtml OR inurl:/dataverse/` |
| Google | `"API" "info/version" dataverse` |
| Censys | `web.endpoints.http.html_title: "Dataverse"` |
| FOFA | `title="Dataverse"` |
| Censys | `web.endpoints.http.body: "dataverse"` |
| FOFA | `body="dataverse"` |
| Shodan | `http.title:"Dataverse"` |
| crt.sh | `dataverse.%` |

**False positives:** guides.dataverse.org, the Harvard demo, individual dataset landing pages (`/dataset.xhtml?persistentId=`). Register the installation root. Local brands without “Dataverse” in the HTML title still count when `/api/info/version` returns Dataverse JSON (Aleia, Deposita Dados, Repo4Cat; GlobeData reports 6.10.1). A 403 `{"message":"API is disabled"}` on `/api/info/version` is **not** enough when the public UI is Omeka Classic (`/items/browse`, “Canal de RSS Omeka”). A homepage title “Welcome to Data Repository” without `/api/info/version`, `/api/search`, `/oai`, or `/dataverse.xhtml` stays `custom` (`datarepository.stat.unipd.it`).

## DSpace (`dspace`) {#dspace}

Institutional repositories. DSpace 7+ API at `/server/api` even when the public URL has no `/xmlui` or `/jspui` (University of Ostrava EDUO reports DSpace 7.6; UNESP reports DSpace 10.0; BAW HENRY reports DSpace 7.5; Rice Research Repository reports DSpace 9.3; UNCo RDI reports DSpace 8.4; uBibliorum reports DSpace 7.6.1). Older 5.x/6.x: `/rest/items`, XMLUI/JSPUI, or `meta name="generator" content="DSpace 5.x"` / `DSpace 6.x` (AERADE Cranfield is 5.10; Universitas Medan Area is 6.3). OAI-PMH: `/oai/request?verb=Identify`.

| Tool | Query |
|------|-------|
| Google | `"DSpace" (repository OR "handle") site:.edu` |
| Google | `inurl:/xmlui OR inurl:/jspui "DSpace"` |
| Google | `inurl:/server/api/discover/search/objects` |
| Censys | `web.endpoints.http.body: "DSpace"` |
| FOFA | `body="DSpace"` |
| Shodan | `http.html:"generator\" content=\"DSpace"` |

ROAR ([roar.eprints.org](http://roar.eprints.org)) lists many DSpace hosts; still duplicate-check this registry. Harvest type filters: [harvest-scientific.md](harvest-scientific.md#dspace).

## DSpace-CRIS (`dspacecris`) {#dspacecris}

Set `dspacecris` only when the UI is DSpace-CRIS (researcher profiles, CRIS entities), not vanilla DSpace. `meta name="Generator" content="DSpace CRIS-…"` (HCU Hamburg repOS) is enough. Same OAI/REST probes as [DSpace](#dspace).

| Tool | Query |
|------|-------|
| Google | `"DSpace-CRIS" OR "dspace-cris"` |
| Censys | `web.endpoints.http.body: "DSpace CRIS"` |
| FOFA | `body="DSpace CRIS"` |

## Invenio (`invenio`) {#invenio}

Classic Invenio (not RDM). **Confirm:** `/api/records?size=1` JSON and Invenio branding without InvenioRDM (`generator` Invenio only, as on eLTER DAR), **or** JOIN2 Invenio 1.x (`join2-wiki.gsi.de` credit, `/oai2d`) when `/api/records` 404s (RWTH Publications). Do **not** set `eprints` from an OAI Identify that only mentions the word EPrints without an `eprints` xmlns. OAI-PMH often `/oai2d`.

Use `inveniordm` when the product is InvenioRDM. Skip zenodo.org itself if already registered.

| Tool | Query |
|------|-------|
| Google | `inurl:/api/records "invenio" -InvenioRDM` |
| Censys | `web.endpoints.http.body: "invenio"` |
| FOFA | `body="invenio"` |

## InvenioRDM (`inveniordm`) {#inveniordm}

Zenodo-like research data repositories. **Confirm:** `/api/records?size=1` JSON plus InvenioRDM / `invenio-rdm` branding, or `meta generator` `InvenioRDM` (GALENOS reports InvenioRDM 12.0; Knowledge@UChicago reports 13.1). `generator` Invenio **without** that branding is [classic Invenio](#invenio). OAI-PMH often `/oai2d`. Look for **institutional** RDM instances. Do **not** set `inveniordm` on a Metadata catalog (`nma.eosc.cz`): allowed types are Scientific data repository and General research repository only.

| Tool | Query |
|------|-------|
| Google | `"InvenioRDM" OR "invenio-rdm" repository` |
| Google | `inurl:/api/records "invenio"` |
| Censys | `web.endpoints.http.body: "invenio"` |
| FOFA | `body="invenio"` |

## EPrints (`eprints`) {#eprints}

**Confirm:** `/eprint` URLs, “Powered by EPrints”, `meta generator` EPrints (Warwick WRAP and UAL Research Online are EPrints 3.4.5; UNAM IIEc is 3.3.16; UCL Discovery is 3.4.3; NERC Open Research Archive, LSE Research Online, and LSHTM Research Online are 3.4.6), or OAI-PMH Identify with an `eprints` xmlns (`/cgi/oai2` or `/oai`; PTB uses `/oai`). Directory: [ROAR](http://roar.eprints.org). Do **not** set `eprints` from a Digital Commons `/do/oai/` Identify that only lists an `eprints` metadata prefix.

| Tool | Query |
|------|-------|
| Google | `"Powered by EPrints" -site:eprints.org` |
| Google | `inurl:/cgi/oai2 eprints` |
| Censys | `web.endpoints.http.body: "EPrints"` |
| FOFA | `body="EPrints"` |

## DiVA Portal (`divaportal`) {#divaportal}

Swedish shared IR (Uppsala University Library). Tenants at `{org}.diva-portal.org` with a JSF smash search UI. Hub: [diva-portal.org](https://www.diva-portal.org). Distinct from **DIVA-GIS** species downloads.

**Signals:** hostname `*.diva-portal.org`; path `/smash/`; WildFly / PrimeFaces; branding DiVA.

**Confirm:** GET `/smash/` search. One record per organisational tenant (and the hub). Filter harvest to research data — publications dominate.

| Tool | Query |
|------|-------|
| Google | `site:diva-portal.org` |
| Google | `"DiVA" (repository OR "research data") site:.se` |
| Censys | `web.names: "diva-portal.org"` |
| FOFA | `domain="diva-portal.org"` |
| crt.sh | `%.diva-portal.org` |

## Samvera Hyrax (`hyrax`) {#hyrax}

Rails institutional repo. **Confirm:** `/catalog.json` or Blacklight `/catalog`. Branding “Hyrax”, “Samvera”, “Nurax”.

Hyrax (and Islandora, PHAIDRA) often sit on **Fedora Repository** as the preservation backend. Set `software.id` from the **public catalog UI**, not the storage layer. Use `fedora` only when Fedora’s REST/LDP API is the public product — see [Fedora](#fedora).

| Tool | Query |
|------|-------|
| Google | `"Hyrax" (repository OR "research data") site:.edu` |
| Google | `"Powered by Hyrax" OR "Samvera"` |
| Censys | `web.endpoints.http.body: "hyrax"` |
| FOFA | `body="hyrax"` |

## Figshare (`figshare`) {#figshare}

Institutional Figshare (not figshare.com itself). **Signals:** `{org}.figshare.com` or a custom domain with Figshare UI.

Do **not** set `figshare` on a library CMS or GitHub Pages hub that only links an already-tagged `{org}.figshare.com` catalog (University of Arizona ReDATA → `arizona.figshare.com`).

| Tool | Query |
|------|-------|
| Google | `site:figshare.com -site:figshare.com/articles "{university}"` |
| Google | `"figshare" "institutional repository"` |
| crt.sh | `%.figshare.com` |
| Censys | `web.names: "figshare.com"` |
| FOFA | `domain="figshare.com"` |

Register the **institution** instance, not individual article URLs.

## MyCoRe (`mycore`) {#mycore}

German institutional repos. List: [mycore.de applications](https://www.mycore.de/site/applications/list/).

| Tool | Query |
|------|-------|
| Google | `"MyCoRe" (repositorium OR repository) site:.de` |
| Censys | `web.endpoints.http.body: "MyCoRe"` |
| FOFA | `body="MyCoRe"` |

## OPUS (`opus`) {#opus}

German (and some Austrian) institutional repositories. Official instance list: [KOBV OPUS 4 references](https://www.kobv.de/entwicklung/software/opus-4/referenzen/). Many hosts share `opus4.kobv.de` or `opus.bsz-bw.de` with a per-institution path.

Prefer instances that publish research data (`doc-type:ResearchData` in OAI-PMH `ListSets`, or a Forschungsdaten collection), not thesis-only publication servers.

**Confirm:** `{base}/oai?verb=Identify` and `{base}/oai?verb=ListSets` (replace `{base}` with the repository root). Search UI often under `/solrsearch/` or `/home`. `meta name="Opus-Version"` plus Identify `repositoryName` `Opus4 … Instance` is enough on an already-registered scientific IR (BBAW edoc 4.8.0.19) even when ListSets has no `doc-type:ResearchData`.

| Tool | Query |
|------|-------|
| Google | `"OPUS 4" (Forschungsdaten OR "research data" OR Repositorium) site:.de` |
| Google | `inurl:opus4.kobv.de OR inurl:opus.bsz-bw.de` |
| Censys | `web.endpoints.http.body: "OPUS 4"` |
| FOFA | `body="OPUS 4"` |

Skip intranet-only thesis portals (Hochschulnetz / account required). Register the repository root, not a single document frontdoor.

## RADAR (`radar`) {#radar}

FIZ Karlsruhe research data repositories (RADAR Cloud and RADAR Local). Official instance notes: [About RADAR](https://radar.products.fiz-karlsruhe.de/en/radarabout/ueber-radar). re3data lists them under software **RADAR**.

**Confirm:** `{base}/radar/en/home` or `{base}/radar/de/home` titled RADAR / the local brand, `{base}/oai/OAIHandler?verb=Identify`, and `{base}/radar/api/datasets` JSON with `totalHits` > 0. Prefer instances that already publish datasets. Use `software.id: radar`.

Register distinct **Local** hosts (KonDATA, WueData, Datathek, FoDaSi, OstData, RADAR-BB). Do **not** add `radar.kit.edu` or NFDI branded subdomains (`radar4chem.radar-service.eu`, `radar4culture.radar-service.eu`, `radar4memory.radar-service.eu`) — those share the already-registered Cloud catalog at `www.radar-service.eu`.

| Tool | Query |
|------|-------|
| Google | `"RADAR" (Forschungsdaten OR "research data") (repositorium OR repository) site:.de` |
| Google | `inurl:/radar/de/home OR inurl:/radar/en/home` |
| Censys | `web.endpoints.http.html_title: "Forschungsdaten"` plus RADAR body hints |
| FOFA | `title="Forschungsdaten" && body="RADAR"` |
| re3data | software filter **RADAR** |

Skip the FIZ product/marketing site (`radar.products.fiz-karlsruhe.de`) and dataset landing pages (`/radar/de/dataset/{id}`).

## Redivis (`redivis`) {#redivis}

Hosted research-data platform ([redivis.com](https://redivis.com)). Academic orgs get `{org}.redivis.com` workspaces (Stanford Data Farm, AIMI, and similar). **Signals:** title “Redivis” or “Data Farm”, scripts from `redivis.com/static/`, JSON-LD `Organization`, OpenAPI at `/api/v1/openapi.json`.

**Confirm:** `GET https://host/api/v1/openapi.json` titled Redivis API. Use `software.id: redivis`.

| Tool | Query |
|------|-------|
| Google | `"powered by Redivis" OR "Redivis" ("data farm" OR datasets) site:.edu` |
| Google | `site:redivis.com -site:docs.redivis.com` |
| Censys | `web.endpoints.http.body: "redivis.com/static"` |
| FOFA | `body="redivis.com/static"` |
| crt.sh | `%.redivis.com` |

Register the **organization root** (`https://stanford.redivis.com`), not a nested dataset URL and not every `/ORG/datasets` collection. Skip `docs.redivis.com` and individual dataset pages.

## Yoda (`yoda`) {#yoda}

Dutch research-data management platform (Utrecht University / Yoda Consortium, often hosted by SURF) on iRODS. Docs: [utrechtuniversity.github.io/yoda](https://utrechtuniversity.github.io/yoda/). Public catalogs are institutional **publication landings** (DataCite-indexed datasets), not the authenticated vault.

**Confirm:** a public dataset landing or portal titled Yoda / Your Data for that institution. Hostnames often `public.yoda.*`, `portal.yoda.*`, or `*-landing.irods.surfsara.nl`. Use `software.id: yoda`. Skip login-only workspaces and SURF marketing pages.

| Tool | Query |
|------|-------|
| Google | `"Yoda" ("research data" OR "data publication") (university OR SURF) site:.nl` |
| Google | `inurl:yoda. "data" (portal OR public)` |
| Censys | `web.names: "yoda."` |
| FOFA | `host="yoda."` |

Register one catalog per **institution** public landing. Do not add every DataCite DOI.

## DLCM (`dlcm`) {#dlcm}

swissuniversities OAIS research-data platform (University of Geneva). Product: [dlcm.ch](https://dlcm.ch/). Public tenants use an Angular catalog UI; OAI-PMH lives on the access module (`/oai-info/oai-provider/oai`). Use `software.id: dlcm`. Yareta is in-scope. Do **not** set `dlcm` on `olos.swiss` (WordPress marketing homepage). The former `access.olos.swiss` consultation portal is inactive.

**Confirm:** GET the catalog home (title often `Yareta`) and `https://access.{host}/oai-info/oai-provider/oai?verb=Identify`. Skip `/dlcm-oai/oai` 404s and login-only `/access/oai-provider/oai`.

| Tool | Query |
|------|-------|
| Google | `"Yareta" (research data OR dépôt) site:.ch` |
| Google | `"DLCM" ("research data" OR OAIS) (portal OR repository)` |
| Censys | `web.endpoints.http.body: "Yareta"` |
| FOFA | `body="Yareta"` |

Register one catalog per public tenant. Do not add the product marketing site as a second catalog.

## easydb (`easydb`) {#easydb}

Programmfabrik collection and research-data catalog (easydb 5; fylr is the successor). Product: [programmfabrik.de](https://www.programmfabrik.de/). Use `software.id: easydb` for both. HilData and heidICON are in-scope.

**Confirm:** HTML title `easydb 5`, comment `fylr_inject`, and/or `window.easydb_base_prefix`. Optional: `/api/v1/session` JSON with `"method": "easydb"`. The session endpoint is not a dataset list — keep `api: false` unless a public object-search API is confirmed. Skip vendor demos and login-only collections.

| Tool | Query |
|------|-------|
| Google | `"easydb 5" (repository OR collection OR Forschungsdaten)` |
| Google | `"heidICON" OR "HilData" easydb` |
| Censys | `web.endpoints.http.body: "fylr_inject"` |
| FOFA | `body="fylr_inject"` |

Register one catalog per institutional tenant, not per collection folder.

## CONTENTdm (`contentdm`) {#contentdm}

OCLC hosted digital collections. Hosts are often `*.contentdm.oclc.org`. Docs: [OCLC CONTENTdm](https://help.oclc.org/Metadata_Services/CONTENTdm).

Register a CONTENTdm site only when it publishes **research datasets, statistical series, or a data collection**, not a photo/manuscript exhibit with no dataset catalog. Stats NZ Digital Library and climate-data collections are in scope; typical campus image libraries are not (Claremont CCDL `/digital/` title `CONTENTdm` stays `custom`). The same dataset-catalog test applies to Goobi viewer / Intranda digital libraries (`digi.landesbibliothek.at`, `gei-digital.gei.de`): heritage book and textbook viewers stay `custom` (no `goobi` software id).

**Confirm:** `https://host/digital/api/collections` and/or `/oai/oai.php?verb=Identify`. Website API: `/digital/bl/dmwebservices/index.php?q=dmGetCollectionList/json`.

| Tool | Query |
|------|-------|
| Google | `site:contentdm.oclc.org (dataset OR "research data" OR statistics OR climate)` |
| Google | `"CONTENTdm" ("digital collections" OR dataset) -site:oclc.org` |
| Censys | `web.names: "contentdm.oclc.org"` |
| FOFA | `host="contentdm.oclc.org"` |
| crt.sh | `%.contentdm.oclc.org` |

Register the collection or library root that lists datasets, not a single item URL.

## Omeka S (`omekas`) {#omekas}

Cultural-heritage and research publishing platform. JSON-LD REST API; modules include Linked Data Sets and OAI-PMH Repository. Docs: [omeka.org/s](https://omeka.org/s).

Set `omekas` when the public product is a **dataset catalog** (schema.org DataCatalog, SPARQL, or a datasets/items API), not an exhibit-only museum site.

**Confirm:** `https://host/api` or `/api/items` returns JSON-LD. Optional: `/.well-known/datacatalog`, `/oai`.

| Tool | Query |
|------|-------|
| Google | `"Omeka S" (dataset OR datacatalog OR SPARQL OR "linked open data") -site:omeka.org` |
| Google | `inurl:/api/items omeka` |
| Censys | `web.endpoints.http.body: "Omeka S"` |
| FOFA | `body="Omeka S"` |
| Censys | `web.endpoints.http.body: "o:item"` |
| FOFA | `body="o:item"` |

Omeka Classic is a different product — do not label it `omekas` without the S API (`/api` JSON-LD). UBA Sociales (`repositorio.sociales.uba.ar`) is Classic (`/items/browse`); leave it `custom`.

## Fedora Repository (`fedora`) {#fedora}

Preservation repository with a Linked Data Platform REST API. Public catalogs usually wrap it with Hyrax, Islandora, or PHAIDRA.

**Confirm:** `GET https://host/fcrepo/rest` or `/rest` with Fedora version headers or RDF. Use `fedora` only if that API (or a thin Fedora HTML) is what users treat as the catalog.

| Tool | Query |
|------|-------|
| Google | `"Fedora Repository" OR inurl:/fcrepo/rest (research OR dataset)` |
| Google | `"fcrepo" "research data" -site:github.com` |
| Censys | `web.endpoints.http.body: "Fedora Repository"` |
| FOFA | `body="Fedora Repository"` |

Prefer `hyrax`, `islandora`, or `phaidra` when those UIs are the public product on the same host.

## PHAIDRA (`phaidra`) {#phaidra}

University of Vienna institutional repository (and clones). List and docs: [phaidra.org](https://phaidra.org). OAI-PMH and REST search are common.

**Confirm:** `/api/oai?verb=Identify` or `/api/search/select`. Hostnames often `phaidra.{university}`.

| Tool | Query |
|------|-------|
| Google | `"PHAIDRA" (repository OR Forschungsdaten OR "research data") -site:univie.ac.at` |
| Google | `inurl:phaidra (oai OR repository)` |
| Censys | `web.endpoints.http.body: "PHAIDRA"` |
| FOFA | `body="PHAIDRA"` |

## Elsevier Pure (`pure`) {#pure}

CRIS / research portal. Showcase: [Pure in action](https://www.elsevier.com/solutions/pure/pure-in-action). Portal paths often `/portal` or `/en/`.

**Confirm:** GET the public datasets/research portal and match “Powered by Elsevier Pure” / “Angetrieben von Pure” (Lancaster `?en/datasets/search.html`; WU Vienna Research). Skip marketing pages. The public research **portal** is the catalog, not the admin Pure backend.

| Tool | Query |
|------|-------|
| Google | `"Pure" "research portal" Elsevier OR "pure.elsevier"` |
| Google | `inurl:/portal/en/ persons datasets` |
| Censys | `web.endpoints.http.body: "Elsevier Pure"` |
| FOFA | `body="Elsevier Pure"` |

Skip marketing pages. The public research **portal** is the catalog, not the admin Pure backend.

## Esploro (`esploro`) {#esploro}

Clarivate / Ex Libris research information management and repository. Vendor: [Esploro](https://exlibrisgroup.com/products/esploro-research-services-platform/). Hosts often `*.esploro.exlibrisgroup.com` or a campus custom domain with `/esploro` or research-outputs views. Surrey Research Insight redirected from `epubs.surrey.ac.uk` to `openresearch.surrey.ac.uk/esploro/` (`<base href="/esploro/"/>`). A `202` empty body on a successor host (Manchester Met `repository.mmu.ac.uk`) is not enough.

Register the institutional research portal that lists datasets, not a single output URL. Skip Ex Libris marketing pages.

| Tool | Query |
|------|-------|
| Google | `"Esploro" ("research portal" OR "research outputs" OR datasets) -site:exlibrisgroup.com` |
| Google | `site:esploro.exlibrisgroup.com` |
| Censys | `web.names: "esploro.exlibrisgroup.com"` |
| FOFA | `host="esploro.exlibrisgroup.com"` |
| crt.sh | `%.esploro.exlibrisgroup.com` |

## Elsevier Digital Commons (`elsevierdigitalcommons`) {#elsevierdigitalcommons}

Hosted institutional repository (bepress / Elsevier). Hosts often `*.bepress.com`, `digitalcommons.` plus a campus domain, or `dc.` plus a campus host.

**Signals:** Digital Commons branding; `/do/oai/` or bepress OAI; article/dataset collections.

**Confirm:** GET the IR home and OAI Identify when public. Register the repository root, not a single series. Skip exhibit-only faculty profile sites with no dataset or research-output catalog. Live Digital Commons chrome (`dc-responsive-nav.js`, bepress assets) is enough (RIT Digital Institutional Repository; SJSU ScholarWorks).

| Tool | Query |
|------|-------|
| Google | `"Digital Commons" (bepress OR Elsevier) (datasets OR repository) -site:elsevier.com` |
| Google | `site:bepress.com OR inurl:digitalcommons` |
| Censys | `web.endpoints.http.body: "bepress"` |
| FOFA | `body="bepress"` |
| crt.sh | `%.bepress.com` |

## InstDB (`instdb`) {#instdb}

FairStack institutional research-data repository (CAS / CNIC). Site: [fairstack.cn](https://fairstack.cn/product/software/InstDB).

**Signals:** InstDB / FairStack branding; Chinese Academy of Sciences data-center portals; DOI/CSTR assignment UI.

**Confirm:** GET the public catalog home. One record per institutional node, not per dataset.

| Tool | Query |
|------|-------|
| Google | `"InstDB" OR "FairStack" (数据仓储 OR repository) -site:fairstack.cn` |
| Censys | `web.endpoints.http.body: "InstDB"` |
| FOFA | `body="InstDB"` |

## DABAR (`dabar`) {#dabar}

Croatia’s national multi-tenant IR, operated by SRCE. Site: [dabar.srce.hr](https://dabar.srce.hr). Tenant list (bot-blocked from some clients): [browse/repository](https://dabar.srce.hr/browse/repository). Production moved off Drupal+Islandora to Laravel + Fedora in November 2025.

**Signals:** hostname `repozitorij.{org}.hr` or `*.unizg.hr` / `*.unist.hr` / `*.unizd.hr` faculty repos; national ETD hosts `zir.nsk.hr` and `dr.nsk.hr`; hub `dabar.srce.hr`; HTML title “Dabar” / “Repozitorij”; OAI-PMH `/oai/?verb=Identify` or `/oai?verb=Identify`.

**Confirm:** GET the public repository home (not a single thesis). One catalog per **institutional hostname**. Do not add each `?ns=` namespace on the hub as its own catalog — those are facets of `dabar.srce.hr`. Do not label tenants `islandora`.

| Tool | Query |
|------|-------|
| Google | `"Digitalni akademski arhivi" OR DABAR (repozitorij OR repository) site:.hr -site:github.com` |
| Google | `inurl:repozitorij (unizg.hr OR srce.hr OR nsk.hr)` |
| Censys | `web.endpoints.http.body: "Dabar"` |
| FOFA | `body="Dabar"` |
| Censys | `web.names: "dabar.srce.hr"` |
| FOFA | `host="dabar.srce.hr"` |

## OpenScience.si repository (`opensciencesi`) {#opensciencesi}

Shared Slovenian IR stack (University of Maribor FERI) used by DKUM, RUL, RUP, RUNG, ReVIS, and DiRROS. National portal: [openscience.si](https://www.openscience.si). Not DSpace, EPrints, or Fedora.

**Signals:** path `/oai/oai2.php`; `/info/index.php/eng/policies`; “OpenScience.si” / DKUM / DiRROS chrome; hosts `dk.um.si`, `repozitorij.uni-lj.si`, `repozitorij.upr.si`, `repozitorij.ung.si`, `*.openscience.si`.

**Confirm:** GET the public repository home and `/oai/oai2.php?verb=Identify` (some tenants use `/oai/?verb=Identify`). One catalog per university or research-organisation tenant. Keep `www.openscience.si` as the national **aggregator** (`custom`), not a seventh install of the IR software.

| Tool | Query |
|------|-------|
| Google | `"OpenScience.si" (repozitorij OR repository OR DiRROS OR DKUM) site:.si` |
| Google | `inurl:/oai/oai2.php (dk.um.si OR repozitorij)` |
| Censys | `web.endpoints.http.body: "OpenScience.si"` |
| FOFA | `body="OpenScience.si"` |

## WEKO3 (`weko3`) {#weko3}

NII / RCOS open-source institutional repository. Docs: [weko3.readthedocs.io](https://weko3.readthedocs.io).

**Signals:** WEKO3 / WEKO branding; Invenio-like item types; `/api/records/` search; JAIRO Cloud hosts `*.repo.nii.ac.jp` and `*.ecats-library.jp`; older WEKO paths `/repo/{name}/all/` and `/da/`.

**Confirm:** GET the repository home. Prefer `/api/records/` on WEKO3/JAIRO Cloud. `/oai?verb=Identify` is often missing. Register the IR root, not a single item.

| Tool | Query |
|------|-------|
| Google | `"WEKO3" OR "WEKO 3" (repository OR 機関リポジトリ) -site:github.com` |
| Censys | `web.endpoints.http.body: "WEKO3"` |
| FOFA | `body="WEKO3"` |

## Omega-PSIR (`omegapsir`) {#omegapsir}

Polish university CRIS + repository. Site: [omegapsir.io](https://www.omegapsir.io).

**Signals:** Omega-PSIR / “Baza Wiedzy”; researcher profiles plus research-data records.

**Confirm:** GET the public CRIS/repository home. One record per university instance.

| Tool | Query |
|------|-------|
| Google | `"Omega-PSIR" OR "Baza Wiedzy" (repozytorium OR CRIS) site:.pl` |
| Censys | `web.endpoints.http.body: "Omega-PSIR"` |
| FOFA | `body="Omega-PSIR"` |

## Converis (`converis`) {#converis}

Clarivate Converis CRIS. Same publication-vs-data problem as Pure: the public product is often researcher profiles and publications.

**Signals:** Converis branding; Clarivate research information; `/converis/` or a campus CRIS titled Converis.

**Confirm:** GET the public CRIS home and a **datasets / research data** listing if present. One record per university instance. Skip login-only `/ws` APIs and marketing pages.

| Tool | Query |
|------|-------|
| Google | `"Converis" (research OR repository OR "research data" OR CRIS) -site:clarivate.com` |
| Censys | `web.endpoints.http.body: "Converis"` |
| FOFA | `body="Converis"` |

## Islandora (`islandora`) {#islandora}

Public Drupal + Fedora repository UI. Prefer `islandora` over `fedora` when users see an Islandora collection browser (not a generic Drupal site).

| Tool | Query |
|------|-------|
| Google | `"Islandora" (repository OR collections) -site:github.com` |
| Censys | `web.endpoints.http.body: "Islandora"` |
| FOFA | `body="Islandora" && body="islandora"` |

## Archipelago Commons (`archipelago`) {#archipelago}

Drupal digital-objects repository (Strawberryfield JSON ADOs), not Islandora. Official instance list: [Archipelagos in the Wild](https://docs.archipelago.nyc/1.6.0/inthewild/). Prefer `archipelago` over `drupal` when `/do/{uuid}` objects and Solr `/search?search_api_fulltext=` are the catalog.

**Confirm:** public `/search` (or `/do/` object pages) plus strawberryfield / Cantaloupe / “indexed Digital Objects”. Keep catalogs that include **Dataset** ADOs or structured scientific accessions (germplasm, isolate records). Skip METRO playgrounds, finding-aid-only sites, web-archive demos, and login-only tenants.

| Tool | Query |
|------|-------|
| Google | `"Archipelago Commons" OR "indexed Digital Objects" OR strawberryfield (repository OR collections) -site:github.com -site:docs.archipelago.nyc` |
| Censys | `web.endpoints.http.body: "strawberryfield"` |
| FOFA | `body="strawberryfield"` |

## Samvera (`samvera`) {#samvera}

Samvera collection UI without Hyrax branding. Use [Hyrax](#hyrax) when that is the branded product. Prefer these IDs over `fedora`. **Confirm:** `/catalog` JSON.

| Tool | Query |
|------|-------|
| Google | `"Samvera" (repository OR "research data") -site:samvera.org` |
| Censys | `web.endpoints.http.body: "Samvera"` |
| FOFA | `body="Samvera"` |

## Haplo (`haplo`) {#haplo}

Research information / repository platform. Site: [haplo.com](https://www.haplo.com).

**Confirm:** GET the public research-outputs or dataset catalog (not a staff-only CRIS). Skip haplo.com marketing.

| Tool | Query |
|------|-------|
| Google | `"Haplo" (repository OR "research outputs" OR "research data") -site:haplo.com` |
| Censys | `web.endpoints.http.body: "haplo"` |
| FOFA | `body="haplo"` |

## Worktribe (`worktribe`) {#worktribe}

University research hub. Site: [worktribe.com](https://worktribe.com).

**Confirm:** GET a public repository or research-data listing. Skip grant-admin-only tenants.

| Tool | Query |
|------|-------|
| Google | `"Worktribe" (repository OR "research data") -site:worktribe.com` |
| Censys | `web.endpoints.http.body: "worktribe"` |
| FOFA | `body="worktribe"` |

## FAIRDOM-SEEK (`seek`) {#seek}

Catalog for datasets, models, SOPs, and workflows. Site: [seek4science.org](https://seek4science.org). Includes WorkflowHub / FAIRDOMHub-style Rails apps.

**Confirm:** GET the public SEEK home or `/investigations` listing. JSON API is a plus. Do not add a single assay page.

| Tool | Query |
|------|-------|
| Google | `"FAIRDOM-SEEK" OR "FAIRDOMHub" OR WorkflowHub (datasets OR catalog)` |
| Censys | `web.endpoints.http.body: "fairdom"` |
| FOFA | `body="fairdom"` |

## RAMADDA (`ramadda`) {#ramadda}

Repository for Archiving, Managing and Accessing Diverse Data. Site: [ramadda.org](https://www.ramadda.org).

**Confirm:** GET the repository entry page (folder/catalog UI). Skip a single file download.

| Tool | Query |
|------|-------|
| Google | `"RAMADDA" (repository OR catalog OR "data portal") -site:github.com` |
| Censys | `web.endpoints.http.body: "RAMADDA"` |
| FOFA | `body="RAMADDA"` |

## META-SHARE (`metashare`) {#metashare}

META-NET language-resource repository nodes. Site: [meta-net.eu/meta-share](https://www.meta-net.eu/meta-share). Hosts are often `metashare.{org}`.

**Signals:** title “META-SHARE”; resource browse/search for corpora, lexica, and tools; META-NET branding.

**Confirm:** GET the public repository home (resource search). One catalog per **node**, not per language resource. Skip Victoria MetaShare (that is GeoNetwork). Do not add a single corpus landing page.

| Tool | Query |
|------|-------|
| Google | `"META-SHARE" (corpus OR "language resource" OR repository) -site:github.com` |
| Google | `inurl:metashare (repository OR resources)` |
| Censys | `web.endpoints.http.body: "META-SHARE"` |
| FOFA | `body="META-SHARE"` |
| crt.sh | `metashare.%` |

## LabKey Server (`labkey`) {#labkey}

LabKey Server study/assay platform. Site: [labkey.com](https://www.labkey.com). Public projects such as Panorama Public use `begin.view` folders.

**Confirm:** GET a public project home or `begin.view`. One record per public LabKey instance. Skip login-only folders and a single assay run.

| Tool | Query |
|------|-------|
| Google | `"LabKey Server" OR "LabKey" (Panorama OR "begin.view" OR study) -site:labkey.com -site:github.com` |
| Censys | `web.endpoints.http.body: "LabKey"` |
| FOFA | `body="LabKey"` |

## Synapse (`synapse`) {#synapse}

Sage Bionetworks hosted biomedical sharing platform. Site: [synapse.org](https://www.synapse.org). Disease portals (AD Knowledge Portal, NF Data Portal) are Synapse tenants.

**Confirm:** GET the public project/dataset catalog. One record per public portal or the main Synapse catalog. Skip a single file entity (`syn########` download).

| Tool | Query |
|------|-------|
| Google | `"Synapse" "Sage Bionetworks" (portal OR datasets) -site:github.com` |
| Censys | `web.endpoints.http.body: "Sage Bionetworks"` |
| FOFA | `body="Sage Bionetworks"` |

## Gen3 (`gen3`) {#gen3}

University of Chicago CTDS data-commons platform. Site: [gen3.org](https://gen3.org). Docs: [docs.gen3.org](https://docs.gen3.org). Public portals share a React data-portal UI, Fence login, Indexd/DRS, and GraphQL.

**Signals:** `_status` JSON (`Feelin good!`); `/index/ga4gh/drs/v1/service-info` with Indexd; `planx` / `uc-cdis` assets; title often “Data Portal”.

**Confirm:** GET `/_status` and/or DRS `service-info`. One catalog per **commons portal**, not per study or file. Do **not** label NCI GDC, PDC, or IDC as Gen3 (different stacks). Do not label Bento UIs (ICDC and similar) as Gen3 even when Fence is used for login.

| Tool | Query |
|------|-------|
| Google | `"Gen3" ("data portal" OR "data commons") (Fence OR Indexd OR CTDS)` |
| Google | `inurl:/index/ga4gh/drs/v1/service-info` |
| Censys | `web.endpoints.http.body: "Feelin good!"` |
| FOFA | `body="Feelin good!"` |
| crt.sh | `%.midrc.org` |

## XNAT (`xnat`) {#xnat}

Neuroimaging archive platform. Site: [xnat.org](https://www.xnat.org). Independent hospital and consortium installs expose `/xnat/` or a project catalog.

**Confirm:** GET the public XNAT home or REST project list. Skip login-only archives and a single imaging session.

| Tool | Query |
|------|-------|
| Google | `"XNAT" (neuroimaging OR "imaging archive" OR repository) -site:xnat.org -site:github.com` |
| Censys | `web.endpoints.http.body: "XNAT"` |
| FOFA | `body="XNAT"` |

## Shanoir (`shanoir`) {#shanoir}

Inria Empenn neuroimaging platform (Shanoir-NG). Site: [project.inria.fr/shanoir](https://project.inria.fr/shanoir/). Independent clinical instances (Neurinfo, OFSEP) share title `Shanoir` and HTML comment `Shanoir NG`.

**Confirm:** GET the public welcome UI (`/shanoir-ng/welcome` or `/`). One record per public instance. Skip login-only hospital tenants and a single imaging study. Demo/docs hosts are out of scope.

| Tool | Query |
|------|-------|
| Google | `"Shanoir" (neuroimaging OR "imaging" OR OFSEP) (repository OR platform) -site:github.com` |
| Censys | `web.endpoints.http.title: "Shanoir"` |
| FOFA | `title="Shanoir"` |

## LORIS (`loris`) {#loris}

McGill Centre for Integrative Neuroscience longitudinal research platform. Site: [loris.ca](https://loris.ca). Public study portals use `*.loris.ca` and title `LORIS`.

**Confirm:** GET the public data portal home. One record per public study instance. Skip `demo.loris.ca` and the product marketing site.

| Tool | Query |
|------|-------|
| Google | `"LORIS" (neuroimaging OR "data portal" OR repository) (McGill OR "The Neuro") -site:github.com` |
| Censys | `web.endpoints.http.body: "LORIS"` `web.names: "loris.ca"` |
| FOFA | `body="LORIS" && domain="loris.ca"` |

## OMERO (`omero`) {#omero}

Open Microscopy Environment image repository. Public archives such as the Image Data Resource (IDR) are OMERO deployments.

**Confirm:** GET the public repository home or documented OMERO JSON API. Skip a single image/screen landing page.

| Tool | Query |
|------|-------|
| Google | `"OMERO" OR "Image Data Resource" (microscopy OR repository) -site:github.com` |
| Censys | `web.endpoints.http.body: "OMERO"` |
| FOFA | `body="OMERO"` |

## Kadi4Mat (`kadi4mat`) {#kadi4mat}

KIT research-data infrastructure for materials science. Site: [kadi.iam.kit.edu](https://kadi.iam.kit.edu).

**Confirm:** GET the public records/collections UI or REST API. One record per public Kadi instance. Skip login-only lab tenants.

| Tool | Query |
|------|-------|
| Google | `"Kadi4Mat" OR "Kadi" (KIT OR "research data") -site:github.com` |
| Censys | `web.endpoints.http.body: "Kadi4Mat"` |
| FOFA | `body="Kadi4Mat"` |

## TR32DB (`tr32db`) {#tr32db}

University of Cologne CRC research-data management system (TR32DB), reused as CRC1211DB and TRR228DB.

**Signals:** path `/site/index.php`; scripts `/extLib/jquery/jquery-3.4.1.js`, `/lib/js/generic/helper.js`, `/lib/js/generic/newLogin.js`.

**Confirm:** GET `/site/index.php` and match the helper.js / newLogin.js stack. One record per CRC database. Do **not** set `tr32db` on CRC806DB (`crc806db.uni-koeln.de`), which is a different SPA.

| Tool | Query |
|------|-------|
| Google | `"TR32DB" OR "CRC1211DB" OR "TRR228DB" (database OR repository)` |
| Google | `inurl:/site/index.php (TR32DB OR CRC1211 OR TRR228)` |
| Censys | `web.endpoints.http.body: "/lib/js/generic/newLogin.js"` |
| FOFA | `body="newLogin.js" && body="TR32"` |

## e!DAL (`edal`) {#edal}

IPK Gatersleben electronic Data Archive Library. Core archive and domain stores (e!DAL-PGP) share the e!DAL stack.

**Confirm:** GET the public dataset catalog. One record per public e!DAL store. Skip a single DOI landing as a seed.

| Tool | Query |
|------|-------|
| Google | `"e!DAL" OR "eDAL" (IPK OR Gatersleben OR repository)` |
| Censys | `web.endpoints.http.body: "e!DAL"` |
| FOFA | `body="e!DAL"` |

## NOMAD (`nomad`) {#nomad}

NOMAD Laboratory archive and Oasis software for computational materials data. Site: [nomad-lab.eu](https://nomad-lab.eu). Central lab and self-hosted Oasis instances share `/prod/v1/api/v1/info`.

**Confirm:** GET `/prod/v1/api/v1/info` or the public upload/entry catalog. One record per public Oasis or the central archive. Skip a single calculation entry.

| Tool | Query |
|------|-------|
| Google | `"NOMAD" ("Oasis" OR "nomad-lab" OR "materials discovery") (repository OR API) -site:github.com` |
| Censys | `web.endpoints.http.body: "nomad-lab"` |
| FOFA | `body="nomad-lab"` |

## AODN Portal (`aodn`) {#aodn}

Australian Ocean Data Network marine/climate discovery. Hub: [portal.aodn.org.au](https://portal.aodn.org.au).

**Signals:** AODN portal chrome; `/portal/search`; IMOS/AODN branding.

**Confirm:** GET the public dataset search. One record for the portal (and any independent AODN regional catalog). Skip individual NetCDF files.

| Tool | Query |
|------|-------|
| Google | `"AODN" portal` |
| Censys | `web.names: "aodn.org.au"` |
| FOFA | `host="aodn.org.au"` |

## DataLad (`datalad`) {#datalad}

Git/git-annex dataset distribution. Site: [datalad.org](https://datalad.org). Docs: [docs.datalad.org](https://docs.datalad.org).

**Signals:** DataLad catalog UI or GIN-like dataset browser; `datalad` dataset metadata.

**Confirm:** GET a public dataset catalog (not a single git repo). One catalog per public DataLad/GIN-style catalog UI.

| Tool | Query |
|------|-------|
| Google | `"DataLad" (catalog OR datasets)` |
| Censys | `web.endpoints.http.body: "datalad"` |
| FOFA | `body="datalad"` |

## Djehuty (`djehuty`) {#djehuty}

4TU research-data repository platform. Site: [djehuty.org](https://djehuty.org). Source: [4TUResearchData/djehuty](https://github.com/4TUResearchData/djehuty).

**Signals:** Djehuty chrome; 4TU dataverse-style dataset UI.

**Confirm:** GET the public dataset search. One institutional repository per deployment.

| Tool | Query |
|------|-------|
| Google | `"Djehuty" (repository OR 4TU)` |
| Censys | `web.endpoints.http.body: "djehuty"` |
| FOFA | `body="djehuty"` |

## dLibra (`dlibra`) {#dlibra}

PSNC digital library/repository. Product: [dingo.psnc.pl/dlibra](https://dingo.psnc.pl/dlibra/). Docs: [dlibra.psnc.pl](https://dlibra.psnc.pl). Use only when the library **lists datasets**, not publication-only collections.

**Signals:** `/dlibra/` paths; dLibra chrome.

**Confirm:** GET a public collection that includes datasets. Skip theses-only libraries.

| Tool | Query |
|------|-------|
| Google | `"dLibra" (dane OR dataset)` |
| Censys | `web.endpoints.http.body: "dlibra"` |
| FOFA | `body="dlibra"` |

## Ensembl (`ensembl`) {#ensembl}

EMBL-EBI genome browsers. Hub: [ensembl.org](https://www.ensembl.org). Docs: [Ensembl API](https://www.ensembl.org/info/docs/api/index.html).

**Confirm:** do **not** clone www.ensembl.org. Register only distinct **taxon portals** (Fungi, Protists, Metazoa, Bacteria, Plants, …) with their own public UI.

| Tool | Query |
|------|-------|
| Google | `site:ensembl.org` taxon portals only |
| Censys | `web.names: "ensembl.org"` |
| FOFA | `domain="ensembl.org"` |

## GBIF Platform (`gbifplatform`) {#gbifplatform}

Global Biodiversity Information Facility infrastructure. Hub: [gbif.org](https://www.gbif.org). Guides: [gbif.org/guides](https://www.gbif.org/guides). Publisher IPT instances use `ipt`, not this id.

**Confirm:** do **not** re-add www.gbif.org. Register only a distinct GBIF-branded national/thematic portal. Prefer `ipt` for publisher IPT catalogs.

| Tool | Query |
|------|-------|
| Google | `"GBIF" (portal OR occurrence) -site:gbif.org` |
| Censys | `web.names: "gbif.org"` |
| FOFA | `domain="gbif.org"` |

## GIN (`gin`) {#gin}

G-Node git-annex neuroscience repositories. Hub: [gin.g-node.org](https://gin.g-node.org). Wiki: [G-Node/Info](https://gin.g-node.org/G-Node/Info/wiki).

**Signals:** Gogs-like UI; git-annex; G-Node branding.

**Confirm:** GET a public organization or dataset listing. One catalog for GIN (plus independent GIN-like deployments). Skip individual repositories as catalogs.

| Tool | Query |
|------|-------|
| Google | `site:gin.g-node.org` OR `"GIN" g-node` |
| Censys | `web.names: "gin.g-node.org"` |
| FOFA | `host="gin.g-node.org"` |

## HUBzero (`hubzero`) {#hubzero}

Science-gateway platform. Site: [hubzero.org](https://hubzero.org). Docs: [hubzero.org/documentation](https://hubzero.org/documentation).

**Signals:** HUBzero chrome; `/resources/` or publications/resources catalog.

**Confirm:** GET a public resources/database listing. One gateway per hub. Skip marketing and login-only sites.

| Tool | Query |
|------|-------|
| Google | `"HUBzero" (resources OR database)` |
| Censys | `web.endpoints.http.body: "HUBzero"` |
| FOFA | `body="HUBzero"` |

## SEANOE (`ifremercatalog`) {#ifremercatalog}

IFREMER oceanographic data publishing. Hub: [seanoe.org](https://www.seanoe.org).

**Signals:** SEANOE chrome; IFREMER dataset DOIs.

**Confirm:** GET the public dataset search. One catalog for SEANOE (plus independent IFREMER catalog UIs). Skip individual dataset landing pages.

| Tool | Query |
|------|-------|
| Google | `"SEANOE" IFREMER` |
| Censys | `web.names: "seanoe.org"` |
| FOFA | `domain="seanoe.org"` |

## LibreCat (`librecat`) {#librecat}

Publication and research-information repository. Site: [librecat.org](https://librecat.org). Source: [LibreCat/LibreCat](https://github.com/LibreCat/LibreCat).

**Signals:** LibreCat chrome; publication/dataset catalog.

**Confirm:** GET a public repository search that includes datasets. Skip publication-only CRIS with no dataset records.

| Tool | Query |
|------|-------|
| Google | `"LibreCat" repository` |
| Censys | `web.endpoints.http.body: "LibreCat"` |
| FOFA | `body="LibreCat"` |

## LinkAhead (`linkahead`) {#linkahead}

IndiScale research-data toolkit (formerly CaosDB). Site: [getlinkahead.com](https://getlinkahead.com/). Docs: [docs.indiscale.com](https://docs.indiscale.com/).

**Signals:** LinkAhead / CaosDB chrome; FAIR research-data catalog UI.

**Confirm:** GET a public dataset/entity browser. Stop on `401`. One catalog per public installation.

| Tool | Query |
|------|-------|
| Google | `"LinkAhead" OR CaosDB repository` |
| Censys | `web.endpoints.http.body: "LinkAhead"` |
| FOFA | `body="LinkAhead"` |

## MyTardis (`mytardis`) {#mytardis}

Instrument-data repository. Site: [mytardis.org](https://www.mytardis.org). Docs: [mytardis.readthedocs.io](https://mytardis.readthedocs.io).

**Signals:** MyTardis chrome; experiment/dataset browser.

**Confirm:** GET the public experiment/dataset list. One facility catalog per deployment.

| Tool | Query |
|------|-------|
| Google | `"MyTardis" (data OR repository)` |
| Censys | `web.endpoints.http.body: "MyTardis"` |
| FOFA | `body="MyTardis"` |

## NYU Data Catalog (`nyudatacatalog`) {#nyudatacatalog}

Open-source institutional dataset catalog (medical-library forks). Source: [NYU-DataCatalog/data-catalog](https://github.com/NYU-DataCatalog/data-catalog).

**Signals:** NYU Data Catalog chrome; Drupal/PHP data-catalog listings.

**Confirm:** GET the public dataset search. One catalog per institutional fork.

| Tool | Query |
|------|-------|
| Google | `"NYU Data Catalog" OR "data-catalog" medical library` |
| Censys | `web.endpoints.http.body: "Data Catalog"` |
| FOFA | `body="Data Catalog"` |

## Open Science Framework (`osf`) {#osf}

Center for Open Science collaboration/repository. Hub: [osf.io](https://osf.io). API docs: [developer.osf.io](https://developer.osf.io).

**Confirm:** register **institution** catalogs only (`osf.io/institutions/…` or branded institutional landing). Do not add every user project. Skip login-walled storage.

| Tool | Query |
|------|-------|
| Google | `site:osf.io` institution catalogs only |
| Censys | `web.names: "osf.io"` |
| FOFA | `domain="osf.io"` |

## PyDAP (`pydap`) {#pydap}

Python OPeNDAP server. Site: [pydap.github.io/pydap](https://pydap.github.io/pydap/). Docs: [pydap.readthedocs.io](https://pydap.readthedocs.io). Prefer `opendap` when the public product is a generic OPeNDAP directory.

**Signals:** PyDAP HTML directory; DAP `.dds` / `.das` on a PyDAP stack.

**Confirm:** GET the catalog directory of dataset nodes. Use `opendap` if PyDAP is not the branded product.

| Tool | Query |
|------|-------|
| Google | `"PyDAP" OPeNDAP` |
| Censys | `web.endpoints.http.body: "pydap"` |
| FOFA | `body="pydap"` |

## VuFind (`vufind`) {#vufind}

Library discovery over catalogs and repositories. Site: [vufind.org](https://vufind.org). Wiki: [vufind.org/wiki](https://vufind.org/wiki). Use only for **data/repo discovery**, not a library OPAC with no datasets.

**Signals:** VuFind chrome; `/vufind/` paths; research-data community.

**Confirm:** GET a public search that lists datasets or research-data records. Skip publication-only library catalogs.

| Tool | Query |
|------|-------|
| Google | `"VuFind" (research data OR datasets)` |
| Censys | `web.endpoints.http.body: "VuFind"` |
| FOFA | `body="VuFind"` |

## Other scientific platforms

| `software.id` | Signals | Typical query |
|---------------|---------|---------------|
| `haplo` | see above | |
| `worktribe` | see above | |
| `seek` | see above | |
| `ramadda` | see above | |
| `labkey` | see above | |
| `synapse` | see above | |
| `xnat` | see above | |
| `omero` | see above | |
| `kadi4mat` | see above | |
| `edal` | see above | |
| `nomad` | see above | |
| `nyudatacatalog` | see above | |
| `icat` | see above | |
| `ensembl` | see above | |
| `datalad` | see above | |
| `hubzero` | see above | |
| `linkahead` | see above | |
| `vufind` | see above | |
| `mytardis` | see above | |
| `librecat` | see above | |
| `gin` | see above | |
| `symbiota` | see above | |
| `breedbase` | BrAPI crop breeding instances | `"Breedbase" OR CassavaBase BrAPI` |
| `tripal` | Tripal/Chado genome databases | `"Powered by Tripal"` |
| `veupathdb` | EuPathDB WDK organism sites | `VEuPathDB OR PlasmoDB` |
| `massbank` | MassBank / MoNA instances | `"MassBank" spectra database` |
| `iochembd` | ioChem-BD nodes + Find index | `"ioChem-BD" repository` |
| `esgf` | Metagrid / esg-search (not TDS) | `"esg-search" OR Metagrid ESGF` |
| `yoda` | see above | |
| `gbifplatform` | see above | |
| `converis` | see above | |
| `aodn` | see above | |
| `osf` | see above | |
| `ifremercatalog` | see above | |
| `pydap` | see above | |
| `djehuty` | see above | |
| `dlibra` | see above | |

## Generic scientific probes

On a **named** university or lab host:

```text
/oai/request?verb=Identify
/oai?verb=Identify
/api/info/version
/api/records?size=1
/server/api
/digital/api/collections
/api/items
```

Google: ``"research data repository" {university}``, ``"repositorio de datos" {universidad}``, ``Forschungsdaten {hochschule}``. re3data.org advanced search by country and software is usually faster than Google for this class.

## Country university IRs {#country-university-irs}

Prompt: `There are a lot of {country} universities and research organizations that could have scientific data repositories that are not yet listed. Which of them are missing?`

1. Count existing `scientific/` YAML for that ISO folder (DuckDB or path glob). Skip the hunt if the folder is already thick (US, DE, GB, IT AIR/IRIS, ES DSpace).
2. Pull [OpenDOAR](https://v2.sherpa.ac.uk/opendoar/) (country + software), [ROAR](http://roar.eprints.org), re3data country facet, OpenAIRE Graph country, and national aggregators (IRDB Japan, DABAR, OpenScience.si, Scholaris Canada).
3. Duplicate-check hostname. Probe DSpace `/server/api` or `/oai/request?verb=Identify`, Dataverse `/api/info/version`, EPrints `/cgi/oai2?verb=Identify`.
4. **Accept only IRs that list datasets.** DSpace 7: Dataset type browse or `/server/api` type facet. Dataverse and research-data communities count. Publication-only IRs were added and later removed (ten Kazakhstan hosts).
5. Skip login-only, dead/parked, theses-only with no Dataset type, and microstates with no universities (Monaco, Liechtenstein, Kiribati). [CoreTrustSeal](https://www.coretrustseal.org/) is a useful overlay — keep certified hosts that have a public dataset catalog, not preservation systems (SPAR, EWIG, film archives). If OpenDOAR + re3data for that country are exhausted, report 0 missing and stop.

`is_national: false` except for a country’s official research-data catalog of that type.

## FLAT (`flat`) {#flat}

[Fedora Language Archiving Technology](https://github.com/TLA-FLAT/FLAT) packages Fedora
Commons and Islandora for language-resource repositories with CLARIN Component Metadata.
**Signals:** FLAT-specific theme assets such as `flat_bootstrap_theme`, Islandora resource
routes under `/flat/`, and attribution to The Language Archive. The path `/flat/` alone is
not enough. The upstream Docker setup documents the package's repository components.

**Confirm:** check the public collection page and its advertised OAI-PMH Identify response.
Lund Humanities Lab serves `/flat/oai2?verb=Identify`; other deployments may use different
OAI paths. **Search:** `"flat_bootstrap_theme"` or `"Fedora Language Archiving Technology"`.
Use the more specific `flat` ID only with FLAT evidence; ordinary Islandora remains `islandora`.


| Tool | Query |
|------|-------|
| Google | `"flat_bootstrap_theme" OR "Fedora Language Archiving Technology"` |
| Censys | `web.endpoints.http.body: "flat_bootstrap_theme"` |
| FOFA | `body="flat_bootstrap_theme"` |


## openEQUELLA (`openequella`) {#openequella}

[openEQUELLA](https://www.edalex.com/openequella/) is the reusable EQUELLA repository family.
**Signals:** versioned assets under `p/r/{version}/com.equella.core/`, EQUELLA branding,
and repository collection/search pages. Oxford Brookes RADAR is a verified installation.
Do not confuse that institution's RADAR name with the separate RADAR repository software.

**Search:** `"com.equella.core"` or `"openEQUELLA" "research"`.
Check the live asset paths and published OAI endpoint; a generic `/items/` route is not enough.
The [source project](https://github.com/openequella/openEQUELLA) and vendor use cases
establish reuse across independent institutions.


| Tool | Query |
|------|-------|
| Google | `"com.equella.core" OR "openEQUELLA" research` |
| Censys | `web.endpoints.http.body: "com.equella.core"` |
| FOFA | `body="com.equella.core"` |


## Aubrey (`aubrey`) {#aubrey}

UNT Libraries' public digital collection platform. The
[operator's infrastructure description](https://library.unt.edu/digital-libraries/trusted-digital-repository/)
and [instance presentation](https://digital.library.unt.edu/ark:/67531/metadc2405129/m1/7/)
identify separate Aubrey deployments at UNT Digital Library, Portal to Texas History and
Gateway to Oklahoma History.

**Signals:** operator-confirmed Aubrey deployment, `/explore/collections/{code}/`, ARK item
links and collection-specific API help. ARKs and OAI-PMH alone are not Aubrey fingerprints.
**Search:** `"Aubrey" "digital library"` and `site:library.unt.edu "Aubrey"`.
The public GitHub repository is empty as reviewed; do not describe it as downloadable source.


| Tool | Query |
|------|-------|
| Google | `"Aubrey" "digital library" site:.edu` |
| Censys | `web.endpoints.http.body: "/explore/collections/"` |
| FOFA | `body="/explore/collections/" && body="ARK"` |


## Dialnet CRIS (`dialnetcris`) {#dialnetcris}

[Fundacion Dialnet's hosted research-portal product](https://fundaciondialnet.unirioja.es/servicios/dialnet-cris/)
is used by multiple institutions. **Signals:** Fundacion Dialnet attribution on a research
portal with researcher, project and output navigation, confirmed against the provider's
portal directory or the institution's product documentation. La Rioja's research portal is
an example. Linking to a Dialnet publication is not evidence that Dialnet powers the site.

**Search:** `"Dialnet CRIS" "portal"` or `"Fundación Dialnet" "investigadores"`.
Distinguish hosted institutional CRIS portals from the central Dialnet bibliographic database.

| Tool | Query |
|------|-------|
| Google | `"Dialnet CRIS" portal OR "Fundación Dialnet" investigadores` |
| Censys | `web.endpoints.http.body: "Dialnet CRIS"` |
| FOFA | `body="Dialnet CRIS"` |

## Related

- [discovery-scientific-domain.md](discovery-scientific-domain.md)
- [discovery.md](discovery.md)
- [discovery.md](discovery.md#hunt-patterns) — session hunt patterns
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-metadata.md](discovery-metadata.md)
- [discovery-other.md](discovery-other.md)
- [re3data.md](re3data.md)
- [harvest.md](harvest.md) — crawl datasets from repository APIs (filter publications vs data)
- [harvest-scientific.md](harvest-scientific.md), [harvest-scientific-domain.md](harvest-scientific-domain.md), [harvest-biodiversity.md](harvest-biodiversity.md), [harvest-earthdata.md](harvest-earthdata.md)
- [software-taxonomy.md](software-taxonomy.md)

