# Valid Palindrome (LeetCode 125) — Two Pointers

> **分享會專用**｜時長預估 10-12 分鐘｜對象：同事 / 讀書會

---

## 🎤 分享會逐字稿（照著念也能用）

### 開場 (30 秒)

> 「今天分享 LeetCode 125 Valid Palindrome，Easy 題。這題看似簡單，但裡面有三個面試常考的重點：
> (1) Brute Force 到 Optimal 的思考過程
> (2) Two Pointers 這個 pattern 怎麼應用
> (3) 怎麼把 Space 從 O(n) 壓到 O(1)。」

---

### 1. 題目 (1.5 分鐘)

**題目：** 給一個字串，判斷是不是 palindrome（回文）。
忽略大小寫，忽略非字母數字字元（空白、標點）。

**範例：**

| Input | Output | 說明 |
|-------|--------|------|
| `"A man, a plan, a canal: Panama"` | True | 過濾後 `"amanaplanacanalpanama"` |
| `"race a car"` | False | 過濾後 `"raceacar"`，不對稱 |
| `" "` | True | 過濾後空字串 |
| `""` | True | 空字串視為 palindrome |
| `"0P"` | False | `0` vs `P` 不同類 |

**Constraints:**
- `1 ≤ len(s) ≤ 2 × 10⁵`
- ASCII printable characters

**Edge cases 要問面試官的：**
- 空字串算 palindrome 嗎？（LeetCode 慣例：True）
- 只有標點符號呢？（過濾後變空，回傳 True）
- 數字跟字母混合？（都算 alphanumeric）

---

### 2. Brute Force（最直覺的方法）(2.5 分鐘)

**思路：**
1. 把字串過濾 + 轉小寫，得到乾淨字串
2. 把乾淨字串反過來
3. 比較「正的」和「反的」是否相等

```python
class SolutionBrute:
    def isPalindrome(self, s: str) -> bool:
        filtered = ""
        for ch in s:
            if ch.isalnum():
                filtered += ch.lower()
        return filtered == filtered[::-1]
```

**複雜度：**
- Time: **O(n)**（掃一次 + 反轉一次 + 比較一次）
- Space: **O(n)**（需要存 `filtered` 字串）

**講話重點：** 這個解法時間已經是最優的 O(n)，但**額外用了 O(n) 空間**。面試官常問：「能不能 in-place？」這就是下一版要解決的問題。

---

### 3. Optimal: Two Pointers (4 分鐘)

**核心比喻：** Palindrome 就像**把紙條對折**，兩端的字元要對得上。

```
s = "a b c b a"
     ↑       ↑
    left   right     每輪兩邊往中間走一步
```

**思路：**
1. `left = 0`, `right = len(s) - 1`
2. 外層迴圈 `while left < right`：
   - 內層：如果 `s[left]` 不是字母數字 → `left += 1`（跳過）
   - 內層：如果 `s[right]` 不是字母數字 → `right -= 1`（跳過）
   - 比較 `s[left].lower()` 和 `s[right].lower()`
     - 不相等 → 直接 `return False`
     - 相等 → 兩邊都往中間走一步
3. 整個迴圈沒抓到不相等，`return True`

```python
class SolutionOptimal:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True
```

**複雜度：**
- Time: **O(n)**（指標總共移動 n 步）
- Space: **O(1)**（只用 2 個變數）

**講話重點：**
> 「兩個指標一個從左一個從右往中間走，總共移動 n 步，每步 O(1) 操作，所以整體 O(n)。空間上只用了 left 跟 right 兩個變數，壓到 O(1)。」

---

### 4. 複雜度對比 (1 分鐘)

| 方法 | Time | Space | 適用場景 |
|------|------|-------|----------|
| Brute Force | O(n) | O(n) | 可讀性優先，一般伺服器 |
| Two Pointers | O(n) | **O(1)** | 長字串、記憶體受限（嵌入式、Lambda cold start） |

**重點話術：**
> 「對短字串兩個差不多，但 LeetCode 給的 constraint 是 2 × 10⁵ 字元，再加上如果這個服務 QPS 很高，每個 request 省下的 n bytes 會影響整體記憶體。這就是為什麼工程師要會 Two Pointers。」

---

### 5. 陷阱 / Pitfalls (2 分鐘)

寫 Two Pointers 我踩過的 3 個坑：

| Bug | 長相 | 後果 |
|-----|------|------|
| **1. 忘記 `.lower()`** | `if s[l] != s[r]` | `"Panama"` 的 `P` vs `a` 不相等 → 錯判 |
| **2. 忘記移動指標** | 比較完沒 `l += 1` | 無限迴圈，終端炸 |
| **3. 忘記 `return True`** | 函式最後沒 return | Python 默認回 `None`，被當成 False |

**進階坑：**
- `.isalnum()` 在 Unicode 下**中文字也回 True**。如果題目允許 Unicode，程式不會壞，但行為可能不是期望的
- 外層 `while l < r` 用 `<` 而非 `<=`。因為當 `l == r` 時兩邊是同一個字元，比較沒意義
- 內層的 `while l < r and not s[l].isalnum()` 也要加 `l < r`，否則全是符號的字串會 IndexError

---

### 6. Follow-up 問題預習 (如果還有時間)

面試官可能追問：

**Q: 如果允許「至多刪除 k 個字元」讓它變 palindrome？(LeetCode 680, 1216)**
> A: 遇到不相等時不立刻 return False，而是嘗試跳過 `l` 或跳過 `r`，k -= 1，最多跳 k 次。

**Q: 如果輸入是 Unicode（中文、emoji）？**
> A: `.isalnum()` 對中文回 True，對 emoji 回 False。程式不會 crash，但定義要跟面試官對齊「中文算 palindrome 字元嗎？」

**Q: 如果要忽略大小寫 + 忽略變音符號（café vs CAFE）？**
> A: 先用 `unicodedata.normalize('NFKD', s)` 分解變音，再過濾。

---

### 7. 一句話收尾

> 「Valid Palindrome 是 Two Pointers 的入門題。Pattern 一句話總結：**左右兩個指標往中間走，對稱比較，遇標點跳過。** 時間 O(n)，空間 O(1)。明天見到類似『兩端對稱比較』的題目，第一個念頭就是 Two Pointers。」

---

## Pattern 摘要（One-Liner）

> **Two Pointers（收斂型）：左右兩個指標從兩端往中間走，邊走邊比較，O(n) 時間 O(1) 空間**

---

## 💻 My Code

```python
# Brute Force — O(n) time, O(n) space
class SolutionBrute:
    def isPalindrome(self, s: str) -> bool:
        filtered = ""
        for ch in s:
            if ch.isalnum():
                filtered += ch.lower()
        return filtered == filtered[::-1]


# Optimal: Two Pointers — O(n) time, O(1) space
class SolutionOptimal:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True
```

---

## ⚡ Edge Cases

- ✅ `""` (空字串) → True
- ✅ `" "` (只有空白) → True
- ✅ `"a"` (單字元) → True
- ✅ `"0P"` (數字 vs 字母) → False（⚠️ 容易以為會錯判，實際 `.lower()` 不會影響數字）
- ✅ `"!@#$%"` (全符號) → True（過濾後空）
- ⚠️ Unicode 中文：`.isalnum()` 回 True，行為跟 ASCII 不同

---

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| 比較兩字元直接 `s[l] != s[r]` | 要先 `.lower()` 正規化 | 忘記「大小寫忽略」要在比較前做 |
| 比較完 if 就結束 | 要 `l += 1; r -= 1` 移動指標 | Two Pointers 最常見的無限迴圈陷阱 |
| function 不寫 return 也會自動回 True | Python 默認回 `None` → 被當 False | Brute force 也犯過同樣錯誤 |
| `=` 和 `==` 都差不多 | `=` 改變世界、`==` 只問問題 | 第 4 次犯，這次終於鎖住 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd approach this with Two Pointers. The key insight: a palindrome reads the same forward and backward, so I can check it by comparing pairs from the outside in. Two pointers, one from each end, converge toward the middle."

**Optimization:**
> "The brute force filters the string and compares with its reverse — O(n) time but O(n) space. With Two Pointers, I eliminate the extra string. I skip non-alphanumeric chars in place and compare after lowercasing. Same O(n) time, but **O(1) space**."

**Edge cases:**
> "Empty string or whitespace-only — filtered version is empty, which counts as a palindrome. Unicode — `.isalnum()` returns True for Chinese characters, so the code won't crash, but I'd clarify the expected behavior with the interviewer."

**Follow-up readiness:**
> "If the problem allowed up to k deletions, I'd switch from a hard return-false to a branching approach: try skipping either the left or right char, decrement k, and recurse."

---

## 分享當下小抄（一張卡片）

```
開場：LC 125, Two Pointers 入門題
題目：忽略大小寫 + 非字母數字，判斷 palindrome

Brute: 過濾 + 反轉比較
       O(n) / O(n)

Optimal: Two Pointers 從兩端往中間走
       O(n) / O(1)

Pitfalls:
  1. 忘記 .lower()
  2. 忘記移動指標 → 無限迴圈
  3. 忘記 return True

Pattern 總結：
  左右指標往中間走，對稱比較，遇標點跳過
```
