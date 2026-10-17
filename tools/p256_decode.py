#!/usr/bin/env python3
"""The `p256-decode` class: compressed SEC1 P-256 key -> point, or refusal.

    python3 tools/p256_decode.py --emit       # write vectors/p256-decode.json
    python3 tools/p256_decode.py --selftest   # prove each vector, and that each negative bites

Why a class of its own: end-to-end signature vectors cannot test a decoder's
refusals. A reject vector carries a real signature under another key, so it fails
for that reason whatever the decoder does. That was measured in warrant (impl-rs,
2026-10-16): with its on-curve, x < p and prefix checks removed, the Rust decoder
still passed every signature vector. Here the decoder is asked directly.

Input `{"key": "<hex>"}`. Output `{"point": {"x": "<64 hex>", "y": "<64 hex>"}}`
or `{"point": null}`. The rules are warrant WRT-019's: exactly 33 bytes, lowercase
hex, prefix 02 or 03, x < p, x^3 - 3x + b a square mod p; y is the root whose
parity matches the prefix.

Expected outputs are computed here with plain integer arithmetic. The selftest
cross-checks every accepted point against Python `cryptography`, and for every
negative names a lenient decoder that would have accepted it.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "vectors" / "p256-decode.json"
P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5


def h32(n):
    return n.to_bytes(32, "big").hex()


def rhs(x):
    return (x * x * x - 3 * x + B) % P


def is_square(v):
    return v == 0 or pow(v, (P - 1) // 2, P) == 1


def decode(key_hex):
    """The reference rule. Returns (x, y) or None."""
    if not (isinstance(key_hex, str) and re.fullmatch(r"0[23][0-9a-f]{64}", key_hex)):
        return None
    x = int(key_hex[2:], 16)
    if x >= P or not is_square(rhs(x)):
        return None
    y = pow(rhs(x), (P + 1) // 4, P)
    if y % 2 != int(key_hex[:2], 16) % 2:
        y = P - y
    return x, y


def lenient(key_hex):
    """A decoder that takes uppercase, reduces x mod p and accepts uncompressed keys."""
    try:
        raw = bytes.fromhex(key_hex)
    except (ValueError, TypeError):
        return None
    if len(raw) == 65 and raw[0] == 4:
        return int.from_bytes(raw[1:33], "big"), int.from_bytes(raw[33:], "big")
    if len(raw) != 33 or raw[0] not in (2, 3):
        return None
    x = int.from_bytes(raw[1:], "big") % P
    if not is_square(rhs(x)):
        return None
    y = pow(rhs(x), (P + 1) // 4, P)
    return x, (y if y % 2 == raw[0] % 2 else P - y)


def first_x(want_square, start=0):
    x = start
    while is_square(rhs(x)) != want_square:
        x += 1
    return x


def cases():
    g = ("02" if GY % 2 == 0 else "03") + h32(GX)
    g_other = ("03" if GY % 2 == 0 else "02") + h32(GX)
    x0 = first_x(True)                     # 0: b is a square mod p
    x_bad = first_x(False)                 # 1
    pos = [
        ("generator, its own parity", g),
        ("generator x with the other parity: the point -G", g_other),
        (f"x = {x0}, the smallest x on the curve", "02" + h32(x0)),
        ("x = p - 1 if on the curve, else the largest such x below it",
         "02" + h32(next(x for x in range(P - 1, P - 1000, -1) if is_square(rhs(x))))),
    ]
    neg = [
        (f"x = p + {x0}: an alias of x = {x0} (two strings, one point)", "02" + h32(P + x0)),
        ("x = p", "02" + h32(P)),
        (f"x = {x_bad}: x^3 - 3x + b is not a square, no point has this x", "02" + h32(x_bad)),
        ("the generator UNCOMPRESSED (04 || x || y): one key, one encoding", "04" + h32(GX) + h32(GY)),
        ("the generator in UPPERCASE hex: one key, one string", g.upper()),
    ] + [(f"prefix {p:02x}", f"{p:02x}" + h32(GX)) for p in (0, 1, 4, 5, 6, 7)] + [
        ("32 bytes: the prefix missing", h32(GX)),
        ("34 bytes: one byte too many", g + "00"),
        ("empty", ""),
        ("not hex", "zz" + h32(GX)),
    ]
    return pos, neg


def build():
    pos, neg = cases()
    vectors = []
    for i, (why, key) in enumerate(pos):
        x, y = decode(key)
        vectors.append({"id": f"p256-decode/accept-{i:02d}", "polarity": "positive", "spec": "WRT-019",
                        "why": why, "input": {"key": key}, "expect": {"point": {"x": h32(x), "y": h32(y)}}})
    for i, (why, key) in enumerate(neg):
        vectors.append({"id": f"p256-decode/reject-{i:02d}", "polarity": "negative", "spec": "WRT-019",
                        "why": f"MUST NOT decode: {why}", "input": {"key": key}, "expect": {"point": None}})
    return {"tag": "primitives.vectors@v0", "class": "p256-decode",
            "source": {"authored": "tools/p256_decode.py"},
            "note": ("A compressed SEC1 P-256 key, decoded alone. Negatives are encodings a lenient "
                     "decoder accepts or that are malformed for a named reason; see the selftest."),
            "vectors": vectors}


def selftest():
    from cryptography.hazmat.primitives.asymmetric import ec
    doc = build()
    ok = doc == json.loads(OUT.read_text()) if OUT.exists() else False
    print(("ok  " if ok else "FAIL"), "committed vectors reproduce byte-exactly")
    for v in doc["vectors"]:
        key = v["input"]["key"]
        if v["polarity"] == "positive":
            pt = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), bytes.fromhex(key)).public_numbers()
            good = (h32(pt.x), h32(pt.y)) == (v["expect"]["point"]["x"], v["expect"]["point"]["y"])
            note = "matches cryptography"
        else:
            good = decode(key) is None
            bites = lenient(key) is not None
            note = "a lenient decoder accepts it" if bites else "malformed for the reason named"
        ok &= good
        print(("ok  " if good else "FAIL"), v["id"], "|", v["why"][:70], "|", note)
    print("P256-DECODE VECTORS:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--emit" in sys.argv:
        OUT.write_text(json.dumps(build(), indent=2) + "\n")
        print(f"wrote {OUT.relative_to(ROOT)}")
    elif "--selftest" in sys.argv:
        sys.exit(selftest())
    else:
        print(__doc__)
