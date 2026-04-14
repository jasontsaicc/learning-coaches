from typing import List


class Solution:

    def encode(self, strs: List[str]) -> str:
        result = ""
        for s in strs:
            result += str(len(s)) + "#" + s
        return result

    def decode(self, s: str) -> List[str]:
        result = []
        i = 0
        while i < len(s):
            j = s.find("#", i)
            l = int(s[i:j])
            result.append(s[j + 1: j + 1 + l])
            i = j + 1 + l
        return result


# --- Test ---
sol = Solution()

tests = [
    ["hi", "bye"],
    [""],
    [],
    ["h#i", "bye"],
    ["hello world!!"],
]

for t in tests:
    encoded = sol.encode(t)
    decoded = sol.decode(encoded)
    status = "PASS" if decoded == t else "FAIL"
    print(f"{status} | input={t} | encoded='{encoded}' | decoded={decoded}")
