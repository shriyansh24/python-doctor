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
