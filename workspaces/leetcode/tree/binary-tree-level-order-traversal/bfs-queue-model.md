# BFS 母版:排隊模型

2026-09-27 學員用 ChatGPT 學 BFS 的整理,學員自評「好懂很多」。
兔模式(#637、#103、#199…)開場先貼這份,不從記憶裡撈。

## 三句話

1. **Queue = 排隊**
2. **前面拿,後面塞**:`queue.popleft()` / `queue.append(...)`
3. **要分層:先數這層**:`level_size = len(queue)`

```text
while = 一層
for   = 這層的人
```

## 固定例子

```text
        1
       / \
      2   3
     / \
    4   5
```

普通 BFS 順序:`1 → 2 → 3 → 4 → 5`

```text
Queue = [1]
拿 1,塞 2、3        Queue = [2, 3]
拿 2,塞 4、5        Queue = [3, 4, 5]     ← 不是 [4, 5, 3],3 比較早排隊
```

**誰先排隊,誰先處理。** 所以自然一層一層。

## 為什麼要先數這層

```text
開始這層:     queue = [2, 3]      level_size = 2
拿 2,塞 4、5: queue = [3, 4, 5]   level_size 還是 2
拿 3:         queue = [4, 5]      已拿 2 個,這層結束
下一圈 while:  level_size = len(queue) = 2,開始處理 4、5
```

4、5 是下一層。不能因為 queue 裡還有人,就一起處理。
**先數這層,再處理這層。**

## BFS vs DFS

```text
        1
       / \
      2   3
     /
    4
BFS = 1, 2, 3, 4   一層一層
DFS = 1, 2, 4, 3   一條路走到底
```

## 模板

```python
from collections import deque

queue = deque([root])

while queue:
    level_size = len(queue)

    for _ in range(level_size):
        node = queue.popleft()

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)
```

人話版:

```text
root 先排隊
只要 queue 還有人:
    先數這層
    把這層每個人處理完:
        前面拿
        左小孩後面塞
        右小孩後面塞
```

## 我踩過的

- `queue.left()`:方向對(要從左邊拿),只差 API 名字 → `queue.popleft()`
- `visited` 是 Graph BFS 的東西(A→B→A 會繞圈),Tree BFS 先不用。

## 這份為什麼好懂(給 coach 的)

先有畫面再有名詞 → 一次只加一個概念 → 固定同一棵樹 → 每步預測 `queue = ?` →
填一行 → 逐行組出模板 → 最後才默寫。錯誤先分「概念錯 / API 錯」。
規則已寫進 `skills/leetcode-coach/references/teaching-loop.md` 的「步伐規則」。
