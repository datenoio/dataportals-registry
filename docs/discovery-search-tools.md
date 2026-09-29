# Search engines and internet maps

Use these tools **after** vendor and government lists ([discovery.md](discovery.md#existing-lists-start-here)). They find catalog installations that never appear on a gallery page: city CKAN sites, municipal GeoNetwork nodes, university Dataverse hosts.

This page is for **public catalog discovery** for the registry. It is not a scanner playbook. Do not write internet-wide crawlers in this repository. Query existing search indexes, then confirm each candidate with one or two public GETs.

Agent checklist: [agents/discover.md](agents/discover.md). Platform fingerprints: [opendata](discovery-opendata.md), [geoportals](discovery-geoportals.md), [scientific](discovery-scientific.md), [metadata](discovery-metadata.md), [indicators and microdata](discovery-indicators.md).

## Workflow

1. Scope the search: one country, one city, one `software.id`, one TLD, or one named list URL. Unscoped queries produce more noise than this registry can review. For municipal geoportals, scope to a **product tenant list**, not every city name.
2. Duplicate-check exports (`datasets.duckdb` / `full.parquet`) and `data/scheduled/` **before** opening dozens of tabs. Match on hostname, not display name. If DuckDB is locked, use Parquet. For a batch of candidates, use `python scripts/hunt.py dedupe candidates.jsonl` — it reads DuckDB read-only and falls back to parquet automatically.
3. Run a **title / URL** query first (Google `intitle:` / `inurl:`, Censys `html_title`, FOFA `title=`). Then a **body / snippet** query (`ckan-footer-logo`, HTTP body). For open-source software that people deploy by forking, search GitHub forks and code search ([#github](#github)) before an internet-wide body query — the fingerprint is often in the repo, not the HTML title. When that file is also served, use the same string as the FOFA `body=` query ([#common-files](#common-files)). For SaaS viewers, Certificate Transparency often beats Google (`%.pozi.com`, `%.giscloud.com`, `%.webewid.pl`).
4. Restrict with `site:.gov`, a national TLD, a Censys `location.country_code`, or FOFA `country="XX"`.
5. Confirm the live site with the probe table for that platform. Set `software.id` only when two signals match. For a batch, `python scripts/hunt.py probe candidates.deduped.jsonl --software ckan` does polite per-host GETs with encoding-safe title extraction and fingerprint probes.
6. Add verified finds with `add-single --scheduled` (or `add-batch` for a list). Skip demos, docs, GitHub repos, and login-only sites. If the vendor list is exhausted, report 0 missing and stop.
7. Log the hunt with `python scripts/hunt.py log --kind software-instance --target <software-id> --added N --skipped-dupes M --notes "..."`.

## Scripted searches with hunt.py

`scripts/hunt.py` is the tested implementation of the plumbing discovery sessions used to rebuild as throwaway scripts. It is a local maintainer/agent CLI — it queries the documented search APIs and probes only candidate hosts, never the open internet.

```bash
# FOFA (needs FOFA_EMAIL + FOFA_KEY in the environment)
python scripts/hunt.py search fofa 'title="数据开放" && country="CN"' --out candidates.jsonl --max-pages 2

# Censys Platform v3 (needs CENSYS_API_TOKEN, optional CENSYS_ORGANIZATION_ID)
python scripts/hunt.py search censys 'web.endpoints.http.html_title: "HSLayers"' --out candidates.jsonl

# Duplicate-check against exports (DuckDB read-only, parquet fallback on lock)
python scripts/hunt.py dedupe candidates.jsonl

# Polite probe: per-host serialization, encoding detection, liveness, fingerprints
python scripts/hunt.py probe candidates.deduped.jsonl --software ckan --concurrency 8

# Log the hunt
python scripts/hunt.py log --kind software-instance --target ckan --added 5 --skipped-dupes 12
```

`search` retries 429/5xx with exponential backoff and honors `Retry-After`. `probe` classifies liveness with the same vocabulary as `scripts/check_liveness.py`, decodes legacy encodings (GBK, Big5, Cyrillic) for titles, flags `401`/`403` as `auth_required` (never bypasses them), and annotates `software_id` when a fingerprint probe from the apidetect URL maps matches.

## What counts as a hit

Keep a URL when all of these are true:

- A public catalog UI or harvestable API (dataset list, map catalog, repository search, indicator tables)
- Country (and subregion for local owners) can be determined from the owner
- Software is known or explicitly `custom`

Discard documentation sites, vendor marketing, software forges, single-file download pages, expired domains, and anything that returns `401`/`403` for the catalog listing.

## Google Search

[Google](https://www.google.com) is the highest-yield first pass for named cities and government TLDs. Use [Bing](https://www.bing.com) or [DuckDuckGo](https://duckduckgo.com) with the same operators when Google rate-limits.

### Operators that matter

| Operator | Meaning | Catalog example |
|----------|---------|-----------------|
| `"exact phrase"` | Words in that order | `"Powered by CKAN"` |
| `intitle:` | Words in the HTML title | `intitle:"GeoNetwork opensource"` |
| `inurl:` | Path or host fragment | `inurl:/dataset site:.gov` |
| `intext:` | Words in the page body | `intext:"Powered by OpenDataSoft"` |
| `site:` | Host or TLD | `site:.gouv.fr données ouvertes` |
| `OR` | Either term | `"open data" OR "datos abiertos"` |
| `-term` | Exclude | `"CKAN" -site:github.com -site:ckan.org` |
| `filetype:` | File extension | `filetype:xml inurl:GetCapabilities CSW` |
| `after:` / `before:` | Date filter | `opendata after:2024-01-01` |
| `AROUND(n)` | Terms near each other | `datos AROUND(3) abiertos` |

Combine operators. A useful pattern is **phrase + path + TLD + exclusions**:

```text
"Powered by CKAN" inurl:/dataset site:.gov -site:github.com -site:ckan.org
```

### Language and TLD filters

Search in the local language. Restrict to the government or national TLD so you do not harvest every blog post about open data.

| Language | Catalog phrases | Typical `site:` |
|----------|-----------------|-----------------|
| English | open data, data portal, geoportal, data catalog | `.gov`, `.gov.uk`, `.gov.au` |
| Spanish | datos abiertos, catálogo de datos, geoportal | `.gob.*`, `.gob.es`, `.gob.mx`, `.gob.ar` |
| French | données ouvertes, catalogue de données | `.gouv.fr`, `.gc.ca` |
| German | offene daten, datenportal, geoportal | `.de`, `.gv.at`, `.admin.ch` |
| Portuguese | dados abertos, portal de dados | `.gov.br`, `.gov.pt` |
| Italian | dati aperti, catalogo dati | `.gov.it` |
| Dutch | open data, dataportaal | `.overheid.nl` |
| Russian | открытые данные, геопортал | `.gov.ru`, `.рф` |
| Chinese | 开放数据, 数据开放, 政务数据 | `.gov.cn` |
| Arabic | البيانات المفتوحة | `.gov.sa`, `.gov.eg` |
| Japanese | オープンデータ | `.go.jp`, `.lg.jp` |

City and agency names beat generic “open data” queries. Example: `datos abiertos "municipalidad" site:.gob.pe`.

### Query recipes

Copy and replace the TLD or place name. Platform-specific queries live on the platform pages; these are generic starters.

**Open data**

```text
("open data" OR opendata OR "data portal") (catalog OR datasets) site:.gov
inurl:/opendata OR inurl:/data OR inurl:/datasets site:.gouv.fr
"datos abiertos" (ayuntamiento OR municipio OR gobernación) site:.gob.mx
inurl:/odweb/ (数据开放 OR "公共数据开放平台") site:.gov.cn
```

**Geoportals**

```text
(geoportal OR "geo portal" OR "spatial data" OR INSPIRE) (catalog OR metadata) site:.europa.eu
intitle:geoportal (WMS OR CSW OR GeoNetwork) site:.de
```

**Scientific repositories**

```text
("research data" OR "data repository" OR dataverse OR dspace) (datasets OR "dataverse") site:.edu
"institutional repository" (data OR research) site:.ac.uk
("LabKey Server" OR cBioPortal OR InterMine OR "Kadi4Mat" OR NOMAD OR XNAT OR OMERO) (repository OR studies OR archive)
"National Summary Data Page" (e-GDDS OR SDDS OR IMF)
```

**Host patterns**

Google `site:` does not treat `data.*` as a DNS wildcard. Use `inurl:` for prefixes, or Certificate Transparency ([crt.sh](#certificate-transparency-and-dns)) for `opendata.` names:

```text
inurl:data. "open data"
inurl:opendata. OR inurl:geoportal.
inurl:hub.arcgis.com
inurl:opendatasoft.com
```

### Noise to exclude

Add these exclusions once you see the same junk in the first page of results:

```text
-site:github.com -site:gitlab.com -site:sourceforge.net
-site:stackoverflow.com -site:reddit.com -site:wikipedia.org
-site:ckan.org -site:docs.ckan.org -site:opendatasoft.com/blog
-"getting started" -documentation -"quick start" -tutorial
```

Google often ranks **dataset pages** and **news articles** above the catalog homepage. Open the site, then walk up to `/`, `/data`, `/dataset`, or `/geonetwork` until you have the catalog root. Register the catalog URL, not a single dataset.

## GitHub {#github}

Open-source catalog software is often deployed by forking the upstream repository and publishing GitHub Pages or a custom domain. Google, Censys, and FOFA miss those installs when the fingerprint lives in `_config.yml`, a compose file, or the README rather than the HTML title. Use GitHub for that class of product. Hosted SaaS (ArcGIS Hub, Socrata, OpenDataSoft) still comes from the vendor hostname pattern, not from forks.

Read `repository_url` on the software YAML. When installations are copies of that repo, build the instance list from GitHub. Do not clone the network. `gh api` pagination is enough.

### Two lists

GitHub code search does **not** index most forks. Run both passes or you will miss either the untouched forks or the detached copies.

| Pass | What it finds | How |
|------|----------------|-----|
| Forks | Copies that stayed attached to the upstream repo | `GET /repos/{owner}/{repo}/forks?per_page=100` (paginate) |
| Code search | Renames, “based on” repos, and forks GitHub has detached | A product-specific string in a file operators edit |

Code search needs a string that only this product writes, not the product name alone. `filename:_config.yml`, a theme key, a Docker Compose service, or a layout path from the platform page. The JKAN pair is the worked example for a GitHub Pages app: forks of [timwis/jkan](https://github.com/timwis/jkan), then `jkan_theme filename:_config.yml` ([discovery-opendata.md](discovery-opendata.md#jkan)). A wider README phrase (`"backend-free open data portal"`) finds more repos and more empty clones.

CKAN is the server-app shape. Forks of `ckan/ckan` and `ckan/ckan-docker` keep `CKAN_SITE_URL` on localhost. Search the committed config instead: `ckan.site_url` in `ckan.ini` (2.9+) and `production.ini` (2.8), or `CKAN_SITE_URL=https://` in `.env` and READMEs ([discovery-opendata.md](discovery-opendata.md#ckan)).

### Common files, then FOFA {#common-files}

Take the code-search string from a file the upstream repo ships (`_config.yml`, `Gemfile`, `index.html`, a layout, `local.cfg`). When that same string is written into the HTML, it is also the FOFA `body=` query. A short product-name body query is a weak fingerprint: in September 2026 `body="NADA"` matched about 1.4 million unrelated hosts, and `body="Powered by Datasette"` matched none because the footer template splits the words around an `<a>` tag.

Forks of a server framework (CKAN, Datasette, Omeka S, DSpace, VuFind, Hyrax) are the software, not a portal list. Search the committed config or the served string from the layout. Forks are the portal list for a GitHub Pages app (JKAN, OpenSDG) and for a viewer people copy (`mviewer`, STAC Browser).

| `software.id` | File | Search |
|---------------|------|----------------|
| [`opensdg`](discovery-indicators.md#opensdg) | `open-sdg-site-starter` `_config.yml`, `Gemfile` | GitHub `remote_theme: open-sdg/open-sdg filename:_config.yml`; FOFA `body="jekyll-open-sdg-plugins"` |
| [`stacbrowser`](discovery-geoportals-sdi.md#stacbrowser) | `index.html`, `config.js` | GitHub forks of `radiantearth/stac-browser`; read `catalogUrl`; FOFA `body="STAC Browser doesn't work properly"` |
| [`mviewer`](discovery-geoportals-sdi.md#mviewer) | `index.html` | GitHub forks of `geobretagne/mviewer`; FOFA `body="css/mviewer.css"` |
| [`dspace`](discovery-scientific.md#dspace) | `dspace/config/local.cfg.EXAMPLE`, `dspace-angular` `head-tag.service.ts` | GitHub `"dspace.ui.url = https://" filename:local.cfg`; FOFA `body="generator\" content=\"DSpace"` |
| [`datasette`](discovery-opendata.md#datasette) | `datasette/templates/base.html` | FOFA `body="application/json+datasette"` |
| [`omekas`](discovery-scientific.md#omekas) | `application/view/layout/layout.phtml` | FOFA `body="Powered by Omeka S"` |
| [`dataverse`](discovery-scientific.md#dataverse) | `src/main/webapp/dataverse.xhtml` | FOFA `body="dataverse.xhtml"` |
| [`hyrax`](discovery-scientific.md#hyrax) | `app/views/layouts/_generator_meta_tag.html.erb` | FOFA `body="Samvera Hyrax"` |
| [`inveniordm`](discovery-scientific.md#inveniordm) | `invenio_app_rdm/.../footer.html` | FOFA `body="app-rdm-footer"` |
| [`vufind`](discovery-scientific.md#vufind) | `themes/bootstrap5/templates/layout/layout.phtml` | FOFA `body="VuFind.path"` |
| [`nada`](discovery-indicators.md#nada) | `themes/nada/footer.php`, `themes/nada52/footer.php` | FOFA `body="nada-logo"` |
| [`aleph`](discovery-opendata.md#aleph) | `ui/public/index.html` | FOFA `body="data-api-endpoint=\"/api/2/\""` |
| [`geonode`](discovery-geoportals-sdi.md#geonode) | `geonode/templates/base.html` | FOFA `body="geonode/css/base.css"` |
| [`mapstore`](discovery-geoportals-sdi.md#mapstore) | `web/client/indexTemplate.html` | FOFA `body="_ms2_init_text"` |
| [`qwc2`](discovery-geoportals-sdi.md#qwc2) | `index.html` | FOFA `body="assets/css/qwc2.css"` |
| [`geoblacklight`](discovery-geoportals-sdi.md#geoblacklight) | `app/views/catalog/_home_text.html.erb` | FOFA `body="geoblacklight-version"` |
| [`eprints`](discovery-scientific.md#eprints) | `lib/templates/default.xml` | FOFA `body="ep_tm_header"` |
| [`pygeoapi`](discovery-geoportals-sdi.md#pygeoapi) | `pygeoapi/templates/_base.html`, `pygeoapi-config.yml` | FOFA `body="static/img/pygeoapi.png"`; GitHub `filename:pygeoapi-config.yml` |
| [`pxweb`](discovery-indicators.md#pxweb) | `PXWeb/PxWeb.Master` | FOFA `body="main-pxweb.css"` |
| [`lizmap`](discovery-geoportals-sdi.md#lizmap) | `lizmap/modules/view/templates/map.tpl` | FOFA `body="lizmap-navbar"` |
| [`mapbender`](discovery-geoportals-sdi.md#mapbender) | `src/Mapbender/CoreBundle/Resources/public` | FOFA `body="bundles/mapbendercore"` |
| [`invenio`](discovery-scientific.md#invenio) | `invenio_theme/.../footer.html` | FOFA `body="http://inveniosoftware.org"` |
| [`wikibase`](discovery-scientific-domain.md#wikibase) | `view/resources/templates.php` | FOFA `body="wikibase-title"` |
| [`phaidra`](discovery-scientific.md#phaidra) | `src/phaidra-ui/app.html` | FOFA `body="This repository is powered by PHAIDRA"` |
| [`oskari`](discovery-geoportals-sdi.md#oskari) | `servlet-map/.../index.jsp` | FOFA `body="oskari.min.css"` |
| [`galaxy`](discovery-scientific-domain.md#galaxy) | `templates/js-app.mako` | FOFA `body="Javascript Required for Galaxy"` |
| [`opus`](discovery-scientific.md#opus) | `public/layouts/opus4/common.phtml` | FOFA `body="layouts/opus4"` |
| [`librecat`](discovery-scientific.md#librecat) | `views/header.tt` | FOFA `body="BEGIN header.tt"` |
| [`magda`](discovery-opendata.md#magda) | `magda-web-client/public/index.html` | FOFA `body="/api/v0/content/favicon.ico"` |
| [`udata`](discovery-opendata.md#udata) | `udata_front/.../footer.html` | FOFA `body="github.com/opendatateam/udata/"` |
| [`superset`](discovery-indicators.md#superset) | `superset/templates/superset/spa.html` | FOFA `body="superset-theme-mode"` |
| [`tripal`](discovery-scientific-domain.md#tripal) | `tripal/css/tripal.css` | FOFA `body="tripal.css"` |
| [`mytardis`](discovery-scientific.md#mytardis) | `tardis_portal/templates/.../portal_template.html` | FOFA `body="github.com/mytardis/mytardis"` |
| [`korp`](discovery-scientific-domain.md#korp) | `app/index.html` | FOFA `body="You need JavaScript to run Korp."` |
| [`igo2`](discovery-geoportals-viewers.md#igo2) | `src/index.html` | GitHub forks of `infra-geo-ouverte/igo2`; code search `splash-screen__filmstrip`; FOFA `body="splash-screen__filmstrip"` |
| [`xnat`](discovery-scientific.md#xnat) | `xnat-templates/navigations/htmlOpen.vm` | FOFA `body="xnat-templates/navigations/htmlOpen"` |
| [`terria`](discovery-geoportals-sdi.md#terria) | `apps/terriamap/wwwroot/index.ejs` | FOFA `body="class=\"terria\""` |
| [`scicat`](discovery-scientific-domain.md#scicat) | `src/index.html` | FOFA `body="SciCat metadata catalogue"` |
| [`weko3`](discovery-scientific.md#weko3) | `weko_theme/.../header.html` | FOFA `body="weko_admin/quill.snow.css"` |
| [`omero`](discovery-scientific.md#omero) | `webclient/templates/webclient/login.html` | FOFA `body="ome.login.css"` |
| [`bexis2`](discovery-scientific-domain.md#bexis2) | `Themes/Default/Layouts/_Layout.cshtml` | FOFA `body="bundles/bexis"` |
| [`mycore`](discovery-scientific.md#mycore) | `mir-module/.../mir-common-layout.xsl` | FOFA `body="mir-lang"` |
| [`micka`](discovery-geoportals-sdi.md#micka) | `Catalog/templates/default/@layout.latte` | FOFA `body="micka.css"` |
| [`intermine`](discovery-scientific-domain.md#intermine) | `intermine/webapp/.../layout.jsp` | FOFA `body="intermine.Service"` |
| [`fedora`](discovery-scientific.md#fedora) | `fcrepo-webapp/.../index.html` | FOFA `body="fcrepo-favicon.png"` |
| [`gsimaps`](discovery-geoportals-viewers.md#gsimaps) | `index.html` | FOFA `body="css/gsimaps.css"` |
| [`thredds`](discovery-scientific-domain.md#thredds) | `WEB-INF/templates/catalog.html` | FOFA `body="tds.css"` |
| [`liferay`](discovery-opendata.md#liferay) | `frontend-theme-classic/.../portal_normal.ftl` | FOFA `body="http://www.liferay.com"` |
| [`symbiota`](discovery-scientific-domain.md#symbiota) | `includes/head_template.php` | FOFA `body="symbiota/header.css"` |
| [`cbioportal`](discovery-scientific-domain.md#cbioportal) | `my-index.ejs` | FOFA `body="cbioportal-frontend"` |
| [`fairdatapoint`](discovery-metadata.md#fairdatapoint) | `public/index.html` | FOFA `body="fdp-client doesn't work properly"` |
| [`geonetwork`](discovery-geoportals-sdi.md#geonetwork) | `catalog/views/api/index.html`, `catalog/locales/en-core.json` | FOFA `body="gn_search_default"`; also `body="gn-bottom-bar"`, `body="datahub-root"`, `body="GeoNetwork opensource"` |
| [`labkey`](discovery-scientific.md#labkey) | `bootstrap/pageTemplate.jsp` | FOFA `body="lk-body-ct"` |
| [`pycsw`](discovery-geoportals-sdi.md#pycsw) | `pycsw/templates/_base.html` | FOFA `body="pycsw-logo-vertical.png"` |
| [`mapserver`](discovery-geoportals-sdi.md#mapserver) | `src/maperror.c` | FOFA `body="MapServer version"` |
| [`opendaphyrax`](discovery-scientific-domain.md#opendaphyrax) | `hyrax/xsl/threddsCatalogPresentation.xsl` | FOFA `body="OPeNDAP Hyrax"` |
| [`hubzero`](discovery-scientific.md#hubzero) | `en-GB.tpl_kameleon.ini` | FOFA `body="http://hubzero.org"` |
| [`pydap`](discovery-scientific.md#pydap) | `wsgi/templates/index.html`, 3.2 `pydap-listing` | FOFA `body="pydap-listing"`; also `body="http://pydap.org/"` and `body="OPeNDAP pydap"` |
| [`dataone`](discovery-scientific-domain.md#dataone) | `src/index.html` | FOFA `body="configuration file for MetacatUI"` |
| [`clowder`](discovery-scientific.md#clowder) | `app/views/main.scala.html` | FOFA `body="clowderframework.org"` |
| [`ramadda`](discovery-scientific.md#ramadda) | `resources/web/jsimports.html` | FOFA `body="ramadda.js"` |
| [`metashare`](discovery-scientific.md#metashare) | `metashare/templates/base.html` | FOFA `body="metashare/js/metashare.js"` |
| [`shanoir`](discovery-scientific.md#shanoir) | `shanoir-ng-front/src/index.html` | FOFA `body="/shanoir-ng/"` |
| [`nomad`](discovery-scientific.md#nomad) | `gui/public/index.html` | FOFA `body="close all NOMAD tabs"` |
| [`ipt`](discovery-scientific-domain.md#ipt) | `WEB-INF/pages/inc/footer.ftl` | FOFA `body="GBIF-2015-standard-ipt.png"` |
| [`vivo`](discovery-scientific-domain.md#vivo) | `themes/wilma/templates/footer.ftl` | FOFA `body="vivoweb.org"` |
| [`frostserver`](discovery-scientific-domain.md#frostserver) | `FROST-Server.MQTTP/.../index.html` | FOFA `body="FROST-Server"` |
| [`geoserver`](discovery-geoportals-sdi.md#geoserver) | `web/app/.../index.html` | FOFA `body="GeoServer admin console"` |
| [`mapproxy`](discovery-geoportals-sdi.md#mapproxy) | `service/templates/demo/static.html` | FOFA `body="MapProxy Demo"` |
| [`umap`](discovery-geoportals-viewers.md#umap) | `umap/templates/base.html` | FOFA `body="umap/favicons"` |
| [`dandi`](discovery-scientific-domain.md#dandi) | `web/index.html` | FOFA `body="DANDI Archive doesn't work properly"` |
| [`breedbase`](discovery-scientific-domain.md#breedbase) | `mason/site/footer/body.mas` | FOFA `body="solgenomics/sgn"` |
| [`nextstrain`](discovery-scientific-domain.md#nextstrain) | `static-site/components/footer/index.tsx` | FOFA `body="attribution to nextstrain.org"` |
| [`opencontext`](discovery-scientific-domain.md#opencontext) | `bootstrap_vue/page_footer.html` | FOFA `body="Open Context is a publishing service"` |
| [`gin`](discovery-scientific.md#gin) | `templates/base/footer_gin_brand.tmpl` | FOFA `body="doi.org/10.17616/R3SX9N"` |
| [`shogun`](discovery-geoportals-viewers.md#shogun) | `shogun-boot/.../index.html` | FOFA `body="terrestris.github.io/shogun"` |
| [`tailormap`](discovery-geoportals-viewers.md#tailormap) | `projects/app/src/index.html` | GitHub `"<title>Tailormap</title>" "<tm-root></tm-root>"`; FOFA `body="<tm-root></tm-root>" && title="Tailormap"` |
| [`obibamica`](discovery-indicators.md#obibamica) | `mica-webapp/.../footer.ftl` | FOFA `body="www.obiba.org"` |
| [`datahubproject`](discovery-metadata.md#datahubproject) | `datahub-web-react/index.html` | FOFA `body="A Metadata Platform for the Modern Data Stack"` |
| [`hajk`](discovery-geoportals-viewers.md#hajk) | `apps/client/index.html` | FOFA `body="Hajk - open source webGIS"` |
| [`sitmun`](discovery-geoportals-viewers.md#sitmun) | `sitmun-viewer-app` `src/index.html`; classic `inicio.jsp` | FOFA `body="SITMUN Service worker registered"`; classic `body="library/dojo/themes/sitmun"` and `body="/sitmun/inicio.jsp"` |
| [`gc2`](discovery-geoportals-sdi.md#gc2) | `public/apps/viewer/index.html` | FOFA `body="window.MapCentia"` |
| [`biodare2`](discovery-scientific-domain.md#biodare2) | `static/index.html` | FOFA `body="BioDare2 - circadian period analysis"` |
| [`cellxgene`](discovery-scientific-domain.md#cellxgene) | `frontend/src/pages/_app.tsx` | FOFA `body="Cellxgene Data Portal"` |
| [`clld`](discovery-scientific-domain.md#clld) | `src/clld/web/templates/app.mako` | FOFA `body="clld-disclaimer"` |
| [`massbank`](discovery-scientific-domain.md#massbank) | `MassBank-web/.../Index.jsp` | FOFA `body="MassBank Consortium"` |
| [`databus`](discovery-scientific-domain.md#databus) | `public/templates/footer.ejs` | FOFA `body="Global and Unified Access to Knowledge Graphs"` |
| [`ontoportal`](discovery-scientific-domain.md#ontoportal) | `layouts/_footer.html.haml` | FOFA `body="ontoportal"` |
| [`lovd`](discovery-scientific-domain.md#lovd) | `src/class/template.php` | FOFA `body="LOVD v."` |
| [`jacq`](discovery-scientific-domain.md#jacq) | `output.new/index.php` | FOFA `body="JACQ_LOGO.png"` |
| [`proteosafe`](discovery-scientific-domain.md#proteosafe) | `LiveSearch/.../index.jsp` | FOFA `body="General ProteoSAFe scripts"` |
| [`molgenis`](discovery-scientific-domain.md#molgenis) | `apps/tailwind-components/.../FooterComponent.vue` | FOFA `body="Created with MOLGENIS"` |
| [`opengeoportal`](discovery-geoportals-viewers.md#opengeoportal) | `templates/ogp_home.html` | FOFA `body="OpenGeoportal.Config"` |
| [`specify`](discovery-scientific-domain.md#specify) | `PortalApp/index.html` | FOFA `body="resources/css/thumb-view.css"` |
| [`reearth`](discovery-geoportals-viewers.md#reearth) | `web/index.html`, published `publishedAppProvider` | GitHub forks of `reearth/reearth-visualizer` and `reearth/reearth-cms`; FOFA `body="publishedAppProvider"`; CMS `body="Re:Earth CMS"` |
| [`gobierto`](discovery-opendata.md#gobierto) | `layouts/_gobierto_footer.html.erb` | FOFA `body="window.gobiertoAPI"` |
| [`origo`](discovery-geoportals-viewers.md#origo) | `build/index.html` | FOFA `body="var origo = Origo"` |
| [`yoda`](discovery-scientific.md#yoda) | `themes/vu/index.html` | FOFA `body="Yoda is a share-collaborate environment"` |
| [`gisquick`](discovery-geoportals-viewers.md#gisquick) | `clients/gisquick-web/public/index.html` | FOFA `body="gisquick-web doesn't work properly"`; `/map/` mounts also `body="/map/static/js/chunk-vendors"` |
| [`instdb`](discovery-scientific.md#instdb) | Vue `public/index.html` noscript | FOFA `body="instdb-web doesn't work properly"` |
| [`argenmap`](discovery-geoportals-viewers.md#argenmap) | `index.html` | FOFA `body="src/js/components/openfiles/openfiles.css"` |
| [`miramon`](discovery-geoportals-viewers.md#miramon) | `src/index.htm`, `src/examples/*.json` | GitHub forks of `grumets/MiraMonMapBrowser`; read `ServidorLocal`; FOFA `body="StartMiraMonMapBrowser"` |
| [`atlasmapper`](discovery-geoportals-viewers.md#atlasmapper) | `clientResources/amcTemplates/index.html.ftl` | FOFA `body="atlasmapperVer"` |
| [`geonature`](discovery-geoportals-sdi.md#geonature) | `atlas/templates/core/assets_header.html` | FOFA `body="/static/css/atlas.css"` |
| [`dhis2`](discovery-indicators.md#dhis2) | `app-platform` `shell/index.html`; `dhis-web-api/.../login.html` | FOFA `body="dhis2-app-root"`; also `body="dhis-web-commons"` |
| [`52northsos`](discovery-scientific-domain.md#52northsos) | `WEB-INF/views/common/header.jsp` | FOFA `body="static/css/52n.css"` |
| [`geomapfish`](discovery-geoportals-viewers.md#geomapfish) | `contribs/gmf/apps/desktop/index.html.ejs` | FOFA `body="gmf-app-data-panel"` |
| [`shiny`](discovery-indicators.md#shiny) | `inst/www/shared/shiny.min.css` | FOFA `body="shared/shiny.min.css"` |
| [`gvsigonline`](discovery-geoportals-sdi.md#gvsigonline) | `gvsigol_core/templates/base.html` | FOFA `body="gvsigOL.css"` |
| [`datafair`](discovery-opendata.md#datafair) | `ui/index.html` | FOFA `body="simple-directory/api/sites"` |
| [`gbdwebsuite`](discovery-geoportals-viewers.md#gbdwebsuite) | `data/web/demo.html`, client login `gwsUsername`, `/gws-client/gws-start-` | FOFA `body="webSystemAsset"`; also `body="gwsUsername"` and `body="/gws-client/gws-start"`; GitHub `"gbdconsult/gws-server"` |
| [`istatdatabrowser`](discovery-indicators.md#istatdatabrowser) | `databrowser/index.html` | FOFA `body="webpackJsonpdata-browser"` |
| [`mxsig`](discovery-geoportals-viewers.md#mxsig) | `mxsig/index.html` | FOFA `body="mdm6ico.png"` |
| [`mfgeoadmin3`](discovery-geoportals-viewers.md#mfgeoadmin3) | `src/index.mako.html` | FOFA `body="GaMainController"` |
| [`amp`](discovery-opendata.md#amp) | `amp-boilerplate/.../about-template.html` | FOFA `body="ampTemplate"` |
| [`openequella`](discovery-scientific.md#openequella) | `com.equella.core/.../ResourcesService.java` | FOFA `body="com.equella.core"` |
| [`wis20box`](discovery-geoportals-sdi.md#wis20box) | `wis2box-ui/index.html` | FOFA `body="WIS 2.0 node in a box"` |
| [`flat`](discovery-scientific.md#flat) | `docker/flat/islandora/template.php` | FOFA `body="flat_bootstrap_theme"` |
| [`synapse`](discovery-scientific.md#synapse) | `src/main/webapp/Portal.html` | FOFA `body="info@sagebase.org"` |
| [`geomoose`](discovery-geoportals-viewers.md#geomoose) | `examples/desktop/index.html`, `geomoose.html` | GitHub forks of `geomoose/gm3`; `mapfile_root filename:config.js`; FOFA `body="geocode-osm.js"`; also `body="user_catalog.css"` |
| [`g3wsuite`](discovery-geoportals-sdi.md#g3wsuite) | `client/templates/client/index.html` | FOFA `body="g3wsuite_logo.png"` |
| [`fellesdatakatalog`](discovery-opendata.md#fellesdatakatalog) | `src/entrypoints/main/index.html` | FOFA `body="cms.fellesdatakatalog.digdir.no"` |
| [`materialscloud`](discovery-scientific-domain.md#materialscloud) | `materialscloud-discover/index.html.j2` | FOFA `body="mcloud_theme.min.css"` |
| [`opendatacube`](discovery-geoportals-sdi.md#opendatacube) | `cubedash/templates/layout/base.html` | GitHub forks of `opendatacube/datacube-explorer`; `filename:ingress.yaml datacube-explorer`; FOFA `body="id=\"datacube-version\""` |
| [`ckan`](discovery-opendata.md#ckan) | `ckan/templates/footer.html` | FOFA `body="ckan-footer-logo"` |
| [`vcmap`](discovery-geoportals-viewers.md#vcmap) | `index.html` | FOFA `body="vcs-ui"` |
| [`datacubews`](discovery-geoportals-sdi.md#datacubews) | `datacube_ows/templates/index.html` | FOFA `body="datacube-ows"` |
| [`hydroshare`](discovery-scientific-domain.md#hydroshare) | `theme/templates/base.html` | FOFA `body="hydroshare_core.css"` |
| [`dkan`](discovery-opendata.md#dkan) | `data-catalog-app/index.html` | FOFA `body="DKAN is an open-source data management platform"` |
| [`statplanet`](discovery-indicators.md#statplanet) | `StatPlanet_Cloud.html` | FOFA `body="statsilk-container"` |
| [`geotrek`](discovery-geoportals-sdi.md#geotrek) | `frontend/src/pages/_document.tsx` | FOFA `body="--color-primary1-default"` |
| [`grandchallenge`](discovery-other.md#grandchallenge) | `partials/script.html` | GitHub forks of `DIAGNijmegen/rse-grand-challenge`; `datatables.defaults.mjs`; FOFA `body="js/datatables.defaults.mjs" && domain!="grand-challenge.org"` |
| [`bodikodcs`](discovery-opendata.md#bodikodcs) | `ckanext/bodik_theme/templates/base.html` | FOFA `body="bodik_odcs.css"` |
| [`andino`](discovery-opendata.md#andino) | `ckanext/gobar_theme/templates/footer.html` | FOFA `body="gobar-footer-grid"` |
| [`checklistbank`](discovery-scientific-domain.md#checklistbank) | `index.html` | FOFA `body="<title>ChecklistBank</title>"` |
| [`terristory`](discovery-indicators.md#terristory) | `front/index.html` | FOFA `body="base de données TerriSTORY"` |
| [`statsuite`](discovery-indicators.md#statsuite) | `i18n/en.json` | FOFA `body=".Stat Suite"` |
| [`kadi4mat`](discovery-scientific.md#kadi4mat) | `kadi/templates/base.html` | FOFA `body="window.kadi"` |
| [`piveau`](discovery-opendata.md#piveau) | `index.html` | FOFA `body="<title>Piveau UI</title>"` |
| [`lkod`](discovery-opendata.md#lkod) | `src/app/metatags.json` | FOFA `body="Procházejte a stahujte datové sady"` |
| [`openwis`](discovery-geoportals-sdi.md#openwis) | `jsp/banner.jsp` | FOFA `body="images/openwis/header-left.jpg"` |
| [`resourcecontracts`](discovery-opendata.md#resourcecontracts) | `layout/partials/head.blade.php` | FOFA `body="css/new-rc.css"` |
| [`webmapviewer`](discovery-geoportals-viewers.md#webmapviewer) | `packages/mapviewer/index.html` | FOFA `body="Maps of Switzerland - Swiss Confederation - map.geo.admin.ch"` |
| [`codalab`](discovery-other.md#codalab) | `apps/web/templates/base.html` | FOFA `body="<title>CodaLab -"` |
| [`codabench`](discovery-other.md#codabench) | `src/templates/base.html` | FOFA `title="Codabench"` |
| [`evalai`](discovery-other.md#evalai) | `frontend/base.html` | FOFA `body="ng-app=\"evalai\""` |
| [`openspending`](discovery-opendata.md#openspending) | `spendb/templates/layout.html` | FOFA `body="explore, visualize and track government spending"` |
| [`brainlife`](discovery-scientific-domain.md#brainlife) | `ui/index.html` | FOFA `body="<title>brainlife</title>"` |
| [`ourworldindata`](discovery-indicators.md#ourworldindata) | `site/SiteFooter.tsx` | FOFA `body="Teaching with OWID"` |
| [`smartmetserver`](discovery-geoportals-sdi.md#smartmetserver) | `source/AsyncConnection.cpp`, `smartmet-{iso2}` portainer compose | GitHub `routers.smartmetserver.rule`; FOFA `header="SmartMet Server"` and `body="SmartMet Server"` |
| [`dachs`](discovery-scientific-domain.md#dachs) | `resources/web/xsl/dachs-xsl-config.xsl` | FOFA `body="gavo_dc.css"` |
| [`iudx`](discovery-opendata.md#iudx) | `docs/apidoc.html`, UI `index.html` | FOFA `body="DX Catalogue API Docs"`; UI `title="IUDX \| Indian Urban Data Exchange"` and `body="IUDX UI Team"`; GitHub ingress hosts in `datakaveri/iudx-deployment` |
| [`masterportal`](discovery-geoportals-viewers.md#masterportal) | `portal/master/index.html` | FOFA `body="masterportal-root"` |
| [`kvwmap`](discovery-geoportals-viewers.md#kvwmap) | `funktionen/gui_functions.js` | FOFA `body="funktionen/gui_functions.js"` |
| [`mediatum`](discovery-scientific.md#mediatum) | generator meta | FOFA `body="mediatum - a multimedia content repository"` |
| [`klimadashboardmuenster`](discovery-indicators.md#klimadashboardmuenster) | Open CoDE credit | FOFA `body="klimadashboard-muenster"` |
| [`minerva`](discovery-scientific-domain.md#minerva) | `pages/_document.tsx` | FOFA `body="/minerva/config.js"` |
| [`opengdc`](discovery-opendata.md#opengdc) | `themes/custom/dexes/templates/page.html.twig` | FOFA `body="themes/custom/dexes"` |
| [`ensembl`](discovery-scientific.md#ensembl) | `htdocs/info/about/ensembl_powered.html` | FOFA `body="/img/empowered.png"` |
| [`ovie`](discovery-geoportals-viewers.md#ovie) | `index.html` | GitHub `js/libs/jquery.ntm/js/jquery.ntm.js filename:index.html` (client is on INEGI GitLab; title phrase finds linked deployments); FOFA `body="js/libs/jquery.ntm/js/jquery.ntm.js"` |
| [`onegeosuite`](discovery-geoportals.md#onegeosuite) | `gatsby-config.js` | FOFA `body="Onegeo Portal"` |

September 2026 FOFA hit counts for these strings are on the platform pages, next to the full query tables.

```bash
gh api --paginate "repos/timwis/jkan/forks?per_page=100"
gh api -H "Accept: application/vnd.github+json" \
  "search/code?q=jkan_theme+filename:_config.yml&per_page=100"
```

### From a repository to a catalog URL

Register the **published site**, not the `github.com` repository.

- Use `homepage` when it is a real catalog. Ignore it when every fork still carries the upstream marketing URL (`https://jkan.io`).
- Otherwise try `https://{owner}.github.io/{repo}/`, or `https://{owner}.github.io/` when the repository is `{owner}.github.io`.
- Read `CNAME` when Pages uses a custom domain.
- Probe the platform GET (`/data.json` for JKAN, the package or CSW URL for other stacks). Keep a site that lists datasets. Drop the upstream repo, docs, demos, empty forks, and templates whose only entry is the stock sample dataset.
- Several path tenants on one `github.io` host are separate catalogs. Set `--id` so the host-only id does not collide (`datascientiafoundation.github.io/LiveData/` and `/LiveDataNUM/`).
- A custom domain and a `github.io` URL that serve the same dataset list are one catalog. Keep the public hostname.

## Censys

[Censys Platform](https://platform.censys.io) indexes hosts, certificates, and web properties. It is useful when Google does not list a site (no inbound links, robots-blocked HTML, IP-only services). If Censys search is not on your plan or MCP is not connected, use [FOFA](#fofa) with the same title / body / country filters.

Create a free or research account. Use the **web properties** dataset for catalogs (they are websites). Use **hosts** when you need a product fingerprint on a port (GeoServer, ArcGIS Server). Use **certificates** for hostname patterns such as `opendata.*`.

Do not export huge unscoped result sets. Filter by country or software, then review hostnames one by one.

### Query language (Platform)

Censys Platform uses CenQL. `:` is tokenized full-text search. `=` is an exact match. Prefer **web properties** for catalog UIs:

| Goal | Field (web properties) | Field (hosts) |
|------|------------------------|---------------|
| HTML title | `web.endpoints.http.html_title` | `host.services.endpoints.http.html_title` |
| HTML body (first 64 KB) | `web.endpoints.http.body` | `host.services.endpoints.http.body` |
| Software product | `web.software.product` | `host.services.software.product` |
| Country | `web.location.country_code` | `host.location.country_code` |
| Hostname / name | `web.names` | `host.dns.names` |

Official syntax: [Censys Query Language](https://docs.censys.com/docs/censys-query-language). Field names change between Legacy Search and Platform; if a query returns a parse error, switch the dataset tab or check the field browser in the UI.

### Starter queries (Platform)

**Web properties — titles and body snippets**

```text
web.endpoints.http.html_title: "CKAN"
web.endpoints.http.body: "ckan-footer-logo"
web.endpoints.http.html_title: "GeoNetwork"
web.endpoints.http.body: "GeoNetwork opensource"
web.endpoints.http.html_title: "Socrata"
web.endpoints.http.body: "OpenDataSoft"
web.endpoints.http.body: "LabKey"
web.endpoints.http.body: "cBioPortal"
web.endpoints.http.body: "Kadi4Mat"
web.endpoints.http.body: "/odweb/"
web.software.product: "GeoServer"
web.names: "opendata"
```

**Hosts — products that listen on a port**

```text
host.services.software.product = "GeoServer"
host.services.software.product = "ArcGIS"
host.services: (software.product = "GeoServer" and endpoints.http.html_title: "GeoServer")
host.location.country_code = "FR" and host.services.endpoints.http.html_title: "CKAN"
```

**Certificates — hostname patterns**

```text
cert.parsed.names: "opendata"
cert.parsed.names: "geoportal"
cert.parsed.names: "data.gov"
```

Intersect with country whenever the UI allows it. Example: French CKAN-like titles:

```text
web.location.country_code = "FR" and web.endpoints.http.html_title: "données"
web.names: ".gouv.fr" and web.endpoints.http.body: "ckan"
```

### Legacy Search (older UI)

If you still have access to [search.censys.io](https://search.censys.io) Legacy Search, the equivalent fields are `services.http.response.html_title`, `services.http.response.body`, and `services.software.product`:

```text
services.http.response.html_title: "CKAN"
services.http.response.body: "ckan-footer-logo"
services.software.product: GeoServer
location.country_code: FR
```

### How to turn a Censys hit into a registry URL

1. Copy the hostname (prefer the certificate or web-property name, not a raw IP).
2. Try `https://{hostname}/` first, then the platform path (`/dataset`, `/geonetwork`, `/dataverse`).
3. Duplicate-check the hostname in DuckDB.
4. Probe the public API path from the platform guide.
5. Skip hosts that only serve a login form, a default web-server page, or an internal dashboard.

Censys records IPs that may host **many** vhosts. Always confirm the catalog URL in a browser or with a GET that includes a `Host` header / HTTPS name. Do not register a bare IP as `link`.

## Shodan

[Shodan](https://www.shodan.io) is the other large internet map. Filters that help:

| Filter | Use |
|--------|-----|
| `http.title:` | HTML title |
| `http.html:` | Body snippet |
| `http.component:` | Detected component |
| `product:` | Service product |
| `org:` / `ssl:` | Organisation or cert CN |
| `country:` | ISO country |
| `hostname:` | Reverse DNS / vhost |

```text
http.title:"CKAN" country:DE
http.html:"ckan-footer-logo"
http.title:"GeoNetwork" country:FR
product:GeoServer country:ES
http.html:"ArcGIS REST Services Directory"
http.title:"Dataverse" hostname:edu
ssl.cert.subject.CN:opendata
```

Same review rules as Censys: hostname over IP, public catalog UI, no auth bypass.

## FOFA {#fofa}

[FOFA](https://en.fofa.info) is an internet map in the same class as Censys and Shodan. Use it as the **Censys alternative** when any of these is true:

- Censys Platform search is not on the plan, or the official Censys MCP is not connected
- The hunt is East Asia (China, Japan, Korea, Taiwan, Hong Kong) — FOFA’s index is often denser there
- You already have `FOFA_EMAIL` / `FOFA_KEY` and want the same title / body / country filters in FOFA syntax

Same job as Censys: find catalog UIs that Google does not list. Same review rules: hostname over IP, public catalog UI, no auth bypass. Do not export huge unscoped result sets. Filter by country or software, then review hostnames one by one.

API and agent setup: [discovery-agent-tools.md](discovery-agent-tools.md#fofa). Official syntax: [FOFA rule list](https://en.fofa.info) (sign-in). Free and low plans often cannot search `body=` or `header=` over the API — fall back to `title=`, `host=`, `domain=`, `app=`, and `cert=`.

### Query language

FOFA uses `field="value"` with `&&` (AND), `||` (OR), and `!=` (NOT). Values are quoted. Translate any Censys row in the platform guides with this table. Software pages include a FOFA row for each Censys query; use this table when you need a variant (country, TLD) that is not listed.

| Goal | FOFA | Censys (web properties) |
|------|------|-------------------------|
| HTML title | `title="CKAN"` | `web.endpoints.http.html_title: "CKAN"` |
| HTML body | `body="ckan-footer-logo"` | `web.endpoints.http.body: "ckan-footer-logo"` |
| HTTP header | `header="X-Socrata"` | (headers / body) |
| Detected product | `app="GeoServer"` | `web.software.product: "GeoServer"` |
| Country | `country="PT"` | `web.location.country_code = "PT"` |
| Hostname fragment | `host="opendata"` | `web.names: "opendata"` |
| Registrable domain | `domain="opendatasoft.com"` | `web.names: "opendatasoft.com"` |
| Certificate name | `cert="opendata"` | `cert.parsed.names: "opendata"` |
| HTTPS only | `protocol="https"` | prefer HTTPS web-property names |

`host=` is a substring match, so `host=".gouv.fr"` is the usual TLD filter. Combine with country whenever the query would otherwise be global.

`domain=` is the registrable domain (`arcgis.com`), not a product hostname. A row for `city.hub.arcgis.com` has `domain` = `arcgis.com`, so `domain!="hub.arcgis.com"` does **not** drop ArcGIS Hub tenants. Exclude that SaaS with `domain!="arcgis.com"`, and find the tenants themselves with `host="hub.arcgis.com"` (substring) or `domain="opendata.arcgis.com"`. Custom-domain Hub shells are `body="hubcdn.arcgis.com/opendata-ui" && domain!="arcgis.com"` — see [ArcGIS Hub](discovery-geoportals-sdi.md#arcgishub). Short body tokens (`body="opendata-ui"`, `body="hub.js"`) are weak fingerprints.

**Path tenants.** `host=` and `domain=` return one asset per host. A product that puts every city on one host (`app.gisonline.cz/{city}`) does not yield one FOFA row per city. Search the tenant host as a body backlink (`body="app.gisonline.cz" && domain!="gisonline.cz"`) and read the path from the referring page. See [GisOnline](discovery-geoportals-viewers.md#gisonline).

**Scheme stored in `host`.** Some rows set `host` to `https://app.example.cz` rather than `app.example.cz`. `protocol="https"` then returns 0. Filter those with `port="443"`.

**`body=` query versus `body` field.** A `body="..."` query can succeed on a plan that still rejects `fields` containing `body` (FOFA error `820001`, no permission to return the body). Keep `fields` to `host,link,title,domain,port` and open the live page for the path.

**Worked translations**

| Censys | FOFA |
|--------|------|
| `web.location.country_code = "FR" and web.endpoints.http.html_title: "données"` | `title="données" && country="FR"` |
| `web.names: ".gouv.fr" and web.endpoints.http.body: "ckan"` | `host=".gouv.fr" && body="ckan"` |
| `web.names: "opendatasoft.com"` | `domain="opendatasoft.com"` |
| `host.services.software.product = "GeoServer"` | `app="GeoServer"` |
| `web.endpoints.http.body: "/odweb/"` | `body="/odweb/"` |

### Starter queries

```text
title="CKAN"
body="name=\"generator\" content=\"ckan"
body="ckan-footer-logo"
body="profiles/dkan"
body="DKAN is an open-source data management platform"
title="CKAN" && country="PT"
body="ckan-footer-logo" && country="JP"
title="GeoNetwork"
body="GeoNetwork opensource"
app="GeoServer"
title="Socrata"
body="OpenDataSoft"
domain="opendatasoft.com"
host="opendata"
cert="opendata"
title="数据开放" && country="CN"
body="/odweb/" && title="数据开放"
host="data.gxzf.gov.cn"
title="Dataverse"
body="DSpace"
title="PxWeb"
```

Paste these in the FOFA web search box, or Base64-encode them for the API (`qbase64`). Platform pages include a few FOFA rows where the query is not a 1:1 Censys translation or where FOFA coverage is stronger (ODWeb, Guangxi, Tianditu, MapGIS, Hyrax).

CKAN’s default footer splits “Powered by” and “CKAN” around the class `ckan-footer-logo`, so `body="Powered by CKAN"` is a weak CKAN query (85 hosts in September 2026, led by ckan.org). Prefer `body="name=\"generator\" content=\"ckan"` and the config-file queries in [discovery-opendata.md](discovery-opendata.md#ckan). `body="ckan.js"` and `js_name="ckan.js"` miss current installs.

DKAN has no `app="DKAN"`. `body="DKAN"` is a mention search (2261 hosts in September 2026). `body="dkan.js"` and `js_name="dkan.js"` return 0. Prefer `body="profiles/dkan"` for the Drupal 7 profile and `body="DKAN is an open-source data management platform"` for the DKAN 2 React shell, then the file queries in [discovery-opendata.md](discovery-opendata.md#dkan).

Tablion has no `app="Tablion"`. `body="Tablion"` is a mention search (38 hosts in September 2026) and also matches the Byzantine garment of that name. `domain="tabliondata.com"` only sees the marketing redirect. Tenant apps are `{org}.tabliondata.com`; find the names with `%.tabliondata.com` in Certificate Transparency, then the chrome queries in [discovery-opendata.md](discovery-opendata.md#tablion). `body="aristotle_mdr"` is the metadata registry, not Tablion.

### How to turn a FOFA hit into a registry URL

1. Prefer `host`, `domain`, or `link` in the result, not `ip`.
2. Try `https://{host}/` first (drop `:443`; keep a non-443 port only if the catalog really listens there), then the platform path (`/dataset`, `/geonetwork`, `/dataverse`, `/odweb/`).
3. If the hit is a site that only links the product, follow that product URL. Do not register the referring homepage.
4. Duplicate-check the hostname in DuckDB. For a path tenant, duplicate-check the full path, not the shared host.
5. Probe the public API path from the platform guide.
6. Skip hosts that only serve a login form, a default web-server page, or an internal dashboard.

FOFA often returns the same catalog on ports 80 and 443, or several vhosts on one IP. Deduplicate by hostname before probing. Never set `link` to a bare IP.

## ZoomEye and similar maps

These indexes overlap FOFA for East Asian and some European hosts that Google ranks poorly.

**[ZoomEye](https://www.zoomeye.org)**:

```text
title:"CKAN"
http.body:"ckan-footer-logo"
app:"GeoServer"
```

**[Netlas](https://app.netlas.io)** and **[Onyphe](https://www.onyphe.io)** expose similar `title` / `body` / `country` filters. Translate the same phrases; do not expect identical field names.

## URLScan, PublicWWW, and page-source search

**[urlscan.io](https://urlscan.io/search/)** searches recently crawled pages (good for new city portals):

```text
page.title:"CKAN"
page.title:"GeoNetwork"
page.url:"opendata" AND page.title:"data"
page.url:"/api/3/action" AND filename:json
```

**[PublicWWW](https://publicwww.com)** and **[nerdydata](https://www.nerdydata.com)** search HTML source across the web. They catch footer strings that Google tokenizes away:

```text
"ckan-footer-logo"
"od_80x15_blue.png"
"Powered by CKAN"
"GeoNetwork opensource"
"ods-theme"
"soda.demo.socrata.com"   # exclude this; look for soda. hosts instead
"dataverse.js"
```

Export hostnames, then duplicate-check. These services are noisy: always open the live catalog.

## Certificate Transparency and DNS

Catalogs often sit on predictable names. Search Certificate Transparency rather than brute-forcing DNS.

**[crt.sh](https://crt.sh)** (SQL-like `%` wildcards):

```text
%.opendata.%
opendata.%
data.%.gov.%
geoportal.%
geonetwork.%
%.hub.arcgis.com
%.opendatasoft.com
%.pozi.com
%.giscloud.com
%.spatial.t1cloud.com
%.webewid.pl
```

**[Censys certificates](https://platform.censys.io)** and **[Cloudflare Radar / CT](https://radar.cloudflare.com)** can list the same names.

Useful hostname prefixes: `data.`, `opendata.`, `datos.`, `donnees.`, `geo.`, `geoportal.`, `metadata.`, `catalog.`, `ckan.`, `dkan.`, `gis.`, `maps.`, `indicators.`, `stats.`, `microdata.`, `nada.`.

A certificate name is not a catalog. Resolve it, then confirm a catalog UI.

## Common Crawl and web archives

When a site is gone from Google but you need the catalog root:

- [Common Crawl CDX](https://index.commoncrawl.org) — URL patterns such as `*.ckan.*`, `*/geonetwork/*`
- [Internet Archive CDX](https://web.archive.org) — `https://web.archive.org/cdx/search/cdx?url=data.example.gov/*&output=json`
- [Web Data Commons](http://webdatacommons.org/structureddata/) — `schema.org/Dataset` / DCAT pages (noisy; use as a lead list)

Prefer the live URL for `link`. Use archives only to recover a name or to mark `status: inactive`.

## Technology lookup (verify, not hunt)

Once you have a hostname, these tools confirm `software.id`. They are weak for hunting unknown sites.

| Tool | What it tells you |
|------|-------------------|
| [Wappalyzer](https://www.wappalyzer.com) / browser extension | JS frameworks, CMS, sometimes CKAN / Socrata |
| [BuiltWith](https://builtwith.com) | Similar, plus historical tech |
| Browser **View source** / Network tab | `/api/3`, `/srv/api`, `/api/explore`, `/arcgis/rest` |
| `https://host/robots.txt` and `/sitemap.xml` | Hidden API or catalog paths |
| HTTP headers | `X-Socrata-*`, `Server:`, cookies named `ckan` / `geonetwork` |

Cross-check at least two signals before setting `software.id`. If nothing matches, use `custom`.

## Official and community lists (still first)

Search engines miss less when you start from a list. Highest yield:

| Source | Typical software |
|--------|------------------|
| [CKAN ecosystem](https://ecosystem.ckan.org/dataset/ckan-sites-metadata) | `ckan` (also `scripts/sync_ckan_ecosystem.py`) |
| [Datashades](https://datashades.info/) | CKAN and others |
| [data.europa.eu catalogues](https://data.europa.eu/data/catalogues) | National EU catalogs |
| [GeoNetwork gallery](https://github.com/geonetwork/doc/blob/develop/source/annexes/gallery/gallery-urls.csv) | `geonetwork` |
| [INSPIRE geoportal](https://inspire-geoportal.ec.europa.eu/) | European SDI catalogs |
| [re3data](https://www.re3data.org/) | Scientific repositories |
| [OpenAIRE Graph data sources](https://graph.openaire.eu/docs/apis/graph-api/data-sources/) | Scientific repositories (`scripts/extract_openaire_portals.py`) |
| [Dataverse installations](https://iqss.github.io/dataverse-installations/data/data.json) | `dataverse` |
| [STAC Index](https://stacindex.org/catalogs) | STAC |
| [ArcGIS Hub](https://hub.arcgis.com/) | `arcgishub` |
| [Open Data Inception](https://data.opendatasoft.com/explore/dataset/open-data-sources%40public/information/) | Mixed open data |
| [ROAR](http://roar.eprints.org) | Repositories (`eprints`, `dspace`, …) |
| [OpenDOAR](https://v2.sherpa.ac.uk/opendoar/) | Open-access repositories by country/software |
| [GBIF IPT](https://www.gbif.org/ipt) | `ipt` |
| [ODIS catalogue](https://catalogue.odis.org/) | Ocean catalogs |
| [CoreTrustSeal](https://www.coretrustseal.org/) | Certified repos with a public dataset catalog |
| [WMO WIS2 GDC](https://gdc.wis.cma.cn/) | Meteorological node catalogs |
| National harvest APIs | Origin catalogs behind data.go.id, datos.gob.es, opendata.swiss, data.gov.ru, search.open.canada.ca, data.gouv.fr, govdata.de, data.go.kr, dane.gov.pl |

More lists and the hunt-pattern table: [discovery.md](discovery.md#existing-lists-start-here), [discovery.md](discovery.md#hunt-patterns).

## Duplicate check (do this constantly)

```sql
SELECT id, uid, name, link, catalog_type, status,
       software.id AS software_id
FROM catalogs
WHERE lower(link) LIKE '%example.gov%'
   OR id = 'examplegov';
```

Match `www` vs bare host, `http` vs `https`, and `/data` vs `/`. `DUPLICATE_LINK` / `DUPLICATE_LINK_NORMALIZED` fail quality checks.

## Conduct

- Public catalog metadata only. Stop on `401`/`403`. Do not follow login forms or guess API keys.
- Space out live GETs (about one to two seconds between hosts). Search-engine queries do not hit the catalog until you verify.
- Respect `robots.txt` and site terms when you fetch the candidate itself.
- Do not collect personal data or non-public APIs.
- Do not add internet-wide scanners, mass port scans, or recursive crawlers to this repository.

## Related

- [discovery.md](discovery.md) — overview and accept/reject rules
- [discovery-opendata.md](discovery-opendata.md)
- [discovery-geoportals.md](discovery-geoportals.md) ([SDI](discovery-geoportals-sdi.md), [viewers](discovery-geoportals-viewers.md))
- [discovery-scientific.md](discovery-scientific.md) ([domain](discovery-scientific-domain.md))
- [discovery-metadata.md](discovery-metadata.md)
- [discovery-indicators.md](discovery-indicators.md)
- [agents/discover.md](agents/discover.md)
- [discovery-agent-tools.md](discovery-agent-tools.md)
