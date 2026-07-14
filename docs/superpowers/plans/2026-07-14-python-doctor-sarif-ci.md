# Python Doctor SARIF and GitHub Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and superpowers:test-driven-development task-by-task.

**Goal:** Add deterministic SARIF 2.1.0, GitHub annotation output, safe report-file writing, and a first-class GitHub Actions workflow without adding telemetry or implicit network behavior to the scanner.

**Architecture:** Report renderers remain pure transformations of the normalized `ScanReport`. The CLI alone owns stdout/file delivery. The checked-in workflow emits ephemeral GitHub job annotations and never uploads or persists scan reports; the Python Doctor runtime itself contains no GitHub client, upload code, analytics, or remote reporting subsystem.

**Constraints:** Python 3.9+, deterministic byte output, no embedded source snippets, no absolute diagnostic paths, no network-client imports, `shell=False` remains the only process policy.

---

### Task 1: Render SARIF 2.1.0

**Files:**
- Create: `src/python_doctor/reports/sarif.py`
- Modify: `src/python_doctor/reports/__init__.py`
- Create: `tests/test_sarif_report.py`

**Contract:**
- `render_sarif(report: ScanReport, pretty: bool = True) -> str` returns newline-terminated JSON.
- Use SARIF version `2.1.0` and the official schema URI.
- Emit one run with tool driver name `Python Doctor`, semantic version, sorted unique rules, normalized results, and scan coverage in run properties.
- Map info/warning/error to note/warning/error.
- Emit relative artifact URIs, 1-based regions, stable fingerprints under `partialFingerprints`, and no `artifactContent`, source text, environment, or command line.

- [ ] Add golden-shape tests for schema/version, rule deduplication/order, severity mapping, location, fingerprint, coverage properties, newline termination, and absence of source/absolute paths.
- [ ] Run focused tests RED, implement the renderer, then run focused/full tests GREEN.
- [ ] Commit as `feat: render sarif reports`.

---

### Task 2: Render GitHub workflow annotations

**Files:**
- Create: `src/python_doctor/reports/github.py`
- Modify: `src/python_doctor/reports/__init__.py`
- Create: `tests/test_github_report.py`

**Contract:**
- `render_github(report: ScanReport) -> str` emits one GitHub workflow command per diagnostic.
- Map info/warning/error to notice/warning/error.
- Include file, line/endLine, col/endColumn, rule ID as title, and message.
- Escape `%`, carriage return, newline, `:`, and `,` according to workflow-command rules.
- Empty findings emit a concise status line that is not a workflow annotation.

- [ ] Add failing tests for mapping, metadata, escaping, deterministic order, and empty reports.
- [ ] Implement and run focused/full tests GREEN.
- [ ] Commit as `feat: render github annotations`.

---

### Task 3: Add CLI formats and safe file output

**Files:**
- Modify: `src/python_doctor/cli.py`
- Modify: `tests/test_cli.py`

**Contract:**
- Extend `--format` to `terminal|json|sarif|github`.
- Add `--output PATH`; write UTF-8 output atomically via a same-directory temporary file and `Path.replace`.
- Reject `--score` with `--output` and reject output paths that resolve to an existing directory.
- Preserve scan exit codes after report delivery.
- Stdout is empty when `--output` succeeds.

- [ ] Add failing CLI tests for SARIF stdout, GitHub stdout, atomic file output, invalid combinations, and retained blocking exit code.
- [ ] Implement format routing and `_write_output` with cleanup on failure.
- [ ] Run focused/full tests GREEN.
- [ ] Commit as `feat: expose ci report formats`.

---

### Task 4: Add the GitHub Actions workflow

**Files:**
- Create: `.github/workflows/python-doctor.yml`
- Create: `tests/test_github_workflow.py`

**Contract:**
- Trigger on pull request and pushes to `main`.
- Set least-privilege `contents: read` permissions only.
- Use `actions/checkout@v4`, `actions/setup-python@v5` with Python 3.12, install the checked-out package, and run a complete scan in GitHub annotation format without writing or uploading a report file.
- Do not add secrets, tokens, telemetry endpoints, curl, or custom network scripts.

- [ ] Add a text-structure test asserting triggers, least-privilege permissions, pinned major actions, complete scan flags, no report persistence, and absence of prohibited telemetry/network strings.
- [ ] Add the workflow and run focused/full tests GREEN.
- [ ] Commit as `ci: add python doctor workflow`.

---

### Task 5: Verification checkpoint

- [ ] Run compileall and the complete suite twice.
- [ ] Validate Python 3.9 grammar across source/tests.
- [ ] Render the same SARIF and GitHub reports twice and compare bytes.
- [ ] Parse generated SARIF as JSON and assert it contains no source text or absolute diagnostic paths.
- [ ] Scan runtime source for network-client imports and telemetry code.
- [ ] Merge fast-forward, rerun tests, and tag `python-doctor-ci-v0`.
