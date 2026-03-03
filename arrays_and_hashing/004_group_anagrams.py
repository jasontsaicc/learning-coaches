"""
LeetCode 49. Group Anagrams
https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together.
You can return the answer in any order.

Example 1:
    Input: strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
    Input: strs = [""]
    Output: [[""]]

Example 3:
    Input: strs = ["a"]
    Output: [["a"]]

Constraints:
    - 1 <= strs.length <= 10^4
    - 0 <= strs[i].length <= 100
    - strs[i] consists of lowercase English letters.

---
中文翻譯：給定一個字串陣列，把所有 anagram 分組在一起
"""

from typing import List


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    """
    把 anagram 分組

    思路：
    1. 用「排序後的字串」當作 key（標籤）
       - "eat" → 排序 → "aet"
       - "tea" → 排序 → "aet"
       - 同樣的 key 就放同一組
    2. 用 dict 存分組：key = 標籤, value = 原始字串的 list
    3. 最後回傳所有 list

    提示：
    - sorted("eat") 回傳 ['a', 'e', 't']（是 list）
    - "".join(['a', 'e', 't']) 回傳 "aet"（變成字串當 key）
    - 如果 key 不存在，需要先建立空 list
    """
    # TODO(human): 從頭實作你的解法
    groups = {}
    for word in strs:
        sorted_word = sorted(word)
        str_word = "".join(sorted_word)

        if str_word  not in groups:
            groups[str_word] = []
        groups[str_word].append(word)
    
    return list(groups.values())

    


# 本地測試
if __name__ == "__main__":
    test_cases = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        ),
        ([""], [[""]]),
        (["a"], [["a"]]),
    ]

    print("Testing groupAnagrams:")
    print("-" * 50)

    for strs, expected in test_cases:
        result = groupAnagrams(strs)
        result_sorted = sorted([sorted(g) for g in result])
        expected_sorted = sorted([sorted(g) for g in expected])
        status = "✅" if result_sorted == expected_sorted else "❌"
        print(f'{status} groupAnagrams({strs})')
        print(f'   Got: {result}')
        print()
