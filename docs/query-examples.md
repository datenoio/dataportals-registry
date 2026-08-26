# Query examples (DuckDB)

Verified patterns against `data/datasets/datasets.duckdb` (table `catalogs`) or `data/datasets/full.parquet`. Nested fields are `STRUCT` / `LIST` — see [ai-consumers.md](ai-consumers.md).

## Connect

```python
import duckdb

con = duckdb.connect("data/datasets/datasets.duckdb")
```

```python
import duckdb

con = duckdb.connect()
con.execute("SELECT count(*) FROM 'data/datasets/full.parquet'").fetchone()
```

## Counts by catalog type

```sql
SELECT catalog_type, count(*) AS n
FROM catalogs
GROUP BY 1
ORDER BY n DESC;
```

## CKAN portals in the United States

```sql
SELECT id, name, link
FROM catalogs
WHERE software.id = 'ckan'
  AND list_contains(
        list_transform(coverage, x -> x.location.country.id),
        'US'
      )
  AND status = 'active'
ORDER BY name
LIMIT 50;
```

## Active catalogs with an API

```sql
SELECT id, name, catalog_type, software.id AS software_id
FROM catalogs
WHERE api = true
  AND api_status = 'active'
ORDER BY name
LIMIT 50;
```

## Geoportals by software

```sql
SELECT software.id AS software_id, count(*) AS n
FROM catalogs
WHERE catalog_type = 'Geoportal'
GROUP BY 1
ORDER BY n DESC;
```

## External identifiers (Wikidata)

```sql
SELECT id, name, identifiers
FROM catalogs
WHERE list_contains(list_transform(identifiers, x -> x.id), 'wikidata')
LIMIT 20;
```

## Scientific repositories with re3data

```sql
SELECT id, name, link
FROM catalogs
WHERE catalog_type = 'Scientific data repository'
  AND list_contains(list_transform(identifiers, x -> x.id), 're3data')
ORDER BY name
LIMIT 50;
```

## Is this URL already registered?

```sql
SELECT id, name, link, catalog_type, status
FROM catalogs
WHERE lower(link) LIKE '%example.gov%';
```

Use this before adding a catalog. Full workflow: [discovery.md](discovery.md).

## Software table

```sql
SELECT id, name, category
FROM software
ORDER BY name;
```

## Metadata catalogs (FAIR Data Point)

```sql
SELECT id, name, link, status
FROM catalogs
WHERE catalog_type = 'Metadata catalog'
   OR software.id = 'fairdatapoint'
ORDER BY name;
```

DuckDB/Parquet lag source YAML until the next `build`. Duplicate-check `data/scheduled/` as well as exports.

## Scientific IRs to harvest (mixed publications + data)

```sql
SELECT id, name, link, software.id AS software_id
FROM catalogs
WHERE catalog_type = 'Scientific data repository'
  AND status = 'active'
  AND software.id IN (
    'dspace', 'dspacecris', 'invenio', 'inveniordm', 'eprints',
    'hyrax', 'pure', 'esploro', 'opus', 'elsevierdigitalcommons',
    'figshare', 'converis', 'omegapsir', 'archipelago'
  )
ORDER BY software_id, name
LIMIT 50;
```

Dataset-native scientific platforms (`labkey`, `synapse`, `xnat`, `omero`, `kadi4mat`, `edal`, `nomad`, `redivis`) and domain stacks (`intermine`, `gringlobal`, `plutof`, `jgi`, `cbioportal`, `esasciencearchive`) use the same `catalog_type` filter with those `software.id` values. Recipes: [software-index.md](software-index.md).

API recipes and dataset-vs-publication filters: [harvest.md](harvest.md).

## Catalogs with recorded endpoints

Nested `endpoints` is `STRUCT[]`. A non-empty array means at least one probed API URL:

```sql
SELECT id, name, software.id AS software_id, endpoints
FROM catalogs
WHERE len(endpoints) > 0
ORDER BY name
LIMIT 50;
```

## Owner type

```sql
SELECT owner.type AS owner_type, count(*) AS n
FROM catalogs
GROUP BY 1
ORDER BY n DESC;
```

```sql
SELECT id, name, link
FROM catalogs
WHERE owner.type = 'Central government'
  AND status = 'active'
LIMIT 50;
```

Canonical values: [vocabularies.md](vocabularies.md).

## Scheduled and inactive

`data/datasets/catalogs.jsonl` is verified entities. Scheduled rows are in `full.jsonl` / `full.parquet` / `datasets.duckdb` table `catalogs` only after a build that includes scheduled — prefer `full.parquet` if counts look short.

```sql
SELECT id, name, link, status
FROM catalogs
WHERE status = 'scheduled';
```

```sql
SELECT id, name, link, catalog_type
FROM catalogs
WHERE status = 'inactive'
ORDER BY name
LIMIT 50;
```

## Catalogs without a public API flag

```sql
SELECT id, name, software.id AS software_id
FROM catalogs
WHERE api = false
  AND status = 'active'
ORDER BY name
LIMIT 50;
```

`api: false` means no recorded public API — not that the site is empty.

## Join catalogs to software definitions

```sql
SELECT
  c.id,
  c.name,
  c.software.id AS software_id,
  s.name AS software_name,
  s.category
FROM catalogs c
LEFT JOIN software s
  ON c.software.id = s.id
WHERE c.software.id = 'geonetwork'
LIMIT 20;
```

## JSONL without DuckDB

```python
import json

with open("data/datasets/catalogs.jsonl", encoding="utf-8") as fh:
    for line in fh:
        rec = json.loads(line)
        if rec.get("software", {}).get("id") == "ckan":
            print(rec["id"], rec["link"])
```

## Polars / Parquet

```python
import polars as pl

df = pl.read_parquet("data/datasets/full.parquet")
ckan = df.filter(pl.col("software").struct.field("id") == "ckan")
print(ckan.select(["id", "name", "link"]).head())
```
