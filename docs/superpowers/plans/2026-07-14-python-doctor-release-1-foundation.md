# Python Doctor Release 1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable Python Doctor vertical slice: discover a Python project, run deterministic native and Ruff-compatible checks, normalize diagnostics, and emit terminal or versioned JSON reports without any network access.

**Architecture:** A dependency-light Python package exposes an `argparse` CLI over focused core modules. Project discovery produces immutable project metadata; native rules and external adapters both emit the same diagnostic contract; a scan service owns orchestration and coverage reporting. Contract tests use a fake Ruff executable so the foundation can be built and verified without downloading tools.

**Tech Stack:** Python 3.9+, standard library (`argparse`, `ast`, `dataclasses`, `enum`, `hashlib`, `json`, `pathlib`, `subprocess`, `tomllib`/`tomli`), setuptools build backend, `unittest`, Ruff JSON compatibility.

## Global Constraints

- Support Python 3.9 and newer; use `from __future__ import annotations` and avoid syntax introduced after 3.9.
- License all original source under Apache-2.0.
- Never implement telemetry or transmit analytics, crashes, repository metadata, diagnostics, source, or scores.
- Make ordinary and `--offline` scans perform zero network requests.
- Keep scoring local; scoring is deferred to the policy/scoring plan.
- Treat false positives as detector defects and preserve regression fixtures.
- Keep every diagnostic deterministic and machine-readable.
- Apply no source edits in this foundation slice.
- Respect existing project configuration; never rewrite it implicitly.
- Develop test-first and commit after every task.

## Release 1 Plan Decomposition

This is plan 1 of 6 approved Release 1 execution plans:

1. Foundation scan vertical slice - this document.
2. Analyzer coverage, policy, profiles, suppressions, deduplication, and scoring.
3. Git scopes, stable baselines, JSON schema, SARIF, and GitHub Actions.
4. Safe-fix transactions and validation.
5. Companion Codex skill and installation flow.
6. Real-repository evaluation, performance, packaging, and release hardening.

Each later plan starts only after the preceding slice is green and committed.

## File Map

Create the product repository at `/workspace/python-doctor` during execution.

```text
python-doctor/
├── pyproject.toml                       # package metadata and console entry point
├── src/python_doctor/
│   ├── __init__.py                      # public version
│   ├── __main__.py                      # `python -m python_doctor`
│   ├── cli.py                           # argument parsing and exit-code mapping
│   ├── config.py                        # TOML configuration loading and validation
│   ├── diagnostics.py                   # normalized immutable diagnostic contract
│   ├── discovery.py                     # project/source/config discovery
│   ├── fingerprints.py                  # stable diagnostic identity
│   ├── scanner.py                       # scan orchestration and coverage
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py                      # external-tool process/result contracts
│   │   └── ruff.py                      # Ruff JSON adapter
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── json_report.py               # schema-versioned JSON serialization
│   │   └── terminal.py                  # deterministic human report
│   └── rules/
│       ├── __init__.py                  # built-in registry
│       ├── base.py                      # native rule protocol/context
│       └── no_direct_recursion.py       # first safety-critical native rule
└── tests/
    ├── __init__.py
    ├── fixtures/
    │   ├── clean_project/pyproject.toml
    │   ├── clean_project/src/app.py
    │   ├── recursive_project/pyproject.toml
    │   └── recursive_project/src/worker.py
    ├── test_cli.py
    ├── test_config.py
    ├── test_diagnostics.py
    ├── test_discovery.py
    ├── test_fingerprints.py
    ├── test_native_rules.py
    ├── test_ruff_adapter.py
    ├── test_scanner.py
    └── test_reports.py
```

---

### Task 1: Package shell and CLI entry point

**Files:**
- Create: `/workspace/python-doctor/pyproject.toml`
- Create: `/workspace/python-doctor/src/python_doctor/__init__.py`
- Create: `/workspace/python-doctor/src/python_doctor/__main__.py`
- Create: `/workspace/python-doctor/src/python_doctor/cli.py`
- Create: `/workspace/python-doctor/tests/__init__.py`
- Create: `/workspace/python-doctor/tests/test_cli.py`

**Interfaces:**
- Produces: `python_doctor.cli.main(argv: Sequence[str] | None = None) -> int`
- Produces: console script `python-doctor = python_doctor.cli:entrypoint`
- Produces: version constant `python_doctor.__version__`

- [ ] **Step 1: Create package metadata and the failing CLI tests**

Initialize the standalone repository before creating files:

```bash
mkdir -p /workspace/python-doctor
cd /workspace/python-doctor
git init -b main
mkdir -p src/python_doctor tests
```

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "python-doctor"
version = "0.1.0.dev0"
description = "Deterministic Python codebase health scanner"
requires-python = ">=3.9"
license = { text = "Apache-2.0" }
authors = [{ name = "Python Doctor contributors" }]
dependencies = [
  "tomli>=2.0.1; python_version < '3.11'",
]

[project.scripts]
python-doctor = "python_doctor.cli:entrypoint"

[tool.setuptools.packages.find]
where = ["src"]
```

Create `tests/__init__.py` as an empty file and `tests/test_cli.py`:

```python
from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from python_doctor.cli import main


class CliTests(unittest.TestCase):
    def test_version_prints_public_version(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["--version"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "python-doctor 0.1.0.dev0\n")

    def test_missing_command_prints_help_and_succeeds(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main([])
        self.assertEqual(exit_code, 0)
        self.assertIn("scan", output.getvalue())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
cd /workspace/python-doctor
PYTHONPATH=src python3 -m unittest tests.test_cli -v
```

Expected: import failure for `python_doctor`.

- [ ] **Step 3: Implement the minimal CLI shell**

Create `src/python_doctor/__init__.py`:

```python
from __future__ import annotations

__version__ = "0.1.0.dev0"
```

Create `src/python_doctor/cli.py`:

```python
from __future__ import annotations

import argparse
from typing import Sequence

from python_doctor import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python-doctor")
    parser.add_argument("--version", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    scan = subparsers.add_parser("scan", help="scan a Python project")
    scan.add_argument("path", nargs="?", default=".")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(f"python-doctor {__version__}")
        return 0
    if args.command is None:
        parser.print_help()
    return 0


def entrypoint() -> None:
    raise SystemExit(main())
```

Create `src/python_doctor/__main__.py`:

```python
from python_doctor.cli import entrypoint


if __name__ == "__main__":
    entrypoint()
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run:

```bash
PYTHONPATH=src python3 -m unittest tests.test_cli -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Commit the package shell**

```bash
git add pyproject.toml src/python_doctor tests/__init__.py tests/test_cli.py
git commit -m "feat: scaffold python doctor cli"
```

---

### Task 2: Normalized diagnostic and scan-report contracts

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/diagnostics.py`
- Create: `/workspace/python-doctor/tests/test_diagnostics.py`

**Interfaces:**
- Produces: `Severity`, `RuleMaturity`, `FixSafety`, `ScanStatus`
- Produces: `SourceSpan`, `Diagnostic`, `AnalyzerCoverage`, `ScanReport`
- Produces: `Diagnostic.to_dict() -> dict[str, object]`
- Produces: `ScanReport.to_dict() -> dict[str, object]`

- [ ] **Step 1: Write failing serialization tests**

Create `tests/test_diagnostics.py`:

```python
from __future__ import annotations

import unittest

from python_doctor.diagnostics import (
    AnalyzerCoverage,
    Diagnostic,
    FixSafety,
    RuleMaturity,
    ScanReport,
    ScanStatus,
    Severity,
    SourceSpan,
)


class DiagnosticTests(unittest.TestCase):
    def test_diagnostic_serializes_with_stable_field_names(self) -> None:
        diagnostic = Diagnostic(
            fingerprint="abc123",
            analyzer="python-doctor",
            analyzer_version="0.1.0.dev0",
            rule_id="python-doctor/safety/no-direct-recursion",
            original_rule_id="no-direct-recursion",
            title="Direct recursion",
            message="Function 'walk' calls itself.",
            rationale="Recursion prevents a static stack bound.",
            remediation="Replace recursion with a bounded iterative traversal.",
            category="Reliability",
            severity=Severity.ERROR,
            confidence=1.0,
            maturity=RuleMaturity.EXPERIMENTAL,
            path="src/worker.py",
            span=SourceSpan(3, 1, 4, 16),
            fix_safety=FixSafety.AGENT_REQUIRED,
            root_cause_group=None,
            tags=("safety-critical",),
        )
        payload = diagnostic.to_dict()
        self.assertEqual(payload["ruleId"], diagnostic.rule_id)
        self.assertEqual(payload["severity"], "error")
        self.assertEqual(payload["span"]["startLine"], 3)
        self.assertNotIn("source", payload)

    def test_partial_report_keeps_coverage_reason(self) -> None:
        report = ScanReport(
            schema_version=1,
            status=ScanStatus.PARTIAL,
            project_root="/repo",
            diagnostics=(),
            coverage=(AnalyzerCoverage("ruff", "unavailable", "executable not found"),),
            skipped_checks=("ruff",),
        )
        payload = report.to_dict()
        self.assertEqual(payload["status"], "partial")
        self.assertEqual(payload["coverage"][0]["reason"], "executable not found")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_diagnostics -v`

Expected: import failure for `python_doctor.diagnostics`.

- [ ] **Step 3: Implement immutable contracts and explicit serialization**

Create `src/python_doctor/diagnostics.py`:

```python
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

    def to_dict(self) -> Dict[str, object]:
        return {
            "schemaVersion": self.schema_version,
            "status": self.status.value,
            "projectRoot": self.project_root,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "coverage": [item.to_dict() for item in self.coverage],
            "skippedChecks": list(self.skipped_checks),
        }
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_diagnostics -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit the contracts**

```bash
git add src/python_doctor/diagnostics.py tests/test_diagnostics.py
git commit -m "feat: define diagnostic contracts"
```

---

### Task 3: Stable diagnostic fingerprints

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/fingerprints.py`
- Create: `/workspace/python-doctor/tests/test_fingerprints.py`

**Interfaces:**
- Consumes: normalized repository-relative path, rule ID, message key, and evidence text
- Produces: `compute_fingerprint(path: str, rule_id: str, message_key: str, evidence: str) -> str`

- [ ] **Step 1: Write failing normalization and stability tests**

Create `tests/test_fingerprints.py`:

```python
from __future__ import annotations

import unittest

from python_doctor.fingerprints import compute_fingerprint


class FingerprintTests(unittest.TestCase):
    def test_path_separators_and_whitespace_do_not_change_identity(self) -> None:
        left = compute_fingerprint("src\\app.py", "ruff/F401", "unused-import", " import   os ")
        right = compute_fingerprint("src/app.py", "ruff/F401", "unused-import", "import os")
        self.assertEqual(left, right)

    def test_rule_change_changes_identity(self) -> None:
        first = compute_fingerprint("src/app.py", "ruff/F401", "unused-import", "import os")
        second = compute_fingerprint("src/app.py", "ruff/F841", "unused-variable", "import os")
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_fingerprints -v`

Expected: import failure for `python_doctor.fingerprints`.

- [ ] **Step 3: Implement canonicalization and SHA-256 identity**

Create `src/python_doctor/fingerprints.py`:

```python
from __future__ import annotations

import hashlib
import re


_WHITESPACE = re.compile(r"\s+")


def compute_fingerprint(path: str, rule_id: str, message_key: str, evidence: str) -> str:
    normalized_path = path.replace("\\", "/").lstrip("./")
    normalized_evidence = _WHITESPACE.sub(" ", evidence).strip()
    canonical = "\x1f".join((normalized_path, rule_id, message_key, normalized_evidence))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_fingerprints -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit fingerprinting**

```bash
git add src/python_doctor/fingerprints.py tests/test_fingerprints.py
git commit -m "feat: add stable diagnostic fingerprints"
```

---

### Task 4: Configuration loading with a permanent telemetry prohibition

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/config.py`
- Create: `/workspace/python-doctor/tests/test_config.py`

**Interfaces:**
- Produces: `NetworkConfig`, `DoctorConfig`, `ConfigError`
- Produces: `load_config(project_root: Path) -> DoctorConfig`
- Rejects: any `telemetry`, `analytics`, `crash_reporting`, or `remote_scoring` key at any depth

- [ ] **Step 1: Write failing default, explicit-network, and prohibited-key tests**

Create `tests/test_config.py`:

```python
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_doctor.config import ConfigError, load_config


class ConfigTests(unittest.TestCase):
    def test_defaults_are_offline_and_default_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = load_config(Path(directory))
        self.assertEqual(config.profile, "default")
        self.assertFalse(config.network.vulnerability_intelligence)

    def test_reads_python_doctor_table_from_pyproject(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("pyproject.toml").write_text(
                '[tool.python-doctor]\nprofile = "strict"\n'
                '[tool.python-doctor.network]\nvulnerability_intelligence = true\n',
                encoding="utf-8",
            )
            config = load_config(root)
        self.assertEqual(config.profile, "strict")
        self.assertTrue(config.network.vulnerability_intelligence)

    def test_rejects_telemetry_even_when_nested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                '[network]\ntelemetry = true\n', encoding="utf-8"
            )
            with self.assertRaisesRegex(ConfigError, "telemetry is not supported"):
                load_config(root)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_config -v`

Expected: import failure for `python_doctor.config`.

- [ ] **Step 3: Implement strict TOML loading**

Create `src/python_doctor/config.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.9/3.10 CI
    import tomli as tomllib  # type: ignore[no-redef]


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class NetworkConfig:
    vulnerability_intelligence: bool = False


@dataclass(frozen=True)
class DoctorConfig:
    profile: str = "default"
    network: NetworkConfig = NetworkConfig()


_PROHIBITED_KEYS = {"telemetry", "analytics", "crash_reporting", "remote_scoring"}
_PROFILES = {"default", "strict", "safety-critical"}


def _reject_prohibited_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _PROHIBITED_KEYS:
                raise ConfigError(f"{normalized} is not supported by Python Doctor")
            _reject_prohibited_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_prohibited_keys(nested)


def _read_toml(path: Path) -> Dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_config(project_root: Path) -> DoctorConfig:
    standalone = project_root / "python-doctor.toml"
    pyproject = project_root / "pyproject.toml"
    if standalone.exists():
        raw = _read_toml(standalone)
    elif pyproject.exists():
        raw = _read_toml(pyproject).get("tool", {}).get("python-doctor", {})
    else:
        raw = {}
    _reject_prohibited_keys(raw)
    profile = str(raw.get("profile", "default"))
    if profile not in _PROFILES:
        raise ConfigError(f"unknown profile: {profile}")
    network = raw.get("network", {})
    vulnerability_intelligence = network.get("vulnerability_intelligence", False)
    if not isinstance(vulnerability_intelligence, bool):
        raise ConfigError("network.vulnerability_intelligence must be a boolean")
    return DoctorConfig(
        profile=profile,
        network=NetworkConfig(vulnerability_intelligence=vulnerability_intelligence),
    )
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_config -v`

Expected: 3 tests pass.

- [ ] **Step 5: Commit configuration**

```bash
git add src/python_doctor/config.py tests/test_config.py
git commit -m "feat: load privacy-safe doctor config"
```

---

### Task 5: Python project discovery

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/discovery.py`
- Create: `/workspace/python-doctor/tests/test_discovery.py`
- Create: `/workspace/python-doctor/tests/fixtures/clean_project/pyproject.toml`
- Create: `/workspace/python-doctor/tests/fixtures/clean_project/src/app.py`

**Interfaces:**
- Produces: `ProjectInfo(root: Path, python_files: tuple[Path, ...], config_files: tuple[Path, ...], python_requires: str | None)`
- Produces: `discover_project(path: Path) -> ProjectInfo`
- Excludes: `.git`, `.venv`, `venv`, `__pycache__`, `build`, `dist`, `.tox`, `.nox`, generated and vendored trees by directory name

- [ ] **Step 1: Write failing discovery tests and fixture**

Create `tests/fixtures/clean_project/pyproject.toml`:

```toml
[project]
name = "clean-project"
version = "0.1.0"
requires-python = ">=3.9"
```

Create `tests/fixtures/clean_project/src/app.py`:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

Create `tests/test_discovery.py`:

```python
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_doctor.discovery import discover_project


FIXTURE = Path(__file__).parent / "fixtures" / "clean_project"


class DiscoveryTests(unittest.TestCase):
    def test_discovers_sources_and_python_requirement(self) -> None:
        project = discover_project(FIXTURE)
        self.assertEqual(project.python_requires, ">=3.9")
        self.assertEqual([path.relative_to(project.root).as_posix() for path in project.python_files], ["src/app.py"])

    def test_excludes_virtual_environment_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            root.joinpath(".venv/lib").mkdir(parents=True)
            root.joinpath(".venv/lib/foreign.py").write_text("bad = 1\n", encoding="utf-8")
            project = discover_project(root)
        self.assertEqual([path.name for path in project.python_files], ["app.py"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_discovery -v`

Expected: import failure for `python_doctor.discovery`.

- [ ] **Step 3: Implement deterministic discovery**

Create `src/python_doctor/discovery.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


_IGNORED_DIRECTORIES = {
    ".git", ".venv", "venv", "__pycache__", "build", "dist", ".tox", ".nox", "vendor", "vendored"
}
_CONFIG_NAMES = (
    "pyproject.toml", "python-doctor.toml", "ruff.toml", ".ruff.toml", "mypy.ini", "pyrightconfig.json"
)


@dataclass(frozen=True)
class ProjectInfo:
    root: Path
    python_files: Tuple[Path, ...]
    config_files: Tuple[Path, ...]
    python_requires: Optional[str]


def _python_requirement(root: Path) -> Optional[str]:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    with pyproject.open("rb") as handle:
        project = tomllib.load(handle).get("project", {})
    value = project.get("requires-python")
    return str(value) if value is not None else None


def discover_project(path: Path) -> ProjectInfo:
    root = path.expanduser().resolve()
    python_files = tuple(
        sorted(
            candidate
            for candidate in root.rglob("*.py")
            if not any(part in _IGNORED_DIRECTORIES for part in candidate.relative_to(root).parts)
        )
    )
    config_files = tuple(root / name for name in _CONFIG_NAMES if (root / name).exists())
    return ProjectInfo(root, python_files, config_files, _python_requirement(root))
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_discovery -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit discovery**

```bash
git add src/python_doctor/discovery.py tests/test_discovery.py tests/fixtures/clean_project
git commit -m "feat: discover python project sources"
```

---

### Task 6: Native rule protocol and direct-recursion detector

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/rules/base.py`
- Create: `/workspace/python-doctor/src/python_doctor/rules/no_direct_recursion.py`
- Create: `/workspace/python-doctor/src/python_doctor/rules/__init__.py`
- Create: `/workspace/python-doctor/tests/test_native_rules.py`
- Create: `/workspace/python-doctor/tests/fixtures/recursive_project/pyproject.toml`
- Create: `/workspace/python-doctor/tests/fixtures/recursive_project/src/worker.py`

**Interfaces:**
- Produces: `RuleContext(project_root: Path, profile: str)`
- Produces: `NativeRule` protocol with `analyze(path: Path, source: str, context: RuleContext) -> tuple[Diagnostic, ...]`
- Produces: `NoDirectRecursionRule`
- Produces: `built_in_rules(profile: str) -> tuple[NativeRule, ...]`

- [ ] **Step 1: Write failing positive, negative, and profile-gating tests**

Create `tests/fixtures/recursive_project/pyproject.toml`:

```toml
[project]
name = "recursive-project"
version = "0.1.0"
requires-python = ">=3.9"
```

Create `tests/fixtures/recursive_project/src/worker.py`:

```python
def countdown(value: int) -> int:
    if value <= 0:
        return 0
    return countdown(value - 1)
```

Create `tests/test_native_rules.py`:

```python
from __future__ import annotations

import unittest
from pathlib import Path

from python_doctor.rules import built_in_rules
from python_doctor.rules.base import RuleContext
from python_doctor.rules.no_direct_recursion import NoDirectRecursionRule


class NativeRuleTests(unittest.TestCase):
    def test_reports_direct_recursion(self) -> None:
        source = "def walk(value):\n    return walk(value - 1)\n"
        rule = NoDirectRecursionRule()
        findings = rule.analyze(Path("src/worker.py"), source, RuleContext(Path("."), "safety-critical"))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule_id, "python-doctor/safety/no-direct-recursion")
        self.assertEqual(findings[0].span.start_line, 1)

    def test_does_not_report_call_to_different_function(self) -> None:
        source = "def walk(value):\n    return visit(value)\n"
        findings = NoDirectRecursionRule().analyze(
            Path("src/worker.py"), source, RuleContext(Path("."), "safety-critical")
        )
        self.assertEqual(findings, ())

    def test_rule_is_only_enabled_for_safety_profile(self) -> None:
        self.assertEqual(built_in_rules("default"), ())
        self.assertEqual(len(built_in_rules("safety-critical")), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_native_rules -v`

Expected: import failure for `python_doctor.rules`.

- [ ] **Step 3: Implement the rule protocol and detector**

Create `src/python_doctor/rules/base.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Tuple

from python_doctor.diagnostics import Diagnostic


@dataclass(frozen=True)
class RuleContext:
    project_root: Path
    profile: str


class NativeRule(Protocol):
    def analyze(
        self, path: Path, source: str, context: RuleContext
    ) -> Tuple[Diagnostic, ...]: ...
```

Create `src/python_doctor/rules/no_direct_recursion.py`:

```python
from __future__ import annotations

import ast
from pathlib import Path
from typing import List, Tuple

from python_doctor import __version__
from python_doctor.diagnostics import Diagnostic, FixSafety, RuleMaturity, Severity, SourceSpan
from python_doctor.fingerprints import compute_fingerprint
from python_doctor.rules.base import RuleContext


class _RecursionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.stack: List[ast.FunctionDef] = []
        self.matches: List[Tuple[ast.FunctionDef, ast.Call]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.stack.append(node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.stack.append(node)  # type: ignore[arg-type]
        self.generic_visit(node)
        self.stack.pop()

    def visit_Call(self, node: ast.Call) -> None:
        if self.stack and isinstance(node.func, ast.Name) and node.func.id == self.stack[-1].name:
            self.matches.append((self.stack[-1], node))
        self.generic_visit(node)


class NoDirectRecursionRule:
    def analyze(self, path: Path, source: str, context: RuleContext) -> Tuple[Diagnostic, ...]:
        tree = ast.parse(source, filename=str(path))
        visitor = _RecursionVisitor()
        visitor.visit(tree)
        findings = []
        relative_path = path.as_posix()
        for function, call in visitor.matches:
            findings.append(
                Diagnostic(
                    fingerprint=compute_fingerprint(
                        relative_path,
                        "python-doctor/safety/no-direct-recursion",
                        "direct-recursion",
                        function.name,
                    ),
                    analyzer="python-doctor",
                    analyzer_version=__version__,
                    rule_id="python-doctor/safety/no-direct-recursion",
                    original_rule_id="no-direct-recursion",
                    title="Direct recursion",
                    message=f"Function '{function.name}' calls itself directly.",
                    rationale="Recursion prevents a static upper bound on stack use.",
                    remediation="Use an explicitly bounded iterative traversal.",
                    category="Reliability",
                    severity=Severity.ERROR,
                    confidence=1.0,
                    maturity=RuleMaturity.EXPERIMENTAL,
                    path=relative_path,
                    span=SourceSpan(
                        function.lineno,
                        function.col_offset + 1,
                        getattr(call, "end_lineno", call.lineno),
                        getattr(call, "end_col_offset", call.col_offset + 1) + 1,
                    ),
                    fix_safety=FixSafety.AGENT_REQUIRED,
                    root_cause_group=None,
                    tags=("safety-critical",),
                )
            )
        return tuple(findings)
```

Create `src/python_doctor/rules/__init__.py`:

```python
from __future__ import annotations

from typing import Tuple

from python_doctor.rules.base import NativeRule
from python_doctor.rules.no_direct_recursion import NoDirectRecursionRule


def built_in_rules(profile: str) -> Tuple[NativeRule, ...]:
    if profile == "safety-critical":
        return (NoDirectRecursionRule(),)
    return ()
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_native_rules -v`

Expected: 3 tests pass.

- [ ] **Step 5: Commit the first native rule**

```bash
git add src/python_doctor/rules tests/test_native_rules.py tests/fixtures/recursive_project
git commit -m "feat: detect direct recursion in safety profile"
```

---

### Task 7: External-tool runner and Ruff JSON adapter

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/adapters/base.py`
- Create: `/workspace/python-doctor/src/python_doctor/adapters/ruff.py`
- Create: `/workspace/python-doctor/src/python_doctor/adapters/__init__.py`
- Create: `/workspace/python-doctor/tests/test_ruff_adapter.py`

**Interfaces:**
- Produces: `ToolExecution`, `ExternalToolError`, `run_tool(command: Sequence[str], cwd: Path, timeout_seconds: float) -> ToolExecution`
- Produces: `RuffAdapter(executable: str = "ruff")`
- Produces: `RuffAdapter.analyze(project: ProjectInfo) -> tuple[Diagnostic, ...]`
- Never invokes a shell and never performs installation or network access.

- [ ] **Step 1: Write failing Ruff contract tests with a fake executable**

Create `tests/test_ruff_adapter.py`:

```python
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from python_doctor.adapters.ruff import RuffAdapter
from python_doctor.discovery import discover_project


class RuffAdapterTests(unittest.TestCase):
    def test_normalizes_ruff_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("import os\n", encoding="utf-8")
            fake = root / "fake-ruff"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps([{\"code\":\"F401\",\"message\":\"`os` imported but unused\","
                "\"filename\":\"app.py\",\"location\":{\"row\":1,\"column\":8},"
                "\"end_location\":{\"row\":1,\"column\":10},\"fix\":None}]))\n",
                encoding="utf-8",
            )
            fake.chmod(fake.stat().st_mode | 0o111)
            diagnostic = RuffAdapter(str(fake)).analyze(discover_project(root))[0]
        self.assertEqual(diagnostic.rule_id, "ruff/F401")
        self.assertEqual(diagnostic.path, "app.py")
        self.assertEqual(diagnostic.severity.value, "warning")

    def test_fake_adapter_receives_no_network_environment_toggle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            fake = root / "fake-ruff"
            marker = root / "marker.txt"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import os, pathlib\n"
                f"pathlib.Path({str(marker)!r}).write_text(os.environ.get('PYTHON_DOCTOR_OFFLINE', ''))\n"
                "print('[]')\n",
                encoding="utf-8",
            )
            fake.chmod(fake.stat().st_mode | 0o111)
            RuffAdapter(str(fake)).analyze(discover_project(root))
            self.assertEqual(marker.read_text(encoding="utf-8"), "1")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_ruff_adapter -v`

Expected: import failure for `python_doctor.adapters.ruff`.

- [ ] **Step 3: Implement safe subprocess execution and Ruff normalization**

Create `src/python_doctor/adapters/base.py`:

```python
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


class ExternalToolError(RuntimeError):
    pass


@dataclass(frozen=True)
class ToolExecution:
    return_code: int
    stdout: str
    stderr: str


def run_tool(command: Sequence[str], cwd: Path, timeout_seconds: float) -> ToolExecution:
    environment = os.environ.copy()
    environment["PYTHON_DOCTOR_OFFLINE"] = "1"
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd),
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            shell=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ExternalToolError(str(error)) from error
    return ToolExecution(completed.returncode, completed.stdout, completed.stderr)
```

Create `src/python_doctor/adapters/ruff.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from python_doctor.adapters.base import ExternalToolError, run_tool
from python_doctor.diagnostics import Diagnostic, FixSafety, RuleMaturity, Severity, SourceSpan
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
            try:
                path = filename.resolve().relative_to(project.root).as_posix()
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
                    span=SourceSpan(location["row"], location["column"], end["row"], end["column"]),
                    fix_safety=FixSafety.SAFE_AUTOMATIC if fix and fix.get("applicability") == "safe" else FixSafety.AGENT_REQUIRED,
                    root_cause_group=None,
                    tags=("ruff",),
                )
            )
        return tuple(findings)
```

Create `src/python_doctor/adapters/__init__.py`:

```python
from python_doctor.adapters.ruff import RuffAdapter

__all__ = ["RuffAdapter"]
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_ruff_adapter -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit the adapter**

```bash
git add src/python_doctor/adapters tests/test_ruff_adapter.py
git commit -m "feat: normalize ruff diagnostics"
```

---

### Task 8: Scan orchestration and explicit partial coverage

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/scanner.py`
- Create: `/workspace/python-doctor/tests/test_scanner.py`

**Interfaces:**
- Produces: `ScanOptions(profile: str, require_ruff: bool, ruff_executable: str)`
- Produces: `scan_project(path: Path, options: ScanOptions) -> ScanReport`
- Consumes: configuration, discovery, built-in rules, Ruff adapter
- Guarantees: deterministic diagnostic ordering by `(path, line, column, rule_id, fingerprint)`

- [ ] **Step 1: Write failing full and partial scan tests**

Create `tests/test_scanner.py`:

```python
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_doctor.diagnostics import ScanStatus
from python_doctor.scanner import ScanOptions, scan_project


FIXTURES = Path(__file__).parent / "fixtures"


class ScannerTests(unittest.TestCase):
    def test_safety_profile_finds_direct_recursion_without_ruff(self) -> None:
        report = scan_project(
            FIXTURES / "recursive_project",
            ScanOptions(profile="safety-critical", require_ruff=False, ruff_executable="missing-ruff"),
        )
        self.assertEqual(report.status, ScanStatus.PARTIAL)
        self.assertEqual(len(report.diagnostics), 1)
        self.assertEqual(report.diagnostics[0].rule_id, "python-doctor/safety/no-direct-recursion")
        self.assertEqual(report.coverage[1].status, "unavailable")

    def test_required_missing_ruff_marks_failed_coverage(self) -> None:
        report = scan_project(
            FIXTURES / "clean_project",
            ScanOptions(profile="default", require_ruff=True, ruff_executable="missing-ruff"),
        )
        self.assertEqual(report.status, ScanStatus.FAILED)
        self.assertIn("ruff", report.skipped_checks)

    def test_syntax_error_marks_native_coverage_partial_instead_of_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("broken.py").write_text("def broken(:\n", encoding="utf-8")
            report = scan_project(
                root,
                ScanOptions(
                    profile="safety-critical",
                    require_ruff=False,
                    ruff_executable="missing-ruff",
                ),
            )
        self.assertEqual(report.status, ScanStatus.PARTIAL)
        self.assertEqual(report.coverage[0].status, "partial")
        self.assertIn("python-doctor/native", report.skipped_checks)

    def test_directory_without_python_sources_is_unsupported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = scan_project(Path(directory), ScanOptions(ruff_executable="missing-ruff"))
        self.assertEqual(report.status, ScanStatus.UNSUPPORTED)
        self.assertEqual(report.diagnostics, ())
        self.assertIn("no Python source files", report.coverage[0].reason or "")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_scanner -v`

Expected: import failure for `python_doctor.scanner`.

- [ ] **Step 3: Implement orchestration and coverage semantics**

Create `src/python_doctor/scanner.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from python_doctor.adapters.base import ExternalToolError
from python_doctor.adapters.ruff import RuffAdapter
from python_doctor.diagnostics import AnalyzerCoverage, Diagnostic, ScanReport, ScanStatus
from python_doctor.discovery import discover_project
from python_doctor.rules import built_in_rules
from python_doctor.rules.base import RuleContext


@dataclass(frozen=True)
class ScanOptions:
    profile: str = "default"
    require_ruff: bool = False
    ruff_executable: str = "ruff"


def scan_project(path: Path, options: ScanOptions) -> ScanReport:
    project = discover_project(path)
    if not project.python_files:
        return ScanReport(
            schema_version=1,
            status=ScanStatus.UNSUPPORTED,
            project_root=str(project.root),
            diagnostics=(),
            coverage=(
                AnalyzerCoverage("python-doctor", "unsupported", "no Python source files"),
                AnalyzerCoverage("ruff", "skipped", "no Python source files"),
            ),
            skipped_checks=("python-doctor/native", "ruff"),
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
                    rule.analyze(relative, source, RuleContext(project.root, options.profile))
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

    ruff_failed = False
    try:
        diagnostics.extend(RuffAdapter(options.ruff_executable).analyze(project))
        coverage.append(AnalyzerCoverage("ruff", "complete", None))
    except ExternalToolError as error:
        skipped.append("ruff")
        ruff_failed = options.require_ruff
        coverage.append(AnalyzerCoverage("ruff", "unavailable", str(error)))

    diagnostics.sort(
        key=lambda item: (
            item.path,
            item.span.start_line,
            item.span.start_column,
            item.rule_id,
            item.fingerprint,
        )
    )
    if ruff_failed:
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
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_scanner -v`

Expected: 4 tests pass.

- [ ] **Step 5: Commit orchestration**

```bash
git add src/python_doctor/scanner.py tests/test_scanner.py
git commit -m "feat: orchestrate deterministic scans"
```

---

### Task 9: Terminal and JSON reports

**Files:**
- Create: `/workspace/python-doctor/src/python_doctor/reports/json_report.py`
- Create: `/workspace/python-doctor/src/python_doctor/reports/terminal.py`
- Create: `/workspace/python-doctor/src/python_doctor/reports/__init__.py`
- Create: `/workspace/python-doctor/tests/test_reports.py`

**Interfaces:**
- Produces: `render_json(report: ScanReport, pretty: bool = True) -> str`
- Produces: `render_terminal(report: ScanReport) -> str`
- Guarantees: sorted JSON keys, newline-terminated output, no source contents

- [ ] **Step 1: Write failing report tests**

Create `tests/test_reports.py`:

```python
from __future__ import annotations

import json
import unittest

from python_doctor.diagnostics import AnalyzerCoverage, ScanReport, ScanStatus
from python_doctor.reports import render_json, render_terminal


class ReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.report = ScanReport(
            schema_version=1,
            status=ScanStatus.PARTIAL,
            project_root="/repo",
            diagnostics=(),
            coverage=(AnalyzerCoverage("ruff", "unavailable", "not found"),),
            skipped_checks=("ruff",),
        )

    def test_json_is_versioned_and_newline_terminated(self) -> None:
        rendered = render_json(self.report)
        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(json.loads(rendered)["schemaVersion"], 1)

    def test_terminal_report_never_calls_partial_scan_clean(self) -> None:
        rendered = render_terminal(self.report)
        self.assertIn("PARTIAL", rendered)
        self.assertIn("ruff: unavailable", rendered)
        self.assertNotIn("No issues found", rendered)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_reports -v`

Expected: import failure for `python_doctor.reports`.

- [ ] **Step 3: Implement deterministic renderers**

Create `src/python_doctor/reports/json_report.py`:

```python
from __future__ import annotations

import json

from python_doctor.diagnostics import ScanReport


def render_json(report: ScanReport, pretty: bool = True) -> str:
    return json.dumps(
        report.to_dict(),
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        sort_keys=True,
    ) + "\n"
```

Create `src/python_doctor/reports/terminal.py`:

```python
from __future__ import annotations

from typing import List

from python_doctor.diagnostics import ScanReport, ScanStatus


def render_terminal(report: ScanReport) -> str:
    lines: List[str] = [f"Python Doctor: {report.status.value.upper()}"]
    lines.append(f"Project: {report.project_root}")
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
```

Create `src/python_doctor/reports/__init__.py`:

```python
from python_doctor.reports.json_report import render_json
from python_doctor.reports.terminal import render_terminal

__all__ = ["render_json", "render_terminal"]
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `PYTHONPATH=src python3 -m unittest tests.test_reports -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit report rendering**

```bash
git add src/python_doctor/reports tests/test_reports.py
git commit -m "feat: render terminal and json reports"
```

---

### Task 10: Wire the `scan` CLI, exit codes, and offline guarantee

**Files:**
- Modify: `/workspace/python-doctor/src/python_doctor/cli.py`
- Modify: `/workspace/python-doctor/tests/test_cli.py`

**Interfaces:**
- Consumes: `load_config`, `ScanOptions`, `scan_project`, report renderers
- Produces flags: `--format terminal|json`, `--profile`, `--require-ruff`, `--ruff-executable`, `--offline`
- Exit codes: `0` clean/findings below policy, `2` invalid invocation/config, `3` required analyzer failed, `4` partial scan when completeness is required, `5` internal failure
- Foundation behavior: findings are advisory, so they return `0`; severity policy arrives in plan 2.

- [ ] **Step 1: Extend CLI tests before implementation**

Add these methods to `CliTests` in `tests/test_cli.py`:

```python
    def test_scan_json_reports_schema_and_partial_status(self) -> None:
        import json
        from pathlib import Path

        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                ["scan", str(fixture), "--format", "json", "--ruff-executable", "missing-ruff"]
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["schemaVersion"], 1)
        self.assertEqual(payload["status"], "partial")

    def test_required_missing_ruff_returns_analyzer_exit_code(self) -> None:
        from pathlib import Path

        fixture = Path(__file__).parent / "fixtures" / "clean_project"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                ["scan", str(fixture), "--require-ruff", "--ruff-executable", "missing-ruff"]
            )
        self.assertEqual(exit_code, 3)
        self.assertIn("FAILED", output.getvalue())
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_cli.CliTests.test_scan_json_reports_schema_and_partial_status tests.test_cli.CliTests.test_required_missing_ruff_returns_analyzer_exit_code -v`

Expected: argparse rejects the new flags or returns the wrong output.

- [ ] **Step 3: Replace `cli.py` with the complete foundation CLI**

```python
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from python_doctor import __version__
from python_doctor.config import ConfigError, load_config
from python_doctor.diagnostics import ScanStatus
from python_doctor.reports import render_json, render_terminal
from python_doctor.scanner import ScanOptions, scan_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python-doctor")
    parser.add_argument("--version", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    scan = subparsers.add_parser("scan", help="scan a Python project")
    scan.add_argument("path", nargs="?", default=".")
    scan.add_argument("--format", choices=("terminal", "json"), default="terminal")
    scan.add_argument("--profile", choices=("default", "strict", "safety-critical"))
    scan.add_argument("--require-ruff", action="store_true")
    scan.add_argument("--ruff-executable", default="ruff")
    scan.add_argument("--offline", action="store_true", default=True)
    return parser


def _scan(args: argparse.Namespace) -> int:
    root = Path(args.path).expanduser().resolve()
    try:
        config = load_config(root)
    except (ConfigError, OSError, ValueError) as error:
        print(f"Configuration error: {error}")
        return 2
    profile = args.profile or config.profile
    report = scan_project(
        root,
        ScanOptions(
            profile=profile,
            require_ruff=args.require_ruff,
            ruff_executable=args.ruff_executable,
        ),
    )
    print(
        render_json(report).rstrip("\n")
        if args.format == "json"
        else render_terminal(report).rstrip("\n")
    )
    if report.status is ScanStatus.FAILED:
        return 3
    return 0


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
```

- [ ] **Step 4: Run the complete foundation test suite**

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Expected: all tests pass with no warnings or network access.

- [ ] **Step 5: Run two manual smoke checks**

Run:

```bash
PYTHONPATH=src python3 -m python_doctor scan tests/fixtures/clean_project --format json --ruff-executable missing-ruff
PYTHONPATH=src python3 -m python_doctor scan tests/fixtures/recursive_project --profile safety-critical --ruff-executable missing-ruff
```

Expected: the first returns versioned JSON with `status: partial`; the second reports exactly one direct-recursion finding and partial Ruff coverage.

- [ ] **Step 6: Commit the usable vertical slice**

```bash
git add src/python_doctor/cli.py tests/test_cli.py
git commit -m "feat: expose deterministic scan command"
```

---

### Task 11: Foundation verification checkpoint

**Files:**
- Modify only files required by failures discovered during this checkpoint.

**Interfaces:**
- Verifies every interface produced by Tasks 1-10.
- Produces a clean commit and evidence for the next plan.

- [ ] **Step 1: Run syntax compilation across source and tests**

Run:

```bash
python3 -m compileall -q src tests
```

Expected: exit code 0 and no output.

- [ ] **Step 2: Run the full tests twice to detect state leakage**

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Expected: identical passing counts both times.

- [ ] **Step 3: Verify no telemetry vocabulary or network-capable imports entered production code**

Run:

```bash
rg -n "telemetry|analytics|crash.report|remote.scor|requests|urllib|httpx|aiohttp|socket" src/python_doctor
```

Expected: only the deliberate prohibited-key strings in `config.py`; no network library imports and no telemetry implementation.

- [ ] **Step 4: Verify deterministic JSON**

Run:

```bash
PYTHONPATH=src python3 -m python_doctor scan tests/fixtures/recursive_project --profile safety-critical --format json --ruff-executable missing-ruff > /tmp/python-doctor-a.json
PYTHONPATH=src python3 -m python_doctor scan tests/fixtures/recursive_project --profile safety-critical --format json --ruff-executable missing-ruff > /tmp/python-doctor-b.json
cmp /tmp/python-doctor-a.json /tmp/python-doctor-b.json
```

Expected: `cmp` exits 0.

- [ ] **Step 5: Inspect repository state and commit only verification fixes**

Run:

```bash
git status --short
git log --oneline --decorate -10
```

Expected: no uncommitted changes. If verification exposed a defect, add a regression test first, fix it, rerun Steps 1-4, and use a commit message that names the observed behavior, such as `fix: preserve partial status when Ruff is unavailable`.

- [ ] **Step 6: Record the checkpoint tag locally**

```bash
git tag python-doctor-foundation-v0
```

Expected: `git tag --list python-doctor-foundation-v0` prints the tag. Do not push or publish the product repository until the user selects its GitHub destination.
