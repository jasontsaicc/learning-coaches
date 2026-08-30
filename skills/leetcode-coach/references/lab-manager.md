# Lab Manager

本地 pytest harness,不碰雲端資源,零成本。腳本是 `scripts/lab-lc.sh <problem-dir>`:
它跑該題資料夾的 pytest,每個 test 有 wall-clock 上限(`LAB_LC_TIMEOUT`,預設 5 秒,
走 pytest-timeout)。

## 環境

需要 Python 3,且 `pytest` 與 `pytest-timeout` 可 import。session 前確認:
`python3 -m pytest --version`。harness 會自檢:缺套件時 exit 3 並印安裝提示,
題目資料夾不存在時 exit 2。

## 用法

每題一個資料夾(規則見 `teaching-loop.md` 的 eli5 圖解頁規格一節),內含
`solution.py` 與 `test_<slug>.py`。測試檔由 coach 提供,`solution.py` 由學員產出。

```
scripts/lab-lc.sh workspaces/leetcode/<pattern>/<slug>/
```

## 複雜度絆線(關鍵設計)

每個測試檔都帶一個大 N 的 case(例 n = 10^5),標 `@pytest.mark.timeout(N)`。
O(n^2) 的暴力解會通過小 case 但在大 N 逾時而整組紅。這讓「到底是不是最佳解」
變成機器判定,不是 coach 的主觀判斷,也堵掉「和善的 coach 放行一個能跑但很慢的解」
這條路。

刻意要驗證暴力 baseline 時,用 `-k "not large_n"` 只跑小 case。絆線是給最佳解那一步用的。

## 驗收

一個題目算過,條件是 `lab-lc.sh` exit 0:功能測試全綠**且**大 N 計時測試綠。
客觀、機器檢查,不接受自我回報。

**注意:** exit 0 只證明 code 會跑。它不證明學員自己寫得出來。是不是自己寫的,
由 `teaching-loop.md` 的三層溫度計判定,記在 `progress.md` 的 pattern 狀態表。

## 收尾

session 後清掉題目資料夾的 `__pycache__/` 與 `.pytest_cache/`:

```
find workspaces/leetcode -name '__pycache__' -o -name '.pytest_cache' | xargs rm -rf
```

沒有雲端資源,所以沒有成本 teardown。
