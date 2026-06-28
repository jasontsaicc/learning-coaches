---
name: engine-probe
description: Temporary probe. Use when the user types "probe engine read" to verify the plugin can read the shared engine file.
---

# Engine Probe

When activated, do BOTH of these and report which succeeded:

1. Read `${CLAUDE_PLUGIN_ROOT}/engine/ENGINE.md` and report whether it contains `ENGINE_READ_OK`.
2. Read `../../engine/ENGINE.md` (relative to this skill file) and report whether it contains `ENGINE_READ_OK`.

Report: "plugin-root read: PASS/FAIL, skill-relative read: PASS/FAIL".
