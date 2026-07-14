import pytest

from solution import Solution


@pytest.fixture
def sol():
    return Solution()


def rotate(sorted_list, k):
    """Rotate right by k: [0,1,2,3] rotated 1 -> [3,0,1,2]."""
    k %= len(sorted_list)
    return sorted_list[-k:] + sorted_list[:-k] if k else list(sorted_list)


BASIC = [
    ([3, 4, 5, 1, 2], 1),
    ([4, 5, 6, 7, 0, 1, 2], 0),
    ([11, 13, 15, 17], 11),          # not rotated at all
    ([2, 1], 1),
    ([1, 2], 1),                     # not rotated, size 2
    ([1], 1),                        # single element
    ([5, 1, 2, 3, 4], 1),            # minimum right after index 0
    ([2, 3, 4, 5, 1], 1),            # minimum at the last index
    ([-5, -3, -1, -9, -8], -9),      # negatives
]


@pytest.mark.parametrize("nums,expected", BASIC)
def test_basic(sol, nums, expected):
    assert sol.findMin(nums) == expected


@pytest.mark.parametrize("k", range(9))
def test_every_rotation(sol, k):
    """Hostile input: every possible rotation of the same array must work."""
    base = [1, 3, 5, 7, 9, 11, 13, 15, 17]
    assert sol.findMin(rotate(base, k)) == 1


class CountingList(list):
    """Complexity tripwire.

    Counts index reads. A binary search touches ~2 cells per iteration
    (~2*log2(n)); a linear scan touches n. Iterating the whole list
    (min(nums), `for x in nums`) is O(n) by definition, so it hard-fails.
    """

    def __init__(self, items):
        super().__init__(items)
        self.reads = 0

    def __getitem__(self, i):
        self.reads += 1
        return super().__getitem__(i)

    def __iter__(self):
        raise AssertionError(
            "scanning the whole array is O(n) -- the problem demands O(log n)"
        )


@pytest.mark.timeout(5)
def test_large_n_is_logarithmic(sol):
    n = 100_000
    base = list(range(n))
    nums = CountingList(rotate(base, 40_000))

    assert sol.findMin(nums) == 0

    budget = 100  # 2*log2(10^5) ~= 34; generous headroom, still 1000x under O(n)
    assert nums.reads <= budget, (
        f"read {nums.reads} cells for n={n}: that is not O(log n)"
    )
