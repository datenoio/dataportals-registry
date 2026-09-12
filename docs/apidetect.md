# API endpoint detection (`apidetect.py`)

Fill `endpoints[]` on catalog YAML after the record exists. The script GETs known URL templates for a `software.id` and writes types/URLs that respond.

This is **enrichment**, not discovery and not a dataset crawl. Find catalogs with [discovery.md](discovery.md); add YAML with [cli.md](cli.md); then optionally run apidetect. To list datasets inside a catalog, use [harvest.md](harvest.md).

Do not treat `scripts/apidetect_urlmaps_draft.py` as a CLI. Draft maps are merged into `CATALOGS_URLMAP` inside `apidetect.py` at import time.

## When to run

- After adding or retagging a catalog whose `software.id` has a URL map
- When quality reports `MISSING_ENDPOINTS` and `api: true`
- In `--dryrun` first; write YAML only when probes match the live site

Skip software IDs with no map. Do **not** guess dump paths by hand. `custom` catalogs are skipped by quality fixers and by detect CLI unless you pass `--include-custom`.

Harvestable dumps (DCAT `/data.json`, `/catalog.xml`, `/catalog.rdf`, OAI-PMH, CSW, SPARQL) are written to `endpoints[]`. Do not use `catalog_export`.

## Commands

From the repository root:

```bash
python scripts/apidetect.py detect-single catalogdatagov --dryrun
python scripts/apidetect.py detect-single cdi00001616 --dryrun
python scripts/apidetect.py detect-software ckan --dryrun
python scripts/apidetect.py detect-software ckan --max-endpoints 1 --dryrun
python scripts/apidetect.py detect-software ckan --action update --dryrun
python scripts/apidetect.py detect-software custom --include-custom --dryrun
python scripts/apidetect.py detect-country US --dryrun
python scripts/apidetect.py detect-cattype "Open data portal" --dryrun
```

`--workers` (default 8) runs catalog jobs in parallel. `--probe-workers` (default 8) runs URL-map HTTP probes for one catalog in parallel. Use `--workers 1 --probe-workers 1` to restore sequential behaviour. `detect-single` looks up `{id}.yaml` by filename first instead of walking every entity file.

`--dryrun` prints planned endpoints and does not write YAML. Omit it to insert. `--action insert` is the default and **skips records that already have endpoints**. Use `--action update` to add newly mapped protocols (OAI, DCAT RDF, SPARQL, TAP, OData) without replacing existing URLs.

`--include-custom` is required to probe `software.id: custom` with the dump map (`/catalog.xml`, OAI-PMH, CSW, SPARQL, …). Quality fixers never set this flag.

`--mode entries` (default) walks `data/entities/`. Use `--mode scheduled` for unverified files.

`detect-all` walks every mapped `software.id` — too heavy for a normal contribution; prefer `detect-single` or `detect-software`.

## Software IDs with URL maps

Maps exist for the IDs in `CATALOGS_URLMAP` (built-in plus draft merge from `apidetect_urlmaps_draft.py`). The [software index](software-index.md) `apidetect` column is `yes` when a map exists. High-traffic examples:

| Area | `software.id` |
|------|----------------|
| Open data | `ckan`, `dkan`, `opendatasoft`, `socrata`, `udata`, `magda`, `jkan`, `junar`, `entryscape`, `drupal`, `wordpress`, `triplydb`, `piveau`, `idra`, `resourcecontracts`, `gisopendataportal`, `datafair`, `lkod`, `ouropendata`, `dataeye`, `opengov`, `odweb`, `atmmaggioli`, `simaiopendata`, `bitrix`, `gipuzkoairekia` |
| Geo | `geonetwork`, `geonode`, `geoserver`, `arcgishub`, `arcgisserver`, `pycsw`, `pygeoapi`, `mapproxy`, `qwc2`, `mapstore`, `lizmap`, `mapbender`, `geomapfish`, `getsdiportal`, `terria`, `gvsigonline`, `erdasapollo`, `wis20box`, `koordinates`, `nextgisweb`, `tianditu`, `openeo`, `isogeo`, `mapgisigserver`, `cubewerx`, `haleconnect`, `palapa`, `stacbrowser`, `qgisserver`, `deegree`, `gc2`, `micka`, `supermapiportal`, `g3wsuite`, `geonature`, `hajk`, `tergis`, `geocortex`, `activemapgis`, `opendatacube`, `datacubews`, `origo`, `esrigeo` |
| Scientific | `dataverse`, `dspace`, `invenio`, `inveniordm`, `eprints`, `hyrax`, `opus`, `esploro`, `pure`, `weko3`, `elsevierdigitalcommons`, `opendap`, `opendaphyrax`, `thredds`, `erddap`, `ipt`, `galaxy`, `ramadda`, `ala`, `figshare`, `redivis`, `radar`, `breedbase`, `tripal`, `veupathdb`, `massbank`, `iochembd`, `esgf`, `omekas`, `contentdm`, `symbiota`, `frostserver`, `cbioportal`, `bexis2`, `intermine`, `kadi4mat`, `omero`, `xnat`, `wikibase`, `huggingface`, `openalex`, `idigbio`, `inaturalist`, `clld`, `minerva`, `aubrey`, `gringlobal`, `synapse`, `yoda`, `dataone`, `codalab`, `tr32db`, `vufind`, `librecat`, `islandora`, `archipelago`, `divaportal`, `icat`, `talkbank`, `materialscloud`, `phaidra`, `greenstone`, `dlibra` |
| Indicators / microdata | `pxweb`, `pxstat`, `opensdg`, `statsuite`, `istatdatabrowser`, `sdmxri`, `nada`, `nesstar`, `redatam`, `colectica`, `obibamica`, `knoema`, `dhis2`, `edatos`, `superset`, `dgbasweb`, `swing`, `ibisph`, `superstar`, `duva`, `beyond2020` |
| Metadata | `fusionregistry`, `aristotlemdr`, `mwmb`, `fairdatapoint`, `datahubproject` |

If `detect-single` reports no map for the ID, stop. Do not copy URLs from a different platform. Most map-viewer IDs and BI/query UIs are listed in `NO_STANDARD_PROBE` (`apidetect_urlmaps_draft.py`); the [software index](software-index.md) shows `—` for those IDs.

## After a successful run

1. `python scripts/builder.py validate-yaml --id` for that catalog `id`
2. Set `api` / `api_status` together when an API is confirmed ([data-model.md](data-model.md))
3. Prefer endpoint `type` values already used for that `software.id` ([vocabularies.md](vocabularies.md#endpoint-types)). TAP capabilities are `tap:capabilities`, DHuS product queries are `odata`, pygeoapi `/collections` is `ogc:features`, OpenDataSoft catalog APIs are `opendatasoftapi`, Data Fair is `datafairapi`, Our Open Data `/api/package_list` is `ouropendata:packages`, cBioPortal studies are `cbioportal:studies`, Hugging Face is `huggingface:api`, OMERO projects are `omero:projects`, SciCat lists are `scicat:datasets`, Kadi4Mat is `kadi4mat:records` / `kadi4mat:collections`, MyTardis dataset lists are `mytardis:datasets`, InterMine is `intermine:version`, XNAT project lists are `xnat:projects`, Dataverse version/search is `dataverseapi`, PxWeb is `pxwebapi`, eDatos / Superset / GC2 / Nextstrain / SEEK `/api` / MINERVA project lists / Islandora Solr Dataset select / PHAIDRA Dataset Solr select are `rest`, and VuFind / LibreCat / Archipelago Dataset search, Figshare `/articles/dataset/`, DiVA smash search, TalkBank `/data.html`, Materials Cloud `/explore`, ICAT `/icat/portlet/`, and GRIN-Global `/gringlobal/` are `index`. Palapa GeoServer WMS is `wms130`. Esri Geoportal CSW GetCapabilities is `csw202`. EPrints `/cgi/opensearchdescription`, GeoBlacklight `/catalog/opensearch.xml`, Micka `/opensearch`, TriplyDB `/opensearch.xml`, Socrata `/opensearch.xml`, GeoNode `/catalogue/opensearch`, and Esri Geoportal `/openSearchDescription` are `opensearch`. Piveau `/api/sparql` is `sparql`. DaCHS `/oai.xml`, hale»connect `/csw?mode=oaipmh`, dLibra `/dlibra/oai-pmh-repository.xml`, Elsevier `/oai`, WEKO3 `/oai`, pycsw `/?mode=oaipmh`, and LibreCat `/oai` Identify are `oaipmh20`. ArcGIS Hub `/data.json` and OpenDataSoft `/data.json` are `dcatus11`. SuperMap iPortal `/iportal/web/maps.json` and `/iportal/web/datas.json` are `supermapiportal:maps` / `supermapiportal:datas`. Gipuzkoa Irekia `/catalog.xml` is `dcat:xml`, `/catalog.rdf` is `dcatap`, `/catalog.jsonld` is `dcat:jsonld`, and `/api/feed/dcat` is `dcatap201`. DKAN `/jsonapi/dataset/dataset` is `drupal:jsonapi`. pygeoapi `/collections?f=json` is `ogc:features`. DataPress `/api/3/action/package_search` is `ckan:package-search`. VuFind `/api?openapi` and PHAIDRA `/api/openapi` are `openapi`.

## Related

- [cli.md](cli.md)
- [harvest.md](harvest.md) (dataset crawl recipes; not this script)
- [liveness.md](liveness.md) (URL reachability of `link`, not API maps)
- [architecture.md](architecture.md)
- [quality-rules.md](quality-rules.md)
