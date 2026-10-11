# 2026-10-11 SD 章節筆記工作紀錄

用 `deep-dive-notes` skill 產出 SD 五個 phase 的章節 HTML 筆記，結構照 k8s 章節筆記
（章節地圖 → L0–L7 → 我的錯題軌跡 → topic 筆記）。來源：`workspaces/sd/progress.md`
（Mastery、Mistake Registry、Scorecard）、`skills/sd-coach/references/`（curriculum-detail、
first-principles-chains、8-block-skeleton）、`workspaces/sd/pattern-map.md`。

## 完成

| 章節 | 檔案（`portfolio/sd/notes/`） | claude.ai artifact |
|---|---|---|
| P0 思考框架 | `p0-chapter-thinking-framework.html` | `BKXgR76y4eekRRnJ8bZ5oJ` |
| P1 核心元件 | `p1-chapter-building-blocks.html` | `RKosdV37PuwuAqKxBJ7YWA` |
| P2 分散式核心 | `p2-chapter-distributed-core.html` | `KBjAa1Fp3S4agTY8kHRNSK` |
| P3 經典設計題 | `p3-chapter-classic-problems.html` | `RgYUqLGsAhSfzPxu6jKS3g` |
| P4 進階與模擬面試（預習頁） | `p4-chapter-advanced-mocks.html` | `6H7Ym4tgGajGF1y2BzBkZz` |

- 視覺刻意和 k8s 不同：藍圖風（深藍底 + 青色格線，淺色模式為晒圖紙）、標題欄、每層一張帶標籤的 sheet、
  線條語意（實線 = 資料路徑、虛線 = 看不見的、琥珀 = 重點、紅 = 故障）、錯題用 REDLINE / REV。
  字體：Barlow Condensed + Noto Sans TC + JetBrains Mono。
- 檔名 `p<N>-chapter-*` 依 `note_target()` 掛到對應 phase。topic 連結用站內相對路徑
  （`day*.html` 同目錄、Markdown 走 `../../../../#/read/...`），在 claude.ai artifact 裡不能點。
- P3 的 chat「送出 → 投遞」時序圖收在 `<details>` 裡：S52 step F（教 Yuki）還沒跑，避免先看答案。
- P4 未開課：L1–L6 以 brownfield migration 為主軸；REDLINE 列面試輸出習慣債，作為 Day 66-67 的清單。
- 錯題軌跡取自 Mistake Registry 改寫，不貼 session log 原文；story-bank、career 內容不進筆記。

## 踩到的雷：中文亂碼

直接把 scratchpad 檔案 `cp` 進 repo，網站上中文變亂碼。原因：site server 回 `Content-type: text/html`
不帶 charset，檔案本身也沒有 `<meta charset>`，瀏覽器退回 Windows-1252。claude.ai 發佈時會自動包一層
帶 charset 的 head，所以 artifact 正常；k8s 筆記是經 `Artifact read` 取回，已含這層 head。
修法：五份 repo 檔開頭補上與 k8s 相同的 `<!doctype html><html><head><meta charset="utf-8">...`。
artifact 原始檔（scratchpad）不加，避免發佈時被重複包裝。

## 驗證

- `./scripts/lint-all.sh` ALL PASS；`python3 site/build.py` 成功。
- `site/dist/data.json`：五份各自掛在 `sd:P0` 到 `sd:P4`。
- 筆記內所有站內連結都對到已匯出的檔案（0 missing）；網站回 HTTP 200，`<title>` 正確且帶 charset。
- P1 用 Playwright 截圖：桌機 dark、手機 390px light，皆無橫向捲動。腳本掃出 8 個 SVG 標籤超出 viewBox，已修。
- 已查證的事實：SQS 訊息上限 1 MiB（2025-08）、API Gateway WebSocket 2 h / 10 min / 128 KB / 500 新連線/s、
  WAF rate-based 窗口 1/2/5/10 分鐘且最低 10、DynamoDB MRSC GA（2025-06，建表時決定）、
  Pinpoint end of support 2026-10-30、Evidently 停止支援（2025-10）、Aurora failover 通常 &lt; 60 s 常 &lt; 30 s、
  ElastiCache `reserved-memory-percent` 25%。
  事故：Kinesis 2020-11-25、GitHub 2018-10-21、Facebook 2010-09-23、Knight Capital 2012（SEC 2013-222）。

## 已知限制

- 依記憶撰寫、未逐一對文件：ElastiCache `maxmemory-policy` 預設 `volatile-lru`、CloudFront default TTL 86,400 s、
  API Gateway 帳號 throttle 10,000 RPS / burst 5,000、跨 AZ $0.01/GB、Cognito / Step Functions 的細節、
  Knight Capital 損失金額（寫「超過 4.6 億美元」）。
- 只截了 P1；其他四份只跑了 SVG 文字溢出腳本，未目視。
- 每份是獨立 HTML（約 41–51 KB），CSS 重複；改版要逐份重產。scratchpad 的 `_head.html` + `p*.body.html`
  組裝流程不會保留到下個 session。
- artifact 與 repo 檔是兩份：repo 多了 charset head，內容其他部分相同。

## 下一步

1. 使用者在學習地圖看過實際畫面，回饋藍圖風、深度、長度。
2. `site/README.md` Traps 補一條：從 scratchpad 匯入的 HTML 要自帶 `<meta charset="utf-8">`（或讓 server 回 charset）。
3. Chat 的 F / G 跑完後，P3 的 Chat 列和 `<details>` 圖可以更新；News Feed、Payment 學完後補 P3 對應段落。
