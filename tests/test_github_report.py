from __future__ import annotations

import unittest
from dataclasses import replace

from python_doctor.diagnostics import ScanReport, ScanStatus, Severity
from python_doctor.reports import render_github
from tests.test_deduplication import make_diagnostic


class GitHubReportTests(unittest.TestCase):
    def test_renders_annotations_with_escaped_properties_and_messages(self) -> None:
        warning = replace(
            make_diagnostic("warning", path="src/a,b.py"),
            rule_id="test:rule",
            message="100% bad\nnext line",
            severity=Severity.WARNING,
        )
        notice = replace(
            make_diagnostic("notice", severity=Severity.INFO, path="src/b.py"),
            rule_id="test/info",
        )
        report = ScanReport(
            1,
            ScanStatus.FINDINGS,
            "/repo",
            (warning, notice),
            (),
            (),
        )

        rendered = render_github(report)
        lines = rendered.splitlines()

        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("::warning "))
        self.assertIn("file=src/a%2Cb.py", lines[0])
        self.assertIn("title=test%3Arule", lines[0])
        self.assertIn("line=1,endLine=1,col=1,endColumn=2", lines[0])
        self.assertTrue(lines[0].endswith("::100%25 bad%0Anext line"))
        self.assertTrue(lines[1].startswith("::notice "))
        self.assertTrue(rendered.endswith("\n"))

    def test_empty_report_emits_plain_status_line(self) -> None:
        report = ScanReport(1, ScanStatus.CLEAN, "/repo", (), (), ())
        rendered = render_github(report)
        self.assertEqual(rendered, "Python Doctor: CLEAN (0 findings)\n")
        self.assertNotIn("::notice", rendered)


if __name__ == "__main__":
    unittest.main()
