from __future__ import annotations

import json
import unittest
from dataclasses import replace

from python_doctor.diagnostics import AnalyzerCoverage, ScanReport, ScanStatus, Severity
from python_doctor.reports import render_sarif
from tests.test_deduplication import make_diagnostic


class SarifReportTests(unittest.TestCase):
    def test_renders_versioned_normalized_sarif_without_source(self) -> None:
        warning = replace(
            make_diagnostic("warning", path="src/app.py"),
            rule_id="ruff/F401",
            original_rule_id="F401",
            title="Unused import",
            message="Unused import detected.",
            severity=Severity.WARNING,
        )
        duplicate_rule = replace(
            warning,
            fingerprint="warning-2",
            path="src/other.py",
        )
        error = replace(
            make_diagnostic("error", severity=Severity.ERROR, path="src/security.py"),
            rule_id="bandit/B101",
            original_rule_id="B101",
            title="Assert used",
            message="Use of assert detected.",
            category="Security",
        )
        report = ScanReport(
            schema_version=1,
            status=ScanStatus.FINDINGS,
            project_root="/private/repo",
            diagnostics=(warning, duplicate_rule, error),
            coverage=(AnalyzerCoverage("ruff", "complete", None),),
            skipped_checks=(),
            score=82.5,
            score_label="attention",
        )

        rendered = render_sarif(report)
        payload = json.loads(rendered)

        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(payload["version"], "2.1.0")
        self.assertIn("sarif-schema-2.1.0", payload["$schema"])
        run = payload["runs"][0]
        self.assertEqual(run["tool"]["driver"]["name"], "Python Doctor")
        self.assertEqual(
            [rule["id"] for rule in run["tool"]["driver"]["rules"]],
            ["bandit/B101", "ruff/F401"],
        )
        self.assertEqual(
            [result["level"] for result in run["results"]],
            ["warning", "warning", "error"],
        )
        self.assertEqual(
            run["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"],
            "src/app.py",
        )
        self.assertEqual(
            run["results"][0]["partialFingerprints"]["pythonDoctorFingerprint/v1"],
            "warning",
        )
        self.assertEqual(run["properties"]["score"], 82.5)
        self.assertEqual(run["properties"]["coverage"][0]["status"], "complete")
        self.assertNotIn("/private/repo", rendered)
        self.assertNotIn("artifactContent", rendered)
        self.assertNotIn("source", rendered.lower())


if __name__ == "__main__":
    unittest.main()
