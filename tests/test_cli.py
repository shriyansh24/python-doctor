from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from python_doctor.cli import main


class CliTests(unittest.TestCase):
    def test_version_prints_public_version(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["--version"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "python-doctor 0.1.0.dev0\n")

    def test_missing_command_prints_help_and_succeeds(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main([])
        self.assertEqual(exit_code, 0)
        self.assertIn("scan", output.getvalue())

    def test_scan_json_reports_schema_and_partial_status(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--format",
                    "json",
                    "--ruff-executable",
                    "missing-ruff",
                ]
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["schemaVersion"], 1)
        self.assertEqual(payload["status"], "partial")

    def test_required_missing_ruff_returns_analyzer_exit_code(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--require-ruff",
                    "--ruff-executable",
                    "missing-ruff",
                ]
            )
        self.assertEqual(exit_code, 3)
        self.assertIn("FAILED", output.getvalue())

    def test_blocking_error_returns_findings_exit_code(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "recursive_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--profile",
                    "safety-critical",
                    "--blocking",
                    "error",
                    "--ruff-executable",
                    "missing-ruff",
                ]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("no-direct-recursion", output.getvalue())

    def test_require_complete_returns_incomplete_exit_code(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--require-complete",
                    "--ruff-executable",
                    "missing-ruff",
                ]
            )
        self.assertEqual(exit_code, 4)
        self.assertIn("PARTIAL", output.getvalue())

    def test_blocking_none_keeps_findings_advisory(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "recursive_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--profile",
                    "safety-critical",
                    "--blocking",
                    "none",
                    "--ruff-executable",
                    "missing-ruff",
                ]
            )
        self.assertEqual(exit_code, 0)
        self.assertIn("no-direct-recursion", output.getvalue())

    def test_score_prints_only_numeric_line(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--score",
                    "--ruff-executable",
                    "missing-ruff",
                ]
            )
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "100.0\n")

    def test_required_missing_bandit_returns_analyzer_exit_code(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "scan",
                    str(fixture),
                    "--require-bandit",
                    "--bandit-executable",
                    "missing-bandit",
                    "--ruff-executable",
                    "missing-ruff",
                    "--radon-executable",
                    "missing-radon",
                ]
            )
        self.assertEqual(exit_code, 3)
        self.assertIn("bandit: unavailable", output.getvalue())

    def test_disabled_adapters_are_explicitly_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            root.joinpath("python-doctor.toml").write_text(
                '[adapters.ruff]\nenabled = false\n'
                '[adapters.bandit]\nenabled = false\n'
                '[adapters.radon]\nenabled = false\n',
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["scan", str(root), "--format", "json"])
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(
            [item["reason"] for item in payload["coverage"][1:]],
            ["disabled by configuration"] * 3,
        )

    def test_cli_executable_overrides_adapter_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            fake = root / "fake-bandit"
            fake.write_text(
                "#!/usr/bin/env python3\nprint('{\"errors\": [], \"results\": []}')\n",
                encoding="utf-8",
            )
            fake.chmod(fake.stat().st_mode | 0o111)
            root.joinpath("python-doctor.toml").write_text(
                '[adapters.ruff]\nenabled = false\n'
                '[adapters.radon]\nenabled = false\n'
                '[adapters.bandit]\nexecutable = "configured-missing-bandit"\n',
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "scan",
                        str(root),
                        "--format",
                        "json",
                        "--bandit-executable",
                        str(fake),
                    ]
                )
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["coverage"][2]["status"], "complete")

    def test_scan_can_render_sarif_and_github_formats(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        sarif_output = io.StringIO()
        with redirect_stdout(sarif_output):
            sarif_exit = main(
                [
                    "scan",
                    str(fixture),
                    "--format",
                    "sarif",
                    "--ruff-executable",
                    "missing-ruff",
                    "--bandit-executable",
                    "missing-bandit",
                    "--radon-executable",
                    "missing-radon",
                ]
            )
        self.assertEqual(sarif_exit, 0)
        self.assertEqual(json.loads(sarif_output.getvalue())["version"], "2.1.0")

        github_output = io.StringIO()
        with redirect_stdout(github_output):
            github_exit = main(
                [
                    "scan",
                    str(fixture),
                    "--format",
                    "github",
                    "--ruff-executable",
                    "missing-ruff",
                    "--bandit-executable",
                    "missing-bandit",
                    "--radon-executable",
                    "missing-radon",
                ]
            )
        self.assertEqual(github_exit, 0)
        self.assertEqual(github_output.getvalue(), "Python Doctor: PARTIAL (0 findings)\n")

    def test_output_writes_report_atomically_and_silences_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            root.joinpath("python-doctor.toml").write_text(
                '[adapters.ruff]\nenabled = false\n'
                '[adapters.bandit]\nenabled = false\n'
                '[adapters.radon]\nenabled = false\n',
                encoding="utf-8",
            )
            destination = root / "reports" / "doctor.sarif"
            destination.parent.mkdir()
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "scan",
                        str(root),
                        "--format",
                        "sarif",
                        "--output",
                        str(destination),
                    ]
                )
            payload = json.loads(destination.read_text(encoding="utf-8"))
            temporary_files = tuple(destination.parent.glob(".doctor.sarif.*.tmp"))
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(payload["version"], "2.1.0")
        self.assertEqual(temporary_files, ())

    def test_score_rejects_output_file(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                ["scan", str(fixture), "--score", "--output", "score.txt"]
            )
        self.assertEqual(exit_code, 2)
        self.assertIn("cannot be used together", output.getvalue())

    def test_output_preserves_blocking_exit_code(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "recursive_project"
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "doctor.json"
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "scan",
                        str(fixture),
                        "--profile",
                        "safety-critical",
                        "--format",
                        "json",
                        "--output",
                        str(destination),
                        "--ruff-executable",
                        "missing-ruff",
                        "--bandit-executable",
                        "missing-bandit",
                        "--radon-executable",
                        "missing-radon",
                    ]
                )
            payload = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(len(payload["diagnostics"]), 1)


if __name__ == "__main__":
    unittest.main()
