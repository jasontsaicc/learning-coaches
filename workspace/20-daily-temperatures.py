from typing import List


class Solution:
    # Brute force: for each day i, scan forward to find the first hotter day.
    # Time O(n^2), Space O(1) extra.
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n  # default 0: no hotter day found
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    answer[i] = j - i
                    break
        # TODO (你來寫):
        #   內層 for j in range(i+1, n):
        #       如果 temperatures[j] > temperatures[i]:
        #           answer[i] = j - i
        #           break   # 找到「第一個」就停
        # 最後 return answer

        return answer

    # Monotonic Stack: stack holds indices of days still waiting for a warmer day.
    # Temperatures of stacked indices stay strictly decreasing (monotonic).
    # Time O(n) — each index pushed once, popped at most once. Space O(n).
    def dailyTemperaturesStack(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []  # 等待區，裝 index

        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev = stack.pop()              # 等到暖天的那一天
                answer[prev] = i - prev         # 距離 = 今天 - 那天
            stack.append(i)                     # 今天自己進等待區 (while 跑完才做)

        return answer


# --- self-check: 跑這個檔案就會驗證 ---
if __name__ == "__main__":
    s = Solution()
    assert s.dailyTemperaturesStack([73, 74, 75, 71, 69, 72, 76, 73]) == [
        1,
        1,
        4,
        2,
        1,
        1,
        0,
        0,
    ]
    assert s.dailyTemperaturesStack([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert s.dailyTemperaturesStack([30, 60, 90]) == [1, 1, 0]
    assert s.dailyTemperaturesStack([90, 80, 70]) == [0, 0, 0]
    assert s.dailyTemperaturesStack([55]) == [0]
    print("all monotonic-stack tests passed ✅")

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
    print("all brute-force tests passed ✅")
