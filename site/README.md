# site/ — learning map

Static site: course cards → per-course learning path (zigzag lessons per phase) → learning-map modal, key points, flashcards, notes/HTML. Read-only view of the repo; teaching stays in the coaches.

```
python3 site/build.py            # → site/dist/ (gitignored)
python3 site/build.py --check    # parse only; lint-all.sh runs this + test_build.py
cd site/dist && python3 -m http.server 8123 --bind 100.86.161.122   # tailnet only
```

## Files

| File | Role |
|---|---|
| `build.py` | stdlib-only parsers → `dist/data.json` + copies note files to `dist/files/` |
| `index.html` | whole front end (hash routes `#/`, `#/c/<coach>`); d3/marked/DOMPurify from cdnjs with SRI |
| `test_build.py` | assert cases for every parser; add a case when you touch a parser |
| `img/<coach>.svg` | course hero art (isometric, hand-generated; one per coach id) |

## Data sources (allowlist — nothing else reaches dist)

| Shown as | Source |
|---|---|
| phases | `workspaces/<c>/progress.md` `## Phase status`; names/focus from `skills/<c>-coach/references/curriculum.md` (ca: `cloud-architect-coach`) |
| learned topics + level | `## Mastery` lines, parsed by `parse_mastery_line` |
| planned (dashed) lessons | sd: `curriculum-detail.md` `### Day a-b: Title`; k8s: not-started phase focus split on `、`; leetcode: curriculum table rows |
| leetcode problems | folders `workspaces/leetcode/<group>/<slug>/` + `## 做過` for labels |
| key points / flashcards | `KEYPOINTS` in `build.py` (one-liner tables, k8s term-registry, sd pattern-map) |
| notes / HTML | `portfolio/<c>/notes/`, `workspaces/<c>/notes/`, leetcode problem folders, `portfolio/leetcode/notes/` |

Never shown: session logs, breakpoint text, story-bank, career files.

## Note → topic attachment (by filename)

| Filename | Attaches to |
|---|---|
| `p2a-*.md/html` | phase P2a |
| `s40-*` | every topic whose Mastery line ends `(s40)` |
| `day10-*` | sd topic/planned lesson whose `(Day a-b)` covers 10 |
| `portfolio/leetcode/notes/<problem-slug>.html` | that problem (folder slug or title slug) |
| anything else | course-level "全部筆記 / HTML" only |

HTML buttons show the page `<title>`. To bring in a claude.ai artifact: `Artifact read` with `path: "index.html"` saves the file, then copy it here under a name from this table. Skip work artifacts and English drills.

## Traps

- A progress/curriculum format change breaks the build (by design). Fix the parser + add a `test_build.py` case; don't loosen to silent skips.
- Don't write `workspaces/` from dev work (repo CLAUDE.md). Imported notes go to `portfolio/`.
- `python -m http.server` sends no Cache-Control: after a rebuild, open with `?v=N` or hard refresh.
- Verify UI with a screenshot (`/browse`), not just data. If headless Chromium dies with "No usable sandbox", the AppArmor profile `/etc/apparmor.d/playwright-chromium` (userns) is missing or not loaded.
- Flashcard state is per-browser `localStorage`; it never writes back to progress.md (source of truth).
- The tailnet server is a foreground process; it stops with the session.
