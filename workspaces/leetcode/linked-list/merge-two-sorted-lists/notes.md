# 21. Merge Two Sorted Lists

- 圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
- 模式:龜(linked list 首刷)
- 口訣:兩條已排序合併 = dummy 假車頭 + tail 跟著跑,每圈挑小的接走,一條空了把另一條整段掛上。O(n+m) 時間,O(1) 空間
- invariant:兩邊都排序 → 最小的一定是兩個 head 之一,永遠不用看更深
- dummy 的交易:一節常數空間,換掉「接第一節」這個 special case
- 通往 #23:只換「怎麼挑出最小的 head」(兩兩比 → min-heap),骨架其餘不動 → O(N log k)

harness:`./scripts/lab-lc.sh workspaces/leetcode/linked-list/merge-two-sorted-lists/`

## 2026-09-04 速刷

冷寫卡在 loop body。

```
✗ 我以為:走路指標「也是 prev 嗎」(套 #206)
✓ 其實是:#206 的 prev 是「走過的地方,往回指」;#21 的 tail 是「正在蓋的新鏈末端,往前接」。
         起手都要 tail = dummy,dummy 本身不動(結尾 return dummy.next)
→ 為什麼會搞混:兩題都有「跟在後面的指標」,但一個往回指一個往前接,角色相反
```

其他缺塊(提示後自補):`tail = tail.next` 要在 if/else 外面每圈一次(最經典的雷)、
迴圈後 `tail.next = list1 or list2` 掛尾段、`return dummy.next`。
手滑:`else` 少冒號 → SyntaxError。

變形題「`list1 or list2` 為何能整段掛」沒答出。已講:`None or X` 回 X;
invariant = 每圈挑較小 head → 跳出時已合併的每個 node ≤ 剩下那條的每個 node,
剩下那條又已排序 → 直接就位,O(1) 不用逐一接。這句 invariant 是 L6 逐字稿 Move 3。
