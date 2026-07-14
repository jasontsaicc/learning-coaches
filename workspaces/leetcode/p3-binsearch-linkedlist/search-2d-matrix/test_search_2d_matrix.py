import time

import pytest

from solution import Solution


@pytest.fixture
def sol():
    return Solution()


BASIC = [
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13, False),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 1, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 60, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 0, False),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 61, False),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 10, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 20, True),
]


@pytest.mark.parametrize("matrix,target,expected", BASIC)
def test_basic(sol, matrix, target, expected):
    assert sol.searchMatrix(matrix, target) is expected


EDGE = [
    ([[1]], 1, True),
    ([[1]], 2, False),
    ([[1, 3]], 3, True),
    ([[1, 3]], 2, False),
    ([[1], [3], [5]], 5, True),
    ([[1], [3], [5]], 4, False),
    # non-square: 2 rows x 5 cols. Catches row = idx // m instead of idx // n.
    ([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]], 7, True),
    ([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]], 10, True),
    # non-square: 5 rows x 2 cols.
    ([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], 9, True),
    ([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], 11, False),
]


@pytest.mark.parametrize("matrix,target,expected", EDGE)
def test_edge(sol, matrix, target, expected):
    assert sol.searchMatrix(matrix, target) is expected


@pytest.mark.timeout(20)
def test_large_n(sol):
    """Complexity tripwire: 1000x1000 matrix, 200 lookups.

    O(log(m*n)) per lookup -> ~4k comparisons total.
    O(m*n) per lookup      -> 2*10^8 cell visits. Blows the budget.
    """
    m, n = 1000, 1000
    matrix = [[r * n + c for c in range(n)] for r in range(m)]  # 0 .. 999_999

    targets = [i * 5000 for i in range(200)]  # all present, spread across the matrix

    start = time.perf_counter()
    for t in targets:
        assert sol.searchMatrix(matrix, t) is True
    assert sol.searchMatrix(matrix, -1) is False
    assert sol.searchMatrix(matrix, m * n) is False
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s for 202 lookups -> not O(log(m*n))"
