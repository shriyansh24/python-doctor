# Complete Python Doctor and Universal Python Skills Design

**Status:** User-approved primary specification; implementation remains gated
by G00

**Date:** 2026-07-14

**Companion release gates:**
`docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md`

**Subordinate Python-native architecture:**
`docs/design/proof-carrying-python-architecture.md`, adopted under the user's
originality direction. If it conflicts with this primary specification or the
release gates, this specification and the release gates control.

**Functional inspiration named by the user:** `millionco/react-doctor`

**Clean-room restriction:** the inspected reference commit uses a modified
license that restricts use by automated AI pipelines. No React Doctor code,
tests, prompts, skills, assets, prose, or close paraphrase may be copied into
this Apache-2.0 project. Do not process the reference checkout further without
prior written permission from its copyright holder or a documented legal
determination; user approval alone cannot waive a third party's license. The design below is an
independently authored Python system based on user-approved jobs and public
Python specifications, not a derivative implementation.

## 1. Mission

Build Python Doctor toward a best-in-class local-first Python codebase health
system and broadly reusable Python engineering skill suite for coding agents.
It must combine deterministic diagnostics, explainable findings, safe fixes,
repository-wide audits, reusable Agent Skills, editor integration, CI support,
rule research and fuzzing, and first-class documentation.

Python Doctor must cover the complete set of Python-native user jobs approved
in this specification. “Parity” means verified responsibility and workflow
coverage, never file-by-file similarity. Python-specific equivalents must be
real and useful; empty packages and structure-only placeholders are forbidden.

## 2. Non-negotiable constraints

1. License all original project code and skills under Apache-2.0.
2. Core, API, CLI, native rules, and reports install and run on CPython 3.9
   through 3.14 and analyze declared target grammars 3.9 through 3.14. LSP,
   Node/Rust editor clients, frameworks, runtimes, and optional tools publish
   separate exact support matrices. A narrower integration range requires an
   approved host constraint and may not reduce essential-package claims.
3. Perform scans locally and deterministically.
4. Include no telemetry subsystem: no analytics, crash reporting, Sentry,
   OpenTelemetry export, OTLP, usage counters, installation/device/user/session
   identifiers, hosted score,
   report upload, background HTTP, remote prompt fetch, or update check.
5. Do not add a telemetry opt-out flag because there is nothing to disable.
6. The scanner, API, LSP, editor integration, and bundled skill helpers never
   initiate network access or transmit a scanned repository's source, findings,
   paths, metadata, environment, or reports. Deterministic local diagnostic IDs
   and fingerprints may contain no sensitive data.
7. Write reports only to stdout or a path explicitly selected by the user.
8. Treat incomplete analysis as incomplete. Never call a partial scan clean.
9. Preserve deterministic output ordering and stable diagnostic identities.
10. Use project-specific conventions before generic style preferences.
11. Preserve public API compatibility or provide an explicit deprecation path.
12. Keep third-party skill and rule provenance reviewable.
13. Do not claim NASA endorsement, certification, or NASA-STD compliance.
14. Use test-first implementation for behavior changes.
15. Do not declare completion while any required gate, package, skill, document,
    compatibility target, or adversarial review is missing.
16. Use a clean-room process. Do not copy, translate, or closely paraphrase
    React Doctor implementation material, even when only names are changed.
17. Remove scanner/runtime vulnerability intelligence, remote rules/prompts/
    configuration, source/finding/report upload, update checks, and related
    guidance; do not retain dormant feature flags. Separately authorized
    development research/dependency acquisition and publication of Python
    Doctor's own artifacts are outside scanner runtime.
18. Treat deliberate user-authorized publication of Python Doctor's own source
    and release artifacts as a separate release operation, not runtime product
    behavior. External platform telemetry is outside the project boundary;
    shipped integrations still include no tracker, SDK, or telemetry call.

## 3. Research foundation

The design is grounded in:

- The high-level functional responsibilities the user selected after reviewing
  React Doctor: scanner, rules, skills, CLI/API, language tooling, fuzzing,
  evaluation, documentation, CI, and release workflows. These are re-designed
  independently for Python under the clean-room restriction above.
- The Agent Skills specification and progressive-disclosure model.
- PEP 8, PEP 20, PEP 257, Python's typing guidance, PyPA specifications,
  pytest integration guidance, Hypothesis, Ruff, mypy, Bandit, and Python's
  language/library references.
- OSS skill repositories from Anthropic, OpenAI, GitHub Awesome Copilot,
  wshobson/agents, Trail of Bits, Microsoft, Hugging Face, and Superpowers.
- Gerard J. Holzmann's 2006 article, “The Power of 10: Rules for Developing
  Safety-Critical Code,” DOI `10.1109/MC.2006.212`, supplied by the user.

Among the named repositories and revisions reviewed on 2026-07-14, research
found no suite that is simultaneously Python-wide,
semantics-aware, web/data/ML complete, locally verifiable, zero-telemetry, and
equipped with deterministic diagnostics and skill evaluations. Python Doctor
must fill that gap without importing incompatible prose or unsafe skills.

### 3.1 Legal and provenance gate

Before production implementation:

- quarantine the React Doctor checkout as non-reusable reference material;
- record every researched source by immutable revision, verified license,
  inspected paths, extracted concept, reuse status, and attribution need;
- permit copied prose or code only after file-level license compatibility is
  established; custom, no-AI, noncommercial, copyleft-incompatible, and unknown
  licenses may inform only an independently expressed gap list;
- record the exact restricted-source commit, license-file path/hash,
  already-inspected paths, and exposure/taint status;
- require future clean implementers to certify they received only approved
  user-authored requirements and public Python standards;
- permit restricted-source comparison only by an authorized human/legal
  reviewer; without that authority, the legal gate remains `BLOCKED` rather than
  asking an automated agent to perform a similarity review;
- keep the supplied Power of Ten PDF out of distribution and cite/paraphrase it;
- record the two supplied copies as byte-identical, SHA-256
  `c762a07be7b8ea65b95e1f1f748efa60f7196d75fdf81181169cfb8e0b2b4c8f`,
  four-page source inputs that are excluded from the repository and artifacts;
- require root Apache-2.0 licensing, SPDX package metadata, notices, dependency
  license review, SBOMs, and a provenance manifest.

The requirements matrix must include at least `LEG-01` clean-room
implementation, `LEG-02` Apache-2.0 release, and `LEG-03` OSS research
provenance. A legal/provenance failure is stop-ship.

### 3.2 Reproducible OSS research protocol

Do not claim to have found literally every Python skill in OSS. Record the
research date, registries, GitHub queries, repositories, revisions, licenses,
candidate skills, unique techniques, evidence quality, gaps, duplicates, and
adopt/adapt-idea-only/reject disposition. Search across Python code review,
naming, comments/docstrings, typing, testing, security, packaging, performance,
concurrency, web, data, ML, scientific computing, native boundaries, editors,
and release engineering.

Run at least two independent query rounds. Research reaches category saturation
only when two consecutive rounds reveal no new P0/P1 capability category. New
wording for an existing category does not count as a new capability. Preserve
the query log and stopping evidence under `docs/research/`.

## 4. Repository architecture

```text
python-doctor/
├── .agents/skills/                    generated compatibility copies
├── .github/
│   ├── instructions/                  generated path-specific instructions
│   └── workflows/
│       ├── ci.yml
│       ├── code-quality.yml
│       ├── delta-audit.yml
│       ├── privacy-audit.yml
│       ├── publish.yml
│       └── python-doctor.yml
├── assets/
├── changes/                           release fragments
├── docs/
│   ├── architecture/
│   ├── cli/
│   ├── configuration/
│   ├── contributing/
│   ├── editor/
│   ├── reports/
│   ├── rules/
│   ├── safety/
│   ├── skills/
│   └── superpowers/
├── evals/
│   ├── corpus/
│   ├── diagnostics/
│   └── skills/
├── packages/
│   ├── core/
│   ├── api/
│   ├── python-doctor/
│   ├── rules/
│   ├── deslop/
│   ├── deslop-cli/
│   ├── fuzz/
│   ├── language-server/
│   ├── vscode-python-doctor/
│   ├── zed-python-doctor/
│   └── website/
├── scripts/
│   ├── delta-audit/
│   ├── function-mining/
│   ├── performance/
│   ├── release/
│   └── skills/
├── skills/                            canonical Agent Skills source
│   ├── routers/
│   ├── profiles/
│   └── library/
├── tests/
│   ├── e2e/
│   ├── integration/
│   ├── privacy/
│   └── release/
├── action.yml
├── AGENTS.md
├── CLAUDE.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── PRIVACY.md
├── README.md
├── SECURITY.md
└── pyproject.toml
```

Nested `AGENTS.md` files define package-specific constraints. The root
`CLAUDE.md` imports or points to the canonical root instructions. Generated
Copilot and agent compatibility files are checked for drift.

## 5. Package boundaries

### 5.1 `packages/core`

Owns project discovery, configuration, capabilities, diagnostics, analyzer
coverage, policies, ignores, suppressions, severity controls, stable identity,
baseline/diff/staged selection, score calculation, deterministic caching,
deadlines, report models, analyzer orchestration, and local-only privacy guards.

Core must not contain terminal interaction, GitHub clients, HTTP clients,
telemetry, editor protocol code, or package-install behavior.

### 5.2 `packages/api`

Exports stable synchronous and asynchronous programmatic interfaces:

```python
diagnose(path, *, options=None) -> DiagnoseResult
diagnose_async(path, *, options=None) -> DiagnoseResult
inspect_project(path, *, options=None) -> ProjectInfo
define_config(**values) -> DoctorConfig
```

The API never prints, prompts, changes repository files, or accesses the
network. Its default cache is in memory. Persistent cache/output requires an
explicit option and never writes inside the scanned repository unless the user
selects that exact destination. Errors use a documented exception hierarchy and
preserve causes.

### 5.3 `packages/python-doctor`

Published CLI and user orchestration. It owns argument parsing, terminal
rendering, interactive setup, explicit local file writes, skill installation,
hook installation, CI scaffolding, and agent handoff.

### 5.4 `packages/rules`

Canonical native Python rule registry. Detectors choose the narrowest adequate
analysis level:

- token or text for comment/suppression structure;
- `ast` for syntax and control flow;
- symbol tables for bindings and scopes;
- LibCST only where safe rewrites or comment fidelity require it;
- type-aware adapters when a rule genuinely requires type information;
- project scan rules for filesystem, packaging, dependency, or cross-module
  evidence.

Ruff does not expose a general third-party plugin system, so Python Doctor must
not create a fake Ruff plugin. Optional bridges may target real Flake8 or
Pylint plugin contracts while the native registry remains authoritative.

### 5.5 `packages/deslop` and `packages/deslop-cli`

Own dead and duplicate modules, functions, imports, dependencies, aliases,
cycles, layering violations, stale feature flags, mutable globals, side-effect
imports, and confidence-ranked semantic duplication.

### 5.6 `packages/fuzz`

Own deterministic AST/CST generation, Hypothesis strategies, metamorphic
variants, pathological depth/width programs, crash/timeout oracles, rule
invariance checks, and a permanent regression corpus for confirmed false
positives.

### 5.7 `packages/language-server`

Provide LSP diagnostics over saved and unsaved buffers, precise ranges, hovers,
rule explanations, narrow suppressions, safe quick fixes, workspace/project
ownership, cancellation, cache invalidation, progress, and local server status.

### 5.8 Editor clients

VS Code/Cursor and Zed packages are thin host-native clients for the language
server. They must not duplicate diagnostic logic or add network behavior.
They never auto-download or update the server, rules, skills, or configuration.

### 5.9 `packages/website`

Static, buildable documentation. It must work without runtime analytics,
cookies, tracking pixels, external fonts, or client telemetry.

## 6. Product capabilities

### 6.1 Scan modes

- full repository;
- workspace/monorepo;
- path or file;
- Git changed files;
- changed lines;
- staged files;
- baseline comparison;
- editor buffer;
- safety-scoped paths.

### 6.2 Project discovery

Recognize `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt`, uv,
Poetry, PDM, Pipenv, Hatch and Conda metadata, `src` and flat layouts,
namespace packages, editable/path dependencies, applications, libraries,
typed packages, stubs, tests, migrations, notebooks, generated code, vendored
code, and multi-package workspaces.

### 6.3 Analyzer integration

Integrate local executables through strict machine-readable contracts. Initial
adapters include Ruff, Bandit, Radon, mypy, Pyright/ty where configured,
Vulture, and local dependency/lockfile checks. Optional analyzers never install
themselves or access the network.

Every analyzer plan/result records `not_selected`, `complete`, `partial`,
`unavailable`, `failed`, or `skipped` with a reason. Required analyzer failure
fails the scan.

Before execution, resolve and serialize the scan plan. An optional analyzer not
selected by its profile is `not_selected` and does not affect completeness. Any
selected or required analyzer that is skipped, unavailable, failed, timed out,
or partial makes the scan incomplete and produces a nonzero result. Profiles
require capabilities explicitly and never depend on whichever tools happen to
be installed.

Treat scanned repositories as hostile. Never execute `setup.py`, project code,
Git hooks, analyzer plugins, arbitrary commands, remote includes, or config that
imports code. Parse metadata statically. Resolve only explicit or vetted
executables, use argument arrays without a shell, pass a minimal environment
allowlist with proxy/token variables removed, and invoke Git with external diff
and text conversion disabled. Enforce root containment; do not follow symlinks
outside the root or read devices/FIFOs. Bound files, input/output bytes,
processes, time, memory, and the entire child process tree. An analyzer that
cannot run inside the declared sandbox is unavailable, never silently run with
weaker isolation.

### 6.4 CLI surface

```text
python-doctor scan
python-doctor fix --preview|--apply|--rollback
python-doctor inspect
python-doctor explain <occurrence-fingerprint> --result <local-result>
python-doctor rules list|explain|enable|disable|set
python-doctor baseline create|compare
python-doctor config validate|show
python-doctor skills list|install|validate|eval
python-doctor hooks install|remove|status
python-doctor ci install|config|upgrade|validate
python-doctor cache clear|status
python-doctor doctor
python-doctor version
```

No command may imply sharing or remote score publication.

`explain` resolves one diagnostic occurrence from an explicitly selected local
result using its occurrence fingerprint and result/capsule identity; `rules
explain` documents a rule contract and never pretends to identify an occurrence.

Fixes are preview-first, limited to declared safety classes, atomic,
root-contained, symlink-safe, concurrent-change-aware, idempotent, and backed by
a rollback journal. Public API renames require explicit migration authority.
The CLI contract reserves distinct nonzero exits for blocking findings,
incomplete/configuration failure, and internal failure; exact values live in the
versioned CLI schema.

### 6.5 Reports

Support terminal, JSON, SARIF, GitHub annotation text, and agent handoff JSON.
Reports include:

- schema version;
- scan mode and profile;
- project identity using relative/local values only;
- diagnostic IDs, rule, category, severity, confidence and evidence;
- normalized relative location;
- recommended skill identifiers;
- safe-fix metadata;
- complete analyzer coverage;
- skipped checks and reasons;
- score and label;
- baseline delta where applicable.

Empty diagnostics cannot imply clean unless planned coverage completed.

## 7. Diagnostic and rule contract

Every rule defines:

- stable rule ID;
- title and category;
- default severity by profile;
- maturity (`experimental`, `preview`, `stable`);
- evidence level;
- supported Python versions;
- required capabilities;
- diagnostic message and remediation;
- false-positive traps and non-goals;
- safe-fix or agent-fix classification;
- recommended skill IDs;
- documentation URL/path;
- deterministic tests and corpus cases.

Diagnostics are sorted by normalized path, span, severity rank, analyzer, rule,
and fingerprint. Fingerprints never include absolute paths or source text.

Baseline and persistent-cache schemas are versioned, content-addressed, and
invalidated by tool/rule/config/source-version changes. The score formula has a
versioned schema and explainable deductions; incomplete scans never receive a
comparable score or clean label. Terminal and machine output sanitize ANSI and
control characters from hostile input.

## 8. Skill system architecture

### 8.1 Canonical format

`skills/` is authoritative. Each Agent Skill uses a pinned agentskills.io
schema revision, a focused `SKILL.md`, and optional one-hop `references/`,
`scripts/`, and `assets/`. Original material is Apache-2.0. Compatible imported
material retains its source license, SPDX metadata, notice, and provenance;
generated copies preserve that metadata.

Generated copies under `.agents/skills/` and other client integration paths
must never be hand-edited. A sync command and drift test enforce identity.

A versioned capability manifest distinguishes:

- globally discoverable routers;
- opt-in profile packs;
- router-invocable leaf skills;
- internal reference modules that are never independently advertised.

Each entry declares its owner router, kind, trigger, exclusions, prerequisites,
conflicts, deterministic precedence, lifecycle (`planned`, `experimental`,
`preview`, `stable`), delivered capabilities (a set drawn from `guidance`,
`evaluated_guidance`, `tool_integration`, `diagnostic`, and `safe_fix`),
host/runtime/source/framework
support, context cost, mutation authority, and eval IDs. Cycles are forbidden.
The default load budget is one router plus at most five leaves; a larger set
requires explicit user scope and records why each module is needed.

Before implementation, freeze a release manifest. Entries listed in sections
8.2–8.13 and 8.15 are `required=true`; optional means optional user activation,
not optional delivery. Section 8.14 entries are explicitly `delivered`,
`planned`, or `unsupported`. Only delivered, evaluation-backed capabilities
count toward release claims, and a placeholder page cannot count as coverage.

Skill schemas vary by kind: routers require routing and budget contracts;
diagnostic/review skills require evidence, confidence, false-positive, and safe
fix policies; mutation skills require authorization and rollback; framework
adapters require detection and version support; procedural/reference skills
require executable steps and validators. Inapplicable fields are explicit and
justified rather than filled with boilerplate.

### 8.2 Default routers

- `python-doctor`
- `build-python`
- `improve-python`
- `review-python`
- `debug-python`
- `refactor-python`
- `test-python`
- `secure-python`
- `optimize-python`
- `package-python`
- `ship-python`

Routers detect repository facts and load only relevant leaf skills. They must
not paste the entire skill library into context.

`review-python`, `improve-python`, and `refactor-python` may call
`self-explanatory-python`. That orchestrator calls `naming-python` only when
symbol meaning is in scope and `comments-docstrings-python` only when comments,
docstrings, suppressions, or documentation contracts are in scope. Similar
overlap groups designate one orchestrator and focused leaves; orchestrators and
their reference modules are not double-counted as separate capabilities.

### 8.3 Optional profile packs

- `python-core`
- `python-web`
- `python-data-ml`
- `python-security`
- `python-safety`
- `python-packaging-release`
- `python-docs`

### 8.4 Readability and explainability skills

- `naming-python`
- `comments-docstrings-python`
- `self-explanatory-python`
- `python-code-clarity`
- `python-complexity-decomposition`
- `find-similar-python-symbols`
- `simplify-python`
- `python-domain-language`
- `python-magic-values-and-units`
- `python-duplicate-dead-code`

### 8.5 Language and design skills

- `python-idioms`
- `typing-python`
- `python-generics-protocols`
- `designing-python-apis`
- `handling-python-errors`
- `managing-python-resources`
- `python-iterators-generators`
- `python-decorators-descriptors`
- `structuring-python-imports`
- `python-dataclasses-models`
- `python-immutability-state`
- `python-datetime-timezones`
- `python-serialization`
- `python-regex-text`
- `python-text-bytes-encoding`
- `python-unicode-locale-i18n`
- `python-pattern-matching`
- `python-numeric-correctness`
- `python-equality-hashing-ordering-copying`
- `python-warnings-deprecations`
- `python-filesystem-process-signal-portability`
- `python-plugin-architecture`
- `python-version-compatibility`
- `configuring-python`
- `logging-python`
- `designing-python-cli`

`logging-python` covers local application logs and diagnostics only. It must
never introduce remote log shipping or telemetry.

### 8.6 Testing and verification skills

- `testing-python`
- `python-pytest`
- `python-test-design`
- `python-property-testing`
- `python-mutation-testing`
- `python-contract-testing`
- `python-integration-testing`
- `python-snapshot-golden-tests`
- `python-flaky-test-diagnosis`
- `python-test-isolation`
- `python-coverage-quality`
- `python-fuzzing`
- `python-cross-version-matrix`
- `python-cli-testing`

### 8.7 Security and supply-chain skills

- `securing-python`
- `python-static-security`
- `python-dependency-audit`
- `python-secret-handling`
- `python-crypto-safety`
- `python-deserialization-safety`
- `python-subprocess-shell-safety`
- `python-filesystem-tempfile-safety`
- `python-http-ssrf-safety`
- `python-sql-injection-safety`
- `python-auth-session-safety`
- `python-privacy-logging`
- `python-supply-chain`
- `python-reproducible-builds`
- `python-sbom-provenance`
- `python-dangerous-api-review`

### 8.8 Concurrency and reliability skills

- `async-python`
- `python-structured-concurrency`
- `python-cancellation-timeouts`
- `python-backpressure`
- `concurrent-python`
- `python-free-threading`
- `python-multiprocessing`
- `python-race-deadlock-review`
- `python-background-jobs`
- `python-retries-idempotency`
- `python-resilience`
- `python-contextvars`
- `python-graceful-shutdown`

### 8.9 Performance skills

- `optimizing-python`
- `python-profile-first`
- `python-algorithmic-performance`
- `python-memory-profiling`
- `python-io-performance`
- `python-caching`
- `python-benchmarking`
- `python-vectorization`
- `python-native-extensions-ffi`
- `python-startup-import-performance`
- `python-performance-regression`

### 8.10 Packaging and release skills

- `packaging-python`
- `python-project-structure`
- `python-pyproject`
- `python-dependencies`
- `python-lockfiles`
- `python-src-layout`
- `python-build-wheel-sdist`
- `python-cli-packaging`
- `python-library-typing-pytyped`
- `python-entrypoints-plugins`
- `python-namespace-packages`
- `python-versioning-changelog`
- `python-deprecation-migration`
- `python-trusted-publishing`
- `python-release-checklist`
- `python-cross-platform`
- `python-uv`
- `python-pip`
- `python-poetry`
- `python-conda`

### 8.11 Web and API skills

- `python-http-api-design`
- `python-http-client-lifecycle`
- `python-openapi`
- `fastapi-python`
- `django-python`
- `python-django-rest-framework`
- `flask-python`
- `pydantic-python`
- `sqlalchemy-python`
- `alembic-python`
- `python-database-transactions`
- `python-persistence-query-correctness`
- `python-deployment-service-runtime`
- `python-celery`
- `python-websockets`
- `python-graphql`
- `python-mcp-server`
- `python-serverless`
- `python-typer-click`

### 8.12 Data, science, and ML skills

- `numpy-python`
- `pandas-python`
- `polars-python`
- `python-scientific-computing`
- `python-numerical-stability`
- `notebooks-python`
- `python-data-validation`
- `python-data-quality-lineage`
- `python-data-privacy-retention`
- `python-data-leakage`
- `python-reproducible-experiments`
- `python-randomness-seeding`
- `python-ml-evaluation`
- `python-model-serialization-security`
- `python-model-serving`
- `python-gpu`
- `python-sklearn`
- `python-pytorch`
- `python-tensorflow`
- `python-jax`
- `python-spark`
- `python-dask`
- `python-airflow`
- `python-mlops`

### 8.13 Documentation and community skills

- `documenting-python`
- `python-readme-writing`
- `python-api-docs`
- `python-tutorial-writing`
- `python-examples`
- `python-architecture-docs`
- `python-adr`
- `python-contributing-guide`
- `python-security-policy`
- `python-changelog`
- `python-migration-guide`
- `python-issue-pr-templates`
- `python-doc-snippet-testing`
- `python-link-checking`
- `python-ci-artifact-verification`

### 8.14 Additional profile-pack coverage

The manifest must also cover these major Python environments through focused
profile references rather than hundreds of equally discoverable top-level
skills:

- environment and workflow tools: PDM, Hatch, Pipenv, tox, nox, and lock/hash
  policy in addition to pip, uv, Poetry, and Conda;
- type ecosystems: mypy, Pyright/basedpyright, stubs, `py.typed`, gradual
  typing, and version-specific typing behavior;
- object model and native boundaries: MRO, metaclasses, slots, weak references,
  import-time effects, C/Cython, `ctypes`, CFFI, PyO3, ABI policy, and buffers;
- runtimes: CPython, PyPy, free-threaded CPython, embedded Python,
  MicroPython/CircuitPython, and Pyodide/WASM, with explicit support levels;
- UI/TUI: Tkinter, Qt/PySide, Kivy, Textual/Rich, and accessibility;
- distributed/scientific systems: Ray, Dagster, Prefect, Kafka clients, SciPy,
  xarray, Numba, MPI, Arrow/Parquet, Protobuf, and schema evolution;
- application protocols: REST/OpenAPI, GraphQL, WebSockets, gRPC, MCP, events,
  and serverless handlers;
- Unicode, internationalization, locale, filesystem, Windows, and time-zone
  correctness;
- malicious-repository handling: prompt injection in source files, symlink
  escape, giant/minified/generated files, hostile filenames, and archive bombs.

Each profile has an explicit support tier. Mentioned-but-unimplemented domains
must be labeled planned rather than counted as delivered.

### 8.15 Rule and skill development skills

- `python-product-thinking`
- `python-rule-research`
- `python-rule-writing`
- `python-rule-validate`
- `fuzz-python-rules`
- `python-doctor-eval`
- `explain-python-rule`
- `writing-python-docs`
- `author-python-skills`
- `validate-python-skills`
- `review-skill-supply-chain`
- `ship-python-doctor`

## 9. Semantic naming contract

The naming system separates mechanically provable diagnostics from semantic
agent/human review. Semantic naming findings are advisory by default and may
block only when an explicit profile has sufficient evidence. It preserves
legitimate short names and compatibility.

- Functions use precise verbs that reveal effects, except where project
  vocabulary, properties/accessors, conversions, constructors/factories, or
  protocol/dunder contracts establish a clearer convention.
- Predicates express an unambiguous truth condition and avoid confusing double
  negation; legitimate states such as `is_empty` remain valid.
- Collections use honest plurality or established collective nouns such as
  `inventory`, `data`, and `children`.
- Time, size, count, distance, rate, currency, angle, and other ambiguous
  quantities include units when types do not already carry them.
- Async, I/O, mutation, and expense are named according to repository/domain
  conventions when the existing name is demonstrably misleading; suffixes are
  not imposed as universal Python style.
- Classes, protocols, aliases, exceptions, fixtures, callbacks, modules, and
  tests use role-appropriate vocabulary.
- Vague names are judged using scope, types, call sites, and domain terms.
- Mathematical notation, coordinates, short comprehensions, standard protocol
  parameters, and documented domain abbreviations receive exemptions.
- Public renames require an API impact and deprecation assessment.

A finding includes symbol role, confidence, evidence, optional ranked
suggestions only when evidence supports them,
public API risk, known references, and analysis completeness. Dynamic `getattr`,
string registration, serialization fields, exports, plugins, reflection,
pickles, and external callers can make reference analysis incomplete; in that
case automatic rename is forbidden.

## 10. Comment and docstring contract

Code explains what and how. Comments explain why, constraints, invariants,
resource/lifetime/concurrency ownership, safety, compatibility, non-obvious
algorithms, or external facts. Human/team ownership belongs in issue tracking
or CODEOWNERS unless an explicit policy requires local metadata.

When diff context exists, each changed comment is evaluated on separate
necessity, accuracy, and risk axes. A comment may simultaneously be stale,
misleading, and dangerous; these are not forced into a single exclusive class.
Misleading comments rank above missing docs.

The analyzer flags narration, stale identifiers, contradicted claims,
commented-out code, source changelogs, TODO/FIXME notes missing the configured
issue/owner/expiry metadata, vague warnings, signature-repeating docstrings, and
unexplained suppressions. Stale, contradicted, and external-fact claims always
carry evidence and confidence; offline analysis does not claim universal truth.

Docstrings are runtime language objects, not comments. Public docstrings include
only contract-relevant sections: behavior, relevant parameter meaning, returns,
raised exceptions, side effects, mutability, concurrency, restrictions, and
examples without duplicating information already clear from names and types.

The preferred rewrite order is rename, introduce domain type, simplify flow,
extract operation, separate responsibility, then comment only if necessary.

## 11. Python Power of Ten safety profile

The supplied article is a source and inspiration, not bundled content. Rule
docs paraphrase it, cite the DOI, explain translation limits, and include a
non-endorsement statement.

Profiles:

- `advisory`: uncertain findings are informational;
- `strict`: high-confidence violations block;
- `safety`: inability to prove a required property blocks.

Safety result states are `satisfied`, `violation`, `unproven`,
`not_applicable`, and `not_evaluated`. `not_applicable` requires rule-specific
machine evidence or an approved human determination; configuration cannot
self-declare a required property inapplicable. Separate reason codes include
`tool_unavailable`, `unsupported_syntax`, `dynamic_dispatch`, and
`judgment_required`. Required safety properties block on `violation`,
`unproven`, `not_evaluated`, or unresolved judgment unless a scoped approved
exception exists.

Rules:

1. `P10-PY01`: statically understandable control flow, including direct and
   indirect recursion, callbacks, generators, exception paths, and dynamic
   dispatch limitations.
2. `P10-PY02`: evidenced bounds for iteration, retries, polling, queues,
   pagination, generators, and streams. Long-lived services may use event loops
   only when per-event work, queue size, deadlines, and shutdown are bounded.
3. `P10-PY03`: bounded memory, collections, queues, caches, payloads, file
   descriptors, sockets, subprocesses, tasks, and concurrency, distinguishing
   static caps, runtime-enforced caps, and empirical high-water evidence.
4. `P10-PY04`: functions small enough to verify, with a default 60 effective
   source-line limit plus complexity, nesting, and cohesive-responsibility
   review.
5. `P10-PY05`: explicit contracts and side-effect-free invariants; runtime
   safety never depends on removable `assert` statements.
6. `P10-PY06`: minimized mutable scope and state lifetime.
7. `P10-PY07`: validated boundaries and consumed meaningful outcomes,
   including exceptions, task/future results, context-manager exits, and
   subprocess return codes.
8. `P10-PY08`: static program shape; restrictions on `eval`, `exec`, dynamic
   imports, import hooks, monkeypatching, runtime generation, and
   configuration-created variants.
9. `P10-PY09`: restricted risky reflection, opaque decorators/proxies,
   `ctypes`, CFFI/native pointers, and FFI boundaries without banning ordinary
   first-class callables.
10. `P10-PY10`: zero blocking diagnostics from the declared required toolchain;
    advisory diagnostics remain visible and do not imply certification.

Each rule page separates the original C-oriented intent, the weaker or changed
Python guarantee, enforceable static checks, runtime/test evidence, human
judgment, and residual risk. In particular, Python cannot literally prohibit
all post-initialization allocation; the adaptation instead requires bounded
queues, caches, collections, tasks, payloads, files, processes, and measured
high-water marks. Configured/static/runtime-enforced limits establish bounds;
empirical high-water measurements only supplement assurance and can never
independently produce `satisfied`. Function-size review combines effective lines with complexity,
nesting, and cohesion so line limits cannot be gamed.
The original assertion-density rule is not translated literally: Python
`assert` may document internal assumptions, but required input or safety
validation must use runtime checks because optimization can remove assertions.
Every checker documents its soundness boundary; general dynamic Python may
produce `unproven` rather than a false proof of safety.

Each rule has valid/invalid fixtures, exact spans, JSON/SARIF goldens,
metamorphic tests, property tests, version tests, false-positive cases,
mutation tests, corpus evidence, remediation, and exception requirements.

Safety exceptions require rule ID, exact scope, technical reason, owner,
evidence, review date, and expiration. No blanket suppressions are allowed.

## 12. Configuration and policy

Use a versioned `python-doctor.toml` or `[tool.python-doctor]` table with one
canonical parsed model. Support profiles, analyzer controls, rule/category
severity, ignores, justified suppressions, source/generated/vendor roots,
blocking threshold, coverage requirements, baselines, skill packs, safety
scope, and bounded-resource declarations.

Configuration validation is strict. Unknown keys, invalid types, conflicting
settings, required-but-disabled analyzers, expired safety exceptions, and
unsupported schema versions fail with actionable messages.

Configuration precedence is versioned and explainable. Configuration does not
interpolate environment variables, load remote includes, execute commands, or
import repository code. Changed-file analysis disables Git external diff and
text conversion, handles shallow or absent merge bases explicitly, and never
runs hooks.

The safety profile pins required rules, analyzers, and blocking thresholds.
Disabling or demoting them requires the same scoped, reviewed, expiring safety
exception; ordinary severity configuration cannot manufacture a clean result.

## 13. Skill quality contract

Every skill satisfies its kind-specific schema from section 8.1. Applicable
fields include:

- a specific trigger and non-goals;
- supported Python versions and environments;
- read-only versus mutation authority;
- authoritative references and license provenance;
- for version-sensitive guidance, authoritative source revision, applicable
  version range, and last-verified date;
- ordered procedure;
- deterministic command matrix and fallbacks;
- for diagnostic/review kinds, evidence, severity, confidence, false-positive,
  and safe-fix policy;
- before/after examples;
- verification and exit criteria;
- fixtures and expected outputs;
- adversarial negative evaluations;
- platform notes.

Skills may not fetch instructions at runtime. Bundled scripts are reviewed as
production code. Third-party ideas require source and license records; linked
content is not assumed to inherit an aggregator's license.

## 14. Evaluation architecture

### 14.1 Diagnostic rule evaluation

- focused positive and negative fixtures;
- exact diagnostic spans and IDs;
- JSON and SARIF golden reports;
- formatting/renaming metamorphic invariance;
- Hypothesis AST/CST generation;
- mutation tests that remove guards or bounds;
- fail-closed parser/analyzer failures;
- offline OSS corpus noise measurement;
- deterministic repeat runs.

### 14.2 Skill evaluation

For each skill:

1. run pressure scenario without the skill;
2. record incorrect behavior or rationalization;
3. add the minimum skill;
4. rerun identical scenario;
5. add adversarial variations;
6. test router composition;
7. validate metadata and references;
8. verify no remote instruction or telemetry behavior.

### 14.3 Compatibility matrix

- CPython 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14;
- Linux, macOS, and Windows for essential packages, with component-specific
  host matrices for integrations;
- `src` and flat layouts;
- packages, applications, workspaces, namespace packages, and typed packages;
- synchronous, asynchronous, threaded, multiprocess, and free-threaded-relevant
  fixtures;
- major supported packaging and lockfile tools.

## 15. Privacy architecture

Privacy is enforced structurally and by tests.

- Runtime packages may not import network clients.
- Delete the existing `network.vulnerability_intelligence` model, configuration,
  tests, documentation, and skill guidance instead of retaining a disabled
  subsystem.
- the CLI schema proves `--offline` is absent because runtime networking does
  not exist and there is no mode to toggle;
  setting an environment variable is not enforcement.
- Socket creation is denied during privacy integration tests in Python Doctor
  and every spawned analyzer process.
- Linux syscall traces and cross-platform socket, DNS, HTTP, and proxy canaries
  must observe zero egress attempts on CLI, API, LSP, editor, skill helper,
  report, failure, and cancellation paths.
- Network-available and network-blocked scans produce identical normalized
  output.
- No environment variable enables reporting.
- No persistent unique identifier is generated.
- No report is uploaded by CI.
- The GitHub Action uses least privilege and emits only exit status plus a
  generic non-source-derived product status. Local annotation-format output may
  be generated for compatibility, but the hosted Action never sends findings,
  paths, reports, annotations, summaries, or artifacts to GitHub.
- Dependency research/download is a separate explicit user-authorized action,
  never a scan side effect.
- The static documentation site contains no analytics or remote assets.
- Secret canaries placed in environment variables, Git configuration, home
  paths, and hostile filenames never appear in diagnostics or crash output.

## 16. Documentation deliverables

Required root documents:

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `PRIVACY.md`
- `LICENSE`

Required detailed documentation:

- architecture and package boundaries;
- installation and 60-second quickstart;
- complete CLI and API references;
- configuration schema and examples;
- diagnostic, severity, confidence, identity, score, and coverage contracts;
- JSON, SARIF, GitHub annotations, and agent handoff schemas;
- rule catalog and how to research, write, validate, fuzz, explain, and release
  rules;
- skill catalog, composition, installation, provenance, and authoring;
- comment, naming, explainability, suppression, and false-positive policies;
- Python Power of Ten provenance, adaptation, profiles, exceptions, migration,
  and individual rule pages;
- LSP/editor setup;
- GitHub Action and local-only CI behavior;
- packaging, release, versioning, deprecation, migration, performance, and OSS
  corpus methodology;
- rule candidate backlog.

README examples are executed in clean environments. Commands, options, schema
versions, supported Python versions, and output samples must match the code.

## 17. Delivery phases

1. Program governance, master specification, prompt, traceability, and gates.
2. Monorepo migration with compatibility layer and package boundaries.
3. Core report/config/discovery/API contracts.
4. Native rules and analyzer orchestration.
5. Naming, comments, explainability, and deslop capabilities.
6. Python Power of Ten safety profile.
7. Full CLI, baselines, caches, hooks, skills, and CI installers.
8. Canonical skill routers, profile packs, and leaf library.
9. Skill evaluation and provenance system.
10. Fuzzing, corpus evaluation, delta audit, and performance harnesses.
11. Language server and editor clients.
12. Documentation site and complete Markdown surface.
13. Packaging, GitHub Action, release automation, SBOM/provenance, and install
    smoke tests.
14. Whole-product adversarial review, privacy audit, compatibility matrix,
    dogfood scan, and final publication.

Each phase receives its own implementation plan and cannot begin until the
prior phase's release gate passes. Gate meanings, task-level RED/GREEN evidence,
package-boundary enforcement, compatibility matrices, adversarial stages, and
publication proof are normative in the companion validation specification.

## 18. Completion definition

The project is complete only when:

- every requirement maps to implemented code, skill, documentation, or an
  explicit non-goal approved in this specification;
- all packages contain functional behavior and package-level tests;
- every `required=true` entry in the versioned release skill manifest exists,
  validates, and has pressure evals; “optional activation” does not mean
  optional delivery, while planned profile domains are excluded from delivered
  claims;
- all ten safety rules and documents exist with false-positive tests;
- all required root and detailed Markdown files exist and validate;
- the full local test, lint, type, build, package, fuzz-smoke, skill-eval,
  privacy, schema, documentation, LSP, editor, action, and compatibility gates
  pass;
- adversarial spec, code-quality, security, privacy, safety, packaging, and
  documentation reviews have no unresolved blocking findings;
- a wheel and sdist install and run successfully in clean environments;
- Python Doctor scans itself with complete required coverage and no blocking
  diagnostics;
- the GitHub repository contains the verified release and documentation;
- the final report states evidence, limitations, and any non-blocking advisory
  findings without hiding them.
