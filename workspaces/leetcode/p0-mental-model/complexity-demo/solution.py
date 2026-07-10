"""
時間複雜度 & 空間複雜度 - 親手感受！

跑這個檔案，觀察不同複雜度的差異
"""

import time


def measure_time(func, *args):
    """測量函數執行時間"""
    start = time.time()
    result = func(*args)
    end = time.time()
    return end - start, result


# ========================================
# O(1) - 常數時間：不管資料多大，都一樣快
# ========================================
def o1_example(data: dict, key: str):
    """
    比喻：飯店櫃檯直接查房號
    不管飯店有 10 間房還是 10000 間房，查詢時間一樣
    """
    return data.get(key)


# ========================================
# O(n) - 線性時間：資料越多，越慢
# ========================================
def on_example(data: list, target: str):
    """
    比喻：一間一間房敲門找人
    10 間房最多敲 10 次，10000 間房最多敲 10000 次
    """
    for item in data:
        if item == target:
            return True
    return False


# ========================================
# O(n²) - 平方時間：資料越多，慢到爆炸
# ========================================
def on2_example(data: list):
    """
    比喻：每個房客都要跟其他所有房客握手
    10 個人握 100 次，100 個人握 10000 次！
    """
    count = 0
    for i in data:
        for j in data:
            count += 1  # 模擬一次操作
    return count


# ========================================
# 實驗區 - 跑跑看！
# ========================================
if __name__ == "__main__":

    # 測試不同大小的資料
    sizes = [100, 1000, 10000]

    print("=" * 50)
    print("觀察：資料量變大，執行時間如何變化？")
    print("=" * 50)

    for n in sizes:
        print(f"\n📊 資料量 n = {n}")
        print("-" * 30)

        # 準備測試資料
        test_list = list(range(n))
        test_dict = {i: f"value_{i}" for i in range(n)}

        # O(1) 測試
        t1, _ = measure_time(o1_example, test_dict, n - 1)
        print(f"O(1)  dict 查詢: {t1:.6f} 秒")

        # O(n) 測試
        t2, _ = measure_time(on_example, test_list, n - 1)
        print(f"O(n)  list 搜尋: {t2:.6f} 秒")

        # O(n²) 測試
        t3, _ = measure_time(on2_example, test_list)
        print(f"O(n²) 雙層迴圈:  {t3:.6f} 秒")

    print("\n" + "=" * 50)
    print("🤔 思考題：")
    print("1. O(1) 的時間有沒有隨 n 變大而變化？")
    print("2. O(n²) 在 n=10000 時比 n=1000 慢幾倍？")
    print("   (提示：10000² / 1000² = ?)")
    print("=" * 50)
