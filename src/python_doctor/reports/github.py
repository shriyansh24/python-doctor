from __future__ import annotations

from typing import Dict, List

from python_doctor.diagnostics import ScanReport, Severity


_ANNOTATION_LEVEL: Dict[Severity, str] = {
    Severity.INFO: "notice",
    Severity.WARNING: "warning",
    Severity.ERROR: "error",
}


def _escape_data(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _escape_property(value: str) -> str:
    return _escape_data(value).replace(":", "%3A").replace(",", "%2C")


def _relative_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or (
        len(normalized) >= 2 and normalized[1] == ":"
    ):
        return normalized.rsplit("/", 1)[-1]
    while normalized.startswith("../"):
        normalized = normalized[3:]
    return normalized


def render_github(report: ScanReport) -> str:
    if not report.diagnostics:
        return f"Python Doctor: {report.status.value.upper()} (0 findings)\n"
    lines: List[str] = []
    for diagnostic in report.diagnostics:
        metadata = ",".join(
            (
                f"file={_escape_property(_relative_path(diagnostic.path))}",
                f"line={diagnostic.span.start_line}",
                f"endLine={diagnostic.span.end_line}",
                f"col={diagnostic.span.start_column}",
                f"endColumn={diagnostic.span.end_column}",
                f"title={_escape_property(diagnostic.rule_id)}",
            )
        )
        lines.append(
            f"::{_ANNOTATION_LEVEL[diagnostic.severity]} {metadata}::"
            f"{_escape_data(diagnostic.message)}"
        )
    return "\n".join(lines) + "\n"
