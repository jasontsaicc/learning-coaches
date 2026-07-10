# Group Anagrams 學習筆記

> LeetCode 49. Group Anagrams
> https://leetcode.com/problems/group-anagrams/

---

## 這是什麼？（一句話白話解釋）

把「字母組成一樣但順序不同」的字串分成同一組。

---

## 用什麼比喻理解？

**整理檔案到資料夾：**
- 你有一堆 log 檔案，老闆叫你把「本質上一樣的」分組
- 你用「排序後的檔名」當資料夾名稱
- `"eat"`, `"tea"`, `"ate"` 排序後都是 `"aet"` → 丟進同一個資料夾

**撲克牌比喻：**
- 三組牌：[♣A][♥E][♦T]、[♦T][♥E][♣A]、[♣A][♦T][♥E]
- 每組都按字母排好 → 都變成 [♣A][♥E][♦T]
- 用「排序後的樣子」當標籤，就能把同類的分在一起

---

## 踩過什麼雷？

### 1. `sorted()` 回傳的是 list，不是字串
```python
sorted("eat")  # ['a', 'e', 't'] ← 是 list！
# 要變成字串當 key，要用 join
"".join(sorted("eat"))  # "aet" ✅
```

### 2. Dict 的 key 不能用 list
```python
groups[['a', 'e', 't']] = ...  # ❌ TypeError: unhashable type: 'list'
groups["aet"] = ...             # ✅ 字串可以當 key
```

### 3. 直接賦值會覆蓋，要用 append
```python
# ❌ 錯誤：後面的會覆蓋前面的
groups["aet"] = "eat"
groups["aet"] = "tea"  # "eat" 不見了！

# ✅ 正確：用 list 收集
groups["aet"] = []
groups["aet"].append("eat")
groups["aet"].append("tea")  # ["eat", "tea"]
```

### 4. append 要放在 if 外面
```python
# ❌ 錯誤：只有第一個會進去
if key not in groups:
    groups[key] = []
    groups[key].append(word)  # 只有 key 不存在時才 append

# ✅ 正確：每個字都要 append
if key not in groups:
    groups[key] = []
groups[key].append(word)      # 這行永遠都要執行！
```

---

## 最終正確 Code

```python
def groupAnagrams(strs: List[str]) -> List[List[str]]:
    groups = {}
    for word in strs:
        sorted_word = sorted(word)
        str_word = "".join(sorted_word)

        if str_word not in groups:
            groups[str_word] = []
        groups[str_word].append(word)

    return list(groups.values())
```

---

## 複雜度分析

### 時間複雜度：O(n × k log k)
- `n` = 字串數量
- `k` = 最長字串的長度
- 遍歷 n 個字串，每個要排序 k 個字母
- 排序 k 個字母 = O(k log k)

### 空間複雜度：O(n × k)
- 存所有字串到 dict 裡
- 最多 n 個字串，每個最長 k 個字母

---

## 面試怎麼回答？

### Q: 請解釋你的思路

> 「我注意到 anagram 的特徵是『字母相同但順序不同』。
> 所以我想到用**排序後的字串當 key**，這樣所有 anagram 都會有相同的 key。
> 用 dict 收集，最後回傳所有 values 就是分組結果。」

### Q: 時間複雜度？

> 「O(n × k log k)，n 是字串數量，k 是最長字串長度。
> 因為遍歷 n 個字串，每個要排序，排序 k 個字母是 O(k log k)。」

### Q: 有沒有其他解法？

> 「可以用 **counting** 的方式當 key，不用排序。
> 把每個字母出現次數變成 tuple，例如 `"eat"` → `(1,0,0,0,1,...,1,0,...)`
> 這樣時間複雜度可以變成 O(n × k)，省掉 log k。
> 但實務上字串通常不長，排序的 k log k 影響不大。」

---

## 學到的語法

| 語法 | 用途 | 範例 |
|------|------|------|
| `sorted(str)` | 排序字串，回傳 list | `sorted("eat")` → `['a','e','t']` |
| `"".join(list)` | 把 list 黏成字串 | `"".join(['a','e','t'])` → `"aet"` |
| `key not in dict` | 檢查 key 是否存在 | `if "aet" not in groups` |
| `dict[key] = []` | 建立空 list | `groups["aet"] = []` |
| `list.append()` | 加到 list 最後 | `groups["aet"].append("eat")` |
| `dict.values()` | 取得所有 values | `groups.values()` |

---

## 學習日期
2026-01-07
