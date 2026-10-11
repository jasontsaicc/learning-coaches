# 章節題庫與筆記維護

互動練習是人工維護的 JSON，不會從筆記自動產生。每門課一個檔案，最外層陣列可放多個章節；前端共用同一套呈現與批改邏輯。

| 課程 | 題庫檔案 | 目前練習章節 |
|---|---|---|
| Kubernetes | [exercises/k8s.json](exercises/k8s.json) | apply→Running、容器的隔離、Pod 探針、Deployment rollout、Resource/QoS/OOM、Service、Ingress、DNS 排障 |
| System Design | [exercises/sd.json](exercises/sd.json) | Cache-Aside |
| LeetCode | [exercises/leetcode.json](exercises/leetcode.json) | Linked List Cycle |
| Cloud Architect | [exercises/ca.json](exercises/ca.json) | VPC Peering |

課綱節點、筆記和練習題庫是三件事：有 Chat System 節點與筆記，不代表已經編寫它的練習題。`build.py` 負責把三者連起來；不要修改產生的 `dist/data.json`，重建時會覆蓋。

## 新增一章

1. 在對應課程 JSON 陣列中複製一個完整章節物件。更新全站唯一的 `id`、`title`、`coachId`、`phaseId`。
2. `topicRefs` 填入網站資料中完全一致的 `parent` 與 `label`。例如 Chat System 是 `sd:P3` 與 `Chat System (Day 35-37)`。可執行 `python3 site/build.py` 後查閱 `site/dist/data.json` 的 `nodes`。
3. 填寫至少兩個 `objectives`；`sources` 指向已匯入網站的教材檔案。開發新增教材放 `portfolio/<課程>/notes/`，不要修改 `workspaces/`。
4. 編寫六道主題題目，至少三種互動，涵蓋至少兩個目標；再替每道主題各寫一道變式（`variantOf`）。每輪固定取前六道非變式題；弱項重練只取每道主題的第一個變式，同一題疊多個變式不會被用到。變式要改條件（數字、故障點、情境），不能只換名稱或選項順序。
5. 每題的 `hint` 指向下一個推理動作（追哪個狀態、比哪個條件、查哪段設定），不透露答案；同章不要重複同一句。
6. 填寫 `challenge.prompt` 與 `challenge.criteria`，讓學習者能用實作或解釋展示理解：寫明環境與指令、執行前要寫下的預測，以及可觀察的檢查標準。
7. 執行下方驗證，人工核對答案、干擾選項、提示與來源，再更新網站。

## 題目欄位

所有題目都需要 `id`、`revision`、`type`、`objectiveId`、`prompt`、`hint`、`explanation`、`source.path` 與 `source.section`。來源段落需人工確認，建置只驗證檔案可匯出。

| `type` | 額外欄位與答案格式 |
|---|---|
| `choice` | `multiple`、`options`（每項有 id/text/feedback），`answer` 為正確選項 ID 陣列 |
| `fill` | `answer.kind` 為 text 或 number；請複製現有同型題的接受答案、單位及容差設定 |
| `order` | `items` 與 `answer`；答案為「可接受的完整 ID 排列」陣列，可容許多種順序 |
| `match` | 請複製現有同型題的配對項目、目標及答案格式 |

以下是放進 Cache-Aside 章節 `questions` 的單選變式範例；實際新增前仍需校對內容與目標：

```json
{
  "id": "miss-responsibility-variant",
  "revision": 1,
  "type": "choice",
  "objectiveId": "o1",
  "variantOf": "owner",
  "prompt": "應用採用 cache-aside。Redis 裡沒有商品資料，下一步由誰向資料庫讀取？",
  "hint": "想想這個模式的資料載入邏輯寫在哪一層。",
  "explanation": "Cache-aside 由應用在未命中時查詢資料庫，再回填快取。",
  "source": {"path": "portfolio/sd/notes/day06-07-caching.md", "section": "Cache-Aside"},
  "multiple": false,
  "options": [
    {"id": "app", "text": "應用程式", "feedback": "正確：應用負責載入與回填。"},
    {"id": "redis", "text": "Redis 自動查詢", "feedback": "Redis 不會因為未命中就自動知道如何查詢業務資料庫。"}
  ],
  "answer": ["app"]
}
```

`variantOf` 必須指向同章、同學習目標的主題題目。不要更換既有章節／題目 ID；更改題意、答案或批改規則時提高 `revision`，避免舊作答被視為新版證據。新增題目使用新 ID。

## 筆記掛到錯誤節點時

預設會以檔名判斷：例如 `day35-*` 對應課綱 Day 35。但練習的第 40 次 session 不一定是課綱 Day 40。這時在 Markdown 加上獨立一行：

```html
<!-- topic: Distributed Rate Limiter (Day 31-32) -->
```

HTML 則在 head 加上 `<meta name="topic" content="Distributed Rate Limiter (Day 31-32)">`。標籤須與節點名稱完全一致，優先於檔名；找不到節點會讓建置失敗。

## 驗證與發布

```bash
python3 site/build.py --check
./scripts/lint-all.sh
./scripts/site-refresh.sh
```

在網站親自走過新章的答對、答錯、提示與變式重試流程。瀏覽器若保留舊畫面請強制重新整理。確認後再 commit / push；Git 推送與目前這台主機的網站重建是不同動作。

## 下一步維護方式建議

先保留 JSON + Git 審查：現在題庫小，適合校對與追蹤答案修訂。章節增加時再改成「每章一個 JSON」，例如 `exercises/sd/chat-system.json`，讓修改互不干擾；這需要同步修改載入器，目前尚不支援巢狀目錄。之後若手寫欄位經常出錯，再加新增章節範本指令或表單編輯器。題目品質仍由人工審核。
