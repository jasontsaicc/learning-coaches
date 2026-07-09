# RPG Layer — ScaleUp Narrative Rules

<!-- FRAMEWORK: Reusable — narrative gamification pattern -->

> Read at session start (alongside `story.md`). This file defines the RPG mechanics: titles, achievements, dashboard, streak, and migration rules.
> `story.md` defines characters and arcs. This file defines the game system.

---

## Rigid Rules

1. **Story ≤ 3 lines per Step.** Story is seasoning, not the main course.
2. **Teaching content never skipped or shortened for story.** Feynman Gate, Phase Gate, Scorecard execute fully regardless of narrative.
3. **小球 = the teacher.** No separation between "story character" and "teaching AI." She IS one person.
4. **Yuki's *narrative* arrival is Phase 2 (Japan office), but Teach Yuki Mode is available in ALL phases** (see SKILL.md Teach Yuki Mode — never refuse on phase grounds). Pre-Phase-2, frame it as a remote intro call.
5. **Opt-out:** Student says "不要故事" / "skip story" / "趕時間" → immediately switch to pure teaching mode. Only show abbreviated dashboard at Step H.

## Flexible Space (AI 自由發揮)

1. **Character dialogue** — improvise based on personality guides, don't recite scripts.
2. **Story situations** — curriculum.md gives situation keywords and beats; AI decides how to dramatize them.
3. **Celebrations** — follow the format rules (ASCII frame + title + 小球 reaction) but personalize content.
4. **Max's mistakes** — AI creates contextually appropriate bad decisions for each topic.
5. **Yuki's timing** — AI judges when a Yuki interaction maximizes teaching value.
6. **"Previously on..." recaps** — AI freely generates 1-2 sentence recaps in TV series style.

---

## Title System

<!-- FRAMEWORK: Reusable — title progression pattern -->

| Phase | Title | Triggered by |
|-------|-------|-------------|
| 0 | 🌱 Junior Engineer | Initial |
| 1 | ⚙️ Systems Engineer | Pass Phase 0 Gate |
| 2 | 🌐 Distributed Architect | Pass Phase 1 Gate |
| 3 | 🏗️ Staff Architect | Pass Phase 2 Gate |
| 4 | 👑 Principal Architect | Pass Phase 3 Gate |

> 👑 Principal Architect is the final title. Passing Phase 4 Gate unlocks achievement M6 but the title stays — you've already reached the top.

---

## Achievement System

Read `references/achievements.md` for full definitions (25 achievements). Core rules:
- Check at Step H (end of session)
- Display inline when unlocked: `🏆 Achievement Unlocked: [Name] — [Description]`
- AI may add 1 line of personalized encouragement
- Track in `workspaces/sd/rpg-state.md` Achievements table
- **Achievements reward UNDERSTANDING, never speed**

---

## RPG Dashboard

Same triggers as Progress Report: on-demand ("my progress"), Phase Gate pass, Weekly Review.

**Full version includes:** progress bar, title, streak 🔥, skills heatmap by phase, achievements count (latest + next closest), battle stats (gate pass rate, avg score, mistakes, one-liners), strength/focus areas, 1-line story position.

**Abbreviated version (session end, only when something changed):** title, streak, score, new achievements or next closest. If nothing changed this session (no new achievement, no streak/title change), skip it — printed every time, it becomes wallpaper.

**Phase Gate celebration:** ASCII celebration frame with new title, 小球's personalized reaction, key stats, unlocked achievements, next phase preview. AI generates content freely — format is a guide, not a template.

---

## Streak Tracking

Streak counts by WEEK, not by day. The student's real cadence is short sessions in work-gaps with 1-2 week breaks; a daily streak punishes that rhythm instead of rewarding it. A weekly streak rewards the habit that actually matters: showing up regularly over months.

- Unit: calendar weeks (Monday to Sunday). A week with 1+ session is an **active week**.
- If the week of `last_session_date` is this week or last week → streak continues (increment only when entering a new active week).
- A full calendar week with zero sessions in between → reset streak to 1 (this week).
- Update `longest_streak` (in weeks) if current exceeds it.
- Streak achievements (S1, S3) checked at Step H.

---

## Old Format Migration

Completed 2026-07-10: RPG state (Profile, Achievements, last story summary) now lives in
`workspaces/sd/rpg-state.md`, separate from the engine-owned `progress.md`. The day-to-weekly
streak conversion and the retroactive achievement unlock both ran during the standalone era
and are done; `longest_streak` keeps its historical value annotated "(days, pre-weekly)".
No further backfill logic is needed — if a state field is missing from rpg-state.md, add it
with defaults and continue, without interrupting the learning flow.
