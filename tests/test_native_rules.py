from __future__ import annotations

import unittest
from pathlib import Path

from python_doctor.rules import built_in_rules
from python_doctor.rules.base import RuleContext
from python_doctor.rules.no_direct_recursion import NoDirectRecursionRule


class NativeRuleTests(unittest.TestCase):
    def test_reports_direct_recursion(self) -> None:
        source = "def walk(value):\n    return walk(value - 1)\n"
        rule = NoDirectRecursionRule()
        findings = rule.analyze(
            Path("src/worker.py"),
            source,
            RuleContext(Path("."), "safety-critical"),
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule_id, "python-doctor/safety/no-direct-recursion")
        self.assertEqual(findings[0].span.start_line, 1)

    def test_does_not_report_call_to_different_function(self) -> None:
        source = "def walk(value):\n    return visit(value)\n"
        findings = NoDirectRecursionRule().analyze(
            Path("src/worker.py"),
            source,
            RuleContext(Path("."), "safety-critical"),
        )
        self.assertEqual(findings, ())

    def test_rule_is_only_enabled_for_safety_profile(self) -> None:
        self.assertEqual(built_in_rules("default"), ())
        self.assertEqual(len(built_in_rules("safety-critical")), 1)


if __name__ == "__main__":
    unittest.main()
