from typing import List


class Solution:
    # 冷寫 (cold solve): 不要回去看 20-daily-temperatures.py，憑記憶默出來。
    # Monotonic Stack — 等待區存 index、遞減；新的一天 pop 掉比它冷的並記距離。
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []

        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev = stack.pop()
                answer[prev] = i - prev
            stack.append(i)

        return answer


# --- self-check ---
if __name__ == "__main__":
    s = Solution()
    assert s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [
        1,
        1,
        4,
        2,
        1,
        1,
        0,
        0,
    ]
    assert s.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert s.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    assert s.dailyTemperatures([90, 80, 70]) == [0, 0, 0]
    assert s.dailyTemperatures([55]) == [0]
    print("cold solve passed ✅ — Stack 升 🟢")
