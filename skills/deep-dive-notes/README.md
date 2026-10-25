# deep-dive-notes

A Claude Code skill that turns one technical topic into a layered HTML study note, aimed at big-tech DevOps/SRE depth. Output is in Traditional Chinese, with technical terms kept in English.

| Layer | Content |
|---|---|
| 0 | One analogy and one diagram |
| 1 | First principles: the unavoidable problem and its hard limits |
| 2 | Mechanism, with real defaults and numbers |
| 3 | Trade-offs: why this design won over the alternatives |
| 4 | How AWS does it: services, quotas, cost, one trap per service |
| 5 | Scaling: the evolution ladder from small team to big tech |
| 6 | Failure and on-call: symptoms, first command, SLOs |
| 7 | Interview: one question, L4 vs L6 answer |

Every layer ships a real diagram (SVG or ASCII).

## Install

Lives in learning-coaches. `scripts/link-skills.sh` links it into `~/.claude/skills/`.

## Use

```
/deep-dive-notes DNS        # layers 0-2 first, then 3-5, then 6-7
/deep-dive-notes DNS all    # all seven layers at once
```

## Notes

- Written for my own setup. It routes some topics to my other coach skills (k8s-coach, sd-coach, leetcode-coach, terraform-coach, cloud-architect-coach). Without them, routing may behave differently.
- Visual style lives in `references/notebook-style.md`.
- `evals/evals.json` holds behavioral evals for the skill-creator eval runner.
