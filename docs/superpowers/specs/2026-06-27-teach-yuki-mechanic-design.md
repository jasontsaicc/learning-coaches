# Teach Yuki Mechanic — Design Spec

Date: 2026-06-27
Skill: sd-coach
Status: approved, ready for implementation plan

## Problem

The skill's Feynman parts are mostly coach-led: the student explains (Recall), then 小球 asks one Transfer question. That tests recall, not the ability to teach a confused beginner who pokes holes. The student can pass the gate while still unable to field an unscripted follow-up.

Concrete trigger: the student knew the TTL definition but froze when a colleague asked "why short, when long?" Knowing a definition is not the same as having the underlying trade-off model. The real test is fielding a question you never rehearsed.

Yuki (junior dev character) already exists for exactly this, but she is barely wired in. She appears in two thin spots and is locked to Phase 2+:
- Step C Step 3: "Phase 2+: Occasionally have Yuki ask a question the student must answer. AI decides when."
- RPG Core Rule 3: "Yuki Phase 2+ only."

## Goal

Turn Yuki into a real antifragility trainer: the student teaches her, she fires unanticipated follow-ups aimed at the student's knowledge boundary. Works for learning a new concept, reviewing an old one, or walking a whole design problem. The blind spots she exposes feed the existing weakness-tracking system so they get retested and actually closed.

## The Loop

Two sub-actions:

1. **Teach-back (monologue test).** The student explains the concept or design coherently to Yuki, no notes. This catches the "I can use it but can't articulate it" gap. It surfaces axes the student uses by instinct but never names out loud (the gap that costs points in interviews).

2. **Yuki's follow-ups (the antifragile core).** Yuki asks unscripted questions aimed at the student's knowledge boundary: naive-but-deep, what-if, when-not-to, comparison traps, and deliberately-wrong naive suggestions the student must catch. Always pressing, regardless of phase.

## Placement

Independent mode plus woven into existing steps (not a replacement of either).

### 1. Independent `Teach Yuki` mode

- Student invokes anytime: "教 Yuki [topic]", "Teach Yuki", "我想教 Yuki short URL".
- Three uses: a freshly-learned concept, review of an old concept, or a whole design problem ("teach Yuki how to design a URL shortener").
- Added to the Quick Start router. Not phase-locked.
- Flow: teach-back first (student explains), then Yuki's follow-up volley, then blind-spot capture (see below).

### 2. Woven into the daily flow (upgrade existing steps)

- **Step C · Feynman Gate.** After a chunk passes Transfer, 小球 may hand the chunk to Yuki for 1-2 follow-ups. Not every chunk (that would exhaust the student) — the AI picks high-value chunks, and especially presses when the student passed too easily (the existing fast-track signal).
- **Step E · Simon Drill, "AI Challenge" phase.** The existing probing-follow-up phase becomes Yuki's turn: same intent, in-character, with the antifragile framing and the safety valve.

## Difficulty and Safety Valve

- No phase lock. Yuki always presses at the student's knowledge boundary. Phase affects only where that boundary naturally sits (a Phase 0 student's edge is simpler), not how hard Yuki tries.
- Safety valve (reuses the existing Failure Escalation principle): on 2 consecutive stalls or "太難了", Yuki narrows the question to a smaller step, lets the student stand back up, then re-pressures. Pressure stays continuous but never crushes. This is "在弱點加壓 + 過載就退" — add load, do not snap the spine.

## Yuki Question-Style Guide

Written into the skill so the AI generates good hard questions rather than random ones. These map to the existing Feynman Transfer categories, delivered in-character and aimed at the boundary:

- Naive-but-deep (exposes a hidden assumption): "為什麼不能直接…?"
- What-if / edge case: "如果 X 突然爆掉會怎樣?"
- When-boundary: "那什麼時候就不該用這個了?"
- Comparison trap: "這跟 Y 我分不出來欸?"
- Deliberately-wrong naive suggestion (borrows Max's anti-pattern move): "我覺得 TTL 設超長就好了啊?" — the student must catch it and correct it.

## Blind-Spot Capture (compounding)

- Every point Yuki stumps the student on is written to `progress.md` Mistake Registry as ❌ Unresolved, with a short tag.
- The Step A review queue and Weekly Review retest these. Today's blind spot becomes a tested-and-closed gap a few sessions later. Antifragility compounds instead of evaporating at the end of the session.

## Decisions Locked

- Teach-back monologue: kept. It is the tool that catches the articulation gap.
- Lightweight achievement: included. The RPG layer already exists, so a small "survived Yuki's interrogation" style unlock reinforces the mechanic at near-zero cost.

## Files Affected

- `SKILL.md`
  - New section: "Teach Yuki Mode" (independent mode + question-style guide + safety valve + blind-spot capture).
  - Step C Step 3 (Feynman Gate): replace the thin "Phase 2+ occasionally" line with the Yuki handoff, unlocked for all phases.
  - Step E (Simon Drill): reframe the AI Challenge phase as Yuki's turn.
  - Quick Start routing: add the invoke trigger.
  - RPG Quick Reference table + Core Rules: remove the "Phase 2+ only" lock, expand Yuki's role.
  - Reference table: add a pointer if a new reference file is created.
- `references/story.md`: expand Yuki's character — curious, persistent antifragile sparring partner.
- `references/achievements.md`: add one lightweight achievement.
- `evals/evals.json`: add 1-2 evals — the independent mode triggers on "教 Yuki …", and Yuki presses at the boundary with the safety valve on repeated stalls.

## Out of Scope (YAGNI)

- No separate question-bank reference file. The style guide lives inline in the Teach Yuki Mode section unless it grows past a screen.
- No new progress.md structure. Mistake Registry already exists and is reused as-is.
- No change to phase gates, scorecard, or curriculum content.

## Success Criteria

- The student can invoke "教 Yuki <topic>" in any phase and get a teach-back prompt followed by boundary-pressing follow-ups.
- On 2 consecutive stalls, Yuki demonstrably narrows the question instead of repeating the same hard one.
- Blind spots land in the Mistake Registry and resurface in a later Step A / Weekly Review.
- Existing teaching flow (A→H), gates, and RPG mechanics still work unchanged.
