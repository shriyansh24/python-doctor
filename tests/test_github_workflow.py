from __future__ import annotations

import unittest
from pathlib import Path


class GitHubWorkflowTests(unittest.TestCase):
    def test_workflow_has_least_privilege_complete_scan_without_uploads(self) -> None:
        workflow = Path(".github/workflows/python-doctor.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("pull_request:", workflow)
        self.assertIn("branches: [main]", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("actions/checkout@v4", workflow)
        self.assertIn("actions/setup-python@v5", workflow)
        self.assertIn("--format github", workflow)
        self.assertIn("--require-complete", workflow)
        self.assertIn("--blocking error", workflow)
        prohibited = (
            "upload-sarif",
            "upload-artifact",
            "security-events: write",
            "telemetry",
            "analytics",
            "curl ",
            "wget ",
            "http://",
        )
        self.assertFalse(any(value in workflow.lower() for value in prohibited))


if __name__ == "__main__":
    unittest.main()
