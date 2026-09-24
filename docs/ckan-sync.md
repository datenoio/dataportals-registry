# CKAN ecosystem sync

`scripts/sync_ckan_ecosystem.py` imports CKAN sites from the [CKAN ecosystem dataset](https://ecosystem.ckan.org/dataset/ckan-sites-metadata). Duplicate `link` values are skipped. New records default to `data/scheduled/`.

## Commands

```bash
python scripts/sync_ckan_ecosystem.py --dry-run
python scripts/sync_ckan_ecosystem.py
python scripts/sync_ckan_ecosystem.py --entities
python scripts/sync_ckan_ecosystem.py --delay 2.0 --no-enrich
```

| Flag | Effect |
|------|--------|
| `--dry-run` | Log candidates; write nothing |
| `--scheduled` / `--entities` | Target directory (default scheduled) |
| `--enrich` / `--no-enrich` | Scrape title/description from the live site |
| `--delay` | Seconds between HTTP requests (default `1.0`) |

## What it does

1. Fetches CKAN site records from ecosystem.ckan.org.
2. Loads existing registry ids/URLs from exports.
3. Normalizes URLs (scheme, `www`, trailing slash) and skips duplicates.
4. Optionally scrapes the public homepage for name/description.
5. Calls the same `add-single` path as the CLI.

After a real sync, run `python scripts/builder.py assign` and `validate-yaml`. Promote reviewed files with [scheduled.md](scheduled.md). Finding catalogs in general: [discovery.md](discovery.md).

## Insights dashboard as a hunt source

[CKAN Ecosystem Insights](https://ecosystem.ckan.org/insights) is a weekly-crawl dashboard over every portal the ecosystem catalog tracks: per-instance dataset counts, CKAN versions, installed extensions, and crawl reliability. The page reads a published rollup that can be diffed against registry exports without scraping:

```bash
curl -sLO https://raw.githubusercontent.com/dathere/pose-ckanext-metadata/main/dashboard-data/dashboard.json
# dashboard.json -> instances[]: n (name), u (url), h (host), d (datasets), up (weekly reachability), gone
```

Match each instance host against `data/datasets/full.parquet` (`link` and `endpoints[].url` hosts). Watch for alias domains before adding: portals often answer on both `*.gov.ar`/`*.gob.ar`-style pairs, and the CKAN `status_show` `site_url` reveals the canonical host. Instances flagged `gone` or with all-zero `up` weeks are usually dead — probe before scheduling.

Maintainer notes: [devdocs/ckan_ecosystem_sync.md](https://github.com/datenoio/dataportals-registry/blob/main/devdocs/ckan_ecosystem_sync.md).
