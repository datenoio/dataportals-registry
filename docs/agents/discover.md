# Agent guide: discovering catalogs

Find catalog installations that are **not yet in this registry**, then hand off to [contribute.md](contribute.md). Human narrative: [discovery.md](../discovery.md). Search-engine and per-platform queries: [discovery-search-tools.md](../discovery-search-tools.md).

This is **not** the query workflow. To look up existing records, use [query.md](query.md). To list datasets *inside* a catalog, use [harvest.md](harvest.md).

## Goal

Produce a short list of verified candidate URLs with:

- `name`, `link`
- proposed `catalog_type` and `software.id`
- ISO country (and subregion when the owner is regional/local)
- whether the site already exists in exports

Do not invent `uid`. Do not add dataset-level records. Do not implement production search APIs here.

## Before probing the web

1. Read [llms.txt](https://github.com/datenoio/dataportals-registry/blob/main/llms.txt) if you have not already.
2. Duplicate-check **exports** (`data/datasets/datasets.duckdb` or `full.parquet`), then `data/scheduled/` if present.
3. If the user named a URL or domain, search that first and stop if it is already registered.

```sql
SELECT id, uid, name, link, catalog_type, status,
       software.id AS software_id
FROM catalogs
WHERE lower(link) LIKE '%example.gov%'
   OR id = 'examplegov';
```

Match on hostname, not display name. `id` is not a URL.

## Discovery order

1. **Vendor and government lists** in [discovery.md](../discovery.md) — highest yield, fewest false positives.
2. **Vendor lists and Graph dumps** (preview only until the user wants files written):

   ```bash
   python scripts/sync_ckan_ecosystem.py --dry-run
   python scripts/extract_openaire_portals.py list-sources --output /tmp/openaire_sources.json
   ```

3. **Targeted search** the user asked for (one country, one software, one city, or one named list URL). Use local-language open-data terms and government TLDs. Query recipes: [discovery-search-tools.md](../discovery-search-tools.md) and the platform guides ([opendata](../discovery-opendata.md), [geoportals](../discovery-geoportals.md), [scientific](../discovery-scientific.md) ([domain](../discovery-scientific-domain.md)), [metadata](../discovery-metadata.md), [indicators](../discovery-indicators.md)). Software ID → page: [software-index.md](../software-index.md). Hunt-pattern table: [discovery.md](../discovery.md#hunt-patterns).
4. **Endpoint probes** on the candidate host only (table below). GET, short timeout, public URLs.

You MAY run documented Google / Censys / Shodan / FOFA queries when the user asked to discover catalogs and the scope is a country, software, city, TLD, or a named directory URL. Do not write internet-wide scanners, recursive crawlers, or unscoped sweeps in this repository. Still duplicate-check exports before probing live hosts.

## Hunt types {#hunt-types}

Match the user prompt to one of these loops. Do not mix them in the same pass.

### Software instance {#software-instance}

```text
Which {software} catalogs are missing?
```

Read the software YAML and [software-index.md](../software-index.md) row. `SELECT link FROM catalogs WHERE software.id = '{id}'`. Fetch the vendor list or hostname pattern (not a scanner). Probe fingerprints. One record per public tenant, not a second copy of the same hub (PISO geoprostor.net, SeaSketch marketing home, GISApp REST adaptor).

### National harvest sources {#national-harvest-sources}

```text
Which data sources harvested by {national portal} are missing?
```

Use the portal’s harvest / organisations / catalogues API (data.gouv.fr, govdata.de, datos.gob.es, data.go.kr, data.gov.ru, opendata.swiss, dane.gov.pl, data.go.id, search.open.canada.ca). Match origin hostnames to exports. Probe the **origin catalog UI**, not the harvest-source row inside the national CKAN.

**Accept:** independent CKAN / GeoNetwork / Hub / agency `/opendata` list. **Reject:** XML dataset feeds and developer price files (dane.gov.pl had thousands of those), slices of the same national catalog (opendata.swiss geocat/I14Y), scientific IR dumps already registered, login walls. Full recipe: [discovery-opendata.md](../discovery-opendata.md#national-harvest-sources).

### Country university IRs {#country-university-irs}

```text
There are a lot of {country} universities and research organizations that could have scientific data repositories that are not yet listed. Which of them are missing?
```

Count existing `scientific/` YAML for that ISO folder first. Sources: OpenDOAR country facet, ROAR, re3data, OpenAIRE Graph, national IR aggregators (IRDB Japan, DABAR, OpenScience.si, Scholaris). Probe DSpace `/server/api` or OAI Identify.

**Accept** only IRs that **list datasets** (DSpace Dataset type browse, Dataverse, a research-data community). Publication-only IRs were later removed (Kazakhstan). Skip microstates with no universities. Recipe: [discovery-scientific.md](../discovery-scientific.md#country-university-irs).

### Country indicators {#country-indicators}

```text
Which {country} indicators catalogs are missing?
```

Count existing `indicators/` YAML. Hunt the **missing product**, not another IMF NSDP: native NSO table DB (PxWeb, .Stat, STATcube, custom), health (DHIS2, TabNet, HCI, Cancer-Rates), education/labour explorers, SDG, central bank, subnational.

**Reject:** PDF publications, CMS homepages, login dashboards, agency PxWeb already on the national StatBank, open-data APIs that are not indicator catalogs. `is_national: true` only for the official NSO product of that type. Recipe: [discovery-indicators.md](../discovery-indicators.md#country-indicators-hunt).

### Named directory {#named-directory}

```text
Which data catalogs from {list URL} are missing?
```

One bounded list per session: ODIS, CoreTrustSeal, STAC Index, WIS2 GDC, GeoNetwork/GeoNode galleries, CLARIN/VLO, PANGAEA harvest sources, FGDC SSC, MappingSupport, Geoseer. Duplicate-check hostname; probe live; skip preservation systems with no dataset catalog (CoreTrustSeal SPAR/EWIG) and org homepages (many PANGAEA harvest sources).

### Custom-software review {#custom-software-review}

```text
Review custom {geoportals|indicators|scientific} catalogs and identify new software definitions
```

Cluster remaining `software.id: custom` by hostname or path. Add a software YAML only when ≥3 independent installations share a product, then retag those rows in the same change. One-off national `.gov` roots stay `custom`.

## Software probes

Set `software.id` only when a probe or page signal matches **and** that id exists in `data/software/` (see `software_ids.yaml`). Otherwise `custom`. Full map of IDs to fingerprints: [software-index.md](../software-index.md). Definitions: [software-taxonomy.md](../software-taxonomy.md).

Do not paste long GET recipes here — open the index row, then the discovery heading.

| If you see | `software.id` | Typical type |
|------------|---------------|--------------|
| `/api/3/action/status_show` | `ckan` | Open data portal |
| `/api/explore/v2.1/catalog/datasets` | `opendatasoft` | Open data portal |
| `/api/views` (SODA) | `socrata` | Open data portal |
| `/srv/eng/csw` or `/srv/api` | `geonetwork` | Geoportal |
| `/geoserver/ows` GetCapabilities | `geoserver` | Geoportal |
| ArcGIS Hub search / `opendata.arcgis.com` | `arcgishub` | Geoportal or Open data portal |
| `/arcgis/rest/info?f=pjson` | `arcgisserver` | Geoportal |
| STAC `/collections` JSON | `stacserver` | Geoportal |
| `/api/info/version` | `dataverse` | Scientific data repository |
| DSpace `/server/api` or `/xmlui` | `dspace` | Scientific data repository |
| `/api/records?size=1` InvenioRDM | `inveniordm` | Scientific data repository |
| `/api/v1/` PxWeb tables | `pxweb` | Indicators catalog |
| `PxStat.Data.Cube_API` / “PxStat Open Data Platform” | `pxstat` | Indicators catalog |
| `/databrowserhub/api/core` or `/databrowser/api/core` hub JSON | `istatdatabrowser` | Indicators catalog |
| Title “TabNet Win32” / `deftohtm.exe` / `cgi-bin/dh` | `tabnet` | Indicators catalog |
| `fenixservices.fao.org` / FAOSTAT API / CountrySTAT FENIX UI | `fenix` | Indicators catalog |
| Finnish `/IMS/` karttapalvelu (`tekla-mvc-common`) | `trimblelocus` | Geoportal |
| SpatialMap `webkort` | `spatialsuite` | Geoportal |
| Hajk `appConfig.json` / `mapserviceBase` | `hajk` | Geoportal |
| `drift.kortinfo.net/Map.aspx` | `kortinfo` | Geoportal |
| `portals.landfolio.com` cadastre map | `landfolio` | Geoportal |
| G3W-CLIENT `/map/{group}/` | `g3wsuite` | Geoportal |
| MapCentia `/apps/viewer` or `/mapcache/` WMTS | `gc2` | Geoportal |
| hale»connect `/csw` or `/ows/services/` | `haleconnect` | Geoportal |
| `*.sentinel-hub.com` STAC `/api/v1/catalog` | `sentinelhub` | Geoportal |
| `*.revenuedev.org` license portal | `rdfrepository` | Open data portal |
| ResourceContracts `/contract/resources` | `resourcecontracts` | Open data portal |
| `{city}.data.gxzf.gov.cn` | `gxopendata` | Open data portal |
| `/openapi.json` + `/api/datasets` JSON:API (`type: dataset`) | `opengdc` | Open data portal |
| SparkMap / All Things hub | `sparkmap` | Indicators catalog |
| Clarivate Converis CRIS | `converis` | Scientific data repository |
| `begin.view` / Panorama Public / LabKey | `labkey` | Scientific data repository |
| Sage Bionetworks / `synapse.org` | `synapse` | Scientific data repository |
| `/xnat/` or `/data/projects` | `xnat` | Scientific data repository |
| OMERO `/webclient/` or IDR | `omero` | Scientific data repository |
| Kadi4Mat `/api/records` | `kadi4mat` | Scientific data repository |
| `/prod/v1/api/v1/info` NOMAD Oasis | `nomad` | Scientific data repository |
| InterMine `/begin.do` / `/service/version` | `intermine` | Scientific data repository |
| `/gringlobal/` accession search | `gringlobal` | Scientific data repository |
| `{project}.birdmap.africa` pentad atlas | `birdmap` | Scientific data repository |
| `{bank}.talkbank.org` CHAT corpus browser | `talkbank` | Scientific data repository |
| `/do/{uuid}` + strawberryfield / “indexed Digital Objects” | `archipelago` | Scientific data repository |
| `{org}.redivis.com` / OpenAPI titled Redivis | `redivis` | Scientific data repository |
| PlutoF workbench (`api.plutof.ut.ee`) | `plutof` | Scientific data repository |
| MycoCosm / Phytozome / JGI Genome Portal | `jgi` | Scientific data repository |
| cBioPortal `/api/info` `portalVersion` | `cbioportal` | Scientific data repository |
| ESA TAP `/tap/capabilities` | `esasciencearchive` | Scientific data repository |
| path `/odweb/` 公共数据开放平台 | `odweb` | Open data portal |
| “National Summary Data Page” + SDMX XML | `imfnsdp` | Indicators catalog |
| Two fingerprints fail | `custom` | Primary UI type |

Same-host collision (GeoNetwork+GeoServer, viewer+QGIS Server): [discovery.md](../discovery.md#one-catalog-per-public-product). Types: [catalog-types.md](../catalog-types.md).

After a YAML file exists, optional endpoint fill:

```bash
python scripts/apidetect.py detect-single catalogdatagov --dryrun
```

See [apidetect.md](../apidetect.md). Do not run `apidetect_urlmaps_draft.py` as a CLI.

## Accept / reject

**Accept** when all are true:

- Public HTTP(S) catalog UI or harvestable API
- Not a duplicate of `link` / same host catalog already in entities or scheduled
- Country (and subregion) can be determined from the owner
- Software is known or explicitly `custom`

**Reject** (do not add):

- Demo, template, or documentation-only sites
- Single file downloads with no catalog
- Sites that require authentication for any catalog listing
- Dataset records, CKAN packages, STAC items (out of scope)
- Guessed software IDs

## After a valid find

1. `python scripts/builder.py add-single URL --scheduled` (preferred) or write YAML per [contribute.md](contribute.md).
2. `python scripts/builder.py assign`
3. `python scripts/builder.py validate-yaml --id` for that catalog id
4. Cite `id` + `link` in the reply. List skipped duplicates with their existing `id`.

## Do not

- Walk `data/entities/**/*.yaml` to search; use exports
- Hand-edit `data/datasets/`
- Bypass `401`/`403`, guess API keys, or follow login forms
- Flood a host; one or two GETs per path is enough
- Commit generated dumps unless the user asked for a rebuild

## Related

- [discovery.md](../discovery.md) — overview, lists, [hunt patterns](../discovery.md#hunt-patterns)
- [discovery-search-tools.md](../discovery-search-tools.md)
- [discovery-agent-tools.md](../discovery-agent-tools.md)
- [discovery-opendata.md](../discovery-opendata.md) / [discovery-geoportals.md](../discovery-geoportals.md) / [discovery-scientific.md](../discovery-scientific.md) ([domain](../discovery-scientific-domain.md)) / [discovery-metadata.md](../discovery-metadata.md) / [discovery-indicators.md](../discovery-indicators.md) / [discovery-other.md](../discovery-other.md)
- [software-index.md](../software-index.md)
- [apidetect.md](../apidetect.md) / [liveness.md](../liveness.md)
- [contribute.md](contribute.md)
- [improve.md](improve.md) — what to hunt next (coverage gaps, session patterns)
- [query.md](query.md)
- [cli.md](../cli.md)
