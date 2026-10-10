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


# Learning-point sources per coach: (file, section heading or None, title, columns to show, flashcard prompt)
KEYPOINTS = {
    "sd": [("workspaces/sd/one-liner-library.md", None, "One-liners", ["Topic", "One-Liner"], "用一句話講給面試官聽"),
           ("workspaces/sd/pattern-map.md", "Pattern 總表", "Pattern map", ["Pattern", "核心零件", "狀態"], "核心零件有哪些？")],
    "k8s": [("workspaces/k8s/term-registry.md", None, "術語", ["術語 (EN)", "中文點破", "一句英文定義"], "中文點破 + 英文定義？")],
    "leetcode": [("workspaces/leetcode/one-liner-library.md", None, "Pattern 口訣", ["Pattern", "One-Liner"], "口訣是什麼？")],
}


def keypoints(coach):
    out = []
    for path, heading, title, cols, prompt in KEYPOINTS.get(coach, []):
        text = (ROOT / path).read_text()
        header, rows = parse_table(section(text, heading) if heading else text)
        missing = [c for c in cols if c not in header]
        if missing:
            raise ValueError(f"{path}: table lost columns {missing} (header: {header})")
        idx = [header.index(c) for c in cols]
        out.append({"title": title, "cols": cols, "prompt": prompt, "rows": [[r[i] for i in idx] for r in rows if len(r) == len(header)]})
    return out


def note_target(filename, topics, phases):
    """Which nodes a note belongs to: 'p2a-ingress.md' -> phase P2a, 's38-secrets.md' -> topics at
    session 38, 'day10-message-queue.md' -> topic whose '(Day 10-11)' range covers 10."""
    stem = Path(filename).stem.lower()
    if m := re.match(r"p(\d+[a-z]?)-", stem):
        return [pid for pid in phases if pid.lower() == f"p{m.group(1)}"]
    if m := re.match(r"s(\d+)-", stem):
        return [t["id"] for t in topics if t.get("session") == int(m.group(1))]
    if m := re.match(r"day(\d+)", stem):
        day = int(m.group(1))
        hits = []
        for t in topics:
            r = re.search(r"Day (\d+)(?:-(\d+))?", t["label"])
            if r and int(r.group(1)) <= day <= int(r.group(2) or r.group(1)):
                hits.append(t["id"])
        return hits
    return []


SD_DAY_RE = re.compile(r"^#{3,4} Day (\d+)(?:-(\d+))?: (.+)$", re.M)


def sd_plan(detail_text):
    """curriculum-detail '### Day 4-5: Load Balancer & Reverse Proxy' under '## Phase 1: ...'
    -> [('P1', 4, 5, 'Load Balancer & Reverse Proxy'), ...]"""
    out = []
    for chunk in re.split(r"^## Phase (\d+):[^\n]*\n", detail_text, flags=re.M)[1:]:
        if chunk.isdigit():
            phase = f"P{chunk}"
            continue
        out += [(phase, int(a), int(b or a), re.sub(r"\s*[★☆—].*$", "", t).strip())
                for a, b, t in SD_DAY_RE.findall(chunk)]
    return out


def phase_focus(curriculum_text):
    """Phase -> (name, focus). Table rows '| **P2a 網路深水區** ⭐ | focus | ...' (k8s/sd) or
    '## P1 Networking Gap-Scan (0.5 week)' followed by a '**焦點**:...' line (ca)."""
    out = {}
    for pid, name, focus in re.findall(r"^\| \*\*(P\d+[a-z]?) ([^*]+)\*\*[^|]*\| ([^|]+) \|", curriculum_text, re.M):
        out[pid] = (re.sub(r"\(Day [^)]*\)", "", name).strip(), focus.strip())
    for pid, name, body in re.findall(r"^## (P\d+[a-z]?) (.+?)(?: \([^)]*\))?\n(.*?)(?=^## |\Z)", curriculum_text, re.M | re.S):
        m = re.search(r"\*\*焦點\*\*[:：]\s*(.+)", body)
        out.setdefault(pid, (name.strip(), m.group(1).strip() if m else ""))
    return out


def split_focus(focus):
    """'scheduler、affinity/taints、HPA/VPA/Karpenter' -> ['scheduler', 'affinity/taints', 'HPA/VPA/Karpenter']"""
    return [x.strip() for x in focus.split("、") if x.strip()] if "、" in focus else []


LC_ROW_RE = re.compile(r"^\| (\d+) \| ([^|]+?) \|", re.M)


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def build():
    nodes = [{"id": "me", "label": "me", "kind": "root"}]

    def add(id_, label, kind, parent, **kw):
        nodes.append({"id": id_, "label": label, "kind": kind, "parent": parent, **kw})
        return nodes[-1]

    for c in ENGINE_COACHES:
        ws = ROOT / "workspaces" / c
        text = (ws / "progress.md").read_text()
        refs = ROOT / "skills" / f"{'cloud-architect' if c == 'ca' else c}-coach" / "references"
        curriculum = (refs / "curriculum.md").read_text()
        ranges, focus = day_phases(curriculum), phase_focus(curriculum)
        notes = files_in(ROOT / "portfolio" / c / "notes", ws / "notes")
        kp = keypoints(c)
        add(c, c, "coach", "me", files=notes, keypoints=kp)
        phases = {}
        for pid, label, status in parse_phases(text):
            name, plan = focus.get(pid, (label, ""))
            phases[pid] = add(f"{c}:{pid}", f"{pid} {label or name}".strip(), "phase", c,
                              status=status, plan=plan, files=[])
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
        # planned (not yet taught) lessons from the curriculum, shown grey on the path
        if c == "sd":
            taught = [tuple(map(int, m.groups(default=0))) for t in topics
                      if (m := re.search(r"Day (\d+)(?:-(\d+))?", t["label"]))]
            for j, (pid, a, b, title) in enumerate(sd_plan((refs / "curriculum-detail.md").read_text())):
                if pid in phases and not any(x <= b and a <= (y or x) for x, y in taught):
                    topics.append(add(f"{c}:plan{j}", f"{title} (Day {a}{f'-{b}' if b != a else ''})", "topic", f"{c}:{pid}", planned=True, files=[]))
        else:
            for pid, ph in phases.items():
                if ph["status"] == "not-started" and not any(t["parent"] == ph["id"] for t in topics):
                    for j, item in enumerate(split_focus(ph["plan"])):
                        add(f"{c}:{pid}:plan{j}", item, "topic", ph["id"], planned=True)
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
    have = {re.match(r"#(\d+)", n["label"]).group(1) for n in nodes if re.match(r"#\d+", n["label"])}
    have |= {n["id"].rsplit("/", 1)[-1] for n in nodes if n["id"].startswith("lc:") and "/" in n["id"]}
    for num, title in LC_ROW_RE.findall((ROOT / "skills/leetcode-coach/references/curriculum.md").read_text()):
        if num not in have and slug(title) not in have:
            add(f"lc:plan{num}", f"#{num} {title}", "problem", "lc:linked-list", planned=True, files=[])
    # extra leetcode notes (e.g. saved artifact pages) attach by slug: notes/<problem-slug>.html
    by_slug = {slug(re.sub(r"^#\d+ ", "", n["label"])): n for n in nodes if n["kind"] == "problem"}
    by_slug |= {n["id"].rsplit("/", 1)[-1]: n for n in nodes if n["kind"] == "problem" and "/" in n["id"]}
    for f in files_in(ROOT / "portfolio" / "leetcode" / "notes"):
        if (n := by_slug.get(Path(f).stem)):
            n["files"] = n.get("files", []) + [f]

    titles = {}
    for f in {f for n in nodes for f in n.get("files", []) if f.endswith(".html")}:
        m = re.search(r"<title>([^<]+)", (ROOT / f).read_text(errors="ignore"))
        if m:
            titles[f] = m.group(1).strip()
    return {"nodes": nodes, "titles": titles}


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
