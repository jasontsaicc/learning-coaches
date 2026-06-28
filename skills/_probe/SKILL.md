---
name: engine-probe
description: Temporary probe. Use when the user types "probe engine read" to verify the plugin can read the shared engine file.
---

# Engine Probe

When activated, do BOTH of these and report which succeeded:

1. Run `cat ${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` and report whether it contains `ENGINE_READ_OK`.
2. Read the markdown link [engine](../../engine/ENGINE.md) and report whether it contains `ENGINE_READ_OK`.

Report: "skill-dir bash read: PASS/FAIL, markdown-link read: PASS/FAIL".
