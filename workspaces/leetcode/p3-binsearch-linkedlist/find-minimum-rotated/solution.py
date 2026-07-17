from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Q1: what am I looking for?
        #     -> the first element of the second (low) segment = the cliff bottom
        #

        # Q3: invariant -- the answer always lives in [l, r]

        # Q5: stop when the range collapses to a single cell

        # Q2: check -- compare nums[mid] against nums[r]

        # Q4: mid has a witness (nums[r]) -> safe to discard mid

        # Q4: mid has no witness -- it could BE the answer -> keep it

        # Q5: l == r, that cell is the answer
        l = 0
        r = len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                r = mid
        return nums[l]
