# Data model

Each catalog is one YAML document validated against `data/schemes/catalog.json` (Cerberus). JSON Schema with descriptions: `data/schemes/catalog.schema.json`. DCAT/schema.org mappings: `data/schemes/catalog.context.jsonld` ([exports.md](exports.md#json-ld--dcat)). Vocabularies: [vocabularies.md](vocabularies.md).

## Required fields

| Field | Type | Notes |
|-------|------|--------|
| `id` | string | Filename stem; lowercase letters and digits |
| `uid` | string | `cdi########` for entities; assigned by `builder.py assign` |
| `name` | string | Display name |
| `link` | string | Catalog URL |
| `catalog_type` | string | See [catalog-types.md](catalog-types.md) |
| `access_mode` | list of string | Prefer `open` or `restricted` |
| `status` | string | `active`, `inactive`, `scheduled`, or `deprecated` |
| `software` | object | `{id, name}` — `id` should exist under `data/software/` |
| `owner` | object | `{name, type, location.country.{id,name}}` |
| `coverage` | list | At least one `{location.country.{id,name}}` — enforced by the `MISSING_COVERAGE` quality rule (IMPORTANT), not by the Cerberus schema |

## Recommended fields

| Field | Purpose |
|-------|---------|
| `description` | Short human-readable summary |
| `endpoints` | Harvestable APIs (`type`, `url`, optional `version`) |
| `identifiers` | `{id, value, url}` for wikidata / re3data / fairsharing |
| `langs` | `{id, name}` e.g. `EN` / `English` |
| `tags` | Keywords (`government`, `has_api`, …) |
| `topics` | `{type, id, name}` — EU data themes or ISO 19115 |
| `api` / `api_status` | Set together when an API exists |
| `owner.link` | Owning organization URL |
| `content_types` | e.g. `dataset`, `map_layer` |
| `rights` | `license_id`, `license_name`, `license_url`, `rights_type`, `tos_url`, `privacy_policy_url` |

## Optional / enrichment fields

| Field | Purpose |
|-------|---------|
| `properties` | Flags such as `has_doi`, `is_national`, `transferable_topics`, `transferable_location`, `unfinished`, `dataset_count_reported` |
| `catalog_export` | Export/syndication label (e.g. `CKAN API`) |
| `trust_score` / `trust_score_components` | Optional 0–100 score; see [trust-score.md](trust-score.md) |
| `_re3data` | Re3Data payload; see [re3data.md](re3data.md) |

Do not invent `uid`. Scheduled records use `temp########` until [scheduled.md](scheduled.md) promotion.

## Properties

`properties` is an optional object of catalog flags (schema: `data/schemes/catalog.json`). Common keys:

| Key | Type | Meaning |
|-----|------|---------|
| `has_doi` | boolean | Catalog or datasets routinely expose DOIs |
| `is_national` | boolean | Official national catalog of that type (see below). **Not** “owned by a federal/central agency” |
| `transferable_topics` | boolean | Topics may be copied onto related records |
| `transferable_location` | boolean | Location may be copied onto related records |
| `unfinished` | boolean | Record is known incomplete; do not treat as fully curated |
| `dataset_count_reported` | integer | Count claimed by the source (not verified by this repo) |
| `base_last_seen` | string | Internal harvest/seen stamp; do not invent for new YAML |
| `invenio-filters` | string | Invenio search filter used during enrichment |

Omit keys you cannot verify. These flags are not a substitute for `status` or `coverage`.

### `properties.is_national`

Set `is_national: true` only when the catalog is the country’s **official catalog of that type**:

| May be true | Must be false |
|-------------|----------------|
| Primary national open-data portal (`data.gov`, `datos.gob`, `data.gouv.fr`, Satu Data, …). Typically **one current** plus **one documented legacy** per country | Ministry/agency open data (NASA, NOAA labs, INPS, VA, health, mining) |
| NSDI / national geoportal / INSPIRE node (typically 1–2 per country) | Agency GIS (USGS park, HRSA, NOAA CoastWatch, mining cadastre) |
| NSO indicators, NSO microdata, IMF NSDP, optional Open Data for Africa country page | Line-ministry dashboards (HMIS, EMIS, energy, budget) |
| National metadata registry when it is the country MDR | Scientific domain/lab repos (NCBI, ERDDAP, DAACs, DSpace, Dataverse) |
| | Subnational catalogs, civil society/academy/business, MapBiomas, resource-contracts sites, museums |

Federal/central ownership is already expressed by the `Federal/` directory, `owner.type` (`Central government` / `Federal government`), and `coverage.level: 20`. Do **not** copy `is_national: true` onto every federal `.gov`/`.mil` catalog.

If you have reviewed a catalog and it is not national, set `is_national: false` rather than omitting the key. Classifier and quality rule: `scripts/national_catalog.py` (`IS_NATIONAL_AGENCY_OR_TOPIC`). Batch realignment: `python scripts/fix_is_national_flags.py`.

## Owner

Canonical `owner.type` values (see `data/reference/owner_types.yaml`):

`Local government`, `Central government`, `Regional government`, `Federal government`, `Academy`, `Business`, `Civil society`, `International`, `Community`, `Other`.

Synonyms such as `University` → `Academy` are accepted by quality checks but new entries should use canonical values.

`owner.location.level` uses the same scale as coverage: **20 national, 30+ subnational** (higher = more local). Regional/local owners need level 30 or higher and a matching subregion directory. Full table: [vocabularies.md](vocabularies.md#geographic-levels).

## Coverage location

```yaml
coverage:
- location:
    country:
      id: US
      name: United States
    level: 20
    macroregion:
      id: '021'
      name: Northern America
    subregion:
      id: US-CA
      name: California
```

`level` is numeric (higher = more local). Subregion `id` uses ISO 3166-2 style when the catalog is not national. Country `id` and macroregion `id` are strings: quote `'NO'` (Norway) and M49 codes (`'021'`, `'155'`). Identifier and endpoint vocabularies: [vocabularies.md](vocabularies.md).

`tags` is a list of strings. Quote numeric tags (`'911'`). Do not use `{tag: water}` mappings.

## Endpoints

```yaml
endpoints:
- type: ckan
  url: https://catalog.data.faa.gov/api/3
  version: '3'
- type: dcatus11
  url: https://catalog.data.faa.gov/data.json
```

Common `type` values include `ckan`, `ckan:package-search`, `dcatap201`, `dcatus11`, `geonetwork:csw`, `oaipmh`, `socrata:opendata`, `stac`, `sparql`. Use the types already present for the same `software.id`.

## Example (verified entity)

```yaml
access_mode:
- open
api: true
api_status: active
catalog_type: Open data portal
id: catalogdatafaagov
link: https://catalog.data.faa.gov
name: Federal Aviation Administration Open Data Portal
owner:
  name: Federal Aviation Administration
  type: Central government
  location:
    country:
      id: US
      name: United States
    level: 20
software:
  id: ckan
  name: CKAN
status: active
uid: cdi00005263
```

Full file: `data/entities/US/Federal/opendata/catalogdatafaagov.yaml`.

## Software records

Software YAML under `data/software/{category}/{id}.yaml` includes `id`, `name`, `category`, `subtype`, API/metadata support flags, and documentation URLs. See [software-taxonomy.md](software-taxonomy.md).
