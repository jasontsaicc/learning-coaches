# 我的常犯錯

這是 checklist,不是帳本。沒有到期日、沒有未結狀態、沒有順延計數。

**升級規則:** 一次性的搞混留在該題圖解頁的「這次的釐清」區塊。重複出現才升上這張表。
新增一列時把次數寫上去,並重新按次數排序,最上面永遠是最常犯的。

初始內容來自 2026-08-28 重建前 Mistake Registry 的 32 列(s5 到 s20),已合併同家族。

## 寫 code 前掃這張表

| # | 檢查 | 犯過 | 症狀 |
|---|---|---|---|
| 1 | `return` 是不是縮排卡在迴圈裡? | 4 | 找得到的全掛、找不到的全綠。不報錯,所以最貴 |
| 2 | 變數名有沒有手滑?(pairs→paris、answes、`nxt`→`next`、`dfa`→`dfs`) | 4 | `NameError`;或 `nxt`→`next` 打成 builtin,`AttributeError: 'builtin_function_or_method' object has no attribute ...` |
| 3 | 算 index 有沒有用 `//`?`/` 回 float,float 不能當 index | 2 | `TypeError: list indices must be integers` |
| 4 | 字元有沒有打錯?(`stack, append(i)` 的逗點、`len(matrix)[0]` 的括號位置) | 2 | 當場報錯,成本低 |
| 5 | 閉區間 `[l, r]` 配 `while l <= r` 時,`r` 初始值是 `len(nums) - 1` 不是 `len(nums)` | 2 | `IndexError`,或測資不夠 hostile 而整組漏掉 |
| 6 | `if` / `elif` / `else` / `for` / `while` / `def` 開頭的行,結尾冒號補了嗎? | 2 | `SyntaxError: invalid syntax`,箭頭指在關鍵字後 |
| 7 | Python list 是 `.append`,沒有 `.push` | 1 | `AttributeError` |
| 8 | `if stack` 是「有東西」,`not stack` 是「空的」。`not stack` 要放 `or` 左邊短路保護 `stack[-1]` | 1 | `IndexError` 或邏輯全反 |

## 你容易搞混的觀念

這一段餵教學迴圈的步驟 7(主動指出最可能犯的錯)。不是 checklist,是教的時候要主動戳的點。

| # | 觀念 | 出現過 | 怎麼戳 |
|---|---|---|---|
| 1 | **「這行什麼時候被求值」** 沒有心智模型。三個症狀同源:`while` 條件答成迴圈結束狀態、迴圈變數以為每圈不變、講不出哪些行該在迴圈內 | 4 次跨題 | 問「這行在第 k 圈執行時,值是誰?依賴什麼?」 |
| 2 | **`return` 做的兩件事只認得第一件**。知道「給出一個值」,不知道「撕掉自己這張 frame、控制權**倒退**回呼叫者、從它卡住的那一行接著跑」。同源症狀:`print` 與 `return` 混為一談 | 3 次(2026-09-10 #226 溫度計 ② 不會;2026-09-11 #104 拷問 ② 不會;`print`/`return` 1 次) | **不要用講的,畫兩張圖**:撕之前 / 撕之後的 frame 疊。問「這張紙撕掉之後,下一行是誰的哪一行」 |
| 3 | binary search 的前提是「丟掉的那半保證不含 target」,**不是**「array 要 sorted」。sorted 只是取得這個許可證的手段 | 3 | 問「沒排序但有一個保證答對的 oracle,能不能 binary search?Koko 沒有 sorted array 為什麼是 binary search?」 |
| 4 | **linked list 指標推進迴圈:零件都懂,組不出骨架**。且會把 trailing 指標(#206 的 `prev`,往回指)和 moving 指標(#21 的 `tail`,往前接)的角色混掉 | 3 次(#206 #21 2026-09-04;2026-09-07 複測骨架已過、角色描述仍模糊) | 骨架部分 2026-09-07 隔堂冷默已通過。剩下的加壓點是**指標角色的精確描述**:用「`prev` 在 `=` 右邊被讀(箭頭指向的目標),`tail` 在 `=` 左邊被寫(新貨掛上去的接口)」,不要用「前一個 / 最後一個」 |
| 5 | **合併類的「尾段可以整段掛」invariant 內化不了**。#21 的 `tail.next = list1 or list2` 講得出「如果還有就補上」,但寫不出 code、也說不出為什麼不用一顆一顆接 | 2 次(2026-09-04 當場補過,2026-09-07 隔堂又空白) | 問「迴圈停下來時另一條剩的東西,順序是亂的還是排好的?它的每一顆跟你剛接上的最後一顆比,誰大?」兩個都答對,code 自己會掉出來 |
| 6 | 抽象原則講得出來,套不到具體元素上(給原則加具體矩陣,講不出「這兩個 row 的每個元素都小於 target」) | 2 | 給原則加一個具體例子,要求指名是哪幾個元素 |
| 7 | harness 掛了先看 code,沒先看 fail/pass 分布 | 2 | 給一組 fail 分布,問這是哪一類邏輯錯 |
