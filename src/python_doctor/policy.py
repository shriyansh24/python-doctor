from __future__ import annotations

import fnmatch
from dataclasses import dataclass, replace
from typing import Dict, List, Tuple

from python_doctor.config import DoctorConfig
from python_doctor.diagnostics import Diagnostic, ScanReport, Severity


_SEVERITY_RANK = {
    Severity.INFO: 0,
    Severity.WARNING: 1,
    Severity.ERROR: 2,
}


@dataclass(frozen=True)
class PolicyResult:
    report: ScanReport
    suppressed: Tuple[Diagnostic, ...]
    blocking_diagnostics: Tuple[Diagnostic, ...]


def _matches_ignored_file(path: str, patterns: Tuple[str, ...]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in patterns)


def _is_blocking(severity: Severity, blocking: str) -> bool:
    if blocking == "none":
        return False
    threshold = Severity.WARNING if blocking == "warning" else Severity.ERROR
    return _SEVERITY_RANK[severity] >= _SEVERITY_RANK[threshold]


def apply_policy(report: ScanReport, config: DoctorConfig) -> PolicyResult:
    rule_policy: Dict[str, str] = dict(config.rules)
    category_policy: Dict[str, str] = dict(config.categories)
    ignored_rules = set(config.ignore_rules)
    visible: List[Diagnostic] = []
    suppressed: List[Diagnostic] = []

    for diagnostic in report.diagnostics:
        if diagnostic.rule_id in ignored_rules or _matches_ignored_file(
            diagnostic.path, config.ignore_files
        ):
            suppressed.append(diagnostic)
            continue

        severity_name = category_policy.get(diagnostic.category)
        severity_name = rule_policy.get(diagnostic.rule_id, severity_name)
        if severity_name == "off":
            suppressed.append(diagnostic)
            continue
        if severity_name is not None:
            diagnostic = replace(diagnostic, severity=Severity(severity_name))
        visible.append(diagnostic)

    visible_tuple = tuple(visible)
    return PolicyResult(
        report=replace(report, diagnostics=visible_tuple),
        suppressed=tuple(suppressed),
        blocking_diagnostics=tuple(
            item for item in visible_tuple if _is_blocking(item.severity, config.blocking)
        ),
    )
