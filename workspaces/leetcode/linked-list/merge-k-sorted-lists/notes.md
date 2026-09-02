# 23. Merge K Sorted Lists

- 圖解頁:https://claude.ai/code/artifact/65a51c4d-d03a-4161-8140-0f8b9669254f
- 模式:Hard(講得出來；預設對照打)
- 拆解:#23 = #21 的 `dummy + tail` 串接 + min-heap 選最小 head
- invariant:heap 恰好保存每條尚未合併 list 的當前 head；因此 heap root 是所有剩餘 node 的全域最小值
- tie-breaker:`(node.val, list_id, node)` 讓相同值先比較唯一的 `list_id`，避免 Python 比較 `ListNode`
- 複雜度:精確寫法是 O(k + N log k) 時間、O(k) 額外空間；一般簡寫 O(N log k)
- follow-up:把 lists 兩兩配對，用 #21 做 divide and conquer，也能達到 O(N log k)

讀書會目標:不背 heap code；能用一句 invariant 解釋為什麼每次只放各 list 的 head 就足夠。
