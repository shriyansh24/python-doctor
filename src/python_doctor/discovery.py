from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.9/3.10 compatibility
    import tomli as tomllib  # type: ignore[no-redef]


_IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
    ".tox",
    ".nox",
    "vendor",
    "vendored",
}
_CONFIG_NAMES = (
    "pyproject.toml",
    "python-doctor.toml",
    "ruff.toml",
    ".ruff.toml",
    "mypy.ini",
    "pyrightconfig.json",
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
            if not any(
                part in _IGNORED_DIRECTORIES
                for part in candidate.relative_to(root).parts
            )
        )
    )
    config_files = tuple(root / name for name in _CONFIG_NAMES if (root / name).exists())
    return ProjectInfo(root, python_files, config_files, _python_requirement(root))
