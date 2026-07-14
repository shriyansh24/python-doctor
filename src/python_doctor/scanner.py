from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from python_doctor.adapters.base import ExternalToolError
from python_doctor.adapters.bandit import BanditAdapter
from python_doctor.adapters.radon import RadonAdapter
from python_doctor.adapters.ruff import RuffAdapter
from python_doctor.diagnostics import AnalyzerCoverage, Diagnostic, ScanReport, ScanStatus
from python_doctor.discovery import discover_project
from python_doctor.rules import built_in_rules
from python_doctor.rules.base import RuleContext


@dataclass(frozen=True)
class ScanOptions:
    profile: str = "default"
    require_ruff: bool = False
    require_bandit: bool = False
    require_radon: bool = False
    enable_ruff: bool = True
    enable_bandit: bool = True
    enable_radon: bool = True
    ruff_executable: str = "ruff"
    bandit_executable: str = "bandit"
    radon_executable: str = "radon"


def _run_adapter(
    name: str,
    adapter: object,
    project: object,
    required: bool,
    enabled: bool,
    diagnostics: List[Diagnostic],
    coverage: list,
    skipped: list,
) -> bool:
    if not enabled:
        skipped.append(name)
        coverage.append(
            AnalyzerCoverage(name, "skipped", "disabled by configuration")
        )
        return required
    try:
        diagnostics.extend(adapter.analyze(project))  # type: ignore[attr-defined]
        coverage.append(AnalyzerCoverage(name, "complete", None))
        return False
    except ExternalToolError as error:
        skipped.append(name)
        coverage.append(AnalyzerCoverage(name, "unavailable", str(error)))
        return required


def scan_project(path: Path, options: ScanOptions) -> ScanReport:
    project = discover_project(path)
    if not project.python_files:
        return ScanReport(
            schema_version=1,
            status=ScanStatus.UNSUPPORTED,
            project_root=str(project.root),
            diagnostics=(),
            coverage=(
                AnalyzerCoverage(
                    "python-doctor",
                    "unsupported",
                    "no Python source files",
                ),
                AnalyzerCoverage("ruff", "skipped", "no Python source files"),
                AnalyzerCoverage("bandit", "skipped", "no Python source files"),
                AnalyzerCoverage("radon", "skipped", "no Python source files"),
            ),
            skipped_checks=("python-doctor/native", "ruff", "bandit", "radon"),
        )

    diagnostics: List[Diagnostic] = []
    coverage = []
    skipped = []
    native_errors = []
    for source_path in project.python_files:
        relative = source_path.relative_to(project.root)
        try:
            source = source_path.read_text(encoding="utf-8")
            for rule in built_in_rules(options.profile):
                diagnostics.extend(
                    rule.analyze(
                        relative,
                        source,
                        RuleContext(project.root, options.profile),
                    )
                )
        except (SyntaxError, UnicodeDecodeError) as error:
            native_errors.append(f"{relative.as_posix()}: {error}")

    if native_errors:
        skipped.append("python-doctor/native")
        coverage.append(
            AnalyzerCoverage("python-doctor", "partial", "; ".join(native_errors))
        )
    else:
        coverage.append(AnalyzerCoverage("python-doctor", "complete", None))

    required_adapter_failed = False
    adapter_specs = (
        (
            "ruff",
            RuffAdapter(options.ruff_executable),
            options.require_ruff,
            options.enable_ruff,
        ),
        (
            "bandit",
            BanditAdapter(options.bandit_executable),
            options.require_bandit,
            options.enable_bandit,
        ),
        (
            "radon",
            RadonAdapter(options.radon_executable),
            options.require_radon,
            options.enable_radon,
        ),
    )
    for name, adapter, required, enabled in adapter_specs:
        required_adapter_failed = (
            _run_adapter(
                name,
                adapter,
                project,
                required,
                enabled,
                diagnostics,
                coverage,
                skipped,
            )
            or required_adapter_failed
        )

    diagnostics.sort(
        key=lambda item: (
            item.path,
            item.span.start_line,
            item.span.start_column,
            item.rule_id,
            item.fingerprint,
        )
    )
    if required_adapter_failed:
        status = ScanStatus.FAILED
    elif skipped:
        status = ScanStatus.PARTIAL
    elif diagnostics:
        status = ScanStatus.FINDINGS
    else:
        status = ScanStatus.CLEAN
    return ScanReport(
        schema_version=1,
        status=status,
        project_root=str(project.root),
        diagnostics=tuple(diagnostics),
        coverage=tuple(coverage),
        skipped_checks=tuple(skipped),
    )
