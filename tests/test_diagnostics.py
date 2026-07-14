from __future__ import annotations

import unittest

from python_doctor.diagnostics import (
    AnalyzerCoverage,
    Diagnostic,
    FixSafety,
    RuleMaturity,
    ScanReport,
    ScanStatus,
    Severity,
    SourceSpan,
)


class DiagnosticTests(unittest.TestCase):
    def test_diagnostic_serializes_with_stable_field_names(self) -> None:
        diagnostic = Diagnostic(
            fingerprint="abc123",
            analyzer="python-doctor",
            analyzer_version="0.1.0.dev0",
            rule_id="python-doctor/safety/no-direct-recursion",
            original_rule_id="no-direct-recursion",
            title="Direct recursion",
            message="Function 'walk' calls itself.",
            rationale="Recursion prevents a static stack bound.",
            remediation="Replace recursion with a bounded iterative traversal.",
            category="Reliability",
            severity=Severity.ERROR,
            confidence=1.0,
            maturity=RuleMaturity.EXPERIMENTAL,
            path="src/worker.py",
            span=SourceSpan(3, 1, 4, 16),
            fix_safety=FixSafety.AGENT_REQUIRED,
            root_cause_group=None,
            tags=("safety-critical",),
        )
        payload = diagnostic.to_dict()
        self.assertEqual(payload["ruleId"], diagnostic.rule_id)
        self.assertEqual(payload["severity"], "error")
        self.assertEqual(payload["span"]["startLine"], 3)
        self.assertNotIn("source", payload)

    def test_partial_report_keeps_coverage_reason(self) -> None:
        report = ScanReport(
            schema_version=1,
            status=ScanStatus.PARTIAL,
            project_root="/repo",
            diagnostics=(),
            coverage=(AnalyzerCoverage("ruff", "unavailable", "executable not found"),),
            skipped_checks=("ruff",),
        )
        payload = report.to_dict()
        self.assertEqual(payload["status"], "partial")
        self.assertEqual(payload["coverage"][0]["reason"], "executable not found")

    def test_report_serializes_local_score(self) -> None:
        report = ScanReport(
            schema_version=1,
            status=ScanStatus.CLEAN,
            project_root="/repo",
            diagnostics=(),
            coverage=(),
            skipped_checks=(),
            score=100.0,
            score_label="healthy",
        )
        payload = report.to_dict()
        self.assertEqual(payload["score"], 100.0)
        self.assertEqual(payload["scoreLabel"], "healthy")


if __name__ == "__main__":
    unittest.main()
