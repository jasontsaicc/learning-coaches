"""
LeetCode 169. Majority Element
https://leetcode.com/problems/majority-element/

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times.
You may assume that the majority element always exists in the array.

Example 1:
    Input: nums = [3,2,3]
    Output: 3

Example 2:
    Input: nums = [2,2,1,1,1,2,2]
    Output: 2

Constraints:
    - n == nums.length
    - 1 <= n <= 5 * 10^4
    - -10^9 <= nums[i] <= 10^9

Follow-up: Could you solve the problem in linear time and in O(1) space?

---
中文翻譯：
給你一個大小為 n 的陣列 nums，回傳 majority element（多數元素）。
多數元素是指出現次數「超過 n/2 次」的元素。
題目保證多數元素一定存在。

進階挑戰：你能用 O(n) 時間和 O(1) 空間解決嗎？
"""

from typing import List
from collections import Counter

def majorityElement(nums: List[int]) -> int:
    """
    思路：
    - 這題跟 Top K Frequent 很像，都是「計數」問題
    - 差別：Top K 要找前 k 個最多的，這題只要找「出現超過 n/2 次」的那一個

    提示：
    - 你可以用 dict 計數，然後找出 count > len(nums)//2 的
    - 或者用 Counter，想想怎麼只取「最多的那一個」
    """
    count = Counter(nums).most_common(1)
    return count[0][0]

def majorityElement_dict(nums):
    my_dict = {}
    for i in nums:
        if i not in my_dict:
            my_dict[i] = 1
        else:
            my_dict[i] += 1
    for n in my_dict.keys():
        if my_dict[n] > len(nums) / 2:
            return n

# 本地測試
if __name__ == "__main__":
    test_cases = [
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
        ([1, 1, 1, 1, 2, 2, 2], 1),
        ([6, 6, 6, 7, 7], 6),
    ]

    for i, (nums, expected) in enumerate(test_cases, 1):
        result = majorityElement(nums)
        status = "✅" if result == expected else "❌"
        print(f"測試 {i}: nums={nums}, expected={expected}, got={result} {status}")
