from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path


def _installed_skill_root() -> Path:
    configured = os.environ.get("PYTHON_DOCTOR_SKILL_DIR")
    if configured:
        return Path(configured)
    skills_root = Path("/root/.codex/skills/remote-skills")
    preferred = skills_root / "python-doctor"
    if preferred.joinpath("SKILL.md").is_file():
        return preferred
    for skill_file in sorted(skills_root.glob("*/SKILL.md")):
        header = skill_file.read_text(encoding="utf-8").splitlines()[:4]
        if "name: python-doctor" in header:
            return skill_file.parent
    return preferred


SKILL_ROOT = _installed_skill_root()


class SkillContractTests(unittest.TestCase):
    def test_skill_package_has_required_structure_and_trigger(self) -> None:
        skill = SKILL_ROOT.joinpath("SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: python-doctor\n"))
        description = next(
            line for line in skill.splitlines() if line.startswith("description:")
        )
        self.assertIn("Use when", description)
        self.assertTrue(SKILL_ROOT.joinpath("agents/openai.yaml").is_file())
        self.assertNotIn("TODO", skill)

    def test_skill_covers_scan_fix_ci_and_privacy_scenarios(self) -> None:
        paths = [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").glob("*.md"))]
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
        required_phrases = (
            "partial",
            "coverage",
            "safe-automatic",
            "rerun",
            "git diff",
            "sarif",
            "exit code",
            "no telemetry",
            "never upload source",
            "vulnerability intelligence",
        )
        for phrase in required_phrases:
            self.assertIn(phrase, corpus)

    def test_launcher_exposes_doctor_help(self) -> None:
        launcher = SKILL_ROOT / "scripts" / "run_python_doctor.py"
        completed = subprocess.run(
            ["python3", str(launcher), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("python-doctor", completed.stdout)
        self.assertIn("scan", completed.stdout)


if __name__ == "__main__":
    unittest.main()
