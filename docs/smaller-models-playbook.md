# Model Playbook

Rewritten 2026-07-29: this environment runs Fable-class models again (Claude Fable 5).
The 2026-07-10 version assumed a downgrade to smaller models; that premise inverted, so
the weak-model rules (one-session-one-task, restart-on-drift, the Opus/Sonnet/Haiku
routing table) are deleted. If the environment downgrades again, restore them from this
file's git history. Re-read after any model change and delete rules that stop earning
their keep.

## Standing rules (any model)

- Demand evidence. "Done" without pasted command output is not done. Ask: show the
  verification output.
- Review diffs yourself before commit. Trust is calibrated per model; let each model
  re-earn it.
- Judge the plan, not the prose. Confident prose around a wrong plan reads the same as
  around a right one.
- Bulk mechanical work (rename, reformat, scaffold) can still drop to a smaller model
  with `/model`; judgment-heavy work stays on the default.

## Coach-session audit checklist

The engine locks these invariants (ENGINE.md, Adversarial Default). Sycophancy drift
and grade inflation are model-independent failure modes; spot-check regardless of
model. Signs, and what to say:

| Drift sign | Say this |
|---|---|
| Coach or peer agrees quickly, praise feels cheap | 跑 adversarial default: 先戳最弱點, 活下來才給 pass |
| Session ends with empty Mistake Registry and coach accepts it | 空 registry 可疑, 重新 probe |
| Step F (Teach-to-Learn) or G (Interview Q&A) skipped to save time | F/G 是 locked steps, 補跑 |
| You stop but no breakpoint gets written | 先寫 breakpoint 到 progress.md 再回話 |
| Coach scores its own Phase Gate | Phase Gate 要 dispatch Examiner subagent, 不能自己改考卷 |
| Session starts without `git pull` | 先 pull 再讀 progress.md |

## Maintenance cadence

| When | What |
|---|---|
| Weekly | `./scripts/lint-all.sh` in this repo; skim progress.md files for breakpoints that never resumed |
| After correcting the model | Say 寫進 memory (feedback type); confirm a file landed in `~/.claude/projects/-home-ubuntu/memory/` |
| Monthly | Prune memory: delete stale or wrong entries; keep MEMORY.md under ~20 lines |
| Quarterly, or after a model change | `/revise-claude-md` on the global CLAUDE.md; re-read this playbook and delete rules that stopped earning their keep |

## Machine sync

This playbook and the coaches sync through this repo. The global `~/.claude/CLAUDE.md`
and the memory directory do not sync; after editing CLAUDE.md on one machine, copy the
change to the other by hand. Diff them during the quarterly review.
