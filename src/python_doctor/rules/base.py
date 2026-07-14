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
        self,
        path: Path,
        source: str,
        context: RuleContext,
    ) -> Tuple[Diagnostic, ...]: ...
