---
name: sd-coach
description: <!-- TODO: one-line trigger description. Name the domain and the concrete contexts where this coach should activate. Be specific and a little pushy so it fires when the user needs it, not only when they name it. -->
---

# Sd Coach

At session start, read the shared engine (run `cat ${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` or follow [shared engine](../../engine/ENGINE.md)), then read the hook files listed below. The engine owns all session mechanics; these hooks supply only domain content. The progress-file schema is engine-owned (`engine/PROGRESS-SCHEMA.md`); do not redefine it here.

## Hook Map

| Hook | File |
|------|------|
| north-star | `${CLAUDE_SKILL_DIR}/references/north-star.md` |
| curriculum | `${CLAUDE_SKILL_DIR}/references/curriculum.md` |
| teaching-elements | `${CLAUDE_SKILL_DIR}/references/teaching-elements.md` |
| scorecard-dims | `${CLAUDE_SKILL_DIR}/references/scorecard-dims.md` |
| phase-gates | `${CLAUDE_SKILL_DIR}/references/phase-gates.md` |
| language | `${CLAUDE_SKILL_DIR}/references/language.md` |
| narrative | `${CLAUDE_SKILL_DIR}/references/narrative.md` |
| portfolio | `${CLAUDE_SKILL_DIR}/references/portfolio.md` |
