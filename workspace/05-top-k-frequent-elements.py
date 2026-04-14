# Problem: Top K Frequent Elements (LeetCode 347)
# Pattern: Arrays & Hashing
# Step: D (Brute Force) — write your solution below

from typing import List
from collections import Counter


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # dict 頻率
         freq = Counter(nums)
       freq = Counter(nums)

        sorted_keys = sorted(freq, key=freq.get, reverse=True)
        return sorted_keys[:k]


# --- Optimal Solution (Step E) ---
# Pattern: Bucket Sort — avoid O(n log n) sorting


class SolutionOptimal:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # your code here
        freq = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, count in freq.items():
            buckets[count].append(num)

        result = []
        for i in range(len(buckets) - 1, -1, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result
