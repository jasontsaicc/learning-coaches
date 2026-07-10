# LeetCode #704 Binary Search
# Sorted array + target. Return the index of target, or -1 if not found.
# Must be O(log n).

from typing import List


def search(nums: List[int], target: int) -> int:
    l = 0
    r = len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            r = mid - 1
        else:
            l = mid + 1

    return -1


# --- tests ---
if __name__ == "__main__":
    assert search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert search([5], 5) == 0
    assert search([5], -5) == -1
    assert search([2, 5], 5) == 1
    assert search([1, 2, 3, 4, 5, 6, 7, 8], 1) == 0  # first element
    assert search([1, 2, 3, 4, 5, 6, 7, 8], 8) == 7  # last element
    print("all pass")
