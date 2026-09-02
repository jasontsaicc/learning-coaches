# 146. LRU Cache

- 圖解頁:https://claude.ai/code/artifact/69673f1c-d044-49b9-bb01-42082143e263
- 模式:龜(新結構首刷:hash 加雙向鏈)
- 觸發:2026-09-01 讀書會同事分享,插隊到 #146,curriculum 原順序不變(#146 在 #23 之前)
- 口訣:LRU = 服務台號碼本(hashmap)記位址 + 掛衣桿(doubly linked list)記順序。碰一次就「拔下來、插到最前面」,滿了就「砍掛桿最裡面那個,順手把它的號碼牌從號碼本撕掉」。get/put 都是 O(1) 時間,O(capacity) 空間
- invariant:鏈的順序永遠等於 recency 順序;map 永遠指向活著的 node
- sentinel 的交易:head/tail 兩個 dummy 換掉邊界 special case,跟 #21 的 dummy node 同一招
- 暴力解浪費的免費情報:dict 已經 O(1) 查到值,但「它在 list 哪個位置」這情報沒存下來,list.remove 要重新掃一遍,O(n)

harness:`./scripts/lab-lc.sh workspaces/leetcode/hashmap-doubly-linked-list/lru-cache/`
