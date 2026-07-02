# Min Stack (#155) — Medium

> Pattern: Stack (Design — 記狀態)
> Session 12 · jump-to（分享會速成）· 2026-06-11

---

## Pattern 摘要

> 設計一個 stack，push/pop/top/getMin 全部 O(1)。核心技巧：每個元素進來時，把「當下的最小值」一起存進去 `[val, min]`。這樣不管 pop 幾次，每一層都自帶當時的 min，`getMin()` 直接看頂端 → O(1)。

---

## 解法 (Approach)

### 暴力法 — Time O(n), Space O(n)

每次呼叫 `getMin()` 就掃整個 stack 找最小值。問題：O(n) per call，不符合要求。

### 最佳解 — Time O(1) all ops, Space O(n)

每個元素存 `[val, min_at_this_level]`：

1. **push**：算出 `cur_min = min(val, 頂端的min)`，append `[val, cur_min]`
2. **pop**：`self.stack.pop()`，val 和 min 一起移除
3. **top**：`self.stack[-1][0]`（第 0 個 = val）
4. **getMin**：`self.stack[-1][1]`（第 1 個 = min）

### 關鍵洞察 (Key Insight)

**用空間換時間**：原本 getMin 要 O(n) 掃描，現在每個元素多存一個 min，換來 O(1)。每一層的 min 在 push 時就算好，pop 時自動跟著消失，不需要額外更新。

---

## 💻 My Code

```python
class MinStack:

    def __init__(self):
        self.stack = []  # each element: [val, min_at_this_level]

    def push(self, val: int) -> None:
        if not self.stack:
            cur_min = val
        else:
            cur_min = min(val, self.stack[-1][1])
        self.stack.append([val, cur_min])

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

---

## 🧠 心智模型：每個元素自帶「那個時刻的 min」

```
push(-2) → stack: [[-2, min=-2]]
push(0)  → stack: [[-2, -2], [0,  min=-2]]   ← 0 > -2，min 不變
push(-3) → stack: [[-2, -2], [0, -2], [-3, min=-3]]

getMin() → stack[-1][1] = -3   O(1)

pop()    → 移掉 [-3, -3]

getMin() → stack[-1][1] = -2   O(1)  ← 自動恢復，因為每層都記好了
```

---

## 🔑 為什麼用 class？

| | function | class |
|--|--|--|
| 用途 | 一進一出，做完結束 | 需要記住狀態，跨操作保留資料 |
| 例子 | `isValid(s)` | `MinStack()` |

`self.stack` 跟著物件一直活著，多次 push/pop/getMin 之間的資料都保留在裡面。LeetCode Design 類題目幾乎都是 class，因為都需要記狀態。

---

## ⚡ Edge Cases

- **只有一個元素**：push 完直接 getMin = 那個值本身
- **相同值重複 push**：`min(val, stack[-1][1])` 取到相同的 min，沒問題
- **stack 是空的時候 push**：`if not self.stack` 特別處理，cur_min = val

---

## 🔴 我的錯誤

| 我寫的 | 正確 | 為什麼錯 |
|--------|------|----------|
| `min(val.self.stack[-1][1])` | `min(val, self.stack[-1][1])` | `.` 是存取屬性，`,` 才是分隔參數 |

---

## 💡 另一種寫法（兩個分開的 stack）

```python
def __init__(self):
    self.stack = []
    self.min_stack = []

def push(self, val):
    self.stack.append(val)
    cur_min = val if not self.min_stack else min(val, self.min_stack[-1])
    self.min_stack.append(cur_min)

def pop(self):
    self.stack.pop()
    self.min_stack.pop()
```

概念完全一樣，只是把 `[val, min]` 拆開成兩個 list。面試兩種都可以。

---

## 🎤 How to Say It in Interview

**Opening:**
> "The naive approach is to scan the whole stack for getMin, which is O(n). Instead, I store each element as a pair `[val, current_min]`. When pushing, I compare the new value with the top's min and keep the smaller one. This way, getMin is always O(1) — just peek at the top's min."

**Complexity:**
> "All four operations are O(1). Space is O(n) — we're storing one extra min per element."
