from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from python_doctor.deduplication import deduplicate_diagnostics
from python_doctor.diagnostics import Diagnostic, Severity


_SEVERITY_WEIGHT = {
    Severity.INFO: 1.0,
    Severity.WARNING: 4.0,
    Severity.ERROR: 12.0,
}
_CATEGORY_MULTIPLIER = {
    "Security": 1.25,
    "Reliability": 1.15,
    "Correctness": 1.10,
}
_PER_RULE_CAP = 24.0


@dataclass(frozen=True)
class RuleDeduction:
    rule_id: str
    deduction: float


@dataclass(frozen=True)
class ScoreResult:
    score: float
    label: str
    deductions: Tuple[RuleDeduction, ...]


def _score_label(score: float) -> str:
    if score >= 90.0:
        return "healthy"
    if score >= 75.0:
        return "attention"
    if score >= 50.0:
        return "risky"
    return "critical"


def calculate_score(
    diagnostics: Iterable[Diagnostic], source_file_count: int
) -> ScoreResult:
    by_rule: Dict[str, float] = {}
    for diagnostic in deduplicate_diagnostics(diagnostics):
        confidence = min(1.0, max(0.0, diagnostic.confidence))
        raw = (
            _SEVERITY_WEIGHT[diagnostic.severity]
            * confidence
            * _CATEGORY_MULTIPLIER.get(diagnostic.category, 1.0)
        )
        by_rule[diagnostic.rule_id] = by_rule.get(diagnostic.rule_id, 0.0) + raw

    deductions: List[RuleDeduction] = []
    for rule_id in sorted(by_rule):
        deductions.append(
            RuleDeduction(rule_id, round(min(_PER_RULE_CAP, by_rule[rule_id]), 4))
        )
    project_scale = max(1.0, math.sqrt(max(source_file_count, 1) / 10.0))
    score = round(
        max(0.0, 100.0 - sum(item.deduction for item in deductions) / project_scale),
        1,
    )
    return ScoreResult(score, _score_label(score), tuple(deductions))
