from __future__ import annotations

import unittest
from dataclasses import replace

from python_doctor.diagnostics import Severity
from python_doctor.scoring import calculate_score
from tests.test_deduplication import make_diagnostic


class ScoringTests(unittest.TestCase):
    def test_no_diagnostics_is_healthy(self) -> None:
        result = calculate_score((), source_file_count=10)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.label, "healthy")
        self.assertEqual(result.deductions, ())

    def test_error_scores_lower_than_warning(self) -> None:
        warning = make_diagnostic("warning", severity=Severity.WARNING)
        error = make_diagnostic("error", severity=Severity.ERROR)
        self.assertLess(
            calculate_score((error,), 10).score,
            calculate_score((warning,), 10).score,
        )

    def test_duplicate_root_cause_groups_are_counted_once(self) -> None:
        first = make_diagnostic("first", root_cause_group="shared")
        second = make_diagnostic("second", root_cause_group="shared")
        self.assertEqual(
            calculate_score((first, second), 10).score,
            calculate_score((first,), 10).score,
        )

    def test_per_rule_deduction_is_capped_before_size_normalization(self) -> None:
        diagnostics = tuple(
            replace(make_diagnostic(f"finding-{index}"), rule_id="test/shared")
            for index in range(100)
        )
        result = calculate_score(diagnostics, source_file_count=10)
        self.assertEqual(result.score, 76.0)
        self.assertEqual(result.deductions[0].deduction, 24.0)

    def test_same_inputs_return_equal_result(self) -> None:
        diagnostics = (make_diagnostic("stable"),)
        self.assertEqual(
            calculate_score(diagnostics, source_file_count=27),
            calculate_score(diagnostics, source_file_count=27),
        )


if __name__ == "__main__":
    unittest.main()
