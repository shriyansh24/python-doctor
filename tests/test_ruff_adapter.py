from __future__ import annotations

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
                'print(json.dumps([{"code":"F401","message":"`os` imported but unused",'
                '"filename":"app.py","location":{"row":1,"column":8},'
                '"end_location":{"row":1,"column":10},"fix":None}]))\n',
                encoding="utf-8",
            )
            fake.chmod(fake.stat().st_mode | 0o111)
            diagnostic = RuffAdapter(str(fake)).analyze(discover_project(root))[0]
        self.assertEqual(diagnostic.rule_id, "ruff/F401")
        self.assertEqual(diagnostic.path, "app.py")
        self.assertEqual(diagnostic.severity.value, "warning")

    def test_fake_adapter_receives_offline_environment_toggle(self) -> None:
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
