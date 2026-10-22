# Shared patterns

Methods our projects share, as forms with their instances and lessons: shared method, not shared code. Each project keeps its own implementation; before building one of these, read its entry and start from the form and the lessons, not from scratch. PATTERNS.md is rendered from this file (python3 tools/patterns.py --write); tools/check.py refuses a hand-edited PATTERNS.md, and `python3 tools/patterns.py --locate ~/Projects` checks every instance path in local checkouts.

- [Claims are the source; documents are views](#claims-are-the-source)
- [A check counts only when a mutant breaks it](#mutants-burn-claims)
- [Generate or refuse; do not enumerate or parse](#generate-or-refuse)
- [Independent implementations held to shared vectors](#vectors-not-shared-code)
- [Strong review where a mistake is costly, once](#review-economy)
- [Forget by record, never by deletion](#controlled-forgetting)

<a id="claims-are-the-source"></a>
## Claims are the source; documents are views

**Problem.** A prose spec or assurance document drifts from what the tests establish, and a checker that reads the prose to find claims can be fooled by the prose.

**Form.**

- Each normative sentence or assurance row is a record: id, text, witnesses (tests, proofs), mutants, status (proved, tested, unburned, assumed, informative...).
- The human document, or the part of it that carries claims, is generated from the records; CI refuses a view that differs from the rendering.
- Debt is listed, never hidden: a claim with no witness or no biting mutant is shown as such.

**Lessons.**

- Never parse Markdown to find claims: minds PR #4 spent nine review rounds on comments, fences, escapes and renderer disagreements before switching ASSURANCE.md to a rendering of data, which warrant's SPEC-CLAIMS.md had already done.
- A checker whose scope comes out empty must fail, not pass (sokol-core scripts/check-claims.sh).
- A count of quotes found is stale-green: it stays green when the source is deleted (manifesto, papers/every-check-spawns-more/check_claims.py, deprecated for that reason).

**Where.**

- `warrant`: `tools/claims.py` — normative SPEC.md sentences filed as Warrant 2 records in .warrant/store; SPEC-CLAIMS.md is the generated view
- `warrant`: `SPEC-CLAIMS.md` — generated; `tools/claims.py check` refuses a differing file
- `minds`: `assurance.json` — ASSURANCE.md rendered from it, byte-compared (PR #4)
- `minds`: `tools/check_claims.py` — claims.json quotes every spec block; the spec itself is still split by hand (open: spec as a projection of its parts)
- `sokol-core`: `scripts/check-claims.sh` — every test, metric, flag, ADR or path a document cites must exist; an empty scope fails
- `sokol-core`: `docs/contracts` — one contract per invariant row, with shadow evidence

<a id="mutants-burn-claims"></a>
## A check counts only when a mutant breaks it

**Problem.** A green test whose name outruns what it tests looks like evidence.

**Form.**

- Each tested claim names mutants: an exact find/replace in one file.
- A runner applies one mutant at a time, runs the named tests, requires them to fail on an assertion (an import error proves nothing), and restores the file.
- Before trusting a kill, look at why it failed.

**Lessons.**

- A mutant killed only by a diagnostic's wording proves no lost refusal: check that the refusal disappears, not that its message changes (minds PR #4, rounds 1-2).
- A mutant that becomes equivalent after a redesign must be retargeted or removed, not kept as a green number.
- Give every mutant run a fresh bytecode cache: an earlier same-size mutant's cache can be loaded instead (minds tools/run_mutants.py, PR #4 round 3).
- End-to-end vectors can be blind to a component's refusals; measure with a mutant before trusting them (primitives p256-decode).

**Where.**

- `minds`: `tools/run_mutants.py` — mutants.json; TwinDivergence also counts as a kill
- `warrant`: `tests/mutants.py` — cited per claim in SPEC-CLAIMS.md
- `warrant-pdf`: `tools/mutants.json`
- `warrant-vet`: `tools/mutants.json`
- `sokol-core`: `.cargo/mutants.toml` — cargo-mutants
- `primitives`: `tools/p256_decode.py` — --selftest: every negative bites

<a id="generate-or-refuse"></a>
## Generate or refuse; do not enumerate or parse

**Problem.** A list of what something depends on, or a reader of a free-form document, is wider than anything that can check it: each review round finds another corner.

**Form.**

- When a finding recurs in a new form, stop patching instances and close the class.
- Either generate the artifact from data (so there is nothing to parse) or cover everything and refuse what cannot be read.

**Lessons.**

- minds release profile: a list of 'files an admission depends on' was bypassed four times (symlink, bytecode, namespace package, ZIP import); naming every tracked file closed it (PR #4).
- minds ASSURANCE.md: seven hand-made Markdown readers fell in turn; generation from assurance.json ended it (PR #4).

**Where.**

- `minds`: `tools/minds_chain.py` — profile_at: SHA-256 of every tracked file; a symlink or submodule refused
- `minds`: `assurance.json`
- `warrant`: `SPEC-CLAIMS.md`

<a id="vectors-not-shared-code"></a>
## Independent implementations held to shared vectors

**Problem.** A shared library agrees only with itself; one bug passes everywhere at once.

**Form.**

- Behaviour lives as vectors with provenance; each implementation keeps its own code and answers a small probe.
- Negatives must be shown to bite: each reject vector is rejected for the reason it names.

**Where.**

- `primitives`: `catalog.json` — classes, boundaries, bite proofs, registered implementations
- `primitives`: `run.py`

<a id="review-economy"></a>
## Strong review where a mistake is costly, once

**Problem.** Model review is expensive, a weak reviewer's false ACCEPT is worse than none, and repeated rounds on tooling cost hours.

**Form.**

- Mechanical checks (CI, mutants, claims) on every change; one strong adversarial reviewer per pull request only on costly surfaces (gate, kernel, rules changes, verifier, release checks, normative spec).
- The reviewer starts from the claims that moved, and works blind: what and where, never the author's conclusions.
- After fixes, a further round only when a fix touched a costly surface, scoped to those claims by name.
- Locally run what the change touches; the full suites and every mutant run in CI.

**Lessons.**

- minds PR #4 took ten rounds; six were on tooling that section 0 had already exempted.

**Where.**

- `minds`: `REVIEWING.md` — section 0
- `sokol-core`: `.github/workflows/witness-gate.yml` — signed witnesses as a required check

<a id="controlled-forgetting"></a>
## Forget by record, never by deletion

**Problem.** Old drafts, reviews and retired subjects keep pulling agents back into stale context.

**Form.**

- A subject leaves the active surface by a retirement record or tombstone that names it, why, and where its bytes are kept.
- Nothing is recreated from history by default; re-adoption is a new explicit decision.

**Where.**

- `manifesto`: `CONTROLLED-FORGETTING-0.1.md`
- `sokol-core`: `docs/RETIRED.md`
- `workspace`: `ARCHIVED-WORKSPACE.md` — ~/Projects tombstone
- `workspace`: `ARCHIVED-REPOSITORIES.md`
