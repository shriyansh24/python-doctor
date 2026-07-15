# Python Doctor Phase 1 Governance Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan task-by-task.
> Every task receives independent specification and code-quality review.

**Goal:** Establish the version-controlled governance, provenance, originality,
release-scope, compatibility, skill, evidence, and executable-gate foundation
required before production implementation.

**Architecture:** Typed TOML manifests under `governance/` define requirements,
gates, sources, authorized destinations, compatibility, and skill delivery. A
standard-library Python runner under `scripts/gates/` validates references,
executes argv-only checks, aggregates fail-closed states, sanitizes evidence,
and binds results to immutable inputs. This phase does not change scanner
behavior or migrate packages.

**Tech Stack:** CPython 3.9–3.14, standard library, `tomli` below Python 3.11,
`unittest`, TOML manifests, JSON schemas/results, Git, pinned Bubblewrap on
Linux, and pinned OpenSSL with Ed25519 verification support.

### Post-publication Task -1 control amendment: Task 0 oracle portability

This section is a post-publication Task -1 control amendment governing Task 0.
It must be committed as a plan-only descendant of the previously published
Task -1 anchor, independently reviewed, published, captured as a new anchor
generation, and accepted as the live `PublishedAnchorCheckpoint` before Task 0
is dispatched. The five-field
`docs/evidence/contracts/phase-01-governance.toml` bootstrap contract and its
historical blob remain byte-identical. Task 0 never edits this plan or that
contract; either edit is a task-separation failure, not a digest update.

Checkpoint generations are append-only. Before amendment authoring begins, the
orchestrator clears the old in-memory checkpoint and prohibits Task 0 dispatch.
The old sealed external-evidence generation remains immutable and is neither
renamed, overwritten, nor deleted. The replacement projection, author
inventory, and review transcript are written and reviewed in a new sibling
generation directory. A generation contains exactly
`published-anchor-projection.json`, `author-inventory.json`, and
`published-anchor-reviews.json`. Its `generation_id` is the lowercase SHA-256
of the ASCII encoding of the three lowercase file SHA-256 values in that order,
each followed by LF; its directory name is `generation-<generation_id>`.

After a generation is sealed, the generations' parent contains the only
mutable durable object, `live-generation.json`. It is a closed canonical JSON
object using the same RFC 8785-plus-one-LF encoding, with exactly
`schema_version`, `run_id`, `generation_id`, `relative_directory`, `anchor_sha`,
`anchor_tree`, `evidence_parent_identity`, `projection_sha256`,
`author_inventory_sha256`, and `reviews_sha256`. `schema_version` is
`published-anchor-live-pointer/v1`; `relative_directory` is exactly
`generation-<generation_id>` with no path separator. Only after both independent
reviews pass does the orchestrator atomically replace this pointer. The
`evidence_parent_identity` is the lowercase SHA-256 of the UTF-8 encoding of the
canonical resolved, native-case-normalized evidence-parent path plus LF. The
orchestrator resolves `PHASE_01_EXTERNAL_EVIDENCE_ROOT` to that sibling,
verifies the parent identity and all three hashes, and creates the new in-memory
checkpoint bound to that identity. Moving or copying the evidence tree changes
the resolved identity and is `FAIL`. The previous generation stays sealed but
is superseded and inadmissible for a new Task 0 dispatch.

The orchestration-owned `PHASE_01_TASK_DISPATCH_ROOT` is a separate canonical
directory, neither equal to nor an ancestor or descendant of the evidence
parent or any Git worktree. The dispatch record is written there as
`task-00-dispatch-<generation_id>.json`, never inside a sealed generation. It
binds the new generation ID, evidence-parent identity, live-pointer digest,
three sealed-file digests, anchor commit/tree, exact Task 0 author path, and UTC
dispatch time. Its own captured-byte SHA-256 is supplied as
`PUBLISHED_TASK_00_DISPATCH_SHA256` and becomes an immutable Task 0 audit and
acceptance-evidence input.

Task 0 oracle validation and later schema/manifest tooling must remain
functional on Linux, macOS, and Windows across the supported CPython matrix.
Where the host exposes descriptor-relative open, directory-only open, and
no-follow flags, the oracle reader uses handle-bound component traversal and
binds every opened directory identity before reading the final file.

Where those primitives are unavailable, portable snapshot mode must reject
components that are symlinks, observed Windows reparse points, or non-regular
inputs at inspection time; require resolved-root containment; bind the opened
file's identity and metadata to that inspection; cap the read; and repeat path
and descriptor checks afterward. This mode detects persistent path substitution
and file mutation. It does not provide atomic component containment and cannot
exclude transient namespace or component substitution by a concurrent
malicious mutator, including substitutions fully restored between checks. It
is limited to fixed governance inputs in an orchestration-owned clean checkout
with no untrusted concurrent mutator.

Portable snapshot evidence is inadmissible for `G13-HOSTILE-REPOSITORY` and
cannot make that check pass. Because the missing secure backend is
project-owned and `G13-HOSTILE-REPOSITORY` is not externally blockable,
`G13-HOSTILE-REPOSITORY` must `FAIL` until secure traversal or a reviewed native
reader is available. A strong Windows claim requires a separately reviewed
native handle-relative no-reparse reader and green pinned Windows CI across
CPython 3.9–3.14; portable snapshot mode permits ordinary cross-platform oracle,
schema, and manifest validation but cannot supply that hostile-repository
claim.

Every Task 0 local and CI unittest run captures the pre-run suite count and must
satisfy `result.wasSuccessful()`, `result.testsRun == expected_count`, and empty
`skipped`, `expectedFailures`, and `unexpectedSuccesses`. A platform-
inapplicable native test is conditionally defined and registered only on its
target platform; it must not be registered as a skipped test. Task 0 removes
every `skipTest`, `skipIf`, `skipUnless`, skip decorator, and
`expectedFailure` reference from
`tests/test_governance_oracles.py`. A required host fixture that cannot be
provisioned is a test failure. A capability-independent behavior uses a
deterministic simulated regression; a platform-native behavior is registered
only on that platform and is mandatory in the corresponding pinned CI job.
Windows coverage is mandatory on
`windows-2022` for the exact Windows x64 patch selectors 3.9.13, 3.10.11,
3.11.9, 3.12.10, 3.13.14, and 3.14.6. Every cell must directly execute the
fully qualified native test
`tests.test_governance_oracles.GovernanceOracleTests.test_windows_junction_component_is_rejected_without_skip`
and the simulated reparse test
`tests.test_governance_oracles.GovernanceOracleTests.test_observed_windows_reparse_points_are_rejected_at_every_level`,
then execute the full oracle module. Missing test registration, a skip, junction
fixture provisioning failure, or any failed cell is `FAIL`; no
`continue-on-error`, silent skip, or provisional Windows support claim is
allowed.

The Windows workflow has no `paths` or `paths-ignore` event filter. It runs for
every pull request and for every push to `agent/phase-01-governance`, so a
change anywhere in the current or future Python startup/import trusted
computing base cannot bypass the matrix merely because its pathname was not
anticipated when Task 0 was written. The push event retains that exact branch
restriction; `workflow_dispatch` remains available for an explicit rerun.

Within this new Task 0 Windows workflow, neither its steps nor the Task 0 oracle
code it invokes contain analytics, telemetry, crash reporting, update checks,
report or source uploads, artifact publication, coverage service, SARIF
publication, dependency cache, persisted Git credentials, or package-manager
installation. Checkout explicitly sets `persist-credentials: false`;
setup-python selects the matrix interpreter, and no `pip`, `uv`, `poetry`, or
other package-install command runs. This scoped claim does not describe or
authorize unrelated pre-existing workflows. GitHub-hosted CI necessarily sends
job logs, check statuses, and operational metadata to GitHub as part of
executing the requested workflow. That infrastructure operation is not a
Python Doctor telemetry feature, and the project does not claim absolute
metadata silence for cloud CI.

## Global constraints

- Do not read, copy, translate, paraphrase, compare against, or structurally
  mirror restricted React Doctor material.
- Implement from the approved Python requirements, public standards, and
  `docs/design/proof-carrying-python-architecture.md` only.
- No telemetry, analytics, crash reporting, update checks, remote prompts/
  rules/configuration, report uploads, or runtime networking.
- The Phase 1 runner and child checks initiate no network access. The isolated
  containment test harness may open loopback-only canary sockets; it sends no
  external traffic and records no repository data.
- Raw legal messages, logs, paths, environment values, and source-sensitive
  evidence stay under gitignored `.evidence/`.
- Gate states are exactly `PASS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`.
- Gate-runner exits are exactly `0`, `1`, `2`, and `3`.
- Future work is `PLANNED`, never `NOT_APPLICABLE`.
- G00 remains `BLOCKED` until the actual permission/legal artifact and an
  authorized human/legal disposition are recorded.
- No production package migration or scanner behavior begins in Phase 1.
- Production implementers start in context-free agents/worktrees, receive only
  approved control documents and public standards, and sign the LEG-06 exposure
  pre-task declaration before code tasks; a post-task trusted receipt later
  binds it to the final subject. Agents inheriting restricted-reference
  discussion may plan/review governance but may not implement production code.
- Intentional edits use `apply_patch`; no destructive Git operation is allowed.

## File map

Planning prerequisites committed with this plan (reviewed inputs, not Phase 1
implementation outputs):

```text
docs/design/proof-carrying-python-architecture.md
docs/governance/requirements-traceability.md
```

Create:

```text
governance/
├── authorized-destinations.toml
├── clause-registry.toml
├── compatibility.toml
├── gates.toml
├── provenance.toml
├── requirements.toml
├── skills-release.toml
├── toolchain.lock.toml
└── validation-inputs.toml
scripts/
├── __init__.py
├── gates/
│   ├── __init__.py
│   ├── __main__.py
│   ├── attestation.py
│   ├── identity.py
│   ├── loader.py
│   ├── models.py
│   ├── child_protocol.py
│   ├── redaction.py
│   ├── runner.py
│   ├── containment.py
│   └── validation.py
└── governance/
    ├── __init__.py
    ├── validate.py
    └── validate_oracles.py
tests/
├── governance_helpers.py
├── test_governance_schemas.py
├── test_governance_oracles.py
├── test_authorized_destinations_manifest.py
├── test_compatibility_manifest.py
├── test_evidence_attestation.py
├── test_gate_identity.py
├── test_gate_manifest.py
├── test_gate_redaction.py
├── test_gate_runner.py
├── test_legal_disposition.py
├── test_network_containment.py
├── test_provenance_manifest.py
├── test_requirements_manifest.py
├── test_repository_instructions.py
└── test_skills_release_manifest.py
tests/fixtures/governance/
├── expected-gate-checks.toml
├── expected-gate-clauses.toml
├── expected-profile-domain-ids.txt
├── expected-provenance-sources.toml
├── expected-requirement-ids.txt
└── expected-skill-ids.txt
schemas/governance/
├── child-result-v1.schema.json
├── check-result-v1.schema.json
├── clean-implementer-certification-v1.schema.json
├── evidence-index-v1.schema.json
├── gate-result-v1.schema.json
├── legal-review-v1.schema.json
├── trust-anchor-receipt-v1.schema.json
└── review-findings-v1.schema.json
docs/
├── evidence/contracts/phase-01-governance.toml
├── legal/restricted-source-review-process.md
└── research/
    ├── provenance-sources.md
    ├── query-rounds.md
    └── saturation-review.md
```

Modify:

```text
.gitignore
AGENTS.md
docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md
```

Pre-base trust input, independently reviewed on protected `main` and never
created or modified by Phase 1 tasks:

```text
governance/trust/legal-release-authority-v1.pem
```

`governance/` is normative. `AGENTS.md` prohibits unreviewed weakening of gates,
applicability, requirements, compatibility, privacy, or publication scope.

## Stable interfaces

```python
class GateState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DeliveryState(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED_UNVERIFIED = "implemented_unverified"
    VERIFIED = "verified"
    BLOCKED = "blocked"


class ChildOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    ASSERTION_FAILURE = "ASSERTION_FAILURE"
    EXTERNAL_BLOCKER = "EXTERNAL_BLOCKER"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ValidationMode(str, Enum):
    BOOTSTRAP = "bootstrap"
    FINAL = "final"


class BootstrapCheckpoint(str, Enum):
    TASK_01 = "task-01"
    TASK_02 = "task-02"
    TASK_03 = "task-03"
    TASK_04 = "task-04"
    TASK_05 = "task-05"
    TASK_06 = "task-06"
    TASK_07 = "task-07"
    TASK_08 = "task-08"
    TASK_09 = "task-09"
    TASK_10 = "task-10"


class IdentityKind(str, Enum):
    BOOTSTRAP = "bootstrap"
    FINAL = "final"


@dataclass(frozen=True)
class RequirementSpec:
    requirement_id: str
    statement: str
    owner: str
    source_clauses: tuple[str, ...]
    introduced_phase: int
    required_by_phase: int
    verification_phases: tuple[int, ...]
    implementation_artifacts: tuple[str, ...]
    behavioral_evidence: tuple[str, ...]
    gate_check_ids: tuple[str, ...]
    dependency_ids: tuple[str, ...]
    completion_condition: str  # human explanation only
    completion_predicates: tuple[str, ...]
    review_required: bool
    origin: str


@dataclass(frozen=True)
class ToolRequirement:
    executable: str
    owner: str  # project or external
    version: str
    expected_sha256: str
    trust_source: str


@dataclass(frozen=True)
class ApplicabilityPredicate:
    kind: str
    arguments: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class GateCheckSpec:
    check_id: str
    gate_id: str
    requirement_ids: tuple[str, ...]
    source_clauses: tuple[str, ...]
    scheduled_phase: int
    required: bool
    schedule_state: DeliveryState
    applicability_predicate: ApplicabilityPredicate
    external_prerequisite: bool
    command: tuple[str, ...]
    working_directory: str
    timeout_seconds: int
    required_tools: tuple[ToolRequirement, ...]
    expected_artifacts: tuple[str, ...]
    pass_criteria: tuple[str, ...]
    warning_policy: str
    skip_policy: str
    invalidation_inputs: tuple[str, ...]


@dataclass(frozen=True)
class ProvenanceSpec:
    source_id: str
    kind: str
    url: str
    immutable_revision: str
    license_id: str
    license_path: str
    license_sha256: str
    license_status: str
    inspected_paths: tuple[str, ...]
    concepts: tuple[str, ...]
    disposition: str
    attribution: str
    artifact_sha256: str
    distribution: str


@dataclass(frozen=True)
class RestrictedSourceSpec:
    source_id: str
    exposure_status: str
    inspected_paths: tuple[str, ...]
    taint_determination: str
    raw_artifact_path: str
    raw_artifact_sha256: str
    review_owner: str
    status: str


@dataclass(frozen=True)
class LegalDispositionSpec:
    restricted_source_id: str
    review_attestation_sha256: str
    signature_sha256: str
    trust_root_fingerprint: str
    authority_evidence_sha256: str
    grant_scope_digest: str
    reviewer_disposition: str


@dataclass(frozen=True)
class CleanImplementerPreTaskDeclarationSpec:
    declaration_id: str
    person_or_agent_identity: str
    role: str
    exposure_status: str
    approved_input_bundle_sha256: str
    base_commit: str
    base_tree: str
    task_ids: tuple[str, ...]
    declaration_date: str
    payload_sha256: str
    implementer_signature_sha256: str


@dataclass(frozen=True)
class CleanImplementerCompletionSpec:
    completion_id: str
    declaration_sha256: str
    subject_commit: str
    subject_tree: str
    completed_task_ids: tuple[str, ...]
    completion_date: str
    completion_payload_sha256: str
    implementer_signature_sha256: str
    reviewer_attestation_sha256: str
    reviewer_signature_sha256: str
    reviewer_trust_root_fingerprint: str
    verification_receipt_sha256: str


@dataclass(frozen=True)
class DestinationSpec:
    destination_id: str
    kind: str
    repository: str
    ref_pattern: str
    state: str


@dataclass(frozen=True)
class CompatibilitySpec:
    component: str
    host_python: str
    target_grammar: str
    operating_system: str
    support_tier: str
    claim_status: str


@dataclass(frozen=True)
class SkillReleaseSpec:
    skill_id: str
    kind: str
    owner_router: str
    required: bool
    triggers: tuple[str, ...]
    exclusions: tuple[str, ...]
    prerequisites: tuple[str, ...]
    conflicts: tuple[str, ...]
    precedence: int
    support_contracts: tuple[str, ...]
    lifecycle: str
    context_cost: int
    required_topics: tuple[str, ...]
    planned_capabilities: tuple[str, ...]
    delivered_capabilities: tuple[str, ...]
    planned_evaluation_ids: tuple[str, ...]
    evidence_policy: str
    false_positive_policy: str
    fix_policy: str
    mutation_authority: str
    rollback_contract: str
    agent_skills_schema_revision: str
    reference_depth: int
    canonical_source: str


@dataclass(frozen=True)
class ProvenanceManifest:
    sources: tuple[ProvenanceSpec, ...]
    restricted_sources: tuple[RestrictedSourceSpec, ...]
    legal_dispositions: tuple[LegalDispositionSpec, ...]
    legal_review_policy: str


@dataclass(frozen=True)
class AuthorizedDestinationsManifest:
    destinations: tuple[DestinationSpec, ...]
    unknown_destination_policy: str
    development_branch_pattern: str
    candidate_branch_pattern: str


@dataclass(frozen=True)
class CompatibilityManifest:
    rows: tuple[CompatibilitySpec, ...]
    essential_components: tuple[str, ...]
    python_versions: tuple[str, ...]
    target_grammars: tuple[str, ...]
    operating_systems: tuple[str, ...]


@dataclass(frozen=True)
class SkillReleaseManifest:
    skills: tuple[SkillReleaseSpec, ...]
    default_router_budget: int
    default_leaf_budget: int


@dataclass(frozen=True)
class ClauseRegistry:
    clauses: tuple[tuple[str, str, str, str], ...]  # id, path, section, digest

    def resolves(self, clause_id: str) -> bool:
        return any(item[0] == clause_id for item in self.clauses)


@dataclass(frozen=True)
class ToolchainLock:
    tools: tuple[ToolRequirement, ...]
    platform_claim: str


@dataclass(frozen=True)
class ValidationInputsManifest:
    paths: tuple[str, ...]
    schema_version: int


@dataclass(frozen=True)
class ReviewEvidence:
    review_id: str
    role: str
    candidate_commit: str
    candidate_tree: str
    disposition: str
    evidence_sha256: str


@dataclass(frozen=True)
class PublishedAnchorBinding:
    commit: str
    tree: str
    projection_sha256: str
    reviews_sha256: str


@dataclass(frozen=True)
class PhaseContract:
    schema_version: str
    governance_base_commit: str
    governance_base_tree: str
    source_branch: str
    phase_branch: str
    published_anchor: PublishedAnchorBinding | None


@dataclass(frozen=True)
class GovernanceBundle:
    requirements: tuple[RequirementSpec, ...]
    checks: tuple[GateCheckSpec, ...]
    provenance: ProvenanceManifest
    destinations: AuthorizedDestinationsManifest
    compatibility: CompatibilityManifest
    skills: SkillReleaseManifest
    clauses: ClauseRegistry
    toolchain: ToolchainLock
    validation_inputs: ValidationInputsManifest
    phase_contract: PhaseContract
    manifest_digests: tuple[tuple[str, str], ...]
    validation_mode: ValidationMode


@dataclass(frozen=True)
class SubjectIdentity:
    commit: str
    tree: str
    dirty: bool
    dependency_lock_digest: str
    fixture_eval_digest: str
    validation_inputs_digest: str
    normative_documents_digest: str
    runner_source_digest: str
    runner_version: str
    published_anchor_commit: str
    published_anchor_tree: str
    published_anchor_projection_sha256: str
    published_anchor_reviews_sha256: str
    dirty_state_digest: str
    identity_kind: IdentityKind


@dataclass(frozen=True)
class ExecutionEnvironmentIdentity:
    platform: str
    python_version: str
    python_executable_sha256: str
    tool_versions: tuple[tuple[str, str], ...]
    tool_sha256: tuple[tuple[str, str], ...]
    containment_backend: str
    containment_backend_sha256: str


@dataclass(frozen=True)
class ExecutionRecord:
    redacted_argv: tuple[str, ...]
    working_directory_token: str
    environment: ExecutionEnvironmentIdentity
    started_at: str
    finished_at: str
    exit_code: int
    warning_count: int
    skip_count: int
    deselection_count: int
    xfail_count: int
    xpass_count: int
    retry_count: int
    collection_error_count: int
    stdout_sha256: str
    stderr_sha256: str
    stdout_truncated: bool
    stderr_truncated: bool


@dataclass(frozen=True)
class ChildResult:
    schema_version: int
    check_id: str
    outcome: ChildOutcome
    warning_count: int
    skip_count: int
    deselection_count: int
    xfail_count: int
    xpass_count: int
    retry_count: int
    collection_error_count: int
    produced_artifacts: tuple[str, ...]
    reason_codes: tuple[str, ...]
    applicability_evidence: tuple[str, ...]
    external_prerequisite_evidence: tuple[str, ...]
    blocker_owner: str
    alternatives_attempted: tuple[str, ...]
    retry_evidence: tuple[str, ...]
    unblock_condition: str
    applicability_inputs: tuple[tuple[str, str], ...]
    applicability_result: Optional[bool]
    applicability_review_evidence_id: str
    failure_classification: str


@dataclass(frozen=True)
class CheckResult:
    schema_version: int
    subject: SubjectIdentity
    check_id: str
    gate_id: str
    state: GateState
    execution: ExecutionRecord
    artifact_hashes: tuple[tuple[str, str], ...]
    redaction_version: str
    reason_codes: tuple[str, ...]
    applicability_evidence: tuple[str, ...]
    external_prerequisite_evidence: tuple[str, ...]
    external_input_hashes: tuple[tuple[str, str], ...]
    trust_root_fingerprint: str
    child_result_sha256: str
    summary: str


@dataclass(frozen=True)
class GateRunResult:
    schema_version: int
    gate_id: str
    subject: SubjectIdentity
    state: GateState
    checks: tuple[CheckResult, ...]


@dataclass(frozen=True)
class RequirementResult:
    requirement_id: str
    subject: SubjectIdentity
    state: DeliveryState
    satisfied_check_ids: tuple[str, ...]
    dependency_results: tuple[str, ...]
    review_evidence_ids: tuple[str, ...]
    predicate_results: tuple[tuple[str, bool], ...]
    remaining_verification_phases: tuple[int, ...]
```

Public functions have the exact signatures `load_governance(root: Path, mode:
ValidationMode = ValidationMode.FINAL, checkpoint: Optional[BootstrapCheckpoint]
= None) ->
GovernanceBundle`, `validate_governance(bundle: GovernanceBundle, active_phase:
int) -> tuple[Violation, ...]`, `identify_subject(root: Path) ->
SubjectIdentity`, `derive_requirement_result(requirement: RequirementSpec,
bundle: GovernanceBundle, gate_results: Sequence[GateRunResult], subject:
SubjectIdentity, review_evidence: Sequence[ReviewEvidence], active_phase: int)
-> RequirementResult`, `redact_text(value: str, secrets:
Sequence[str] = ()) -> str`, `run_gate(root: Path, gate_id: str, evidence_dir:
Path) -> GateRunResult`, and `main(argv: Sequence[str] | None = None) -> int`.
Runner helpers have the exact signatures `aggregate(states:
Sequence[GateState]) -> GateState`, `exit_code(state: GateState) -> int`, and
`run_check(root: Path, check: GateCheckSpec, subject: SubjectIdentity,
evidence_dir: Path) -> CheckResult`.
`run_gate()`, real `run_check()`, and `write_attestation_ref()` require
`subject.identity_kind is IdentityKind.FINAL`; bootstrap subjects are rejected before
child execution or evidence creation.
Invalid configuration is a runner error returning exit 3 before a `GateState`
is constructed; it is never a fifth gate state.

Bootstrap mode requires a checkpoint and permits only that enum member's frozen
missing-path allowlist, marks the bundle non-evidentiary, and is accepted only by
manifest/unit tests. The CLI, `run_gate`, requirement closure, and attestation
always use `FINAL` and reject any missing validation input.

The canonical aggregate precedence is `FAIL > BLOCKED > PASS`; a gate is
`NOT_APPLICABLE` only when every mandatory child is independently and validly
not applicable. A mix of `PASS` and `NOT_APPLICABLE` aggregates to `PASS`.
Every N/A result names a schema-valid candidate-bound independent review
evidence ID whose reviewed predicate inputs match the child result.

Every child command writes exactly one `child-result-v1` JSON document to a
runner-allocated root-contained path. The runner validates it against the
frozen schema and correlates `check_id`; stdout/stderr are never scraped to
infer warnings, skips, deselections, xfails, xpasses, retries, collection
errors, or artifacts. Missing, malformed, duplicate, or mismatched child
results fail.

The runner derives state from a frozen truth table over process exit, validated
child outcome, counts, expected artifacts, tool ownership, applicability, and
external evidence. A child can report facts but cannot select `GateState`.
Project-owned missing tools/controls and failed containment probes are `FAIL`;
only externally disabled OS facilities after recorded alternatives are
`BLOCKED`.

`BLOCKED` requires at least one closed external-prerequisite reason code and a
redacted evidence reference. `NOT_APPLICABLE` requires a registered predicate,
typed repository/platform facts, and independently reviewable applicability
evidence. Neither state can be emitted from prose or an empty evidence list.

Manifest commands are arrays. Shell strings, substitutions, redirections,
remote URLs, arbitrary expressions, and parent-traversal paths are invalid.
Canonical outputs sort requirement IDs, check IDs, clause IDs, tool identities,
artifact paths/hashes, violations, manifest digests, evidence references, and
review findings by UTF-8 byte order of their stable IDs; arrays whose order is
semantically meaningful declare that explicitly.

The closed completion-predicate registry is
`all_required_checks_pass`, `dependencies_closed`,
`behavioral_evidence_valid`, `artifacts_present_and_hashed`,
`required_review_bound`, and `final_verification_phase_complete`. Unknown
predicates are invalid; every predicate emits a candidate-bound boolean in
`RequirementResult`.

---

### Task -1: Anchor planning and execution to remote `main`

**Classification:** `verification_content`

**Requirements:** `QA-02`, `PUB-01`, `PUB-02`, `REL-03`

**Required sub-skill:** `superpowers:using-git-worktrees`

**Files:**

- Create: `docs/evidence/contracts/phase-01-governance.toml` with only the
  immutable execution-base binding; Task 2 later extends this same record.
- Modify: this plan to record the reviewed sequencing and external-anchor
  acceptance corrections discovered before Task 0.

- [ ] **Step 1: Verify the planning publication base**

Fetch without force or history rewrite. Confirm the connected GitHub app and
local remote both resolve `refs/heads/main` to
`e3049ee12771c1055bde2392adeba2de33324602`. If it moved, stop, inspect the new
tree, update the orientation evidence in a separately reviewed planning commit,
and rerun adversarial review.

- [ ] **Step 2: Publish the approved control-document tree from remote history**

Create `agent/original-python-doctor-plan` and its isolated worktree directly
from the verified remote commit. Apply the exact reviewed tree delta from this
planning workspace, verify the staged scope, commit once, and open a draft PR to
`main`. The local unrelated `master` branch is never pushed or merged. Verify:

```bash
test "$(git merge-base origin/main HEAD)" = "e3049ee12771c1055bde2392adeba2de33324602"
git diff --check origin/main...HEAD
```

- [ ] **Step 3: Freeze the Phase 1 execution base after merge**

After the control-document PR is merged, fetch `origin/main`, record that exact
merge/fast-forward SHA as `GOVERNANCE_BASE_SHA` in the Phase 1 evidence contract,
and create `agent/phase-01-governance` plus its worktree from that SHA. Before
the first Phase 1 commit, prove `HEAD`, `HEAD^{tree}`, and merge-base match the
approved remote state. After the contract commit, `HEAD^{tree}` is expected to
differ because the contract is now part of the subject; prove instead that the
recorded base is the exact parent and ancestor of `HEAD` and that the recorded
base tree equals `<base-commit>^{tree}`. All Task 0–10 review/evidence binds
commits in this ancestry. Rebase, cherry-pick, replay, or force-push after review
invalidates the candidate and requires fresh execution/review rather than SHA
substitution.

The Task -1 contract is intentionally minimal and records exactly
`schema_version`, `governance_base_commit`, `governance_base_tree`,
`source_branch`, and `phase_branch`. Commit it before Task 0. Task 2 modifies
this existing record to add the complete evidence contract; it never replaces
or weakens the frozen base commit/tree.

Immediately after creating the isolated worktree, before creating or editing
any Phase 1 file, run this pre-edit acceptance block:

```bash
set -eu
GOVERNANCE_BASE_SHA=$(git rev-parse origin/main)
GOVERNANCE_BASE_TREE=$(git rev-parse "$GOVERNANCE_BASE_SHA^{tree}")
test "$(git rev-parse HEAD)" = "$GOVERNANCE_BASE_SHA"
test "$(git merge-base origin/main HEAD)" = "$GOVERNANCE_BASE_SHA"
test "$(git rev-parse 'HEAD^{tree}')" = "$GOVERNANCE_BASE_TREE"
test -z "$(git status --porcelain=v1)"
```

Immediately after the contract-introduction commit, and only while that commit
is `HEAD`, post-commit acceptance parses the TOML with exactly the five declared keys,
checks `HEAD^ == governance_base_commit`, checks
`governance_base_commit^{tree} == governance_base_tree`, and requires
`git merge-base --is-ancestor governance_base_commit HEAD`. It also verifies
that the contract-addition commit is unique and that its changed-file set is
limited to the contract plus this separately reviewed sequencing correction.

```bash
set -eu
python -c 'import importlib.util,pathlib,subprocess; tomllib=__import__("tomllib" if importlib.util.find_spec("tomllib") else "tomli"); p="docs/evidence/contracts/phase-01-governance.toml"; plan="docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md"; d=tomllib.loads(pathlib.Path(p).read_text("utf-8")); run=lambda *a: subprocess.check_output(["git",*a],text=True).strip(); require=lambda c,m: c or (_ for _ in ()).throw(SystemExit(m)); keys={"schema_version","governance_base_commit","governance_base_tree","source_branch","phase_branch"}; require(set(d)==keys and all(isinstance(d[k],str) for k in keys),"invalid contract shape"); require(d["schema_version"]=="phase-01-governance-contract/v1" and d["source_branch"]=="main" and d["phase_branch"]==run("branch","--show-current"),"invalid contract identity"); require(run("rev-parse","HEAD^")==d["governance_base_commit"],"wrong base parent"); require(run("rev-parse",d["governance_base_commit"]+"^{tree}")==d["governance_base_tree"],"wrong base tree"); subprocess.run(["git","merge-base","--is-ancestor",d["governance_base_commit"],"HEAD"],check=True); require(run("log","--diff-filter=A","--format=%H","--",p).splitlines()==[run("rev-parse","HEAD")],"non-unique contract introduction"); require(set(run("diff-tree","--no-commit-id","--name-only","-r","HEAD").splitlines())=={p,plan},"invalid Task -1 commit scope")'
git diff --check HEAD^
test -z "$(git status --porcelain=v1)"
```

- [ ] **Step 4: Freeze the published content-addressed execution anchor**

Publish all Task -1 changes to PR `shriyansh24/python-doctor#2`. After the final
Task -1 commit is remotely created, stop editing and fetch its immutable
projection through the connected GitHub app. The orchestration-owned canonical
`published-anchor-projection/v1` is a closed JSON object with exactly these
keys: `schema_version`, `purpose`, `run_id`, `repository_id`, `repository`,
`pull_request_number`, `base_ref`, `base_sha`, `head_ref`, `head_sha`,
`head_parent_sha`, `head_tree_sha`, `commit_url`,
`contract_introduction_sha`, `contract_introduction_tree_sha`,
`contract_introduction_blob_sha`, `captured_at`,
`changed_file_count`, `task_minus_one_commit_chain`, `head_commit_object_sha256`,
`head_tree_object_sha256`, `contract_introduction_commit_object_sha256`,
`contract_introduction_tree_object_sha256`,
`governance_base_commit_object_sha256`,
`governance_base_tree_object_sha256`, and `files`. The fixed non-derived values
are `schema_version = "published-anchor-projection/v1"`,
`purpose = "phase-01-governance-input"`,
`run_id = "phase-01-governance-2026-07-14"`, `repository_id = 1300970386`,
`repository = "shriyansh24/python-doctor"`, `pull_request_number = 2`,
`base_ref = "main"`, and `head_ref = "agent/phase-01-governance"`;
SHA/tree values are lowercase 40-hex Git object
IDs, `commit_url` is the connector-returned canonical HTTPS URL, and
`captured_at` is UTC RFC 3339 with `Z` and whole seconds.

`files` is an array of closed objects with exactly `status`, `old_path`,
`new_path`, `mode`, `blob_sha`, `raw_sha256`, and `byte_size`. `status` is one
of `added`, `modified`, or `removed`; rename detection is disabled and a rename
is represented as one removed plus one added entry. `old_path` is the base path
only when removed and otherwise JSON `null`; `new_path` is the head path for
added/modified and JSON `null` when removed. `mode` is the six-digit head Git
mode, or the base-tree mode when removed. `blob_sha` is the lowercase 40-hex Git object ID at
the head (JSON `null` when removed), `raw_sha256` is the lowercase 64-hex digest
of head bytes (JSON `null` when removed), and `byte_size` is a non-negative
integer (JSON `null` when removed). Phase 1 Task -1 accepts only regular-file
mode `100644`; a symlink, executable, submodule/gitlink, directory entry,
non-blob entry, or non-UTF-8 path is `FAIL`. Paths must already be Unicode NFC,
contain neither NUL nor `..` components, and are sorted by their UTF-8 byte
sequence on `(new_path or "", old_path or "")`. The complete file set must
equal both the connector's fully paginated `list_pr_changed_filenames` result
and `git diff --name-status -z --no-renames <base>..<head>` after comparing the
union of non-null old/new paths. The connector wrapper
guarantees complete pagination; an error, truncation indication, duplicate
path, or count mismatch is `BLOCKED` before capture and `FAIL` after capture.

The head commit must have exactly one parent. `contract_introduction_blob_sha`
is the Git blob ID at the exact contract path and must equal the final head's
blob at that path; the contract file entry is `added`, mode `100644`, and
byte-identical from introduction through anchor. The projection additionally has
six lowercase 64-hex fields: `head_commit_object_sha256`,
`head_tree_object_sha256`, `contract_introduction_commit_object_sha256`,
`contract_introduction_tree_object_sha256`, `governance_base_commit_object_sha256`,
and `governance_base_tree_object_sha256`. Each is SHA-256 of the canonical Git
object bytes `type + SP + decimal-size + NUL + payload`, independently rebuilt
with `git cat-file --batch`. These fields are part of the closed top-level key
set above. `repository_id` and repository/ref strings must exactly match the
fixed values; refs contain only the stated ASCII strings. Capture time comes
from the orchestration host UTC clock and is informational, not an authority or
freshness proof.

`task_minus_one_commit_chain` is an ordered array of lowercase 40-hex commit
IDs from `contract_introduction_sha` through `head_sha`, inclusive. It contains
at least two unique entries, its first/last entries equal those projected SHAs,
and every entry's sole parent is the preceding entry (the introduction parent
is `base_sha`). Every post-introduction commit changes only this plan and leaves
the projected contract blob unchanged.

Projection validation additionally requires `base_sha` to equal the contract's
`governance_base_commit`, that commit's tree to equal
`governance_base_tree`, and `head_sha` to equal both the connector PR head and
the connector-fetched commit. `head_parent_sha` is its sole parent and equals
the penultimate commit-chain entry; the introduction SHA is the unique contract-path
addition commit, its parent is `base_sha`, its tree is the projected
introduction tree, and its contract blob parses to exactly the historical
five-key bootstrap contract. The final head contains that same contract blob.
Any inequality is `FAIL`.

Canonical JSON follows RFC 8785 JSON Canonicalization Scheme for the closed
object, with the additional invariant that the serialized UTF-8 bytes end in
exactly one LF; no BOM is permitted. Integers stay in the I-JSON safe range and
duplicate keys, floats, surrogate code points, and Unicode normalization by the
serializer are forbidden. `projection_sha256` is the SHA-256 of those canonical
bytes and is stored outside the subject commit. The remote head commit, not the
movable branch name or mutable PR prose, is `PHASE_01_PUBLISHED_ANCHOR_SHA`.

The reviewed amendments that define and clarify this procedure are ordered
post-introduction Task -1 commits. `CONTRACT_INTRODUCTION_SHA` remains the
unique earlier commit that added the five-field contract and whose parent is
`GOVERNANCE_BASE_SHA`; the final published anchor must descend linearly from it,
every later Task -1 commit may change only this plan, and none may alter the
contract's immutable projection.

After every initial or superseding Task -1 publication, run the following exact
handoff from the repository's main working tree. The caller supplies absolute
`REPOSITORY_ROOT`, current `TASK_MINUS_ONE_AUTHORING_WORKTREE`, desired
`PHASE_01_EXECUTION_WORKTREE`, local `LOCAL_TASK_MINUS_ONE_CANDIDATE_SHA`, and
connector-reported `PHASE_01_PUBLISHED_ANCHOR_SHA`. If an earlier execution
worktree is still registered, `PREVIOUS_EXECUTION_WORKTREE` is its absolute
path; otherwise it is empty. Every supplied worktree must share the repository
common directory, be clean, and have a named branch. The procedure archives
both the local amendment candidate and any prior execution generation before
removing only their clean worktree registrations. It never deletes or rewrites
an archive branch, never force-fetches, and recreates execution only from the
verified connector commit.

```bash
set -eu
: "${REPOSITORY_ROOT:?absolute repository root is required}"
: "${TASK_MINUS_ONE_AUTHORING_WORKTREE:?absolute authoring worktree is required}"
: "${PHASE_01_EXECUTION_WORKTREE:?absolute execution worktree is required}"
: "${LOCAL_TASK_MINUS_ONE_CANDIDATE_SHA:?local candidate SHA is required}"
: "${PHASE_01_PUBLISHED_ANCHOR_SHA:?remote anchor SHA is required}"
: "${PREVIOUS_EXECUTION_WORKTREE:=}"

CANONICAL_BRANCH=agent/phase-01-governance
REMOTE_TRACKING_REF=refs/remotes/origin/agent/phase-01-governance
REPOSITORY_ROOT=$(realpath "$REPOSITORY_ROOT")
AUTHORING_WORKTREE=$(realpath "$TASK_MINUS_ONE_AUTHORING_WORKTREE")
EXECUTION_WORKTREE=$(realpath -m "$PHASE_01_EXECUTION_WORKTREE")
COMMON_DIR=$(git -C "$REPOSITORY_ROOT" rev-parse --path-format=absolute --git-common-dir)
test "$AUTHORING_WORKTREE" != "$REPOSITORY_ROOT"
test "$AUTHORING_WORKTREE" != "$EXECUTION_WORKTREE"
test "$(git -C "$AUTHORING_WORKTREE" rev-parse --path-format=absolute --git-common-dir)" = "$COMMON_DIR"
test "$(git -C "$AUTHORING_WORKTREE" branch --show-current)" = "$CANONICAL_BRANCH"
test "$(git -C "$AUTHORING_WORKTREE" rev-parse HEAD)" = "$LOCAL_TASK_MINUS_ONE_CANDIDATE_SHA"
test -z "$(git -C "$AUTHORING_WORKTREE" status --porcelain=v1)"

if test -n "$PREVIOUS_EXECUTION_WORKTREE"; then
  PREVIOUS_EXECUTION_WORKTREE=$(realpath "$PREVIOUS_EXECUTION_WORKTREE")
  test "$PREVIOUS_EXECUTION_WORKTREE" = "$EXECUTION_WORKTREE"
  test "$PREVIOUS_EXECUTION_WORKTREE" != "$AUTHORING_WORKTREE"
  test "$PREVIOUS_EXECUTION_WORKTREE" != "$REPOSITORY_ROOT"
  test "$(git -C "$PREVIOUS_EXECUTION_WORKTREE" rev-parse --path-format=absolute --git-common-dir)" = "$COMMON_DIR"
  test -n "$(git -C "$PREVIOUS_EXECUTION_WORKTREE" branch --show-current)"
  test -z "$(git -C "$PREVIOUS_EXECUTION_WORKTREE" status --porcelain=v1)"
  PREVIOUS_SHA=$(git -C "$PREVIOUS_EXECUTION_WORKTREE" rev-parse HEAD)
  PREVIOUS_SHORT=$(git -C "$PREVIOUS_EXECUTION_WORKTREE" rev-parse --short=12 HEAD)
  PREVIOUS_ARCHIVE="archive/phase-01-execution-pre-generation-$PREVIOUS_SHORT"
  test -z "$(git -C "$REPOSITORY_ROOT" branch --list "$PREVIOUS_ARCHIVE")"
  git -C "$PREVIOUS_EXECUTION_WORKTREE" branch -m "$PREVIOUS_ARCHIVE"
  git -C "$REPOSITORY_ROOT" worktree remove "$PREVIOUS_EXECUTION_WORKTREE"
  test "$(git -C "$REPOSITORY_ROOT" rev-parse "refs/heads/$PREVIOUS_ARCHIVE")" = "$PREVIOUS_SHA"
fi

LOCAL_SHORT=$(git -C "$AUTHORING_WORKTREE" rev-parse --short=12 HEAD)
LOCAL_ARCHIVE="archive/phase-01-governance-local-$LOCAL_SHORT"
test -z "$(git -C "$REPOSITORY_ROOT" branch --list "$LOCAL_ARCHIVE")"
git -C "$AUTHORING_WORKTREE" branch -m "$LOCAL_ARCHIVE"
git -C "$REPOSITORY_ROOT" worktree remove "$AUTHORING_WORKTREE"
test "$(git -C "$REPOSITORY_ROOT" rev-parse "refs/heads/$LOCAL_ARCHIVE")" = "$LOCAL_TASK_MINUS_ONE_CANDIDATE_SHA"
test ! -e "$EXECUTION_WORKTREE"

git -C "$REPOSITORY_ROOT" fetch origin refs/heads/agent/phase-01-governance:refs/remotes/origin/agent/phase-01-governance
test "$(git -C "$REPOSITORY_ROOT" rev-parse "$REMOTE_TRACKING_REF")" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test -z "$(git -C "$REPOSITORY_ROOT" branch --list "$CANONICAL_BRANCH")"
git -C "$REPOSITORY_ROOT" worktree add -b "$CANONICAL_BRANCH" "$EXECUTION_WORKTREE" "$REMOTE_TRACKING_REF"
git -C "$EXECUTION_WORKTREE" branch --set-upstream-to=origin/agent/phase-01-governance
test "$(git -C "$EXECUTION_WORKTREE" rev-parse HEAD)" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git -C "$EXECUTION_WORKTREE" rev-parse '@{upstream}')" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git -C "$EXECUTION_WORKTREE" branch --show-current)" = "$CANONICAL_BRANCH"
test -z "$(git -C "$EXECUTION_WORKTREE" status --porcelain=v1)"
```

This preserves the five-field contract's branch identity while ensuring
execution starts from GitHub's actual commit rather than a locally predicted
equivalent. In the execution worktree verify:

```bash
set -eu
export GIT_NO_REPLACE_OBJECTS=1
test -z "${GIT_ALTERNATE_OBJECT_DIRECTORIES:-}"
GIT_COMMON_DIR=$(git --no-replace-objects rev-parse --path-format=absolute --git-common-dir)
test -z "$(git --no-replace-objects for-each-ref --format='%(refname)' refs/replace)"
test ! -e "$GIT_COMMON_DIR/info/grafts"
test ! -e "$GIT_COMMON_DIR/objects/info/alternates"
test ! -e "$GIT_COMMON_DIR/shallow"
test "$(git --no-replace-objects rev-parse --is-shallow-repository)" = "false"
test -n "${PHASE_01_PUBLISHED_ANCHOR_SHA:-}"
test -n "${PHASE_01_PUBLISHED_ANCHOR_TREE:-}"
test -n "${PHASE_01_PUBLISHED_ANCHOR_PARENT:-}"
test -n "${PHASE_01_TASK_MINUS_ONE_CHAIN:-}"
test -n "${GOVERNANCE_BASE_SHA:-}"
test -n "${CONTRACT_INTRODUCTION_SHA:-}"
test -n "${CONTRACT_INTRODUCTION_TREE:-}"
test -n "${CONTRACT_INTRODUCTION_BLOB:-}"
test "$(git rev-parse HEAD)" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git branch --show-current)" = "agent/phase-01-governance"
test "$(git rev-parse '@{upstream}')" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git rev-parse refs/remotes/origin/agent/phase-01-governance)" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git rev-parse 'HEAD^{tree}')" = "$PHASE_01_PUBLISHED_ANCHOR_TREE"
test "$(git rev-parse 'HEAD^')" = "$PHASE_01_PUBLISHED_ANCHOR_PARENT"
test "$(git rev-list --parents -n 1 HEAD | wc -w)" -eq 2
test "$(git merge-base "$GOVERNANCE_BASE_SHA" HEAD)" = "$GOVERNANCE_BASE_SHA"
test "$(git rev-parse "$CONTRACT_INTRODUCTION_SHA^")" = "$GOVERNANCE_BASE_SHA"
test "$(git rev-parse "$CONTRACT_INTRODUCTION_SHA^{tree}")" = "$CONTRACT_INTRODUCTION_TREE"
test "$(git rev-parse "$CONTRACT_INTRODUCTION_SHA:docs/evidence/contracts/phase-01-governance.toml")" = "$CONTRACT_INTRODUCTION_BLOB"
test "$(git rev-parse "HEAD:docs/evidence/contracts/phase-01-governance.toml")" = "$CONTRACT_INTRODUCTION_BLOB"
git merge-base --is-ancestor "$CONTRACT_INTRODUCTION_SHA" HEAD
test "$(git rev-list --reverse "$CONTRACT_INTRODUCTION_SHA^..HEAD")" = "$PHASE_01_TASK_MINUS_ONE_CHAIN"
test "$(git diff-tree --no-commit-id --name-only -r "$CONTRACT_INTRODUCTION_SHA" | wc -l)" -eq 2
git diff-tree --no-commit-id --name-only -r "$CONTRACT_INTRODUCTION_SHA" | grep -Fx "docs/evidence/contracts/phase-01-governance.toml"
git diff-tree --no-commit-id --name-only -r "$CONTRACT_INTRODUCTION_SHA" | grep -Fx "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md"
for TASK_MINUS_ONE_COMMIT in $(git rev-list --reverse "$CONTRACT_INTRODUCTION_SHA..HEAD"); do
  test "$(git rev-list --parents -n 1 "$TASK_MINUS_ONE_COMMIT" | wc -w)" -eq 2
  test "$(git diff-tree --no-commit-id --name-only -r "$TASK_MINUS_ONE_COMMIT")" = "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md"
  test "$(git rev-parse "$TASK_MINUS_ONE_COMMIT:docs/evidence/contracts/phase-01-governance.toml")" = "$CONTRACT_INTRODUCTION_BLOB"
done
test -z "$(git submodule status)"
test -z "$(git status --porcelain=v1)"
```

`PHASE_01_TASK_MINUS_ONE_CHAIN` is the projection array joined with LF and no
final LF. Every Git ancestry, parent, tree, diff, blob, and object-hash query in
capture/review runs with replacement objects disabled. A replace ref, graft,
shallow boundary, object alternate, or chain mismatch is `FAIL`; reviewers do
not accept a normal Git query as a substitute for the replacement-disabled
result.

The orchestrator supplies those variables from the canonical projection, not
from repository text. `PHASE_01_EXTERNAL_EVIDENCE_ROOT` is an absolute,
orchestration-owned directory whose resolved path must be outside every Git
worktree. It contains `published-anchor-projection.json`,
`author-inventory.json`, and `published-anchor-reviews.json`; no Task -1
external artifact is written below a repository root. `author-inventory.json`
is closed schema `published-anchor-authors/v1` with exactly `schema_version`,
`run_id`, `author_task_paths`, and `mutation_events`. `author_task_paths` is a
sorted duplicate-free array containing `/root` plus every agent task that
edited Task -1. `mutation_events` is a chronological array of closed objects
with exactly `event_kind`, `actor_id`, `operation`, `input_identity`, and
`result_identity`; all five are strings. `event_kind` is `local` or `github`.
For `local`, `actor_id` is a collaboration task path, `operation` is one of
`apply_patch` or `git_commit`, and input/result identities are one lowercase
SHA-256 file digest or 40-hex Git tree/commit ID per event. For `github`,
`actor_id` is exactly `60398680`, `operation` is one of `create_blob`,
`create_tree`, `create_commit`, or `update_ref`, and input/result identities are
one lowercase Git object/ref-target SHA per event. A local `apply_patch` event
is explicitly a logical authoring batch: it starts at one stable reviewed
file/tree identity and ends at the next stable reviewed file/tree identity.
Intermediate uncommitted edit states are not review subjects, are not assigned
invented identities, and do not become separate events; the batch's sole author
task remains fully disclosed in `author_task_paths`. Multiple stable reviewed
results or multiple GitHub API results require multiple chronological events;
no arrays, nested objects, empty strings, or unlisted values are accepted. It uses the same
canonical bytes and its SHA-256 is bound by the review transcript. Two distinct
review agents independently compare the projection with the fresh local Git
objects, contract, and author inventory.

This is explicitly a session-scoped procedural checkpoint, not a cryptographic
receipt, trusted timestamp, or replay-resistant capability. The available
platform exposes authenticated collaboration task identities and result
messages but no receipt issuer/verifier API. The closed review transcript has
exactly `schema_version`, `run_id`, `projection_sha256`, `anchor_sha`,
`anchor_tree`, `author_inventory_sha256`, and `reviews`; its first two values
are `published-anchor-reviews/v1` and the projection run ID. `reviews` contains
exactly two objects, each with exactly `task_path`, `role`, `verdict`,
`result_text`, and `completed_at`. Roles are exactly one `specification` and one
`adversarial`; verdict is exactly uppercase `PASS`. `result_text` is the exact
Unicode collaboration payload delivered to root, with no newline added,
removed, or normalized.
Timestamps use the same informational UTC grammar and canonical JSON uses the
same RFC 8785-plus-one-LF bytes as the projection. Each entry records the actual
collaboration result rather than rewritten review prose. Review task paths
must be distinct, absent from the author inventory, have made no filesystem or
GitHub mutations, and return `PASS` over the same projection.

Immediately before and after each reviewer runs, root records and compares
subject `HEAD`, tree, branch/upstream SHA, porcelain-v1 status bytes, projection
digest, and author-inventory digest. Any observable mutation is `FAIL`; because
the platform exposes no reviewer tool-call audit API, this procedural check
does not claim detection of a perfectly reverted hidden mutation. The root
orchestrator consumes the actual collaboration results in the current session,
writes the transcript exactly once, recomputes all three external-file digests, and sets
the in-memory `PublishedAnchorCheckpoint` only after all comparisons pass.
There is deliberately no repository constructor or verifier for this
checkpoint. Task 0 may be dispatched only in that same live session and its
separate session dispatch record binds the generation ID, evidence-parent
identity, live-pointer digest, all three external-file SHA-256 values, and its
own captured-byte digest. The content-addressed commit, tree, and files sealed
by one Task -1 generation are never mutated. A later approved
post-publication plan-only amendment creates a new descendant and sibling
generation under this amendment's supersession protocol; it does not rewrite
the prior Git objects or external generation. If the session or any external
file is lost, moved, or changed, rerun both reviews; do not reconstruct approval
from repository strings. A mismatch, missing object, wrong repository/PR,
substituted commit, dirty worktree, incomplete file set, or self-review is
`FAIL`; GitHub/reviewer unavailability is `BLOCKED`.

Branch movement after capture cannot mutate the content-addressed commit/tree.
Every later orchestration identity check binds the checkpoint's projection and
review-transcript digests as immutable execution inputs. Tasks 0–10 necessarily
create new candidate commits; those use the
separate candidate `SubjectIdentity` and do not re-anchor Task -1. A change to
the Task -1 control inputs or their ancestry invalidates the checkpoint and requires
fresh publication/review. Protected refs remain optional release hardening, not
a prerequisite for governance Task 0.

---

### Task 0: Independently freeze normative oracle fixtures

**Classification:** `verification_content`

**Requirements:** `LEG-03`, `QA-01`, `QA-05`, `SKL-03`

**Files:**

- Create: `tests/fixtures/governance/expected-requirement-ids.txt`
- Create: `tests/fixtures/governance/expected-skill-ids.txt`
- Create: `tests/fixtures/governance/expected-profile-domain-ids.txt`
- Create: `tests/fixtures/governance/expected-provenance-sources.toml`
- Create: `tests/fixtures/governance/expected-gate-clauses.toml`
- Create: `tests/fixtures/governance/expected-gate-checks.toml`
- Create: `docs/audits/2026-07-14-governance-oracle-review.md`
- Create: `scripts/__init__.py`
- Create: `scripts/governance/__init__.py`
- Create: `scripts/governance/validate_oracles.py`
- Create: `tests/test_governance_oracles.py`
- Create: `.github/workflows/governance-oracles-windows.yml`

- [ ] **Step 0: Consume the live Task -1 checkpoint**

Before dispatching any Task 0 author, the root orchestrator confirms the
in-memory `PublishedAnchorCheckpoint` still exists, recomputes all three external
file digests, rechecks `HEAD`, tree, upstream, ancestry, and cleanliness, and
writes `task-00-dispatch-<generation_id>.json` under the separate
`PHASE_01_TASK_DISPATCH_ROOT`, never inside the exact three-file sealed
generation or its parent. The dispatch payload has exactly these closed keys:
`schema_version: str`, `task_id: int`, `generation_id: str`,
`evidence_parent_identity: str`, `live_pointer_sha256: str`,
`projection_sha256: str`, `author_inventory_sha256: str`,
`reviews_sha256: str`, `anchor_sha: str`, `anchor_tree: str`,
`author_task_path: str`, and `dispatched_at: str`. Its schema is exactly
`task-dispatch/v1`, task ID is integer `0`, hashes have their exact lowercase
40/64-hex widths, author path equals the dispatched collaboration task, and
time is whole-second UTC RFC 3339 no more than 15 minutes old and not in the
future. Canonical bytes use RFC 8785's applicable closed string/integer subset
plus one LF.

Acceptance rejects a zero-byte dispatch, `dispatch file exceeds 16384 bytes`,
`duplicate dispatch key`, `dispatch is stale`, unrelated field values,
symlinks, observed Windows reparse points, and non-regular inputs. Pointer,
three sealed files, and dispatch are each captured once through a bounded
no-follow regular-file reader with before/opened/after descriptor and path
identity checks. Digests and JSON parsing consume those same captured bytes.
The process runs under isolated Python with no inherited `PYTHON*` behavior,
uses explicit conditional failures rather than optimization-removable
`assert`, and binds the dispatch byte digest into the Task 0 audit and
acceptance evidence. The Task 0 author receives immutable control-document
paths and anchor SHA, never mutable PR prose. Run in the execution worktree:

```bash
set -eu
test -n "${PUBLISHED_ANCHOR_PROJECTION_SHA256:-}"
test -n "${PUBLISHED_ANCHOR_AUTHORS_SHA256:-}"
test -n "${PUBLISHED_ANCHOR_REVIEWS_SHA256:-}"
test -n "${PUBLISHED_ANCHOR_GENERATION_ID:-}"
test -n "${PUBLISHED_ANCHOR_LIVE_POINTER_SHA256:-}"
test -n "${PUBLISHED_ANCHOR_EVIDENCE_PARENT_IDENTITY:-}"
test -n "${PUBLISHED_TASK_00_DISPATCH_SHA256:-}"
test -n "${TASK_00_AUTHOR_TASK_PATH:-}"
test -n "${PHASE_01_EXTERNAL_EVIDENCE_PARENT:-}"
test -n "${PHASE_01_EXTERNAL_EVIDENCE_ROOT:-}"
test -n "${PHASE_01_TASK_DISPATCH_ROOT:-}"
test -n "${PHASE_01_PUBLISHED_ANCHOR_SHA:-}"
test -n "${PHASE_01_PUBLISHED_ANCHOR_TREE:-}"
test -n "${PHASE_01_PUBLISHED_ANCHOR_PARENT:-}"
test -n "${PHASE_01_TASK_MINUS_ONE_CHAIN:-}"
test -n "${GOVERNANCE_BASE_SHA:-}"
test -n "${CONTRACT_INTRODUCTION_SHA:-}"
test -n "${CONTRACT_INTRODUCTION_TREE:-}"
test -n "${CONTRACT_INTRODUCTION_BLOB:-}"
env -i PATH="$PATH" LC_ALL=C.UTF-8 python -I -B -X utf8 -S - \
  "$PHASE_01_EXTERNAL_EVIDENCE_PARENT" \
  "$PHASE_01_EXTERNAL_EVIDENCE_ROOT" \
  "$PHASE_01_TASK_DISPATCH_ROOT" \
  "$PUBLISHED_ANCHOR_GENERATION_ID" \
  "$PUBLISHED_ANCHOR_EVIDENCE_PARENT_IDENTITY" \
  "$PUBLISHED_ANCHOR_LIVE_POINTER_SHA256" \
  "$PUBLISHED_ANCHOR_PROJECTION_SHA256" \
  "$PUBLISHED_ANCHOR_AUTHORS_SHA256" \
  "$PUBLISHED_ANCHOR_REVIEWS_SHA256" \
  "$PUBLISHED_TASK_00_DISPATCH_SHA256" \
  "$PHASE_01_PUBLISHED_ANCHOR_SHA" \
  "$PHASE_01_PUBLISHED_ANCHOR_TREE" \
  "$TASK_00_AUTHOR_TASK_PATH" \
  "$PHASE_01_PUBLISHED_ANCHOR_PARENT" \
  "$PHASE_01_TASK_MINUS_ONE_CHAIN" \
  "$GOVERNANCE_BASE_SHA" \
  "$CONTRACT_INTRODUCTION_SHA" \
  "$CONTRACT_INTRODUCTION_TREE" \
  "$CONTRACT_INTRODUCTION_BLOB" <<'PY'
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

MAX_CONTROL_BYTES = 16_384
MAX_SEALED_BYTES = 1_048_576
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
AUTHOR_PATH = re.compile(r"/root(?:/[a-z0-9_]+)+\Z")
RUN_ID = "phase-01-governance-2026-07-14"


def fail(detail):
    raise SystemExit(detail)


def require(condition, detail):
    if not condition:
        fail(detail)


def is_reparse(metadata):
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(flag and attributes & flag)


def signature(metadata):
    return (
        metadata.st_dev,
        metadata.st_ino,
        stat.S_IFMT(metadata.st_mode),
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def canonical_directory(raw, label):
    candidate = Path(raw)
    require(candidate.is_absolute(), f"{label} is not absolute")
    resolved = candidate.resolve(strict=True)
    require(Path(os.path.abspath(candidate)) == resolved, f"{label} is not canonical")
    metadata = resolved.lstat()
    require(not is_reparse(metadata), f"{label} is a link or reparse point")
    require(stat.S_ISDIR(metadata.st_mode), f"{label} is not a directory")
    return resolved


def read_verified(path, maximum, label):
    descriptor = None
    try:
        before = path.lstat()
        require(not is_reparse(before), f"{label} is a link or reparse point")
        require(stat.S_ISREG(before.st_mode), f"{label} is not regular")
        require(0 < before.st_size <= maximum, f"{label} has invalid size")
        nofollow = getattr(os, "O_NOFOLLOW", 0)
        require(bool(nofollow), f"{label} no-follow open is unavailable")
        flags = (
            os.O_RDONLY
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOINHERIT", 0)
            | nofollow
            | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        require(signature(opened) == signature(before), f"{label} identity changed")
        chunks = bytearray()
        while len(chunks) <= maximum:
            chunk = os.read(descriptor, min(65_536, maximum + 1 - len(chunks)))
            if not chunk:
                break
            chunks.extend(chunk)
        require(len(chunks) <= maximum, f"{label} exceeds byte limit")
        after_descriptor = os.fstat(descriptor)
        after_path = path.lstat()
        require(signature(after_descriptor) == signature(opened), f"{label} mutated")
        require(signature(after_path) == signature(opened), f"{label} path changed")
        return bytes(chunks)
    except OSError:
        fail(f"{label} could not be captured")
    finally:
        if descriptor is not None:
            os.close(descriptor)


def parse_canonical(raw, label):
    require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), f"{label} newline")

    def closed_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate {label} key")
            result[key] = value
        return result

    def reject_number(_value):
        fail(f"{label} contains a forbidden number")

    try:
        value = json.loads(
            raw[:-1].decode("utf-8", "strict"),
            object_pairs_hook=closed_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
        canonical = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8") + b"\n"
    except (TypeError, UnicodeError, ValueError):
        fail(f"{label} is invalid JSON")
    require(raw == canonical, f"{label} is not canonical")
    require(isinstance(value, dict), f"{label} root is not an object")
    return value


def value_matches(mapping, key, expected):
    return type(mapping.get(key)) is type(expected) and mapping.get(key) == expected


def main(arguments):
    require(len(arguments) == 19, "invalid acceptance arguments")
    (
        parent_raw,
        generation_raw,
        dispatch_root_raw,
        generation_id,
        parent_identity,
        pointer_digest,
        projection_digest,
        authors_digest,
        reviews_digest,
        dispatch_digest,
        anchor_sha,
        anchor_tree,
        author_task_path,
        anchor_parent,
        task_minus_one_chain,
        governance_base_sha,
        contract_introduction_sha,
        contract_introduction_tree,
        contract_introduction_blob,
    ) = arguments
    for digest in (
        generation_id,
        parent_identity,
        pointer_digest,
        projection_digest,
        authors_digest,
        reviews_digest,
        dispatch_digest,
    ):
        require(isinstance(digest, str) and HEX64.fullmatch(digest), "invalid digest")
    require(HEX40.fullmatch(anchor_sha) is not None, "invalid anchor SHA")
    require(HEX40.fullmatch(anchor_tree) is not None, "invalid anchor tree")
    for git_identity in (
        anchor_parent,
        governance_base_sha,
        contract_introduction_sha,
        contract_introduction_tree,
        contract_introduction_blob,
    ):
        require(HEX40.fullmatch(git_identity) is not None, "invalid Git identity")
    require(AUTHOR_PATH.fullmatch(author_task_path) is not None, "invalid author path")
    projected_chain = task_minus_one_chain.splitlines()
    require(
        len(projected_chain) >= 2
        and len(set(projected_chain)) == len(projected_chain)
        and all(HEX40.fullmatch(commit) is not None for commit in projected_chain),
        "invalid Task -1 chain",
    )
    require(projected_chain[0] == contract_introduction_sha, "wrong chain introduction")
    require(projected_chain[-1] == anchor_sha, "wrong chain head")
    require(projected_chain[-2] == anchor_parent, "wrong chain parent")

    parent = canonical_directory(parent_raw, "evidence parent")
    generation = canonical_directory(generation_raw, "evidence generation")
    dispatch_root = canonical_directory(dispatch_root_raw, "dispatch root")
    require(generation == parent / f"generation-{generation_id}", "wrong generation")
    require(
        dispatch_root != parent
        and parent not in dispatch_root.parents
        and dispatch_root not in parent.parents,
        "dispatch root is not separate",
    )
    canonical_parent = os.path.normcase(os.path.normpath(str(parent)))
    observed_parent_identity = hashlib.sha256(
        (canonical_parent + "\n").encode("utf-8")
    ).hexdigest()
    require(observed_parent_identity == parent_identity, "evidence parent moved")

    raw_worktrees = subprocess.check_output(
        ["git", "worktree", "list", "--porcelain", "-z"]
    )
    worktrees = [
        Path(item[9:].decode("utf-8", "strict")).resolve(strict=True)
        for item in raw_worktrees.split(b"\0")
        if item.startswith(b"worktree ")
    ]
    common = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            text=True,
        ).strip()
    ).resolve(strict=True)
    require(bool(worktrees), "worktree inventory is empty")
    for external in (parent, generation, dispatch_root):
        for repository_path in (*worktrees, common):
            require(
                external != repository_path
                and repository_path not in external.parents
                and external not in repository_path.parents,
                "external evidence overlaps a repository",
            )

    expected_entries = [
        "author-inventory.json",
        "published-anchor-projection.json",
        "published-anchor-reviews.json",
    ]
    require(
        sorted(path.name for path in generation.iterdir()) == expected_entries,
        "generation file set differs",
    )

    pointer_raw = read_verified(parent / "live-generation.json", MAX_CONTROL_BYTES, "pointer")
    require(hashlib.sha256(pointer_raw).hexdigest() == pointer_digest, "pointer digest")
    pointer = parse_canonical(pointer_raw, "pointer")
    pointer_keys = {
        "schema_version",
        "run_id",
        "generation_id",
        "relative_directory",
        "anchor_sha",
        "anchor_tree",
        "evidence_parent_identity",
        "projection_sha256",
        "author_inventory_sha256",
        "reviews_sha256",
    }
    require(set(pointer) == pointer_keys, "pointer keys differ")
    pointer_expected = {
        "schema_version": "published-anchor-live-pointer/v1",
        "run_id": RUN_ID,
        "generation_id": generation_id,
        "relative_directory": f"generation-{generation_id}",
        "anchor_sha": anchor_sha,
        "anchor_tree": anchor_tree,
        "evidence_parent_identity": parent_identity,
        "projection_sha256": projection_digest,
        "author_inventory_sha256": authors_digest,
        "reviews_sha256": reviews_digest,
    }
    require(pointer == pointer_expected, "pointer values differ")

    sealed = {}
    for name, expected_digest in (
        ("published-anchor-projection.json", projection_digest),
        ("author-inventory.json", authors_digest),
        ("published-anchor-reviews.json", reviews_digest),
    ):
        captured = read_verified(generation / name, MAX_SEALED_BYTES, name)
        require(hashlib.sha256(captured).hexdigest() == expected_digest, f"{name} digest")
        sealed[name] = parse_canonical(captured, name)
    projection = sealed["published-anchor-projection.json"]
    authors = sealed["author-inventory.json"]
    reviews = sealed["published-anchor-reviews.json"]
    require(value_matches(projection, "run_id", RUN_ID), "projection run")
    require(value_matches(projection, "base_sha", governance_base_sha), "projection base")
    require(value_matches(projection, "head_sha", anchor_sha), "projection anchor")
    require(value_matches(projection, "head_tree_sha", anchor_tree), "projection tree")
    require(value_matches(projection, "head_parent_sha", anchor_parent), "projection parent")
    require(
        value_matches(projection, "task_minus_one_commit_chain", projected_chain),
        "projection chain",
    )
    require(
        value_matches(projection, "contract_introduction_sha", contract_introduction_sha),
        "projection contract introduction",
    )
    require(
        value_matches(
            projection,
            "contract_introduction_tree_sha",
            contract_introduction_tree,
        ),
        "projection contract tree",
    )
    require(
        value_matches(
            projection,
            "contract_introduction_blob_sha",
            contract_introduction_blob,
        ),
        "projection contract blob",
    )
    require(value_matches(authors, "run_id", RUN_ID), "authors run")
    require(value_matches(reviews, "run_id", RUN_ID), "reviews run")
    require(value_matches(reviews, "anchor_sha", anchor_sha), "reviews anchor")
    require(value_matches(reviews, "anchor_tree", anchor_tree), "reviews tree")

    generation_material = "".join(
        digest + "\n" for digest in (projection_digest, authors_digest, reviews_digest)
    ).encode("ascii")
    require(
        hashlib.sha256(generation_material).hexdigest() == generation_id,
        "generation identity differs",
    )

    dispatch_path = dispatch_root / f"task-00-dispatch-{generation_id}.json"
    dispatch_raw = read_verified(dispatch_path, MAX_CONTROL_BYTES, "dispatch file")
    require(hashlib.sha256(dispatch_raw).hexdigest() == dispatch_digest, "dispatch digest")
    dispatch = parse_canonical(dispatch_raw, "dispatch")
    dispatch_keys = {
        "schema_version",
        "task_id",
        "generation_id",
        "evidence_parent_identity",
        "live_pointer_sha256",
        "projection_sha256",
        "author_inventory_sha256",
        "reviews_sha256",
        "anchor_sha",
        "anchor_tree",
        "author_task_path",
        "dispatched_at",
    }
    require(set(dispatch) == dispatch_keys, "dispatch keys differ")
    dispatch_expected = {
        "schema_version": "task-dispatch/v1",
        "task_id": 0,
        "generation_id": generation_id,
        "evidence_parent_identity": parent_identity,
        "live_pointer_sha256": pointer_digest,
        "projection_sha256": projection_digest,
        "author_inventory_sha256": authors_digest,
        "reviews_sha256": reviews_digest,
        "anchor_sha": anchor_sha,
        "anchor_tree": anchor_tree,
        "author_task_path": author_task_path,
    }
    for key, expected in dispatch_expected.items():
        require(value_matches(dispatch, key, expected), f"dispatch {key} differs")
    dispatched_at = dispatch.get("dispatched_at")
    require(isinstance(dispatched_at, str), "dispatch time type")
    try:
        dispatched = datetime.strptime(dispatched_at, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        fail("dispatch time grammar")
    now = datetime.now(timezone.utc)
    require(dispatched <= now, "dispatch is in the future")
    require(now - dispatched <= timedelta(minutes=15), "dispatch is stale")


try:
    main(sys.argv[1:])
except (OSError, subprocess.SubprocessError, UnicodeError, ValueError):
    fail("Task 0 acceptance failed")
PY
export GIT_NO_REPLACE_OBJECTS=1
test -z "${GIT_ALTERNATE_OBJECT_DIRECTORIES:-}"
GIT_COMMON_DIR=$(git --no-replace-objects rev-parse --path-format=absolute --git-common-dir)
test -z "$(git --no-replace-objects for-each-ref --format='%(refname)' refs/replace)"
test ! -e "$GIT_COMMON_DIR/info/grafts"
test ! -e "$GIT_COMMON_DIR/objects/info/alternates"
test ! -e "$GIT_COMMON_DIR/shallow"
test "$(git --no-replace-objects rev-parse --is-shallow-repository)" = "false"
test "$(git --no-replace-objects rev-parse HEAD)" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git --no-replace-objects rev-parse 'HEAD^{tree}')" = "$PHASE_01_PUBLISHED_ANCHOR_TREE"
test "$(git --no-replace-objects rev-parse 'HEAD^')" = "$PHASE_01_PUBLISHED_ANCHOR_PARENT"
test "$(git --no-replace-objects rev-parse '@{upstream}')" = "$PHASE_01_PUBLISHED_ANCHOR_SHA"
test "$(git --no-replace-objects branch --show-current)" = "agent/phase-01-governance"
test "$(git --no-replace-objects rev-list --parents -n 1 HEAD | wc -w)" -eq 2
test "$(git --no-replace-objects rev-parse "$CONTRACT_INTRODUCTION_SHA^")" = "$GOVERNANCE_BASE_SHA"
test "$(git --no-replace-objects rev-parse "$CONTRACT_INTRODUCTION_SHA^{tree}")" = "$CONTRACT_INTRODUCTION_TREE"
test "$(git --no-replace-objects rev-parse "$CONTRACT_INTRODUCTION_SHA:docs/evidence/contracts/phase-01-governance.toml")" = "$CONTRACT_INTRODUCTION_BLOB"
test "$(git --no-replace-objects rev-parse "HEAD:docs/evidence/contracts/phase-01-governance.toml")" = "$CONTRACT_INTRODUCTION_BLOB"
test "$(git --no-replace-objects rev-list --reverse "$CONTRACT_INTRODUCTION_SHA^..HEAD")" = "$PHASE_01_TASK_MINUS_ONE_CHAIN"
for TASK_MINUS_ONE_COMMIT in $(git --no-replace-objects rev-list --reverse "$CONTRACT_INTRODUCTION_SHA..HEAD"); do
  test "$(git --no-replace-objects rev-list --parents -n 1 "$TASK_MINUS_ONE_COMMIT" | wc -w)" -eq 2
  test "$(git --no-replace-objects diff-tree --no-commit-id --name-only -r "$TASK_MINUS_ONE_COMMIT")" = "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md"
  test "$(git --no-replace-objects rev-parse "$TASK_MINUS_ONE_COMMIT:docs/evidence/contracts/phase-01-governance.toml")" = "$CONTRACT_INTRODUCTION_BLOB"
done
test -z "$(git status --porcelain=v1)"
```

An absent in-memory checkpoint, changed digest, stale dispatch, or changed
identity is not recoverable from repository text: rerun Task -1 capture and
both reviews. `docs/audits/2026-07-14-governance-oracle-review.md` records the
accepted `PUBLISHED_TASK_00_DISPATCH_SHA256`, and every Task 0 review/evidence
record binds that digest with the three checkpoint digests.

- [ ] **Step 1: Write and prove the RED oracle validator**

The standalone standard-library validator rejects missing files, duplicate/
blank/unknown IDs, wrong 105/198/9 counts, invalid TOML shape, unresolved source
paths/sections, normalized clause-digest mismatch, missing G00–G20 children,
non-bidirectional requirement/clause edges, and truth criteria outside the
closed registry. Run it before fixture creation and record the expected missing-
oracle failure.

The validator has no third-party TOML dependency. CPython 3.11–3.14 use
`tomllib` as the authoritative parser and also exercise the embedded fallback
directly. CPython 3.9 and 3.10 do not provide `tomllib`; those cells honestly
exercise the fallback only and make no native-parser parity claim. This is not
a general TOML reader. It accepts only the following reviewed grammar used by
the six frozen fixtures; any unspecified syntax fails closed:

- The three ID fixtures are terminal-newline-terminated ASCII, with exactly one
  nonempty ID per line and no whitespace or comment syntax. Requirement IDs are
  `[A-Z][A-Z0-9]*-[0-9]{2}`; skill IDs are lowercase alphanumeric hyphen tokens;
  specifically `[a-z0-9]+(?:-[a-z0-9]+)*`; profile IDs use that same token
  grammar with the exact `profile-` prefix.
- TOML documents use bare ASCII keys only. The provenance top level has exactly
  `schema_version`, `required_record_fields`, and `source_ids`. The clause top
  level has exactly `schema_version`, `normalization`, `hash_domain`, and
  repeated `[[clauses]]` records whose keys are exactly `clause_id`, `path`,
  `section`, `sha256`, `assertion_kind`, and `requirement_ids`. The check top
  level has exactly `schema_version`, `order`, `truth_criteria_registry`,
  `artifact_class_registry`, `state_truth`, `externally_blockable_check_ids`,
  and repeated `[[checks]]` records whose keys are exactly `check_id`, `gate_id`,
  `required`, `scheduled_phase`, `schedule_state`, `requirement_ids`,
  `clause_ids`, `truth_criteria`, and `expected_artifact_classes`.
- Values are single-line unescaped double-quoted strings, nonempty single-line
  arrays of those strings, lowercase `true`/`false`, or canonical unsigned
  decimal integers matching `0|[1-9][0-9]{0,9}` and not exceeding 2,147,483,647.
  String payloads admit printable ASCII except `"` and `\\`, plus U+2014 only;
  that single reviewed non-ASCII scalar is required by the clause section names.
  The sole inline-table form is `state_truth`: exactly the bare keys `PASS`,
  `NOT_APPLICABLE`, and `BLOCKED`, each mapped to a permitted string array.
- Every one of the six fixtures accepts either LF or CRLF consistently and ends
  with exactly one such line ending; a mixed-ending file is rejected. TOML
  nonblank lines have no leading or trailing horizontal whitespace. Assignments
  use exactly one U+0020 on each side of `=`, array and inline-table elements use
  exactly comma-plus-U+0020 separators, and the two array-table headers contain
  no whitespace. Blank lines are the only otherwise empty TOML lines.
- A top-level key is unique in its document, a record key is unique within its
  current array-table record, and an inline-table key is unique within that
  table. Each exact `[[clauses]]` or `[[checks]]` header starts a new record.
  Cross-record reuse of record-field names is the only duplicate-key reuse.
  Regular tables, nested/dotted/quoted keys, literal or multiline strings,
  escapes, signed/base-prefixed/underscored integers, floats, dates, null-like
  values, heterogeneous/nested arrays, trailing commas, and comments are not
  part of the grammar and are rejected even when a broader TOML parser could
  accept a particular form.

Every fallback-accepted TOML document is consequently valid TOML 1.0, but the
converse is intentionally false. Schema validation after parsing still enforces
the exact key sets, record counts, ordering, and semantic inventory equality.

Before classifying or rejecting any comment marker, the fallback validates the
entire decoded input and rejects TOML-forbidden raw control characters. It
accepts line endings only as LF or CRLF, rejects a bare CR, and rejects Unicode
NEL and line/paragraph separators U+0085, U+2028, and U+2029. An unquoted `#`
is then rejected because this fixture grammar has no comments; `#` inside an
otherwise permitted basic string is data. No comment stripping or other
preprocessing step may turn malformed input into an accepted document.

The frozen differential corpus has three explicit outcome classes. Shared-valid
cases include all three TOML fixtures under LF and CRLF plus minimal examples of
each permitted scalar/container; on CPython 3.11–3.14 native and fallback values
must be structurally equal. Invalid-TOML cases include every forbidden raw
control before and after `#`, bare CR, U+0085/U+2028/U+2029, malformed and
unterminated literal strings (`'unterminated`, a raw newline before the closing
quote, and surplus tokens after a closing quote), duplicate keys in each scope,
malformed arrays/inline tables/array-table headers, and trailing tokens; native
and fallback must both reject them. Native-valid-but-unsupported cases include
a valid literal string, escaped basic string, comment, dotted/quoted key,
regular table, signed or underscored integer, and multiline string; native must
accept and fallback must reject, proving the boundary is deliberate. CPython
3.9/3.10 freeze the fallback outcome for every named corpus case without
claiming an unavailable native comparison.

Run the isolated local harness specified in Step 3. In the RED state it must
exit with its declared missing-root, missing-module, or failed-stage supervisor
code, never a startup-controlled zero.

- [ ] **Step 2: Assign independent specification authors**

Use context-free non-implementation agents. One derives requirement, skill,
profile, provenance, and clause inventories directly from the immutable control
documents; another reviews exact equality, normalized clause digests, the
105/198/9 counts, source entries, and the complete G00–G20 child/truth-criteria
inventory. They do not author the manifests or runner.

- [ ] **Step 3: Verify GREEN and freeze the oracle commit**

The oracle includes child IDs, required flags, clause/requirement edges, and
truth criteria, but no executable command realization. The review records source
document digests and all dispositions. `tests/test_governance_oracles.py` also
freezes the Windows workflow's all-PR and branch-restricted all-push triggers
with no path filter; runner; exact Windows x64 patch matrix 3.9.13, 3.10.11,
3.11.9, 3.12.10, 3.13.14, and 3.14.6; exact action SHAs; two fully qualified
mandatory test names; full-module execution; and zero-skip result check. The
native junction test is conditionally defined only when
`os.name == "nt"`; it has no skip decorator, and failure to provision its
junction fixture fails the test. The simulated reparse test remains registered
on every platform. A source regression asserts that the module contains no
runtime skip call, unittest skip decorator, or `expectedFailure` reference.
Every suite captures `suite.countTestCases()` before execution and accepts a
result only when `testsRun` equals that count, `wasSuccessful()` is true, and
`skipped`, `expectedFailures`, and `unexpectedSuccesses` are all empty. Each
mandatory single-test suite must additionally have a pre-run count of one.
The full suite is bound to an embedded exact inventory of fully qualified test
IDs: 52 on the current non-Windows Task 0 subject and 49 on Windows, where four
POSIX-only tests are absent and the mandatory native-junction test is present.
Discovery order, IDs, and cardinality must match exactly before any test runs.
The ASCII-LF inventories are content-addressed as
`0dc6c93343d96463783a39c6ac91aab399a10411c496a923eb70a8b41f145078`
for non-Windows and
`c5845af178802905e0c02a2ccdc79a188cf5cd42cfd8020fb5824907177f4adc`
for Windows.
Task 0 extends existing inventory-preserving regression methods for new hostile
cases; it does not add, delete, or rename a test method unless this independent
control and both platform inventories are amended first.

Every trusted Task 0 Python process—checkpoint acceptance, workflow supervisor,
local supervisor, every supervised child, and `compileall`—starts with the
complete `python -I -B -X utf8 -S` isolation set; neither command nor workflow
environment sets `PYTHONPATH`. The inline supervisor imports trusted standard-library modules
only and never imports or executes repository code in its process. It validates
the checkout, `src`, `tests`, `scripts`, `scripts/governance`, and
`src/python_doctor` component by component: every resolved path is root-
contained, every component is a directory, and no component is a symlink or an
observed Windows reparse point. A bounded recursive before/after snapshot
rejects non-regular files, symlink/reparse descendants, identity changes, and
persistent mutation of any Python file in those roots during a stage.
The same bounded, descriptor-read, no-follow snapshot explicitly enumerates
every Task 0 artifact: the Windows workflow, exact Task 0 audit, three script
files, test module, and six governance fixtures. Entries already covered by a
watched root are identity/digest compared rather than silently skipped. Thus
the workflow and audit are protected even though neither is below `tests`,
`scripts`, or `src/python_doctor`.

Every repository-controlled stage runs in its own new
`python -I -B -X utf8 -S` child. Before repository import, the child reduces
`sys.path` to the interpreter's validated standard-library, zip-library, and
dynamic-loader entries. It installs one closed finder backed by exact-origin
`SourceFileLoader` instances for only `tests`,
`tests.test_governance_oracles`, `scripts`, `scripts.governance`,
`scripts.governance.validate_oracles`, and `python_doctor`. The finder validates
the caller-supplied package path, source identity, loader, `spec.origin`, and
package search locations against the predeclared resolved file before and after
load. An allowlisted-prefix miss or redirected `__path__` raises immediately and
never falls through to a later meta finder, path hook, or `sys.path` lookup.
Repository paths never enter `sys.path`; all child import machinery and path
state must equal the captured closed state after the stage. Before repository
import, the child clears `sys.path_importer_cache`, repopulates it once for the
closed trusted path, and captures each exact key, finder type,
origin path/archive, and loader table. Post-stage validation repopulates and
requires every baseline key with the same validated fingerprint. Additional
package-cache keys are allowed only when root-contained by a trusted
stdlib/zip/dynamic-loader path and backed by a validated FileFinder/zip loader;
equivalent trusted finder reconstitution is allowed, but an unknown finder is not.
Baseline non-project modules must
retain every original `sys.modules` key and its object/spec/loader/origin
identity, including the identity of the dictionary key and the initially
captured key/spec-name/module-name relationship; equality is never accepted as
identity. This preserves CPython's pre-existing frozen aliases such as
`os.path`/`posixpath` only when their original key object and original names are
unchanged. Every later non-project module must instead satisfy exact
`sys.modules` key = spec name = module name and have a built-in, frozen, or
validated stdlib/zip/dynamic-loader origin and corresponding exact loader type.
Built-in and frozen loaders are accepted only by frozen class identity.
File-backed loaders bind their exact frozen class, module/spec/loader name,
path, frozen suffix backend, and origin; zip loaders bind the exact frozen
`zipimporter` type, archive, normalized prefix, module/spec name, and the exact
`get_filename()` member origin. Each stage also declares the exact project-
module set it must leave loaded; deletion of either a baseline module or a
required project module is a failure. Loader-class references and source,
bytecode, and extension suffix tuples are captured before repository import
and never reread from mutable `importlib` module state afterward.
The complete class dictionaries of every approved loader/finder class and each
non-`object` class in their method-resolution orders are identity-frozen and
rechecked before post-stage import work. This includes `PathFinder`,
`FileFinder`, built-in/frozen importers, source/bytecode/extension loaders,
`zipimporter`, and the two project-only loader/finder classes; adding, deleting,
or replacing even an inherited method fails. Each class's exact `__bases__`
and `__mro__` tuple objects and every member of the MRO are frozen too, so even
an equivalent base reassignment fails. Exact loader/finder instances
retain their version-independent closed attribute shape with no callable
shadowing. The exact built-in `dict` containers for
`sys.modules`/`sys.path_importer_cache` and built-in `list` containers for
`sys.path`/`sys.path_hooks`/`sys.meta_path` are identity-bound. Project loads
are recorded before repository execution as an exact key/module/spec/loader
registry. Their stored import attributes, loader-state values, package path
containers, and every path/search-location string are verified immediately
after `exec_module` returns and retained by object identity through final stage
validation. Every
promised baseline stored import attribute—including presence versus absence,
spec-less module name, spec origin, module package/cache/path state, spec
loader/search-location state, and loader name/path/archive/prefix—is likewise
retained by object identity.
The registry's exact key set must equal the stage's declared required project
module set, and every registry key must be the identical `sys.modules` key
object captured at load. An allowlisted project module imported and then
deleted remains an extra registry entry and fails even when the final visible
project-module set otherwise matches.

The workflow supervisor launches separate native-test, simulated-test,
full-module, and validator children; the local supervisor omits the native child
off Windows because that test is intentionally not registered there. A child
accepts a test stage only under the complete result predicate above and accepts
the validator only for exact integer zero. Only after all stage checks and
post-stage import/path/source checks pass does trusted child code flush a
stage-and-nonce evidence line and terminate with that stage's distinctive
nonzero success sentinel. The supervisor replays captured child stdout/stderr
and accepts only the exact sentinel plus exactly one matching evidence line.
Exit zero, hard `os._exit(0)`, another code, missing/duplicate evidence,
exception, skip, expected failure, unexpected success, wrong `testsRun`,
validator nonzero/non-integer, or before/after mutation is a parent failure.

Tests parse the Task 0 acceptance block, exact workflow, exact local supervisor,
supervisor child argv, and compileall line. They fail if any trusted Python
invocation lacks `python -I -B -X utf8 -S`, if `PYTHONPATH` occurs anywhere in
either supervisor, if an unapproved project import is added to the
finder, if any repository path is added to `sys.path`, or if a repository path
precedes the trusted startup paths. Hostile regressions cover symlink/reparse
components and files; redirected package `__path__`; an allowlisted module miss;
a later meta finder, path hook, or repository `sys.path` entry; persistent source
mutation; hard exit zero; validator exception/`SystemExit`; a suite that runs
fewer tests than collected; and `expectedFailure`/unexpected-success cases.
The import-cache regression persists a cache finder for a trusted key and uses
it to attempt loading a non-prefix repository payload; both the payload origin
check and the post-stage cache object/fingerprint comparison must fail.
A dedicated equality-spoofing attribute-object regression and a separate
`EvilLoader`-subclass-of-`SourceFileLoader` regression must not satisfy identity
or exact-loader checks. Two more independent regressions delete baseline `json`
and a stage-required project module from `sys.modules`; both must fail even
when all remaining modules validate.
Further cases replace a baseline key with a distinct equal `str`, add an alias
key for a valid stdlib module, mutate an importlib suffix list before installing
an injected-suffix `FileFinder`, and mismatch a zip module's declared name from
the exact `zipimporter.get_filename()` origin; each must fail closed.
Independent cases shadow `get_code` on an exact `SourceFileLoader` instance,
mutate a frozen loader class method, reassign the same or different loader
`__bases__` tuple, replace a project module while reusing its
spec/loader, substitute `HidingModules`/`HidingCache` dictionary subclasses,
and replace each import-state list with an equal list; each must fail closed.
Separate red-green cases use distinct equal objects for baseline `spec.origin`
and name attributes, replace spec-less-module and loader name/path attributes,
install `os.PathLike` project name/origin/file/path/search-location values,
replace a project module with an equivalent object, mutate the exact
`SourceFileLoader` class or instance, shadow `FileFinder`/`zipimporter`
callables, and hide entries behind dict/list subclasses. Each regression first
passes against the intact gate, then fails solely because of its hostile
mutation; restoring that mutation makes the same gate pass again.
Separate cases reject a new `None` negative-cache entry and a
purelib/platlib/user-site or `site-packages`/`dist-packages` finder and payload,
even when that install root is a descendant of stdlib. A positive portable
case freezes nested zip-package keys by requiring the cache key to equal the
trusted archive joined to the zipimporter's normalized prefix.
Snapshot regressions additionally require a traversal/scandir error, excessive
entry count, excessive depth, and persistent mutation of each non-Python
`.txt`/`.toml` oracle class to fail closed; every regular watched file is
identity-bound and hashed, not only Python source.
Independent persistent mutations of
`.github/workflows/governance-oracles-windows.yml` and
`docs/audits/2026-07-14-governance-oracle-review.md` must also fail at the
outer snapshot boundary. A full-suite source regression deletes one
non-mandatory test and fails exact ID/cardinality validation. Another imports
the allowlisted `python_doctor`, deletes it from `sys.modules`, and fails the
exact project-registry set check.
They also retain the exit-zero `sitecustomize.py`, `usercustomize.py`, and
`unittest.py` traps in checkout root and `src`. Every case must yield the
supervisor's declared failure, not a successful workflow.

The stage dispatcher captures the original verifier and suite runner in local
default arguments before repository execution; replacing the ordinary
`__main__.verify_import_state` name therefore does not replace the reference
used after the suite. A regression's `tearDownModule` replaces that public name
and deletes baseline `json`; the captured verifier must still reject deletion.

**Exact same-process boundary:** This protocol detects accidental bypasses and
the named persistent, non-self-restoring mutations. It does not sandbox
repository code executed in the same Python interpreter. Intentionally
adversarial code that uses frame/global/function introspection, rewrites
captured defaults or code objects, or restores a mutation before validation is
outside this guarantee, whether or not it forges nonce, evidence, or sentinel
values. No stronger same-process authenticity claim is made.

`tests/test_governance_oracles.py` must assert that the preceding exact
same-process-boundary paragraph appears once, that each supervisor captures the
verifier as an `execute_stage` default before repository execution, and that no
text claims same-interpreter sandboxing or protection from self-restoring
introspection attacks.
`G13-HOSTILE-REPOSITORY` remains governed by the separate fail-closed native-
containment requirements above.

Create `.github/workflows/governance-oracles-windows.yml` exactly as follows.
The two action revisions are the verified official `actions/checkout` v7.0.0
and `actions/setup-python` v6.3.0 commits. Both use Node 24 and require runner
2.327.1 or newer; the hosted `windows-2022` runner satisfies that prerequisite.
The official setup-python versions manifest supplies the exact stable Windows
x64 selectors 3.9.13, 3.10.11, 3.11.9, 3.12.10, 3.13.14, and 3.14.6. Later
security releases for the older minors are source-only and have no Windows x64
asset, so moving minor-only selectors are forbidden.

```yaml
name: Governance oracles on Windows

on:
  pull_request:
  push:
    branches:
      - "agent/phase-01-governance"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  governance-oracles-windows:
    name: CPython ${{ matrix.python-version }} / windows-2022
    runs-on: windows-2022
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python-version:
          - "3.9.13"
          - "3.10.11"
          - "3.11.9"
          - "3.12.10"
          - "3.13.14"
          - "3.14.6"
    steps:
      - name: Check out the immutable subject
        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0
        with:
          persist-credentials: false
      - name: Select the matrix interpreter
        uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0
        with:
          python-version: ${{ matrix.python-version }}
          architecture: "x64"
          check-latest: false
      - name: Run mandatory native, simulated, and full oracle tests
        shell: pwsh
        run: |
          @'
          import ast
          import hashlib
          import json
          import os
          import pathlib
          import secrets
          import stat
          import subprocess
          import sys

          MAX_ENTRIES = 8192
          MAX_DEPTH = 32
          MAX_FILE_BYTES = 4 * 1024 * 1024
          MAX_TOTAL_BYTES = 64 * 1024 * 1024

          def fail(code, detail):
              print("oracle supervisor failure: " + detail, file=sys.stderr)
              raise SystemExit(code)

          def is_reparse(metadata):
              flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
              attributes = getattr(metadata, "st_file_attributes", 0)
              return stat.S_ISLNK(metadata.st_mode) or bool(flag and attributes & flag)

          def signature(metadata):
              return (
                  metadata.st_dev,
                  metadata.st_ino,
                  stat.S_IFMT(metadata.st_mode),
                  metadata.st_size,
                  metadata.st_mtime_ns,
                  metadata.st_ctime_ns,
              )

          def within(candidate, parent):
              return candidate == parent or parent in candidate.parents

          def checked_directory(path, root=None):
              absolute = pathlib.Path(os.path.abspath(str(path)))
              try:
                  resolved = absolute.resolve(strict=True)
              except (OSError, RuntimeError):
                  fail(90, "directory resolution")
              if os.path.normcase(str(absolute)) != os.path.normcase(str(resolved)):
                  fail(90, "non-canonical directory")
              cursor = pathlib.Path(resolved.anchor)
              for component in resolved.parts[1:]:
                  cursor = cursor / component
                  metadata = cursor.lstat()
                  if is_reparse(metadata) or not stat.S_ISDIR(metadata.st_mode):
                      fail(90, "unsafe directory component")
              if root is not None and not within(resolved, root):
                  fail(90, "directory escapes checkout")
              return resolved

          def read_regular(path, root):
              try:
                  resolved = path.resolve(strict=True)
                  before = path.lstat()
                  if resolved != path or not within(resolved, root):
                      fail(91, "source escapes checkout")
                  if is_reparse(before) or not stat.S_ISREG(before.st_mode):
                      fail(91, "source is not regular")
                  if before.st_size > MAX_FILE_BYTES:
                      fail(91, "source exceeds cap")
                  flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
                  flags |= getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
                  descriptor = os.open(path, flags)
                  try:
                      opened = os.fstat(descriptor)
                      if signature(opened) != signature(before):
                          fail(91, "source identity changed")
                      chunks = bytearray()
                      while len(chunks) <= MAX_FILE_BYTES:
                          part = os.read(descriptor, min(65536, MAX_FILE_BYTES + 1 - len(chunks)))
                          if not part:
                              break
                          chunks.extend(part)
                      after_fd = os.fstat(descriptor)
                  finally:
                      os.close(descriptor)
                  after_path = path.lstat()
              except OSError:
                  fail(91, "source capture failed")
              if len(chunks) > MAX_FILE_BYTES:
                  fail(91, "source exceeds cap")
              if signature(opened) != signature(after_fd) or signature(opened) != signature(after_path):
                  fail(91, "source mutated")
              return bytes(chunks), signature(opened)

          def snapshot(roots, files, checkout):
              records = {}
              total = 0
              count = 0
              for base in roots:
                  pending = [(base, 0)]
                  while pending:
                      current, depth = pending.pop()
                      if depth > MAX_DEPTH:
                          fail(92, "snapshot depth exceeds cap")
                      current = checked_directory(current, checkout)
                      count += 1
                      if count > MAX_ENTRIES:
                          fail(92, "snapshot entry count exceeds cap")
                      records["D:" + current.relative_to(checkout).as_posix()] = signature(current.lstat())
                      try:
                          with os.scandir(current) as iterator:
                              names = []
                              for entry in iterator:
                                  count += 1
                                  if count > MAX_ENTRIES:
                                      fail(92, "snapshot entry count exceeds cap")
                                  names.append(entry.name)
                      except OSError:
                          fail(92, "snapshot traversal failed")
                      child_directories = []
                      for name in sorted(names):
                          path = current / name
                          try:
                              metadata = path.lstat()
                          except OSError:
                              fail(92, "snapshot entry inspection failed")
                          if is_reparse(metadata):
                              fail(92, "snapshot entry is a link or reparse point")
                          if stat.S_ISDIR(metadata.st_mode):
                              child_directories.append(path)
                              continue
                          if not stat.S_ISREG(metadata.st_mode):
                              fail(92, "snapshot entry is not regular")
                          raw, identity = read_regular(path, checkout)
                          total += len(raw)
                          if count > MAX_ENTRIES or total > MAX_TOTAL_BYTES:
                              fail(92, "snapshot exceeds cap")
                          key = "F:" + path.relative_to(checkout).as_posix()
                          records[key] = (identity, hashlib.sha256(raw).hexdigest())
                      for child in reversed(child_directories):
                          pending.append((child, depth + 1))
              for path in files:
                  path = pathlib.Path(os.path.abspath(str(path)))
                  raw, identity = read_regular(path, checkout)
                  key = "F:" + path.relative_to(checkout).as_posix()
                  record = (identity, hashlib.sha256(raw).hexdigest())
                  if key in records:
                      if records[key] != record:
                          fail(92, "enumerated artifact disagrees with root snapshot")
                      continue
                  count += 1
                  total += len(raw)
                  if count > MAX_ENTRIES or total > MAX_TOTAL_BYTES:
                      fail(92, "snapshot exceeds cap")
                  records[key] = record
              return records

          if len(sys.argv) != 2:
              fail(90, "arguments")
          checkout = checked_directory(pathlib.Path(sys.argv[1]))
          if pathlib.Path.cwd().resolve(strict=True) != checkout:
              fail(90, "working directory")
          source = checked_directory(checkout / "src", checkout)
          tests_root = checked_directory(checkout / "tests", checkout)
          scripts_root = checked_directory(checkout / "scripts", checkout)
          checked_directory(scripts_root / "governance", checkout)
          doctor_root = checked_directory(source / "python_doctor", checkout)
          watched_roots = (tests_root, scripts_root, doctor_root)

          module_paths = {
              "tests": (tests_root / "__init__.py", True),
              "tests.test_governance_oracles": (tests_root / "test_governance_oracles.py", False),
              "scripts": (scripts_root / "__init__.py", True),
              "scripts.governance": (scripts_root / "governance" / "__init__.py", True),
              "scripts.governance.validate_oracles": (scripts_root / "governance" / "validate_oracles.py", False),
              "python_doctor": (doctor_root / "__init__.py", True),
          }
          task0_artifacts = tuple(
              checkout / relative
              for relative in (
                  ".github/workflows/governance-oracles-windows.yml",
                  "docs/audits/2026-07-14-governance-oracle-review.md",
                  "scripts/__init__.py",
                  "scripts/governance/__init__.py",
                  "scripts/governance/validate_oracles.py",
                  "tests/test_governance_oracles.py",
                  "tests/fixtures/governance/expected-requirement-ids.txt",
                  "tests/fixtures/governance/expected-skill-ids.txt",
                  "tests/fixtures/governance/expected-profile-domain-ids.txt",
                  "tests/fixtures/governance/expected-provenance-sources.toml",
                  "tests/fixtures/governance/expected-gate-clauses.toml",
                  "tests/fixtures/governance/expected-gate-checks.toml",
              )
          )
          if len(task0_artifacts) != 12 or len(set(task0_artifacts)) != 12:
              fail(92, "Task 0 artifact inventory")
          encoded_modules = {}
          for name, (path, package) in module_paths.items():
              raw, _identity = read_regular(path, checkout)
              encoded_modules[name] = (str(path), package, hashlib.sha256(raw).hexdigest())
          test_raw, _test_identity = read_regular(module_paths["tests.test_governance_oracles"][0], checkout)
          try:
              syntax = ast.parse(test_raw, filename="tests/test_governance_oracles.py")
          except (SyntaxError, ValueError):
              fail(93, "test source syntax")
          for node in ast.walk(syntax):
              if (
                  isinstance(node, ast.Name) and node.id == "expectedFailure"
              ) or (
                  isinstance(node, ast.Attribute) and node.attr == "expectedFailure"
              ):
                  fail(93, "expectedFailure is forbidden")

          CHILD = r'''
          import hashlib
          import importlib.abc
          import importlib.machinery
          import importlib.util
          import json
          import os
          import pathlib
          import site
          import stat
          import sys
          import sysconfig
          import unittest
          import zipimport

          MAX_SOURCE_BYTES = 4 * 1024 * 1024

          def abort():
              os._exit(50)

          def is_reparse(metadata):
              flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
              attributes = getattr(metadata, "st_file_attributes", 0)
              return stat.S_ISLNK(metadata.st_mode) or bool(flag and attributes & flag)

          def signature(metadata):
              return (metadata.st_dev, metadata.st_ino, stat.S_IFMT(metadata.st_mode), metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns)

          def capture(path, expected_digest):
              try:
                  resolved = path.resolve(strict=True)
                  before = path.lstat()
                  if resolved != path or not (resolved == root or root in resolved.parents):
                      abort()
                  if is_reparse(before) or not stat.S_ISREG(before.st_mode) or before.st_size > MAX_SOURCE_BYTES:
                      abort()
                  descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0))
                  try:
                      opened = os.fstat(descriptor)
                      chunks = bytearray()
                      while len(chunks) <= MAX_SOURCE_BYTES:
                          part = os.read(descriptor, min(65536, MAX_SOURCE_BYTES + 1 - len(chunks)))
                          if not part:
                              break
                          chunks.extend(part)
                      after_fd = os.fstat(descriptor)
                  finally:
                      os.close(descriptor)
                  after_path = path.lstat()
              except OSError:
                  abort()
              if len(chunks) > MAX_SOURCE_BYTES:
                  abort()
              raw = bytes(chunks)
              if signature(before) != signature(opened) or signature(opened) != signature(after_fd) or signature(opened) != signature(after_path):
                  abort()
              if hashlib.sha256(raw).hexdigest() != expected_digest:
                  abort()
              return raw

          if len(sys.argv) != 6:
              abort()
          root = pathlib.Path(sys.argv[1])
          stage = sys.argv[2]
          nonce = sys.argv[3]
          success_code = int(sys.argv[4])
          modules = json.loads(sys.argv[5])
          required_project_modules_by_stage = {
              "native": frozenset(("tests", "tests.test_governance_oracles", "scripts", "scripts.governance", "scripts.governance.validate_oracles")),
              "simulated": frozenset(("tests", "tests.test_governance_oracles", "scripts", "scripts.governance", "scripts.governance.validate_oracles")),
              "full": frozenset(("tests", "tests.test_governance_oracles", "scripts", "scripts.governance", "scripts.governance.validate_oracles")),
              "validator": frozenset(("scripts", "scripts.governance", "scripts.governance.validate_oracles")),
          }
          required_project_modules = required_project_modules_by_stage.get(stage)
          if required_project_modules is None:
              abort()
          full_suite_inventory = {
              "posix": (52, "0dc6c93343d96463783a39c6ac91aab399a10411c496a923eb70a8b41f145078"),
              "nt": (49, "c5845af178802905e0c02a2ccdc79a188cf5cd42cfd8020fb5824907177f4adc"),
          }.get(os.name)
          if full_suite_inventory is None:
              abort()
          MODULES_CONTAINER = sys.modules
          IMPORTER_CACHE_CONTAINER = sys.path_importer_cache
          PATH_CONTAINER = sys.path
          PATH_HOOKS_CONTAINER = sys.path_hooks
          META_PATH_CONTAINER = sys.meta_path
          if (
              type(MODULES_CONTAINER) is not dict
              or type(IMPORTER_CACHE_CONTAINER) is not dict
              or type(PATH_CONTAINER) is not list
              or type(PATH_HOOKS_CONTAINER) is not list
              or type(META_PATH_CONTAINER) is not list
          ):
              abort()
          stdlib = pathlib.Path(sysconfig.get_path("stdlib")).resolve(strict=True)
          platstdlib = pathlib.Path(sysconfig.get_path("platstdlib")).resolve(strict=True)
          base = pathlib.Path(sys.base_prefix).resolve(strict=True)
          package_install_roots = set()
          for scheme_key in ("purelib", "platlib"):
              scheme_path = sysconfig.get_path(scheme_key)
              if scheme_path:
                  candidate = pathlib.Path(scheme_path).resolve(strict=False)
                  if candidate not in (stdlib, platstdlib):
                      package_install_roots.add(candidate)
          user_sites = site.getusersitepackages()
          if not user_sites:
              user_sites = ()
          elif isinstance(user_sites, str):
              user_sites = (user_sites,)
          for user_site in user_sites:
              package_install_roots.add(pathlib.Path(user_site).resolve(strict=False))

          def under_package_install_root(candidate):
              lowered_parts = {part.lower() for part in candidate.parts}
              if "site-packages" in lowered_parts or "dist-packages" in lowered_parts:
                  return True
              return any(
                  candidate == package_root or package_root in candidate.parents
                  for package_root in package_install_roots
              )

          sanitized = []
          for item in tuple(sys.path):
              if not item:
                  continue
              candidate = pathlib.Path(item).resolve(strict=False)
              allowed = candidate in (stdlib, platstdlib)
              allowed = allowed or candidate.name in ("lib-dynload", "DLLs") and base in candidate.parents
              allowed = allowed or candidate.suffix == ".zip" and base in candidate.parents
              if allowed and not under_package_install_root(candidate):
                  sanitized.append(str(candidate))
          if not sanitized:
              abort()
          sys.path[:] = sanitized
          closed_path = tuple(sys.path)
          closed_hooks = tuple(sys.path_hooks)
          sys.path_importer_cache.clear()
          cache_probe = "_python_doctor_closed_cache_probe_"
          for item in closed_path:
              importlib.machinery.PathFinder.find_spec(cache_probe, [item])

          BUILTIN_LOADER = importlib.machinery.BuiltinImporter
          FROZEN_LOADER = importlib.machinery.FrozenImporter
          FILE_FINDER = importlib.machinery.FileFinder
          SOURCE_LOADER = importlib.machinery.SourceFileLoader
          SOURCE_SUFFIXES = tuple(importlib.machinery.SOURCE_SUFFIXES)
          BYTECODE_LOADER = importlib.machinery.SourcelessFileLoader
          BYTECODE_SUFFIXES = tuple(importlib.machinery.BYTECODE_SUFFIXES)
          EXTENSION_LOADER = importlib.machinery.ExtensionFileLoader
          EXTENSION_SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
          ZIP_IMPORTER = zipimport.zipimporter
          ZIP_GET_FILENAME = ZIP_IMPORTER.get_filename
          ALLOWED_BACKENDS = (
              (SOURCE_LOADER, SOURCE_SUFFIXES),
              (BYTECODE_LOADER, BYTECODE_SUFFIXES),
              (EXTENSION_LOADER, EXTENSION_SUFFIXES),
          )
          PATH_FINDER = importlib.machinery.PathFinder
          SOURCE_EXEC_MODULE = SOURCE_LOADER.exec_module
          SOURCE_TO_CODE = SOURCE_LOADER.source_to_code
          PATH_FIND_SPEC = PATH_FINDER.find_spec

          def freeze_class_state(owner):
              return owner, owner.__bases__, owner.__mro__, tuple(vars(owner).items())

          def verify_class_states(states):
              for owner, expected_bases, expected_mro, expected in states:
                  current = tuple(vars(owner).items())
                  if (
                      owner.__bases__ is not expected_bases
                      or owner.__mro__ is not expected_mro
                      or len(owner.__mro__) != len(expected_mro)
                      or any(
                          current_owner is not expected_owner
                          for current_owner, expected_owner
                          in zip(owner.__mro__, expected_mro)
                      )
                      or len(current) != len(expected)
                      or any(
                      current_name is not expected_name or current_value is not expected_value
                      for (current_name, current_value), (expected_name, expected_value)
                      in zip(current, expected)
                      )
                  ):
                      abort()

          core_class_owners = []
          for root_class in (
              BUILTIN_LOADER,
              FROZEN_LOADER,
              PATH_FINDER,
              FILE_FINDER,
              SOURCE_LOADER,
              BYTECODE_LOADER,
              EXTENSION_LOADER,
              ZIP_IMPORTER,
              importlib.abc.MetaPathFinder,
          ):
              for owner in root_class.__mro__:
                  if owner is not object and owner not in core_class_owners:
                      core_class_owners.append(owner)
          CORE_CLASS_STATES = tuple(freeze_class_state(owner) for owner in core_class_owners)
          CALLABLE_CLASS_ATTRIBUTES = frozenset(
              name
              for _owner, _bases, _mro, state in CORE_CLASS_STATES
              for name, value in state
              if callable(value)
          )

          MISSING_ATTRIBUTE = object()
          MODULE_IMPORT_ATTRIBUTES = (
              "__name__", "__loader__", "__package__", "__spec__",
              "__path__", "__file__", "__cached__",
          )
          SPEC_IMPORT_ATTRIBUTES = (
              "name", "loader", "origin", "submodule_search_locations",
              "cached", "has_location",
          )
          LOADER_IMPORT_ATTRIBUTES = ("name", "path", "archive", "prefix")

          def read_attribute(subject, name):
              try:
                  return True, getattr(subject, name)
              except AttributeError:
                  return False, MISSING_ATTRIBUTE
              except BaseException:
                  abort()

          def freeze_attributes(subject, names):
              return tuple((name,) + read_attribute(subject, name) for name in names)

          def verify_attributes(subject, expected):
              for name, expected_present, expected_value in expected:
                  present, value = read_attribute(subject, name)
                  if present is not expected_present or value is not expected_value:
                      abort()

          def frozen_attribute(expected, name):
              for attribute_name, present, value in expected:
                  if attribute_name == name:
                      return value if present else MISSING_ATTRIBUTE
              abort()

          def freeze_string_list(value):
              if type(value) is not list or any(type(item) is not str for item in value):
                  abort()
              return value, tuple(value)

          def verify_string_list(value, expected):
              container, items = expected
              if value is not container or type(value) is not list or len(value) != len(items):
                  abort()
              if any(observed is not frozen for observed, frozen in zip(value, items)):
                  abort()

          def freeze_package_paths(module, spec):
              path_present, module_path = read_attribute(module, "__path__")
              spec_path = None if spec is None else spec.submodule_search_locations
              if spec_path is None:
                  if path_present:
                      abort()
                  return None, None
              if not path_present:
                  abort()
              module_state = freeze_string_list(module_path)
              spec_state = freeze_string_list(spec_path)
              if (
                  module_state[0] is not spec_state[0]
                  or len(module_state[1]) != len(spec_state[1])
                  or any(
                      module_item is not spec_item
                      for module_item, spec_item in zip(module_state[1], spec_state[1])
                  )
              ):
                  abort()
              return module_state, spec_state

          def verify_exact_sequence(value, expected, expected_type):
              if type(value) is not expected_type or len(value) != len(expected):
                  abort()
              if any(observed is not frozen for observed, frozen in zip(value, expected)):
                  abort()

          def importer_fingerprint(key, importer):
              if importer is None:
                  return ("none",)
              if type(importer) is FILE_FINDER:
                  if type(key) is not str or type(importer.path) is not str:
                      abort()
                  try:
                      finder_state = vars(importer)
                  except TypeError:
                      abort()
                  if (
                      type(finder_state) is not dict
                      or set(finder_state) != {"path", "_loaders", "_path_mtime", "_path_cache", "_relaxed_path_cache"}
                      or finder_state.get("path") is not importer.path
                      or finder_state.get("_loaders") is not importer._loaders
                      or type(importer._loaders) is not list
                      or type(finder_state.get("_path_cache")) is not set
                      or type(finder_state.get("_relaxed_path_cache")) is not set
                  ):
                      abort()
                  if any(name in CALLABLE_CLASS_ATTRIBUTES for name in finder_state):
                      abort()
                  if pathlib.Path(importer.path).resolve(strict=False) != pathlib.Path(key).resolve(strict=False):
                      abort()
                  if any(
                      type(suffix) is not str
                      or not any(
                          factory is approved_factory and suffix in approved_suffixes
                          for approved_factory, approved_suffixes in ALLOWED_BACKENDS
                      )
                      for suffix, factory in importer._loaders
                  ):
                      abort()
                  return ("file", importer.path, tuple(importer._loaders))
              if type(importer) is ZIP_IMPORTER:
                  if type(key) is not str or type(importer.archive) is not str or type(importer.prefix) is not str:
                      abort()
                  try:
                      zip_state = vars(importer)
                  except TypeError:
                      abort()
                  if (
                      type(zip_state) is not dict
                      or set(zip_state) != {"_files", "archive", "prefix"}
                      or type(zip_state.get("_files")) is not dict
                      or zip_state.get("archive") is not importer.archive
                      or zip_state.get("prefix") is not importer.prefix
                      or any(name in CALLABLE_CLASS_ATTRIBUTES for name in zip_state)
                  ):
                      abort()
                  archive = pathlib.Path(importer.archive).resolve(strict=False)
                  prefix = importer.prefix.replace("/", os.sep).replace("\\", os.sep).strip(os.sep)
                  expected_key = archive if not prefix else pathlib.Path(str(archive) + os.sep + prefix)
                  if pathlib.Path(key).resolve(strict=False) != expected_key.resolve(strict=False):
                      abort()
                  return ("zip", str(archive), prefix)
              abort()

          if set(sys.path_importer_cache) != set(closed_path):
              abort()
          closed_importer_cache = {
              key: importer_fingerprint(key, importer)
              for key, importer in sys.path_importer_cache.items()
          }
          project_identities = {}

          class ExactLoader(SOURCE_LOADER):
              def __init__(self, fullname, path, digest):
                  super().__init__(fullname, path)
                  self.digest = digest

              def get_code(self, fullname):
                  raw = capture(pathlib.Path(self.path), self.digest)
                  return SOURCE_TO_CODE(self, raw, self.path)

              def exec_module(self, module):
                  spec = getattr(module, "__spec__", None)
                  if self.name in project_identities or spec is None or spec.loader is not self:
                      abort()
                  matching_keys = tuple(
                      key
                      for key, value in sys.modules.items()
                      if type(key) is str and key == self.name and value is module
                  )
                  if len(matching_keys) != 1:
                      abort()
                  project_key = matching_keys[0]
                  module_attributes = freeze_attributes(module, MODULE_IMPORT_ATTRIBUTES)
                  spec_attributes = freeze_attributes(spec, SPEC_IMPORT_ATTRIBUTES)
                  loader_attributes = freeze_attributes(self, LOADER_IMPORT_ATTRIBUTES + ("digest",))
                  module_path_state, spec_path_state = freeze_package_paths(module, spec)
                  project_identities[project_key] = (
                      project_key, module, spec, self,
                      module_attributes, spec_attributes, loader_attributes,
                      module_path_state, spec_path_state,
                  )
                  SOURCE_EXEC_MODULE(self, module)
                  identity = project_identities.get(project_key)
                  if (
                      identity is None
                      or identity[0] not in sys.modules
                      or sys.modules[identity[0]] is not module
                      or getattr(module, "__spec__", None) is not spec
                      or spec.loader is not self
                  ):
                      abort()
                  verify_attributes(module, module_attributes)
                  verify_attributes(spec, spec_attributes)
                  verify_attributes(self, loader_attributes)
                  if module_path_state is not None:
                      verify_string_list(module.__path__, module_path_state)
                      verify_string_list(spec.submodule_search_locations, spec_path_state)

          EXACT_LOADER_METHODS = (ExactLoader.get_code, ExactLoader.exec_module)

          class ClosedFinder(importlib.abc.MetaPathFinder):
              prefixes = ("tests", "scripts", "python_doctor")

              def find_spec(self, fullname, path=None, target=None):
                  if fullname.partition(".")[0] not in self.prefixes:
                      return None
                  if fullname not in modules:
                      raise ModuleNotFoundError("allowlisted module miss")
                  raw_path, package, digest = modules[fullname]
                  if type(raw_path) is not str or type(package) is not bool or type(digest) is not str:
                      abort()
                  source_path = pathlib.Path(raw_path)
                  expected_parent = source_path.parent
                  if path is None:
                      if "." in fullname:
                          raise ModuleNotFoundError("missing package path")
                  else:
                      parent_name = fullname.rpartition(".")[0]
                      if parent_name not in modules:
                          raise ModuleNotFoundError("unreviewed parent package")
                      parent_identity = project_identities.get(parent_name)
                      if parent_identity is None or parent_identity[7] is None:
                          raise ModuleNotFoundError("unregistered parent package")
                      verify_string_list(path, parent_identity[7])
                      parent_source = pathlib.Path(modules[parent_name][0])
                      supplied = tuple(pathlib.Path(item).resolve(strict=False) for item in path)
                      if supplied != (parent_source.parent,):
                          raise ModuleNotFoundError("redirected package path")
                  capture(source_path, digest)
                  loader = ExactLoader(fullname, raw_path, digest)
                  spec = importlib.util.spec_from_loader(fullname, loader, is_package=package)
                  if spec is None or pathlib.Path(spec.origin).resolve(strict=False) != source_path:
                      abort()
                  if package and tuple(pathlib.Path(item).resolve(strict=False) for item in spec.submodule_search_locations or ()) != (expected_parent,):
                      abort()
                  return spec

          PROJECT_CLASS_STATES = tuple(
              freeze_class_state(owner) for owner in (ExactLoader, ClosedFinder)
          )

          finder = ClosedFinder()
          try:
              finder_state = vars(finder)
          except TypeError:
              abort()
          if type(finder) is not ClosedFinder or type(finder_state) is not dict or finder_state:
              abort()
          sys.meta_path.insert(0, finder)
          closed_meta = tuple(sys.meta_path)
          trusted_roots = tuple(
              pathlib.Path(item).resolve(strict=False)
              for item in closed_path
              if pathlib.Path(item).suffix != ".zip"
          )
          trusted_archives = tuple(
              os.path.normcase(str(pathlib.Path(item).resolve(strict=False)))
              for item in closed_path
              if pathlib.Path(item).suffix == ".zip"
          )

          def trusted_origin(origin):
              if type(origin) is not str:
                  return False
              if origin == "built-in" or origin == "frozen":
                  return True
              normalized = os.path.normcase(origin)
              if any(
                  normalized == archive or normalized.startswith(archive + os.sep)
                  for archive in trusted_archives
              ):
                  return True
              try:
                  resolved = pathlib.Path(origin).resolve(strict=True)
              except (OSError, RuntimeError):
                  return False
              if under_package_install_root(resolved):
                  return False
              return any(resolved == base_path or base_path in resolved.parents for base_path in trusted_roots)

          def validate_trusted_module(key, module, baseline_names=None):
              spec = getattr(module, "__spec__", None)
              loader = getattr(module, "__loader__", None)
              module_name = getattr(module, "__name__", None)
              module_file = getattr(module, "__file__", None)
              if (
                  type(key) is not str
                  or spec is None
                  or spec.loader is not loader
                  or type(spec.name) is not str
                  or type(module_name) is not str
                  or not trusted_origin(spec.origin)
              ):
                  abort()
              if baseline_names is None:
                  if key != spec.name or spec.name != module_name:
                      abort()
              else:
                  expected_spec_name, expected_module_name = baseline_names
                  if spec.name is not expected_spec_name or module_name is not expected_module_name:
                      abort()
              if loader is BUILTIN_LOADER:
                  if spec.origin != "built-in" or module_file is not None:
                      abort()
                  return
              if loader is FROZEN_LOADER:
                  if spec.origin != "frozen":
                      abort()
                  if module_file is not None and (type(module_file) is not str or not trusted_origin(module_file)):
                      abort()
                  return
              if type(loader) is ZIP_IMPORTER:
                  if (
                      type(loader.archive) is not str
                      or type(loader.prefix) is not str
                      or type(spec.origin) is not str
                      or type(module_file) is not str
                      or spec.name != module_name
                      or spec.origin != module_file
                  ):
                      abort()
                  try:
                      exact_member = ZIP_GET_FILENAME(loader, spec.name)
                  except (ImportError, OSError, ValueError):
                      abort()
                  if type(exact_member) is not str:
                      abort()
                  archive = os.path.normcase(str(pathlib.Path(loader.archive).resolve(strict=False)))
                  prefix = loader.prefix.replace("/", os.sep).replace("\\", os.sep).strip(os.sep)
                  prefix_root = archive if not prefix else archive + os.sep + prefix
                  normalized_origin = os.path.normcase(os.path.normpath(spec.origin))
                  if archive not in trusted_archives or not (
                      normalized_origin == prefix_root or normalized_origin.startswith(prefix_root + os.sep)
                  ) or normalized_origin != os.path.normcase(os.path.normpath(exact_member)):
                      abort()
                  return
              backend_suffixes = next(
                  (suffixes for approved_type, suffixes in ALLOWED_BACKENDS if type(loader) is approved_type),
                  None,
              )
              if backend_suffixes is None:
                  abort()
              try:
                  loader_state = vars(loader)
              except TypeError:
                  abort()
              if (
                  type(loader_state) is not dict
                  or set(loader_state) != {"name", "path"}
                  or loader_state.get("name") is not loader.name
                  or loader_state.get("path") is not loader.path
                  or type(loader.name) is not str
                  or type(loader.path) is not str
                  or type(spec.origin) is not str
                  or type(module_file) is not str
                  or loader.name != spec.name
                  or spec.name != module_name
                  or os.path.normcase(os.path.normpath(loader.path)) != os.path.normcase(os.path.normpath(spec.origin))
                  or os.path.normcase(os.path.normpath(spec.origin)) != os.path.normcase(os.path.normpath(module_file))
                  or not any(loader.path.endswith(suffix) for suffix in backend_suffixes)
                  or not trusted_origin(loader.path)
              ):
                  abort()

          baseline_modules = []
          for name, module in tuple(sys.modules.items()):
              if type(name) is not str:
                  abort()
              if name.partition(".")[0] in finder.prefixes:
                  abort()
              spec = getattr(module, "__spec__", None)
              if spec is not None:
                  validate_trusted_module(name, module, (
                      getattr(spec, "name", None),
                      getattr(module, "__name__", None),
                  ))
              loader = getattr(module, "__loader__", None)
              module_path_state, spec_path_state = freeze_package_paths(module, spec)
              baseline_modules.append((
                  name,
                  module,
                  spec,
                  loader,
                  freeze_attributes(module, MODULE_IMPORT_ATTRIBUTES),
                  () if spec is None else freeze_attributes(spec, SPEC_IMPORT_ATTRIBUTES),
                  () if loader is None else freeze_attributes(loader, LOADER_IMPORT_ATTRIBUTES),
                  module_path_state,
                  spec_path_state,
              ))
          baseline_modules = tuple(baseline_modules)
          baseline_key_identities = {id(entry[0]): entry for entry in baseline_modules}
          if len(baseline_key_identities) != len(baseline_modules):
              abort()

          def verify_import_state():
              if (
                  sys.modules is not MODULES_CONTAINER or type(sys.modules) is not dict
                  or sys.path_importer_cache is not IMPORTER_CACHE_CONTAINER or type(sys.path_importer_cache) is not dict
                  or sys.path is not PATH_CONTAINER or type(sys.path) is not list
                  or sys.path_hooks is not PATH_HOOKS_CONTAINER or type(sys.path_hooks) is not list
                  or sys.meta_path is not META_PATH_CONTAINER or type(sys.meta_path) is not list
              ):
                  abort()
              verify_class_states(CORE_CLASS_STATES)
              verify_class_states(PROJECT_CLASS_STATES)
              if ExactLoader.get_code is not EXACT_LOADER_METHODS[0] or ExactLoader.exec_module is not EXACT_LOADER_METHODS[1]:
                  abort()
              try:
                  current_finder_state = vars(finder)
              except TypeError:
                  abort()
              if type(finder) is not ClosedFinder or type(current_finder_state) is not dict or current_finder_state:
                  abort()
              verify_exact_sequence(sys.path, closed_path, list)
              verify_exact_sequence(sys.path_hooks, closed_hooks, list)
              verify_exact_sequence(sys.meta_path, closed_meta, list)
              if sys.meta_path[0] is not finder:
                  abort()
              for item in closed_path:
                  PATH_FIND_SPEC(cache_probe, [item])
              if not set(closed_importer_cache).issubset(sys.path_importer_cache):
                  abort()
              for key, observed_importer in sys.path_importer_cache.items():
                  observed_fingerprint = importer_fingerprint(key, observed_importer)
                  if key in closed_importer_cache:
                      if observed_fingerprint != closed_importer_cache[key]:
                          abort()
                  elif observed_fingerprint == ("none",) or not trusted_origin(key):
                      abort()
              current_modules = tuple(sys.modules.items())
              current_by_key_identity = {}
              for name, module in current_modules:
                  if type(name) is not str or id(name) in current_by_key_identity:
                      abort()
                  current_by_key_identity[id(name)] = (name, module)
              for expected in baseline_modules:
                  (
                      expected_name, expected_module, expected_spec, expected_loader,
                      expected_module_attributes, expected_spec_attributes,
                      expected_loader_attributes, expected_module_path_state,
                      expected_spec_path_state,
                  ) = expected
                  observed = current_by_key_identity.get(id(expected_name))
                  if observed is None or observed[0] is not expected_name:
                      abort()
                  name, module = observed
                  if (
                      module is not expected_module
                      or getattr(module, "__spec__", None) is not expected_spec
                      or getattr(module, "__loader__", None) is not expected_loader
                  ):
                      abort()
                  verify_attributes(module, expected_module_attributes)
                  if expected_spec is not None:
                      verify_attributes(expected_spec, expected_spec_attributes)
                  if expected_loader is not None:
                      verify_attributes(expected_loader, expected_loader_attributes)
                  if expected_module_path_state is not None:
                      verify_string_list(module.__path__, expected_module_path_state)
                      verify_string_list(expected_spec.submodule_search_locations, expected_spec_path_state)
                  if expected_spec is not None:
                      validate_trusted_module(name, module, (
                          frozen_attribute(expected_spec_attributes, "name"),
                          frozen_attribute(expected_module_attributes, "__name__"),
                      ))
              observed_project_modules = {
                  name
                  for name in sys.modules
                  if type(name) is str and name.partition(".")[0] in finder.prefixes
              }
              if observed_project_modules != required_project_modules:
                  abort()
              if set(project_identities) != required_project_modules:
                  abort()
              project_by_key_identity = {}
              for project_key, project_identity in project_identities.items():
                  if project_key is not project_identity[0] or id(project_key) in project_by_key_identity:
                      abort()
                  project_by_key_identity[id(project_key)] = (project_key, project_identity)
              for name, module in current_modules:
                  if name.partition(".")[0] not in finder.prefixes:
                      baseline_entry = baseline_key_identities.get(id(name))
                      if baseline_entry is not None and name is baseline_entry[0]:
                          continue
                      else:
                          validate_trusted_module(name, module)
                      continue
                  if name not in modules:
                      abort()
                  raw_path, package, digest = modules[name]
                  expected = pathlib.Path(raw_path)
                  spec = getattr(module, "__spec__", None)
                  loader = getattr(module, "__loader__", None)
                  registry_entry = project_by_key_identity.get(id(name))
                  if registry_entry is None or registry_entry[0] is not name:
                      abort()
                  identity = registry_entry[1]
                  if (
                      identity is None
                      or identity[0] is not name
                      or identity[1] is not module
                      or identity[2] is not spec
                      or identity[3] is not loader
                      or spec is None
                      or type(loader) is not ExactLoader
                      or spec.loader is not loader
                      or type(spec.name) is not str
                      or type(module.__name__) is not str
                      or type(loader.name) is not str
                      or type(loader.path) is not str
                      or type(loader.digest) is not str
                      or spec.name != name
                      or module.__name__ != name
                      or loader.name != name
                      or loader.digest != digest
                      or loader.path is not raw_path
                      or loader.digest is not digest
                      or spec.origin is not loader.path
                      or module.__file__ is not loader.path
                      or spec.name is not loader.name
                      or module.__name__ is not loader.name
                  ):
                      abort()
                  verify_attributes(module, identity[4])
                  verify_attributes(spec, identity[5])
                  verify_attributes(loader, identity[6])
                  try:
                      loader_state = vars(loader)
                  except TypeError:
                      abort()
                  if (
                      type(loader_state) is not dict
                      or set(loader_state) != {"name", "path", "digest"}
                      or loader_state.get("name") is not loader.name
                      or loader_state.get("path") is not loader.path
                      or loader_state.get("digest") is not loader.digest
                      or type(spec.origin) is not str
                      or type(module.__file__) is not str
                  ):
                      abort()
                  if pathlib.Path(loader.path).resolve(strict=False) != expected:
                      abort()
                  if pathlib.Path(spec.origin).resolve(strict=False) != expected:
                      abort()
                  if pathlib.Path(module.__file__).resolve(strict=False) != expected:
                      abort()
                  if package:
                      if identity[7] is None or identity[8] is None:
                          abort()
                      verify_string_list(module.__path__, identity[7])
                      verify_string_list(spec.submodule_search_locations, identity[8])
                      raw_locations = identity[7][1]
                      raw_spec_locations = identity[8][1]
                      locations = tuple(pathlib.Path(item).resolve(strict=False) for item in raw_locations)
                      if locations != (expected.parent,):
                          abort()
                      spec_locations = tuple(pathlib.Path(item).resolve(strict=False) for item in raw_spec_locations)
                      if spec_locations != (expected.parent,):
                          abort()
                  elif spec.submodule_search_locations is not None or identity[7] is not None or identity[8] is not None:
                      abort()
                  capture(expected, digest)

          def discovered_test_ids(suite):
              identifiers = []
              pending = [suite]
              while pending:
                  item = pending.pop()
                  if isinstance(item, unittest.TestSuite):
                      pending.extend(reversed(tuple(item)))
                      continue
                  identifier = item.id()
                  if type(identifier) is not str:
                      abort()
                  identifiers.append(identifier)
              return tuple(identifiers)

          def run_suite(target, exact_count, exact_digest=None):
              try:
                  suite = unittest.defaultTestLoader.loadTestsFromName(target)
                  expected = suite.countTestCases()
                  if expected <= 0 or exact_count is not None and expected != exact_count:
                      abort()
                  identifiers = discovered_test_ids(suite)
                  if len(identifiers) != expected:
                      abort()
                  if exact_count == 1 and identifiers != (target,):
                      abort()
                  if exact_digest is not None:
                      encoded_ids = ("\n".join(identifiers) + "\n").encode("ascii")
                      if identifiers != tuple(sorted(identifiers)) or hashlib.sha256(encoded_ids).hexdigest() != exact_digest:
                          abort()
                  result = unittest.TextTestRunner(verbosity=2).run(suite)
              except BaseException:
                  abort()
              if not result.wasSuccessful() or result.testsRun != expected:
                  abort()
              if result.skipped or result.expectedFailures or result.unexpectedSuccesses:
                  abort()

          def execute_stage(
              _stage=stage,
              _root=root,
              _inventory=full_suite_inventory,
              _run_suite=run_suite,
              _verify_import_state=verify_import_state,
          ):
              if _stage == "native":
                  _run_suite("tests.test_governance_oracles.GovernanceOracleTests.test_windows_junction_component_is_rejected_without_skip", 1)
              elif _stage == "simulated":
                  _run_suite("tests.test_governance_oracles.GovernanceOracleTests.test_observed_windows_reparse_points_are_rejected_at_every_level", 1)
              elif _stage == "full":
                  _run_suite("tests.test_governance_oracles", _inventory[0], _inventory[1])
              elif _stage == "validator":
                  try:
                      from scripts.governance import validate_oracles
                      status = validate_oracles.main((str(_root),))
                  except BaseException:
                      abort()
                  if type(status) is not int or status != 0:
                      abort()
              else:
                  abort()
              _verify_import_state()
              return _stage

          completed_stage = execute_stage()
          evidence = "PYTHON_DOCTOR_ORACLE_STAGE_OK:" + nonce + ":" + completed_stage
          print(evidence, flush=True)
          sys.stdout.flush()
          sys.stderr.flush()
          os._exit(success_code)
          '''

          stages = (("native", 71), ("simulated", 72), ("full", 73), ("validator", 74))
          child_environment = {
              key: value
              for key, value in os.environ.items()
              if not key.upper().startswith("PYTHON")
              and key.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP"}
          }
          encoded = json.dumps(encoded_modules, sort_keys=True, separators=(",", ":"))
          for stage, success_code in stages:
              before = snapshot(watched_roots, task0_artifacts, checkout)
              nonce = secrets.token_hex(16)
              try:
                  process = subprocess.run(
                      [sys.executable, "-I", "-B", "-X", "utf8", "-S", "-", str(checkout), stage, nonce, str(success_code), encoded],
                      input=CHILD.encode("utf-8"),
                      cwd=str(checkout),
                      env=child_environment,
                      capture_output=True,
                      timeout=300,
                  )
              except subprocess.TimeoutExpired as error:
                  if error.stdout:
                      sys.stdout.buffer.write(error.stdout)
                      sys.stdout.buffer.flush()
                  if error.stderr:
                      sys.stderr.buffer.write(error.stderr)
                      sys.stderr.buffer.flush()
                  fail(94, "stage timeout")
              sys.stdout.buffer.write(process.stdout)
              sys.stdout.buffer.flush()
              sys.stderr.buffer.write(process.stderr)
              sys.stderr.buffer.flush()
              after = snapshot(watched_roots, task0_artifacts, checkout)
              evidence = ("PYTHON_DOCTOR_ORACLE_STAGE_OK:" + nonce + ":" + stage).encode("ascii")
              if before != after or process.returncode != success_code:
                  fail(94, "stage process failed")
              if process.stdout.splitlines().count(evidence) != 1:
                  fail(94, "stage evidence missing or duplicated")
          raise SystemExit(0)
          '@ | python -I -B -X utf8 -S - "$env:GITHUB_WORKSPACE"
          exit $LASTEXITCODE
```

Run the local zero-skip gate and commit these exact files before Task 1.

```bash
python -I -B -X utf8 -S - "$PWD" <<'PY'
import ast
import hashlib
import json
import os
import pathlib
import secrets
import stat
import subprocess
import sys

MAX_ENTRIES = 8192
MAX_DEPTH = 32
MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024

def fail(code, detail):
    print("oracle supervisor failure: " + detail, file=sys.stderr)
    raise SystemExit(code)

def is_reparse(metadata):
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(flag and attributes & flag)

def signature(metadata):
    return (
        metadata.st_dev,
        metadata.st_ino,
        stat.S_IFMT(metadata.st_mode),
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )

def within(candidate, parent):
    return candidate == parent or parent in candidate.parents

def checked_directory(path, root=None):
    absolute = pathlib.Path(os.path.abspath(str(path)))
    try:
        resolved = absolute.resolve(strict=True)
    except (OSError, RuntimeError):
        fail(90, "directory resolution")
    if os.path.normcase(str(absolute)) != os.path.normcase(str(resolved)):
        fail(90, "non-canonical directory")
    cursor = pathlib.Path(resolved.anchor)
    for component in resolved.parts[1:]:
        cursor = cursor / component
        metadata = cursor.lstat()
        if is_reparse(metadata) or not stat.S_ISDIR(metadata.st_mode):
            fail(90, "unsafe directory component")
    if root is not None and not within(resolved, root):
        fail(90, "directory escapes checkout")
    return resolved

def read_regular(path, root):
    try:
        resolved = path.resolve(strict=True)
        before = path.lstat()
        if resolved != path or not within(resolved, root):
            fail(91, "source escapes checkout")
        if is_reparse(before) or not stat.S_ISREG(before.st_mode):
            fail(91, "source is not regular")
        if before.st_size > MAX_FILE_BYTES:
            fail(91, "source exceeds cap")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        try:
            opened = os.fstat(descriptor)
            if signature(opened) != signature(before):
                fail(91, "source identity changed")
            chunks = bytearray()
            while len(chunks) <= MAX_FILE_BYTES:
                part = os.read(descriptor, min(65536, MAX_FILE_BYTES + 1 - len(chunks)))
                if not part:
                    break
                chunks.extend(part)
            after_fd = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        after_path = path.lstat()
    except OSError:
        fail(91, "source capture failed")
    if len(chunks) > MAX_FILE_BYTES:
        fail(91, "source exceeds cap")
    if signature(opened) != signature(after_fd) or signature(opened) != signature(after_path):
        fail(91, "source mutated")
    return bytes(chunks), signature(opened)

def snapshot(roots, files, checkout):
    records = {}
    total = 0
    count = 0
    for base in roots:
        pending = [(base, 0)]
        while pending:
            current, depth = pending.pop()
            if depth > MAX_DEPTH:
                fail(92, "snapshot depth exceeds cap")
            current = checked_directory(current, checkout)
            count += 1
            if count > MAX_ENTRIES:
                fail(92, "snapshot entry count exceeds cap")
            records["D:" + current.relative_to(checkout).as_posix()] = signature(current.lstat())
            try:
                with os.scandir(current) as iterator:
                    names = []
                    for entry in iterator:
                        count += 1
                        if count > MAX_ENTRIES:
                            fail(92, "snapshot entry count exceeds cap")
                        names.append(entry.name)
            except OSError:
                fail(92, "snapshot traversal failed")
            child_directories = []
            for name in sorted(names):
                path = current / name
                try:
                    metadata = path.lstat()
                except OSError:
                    fail(92, "snapshot entry inspection failed")
                if is_reparse(metadata):
                    fail(92, "snapshot entry is a link or reparse point")
                if stat.S_ISDIR(metadata.st_mode):
                    child_directories.append(path)
                    continue
                if not stat.S_ISREG(metadata.st_mode):
                    fail(92, "snapshot entry is not regular")
                raw, identity = read_regular(path, checkout)
                total += len(raw)
                if count > MAX_ENTRIES or total > MAX_TOTAL_BYTES:
                    fail(92, "snapshot exceeds cap")
                key = "F:" + path.relative_to(checkout).as_posix()
                records[key] = (identity, hashlib.sha256(raw).hexdigest())
            for child in reversed(child_directories):
                pending.append((child, depth + 1))
    for path in files:
        path = pathlib.Path(os.path.abspath(str(path)))
        raw, identity = read_regular(path, checkout)
        key = "F:" + path.relative_to(checkout).as_posix()
        record = (identity, hashlib.sha256(raw).hexdigest())
        if key in records:
            if records[key] != record:
                fail(92, "enumerated artifact disagrees with root snapshot")
            continue
        count += 1
        total += len(raw)
        if count > MAX_ENTRIES or total > MAX_TOTAL_BYTES:
            fail(92, "snapshot exceeds cap")
        records[key] = record
    return records

if len(sys.argv) != 2:
    fail(90, "arguments")
checkout = checked_directory(pathlib.Path(sys.argv[1]))
if pathlib.Path.cwd().resolve(strict=True) != checkout:
    fail(90, "working directory")
source = checked_directory(checkout / "src", checkout)
tests_root = checked_directory(checkout / "tests", checkout)
scripts_root = checked_directory(checkout / "scripts", checkout)
checked_directory(scripts_root / "governance", checkout)
doctor_root = checked_directory(source / "python_doctor", checkout)
watched_roots = (tests_root, scripts_root, doctor_root)

module_paths = {
    "tests": (tests_root / "__init__.py", True),
    "tests.test_governance_oracles": (tests_root / "test_governance_oracles.py", False),
    "scripts": (scripts_root / "__init__.py", True),
    "scripts.governance": (scripts_root / "governance" / "__init__.py", True),
    "scripts.governance.validate_oracles": (scripts_root / "governance" / "validate_oracles.py", False),
    "python_doctor": (doctor_root / "__init__.py", True),
}
task0_artifacts = tuple(
    checkout / relative
    for relative in (
        ".github/workflows/governance-oracles-windows.yml",
        "docs/audits/2026-07-14-governance-oracle-review.md",
        "scripts/__init__.py",
        "scripts/governance/__init__.py",
        "scripts/governance/validate_oracles.py",
        "tests/test_governance_oracles.py",
        "tests/fixtures/governance/expected-requirement-ids.txt",
        "tests/fixtures/governance/expected-skill-ids.txt",
        "tests/fixtures/governance/expected-profile-domain-ids.txt",
        "tests/fixtures/governance/expected-provenance-sources.toml",
        "tests/fixtures/governance/expected-gate-clauses.toml",
        "tests/fixtures/governance/expected-gate-checks.toml",
    )
)
if len(task0_artifacts) != 12 or len(set(task0_artifacts)) != 12:
    fail(92, "Task 0 artifact inventory")
encoded_modules = {}
for name, (path, package) in module_paths.items():
    raw, _identity = read_regular(path, checkout)
    encoded_modules[name] = (str(path), package, hashlib.sha256(raw).hexdigest())
test_raw, _test_identity = read_regular(module_paths["tests.test_governance_oracles"][0], checkout)
try:
    syntax = ast.parse(test_raw, filename="tests/test_governance_oracles.py")
except (SyntaxError, ValueError):
    fail(93, "test source syntax")
for node in ast.walk(syntax):
    if (
        isinstance(node, ast.Name) and node.id == "expectedFailure"
    ) or (
        isinstance(node, ast.Attribute) and node.attr == "expectedFailure"
    ):
        fail(93, "expectedFailure is forbidden")

CHILD = r'''
import hashlib
import importlib.abc
import importlib.machinery
import importlib.util
import json
import os
import pathlib
import site
import stat
import sys
import sysconfig
import unittest
import zipimport

MAX_SOURCE_BYTES = 4 * 1024 * 1024

def abort():
    os._exit(50)

def is_reparse(metadata):
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(flag and attributes & flag)

def signature(metadata):
    return (metadata.st_dev, metadata.st_ino, stat.S_IFMT(metadata.st_mode), metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns)

def capture(path, expected_digest):
    try:
        resolved = path.resolve(strict=True)
        before = path.lstat()
        if resolved != path or not (resolved == root or root in resolved.parents):
            abort()
        if is_reparse(before) or not stat.S_ISREG(before.st_mode) or before.st_size > MAX_SOURCE_BYTES:
            abort()
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            opened = os.fstat(descriptor)
            chunks = bytearray()
            while len(chunks) <= MAX_SOURCE_BYTES:
                part = os.read(descriptor, min(65536, MAX_SOURCE_BYTES + 1 - len(chunks)))
                if not part:
                    break
                chunks.extend(part)
            after_fd = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        after_path = path.lstat()
    except OSError:
        abort()
    if len(chunks) > MAX_SOURCE_BYTES:
        abort()
    raw = bytes(chunks)
    if signature(before) != signature(opened) or signature(opened) != signature(after_fd) or signature(opened) != signature(after_path):
        abort()
    if hashlib.sha256(raw).hexdigest() != expected_digest:
        abort()
    return raw

if len(sys.argv) != 6:
    abort()
root = pathlib.Path(sys.argv[1])
stage = sys.argv[2]
nonce = sys.argv[3]
success_code = int(sys.argv[4])
modules = json.loads(sys.argv[5])
required_project_modules_by_stage = {
    "native": frozenset(("tests", "tests.test_governance_oracles", "scripts", "scripts.governance", "scripts.governance.validate_oracles")),
    "simulated": frozenset(("tests", "tests.test_governance_oracles", "scripts", "scripts.governance", "scripts.governance.validate_oracles")),
    "full": frozenset(("tests", "tests.test_governance_oracles", "scripts", "scripts.governance", "scripts.governance.validate_oracles")),
    "validator": frozenset(("scripts", "scripts.governance", "scripts.governance.validate_oracles")),
}
required_project_modules = required_project_modules_by_stage.get(stage)
if required_project_modules is None:
    abort()
full_suite_inventory = {
    "posix": (52, "0dc6c93343d96463783a39c6ac91aab399a10411c496a923eb70a8b41f145078"),
    "nt": (49, "c5845af178802905e0c02a2ccdc79a188cf5cd42cfd8020fb5824907177f4adc"),
}.get(os.name)
if full_suite_inventory is None:
    abort()
MODULES_CONTAINER = sys.modules
IMPORTER_CACHE_CONTAINER = sys.path_importer_cache
PATH_CONTAINER = sys.path
PATH_HOOKS_CONTAINER = sys.path_hooks
META_PATH_CONTAINER = sys.meta_path
if (
    type(MODULES_CONTAINER) is not dict
    or type(IMPORTER_CACHE_CONTAINER) is not dict
    or type(PATH_CONTAINER) is not list
    or type(PATH_HOOKS_CONTAINER) is not list
    or type(META_PATH_CONTAINER) is not list
):
    abort()
stdlib = pathlib.Path(sysconfig.get_path("stdlib")).resolve(strict=True)
platstdlib = pathlib.Path(sysconfig.get_path("platstdlib")).resolve(strict=True)
base = pathlib.Path(sys.base_prefix).resolve(strict=True)
package_install_roots = set()
for scheme_key in ("purelib", "platlib"):
    scheme_path = sysconfig.get_path(scheme_key)
    if scheme_path:
        candidate = pathlib.Path(scheme_path).resolve(strict=False)
        if candidate not in (stdlib, platstdlib):
            package_install_roots.add(candidate)
user_sites = site.getusersitepackages()
if not user_sites:
    user_sites = ()
elif isinstance(user_sites, str):
    user_sites = (user_sites,)
for user_site in user_sites:
    package_install_roots.add(pathlib.Path(user_site).resolve(strict=False))

def under_package_install_root(candidate):
    lowered_parts = {part.lower() for part in candidate.parts}
    if "site-packages" in lowered_parts or "dist-packages" in lowered_parts:
        return True
    return any(
        candidate == package_root or package_root in candidate.parents
        for package_root in package_install_roots
    )

sanitized = []
for item in tuple(sys.path):
    if not item:
        continue
    candidate = pathlib.Path(item).resolve(strict=False)
    allowed = candidate in (stdlib, platstdlib)
    allowed = allowed or candidate.name in ("lib-dynload", "DLLs") and base in candidate.parents
    allowed = allowed or candidate.suffix == ".zip" and base in candidate.parents
    if allowed and not under_package_install_root(candidate):
        sanitized.append(str(candidate))
if not sanitized:
    abort()
sys.path[:] = sanitized
closed_path = tuple(sys.path)
closed_hooks = tuple(sys.path_hooks)
sys.path_importer_cache.clear()
cache_probe = "_python_doctor_closed_cache_probe_"
for item in closed_path:
    importlib.machinery.PathFinder.find_spec(cache_probe, [item])

BUILTIN_LOADER = importlib.machinery.BuiltinImporter
FROZEN_LOADER = importlib.machinery.FrozenImporter
FILE_FINDER = importlib.machinery.FileFinder
SOURCE_LOADER = importlib.machinery.SourceFileLoader
SOURCE_SUFFIXES = tuple(importlib.machinery.SOURCE_SUFFIXES)
BYTECODE_LOADER = importlib.machinery.SourcelessFileLoader
BYTECODE_SUFFIXES = tuple(importlib.machinery.BYTECODE_SUFFIXES)
EXTENSION_LOADER = importlib.machinery.ExtensionFileLoader
EXTENSION_SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
ZIP_IMPORTER = zipimport.zipimporter
ZIP_GET_FILENAME = ZIP_IMPORTER.get_filename
ALLOWED_BACKENDS = (
    (SOURCE_LOADER, SOURCE_SUFFIXES),
    (BYTECODE_LOADER, BYTECODE_SUFFIXES),
    (EXTENSION_LOADER, EXTENSION_SUFFIXES),
)
PATH_FINDER = importlib.machinery.PathFinder
SOURCE_EXEC_MODULE = SOURCE_LOADER.exec_module
SOURCE_TO_CODE = SOURCE_LOADER.source_to_code
PATH_FIND_SPEC = PATH_FINDER.find_spec

def freeze_class_state(owner):
    return owner, owner.__bases__, owner.__mro__, tuple(vars(owner).items())

def verify_class_states(states):
    for owner, expected_bases, expected_mro, expected in states:
        current = tuple(vars(owner).items())
        if (
            owner.__bases__ is not expected_bases
            or owner.__mro__ is not expected_mro
            or len(owner.__mro__) != len(expected_mro)
            or any(
                current_owner is not expected_owner
                for current_owner, expected_owner
                in zip(owner.__mro__, expected_mro)
            )
            or len(current) != len(expected)
            or any(
            current_name is not expected_name or current_value is not expected_value
            for (current_name, current_value), (expected_name, expected_value)
            in zip(current, expected)
            )
        ):
            abort()

core_class_owners = []
for root_class in (
    BUILTIN_LOADER,
    FROZEN_LOADER,
    PATH_FINDER,
    FILE_FINDER,
    SOURCE_LOADER,
    BYTECODE_LOADER,
    EXTENSION_LOADER,
    ZIP_IMPORTER,
    importlib.abc.MetaPathFinder,
):
    for owner in root_class.__mro__:
        if owner is not object and owner not in core_class_owners:
            core_class_owners.append(owner)
CORE_CLASS_STATES = tuple(freeze_class_state(owner) for owner in core_class_owners)
CALLABLE_CLASS_ATTRIBUTES = frozenset(
    name
    for _owner, _bases, _mro, state in CORE_CLASS_STATES
    for name, value in state
    if callable(value)
)

MISSING_ATTRIBUTE = object()
MODULE_IMPORT_ATTRIBUTES = (
    "__name__", "__loader__", "__package__", "__spec__",
    "__path__", "__file__", "__cached__",
)
SPEC_IMPORT_ATTRIBUTES = (
    "name", "loader", "origin", "submodule_search_locations",
    "cached", "has_location",
)
LOADER_IMPORT_ATTRIBUTES = ("name", "path", "archive", "prefix")

def read_attribute(subject, name):
    try:
        return True, getattr(subject, name)
    except AttributeError:
        return False, MISSING_ATTRIBUTE
    except BaseException:
        abort()

def freeze_attributes(subject, names):
    return tuple((name,) + read_attribute(subject, name) for name in names)

def verify_attributes(subject, expected):
    for name, expected_present, expected_value in expected:
        present, value = read_attribute(subject, name)
        if present is not expected_present or value is not expected_value:
            abort()

def frozen_attribute(expected, name):
    for attribute_name, present, value in expected:
        if attribute_name == name:
            return value if present else MISSING_ATTRIBUTE
    abort()

def freeze_string_list(value):
    if type(value) is not list or any(type(item) is not str for item in value):
        abort()
    return value, tuple(value)

def verify_string_list(value, expected):
    container, items = expected
    if value is not container or type(value) is not list or len(value) != len(items):
        abort()
    if any(observed is not frozen for observed, frozen in zip(value, items)):
        abort()

def freeze_package_paths(module, spec):
    path_present, module_path = read_attribute(module, "__path__")
    spec_path = None if spec is None else spec.submodule_search_locations
    if spec_path is None:
        if path_present:
            abort()
        return None, None
    if not path_present:
        abort()
    module_state = freeze_string_list(module_path)
    spec_state = freeze_string_list(spec_path)
    if (
        module_state[0] is not spec_state[0]
        or len(module_state[1]) != len(spec_state[1])
        or any(
            module_item is not spec_item
            for module_item, spec_item in zip(module_state[1], spec_state[1])
        )
    ):
        abort()
    return module_state, spec_state

def verify_exact_sequence(value, expected, expected_type):
    if type(value) is not expected_type or len(value) != len(expected):
        abort()
    if any(observed is not frozen for observed, frozen in zip(value, expected)):
        abort()

def importer_fingerprint(key, importer):
    if importer is None:
        return ("none",)
    if type(importer) is FILE_FINDER:
        if type(key) is not str or type(importer.path) is not str:
            abort()
        try:
            finder_state = vars(importer)
        except TypeError:
            abort()
        if (
            type(finder_state) is not dict
            or set(finder_state) != {"path", "_loaders", "_path_mtime", "_path_cache", "_relaxed_path_cache"}
            or finder_state.get("path") is not importer.path
            or finder_state.get("_loaders") is not importer._loaders
            or type(importer._loaders) is not list
            or type(finder_state.get("_path_cache")) is not set
            or type(finder_state.get("_relaxed_path_cache")) is not set
        ):
            abort()
        if any(name in CALLABLE_CLASS_ATTRIBUTES for name in finder_state):
            abort()
        if pathlib.Path(importer.path).resolve(strict=False) != pathlib.Path(key).resolve(strict=False):
            abort()
        if any(
            type(suffix) is not str
            or not any(
                factory is approved_factory and suffix in approved_suffixes
                for approved_factory, approved_suffixes in ALLOWED_BACKENDS
            )
            for suffix, factory in importer._loaders
        ):
            abort()
        return ("file", importer.path, tuple(importer._loaders))
    if type(importer) is ZIP_IMPORTER:
        if type(key) is not str or type(importer.archive) is not str or type(importer.prefix) is not str:
            abort()
        try:
            zip_state = vars(importer)
        except TypeError:
            abort()
        if (
            type(zip_state) is not dict
            or set(zip_state) != {"_files", "archive", "prefix"}
            or type(zip_state.get("_files")) is not dict
            or zip_state.get("archive") is not importer.archive
            or zip_state.get("prefix") is not importer.prefix
            or any(name in CALLABLE_CLASS_ATTRIBUTES for name in zip_state)
        ):
            abort()
        archive = pathlib.Path(importer.archive).resolve(strict=False)
        prefix = importer.prefix.replace("/", os.sep).replace("\\", os.sep).strip(os.sep)
        expected_key = archive if not prefix else pathlib.Path(str(archive) + os.sep + prefix)
        if pathlib.Path(key).resolve(strict=False) != expected_key.resolve(strict=False):
            abort()
        return ("zip", str(archive), prefix)
    abort()

if set(sys.path_importer_cache) != set(closed_path):
    abort()
closed_importer_cache = {
    key: importer_fingerprint(key, importer)
    for key, importer in sys.path_importer_cache.items()
}
project_identities = {}

class ExactLoader(SOURCE_LOADER):
    def __init__(self, fullname, path, digest):
        super().__init__(fullname, path)
        self.digest = digest

    def get_code(self, fullname):
        raw = capture(pathlib.Path(self.path), self.digest)
        return SOURCE_TO_CODE(self, raw, self.path)

    def exec_module(self, module):
        spec = getattr(module, "__spec__", None)
        if self.name in project_identities or spec is None or spec.loader is not self:
            abort()
        matching_keys = tuple(
            key
            for key, value in sys.modules.items()
            if type(key) is str and key == self.name and value is module
        )
        if len(matching_keys) != 1:
            abort()
        project_key = matching_keys[0]
        module_attributes = freeze_attributes(module, MODULE_IMPORT_ATTRIBUTES)
        spec_attributes = freeze_attributes(spec, SPEC_IMPORT_ATTRIBUTES)
        loader_attributes = freeze_attributes(self, LOADER_IMPORT_ATTRIBUTES + ("digest",))
        module_path_state, spec_path_state = freeze_package_paths(module, spec)
        project_identities[project_key] = (
            project_key, module, spec, self,
            module_attributes, spec_attributes, loader_attributes,
            module_path_state, spec_path_state,
        )
        SOURCE_EXEC_MODULE(self, module)
        identity = project_identities.get(project_key)
        if (
            identity is None
            or identity[0] not in sys.modules
            or sys.modules[identity[0]] is not module
            or getattr(module, "__spec__", None) is not spec
            or spec.loader is not self
        ):
            abort()
        verify_attributes(module, module_attributes)
        verify_attributes(spec, spec_attributes)
        verify_attributes(self, loader_attributes)
        if module_path_state is not None:
            verify_string_list(module.__path__, module_path_state)
            verify_string_list(spec.submodule_search_locations, spec_path_state)

EXACT_LOADER_METHODS = (ExactLoader.get_code, ExactLoader.exec_module)

class ClosedFinder(importlib.abc.MetaPathFinder):
    prefixes = ("tests", "scripts", "python_doctor")

    def find_spec(self, fullname, path=None, target=None):
        if fullname.partition(".")[0] not in self.prefixes:
            return None
        if fullname not in modules:
            raise ModuleNotFoundError("allowlisted module miss")
        raw_path, package, digest = modules[fullname]
        if type(raw_path) is not str or type(package) is not bool or type(digest) is not str:
            abort()
        source_path = pathlib.Path(raw_path)
        expected_parent = source_path.parent
        if path is None:
            if "." in fullname:
                raise ModuleNotFoundError("missing package path")
        else:
            parent_name = fullname.rpartition(".")[0]
            if parent_name not in modules:
                raise ModuleNotFoundError("unreviewed parent package")
            parent_identity = project_identities.get(parent_name)
            if parent_identity is None or parent_identity[7] is None:
                raise ModuleNotFoundError("unregistered parent package")
            verify_string_list(path, parent_identity[7])
            parent_source = pathlib.Path(modules[parent_name][0])
            supplied = tuple(pathlib.Path(item).resolve(strict=False) for item in path)
            if supplied != (parent_source.parent,):
                raise ModuleNotFoundError("redirected package path")
        capture(source_path, digest)
        loader = ExactLoader(fullname, raw_path, digest)
        spec = importlib.util.spec_from_loader(fullname, loader, is_package=package)
        if spec is None or pathlib.Path(spec.origin).resolve(strict=False) != source_path:
            abort()
        if package and tuple(pathlib.Path(item).resolve(strict=False) for item in spec.submodule_search_locations or ()) != (expected_parent,):
            abort()
        return spec

PROJECT_CLASS_STATES = tuple(
    freeze_class_state(owner) for owner in (ExactLoader, ClosedFinder)
)

finder = ClosedFinder()
try:
    finder_state = vars(finder)
except TypeError:
    abort()
if type(finder) is not ClosedFinder or type(finder_state) is not dict or finder_state:
    abort()
sys.meta_path.insert(0, finder)
closed_meta = tuple(sys.meta_path)
trusted_roots = tuple(
    pathlib.Path(item).resolve(strict=False)
    for item in closed_path
    if pathlib.Path(item).suffix != ".zip"
)
trusted_archives = tuple(
    os.path.normcase(str(pathlib.Path(item).resolve(strict=False)))
    for item in closed_path
    if pathlib.Path(item).suffix == ".zip"
)

def trusted_origin(origin):
    if type(origin) is not str:
        return False
    if origin == "built-in" or origin == "frozen":
        return True
    normalized = os.path.normcase(origin)
    if any(
        normalized == archive or normalized.startswith(archive + os.sep)
        for archive in trusted_archives
    ):
        return True
    try:
        resolved = pathlib.Path(origin).resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    if under_package_install_root(resolved):
        return False
    return any(resolved == base_path or base_path in resolved.parents for base_path in trusted_roots)

def validate_trusted_module(key, module, baseline_names=None):
    spec = getattr(module, "__spec__", None)
    loader = getattr(module, "__loader__", None)
    module_name = getattr(module, "__name__", None)
    module_file = getattr(module, "__file__", None)
    if (
        type(key) is not str
        or spec is None
        or spec.loader is not loader
        or type(spec.name) is not str
        or type(module_name) is not str
        or not trusted_origin(spec.origin)
    ):
        abort()
    if baseline_names is None:
        if key != spec.name or spec.name != module_name:
            abort()
    else:
        expected_spec_name, expected_module_name = baseline_names
        if spec.name is not expected_spec_name or module_name is not expected_module_name:
            abort()
    if loader is BUILTIN_LOADER:
        if spec.origin != "built-in" or module_file is not None:
            abort()
        return
    if loader is FROZEN_LOADER:
        if spec.origin != "frozen":
            abort()
        if module_file is not None and (type(module_file) is not str or not trusted_origin(module_file)):
            abort()
        return
    if type(loader) is ZIP_IMPORTER:
        if (
            type(loader.archive) is not str
            or type(loader.prefix) is not str
            or type(spec.origin) is not str
            or type(module_file) is not str
            or spec.name != module_name
            or spec.origin != module_file
        ):
            abort()
        try:
            exact_member = ZIP_GET_FILENAME(loader, spec.name)
        except (ImportError, OSError, ValueError):
            abort()
        if type(exact_member) is not str:
            abort()
        archive = os.path.normcase(str(pathlib.Path(loader.archive).resolve(strict=False)))
        prefix = loader.prefix.replace("/", os.sep).replace("\\", os.sep).strip(os.sep)
        prefix_root = archive if not prefix else archive + os.sep + prefix
        normalized_origin = os.path.normcase(os.path.normpath(spec.origin))
        if archive not in trusted_archives or not (
            normalized_origin == prefix_root or normalized_origin.startswith(prefix_root + os.sep)
        ) or normalized_origin != os.path.normcase(os.path.normpath(exact_member)):
            abort()
        return
    backend_suffixes = next(
        (suffixes for approved_type, suffixes in ALLOWED_BACKENDS if type(loader) is approved_type),
        None,
    )
    if backend_suffixes is None:
        abort()
    try:
        loader_state = vars(loader)
    except TypeError:
        abort()
    if (
        type(loader_state) is not dict
        or set(loader_state) != {"name", "path"}
        or loader_state.get("name") is not loader.name
        or loader_state.get("path") is not loader.path
        or type(loader.name) is not str
        or type(loader.path) is not str
        or type(spec.origin) is not str
        or type(module_file) is not str
        or loader.name != spec.name
        or spec.name != module_name
        or os.path.normcase(os.path.normpath(loader.path)) != os.path.normcase(os.path.normpath(spec.origin))
        or os.path.normcase(os.path.normpath(spec.origin)) != os.path.normcase(os.path.normpath(module_file))
        or not any(loader.path.endswith(suffix) for suffix in backend_suffixes)
        or not trusted_origin(loader.path)
    ):
        abort()

baseline_modules = []
for name, module in tuple(sys.modules.items()):
    if type(name) is not str:
        abort()
    if name.partition(".")[0] in finder.prefixes:
        abort()
    spec = getattr(module, "__spec__", None)
    if spec is not None:
        validate_trusted_module(name, module, (
            getattr(spec, "name", None),
            getattr(module, "__name__", None),
        ))
    loader = getattr(module, "__loader__", None)
    module_path_state, spec_path_state = freeze_package_paths(module, spec)
    baseline_modules.append((
        name,
        module,
        spec,
        loader,
        freeze_attributes(module, MODULE_IMPORT_ATTRIBUTES),
        () if spec is None else freeze_attributes(spec, SPEC_IMPORT_ATTRIBUTES),
        () if loader is None else freeze_attributes(loader, LOADER_IMPORT_ATTRIBUTES),
        module_path_state,
        spec_path_state,
    ))
baseline_modules = tuple(baseline_modules)
baseline_key_identities = {id(entry[0]): entry for entry in baseline_modules}
if len(baseline_key_identities) != len(baseline_modules):
    abort()

def verify_import_state():
    if (
        sys.modules is not MODULES_CONTAINER or type(sys.modules) is not dict
        or sys.path_importer_cache is not IMPORTER_CACHE_CONTAINER or type(sys.path_importer_cache) is not dict
        or sys.path is not PATH_CONTAINER or type(sys.path) is not list
        or sys.path_hooks is not PATH_HOOKS_CONTAINER or type(sys.path_hooks) is not list
        or sys.meta_path is not META_PATH_CONTAINER or type(sys.meta_path) is not list
    ):
        abort()
    verify_class_states(CORE_CLASS_STATES)
    verify_class_states(PROJECT_CLASS_STATES)
    if ExactLoader.get_code is not EXACT_LOADER_METHODS[0] or ExactLoader.exec_module is not EXACT_LOADER_METHODS[1]:
        abort()
    try:
        current_finder_state = vars(finder)
    except TypeError:
        abort()
    if type(finder) is not ClosedFinder or type(current_finder_state) is not dict or current_finder_state:
        abort()
    verify_exact_sequence(sys.path, closed_path, list)
    verify_exact_sequence(sys.path_hooks, closed_hooks, list)
    verify_exact_sequence(sys.meta_path, closed_meta, list)
    if sys.meta_path[0] is not finder:
        abort()
    for item in closed_path:
        PATH_FIND_SPEC(cache_probe, [item])
    if not set(closed_importer_cache).issubset(sys.path_importer_cache):
        abort()
    for key, observed_importer in sys.path_importer_cache.items():
        observed_fingerprint = importer_fingerprint(key, observed_importer)
        if key in closed_importer_cache:
            if observed_fingerprint != closed_importer_cache[key]:
                abort()
        elif observed_fingerprint == ("none",) or not trusted_origin(key):
            abort()
    current_modules = tuple(sys.modules.items())
    current_by_key_identity = {}
    for name, module in current_modules:
        if type(name) is not str or id(name) in current_by_key_identity:
            abort()
        current_by_key_identity[id(name)] = (name, module)
    for expected in baseline_modules:
        (
            expected_name, expected_module, expected_spec, expected_loader,
            expected_module_attributes, expected_spec_attributes,
            expected_loader_attributes, expected_module_path_state,
            expected_spec_path_state,
        ) = expected
        observed = current_by_key_identity.get(id(expected_name))
        if observed is None or observed[0] is not expected_name:
            abort()
        name, module = observed
        if (
            module is not expected_module
            or getattr(module, "__spec__", None) is not expected_spec
            or getattr(module, "__loader__", None) is not expected_loader
        ):
            abort()
        verify_attributes(module, expected_module_attributes)
        if expected_spec is not None:
            verify_attributes(expected_spec, expected_spec_attributes)
        if expected_loader is not None:
            verify_attributes(expected_loader, expected_loader_attributes)
        if expected_module_path_state is not None:
            verify_string_list(module.__path__, expected_module_path_state)
            verify_string_list(expected_spec.submodule_search_locations, expected_spec_path_state)
        if expected_spec is not None:
            validate_trusted_module(name, module, (
                frozen_attribute(expected_spec_attributes, "name"),
                frozen_attribute(expected_module_attributes, "__name__"),
            ))
    observed_project_modules = {
        name
        for name in sys.modules
        if type(name) is str and name.partition(".")[0] in finder.prefixes
    }
    if observed_project_modules != required_project_modules:
        abort()
    if set(project_identities) != required_project_modules:
        abort()
    project_by_key_identity = {}
    for project_key, project_identity in project_identities.items():
        if project_key is not project_identity[0] or id(project_key) in project_by_key_identity:
            abort()
        project_by_key_identity[id(project_key)] = (project_key, project_identity)
    for name, module in current_modules:
        if name.partition(".")[0] not in finder.prefixes:
            baseline_entry = baseline_key_identities.get(id(name))
            if baseline_entry is not None and name is baseline_entry[0]:
                continue
            else:
                validate_trusted_module(name, module)
            continue
        if name not in modules:
            abort()
        raw_path, package, digest = modules[name]
        expected = pathlib.Path(raw_path)
        spec = getattr(module, "__spec__", None)
        loader = getattr(module, "__loader__", None)
        registry_entry = project_by_key_identity.get(id(name))
        if registry_entry is None or registry_entry[0] is not name:
            abort()
        identity = registry_entry[1]
        if (
            identity is None
            or identity[0] is not name
            or identity[1] is not module
            or identity[2] is not spec
            or identity[3] is not loader
            or spec is None
            or type(loader) is not ExactLoader
            or spec.loader is not loader
            or type(spec.name) is not str
            or type(module.__name__) is not str
            or type(loader.name) is not str
            or type(loader.path) is not str
            or type(loader.digest) is not str
            or spec.name != name
            or module.__name__ != name
            or loader.name != name
            or loader.digest != digest
            or loader.path is not raw_path
            or loader.digest is not digest
            or spec.origin is not loader.path
            or module.__file__ is not loader.path
            or spec.name is not loader.name
            or module.__name__ is not loader.name
        ):
            abort()
        verify_attributes(module, identity[4])
        verify_attributes(spec, identity[5])
        verify_attributes(loader, identity[6])
        try:
            loader_state = vars(loader)
        except TypeError:
            abort()
        if (
            type(loader_state) is not dict
            or set(loader_state) != {"name", "path", "digest"}
            or loader_state.get("name") is not loader.name
            or loader_state.get("path") is not loader.path
            or loader_state.get("digest") is not loader.digest
            or type(spec.origin) is not str
            or type(module.__file__) is not str
        ):
            abort()
        if pathlib.Path(loader.path).resolve(strict=False) != expected:
            abort()
        if pathlib.Path(spec.origin).resolve(strict=False) != expected:
            abort()
        if pathlib.Path(module.__file__).resolve(strict=False) != expected:
            abort()
        if package:
            if identity[7] is None or identity[8] is None:
                abort()
            verify_string_list(module.__path__, identity[7])
            verify_string_list(spec.submodule_search_locations, identity[8])
            raw_locations = identity[7][1]
            raw_spec_locations = identity[8][1]
            locations = tuple(pathlib.Path(item).resolve(strict=False) for item in raw_locations)
            if locations != (expected.parent,):
                abort()
            spec_locations = tuple(pathlib.Path(item).resolve(strict=False) for item in raw_spec_locations)
            if spec_locations != (expected.parent,):
                abort()
        elif spec.submodule_search_locations is not None or identity[7] is not None or identity[8] is not None:
            abort()
        capture(expected, digest)

def discovered_test_ids(suite):
    identifiers = []
    pending = [suite]
    while pending:
        item = pending.pop()
        if isinstance(item, unittest.TestSuite):
            pending.extend(reversed(tuple(item)))
            continue
        identifier = item.id()
        if type(identifier) is not str:
            abort()
        identifiers.append(identifier)
    return tuple(identifiers)

def run_suite(target, exact_count, exact_digest=None):
    try:
        suite = unittest.defaultTestLoader.loadTestsFromName(target)
        expected = suite.countTestCases()
        if expected <= 0 or exact_count is not None and expected != exact_count:
            abort()
        identifiers = discovered_test_ids(suite)
        if len(identifiers) != expected:
            abort()
        if exact_count == 1 and identifiers != (target,):
            abort()
        if exact_digest is not None:
            encoded_ids = ("\n".join(identifiers) + "\n").encode("ascii")
            if identifiers != tuple(sorted(identifiers)) or hashlib.sha256(encoded_ids).hexdigest() != exact_digest:
                abort()
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    except BaseException:
        abort()
    if not result.wasSuccessful() or result.testsRun != expected:
        abort()
    if result.skipped or result.expectedFailures or result.unexpectedSuccesses:
        abort()

def execute_stage(
    _stage=stage,
    _root=root,
    _inventory=full_suite_inventory,
    _run_suite=run_suite,
    _verify_import_state=verify_import_state,
):
    if _stage == "native":
        _run_suite("tests.test_governance_oracles.GovernanceOracleTests.test_windows_junction_component_is_rejected_without_skip", 1)
    elif _stage == "simulated":
        _run_suite("tests.test_governance_oracles.GovernanceOracleTests.test_observed_windows_reparse_points_are_rejected_at_every_level", 1)
    elif _stage == "full":
        _run_suite("tests.test_governance_oracles", _inventory[0], _inventory[1])
    elif _stage == "validator":
        try:
            from scripts.governance import validate_oracles
            status = validate_oracles.main((str(_root),))
        except BaseException:
            abort()
        if type(status) is not int or status != 0:
            abort()
    else:
        abort()
    _verify_import_state()
    return _stage

completed_stage = execute_stage()
evidence = "PYTHON_DOCTOR_ORACLE_STAGE_OK:" + nonce + ":" + completed_stage
print(evidence, flush=True)
sys.stdout.flush()
sys.stderr.flush()
os._exit(success_code)
'''

stages = (("simulated", 72), ("full", 73), ("validator", 74))
if os.name == "nt":
    stages = (("native", 71),) + stages
child_environment = {
    key: value
    for key, value in os.environ.items()
    if not key.upper().startswith("PYTHON")
    and key.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP"}
}
encoded = json.dumps(encoded_modules, sort_keys=True, separators=(",", ":"))
for stage, success_code in stages:
    before = snapshot(watched_roots, task0_artifacts, checkout)
    nonce = secrets.token_hex(16)
    try:
        process = subprocess.run(
            [sys.executable, "-I", "-B", "-X", "utf8", "-S", "-", str(checkout), stage, nonce, str(success_code), encoded],
            input=CHILD.encode("utf-8"),
            cwd=str(checkout),
            env=child_environment,
            capture_output=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired as error:
        if error.stdout:
            sys.stdout.buffer.write(error.stdout)
            sys.stdout.buffer.flush()
        if error.stderr:
            sys.stderr.buffer.write(error.stderr)
            sys.stderr.buffer.flush()
        fail(94, "stage timeout")
    sys.stdout.buffer.write(process.stdout)
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(process.stderr)
    sys.stderr.buffer.flush()
    after = snapshot(watched_roots, task0_artifacts, checkout)
    evidence = ("PYTHON_DOCTOR_ORACLE_STAGE_OK:" + nonce + ":" + stage).encode("ascii")
    if before != after or process.returncode != success_code:
        fail(94, "stage process failed")
    if process.stdout.splitlines().count(evidence) != 1:
        fail(94, "stage evidence missing or duplicated")
raise SystemExit(0)

PY
python -I -B -X utf8 -S -m compileall -q scripts tests
git add .github/workflows/governance-oracles-windows.yml scripts/__init__.py scripts/governance/__init__.py scripts/governance/validate_oracles.py tests/test_governance_oracles.py tests/fixtures/governance/expected-requirement-ids.txt tests/fixtures/governance/expected-skill-ids.txt tests/fixtures/governance/expected-profile-domain-ids.txt tests/fixtures/governance/expected-provenance-sources.toml tests/fixtures/governance/expected-gate-clauses.toml tests/fixtures/governance/expected-gate-checks.toml docs/audits/2026-07-14-governance-oracle-review.md
git diff --cached --name-only
git commit -m "docs(governance): freeze independent oracle inventories"
```

- [ ] **Step 4: Enforce role and diff separation**

Tasks 1–10 consume but may not edit oracle files. Any required oracle change
returns to an independent specification task, produces its own commit/review,
and invalidates downstream evidence. A manifest implementer and command
implementer may not approve their corresponding oracle.

---

### Task 1: Strict governance models and loader

**Classification:** `behavior_change`

**Requirements:** `QA-01`, `QA-02`, `REL-01`

**Files:**

- Consume: `scripts/__init__.py`
- Create: `scripts/gates/__init__.py`
- Create: `scripts/gates/models.py`
- Create: `scripts/gates/loader.py`
- Create: `scripts/gates/validation.py`
- Create: `tests/governance_helpers.py`
- Test: `tests/test_gate_manifest.py`

**Interfaces:**

- Produces: every model in **Stable interfaces**, including
  `PublishedAnchorBinding` and `PhaseContract`; `Violation`;
  `load_governance()`; `validate_governance()`;
  `load_requirements(path: Path) -> tuple[RequirementSpec, ...]`;
  `load_clause_registry(path: Path) -> ClauseRegistry`;
  `load_phase_contract(path: Path, *, expected_stage:
  Literal["bootstrap", "anchor-bound"]) -> PhaseContract`; and
  `bootstrap_projection(contract: PhaseContract) -> tuple[str, str, str, str,
  str]`. Task 1 unit tests use temporary synthetic v1/v2 files so both closed
  stage parsers exist before Task 2 populates the repository's v2 contract.
- Consumes: only Python standard library and the existing `tomli` compatibility
  dependency.

- [ ] **Step 1: Write the manifest RED tests**

```python
class GateManifestTests(unittest.TestCase):
    def test_rejects_shell_string_command(self) -> None:
        bundle = minimal_bundle(command="python -m unittest")
        violations = validate_governance(bundle, active_phase=1)
        self.assertIn("command must be an argv array", messages(violations))

    def test_rejects_dangling_requirement(self) -> None:
        bundle = minimal_bundle(requirement_ids=("PRIV-999",))
        violations = validate_governance(bundle, active_phase=1)
        self.assertIn("unknown requirement PRIV-999", messages(violations))

    def test_accepts_future_planned_work(self) -> None:
        bundle = minimal_bundle(
            scheduled_phase=8,
            schedule_state=DeliveryState.PLANNED,
        )
        violations = validate_governance(bundle, active_phase=1)
        self.assertNotIn("future work must remain PLANNED", messages(violations))

    def test_rejects_deferred_work_disguised_as_not_applicable(self) -> None:
        bundle = minimal_bundle(
            scheduled_phase=8,
            schedule_state=DeliveryState.PLANNED,
            applicability_predicate=predicate("always"),
            fabricated_result=GateState.NOT_APPLICABLE,
        )
        self.assertIn(
            "future work must remain PLANNED",
            messages(validate_governance(bundle, active_phase=1)),
        )
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_gate_manifest -v`

Expected: import failure for `scripts.gates`.

- [ ] **Step 3: Implement the stable interfaces exactly**

```python
class GateState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class Violation:
    path: str
    code: str
    message: str
```

Implement every model and public signature in **Stable interfaces**. Test
helpers `minimal_bundle()`, `messages()`, and `temporary_manifest_tree()` live
only in `tests/governance_helpers.py`. Strict TOML checks enforce closed field
sets, ID regexes, duplicate and dangling references, deterministic violation
ordering, root-contained relative paths, argv arrays, and a closed predicate
registry. The registry contains `always`, `host_os`, `python_version`,
`artifact_kind`, `destination_authorized`, and
`external_prerequisite_present`; `never` is accepted only in a RED fixture and
must be rejected. No manifest text is evaluated as Python, shell, regex
program, or arbitrary boolean expression.

Validation also rejects requirement dependency cycles, dependencies scheduled
after their dependent's required phase, non-bidirectional requirement/check
edges, unresolved clause IDs, and authored status claims. Requirement state is
computed for one candidate: every dependency must be verified for that same
candidate (or validly N/A), every completion predicate and mandatory check must
pass, required review must bind that candidate, and no required future
verification phase may remain. Phase 1 product requirements derive
`IN_PROGRESS`, never `IMPLEMENTED_UNVERIFIED` or `VERIFIED`.

- [ ] **Step 4: Verify GREEN**

Run: `PYTHONPATH=src:. python -m unittest tests.test_gate_manifest -v`

Expected: all tests pass.

- [ ] **Step 5: Run regression suite**

Run: `PYTHONPATH=src:. python -m unittest discover -s tests`

Expected: every discovered test passes; zero errors, failures, or skips. Final
collection equality is frozen by the Phase 1 gate-child inventory rather than a
fragile numeric count.

- [ ] **Step 6: Commit**

```bash
git add scripts/gates/__init__.py scripts/gates/models.py scripts/gates/loader.py scripts/gates/validation.py tests/governance_helpers.py tests/test_gate_manifest.py
git diff --cached --name-only
git commit -m "feat(governance): add strict manifest contracts"
```

---

### Task 2: Requirements traceability manifest

**Classification:** `verification_content`

**Requirements:** every stable family in the approved traceability design.

**Files:**

- Create: `governance/requirements.toml`
- Create: `governance/clause-registry.toml`
- Create: `governance/toolchain.lock.toml`
- Create: `governance/validation-inputs.toml`
- Create: `tests/test_requirements_manifest.py`
- Consume without editing: `tests/fixtures/governance/expected-gate-clauses.toml`
- Consume without editing: `tests/fixtures/governance/expected-requirement-ids.txt`
- Modify without changing the Task -1 base binding:
  `docs/evidence/contracts/phase-01-governance.toml`
- Modify: `tests/governance_helpers.py` with pure local Git-history validation;
  it has no GitHub client, checkpoint constructor, or external-evidence parser.

**Interfaces:**

- Consumes: `load_governance()`, `validate_governance()`, and four inert values
  exported by the current live `PublishedAnchorCheckpoint`: published anchor
  commit/tree plus projection/review-transcript SHA-256.
- Produces: canonical `RequirementSpec` records referenced by every task/gate.
- Uses the Task 1 phase-contract types/loaders. Bootstrap mode accepts only the
  five-key v1 document; anchor-bound mode accepts only the v2 root/table shape
  below.
- Adds test-only `unique_addition_commit(path: str) -> str`,
  `load_phase_contract_from_git(commit: str, path: str) -> PhaseContract`,
  `commit_parent(commit: str) -> str`, `git_tree(commit: str) -> str`, and
  `is_ancestor(ancestor: str, descendant: str) -> bool` in
  `tests/governance_helpers.py`; every Git call uses fixed argv, disables
  hooks/config/external diff, and rejects ambiguous or multi-parent results.

- [ ] **Step 1: Write the failing completeness validator**

```python
import unittest

from scripts.gates.loader import (
    bootstrap_projection,
    load_clause_registry,
    load_phase_contract,
    load_requirements,
)
from tests.governance_helpers import (
    ROOT,
    commit_parent,
    git_tree,
    is_ancestor,
    load_phase_contract_from_git,
    unique_addition_commit,
)


class TestRequirementsManifest(unittest.TestCase):
    def test_manifest_matches_independently_frozen_id_set(self) -> None:
        requirements = load_requirements(ROOT / "governance/requirements.toml")
        lines = (ROOT / "tests/fixtures/governance/expected-requirement-ids.txt").read_text(
            encoding="utf-8"
        ).splitlines()
        self.assertEqual(len(lines), 105)
        self.assertEqual(len(lines), len(set(lines)))
        self.assertTrue(all(line and not line.startswith("#") for line in lines))
        self.assertEqual(
            {item.requirement_id for item in requirements}, frozenset(lines)
        )

    def test_requirement_state_is_derived_not_authored(self) -> None:
        requirements = load_requirements(ROOT / "governance/requirements.toml")
        self.assertTrue(all(not hasattr(item, "release_status") for item in requirements))
        self.assertTrue(
            all(not hasattr(item, "current_phase_status") for item in requirements)
        )

    def test_every_source_clause_resolves_to_frozen_digest(self) -> None:
        requirements = load_requirements(ROOT / "governance/requirements.toml")
        registry = load_clause_registry(ROOT / "governance/clause-registry.toml")
        self.assertTrue(
            all(
                registry.resolves(clause)
                for item in requirements
                for clause in item.source_clauses
            )
        )

    def test_task_minus_one_base_binding_is_immutable(self) -> None:
        contract = load_phase_contract(
            ROOT / "docs/evidence/contracts/phase-01-governance.toml",
            expected_stage="anchor-bound",
        )
        introduction = unique_addition_commit(
            "docs/evidence/contracts/phase-01-governance.toml"
        )
        original = load_phase_contract_from_git(
            introduction, "docs/evidence/contracts/phase-01-governance.toml"
        )
        self.assertEqual(
            bootstrap_projection(contract), bootstrap_projection(original)
        )
        self.assertEqual(commit_parent(introduction), contract.governance_base_commit)
        self.assertEqual(
            git_tree(contract.governance_base_commit), contract.governance_base_tree
        )
        self.assertIsNotNone(contract.published_anchor)
        anchor = contract.published_anchor
        assert anchor is not None
        self.assertTrue(is_ancestor(introduction, anchor.commit))
        self.assertTrue(is_ancestor(anchor.commit, "HEAD"))
        self.assertEqual(
            git_tree(anchor.commit), anchor.tree
        )
        self.assertRegex(anchor.projection_sha256, r"^[0-9a-f]{64}$")
        self.assertRegex(anchor.reviews_sha256, r"^[0-9a-f]{64}$")
```

The live `PublishedAnchorCheckpoint` remains a session orchestration
precondition and is never synthesized in repository tests. Task 2 migrates the
bootstrap contract to this exact closed schema:

```toml
schema_version = "phase-01-governance-contract/v2"
governance_base_commit = "<unchanged-40-hex>"
governance_base_tree = "<unchanged-40-hex>"
source_branch = "main"
phase_branch = "agent/phase-01-governance"

[published_anchor]
commit = "<checkpoint-anchor-40-hex>"
tree = "<checkpoint-tree-40-hex>"
projection_sha256 = "<checkpoint-projection-64-hex>"
reviews_sha256 = "<checkpoint-review-transcript-64-hex>"
```

The v2 root has exactly the six keys shown and the table has exactly four; all
unknown keys, wrong types, uppercase hex, and alternate stage/version shapes
fail. `bootstrap_projection(v2)` returns a five-tuple whose first value is the
historical constant `phase-01-governance-contract/v1` and whose remaining four
values come from the unchanged base/branch fields, allowing exact comparison
with the unique historical v1 blob.

Immediately before accepting the Task 2 commit, the live root orchestrator
compares all four table values with its in-memory checkpoint, recomputes the
projection, review, and author-inventory digests, proves
`introduction -> anchor -> candidate` ancestry,
and writes a separate immutable `task-02-acceptance.json` session record with
the candidate SHA/tree and three sealed input digests. Repeat that
orchestration check before every later task dispatch and final evidence
assembly; losing the session checkpoint requires fresh reviews. The unit test
proves only the repository's network-free half: the original five-value
bootstrap projection is preserved, the introduction parent/tree are intact,
the fixed published anchor is an ancestor with the recorded tree, and both
contract-recorded external digests are well-formed. Plausible repository-authored digest strings
cannot satisfy the separate live checkpoint comparison.

- [ ] **Step 2: Verify the validator fails because the manifest is absent**

Run: `PYTHONPATH=src:. python -m unittest tests.test_requirements_manifest -v`

Expected: deliberate failures for the missing requirements/clause manifests
and the not-yet-migrated anchor-bound v2 contract; no import, collection, or
undefined-name error.

- [ ] **Step 3: Populate every approved requirement**

Each TOML record uses this complete shape:

```toml
[[requirements]]
id = "PRIV-01"
statement = "Python Doctor contains no telemetry subsystem."
owner = "privacy"
source_clauses = ["complete-design:constraint-4", "validation:G12"]
introduced_phase = 1
required_by_phase = 14
verification_phases = [1, 3, 11, 12, 13, 14]
implementation_artifacts = ["governance/requirements.toml"]
behavioral_evidence = ["no-runtime-network-imports", "process-tree-egress-denial"]
gate_check_ids = ["G00-PRIVACY-SCOPE", "G12-FORBIDDEN-CAPABILITIES", "G12-PROCESS-SET-DENIAL", "G13-LICENSE-SBOM-PROVENANCE"]
dependency_ids = ["QA-01"]
completion_condition = "All shipped runtime paths and artifacts satisfy PRIV-01 at the final candidate."
completion_predicates = ["all_required_checks_pass", "dependencies_closed", "required_review_bound", "final_verification_phase_complete"]
review_required = true
origin = "user_requirement"
```

Populate all IDs defined in `docs/governance/requirements-traceability.md`.
The independently reviewed expected-ID fixture freezes exact equality. Phase
1 governance evidence never marks a cross-phase product requirement verified.
`LEG-05` derives `BLOCKED` pending the legal artifact. Every completion criterion
maps to exact source clauses, implementation artifacts, behavioral evidence,
dependency IDs, executable gate-check IDs, and a non-file-existence completion
predicate.

The manifest freezes these contracts explicitly rather than linking only broad
prose: CORE-01's complete discovery inventory; CORE-02's ten scan modes;
CORE-07's rule fields; CORE-08–CORE-11's proof architecture; ADP-05's exact
provider list; ADP-06's hostile-repository threat model; REP-02's report fields;
REP-05's two explain surfaces; SKL-07's local and authorized-model evaluation
protocol; QA-03's coverage/mutation thresholds; and QA-04's precision/recall
thresholds. Source clauses are exact heading and requirement anchors, not
document-wide references.

Frozen inventory assertions also cover ARC-01 package/distribution names,
API-01 functions/signatures/defaults, CLI-01's exact command tree, CORE-04's
configuration fields/prohibitions, DOC-01 root files, DOC-02 detailed documents,
and every required LSP/editor/Action scenario. These inventories live as typed
clause/requirement records rather than the phrase “complete approved surface.”

`clause-registry.toml` freezes a stable clause ID, source document path, section,
normalized clause SHA-256, and assertion kind for every normative bullet. The
separately reviewed `expected-gate-clauses.toml` was created and frozen in
Task 0. This task consumes and validates it without editing it, before the
executable gate catalog, and it cannot be derived from `gates.toml`.

`validation-inputs.toml` is the sole versioned repository-input identity
inventory. It lists the
master prompt, primary specification, validation gates, proof architecture,
traceability index, this Phase 1 task contract, root instructions, every
normative governance manifest, every governance schema, every independently
frozen fixture, runner/identity/redaction/attestation source, and the Phase 1
evidence contract. Identity hashes normalized path, Git mode/type, size, and
bytes for every listed input; a missing or extra normative file is invalid
configuration. `toolchain.lock.toml` freezes CPython minor version, executable
digest, TOML backend/version/digest, Bubblewrap ownership/version/digest, Git
version, OpenSSL absolute path/version/SHA-256/trust source/Ed25519 feature
probe/exact `pkeyutl -verify -rawin` invocation, schema versions, and the exact
platform capability claim. A missing project-provisioned verifier is `FAIL`. It replaces
the prior no-lock sentinel.

Bootstrap uses `load_requirements(path)` rather than the all-manifest
`load_governance()` call. Bootstrap validation is explicitly non-evidentiary;
final strict loading activates only after every validation input exists in Task
10.

The repository base-binding validator reads the contract's unique Git addition
commit and compares the current five-value bootstrap projection to the
historical blob. It rejects multiple addition commits, a non-base parent, a
changed base commit or tree, a base/tree mismatch, missing anchor ancestry, or
rewritten/replayed local history. The orchestration validator independently
requires exact equality between the four inert checkpoint exports in the
contract and the live session checkpoint, including the complete reviewed
GitHub projection and transcript digests. Neither validator can substitute for
the other. Hashing only the current editable contract is insufficient. GitHub
unavailability before Task -1 capture is `BLOCKED`; a captured projection or
checkpoint mismatch is `FAIL`.

- [ ] **Step 4: Verify GREEN and regression**

Run:

```bash
PYTHONPATH=src:. python -m unittest tests.test_requirements_manifest -v
PYTHONPATH=src:. python -m unittest discover -s tests
```

Expected: all tests pass with no missing family, gate, artifact, or test mapping.

- [ ] **Step 5: Commit**

```bash
git add governance/clause-registry.toml governance/requirements.toml governance/toolchain.lock.toml governance/validation-inputs.toml tests/test_requirements_manifest.py tests/governance_helpers.py docs/evidence/contracts/phase-01-governance.toml
git diff --cached --name-only
git commit -m "docs(governance): freeze requirements traceability"
```

---

### Task 3: Provenance and restricted-source control

**Classification:** `verification_content`

**Requirements:** `LEG-01`–`LEG-06`, `PRIV-04`, `QA-05`

**Files:**

- Create: `governance/provenance.toml`
- Create: `docs/legal/restricted-source-review-process.md`
- Create: `docs/research/provenance-sources.md`
- Create: `docs/research/query-rounds.md`
- Create: `docs/research/saturation-review.md`
- Create: `schemas/governance/clean-implementer-certification-v1.schema.json`
- Consume without editing: `tests/fixtures/governance/expected-provenance-sources.toml`
- Create: `tests/test_provenance_manifest.py`
- Modify: `.gitignore`

**Interfaces:**

- Produces: source records and a fail-closed legal disposition contract.
- Does not consume or store restricted content in the repository.

- [ ] **Step 1: Write permission-forgery rejection tests**

```python
REQUIRED_APPROVAL_FIELDS = {
    "artifact_sha256", "grantor_identity", "authority_basis",
    "decision_date", "repository", "revision", "ai_use_scope",
    "adaptation_scope", "redistribution_scope", "covered_material",
    "attribution_terms", "reviewer_identity", "reviewer_disposition",
}

def test_rejects_approval_without_authority_and_scope() -> None:
    record = restricted_source_record(status="approved", approval={})
    violations = validate_provenance((record,))
    assert REQUIRED_APPROVAL_FIELDS.issubset(missing_fields(violations))

def test_raw_legal_artifact_is_never_committed() -> None:
    legal_paths = (
        ".evidence/legal/permission-message.raw",
        ".evidence/legal/permission-message.sha256",
        ".evidence/legal/trusted-review-root.pem",
        ".evidence/legal/trust-anchor-receipt.json",
        ".evidence/legal/trust-anchor-receipt.sig",
        ".evidence/legal/permission-review.json",
        ".evidence/legal/permission-review.sig",
    )
    for path in legal_paths:
        ignored = subprocess.run(
            ["git", "check-ignore", "--no-index", "-q", "--", path],
            cwd=ROOT,
            check=False,
        )
        assert ignored.returncode == 0, path
    tracked = subprocess.run(
        ["git", "ls-files", "-z", ".evidence"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    assert tracked == b""

def test_project_known_source_inventory_is_exact() -> None:
    expected = load_expected_sources(
        ROOT / "tests/fixtures/governance/expected-provenance-sources.toml"
    )
    actual = load_provenance(ROOT / "governance/provenance.toml")
    assert project_known_projection(actual) == expected

def test_supplied_pdf_is_excluded_and_hashed() -> None:
    source = find_source("power-of-ten-user-supplied-pdf")
    assert source.artifact_sha256 == "c762a07be7b8ea65b95e1f1f748efa60f7196d75fdf81181169cfb8e0b2b4c8f"
    assert source.distribution == "excluded"

def test_clean_implementer_certifications_fail_closed() -> None:
    subject = final_subject_fixture()
    assert certification_state(subject, ()) is GateState.BLOCKED
    assert certification_state(subject, (completion_without_pre_task_declaration(),)) is GateState.FAIL
    assert certification_state(subject, (verified_certification_chain(exposure_status="tainted"),)) is GateState.FAIL
    assert certification_state(subject, (forged_nonempty_certification(),)) is GateState.FAIL
    assert certification_state(subject, (signed_certification_for_wrong_subject(),)) is GateState.FAIL
    assert certification_state(subject, (signed_certification_for_wrong_task(),)) is GateState.FAIL
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_provenance_manifest -v`

Expected: missing provenance manifest and legal process document.

- [ ] **Step 3: Add the blocked restricted-source record**

```toml
[[sources]]
source_id = "restricted-react-doctor-reference"
kind = "restricted_repository"
url = "https://github.com/millionco/react-doctor"
immutable_revision = "d8b2989fd5d440d70931743a88ab6f7a91cf7b89"
license_id = "modified-restricted-pending-authorized-review"
license_path = "pending-authorized-review"
license_sha256 = "pending-authorized-review"
license_status = "restricted_pending_authorized_review"
inspected_paths = ["pending-authorized-review"]
concepts = []
disposition = "prohibited_pending_review"
attribution = "pending-authorized-review"
artifact_sha256 = ""
distribution = "excluded"

[[restricted_sources]]
source_id = "restricted-react-doctor-reference"
exposure_status = "previously_inspected"
inspected_paths = ["pending-authorized-review"]
taint_determination = "pending-authorized-review"
raw_artifact_path = ".evidence/legal/permission-message.raw"
raw_artifact_sha256 = ""
review_owner = "external_authorized_human_or_legal_reviewer"
status = "blocked"
```

No `[[legal_dispositions]]` record exists until Task 4 receives and validates
the externally trusted review.

Certifications are never committed to `provenance.toml`, because a record naming
its containing commit would be self-referential. Before work, each context-free
implementer/reviewer signs a pre-task declaration under
`.evidence/certifications/<id>/` binding identity, role, exposure status,
approved-input-bundle SHA-256, execution-base commit/tree, authorized task IDs,
and date. After work, the implementer signs a completion payload binding the
pre-task declaration digest, final subject commit/tree, actually completed task
IDs, and date. An independent reviewer verifies the chain and countersigns the
completion with an externally pinned trust root.

G00 verifies both canonical payloads, both implementer signatures, trusted
reviewer countersignature, base ancestry, final subject/tree, subset/equality of
task scope, and input-bundle equality, then places only the verified chain
receipt in E1 evidence. Forged, missing-pre-task, wrong-key, wrong-subject,
wrong-task, tainted, or unsigned chains fail. Missing pre-task declaration is
external `BLOCKED` only before assignment; missing evidence for work already
performed is `FAIL`.

The certification schema uses the same duplicate-key rejection and canonical
JSON byte rules as `legal-review-v1`, with separate domain prefixes
`python-doctor/clean-implementer-pre-task/v1\0` and
`python-doctor/clean-implementer-completion/v1\0`.

Also record:

- every prior research source with immutable revision, verified license, exact
  inspected paths, extracted concept, disposition, and attribution;
- the supplied Power-of-Ten PDF identifier/hash, citation, redistribution
  prohibition, and artifact exclusion;
- research query rounds, dates, registries, results, and two-round saturation;
- clean-implementer/reviewer identity, exposure status, approved input set,
  certification date, and task range.

The expected-source fixture enumerates every known research source by stable
ID, URL/repository, immutable revision, license ID/path/hash, inspected paths,
concepts, disposition, and attribution. The three research documents enumerate
exact query text, date, registry/domain, result IDs, disposition, two consecutive
zero-new-category rounds, and reviewer saturation decision. Missing or malformed
project-known inventory is `FAIL`; only absent genuinely external permission or
review authority is `BLOCKED`.

The initial source-ID inventory is exact: `restricted-react-doctor-reference`,
`power-of-ten-user-supplied-pdf`, `agent-skills-spec`, `anthropic-skills`,
`openai-skills`, `github-awesome-copilot`, `wshobson-agents`,
`trailofbits-skills`, `microsoft-python-guidance`, `huggingface-skills`,
`superpowers-skills`, `python-language-reference`, `pep-0008`, `pep-0020`,
`pep-0257`, `python-typing-guidance`, `pypa-specifications`, `pytest-docs`,
`hypothesis-docs`, `ruff-docs`, `mypy-docs`, and `bandit-docs`. Task 3 may add a
source only through a reviewed fixture change with immutable revision/license
evidence; it may not silently drop or merge these IDs. Exact revisions,
license hashes, and inspected paths come from the retained pre-restriction
research ledger or fresh public-source verification, never invention.

Pending values are valid only while the legal child derives `BLOCKED`; they can
never support `PASS`.

The legal process document states that the user assertion alone cannot close
the check. The actual message stays raw, hashed, and outside Git. No automated
agent rereads the reference or performs similarity comparison.

- [ ] **Step 4: Verify GREEN with G00 still blocked**

Run: `PYTHONPATH=src:. python -m unittest tests.test_provenance_manifest -v`

Expected: manifest valid; restricted source state is `blocked`.

- [ ] **Step 5: Commit**

```bash
git add .gitignore governance/provenance.toml schemas/governance/clean-implementer-certification-v1.schema.json docs/legal/restricted-source-review-process.md docs/research/provenance-sources.md docs/research/query-rounds.md docs/research/saturation-review.md tests/test_provenance_manifest.py
git commit -m "docs(governance): record clean-room provenance controls"
```

---

### Task 4: Conditional permission ingestion and authorized disposition

**Classification:** `verification_content`

**Requirements:** `LEG-05`, `LEG-06`, `QA-05`

**Files:**

- Create locally, never commit: `.evidence/legal/permission-message.raw`
- Create locally, never commit: `.evidence/legal/permission-message.sha256`
- Obtain externally, never commit: `.evidence/legal/trusted-review-root.pem`
- Obtain externally, never commit: `.evidence/legal/trust-anchor-receipt.json`
- Obtain externally, never commit: `.evidence/legal/trust-anchor-receipt.sig`
- Obtain externally, never commit: `.evidence/legal/permission-review.json`
- Obtain externally, never commit: `.evidence/legal/permission-review.sig`
- Consume only from the immutable governance base, never create or modify in
  Tasks 0–10: `governance/trust/legal-release-authority-v1.pem`
- Update after authorized review: `governance/provenance.toml`
- Create: `schemas/governance/legal-review-v1.schema.json`
- Create: `schemas/governance/trust-anchor-receipt-v1.schema.json`
- Create: `tests/test_legal_disposition.py`

**Interfaces:**

- Consumes: a user-supplied unaltered permission message and an authorized
  human/legal disposition.
- Produces: sanitized provenance metadata only. It never stores message text,
  headers, personal identifiers, or legal correspondence in Git.

**Precondition and blocked-state rule:** Task 4 must not create any
`.evidence/legal/*` file until Task 3 has committed `.evidence/` to `.gitignore`
and its tracked-file rejection test passes. Task 4 may implement and test the
fail-closed derivation mechanics while external review is absent. It must not
add an approved sanitized disposition, report G00 `PASS`, or treat a user
assertion as authority until the complete externally rooted signed review is
present and verifies successfully; otherwise G00 remains `BLOCKED`.

- [ ] **Step 1: Add fail-closed transition tests**

```python
LEGAL_EVIDENCE_PATHS = (
    ".evidence/legal/permission-message.raw",
    ".evidence/legal/permission-message.sha256",
    ".evidence/legal/trusted-review-root.pem",
    ".evidence/legal/trust-anchor-receipt.json",
    ".evidence/legal/trust-anchor-receipt.sig",
    ".evidence/legal/permission-review.json",
    ".evidence/legal/permission-review.sig",
)

def test_permission_summary_cannot_approve_legal_gate() -> None:
    record = restricted_record(
        artifact_sha256="",
        reviewer_disposition="approved",
    )
    assert legal_state(record, raw_artifact=None, trusted_review=None) is GateState.BLOCKED


def test_signed_fixture_review_can_satisfy_derivation_mechanics() -> None:
    authority_root, trust_root, signed_anchor, raw, signed_review = signed_legal_fixture()
    record = restricted_record(
        artifact_sha256=sha256(raw),
        review_attestation_sha256=sha256(signed_review.json_bytes),
    )
    anchored_root = verify_trust_anchor(signed_anchor, authority_root)
    assert legal_state(record, raw, verify_review(signed_review, trust_root, anchored_root)) is GateState.PASS

def test_complete_self_authored_strings_never_pass() -> None:
    raw = b"invented permission"
    record = complete_looking_record(artifact_sha256=sha256(raw))
    assert legal_state(record, raw, trusted_review=None) is GateState.BLOCKED

def test_self_generated_review_root_cannot_substitute_for_base_authority() -> None:
    attacker = self_generated_legal_bundle()
    assert verify_trust_anchor(attacker.anchor, governance_base_authority_key()) is None
    assert legal_state(attacker.record, attacker.raw, trusted_review=None) is GateState.BLOCKED

def test_missing_base_authority_key_is_blocked() -> None:
    assert live_legal_state(governance_base_without_authority_key()) is GateState.BLOCKED

def test_trust_anchor_receipt_rejects_wrong_semantics() -> None:
    assert_anchor_rejected(anchor_receipt(purpose="anything-else"))
    assert_anchor_rejected(anchor_receipt(schema_version="trust-anchor-receipt/v0"))
    assert_anchor_rejected(anchor_receipt(authority_identity="substitute-authority"))
    assert_anchor_rejected(anchor_receipt(not_after=VERIFICATION_TIME - 1))
    assert_anchor_rejected(anchor_receipt(not_before=VERIFICATION_TIME + 1))

def test_trust_anchor_receipt_rejects_noncanonical_or_ambiguous_bytes() -> None:
    assert_anchor_rejected(anchor_with_duplicate_json_key())
    assert_anchor_rejected(anchor_with_unknown_key())
    assert_anchor_rejected(anchor_with_noncanonical_json())
    assert_anchor_rejected(anchor_signed_under_legal_review_domain())
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_legal_disposition -v`

Expected: legal-state derivation does not exist.

- [ ] **Step 3: Ingest the raw artifact outside Git**

Copy the unaltered supplied message to `.evidence/legal/permission-message.raw`
and calculate SHA-256 without printing contents. Record sender/grantor authority,
date, repository/revision, AI-use, adaptation, redistribution, covered-material,
attribution, notice, and other conditions in the authorized review worksheet.
If any required field is ambiguous, state remains `BLOCKED`.
The validator recomputes the raw file hash when it is locally present and
requires exact equality with sanitized metadata. If the file is unavailable on
another machine, the external prerequisite remains `BLOCKED`; it never trusts
the metadata value alone.

- [ ] **Step 4: Obtain and record authorized review**

Only an authorized human/legal reviewer may set the sanitized disposition.
`permission-review.json` is canonical JSON that binds raw permission SHA-256,
grantor identity and authority evidence digest, exact repository/revision,
AI-use/adaptation/redistribution/material scopes, conditions, attribution,
reviewer identity/authority basis, decision/date, and review schema version.
The authorized reviewer signs it with Ed25519. `trusted-review-root.pem` is
provisioned out of band by the independent release authority, but a caller-
supplied root is never trusted by itself. The independent release authority
also signs `trust-anchor-receipt.json`, which binds that review-root fingerprint,
purpose, validity interval, authority identity, and schema version. The receipt
signature is verified only with
`governance/trust/legal-release-authority-v1.pem` read byte-for-byte from
`governance_base_commit`, not from the current worktree, environment, CLI, or
editable metadata. If that authority key was absent from the immutable base,
the live legal child is unconditionally `BLOCKED`; introducing it requires a
separately authorized protected-main change and a complete Phase 1 restart from
the new governance base. Tasks 0–10 may implement synthetic verification
mechanics but may not add or replace that key.

The pinned OpenSSL verifier checks both signatures and exact canonical bytes.
`legal_state()` requires the raw digest match, a review root whose fingerprint
matches the authority-signed receipt, and a verified trusted review. A locally
generated root, a caller-provided expected fingerprint, complete-looking TOML
strings, `initial_state`, `approved = true`, or user assertion can produce only
`BLOCKED` or `FAIL`, never `PASS`. Record clean-implementer exposure
certifications separately.

`legal-review-v1` allows closed objects, UTF-8 strings, booleans, arrays, and
bounded base-10 integers only—no floats. Parsing rejects duplicate keys,
unknown keys, invalid Unicode, NaN/infinity, and non-minimal integers. Signed
bytes use sorted Unicode-code-point object keys, standard shortest JSON string
escapes, lowercase literals, compact separators, UTF-8, and exactly one trailing
newline, prefixed for signature by `python-doctor/legal-review/v1\0`. Parsing
then reserialization must reproduce the signed bytes exactly.

`trust-anchor-receipt-v1` uses the same closed-object, duplicate-key rejection,
integer, Unicode, and canonical JSON rules, but signs bytes under the distinct
domain prefix `python-doctor/trust-anchor-receipt/v1\0`. It requires exactly
`schema_version = "trust-anchor-receipt/v1"`,
`purpose = "python-doctor/legal-review-root"`,
`authority_identity = "python-doctor-independent-release-authority-v1"`, the
lowercase SHA-256 fingerprint of the review root, and bounded UTC integer
`not_before`/`not_after` values with `not_before <= verification_time <=
not_after`. Verification time comes from the gate execution clock, is recorded
in the evidence ledger, and is not accepted from receipt fields, CLI arguments,
environment variables, or editable metadata. Wrong schema, purpose, authority
identity, domain prefix, key fingerprint, validity interval, canonical bytes,
or signature produces `FAIL`; an absent base authority key or absent external
receipt remains `BLOCKED`.

The legal check receives only declared read-only external files inside the
containment backend. Its `CheckResult.external_input_hashes` records raw
permission, canonical review JSON, review signature, canonical trust-anchor
receipt, and receipt signature SHA-256. It separately records the base-loaded
release-authority key fingerprint, anchored review-root fingerprint, and
verified authority-evidence digest. Any change invalidates the check without
changing `SubjectIdentity`.

- [ ] **Step 5: Prove raw material is ignored, not absent**

```python
def test_raw_permission_artifact_is_not_tracked() -> None:
    for path in LEGAL_EVIDENCE_PATHS:
        ignored = subprocess.run(
            ["git", "check-ignore", "--no-index", "-q", "--", path],
            cwd=ROOT,
            check=False,
        )
        assert ignored.returncode == 0, path
    tracked = subprocess.run(
        ["git", "ls-files", "-z", ".evidence"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    assert tracked == b""
```

- [ ] **Step 6: Verify and commit only sanitized metadata**

Run: `PYTHONPATH=src:. python -m unittest tests.test_legal_disposition -v`

Expected: `PASS` only with raw digest equality and the externally rooted signed
authorized disposition; otherwise
`BLOCKED`.

```bash
git add governance/provenance.toml schemas/governance/legal-review-v1.schema.json schemas/governance/trust-anchor-receipt-v1.schema.json tests/test_legal_disposition.py
git diff --cached --name-only
git commit -m "docs(legal): record restricted-source disposition"
```

---

### Task 5: Publication and compatibility scope

**Classification:** `verification_content`

**Requirements:** `PUB-01`–`PUB-03`, `ARC-03`, `REL-01`

**Files:**

- Create: `governance/authorized-destinations.toml`
- Create: `governance/compatibility.toml`
- Create: `tests/test_authorized_destinations_manifest.py`
- Create: `tests/test_compatibility_manifest.py`

- [ ] **Step 1: Write the scope RED tests**

```python
def test_only_source_repository_is_currently_authorized() -> None:
    manifest = load_destinations(ROOT)
    required = {item.destination_id for item in manifest.destinations if item.state == "required"}
    assert required == {"github-source-branch"}
    assert destination(manifest, "github-source-branch").repository == "shriyansh24/python-doctor"
    assert destination(manifest, "github-source-branch").ref_pattern == "refs/heads/main"
    assert manifest.development_branch_pattern == r"refs/heads/agent/[a-z0-9][a-z0-9-]{0,62}"
    assert manifest.candidate_branch_pattern == r"refs/heads/candidate/[a-f0-9]{40}"
    assert manifest.unknown_destination_policy == "deny"
    assert destination(manifest, "pypi").state == "not_authorized"
    assert destination(manifest, "github-tags").state == "not_authorized"

def test_essential_matrix_is_not_narrowable() -> None:
    matrix = load_compatibility(ROOT)
    assert matrix.essential_components == ("core", "api", "cli", "native-rules", "reports")
    assert matrix.python_versions == ("3.9", "3.10", "3.11", "3.12", "3.13", "3.14")
    assert matrix.target_grammars == ("3.9", "3.10", "3.11", "3.12", "3.13", "3.14")
    assert matrix.operating_systems == ("linux", "macos", "windows")
    essential_rows = tuple(row for row in matrix.rows if row.component in matrix.essential_components)
    assert all(item.support_tier == "essential" for item in essential_rows)
    assert all(item.claim_status == "planned" for item in essential_rows)
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_authorized_destinations_manifest tests.test_compatibility_manifest -v`

Expected: both manifests are absent.

- [ ] **Step 3: Populate exact scope**

Authorize required `refs/heads/main`, review branches matching
`refs/heads/agent/<lowercase-slug>`, and candidate refs matching
`refs/heads/candidate/<40-lowercase-hex>` in
`https://github.com/shriyansh24/python-doctor`. The only required publication
record is `main`; agent refs are permitted review staging and candidate refs are
permitted verification staging, not releases. Mark tags, Releases, Pages, PyPI,
editor registries, containers, and every other destination `not_authorized`;
unknown destination kinds deny by default. Freeze `core`, `api`, `cli`,
`native-rules`, and `reports` as essential for host and target grammar 3.9–3.14
on Linux/macOS/Windows. Later integrations are `planned` with decision phases
and cannot support current claims.

Repository orientation on 2026-07-14 used the connected GitHub app, which
reported default branch `main` at commit
`e3049ee12771c1055bde2392adeba2de33324602`. The local historical branch is
named `master` and has unrelated commit ancestry; it is not evidence that the
remote required ref is `master`. Publication must branch from fetched
`origin/main`, preserve its history, and never force-push or substitute the
local `master` ref.

- [ ] **Step 4: Verify and commit**

```bash
PYTHONPATH=src:. python -m unittest tests.test_authorized_destinations_manifest tests.test_compatibility_manifest -v
git add governance/authorized-destinations.toml governance/compatibility.toml tests/test_authorized_destinations_manifest.py tests/test_compatibility_manifest.py
git diff --cached --name-only
git commit -m "docs(governance): freeze release and compatibility scope"
```

---

### Task 6: Complete skill release manifest

**Classification:** `verification_content`

**Requirements:** `SKL-01`–`SKL-07`

**Files:**

- Create: `governance/skills-release.toml`
- Create: `tests/test_skills_release_manifest.py`
- Consume without editing: `tests/fixtures/governance/expected-skill-ids.txt`
- Consume without editing: `tests/fixtures/governance/expected-profile-domain-ids.txt`

- [ ] **Step 1: Write manifest contract tests**

```python
def test_all_required_skill_ids_are_frozen() -> None:
    manifest = load_skill_release(ROOT)
    assert ids(manifest) == frozen_ids("expected-skill-ids.txt")
    assert len(ids(manifest)) == 198
    assert all(item.required for item in required_items(manifest))
    assert all(item.lifecycle == "planned" for item in required_items(manifest))
    assert all(not item.delivered_capabilities for item in required_items(manifest))

def test_route_graph_is_acyclic_and_budgeted() -> None:
    manifest = load_skill_release(ROOT)
    assert find_cycles(manifest) == ()
    assert manifest.default_router_budget == 1
    assert manifest.default_leaf_budget == 5

def test_profile_domain_inventory_is_exact() -> None:
    manifest = load_skill_release(ROOT)
    assert profile_domain_ids(manifest) == frozen_ids("expected-profile-domain-ids.txt")
    assert len(profile_domain_ids(manifest)) == 9

def test_plans_cannot_inflate_delivery() -> None:
    manifest = load_skill_release(ROOT)
    assert all(not item.delivered_capabilities for item in planned_items(manifest))
    assert all(item.planned_evaluation_ids for item in agent_facing_items(manifest))
```

Also reject duplicate IDs, ownerless leaves, router/profile kind mismatches,
planned entries claiming evaluated delivery, network authority, mutation without
authorization/rollback, and noncanonical sources.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_skills_release_manifest -v`

Expected: manifest absent.

- [ ] **Step 3: Populate from approved sections**

Every required router/profile/leaf from sections 8.2–8.13 and 8.15 declares:

```toml
[[skills]]
id = "naming-python"
kind = "diagnostic_review"
owner_router = "review-python"
required = true
lifecycle = "planned"
planned_capabilities = ["guidance"]
delivered_capabilities = []
triggers = ["semantic naming review requested"]
exclusions = ["mechanical formatter-only change"]
prerequisites = []
conflicts = []
precedence = 100
support_contracts = ["python>=3.9", "source:python"]
context_cost = 3
mutation_authority = "none"
rollback_contract = "not_applicable_read_only"
evidence_policy = "semantic_evidence_required"
false_positive_policy = "advisory_by_default"
fix_policy = "no_automatic_public_rename"
agent_skills_schema_revision = "agentskills-v1-pinned-digest"
reference_depth = 1
planned_evaluation_ids = ["naming-baseline", "naming-enabled", "naming-adversarial-1", "naming-adversarial-2", "naming-routing"]
canonical_source = "skills/naming-python"
```

The separately reviewed 198-ID fixture is the completeness oracle. The 8.14
profile-domain fixture gives every grouped domain a stable ID and exact support
tier. Its nine records correspond to the nine 8.14 groups and each freezes the
full required-topic inventory, so individual technologies cannot disappear
inside a group. Planned evaluation IDs are validated as syntactically stable future
records with `scheduled_phase = 9`; delivered evaluation IDs may reference only
an existing versioned eval manifest. Additional profile domains declare
`delivered`, `planned`, or `unsupported` and never count toward delivery while
planned.

The nine profile IDs and required topics are exact:

- `profile-environments-workflows`: pip, uv, Poetry, Conda, PDM, Hatch, Pipenv,
  tox, nox, lock and hash policy;
- `profile-typing-ecosystems`: mypy, Pyright, basedpyright, stubs, `py.typed`,
  gradual typing, version-specific typing;
- `profile-object-native-boundaries`: MRO, metaclasses, slots, weak references,
  import-time effects, C, Cython, ctypes, CFFI, PyO3, ABI, buffers;
- `profile-python-runtimes`: CPython, PyPy, free-threaded CPython, embedded
  Python, MicroPython, CircuitPython, Pyodide, WASM;
- `profile-ui-tui`: Tkinter, Qt, PySide, Kivy, Textual, Rich, accessibility;
- `profile-distributed-scientific`: Ray, Dagster, Prefect, Kafka clients,
  SciPy, xarray, Numba, MPI, Arrow, Parquet, Protobuf, schema evolution;
- `profile-application-protocols`: REST, OpenAPI, GraphQL, WebSockets, gRPC,
  MCP, events, serverless handlers;
- `profile-platform-text-time`: Unicode, internationalization, locale,
  filesystem, Windows, time-zone correctness;
- `profile-malicious-repositories`: prompt injection in source, symlink escape,
  giant/minified/generated files, hostile filenames, archive bombs.

- [ ] **Step 4: Verify and commit**

```bash
PYTHONPATH=src:. python -m unittest tests.test_skills_release_manifest -v
git add governance/skills-release.toml tests/test_skills_release_manifest.py
git diff --cached --name-only
git commit -m "docs(skills): freeze complete release manifest"
```

---

### Task 7: Candidate identity and evidence redaction

**Classification:** `behavior_change`

**Requirements:** `QA-02`, `PRIV-04`, `REL-03`

**Files:**

- Create: `scripts/gates/identity.py`
- Create: `scripts/gates/redaction.py`
- Create: `tests/test_gate_identity.py`
- Create: `tests/test_gate_redaction.py`

- [ ] **Step 1: Write RED tests**

```python
def test_dirty_tree_changes_candidate_identity() -> None:
    root = complete_identity_fixture()
    clean = identify_subject(root)
    with temporary_untracked_file(root, "dirty.txt"):
        dirty = identify_subject(root)
    assert clean.dirty is False
    assert dirty.dirty is True
    assert clean != dirty

def test_two_tracked_edits_have_distinct_dirty_identity() -> None:
    root = complete_identity_fixture()
    first = identify_after_tracked_edit(root, b"first")
    second = identify_after_tracked_edit(root, b"second")
    assert first.dirty_state_digest != second.dirty_state_digest

def test_hostile_filesystem_entries_fail_without_reading() -> None:
    root = complete_identity_fixture(untracked_kind="fifo")
    with assert_raises(InvalidCandidate):
        identify_subject(root)

def test_anchor_binding_is_derived_only_from_strict_v2_contract() -> None:
    root = complete_identity_fixture()
    identity = identify_subject(root)
    contract = load_phase_contract(
        root / "docs/evidence/contracts/phase-01-governance.toml",
        expected_stage="anchor-bound",
    )
    anchor = contract.published_anchor
    assert anchor is not None
    assert identity.published_anchor_commit == anchor.commit
    assert identity.published_anchor_tree == anchor.tree
    assert identity.published_anchor_projection_sha256 == anchor.projection_sha256
    assert identity.published_anchor_reviews_sha256 == anchor.reviews_sha256

def test_missing_tampered_or_nonancestor_anchor_binding_is_invalid() -> None:
    for mutation in ("missing", "wrong-tree", "malformed-digest", "nonancestor"):
        root = complete_identity_fixture(anchor_mutation=mutation)
        with assert_raises(InvalidCandidate):
            identify_subject(root)

def test_redaction_removes_sensitive_values_and_controls() -> None:
    raw = f"{HOME}/repo secret={SECRET}\x1b[31m hostile.py"
    redacted = redact_text(raw, secrets=(SECRET,))
    assert HOME not in redacted
    assert SECRET not in redacted
    assert "\x1b" not in redacted
    assert "<HOME>" in redacted
    assert "<REDACTED>" in redacted
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_gate_identity tests.test_gate_redaction -v`

Expected: modules absent. After implementation the live-root final identity
remains invalid until every Task 8–10 normative input exists; unit tests use a
complete temporary fixture, never a partial live identity as gate evidence.

- [ ] **Step 3: Implement deterministic identity/redaction**

Use `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git diff --binary
--no-ext-diff`, `git diff --cached --binary --no-ext-diff`, and `git status
--porcelain=v1 -z` with argv arrays, hooks/config/external diff disabled, and a
minimal environment. Subject identity derives the runner version from the
versioned source plus runner-source digest; no caller-supplied version is
trusted. Its dependency-lock digest covers the versioned toolchain lock bytes;
observed executable versions/digests belong only to the separate execution-
environment identity. `identify_subject()` loads the strict v2 `PhaseContract`
itself and accepts no caller-supplied anchor values. It copies all four
`SubjectIdentity` anchor fields only from `published_anchor`, rejects a missing
binding, proves the unique contract introduction is an ancestor of the anchor,
proves the anchor/tree match and anchor ancestry to the candidate, and rejects
malformed digest syntax or a locally inconsistent tree before returning an
identity. A syntactically valid but substituted projection/review digest is
indistinguishable to repository-only code and is rejected only by the live
orchestration checkpoint comparison. The validation-input digest is the canonical hash of every
entry named by `validation-inputs.toml`; final identity refuses any missing
entry. Task 7 uses a complete temporary normative fixture because live Task
8–10 inputs do not yet exist; bootstrap subjects use
`identity_kind = IdentityKind.BOOTSTRAP` and may drive unit tests only.

Every collection digest hashes a canonical sequence of raw root-relative path
bytes, Git/file mode and type, size, and exact bytes/content digest with
explicit absence markers. It covers staged/unstaged tracked modifications,
deletions, renames, type changes, and non-ignored untracked entries, so equal
porcelain labels cannot collide. Traverse with `lstat`, never follow symlinks,
reject devices/FIFOs/sockets and escapes, and enforce file/byte/time limits.
Later monorepo phases add every nested project metadata and recognized lock
through the versioned input inventory. A release candidate with `dirty = true`
is invalid; diagnostic evidence may bind the safe dirty digest. Redact longest
sensitive values first, normalize
roots to stable placeholders, escape bidi/ANSI/control bytes, sanitize argv
credentials and credentialed URLs, and cap every output stream and aggregate.
Tests include binary/multiline output, Unicode controls, hostile names, cloud/
Git/package tokens, home aliases, symlinked roots, and truncation.

- [ ] **Step 4: Verify and commit**

```bash
PYTHONPATH=src:. python -m unittest tests.test_gate_identity tests.test_gate_redaction -v
git add scripts/gates/identity.py scripts/gates/redaction.py tests/test_gate_identity.py tests/test_gate_redaction.py
git diff --cached --name-only
git commit -m "feat(gates): bind and redact validation evidence"
```

---

### Task 8: Canonical fail-closed gate runner

**Classification:** `behavior_change`

**Requirements:** `QA-01`, `QA-02`, `PRIV-01`, `PRIV-02`

**Files:**

- Create: `scripts/gates/runner.py`
- Create: `scripts/gates/attestation.py`
- Create: `scripts/gates/child_protocol.py`
- Create: `scripts/gates/containment.py`
- Create: `scripts/gates/__main__.py`
- Consume: `scripts/governance/__init__.py`
- Create: `scripts/governance/validate.py`
- Create: `schemas/governance/child-result-v1.schema.json`
- Create: `schemas/governance/check-result-v1.schema.json`
- Create: `schemas/governance/gate-result-v1.schema.json`
- Create: `schemas/governance/evidence-index-v1.schema.json`
- Create: `tests/test_gate_runner.py`
- Create: `tests/test_evidence_attestation.py`
- Create: `tests/test_governance_schemas.py`
- Create: `tests/test_network_containment.py`

- [ ] **Step 1: Write runner RED tests**

```python
def test_aggregate_precedence() -> None:
    assert aggregate((GateState.PASS, GateState.BLOCKED)) is GateState.BLOCKED
    assert aggregate((GateState.PASS, GateState.BLOCKED, GateState.FAIL)) is GateState.FAIL

def test_exit_contract() -> None:
    assert exit_code(GateState.PASS) == 0
    assert exit_code(GateState.NOT_APPLICABLE) == 0
    assert exit_code(GateState.FAIL) == 1
    assert exit_code(GateState.BLOCKED) == 2

def test_empty_aggregate_is_invalid_configuration() -> None:
    with assert_raises(InvalidGateConfiguration):
        aggregate(())

def test_invalid_configuration_returns_three_without_gate_result() -> None:
    completed = invoke_runner(malformed_manifest_tree())
    assert completed.returncode == 3
    assert not completed.gate_result_path.exists()

def test_owned_missing_tool_is_failure() -> None:
    spec = check(required_tools=(owned_tool("missing-owned-tool"),))
    result = run_check(ROOT, spec, candidate(), evidence_dir())
    assert result.state is GateState.FAIL

def test_timeout_kills_process_tree() -> None:
    spec, pid_probe = spawning_timeout_check()
    result = run_check(ROOT, spec, candidate(), evidence_dir())
    assert result.state is GateState.FAIL
    assert all(not process_is_alive(pid) for pid in pid_probe.recorded_pids())
```

Also cover warning/skip/deselection/xfail/xpass/retry/collection failure,
missing artifact, false `NOT_APPLICABLE`, argv/cwd/path rejection, proxy/token
environment stripping, deterministic JSON, and zero socket creation on import.
Add child-protocol cases for missing, duplicate, malformed, wrong-version, and
wrong-check-ID results. Process cases cover child and grandchild, attempted
detach, timeout, cancellation, output flood, and post-run PID cleanup.

The runner appends reserved `--python-doctor-result-json <private-path>` to each
registered project-owned child command. Manifests containing that reserved
option are invalid. External tools run only behind project-owned adapters that
emit the child schema. Each check gets a mode-0700 private directory and an
exclusive no-follow regular result file; sibling checks cannot write it.
Symlinks, hardlink count changes, devices, FIFOs, sockets, ownership/type
mismatch, or post-validation mutation fail. Validated evidence is atomically
promoted into the gate directory.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_gate_runner -v`

Expected: runner absent.

- [ ] **Step 3: Implement the runner**

Use `subprocess.Popen` with `shell=False`, explicit cwd, a minimal environment,
captured bounded bytes, monotonic timeout, and the structured child protocol.
Manual prose cannot set PASS. Emit canonical JSON plus a sanitized summary under
`.evidence/`. `ExecutionRecord` binds a separate execution-environment identity,
UTC start/finish, redacted argv, stable working-directory token, exit, warnings/
skips/retries, redaction version, and artifact hashes to `SubjectIdentity`. It never
serializes an absolute cwd, raw credential-bearing argument, username, home, or
host path.

Phase 1 gate *execution evidence* is supported only on Linux with an independently
feature-tested Bubblewrap backend using a new user/PID/network namespace,
read-only subject tree, writable runner-owned evidence directory,
`--die-with-parent`, and a new session. The Bubblewrap executable is an external
prerequisite resolved by absolute trusted path and version/digest; absence or a
failed feature probe yields `BLOCKED`, never an uncontained fallback. Manifest
validation and schema tooling remain cross-platform. macOS and Windows return a
typed containment-unavailable result in Phase 1; product-level macOS/Windows
backends (including Windows Job Objects for process ownership plus a separately
verified egress control) are required before cross-platform release claims.
Canaries do not substitute for containment.

Deterministic unit tests use fake containment backends and always run in normal
`unittest` discovery. The real containment probe is a structured Phase 1 gate
child, not a skip-capable unit test. It starts host-local TCP and UDP/DNS
canaries, then proves sandboxed direct-IP, DNS, HTTP, proxy-variable, child,
grandchild, and detached attempts cannot reach them. It also proves the subject
tree is read-only and cancellation/timeout leaves no descendant. Missing
project-provisioned/pinned Bubblewrap or a broken project probe is `FAIL`;
verified external kernel/user-namespace denial after documented alternatives is
`BLOCKED`. Normal unit discovery can pass by proving this classification while
the separate real gate remains honestly `BLOCKED`.

`write_attestation_ref(root: Path, subject: SubjectIdentity, payload_dir:
Path) -> tuple[str, str]` uses argv-only Git plumbing and a temporary index. It
creates parentless payload commit E1 containing only schema-valid sanitized
evidence, then binding commit E2 containing the subject commit/tree and E1 hash.
It compare-and-swaps `refs/python-doctor/evidence/<subject-commit>` from the zero
OID to E2. An existing ref is accepted only if it resolves to byte-identical E1
and E2; overwrite is forbidden. Git runs with hooks disabled, stripped
environment, explicit safe config, and a clean subject. No
evidence commit is merged into the subject and product artifacts are built only
from the subject. The two-commit construction avoids a self-hash claim.

- [ ] **Step 4: Verify interface and tests**

```bash
PYTHONPATH=src:. python -m unittest tests.test_gate_runner -v
PYTHONPATH=src:. python -m scripts.gates --help
```

Expected: tests pass; help exits 0 without network or filesystem mutation.

- [ ] **Step 5: Commit**

```bash
git add scripts/gates/__main__.py scripts/gates/attestation.py scripts/gates/child_protocol.py scripts/gates/containment.py scripts/gates/runner.py scripts/governance/validate.py schemas/governance/child-result-v1.schema.json schemas/governance/check-result-v1.schema.json schemas/governance/gate-result-v1.schema.json schemas/governance/evidence-index-v1.schema.json tests/test_evidence_attestation.py tests/test_gate_runner.py tests/test_governance_schemas.py tests/test_network_containment.py
git diff --cached --name-only
git commit -m "feat(gates): add canonical fail-closed runner"
```

---

### Task 9: Normative G00–G20 executable catalog

**Classification:** `verification_content`

**Requirements:** every gate and requirement family.

**Files:**

- Create: `governance/gates.toml`
- Consume without editing: `tests/fixtures/governance/expected-gate-checks.toml`
- Extend: `tests/test_gate_manifest.py`

- [ ] **Step 1: Add the failing catalog completeness test**

```python
def test_exact_normative_gate_set() -> None:
    bundle = load_governance(
        ROOT, mode=ValidationMode.BOOTSTRAP,
        checkpoint=BootstrapCheckpoint.TASK_09,
    )
    assert {check.gate_id for check in bundle.checks} == {
        f"G{number:02d}" for number in range(21)
    }

def test_exact_child_assertions_and_bidirectional_trace() -> None:
    bundle = load_governance(
        ROOT, mode=ValidationMode.BOOTSTRAP,
        checkpoint=BootstrapCheckpoint.TASK_09,
    )
    expected = load_expected_checks(
        ROOT / "tests/fixtures/governance/expected-gate-checks.toml"
    )
    assert oracle_projection(bundle) == expected
    check_edges = {
        (check.check_id, requirement_id)
        for check in bundle.checks
        for requirement_id in check.requirement_ids
    }
    requirement_edges = {
        (check_id, requirement.requirement_id)
        for requirement in bundle.requirements
        for check_id in requirement.gate_check_ids
    }
    assert check_edges == requirement_edges
    assert clause_edges(bundle) == load_expected_gate_clauses(ROOT)

def test_permission_check_is_mandatory_and_state_is_externally_derived() -> None:
    check = find_check("G00-LEGAL-PERMISSION")
    assert check.required is True
    assert check.external_prerequisite is True
    assert not hasattr(check, "initial_state")
    assert legal_fixture_state("missing-review") is GateState.BLOCKED
    assert legal_fixture_state("missing-base-authority-key") is GateState.BLOCKED
    assert legal_fixture_state("unanchored-review-root") is GateState.FAIL
    assert legal_fixture_state("ambiguous-scope") is GateState.BLOCKED
    assert legal_fixture_state("forged-signature") is GateState.FAIL
    assert legal_fixture_state("base-anchored-complete-review") is GateState.PASS
    assert live_legal_state(ROOT) is GateState.BLOCKED
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src:. python -m unittest tests.test_gate_manifest -v`

Expected: missing gate catalog.

- [ ] **Step 3: Populate checks**

Each entry declares check ID, G00–G20 ID, exact requirement IDs and source
clauses, scheduled phase, closed applicability predicate, argv command, cwd,
timeout, required tools/ownership/version, expected artifacts, warning/skip
policy, pass criteria, and invalidation inputs. The independently reviewed
fixture freezes every required child assertion and mapping; equality is exact
and bidirectional to the independently frozen Task 2 clause inventory. Duplicate,
unknown, unresolved, document-wide, or digest-mismatched clauses fail. Phase 1
governance checks are scheduled. Later checks remain
`planned`. No placeholder child and no second namespace exists.

`G00-LEGAL-PERMISSION` has no editable state. Its result is derived only from
the restricted-source record, raw-artifact digest match, complete grant fields,
clean-implementer certifications, the release-authority key read from the
immutable governance base, a valid authority-signed trust-anchor receipt, an
exact anchored review-root fingerprint, and the authorized review signature and
disposition. Missing or ambiguous external proof yields `BLOCKED`;
contradictory, forged, substituted-root, expired, or noncanonical evidence
yields `FAIL`. Because this execution's governance base contains no release-
authority key, its live G00 result is unconditionally `BLOCKED`; synthetic
fixtures prove mechanics only and cannot make this subject pass.

The frozen child-ID inventory is:

```text
G00: G00-CLEAN-TREE, G00-REPOSITORY-HYGIENE, G00-PROVENANCE-INVENTORY,
     G00-RESTRICTED-EXPOSURE, G00-LEGAL-PERMISSION,
     G00-PRIVACY-SCOPE, G00-METADATA-SCHEMA-CONSISTENCY,
     G00-IMMUTABLE-ACTIONS
G01: G01-GRAMMAR-COMPILE, G01-FORMAT-RUFF, G01-STRICT-TYPES,
     G01-WARNINGS-AS-ERRORS, G01-SUPPRESSION-FILTER-AUDIT
G02: G02-UNIT-INTEGRATION, G02-COLLECTION-MANIFEST, G02-COVERAGE-THRESHOLDS,
     G02-CRITICAL-BRANCH-COVERAGE, G02-CHANGED-CRITICAL-MUTATION
G03: G03-DEPENDENCY-DAG, G03-IMPORT-BOUNDARIES,
     G03-INDEPENDENT-DISTRIBUTIONS, G03-ENGINE-PARITY
G04: G04-PUBLIC-API, G04-SCHEMAS, G04-DIAGNOSTIC-IDENTITY,
     G04-CLI-GOLDENS, G04-BREAKING-CHANGE-PROTOCOL
G05: G05-PR-MATRIX, G05-RELEASE-MATRIX, G05-INSTALLED-WHEEL-CELLS,
     G05-TARGET-GRAMMARS, G05-INTEGRATION-RANGES, G05-ALT-RUNTIME-TIERS
G06: G06-RULE-CONTRACTS, G06-LOCATIONS-REMEDIATION,
     G06-NONGOALS-FALSE-POSITIVES, G06-FIX-IDEMPOTENCE,
     G06-PRECISION-THRESHOLDS, G06-SAFETY-RECALL
G07: G07-DETERMINISTIC-GENERATORS, G07-HOSTILE-INPUTS,
     G07-INVARIANTS, G07-INCOMPLETE-FAIL-CLOSED, G07-MINIMIZED-SEEDS
G08: G08-CHANGED-CRITICAL-MUTANTS, G08-WHOLE-SUITE-MUTATION,
     G08-EQUIVALENT-MUTANT-REVIEW
G09: G09-LAYOUT-WORKFLOWS, G09-ANALYZER-FAILURES,
     G09-CONFIG-STDIN-REPORTS, G09-FIX-ROLLBACK-CONCURRENCY,
     G09-PARTIAL-NEVER-CLEAN
G10: G10-CORPUS-PROVENANCE, G10-PER-RULE-PRECISION,
     G10-ACCEPTED-FINDING-DELTAS, G10-RESOURCE-EVIDENCE,
     G10-BASELINE-REVIEW
G11: G11-SKILL-SCHEMA, G11-ROUTING-BUDGETS, G11-AUTHORITY-SAFETY,
     G11-PRESSURE-GUARDRAILS, G11-EVAL-MANIFEST,
     G11-DETERMINISTIC-SCORER, G11-MODEL-TRIALS
G12: G12-FORBIDDEN-CAPABILITIES, G12-PROCESS-SET-DENIAL,
     G12-CANARY-ZERO-ATTEMPT, G12-NETWORK-PARITY,
     G12-SECRET-NONLEAKAGE, G12-PLATFORM-CONTAINMENT,
     G12-EXTENSION-PROCESS-BOUNDARY
G13: G13-THREAT-MODELS, G13-HOSTILE-REPOSITORY,
     G13-PINNED-SUPPLY-CHAIN, G13-LOCAL-VULNERABILITY-DATA,
     G13-LICENSE-SBOM-PROVENANCE, G13-RESTRICTED-ARTIFACT-EXCLUSION
G14: G14-EXECUTABLE-DOCS, G14-CATALOG-DRIFT, G14-OFFLINE-LINKS,
     G14-PUBLIC-CLAIM-MAPPING, G14-FORBIDDEN-CLAIMS
G15: G15-ISOLATED-BUILDS, G15-ARTIFACT-CONTENTS,
     G15-INSTALL-EXTRAS-ENTRYPOINTS, G15-UNINSTALL,
     G15-REPRODUCIBILITY-IDENTITY
G16: G16-LSP-PROTOCOL, G16-LSP-RACES-LIFECYCLE, G16-LSP-POSITIONS-FRAMING,
     G16-EDITOR-PACKAGES-HANDSHAKE, G16-EDITOR-PRIVACY-TRUST
G17: G17-ACTION-CONTRACT, G17-FORK-PRIVILEGE-SAFETY,
     G17-TIMEOUT-CANCELLATION, G17-IMMUTABLE-PINS,
     G17-HOSTED-OUTPUT-DENIAL, G17-NO-TOKEN-NORMAL-SCAN
G18: G18-BENCHMARK-POLICY, G18-NATIVE-SCAN-BUDGETS,
     G18-ANALYZER-RESOURCE-BOUNDS, G18-LSP-BUDGETS,
     G18-REPEATED-RUN-PLATEAU
G19: G19-INDEPENDENT-ROLE-COVERAGE, G19-ZERO-CRITICAL-HIGH,
     G19-MEDIUM-EXCEPTIONS, G19-CANDIDATE-INVALIDATION
G20: G20-EVIDENCE-COMPLETENESS, G20-CANDIDATE-ARTIFACT-IDENTITY,
     G20-AUTHORIZED-DESTINATIONS, G20-REMOTE-TREE-PARITY,
     G20-POST-PUBLISH-SMOKE, G20-FINAL-CLAIM-AUTHORITY
```

`expected-gate-checks.toml` adds each ID's exact requirement edges, clause
digests, required/schedule state, expected artifact classes, and truth criteria;
`oracle_projection()` explicitly excludes executable argv/cwd/tool realization.
Task 9's command realization receives separate non-author security review.
Removing or adding a
child requires a separately reviewed normative-clause change, not a same-task
fixture edit.

- [ ] **Step 4: Verify and commit**

```bash
PYTHONPATH=src:. python -m unittest tests.test_gate_manifest -v
git add governance/gates.toml tests/test_gate_manifest.py
git diff --cached --name-only
git commit -m "docs(gates): freeze executable release catalog"
```

---

### Task 10: Instructions, adversarial review, and Phase 1 evidence

**Classification:** `verification_content`

**Requirements:** `ARC-04`, `QA-05`, `G00`, `G19`

**Files:**

- Create: `AGENTS.md`
- Create: `docs/audits/2026-07-14-phase-01-governance-review-process.md`
- Consume without editing: `docs/evidence/contracts/phase-01-governance.toml`;
  its v2 anchor binding was frozen in Task 2 and is immutable thereafter.
- Create: `schemas/governance/review-findings-v1.schema.json`
- Create: `tests/test_repository_instructions.py`

- [ ] **Step 1: Add failing instruction and review validators**

```python
def test_root_instructions_protect_normative_manifests() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for phrase in (
        "governance/ is normative",
        "Do not weaken gate applicability",
        "Do not process restricted reference material",
        "No telemetry or runtime networking",
    ):
        assert phrase in text

def test_normative_change_requires_review_contract() -> None:
    policy = load_instruction_policy(ROOT / "AGENTS.md")
    assert policy.protected_paths == (
        "AGENTS.md",
        "docs/PYTHON_DOCTOR_MASTER_PROMPT.md",
        "docs/design/proof-carrying-python-architecture.md",
        "docs/evidence/contracts/phase-01-governance.toml",
        "docs/governance/requirements-traceability.md",
        "docs/superpowers/plans/2026-07-14-python-doctor-phase-01-governance-foundation.md",
        "docs/superpowers/specs/2026-07-14-python-doctor-complete-parity-design.md",
        "docs/superpowers/specs/2026-07-14-python-doctor-validation-gates.md",
        "governance/", "schemas/governance/", "tests/fixtures/governance/",
    )
    assert policy.required_review_kinds == (
        "specification", "quality", "adversarial", "privacy_security",
        "gate_containment_verifier",
    )
```

- [ ] **Step 2: Verify RED, then write the minimum truthful instructions**

Run: `PYTHONPATH=src:. python -m unittest tests.test_repository_instructions -v`

Expected: missing `AGENTS.md` requirement fails.

- [ ] **Step 3: Run independent adversarial reviews**

Assign non-author reviewers to forged permission, missing requirements,
manifest weakening, unauthorized publication, false applicability, skill-count
inflation, shell/path/symlink injection, environment leakage, evidence tamper,
dirty identity, timeouts, and source/log publication. Every accepted finding
gets a validator or behavioral regression and re-review.

Required independent roles are specification, code quality, adversarial,
privacy/security, and gate/containment verifier. No author fills their own
required review role. Production subagents use context-free spawning and receive
only the hashed approved-input bundle; their LEG-06 certification is evidence.

Every finding is a `review-findings-v1` record with `finding_id`, `severity`,
`requirement_ids`, subject commit/tree, reviewer identity and independence
statement, evidence hash, disposition, prevention/regression path, resolution
commit, and re-review status. The review process document defines these fields;
the actual candidate-bound review remains sanitized evidence outside the subject
commit. A prose “approved” statement cannot satisfy G19.

- [ ] **Step 4: Commit the immutable review subject**

```bash
git add AGENTS.md schemas/governance/review-findings-v1.schema.json tests/test_repository_instructions.py docs/audits/2026-07-14-phase-01-governance-review-process.md
git diff --cached --name-only
git commit -m "docs(review): freeze phase one review contract"
git status --porcelain=v1
```

Expected: the subject candidate is clean. Any edit after this step creates a
new subject and invalidates prior review/evidence.

- [ ] **Step 5: Run the complete Phase 1 verification against the subject**

Developer-feedback commands (useful but not candidate evidence):

```bash
PYTHONPATH=src:. python -m unittest discover -s tests -v
PYTHONPATH=src:. python -m unittest discover -s evals -v
```

Candidate evidence commands:

```bash
PYTHONPATH=src:. python -m scripts.gates --validate-only
PYTHONPATH=src:. python -m scripts.gates --phase 1 --containment required --evidence-dir .evidence/phase-01
git diff --check
git status --porcelain=v1
```

Expected:

- all structural/behavioral tests and current evals pass;
- governance configuration is valid;
- the Phase 1 ledger proves every scheduled child across G00–G20 executed under
  containment or names the exact external blocker; an unexecuted child fails;
- G00 contributes `BLOCKED` for this execution because its immutable governance
  base lacks the release-authority key; external review files alone cannot
  change that state;
- every project-owned Phase 1 check passes; missing legal or containment
  authority remains explicitly `BLOCKED`, never skipped or green;
- no Phase 2 production implementation starts.

- [ ] **Step 6: Adversarially review the same immutable subject**

Store raw reviewer material under `.evidence/phase-01/raw/`. Store only
schema-valid redacted findings and result indexes under
`.evidence/phase-01/sanitized/`. Re-run affected checks after every accepted
finding. A fix changes the subject SHA, so restart Steps 4–6 for that new subject.

- [ ] **Step 7: Create the non-circular evidence binding**

Run `write_attestation_ref()` over the sanitized payload. Verify E1 contains no
raw logs/source/paths/secrets; E2 names the exact subject commit/tree and E1;
the ref name matches the subject; and the worktree remains clean. The local
`refs/python-doctor/evidence/*` namespace is not an authorized publication
destination and is never pushed without a separate destination grant.

## Phase exit

Phase 1 implementation tasks are complete only when Tasks -1 through 10 are independently
reviewed and every project-owned check passes. If the legal child is still
`BLOCKED`, Phase 1 gate state remains `BLOCKED`, the phase is not closed, and
Phase 2 is prohibited.

This execution's immutable governance base does not contain
`governance/trust/legal-release-authority-v1.pem`, so live G00 cannot become
`PASS` in this branch. Supplying review files later is insufficient. A future
authorized base-key addition requires a new protected-main base, new remote
execution anchor, new Phase 1 branch, and complete rerun/review.

The permission artifact must establish grantor identity/authority, date,
repository/revision scope, automated-AI permission, adaptation and Apache-2.0
redistribution scope, covered material types, conditions/attribution, immutable
artifact hash, and authorized human/legal disposition. The repository never
fabricates or commits the raw message.
