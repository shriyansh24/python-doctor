# Python Doctor Policy and Scoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic policy controls, suppressions, root-cause deduplication, local scoring, and explicit scan exit behavior to the verified foundation.

**Architecture:** Keep detection truth in `ScanReport`; transform it through pure deduplication, policy, and scoring functions. Configuration remains immutable at the boundary. The CLI composes the phases and maps their outcomes to the versioned exit-code contract without changing analyzer behavior.

**Tech Stack:** Python 3.9+, standard library (`dataclasses`, `fnmatch`, `math`, `pathlib`, TOML), `unittest`.

## Global Constraints

- Preserve all foundation constraints and Python 3.9 compatibility.
- Perform all scoring locally and deterministically.
- Do not add network libraries, telemetry, remote scoring, or source upload behavior.
- Treat score as advisory; gate on explicit diagnostics unless score gating is explicitly added in a later plan.
- Apply rule-level severity over category-level severity.
- Use exact rule and glob suppressions; never suppress silently.
- Develop test-first and commit after every task.

---

### Task 1: Extend configuration with policy controls

**Files:**
- Modify: `src/python_doctor/config.py`
- Modify: `tests/test_config.py`

**Interfaces:**
- Extend `DoctorConfig` with `rules`, `categories`, `ignore_rules`, `ignore_files`, `blocking`, and `require_complete`.
- Keep `load_config(project_root: Path) -> DoctorConfig`.
- Accept severities `off`, `info`, `warning`, and `error`; accept blocking values `none`, `warning`, and `error`.

- [ ] **Step 1: Add failing configuration tests**

```python
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
```

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_config -v`

Expected: missing `DoctorConfig.rules` or validation failure.

- [ ] **Step 3: Implement immutable tuple-backed controls**

Add fields:

```python
@dataclass(frozen=True)
class DoctorConfig:
    profile: str = "default"
    network: NetworkConfig = NetworkConfig()
    rules: Tuple[Tuple[str, str], ...] = ()
    categories: Tuple[Tuple[str, str], ...] = ()
    ignore_rules: Tuple[str, ...] = ()
    ignore_files: Tuple[str, ...] = ()
    blocking: str = "error"
    require_complete: bool = False
```

Add validation helpers that require mappings of strings to valid severities, lists of strings for ignores, a valid blocking value, and a boolean `require_complete`. Sort mapping items before storing them so configuration identity is deterministic.

- [ ] **Step 4: Run GREEN and full regression suite**

Run: `PYTHONPATH=src python3 -m unittest tests.test_config -v && PYTHONPATH=src python3 -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/python_doctor/config.py tests/test_config.py
git commit -m "feat: configure diagnostic policy"
```

---

### Task 2: Deduplicate shared root causes

**Files:**
- Create: `src/python_doctor/deduplication.py`
- Create: `tests/test_deduplication.py`

**Interfaces:**
- Produce `deduplicate_diagnostics(diagnostics: Iterable[Diagnostic]) -> tuple[Diagnostic, ...]`.
- Use `root_cause_group` when present; otherwise use `fingerprint`.
- Retain the highest-severity diagnostic; break ties by analyzer, rule ID, path, and span.

- [ ] **Step 1: Write failing root-cause and ordering tests**

Create a local `make_diagnostic()` fixture returning a valid `Diagnostic`. Assert that two diagnostics with group `group-a` collapse to the error-severity one, while two diagnostics without a group remain distinct. Assert deterministic output ordering.

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_deduplication -v`

Expected: import failure for `python_doctor.deduplication`.

- [ ] **Step 3: Implement deterministic grouping**

```python
_SEVERITY_RANK = {Severity.INFO: 0, Severity.WARNING: 1, Severity.ERROR: 2}

def deduplicate_diagnostics(diagnostics: Iterable[Diagnostic]) -> Tuple[Diagnostic, ...]:
    selected: Dict[str, Diagnostic] = {}
    for diagnostic in diagnostics:
        key = f"group:{diagnostic.root_cause_group}" if diagnostic.root_cause_group else f"finding:{diagnostic.fingerprint}"
        current = selected.get(key)
        if current is None or _selection_key(diagnostic) > _selection_key(current):
            selected[key] = diagnostic
    return tuple(sorted(selected.values(), key=_output_key))
```

Define `_selection_key` and `_output_key` with only stable primitive fields.

- [ ] **Step 4: Run GREEN and regression suite**

Run: `PYTHONPATH=src python3 -m unittest tests.test_deduplication -v && PYTHONPATH=src python3 -m unittest discover -s tests -v`

- [ ] **Step 5: Commit**

```bash
git add src/python_doctor/deduplication.py tests/test_deduplication.py
git commit -m "feat: deduplicate diagnostic root causes"
```

---

### Task 3: Apply suppressions and severity policy

**Files:**
- Create: `src/python_doctor/policy.py`
- Create: `tests/test_policy.py`

**Interfaces:**
- Produce `PolicyResult(report, suppressed, blocking_diagnostics)`.
- Produce `apply_policy(report: ScanReport, config: DoctorConfig) -> PolicyResult`.
- Apply file globs and ignored rules first, then category severity, then rule severity.

- [ ] **Step 1: Write failing policy precedence tests**

Test these independent behaviors:

```python
config = DoctorConfig(
    rules=(("ruff/F401", "warning"),),
    categories=(("Correctness", "error"),),
    ignore_rules=("bandit/B101",),
    ignore_files=("tests/**",),
    blocking="warning",
)
```

Assert that `ruff/F401` becomes warning despite category error, `bandit/B101` is suppressed, a diagnostic in `tests/unit.py` is suppressed, suppressed diagnostics remain available in `PolicyResult.suppressed`, and warning/error findings enter `blocking_diagnostics`.

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_policy -v`

- [ ] **Step 3: Implement pure policy evaluation**

Use `dataclasses.replace` to change severity without mutating detector output. Use `fnmatch.fnmatchcase` on normalized `/` paths. Return a report containing only visible diagnostics and preserve coverage/status metadata.

```python
@dataclass(frozen=True)
class PolicyResult:
    report: ScanReport
    suppressed: Tuple[Diagnostic, ...]
    blocking_diagnostics: Tuple[Diagnostic, ...]
```

Blocking rank: `none` blocks nothing, `warning` blocks warnings and errors, `error` blocks errors only.

- [ ] **Step 4: Run GREEN and regression suite**

Run: `PYTHONPATH=src python3 -m unittest tests.test_policy -v && PYTHONPATH=src python3 -m unittest discover -s tests -v`

- [ ] **Step 5: Commit**

```bash
git add src/python_doctor/policy.py tests/test_policy.py
git commit -m "feat: apply diagnostic policy"
```

---

### Task 4: Calculate the local health score

**Files:**
- Create: `src/python_doctor/scoring.py`
- Create: `tests/test_scoring.py`
- Modify: `src/python_doctor/diagnostics.py`
- Modify: `tests/test_diagnostics.py`

**Interfaces:**
- Add `score: Optional[float] = None` and `score_label: Optional[str] = None` to `ScanReport`; serialize them as `score` and `scoreLabel`.
- Produce `ScoreResult(score: float, label: str, deductions: tuple[RuleDeduction, ...])`.
- Produce `calculate_score(diagnostics, source_file_count) -> ScoreResult`.

- [ ] **Step 1: Write failing score tests**

Assert:

- no diagnostics yields `100.0` and `healthy`
- one error scores lower than one warning
- duplicate root-cause groups are counted once
- 100 identical warnings for one rule are capped at 24 deduction points before project-size normalization
- the same inputs return byte-for-byte equal `ScoreResult`

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_scoring tests.test_diagnostics -v`

- [ ] **Step 3: Implement the exact scoring formula**

```python
_SEVERITY_WEIGHT = {Severity.INFO: 1.0, Severity.WARNING: 4.0, Severity.ERROR: 12.0}
_CATEGORY_MULTIPLIER = {"Security": 1.25, "Reliability": 1.15, "Correctness": 1.10}
_PER_RULE_CAP = 24.0

raw = severity_weight * clamp(confidence, 0.0, 1.0) * category_multiplier
project_scale = max(1.0, math.sqrt(max(source_file_count, 1) / 10.0))
score = round(max(0.0, 100.0 - sum(capped_rule_deductions) / project_scale), 1)
```

Labels: `healthy` at 90+, `attention` at 75+, `risky` at 50+, otherwise `critical`.

- [ ] **Step 4: Run GREEN and regression suite**

Run: `PYTHONPATH=src python3 -m unittest tests.test_scoring tests.test_diagnostics -v && PYTHONPATH=src python3 -m unittest discover -s tests -v`

- [ ] **Step 5: Commit**

```bash
git add src/python_doctor/scoring.py src/python_doctor/diagnostics.py tests/test_scoring.py tests/test_diagnostics.py
git commit -m "feat: calculate local health score"
```

---

### Task 5: Compose deduplication, policy, and scoring in the CLI

**Files:**
- Modify: `src/python_doctor/cli.py`
- Modify: `src/python_doctor/reports/terminal.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_reports.py`

**Interfaces:**
- Add CLI overrides `--blocking none|warning|error`, `--require-complete`, and `--score`.
- Exit `1` for blocking diagnostics, `3` for required analyzer failure, and `4` for partial scans when complete coverage is required.
- `--score` prints only one numeric line.

- [ ] **Step 1: Write failing CLI and report tests**

Add tests proving:

- safety recursion with `--blocking error` exits `1`
- missing optional Ruff with `--require-complete` exits `4`
- `--blocking none` keeps findings advisory
- `--score` prints a float and no diagnostic detail
- terminal and JSON reports include local score and label

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python3 -m unittest tests.test_cli tests.test_reports -v`

- [ ] **Step 3: Implement CLI composition**

After `scan_project`:

1. deduplicate diagnostics
2. replace report diagnostics with deduplicated diagnostics
3. apply config plus CLI blocking/complete overrides
4. calculate score using discovered Python file count
5. attach score and label to the policy report
6. render output
7. map exit precedence: internal/analyzer `3`, incomplete-required `4`, blocking `1`, otherwise `0`

- [ ] **Step 4: Run GREEN and complete suite**

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

- [ ] **Step 5: Commit**

```bash
git add src/python_doctor/cli.py src/python_doctor/reports/terminal.py tests/test_cli.py tests/test_reports.py
git commit -m "feat: enforce policy and report local score"
```

---

### Task 6: Policy and scoring verification checkpoint

**Files:**
- Modify only when a failing verification receives a regression test first.

- [ ] **Step 1: Compile and run the full suite twice**

Run: `python3 -m compileall -q src tests && PYTHONPATH=src python3 -m unittest discover -s tests -v && PYTHONPATH=src python3 -m unittest discover -s tests -v`

- [ ] **Step 2: Verify Python 3.9 grammar**

Run the existing `ast.parse(..., feature_version=(3, 9))` check across all source and test files.

- [ ] **Step 3: Verify deterministic score and JSON output**

Run the same safety-critical fixture twice in-process and assert equal JSON output and equal score.

- [ ] **Step 4: Verify privacy and tree cleanliness**

Run: `rg -n "requests|urllib|httpx|aiohttp|socket" src/python_doctor || true`, `git diff --check`, and `git status --short --branch`.

- [ ] **Step 5: Tag the verified checkpoint**

Run: `git tag python-doctor-policy-v0`.
