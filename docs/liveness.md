# Catalog URL liveness

HTTP probes of each catalog `link`. The weekly workflow writes `dataquality/liveness_report.jsonl` as a CI artifact. A local apply step can mark confirmed-dead catalogs `status: inactive`. Schema fields such as `liveness_status` / `last_verified_at` are not on catalog YAML.

Workflow: `.github/workflows/liveness.yml` (weekly Sunday 03:00 UTC, plus `workflow_dispatch`). Script: `scripts/check_liveness.py`. Do not commit stale probe reports.

## Local run

```bash
python scripts/check_liveness.py --sample 10
python scripts/check_liveness.py --country World --delay 0.25
python scripts/check_liveness.py --output dataquality/liveness_report.jsonl
```

`--sample N` picks N random entity records (seed 42 by default). `--country` is an ISO code or a folder such as `World`. `--timeout` defaults to 10 seconds; `--retries` defaults to 2.

## Apply dead hosts

Only `liveness_status: dead` rows with a `cdi########` UID are eligible. Timeouts classified as `error` / `inconclusive` are not applied. Confirm a sample in a browser before `--write`.

```bash
python scripts/check_liveness.py --apply-dead --dry-run
python scripts/check_liveness.py --apply-dead --write
```

`--write` sets `status: inactive` and, when present, `api: false` / `api_status: inactive`. Download the weekly GitHub Actions artifact over the local report before applying.

Do not turn this into an internet-wide scanner. It only reads `link` values already in `data/entities/`.

## Status values

| Status | Meaning |
|--------|---------|
| `live` | Successful HTTP response for the catalog URL |
| `redirect` | HTTP redirect to another location |
| `dead` | Persistent client error (for example 404) |
| `inconclusive` | Timeout, 5xx after retries, or TLS/network noise |
| `error` | Request failed before an HTTP status was available |

Treat `inconclusive` as a probe problem, not proof the catalog is gone. Confirm in a browser before changing `status: inactive`.

## Related

- [architecture.md](architecture.md)
- [metadata-quality.md](metadata-quality.md)
- [apidetect.md](apidetect.md)
- [releasing.md](releasing.md)
