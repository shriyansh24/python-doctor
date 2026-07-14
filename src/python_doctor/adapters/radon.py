from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

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


def _relative_path(project: ProjectInfo, filename: object) -> str:
    path = Path(str(filename))
    resolved = path.resolve() if path.is_absolute() else (project.root / path).resolve()
    try:
        return resolved.relative_to(project.root).as_posix()
    except ValueError:
        return path.as_posix()


def _blocks(items: Iterable[object]) -> Iterable[Dict[str, Any]]:
    for item in items:
        if not isinstance(item, dict):
            raise TypeError("complexity block must be an object")
        yield item
        methods = item.get("methods", [])
        if not isinstance(methods, list):
            raise TypeError("methods must be a list")
        yield from _blocks(methods)


class RadonAdapter:
    def __init__(self, executable: str = "radon") -> None:
        self.executable = executable

    def analyze(self, project: ProjectInfo) -> Tuple[Diagnostic, ...]:
        execution = run_tool(
            [self.executable, "cc", "-j", "-s", "."],
            cwd=project.root,
            timeout_seconds=120.0,
        )
        if execution.return_code != 0:
            raise ExternalToolError(execution.stderr or execution.stdout)
        try:
            payload: Dict[str, Any] = json.loads(execution.stdout or "{}")
            if not isinstance(payload, dict):
                raise TypeError("top-level value must be an object")
            findings: List[Diagnostic] = []
            for filename, raw_blocks in payload.items():
                if not isinstance(raw_blocks, list):
                    raise TypeError("file value must be a list")
                path = _relative_path(project, filename)
                for item in _blocks(raw_blocks):
                    rank = str(item["rank"]).upper()
                    if rank not in {"A", "B", "C", "D", "E", "F"}:
                        raise ValueError(f"unknown complexity rank: {rank}")
                    if rank in {"A", "B"}:
                        continue
                    name = str(item["name"])
                    complexity = int(item["complexity"])
                    message = (
                        f"{name} has cyclomatic complexity {complexity} (rank {rank})."
                    )
                    findings.append(
                        Diagnostic(
                            fingerprint=compute_fingerprint(
                                path,
                                "radon/cyclomatic-complexity",
                                name,
                                message,
                            ),
                            analyzer="radon",
                            analyzer_version="unknown",
                            rule_id="radon/cyclomatic-complexity",
                            original_rule_id="cc",
                            title="High cyclomatic complexity",
                            message=message,
                            rationale=(
                                "High branch complexity increases review, testing, and "
                                "maintenance risk."
                            ),
                            remediation=(
                                "Split independent decisions into smaller named functions "
                                "while preserving behavior."
                            ),
                            category="Maintainability",
                            severity=(
                                Severity.WARNING if rank == "C" else Severity.ERROR
                            ),
                            confidence=1.0,
                            maturity=RuleMaturity.STABLE,
                            path=path,
                            span=SourceSpan(
                                int(item["lineno"]),
                                int(item.get("col_offset", 0)) + 1,
                                int(item.get("endline", item["lineno"])),
                                int(item.get("end_col_offset", item.get("col_offset", 0)))
                                + 1,
                            ),
                            fix_safety=FixSafety.AGENT_REQUIRED,
                            root_cause_group=None,
                            tags=("radon", "complexity"),
                        )
                    )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ExternalToolError(f"invalid Radon JSON: {error}") from error
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
