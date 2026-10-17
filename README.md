# primitives

One source of truth for the **behaviour** of the primitives our implementations
share: hashes, canonical JSON, signature messages, Ed25519, P-256. This is not
shared **code**. Nothing here is imported at run time. Each implementation keeps its
own code and is held to the same vectors through a small probe.

Why not a shared library: independent implementations are the evidence. When
Python (`cryptography`), Go (standard library) and Rust (written from scratch) agree,
that says something about the specification. A library they all import would only
agree with itself, and one bug would pass everywhere at once.

## What is here

| Class | What | Boundary | Vectors |
|---|---|---|---|
| `blob-hash` | SHA-256 over raw bytes | deterministic | 4, from warrant |
| `canon` | RFC 8785 bytes of a warrant body, and its WarrantID | deterministic | 52, from warrant |
| `sig-message` | the 47 bytes a warrant signature covers | deterministic | 4, from warrant |
| `verify-sig` | Ed25519 (cofactorless, weak keys rejected) and P-256 with `alg` | deterministic | 50, from warrant |
| `p256-decode` | a compressed P-256 key decoded **alone** | deterministic | 19, authored here |

[catalog.json](catalog.json) holds each class's boundary, its spec, where the proof
that its negatives bite lives, and the registered implementations. Vectors imported
from warrant carry the commit and the SHA-256 of their source file
([tools/import_warrant.py](tools/import_warrant.py)).

## Why `p256-decode` exists (measured)

End-to-end signature vectors cannot test a decoder's refusals. A reject vector carries
a real signature under another key, so it fails for that reason whatever the decoder
does. Measured on warrant's Rust implementation (2026-10-17), with a check removed
from its P-256 decoder:

| Mutant | `verify-sig` | `p256-decode` |
|---|---|---|
| no `x < p` check (so `02‖p` decodes as an alias of `02‖0`) | 50/50 pass, **blind** | 2 MUST-REJECT accepted |
| no on-curve check | 50/50 pass, **blind** | 1 MUST-REJECT accepted |

`tools/p256_decode.py --selftest` shows that each negative is either accepted by a
lenient decoder (x reduced mod p, uppercase hex, uncompressed keys) or malformed for
a named reason.

## Using it

Any program that answers one request on stdin can be held to the pack. The protocol
is warrant's conformance protocol, so warrant's three CLIs need no adapter:

```bash
python3 run.py --candidate "warrant-rs probe"
python3 run.py --candidate "python3 adapters/black_heart_probe.py" --class verify-sig
```

A consumer vendors a released pack and checks [MANIFEST.sha256](MANIFEST.sha256)
against the digest it pins (`run.py` refuses a pack whose files do not match its
manifest). When a defect is found in one implementation, its vector lands here, and
every consumer meets it at its next pin bump.

## Measured implementations (2026-10-17)

| Implementation | blob-hash | canon | sig-message | verify-sig | p256-decode |
|---|---|---|---|---|---|
| warrant Python, `master` 41fd08c | 4/4 | 52/52 | 4/4 | 50/50 | UNRUN (no probe class yet) |
| warrant Go, same | 4/4 | 52/52 | 4/4 | 50/50 | UNRUN |
| warrant Rust, same | 4/4 | 52/52 | 4/4 | 50/50 | UNRUN |
| warrant `master` c2215c1, after PR #123 (Python, Go, Rust) | 4/4 | 52/52 | 4/4 | 50/50 | 19/19 |
| black-heart `crypto.py` via adapter | UNRUN | UNRUN | UNRUN | 34/34 Ed25519, 16 P-256 UNRUN | UNRUN |
| warrant before WRT-019 (old checkout) | 4/4 | 52/52 | 4/4 | 47/50: rejects both P-256 positives, **accepts** an Ed25519 signature labelled P-256 | UNRUN |

```bash
python3 tools/check.py      # catalog, manifest, provenance, p256-decode selftest
```

License: MIT.
