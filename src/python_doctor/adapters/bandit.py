from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from python_doctor.adapters.base import ExternalToolError, run_tool
from python_doctor.diagnostics import (
    Diagnostic,
    FixSafety,
    RuleMaturity,
    Severity,
    SourceSpan,
)
from python_doctor.discovery import ProjectInfo
from python_doctor.fingerprints import compute_fingerprint


_SEVERITY = {
    "LOW": Severity.INFO,
    "MEDIUM": Severity.WARNING,
    "HIGH": Severity.ERROR,
}
_CONFIDENCE = {"LOW": 0.5, "MEDIUM": 0.8, "HIGH": 1.0}


def _relative_path(project: ProjectInfo, filename: object) -> str:
    path = Path(str(filename))
    resolved = path.resolve() if path.is_absolute() else (project.root / path).resolve()
    try:
        return resolved.relative_to(project.root).as_posix()
    except ValueError:
        return path.as_posix()


class BanditAdapter:
    def __init__(self, executable: str = "bandit") -> None:
        self.executable = executable

    def analyze(self, project: ProjectInfo) -> Tuple[Diagnostic, ...]:
        execution = run_tool(
            [self.executable, "-r", ".", "-f", "json", "-q"],
            cwd=project.root,
            timeout_seconds=120.0,
        )
        if execution.return_code not in (0, 1):
            raise ExternalToolError(execution.stderr or execution.stdout)
        try:
            payload: Dict[str, Any] = json.loads(execution.stdout or "{}")
            results = payload["results"]
            errors = payload["errors"]
            if not isinstance(results, list) or not isinstance(errors, list):
                raise TypeError("results and errors must be lists")
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ExternalToolError(f"invalid Bandit JSON: {error}") from error
        if errors:
            details = "; ".join(
                f"{item.get('filename', 'unknown')}: {item.get('reason', 'unknown error')}"
                if isinstance(item, dict)
                else str(item)
                for item in errors
            )
            raise ExternalToolError(f"Bandit could not analyze files: {details}")

        findings: List[Diagnostic] = []
        try:
            for item in results:
                if not isinstance(item, dict):
                    raise TypeError("result must be an object")
                test_id = str(item["test_id"])
                message = str(item["issue_text"])
                path = _relative_path(project, item["filename"])
                line_range = item.get("line_range") or [item["line_number"]]
                start_line = int(item["line_number"])
                end_line = max(int(line) for line in line_range)
                severity = _SEVERITY[str(item["issue_severity"]).upper()]
                confidence = _CONFIDENCE[str(item["issue_confidence"]).upper()]
                test_name = str(item.get("test_name") or test_id)
                cwe = item.get("issue_cwe")
                cwe_id = cwe.get("id") if isinstance(cwe, dict) else None
                rationale = "Bandit reported a deterministic security finding."
                if cwe_id is not None:
                    rationale += f" Associated CWE: {cwe_id}."
                more_info = item.get("more_info")
                remediation = "Review the Bandit rule guidance and remove the unsafe pattern."
                if more_info:
                    remediation += f" Guidance: {more_info}"
                findings.append(
                    Diagnostic(
                        fingerprint=compute_fingerprint(
                            path, f"bandit/{test_id}", test_id, message
                        ),
                        analyzer="bandit",
                        analyzer_version="unknown",
                        rule_id=f"bandit/{test_id}",
                        original_rule_id=test_id,
                        title=test_name,
                        message=message,
                        rationale=rationale,
                        remediation=remediation,
                        category="Security",
                        severity=severity,
                        confidence=confidence,
                        maturity=RuleMaturity.STABLE,
                        path=path,
                        span=SourceSpan(
                            start_line,
                            int(item.get("col_offset", 0)) + 1,
                            end_line,
                            int(item.get("end_col_offset", 0)) + 1,
                        ),
                        fix_safety=FixSafety.AGENT_REQUIRED,
                        root_cause_group=None,
                        tags=("bandit", "security"),
                    )
                )
        except (KeyError, TypeError, ValueError) as error:
            raise ExternalToolError(f"invalid Bandit JSON: {error}") from error
        findings.sort(
            key=lambda item: (
                item.path,
                item.span.start_line,
                item.span.start_column,
                item.rule_id,
                item.fingerprint,
            )
        )
        return tuple(findings)
