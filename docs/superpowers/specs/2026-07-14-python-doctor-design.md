# Python Doctor Design

Date: 2026-07-14
Status: Approved conversational design, pending written-spec review
License: Apache-2.0

## 1. Purpose

Python Doctor is an installable, deterministic Python codebase health product with a companion Codex skill. It scans repositories, normalizes evidence from mature analyzers and native rules, prioritizes root causes, applies only safe fixes, validates the result, and produces stable reports for local use and CI.

The implementation is clean-room. React Doctor is an architectural and product reference, not a source-code dependency. Python Doctor will use original Python code, schemas, rule definitions, documentation, and tests.

## 2. Product principles

- Run locally and deterministically.
- Never collect telemetry. Do not send analytics, crash reports, usage counters, repository metadata, diagnostics, source code, or scores.
- Perform all scoring locally.
- Make every network operation explicit, user-controlled, and auditable.
- Treat false positives as detector defects.
- Prefer a small, precise, mechanically verifiable rule set over a large noisy catalog.
- Reuse mature analyzers through stable adapters instead of reimplementing their strengths.
- Implement native rules only where project-aware or Python-specific evidence creates additional value.
- Gate CI on explicit findings and deltas, not on an opaque score.
- Apply automatic fixes only when they are deterministic, idempotent, and behavior-preserving.

## 3. Delivery sequence

Development proceeds in three releases:

1. General modern Python: Python 3.9+ libraries, applications, CLIs, APIs, scripts, packages, and common monorepos.
2. Backend: FastAPI, Django, Flask, asynchronous services, ORMs, API contracts, authentication, and deployment checks.
3. Data and ML: notebooks, pandas, Spark, training and inference pipelines, reproducibility, leakage, serialization, and model serving.

Release 1 is complete only when its CLI, schemas, tests, CI workflow, and Codex skill are usable together. Releases 2 and 3 extend the same contracts rather than introduce separate products.

## 4. Architecture

### 4.1 CLI layer

Expose the following commands:

```text
python-doctor scan [path]
python-doctor fix [path] --safe
python-doctor rules list|explain|set
python-doctor baseline create|check|update
python-doctor ci init|check
python-doctor skill install
python-doctor doctor
```

`doctor` is the end-to-end workflow: discover, scan, prioritize, safe-fix, rescan, test, and report.

### 4.2 Project discovery

Detect Python versions, package managers, source roots, workspaces, frameworks, tests, notebooks, generated code, vendored code, and existing tool configuration. Discovery must report uncertainty instead of silently guessing.

### 4.3 Analyzer adapters

Invoke compatible external analyzers through versioned adapters and normalize their outputs. The default release 1 installation includes the native engine plus pinned Ruff, Bandit, and complexity-analysis support. It discovers project-owned Pyright, BasedPyright, Mypy, pytest, and coverage installations without installing or reconfiguring them. If exactly one supported type checker is configured, run it; if multiple are explicitly configured, run each and deduplicate equivalent findings. Run pip-audit only when vulnerability intelligence is enabled. Adapter availability is recorded as scan coverage. Missing optional adapters do not masquerade as a clean result; missing required adapters produce a distinct incomplete-scan outcome.

Adapters must use machine-readable output when available, tolerate supported version differences, retain the originating analyzer and rule, and never rewrite another tool's configuration without explicit authorization.

### 4.4 Native rule engine

Use the Python AST and project metadata for findings that external tools cannot express precisely. Native rules may be syntax-aware, scope-aware, path-aware, call-graph-aware, or project-level. A native rule must not duplicate an adapter rule unless it materially improves precision or adds project evidence.

### 4.5 Policy engine

Apply profiles, configuration, severity overrides, category controls, path exclusions, suppressions, scan scopes, output-surface filters, baselines, and CI thresholds after normalization. Preserve raw evidence so policy changes do not alter detector truth.

### 4.6 Scoring engine

Calculate a reproducible local score from normalized, deduplicated root causes. Weight severity, confidence, category risk, and affected scope; normalize for project size; and cap repeated findings from a single rule. Publish scan coverage beside the score. Scores produced with materially different coverage are not presented as directly equivalent.

The score is advisory by default. CI failure is based on configured diagnostic severity, category, rule, baseline, or newly introduced findings. A score regression fails CI only when a project explicitly enables that policy.

### 4.7 Fix engine

Classify every remediation as unavailable, agent-required, or safe-automatic. A safe automatic fix must be deterministic, idempotent, syntax-preserving, and intended to preserve observable behavior. After editing, rerun the originating detector and relevant tests. If validation fails, keep the evidence, report the failed validation, and avoid claiming success.

Complex fixes are handed to the Codex skill with the diagnostic, related evidence, constraints, suggested validation commands, and root-cause group.

### 4.8 Reports and integrations

Support a human terminal report, versioned JSON, SARIF, GitHub Actions annotations, baseline and delta reports, and a structured handoff consumed by the Codex skill. Stable fingerprints identify findings across line movement and formatting-only changes.

## 5. Diagnostic contract

Each diagnostic contains:

- schema version and stable fingerprint
- analyzer and analyzer version
- canonical rule ID and original rule ID
- title, message, rationale, and remediation
- category, severity, confidence, and rule maturity
- file path and precise primary span
- related locations and project-level evidence
- applicable profile and tags
- suppression information
- fix safety and fix identifier
- root-cause group identifier
- scan scope and baseline status

The schema must distinguish a clean scan from a partial scan, skipped check, unsupported project, analyzer failure, invalid configuration, and policy failure.

## 6. Rule system

Release 1 categories are:

- Correctness
- Type safety and API contracts
- Security and dependency health
- Reliability and error handling
- Maintainability and architecture
- Performance and resource use
- Tests and coverage
- Packaging and environment

Every rule must:

1. State one exact problem.
2. Explain the runtime, security, maintenance, or verification impact.
3. Identify the triggering code or project shape.
4. Identify similar-looking valid cases.
5. Define intentional non-goals.
6. Include positive, negative, adversarial, and suppression tests.
7. Declare confidence, default severity, maturity, tags, and fix safety.

Rules begin as `experimental`. Promotion to `stable` requires all mandated tests, manual review of candidates from at least three structurally different repositories, no unresolved high-severity false positive, and estimated precision of at least 95 percent. A stable rule enters the `default` profile only at an estimated precision of at least 98 percent. When a rule produces fewer than 50 real-project candidates, promotion additionally requires two independently sourced positive examples and full review of every candidate. Confirmed false positives and missed findings receive permanent regression fixtures.

## 7. Profiles

- `default`: high-confidence findings suitable for most projects.
- `strict`: broader typing, maintainability, architecture, and test expectations.
- `safety-critical`: Python adaptations of the Power of 10 principles where mechanical checking is meaningful. It must label adaptations and must not pretend that Python offers C-style static memory guarantees.
- `backend`: introduced in release 2.
- `data-ml`: introduced in release 3.

Profiles alter policy and rule selection, not the underlying meaning of diagnostics.

## 8. Scan scopes and baselines

Support four scopes:

- `full`: analyze the complete repository.
- `files`: report all findings in files changed from the Git merge base.
- `changed`: report findings introduced relative to the merge base.
- `lines`: report findings whose primary evidence intersects modified lines.

Whole-project checks run only when their required evidence is available. A narrower scope must report which whole-project checks were skipped.

Baselines store versioned finding fingerprints plus the minimum metadata necessary to explain their origin. They must not store source code. Baseline updates are explicit and reviewable. CI defaults to blocking new findings at the configured threshold while preserving visibility into existing debt.

## 9. Configuration

Prefer `pyproject.toml` under `[tool.python-doctor]`. Also support `python-doctor.toml` for repositories that require a separate policy file. Configuration controls profiles, rules, categories, paths, adapters, output surfaces, baselines, fixes, CI thresholds, and the optional vulnerability lookup.

Respect existing Ruff, Pyright, Mypy, pytest, coverage, Bandit, and related configuration. CLI flags override Python Doctor configuration for the current run without mutating files.

The only supported network configuration is:

```toml
[tool.python-doctor.network]
vulnerability_intelligence = false
```

It is disabled by default. When enabled, send only standardized package identifiers and versions to the documented vulnerability provider. Disclose the provider, purpose, queried packages, cache behavior, and skipped checks. `--offline` prohibits all network access and reports a clear incompatibility if a requested operation requires it.

Python Doctor contains no telemetry subsystem or telemetry configuration.

## 10. CI behavior

GitHub Actions is the first-class release 1 CI target. Pull requests default to the `changed` scope, publish annotations and SARIF, and fail only at the configured diagnostic threshold. CI configuration must make the base revision, scan coverage, skipped checks, baseline status, and exit reason visible.

Exit codes are:

- `0`: scan completed and passed policy
- `1`: scan completed and failed diagnostic policy
- `2`: invalid configuration or invocation
- `3`: required analyzer unavailable or failed
- `4`: scan completed incompletely and policy requires complete coverage
- `5`: internal Python Doctor failure

## 11. Codex skill

The companion `python-doctor` skill triggers when finishing Python work, fixing a Python defect, preparing a commit, scanning repository health, explaining a diagnostic, or running `/doctor`-style cleanup. It invokes the local CLI, interprets structured evidence, prioritizes root causes, applies safe fixes through the CLI, performs complex repairs test-first, and validates that findings and tests did not regress.

The skill never commits, pushes, opens a pull request, changes CI policy, suppresses a rule, or updates a baseline without explicit user authorization. When a user disputes a rule, explain its evidence before offering the narrowest configuration control.

## 12. Repository structure

The source repository uses this layout:

```text
python-doctor/
├── src/python_doctor/
│   ├── cli/
│   ├── core/
│   ├── adapters/
│   ├── rules/
│   ├── fixes/
│   ├── reports/
│   └── integrations/
├── tests/
│   ├── unit/
│   ├── contracts/
│   ├── fixtures/
│   ├── integration/
│   └── end_to_end/
├── skills/python-doctor/
├── docs/
├── pyproject.toml
└── LICENSE
```

The source-of-truth skill lives in `skills/python-doctor/`. Installation copies that validated skill into the user's personal skills directory. The standalone product repository remains separate from the personal-skills Git repository. Until the user selects a destination GitHub repository, product implementation may be created in a local Git repository but must not be published externally.

## 13. Testing strategy

Use test-driven development for every behavior and rule:

- unit tests for discovery, normalization, policy, scoring, and reporting
- positive, valid-counterexample, adversarial, and suppression tests for each rule
- golden contract tests for supported analyzer versions
- property tests for stable fingerprints, path normalization, deduplication, and fix idempotence
- fixture repositories for packages, applications, scripts, and monorepos
- end-to-end Git tests for all scopes and baselines
- JSON schema and SARIF compatibility tests
- privacy tests proving ordinary and offline scans make no network requests
- performance and memory budgets for small, medium, and large fixtures
- end-to-end skill evaluations for scan, explanation, safe-fix, complex-fix, and regression workflows

Each safe fix test must first demonstrate the finding, apply the fix, demonstrate idempotence, rerun the detector, and run relevant behavioral tests.

## 14. Release 1 implementation slices

1. Core schemas, project discovery, configuration, CLI shell, and initial native-rule test harness.
2. Analyzer execution and normalization with coverage reporting.
3. Policy, suppressions, profiles, deduplication, and local scoring.
4. Git scopes, fingerprints, baselines, JSON, SARIF, and GitHub Actions.
5. Safe fix engine and validation transactions.
6. Codex skill, installation flow, realistic repository evaluations, and release hardening.

Every slice must be independently testable and leave the main branch usable.

## 15. Success criteria

Release 1 is ready when:

- a user can install `python-doctor` and scan a supported Python 3.9+ repository with one command
- reports distinguish clean, failing, partial, and unsupported scans
- the same inputs and tool versions produce stable diagnostics, fingerprints, and scores
- baseline and changed-scope behavior work in local Git and GitHub Actions
- no standard or offline workflow performs an undeclared network request
- no telemetry code path exists
- safe fixes are idempotent and validated
- the Codex skill can explain, prioritize, fix, and rescan without weakening policy silently
- the complete test suite and representative repository evaluations pass

## 16. References and adaptations

- React Doctor supplies the reference pattern of a deterministic scanner plus a thin agent skill, structured diagnostics, scan scopes, baselines, configuration controls, CI surfaces, and safe explanation workflows.
- Gerard J. Holzmann's *The Power of 10: Rules for Developing Safety-Critical Code* supplies the design principle that critical rules should be few, clear, mechanically checkable, and enforced with strong analysis. Python Doctor adapts relevant principles to Python and labels language-specific limitations.
