from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class RuleMaturity(str, Enum):
    EXPERIMENTAL = "experimental"
    STABLE = "stable"


class FixSafety(str, Enum):
    UNAVAILABLE = "unavailable"
    AGENT_REQUIRED = "agent-required"
    SAFE_AUTOMATIC = "safe-automatic"


class ScanStatus(str, Enum):
    CLEAN = "clean"
    FINDINGS = "findings"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"


@dataclass(frozen=True)
class SourceSpan:
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "startLine": self.start_line,
            "startColumn": self.start_column,
            "endLine": self.end_line,
            "endColumn": self.end_column,
        }


@dataclass(frozen=True)
class Diagnostic:
    fingerprint: str
    analyzer: str
    analyzer_version: str
    rule_id: str
    original_rule_id: str
    title: str
    message: str
    rationale: str
    remediation: str
    category: str
    severity: Severity
    confidence: float
    maturity: RuleMaturity
    path: str
    span: SourceSpan
    fix_safety: FixSafety
    root_cause_group: Optional[str]
    tags: Tuple[str, ...]

    def to_dict(self) -> Dict[str, object]:
        return {
            "fingerprint": self.fingerprint,
            "analyzer": self.analyzer,
            "analyzerVersion": self.analyzer_version,
            "ruleId": self.rule_id,
            "originalRuleId": self.original_rule_id,
            "title": self.title,
            "message": self.message,
            "rationale": self.rationale,
            "remediation": self.remediation,
            "category": self.category,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "maturity": self.maturity.value,
            "path": self.path,
            "span": self.span.to_dict(),
            "fixSafety": self.fix_safety.value,
            "rootCauseGroup": self.root_cause_group,
            "tags": list(self.tags),
        }


@dataclass(frozen=True)
class AnalyzerCoverage:
    analyzer: str
    status: str
    reason: Optional[str]

    def to_dict(self) -> Dict[str, object]:
        return {"analyzer": self.analyzer, "status": self.status, "reason": self.reason}


@dataclass(frozen=True)
class ScanReport:
    schema_version: int
    status: ScanStatus
    project_root: str
    diagnostics: Tuple[Diagnostic, ...]
    coverage: Tuple[AnalyzerCoverage, ...]
    skipped_checks: Tuple[str, ...]
    score: Optional[float] = None
    score_label: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "schemaVersion": self.schema_version,
            "status": self.status.value,
            "projectRoot": self.project_root,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "coverage": [item.to_dict() for item in self.coverage],
            "skippedChecks": list(self.skipped_checks),
            "score": self.score,
            "scoreLabel": self.score_label,
        }
