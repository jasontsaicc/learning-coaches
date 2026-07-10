"""
LeetCode 167. Two Sum II - Input Array Is Sorted
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Given a 1-indexed array of integers numbers that is already sorted in
non-decreasing order, find two numbers such that they add up to a
specific target number. Let these two numbers be numbers[index1] and
numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one
as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution.
You may not use the same element twice.

Your solution must use only constant extra space.

Example 1:
    Input: numbers = [2,7,11,15], target = 9
    Output: [1,2]
    Explanation: The sum of 2 and 7 is 9.
    Therefore, index1 = 1, index2 = 2. We return [1, 2].

Example 2:
    Input: numbers = [2,3,4], target = 6
    Output: [1,3]
    Explanation: The sum of 2 and 4 is 6.
    Therefore index1 = 1, index2 = 3. We return [1, 3].

Example 3:
    Input: numbers = [-1,0], target = -1
    Output: [1,2]
    Explanation: The sum of -1 and 0 is -1.
    Therefore index1 = 1, index2 = 2. We return [1, 2].

Constraints:
    - 2 <= numbers.length <= 3 * 10^4
    - -1000 <= numbers[i] <= 1000
    - numbers is sorted in non-decreasing order.
    - -1000 <= target <= 1000
    - The tests are generated such that there is exactly one solution.

---
中文翻譯：
給你一個「已排序」的整數陣列 numbers（1-indexed），找出兩個數字相加等於 target。
回傳這兩個數字的 index（注意是 1-indexed，不是 0-indexed！）

重點限制：只能用 O(1) 額外空間（不能用 Hash Map！）
"""

from typing import List


def twoSum(numbers: List[int], target: int) -> List[int]:
    """
    思路（你剛剛已經想出來了！）：
    1. 左指針從最左邊開始，右指針從最右邊開始
    2. 如果總和太大 → ?
    3. 如果總和太小 → ?
    4. 如果剛好 → ?

    注意：回傳的是 1-indexed！（要 +1）
    """
    l, r = 0, len(numbers) - 1
    while l < r:
        if target > numbers[l] + numbers[r]:
            l += 1
        elif target < numbers[l] + numbers[r]:
            r -= 1
        else:
            return [l+1, r+1]
    return False       
    


# 本地測試
if __name__ == "__main__":
    # Test 1: 基本測試
    result1 = twoSum([2, 7, 11, 15], 9)
    print(f"Test 1: {result1}")  # 預期 [1, 2]

    # Test 2: 答案在兩端
    result2 = twoSum([2, 3, 4], 6)
    print(f"Test 2: {result2}")  # 預期 [1, 3]

    # Test 3: 負數
    result3 = twoSum([-1, 0], -1)
    print(f"Test 3: {result3}")  # 預期 [1, 2]

    # Test 4: 較長的 array
    result4 = twoSum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19)
    print(f"Test 4: {result4}")  # 預期 [9, 10]
