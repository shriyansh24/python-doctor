from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from python_doctor.adapters.base import ExternalToolError
from python_doctor.diagnostics import ScanStatus
from python_doctor.scanner import ScanOptions, scan_project
from tests.test_deduplication import make_diagnostic


FIXTURES = Path(__file__).parent / "fixtures"


class ScannerTests(unittest.TestCase):
    def test_safety_profile_finds_direct_recursion_without_ruff(self) -> None:
        report = scan_project(
            FIXTURES / "recursive_project",
            ScanOptions(
                profile="safety-critical",
                require_ruff=False,
                ruff_executable="missing-ruff",
                bandit_executable="missing-bandit",
                radon_executable="missing-radon",
            ),
        )
        self.assertEqual(report.status, ScanStatus.PARTIAL)
        self.assertEqual(len(report.diagnostics), 1)
        self.assertEqual(
            report.diagnostics[0].rule_id,
            "python-doctor/safety/no-direct-recursion",
        )
        self.assertEqual(report.coverage[1].status, "unavailable")

    def test_required_missing_ruff_marks_failed_coverage(self) -> None:
        report = scan_project(
            FIXTURES / "clean_project",
            ScanOptions(
                profile="default",
                require_ruff=True,
                ruff_executable="missing-ruff",
                bandit_executable="missing-bandit",
                radon_executable="missing-radon",
            ),
        )
        self.assertEqual(report.status, ScanStatus.FAILED)
        self.assertIn("ruff", report.skipped_checks)

    def test_syntax_error_marks_native_coverage_partial_instead_of_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("broken.py").write_text("def broken(:\n", encoding="utf-8")
            report = scan_project(
                root,
                ScanOptions(
                    profile="safety-critical",
                    require_ruff=False,
                    ruff_executable="missing-ruff",
                    bandit_executable="missing-bandit",
                    radon_executable="missing-radon",
                ),
            )
        self.assertEqual(report.status, ScanStatus.PARTIAL)
        self.assertEqual(report.coverage[0].status, "partial")
        self.assertIn("python-doctor/native", report.skipped_checks)

    def test_directory_without_python_sources_is_unsupported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = scan_project(
                Path(directory),
                ScanOptions(
                    ruff_executable="missing-ruff",
                    bandit_executable="missing-bandit",
                    radon_executable="missing-radon",
                ),
            )
        self.assertEqual(report.status, ScanStatus.UNSUPPORTED)
        self.assertEqual(report.diagnostics, ())
        self.assertIn("no Python source files", report.coverage[0].reason or "")

    def test_aggregates_all_release_analyzers_in_fixed_coverage_order(self) -> None:
        class CompleteAdapter:
            def __init__(self, executable: str) -> None:
                self.executable = executable

            def analyze(self, project: object) -> tuple:
                return (
                    replace(
                        make_diagnostic(self.executable),
                        analyzer=self.executable,
                        rule_id=f"{self.executable}/rule",
                    ),
                )

        with patch("python_doctor.scanner.RuffAdapter", CompleteAdapter), patch(
            "python_doctor.scanner.BanditAdapter", CompleteAdapter
        ), patch("python_doctor.scanner.RadonAdapter", CompleteAdapter):
            report = scan_project(
                FIXTURES / "clean_project",
                ScanOptions(
                    ruff_executable="ruff",
                    bandit_executable="bandit",
                    radon_executable="radon",
                ),
            )

        self.assertEqual(report.status, ScanStatus.FINDINGS)
        self.assertEqual(
            [item.analyzer for item in report.coverage],
            ["python-doctor", "ruff", "bandit", "radon"],
        )
        self.assertTrue(all(item.status == "complete" for item in report.coverage))
        self.assertEqual(
            {item.analyzer for item in report.diagnostics},
            {"ruff", "bandit", "radon"},
        )

    def test_one_failure_does_not_prevent_later_adapter(self) -> None:
        calls = []

        class CompleteAdapter:
            def __init__(self, executable: str) -> None:
                self.executable = executable

            def analyze(self, project: object) -> tuple:
                calls.append(self.executable)
                return ()

        class FailingAdapter(CompleteAdapter):
            def analyze(self, project: object) -> tuple:
                calls.append(self.executable)
                raise ExternalToolError("adapter unavailable")

        with patch("python_doctor.scanner.RuffAdapter", CompleteAdapter), patch(
            "python_doctor.scanner.BanditAdapter", FailingAdapter
        ), patch("python_doctor.scanner.RadonAdapter", CompleteAdapter):
            report = scan_project(
                FIXTURES / "clean_project",
                ScanOptions(
                    ruff_executable="ruff",
                    bandit_executable="bandit",
                    radon_executable="radon",
                ),
            )

        self.assertEqual(calls, ["ruff", "bandit", "radon"])
        self.assertEqual(report.status, ScanStatus.PARTIAL)
        self.assertEqual(report.coverage[2].status, "unavailable")
        self.assertEqual(report.coverage[3].status, "complete")

    def test_required_missing_radon_marks_failed_coverage(self) -> None:
        report = scan_project(
            FIXTURES / "clean_project",
            ScanOptions(
                ruff_executable="missing-ruff",
                bandit_executable="missing-bandit",
                radon_executable="missing-radon",
                require_radon=True,
            ),
        )
        self.assertEqual(report.status, ScanStatus.FAILED)
        self.assertIn("radon", report.skipped_checks)


if __name__ == "__main__":
    unittest.main()
