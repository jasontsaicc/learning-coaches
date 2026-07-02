# 84. Largest Rectangle in Histogram（直方圖最大矩形）

> 讀書會講稿版。從直覺到 code，照順序講。

## 一句話題意

給一排長條（每根寬 1、高度是 `heights[i]`），在直方圖裡框出**面積最大的矩形**。
矩形規則：一旦跨越多根，**高度只能取這段區間裡最矮那根**（超過就凸出去了）。

範例 `heights = [2,1,5,6,2,3]`，答案 = **10**。

```
              6
          5   █
          █   █
          █   █           3
  2       █   █   2       █
  █   1   █   █   █       █
  █   █   █   █   █   █   █
  2   1   5   6   2   3
  0   1   2   3   4   5     index
```

## 核心直覺（整題就這一句）

**每根長條都問自己一次：「以我的高度當最矮天花板，我能往左右拉多寬？」**
往左往右伸手，**撞到比我矮的長條就停**（那根擋住我）；比我高的可以鑽過去。
掃過每一根、各算一次面積、取最大。

為什麼每根都要試？因為**高和寬在互相拉扯**，用範例看三根：

| 站在 | 高度 | 往左撞牆 | 往右撞牆 | 寬 | 面積 |
|------|------|----------|----------|----|------|
| index 3 | 6（最高）| 5<6 立刻停 | 2<6 立刻停 | 1 | 6 |
| index 2 | 5 | 1<5 停 | 6>5 鑽過去、到 2<5 才停 | 2 | **10** |
| index 1 | 1（最矮）| 到底 | 一路到底 | 6 | 6 |

重點：**冠軍是中間的 index 2（高5、寬2）**，不是最高的、也不是最寬的。所以不能只挑一根，要每根都試。

口訣：**越高越容易被困窄，越矮越能拉寬。**

## 解法一：Brute Force　O(n²)

對每根 `i`：往左延伸到第一根比它矮的、往右延伸到第一根比它矮的，`寬 = 右 - 左 - 1`，`面積 = 高[i] × 寬`，取最大。

```python
def largest_rectangle_area(heights):
    n = len(heights)
    max_area = 0
    for i in range(n):
        left = i
        while left >= 0 and heights[left] >= heights[i]:
            left -= 1                 # 停在左邊第一根比我矮的（界外一格）
        right = i
        while right < n and heights[right] >= heights[i]:
            right += 1                # 停在右邊第一根比我矮的（界外一格）
        width = right - left - 1      # 兩端都界外，中間才是我的 → 再 -1
        max_area = max(max_area, heights[i] * width)
    return max_area
```

複雜度：外層 n 根 × 每根往左右各掃最多 n 格 = **O(n²)**，空間 **O(1)**。
瓶頸：同一段長條被重複掃很多次。

## 解法二：Monotonic Stack（單調堆疊）　O(n)

### 排隊故事（講這段就好懂）

長條**一根一根照順序進場排隊**。隊伍規則：**只有比隊尾高才排得進來**（所以隊伍高度由底到頂遞增）。

- **新來的比隊尾高** → 自己排進去等。（還不知道右牆在哪）
- **新來的比隊尾矮** → 它就是隊尾那根的**右牆**！把隊尾**結算離場**（算面積）。而且可能連續踢好幾根（誰比它高就踢誰）。

結算離場那一刻，兩道牆**自動送上門**：

| 牆 | 是誰 | 原因 |
|----|------|------|
| **右牆** | 逼你離場的那個新人 | 就是它比你矮才觸發結算 |
| **左牆** | 踢掉你之後的新隊尾 | 隊伍遞增，你身後那根正是左邊最近一個比你矮的（空了就代表沒左牆、延伸到最左）|

寬度公式跟 brute force 一樣：`寬 = 右牆index - 左牆index - 1`。

### 逐格 trace（`[2,1,5,6,2,3]`）

```
stack 存 index（高度遞增）
i=0 h=2  push 0                      stack=[0]      高[2]
i=1 h=1  頂端0(h2)>1 → pop 0
           右=1 左=空(-1) 寬=1 面積=2×1=2
         push 1                      stack=[1]      高[1]
i=2 h=5  頂端1(h1)>5? 否 → push 2     stack=[1,2]    高[1,5]
i=3 h=6  頂端2(h5)>6? 否 → push 3     stack=[1,2,3]  高[1,5,6]
i=4 h=2  頂端3(h6)>2 → pop 3
           右=4 左=位置2 寬=4-2-1=1 面積=6×1=6
         頂端2(h5)>2 → pop 2
           右=4 左=位置1 寬=4-1-1=2 面積=5×2=10   ← 冠軍
         頂端1(h1)>2? 否 → push 4     stack=[1,4]    高[1,2]
i=5 h=3  頂端4(h2)>3? 否 → push 5     stack=[1,4,5]  高[1,2,3]
收尾（右邊界當 n=6）:
   pop 5  h3 左=位置4 寬=1 面積=3
   pop 4  h2 左=位置1 寬=6-1-1=4 面積=8
   pop 1  h1 左=空(-1) 寬=6 面積=6
答案 = 10
```

### Code

```python
def largest_rectangle_area(heights):
    n = len(heights)
    max_area = 0
    stack = []                                  # 存 index，高度由底到頂遞增

    for i in range(n):
        # 頂端比目前這根「高」→ i 就是它的右牆 → 結算它
        while stack and heights[stack[-1]] > heights[i]:
            top = stack.pop()
            left = stack[-1] if stack else -1   # 新隊尾=左牆；空→-1(延伸到最左)
            width = i - left - 1                 # 右(i) - 左 - 1
            max_area = max(max_area, heights[top] * width)
        stack.append(i)

    # 收尾：還留在隊伍的，右邊沒遇到更矮的 → 右牆當 n
    while stack:
        top = stack.pop()
        left = stack[-1] if stack else -1
        width = n - left - 1
        max_area = max(max_area, heights[top] * width)

    return max_area
```

### 複雜度：為什麼有雙層迴圈還是 O(n)

每個 index **一生只進隊一次、只離隊一次**，所以就算內層有 while，全程 pop 的總次數加起來 `<= n`。
時間 **O(n)**（攤還 amortized），空間 **O(n)**（stack 最多裝 n 個 index）。

> 攤還：不看單次最壞，看「總操作量 ÷ 次數」。

## 記憶點

1. 每根當最矮天花板，往左右撞矮牆，`寬 = 右 - 左 - 1`。
2. Stack 排隊：**比隊尾高就排進去、比隊尾矮就把高的結算離場**。
3. 結算時：**右牆 = 逼你離場的新人、左牆 = 你身後的隊尾**（空了就到最左）。
4. **pop 條件決定 stack 方向**：pop「更矮的」→ 遞增 stack（本題）；pop「更大的」→ 遞減 stack（Daily Temperatures #739）。兩題完美鏡像。
