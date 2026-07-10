"""
LeetCode 349. Intersection of Two Arrays
https://leetcode.com/problems/intersection-of-two-arrays/

Given two integer arrays nums1 and nums2, return an array of their intersection.
Each element in the result must be unique and you may return the result in any order.

Example 1:
Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]

Example 2:
Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [9,4]
Explanation: [4,9] is also accepted.

Constraints:
- 1 <= nums1.length, nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 1000

---
中文翻譯：
給你兩個整數陣列 nums1 和 nums2，回傳它們的交集。
結果中每個元素必須是唯一的（不重複），順序不重要。
"""

from typing import List


def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    思路 (Your plan):
    1. Convert nums1 to set
    2. Convert nums2 to set
    3. Use & to find common items
    4. Convert result back to list

    Hint:
    - set(some_list) converts list to set
    - set_a & set_b finds intersection
    - list(some_set) converts set to list
    """
    # TODO(human): Write your solution here!
    set_nums1 = set(nums1)
    set_nums2 = set(nums2)
    result = set_nums1 & set_nums2
    return list(result)


# Local tests
if __name__ == "__main__":
    # Test 1
    result1 = intersection([1, 2, 2, 1], [2, 2])
    print(f"Test 1: {result1}")  # Expected: [2]

    # Test 2
    result2 = intersection([4, 9, 5], [9, 4, 9, 8, 4])
    print(f"Test 2: {result2}")  # Expected: [9, 4] or [4, 9]

    # Test 3: No common items
    result3 = intersection([1, 2, 3], [4, 5, 6])
    print(f"Test 3: {result3}")  # Expected: []

    # Test 4: All same
    result4 = intersection([1, 1, 1], [1, 1])
    print(f"Test 4: {result4}")  # Expected: [1]
