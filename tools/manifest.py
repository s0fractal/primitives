#!/usr/bin/env python3
"""Write or check MANIFEST.sha256 over the pack (run.py, catalog.json, vectors/)."""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def lines():
    files = ["catalog.json", "run.py"] + sorted(str(p.relative_to(ROOT)) for p in (ROOT / "vectors").glob("*.json"))
    return "".join(f"{hashlib.sha256((ROOT / f).read_bytes()).hexdigest()}  {f}\n" for f in files)


if __name__ == "__main__":
    m = ROOT / "MANIFEST.sha256"
    if "--check" in sys.argv:
        ok = m.is_file() and m.read_text() == lines()
        print("MANIFEST:", "in sync" if ok else "STALE (run tools/manifest.py)",
              hashlib.sha256(m.read_bytes()).hexdigest() if m.is_file() else "")
        sys.exit(0 if ok else 1)
    m.write_text(lines())
    print("pack digest", hashlib.sha256(m.read_bytes()).hexdigest())
