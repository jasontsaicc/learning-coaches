# Pre-migration archive(2026-07-10)

Standalone 時期(`system-design-notes` repo,tag `pre-migration` = 292223f)的原始狀態檔,
verbatim 保存,不再更新。轉換後的活檔在 `workspaces/sd/`。

## 檔案

| 檔案 | 說明 | 轉換去向 |
|------|------|---------|
| `progress.md` | 原進度檔(單一大檔,S40 止) | 拆為 progress.md(engine schema)/ one-liner-library.md / rpg-state.md / session-log.md |
| `CLAUDE.md` | 原 notes repo 的專案偏好(語言規則/結構/PoC 偏好) | 語言規則 → sd-coach language hook;結構 → portfolio hook;PoC 偏好 → teaching-elements step D |
| `curriculum-roadmap.md` | pre-skill 時期的 roadmap + daily tracker | superseded(課綱主檔 = skills/sd-coach/references/curriculum-detail.md) |
| `planning-review.md` | 2026-02 課綱審查紀錄 | superseded(結論已折進課綱 v4/v5) |

仍然活著、只是搬家的:`docs/coaching-brief.md` → `workspaces/sd/coaching-brief.md`、
`docs/pattern-map.md` → `workspaces/sd/pattern-map.md`(皆 git mv,內容未動)。

## 轉換對帳(原檔 → 轉換檔,2026-07-10 核對)

| 項目 | 原檔 | 轉換後 | 說明 |
|------|------|--------|------|
| session_count | 40 | 40 | |
| last_weekly_review | 33 | 33 | S41 = WR5 到期 |
| Mistake Registry | 91 列(66 ✅ / 14 ❌ / 11 🟡) | 25 筆 live(14 ❌ + 11 🟡→unresolved)+ 66 筆 resolved 留存本檔 | 🟡 Improving/Partial 併入 unresolved,原狀態照錄於註記 |
| Scorecard history | 17 列 | 17 筆 | 分數照原數字;唯 s36 原記 ~4/7 → 正規化 3/7(✅=1),原符號留註記 |
| One-Liner Library | 21 條 | 21 條(one-liner-library.md) | verbatim |
| Review Schedule | 14 張主題卡(Leitner Box 1-4) | 14 筆 queue 條目 | Box1→3、Box2→3、Box3→7、Box4→14;到期日 verbatim(過期照舊) |
| Achievements | 16/25 | 16/25(rpg-state.md) | verbatim |
| Curiosity Branches | 3 | 3 | |
| Topic Mastery | 39 列(22 已學 + 17 ⬜ 未開) | 22 筆(⬜ 不列,課表見 curriculum hook) | 🟢→high、🟡→med |
| Phase Gates | P0 retroactive / P1 3/3(2026-05-29)/ P2 5/6(2026-06-18) | 同,標 legacy pre-Examiner | Examiner ledger 從空白開始 |

已知的格式性損失(皆已註記在對應轉換檔):
- Leitner「Box 1 = 隔天」檔位 engine 沒有,映為 interval 3(到期日未動)。
- standalone scorecard/registry 以 session 編號為鍵,多數未記日期;轉換檔已知日期照填,其餘標(未記日期),不回填猜測。
- registry 的 interval / next-review-date / unresolved-session-count 為遷移初始化(近似),來源邏輯見 progress.md 註記。
