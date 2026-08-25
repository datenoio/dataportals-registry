# OpenAIRE Graph data sources

`scripts/extract_openaire_portals.py` lists **data portals registered in the OpenAIRE Graph** ([Graph data sources API](https://graph.openaire.eu/docs/apis/graph-api/data-sources/)). It is the harvest list for GitHub issue #41. Attaching OpenAIRE ids onto catalogs we already have is issue #31 — reuse the same JSON dump.

The script talks to `https://api.openaire.eu/graph/v3/datasources`. It does not scrape Explore HTML.

## Commands

```bash
python scripts/extract_openaire_portals.py list-sources --output /tmp/openaire_sources.json
python scripts/extract_openaire_portals.py match-registry --input /tmp/openaire_sources.json --output /tmp/openaire_misses.json
python scripts/extract_openaire_portals.py add-scheduled --input /tmp/openaire_misses.json --dry-run
python scripts/extract_openaire_portals.py add-scheduled --input /tmp/openaire_misses.json
```

| Flag | Effect |
|------|--------|
| `--types` | Comma-separated `dataSourceTypeName` values (default: data repositories, mixed IRs, journal aggregators) |
| `--check-datasets` | Extra Graph `research-products?type=dataset` call for mixed IRs with no other data signal |
| `--delay` | Seconds between Graph pages (default `0.2`) |
| `--dry-run` | Log candidates; write nothing |
| `--detect` | On `add-scheduled`, also run `apidetect` (slow) |
| `--limit` | Cap how many scheduled YAML files to write |

After a real add, run `python scripts/builder.py assign --mode scheduled` and `python scripts/builder.py validate-yaml`. Probe OAI-PMH/REST before promoting ([harvest-scientific.md](harvest-scientific.md), [scheduled.md](scheduled.md)).

## What it keeps

OpenAIRE has ~150k data sources; most are journals. The harvest keeps `dataSourceTypeName` in:

- **Data Repository** / **Data Repository Aggregator** (always, if the `websiteUrl` is a real catalog host)
- **Institutional / Thematic / Publication Repository** and **Journal Aggregator/Publisher** only when they look like they publish datasets

Publication-only IRs are dropped using, in order: OpenDOAR `contentTypes`, re3data/FAIRsharing `collectedFrom`, OpenAIRE data compatibility, name/URL signals (Dataverse, Figshare, “research data”, …), then an optional Graph dataset count.

Placeholder hosts (`test.de`, `example.com`, FAIRsharing/re3data registry pages) are skipped. Duplicate detection is **hostname** against `data/datasets/datasets.duckdb` (and `data/scheduled/`).

New scheduled records use `catalog_type: Scientific data repository`, `software.id: custom` unless the URL is an obvious Dataverse/Figshare host, and an `identifiers[]` row with `id: openaire`.

## Related

- Finding CONNECT/EXPLORE gateways: [discovery-other.md](discovery-other.md#openaire)
- Scientific IR harvest filters: [harvest-scientific.md](harvest-scientific.md)
- CKAN bulk import (same scheduled pattern): [ckan-sync.md](ckan-sync.md)
