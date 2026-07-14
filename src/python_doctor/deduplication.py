from __future__ import annotations

from typing import Dict, Iterable, Tuple

from python_doctor.diagnostics import Diagnostic, Severity


_SEVERITY_RANK = {
    Severity.INFO: 0,
    Severity.WARNING: 1,
    Severity.ERROR: 2,
}


def _selection_key(diagnostic: Diagnostic) -> Tuple[object, ...]:
    return (
        _SEVERITY_RANK[diagnostic.severity],
        diagnostic.analyzer,
        diagnostic.rule_id,
        diagnostic.path,
        diagnostic.span.start_line,
        diagnostic.span.start_column,
        diagnostic.span.end_line,
        diagnostic.span.end_column,
        diagnostic.fingerprint,
    )


def _output_key(diagnostic: Diagnostic) -> Tuple[object, ...]:
    return (
        diagnostic.path,
        diagnostic.span.start_line,
        diagnostic.span.start_column,
        diagnostic.analyzer,
        diagnostic.rule_id,
        diagnostic.fingerprint,
    )


def deduplicate_diagnostics(
    diagnostics: Iterable[Diagnostic],
) -> Tuple[Diagnostic, ...]:
    selected: Dict[str, Diagnostic] = {}
    for diagnostic in diagnostics:
        if diagnostic.root_cause_group:
            key = f"group:{diagnostic.root_cause_group}"
        else:
            key = f"finding:{diagnostic.fingerprint}"
        current = selected.get(key)
        if current is None or _selection_key(diagnostic) > _selection_key(current):
            selected[key] = diagnostic
    return tuple(sorted(selected.values(), key=_output_key))
