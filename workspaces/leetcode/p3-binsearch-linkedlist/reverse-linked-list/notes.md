# #206 Reverse Linked List (S20, 2026-08-03)

## Pattern

Linked List 指向改寫。秒認信號:反轉/合併/中點/環。換皮鏈:206 → 21(合併)→ 141(快慢判環)→ 143(三合一)。DevOps 錨:middleware chain 改一棒的指向,不重排整條鏈。

## 前置概念(Chunk 1,一次過)

- node = val + next(下一棒的位址)。
- 交易:array 用連續擺放換 O(1) 隨機存取、付 O(n) 插入;linked list 用存 next 換 O(1) 插入刪除、付 O(n) 尋找。
- O(1) 插入的隱藏前提:你已經站在那個位置;走到那裡是 O(n)。

## 推導腳本(五問)

1. 改什麼:每個 node 的 next 從指下一棒改成指前一棒 → `curr.next = prev`
2. 保住什麼:改之前先存下一棒,否則斷線 → `nxt = curr.next`
3. 怎麼走:整組往前挪 → `prev = curr; curr = nxt`
4. 起點:`prev = None`(頭變尾,尾指 None)、`curr = head`
5. 何時停:`while curr`(還踩在 node 上就繼續);停時 `prev` = 新 head

口訣:**存、改、挪、挪**。順序錯 = 斷線或原地打轉。

## 手動模擬(1 → 2 → 3)

| 輪 | 存 nxt | 改 | prev | curr |
|----|--------|-----|------|------|
| 1 | 2 | 1.next=None | 1 | 2 |
| 2 | 3 | 2.next=1 | 2 | 3 |
| 3 | None | 3.next=2 | 3 | None → 停 |

## 紅字(本題的錯)

- 🔴 五問 Recall 自跑失敗:Q1/Q2 都答成「存 next」,主角「改指向」消失(answer-debt)。
- 🔴 模擬第二輪 nxt 答成上一輪的值 2;`nxt = curr.next` 每輪重新求值(loop-variable-liveness,同 while 條件家族)。
- 🟡 Transfer 首答「有環會無限迴圈」,trace 後自行推翻:繞回已反轉區會踩到第一輪埋的 None 而停。教訓:不確定就 trace,不用猜的。

## 結果

harness 8/8 green(空鏈/單節點/in-place/大 N 10 萬),手打零 bug(謄寫)。O(n) time / O(1) space。白紙重寫 2026-08-05 到期。
