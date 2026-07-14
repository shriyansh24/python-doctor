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
        self.assertEqual(
            [path.relative_to(project.root).as_posix() for path in project.python_files],
            ["src/app.py"],
        )

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
