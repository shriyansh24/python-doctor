from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_doctor.config import ConfigError, load_config


class ConfigTests(unittest.TestCase):
    def test_defaults_are_offline_and_default_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = load_config(Path(directory))
        self.assertEqual(config.profile, "default")
        self.assertFalse(config.network.vulnerability_intelligence)

    def test_reads_python_doctor_table_from_pyproject(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("pyproject.toml").write_text(
                '[tool.python-doctor]\nprofile = "strict"\n'
                '[tool.python-doctor.network]\nvulnerability_intelligence = true\n',
                encoding="utf-8",
            )
            config = load_config(root)
        self.assertEqual(config.profile, "strict")
        self.assertTrue(config.network.vulnerability_intelligence)

    def test_rejects_telemetry_even_when_nested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                '[network]\ntelemetry = true\n', encoding="utf-8"
            )
            with self.assertRaisesRegex(ConfigError, "telemetry is not supported"):
                load_config(root)

    def test_reads_policy_controls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                'rules = { "ruff/F401" = "off" }\n'
                'categories = { Security = "error" }\n'
                '[ignore]\nrules = ["bandit/B101"]\nfiles = ["tests/**"]\n'
                '[ci]\nblocking = "warning"\nrequire_complete = true\n',
                encoding="utf-8",
            )
            config = load_config(root)
        self.assertEqual(dict(config.rules)["ruff/F401"], "off")
        self.assertEqual(dict(config.categories)["Security"], "error")
        self.assertEqual(config.ignore_rules, ("bandit/B101",))
        self.assertEqual(config.ignore_files, ("tests/**",))
        self.assertEqual(config.blocking, "warning")
        self.assertTrue(config.require_complete)

    def test_rejects_unknown_rule_severity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                'rules = { "ruff/F401" = "sometimes" }\n', encoding="utf-8"
            )
            with self.assertRaisesRegex(ConfigError, "invalid severity"):
                load_config(root)

    def test_rejects_non_boolean_require_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                '[ci]\nrequire_complete = "yes"\n', encoding="utf-8"
            )
            with self.assertRaisesRegex(ConfigError, "ci.require_complete must be a boolean"):
                load_config(root)

    def test_adapter_defaults_are_enabled_optional_and_local(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = load_config(Path(directory))
        self.assertTrue(config.adapters.ruff.enabled)
        self.assertFalse(config.adapters.ruff.required)
        self.assertEqual(config.adapters.ruff.executable, "ruff")
        self.assertEqual(config.adapters.bandit.executable, "bandit")
        self.assertEqual(config.adapters.radon.executable, "radon")

    def test_reads_adapter_controls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                '[adapters.ruff]\nenabled = false\n'
                '[adapters.bandit]\nrequired = true\nexecutable = "local-bandit"\n',
                encoding="utf-8",
            )
            config = load_config(root)
        self.assertFalse(config.adapters.ruff.enabled)
        self.assertTrue(config.adapters.bandit.required)
        self.assertEqual(config.adapters.bandit.executable, "local-bandit")

    def test_rejects_required_disabled_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("python-doctor.toml").write_text(
                '[adapters.radon]\nenabled = false\nrequired = true\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ConfigError, "cannot be required and disabled"):
                load_config(root)


if __name__ == "__main__":
    unittest.main()
