from __future__ import annotations

import unittest
from typing import Optional

from python_doctor.deduplication import deduplicate_diagnostics
from python_doctor.diagnostics import (
    Diagnostic,
    FixSafety,
    RuleMaturity,
    Severity,
    SourceSpan,
)


def make_diagnostic(
    fingerprint: str,
    *,
    severity: Severity = Severity.WARNING,
    root_cause_group: Optional[str] = None,
    path: str = "src/app.py",
) -> Diagnostic:
    return Diagnostic(
        fingerprint=fingerprint,
        analyzer="test",
        analyzer_version="1.0",
        rule_id=f"test/{fingerprint}",
        original_rule_id=fingerprint,
        title="Finding",
        message="A finding",
        rationale="Test rationale",
        remediation="Test remediation",
        category="Correctness",
        severity=severity,
        confidence=1.0,
        maturity=RuleMaturity.STABLE,
        path=path,
        span=SourceSpan(1, 1, 1, 2),
        fix_safety=FixSafety.UNAVAILABLE,
        root_cause_group=root_cause_group,
        tags=(),
    )


class DeduplicationTests(unittest.TestCase):
    def test_root_cause_group_keeps_highest_severity(self) -> None:
        warning = make_diagnostic(
            "warning", severity=Severity.WARNING, root_cause_group="group-a"
        )
        error = make_diagnostic(
            "error", severity=Severity.ERROR, root_cause_group="group-a"
        )
        self.assertEqual(deduplicate_diagnostics((warning, error)), (error,))

    def test_findings_without_root_cause_group_remain_distinct(self) -> None:
        first = make_diagnostic("first")
        second = make_diagnostic("second")
        self.assertCountEqual(deduplicate_diagnostics((first, second)), (first, second))

    def test_output_order_is_deterministic(self) -> None:
        first = make_diagnostic("zeta", path="z.py")
        second = make_diagnostic("alpha", path="a.py")
        expected = deduplicate_diagnostics((first, second))
        self.assertEqual(deduplicate_diagnostics((second, first)), expected)


if __name__ == "__main__":
    unittest.main()
