<!-- Schema: docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md 第 8 節。
     這個檔只回答「現在在哪」,不回答「你欠什麼」。
     不加到期日欄位、不加未結狀態、不加順延計數。重建前的舊 state 在 archive/pre-rebuild/。 -->

# leetcode

- 今天做到:2026-08-31 第二場。學員回報早上完成 #21;開場默寫記得 dummy、tail、tail 前進與回傳,
  當場補上漏掉的 `tail.next = node`。#23 圖解頁與 L6 逐字稿已備妥,課程停在拷問 ① 前
- 模式:Hard(#23 = min-heap + #21,目標是拆得開、講得出來)

## Pattern 狀態

| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 合併(dummy + tail) | ✓ | ✓ | | ✓ |
| Heap k-way merge(每條一個 head) | | | | |

## 做過

- **Layer 0 執行模型**:跑了概念 1(變數是貼標籤)、4(縮排歸誰管)、5(迴圈變數每圈重算)、
  7(node / pointer / `.next`)。概念 2(`//`)、3(list 方法名)、6(`while` 條件)當天跳過,
  linked list 用不到,卡到再翻。
- **#21 Merge Two Sorted Lists** — `linked-list/merge-two-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
  已完成:圖解頁、L6 面試逐字稿(含 code 對照表)、pytest harness;2026-08-31 學員回報早上完成。
- **#23 Merge K Sorted Lists** — `linked-list/merge-k-sorted-lists/`
  圖解頁:`linked-list/merge-k-sorted-lists/eli5.html`
  本場產出:圖解頁、min-heap 主解、divide-and-conquer follow-up、L6 面試逐字稿(含 code 對照表)。

## 接下來

1. #23 拷問 ①:不知道 heap 時會怎麼做,暴力的也算
2. 讀圖解頁 01–04,用自己的話講出「為什麼只放每條 list 的 head 就夠」
3. 用 `[[1,4,5],[1,3,4],[2,6]]` 預測 pop 一個 node 後該 push 誰
4. 對照 code 後完成 L6 讀書會口說演練
