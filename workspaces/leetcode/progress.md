# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone leetcode-notes docs/session-progress-archive.md (original verbatim in
     archive/pre-migration/; entry reconciliation in archive/pre-migration/README.md).
     One-liners live in one-liner-library.md; skeleton recall in skeleton-registry.md;
     the cross-pattern playbook builds in patterns.md; per-problem work in <phase>/<slug>/.
     Standalone 時期多數列以 session 編號為鍵、未記日期;已知日期照填,其餘標 (未記日期)。
     間隔複習排程欄位為 migration 初始化的近似值(以已知 session/commit 日期推 +3d/+7d;
     無日期者以轉換日 2026-07-10 起算),原始相對排程(+3d/+7d/+14d)引註於各列。
     Resolved 歷史(54 列)留在 archive 原檔,不逐列重排;此處只序列化 open 項。 -->

## Meta

- session_count: 18
- last_weekly_review: 0 — 🔴 從未跑過;18-0 ≥ 7,**第 3 次順延**(S17 學生選推遲、S18 折衷方案只回收 binary-search 債)。S19 前置:完整 Weekly Review(3 題 blind recall + Mistake Registry 全測 + P0 gate)
- last_session_date: 2026-07-14
- warm_up_classification: (standalone 時期未記錄;既有證據:blank-page 傾向為主要弱點,S16 顯示 bridge 已能自主運行 — 建議 S17 順帶補跑分類,不當新生重測)

## Current Session breakpoint

**S18 (2026-07-14) 學生喊停** | phase P3 | topic: #153 Find Minimum in Rotated Sorted Array(七步 flow 首次啟用)
- Chunk 1 「推導」(第 0-3 步):Recall ✅(五問腳本以 code 形式跑出,零 bug)
- Chunk 2 「驗證」(第 4 步 + step D):step D **19/19 green,含對數 tripwire(讀取次數 ≤ 100)**,solution.py 手打**零 bug**(對比 #74 有 2 bug)
- **Transfer ❌ 未答** — 停在 #33 兩問:① `while l < r` 還 `l <= r`,用「mid 要不要留」判準推 ② #33 的 check 比 #153 多做什麼(判斷 target 在不在有序的那半)
- next: 開場先答 #33 兩問(Transfer gate)→ step E 用 #33 驗收

⚠️ S18 = Weekly Review 第 3 次順延(學生選折衷:今天 #153 + 只回收 binary-search 債)。順延債務:
- 🔴 **Weekly Review #1** — 逾期 18 sessions,S19 必須先跑(3 題 blind recall:binary-search / stack / two-pointers)
- ① #704 Binary Search cold re-do(fluency 驗收,**逾期**)— 註:#153 手打零 bug 已部分證明 skeleton fluency,但 #153 是 `l<r` 變體,#704 的 `l<=r` 閉區間版仍未冷寫回測
- ② A2/A4 answer-debt(S18 學生喊「直接說明」,答案由 coach 給出)— 3 天內白紙重考,見 Mistake Registry
- ③ 舊債:#84 stack cold re-do(answer-debt,逾期)/ 教 Yuki(#84 + Car Fleet)/ P0 Gate 正式驗收
- ④ #74 Chunk 3(complexity bound gate)未跑,step E 未跑
- ⏸️ Parked Feynman 債(Transfer Q2/Q3):#239 Sliding Window Maximum、#42 Trapping Rain Water、#11 Container With Most Water
- ⏸️ Queued:Sliding Window 基礎題 #121 / #3(有 brute 半成品)/ #567(做到 step E)

## Phase status

- P0 Problem-Solving Mental Model: in-progress(articulation bridge 已日常運行、Big-O 概念多次驗證;但 gate 從未正式跑,列為舊債 — 不回填 retroactive pass,無 Examiner 證據)
- P1 Arrays / Hashing / Two Pointers: in-progress(Arrays & Hashing 5/11、Two Pointers 2.5/5;讀書會 jump-to 順序,缺口見 mastery)
- P2 Sliding Window / Stack: in-progress(Stack 6/6 完成、Sliding Window 1/5;#84 未冷寫)
- P3 Binary Search / Linked List: in-progress(Binary Search 1/6,S16 開場;Linked List 0/9)
- P4 Trees: not-started
- P5 Heap / Backtracking: not-started
- P6 Graphs + 1-D DP: not-started
- P7 Interview Sprint: not-started

注:standalone 時期讀書會採 jump-to(照 NeetCode 順序但跨 pattern 跳題),故多 phase 同時
in-progress。Gate 順序照 curriculum 補齊:P0 gate 先行,P1/P2 缺口補完再各自 gate。

## Mastery

- arrays-hashing: med (s5;Frequency Counter / Bucket Sort / Length-Prefix / HashSet per row-col-box / Sequence Start Detection 學會;#238 skipped 待補)
- two-pointers: med (s7;#42 Hard 三層全綠,但 Feynman Q2/Q3 看答案 — 升 high 條件:transfer Q 自答)
- sliding-window: med (s8;#239 Hard 親手寫完,基礎 5 題未做;Feynman Q2/Q3 + Mock 待補)
- stack: high (s15;NeetCode Stack 全清,#84 code 未冷寫 — 冷寫過才算穩)
- binary-search: med (s18;#704 Learn 模式 skeleton 冷寫首次 100%;#74 手打 2 bug;#153 手打**零 bug** 19/19 green。升 high 條件:① #704 閉區間版 cold re-do 零 bug ② 開閉區間配對規則(`l<r` vs `l<=r`)能直覺產出而非現場推導)

## Scorecard history

- (s1, 未記日期) | step G (standalone interview drill) | 3/3 | — | Think aloud / Pattern ID / Code runs 全過 | coach(pre-Examiner,legacy 認證)

## Mistake Registry

Open 項(15 列)自 standalone 遷入;原始狀態原文引註。Resolved 54 列見 archive 原檔。

- (s5, 未記日期) | arrays-hashing #128 | 起點判斷邏輯反了(有值→沒值)| sequence-start-detection | unresolved(原:🟡 Parked - 補課時理解,尚未自主應用測試)| 3 | 2026-07-10 | 11 ⚠️ Priority Override
- (s7-d2, 未記日期) | two-pointers #42 | Feynman Q2(`[5,4,3,2,1]` 為什麼 0)沒自答 | transfer-question-self-answer | unresolved(原:🟡 Parked - Day 3 Step A 重抽)| 3 | 2026-07-10 | 9 ⚠️ Priority Override
- (s7-d2, 未記日期) | two-pointers #42 | Feynman Q3(heights 允許負數會壞掉)沒自答 | transfer-question-self-answer | unresolved(原:🟡 Parked - Day 3 Step A 重抽)| 3 | 2026-07-10 | 9 ⚠️ Priority Override
- (s9, 未記日期) | stack #20 | 變數名手滑 pairs→paris→pairss(連三次)| variable-name-precision | unresolved(原:🟡 Recurring - 同 num/nums, window/windows 家族)| 3 | 2026-07-10 | 7 ⚠️ Priority Override
- (s11, 未記日期) | stack #150 | 忘記 return(第 4 次)症狀:答案全 None | missing-return-reflex | unresolved(原:🟡 Recurring - 反射:看到 None 先查 return)| 3 | 2026-07-10 | 5 ⚠️ Priority Override
- (s13, 未記日期) | stack #739 | `answes[prev]` 變數名手滑 | variable-name-precision | unresolved(原:🟡 Recurring)| 3 | 2026-07-05 (approx) | 3
- (s13, 未記日期) | stack #739 | cold solve `stack, append(i)` 逗點⇄點 → NameError(自讀錯誤訊息修好)| character-precision | unresolved(原:🟡 Recurring - debug 反射 ✅ 養成中)| 3 | 2026-07-05 (approx) | 3
- (s13, 未記日期) | stack #739 | Yuki 拷問盲點:把「while 不執行」誤歸因成「ans 初始化=0」;攤還 O(n) 需動畫才懂 | condition-vs-value + amortized-argument | unresolved(原:🟡 Re-test +3d;抽問:① while 條件 vs 答案值兩條獨立線 ② 每元素一生 pop 一次 → 總 pop ≤ n)| 3 | 2026-07-05 (approx) | 3
- (s13, 未記日期) | stack #739 | Yuki spot-my-bug:縮排雷達對但指錯行(指 append,真兇 return 卡 for 內)| precise-line-blame | unresolved(原:🟡 Re-test +3d;方法:每行問「這動作該做幾次」;S16 已一次指對行,再驗一次可 resolve)| 3 | 2026-07-05 (approx) | 3
- (s14, 未記日期) | stack #853 | `if` 開頭行結尾少冒號 | colon-reflex | unresolved(原:🟡 Recurring - 反射:寫完 if/for/while/def 先補 `:`)| 3 | 2026-07-05 (approx) | 2
- (s14, 未記日期) | stack #853 | 邏輯反:`if stack` vs `not stack`;且 `not stack` 必須放 `or` 左邊短路保護 `stack[-1]` | list-truthiness + short-circuit-guard | unresolved(原:🟡 Re-test +3d;抽問:① `if stack:` 是空還是有? ② 為什麼 `not stack` 要在左邊)| 3 | 2026-07-05 (approx) | 2
- (s14, 未記日期) | stack #853 | `stack.push()` — Python list 沒 `.push` 應 `.append`,且括號內空的 | method-name-precision | unresolved(原:🟡 Recurring - 同 `.top` 錯方法名家族)| 3 | 2026-07-05 (approx) | 2
- (2026-07-02, s15) | stack #84 | 猜 stack 是「遞減」(其實遞增);沒連結「pop 條件決定方向」| monotonic-direction-mechanism | unresolved(原:🟡 Re-test +7d;改考機制不考題號:「pop 條件是『比隊尾矮就踢』時 stack 維持遞增還遞減?」)| 7 | 2026-07-09 | 1
- (2026-07-08, s16) | binary-search #704 | `mid=(l+r)/2` 用 `/`(float)→ `nums[float]` TypeError;索引要 `//` | floor-div-for-index | unresolved(原:🟡 Recurring 觀察 - #11 `//` 的鏡像;反射:算索引/中點一律 `//`)| 3 | 2026-07-11 | 0
- (2026-07-08, s16) | binary-search #704 | `r=len(nums)` 越界;all pass 沒抓到(測試沒 hostile input)| closed-interval-bounds + hostile-input-reflex | unresolved(原:🟡 Re-test +3d;抽問:閉區間 `[l,r]` + `while l<=r` 時 r 初始 `len-1`;「綠燈≠正確」)| 3 | 2026-07-11 | 0
- (2026-07-13, s17) | binary-search #74 | 以為 binary search 的前提是「array 要 sorted」;實為「捨棄的半邊保證不含 target」(sorted 只是取得該許可證的手段)| discard-license-vs-sorted | unresolved(抽問:沒排序的 array + 一個保證答對的 oracle,能不能 binary search?為什麼 Koko 沒有 sorted array 卻是 binary search?)| 3 | 2026-07-16 | 0
- (2026-07-13, s17) | binary-search #74 | Transfer FAIL:能複誦抽象原則,無法套到具體元素上。問「砍掉 row0/row1 需要什麼保證」時把原則原句抄回,講不出「這兩個 row 的每個元素都 < target」| principle-instantiation | unresolved(根因疑似同 blank-page 家族:抽象→具體的實例化能力。抽問法:給原則 + 具體矩陣,要求指名元素)| 3 | 2026-07-16 | 0
- (2026-07-13, s17) | binary-search #74 | `n = len(matrix)[0]` 括號放外面 → `TypeError: 'int' object is not subscriptable` | character-precision | unresolved(🟡 Recurring 第 2 次,同 S13 `stack, append(i)` 家族;此類 bug 當場報錯,成本低)| 3 | 2026-07-16 | 0
- (2026-07-13, s17) | binary-search #74 | `return False` 縮排卡在 `while` 內 → 每次只跑 1 圈,期望 True 的 11 題全掛、期望 False 的 8 題全綠 | precise-line-blame + return-placement-in-loop | unresolved(🔴 **第 2 次同型**,S13 #739 `return` 卡 `for` 內由 Yuki 抓出。危險性遠高於 syntax error:不報錯、部分測試綠。抽問:「哪些行該在迴圈內、哪些該在迴圈後?判準是什麼?」)| 3 | 2026-07-16 | 0
- (2026-07-13, s17) | binary-search #74 | 連續 2 次跳過「為什麼 `l = mid + 1` 而非 `l = mid`」的機制題(捨棄許可證的實例化)| discard-license-vs-sorted(同上游)| unresolved(抽問:`val < target` 時,為什麼連 mid 自己也丟?)| 3 | 2026-07-16 | 0
- (2026-07-14, s18) | binary-search #153 | 以為 `int // int` 也回 float(「`//` 也是 float 沒有餘數」)。實為 int;`/` 才回 float,而 float **不能**當索引也不會自動轉 | floor-div-type-confusion(S16 `//` 家族第 2 次)| unresolved(有拒絕誘餌 ✅ 但機制講錯;抽問:`7//2` 和 `7/2` 各回什麼型別?)| 3 | 2026-07-17 | 0
- (2026-07-14, s18) | binary-search #153 | 講不出 `r = len(nums)` 的**具體反例**,只複誦「因為是 index 所以要 -1」| hostile-input-reflex | unresolved(**answer-debt**:coach 給了答案;3 天內白紙重考。抽問:給 `nums=[1,2,3]`, `target=5`,逐圈跑到爆為止)| 3 | 2026-07-17 | 0
- (2026-07-14, s18) | binary-search #153 | 講不出「這行該在迴圈內還是迴圈後」的判準 | loop-placement-criterion | unresolved(**answer-debt**;🔴 同 return-卡迴圈家族第 3 次接觸。判準:「這動作該做幾次?」每圈一次→內;結束後一次→外。抽問時要學生自己講出判準)| 3 | 2026-07-17 | 0
- (2026-07-14, s18) | binary-search #153 | `[5,6,7,1,2,3,4]` mid=3(值 1)誤標成「第一段」,但同時答對「mid 不能丟、證人是 mid 自己」→ 機制對、標籤反 | segment-labeling | unresolved(用矛盾點自行修正。抽問:第一段=高的還低的?第一段的元素有可能是最小值嗎?)| 3 | 2026-07-17 | 0
- (2026-07-14, s18) | binary-search #153 | 學生自述:`while` 加不加 `=`、`r=mid` 還是 `mid+1`,無法直覺產出,要現場想 | interval-openness-pairing | unresolved(**最高價值項**。配對規則:兩邊都跳 mid → `l<=r`;有一邊留 mid → `l<r`。抽問:`l<=r` 配 `r=mid` 會怎樣?為什麼?)| 3 | 2026-07-17 | 0

## Spaced-repetition queue

Mistake 項引用上表(不重複)。Chunk 型債務:

- chunk:p3/#153 Chunk 2 Transfer 兩問(#33 的迴圈條件 + check 多做什麼)| chunk | — | 2026-07-15(下次開場)| active
- chunk:p3/binary-search #704 cold re-do(fluency 驗收)| chunk | 3 | 2026-07-11 | active
- chunk:p2/largest-rectangle #84 cold re-do(answer-debt:S15 code 是看的)| chunk | 3 | 2026-07-05 (approx, 逾期) | active
- chunk:teach-back #84 + Car Fleet(S14/S15 跳過的 pattern 收尾教學)| chunk | 3 | 2026-07-05 (approx, 逾期) | active

## Curiosity branch

(none — standalone 時期未記錄 parked threads)

## Domain registries

- `one-liner-library.md` — 18 條 pattern one-liners(standalone Pattern One-Liner Library 遷入)
- `skeleton-registry.md` — 核心 skeleton recall 排程(code 本體在 references/pattern-cheatsheet.md)
- `retention.md` — 留存階梯(七步 flow 第 6 步;S18 建立,首列 #153)

## Examiner ledger

(empty — Examiner 制度自遷入起算;legacy 認證見 scorecard history 的 pre-Examiner 標記)
