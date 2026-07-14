from __future__ import annotations

import unittest
from dataclasses import replace

from python_doctor.config import DoctorConfig
from python_doctor.diagnostics import ScanReport, ScanStatus, Severity
from python_doctor.policy import apply_policy
from tests.test_deduplication import make_diagnostic


class PolicyTests(unittest.TestCase):
    def test_applies_suppressions_precedence_and_blocking(self) -> None:
        ruff = replace(
            make_diagnostic("ruff"),
            rule_id="ruff/F401",
            category="Correctness",
        )
        bandit = replace(
            make_diagnostic("bandit"),
            rule_id="bandit/B101",
            category="Security",
        )
        ignored_file = replace(
            make_diagnostic("ignored-file", path="tests/unit.py"),
            rule_id="ruff/E501",
            category="Correctness",
        )
        category_only = replace(
            make_diagnostic("category"),
            rule_id="native/category",
            category="Correctness",
        )
        report = ScanReport(
            schema_version=1,
            status=ScanStatus.FINDINGS,
            project_root="/repo",
            diagnostics=(ruff, bandit, ignored_file, category_only),
            coverage=(),
            skipped_checks=(),
        )
        config = DoctorConfig(
            rules=(("ruff/F401", "warning"),),
            categories=(("Correctness", "error"),),
            ignore_rules=("bandit/B101",),
            ignore_files=("tests/**",),
            blocking="warning",
        )

        result = apply_policy(report, config)

        visible = {item.rule_id: item for item in result.report.diagnostics}
        self.assertEqual(visible["ruff/F401"].severity, Severity.WARNING)
        self.assertEqual(visible["native/category"].severity, Severity.ERROR)
        self.assertEqual(
            {item.fingerprint for item in result.suppressed},
            {"bandit", "ignored-file"},
        )
        self.assertEqual(
            {item.rule_id for item in result.blocking_diagnostics},
            {"ruff/F401", "native/category"},
        )

    def test_rule_off_is_a_visible_suppression_result(self) -> None:
        diagnostic = make_diagnostic("off")
        report = ScanReport(1, ScanStatus.FINDINGS, "/repo", (diagnostic,), (), ())
        config = DoctorConfig(rules=((diagnostic.rule_id, "off"),))

        result = apply_policy(report, config)

        self.assertEqual(result.report.diagnostics, ())
        self.assertEqual(result.suppressed, (diagnostic,))

    def test_blocking_none_never_blocks(self) -> None:
        diagnostic = replace(make_diagnostic("error"), severity=Severity.ERROR)
        report = ScanReport(1, ScanStatus.FINDINGS, "/repo", (diagnostic,), (), ())
        result = apply_policy(report, DoctorConfig(blocking="none"))
        self.assertEqual(result.blocking_diagnostics, ())


if __name__ == "__main__":
    unittest.main()
