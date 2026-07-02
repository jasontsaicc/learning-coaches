# Problem: Longest Substring Without Repeating Characters (LeetCode #3)
# Pattern: Sliding Window (Dynamic Window)
# Step: D (Brute Force) — write your solution below
#
# Goal: Return the length of the longest substring without repeating characters.
#
# Examples:
#   lengthOfLongestSubstring("abcabcbb") -> 3
#   lengthOfLongestSubstring("bbbbb")    -> 1
#   lengthOfLongestSubstring("pwwkew")   -> 3
#   lengthOfLongestSubstring("")         -> 0


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        best = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                substring = s[i : j + 1]
                if len(set(substring)) == len(substring):
                    best = max(best, len(substring))
        return best


# ---- Tests ----
if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("au", 2),
        ("a", 1),
    ]
    for s, expected in test_cases:
        result = sol.lengthOfLongestSubstring(s)
        status = "✅" if result == expected else "❌"
        print(
            f"{status}  lengthOfLongestSubstring({s!r}) = {result}  (expected {expected})"
        )
