# Problem: Evaluate Reverse Polish Notation (#150)
# Pattern: Stack (FILO — 最近兩個運算元)
# Mode: Drill — 冷寫，不看昨天的 code，不 autocomplete
#
# 規格回顧：
#   tokens 元素是「數字字串」或 "+ - * /"
#   數字   → push 進 stack
#   運算子 → pop 兩次、算、結果 push 回去
#   掃完   → stack 只剩一個元素 = 答案
#
# ⚠️ 兩個地雷自己留意（不提示你怎麼處理，自己想）：
#   1. "+ - * /" 算的時候，兩個運算元的「順序」會不會有差？
#   2. 題目除法向 0 取整（不是 Python 預設的向下取整）


from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for token in tokens:
            if token in {"+", "-", "*", "/"}:
                r = stack.pop()
                l = stack.pop()
                if token == "+":
                    stack.append(l + r)
                elif token == "-":
                    stack.append(l - r)
                elif token == "*":
                    stack.append(l * r)
                else:
                    stack.append(int(l / r))
            else:
                stack.append(int(token))
        return stack.pop()


# ---- quick tests (跑這個檔就會驗證) ----
if __name__ == "__main__":
    sol = Solution()
    cases = [
        (["2", "1", "+", "3", "*"], 9),  # (2+1)*3
        (["4", "13", "5", "/", "+"], 6),  # 4 + (13/5)=4+2
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
        (["3", "4", "-"], -1),  # 順序地雷：3-4 還是 4-3？
        (["6", "-132", "/"], 0),  # 向 0 取整地雷
    ]
    for toks, expected in cases:
        got = sol.evalRPN(toks)
        mark = "✅" if got == expected else "❌"
        print(f"{mark}  evalRPN({toks}) = {got}  (expected {expected})")
