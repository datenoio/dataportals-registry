# Exports

Generated artifacts live in `data/datasets/`. Rebuild with `python scripts/builder.py build`. Never hand-edit this directory.

## Primary dumps

| File | Contents |
|------|----------|
| `catalogs.jsonl` (+ `.zst`) | Verified entities only |
| `scheduled.jsonl` (+ `.zst`) | Unverified scheduled records (may be empty) |
| `full.jsonl` (+ `.zst`) | Entities + scheduled |
| `software.jsonl` (+ `.zst`) | Software / platform definitions |
| `full.parquet` | Analytics table of `full.jsonl` |
| `datasets.duckdb` | Tables `catalogs` and `software` |
| `catalogs.jsonld` | Optional; `build --jsonld` |

## Record counts

Do not mix these three numbers. Exports lag YAML until `python scripts/builder.py build`.

| Layer | Date | Catalogs | Scheduled | Software | Countries |
|-------|------|----------|-----------|----------|-----------|
| **Published GitHub snapshot** | v1.18.0, 28 August 2026 | **24,993** | **7** | **282** | **219** |
| **Working-tree exports** | last `build` in this tree (28 August 2026) | **24,993** (`catalogs.jsonl`) | **7** | **282** | **219** |
| **Current source YAML** | 28 August 2026 | **24,993** (`data/entities/`) | **7** (`data/scheduled/`) | **282** | **219** |

Working-tree dumps match source YAML (**24,993** catalogs). Canonical software IDs: `data/reference/software_ids.yaml`.

Filter by catalog type or software in DuckDB / Parquet (see [query-examples.md](query-examples.md)); there are no pre-sliced `bytype/` or `bysoftware/` dumps.

Incidental files such as `software_stats.csv` or `fulldbreg.parquet` may appear in `data/datasets/` from older tooling — prefer the primary dumps above.

## Compression

`.zst` files are [zstandard](https://facebook.github.io/zstd/). Decompress with `unzstd file.zst` or stream them in Python via `zstandard`.

## DuckDB columns

`datasets.duckdb` table `catalogs` (same nested types as `full.parquet`). Lists are DuckDB `LIST` (`VARCHAR[]` or `STRUCT[]`); objects are `STRUCT`. Query with field access (`software.id`) and list functions (`list_contains`, `unnest`, `list_transform`) rather than `LIKE` on JSON text. Heterogeneous Re3Data leaves may remain `JSON`. `api` is `BOOLEAN`.

| Column | JSONL type | DuckDB |
|--------|------------|--------|
| `id`, `uid`, `name`, `link`, `catalog_type`, `status`, `api_status`, `description`, `catalog_export` | string | VARCHAR |
| `api` | boolean | BOOLEAN |
| `access_mode`, `content_types`, `tags` | list of strings | VARCHAR[] |
| `langs`, `topics`, `identifiers`, `endpoints`, `coverage` | list of objects | STRUCT[] |
| `software`, `owner`, `rights`, `properties` | object | STRUCT |
| `_re3data` | object | STRUCT (some nested leaves `JSON`) |

Table `software` keeps Yes/No flags (`has_api`, `has_bulk`) as VARCHAR. Nested `datatypes`, `metadata_support`, `owner`, `license`, `pid_support`, and `rights_management` are STRUCT; `export_formats` and `capabilities` are VARCHAR[].

`trust_score` is optional on YAML and may be absent from a given DuckDB build if no records in the snapshot have the field.

## JSON-LD / DCAT

`data/schemes/catalog.context.jsonld` maps fields to DCAT-AP, Dublin Core, schema.org, and the `cdi:` namespace. Emit a framed dump with:

```bash
python scripts/builder.py build --jsonld
```

| Catalog field | JSON-LD term |
|---------------|--------------|
| (type) | `dcat:DataCatalog` |
| `name` | `dct:title` |
| `description` | `dct:description` |
| `link` | `dcat:landingPage` |
| `owner` | `dct:publisher` |
| `rights` | `dct:rights` |
| `access_mode` | `dct:accessRights` |
| `identifier` | `dct:identifier` |
| `id` | `cdi:id` |
| `uid` | `cdi:uid` |
| `catalog_type` | `cdi:catalogType` |
| `status` | `cdi:status` |
| `software` | `cdi:software` |
| `coverage` | `cdi:coverage` |
| `endpoints` | `cdi:endpoints` |
| `identifiers` | `cdi:identifiers` |
| `api` | `cdi:hasApi` |
| `api_status` | `cdi:apiStatus` |
| `tags` | `cdi:tags` |
| `topics` | `cdi:topics` |
| `langs` | `cdi:langs` |
| `content_types` | `cdi:contentTypes` |
| `trust_score` | `cdi:trustScore` |
| `properties` | `cdi:properties` |
| `catalog_export` | `cdi:catalogExport` |
| `_re3data` | `cdi:re3dataEnrichment` |

`cdi:` is `https://commondata.io/ns/dataportals-registry#`.
