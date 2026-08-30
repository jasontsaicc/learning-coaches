<!-- ponytail: 此課程針對 Easy+Medium、DevOps coding 輪。
     觸發升級的條件(三選一發生就回來改):
       1. 目標公司換成算法題比重高的
       2. recruiter 明講 round 會有 Hard
       3. Medium 已經穩到無聊
     升級要動的只有兩處,不是重寫:
       1. 龜模式比例拉高(目前只有 pattern 首刷題走龜)
       2. 加 Hard 題池
-->

# Curriculum

順序跟著讀書會走 NeetCode,不自己另排一套。難度是 Easy 加 Medium;NeetCode 順序內
出現的 Hard 不跳過,但走 Hard 規格(見 `teaching-loop.md`)。

## Layer 0:Python 執行模型

**跑一次,不寫題。** 內容在 `layer0-execution-model.md`,7 個概念,全部從重建前那 32 筆
錯誤倒推出來。

跑完之後不再單獨複習。之後任何一場 session 只要學員卡在執行模型(哪一行會跑、
跑幾次、什麼型別),就回頭翻對應那一節,不重跑整個 Layer 0。

遞迴不在 Layer 0,走到 Tree 再教。

## Linked List(起點)

讀書會 2026-08 的進度在這裡,所以從這裡開始。

**開始前先跟讀書會核對一次實際順序。** 下表是 NeetCode 的順序,但以讀書會排的為準。

| 題號 | 題目 | 模式 | 備註 |
|---|---|---|---|
| 206 | Reverse Linked List | 龜 | 2026-08-03 做過一次,重跑。既有資料夾 `p3-binsearch-linkedlist/reverse-linked-list/` |
| 21 | Merge Two Sorted Lists | 兔 | |
| 141 | Linked List Cycle | 小龜 | fast-slow 是新招,不是 206 的換皮 |
| 143 | Reorder List | 兔 | 等於中點加反轉加合併 |
| 19 | Remove Nth Node From End | 兔 | |
| 138 | Copy List with Random Pointer | 兔 | |
| 2 | Add Two Numbers | 兔 | |
| 287 | Find the Duplicate Number | 兔 | fast-slow 換皮到陣列上 |
| 146 | LRU Cache | 龜 | 新結構:hash 加雙向鏈 |
| 23 | Merge K Sorted Lists | Hard 規格 | 等於 heap 加 #21 |
| 25 | Reverse Nodes in k-Group | Hard 規格 | 等於 #206 加分組 |

**龜兔判準看「這題有沒有沒見過的動作」,不看題號順序。** 同一個 pattern 底下也可能藏新招,
141 的 fast-slow 就是例子。

## Linked List 之後

依讀書會進度決定,不預先排。要排的時候照同一個格式:題號、題目、龜兔、一句話備註,
備註寫「這題等於哪幾個學過的東西」。

模板與秒認信號在 `pattern-cheatsheet.md`。
