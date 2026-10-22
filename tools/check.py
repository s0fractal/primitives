#!/usr/bin/env python3
"""Everything this repository claims about itself, checked. No candidate is run here."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ok = True


def chk(label, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("ok  " if cond else "FAIL"), label, "" if cond else f"-> {detail}")


cat = json.loads((ROOT / "catalog.json").read_text())
for cls, entry in cat["classes"].items():
    p = ROOT / "vectors" / f"{cls}.json"
    chk(f"{cls}: vector file exists", p.is_file())
    if not p.is_file():
        continue
    doc = json.loads(p.read_text())
    ids = [v["id"] for v in doc["vectors"]]
    chk(f"{cls}: boundary is a declared kind", entry.get("boundary") in cat["boundaries"], entry.get("boundary"))
    chk(f"{cls}: names its bite proof", bool(entry.get("bite_proof")))
    chk(f"{cls}: vector ids unique and prefixed", len(ids) == len(set(ids)) and all(i.startswith(cls + "/") for i in ids))
    chk(f"{cls}: provenance recorded", "commit" in doc["source"] or "authored" in doc["source"], doc["source"])
for p in sorted((ROOT / "vectors").glob("*.json")):
    chk(f"{p.stem}: listed in the catalog", p.stem in cat["classes"])
r = subprocess.run([sys.executable, str(ROOT / "tools" / "manifest.py"), "--check"], capture_output=True, text=True)
chk("MANIFEST.sha256 covers the pack and is current", r.returncode == 0, r.stdout.strip())
r = subprocess.run([sys.executable, str(ROOT / "tools" / "p256_decode.py"), "--selftest"], capture_output=True, text=True)
chk("p256-decode: vectors reproduce and every negative bites", r.returncode == 0, r.stdout.strip().splitlines()[-1:])
r = subprocess.run([sys.executable, str(ROOT / "tools" / "patterns.py"), "--check"], capture_output=True, text=True)
chk("PATTERNS.md is the rendering of patterns.json, and every pattern has an instance", r.returncode == 0,
    r.stdout.strip().splitlines()[:3])
print("\nPRIMITIVES CHECK:", "ALL PASS" if ok else "FAILURES")
sys.exit(0 if ok else 1)
