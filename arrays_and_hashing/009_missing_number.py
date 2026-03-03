"""
LeetCode 268. Missing Number
https://leetcode.com/problems/missing-number/

Given an array nums containing n distinct numbers in the range [0, n],
return the only number in the range that is missing from the array.

Example 1:
    Input: nums = [3, 0, 1]
    Output: 2
    Explanation: n = 3 since there are 3 numbers, so all numbers are in
    the range [0, 3]. 2 is the missing number since it does not appear in nums.

Example 2:
    Input: nums = [0, 1]
    Output: 2
    Explanation: n = 2 since there are 2 numbers, so all numbers are in
    the range [0, 2]. 2 is the missing number since it does not appear in nums.

Example 3:
    Input: nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
    Output: 8
    Explanation: n = 9 since there are 9 numbers, so all numbers are in
    the range [0, 9]. 8 is the missing number since it does not appear in nums.

Constraints:
    - n == nums.length
    - 1 <= n <= 10^4
    - 0 <= nums[i] <= n
    - All the numbers of nums are unique.

---
中文翻譯：
給你一個包含 n 個不重複數字的陣列 nums，數字範圍是 [0, n]。
找出這個範圍內唯一缺少的數字。
"""

from typing import List


def missingNumber(nums: List[int]) -> int:
    """
    思路：
    1. 陣列有 n 個數字，範圍是 0 到 n
    2. 所以「應該有」n+1 個數字，但少了一個
    3. 怎麼找出少了哪一個？

    提示：
    - 想想你之前學過的 Set 怎麼用
    - 或者... 數學課教過 1+2+3+...+n 怎麼算？
    """
    # TODO(human): 從頭實作你的解法
    my_set = set()
    total = len(nums)
    for i in range(len(nums) +1):
        my_set.add(i)
    result = my_set - set(nums)
    return result.pop()

# 本地測試
if __name__ == "__main__":
    test_cases = [
        ([3, 0, 1], 2),
        ([0, 1], 2),
        ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
        ([0], 1),
        ([1], 0),
    ]

    for i, (nums, expected) in enumerate(test_cases, 1):
        result = missingNumber(nums)
        status = "✅" if result == expected else "❌"
        print(f"測試 {i}: nums={nums}")
        print(f"        結果={result}, 預期={expected} {status}")
        print()
