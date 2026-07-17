from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Bridge:
        #   1. What am I computing?  -> is target in matrix -> bool
        #   2. Brute force?          -> visit every cell, O(m*n)
        #   3. How do I shrink?      -> the matrix, read row-major, IS a sorted
        #                               1-D array of length m*n. Binary search it.
        #                               Translate idx -> (row, col) on each read.
        #   4. When do I stop?       -> found target, or the search range is empty.
        #
        # TODO: write it.
        m = len(matrix)
        n = len(matrix[0])
        l = 0
        r = m * n - 1
        while l <= r:
            mid = (l + r) // 2
            row = mid // n
            col = mid % n
            val = matrix[row][col]
            if val == target:
                return True
            elif val < target:
                l = mid + 1
            else:
                r = mid - 1
        return False
