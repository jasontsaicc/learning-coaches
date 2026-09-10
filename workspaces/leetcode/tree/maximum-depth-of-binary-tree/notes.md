# #104 Maximum Depth of Binary Tree

圖解頁:尚未產出。

模式:龜(第一題真的要吃下屬的回傳值。#226 是模板最鬆的版本,不吃回傳值,
交換擺哪都行;#104 開始「順序鎖死」— 委派要先跑完才能組出這一層的答案)。

## 這題的重點

- base case:`dfs(None) = 0`(空樹深度是 0)。
- 這一層自己不知道左右哪邊比較深,兩邊都要問過(委派)才能比,**不能隨便選一邊**。
  反例:`2` 只有左小孩 `4`,沒右小孩。永遠選右邊 → `dfs(2) = 1 + dfs(None) = 1`,
  但正確答案是 `2`(2→4 兩層)。漏算整條左邊。
- 完整公式:`return max(left, right) + 1`。`+1` 算的是自己這一層。

```python
def maxDepth(root):
    if not root:
        return 0
    left = maxDepth(root.left)
    right = maxDepth(root.right)
    return max(left, right) + 1
```

- dry run 範例(下次接著用同一棵樹跑拷問 ②③④):

```
        1
       / \
      2   3
     /
    4
```

```
dfs(1)
├─ dfs(2)
│  ├─ dfs(4)
│  │  ├─ dfs(None) → 0
│  │  ├─ dfs(None) → 0
│  │  └─ return max(0,0)+1 = 1      ← dfs(4) = 1
│  ├─ dfs(None) → 0                  (2 沒有右小孩)
│  └─ return max(1,0)+1 = 2         ← dfs(2) = 2
├─ dfs(3)
│  ├─ dfs(None) → 0
│  ├─ dfs(None) → 0
│  └─ return max(0,0)+1 = 1         ← dfs(3) = 1
└─ return max(2,1)+1 = 3            ← dfs(1) = 3
```

## 模板遷移

`dfs(node)` 通用模板,跟 #226 同骨架,差在委派後要不要吃回傳值:
#100 Same Tree(回 True/False)、#543 Diameter(回高度 + 全域最大)。

## 檔案

尚無 solution.py / drill.py / eli5.html。

## 進度

- 2026-09-10:對話中用具體反例(2 的右小孩選 → 漏算左邊)糾正「隨便選一邊」,
  Socratic 帶出完整公式 `max(left,right)+1`,已組出完整函式。開始 dry run
  (上面的 1-2-3-4 樹),coach 畫出完整 call stack。**收在「dfs(1) 最後
  max(2,1)+1 這兩個數字從哪來」這題,學員還沒回答就下班,不記債。**
  下次直接從這題接著問,再走拷問 ②③④、溫度計 ②、產出 eli5 圖解頁 + drill.py + L6 逐字稿。
