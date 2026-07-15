# Python Doctor engineering handover

Status date: 2026-07-15 (America/Chicago)

This document is the authoritative continuation guide for the current clean-room
Python Doctor effort. The repository is **not complete or release-ready**. The
active work is intentionally kept on a draft pull-request branch, and the most
advanced Task 0 implementation is preserved on a separate archive branch.

## Non-negotiable project constraints

- The implementation must be independently written. Do not copy or mechanically
  port source files from React Doctor.
- The permission screenshot supplied by the requester states or purports to
  authorize a clean-room Python adaptation and asks for attribution, Apache-2.0
  licensing, and distinct branding. The screenshot does not independently
  authenticate the sender, so legal gate G00 remains `BLOCKED`.
- Do not inspect restricted upstream source while G00 is blocked. High-level
  concepts may be researched from independently available Python sources.
- There must be **no project telemetry**: no analytics, usage reporting, update
  checks, runtime uploads, hidden network calls, or persisted credentials.
  GitHub-hosted CI necessarily produces provider job logs and status metadata;
  that infrastructure behavior is not application telemetry and must be
  described honestly.
- Do not claim that in-process Python validation is a security sandbox. The gate
  detects accidental and named non-self-restoring mutations. Intentionally
  adversarial repository code with arbitrary same-interpreter introspection and
  monkey-patching is outside its guarantee.

## Published repository state before this handover

- Repository: `shriyansh24/python-doctor`
- Default branch: `main`
- Governance pull request: `#2` (draft)
- Published governance branch before this handover:
  `d3d66e2b45dafd2c65e49ff80d344f6bcc470fad`
- Immutable Phase 1 contract blob:
  `405e2450d4a5e3e5a82f6f16cdbb5228f40f8058`
- Contract raw SHA-256:
  `d65ee5af0c308d3b1a37f0d83e1bd2714b2ac41f018a30af121db6e54371548c`

## Work completed locally after the published anchor

The active branch contains seven linear, plan-only governance amendments after
`d3d66e2...`:

1. `70e380382c713297dad31a75d79c90f52c48438c` — close oracle gate coverage
2. `0f8c4a983eeaf9df60d0a7c1c57b9a99ae12b8ae` — isolate oracle startup
3. `a22b65ffe586724d73329d838b3c71c43bf35e59` — supervise oracle stages
4. `619a72dec88141de859c8da1ceb9ca50e5c36b07` — close import-cache bypasses
5. `fdae2733f8b98860fb502a5e679930dea54bc2ee` — bind import identities
6. `2f69ac4be1d4efb53973812c451967e41c962edd` — close identity bypasses
7. `c23ef439ad9770ad8db4f97d857a7122d60fd7ae` — close completion bypasses

The seventh commit has tree
`0cfc3eff73e986df428f88edf9e0d1f4ca370e61`, plan blob
`6d700dd05e8bc88a9af52ef29adf23033bfa1a41`, and raw plan SHA-256
`026e3fa511a4a1d6ce10dbe648d2a539839fa38ad058faa7596989f62f062193`.
The contract blob is unchanged across the chain.

The amendments specify and test:

- all-PR and branch-restricted push CI triggers without path filters;
- pinned GitHub Actions and a Windows CPython 3.9–3.14 matrix;
- zero telemetry, uploads, caches, runtime installs, and persisted credentials;
- a closed Python 3.9/3.10 fallback grammar for the exact governance fixtures;
- isolated `python -I -B -X utf8 -S` trusted supervisors and stage children;
- exact unittest inventories, counts, zero skips, zero expected failures, and
  zero unexpected successes;
- bounded no-follow snapshots of all 12 Task 0 artifacts;
- exact module, loader, finder, cache, origin, package-path, and state-container
  invariants, including CPython baseline aliases and zip-member binding;
- nonce-bound stage completion evidence and distinct nonzero success sentinels;
- explicit limitations for intentionally hostile same-interpreter code.

Latest local author-run evidence for the seventh amendment:

- archived Task 0 simulated mandatory test: 1/1 pass;
- archived Task 0 full suite: 52/52 pass;
- validator: pass;
- exactly three stage evidence sentinels;
- clean parent exit: 0;
- five newly reproduced bypasses fail closed with exit 94;
- internal adversarial review: PASS with no residual Critical/Important finding;
- Python 3.9 grammar/static checks: pass;
- workflow/local child parity SHA-256:
  `0fcc3d2a6ea828de071d22e4faed9841d6cd3dbee525c4026d4433d4bb1c7a62`.

This evidence is ephemeral: it is reported from the authoring session but is not
yet captured in a tracked transcript or a sealed external evidence generation.
Rerun it and preserve the exact commands, stdout/stderr, environment identity,
and digests before using it as approval evidence.

Important: the seventh amendment has **not** received the two fresh root-level
reviews that must precede implementation replay. Treat it as a reviewed draft,
not an approved execution anchor.

## Preserved Task 0 implementation candidate

Archive commit:
`254cf3680596c6e52954b63d8c5a8894adc8f126`

Recommended remote archive branch:
`archive/phase-01-task00-pre-gate-reanchor-254cf3680596`

At handover creation this commit and branch are **local only**; no matching
`origin/` ref exists. Publish the archive ref explicitly to preserve it on
GitHub, without merging it or presenting it as an approved candidate.

It contains exactly 12 files and 4,495 added lines:

- `.github/workflows/governance-oracles-windows.yml`
- `docs/audits/2026-07-14-governance-oracle-review.md`
- `scripts/__init__.py`
- `scripts/governance/__init__.py`
- `scripts/governance/validate_oracles.py`
- six exact governance fixture inventories under `tests/fixtures/governance/`
- `tests/test_governance_oracles.py`

This candidate passed 52 tests, the validator, and prior spec review, but it is
superseded as an execution candidate. Do not merge or cherry-pick it directly.
Replay its exact intended files with `apply_patch` onto the final published
governance anchor, then apply the latest parser/workflow corrections and rerun
all gates.

## Existing Python Doctor implementation

The repository already contains an independently written Python package scaffold
under `src/python_doctor/` with CLI, configuration, discovery, scanner, scoring,
diagnostics, policy, fingerprinting, report writers, native rules, and Bandit,
Radon, and Ruff adapters. It also contains unit tests and architecture/design
plans. This code predates completion of the Phase 1 governance sequence and must
be revalidated against the final requirements contract before any release claim.

## Required next actions, in order

1. Run two fresh independent reviews over
   `d3d66e2...c23ef43`: one requirements/spec review and one adversarial review.
   Fix Critical/Important findings as new linear plan-only children.
2. Publish the final reviewed Task -1 chain without force-pushing. Confirm the
   remote tree, plan blob/raw hash, contract blob, PR changed-file set, and
   single-parent ancestry through the GitHub connector. Update PR #2's stale
   body (which still names `7af67cc...` as the final anchor) with the actual
   remote anchor, review status, and incomplete/draft disposition.
3. Stage the connector-created remote projection and complete author inventory
   outside the sealed generation. Obtain fresh non-author spec and adversarial
   reviews of those exact remote objects; local reviews do not approve
   connector-created SHAs, which can differ from local commit IDs. Create the
   review transcript, compute and assemble the exact three-file immutable sealed
   generation, and only then atomically replace `live-generation.json`. Never
   overwrite or move earlier generations. Finally create a fresh Task 0 dispatch
   outside the sealed generation and execute the exact acceptance block.
4. Replay the preserved 12-file Task 0 candidate onto that exact remote anchor
   using `apply_patch`. Apply the final closed parser and supervisor workflow.
5. Run the full multi-version/static gate, all tests with exact inventory and
   zero non-pass dispositions, validator, no-telemetry scan, spec review, and
   adversarial review. Publish Task 0 only after both reviews pass.
6. Complete Phase 1 Tasks 1–10 from the governance plan: manifests, provenance,
   NASA-rule adaptation, naming/comment/docstring policies, security and
   complexity checks, containment, gate runner, repository instructions, and
   release evidence.
7. Expand the skills library and main router for naming functions/variables,
   comments and self-explanatory code, architecture, typing, testing, packaging,
   async/concurrency, data/scientific Python, web frameworks, CLIs, databases,
   security, performance, observability without telemetry, notebooks, and
   migration/modernization. Every extension needs a focused `SKILL.md`, trigger
   contract, tests/evals, and routing from the main skill.
8. Translate the supplied NASA/JPL ten C rules into evidence-backed Python rules.
   Preserve the original document as a cited input; distinguish direct
   translation from Python-specific judgment and avoid claiming NASA endorsement.
9. Finish README, installation, quick start, configuration, report examples,
   contributing/security policies, Apache-2.0 license/NOTICE, clean-room
   attribution, changelog, and release checklist.
10. Treat legal G00 as permanently unable to PASS on the current lineage. The
    immutable base `3080b2a11e147bd7aa27f85b2750fdd4cf66ab00` does not contain
    `governance/trust/legal-release-authority-v1.pem`; external review files or
    an authenticated message alone cannot repair that ancestry. Authenticated
    rights-holder authorization is necessary, but a PASS also requires a new
    protected-main base containing the independently authorized key, a new
    remote anchor and Phase 1 branch, and a complete rerun/review from that base.
    Until then, do not inspect restricted upstream source, begin Phase 2, or make
    parity claims. Keep the project name and branding distinct.

## Handover publication actions

Before closing this handover, publish preservation refs without force:

1. Do **not** commit this document to or advance
   `agent/phase-01-governance`. That branch has a strict plan-only descendant
   invariant and may move only after both required local reviews pass.
2. Create and push a separate preservation branch named
   `handover/python-doctor-2026-07-15` containing the current linear Task -1
   draft commits plus this document. It is not an execution anchor or merge
   candidate.
3. Push local ref
   `archive/phase-01-task00-pre-gate-reanchor-254cf3680596` to the identically
   named remote archive branch.
4. Fetch both preservation refs back and compare their remote commit/tree/file identities to
   the intended local objects. Record any connector-created SHA differences.
5. Keep PR #2 open and draft at its existing reviewed remote head until the
   plan-only review/publish protocol is resumed.
6. Do not merge either preservation branch and do not call the handover a
   release.

## Completion definition

Do not call the project complete until all required skills and rules are present,
all unit/integration/eval/fixture/CLI/packaging/Windows checks pass with zero
skips or expected failures where prohibited, both final reviews pass, the
no-telemetry scan is clean, documentation and licensing are complete, GitHub CI
is green, and the exact reviewed commits are present on the intended remote
branch without force-push divergence.
