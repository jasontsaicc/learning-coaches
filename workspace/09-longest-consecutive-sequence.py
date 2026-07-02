# Problem: Longest Consecutive Sequence (128)
# Pattern: Arrays & Hashing (HashSet + Sequence Start Detection)
# Step: D (Brute Force) — write your solution below

from typing import Coroutine, List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # your code here
        counter = 1
        max_len = 1
        if not nums:
            return 0

        sort_num = sorted(nums)
        for i in range(1, len(sort_num)):
            if sort_num[i] - sort_num[i - 1] == 0:
                continue
            elif sort_num[i] - sort_num[i - 1] == 1:
                counter += 1
                max_len = max(max_len, counter)
            else:
                counter = 1
        return max_len


# --- Optimal Solution (Step E) ---


class SolutionOptimal:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        max_len = 0

        for num in numSet:
            # only start counting from sequence start
            if num - 1 not in numSet:
                length = 1
                while num + length in numSet:
                    length += 1
                max_len = max(max_len, length)

        return max_len
