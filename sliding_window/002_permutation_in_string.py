# Problem: Permutation in String (#567)
# Pattern: Sliding Window (fixed window + frequency match)
# Step: D/E — student jumped straight to the optimal solution

# TODO: one import line is missing — Counter comes from where?

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        k = len(s1)  # window width
        target = Counter(s1)
        window = Counter(s2[:k])
        if window == target:
            return True
        for right in range(k, len(s2)):
            ch_in = s2[right]
            window[ch_in] += 1

            ch_out = s2[right - k]
            window[ch_out] -= 1
            if window[ch_out] == 0:
                del window[ch_out]
            if window == target:
                return True

        return False
