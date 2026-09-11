"""為什麼 self.ans 不用宣告,ans 要 nonlocal

跑法:  python3 scope-demo.py

同一件事(內層函式想改外層的東西)五種寫法,只有一種會炸。
判準只有一條: 看 `=` 左邊有沒有 `.` 或 `[]`
"""


# ── A. 什麼都不宣告,直接寫 ans = ... ─────────────────────
def case_a():
    ans = 0

    def bump():
        ans = ans + 1        # ← = 左邊是「光禿禿的名字」

    bump()
    return ans


# ── B. nonlocal:明講「我要改外層那個」 ──────────────────
def case_b():
    ans = 0

    def bump():
        nonlocal ans
        ans = ans + 1

    bump()
    return ans, bump


# ── C. self.ans:= 左邊有 `.`,這不是換標籤 ───────────────
class CaseC:
    def run(self):
        self.ans = 0

        def bump():
            self.ans = self.ans + 1   # ← = 左邊是 self.ans,有 `.`

        bump()
        return self.ans, bump


# ── D. 只讀不寫 ────────────────────────────────────────
def case_d():
    ans = 41

    def peek():
        return ans + 1       # 沒有 = ,純讀取

    return peek()


# ── E. list 當盒子:跟 C 同一招,= 左邊有 [] ───────────────
def case_e():
    ans = [0]

    def bump():
        ans[0] = ans[0] + 1  # ← = 左邊是 ans[0],不是 ans

    bump()
    return ans[0]


def show(name, fn):
    try:
        out = fn()
        val, inner = out if isinstance(out, tuple) else (out, None)
        extra = ""
        if inner is not None:
            extra = (f"   內層 co_varnames={inner.__code__.co_varnames} "
                     f"co_freevars={inner.__code__.co_freevars}")
        print(f"  {name:<26} -> {val}{extra}")
    except Exception as e:
        print(f"  {name:<26} -> X {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("\n想把外層的 ans 從 0 加到 1:\n")
    show("A  什麼都不宣告", case_a)
    show("B  nonlocal ans", case_b)
    show("C  self.ans", CaseC().run)
    show("D  只讀不寫 (41+1)", case_d)
    show("E  ans[0] 當盒子", case_e)
    print("\n  co_varnames = 這個函式自己的區域變數")
    print("  co_freevars = 從外層借來的閉包變數 (closure cell)\n")
