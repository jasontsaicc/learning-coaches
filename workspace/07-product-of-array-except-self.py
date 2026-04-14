# Problem: Product of Array Except Self (238)
# Pattern: Arrays & Hashing (Prefix / Suffix)
# Step: D (Brute Force) — write your solution below

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # your code here
        answer = []

        for i in range(len(nums)):
            product = 1
            for j in range(len(nums)):
                if j == i:
                    continue
                product *= nums[j]
            answer.append(product)
        return answer


# --- Optimal Solution (Step E) ---


class SolutionOptimal:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # Step 1: Build prefix array (left side products)
        prefix = [1] * n
        # your code here — fill prefix from left to right
        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]
        # Step 2: Build suffix array (right side products)
        suffix = [1] * n
        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]
        # your code here — fill suffix from right to left

        # Step 3: Combine prefix * suffix
        answer = []
        for i in range(n):
            answer.append(prefix[i] * suffix[i])
        # your code here — multiply prefix[i] * suffix[i]

        return answer
