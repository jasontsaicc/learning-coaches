"""#208 Implement Trie (Prefix Tree)(速刷)

跑法:  python3 drill.py

  insert(word):把字存進去
  search(word):這個字存過嗎(整個字)
  startsWith(prefix):有存過的字用這個開頭嗎

一句話:
  三個方法都是一格一格往下走,差別只在「路斷了」和「走完了」各做什麼
"""


class TrieNode:
    def __init__(self):
        self.children = {}  # 字元 -> 下一格 TrieNode
        self.end = False  # 有沒有一個字剛好在這格結束


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        # ── 打在這裡 ──
        pass

    def search(self, word):
        # ── 打在這裡 ──
        pass

    def startsWith(self, prefix):
        # ── 打在這裡 ──
        pass


# ── 以下不用改 ────────────────────────────────────────────
WORDS = ["app", "apple", "at"]

CASES = [
    # (先存哪些字, 方法, 參數, 期望, 這個 case 在考什麼)
    (WORDS, "search", "app", True, "a-p-p 走完,end=True"),
    (WORDS, "search", "ap", False, "a-p 走完,end=False"),
    (WORDS, "startsWith", "ap", True, "前綴只要路走得通"),
    (WORDS, "search", "apple", True, "跟 app 共用開頭,兩個字都在"),
    (WORDS, "search", "apples", False, "比存的字長,走到一半路斷"),
    (WORDS, "startsWith", "b", False, "第一格路就斷"),
    (WORDS, "search", "at", True, "在 a 分岔的另一條路"),
    (WORDS, "startsWith", "apple", True, "整個字也算前綴"),
    (["apple"], "search", "app", False, "題目原例:只存 apple,app 只是路過"),
]

if __name__ == "__main__":
    passed = 0
    for words, method, arg, want, why in CASES:
        trie = Trie()
        for word in words:
            trie.insert(word)
        got = getattr(trie, method)(arg)
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {method}({arg!r})  want={want} got={got}   {why}")
    print(f"{passed}/{len(CASES)}")
