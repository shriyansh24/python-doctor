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


class RuffAdapter:
    def __init__(self, executable: str = "ruff") -> None:
        self.executable = executable

    def analyze(self, project: ProjectInfo) -> Tuple[Diagnostic, ...]:
        execution = run_tool(
            [self.executable, "check", "--output-format", "json", "."],
            cwd=project.root,
            timeout_seconds=120.0,
        )
        if execution.return_code not in (0, 1):
            raise ExternalToolError(execution.stderr or execution.stdout)
        try:
            payload: List[Dict[str, Any]] = json.loads(execution.stdout or "[]")
        except json.JSONDecodeError as error:
            raise ExternalToolError(f"invalid Ruff JSON: {error}") from error

        findings = []
        for item in payload:
            filename = Path(str(item["filename"]))
            resolved = filename.resolve() if filename.is_absolute() else (project.root / filename).resolve()
            try:
                path = resolved.relative_to(project.root).as_posix()
            except ValueError:
                path = filename.as_posix()
            code = str(item["code"])
            message = str(item["message"])
            location = item["location"]
            end = item["end_location"]
            fix = item.get("fix")
            findings.append(
                Diagnostic(
                    fingerprint=compute_fingerprint(path, f"ruff/{code}", code, message),
                    analyzer="ruff",
                    analyzer_version="unknown",
                    rule_id=f"ruff/{code}",
                    original_rule_id=code,
                    title=code,
                    message=message,
                    rationale="Ruff reported this deterministic static-analysis finding.",
                    remediation="Apply the Ruff rule guidance and rerun the check.",
                    category="Correctness",
                    severity=Severity.WARNING,
                    confidence=1.0,
                    maturity=RuleMaturity.STABLE,
                    path=path,
                    span=SourceSpan(
                        location["row"],
                        location["column"],
                        end["row"],
                        end["column"],
                    ),
                    fix_safety=(
                        FixSafety.SAFE_AUTOMATIC
                        if fix and fix.get("applicability") == "safe"
                        else FixSafety.AGENT_REQUIRED
                    ),
                    root_cause_group=None,
                    tags=("ruff",),
                )
            )
        return tuple(findings)
