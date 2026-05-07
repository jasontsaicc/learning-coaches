# Problem: Valid Palindrome (LeetCode 125)
# Pattern: Two Pointers
# Link: https://neetcode.io/problems/is-palindrome

# ================================================================
# Step D: Brute Force — write your first solution below
# ================================================================
# Hint: The most intuitive brute force is:
#   1. Filter out non-alphanumeric chars
#   2. Convert to lowercase
#   3. Compare the filtered string with its reverse
#
# Useful Python helpers:
#   - ch.isalnum()      # True if ch is letter or digit
#   - ch.lower()        # lowercase version of ch
#   - s[::-1]           # reverse a string
#
# Don't worry about O(1) space yet — brute force is allowed O(n).


class SolutionBrute:
    def isPalindrome(self, s: str) -> bool:
        filtered = ""
        for ch in s:
            if ch.isalnum():
                filtered += ch.lower()
        return filtered == filtered[::-1]


# ================================================================
# Step E: Optimal Solution (Two Pointers) — O(1) space
# ================================================================
# Strategy:
#   1. left = 0, right = len(s) - 1
#   2. while left < right:
#        - skip non-alphanumeric from left (left += 1)
#        - skip non-alphanumeric from right (right -= 1)
#        - compare s[left].lower() vs s[right].lower()
#          - not equal → return False
#          - equal → move both pointers inward
#   3. return True
#
# Watch out:
#   - "=" (assign) vs "==" (compare). You want "==" for comparison.
#   - Skip loops need their own `while` inside the outer while,
#     or you'll compare a punctuation char.


class SolutionOptimal:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True


# ================================================================
# Test cases
# ================================================================
if __name__ == "__main__":
    tests = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("", True),
        ("0P", False),  # edge: digit vs letter
        ("a", True),
    ]

    print("--- Brute Force ---")
    brute = SolutionBrute()
    for s, expected in tests:
        got = brute.isPalindrome(s)
        mark = "✅" if got == expected else "❌"
        print(f"{mark} isPalindrome({s!r}) = {got}  (expected {expected})")

    print("\n--- Optimal (Two Pointers) ---")
    opt = SolutionOptimal()
    for s, expected in tests:
        got = opt.isPalindrome(s)
        mark = "✅" if got == expected else "❌"
        print(f"{mark} isPalindrome({s!r}) = {got}  (expected {expected})")
