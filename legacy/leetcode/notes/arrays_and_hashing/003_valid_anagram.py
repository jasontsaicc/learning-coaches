"""
LeetCode 242. Valid Anagram

題目：給定兩個字串 s 和 t，判斷 t 是否為 s 的 anagram（易位詞）

範例：
    s = "anagram", t = "nagaram" → True
    s = "rat", t = "car" → False
"""


def isAnagram(s: str, t: str) -> bool:
    """
    判斷 t 是否為 s 的 anagram

    思路：
    1. 先檢查長度（early return）
    2. 用一個 dict 計數：s 的字母 +1，t 的字母 -1
    3. 最後檢查是否全部歸零

    Args:
        s: 第一個字串
        t: 第二個字串

    Returns:
        bool: 如果 t 是 s 的 anagram 回傳 True，否則 False
    """
    # TODO(human): 實作你的解法
    # 提示：
    # 1. 先檢查 len(s) 和 len(t)
    # 2. 建立一個空 dict: count = {}
    # 3. 遍歷 s，對每個字母 +1
    # 4. 遍歷 t，對每個字母 -1
    # 5. 檢查 count 的所有值是否為 0
    
    if len(s) != len(t):
        return False
    my_dict = {}
    for i in s:
        my_dict[i] = my_dict.get(i, 0) + 1
    for j in t:
        my_dict[j] = my_dict.get(j, 0) - 1
    for v in my_dict.values():
        if v != 0:
            return False
    return True


# 測試
if __name__ == "__main__":
    # 測試案例
    test_cases = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("aab", "aba", True),
        ("aab", "aaa", False),
        ("", "", True),           # edge case: 空字串
        ("a", "ab", False),       # edge case: 長度不同
    ]

    print("Testing isAnagram:")
    print("-" * 40)

    for s, t, expected in test_cases:
        result = isAnagram(s, t)
        status = "✅" if result == expected else "❌"
        print(f'{status} isAnagram("{s}", "{t}")')
        print(f'   Expected: {expected}, Got: {result}')
        print()
