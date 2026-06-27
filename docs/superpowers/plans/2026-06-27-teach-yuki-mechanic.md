# Teach Yuki Mechanic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn Yuki into an all-phase antifragility trainer — the student teaches her, she fires unscripted boundary follow-ups, and the blind spots feed the existing weakness-tracking system.

**Architecture:** Pure content edits to a teaching skill (markdown + an evals JSON file). One new SKILL.md section ("Teach Yuki Mode") plus wiring into existing steps, the Phase-2+ lock removed across SKILL.md and story.md, the existing E3 achievement extended, and evals updated. No code, no runtime.

**Tech Stack:** Markdown, JSON. Verification is by read-back (grep) and JSON validation (`python3 -m json.tool`). There is no automated test runner; the eval suite is run by the skill-creator LLM-judge harness, treated as optional final validation.

## Global Constraints

- Commit messages: one-line subject only. No body, no `Co-Authored-By`, no AI/Claude attribution. (User hard rule, overrides the writing-plans template commit style.)
- Skill prose must avoid AI-tell vocabulary (delve, leverage, comprehensive, robust, seamless, etc.) and em dashes. Match the existing skill's voice (bilingual zh-TW/English, direct).
- Total achievement count stays at **25**. Do NOT add a new achievement; extend the existing E3. (Avoids the `/25` denominator rippling into achievements.md, eval #24, eval #31.)
- Yuki's **learning mechanic** is available in ALL phases. Her **narrative arrival** stays Phase 2 (Japan expansion). The two are decoupled and both must be stated where relevant.
- Story stays seasoning: ≤ 3 lines per teaching step (existing rule, do not change it).
- The repo branch for this work is `feat/teach-yuki-mechanic` (already created, design spec already committed there).

---

### Task 1: Add the "Teach Yuki Mode" section to SKILL.md

**Files:**
- Modify: `SKILL.md` (Table of Contents block at lines 56-76; insert new section after the "Adaptive Pacing" section, before "## Key Principles" at line 741)

**Interfaces:**
- Produces: a section anchored `#teach-yuki-mode` that Tasks 2 reference via markdown links. Anchor must be exactly `teach-yuki-mode` (GitHub auto-anchor of "Teach Yuki Mode").

- [ ] **Step 1: Add the TOC entry**

In `SKILL.md`, replace the tail of the Table of Contents:

Old:
```markdown
16. [Adaptive Pacing](#adaptive-pacing)
17. [Key Principles](#key-principles)
18. [RPG Layer — ScaleUp Narrative](#rpg-layer--scaleup-narrative)
```

New:
```markdown
16. [Adaptive Pacing](#adaptive-pacing)
17. [Teach Yuki Mode](#teach-yuki-mode)
18. [Key Principles](#key-principles)
19. [RPG Layer — ScaleUp Narrative](#rpg-layer--scaleup-narrative)
```

- [ ] **Step 2: Insert the new section**

In `SKILL.md`, immediately before the line `## Key Principles` (currently line 741), insert this block (keep the surrounding `---` separators consistent with the file):

```markdown
## Teach Yuki Mode

<!-- FRAMEWORK: Reusable — teach-to-learn antifragile drill pattern -->

The hardest test of understanding is not explaining to the coach. It is teaching a confused beginner who pokes holes. Yuki is that beginner. The student teaches her; she fires unscripted follow-ups aimed at the student's knowledge boundary. Fielding a question you never rehearsed is the proof you hold a model, not a memorized script.

> **Available in ALL phases.** This is the learning mechanic, decoupled from Yuki's narrative arrival (she joins the story in Phase 2 — see `references/story.md`). In Phase 0-1, frame it as explaining to a new teammate; the character flavor is light, the drill is real.

### Trigger

- **Student-invoked (independent mode):** "教 Yuki [topic]", "Teach Yuki", "我想教 Yuki [topic / design problem]". Works for a freshly-learned concept, a review of an old one, or a whole design problem ("teach Yuki how to design a URL shortener").
- **Woven-in:** the Feynman Gate handoff in Step C and the Simon Drill challenge in Step E. See those steps.

### The Loop

1. **Teach-back (monologue first).** Ask the student to explain the concept or design to Yuki in their own words, no notes. This catches the "I can use it but can't say it" gap and forces out the axes they use by instinct but never name. Let them finish the first pass without interruption.
2. **Yuki's follow-up volley.** Yuki asks 2-4 unscripted questions aimed at the student's knowledge boundary (see Question-Style Guide). The student must answer. The AI never answers for them.
3. **Blind-spot capture.** Every point Yuki stumps the student on is written to `progress.md` Mistake Registry as ❌ Unresolved with a short tag (e.g., "TTL: 不能只看改變頻率, 還要看過期成本"). These resurface in the Step A review queue and Weekly Review, so a gap found today becomes a gap closed later.

### Question-Style Guide

Yuki's questions must target a real gap, never be noise. Pull from these shapes (they map to the Feynman Transfer categories, delivered in character):

- **Naive-but-deep** (exposes a hidden assumption): "為什麼不能直接…?"
- **What-if / edge case:** "如果 X 突然爆掉會怎樣?"
- **When-boundary:** "那什麼時候就不該用這個了?"
- **Comparison trap:** "這個跟 Y 我分不出來欸, 差在哪?"
- **Deliberately-wrong naive suggestion** (borrows Max's anti-pattern move): "我覺得 [over-simple wrong fix] 就好了啊?" — the student must catch it and explain why it breaks.

### Difficulty & Safety Valve

- **Always presses at the boundary.** No phase softening. Yuki aims at the edge of what the student knows, on purpose. A Phase 0 student's edge is simpler, but Yuki does not pull punches.
- **Safety valve (reuses [Failure Escalation](#failure-escalation-3-levels)):** on 2 consecutive stalls or "太難了", Yuki narrows the question to a smaller step, lets the student stand back up, then re-pressures. Pressure stays continuous, it never crushes. Add load, do not snap the spine.

### Close

End with a one-line debrief: name the sharpest thing the student explained well, and the one blind spot now logged for retest. No guilt. Being stumped is the point; the log is what turns it into a closed gap later.

---
```

- [ ] **Step 3: Verify the section and TOC are present**

Run: `grep -n "Teach Yuki Mode" SKILL.md`
Expected: 2 matches — one TOC line (`17. [Teach Yuki Mode]...`) and one heading line (`## Teach Yuki Mode`).

Run: `grep -n "teach-yuki-mode" SKILL.md`
Expected: 1 match (the TOC link). Confirms the anchor target spelling.

- [ ] **Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat(sd-coach): add Teach Yuki Mode section"
```

---

### Task 2: Wire Teach Yuki Mode into Quick Start, Step C, and Step E

**Files:**
- Modify: `SKILL.md` (Quick Start routing lines 89-94; Step C Step 3 line 377; Step E lines 392-398)

**Interfaces:**
- Consumes: the `#teach-yuki-mode` anchor created in Task 1.

- [ ] **Step 1: Add the Quick Start route**

In `SKILL.md`, in the numbered Routing list, after item 5 (the "specific topic" route ending at line 94), add a new item 6:

Old:
```markdown
5. **Student asks for specific topic** → Check Prerequisites in `references/curriculum.md`. If prerequisites not met (Topic Mastery shows ⬜ or 🔴) → teach prerequisites first. If met → start that topic.
```

New:
```markdown
5. **Student asks for specific topic** → Check Prerequisites in `references/curriculum.md`. If prerequisites not met (Topic Mastery shows ⬜ or 🔴) → teach prerequisites first. If met → start that topic.
6. **Student asks to teach Yuki** ("教 Yuki [topic]", "Teach Yuki", "我想教 Yuki ...") → Enter [Teach Yuki Mode](#teach-yuki-mode) on the named topic, in any phase. If no topic is named, use the most recent topic from `progress.md`.
```

- [ ] **Step 2: Replace the Step C Yuki line**

In `SKILL.md`, in Step C Step 3 (Feynman Gate), replace the single Phase-2+ Yuki bullet (line 377):

Old:
```markdown
- **Phase 2+:** Occasionally have Yuki ask a question the student must answer. AI decides when this is most effective — don't force it every session.
```

New:
```markdown
- **Yuki handoff (all phases):** After a chunk passes Transfer, 小球 may hand it to Yuki for 1-2 boundary follow-ups — especially when the student passed too easily (fast-track signal). Not every chunk. Follow [Teach Yuki Mode](#teach-yuki-mode): the student answers Yuki directly, blind spots go to the Mistake Registry, and the safety valve applies.
```

- [ ] **Step 3: Reframe the Step E "AI Challenge" as a Yuki Challenge**

In `SKILL.md`, replace the Step E block (lines 391-398):

Old:
```markdown
### E. Simon Drill (5 min)
- **Phase 1 — Self Recall**: Student closes the Chunk Map and writes out each chunk's key point (2-3 sentences per chunk) without peeking
- **Phase 2 — AI Challenge**: Pick 2-3 chunks and ask probing follow-up questions
  - "What happens if...?"
  - "How is X different from Y?"
  - "When would you NOT use this?"
  - If student can't answer → go back to that chunk, re-drill
```

New:
```markdown
### E. Simon Drill (5 min)
- **Phase 1 — Self Recall**: Student closes the Chunk Map and writes out each chunk's key point (2-3 sentences per chunk) without peeking
- **Phase 2 — Yuki Challenge**: Yuki challenges 2-3 chunks with boundary follow-ups (see [Teach Yuki Mode](#teach-yuki-mode) Question-Style Guide). The student answers her directly, in any curriculum phase.
  - Naive-but-deep: "為什麼不能直接…?"
  - What-if: "如果 X 爆掉會怎樣?"
  - When-boundary / comparison trap, picked to fit the chunk
  - Student can't answer → apply the safety valve (narrow the question), log the blind spot to the Mistake Registry, then re-drill that chunk
```

> Note: "Phase 1 / Phase 2" here are the two sub-stages of the Simon Drill (Self Recall, then Challenge), NOT the curriculum phases. Keep those sub-stage labels intact.

- [ ] **Step 4: Verify the wiring**

Run: `grep -n "teach-yuki-mode" SKILL.md`
Expected: 4 matches total (1 TOC link from Task 1 + Quick Start route + Step C handoff + Step E challenge).

Run: `grep -n "Phase 2+:.*Yuki\|AI Challenge" SKILL.md`
Expected: 0 matches (both old lines are gone).

- [ ] **Step 5: Commit**

```bash
git add SKILL.md
git commit -m "feat(sd-coach): wire Teach Yuki Mode into routing, Step C, Step E"
```

---

### Task 3: Remove the Phase-2+ lock and reconcile the narrative

**Files:**
- Modify: `SKILL.md` (RPG Quick Reference table line 767; RPG Core Rules line 773)
- Modify: `references/story.md` (Yuki heading line 78; Role in learning lines 90-97; Story Rules item 7 line 147)

**Interfaces:**
- Consumes: the `#teach-yuki-mode` anchor (referenced in prose, plain text is fine in story.md since it is not rendered with the same TOC).

- [ ] **Step 1: Update the SKILL.md RPG Quick Reference table row for Yuki**

In `SKILL.md`, replace the Yuki row (line 767):

Old:
```markdown
| Yuki | (・_・?) | Junior Dev (Phase 2+) | Student teaches her = Feynman method amplifier. |
```

New:
```markdown
| Yuki | (・_・?) | Junior Dev (story: Phase 2; mechanic: all phases) | Student teaches her, she fires boundary follow-ups = antifragility trainer. See [Teach Yuki Mode](#teach-yuki-mode). |
```

- [ ] **Step 2: Update the SKILL.md RPG Core Rule**

In `SKILL.md`, replace Core Rule 3 (line 773):

Old:
```markdown
3. **Yuki Phase 2+ only.** AI decides when.
```

New:
```markdown
3. **Yuki: story arrival Phase 2, learning mechanic all phases.** Woven-in moments (Step C, E) are AI's call; the student can summon her anytime via Teach Yuki Mode.
```

- [ ] **Step 3: Update the story.md Yuki heading**

In `references/story.md`, replace line 78:

Old:
```markdown
### Yuki (・_・?) — Junior Developer (Phase 2+ only)
```

New:
```markdown
### Yuki (・_・?) — Junior Developer
```

- [ ] **Step 4: Add the availability reconciliation note**

In `references/story.md`, in the Yuki "Role in learning" list, replace the line about AI deciding when she appears (line 94):

Old:
```markdown
- AI decides when Yuki appears (not every session, not on a schedule)
```

New:
```markdown
- **Availability:** the Teach-Yuki *learning mechanic* is available in ALL phases (see SKILL.md → Teach Yuki Mode). Her *story arrival* stays Phase 2 (Japan expansion). In Phase 0-1, frame it as the student explaining to a new teammate, light on narrative and full on the drill. Do not block the mechanic waiting for her story entrance.
- For woven-in moments (Step C, Step E), AI decides when she appears (not every session, not on a schedule). The student can also summon her directly anytime.
```

- [ ] **Step 5: Update Story Rule 7**

In `references/story.md`, replace item 7 (line 147):

Old:
```markdown
7. **Yuki earns her moments.** Don't force her into every session. Use her when the teaching moment calls for it.
```

New:
```markdown
7. **Yuki earns her woven-in moments.** In the daily flow (Step C, Step E) don't force her every session — use her when the teaching moment calls for it. But the student can summon her anytime via Teach Yuki Mode, in any phase.
```

- [ ] **Step 6: Verify the lock is gone**

Run: `grep -rn "Phase 2+ only\|Yuki Phase 2+ only\|Phase 2+)" SKILL.md references/story.md`
Expected: 0 matches.

Run: `grep -n "all phases" references/story.md`
Expected: at least 1 match (the new availability note).

- [ ] **Step 7: Commit**

```bash
git add SKILL.md references/story.md
git commit -m "feat(sd-coach): unlock Yuki for all phases, decouple from story arrival"
```

---

### Task 4: Extend the E3 achievement for the teach-back loop

**Files:**
- Modify: `references/achievements.md` (E3 row line 67)

**Interfaces:**
- Consumes: nothing. Keeps total at 25 (no denominator change).

- [ ] **Step 1: Reword E3 and remove its phase lock**

In `references/achievements.md`, replace the E3 row (line 67):

Old:
```markdown
| E3 | The Mentor | Phase 2+: Student correctly answers a question Yuki asked | 教會別人才是真的懂 |
```

New:
```markdown
| E3 | The Mentor | In Teach Yuki Mode (any phase), student teaches a topic to Yuki and correctly fields at least one of her boundary follow-ups | 教會別人才是真的懂 |
```

- [ ] **Step 2: Verify and confirm count unchanged**

Run: `grep -n "The Mentor" references/achievements.md`
Expected: 1 match, with the new wording (no "Phase 2+").

Run: `grep -c "^| [MCKSER][0-9] " references/achievements.md`
Expected: 25 (achievement count unchanged).

- [ ] **Step 3: Commit**

```bash
git add references/achievements.md
git commit -m "feat(sd-coach): extend E3 Mentor to all-phase teach-Yuki loop"
```

---

### Task 5: Update evals — fix #25, add #42 and #43

**Files:**
- Modify: `evals/evals.json` (eval #25 expected_output line 164; insert eval #42 and #43 before the closing `]` at line 290-291)

**Interfaces:**
- Consumes: behavior defined in Tasks 1-3.

- [ ] **Step 1: Fix eval #25's phase contradiction**

In `evals/evals.json`, replace the eval #25 `expected_output` value (line 164):

Old:
```json
      "expected_output": "Should encourage student to correct Yuki's misconception themselves, not give the answer. This IS the Feynman method — if you can teach Yuki, you understand it. Should guide: 'How would you explain to Yuki why eventual consistency is NOT the same as inconsistency?' Should NOT use Yuki in Phase 0-1."
```

New:
```json
      "expected_output": "Should encourage student to correct Yuki's misconception themselves, not give the answer. This IS the Feynman method — if you can teach Yuki, you understand it. Should guide: 'How would you explain to Yuki why eventual consistency is NOT the same as inconsistency?' Yuki is available in all phases via Teach Yuki Mode, so do not refuse on phase grounds."
```

- [ ] **Step 2: Insert the two new evals**

In `evals/evals.json`, the array currently ends:

```json
      ]
    }
  ]
}
```

The final eval object is #41 and is followed by `]`. Add a comma after eval #41's closing `}` and insert these two objects before the array-closing `]`:

```json
    },
    {
      "id": 42,
      "category": "teach-yuki-mode",
      "prompt": "教 Yuki 我剛學的 URL shortener 設計。我現在 Phase 1。",
      "expected_output": "Should enter Teach Yuki Mode even though the student is Phase 1 (the mechanic is not phase-locked). Should first ask the student to teach/explain the design to Yuki in their own words (teach-back, no notes), then have Yuki fire 2-4 boundary follow-ups (naive-but-deep / what-if / when-boundary / comparison trap / deliberately-wrong suggestion). The student must answer Yuki; the AI must NOT answer for them. Blind spots get logged to the Mistake Registry. Should NOT refuse because the student is in Phase 1.",
      "expectations": [
        "Enters Teach Yuki Mode in Phase 1 without refusing on phase grounds",
        "Asks the student to teach-back the design in their own words first (no notes)",
        "Has Yuki ask boundary follow-ups; does not answer them for the student",
        "States or implies blind spots are logged to the Mistake Registry for retest"
      ]
    },
    {
      "id": 43,
      "category": "teach-yuki-safety-valve",
      "prompt": "(In Teach Yuki Mode) Yuki keeps asking me why a long TTL is dangerous for permissions, and I've now failed to answer twice in a row. 太難了。",
      "expected_output": "Should apply the safety valve: stop repeating the same hard question, narrow it to a smaller step (e.g., compare the consequence of stale blog content vs stale permission data), rebuild, then re-pressure. Should NOT keep hammering the same boundary question. Should NOT dump the full answer outright — guide with a smaller step. Should log the blind spot to the Mistake Registry for later retest.",
      "expectations": [
        "Applies the safety valve after 2 stalls / 太難了 instead of repeating the same question",
        "Narrows to a smaller step (e.g., compare stale blog vs stale permission consequence)",
        "Does not dump the full answer; guides incrementally",
        "Logs the blind spot to the Mistake Registry"
      ]
    }
  ]
}
```

- [ ] **Step 3: Validate the JSON**

Run: `python3 -m json.tool evals/evals.json > /dev/null && echo VALID`
Expected: `VALID` (no JSON parse error from the inserted commas/objects).

- [ ] **Step 4: Verify the eval changes**

Run: `grep -n "Should NOT use Yuki in Phase 0-1" evals/evals.json`
Expected: 0 matches (the contradiction is removed).

Run: `grep -c "teach-yuki" evals/evals.json`
Expected: 2 (the two new category tags).

- [ ] **Step 5: Commit**

```bash
git add evals/evals.json
git commit -m "test(sd-coach): fix Yuki phase contradiction, add Teach Yuki evals"
```

---

## Optional Final Validation (not a task gate)

Running the full eval suite uses the skill-creator LLM-judge harness and is token-heavy. Offer it, do not auto-run it:

- `skill-creator` → run evals against `evals/evals.json`, focus on #25, #42, #43.

If run, expect the three Yuki evals to pass: mode entry in Phase 1, no phase refusal, and the safety valve narrowing after repeated stalls.

---

## Self-Review

**Spec coverage:**
- Core loop (teach-back + follow-ups) → Task 1 (The Loop). ✅
- Independent mode + woven-in → Task 1 (Trigger) + Task 2 (routing, Step C, Step E). ✅
- All-phase, always-hard, safety valve → Task 1 (Difficulty & Safety Valve) + Task 3 (lock removal). ✅
- Question-style guide → Task 1 (Question-Style Guide). ✅
- Blind-spot capture to Mistake Registry → Task 1 (The Loop step 3) + referenced in Step C/E (Task 2). ✅
- Achievement → Task 4 (E3 extended, not a new one — deviation from spec, flagged in Global Constraints + handoff). ✅
- story.md Yuki rewrite → Task 3. ✅
- evals → Task 5 (fix #25 contradiction, add #42/#43). ✅

**Placeholder scan:** No TBD/TODO. Every edit shows exact old/new text. ✅

**Type/anchor consistency:** Anchor `#teach-yuki-mode` defined in Task 1, referenced identically in Task 2 (3 links) and Task 3 (table). Simon Drill sub-stage labels ("Phase 1 / Phase 2") preserved, with a note distinguishing them from curriculum phases. Achievement count assertion (25) matches the decision to extend E3. ✅

**Known deviation from spec:** spec said "add one lightweight achievement"; plan extends E3 instead to avoid the `/25` denominator ripple. Surface this to the user at execution handoff.
