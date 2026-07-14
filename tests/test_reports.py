from __future__ import annotations

import json
import unittest

from python_doctor.diagnostics import AnalyzerCoverage, ScanReport, ScanStatus
from python_doctor.reports import render_json, render_terminal


class ReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.report = ScanReport(
            schema_version=1,
            status=ScanStatus.PARTIAL,
            project_root="/repo",
            diagnostics=(),
            coverage=(AnalyzerCoverage("ruff", "unavailable", "not found"),),
            skipped_checks=("ruff",),
        )

    def test_json_is_versioned_and_newline_terminated(self) -> None:
        rendered = render_json(self.report)
        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(json.loads(rendered)["schemaVersion"], 1)

    def test_terminal_report_never_calls_partial_scan_clean(self) -> None:
        rendered = render_terminal(self.report)
        self.assertIn("PARTIAL", rendered)
        self.assertIn("ruff: unavailable", rendered)
        self.assertNotIn("No issues found", rendered)

    def test_terminal_and_json_include_local_score(self) -> None:
        report = ScanReport(
            schema_version=1,
            status=ScanStatus.CLEAN,
            project_root="/repo",
            diagnostics=(),
            coverage=(),
            skipped_checks=(),
            score=98.5,
            score_label="healthy",
        )
        self.assertIn("Score: 98.5 (healthy)", render_terminal(report))
        payload = json.loads(render_json(report))
        self.assertEqual(payload["score"], 98.5)
        self.assertEqual(payload["scoreLabel"], "healthy")


if __name__ == "__main__":
    unittest.main()
