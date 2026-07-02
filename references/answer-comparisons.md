# L4 vs L6 Answer Comparisons

> **用途**：建立「什麼是好答案」的直覺。比抽象教學快：直接看同一題的弱答案和強答案逐段對比，加上面試官的內心 OS。
> 用法：先讀 L4 的回答，自問「我會怎麼說」，再看 L6 版本和面試官 OS。如果你的版本接近 L4，把差距記進 `progress.md` 的 Mistake Registry。
>
> 核心差異速覽（四題共通的 pattern）：
>
> | 維度 | 🟥 L4 行為 | 🟩 L6 行為 |
> |------|-----------|-----------|
> | 開場 | 跳過釐清直接畫圖 | 先協商 scope，主動排除不做的事 |
> | 數字 | 不估算，或估了不用 | 估算驅動每個設計決策 |
> | Trade-off | 列出選項就停 | 講「為什麼在這個 context 選它」+ 標出代價 |
> | Failure | 等面試官問才想 | 主動講 failure mode 和 operational 應對 |
> | 收手 | 在不重要的地方鑽細節 | 知道哪裡點到為止、哪裡值得深挖 |

---

## 題目 1: URL Shortener

### 開場：Clarify Requirements

> 🟥 L4: "好，URL shortener，我知道這題。基本上就是一個 hash function 把長網址變短網址，存進資料庫，讀的時候查出來 redirect。我先畫架構圖。"
>
> 🟩 L6: "我先確認幾件事再開始。第一，規模：假設 DAU 1 億、每天新增 1 億條短網址，可以嗎？第二，讀寫比：redirect 是 100:1 還是更高？這會決定我整個架構往讀傾斜。第三，要不要點擊分析？這影響我選 301 還是 302。第四，短碼長度有限制嗎？自訂 alias 要支援嗎？最後，我先假設不需要修改和刪除短網址，如果需要我再加回來。"
>
> 🎙️ 面試官 OS: L4 第一句就暴露了「背過題」：把面試當默寫，而我要看的是工程判斷。他直接跳進解法，等一下我隨便改一個需求（比如要 analytics）他的設計就會崩。L6 問的每個問題都連到一個設計決策（讀寫比 → cache 策略、analytics → 301/302、規模 → 是否分片），這叫 requirements-driven design，這是 hire signal。而且他主動宣告「假設不做刪除」是在管理 scope，這是 senior 的時間管理。

### High-Level Design

> 🟥 L4: "Client 打到 server，server 用 MD5 把長網址 hash 成短碼，存進 MySQL。讀的時候用短碼查 MySQL，回 redirect。前面加個 load balancer 就可以 scale 了。"
>
> 🟩 L6: "先做估算。寫入：1 億/天約 1200 QPS，尖峰抓 3 倍是 3600。讀取按 100:1 是 12 萬 QPS、尖峰 36 萬。儲存：每條 500 bytes，一天 50GB、五年約 90TB。這些數字告訴我三件事：寫入很小，單一發號服務綽綽有餘，不用過度設計；讀取很大，必須有 cache 層，而且 redirect 是純 KV 查詢，cache hit ratio 可以做到 95% 以上；儲存要分片，但 access pattern 單純，KV store 就夠，不需要關聯查詢。所以架構是：讀路徑 client → CDN/LB → service → Redis → DB，寫路徑走獨立的發號邏輯。我畫出來。"
>
> 🎙️ 面試官 OS: L4 的設計不算錯，但他是「憑感覺」拼的，我問他「為什麼用 MySQL」他大概率答不出來。L6 在畫圖之前先把數字攤出來，然後每個架構決策都引用一個數字當理由：「寫入小所以不過度設計」這句話特別加分，多數 candidate 只會往上堆元件，知道「哪裡不需要複雜」的人比知道「哪裡要加東西」的人少見得多。90TB 這個數字一出來，後面聊分片就有了共同的事實基礎。

### Deep Dive：短碼生成

> 🟥 L4: "用 MD5 hash 長網址，取前 7 個字元當短碼。Base62 的話 7 位有 62^7 大概 3.5 兆個組合，夠用了。"
>
> 🟩 L6: "短碼生成有兩條路線，我比較一下再選。路線一是 hash 截斷：MD5 取前 7 碼，好處是無狀態、同網址天然去重，但截斷後會碰撞，需要查庫探測再加 salt 重試，寫入路徑多一次往返。路線二是發號器 + base62：全局 counter 編碼成短碼，無碰撞，但有兩個問題：counter 是中心化元件要考慮可用性，而且循序 ID 可被遍歷，有人可以把全站短網址爬一遍，這是安全問題。我的選擇：發號器路線，用分段發號解可用性（每個 service 實例一次領 10 萬個號，counter 服務掛了還能撐一陣子），用混淆函數打亂輸出解遍歷問題。理由是寫入 3600 QPS 下，hash 探測的額外查庫成本不划算，而且 business 上 99% 不需要『同網址同短碼』的去重。"
>
> 🎙️ 面試官 OS: L4 講的是教科書標準答案的一半，3.5 兆這個數字算對了，但他沒提碰撞處理，我追問「兩個網址 hash 出同一個前 7 碼怎麼辦」他就會卡住。L6 的回答結構是我最想看到的：選項 A 的代價、選項 B 的代價、我的選擇、為什麼在這個 context 下這樣選。特別是他主動講出「循序 ID 可被遍歷」這個安全面，這不在多數題解裡，代表他真的想過這個系統被惡意使用的樣子。分段發號講出「掛了還能撐一陣子」是 operational 思維。

### Scale & Trade-offs

> 🟥 L4: "如果流量變大，就加更多 server，DB 做 sharding，cache 用 Redis cluster。應該就可以了。"
>
> 🟩 L6: "Scale 我講三個具體的點。第一，DB 分片：shard key 用短碼本身，因為唯一的查詢就是 by 短碼，hash 分佈天然均勻，不會有 hot partition。第二，真正的風險是熱 key：一條短網址被瘋傳，單一 cache 節點被打爆，我會在 service 層加 local cache（毫秒級 TTL）扛住這種尖峰，代價是極短的不一致窗口，redirect 場景完全可接受。第三，operational：我會監控 cache hit ratio、redirect P99、和發號器的號段餘量，hit ratio 掉到 90% 以下要告警，因為那代表 DB 流量翻倍。一個明確的 trade-off 總結：我整個設計用最終一致換讀取效能，新建的短網址可能有一兩秒查不到，business 上沒人在乎。"
>
> 🎙️ 面試官 OS: 「加 server、做 sharding、上 cluster」是 L4 的三句咒語，等於什麼都沒說，我聽不到任何這題特有的洞察。L6 的三點全部是這題專屬的：shard key 的選擇有理由、熱 key 是 URL shortener 真實世界最常出的事故、監控指標講到 hit ratio 和號段餘量這種具體粒度。最後那句主動總結 trade-off 並標注「business 上沒人在乎」，展示他知道一致性的代價要用業務語言衡量。這是我會在 feedback 寫 strong hire 的段落。

---

## 題目 2: Distributed Rate Limiter

### 開場：Clarify Requirements

> 🟥 L4: "Rate limiter 就是限制請求頻率。我用 token bucket 演算法，因為它是最常用的。每個用戶一個 bucket，超過就拒絕。"
>
> 🟩 L6: "我先釐清需求邊界。第一，限流維度：per-user、per-IP、per-API 還是組合？第二，這是部署在 API gateway 的集中式限流，還是給各服務用的 library？第三，精確度要求：是計費配額那種一個都不能多，還是防濫用那種有 5% 誤差也沒關係？這題的精確度直接決定架構複雜度。第四，規模：多少 QPS 經過 limiter？最後一個關鍵問題：限流器本身故障的時候，你們希望放行還是全擋？這是 business 決策，我需要知道。"
>
> 🎙️ 面試官 OS: L4 在需求都沒確認的情況下就選定了演算法，這是本末倒置：演算法是這題最不值錢的部分。L6 的問題裡有兩個讓我立刻坐直：「精確度要求」和「fail open or fail closed」。前者代表他知道「允許誤差」能讓設計簡化一個數量級，後者代表他被生產環境毒打過，知道 limiter 自己也是個會掛的元件。問出 fail policy 的 candidate 十個裡不到一個。

### High-Level Design

> 🟥 L4: "每台 server 收到請求就去 Redis 查這個 user 的 counter，沒超過就加一放行，超過就回錯誤。Redis 是共享的所以多台 server 也能正確計數。"
>
> 🟩 L6: "假設 50 萬 QPS 經過 limiter、防濫用場景、允許小誤差。架構放在 gateway 層，counter 集中在 Redis。先講基本流程：請求進來，以 user_id + API 當 key，在 Redis 做 check-and-increment。但這裡有兩個我要立刻處理的問題。第一，check 和 increment 分兩步有 race condition，並發下會超賣配額，所以用 Lua script 把判斷和遞增原子化。第二，50 萬 QPS 全打 Redis，單節點扛不住，但限流 key 天然可以按 user_id 分片，所以 Redis Cluster 水平切就行。被拒絕的請求回 429 加 Retry-After header，讓 client 知道退避。"
>
> 🎙️ 面試官 OS: L4 描述的流程在白板上看起來能動，但 race condition 這個地雷他沒看見，我等下一問並發他就會當場 debug。L6 不等我問就把 race 講了，而且解法是 Lua 不是分散式鎖：如果他答分散式鎖我會一路追問鎖的延遲成本直到他承認過度設計。429 + Retry-After 是小細節但很說明問題，他知道限流是 client 和 server 的協作協議，不是單方面拒絕。

### Deep Dive：演算法與 Redis 故障

> 🟥 L4: "演算法用 sliding window log，把每個請求的 timestamp 存進 Redis 的 sorted set，每次查詢就數窗口內有幾筆。這樣最精確。Redis 掛掉的話⋯⋯可以加一個 replica。"
>
> 🟩 L6: "演算法我選 sliding window counter 而不是 log。Log 法精確，但每個用戶要存窗口內所有 timestamp：1000 req/min 的用戶就是 1000 個 entry，乘上百萬活躍用戶是 GB 級記憶體，而我們開場就確認了允許小誤差，所以用當前窗口計數加上前窗口的加權近似，記憶體 O(1)，誤差最壞百分之幾，划算。再來是 Redis 故障，這是這題的靈魂：第一層，Redis 本身做 replica + 自動 failover；第二層，failover 的幾秒鐘內，gateway 降級到 local in-memory 限流，每節點配額抓 limit 除以節點數的近似值；第三層，如果整組 Redis 不可用，依照開場確認的 policy 走 fail open，放行但打 metric 告警。設計原則是：限流器是保護系統的，它自己絕不能變成讓系統全掛的單點。"
>
> 🎙️ 面試官 OS: L4 選 log 法的理由是「最精確」，但開場根本沒人要求精確，他在為不存在的需求付出 GB 級記憶體，這就是沒有把需求和設計連起來。被問到 Redis 掛掉只擠出「加 replica」，沒有降級層次。L6 的回答展示了兩個 L6 特徵：用開場確認過的需求（允許誤差）回頭證成演算法選擇，前後呼應；故障處理有三層深度（HA、降級、fail policy），而且最後一句「限流器不能變成單點」是原則性陳述，代表他不是背案例而是有設計哲學。

### Scale & Trade-offs

> 🟥 L4: "Redis 可以用 cluster 模式 scale。如果還不夠，就再加更多節點。"
>
> 🟩 L6: "再往上 scale，我會挑戰『每個請求都過 Redis』這個前提。每請求一次 Redis 往返是 1ms 級延遲加一份網路成本，乘 50 萬 QPS 很可觀。優化是兩級限流：每個 gateway 節點先在本地預扣一小批配額（比如一次跟 Redis 領 50 個），本地扣完再去領，這把 Redis 壓力降一到兩個數量級，代價是用戶配額的精確度再放寬一點，以及節點掛掉時預領的配額會蒸發。這個 trade-off 在防濫用場景完全成立，但如果今天是計費配額，我就會反過來：保留每請求過 Redis，甚至用持久化儲存。最後是上線策略：我不會直接啟用，先跑 shadow mode 只記錄不攔截，比對 would-be-blocked 的流量確認沒有誤殺，再灰度放量。"
>
> 🎙️ 面試官 OS: L4 又是「加節點」咒語。L6 做了一件 senior 才會做的事：挑戰自己架構的前提（每請求過 Redis），然後用批次預扣這個業界真實做法換掉它，並誠實標出代價。更重要的是他說「如果是計費場景我就反過來」，同一個人能根據需求翻轉自己的設計，這證明他持有的是決策框架不是標準答案。Shadow mode 上線是純粹的 operational maturity，這種人進來不會把生產環境弄掛。

---

## 題目 3: News Feed

### 開場：Clarify Requirements

> 🟥 L4: "News feed 就像 Facebook 那樣，用戶發文，follower 看到動態牆。功能就是發文和看 feed 兩個，我開始設計。"
>
> 🟩 L6: "幾個會影響架構的問題。第一，規模和分佈：假設 3 億 DAU，follow 關係的分佈很關鍵，有沒有千萬 follower 等級的大帳號？這決定 fan-out 策略。第二，排序：時間序還是 ML ranking？我建議先按時間序設計，最後留一段講 ranking 怎麼插進來。第三，feed 的新鮮度要求：發文後多久要出現在 follower 的 feed？秒級還是分鐘級可接受？第四，內容型態先假設純文字加圖片連結，影片的儲存和 CDN 是另一題。讀寫比我假設 100:1，看 feed 遠多於發文。"
>
> 🎙️ 面試官 OS: L4 把題目複述了一遍就要開始畫圖，他沒有問 celebrity 問題，而那是這題的核心考點，等於還沒開始就錯過了主線。L6 直接點名「大帳號分佈決定 fan-out 策略」，他知道這題在考什麼；「先時間序、ranking 最後再講」是主動的 scope 協商，把最深的坑留到時間允許再跳；「影片是另一題」是邊界管理。這個開場讓我可以放心把時間花在 deep dive，因為他自己會導航。

### High-Level Design

> 🟥 L4: "用戶發文存進 post DB。看 feed 的時候，查出這個用戶 follow 的所有人，去 post DB 撈他們最近的文，按時間排序回傳。前面加 cache 加速。"
>
> 🟩 L6: "先算讀路徑的成本。純 fan-out on read：用戶平均 follow 500 人，打開 feed 要查 500 人的最近發文再 merge，3 億 DAU 每人每天開 10 次，這個 scatter-gather 在尖峰是幾十萬 QPS 乘 500 路扇出，DB 直接死。所以主策略是 fan-out on write：發文時把 post id 推進每個 follower 的 feed cache（Redis ZSET，per-user 一條），讀 feed 變成讀自己那條 list 的 O(1) 操作，整個讀路徑就快了。寫路徑：post service 存文，發事件到 queue，fan-out worker 非同步消費、查 follower 清單、寫入各 feed cache。Feed 裡只存 post id，讀的時候再 batch hydration 取內文，避免內容重複儲存爆炸。"
>
> 🎙️ 面試官 OS: L4 描述的就是 fan-out on read，而且他不知道這個術語也不知道它的成本，我問「3 億用戶會怎樣」他才會開始現場心算。L6 用一段估算直接判了純 read 方案死刑再給出 write 方案，這個「先證明為什麼不行、再給解法」的敘事是說服力的來源。「只存 id 不存全文」加 hydration 這個細節，分得出看過真實系統和只看過部落格文章的人。

### Deep Dive：Celebrity Problem

> 🟥 L4: "如果是名人發文，follower 很多，fan-out 會比較慢⋯⋯可以多開一些 worker 平行處理，應該就能加快。"
>
> 🟩 L6: "Fan-out on write 在大帳號上會炸，算給你看：3000 萬 follower 的帳號發一篇文，就是 3000 萬次 Redis 寫入，假設每次 0.1ms 串行要 50 分鐘，平行化也要佔掉巨量 worker 容量，而且粉絲看到文的時間差會拉到分鐘級，體驗不一致。加 worker 是線性手段，解不了這個量級。正解是 hybrid：帳號標記 celebrity（比如 follower 超過 10 萬），他們的發文不做 fan-out，只寫 post DB；讀 feed 時做 merge：自己的 precomputed feed list，加上 follow 清單中 celebrity 帳號的即時查詢，兩路合併排序。代價是讀路徑變複雜、celebrity 那路要靠 cache 撐（但 celebrity 的最新發文天然是熱資料，cache hit 極高，剛好成立）。閾值 10 萬不是魔法數字，是 fan-out 成本和讀放大之間的調節旋鈕，要用 metrics 持續校準。"
>
> 🎙️ 面試官 OS: L4 的「多開 worker」暴露他用線性思維解指數問題，50 分鐘這種數字他沒算過，所以感受不到「加 worker」有多無力。L6 先量化問題的規模讓「為什麼要 hybrid」不證自明，然後 merge 的兩路來源講得具體（自己的 list + celebrity 即時查），最後說「閾值是調節旋鈕要用 metrics 校準」，把一個靜態設計變成可營運的系統。這段是這題的勝負手，L6 的回答我可以直接寫進 hiring committee packet。

### Scale & Trade-offs

> 🟥 L4: "Feed cache 用 Redis cluster，post DB 做 sharding，再加 CDN。排序如果要 ML 的話就接一個 ML 模型。"
>
> 🟩 L6: "收尾講三個 trade-off 和 operational。第一，feed cache 的記憶體預算：3 億用戶每人留 800 個 post id，每條約 20 bytes，粗估 5TB 級，所以 inactive 用戶（30 天沒登入）的 feed 直接不維護，回來時用 fan-out on read 現場重建一次，這是用「重建成本」換「常駐記憶體」。第二，刪文和封鎖：已經 fan-out 出去的 id 不回收（找出所有投遞點太貴），在讀取 hydration 時過濾掉已刪除的文，洞用多取幾個 id 補，這是用讀時檢查換寫時簡單。第三，監控：fan-out lag（發文到 follower 可見的延遲）是核心 SLI，大帳號發文時這個指標會說話；feed cache hit ratio 和 hydration 的 batch 延遲也要上 dashboard。ML ranking 進來的位置：feed list 降級為候選池，後面接 ranking service 打分，ranking 掛了退回時間序，這樣 ranking 是可降級的附加層而不是單點。"
>
> 🎙️ 面試官 OS: L4 的回答仍然是元件名詞接龍，「接一個 ML 模型」這種句子等於沒講。L6 的三點各自展示一種資深能力：5TB 估算加 inactive 剔除是容量工程；刪文走讀時過濾是知道業界真實做法（這個問題九成 candidate 沒想過）；fan-out lag 當 SLI 是把抽象架構翻譯成可以 on-call 的東西。最後 ranking 的插入位置講了一句「可降級的附加層」就收手，沒有鑽進 ML 細節，時間管理完美。

---

## 題目 4: Payment System

### 開場：Clarify Requirements

> 🟥 L4: "Payment system，就是用戶付錢、我們扣款。需要一個 API 接收付款請求，然後呼叫像 Stripe 這種第三方去刷卡，成功就更新訂單狀態。"
>
> 🟩 L6: "支付這題我先把邊界和不變量定清楚。第一，scope：我們是接第三方 PSP（Stripe/Adyen）的商戶系統，還是自己做收單？我假設前者，後者牽涉卡組織和合規是完全不同的題。第二，這個系統的兩個不可妥協的不變量：不能重複扣款、不能丟交易，錢的正確性優先於延遲和可用性，這和前面幾題的取捨方向相反。第三，規模：假設 100 萬筆/天，尖峰 100 TPS，支付系統的難度從來不在 QPS 而在正確性。第四，需要支援退款和部分退款嗎？對帳的範圍包含跟 PSP 對還是也要跟銀行對？我先納入 PSP 對帳。"
>
> 🎙️ 面試官 OS: L4 把支付描述成「呼叫 API 然後更新狀態」，這個心智模型等下會在 timeout 問題上全面崩潰。L6 開場就講「不變量」和「正確性優先於延遲」，他知道這題的取捨軸和高吞吐系統相反，這個 meta 認知本身就是 signal。主動說「100 TPS、難度不在 QPS」防止自己把時間浪費在不重要的 scaling 上。區分商戶系統和收單系統，代表他知道這個領域的地形。

### High-Level Design

> 🟥 L4: "Client 發付款請求到 payment service，service 呼叫 Stripe API，Stripe 回成功後，把訂單標成已付款，寫進 DB，然後回應 client。失敗就回錯誤讓用戶重試。"
>
> 🟩 L6: "核心流程我用狀態機來講，因為支付的本質是狀態機不是 request-response。一筆 payment 的狀態：created → pending → succeeded / failed，每個轉移都持久化。流程：client 帶著 idempotency key 發起付款，payment service 先寫入 created 狀態的 payment record（這步成功才往下走），轉 pending 後呼叫 PSP（呼叫本身也帶冪等 key），拿到結果轉終態，再透過 outbox pattern 發事件給下游（訂單、通知、ledger）。三個設計重點：第一，先寫庫再呼叫 PSP，保證任何時刻當機都有紀錄可恢復；第二，所有金額異動進 double-entry ledger，append-only，balance 是衍生值；第三，PSP 的 webhook 是結果的最終權威，同步回應只是樂觀提示，webhook handler 要冪等因為 PSP 會重送。"
>
> 🎙️ 面試官 OS: L4 的流程裡「失敗就讓用戶重試」這句話讓我在評分表上記了一筆：沒有冪等保護的重試在支付系統等於雙重扣款事故。L6 開口第一句「支付的本質是狀態機」就把抽象層級拉對了，先寫庫再呼叫外部、outbox、webhook 為權威加冪等消費，這三個 pattern 是支付系統的地基，他一次講齊而且每個都附了理由。ledger 在 high-level 就出現而不是被我逼出來，說明他知道錢的系統長什麼樣。

### Deep Dive：Timeout 與 Exactly-Once

> 🟥 L4: "如果呼叫 Stripe timeout，就 retry 三次，都失敗就把訂單標成失敗，請用戶重新付款。"
>
> 🟩 L6: "Timeout 是支付系統最危險的時刻，因為它是未知狀態不是失敗：Stripe 可能已經扣款成功只是回應沒到我這。所以絕對不能把 timeout 當失敗處理，否則用戶重付就是雙扣。我的處理：payment 停在 pending，啟動查證流程，用 PSP 的查詢 API 以冪等 key 查這筆交易的真實狀態；查到成功就補狀態，查到不存在才能安全地以同一個冪等 key 重送（PSP 端會去重）；查證系統本身也失敗的話，這筆單進人工 review queue，寧可慢不可錯。再講 exactly-once：分散式系統沒有傳輸層的 exactly-once，只有『at-least-once 傳遞加上冪等處理』等效出來的 exactly-once 結果。每一層都要冪等：client 到我們（idempotency key 唯一索引）、我們到 PSP（PSP 冪等 key）、webhook 進來（event id 去重）、ledger 寫入（交易 id 唯一）。最後的安全網是對帳：每日拉 PSP settlement file 跟 ledger 逐筆對，差異分三類（我有他無、他有我無、金額不符）各有處理 runbook。對帳不是不信任自己的代碼，是承認分散式系統的故障模式永遠比你想的多。"
>
> 🎙️ 面試官 OS: L4 那句「timeout 就標失敗請用戶重付」是這整份文件裡最貴的一句話，生產環境裡它就是大規模雙扣事故加上岸然來的客訴和退款成本。L6 把「timeout 是未知態」當成段落的第一性原理，查證、同 key 重送、人工兜底的三層處理是真實支付系統的標準作業。「exactly-once 是冪等等效出來的結果」這句話我會原文記進 feedback。最後那句對帳的哲學陳述（承認故障模式比你想的多）是工程成熟度的展現，這是 L6 和 L5 的分界線。

### Scale & Trade-offs

> 🟥 L4: "如果交易量變大，payment service 可以水平擴展多開幾台，DB 可以分片。Stripe 那邊應該他們自己會 scale。"
>
> 🟩 L6: "支付系統的 scale 重點不在吞吐在隔離和可用性，講四個。第一，PSP 故障隔離：Stripe 整段不可用時，circuit breaker 斷開、payment 排進 retry queue 延後處理，更進一步是 multi-PSP failover（路由層按健康度和費率選 PSP），代價是對帳和冪等要跨 PSP 處理，複雜度高，是否值得取決於 business 對掉單的容忍度。第二，DB：100 TPS 單一 Postgres 撐得綽綽有餘，我反而要強調不分片的好處：單庫交易保住狀態機轉移的原子性，等真的到幾千 TPS 再按 merchant id 分片。第三，operational：核心 SLI 是 payment success rate，按 PSP、卡種、地區切片，掉 0.5% 就 page，因為這通常比任何 infra alert 更早暴露問題；再來是 pending 超時單數量（狀態機卡住的單）和每日對帳差異趨勢。第四，安全合規點到為止：卡號絕不落地，用 PSP tokenization，PCI DSS scope 縮到最小。總結這題的 trade-off：我用延遲和架構簡單性換正確性，支付寧可慢一秒，不能錯一分錢。"
>
> 🎙️ 面試官 OS: L4 到了最後一段還在講水平擴展，他從頭到尾沒有發現這題的計分維度根本不是吞吐。L6 說「100 TPS 單庫就夠、而且單庫交易是優點」，敢於說「不需要分片」並給出理由的 candidate 比硬上分片的強一個 level，這是判斷力。Success rate 按維度切片、掉 0.5% 就 page，這是真的維運過支付的人才講得出的數字。最後用一句話總結整題的取捨方向，首尾呼應開場宣告的不變量。四段下來他展示的不是知識量而是判斷的一致性，strong hire。

---

## 題目 5: Ticket Booking / Flash Sale

### 開場：Clarify Requirements

> 🟥 L4: "搶票系統，重點就是高並發。我會用 Redis 扛流量，庫存放 Redis 做原子扣減，後面接 queue 慢慢寫 DB。我先畫圖。"
>
> 🟩 L6: "我先確認幾個決定架構的問題。第一，規模對比：庫存多大、搶的人多少？1 萬張票 100 萬人搶，跟 100 萬張票 100 萬人搶，是兩個完全不同的題目。第二，業務規則：超賣和少賣哪個絕對不能發生？演唱會票我假設超賣是紅線。第三，付款流程：搶到之後付款有多久時限？這決定庫存要不要有預留態。第四，公平性有要求嗎？先到先得、抽籤、還是防黃牛優先？最後，一個用戶限購幾張？這影響我要不要做 per-user 限制。"
>
> 🎙️ 面試官 OS: L4 一開口就是解法拼裝（Redis、queue 都是對的零件），但他不知道自己在解哪一題。L6 的第一個問題就值回票價：供需比是這題的核心參數，10:1 和 100:1 的架構差一個數量級的複雜度。「超賣和少賣哪個是紅線」這個問題直接暴露他懂這題的本質是 business 約束下的一致性取捨，不是純技術題。問付款時限的人知道庫存有生命週期，這是做過交易系統才有的直覺。

### High-Level Design

> 🟥 L4: "用戶請求進來，先過 rate limiter，然後到 Redis 用 DECR 扣庫存，扣成功就發訊息到 Kafka，consumer 慢慢建訂單。這樣 DB 就不會被打爆。"
>
> 🟩 L6: "先算數字：1 萬張票、100 萬人、開賣瞬間假設 50 萬 QPS。這個數字告訴我：99% 的請求注定失敗，所以架構的核心是分層漏斗，讓失敗的請求在越外層死掉越好。第一層，前端排隊頁加隨機打散，把瞬間尖峰攤平成幾十秒；第二層，gateway 做 per-user 限流加全局限流，過濾重試轟炸；第三層，只有拿到排隊 token 的請求才能進扣減流程，這時 QPS 已經從 50 萬降到千級；第四層才是庫存扣減：Redis Lua 原子扣減，成功者拿到預留憑證進付款流程。DB 只接收序列化之後的訂單寫入，壓力是千級 QPS，完全扛得住。"
>
> 🎙️ 面試官 OS: L4 的架構零件都對，但他把 50 萬 QPS 直接放進 Redis DECR，我追問「Redis 單 key 扛得住嗎、掛了怎麼辦」他就會開始現場補洞。L6 先算出「99% 注定失敗」這個洞察，整個架構就有了主軸：不是怎麼處理 50 萬請求，是怎麼讓 49 萬 9 千個請求便宜地死掉。每一層漏斗都有明確目的和量級變化，這是我最想聽到的敘事結構。

### Deep Dive：庫存扣減的正確性

> 🟥 L4: "Redis DECR 是原子的，所以不會超賣。扣成功就是搶到了，之後建訂單、付款。"
>
> 🟩 L6: "原子扣減只解決一半問題，我走一遍失敗場景。DECR 成功後、訂單建立前，service crash 了：庫存少 1 但沒有訂單，這張票就漏掉了。所以我的設計是預扣模型：DECR 成功等於拿到一個帶 TTL 的預留，比如 10 分鐘內要完成付款，逾期由過期機制自動歸還庫存。這裡有個刻意的偏向：所有邊界情況我都讓它傾向少賣而不是超賣，因為少賣的票可以歸還再放出，超賣是賠償和公關災難。另外兜底：一個對帳 job 定期檢查 invariant，Redis 剩餘量加上已建訂單加上預留中的數量，必須等於初始庫存，對不上就告警。最後，整條鏈路用 client 生成的冪等 key，用戶重試不會重複扣。"
>
> 🎙️ 面試官 OS: 「DECR 是原子的所以不會超賣」是這題最經典的半對答案，L4 停在這裡，我問一句「扣完 crash 呢」他就垮了。L6 主動走 failure timeline 是 senior 的標誌行為，「預扣是租約不是所有權」這個模型一出來，TTL、歸還、對帳全部順理成章。最加分的是「刻意傾向少賣」：他知道工程做不到兩全時，要把偏向變成一個明說的設計決策，而且用 business 語言論證。庫存 invariant 對帳這條，十個 candidate 有九個不會主動講。

### Scale & Trade-offs

> 🟥 L4: "如果票更多就把庫存分片，Redis 上 cluster，consumer 多開幾個。監控的話看 QPS 和 latency。"
>
> 🟩 L6: "三個點。第一，單 SKU 熱點：一場演唱會就是一個 key，Redis cluster 分片解決不了單 key 熱點，真要再往上就把庫存拆桶，比如 1 萬張拆成 100 桶各 100 張隨機路由，代價是桶間餘量不均可能提前顯示售罄，需要桶間 rebalance。第二，惡意流量：黃牛腳本會繞過前端排隊直接打 API，所以排隊 token 必須是 server 簽發、進扣減層強制驗證，不能只做前端擋板。第三，operational：我監控漏斗每層的通過率，某層通過率突然改變就代表有人繞層；庫存 invariant 對帳差異是 P0 告警；預留歸還率異常升高代表付款環節出問題。總結 trade-off：整個設計用「多層過濾的複雜度＋預留機制的狀態管理」換「DB 只承受千級序列化寫入＋超賣機率趨近於零」，代價是用戶體驗上會有排隊等待，這在搶票場景是可接受甚至預期的。"
>
> 🎙️ 面試官 OS: L4 說「庫存分片」暴露他沒想過這題的熱點是單 key，加機器沒用。L6 講出「拆桶＋桶間不均的代價」代表真的推演過。「排隊 token 必須 server 端強制驗證」這句是安全思維：他假設了有人會作弊。監控講到「漏斗通過率突變 = 有人繞層」這種攻防粒度，加上最後一句完整的 trade-off 總結把複雜度的買賣講清楚，這是 strong hire 段落。

---

## 自我檢測：你在哪一級？

讀完五題後，用這個 checklist 對照自己最近一次 mock 的表現：

| 檢查項 | L4 症狀 | L6 行為 | 自評 |
|--------|---------|---------|------|
| 開場 30 秒 | 複述題目就開始畫圖 | 問出 3-5 個連到設計決策的問題 | ☐ |
| 估算 | 沒算，或算完沒用上 | 每個架構選擇都引用一個數字 | ☐ |
| 選型 | "X 是最常用的所以用 X" | 兩個選項各標代價，用 context 決定 | ☐ |
| Failure mode | 等面試官問 | 主動講「這裡掛了會怎樣」 | ☐ |
| Timeout/重試 | retry 就好 | 冪等 key + 未知態處理 | ☐ |
| Operational | 沒提或只講 CPU alert | 講 SLI、降級路徑、上線策略 | ☐ |
| 收手 | 在次要處鑽牛角尖 | 「這是另一題，點到為止」 | ☐ |
| Trade-off 總結 | 沒有總結 | 一句話講清整題用什麼換什麼 | ☐ |

勾不到 5 項：回去重練對應主題的 follow-up bank（`references/follow-up-bank.md`），把缺的維度寫進下一次 mock 的目標。
