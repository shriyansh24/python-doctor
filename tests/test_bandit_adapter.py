from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from python_doctor.adapters.bandit import BanditAdapter
from python_doctor.adapters.base import ExternalToolError
from python_doctor.discovery import discover_project


def write_fake(root: Path, body: str) -> Path:
    fake = root / "fake-bandit"
    fake.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
    fake.chmod(fake.stat().st_mode | 0o111)
    return fake


class BanditAdapterTests(unittest.TestCase):
    def test_normalizes_security_finding_without_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("assert True\n", encoding="utf-8")
            payload = {
                "errors": [],
                "results": [
                    {
                        "code": "assert True",
                        "filename": "app.py",
                        "issue_confidence": "HIGH",
                        "issue_severity": "MEDIUM",
                        "issue_text": "Use of assert detected.",
                        "line_number": 1,
                        "line_range": [1],
                        "col_offset": 0,
                        "end_col_offset": 11,
                        "test_id": "B101",
                        "test_name": "assert_used",
                        "more_info": "https://bandit.readthedocs.io/B101",
                        "issue_cwe": {"id": 703, "link": "https://cwe.mitre.org/703"},
                    }
                ],
            }
            fake = write_fake(root, f"print({json.dumps(json.dumps(payload))})\n")
            diagnostic = BanditAdapter(str(fake)).analyze(discover_project(root))[0]

        self.assertEqual(diagnostic.rule_id, "bandit/B101")
        self.assertEqual(diagnostic.path, "app.py")
        self.assertEqual(diagnostic.severity.value, "warning")
        self.assertEqual(diagnostic.confidence, 1.0)
        self.assertEqual(diagnostic.span.start_column, 1)
        self.assertNotIn("assert True", str(diagnostic.to_dict()))

    def test_maps_low_and_high_severity_and_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            base = {
                "filename": "app.py",
                "issue_text": "Finding",
                "line_number": 1,
                "line_range": [1],
                "col_offset": 0,
                "end_col_offset": 1,
                "test_name": "test",
            }
            payload = {
                "errors": [],
                "results": [
                    dict(base, test_id="B001", issue_severity="LOW", issue_confidence="LOW"),
                    dict(base, test_id="B002", issue_severity="HIGH", issue_confidence="MEDIUM"),
                ],
            }
            fake = write_fake(root, f"print({json.dumps(json.dumps(payload))})\n")
            diagnostics = BanditAdapter(str(fake)).analyze(discover_project(root))

        self.assertEqual(
            [(item.severity.value, item.confidence) for item in diagnostics],
            [("info", 0.5), ("error", 0.8)],
        )

    def test_bandit_reported_errors_fail_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            payload = {"errors": [{"filename": "bad.py", "reason": "parse error"}], "results": []}
            fake = write_fake(root, f"print({json.dumps(json.dumps(payload))})\n")
            with self.assertRaisesRegex(ExternalToolError, "bad.py"):
                BanditAdapter(str(fake)).analyze(discover_project(root))

    def test_malformed_json_fails_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            fake = write_fake(root, "print(\"not-json\")\n")
            with self.assertRaisesRegex(ExternalToolError, "invalid Bandit JSON"):
                BanditAdapter(str(fake)).analyze(discover_project(root))

    def test_receives_offline_environment_toggle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("app.py").write_text("value = 1\n", encoding="utf-8")
            marker = root / "marker.txt"
            fake = write_fake(
                root,
                "import os, pathlib\n"
                f"pathlib.Path({str(marker)!r}).write_text(os.environ.get('PYTHON_DOCTOR_OFFLINE', ''))\n"
                "print('{\"errors\": [], \"results\": []}')\n",
            )
            BanditAdapter(str(fake)).analyze(discover_project(root))
            self.assertEqual(marker.read_text(encoding="utf-8"), "1")


if __name__ == "__main__":
    unittest.main()
