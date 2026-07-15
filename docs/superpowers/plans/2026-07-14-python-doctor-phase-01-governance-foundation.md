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

Post-commit acceptance parses the TOML with exactly the five declared keys,
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

- [ ] **Step 4: Obtain an independently controlled remote execution anchor**

Before Task 0, an authorized repository/release owner who is not a Phase 1
implementation author creates
`refs/heads/agent/phase-01-anchor-2026-07-14` at the exact Task -1 contract
addition commit. A GitHub ruleset must prevent Phase 1 authors from updating,
force-updating, or deleting that ref and must apply to administrators. The
independent owner queries the live ref and effective ruleset through GitHub,
then signs an offline `github-protected-ref-receipt-v1` payload. Editable
repository text, a local remote-tracking ref, unsigned JSON, and a self-authored
`independently_controlled = true` value are not proof of protection.

The receipt binds exact schema and purpose, repository
`shriyansh24/python-doctor`, ref name, anchor commit, base commit, contract blob
SHA-256, ruleset ID and canonical rules projection SHA-256, signer identity,
verification timestamp, expiry timestamp, and booleans proving force-update,
deletion, and direct Phase 1 author updates are denied and administrators are
covered. It is canonical closed JSON with duplicate/unknown-key rejection and
the signature domain prefix
`python-doctor/github-protected-ref-receipt/v1\0`. It expires after at most 24
hours and must be current when Task 0 starts; wrong repository/ref/commit/base/
blob/rules/purpose/signer, future or expired time, noncanonical bytes, or a bad
signature is `FAIL`.

Receipt production and verification belong to a trusted external facility named
`github-protected-anchor`, not to any repository script or caller-selected
executable. The facility runs in an independently attested immutable execution
environment, authenticates to GitHub with read-only ref/ruleset access, pins its
GitHub API and cryptographic toolchain identities, and signs the canonical
provider result with a platform-managed key unavailable to Phase authors. Its
result binds the receipt fields above, provider/environment/toolchain identity,
query time, expiry, subject commit/tree, and facility schema version. The
orchestrator verifies the provider signature and freshness before dispatching
Task 0; a Phase process never queries GitHub, selects a trust key, verifies its
own provider result, or promotes a cached/local JSON file.

The orchestration-owned interface is
`TrustedFacilityAccessor.get_pass("github-protected-anchor",
required_projection) -> TrustedExternalFacilityResult`. `get_pass` returns only
a fresh authenticated `PASS`; it raises typed `ExternalFacilityBlocked` or
`ExternalFacilityFailed` for the states below. Repository modules cannot import,
construct, deserialize, or shadow the opaque accessor/result capability.
`TrustedExternalFacilityResult` freezes `facility_id`, `provider_instance_id`,
`provider_attestation_digest`, `schema_version`, `repository`, `ref`,
`anchor_commit`, `base_commit`, `contract_blob_sha256`, `ruleset_id`,
`rules_projection_sha256`, `force_update_denied`, `deletion_denied`,
`phase_author_update_denied`, `administrators_covered`, `queried_at`,
`expires_at`, and `signed_result_digest`. Trust comes from the platform-verified
capability envelope, never from a boolean field inside repository data.

Provider result state is exact: absent facility, unavailable GitHub authority,
or absent ref/ruleset evidence is `BLOCKED`; malformed, mismatched, stale,
forged, unprotected, or noncanonical evidence is `FAIL`; only a fresh valid
provider result is `PASS`. Task 2 receives the already authenticated typed
provider result through the orchestration control plane and binds its digest to
the candidate `CheckResult`; it does not load a path, invoke a local verifier,
or accept `independently_controlled` from repository data. Every later identity
check requires the same provider-result digest or a newer fresh result with the
same stable projection.

The currently available GitHub connection can read/write refs but exposes no
ruleset query and no independently attested provider-result signature. Therefore
the `github-protected-anchor` facility is unavailable in this execution: Task -1
is `BLOCKED` and Task 0 must not begin. A future environment may proceed only
after that external facility is provisioned and independently reviewed; local
PATH pinning, repository keys, or self-authored bootstrap code are not accepted
as substitutes.

Task 2 and every later identity check compare the immutable five-field
projection and contract-introduction commit to the authenticated external
provider result, not merely to the current local history. Rewriting or replaying local
commits cannot substitute a new base. A deliberate later execution from a newer protected
`main` requires a newly named anchor, a new Phase 1 branch, and fresh execution
and review; it is not a continuation of this run.

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

- [ ] **Step 1: Write and prove the RED oracle validator**

The standalone standard-library validator rejects missing files, duplicate/
blank/unknown IDs, wrong 105/198/9 counts, invalid TOML shape, unresolved source
paths/sections, normalized clause-digest mismatch, missing G00–G20 children,
non-bidirectional requirement/clause edges, and truth criteria outside the
closed registry. Run it before fixture creation and record the expected missing-
oracle failure.

Run: `PYTHONPATH=src:. python -m unittest tests.test_governance_oracles -v`

- [ ] **Step 2: Assign independent specification authors**

Use context-free non-implementation agents. One derives requirement, skill,
profile, provenance, and clause inventories directly from the immutable control
documents; another reviews exact equality, normalized clause digests, the
105/198/9 counts, source entries, and the complete G00–G20 child/truth-criteria
inventory. They do not author the manifests or runner.

- [ ] **Step 3: Verify GREEN and freeze the oracle commit**

The oracle includes child IDs, required flags, clause/requirement edges, and
truth criteria, but no executable command realization. The review records source
document digests and all dispositions. Commit these exact files before Task 1.

```bash
PYTHONPATH=src:. python -m unittest tests.test_governance_oracles -v
git add scripts/__init__.py scripts/governance/__init__.py scripts/governance/validate_oracles.py tests/test_governance_oracles.py tests/fixtures/governance/expected-requirement-ids.txt tests/fixtures/governance/expected-skill-ids.txt tests/fixtures/governance/expected-profile-domain-ids.txt tests/fixtures/governance/expected-provenance-sources.toml tests/fixtures/governance/expected-gate-clauses.toml tests/fixtures/governance/expected-gate-checks.toml docs/audits/2026-07-14-governance-oracle-review.md
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

- Produces: `GateState`, `RequirementSpec`, `GateCheckSpec`, `GovernanceBundle`,
  `Violation`, `load_governance()`, and `validate_governance()`.
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

**Interfaces:**

- Consumes: `load_governance()` and `validate_governance()`.
- Produces: canonical `RequirementSpec` records referenced by every task/gate.

- [ ] **Step 1: Write the failing completeness validator**

```python
def test_manifest_matches_independently_frozen_id_set() -> None:
    requirements = load_requirements(ROOT / "governance/requirements.toml")
    lines = (ROOT / "tests/fixtures/governance/expected-requirement-ids.txt").read_text(encoding="utf-8").splitlines()
    assert len(lines) == len(set(lines)) == 105
    assert all(line and not line.startswith("#") for line in lines)
    expected = frozenset(lines)
    assert {item.requirement_id for item in requirements} == expected

def test_requirement_state_is_derived_not_authored() -> None:
    requirements = load_requirements(ROOT / "governance/requirements.toml")
    assert all(not hasattr(item, "release_status") for item in requirements)
    assert all(not hasattr(item, "current_phase_status") for item in requirements)

def test_every_source_clause_resolves_to_frozen_digest() -> None:
    requirements = load_requirements(ROOT / "governance/requirements.toml")
    registry = load_clause_registry(ROOT / "governance/clause-registry.toml")
    assert all(registry.resolves(clause) for item in requirements for clause in item.source_clauses)

def test_task_minus_one_base_binding_is_immutable() -> None:
    contract = load_phase_contract(ROOT / "docs/evidence/contracts/phase-01-governance.toml")
    introduction = unique_addition_commit("docs/evidence/contracts/phase-01-governance.toml")
    anchor = SyntheticAnchorProjection(
        state="PASS",
        ref="refs/heads/agent/phase-01-anchor-2026-07-14",
        anchor_commit=introduction,
        force_update_denied=True,
        deletion_denied=True,
        phase_author_update_denied=True,
        administrators_covered=True,
    )
    assert validate_anchor_projection(anchor) == ()
    original = load_phase_contract_from_git(introduction)
    assert immutable_base_projection(contract) == immutable_base_projection(original)
    assert commit_parent(introduction) == contract.governance_base_commit
    assert git_tree(contract.governance_base_commit) == contract.governance_base_tree
    assert is_ancestor(contract.governance_base_commit, "HEAD")
```

`SyntheticAnchorProjection` is test-only and exercises pure field validation;
it is deliberately incapable of satisfying the live trust gate. The live
`get_pass` call is an orchestration precondition outside ordinary unittest
discovery and must already have succeeded before Task 0 was dispatched. Task 2
binds the orchestrator-provided result digest during evidence assembly but does
not fetch or manufacture the capability in repository tests.

- [ ] **Step 2: Verify the validator fails because the manifest is absent**

Run: `PYTHONPATH=src:. python -m unittest tests.test_requirements_manifest -v`

Expected: missing `governance/requirements.toml`.

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

`validation-inputs.toml` is the sole versioned identity inventory. It lists the
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

The base-binding validator reads the contract's unique Git addition commit,
requires exact equality with the live independently controlled protected anchor,
and compares the current five-field immutable projection to that anchored blob.
It rejects multiple addition commits, an absent/unprotected/movable anchor, a
non-base parent, a changed base commit or tree, a base/tree mismatch, missing
ancestry, or a rewritten/replayed local history. Hashing only the current
editable contract is insufficient and must never be used as the immutability
proof. Missing external anchor/ruleset evidence is `BLOCKED`, never `PASS`.

- [ ] **Step 4: Verify GREEN and regression**

Run:

```bash
PYTHONPATH=src:. python -m unittest tests.test_requirements_manifest -v
PYTHONPATH=src:. python -m unittest discover -s tests
```

Expected: all tests pass with no missing family, gate, artifact, or test mapping.

- [ ] **Step 5: Commit**

```bash
git add governance/clause-registry.toml governance/requirements.toml governance/toolchain.lock.toml governance/validation-inputs.toml tests/test_requirements_manifest.py docs/evidence/contracts/phase-01-governance.toml
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
    anchor = destination(manifest, "github-phase-01-protected-anchor")
    assert anchor.state == "permitted"
    assert anchor.ref_pattern == "refs/heads/agent/phase-01-anchor-2026-07-14"
    assert anchor.purpose == "immutable_phase_01_execution_anchor"
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

Within the agent-ref allowance, add an exact permitted record
`github-phase-01-protected-anchor` for
`refs/heads/agent/phase-01-anchor-2026-07-14` with purpose
`immutable_phase_01_execution_anchor`. It may point only to the verified Task -1
contract-addition commit, may not be used for releases or artifacts, and is
valid only with the independently controlled ruleset and signed offline receipt
specified in Task -1. A similarly named or unprotected ref is denied.

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
environment identity. The validation-input digest is the canonical hash of every
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
- Update: `docs/evidence/contracts/phase-01-governance.toml`
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
git add AGENTS.md schemas/governance/review-findings-v1.schema.json tests/test_repository_instructions.py docs/audits/2026-07-14-phase-01-governance-review-process.md docs/evidence/contracts/phase-01-governance.toml
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
