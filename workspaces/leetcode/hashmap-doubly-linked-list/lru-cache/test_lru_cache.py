import pytest

from solution import LRUCache


def test_leetcode_example():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)          # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)          # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    assert cache.get(1) == 1
    cache.put(2, 2)           # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_put_existing_key_updates_value_and_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)          # update existing key, 1 becomes MRU
    cache.put(3, 3)           # must evict key 2 (LRU), not key 1
    assert cache.get(1) == 10
    assert cache.get(2) == -1
    assert cache.get(3) == 3


def test_get_missing_key_does_not_disturb_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(99) == -1   # miss must not touch the chain
    cache.put(3, 3)               # key 1 is still LRU, should still be evicted
    assert cache.get(1) == -1
    assert cache.get(2) == 2
    assert cache.get(3) == 3


def test_repeated_get_collapses_to_single_node():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    for _ in range(5):
        cache.get(1)
    cache.put(3, 3)      # key 2 is LRU; repeated get(1) must not create duplicates
    assert cache.get(1) == 1
    assert cache.get(2) == -1


@pytest.mark.timeout(5)
def test_large_n_repeated_access_stays_o1():
    """Every get() must stay O(1) regardless of cache size.
    An O(n) list-scan-and-move design times out here."""
    capacity = 2000
    cache = LRUCache(capacity)
    for k in range(capacity):
        cache.put(k, k * 10)
    # key 0 is now the least-recently-used entry; hammer it.
    for _ in range(500_000):
        assert cache.get(0) == 0
    # get(0) refreshes key 0 to MRU every time, so key 1 is the real LRU now.
    cache.put(capacity, 999)
    assert cache.get(1) == -1
    assert cache.get(0) == 0
