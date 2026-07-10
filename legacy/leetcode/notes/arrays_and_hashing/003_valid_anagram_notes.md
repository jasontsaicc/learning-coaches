# Valid Anagram 學習筆記

> LeetCode 242 | Easy | Arrays & Hashing

---

## 這是什麼？（一句話白話解釋）

判斷兩個字串是不是用「同樣的字母、同樣的數量」組成的，只是順序不同。

---

## 用什麼比喻理解？

### DevOps 比喻：比對兩份 Server 清單

老闆給你兩份 server 清單：

```
清單 A：["web-01", "web-02", "db-01", "web-01"]
清單 B：["db-01", "web-01", "web-01", "web-02"]
```

問：「這兩份清單是不是包含完全一樣的 server？（不管順序）」

**解法：** 數一數每種 server 各有幾台，兩邊一樣就是 anagram！

---

## 解題思路

### 和 Contains Duplicate 的差別

| 題目 | 需要知道什麼 | 資料結構 |
|------|-------------|---------|
| Contains Duplicate | 有沒有出現 | Set |
| Valid Anagram | 出現幾次 | Dict（key → 次數） |

### 核心思路：一個 Dict，加減抵消

1. **Early return**：長度不同 → 直接 False
2. **遍歷 s**：每個字母 +1
3. **遍歷 t**：每個字母 -1
4. **檢查**：全部 value 是否為 0

```
s = "anagram"  →  {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
t = "nagaram"  →  {'a': 0, 'n': 0, 'g': 0, 'r': 0, 'm': 0}
全部歸零 → True！
```

---

## 踩過什麼雷？

### 雷 1：`if` 語句少冒號
```python
# ❌ 錯誤
if len(s) != len(t)

# ✅ 正確
if len(s) != len(t):
```

### 雷 2：`return` 拼錯
```python
# ❌ 錯誤
reture False
retune False

# ✅ 正確
return False  # re + turn = 轉回去 = 回傳
```

### 雷 3：Dict key 不存在時直接 +=
```python
my_dict = {}

# ❌ 錯誤：KeyError
my_dict['a'] += 1

# ✅ 正確：用 .get() 給預設值
my_dict['a'] = my_dict.get('a', 0) + 1
```

### 雷 4：Copy-paste 忘記改變數名
```python
# ❌ 錯誤：第二個迴圈用了 i 而不是 j
for j in t:
    my_dict[j] = my_dict.get(i, 0) - 1  # 應該是 j！

# ✅ 正確
for j in t:
    my_dict[j] = my_dict.get(j, 0) - 1
```

### 雷 5：Python 縮排決定邏輯
```python
# ❌ 錯誤：return True 在迴圈裡面，第一次就結束
for v in my_dict.values():
    if v != 0:
        return False
    return True  # 縮排錯誤！

# ✅ 正確：return True 在迴圈外面，全部檢查完才結束
for v in my_dict.values():
    if v != 0:
        return False
return True  # 在 for 外面
```

---

## 最終正確 Code

```python
def isAnagram(s: str, t: str) -> bool:
    # Early return：長度不同不可能是 anagram
    if len(s) != len(t):
        return False

    # 用一個 dict 計數
    my_dict = {}

    # s 的字母 +1
    for i in s:
        my_dict[i] = my_dict.get(i, 0) + 1

    # t 的字母 -1
    for j in t:
        my_dict[j] = my_dict.get(j, 0) - 1

    # 檢查是否全部歸零
    for v in my_dict.values():
        if v != 0:
            return False
    return True
```

---

## 複雜度分析

| 複雜度 | 值 | 解釋 |
|--------|-----|------|
| 時間 | O(n) | 遍歷 s 一次 + 遍歷 t 一次 + 遍歷 dict values |
| 空間 | O(k) | k = 不同字母的數量（最多 26 個英文字母） |

---

## 面試怎麼回答？

### 問：請解釋你的思路

> 「我用一個 dict 來計數。先檢查長度，不一樣直接回傳 False。
> 然後遍歷第一個字串，每個字母出現就 +1。
> 再遍歷第二個字串，每個字母出現就 -1。
> 最後檢查 dict 裡所有的值是不是都歸零，是的話就是 anagram。」

### 問：為什麼先檢查長度？

> 「這是 early return 的技巧。長度不同的話，字母數量一定不同，不可能是 anagram。
> 提早結束可以省掉後面不必要的計算。」

### 問：有沒有其他解法？

> 「有！可以把兩個字串都排序，然後比較是否相等。
> 但排序是 O(n log n)，用 dict 計數是 O(n)，所以 dict 更快。」

### 問：空間複雜度是 O(n) 還是 O(1)？

> 「如果只考慮英文小寫字母，最多 26 個 key，所以是 O(1)。
> 如果是 Unicode 任意字元，那就是 O(n)。要看題目的限制條件。」

---

## 延伸練習

- [ ] Group Anagrams（Medium）：把一堆字串按 anagram 分組
- [ ] Find All Anagrams in a String（Medium）：在長字串中找所有 anagram 的起始位置

---

## 學習日期

2026-01-06
