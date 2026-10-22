#!/usr/bin/env python3
"""PATTERNS.md as a rendering of patterns.json.

    python3 tools/patterns.py --write                 # render PATTERNS.md
    python3 tools/patterns.py --check                 # the file is the rendering, and the data is well formed
    python3 tools/patterns.py --locate ~/Projects     # every instance path exists in its local checkout
                                                      # (repo "workspace" is the folder itself)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("id", "name", "problem", "form", "lessons", "instances")


def render(doc: dict) -> str:
    out = ["# Shared patterns", "", doc["about"], ""]
    out += [f"- [{p['name']}](#{p['id']})" for p in doc["patterns"]] + [""]
    for p in doc["patterns"]:
        out += [f'<a id="{p["id"]}"></a>', f"## {p['name']}", "", f"**Problem.** {p['problem']}", "", "**Form.**", ""]
        out += [f"- {f}" for f in p["form"]] + [""]
        if p["lessons"]:
            out += ["**Lessons.**", ""] + [f"- {x}" for x in p["lessons"]] + [""]
        out += ["**Where.**", ""]
        out += [f"- `{i['repo']}`: `{i['path']}`" + (f" — {i['note']}" if i["note"] else "") for i in p["instances"]] + [""]
    return "\n".join(out)


def problems(doc: dict) -> list:
    errs = []
    ids = [p.get("id") for p in doc["patterns"]]
    if len(ids) != len(set(ids)):
        errs.append("pattern ids are not unique")
    for p in doc["patterns"]:
        errs += [f"{p.get('id')}: missing {f}" for f in FIELDS if f not in p]
        if not p.get("instances"):
            errs.append(f"{p.get('id')}: no instance: a pattern nobody uses is an idea, not a pattern")
        errs += [f"{p.get('id')}: an instance needs repo and path" for i in p.get("instances", [])
                 if not i.get("repo") or not i.get("path")]
    return errs


def main(argv: list) -> int:
    doc = json.loads((ROOT / "patterns.json").read_text())
    if "--write" in argv:
        (ROOT / "PATTERNS.md").write_text(render(doc))
    errs = problems(doc)
    md = ROOT / "PATTERNS.md"
    if not md.is_file() or md.read_text() != render(doc):
        errs.append("PATTERNS.md is not the rendering of patterns.json (python3 tools/patterns.py --write)")
    if "--locate" in argv:
        base = Path(argv[argv.index("--locate") + 1]).expanduser()
        for p in doc["patterns"]:
            for i in p["instances"]:
                where = base / ("" if i["repo"] == "workspace" else i["repo"]) / i["path"]
                if not where.exists():
                    errs.append(f"{p['id']}: {i['repo']}:{i['path']} not found under {base}")
    for e in errs:
        print("FAIL", e)
    print("patterns:", "ok" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
