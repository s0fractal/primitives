# Shared patterns

Methods our projects share, as forms with their instances and lessons: shared method, not shared code. Each project keeps its own implementation; before building one of these, read its entry and start from the form and the lessons, not from scratch. PATTERNS.md is rendered from this file (python3 tools/patterns.py --write); tools/check.py refuses a hand-edited PATTERNS.md, and `python3 tools/patterns.py --locate ~/Projects` checks every instance path in local checkouts.

- [Claims are the source; documents are views](#claims-are-the-source)
- [A check counts only when a mutant breaks it](#mutants-burn-claims)
- [Generate or refuse; do not enumerate or parse](#generate-or-refuse)
- [Independent implementations held to shared vectors](#vectors-not-shared-code)
- [Admit by evidence, never by an admin](#admission-by-evidence)
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
- A view of superseding records orders a lineage by the supersession chain, never by id or time alone: records filed in the same second tie on `at`, and ordering by id printed a reformulated goal before the one it replaced (warrant tools/roadmap.py, roadmap_test P6).

**Where.**

- `warrant`: `tools/claims.py` — normative SPEC.md sentences filed as Warrant 2 records in .warrant/store; SPEC-CLAIMS.md is the generated view
- `warrant`: `SPEC-CLAIMS.md` — generated; `tools/claims.py check` refuses a differing file
- `warrant`: `tools/roadmap.py` — goals (unowned questions) and obligations (duties that answer them) as Warrant 2 records in .warrant/store; ROADMAP.md is the generated view, byte-compared; nothing renders into SPEC.md
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
- A guard is burned only when removing it lets the forbidden write happen. If the code right after the guard would crash without it, the mutant is killed by the crash and proves nothing: make that code total, so the lost property is what the mutant exposes (warrant PR #170: M327 and M335 were first killed by an IndexError).
- A mutant run means nothing over a red baseline: a runner that counts a kill when the target case fails also counts a case that fails without any mutant (warrant #170 AMEND 1: M300-M318 read killed while roadmap_test was red). Make the runner refuse it: run each targeted test file once unmutated, in the same copy the mutants use, and refuse the whole run when a target case fails there (warrant #172: BASELINE_RED, exit 2; master's runner read M25 and A09 killed over a planted red case).
- A sharded mutant run claims coverage only when a merge proves it: the parts' union is the whole list, no id is in two parts, each row is the current definition over the same sources, and each kill is recomputed from the row's own case results, not read from its label (warrant #172: tests/mutants.py --merge, in the required check).

**Where.**

- `minds`: `tools/run_mutants.py` — mutants.json; TwinDivergence also counts as a kill
- `warrant`: `tests/mutants.py` — cited per claim in SPEC-CLAIMS.md; BASELINE_RED guard, --shard K/N and --merge (PR #172)
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

<a id="admission-by-evidence"></a>
## Admit by evidence, never by an admin

**Problem.** A list of admitted people is an authority every reader must trust, and its keeper becomes the gate a counterexample has to pass.

**Form.**

- A key binding certifies itself: the key signs {actor, public key, purpose}. A checker admits it mechanically; a name with no role is first-come, a name the configuration gives a role binds only the key its pin names, and a binding admitted at the base can be neither dropped nor preceded.
- A binding grants only 'this key signs as this actor'. Who may act is the duty's (holder, owed_to, accept_by); whose acceptance or challenge counts is each receiver's own profile.
- A counterexample is admitted by its replay, whoever files it: it lowers what it refutes (a claim's backing), never authorship. Only a lineage's author supersedes or retires it.
- A record of who did what (accepted, challenged, refuted) is a generated view that grants nothing and that no rule reads.

**Lessons.**

- Open admission must not make the names the configuration already gives a role first-come: on warrant #170's first head a fresh key bound `codex` and accepted a claim as codex, with check green. Pin every configured role in a reviewed file, as a receiver's profile pins keys: a key, reserved (null) or collective (never bindable, e.g. `readers`). Only names with no role stay first-come, and who a role is changes by a visible config diff (warrant #170 AMEND 1, .warrant/roles.json).
- Without a counter, a stranger's challenge must not block CI, or open admission becomes a way to stop the repository: count it only for the author, owed_to and accept_by, and list everyone else's as a thesis (warrant PR #170).

**Where.**

- `warrant`: `tools/claims.py` — admit_bindings (self-certifying .warrant/trust.json), challenge_table (counters from anyone), accept, ledger -> WITNESSES.md
- `warrant`: `tests/circle_test.py` — every rule as a fixture case; mutants M319-M373

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
