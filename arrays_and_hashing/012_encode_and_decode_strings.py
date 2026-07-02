# Problem: Encode and Decode Strings (LeetCode 271)
# Pattern: Arrays & Hashing — Delimiter Design (Length-Prefix)
# Step: D (Brute Force) — write your solution below

from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        # your code her
        result = ""
        for s in strs:
            result += str(len(s)) + "#" + s
        return result

    def decode(self, s: str) -> List[str]:
        # your code here
        result = []
        i = 0
        while i < len(s):
            j = s.find("#", i)
            length = int(s[i:j])
            result.append(s[j + 1 : j + 1 + length])

            i = j + 1 + length
        return result
