# Discovering open data portals

How to find **open data portal** installations (`catalog_type: Open data portal`) that are not yet in this registry. Search-engine syntax (Google, Censys, Shodan, and [FOFA as a Censys alternative](discovery-search-tools.md#fofa)): [discovery-search-tools.md](discovery-search-tools.md). Overview and accept/reject rules: [discovery.md](discovery.md). Also covered here: Idra (`idra`), a DCAT-AP federation layer that is usually typed as a **Data search engine**; Piveau, Our Open Data, Gipuzkoa Irekia, DataPress, Taiwan MODA, ResourceContracts, RDF Online Repository, the Guangxi Public Data Open Platform, ODWeb, ATM Maggioli, OpenGov, OPENDATAENTE, KUKAN, the Epoint Big Data Open Platform, Taiji Digital, BODIK ODCS, and the jig.jp Open Data Platform.

Set `software.id` from `data/software/` only when a probe or page signal matches. Otherwise `custom`. After YAML exists: `python scripts/apidetect.py detect-single {id} --dryrun` (replace `{id}` with the catalog id).

## CKAN (`ckan`) {#ckan}

Most common self-hosted open-data CMS. Gallery: [CKAN ecosystem](https://ecosystem.ckan.org/dataset/ckan-sites-metadata) (automated: `python scripts/sync_ckan_ecosystem.py --dry-run`) and [Datashades](https://datashades.info/). GitHub method for server apps: [discovery-search-tools.md](discovery-search-tools.md#github).

**Signals:** `<meta name="generator" content="ckan {version}">`; footer class `ckan-footer-logo` in [footer.html](https://github.com/ckan/ckan/blob/master/ckan/templates/footer.html); static files `/base/images/ckan.ico` and `/base/images/od_80x15_blue.png`; asset paths containing `ckanext-`; Beaker session cookie `ckan`. The default footer is `<strong>Powered by</strong>` plus a separate `<a class="hide-text ckan-footer-logo" href="http://ckan.org">CKAN</a>`, so the page source usually lacks the contiguous phrase “Powered by CKAN”. Current installs load hashed webassets (2.9+) or `fanstatic/base` (2.8). A script named `ckan.js` is rare.

**Confirm (GET):** `https://host/api/3/action/status_show` and/or `/api/3/action/package_list`. JSON with `"success": true` is enough. Scientific data repositories may also be `ckan` when that API matches (AuScope Data Repository, `generator` CKAN 2.10.1; Observatorio Medioambiental La Plata, `generator` CKAN 2.7.3). HTML that mentions “ckan” is not enough when `status_show` returns HTML or 503 (INAIL `dati.inail.it`). An `og:url` pointing at a CKAN test host is not enough when `status_show` 404s (NIRD `archive.sigma2.no`).

**GitHub: read `ckan.site_url`, skip the fork list.** Forks of [ckan/ckan](https://github.com/ckan/ckan), [ckan/ckan-docker](https://github.com/ckan/ckan-docker), [okfn/docker-ckan](https://github.com/okfn/docker-ckan), and [keitaroinc/docker-ckan](https://github.com/keitaroinc/docker-ckan) are the software and Compose templates. `CKAN_SITE_URL` in those trees is `localhost`, `ckan:5000`, or `nginx:8080`. Code search does not index most forks, and paginating these forks does not list portals.

The public URL, when someone committed it, is in one of these files:

| File | Where the URL sits |
|------|--------------------|
| `ckan.ini` (and `ckan.ini.j2`) | `ckan.site_url` — CKAN 2.9+ |
| `production.ini` | `ckan.site_url` — CKAN 2.8 and earlier |
| `.env`, README, shell | `CKAN_SITE_URL=` |

```bash
gh api -H "Accept: application/vnd.github.text-match+json" \
  "search/code?q=%22ckan.site_url%20%3D%20https%3A%2F%2F%22&per_page=100"
gh api -H "Accept: application/vnd.github.text-match+json" \
  "search/code?q=ckan.site_url+https%3A%2F%2F+extension%3Aini&per_page=100"
gh api -H "Accept: application/vnd.github.text-match+json" \
  "search/code?q=%22CKAN_SITE_URL%3Dhttps%3A%2F%2F%22&per_page=100"
```

Keep a literal hostname (`https://energydata.info`, `https://danepubliczne.gov.pl`, `https://data.openpeoria.com`, `https://openafrica.net` in a README). Skip `localhost`, `127.0.0.1`, docker DNS names, unsubstituted `{{ }}` / `${VAR}` / `<%= %>`, `example.com`, `.env.example`, and hosts marked notprod, test, or staging unless that host is the public catalog. Then GET `status_show`. In September 2026 `"ckan.site_url = https://"` had about 40 code hits and `"CKAN_SITE_URL=https://"` about 100, and most of both were templates.

**FOFA** (checked September 2026). Google’s `"Powered by CKAN"` still matches the visible footer. FOFA, Censys, Shodan, and PublicWWW search HTML source, where those two words are not adjacent. FOFA has no `app="CKAN"`. `js_name="ckan.js"` returned 0 and `body="ckan.js"` returned 22. `body="webassets"` matches tens of thousands of unrelated hosts. `body="/api/3/action/status_show"` returned 8 because that path is not in the HTML. `body="Powered by CKAN"` returned 85, and the first host was ckan.org.

| Query | Hits | What it matches |
|-------|------|-----------------|
| `body="name=\"generator\" content=\"ckan"` | 5607 | generator meta `ckan {version}` |
| `body="ckanext-"` | 4253 | extension assets, including themes that drop the footer |
| `header="ckan="` | 4278 | Beaker cookie; also docs.ckan.org; `header=` is often off on free plans |
| `body="ckan-footer-logo"` | 3638 | default footer class |
| `body="docs.ckan.org"` | 2966 | footer “CKAN API” link |
| `body="od_80x15_blue.png"` | 2898 | Open Definition badge in the default footer |
| `body="/base/images/ckan.ico"` | 2809 | default favicon; a custom favicon drops this |
| `body="fanstatic/base"` | 929 | CKAN 2.8 and earlier |
| `title="CKAN"` | 1092 | default title suffix; branded titles are absent |
| `body="Powered by CKAN"` | 85 | themes that flatten the split footer, plus ckan.org |

Use the generator query first. Add `ckan-footer-logo` or `ckanext-` when a theme replaces `base.html`. Add `country=` or `host=` for a single-country hunt. When `body=` is not on the plan, fall back to `title="CKAN"` and expect branded portals to be missing. Deduplicate `http`/`https` and `www`.

| Tool | Query |
|------|-------|
| Google | `"ckan-footer-logo" OR "od_80x15_blue.png" -site:ckan.org` |
| Google | `"Powered by CKAN" inurl:/dataset -site:github.com -site:ckan.org` |
| Google | `inurl:/api/3/action/status_show` |
| Censys (web) | `web.endpoints.http.body: "ckan-footer-logo"` |
| Censys (web) | `web.endpoints.http.body: "name=\"generator\" content=\"ckan"` |
| FOFA | `body="name=\"generator\" content=\"ckan"` |
| FOFA | `body="ckan-footer-logo"` |
| FOFA | `body="ckanext-"` |
| FOFA | `body="/base/images/ckan.ico"` |
| FOFA | `body="fanstatic/base"` |
| FOFA | `title="CKAN" && country="PT"` |
| Shodan | `http.html:"ckan-footer-logo"` |
| PublicWWW | `"ckan-footer-logo"` or `"od_80x15_blue.png"` |
| GitHub code | `"ckan.site_url = https://"` |
| GitHub code | `"CKAN_SITE_URL=https://"` |

**False positives:** ckan.org, docs.ckan.org, demo.ckan.org, Datopian onboarding hosts, the same catalog on ports 80 and 443, CKAN extensions that are not a portal, harvest *sources* listed inside another CKAN. Prefer the catalog homepage, not `/dataset/{slug}`.

**Paths:** `/dataset`, `/organization`, `/api/3`, `/data.json`, `/catalog.xml`. Some installs live under `/data` or `/opendata` — probe `https://host/data/api/3/action/status_show` as well.

## Andino (`andino`) {#andino}

Docker-packaged CKAN distribution from the Argentine Republic (datos.gob.ar): CKAN core plus `gobar_theme`, `series_explorer`, `gobar_ckan_harvester`, and `xlsx_harvester`. Powers Argentina's national portal and provincial/municipal/agency portals; the national modernization office also hosts municipal instances under `*.paisdigital.modernizacion.gob.ar` / `*.paisdigital.innovacion.gob.ar`. Repo: [datosgobar/portal-andino](https://github.com/datosgobar/portal-andino).

**Confirm (GET):** `https://host/api/3/action/status_show` — extensions list contains `gobar_theme`. Homepage HTML includes "andino" or "gobar" (theme assets). Plain CKAN `status_show` without `gobar_theme` is `ckan`, not `andino`.

[footer.html](https://github.com/datosgobar/ckanext-gobar-theme/blob/main/ckanext/gobar_theme/templates/footer.html) sets `class="gobar-footer-grid"` (6 hosts in September 2026, all `datos.gob.ar` / `andino-v2.datos.gob.ar`). [base.html](https://github.com/datosgobar/ckanext-gobar-theme/blob/main/ckanext/gobar_theme/templates/base.html) loads the `gobar_theme` asset (the same 6 hosts). `body="andino" && country="AR"` matched 843, and the first hits are `reservadoncarmelo.unsj.edu.ar` and a geology lab, not Andino portals.

| Tool | Query |
|------|-------|
| Google | `"andino" inurl:/dataset site:.gob.ar OR site:.gov.ar` |
| Google | `"gobar_theme" OR "portal-andino"` |
| Censys | `web.endpoints.http.body: "gobar-footer-grid"` |
| FOFA | `body="gobar-footer-grid"` |
| Censys | `web.endpoints.http.body: "gobar_theme"` |
| FOFA | `body="gobar_theme"` |

**False positives:** the datosgobar GitHub/docs pages, blog posts about Andino. Register the portal root, not the repo.

## BODIK ODCS (`bodikodcs`) {#bodikodcs}

Hosted Japanese municipal open-data catalogs from the Big Data & Open Data Initiative Kyushu. Gallery: [odcs.bodik.jp](https://odcs.bodik.jp/). Tenant URL `https://odcs.bodik.jp/{lgcode}` (6-digit local-government code). Shared CKAN API: [data.bodik.jp](https://data.bodik.jp/). Organization list: `GET https://data.bodik.jp/api/3/action/organization_list`.

**Signals:** host `odcs.bodik.jp` or `data.bodik.jp`; WordPress theme `bodik_odcs`; footer credit to 九州先端科学技術研究所.

**Confirm:** the tenant page lists datasets, or `package_search?q=organization:{lgcode}` returns that municipality. One record per local government. The aggregate `data.bodik.jp` catalog is the shared API host, not a second copy of each tenant. Skip non-municipality organization ids (`city`, `isit`, and similar slugs). Plain CKAN on any other host stays `ckan`.

[base.html](https://github.com/ISITBODIK/odpkg-docker/blob/master/ckan/ckanext-bodik_theme/ckanext/bodik_theme/templates/base.html) links `/bodik_odcs.css` (8 hosts in September 2026, including `data.bodik.jp`, `gifu-opendata.pref.gifu.lg.jp`, and `ckan.pf-sapporo.jp`). `body="bodik_odcs"` matched 4, including the WordPress gallery `odcs.bodik.jp`, which does not serve that stylesheet. Keep the host query for gallery tenants.

| Tool | Query |
|------|-------|
| Google | `site:odcs.bodik.jp` |
| Google | `"BODIK ODCS" オープンデータ` |
| Censys | `web.endpoints.http.body: "bodik_odcs.css"` |
| FOFA | `body="bodik_odcs.css"` |
| Censys | `web.endpoints.http.body: "bodik_odcs"` |
| FOFA | `body="bodik_odcs"` |
| FOFA | `host="odcs.bodik.jp"` |

## jig.jp Open Data Platform (`jigodp`) {#jigodp}

Hosted municipal catalog from B Inc. Product site: [odp.jig.jp](https://odp.jig.jp/). Shared CKAN: [ckan.odp.jig.jp](https://ckan.odp.jig.jp/). Municipalities are organizations inside that one catalog.

**Signals:** host `odp.jig.jp` or `ckan.odp.jig.jp`; `GET /api/3/action/status_show` extensions include `odp`.

**Confirm:** the status payload lists `odp` and `package_search` returns datasets. One record for the shared catalog, not one record per municipality organization. Other CKAN sites stay `ckan`.

| Tool | Query |
|------|-------|
| Google | `site:odp.jig.jp` |
| Google | `"ckan.odp.jig.jp"` |
| Censys | `web.endpoints.http.body: "ckan.odp.jig.jp"` |
| FOFA | `host="ckan.odp.jig.jp"` |

## DKAN (`dkan`) {#dkan}

Drupal portal from [GetDKAN](https://github.com/GetDKAN/dkan). Two public shells, checked September 2026:

- **DKAN 1** (Drupal 7 install profile [dkan-drops-7](https://github.com/GetDKAN/dkan-drops-7)). HTML serves `profiles/dkan/` and, on the default theme, `nuboot_radix`. The generator meta says Drupal 7. The “Powered by DKAN” block is easy to remove.
- **DKAN 2** (Drupal `getdkan/dkan` plus the React shell [data-catalog-app](https://github.com/GetDKAN/data-catalog-app)). The shell’s `index.html` ships the title `DKAN data catalog`, the meta description `DKAN is an open-source data management platform.`, and `/dkan-avatar-blue.png` (often copied to `/frontend/build/`). A custom title keeps the description. The Drupal backend HTML can omit the string `dkan`.

**Confirm.** DKAN 1: homepage HTML contains `profiles/dkan`. When the API is open, `GET /api/3/action/site_read` returns `"success": true`, and `GET /data.json` is Project Open Data JSON (Czech Telecommunication Office, Alaska Conservation Science Catalog). `GET /api/3/action/package_search` and `GET /api/1/search` 404 on several live DKAN 1 hosts, so a 404 there does not rule the profile out. DKAN 2: `GET /api/1/metastore/schemas/dataset` returns a JSON schema (`data.bmel.cloud`, `webktim.ellak.gr`, `datosabiertos.rosario.gob.ar`). A CKAN Action API with no `profiles/dkan` path and no metastore schema is [`ckan`](#ckan). `profiles/contrib/ekan` or `ekan_theme` is [`ekan`](#ekan).

**GitHub: read the project file, then the README.** Forks of [GetDKAN/dkan](https://github.com/GetDKAN/dkan) (about 170) and [GetDKAN/dkan-drops-7](https://github.com/GetDKAN/dkan-drops-7) (about 35) are the software and the Pantheon upstream. Code search does not index most forks. The drops-7 homepage field stays empty; two forks name a portal in `homepage` or the README ([inptdat.de](https://www.inptdat.de), diversicon-kb.eu). Forks of [data-catalog-app](https://github.com/GetDKAN/data-catalog-app) are frontends whose README is still the starter text.

The committed files that identify a deployment:

| File | What it holds |
|------|----------------|
| `composer.json`, `composer.lock` | `"getdkan/dkan"` — a DKAN 2 project. The public URL is usually absent. `"getdkan/dkan" filename:composer.json` was about 12 hits, and several are GetDKAN itself (`Ktimatologio/opendata` is a real portal repo). |
| `.env.production`, `.env.development`, `src/frontend/.env.*`, `docroot/frontend/.env.*` | `REACT_APP_ROOT_URL` or `VITE_REACT_APP_ROOT_URL`. The value is usually the relative path `"/api/1"`, so the hostname is the published site. An absolute `https://` value is the API host. |
| `src/assets/config.json`, `src/frontend/src/assets/config.json` | display name in `site` / `slogan` |
| `index.html` (data-catalog-app) | default title, description, and `dkan-avatar-blue.png` — the FOFA strings below |
| README | sometimes the only public URL |

`dktl.yml` is often empty. DKAN Tools serves `{slug}.localtest.me`. `$base_url` next to `dkan` in PHP was about 52 hits, and the sampled `sites/default/settings.php` files still had the commented `example.com` line.

```bash
gh api -H "Accept: application/vnd.github.text-match+json" \
  "search/code?q=%22getdkan%2Fdkan%22+filename%3Acomposer.json&per_page=100"
gh api -H "Accept: application/vnd.github.text-match+json" \
  "search/code?q=%22REACT_APP_ROOT_URL%22+%22%2Fapi%2F1%22&per_page=100"
```

The second query also hits `VITE_REACT_APP_ROOT_URL` (18 hits in September 2026, almost all `"/api/1"`). Keep a literal hostname. Skip `dkan.localtest.me`, `example.com`, and unsubstituted `${VAR}`. `"GATSBY_API_URL=https://"` is any Gatsby app (about 100 hits). `DYNAMIC_API_URL` is unrelated (about 220 hits). The older Gatsby frontend only counts when `GATSBY_API_URL` sits next to `/api/1`.

**FOFA** (checked September 2026). FOFA has no `app="DKAN"`. `body="dkan.js"` and `js_name="dkan.js"` returned 0. `body="modules/contrib/dkan"` and `body="data-catalog-frontend"` returned 0 (those paths are not in the HTML). `body="sites/all/modules/dkan"` returned 1 (pre-profile layout). `body="DKAN"` returned 2261 and is a mention search (blogs, vendors, reviews). `body="Powered by DKAN"` returned 8. `body="/api/1/datastore"` returned 19 and the first hosts were unrelated healthcare sites. `header="dkan"` was noisy.

| Query | Hits | What it matches |
|-------|------|-----------------|
| `body="profiles/dkan"` | 199 | DKAN 1 install profile in CSS/JS; survives a theme that drops the footer |
| `body="nuboot_radix"` | 199 | DKAN 1 default theme |
| `body="dkan_dataset.css"` | 199 | DKAN 1 dataset stylesheet |
| `body="dkan_sitewide_dataset_search_form"` | 165 | DKAN 1 homepage search form; a replaced form drops this |
| `body="getdkan.org"` | 44 | footer link, plus getdkan.org |
| `body="DKAN is an open-source data management platform"` | 22 | DKAN 2 React shell, including retitled portals |
| `body="dkan-avatar-blue.png"` | 14 | DKAN 2 default icon; also getdkan.org and `demo.*` |
| `title="DKAN data catalog"` | 8 | untouched DKAN 2 `<title>` |
| `title="DKAN"` | 35 | default title, plus shops such as dkan.co.th |
| `body="Powered by DKAN"` | 8 | DKAN 1 sites that kept the footer block |

Use `profiles/dkan` for DKAN 1 and the default meta description for DKAN 2. Add `country=` or `host=` for a single-country hunt. Deduplicate `http`/`https` and `www`. A DKAN 2 backend with a fully custom frontend has neither string; confirm it with the metastore schema.

| Tool | Query |
|------|-------|
| Google | `"profiles/dkan" OR "nuboot_radix" -site:github.com` |
| Google | `"dkan-avatar-blue.png" OR "DKAN is an open-source data management platform"` |
| Google | `inurl:/api/1/metastore/schemas/dataset` |
| Censys (web) | `web.endpoints.http.body: "profiles/dkan"` |
| Censys (web) | `web.endpoints.http.body: "DKAN is an open-source data management platform"` |
| FOFA | `body="profiles/dkan"` |
| FOFA | `body="nuboot_radix"` |
| FOFA | `body="dkan_sitewide_dataset_search_form"` |
| FOFA | `body="DKAN is an open-source data management platform"` |
| FOFA | `body="dkan-avatar-blue.png"` |
| Shodan | `http.html:"profiles/dkan"` |
| Shodan | `http.html:"dkan-avatar-blue.png"` |
| GitHub code | `"getdkan/dkan" filename:composer.json` |
| GitHub code | `"REACT_APP_ROOT_URL" "/api/1"` |

**False positives:** getdkan.org, `demo.webktim.ellak.gr`, `demodkan.*.zyxware.com`, dkan.co.th and other “DKAN” shops, the same catalog on ports 80 and 443, DKAN extension repos. Prefer the catalog homepage. A description hit whose metastore schema 404s (`data.ncsi.gov.om`, `otvoreni.oprtalj.hr` in this pass) still needs another confirm before `software.id` is `dkan`.

## EKAN (`ekan`) {#ekan}

Eighty Options Drupal 9/10 distribution and the upgrade path for Drupal 7 DKAN 1.0 sites. Product: [ekan-data.org](https://www.ekan-data.org/). Drupal project: [drupal.org/project/ekan](https://www.drupal.org/project/ekan). Distinct from GetDKAN ([`dkan`](#dkan)).

**Confirm:** HTML serves `/profiles/contrib/ekan/` or `ekan_theme` (or a subtheme such as `ouc_ekan_theme`) **and** Drupal 9+. Dataset list is Drupal JSON:API `/jsonapi/dataset/dataset` when public; many INFORM/Cyprus sites also publish `/data.json`. The CKAN-style `/api/3` and GetDKAN `/api/1/metastore` routes are **absent**.

| Tool | Query |
|------|-------|
| Google | `"ekan_theme" OR inurl:/profiles/contrib/ekan` |
| Google | `"EKAN Datastore" OR "ekan_search"` |
| Censys | `web.endpoints.http.body: "ekan_theme"` |
| FOFA | `body="profiles/contrib/ekan"` |
| FOFA | `body="ekan_theme.style.css"` |
| Shodan | `http.html:"ekan_theme"` |

**False positives:** the product homepage, Packagist/Drupal.org project pages, Eighty Options staging hosts (`*.eightyoptions.com.au`), the vendor demo. Register the public catalog root. Login-only Drupal apps on the same vendor (TREDS, Indicator Reporting Tool) are not catalogs.

## OpenDataSoft (`opendatasoft`) {#opendatasoft}

SaaS and self-hosted Explore portals. Many hosts end in `*.opendatasoft.com` or use a custom domain with `/explore`. Huwise is the same product after the rebrand (`*.huwise.com` and custom domains that no longer say OpenDataSoft).

**Confirm:** `https://host/api/explore/v2.1/catalog/datasets` (or legacy `/api/v2/catalog/datasets/`). UI path `/explore`.

`domain="opendatasoft.com"`, `body="OpenDataSoft"`, and `body="ods-explore"` miss Huwise-branded hosts and custom domains that dropped the old name. Checked 24 September 2026: `domain="huwise.com"` returned 77. `body="ods-front-header" && domain!="opendatasoft.com"` returned 399. `body="huwise-black.svg"` returned 90 custom-domain rows. `body="opendatasoft-staticfileset"` returned 259 custom-domain rows. `body="ods-widgets" && body!="ods-front-header"` returned 119 and is mostly widget embeds, not portals.

| Tool | Query |
|------|-------|
| Google | `inurl:/explore "opendatasoft" -site:opendatasoft.com/blog` |
| Google | `site:opendatasoft.com/explore` |
| Google | `"Powered by OpenDataSoft" OR "ods-explore"` |
| Google | `site:huwise.com/explore` |
| Censys | `web.names: "opendatasoft.com"` |
| FOFA | `domain="opendatasoft.com"` |
| FOFA | `domain="huwise.com"` |
| Censys | `web.endpoints.http.body: "OpenDataSoft"` |
| FOFA | `body="OpenDataSoft"` |
| FOFA | `body="ods-explore"` |
| FOFA | `body="ods-front-header"` |
| FOFA | `body="huwise-black.svg"` |
| FOFA | `body="opendatasoft-staticfileset"` |
| FOFA | `body="OpenDataSoft" && country="BE"` |
| crt.sh | `%.opendatasoft.com` |
| crt.sh | `%.huwise.com` |

**False positives:** the vendor homepage, academy, and blog; widget embeds; login walls; a second hostname of the same `domain_id`. Register the **portal** (`{org}.opendatasoft.com`, `{org}.huwise.com`, or the city’s custom domain), not `www.opendatasoft.com`. List: [Open Data Inception](https://data.opendatasoft.com/explore/dataset/open-data-sources%40public/information/).

## Socrata (`socrata`) {#socrata}

Tyler / Socrata Open Data. UI often `/browse` or `/datasets`. SODA API under `/api/views`. Network: [opendatanetwork.com](https://www.opendatanetwork.com/search?q=).

**Confirm:** `https://host/api/views.json?limit=1` or `/api/views`. Many sites also serve `/data.json`. Headers may include `X-Socrata-*`.

| Tool | Query |
|------|-------|
| Google | `inurl:/browse "socrata" OR "open data network"` |
| Google | `"Powered by Socrata" OR inurl:/api/views` |
| Google | `site:*.socrata.com` (custom domains are more interesting) |
| Censys | `web.endpoints.http.body: "socrata"` |
| FOFA | `header="X-Socrata"` |
| FOFA | `body="socrata"` |
| FOFA | `body="Powered by Socrata"` |
| Shodan | `http.html:"X-Socrata" OR http.html:"soda.demo"` |

Skip `soda.demo.socrata.com` and Tyler marketing sites. Prefer the city’s production domain.

## uData (`udata`) {#udata}

French-origin portal (data.gouv.fr lineage). Dataset UI `/datasets/`. API `/api/1/datasets/`.

**Confirm:** `https://host/api/1/datasets/?page_size=1` returns JSON with `data` / `total`.

The default theme footer [udata_front/theme/gouvfr/templates/footer.html](https://github.com/datagouv/udata-front/blob/master/udata_front/theme/gouvfr/templates/footer.html) links `https://github.com/opendatateam/udata/` (16 hosts in September 2026, including `demo.data.gouv.fr`). The visible label is translated, so `body="Open-source engine: udata"` matched 1 host. `body="udata"` matched about 20,000 unrelated hosts. Production themes often drop the engine link, so a miss there still needs the API check.

| Tool | Query |
|------|-------|
| Google | `"opendata" inurl:/datasets site:.gouv.fr` |
| Google | `"udata" "jeux de données" OR inurl:/api/1/datasets` |
| Censys | `web.endpoints.http.body: "github.com/opendatateam/udata/"` |
| FOFA | `body="github.com/opendatateam/udata/"` |
| Censys | `web.names: "data.gouv"` |
| FOFA | `domain="data.gouv"` |

Local clones exist outside France. Do not assume every `/api/1/datasets` is uData — check the JSON shape.

## PortalJS (`portaljs`) {#portaljs}

Datopian catalog frontend. Product: [PortalJS](https://www.portaljs.com/). Showcase: [data portals](https://www.portaljs.com/data-portals). Live shells include [opendata.malmo.se](https://opendata.malmo.se/), [data.hounslow.gov.uk](https://data.hounslow.gov.uk/), [data.lincolnshire.gov.uk](https://data.lincolnshire.gov.uk/), [www.opendatani.gov.uk](https://www.opendatani.gov.uk/), [opendatanepal.com](https://opendatanepal.com/), and [portal.transport-data.org](https://portal.transport-data.org/).

**Signals:** footer “PortalJS” or “PortalJS on CKAN Backend”; dataset path `/@{org}/{slug}` (a locale prefix such as `/en` may sit in front).

**Confirm:** GET the catalog home or `/search` and match that footer plus a dataset link. One portal host = one record. Do **not** register `portaljs.com` marketing, `arc.portaljs.com` sign-in, or GitHub example repos. A CKAN Action API on the same host or on a linked `admin.` / `api.` / `ckan.` host stays with this catalog; do **not** set `ckan` for the public PortalJS shell, and do **not** add the API host as a second catalog.

| Tool | Query |
|------|-------|
| Google | `"PortalJS on CKAN Backend" OR "Powered by PortalJS"` |
| Google | `inurl:/@ "PortalJS" (dataset OR "open data")` |
| Censys | `web.endpoints.http.body: "PortalJS on CKAN Backend"` |
| FOFA | `body="PortalJS"` |

## Magda (`magda`) {#magda}

Search-centric catalog (data.gov.au and derivatives). API `/api/v0/search/datasets` or `/search/api/v0/search/datasets`.

**Confirm:** that search endpoint returns JSON datasets. UI often `/search` or `/dataset`.

[magda-web-client/public/index.html](https://github.com/magda-io/magda/blob/main/magda-web-client/public/index.html) requests `/api/v0/content/favicon.ico` (13 hosts in September 2026). `body="magda"` is not usable: it matched about 67,000 unrelated hosts.

| Tool | Query |
|------|-------|
| Google | `"magda" "data catalog" OR inurl:/api/v0/search/datasets` |
| Google | `inurl:/search/api/v0/search/datasets` |
| Censys | `web.endpoints.http.body: "/api/v0/content/favicon.ico"` |
| FOFA | `body="/api/v0/content/favicon.ico"` |

## JKAN (`jkan`) {#jkan}

Jekyll + CKAN-like static portal. Often GitHub Pages. Datasets as Markdown in `_datasets/`, listed at `/datasets/`. Project: [jkan.io](https://jkan.io). The fork parent for public installs is [timwis/jkan](https://github.com/timwis/jkan). General GitHub method (forks plus code search): [discovery-search-tools.md](discovery-search-tools.md#github).

**Signals:** `_config.yml` key `jkan_theme`; page or repo text “backend-free open data portal”; DCAT-US `GET /data.json` or `GET /datasets.json` with a `dataset` array. No CKAN Action API. A `status_show` body that includes `ckan_version` is CKAN, not JKAN.

**Confirm:** the dataset list or `data.json` has entries beyond the stock “Sample dataset”. One published site = one record. A custom domain and `{owner}.github.io/{repo}` that return the same `data.json` are one catalog (Swiss Heritage is [data.openglam.ch](https://data.openglam.ch/), not a second copy of the GitHub Pages URL). Several catalogs on one `github.io` host (`/LiveData/`, `/LiveDataNUM/`) are separate records; set `--id` so the host-only id does not collide.

**GitHub, do both.** Code search does not index most forks.

1. Forks: `GET /repos/timwis/jkan/forks` (`gh api`, paginate). `homepage` is often still `https://jkan.io` on forks that never edited it. Probe `https://{owner}.github.io/{repo}/data.json` anyway.
2. Detached copies (not forks): code search `jkan_theme filename:_config.yml`. Wider and noisier: `"backend-free open data portal"`.

**Skip:** [jkan.io](https://jkan.io), [demo.jkan.io](https://demo.jkan.io), untouched “Welcome to JKAN” templates, fictional training cities, empty `data.json`, and repos whose page says the catalog moved (Open Austin → data.world). `title="JKAN"` misses branded portals (OxOpenData, OpenKnoxville, A-GeoCat).

| Tool | Query |
|------|-------|
| GitHub forks | `repos/timwis/jkan/forks` |
| GitHub code | `jkan_theme filename:_config.yml` |
| GitHub code | `"backend-free open data portal"` |
| Google | `"JKAN" "open data" OR "jkan" inurl:/datasets` |
| Google | `site:github.io "JKAN"` |
| Censys | `web.endpoints.http.body: "jkan_theme"` |
| FOFA | `body="jkan_theme"` |
| FOFA | `body="timwis/jkan"` |
| FOFA | `body="backend-free open data portal"` |

`body="JKAN"` and `title="JKAN"` are weak: the short token matches unrelated hosts, and the real fingerprint sits in `_config.yml`, which FOFA does not see on GitHub Pages. In September 2026 the three longer FOFA queries returned only jkan.io, demo.jkan.io, and a report that mentions the project. Use GitHub first.

## KUKAN (`kukan`) {#kukan}

Open-source CKAN-compatible catalog from Info Lounge. Product site: [kukan.dev](https://kukan.dev/). Source: [kukan-project/kukan](https://github.com/kukan-project/kukan). Native API `/api/v1/packages`; CKAN read API `/api/3/action/package_search`.

**Signals:** page or footer text `KUKAN`; `GET /api/health` returns `{"status":"ok"}` together with CKAN-shaped `/api/3/action/package_search`. A CKAN `status_show` body that includes `ckan_version` is CKAN, not KUKAN.

**Confirm:** the package search JSON lists datasets and the health or UI names KUKAN. One catalog per installation. Skip kukan.dev marketing. Niigata Prefecture’s catalog is contracted and not public until March 2027.

| Tool | Query |
|------|-------|
| Google | `"KUKAN" ("データカタログ" OR "open data" OR "package_search") -site:kukan.dev -site:github.com` |
| Censys | `web.endpoints.http.body: "KUKAN"` |
| FOFA | `body="KUKAN" && body="package_search"` |

## Datasette (`datasette`) {#datasette}

Open-source SQLite publisher with a JSON/CSV API. Site and instance examples: [datasette.io](https://datasette.io/).

**Confirm:** GET the instance root. Title or footer `Datasette`; table/query UI; JSON at `/-/versions` or `/{database}.json`. Register the published instance, not each table or canned query. Skip datasette.io marketing and `lite.datasette.io` demos unless they are the catalog being registered.

The footer in `datasette/templates/_footer.html` is `Powered by <a ...>Datasette</a>`, so `body="Powered by Datasette"` matches nothing. The contiguous string is the alternate link type in `datasette/templates/base.html` (`application/json+datasette`, 544 hosts in September 2026). `datasette-manager.js` in the same template matched 47 hosts. Forks of [simonw/datasette](https://github.com/simonw/datasette) are the software, not a portal list.

| Tool | Query |
|------|-------|
| Google | `"Datasette" ("powered by" OR "explore this database") -site:datasette.io -site:github.com` |
| Google | `inurl:/-/versions Datasette` |
| Censys | `web.endpoints.http.body: "application/json+datasette"` |
| FOFA | `body="application/json+datasette"` |

## Datadex (`datadex`) {#datadex}

Serverless, local-first open-data pattern. Product page: [Datadex](https://datadex.datonic.io/). The implementation list is the [Datadex README](https://github.com/datonic/datadex#implementations). Live portals include [datania.cc](https://datania.cc/), [filecoindataportal.xyz](https://filecoindataportal.xyz/), and [grantsdataportal.xyz](https://grantsdataportal.xyz/).

**Signals:** page text “instance of Datadex”, or a dataset index of Parquet/CSV files next to a repository under [datonic/datadex](https://github.com/datonic/datadex). Filecoin’s about page names Datadex explicitly.

**Confirm:** GET the portal and find a list of downloadable tables. One portal host = one record. Skip [datadex.datonic.io](https://datadex.datonic.io/) (pattern homepage) and GitHub repos. Skip Hugging Face organization pages; those datasets already belong to the Hugging Face Datasets catalog. `body="datadex"`, `title="Datadex"`, and `host="datadex"` are mostly unrelated names (Hainan Data Exchange, Ficus DataDex, a Pokémon app, and pages that mention a token named DataDex).

| Tool | Query |
|------|-------|
| Google | `"instance of Datadex"` |
| Google | `"github.com/datonic/datadex" (datasets OR parquet) -site:github.com` |
| Censys | `web.endpoints.http.body: "instance of Datadex"` |
| FOFA | `body="instance of Datadex"` |
| FOFA | `body="local-first Data Platform"` |

## Junar (`junar`) {#junar}

SaaS open-data CMS used in Latin America. Customer list: [junar.com/customers](https://junar.com/customers/). Often `/data.json`.

| Tool | Query |
|------|-------|
| Google | `"powered by Junar" OR "junar" "datos abiertos"` |
| Censys | `web.endpoints.http.body: "Junar"` |
| FOFA | `body="Junar"` |

## EntryScape (`entryscape`) {#entryscape}

DCAT-AP catalogs, especially Sweden and Nordics. Customers: [entryscape.com/en/customers](https://entryscape.com/en/customers/). UI may be Blocks or the Catalog suite; API under `/store/`.

The suite shell [suite/stable/index.html](https://static.cdn.entryscape.com/suite/stable/index.html) sets `<title>EntryScape</title>`, points `dc.source` at `static.cdn.entryscape.com/suite/{version}/index.html`, and loads `bootstrap.js` from that path. The same response sends a Content-Security-Policy report to `security.entryscape.com`. The shell is `noindex, nofollow`, so Google misses hosts that FOFA still has.

Checked 24 September 2026. `title=="EntryScape"` is the exact suite title (144 hosts). `title="EntryScape"` is 152 and also matches “EntryScape Community” and “EntryScape Service Desk”. `body="static.cdn.entryscape.com/suite/"` is the same shell (136). `header="security.entryscape.com"` alone is 266, and the extra rows are mostly bare-IP 404s; keep it only together with the exact title. `domain="entryscape.net"` is the SaaS tenant list (165). Names such as `catalog-goteborg-se.entryscape.net` are often 404 aliases of a custom domain (`catalog.goteborg.se`) — register the custom domain. `body="static.entryscape.com"` is the older Blocks CDN (11) and still catches branded portals that do not use the suite title, including `www.opendata.sachsen.de`.

Do **not** hunt with `body="entryscape"` (195, including `docs.entryscape.com`, municipal homepages, and unrelated hosts such as `mtscapes.com`; `body=="entryscape"` is the same 195 because this plan stays in extended mode). `body="EntryStore"` matched 240 unrelated sites. `body="blocks-ext"` matched 18,061. `body="data-entryscape"` matched 9 (docs and embeds). `body="data-entryscape-entrystore"` and `body="static.cdn.entryscape.com/blocks/1/app.js"` matched 0 — FOFA does not index that attribute or the current Blocks script URL. `cert="entryscape.net"` and `cert="entryscape.com"` matched 2 hosts each. `host=".entryscape.com"` (63) is the vendor: docs, assets, demo, and dev.

A Blocks page whose `data-entryscape-entrystore` points at a store already registered (Miljödokument → `data.naturvardsverket.se`) is that catalog, not a second one. Skip `admin`, `editera`, `sandbox`, `staging`, `test`, `demo`, `dev`, `docs`, `assets`, and `support` hosts.

| Tool | Query |
|------|-------|
| Google | `"EntryScape" (catalog OR "öppna data" OR dcat)` |
| Google | `inurl:/store "entryscape"` |
| Censys | `web.endpoints.http.body: "EntryScape"` |
| FOFA | `title=="EntryScape"` |
| FOFA | `body="static.cdn.entryscape.com/suite/"` |
| FOFA | `header="security.entryscape.com" && title=="EntryScape"` |
| FOFA | `domain="entryscape.net"` |
| FOFA | `body="static.entryscape.com"` |

## Felles datakatalog (`fellesdatakatalog`) {#fellesdatakatalog}

Norwegian Digitalisation Agency's open-source federated metadata catalog. It powers
[data.norge.no](https://data.norge.no) and the transport-focused
[Transportportal](https://transportportal.no). Source:
[Informasjonsforvaltning/fdk-portal](https://github.com/Informasjonsforvaltning/fdk-portal).

**Signals:** `/config.js` defines `FDK_PORTAL_BASE_URI` and `SEARCH_SERVICE_HOST`;
the page title is “Felles datakatalog” or “Der Norge deler data”; the search service
host is `search.api.fellesdatakatalog.digdir.no`.

**Confirm:** GET `/config.js`, then POST `/search/datasets` on the configured search
service with `{"pagination":{"size":1,"page":1}}`. A JSON response with `hits` and
`page.totalElements` confirms the catalog. Transportportal is a distinct public
`TRANSPORT` profile; skip admin, demo, and staging environments.

[index.html](https://github.com/Informasjonsforvaltning/fdk-portal/blob/main/src/entrypoints/main/index.html) points Open Graph images at `cms.fellesdatakatalog.digdir.no` (2 hosts in September 2026, `transportportal.no`).

| Tool | Query |
|------|-------|
| Google | `"Felles datakatalog" (dataset OR datasett) -site:github.com` |
| Censys | `web.endpoints.http.body: "cms.fellesdatakatalog.digdir.no"` |
| FOFA | `body="cms.fellesdatakatalog.digdir.no"` |
| Censys | `web.endpoints.http.body: "FDK_PORTAL_BASE_URI"` |
| FOFA | `title="Felles datakatalog"` |
| FOFA | `title="Der Norge deler data"` |
| FOFA | `body="search.api.fellesdatakatalog"` |

## ArcGIS Hub as an open-data site (`arcgishub`) {#arcgishub}

Many Hub sites are **open data** first (dataset search, DCAT) rather than a map viewer. If the primary UI is a dataset catalog, use `catalog_type: Open data portal` and `software.id: arcgishub`. If it is a GIS hub / map gallery, use **Geoportal** — see [discovery-geoportals-sdi.md](discovery-geoportals-sdi.md#arcgishub).

**Confirm:** `/api/search/v1` or `/api/feed/dcat-us/1.1.json`. Hosts often `*.hub.arcgis.com` or `opendata.arcgis.com`. Custom-domain example: Bloemendaal (`hubcdn.arcgis.com/opendata-ui`).

Checked 24 September 2026. Same FOFA rules as [discovery-geoportals-sdi.md](discovery-geoportals-sdi.md#arcgishub): `host="hub.arcgis.com"` matches SaaS tenants (1,829) because `host=` is a substring, and custom domains need the CDN path plus `domain!="arcgis.com"` (2,676). `domain!="hub.arcgis.com"` does not exclude `*.hub.arcgis.com` — FOFA's `domain` field is the registrable domain `arcgis.com`.

| Tool | Query |
|------|-------|
| Google | `site:hub.arcgis.com "open data"` |
| Google | `site:opendata.arcgis.com` |
| Google | `inurl:hub.arcgis.com` |
| Censys | `web.names: "hub.arcgis.com"` |
| FOFA | `host="hub.arcgis.com"` |
| FOFA | `domain="opendata.arcgis.com"` |
| FOFA | `body="hubcdn.arcgis.com/opendata-ui" && domain!="arcgis.com"` |
| FOFA | `body="hub-site-head-content"` |
| crt.sh | `%.hub.arcgis.com` |

Do **not** use `body="opendata-ui"` as the custom-domain query (5,998, broader than the CDN path) or `body="hub.js"` (12,006, unrelated). Dataset-first sites stay Open data portal; map galleries stay Geoportal.

Gallery: [hub.arcgis.com](https://hub.arcgis.com/).


## Idra (`idra`) {#idra}

Open Data Federation Platform (FIWARE / Engineering Ingegneria Informatica). It harvests CKAN, DKAN, Socrata, OpenDataSoft, NGSI, and DCAT-AP sources into one search UI. Docs: [idra.readthedocs.io](https://idra.readthedocs.io). Source: [OPSILab/Idra](https://github.com/OPSILab/Idra).

Typical `catalog_type` is **Data search engine** (folder `search/`), not Open data portal: Idra is an aggregator over other ODMS catalogues.

**Signals:** path `/IdraPortal/`; REST under `/Idra/api/v1/`; SPARQL; DCAT-AP / DCAT-AP_IT branding.

**Confirm:** GET `https://host/IdraPortal/` (or `/Idra/api/v1/` JSON). Prefer a live production federation. The public demos (`idra.site`, `idra.opsilab.it`, `idra.eng.it`, sandbox hosts) are already registered and mostly **inactive** — do not re-add them.

| Tool | Query |
|------|-------|
| Google | `"Idra" ("Open Data Federation" OR IdraPortal OR "DCAT-AP_IT") -site:github.com -site:readthedocs.io` |
| Google | `inurl:/IdraPortal/ OR inurl:/Idra/api/v1/` |
| Censys | `web.endpoints.http.body: "IdraPortal"` |
| FOFA | `body="IdraPortal"` |
| Censys | `web.endpoints.http.body: "Idra"` |
| FOFA | `body="Idra"` |

Do not register harvested source catalogs a second time as Idra. Duplicate-check the underlying CKAN/Socrata/OpenDataSoft `link` as well.

## Liferay (`liferay`) {#liferay}

Digital experience CMS. **Only** register when a public Open Data / RISP dataset listing exists (common on Spanish provincial sites), not a generic Liferay intranet.

**Signals:** Liferay portal paths (`/web/guest/`); “datos abiertos” / RISP module; Excel/XML/JSON/CSV dataset tables.

**Confirm:** GET the open-data page and verify a reusable dataset list. Skip city hall homepages that only mention open data in a news article.

[portal_normal.ftl](https://github.com/liferay/liferay-portal/blob/master/modules/apps/frontend-theme/frontend-theme-classic/src/templates/portal_normal.ftl) links `http://www.liferay.com` from the powered-by footer (5,471 hosts in September 2026, including `nutricion.umsa.bo`). `body="Liferay"` matched 54,186. Sites that drop that footer still match the product name, so keep both.

| Tool | Query |
|------|-------|
| Google | `"datos abiertos" Liferay OR RISP (ayuntamiento OR diputación) site:.es` |
| Google | `inurl:/web/guest/ "datos abiertos"` |
| Censys | `web.endpoints.http.body: "http://www.liferay.com"` |
| FOFA | `body="http://www.liferay.com"` |
| Censys | `web.endpoints.http.body: "Liferay"` |
| FOFA | `body="Liferay"` |

## ATM Maggioli (`atmmaggioli`) {#atmmaggioli}

Spanish municipal sede electrónica / Portal de Transparencia with an open-data catalog (ATM Grupo Maggioli / Galileo IyS). Common on Canary Islands `eadmin.*` and `sede.*` tenants. Product: [administración electrónica](https://www.atm-maggioli.es/software-y-consultoria/administracion-electronica/).

**Signals:** path `/transparencia/datos/catalogo`; Maggioli / Galileo IyS / ATM branding; title “Sede Electrónica”; dataset list under transparencia.

**Confirm:** GET `https://host/transparencia/datos/catalogo` and match a reusable dataset listing. One record per municipality tenant. Do **not** set `ckan`, `opendatasoft`, or `socrata` from guessed `/api/3`, `/api/v2/catalog`, or `/api/views` paths — those URLs return the HTML shell. Do **not** set `atmmaggioli` on Italian Municipium / Maggioli “Portale Opendata” shells (`municipiumapp.it` civic CMS); that is a different product — use [`municipium`](#municipium).

| Tool | Query |
|------|-------|
| Google | `inurl:/transparencia/datos/catalogo (Maggioli OR Galileo OR "sede electrónica")` |
| Google | `"grupo ATM-Maggioli" OR "ATM Maggioli" ("datos abiertos" OR catálogo)` |
| Censys | `web.endpoints.http.body: "Maggioli"` |
| FOFA | `body="Maggioli"` |

Skip the vendor homepage and Galileo demo sede. Prefer the municipal catalog path, not the whole e-office.

## Gobierto Datos (`gobierto`) {#gobierto}

Populate Tools open-data catalog for Spanish municipalities, offered as SaaS and as the open-source Gobierto suite. Product: [Gobierto Datos](https://www.gobierto.es/transparencia/datos-abiertos). Source: [PopulateTools/gobierto](https://github.com/PopulateTools/gobierto).

**Signals:** Gobierto chrome; dataset hub path `/datos/`; DCAT metadata; SQL API over HTTP.

**Confirm:** GET the tenant `/datos` list and match reusable datasets. One record per municipality host. Do **not** set `gobierto` on budget, contracts, agendas, or transparency pages that have no dataset catalog, and do **not** register `gobierto.es` marketing or the national budget explorer `presupuestos.gobierto.es`. Do **not** set `ckan`.

[_gobierto_footer.html.erb](https://github.com/PopulateTools/gobierto/blob/master/app/views/layouts/_gobierto_footer.html.erb) sets `window.gobiertoAPI` (51 hosts in September 2026, including `frp.gobierto.es`). That object is the whole Gobierto suite, so still require a `/datos` catalog. `body="gobierto"` matched 159 hosts, including `populate.tools`.

| Tool | Query |
|------|-------|
| Google | `"Gobierto" "/datos" (ayuntamiento OR datasets OR "datos abiertos")` |
| Google | `inurl:/datos gobierto (csv OR dcat)` |
| Censys | `web.endpoints.http.body: "window.gobiertoAPI"` |
| FOFA | `body="window.gobiertoAPI"` |

## Viavansi Open Government (`viavansi`) {#viavansi}

Spanish municipal open-data catalog skinned with the Viavansi WordPress theme. Installs: [Diputación de Cádiz](https://datosabiertos.dipucadiz.es/data/) (`viavansi-open-government`) and [Santander](https://datos.santander.es/) (`viavansi-ogov-current`). Product note: [INPRO portal de datos abiertos](https://inpro.dipusevilla.es/productos-y-servicios/participacion-y-transparencia/portal-de-datos-abiertos/index.html).

**Signals:** `/wp-content/themes/viavansi-open-government/` or `/wp-content/themes/viavansi-ogov-current/`.

**Confirm:** GET the catalog page and match the theme path. One record per institution. A WordPress open-data page without this theme stays `wordpress`. Do **not** set `ckan` unless the public catalog UI is CKAN.

| Tool | Query |
|------|-------|
| Google | `inurl:wp-content/themes/viavansi "datos abiertos"` |
| FOFA | `body="viavansi-open-government"` |
| FOFA | `body="viavansi-ogov"` |

## Municipium Portale Opendata (`municipium`) {#municipium}

Maggioli Municipium "Portale Opendata" — Italian municipal open-data SaaS, distinct from the Spanish ATM Maggioli product above. Tenants run on their own host (`opendata.comune.{slug}.it`, `opendata.cittametropolitana.{slug}.it`) backed by `{tenant}-opendata-api.cloud.municipiumapp.it`. Demo: [opendata.municipiumapp.it](https://opendata.municipiumapp.it/it). Product: [Maggioli Municipium](https://www.maggioli.com/it-it/soluzioni/servizi-al-cittadino/municipium).

**Signals:** jQuery loaded from `opendata-api.cloud.municipiumapp.it/s3/0/sito/jquery/`, `/js/agid-home.js` + `/js/all-agid-home.js`, `bootstrap-italia` assets, `apis.maggioli.cloud/rest/captcha/v2/widget.module.min.js`, title “Portale Opendata”, catalog page `/it/page/catalogo`.

**Confirm:** GET the tenant root or `/it` and match at least the `municipiumapp.it` asset host. One record per comune tenant. Do **not** set `atmmaggioli` on these (Spanish sede product) and do not register the `opendata.municipiumapp.it` demo (“Comune di Futura” placeholder content) or `{tenant}-opendata-sito.cloud.municipiumapp.it` staging hosts that 403. The shared CKAN hub [opendata.maggioli.cloud](https://www.opendata.maggioli.cloud/) is already registered as `ckan`. Do not add an `organization:` filter on that hub as a second catalog of a comune that already has a Municipium portale.

| Tool | Query |
|------|-------|
| Google | `inurl:opendata.comune "Portale Opendata" catalogo` |
| Google | `"municipiumapp" opendata comune` |
| Censys | `web.endpoints.http.body: "municipiumapp.it"` |
| FOFA | `body="municipiumapp.it"` |

## OPENDATAENTE (`opendataente`) {#opendataente}

Actainfo cloud SaaS open-data catalog for Italian municipalities and local authorities (ACN sa-5127). Product: [opendataente.it](https://opendataente.it/) and the [Actainfo instance list](https://www.actainfo.it/news/dataset-open-data-2025/). Tenants use `dati.comune.{slug}.{province}.it` (or a dedicated `dati.` host), not `*.opendataente.it`.

**Signals:** title “Portale Open Data”; `/env.js` with `BACKEND_BASE_URL` / `DATI_BASE_URL`; footer “Powered by ACTAINFO”; React shell `/static/js/main.*.js`.

**Confirm:** GET `https://host/backend/api/catalog/` and match DCAT-AP_IT RDF (`application/rdf+xml`, `dcatapit:Dataset`). One record per public tenant. Do **not** set `ckan` from a guessed `/api/3` path — the homepage is an SPA shell. Do **not** register `opendataente.it` / `opendataente.cloud` (vendor marketing) or ActaLogin (`login.comune.*`) tenants.

| Tool | Query |
|------|-------|
| Google | `"Portale Open Data" "Powered by ACTAINFO"` |
| Google | `inurl:dati.comune "Portale Open Data" site:.it` |
| Censys | `web.endpoints.http.html_title: "Portale Open Data"` |
| FOFA | `title="Portale Open Data" && body="ACTAINFO"` |
| crt.sh | `dati.comune.%.it` (then confirm `/backend/api/catalog/`) |

Skip the vendor homepage. Prefer the municipal `dati.` catalog, not the commune CMS.

## DataPortal.AI (`dataportalai`) {#dataportalai}

Sister (Almawave) open-data portal, current name of StatPortal Open Data / SPOD. Product: [DataPortal.AI](https://www.sister.it/prodotti/dataportalai/). The vendor site has no tenant gallery (product page, sitemap, and news only). Tenants run on the administration’s own host. Mapped portals show two generations; require signals from one generation, not a Drupal or CKAN guess.

**StatPortal Open Data / SPOD (Drupal 7).** Mapped: [dati.veneto.it](https://dati.veneto.it/), [opendata.comune.pisa.it](https://opendata.comune.pisa.it/).

- `/sites/all/modules/spodata/`
- theme `/sites/all/themes/statportal` (including `statportal_{tenant}`) or `/sites/all/themes/spod_bootstrap`
- catalog index `/catalogo-opendata` or `/catalog`
- dataset pages `/opendata/{slug}` (`/content/` is mostly CMS pages)
- Pisa footer only: “Realizzato con la tecnologia Open Source **StatPortal OpenData**”, linking to `opendata.statportal.it`. Veneto has no product footer. The phrase “Powered by StatPortal Open Data” is not on these portals.

**DataPortal.AI SPA.** Mapped: [dati.lavoro.gov.it](https://dati.lavoro.gov.it/).

- HTML title `DataPortal.AI`
- shell `/lmap/lmap-core/` and `/config/custom.css` (the same HTML is returned for `/catalogo-opendata/` and `/content/`)
- `/config/config.json` with `"baseURL": "/api/core/"`

**Confirm:** two signals from the same generation, and a public dataset list (SPOD catalog or `/opendata/{slug}`, or the SPA title). One administration portal = one record.

**Reject:**

- Drupal `generator` alone, or a generic Drupal theme
- `/api/3` or `SpodCkanApi` alone. `GET /api/3/action/status_show` that returns `ckan_version` is CKAN. FOFA still lists [dati.unionevallesavio.it](https://dati.unionevallesavio.it/) under `modules/spodata` and `themes/statportal`; the live site is CKAN 2.9.8, and both `/catalogo-opendata` and `SpodCkanApi` are 404
- `/lmap/lmap-core/` with title `Data Browser` (Sister Data Browser / Istat-style indicator UI: `esploradati.istat.it`, `*.databrowser.sister.it`)
- Istat browser [statportal.it](http://www.statportal.it/catalogo-dati)
- StatKit statistical portals such as ASTATDATA (`statastat.prov.bz.it`). Product: [StatKit](https://www.sister.it/prodotti/statkit/)
- `sister.it` marketing

| Tool | Query |
|------|-------|
| Google | `"modules/spodata" OR "themes/statportal" OR "spod_bootstrap"` |
| Google | `"StatPortal OpenData" OR intitle:"DataPortal.AI"` |
| Censys | `web.endpoints.http.body: "/sites/all/modules/spodata/"` |
| Censys | `web.endpoints.http.html_title: "DataPortal.AI"` |
| FOFA | `body="modules/spodata"` |
| FOFA | `body="themes/statportal" \|\| body="themes/spod_bootstrap"` |
| FOFA | `title="DataPortal.AI"` |

`body="StatPortal Open Data"` returns no FOFA hits. Re-check any `spodata` host whose live generator is `ckan`.

## ComunWeb (`comunweb`) {#comunweb}

Consorzio dei Comuni Trentini website platform. Product: [ComunWeb](https://www.comunweb.it/). Trentino municipalities publish a dataset list on their own host.

**Signals:** content class `opendata_dataset` at `/api/opendata/v1/content/class/opendata_dataset`; CSV `/exportas/csv/opendata_dataset`; public path `Open-Data/I-dataset-disponibili`.

**Confirm:** GET the `opendata_dataset` class and match dataset nodes (`objectName`, `fullUrl`). One ente site = one record. Do **not** register `comunweb.it` or `comunitrentini.it` marketing. Do **not** set `ckan` because `objectRemoteId` starts with `ckan_`; that is a remote id. Set `ckan` only when `/api/3/action/status_show` returns `ckan_version`.

| Tool | Query |
|------|-------|
| Google | `"piattaforma ComunWeb" "Open-Data"` |
| Google | `inurl:/api/opendata/v1/content/class/opendata_dataset` |
| Censys | `web.endpoints.http.body: "opendata_dataset"` |
| FOFA | `body="opendata_dataset"` |

## PA-Online Open Data (`paonline`) {#paonline}

Technical Design hosted DCAT catalogs for Italian municipalities. Host: [pa-online.it](https://www.pa-online.it/). dati.gov.it harvests per-comune RDF under `/OpenData/{ISTAT code}/`.

**Signals:** path `/OpenData/` plus a 6-digit ISTAT directory; file `METADATO.rdf` or a comune-named `.rdf` with `dcatapit:Dataset`.

**Confirm:** GET the comune RDF and match a DCAT catalog. One ISTAT directory = one record. Do **not** register `hosting.pa-online.it` sportello pages, `GisMasterWebS` payment or SUAP screens, or GisMaster map viewers (`gismaster`).

| Tool | Query |
|------|-------|
| Google | `site:pa-online.it/OpenData METADATO.rdf` |
| Google | `inurl:pa-online.it/OpenData filetype:rdf` |
| Censys | `web.endpoints.http.body: "pa-online.it/OpenData"` |
| FOFA | `host="pa-online.it" && body="dcatapit"` |

## OpenGov (`opengov`) {#opengov}

Tyler / OpenGov financial transparency SaaS for US cities and states. Public tenants are `{org}.opengov.com` with `/transparency` and `/data` report views.

**Signals:** hostname `*.opengov.com`; path `/transparency` or `/data/`; Highcharts budget explorer; “Transparency Home”.

**Confirm:** GET the tenant home or `/transparency` and match OpenGov report navigation. One record per government tenant. Do **not** set `opengov` from the word “OpenGov” on ArcGIS Hub, `wyopen.gov`, `opengov.brandon.ca`, or other checkbooks that are not `*.opengov.com`.

| Tool | Query |
|------|-------|
| Google | `site:opengov.com/transparency (budget OR financial)` |
| Google | `inurl:.opengov.com/data` |
| Censys | `web.names: "opengov.com"` |
| FOFA | `domain="opengov.com"` |

Skip `www.opengov.com` marketing. Do not bulk-add every guessed city subdomain.

## OneGov Election Day (`onegov`) {#onegov}

Seantis OneGov Cloud application for Swiss election and vote results. Source: [onegov-cloud](https://github.com/OneGov/onegov-cloud). Public portals include [abstimmungen.gr.ch](https://abstimmungen.gr.ch), [wab.zug.ch](https://wab.zug.ch), [wab.sg.ch](https://wab.sg.ch), and [landsgemeinde.gl.ch](https://www.landsgemeinde.gl.ch). Distinct from Tyler OpenGov (`opengov`) on `*.opengov.com`.

**Signals:** HTML `onegov` and `election_day`; `data-version` on the document element; DCAT-AP CH at `/catalog.rdf`; JSON at `/json` and `/archive/{year}/json`.

**Confirm:** GET `/catalog.rdf` and the portal home. One record per public canton or commune portal. Skip `abstimmungen.sz.ch` (hostname does not resolve) and cantonal CMS pages that only link to results. Do not register the OneGov Cloud marketing site as a catalog.

| Tool | Query |
|------|-------|
| Google | `"Wahlen & Abstimmungen" (Kanton OR Landsgemeinde) catalog.rdf` |
| Google | `inurl:catalog.rdf (abstimmungen OR wab) site:.ch` |
| Censys | `web.endpoints.http.body: "election_day"` |
| FOFA | `body="election_day" && body="onegov"` |

## POMOSAM (`pomosam`) {#pomosam}

CORA GEO municipal eGovernment / open-data publisher used by Slovak cities (contracts, invoices, orders, public datasets). Vendor: [pomosam.sk](http://www.pomosam.sk).

**Signals:** POMOSAM / CG eGOV branding; municipal zverejňovanie / open-data modules.

**Confirm:** GET the public dataset or disclosure catalog. One record per municipality tenant.

| Tool | Query |
|------|-------|
| Google | `"POMOSAM" OR "CG eGOV" (otvorené OR zverejňovanie) site:.sk` |
| Censys | `web.endpoints.http.body: "POMOSAM"` |
| FOFA | `body="POMOSAM"` |

## oPortal (`oportal`) {#oportal}

Inspur Chinese government open-data product. Deployments share `/oportal/` catalogs, a developer center, and an application gallery.

**Signals:** path `/oportal/`; 浪潮 / Inspur; data-service / API gallery pages.

**Confirm:** GET `/oportal/` (or the documented catalog path) and match a dataset listing. One record per government tenant.

| Tool | Query |
|------|-------|
| Google | `inurl:/oportal/ (数据 OR 开放)` |
| Google | `"浪潮" 开放数据 oportal` |
| Censys | `web.endpoints.http.body: "/oportal/"` |
| FOFA | `body="/oportal/"` |

## Epoint Big Data Open Platform (`epointopendata`) {#epointopendata}

Commercial Chinese public-data portal from Epoint (国泰新点软件), branded 新点大数据开放平台. Catalog UI is served under `/extranet/openportal/` on the agency host. Not Inspur oPortal (`oportal`).

**Signals:** page title or HTML `新点大数据开放平台`; application script references `epoint.com.cn` with `basePath` `/extranet/openportal` (Tongliao’s `boot.min.js` does). Shared path plus `ResBoot` is a lead, not proof.

**Confirm:** the product name or the `epoint.com.cn` asset, and a public dataset listing. One record per government tenant. Leave lookalike `/extranet/openportal/` hosts as `custom` until that signal is present. Do not retag `/oportal/` tenants.

| Tool | Query |
|------|-------|
| Google | `"新点大数据开放平台"` |
| Google | `inurl:/extranet/openportal/ 新点` |
| Censys | `web.endpoints.http.body: "新点大数据开放平台"` |
| FOFA | `body="新点大数据开放平台"` |

## Taiji Digital Public Data Open Platform (`tykyopendata`) {#tykyopendata}

Commercial Chinese public-data portal from Taiji Digital (深圳太极数智技术有限公司, tyky.com.cn), branded 太极数智公共数据开放平台. Product page: [tyky.com.cn](https://www.tyky.com.cn/product/show-1059.html). Distinct from Inspur oPortal (`oportal`) and Epoint (`epointopendata`).

**Signals:** homepage assets under `/static/opendata1.0/`; the vendor page names the host. The live shell does not print 太极 or tyky.

**Confirm:** `/static/opendata1.0/` on a public dataset catalog, or the vendor page cites that exact host, and the page lists datasets. One record per government. A city named only in the vendor case list, with no asset path and no cited URL, stays `custom`. Do not retag `/oportal/` or `/extranet/openportal/` tenants.

Checked 25 September 2026. Of Chinese open-data homepages that answered, only [opendata.sz.gov.cn](https://opendata.sz.gov.cn/) served `/static/opendata1.0/`. The vendor page cites that URL. Guiyang is a case title only; `www.gyopendata.gov.cn` did not resolve.

**FOFA** (same day). `body="/static/opendata1.0/"` returned two hosts: Shenzhen and [data.ziyang.gov.cn](http://data.ziyang.gov.cn/) (资阳市政府数据开放平台). The same pair is returned by `body="opendata1.0"`, `body="/data/api/toApi"`, `body="t4_css.css"`, and `body="t4_index.js"`. Ziyang did not answer a live GET from outside China; the FOFA body match is the confirm. `body="太极数智公共数据开放平台"` and `title="太极数智"` hit the vendor site and spam clones, not catalogs — the shell does not print the brand. `domain="tyky.com.cn"` is wildcard noise. `body="2018-10-18-PC.css"` also hits Ningbo JDOP (`../src/assets/css/2018-10-18-PC.css` on `/sjkfptold/`), which has no `/static/opendata1.0/`. `body="useOldFixed.css"` hits hospital sites. `body="/static/opendata/"` is unrelated.

| Tool | Query |
|------|-------|
| Google | `"opendata1.0" 数据开放` |
| Google | `"太极数智公共数据开放平台"` |
| Censys | `web.endpoints.http.body: "/static/opendata1.0/"` |
| FOFA | `body="/static/opendata1.0/"` |
| FOFA | `body="/data/api/toApi"` |
| FOFA | `body="t4_css.css"` |

## data.world (`dataworld`) {#dataworld}

Commercial catalog SaaS. Hub: [data.world](https://data.world). Distinct from World Bank Data (`dataworldbankorg`).

**Signals:** host `data.world`; data.world chrome.

**Confirm:** GET the public dataset search. One hub, not per-user or private organization spaces.

| Tool | Query |
|------|-------|
| Google | `site:data.world datasets` |
| Censys | `web.names: "data.world"` |
| FOFA | `host="data.world"` |

## IUDX Catalogue (`iudx`) {#iudx}

India Urban Data Exchange catalogue server. Hub: [catalogue.iudx.org.in](https://catalogue.iudx.org.in/). Source: [datakaveri/iudx-catalogue-server](https://github.com/datakaveri/iudx-catalogue-server). Distinct from CKAN and from pygeoapi on other IUDX hosts.

**Signals:** IUDX catalogue chrome; `/cat/v1/` or central-catalogue host.

**Confirm:** GET `{base}/count?property=[type]&value=[[iudx:Resource]]` (or the tenant base `adex/cat/v1`, `dx/cat/v1`). Keep a host only when `totalHits` is a public dataset list. One record per public catalogue tenant, not each resource ID, and not a second hostname of the same index.

The catalogue UI `index.html` title is `IUDX | Indian Urban Data Exchange` and the author meta is `IUDX UI Team` (rebrands such as GDI keep that author). [apidoc.html](https://github.com/datakaveri/iudx-catalogue-server/blob/master/docs/apidoc.html) titles the ReDoc page `DX Catalogue API Docs`. Forks of `datakaveri/iudx-catalogue-server` repeat the national hub. Deployed hostnames are the ingress files in [datakaveri/iudx-deployment](https://github.com/datakaveri/iudx-deployment) (`host: api.*catalogue`, `host: dataexplorer.*`).

`catalogue.iudx.org.in` redirects to `catalogue.cos.iudx.org.in`. That API returns the same resource ids as `api.central-catalogue.iudx.org.in` (already `centralcatalogueiudxorgin`). Do not add COS as a second catalog. Skip sandbox, `*.iudx.io` test hosts, and API-doc vhosts whose items are secure test records (GMAS).

| Tool | Query |
|------|-------|
| Google | `"IUDX" (catalogue OR catalog) site:.in` |
| GitHub | ingress `host:` in `datakaveri/iudx-deployment` |
| Censys | `web.endpoints.http.body: "DX Catalogue API Docs"` |
| FOFA | `body="DX Catalogue API Docs"` |
| FOFA | `title="IUDX \| Indian Urban Data Exchange"` |
| FOFA | `body="IUDX UI Team"` |
| FOFA | `domain="adex.org.in"` |
| Censys | `web.names: "iudx.org.in"` |
| FOFA | `host="iudx.org.in"` |

## OGD Platform India (`ogdindia`) {#ogdindia}

NIC SaaS on data.gov.in for ministries and states. Site: [data.gov.in](https://data.gov.in).

**Signals:** `data.gov.in` tenant host or path; OGD Platform India; CKAN-like catalog UI on NIC hosting.

**Confirm:** GET the ministry/state catalog home. Do not re-add the national portal if it is already registered; add only distinct tenant catalogs.

| Tool | Query |
|------|-------|
| Google | `site:data.gov.in (catalog OR dataset)` |
| Google | `"OGD Platform" OR "Open Government Data" site:.gov.in` |
| crt.sh | `%.data.gov.in` |
| Censys | `web.names: "data.gov.in"` |
| FOFA | `host="data.gov.in"` |

## data eye (`dataeye`) {#dataeye}

Japanese municipal open-data SaaS (Data Cradle). Site: [dataeye.jp](https://dataeye.jp). Some tenants expose a CKAN-compatible metadata API. Custom-domain tenants (`opendata.pref.chiba.lg.jp`, `shimane-opendata.jp`, `www.okayama-opendata.jp`) still link `https://dataeye.jp/` from the footer, so the `body="dataeye.jp"` query catches hosts the domain query misses.

**Confirm:** GET the prefecture/city catalog and `ckan_api/package_search`. Keep a tenant only when `result.count` is greater than 0. One record per tenant (including joint prefecture-municipality group portals). Drop the vendor homepage, `dev-*` hosts, idea-box-only sites, and map viewers that 404 `package_search` (`kurashiki-vaccine-map.dataeye.jp`, `map.dataeye.jp`, `kanko-dataeye.jp`).

**FOFA** (checked 24 September 2026). `domain="dataeye.jp"` returned 59 rows (38 hosts). `cert="dataeye.jp"` returned 139 and was the same wildcard certificate (`*.dataeye.jp`), not extra catalogs. `body="datasets_condition"` is the catalog-nav path and returned 77 rows, including the custom domains the domain query misses. `body="/graphs/top"` returned 101 and was mostly unrelated sites. `body="/ckan_api/"` returned 1 unrelated blog. `body="ckan_api/package_search"` returned 0 because that path is not in the HTML.

| Tool | Query |
|------|-------|
| Google | `site:dataeye.jp` |
| Google | `"data eye" オープンデータ (市 OR 県)` |
| crt.sh | `%.dataeye.jp` |
| Censys | `web.names: "dataeye.jp"` |
| FOFA | `body="datasets_condition"` |
| FOFA | `domain="dataeye.jp"` |
| FOFA | `body="dataeye.jp"` |

## LinkData (`linkdata`) {#linkdata}

Info Lounge hosted hub for publishing open tables. Site: [linkdata.org](https://linkdata.org/). Japanese municipalities publish dataset works on this single platform.

**Signals:** host `linkdata.org`; LinkData work pages; CSV and RDF downloads.

**Confirm:** GET the public hub and match published data works. One record for the hub. Do **not** register each municipality homepage that only links to a work, and do **not** register `app.linkdata.org` or `idea.linkdata.org` as separate catalogs.

| Tool | Query |
|------|-------|
| Google | `site:linkdata.org オープンデータ` |
| Censys | `web.names: "linkdata.org"` |
| FOFA | `host="linkdata.org"` |

## Seoul Open Data Plaza (`seoulopendataplaza`) {#seoulopendataplaza}

Shared catalog used by Seoul Metropolitan Government district (`gu`) portals. Titles of the form 열린 데이터 광장; `/openinf/` JSP pages.

**Confirm:** GET the district plaza home. One record per `gu` tenant, plus the city portal if it is a distinct catalog.

| Tool | Query |
|------|-------|
| Google | `"열린 데이터 광장" site:.go.kr` |
| Google | `inurl:/openinf/ seoul` |
| Censys | `web.endpoints.http.body: "openinf"` |
| FOFA | `body="openinf"` |

## Data Fair (`datafair`) {#datafair}

Koumoul open-source data portals. Docs: [data-fair.github.io](https://data-fair.github.io/3/en/).

**Signals:** Data Fair / Koumoul; `/data-fair/` or dataset explorer APIs.

**Confirm:** GET the public portal and a dataset list API. Skip the vendor docs site.

[ui/index.html](https://github.com/data-fair/data-fair/blob/master/ui/index.html) loads `simple-directory/api/sites` (93 hosts in September 2026, including `data.grandpoitiers.fr`). `body="data-fair"` is not usable: it matched 2,169 hosts, including `fairplus-project.eu`.

| Tool | Query |
|------|-------|
| Google | `"Data Fair" (Koumoul OR datasets) -site:github.com` |
| Censys | `web.endpoints.http.body: "simple-directory/api/sites"` |
| FOFA | `body="simple-directory/api/sites"` |

## Datawheel (`datawheel`) {#datawheel}

Datawheel-hosted open-data / economic-complexity portals. Site: [datawheel.us](https://datawheel.us).

**Confirm:** GET the public data portal (not a marketing page). One record per government or international-organization catalog.

| Tool | Query |
|------|-------|
| Google | `"Datawheel" (open data OR "data portal") -site:datawheel.us` |
| Censys | `web.endpoints.http.body: "datawheel"` |
| FOFA | `body="datawheel"` |

## SEU-e (`seue`) {#seue}

Consorci AOC electronic office / transparency / open-data service for Catalan administrations. Hosts under `seu-e.cat`.

**Confirm:** GET the municipality’s open-data or transparency dataset listing on `seu-e.cat`. One record per public-administration tenant that publishes datasets.

| Tool | Query |
|------|-------|
| Google | `site:seu-e.cat (dades OR datasets OR "dades obertes")` |
| crt.sh | `%.seu-e.cat` |
| Censys | `web.names: "seu-e.cat"` |
| FOFA | `domain="seu-e.cat"` |

## TriplyDB (`triplydb`) {#triplydb}

Linked-data / knowledge-graph publishing with SPARQL. Site: [triplydb.com](https://triplydb.com).

**Confirm:** GET the public dataset catalog or SPARQL UI. One record per public instance, not per named graph.

| Tool | Query |
|------|-------|
| Google | `site:triplydb.com` |
| Google | `"TriplyDB" (SPARQL OR datasets) -site:triplydb.com` |
| crt.sh | `%.triplydb.com` |
| Censys | `web.names: "triplydb.com"` |
| FOFA | `domain="triplydb.com"` |

## Drupal (`drupal`) {#drupal}

Use `drupal` only when the **public product is a dataset catalog** (open-data nodes, JSON:API dataset bundle). Do not register ordinary CMS homepages. If the site is DKAN, use `dkan`. If it is EKAN (`profiles/contrib/ekan` / `ekan_theme`), use [`ekan`](#ekan). Dutch municipal OpenGDC tenants (`/openapi.json` + `/api/datasets`) use [`opengdc`](#opengdc), not `drupal`.

**Confirm:** `/jsonapi/node/dataset` (or the site’s dataset bundle) or a public `data.json`.

| Tool | Query |
|------|-------|
| Google | `"powered by Drupal" ("open data" OR datasets) inurl:/data` |
| Censys | `web.endpoints.http.body: "/jsonapi/node/dataset"` |
| FOFA | `body="/jsonapi/node/dataset"` |

## WordPress (`wordpress`) {#wordpress}

Use `wordpress` only for a **datasets** custom post type or CKAN-theme WP catalog. Ordinary WordPress homepages are out of scope.

| Tool | Query |
|------|-------|
| Google | `"open data" WordPress (CKAN OR dataset) -site:wordpress.org` |
| Censys | `web.endpoints.http.body: "wp-content"` |
| FOFA | `body="wp-content" && body="open data" && body="dataset"` |

## Joomla (`joomla`) {#joomla}

Use `joomla` for catalog or portal records whose site runs on the Joomla CMS, the same
convention as `wordpress` and `liferay`. Signals: generator meta `Joomla! - Open Source
Content Management`, `/media/`, and `/components/com_*` asset paths. Ordinary Joomla
homepages without a data or map catalog function are out of scope.

## OutSystems (`outsystems`) {#outsystems}

Low-code application platform. Site: [outsystems.com](https://www.outsystems.com). Use
`outsystems` when the catalog itself is an OutSystems application. Confirmed
installations: PORDATA (PT indicators database), Diário da República (PT official
gazette), and the California DWR Water Data Library (US-CA hydrometric station
archive, traditional-web `.aspx` + `RichWidgets`).

**Signals:** `OutSystems*.js` scripts (`OutSystemsReactView.js`, `OutSystemsClientRuntime`), `_OSGlobalJS`, and `/Blocks/` + `RichWidgets` asset paths.

| Tool | Query |
|------|-------|
| Google | `"OutSystems" ("open data" OR statistics) (portal OR catálogo)` |
| Censys | `web.endpoints.http.body: "OutSystemsReactView"` |
| FOFA | `body="OutSystemsReactView.js"` |

## Plone (`plone`) {#plone}

Zope CMS. Site: [plone.org](https://plone.org). Use `plone` when the catalog page
itself is served by Plone. Confirmed installations: Brazil’s gov.br portal
(INEP microdata) and the BCGSC physical-mapping file catalog
(`plone.bcgsc.ca`).

**Signals:** generator meta `Plone - http://plone.org`; `/portal_css/`; Zope
`ZServer` banner.

**Confirm:** GET the catalog page and check the generator meta. One record per
catalog, not per Plone site. Skip ordinary ministry homepages.

| Tool | Query |
|------|-------|
| Google | `"Plone - http://plone.org" (microdata OR datasets OR catalog)` |
| Censys | `web.endpoints.http.body: "Plone - http://plone.org"` |
| FOFA | `body="Plone - http://plone.org"` |

## Government Site Builder (`governmentsitebuilder`) {#governmentsitebuilder}

Central CMS of the German federal administration, provided by ITZBund and used by
80+ federal agencies (250+ websites). Use `governmentsitebuilder` when a German
federal catalog page (statistics, health reporting, legal or open-data
publications) is served by the GSB itself. GSB 11 is TYPO3-based but keeps its own
generator meta; do not retag those sites as `typo3`.

**Signals:** generator meta `Government Site Builder` (sometimes `GSB11`);
`*.bund.de` hostnames.

**Confirm:** GET the catalog page and check the generator meta. One record per
catalog, not per agency site.

| Tool | Query |
|------|-------|
| Google | `"Government Site Builder" (statistik OR daten OR "open data")` |
| Censys | `web.endpoints.http.body: "Government Site Builder"` |
| FOFA | `body="Government Site Builder"` |

## Ísland.is (`islandis`) {#islandis}

Open-source digital-services platform of the Icelandic government (Stafrænt Ísland /
Digital Iceland). Source: [island-is/island.is](https://github.com/island-is/island.is)
(MIT). Government content catalogs — the Stjórnartíðindi official gazette, the Opin
gögn open-data page — are published as Ísland.is applications on `island.is`.
Distinct from the national CKAN catalog on `ckan.island.is` (`ckan`).

**Signals:** `island.is` hostname with the Ísland.is design system; Next.js `_next`
assets; GraphQL gateway at `api.island.is`; developer handbook at `docs.devland.is`.

**Confirm:** GET the catalog page on `island.is`. One record per published catalog,
not per island.is service page. Do not register the island.is portal root or
ministry profile pages as catalogs.

| Tool | Query |
|------|-------|
| Google | `site:island.is (gögn OR gagnasafn OR "open data")` |
| Censys | `web.endpoints.http.body: "island.is" and services.port: 443` |

## Piveau (`piveau`) {#piveau}

DCAT-AP microservice catalog (Fraunhofer FOKUS). Site: [piveau.de](https://www.piveau.de). Powers several European public-sector portals (including patterns used by data.europa.eu).

**Signals:** Piveau / DCAT-AP; Sparql or Hub-UI; `piveau` in HTML or API paths.

**Confirm:** GET the public catalog and a DCAT/search API. Do not re-add data.europa.eu if it is already registered.

[index.html](https://github.com/piveau-data/piveau-hub-ui/blob/master/index.html) sets `<title>Piveau UI</title>` (3 hosts in September 2026, including `www.sozial-informations-system.de` and `piveau-hub-ui-gsi.apps.osc.fokus.fraunhofer.de`). `body="piveau"` matched 52, and the first hits include a scheduling endpoint and `apirails.com`. `class="edp2-footer"` is in a Vue component and matched nothing.

| Tool | Query |
|------|-------|
| Google | `"Piveau" (DCAT-AP OR "open data") -site:github.com -site:piveau.de` |
| Censys | `web.endpoints.http.body: "<title>Piveau UI</title>"` |
| FOFA | `body="<title>Piveau UI</title>"` |

## LKOD (`lkod`) {#lkod}

Czech local DCAT-AP-CZ catalogs (Golemio / Operátor ICT). Harvests into NKOD. Site: [lkod.cz](https://lkod.cz). Slovak municipal clones use `/opendata/set/lkod` (DCAT-AP-SK TTL) on city `opendata.*` hosts — still `lkod`, not POMOSAM.

**Confirm:** GET the municipal/local catalog (Next.js LKOD UI or `/opendata/set/lkod`), not the national NKOD/data.slovensko.sk record twice.

[metatags.json](https://gitlab.com/operator-ict/golemio/lkod/lkod-catalog-2-0/-/blob/release/src/app/metatags.json) describes `Procházejte a stahujte datové sady` (2 hosts in September 2026, both `lkod.cz`). The same file’s title `Lokální katalog otevřených dat` matched 13, and the first hits are `golemio.cz` and the admin host `lkod-admin.msmt.gov.cz`. `body="lkod"` matched 2,767, and the first hits are a monastery site, a Hungarian GMO map, and unrelated pages.

| Tool | Query |
|------|-------|
| Google | `"LKOD" OR "lokální katalog otevřených dat" site:.cz` |
| Google | `inurl:/opendata/set/lkod site:.sk` |
| Censys | `web.endpoints.http.body: "Procházejte a stahujte datové sady"` |
| FOFA | `body="Procházejte a stahujte datové sady"` |

## Aleph (`aleph`) {#aleph}

OCCRP investigative document/dataset search. Site: [aleph.occrp.org](https://aleph.occrp.org). Often `catalog_type: Data search engine` or Open data portal depending on whether it hosts datasets or searches collections.

**Confirm:** GET a public Aleph instance. Skip login-only investigations.

The shell in [ui/public/index.html](https://github.com/alephdata/aleph/blob/develop/ui/public/index.html) is `<html data-api-endpoint="/api/2/">`. `body="aleph"` also matches Ex Libris Aleph library catalogs and unrelated pages. `body="data-api-endpoint=\"/api/2/\""` matched 319 hosts in September 2026.

| Tool | Query |
|------|-------|
| Google | `"Aleph" OCCRP (datasets OR documents) -site:occrp.org` |
| Censys | `web.endpoints.http.body: "data-api-endpoint=\"/api/2/\""` |
| FOFA | `body="data-api-endpoint=\"/api/2/\""` |

## Our Open Data (`ouropendata`) {#ouropendata}

Japanese prefecture/city open-data CMS (Tokushima, Kagawa, Aomori, and others). This is the SHIRASAGI (シラサギ) catalog UI. Shared assets: `/assets/cms/public.css`, numeric `/dataset/` HTML pages, plus an application market and idea box. API: `/api/package_list` (not CKAN `/api/3/action/status_show`).

**Confirm:** GET the catalog home (not a single dataset HTML page). Distinct from CKAN and data.go.jp. Do not add a separate `shirasagi` software id.

| Tool | Query |
|------|-------|
| Google | `"Our Open Data" オープンデータ OR inurl:/assets/cms/public.css` |
| Censys | `web.endpoints.http.body: "assets/cms/public.css"` |
| FOFA | `body="assets/cms/public.css"` |

## Gipuzkoa Irekia (`gipuzkoairekia`) {#gipuzkoairekia}

Shared open-government / open-data platform for Gipuzkoa municipalities. Hub: [gipuzkoairekia.eus](https://www.gipuzkoairekia.eus).

**Confirm:** GET a **tenant** catalog (municipality or foral entity), not only the provincial hub if that hub is already registered. DCAT feeds are a plus.

| Tool | Query |
|------|-------|
| Google | `site:gipuzkoairekia.eus (datos OR datuak OR catalog)` |
| Google | `"Gipuzkoa Irekia" (opendata OR "datos abiertos")` |
| Censys | `web.names: "gipuzkoairekia.eus"` |
| FOFA | `domain="gipuzkoairekia.eus"` |

## Open Data Euskadi (`opendataeuskadi`) {#opendataeuskadi}

Basque Government open data portal on the euskadi.eus web stack. Hub: [opendata.euskadi.eus](https://opendata.euskadi.eus). Custom REST API documented under `/apis/`, plus a SPARQL endpoint on `api.euskadi.eus`.

**Signals:** host `opendata.euskadi.eus`; path `/catalogo-datos/`; euskadi.eus chrome ("Open Data Euskadi", trilingual eu/es/en).

**Confirm:** GET the catalog at `/catalogo-datos/` or a documented API collection under `/apis/`. Register the hub once — geoEuskadi (`geo.euskadi.eus`) and Udalmap are separate catalogs, and municipal Basque portals (Bilbao, Getxo) run their own stacks.

| Tool | Query |
|------|-------|
| Google | `site:opendata.euskadi.eus catalogo-datos` |
| Google | `"Open Data Euskadi" ("datos abiertos" OR "datu irekiak")` |
| Censys | `web.names: "opendata.euskadi.eus"` |
| FOFA | `domain="opendata.euskadi.eus"` |

## DataPress (`datapress`) {#datapress}

Managed CKAN plus CMS. Site: [datapress.com](https://datapress.com). Prefer `datapress` when the public product is branded DataPress; otherwise `ckan` if only the CKAN API is visible.

**Confirm:** CKAN `status_show` **and** DataPress chrome (or vendor docs naming DataPress). Do not double-register the same host as both `ckan` and `datapress`.

| Tool | Query |
|------|-------|
| Google | `"DataPress" ("open data" OR CKAN)` |
| Censys | `web.endpoints.http.body: "datapress"` |
| FOFA | `body="datapress"` |

## MODA Open Data Platform (`modaopendata`) {#modaopendata}

Taiwan Nuxt/Vue open-data frontend (national data.gov.tw family plus local clones). Source: moda-gov-tw/opendata-frontend.

**Confirm:** GET a **tenant** catalog (city/ministry), not a duplicate of the national hub if that hub is already registered. Shared `_nuxt` stack plus catalog API.

| Tool | Query |
|------|-------|
| Google | `"data.gov.tw" OR inurl:_nuxt (opendata OR 開放資料) site:.tw` |
| Google | `"moda-gov-tw" opendata` |
| Censys | `web.names: "data.gov.tw"` |
| FOFA | `host="data.gov.tw"` |

## Taiwan Government Website Open Data (`twgovopendata`) {#twgovopendata}

ASP.NET open-data module on Taiwan local-government websites. Dataset list, detail, and file-download pages share one application. Not the MODA Nuxt platform (`modaopendata`).

**Signals:** `OpenDataList.aspx` plus `OpenDataDetail.aspx` or `OpenDataContent.aspx`, and `OpenDataFileHit.ashx`. Miaoli also serves `OpenDataGroup.aspx`, `OpenDataOrg.aspx`, and `OpenDataTheme.aspx`.

**Confirm:** the list page shows datasets (title, format, organization) on that same host. One record per government catalog. Leave `Default.aspx` sections that do not serve those pages as `custom`. Do not retag `_nuxt` / `modaopendata` hosts. A page that only links `OpenDataList.aspx` on another host is a link-out.

Checked 25 September 2026. `body="OpenDataList.aspx" && body="OpenDataFileHit.ashx"` is 2 rows, both `opendata.yunlin.gov.tw`. `body="OpenDataFileHit.ashx"` and `body="/Common/OpenDataFileHit.ashx"` are the same two rows. `body="OpenDataList.aspx"` worldwide is 8 rows and 5 hosts: Yunlin is the catalog; `food-safety.tycg.gov.tw` links to Yunlin; `www.hcshb.gov.tw` links to `www.hsinchu.gov.tw/OpenDataList.aspx`; `eghouse.hccg.gov.tw` is the registered Hsinchu City Web GIS; `opendata.hccg.gov.tw` is the registered Hsinchu City CKAN host (live GET timed out). `social.hsinchu.gov.tw` is in that set and did not answer. `body="OpenDataDetail.aspx" && country="TW"` is 4 and adds `www.hccp.gov.tw` and `citizenshandbook.hccg.gov.tw`, both linking to `opendata.hccg.gov.tw`. Miaoli serves `OpenDataList.aspx`, `OpenDataDetail.aspx`, and `OpenDataFileHit.ashx` on the homepage and is absent from FOFA. `body="OpenDataTheme.aspx"`, `body="customize-openData"`, and `body="OpenDataFileHit.ashx?s="` are 0.

Title and host queries list Taiwan open-data homepages that still need a same-host GET. They are mostly CKAN, MODA, or another stack: `title="開放資料平台" && country="TW"` is 10, `title="資料開放平臺" && country="TW"` is 21, `title="資料開放平台" && country="TW"` is 24, `title="開放資料" && host=".gov.tw"` is 12, `host="opendata" && host=".gov.tw"` is 20. `body="jUtil.js" && body="OpenData" && country="TW"` is 13 and is the shared government CMS (`Scripts/jUtil.js`), including agency homepages that do not serve the dataset list.

| Tool | Query |
|------|-------|
| Google | `inurl:OpenDataList.aspx 資料開放` |
| Censys | `web.endpoints.http.body: "OpenDataFileHit.ashx"` |
| FOFA | `body="OpenDataList.aspx" && country="TW"` |
| FOFA | `body="OpenDataList.aspx" && body="OpenDataFileHit.ashx"` |
| FOFA | `title="開放資料平台" && country="TW"` |
| FOFA | `title="資料開放平臺" && country="TW"` |
| FOFA | `title="資料開放平台" && country="TW"` |
| FOFA | `host="opendata" && host=".gov.tw"` |
| FOFA | `body="jUtil.js" && body="OpenData" && country="TW"` |

## RDF Online Repository (`rdfrepository`) {#rdfrepository}

Revenue Development Foundation license-transparency portals. Docs: [Online Repository](https://revenuedevelopment.org/online-repository/). Tenants: `*.revenuedev.org`. Distinct from W3C RDF.

**Signals:** host `*.revenuedev.org`; title Repository; RDF/MCAS branding.

**Confirm:** GET the country tenant home. One record per country portal, not the vendor site.

| Tool | Query |
|------|-------|
| Google | `site:revenuedev.org` |
| Google | `"Online Repository" ("Revenue Development" OR mining) -site:revenuedevelopment.org` |
| Censys | `web.names: "revenuedev.org"` |
| FOFA | `domain="revenuedev.org"` |
| crt.sh | `%.revenuedev.org` |

## ResourceContracts (`resourcecontracts`) {#resourcecontracts}

NRGI oil/gas/mining contract repository. Hub: [resourcecontracts.org](https://resourcecontracts.org). Source: [NRGI/resourcecontracts.org](https://github.com/NRGI/resourcecontracts.org).

**Signals:** ResourceContracts chrome; country hosts `{country}.resourcecontracts.org`.

**Confirm:** GET the public contract search (hub or country tenant). One record per public catalog, not per contract PDF.

[head.blade.php](https://github.com/younginnovations/resourcecontracts-rc-subsite/blob/master/resources/views/layout/partials/head.blade.php) links `css/new-rc.css` (7 hosts in September 2026, including `resourcecontracts.org`; `dmachine.mshstudios.com` is a copied template, not a catalog). Country tenants that drop the stylesheet still match the domain query, so keep it.

| Tool | Query |
|------|-------|
| Google | `site:resourcecontracts.org` |
| Google | `"ResourceContracts" (mining OR petroleum) contract` |
| Censys | `web.endpoints.http.body: "css/new-rc.css"` |
| FOFA | `body="css/new-rc.css"` |
| Censys | `web.names: "resourcecontracts.org"` |
| FOFA | `domain="resourcecontracts.org"` |
| crt.sh | `%.resourcecontracts.org` |

## OpenSpending (`openspending`) {#openspending}

Open Knowledge Foundation public-finance catalog. Hub: [openspending.org](https://openspending.org). Fiscal Data Packages with a public search UI and API.

**Confirm:** GET the public dataset search. One record for the hub (and any independent OpenSpending deployment). Skip individual budget visualizations as catalogs.

[layout.html](https://github.com/openspending/spendb/blob/master/spendb/templates/layout.html) describes the site as `explore, visualize and track government spending` (3 hosts in September 2026, all `openspending.hel.ninja`, the City of Helsinki spendb deployment). `ng-app="spendb"` in the same file matched nothing. Keep the domain query for the canonical hub.

| Tool | Query |
|------|-------|
| Google | `"OpenSpending" (budget OR "fiscal data" OR "open spending")` |
| Censys | `web.endpoints.http.body: "explore, visualize and track government spending"` |
| FOFA | `body="explore, visualize and track government spending"` |
| Censys | `web.names: "openspending.org"` |
| FOFA | `domain="openspending.org"` |

## ODWeb (`odweb`) {#odweb}

Chinese municipal and provincial public-data catalog under `/odweb/`. Distinct from Inspur oPortal (`oportal`) and Zhejiang JDOP (`jdop`).

**Signals:** path `/odweb/`; script roots `/odweb/{city}/libs/`; page title 公共数据开放平台.

**Confirm:** GET `http(s)://host/odweb/`. One record per city or provincial catalog, not per dataset. Skip hosts that redirected off `/odweb/` onto an unrelated government CMS.

| Tool | Query |
|------|-------|
| Google | `inurl:/odweb/ 数据开放` |
| Google | `"odweb" 公共数据开放平台` |
| Censys | `web.endpoints.http.body: "/odweb/"` |
| FOFA | `body="/odweb/" && title="数据开放"` |

## Guangxi Public Data Open Platform (`gxopendata`) {#gxopendata}

Guangxi Zhuang Autonomous Region public data portal. Provincial hub: [data.gxzf.gov.cn](https://data.gxzf.gov.cn). City tenants: `{city}.data.gxzf.gov.cn`. Not CKAN.

**Signals:** host `data.gxzf.gov.cn` or `{city}.data.gxzf.gov.cn`; 公共数据开放平台 chrome.

**Confirm:** GET the tenant home. One record per city or provincial tenant, not per dataset.

| Tool | Query |
|------|-------|
| Google | `site:data.gxzf.gov.cn` |
| Google | `"公共数据开放平台" site:gxzf.gov.cn` |
| Censys | `web.names: "data.gxzf.gov.cn"` |
| FOFA | `host="data.gxzf.gov.cn"` |
| crt.sh | `%.data.gxzf.gov.cn` |

## OpenGDC (`opengdc`) {#opengdc}

Dutch municipal open-data and Woo catalog (Drupal / Dexes). Product site: [opengdc.nl](https://www.opengdc.nl). Live tenants include Utrecht, Groningen, Nijmegen, Oss, Hilversum, and Land van Cuijk. Not the genomic OpenGDC (GDC/BED) tool.

**Signals:** `/datasets` catalog UI; `/api` titled “Open API Specification”; `/openapi.json` OpenAPI 3 with paths `/api/datasets`, `/api/documents`, `/api/dossiers`; JSON:API `type: dataset`. Title often “Datacatalogus” or “Dataportaal”.

**Confirm:** GET `https://host/openapi.json` and `https://host/api/datasets` (JSON:API, `meta.total`). Some tenants sit behind a WAF (`403`). Prefer `opengdc` over generic `drupal`. One municipality = one catalog.

[page.html.twig](https://gitlab.com/dexes.efro/drupal-dataspace/-/blob/main/web/themes/custom/dexes/templates/page.html.twig) is the Dexes theme; served pages load assets from `themes/custom/dexes` (31 hosts in September 2026, including `dexes.eu` and `stedelijkverkeer.staging.dmi.dexes.eu`, both titled “Your trusted data marketplace”).

| Tool | Query |
|------|-------|
| Google | `"OpenGDC" (dataportaal OR datacatalogus) site:.nl` |
| Google | `inurl:/openapi.json "api/datasets" (Datacatalogus OR Dataportaal)` |
| Censys | `web.endpoints.http.body: "themes/custom/dexes"` |
| FOFA | `body="themes/custom/dexes"` |
| Censys | `web.endpoints.http.body: "api/dossiers"` |
| FOFA | `body="api/dossiers"` |

## Bitrix (`bitrix`) {#bitrix}

1C-Bitrix CMS used for government dataset catalogs. Site: [1c-bitrix.ru](https://www.1c-bitrix.ru). Skip ordinary Bitrix homepages.

**Signals:** Bitrix chrome; a **datasets** catalog section (открытые данные), not a news CMS. A geoportal on the same CMS uses a site template such as `/bitrix/cache/css/s1/investmap/`.

**Confirm:** GET the public dataset listing or the public map catalog. One catalog per dataset portal or geoportal.

| Tool | Query |
|------|-------|
| Google | `"Битрикс" открытые данные` |
| Censys | `web.endpoints.http.body: "bitrix"` |
| FOFA | `body="bitrix"` |

## Gosweb (`gosweb`) {#gosweb}

Gosuslugi website constructor for Russian state and municipal bodies. Tenants use `*.gosweb.gosuslugi.ru` or a branded host that still loads Gosweb assets.

**Signals:** `static.gosweb.gosuslugi.ru/omsu/`; NetCat template `/netcat_template/template/gw_omsu/`; open-data path `/ofitsialno/statistika/otkrytye-dannye/` with `list.csv` or `meta.csv`.

**Confirm:** GET the open-data page and match `gw_omsu`. One catalog per municipality or agency site. Do not tag a generic NetCat site that lacks `gw_omsu` (for example Obninsk). Do not tag `esnsi.gosuslugi.ru`.

| Tool | Query |
|------|-------|
| Google | `site:gosweb.gosuslugi.ru "открытые данные"` |
| Google | `"gw_omsu" "открытые данные"` |
| Censys | `web.endpoints.http.body: "netcat_template/template/gw_omsu"` |
| FOFA | `body="netcat_template/template/gw_omsu"` |
| FOFA | `body="static.gosweb.gosuslugi.ru/omsu"` |

## Copernicus Data Stores (`copernicuscds`) {#copernicuscds}

ECMWF Climate / Atmosphere / CEMS data stores. Hub: [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu).

**Confirm:** do **not** clone the CDS hub. Register only a distinct CDS/ADS/CEMS catalog UI. Harvest recipes: [harvest-earthdata.md](harvest-earthdata.md#copernicuscds).

| Tool | Query |
|------|-------|
| Google | `"Climate Data Store" Copernicus` |
| Censys | `web.names: "cds.climate.copernicus.eu"` |
| FOFA | `host="cds.climate.copernicus.eu"` |

## D4Science (`d4science`) {#d4science}

CNR virtual research environments with a gCube CKAN data-catalogue. Site: [d4science.org](https://www.d4science.org).

**Signals:** `/web/{lab}/data-catalogue`; `gcube-ckan-datacatalog`; D4Science VRE chrome.

**Confirm:** GET the public data-catalogue for that VRE. One catalog per lab catalogue, not the D4Science marketing home.

| Tool | Query |
|------|-------|
| Google | `"D4Science" (catalog OR "open data")` OR `inurl:d4science.org/web` |
| Censys | `web.names: "d4science.org"` |
| FOFA | `domain="d4science.org"` |

## data.gov.my (`datagovmy`) {#datagovmy}

Malaysia national open-data stack. Hub: [data.gov.my](https://www.data.gov.my).

**Confirm:** register **tenant** catalogs on the stack, not a second copy of the national hub. Duplicate-check `*.data.gov.my`.

| Tool | Query |
|------|-------|
| Google | `site:data.gov.my` tenant catalogs only |
| Censys | `web.names: "data.gov.my"` |
| FOFA | `host="data.gov.my"` |

## JDOP (`jdop`) {#jdop}

Zhejiang public-data open platform (浙江•数据开放). Distinct from Inspur oPortal (`oportal`) and ODWeb (`odweb`).

**Signals:** `/jdop_front/` or `/dopServer/`; 浙江•数据开放 chrome.

**Confirm:** GET the public dataset catalog. One record per provincial/municipal JDOP tenant.

| Tool | Query |
|------|-------|
| Google | `"JDOP" オープンデータ` OR `"jdop_front"` |
| Censys | `web.endpoints.http.body: "jdop_front"` |
| FOFA | `body="jdop_front"` |

## Open Data Registry (`opendatareg`) {#opendatareg}

AWS Labs YAML registry of public datasets (and regional IT clones named OpenData.reg). Source: [awslabs/open-data-registry](https://github.com/awslabs/open-data-registry).

**Confirm:** GET a public dataset registry UI or the published catalog files. Skip a GitHub clone with no catalog UI. One catalog per public registry.

| Tool | Query |
|------|-------|
| Google | `"opendata.reg"` OR `"Open Data Registry" awslabs` |
| Censys | `web.endpoints.http.body: "open-data-registry"` |
| FOFA | `body="open-data-registry"` |

## PublishMyData (`publishmydata`) {#publishmydata}

Swirrl linked-data publisher for official statistics. Site: [publishmydata.com](https://publishmydata.com). Docs: [publishmydata.com/docs](https://publishmydata.com/docs).

**Signals:** PublishMyData chrome; SPARQL / linked-data catalog UI.

**Confirm:** GET the public dataset/SPARQL catalog. One catalog per deployment.

| Tool | Query |
|------|-------|
| Google | `"PublishMyData" OR publishmydata` |
| Censys | `web.endpoints.http.body: "PublishMyData"` |
| FOFA | `body="PublishMyData"` |

## Semantic MediaWiki (`smw`) {#smw}

MediaWiki with semantic queries used as a dataset catalog. Site: [semantic-mediawiki.org](https://www.semantic-mediawiki.org). Skip ordinary MediaWiki encyclopedias.

**Signals:** Semantic MediaWiki / `#ask` catalog pages; RDF export of datasets.

**Confirm:** GET a public dataset/category listing. One catalog per wiki that publishes datasets.

| Tool | Query |
|------|-------|
| Google | `"Semantic MediaWiki" (dataset OR catalog)` |
| Censys | `web.endpoints.http.body: "Semantic MediaWiki"` |
| FOFA | `body="Semantic MediaWiki"` |

## Strapi (`strapi`) {#strapi}

Headless CMS. Site: [strapi.io](https://strapi.io). Docs: [strapi.io/docs](https://strapi.io/docs). Use only with a **public dataset API**, not a blog CMS.

**Signals:** `/api/` content-types that list datasets; Strapi admin is not the catalog.

**Confirm:** GET a public dataset collection. Skip login-only Strapi. One catalog per public API.

| Tool | Query |
|------|-------|
| Google | `"Strapi" ("open data" OR datasets)` |
| Censys | `web.endpoints.http.body: "strapi"` |
| FOFA | `body="strapi"` |

## Tablion (`tablion`) {#tablion}

Aristotle Metadata data-request portal. Product: [Tablion Data Portal](https://www.aristotlemetadata.com/products/tablion-data-portal/). Help: [tablion-help.aristotlemetadata.com](https://tablion-help.aristotlemetadata.com/). Tenants are `{org}.tabliondata.com` or a customer domain (DSS uses [requestdata.dss.gov.au](https://requestdata.dss.gov.au/)). The apex `tabliondata.com` is a Netlify redirect to the marketing page.

**Signals:** public home nav `Dataset Library`, `Apply for Data Passport`, `Submit a Data Request`, and `Register` / `Login`. Default copy on the product screenshot is “Step 1: Apply for Data Passport”. Mail from a tenant is `notifications@noreply.tabliondata.com`.

**Confirm:** GET the public home or Dataset Library. One catalog per portal. Stop on `403` from `awselb` (the app tenants reject crawlers). Skip the marketing redirect. An Aristotle Metadata Registry (`body="aristotle_mdr"`, `*.aristotlecloud.io`, `/account/login/`) is [`aristotlemdr`](discovery-metadata.md#aristotlemdr), not Tablion.

**FOFA** (checked 24 September 2026). There is no `app="Tablion"`. `body="Tablion"` is a mention search (38 hosts). The word is also a Byzantine garment, so the first hits are fashion-history sites, a museum, restaurants, and the vendor’s own pages (`aristotlemetadata.com`, `community.aristotlemetadata.com`, `help.aristotlemetadata.com`, `tabliondata.com`). `title="tablion"` returned 0. `body="Tablion Data Portal"` returned 2 (the vendor home and a conference page). `body="powered by Tablion"`, `body="/static/tablion"`, and `body="noreply.tabliondata.com"` returned 0.

`host=` is a substring, but the app tenants are not in the web index: `domain="tabliondata.com"` and `host="tabliondata.com"` returned 3 (apex and `www`, the marketing redirect), and `cert="tabliondata.com"` returned 2 of the same. `host="dcj.tabliondata.com"`, `host="mast.tabliondata.com"`, `host="temporary.tabliondata.com"`, and `host="dss.tabliondata.com"` returned 0, as did `cert=` for those names. `body="Apply for Data Passport"` and `body="Dataset Library" && body="Data Passport"` returned 0 because that HTML is behind the load balancer. `body="Dataset Library"` alone returned 174 unrelated hosts. `body="Submit a Data Request"` returned 391.

Find tenant names in Certificate Transparency (`%.tabliondata.com`), then GET. Unexpired names on 24 September 2026: `dss.tabliondata.com`, `dcj.tabliondata.com`, `mast.tabliondata.com`, `temporary.tabliondata.com`, plus the apex. All four app hosts returned HTTP 403 (`server: awselb/2.0`), including `/robots.txt`. Historical urlscan captures `metservice.tabliondata.com` (2023) and `boldatapassport.tabliondata.com` (2022) no longer resolve.

| Query | Hits | What it matches |
|-------|------|-----------------|
| `domain="tabliondata.com"` | 3 | Marketing redirect only (`tabliondata.com`, `www`) |
| `host="tabliondata.com"` | 3 | Same. Does not list `{org}.tabliondata.com` while those hosts are absent from the index |
| `cert="tabliondata.com"` | 2 | Marketing certificate, not the tenant certificates |
| `body="Apply for Data Passport"` | 0 | Product chrome; use it when a tenant HTML page is indexed |
| `body="Dataset Library" && body="Data Passport"` | 0 | Same chrome, both labels |
| `body="Tablion"` | 38 | Garment, museums, vendor docs. Not a portal list |

| Tool | Query |
|------|-------|
| Google | `"tabliondata.com" OR "Apply for Data Passport"` |
| Censys | `web.names: "tabliondata.com"` |
| FOFA | `domain="tabliondata.com"` |
| FOFA | `host="tabliondata.com"` |
| Censys | `web.endpoints.http.body: "Apply for Data Passport"` |
| FOFA | `body="Apply for Data Passport"` |
| crt.sh | `%.tabliondata.com` |

## Other open-data platforms

| `software.id` | Signals | Typical query |
|---------------|---------|---------------|
| `ouropendata` | see above | |
| `gipuzkoairekia` | see above | |
| `datapress` | see above | |
| `modaopendata` | see above | |
| `bitrix` | see above | |
| `jdop` | see above | |
| `publishmydata` | see above | |
| `opendatareg` | see above | |
| `datagovmy` | see above | |
| `copernicuscds` | see above | |
| `tablion` | see above | |
| `strapi` | see above | |
| `smw` | see above | |
| `d4science` | see above | |
| `rdfrepository` | see above | |
| `resourcecontracts` | see above | |
| `openspending` | see above | |
| `gxopendata` | see above | |

## Generic open-data URL patterns

Try these on a **named** government or city host only (not as an internet-wide scan):

- `/data`, `/opendata`, `/datasets`, `/catalog`, `/datos`, `/donnees`
- `/data.json`, `/catalog.json`, `/catalog.xml` (DCAT)
- `/api/3/action/status_show` (CKAN)
- `/api/explore/v2.1/catalog/datasets` (OpenDataSoft)
- `/IdraPortal/` and `/Idra/api/v1/` (Idra)
- `/oportal/` (Inspur oPortal)
- `/static/opendata1.0/` (Taiji Digital)
- `/openinf/` (Seoul Open Data Plaza)
- `/assets/cms/public.css` (Our Open Data)
- `*.revenuedev.org` tenant home (RDF Online Repository)
- `/contract/resources` (ResourceContracts)
- `{city}.data.gxzf.gov.cn` (Guangxi tenant)
- `/transparencia/datos/catalogo` (ATM Maggioli)
- `/opendata/set/lkod` (LKOD, including Slovak municipal clones)

Search with local terms plus the city: `datos abiertos "Rosario"`, `offene Daten "Leipzig"`, `开放数据 市`.

## National harvest sources {#national-harvest-sources}

When a country already has a national open-data portal, its **harvest / organisations / catalogues API** is a better candidate list than Google. Prompt: `Which data sources harvested by {national portal} are missing?`

Portals that produced origin catalogs in 28–30 August 2026 sessions:

| National portal | What to pull | Typical origin catalogs |
|-----------------|--------------|-------------------------|
| [data.go.id](https://data.go.id/) | Harvest-source list | Provincial/city CKAN and GeoServer (112 scheduled in one pass) |
| [datos.gob.es](https://datos.gob.es/) | Harvest sources | City/province CKAN and custom `/datos` |
| [opendata.swiss](https://opendata.swiss) | Harvest sources | Cantonal votes, BAG indicator DBs, Viageo — not geocat/I14Y/LINDAS slices |
| [data.gov.ru](https://data.gov.ru/) | Organisations with `/opendata` | Federal agency `list.csv` catalogs (Rosstat, Minenergo, …) |
| [search.open.canada.ca](https://search.open.canada.ca/opendata/) | Harvested origin URLs | Provincial geo/scientific portals not already in the registry |
| [data.gouv.fr](https://www.data.gouv.fr/) | Harvest sources | Local CKAN / uData / OpenDataSoft |
| [www.govdata.de](https://www.govdata.de/) | Harvest sources | Länder / municipal CKAN |
| [www.data.go.kr](https://www.data.go.kr/) | Harvest sources | Ministry/local portals |
| [dane.gov.pl](https://dane.gov.pl) | Institutions API | CKAN city catalogs only — thousands of XML dataset feeds are not catalogs |
| [data.europa.eu catalogues](https://data.europa.eu/data/catalogues) | Catalogue list | Member-state catalogs |

**Accept:** a live independent catalog UI on the origin host (CKAN `/api/3`, GeoNetwork CSW, ArcGIS Hub, agency `/opendata` dataset list). `is_national: false` on those origin catalogs.

**Reject:** harvest-source *rows* inside the national CKAN; XML/CSV dataset feeds and developer price files; slices of the same national catalog (geocat, I14Y, LINDAS); scientific IR dumps already registered; login walls; a private ArcGIS org when a public Hub exists (register the Hub).

Duplicate-check the origin hostname, then GET the origin homepage. Do not invent harvest API paths — use the portal’s documented organisations/harvest endpoint.


## GIS Open Data Portal (`gisopendataportal`) {#gisopendataportal}

Shared municipal catalog deployed at `tvrdosin.twinmap.ai` and `nove-mesto.twinmap.ai`.
Both `/developer` pages identify the same `gis-open-data-portal/od-portal` source project
and document `/api/open-api/features`, GraphQL at `/api/open-api`, and DCAT-AP-SK at
`/api/opendata/set/catalog/lkod`. Confirm this combination and the repository attribution;
a `twinmap.ai` hostname or a Next.js bundle alone is insufficient. The advertised GitLab
repository redirected to sign-in on 2026-09-07, so do not assume a verified open-source license.

Search: `"gis-open-data-portal/od-portal"`, `site:twinmap.ai "OpenAPI"`.
First-party examples: [Tvrdošín developer guide](https://tvrdosin.twinmap.ai/developer),
[Nové Mesto developer guide](https://nove-mesto.twinmap.ai/developer).


| Tool | Query |
|------|-------|
| Google | `"gis-open-data-portal/od-portal" OR site:twinmap.ai OpenAPI` |
| Censys | `web.names: "twinmap.ai"` |
| FOFA | `host="twinmap.ai"` |


## Esri UK Data Observatory (`esridataobservatory`) {#esridataobservatory}

Managed local-data service, formerly InstantAtlas Data Observatory. Confirm vendor or
operator attribution to the product, with supporting Data Explorer / Quick Ward Profile /
Custom Area Reporter features. Technical corroboration includes
`hub.instantatlas.com/data-catalog-explorer/` assets and `window.dataCatalogExplorer.launch`.
WordPress, ArcGIS maps, or an embedded report alone do not establish this product.
Confirmed Oxfordshire, Kingston, and Ealing deployments load `/wp-content/themes/ia-theme/`
with `ia-map.js`, `ia-quickprofile.js`, and `ia-stat.js`, and explicitly credit Esri UK.
Use this combination of theme assets and attribution as a stronger installation fingerprint.
The [vendor product page](https://www.esriuk.com/en-gb/arcgis/products/instantatlas/products/data-observatory)
identifies Suffolk; the [Hounslow case study](https://resource.esriuk.com/esri-resources/london-borough-of-hounslow/)
confirms another independent deployment. See the [branding and theme documentation](https://help.instantatlas.com/category/data-observatory/).

Search: `"Esri UK Data Observatory"`, `"InstantAtlas Data Observatory"`,
`"hub.instantatlas.com/data-catalog-explorer"`.


| Tool | Query |
|------|-------|
| Google | `"Esri UK Data Observatory" OR "InstantAtlas Data Observatory"` |
| Censys | `web.endpoints.http.body: "hub.instantatlas.com/data-catalog-explorer"` |
| FOFA | `body="dataCatalogExplorer"` |


## RUDI (`rudi`) {#rudi}

An independently deployable, distributed data-sharing platform. The
[portal source](https://github.com/rudi-platform/rudi-portal) identifies the
[Rennes deployment](https://rudi.rennesmetropole.fr/); the
[out-of-the-box distribution](https://github.com/rudi-platform/rudi-out-of-the-box)
provides Docker Compose installation. Match explicit RUDI branding and project provenance,
not generic Angular bundles. Producer nodes and the central metadata portal have different
interfaces. See [API documentation](https://doc.rudi.fr/api/api_exposees/).


| Tool | Query |
|------|-------|
| Google | `"RUDI" (données OR "data sharing") -site:github.com` |
| Censys | `web.endpoints.http.body: "rudi-portal"` |
| FOFA | `body="RUDI" && body="rudi"` |


## SIMAI Open Data Portal (`simaiopendata`) {#simaiopendata}

The [vendor product page](https://simai.ru/solution/gosudarstvennye-organizatsii/simai-portal-otkrytykh-dannykh/)
markets a dedicated 1C-Bitrix open-data application and links its
[current demo](https://opendata.sf2.simai.ru/). Strong fingerprints are explicit
«SIMAI: Портал открытых данных» credit plus `simai.opendata` template/cache asset paths.
Generic `/bitrix/` assets alone do not identify this product. The Bashkortostan-branded
vendor demo is not a production government portal; the old `opendata.demo.simai.ru`
host currently serves a hosting placeholder.


| Tool | Query |
|------|-------|
| Google | `"SIMAI" "Портал открытых данных" OR simai.opendata` |
| Censys | `web.endpoints.http.body: "simai.opendata"` |
| FOFA | `body="simai.opendata"` |

## Aid Management Platform (`amp`) {#amp}

Development Gateway aid-information system. Product: [devgateway.github.io/amp](https://devgateway.github.io/amp/). Country installations publish official development-assistance activities. Source: [github.com/devgateway/amp](https://github.com/devgateway/amp).

**Signals:** “Aid Management Platform” or AMP portal chrome on a government aid-transparency host.

**Confirm:** GET the public activity catalog. One record per country portal, not per report, chart, or dashboard. Skip PDF-only aid reports that are not an AMP installation.

[about-template.html](https://github.com/devgateway/amp/blob/develop/amp/TEMPLATE/ampTemplate/amp-boilerplate/src/templates/about-template.html) serves `/TEMPLATE/ampTemplate/` (105 hosts in September 2026, including `amp.mofed.gov.et` and `amp.gov.md`). `body="Aid Management Platform"` matched 34, the same product, including `amp.finance.go.ug`. Translated skins drop the English name, so keep both.

| Tool | Query |
|------|-------|
| Google | `"Aid Management Platform" (portal OR "development assistance" OR disbursement)` |
| Google | `"ampTemplate" (aid OR ODA OR portal)` |
| Censys | `web.endpoints.http.body: "ampTemplate"` |
| FOFA | `body="ampTemplate"` |
| Censys | `web.endpoints.http.body: "Aid Management Platform"` |
| FOFA | `body="Aid Management Platform"` |

## Het Dataloket (`dataloket`) {#dataloket}

Analyze SaaS catalog of data assets for Dutch municipalities and provinces. Product: [Het Dataloket](https://kbenp.nl/expertise/datatoepassingen). Tenants use their own host (`data.venlo.nl`, `dataportaal.tilburg.nl`, `dataportaal.prvlimburg.nl`), not a shared vendor domain.

**Signals:** HTML title “Dataportaal”; `/assets/img/search-blue.svg` and `/assets/img/logo_analyze.svg`; `/api/configuration` JSON with `feature_flags.has_public_portal`; `/api/search` JSON with `Total` and `Results`; Kibana host `dataloket-{org}-*.kb.westeurope.azure.elastic-cloud.com`.

**Confirm:** GET `/api/configuration` and `/api/search`. One record per tenant host. Register a tenant when `/api/search` returns public (`Openbaar`) assets, including Venlo where `has_public_portal` is false. Do **not** set `dataloket` on `dataportaal-viewer.prvlimburg.nl` (a separate indicator viewer), Civity CKAN at `ckan.dataplatform.nl`, or Swing `*.incijfers.nl`.

| Tool | Query |
|------|-------|
| Google | `"Dataportaal" "search-blue.svg"` |
| Google | `"Het Dataloket" (gemeente OR provincie) dataportaal` |
| Censys | `web.endpoints.http.body: "/assets/img/search-blue.svg"` |
| FOFA | `body="/assets/img/search-blue.svg"` |

## Contrataciones Abiertas (`contratacionesabiertas`) {#contratacionesabiertas}

INAI EDCA-MX capture system and public dashboard. Source: [datosabiertosmx/contrataciones-abiertas-infraestructura](https://github.com/datosabiertosmx/contrataciones-abiertas-infraestructura) (version 2.1.8). The dashboard is `/contratacionesabiertas/datosabiertos`. `static/javascripts/common.js` sets `globals.site.url` and `globals.site.port` for the capture API.

**Signals:** path `/contratacionesabiertas/datosabiertos`; `/contratacionesabiertas/static/bower_components/`; `X-Powered-By: Express`; common.js comment `Variables de conexion a la API del sistema de captura para contrataciones abiertas`.

**Confirm:** GET the datos abiertos page and match that common.js comment. Read `globals.site` and confirm `GET {url}:{port}/edca/fiscalYears` returns JSON. One record per institution. Do **not** set `contratacionesabiertas` on Peru's OECE portal, on a page that only cites the OCDS standard, or on INFO CDMX CKAN (`datosabiertos.infocdmx.org.mx`).

| Tool | Query |
|------|-------|
| Google | `inurl:/contratacionesabiertas/datosabiertos` |
| Google | `"sistema de captura para contrataciones abiertas"` |
| Censys | `web.endpoints.http.body: "/contratacionesabiertas/static/javascripts/common.js"` |
| FOFA | `body="/contratacionesabiertas/static/javascripts/common.js"` |

## Centurion (`centurion`) {#centurion}

eBdesk government data portal. Product login: [centurion.id](https://centurion.id). Vendor description: [Government Intelligence](https://www.ebdesk.com/goverment-intelligence.html). Live shells include [data.kalselprov.go.id](https://data.kalselprov.go.id), [sadaina.sumutprov.go.id](https://sadaina.sumutprov.go.id), and [data.polri.go.id](https://data.polri.go.id).

**Signals:** `<html theme-fontsize data-maps>` and `<body theme-shape="rounded">`. Module federation `https://fem.centurion.id/remoteEntry.js`, or same-host `/femc/remoteEntry.js` whose body starts with `var Charts`. Tenant hostnames `*.centurion.id`.

**Confirm:** GET the public portal and match that shell. A `satudata.*` hostname alone is not Centurion. One installation = one record. Kalimantan Selatan `data.`, `opendata.`, and `satupeta.` share one `metadata_datasets` collection (same `totalCount`); keep the registered open-data host. Do **not** register `satudata.kalselprov.go.id` (GraphQL returns 401), the `centurion.id` login, or `fem.centurion.id`.

| Tool | Query |
|------|-------|
| Google | `"theme-fontsize" "data-maps" (satudata OR "open data" OR "satu data")` |
| Censys | `web.endpoints.http.body: "theme-fontsize"` |
| FOFA | `body="theme-fontsize" && body="data-maps"` |
| FOFA | `body="fem.centurion.id/remoteEntry.js"` |

## CreatorCMS (`creatorcms`) {#creatorcms}

Chinese government website CMS data-open module on Hunan municipal portals. Catalog path `/webapp/{city}/dataPublic/index.jsp` (or `/webapp/{city}/index.jsp`), dataset pages `dataDetail.jsp?id=`, front-end assets `KCUI/KCUI3.min.js`, backend routes `/creatorCMS/`.

**Signals:** path `/webapp/{city}/` + `dataDetail.jsp`; body strings `KCUI/KCUI3` or `/creatorCMS/`; page title 数据开放.

**Confirm:** GET the data-open page and match `KCUI` or `creatorCMS`. One municipal catalog = one record. Do not register the parent government homepage or non-data modules of the same CMS.

| Tool | Query |
|------|-------|
| Google | `inurl:dataPublic inurl:index.jsp 数据开放` |
| Google | `"creatorCMS" 数据开放` |
| Censys | `web.endpoints.http.body: "creatorCMS"` |
| FOFA | `body="/creatorCMS/" || body="KCUI/KCUI3"` |

## Anhui open-data-web (`ahopendataweb`) {#ahopendataweb}

Anhui provincial/municipal public-data platform. Catalog under `/open-data-web/` with Struts `.do` actions (Hefei `index-hfs.do`, Bozhou `index.do`) or `/dataopen-web/` on the provincial host `data.ahzwfw.gov.cn`. Distinct from Inspur oPortal (`oportal`), Zhejiang JDOP (`jdop`), ODWeb (`odweb`).

**Signals:** path `/open-data-web/` or `/dataopen-web/`; `.do` index actions; 公共数据开放平台 chrome.

**Confirm:** GET the catalog root and match the path scheme. One city or provincial catalog = one record.

| Tool | Query |
|------|-------|
| Google | `inurl:open-data-web 数据开放` |
| Google | `inurl:dataopen-web 安徽` |
| Censys | `web.endpoints.http.path: "/open-data-web/"` |
| FOFA | `body="open-data-web" && title="数据开放"` |

## openportal (`openportal`) {#openportal}

Chinese government open-data portal product serving the catalog under `/extranet/openportal/pages/...`. Observed on Yichun, Jiangxi (`data.yichun.gov.cn`) and Zhangjiakou, Hebei (`kf.zjkzwfw.gov.cn`). Distinct from Inspur oPortal (`oportal`) and ODWeb (`odweb`).

**Signals:** path `/extranet/openportal/pages/`; default index `pages/default/index.html`.

**Confirm:** GET `/extranet/openportal/pages/default/index.html`. One municipal catalog = one record.

| Tool | Query |
|------|-------|
| Google | `inurl:extranet inurl:openportal` |
| Censys | `web.endpoints.http.path: "/extranet/openportal/"` |
| FOFA | `body="/extranet/openportal/"` |

## Oraș Digital (`orasdigital`) {#orasdigital}

Romanian municipal open-data portal product by [Oraș Digital](https://oras.digital) ("Connecting the City through technology"), deployed per city as `{city}.oras.digital` with a sister city-app at `{city}.digital`. Known deployment: Iași ([iasi.oras.digital](https://iasi.oras.digital/), alias `opendata.oras.digital`). Distinct from CKAN-based Romanian portals and from the vendor marketing homepage itself.

**Signals:** host `*.oras.digital`; title `Portal Open Data {City}`; Cloudflare-hosted shell loading `assets/js/app.min.js` and `assets/css/app.css`; dataset routes `/datasets/{slug}/` with institution and format filters (HTML, CSV, XLS, XLSX, API); API docs at `/api-docs/` linking a Postman collection (`assets/api/api-postman-collection.json`).

**Confirm:** GET the city subdomain and match the portal shell plus `/api-docs/`. One record per city portal; do not register `oras.digital`, `cx.oras.digital`, or cPanel port variants on the apex, and treat `{city}.digital` city apps as separate products, not portals.

| Tool | Query |
|------|-------|
| Google | `site:oras.digital "Portal Open Data"` |
| Google | `"oras.digital" "Documentație API"` |
| Censys | `web.names: "oras.digital"` |
| FOFA | `host="oras.digital"` |
| FOFA | `body="api-postman-collection.json"` |

## Bon Maximus e-Procurement (`bonmaximus`) {#bonmaximus}

Nigerian vendor-built electronic government procurement portal by [Bon Maximus Companies Ltd](https://bonmaximus.com) (Abuja; "e-Procurement, e-QS, and Digital Solutions"). Deployed for Nigerian state Bureaus of Public Procurement; known public OCDS-facing installs: Kogi (`eproc.bpp.kg.gov.ng`), Osun (`egp.osunstate.gov.ng`), Abia (`abiaeprocurement.ab.gov.ng`), Ebonyi (`ebonyieprocure.eb.gov.ng`), Anambra (`eprocure.bpp.an.gov.ng`).

**Signals:** footer credit "Powered by Bon Maximus Companies"; IIS/10.0 backend with ASP.NET-style pages (`publication.php`, award/tender listing routes); site title pattern `Home | {State} ...`.

**Confirm:** GET the portal root and match the "Bon Maximus" footer credit. One record per state BPP portal. Do not register `bonmaximus.com` itself (vendor marketing), and do not set this id on Nigerian e-procurement portals without the credit (e.g. Edo, Bauchi, Jigawa, Ogun builds are separate one-offs). Do not set `ckan` — no CKAN API is exposed.

| Tool | Query |
|------|-------|
| Google | `"Powered by Bon Maximus"` |
| Google | `inurl:e-procurement OR inurl:eprocure "Bon Maximus"` |
| FOFA | `body="Bon Maximus"` |
| Censys | `web.endpoints.http.body: "Bon Maximus"` |

## Budeshi (`budeshi`) {#budeshi}

Open contracting data platform by the Public and Private Development Centre (PPDC, Nigeria; [budeshi.ng](https://www.budeshi.ng)). Hosts government procurement portals publishing projects, tenders, and awards as OCDS releases with documented HTTP APIs. Known install: Kaduna State Open Contracting Portal (`www.ocds.kdsg.gov.ng`, endpoints `/api` and `/ocds-api`).

**Signals:** footer or page credit "Powered By Budeshi"; OCDS release/search pages; documented REST endpoints (`/api`, `/ocds-api`) serving OCDS JSON.

**Confirm:** GET the portal root or `/api` and match the Budeshi credit or OCDS API. One record per deployment. Do not register `budeshi.ng` itself (platform home), and do not set `bonmaximus` on Budeshi-hosted portals or vice versa — check the footer credit.

| Tool | Query |
|------|-------|
| Google | `"Powered By Budeshi" OR "powered by budeshi"` |
| Google | `inurl:ocds "Budeshi"` |
| FOFA | `body="Budeshi"` |
| Censys | `web.endpoints.http.body: "Budeshi"` |

## MapaInversiones (`mapainversiones`) {#mapainversiones}

IDB regional public-investment transparency platform, open source since 2025
(Code4Dev catalog). National deployments in 14+ Latin American and Caribbean
countries, usually on a planning-ministry domain and branded "MapaInversiones"
(for example `rendircuentas.mideplan.go.cr`, `mapainversiones.dnp.gov.co`,
`mapainversiones.gob.do`). Regional hub: [iadb.org
MapaInversiones](https://www.iadb.org/es/quienes-somos/topicos/modernizacion-del-estado/mapainversiones).

**Signals:** page title or footer "MapaInversiones" (often "+ Módulo
COVID-19"); ASP.NET/IIS stack; sections Presupuesto / Contratación Pública /
Entidades / Inversiones Públicas / Datos Abiertos; BID (IDB) credit on the
"Acerca de" page.

**Confirm:** GET the site root and match the MapaInversiones brand or the IDB
credit. One record per national deployment. Do not register the regional
iadb.org hub pages as catalogs.

| Tool | Query |
|------|-------|
| Google | `"MapaInversiones" "Datos Abiertos" (gob OR gov)` |
| Google | `intitle:MapaInversiones inversión pública` |
| Censys | `web.endpoints.http.body: "MapaInversiones"` |
| FOFA | `body="MapaInversiones"` |

## Related

- [discovery.md](discovery.md)
- [discovery.md](discovery.md#hunt-patterns) — session hunt patterns
- [discovery-search-tools.md](discovery-search-tools.md)
- [discovery-metadata.md](discovery-metadata.md)
- [discovery-indicators.md](discovery-indicators.md)
- [discovery-other.md](discovery-other.md)
- [harvest-opendata.md](harvest-opendata.md)
- [harvest.md](harvest.md)
- [harvest-protocols.md](harvest-protocols.md)
- [apidetect.md](apidetect.md)
- [ckan-sync.md](ckan-sync.md)
- [catalog-types.md](catalog-types.md)
- [software-taxonomy.md](software-taxonomy.md)

