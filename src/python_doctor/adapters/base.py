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
