# Shared patterns

Methods our projects share, as forms with their instances and lessons: shared method, not shared code. Each project keeps its own implementation; before building one of these, read its entry and start from the form and the lessons, not from scratch. PATTERNS.md is rendered from this file (python3 tools/patterns.py --write); tools/check.py refuses a hand-edited PATTERNS.md, and `python3 tools/patterns.py --locate ~/Projects` checks every instance path in local checkouts.

- [Claims are the source; documents are views](#claims-are-the-source)
- [A check counts only when a mutant breaks it](#mutants-burn-claims)
- [Generate or refuse; do not enumerate or parse](#generate-or-refuse)
- [Independent implementations held to shared vectors](#vectors-not-shared-code)
- [Admit by evidence, never by an admin](#admission-by-evidence)
- [Order is witnessed, not claimed](#witnessed-order)
- [A cache changes cost, never the answer](#verified-cache)
- [Views as manifests over a content-addressed store; collection by reachability](#content-addressed-views)
- [Strong review where a mistake is costly, once](#review-economy)
- [Forget by record, never by deletion](#controlled-forgetting)
- [A write actor decides from trusted inputs only, binds them, and is exercised](#write-actor)

<a id="claims-are-the-source"></a>
## Claims are the source; documents are views

**Problem.** A prose spec or assurance document drifts from what the tests establish, and a checker that reads the prose to find claims can be fooled by the prose.

**Form.**

- Each normative sentence or assurance row is a record: id, text, witnesses (tests, proofs), mutants, status (proved, tested, unburned, assumed, informative...).
- A document published as a contract (cited by digest, linked from a release) is generated from the records and committed; CI refuses one that differs from the rendering. Every other view of the records is a build artifact: rendered by CI, checked for determinism, never committed; questions go to the records by query.
- Debt is listed, never hidden: a claim with no witness or no biting mutant is shown as such.

**Lessons.**

- Never parse Markdown to find claims: minds PR #4 spent nine review rounds on comments, fences, escapes and renderer disagreements before switching ASSURANCE.md to a rendering of data, which warrant's SPEC-CLAIMS.md had already done.
- A checker whose scope comes out empty must fail, not pass (sokol-core scripts/check-claims.sh).
- A count of quotes found is stale-green: it stays green when the source is deleted (manifesto, papers/every-check-spawns-more/check_claims.py, deprecated for that reason).
- A view of superseding records orders a lineage by the supersession chain, never by id or time alone: records filed in the same second tie on `at`, and ordering by id printed a reformulated goal before the one it replaced (warrant tools/roadmap.py, roadmap_test P6).
- A view's state label says what the engine decided, not only what the holder must do next: a discharge the engine held UNMET_CONDITION (its prerequisite still open) read 'no closure filed' in ROADMAP.md (warrant tools/roadmap.py need, roadmap_test P14).
- One mechanism for every contract: an application interface's rules go into the same claims document as a new pinned section, not into a second claims tool or document (warrant SPEC §10, the agent interface: 86 claims; AGENT.md became the operator's guide pointing to it). The tool needed only the placement of a new section's heading and first sentence (claims.py heading --section N, add --after N).
- Projections are build artifacts, not sources. warrant committed four views of its record store (SPEC-CLAIMS.md, ROADMAP.md, REVIEWS.md, WITNESSES.md), byte-compared by CI. Every parallel pull request re-rendered them, so they conflicted on nearly every merge (GitHub runs no pull_request workflow on a conflicting branch: warrant #197), the merge gate needed a clause admitting them after the accepted head, the review waker and the reviewer had to regenerate and commit them, and nobody read them. Since warrant #209 they are written to build/views/ and uploaded by CI; `tools/graph.py views --check` renders them in three processes (two other hash seeds) and refuses a difference, a determinism check in place of a comparison with a committed copy; the gate's tail is records and blobs only; and questions go to the graph by query (path, why, frontier, impact, delta, export; the MCP tool warrant_graph). Only published contracts stay committed: SPEC.md, and PILOT.md, which accepted closures cite by digest.

**Where.**

- `warrant`: `tools/claimslib` — normative SPEC.md sentences filed as Warrant 2 records in .warrant/store; SPEC-CLAIMS.md is a generated view, a build artifact since G11 (tools/claims.py is the command; one module per responsibility since warrant #176)
- `warrant`: `tools/graph.py` — the record graph by query (path, why, frontier, impact, delta, export) over warrant_agent/graph.py; `views --check`: the Markdown projections as build artifacts, rendered in three processes and compared (G11)
- `warrant`: `tools/roadmap.py` — goals (unowned questions) and obligations (duties that answer them) as Warrant 2 records in .warrant/store; ROADMAP.md is a generated view, a build artifact since G11; nothing renders into SPEC.md
- `minds`: `assurance.json` — ASSURANCE.md rendered from it, byte-compared (PR #4)
- `minds`: `tools/check_claims.py` — claims.json quotes every spec block; the spec itself is still split by hand (open: spec as a projection of its parts)
- `sokol-core`: `scripts/check-claims.sh` — every test, metric, flag, ADR or path a document cites must exist; an empty scope fails
- `sokol-core`: `docs/contracts` — one contract per invariant row, with shadow evidence
- `warrant`: `SPEC.md` — §10 Agent interface: the contract of warrant_agent (warrant-agent/1) as claims in the same document as the engine's rules, backed by agent cases and agent mutants

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
- A relative claim (A no worse than B) is green when the instrument reads nothing: two decoders that read neither arm tie at the floor and 'support' parity. Pair the relative test with an absolute adequacy condition on the reference arm, and name a mutant that drops it (lab phs-clock PREREG D12, Codex r1 F3, mutant M20). In the confirmatory run the condition held (the honest decoder read Pure-PHS 0.10-0.21 above its own readout), so H1 CONTRADICTED is about the memory, not a blind decoder.
- Give every mutant run a fresh bytecode cache: an earlier same-size mutant's cache can be loaded instead (minds tools/run_mutants.py, PR #4 round 3).
- End-to-end vectors can be blind to a component's refusals; measure with a mutant before trusting them (primitives p256-decode).
- A guard is burned only when removing it lets the forbidden write happen. If the code right after the guard would crash without it, the mutant is killed by the crash and proves nothing: make that code total, so the lost property is what the mutant exposes (warrant PR #170: M327 and M335 were first killed by an IndexError).
- A mutant run means nothing over a red baseline: a runner that counts a kill when the target case fails also counts a case that fails without any mutant (warrant #170 AMEND 1: M300-M318 read killed while roadmap_test was red). Make the runner refuse it: run each targeted test file once unmutated, in the same copy the mutants use, and refuse the whole run when a target case fails there (warrant #172: BASELINE_RED, exit 2; master's runner read M25 and A09 killed over a planted red case).
- A sharded mutant run claims coverage only when a merge proves it: the parts' union is the whole list, no id is in two parts, each row is the current definition over the same sources, and each kill is recomputed from the row's own case results, not read from its label (warrant #172: tests/mutants.py --merge, in the required check).
- Read the map from the code's side too: claims listing their mutants say nothing about the statements no mutant changes. On warrant 3f2be6a, 274 of 2820 statements of warrant/ and warrant_agent/ were changed by a mutant a BACKED claim cites, and 9 cited mutants only insert code before a statement, so their claims reach no existing statement (warrant tools/claims.py why --uncovered).
- A case that reads its results through an asserting helper (ok(), a bare ['ok'] index) dies before its own check: a mutant that breaks that call is killed by the exception, or lost with every case after it, never on the case's assertion. Read results with .get in the case a mutant targets (warrant agent_write_test W04 and W07, mutants A72 and A78). The same shape recurs where a mutant removes a key the control reads: in time-lab q8-what-counts seven mutants first survived because the controls read a verdict's ['reason'], which the mutated analysis no longer wrote, and failed with KeyError; with .get('reason', '') every one died on its assertion.
- Generated mutants find blind spots; they never back a claim. Keep them in a harness the claims checker does not know, so a citation of one is refused (warrant tests/generated_mutants.py, UNKNOWN_MUTANT). A survivor is closed by a witness that kills it on an assertion plus a curated mutant the claim cites (warrant #178: R49, M475 and M476 under SPEC-4.5-1).
- Name a generated mutant by what it changes, not where: hash the file, scope, the statement's syntax, its occurrence among equal statements, the operator and the site. A positional key shifts with every insert above it, and a run-to-run diff (BLIND: killed before, surviving now) then means nothing.
- Select tests per mutant from a line-coverage map made once per tree from the unmutated run, which doubles as the red baseline. Trace subprocesses too (a sitecustomize.py on PYTHONPATH, a SIGTERM handler that dumps): a test that overwrote PYTHONPATH hid the MCP server it starts, and its statements read NOT_RUN.
- A hunt's exit status says the run happened, never what survived; its merge recomputes each outcome from its row instead of requiring KILLED. A TIMEOUT depends on the runner's load (six mutants flipped SURVIVED -> TIMEOUT between two local runs): never let it make a later survivor BLIND.
- Boundaries are what hand-written mutants miss: of 8632 generated mutants of warrant (#178), the survivors closed first were `<=`/`<` and `>`/`>=` on attenuation, a depth bound with no case at 256/257, and a trust file binding one key twice. A survivor whose guard no input reaches is equivalent: record it with its reason under review, and name the entry when a test later kills it.
- An assertRaisesRegex failing with "X does not match Y" is no kill: the expected exception was raised, the input is still refused, only the message moved (another layer or the crash net caught it). minds found 23 of 203 such kills. Decide it where assertRaises checks (wrap _AssertRaisesContext.__exit__), not from printed lines: a multi-line message defeated the first line filter (Codex, minds PR #15). An import-time assert that refuses the mutant before the test runs is no kill either.
- A refusal held by several layers (minds append-only: Check #2, the reader's status and mode checks, then the read of a deleted entry itself; a host guard and the pinned kernel) cannot be burned by guard mutants, even all of them together: its honest status is unburned, with the layers named. Build the vector that only one rule breaks first (delete an orphan atom, not change a mode): an ambiguous vector hides which layer refused. time-lab q6-renewal: the control with every row one trajectory short was refused by the world check before any clock check ran, so the mutant without the clock's shape check survived; the vector only a clock row breaks (one clock short of a trajectory) killed it, and showed that the check sat after np.asarray, which raised on the ragged rows instead of refusing them. Check lengths before building the array.
- Cargo decides what to rebuild by modification time: mutants built into a shared target were served the previous mutant's build (three false kills in minds). Build each kernel mutant in a fresh target, and refuse a build byte-equal to the pinned kernel as equivalent.
- A test that fixes the step count while halving dt cannot see a defect whose error grows with simulated time: the starter PDF's energy test for the port-Hamiltonian kernel shows orders 4.4 and 2.4 for an explicit gyroscopic kick that diverges to 6e20 over 10^4 steps. Fix the horizon, not the step count, and name the kick as the mutant the test must kill (lab phs-soliton test 1, starter check C4a).
- When an edit changes a line that several mutants target, re-check every mutant whose find text contains the old text, not only the ones the change names: warrant PR #195 retargeted M576 and M577 after moving the walker's depth check and missed M592, which went BAD_MUTANT on the same "if dep in objects" text (CI mutants 3/4, run 40187522296; fixed in a7eebef). Before committing, search the mutant list for the old line, and run every mutant that matches it.
- Run one mutant by hand before trusting a new runner's first table: minds G6 (PR #40) first copied the mutated module into a temporary directory, where its sibling import failed, and all 17 mutants read as survived; the copy now sits beside the original and imports as it does. A mutant that deletes the only line of an `if` body is a syntax error, a crash and not a kill: replace the line with `pass` (m-contrast-worst).
- A skip reports ok, and a crash can report a verdict. minds' test 25 skipped when the chain ref was absent, so only CI's fetch step stood between it and a green no-op; MINDS_REQUIRE_CHAIN=1 now turns that skip into a failure in the job that provides the ref (open-ontologies' OO_REQUIRE_FIXTURES). An uncaught Python error exits 1, the code of a refusal or a negative verdict; minds' witness checker and offline verifier now exit 3 on one, a code no verdict uses (minds PR #48).
- A verdict reached under a weaker assumption gets a word of its own, or the output alone cannot say which was reached: minds' inspect-attestation, which pins no keys, printed `accepted`, the word of verify-attestation, and now prints `accepted_under_own_policy` (minds PR #48; open-ontologies decision 0003, `entailed` against `entailed_under_supplied_rules`). Burn the distinction with a mutant that lets both words through.
- A proved checker still reads through a decode. minds' Lean witness checker (vars1witness; theorem witness_sound) checks the store that check.py decoded from bytes, so the theorem states the decode's faithfulness as a hypothesis beside the reader's pin. Four mutants of the decode (kill edges dropped, INVALID verdicts not marked, seals written unverified, a seal's scope replaced) are killed by requiring the proved checker and the unproved one to agree on every term the tests make (minds PR #50). Name each hypothesis a proof rests on, and burn the ones that code can break.
- Controls that share a nuisance parameter cannot kill a mutant that drops it: every synthetic cell of time-lab q4-line moved at velocity 0.5, so a mutant that removed v² from the efficiency v²/(D Σ) survived until a control with one slower cell was added. Vary each factor the computation reads in at least one control. The same holds for the property a statistic is chosen for: time-lab q8-what-counts takes the median of model answers because a few answers run wild, and a mutant that took the mean survived until a control gave a few lists of each cell wild answers. A gate on a maximum is a tail statistic: time-lab q9-field's slip gate first refused at a bond range of pi, where a slip moves it by 2 pi, and the bath alone reached 3.6 at the calibration's maximum over 32 trajectories, thousands of bonds and 4000 samples; it would have made two hypotheses inconclusive with no slip at all. Set such a gate from the calibration's own maximum and the size of the event it detects (here 1.5 pi), and keep a control that the bath alone does not trip it.
- Synthetic controls drawn Gaussian cannot show a tail, and a calibration that reports a point cannot show the registered interval: time-lab q4-line's light line (H3) was calibrated at G = 0.034, and the confirmatory point was 0.012, yet its interval over trajectories reached ×2.8 because 3 of 1024 trajectories (each a stage slip that stalled the clock) carried the whole damage; the hypothesis closed inconclusive. Calibrate the registered interval, not only the estimate, before choosing a threshold. q5-bound did so (calibration/full-analysis.json: the registered analysis over a full-size run on calibration seeds) and moved two thresholds before registering; its adequacy gate, first drafted as eta(alone) > 0.8, would have left H2 inconclusive (confirmatory lower bound 0.784), and at the calibrated 0.6 it was assessed and supported. A blind prediction can have its interval calibrated too, without data: time-lab q7-duration ran no readout on calibration seeds and took its widths from synthetic errors exact to the formula it predicts; its first ×1.15 window was narrower than the interval the formula itself produces, and its input (a diffusion measured by q6-renewal) carries its own sampling error. Widened before registering (×4/3 and ×1.5, still ×16 apart from the rival laws), all five blind predictions were supported, the points within ×1.02.
- A threshold the tested quantity cannot cross is no hypothesis, and no mutant of it can be killed: time-lab q7-duration first stated 'the clock with counting gains less than 1.5 times' on an estimate fused with a weight fixed at registration, which bounds the gain by 1 / (1 - w)², here 1.375; a control meant to contradict it could not. Derive the bound of each tested quantity before writing its threshold, and test the quantity that is free (here the ratio of the two independent errors, whose best combination gains 1 + R).
- A differential check is as good as the inputs it runs on. minds compared its proved executable lens (vars1exec) with the rules kernel only on generated chains of a few dozen cells; compiled as written, the proved code built its results from nested closures and always ran n rounds of Pass 2, and took 4 s at 76 cells and gave no answer in 15 minutes at the live chain's 624. Run the comparison on the live artifact too: minds PR #52 runs it on every tip of refs/vars/heads/minds. When proved code is too slow, do not hand-write a fast twin beside it: prove the fast version equal and let the compiler substitute it (Lean `@[csimp]`, minds Exec.lean `fill_eq_fast`, `staleOf_eq_fast`), so the proofs hold of the code that runs (624 cells: 8 s).
- A mutant whose replacement names a variable the code no longer has does not fail on its assertion; it crashes, and a runner that counts only assertion failures reports it SURVIVED (minds' witness mutant m-lean-seal-ctx after `scopes` became `chain`). That refusal is right: a crash proves nothing. When the code a mutant targets is renamed, re-derive its replacement as well as its find string.

**Where.**

- `minds`: `tools/run_mutants.py` — mutants.json; TwinDivergence also counts as a kill; tools/mutant_test.py decides wording-only failures inside assertRaises (PR #15)
- `warrant`: `tests/mutants.py` — cited per claim in the claim records (tools/graph.py path SPEC-…); BASELINE_RED guard, --shard K/N and --merge (PR #172)
- `sokol-core`: `.cargo/mutants.toml` — cargo-mutants
- `primitives`: `tools/p256_decode.py` — --selftest: every negative bites
- `warrant`: `tools/claimslib/why.py` — why FILE:LINE: a statement -> the mutants that change it -> the BACKED claims citing them -> obligations -> goals; why --uncovered: the statements no cited mutant changes
- `warrant`: `tests/generated_mutants.py` — generated mutants and survivors: discovery, never backing; .github/workflows/survivors.yml weekly, with claims.py audit pairs
- `lab`: `phs-soliton/tools/run_mutants.py` — mutants.json; every named test must fail on an assertion (all, not any), the baseline must pass first, a fresh pycache_prefix per test under ignored runs/
- `minds`: `experiments/g6/test_g6.py` — --mutants: an experiment's generator, renderings and scorer (mutants.json beside it); the mutated copy is written beside g6.py and run against the named test, which must fail on an assertion (PR #40)
- `minds`: `experiments/witness/test_witness.py` — --mutants: 35 mutants of an independent proof-term checker; the named tests run unmutated first and a red baseline is refused, each mutant runs without a bytecode cache (PR #46)
- `lab`: `phs-clock/mutants.py` — a PREREG's frozen analysis and admission (28 mutants, mutants.json) on phs-soliton's harness; an equivalent mutant (inside the EPS slack) was removed, a KeyError kill rewritten to fail on an assertion (lab #11)
- `time-lab`: `q1-weber/tests/mutants.py` — five mutants of the registered analysis, each killed by a synthetic control on an assertion before the analysis bytes were registered
- `time-lab`: `q4-line/tests/mutants.py` — 14 mutants of a registered analysis that compares gains and precision per entropy across cells; q2-crystal, q3-self, q5-bound, q6-renewal, q7-duration, q8-what-counts and q9-field keep the same form (7, 13, 16, 20, 21, 23 and 37; q8 removed one near-equivalent mutant, an unparsed answer counted as 0, which its 95% parse gate leaves too few answers to move a median)

<a id="generate-or-refuse"></a>
## Generate or refuse; do not enumerate or parse

**Problem.** A list of what something depends on, or a reader of a free-form document, is wider than anything that can check it: each review round finds another corner.

**Form.**

- When a finding recurs in a new form, stop patching instances and close the class.
- Either generate the artifact from data (so there is nothing to parse) or cover everything and refuse what cannot be read.

**Lessons.**

- minds release profile: a list of 'files an admission depends on' was bypassed four times (symlink, bytecode, namespace package, ZIP import); naming every tracked file closed it (PR #4).
- minds ASSURANCE.md: seven hand-made Markdown readers fell in turn; generation from assurance.json ended it (PR #4).
- A shape written in each module that checks it is a class, not a set of instances. Warrant's `$` anchor had to be fixed at fourteen sites (#164), with fourteen definitions of four hex shapes and the actor-id predicate in eleven modules. Define each shape once (warrant/shapes.py), make every former copy import it, and refuse any second definition by reading the source (tests/shapes_test.py S6), even a correct one. Retarget the mutants of a moved definition under their old ids, and give each predicate the same vectors: \n, \r\n, non-ASCII digits, uppercase, one short and one long, non-strings (warrant #176).
- A table that explains a tuple's words drifts from the tuple: warrant's explain glossary had no entry for 4 of its 18 refusal codes. Hold the table to the tuple with a case that enumerates it (warrant agent_mcp_test M16 over errors.CODES, config.RELATIONS and engine.RELIANCE), not by review.
- A recipe in a guide is the test's input, not a copy of it: the exact MCP arguments for the roadmap's oblige, done and accept live in one JSON block of AGENT.md, and the equivalence test reads that block and requires the store it files to be byte-identical to the tool's after every step (warrant #179, Q01). Dogfooding the recipe on the real store found what the fixture could not: owned goals were not reachable through the interface at all (context scope).

**Where.**

- `minds`: `tools/minds_chain.py` — profile_at: SHA-256 of every tracked file; a symlink or submodule refused
- `lab`: `phs-clock/run.py` — source_problems: the whole repository outside the two output paths against the PREREG tag, committed additions and untracked files included; hashing the tag's files plus a dirty-tree check let a clean committed phs-clock/numpy.py through (Codex r1 F2, lab #11)
- `minds`: `assurance.json`
- `warrant`: `tools/claimslib/views.py` — SPEC-CLAIMS.md rendered from the records (a build artifact since G11)
- `warrant`: `warrant/shapes.py` — hex64, hex128, the view token, the question reference and the actor id, defined once; tests/shapes_test.py S6 refuses a hex pattern written anywhere else
- `warrant`: `tests/agent_repo_test.py` — Q01 reads AGENT.md's roadmap recipe and compares stores byte for byte with tools/roadmap.py; Q02 runs it over stdio MCP

<a id="vectors-not-shared-code"></a>
## Independent implementations held to shared vectors

**Problem.** A shared library agrees only with itself; one bug passes everywhere at once.

**Form.**

- Behaviour lives as vectors with provenance; each implementation keeps its own code and answers a small probe.
- Negatives must be shown to bite: each reject vector is rejected for the reason it names.

**Lessons.**

- Independent code is not independent evidence: minds' witness checker (experiments/witness/check.py, PR #46) shares no code with the lens, but the absences it relies on (no cell invalidates the decision's cone, no INVALID verdict on it) are read over the same store, so a complete forged store fools both. Split what a checker proves from bytes (hashes, signatures, keys fixed by the asked id) from what it reads under a closed-world assumption, and say which input the latter rests on.
- Evidence must read one way: Python's json keeps the last value of a repeated key and other readers the first, so a witness term or bundle naming a key twice has two readings and two correct readers can check different decisions (open-ontologies decision 0008: two verified kernels disagreed over a repeated binding key, and the defect was in the format). warrant's jcs.py and sigma's sigma_resume already refused repeated keys; minds' witness checker and offline verifier read them last-wins until minds PR #48. Refuse the repeated key at the parser of every untrusted input, and refuse NaN, Infinity and -Infinity there too: Python's json reads them and JSON does not have them (Codex finding fb410499 on minds #48, after the first fix set only object_pairs_hook; warrant's jcs.py sets parse_constant as well). A canonical-bytes check (re-serialise and compare) refuses the repeated key too. The `canon` vectors take a parsed body and cannot hold one: a class of raw-bytes vectors would need a probe in every reader, and is not built.
- Excluding an identity member from a byte comparison is sound only once it is shown derived from members that are compared plus the engine's own identity: warrant's report `assessment` digests its operands (snapshot, trust, profile, as_of, code), not its findings. The first forgery test changed a finding and that check did not catch it, because the digest never covered findings; the check guards the operands, and the findings are compared themselves (warrant differential D03).

**Where.**

- `primitives`: `catalog.json` — classes, boundaries, bite proofs, registered implementations
- `primitives`: `run.py`
- `minds`: `experiments/witness/check.py` — a proof-term checker for 'Settled at a tip' with its own parsers and Ed25519 and the spec's constants, no code of vars1.py; held to the lens by an exhaustive subset test (222 terms on two G6 histories) and to RFC 8032 by its vectors; a term that names a key twice is refused, not read last-wins (minds PR #48)
- `warrant`: `warrant/differential.py` — release n (from PyPI) and the head assess one live store; reports must be the same bytes but for the engine's identity (code, assessment), any other difference declared member by member, else refused (roadmap G12, D01-D05, T61-T67). First run: warrant, minds, time-lab and interdict-mesh SAME between 3.0.0a2 and 95 later commits
- `minds`: `test_vars1_props.py` — lean_checks: the Lean model's fold (Fold.lean, Fold2.lean under v2) and proved Passes 1-2 (Exec.lean), compiled, against the rules kernels (I9, I10) on generated chains, test 88's rules changes and every tip of the live chain (test_every_tip_of_the_live_chain, PR #52)

<a id="admission-by-evidence"></a>
## Admit by evidence, never by an admin

**Problem.** A list of admitted people is an authority every reader must trust, and its keeper becomes the gate a counterexample has to pass.

**Form.**

- A key binding certifies itself: the key signs {actor, public key, purpose}. A checker admits it mechanically; a name with no role is first-come, a name the configuration gives a role binds only the key its pin names, and a binding admitted at the base can be neither dropped nor preceded.
- A binding grants only 'this key signs as this actor'. Who may act is the duty's (holder, owed_to, accept_by); whose acceptance or challenge counts is each receiver's own profile.
- A counterexample is admitted by its replay, whoever files it: it lowers what it refutes (a claim's backing), never authorship. Only a lineage's author supersedes or retires it.
- A record of who did what (accepted, challenged, refuted) is a generated view that grants nothing and that no rule reads.
- What a mechanical backing establishes can be accepted mechanically: a checker is an actor named by the hash of its code, its key pinned like any role. It accepts only after it replays the claim's witnesses and mutants at one commit. Its acceptance carries the replay report and is named for what it checked, never as a review. The receiver reads every report against the claim, and the code at the reported commit against the actor id.

**Lessons.**

- Open admission must not make the names the configuration already gives a role first-come: on warrant #170's first head a fresh key bound `codex` and accepted a claim as codex, with check green. Pin every configured role in a reviewed file, as a receiver's profile pins keys: a key, reserved (null) or collective (never bindable, e.g. `readers`). Only names with no role stay first-come, and who a role is changes by a visible config diff (warrant #170 AMEND 1, .warrant/roles.json).
- Without a counter, a stranger's challenge must not block CI, or open admission becomes a way to stop the repository: count it only for the author, owed_to and accept_by, and list everyone else's as a thesis (warrant PR #170).
- An acceptor that no one may sign as cannot be replaced, because duties are append-only: a duty naming it can never be discharged by anyone else. The way out is a new duty for each lineage, filed by the author when it next supersedes the claim, with the old duty left OPEN as history and the views following the lineage. Warrant's 195 BACKED claims named codex, who would not accept them one by one. `claims.py rehome` moved them to duties the replay checker accepts, and `claims.py replay` accepted all 195 (warrant #176).
- Name a commit by its canonical full id, never by a ref: the full lowercase hex id of the repository's object format that Git resolves to itself as a commit, not a tag, a branch, HEAD~1, an abbreviation, an annotated tag's own id, uppercase or a trailing newline. A name can move. A signed replay report naming `refs/tags/replay-source` passed warrant #176 at c2d1bbd, and after the tag moved `claims.py replay --verify` re-executed another tree and said OK (Codex). Check the shape for every receipt, without git, so it holds after the receipt is in the base. Before reading or running anything, resolve the id to itself and compare its tree with the signed one. The rule is minds VARS-1 §3 (prior art), and warrant #176 AMEND 1 applies it: replay.canonical, CHECKER_COMMIT_NAME, regressions R16-R22.
- Custody of a program's key is still custody: whoever holds the checker's seed can sign as the checker without running it. Re-executing the reported commit's own checker code (hashed first) in CI is what turns a false report into a refusal before merge (warrant `claims.py replay --verify`, CHECKER_REPLAY_DIFFERS).
- One admission rule, one implementation, wherever keys are admitted: when a second reader (warrant's agent workspace) needed the repository's bindings under its roles, the rule moved from the claims tool into the engine package (warrant/bindings.py) and the tool imports it; its mutants moved with it (M319-M326, M376, M379). The reader admits on every view, and a roles file with any problem refuses instead of being read as fewer pins: a dropped pin makes its name first-come (warrant #179, T01-T03, A94-A96).

**Where.**

- `warrant`: `tools/claimslib/bindings.py` — admit_bindings (self-certifying .warrant/trust.json); counters.py challenge_table (counters from anyone); author.py accept; views.py ledger -> WITNESSES.md
- `warrant`: `tools/claimslib/replay.py` — the replay checker: actor `checker sha256:<hash of this file>`; by_replay.py is what check reads of its acceptances
- `warrant`: `tests/replay_test.py` — R0-R22: each adversary case of acceptance by replay (R16-R22: a commit named by its canonical id), mutants M444-M469
- `minds`: `VARS-1-SPEC.md` — §3 Store and gate: a commit is named by its canonical id, never a ref, an abbreviation or a revision expression
- `warrant`: `tests/circle_test.py` — every rule as a fixture case; mutants M319-M373
- `warrant`: `warrant_agent/init.py` — warrant-agent-mcp init: a signer only from an existing seed whose key the repository pins and admits; no key created (I01-I10, A87-A93)

<a id="witnessed-order"></a>
## Order is witnessed, not claimed

**Problem.** A time a signer writes into its own record orders nothing: whoever dates a record can place it before records it already knows about, and a rule that compares those times lets one party rewrite what happened.

**Form.**

- Each writer's records form a chain: every record names the one its writer filed before (its id covers that link), so a record cannot be placed before what its writer already filed; it can only extend the chain or fork it.
- Where a rule needs one of a writer's records before another of the same writer's, the chain decides, never the claimed time; a pair the chain does not order (a fork, a record outside every chain) does not meet the rule.
- A fork is listed as evidence, and nothing is excluded for it: exclusion lets the forker retract its own earlier records.
- Writers extend the head by compare-and-swap; a reader treats claimed time as a claim and states what no record witnesses (the order of two writers' records that do not name each other).

**Lessons.**

- warrant F43 (outside review, reproduced on 3f2be6a): a delegate discharged before accepting, then filed a second acceptance dated before its discharge; the engine took the earliest acceptance and the duty became DISCHARGED. 'Use the latest acceptance' stops that reproduction, not a single backdated acceptance filed after the discharge; only the delegate's own chain orders the two (warrant #174, SPEC-4.1-11).
- Excluding both branches of a fork looks strict and is a retraction button: a holder forks before its own handover, the handover disappears, and the new holder's admitted work becomes unauthorized. Keep both, list the fork, and let the chain rules fail only the forker's own unordered filings (warrant assessment_test R43, mutant M415).
- A per-receiver intake log (witnessed birth) is no base order for records that travel as whole-store unions: at the receiver everything arrives in one import and the order falls back to claimed time, so two receivers judge the same records differently. A shared history the receiver trusts (a protected branch's merges) can be a later operand; it is not in the snapshot.
- Records filed in one second must still follow their chain: an order of (time, id) put a writer's discharge before its own acceptance whenever the discharge had the smaller id (warrant SPEC-4-7, assessment_test R48).
- A chain orders a writer's records among themselves, never against the world, and a pre-registration must show that its data came after it. time-lab derives every seed of its data from the registration's id (the hypotheses and the analysis code cannot be fitted to data that depend on them) and from the first drand round dated at or after the GitHub-witnessed push holding the registration (the data could not exist earlier, and a private re-roll of the registration cannot reach a round before its own publication). q1-weber: push 2026-10-31T01:56:26Z, round 33536141 one second later. The core has no notion of either anchor; they live in tools and in an attest's body (time-lab METHOD.md N2).

**Where.**

- `minds`: `vars1.py` — the gate: refs/vars/heads/<scope> is a linear chain moved by `git update-ref` compare-and-swap; append-only checked by `git diff-tree --diff-filter=a`; birth = first commit holding an object (VARS-1 §3, §4.1)
- `warrant`: `warrant/engine.py` — View._chains / before / ordered; Holders.at(pos, filing): a filer's own records in chain order (SPEC-4-8..4-10, SPEC-4.1-11/12)
- `warrant`: `warrant/store.py` — Store.append / Store.extend: prev from the actor's head under a lock on records/; warrant-agent commit refuses CHAIN_MOVED
- `time-lab`: `tools/tl.py` — beacon: the earliest push GitHub's activity API reports holding the registration, the first drand quicknet round after it, filed as an attest on the registration; run.py seeds from both

<a id="verified-cache"></a>
## A cache changes cost, never the answer

**Problem.** Re-verifying everything on every read makes a store quadratic to write and slow to read, and a cache that stands in for verification is a second, unverified source of answers: one stale, forged or foreign entry admits what the full check refuses.

**Form.**

- Cache only a pure function's result, keyed by everything the answer depends on: the exact input bytes (a digest, not a file name or a timestamp), the trust or profile it was judged under, and the identity of the code that judged it.
- Consult an entry only when every byte it stands for is present and hashed in this read; never let it stand for a file that is absent, changed or new. What remains per read is the I/O and the hashing: the floor of 'the bytes counted are the bytes present'.
- The cache is the receiver's own, outside the data it describes: not in the store, the snapshot, the handoff or the identity of any result. An entry that is not provably its owner's (a MAC under the owner's secret) is skipped: a tampered, forged, stale or foreign cache costs a recomputation, never an answer.
- Prove it against the cold path, whole: for every guard, a corruption case (other trust, changed bytes, another name, a new file, a removed file, a forged line, an edited verdict, another code identity) whose answers equal the uncached answers byte for byte, and a mutant that drops the guard and is killed by that case.

**Lessons.**

- warrant F44 (outside review 'Monday', reproduced on 6588a2b): the writer's head re-authenticated the whole store on every append, twice; 1000 appends by one actor took 184 s and one append at 10 000 records 3.8 s. Remembered verdicts (process memory, and an owner's MACed index for one-shot processes) remove the signature checks without trusting anything the full read would not; the second head read under the same lock found nothing the first did not and was removed (warrant #175: store.Verdicts, tests/store_index_test.py, mutants M430-M437).
- A cache that holds verdicts must authenticate its own entries: warrant's ReplayCache trusts any file in its directory, so whoever can write there can choose a replay result. The F44 index MACs every line (trust, record id, bytes digest, verdict, code identity) under a random secret only its owner reads; the secret's randomness is itself a mutant (M437).
- Key the code too: a verdict an older package computed under rules since tightened would admit what the new rules refuse. The F44 key binds the package's whole-tree identity (engine_identity) and the signature library's version, inside the MAC (M436).
- Keep the cache out of the data's directory: the first F44 draft wrote the writer's index into the store, and warrant's claims check refused it as a STRAY_FILE; there it would also travel with every copy of the store. A directory of the owner's, like its keys, has neither problem.
- A file's name is part of its input: keyed by the bytes digest alone, an authentic record's bytes copied under another record's name would inherit its verdict (M432).

**Where.**

- `warrant`: `warrant/store.py` — _verdict, Verdicts: authentication verdicts by (trust digest, record id, sha256 of the bytes), MACed with the code identity under the owner's secret; Store(root, verdicts=DIR), assess(verdicts=DIR), `--verdicts DIR` (F44, #175)
- `warrant`: `warrant/compute.py` — ReplayCache: verified replays by provider identity and exact chain, consulted only when every byte is in the view (SPEC §7); its entries are not MACed

<a id="content-addressed-views"></a>
## Views as manifests over a content-addressed store; collection by reachability

**Problem.** A frozen view that copies every byte it may answer from costs a whole store per view: the reader's guarantee (later changes alter nothing it reads) is bought with unbounded disk, and nothing ever decides which copies may go.

**Form.**

- One object store per owner, every object named by the SHA-256 of its bytes (git's loose objects, minds cas/): written once by linking a complete read-only file into place, so a name is never overwritten by a racing writer. Bytes under a name that do not hash to it are damage; the only replacement is the bytes that do, which can only restore what every reader of the name pins.
- A view is a small manifest, itself an object, naming everything it answers from by hash: a tree (the listing, shared by every view of the same store state), the report body (shared while it is the same), the code it ran; a per-view pointer names the manifest. Bytes that may not be what their outer name says (a record file under a record id) are stored under their own hash, and the tree maps the outer name to it.
- Every read hashes what it read; an absent or damaged object is a typed refusal, never a read from the live source. The frozen guarantee is then structural: objects only ever get added, and a manifest pins exact names.
- Collection is mark and sweep from the live manifests only: expired views go first, then every object no live manifest reaches. Everything else keeps its own bytes and is never a root or touched (drafts, staging, journals); the source store is never touched.
- Close the race by the lock, not by timing: a writer holds it shared from its first object until its manifest is reachable, a collector exclusively; readers take none, and a reader whose view expired under it is told so, not that the bytes are damaged. An opportunistic collection tries the lock without waiting, after the writer has released it.

**Lessons.**

- warrant-agent views were full copies: 45 views of a 1500-record store took 756 MB and 127 128 files on disk (Codex's real state reached 720 MB). As manifests over one object store: 18 MB and 2 964 files, 3 files and 12 KB per view, and context got faster (1.12 s to 0.65 s) because unchanged objects are compared, not rewritten (warrant #184, tests/agent_views_test.py J01-J16, mutants A114-A131).
- Split what differs from what is shared before hashing it: two reports of an unchanged store differed only in their assessment id and as_of, so the report body is one shared object and the manifest carries the two fields.
- Do not name an object by an identity its bytes may not have: a store can hold, under a record id, bytes that are not that record, and the view must show them as they were. Name every object by its own bytes and map the outer name in the tree.
- Carry the source's own anomalies in the tree: the copying views dropped the store's misfiled entries, so the assessed snapshot never matched the captured one and every context of a store with a stray file was refused; a tree that lists them reproduces the store read exactly.

**Where.**

- `warrant`: `warrant_agent/objects.py` — the workspace's object store: put (link once, repair damage), get (hash on read), snapshot under admission limits, the shared/exclusive lock
- `warrant`: `warrant_agent/views.py` — capture writes objects and a manifest under the shared lock; load resolves through it; collect marks from live manifests and sweeps; collect_due at a capture by gc_interval; `warrant-agent gc` (SPEC §10.2)
- `minds`: `VARS-1-SPEC.md` — §3: cas/{atoms,cells,seals}/<2 hex>/<62 hex>, every entry's bytes hash to its path

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
- A review the reviewer does not sign itself is prose relayed by hand: warrant's review loop ran 30+ times as REVIEW.md, chat and copy-paste. As records, ACCEPT is the reviewer's own accept of one head's closure, AMEND its challenge carrying a finding, and a finding with a test is replayed at each later head (reproduces / no longer reproduces) by a checker named by its code; a finding without one stays a labelled thesis.
- Name what was reviewed by its full commit id, and what merged by its merge commit's second parent: acceptance is read from the tip's own store, so an acceptance filed after the merge does not turn it into a reviewed merge; a merge is a Git act, observed, never a closure.
- Across actors only the signed `at` orders records: a same-second tie is not 'later'. Rules that ask whether a finding came after the next head use strict order, and fixtures date the later record explicitly, or the test is flaky (warrant reviews_test V18 failed under unrelated mutants).
- A ledger column a generated view adds is paid in every case of the selftest that renders the view: the review counts of WITNESSES.md read the records without assessing them (warrant claims selftest, 134 cases).
- A checker named by the hash of its code signs only from that code, but its seed is an ordinary file: when model sessions held it, they filed the checker's records at their own discretion (warrant #176, #181), and a session that refused left findings NOT REPLAYED (#190). The deployed waker now runs the base's pinned checker on every due head before the reviewer is woken: sandboxed (no network, writes confined to the worktree, the seed directory unreadable), the seed on standard input only, and it pushes only the records that run printed, while the branch is still at that head (warrant #192, W1-W11). On one machine, keeping the seed from agents is still policy, not enforcement.

**Where.**

- `minds`: `REVIEWING.md` — section 0
- `sokol-core`: `.github/workflows/witness-gate.yml` — signed witnesses as a required check
- `warrant`: `tools/claimslib/reviews.py` — the pull request review loop as records: duty, head closures, findings as challenges, replayed tests, merge observations; REVIEWS.md
- `warrant`: `integrations/codex-plugin/waker/waker.py` — Waker.replay: the review replay checker before each wake, sandboxed, seed on stdin

<a id="controlled-forgetting"></a>
## Forget by record, never by deletion

**Problem.** Old drafts, reviews and retired subjects keep pulling agents back into stale context.

**Form.**

- A subject leaves the active surface by a retirement record or tombstone that names it, why, and where its bytes are kept.
- Nothing is recreated from history by default; re-adoption is a new explicit decision.

**Lessons.**

- Retiring an experiment can cut a live dependency: minds' witness tests built their histories with the withdrawn G6 pilot's generator. Move what live code needs first, and show that the moved code gives the same outputs (a fingerprint of histories, kinds and cell ids from the old and the new code; commit ids carry commit times and are left out), then retire the rest with a tombstone naming the commit that keeps its bytes. Files that records cite by line stay unedited (minds PR #49).
- An ignored run directory is not a place where bytes are kept: at the close of lab's PHS line, phs-soliton v1's 160 checkpoints had lived only in a session worktree's ignored runs/, which was later removed. Its manifests carry every registered metric, but no new state-level analysis of the v1 models (the later honest decoder, for one) is possible without retraining; phs-clock (60 checkpoints, 5 MB) and fringes (35 in a 1.3 MiB snapshot) committed theirs and can re-decode. Commit or archive the weights when the verdict lands, and name what was lost in the closure record (lab CLOSED.md).

**Where.**

- `manifesto`: `CONTROLLED-FORGETTING-0.1.md`
- `sokol-core`: `docs/RETIRED.md`
- `workspace`: `ARCHIVED-WORKSPACE.md` — ~/Projects tombstone
- `workspace`: `ARCHIVED-REPOSITORIES.md`
- `minds`: `experiments/g6/RETIRED.md` — a withdrawn pilot's harness and run data; its report kept unedited, its generator moved to experiments/witness/histories.py (PR #49)
- `lab`: `CLOSED.md` — a closed research line kept in place: three directories stay as results, no new runs; names where each part of the bytes is kept and the v1 checkpoints as lost

<a id="write-actor"></a>
## A write actor decides from trusted inputs only, binds them, and is exercised

**Problem.** An agent or workflow allowed to merge, publish or sign by itself is only as good as the inputs it reads at the moment of the write, and a gate never run on a real case is no evidence that it works.

**Form.**

- One predicate decides, and its twin (the condition for asking a reviewer) shares every fact and rule with it; formats are functions of the one result, never second copies of the logic.
- Only trusted code runs: the base branch's, at the exact commit the forge reports for it. The candidate is read as data (Git objects: ls-tree, cat-file, diff-tree), never checked out, installed or run.
- Authority comes from the base, never from the candidate: configuration, role pins and the trust built from them.
- Every derived input is refused unless it is exactly what it claims: regular files named by their content address, no symlinks or submodules, checks bound to the workflow file that produced them and to the app that posted them.
- The write binds what was read (the forge refuses the merge when the head moved), after reading the base and the candidate again just before it.
- Holds the owner controls without code (a label, a repository variable, disabling the workflow); every refusal reason written where the owner reads it; changes to what decides merging are reviewed, and merged by the owner.
- Negative tests assert the exact set of refusal codes, so a mutant removing one rule is seen even when another rule also refuses.

**Lessons.**

- warrant's autonomy envelope 0.1 was retired without ever merging anything: every production run stopped because the workflow token could not read the branch-protection endpoint it depended on (history/AUTONOMY-ENVELOPE-0.1-RETIREMENT.md at the tag history/warrant-0.x-2026-10-18). Read only what the actor's own token can read, and exercise the write on a real case before relying on it.
- A required check is a name: any workflow of the pull request can post a job called `test`. Bind each required check to its workflow file through its check suite, and refuse a check of that name from another workflow (warrant merge-on-acceptance, G18).
- A merge made with a workflow's GITHUB_TOKEN starts no push workflow: dispatch the base branch's CI after it, or master CI silently stops running (warrant merge-on-acceptance, G23).
- A gate that can merge changes to its own rules lets the acceptor widen its own authority: the gate's configuration, pins, workflows and predicate are owner paths (warrant .warrant/merge.json owner_paths, G29-G30).
- A verifier's checks are its own code, run on another commit: minds `verify-release` reruns today's `run_checks` on each release's commit. A check added for new work would fail every older release still awaiting a verdict on a file its commit never had, and record INVALID under the member's key. Run each check only where the commit carries what it checks (minds `witness_checks`, as `kernel_checks` before it), and exercise it on a real pending release in the fresh clone the verifier uses, with the chain as that release was recorded (minds test 100; the 12 releases awaiting antigravity carry no witness suite).
- So is the interpreter they run under: a dependency upgrade in the verifier changes every older release's run. After minds moved to sigma-glyph 1.0.0, each release recorded on 0.8.0 would have been refused by its own commit's check of the Book I bytes and recorded INVALID, which no later verdict takes back. Run each commit's checks under the requirements that commit pins (minds `interpreter_for`: this interpreter where the commit pins the same bytes or none, otherwise one built once from the commit's file with `--require-hashes`), and record nothing when that interpreter cannot be built: the release was not checked, which is not a failed check. Exercise it on a real pending release (minds test 101; `be482c9`, recorded on 0.8.0, checked by the tool running 1.0.0: 13 of 13 checks passed).

**Where.**

- `warrant`: `tools/claimslib/eligibility.py` — merge-eligible and due-for-review from one predicate; the pull request's head read as Git objects under the base's pins
- `warrant`: `.github/workflows/merge-on-acceptance.yml` — base code only; at most one merge per run, bound to the assessed head; master CI dispatched after it
- `warrant`: `integrations/codex-plugin/waker/waker.py` — runs the base tree's due predicate and wakes the reviewer once per head
- `minds`: `tools/minds_chain.py` — witness_checks and kernel_checks: a release check runs only where the released commit carries it; interpreter_for: under the requirements the commit pins; so verify-release of older releases is unchanged
