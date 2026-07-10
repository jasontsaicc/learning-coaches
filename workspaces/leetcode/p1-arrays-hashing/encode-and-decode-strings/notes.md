# Encode and Decode Strings (LeetCode 271)

- **Pattern:** Arrays & Hashing — Delimiter Design (Length-Prefix)
- **Difficulty:** Medium (NeetCode 150 Premium)
- **Date:** 2026-04-07 (updated 2026-04-08 study group review)
- **Session:** 3 (jump-to, study group prep) + S4 review

---

## Pattern 摘要
> 把 string list 編碼成一個 string：每個字串前面加「長度#」，decode 時讀數字就知道要往後數幾個字元，不管字串裡有什麼特殊字元都不會搞混。

## ⚠️ 這題的 Encode/Decode ≠ Base64

| | Base64 / Base62 | 這題的 Encode/Decode |
|---|---|---|
| **目的** | 把 binary data 變成安全的文字 | 把 **list** 變成 **一個 string**，再還原 |
| **類比** | 翻譯成另一種語言 | 把多個東西**打包**成一箱，再拆箱 |
| **更精確的說法** | encoding（編碼） | **serialization / deserialization**（序列化） |

> 重點：Base64 是內容被轉換，這題是內容沒變、只加了標記。

## 解法 (Approach)
- **為什麼不能用分隔符（如逗號）：** 字串本身可能包含該分隔符，導致 decode 時切錯
- **為什麼不用跳脫字元（如 \）：** 可行但很複雜，`\` 本身也需要 escape（`\\`），越套越複雜容易出 bug
- **最佳解 (Length-Prefix)：** 每個字串前面加 `長度#字串`，decode 時先讀數字和 `#`，再往後數那麼多字元 — Time O(n), Space O(n)
- **關鍵洞察 (Key Insight)：** 靠「長度」數字元，不靠分隔符切字串 → **用數的，不用找的** → 字串內容不會干擾 decode

## 💻 My Code

```python
from typing import List

class Solution:
    def encode(self, strs: List[str]) -> str:
        result = ""
        for s in strs:
            result += str(len(s)) + "#" + s
        return result

    def decode(self, s: str) -> List[str]:
        result = []
        i = 0
        while i < len(s):
            j = s.find("#", i)
            length = int(s[i:j])
            result.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return result
```

## ⚡ Edge Cases

| Input | Encode | Decode 怎麼走 | 為什麼安全 |
|-------|--------|---------------|------------|
| `[""]` 空字串 | `"0#"` | `length=0` → `s[2:2]=""` → 取到空字串 | `slice` 起終點一樣 → 空字串 |
| `[]` 空 list | `""` | `i=0`, `len(s)=0` → 迴圈不跑 → `[]` | 直接 return |
| `["h#i"]` 有 `#` | `"3#h#i"` | `length=3` → 往後數 3 個字元 → `"h#i"` | 用數的不用找的 |
| `["hello world!!"]` 多位數長度 | `"12#hello world!!"` | `s.find("#")` 找到 `#` 位置 → `s[0:2]="12"` | slice 不限一位數 |

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| 用 `len(strs)` 取長度 | 要用 `len(s)` 取每個字串的長度 | `len(strs)` 是 list 有幾個元素，`len(s)` 才是字串有幾個字元 |
| length-prefix 不怕 `#` 是因為「只看第一個 `#`」 | 是因為靠長度數字元，根本不需要找 `#` 來切 | decode 不是用 `#` 分隔字串，而是用數字決定讀幾個字元 |
| 以為 encode/decode 跟 Base64 一樣 | 這題是 serialization（打包/拆箱），不是 encoding（編碼轉換） | Base64 會轉換內容，這題內容不變只加長度標記 |

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd use length-prefix encoding. The key insight is that we can't use a simple delimiter like a comma because the strings themselves might contain that character. Instead, we prefix each string with its length followed by a separator like '#'."

**Core logic:**
> "For encoding, I prepend each string with its length and a '#'. For decoding, I read the number before '#' to know exactly how many characters to consume next. This makes the encoding safe regardless of what characters the strings contain."

**Edge cases:**
> "This handles empty strings — they get encoded as '0#'. And if a string contains '#', it doesn't matter because we're counting characters, not looking for delimiters."

## Study Group 分享用重點

| 順序 | 內容 | 重點 |
|------|------|------|
| 1 | 題目是什麼 | list ↔ string 的 **serialization**，不是 Base64 |
| 2 | 為什麼分隔符不行 | 用 `["h#i"]` 舉例，分隔符會跟內容搞混 |
| 3 | Length-Prefix 怎麼做 | `長度#內容`，像包裹外面寫數量 |
| 4 | 帶 `["hi","bye"]` 走 encode | `"2#hi"` + `"3#bye"` → `"2#hi3#bye"` |
| 5 | 帶同樣例子走 decode | `j=find("#")` → `length=int()` → `slice` 取字元 → 更新 `i` |
| 6 | Edge case | `[""]`→`"0#"`, `["h#i"]`→`"3#h#i"`, 多位數長度 |

### Decode Walkthrough（白板用）

```
s = "2#hi3#bye"
     0123456789

第一圈: i=0 → j=1 → length=2 → s[2:4]="hi"  → i=4
第二圈: i=4 → j=5 → length=3 → s[6:9]="bye" → i=9
i=9, 9<9 False → 跳出 → return ["hi","bye"]
```

## 重要語法筆記

| 語法 | 用法 | 說明 |
|------|------|------|
| `str(len(s))` | 數字轉字串 | `len()` 回傳 int，要用 `str()` 串接 |
| `s.find("#", i)` | 從 index i 開始找 `#` | 回傳 `#` 的 index |
| `int(s[i:j])` | 字串切片轉數字 | 取 i 到 j-1 的子字串，轉成 int |
| `s[j+1 : j+1+length]` | 從 `#` 後面取 length 個字元 | Python slice：`[start : end]` 不含 end |
