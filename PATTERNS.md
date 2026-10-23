# Shared patterns

Methods our projects share, as forms with their instances and lessons: shared method, not shared code. Each project keeps its own implementation; before building one of these, read its entry and start from the form and the lessons, not from scratch. PATTERNS.md is rendered from this file (python3 tools/patterns.py --write); tools/check.py refuses a hand-edited PATTERNS.md, and `python3 tools/patterns.py --locate ~/Projects` checks every instance path in local checkouts.

- [Claims are the source; documents are views](#claims-are-the-source)
- [A check counts only when a mutant breaks it](#mutants-burn-claims)
- [Generate or refuse; do not enumerate or parse](#generate-or-refuse)
- [Independent implementations held to shared vectors](#vectors-not-shared-code)
- [Admit by evidence, never by an admin](#admission-by-evidence)
- [Order is witnessed, not claimed](#witnessed-order)
- [A cache changes cost, never the answer](#verified-cache)
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
- A view's state label says what the engine decided, not only what the holder must do next: a discharge the engine held UNMET_CONDITION (its prerequisite still open) read 'no closure filed' in ROADMAP.md (warrant tools/roadmap.py need, roadmap_test P14).
- One mechanism for every contract: an application interface's rules go into the same claims document as a new pinned section, not into a second claims tool or document (warrant SPEC §10, the agent interface: 86 claims; AGENT.md became the operator's guide pointing to it). The tool needed only the placement of a new section's heading and first sentence (claims.py heading --section N, add --after N).

**Where.**

- `warrant`: `tools/claimslib` — normative SPEC.md sentences filed as Warrant 2 records in .warrant/store; SPEC-CLAIMS.md is the generated view (tools/claims.py is the command; one module per responsibility since warrant #176)
- `warrant`: `SPEC-CLAIMS.md` — generated; `tools/claims.py check` refuses a differing file
- `warrant`: `tools/roadmap.py` — goals (unowned questions) and obligations (duties that answer them) as Warrant 2 records in .warrant/store; ROADMAP.md is the generated view, byte-compared; nothing renders into SPEC.md
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
- Give every mutant run a fresh bytecode cache: an earlier same-size mutant's cache can be loaded instead (minds tools/run_mutants.py, PR #4 round 3).
- End-to-end vectors can be blind to a component's refusals; measure with a mutant before trusting them (primitives p256-decode).
- A guard is burned only when removing it lets the forbidden write happen. If the code right after the guard would crash without it, the mutant is killed by the crash and proves nothing: make that code total, so the lost property is what the mutant exposes (warrant PR #170: M327 and M335 were first killed by an IndexError).
- A mutant run means nothing over a red baseline: a runner that counts a kill when the target case fails also counts a case that fails without any mutant (warrant #170 AMEND 1: M300-M318 read killed while roadmap_test was red). Make the runner refuse it: run each targeted test file once unmutated, in the same copy the mutants use, and refuse the whole run when a target case fails there (warrant #172: BASELINE_RED, exit 2; master's runner read M25 and A09 killed over a planted red case).
- A sharded mutant run claims coverage only when a merge proves it: the parts' union is the whole list, no id is in two parts, each row is the current definition over the same sources, and each kill is recomputed from the row's own case results, not read from its label (warrant #172: tests/mutants.py --merge, in the required check).
- Read the map from the code's side too: claims listing their mutants say nothing about the statements no mutant changes. On warrant 3f2be6a, 274 of 2820 statements of warrant/ and warrant_agent/ were changed by a mutant a BACKED claim cites, and 9 cited mutants only insert code before a statement, so their claims reach no existing statement (warrant tools/claims.py why --uncovered).
- A case that reads its results through an asserting helper (ok(), a bare ['ok'] index) dies before its own check: a mutant that breaks that call is killed by the exception, or lost with every case after it, never on the case's assertion. Read results with .get in the case a mutant targets (warrant agent_write_test W04 and W07, mutants A72 and A78).
- Generated mutants find blind spots; they never back a claim. Keep them in a harness the claims checker does not know, so a citation of one is refused (warrant tests/generated_mutants.py, UNKNOWN_MUTANT). A survivor is closed by a witness that kills it on an assertion plus a curated mutant the claim cites (warrant #178: R49, M475 and M476 under SPEC-4.5-1).
- Name a generated mutant by what it changes, not where: hash the file, scope, the statement's syntax, its occurrence among equal statements, the operator and the site. A positional key shifts with every insert above it, and a run-to-run diff (BLIND: killed before, surviving now) then means nothing.
- Select tests per mutant from a line-coverage map made once per tree from the unmutated run, which doubles as the red baseline. Trace subprocesses too (a sitecustomize.py on PYTHONPATH, a SIGTERM handler that dumps): a test that overwrote PYTHONPATH hid the MCP server it starts, and its statements read NOT_RUN.
- A hunt's exit status says the run happened, never what survived; its merge recomputes each outcome from its row instead of requiring KILLED. A TIMEOUT depends on the runner's load (six mutants flipped SURVIVED -> TIMEOUT between two local runs): never let it make a later survivor BLIND.
- Boundaries are what hand-written mutants miss: of 8632 generated mutants of warrant (#178), the survivors closed first were `<=`/`<` and `>`/`>=` on attenuation, a depth bound with no case at 256/257, and a trust file binding one key twice. A survivor whose guard no input reaches is equivalent: record it with its reason under review, and name the entry when a test later kills it.
- An assertRaisesRegex failing with "X does not match Y" is no kill: the expected exception was raised, the input is still refused, only the message moved (another layer or the crash net caught it). minds found 23 of 203 such kills. Decide it where assertRaises checks (wrap _AssertRaisesContext.__exit__), not from printed lines: a multi-line message defeated the first line filter (Codex, minds PR #15). An import-time assert that refuses the mutant before the test runs is no kill either.
- A refusal held by several layers (minds append-only: Check #2, the reader's status and mode checks, then the read of a deleted entry itself; a host guard and the pinned kernel) cannot be burned by guard mutants, even all of them together: its honest status is unburned, with the layers named. Build the vector that only one rule breaks first (delete an orphan atom, not change a mode): an ambiguous vector hides which layer refused.
- Cargo decides what to rebuild by modification time: mutants built into a shared target were served the previous mutant's build (three false kills in minds). Build each kernel mutant in a fresh target, and refuse a build byte-equal to the pinned kernel as equivalent.

**Where.**

- `minds`: `tools/run_mutants.py` — mutants.json; TwinDivergence also counts as a kill; tools/mutant_test.py decides wording-only failures inside assertRaises (PR #15)
- `warrant`: `tests/mutants.py` — cited per claim in SPEC-CLAIMS.md; BASELINE_RED guard, --shard K/N and --merge (PR #172)
- `warrant-pdf`: `tools/mutants.json`
- `warrant-vet`: `tools/mutants.json`
- `sokol-core`: `.cargo/mutants.toml` — cargo-mutants
- `primitives`: `tools/p256_decode.py` — --selftest: every negative bites
- `warrant`: `tools/claimslib/why.py` — why FILE:LINE: a statement -> the mutants that change it -> the BACKED claims citing them -> obligations -> goals; why --uncovered: the statements no cited mutant changes
- `warrant`: `tests/generated_mutants.py` — generated mutants and survivors: discovery, never backing; .github/workflows/survivors.yml weekly, with claims.py audit pairs

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
- `minds`: `assurance.json`
- `warrant`: `SPEC-CLAIMS.md`
- `warrant`: `warrant/shapes.py` — hex64, hex128, the view token, the question reference and the actor id, defined once; tests/shapes_test.py S6 refuses a hex pattern written anywhere else
- `warrant`: `tests/agent_repo_test.py` — Q01 reads AGENT.md's roadmap recipe and compares stores byte for byte with tools/roadmap.py; Q02 runs it over stdio MCP

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

**Where.**

- `minds`: `vars1.py` — the gate: refs/vars/heads/<scope> is a linear chain moved by `git update-ref` compare-and-swap; append-only checked by `git diff-tree --diff-filter=a`; birth = first commit holding an object (VARS-1 §3, §4.1)
- `warrant`: `warrant/engine.py` — View._chains / before / ordered; Holders.at(pos, filing): a filer's own records in chain order (SPEC-4-8..4-10, SPEC-4.1-11/12)
- `warrant`: `warrant/store.py` — Store.append / Store.extend: prev from the actor's head under a lock on records/; warrant-agent commit refuses CHAIN_MOVED

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
