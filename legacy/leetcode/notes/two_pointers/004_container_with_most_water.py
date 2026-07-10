# Problem: Container With Most Water (LeetCode 11)
# Pattern: Two Pointers (Converging + Greedy decision)
# Difficulty: Medium

# ============================================================
# Step D: Brute Force
# ============================================================
# Goal: write a working solution by trying EVERY pair of lines.
# Forget the Two Pointers trick for now — just brute force it.
#
# Hint: try every pair (i, j) where i < j, calculate the area,
# and keep track of the maximum.
#
# Area formula:
#   area = (j - i) * min(height[i], height[j])
#
# Expected complexity: O(n^2) time, O(1) space.
#
# Constraints reminder:
#   - 2 <= n <= 10^5
#   - 0 <= height[i] <= 10^4
#   - return: an integer (the maximum water area)


class Solution:
    def maxArea(self, height: list[int]) -> int:
        # Refactored brute force: area gets its own line
        maxarea = 0
        n = len(height)
        for i in range(n):
            for j in range(i + 1, n):
                area = (j - i) * min(height[i], height[j])  # step 1: compute
                if area > maxarea:  # step 2: compare
                    maxarea = area  # step 3: update
        return maxarea


# ============================================================
# Step E: Optimal Solution (Two Pointers, Converging + Greedy)
# ============================================================
# Goal: O(n) time, O(1) space.
#
# Idea (your job to implement):
#   - l = 0 (left), r = n - 1 (right)
#   - max_area = 0
#   - while l < r:
#       area = (r - l) * min(height[l], height[r])
#       max_area = max(max_area, area)
#       # GREEDY: move the pointer at the SHORTER line
#       if height[l] < height[r]:
#           l += 1
#       else:
#           r -= 1
#   - return max_area
#
# 🚨 WARNING (from Two Sum II Step E bug you parked):
#   - Use `l += 1` NOT `l + 1` (the second one does NOTHING)
#   - Use `r -= 1` NOT `r - 1`


class SolutionOptimal:
    def maxArea(self, height: list[int]) -> int:
        # your code here
        l, r = 0, len(height) - 1
        max_area = 0
        while l < r:
            area = (r - l) * min(height[l], height[r])
            max_area = max(max_area, area)
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return max_area


# ============================================================
# Test cases (you can run this file to verify)
# ============================================================
if __name__ == "__main__":
    sol = Solution()
    sol_opt = SolutionOptimal()

    print("--- Brute Force ---")
    # Example 1: [1,8,6,2,5,4,8,3,7] -> 49
    print(sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))

    # Example 2: [1,1] -> 1
    print(sol.maxArea([1, 1]))

    # Edge: [4,3,2,1,4] -> 16  (index 0 to 4, width 4, min height 4)
    print(sol.maxArea([4, 3, 2, 1, 4]))

    # Edge: [1,2,1] -> 2  (index 0 to 2, width 2, min height 1)
    print(sol.maxArea([1, 2, 1]))

    print("--- Optimal (Two Pointers) ---")
    print(sol_opt.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
    print(sol_opt.maxArea([1, 1]))  # 1
    print(sol_opt.maxArea([4, 3, 2, 1, 4]))  # 16
    print(sol_opt.maxArea([1, 2, 1]))  # 2
