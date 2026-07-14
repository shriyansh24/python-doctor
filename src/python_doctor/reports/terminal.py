from __future__ import annotations

from typing import List

from python_doctor.diagnostics import ScanReport, ScanStatus


def render_terminal(report: ScanReport) -> str:
    lines: List[str] = [f"Python Doctor: {report.status.value.upper()}"]
    lines.append(f"Project: {report.project_root}")
    if report.score is not None and report.score_label is not None:
        lines.append(f"Score: {report.score:.1f} ({report.score_label})")
    lines.append(f"Findings: {len(report.diagnostics)}")
    for diagnostic in report.diagnostics:
        lines.append(
            f"{diagnostic.severity.value.upper()} {diagnostic.path}:"
            f"{diagnostic.span.start_line}:{diagnostic.span.start_column} "
            f"{diagnostic.rule_id} {diagnostic.message}"
        )
    lines.append("Coverage:")
    for item in report.coverage:
        suffix = f" ({item.reason})" if item.reason else ""
        lines.append(f"  {item.analyzer}: {item.status}{suffix}")
    if report.status is ScanStatus.CLEAN:
        lines.append("No issues found in the completed scan.")
    return "\n".join(lines) + "\n"
