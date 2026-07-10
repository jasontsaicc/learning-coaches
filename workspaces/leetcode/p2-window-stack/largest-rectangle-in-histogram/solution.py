# 84. Largest Rectangle in Histogram
# https://leetcode.com/problems/largest-rectangle-in-histogram/


def largest_rectangle_area(heights):
    # Brute force: 每根當「最矮天花板」，往左右延伸到第一根比它矮的，寬 × 高 = 面積，取最大。
    n = len(heights)
    max_area = 0  # 老朋友：邊掃邊更新，先給 0

    for i in range(n):
        # ── 往左延伸（你寫的，補上 left = i 就對了）──
        left = i
        while left >= 0 and heights[left] >= heights[i]:
            left -= 1
        # while 停下時，left 停在「第一根比我矮的」位置 = 界外一格

        # ── 往右延伸（鏡像左邊，照抄改方向）──
        right = i  # ① 從哪出發？(對照 left = i)
        while (
            right < n and heights[right] >= heights[i]
        ):  # ② 界內條件？(左邊是 left >= 0，右邊界是誰？)
            right += 1

        # ── 算面積 ──
        width = right - left - 1  # ③【要動腦】left、right 都停在界外一格，寬度公式？
        #    驗證：index 4 那根，left 停 1、right 停 6，寬度應該 = 4
        area = heights[i] * width  # ④ 面積 = ?
        max_area = max(max_area, area)  # ⑤ 更新最大 (你的老朋友 max(...))

    return max_area


def largest_rectangle_area_stack(heights):
    # Monotonic stack (遞增): stack 存 index。遇到比頂端矮的 → 頂端等到右邊界了，pop + 結算。
    # 結算時左右邊界從 stack 免費拿到，width 公式跟 brute force 一模一樣：右 - 左 - 1。
    n = len(heights)
    max_area = 0
    stack = []  # 存 index，heights 由底到頂「遞增」

    for i in range(n):
        # 頂端比目前這根「高」→ 它右邊遇到更矮的(就是 i) → 結算它
        while stack and heights[stack[-1]] > heights[i]:
            top = stack.pop()
            left = stack[-1] if stack else -1   # pop 完的新頂端 = 左邊界；空→-1(一路到最左)
            width = i - left - 1                 # 右(i) - 左 - 1，同 brute force
            max_area = max(max_area, heights[top] * width)
        stack.append(i)

    # 收尾：還留 stack 裡的，右邊沒遇到更矮的 → 右邊界當 n
    while stack:
        top = stack.pop()
        left = stack[-1] if stack else -1
        width = n - left - 1                     # 右邊界換成 n
        max_area = max(max_area, heights[top] * width)

    return max_area


tests = [
    ([2, 1, 5, 6, 2, 3], 10),
    ([2, 4], 4),
    ([5], 5),
    ([2, 1, 2], 3),
    ([0], 0),
]

for heights, expected in tests:
    brute = largest_rectangle_area(heights)
    stack = largest_rectangle_area_stack(heights)
    ok = brute == expected == stack
    status = "PASS" if ok else "FAIL"
    print(f"{status}  heights={heights}  expected={expected}  brute={brute}  stack={stack}")
