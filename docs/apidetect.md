# API endpoint detection (`apidetect.py`)

Fill `endpoints[]` on catalog YAML after the record exists. The script GETs known URL templates for a `software.id` and writes types/URLs that respond.

This is **enrichment**, not discovery and not a dataset crawl. Find catalogs with [discovery.md](discovery.md); add YAML with [cli.md](cli.md); then optionally run apidetect. To list datasets inside a catalog, use [harvest.md](harvest.md).

Do not treat `scripts/apidetect_urlmaps_draft.py` as a CLI. Draft maps are merged into `CATALOGS_URLMAP` inside `apidetect.py` at import time.

## When to run

- After adding or retagging a catalog whose `software.id` has a URL map
- When quality reports `MISSING_ENDPOINTS` and `api: true`
- In `--dryrun` first; write YAML only when probes match the live site

Skip software IDs with no map (including most `custom` records). Guessing endpoint paths by hand is worse than leaving `endpoints` empty.

## Commands

From the repository root:

```bash
python scripts/apidetect.py detect-single catalogdatagov --dryrun
python scripts/apidetect.py detect-single cdi00001616 --dryrun
python scripts/apidetect.py detect-software ckan --dryrun
python scripts/apidetect.py detect-software ckan --max-endpoints 1 --dryrun
python scripts/apidetect.py detect-country US --dryrun
python scripts/apidetect.py detect-cattype "Open data portal" --dryrun
```

`--dryrun` prints planned endpoints and does not write YAML. Omit it to insert. `--action insert` is the default; use the script `--help` for replace behaviour.

`--mode entries` (default) walks `data/entities/`. Use `--mode scheduled` for unverified files.

`detect-all` walks every mapped `software.id` — too heavy for a normal contribution; prefer `detect-single` or `detect-software`.

## Software IDs with URL maps

Maps exist for the IDs in `CATALOGS_URLMAP` (built-in plus draft merge from `apidetect_urlmaps_draft.py`). The [software index](software-index.md) `apidetect` column is `yes` when a map exists. High-traffic examples:

| Area | `software.id` |
|------|----------------|
| Open data | `ckan`, `dkan`, `opendatasoft`, `socrata`, `udata`, `magda`, `jkan`, `junar`, `entryscape`, `drupal`, `wordpress`, `triplydb`, `piveau`, `idra`, `resourcecontracts`, `gisopendataportal`, `datafair`, `lkod`, `ouropendata`, `dataeye`, `opengov`, `odweb`, `atmmaggioli`, `simaiopendata` |
| Geo | `geonetwork`, `geonode`, `geoserver`, `arcgishub`, `arcgisserver`, `pycsw`, `pygeoapi`, `mapproxy`, `qwc2`, `mapstore`, `lizmap`, `mapbender`, `geomapfish`, `getsdiportal`, `terria`, `gvsigonline`, `erdasapollo`, `wis20box`, `koordinates`, `nextgisweb`, `tianditu`, `openeo`, `isogeo`, `mapgisigserver`, `cubewerx`, `haleconnect`, `palapa`, `stacbrowser`, `qgisserver`, `deegree`, `gc2`, `micka`, `supermapiportal`, `g3wsuite`, `geonature`, `hajk`, `tergis`, `geocortex`, `activemapgis`, `opendatacube`, `datacubews`, `origo` |
| Scientific | `dataverse`, `dspace`, `invenio`, `inveniordm`, `eprints`, `hyrax`, `opus`, `esploro`, `pure`, `weko3`, `elsevierdigitalcommons`, `opendap`, `opendaphyrax`, `thredds`, `erddap`, `ipt`, `galaxy`, `ala`, `figshare`, `redivis`, `radar`, `breedbase`, `tripal`, `veupathdb`, `massbank`, `iochembd`, `esgf`, `omekas`, `contentdm`, `symbiota`, `frostserver`, `cbioportal`, `bexis2`, `intermine`, `kadi4mat`, `omero`, `xnat`, `wikibase`, `huggingface`, `openalex`, `idigbio`, `inaturalist`, `clld`, `minerva`, `aubrey`, `gringlobal`, `synapse`, `yoda`, `dataone`, `codalab`, `tr32db` |
| Indicators / microdata | `pxweb`, `pxstat`, `opensdg`, `statsuite`, `istatdatabrowser`, `sdmxri`, `nada`, `nesstar`, `redatam`, `colectica`, `obibamica`, `knoema`, `dhis2`, `edatos`, `superset`, `dgbasweb`, `swing`, `ibisph`, `superstar`, `duva`, `beyond2020` |
| Metadata | `fusionregistry`, `aristotlemdr`, `mwmb`, `fairdatapoint`, `datahubproject` |

If `detect-single` reports no map for the ID, stop. Do not copy URLs from a different platform. Most map-viewer IDs and BI/query UIs are listed in `NO_STANDARD_PROBE` (`apidetect_urlmaps_draft.py`); the [software index](software-index.md) shows `—` for those IDs.

## After a successful run

1. `python scripts/builder.py validate-yaml --id` for that catalog `id`
2. Set `api` / `api_status` together when an API is confirmed ([data-model.md](data-model.md))
3. Prefer endpoint `type` values already used for that `software.id` ([vocabularies.md](vocabularies.md#endpoint-types))

## Related

- [cli.md](cli.md)
- [harvest.md](harvest.md) (dataset crawl recipes; not this script)
- [liveness.md](liveness.md) (URL reachability of `link`, not API maps)
- [architecture.md](architecture.md)
- [quality-rules.md](quality-rules.md)
