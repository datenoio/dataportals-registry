"""UID uniqueness: duplicate-uid detection and the validate-yaml exit code."""

from pathlib import Path

from typer.testing import CliRunner

REPO_ROOT = Path(__file__).parent.parent

import builder  # noqa: E402

runner = CliRunner()


def _write(path: Path, uid: str, rid: str = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    rid = rid or path.stem
    path.write_text(f"id: {rid}\nname: {rid}\nuid: {uid}\n", encoding="utf8")
    return path


class TestFindDuplicateUids:
    def test_reports_shared_uid(self, tmp_path):
        a = _write(tmp_path / "CN" / "geo" / "a.yaml", "cdi00000001")
        b = _write(tmp_path / "JP" / "geo" / "b.yaml", "cdi00000001")
        _write(tmp_path / "JP" / "geo" / "c.yaml", "cdi00000002")
        dups = builder._find_duplicate_uids([str(tmp_path)])
        assert set(dups) == {"cdi00000001"}
        assert sorted(dups["cdi00000001"]) == sorted([str(a), str(b)])

    def test_quoted_uid_matches_plain(self, tmp_path):
        _write(tmp_path / "a.yaml", "cdi00000001")
        _write(tmp_path / "b.yaml", "'cdi00000001'")
        assert "cdi00000001" in builder._find_duplicate_uids([str(tmp_path)])

    def test_nested_uid_keys_are_ignored(self, tmp_path):
        _write(tmp_path / "a.yaml", "cdi00000001")
        (tmp_path / "b.yaml").write_text(
            "id: b\nuid: cdi00000002\nowner:\n  uid: cdi00000001\n", encoding="utf8"
        )
        assert builder._find_duplicate_uids([str(tmp_path)]) == {}

    def test_errors_for_subset_check_against_tree(self, tmp_path):
        tree = tmp_path / "entities"
        _write(tree / "a.yaml", "cdi00000001")
        new = _write(tmp_path / "incoming" / "new.yaml", "cdi00000001")
        ok = _write(tmp_path / "incoming" / "ok.yaml", "cdi00000009")
        errors = builder._duplicate_uid_errors([str(new), str(ok)], [str(tree)])
        assert [e[0] for e in errors] == [str(new)]
        assert "duplicate uid cdi00000001" in errors[0][1]


class TestRegistryData:
    def test_no_duplicate_uids_in_registry(self):
        dups = builder._find_duplicate_uids([builder.ROOT_DIR, builder.SCHEDULED_DIR])
        sample = {
            uid: [str(Path(p).relative_to(REPO_ROOT)) for p in paths]
            for uid, paths in list(sorted(dups.items()))[:10]
        }
        assert not dups, f"{len(dups)} duplicate uid(s), e.g. {sample}"


class TestValidateYamlExitCode:
    def test_invalid_file_exits_1(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("id: bad\nname: bad\n", encoding="utf8")
        result = runner.invoke(builder.app, ["validate-yaml", "--file", str(bad)])
        assert result.exit_code == 1

    def test_duplicate_uid_file_exits_1(self, tmp_path):
        existing = next(Path(builder.ROOT_DIR).rglob("*.yaml"))
        uid = builder._read_uid_value(str(existing))
        clone = tmp_path / "clone.yaml"
        clone.write_text(existing.read_text(encoding="utf8"), encoding="utf8")
        result = runner.invoke(builder.app, ["validate-yaml", "--file", str(clone)])
        assert result.exit_code == 1
        assert uid
