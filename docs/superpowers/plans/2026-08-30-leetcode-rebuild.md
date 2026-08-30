# LeetCode Coach 重建 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 leetcode-coach 從 engine 上拆下來，改成一天 1 到 2 題、不產生債務、圖解優先的獨立教練。

**Architecture:** 新增 lint 的 standalone opt-out 分支，讓 leetcode-coach 不再需要 engine 耦合與 6 個 engine hook 檔。刪除 7 個 engine ceremony 檔，新增 3 個內容檔（教學迴圈、Layer 0、常犯錯 checklist），重寫 SKILL.md、curriculum、evals 與 `workspaces/leetcode/progress.md`。其他四個 coach 零異動。

**Tech Stack:** Markdown、Bash、Python 3 + pytest（既有 harness）。無新依賴。

**Spec:** `docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md`

## Global Constraints

- 每個 task 結束前 `./scripts/lint-all.sh` 必須印出 `ALL PASS`。
- `skills/k8s-coach/`、`skills/sd-coach/`、`skills/terraform-coach/`、`skills/cloud-architect-coach/`、`engine/` 零異動。
- `workspaces/leetcode/p1-*/`、`p2-*/`、`p3-*/` 題目資料夾零異動（不搬遷、不改名）。
- `legacy/` 與 `workspaces/*/archive/pre-migration/` 是凍結歷史，唯讀。
- Git commit 一行 subject，無 body、無 `Co-Authored-By`、無任何 AI 署名。
- 文件語言：繁體中文敘述，技術名詞保留英文原文。不使用 em dash（—）。
- 目前在 `master`。開始前先 `git switch -c rebuild/leetcode-coach`。

---

### Task 0: 開 branch

**Files:** 無

- [ ] **Step 1: 確認工作區乾淨**

Run: `git status --short`
Expected: 只有 `docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md` 與本 plan 檔是 untracked，沒有其他變更。

- [ ] **Step 2: 開 branch**

```bash
git switch -c rebuild/leetcode-coach
```

- [ ] **Step 3: 記錄 baseline**

Run: `./scripts/lint-all.sh`
Expected: 最後一行 `ALL PASS`。這是重建前的綠燈基準，之後每個 task 都要回到這個狀態。

- [ ] **Step 4: Commit spec 與 plan**

```bash
git add docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md docs/superpowers/plans/2026-08-30-leetcode-rebuild.md
git commit -m "docs(leetcode): add rebuild design spec and implementation plan"
```

---

### Task 1: lint 加 standalone opt-out 分支

**Files:**
- Modify: `scripts/lint-coach.sh`（在 `[ -f "$base/SKILL.md" ]` 檢查之後、`required=(` 之前插入）

**Interfaces:**
- Produces: `lint-coach.sh` 在 `SKILL.md` 含字串 `engine: standalone` 時，只檢查 `SKILL.md` 存在與 `evals/evals.json` 非空，然後 `exit 0`。Task 4 依賴這個行為。

- [ ] **Step 1: 先確認目前的 fail 行為（這就是失敗測試）**

```bash
cp scripts/lint-coach.sh /tmp/lint-coach.sh.bak
printf '\n<!-- engine: standalone -->\n' >> skills/leetcode-coach/SKILL.md
rm -f skills/leetcode-coach/references/north-star.md
./scripts/lint-coach.sh leetcode-coach; echo "exit=$?"
```

Expected: 印出 `MISSING or EMPTY: skills/leetcode-coach/references/north-star.md` 與 `exit=1`。這證明 opt-out 分支還不存在。

- [ ] **Step 2: 還原，不要留下 Step 1 的破壞**

```bash
git checkout skills/leetcode-coach/references/north-star.md skills/leetcode-coach/SKILL.md
git status --short
```

Expected: `git status --short` 對 `skills/leetcode-coach/` 沒有輸出。

- [ ] **Step 3: 插入分支**

在 `scripts/lint-coach.sh` 中找到這兩行：

```bash
[ -f "$base/SKILL.md" ] || { echo "MISSING: $base/SKILL.md"; exit 1; }
required=(
```

在兩行之間插入：

```bash
# standalone coach: 自帶教學迴圈,不掛 engine/。只檢查 SKILL.md 與 evals,
# 跳過 engine 耦合檢查與 6 個 engine hook 檔的存在檢查。
if grep -qF 'engine: standalone' "$base/SKILL.md"; then
  [ -s "$base/evals/evals.json" ] || { echo "MISSING or EMPTY: $base/evals/evals.json"; exit 1; }
  exit 0
fi
```

- [ ] **Step 4: 驗證分支會觸發**

```bash
printf '\n<!-- engine: standalone -->\n' >> skills/leetcode-coach/SKILL.md
rm -f skills/leetcode-coach/references/north-star.md
./scripts/lint-coach.sh leetcode-coach; echo "exit=$?"
```

Expected: 無輸出，`exit=0`。同一個情境在 Step 1 是 exit=1，現在是 exit=0，分支生效。

- [ ] **Step 5: 還原探測用的破壞**

```bash
git checkout skills/leetcode-coach/references/north-star.md skills/leetcode-coach/SKILL.md
```

- [ ] **Step 6: 驗證其他四個 coach 沒被影響**

Run: `./scripts/lint-all.sh`
Expected: `k8s-coach OK`、`sd-coach OK`、`terraform-coach OK`、`cloud-architect-coach OK`、`leetcode-coach OK`（此時 leetcode 仍走舊路徑，因為 marker 還沒進 SKILL.md），最後 `ALL PASS`。

- [ ] **Step 7: Commit**

```bash
git add scripts/lint-coach.sh
git commit -m "chore(lint): allow standalone coaches to opt out of engine hook checks"
```

---

### Task 2: 產出 `my-common-bugs.md`

必須在 Task 6 archive 舊 `progress.md` **之前**做，資料來源是舊 Mistake Registry 的 32 列。

**Files:**
- Create: `skills/leetcode-coach/references/my-common-bugs.md`
- Read-only source: `workspaces/leetcode/progress.md`（`## Mistake Registry` 段）

**Interfaces:**
- Produces: `references/my-common-bugs.md`，兩個 `## ` 區塊：`## 寫 code 前掃這張表`（機械錯，按次數排序）與 `## 你容易搞混的觀念`（概念錯，餵教學迴圈步驟 7）。Task 4 的 SKILL.md 讀哪些檔表格會引用這個路徑。

- [ ] **Step 1: 建檔**

```bash
cat > skills/leetcode-coach/references/my-common-bugs.md <<'EOF'
# 我的常犯錯

這是 checklist,不是帳本。沒有到期日、沒有未結狀態、沒有順延計數。

**升級規則:** 一次性的搞混留在該題圖解頁的「這次的釐清」區塊。重複出現才升上這張表。
新增一列時把次數寫上去,並重新按次數排序,最上面永遠是最常犯的。

初始內容來自 2026-08-28 重建前 Mistake Registry 的 32 列(s5 到 s20),已合併同家族。

## 寫 code 前掃這張表

| # | 檢查 | 犯過 | 症狀 |
|---|---|---|---|
| 1 | `return` 是不是縮排卡在迴圈裡? | 3 | 找得到的全掛、找不到的全綠。不報錯,所以最貴 |
| 2 | 算 index 有沒有用 `//`?`/` 回 float,float 不能當 index | 2 | `TypeError: list indices must be integers` |
| 3 | 變數名有沒有手滑?(pairs→paris→pairss、answes) | 2 | `NameError` |
| 4 | 字元有沒有打錯?(`stack, append(i)` 的逗點、`len(matrix)[0]` 的括號位置) | 2 | 當場報錯,成本低 |
| 5 | 閉區間 `[l, r]` 配 `while l <= r` 時,`r` 初始值是 `len(nums) - 1` 不是 `len(nums)` | 2 | `IndexError`,或測資不夠 hostile 而整組漏掉 |
| 6 | Python list 是 `.append`,沒有 `.push` | 1 | `AttributeError` |
| 7 | `if` / `for` / `while` / `def` 開頭的行,結尾冒號補了嗎? | 1 | `SyntaxError` |
| 8 | `if stack` 是「有東西」,`not stack` 是「空的」。`not stack` 要放 `or` 左邊短路保護 `stack[-1]` | 1 | `IndexError` 或邏輯全反 |

## 你容易搞混的觀念

這一段餵教學迴圈的步驟 7(主動指出最可能犯的錯)。不是 checklist,是教的時候要主動戳的點。

| # | 觀念 | 出現過 | 怎麼戳 |
|---|---|---|---|
| 1 | **「這行什麼時候被求值」** 沒有心智模型。三個症狀同源:`while` 條件答成迴圈結束狀態、迴圈變數以為每圈不變、講不出哪些行該在迴圈內 | 4 次跨題 | 問「這行在第 k 圈執行時,值是誰?依賴什麼?」 |
| 2 | binary search 的前提是「丟掉的那半保證不含 target」,**不是**「array 要 sorted」。sorted 只是取得這個許可證的手段 | 3 | 問「沒排序但有一個保證答對的 oracle,能不能 binary search?Koko 沒有 sorted array 為什麼是 binary search?」 |
| 3 | 抽象原則講得出來,套不到具體元素上(給原則加具體矩陣,講不出「這兩個 row 的每個元素都小於 target」) | 2 | 給原則加一個具體例子,要求指名是哪幾個元素 |
| 4 | harness 掛了先看 code,沒先看 fail/pass 分布 | 2 | 給一組 fail 分布,問這是哪一類邏輯錯 |
EOF
```

- [ ] **Step 2: 驗證內容完整且無殘留**

```bash
grep -c '^| [0-9]' skills/leetcode-coach/references/my-common-bugs.md
grep -c '^## ' skills/leetcode-coach/references/my-common-bugs.md
grep -n '到期\|unresolved\|順延\|—' skills/leetcode-coach/references/my-common-bugs.md || echo "no ledger fields, no em dash: OK"
```

Expected: 第一行 `12`（8 列 checklist 加 4 列觀念），第二行 `2`，第三行 `no ledger fields, no em dash: OK`。

- [ ] **Step 3: lint**

Run: `./scripts/lint-all.sh`
Expected: `ALL PASS`（新增檔案不影響既有檢查）。

- [ ] **Step 4: Commit**

```bash
git add skills/leetcode-coach/references/my-common-bugs.md
git commit -m "feat(leetcode): harvest 32 registry rows into a static bug checklist"
```

---

### Task 3: 產出教學內容三檔

**Files:**
- Create: `skills/leetcode-coach/references/teaching-loop.md`
- Create: `skills/leetcode-coach/references/layer0-execution-model.md`
- Rewrite: `skills/leetcode-coach/references/curriculum.md`

**Interfaces:**
- Consumes: `references/my-common-bugs.md`（Task 2）在 teaching-loop 的步驟 7 被引用。
- Produces: 三個檔案路徑，Task 4 的 SKILL.md 讀哪些檔表格會引用它們。

**內容來源：** spec 第 4 節（教學迴圈）、5 節（圖解頁規格）、6.1 節（Layer 0）、6.2 節（Linked List）、10 節（天花板註解）。逐字搬進對應檔案，不重新發明。

- [ ] **Step 1: 寫 `teaching-loop.md`**

搬 spec 第 4 節與第 5 節全文。檔案結構：

```
# 教學迴圈

## 開場（固定 2 分鐘）        ← spec 4.1
## 龜模式                     ← spec 4.2，含 8 步 + 4 拷問的表格
## 兔模式                     ← spec 4.3
## Hard 規格                  ← spec 4.4
## 卡住協定                   ← spec 4.5
## 三層溫度計                 ← spec 4.6
## eli5 圖解頁規格            ← spec 第 5 節，含題目資料夾規則
## 反模式（禁止）
```

`## 反模式（禁止）` 這一節 spec 沒有，補上四條：

```markdown
## 反模式（禁止）

1. 直接貼完整最優解加逐行解釋。圖解頁的 code 區塊必須摺疊,由學員決定何時展開。
2. 記債。不要寫「3 天內白紙重寫」「這筆待清」。看答案是合法動作,處置在當場。
3. 因為某個檢查沒過就不讓學員往下走。檢查是溫度計,失敗的處置是當場補完後繼續。
4. 只問「懂了嗎」。要用 4 階拷問(說思路 / 預測下一步 / 填關鍵 code / 獨立寫完)。
```

- [ ] **Step 2: 寫 `layer0-execution-model.md`**

搬 spec 6.1 的 7 個概念。每個概念一個 `## ` 區塊，四個固定欄位：白話一句話、一張 ASCII 圖、
一個 30 秒能手算驗證的小例子、對應 `my-common-bugs.md` 的哪一列。概念 4 是這個格式的樣板，
其餘六個照抄結構：

````markdown
## 4. 縮排等於這行屬於誰

**白話:** 縮排不是排版,是在講「這行歸誰管」。歸迴圈管的每圈做一次,歸函式管的做一次。

```
def f(nums):          ← 歸函式管
    for n in nums:    ← 歸函式管,做一次
        print(n)      ← 歸迴圈管,每圈做一次
        return n      ← 歸迴圈管 → 第一圈就跑掉了
    return 0          ← 歸函式管,迴圈跑完才做
```

**30 秒手算:** `f([7, 8, 9])` 回傳什麼?答案是 `7`,因為 `return n` 在迴圈裡,
第一圈就結束了。把 `return n` 往左退一格,答案會變成 `0`。

**判準(自己講得出來才算會):** 問「這個動作該做幾次?」每圈一次就在迴圈內,
跑完做一次就在迴圈外。

**對應常犯錯:** checklist 第 1 列(`return` 縮排卡在迴圈裡,犯過 3 次,最貴的一種)。
````

檔案結尾寫明:「遞迴不在 Layer 0。走到 Tree 才教,現在教用不到。」

- [ ] **Step 3: 重寫 `curriculum.md`**

檔案開頭放 spec 第 10 節的天花板註解：

```markdown
<!-- ponytail: 此課程針對 Easy+Medium、DevOps coding 輪。
     觸發升級的條件(三選一發生就回來改):
       1. 目標公司換成算法題比重高的
       2. recruiter 明講 round 會有 Hard
       3. Medium 已經穩到無聊
     升級要動的只有兩處,不是重寫:
       1. 龜模式比例拉高(目前只有 pattern 首刷題走龜)
       2. 加 Hard 題池
-->
```

然後兩節：`## Layer 0`（指向 `layer0-execution-model.md`，說明它只跑一次）與 `## Linked List`（spec 6.2 的 11 列表格，含「順序需跟讀書會核對」的註記）。加一行說明 Linked List 之後的順序依讀書會進度決定，不預先排。

**注意：** 舊 `curriculum.md` 的 lint marker 要求（`warm-up` 字串、至少 3 個 `## ` 區塊）在 Task 4 之後不再適用，因為 standalone 分支會提早 exit。但 Task 3 執行時 marker 檢查仍生效，所以本 task 結束時 `curriculum.md` 需暫時滿足舊 marker，或把 Task 3 與 Task 4 合併成一次 commit。**採後者：Task 3 不單獨跑 lint，直接進 Task 4。**

- [ ] **Step 4: 確認三檔存在且非空**

```bash
wc -l skills/leetcode-coach/references/{teaching-loop,layer0-execution-model,curriculum}.md
grep -c '^## ' skills/leetcode-coach/references/teaching-loop.md
```

Expected: 三個檔都非零行；`teaching-loop.md` 有 8 個 `## ` 區塊。

- [ ] **Step 5: 不 commit，直接進 Task 4**

理由見 Step 3 的註記：`curriculum.md` 重寫後會掉出舊 lint marker，必須等 Task 4 的 standalone marker 進 SKILL.md 才會綠。兩個 task 合併成一次 commit。

---

### Task 4: 重寫 SKILL.md 與 evals

**Files:**
- Rewrite: `skills/leetcode-coach/SKILL.md`
- Rewrite: `skills/leetcode-coach/evals/evals.json`
- Rewrite: `skills/leetcode-coach/evals/files/progress-resume.md`
- Rewrite: `skills/leetcode-coach/evals/files/progress-new.md`

**Interfaces:**
- Consumes: Task 1 的 standalone 分支；Task 2、Task 3 建立的四個 reference 檔路徑。
- Produces: `SKILL.md` 內文第一行含 `<!-- engine: standalone -->`，lint 走 standalone 路徑。

- [ ] **Step 1: 寫新的 SKILL.md**

```bash
cat > skills/leetcode-coach/SKILL.md <<'EOF'
---
name: leetcode-coach
description: LeetCode 私人教練(Python、ELI5、圖解優先、跟著 NeetCode 順序)。Use PROACTIVELY when the user wants to practice LeetCode / NeetCode, coding-interview prep, algorithm patterns (linked list, arrays/hashing, two pointers, sliding window, stack, binary search, trees, BFS/DFS, heap, graphs, DP), mentions the 讀書會 daily problem, or says they freeze on a blank page and need step-by-step guidance with diagrams.
---

<!-- engine: standalone -->

# LeetCode Coach

這個 coach **不掛 `engine/`**。它有自己的教學迴圈,尺寸是為「上班空檔、一天 1 到 2 題」
設計的。重建的診斷與設計理由:`docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md`。

## 語言

繁體中文對話,技術名詞保留英文原文(pointer、node、sliding window、O(n))。
面試講得出口的才算學會,所以名詞不翻譯。

## Session 開場

1. 讀 `workspaces/leetcode/progress.md`,說出「今天做到哪」。
2. 檢查 `git status`。工作區乾淨且使用者授權才 pull;否則保留本地變更並回報 stale state 的風險。
3. 跑開場默寫(2 分鐘,見 teaching-loop)。

## 讀哪些檔

| 什麼時候 | 讀什麼 |
|---|---|
| 每次 session | `${CLAUDE_SKILL_DIR}/references/teaching-loop.md`、`workspaces/leetcode/progress.md` |
| 寫 code 之前 | `${CLAUDE_SKILL_DIR}/references/my-common-bugs.md` |
| 決定今天做什麼 | `${CLAUDE_SKILL_DIR}/references/curriculum.md` |
| 執行模型卡住 | `${CLAUDE_SKILL_DIR}/references/layer0-execution-model.md` |
| 需要模板 | `${CLAUDE_SKILL_DIR}/references/pattern-cheatsheet.md` |
| 查 Python 寫法 | `${CLAUDE_SKILL_DIR}/references/python-dsa-cheatsheet.md` |
| 講複雜度 | `${CLAUDE_SKILL_DIR}/references/complexity-cheatsheet.md` |
| 跑 harness | `${CLAUDE_SKILL_DIR}/references/lab-manager.md` |

不要一次全讀。

## 三條不能違反的規則

1. **不產生債務。** 不記 answer-debt、不排複習佇列、不開 gate。看答案與對照打 code 是合法動作。
2. **失敗不擋路。** 任何檢查失敗的處置都是當場補完後繼續,不是卡住重考。
3. **不直接貼完整解。** 先圖解、先讓學員講,code 摺疊起來由學員決定何時展開。

## Session 收尾

1. 更新 `workspaces/leetcode/progress.md`(今天做到哪、pattern 狀態表、做過的題)。
2. 圖解頁補寫「這次的釐清」區塊,redeploy 到同一個 artifact URL。
3. 重複出現的搞混升級到 `references/my-common-bugs.md`,並重新按次數排序。
4. 回報改了哪些檔。commit 與 push 只在使用者授權時做。
EOF
```

- [ ] **Step 2: 驗證 standalone 分支被觸發**

```bash
./scripts/lint-coach.sh leetcode-coach; echo "exit=$?"
```

Expected: 無輸出，`exit=0`。注意此時 `north-star.md` 等檔還在（Task 5 才刪），但 lint 已經不看它們了。

- [ ] **Step 3: 重寫 evals fixture `progress-resume.md`**

用 spec 第 8 節的新 schema，模擬「Linked List 做到 #21、圖解頁看完還沒寫」的續跑狀態：

```bash
cat > skills/leetcode-coach/evals/files/progress-resume.md <<'EOF'
# leetcode

- 今天做到:Linked List / #21 Merge Two Sorted Lists / 圖解頁看完了,還沒自己寫
- 模式:兔

## Pattern 狀態
| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 反轉 | ✅ | ✅ | ✅ #206 | 存下一個、改指向、兩個往前挪 |

## 做過
206 ✅ | 21 ⏳
EOF
```

- [ ] **Step 4: 重寫 evals fixture `progress-new.md`**

```bash
cat > skills/leetcode-coach/evals/files/progress-new.md <<'EOF'
# leetcode

- 今天做到:(還沒開始)
- 模式:-

## Pattern 狀態
(empty)

## 做過
(none)
EOF
```

- [ ] **Step 5: 重寫 evals.json**

舊的 8 個 case 有 6 個測已刪掉的機制（answer-debt、articulation bridge、weekly review、compressed sitting、P0-P7 warm-up、skeleton fluency drill）。全部換掉，保留 out-of-scope 那一個。

```bash
cat > skills/leetcode-coach/evals/evals.json <<'EOF'
{
  "skill_name": "leetcode-coach",
  "_note": "Behavioral evals for the standalone rebuild (2026-08-30). Each tests the FIRST coaching turn. The coach does NOT run on engine/; progress files follow the schema in docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md section 8. Replaces the 8 engine-era cases.",
  "evals": [
    {
      "id": 1,
      "name": "turtle-diagram-first",
      "prompt": "今天讀書會要開始 Linked List,從 Reverse Linked List 開始。",
      "expected_output": "Recognizes #206 as a pattern-first problem (turtle mode). Produces the eli5 HTML artifact FIRST and asks the student to read it before the dialogue, rather than lecturing straight into an explanation. The artifact's code, trace table, and mnemonic sections are collapsed behind <details>. Does not paste the full solution into chat.",
      "files": ["evals/files/progress-new.md"],
      "expectations": []
    },
    {
      "id": 2,
      "name": "rabbit-adapt-template",
      "prompt": "接下來是 #21 Merge Two Sorted Lists。",
      "expected_output": "Runs rabbit mode: asks the student to name the pattern, then shows the student's OWN template and asks which lines need to change. Does NOT ask the student to write it from a blank file, because the student has stated they cannot do that for a variant problem.",
      "files": ["evals/files/progress-resume.md"],
      "expectations": []
    },
    {
      "id": 3,
      "name": "stuck-three-stage-no-debt",
      "prompt": "我不會,直接跟你說。",
      "expected_output": "Advances one stage of the stuck protocol (point at the location, then narrow to the concept, then give the answer for the student to copy out). Does not time the student or tell them to try again. Copying the answer is treated as legitimate. Logs NO debt, NO due date, NO re-test appointment. Offers the immediate retype and a variant question instead.",
      "files": ["evals/files/progress-resume.md"],
      "expectations": []
    },
    {
      "id": 4,
      "name": "give-answer-then-thermometer",
      "prompt": "這題我看不懂,直接給我完整答案。",
      "expected_output": "Gives the answer rather than refusing or lecturing about self-generation. Then runs the thermometers: has the student clear the file and retype it immediately, and asks one variant question of the form 'what breaks if we remove this line'. Does not schedule a future cold re-do or create an answer-debt entry.",
      "files": ["evals/files/progress-resume.md"],
      "expectations": []
    },
    {
      "id": 5,
      "name": "hard-explain-not-write",
      "prompt": "讀書會排到 #23 Merge K Sorted Lists 了。",
      "expected_output": "Applies the Hard spec: the goal is to decompose it into already-learned components (heap plus the #21 merge), not to write it independently. Copying the code is the default action, not a fallback. Does NOT require a clear-and-retype, and does not require a green harness from a solo attempt.",
      "files": ["evals/files/progress-resume.md"],
      "expectations": []
    },
    {
      "id": 6,
      "name": "resume-reads-breakpoint",
      "prompt": "我回來了,繼續 leetcode。",
      "expected_output": "Reads progress.md and states where the student left off (Linked List, #21, artifact read but not yet written). Runs the 2-minute opening recall of the linked-list template before new content. Does not treat the student as new, does not surface any debt list or overdue queue, and does not propose a weekly review.",
      "files": ["evals/files/progress-resume.md"],
      "expectations": []
    },
    {
      "id": 7,
      "name": "out-of-scope-system-design",
      "prompt": "幫我設計一個 URL shortener 系統,我要準備 system design 面試。",
      "expected_output": "Recognizes this is system design, outside the LeetCode coaching scope. Redirects to the sd-coach skill rather than attempting the design, and offers to continue with coding practice instead. Does not start designing the URL shortener.",
      "files": [],
      "expectations": []
    }
  ]
}
EOF
```

- [ ] **Step 6: 驗證 evals.json 是合法 JSON 且滿足 lint 的斷言**

```bash
python3 -c "import json;d=json.load(open('skills/leetcode-coach/evals/evals.json'));assert d['evals'];[ (item['id'], item['prompt']) for item in d['evals'] ];print(f\"{len(d['evals'])} cases OK\")"
```

Expected: `7 cases OK`

- [ ] **Step 7: 全 lint**

Run: `./scripts/lint-all.sh`
Expected: `ALL PASS`，且 `leetcode-coach OK`。

- [ ] **Step 8: Commit（含 Task 3 的三個檔）**

```bash
git add skills/leetcode-coach/SKILL.md skills/leetcode-coach/evals/ skills/leetcode-coach/references/teaching-loop.md skills/leetcode-coach/references/layer0-execution-model.md skills/leetcode-coach/references/curriculum.md
git commit -m "feat(leetcode): rewrite coach as standalone with diagram-first teaching loop"
```

---

### Task 5: 刪掉 7 個 engine ceremony 檔

**Files:**
- Rewrite: `skills/leetcode-coach/references/lab-manager.md`（保留但要清掉 engine 引用，見 Step 1）
- Delete: `skills/leetcode-coach/references/north-star.md`
- Delete: `skills/leetcode-coach/references/teaching-elements.md`
- Delete: `skills/leetcode-coach/references/scorecard-dims.md`
- Delete: `skills/leetcode-coach/references/phase-gates.md`
- Delete: `skills/leetcode-coach/references/portfolio.md`
- Delete: `skills/leetcode-coach/references/problem-solving-framework.md`
- Delete: `skills/leetcode-coach/references/language.md`

**保留（不要刪）：** `ops-coding-bank.md`（`docs/plans/2026-08-11-module-roadmap.md:15` 仍引用，且 ops coding 驗收場排在 2026-09，是獨立模組）、`pattern-cheatsheet.md`、`python-dsa-cheatsheet.md`、`complexity-cheatsheet.md`、`lab-manager.md`、`my-common-bugs.md`、`teaching-loop.md`、`layer0-execution-model.md`、`curriculum.md`。

- [ ] **Step 1: 先重寫 `lab-manager.md`**

它在保留清單上,但目前有 4 處引用即將被刪的檔或 engine 機制:第 15 行的 `portfolio.md`、
第 17 行的 `teaching-elements.md`、第 36 行的 Examiner 與 phase gates、以及倒數第二段的
「the gates」。42 行整份重寫比逐行改乾淨:

```bash
cat > skills/leetcode-coach/references/lab-manager.md <<'EOF'
# Lab Manager

本地 pytest harness,不碰雲端資源,零成本。腳本是 `scripts/lab-lc.sh <problem-dir>`:
它跑該題資料夾的 pytest,每個 test 有 wall-clock 上限(`LAB_LC_TIMEOUT`,預設 5 秒,
走 pytest-timeout)。

## 環境

需要 Python 3,且 `pytest` 與 `pytest-timeout` 可 import。session 前確認:
`python3 -m pytest --version`。harness 會自檢:缺套件時 exit 3 並印安裝提示,
題目資料夾不存在時 exit 2。

## 用法

每題一個資料夾(規則見 `teaching-loop.md` 的 eli5 圖解頁規格一節),內含
`solution.py` 與 `test_<slug>.py`。測試檔由 coach 提供,`solution.py` 由學員產出。

```
scripts/lab-lc.sh workspaces/leetcode/<pattern>/<slug>/
```

## 複雜度絆線(關鍵設計)

每個測試檔都帶一個大 N 的 case(例 n = 10^5),標 `@pytest.mark.timeout(N)`。
O(n^2) 的暴力解會通過小 case 但在大 N 逾時而整組紅。這讓「到底是不是最佳解」
變成機器判定,不是 coach 的主觀判斷,也堵掉「和善的 coach 放行一個能跑但很慢的解」
這條路。

刻意要驗證暴力 baseline 時,用 `-k "not large_n"` 只跑小 case。絆線是給最佳解那一步用的。

## 驗收

一個題目算過,條件是 `lab-lc.sh` exit 0:功能測試全綠**且**大 N 計時測試綠。
客觀、機器檢查,不接受自我回報。

**注意:** exit 0 只證明 code 會跑。它不證明學員自己寫得出來。是不是自己寫的,
由 `teaching-loop.md` 的三層溫度計判定,記在 `progress.md` 的 pattern 狀態表。

## 收尾

session 後清掉題目資料夾的 `__pycache__/` 與 `.pytest_cache/`:

```
find workspaces/leetcode -name '__pycache__' -o -name '.pytest_cache' | xargs rm -rf
```

沒有雲端資源,所以沒有成本 teardown。
EOF
```

- [ ] **Step 2: 刪檔**

```bash
git rm skills/leetcode-coach/references/{north-star,teaching-elements,scorecard-dims,phase-gates,portfolio,problem-solving-framework,language}.md
```

- [ ] **Step 3: 確認留下來的是預期的 9 個**

```bash
ls skills/leetcode-coach/references/
```

Expected 恰好 9 個檔：`complexity-cheatsheet.md`、`curriculum.md`、`lab-manager.md`、`layer0-execution-model.md`、`my-common-bugs.md`、`ops-coding-bank.md`、`pattern-cheatsheet.md`、`python-dsa-cheatsheet.md`、`teaching-loop.md`。

- [ ] **Step 4: 確認沒有殘留的 engine 引用**

```bash
grep -rn 'engine/ENGINE.md\|engine/GOVERNANCE.md\|PROGRESS-SCHEMA\|Feynman Gate\|Examiner\|phase gate' skills/leetcode-coach/ || echo "no engine references: OK"
```

Expected: `no engine references: OK`

- [ ] **Step 5: 確認沒有檔案引用被刪掉的檔**

```bash
grep -rn 'north-star\|teaching-elements\|scorecard-dims\|phase-gates\|problem-solving-framework\|portfolio\.md\|language\.md' skills/leetcode-coach/ || echo "no dangling references: OK"
```

Expected: `no dangling references: OK`

- [ ] **Step 6: 全 lint**

Run: `./scripts/lint-all.sh`
Expected: `ALL PASS`

- [ ] **Step 7: Commit**

```bash
git add skills/leetcode-coach/references/lab-manager.md
git commit -m "chore(leetcode): drop seven engine ceremony reference files"
```

---

### Task 6: 重塑 `workspaces/leetcode/`

**Files:**
- Create: `workspaces/leetcode/archive/pre-rebuild/` 並移入 4 個檔
- Rewrite: `workspaces/leetcode/progress.md`
- Untouched: `one-liner-library.md`、`p1-*/`、`p2-*/`、`p3-*/`、`archive/pre-migration/`

**Interfaces:**
- Consumes: 舊 `progress.md`（Task 2 已把 Mistake Registry 收割完，此處才可以動它）。
- Produces: 新 `progress.md`，schema 見 spec 第 8 節。

- [ ] **Step 1: 確認 Task 2 已完成（先決條件）**

```bash
test -s skills/leetcode-coach/references/my-common-bugs.md && echo "harvest done, safe to archive" || echo "STOP: run Task 2 first"
```

Expected: `harvest done, safe to archive`。若印出 STOP，回頭做 Task 2，不要繼續。

- [ ] **Step 2: 歸檔舊 state**

```bash
mkdir -p workspaces/leetcode/archive/pre-rebuild
git mv workspaces/leetcode/{patterns,retention,session-log,skeleton-registry}.md workspaces/leetcode/archive/pre-rebuild/
cp workspaces/leetcode/progress.md workspaces/leetcode/archive/pre-rebuild/progress.md
git add workspaces/leetcode/archive/pre-rebuild/progress.md
```

舊 `progress.md` 用 `cp` 不用 `git mv`，因為下一步要就地重寫它，歸檔的是重建前的快照。

- [ ] **Step 3: 寫歸檔說明**

```bash
cat > workspaces/leetcode/archive/pre-rebuild/README.md <<'EOF'
# pre-rebuild snapshot (2026-08-30)

engine 時期(s1 到 s20,2026-07-10 遷入到 2026-08-03)的學員 state。唯讀,不再更新。

重建的診斷與設計:`docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md`。

- `progress.md` 重建前快照。Mistake Registry 的 32 列已收割進
  `skills/leetcode-coach/references/my-common-bugs.md`,不需要回頭讀這份。
- `retention.md` 舊留存階梯。新設計改成開場 2 分鐘默寫,不再排程。
- `skeleton-registry.md` 舊 skeleton 回憶排程。同上。
- `session-log.md` s1 到 s20 的 session 紀錄。
- `patterns.md` 跨 pattern playbook 的半成品。

題目資料夾(`p1-*/`、`p2-*/`、`p3-*/`)沒有搬遷,仍在原位可用。
EOF
git add workspaces/leetcode/archive/pre-rebuild/README.md
```

- [ ] **Step 4: 重寫 progress.md**

```bash
cat > workspaces/leetcode/progress.md <<'EOF'
<!-- Schema: docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md 第 8 節。
     這個檔只回答「現在在哪」,不回答「你欠什麼」。
     不加到期日欄位、不加未結狀態、不加順延計數。重建前的舊 state 在 archive/pre-rebuild/。 -->

# leetcode

- 今天做到:(重建完成,還沒開始第一場)
- 模式:-

## Pattern 狀態

| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|

## 做過

(none)

<!-- 起點:Layer 0 跑一次,然後 Linked List #206,順序見
     skills/leetcode-coach/references/curriculum.md。
     #206 沿用既有資料夾 p3-binsearch-linkedlist/reverse-linked-list/。 -->
EOF
```

- [ ] **Step 5: 驗證行數與欄位**

```bash
wc -l < workspaces/leetcode/progress.md
grep -n '到期\|unresolved\|順延\|spaced\|Examiner\|Mistake Registry' workspaces/leetcode/progress.md || echo "no ledger fields: OK"
ls workspaces/leetcode/
```

Expected: 行數小於 30；`no ledger fields: OK`；`ls` 只剩 `archive/`、`one-liner-library.md`、`p1-arrays-hashing/`、`p2-window-stack/`、`p3-binsearch-linkedlist/`、`progress.md`。

- [ ] **Step 6: 驗證題目 harness 沒被弄壞**

```bash
./scripts/lab-lc.sh workspaces/leetcode/p3-binsearch-linkedlist/reverse-linked-list/; echo "exit=$?"
```

Expected: `exit=0`（pytest 全綠）。若 exit 為 3，先裝 `pytest` 與 `pytest-timeout` 再重跑。

- [ ] **Step 7: 全 lint**

Run: `./scripts/lint-all.sh`
Expected: `ALL PASS`

- [ ] **Step 8: Commit**

```bash
git add workspaces/leetcode/
git commit -m "refactor(leetcode): reset learner state to the debt-free progress schema"
```

---

### Task 7: 更新 README 與 repo CLAUDE.md

**Files:**
- Modify: `README.md`（2 處，非 spec 寫的 4 處，見下方 Step 1 的更正）
- Modify: `CLAUDE.md`（repo 根，第 3 行描述）

**spec 的更正：** spec 第 7 節寫 README 有 4 處要改（L56、L76、L113、L119）。實際只有 2 處：L113 的遷移表是 pre-migration 的歷史事實，仍然成立；L119 的 symlink 清單說 leetcode-coach 已部署，也仍然成立。只改 L56 附近的檔案樹與 L76 附近的 workspace 說明。

- [ ] **Step 1: 更新 README 的 coach 檔案樹**

找到：

```
│   ├── leetcode-coach/
│   │   ├── SKILL.md
│   │   ├── references/                      # 8 hook files (incl. language) + cheatsheets
│   │   │                                    #   (problem-solving-framework, pattern,
│   │   │                                    #    complexity, python-dsa)
```

換成：

```
│   ├── leetcode-coach/                      # standalone: does NOT run on engine/
│   │   ├── SKILL.md
│   │   ├── references/                      # teaching-loop, curriculum, layer0-execution-model,
│   │   │                                    #   my-common-bugs, lab-manager + cheatsheets
│   │   │                                    #   (pattern, complexity, python-dsa)
│   │   └── evals/                           # behavioral evals + fixtures
```

- [ ] **Step 2: 更新 README 的 workspace 說明**

找到：

```
│   ├── leetcode/                            # progress.md (engine schema), one-liner-library,
│   │                                        #   skeleton-registry, patterns.md,
│   │                                        #   <phase>/<slug>/ problem folders
```

換成：

```
│   ├── leetcode/                            # progress.md (standalone schema), one-liner-library,
│   │                                        #   <pattern>/<slug>/ problem folders,
│   │                                        #   archive/pre-rebuild/ (engine-era state)
```

- [ ] **Step 3: 更新 repo 根的 CLAUDE.md 描述**

找到第 3 行：

```
Claude Code plugin: learning coaches sharing one teaching engine. Details in README.md.
```

換成：

```
Claude Code plugin: learning coaches. Details in README.md.

- k8s / sd / terraform / ca 共用 `engine/`。leetcode-coach 是 standalone(節奏不同,
  一天 1 到 2 題;設計理由見 `docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md`)。
```

同時把既有那條「Progress schema is engine-owned」改成只適用於掛 engine 的四個 coach：

```
- 掛 engine 的四個 coach:progress schema 是 engine-owned(engine/PROGRESS-SCHEMA.md),
  hook 照 engine/PLUGIN-INTERFACE.md。不要在 coach 裡 fork schema。
  leetcode-coach 不適用,它有自己的 schema。
```

- [ ] **Step 4: 驗證沒有殘留的過時敘述**

```bash
grep -n 'sharing one teaching engine' README.md CLAUDE.md || echo "tagline updated: OK"
grep -n 'leetcode.*engine schema\|problem-solving-framework\|8 hook files (incl. language) + cheatsheets' README.md || echo "README updated: OK"
```

Expected: 兩行都印 OK。

- [ ] **Step 5: 全 lint**

Run: `./scripts/lint-all.sh`
Expected: `ALL PASS`

- [ ] **Step 6: Commit**

```bash
git add README.md CLAUDE.md
git commit -m "docs: record leetcode-coach as standalone in README and repo instructions"
```

---

### Task 8: 全案驗收

**Files:** 無異動，只驗證。

跑 spec 第 11 節的 6 條驗收條件。

- [ ] **Step 1: 條件 1，lint 全綠**

Run: `./scripts/lint-all.sh`
Expected: 最後一行 `ALL PASS`，且五個 coach 都印 `OK`。

- [ ] **Step 2: 條件 2，刪除清單確實不存在**

```bash
for f in north-star teaching-elements scorecard-dims phase-gates portfolio problem-solving-framework language; do
  test -e "skills/leetcode-coach/references/$f.md" && echo "STILL EXISTS: $f.md"
done; echo "delete check done"
```

Expected: 只印 `delete check done`，沒有 `STILL EXISTS`。

- [ ] **Step 3: 條件 3，無 engine 引用**

```bash
grep -rF 'engine/ENGINE.md' skills/leetcode-coach/ || echo "no engine coupling: OK"
```

Expected: `no engine coupling: OK`

- [ ] **Step 4: 條件 4，progress.md 行數**

```bash
wc -l < workspaces/leetcode/progress.md
```

Expected: 小於 30。

- [ ] **Step 5: 條件 5，harness 仍可用**

```bash
./scripts/lab-lc.sh workspaces/leetcode/p3-binsearch-linkedlist/reverse-linked-list/; echo "exit=$?"
```

Expected: `exit=0`

- [ ] **Step 6: 條件 6，其他四個 coach 與 engine 零異動**

```bash
git diff --stat master -- skills/k8s-coach skills/sd-coach skills/terraform-coach skills/cloud-architect-coach engine/ workspaces/k8s workspaces/sd workspaces/ca
```

Expected: 無輸出（零異動）。

- [ ] **Step 7: 條件 7，題目資料夾零異動**

```bash
git diff --stat master -- workspaces/leetcode/p1-arrays-hashing workspaces/leetcode/p2-window-stack workspaces/leetcode/p3-binsearch-linkedlist
```

Expected: 無輸出。

- [ ] **Step 8: 回報結果**

把 Step 1 到 Step 7 的實際輸出貼給使用者。**沒有輸出就不宣稱通過。** 有任何一條沒過，停下來報告，不要自行修補後才說。

---

## 執行順序與相依

```
Task 0  開 branch
   ↓
Task 1  lint standalone 分支          （必須最先，其他 task 都依賴它）
   ↓
Task 2  收割 my-common-bugs           （必須早於 Task 6，資料源會被歸檔）
   ↓
Task 3  三個教學內容檔  ─┐
   ↓                     ├─ 合併成一次 commit（Task 3 單獨會掉出舊 lint marker）
Task 4  SKILL.md + evals ┘
   ↓
Task 5  刪 7 個檔                      （必須晚於 Task 4，marker 進去才不會紅）
   ↓
Task 6  workspaces 重塑
   ↓
Task 7  README + CLAUDE.md
   ↓
Task 8  全案驗收
```

## 本計畫刻意不做的事

- **不搬遷題目資料夾。** `p1-` / `p2-` / `p3-` 原地不動。新題走 `<pattern>/<slug>/`。路徑不一致由 `progress.md` 的「做過」行索引，不值得為一致性做 migration。
- **不動 `ops-coding-bank.md`。** 2026-09 的 ops coding 驗收場是獨立模組，不在本次範圍。
- **不寫任何一題的教材。** 第一題（Layer 0 加 #206）在第一場 session 現場產出，不預先寫死。
- **不改 `engine/`。** 其他四個 coach 的行為必須逐位元不變。
