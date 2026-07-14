from __future__ import annotations

import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.9/3.10 compatibility
    import tomli as tomllib  # type: ignore[no-redef]


class PackageMetadataTests(unittest.TestCase):
    def test_release_analyzers_are_exactly_pinned(self) -> None:
        with Path("pyproject.toml").open("rb") as handle:
            dependencies = set(tomllib.load(handle)["project"]["dependencies"])
        self.assertIn("ruff==0.15.21", dependencies)
        self.assertIn("radon==6.0.1", dependencies)
        self.assertIn(
            "bandit==1.8.6; python_version < '3.10'",
            dependencies,
        )
        self.assertIn(
            "bandit==1.9.4; python_version >= '3.10'",
            dependencies,
        )


if __name__ == "__main__":
    unittest.main()
