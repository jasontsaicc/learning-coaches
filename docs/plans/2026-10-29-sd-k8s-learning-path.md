# SD / k8s：Node → Chunk → HTML 學習路徑

日期：2026-10-29。狀態：課程與導航藍圖；尚未接入網站，也不改寫 coach 的執行課表或學員進度。

## 1. 層級與順序

- Phase 是分區；node 是一個可說清楚的大問題；chunk 是一個能驗收的學習目標。
- 畫面呈現兩層：node 展開 chunks。Phase 不再多包一層收合。
- 點箭頭展開，點 node 標題進主題 HTML，點 chunk 進專題 HTML 或已核對的章節錨點。展開按鈕與連結分開，支援鍵盤與 `aria-expanded`。
- Node 優先連 hub；沒有 hub 時連既有主題 layers 頁並標「主題筆記」。只有 phase 總覽不能假裝已有 node 教材。
- Chunk 不等於一次 sitting，也不等於 HTML 的 L0–L7。L0–L7 是同一主題的深度層，chunk 是不同學習目標。
- 同一 HTML 可供多個 chunk 使用，先連整篇並標「共用筆記」；只有內容與錨點均核對後才深連。缺教材顯示「待補 HTML」，不產生空連結。
- 表格由上而下是導航順序；同列的 ①②③ 是 chunk 順序。Day / C 編號保留作教材來源，不拿來自動排序。
- 課程清單完整可見；「繼續學習」由既有進度決定。已學內容重新分組後不重上、不自動清帳。

## 2. 依據與教材標記

課程範圍取自 [SD curriculum](../../skills/sd-coach/references/curriculum.md)、[SD detail](../../skills/sd-coach/references/curriculum-detail.md)、[k8s curriculum](../../skills/k8s-coach/references/curriculum.md) 及各 phase reference。
個人隊列以 [SD plan 的 2026-10-29 方案 B](../../workspaces/sd/curriculum-plan.md)、[k8s plan §12.2–12.6](../../workspaces/k8s/curriculum-plan.md) 為依據。
SD 尚未完成的八章沿用 [既有 roadmap](../../portfolio/sd/notes/p3-roadmap.html)，避免退回舊的 Day 排序。

教材盤點核對了 HTML 標題、章節及檔案存在性，未逐句驗證技術內容：

| 標記 | 意義 |
|---|---|
| 專題 | 已有對應主題 HTML；不代表已完成所有 chunk 或驗收 |
| 部分 | 只有共用／預習／phase 概覽，或單一 chunk 的教材 |
| 待補 | 沒有對應專題 HTML；原始課綱或 Markdown 仍可供備課 |

下列每列教材屬於整個 node 的盤點；未明確指定 chunk 的連結均為共用閱讀入口，不表示每個 chunk 已有獨立頁。實作時不能把一個 node 的教材狀態直接複製給所有 chunks。

## 3. SD 完整路徑

### P0：先學會把問題講清楚

分區入口：[思考框架](../../portfolio/sd/notes/p0-chapter-thinking-framework.html)。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 面試如何評估設計 / D1 | ①辨認需求與評分維度 ②比較好壞回答，指出缺少的論證 | 專題：[Interview rubric](../../portfolio/sd/notes/day01-interview-rubric-layers.html) |
| 容量估算 / D2 | ①從 workload 算 QPS ②算儲存與頻寬 ③用估算找第一個瓶頸 | 專題：[Estimation](../../portfolio/sd/notes/day02-estimation-layers.html) |
| 組織設計答案 / D3 | ①澄清需求 ②畫最小資料流 ③沿瓶頸深入與量化取捨 | 專題：[Framework](../../portfolio/sd/notes/day03-framework-layers.html) |

收尾：P0 gate，練完整回答，不因讀完三頁自動通過。

### P1：核心元件

分區入口：[Building blocks](../../portfolio/sd/notes/p1-chapter-building-blocks.html)。維持原有前置順序；每個 node 的收尾都帶一個 SLI、SLO、告警與 dashboard 判斷。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 流量入口與負載平衡 / D4–5 | ①DNS 與入口 ②L4/L7、分流策略 ③health check、sticky session、draining ④ALB/NLB 與故障判讀 | 專題：[Load balancer](../../portfolio/sd/notes/day04-load-balancer-layers.html) |
| Cache 與 CDN / D6–7 | ①Cache-Aside 與寫入策略 ②TTL、eviction、失效 ③CDN 與邊緣快取 ④用命中率和延遲驗證取捨 | 專題：[Caching](../../portfolio/sd/notes/day06-07-caching.html) |
| 資料庫選型 / D8–9 | ①access pattern 與資料模型 ②SQL/NoSQL、B-tree/LSM ③WAL、replica、partition key ④連線池與熱分區 | 專題：[Database](../../portfolio/sd/notes/day08-database-selection-layers.html) |
| 非同步處理 / D10–11 | ①解耦、緩衝與背壓 ②delivery semantics、冪等 ③retry、DLQ ④SQS/Kafka/RabbitMQ 選型 | 專題：[Message queue](../../portfolio/sd/notes/day10-message-queue-layers.html) |
| API 契約 / D12–13 | ①REST/gRPC/GraphQL ②分頁與版本 ③冪等與錯誤契約 ④從使用者流量驗證設計 | 專題：[API design](../../portfolio/sd/notes/day12-api-design-layers.html) |
| 身分與權限 / D14 | ①authentication vs authorization ②session/JWT/OAuth ③撤銷與生命週期 ④威脅與防護取捨 | 專題：[Security & auth](../../portfolio/sd/notes/day14-security-auth-layers.html) |
| 分片與資料分布 / D15–16 | ①單機瓶頸與 partition ②consistent hashing ③vnodes 與熱點 ④擴縮容的資料搬動 | 專題：[Consistent hashing](../../portfolio/sd/notes/day15-consistent-hashing.html) |

收尾：[P1 cache gate](../../portfolio/sd/notes/phase1-gate-distributed-cache-layers.html)。PoC 是否執行沿用個人課表，不因導航重整恢復已停用的 PoC。

### P2：以 Distributed Cache 帶出分散式核心

分區入口：[Distributed core](../../portfolio/sd/notes/p2-chapter-distributed-core.html)。下列是可展開的觀念 node；教學從 cache 情境按需拉入，不重新強制逐 Day 上課。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 分區時如何取捨 / D17–18 | ①網路分區情境 ②availability/consistency 選擇 ③回到 cache 的讀寫決策 | 專題：[CAP](../../portfolio/sd/notes/day17-cap-layers.html) |
| 一致性承諾 / D19–20 | ①使用者需要什麼保證 ②strong/eventual/causal ③read-your-writes 與代價 | 專題：[Consistency](../../portfolio/sd/notes/day19-consistency-models-layers.html) |
| 複寫與故障切換 / D21–22 | ①leader/follower ②同步與非同步複寫 ③選主、quorum 與故障窗口 | 專題：[Replication](../../portfolio/sd/notes/day21-replication-layers.html) |
| 過載與故障隔離 / D23–24 | ①限流演算法 ②timeout/retry 放大 ③circuit breaker 與恢復 | 專題：[Rate limiting](../../portfolio/sd/notes/day23-rate-limiting-circuit-breaker-layers.html) |
| 可觀測的設計 / D25 | ①SLI/SLO ②metrics/logs/traces 的證據 ③告警與 3AM 排障 | 專題：[Observability](../../portfolio/sd/notes/day25-observability-layers.html) |
| 大規模摘要與成員資訊 / D26 | ①Bloom filter 與誤判 ②gossip 傳播 ③何時值得用近似或最終收斂 | 專題：[Bloom & gossip](../../portfolio/sd/notes/day26-bloom-gossip-layers.html) |

收尾：[Session store gate](../../portfolio/sd/notes/phase2-gate-session-store-layers.html)。Kill Pack 維持遇到故障時的補充 reference，不變成必修新支線。

### P3：設計題與目前隊列

分區入口：[Classic problems](../../portfolio/sd/notes/p3-chapter-classic-problems.html)。前五題保留作已練習內容的瀏覽區，完成與掌握狀態仍由 progress 判定。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| URL Shortener / D27–28 | ①需求與容量 ②key 產生與資料模型 ③redirect/cache ④故障與設計驗收 | 專題：[URL Shortener](../../portfolio/sd/notes/day27-url-shortener.html) |
| Unique ID / D29–30 | ①唯一、有序、吞吐的需求 ②UUID/Snowflake ③時鐘回撥與 worker ID ④取捨驗收 | 專題：[Snowflake](../../portfolio/sd/notes/day29-snowflake-id-layers.html) |
| Distributed Rate Limiter / D31–32 | ①單機到分散式 ②Redis 原子更新 ③故障時 fail-open/closed ④容量與驗收 | 專題：[Rate limiter](../../portfolio/sd/notes/day31-distributed-rate-limiter-layers.html) |
| Notification / D33–34 | ①多通道資料流 ②優先級與使用者偏好 ③重試、去重與送達 ④整體設計驗收 | 專題：[Notification](../../portfolio/sd/notes/day33-notification-system-layers.html) |
| Chat / D35–37 | ①連線、持久化、ordering ②離線補送與推播 ③群組 fan-out ④presence/read receipt ⑤完整 mock | Node：[Hub](../../portfolio/sd/notes/day35-chat-system-hub.html)；①[Layers](../../portfolio/sd/notes/day35-chat-system-layers.html)、②[Offline](../../portfolio/sd/notes/day35-chat-offline-push-slo.html)、③[Fan-out](../../portfolio/sd/notes/day36-group-fanout.html)、④[Presence](../../portfolio/sd/notes/day36-presence-heartbeat.html)（read receipt 共用 hub）、⑤[Mock](../../portfolio/sd/notes/day35-chat-system-mock-l6.html) |

接下來的八個 node 順序固定沿用 2026-10-29 方案 B。Brownfield 的來源是 P4 D62–63，但執行位置在此，不再於 P4 重複排課。

| 順序 / Node | Chunks（依序） | HTML 對應與缺口 |
|---|---|---|
| 1. Metrics & Logging / D46–47 | ①agent→collector→buffer ②TSDB 與 cardinality ③aggregation/downsampling/retention ④mock 與收帳 | 部分：[預習頁](../../portfolio/sd/notes/day46-metrics-logging-layers.html)；①–③共用，④待補；完整 hub 待課程收尾 |
| 2. Top-K / D56–57 | ①ZSET vs CMS + heap ②time window 與 sketch 合併 ③mock 與收帳 | 待補：node 與全部 chunks |
| 3. Brownfield / D62–63 | ①Strangler Fig ②dual-write/backfill ③shadow traffic ④cutover/rollback/雙重監控 ⑤mock 與收帳 | 部分：[預習頁](../../portfolio/sd/notes/day62-brownfield-migration-layers.html)；①–④共用，⑤待補；hub 待收尾 |
| 4. Deploy System / 組裝 mock | ①rollout、health、自動 rollback、fleet capacity mock ②debrief 與收帳 | 待補：mock 與回饋 HTML；不新增一輪元件教學 |
| 5. Distributed Cache / D38–39 | ①分片與 invalidation at scale ②thundering herd、locking、coalescing ③mock 與收帳 | 部分：[既有 cache gate](../../portfolio/sd/notes/phase1-gate-distributed-cache-layers.html) + [hashing](../../portfolio/sd/notes/day15-consistent-hashing.html) 可複習；本輪完整 hub/mock 待補 |
| 6. Payment / D43–45 | ①authorization→capture→settlement ②idempotency key ③SAGA ④ledger/reconciliation ⑤mock 與收帳 | 待補：node 與全部 chunks |
| 7. Ticket / D54–55 | ①TOCTOU 與超賣 ②row lock/DECR/queue ③預扣、TTL、對帳 ④overload 與入口排隊 ⑤mock 與收帳 | 待補；前置 Payment ②，不可為了 Day 排序移到 Payment 前 |
| 8. News Feed / D40–42 | ①fan-out on write/read ②大帳號 hybrid、ranking、cache warming ③mock 與收帳 | 待補；Chat fan-out 只作前置連結，不冒充本題教材 |

八章沿用約 30 堂估算，不由 chunk 數重新推算日期。P3 gate 是否考仍依現有個人計畫，到隊列結束再決定。

### P4：輸出、遷移能力驗證與陌生題

分區入口：[Advanced & mocks](../../portfolio/sd/notes/p4-chapter-advanced-mocks.html)。以下只有 phase 共用總覽，尚無各 node 專題 HTML。

| Node / 原單元 | Chunks（依序） | 教材狀態 |
|---|---|---|
| Trade-off / D60–61 | ①量化成本與容量 ②陷阱與需求改變 ③解釋何時換方案 | 部分：phase 總覽；專題待補 |
| Mock round 1 / D64–65 | ①無提示完整設計 ②feedback ③重做薄弱段 | 部分：phase 總覽；題目與回饋頁待補 |
| Weak spots / D66–67 | ①辨認反覆錯誤 ②挑 2–3 題重做 ③用新情境驗證修正 | 部分：phase 總覽；個人紀錄不直接公開 |
| Final mock / D68–69 | ①需求變更 ②連續 pivot ③gate 與下一輪重點 | 部分：phase 總覽；專題待補 |

陌生題池單獨收合，標「mock 抽題／非必修隊列」，不擋主線完成：

| Node | Chunks（題目拆解，不預先強制上課） | HTML |
|---|---|---|
| Autocomplete / D48–49 | ①prefix index ②ranking ③更新與延遲取捨 | 待補 |
| Crawler / D50–51 | ①frontier ②去重與 politeness ③擴展與失敗恢復 | 待補 |
| Proximity / D52–53 | ①geo index ②鄰近查詢 ③精度與更新成本 | 待補 |
| Ride Matching / D58–59 | ①位置 ingest ②dispatch ③trip state machine；前置 Proximity | 待補 |
| Tier 3 按需題 | Cloud Storage：分塊→同步→衝突；Video/Instagram：上傳→轉碼→CDN；Task Scheduler：DAG→retry→冪等；A/B：分流→flag→量測；Twitter：Feed→熱點→規模化 | 待補；各題獨立抽用，不串成新必修課 |

## 4. k8s 完整路徑

P0 → P1 → P2a → P2b → P3 → P4 → Terraform 接力 → P5 → Migration → P6。
Controller/GPU 是 P5 後 FLEX 支線；CKA 是副線。保留所有既有 phase gates、P2a/P3 mini-mock，不以新 node 取代驗收。

### P0：從宣告到執行

分區入口：[Mental model](../../portfolio/k8s/notes/p0-chapter-mental-model.html)。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 宣告與協調 / C0–1 | ①desired/actual state ②reconcile loop ③宣告與執行者的責任界線 | 專題：[Reconcile](../../portfolio/k8s/notes/p0-reconcile-loop.html)、[宣告與執行](../../portfolio/k8s/notes/s25-declaration-vs-executor.html) |
| apply 到 Running / C2–3 | ①control plane 分工 ②API 請求鏈 ③scheduler→kubelet→runtime ④找出卡住的一棒 | 專題：[API server](../../portfolio/k8s/notes/p0-apiserver-request-chain.html)、[完整流程](../../portfolio/k8s/notes/s10-apply-to-running.html) |
| 狀態與共識 / C4 | ①etcd 儲存什麼 ②Raft/quorum 入門 ③失去多數時的行為 | 專題：[etcd/Raft](../../portfolio/k8s/notes/p0-etcd-raft.html)；備份還原留 P5 |

P0 C5 容器底層入門連到下列 P1 第一個 node，共用教材，保留原先入門時的教學位置。

### P1：讓 workload 正確運作

分區入口：[Core objects](../../portfolio/k8s/notes/p1-chapter-core-objects.html)。

| Node | Chunks（依序） | HTML 對應 |
|---|---|---|
| 容器與 Pod | ①process/namespace/cgroup ②Pod 共享邊界 ③PID 1、signal 與退出 | 專題：[容器](../../portfolio/k8s/notes/s6-container-namespace-cgroup.html)、[PID 1](../../portfolio/k8s/notes/s26-pid1-signal.html)；Pod 邊界共用 phase 總覽 |
| 健康與發布 | ①startup/readiness/liveness ②Deployment/ReplicaSet ③rollout/rollback ④失敗發布排障 | 專題：[Probe](../../portfolio/k8s/notes/s6-probe.html)、[Rollout](../../portfolio/k8s/notes/s6-deployment-rollout.html) |
| 資源與生命週期 | ①requests/limits ②QoS/OOM ③StatefulSet vs Deployment ④Job 批次任務 | 部分：[QoS/OOM](../../portfolio/k8s/notes/s10-resource-qos-oom.html)；③連 P2b StatefulSet，④待補 |

### P2a：追一個封包

分區入口：[Networking](../../portfolio/k8s/notes/p2a-chapter-networking.html)。沿用教材 C1→C2→C3→C4，CNI 的必要概念在 NetworkPolicy 即時補入，完整封包鏈於最後整合。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 服務發現 / C1 | ①Service 與 endpoints ②kube-proxy 資料路徑 ③CoreDNS ④DNS 分層排障 | 部分：②有[專題](../../portfolio/k8s/notes/p2a-kube-proxy.html)；其餘只有 phase 共用總覽，專題待補 |
| 外部流量入口 / C2 | ①Ingress 與 controller ②host/path/TLS ③404/502/503 ④Gateway API 對照 | 部分：phase 總覽；既有 Ingress/Gateway Markdown，專題 HTML 待補 |
| 網路隔離 / C3 | ①selector 與 allow 規則 ②default deny、DNS egress ③CNI 執行與 Calico lab | 部分：[宣告與執行](../../portfolio/k8s/notes/s25-declaration-vs-executor.html) 輔助；policy 專題與 lab HTML 待補 |
| 封包全鏈路 / C4–5 | ①netns/veth/bridge ②跨 node 路由與封裝 ③Service NAT/回程 ④EKS VPC CNI 對照（選配） | 部分：phase 總覽與既有 Markdown；專題待補 |

### P2b：資料與權限

分區入口：[Storage & permissions](../../portfolio/k8s/notes/p2b-chapter-storage-permissions.html)。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 持久化資料 / C1–3 | ①Volume/PV/PVC ②StorageClass/CSI ③StatefulSet identity/storage ④AZ、重建與資料保留 | 部分：③④有[StatefulSet](../../portfolio/k8s/notes/s32-statefulset-keeps.html)；①②共用 phase 總覽，專題待補 |
| API 與雲端權限 / C4–5 | ①SA/RBAC/binding ②verb/subresource 排障 ③IRSA 身分鏈 ④區分 Linux、k8s、AWS 權限 | 部分：①[RBAC 三條線](../../workspaces/k8s/notes/rbac-three-lines.html)、②[Verb traps](../../portfolio/k8s/notes/s33-rbac-verb-traps.html)、④[三道門](../../portfolio/k8s/notes/p2b-permission-three-doors.html)；③專題待補 |
| 機密與 Pod 安全 / C6 | ①Secrets 的保護邊界 ②securityContext ③PSS/PSA ④拒絕事件與分階段導入 | 部分：[PSS layers](../../portfolio/k8s/notes/s40-pss-layers.html)、[Gate notes](../../portfolio/k8s/notes/s40-pss-gate-notes.html)；Secrets 專題待補 |

### P3：調度、伸縮與韌性

分區入口：[Scheduling & resilience](../../portfolio/k8s/notes/p3-chapter-scheduling-resilience.html)。kubeadm 建置與 NetworkPolicy 補課是已有執行順序的前導節點，不要求學員重新操作。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 實驗叢集 / 前導 | ①Terraform EC2 ②Ansible/kubeadm ③Calico 與 NetworkPolicy 補課 ④收工與資源檢查 | 部分：有 bootstrap/networkpolicy Markdown；HTML 待補 |
| 調度與放置 / C1–2 | ①filter/score 與 Pending ②affinity/taints ③topology spread ④DRA 裝置分配概念 | 部分：phase 總覽與 scheduler/DRA Markdown；專題 HTML 待補 |
| 自動伸縮 / C3→C4→C3b→C5 | ①HPA 公式、requests、窗口 ②VPA 與 HPA 共存 ③KEDA 事件與縮到零 ④CA/Karpenter 節點供給 | ①[HPA](../../portfolio/k8s/notes/s51-hpa-layers.html)、②[VPA](../../portfolio/k8s/notes/s52-vpa-layers.html)、③[KEDA](../../portfolio/k8s/notes/s53-keda-layers.html)（現有頁到機制段，後續內容待補）；④只有 phase 總覽；node hub 待補 |
| 維護與可用性 / C6 | ①PDB 與 eviction ②drain ③graceful shutdown 與流量排空 ④驗證中斷範圍 | 部分：phase 總覽 + [PID 1](../../portfolio/k8s/notes/s26-pid1-signal.html)；專題/lab HTML 待補 |
| 容量與整體排障 / C7 + drills | ①headroom 與容量規劃 ②kubelet/containerd/node 壓力 ③七站流量排障 ④incident commander 與 mini-mock | 部分：phase 總覽；專題/runbook HTML 待補 |

沿用 §12.4：主要動手保留 scheduler/HPA/PDB；其他內容採圖與情境。KEDA 依後續插課決策保留 lab，不為新 chunk 清單額外增加每堂 G。

### P4：可觀測性工程

分區入口：[Observability](../../portfolio/k8s/notes/p4-chapter-observability.html)。先建 Python API + Postgres 作為被監控、之後被遷移的服務。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 建立觀測資料 / 前導、C1–2 | ①API + DB 觀測對象 ②metrics/logs/traces ③Prometheus discovery/scrape ④exporter、node-exporter | 部分：phase 總覽；專題待補 |
| 從數據到可靠性 / C3–4 | ①counter/rate/reset ②histogram/quantile/cardinality ③SLI/SLO ④error budget | 部分：phase 總覽；專題待補 |
| 追蹤與告警 / C5–6 | ①OTel context/span ②端到端 trace ③symptom-based alert ④burn rate 與告警演練 | 部分：phase 總覽；專題待補 |

DCGM exporter 保留概念對照，GPU 動手仍放 FLEX；不在 P4 提前開 GPU lab。

### Terraform 接力與 P5：平台工程

Terraform senior 六場接在 P4 後，連到既有 Terraform coach；capstone 為 EKS + RDS，保留 CDK 對照。此頁只顯示跨課程入口，不複製一套 Terraform 課程與進度。
P5 分區入口：[Platform / GitOps](../../portfolio/k8s/notes/p5-chapter-platform-gitops.html)。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 宣告式交付 / C1–2 | ①Helm template/release ②ArgoCD reconcile ③drift/sync/回復 ④Git→上線閉環 | 部分：phase 總覽；專題待補 |
| 擴充與攔截 / C3–4 | ①CRD/schema ②Operator reconcile ③admission webhook ④失效策略與故障演練 | 部分：phase 總覽；專題待補 |
| 叢集生命週期 / C5–6 | ①升級相容性與順序 ②kubeadm minor upgrade/憑證 ③etcd snapshot/restore/DR ④EKS 升級對照 | 部分：phase 總覽 + [etcd 原理](../../portfolio/k8s/notes/p0-etcd-raft.html)；操作專題待補 |
| EKS 與安全發布 / C7–8 | ①EKS production IaC ②平台權限與網路整合 ③canary/blue-green ④指標判定與 rollback | 部分：phase 總覽；專題待補，重用 Terraform 成果 |

### P5 後：Migration 與選修

| Node / 範圍 | Chunks（依序） | HTML 對應 |
|---|---|---|
| Migration / 必修 | ①既有服務盤點與容器化 ②kubeadm→EKS + RDS ③資料遷移與驗證 ④cutover/rollback ⑤migration runbook | 待補實作 HTML；[SD Brownfield](../../portfolio/sd/notes/day62-brownfield-migration-layers.html) 是設計參考，不能代替實驗證據 |
| 自寫 Controller / FLEX | ①watch/reconcile ②status/finalizer ③失敗重試與驗證 | 待補；P5 Operator 概念之後才排 |
| GPU / FLEX | ①driver/toolkit/device plugin ②GPU Operator/MIG ③升級順序與短期 lab | 待補；不擋 P6 主線 |
| CKA / 副線 | ①kubeadm 操作 ②etcd/故障題 ③限時整合練習 | 待補；P5 後依需求決定，不預設報考 |

### P6：面試整合

分區入口：[Interview sprint](../../portfolio/k8s/notes/p6-chapter-interview-sprint.html)。

| Node / 原單元 | Chunks（依序） | HTML 對應 |
|---|---|---|
| 個人衝刺 / C1 | ①弱點盤點 ②安排 mock 配比 ③檢查覆蓋與重測 | 部分：phase 總覽；個人評量維持原資料來源 |
| Incident / C2 | ①故障假設與證據 ②止血/恢復 ③溝通與復盤 | 部分：phase 總覽；情境專題待補 |
| k8s × SD / C3 | ①multi-tenancy ②multi-cluster/DR ③cost/capacity ④upgrade-at-scale | 部分：phase 總覽；情境專題待補 |
| Behavioral / C4 | ①挑證據 ②STAR ③追問與取捨 | 部分：只提供教學總覽；私人故事庫不匯出到網站 |

C5 CKA 已列副線；C6 English polish 保留課綱入口但標「暫緩」，沿用目前個人計畫的英文暫不處理決策，不自行恢復英文加壓。

## 5. 實作範圍與驗收契約

這份藍圖先交付課程規劃；網站接線時需要一起處理下列位置：

| 位置 | 最小必要改動 |
|---|---|
| `site/` 課程資料 | 新增一份明確 node/chunk 清單，含穩定 ID、順序、原 Day/C/topic 對照與 HTML 目標；不再用標點切割推導這兩科的完整路徑 |
| `site/build.py` | 讀清單，驗證 ID/parent、檔案 allowlist、HTML fragment；保留現有 topic/phase IDs 與舊閱讀連結 |
| `site/app.js`、`styles.css` | Phase 分區、node 展開、標題連結、chunk 列表；目前 node 預設展開；桌面與手機使用同一套層級 |
| `site/exercises/*.json` / exercises | 舊 chapter/question IDs 不變；topicRefs 若需新對照，顯式映射，不重建練習紀錄 |
| `site/map.js`、搜尋與最近閱讀 | 檢查既有 topic 導航仍可用；搜尋可找到 node/chunk 並到相同教材；不另做第二套課綱 |
| `site/test_build.py`、Node / browser checks | 驗證階層、指定順序、缺教材、共用教材、舊 ID 相容、展開與鍵盤操作、直接開 HTML |
| `site/README.md` | 更新來源與導航契約，移除已失效的自動拆詞說明 |

資料只需滿足當前兩科，不新增通用課程引擎、帳號或跨裝置同步。課綱資料只放標籤、來源與連結；學習狀態仍取 progress，教材內容仍住 HTML，避免三份互相矛盾的進度。

驗收要求：

1. SD 八章順序與 10-29 計畫一致；Payment 在 Ticket 前，Brownfield 只排一次。
2. k8s 保留 VPA→KEDA→CA/Karpenter、P4→Terraform→P5→Migration→P6；選修不阻擋主線。
3. 箭頭只展開，標題只閱讀；鍵盤可分別操作；手機不依賴 hover。
4. 缺 HTML 明確標示；phase 總覽不被當成專題齊備；KEDA 部分教材不標完整。
5. 有筆記、已練習、正式 mastery 分開；不以閱讀或折疊狀態推算完成率。
6. 舊筆記、題庫 ID、最近閱讀、練習紀錄可繼續使用；不寫入 `workspaces/`。
7. 原 curriculum/gates 與個人計畫持續有效；這份文件只規劃導航與教材切分，不改評分規則。

補教材優先序：先補目前 SD Metrics、k8s KEDA/節點擴容的目標與缺口，再補下一個 node；其餘待學主題先顯示清單，依實際上課產出 notes。不要一次預造整套空白 HTML。
