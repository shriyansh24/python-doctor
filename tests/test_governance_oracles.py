from __future__ import annotations

import ast
import io
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import scripts.governance.validate_oracles as oracle_validator
from scripts.governance.validate_oracles import main, validate_oracles

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.9/3.10
    tomllib = oracle_validator.tomllib  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATHS = (
    "expected-requirement-ids.txt",
    "expected-skill-ids.txt",
    "expected-profile-domain-ids.txt",
    "expected-provenance-sources.toml",
    "expected-gate-clauses.toml",
    "expected-gate-checks.toml",
)
WINDOWS_WORKFLOW = Path(".github/workflows/governance-oracles-windows.yml")


class GovernanceOracleTests(unittest.TestCase):
    def test_repository_oracles_match_the_approved_control_documents(self) -> None:
        self.assertEqual(validate_oracles(ROOT), ())

    def test_windows_workflow_matches_the_immutable_plan_contract(self) -> None:
        plan = (
            ROOT
            / "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md"
        ).read_text(encoding="utf-8")
        declaration = "Create `.github/workflows/governance-oracles-windows.yml` exactly as follows."
        start = plan.index("```yaml\n", plan.index(declaration)) + len("```yaml\n")
        end = plan.index("```", start)
        expected = plan[start:end]

        actual = (ROOT / WINDOWS_WORKFLOW).read_text(encoding="utf-8")

        self.assertEqual(actual, expected)
        for selector in ("3.9.13", "3.10.11", "3.11.9", "3.12.10", "3.13.14", "3.14.6"):
            self.assertEqual(actual.count(f'- "{selector}"'), 1)
        self.assertIn("actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0", actual)
        self.assertIn("actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1", actual)
        self.assertIn("persist-credentials: false", actual)
        self.assertIn(
            "tests.test_governance_oracles.GovernanceOracleTests."
            "test_windows_junction_component_is_rejected_without_skip",
            actual,
        )
        self.assertIn(
            "tests.test_governance_oracles.GovernanceOracleTests."
            "test_observed_windows_reparse_points_are_rejected_at_every_level",
            actual,
        )
        self.assertIn('run_zero_skip("tests.test_governance_oracles")', actual)
        self.assertIn("result.wasSuccessful() and skip_count == 0", actual)
        normalized = actual.casefold()
        for forbidden in (
            "continue-on-error",
            "upload-artifact",
            "cache:",
            " pip ",
            " uv ",
            "poetry",
            "coverage",
            "sarif",
            "telemetry",
            "analytics",
            "update check",
        ):
            self.assertNotIn(forbidden, normalized)

    def test_oracle_module_has_no_runtime_or_decorator_skips(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden_attributes = {
            "skip" + "Test",
            "skip" + "If",
            "skip" + "Unless",
            "skip",
        }
        offenders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in forbidden_attributes:
                    offenders.append((node.lineno, node.func.attr))
        self.assertEqual(offenders, [])

    def test_native_windows_junction_test_is_registered_only_on_windows(self) -> None:
        name = "test_windows_junction_component_is_rejected_without_skip"
        self.assertEqual(hasattr(type(self), name), os.name == "nt")

    def test_oracle_workflow_has_no_uninstalled_toml_dependency(self) -> None:
        forbidden = "import " + "tomli"
        for relative in (
            Path("scripts/governance/validate_oracles.py"),
            Path("tests/test_governance_oracles.py"),
        ):
            self.assertNotIn(forbidden, (ROOT / relative).read_text(encoding="utf-8"))

    def test_embedded_toml_fallback_matches_fixtures_and_rejects_duplicates(self) -> None:
        for relative in sorted((ROOT / "tests/fixtures/governance").glob("*.toml")):
            text = relative.read_text(encoding="utf-8")
            self.assertEqual(oracle_validator._parse_oracle_toml(text), tomllib.loads(text))
        with self.assertRaises(ValueError):
            oracle_validator._parse_oracle_toml("duplicate = 1\nduplicate = 2\n")

    def test_embedded_toml_fallback_rejects_noncanonical_and_unbounded_tokens(self) -> None:
        hostile_values = (
            "value = 01\n",
            'value = "a\\/b"\n',
            "value = " + ("9" * 5_000) + "\n",
        )
        for text in hostile_values:
            with self.subTest(text_length=len(text)), self.assertRaises(ValueError):
                oracle_validator._parse_oracle_toml(text)

    def test_embedded_toml_fallback_rejects_leading_zero_through_validation(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("scheduled_phase = 1", "scheduled_phase = 01", 1), encoding="utf-8")
            fallback = oracle_validator._OracleTomlCompatibility()
            with mock.patch.object(oracle_validator, "tomllib", fallback):
                codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("invalid-toml", codes)

    def test_embedded_toml_fallback_rejects_surrogate_without_escape(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace('"agent-skills-spec"', '"\\uD800"', 1), encoding="utf-8")
            output = io.StringIO()
            fallback = oracle_validator._OracleTomlCompatibility()
            with mock.patch.object(oracle_validator, "tomllib", fallback), redirect_stdout(output):
                exit_status = main([str(root)])

        self.assertEqual(exit_status, 1)
        self.assertIn("invalid-toml", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())
        self.assertNotIn(str(root), output.getvalue())

    def test_default_oracle_grammar_accepts_valid_cross_version_unicode_aliases(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    'schema_version = "provenance-source-oracle/v1"',
                    'schema_version = "\\U00000070rovenance-source-oracle/v1"',
                    1,
                ),
                encoding="utf-8",
            )

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertEqual(codes, set())

    def test_embedded_and_standard_toml_backends_agree_on_hostile_escape_corpus(self) -> None:
        valid = ('value = "\\U00000070"\n',)
        invalid = (
            "value = 01\n",
            'value = "a\\/b"\n',
            'value = "\\uD800"\n',
            'value = "\\U0000DFFF"\n',
            'value = "\\U00110000"\n',
        )
        fallback = oracle_validator._OracleTomlCompatibility()
        for text in valid:
            with self.subTest(kind="valid", text=text):
                self.assertEqual(fallback.loads(text), tomllib.loads(text))
        for text in invalid:
            with self.subTest(kind="invalid", text=text):
                with self.assertRaises(ValueError):
                    fallback.loads(text)
                with self.assertRaises(ValueError):
                    tomllib.loads(text)

    def test_missing_oracle_files_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            violations = validate_oracles(Path(directory))

        codes = {violation.code for violation in violations}
        self.assertIn("missing-oracle", codes)

    def test_duplicate_and_blank_line_ids_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-requirement-ids.txt"
            first = path.read_text(encoding="utf-8").splitlines()[0]
            path.write_text(f"{first}\n{first}\n\n", encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("blank-id", codes)
        self.assertIn("duplicate-id", codes)
        self.assertIn("wrong-count", codes)

    def test_unknown_ids_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-skill-ids.txt"
            lines = path.read_text(encoding="utf-8").splitlines()
            lines[-1] = "invented-skill"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("unknown-id", codes)

    def test_invalid_toml_shape_is_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
            path.write_text('schema_version = "governance-oracle/v1"\nsources = "wrong"\n', encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("invalid-shape", codes)

    def test_duplicate_toml_keys_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text + 'schema_version = "provenance-source-oracle/v1"\n',
                encoding="utf-8",
            )

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("invalid-toml", codes)

    def test_toml_integer_resource_error_is_controlled_and_sanitized(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
            path.write_text("schema_version = " + ("9" * 5_000) + "\n", encoding="utf-8")
            output = io.StringIO()
            try:
                with redirect_stdout(output):
                    exit_status = main([str(root)])
            except ValueError as error:
                self.fail(f"hostile TOML escaped validation: {error.__class__.__name__}")

        rendered = output.getvalue()
        self.assertEqual(exit_status, 1)
        self.assertIn("invalid-toml", rendered)
        self.assertNotIn("Traceback", rendered)
        self.assertNotIn(str(root), rendered)
        self.assertLessEqual(len(rendered), 512)

    def test_unrelated_parser_value_errors_are_not_masked(self) -> None:
        with self.oracle_copy() as directory, mock.patch.object(
            oracle_validator.tomllib,
            "loads",
            side_effect=ValueError("programmer defect"),
        ):
            with self.assertRaisesRegex(ValueError, "programmer defect"):
                validate_oracles(Path(directory))

    def test_deep_toml_nesting_is_rejected_before_parser_recursion(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
            path.write_text(
                "schema_version = " + ("[" * 500) + "0" + ("]" * 500) + "\n",
                encoding="utf-8",
            )
            output = io.StringIO()
            try:
                with redirect_stdout(output):
                    exit_status = main([str(root)])
            except RecursionError:
                self.fail("hostile TOML nesting escaped validation")

        self.assertEqual(exit_status, 1)
        self.assertIn("invalid-toml", output.getvalue())
        self.assertNotIn(str(root), output.getvalue())

    def test_unrelated_parser_recursion_errors_are_not_masked(self) -> None:
        with self.oracle_copy() as directory, mock.patch.object(
            oracle_validator.tomllib,
            "loads",
            side_effect=RecursionError("programmer recursion"),
        ):
            with self.assertRaisesRegex(RecursionError, "programmer recursion"):
                validate_oracles(Path(directory))

    def test_toml_multiline_quote_runs_cannot_bypass_nesting_limit(self) -> None:
        for quote in ('"', "'"):
            for run_length in (4, 5):
                with self.subTest(quote=quote, run_length=run_length), self.oracle_copy() as directory:
                    root = Path(directory)
                    path = root / "tests/fixtures/governance/expected-provenance-sources.toml"
                    path.write_text(
                        "note = "
                        + (quote * 3)
                        + "abc"
                        + (quote * run_length)
                        + "\nschema_version = "
                        + ("[" * 500)
                        + "0"
                        + ("]" * 500)
                        + "\n",
                        encoding="utf-8",
                    )
                    output = io.StringIO()
                    try:
                        with redirect_stdout(output):
                            exit_status = main([str(root)])
                    except RecursionError:
                        self.fail("multiline quote run bypassed TOML nesting limit")

                    self.assertEqual(exit_status, 1)
                    self.assertIn("invalid-toml", output.getvalue())

    def test_rendered_violations_have_a_deterministic_global_limit(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            header = path.read_text(encoding="utf-8").split("[[checks]]", 1)[0]
            path.write_text(header + ("[[checks]]\n" * 2_000), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                exit_status = main([str(root)])

        rendered = output.getvalue()
        self.assertEqual(exit_status, 1)
        self.assertLessEqual(len(rendered.encode("ascii")), 16_384)
        self.assertIn("output-truncated: additional violations omitted", rendered)

    def test_malformed_nested_requirement_edges_are_controlled_violations(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-clauses.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                'requirement_ids = ["ARC-04", ',
                'requirement_ids = [["ARC-04"], ',
                1,
            )
            path.write_text(text, encoding="utf-8")

            violations = validate_oracles(root)

        self.assertIn("invalid-shape", {violation.code for violation in violations})

    def test_reviewed_control_document_digest_change_invalidates_oracles(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "docs/design/proof-carrying-python-architecture.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("control-document-digest-mismatch", codes)

    def test_unresolved_source_section_and_digest_mismatch_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-clauses.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                'section = "G00 — Repository integrity and legal provenance"',
                'section = "missing section"',
                1,
            )
            first_digest = text.index('sha256 = "')
            second_digest = text.index('sha256 = "', first_digest + 1)
            text = text[:second_digest] + text[second_digest:].replace('sha256 = "', 'sha256 = "0', 1)
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("unresolved-section", codes)
        self.assertIn("clause-digest-mismatch", codes)

    def test_clause_source_cannot_escape_the_approved_document(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-clauses.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                'path = "docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md"',
                'path = "../../../../etc/passwd"',
                1,
            )
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("unresolved-source", codes)

    def test_clause_identity_cannot_be_substituted_with_another_gate(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-clauses.toml"
            text = path.read_text(encoding="utf-8")
            records = tomllib.loads(text)["clauses"]
            first, second = records[0], records[1]
            text = text.replace(
                f'section = "{first["section"]}"',
                f'section = "{second["section"]}"',
                1,
            ).replace(
                f'sha256 = "{first["sha256"]}"',
                f'sha256 = "{second["sha256"]}"',
                1,
            )
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("clause-identity-mismatch", codes)

    def test_schedule_artifacts_and_truth_projection_are_frozen(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace("scheduled_phase = 1", "scheduled_phase = 2", 1)
            text = text.replace(
                (
                    'expected_artifact_classes = ["gate_evidence", "legal_review", '
                    '"manifest", "provenance", "repository_state"]'
                ),
                'expected_artifact_classes = ["gate_evidence"]',
                1,
            )
            text = text.replace('truth_criteria = [', 'truth_criteria = ["applicability_independently_reviewed", ', 1)
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("schedule-mismatch", codes)
        self.assertIn("artifact-class-mismatch", codes)
        self.assertIn("truth-projection-mismatch", codes)

    def test_missing_gate_children_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            marker = '[[checks]]\ncheck_id = "G20-FINAL-CLAIM-AUTHORITY"'
            text = text[: text.index(marker)]
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("gate-child-inventory-mismatch", codes)

    def test_non_bidirectional_requirement_clause_edges_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace('clause_ids = ["validation:G00"]', 'clause_ids = ["validation:G01"]', 1)
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("clause-check-edge-mismatch", codes)

    def test_each_child_inherits_the_complete_gate_requirement_edges(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace('requirement_ids = ["ARC-04", ', 'requirement_ids = [', 1)
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("requirement-check-edge-mismatch", codes)

    def test_duplicate_requirement_edges_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                'requirement_ids = ["ARC-04", ',
                'requirement_ids = ["ARC-04", "ARC-04", ',
                1,
            )
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("duplicate-edge", codes)

    def test_requirement_edges_must_be_unique_and_utf8_sorted(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            for name in ("expected-gate-clauses.toml", "expected-gate-checks.toml"):
                path = root / "tests/fixtures/governance" / name
                text = path.read_text(encoding="utf-8")
                text = text.replace(
                    'requirement_ids = ["ARC-04", "DOC-01", ',
                    'requirement_ids = ["DOC-01", "ARC-04", ',
                    1,
                )
                path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("noncanonical-order", codes)

    if os.name != "nt" and hasattr(os, "symlink"):

        def test_control_and_fixture_inputs_reject_symlinks_and_nonregular_files(self) -> None:
            with self.oracle_copy() as directory:
                root = Path(directory)
                control = root / "docs/design/proof-carrying-python-architecture.md"
                control_copy = control.with_suffix(".real")
                control.rename(control_copy)
                control.symlink_to(control_copy.name)

                fixture = root / "tests/fixtures/governance/expected-skill-ids.txt"
                fixture.unlink()
                fixture.mkdir()

                violations = validate_oracles(root)

            self.assertGreaterEqual(
                sum(violation.code == "unsafe-input" for violation in violations),
                2,
            )
            rendered = "\n".join(
                f"{violation.path}:{violation.detail}" for violation in violations
            )
            self.assertNotIn(str(root), rendered)

    def test_observed_windows_reparse_points_are_rejected_at_every_level(self) -> None:
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

        class ReparseMetadata:
            def __init__(self, metadata: os.stat_result) -> None:
                self._metadata = metadata
                self.st_file_attributes = (
                    getattr(metadata, "st_file_attributes", 0) | reparse_flag
                )

            def __getattr__(self, name: str) -> object:
                return getattr(self._metadata, name)

        for marked_relative in (
            Path(),
            Path("docs/governance"),
            Path("docs/governance/requirements-traceability.md"),
        ):
            with self.subTest(path=str(marked_relative)), self.oracle_copy() as directory:
                root = Path(directory)
                marked = root / marked_relative
                real_lstat = Path.lstat

                def reparse_lstat(path: Path) -> os.stat_result | ReparseMetadata:
                    metadata = real_lstat(path)
                    return ReparseMetadata(metadata) if path == marked else metadata

                with mock.patch.object(Path, "lstat", new=reparse_lstat):
                    violations = validate_oracles(root)

            self.assertIn("unsafe-input", {violation.code for violation in violations})

    if os.name == "nt":

        def test_windows_junction_component_is_rejected_without_skip(self) -> None:
            with self.oracle_copy() as directory:
                root = Path(directory)
                component = root / "tests/fixtures/governance"
                target = component.with_name("governance-real")
                component.rename(target)
                command = f'mklink /J "{component}" "{target}"'
                completed = subprocess.run(
                    [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/s", "/c", command],
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                self.assertEqual(
                    completed.returncode,
                    0,
                    "required Windows matrix could not provision a junction fixture",
                )

                violations = validate_oracles(root)

            self.assertIn("unsafe-input", {violation.code for violation in violations})

    if os.name != "nt" and hasattr(os, "symlink"):

        def test_out_of_root_symlink_fixture_is_rejected_without_path_leak(self) -> None:
            with self.oracle_copy() as directory, tempfile.TemporaryDirectory() as outside:
                root = Path(directory)
                target = Path(outside) / "requirements.txt"
                target.write_text("ARC-01\n", encoding="utf-8")
                fixture = root / "tests/fixtures/governance/expected-requirement-ids.txt"
                fixture.unlink()
                fixture.symlink_to(target)

                violations = validate_oracles(root)

            self.assertIn("unsafe-input", {violation.code for violation in violations})
            self.assertNotIn(
                str(root),
                "\n".join(f"{item.path}:{item.detail}" for item in violations),
            )

    def test_portable_snapshot_fallback_remains_functional(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            real_open = os.open
            with mock.patch.object(
                oracle_validator.os,
                "supports_dir_fd",
                set(),
            ), mock.patch.object(
                oracle_validator.os,
                "O_DIRECTORY",
                0,
            ), mock.patch.object(
                oracle_validator.os,
                "O_NOFOLLOW",
                0,
            ), mock.patch.object(oracle_validator.os, "open", wraps=real_open) as pathname_open:
                violations = validate_oracles(root)

        self.assertGreater(pathname_open.call_count, 0)
        self.assertEqual(violations, ())

    if os.name != "nt" and hasattr(os, "symlink"):

        def test_portable_snapshot_rejects_persistent_same_inode_symlink_race(self) -> None:
            with self.oracle_copy() as directory:
                root = Path(directory)
                target = root / "tests/fixtures/governance/expected-skill-ids.txt"
                replacement = target.with_suffix(".real")
                real_open = os.open
                raced = False

                def racing_open(path: object, flags: int, *args: object, **kwargs: object) -> int:
                    nonlocal raced
                    candidate = Path(path) if isinstance(path, (str, os.PathLike)) else None
                    if not raced and candidate == target:
                        target.rename(replacement)
                        target.symlink_to(replacement.name)
                        raced = True
                    return real_open(path, flags, *args, **kwargs)  # type: ignore[arg-type]

                with mock.patch.object(
                    oracle_validator.os,
                    "supports_dir_fd",
                    set(),
                ), mock.patch.object(
                    oracle_validator.os,
                    "O_NOFOLLOW",
                    0,
                ), mock.patch.object(oracle_validator.os, "open", side_effect=racing_open):
                    violations = validate_oracles(root)

            self.assertTrue(raced)
            self.assertTrue(
                any(
                    violation.code == "unsafe-input"
                    and violation.path == "tests/fixtures/governance/expected-skill-ids.txt"
                    for violation in violations
                )
            )

    def test_openat_directory_descriptors_are_bound_to_lstat_identity(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            alternate = root / "alternate-directory"
            alternate.mkdir()
            real_open = os.open
            real_fstat = os.fstat
            governance_descriptors: set[int] = set()

            def tracking_open(
                path: object,
                flags: int,
                *args: object,
                **kwargs: object,
            ) -> int:
                descriptor = real_open(path, flags, *args, **kwargs)  # type: ignore[arg-type]
                if path == "governance" and kwargs.get("dir_fd") is not None:
                    governance_descriptors.add(descriptor)
                return descriptor

            def substituted_fstat(descriptor: int) -> os.stat_result:
                if descriptor in governance_descriptors:
                    return alternate.stat()
                return real_fstat(descriptor)

            with mock.patch.object(
                oracle_validator.os,
                "open",
                side_effect=tracking_open,
            ) as tracked_open, mock.patch.object(
                oracle_validator.os,
                "supports_dir_fd",
                {tracked_open},
            ), mock.patch.object(
                oracle_validator.os,
                "fstat",
                side_effect=substituted_fstat,
            ):
                violations = validate_oracles(root)

        self.assertTrue(governance_descriptors)
        self.assertTrue(
            any(
                violation.code == "unsafe-input"
                and violation.path.startswith("tests/fixtures/governance/")
                for violation in violations
            )
        )

    def test_same_inode_mutation_during_read_is_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            target = root / "tests/fixtures/governance/expected-skill-ids.txt"
            target_identity = (target.stat().st_dev, target.stat().st_ino)
            real_fdopen = os.fdopen
            mutated = False

            def mutating_fdopen(
                descriptor: int,
                *args: object,
                **kwargs: object,
            ) -> object:
                nonlocal mutated
                metadata = os.fstat(descriptor)
                if not mutated and (metadata.st_dev, metadata.st_ino) == target_identity:
                    with target.open("r+b", buffering=0) as writer:
                        writer.seek(0)
                        writer.write(b"X")
                        writer.flush()
                        os.fsync(writer.fileno())
                    mutated = True
                return real_fdopen(descriptor, *args, **kwargs)

            with mock.patch.object(
                oracle_validator.os,
                "fdopen",
                side_effect=mutating_fdopen,
            ):
                violations = validate_oracles(root)

        self.assertTrue(mutated)
        self.assertTrue(
            any(
                violation.code == "unsafe-input"
                and violation.path == "tests/fixtures/governance/expected-skill-ids.txt"
                for violation in violations
            )
        )

    def test_portable_snapshot_rejects_mutation_during_read(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            target = root / "tests/fixtures/governance/expected-skill-ids.txt"
            target_identity = (target.stat().st_dev, target.stat().st_ino)
            real_fdopen = os.fdopen
            mutated = False

            def mutating_fdopen(
                descriptor: int,
                *args: object,
                **kwargs: object,
            ) -> object:
                nonlocal mutated
                metadata = os.fstat(descriptor)
                if not mutated and (metadata.st_dev, metadata.st_ino) == target_identity:
                    with target.open("r+b", buffering=0) as writer:
                        writer.seek(0)
                        writer.write(b"X")
                        writer.flush()
                        os.fsync(writer.fileno())
                    mutated = True
                return real_fdopen(descriptor, *args, **kwargs)

            with mock.patch.object(
                oracle_validator.os,
                "supports_dir_fd",
                set(),
            ), mock.patch.object(
                oracle_validator.os,
                "O_NOFOLLOW",
                0,
            ), mock.patch.object(
                oracle_validator.os,
                "fdopen",
                side_effect=mutating_fdopen,
            ):
                violations = validate_oracles(root)

        self.assertTrue(mutated)
        self.assertTrue(
            any(
                violation.code == "unsafe-input"
                and violation.path == "tests/fixtures/governance/expected-skill-ids.txt"
                for violation in violations
            )
        )

    def test_control_plan_scopes_portable_snapshot_guarantees(self) -> None:
        text = (
            ROOT
            / "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(text.split())

        self.assertIn("### Post-publication Task -1 control amendment: Task 0 oracle portability", text)
        self.assertIn("portable snapshot mode", normalized)
        self.assertIn("does not provide atomic component containment", normalized)
        self.assertIn("cannot exclude transient namespace or component substitution", normalized)
        self.assertIn("no untrusted concurrent mutator", normalized)
        self.assertIn("Portable snapshot evidence is inadmissible", normalized)
        self.assertIn("`G13-HOSTILE-REPOSITORY` must `FAIL`", normalized)
        self.assertIn("green pinned Windows CI", normalized)
        self.assertIn("must remain functional on Linux, macOS, and Windows", normalized)

    def test_large_sparse_input_is_rejected_by_explicit_byte_limit(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            with path.open("r+b") as stream:
                stream.truncate(1_048_577)

            violations = validate_oracles(root)

        self.assertTrue(
            any(
                violation.code == "unsafe-input"
                and violation.path == "tests/fixtures/governance/expected-gate-checks.toml"
                and "byte limit" in violation.detail
                for violation in violations
            )
        )

    def test_every_descriptor_read_has_a_hard_byte_bound(self) -> None:
        read_limits: list[int] = []
        real_fdopen = os.fdopen

        class TrackingStream:
            def __init__(self, stream: object) -> None:
                self.stream = stream

            def __enter__(self) -> TrackingStream:
                self.stream.__enter__()  # type: ignore[attr-defined]
                return self

            def __exit__(self, *args: object) -> object:
                return self.stream.__exit__(*args)  # type: ignore[attr-defined]

            def read(self, size: int = -1) -> bytes:
                read_limits.append(size)
                return self.stream.read(size)  # type: ignore[attr-defined,no-any-return]

        def tracking_fdopen(
            descriptor: int,
            *args: object,
            **kwargs: object,
        ) -> TrackingStream:
            return TrackingStream(real_fdopen(descriptor, *args, **kwargs))

        with mock.patch.object(oracle_validator.os, "fdopen", side_effect=tracking_fdopen):
            self.assertEqual(validate_oracles(ROOT), ())

        self.assertTrue(read_limits)
        self.assertEqual(set(read_limits), {oracle_validator.MAX_INPUT_BYTES + 1})

    def test_control_digest_tamper_stops_derivation_without_traceback_or_path_leak(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "docs/governance/requirements-traceability.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace("| G00, G13, G19 |", "| G99, G13, G19 |", 1),
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                exit_status = main([str(root)])

        self.assertEqual(exit_status, 1)
        self.assertIn("control-document-digest-mismatch", output.getvalue())
        self.assertNotIn(str(root), output.getvalue())

    def test_hostile_fixture_identifiers_are_not_rendered(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            hostile = "G00-/private/sensitive/path\\u001b[31m"
            text = text.replace("G00-CLEAN-TREE", hostile, 1)
            text = text.replace('requirement_ids = ["ARC-04", ', 'requirement_ids = [', 1)
            path.write_text(text, encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                exit_status = main([str(root)])

        self.assertEqual(exit_status, 1)
        self.assertNotIn("/private/sensitive/path", output.getvalue())
        self.assertNotIn("\x1b", output.getvalue())

    if os.name != "nt" and hasattr(os, "symlink"):

        def test_root_symlink_loop_is_a_controlled_relative_violation(self) -> None:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "loop"
                root.symlink_to(root)
                output = io.StringIO()
                with redirect_stdout(output):
                    exit_status = main([str(root)])

            self.assertEqual(exit_status, 1)
            self.assertIn("unsafe-input", output.getvalue())
            self.assertNotIn(str(root), output.getvalue())

    def test_component_loop_raced_before_resolve_is_a_controlled_violation(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            real_resolve = Path.resolve
            resolve_calls = 0

            def racing_resolve(path: Path, *args: object, **kwargs: object) -> Path:
                nonlocal resolve_calls
                resolve_calls += 1
                if resolve_calls == 2:
                    raise RuntimeError("symlink loop raced")
                return real_resolve(path, *args, **kwargs)

            try:
                with mock.patch.object(Path, "resolve", new=racing_resolve):
                    violations = validate_oracles(root)
            except RuntimeError:
                self.fail("component resolution race escaped validation")

        self.assertGreaterEqual(resolve_calls, 2)
        self.assertIn("unsafe-input", {violation.code for violation in violations})

    def test_state_conditional_truth_and_external_blockers_are_frozen(self) -> None:
        data = tomllib.loads(
            (ROOT / "tests/fixtures/governance/expected-gate-checks.toml").read_text(
                encoding="utf-8"
            )
        )
        state_truth = data.get("state_truth", {})
        self.assertIn("predeclared_machine_fact_false", state_truth.get("NOT_APPLICABLE", []))
        self.assertIn(
            "applicability_independently_reviewed",
            state_truth.get("NOT_APPLICABLE", []),
        )
        self.assertIn("external_blocker_evidenced", state_truth.get("BLOCKED", []))
        self.assertEqual(
            set(data.get("externally_blockable_check_ids", [])),
            {
                "G00-LEGAL-PERMISSION",
                "G05-INSTALLED-WHEEL-CELLS",
                "G05-PR-MATRIX",
                "G05-RELEASE-MATRIX",
                "G11-MODEL-TRIALS",
                "G12-PLATFORM-CONTAINMENT",
                "G20-POST-PUBLISH-SMOKE",
                "G20-REMOTE-TREE-PARITY",
            },
        )

    def test_state_truth_and_external_blocker_mutations_are_rejected(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            marker = '"predeclared_machine_fact_false", '
            first = text.index(marker)
            second = text.index(marker, first + len(marker))
            text = text[:second] + text[second:].replace(marker, "", 1)
            text = text.replace('"G11-MODEL-TRIALS", ', "", 1)
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("state-truth-mismatch", codes)
        self.assertIn("external-blocker-inventory-mismatch", codes)

    def test_check_records_preserve_the_declared_task_nine_order(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            first_start = text.index("[[checks]]")
            second_start = text.index("[[checks]]", first_start + 1)
            third_start = text.index("[[checks]]", second_start + 1)
            first = text[first_start:second_start]
            second = text[second_start:third_start]
            text = text[:first_start] + second + first + text[third_start:]
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("noncanonical-order", codes)

    def test_truth_criteria_are_closed(self) -> None:
        with self.oracle_copy() as directory:
            root = Path(directory)
            path = root / "tests/fixtures/governance/expected-gate-checks.toml"
            text = path.read_text(encoding="utf-8")
            text = text.replace('truth_criteria = [', 'truth_criteria = ["trust-me", ', 1)
            path.write_text(text, encoding="utf-8")

            codes = {violation.code for violation in validate_oracles(root)}

        self.assertIn("unknown-truth-criterion", codes)

    def oracle_copy(self) -> tempfile.TemporaryDirectory[str]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for relative in (
            "docs/governance/requirements-traceability.md",
            "docs/design/proof-carrying-python-architecture.md",
            "docs/superpowers/specs/2026-07-14-python-doctor-complete-parity-design.md",
            "docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md",
            "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md",
        ):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        fixture_root = root / "tests/fixtures/governance"
        fixture_root.mkdir(parents=True)
        for name in FIXTURE_PATHS:
            shutil.copy2(ROOT / "tests/fixtures/governance" / name, fixture_root / name)
        return temporary


if __name__ == "__main__":
    unittest.main()
