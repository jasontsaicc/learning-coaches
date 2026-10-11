# site/ — learning map

Static personal learning site: course paths → chapter exercises → evidence and retry variants, with search, Markdown reading, learning maps and optional memory cards. Read-only view of learner files; teaching and formal assessment stay in the coaches.

```
python3 site/build.py            # → site/dist/ (gitignored)
python3 site/build.py --check    # parse only; lint-all.sh runs this + test_build.py
cd site/dist && python3 -m http.server 8123 --bind 100.86.161.122   # tailnet only
```

## Files

| File | Role |
|---|---|
| `build.py` | stdlib-only parsers → `dist/data.json` + copies note files to `dist/files/` |
| `index.html`, `styles.css` | semantic page shell and shared responsive design; existing CDN dependencies with SRI |
| `app.js` | routes, courses, search, reading and recent position |
| `exercises.js` | question grading, attempts, storage and chapter practice UI |
| `exercises/<coach>.json` | reviewed chapter questions and explanations |
| `review.js`, `map.js` | legacy Leitner cards and D3 map |
| `test_*.mjs`, `browser-check.mjs` | Node tests and optional Playwright integration checks |
| `test_build.py` | assert cases for every parser; add a case when you touch a parser |
| `img/<coach>.svg` | course hero art (isometric, hand-generated; one per coach id) |

## Data sources (allowlist — nothing else reaches dist)

| Shown as | Source |
|---|---|
| phases | `workspaces/<c>/progress.md` `## Phase status`; names/focus from `skills/<c>-coach/references/curriculum.md` (ca: `cloud-architect-coach`) |
| learned topics + level | `## Mastery` lines, parsed by `parse_mastery_line` |
| planned (dashed) lessons | sd: `curriculum-detail.md` `### Day a-b: Title`; k8s: not-started phase focus split on `、`; leetcode: curriculum table rows |
| leetcode problems (practiced, not automatically high) | folders `workspaces/leetcode/<group>/<slug>/` + `## 做過` for labels |
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


## Chapter exercises

Initial coverage: Pod probes, Cache-Aside, Linked List Cycle and VPC Peering.
Each has six primary questions plus two variants. Other chapters explicitly show that
exercises have not been written. Types are `choice` (single/multiple), `fill` (text/number),
`order` and `match` (pairing/classification). Adding another chapter of these types needs
only a bank entry and an exported source note, not a new page or renderer.

Use an existing bank as the exact schema example. Keep chapter/question IDs stable;
increment `revision` when question meaning or answers change. Every question names an
objective, source section, hint, explanation, and declared accepted answer. Choices and
matching items include misconception feedback. Variants point to a primary question in
the same chapter and objective. `topicRefs` match exact parent/label pairs in built data;
a changed or ambiguous reference fails the build instead of attaching to the wrong topic.

Validate with `python3 site/build.py --check`. The validator checks references, exported
source paths, IDs, answer membership, ordering completeness and numeric tolerances.
Question quality still needs human review: record assumptions, accept legitimate alternate
answers, and verify mechanisms against primary documentation. Do not copy private session
logs into banks. Static answers are visible to users; this is self-study, not a secure exam.

Routes: `#/`, `#/c/<coach>`, `#/search`, `#/practice/<chapter-id>`,
`#/read/<encodeURIComponent(file-path)>`. Reading routes allow only exported Markdown.
HTML diagrams keep opening separately. Unsupported relative Markdown links are inert;
external http(s) references remain clickable.

## Local state and evidence

- `srs`: existing card IDs and `{box,due}` schema preserved; UTC day boundaries unchanged.
- `learning-map.practice.v1`: chapter queue, draft, question revision, first/latest attempts.
- `learning-map.reading.v1`: recent exported note/topic and Markdown scroll position.

No account or cross-device sync. Clearing browser storage loses these local records.
Corrupt or unavailable storage displays an error; original corrupt values are not replaced.
First attempts remain immutable after retries; hinted answers and skips remain distinct.
Passing a newer variant can remove a weak item without rewriting the first attempt.
Practice never writes progress.md or marks formal mastery/gates passed.

## Verification

`./scripts/lint-all.sh` runs Python parser/bank checks and Node built-in tests (Node 22+).
Run `python3 site/build.py` to create `dist/`, then serve it with a static server.

The optional integration check uses an existing external Playwright installation:

```bash
SITE_URL=http://127.0.0.1:8124/ PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs node site/browser-check.mjs
```

Set `CHROMIUM_PATH` for a non-default Chromium executable. In a trusted isolated test
container without Chromium sandbox support only, `CHROMIUM_NO_SANDBOX=1` is available.
Screenshots go to `/tmp/learning-site-preview/`. The check covers 360px/desktop layouts,
all input types, keyboard sorting, draft and feedback resume, search, reading, map/cards,
failed requests, stale responses, storage quota errors and CDN fallbacks.
