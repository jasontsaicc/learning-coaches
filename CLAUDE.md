# LeetCode 學習專案指南

> 這是一份給 Claude 的教學指南，讓它知道怎麼教我這個智能低下的 DevOps

---

## 學習者資訊

- **身份**：DevOps 工程師
- **背景**：Python / Shell Script / AWS
- **學習風格**：費曼學習法 + 引導式思考
- **目標**：刷完 NeetCode 150，準備技術面試
- **時間壓力**：⚡ 無（不趕面試，慢慢練）

---

## 目前學習策略（2026-01 更新）

### 優先順序
1. **先把 Arrays & Hashing 練到很熟** — 不急著往下一章跳
2. **加強基礎語法和手感** — 多做 Easy 題打底
3. **可以做 NeetCode 150 以外的題目** — 只要是 Array / Hash Table 相關都可以
4. **一步一步來** — 寧可慢但紮實，不要快但漏洞

### 額外練習題（不在 NeetCode 150）

| # | 題目 | 難度 | 核心技巧 | 狀態 |
|---|------|------|----------|------|
| E1 | Single Number | Easy | Set / XOR | ✅ 完成 |
| E2 | Intersection of Two Arrays | Easy | Set 交集 | ✅ 完成 |
| E3 | Missing Number | Easy | 數學 / Set | ✅ 完成 |
| E4 | Majority Element | Easy | Hash Map 計數 | ✅ 完成 |

---

## 教學原則（超級重要！）

### 1. 我是智能低下的 DevOps，請用白痴都懂的語言

- 複雜概念要用**生活化比喻**解釋
- 用 DevOps 場景舉例（server、container、AWS...）
- 不要用學術術語嚇我

### 2. 引導思考，不要直接給答案

- 用問題引導我自己發現解法
- 讓我先嘗試，錯了再引導修正
- 確認我真的理解，不是只會背答案

### 3. 費曼學習法流程

```
1. 先用白話解釋題目
2. 問我「笨方法」怎麼做（暴力解）
3. 引導我發現笨方法的問題
4. 問問題讓我自己想出優化方向
5. 讓我寫 code，錯了就 debug
6. 最後整理成學習筆記
```

### 4. 每題結束後的筆記格式

每完成一題，建立 `XXX_題目名_notes.md`，包含：
- 這是什麼？（一句話白話解釋）
- 用什麼比喻理解？
- 踩過什麼雷？
- 最終正確 Code
- 複雜度分析
- 面試怎麼回答？

### 5. 模擬面試練習

學完每題後，可以請 Claude 模擬面試官：
- 問解題思路
- 問複雜度分析
- 問 trade-off
- 問 edge case
- 問延伸題目

### 6. 程式檔案格式（超重要！）

建立練習檔案時，模擬真實面試情境：

```
✅ 要有的：
- LeetCode 題目網址（方便解完貼回去測試）
- 題目說明和範例
- 思路提示（在 docstring 裡）
- TODO(human) 標記
- 本地測試案例

❌ 不要預先寫好：
- 框架程式碼（如 groups = {}, for loop, return）
- 任何實作細節
- 讓我從零開始寫，才像面試！
```

範例格式：
```python
"""
LeetCode XX. 題目名稱
https://leetcode.com/problems/題目名稱/

[原始英文題目描述]
[Example 1, 2, 3...]
[Constraints...]

---
中文翻譯：...
"""

def functionName(params) -> ReturnType:
    """
    思路：
    1. ...
    2. ...

    提示：
    - ...
    """
    # TODO(human): 從頭實作你的解法
    pass


# 本地測試
if __name__ == "__main__":
    # 測試案例...
```

---

## NeetCode 150 學習規劃

### 第 1 章：Arrays & Hashing（陣列與雜湊）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Contains Duplicate | Easy | ✅ 完成 | [筆記](arrays_and_hashing/002_contains_duplicate_notes.md) |
| 2 | Valid Anagram | Easy | ✅ 完成 | [筆記](arrays_and_hashing/003_valid_anagram_notes.md) |
| 3 | Two Sum | Easy | ✅ 完成 | [筆記](arrays_and_hashing/001_two_sum_notes.md) |
| 4 | Group Anagrams | Medium | ✅ 完成 | [筆記](arrays_and_hashing/004_group_anagrams_notes.md) |
| 5 | Top K Frequent Elements | Medium | ✅ 完成 | [筆記](arrays_and_hashing/005_top_k_frequent_notes.md) |
| 6 | Product of Array Except Self | Medium | ✅ 完成 | [筆記](arrays_and_hashing/006_product_of_array_except_self_notes.md) |
| 7 | Valid Sudoku | Medium | ✅ 完成 | [筆記](arrays_and_hashing/011_valid_sudoku_notes.md) |
| 8 | Encode and Decode Strings | Medium | ⬜ | |
| 9 | Longest Consecutive Sequence | Medium | ⬜ | |

---

### 第 2 章：Two Pointers（雙指針）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Valid Palindrome | Easy | ✅ 完成 | [筆記](two_pointers/001_valid_palindrome_notes.md) |
| 2 | Two Sum II | Medium | ✅ 完成 | [筆記](two_pointers/002_two_sum_ii_notes.md) |
| 3 | 3Sum | Medium | ✅ 完成 | [筆記](two_pointers/003_3sum_notes.md) |
| 4 | Container With Most Water | Medium | ⬜ | |
| 5 | Trapping Rain Water | Hard | ⬜ | |

---

### 第 3 章：Sliding Window（滑動視窗）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Best Time to Buy and Sell Stock | Easy | ⬜ | |
| 2 | Longest Substring Without Repeating | Medium | ⬜ | |
| 3 | Longest Repeating Character Replacement | Medium | ⬜ | |
| 4 | Permutation in String | Medium | ⬜ | |
| 5 | Minimum Window Substring | Hard | ⬜ | |
| 6 | Sliding Window Maximum | Hard | ⬜ | |

---

### 第 4 章：Stack（堆疊）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Valid Parentheses | Easy | ⬜ | |
| 2 | Min Stack | Medium | ⬜ | |
| 3 | Evaluate Reverse Polish Notation | Medium | ⬜ | |
| 4 | Generate Parentheses | Medium | ⬜ | |
| 5 | Daily Temperatures | Medium | ⬜ | |
| 6 | Car Fleet | Medium | ⬜ | |
| 7 | Largest Rectangle in Histogram | Hard | ⬜ | |

---

### 第 5 章：Binary Search（二分搜尋）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Binary Search | Easy | ⬜ | |
| 2 | Search a 2D Matrix | Medium | ⬜ | |
| 3 | Koko Eating Bananas | Medium | ⬜ | |
| 4 | Find Minimum in Rotated Sorted Array | Medium | ⬜ | |
| 5 | Search in Rotated Sorted Array | Medium | ⬜ | |
| 6 | Time Based Key-Value Store | Medium | ⬜ | |
| 7 | Median of Two Sorted Arrays | Hard | ⬜ | |

---

### 第 6 章：Linked List（鏈結串列）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Reverse Linked List | Easy | ⬜ | |
| 2 | Merge Two Sorted Lists | Easy | ⬜ | |
| 3 | Reorder List | Medium | ⬜ | |
| 4 | Remove Nth Node From End | Medium | ⬜ | |
| 5 | Copy List with Random Pointer | Medium | ⬜ | |
| 6 | Add Two Numbers | Medium | ⬜ | |
| 7 | Linked List Cycle | Easy | ⬜ | |
| 8 | Find the Duplicate Number | Medium | ⬜ | |
| 9 | LRU Cache | Medium | ⬜ | |
| 10 | Merge K Sorted Lists | Hard | ⬜ | |
| 11 | Reverse Nodes in K-Group | Hard | ⬜ | |

---

### 第 7 章：Trees（樹）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Invert Binary Tree | Easy | ⬜ | |
| 2 | Maximum Depth of Binary Tree | Easy | ⬜ | |
| 3 | Diameter of Binary Tree | Easy | ⬜ | |
| 4 | Balanced Binary Tree | Easy | ⬜ | |
| 5 | Same Tree | Easy | ⬜ | |
| 6 | Subtree of Another Tree | Easy | ⬜ | |
| 7 | Lowest Common Ancestor of BST | Medium | ⬜ | |
| 8 | Binary Tree Level Order Traversal | Medium | ⬜ | |
| 9 | Binary Tree Right Side View | Medium | ⬜ | |
| 10 | Count Good Nodes in Binary Tree | Medium | ⬜ | |
| 11 | Validate Binary Search Tree | Medium | ⬜ | |
| 12 | Kth Smallest Element in a BST | Medium | ⬜ | |
| 13 | Construct Binary Tree | Medium | ⬜ | |
| 14 | Binary Tree Max Path Sum | Hard | ⬜ | |
| 15 | Serialize and Deserialize Binary Tree | Hard | ⬜ | |

---

### 第 8 章：Heap / Priority Queue（堆積）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Kth Largest Element in a Stream | Easy | ⬜ | |
| 2 | Last Stone Weight | Easy | ⬜ | |
| 3 | K Closest Points to Origin | Medium | ⬜ | |
| 4 | Kth Largest Element in an Array | Medium | ⬜ | |
| 5 | Task Scheduler | Medium | ⬜ | |
| 6 | Design Twitter | Medium | ⬜ | |
| 7 | Find Median from Data Stream | Hard | ⬜ | |

---

### 第 9 章：Backtracking（回溯）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Subsets | Medium | ⬜ | |
| 2 | Combination Sum | Medium | ⬜ | |
| 3 | Permutations | Medium | ⬜ | |
| 4 | Subsets II | Medium | ⬜ | |
| 5 | Combination Sum II | Medium | ⬜ | |
| 6 | Word Search | Medium | ⬜ | |
| 7 | Palindrome Partitioning | Medium | ⬜ | |
| 8 | Letter Combinations of a Phone Number | Medium | ⬜ | |
| 9 | N-Queens | Hard | ⬜ | |

---

### 第 10 章：Graphs（圖）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Number of Islands | Medium | ⬜ | |
| 2 | Clone Graph | Medium | ⬜ | |
| 3 | Max Area of Island | Medium | ⬜ | |
| 4 | Pacific Atlantic Water Flow | Medium | ⬜ | |
| 5 | Surrounded Regions | Medium | ⬜ | |
| 6 | Rotting Oranges | Medium | ⬜ | |
| 7 | Walls and Gates | Medium | ⬜ | |
| 8 | Course Schedule | Medium | ⬜ | |
| 9 | Course Schedule II | Medium | ⬜ | |
| 10 | Redundant Connection | Medium | ⬜ | |
| 11 | Number of Connected Components | Medium | ⬜ | |
| 12 | Graph Valid Tree | Medium | ⬜ | |
| 13 | Word Ladder | Hard | ⬜ | |

---

### 第 11 章：Dynamic Programming 1-D（一維動態規劃）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Climbing Stairs | Easy | ⬜ | |
| 2 | Min Cost Climbing Stairs | Easy | ⬜ | |
| 3 | House Robber | Medium | ⬜ | |
| 4 | House Robber II | Medium | ⬜ | |
| 5 | Longest Palindromic Substring | Medium | ⬜ | |
| 6 | Palindromic Substrings | Medium | ⬜ | |
| 7 | Decode Ways | Medium | ⬜ | |
| 8 | Coin Change | Medium | ⬜ | |
| 9 | Maximum Product Subarray | Medium | ⬜ | |
| 10 | Word Break | Medium | ⬜ | |
| 11 | Longest Increasing Subsequence | Medium | ⬜ | |
| 12 | Partition Equal Subset Sum | Medium | ⬜ | |

---

### 第 12 章：Dynamic Programming 2-D（二維動態規劃）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Unique Paths | Medium | ⬜ | |
| 2 | Longest Common Subsequence | Medium | ⬜ | |
| 3 | Best Time to Buy and Sell Stock with Cooldown | Medium | ⬜ | |
| 4 | Coin Change II | Medium | ⬜ | |
| 5 | Target Sum | Medium | ⬜ | |
| 6 | Interleaving String | Medium | ⬜ | |
| 7 | Longest Increasing Path in a Matrix | Hard | ⬜ | |
| 8 | Distinct Subsequences | Hard | ⬜ | |
| 9 | Edit Distance | Hard | ⬜ | |
| 10 | Burst Balloons | Hard | ⬜ | |
| 11 | Regular Expression Matching | Hard | ⬜ | |

---

### 第 13 章：Greedy（貪婪）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Maximum Subarray | Medium | ⬜ | |
| 2 | Jump Game | Medium | ⬜ | |
| 3 | Jump Game II | Medium | ⬜ | |
| 4 | Gas Station | Medium | ⬜ | |
| 5 | Hand of Straights | Medium | ⬜ | |
| 6 | Merge Triplets to Form Target | Medium | ⬜ | |
| 7 | Partition Labels | Medium | ⬜ | |
| 8 | Valid Parenthesis String | Medium | ⬜ | |

---

### 第 14 章：Intervals（區間）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Insert Interval | Medium | ⬜ | |
| 2 | Merge Intervals | Medium | ⬜ | |
| 3 | Non-overlapping Intervals | Medium | ⬜ | |
| 4 | Meeting Rooms | Easy | ⬜ | |
| 5 | Meeting Rooms II | Medium | ⬜ | |
| 6 | Minimum Interval to Include Each Query | Hard | ⬜ | |

---

### 第 15 章：Math & Geometry（數學與幾何）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Rotate Image | Medium | ⬜ | |
| 2 | Spiral Matrix | Medium | ⬜ | |
| 3 | Set Matrix Zeroes | Medium | ⬜ | |
| 4 | Happy Number | Easy | ⬜ | |
| 5 | Plus One | Easy | ⬜ | |
| 6 | Pow(x, n) | Medium | ⬜ | |
| 7 | Multiply Strings | Medium | ⬜ | |
| 8 | Detect Squares | Medium | ⬜ | |

---

### 第 16 章：Bit Manipulation（位元操作）

| # | 題目 | 難度 | 狀態 | 筆記 |
|---|------|------|------|------|
| 1 | Single Number | Easy | ⬜ | |
| 2 | Number of 1 Bits | Easy | ⬜ | |
| 3 | Counting Bits | Easy | ⬜ | |
| 4 | Reverse Bits | Easy | ⬜ | |
| 5 | Missing Number | Easy | ⬜ | |
| 6 | Sum of Two Integers | Medium | ⬜ | |
| 7 | Reverse Integer | Medium | ⬜ | |

---

## 學習進度總覽

```
NeetCode 150 進度：10 / 150 題 (6.7%)
額外練習題：4 題

✅ 已完成：14 題（NeetCode 10 + 額外 4）
⬜ 未開始：140 題

目前階段：第 2 章 - Two Pointers
```

---

## 學習紀錄

| 日期 | 完成題目 | 學到什麼 |
|------|----------|----------|
| 2026-01-05 | Two Sum | 反向索引、用空間換時間、Hash Table O(1) 查詢 |
| 2026-01-06 | Contains Duplicate | Set vs Dict、set.add() 語法、建立 O(n) vs 查詢 O(1)、early return 的價值 |
| 2026-01-06 | Valid Anagram | Dict 計數、.get(key, 0) 處理不存在的 key、Python 縮排決定邏輯、list comprehension |
| 2026-01-07 | Group Anagrams | 排序當標籤、dict value 是 list、if + append 組合、O(n × k log k) 複雜度分析 |
| 2026-01-12 | Top K Frequent（部分）| tuple index（x[0], x[1]）、lambda 不能寫 for loop、list comprehension 取特定欄位 |
| 2026-01-13 | Single Number | Set 配對消除法、XOR 位元運算（a^a=0）、discard vs remove、面試先講簡單解法再優化 |
| 2026-01-13 | Intersection of Two Arrays | Set 交集 `&`、`in set` O(1) vs `in list` O(n)、intersection/union/difference |
| 2026-01-14 | Missing Number | Set 差集 `-`、`set()` vs `{}` vs `()`、括號位置影響運算順序、`.pop()` 從 set 取值 |
| 2026-01-14 | Top K Frequent（完成）| Counter.most_common(k)、複習 dict.items() 排序、Bucket Sort 概念（O(n)）|
| 2026-01-14 | Majority Element | dict key vs value 區別、`dict[key]` 取 value、`.keys()` 不是 `.key()`、手動 dict 計數 |
| 2026-01-16 | Product of Array Except Self | Prefix/Suffix 預處理、`append()` vs index 賦值、倒著跑的 `range(n-1, -1, -1)`、不能用除法時分開算再合併 |
| 2026-01-19 | Valid Sudoku | 整數除法 `//` 分組、Dict of Sets 追蹤多維度、tuple 當 dict key、O(1) 固定大小 board |
| 2026-01-19 | Valid Palindrome | Two Pointers 雙指針模式、`.isalnum()` 跳過無效字元、`.lower()` 方法要加括號、O(1) 空間優勢 |
| 2026-01-20 | Two Sum II | 排序 array 用 Two Pointers 省空間 O(1)、大於小於的邏輯要對應正確動作、1-indexed 兩邊都要 +1 |
| 2026-02-10 | 3Sum | 3Sum = 固定一個數 + Two Sum II、去重兩個地方（外層 i + 內層 l/r）、找到答案後 while 跳重複要加 l < r 防越界 |

---

## 快捷指令

跟 Claude 說這些話可以快速開始：

- `開始今天的課程` → 繼續下一題
- `check` → 檢查我寫的 code
- `模擬面試` → 練習面試問答
- `整理筆記` → 把今天學的存成筆記
- `更新進度` → 更新 CLAUDE.md 的進度表
