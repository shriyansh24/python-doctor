# Python Doctor Validation and Release Gates

**Status:** User-approved normative release contract; implementation remains
gated by G00

**Purpose:** turn every implementation claim into reproducible evidence at one
immutable candidate commit.

## 1. Gate semantics

Every gate records one state:

- `PASS`: all required assertions ran and passed;
- `FAIL`: a behavioral, compatibility, privacy, security, legal, quality, or
  documentation assertion failed;
- `BLOCKED`: a required prerequisite outside repository/team authority remains
  unavailable after documented alternatives are exhausted;
- `NOT_APPLICABLE`: an explicit machine-verifiable applicability expression is
  false.

`BLOCKED` is never `PASS`. Missing fixtures, dependencies, interpreters,
analyzers, or tools the project owns provisioning are `FAIL`. External platform
blockers require owner, alternatives attempted, retry evidence, and unblock
condition. Tool crashes, timeouts, missing reports, parse failures, unsupported
required syntax, required analyzer absence, skips, and partial scans fail
closed. A flaky test may be retried once to classify it, but the original
failure remains evidence. Quarantine permits unrelated investigation only; it
never converts a mandatory check to `PASS`, and final release requires zero
quarantined mandatory checks.

Aggregate precedence is invalid configuration, `FAIL`, `BLOCKED`, then `PASS`.
If every mandatory child is validly `NOT_APPLICABLE`, the serialized gate state
is `NOT_APPLICABLE` and the process exits `0`; a mixed `PASS`/validly
`NOT_APPLICABLE` gate serializes as `PASS`.
`PASS` requires every mandatory child to pass; exclusions must already be
predeclared, evaluated, and independently reviewed as `NOT_APPLICABLE`.
Unexpected warnings, skips, deselections, xfails, xpasses, retries, collection
errors, and coverage omissions fail the check. Retry success never erases the
initial failure.

States are computed from a version-controlled applicability manifest. Phase
gates require only checks scheduled through that phase; later requirements stay
`PLANNED`, never `NOT_APPLICABLE`. `NOT_APPLICABLE` requires a predeclared,
machine-evaluated repository/platform fact and independent review; it never
means deferred, unsupported, unavailable, or unimplemented. `BLOCKED` is
reserved for a prerequisite outside repository/team authority after documented
alternatives are exhausted and prevents dependent progression.

Every gate emits machine-readable JSON and a short human summary. Evidence may
contain diagnostic metadata and hashes, but never secrets or source snapshots.
Python Doctor never uploads evidence; user-invoked CI or publication systems
operate separately from the product.

Evidence is local, size-bounded, and uncommitted by default. A versioned
redaction scheme replaces source, argv secrets, environment, home paths, Git
configuration, hostile filenames, and terminal controls with deterministic
placeholders. Unsafe raw logs are represented by hashes and summaries.

Phase 1 delivers one canonical gate runner and manifest. Each check declares
gate and requirement IDs, applicability, command, working directory, timeout,
required tools, expected artifacts, and pass criteria. Results bind candidate
commit/tree, dirty state, dependency-lock and fixture/eval-manifest digests,
gate-runner version, platform, Python/tool versions, times, exit code,
warnings/skips, and artifact hashes. Runner exits are `0=PASS`, `1=FAIL`,
`2=BLOCKED`, and `3=invalid gate configuration`. Any candidate or validation
input change invalidates affected evidence.

## 2. Per-task RED/GREEN ladder

### T00 — Task contract

The task identifies requirement IDs, package owners, public contracts, tests,
expected RED/GREEN behavior, compatibility impact, privacy impact,
documentation impact, and rollback method. Ambiguous multi-purpose tasks split
before code changes.

### T01 — Baseline or RED

The contract classifies work as `behavior_change`, `defect_fix`, `pure_refactor`,
or `verification_content`. Behavior and defect tasks require the smallest
meaningful test to fail for the intended reason before implementation. Pure
refactors require passing characterization/equivalence baselines before and
after. Documentation, provenance, metadata, and generated artifacts require a
validator or contract check demonstrated to fail before and pass after. Phrase
presence, “does not crash,” always-true assertions, broad snapshots, unrelated
environment failures, and mocks replacing the behavior do not qualify.

### T02 — GREEN

The new test and package-local suite pass with the smallest correct
implementation. No new warnings, skips, blanket suppressions, networking, broad
exception catches, unrelated edits, or nondeterministic diagnostics appear.

### T03 — Refactor and strength

Behavior remains green after clarity, naming, comments, types, duplication,
function size, and package-boundary review. Changed safety, privacy, schema,
fingerprint, and exit-code decision logic has full branch coverage and kills
every viable generated mutant. Equivalent, invalid, or unreachable exclusions
require mutant ID, rationale, and independent approval. Other thresholds,
scopes, and exclusions are fixed by the approved phase plan before implementation
and may not be weakened after the baseline.

### T04 — Independent review

A non-author challenges test adequacy, false positives/negatives, boundaries,
API/schema compatibility, error/timeout behavior, egress, and documentation.
Every accepted finding produces task-class-appropriate durable prevention: a
behavioral regression, contract validator, schema assertion, documentation
check, provenance rule, or gate assertion, and returns to the corresponding
RED/failing-validator state.

Raw logs, traces, and source-sensitive evidence live under gitignored
`.evidence/` and are never committed or published. Commit only sanitized task
contracts, gate-result manifests, review dispositions, and the evidence index
under `docs/evidence/`; they contain hashes/bounded summaries of raw evidence
and pass secret, source, path, and control-character redaction tests.

## 3. Package dependency gate

The intended dependency direction is:

```text
core <- rules, deslop, adapters, reports <- api <- CLI and language-server
language-server <- VS Code/Cursor and Zed protocol clients
public API/SPI <- fuzz and test-only tooling
documented contracts <- skills and website
```

Core has no CLI, editor, website, GitHub, remote-service, or network dependency.
Rules use the public rule SPI. API is the normal composition root. CLI is not
imported by API/core. LSP does not duplicate diagnostics. Editors contain no
analysis engine. Website and skills do not import private implementation
modules. Import-linter contracts, AST forbidden-import checks, metadata audits,
isolated wheel installs, and an acyclic graph golden enforce the boundary.

## 4. Repository-to-release gates

### G00 — Repository integrity and legal provenance

- known clean checkout and tree hash;
- no merge markers, case collisions, invalid symlinks, committed caches, or
  generated-file drift;
- clean-room approval and source/license inventory;
- restricted-source revision, license path/hash, inspected paths, and exposure/
  taint record; clean-implementer certifications;
- authorized human/legal determination of no prohibited reuse, or `BLOCKED` if
  the authority is unavailable—no unapproved automated comparison;
- version, changelog, metadata, and schemas agree; authorized tags agree, while
  unauthorized tags are recorded `null/not_authorized`;
- CI actions are immutable-SHA pinned.

Failure stops all downstream gates.

### G01 — Compile, format, lint, and type

- all supported Python grammars compile;
- repository formatting and Ruff pass;
- strict configured type checks pass package by package;
- warnings-as-errors compile/import smoke passes;
- no invalid suppressions or unexplained warning filters.

### G02 — Tests, coverage, and collection

- unit and package integration tests pass;
- test collection matches a checked manifest;
- default targets are at least 90% line and 85% branch coverage;
- policy/scoring, privacy, schema, fingerprint, and safety fail-closed branches
  are fully covered;
- changed critical logic meets T03 mutation requirements.

### G03 — Architecture and independent installation

- dependency graph is acyclic and respects package contracts;
- no private cross-package imports or undeclared transitive dependencies;
- each distribution installs and imports independently;
- CLI, API, LSP, and editor paths produce equivalent engine diagnostics.

### G04 — API, schema, and CLI compatibility

- public names, signatures, defaults, exceptions, typing, and Rule SPI match the
  approved baseline or a reviewed migration;
- JSON, SARIF, configuration, Action, LSP, and diagnostic schemas validate;
- diagnostic IDs are never silently reused and fingerprints are stable across
  operating systems;
- CLI stdout/stderr and exit codes match goldens;
- breaking changes require versioning, migration, change fragment, and
  independent compatibility approval.

### G05 — Python and operating-system matrix

PR evidence covers Ubuntu Python 3.9–3.14 plus representative Windows/macOS
minimum, middle, and maximum versions. Release evidence covers the full
supported CPython 3.9–3.14 × Linux/macOS/Windows matrix. Each cell installs the
built wheel and checks imports, CLI, reports, separators, CRLF/LF, Unicode,
spaces/metacharacters, locale/time-zone independence, case sensitivity, and
external-analyzer failure paths. A required cell is `FAIL` when repository
configuration, dependency resolution, project-owned interpreter provisioning,
installation, or tests fail. It is `BLOCKED` only when an externally provisioned
runner/platform remains unavailable after documented alternatives and retries.

Core, API, CLI, native rules, and reports must satisfy this full host matrix and
the declared target-grammar matrix. LSP, Node/Rust editor clients, frameworks,
and optional tools declare exact host/version ranges in a component manifest.
Any narrower range requires an approved host constraint and cannot reduce the
essential-package claim. PyPy and free-threaded CPython have explicit support
tiers gated by their own cells.

### G06 — Native rule conformance

Every rule has valid/invalid pairs, exact location, remediation, non-goal and
false-positive fixtures, documentation, profile behavior, and safe-fix
idempotence where applicable. Blocking rules target at least 98% precision on
the labeled corpus; advisory semantic naming/comment rules target at least 90%
before default enablement. Required safety fixtures require complete recall.
Noisy rules remain experimental or opt-in.

### G07 — Property, fuzz, and regression corpus

Deterministic Hypothesis and grammar-aware suites cover paths, configuration,
AST/CST, reports, fingerprints, deduplication, malformed/partial source,
Unicode, deep inputs, hostile filenames, LSP framing, and CLI arguments.
Invariants include no crashes, deterministic normalized results, valid spans,
fix idempotence, report round trips, and explicit incomplete results on analyzer
failure. Every failure seed is minimized and retained.

### G08 — Mutation strength

No changed mutant survives in policy thresholds, exit codes, rule predicates,
privacy guards, schemas, compatibility, fingerprints, or safety fail-closed
logic. The whole-suite target is at least 90%, with equivalent mutants reviewed
independently rather than excluded for score improvement.

### G09 — End-to-end product workflows

Installed-wheel scenarios cover empty/single-file repositories, src/flat and
namespace layouts, monorepos, syntax errors among valid files, ignores,
generated/vendor paths, missing/crashed analyzers, config precedence, stdin,
all reports, thresholds, fixes and rollback, concurrent file changes, read-only
trees, and hostile paths. Partial failure never scores as clean.

### G10 — OSS corpus quality and noise

A small checked-in permissively licensed fixture corpus and larger explicit
`corpus.lock` define URL, immutable revision, hash, license, and purpose.
Fetching is a separate deliberate preparation step; scanning is offline.
Per-rule precision, accepted-finding deltas, performance, memory, crash, and
timeout evidence pass. Baseline changes require labeled independent review.

### G11 — Skill contracts and pressure evaluation

Every router and leaf validates triggers, delegation, context budget,
read-only/mutation authority, local-only behavior, safety, missing-tool
handling, evidence requirements, and stop conditions. Pressure prompts attempt
to force skipped tests, hidden warnings, blanket suppressions, NASA
certification claims, remote sending, silent installs, unrelated rewrites,
public API renames, indiscriminate comment deletion, production `assert`
validation, unbounded resources, clean-on-crash results, and incompatible
copying. Critical privacy/safety/destructive-action guardrails require 100%; the
overall task-success target is at least 95%.

`evals/skills/manifest.toml` maps every required skill to at least one baseline,
one enabled, two adversarial, and one router-composition case. Each pins fixture
digest, prompt, allowed modules, timeout, required/forbidden actions, expected
file/command artifacts, privacy assertions, and deterministic evaluator checks.
Phrase matching and model self-grading are insufficient.

A local deterministic schema/routing harness over synthetic,
redistribution-safe fixtures is mandatory. Model-executed pressure evaluation
is also mandatory for every router, guidance skill, and agent-facing review
skill. Use a local model when available; an external backend requires separate
authorization and receives only synthetic nonsecret fixtures. A deterministic
evaluator—not the model—scores files, commands, diagnostics, and forbidden
actions. Baseline/enabled trials use the same pinned backend/settings for at
least three trials. Without an authorized backend, affected checks are
`BLOCKED`. Pure executable integrations may omit model execution only when they
declare no guidance behavior and deterministic E2E tests exercise the complete
contract. Model evaluation is never sole gate evidence and never receives a
user repository.

### G12 — Privacy and network denial

Static review finds no telemetry, analytics, crash reporter, update checker,
remote configuration, vulnerability-intelligence client, remote rule/prompt
service, uploader, hidden endpoint, installation/device/user/session ID,
environment inventory, or runtime network client. Dynamic
CLI/API/LSP/editor/skill/report/crash tests deny
networking and trace Python Doctor plus children. DNS, connect, send, proxy, and
HTTP canaries see zero attempts. Available/denied outputs are byte-identical
after documented normalization. Secret canaries never leak. Any unexplained
attempt or leak is release-critical.

Linux uses a network namespace or equivalent OS deny policy plus process-tree
connection-syscall tracing. The compatibility manifest names an accepted
OS-level process-tree deny and observation mechanism for every required macOS
and Windows platform, supplemented by direct-IP, DNS, HTTP, proxy, and child
canaries. Checkout/dependency setup occurs outside the measured process.
Missing or defective project-owned deny/observation implementation is `FAIL`.
The check is `BLOCKED` only when a correctly configured required OS facility or
externally provisioned runner remains unavailable after documented alternatives
and retries; canaries alone never satisfy it. Measurement covers Python Doctor
packages, bundled extension code, helpers, and the spawned language server.
Unrelated host-application
traffic is outside the measured process set, but shipped extension code contains
no endpoint/network call and never asks the host to initiate networking.

### G13 — Security, supply chain, licenses, and provenance

- threat models cover config, executable discovery, subprocesses, paths,
  symlinks, archives, editors, Action, release, and malicious repositories;
- hostile-repository tests prove static metadata parsing, no project/plugin/
  hook execution, safe Git flags, explicit executable resolution, argv-only
  process creation, environment allowlisting and proxy/token stripping,
  root/symlink/device/FIFO containment, bounded files/output/time/memory, and
  complete process-tree cleanup/sandboxing;
- dependencies are locked/hash-pinned and CI actions immutable-pinned;
- vulnerability analysis runs locally from explicitly prepared data;
- dependency licenses, notices, SPDX metadata, secret scan, SBOMs, provenance,
  typosquat/confusion checks, and reproducible builds pass;
- the NASA PDF is not distributed and the restricted reference contributes no
  copied material.

### G14 — Documentation truth

Every command and Python snippet runs against the built distribution. Schemas,
CLI help, rule/skill indexes, internal links, anchors, README quickstart, and
install examples validate offline. Claims for offline behavior, zero telemetry,
versions, rules, skills, reports, and warnings map to passing gate IDs. No NASA
endorsement, formal safety, or “all OSS skills” claim appears.

### G15 — Wheel and sdist

Every distribution builds in isolation, passes metadata checks, has audited
contents, installs from wheel and sdist without development dependencies, tests
extras and entry points, uninstalls cleanly, includes intended skills/schemas/
licenses, excludes caches/secrets/reference checkouts, and reproduces hashes or
documents normalized differences. Only the exact tested artifacts may publish.

### G16 — LSP and editors

LSP tests cover lifecycle, open/change/save/close, incremental/full sync,
partial syntax, cancellation, stale-result suppression, multi-root, config
reload, rename/delete, UTF-16 positions, Unicode, CRLF, diagnostic clearing,
restart, concurrency, JSON-RPC-only stdout, and CLI/API parity. Packaged VS Code/
Cursor and Zed clients install, launch the server, respect workspace trust,
contain no trackers/endpoints, and pass end-to-end handshakes.

### G17 — GitHub Action

Inputs, outputs, exit codes, fixture-repository runs, fork safety, timeouts,
concurrency, immutable action pins, and least-privilege `contents: read` pass.
Normal scans require no token. No source or report client uploads data. The
hosted Action redirects detailed scanner stdout/stderr to an ephemeral local
runner file, sanitizes failure paths, and emits only exit status and generic
non-source-derived product status to hosted logs. It never writes findings,
paths, diagnostics, annotations, summaries, reports, caches, or artifacts to
GitHub logs, APIs, summaries, or storage. Cancellation cannot become success.

### G18 — Performance and resource bounds

The architecture phase pins fixtures, hardware class, cold/warm methodology,
absolute ceilings, and regression thresholds for startup, 10k/100k LOC native
scans, analyzer scans, peak RSS, LSP initial/incremental latency, cancellation,
report cost, cache/queue growth, and repeated-scan memory plateau. Shared-runner
PR measurements may be advisory; release budgets run on a pinned environment.

### G19 — Independent adversarial stages

Non-author reviewers separately challenge architecture/contracts, analyzer
correctness/noise, skills/explainability, privacy/supply chain, integrations/
packaging, and the final release candidate. Critical/high findings must be zero.
Medium exceptions are narrow, owned, evidence-backed, and expiring. Every valid
finding adds a regression. A material fix changes the candidate SHA and
invalidates affected approvals.

### G20 — Release evidence and publication parity

The exact clean candidate produces an evidence bundle with commit/tree/version,
authorized tag or `null/not_authorized`, tool versions, all gate states,
test/coverage/mutation counts, platform
matrix, API/schema compatibility, rule/corpus quality, skill evals, privacy
attestation and egress traces, supply-chain/license/SBOM/provenance results,
artifact manifests and hashes, performance, known limitations, and independent
reviews.

Publication uses only these artifacts. Every authorized remote branch, tag, and
release asset is checked through GitHub against the manifest. Clean
post-publish minimum and maximum Python installations rerun version, CLI, API,
and privacy smoke tests where a package destination was authorized. The final
report may say complete only when every authorized remote state matches the
candidate; external infrastructure remains `BLOCKED` if unavailable.

Publication authority is destination-specific and frozen in an
`authorized_destinations` manifest. Current required scope is source commits/
branches in `shriyansh24/python-doctor`. Unrequested tags, GitHub Releases/Pages,
PyPI, editor marketplaces/registries, containers, and other destinations are
reviewed child `NOT_APPLICABLE`, not blockers. An authorized required
destination that cannot be reached is `BLOCKED`. Local build verification
proceeds independently of publication authority.

## 5. Failure handling

Classify failures as product defect, test defect, compatibility break, privacy
violation, security/supply-chain failure, documentation falsehood, performance
regression, nondeterminism/flakiness, or infrastructure blocker. Product and
test defects return to RED. Privacy violations immediately block publication.
Compatibility breaks require restoration or a reviewed breaking release.
Threshold, baseline, skip, suppression, and quarantine changes require separate
independent review and cannot be smuggled into the implementation that needs
them to pass.
