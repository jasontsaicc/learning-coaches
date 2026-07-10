"""
LeetCode 238. Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/

Given an integer array nums, return an array answer such that answer[i]
is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using
the division operator.

Example 1:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Constraints:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

---
中文翻譯：
給你一個整數陣列 nums，回傳一個陣列 answer，其中 answer[i] 等於 nums 中除了 nums[i] 以外所有元素的乘積。
必須用 O(n) 時間，而且不能用除法！
"""

def productExceptSelf(nums: list[int]) -> list[int]:
    """
    思路：
    1. 先從左掃到右，算出每個位置「左邊的乘積」存到 left 陣列
    2. 再從右掃到左，算出每個位置「右邊的乘積」存到 right 陣列
    3. 最後 result[i] = left[i] × right[i]

    提示：
    - 左邊沒有人的時候，乘積當作 1
    - 右邊沒有人的時候，乘積也當作 1
    - left[i] 是「i 左邊所有數字的乘積」，不包含 nums[i] 自己
    """
    # TODO(human): 實作你的解法
    left = []
    for i in range(len(nums)):
        if i == 0:
            left.append(1)
        else:
            left.append(left[i-1] * nums[i-1])
    right = [0] * len(nums)
    for i in range(len(nums)-1, -1, -1):
        if i == len(nums) -1:
            right[i] = 1
        else:
            right[i] = right[i+1] * nums[i+1]
    result = []
    for i in range(len(nums)):
        result.append(left[i] * right[i])
    return result


# 本地測試
if __name__ == "__main__":
    # 測試案例 1
    nums1 = [1, 2, 3, 4]
    result1 = productExceptSelf(nums1)
    print(f"輸入: {nums1}")
    print(f"輸出: {result1}")
    print(f"預期: [24, 12, 8, 6]")
    print(f"通過: {result1 == [24, 12, 8, 6]}")
    print()

    # 測試案例 2
    nums2 = [-1, 1, 0, -3, 3]
    result2 = productExceptSelf(nums2)
    print(f"輸入: {nums2}")
    print(f"輸出: {result2}")
    print(f"預期: [0, 0, 9, 0, 0]")
    print(f"通過: {result2 == [0, 0, 9, 0, 0]}")
    print()

    # 測試案例 3：只有兩個數字
    nums3 = [2, 3]
    result3 = productExceptSelf(nums3)
    print(f"輸入: {nums3}")
    print(f"輸出: {result3}")
    print(f"預期: [3, 2]")
    print(f"通過: {result3 == [3, 2]}")
