#!/usr/bin/env python3
"""Build the learning-map static site: workspaces/ + portfolio/ -> site/dist/.

Usage: python3 site/build.py [--check]   (--check parses everything, writes nothing)
Any unparseable input raises, so a bad build never reaches deploy.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
ENGINE_COACHES = ["k8s", "sd", "ca"]  # progress.md follows engine/PROGRESS-SCHEMA.md
FILE_EXTS = {".md", ".html"}


def section(text, heading):
    """Body under '## <heading>...' up to the next '## ' heading."""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def parse_mastery_line(line):
    """'- P2a Ingress(...): med (s14)' -> ('P2a', 'P2a Ingress(...)', 'med', 14)

    Returns (phase|None, name, level, session|None), or None if the line doesn't parse.
    level is normalized to one of: low, low-med, med, med-high, high.
    Cases to survive are in site/test_build.py (colon inside the name,
    'low(scaffolded)', a date instead of sN, trailing commentary).
    """
    # Split at the first ': <level-word>', so a colon inside the name survives.
    m = MASTERY_RE.match(line)
    if not m:
        return None
    name, level, level_hi, session = m.groups()
    phase = re.match(r"P\d+[a-z]?(?= )", name)
    return (phase.group(0) if phase else None, name, level + (level_hi or ""),
            int(session) if session else None)


MASTERY_RE = re.compile(r"^- (.+?): (low|med|high)(-med|-high)?\S* \(?(?:s(\d+))?")


PHASE_RE = re.compile(r"^- (P\d+[a-z]?)(?: (.+?))?: ([a-z-]+)", re.M)


def parse_phases(text):
    """'- P2a 網路深水區: in-progress(...)' -> [('P2a', '網路深水區', 'in-progress'), ...]"""
    return PHASE_RE.findall(section(text, "Phase status"))


DONE_RE = re.compile(r"^- \*\*(#\d+ [^*]+)\*\* — `([^`]+?)/?`[^\n]*\n((?:  .*\n?)*)", re.M)


def leetcode_done(text):
    """'## 做過' entries -> {'tree/invert-binary-tree': ('#226 Invert Binary Tree', body)}"""
    return {path: (label, body.strip()) for label, path, body in DONE_RE.findall(section(text, "做過"))}


def files_in(*dirs):
    return sorted(str(p.relative_to(ROOT)) for d in dirs if d.is_dir()
                  for p in d.iterdir() if p.suffix in FILE_EXTS)


DAY_RANGE_RE = re.compile(r"\*\*(P\d+) [^*]+\*\*\(Day (\d+)-(\d+)\)")


def day_phases(curriculum_text):
    """sd curriculum table '**P1 Core Building Blocks**(Day 4-16)' -> [('P1', 4, 16), ...]"""
    return [(p, int(a), int(b)) for p, a, b in DAY_RANGE_RE.findall(curriculum_text)]


def phase_by_day(name, ranges):
    """'Load Balancer (Day 4-5)' -> 'P1' using the curriculum Day ranges; None if no Day."""
    m = re.search(r"Day (\d+)", name)
    return next((p for p, a, b in ranges if m and a <= int(m.group(1)) <= b), None)


def parse_table(text):
    """First markdown table in text -> (header, rows). Cells stripped of '**' and backticks."""
    lines = [l for l in text.splitlines() if l.startswith("|")]
    cells = [[c.strip().replace("**", "").replace("`", "") for c in l.strip().strip("|").split("|")] for l in lines]
    rows = [r for r in cells[1:] if not set("".join(r)) <= set("-: ")]
    return (cells[0], rows) if cells else ([], [])


# Learning-point sources per coach: (file, section heading or None, title, columns to show)
KEYPOINTS = {
    "sd": [("workspaces/sd/one-liner-library.md", None, "One-liners", ["Topic", "One-Liner"]),
           ("workspaces/sd/pattern-map.md", "Pattern 總表", "Pattern map", ["Pattern", "核心零件", "狀態"])],
    "k8s": [("workspaces/k8s/term-registry.md", None, "術語", ["術語 (EN)", "中文點破", "一句英文定義"])],
    "leetcode": [("workspaces/leetcode/one-liner-library.md", None, "Pattern 口訣", ["Pattern", "One-Liner"])],
}


def keypoints(coach):
    out = []
    for path, heading, title, cols in KEYPOINTS.get(coach, []):
        text = (ROOT / path).read_text()
        header, rows = parse_table(section(text, heading) if heading else text)
        missing = [c for c in cols if c not in header]
        if missing:
            raise ValueError(f"{path}: table lost columns {missing} (header: {header})")
        idx = [header.index(c) for c in cols]
        out.append({"title": title, "cols": cols, "rows": [[r[i] for i in idx] for r in rows if len(r) == len(header)]})
    return out


def note_target(filename, topics, phases):
    """Which nodes a note belongs to: 'p2a-ingress.md' -> phase P2a, 's38-secrets.md' -> topics at
    session 38, 'day10-message-queue.md' -> topic whose '(Day 10-11)' range covers 10."""
    stem = Path(filename).stem.lower()
    if m := re.match(r"p(\d+[a-z]?)-", stem):
        return [pid for pid in phases if pid.lower() == f"p{m.group(1)}"]
    if m := re.match(r"s(\d+)-", stem):
        return [t["id"] for t in topics if t["session"] == int(m.group(1))]
    if m := re.match(r"day(\d+)", stem):
        day = int(m.group(1))
        hits = []
        for t in topics:
            r = re.search(r"Day (\d+)(?:-(\d+))?", t["label"])
            if r and int(r.group(1)) <= day <= int(r.group(2) or r.group(1)):
                hits.append(t["id"])
        return hits
    return []


def build():
    nodes = [{"id": "me", "label": "me", "kind": "root"}]

    def add(id_, label, kind, parent, **kw):
        nodes.append({"id": id_, "label": label, "kind": kind, "parent": parent, **kw})
        return nodes[-1]

    for c in ENGINE_COACHES:
        ws = ROOT / "workspaces" / c
        text = (ws / "progress.md").read_text()
        curriculum = ROOT / "skills" / f"{c}-coach" / "references" / "curriculum.md"
        ranges = day_phases(curriculum.read_text()) if curriculum.exists() else []
        notes = files_in(ROOT / "portfolio" / c / "notes", ws / "notes")
        kp = keypoints(c)
        add(c, c, "coach", "me", files=notes, keypoints=kp)
        phases = {}
        for pid, label, status in parse_phases(text):
            phases[pid] = add(f"{c}:{pid}", f"{pid} {label}".strip(), "phase", c, status=status, files=[])
        topics = []
        for i, line in enumerate(l for l in section(text, "Mastery").splitlines() if l.startswith("- ")):
            parsed = parse_mastery_line(line)
            if parsed is None:
                raise ValueError(f"workspaces/{c}/progress.md: unparseable Mastery line: {line}")
            phase, name, level, s = parsed
            phase = phase or phase_by_day(name, ranges)
            parent = f"{c}:{phase}" if phase in phases else c
            # one-liner whose topic name prefixes this topic ("Load Balancer" -> "Load Balancer (Day 4-5)")
            point = next((r[1] for t in kp if t["cols"][0] == "Topic" for r in t["rows"] if name.startswith(r[0])), None)
            topics.append(add(f"{c}:t{i}", name, "topic", parent, level=level, session=s, point=point, files=[]))
        by_id = {n["id"]: n for n in nodes}
        for f in notes:
            for target in note_target(f, topics, phases):
                (phases[target] if target in phases else by_id[target])["files"].append(f)

    lc = ROOT / "workspaces" / "leetcode"
    done = leetcode_done((lc / "progress.md").read_text())
    add("leetcode", "leetcode", "coach", "me", keypoints=keypoints("leetcode"))
    for group in sorted(d for d in lc.iterdir() if d.is_dir() and d.name != "archive"):
        add(f"lc:{group.name}", group.name, "phase", "leetcode")
        for prob in sorted(d for d in group.iterdir() if d.is_dir()):
            key = f"{group.name}/{prob.name}"
            label = done[key][0] if key in done else prob.name
            add(f"lc:{key}", label, "problem", f"lc:{group.name}",
                level="high" if key in done else None, files=files_in(prob))

    return {"nodes": nodes}


def main():
    data = build()
    topics = sum(n["kind"] == "topic" for n in data["nodes"])
    linked = sum(bool(n.get("files")) for n in data["nodes"] if n["kind"] in ("topic", "phase"))
    print(f"{len(data['nodes'])} nodes, {topics} topics, {linked} topics/phases with notes")
    if "--check" in sys.argv:
        return
    shutil.rmtree(DIST, ignore_errors=True)
    (DIST / "files").mkdir(parents=True)
    for f in {f for n in data["nodes"] for f in n.get("files", [])}:
        dst = DIST / "files" / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f, dst)
    (DIST / "data.json").write_text(json.dumps(data, ensure_ascii=False))
    shutil.copy2(ROOT / "site" / "index.html", DIST / "index.html")
    shutil.copytree(ROOT / "site" / "img", DIST / "img")
    print(f"wrote {DIST}")


if __name__ == "__main__":
    main()
