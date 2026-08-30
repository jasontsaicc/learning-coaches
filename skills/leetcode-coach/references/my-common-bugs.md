# 我的常犯錯

這是 checklist,不是帳本。沒有到期日、沒有未結狀態、沒有順延計數。

**升級規則:** 一次性的搞混留在該題圖解頁的「這次的釐清」區塊。重複出現才升上這張表。
新增一列時把次數寫上去,並重新按次數排序,最上面永遠是最常犯的。

初始內容來自 2026-08-28 重建前 Mistake Registry 的 32 列(s5 到 s20),已合併同家族。

## 寫 code 前掃這張表

| # | 檢查 | 犯過 | 症狀 |
|---|---|---|---|
| 1 | `return` 是不是縮排卡在迴圈裡? | 3 | 找得到的全掛、找不到的全綠。不報錯,所以最貴 |
| 2 | 算 index 有沒有用 `//`?`/` 回 float,float 不能當 index | 2 | `TypeError: list indices must be integers` |
| 3 | 變數名有沒有手滑?(pairs→paris→pairss、answes) | 2 | `NameError` |
| 4 | 字元有沒有打錯?(`stack, append(i)` 的逗點、`len(matrix)[0]` 的括號位置) | 2 | 當場報錯,成本低 |
| 5 | 閉區間 `[l, r]` 配 `while l <= r` 時,`r` 初始值是 `len(nums) - 1` 不是 `len(nums)` | 2 | `IndexError`,或測資不夠 hostile 而整組漏掉 |
| 6 | Python list 是 `.append`,沒有 `.push` | 1 | `AttributeError` |
| 7 | `if` / `for` / `while` / `def` 開頭的行,結尾冒號補了嗎? | 1 | `SyntaxError` |
| 8 | `if stack` 是「有東西」,`not stack` 是「空的」。`not stack` 要放 `or` 左邊短路保護 `stack[-1]` | 1 | `IndexError` 或邏輯全反 |

## 你容易搞混的觀念

這一段餵教學迴圈的步驟 7(主動指出最可能犯的錯)。不是 checklist,是教的時候要主動戳的點。

| # | 觀念 | 出現過 | 怎麼戳 |
|---|---|---|---|
| 1 | **「這行什麼時候被求值」** 沒有心智模型。三個症狀同源:`while` 條件答成迴圈結束狀態、迴圈變數以為每圈不變、講不出哪些行該在迴圈內 | 4 次跨題 | 問「這行在第 k 圈執行時,值是誰?依賴什麼?」 |
| 2 | binary search 的前提是「丟掉的那半保證不含 target」,**不是**「array 要 sorted」。sorted 只是取得這個許可證的手段 | 3 | 問「沒排序但有一個保證答對的 oracle,能不能 binary search?Koko 沒有 sorted array 為什麼是 binary search?」 |
| 3 | 抽象原則講得出來,套不到具體元素上(給原則加具體矩陣,講不出「這兩個 row 的每個元素都小於 target」) | 2 | 給原則加一個具體例子,要求指名是哪幾個元素 |
| 4 | harness 掛了先看 code,沒先看 fail/pass 分布 | 2 | 給一組 fail 分布,問這是哪一類邏輯錯 |
