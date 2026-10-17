#!/usr/bin/env python3
"""Import the warrant conformance classes that are primitives, with provenance.

    python3 tools/import_warrant.py ~/Projects/warrant 41fd08ca73d1b2994b21c638041799db25f0abbc

Reads each class file from that commit (git show, not the working tree), copies
its vectors unchanged, and records the commit and the SHA-256 of the source
bytes in vectors/<class>.json. The vectors are DERIVED: warrant authored them,
and warrant's own selftests (tools/ed25519_edge.py, tools/p256_vectors.py) are
where their bite is proven. This repository re-publishes them so that other
implementations can be held to them without depending on warrant.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ("blob-hash", "canon", "sig-message", "verify-sig")


def main(repo, commit):
    for cls in CLASSES:
        raw = subprocess.run(["git", "-C", repo, "show", f"{commit}:conformance/vectors/{cls}.json"],
                             capture_output=True, check=True).stdout
        src = json.loads(raw)
        doc = {"tag": "primitives.vectors@v0", "class": cls,
               "source": {"repository": "https://github.com/s0fractal/warrant", "commit": commit,
                          "path": f"conformance/vectors/{cls}.json",
                          "sha256": hashlib.sha256(raw).hexdigest()},
               "note": src.get("note", ""), "vectors": src["vectors"]}
        (ROOT / "vectors" / f"{cls}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"{cls}: {len(src['vectors'])} vectors from {commit[:12]}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
