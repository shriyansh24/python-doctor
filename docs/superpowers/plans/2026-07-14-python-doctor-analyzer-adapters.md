# Python Doctor Analyzer Adapters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and superpowers:test-driven-development task-by-task.

**Goal:** Make Ruff, Bandit, and Radon first-class deterministic release-1 analyzers with normalized diagnostics, explicit coverage, configurable executables, and Python-version-compatible pinned installation metadata.

**Architecture:** Each adapter owns one machine-readable external contract and returns only normalized `Diagnostic` values. The scanner remains the orchestrator and records every adapter as complete, unavailable, or failed. External processes run locally with `shell=False`; adapters never install tools, access the network, change analyzer configuration, or transmit source.

**Reference contracts:** Ruff JSON from `ruff check --output-format json`; Bandit JSON fields from PyCQA Bandit's `bandit/formatters/json.py` and `bandit/core/issue.py`; Radon JSON from its documented `cc -j -s` interface. Supported package versions are Ruff 0.15.21, Bandit 1.8.6 on Python 3.9 / 1.9.4 on Python 3.10+, and Radon 6.0.1.

**Constraints:** Python 3.9+, standard-library orchestration, no telemetry, no remote calls, no source snippets in normalized diagnostics, deterministic ordering, tests before implementation.

---

### Task 1: Normalize Bandit JSON

**Files:**
- Create: `src/python_doctor/adapters/bandit.py`
- Create: `tests/test_bandit_adapter.py`

**Contract:**
- Run `[bandit, "-r", ".", "-f", "json", "-q"]` in the project root.
- Accept return codes `0` and `1`; all other return codes are `ExternalToolError`.
- Parse top-level `results` and `errors`; non-empty errors fail the adapter so coverage cannot appear complete.
- Normalize `test_id`, `issue_text`, `issue_severity`, `issue_confidence`, `filename`, `line_number`, `line_range`, `col_offset`, and `end_col_offset`.
- Map LOW/MEDIUM/HIGH severity to info/warning/error and confidence to 0.5/0.8/1.0.
- Use rule IDs `bandit/<test_id>`, category `Security`, stable maturity, agent-required fixes, and no source snippets.

- [ ] Write fake-executable tests for normalization, severity/confidence mapping, relative paths, non-empty Bandit errors, malformed JSON, and offline environment propagation.
- [ ] Run `PYTHONPATH=src python3 -m unittest tests.test_bandit_adapter -v` and confirm RED.
- [ ] Implement `BanditAdapter` with strict shape checks and deterministic result ordering.
- [ ] Run the adapter tests and full suite GREEN.
- [ ] Commit as `feat: normalize bandit security findings`.

---

### Task 2: Normalize Radon complexity JSON

**Files:**
- Create: `src/python_doctor/adapters/radon.py`
- Create: `tests/test_radon_adapter.py`

**Contract:**
- Run `[radon, "cc", "-j", "-s", "."]` in the project root.
- Accept return code `0` only.
- Parse the path-to-block-list JSON mapping.
- Emit findings only for ranks C through F.
- Use one stable rule ID, `radon/cyclomatic-complexity`; warning for C, error for D-F; confidence 1.0; category `Maintainability`; stable maturity; agent-required fix.
- Include block name, numeric complexity, and rank in the message. Normalize `lineno`, `col_offset`, and `endline` without including source text.

- [ ] Write fake-executable tests for A/B filtering, C/D severity mapping, deterministic path/block ordering, malformed JSON, and nonzero exit behavior.
- [ ] Run `PYTHONPATH=src python3 -m unittest tests.test_radon_adapter -v` and confirm RED.
- [ ] Implement `RadonAdapter` and run focused/full tests GREEN.
- [ ] Commit as `feat: normalize radon complexity findings`.

---

### Task 3: Generalize scanner adapter coverage

**Files:**
- Modify: `src/python_doctor/scanner.py`
- Modify: `tests/test_scanner.py`

**Contract:**
- Extend `ScanOptions` with `require_bandit`, `require_radon`, `bandit_executable`, and `radon_executable`.
- Invoke Ruff, Bandit, and Radon independently after native rules.
- Record one `AnalyzerCoverage` item per analyzer in fixed order: python-doctor, ruff, bandit, radon.
- An unavailable optional adapter yields partial coverage; a required unavailable adapter yields failed status.
- One adapter failure must not prevent remaining adapters from running.
- Sort the combined diagnostics once using the existing stable key.

- [ ] Add scanner tests with fake adapters patched at the scanner boundary for complete aggregation, optional unavailable coverage, required failure, and continued execution after one failure.
- [ ] Run `PYTHONPATH=src python3 -m unittest tests.test_scanner -v` and confirm RED.
- [ ] Implement a small private adapter execution helper that never swallows coverage evidence.
- [ ] Run focused/full tests GREEN.
- [ ] Commit as `feat: orchestrate release analyzers`.

---

### Task 4: Expose adapter controls in configuration and CLI

**Files:**
- Modify: `src/python_doctor/config.py`
- Modify: `src/python_doctor/cli.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_cli.py`

**Contract:**
- Add immutable `AdapterConfig(enabled=True, required=False, executable=<name>)` values for Ruff, Bandit, and Radon under `DoctorConfig`.
- Parse optional `[adapters.ruff]`, `[adapters.bandit]`, and `[adapters.radon]` tables with strict boolean/string validation.
- Add CLI flags `--require-bandit`, `--require-radon`, `--bandit-executable`, and `--radon-executable`; keep existing Ruff flags.
- CLI explicit executable flags override configuration. Disabled adapters are recorded as skipped with reason `disabled by configuration`.
- Required and disabled is an invalid configuration.

- [ ] Add failing config/CLI tests for defaults, overrides, validation, disabled coverage, and required missing exit code 3.
- [ ] Run focused tests RED.
- [ ] Implement immutable configuration and CLI composition.
- [ ] Run focused/full tests GREEN.
- [ ] Commit as `feat: configure release analyzers`.

---

### Task 5: Pin the release analyzer matrix

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/test_package_metadata.py`

**Contract:**
- Default dependencies include `ruff==0.15.21`, `radon==6.0.1`, `bandit==1.8.6; python_version < '3.10'`, and `bandit==1.9.4; python_version >= '3.10'`.
- Keep the Python 3.9-compatible `tomli` marker.
- Tests parse `pyproject.toml` with `tomllib`/`tomli` and assert exact analyzer pins and mutually exclusive Bandit markers.

- [ ] Add metadata test and confirm RED.
- [ ] Add exact version pins and run focused/full tests GREEN.
- [ ] Commit as `build: pin release analyzer versions`.

---

### Task 6: Analyzer checkpoint verification

- [ ] Run compileall and the full test suite twice.
- [ ] Parse all source/tests using Python 3.9 grammar.
- [ ] Run fake analyzer contracts twice and compare normalized JSON byte-for-byte.
- [ ] Scan the source for network-client imports and subprocess calls outside `adapters/base.py`.
- [ ] Confirm clean Git state, fast-forward merge to master, rerun the full suite, and tag `python-doctor-analyzers-v0`.

