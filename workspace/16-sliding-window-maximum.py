# Problem: Sliding Window Maximum (#239) - Hard
# Pattern: Sliding Window + Monotonic Deque
# Step: D (Brute Force) — your turn to write!

# ============================================================
# Problem Recap
# ============================================================
# Given an array nums and window size k, slide a window of size k
# from left to right. For each window position, output the MAX
# element in that window.
#
# Example:
#   nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
#   Output: [3, 3, 5, 5, 6, 7]
#
# Key formula (already confirmed):
#   Number of windows = n - k + 1
#   (n=8, k=3 → 8 - 3 + 1 = 6 windows)


# ============================================================
# Step D: Brute Force — YOUR TURN
# ============================================================
# Strategy:
#   1. Loop over each window position (how many iterations?)
#   2. For each position i, extract the k elements (slicing!)
#   3. Find the max of those k elements (built-in function)
#   4. Append to the result list
#
# Tips:
#   - Python slicing: nums[start:end]  (end is exclusive)
#   - Use Python's built-in max() on a list
#   - Watch out for typos in variable names (window vs windows)

from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        result = []

        for i in range(n - k + 1):
            window = nums[i : i + k]
            current_max = max(window)
            result.append(current_max)

        return result


# ============================================================
# Step E: Optimal Solution (Monotonic Deque) — YOUR TURN
# ============================================================
# Target:  Time O(n), Space O(k)
#
# 4-Step Recipe (run inside the for loop, for each new i):
#


from collections import deque


class SolutionOptimal:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        result = []
        dq = (
            deque()
        )  # stores INDICES; values at these indices are monotonically decreasing

        for i in range(n):
            # 1. POPLEFT — drop indices that fell out of the window
            while (
                dq and dq[0] <= i - k
            ):  # Blank A: condition for "leftmost index expired"
                dq.popleft()

            # 2. POP RIGHT — drop indices whose values are smaller than nums[i]
            while (
                dq and nums[dq[-1]] < nums[i]
            ):  # Blank B: condition for "rightmost value < current value"
                dq.pop()

            # 3. APPEND — add current index
            dq.append(i)  # Blank C: append what? (hint: an INDEX, not a value)

            # 4. READ — once window is full, record the max
            if i >= k - 1:  # Blank D: when is the window first full?
                result.append(
                    nums[dq[0]]
                )  # Blank E: how to read the max value out of the deque?

        return result


# ============================================================
# Self-test — runs BOTH solutions for comparison
# Command:  python3 workspace/16-sliding-window-maximum.py
# ============================================================
if __name__ == "__main__":
    brute = Solution()
    optimal = SolutionOptimal()

    test_cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([4, 2, 6, 8], 2, [4, 6, 8]),
        ([5, 2, 9], 3, [9]),
        ([7], 1, [7]),
        ([9, 8, 7, 6, 5], 3, [9, 8, 7]),  # strictly decreasing
        ([1, 2, 3, 4, 5], 3, [3, 4, 5]),  # strictly increasing
    ]

    print("=" * 60)
    print("Brute Force  O(n*k):")
    print("=" * 60)
    for nums, k, expected in test_cases:
        got = brute.maxSlidingWindow(nums[:], k)
        status = "PASS" if got == expected else "FAIL"
        print(f"  nums={nums}, k={k}: got={got} -> {status}")

    print()
    print("=" * 60)
    print("Optimal (Monotonic Deque)  O(n):")
    print("=" * 60)
    for nums, k, expected in test_cases:
        got = optimal.maxSlidingWindow(nums[:], k)
        status = "PASS" if got == expected else "FAIL"
        print(f"  nums={nums}, k={k}: got={got} -> {status}")
