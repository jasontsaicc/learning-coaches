# Notes Template

Notes are mainly a **Learn-mode** artifact (a new pattern worth a full write-up). In Drill, you don't write notes — you just log slips to the Mistake Registry and move on. Save notes into the student's practice directory as `notes/{pattern}-{problem}.md`, never inside the skill repo.

Language follows the `notes_lang` setting at the top of `progress.md`:
- `mixed` (default): Pattern 摘要 + 錯誤 in Chinese, How to Say It + code in English
- `english`: All English
- `chinese`: 70% Chinese / 30% English (only terms and code in English)

---

## Pattern 摘要
> [用自己的話，一句話總結這個 Pattern — 面試時能直接說出來]

## 解法 (Approach)
- **暴力法 (Brute Force):** [中文描述做法] — Time O(?), Space O(?)
- **最佳解 (Optimal):** [中文描述做法] — Time O(?), Space O(?)
- **關鍵洞察 (Key Insight):** [為什麼最佳解比較快？核心想法是什麼？]

## 🖼️ 圖解

> 把上課時 coach 用「你這題的真實數字」畫的圖貼進來。這是復習時最快喚回記憶的東西 — 看圖比看文字快。

```
[ 用 code block 保留 ASCII 圖的對齊。畫出 pointer / window / hashmap / 遞迴樹
  一步步怎麼變，並用 ↑ 指出每步的關鍵。範例：

  i=0  num=2  need 7  → 7 in {}?     no   → store {2:0}
  i=1  num=7  need 2  → 2 in {2:0}?  YES! → answer [0,1] ]
```

Rules:
- 用「你當下那題的實際數值」畫，不要抽象示意圖
- 至少畫出 2-3 步的變化（before→after 的移動），不是單一靜態快照

## 💻 My Code

> Copied from the workspace file. Keep both brute force and optimal (if different).

```python
# Brute Force
# (paste from workspace)

# Optimal (if different)
# (paste from workspace)
```

## ⚡ Edge Cases
- [列出這題需要注意的 edge cases]
- 例如：空陣列、單一元素、全部相同、負數、溢位...

Rules:
- 每題至少列出 3 個 edge cases
- 標記你在解題時漏掉的（⚠️）— 面試扣分重災區

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| (原本的錯誤理解) | (正確的理解) | (為什麼會有這個誤解) |

Rules:
- 記錄每一個錯誤答案、誤解、卡住的地方
- 「我以為」欄位必須寫出具體的錯誤理解，不能空白
- 如果真的沒有錯誤 → 寫 "本次無錯誤"（這應該很少見）

## 🎤 How to Say It in Interview

> Practice articulating today's topic as if you're in a real interview.

**Opening (30 sec):**
> "I'd approach this with [Pattern] because..."

**Optimization:**
> "The brute force is O(?), but we can do O(?) by..."

**Edge cases:**
> "I'd handle [edge case] by..."

Rules:
- Write in YOUR words, not textbook definitions
- Include at least one trade-off with reasoning, and one brute-vs-optimal complexity comparison

## Sync to progress.md

After writing notes, update the three blocks in `progress.md`:
1. Add any new 🔴 mistakes to the **Mistake Registry**
2. Update the pattern's row in **Pattern Fluency** (cold reps, last cold pass, whether it's at bar)
3. Overwrite the **Resume** block with where to pick up next time
