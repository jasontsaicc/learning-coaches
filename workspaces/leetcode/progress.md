<!-- Schema: docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md 第 8 節。
     這個檔只回答「現在在哪」,不回答「你欠什麼」。
     不加到期日欄位、不加未結狀態、不加順延計數。重建前的舊 state 在 archive/pre-rebuild/。 -->

# leetcode

- 今天做到:2026-09-02。#23 重新從頭覆盤:merge two → k 條逐一 merge(講清楚為什麼 O(kN) 會
  TLE)→ 換 heap。拷問 ① 補上(學員自己講出這條路徑)。學員自己寫出 heap 版 code,邏輯與
  tie-breaker 都對,抓到一個漏 `import heapq` 的 bug。#146 沒有進度變動,仍停在拷問 ① 前
- 模式:#23 維持 Hard(min-heap + #21,目標是拆得開、講得出來),本場達成。#146 仍是龜
  (新結構首刷,hash 加雙向鏈)

## Pattern 狀態

| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 合併(dummy + tail) | ✓ | ✓ | | ✓ |
| Heap k-way merge(每條一個 head) | ✓ | | ✓ | ✓ |
| Hashmap + 雙向鏈(LRU) | | | | |

## 做過

- **Layer 0 執行模型**:跑了概念 1(變數是貼標籤)、4(縮排歸誰管)、5(迴圈變數每圈重算)、
  7(node / pointer / `.next`)。概念 2(`//`)、3(list 方法名)、6(`while` 條件)當天跳過,
  linked list 用不到,卡到再翻。
- **#21 Merge Two Sorted Lists** — `linked-list/merge-two-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
  已完成:圖解頁、L6 面試逐字稿(含 code 對照表)、pytest harness;2026-08-31 學員回報早上完成。
- **#23 Merge K Sorted Lists** — `linked-list/merge-k-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/65a51c4d-d03a-4161-8140-0f8b9669254f
  首場產出:圖解頁、min-heap 主解、divide-and-conquer follow-up、L6 面試逐字稿(含 code 對照表)。
  2026-09-02 複盤:merge two → naive merge-one-by-one(TLE 原因)→ heap,拷問 ① 補上,
  學員獨立寫出 heap code(抓到漏 `import heapq`)。
- **#146 LRU Cache** — `hashmap-doubly-linked-list/lru-cache/`
  圖解頁:https://claude.ai/code/artifact/69673f1c-d044-49b9-bb01-42082143e263
  本場產出:圖解頁(寄物間號碼牌比喻)、暴力解對照、L6 面試逐字稿(含 code 對照表)、pytest harness。

## 接下來

1. #146 拷問 ①:不知道 hashmap+雙向鏈時會怎麼做,暴力的也算(list 記順序也算)
2. 讀圖解頁 ①–④,用自己的話講出「為什麼 dict 存指標比存值更有用」
3. 用 capacity=2 的範例預測 put(3,3) 之後鏈跟 map 變成什麼樣子
4. 對照 code 後完成 #146 L6 讀書會口說演練
