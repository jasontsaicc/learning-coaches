# Notes Template

Use this template for every session's notes. Save as `notes/patternXX-problem-name.md`.

Language follows `notes_lang` setting in `progress.md` Student Info:
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
- 這張圖也是 Weekly Review 的快速喚回工具

## 💻 My Code

> Copied from workspace file. Keep both brute force and optimal (if different).

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
- 標記你在解題時漏掉的（⚠️）
- 這是面試扣分重災區，復習時優先看

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| (原本的錯誤理解) | (正確的理解) | (為什麼會有這個誤解) |

Rules:
- 記錄每一個錯誤答案、誤解、卡住的地方
- 「我以為」欄位必須寫出具體的錯誤理解，不能空白
- 如果真的沒有錯誤 → 寫 "本次無錯誤"（這應該很少見）
- 這個 section 是 Weekly Review 的優先複習目標

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
- Must include at least one trade-off with reasoning
- Must include at least one complexity comparison (brute vs optimal)
- This section feeds directly into interview muscle memory

## Sync to Progress File

After writing notes:
1. Add any new 🔴 Mistakes to the Mistake Registry in `progress.md`
2. Add this pattern's one-liner to the One-Liner Library in `progress.md`
3. Update Topic Mastery level based on session performance
4. Add to Problem Log with complexity info
