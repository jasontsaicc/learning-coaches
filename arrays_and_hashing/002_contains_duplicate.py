"""
LeetCode 217: Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

給定一個整數陣列 nums，如果任何值出現至少兩次，回傳 True
如果每個元素都不同，回傳 False
"""

from typing import List


def contains_duplicate(nums: List[int]) -> bool:
    """
    檢查陣列中是否有重複的數字

    Args:
        nums: 整數陣列

    Returns:
        如果有重複回傳 True，否則回傳 False

    Example:
        >>> contains_duplicate([1, 2, 3, 1])
        True
        >>> contains_duplicate([1, 2, 3, 4])
        False
    """
    # TODO(human): 實作思路 A - 邊走邊記
    # 提示：
    # 1. 建立一個空的 set
    # 2. 遍歷每個數字
    # 3. 先查再存：如果在 set 裡 → 回傳 True，不在 → 加進 set
    # 4. 迴圈結束還沒回傳 → 代表什麼？
    my_set = set()
    for i in nums:
        if i in my_set:
            return True
        my_set.add(i)
    return False
    
    # more Pythonic
    return len(nums) > len(set(nus))



# 測試用例
if __name__ == "__main__":
    # 測試 1: 有重複
    test1 = [1, 2, 3, 1]
    print(f"Test 1: {test1} → {contains_duplicate(test1)}")  # 預期: True

    # 測試 2: 沒重複
    test2 = [1, 2, 3, 4]
    print(f"Test 2: {test2} → {contains_duplicate(test2)}")  # 預期: False

    # 測試 3: 全部重複
    test3 = [1, 1, 1, 1]
    print(f"Test 3: {test3} → {contains_duplicate(test3)}")  # 預期: True

    # 測試 4: 空陣列
    test4 = []
    print(f"Test 4: {test4} → {contains_duplicate(test4)}")  # 預期: False

    # 測試 5: 單一元素
    test5 = [1]
    print(f"Test 5: {test5} → {contains_duplicate(test5)}")  # 預期: False
