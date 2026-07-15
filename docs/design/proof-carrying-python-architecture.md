# Proof-Carrying Python Doctor Architecture

**Status:** Subordinate design amendment adopted under the user's originality
direction; implementation remains gated by G00 and the primary specification

**Origin:** Independently authored from the approved clean-room Python
requirements and public Python engineering concepts. Prior exposure to the
restricted reference is recorded in the provenance process; no restricted
expression is intentionally reused. This is an auditable originality statement,
not a legal conclusion.

## 1. Defining idea

Python Doctor is not a bundle of linters behind one command. Its defining
contract is:

> Every conclusion is a local claim with an inspectable evidence chain, an
> explicit analysis boundary, a coverage state, and a verification path.

Python's dynamic behavior makes this separation essential. A property may be
established within documented limits, contradicted, unresolved, inapplicable,
or not evaluated. Python Doctor preserves that distinction instead of flattening
uncertainty into a warning count or opaque score.

## 2. Alternatives considered

1. **Proof-carrying capability graph — selected.** It makes incomplete analysis,
   disagreement, safety evidence, skill routing, and verification explicit.
2. **Conventional scanner pipeline with richer messages — rejected.** It is
   easier initially but cannot honestly represent provider conflicts or absence
   of evidence.
3. **Policy-as-code assurance engine — rejected as the default.** It is useful
   for regulated environments but too enterprise-specific for ordinary Python
   development.

## 3. Execution model

```text
repository snapshot
      ↓
project discovery
      ↓
capability-plan resolver
      ↓
native examiners + sandboxed adapters
      ↓
evidence ledger
      ↓
claim/verdict engine
      ↓
claim envelopes + assurance map
      ↓
reports, skills, fixes, API, LSP, and editors
```

Core responsibilities are divided by Python analysis need:

- `snapshot`: immutable, root-contained file and metadata view;
- `discovery`: versions, layouts, package roles, frameworks, generated/vendor
  regions, configuration, and source-selection facts;
- `capabilities`: questions and guarantees Python Doctor can examine;
- `planning`: deterministic provider and resource plan frozen before execution;
- `examiners`: token, AST, binding, symbol, control-flow, metadata, and project
  analysis;
- `adapters`: approved local tools behind the analyzer airlock;
- `evidence`: observations, derivations, conflicts, and invalidation;
- `verdicts`: claim-state evaluation without hiding uncertainty;
- `diagnostics`: stable actionable claim envelopes;
- `policy`: profiles, severity, exceptions, and blocking;
- `privacy`: sinks, environment stripping, containment, and network denial;
- `reports`: immutable result serialization.

## 4. Examination capsule

Every run begins by freezing an examination capsule containing:

- normalized root-relative file inventory and content digests;
- target Python versions;
- configuration digest;
- selected profile and source-selection mode;
- analyzer identities and versions;
- capability-plan digest;
- resource and privacy policy digests;
- schema versions.

The result refers to the capsule digest. This makes cache invalidation,
determinism, baseline comparison, and evidence identity explainable. The default
evidence store is memory-only. Persistent cache, report, or fix journal requires
an explicit destination. Fingerprints never contain source text, absolute paths,
repository names, usernames, hostnames, or environment values.

Fix preview uses an ephemeral in-memory transaction. `fix --apply` creates a
root-contained temporary journal for crash recovery and removes it after
verified success. Retained rollback requires an explicit `--journal` destination
outside the scanned tree unless the user deliberately selects a contained path.
Journal contents are local, checksummed, permission-restricted, and never
uploaded; recovery refuses a journal whose capsule or preimage digests differ.

Native examiners consume the in-memory snapshot. An external adapter receives a
contained snapshot copy when supported. Otherwise Python Doctor verifies every
input digest immediately before and after the adapter and marks the result
incomplete on concurrent change. A capsule never claims immutability while a
provider reads an unchecked mutable working tree.

## 5. Capability graph

Each capability asks one bounded question, for example:

- can the declared Python grammar be parsed completely;
- can local symbol bindings be resolved;
- is a coroutine result consumed;
- does a retry loop have an enforceable bound;
- are public API documentation contracts present;
- is package metadata internally consistent;
- is a comment contradicted by observable code structure.

Every node declares:

- capability ID and question;
- applicability predicate and admissible applicability evidence;
- required evidence classes and candidate providers;
- dependencies, conflicts, and invalidation edges;
- soundness boundary and failure policy;
- associated rules and remediation skills.

Typed edges are `requires`, `refines`, `corroborates`, `conflicts_with`,
`invalidates`, and `remediated_by`.

Capability obligation is `required` or `optional`. Its independent plan
disposition is `selected`, `not_selected`, or `not_applicable`; a capability can
therefore be both required and selected. `not_applicable` requires admissible
facts, and a required capability cannot become `not_selected`.
Provider results are `complete`, `partial`, `unavailable`, `failed`, and
`skipped`. A selected skipped provider is incomplete; only `not_selected` leaves
completeness unchanged.
Installed-tool accidents cannot silently change the plan. Provider disagreement
is retained as evidence instead of overwritten by completion order.

Provider choice freezes from profile/configuration before availability checks.
An unavailable provider stays unavailable. Another installed tool may replace
it only through a versioned predeclared fallback recorded in the capsule.

## 6. Evidence and verdict calculus

Keep four axes independent.

### Internal claim state

- `established`
- `contradicted`
- `unresolved`
- `not_applicable`
- `not_evaluated`

The public safety schema remains `satisfied`, `violation`, `unproven`,
`not_applicable`, and `not_evaluated`:

| Internal claim | Public safety state |
|---|---|
| `established` with complete coverage, every required subclaim established, admissible safety evidence, and no unresolved/conflicting counterevidence | `satisfied` |
| `contradicted` | `violation` |
| `unresolved` | `unproven` |
| `not_applicable` with admissible applicability evidence | `not_applicable` |
| `not_evaluated` | `not_evaluated` |

Heuristic-only evidence never maps to `satisfied`.

### Coverage

- `complete`
- `limited`
- `failed`

### Evidence method

- `direct`: syntax or metadata observation;
- `derived`: deterministic semantic/control-flow inference;
- `corroborated`: independent evidence supports the claim;
- `heuristic`: measured judgment with explicit limitations;
- `human`: approved scoped determination.

### Inference confidence

- `high`
- `medium`
- `low`
- `not_calibrated`

Confidence never substitutes for completeness or proof. A high-confidence
heuristic cannot establish a required safety property.

The public Python Doctor inference confidence is this ordinal value. A provider's
native numeric or categorical confidence is preserved separately as raw evidence
with provider/version provenance and never silently converted into Python
Doctor's calibrated confidence.

Each evidence atom records its observation code, producer/version, normalized
location, input digest, completeness, derivation parents, soundness boundary,
and invalidation conditions. Derivation-parent edges form an acyclic graph.
Symmetric/general relations such as `conflicts_with` live in a separate relation
graph and may contain cycles. Root observations legitimately have no parents;
“orphan” means evidence unreachable from every claim. Derivation cycles,
unreachable non-root evidence, contradictory terminal states, or conclusions
without admissible evidence fail schema validation.

Identity is versioned and domain-separated. Canonical objects serialize as
UTF-8 JSON with sorted keys, compact separators, exact integers only, no NaN or
infinity, and one trailing newline. Every digest hashes
`b"python-doctor/" + artifact_kind + b"/v1\0" + canonical_bytes` with SHA-256.
Filesystem identities use contained root-relative raw path bytes encoded as
hex plus entry type, mode, size, and content digest; display normalization is
never an identity input. Evidence-atom identity hashes the capsule, producer,
observation, subject/location, boundary, parents, and invalidation contract.
Stable occurrence fingerprints hash fingerprint-schema version, rule/claim ID,
normalized relative semantic subject anchor, and the rule's span policy. The
capsule/result digest scopes lookup and evidence instances but is not part of
the stable fingerprint, so unrelated repository/configuration changes do not
rename unchanged findings. If one digest is observed with
different canonical bytes, validation stops with internal failure rather than
merging the records. Schema and hash-domain versions are explicit migration
boundaries.

## 7. Claim envelope

Every actionable diagnostic contains:

- **Observation:** what was found;
- **Interpretation:** why it matters;
- **Evidence:** facts and derivations;
- **Boundary:** what could not be determined;
- **Impact:** correctness, security, maintainability, performance, or safety;
- **Remediation:** the smallest appropriate response;
- **Verification:** trusted-registry recipe or condition that discharges the
  claim;
- **Skill prescription:** focused remediation skill IDs;
- **Fix authority:** none, previewable safe fix, or agent-assisted;
- **Suppression contract:** required reason, scope, ownership, and expiry.

Example shape:

```text
PD-NAME-014  medium  src/orders.py:48
Boolean `ready` does not reveal readiness for what.

Observed:
  The value gates shipment submission and is assigned from three checks.

Boundary:
  Cross-process state is not visible to static analysis.

Candidate:
  `is_ready_for_submission`

Prescription:
  naming-python → boolean predicates → domain state
```

`python-doctor explain <occurrence-fingerprint> --result <local-result>`
traverses one occurrence envelope within an explicit result/capsule, with
`--evidence` and `--verification` projections. `rules explain` remains the
separate rule-contract surface.

Verification recipes are structured argv arrays from a shipped trusted
registry. Scanned text and analyzer messages never define them, and Python
Doctor never executes a recipe automatically.

## 8. Outcome and assurance map

Present three separate results:

1. outcome: clean, findings, incomplete, or internal failure;
2. examination coverage: required, evaluated, unavailable, and unresolved;
3. health score: versioned deductions available only for complete comparable
   scans.

The primary summary is an assurance map:

```text
Correctness       18/18 capabilities evaluated; 2 findings
Typing            incomplete: required provider unavailable
Security          12/12 capabilities evaluated; no findings in evaluated scope
Maintainability   5 findings, 2 heuristic
Safety            2 required properties unresolved
```

Baseline comparisons show claim transitions: newly contradicted, newly
established, still unresolved, coverage gained/lost, evidence invalidated, and
finding discharged.

## 9. Local-only privacy by construction

Core/API runtime packages contain no HTTP, cloud, telemetry, updater, remote
configuration, downloader, or report-upload capability. There is no telemetry
or offline setting because runtime networking does not exist.

All external analyzers pass through one airlock that:

- accepts registered executables and argument templates only;
- never invokes a shell;
- uses trusted temporary configuration;
- runs from an isolated working directory, passes explicit no-config or trusted
  config arguments, disables tool-specific plugin/autoload mechanisms, and
  receives snapshot-contained inputs only;
- strips proxy, credential, token, cloud, Git, and package-index environment;
- disables plugins, hooks, external diff/textconv, remote includes, and project
  code loading;
- enforces process-tree, time, memory, file, and output limits;
- confines reads/writes to declared roots and temporary space;
- applies OS-level network denial and observation.

If a required boundary cannot be enforced, the provider is unavailable or the
gate is blocked according to the normative gate rules; isolation is never
silently weakened.

The compatibility manifest names an accepted containment backend for each
required platform. Linux uses a network namespace plus process-group and
resource controls. macOS and Windows require separately validated OS-level
process-tree deny/observation backends. If a backend is absent or cannot enforce
an adapter's controls, that adapter is unavailable; canaries alone are not a
containment backend.

The engine returns values only. Explicit CLI sinks are terminal/stdout, a
user-named local file, or a user-authorized fix transaction. A local privacy
receipt records sink kind plus a redacted/digested destination descriptor and
sandbox posture, never the raw path or repository identity.

## 10. Capability-to-skill prescription graph

Skill routing uses task intent, affected artifacts, repository facts,
capability gaps, profile/risk, mutation authority, and context budget—not
keyword matching.

```text
intent → repository profile → capability gap → narrow leaf skills
```

Every route emits a local receipt naming selected/excluded modules, reasons,
prerequisites, conflicts, context cost, authority, and evaluation IDs. One
router plus at most five leaves load by default. Finding-linked skills remain
identifiers until remediation is requested. Read-only diagnosis never activates
mutation, and a skill cannot elevate its own authority.

Skills are classified as examination, explanation, intervention, or
verification skills. This lets main skills invoke naming, comment/docstring,
self-explanatory-code, safety, or framework extensions only when evidence makes
them applicable.

## 11. Safety as mini assurance cases

Each Python Power-of-Ten adaptation is a claim-argument-evidence case:

```text
safety claim
 ├── applicability evidence
 ├── required subclaims
 ├── admissible evidence
 ├── derivation and counterevidence
 ├── residual uncertainty
 └── scoped exception, if approved
```

For bounded retries, evidence covers maximum attempts/deadline, per-attempt
timeout, capped backoff, cancellation/shutdown, bounded queued work, and
exception paths. `contradicted`, `unresolved`, `not_evaluated`, and unsupported
required properties block. `not_applicable` needs admissible evidence.
`established` needs rule-specific evidence, never confidence alone. Empirical
measurements corroborate but cannot independently establish a static guarantee.

The product says “established within documented analysis limits,” never
“certified,” “NASA compliant,” or “proved safe.”

## 12. Originality safeguards

Even with permission, originality remains a release requirement:

- archive the permission artifact, sender authority, scope, revision, AI-use,
  derivative, redistribution, and sublicensing terms;
- quarantine the previously inspected checkout and record its exposure ledger;
- provide implementation agents only approved requirements, public standards,
  and this independently authored architecture;
- record every task origin as user requirement, public standard, independent
  design, or compatible attributed OSS;
- author Python truth tables before rules and generate fresh synthetic fixtures;
- do not mirror reference file counts, names, command symmetry, prose cadence,
  visual assets, fixture domains/order, or one-to-one package boundaries;
- justify packages and UX from Python user stories and analysis needs;
- allow direct restricted-source comparison only by an authorized human/legal
  reviewer.

Originality review applies:

1. an origin audit over requirements, code, rules, tests, messages, and UX;
2. the Python-necessity test: could this component be derived without the
   reference project;
3. independent-origin and Python-necessity review without consulting restricted
   source; direct similarity review is reserved for an authorized human/legal
   reviewer;
4. fresh-fixture and language-fingerprint review;
5. at least two rejected alternatives for major architectural choices;
6. adversarial tests for heuristic-as-proof, hidden coverage loss, analyzer
   conflict, hostile configuration, network access, leakage, authority
   escalation, unsafe exceptions, incomplete scores, nondeterminism, and
   concurrent-change fixes.

## 13. Acceptance criteria

- every diagnostic traces to evidence and a soundness boundary;
- every absence-of-finding claim has completed planned coverage;
- provider conflicts remain visible;
- safety satisfaction never derives from heuristic confidence alone;
- CLI, API, LSP, editors, and Action use one engine result;
- native scanning remains functional with networking denied; selected adapters
  either run under enforced denial or fail closed;
- project-owned shipped runtime code contains no networking implementation or
  import, and each shipped runtime dependency closure has no reachable
  networking call path from a product entry point; exceptions are prohibited
  unless independently proven unreachable and reviewed;
- skill routes are deterministic, budgeted, explainable, and authority-safe;
- provenance explains every major element's origin;
- users can distinguish healthy, not examined, and unresolved at a glance.
