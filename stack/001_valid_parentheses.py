# Problem: Valid Parentheses (#20)
# Pattern: Stack (LIFO matching)
# Step: D — write your stack solution below
#
# 演算法回顧：
#   掃每個字元：
#     開括號 → push 進 stack
#     閉括號 → 看 stack 頂端配不配；配 → pop，不配/空 → return False
#   掃完 → stack 空才 return True
#
# 小工具：pairs = { ')': '(', ']': '[', '}': '{' }  # 閉 → 開


class Solution:
    def isValid(self, s: str) -> bool:
        # your code here
        stack = []
        pairs = {")": "(", "]": "[", "}": "{"}

        for c in s:
            if c in pairs:
                if not stack or stack[-1] != pairs[c]:
                    return False
                stack.pop()
            else:
                stack.append(c)
        return not stack


# ---- quick tests (跑這個檔就會驗證) ----
if __name__ == "__main__":
    sol = Solution()
    cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("(", False),
        (")", False),
        ("((", False),
    ]
    for s, expected in cases:
        got = sol.isValid(s)
        mark = "✅" if got == expected else "❌"
        print(f"{mark}  isValid({s!r}) = {got}  (expected {expected})")
