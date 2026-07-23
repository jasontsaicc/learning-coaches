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
    ([4, 5, 6, 7, 0, 1, 2], 0, 4),
    ([4, 5, 6, 7, 0, 1, 2], 3, -1),      # not present
    ([4, 5, 6, 7, 0, 1, 2], 4, 0),       # first cell
    ([4, 5, 6, 7, 0, 1, 2], 2, 6),       # last cell
    ([1], 0, -1),                        # single element, miss
    ([1], 1, 0),                         # single element, hit
    ([3, 1], 1, 1),
    ([3, 1], 3, 0),
    ([1, 2, 3, 4, 5], 4, 3),             # not rotated at all
    ([1, 2, 3, 4, 5], 9, -1),
    ([-4, -2, 0, 2, -9, -7], -9, 4),     # negatives
]


@pytest.mark.parametrize("nums,target,expected", BASIC)
def test_basic(sol, nums, target, expected):
    assert sol.search(nums, target) == expected


@pytest.mark.parametrize("k", range(9))
def test_every_rotation_finds_every_element(sol, k):
    """Hostile input: every rotation x every element must be found."""
    base = [1, 3, 5, 7, 9, 11, 13, 15, 17]
    nums = rotate(base, k)
    for i, v in enumerate(nums):
        assert sol.search(nums, v) == i


@pytest.mark.parametrize("k", range(9))
def test_every_rotation_rejects_missing(sol, k):
    """Values that are not in the array must return -1, not a stray index."""
    base = [1, 3, 5, 7, 9, 11, 13, 15, 17]
    nums = rotate(base, k)
    for v in (0, 4, 10, 18):
        assert sol.search(nums, v) == -1


class CountingList(list):
    """Complexity tripwire.

    Counts index reads. A binary search touches ~2 cells per iteration
    (~2*log2(n)); a linear scan touches n. Iterating the whole list
    (`nums.index(t)`, `for x in nums`, `t in nums`) is O(n) by definition,
    so it hard-fails.
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

    assert sol.search(nums, 0) == 40_000

    budget = 100  # 2*log2(10^5) ~= 34; generous headroom, still 1000x under O(n)
    assert nums.reads <= budget, (
        f"read {nums.reads} cells for n={n}: that is not O(log n)"
    )


@pytest.mark.timeout(5)
def test_large_n_miss_is_logarithmic(sol):
    n = 100_000
    base = [2 * i for i in range(n)]      # all even -> odd target is absent
    nums = CountingList(rotate(base, 40_000))

    assert sol.search(nums, 12_345) == -1

    assert nums.reads <= 100
