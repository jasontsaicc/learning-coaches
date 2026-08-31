# 21. Merge Two Sorted Lists

- 圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
- 模式:龜(linked list 首刷)
- 口訣:兩條已排序合併 = dummy 假車頭 + tail 跟著跑,每圈挑小的接走,一條空了把另一條整段掛上。O(n+m) 時間,O(1) 空間
- invariant:兩邊都排序 → 最小的一定是兩個 head 之一,永遠不用看更深
- dummy 的交易:一節常數空間,換掉「接第一節」這個 special case
- 通往 #23:只換「怎麼挑出最小的 head」(兩兩比 → min-heap),骨架其餘不動 → O(N log k)

harness:`./scripts/lab-lc.sh workspaces/leetcode/linked-list/merge-two-sorted-lists/`
