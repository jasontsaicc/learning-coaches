# Problem: Two Sum II - Input Array Is Sorted (LeetCode 167)
# Pattern: Two Pointers (Converging on sorted array)
# Difficulty: Medium

# ============================================================
# Step D: Brute Force
# ============================================================
# Goal: write a working solution WITHOUT using the sorted property.
# Just find any pair that sums to target.
#
# Hint: try every pair (i, j) where i < j.
# Expected complexity: O(n^2) time, O(1) space.
#
# Constraints reminder:
#   - return [index1, index2] in 1-indexed form
#   - 1 <= index1 < index2 <= len(numbers)
#   - exactly one solution exists


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        n = len(numbers)
        for i in range(n):
            for j in range(i + 1, n):
                if numbers[i] + numbers[j] == target:
                    return [i + 1, j + 1]
        return []


# ============================================================
# Step E: Optimal Solution (Two Pointers, Converging)
# ============================================================
# Goal: O(n) time, O(1) space using the SORTED property.
#
# Idea (your job to implement):
#   - left = 0 (pointer at smallest)
#   - right = n - 1 (pointer at largest)
#   - while left < right:
#       compute total = numbers[left] + numbers[right]
#       if total == target -> return (1-indexed)
#       if total < target  -> need bigger sum, move left
#       if total > target  -> need smaller sum, move right
#
# Constraints reminder:
#   - return [index1, index2] in 1-indexed form
#   - exactly one solution exists


class SolutionOptimal:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        # your code here
        l, r = 0, len(numbers) - 1
        while l < r:
            total = numbers[l] + numbers[r]

            if total == target:
                return [l + 1, r + 1]
            elif total < target:
                l + 1
            else:
                r + 1
        return []


# ============================================================
# Test cases (you can run this file to verify)
# ============================================================
if __name__ == "__main__":
    sol = Solution()
    sol_opt = SolutionOptimal()

    print("--- Brute Force ---")
    # Example 1: [2, 7, 11, 15], target=9 -> [1, 2]
    print(sol.twoSum([2, 7, 11, 15], 9))

    # Example 2: [2, 3, 4], target=6 -> [1, 3]
    print(sol.twoSum([2, 3, 4], 6))

    # Example 3: [-1, 0], target=-1 -> [1, 2]
    print(sol.twoSum([-1, 0], -1))

    print("--- Optimal (Two Pointers) ---")
    # Same examples for optimal
    print(sol_opt.twoSum([2, 7, 11, 15], 9))
    print(sol_opt.twoSum([2, 3, 4], 6))
    print(sol_opt.twoSum([-1, 0], -1))

numbers = [2, 7, 11]
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        print(i, j)
