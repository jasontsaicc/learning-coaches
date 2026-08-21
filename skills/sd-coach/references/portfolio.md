# Portfolio

## Workspace Directory

Progress file, registries, and in-progress work live in:

```
${CLAUDE_SKILL_DIR}/../../workspaces/sd/
```

這個目錄是 git-tracked 學習狀態(跨機器同步:每堂課後 commit + push,開課前 pull,協定見 SKILL.md Session Sync)。內容:

- `progress.md`:engine 的進度檔。Schema engine-owned,定義在 `engine/PROGRESS-SCHEMA.md`,本 coach 不重定義。
- `one-liner-library.md`:domain registry(每主題一句面試開場白,headline first)。step H 的 One-Liner Challenge 餵進來:「面試官剛問 'What is [topic]?',一句話回答。」沿用 PROGRESS-SCHEMA section 7 的 registry 欄位進間隔抽考;抽考標準是講得出精準的一句,不是方向對就好。
- `rpg-state.md`:RPG 狀態(title、streak、achievements、last story summary)。規則見 `narrative.md`;非間隔複習型。
- `coaching-brief.md`:教法備忘(學員畫像、learning mode 覆寫、有效/無效的教法紀錄)。session 開始跟 progress.md 一起讀。
- `curriculum-plan.md`:戰略層規劃(advisory,見 `curriculum.md`)。
- `session-log.md`:**熱檔,只留最近幾場**。S44 以前封存在 `archive/session-log-S36-S44.md`。
- `archive/`:冷檔,開課時不讀;Weekly Review trend tracking、Phase Gate 三振診斷、或要查某場歷史時才讀。
  - `breakpoint-history.md`:2026-08-19 以前 progress.md 的 Current Session breakpoint 疊層原文(該區段當時已長成 S42-S50 日誌,違反 schema §3)。
  - `session-log-S36-S44.md`:早期 session 敘事。
  - `pre-migration/`:standalone 時期的原始狀態檔,verbatim 保存,不再更新。

**寫入紀律**:`progress.md` 的 Current Session breakpoint 是「當前狀態一行 + 下一場 resume」(PROGRESS-SCHEMA §3),敘事寫 `session-log.md`,不要在 breakpoint 疊舊場。

## Portfolio Directory

Artifacts that clear the quality bar ship to:

```
${CLAUDE_SKILL_DIR}/../../portfolio/sd/
```

Recruiter-facing 展示區,與 workspace 分開:

- `notes/`:每堂筆記 `dayXX-topic.md` + 手抄用 mind map `dayXX-topic-mindmap.md`(格式唯一來源:`references/notes-template.md`,含必填的 🔴 My Mistakes 與 🎤 How to Say It in Interview 段)。筆記 commit freely,連錯誤都有價值,不設門檻。
- `projects/`:Go PoC,每主題一個目錄(例 `caching-poc/`、`day23-rate-limiter/`)。含 Dockerfile/compose 與 README;編譯產物不進 git(.gitignore 擋)。

### Quality Bar

notes/ 不設門檻;projects/ 的 PoC 本身就是練習產出,也 commit freely,但 README 至少講清楚:這題驗證了什麼推導、怎麼跑、量到什麼數字。真正 recruiter-facing 的差異化是「每個 PoC 都在驗證一條第一性推導」,不是程式碼行數。

## Per-Phase Artifacts

| Phase | Artifact | 落點 |
|-------|----------|------|
| P0 | 4-step framework 筆記、估算 cheatsheet 練習 | notes/ |
| P1 | 每個 building block 的筆記 + mind map;build 型主題的 Go PoC(LB、caching、MQ…) | notes/ + projects/ |
| P2 | 錨定題設計文件(multi-region session store 類)+ 分散式主題 PoC(consistent hashing、rate limiter) | notes/ + projects/ |
| P3 | Tier 1/2 經典題的 8-block 設計圖 + deep-dive 筆記;代表作 PoC(URL shortener、unique ID generator) | notes/ + projects/ |
| P4 | mock 逐字稿與 debrief、brownfield migration 設計、trade-off 對照筆記 | notes/ |

Weekly Review 的 artifact audit(engine)對照這張表:該 phase 該有的東西不在,就是該補的債。

## Cross-Coach Evidence

本 coach 主要替 `competency/l6-matrix.md` 產生 architecture judgment、capacity 與
trade-off 證據。`portfolio/sd/` 保留 domain 筆記與 PoC；只有直接支援 shop platform
架構決策、且通過 `engine/GOVERNANCE.md` promotion gate 的 ADR／capacity model，才晉升
到 `portfolio/platform-eks/architecture/` 或 `cost/`。不複製整份筆記。
