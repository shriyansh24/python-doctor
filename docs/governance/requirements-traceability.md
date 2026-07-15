# Python Doctor Requirements Traceability

**Status:** Phase 1 input; `governance/requirements.toml` becomes normative when
implemented and validated.

**Phase legend:** P1 governance; P2 monorepo; P3 core/API; P4 rules/adapters;
P5 explainability/deslop; P6 safety; P7 CLI/workflows; P8 skills; P9 skill
evaluation; P10 fuzz/corpus/performance; P11 LSP/editors; P12 docs/site; P13
packaging/Action/release; P14 whole-product validation/publication.

Every row inherits task controls T00–T04: contract, appropriate RED/baseline or
failing validator, GREEN, strength/refactor evidence, and non-author review.

The tables below are a readable index, not a completion oracle. The normative
TOML record for every ID must keep these fields separate: `source_clauses`,
`introduced_phase`, `required_by_phase`, `verification_phases`,
`implementation_artifacts`, `behavioral_evidence`, `gate_check_ids`,
`dependency_ids`, `completion_condition`, `review_required`,
and typed `completion_predicates`. Current-phase and release status are derived
candidate-bound results, never editable requirement fields. A file or test path
alone never closes a row. Exact ID equality is validated against a separately reviewed
fixture/digest, not against the manifest itself.

## Legal and architecture

| ID | Requirement | Phase | Primary artifact/evidence | Gates |
|---|---|---:|---|---|
| LEG-01 | Clean-room development; no copied, translated, paraphrased, or structurally cloned restricted material. | P1–P14 | Provenance register, exposure record, clean-implementer certifications, authorized legal disposition | G00, G13, G19 |
| LEG-02 | Apache-2.0 for original work; preserve compatible imported licenses/notices. | P1, P13 | LICENSE, SPDX metadata, artifact license audit | G00, G13, G15 |
| LEG-03 | Reproducible OSS research with immutable revision, verified license, inspected paths, concept, disposition, and attribution. | P1, P8–P9 | Source inventory, query logs, two-round saturation evidence | G00, G13, G19 |
| LEG-04 | Do not distribute the supplied PDF (`sha256:c762a07be7b8ea65b95e1f1f748efa60f7196d75fdf81181169cfb8e0b2b4c8f`; duplicate uploads byte-identical) or claim NASA endorsement/certification. | P1, P6, P12–P13 | Exclusion manifest, forbidden-claim tests | G13, G14, G15 |
| LEG-05 | Record and validate immutable restricted-source permission/legal determination, grantor authority, AI/adaptation/redistribution/material scope, conditions, and authorized disposition. | P1 | Raw artifact hash outside Git plus sanitized reviewed disposition | G00, G13, G19 |
| LEG-06 | Record exposure/taint status and approved-input-only certifications for every clean implementer/reviewer. | P1–P14 | Contributor certification ledger and independent sampling | G00, G13, G19 |
| ARC-01 | Functional Python-native monorepo packages; no empty parity scaffolds. | P2–P13 | Installable packages with owned behavior/tests | G03, G09, G15 |
| ARC-02 | Acyclic dependency direction; no private cross-package imports. | P2–P14 | Import contracts, dependency golden, parity tests | G03, G19 |
| ARC-03 | Essential packages run on CPython 3.9–3.14 and Linux/macOS/Windows; integrations declare exact support. | P2–P14 | Compatibility manifest and built-wheel matrix | G01, G05, G15 |
| ARC-04 | Canonical root/nested agent instructions and generated client instructions do not drift. | P2, P8, P13 | AGENTS/CLAUDE/instruction generator and drift tests | G00, G03, G14 |

## Core, adapters, API, CLI, and reports

| ID | Requirement | Phase | Primary artifact/evidence | Gates |
|---|---|---:|---|---|
| CORE-01 | Discover pyproject/setup.cfg/setup.py/requirements, uv/Poetry/PDM/Pipenv/Hatch/Conda, src/flat/namespace/editable/path layouts, apps/libraries/typed/stub/test/notebook/migration/generated/vendor regions without executing code. | P3 | Discovery schema and hostile fixtures for each form | G02, G05, G09, G13 |
| CORE-02 | Distinct full/workspace/path/file/changed-file/changed-line/staged/baseline/editor-buffer/safety scopes. | P3, P7, P11 | Selection models and Git-safe E2E for each mode | G04, G07, G09 |
| CORE-03 | Analyze target grammars 3.9–3.14; parser/tool failure is incomplete. | P3–P4 | Grammar capability registry and version corpus | G01, G05, G07 |
| CORE-04 | Strict canonical config/policy, deterministic precedence, profiles, suppressions, baselines, safety and resource declarations. | P3 | Config schema, invalid/precedence goldens | G04, G07, G09, G12, G13 |
| CORE-05 | Stable diagnostic identity/order, proof-carrying evidence, completeness, versioned score, baseline/cache invalidation. | P3–P4 | Claim/evidence/fingerprint/score models and cross-OS goldens | G02, G04, G07, G08 |
| CORE-06 | Preview-first atomic, contained, idempotent fixes with concurrent-change checks and rollback. | P3, P5, P7 | Fix transaction/journal E2E | G07, G09, G13 |
| CORE-07 | Every rule declares stable ID, category, profile severity, maturity, evidence level, versions, capabilities, message/remediation, non-goals, fix authority, skills, docs, and corpus tests. | P3–P10 | Rule schema, registry/docs/corpus bidirectional validator | G04, G06, G07, G10, G14 |
| CORE-08 | Freeze an examination capsule over snapshot/config/profile/provider/resource/privacy/schema digests and detect concurrent input change. | P3 | Capsule schema, contained-copy or before/after digest tests | G04, G07, G09, G12 |
| CORE-09 | Capability graph has typed dependency/refinement/conflict/invalidation/remediation edges, fixed provider choice, and admissible applicability. | P3–P4 | Graph schema, cycle/fallback/conflict tests | G04, G07, G09 |
| CORE-10 | Evidence keeps claim state, coverage, method, confidence, derivation DAG, relation graph, disagreement, and soundness boundaries distinct. | P3–P4 | Evidence/verdict schemas and invariant tests | G04, G07, G08, G09 |
| CORE-11 | Assurance map and baseline report exact evaluated-capability and claim/coverage transitions without domain-wide proof claims. | P3, P7 | Assurance/baseline schemas and transition goldens | G04, G09, G14 |
| ADP-01 | Local analyzers use explicit versioned machine contracts. | P4 | Adapter SPI and real-tool fixtures | G03, G04, G09 |
| ADP-02 | Freeze scan plan and distinguish `not_selected`, `complete`, `partial`, `unavailable`, `failed`, `skipped`. | P4 | Capability planner/state-machine tests | G02, G04, G09 |
| ADP-03 | Analyzer airlock: vetted argv, no shell/plugins/hooks/project imports, minimal environment, process/resource/network containment. | P4 | Malicious config/process/network tests | G07, G12, G13 |
| ADP-04 | Native rule registry is authoritative; no fake Ruff plugin. | P4 | Registry/bridge contract and docs tests | G03, G06, G14, G15 |
| ADP-05 | Initial provider inventory covers Ruff, Bandit, Radon, mypy, configured Pyright/ty, Vulture, and local dependency/lock checks. | P4 | Per-provider contract and real-executable tests | G03, G04, G09, G10 |
| ADP-06 | Threat model covers config, executable resolution, Git, symlinks/devices/FIFOs, archives, editor/Action/release boundaries, dependency confusion, immutable actions, and process cleanup. | P1–P14 | Threat model plus hostile fixtures and supply-chain audits | G12, G13, G17, G19 |
| API-01 | Stable typed sync/async diagnose, inspect, and config APIs. | P3 | Public signature golden and clean-wheel use | G03, G04, G05 |
| API-02 | API does not print, prompt, mutate by default, install, or network; memory cache default. | P3 | Output/filesystem/socket denial tests | G09, G12 |
| API-03 | Typed result/exception hierarchy preserves causes and separates findings/incomplete/config/internal failure. | P3 | Failure-path contract tests | G02, G04, G09 |
| CLI-01 | Implement complete approved command tree with no placeholder commands. | P7 | Installed-wheel help and command E2E | G04, G05, G09, G15 |
| CLI-02 | Stable distinct exits for findings, incomplete/configuration, and internal failure. | P7 | Exit schema goldens and mutations | G04, G08, G09 |
| CLI-03 | Local skill/hook/CI installers are previewable, idempotent, reversible, and never silently install dependencies. | P7–P9 | Temp-repo lifecycle tests | G09, G11, G13, G15 |
| CLI-04 | No share/upload/hosted-score/remote-report/update/telemetry/offline switch. | P7 | Forbidden CLI-schema and network tests | G04, G12, G14 |
| REP-01 | Terminal, JSON, SARIF, local GitHub-annotation text, and agent handoff JSON. | P3, P7 | Schemas, round trips, goldens | G04, G07, G09 |
| REP-02 | Reports expose schema/capsule/profile/mode, relative project identity/location, diagnostic ID/rule/category/severity/inference confidence/evidence/boundary, provider coverage and reasons, skills, fix metadata, score/label, and baseline deltas. | P3 | Versioned claim-envelope/capsule schemas and cross-renderer equivalence | G04, G09 |
| REP-03 | Sanitize secrets, paths, source, ANSI/control input, and hostile filenames. | P3, P10 | Canary and injection tests | G07, G12, G13 |
| REP-04 | Output only to stdout or explicit local destination; never upload. | P3, P7 | Filesystem and network traces | G09, G12 |
| REP-05 | `explain` resolves one occurrence fingerprint within an explicit local result and provides evidence/verification projections; `rules explain` documents rule contracts. | P3, P7 | CLI/API distinction, occurrence identity, trusted-recipe tests | G04, G09, G14 |

## Rules, deslop, fuzzing, and performance

| ID | Requirement | Phase | Primary artifact/evidence | Gates |
|---|---|---:|---|---|
| DED-01 | Python-aware dead modules/functions/imports/dependencies, cycles, layering, flags, globals, and side effects. | P5 | Native analyzers, dynamic uncertainty fixtures, corpus precision | G06, G07, G10 |
| DED-02 | Deterministic confidence-ranked semantic duplicate/similar-symbol mining. | P5 | Similarity engine, metamorphic/corpus evidence | G06, G07, G10, G18 |
| DED-03 | One canonical engine powers API and dedicated deslop CLI. | P5, P7 | API/CLI parity and clean-wheel tests | G03, G04, G09, G15 |
| FUZ-01 | Deterministic AST/CST, malformed source, Unicode, hostile path, and depth/width generators. | P10 | Seeded strategies and resource caps | G07 |
| FUZ-02 | Enforce no-crash, deterministic results, valid spans, fix idempotence, report round trip, and fail-closed invariants. | P10 | Property and mutation suites | G07, G08 |
| FUZ-03 | Minimize and retain redistribution-safe regression seeds for every accepted failure/false positive. | P10 | Corpus manifest and RED/GREEN replay | G07, G10, G13 |
| PERF-01 | Freeze benchmark fixtures, hardware class, method, ceilings, and regression thresholds before optimization. | P10 | Performance policy validator | G18, G19 |
| PERF-02 | Bound startup/scan/RSS/output/process/analyzer/repeated-run resource behavior. | P10 | Pinned measurements and large hostile inputs | G13, G18 |
| PERF-03 | Meet LSP initial/incremental/cancel/restart and memory-plateau budgets. | P11 | Editor benchmark scenarios | G16, G18 |

## LSP, editors, Action, website, packages, and release

| ID | Requirement | Phase | Primary artifact/evidence | Gates |
|---|---|---:|---|---|
| LSP-01 | Saved/unsaved diagnostics, ranges, hovers, evidence, suppressions and safe fixes use canonical engine. | P11 | JSON-RPC and API/CLI/LSP parity | G03, G04, G16 |
| LSP-02 | Full lifecycle/sync/partial syntax/multi-root/reload/UTF-16/Unicode/CRLF/clear behavior. | P11 | Protocol scenario suite | G07, G16 |
| LSP-03 | Cancellation, stale suppression, restart, concurrency, invalidation, JSON-RPC-only stdout. | P11 | Race/property/framing tests | G07, G08, G16, G18 |
| EDT-01 | Thin installable VS Code/Cursor client with workspace-trust behavior. | P11, P13 | Packaged extension handshake/E2E | G12, G15, G16 |
| EDT-02 | Thin installable Zed client with exact support range. | P11, P13 | Packaged launch/handshake | G12, G15, G16 |
| EDT-03 | Editors contain no analysis engine, trackers, endpoints, downloader, or updater. | P11 | Bundle audit and process-set egress tests | G03, G12, G16 |
| ACT-01 | Least-privilege Action with stable contract, fork safety, timeouts, cancellation. | P13 | Fixture repository E2E | G04, G13, G17 |
| ACT-02 | Hosted Action exposes only generic status/exit; no findings, paths, reports, summaries, caches, or artifacts. | P13 | Hosted canary/log/API/storage denial | G12, G17 |
| ACT-03 | Local annotation formatter remains separate from hosted publication. | P13 | Local golden plus hosted denial | G04, G12, G17 |
| WEB-01 | Substantive static documentation site generated from canonical catalogs. | P12 | Offline build/link/route checks | G14, G15 |
| WEB-02 | No analytics, cookies, pixels, remote fonts/assets, or client telemetry. | P12 | Offline browser and endpoint audit | G12, G14 |
| PKG-01 | Isolated wheels/sdists contain correct metadata, extras, entry points, schemas, skills, licenses/notices. | P13 | Metadata/content and clean-install tests | G13, G15 |
| PKG-02 | Artifacts exclude caches, secrets, raw evidence, restricted checkout, PDF, and unintended files. | P13 | Archive/secret/license/uninstall audit | G13, G15 |
| PKG-03 | Exact built artifacts pass full supported matrix. | P13–P14 | Wheel matrix for CLI/API/reports/rules | G05, G09, G15 |
| PKG-04 | Rebuild hashes match or normalized differences are bounded/reviewed. | P13 | Independent clean rebuild | G13, G15, G20 |
| REL-01 | Version, changelog, fragments, schemas, deprecations, and migrations agree. | P1, P13 | Metadata consistency validator | G00, G04, G14 |
| REL-02 | Local SBOM, dependency/license inventory, notices, and artifact provenance. | P13 | Schema/license/hash validation | G13, G15, G20 |
| REL-03 | Build exact artifacts from clean immutable candidate; no substitution. | P13–P14 | Candidate/artifact identity checks | G00, G15, G20 |
| REL-04 | G00–G19 and non-author release review pass at one candidate before publication. | P14 | Gate ledger and approvals | G19, G20 |

## Skills and Python safety

| ID | Requirement | Phase | Primary artifact/evidence | Gates |
|---|---|---:|---|---|
| SKL-01 | Canonical `skills/`, generated host copies, no absolute/workspace fallback. | P8 | Sync/relocation/drift tests | G00, G11, G15 |
| SKL-02 | Eleven routers, deterministic progressive disclosure, no cycles, one-router/five-leaf budget. | P8 | Capability graph and ambiguous routing tests | G11 |
| SKL-03 | Deliver all required manifest entries; profile domains have honest delivered/planned/unsupported tiers. | P8–P9 | Frozen release manifest and completeness validator | G11, G14, G15 |
| SKL-04 | Semantic naming covers roles, types, calls, units/effects/domain terms, exemptions, and public API risk. | P5, P8 | Adversarial naming fixtures/corpus | G06, G10, G11 |
| SKL-05 | Comment/docstring truth and self-explanatory rewrite order preserve necessary rationale/contracts. | P5, P8 | Necessity/accuracy/risk cases | G06, G10, G11 |
| SKL-06 | Kind-specific metadata defines owner, triggers, conflicts, lifecycle, capabilities, support, context, authority, evals. | P8 | Schema/conflict/authority validators | G11, G13, G15 |
| SKL-07 | Mandatory local schema/routing harness plus model-executed baseline/enabled/two-adversarial/composition evals for agent-facing skills; synthetic-only inputs, authorized backend, identical pinned settings, three trials, deterministic non-model scorer, 100% critical guardrails, ≥95% task success, and BLOCKED without backend. | P9 | Eval manifest, trial transcripts, deterministic artifacts/actions scorer | G11, G12, G19 |
| NASA-01 | Advisory/strict/safety profiles use satisfied/violation/unproven/not-applicable/not-evaluated plus reason codes. | P6 | Result/profile transition tests | G04, G06, G08 |
| NASA-02 | P10-PY01 understandable control flow and direct/indirect recursion/dynamic limitations. | P6 | SCC/callback/generator/exception fixtures | G06–G08, G10 |
| NASA-03 | P10-PY02 evidenced iteration/retry/poll/pagination/stream/queue/event-loop bounds. | P6 | Bounded/unbounded/deadline/shutdown fixtures | G06–G08, G10 |
| NASA-04 | P10-PY03 bounded collections/cache/payload/descriptors/sockets/processes/tasks/concurrency. | P6 | Static/runtime/high-water/leak tests | G06–G08, G10, G18 |
| NASA-05 | P10-PY04 60 effective lines plus complexity/nesting/cohesion. | P6 | Line-gaming and cohesion cases | G06–G08, G10 |
| NASA-06 | P10-PY05 contracts/invariants; required validation survives `python -O`. | P6 | Optimized-mode tests | G05–G08, G10 |
| NASA-07 | P10-PY06 minimized mutable scope/lifetime. | P6 | Local/nonlocal/global/class/alias cases | G06–G08, G10 |
| NASA-08 | P10-PY07 boundary validation and meaningful outcomes/exceptions/tasks/context/subprocess results. | P6 | Ignored/consumed result fixtures | G06–G08, G10 |
| NASA-09 | P10-PY08 restrict eval/exec/dynamic imports/hooks/monkeypatch/runtime generation. | P6 | Static/dynamic shape cases | G06–G08, G10, G13 |
| NASA-10 | P10-PY09 control risky reflection/proxies/decorators/native/FFI boundaries. | P6 | Benign callable vs opaque/native cases | G06–G08, G10, G13 |
| NASA-11 | P10-PY10 zero blocking diagnostics from complete declared toolchain, advisories preserved. | P6 | Missing/crashed/advisory/blocking tests | G04, G06–G10 |
| NASA-12 | Safety exceptions are exact, owned, evidenced, reviewed, and expiring; no blanket demotion. | P6 | Missing/expired/overbroad tests | G04, G06, G08, G14, G19 |

## Privacy, documentation, QA, and publication

| ID | Requirement | Phase | Primary artifact/evidence | Gates |
|---|---|---:|---|---|
| PRIV-01 | No telemetry/analytics/crash/exporter/ID/hosted score/upload/remote prompt/rule/config/vulnerability/update subsystem. | P1–P14 | Forbidden-capability and artifact audits | G00, G12, G13, G19 |
| PRIV-02 | Scanner/API/LSP/editors and diagnostic helpers initiate no networking or scanned-code execution. General intervention/verification skills may run project commands only with explicit authority, network-denied containment, and recorded command scope. | P3–P14 | OS process-tree denial/observation and skill authority receipts | G03, G11, G12, G13 |
| PRIV-03 | Only explicit outputs/cache/fix destinations; default has no persistent side effect. | P3–P14 | Filesystem and identifier snapshots | G09, G12 |
| PRIV-04 | No source/finding/path/env/Git/home/secret/control leakage to unauthorized/public evidence, fingerprints, crash output, or unselected sinks. Explicit local reports may contain findings and normalized relative paths, but never secrets, absolute paths, or unrequested source. | P3, P10, P14 | Canary tests and gitignored raw evidence | G07, G12, G13, G20 |
| PRIV-05 | CI/Action never uploads scanned information. | P13–P14 | Hosted log/API/storage denial | G12, G17 |
| PRIV-06 | Network-available/denied normalized results are byte-identical. | P10, P14 | Paired product-surface runs | G12 |
| DOC-01 | Required root governance/community/privacy/license documents exist and ship correctly. | P1, P12–P13 | Required-file and metadata validators | G00, G14, G15 |
| DOC-02 | Complete architecture/install/CLI/API/config/rule/skill/safety/integration/release docs. | P12 | Catalog completeness | G14 |
| DOC-03 | Execute quickstart, commands, snippets, schemas, and install examples against built artifacts offline. | P12–P14 | Docs harness and clean environment | G14, G15 |
| DOC-04 | Every public claim maps to passing gates; prohibit “all OSS” and certification marketing. | P12–P14 | Claim registry and forbidden-claim audit | G14, G19, G20 |
| QA-01 | One canonical executable gate runner/manifest with exact state/exit semantics. | P1 | Runner self-tests | G00–G20 |
| QA-02 | Evidence binds commit/tree/dirty/locks/fixtures/runner/platform/tools/commands/exits/artifacts. | P1–P14 | Tamper/invalidation/redaction tests | G00, G02, G19, G20 |
| QA-03 | ≥90% line/≥85% branch overall; full changed critical decision branches; all viable changed critical mutants killed; ≥90% whole-suite mutation; exclusions independently reviewed. | P3–P14 | Coverage/mutation reports and exclusion ledger | G02, G08 |
| QA-04 | Per-rule positives/negatives/non-goals/spans/reports/properties/versions; ≥98% blocking precision, ≥90% naming/comment precision before default, complete required safety-fixture recall. | P4–P10 | Per-rule precision/recall and corpus evidence | G06, G07, G10 |
| QA-05 | Independent spec, quality, adversarial, privacy, packaging, and release reviews at exact candidate. | P1–P14 | Finding dispositions and re-review | G19 |
| QA-06 | Dogfood complete deterministic Python Doctor self-scan. | P10, P14 | Repeated network-denied self-scan | G09, G10, G12, G18, G19 |
| PUB-01 | Destination-specific authority; current required scope is source branches in `shriyansh24/python-doctor`. | P13–P14 | Authorized-destinations manifest | G20 |
| PUB-02 | Publish exact verified candidate and compare full remote tree. | P14 | GitHub branch/commit/tree parity | G20 |
| PUB-03 | Perform applicable post-publication smoke and issue evidence-backed final report. | P14 | Remote checkout/install/API/CLI/privacy smoke | G20 |

## Closure rule

A requirement closes only when owner, task IDs, implementation commit,
behavioral/validator evidence, reviewer disposition, candidate identity, and
exact gate assertions are recorded. Scaffolding, phrase search, compile-only
integration, initialize-only LSP, skipped analyzer, one-platform run, README
assertion, an offline environment variable, or review of another SHA cannot
close a row.
