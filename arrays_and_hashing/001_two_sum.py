"""
LeetCode 1. Two Sum
https://leetcode.com/problems/two-sum/

難度：Easy
主題：Arrays & Hashing

== 題目說明 ==
給你一個整數陣列 nums 和一個目標值 target
找出陣列中兩個數字相加等於 target 的 index
假設每個題目只有一個答案，同一個元素不能用兩次

== 範例 ==
輸入：nums = [2, 7, 11, 15], target = 9
輸出：[0, 1]
解釋：nums[0] + nums[1] = 2 + 7 = 9

== DevOps 比喻 ==
想像你在找兩台 server，它們的 CPU 使用率加起來剛好等於 100%
你有一份 server 清單，要找出是哪兩台

== 你要實作的函數 ==
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    """
    找出兩個數字的 index，使得它們相加等於 target

    Args:
        nums: 整數陣列
        target: 目標總和

    Returns:
        包含兩個 index 的 list
    """
    my_dict = {}
    for i, v in enumerate(nums):
        val = target - v
        
        if val in my_dict:
            return [my_dict[val], i]
        my_dict[v] =i


    


# ========== 測試區 ==========
if __name__ == "__main__":
    # 測試案例 1：基本情況
    result1 = two_sum([2, 7, 11, 15], 9)
    print(f"Test 1: {result1}")  # 預期：[0, 1] 或 [1, 0]

    # 測試案例 2：答案在中間
    result2 = two_sum([3, 2, 4], 6)
    print(f"Test 2: {result2}")  # 預期：[1, 2] 或 [2, 1]

    # 測試案例 3：相同的數字
    result3 = two_sum([3, 3], 6)
    print(f"Test 3: {result3}")  # 預期：[0, 1] 或 [1, 0]
