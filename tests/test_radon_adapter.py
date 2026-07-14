from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from python_doctor.adapters.base import ExternalToolError
from python_doctor.adapters.radon import RadonAdapter
from python_doctor.discovery import discover_project
from tests.test_bandit_adapter import write_fake


class RadonAdapterTests(unittest.TestCase):
    def test_filters_low_complexity_and_maps_rank_severity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("def work():\n    pass\n", encoding="utf-8")
            payload = {
                "app.py": [
                    {
                        "type": "function",
                        "name": "simple",
                        "lineno": 1,
                        "col_offset": 0,
                        "endline": 2,
                        "complexity": 2,
                        "rank": "A",
                    },
                    {
                        "type": "function",
                        "name": "branching",
                        "lineno": 5,
                        "col_offset": 0,
                        "endline": 20,
                        "complexity": 12,
                        "rank": "C",
                    },
                    {
                        "type": "class",
                        "name": "Worker",
                        "lineno": 22,
                        "col_offset": 0,
                        "endline": 45,
                        "complexity": 4,
                        "rank": "A",
                        "methods": [
                            {
                                "type": "method",
                                "name": "run",
                                "lineno": 25,
                                "col_offset": 4,
                                "endline": 44,
                                "complexity": 22,
                                "rank": "D",
                            }
                        ],
                    },
                ]
            }
            fake = write_fake(root, f"print({json.dumps(json.dumps(payload))})\n")
            diagnostics = RadonAdapter(str(fake)).analyze(discover_project(root))

        self.assertEqual([item.severity.value for item in diagnostics], ["warning", "error"])
        self.assertEqual([item.path for item in diagnostics], ["app.py", "app.py"])
        self.assertIn("branching", diagnostics[0].message)
        self.assertIn("complexity 12", diagnostics[0].message)
        self.assertEqual(diagnostics[1].span.start_column, 5)

    def test_output_order_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("a.py").write_text("pass\n", encoding="utf-8")
            root.joinpath("z.py").write_text("pass\n", encoding="utf-8")
            block = {
                "type": "function",
                "name": "work",
                "lineno": 1,
                "col_offset": 0,
                "endline": 2,
                "complexity": 11,
                "rank": "C",
            }
            payload = {"z.py": [block], "a.py": [block]}
            fake = write_fake(root, f"print({json.dumps(json.dumps(payload))})\n")
            diagnostics = RadonAdapter(str(fake)).analyze(discover_project(root))
        self.assertEqual([item.path for item in diagnostics], ["a.py", "z.py"])

    def test_malformed_json_fails_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("pass\n", encoding="utf-8")
            fake = write_fake(root, "print('not-json')\n")
            with self.assertRaisesRegex(ExternalToolError, "invalid Radon JSON"):
                RadonAdapter(str(fake)).analyze(discover_project(root))

    def test_nonzero_exit_fails_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("pass\n", encoding="utf-8")
            fake = write_fake(root, "import sys\nprint('radon failed', file=sys.stderr)\nsys.exit(2)\n")
            with self.assertRaisesRegex(ExternalToolError, "radon failed"):
                RadonAdapter(str(fake)).analyze(discover_project(root))


if __name__ == "__main__":
    unittest.main()
