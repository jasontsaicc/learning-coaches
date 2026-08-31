<!-- Schema: docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md 第 8 節。
     這個檔只回答「現在在哪」,不回答「你欠什麼」。
     不加到期日欄位、不加未結狀態、不加順延計數。重建前的舊 state 在 archive/pre-rebuild/。 -->

# leetcode

- 今天做到:2026-08-30 第一場。Layer 0 跑過一輪,#21 進到圖解頁與 L6 逐字稿,solution.py 還沒寫
- 模式:龜(#21 是 linked list 首刷)

## Pattern 狀態

| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 合併(dummy + tail) | ✓ | | | ✓ |

## 做過

- **Layer 0 執行模型**:跑了概念 1(變數是貼標籤)、4(縮排歸誰管)、5(迴圈變數每圈重算)、
  7(node / pointer / `.next`)。概念 2(`//`)、3(list 方法名)、6(`while` 條件)當天跳過,
  linked list 用不到,卡到再翻。
- **#21 Merge Two Sorted Lists** — `linked-list/merge-two-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
  已完成:圖解頁、L6 面試逐字稿(含 code 對照表)、pytest harness。

## 接下來

1. #21 拷問 ②:`tail = tail.next` 搬進 `else` 會怎樣
2. 寫 `solution.py`,跑 `./scripts/lab-lc.sh workspaces/leetcode/linked-list/merge-two-sorted-lists/`
3. `heapq` 是什麼、為什麼 #23 需要它
4. #23 Merge K Sorted Lists(Hard 規格 = heap + #21)。讀書會 2026-09-01 由學員報這題
