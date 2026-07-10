"""
LeetCode 125. Valid Palindrome
https://leetcode.com/problems/valid-palindrome/

A phrase is a palindrome if, after converting all uppercase letters into
lowercase letters and removing all non-alphanumeric characters, it reads
the same forward and backward. Alphanumeric characters include letters
and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.

---
中文翻譯：
給你一個字串 s，判斷它是不是回文。
- 忽略大小寫（A 和 a 視為相同）
- 忽略非字母數字的字元（空格、標點符號都跳過）
"""


def isPalindrome(s: str) -> bool:
    """
    思路（Two Pointers）：
    1. 左指標從頭開始，右指標從尾巴開始
    2. 跳過非字母數字的字元
    3. 比較時忽略大小寫（用 .lower()）
    4. 如果不一樣就 return False
    5. 如果指標相遇都沒問題，return True

    你會用到的工具：
    - s[left] / s[right] → 取得指標位置的字元
    - .isalnum() → 判斷是不是字母或數字
    - .lower() → 轉成小寫
    - left += 1 / right -= 1 → 移動指標
    """
    # TODO(human): 實作 Two Pointers 
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True


# 本地測試
if __name__ == "__main__":
    test_cases = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("a", True),
        ("ab", False),
    ]

    for s, expected in test_cases:
        result = isPalindrome(s)
        status = "✓" if result == expected else "✗"
        print(f"{status} isPalindrome(\"{s}\") = {result}, expected {expected}")
