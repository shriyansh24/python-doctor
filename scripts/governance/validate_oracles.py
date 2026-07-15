from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


class _TomlDecodeError(ValueError):
    pass


class _OracleTomlCompatibility:
    TOMLDecodeError = _TomlDecodeError

    @staticmethod
    def loads(text: str) -> dict[str, Any]:
        return _parse_oracle_toml(text)


tomllib = _OracleTomlCompatibility()


ORACLE_ROOT = Path("tests/fixtures/governance")
REQUIREMENTS_PATH = Path("docs/governance/requirements-traceability.md")
ARCHITECTURE_PATH = Path("docs/design/proof-carrying-python-architecture.md")
DESIGN_PATH = Path("docs/superpowers/specs/2026-07-14-python-doctor-complete-parity-design.md")
GATES_PATH = Path("docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md")
PLAN_PATH = Path("docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md")
CONTROL_DOCUMENT_SHA256 = {
    REQUIREMENTS_PATH: "6ae0740c6ad9fdd47b575d8f6ce2501a295f7d017109239e8afd58ea368a0b90",
    ARCHITECTURE_PATH: "1c4e336937e697846270c190fe39c203c04600ef2fb5251a7b1e5ba304059c01",
    DESIGN_PATH: "fb8b5585a8f7ff40dde5c533939af9ebb06df471e8408c19c3f1f1b163c403ec",
    GATES_PATH: "6b43e708bbd3b3e07150bd59cdfdc291f0b5ab067804935c163af1b24ab29abf",
    PLAN_PATH: "11642923cfcbbb0226482c85d103913779da95f1ba9296b974aa130d1d84bed3",
}

EXPECTED_COUNTS = {
    "expected-requirement-ids.txt": 105,
    "expected-skill-ids.txt": 198,
    "expected-profile-domain-ids.txt": 9,
}
TRUTH_CRITERIA = frozenset(
    {
        "applicability_independently_reviewed",
        "candidate_identity_matches",
        "child_outcome_success",
        "expected_artifacts_present_and_hashed",
        "external_blocker_evidenced",
        "predeclared_machine_fact_false",
        "process_exit_zero",
        "required_tools_verified",
        "source_clause_digest_matches",
        "structured_child_result_valid",
        "zero_unexpected_counts",
    }
)
ARTIFACT_CLASSES = frozenset(
    {
        "artifact_identity",
        "attestation",
        "benchmark",
        "build_artifact",
        "compatibility_matrix",
        "coverage",
        "documentation",
        "gate_evidence",
        "legal_review",
        "manifest",
        "mutation_report",
        "network_trace",
        "package_install",
        "provenance",
        "repository_state",
        "review_findings",
        "schema_validation",
        "skill_evaluation",
        "test_report",
    }
)
GATE_DEFAULT_PHASES = {
    "G00": 1,
    "G01": 3,
    "G02": 1,
    "G03": 2,
    "G04": 3,
    "G05": 5,
    "G06": 4,
    "G07": 10,
    "G08": 10,
    "G09": 2,
    "G10": 10,
    "G11": 8,
    "G12": 3,
    "G13": 13,
    "G14": 12,
    "G15": 13,
    "G16": 11,
    "G17": 13,
    "G18": 10,
    "G19": 1,
    "G20": 14,
}
CHECK_PHASE_OVERRIDES = {
    "G02-COLLECTION-MANIFEST": 2,
    "G02-COVERAGE-THRESHOLDS": 3,
    "G02-CRITICAL-BRANCH-COVERAGE": 3,
    "G02-CHANGED-CRITICAL-MUTATION": 3,
    "G03-ENGINE-PARITY": 3,
    "G04-SCHEMAS": 1,
    "G04-CLI-GOLDENS": 7,
    "G05-TARGET-GRAMMARS": 3,
    "G06-PRECISION-THRESHOLDS": 10,
    "G06-SAFETY-RECALL": 6,
    "G09-ANALYZER-FAILURES": 4,
    "G09-FIX-ROLLBACK-CONCURRENCY": 3,
    "G09-PARTIAL-NEVER-CLEAN": 3,
    "G11-PRESSURE-GUARDRAILS": 9,
    "G11-EVAL-MANIFEST": 9,
    "G11-DETERMINISTIC-SCORER": 9,
    "G11-MODEL-TRIALS": 9,
    "G12-FORBIDDEN-CAPABILITIES": 1,
    "G12-NETWORK-PARITY": 10,
    "G12-EXTENSION-PROCESS-BOUNDARY": 11,
    "G13-THREAT-MODELS": 1,
    "G13-HOSTILE-REPOSITORY": 4,
    "G13-RESTRICTED-ARTIFACT-EXCLUSION": 1,
    "G14-FORBIDDEN-CLAIMS": 1,
    "G18-LSP-BUDGETS": 11,
}
GATE_ARTIFACT_CLASSES = {
    "G00": ("gate_evidence", "legal_review", "manifest", "provenance", "repository_state"),
    "G01": ("gate_evidence", "test_report"),
    "G02": ("coverage", "gate_evidence", "mutation_report", "test_report"),
    "G03": ("gate_evidence", "package_install", "test_report"),
    "G04": ("gate_evidence", "schema_validation", "test_report"),
    "G05": ("compatibility_matrix", "gate_evidence", "package_install", "test_report"),
    "G06": ("gate_evidence", "test_report"),
    "G07": ("gate_evidence", "test_report"),
    "G08": ("gate_evidence", "mutation_report"),
    "G09": ("gate_evidence", "package_install", "test_report"),
    "G10": ("benchmark", "gate_evidence", "provenance", "test_report"),
    "G11": ("gate_evidence", "skill_evaluation", "test_report"),
    "G12": ("gate_evidence", "network_trace", "test_report"),
    "G13": ("gate_evidence", "manifest", "provenance", "test_report"),
    "G14": ("documentation", "gate_evidence", "test_report"),
    "G15": ("artifact_identity", "build_artifact", "gate_evidence", "package_install"),
    "G16": ("build_artifact", "gate_evidence", "test_report"),
    "G17": ("gate_evidence", "test_report"),
    "G18": ("benchmark", "gate_evidence", "test_report"),
    "G19": ("gate_evidence", "review_findings"),
    "G20": ("artifact_identity", "attestation", "gate_evidence"),
}
COMMON_TRUTH_PROJECTION = (
    "candidate_identity_matches",
    "child_outcome_success",
    "expected_artifacts_present_and_hashed",
    "process_exit_zero",
    "required_tools_verified",
    "source_clause_digest_matches",
    "structured_child_result_valid",
    "zero_unexpected_counts",
)
STATE_TRUTH_PROJECTIONS = {
    "PASS": COMMON_TRUTH_PROJECTION,
    "NOT_APPLICABLE": (
        "applicability_independently_reviewed",
        "candidate_identity_matches",
        "predeclared_machine_fact_false",
        "source_clause_digest_matches",
        "structured_child_result_valid",
    ),
    "BLOCKED": (
        "candidate_identity_matches",
        "external_blocker_evidenced",
        "source_clause_digest_matches",
        "structured_child_result_valid",
    ),
}
EXTERNALLY_BLOCKABLE_CHECK_IDS = (
    "G00-LEGAL-PERMISSION",
    "G05-INSTALLED-WHEEL-CELLS",
    "G05-PR-MATRIX",
    "G05-RELEASE-MATRIX",
    "G11-MODEL-TRIALS",
    "G12-PLATFORM-CONTAINMENT",
    "G20-POST-PUBLISH-SMOKE",
    "G20-REMOTE-TREE-PARITY",
)
MAX_INPUT_BYTES = 1_048_576
MAX_TOML_NESTING = 64
MAX_TOML_INTEGER_DIGITS = 64
MAX_RENDERED_OUTPUT_BYTES = 16_384
OUTPUT_TRUNCATION_MARKER = "output-truncated: additional violations omitted"


def _parse_oracle_toml(text: str) -> dict[str, Any]:
    """Parse the deliberately narrow TOML grammar used by frozen Task 0 fixtures."""
    document: dict[str, Any] = {}
    current = document
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[[") and line.endswith("]]"):
            table_name = line[2:-2].strip()
            if not re.fullmatch(r"[A-Za-z0-9_-]+", table_name):
                raise _TomlDecodeError("invalid array table")
            existing = document.setdefault(table_name, [])
            if not isinstance(existing, list):
                raise _TomlDecodeError("table conflicts with key")
            current = {}
            existing.append(current)
            continue
        if "=" not in line:
            raise _TomlDecodeError("expected key/value assignment")
        key, raw_value = (part.strip() for part in line.split("=", 1))
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key) or key in current:
            raise _TomlDecodeError("invalid or duplicate key")
        current[key] = _parse_oracle_toml_value(raw_value)
    return document


def _parse_oracle_toml_value(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return _decode_oracle_basic_string(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_oracle_toml_value(item) for item in _split_oracle_toml(inner)]
    if value.startswith("{") and value.endswith("}"):
        result: dict[str, Any] = {}
        inner = value[1:-1].strip()
        for item in _split_oracle_toml(inner):
            if "=" not in item:
                raise _TomlDecodeError("invalid inline table")
            key, nested = (part.strip() for part in item.split("=", 1))
            if not re.fullmatch(r"[A-Za-z0-9_-]+", key) or key in result:
                raise _TomlDecodeError("invalid or duplicate inline key")
            result[key] = _parse_oracle_toml_value(nested)
        return result
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"[+-]?(?:0|[1-9][0-9]*)", value):
        digits = value.lstrip("+-")
        if len(digits) > MAX_TOML_INTEGER_DIGITS:
            raise _TomlDecodeError("integer exceeds digit limit")
        try:
            return int(value)
        except ValueError as error:
            raise _TomlDecodeError("invalid integer") from error
    raise _TomlDecodeError("unsupported TOML value")


def _decode_oracle_basic_string(value: str) -> str:
    decoded: list[str] = []
    index = 1
    final_quote = len(value) - 1
    while index < final_quote:
        character = value[index]
        codepoint = ord(character)
        if character == '"' or codepoint < 0x20 or 0xD800 <= codepoint <= 0xDFFF:
            raise _TomlDecodeError("invalid string character")
        if character != "\\":
            decoded.append(character)
            index += 1
            continue
        if index + 1 >= final_quote:
            raise _TomlDecodeError("unterminated string escape")
        escape = value[index + 1]
        simple_escapes = {
            '"': '"',
            "\\": "\\",
            "b": "\b",
            "f": "\f",
            "n": "\n",
            "r": "\r",
            "t": "\t",
        }
        if escape in simple_escapes:
            decoded.append(simple_escapes[escape])
            index += 2
            continue
        if escape in {"u", "U"}:
            width = 4 if escape == "u" else 8
            encoded = value[index + 2 : index + 2 + width]
            if len(encoded) != width or re.fullmatch(
                rf"[0-9A-Fa-f]{{{width}}}", encoded
            ) is None:
                raise _TomlDecodeError("invalid unicode escape")
            scalar = int(encoded, 16)
            if scalar > 0x10FFFF or 0xD800 <= scalar <= 0xDFFF:
                raise _TomlDecodeError("unicode escape is not a scalar value")
            decoded.append(chr(scalar))
            index += 2 + width
            continue
        raise _TomlDecodeError("unsupported string escape")
    return "".join(decoded)


def _split_oracle_toml(text: str) -> list[str]:
    items: list[str] = []
    start = 0
    depth = 0
    quote = ""
    escaped = False
    for index, character in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif quote == '"' and character == "\\":
                escaped = True
            elif character == quote:
                quote = ""
            continue
        if character in {'"', "'"}:
            quote = character
        elif character in "[{":
            depth += 1
        elif character in "]}":
            depth -= 1
            if depth < 0:
                raise _TomlDecodeError("unbalanced container")
        elif character == "," and depth == 0:
            item = text[start:index].strip()
            if not item:
                raise _TomlDecodeError("empty value")
            items.append(item)
            start = index + 1
    if quote or depth:
        raise _TomlDecodeError("unterminated value")
    final = text[start:].strip()
    if not final:
        raise _TomlDecodeError("empty value")
    items.append(final)
    return items


@dataclass(frozen=True, order=True)
class OracleViolation:
    code: str
    path: str
    detail: str


def validate_oracles(root: Path) -> tuple[OracleViolation, ...]:
    try:
        root_metadata = root.lstat()
        if _is_link_or_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
            return (
                OracleViolation("unsafe-input", ".", "root is not a regular directory"),
            )
        root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        return (OracleViolation("unsafe-input", ".", "root cannot be safely resolved"),)
    violations: list[OracleViolation] = []
    documents = _load_control_documents(root, violations)
    if any(
        violation.code == "control-document-digest-mismatch"
        for violation in violations
    ):
        return tuple(sorted(set(violations)))

    requirements = _validate_id_file(
        root,
        "expected-requirement-ids.txt",
        _derive_requirement_ids(documents.get(REQUIREMENTS_PATH, "")),
        violations,
    )
    _validate_id_file(
        root,
        "expected-skill-ids.txt",
        _derive_skill_ids(documents.get(DESIGN_PATH, "")),
        violations,
    )
    _validate_id_file(
        root,
        "expected-profile-domain-ids.txt",
        _derive_profile_ids(documents.get(PLAN_PATH, "")),
        violations,
    )

    provenance = _load_toml(root, "expected-provenance-sources.toml", violations)
    _validate_provenance(provenance, documents.get(PLAN_PATH, ""), requirements, violations)

    clauses = _load_toml(root, "expected-gate-clauses.toml", violations)
    clause_records = _validate_clauses(
        root,
        clauses,
        requirements,
        _derive_gate_requirements(documents.get(REQUIREMENTS_PATH, "")),
        documents.get(GATES_PATH, ""),
        violations,
    )

    checks = _load_toml(root, "expected-gate-checks.toml", violations)
    _validate_checks(
        checks,
        documents.get(PLAN_PATH, ""),
        requirements,
        clause_records,
        violations,
    )
    return tuple(sorted(set(violations)))


def _load_control_documents(
    root: Path, violations: list[OracleViolation]
) -> dict[Path, str]:
    documents: dict[Path, str] = {}
    for relative in (REQUIREMENTS_PATH, ARCHITECTURE_PATH, DESIGN_PATH, GATES_PATH, PLAN_PATH):
        raw = _read_regular_bytes(
            root,
            relative,
            violations,
            missing_code="missing-control-document",
        )
        if raw is None:
            continue
        try:
            documents[relative] = raw.decode("utf-8")
        except UnicodeError:
            violations.append(
                OracleViolation(
                    "unsafe-input",
                    str(relative),
                    "input is not valid UTF-8",
                )
            )
            continue
        digest = hashlib.sha256(raw).hexdigest()
        if digest != CONTROL_DOCUMENT_SHA256[relative]:
            violations.append(
                OracleViolation(
                    "control-document-digest-mismatch",
                    str(relative),
                    digest,
                )
            )
    return documents


def _validate_id_file(
    root: Path,
    name: str,
    expected: tuple[str, ...],
    violations: list[OracleViolation],
) -> tuple[str, ...]:
    relative = ORACLE_ROOT / name
    raw = _read_regular_bytes(
        root,
        relative,
        violations,
        missing_code="missing-oracle",
    )
    if raw is None:
        return ()
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        violations.append(
            OracleViolation("unsafe-input", str(relative), "input is not valid UTF-8")
        )
        return ()

    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if any(not line for line in lines):
        violations.append(OracleViolation("blank-id", str(relative), "blank ID line"))
    nonblank = tuple(line for line in lines if line)
    if len(nonblank) != len(set(nonblank)):
        violations.append(OracleViolation("duplicate-id", str(relative), "duplicate ID"))
    if len(nonblank) != EXPECTED_COUNTS[name]:
        violations.append(
            OracleViolation(
                "wrong-count",
                str(relative),
                f"expected {EXPECTED_COUNTS[name]}, found {len(nonblank)}",
            )
        )
    if nonblank != tuple(sorted(nonblank, key=lambda value: value.encode("utf-8"))):
        violations.append(OracleViolation("noncanonical-order", str(relative), "IDs are not byte-sorted"))
    if set(nonblank) != set(expected):
        unknown = sorted(set(nonblank) - set(expected))
        missing = sorted(set(expected) - set(nonblank))
        violations.append(
            OracleViolation(
                "unknown-id",
                str(relative),
                f"unknown_count={len(unknown)}; missing_count={len(missing)}",
            )
        )
    return nonblank


def _load_toml(
    root: Path, name: str, violations: list[OracleViolation]
) -> Mapping[str, Any] | None:
    relative = ORACLE_ROOT / name
    raw = _read_regular_bytes(
        root,
        relative,
        violations,
        missing_code="missing-oracle",
    )
    if raw is None:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        violations.append(
            OracleViolation("unsafe-input", str(relative), "input is not valid UTF-8")
        )
        return None
    if _toml_nesting_exceeds_limit(text):
        violations.append(
            OracleViolation("invalid-toml", str(relative), "TOML nesting exceeds limit")
        )
        return None
    try:
        value = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        violations.append(OracleViolation("invalid-toml", str(relative), "TOML parse failed"))
        return None
    except ValueError as error:
        if not _is_toml_integer_limit_error(error):
            raise
        violations.append(
            OracleViolation("invalid-toml", str(relative), "TOML numeric value exceeds limit")
        )
        return None
    if not isinstance(value, dict):
        violations.append(OracleViolation("invalid-shape", str(relative), "root must be a table"))
        return None
    return value


def _validate_provenance(
    data: Mapping[str, Any] | None,
    plan: str,
    requirement_ids: Sequence[str],
    violations: list[OracleViolation],
) -> None:
    del requirement_ids
    path = str(ORACLE_ROOT / "expected-provenance-sources.toml")
    if data is None:
        return
    if set(data) != {"schema_version", "required_record_fields", "source_ids"}:
        violations.append(OracleViolation("invalid-shape", path, "unexpected provenance root keys"))
        return
    if data.get("schema_version") != "provenance-source-oracle/v1":
        violations.append(OracleViolation("invalid-shape", path, "wrong schema_version"))
    fields = data.get("required_record_fields")
    expected_fields = (
        "source_id",
        "url",
        "immutable_revision",
        "license_id",
        "license_path",
        "license_sha256",
        "inspected_paths",
        "concepts",
        "disposition",
        "attribution",
    )
    if fields != list(expected_fields):
        violations.append(OracleViolation("invalid-shape", path, "wrong required record fields"))
    source_ids = data.get("source_ids")
    if not _is_string_list(source_ids):
        violations.append(OracleViolation("invalid-shape", path, "source_ids must be strings"))
        return
    expected_ids = _derive_provenance_ids(plan)
    if tuple(source_ids) != tuple(sorted(source_ids, key=lambda value: value.encode("utf-8"))):
        violations.append(OracleViolation("noncanonical-order", path, "source IDs are not byte-sorted"))
    if len(source_ids) != len(set(source_ids)):
        violations.append(OracleViolation("duplicate-id", path, "duplicate source ID"))
    if set(source_ids) != set(expected_ids):
        violations.append(OracleViolation("unknown-id", path, "provenance source inventory differs"))


def _validate_clauses(
    root: Path,
    data: Mapping[str, Any] | None,
    requirement_ids: Sequence[str],
    expected_gate_requirements: Mapping[str, set[str]],
    gates_text: str,
    violations: list[OracleViolation],
) -> dict[str, Mapping[str, Any]]:
    oracle_path = str(ORACLE_ROOT / "expected-gate-clauses.toml")
    if data is None:
        return {}
    if set(data) != {"schema_version", "normalization", "hash_domain", "clauses"}:
        violations.append(OracleViolation("invalid-shape", oracle_path, "unexpected clause root keys"))
        return {}
    if (
        data.get("schema_version") != "gate-clause-oracle/v1"
        or data.get("normalization") != "markdown-section-v1"
        or data.get("hash_domain") != "python-doctor/clause/v1"
    ):
        violations.append(OracleViolation("invalid-shape", oracle_path, "wrong clause schema or normalization"))
    records = data.get("clauses")
    if not isinstance(records, list):
        violations.append(OracleViolation("invalid-shape", oracle_path, "clauses must be an array of tables"))
        return {}
    by_id: dict[str, Mapping[str, Any]] = {}
    expected_keys = {"clause_id", "path", "section", "sha256", "assertion_kind", "requirement_ids"}
    known_requirements = set(requirement_ids)
    for index, record in enumerate(records):
        record_path = f"{oracle_path}:clauses[{index}]"
        if not isinstance(record, dict) or set(record) != expected_keys:
            violations.append(OracleViolation("invalid-shape", record_path, "wrong clause fields"))
            continue
        clause_id = record.get("clause_id")
        if not isinstance(clause_id, str) or not clause_id:
            violations.append(OracleViolation("invalid-shape", record_path, "invalid clause_id"))
            continue
        if clause_id in by_id:
            violations.append(
                OracleViolation("duplicate-id", record_path, "duplicate clause ID")
            )
        by_id[clause_id] = record
        if record.get("assertion_kind") != "normative_gate_section":
            violations.append(OracleViolation("invalid-shape", record_path, "invalid assertion_kind"))
        requirement_edges = record.get("requirement_ids")
        valid_requirement_edges = _is_string_list(requirement_edges)
        if not valid_requirement_edges:
            violations.append(OracleViolation("invalid-shape", record_path, "requirement edges must be strings"))
        elif not set(requirement_edges) <= known_requirements:
            violations.append(OracleViolation("unknown-id", record_path, "unknown requirement edge"))
        elif len(requirement_edges) != len(set(requirement_edges)):
            violations.append(OracleViolation("duplicate-edge", record_path, "duplicate requirement edge"))
        elif requirement_edges != sorted(
            requirement_edges, key=lambda value: value.encode("utf-8")
        ):
            violations.append(
                OracleViolation(
                    "noncanonical-order",
                    record_path,
                    "requirement edges are not UTF-8 sorted",
                )
            )
        gate_id = clause_id.removeprefix("validation:")
        if valid_requirement_edges and set(requirement_edges) != expected_gate_requirements.get(gate_id, set()):
            violations.append(
                OracleViolation(
                    "requirement-clause-edge-mismatch",
                    record_path,
                    "clause requirement edges differ",
                )
            )
        relative = record.get("path")
        section = record.get("section")
        if not isinstance(relative, str) or not isinstance(section, str):
            violations.append(OracleViolation("invalid-shape", record_path, "path/section must be strings"))
            continue
        if relative != str(GATES_PATH):
            violations.append(
                OracleViolation("unresolved-source", record_path, "clause path is not the approved gates document")
            )
            continue
        text = gates_text
        if not text:
            violations.append(
                OracleViolation("unresolved-source", record_path, "approved source is unavailable")
            )
            continue
        heading = re.search(rf"^### {re.escape(gate_id)} — (.+)$", text, flags=re.MULTILINE)
        expected_section = f"{gate_id} — {heading.group(1)}" if heading else None
        if section != expected_section:
            violations.append(
                OracleViolation(
                    "clause-identity-mismatch",
                    record_path,
                    "clause identity differs",
                )
            )
        normalized = _normalized_section(text, section)
        if normalized is None:
            violations.append(
                OracleViolation("unresolved-section", record_path, "section not found")
            )
            continue
        digest = hashlib.sha256(
            b"python-doctor/clause/v1\0" + normalized.encode("utf-8")
        ).hexdigest()
        if record.get("sha256") != digest:
            violations.append(OracleViolation("clause-digest-mismatch", record_path, digest))
    expected_ids = {f"validation:G{number:02d}" for number in range(21)}
    if set(by_id) != expected_ids:
        violations.append(OracleViolation("clause-inventory-mismatch", oracle_path, "expected validation:G00..G20"))
    expected_order = tuple(f"validation:G{number:02d}" for number in range(21))
    if tuple(by_id) != expected_order:
        violations.append(OracleViolation("noncanonical-order", oracle_path, "clauses must be in G00..G20 order"))
    return by_id


def _validate_checks(
    data: Mapping[str, Any] | None,
    plan: str,
    requirement_ids: Sequence[str],
    clauses: Mapping[str, Mapping[str, Any]],
    violations: list[OracleViolation],
) -> None:
    path = str(ORACLE_ROOT / "expected-gate-checks.toml")
    if data is None:
        return
    if set(data) != {
        "schema_version",
        "order",
        "truth_criteria_registry",
        "artifact_class_registry",
        "state_truth",
        "externally_blockable_check_ids",
        "checks",
    }:
        violations.append(OracleViolation("invalid-shape", path, "unexpected check root keys"))
        return
    if data.get("schema_version") != "gate-check-oracle/v1":
        violations.append(OracleViolation("invalid-shape", path, "wrong check schema_version"))
    if data.get("order") != "task-09-source-order":
        violations.append(OracleViolation("invalid-shape", path, "wrong check record order contract"))
    if data.get("truth_criteria_registry") != sorted(TRUTH_CRITERIA):
        violations.append(OracleViolation("invalid-shape", path, "truth criteria registry differs"))
    if data.get("artifact_class_registry") != sorted(ARTIFACT_CLASSES):
        violations.append(OracleViolation("invalid-shape", path, "artifact class registry differs"))
    state_truth = data.get("state_truth")
    expected_state_truth = {
        state: list(criteria) for state, criteria in STATE_TRUTH_PROJECTIONS.items()
    }
    if state_truth != expected_state_truth:
        violations.append(
            OracleViolation("state-truth-mismatch", path, "state truth projection differs")
        )
    externally_blockable = data.get("externally_blockable_check_ids")
    if externally_blockable != list(EXTERNALLY_BLOCKABLE_CHECK_IDS):
        violations.append(
            OracleViolation(
                "external-blocker-inventory-mismatch",
                path,
                "externally blockable child inventory differs",
            )
        )
    records = data.get("checks")
    if not isinstance(records, list):
        violations.append(OracleViolation("invalid-shape", path, "checks must be an array of tables"))
        return
    expected_keys = {
        "check_id",
        "gate_id",
        "required",
        "scheduled_phase",
        "schedule_state",
        "requirement_ids",
        "clause_ids",
        "truth_criteria",
        "expected_artifact_classes",
    }
    by_id: dict[str, Mapping[str, Any]] = {}
    known_requirements = set(requirement_ids)
    check_requirement_edges: dict[str, set[str]] = {}
    check_clause_edges: dict[str, set[str]] = {}
    for index, record in enumerate(records):
        record_path = f"{path}:checks[{index}]"
        if not isinstance(record, dict) or set(record) != expected_keys:
            violations.append(OracleViolation("invalid-shape", record_path, "wrong check fields"))
            continue
        check_id = record.get("check_id")
        gate_id = record.get("gate_id")
        if not isinstance(check_id, str) or not isinstance(gate_id, str) or not check_id.startswith(f"{gate_id}-"):
            violations.append(OracleViolation("invalid-shape", record_path, "check/gate identity mismatch"))
            continue
        if check_id in by_id:
            violations.append(
                OracleViolation("duplicate-id", record_path, "duplicate check ID")
            )
        by_id[check_id] = record
        if record.get("required") is not True:
            violations.append(OracleViolation("invalid-shape", record_path, "normative child must be required"))
        phase = record.get("scheduled_phase")
        state = record.get("schedule_state")
        if not isinstance(phase, int) or isinstance(phase, bool) or phase not in range(1, 15):
            violations.append(OracleViolation("invalid-shape", record_path, "invalid scheduled_phase"))
        if state not in {"scheduled", "planned"}:
            violations.append(OracleViolation("invalid-shape", record_path, "invalid schedule_state"))
        expected_phase = CHECK_PHASE_OVERRIDES.get(check_id, GATE_DEFAULT_PHASES.get(gate_id))
        expected_state = "scheduled" if expected_phase == 1 else "planned"
        if phase != expected_phase or state != expected_state:
            violations.append(
                OracleViolation("schedule-mismatch", record_path, "schedule differs")
            )
        reqs = record.get("requirement_ids")
        clause_ids = record.get("clause_ids")
        truth = record.get("truth_criteria")
        artifacts = record.get("expected_artifact_classes")
        if not _is_nonempty_string_list(reqs) or not set(reqs) <= known_requirements:
            violations.append(OracleViolation("unknown-id", record_path, "invalid requirement IDs"))
            reqs = []
        elif len(reqs) != len(set(reqs)):
            violations.append(OracleViolation("duplicate-edge", record_path, "duplicate requirement edge"))
        elif reqs != sorted(reqs, key=lambda value: value.encode("utf-8")):
            violations.append(
                OracleViolation(
                    "noncanonical-order",
                    record_path,
                    "requirement edges are not UTF-8 sorted",
                )
            )
        if not _is_nonempty_string_list(clause_ids) or not set(clause_ids) <= set(clauses):
            violations.append(OracleViolation("unknown-id", record_path, "invalid clause IDs"))
            clause_ids = []
        if clause_ids != [f"validation:{gate_id}"]:
            violations.append(
                OracleViolation(
                    "clause-check-edge-mismatch",
                    record_path,
                    "child must resolve its gate clause",
                )
            )
        clause_requirement_value = clauses.get(f"validation:{gate_id}", {}).get(
            "requirement_ids", []
        )
        expected_requirements = (
            set(clause_requirement_value)
            if _is_string_list(clause_requirement_value)
            else set()
        )
        if set(reqs) != expected_requirements:
            violations.append(
                OracleViolation(
                    "requirement-check-edge-mismatch",
                    record_path,
                    "check requirement edges differ",
                )
            )
        if not _is_nonempty_string_list(truth):
            violations.append(OracleViolation("invalid-shape", record_path, "truth_criteria must be strings"))
        else:
            unknown_truth = set(truth) - TRUTH_CRITERIA
            if unknown_truth:
                violations.append(
                    OracleViolation(
                        "unknown-truth-criterion",
                        record_path,
                        "truth criteria include unknown values",
                    )
                )
            expected_truth = list(COMMON_TRUTH_PROJECTION)
            if truth != expected_truth:
                violations.append(
                    OracleViolation(
                        "truth-projection-mismatch",
                        record_path,
                        "check truth projection differs",
                    )
                )
        if not _is_nonempty_string_list(artifacts) or not set(artifacts) <= ARTIFACT_CLASSES:
            violations.append(OracleViolation("invalid-shape", record_path, "unknown artifact class"))
        elif tuple(artifacts) != GATE_ARTIFACT_CLASSES.get(gate_id):
            violations.append(
                OracleViolation(
                    "artifact-class-mismatch",
                    record_path,
                    "artifact classes differ",
                )
            )
        check_requirement_edges.setdefault(gate_id, set()).update(reqs)
        check_clause_edges.setdefault(gate_id, set()).update(clause_ids)

    expected_check_order = _derive_gate_check_ids(plan)
    if set(by_id) != set(expected_check_order):
        violations.append(OracleViolation("gate-child-inventory-mismatch", path, "child IDs differ from Task 9"))
    if tuple(by_id) != expected_check_order:
        violations.append(
            OracleViolation("noncanonical-order", path, "checks must preserve declared Task 9 source order")
        )
    for gate_id in (f"G{number:02d}" for number in range(21)):
        clause_id = f"validation:{gate_id}"
        clause_requirement_value = clauses.get(clause_id, {}).get("requirement_ids", [])
        clause_requirements = (
            set(clause_requirement_value)
            if _is_string_list(clause_requirement_value)
            else set()
        )
        if check_requirement_edges.get(gate_id, set()) != clause_requirements:
            violations.append(OracleViolation("requirement-check-edge-mismatch", path, gate_id))
        if check_clause_edges.get(gate_id, set()) != {clause_id}:
            violations.append(OracleViolation("clause-check-edge-mismatch", path, gate_id))


def _derive_requirement_ids(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"^\| ([A-Z]+-\d+) \|", text, flags=re.MULTILINE))


def _derive_gate_requirements(text: str) -> dict[str, set[str]]:
    result = {f"G{number:02d}": set() for number in range(21)}
    for line in text.splitlines():
        match = re.match(r"^\| ([A-Z]+-\d+) \|.*\| (G[^|]+) \|$", line)
        if not match:
            continue
        requirement_id, expression = match.groups()
        for start, end in re.findall(r"G(\d{2})(?:[–-]G?(\d{2}))?", expression):
            lower = int(start)
            upper = int(end) if end else lower
            if lower < 0 or upper > 20 or lower > upper:
                continue
            for number in range(lower, upper + 1):
                result[f"G{number:02d}"].add(requirement_id)
    return result


def _derive_skill_ids(text: str) -> tuple[str, ...]:
    skills: list[str] = []
    for number in (*range(2, 14), 15):
        match = re.search(
            rf"^### 8\.{number} .*?\n(.*?)(?=^### 8\.|^## 9\.)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        if match:
            skills.extend(re.findall(r"^- `([^`]+)`\s*$", match.group(1), flags=re.MULTILINE))
    return tuple(skills)


def _derive_profile_ids(text: str) -> tuple[str, ...]:
    block = _between(text, "The nine profile IDs and required topics are exact:", "- [ ] **Step 4")
    return tuple(re.findall(r"^- `(profile-[^`]+)`:", block, flags=re.MULTILINE))


def _derive_provenance_ids(text: str) -> tuple[str, ...]:
    block = _between(text, "The initial source-ID inventory is exact:", "Task 3 may add")
    return tuple(re.findall(r"`([^`]+)`", block))


def _derive_gate_check_ids(text: str) -> tuple[str, ...]:
    block = _between(text, "The frozen child-ID inventory is:", "```", start_delimiter="```text")
    return tuple(re.findall(r"G\d{2}-[A-Z][A-Z0-9-]+", block))


def _between(text: str, start: str, end: str, start_delimiter: str = "") -> str:
    start_index = text.find(start)
    if start_index < 0:
        return ""
    start_index += len(start)
    if start_delimiter:
        delimiter_index = text.find(start_delimiter, start_index)
        if delimiter_index < 0:
            return ""
        start_index = delimiter_index + len(start_delimiter)
    end_index = text.find(end, start_index)
    return text[start_index:] if end_index < 0 else text[start_index:end_index]


def _normalized_section(text: str, section: str) -> str | None:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    heading_index = next(
        (index for index, line in enumerate(lines) if re.fullmatch(r"###\s+" + re.escape(section), line.rstrip())),
        None,
    )
    if heading_index is None:
        return None
    end_index = len(lines)
    for index in range(heading_index + 1, len(lines)):
        if re.match(r"^#{1,3}\s+", lines[index]):
            end_index = index
            break
    selected = [line.rstrip() for line in lines[heading_index:end_index]]
    while selected and not selected[-1]:
        selected.pop()
    return "\n".join(selected) + "\n"


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_nonempty_string_list(value: object) -> bool:
    return _is_string_list(value) and bool(value) and all(value)


def _is_toml_integer_limit_error(error: ValueError) -> bool:
    message = str(error)
    return "Exceeds the limit" in message and "integer string conversion" in message


def _toml_nesting_exceeds_limit(text: str) -> bool:
    depth = 0
    index = 0
    quote = ""
    multiline = False
    while index < len(text):
        if quote:
            if multiline and text[index] == quote:
                run_end = index
                while run_end < len(text) and text[run_end] == quote:
                    run_end += 1
                if run_end - index >= 3:
                    quote = ""
                    multiline = False
                index = run_end
            elif not multiline and text[index] == quote:
                quote = ""
                index += 1
            elif quote == '"' and text[index] == "\\":
                index += 2
            else:
                index += 1
            continue
        if text[index] == "#":
            newline = text.find("\n", index)
            index = len(text) if newline < 0 else newline + 1
            continue
        if text.startswith('"""', index) or text.startswith("'''", index):
            quote = text[index]
            multiline = True
            index += 3
            continue
        if text[index] in {'"', "'"}:
            quote = text[index]
            index += 1
            continue
        if text[index] in "[{":
            depth += 1
            if depth > MAX_TOML_NESTING:
                return True
        elif text[index] in "]}":
            depth = max(0, depth - 1)
        index += 1
    return False


def _component_identity(metadata: os.stat_result) -> tuple[int, int, int]:
    return (metadata.st_dev, metadata.st_ino, stat.S_IFMT(metadata.st_mode))


def _is_link_or_reparse(metadata: os.stat_result) -> bool:
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    file_attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(
        reparse_flag and file_attributes & reparse_flag
    )


def _metadata_signature(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _path_chain_identity(root: Path, relative: Path) -> tuple[tuple[int, int, int], ...] | None:
    identities: list[tuple[int, int, int]] = []
    candidate = root
    try:
        root_metadata = root.lstat()
        if _is_link_or_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
            return None
        identities.append(_component_identity(root_metadata))
        for part in relative.parts:
            candidate /= part
            metadata = candidate.lstat()
            if _is_link_or_reparse(metadata):
                return None
            identities.append(_component_identity(metadata))
    except OSError:
        return None
    return tuple(identities)


def _read_regular_bytes(
    root: Path,
    relative: Path,
    violations: list[OracleViolation],
    *,
    missing_code: str,
) -> bytes | None:
    path_name = str(relative)
    if (
        not relative.parts
        or relative.is_absolute()
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        violations.append(
            OracleViolation("unsafe-input", path_name, "input path is not root-contained")
        )
        return None
    candidate = root
    path_identity: list[tuple[int, int, int]] = []
    try:
        root_metadata = root.lstat()
        if _is_link_or_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
            violations.append(
                OracleViolation("unsafe-input", path_name, "root identity changed")
            )
            return None
        path_identity.append(_component_identity(root_metadata))
        for part in relative.parts:
            candidate = candidate / part
            metadata = candidate.lstat()
            if _is_link_or_reparse(metadata):
                violations.append(
                    OracleViolation("unsafe-input", path_name, "symlink input is forbidden")
                )
                return None
            path_identity.append(_component_identity(metadata))
        if not stat.S_ISREG(metadata.st_mode):
            violations.append(
                OracleViolation("unsafe-input", path_name, "input is not a regular file")
            )
            return None
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError:
        violations.append(OracleViolation(missing_code, path_name, "input is missing"))
        return None
    except (OSError, RuntimeError):
        violations.append(
            OracleViolation("unsafe-input", path_name, "input metadata cannot be verified")
        )
        return None
    if resolved != root and root not in resolved.parents:
        violations.append(
            OracleViolation("unsafe-input", path_name, "input resolves outside the root")
        )
        return None
    return _read_verified_descriptor(
        root,
        relative,
        metadata,
        tuple(path_identity),
        violations,
        path_name,
    )


def _read_verified_descriptor(
    root: Path,
    relative: Path,
    expected_metadata: os.stat_result,
    expected_path_identity: tuple[tuple[int, int, int], ...],
    violations: list[OracleViolation],
    path_name: str,
) -> bytes | None:
    directory_descriptors: list[int] = []
    file_descriptor = -1
    binary_flag = getattr(os, "O_BINARY", 0)
    nofollow_flag = getattr(os, "O_NOFOLLOW", 0)
    nonblock_flag = getattr(os, "O_NONBLOCK", 0)
    close_on_exec_flag = getattr(os, "O_CLOEXEC", 0)
    noinherit_flag = getattr(os, "O_NOINHERIT", 0)
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    supports_openat = (
        os.open in getattr(os, "supports_dir_fd", set())
        and bool(directory_flag)
        and bool(nofollow_flag)
    )
    try:
        if supports_openat:
            directory_flags = (
                os.O_RDONLY | directory_flag | nofollow_flag | close_on_exec_flag
            )
            current_descriptor = os.open(root, directory_flags)
            directory_descriptors.append(current_descriptor)
            if _component_identity(os.fstat(current_descriptor)) != expected_path_identity[0]:
                violations.append(
                    OracleViolation(
                        "unsafe-input",
                        path_name,
                        "root descriptor identity changed",
                    )
                )
                return None
            for index, component in enumerate(relative.parts[:-1], start=1):
                current_descriptor = os.open(
                    component,
                    directory_flags,
                    dir_fd=current_descriptor,
                )
                directory_descriptors.append(current_descriptor)
                if (
                    _component_identity(os.fstat(current_descriptor))
                    != expected_path_identity[index]
                ):
                    violations.append(
                        OracleViolation(
                            "unsafe-input",
                            path_name,
                            "directory descriptor identity changed",
                        )
                    )
                    return None
            file_descriptor = os.open(
                relative.parts[-1],
                os.O_RDONLY
                | binary_flag
                | nofollow_flag
                | nonblock_flag
                | close_on_exec_flag,
                dir_fd=current_descriptor,
            )
        else:
            file_descriptor = os.open(
                root / relative,
                os.O_RDONLY
                | binary_flag
                | nofollow_flag
                | nonblock_flag
                | close_on_exec_flag
                | noinherit_flag,
            )
        opened_metadata = os.fstat(file_descriptor)
        if (
            not stat.S_ISREG(opened_metadata.st_mode)
            or _metadata_signature(opened_metadata) != _metadata_signature(expected_metadata)
            or _path_chain_identity(root, relative) != expected_path_identity
        ):
            violations.append(
                OracleViolation(
                    "unsafe-input",
                    path_name,
                    "input changed during verification",
                )
            )
            return None
        if opened_metadata.st_size > MAX_INPUT_BYTES:
            violations.append(
                OracleViolation(
                    "unsafe-input",
                    path_name,
                    "input exceeds the 1048576-byte limit",
                )
            )
            return None
        with os.fdopen(file_descriptor, "rb", closefd=False) as stream:
            raw = stream.read(MAX_INPUT_BYTES + 1)
        final_metadata = os.fstat(file_descriptor)
        if (
            _metadata_signature(final_metadata) != _metadata_signature(opened_metadata)
            or _path_chain_identity(root, relative) != expected_path_identity
        ):
            violations.append(
                OracleViolation(
                    "unsafe-input",
                    path_name,
                    "input changed during verified read",
                )
            )
            return None
        if len(raw) > MAX_INPUT_BYTES:
            violations.append(
                OracleViolation(
                    "unsafe-input",
                    path_name,
                    "input exceeds the 1048576-byte limit",
                )
            )
            return None
        return raw
    except OSError:
        violations.append(
            OracleViolation(
                "unsafe-input",
                path_name,
                "verified input cannot be opened",
            )
        )
        return None
    finally:
        if file_descriptor >= 0:
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        for descriptor in reversed(directory_descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _format_violations(violations: Iterable[OracleViolation]) -> str:
    lines: list[str] = []
    rendered_size = 0
    content_limit = MAX_RENDERED_OUTPUT_BYTES - 1
    for item in violations:
        line = f"{item.code}: {_safe_output_text(item.path)}: {_safe_output_text(item.detail)}"
        separator_size = 1 if lines else 0
        if rendered_size + separator_size + len(line) <= content_limit:
            lines.append(line)
            rendered_size += separator_size + len(line)
            continue
        marker_size = len(OUTPUT_TRUNCATION_MARKER) + (1 if lines else 0)
        while lines and rendered_size + marker_size > content_limit:
            removed = lines.pop()
            rendered_size -= len(removed) + (1 if lines else 0)
            marker_size = len(OUTPUT_TRUNCATION_MARKER) + (1 if lines else 0)
        lines.append(OUTPUT_TRUNCATION_MARKER)
        break
    return "\n".join(lines)


def _safe_output_text(value: str) -> str:
    without_controls = "".join(
        character if " " <= character <= "~" else "?" for character in value
    )
    without_posix_paths = re.sub(
        r"(?<![A-Za-z0-9_.-])/(?:[^\s:]+)",
        "<absolute-path>",
        without_controls,
    )
    without_absolute_paths = re.sub(
        r"\b[A-Za-z]:[\\/][^\s:]+",
        "<absolute-path>",
        without_posix_paths,
    )
    return without_absolute_paths[:256]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate independently frozen governance oracles.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    arguments = parser.parse_args(argv)
    violations = validate_oracles(arguments.root)
    if violations:
        print(_format_violations(violations))
        return 1
    print("governance oracles: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
