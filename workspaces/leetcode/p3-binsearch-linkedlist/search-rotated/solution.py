from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Q1: 我在找什麼? -> target 的 index,找不到回 -1
        # Q3: 不變量 -> 答案(若存在)永遠在 [l, r]
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1  # 區間縮成空,沒找到
