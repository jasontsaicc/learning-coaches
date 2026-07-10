# Problem: Trapping Rain Water (LeetCode #42)
# Pattern: Two Pointers + Bounded Computation
# Step: D (Brute Force) — write your solution below
#
# Goal: For each position i, water trapped above it is:
#       min(left_max, right_max) - height[i]
#       where left_max  = max(height[0..i])
#             right_max = max(height[i..n-1])
#
# Time:  O(n^2) — outer loop n × inner max() scan n
# Space: O(1)   — no extra arrays
#
# Examples:
#   trap([0,1,0,2,1,0,1,3,2,1,2,1]) -> 6
#   trap([4,2,0,3,2,5])             -> 9
#   trap([5,0,1,0,3])               -> 8


from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        # Brute Force — O(n^2) time, O(1) space
        total = 0
        for i in range(len(height)):
            left_max = max(height[: i + 1])
            right_max = max(height[i:])
            total += min(left_max, right_max) - height[i]
        return total


# --- DP Solution (Step E — Optimization 1) ---
# Time:  O(n)  — three single passes
# Space: O(n)  — two arrays of length n
class SolutionDP:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        # Step 1: build left_max[] — scan left to right
        left_max = [0] * n
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # Step 2: build right_max[] — scan right to left
        right_max = [0] * n
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])
        # Step 3: sum up water
        total = 0
        for i in range(n):
            total += min(left_max[i], right_max[i]) - height[i]
        # your code here: for each i, total += min(left_max[i], right_max[i]) - height[i]

        return total


# --- Two Pointers Solution (Step E — Optimization 2, OPTIMAL) ---
# Time:  O(n)  — single pass, two pointers converge
# Space: O(1)  — only 5 scalars (l, r, left_max, right_max, total)
class Solution2P:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        l, r = 0, n - 1
        left_max, right_max = 0, 0
        total = 0

        while l < r:
            if height[l] < height[r]:
                if height[l] >= left_max:
                    left_max = height[l]
                else:
                    total += left_max - height[l]
                l += 1
            else:
                if height[r] >= right_max:
                    right_max = height[r]
                else:
                    total += right_max - height[r]
                r -= 1
        return total


# ---- Tests ----
if __name__ == "__main__":
    sol_brute = Solution()
    sol_dp = SolutionDP()
    sol_2p = Solution2P()
    test_cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([5, 0, 1, 0, 3], 8),
        ([0, 0, 0], 0),  # all zeros
        ([3, 3, 3], 0),  # flat
        ([1], 0),  # single element
    ]
    print("=== Brute Force ===")
    for i, (heights, expected) in enumerate(test_cases, 1):
        result = sol_brute.trap(heights)
        status = "✅" if result == expected else "❌"
        print(f"Test {i}: {status}  trap({heights}) = {result}  (expected {expected})")

    print("\n=== DP O(n) Solution ===")
    for i, (heights, expected) in enumerate(test_cases, 1):
        result = sol_dp.trap(heights)
        status = "✅" if result == expected else "❌"
        print(f"Test {i}: {status}  trap({heights}) = {result}  (expected {expected})")

    print("\n=== Two Pointers O(1) Space Solution ===")
    for i, (heights, expected) in enumerate(test_cases, 1):
        result = sol_2p.trap(heights)
        status = "✅" if result == expected else "❌"
        print(f"Test {i}: {status}  trap({heights}) = {result}  (expected {expected})")
