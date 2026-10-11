# 2026-10-11 學習網站工作紀錄與下一步

## 今天完成

使用者確認網站以個人學習為主，參考 Wondering 的互動學習方向，並要求依章節練習，
透過選擇、填空、排序等方式檢查理解。第一版已實作、整合到本機 master，
更新既有 tailnet 網站；使用者回饋「改的還算滿意」，要求整理紀錄並 commit／push。

- 首頁改為 Learning Garden：接續閱讀／練習、課程入口與章節卡片。
- 課程頁提供可收合路徑、教練原始評量、題庫入口與尚無題庫提示。
- 新增主題／筆記搜尋、Markdown 阅读頁、目錄與閱讀位置；HTML 圖解維持另開頁。
- 前端拆成 app、exercises、review、map 與共用 CSS；沿用 Python 靜態建置。
- 題庫採 JSON，新增章節不必複製頁面；建置檢查來源、引用、答案與題型格式。
- 支援單選、多選、填空、排序、配對／分類，以及情境式題幹。
- 作答具提示、信心選擇、略過、逐題解說、目標摘要與弱項變式重練。
- 首次作答與後续重做分開；依 revision 保存證據，不回寫教練評量。
- 沿用現有 Leitner 卡片與 srs 紀錄；LeetCode「做過」不再自動等於 high。

## 已上線題庫

| 課程 | 章節 | 主題目 | 變式 |
|---|---|---:|---:|
| Kubernetes / EKS | Pod 探針 | 6 | 2 |
| System Design | Cache-Aside | 6 | 2 |
| LeetCode | Linked List Cycle | 6 | 2 |
| Cloud Architect | VPC Peering | 6 | 2 |

共 4 章、32 題。CA 新增 `portfolio/ca/notes/vpc-peering.md` 教材。
其餘章節未宣稱已有完整題庫；學員 workspace 與歷史資料均未修改。

## 驗證與修正

本日實作階段通過：

- `./scripts/lint-all.sh`：Python parser／題庫驗證、原有教練檢查及 12 項 Node 測試。
- `python3 site/build.py`：靜態網站建置。
- `site/browser-check.mjs`：桌面、360px 手機、不同題型、排序鍵盤操作、續答、搜尋、
  閱讀、地圖與舊卡片；另測 HTTP 失敗重試、過期回應、儲存額度與 CDN 備援。
- 正式 tailnet 網址的首頁、章節入口與資料量檢查。

審查發現並以回歸測試修正：變式成功未解除弱項、跳到主內容連結誤觸路由、
排序草稿修改到首次答案，以及提交後重新整理遺失解說畫面。
獨立 reviewer 提供上述問題後因使用額度限制中斷；剩餘確認由實作者完成，
不將其描述為已取得完整獨立審查結論。

畫面證據位於 `/tmp/learning-site-preview/`，屬本機暫存，可用 browser-check 重新產生，
不作永久追蹤的交付檔。

## 維運與提交

- 網站：`http://100.86.161.122:8123/`，僅 tailnet 存取。
- 服務：`learning-map.service`，沿用既有設定。
- 今天一起納入原先保留的 `site/README.md` 服務／post-commit 自動建置說明。
- 遠端：`origin`，分支：`master`；推送後以遠端追蹤分支和本機 HEAD 比對確認。

本次整理前已有的三筆本機提交：

| Commit | 內容 |
|---|---|
| `fd26d20` | 第一版設計 |
| `cb8b5f7` | 逐章多題型實作計畫 |
| `f50ea28` | 前端改版、題庫與測試 |

相關文件：[設計](../superpowers/specs/2026-10-11-learning-site-design.md)、
[實作計畫與驗證](../superpowers/plans/2026-10-11-learning-site.md)、[維護說明](../../site/README.md)。

## 已知限制

- 作答、閱讀位置與卡片紀錄只存在該瀏覽器；尚無備份匯出／匯入及跨裝置同步。
- 32 題目前共用同一句通用提示，每章的實作挑戰也是通用模板，尚需內容細化。
- 每章只有 2 道變式，並非每個目標的錯題都有對應變式；缺少時會明示原題重做。
- 題庫對主題的 parent／label 採精確比對；教材命名變動需要一起更新題庫引用。
- 自動判分檢查的是既定題目表現，不能替代空白頁實作、口頭推導或正式 Phase Gate。

## 下一輪建議：先提高每章的學習價值

以下是優先順序與驗收提案，尚未開始新增功能。

### 1. 精修現有四章

先把首批章節做到值得反覆練習，再擴大題數。

- 每題提示指出下一個推理動作：追蹤哪個狀態、比較哪個條件或檢查哪段設定；不直接透露答案。
- 四章各補到至少 4 個有實質條件變化的變式；優先補目前只有原題可重做的目標。
- 每章換成具體實作挑戰，例如 probe 現象預測、cache 交錯時序、指標 trace、路由來回分析；
  附可觀察的檢查標準，不由網站自動給「精通」。
- 逐題核對教材來源與正解，補清合理的替代答案、假設和誤解解說。

驗收：四章各有具體章末挑戰；每題提示確實對應題目；變式不能只換名稱或選項順序；
重新作答仍保留首次紀錄，相關測試與 lint 通過。

### 2. 練習紀錄備份（依使用者回饋延後）

增加一個小型資料管理入口，匯出／匯入作答、卡片與閱讀紀錄。

- 檔案包含 schema version 與匯出時間，匯入先驗證格式再顯示影響摘要。
- 不悄悄覆寫：保留匯入前備份，由使用者在介面確認；格式錯誤則拒絕且不改現有資料。
- 題目 revision 不一致的歷史紀錄保留為舊版，不當成新版已通過。

驗收：跨兩個乾淨瀏覽器匯出／匯入可恢復；壞檔案、儲存失敗與版本不符不會清空既有紀錄。
這一步先解決紀錄可攜性；帳號與雲端同步另行設計。

### 3. 按既有教材擴充章節

候選教材已確認存在，先從 K8s、SD 主線補起；實際先後可按使用者近期學習內容調整。

| 順序 | 候選章節 | 已有教材 |
|---|---|---|
| 第一批 | Service / kube-proxy、Load Balancer | `portfolio/k8s/notes/p2a-service-kube-proxy.md`、`portfolio/sd/notes/day04-05-load-balancer.md` |
| 第二批 | Deployment rollout、Message Queue | `portfolio/k8s/notes/p1-deployment-rollout.md`、`portfolio/sd/notes/day10-message-queue.md` |
| 後續 | Merge Two Sorted Lists | `workspaces/leetcode/linked-list/merge-two-sorted-lists/notes.md`，僅讀取作為教材 |

每批兩章，各至少三種互動與兩個學習目標；題目內容校對後再進站。
驗收沿用現有 schema 與測試，不為新章複製介面或另建題型框架。

### 4. 有實際使用紀錄後，再規劃隔日檢查

增加「隔天仍能解釋／換情境仍能判斷」的章節回訪，依最近表現推薦回到哪章。
題目仍留在章節脈絡，不預設混成跨課程題海；先定義時區與推薦規則再實作。
不把使用天數、答題量或一次全對當成能力指標。

暫緩：帳號系統、排行榜、即時 AI 判分、大量自動產題與影片生成。
下一個最小交付建議為「現有四章題目精修」，再依近期學習內容擴充章節；紀錄備份先延後。

## 後續修正：SD 學習狀態與題庫維護

- 補修 Notification System：Scorecard history 已有 Day 33 留存冷測紀錄，不能只當成「已有教材」。以評量標題中明確的 Day 與主題辨識既有練習，顯示「已練習 · 尚無章節評級」；不把局部冷測當成整章通過，也不公開評量原文。

- 原先沒有 Mastery 評量的 SD 章節一律標成「課綱未開」。現在從 Current Session breakpoint 只提取階段與課綱 Day，標記當前章節「進行中」，不匯出私人斷點文字、不虛構評量。
- 有筆記、尚未評量的課綱節點顯示「已有教材 · 尚未評量」，其餘顯示「課綱待學」。Chat System (Day 35-37) 因而能正確呈現正在學習。
- 兩份 day40-gauntlet-rate-limiter 筆記的 40 是 session 編號，原本誤掛 News Feed。新增 Markdown topic 註記，明確掛回 Distributed Rate Limiter (Day 31-32)。
- 新增 `site/AUTHORING.md`：題庫位置、章節欄位、變式範例、revision、筆記歸屬、驗證與發布方式。題庫測試允許增加變式，不再固定只能八題。
- 驗證：完整 lint 與 13 項 Node 測試通過；開發未修改 `workspaces/`。
