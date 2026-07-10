# Valid Palindrome 學習筆記

> LeetCode 125 | Easy | Two Pointers
> https://leetcode.com/problems/valid-palindrome/

---

## 這是什麼？（一句話解釋）

判斷一個字串「正著讀」和「反著讀」是不是一樣，忽略大小寫和標點符號。

---

## 用什麼比喻理解？

**走廊比喻**：想像一條走廊，請兩個人分別從頭尾出發，同時往中間走，邊走邊比對看到的東西。

- 如果中途發現不一樣 → 不是回文，提早結束
- 如果順利相遇 → 是回文！

這比「把整條走廊拍照存起來，再反轉比對」更省空間（不需要額外儲存）。

---

## Two Pointers 核心模式

```
左指標 ─────────────────→ ←───────────────── 右指標
        往中間移動，碰到就停
```

```python
left, right = 0, len(s) - 1
while left < right:
    # 做比較或處理
    left += 1
    right -= 1
```

---

## 踩過什麼雷？

### 1. `.lower` vs `.lower()`
```python
# ❌ 錯誤：比較的是「方法本身」
if s[left].lower != s[right].lower:

# ✅ 正確：呼叫方法得到結果
if s[left].lower() != s[right].lower():
```

### 2. 忘記 return True
```python
while left < right:
    ...
    if 不一樣:
        return False

# ❌ 忘記這行 → 會回傳 None
return True  # ✅ 要記得加！
```

### 3. 跳過無效字元時，只能動一邊
```python
# ❌ 錯誤：跳左邊的時候不小心動到右邊
while not s[left].isalnum():
    left += 1
    right -= 1  # 這行不該在這！

# ✅ 正確：各自處理
while left < right and not s[left].isalnum():
    left += 1
while left < right and not s[right].isalnum():
    right -= 1
```

---

## 最終正確 Code

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        # 跳過左邊無效字元
        while left < right and not s[left].isalnum():
            left += 1
        # 跳過右邊無效字元
        while left < right and not s[right].isalnum():
            right -= 1
        # 比較（忽略大小寫）
        if s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True
```

---

## 複雜度分析

| 複雜度 | 值 | 解釋 |
|--------|-----|------|
| 時間 | O(n) | 兩個指標各走一半，總共走 n 步 |
| 空間 | O(1) | 只用兩個變數，不需額外陣列 |

### 為什麼是 O(n)？
- `left` 從 0 往右走，最多走到 n-1
- `right` 從 n-1 往左走，最多走到 0
- 每個字元最多被看一次
- 兩指標不會回頭 → 總步數 ≤ 2n → O(n)

---

## 面試怎麼回答？

**面試官**：「請判斷一個字串是不是回文，忽略大小寫和非字母數字。」

**回答流程**：

1. **確認需求**：
   - 「所以 'A man, a plan, a canal: Panama' 應該回傳 True 對嗎？」
   - 「空字串或只有空格算 True 嗎？」

2. **說明思路**：
   - 「我會用 Two Pointers，從頭尾往中間走」
   - 「這樣只需要 O(1) 空間，不用額外存一份反轉的字串」

3. **處理 edge cases**：
   - 「遇到非字母數字就跳過」
   - 「比較時用 `.lower()` 忽略大小寫」

4. **說明複雜度**：
   - 「時間 O(n)，每個字元最多看一次」
   - 「空間 O(1)，只用兩個指標」

---

## 學到的 Python 技巧

| 技巧 | 用法 | 說明 |
|------|------|------|
| `isalnum()` | `"a".isalnum()` → True | 判斷是否為字母或數字 |
| `lower()` | `"A".lower()` → "a" | 轉成小寫 |
| 同時賦值 | `left, right = 0, n-1` | Python 可以一行設定多個變數 |

---

## 延伸思考

1. **如果要找「最長回文子字串」呢？**
   → LeetCode 5，需要不同技巧（中心擴展法）

2. **如果允許刪除一個字元呢？**
   → LeetCode 680 Valid Palindrome II

---

*完成日期：2026-01-19*
