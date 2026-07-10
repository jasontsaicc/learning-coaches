# Smaller-Models Playbook

Written 2026-07-10, the last Fable 5 session. From now on this environment runs on smaller models (Opus, Sonnet, Haiku). This doc transfers the judgment a stronger model applied silently into rules you and the model apply explicitly. Canonical copy lives in this repo so both machines get it. Re-read after any model change.

## The one mental shift

A stronger model supplies judgment; a smaller model supplies execution. After the switch, judgment must come from written institutions (engine, CLAUDE.md guardrails, this doc), from the task framing you write, and from your own review. Budget attention accordingly: you review more, the model freelances less.

## Model selection

| Task | Model | Why |
|---|---|---|
| Coach sessions (k8s / sd / leetcode / english) | Opus | Gates need judgment: adversarial probing, Examiner scoring, depth-ceiling calls |
| Plan mode, architecture, debugging unknown causes | Opus | Hypothesis quality matters more than speed |
| Execution against a written plan, routine infra edits | Sonnet | Good enough when the plan carries the judgment |
| Bulk mechanical work (rename, reformat, scaffold) | Sonnet or Haiku | No judgment needed |

Switch with `/model`. The default in settings.json is per machine; set it on the bastion too.

## What you now do that Fable did silently

- Size the task. One session, one task. Smaller models degrade hardest on long mixed sessions; start a fresh session instead of pushing a tired context.
- Name the skill. Smaller models under-trigger skills. Type "k8s-coach" or "sd-coach" instead of describing the topic and hoping it triggers.
- Demand evidence. "Done" without pasted command output is not done. Ask: show the verification output.
- Review diffs yourself before commit. Trust was calibrated to Fable; reset it and let each model re-earn it.
- Judge the plan, not the prose. Smaller models write confident prose around wrong plans. Read the steps, ignore the tone.
- Plan mode earlier. Anything 3+ steps: force plan mode yourself instead of waiting for the model to suggest it.

## Coach-session drift checklist

The engine locks these invariants, but a weaker model drifts toward breaking them. Signs, and what to say:

| Drift sign | Say this |
|---|---|
| Coach or peer agrees quickly, praise feels cheap | 跑 adversarial default: 先戳最弱點, 活下來才給 pass |
| Session ends with empty Mistake Registry and coach accepts it | 空 registry 可疑, 重新 probe |
| Step F (Teach-to-Learn) or G (Interview Q&A) skipped to save time | F/G 是 locked steps, 補跑 |
| You stop but no breakpoint gets written | 先寫 breakpoint 到 progress.md 再回話 |
| Coach scores its own Phase Gate | Phase Gate 要 dispatch Examiner subagent, 不能自己改考卷 |
| Session starts without `git pull` | 先 pull 再讀 progress.md |

Two or more signs in one session: end the session and restart fresh. Restarting is cheaper than arguing with a drifted context.

## Maintenance cadence

| When | What |
|---|---|
| Weekly | `./scripts/lint-all.sh` in this repo; skim progress.md files for breakpoints that never resumed |
| After correcting the model | Say 寫進 memory (feedback type); confirm a file landed in `~/.claude/projects/-home-ubuntu/memory/` |
| Monthly | Prune memory: delete stale or wrong entries; keep MEMORY.md under ~20 lines |
| Quarterly, or after a model change | `/revise-claude-md` on the global CLAUDE.md; re-read this playbook and delete rules that stopped earning their keep |

## Machine sync

This playbook and the coaches sync through this repo. The global `~/.claude/CLAUDE.md` and the memory directory do not sync; after editing CLAUDE.md on one machine, copy the change to the other by hand. Diff them during the quarterly review.
