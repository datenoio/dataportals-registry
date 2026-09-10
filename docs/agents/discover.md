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
3. If DuckDB raises a lock error, query `data/datasets/full.parquet` instead. Do not walk YAML.
4. If the user named a URL or domain, search that first and stop if it is already registered.
5. If this is a software-instance hunt, check whether a prior session already exhausted that vendor list (0 missing is done).

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

Read the software YAML and [software-index.md](../software-index.md) row. `SELECT link FROM catalogs WHERE software.id = '{id}'`. Fetch the vendor list or hostname pattern (not a scanner). Optional: crt.sh for SaaS hosts (`%.pozi.com`, `%.giscloud.com`), then Censys or FOFA title/body if Google is silent ([FOFA as Censys alternative](../discovery-search-tools.md#fofa)). Probe fingerprints. One record per public tenant, not a second copy of the same hub (PISO geoprostor.net, SeaSketch marketing home, GISApp REST adaptor).

If the vendor list is exhausted and nothing new probes live, **stop and list 0 missing**. Do not invent extra cities.

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

One bounded list per session: ODIS, CoreTrustSeal, STAC Index, WIS2 GDC, GeoNetwork/GeoNode galleries, CLARIN/VLO, PANGAEA harvest sources, FGDC SSC, MappingSupport, Geoseer, Instant Apps Filter Gallery hosts. Duplicate-check hostname; probe live; skip preservation systems with no dataset catalog (CoreTrustSeal SPAR/EWIG) and org homepages (many PANGAEA harvest sources).

### Subnational municipal GIS {#subnational-municipal-gis}

```text
Which {country} cities and counties have geoportals that are missing?
```

Count existing `geo/` YAML first. Hunt the **product tenant list** for that country (e-mapa.net, GISPLAN, GisMaster, IntraMaps, SonicWeb, WebEWID), not every administrative unit. **Accept:** live public viewer. **Reject:** REST of an existing Hub, staff login GIS, marketplace demos, “all counties” guesses (Iran: only cities with a public ArcGIS / GeoServer / GeoNode UI). Saturated after v1.20.0: Poland e-mapa, Czech/Slovak GISPLAN/GEPRO/Mapotip, Italian GisMaster, Japanese WagMap/SonicWeb, Brazilian CTMGEO — skip unless a new gallery URL exists.

### Custom-software review {#custom-software-review}

```text
Review custom {geoportals|indicators|scientific} catalogs and identify new software definitions
```

Cluster remaining `software.id: custom` by hostname or path. Add a software YAML when ≥3 independent installations share a product, **or** a first-party product page / vendor deployment list names it (then run the instance hunt). One-off national `.gov` roots stay `custom`. Do not identify Argenmap from Leaflet alone, WebEWID from authenticated role portals, or ArcGIS Dashboards from pages outside `/apps/dashboards/`.

## Software probes

Set `software.id` only when a probe or page signal matches **and** that id exists in `data/software/` (see `software_ids.yaml`). Otherwise `custom`. Full map of IDs to fingerprints: [software-index.md](../software-index.md). Definitions: [software-taxonomy.md](../software-taxonomy.md).

Do not paste long GET recipes here — open the index row, then the discovery heading.

| If you see | `software.id` | Typical type |
|------------|---------------|--------------|
| `/api/3/action/status_show` | `ckan` | Open data portal |
| `/api/explore/v2.1/catalog/datasets` | `opendatasoft` | Open data portal |
| `/api/views` (SODA) | `socrata` | Open data portal |
| `/transparencia/datos/catalogo` Maggioli/Galileo | `atmmaggioli` | Open data portal |
| `{org}.opengov.com` /transparency | `opengov` | Open data portal |
| `/opendata/set/lkod` or lkod.cz catalog | `lkod` | Open data portal |
| `/srv/eng/csw` or `/srv/api` | `geonetwork` | Geoportal |
| Title “Geoportal Palapa” / `/main/` or `/gspalapa/` | `palapa` | Geoportal |
| Argenmap `src/js/app.js` / IGN template | `argenmap` | Geoportal |
| Title `WebEWID` / Portal Mapowy | `webewid` | Geoportal |
| `/geoserver/ows` GetCapabilities | `geoserver` | Geoportal |
| ArcGIS Hub search / `opendata.arcgis.com` | `arcgishub` | Geoportal or Open data portal |
| `/arcgis/rest/info?f=pjson` | `arcgisserver` | Geoportal |
| `experience.arcgis.com/experience/` or `jimu-core/init.js` | `experiencebuilder` | Geoportal |
| `/apps/webappviewer/index.html?id=` | `webappbuilder` | Geoportal |
| STAC `/collections` JSON | `stacserver` | Geoportal |
| `/api/info/version` | `dataverse` | Scientific data repository |
| DSpace `/server/api` or `/xmlui` | `dspace` | Scientific data repository |
| GAVO DaCHS TAP / `DaCHS` | `dachs` | Scientific data repository |
| BEXIS2 `/api/` or bexis2 chrome | `bexis2` | Scientific data repository |
| Specify Web Portal collection search | `specify` | Scientific data repository |
| `/api/records?size=1` InvenioRDM | `inveniordm` | Scientific data repository |
| `/api/v1/` PxWeb tables | `pxweb` | Indicators catalog |
| `webMain.aspx` `funid=` Taiwan statistical dynamic query | `webmain` | Indicators catalog |
| `terristory.fr/{region}` TerriSTORY hub | `terristory` | Indicators catalog |
| `ihk-fachkraeftemonitor.de/{land}/` | `ihkfachkraeftemonitor` | Indicators catalog |
| `/Informationsportal/` DUVA (KOSIS-Gemeinschaft) | `duva` | Indicators catalog |
| `GC_loadCss.php` / `/geoclipair/` Géoclip Air | `geoclip` | Indicators catalog |
| Title InstantAtlas™ / `ia-min.js` | `instantatlas` | Indicators catalog |
| MATS-Datenportal / “Modernes Analyse Tool Statistik” | `mats` | Indicators catalog |
| `*.ifinmon.ru` / iminfin.ru iMonitoring Open Budget | `imonitoring` | Indicators catalog |
| `/jaxi/Tabla.htm` `/jaxiT3/` / `iaeaxi` / `*-jaxi` menu.do | `jaxi` | Indicators catalog |
| `hdc.moph.go.th/{tenant}/public/` Health Data Center | `hdc` | Indicators catalog |
| `PxStat.Data.Cube_API` / “PxStat Open Data Platform” | `pxstat` | Indicators catalog |
| `/databrowserhub/api/core` or `/databrowser/api/core` hub JSON | `istatdatabrowser` | Indicators catalog |
| Title “TabNet Win32” / `deftohtm.exe` / `cgi-bin/dh` | `tabnet` | Indicators catalog |
| `fenixservices.fao.org` / FAOSTAT API / CountrySTAT FENIX UI | `fenix` | Indicators catalog |
| Finnish `/IMS/` karttapalvelu (`tekla-mvc-common`) | `trimblelocus` | Geoportal |
| `web.dmcity.fi/{city}/public/` title “dmCity Web App” | `dmcity` | Geoportal |
| `www.infogis.fi/{muni}/` `/codebase-infogis/` | `infogis` | Geoportal |
| `/sigimweb/` title “SIGimWeb” / `/gomap_web/` | `sigimweb` | Geoportal |
| `/NetGISRuntime/basis/index.jsp` title “NetGIS - © WSP Danmark” | `netgisruntime` | Geoportal |
| SpatialMap `webkort` | `spatialsuite` | Geoportal |
| Hajk `appConfig.json` / `mapserviceBase` | `hajk` | Geoportal |
| `origo.min.js` / `origo.js` / `Origo(` Origosamverkan | `origo` | Geoportal |
| Title “myCarta WebMap” / `/webmap/` / `/mycartawebmap/` | `mycarta` | Geoportal |
| Title `AddSpatial` / `/smart/?profile=` / `images/addspatial.svg` | `addspatial` | Geoportal |
| `drift.kortinfo.net/Map.aspx` | `kortinfo` | Geoportal |
| IntraMaps Public `project=` / `*.spatial.t1cloud.com` | `intramaps` | Geoportal |
| `/connect/analyst/` title Spectrum Spatial / Precisely | `spectrumspatial` | Geoportal |
| `/exponare/` RestPublicApplication / PublicApplication | `exponare` | Geoportal |
| LocalMaps `/localmaps/gallery` | `localmaps` | Geoportal |
| `/mapgis/mapa.jsp` or `/mapgis9/mapa.jsp` (HyG footer) | `hygmapgis` | Geoportal |
| `/vertigisstudio/web/?app=` or `/gcx/WebViewer/` | `vertigisstudioweb` | Geoportal |
| `portals.landfolio.com` cadastre map | `landfolio` | Geoportal |
| `{comune}.servizigis.it` / “GeneGis Site Creator” | `genegis` | Geoportal |
| Title “City Maps powered by XY” / `maps.xymaps.com/{city}` / `/xymaps/Map` | `xymaps` | Geoportal |
| `{council}.pozi.com` title Pozi Web Map | `pozi` | Geoportal |
| `/JMapWeb/` or JMap NG `jmapserver-ng` / `*.jmaponline.net` | `jmap` | Geoportal |
| `{city}.giscloud.com` GIS Cloud | `giscloud` | Geoportal |
| `{county}.mrf.com` / `js/lib/mrf/` MRF Web Map | `mrf` | Geoportal |
| `web.munisight.com/{Tenant}` Catalis Login.aspx | `munisight` | Geoportal |
| `publicmaps.gisquadrat.com/BP/WEPM.aspx` title GeoMedia SmartClient Public Maps | `publicmaps` | Geoportal |
| `webgis.sit-puglia.it/{comune}/` title WebGis or SIT- | `sitwebgis` | Geoportal |
| `/pmapper/` or `{city}.geo-portale.it` p.mapper | `pmapper` | Geoportal |
| `VECommunityView/cities/{city}/` CommunityView | `communityview` | Geoportal |
| `{city}.msgis.net` title GeoInformation | `msgis` | Geoportal |
| Title `Weave Map` webpack `app.*.js` (Cohga) | `weave` | Geoportal |
| `assets/ekmapboxgl/ekmap-mapboxgl.js` / title eKMap Cloud | `ekmap` | Geoportal |
| OVIE OpenLayers `/js/libs/OpenLayers/OL.js` + Materialize | `ovie` | Geoportal |
| `{city}.cadastre.com.ua` or SOFTPRO `/js/locale/ua.js` | `softpro` | Geoportal |
| `/mdm6/` or `/mxsig2/` amplify.js Mapa Digital | `mxsig` | Geoportal |
| `/apps/dashboards/{item-id}` | `arcgisdashboards` | Geoportal |
| HTML comment `DIGITAL TWIN CLOUD - NEWLAYER` / `assets/css/IDE.css` | `digitaltwincloud` | Geoportal |
| V&G `/resources/common/thirdparty/soda/soda.js` | `gtmap` | Geoportal |
| `/js/base/MapSave.js` + `BaseMap.js` / `SeeMap.js` | `myeongji` | Geoportal |
| `/apps/instant/{template}/?appid=` Instant Apps | `instantapps` | Geoportal |
| `{city}.gisplan.sk` / T-MAPY Spinbox / `tmapy.svg` / GIS4U / `{city}.tmapserver.cz` | `gisplan` | Geoportal |
| `mobec.sk/{slug}` T-MAPY mOBEC / `tmapyn.svg` | `mobec` | Geoportal |
| `webgis.{city}.sk` title `WebGIS v2, CG` | `cgwebgis` | Geoportal |
| `gis.{city}.sk` title `Geodeticca WEB GIS` | `geodeticca` | Geoportal |
| `{city}.obce.gepro.cz` / `/OUT/HTML/` Geoportál GEPRO | `gepro` | Geoportal |
| `evald.ee/{slug}/` title EVALD / KOVGIS | `evald` | Geoportal |
| `{tenant}.tergis.lv` title terGIS / `/api/v1/classifiers/layers` | `tergis` | Geoportal |
| `app.gisonline.cz/{city}` TopGis | `gisonline` | Geoportal |
| `{muni}.k5mapserver.cz` title GEOPORTÁL | `k5mapserver` | Geoportal |
| Marushka `zipped.js` or `js/marushka.js` | `marushka` | Geoportal |
| `{dtm|geoportal}.{kraj}.cz/portal/` `Georeal.Cards` | `georeal` | Geoportal |
| `portal.mapotip.cz/{obec}` title Mapotip | `mapotip` | Geoportal |
| `www.gisserver.de/{city}/` portal.js GIScity | `giscity` | Geoportal |
| `vianovis.net/{tenant}/` or `loadTouviaMaps()` touvia.MAPS | `touviamaps` | Geoportal |
| `INGRADA online` / `Softplan.Ingrada.Mobile` | `ingrada` | Geoportal |
| `html.vcs-ui` title `VC Map` | `vcmap` | Geoportal |
| `geoportale.sportellounicodigitale.it/GisMaster` `IdCliente=` | `gismaster` | Geoportal |
| G3W-CLIENT `/map/{group}/` | `g3wsuite` | Geoportal |
| MapCentia `/apps/viewer` or `/mapcache/` WMTS | `gc2` | Geoportal |
| hale»connect `/csw` or `/ows/services/` | `haleconnect` | Geoportal |
| `*.sentinel-hub.com` STAC `/api/v1/catalog` | `sentinelhub` | Geoportal |
| `*.revenuedev.org` license portal | `rdfrepository` | Open data portal |
| ResourceContracts `/contract/resources` | `resourcecontracts` | Open data portal |
| OpenSpending fiscal dataset search | `openspending` | Open data portal |
| Title `Shanoir` / `Shanoir NG` | `shanoir` | Scientific data repository |
| Title `LORIS` / `*.loris.ca` public portal | `loris` | Scientific data repository |
| MINERVA / MINERVA-Net pathway maps | `minerva` | Scientific data repository |
| Nextstrain / Auspice dataset catalog | `nextstrain` | Scientific data repository |
| Materials Cloud Explore (not Archive) | `materialscloud` | Scientific data repository |
| OpenKIM interatomic models | `openkim` | Scientific data repository |
| ChecklistBank dataset API | `checklistbank` | Scientific data repository |
| ProteoSAFe `/ProteoSAFe/datasets.jsp` | `proteosafe` | Scientific data repository |
| CyVerse Data Commons catalog | `cyverse` | Scientific data repository |
| GeoNature-atlas `/static/css/atlas.css` | `geonature` | Geoportal |
| map.geo.admin.ch `/v1.*/assets/index-` | `webmapviewer` | Geoportal |
| DataHub title + `/api/graphql` | `datahubproject` | Metadata catalog |
| Hugging Face `/datasets/` | `huggingface` | Machine learning catalog |
| Title `CodaLab` / `competitions.codalab.org` | `codalab` | Machine learning catalog |
| Title `Codabench` / `codabench.org` | `codabench` | Machine learning catalog |
| `/v1.1/` SensorThings JSON (`Things` / `Datastreams`) or title `FROST-Server` | `frostserver` | Scientific data repository |
| Title `easydb 5` / `fylr_inject` / `/api/v1/session` | `easydb` | Scientific data repository |
| Title `Yareta` / `/oai-info/oai-provider/oai` | `dlcm` | Scientific data repository |
| `meta generator` `GeoCMS Version:` `brain-SCC` | `braingeocms` | Geoportal |
| OpenAlex bibliographic API | `openalex` | Scientific data repository |
| Wikidata / Wikibase SPARQL | `wikibase` | Scientific data repository |
| DBpedia Databus | `databus` | Scientific data repository |
| MGnify / MetaboLights / BioStudies | `mgnify` / `metabolights` / `biostudies` | Scientific data repository |
| Reactome / WikiPathways | `reactome` / `wikipathways` | Scientific data repository |
| UCSC Genome Browser | `ucscgenomebrowser` | Scientific data repository |
| FlyBase / WormBase | `flybase` / `wormbase` | Scientific data repository |
| iDigBio Portal | `idigbio` | Scientific data repository |
| iNaturalist hub | `inaturalist` | Scientific data repository |
| `{city}.data.gxzf.gov.cn` | `gxopendata` | Open data portal |
| `/openapi.json` + `/api/datasets` JSON:API (`type: dataset`) | `opengdc` | Open data portal |
| SparkMap / All Things hub | `sparkmap` | Indicators catalog |
| Clarivate Converis CRIS | `converis` | Scientific data repository |
| `begin.view` / Panorama Public / LabKey | `labkey` | Scientific data repository |
| Sage Bionetworks / `synapse.org` | `synapse` | Scientific data repository |
| `/xnat/` or `/data/projects` | `xnat` | Scientific data repository |
| OMERO `/webclient/` or IDR | `omero` | Scientific data repository |
| Kadi4Mat `/api/records` | `kadi4mat` | Scientific data repository |
| Cologne CRC `/site/index.php` helper.js | `tr32db` | Scientific data repository |
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
- Directory hubs that only list other catalogs (IPUMS Health Surveys-class)
- Survey / data-collection platforms with no public dataset catalog (SurveySolutions)
- Embeds or RPC viewers of another catalog (Oskari embeds of Suomi.fi)
- Marketplace and demo tenants (`giscloud` `mapportal` / `crowdsource-demo`)

## After a valid find

1. `python scripts/builder.py add-single URL --scheduled` (preferred) or write YAML per [contribute.md](contribute.md).
2. `python scripts/builder.py assign`
3. `python scripts/builder.py validate-yaml --id` for that catalog id
4. Cite `id` + `link` in the reply. List skipped duplicates with their existing `id`. If the vendor list is exhausted, say so (0 missing is a complete hunt).

## Do not

- Walk `data/entities/**/*.yaml` to search; use exports
- Treat a DuckDB lock as failure; use `full.parquet`
- Hand-edit `data/datasets/`
- Bypass `401`/`403`, guess API keys, or follow login forms
- Flood a host; one or two GETs per path is enough
- Commit generated dumps unless the user asked for a rebuild
- Repeat a software-instance hunt from the last two weeks unless a new gallery URL exists
- Google every city in a country that already has a complete municipal GIS tenant list

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
