# Harvesting datasets from scientific repositories

Institutional repositories and CRIS portals mix **publications, theses, software, and research data**. Harvest the public API, then **filter to datasets**. Overview and keep/drop vocabulary: [harvest.md](harvest.md). Finding installations: [discovery-scientific.md](discovery-scientific.md). Domain stacks: [discovery-scientific-domain.md](discovery-scientific-domain.md).

Replace `https://host` with the catalog `link` origin (no trailing slash unless the path needs it). GET only. Stop on `401`/`403`.

Use `endpoints[]` from the registry when present ([apidetect.md](apidetect.md)). Paths below are the defaults those maps probe.

| Page | Use when |
|------|----------|
| This page | Institutional repositories and CRIS (Dataverse, DSpace, Invenio, EPrints, Pure, Converis, Omega-PSIR, Archipelago, RADAR, Yoda, Redivis, LabKey, Synapse, XNAT, OMERO, Kadi4Mat, e!DAL, NOMAD, META-SHARE, Gen3, TR32DB, …) |
| [Domain repositories](harvest-scientific-domain.md) | IPT, Symbiota, THREDDS, ERDDAP, Breedbase, Tripal, VEuPathDB, MassBank, ioChem-BD, ESGF, ALA, SciCat-adjacent stacks, CLLD, TalkBank, Pathway Tools, IBDC |

All `software.id` values: [software-index.md](software-index.md).

## Mixed vs dataset-native

| Class | `software.id` (typical) | Filter needed? |
|-------|-------------------------|----------------|
| Mixed IR / CRIS | `dspace`, `dspacecris`, `invenio`, `inveniordm`, `eprints`, `hyrax`, `samvera`, `islandora`, `archipelago`, `opus`, `mycore`, `phaidra`, `weko3`, `dabar`, `opensciencesi`, `pure`, `esploro`, `elsevierdigitalcommons`, `figshare`, `haplo`, `worktribe`, `omegapsir`, `converis`, `librecat`, `vufind`, `divaportal` | **Yes** — publications dominate |
| Dataset-native | `dataverse`, `radar`, `yoda`, `redivis`, `instdb`, `labkey`, `synapse`, `xnat`, `omero`, `kadi4mat`, `edal`, `nomad`, `gen3` on this page; IPT/THREDDS/Breedbase/ESGF/InterMine/cBioPortal and similar on [harvest-scientific-domain.md](harvest-scientific-domain.md) | Little or none — still skip files, occurrences, and login-only rows |

## OAI-PMH fallback (any IR)

When REST search has no type filter, use OAI-PMH ([harvest-protocols.md](harvest-protocols.md#oai-pmh)).

1. `GET https://host/oai/request?verb=Identify` (DSpace) or the Identify URL in `endpoints[]`.
2. `verb=ListSets` — keep `setSpec` values that mean data (`ResearchData`, `doc-type:researchdata`, `datasets`, `Dataset`, `Forschungsdaten`). Ignore `com_` / `col_` sets that are the whole repository.
3. `verb=ListRecords` with `metadataPrefix=oai_dc` and `set` equal to that `setSpec`. Follow `resumptionToken`.
4. If no dataset set exists, harvest `oai_dc` and **keep** records whose `dc:type` (or DataCite `resourceTypeGeneral`, or COAR URI) matches the [keep list](harvest.md#keep-vs-drop-shared-vocabulary).

Common Identify paths: `/oai?verb=Identify`, `/oai/request?verb=Identify`, `/cgi/oai2?verb=Identify`, `/oai2d`, `/ws/oai?verb=Identify`, `/api/oai?verb=Identify`.

Do not treat `ListIdentifiers` titles as datasets. Do not harvest `metadataPrefix=marc21` as a substitute for type.

## Dataverse (`dataverse`) {#dataverse}

Native search already distinguishes objects. Prefer **datasets**, not files or sub-dataverses.

**List datasets:**

```text
GET https://host/api/search?q=*&type=dataset&per_page=100&start=0
```

Page with `start`. `total_count` is in the JSON envelope.

**Also useful:** `/api/info/version` (`dataverseapi`), OAI `/oai?verb=Identify`.

**Drop:** `type=file` (file hits under a dataset), `type=dataverse` (collections), `/dataset.xhtml?persistentId=` as a crawl seed (that is one record). Harvest the installation root from the registry, then this search API.

**Keep:** `type=dataset` search hits.

Docs: [guides.dataverse.org](https://guides.dataverse.org).

## DSpace 7+ (`dspace`) {#dspace}

DSpace items are publications, theses, and datasets in one index.

**Unfiltered (do not use as the crawl):** `/server/api/discover/search/objects`

**Worked example A — DSpace 7 entity type**

Filter to dataset entities (DSpace-CRIS / configurable entities):

```text
GET https://host/server/api/discover/search/objects?dsoType=ITEM&f.entityType=Dataset,equals&size=100&page=0
```

Some campuses name the entity `ResearchData` or `Product`. Inspect facets once:

```text
GET https://host/server/api/discover/search/objects?dsoType=ITEM&size=0
```

Read `_embedded.searchResult.page` and facet values for `entityType` / `dc.type`. If there is no entity type, filter Solr-style:

```text
GET https://host/server/api/discover/search/objects?dsoType=ITEM&query=dc.type:Dataset&size=100
```

Try `Forschungsdaten`, `Research Data`, and `Dataset` — values are local.

**Worked example B — classic OAI ListSets (`dc.type`)**

DSpace 6 and 7 fallback when REST has no entity type:

```text
GET https://host/oai/request?verb=Identify
GET https://host/server/oai/request?verb=Identify
GET https://host/oai/request?verb=ListSets
GET https://host/oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=col_123456789_4
```

Keep `setSpec` values whose name is dataset / research data / Forschungsdaten. Ignore `com_` community sets that are the whole repository. Then `ListRecords` with that `set`. If no dataset set exists, harvest `oai_dc` and keep records whose `dc:type` matches the [keep list](harvest.md#keep-vs-drop-shared-vocabulary).

**DSpace 6 REST:** `/rest/items` has no reliable type filter. Prefer OAI as above, or skip 6.x hosts without a dataset collection.

**Drop:** `dsoType=COMMUNITY` / `COLLECTION`, researcher `Person` / `OrgUnit` / `Project` (CRIS), bitstream URLs.

**Keep:** items filtered to Dataset / ResearchData (REST entity type, `dc.type`, or OAI dataset set).

## DSpace-CRIS (`dspacecris`) {#dspacecris}

Same REST/OAI as [DSpace](#dspace). Prefer `f.entityType=Dataset,equals` (or the campus ResearchData entity). Drop CRIS `Person`, `OrgUnit`, and `Project` objects.

**Keep:** Dataset / ResearchData entities via REST or OAI.
**Drop:** CRIS `Person`, `OrgUnit`, and `Project` objects.

```text
GET https://host/server/api/discover/search/objects?f.entityType=Dataset,equals
```


## Invenio (`invenio`) {#invenio}

Classic Invenio (not RDM). `/api/records` returns **all** record types.

```text
GET https://host/api/records?size=25
```

Filter to datasets the same way as [InvenioRDM](#inveniordm), then confirm the UI is not InvenioRDM-branded. **Keep:** `resource_type` dataset. **Drop:** `publication`, `presentation`, `poster`, `image`, `video`, `lesson`, `other`. `software` is not a dataset. OAI is often `/oai2d?verb=Identify`; some classic installs also expose `/oai?verb=Identify`.

## InvenioRDM (`inveniordm`) {#inveniordm}

`/api/records` returns **all** record types (publication, dataset, software, poster, …).

```text
GET https://host/api/records?q=metadata.resource_type.type:dataset&size=100&page=1
```

If that query returns zero but the UI has a Dataset facet, try:

```text
GET https://host/api/records?q=metadata.resource_type.id:dataset&size=100
GET https://host/api/records?type=dataset&size=100
```

Follow `links.next`. Inspect `hits.hits[].metadata.resource_type`.

**Drop:** `publication`, `presentation`, `poster`, `image`, `video`, `lesson`, `other` unless you explicitly want those corpora. `software` is not a dataset.

**Keep:** `resource_type` dataset (or `type=dataset`).

OAI is often `/oai2d?verb=Identify`. Skip zenodo.org if you only need institutional instances already in the registry.

Docs: [inveniordm.docs.cern.ch](https://inveniordm.docs.cern.ch).

## EPrints (`eprints`) {#eprints}

Every eprint has a `type` (`article`, `thesis`, `dataset`, `monograph`, …).

**Browse/export by type:**

```text
GET https://host/cgi/exportview/type/dataset/JSON/dataset.js
```

**Search:** `/cgi/search/archive/advanced` with `type=dataset` (parameter names vary; confirm on one host).

OpenSearch description is `/cgi/opensearchdescription`. Detection types it `opensearch`.

```text
GET https://host/cgi/opensearchdescription
```

**REST:** `/rest/eprint/` plus the numeric eprint id (`.xml`) is per-record. For a crawl, OAI is better:

```text
GET https://host/cgi/oai2?verb=ListSets
GET https://host/cgi/oai2?verb=ListRecords&metadataPrefix=oai_dc&set=DATASET_SET
```

If there is no dataset set, ListRecords and keep `dc:type` = `dataset` / `Dataset`.

**Drop:** `article`, `thesis`, `book`, `conference_item`, `exhibition`, `performance`.

**Keep:** eprints with `type=dataset` (exportview, OAI set, or `dc:type`).

## Samvera Hyrax (`hyrax`) {#hyrax}

Blacklight JSON catalog. Work types include GenericWork, Dataset, Etd, Image, FileSet.

```text
GET https://host/catalog.json?f[human_readable_type_sim][]=Dataset&per_page=100&page=1
```

If that facet is empty, try `f[resource_type_sim][]=Dataset` or `f[has_model_ssim][]=Dataset`. FileSets are files, not datasets.

Optional OAI-PMH when the Blacklight OAI plugin is enabled:

```text
GET https://host/catalog/oai?verb=Identify
```

Then `ListSets` / `ListRecords` with the [OAI fallback](#oai-pmh-fallback-any-ir).

**Keep:** Blacklight works typed Dataset. **Drop:** FileSets, GenericWork/Etd/Image unless they are the data product.

## Samvera (`samvera`) {#samvera}

Same Blacklight harvest as [Hyrax](#hyrax) when the UI is Samvera without Hyrax branding.

```text
GET https://host/catalog.json?f[human_readable_type_sim][]=Dataset&per_page=100&page=1
```

Same optional OAI as [Hyrax](#hyrax): `/catalog/oai?verb=Identify`.

**Keep:** Dataset works (same grain as Hyrax). **Drop:** FileSets and publication-only work types.

Islandora (`islandora`) is Drupal+Fedora: harvest the public JSON:API or Solr only when a **dataset** content model / collection exists. Prefer Islandora over raw `fedora` `/fcrepo/rest`. See [Islandora](#islandora).

## OPUS (`opus`) {#opus}

German IRs. The dataset document type is usually `researchdata` / `ResearchData`.

```text
GET https://host/oai?verb=ListSets
```

Look for `doc-type:researchdata` (spelling varies). Then:

```text
GET https://host/oai?verb=ListRecords&metadataPrefix=oai_dc&set=doc-type:researchdata
```

Solr UI often supports a doctype facet (`doctypefq=researchdata`). Thesis-only OPUS hosts have no dataset set — skip them for a data crawl (they can still be valid **catalog** records).

**Keep:** `doc-type:researchdata` / ResearchData OAI or Solr facet. **Drop:** thesis-only OPUS hosts for a data crawl.

## MyCoRe (`mycore`) {#mycore}

```text
GET https://host/api/v2/objects
GET https://host/servlets/OAIDataProvider?verb=ListSets
```

Classification values are local (`mir_types`, `state`). Filter to data/Forschungsdaten classes after reading one object and `ListSets`. Unfiltered `/api/v2/objects` is the whole IR.

**Keep:** objects in data/Forschungsdaten classes. **Drop:** unfiltered `/api/v2/objects` as the whole IR.

## PHAIDRA (`phaidra`) {#phaidra}

```text
GET https://host/api/search/select?q=*:*&rows=0
GET https://host/api/oai?verb=Identify
GET https://host/api/openapi
```

Add a type constraint once you see stored fields (often `cmodel`, `dc_type`, or `object_type`). Example patterns to try: `cmodel:*Dataset*`, `dc_type:dataset`. Drop image/book/thesis cmodels.

Type Dataset Solr select (`cmodel:*Dataset*` or `dc_type:dataset`) as `rest`.

**Keep:** Dataset cmodels / `dc_type:dataset`. **Drop:** image, book, and thesis cmodels.

## DiVA Portal (`divaportal`) {#divaportal}

Mixed IR. Publications dominate. Prefer a research-data filter on smash search or OAI.

```text
GET https://host/smash/search.jsf
GET https://www.diva-portal.org/smash/oai?verb=Identify
```

Type `/smash/search.jsf` as `index`. Keep records typed as research data / dataset. Drop articles, theses, and reports. One harvest scope per `{org}.diva-portal.org` tenant.

**Keep:** research data / dataset records (smash filter or OAI). **Drop:** articles, theses, and reports.

## WEKO3 (`weko3`) {#weko3}

Item **type IDs are per instance**. The registry probe uses `type=` on `/api/records/` — that integer is **not** portable.

1. Open the public search UI or API and list item types.
2. Find the id for research data / 研究データ / Dataset.
3. Crawl `/api/records/?type=ITEM_TYPE_ID&page=1&size=20` (replace `ITEM_TYPE_ID`).

Without a resolved type id, you will ingest articles and reports. OAI Identify is portable when present; still filter ListRecords to a research-data set or `dc:type`.

```text
GET https://host/api/records/?page=1&size=20
GET https://host/oai?verb=Identify
```

**Keep:** WEKO3 items whose type id is research data / Dataset. **Drop:** articles and reports (unfiltered `/api/records/`).

## Elsevier Pure (`pure`) {#pure}

The public **portal** lists `/en/datasets/` (locale prefix varies: `/de/datasets/`, `/da/datasets/`). Publications live under `/publications/` and `/persons/`.

**Prefer the datasets channel:**

```text
GET https://host/sitemap/datasets.xml
GET https://host/en/datasets/?search=&format=rss
```

Locale prefix varies (`/de/datasets/`, `/da/datasets/`). Type those dataset RSS feeds as `rss`.

OAI: `/ws/oai?verb=Identify` then `ListSets` for a datasets set.

Pure Web Services (`/ws/api/datasets`) often need an API key. If you get `401`, use the public portal/OAI/sitemap. Do not guess keys.

**Drop:** `/publications/`, activities, prizes, student theses unless typed as datasets.

**Keep:** Pure **datasets** channel (`/datasets/` sitemap, RSS, or OAI datasets set).

## Esploro (`esploro`) {#esploro}

Research outputs include datasets as one resource type.

The registry map checks `/view/google/siteindex.xml` for `/dataset/` paths. Use that sitemap when it exists.

Otherwise use the public research search with a **datasets** facet (UI labels: Dataset, Research data). The SOAP/WADL probe `/esplorows/rest/research/simpleSearch` is a capability URL, not a full crawl.

**Drop:** articles, books, conference papers, ETDs in the same index.

```text
GET https://host/view/google/siteindex.xml
```

**Keep:** Esploro records with a datasets / research-data facet.

## Elsevier Digital Commons (`elsevierdigitalcommons`) {#elsevierdigitalcommons}

Collections mix articles and data series. OAI: `/do/oai/?verb=ListSets` or `/oai?verb=ListSets` on Elsevier Data Repository hosts. Harvest only sets whose names are data/datasets/statistics — not the whole IR.

Sitemap `/sitemap/index` can list every series; still skip photograph and journal series.

```text
GET https://host/do/oai/?verb=ListSets
GET https://host/oai?verb=ListSets
```

**Keep:** OAI sets named data/datasets/statistics. **Drop:** photograph and journal series, and the unfiltered IR.

## Figshare (`figshare`) {#figshare}

Institutional Figshare (not every figshare.com article). Item types are numeric.

| `item_type` | Meaning |
|-------------|---------|
| 3 | Dataset — **keep** |
| 4 | Fileset — **keep** (collection of files) |
| 9 / 18 | Code / software — not a dataset |
| 6, 8, 5, 7 | Paper, thesis, poster, presentation — **drop** |

GraphQL/search endpoints vary by tenant. Prefer the institution’s public API or sitemap entries under `/articles/dataset/`. Do not crawl `figshare.com/articles` globally.

```text
GET https://host/articles/dataset/
```

Type `/articles/dataset/` as `index`. **Keep:** institutional Figshare `item_type` 3 (dataset) and 4 (fileset). **Drop:** papers, theses, posters, presentations, and a global figshare.com crawl.

## Haplo (`haplo`) {#haplo}

Output types include publications and datasets. Use the public catalog/OAI and keep records typed as dataset / research data. Skip grant and HR objects. Skip haplo.com marketing hosts.

**Keep:** public catalog/OAI records typed as dataset or research data.
**Drop:** grant, HR, and person objects; haplo.com marketing hosts.

```text
GET https://host/oaiprovider?verb=Identify
GET https://host/oaiprovider?verb=ListSets
```


## Worktribe (`worktribe`) {#worktribe}

Public catalog/OAI (`/oaiprovider?verb=Identify`). Keep dataset / research data. Skip grant/HR objects and worktribe.com marketing.

**Keep:** public catalog/OAI records typed as dataset / research data.
**Drop:** grant/HR objects and worktribe.com marketing.

```text
GET https://host/oaiprovider?verb=Identify
GET https://host/oaiprovider?verb=ListRecords&metadataPrefix=oai_dc
```


## Omega-PSIR (`omegapsir`) {#omegapsir}

CRIS with separate publications vs data modules when configured. Prefer URLs/APIs under a datasets/research-data listing. A global publication search is the wrong crawl.

**Keep:** records from a datasets / research-data module when configured.
**Drop:** global publication search hits (articles, theses) as datasets.

```text
GET https://host/oai?verb=Identify
```


## VuFind (`vufind`) {#vufind}

Discovery layer over mixed IRs.

```text
GET https://host/vufind/Search/Results?type=AllFields&filter[]=format%3A"Dataset"
GET https://host/api?openapi
```

Add a format/type facet (`format:Dataset`, `document_type:dataset`) **before** paging. Type the Dataset Search/Results listing as `index`. Attach `/Search/Results` to the catalog `link`; do not prefix `/vufind` again when the link already includes that mount. Type `/api?openapi` as `openapi`. **Keep:** facet-filtered dataset records. **Drop:** unfiltered library-catalog hits.

## LibreCat (`librecat`) {#librecat}

Same facet-first harvest as [VuFind](#vufind) when the public UI is LibreCat. Optional OAI Identify is `/oai?verb=Identify` at the repository origin (not under a `/search` UI mount).

**Keep:** facet-filtered dataset / research-data records (same grain as VuFind).
**Drop:** publications and person records.

```text
GET https://host/vufind/Search/Results?type=AllFields&filter[]=format%3A"Dataset"
GET https://host/oai?verb=Identify
```

Type the Dataset Search/Results listing as `index` (same grain as [VuFind](#vufind)). OAI Identify is `oaipmh20`.

## InstDB (`instdb`) {#instdb}

FairStack institutional research-data nodes. Harvest the public dataset/API list on the node (`/api` when present). Skip fairstack.cn marketing and per-file URLs.

**Keep:** dataset records from the node `/api` (or documented catalog list).
**Drop:** fairstack.cn marketing pages and per-file object URLs.

```text
GET https://host/api
```


## META-SHARE (`metashare`) {#metashare}

Language-resource nodes. Harvest the public **resource catalog** (corpora, lexica, tools) from the node search or documented export.

```text
GET https://host/
```

Keep resource records. Drop a single corpus/tool landing page as a crawl seed and META-NET marketing pages. One harvest scope per node. Victoria MetaShare is GeoNetwork — use that recipe instead.

**Keep:** public **resource catalog** records (corpora, lexica, tools). **Drop:** a single corpus/tool landing as a crawl seed and META-NET marketing.

## NYU Data Catalog (`nyudatacatalog`) {#nyudatacatalog}

Medical-library dataset catalog (schema.org DataCatalog JSON-LD on listing pages). Harvest **Dataset** objects from JSON-LD or the public search listing. Drop expert/person pages. Drupal JSON:API only if a dataset bundle exists.

**Keep:** schema.org **Dataset** objects from JSON-LD or the public listing. **Drop:** expert/person pages.

## DataLad (`datalad`) {#datalad}

Harvest the published **catalog** dataset list (`catalog.json` or the catalog site’s dataset pages), not git-annex keys.

**Keep:** dataset entries in the published DataLad catalog (`catalog.json` or equivalent dataset pages).
**Drop:** git-annex keys, annex object URLs, and Git commit pages.

```text
GET https://host/catalog.json
```


## GIN (`gin`) {#gin}

```text
GET https://host/api/v1/repos/search
```

**Keep:** public **repositories** that are datasets. **Drop:** git objects and private repos. Stop on `401`.

## HUBzero (`hubzero`) {#hubzero}

Scientific gateway. Harvest public **resources** typed as datasets/databases. Drop tools, tickets, and login-only groups.

**Keep:** public resources typed as datasets/databases.
**Drop:** tools, tickets, and login-only groups.

```text
GET https://host/resources?sortby=date
```


## LinkAhead (`linkahead`) {#linkahead}

CaosDB REST (`/api/v1/`). Query Record types that are datasets/collections. Drop files and properties as extra datasets.

**Keep:** Record types that are datasets/collections.
**Drop:** files and properties as extra datasets.

Type `/api/v1/` as `rest`.

```text
GET https://host/api/v1/
```


## Fedora (`fedora`) {#fedora}

Use Fedora LDP `/fcrepo/rest` (or `/rest`) **only** when Fedora is the public catalog. Prefer Hyrax/Islandora/PHAIDRA/Archipelago recipes on the same host.

**Keep:** LDP containers that represent datasets or data collections when Fedora is the public catalog.
**Drop:** bitstreams as separate datasets when a parent object exists; prefer Hyrax/Islandora/PHAIDRA/Archipelago on the same host.

```text
GET https://host/fcrepo/rest
GET https://host/rest
```


## DABAR (`dabar`) {#dabar}

Mixed IR (theses, publications, and some research data) on SRCE’s national stack.

1. `GET https://host/oai/?verb=Identify` (hub and some tenants use `/oai/?verb=Identify`; others `/oai?verb=Identify`).
2. `verb=ListSets` — keep setSpecs that mean research data / datasets. Ignore the whole-repository set.
3. If no dataset set exists, harvest `oai_dc` and keep records whose `dc:type` matches the [keep list](harvest.md#keep-vs-drop-shared-vocabulary).

Do not crawl `dabar.srce.hr/search?ns=` as a separate catalog. Prefer the institutional hostname already in the registry. Drop ETDs and journal articles unless typed as datasets.

**Keep:** OAI sets that mean research data / datasets (or `dc:type` keep-list). **Drop:** ETDs and journal articles unless typed as datasets.

## OpenScience.si repository (`opensciencesi`) {#opensciencesi}

Mixed IR. OAI is usually:

```text
GET https://host/oai/oai2.php?verb=Identify
```

Some tenants use `/oai/?verb=Identify`. `ListSets` then keep research-data / dataset sets. Otherwise filter `oai_dc` with the keep list. Skip the national aggregator `www.openscience.si` for dataset harvest — use the university tenants.

**Keep:** research-data / dataset OAI sets (or `oai_dc` keep-list). **Drop:** the national aggregator `www.openscience.si` as a dataset harvest.

## Islandora (`islandora`) {#islandora}

Drupal+Fedora. Harvest Solr/REST with a Dataset content model — not every Drupal node. Prefer Islandora over raw [Fedora](#fedora).

**Keep:** Islandora objects with a Dataset (or equivalent) content model.
**Drop:** every Drupal node, exhibit pages, and raw Fedora bitstreams.

```text
GET https://host/solr/select?q=RELS_EXT_hasModel_uri_ms:*Dataset*&wt=json&rows=25
GET https://host/jsonapi
```

Type the Solr Dataset select as `rest`. Solr `wt=json` may be served as `text/plain`.

Optional OAI-PMH Identify (portable paths only; skip host-specific `/api/oai2` and `/oaiprovider/`):

```text
GET https://host/oai/request?verb=Identify
GET https://host/oai2?verb=Identify
GET https://host/oai?verb=Identify
```

Then `ListSets` / `ListRecords` with the [OAI fallback](#oai-pmh-fallback-any-ir).


## Archipelago Commons (`archipelago`) {#archipelago}

Drupal Strawberryfield ADOs. Mixed GLAM instances need a Dataset (or accession/isolate) filter; germplasm and culture-collection catalogs may harvest every ADO.

```text
GET https://host/search?f[0]=descriptive_metadata_object_types:Dataset
GET https://host/rss.xml
GET https://host/jsonapi/node/digital_object
GET https://host/api/oai_pmh/oai?verb=Identify
```

Type Dataset search as `index`. Keep `Dataset`, accession, and isolate records. Drop Photograph, Book, Finding Aid, and WebPage exhibits. OAI-PMH `/api/oai_pmh/oai?verb=Identify` is optional and often restricted. Prefer Archipelago over raw `drupal`.

**Keep:** `Dataset`, accession, and isolate records. **Drop:** Photograph, Book, Finding Aid, and WebPage exhibits.

## CONTENTdm (`contentdm`) {#contentdm}

Only when the site was accepted as a **dataset** catalog ([discovery-scientific.md](discovery-scientific.md)). `/digital/api/collections` plus OAI; keep statistical/climate collections, skip photo exhibits.

**Keep:** collections that are statistical, climate, or research datasets.
**Drop:** photo/manuscript exhibits and individual image records.

```text
GET https://host/digital/api/collections
GET https://host/digital/oai/oai.php?verb=Identify
```


## Omeka S (`omekas`) {#omekas}

Only when accepted as a dataset catalog. `/api/items` filtered to Dataset / DataCatalog classes; skip exhibit images.

**Keep:** `/api/items` filtered to Dataset / DataCatalog classes.
**Drop:** exhibit images. Only when the site was accepted as a dataset catalog.

```text
GET https://host/api/items?resource_class_label=Dataset
```


## OSF (`osf`) {#osf}

Harvest **institution** or named project catalogs only (`https://api.osf.io/v2/`). Keep nodes/registrations that are data. Do not crawl all of osf.io. Stop on `401`.

**Keep:** institution or named project nodes/registrations that are data.
**Drop:** a crawl of all osf.io. Stop on `401`.

```text
GET https://api.osf.io/v2/nodes/?filter[parent]=null
```


## Converis (`converis`) {#converis}

Clarivate CRIS. Same publication-vs-data problem as Pure: harvest **datasets**, not publications or persons. Filter exports on `software.id = 'converis'`.

Prefer a public datasets / research-data listing or OAI `setSpec` for data. Stop on `/ws` API keys. Do not page an unfiltered publication search.

**Keep:** public **datasets** / research-data listing or OAI data setSpec. **Drop:** unfiltered publication search, persons, and `/ws` API keys.

## Djehuty (`djehuty`) {#djehuty}

4TU.ResearchData stack. Harvest the public dataset search (Invenio-like `resource_type` filter when exposed).

**Keep:** records typed as dataset / research data in the public search.
**Drop:** publications, presentations, and login-only deposit forms.

```text
GET https://host/api/records?q=metadata.resource_type.type:dataset&size=25
GET https://host/v2/articles
```

Type Invenio-like `/api/records` as `inveniordmapi:records`. Some tenants list articles at `/v2/articles` (`rest`).


## RADAR (`radar`) {#radar}

FIZ Karlsruhe research data repositories (RADAR Cloud and RADAR Local). Filter exports on `software.id = 'radar'`.

```text
GET https://host/radar/api/datasets
GET https://host/oai/OAIHandler?verb=Identify
```

Already datasets (`totalHits` in the JSON). Page the API; keep dataset ids/DOIs. Skip a single `/radar/de/dataset/` landing page as a seed and the FIZ marketing site. OAI is a fallback. Discovery: [discovery-scientific.md](discovery-scientific.md#radar).

**Keep:** RADAR **dataset** ids/DOIs from `/radar/api/datasets` or OAI. **Drop:** a single landing page as a seed and FIZ marketing.

## Redivis (`redivis`) {#redivis}

Dataset-native SaaS. The public OpenAPI spec does not need a token; **listing datasets does**. Filter exports on `software.id = 'redivis'`. Org name is the `{org}` subdomain (`stanford.redivis.com` → `stanford`).

```text
GET https://host/api/v1/openapi.json
GET https://redivis.com/api/v1/organizations/{org}/datasets?maxResults=100
```

Page with `pageToken`. Keep `dataset.list` rows (`kind` / dataset name). Drop workflows, notebooks, members, and individual **tables** when a parent dataset exists. A Bearer token with the `public` scope is required for the list URL; stop on `401`/`403`. Do not crawl `redivis.com` globally or a single `/ORG/dataset-name` landing page. Discovery: [discovery-scientific.md](discovery-scientific.md#redivis).

**Keep:** `dataset.list` rows. **Drop:** workflows, notebooks, members, and individual **tables** when a parent dataset exists.

## Yoda (`yoda`) {#yoda}

Utrecht / SURF research-data vault on iRODS. Filter exports on `software.id = 'yoda'`.

```text
GET https://host/oai/oai?verb=Identify
```

**Keep:** **published** vault datasets (DataCite DOI landing pages or the public catalog API in `endpoints[]`). **Drop:** `/research/` collaboration collections, iRODS tickets, and every file in a vault package. Stop on `401`.

## DLCM (`dlcm`) {#dlcm}

swissuniversities OAIS stack. Filter exports on `software.id = 'dlcm'`. Prefer `endpoints[]` OAI-PMH on the access module.

```text
GET https://access.host/oai-info/oai-provider/oai?verb=Identify
GET https://access.host/oai-info/oai-provider/oai?verb=ListRecords&metadataPrefix=oai_dc
```

Keep deposited **datasets** and their DOIs. Follow resumption tokens. Drop the Angular UI chrome, WordPress marketing pages (`olos.swiss`), and login-only OAI. Discovery: [discovery-scientific.md](discovery-scientific.md#dlcm).

**Keep:** deposited **datasets** and their DOIs (OAI on the access module). **Drop:** Angular UI chrome, WordPress marketing, and login-only OAI.

## easydb (`easydb`) {#easydb}

Programmfabrik easydb 5 / fylr. Filter exports on `software.id = 'easydb'`. There is usually **no** public dataset-list API; `/api/v1/session` is session metadata, not a catalog dump.

Harvest the public object/search UI the catalog `link` points at (or a documented public search export if present). Keep collection objects that are datasets or media catalog records. Drop login-walled objects and session JSON. Stop on `401`. Discovery: [discovery-scientific.md](discovery-scientific.md#easydb).

**Keep:** collection objects that are datasets or media catalog records. **Drop:** login-walled objects and `/api/v1/session` JSON.

## LabKey Server (`labkey`) {#labkey}

```text
GET https://host/login/begin.view
```

Keep **studies / published folders** (Panorama Public libraries, Open Research Portal projects). Drop assay run rows and a single `begin.view` folder as a seed. Stop on `401`.

**Keep:** **studies / published folders**. **Drop:** assay run rows and a single `begin.view` folder as a seed.

## Synapse (`synapse`) {#synapse}

```text
GET https://repo-prod.prod.sagebase.org/repo/v1/entity/synNNNN/children
```

Keep **projects and tables/files that are cited as datasets**. Drop every child file under a project when a parent dataset entity exists. Prefer the catalog `link` origin and `endpoints[]`. Stop on `401`.

**Keep:** **projects and tables/files cited as datasets**. **Drop:** every child file under a project when a parent dataset entity exists.

## Gen3 (`gen3`) {#gen3}

Data-commons portal. Prefer `endpoints[]` (Indexd, DRS, GraphQL). Defaults:

```text
GET https://host/_status
GET https://host/index/ga4gh/drs/v1/service-info
```

Keep **studies / projects** from the public GraphQL or portal catalog. Drop individual DRS objects, files, and Fence `/user/login` as harvest seeds. Stop on `401`/`403`. Do not harvest NCI GDC/PDC/IDC under this recipe.

**Keep:** **studies / projects** from public GraphQL or the portal catalog. **Drop:** individual DRS objects, files, and Fence login as harvest seeds.

## XNAT (`xnat`) {#xnat}

```text
GET https://host/data/projects
GET https://host/xnat/data/projects
```

Keep **projects** (and experiment collections when the user asked). Drop individual imaging sessions and DICOM files when a parent project exists. Stop on `401`.

**Keep:** **projects** (and experiment collections when asked). **Drop:** individual imaging sessions and DICOM files when a parent project exists.

Type `/data/projects` as `xnat:projects`.

## Shanoir (`shanoir`) {#shanoir}

```text
GET https://host/shanoir-ng/welcome
```

Keep **studies / datasets** listed on the public instance. Drop individual imaging examinations, DICOM files, and the Inria project homepage. Stop on `401`/`403`. One harvest scope per public Shanoir instance (Neurinfo, OFSEP, …).

**Keep:** public **studies / datasets**. **Drop:** individual imaging examinations, DICOM files, and the Inria project homepage.

## LORIS (`loris`) {#loris}

```text
GET https://host/
```

Keep **published instruments / imaging collections / datasets** on the public portal. Drop candidate pages, visit forms, and `demo.loris.ca`. Stop on `401`/`403`. One harvest scope per public LORIS instance.

**Keep:** published instruments / imaging collections / datasets. **Drop:** candidate pages, visit forms, and `demo.loris.ca`.

## OMERO (`omero`) {#omero}

```text
GET https://host/api/v0/m/projects/
GET https://host/webclient/
```

Keep **projects / screens / studies** (IDR annotations). Drop individual images and wells. Some public archives return `404` on `/api/v0/m/` — fall back to the documented webclient catalog. Stop on `401`.

Type `/api/v0/m/projects/` as `omero:projects`. Fall back `/webclient/` as `omero:webclient`.

**Keep:** **projects / screens / studies**. **Drop:** individual images and wells.

## Kadi4Mat (`kadi4mat`) {#kadi4mat}

```text
GET https://host/api/records
GET https://host/api/collections
```

Keep **records and collections**. Drop individual file blobs when a parent record exists. Stop on `401`.

Type `/api/records` as `kadi4mat:records` and `/api/collections` as `kadi4mat:collections`.

**Keep:** **records and collections**. **Drop:** individual file blobs when a parent record exists.

## TR32DB (`tr32db`) {#tr32db}

`/site/index.php` Cologne CRC databases. Harvest the public **metadata / dataset search** if unauthenticated. Do not scrape file blobs or require project login. One harvest scope per CRC database (TR32, CRC1211, TRR228). Distinct from CRC806DB.

```text
GET https://host/site/index.php
```

**Keep:** public **metadata / dataset search**. **Drop:** file blobs and project-login walls.

## e!DAL (`edal`) {#edal}

```text
GET https://host/
```

Keep versioned **DOI datasets**. Drop a single landing page as a crawl seed. Prefer the documented e!DAL API in `endpoints[]`. Stop on `401`.

**Keep:** versioned **DOI datasets**. **Drop:** a single landing page as a crawl seed.

## NOMAD (`nomad`) {#nomad}

```text
GET https://host/prod/v1/api/v1/info
GET https://host/prod/v1/api/v1/entries
```

Keep **uploads / entries** that are published datasets. Drop individual calculation files and parser logs. One Oasis or the central archive = one harvest scope. Stop on `401`.

Type `/prod/v1/api/v1/info` and `/prod/v1/api/v1/entries` as `rest`.

**Keep:** published **uploads / entries**. **Drop:** individual calculation files and parser logs.

## dLibra (`dlibra`) {#dlibra}

Polish digital library. Most installs expose Identify at `/dlibra/oai-pmh-repository.xml?verb=Identify` (catalog links that already end in `/dlibra` are stripped before that path is attached).

```text
GET https://host/dlibra/oai-pmh-repository.xml?verb=Identify
```

**Keep:** OAI-PMH records with a dataset / dane `set` or `dc:type` filter ([harvest-protocols.md](harvest-protocols.md#oai-pmh)). **Drop:** manuscript/photo libraries that were never accepted as dataset catalogs, and unfiltered ListRecords.

## Dataset-native platforms (short)

Little publication noise. Still skip non-dataset objects.

| Platform | List | Notes |
|----------|------|-------|
| Dataverse | [above](#dataverse) | `type=dataset` only |
| SciCat (`scicat`) | [harvest-earthdata.md](harvest-earthdata.md#scicat) | Facility datasets; stop on `401` |
| RADAR (`radar`) | [above](#radar) | Already datasets; skip marketing and single landings |
| Yoda (`yoda`) | [above](#yoda) | Published datasets only; skip the authenticated vault |
| LabKey (`labkey`) | [above](#labkey) | Studies / published folders |
| Synapse (`synapse`) | [above](#synapse) | Projects and dataset entities, not every file |
| XNAT (`xnat`) | [above](#xnat) | Projects, not sessions |
| Shanoir (`shanoir`) | [above](#shanoir) | Studies, not imaging sessions |
| LORIS (`loris`) | [above](#loris) | Published collections, not candidate visits |
| OMERO (`omero`) | [above](#omero) | Projects/screens, not images |
| Kadi4Mat (`kadi4mat`) | [above](#kadi4mat) | Records and collections |
| e!DAL (`edal`) | [above](#edal) | DOI datasets |
| NOMAD (`nomad`) | [above](#nomad) | Published entries/uploads |

Domain stacks (IPT, THREDDS, Breedbase, ESGF, …): [harvest-scientific-domain.md](harvest-scientific-domain.md). Omeka S and CONTENTdm: sections above.

## Pagination checklist

1. Read `total` / `nHits` / `page.totalPages` / OAI `resumptionToken` from the first response.
2. Cap page size; do not request `size=10000` on Solr-backed IRs.
3. Deduplicate on DOI, handle, or native id plus catalog `uid` ([harvest-identifiers.md](harvest-identifiers.md)). Emit [output records](harvest-output.md).
4. Re-run with `from=` (OAI) or `updated` sort for incremental harvests when the API supports it ([harvest-incremental.md](harvest-incremental.md)).

## FLAT (`flat`) {#flat}

Start at the registered repository and use the advertised OAI-PMH endpoint. For Lund:

```text
GET https://host/flat/oai2?verb=Identify
```

Typical catalog links already end in `/flat/`. Cleanup strips that mount so Identify is not doubled (`/flat/flat/`).

Enumerate metadata formats and sets before ListRecords; prefer CMDI when offered, otherwise a supported descriptive format. Follow resumption tokens and preserve repository identifiers and collection membership.

Keep deposited language-resource collections, corpora and dataset metadata. Exclude navigation
nodes, user profiles and individual media files as independent datasets. Public metadata does
not imply that restricted audio or video is downloadable. The
[FLAT source documentation](https://github.com/TLA-FLAT/FLAT) describes its Fedora/Islandora
components; administrative Fedora endpoints are not public harvesting seeds.

**Keep:** deposited language-resource collections, corpora, and dataset metadata. **Drop:** navigation nodes, user profiles, and individual media files as independent datasets.

## openEQUELLA (`openequella`) {#openequella}

Start at the registered institution's repository and its advertised OAI-PMH or REST search
interface. For RADAR: `GET https://radar.brookes.ac.uk/radar/oai?verb=Identify`.
Enumerate metadata formats and sets, then use ListRecords with resumption tokens.
[Apereo's product description](https://archived.apereo.org/projects/openequella)
documents OAI and REST interfaces; authentication and route prefixes vary by institution.

Keep dataset/research-resource metadata and attached resource links. Exclude teaching objects,
publication-only records and administrative collections when harvesting research datasets.
An item can have several versions and files; preserve its stable identifier and version
without counting every attached file as a new dataset.

**Keep:** dataset / research-resource metadata and attached resource links. **Drop:** teaching objects, publication-only records, and every attached file as a new dataset.

## Aubrey (`aubrey`) {#aubrey}

Start at the registered collection, such as
`GET https://digital.library.unt.edu/explore/collections/UNTDRD/`, and follow its API link.
[Official API guidance](https://digital.library.unt.edu/api/) documents collection-scoped
interfaces and OAI-PMH formats `untl` and `oai_dc`. Resolve the exact collection scope from
that help page instead of harvesting all historical materials in the library.

Keep deposited datasets and their ARK identifiers, collection relationships and resource links.
Follow OAI resumption tokens; exclude page images, IIIF tiles, navigation pages and non-data
historical collections from dataset output. The metadata service is publicly documented;
resource reuse rights still vary by item.

**Keep:** deposited datasets and their ARK identifiers. **Drop:** page images, IIIF tiles, navigation pages, and non-data historical collections.

## Dialnet CRIS (`dialnetcris`) {#dialnetcris}

Start at the registered institutional portal. La Rioja exposes
`GET https://investigacion.unirioja.es/oai/openaire?verb=Identify`.
Enumerate the actual metadata formats and available sets before harvesting records.
The [provider's product page](https://fundaciondialnet.unirioja.es/servicios/dialnet-cris/)
describes an additional REST export service; do not assume that this service is public on
every tenant or invent its URL.

Keep explicitly typed datasets and their metadata/resource links. Drop researcher profiles,
projects, indicators and publication-only entries from a dataset harvest. A CRIS record may
link to a deposit in another repository: preserve that relationship instead of counting the
same dataset twice. The presence of a CRIS platform does not prove that every tenant contains
datasets; return an empty dataset result if the available records are only publications.

**Keep:** explicitly typed **datasets** and their metadata/resource links. **Drop:** researcher profiles, projects, indicators, and publication-only entries.

## Related

- [harvest.md](harvest.md)
- [harvest-opendata.md](harvest-opendata.md)
- [harvest-geoportals.md](harvest-geoportals.md)
- [harvest-scientific-domain.md](harvest-scientific-domain.md)
- [discovery-scientific.md](discovery-scientific.md)
- [harvest-protocols.md](harvest-protocols.md)
- [harvest-biodiversity.md](harvest-biodiversity.md)
- [harvest-earthdata.md](harvest-earthdata.md)
- [harvest-incremental.md](harvest-incremental.md)
- [harvest-identifiers.md](harvest-identifiers.md)
- [harvest-output.md](harvest-output.md)
- [apidetect.md](apidetect.md)
- [agents/harvest.md](agents/harvest.md)
