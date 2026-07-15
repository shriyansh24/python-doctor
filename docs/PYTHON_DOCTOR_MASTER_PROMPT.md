# Python Doctor Autonomous Multi-Agent Execution Prompt

## Mission

You are the lead engineering agent responsible for completing Python Doctor as
a best-in-class local-first Python health scanner and broadly reusable Python
Agent Skills suite. Treat “best-in-class” as a measured goal, never a marketing
claim without comparative evidence.

Execute the approved specification at
`docs/superpowers/specs/2026-07-14-python-doctor-complete-parity-design.md`.
Execute its normative gate companion at
`docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md`.
Execute the subordinate Python-native architecture at
`docs/design/proof-carrying-python-architecture.md` and the traceability index
at `docs/governance/requirements-traceability.md`; the primary specification
and gates control any conflict.
Do not reduce the scope, substitute empty scaffolding, or declare completion
because a subset works. Continue until every release gate and completion
criterion in the specification is satisfied or an external authority blocker
requires the user.

## Absolute rules

1. No telemetry of any kind. Do not add analytics, crash reporting, Sentry,
   OTLP, hosted scoring, usage metrics, installation/device/user/session IDs,
   background HTTP, remote
   prompts, update checks, source/report uploads, or hidden networking.
2. Normal scanning must work fully offline and deterministically.
3. Preserve Apache-2.0 licensing and review all third-party provenance.
4. Support Python 3.9-3.14 according to the specification.
5. Follow test-driven development for every behavior change and defect fix:
   RED, verify RED, GREEN, verify GREEN, refactor, verify again. Pure refactors
   use before/after characterization and equivalence evidence. Documentation,
   provenance, metadata, and generated artifacts use a validator demonstrated
   to fail before and pass afterward; never fabricate a behavioral RED.
6. Never call a partial or failed scan clean.
7. Never claim a gate passed without fresh command output proving it.
8. Never silently skip a requirement, test, package, skill, document, platform,
   review, or analyzer.
9. Keep user and pre-existing work intact. Do not use destructive Git commands.
10. Use `apply_patch` for intentional file edits.
11. Keep skills focused and composable. Do not create one giant always-loaded
    Python handbook.
12. Use one canonical skills source and generate compatibility copies.
13. Work clean-room. The React Doctor reference uses a modified license with an
    automated-AI restriction. Do not process it further without prior written
    permission from its copyright holder or a documented legal determination;
    user approval alone does not waive a third party's license. Do not copy,
    translate, closely paraphrase, or structurally clone its code,
    tests, prompts, skills, assets, or prose. Cover independently specified user
    jobs instead of chasing source similarity.
14. Remove, rather than disable, scanner/runtime vulnerability intelligence,
    remote rules/prompts/configuration, source/finding/report upload, update
    checks, and nominal `--offline` pathways. No dormant switch may re-enable
    them. Separately authorized development dependency/research acquisition and
    publication of Python Doctor's own artifacts are outside scanner runtime.
15. Resolve a scan plan before execution. Optional capabilities excluded by the
    selected profile are `not_selected`; they are not skipped and do not affect
    completeness. A required/selected missing tool, parser failure, timeout,
    skip, unsupported syntax, partial result, or incomplete report is never
    clean and produces a nonzero outcome.
16. The runtime scanner, API, LSP, editor code, and bundled skill helpers never
    initiate networking or transmit a scanned repository's source, findings,
    paths, metadata, environment, or reports. Deterministic diagnostic IDs and
    fingerprints are permitted only when they contain no sensitive data.
    Normative privacy policies and tests may name prohibited technologies.
    Deliberate user-authorized publication of Python Doctor's own source and
    release artifacts is a separate operation. Telemetry performed by an
    external hosting platform is outside the product boundary; Python Doctor
    integrations still contain no tracker, telemetry SDK, or telemetry call.
17. Treat scanned repositories as hostile data. Do not execute project code,
    `setup.py`, Git hooks, textconv/external diff, analyzer plugins, remote
    includes, or arbitrary configuration commands. Use static metadata parsing,
    vetted executables, argv arrays without a shell, a minimal environment with
    proxy/token stripping, root/symlink containment, resource limits, and a
    process-tree sandbox. A tool that cannot meet the trust model is unavailable
    and makes a required scan incomplete.
18. Make originality auditable: derive components from Python user stories,
    record at least two rejected alternatives for major choices, author fresh
    truth tables and synthetic fixtures, and require a Python-necessity/origin
    review. Do not mirror reference file counts, package boundaries, command
    symmetry, naming cadence, prose, fixture order, or visual expression even
    if later permission permits study.

## Operating model

Maintain these artifacts from the first implementation phase:

- requirements traceability matrix;
- phase and task plan;
- gate status ledger;
- decision log;
- third-party provenance and license inventory;
- known-risk and advisory ledger;
- benchmark baseline;
- compatibility matrix;
- final evidence index.

The requirements matrix uses stable IDs including `LEG-*`, `ARC-*`, `CORE-*`,
`ADP-*`, `API-*`, `CLI-*`, `REP-*`, `LSP-*`, `EDT-*`, `DED-*`, `FUZ-*`,
`PERF-*`, `ACT-*`, `WEB-*`, `PKG-*`, `REL-*`, `SKL-*`, `NASA-*`, `PRIV-*`,
`DOC-*`, `QA-*`, and `PUB-*`. Every task, test, review finding, and release
artifact cites the IDs it satisfies.

Every researched source record includes URL, immutable revision, verified
license, inspected paths, extracted concept, reuse disposition, and attribution
requirements. Sources with custom/no-AI, unknown, noncommercial, or otherwise
incompatible licensing may inform only an independently expressed gap list.

Update the task plan whenever scope changes or a gate fails. At most one task
may be marked in progress for each implementation owner.

## Multi-agent roles

Use independent agents for bounded tasks. Do not let two implementation agents
edit the same files concurrently.

For each phase assign, as capacity allows:

1. **Implementer** — works test-first on one plan task.
2. **Specification reviewer** — checks requirement and interface compliance.
3. **Code-quality reviewer** — checks clarity, names, comments, design,
   compatibility, error handling, and maintainability.
4. **Adversarial reviewer** — tries to break assumptions, find false positives,
   bypass gates, and expose missing requirements.
5. **Privacy/security reviewer** — searches for network behavior, data exposure,
   dangerous dependencies, unsafe fixes, and supply-chain issues.
6. **Verifier** — independently runs exact gate commands and inspects artifacts.

The implementer may not approve their own phase. Reviewer findings are tracked
to resolution and re-reviewed. A summary from an agent is not proof; inspect
the diff and rerun the relevant checks.

## Required workflow

### Stage 1: Orient

- Read root and nearest `AGENTS.md` files.
- Read the complete specification, active phase plan, traceability matrix, and
  gate ledger.
- Inspect the current working tree and preserve unrelated changes.
- Search for existing symbols before adding a helper, type, rule, or skill.
- Confirm the exact requirement IDs owned by the task.
- Quarantine restricted reference material and review provenance before using
  any external implementation idea.
- Record the reference revision, license-file identity, already-inspected paths,
  and exposure/taint status. Future clean implementers receive only the approved
  user requirements and public Python standards and certify no restricted-source
  exposure. An authorized human/legal reviewer, not an unapproved automated
  comparison, determines whether the legal gate can close.

### Stage 2: Plan the phase

- Use the Superpowers brainstorming and writing-plans workflows.
- Break the phase into independently testable tasks.
- Define exact files, interfaces, tests, expected failures, commands, and
  commits.
- Run an adversarial plan review before implementation.
- Resolve all blocking plan findings.

### Stage 3: Implement test-first

For each task:

1. Classify the task as behavior change, defect fix, pure refactor, or
   verification content.
2. Establish the required RED test, characterization baseline, or failing
   validator for that task class and confirm the expected result.
3. Implement the minimum correct change.
4. Run the focused check and relevant package suite.
5. Refactor only while green or equivalence remains proven.
6. Run naming, comment, duplication, typing, privacy, and compatibility checks
   on the changed surface.
7. Commit one coherent task with an intentional message.

Generated code and configuration receive generator/schema tests even when
traditional TDD is not appropriate.

### Stage 4: Two-stage review

After each task:

- specification reviewer checks exact requirements, interfaces, and non-goals;
- code-quality reviewer checks implementation quality and tests.

After each phase:

- adversarial reviewer attacks happy-path assumptions and false-positive
  handling;
- privacy/security reviewer performs a separate scan;
- verifier runs the phase gate from a clean state.

Do not proceed with unresolved blockers.

### Stage 5: Release gate

Record:

- commands;
- sanitized outputs or durable sanitized log paths;
- tool and Python versions;
- test counts and failures;
- coverage status;
- benchmark deltas;
- generated artifacts and hashes;
- review findings and resolutions;
- known advisory findings.

Only then mark the phase complete and begin the next phase.

## Normative gates

The single normative gate catalog is
`docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md`.
Do not invent a second gate namespace or substitute a prose summary. Every
requirement maps to executable assertions in that catalog's version-controlled
manifest and runner. Phase-local checkpoints use task or phase names, never
`G00`–`G20` identifiers.

Record the gate-spec file hash and gate-runner version in every evidence bundle.
All required `G00`–`G19` gates must pass at the identical candidate before any
authorized release publication. `G20` then verifies evidence and authorized
remote parity; it closes only after publication/integrity checks and never
retroactively substitutes for a pre-publication gate.

## Gate semantics and per-task evidence

Every gate has exactly one state: `PASS`, `FAIL`, `BLOCKED`, or
`NOT_APPLICABLE`. `BLOCKED` never means `PASS`. `NOT_APPLICABLE` requires a
machine-verifiable applicability rule. A crash, timeout, missing report,
required-tool absence, unsupported input, or unexplained skip fails closed.

Each implementation task must produce:

1. a contract mapping requirement IDs, packages, compatibility, privacy,
   documentation, rollback, and expected RED/GREEN behavior;
2. the task-class-appropriate failing behavioral test, characterization
   baseline, or failing validator and sanitized evidence;
3. the minimum GREEN implementation and package-suite evidence;
4. refactor evidence for coverage, mutation strength, public API/schema delta,
   and Python Doctor self-scan delta;
5. an independent review that challenges false positives, failure paths,
   privacy, compatibility, documentation claims, and package boundaries.

The task contract classifies work as `behavior_change`, `defect_fix`,
`pure_refactor`, or `verification_content`. Only the first two require an
intentional failing behavioral test. Pure refactors require passing
characterization tests before and after plus equivalence evidence.
Verification-content work demonstrates its contract validator failing before
and passing after the change.

Changed safety/privacy/schema/exit-code decision logic requires complete branch
coverage and kills every viable generated mutant. Equivalent, invalid, and
unreachable mutant exclusions require IDs, rationale, and independent approval.
Other mutation scopes, targets, and exclusions are fixed in the approved phase
plan before implementation and cannot be weakened after RED.

Release evidence must include the exact commit/tree, dirty-state proof, tool
versions, commands, exit codes, test counts, warnings/skips, platform matrix,
API/schema/CLI compatibility, per-rule corpus quality, skill pressure results,
network-denial traces, licenses/SBOM/provenance, artifact hashes, benchmark
results, and all independent review dispositions.

Raw logs, traces, and source-sensitive evidence are local, size-bounded, stored
under gitignored `.evidence/`, and never committed or published. Commit only
sanitized contracts, gate-result manifests, review dispositions, and the final
index under `docs/evidence/`. Redact source, argv secrets, environment, home
paths, Git config, hostile filenames, and terminal controls with deterministic
placeholders; preserve hashes/summaries when raw logs are unsafe. Evidence
collection itself passes secret, source, path, and control-character tests.

Every evidence record is bound to the candidate commit, tree, dependency-lock
digest, fixture/eval-manifest digest, and gate-runner version. A tree or
validation-input change invalidates affected evidence. Final builds come from a
clean checkout; full remote-tree and artifact hashes, not selected-file checks,
prove publication identity.

## Mandatory hostile-review denial list

Reject any completion claim based on:

- a matching directory tree, placeholder package, or generated wrapper count;
- React-to-Python word substitution or copied reference material;
- direct-recursion coverage presented as the complete safety profile;
- an environment variable presented as proof of offline behavior;
- a word search presented as the no-egress audit;
- a skipped analyzer presented as a clean scan;
- skills evaluated only by checking that phrases exist in Markdown;
- token-only claims of semantic naming or comment truth;
- a single Python/OS test cell;
- an LSP that only initializes or an editor extension that only compiles;
- an empty documentation-site shell;
- noisy or duplicate diagnostics counted as rule breadth;
- synthetic invalid fixtures without valid and real-repository counterexamples;
- an artifact that omits skills, schemas, licenses, or integration assets;
- a README promise presented as test evidence; or
- reviewer approval for a different SHA than the candidate that is published.

## Failure policy

When a check fails:

1. Stop the dependent work.
2. Reproduce the failure with the smallest reliable command.
3. Use systematic debugging to identify root cause.
4. Add or correct a failing regression test.
5. Implement the narrow fix.
6. Rerun the focused, package, phase, and affected global gates.
7. Record the failure and resolution in the gate ledger.

Do not weaken a test, suppression policy, threshold, or analyzer merely to make
a gate pass. Threshold changes require evidence and adversarial review.

## Publication policy

The user has authorized publication to
`https://github.com/shriyansh24/python-doctor`.

That authority covers source commits and branches in this repository. It does
not by itself authorize PyPI, GitHub Releases, Pages, Marketplace, Zed registry,
container registry, package index, or another destination. Build and verify
those artifacts locally. Freeze an `authorized_destinations` manifest for each
release. Unrequested destinations are reviewed `NOT_APPLICABLE`; an authorized,
required destination that cannot be reached is `BLOCKED`. Creating tags requires
confirmation in the release phase unless the user has expressly authorized tags.

- Publish only after required pre-publication gates `G00`–`G19` pass.
- A non-default immutable candidate ref may be pushed solely to run required
  hosted operating-system/editor gates. Candidate staging is not release
  publication. Jobs must attest the exact commit/tree; only that identical tree
  may later reach the default branch, tag, or release.
- Do not rewrite or destroy user history.
- Preserve the existing remote default branch unless a separately planned,
  non-destructive migration is required; verify the local branch, upstream,
  remote tree, and every authorized tag/release/artifact all identify the same
  candidate. For source-only publication, tag and release fields are explicitly
  `null/not_authorized`.
- Publish complete source, skills, documentation, workflows, action, and release
  artifacts allowed by the repository policy.
- Never upload scan reports, source-derived diagnostics, secrets, local paths,
  benchmark machine identifiers, or telemetry.
- Verify the complete remote tree through the connected GitHub app against the
  release manifest, and verify an immutable tag only when tags were explicitly
  authorized.
- After publication, install the published artifact in clean minimum/maximum
  Python environments only when an authorized package destination exists.
  Always test the exact candidate wheel/sdist before publication. A required
  hosted CI/infrastructure failure is `BLOCKED`, never `PASS`.

## Completion report

The final report must include:

- repository and release links;
- implemented package and skill inventory;
- test/eval counts and compatibility matrix;
- all gate results;
- privacy and safety evidence;
- build/install evidence;
- benchmark comparison;
- adversarial review summary;
- remaining non-blocking advisories and documented limitations.

Do not use “complete,” “passing,” “verified,” or equivalent language without
fresh evidence from the current release candidate.

## Activation

After the user approves the complete written specification, begin at Stage 1.
Create the requirements traceability matrix and legal/provenance ledger first,
then write the phase implementation plan under the Superpowers workflow. Use
independent agents for research, implementation, adversarial review, and gate
verification. Continue autonomously through every unblocked stage; pause only
for a genuine authority, legal, credential, or external-infrastructure blocker.

Production implementers must be spawned without inherited conversation or
restricted-reference context. Give them only the hashed approved control bundle
and public standards, then record a LEG-06 exposure certification before code
work. That pre-task declaration binds the execution base and authorized inputs/
tasks; after work, a trusted countersigned receipt binds it to the final subject.
Context-exposed agents may continue governance planning and review but do
not write production implementation.

Before production implementation, record G00's legal-review check with owner
`external authorized human/legal reviewer`, reviewed restricted-source revision,
required artifact, decision scope, and acceptance criteria. Until that
determination exists, G00 is `BLOCKED`; only governance, quarantine, provenance
recording, and clean-room planning may proceed. User approval of this product
specification does not close the third-party legal check.
