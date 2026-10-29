# site/ — learning map

Static personal learning site: course paths → chapter exercises → evidence and retry variants, with search, Markdown reading, learning maps and optional memory cards. Read-only view of learner files; teaching and formal assessment stay in the coaches.

```
python3 site/build.py            # → site/dist/ (gitignored)
python3 site/build.py --check    # parse only; lint-all.sh runs this + test_build.py
systemctl --user status learning-map   # serves site/dist on 100.86.161.122:8123 (tailnet only)
./scripts/site-refresh.sh               # rebuild + restart + health check + Cloudflare deploy (needs ~/.cloudflare-token)
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
| SD current topic | phase and Day derived from `## Current Session breakpoint`; only the derived status is exported |
| planned (dashed) lessons | sd: `curriculum-detail.md` `### Day a-b: Title`; k8s: focus of phases with no Mastery topic yet, split on `、`, plus `curriculum-plan.md` §12.2 column `新插入 / 換題材` split on `;` (non-P rows become extra modules); leetcode: curriculum table rows |
| leetcode problems (practiced, not automatically high) | folders `workspaces/leetcode/<group>/<slug>/` + `## 做過` for labels |
| key points / flashcards | `KEYPOINTS` in `build.py` (one-liner tables, k8s term-registry, sd pattern-map) |
| notes / HTML | `portfolio/<c>/notes/`, `workspaces/<c>/notes/`, leetcode problem folders, `portfolio/leetcode/notes/` |

Never shown: session logs, breakpoint text, story-bank, career files.

## Note → topic attachment (by filename)

| Filename | Attaches to |
|---|---|
| `p2a-*.md/html` | phase P2a |
| `s40-*` | every topic whose Mastery line ends `(s40)` |
| any HTML with `<meta name="topic" content="<exact Mastery label>">` | that one topic (wins over the prefix; unknown label fails the build) |
| any Markdown with `<!-- topic: <exact topic label> -->` on its own line | explicit topic attachment, before filename rules; unknown label fails the build |
| `day10-*` | sd topic/planned lesson whose `(Day a-b)` covers 10 |
| `portfolio/leetcode/notes/<problem-slug>.html` | that problem (folder slug or title slug) |
| anything else | course-level "全部筆記 / HTML" only |

Per-topic page set (`-layers` / `-hub` / `-mock-l6` suffixes on one prefix): see `skills/deep-dive-notes/SKILL.md` 主題頁面組.

HTML buttons show the page `<title>`. To bring in a claude.ai artifact: `Artifact read` with `path: "index.html"` saves the file, then copy it here under a name from this table. Skip work artifacts and English drills.

## Traps

- A progress/curriculum format change breaks the build (by design). Fix the parser + add a `test_build.py` case; don't loosen to silent skips.
- Don't write `workspaces/` from dev work (repo CLAUDE.md). Imported notes go to `portfolio/`.
- Builds add content versions to the entry JS and CSS URLs so refreshed pages load changed assets. Already-open tabs still need a reload.
- Verify UI with a screenshot (`/browse`), not just data. If headless Chromium dies with "No usable sandbox", the AppArmor profile `/etc/apparmor.d/playwright-chromium` (userns) is missing or not loaded.
- Flashcard state is per-browser `localStorage`; it never writes back to progress.md (source of truth).
- Server: user unit `~/.config/systemd/user/learning-map.service` (linger on, survives reboot). Never needs a restart after a rebuild.
- Cloudflare Pages project `learning-map`: Access apps (email OTP, one address) cover `learn.jasondevops.space` and `learning-map-eep.pages.dev` + `*.` previews. Any new hostname needs its own Access app before DNS. Deploys are manual (`site-refresh.sh`), not on commit.
- Rebuild is automatic on commit via local `.git/hooks/post-commit` (not tracked; recreate on a new clone). Uncommitted note drops need a manual `python3 site/build.py`.


## Chapter exercises

繁中新增與維護步驟：[AUTHORING.md](AUTHORING.md)。

SD activity and assessment are separate: the current breakpoint chapter shows
「進行中 · 尚未評量」 without inventing a grade. Unassessed planned chapters with notes
show 「已有教材 · 尚未評量」; other planned chapters show 「課綱待學」.
Notes alone do not prove completion.
SD scorecard entries with an explicit `Day N Topic Title` also establish prior practice:
ungraded chapters show 「已練習 · 尚無章節評級」. Only the status is exported, not scorecard text;
a partial retest does not establish completion or a mastery grade.
Current-topic detection expects a breakpoint line
starting with `P3 / Chat System(Day 35)/ ...`; changing that format requires updating the parser.

Coverage: k8s has 8 chapters (P0 apply→Running; P1 container isolation, probes, rollout,
QoS/OOM; P2a Service, Ingress, DNS triage), each six primary questions plus one variant per
primary. SD Cache-Aside, LeetCode Linked List Cycle and CA VPC Peering also have six primaries
plus one variant per primary, question-specific hints and concrete practice challenges.
There are 11 chapters and 132 questions in total. Other chapters explicitly show that
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

The home page keeps unfinished practice visible alongside recent reading. Loaded Markdown
notes offer chapter exercises whose declared `sources` include that note; returning to an
unfinished exercise preserves its draft. Completed rounds include expandable per-question
reviews with first/latest answers, reference answers, explanations and source links. Only
current-revision evidence is shown; attempted variants appear alongside primary questions.
Viewing a review does not change stored answers or formal coach assessments.

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
failed requests, stale responses, storage quota errors and CDN fallbacks. It also checks
simultaneous reading/practice resume, note-to-practice links, per-question reviews,
first/latest separation, revision isolation and safe rendering of saved answer text.


## HTML-first notes

Course pages place HTML notes inside the learning path: phase notes precede that
phase’s topics as compact links. Topic titles open their first HTML note directly;
additional HTML and small `md` links sit alongside a topic/practice action. Only notes
without a phase/topic attachment appear in “其他補充筆記”. Existing filename/topic
metadata determines attachment; no title-based guessing is used. Topic, phase and
map lists use compact links, with Markdown in smaller text and no disclosure panels. Search includes
HTML and topics by default; check “包含 Markdown 補充資料” to search older notes.
This is a presentation preference, not proof of content parity: original Markdown
exports, reading URLs and exercise source links remain available until their content
and citations have been explicitly migrated. Development does not modify workspaces.

## SD / k8s expandable curriculum

`learning-paths.json` is the explicit phase → node → chunk navigation catalog for
SD and k8s. Order is intentional (SD follows the October 29 queue, rather than Day
numbers). Node disclosure buttons and HTML links are separate. Missing HTML is
shown as text; shared and partial notes are labelled. Additional legacy notes,
exercises, maps and cards remain available; their IDs and storage are unchanged.

`build.py` validates unique IDs and all catalog destinations against the existing
export allowlist (including fragments). `pathCurrent` exports only a derived node
ID from the current breakpoint; it never exports the breakpoint or infers mastery
from reading. Ambiguous/missing positions remain unknown. Changing a source
breakpoint format requires updating `path_position` and its test.

Catalog titles are searchable; `#/c/<coach>/<node-id>` opens and locates a node.
Expansion is retained in memory while navigating in the app. HTML still opens in
a separate tab. This catalog replaces text-splitting as the displayed curriculum
for these two coaches; the older topic graph remains for exercises and the map.
