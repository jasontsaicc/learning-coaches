"""
LeetCode 347. Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Example 1:
    Input: nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]

Example 2:
    Input: nums = [1], k = 1
    Output: [1]

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - k is in the range [1, the number of unique elements in the array]
    - It is guaranteed that the answer is unique.

---
中文翻譯：
給你一個整數陣列 nums 和一個整數 k，回傳出現頻率最高的 k 個元素。
答案可以用任何順序回傳。
"""

from typing import List
from collections import Counter

def topKFrequent(nums: List[int], k: int) -> List[int]:
    """
    解法一：笨方法（已完成 ✅）
    用 dict 計數 → 按 value 排序 keys → 取前 k 個
    時間複雜度：O(n log n)
    """
    my_dict = {}
    for i in nums:
        if i not in my_dict:
            my_dict[i] = 1
        else:
            my_dict[i] += 1
    sorted_key = sorted(my_dict.keys(), key=lambda x: my_dict[x], reverse=True)
    return sorted_key[:k]


def topKFrequent_counter(nums: List[int], k: int) -> List[int]:
    """
    解法三：用 Counter.most_common()

    思路：
    1. 用 Counter(nums) 一行完成計數
    2. 用 .most_common(k) 取得前 k 個最常見的 [(元素, 次數), ...]
    3. 用 list comprehension 只取出元素

    時間複雜度：O(n log n) — most_common 內部還是用排序
    """
    count = Counter(nums)
    most_common = count.most_common(k)
    result = [i[0] for i in most_common]
    return result


def topKFrequent_bucket(nums: List[int], k: int) -> List[int]:
    """
    解法四：Bucket Sort（桶排序）

    思路：
    1. 先計數（用 dict 或 Counter）
    2. 建立 buckets 陣列，長度 = len(nums) + 1
       - buckets[i] = 出現 i 次的元素列表
    3. 把每個元素放進對應次數的桶子
    4. 從後往前遍歷 buckets，撿 k 個元素

    時間複雜度：O(n) — 不需要排序！
    空間複雜度：O(n) — 需要額外的 buckets 陣列

    範例：
    nums = [1,1,1,2,2,3], k = 2
    計數：{1: 3, 2: 2, 3: 1}
    桶子：
        buckets[0] = []
        buckets[1] = [3]      ← 3 出現 1 次
        buckets[2] = [2]      ← 2 出現 2 次
        buckets[3] = [1]      ← 1 出現 3 次
        buckets[4] = []
        buckets[5] = []
        buckets[6] = []
    從後往前撿 2 個：[1, 2] ✅
    """
    # TODO(human): 實作 Bucket Sort 解法
    pass


def topKFrequent_v2(nums: List[int], k: int) -> List[int]:
    """
    解法二：用 .items() 排序

    思路：
    1. 用 dict 計數
    2. 用 .items() 拿到 [(key, value), ...] 的 list
    3. 用 sorted() + lambda 按 value（次數）排序
    4. 用 list comprehension 只取 key

    提示：
    - my_dict.items() 會給你 [(1, 3), (2, 2), (3, 1)] 這種格式
    - sorted() 的 key=lambda x: x[?] 要填對的 index
    - 最後用 [x[?] for x in ...] 取出 key
    """
    # Step 1: 計數
    my_dict = {}
    for i in nums:
        if i not in my_dict:
            my_dict[i] = 1
        else:
            my_dict[i] += 1

    # Step 2: 變成 [(key, value), ...] 格式
    items = my_dict.items()

    # Step 3: 按 value（次數）從大到小排序
    sorted_items = sorted(items, key=lambda x: x[1], reverse=True)

    # Step 4: 取前 k 個的 key
    result = [x[0] for x in sorted_items[:k]]

    return result
    


# 本地測試
if __name__ == "__main__":
    # 測試資料
    test_cases = [
        ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
        ([1], 1, [1]),
        ([404, 500, 404, 200, 404, 500, 200, 404, 404], 2, [404, 500]),
    ]

    print("=== 解法一：笨方法 ===")
    for i, (nums, k, expected) in enumerate(test_cases, 1):
        result = topKFrequent(nums, k)
        status = "✅" if set(result) == set(expected) else "❌"
        print(f"測試 {i}: {result} {status}")

    print("\n=== 解法二：.items() 版本 ===")
    for i, (nums, k, expected) in enumerate(test_cases, 1):
        result = topKFrequent_v2(nums, k)
        status = "✅" if result and set(result) == set(expected) else "❌"
        print(f"測試 {i}: {result} {status}")
