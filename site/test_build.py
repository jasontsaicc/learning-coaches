#!/usr/bin/env python3
"""Parser self-check for site/build.py. Run: python3 site/test_build.py"""
from build import (day_phases, leetcode_done, note_target, parse_mastery_line, parse_phases, parse_table,
                   phase_by_day, phase_focus, sd_plan, slug, split_focus)

# Real lines from workspaces/*/progress.md (## Mastery), plus one synthetic colon-in-name case.
MASTERY = [
    ("- P2a Ingress(規則 vs controller、L7 純字串比對): med (s14)",
     ("P2a", "P2a Ingress(規則 vs controller、L7 純字串比對)", "med", 14)),
    ("- L4 vs L7 判準: low-med (s18)", (None, "L4 vs L7 判準", "low-med", 18)),
    ("- P2b C-1 三階梯壽命(可寫層 / emptyDir / PVC): med-high (s26)",
     ("P2b", "P2b C-1 三階梯壽命(可寫層 / emptyDir / PVC)", "med-high", 26)),
    ("- P2b C-4 RBAC 四象限: low(scaffolded) (s33)", ("P2b", "P2b C-4 RBAC 四象限", "low", 33)),
    ("- tgw-vs-peering: high (s2 — only clean pass, transitivity mechanism articulated)",
     (None, "tgw-vs-peering", "high", 2)),
    ("- aws-networking (P1 scope): low (s2 — 1/16 pass at mechanism level; retests pending)",
     (None, "aws-networking (P1 scope)", "low", 2)),
    ("- Load Balancer (Day 4-5): high (s40)— S40 結掉三筆 S4 老錯;Least Connections 命名 33 天又掉,續盯",
     (None, "Load Balancer (Day 4-5)", "high", 40)),
    ("- kubectl debug / ephemeral container: low (2026-09-01,ad hoc 非主線,未經 gate)",
     (None, "kubectl debug / ephemeral container", "low", None)),
    ("- P1 probe: liveness vs readiness: high (s6)", ("P1", "P1 probe: liveness vs readiness", "high", 6)),
    ("- not a mastery line", None),
]
for line, want in MASTERY:
    got = parse_mastery_line(line)
    assert got == want, f"\n line: {line}\n want: {want}\n  got: {got}"

PROGRESS = """## Phase status

- P0 心智模型: gate-passed(2026-06-22,legacy pre-Examiner)
- P2a 網路深水區: in-progress(chunk 1 ✅)
- P3 調度 + 高並發 + 排障: not-started
- P4: not-started

weak-topic flags:
- 七站封包全旅程(4-5):盲講式退役

## Mastery
"""
assert parse_phases(PROGRESS) == [("P0", "心智模型", "gate-passed"), ("P2a", "網路深水區", "in-progress"),
                                  ("P3", "調度 + 高並發 + 排障", "not-started"), ("P4", "", "not-started")], parse_phases(PROGRESS)

LC = """## 做過

- **#1448 Count Good Nodes in Binary Tree** — `tree/count-good-nodes-in-binary-tree/`
  2026-10-09 龜模式首刷。
- **Layer 0 執行模型**:跑了概念 1
- **#21 Merge Two Sorted Lists** — `linked-list/merge-two-sorted-lists/`(harness 在 `x/drill.py`)
  已完成:圖解頁。

## 接下來
"""
done = leetcode_done(LC)
assert done == {"tree/count-good-nodes-in-binary-tree": ("#1448 Count Good Nodes in Binary Tree", "2026-10-09 龜模式首刷。"),
                "linked-list/merge-two-sorted-lists": ("#21 Merge Two Sorted Lists", "已完成:圖解頁。")}, done

CURR = "| **P0 Thinking Framework**(Day 1-3) | x |\n| **P1 Core Building Blocks**(Day 4-16) | y |\n"
ranges = day_phases(CURR)
assert ranges == [("P0", 1, 3), ("P1", 4, 16)], ranges
assert phase_by_day("Load Balancer (Day 4-5)", ranges) == "P1"
assert phase_by_day("Go Refresher (Day -5~-1)", ranges) is None
assert phase_by_day("tgw-vs-peering", ranges) is None

TABLE = "intro\n| Topic | One-Liner |\n|---|---|\n| **LB** | spreads `traffic` |\n| Cache | fast |\n\nafter"
assert parse_table(TABLE) == (["Topic", "One-Liner"], [["LB", "spreads traffic"], ["Cache", "fast"]]), parse_table(TABLE)

TOPICS = [{"id": "t1", "label": "Load Balancer (Day 4-5)", "session": 40},
          {"id": "t2", "label": "P2b C-6 Secret 分層", "session": 38},
          {"id": "t3", "label": "Message Queue (Day 10-11)", "session": 18}]
PH = {"P2a": {}, "P0": {}}
assert note_target("portfolio/sd/notes/day04-05-load-balancer.md", TOPICS, PH) == ["t1"]
assert note_target("portfolio/sd/notes/day10-message-queue-part2.md", TOPICS, PH) == ["t3"]
assert note_target("workspaces/k8s/notes/s38-secrets.md", TOPICS, PH) == ["t2"]
assert note_target("portfolio/k8s/notes/p2a-ingress.md", TOPICS, PH) == ["P2a"]
assert note_target("portfolio/sd/notes/go-01-fundamentals.md", TOPICS, PH) == []
# <meta name="topic"> pins one topic even when the s-prefix would match others; unknown label fails loud
assert note_target("portfolio/k8s/notes/s40-load.html", TOPICS, PH, "Message Queue (Day 10-11)") == ["t3"]
try:
    note_target("portfolio/k8s/notes/s38-x.html", TOPICS, PH, "No Such Topic")
    raise AssertionError("unknown meta topic must raise")
except ValueError:
    pass

DETAIL = """## Phase 0: Thinking Framework (Day 1-3)
### Day 1: What SD Interviews Actually Test
### Phase 0 Gate
## Phase 3: Classic SD Problems (Day 27-59)
### Tier 1: Must Do (Day 27-45)
#### Day 35-37: Chat System ★★★★
#### Day 58-59: Ride Matching (Uber) ★★★★ — Geo Capstone
"""
assert sd_plan(DETAIL) == [("P0", 1, 1, "What SD Interviews Actually Test"), ("P3", 35, 37, "Chat System"),
                           ("P3", 58, 59, "Ride Matching (Uber)")], sd_plan(DETAIL)

K8S_CURR = "| **P2a 網路深水區** ⭐ | Service/kube-proxy、Ingress | P1 gate | x |\n| **P1 Core Building Blocks**(Day 4-16) | LB、caching | P0 gate | y |\n"
CA_CURR = "## P1 Networking Gap-Scan (0.5 week)\n\n**焦點**:找出 AWS networking 的洞。前置:P0。\n\n- x\n\n## Sidecar: Linux\n"
assert phase_focus(K8S_CURR) == {"P2a": ("網路深水區", "Service/kube-proxy、Ingress"), "P1": ("Core Building Blocks", "LB、caching")}, phase_focus(K8S_CURR)
assert phase_focus(CA_CURR) == {"P1": ("Networking Gap-Scan", "找出 AWS networking 的洞。前置:P0。")}, phase_focus(CA_CURR)
assert split_focus("scheduler、affinity/taints、PDB") == ["scheduler", "affinity/taints", "PDB"]
assert split_focus("把 migration 練到能推理,前置:P1") == []
assert slug("Remove Nth Node From End") == "remove-nth-node-from-end"

print("site/test_build.py OK")

# Question banks reject ambiguous or broken references before publication.
from build import validate_chapters, build
from copy import deepcopy
fixture = [{"id":"demo", "coachId":"k8s", "phaseId":"k8s:P1", "title":"Demo",
    "topicRefs":[{"parent":"k8s:P1","label":"Probe"}],
    "objectives":[{"id":"mechanism","label":"Explain"}], "sources":["note.md"],
    "challenge":{"prompt":"Try it", "criteria":["Show evidence"]},
    "questions":[{"id":"q1","revision":1,"type":"choice","objectiveId":"mechanism",
      "prompt":"Why?","hint":"Think","explanation":"Because","source":{"path":"note.md","section":"Probe"},
      "multiple":False,"options":[{"id":"a","text":"A","feedback":"Yes"},{"id":"b","text":"B","feedback":"No"}],"answer":["a"]}]}]
nodes = [{"id":"k8s","kind":"coach"},{"id":"k8s:P1","parent":"k8s","kind":"phase"},
         {"id":"t1","parent":"k8s:P1","label":"Probe","kind":"topic"}]
validate_chapters(fixture, nodes, {"note.md"})
for mutate in [
    lambda c: c.append(deepcopy(c[0])),
    lambda c: c[0]['questions'][0].update(answer=['missing']),
    lambda c: c[0]['questions'][0].update(revision=0),
    lambda c: c[0]['questions'][0]['source'].update(path='../secret'),
    lambda c: c[0]['topicRefs'][0].update(label='Missing'),
    lambda c: c[0]['questions'][0].update(type='order',items=[{'id':'a','text':'A'},{'id':'b','text':'B'}],answer=[['a']]),
    lambda c: c[0]['questions'][0].update(type='fill',answer={'kind':'number','value':1,'tolerance':-1,'unit':'s'}),
]:
    bad = deepcopy(fixture)
    mutate(bad)
    try:
        validate_chapters(bad, nodes, {'note.md'})
    except ValueError:
        pass
    else:
        raise AssertionError(f'Accepted invalid bank: {bad}')
data = build()
assert all(n.get('level') is None for n in data['nodes'] if n.get('practiced'))
assert any(n.get('practiced') for n in data['nodes'])
print('chapter validation OK')

banks = build()['chapters']
assert {c['coachId'] for c in banks} == {'k8s','sd','leetcode','ca'}
for c in banks:
    primary = [q for q in c['questions'] if 'variantOf' not in q]
    assert len(primary) == 6 and len(c['questions']) >= 8
    assert len({q['type'] for q in primary}) >= 3
    assert len({q['objectiveId'] for q in primary}) >= 2
print('four chapter banks OK')

# A missing Mastery grade does not mean the current chapter has not started.
from build import sd_topic_states
state_topics = [
    {'id':'chat','label':'Chat System (Day 35-37)','parent':'sd:P3','planned':True,'files':['chat.md']},
    {'id':'notification','label':'Notification (Day 33-34)','parent':'sd:P3','planned':True,'files':['notification.md']},
    {'id':'cache','label':'Distributed Cache (Day 38-39)','parent':'sd:P3','planned':True,'files':[]},
    {'id':'old','label':'Other (Day 35-37)','parent':'sd:P2','planned':True,'files':[]},
]
progress = '## Current Session breakpoint\n<!-- old Day 38 -->\nP3 / Chat System(Day 35)/ chunk 4 PRIVATE DETAIL\n\nresume: Day 38 later\n\n## Phase status\n'
sd_topic_states(state_topics, progress)
assert state_topics[0]['status'] == 'in-progress' and state_topics[0]['planned'] is False
assert state_topics[0].get('level') is None
assert state_topics[1]['status'] == 'materials-available' and state_topics[1]['planned'] is True
assert state_topics[2]['planned'] is True and not state_topics[2].get('status')
assert state_topics[3]['planned'] is True
assert 'PRIVATE' not in str(state_topics)
assert len([n for n in build()['nodes'] if n['label']=='Chat System (Day 35-37)']) == 1
chat = next(n for n in build()['nodes'] if n['label']=='Chat System (Day 35-37)')
assert chat['parent'] == 'sd:P3'
assert 'portfolio/sd/notes/day35-chat-system.md' in chat['files']
news = next(n for n in build()['nodes'] if n['label']=='News Feed (Day 40-42)')
assert not any('rate-limiter' in f for f in news['files'])
limiter = next(n for n in data['nodes'] if n['label']=='Distributed Rate Limiter (Day 31-32)')
assert 'portfolio/sd/notes/day40-gauntlet-rate-limiter.md' in limiter['files']
assert 'portfolio/sd/notes/day40-gauntlet-rate-limiter-mindmap.md' in limiter['files']
unstarted = [{'label':'Chat System (Day 35-37)','parent':'sd:P3','planned':True,'files':['chat.md']}]
sd_topic_states(unstarted, '## Current Session breakpoint\n<!-- P3 / Chat (Day 35) -->\n')
assert unstarted[0]['status'] == 'materials-available' and unstarted[0]['planned']
print('SD learning status and note placement OK')
