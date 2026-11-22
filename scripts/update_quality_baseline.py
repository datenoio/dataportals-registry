#!/usr/bin/env python3
"""Regenerate dataquality/baseline_counts.json from current quality reports."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from quality_regression import DEFAULT_BASELINE, DEFAULT_REPORT, write_baseline


app = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(help="Update quality regression baseline counts")
def main(
    report: Annotated[str, typer.Option("--report", help="Path to full_report.jsonl")] = str(DEFAULT_REPORT),
    baseline: Annotated[str, typer.Option("--baseline", help="Path to baseline JSON")] = str(DEFAULT_BASELINE),
) -> None:
    payload = write_baseline(
        baseline_path=Path(baseline),
        report_path=Path(report),
    )
    typer.echo(f"Updated baseline: {baseline}")
    typer.echo(f"  CRITICAL: {payload['by_priority']['CRITICAL']}")
    typer.echo(f"  IMPORTANT: {payload['by_priority']['IMPORTANT']}")
    typer.echo(f"  MEDIUM: {payload['by_priority']['MEDIUM']}")
    typer.echo(f"  LOW: {payload['by_priority']['LOW']}")
    by_track = payload.get("by_track") or {}
    integrity = by_track.get("integrity") or {}
    enrichment = by_track.get("enrichment") or {}
    typer.echo(
        "  Integrity CRITICAL/IMPORTANT: "
        f"{integrity.get('CRITICAL', 0)}/{integrity.get('IMPORTANT', 0)}"
    )
    typer.echo(
        "  Enrichment MEDIUM/LOW: "
        f"{enrichment.get('MEDIUM', 0)}/{enrichment.get('LOW', 0)}"
    )


if __name__ == "__main__":
    app()
