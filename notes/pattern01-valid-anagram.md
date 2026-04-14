# Pattern 01 — Valid Anagram (LeetCode 242)

**日期：** 2026-03-17
**Pattern：** Arrays & Hashing — Frequency Counter
**難度：** Easy

---

## Pattern 一句話總結
> Frequency Counter 用 hash map 計算字元頻率 — 一個字串 +1、另一個 -1，全部歸零就代表一致。

## 解題思路

- **Brute Force（暴力解）：** 兩個字串排序後比較 — Time O(n log n), Space O(n)
- **Optimal（最佳解）：** 用 dict 做 Frequency Counter — Time O(n), Space O(1)（字元集固定）
- **關鍵洞察：** 排序浪費時間在「排順序」，但我們根本不在乎順序，只在乎每個字母出現幾次。用 hash map 一個 +1 一個 -1，一輪就搞定。

## 我的 Code

### Brute Force（排序法）

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)
```

### Optimal（Frequency Counter）

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        count = {}
        for i in s:
            if i in count:
                count[i] += 1
            else:
                count[i] = 1
        for j in t:
            if j in count:
                count[j] -= 1
            else:
                count[j] = -1
        for z in count.values():
            if z != 0:
                return False
        return True
```

## 🔴 我的錯誤和誤解

| 我原本以為 | 正確觀念 | 為什麼搞錯 |
|---|---|---|
| Python 布林值是 `false`/`true` | 要大寫 `False`/`True` | 跟 JavaScript 搞混了 |
| `sort(s)` 或 `s.sorted` 可以排序字串 | 要用 `sorted(s)` — 獨立的內建函式 | 搞混了 method 和 function 的差別 |
| `z = 0` 可以做比較 | `=` 是賦值，`==` 才是比較 | Python 基礎語法沒記熟 |
| 用 `z == 0` 找問題 | 應該用 `z != 0` — 非零才代表不匹配 | 邏輯反了：要找「哪裡有問題」而不是「哪裡沒問題」 |
| 排序是 O(log n) | 排序是 O(n log n) — n 個元素 × log n 輪 | 忘記每一輪還是要處理 n 個元素 |
| ASCII 字元集 → Space O(n) | ASCII 128 個字元是固定常數 → Space O(1) | 搞混「固定字元集 O(1)」vs「無限字元集如 Unicode → O(n)」 |

## 🎤 面試怎麼說（英文）

**開場 (30 sec):**
> "I'd approach this with a Frequency Counter because we need to check if two strings have the same character composition."

**Edge cases:**
> "First, I'd check if the lengths differ — if so, they can't be anagrams, return False immediately."

**最佳化說明:**
> "The brute force sorts both strings — O(n log n). With a Frequency Counter, we only need one pass — O(n) time, O(1) space since the charset is bounded."

**Trade-off（取捨）：**
> 排序寫起來簡單但比較慢；Frequency Counter 更快更省空間，但要理解 hash map 操作。

## 讀書會重點提示

1. **Frequency Counter 是面試萬用 Pattern** — anagram、permutation、字元比對都能用
2. **先 brute force 再 optimal** — 面試展示思路升級
3. **Space O(1) vs O(n) 的判斷關鍵** — 字元集是固定常數還是無上限
4. **進階變形** — Sliding Window + Frequency Counter 可以找子字串中的 anagram
