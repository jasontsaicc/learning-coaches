# Learning Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task if native execution is selected, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox syntax for tracking.

**Goal:** 提供好維護的個人學習網站，以逐章多題型練習檢查理解，改善搜尋、閱讀與視覺體驗。

**Architecture:** 保留 Python 靜態生成器、既有 JSON 節點與 hash routes。原生 ES modules 分離頁面、章節練習、卡片與地圖；題庫獨立 JSON，作答只存瀏覽器。教練評量繼續唯讀。

**Tech Stack:** Python stdlib、HTML/CSS、原生 JavaScript modules、既有 D3/marked/DOMPurify、Node 內建測試；不新增 runtime 依賴或 bundler。

**Spec:** `docs/superpowers/specs/2026-10-11-learning-site-design.md`

## Global Constraints

- `workspaces/`、歷史目錄及課程內容不因本次開發而變動。
- 一輪預設 5–8 題，題庫不足則顯示實際題數，不重複湊數。
- 首次無提示答對、提示後答對、練習後答對與略過分開，不回寫正式評量。
- 沿用舊卡片 ID、`srs` key 與 `{box, due}` 格式；不因拆分程式重置紀錄。
- 不新增 npm 依賴或前端 bundler；現有套件載入與 SRI 維持。
- 可點擊區域至少 44px；手機 360px 寬度沒有頁面水平溢出。
- 使用者既有 `site/README.md` 修改需保留；每次提交前跑 `./scripts/lint-all.sh`。
- 網站為自學工具，公開題目答案不構成防作弊考試；題庫不足明示。

## Review Focus

1. 多個主題引用同一份筆記：搜尋去重、最近閱讀不能接續到別章；Task 5。
2. JSON 合法但型別錯誤、storage 額度耗盡：提示並保留原紀錄，不能靜默重置；Tasks 3、4。
3. 瀏覽器返回或重整時正在答題：續答與首次結果不丟失，章節切換不能串題；Task 4。
4. 英文大小寫、數值單位、多選漏選與等價排序：只接受題目明列的判分規則；Tasks 1、3。
5. 原筆記的簡化說法或競態：題目需明列前提並核對官方來源，不能把模糊教材變成唯一答案；Task 2。

## Files and Contracts

| 檔案 | 責任 |
|---|---|
| `site/index.html`, `site/styles.css`, `site/app.js` | 骨架、視覺、路由與頁面 |
| `site/review.js`, `site/map.js` | 保留並隔離卡片及地圖 |
| `site/exercises.js` | 純判分函式及共用作答介面 |
| `site/exercises/{k8s,sd,leetcode,ca}.json` | 四門課程的示範章節 |
| `site/build.py`, `site/test_build.py` | 題庫驗證、資料輸出、靜態檔案與 parser 回歸 |
| `site/test_exercises.mjs`, `site/test_review.mjs`, `site/test_app.mjs` | Node 內建測試 |
| `portfolio/ca/notes/vpc-peering.md` | 新增可閱讀的 CA 章節教材 |
| `scripts/lint-all.sh`, `site/README.md` | 測試入口與維護說明 |

保留 `#/`、`#/c/<coach>`，新增 `#/practice/<chapterId>`、`#/read/<encoded-file-path>`。
題庫輸出到 `data.json.chapters`，避免另加 fetch 與版本不同步。
DOM 模組不得在 import 時執行頁面初始化，讓純邏輯可由 Node 測試。
若 Node 無法直接 import `.js` ES modules，新增僅作用於 site 的
`site/package.json`，內容只有 `{"private":true,"type":"module"}`，不增加套件管理流程。

## Task 1: 題庫契約與真實進度語意

**Files:** Modify `site/build.py`, `site/test_build.py`.

**Interfaces:**
- `validate_chapters(chapters, nodes, allowed_files) -> None`：錯誤拋出含章節／題目 ID 的 ValueError。
- `build()` 在原 nodes/titles 外新增 `chapters: []`；題庫目錄未建立時為空。
- 章節：`id, coachId, phaseId, title, topicRefs, objectives, sources, questions, challenge`。
- `challenge:{prompt,criteria:[string]}` 僅顯示實作任務與檢查標準，狀態固定為待實作／教練驗證。
- `topicRefs` 為 `{parent, label}` 陣列，精確對照既有節點；零匹配或多匹配時建置失敗。
- `objectives` 為 `{id,label}` 陣列；`sources` 為允許匯出的檔案路徑。
- 題目：`id,revision,type,objectiveId,prompt,hint,explanation,source,variantOf?`。
- `source` 為 `{path,section}`；path 必須出現在 chapter.sources 且可匯出。
- `choice`：`multiple:boolean, options:[{id,text,feedback}], answer:[id]`。
- `fill`：`answer:{kind:'text', accepted:[string], caseSensitive:boolean}` 或
  `{kind:'number', value:number, tolerance:number, unit:string}`；單位顯示在輸入框外，只輸入數字。
- `order`：`items:[{id,text}], answer:[[id]]`，每個合法順序都含全部且唯一的 item。
- `match`：`items:[{id,text,feedback}], targets:[{id,text}], answer:{itemId:targetId}`；允許多對一分類。
- LeetCode 做過輸出 `practiced:true, level:null`；其他 coach 原始等級不變。

- [ ] 加 assert cases：重複 ID、不存在答案／來源／topicRef、負容差、零 revision、排序漏項均失敗；合法四種型別通過。
- [ ] 加回歸：做過題目只產生 practiced，不產生 high；新增狀態不能影響原節點關係。
- [ ] 跑 `python3 site/test_build.py`，確認新增案例因尚未實作失敗。
- [ ] 實作驗證、JSON 載入及狀態輸出；不動學員資料。
- [ ] 重跑 parser 測試及 `python3 site/build.py --check`，兩者退出 0。
- [ ] 跑全 repo lint，僅提交本 task 檔案。

## Task 2: 四個章節的真實題目與教材

**Files:** Create `site/exercises/{k8s,sd,leetcode,ca}.json`, `portfolio/ca/notes/vpc-peering.md`; extend `site/test_build.py`.

**Interfaces:** 消費 Task 1 schema；每章 6 道主題目、2 道變式，變式 `variantOf` 指向同章主題目。
固定 chapter ID：`k8s-probes`, `sd-cache-aside`, `lc-linked-list-cycle`, `ca-vpc-peering`。

| 章節 | 既有來源／備課來源 | 至少兩個目標 |
|---|---|---|
| K8s 探針 | `portfolio/k8s/notes/p1-pod-probe.md` | 分辨就緒與重啟、預測慢啟動／下游故障結果 |
| Cache-Aside | `portfolio/sd/notes/day06-07-caching.md` | 追蹤 miss 流程、判斷併發讀寫的陳舊資料窗口 |
| Linked List Cycle | `workspaces/leetcode/linked-list/linked-list-cycle/notes.md` | 區分節點身份與值、追蹤快慢指標及終止條件 |
| VPC Peering | 新 CA 筆記；備課讀 `skills/cloud-architect-coach/references/gap-scan-aws-networking.md` | 判斷路由可達性、辨認非傳遞性與雙向路由需求 |

- [ ] 加題庫整合 assertions：四章各 6 主題＋2 變式、至少 3 題型與 2 目標、來源可解析、同章引用有效。
- [ ] 跑測試確認因題庫未建立而失敗。
- [ ] 查閱完整相關筆記，並以官方 K8s、AWS 及相應原始技術文件核對所出題目的機制；記錄來源連結。
- [ ] 撰寫 CA 公開教材；只載入既有 portfolio notes 規則，不能複製私人 gap scan。
- [ ] 寫 32 題及解析。情境給出必要前提：例如 probe threshold、cache 操作交錯、指標初始位置、路由與安全條件。
- [ ] 逐題自己走一次正解與所有干擾答案；多個合理答案須納入或收緊題幹。填空優先程式缺口，避免只考術語。
- [ ] 明列每章一項待實作／教練驗證的挑戰，不自動評為通過。
- [ ] 跑資料整合測試與全 lint，提交題庫、教材及測試。

## Task 3: 純判分與紀錄相容性

**Files:** Create `site/exercises.js`, `site/test_exercises.mjs`; modify lint entry; add minimal package.json if required.

**Interfaces:**
- `gradeQuestion(question, answer) -> {correct:boolean, details:[{id,correct}]}`。
- `makeRound(chapter) -> questionId[]`：選 6 道非 variant 主題；不足 6 道全部選取，不跨章或重複。
- `recordAttempt(state, question, answer, {hintUsed,confidence}) -> nextState`：回傳新狀態，保留該 revision 的 firstAttempt。
- `loadPractice(storage) -> {state,error}`、`savePractice(storage,state) -> {ok,error}`；依賴傳入的 Storage-like 物件。
- key `learning-map.practice.v1`；state `{version:1, chapters:{[chapterId]:{queue,index,attempts}}}`；
  attempts 以 questionId/revision 為鍵，保存 firstAttempt、latestAttempt、時間、是否提示與結果；不覆寫其他章。

- [ ] 先寫測試：多選漏一項為錯、順序無關；fill trim 正常、caseSensitive 生效、空字串不是 0、容差邊界；排序接受第二種合法答案、重複項拒絕；match 允許多對一但缺項為錯。
- [ ] 寫測試：同題第二次答對保留第一次錯誤；revision 改動不沿用通過；hintUsed 不算無提示答對。
- [ ] 寫 storage mock cases：null／array／錯誤型別／throwing getItem／quota setItem，不覆寫原值且回傳可顯示錯誤。
- [ ] 跑 `node --test site/test_exercises.mjs` 確認失敗，再實作上述最小函式。
- [ ] 重跑到全過；把 Node 檢查加入 lint，缺 Node 時提供明確訊息並失敗。
- [ ] 跑全 lint，提交判分與測試。

## Task 4: 章節練習的完整介面

**Files:** Modify `site/index.html`, create `site/styles.css`, `site/app.js`, `site/map.js`, `site/review.js`; extend `site/exercises.js`, `site/build.py`; create `site/test_review.mjs`.

**Interfaces:**
- `mountPractice(container, chapter, {state,onSave,onExit}) -> cleanup()` 使用 Task 3 函式。
- `drawTree(container,nodes,rootId,{onSelect,selected})` 與 `openCards` 從既有程式搬出，保留依賴注入及清理。
- app 解碼 chapter route，核對 ID；頁面切換前執行 cleanup。
- 複習純函式 `gradeCard(state,id,grade,day)` 保留既有 box/day 規則，UTC 日序及舊 ID。

- [ ] 為 card 排程與「答錯最多重試一次」加紅測試，包含超過 20 張時仍有剩餘到期卡。
- [ ] 原樣抽出 CSS／JS，再加入章節路由與題型介面；build 明列複製的新資產。
- [ ] 每題採提交後判分；提供提示、略過、信心選擇、逐項解說及教材返回；未作答不能提交。
- [ ] 排序使用上下按鈕，match 用具 label 的選單；choice 用原生 radio/checkbox，fill 用表單欄位。
- [ ] 儲存變更後的佇列與索引；重新載入可續答；切章清理 listeners，快速點擊不能重複提交。
- [ ] 完成頁依目標顯示結果；不確定／提示／錯誤題有變式重練，無變式明示原題；每題一輪只加入一次。
- [ ] Flashcards 保留每課入口，修正剩餘量與儲存失敗提示；不推出全課混合模式。
- [ ] 跑純邏輯測試及 build；使用可用瀏覽器工具驗證五種操作（單選、多選、填空、排序、配對），重新整理與返回不串題。
- [ ] 跑全 lint，提交可獨立使用的逐章練習流程。

## Task 5: 首頁、閱讀與搜尋

**Files:** Modify `site/app.js`, `site/styles.css`; create `site/test_app.mjs`.

**Interfaces:**
- `searchContent(data,query) -> {kind,id,title,coachId,path?}[]`：對主題／標題／檔名比對，檔案 path 去重。
- `resolveRecent(data,recent) -> target|null`：使用筆記 path 或 coach/parent/label；多匹配回 null。
- key `learning-map.reading.v1`：保存最近目標及 Markdown scrollTop，不保存私人筆記。
- app 初始化採 `startApp()`，import 時不 fetch，確保純查詢函式可測。

- [ ] 紅測試：大小寫／空白查詢、相同筆記多引用、失效 recent、相同標題不同父節點及歧義引用。
- [ ] 實作查詢與 recently-read；資料錯誤或空資料不能顯示假的零進度。
- [ ] 首頁依序顯示搜尋、繼續閱讀／章節練習、依章待重練、課程卡；沒有紀錄提供選課入口。
- [ ] 課程頁縮小 hero、展開進行中階段、提供章節練習／無題庫狀態；移動版直線排列，不改課綱。
- [ ] Markdown 新閱讀頁加目錄、來源課程返回與位置；只能 fetch data.json 匯出的檔案。
- [ ] fetch 檢查 response.ok，以 AbortController 或 request token 防過期回應覆蓋；路由解码失敗與不存在路徑有返回入口。
- [ ] HTML 維持新頁開啟；Markdown parser 不可用時純文字備援；D3 失效不阻斷其他功能。
- [ ] 瀏覽器測試快速切換兩份不同延遲筆記、404、沒有網路、禁用 storage；狀態正確且可恢復。
- [ ] 跑 Node 測試、建置及全 lint，提交首頁與閱讀更新。

## Task 6: 視覺驗收與交付

**Files:** Update `site/styles.css`, `site/README.md`; fix only failures in owning files.

- [ ] 統一 CSS tokens、狀態文字、主次按鈕，練習回饋避免僅靠紅綠色；加入 focus-visible 與 reduced-motion。
- [ ] 彈窗確認焦點圈限、Escape 與關閉後返回觸發元件；頁面切換將焦點移到標題，不跳走填空輸入焦點。
- [ ] 在 360px 與 1280px 截圖首頁、課程長標題、閱讀、四種題型及結果；確認 44px targets、無頁面水平溢出。
- [ ] 手動完整跑一章無提示答錯、看提示、略過、退出／接續、變式重練，檢查報表不混淆不同作答證據。
- [ ] 自行檢查首批 32 題內容、來源、答案與變式；如有 reviewer，依使用者選擇的執行方式處理。
- [ ] 更新 README：新增章節範例、版本化題目、來源白名單、測試命令、首批覆蓋與單機儲存限制；保留原有未提交內容。
- [ ] 跑 `./scripts/lint-all.sh`、`python3 site/build.py`、`git diff --check`，要求退出 0。
- [ ] 比對開始時的 git 狀態，確認 workspaces/history 沒改且使用者 README 改動保留；每次提交只選本任務檔案。
- [ ] 交付實際預覽位址與截圖位置、通過檢查、尚未有題库的章節清單；無法取得的瀏覽器驗證明示，不稱已完成。

## Execution Handoff

建議由主 agent 在本 session 依序實作，因 schema、判分、畫面與題目內容彼此依賴。
待使用者審閱計畫並選擇親自依序執行或分工後開始；不需再次詢問已確認的功能範圍。
