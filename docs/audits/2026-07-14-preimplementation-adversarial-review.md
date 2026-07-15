# Python Doctor Pre-implementation Adversarial Review

**Date:** 2026-07-14

**Repository basis:** local HEAD `0b4ee88`; the reviewed control documents were
uncommitted and therefore all findings remain open. Their final commit/tree and
SHA-256 hashes must be added to the gate ledger after approval.

**Restricted reference basis:** commit
`d8b2989fd5d440d70931743a88ab6f7a91cf7b89`; license-file path/hash,
already-inspected paths, and taint determination remain pending an authorized
human/legal reviewer.

**Scope:** proposed complete Python Doctor program, universal Python skill
system, autonomous execution prompt, safety adaptation, privacy constraints,
packaging, integrations, and publication.

**Verdict:** the existing repository is a useful prototype, not evidence of the
new scope. Production implementation is blocked until the specification and
legal/provenance gate are approved.

## Stop-ship findings and dispositions

### A-01 — Restricted reference license (`OPEN / STOP-SHIP`)

The inspected React Doctor reference uses a modified license that restricts
automated-AI use. Copying or closely paraphrasing its implementation, tests,
prompts, skills, Markdown, or assets into Apache-2.0 Python Doctor is prohibited.

**Disposition:** quarantine the checkout; no further automated processing
without prior written permission from the copyright holder or a documented
legal determination; record the exact revision, license-file path/hash,
inspected paths, and exposure/taint status. Future clean implementers receive
only approved user requirements and public Python standards. Restricted-source
comparison requires an authorized human/legal reviewer; otherwise the legal
gate remains `BLOCKED`.

### A-02 — Offline claim is not currently enforced (`OPEN / STOP-SHIP`)

The prototype parses `--offline`, but the execution model relies on an
environment variable that subprocesses may ignore. That does not prevent socket
creation or prove absence of egress.

**Disposition:** remove redundant nominal controls or enforce the invariant
structurally; deny and observe network syscalls for Python Doctor and all child
processes; compare normalized output with networking available and denied.

### A-03 — Existing optional networking contradicts the approved product (`OPEN / STOP-SHIP`)

The prototype includes vulnerability-intelligence configuration and skill/docs
guidance for remote behavior. A disabled flag would preserve an unacceptable
subsystem.

**Disposition:** remove the model, configuration, tests, docs, and guidance.
Product execution has no network-capable feature and no telemetry setting.

### A-04 — Current skill validation is superficial (`OPEN / STOP-SHIP`)

Phrase-presence assertions do not demonstrate correct triggering, routing,
read-only boundaries, safe fixes, local-only behavior, or evidence-backed
completion. An installed launcher also contains a workspace-specific fallback.

**Disposition:** canonical distributable skill source; no absolute workspace
fallback; baseline-versus-skilled pressure runs; ambiguous/adversarial prompts;
behavioral routing and mutation-authority checks; wrapper drift validation.

### A-05 — Parity could be faked by scaffolding (`OPEN / STOP-SHIP`)

A directory-name checklist can be satisfied with empty packages while none of
the promised user workflows operate.

**Disposition:** parity is a requirements-to-behavior matrix. Each declared
package needs working behavior, tests, integration, documentation, and ownership.
Empty packages, `NotImplementedError`, and nominal editor/site shells fail gates.

### A-06 — Publication integrity is not yet reproducible (`OPEN / STOP-SHIP`)

Local branch/upstream state and the hosted repository must be proven to refer to
the same reviewed candidate.

**Disposition:** release evidence binds commit, tree, version, tag, packages,
hashes, remote branch, hosted artifacts, and post-publish clean installs.

## Required traceability families

The implementation matrix must use stable identifiers across plans, tests,
reviews, and release evidence:

- `LEG-*`: clean-room process, Apache-2.0, OSS provenance;
- `ARC-*`: monorepo behavior, compatibility, package boundaries;
- `CORE-*`: discovery, syntax versions, rules, semantics, identity, coverage,
  suppressions, changed-code analysis, safe fixes;
- `ADP-*`: external analyzer contracts and subprocess trust boundaries;
- `API-*`, `CLI-*`, `REP-*`: public contracts and deterministic reports;
- `LSP-*`, `EDT-*`, `ACT-*`, `WEB-*`: real end-to-end integrations;
- `DED-*`, `FUZ-*`, `PERF-*`: duplicate/dead-code analysis, robustness, budgets;
- `PKG-*`, `REL-*`, `PUB-*`: distributable artifacts and publication parity;
- `SKL-*`: routers, progressive disclosure, naming, comments, explainability,
  behavioral evaluation, host portability;
- `NASA-*`: faithful mapping, profiles, proof language, exceptions, disclaimer;
- `PRIV-*`: no telemetry subsystem, prompts, uploads, or unexplained egress;
- `DOC-*`, `QA-*`: executable documentation, matrices, corpus review, and
  claim-to-test evidence.

Every requirement needs an owner, implementing artifact, behavioral tests,
review evidence, and a final immutable result.

## Adversarial domains required before release

- hostile repositories, prompts in source, symlink/path escape, giant files,
  Unicode, partial syntax, generated/vendor content, and analyzer failure;
- naming exemptions for mathematical notation, callbacks, type variables,
  conventional abbreviations, public API compatibility, units, I/O, mutation,
  and async behavior;
- comment cases spanning useful rationale, stale claims, misleading concurrency
  guarantees, public contracts, safety traceability, TODO ownership, and
  justified suppressions;
- direct/indirect recursion, dynamic call targets, unbounded retries, streams,
  queues, caches, native-memory boundaries, and optimized-away assertions;
- wheel/sdist contents, isolated installs, version/OS behavior, action
  permissions, LSP framing, editor installation, and static-site assets;
- source/dependency network reachability, subprocess egress, crash paths,
  secret canaries, upload clients, remote fonts, and hidden endpoints;
- provenance, incompatible licenses, dependency confusion, typosquatting,
  reproducible builds, SBOMs, CI action pinning, and artifact identity.

## False-completion denial checklist

Do not accept completion based on scaffolding, wrapper counts, phrase-search
skill tests, an environment variable called offline, a telemetry word search,
one OS/Python test cell, synthetic-only rule fixtures, skipped analyzers, a
compile-only editor extension, initialize-only LSP, empty documentation shell,
README claims, or review of an older SHA.

Any material fix after final review produces a new candidate SHA and invalidates
the affected approvals.

## Closure requirements

Each finding closes only when its owner, requirement IDs, regression tests,
evidence paths, reviewer, candidate identity, and re-review result are recorded
in the gate ledger. Editing this audit or any normative control document
invalidates the prior document hashes and requires another independent review.
