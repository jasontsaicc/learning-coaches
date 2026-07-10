# 008. Intersection of Two Arrays - 學習筆記

> 完成日期：2026-01-13

---

## 這是什麼？（一句話白話解釋）

找出兩個 list 裡面「都有」的數字（交集），結果不重複。

---

## 用什麼比喻理解？

**生活比喻：**
- 你的最愛電影清單 vs 朋友的最愛電影清單
- 交集 = 你們「都喜歡」的電影

**DevOps 比喻：**
- Server A 跑的服務：`["nginx", "redis", "mysql"]`
- Server B 跑的服務：`["nginx", "postgres", "redis"]`
- 交集 = `["nginx", "redis"]` ← 兩台都有跑的服務

---

## 核心概念

### Set 的三種運算
| 符號 | 名稱 | 意思 |
|------|------|------|
| `&` | intersection (交集) | 兩邊都有 |
| `\|` | union (聯集) | 全部合起來 |
| `-` | difference (差集) | A 有但 B 沒有 |

### 為什麼用 Set？
| 操作 | List | Set |
|------|------|-----|
| `item in x` | O(n) 慢！ | O(1) 快！ |

---

## 踩過什麼雷？

1. **沒踩雷！** 這題很直覺，學完 Single Number 後 Set 已經很熟了

---

## 最終正確 Code

```python
def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    set_nums1 = set(nums1)
    set_nums2 = set(nums2)
    result = set_nums1 & set_nums2
    return list(result)
```

**One-liner version:**
```python
def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    return list(set(nums1) & set(nums2))
```

---

## 複雜度分析

| | 複雜度 | 說明 |
|---|--------|------|
| Time | O(n + m) | 建 set O(n) + O(m)，交集 O(min(n,m)) |
| Space | O(n + m) | 存兩個 set |

---

## 面試怎麼回答？

**Q: How would you find the intersection of two arrays?**

> "I would convert both arrays to sets to remove duplicates, then use the intersection operator `&` to find common elements, and finally convert the result back to a list.
>
> This approach is O(n + m) in time because set operations use hash tables. If I used nested loops with lists, it would be O(n × m) which is much slower."

**Q: Why use Set instead of List?**

> "Because `item in set` is O(1) using hash table lookup, but `item in list` is O(n) since it checks every element. This makes a big difference when dealing with large datasets."

---

## 相關題目

| 題目 | 關聯 |
|------|------|
| Single Number | 也用 Set 去重 |
| Contains Duplicate | 也用 Set 檢查重複 |
| Intersection of Two Arrays II | 進階版，保留重複次數 |

---

## 學到的英文

| 英文 | 中文 | 例句 |
|------|------|------|
| intersection | 交集 | Find the intersection of two sets |
| union | 聯集 | The union includes all elements |
| remove duplicates | 去除重複 | Set removes duplicates automatically |
| common items | 共同的項目 | Find common items between lists |
