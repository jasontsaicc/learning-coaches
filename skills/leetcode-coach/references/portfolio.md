# Portfolio

## Workspace Directory

Progress file, registries, and per-problem work live in:

```
${CLAUDE_SKILL_DIR}/../../workspaces/leetcode/
```

這個目錄是 git-tracked 學習狀態(跨機器同步:每堂課後 commit + push,開課前 pull,
協定見 SKILL.md Session Sync)。內容:

- `progress.md`: engine 的進度檔。Schema engine-owned,定義在 `engine/PROGRESS-SCHEMA.md`,
  本 coach 不重定義。
- `patterns.md`: cross-pattern playbook。學生用自己的話寫每個 pattern 的 skeleton、
  4-question bridge、何時使用。這是面試前真正的複習 artifact,也是 Weekly Review
  artifact audit 的對象。
- `one-liner-library.md`: domain registry(每 pattern 一句「訊號 → pattern + 為什麼」,
  standalone 時期的 Pattern One-Liner Library 遷入)。沿用 PROGRESS-SCHEMA section 7
  的 registry 欄位進間隔抽考。
- `skeleton-registry.md`: domain registry(~8-10 個核心 skeleton 的 recall 排程,
  觸發條件見 `teaching-elements.md` Skeleton Registry;code 本體在
  `references/pattern-cheatsheet.md`)。
- `<phase>/<slug>/`: per-problem folders(下方 layout)。
- `archive/pre-migration/`: standalone 時期的原始狀態檔,verbatim 保存,不再更新。

Canonical per-problem layout (the Lab-Manager and phase gates reuse this):

```
workspaces/leetcode/
  p1-arrays-hashing/
    two-sum/
      solution.py        # the student's solution (or co-written via fill-in-the-blank)
      test_two_sum.py    # provided tests, incl. the large-N timing case
      notes.md           # per-problem notes: the diagram drawn, the code, the red mistakes
```

- **Solution path:** `workspaces/leetcode/<phase>/<slug>/solution.py`. This is what
  `lab-lc.sh` runs and what the Examiner receives.
- **Notes path:** `workspaces/leetcode/<phase>/<slug>/notes.md`, written in engine
  step H. Co-located so a problem folder is self-contained (diagram + solution +
  tests + notes together).
- Phase directory names: `p0-mental-model`, `p1-arrays-hashing`, `p2-window-stack`,
  `p3-binsearch-linkedlist`, `p4-trees`, `p5-heap-backtracking`, `p6-graphs-dp`,
  `p7-interview-sprint`.

## Per-Phase Artifacts

| Phase | Artifact |
|-------|----------|
| P0 | No problem folder; the artifact is the recorded warm-up classification and a written bridge walkthrough in `patterns.md` |
| P1-P6 | The phase's solved problem folders (each with green harness) plus a `patterns.md` entry per pattern learned: skeleton in own words, its 4-question bridge, when to use it |
| P7 | The complete `patterns.md` playbook plus the timed-mock results |

`patterns.md` is the Weekly Review artifact-audit target: a pattern wrapped without
its playbook entry counts as an audit gap.
