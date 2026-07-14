from __future__ import annotations

import argparse
import os
import tempfile
from dataclasses import replace
from pathlib import Path
from typing import Optional, Sequence, Tuple

from python_doctor import __version__
from python_doctor.config import ConfigError, DoctorConfig, load_config
from python_doctor.deduplication import deduplicate_diagnostics
from python_doctor.diagnostics import ScanReport, ScanStatus
from python_doctor.discovery import discover_project
from python_doctor.policy import apply_policy
from python_doctor.reports import render_github, render_json, render_sarif, render_terminal
from python_doctor.scanner import ScanOptions, scan_project
from python_doctor.scoring import calculate_score


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python-doctor")
    parser.add_argument("--version", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    scan = subparsers.add_parser("scan", help="scan a Python project")
    scan.add_argument("path", nargs="?", default=".")
    scan.add_argument(
        "--format",
        choices=("terminal", "json", "sarif", "github"),
        default="terminal",
    )
    scan.add_argument("--output")
    scan.add_argument(
        "--profile",
        choices=("default", "strict", "safety-critical"),
    )
    scan.add_argument("--require-ruff", action="store_true")
    scan.add_argument("--require-bandit", action="store_true")
    scan.add_argument("--require-radon", action="store_true")
    scan.add_argument("--require-complete", action="store_true")
    scan.add_argument("--blocking", choices=("none", "warning", "error"))
    scan.add_argument("--score", action="store_true")
    scan.add_argument("--ruff-executable")
    scan.add_argument("--bandit-executable")
    scan.add_argument("--radon-executable")
    scan.add_argument(
        "--offline",
        action="store_true",
        help="prohibit every optional network operation",
    )
    return parser


def _render_report(report: ScanReport, format_name: str) -> str:
    if format_name == "json":
        return render_json(report)
    if format_name == "sarif":
        return render_sarif(report)
    if format_name == "github":
        return render_github(report)
    return render_terminal(report)


def _write_output(destination: Path, rendered: str) -> None:
    if destination.exists() and destination.is_dir():
        raise OSError(f"output path is a directory: {destination}")
    parent = destination.parent
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=str(parent),
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _load_doctor_config(root: Path) -> Optional[DoctorConfig]:
    try:
        return load_config(root)
    except (ConfigError, OSError, ValueError) as error:
        print(f"Configuration error: {error}")
        return None


def _scan_options(args: argparse.Namespace, config: DoctorConfig) -> ScanOptions:
    return ScanOptions(
        profile=args.profile or config.profile,
        require_ruff=args.require_ruff or config.adapters.ruff.required,
        require_bandit=args.require_bandit or config.adapters.bandit.required,
        require_radon=args.require_radon or config.adapters.radon.required,
        enable_ruff=config.adapters.ruff.enabled or args.require_ruff,
        enable_bandit=config.adapters.bandit.enabled or args.require_bandit,
        enable_radon=config.adapters.radon.enabled or args.require_radon,
        ruff_executable=args.ruff_executable or config.adapters.ruff.executable,
        bandit_executable=args.bandit_executable or config.adapters.bandit.executable,
        radon_executable=args.radon_executable or config.adapters.radon.executable,
    )


def _evaluate_report(
    root: Path,
    report: ScanReport,
    config: DoctorConfig,
    args: argparse.Namespace,
) -> Tuple[ScanReport, DoctorConfig, bool]:
    report = replace(report, diagnostics=deduplicate_diagnostics(report.diagnostics))
    effective_config = replace(
        config,
        blocking=args.blocking or config.blocking,
        require_complete=args.require_complete or config.require_complete,
    )
    policy_result = apply_policy(report, effective_config)
    score_result = calculate_score(
        policy_result.report.diagnostics,
        source_file_count=len(discover_project(root).python_files),
    )
    report = replace(
        policy_result.report,
        score=score_result.score,
        score_label=score_result.label,
    )
    return report, effective_config, bool(policy_result.blocking_diagnostics)


def _deliver_report(report: ScanReport, args: argparse.Namespace) -> bool:
    if args.score:
        print(report.score)
        return True
    rendered = _render_report(report, args.format)
    if not args.output:
        print(rendered.rstrip("\n"))
        return True
    try:
        _write_output(Path(args.output).expanduser().resolve(), rendered)
        return True
    except OSError as error:
        print(f"Output error: {error}")
        return False


def _scan_exit_code(
    report: ScanReport, config: DoctorConfig, has_blocking: bool
) -> int:
    if report.status is ScanStatus.FAILED:
        return 3
    if config.require_complete and report.status is ScanStatus.PARTIAL:
        return 4
    if has_blocking:
        return 1
    return 0


def _scan(args: argparse.Namespace) -> int:
    if args.score and args.output:
        print("Usage error: --score and --output cannot be used together")
        return 2
    root = Path(args.path).expanduser().resolve()
    config = _load_doctor_config(root)
    if config is None:
        return 2
    raw_report = scan_project(root, _scan_options(args, config))
    report, effective_config, has_blocking = _evaluate_report(
        root, raw_report, config, args
    )
    if not _deliver_report(report, args):
        return 2
    return _scan_exit_code(report, effective_config, has_blocking)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(f"python-doctor {__version__}")
        return 0
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "scan":
        return _scan(args)
    return 2


def entrypoint() -> None:
    raise SystemExit(main())
