"""CLI parsing of scripts converted from argparse or bare ``__main__`` to typer
(openspec: refactor-shared-script-library, Entry-Point Conventions).

The conversion keeps option names, defaults and exit codes, and a
single-command script runs without a subcommand name. No test here makes a
network request or writes outside ``tmp_path``.
"""

import logging

import pytest
from typer.main import get_command
from typer.testing import CliRunner

import check_liveness
import docs_software_coverage
import refresh_subregion_reference
import remove_scheduled_duplicates
import update_quality_baseline

runner = CliRunner()


def _options(app):
    """Map each option's parameter name to (flags, default)."""
    return {
        param.name: (sorted(param.opts), param.default)
        for param in get_command(app).params
    }


# --- check_liveness ---------------------------------------------------------


def test_check_liveness_keeps_argparse_options_and_defaults():
    options = _options(check_liveness.app)
    assert options == {
        "entities": (["--entities"], str(check_liveness.DEFAULT_ENTITIES)),
        "output": (["--output"], str(check_liveness.DEFAULT_OUTPUT)),
        "country": (["--country"], None),
        "sample": (["--sample"], None),
        "timeout": (["--timeout"], 10.0),
        "retries": (["--retries"], 2),
        "delay": (["--delay"], 0.0),
        "workers": (["--workers"], 16),
        "seed": (["--seed"], 42),
        "apply_dead": (["--apply-dead"], False),
        "dry_run": (["--dry-run"], True),
        "write": (["--write"], False),
    }


@pytest.fixture
def fake_probe(monkeypatch):
    """Replace record loading and probing so the CLI makes no requests."""
    calls = {}
    records = [
        {"uid": f"cdi0000000{i}", "link": f"https://host{i}.example/", "id": f"r{i}", "country": "XX"}
        for i in range(3)
    ]

    def fake_iter(entities_dir, country=None):
        calls["entities_dir"] = entities_dir
        calls["country"] = country
        return iter(records)

    def fake_probe_records(recs, output_path, **kwargs):
        recs = list(recs)
        calls["records"] = recs
        calls["output_path"] = output_path
        calls.update(kwargs)
        return [
            check_liveness.ProbeResult(
                uid=r["uid"], link=r["link"], liveness_status="live", http_code=200, checked_at="t"
            )
            for r in recs
        ]

    monkeypatch.setattr(check_liveness, "iter_catalog_records", fake_iter)
    monkeypatch.setattr(check_liveness, "probe_records", fake_probe_records)
    return calls


def test_check_liveness_workflow_invocation_parses(fake_probe):
    """.github/workflows/liveness.yml runs the script with no subcommand name."""
    result = runner.invoke(
        check_liveness.app,
        ["--workers", "64", "--delay", "0.25", "--sample", "1", "--country", "XX"],
    )
    assert result.exit_code == 0, result.output
    assert fake_probe["workers"] == 64
    assert fake_probe["delay"] == 0.25
    assert fake_probe["timeout"] == 10.0
    assert fake_probe["retries"] == 2
    assert fake_probe["country"] == "XX"
    assert len(fake_probe["records"]) == 1
    assert fake_probe["entities_dir"] == check_liveness.DEFAULT_ENTITIES
    assert fake_probe["output_path"] == check_liveness.DEFAULT_OUTPUT
    assert result.stdout.splitlines() == [
        f"Wrote 1 results to {check_liveness.DEFAULT_OUTPUT}",
        "  live: 1",
    ]


def test_check_liveness_defaults_probe_every_record(fake_probe, tmp_path):
    result = runner.invoke(
        check_liveness.app,
        ["--entities", str(tmp_path / "entities"), "--output", str(tmp_path / "out.jsonl")],
    )
    assert result.exit_code == 0, result.output
    assert fake_probe["workers"] == 16
    assert fake_probe["delay"] == 0.0
    assert fake_probe["country"] is None
    assert len(fake_probe["records"]) == 3
    assert fake_probe["entities_dir"] == tmp_path / "entities"
    assert fake_probe["output_path"] == tmp_path / "out.jsonl"


@pytest.mark.parametrize(
    "extra, dry_run, label",
    [
        ([], True, "Dry-run"),
        (["--dry-run"], True, "Dry-run"),
        (["--write"], False, "Applied"),
    ],
)
def test_check_liveness_apply_dead_flags(monkeypatch, tmp_path, extra, dry_run, label):
    seen = {}

    def fake_apply(report_path, entities_dir, dry_run=True):
        seen["dry_run"] = dry_run
        seen["report_path"] = report_path
        return [{"uid": "cdi00000001", "action": "would_inactivate", "path": "x.yaml"}]

    monkeypatch.setattr(check_liveness, "apply_dead_from_report", fake_apply)
    report = tmp_path / "report.jsonl"
    result = runner.invoke(check_liveness.app, ["--apply-dead", "--output", str(report), *extra])
    assert result.exit_code == 0, result.output
    assert seen == {"dry_run": dry_run, "report_path": report}
    assert result.stdout.splitlines() == [
        f"{label} 1 dead-row actions from {report}",
        "  would_inactivate: cdi00000001 x.yaml",
    ]


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_check_liveness_help_flags(flag):
    result = runner.invoke(check_liveness.app, [flag])
    assert result.exit_code == 0
    assert "--workers" in result.stdout


def test_check_liveness_usage_error_exits_2():
    result = runner.invoke(check_liveness.app, ["--no-such-option"])
    assert result.exit_code == 2


def test_probe_records_logs_progress(tmp_path, caplog):
    class _Session:
        def request(self, method, url, timeout=None, allow_redirects=None):
            class _Response:
                status_code = 200

            response = _Response()
            response.url = url
            return response

    records = [{"uid": "cdi00000001", "link": "https://a.example/"}]
    with caplog.at_level(logging.INFO, logger="check_liveness"):
        check_liveness.probe_records(
            records, tmp_path / "out.jsonl", workers=1, retries=0, progress_every=1, session_factory=_Session
        )
    assert "Probed 1/1" in caplog.messages


# --- refresh_subregion_reference --------------------------------------------


def test_refresh_subregion_reference_options():
    assert _options(refresh_subregion_reference.app) == {
        "output": (["--output"], "data/reference/subregions/ISO3166-2.CSV"),
    }


def test_refresh_subregion_reference_writes_csv(tmp_path):
    output = tmp_path / "subregions.csv"
    result = runner.invoke(refresh_subregion_reference.app, ["--output", str(output)])
    assert result.exit_code == 0, result.output
    lines = output.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "code,subdivision_name"
    assert result.stdout.strip() == f"Wrote {len(lines) - 1} rows to {output.resolve()}"


# --- update_quality_baseline ------------------------------------------------


def test_update_quality_baseline_options():
    assert _options(update_quality_baseline.app) == {
        "report": (["--report"], str(update_quality_baseline.DEFAULT_REPORT)),
        "baseline": (["--baseline"], str(update_quality_baseline.DEFAULT_BASELINE)),
    }


def test_update_quality_baseline_prints_counts(monkeypatch, tmp_path):
    seen = {}

    def fake_write_baseline(baseline_path, report_path):
        seen["baseline_path"] = baseline_path
        seen["report_path"] = report_path
        return {
            "by_priority": {"CRITICAL": 1, "IMPORTANT": 2, "MEDIUM": 3, "LOW": 4},
            "by_track": {
                "integrity": {"CRITICAL": 1, "IMPORTANT": 2},
                "enrichment": {"MEDIUM": 3, "LOW": 4},
            },
        }

    monkeypatch.setattr(update_quality_baseline, "write_baseline", fake_write_baseline)
    baseline = tmp_path / "baseline.json"
    report = tmp_path / "full_report.jsonl"
    result = runner.invoke(
        update_quality_baseline.app, ["--report", str(report), "--baseline", str(baseline)]
    )
    assert result.exit_code == 0, result.output
    assert seen == {"baseline_path": baseline, "report_path": report}
    assert result.stdout.splitlines() == [
        f"Updated baseline: {baseline}",
        "  CRITICAL: 1",
        "  IMPORTANT: 2",
        "  MEDIUM: 3",
        "  LOW: 4",
        "  Integrity CRITICAL/IMPORTANT: 1/2",
        "  Enrichment MEDIUM/LOW: 3/4",
    ]


# --- docs_software_coverage -------------------------------------------------


def _patch_coverage(monkeypatch, tmp_path, missing=((), ()), headings=((), ()), combined=(), stale=()):
    dest = tmp_path / "software-index.md"
    monkeypatch.setattr(docs_software_coverage, "missing_mentions", lambda: tuple(list(x) for x in missing))
    monkeypatch.setattr(docs_software_coverage, "missing_headings", lambda: tuple(list(x) for x in headings))
    monkeypatch.setattr(docs_software_coverage, "combined_software_headings", lambda: list(combined))
    monkeypatch.setattr(docs_software_coverage, "stale_software_anchor_links", lambda: list(stale))
    monkeypatch.setattr(docs_software_coverage, "write_index", lambda: dest)
    return dest


def test_docs_software_coverage_runs_without_arguments(monkeypatch, tmp_path):
    dest = _patch_coverage(monkeypatch, tmp_path)
    result = runner.invoke(docs_software_coverage.app, [])
    assert result.exit_code == 0, result.output
    assert result.stdout.splitlines() == [
        f"Wrote {dest}",
        "All software IDs mentioned; unique H2s; anchors current.",
    ]


def test_docs_software_coverage_lists_gaps(monkeypatch, tmp_path):
    dest = _patch_coverage(
        monkeypatch,
        tmp_path,
        missing=(["a", "b"], ["c"]),
        headings=(["d"], ["e"]),
        combined=["discovery.md:1:## X"],
        stale=["harvest.md:2: #old → #new"],
    )
    result = runner.invoke(docs_software_coverage.app, [])
    assert result.exit_code == 0, result.output
    assert result.stdout.splitlines() == [
        f"Wrote {dest}",
        "Missing discovery mentions: a, b",
        "Missing harvest mentions: c",
        "Missing discovery headings: d",
        "Missing harvest headings: e",
        "Combined software H2s (split these):",
        "  discovery.md:1:## X",
        "Stale software heading links:",
        "  harvest.md:2: #old → #new",
    ]


# --- remove_scheduled_duplicates --------------------------------------------


@pytest.fixture
def scheduled_tree(monkeypatch, tmp_path):
    entities = tmp_path / "entities" / "XX" / "opendata"
    scheduled = tmp_path / "scheduled" / "XX" / "opendata"
    entities.mkdir(parents=True)
    scheduled.mkdir(parents=True)
    (entities / "foo.yaml").write_text("id: foo\nlink: https://foo.example.org\n", encoding="utf-8")
    (scheduled / "foo.yaml").write_text("id: foo\nlink: https://foo.example.org/\n", encoding="utf-8")
    (scheduled / "bar.yaml").write_text("id: bar\nlink: https://bar.example.org\n", encoding="utf-8")
    monkeypatch.setattr(remove_scheduled_duplicates, "ENTITIES_DIR", tmp_path / "entities")
    monkeypatch.setattr(remove_scheduled_duplicates, "SCHEDULED_DIR", tmp_path / "scheduled")
    return scheduled


def test_remove_scheduled_duplicates_dry_run(scheduled_tree, caplog):
    with caplog.at_level(logging.INFO, logger="remove_scheduled_duplicates"):
        result = runner.invoke(remove_scheduled_duplicates.app, ["--dry-run"])
    assert result.exit_code == 0, result.output
    assert (scheduled_tree / "foo.yaml").exists()
    assert result.stdout.splitlines() == [
        "  [would remove] foo -> exists in entities",
        "",
        "Removed: 1, kept: 1",
    ]
    assert "DRY RUN - no files will be deleted" in caplog.messages
    assert "Loaded 1 entity IDs, 1 entity URLs" in caplog.messages


def test_remove_scheduled_duplicates_removes(scheduled_tree):
    result = runner.invoke(remove_scheduled_duplicates.app, [])
    assert result.exit_code == 0, result.output
    assert not (scheduled_tree / "foo.yaml").exists()
    assert (scheduled_tree / "bar.yaml").exists()
    assert result.stdout.splitlines() == [
        "  [removed] foo",
        "",
        "Removed: 1, kept: 1",
        "",
        "Next steps:",
        "  python scripts/builder.py build",
    ]
