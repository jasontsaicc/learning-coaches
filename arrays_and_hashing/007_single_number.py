"""
LeetCode 136. Single Number
https://leetcode.com/problems/single-number/

Given a non-empty array of integers nums, every element appears twice except
for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only
constant extra space.

Example 1:
    Input: nums = [2,2,1]
    Output: 1

Example 2:
    Input: nums = [4,1,2,1,2]
    Output: 4

Example 3:
    Input: nums = [1]
    Output: 1

Constraints:
    - 1 <= nums.length <= 3 * 10^4
    - -3 * 10^4 <= nums[i] <= 3 * 10^4
    - Each element in the array appears twice except for one element which appears only once.

---
中文翻譯：
給你一個非空整數陣列，每個元素都出現兩次，只有一個元素只出現一次。
找出那個只出現一次的元素。

進階要求：O(n) 時間，O(1) 空間（先不管這個，用 O(n) 空間也可以）
"""

from typing import List


def singleNumber(nums: List[int]) -> int:
    """
    思路：
    1. 怎麼知道一個數字「只出現一次」？
    2. 如果數字第一次出現，做什麼？
    3. 如果數字第二次出現，做什麼？

    提示：
    - 可以用 Set 來追蹤「目前只出現一次」的數字
    - 第一次看到 → 加進去
    - 第二次看到 → 拿掉
    - 最後 Set 裡剩什麼？
    """
    # TODO(human): 從頭實作你的解法
    my_set = set()
    for i in nums:
        if i not in my_set:
            my_set.add(i)
        else:
            my_set.discard(i)
    return my_set.pop()

def singleNumber_xor(nums: List[int]) -> int:
    result = 0
    for num in nums:
        result ^= num
    return result

# 本地測試
if __name__ == "__main__":
    test_cases = [
        ([2, 2, 1], 1),
        ([4, 1, 2, 1, 2], 4),
        ([1], 1),
        ([5, 3, 5, 3, 9, 8, 8], 9),  # DevOps: 找出只出現一次的 error code
    ]

    print("=== 解法一：Set 配對消除法 ===")
    for i, (nums, expected) in enumerate(test_cases, 1):
        result = singleNumber(nums)
        status = "✅" if result == expected else "❌"
        print(f"測試 {i}: {result} {status}")

    print("\n=== 解法二：XOR 位元運算 ===")
    for i, (nums, expected) in enumerate(test_cases, 1):
        result = singleNumber_xor(nums)
        status = "✅" if result == expected else "❌"
        print(f"測試 {i}: {result} {status}")
