# LeetCode Coach 重建設計

取代 `2026-07-01-leetcode-coach-design.md`。舊設計的實作留在 git 歷史，不刪。

## 1. 為什麼重建

舊系統在 20 場 session 後停擺，之後 25 天沒有動作。停擺當下 `workspaces/leetcode/progress.md`
的狀態：

- Mistake Registry 32 筆 `unresolved`
- chunk 債 5 筆，全部逾期
- Weekly Review 連續順延 5 次

三個根因：

**根因 1：gate 密度超過刷題節奏。** engine 規定每個 chunk 跑一次 Feynman Gate（Recall +
Transfer），step F（teach-to-learn）與 step G（mock）標為 not-skippable。`teaching-elements.md`
規定一題兩個 chunk。一題新題等於 4 個 gate 加一個 retention rung 加 registry 寫入。目標節奏
是一天 2 題，等於一天 10 個 gate。佇列只會累積。

**根因 2：帳本量錯層級。** 32 筆裡重複出現的是 `return` 縮排卡在迴圈內（3 次）、`//` 與 `/`
混淆（2 次）、`.push` 不存在（2 次）、少寫冒號、迴圈變數每圈重算不理解（2 次）、把迴圈結束
狀態當 `while` 條件（2 次）。這些是 Python execution model 的缺口，不是演算法缺口。舊
curriculum 的入口是 P0（Big-O 加 articulation bridge），底下沒有更基礎的一層。

**根因 3：債務沒有到期機制。** 每列只有 `unresolved` 與往上加的 review 計數。`#128` 從 s5
掛到停擺，累積 11 次 review，從未結案。

## 2. 設計原則

**原則 1：系統不產生債務。** 持久化的 state 只回答「現在在哪」，不回答「你欠什麼」。沒有
spaced-repetition queue、沒有 answer-debt、沒有 retention 梯、沒有 weekly review、沒有 phase
gate、沒有 Examiner、沒有 scorecard。

**原則 2：訊號接成溫度計，不接成關卡。** 舊系統的三個檢查（清空重寫、Transfer 問題、隔天
回憶）本身沒錯，錯在失敗會擋路。新系統保留三個檢查，失敗的處置改成當場補完後繼續。

**原則 3：複習寄生在正課，不另開佇列。** 一天 2 題沒有預算養獨立的複習排程。換皮題本身就是
retrieval，NeetCode 順序天然提供間隔。唯一額外的複習是開場 2 分鐘默寫今天要用的 template，
零排程成本。

## 3. 架構決定

leetcode-coach 脫離 `engine/`，成為 standalone skill，但留在本 repo。

**留在本 repo 的理由：** `scripts/lab-lc.sh` 的 pytest harness 可直接沿用（含 large-N
tripwire）；30 幾個題目資料夾的 `notes.md` 與 `solution.py` 已在此；repo 已跨機器同步。搬到
新 repo 要重做 plugin manifest、marketplace 註冊、harness 搬遷、歷史搬遷、兩台機器重設，換不到
學習上的好處。

**代價與處理：** repo 的 CLAUDE.md 描述「learning coaches sharing one teaching engine」在重建後
不再成立。改描述，不搬 repo：

```
Claude Code plugin: learning coaches。k8s / sd / terraform / ca 共用 engine/；
leetcode-coach 是 standalone（節奏不同，見其 SKILL.md）。
```

`scripts/lint-coach.sh` 目前硬性要求 `SKILL.md` 含 `engine/ENGINE.md` 與 `engine/GOVERNANCE.md`，
並強制 6 個 reference 檔存在。加一個 opt-out 分支，其他四個 coach 不受影響：

分支必須放在 `base=` 賦值與既有的 `[ -f "$base/SKILL.md" ]` 檢查**之後**、`required=(...)`
迴圈**之前**：

```bash
# standalone coach: 只檢查 SKILL.md + evals，跳過 engine 耦合與 hook 檔檢查
if grep -qF 'engine: standalone' "$base/SKILL.md"; then
  [ -s "$base/evals/evals.json" ] || { echo "MISSING or EMPTY: $base/evals/evals.json"; exit 1; }
  exit 0
fi
```

`lint-all.sh` 的 template 檢查（`templates/coach/references/*.md.tmpl` 含 TODO sentinel）針對
新 coach 的鷹架，不受影響。

## 4. 教學迴圈

### 4.1 開場（固定）

不看任何東西，默寫今天這題要用的 template。默不出來就對照抄一遍。上限 2 分鐘，不糾纏。
這是溫度計第 3 層。

### 4.2 龜模式（pattern 首刷題，或該題含新招）

先產出 eli5 圖解頁（規格見第 5 節），學生自行閱讀，再進對話。對話跑 8 步教學，4 階拷問
織在步驟之間：

| 順序 | 內容 |
|---|---|
| 步驟 1 | 白話講題目在幹嘛，一句話，不念題目原文 |
| 步驟 2 | 這是什麼題型，加 2 到 3 個秒認信號 |
| 拷問 ① | 說思路：「你會怎麼做？暴力的也算」（在教解法之前問） |
| 步驟 3 | 最直覺的暴力想法，加它為什麼慢，畫出來 |
| 步驟 4 | 做法一步一步，用圖手動走一遍，沒有 code |
| 拷問 ② | 預測下一步：「第 3 步做完，第 4 步該做什麼？」 |
| 步驟 5 | code 逐行解釋，每個變數說明用途 |
| 步驟 6 | 用步驟 4 的同一個例子跑一遍 code |
| 拷問 ③ | 填關鍵 code：給骨架，挖掉 1 到 2 行最關鍵的 |
| 步驟 7 | 你最可能犯的錯，從 `my-common-bugs.md` 撈 |
| 拷問 ④ | 不看答案獨立寫完整 code，跑 harness |
| 溫度計 ② | 變形問題：「拿掉這行會怎樣？」 |
| 步驟 8 | 一句口訣加一個可重複使用的模板 |

步驟 4 與步驟 6 必須用同一個例子。步驟 4 用手走（具體），步驟 6 用 code 走（抽象），收尾
點明兩者做的是同一件事。這是龜模式最重要的一下，且不多花時間。

對話中大量使用 ASCII 圖。圖解頁是靜態教材，對話中的 ASCII 針對學生當下答錯的那一步畫。

### 4.3 兔模式（換皮題）

學生無法憑空寫出換皮題，這是已確認的前提。兔模式是拿模板改，不是憑空寫：

1. 念題目，學生講出「這什麼型、跟哪一題同款」
2. 貼出學生自己那份模板，學生指出「這題要改哪幾行」
3. 學生改。改不動就說，coach 給提示
4. harness 綠之後問一個變形問題，收工

### 4.4 Hard 規格（NeetCode 順序內出現的 Hard）

不跳過，但只練「講得出來」，不練「寫得出來」。

| 項目 | Medium | Hard |
|---|---|---|
| 目標 | 獨立寫出來 | 拆解成已學過的組件，講得出思路 |
| 對照打 | 退路 | 預設動作 |
| 清空重打 | 要 | 不要 |
| 交付物 | harness 綠 | 一句話說出「這題等於哪幾個學過的東西疊起來」 |

理由：NeetCode 的 Hard 多為已知 pattern 的疊加（#23 等於 heap 加 #21，#25 等於 #206 加分組）。
價值在看穿疊加，不在手速。

### 4.5 卡住協定

取代舊的 answer-debt。由學生說「不會」推進，沒有計時：

```
階 1   coach 指位置，不講錯在哪
        ↓ 學生說「不會」
階 2   coach 縮小到概念
        ↓ 學生說「不會」
階 3   給答案，學生對照打，存一句口訣。不記債，結束。
```

看答案與對照打 code 是合法動作。學習時段多為上班空檔，來回猜測的成本高於直接給答案。

### 4.6 三層溫度計

三個檢查測不同的東西，一個測不到另一個：

| 層 | 檢查 | 測什麼 | 成本 |
|---|---|---|---|
| 1 | 對照打完，當場清空重打 | 短期記憶 | 3 到 5 分鐘 |
| 2 | 立刻問一個變形問題 | 理解 | 30 秒 |
| 3 | 隔天開場默寫 template | 留存 | 2 分鐘 |

第 2 層是治 illusion of competence 的主力，因為它是唯一短期記憶過不了的檢查。變形問題問
「拿掉這行會怎樣」，不問 code 長什麼樣。抄過的人答不出來。

三層任何一層失敗，處置都是當場補完後繼續，不記債、不排期。

第 1 層若時間不夠，降級為隔天開場默寫該 template（即第 3 層），並在 pattern 狀態表標記
「對照打」。

## 5. eli5 圖解頁規格

每題一頁 HTML artifact，先產出、學生先讀、再進對話。code 區塊用原生 `<details>` 摺疊，學生
自行決定何時展開。

```
① 白話：這題在幹嘛                        預設展開
② 這是什麼型，加秒認信號                  預設展開
③ 暴力法長怎樣、為什麼慢（圖）            預設展開
④ 做法一步一步（圖，手動走一遍，無 code） 預設展開
▸ 完整 code 加逐行解釋                    摺疊
▸ 逐輪執行模擬表                          摺疊
▸ 口訣加模板                              摺疊
▸ 這次的釐清（session 結束時補寫）        摺疊
```

「這次的釐清」格式：

```
✗ 我以為：nxt 每一圈都是同一個
✓ 其實是：每一圈重新求值，第 2 圈的 nxt 是 3 不是 2
→ 為什麼會搞混：把「賦值」看成「綁定」了
```

檔案落在該題資料夾內，命名 `eli5.html`，發布為 artifact，URL 記在該題 `notes.md`。同一題重跑
時 redeploy 到同一個 URL。

**題目資料夾規則：** 新題落在 `workspaces/leetcode/<pattern-slug>/<problem-slug>/`（例
`linked-list/merge-two-sorted-lists/`）。既有的 `p1-` / `p2-` / `p3-` 資料夾原地不動，不做搬遷。
`#206` 沿用既有的 `p3-binsearch-linkedlist/reverse-linked-list/`（已有 `solution.py`、
`notes.md`、`test_reverse_linked_list.py`）。路徑不一致由 `progress.md` 的「做過」行負責索引，
不值得為一致性做 migration。

## 6. Curriculum

### 6.1 Layer 0（開場一次帶完，不寫題）

內容從那 32 筆倒推，不是通用 Python 教材：

1. 變數等於貼標籤，不是數學等號
2. `/` 給小數、`//` 給整數；index 只吃整數
3. list 的方法：`append` 不是 `push`、`pop`、`[-1]`
4. 縮排等於這行屬於誰；迴圈內與迴圈後的差別
5. 迴圈變數每一圈重算
6. `while X:` 的 X 是「還要不要再跑一圈」，不是「結束時長什麼樣」
7. node、pointer、`.next` 等於火車廂

遞迴不放 Layer 0，走到 Tree 再教。

### 6.2 Linked List（起點，對齊讀書會）

NeetCode 順序。下表的順序需在第一天開始前跟讀書會實際進度核對一次。

| 題號 | 題目 | 模式 | 備註 |
|---|---|---|---|
| 206 | Reverse Linked List | 龜 | 2026-08-03 做過，重跑 |
| 21 | Merge Two Sorted Lists | 兔 | |
| 141 | Linked List Cycle | 小龜 | fast-slow 是新招 |
| 143 | Reorder List | 兔 | 等於中點加反轉加合併 |
| 19 | Remove Nth Node From End | 兔 | |
| 138 | Copy List with Random Pointer | 兔 | |
| 2 | Add Two Numbers | 兔 | |
| 287 | Find the Duplicate Number | 兔 | fast-slow 換皮到陣列 |
| 146 | LRU Cache | 龜 | 新結構：hash 加雙向鏈 |
| 23 | Merge K Sorted Lists | Hard 規格 | 等於 heap 加 #21 |
| 25 | Reverse Nodes in k-Group | Hard 規格 | 等於 #206 加分組 |

龜兔判準看「這題有沒有沒見過的動作」，不看題號順序。同一個 pattern 底下也可能藏新招。

Linked List 之後的順序依讀書會進度決定，不預先排。

## 7. 檔案異動

### skills/leetcode-coach/

| 檔案 | 動作 |
|---|---|
| `SKILL.md` | 重寫。不 read engine。標記寫在**內文第一行**，不放 frontmatter（其他 coach 的 frontmatter 只有 `name` 與 `description`，不要引入新鍵）：`<!-- engine: standalone -->` |
| `references/north-star.md` | 刪 |
| `references/teaching-elements.md` | 刪 |
| `references/scorecard-dims.md` | 刪 |
| `references/phase-gates.md` | 刪 |
| `references/portfolio.md` | 刪，資料夾規則併入 `teaching-loop.md` |
| `references/problem-solving-framework.md` | 刪 |
| `references/language.md` | 刪，併入 `SKILL.md` |
| `references/ops-coding-bank.md` | 留，但不接進新迴圈。`docs/plans/2026-08-11-module-roadmap.md:15` 仍引用它，且 ops coding 驗收場排在 2026-09，是獨立模組，不在本次重建範圍 |
| `references/curriculum.md` | 重寫，內容見第 6 節 |
| `references/teaching-loop.md` | 新增，內容見第 4 節 |
| `references/layer0-execution-model.md` | 新增，內容見 6.1 |
| `references/my-common-bugs.md` | 新增，從 32 筆對靈 |
| `references/pattern-cheatsheet.md` | 留 |
| `references/python-dsa-cheatsheet.md` | 留 |
| `references/complexity-cheatsheet.md` | 留 |
| `references/lab-manager.md` | 留 |
| `evals/evals.json` | 更新，對齊新迴圈 |

### workspaces/leetcode/

| 檔案 | 動作 |
|---|---|
| `progress.md` | 重寫，schema 見第 8 節 |
| `one-liner-library.md` | 沿用，作為口訣本 |
| `patterns.md` | 移到 `archive/pre-rebuild/` |
| `retention.md` | 移到 `archive/pre-rebuild/` |
| `session-log.md` | 移到 `archive/pre-rebuild/` |
| `skeleton-registry.md` | 移到 `archive/pre-rebuild/` |
| `p1-*/ p2-*/ p3-*/` | 不動 |

### 其他

| 檔案 | 動作 |
|---|---|
| `scripts/lint-coach.sh` | 加 standalone opt-out 分支 |
| `CLAUDE.md`（repo 根） | 改描述，見第 3 節 |
| `README.md` | 更新 4 處：L56 coach 檔案樹、L76 `workspaces/leetcode/` 說明（目前寫 `progress.md (engine schema)`，已不成立）、L113 遷移表、L119 symlink 說明 |

## 8. progress.md schema

engine 的 PROGRESS-SCHEMA 不再適用。新 schema 只有三節：

```markdown
# leetcode

- 今天做到：<pattern> / <題號 題名> / <狀態一句話>
- 模式：龜 | 兔 | Hard

## Pattern 狀態
| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 反轉 | ✅ | ✅ | ✅ #206 | 存下一個、改指向、兩個往前挪 |

## 做過
206 ✅ | 21 ⏳
```

沒有到期日欄位、沒有 unresolved 狀態、沒有順延計數。

## 9. my-common-bugs.md schema

checklist，不是帳本。可以持續長大，按犯過次數排序，最上面是最常犯的。

```markdown
寫完 code、跑 harness 之前掃這張表：

□ return 是不是縮排卡在迴圈裡？（犯過 3 次）
   症狀：找得到的全掛、找不到的全綠
□ 算 index 有沒有用 //？（犯過 2 次）
□ list 是 .append 不是 .push（犯過 2 次）
□ if / for / while / def 後面的冒號補了嗎？
□ 變數名有沒有手滑？（pairs/paris、answes）
□ while 裡填的是「還要不要再跑一圈」，不是「結束時長什麼樣」
```

欄位只有：症狀、犯過幾次、怎麼防。升級規則：一次性的搞混留在該題圖解頁的「這次的釐清」，
重複出現才升上這張表。

## 10. 已知天花板

此設計針對 Easy 加 Medium、senior DevOps coding 輪。觸發升級的條件三選一：

1. 目標公司換成算法題比重高的
2. recruiter 明確說 round 會有 Hard
3. Medium 已經穩到無聊

升級要動的只有兩處，不需重寫：龜模式比例拉高（目前只有 pattern 首刷題走龜）、加 Hard 題池。

此條以註解形式寫進 `references/curriculum.md` 頂端。

**已接受的取捨：** 允許看答案與對照打會提高 illusion of competence 的風險，由三層溫度計對沖，
但不會歸零。放棄獨立複習佇列會降低長期留存，由開場默寫與換皮題的 interleaving 部分補回。
兩者都是為了換取續航，因為舊系統的失效模式是完全停擺，不是留存不足。

## 11. 驗收條件

1. `./scripts/lint-all.sh` 通過，五個 coach 全綠
2. `skills/leetcode-coach/` 下不存在第 7 節列為刪除的檔案
3. `grep -rF 'engine/ENGINE.md' skills/leetcode-coach/` 無結果
4. 重建當下 `workspaces/leetcode/progress.md` 行數少於 30（此表會隨 pattern 增加而長，
   只驗收重建當下的值）
5. `scripts/lab-lc.sh` 對既有任一題目資料夾仍 exit 0
6. k8s / sd / terraform / ca 四個 coach 的檔案零異動
