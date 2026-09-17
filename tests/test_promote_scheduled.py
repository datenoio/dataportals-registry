"""Tests for scripts/promote_scheduled.py — selective, subregion-aware, liveness-gated promotion."""

import sys
from pathlib import Path

import pytest
import typer
import yaml
from typer.testing import CliRunner

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import promote_scheduled as ps  # noqa: E402

runner = CliRunner()


def make_record(rid, link="https://example.com", country="US", subregion=None, status="scheduled"):
    owner_loc = {"country": {"id": country, "name": country}}
    cov_loc = {"country": {"id": country, "name": country}, "level": 20}
    if subregion:
        owner_loc["subregion"] = {"id": subregion, "name": subregion}
        cov_loc["subregion"] = {"id": subregion, "name": subregion}
    return {
        "id": rid,
        "uid": "temp00000001",
        "name": f"Test {rid}",
        "link": link,
        "catalog_type": "Open data portal",
        "access_mode": ["open"],
        "status": status,
        "software": {"id": "custom", "name": "Custom"},
        "owner": {"name": "Owner", "type": "Central government", "location": owner_loc},
        "coverage": [{"location": cov_loc}],
    }


def write_scheduled(base, country, type_dir, record):
    d = base / country / type_dir
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{record['id']}.yaml"
    path.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True))
    return path


@pytest.fixture
def dirs(tmp_path):
    scheduled = tmp_path / "scheduled"
    entities = tmp_path / "entities"
    scheduled.mkdir()
    entities.mkdir()
    return scheduled, entities


# ---------------------------------------------------------------------------
# --id filter
# ---------------------------------------------------------------------------


class TestIdFilter:
    def test_promotes_only_requested_ids(self, dirs):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("reca"))
        write_scheduled(scheduled, "US", "opendata", make_record("recb"))
        counters = ps.promote_records(ids=["reca"], scheduled_dir=scheduled, entities_dir=entities)
        assert counters["promoted"] == 1
        assert (entities / "US" / "Federal" / "opendata" / "reca.yaml").exists()
        assert (scheduled / "US" / "opendata" / "recb.yaml").exists()

    def test_unknown_id_errors(self, dirs):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("reca"))
        with pytest.raises(typer.Exit):
            ps.promote_records(ids=["nope"], scheduled_dir=scheduled, entities_dir=entities)
        # nothing moved
        assert (scheduled / "US" / "opendata" / "reca.yaml").exists()

    def test_cli_unknown_id_exit_1(self):
        result = runner.invoke(ps.app, ["--id", "definitely-not-a-real-id-xyz"])
        assert result.exit_code == 1
        assert "not found" in result.output


# ---------------------------------------------------------------------------
# Subregion routing
# ---------------------------------------------------------------------------


class TestSubregionRouting:
    def test_valid_subregion_routes_and_sets_level(self, dirs):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("carec", subregion="US-CA"))
        ps.promote_records(scheduled_dir=scheduled, entities_dir=entities)
        target = entities / "US" / "US-CA" / "opendata" / "carec.yaml"
        assert target.exists()
        data = yaml.safe_load(target.read_text())
        assert data["owner"]["location"]["level"] == 30
        assert data["coverage"][0]["location"]["level"] == 30

    def test_unknown_subregion_falls_back_to_federal(self, dirs, capsys):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("badrec", subregion="US-ZZ"))
        ps.promote_records(scheduled_dir=scheduled, entities_dir=entities)
        assert (entities / "US" / "Federal" / "opendata" / "badrec.yaml").exists()
        assert "falling back to Federal" in capsys.readouterr().out

    def test_no_subregion_stays_federal(self, dirs):
        scheduled, entities = dirs
        write_scheduled(scheduled, "FR", "opendata", make_record("frrec"))
        ps.promote_records(scheduled_dir=scheduled, entities_dir=entities)
        assert (entities / "FR" / "Federal" / "opendata" / "frrec.yaml").exists()


# ---------------------------------------------------------------------------
# Probe gating
# ---------------------------------------------------------------------------


class TestProbeGating:
    def _patch_probe(self, monkeypatch, results):
        monkeypatch.setattr(ps, "probe_url", lambda url, session, timeout=10.0: results[url])

    def test_dead_stays_in_scheduled(self, dirs, monkeypatch):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("deadrec", link="http://dead.example"))
        self._patch_probe(monkeypatch, {"http://dead.example": (None, "timeout: boom", None)})
        counters = ps.promote_records(probe=True, scheduled_dir=scheduled, entities_dir=entities)
        assert counters["dead"] == 1
        assert counters["promoted"] == 0
        assert (scheduled / "US" / "opendata" / "deadrec.yaml").exists()

    def test_live_promotes(self, dirs, monkeypatch):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("liverec", link="http://ok.example"))
        self._patch_probe(monkeypatch, {"http://ok.example": (200, None, "http://ok.example")})
        counters = ps.promote_records(probe=True, scheduled_dir=scheduled, entities_dir=entities)
        assert counters["promoted"] == 1
        assert (entities / "US" / "Federal" / "opendata" / "liverec.yaml").exists()

    def test_inconclusive_promotes_with_warning(self, dirs, monkeypatch, capsys):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("botrec", link="http://bot.example"))
        self._patch_probe(monkeypatch, {"http://bot.example": (403, None, "http://bot.example")})
        counters = ps.promote_records(probe=True, scheduled_dir=scheduled, entities_dir=entities)
        assert counters["promoted"] == 1
        assert "promoting anyway" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Country hints
# ---------------------------------------------------------------------------


class TestCountryHints:
    def test_hints_file_loads(self):
        hints = ps.load_country_hints()
        assert hints, "country_hints.yaml should load"
        assert all("country" in h for h in hints)

    @pytest.mark.parametrize(
        "haystack,expected",
        [
            ("brasilio https://brasil.io/x", "BR"),
            ("myaxiellsite https://axiell.example.com", "NL"),
            ("inondationsdakar https://floods.example.com", "SN"),
            ("unesco data https://unesco.example.org", "World"),
            ("dhsprogram https://dhsprogram.example.com", "US"),
            ("data4citizen https://data4citizen.example.com", "FR"),
            ("junar portal https://junar.example.com", "CL"),
            ("d4science https://d4science.example.org", "EU"),
        ],
    )
    def test_known_patterns(self, haystack, expected):
        hints = ps.load_country_hints()
        assert ps.match_country_hint(haystack.lower(), hints) == expected

    def test_all_form_requires_every_substring(self):
        hints = ps.load_country_hints()
        both = ps.match_country_hint("zastrug https://zastrug.opendatasoft.com", hints)
        only_one = ps.match_country_hint("someportal https://x.opendatasoft.com", hints)
        assert both == "RS"
        assert only_one is None

    def test_infer_country_uses_hints_after_tld(self):
        record = make_record("dakar floods", link="https://floods-dakar.example.com", country="Unknown")
        assert ps.infer_country_for_unknown(record) == "SN"

    def test_infer_country_tld_beats_hints(self):
        record = make_record("plain", link="https://data.gouv.fr", country="Unknown")
        assert ps.infer_country_for_unknown(record) == "FR"


# ---------------------------------------------------------------------------
# review-scheduled
# ---------------------------------------------------------------------------


class TestReviewScheduled:
    def _patch_exports_and_probe(self, monkeypatch, live_map):
        import hunt

        monkeypatch.setattr(
            hunt,
            "_build_export_indexes",
            lambda: ({"existingrec"}, {"https://existing.example.com": "existingrec"}, {}),
        )

        def fake_probe_rows(candidates, **kwargs):
            out = []
            for c in candidates:
                row = dict(c)
                row["liveness"] = live_map.get(c["url"], "live")
                row["http_code"] = 200 if row["liveness"] == "live" else None
                out.append(row)
            return out

        monkeypatch.setattr(hunt, "probe_rows", fake_probe_rows)

    def test_buckets_and_report(self, dirs, monkeypatch, tmp_path):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("duprec", link="https://existing.example.com"))
        write_scheduled(scheduled, "US", "opendata", make_record("liverec", link="http://ok.example"))
        write_scheduled(scheduled, "US", "opendata", make_record("deadrec", link="http://dead.example"))
        write_scheduled(scheduled, "Unknown", "opendata", make_record("dakarrec", link="https://dakar.example.com", country="Unknown"))
        self._patch_exports_and_probe(monkeypatch, {"http://ok.example": "live", "http://dead.example": "dead", "https://dakar.example.com": "live"})

        rows = ps.review_queue(probe=True, scheduled_dir=scheduled)
        by_id = {r["id"]: r for r in rows}
        assert by_id["duprec"]["bucket"] == "duplicate"
        assert by_id["duprec"]["existing_id"] == "existingrec"
        assert by_id["liverec"]["bucket"] == "promote-ready"
        assert by_id["deadrec"]["bucket"] == "dead"
        # Unknown path inferred via hints
        assert by_id["dakarrec"]["country"] == "SN"
        assert by_id["dakarrec"]["bucket"] == "promote-ready"
        # nothing moved
        assert (scheduled / "US" / "opendata" / "liverec.yaml").exists()

    def test_country_filter(self, dirs, monkeypatch):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("usrec"))
        write_scheduled(scheduled, "FR", "opendata", make_record("frrec"))
        self._patch_exports_and_probe(monkeypatch, {})
        rows = ps.review_queue(probe=False, country="FR", scheduled_dir=scheduled)
        assert [r["id"] for r in rows] == ["frrec"]

    def test_no_probe_marks_promote_ready(self, dirs, monkeypatch):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("reca"))
        self._patch_exports_and_probe(monkeypatch, {})
        rows = ps.review_queue(probe=False, scheduled_dir=scheduled)
        assert rows[0]["bucket"] == "promote-ready"
        assert "liveness" not in rows[0]

    def test_cli_writes_jsonl(self, dirs, monkeypatch, tmp_path):
        scheduled, entities = dirs
        write_scheduled(scheduled, "US", "opendata", make_record("reca"))
        self._patch_exports_and_probe(monkeypatch, {})
        monkeypatch.setattr(ps, "SCHEDULED_DIR", scheduled)
        out = tmp_path / "report.jsonl"
        result = runner.invoke(ps.app, ["review-scheduled", "--no-probe", "--out", str(out)])
        assert result.exit_code == 0
        import json

        report = [json.loads(line) for line in out.read_text().splitlines()]
        assert report[0]["id"] == "reca"
        assert "promote-ready: 1" in result.output
