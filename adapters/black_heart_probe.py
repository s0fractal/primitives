#!/usr/bin/env python3
"""A probe for black-heart's from-scratch Ed25519 (crypto.py), which has no CLI.

    BLACK_HEART=~/Projects/black-heart python3 adapters/black_heart_probe.py < request.json

Answers `verify-sig` for Ed25519 entries (no `alg`) and declines everything
else: black-heart has no P-256, no warrant canonicalization, no decoder to ask.
Declining is reported UNRUN by run.py, which is the honest result.
"""
import json
import os
import sys

req = json.loads(sys.stdin.read())
out = {"warrant_conformance": "1", "id": req.get("id")}
inp = req.get("input", {})
if req.get("class") != "verify-sig" or "alg" in inp:
    out["unsupported"] = "black-heart crypto.py: Ed25519 verify-sig only"
else:
    sys.path.insert(0, os.path.expanduser(os.environ.get("BLACK_HEART", "~/Projects/black-heart")))
    import crypto  # black-heart's own module
    try:
        msg = b"warrant-sig-v1:" + bytes.fromhex(inp["warrant_id"])
        valid = len(bytes.fromhex(inp["warrant_id"])) == 32 and crypto.verify_bytes(
            bytes.fromhex(inp["key"]), msg, bytes.fromhex(inp["sig"])) is True
    except (ValueError, TypeError, KeyError):
        valid = False
    out["output"] = {"valid": valid}
print(json.dumps(out))
