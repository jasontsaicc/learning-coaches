# Interviewer Follow-Up Bank

> **用途**：給 skill 的 Step F「Interviewer Follow-Up Preview」抽題用，也供學生自我檢測。
> 每個主題列出真實面試中最高頻的追問（針對 failure mode、scale、trade-off、edge case、operational）。
> 「好答案要抓的重點」是骨架，不是完整答案：學生要能用自己的話展開，並帶數字或具體機制。
> 自我檢測方式：遮住右邊兩欄，只看追問，口頭回答 60-90 秒，再對照骨架檢查有沒有漏掉關鍵維度。

---

## Phase 1: Core Building Blocks

### Load Balancer & Reverse Proxy

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "LB 本身掛了怎麼辦？它不就是新的 SPOF？" | active-passive pair + VIP failover（keepalived/VRRP）、雲上用 managed LB（本身就是 multi-AZ cluster）、DNS 層再做一層 failover、healthcheck 間隔 vs failover 時間的 trade-off | 只說「再加一台 LB」卻講不出流量怎麼切過去（VIP、DNS、anycast 至少要講一個機制） |
| "L4 和 L7 你選哪個？為什麼？" | 先問 protocol 和需求：需要 content-based routing（path、header、cookie）就 L7；要極低 latency、非 HTTP（gRPC raw TCP、game、MQTT）、超高 throughput 就 L4；講出 L7 要終結 TLS + parse HTTP 的成本 | 背「L7 比較高級所以選 L7」；不知道 L4 不能看 HTTP header |
| "Health check 顯示健康，但用戶一直報錯，怎麼回事？" | shallow check（TCP/port）vs deep check（依賴 DB 的 endpoint）的差異、health check path 沒覆蓋真實依賴、partial failure（某個下游掛了但 /health 只回 200）、解法：分層 health check + 用 error rate metrics 補盲區 | 答「health check 壞了」就停；沒意識到 health check 的覆蓋範圍是設計決策 |
| "某台 backend 變慢但沒掛，LB 會發生什麼事？" | slow node 拖垮整體 P99（round robin 照樣送流量）、least connections / least latency 演算法可緩解、需要 outlier detection（被動健康檢查：連續 5xx 或 timeout 就摘除）、搭配 circuit breaker | 以為 health check 會自動處理「慢」；不知道 round robin 對慢節點無感 |
| "Sticky session 有什麼問題？什麼時候不得不用？" | 破壞負載均衡（熱用戶集中）、節點掛掉 session 全失、擴縮容時 rebalance 痛苦；正解是 externalize session（Redis）讓服務 stateless；不得不用的場景：legacy app、WebSocket 長連線 | 只說 sticky session 不好，講不出「為什麼 WebSocket 場景反而常見」 |
| "connection draining 是什麼？部署時不做會怎樣？" | 摘除節點前停止送新請求、等存量請求完成（設 timeout 上限如 30-300s）、不做會導致 deploy 時 5xx spike、長連線（WebSocket）要另外處理：主動發 close 讓 client 重連 | 沒聽過 draining；或以為「直接砍掉 client 會自動重試」就沒事（非冪等請求會出事） |

### Caching & CDN

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Redis 整個掛了，你的系統會怎樣？" | 量化衝擊：cache hit ratio 95% 表示 DB 流量瞬間 x20，DB 大概率跟著掛（cascading failure）、緩解：DB 端 connection pool 上限 + rate limit 保底、cache cluster 化（replica + failover）、degraded mode（回部分功能或 stale data） | 只說「就去打 DB」，沒算出 DB 會被打爆；沒提保護 DB 的手段 |
| "怎麼防 cache stampede / 雪崩？" | 分清三件事：stampede（單一熱 key 過期，萬人同時回源）用 request coalescing / mutex lock / 邏輯過期；雪崩（大量 key 同時過期）用 TTL 加 jitter；穿透（查不存在的 key）用 negative cache 或 Bloom filter | 三個名詞混為一談；只會說「加鎖」但講不出鎖加在哪、誰去回源 |
| "TTL 要設多久？怎麼決定？" | 沒有萬用值，從兩個軸推：資料容忍多舊（business staleness budget）+ 變更頻率；寫少讀多可以長 TTL + 主動 invalidation；給出範例數字（商品價格 30s-5min、用戶 profile 1h）；TTL 加 jitter 防雪崩 | 答一個數字（"5 分鐘"）卻講不出推導；不知道 TTL 和 invalidation 可以並用 |
| "Cache 和 DB 不一致怎麼處理？" | 先講「先更 DB 再刪 cache」（cache-aside + delete）是業界 default、為什麼不是 update cache（並發寫亂序）、刪除失敗的兜底：CDC/binlog 異步補刪、或短 TTL 當最終防線、要強一致就別用 cache 或上鎖（代價講清楚） | 說「write-through 就一致了」（並發下仍有窗口）；沒有 fallback 方案 |
| "熱 key 問題怎麼解？比如某明星商品被瘋搶。" | 偵測：per-key metrics / 抽樣統計；解法分層：local cache（in-process，毫秒級 TTL）、key 打散（key#1..N 隨機讀）、read replica 分流；說明 local cache 的代價：多副本不一致窗口 | 只說「加更多 Redis」（單 key 在單 shard 上，加節點沒用）；不知道 consistent hashing 下熱 key 不會自動分散 |
| "CDN 快取了舊版 JS 導致前端壞掉，怎麼辦？怎麼預防？" | 立即：CDN purge/invalidation（講出生效時間不是瞬間）；預防（正解）：content-hash filename（app.a1b2c3.js）讓靜態資源 immutable + 長 TTL，HTML 短 TTL 或 no-cache；版本化部署 | 只會 purge，不知道 cache busting by filename 是業界標準；HTML 和 asset 的 TTL 策略混在一起講 |

### Database Selection

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "為什麼選 NoSQL？SQL 哪裡不行？" | 先反過來：default 是 SQL（transaction、join、成熟生態），NoSQL 要有具體理由：寫入量超過單機（>10K writes/s 級）、schema 高度彈性、特定 access pattern（KV、time-series、graph）；用數字支撐而不是信仰 | "因為要 scale 所以 NoSQL"（Postgres 分片照樣 scale）；講不出自己 QPS 估算就選型 |
| "你的分片（shard key）怎麼選？選錯會怎樣？" | 從 access pattern 反推：最高頻查詢要能單分片命中、檢查 cardinality 和分佈均勻度、選錯的後果：hot partition（如用 date 當 key，今天的分片被打爆）、cross-shard query 變 scatter-gather；改 shard key 是大手術，要 resharding | 用 auto-increment id 或 timestamp 當 shard key 還說「很均勻」；沒考慮查詢路由 |
| "B-tree 和 LSM-tree 差在哪？什麼場景選哪個？" | B-tree：原地更新、讀友好（O(log N) 一次定位）、寫放大來自 random IO；LSM：append-only、寫友好（sequential write）、讀要查多層（memtable + SSTables）用 Bloom filter 補救、有 compaction 成本；read-heavy 選 B-tree 系（MySQL/PG），write-heavy 選 LSM 系（Cassandra/RocksDB） | 背名詞但講不出「為什麼 LSM 寫快」（sequential vs random IO 的物理差異）；不知道 compaction 會吃 IO 影響線上 |
| "Index 加越多越好嗎？" | 每個 index 是一份額外寫入成本（寫放大）+ 儲存成本、寫入 QPS 高的表要克制、composite index 的最左前綴原則、實務：用 slow query log / execution plan 驗證後才加 | "查得慢就加 index" 無腦加；不知道 index 拖慢寫入 |
| "資料量到 10TB、單表 50 億列，你會怎麼做？" | 分層回答：先確認 access pattern（也許大半是冷資料可以歸檔）、垂直拆（按 column/功能）、水平分片（shard key 設計）、冷熱分離（hot 在 DB、cold 到 object storage）、講 migration 怎麼做（dual write / backfill / cutover） | 直接說「上 Cassandra」跳過歸檔和冷熱分離；不提 migration 路徑 |
| "Read replica 解決什麼？不能解決什麼？" | 解決：讀流量水平擴展、讀寫分離降低主庫壓力；不能解決：寫入瓶頸（所有寫還是進 leader）、replication lag 造成 read-after-write 問題（解法：關鍵讀走 leader、session 黏性、或等 LSN）；replica 數量有上限（複製風扇出成本） | 以為 replica 能擴寫入；不知道 lag 會讓用戶「發了文自己看不到」 |

### Message Queue & Async Processing

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Consumer 處理到一半掛了，這條訊息會怎樣？" | 取決於 ack 時機：先 ack 後處理會丟訊息（at-most-once）、先處理後 ack 會重複處理（at-least-once）、visibility timeout / redelivery 機制、結論：default 用 at-least-once + consumer 端冪等 | 說「queue 會保證不丟不重」；不知道 exactly-once 不能只靠 broker |
| "重複訊息怎麼處理？冪等具體怎麼做？" | 冪等 key 的選擇（業務 id 如 order_id，不是 message_id 因為 producer retry 會生成新 id）、儲存：unique constraint / Redis SETNX、dedup window 多久（依業務重試週期）、副作用外溢怎麼辦（如已發 email 不可回收，盡量把副作用放最後一步） | 只說「做冪等」沒講 key 存哪、TTL 多久；用 message_id 去重但 producer 重送會換 id |
| "Queue 一直堆積（backlog 暴漲），你怎麼處理？" | 先判斷：consumer 掛了還是吞不動（看 consumer lag + error rate）、短期：scale out consumer（注意 partition 數是並行上限）、降級非關鍵 producer、長期：容量規劃 + backpressure、設 alert 在 lag 而不是 queue depth 絕對值 | 只會「加 consumer」（Kafka partition 數卡死並行度時加了沒用）；不知道要監控 lag |
| "什麼訊息該進 DLQ？進去之後呢？" | retry N 次仍失敗的 poison message（區分 transient error 該重試 vs permanent error 直接進 DLQ）、DLQ 要有 alert + 人工/自動 replay 流程、replay 前要確認 bug 已修，否則重新中毒 | 把 DLQ 當垃圾桶（進去就沒人管）；transient 和 permanent error 用同一種 retry 策略 |
| "訊息順序怎麼保證？真的需要全局有序嗎？" | 先挑戰需求：通常只需要 per-key 有序（同一訂單的事件有序），不需要全局、Kafka 同 partition 有序（用 order_id 當 partition key）、SQS FIFO 的 message group、全局有序 = 單 partition = 吞吐上限，講出這個代價 | 不假思索答「用 FIFO queue」犧牲吞吐；不知道 partition key 就能解決大多數順序需求 |
| "為什麼不直接同步呼叫就好？async 帶來什麼新問題？" | async 的代價要主動講：最終一致（用戶看不到即時結果）、追蹤困難（要 correlation id）、失敗處理複雜（retry/DLQ/監控）、何時不該用 queue：需要即時回饋的同步流程（如付款授權結果） | 把 queue 當銀彈到處塞；講不出「什麼時候同步反而對」 |

### API Design

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Offset pagination 在大表深翻頁會怎樣？怎麼解？" | OFFSET 100000 要掃過前 10 萬列再丟掉（O(offset)）、且翻頁過程資料插入會位移（漏看或重複）、cursor-based：用上一頁最後一筆的 sort key 當游標（WHERE id > cursor LIMIT n）、代價：不能跳頁 | 不知道 offset 的效能是線性劣化；說 cursor 好但講不出 cursor 是什麼（就是個編碼過的 sort key） |
| "POST 請求 timeout 了，client 該 retry 嗎？" | 核心：client 不知道 server 到底做了沒（timeout 是未知狀態不是失敗）、retry 必須配 idempotency key（client 生成、server 用它去重）、講 Stripe 的 Idempotency-Key header 實例、retry 策略：exponential backoff + jitter + 上限 | "retry 就好了"（重複下單/扣款）；或「不能 retry」（可用性差）；不知道冪等 key 由誰生成 |
| "API 要改 breaking change，幾百個 client 在用，怎麼辦？" | versioning 策略（URL /v2 或 header）、新舊並行 + deprecation period（公告、監控舊版流量、設 sunset date）、能不 break 就不 break：加欄位向後相容、用 API gateway 做轉換層過渡 | 「直接升 v2 叫大家改」；不知道要監控舊版本還有誰在用才能下線 |
| "REST 和 gRPC 你怎麼選？" | 邊界內外分開談：對外 public API 用 REST/JSON（生態、可讀、瀏覽器原生）、內部 service-to-service 用 gRPC（強 schema、HTTP/2 multiplexing、binary 省頻寬、streaming）、講出 gRPC 的代價：瀏覽器支援差（要 grpc-web）、debug 較難 | 只比效能不比生態和場景；不知道 gRPC 走 HTTP/2 帶來什麼（multiplexing、header 壓縮） |
| "怎麼設計批次操作 API？部分成功怎麼回？" | batch endpoint 的回應要 per-item status（207 Multi-Status 概念）、整批原子 vs 部分成功要先跟 client 約定、batch size 上限 + 文件寫清楚、冪等同樣適用（batch id） | 回 200 但部分失敗藏在 body 裡沒人看；沒設 batch 上限被人一次塞 10 萬筆 |

### Security & Authentication

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "JWT 怎麼做登出 / 撤銷？" | 戳破核心矛盾：JWT 的賣點是 stateless，但撤銷需要 state、解法：短 access token（5-15min）+ refresh token（存 DB 可撤銷）、或 denylist（只存被撤銷的 jti，量小）、講出「完全即時撤銷 = 每次驗證查狀態 = 退回 stateful」這個 trade-off | 說「把 JWT 從 client 刪掉就登出了」（token 還是有效的）；不知道 refresh token rotation |
| "JWT 和 session 你選哪個？" | 從架構需求推：單體或同域 web app 用 session（成熟、好撤銷）、跨服務/跨域/mobile 用 JWT（不用共享 session store、服務各自驗簽）、JWT 的坑：payload 不加密只簽名（別放敏感資料）、token 變大每請求都帶 | 背「JWT 比較現代」；不知道 session + Redis 在多數場景完全夠用 |
| "API key 洩漏了怎麼辦？你的系統怎麼把傷害降到最小？" | 偵測：異常流量/地理位置 alert；止血：立即 revoke + rotate；降害設計（事前）：key 綁最小權限（scope）、綁 IP/referrer、設 rate limit、key 分環境、secrets 不進 code（用 secrets manager + 自動 rotation） | 只答「換一把 key」；沒講事前的 blast radius 控制（最小權限、scope） |
| "OAuth 2.0 的 authorization code flow 為什麼要多一步換 code？" | 核心：access token 不經過瀏覽器前端（front channel 只傳一次性 code，back channel 用 client secret 換 token）、防 token 被攔截/留在 browser history、public client（SPA/mobile）沒有 secret 所以要 PKCE | 背流程圖但講不出「為什麼不直接回 token」；不知道 PKCE 解什麼問題 |
| "內部服務之間需要驗證嗎？都在 VPC 裡面欸。" | zero trust 觀念：網路邊界不等於信任邊界（內網淪陷、SSRF、誤設定）、service-to-service auth：mTLS 或 service mesh、IAM role/service account、講 defense in depth、實務上至少做到：內部 API 也要 authn + authz | "內網很安全不用驗"（紅旗答案）；把 network security group 當作唯一防線 |

### Consistent Hashing & Data Partitioning

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "為什麼 hash mod N 不行？加一台機器會怎樣？" | mod N 在 N 變動時平均 (N-1)/N 的 key 要搬家（幾乎全部）、consistent hashing 只搬 K/N、量化講：100 台加 1 台，mod 法搬 99%，CH 搬約 1%、搬移期間 cache miss 風暴打爆 DB | 知道結論但算不出搬移比例；講不出「搬移」在 cache 場景的實際傷害是 miss 風暴 |
| "Virtual node 解決什麼問題？要幾個？" | 兩個問題：節點少時分佈不均（standard deviation 大）+ 節點異質（強機器多拿 vnode）、數量級：每實體節點 100-200 個 vnode 是常見值、代價：metadata 變大、查詢 ring 的成本微增 | 知道 vnode 但講不出「不用 vnode 會多不均」；vnode 數量信口開河沒有數量級概念 |
| "一個節點掛了，它的資料/流量去哪？" | ring 上順時針流到下一個節點、無 vnode 時鄰居節點承受 2 倍壓力可能連鎖崩、vnode 把故障節點的負載打散到全環、若是 storage（非 cache）還要講 replication：每份資料存順時針 N 個後繼節點 | 只答「給下一個節點」沒看出鄰居過載的連鎖風險；分不清 cache（掉了就 miss）和 storage（掉了要 replica）場景 |
| "Range-based 和 hash-based partitioning 怎麼選？" | hash：分佈均勻但失去順序（range scan 變 scatter-gather）；range：range query 高效但有 hot range 風險（時間序資料最新分區最熱）、實例：DynamoDB hash key、HBase range、複合策略：hash(tenant) + range(time) | 不知道 hash 完就不能高效 range scan；time-series 資料用 range partition 卻沒提 hot partition |
| "Rebalancing 進行中，讀寫怎麼不出錯？" | 搬移期間的 routing：雙讀（先新後舊）或 proxy 層維護 migration state、寫入：dual write 或先寫舊再 backfill + cutover、要有 fencing 避免新舊節點同時認為自己擁有該分區、講 migration 是漸進的不是瞬間的 | 假設 rebalance 是原子瞬間完成；沒想過搬移中讀到一半舊一半新的問題 |

---

## Phase 2: Distributed Systems Core

### CAP / PACELC

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "你說這系統選 AP，那 partition 的時候用戶會看到什麼？" | 具體化：兩側都可寫導致衝突（之後要 conflict resolution）、用戶可能看到舊資料、舉實際場景（購物車兩邊加商品，合併用 union）、partition 癒合後的收斂機制（LWW、vector clock、CRDT 擇一講） | 只會說「選擇可用性」，講不出用戶體感和衝突怎麼收斂 |
| "沒有 partition 的平常時候，就沒有 trade-off 了嗎？" | 這就是 PACELC 的 ELC：Else 的時候 trade Latency vs Consistency、同步複製 = 一致但每寫都等 quorum（延遲高）、異步複製 = 低延遲但有 lag、舉例：DynamoDB 預設 PA/EL，Spanner PC/EC（用 TrueTime 花錢買一致） | 以為 CAP 講完就沒了；不知道平時的 latency vs consistency 才是日常面對的選擇 |
| "CA 系統存在嗎？" | 單機系統（無 partition 可言）勉強算、分散式系統中 partition 不可選（網路一定會斷），所以實際只能選 CP 或 AP、傳統單機 RDBMS 常被稱 CA 但一做 replication 就要面對 P | 答「MySQL 是 CA」然後被追問 replication 場景就垮掉 |
| "Zookeeper 是 CP，那 partition 時少數派那邊會怎樣？" | 少數派無法形成 quorum：拒絕寫入（犧牲 A 保 C）、依賴 ZK 的服務在那一側會拿不到鎖/config、所以 CP 系統的部署要算 quorum 數（2N+1 容忍 N 台掛）、跨 AZ 部署要奇數成員 | 背「ZK 是 CP」但講不出少數派「不可用」具體長什麼樣 |
| "你會怎麼跟 PM 解釋這個系統為什麼偶爾讀到舊資料？" | 翻譯能力考察：用 business 語言講 staleness budget（「最多舊 X 秒，換來不宕機和低延遲」）、給選項和標價（強一致要多花多少錢/多慢）、讓 business 做 informed decision | 用術語轟炸 PM（quorum、PACELC）；或反過來答應 PM「我讓它完全一致」不講代價 |

### Consistency Models

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "用戶發完留言重新整理後看不到自己的留言，怎麼修？" | 這是 read-your-writes 問題（replication lag + 讀到 replica）、解法分層：關鍵讀走 leader、session sticky（同 session 讀同 replica）、client 記 LSN/timestamp 要求 replica 追上才回、最便宜：前端樂觀顯示（local echo） | 直接說「上強一致」（全系統陪葬延遲）；不知道一致性可以 per-operation 選擇 |
| "W + R > N 是什麼意思？W=1, R=1, N=3 會怎樣？" | quorum 重疊原理：讀寫集合必有交集所以能讀到最新寫、W=1,R=1,N=3：讀寫都快但 1+1 < 3 無重疊，可能讀到舊值（最終一致）、W=N 寫慢但讀快、用「調 W/R 是調 latency vs consistency 的旋鈕」收尾 | 背公式但給具體數字就不會推；不知道 quorum 也擋不住 sloppy quorum / hinted handoff 的邊角 |
| "兩個資料中心同時改同一筆資料，誰贏？" | 先講偵測：LWW（簡單但會默默丟寫入 + 依賴時鐘）、vector clock（偵測並發但要應用層 merge）、CRDT（資料結構自動收斂，限特定型別）、business 邏輯決定 merge 策略（購物車 union、餘額不能 LWW） | 只會 LWW 且不知道 LWW 會丟資料；把 vector clock 講成「精確時鐘」 |
| "Causal consistency 解決什麼？舉個沒有它會出糗的例子。" | 例子要熟：回覆比原留言先出現（A 問 B 答，C 只看到答案）、機制：因果關係追蹤（session 或 vector clock），有因果關係的寫入按序可見，無關寫入可亂序、強度：比 eventual 強、比 linearizable 弱也便宜 | 舉不出體感例子；把 causal 和 strong 混為一談 |
| "你的系統哪些操作需要強一致、哪些可以最終一致？" | 展示分級思維：錢和庫存（強）、計數器和按讚數（最終）、用戶自己的寫入（read-your-writes 即可）、講出「一致性是 per-operation 的 menu 不是全系統開關」、每升一級標出延遲/可用性代價 | 全系統一刀切；說不出具體操作的分級理由 |

### Replication & Leader Election

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Leader 掛了，failover 過程會發生什麼壞事？" | 三大坑：async replication 下新 leader 缺最後幾筆寫入（資料丟失）、舊 leader 復活造成 split brain（要 fencing/epoch number）、failover 期間寫入不可用（幾秒到幾十秒）、auto failover 的誤判（網路抖動造成不必要切換） | 以為 failover 是無痛自動的；沒聽過 fencing token / epoch |
| "Split brain 怎麼防？" | quorum：只有拿到多數派承認的才能當 leader（2N+1）、fencing：舊 leader 的寫入帶舊 epoch 被拒、lease：leader 身份有租期要續約、STONITH 概念（確保舊 leader 真的死了） | 只說「用 Zookeeper」當咒語，講不出 quorum 和 fencing 的原理 |
| "為什麼 Raft 需要多數派？3 台掛 1 台和掛 2 台差在哪？" | 多數派確保任兩個 quorum 必相交（不會選出兩個 leader、不會丟 committed 資料）、3 台容忍 1 台（剩 2 > 3/2）、掛 2 台剩 1 台無法成 quorum：系統停寫保正確性、所以容錯 N 台需要 2N+1 | 算不出 quorum 數；不理解「停止服務」是 CP 系統故意的設計 |
| "Multi-leader 什麼時候用？最大的痛是什麼？" | 場景：multi-region 寫入就近（跨洋 RTT 100ms+ 的物理限制）、離線設備同步、最大的痛：寫衝突無法避免只能 resolve（LWW/merge/CRDT）、建議：能用 single-leader + 就近讀就別碰 multi-leader | 為了「聽起來厲害」選 multi-leader 卻講不出衝突解決方案 |
| "Replication lag 多大算正常？lag 暴增你怎麼查？" | 正常：同 region 毫秒級、跨 region 幾十到幾百 ms、查法：是寫入暴增（producer 端）還是 replica 消化慢（IO/lock/長交易）、監控 replica lag metric + alert、lag 大時的降級：把 read-your-writes 流量導回 leader | 沒有數量級概念；不知道 lag 是必須監控的 SLI |

### Rate Limiting & Circuit Breaker

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Token bucket 和 sliding window 怎麼選？" | 從流量型態推：允許短 burst（API 偶發高峰）用 token bucket（bucket size = 允許的 burst 量）、嚴格平滑限制（防爬蟲、保護脆弱下游）用 sliding window、講 fixed window 的邊界問題（窗口交界處 2 倍流量）當對照 | 背演算法但講不出「burst 容忍度」這個選擇軸；不知道 fixed window 的雙倍邊界漏洞 |
| "分散式環境下 counter 放哪？Redis 掛了限流器怎麼辦？" | 集中式 counter（Redis + Lua 原子操作）vs 本地限流（每節點 limit/N，省一跳但不準）、Redis 掛了的 policy 決策：fail open（放行，保可用）vs fail closed（全擋，保護下游）、依場景選：付費 API 配額 fail closed、一般防護 fail open + alert | 沒想過 limiter 本身會掛；說不出 fail open/closed 是 business 決策 |
| "被限流的請求你回什麼？client 應該怎麼做？" | HTTP 429 + Retry-After header + rate limit headers（X-RateLimit-Remaining）、client 端 exponential backoff + jitter（防 retry 同步化造成第二波）、區分用戶級限流（429）和系統過載（503） | 回 500 讓 client 無腦重試（雪上加霜）；不知道 jitter 防的是 thundering herd |
| "Circuit breaker 的閾值怎麼定？Half-open 是幹嘛的？" | 閾值用 error rate + 最小請求數（如 10 秒內 ≥20 請求且 50% 失敗才 open，避免低流量誤判）、half-open：放少量探測請求驗證下游復原，成功關閉、失敗重新 open、沒有 half-open 就永遠不會自動復原或盲目全開二次打掛 | 隨口說個閾值沒有最小樣本數概念；不知道 half-open 存在的理由 |
| "Rate limit 應該放在哪一層？Gateway 還是每個 service？" | 分層：edge/gateway 擋 per-user/per-IP（粗粒度、擋外部濫用）、service 層擋 per-dependency（保護自己的下游）、兩層互補不是二選一、集中 config 管理（改 limit 不用部署） | 只放一層；gateway 限流後以為內部就不需要保護 |
| "Retry 加 circuit breaker 一起用，有什麼要注意？" | retry 放大流量（3 次 retry = 4 倍請求），下游半死時 retry 風暴補刀、所以 retry 要看 breaker 狀態 + retry budget（如最多 10% 流量是 retry）、冪等才能 retry、整條 call chain 的 retry 會指數放大（每層 3 次，3 層 = 27 倍） | 不知道 retry 會跨層放大；retry、timeout、breaker 三者沒有整體觀 |

### Observability

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "你會設哪些 alert？怎麼避免 alert 疲勞？" | alert on symptom not cause（SLO burn rate、error rate、P99，而不是 CPU 80%）、每個 alert 要 actionable（有 runbook）、分級：page（半夜叫醒人）vs ticket（明天處理）、定期 review 沒人理的 alert 就刪 | 列一堆資源型 alert（CPU/memory）；alert 沒有對應行動；不知道 burn rate alert |
| "P99 latency 突然飆高，平均值正常，怎麼查？" | 長尾問題的排查路徑：先看是全局還是特定維度（endpoint/region/用戶群，用 tracing 切片）、常見根因：GC pause、慢查詢、重試放大、單一慢依賴、connection pool 耗盡、為什麼平均沒動：1% 的慢被 99% 稀釋、所以 SLO 要定在 percentile 不是 mean | 只看平均值；說「加機器」不先定位；不知道 P99 對大 fan-out 服務的放大效應（呼叫 100 個服務，P99 變體感常態） |
| "Metrics、logs、traces 各自回答什麼問題？" | metrics：what（系統現在怎樣，便宜、可 alert）、logs：why（具體事件細節，貴、高基數）、traces：where（請求在哪個服務段慢，跨服務因果）、串起來的關鍵：correlation id / trace id 貫穿三者 | 三個都講但講不出怎麼互相 pivot（從 metric 異常跳到對應 trace 再跳到 log） |
| "Tracing 全量採集太貴，怎麼辦？" | sampling 策略：head-based（入口決定，便宜但可能漏掉出錯的請求）vs tail-based（看完整條 trace 再決定留不留，能保證留下 error/慢請求但要 buffer）、實務組合：錯誤和慢請求 100% 留、正常請求採 1% | 不知道 sampling 存在；或只知道採樣率不知道 head/tail 的差異 |
| "SLO 99.9% 和 99.99% 差在哪？你怎麼選？" | 換算 error budget：99.9% = 每月約 43 分鐘、99.99% = 4.3 分鐘、每加一個 9 成本超線性增長（架構冗餘、on-call、發布速度變慢）、從 business 反推：用戶感知和合約要求，不是越多 9 越好、error budget 當發布節奏的調節器 | 張口就要 99.999% 不講成本；不會把 % 換算成分鐘給人體感 |

---

## Tier 1 Classic Problems

### URL Shortener

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "兩個人同時縮同一個長網址，要回同一個短碼嗎？" | 先反問需求（去重是 nice-to-have 不是必須）、要去重：long URL hash 加 unique index，衝突時回已存在的、不去重更簡單且支援 per-user 統計、講出這是 business 決策不是技術難題 | 沒意識到這是需求釐清問題，直接鑽進技術；為了去重把寫入路徑搞複雜 |
| "短碼怎麼生成？hash 截斷會有什麼問題？" | hash 截斷（MD5 取前 7 碼）有碰撞要 retry 探測、counter + base62 無碰撞但 ID 可預測（被遍歷爬取）+ 中心化 counter 是瓶頸、改良：分段發號（每節點領一段 range）、隨機化或加密 counter 防遍歷 | 說「用 hash 就好」不提碰撞處理；不知道循序 ID 可被遍歷是安全問題 |
| "301 還是 302？對 analytics 有什麼影響？" | 301（permanent）：瀏覽器永久快取，之後不再經過你的 server，analytics 丟失、302/307：每次都回源，能記錄點擊但多一跳延遲、要 analytics 就用 302，純轉址用 301 省流量、這是經典「技術細節背後是 business 需求」考點 | 不知道 301 會被瀏覽器快取導致數據蒸發；隨便選一個講不出差異 |
| "讀寫比 100:1，你的架構哪裡要為這個優化？" | read path 全力優化：cache（redirect 是 KV 查詢，hit ratio 可以很高）、DB 選 KV 型或加 read replica、估算：cache 95% hit 之後 DB 只剩 5% 讀流量、write path 簡單不用過度設計 | 沒把讀寫比轉化成架構決策；對 write path 過度設計（分散式發號搞很複雜但寫入根本不大） |
| "有人用你的服務縮惡意網址，怎麼辦？" | 建立：建立時比對 URL blocklist（Google Safe Browsing API）、事後：被檢舉的短碼下架（軟刪除 + 快取失效）、rate limit 防批量建立、redirect 前插 interstitial 警告頁（高風險網域） | 完全沒想過 abuse（這題的隱藏考點）；只說「封鎖」沒講偵測來源 |
| "10 倍流量之後，第一個掛的是哪個元件？" | 用估算回答：先給當前 QPS 假設，乘 10 後逐層檢查（LB、cache、DB、發號器）、通常答案是 cache miss 後的 DB 或熱 key、講出「我會先看 metrics 確認瓶頸再動手」的工程素養 | 憑感覺亂指；給不出任何數字就說「DB 會掛」 |

### Unique ID Generator

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "為什麼不直接用 UUID？" | 先肯定 UUID 的適用面（無協調、衝突機率可忽略）、再講缺點：128-bit 太長、UUIDv4 完全無序導致 B-tree index 寫入隨機分佈（page split、cache 不友好）、需要 time-ordered 就用 Snowflake/ULID/UUIDv7、用「需求是否要有序」當決策軸 | 一句「UUID 會重複」（機率上不成立）；不知道無序 ID 對 index 的傷害 |
| "Snowflake 的機器時鐘往回跳了，會發生什麼？怎麼處理？" | clock 回撥 + 同 sequence 會生成重複 ID、處理選項：拒發等時鐘追上（小回撥）、用邏輯時鐘繼續、回撥太大直接告警下線該節點、預防：NTP 平滑校時（slew 不是 step）、不依賴 wall clock 改用單調時鐘思路 | 不知道 clock skew 是 Snowflake 的核心弱點；說「時鐘不會錯」 |
| "Worker ID 怎麼分配？兩台機器拿到同一個 ID 會怎樣？" | 撞 worker ID = 同毫秒可能發出重複 ID（靜默資料污染，比當機可怕）、分配方案：Zookeeper/etcd 註冊（租約制）、配置中心靜態分配、K8s StatefulSet ordinal、要處理租約過期但程序還活著的 fencing 問題 | 忽略這個運維問題；用「隨機選一個」當分配方案 |
| "一毫秒內 sequence 用完了（超過 4096 個）怎麼辦？" | 自旋等下一毫秒（最簡單，犧牲一點延遲）、或借未來時間戳（有風險）、先算需求：4096/ms = 單節點 400 萬/s，多數場景根本到不了，講出「先估算再擔心」 | 沒算過 4096/ms 是什麼量級就開始過度設計 |
| "ID 連續遞增會洩漏什麼商業資訊？" | 可被推算業務量（德國坦克問題：對手用訂單 ID 差值估你的單量）、防法：sequence 起始隨機化、ID 加密/混淆後對外、內外 ID 分離（內部用 Snowflake、對外用隨機短碼） | 沒想過 ID 是資訊洩漏面；把內部 ID 直接曝露在 URL |

### Distributed Rate Limiter

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Redis 是你的 counter store，它掛了怎麼辦？" | 先講 policy：fail open vs fail closed 是 business 決策（防濫用場景 fail open + alert、計費配額 fail closed）、技術緩解：Redis HA（replica + sentinel/cluster）、降級到 local in-memory 限流（每節點 limit/N 近似值）、絕不能讓 limiter 故障變成全站故障 | 沒有 fail policy 思維；說「Redis 不會掛」；降級方案會讓限流完全失效也沒提 |
| "Check 和 increment 之間有 race condition，怎麼解？" | read-modify-write 在並發下超賣 quota、解法：Lua script 把 check+incr 原子化（單線程執行）、或 INCR 先加再判斷（超了就拒絕，天然原子）、不要用分散式鎖（為一個 counter 上鎖是殺雞用牛刀，延遲爆炸） | 沒看出 race；提出用分散式鎖（面試官會追問鎖的成本直到你垮） |
| "每個請求都要過 Redis，這一跳的 latency 和瓶頸怎麼辦？" | 量化：Redis 單節點 10 萬+ ops/s、加一跳約 1ms 內網 RTT、超過單節點就 shard by user_id（限流 key 天然可分片）、進一步：local cache + 批次同步（每節點先扣本地配額，定期跟 Redis 對帳，犧牲精確度換延遲）、講出「精確 vs 效能」這條 trade-off 軸 | 沒意識到 limiter 自己會成為瓶頸；不知道「允許少量誤差」能換來巨大簡化 |
| "Sliding window log 和 sliding window counter 差在哪？" | log：存每個請求 timestamp（ZSET），精確但記憶體 O(rate)、counter：當前窗口計數 + 前窗口加權近似，O(1) 記憶體但有近似誤差、量化：每用戶 1000 req/min 的 log 要存 1000 個 timestamp，百萬用戶就是 GB 級、多數場景 counter 的誤差完全可接受 | 只知道一種；講不出 log 法的記憶體代價數量級 |
| "不同用戶要不同的 limit（免費 100/min、付費 10000/min），怎麼設計？" | rule/config service：limit 規則外部化（不寫死在 code）、層級：per-user 覆蓋 per-tier 覆蓋 default、規則熱更新（limiter 訂閱 config 變更）、回應帶 X-RateLimit-Limit 讓 client 知道自己的額度 | 把 limit 寫死；沒想過規則變更不能重新部署 |
| "怎麼驗證你的 rate limiter 沒有誤殺？上線策略是什麼？" | shadow mode 先跑（只記 log 不真擋）、比對 would-be-blocked 流量是不是真濫用、灰度放量、dashboard：block rate by rule、誤殺的客訴回路、這題考 operational maturity | 直接全量上線；沒有 shadow/dry-run 概念 |

### Notification System

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "用戶收到兩次同一則推播，哪裡出了問題？怎麼防？" | 重複來源逐層列：producer retry、queue at-least-once redelivery、worker 處理完沒 ack、防法：notification id + dedup（發送前查 sent log / Redis SETNX，TTL 覆蓋重試窗口）、講出「推播發出去就收不回」所以 dedup 要在發送動作之前 | 只查一層原因；dedup 放在發送之後（已經晚了） |
| "第三方（APNs/FCM/SMS gateway）掛了或變慢，你的系統會怎樣？" | 隔離：per-channel queue + worker pool（SMS 掛不拖累 push）、circuit breaker 對第三方、降速 + 退避重試（第三方有自己的 rate limit）、可選 channel fallback（push 失敗轉 SMS，注意成本和用戶體感）、backlog 監控 | 所有 channel 共用一條 pipeline（一個第三方掛全部堵死）；無腦 retry 把第三方打更死 |
| "行銷要對 1000 萬用戶群發，怎麼不影響交易通知（OTP）？" | priority queue：transactional（OTP、交易）和 marketing 分隊列分 worker pool、群發要 rate control（保護第三方 quota 和自家 DB 查詢）、批次拉取用戶分片處理、OTP 的 SLA 是秒級，行銷可以攤平到小時級 | 一條 queue 混所有流量（OTP 排在 1000 萬則行銷後面）；不知道 priority 要靠「分隊列」實現而不是排序 |
| "怎麼知道用戶真的收到了？送達率怎麼算？" | 分層 funnel：sent（我方發出）→ delivered（第三方回執/device ack）→ opened（client 埋點）、各層 metrics + 分 channel 監控、APNs/FCM 的 feedback（token 失效要清理，否則送達率虛低）、講出「invalid token 清理」是 operational 重點 | 以為發出去 = 送達；不知道 device token 會過期失效 |
| "用戶設定『晚上不要吵我』，這個檢查放在哪一層？" | user preference service：發送前 worker 檢查（quiet hours、channel opt-out、frequency cap）、preference 查詢要 cache（每則通知都查 DB 撐不住）、時區處理（quiet hours 是用戶當地時間）、被壓制的通知怎麼辦：丟棄 vs 延遲到早上（business 決策） | 把 preference 檢查放在 producer（每個業務方都要重複實作）；忘記時區 |

### Chat System

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "為什麼用 WebSocket 不用 polling？代價是什麼？" | 比較三件套：short polling（延遲高、空輪詢浪費）、long polling（即時性可、連線反覆重建）、WebSocket（全雙工、低延遲、但 stateful）、WebSocket 的代價要講足：connection state 讓 server 不再無狀態、LB 要支援、斷線重連邏輯、百萬連線的記憶體成本（每連線數十 KB） | 只說 WebSocket 快；講不出 stateful 對部署和擴展的衝擊 |
| "用戶 A 連在 server 1，用戶 B 連在 server 2，訊息怎麼送過去？" | 核心是 connection registry：user → gateway server 的映射（Redis）、跨機路由：查 registry 直接轉發、或 pub/sub（每個 gateway 訂閱自己持有用戶的 channel）、講出 gateway（連線層）和 message service（邏輯層）分離的理由：連線層要輕、擴展節奏不同 | 假設所有人連在同一台；沒有 connection registry 概念，說「廣播給所有 server」（不 scale） |
| "訊息順序怎麼保證？client 顯示亂序怎麼辦？" | 全局有序不需要也做不到，per-conversation 有序就夠、server 端：同一 conversation 的訊息走同一 partition / 單一 sequencer 發 per-conversation seq id、client 端：按 seq id 排序渲染、發現 gap 就拉 API 補洞 | 追求全局時間戳排序（時鐘不可信）；沒有 client 端補償機制 |
| "用戶離線三天，重新上線怎麼同步訊息？" | inbox model：訊息持久化到收件箱（per-user 或 per-conversation cursor）、上線後增量拉取（自上次 sync cursor 之後的）、大量未讀要分頁 + 摘要（只拉每個會話最新 N 則 + unread count）、多裝置：每裝置自己的 cursor | 只想到 push 沒想到 pull 補課；多裝置同步完全沒考慮 |
| "已讀回條在 500 人群組會發生什麼？" | 量化放大：一則訊息 500 人已讀 = 500 個 receipt 事件 x 推給 500 人 = 25 萬次推送、收斂手段：batch + debounce（聚合幾秒內的已讀再推）、大群降級成「已讀人數」不列名單、或乾脆大群不做已讀（產品決策）、講出 read receipt 是典型 write 放大問題 | 沒算出 N² 放大；直接說「就推啊」 |
| "presence（在線狀態）為什麼難做？" | 心跳機制：TCP 斷線偵測不可靠所以要 application-level heartbeat（30s 級）+ timeout 判離線、狀態傳播是 fan-out 問題（一人上線要通知所有好友）、優化：只推給「正在看著你的人」（打開聊天視窗的）、presence 允許不準（最終一致，遲 30 秒沒人在乎），用這個放寬大幅降成本 | 想做即時精確 presence（成本爆炸）；不知道「降低精確度」是這題的正解方向 |

### Distributed Cache

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "一個 cache 節點掛了，會發生什麼連鎖反應？" | 該節點的 key 全 miss 打到 DB（量化：20 節點掛 1 台 = 5% 流量回源，可承受；掛一半就危險）、consistent hashing 讓 miss 範圍只限該節點、可加 replica（每 shard 一主一從）降 miss、DB 端保護：request coalescing + 連線上限 | 沒量化 miss 的爆炸半徑；不知道 cache 層 replica 和 DB replica 目的不同（前者防 miss 風暴） |
| "怎麼做 cache invalidation at scale？" | 三條路線並用：TTL 當 baseline（最終防線）、event-driven（資料變更發 invalidation event，CDC/binlog 驅動最可靠因為不漏）、versioning（key 帶版本，改資料就換 key，舊的等 TTL 自然死）、講 invalidation message 自己也會丟所以 TTL 不可省 | 只講 TTL 或只講主動失效；不知道 CDC 比應用層雙寫可靠在哪（不會漏） |
| "Thundering herd：熱 key 過期瞬間一萬個請求打進來，怎麼辦？" | request coalescing：單飛模式（singleflight），同 key 並發 miss 只放一個回源其他人等結果、邏輯過期：cache 不真過期，值內帶過期時間，過期後一個請求去刷新、其他人先吃 stale、提前刷新（過期前異步 refresh）、講出「stale 幾秒通常可接受」是解題鑰匙 | 只會加鎖但講不清鎖粒度（per-key 不是全局）；不知道 serve-stale 這個選項 |
| "Client 怎麼知道某個 key 在哪個節點？路由放哪裡？" | 三種拓撲：client-side sharding（client 內建 ring，省一跳但升級難）、proxy 層（Twemproxy/Envoy，集中路由好運維但多一跳）、cluster protocol（Redis Cluster 的 MOVED redirect，去中心化）、選擇軸：團隊運維能力 + client 語言多樣性 | 不知道路由是個要設計的問題；只背 Redis Cluster 但講不出 client-side vs proxy 的 trade-off |
| "Cache 要不要做持久化？重啟後冷快取怎麼辦？" | cache 的定位是可丟資料（truth 在 DB）所以通常不持久化、但冷啟動 miss 風暴是真問題：cache warming（重啟前預載熱 key list）、漸進放量（新節點先接小流量）、Redis 場景 RDB 快照可加速重啟回血、別把 cache 當 DB 用（有人真的會） | 把持久化當理所當然（混淆 cache 和 storage 的定位）；沒有 warming 概念 |

### News Feed

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "Fan-out on write 和 on read 怎麼選？" | 從讀寫比和 follower 分佈推：一般用戶 fan-out on write（發文時寫進 follower 的 feed cache，讀超快）、讀很少的殭屍用戶寫了浪費、celebrity 千萬 follower 寫不動、結論先講 hybrid 再講純策略的適用邊界 | 二選一站隊；講不出「為什麼要 hybrid」的推導過程 |
| "千萬 follower 的明星發文，fan-out on write 會發生什麼？" | 量化：1000 萬次寫入，每次 1KB 就是 10GB 寫入量、隊列堵塞影響普通用戶、延遲分鐘級（粉絲看到的時間嚴重不均）、解法：celebrity 的文不 fan-out，讀的時候 merge（follow 清單中的大 V 即時拉 + 自己的 precomputed feed 合併）、celebrity 判定線（如 >10 萬 follower）是個可調參數 | 沒算寫放大數量；hybrid 的 merge 過程講不清楚（讀時要查哪兩個來源） |
| "Feed 的儲存放哪？存全文還是存 ID？" | feed cache 存 post id list（Redis ZSET，score = timestamp/rank）不存全文、原因：全文重複儲存爆炸（一篇文 fan-out 給 1 萬人就是 1 萬份）、讀取時 id list → batch get post content（hydration）、feed 長度截斷（每人留最近 500-1000 則，更舊的 fallback 查 DB） | 在每個 follower 的 feed 裡存全文（儲存爆炸）；feed 無限長不截斷 |
| "用戶刪文或封鎖某人，已經 fan-out 出去的 feed 怎麼辦？" | 寫時修補太貴（要找出所有被投遞的 feed）、主流做法：讀時過濾（hydration 階段查 post 狀態，刪除的跳過；block list 在讀時過濾）、代價：讀路徑多一層檢查、feed 裡留下的「洞」靠多取一些 id 補齊 | 想要同步清理所有 feed（不可行）；完全沒想過刪文場景 |
| "排序從時間序改成 ML ranking，架構要改什麼？" | 候選生成和排序分離：feed cache 變成 candidate pool（取最近幾百則）、線上 ranking service 對候選打分（feature store + model serving、預算 P99 100ms 級）、降級路徑：ranking 掛了退回時間序、講出「ranking 是另一個系統」的邊界感，面試中點到為止 | 在 feed 系統裡硬塞 ML 細節失焦；或完全答不出架構上「哪裡插進去」 |

### Payment System

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "用戶點了付款，請求 timeout，client 重試，會重複扣款嗎？" | idempotency key 全鏈路：client 生成 key（同一筆訂單同一個 key）、server 用 key 查狀態：已成功回原結果、處理中回 409/等待、未見過才執行、key 和結果持久化（DB unique constraint，不能只放 Redis）、對 PSP 的呼叫也要帶冪等 key（Stripe 原生支援） | 冪等只做自己這層忘了對 PSP 那層；冪等記錄放 Redis（掉了就重複扣款） |
| "呼叫第三方 PSP timeout 了，這筆到底扣了沒？你怎麼辦？" | timeout 是未知狀態（不是失敗）、絕不能直接當失敗重試也不能當成功、處理：查詢 PSP 的 transaction status API 確認、查不到就用同一個冪等 key 重送（PSP 端去重）、最終靠 reconciliation 兜底、pending 狀態要設計進狀態機 | 把 timeout 當失敗直接重試（沒帶冪等 key 就是雙扣）；狀態機沒有 pending/unknown 態 |
| "為什麼要對帳（reconciliation）？你的系統不是已經 exactly-once 了嗎？" | 謙卑回答：分散式系統沒有絕對的 exactly-once，bug、時序、第三方差錯都會漏、對帳是獨立的正確性驗證（防禦縱深）：每日拉 PSP settlement file 對我方 ledger、差異分類：我有他無（掉單）、他有我無（漏記）、金額不符、差異進人工 queue、講 double-entry ledger 讓對帳可行（append-only、有跡可循） | 自信宣稱「我的設計不會錯所以不用對帳」（資深紅旗）；不知道對帳對的是「外部世界」 |
| "資料庫怎麼記錢？可以直接 UPDATE balance 嗎？" | 不行，要 double-entry ledger：append-only 交易分錄（debit + credit 成對、sum = 0）、balance 是 ledger 的衍生值（物化視圖，可重算可審計）、直接 UPDATE 的問題：無審計軌跡、並發 lost update、錯帳無法追溯、金額用整數最小單位（分）不用浮點 | 用 float 存錢（紅旗）；UPDATE balance 沒有 ledger（追問「錢對不上怎麼查」就垮） |
| "下單、扣庫存、扣款跨三個服務，怎麼保證一致？為什麼不用 2PC？" | 2PC 的問題：同步阻塞、coordinator SPOF、參與者鎖資源（吞吐殺手）、實務用 SAGA：每步本地交易 + 失敗時補償（refund、釋放庫存）、補償的設計重點：補償動作本身要冪等 + 可能失敗要重試、SAGA 的代價：中間狀態對外可見（要設計 pending UX）、orchestration vs choreography 點一下 | 答 2PC 沒講代價；SAGA 的補償流程說不出細節（refund 失敗怎麼辦） |
| "你的 payment 系統要監控什麼？怎麼第一時間知道出事？" | business metrics 優先：payment success rate（分 PSP、分卡種、分地區切片）、掉一個百分點就是大事故、P99 授權延遲、pending 卡單數量（狀態機卡住的單）、對帳差異數趨勢、第三方 PSP 的 error rate 分 code、alert 設在 success rate 驟降（比 infra metrics 更早發現問題） | 只講 CPU/latency 等 infra metrics；不知道 success rate by dimension 切片是支付監控的核心 |

---

## Tier 2 Problems（Day 54-59 新增 archetype）

### Ticket Booking / Flash Sale

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "1000 件庫存、10 萬人同時搶，你的第一道防線在哪？" | 分層漏斗：大部分流量根本不該碰到庫存層——前端排隊頁/驗證碼打散、gateway rate limit、排隊 token（拿到才能進下單流程），真正到扣減層的只剩千分之一；講出每一層漏斗的目的 | 直接從 DB 鎖講起，沒意識到最好的解法是讓流量根本到不了 DB |
| "Redis DECR 成功了、訂單還沒寫入，service crash——庫存少了但沒有訂單，怎麼辦？" | 預扣是租約不是所有權：預扣 + TTL reservation（付款超時自動歸還）、對帳 job 掃 dangling 預扣、冪等 key 讓 client 重試安全；狀態機要有 reserved 中間態 | 以為 DECR 原子 = 整條鏈安全；沒有歸還機制，庫存慢慢漏光 |
| "為什麼不直接 DB row lock？`SELECT FOR UPDATE` 不行嗎？" | 可以但吞吐有天花板：hot row 上千並發排隊、鎖等待堆積、連線池耗盡；單 row 鎖是千級 TPS，搶購瞬間是十萬級 QPS——所以把競爭前移到 Redis 原子操作或 queue 序列化，DB 只收序列化後的結果；低並發場景 row lock 反而是最簡單正解 | 不知道 hot-row 鎖的吞吐上限在哪；或全盤否定 DB 鎖（過度設計的反向錯誤） |
| "超賣和少賣，哪個可以接受？" | 這是 business 決策不是工程決策：超賣 = 賠償/公關災難（演唱會票不可超）、少賣 = 收入損失但可補救（歸還的庫存再放出）；多數場景寧可少賣，「預扣傾向少賣」是刻意設計的偏向 | 沒意識到這是可選的 trade-off；或兩個都說不能接受（工程上做不到絕對兩全） |
| "拍賣（auction）出價跟搶購有什麼不同？" | 同是 hot-row 併發寫但語義不同：auction 是 max(bid) 不是 decrement，可用樂觀鎖/CAS（版本號），輸了重讀重試；最後一秒 sniping 造成尖峰；「展示目前最高價」可以 stale（最終一致），「判定得標」不可以 | 照搬庫存扣減方案；分不清展示路徑和成交判定的一致性需求不同 |
| "這個系統你監控什麼？" | 漏斗每層通過率（突變 = 有人繞過）、庫存 invariant check（Redis 水位 + 已成訂單 + 預扣中 = 初始庫存，對不上 = 超賣或漏）、預扣歸還率、429 率、DB lock wait time | 只講 QPS/latency，沒有「庫存 invariant」這個 business 正確性監控 |

### Top-K / Real-Time Leaderboard

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "為什麼不每分鐘跑一次 `COUNT + ORDER BY`？" | 全表聚合 O(N)，高頻刷新 × 大表 = DB 被自己人打爆；先反問兩件事：要多即時、容忍多少誤差——答案直接決定架構複雜度差一個數量級 | 沒先問精確度需求就選方案；不知道「允許近似」是這題最大的設計槓桿 |
| "Redis ZSET 什麼時候夠用、什麼時候不夠？" | ZINCRBY + ZREVRANGE 精確且 O(log N)，key 空間放得進單節點記憶體（百萬級 key）就夠用；十億級 key（全站 URL、搜尋詞）記憶體爆炸，這時才需要 CMS 近似 | 一上來就 CMS（過度設計）；或不知道 ZSET 的記憶體天花板大概在哪個量級 |
| "Count-Min Sketch 為什麼只會高估、不會低估？" | hash 碰撞讓多個 key 累加到同一格，查詢取所有 hash 格的 min——min 仍可能含別人的計數（偏大）但絕不會少算自己的；跟 Bloom 同構（no false negative ↔ 永不低估）；高估的後果：長尾誤入榜，用 heap + 二次驗證緩解 | 講不出「為什麼取 min」；不知道單向誤差這個關鍵性質 |
| "要『最近一小時』的 Top-K，sliding window 怎麼做？" | CMS 不能減量（decrement 會破壞不低估性質）→ 時間分桶：每桶一個 sketch，查詢合併最近 N 桶，過期桶整桶丟棄；桶粒度 vs 記憶體的 trade-off | 想對 CMS 做 decrement（做不到）；或每次滑動全量重算 |
| "50 台機器各自統計，全局 Top-K 怎麼合併？" | CMS 同參數可逐格相加（線性可合併，map-reduce 友好）；各節點上送局部 top-N 候選集合併排序——但局部 top-10 的併集不保證涵蓋全局 top-10（某 key 在每台都排 11 名），候選數要放寬 | 以為各節點 top-10 合併取 top-10 就是對的（分佈式聚合的經典陷阱） |

### Ride Matching (Uber / Delivery)

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "百萬司機每 4 秒回報位置，這個寫入流怎麼扛？" | ~25 萬 writes/s；抓住資料特性：只要最新值（last-write-wins KV）、丟一筆無所謂（4 秒後又來）→ in-memory geo index + KV，不進 durable DB；歷史軌跡另走 async pipeline 進冷儲存 | 把位置更新寫進 PostgreSQL——把 ephemeral 資料當 durable 資料處理 |
| "兩張訂單同時派給同一個司機，怎麼辦？" | matching 的核心是司機狀態的互斥：dispatch 時原子標記 busy（CAS），搶到的才發 offer；offer 有 timeout，拒絕/超時就釋放重派——本質跟搶庫存同構（司機 = 庫存量 1） | 只做「查附近」沒做狀態互斥；沒有 offer timeout 導致司機被幽靈訂單鎖死 |
| "司機一直在移動，geo index 怎麼保持新鮮？" | geohash bucket：跨 cell 才更新 index（多數移動不跨 cell）、讀取容忍 4 秒 stale（業務無感）；兩階段：index 只出「候選集」，精確位置和排序查 KV | 每次位置更新都動 index；不區分候選篩選和精排兩個階段 |
| "最近的司機就是最好的選擇嗎？" | 直線距離 ≠ 到達時間（河對岸問題）→ ETA 要路網；貪心逐單派會讓整體等待惡化 → 批次配對（每 2 秒一批做二分圖匹配）；fairness（司機收入分佈）也是隱含目標 | 只答「找最近的」；不知道批次匹配這個優化層次存在 |
| "訂單狀態機哪些轉移最容易出 bug？" | 併發轉移：rider cancel 和 driver accept 同時到達（定義誰贏 + 輸方補償）、timeout 自動轉移和人為操作 race；解法：狀態轉移做成 CAS（帶 from-state 檢查），非法轉移拒絕 + 審計 log | 狀態機只畫 happy path；沒想過兩個「都合法」的事件同時發生 |
| "Tinder 跟 Uber 的 matching 差在哪？" | 同骨架（geo 候選 + 雙向確認）但參數全變：非即時（異步 like）、N×N 不是 1×1 搶佔、無互斥需求、多了偏好排序/推薦層——展示「同 pattern 改約束」的遷移能力 | 硬搬 dispatch 機制；講不出哪些約束變了所以哪些元件可以拿掉 |

## Phase 4 專題

### Brownfield / Legacy Migration

| 面試官追問 | 好答案要抓的重點（骨架） | 常見地雷 |
|-----------|------------------------|---------|
| "挑流量低谷停機切換不行嗎？" | 全球服務沒有共同半夜、資料量大到 copy 時間 > 可接受停機窗口；更本質：一次性切換 = 一次性風險，失敗連回滾都要再停一次機——漸進遷移是把一個大風險拆成 N 個可獨立回滾的小風險 | 只說「停機不好」講不出為什麼；沒抓到「風險拆分」這個核心論證 |
| "dual-write 期間兩邊怎麼保證一致？" | 誠實回答：不能強一致（跨兩系統沒有共同 transaction）；設計上：舊系統是 source of truth 直到 cutover、寫新系統失敗只記 log 不擋主流程、靠 verification job 持續比對修復；提 CDC/binlog 是 dual-write 的替代路線（少一份雙寫程式碼） | 宣稱 dual-write 兩邊一定一致（分散式基本功破綻）；不知道要指定誰是 truth |
| "backfill 歷史資料時線上還在寫，怎麼不漏不重？" | 順序關鍵：先開 dual-write 再 backfill（反過來中間的寫入會漏）；backfill 冪等（upsert）+ 用 version/updated_at 確保不覆蓋更新的資料；分批 + 限速保護線上 DB | 先 backfill 再 dual-write（經典漏資料順序錯誤）；backfill 全速跑把線上 DB 打掛 |
| "你怎麼證明新系統是對的、敢切？" | 三層證據：shadow traffic 比對 response diff（不影響用戶）、資料層 verification（row count / checksum / 抽樣全比對）、金絲雀漸進 1%→10%→100%——每階段事先定義回滾觸發條件（diff rate / error rate 閾值） | 「測試都過了就切」；金絲雀沒有預先定義的回滾條件（出事時現場吵要不要回滾） |
| "切到一半出事怎麼回滾？哪個階段最難回滾？" | 每階段回滾手段不同：proxy 切回（秒級）、停新寫（分鐘級）；最難是 cutover 之後——新系統已接受「只存在於新系統的寫入」，直接切回 = 資料遺失，所以 cutover 後要反向 dual-write（new→old）保留回滾窗口，直到信心足夠才 decommission | 以為回滾永遠只是「切回去」；不知道 cutover 後有資料回填問題 |

---

## 使用建議（給 skill / 自學）

| 模式 | 做法 |
|------|------|
| **Step F 抽題** | 從當日主題的表格隨機抽 2-3 條，學生口頭作答後對照骨架給回饋 |
| **自我檢測** | 遮住右兩欄，計時 90 秒口頭回答，錄音回聽，對照骨架找漏洞 |
| **弱點複習** | 答不出的追問記入 `progress.md` Mistake Registry，進 Leitner Box 1 |
| **Mock 前衝刺** | 只看「常見地雷」欄，確認自己不會踩同樣的坑 |
