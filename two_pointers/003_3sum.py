"""
LeetCode 15. 3Sum
https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]

Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

---
中文翻譯：
給你一個整數陣列 nums，找出所有三個數加起來等於 0 的組合。
答案不能有重複的組合。
"""

from typing import List


def threeSum(nums: List[int]) -> List[List[int]]:
    """
    思路：
    1. 先排序 array
    2. 外層 for loop 固定第一個數 nums[i]
       - 如果 nums[i] == nums[i-1]，跳過（避免重複）
    3. 內層用 Two Pointers (left, right) 找兩個數加起來 = -nums[i]
       - 找到答案後，移動指針時也要跳過重複的值

    提示：
    - 排序用 nums.sort() 或 sorted(nums)
    - Two Pointers: left = i + 1, right = len(nums) - 1
    - 三數之和 < 0 → left 往右移（讓總和變大）
    - 三數之和 > 0 → right 往左移（讓總和變小）
    """
    # TODO(human): 從頭實作你的解法
    nums.sort()
    result = [] 
    for i in range(len(nums)) :
        if i > 0 and nums[i] == nums[ i - 1 ]:
             continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            if nums[i] + nums[l] + nums[r] < 0:
                l += 1

            elif nums[i] + nums[l]+ nums[r] > 0:
                 r -= 1
            else:
                result.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
    return result


# 本地測試
if __name__ == "__main__":
    # Test Case 1: 標準案例
    nums1 = [-1, 0, 1, 2, -1, -4]
    result1 = threeSum(nums1)
    print(f"Input: {nums1}")
    print(f"Output: {result1}")
    print(f"Expected: [[-1,-1,2],[-1,0,1]] (順序可能不同)")
    print()

    # Test Case 2: 沒有答案
    nums2 = [0, 1, 1]
    result2 = threeSum(nums2)
    print(f"Input: {nums2}")
    print(f"Output: {result2}")
    print(f"Expected: []")
    print()

    # Test Case 3: 全部都是 0
    nums3 = [0, 0, 0]
    result3 = threeSum(nums3)
    print(f"Input: {nums3}")
    print(f"Output: {result3}")
    print(f"Expected: [[0,0,0]]")
    print()

    # Test Case 4: 有很多重複
    nums4 = [-2, 0, 0, 2, 2]
    result4 = threeSum(nums4)
    print(f"Input: {nums4}")
    print(f"Output: {result4}")
    print(f"Expected: [[-2,0,2]]")
