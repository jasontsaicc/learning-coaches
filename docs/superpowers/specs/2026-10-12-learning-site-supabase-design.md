# 學習網站：Supabase Free 作答同步設計

日期：2026-10-12。狀態：待使用者審閱，尚未實作或建立雲端資源。

## 目的與已確認限制

使用者同意使用 Supabase，指定免費方案。沿用個人學習網站，讓同一帳號在手機與電腦
看見相同作答證據，不因換裝置而遺失首次結果。第一版聚焦登入、作答同步、既有紀錄匯入。
閱讀位置與卡片同步列為後續工作；本輪不重做題庫、課綱或教練評量。

目前 `site/build.py` 產生靜態網站；`exercises.js` 將每題每個 revision 的首次／最新
作答存入 `learning-map.practice.v1`；`app.js` 的 onSave 同時保存草稿與練習位置。
目前並沒有完整作答歷史，因此無法從舊資料復原中間每次重做。

## 選擇與成本

- 採用 Supabase 託管 Free：PostgreSQL、Auth、Data API；沿用靜態頁面，不新增自架 API。
- SQLite＋自架 API 同樣可行，但需要自行管理登入與服務，不符合本輪選定方向。
- 只做 JSON 匯出／匯入最簡單，但無法達成自動跨裝置同步。
- 教材、題庫繼續放 Git 的 Markdown／JSON，不上傳 Supabase Storage。
- 不使用付費附加功能、Realtime、Edge Functions 或人為保活排程。

2026-10-12 核對官方方案：Free 為每月 $0，500 MB 資料庫、5 GB egress、
50,000 MAU，最多 2 個 active projects；一週低活動可能暫停，不含自動備份。
以單人文字作答為主，判斷足以起步；不是無限容量或可用性保證。
保留可下載 JSON 紀錄，README 說明定期匯出與 Dashboard 恢復操作。

## 帳號與資料權限

建議使用 Email／密碼登入。專案擁有者在 Supabase Dashboard 預先建立並確認自己的
帳號，停用公開註冊；網站只提供登入、登出及同步狀態，不提供自助註冊。
忘記密碼時依管理者操作文件處理，不假設免費內建 SMTP 能可靠支援任意收件者。
這是本設計提出的登入選擇，仍可在審閱時調整。

使用官方 supabase-js v2 處理 session、更新 token 及 Data API，固定實際版本，
在實作計畫中定下現有靜態建置可用的載入方式，不手寫 refresh-token 流程。
SDK 載入失敗只停用雲端功能，不能讓現有課程與練習無法開啟。
設定只需要 Project URL 和 publishable key；secret、service-role、密碼不得進入 Git、
dist 或對話。所有雲端請求走 Supabase HTTPS endpoint。

網站目前在 tailnet HTTP 位址；啟用真實帳號前需驗證 tailnet HTTPS 存取，
例如 Tailscale Serve。更換 origin 會使舊 localStorage 不可直接讀取，需先在舊位址
匯出，再於新位址匯入。未處理 origin 搬移前不切換正式入口。

唯一業務表為 `practice_attempts`：

| 欄位 | 用途 |
| --- | --- |
| user_id | Auth 使用者，外鍵；RLS 的所有權依據 |
| event_id | 客戶端產生並持久保存的 UUID；與 user_id 組成主鍵 |
| chapter_id、question_id、revision | 穩定題目識別；revision 必須正整數 |
| answer | JSONB，沿用各題型答案結構 |
| correct、hint_used、skipped、confidence | 沿用現有自我練習證據 |
| occurred_at | 本機提交時間，支援離線作答排序 |
| received_at | 伺服器產生的接收時間，用於稽核 |

開啟 RLS，authenticated 只能 SELECT／INSERT 自己的紀錄；anon 無權限，
不授予 UPDATE／DELETE。CHECK 限制 revision、confidence、識別字串與資料大小。
同 event_id 重送採 ignore-duplicate，不改寫舊資料。讀入的 payload 仍需前端驗證。
前端判分維持自我練習用途，不宣稱這是可信的正式考試或教練評級。

## 保存、同步與跨裝置行為

1. 每次正式提交／略過只新增一筆事件；輸入草稿、提示切換不送出雲端寫入。
2. 登入後的本機資料按 user_id 隔離。一個具版本的 localStorage envelope 保存
   事件、待送事件與章節草稿，一次 setItem 完成一次本機更新，避免只存結果卻漏掉待送事件。
3. 先確認本機保存成功，再送出；成功回應才清除待送標記。失敗保留資料，顯示
   「已存此裝置／等待同步」，提供重試；本機失敗則明示「尚未保存」，不顯示已同步。
4. 登入、回到頁面、網路恢復、提交完成及手動重試時同步；請求不可重疊無限堆積。
   本輪不做背景定時輪詢，兩台都開著時以回到頁面或手動刷新取得另一台紀錄。
5. 按固定順序分頁下載完整事件，不受 Data API 預設每次筆數限制而遺漏；驗證成功
   才合併本機 pending。任何分頁失敗不清空現有證據。個人規模先不用增量游標。
6. 依 chapter／question／revision 整理首次與最新事件，以 occurred_at、event_id
   確定排序。多裝置資料合併後，較早的真實作答可能成為全帳號首次；任何原事件均不變。
   同一題重做不能覆寫首次。裝置時鐘需正常，時間嚴重失準時仍保留全部原始事件供查核。
7. 舊 revision 紀錄保留，不當成新題已通過；網站不回寫 progress.md 或教練 Mastery。
8. 草稿、輪次索引與 queue 仍按裝置保存；同步的是作答證據，不承諾在另一台接續同一
   個尚未提交的輸入框。下載資料不應重繪並中斷使用者正在填寫的答案。
9. 登出停止同步、清除畫面上的帳號資料並回到訪客模式；未送事件保留於原帳號的
   本機區域，提示尚未同步。舊請求回應須檢查 session 世代，不得寫入新帳號狀態。

## 舊資料與手動備份

未登入仍沿用原有訪客模式。首次登入不自動把訪客資料歸到某個帳號；顯示章節／
紀錄數量摘要，使用者在產品介面選擇匯入。這是資料歸屬操作，不是開發授權流程。

匯入前保留原始 v1 字串，且提供 JSON 下載；舊 key 不刪除、不覆寫。
將現存 firstAttempt／latestAttempt 轉為事件，兩者相同只產生一筆；以固定欄位順序
序列化題目識別與作答內容，導出穩定 UUID，重複匯入不新增同一份證據。
明示旧格式僅保存首次與最新，不能補造中間作答。草稿仍留在原裝置。

JSON 匯出包含 schema version、時間、事件與本機待送紀錄，不包含登入 token 或密碼。
匯入先做大小／格式／版本驗證，顯示摘要，確認後合併至目前帳號，不能清空遠端紀錄。
取消、壞檔案或本機保存失敗皆保留原資料。跨瀏覽器相同事件可安全重複匯入。

## 影響範圍

- `site/exercises.js`：提交事件掛點與沿用既有驗證／first/latest 顯示。
- `site/app.js`、`index.html`、`styles.css`：登入、同步狀態、匯入／匯出與帳號切換。
- 新增小型 `site/sync.js`：本機事件保存、Supabase 連線及事件合併；不建立通用資料層。
- `site/build.py`：明列新靜態資產及公開設定；未設定時保持原網站可用。
- SQL migration 與權限測試、對應 Node 測試、`browser-check.mjs`、README 設定文件。
- 不修改 `workspaces/`、歷史資料或題庫答案。開工前既有未追蹤的 drill-recall.py 保留。

## 驗收與部署前提

- 兩個瀏覽器同帳號：A 作答後 B 同步可見；兩邊離線作答再上線，事件都保留。
- 模擬伺服器已收資料但回應遺失、重試、重新載入，不新增重複事件。
- 首次／最新、revision、首次匯入、重複匯入、損壞檔案、localStorage quota 均有測試。
- 登出後的延遲回應、token 到期、不同帳號切換不串資料。
- 真實 PostgreSQL／Supabase 測試匿名與 A／B 帳號隔離，拒絕偽造 user_id 及修改事件；
  不能只用 mock 或掃描 SQL 字串就宣稱 RLS 通過。
- 雲端暫停、SDK／網路失敗時，本機練習仍可用且狀態不誤導。
- 全 repo lint、靜態 build、既有及新增瀏覽器驗證通過。
- 首次正式啟用前需 Free 專案、公開連線設定、已確認的個人帳號與 HTTPS 入口；
  目前尚未取得專案設定，也無可呼叫的 Supabase connector。不因此先加入付費服務。

## 官方依據

- [Pricing](https://supabase.com/pricing)
- [Free project pausing](https://supabase.com/docs/guides/platform/free-project-pausing)
- [SMTP restrictions](https://supabase.com/docs/guides/auth/auth-smtp)
- [Password-based Auth](https://supabase.com/docs/guides/auth/passwords)
- [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [API keys](https://supabase.com/docs/guides/getting-started/api-keys)
