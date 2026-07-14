from __future__ import annotations

import json
from typing import Dict, List

from python_doctor import __version__
from python_doctor.diagnostics import Diagnostic, ScanReport, Severity


_LEVEL = {
    Severity.INFO: "note",
    Severity.WARNING: "warning",
    Severity.ERROR: "error",
}
_SCHEMA = (
    "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cs01/schemas/"
    "sarif-schema-2.1.0.json"
)


def _artifact_uri(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith("/") or (
        len(normalized) >= 2 and normalized[1] == ":"
    ):
        return normalized.rsplit("/", 1)[-1]
    while normalized.startswith("../"):
        normalized = normalized[3:]
    return normalized


def _rule(diagnostic: Diagnostic) -> Dict[str, object]:
    return {
        "id": diagnostic.rule_id,
        "name": diagnostic.original_rule_id,
        "shortDescription": {"text": diagnostic.title},
        "fullDescription": {"text": diagnostic.rationale},
        "help": {"text": diagnostic.remediation},
        "properties": {
            "analyzer": diagnostic.analyzer,
            "category": diagnostic.category,
            "tags": list(diagnostic.tags),
        },
    }


def _result(diagnostic: Diagnostic) -> Dict[str, object]:
    return {
        "ruleId": diagnostic.rule_id,
        "level": _LEVEL[diagnostic.severity],
        "message": {"text": diagnostic.message},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": _artifact_uri(diagnostic.path)},
                    "region": {
                        "startLine": diagnostic.span.start_line,
                        "startColumn": diagnostic.span.start_column,
                        "endLine": diagnostic.span.end_line,
                        "endColumn": diagnostic.span.end_column,
                    },
                }
            }
        ],
        "partialFingerprints": {
            "pythonDoctorFingerprint/v1": diagnostic.fingerprint
        },
        "properties": {
            "analyzer": diagnostic.analyzer,
            "category": diagnostic.category,
            "confidence": diagnostic.confidence,
            "fixSafety": diagnostic.fix_safety.value,
            "maturity": diagnostic.maturity.value,
        },
    }


def render_sarif(report: ScanReport, pretty: bool = True) -> str:
    rules_by_id: Dict[str, Diagnostic] = {}
    for diagnostic in report.diagnostics:
        rules_by_id.setdefault(diagnostic.rule_id, diagnostic)
    rules: List[Dict[str, object]] = [
        _rule(rules_by_id[rule_id]) for rule_id in sorted(rules_by_id)
    ]
    payload = {
        "$schema": _SCHEMA,
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Python Doctor",
                        "version": __version__,
                        "semanticVersion": __version__.split(".dev", 1)[0],
                        "rules": rules,
                    }
                },
                "results": [_result(item) for item in report.diagnostics],
                "properties": {
                    "scanStatus": report.status.value,
                    "coverage": [item.to_dict() for item in report.coverage],
                    "skippedChecks": list(report.skipped_checks),
                    "score": report.score,
                    "scoreLabel": report.score_label,
                },
            }
        ],
    }
    return json.dumps(
        payload,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        sort_keys=True,
    ) + "\n"
