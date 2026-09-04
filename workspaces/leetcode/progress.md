<!-- Schema: docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md 第 8 節。
     這個檔只回答「現在在哪」,不回答「你欠什麼」。
     不加到期日欄位、不加未結狀態、不加順延計數。重建前的舊 state 在 archive/pre-rebuild/。 -->

# leetcode

- 今天做到:2026-09-04。Linked list 速刷開跑。學員自評「原理懂但寫不出來」,讀書會的
  NeetCode linked list 已自行刷完,這邊重新速刷驗收。#206 + #21 兩題:冷寫都組不出
  「指標推進迴圈」的骨架 → 卡住協定逐塊補 → harness 綠。#206 清空重打過(1 個
  `nxt`/`next` 手滑,階 1 提示後自抓)。#21 溫度計②變形題(`list1 or list2` 尾段
  invariant)沒答出來,當場補。
- 模式:速刷 = 每題冷寫 → 卡住協定 → harness → 變形題。學員確認這個節奏 ok。
  診斷:零件(prev=None、存在改之前、dummy/tail 分工)分開問都懂,從空白頁組不起來。

## Pattern 狀態

| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 反轉(prev/curr/nxt) | ✓(notes) | ✓ | 🟡 清空重打過,但緊接對照打 | ✓ |
| Linked List 合併(dummy + tail) | ✓ | ✓ | 🟡 逐塊提示下完成,非全冷 | ✓ |
| Heap k-way merge(每條一個 head) | ✓ | | ✓ | ✓ |
| Hashmap + 雙向鏈(LRU) | | | | |

## 做過

- **Layer 0 執行模型**:跑了概念 1(變數是貼標籤)、4(縮排歸誰管)、5(迴圈變數每圈重算)、
  7(node / pointer / `.next`)。概念 2(`//`)、3(list 方法名)、6(`while` 條件)當天跳過,
  linked list 用不到,卡到再翻。
- **#21 Merge Two Sorted Lists** — `linked-list/merge-two-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
  已完成:圖解頁、L6 面試逐字稿(含 code 對照表)、pytest harness;2026-08-31 學員回報早上完成。
  2026-09-04 速刷:冷寫卡在 loop body(有 dummy 沒 tail、把 tail 角色跟 #206 的 prev 混),
  逐塊補完 harness 10/10 綠(含 10 萬×2 + 節點重用)。變形題「尾段為何能整段掛」沒答出,已講。
- **#23 Merge K Sorted Lists** — `linked-list/merge-k-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/65a51c4d-d03a-4161-8140-0f8b9669254f
  首場產出:圖解頁、min-heap 主解、divide-and-conquer follow-up、L6 面試逐字稿(含 code 對照表)。
  2026-09-02 複盤:merge two → naive merge-one-by-one(TLE 原因)→ heap,拷問 ① 補上,
  學員獨立寫出 heap code(抓到漏 `import heapq`)。
- **#146 LRU Cache** — `hashmap-doubly-linked-list/lru-cache/`
  圖解頁:https://claude.ai/code/artifact/69673f1c-d044-49b9-bb01-42082143e263
  本場產出:圖解頁(寄物間號碼牌比喻)、暴力解對照、L6 面試逐字稿(含 code 對照表)、pytest harness。
- **#206 Reverse Linked List** — `p3-binsearch-linkedlist/reverse-linked-list/`
  2026-08-03 首刷,2026-09-04 速刷:冷寫失敗(`prev = head` 起手錯、組不出 4 步順序),
  對照打 + 變形題(刪 `nxt = curr.next` 會斷鏈)過,清空重打 harness 8/8 綠(1 個手滑自抓)。
  缺 eli5 圖解頁 + L6 逐字稿。

## 接下來

1. 開場默寫 #206 + #21 的 template(隔堂留存測 = 溫度計第 3 層,今天的清空重打只測到短期記憶)
2. 速刷 #141 Linked List Cycle(fast-slow 是新招,龜模式)
3. 補債:#206 的 eli5 圖解頁 + L6 逐字稿;#21 eli5 補「這次的釐清」
4. #146 LRU 仍停在拷問 ① 前,未動
