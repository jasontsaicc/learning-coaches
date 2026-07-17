# 課程總體規劃 v2(2026-07-09,Fable 制定)

<!-- 給後續教練模型(Opus 4.8+)的使用說明:
     本檔是「戰略層」規劃,advisory,不是鐵軌。
     runtime 真相永遠在 progress.md / mistake-registry.md,衝突時現場贏、回寫本檔。
     [FLEX] 標記 = 刻意留白的決策點,由當時的教練依現場狀態拍板。
     重規劃觸發器見 §7,符合任一條就更新本檔,不必整份推翻。 -->

## §1 北極星與現況

- 北極星不變:通過大廠 senior DevOps/SRE 面試 + 拿到外商 package。仲裁規則不變:面試 ROI 與變強深度衝突時,面試贏。
- 面試窗口:2027 農曆新年前後開始投遞(2026-07-09 學員定),跑道約 30 週,策略是紮實加深不是趕進度,詳 §5。
- 現況(s14, 2026-07-09):P2a chunk 2 Ingress 全畢業,下一步 chunk 3 NetworkPolicy(要開 Calico 叢集)。
- 節奏實測:14 堂 / 23 天,約每週 4-5 堂,Gap Mode 重度使用,單堂常被切段。所有估算以此節奏為底。

## §2 學員畫像 v2(14 堂實證,取代開課診斷)

### 可以依賴的強項
1. 排障方向感:P1 gate 三隻混合故障全定位;s13 照 404 階梯逐層查、s14 排障第一刀方向都對。
2. 第一性推導力:被縮小成思想實驗後幾乎都能自己推回(中央 LB 瓶頸、OOM 不可壓縮、NodePort 到 Ingress 整條階梯自己爬)。這是「出手門檻 2-strike」的依據,先讓他持球。
3. 預測準:lab 預測命中率極高(probe 兩次全中、endpoints 內容、Ingress 三題全中、/api/v2 押注押中)。
4. 誠實自標盲點:會主動說「壓縮是啥意思不懂」,自我校準可信。

### 弱點 pattern(重規劃的靶心,皆有日期證據)
- W1 隱性會、顯性不會:結果預測準,why 講不出(s14 定型的 pattern;F 段第一輪獨白偏薄是常態)。
- W2 「規則 / 狀態 / 資料」三分不清的混淆家族:iptables vs Endpoints(06-27 手vs名單)、iptables vs conntrack(07-06 規則vs狀態)、etcd 角色三次滑掉。同一個根,單顆治標,要家族級對治。
- W3 精度衰減:講對過的東西回測時滑掉(kube-proxy「只寫規則」s8 對、s13 退;conntrack 精度 07-06 掉)。
- W4 盲講漏中間棒次(WR#1 漏 scheduler,正是 P0 原始洞)。
- W5 英文與內容難度不能同時上升(錯峰規則已立);英文可交付但短,詞彙 recall 弱(thundering herd)。
- W6 沒把握就被牽著走(memory [[led-along-despite-doubt]]),誘答要持續埋。
- W7 純口頭修復保鮮期約 2 天(+2 天格已立)。
- W8 輸出段(F/G)是瓶頸且曾被收工砍(收工儀式已立)。

## §3 對治機制

既有機制全部保留(誘答、+2 天格、錯峰、收工儀式、2-strike 出手門檻)。新增四個,前三個都是秒級到 30 秒級的動作,不吃課時:

- **M1 Why-first(對治 W1)**:D 段每個實驗,按 Enter 前先講兩句:預測結果 + 一口氣講機制 why。結果只拿來驗證預講。預講不出來 = 當場入 registry,不等 F 段才發現。這把「隱性會」在最便宜的時點逼成顯性。
- **M2 三分類牌(對治 W2)**:固定 30 秒 drill,丟一個名詞問「規則(宣告)/狀態(runtime 記憶)/資料(被查的名單)?」。題池:iptables 規則=規則、conntrack=狀態、Endpoints=資料、Ingress 物件=規則、nginx.conf=規則(render 產物)、etcd 內容=資料(desired)。進 A 段輪抽;mistake-registry 同家族的坑合併成一張 pattern 卡追蹤,家族三連過才算封印。
- **M3 一句話精準版(對治 W3)**:A 段抽考過關不只看「對」,要收一句精準版收尾(例:kube-proxy 只寫規則、kernel 搬封包)。說不出精準版 = 半過,拉近期。
- **M4 Story mining(對治 behavioral 短板)**:story-bank 目前近乎空,但學員在 billing EKS 平台有真實 prod 經歷。每次 Weekly Review 固定挖 10 分鐘一則(incident、on-call、架構決策),raw 一行入帳就好,P6 才提煉 STAR。機會式入帳照舊,這條是保底頻率。

## §4 課程主幹修訂

### 4.1 Capstone 主線:shop platform(本次最大的結構改動;學員 2026-07-09 拍板採用)

s12-s14 的 shop-api / shop-web 不再是丟棄式 lab,升級為貫穿到 P6 的持續演進平台。每個 phase 在同一個平台上長一層,終點是一個 recruiter 可看的 production-like 平台,外加一條完整敘事:「我從零長出一個平台,每一層都能講到 kernel」。這同時解決 portfolio 連貫性與 behavioral 素材。

| Phase | shop platform 長出什麼 | portfolio 落點 |
|-------|----------------------|----------------|
| P2a 剩餘 | NetworkPolicy 隔離 api/web、Calico 叢集、封包全鏈路圖 | manifests/ |
| P2b | api 掛 PVC(訂單資料)、最小權限 RBAC、EKS 首登:IRSA 讓 api 讀 S3 | manifests/ + terraform-eks/ |
| P3 | load generator、HPA、PDB、node 壓力大演練、capacity runbook | manifests/ + notes/(runbook 英文) |
| P4 | Prometheus + SLO(api 可用性/延遲)、OTel 打通一條 trace | observability/(主秀) |
| P5 | Helm 化、ArgoCD 部署整個平台、EKS prod-grade terraform | gitops/ + terraform-eks/(主秀) |
| Migration(P5 後,§4.6) | 加一個 legacy 服務,完整導入演練 + cutover | notes/(英文 migration runbook) |
| P6 | 平台本身變成 mock 與 behavioral 的素材 | story-bank 提煉 |

[FLEX] 平台細節(掛什麼儲存、SLO 定幾個 9)由當時教練依現場定;唯一硬要求是「同一個平台一路長」,不重開爐灶。

### 4.2 Phase 順序:維持 P2a → P2b → P3 → P4 → P5 → P6

考慮過把 P3 提前(HPA 有趣、接得住動能),但 P2b 的 IRSA/RBAC 是 AWS 系大廠高頻靶,學員 AWS 背景是差異化武器,且 EKS 越晚進場 story 越薄,維持原序。[FLEX] 若 P2b 中段動能明顯掉,可插 P3 chunk 1(scheduler)換口味,P2b 剩餘延後,由當時教練拍板。

### 4.3 EKS 策略(成本與安全)

- kind 為主。EKS 只做 kind 做不到的:IRSA(P2b)、ALB controller / Karpenter(P3)、prod-grade IaC(P5)。
- 每次 EKS lab 必附 destroy + 驗證指令;命名 `billing-dev-eks-*`;terraform 由學員親手跑。
- 安全鐵律不變:context `kind` / `kind-k8s-coach-p0` 安全,`eks` = 公司 PROD,動手前必查 current-context。

### 4.4 Mock 節奏升級(面試 ROI 前置,不等 P6)

- P2a 收尾:30min 迷你 mock(既定,別漏)。
- P3 收尾:30min 迷你 mock(既定)。
- 新增:P4 起每次 Weekly Review 掛一題「英文完整作答」的面試題(從 interview-bank 抽),讓 P6 之前英文面試肌肉已經在長。
- P6:full loop mock(原理 why-chain / 故障 scenario / k8s×SD / behavioral),英文模式。

### 4.5 English Ramp 微調

- 說的維持錯峰(新難主題堂降回術語卡層級)。
- 新增:寫的不錯峰。P3 起產出物(runbook、postmortem、README)一律英文書寫;寫作沒有即時壓力,是安全的加壓面,而且英文 runbook 直接可放 portfolio。
- 詞彙 recall 弱的對治:term 卡抽考改雙向(給中文情境要英文詞;給英文詞要機制解釋)。

### 4.6 Migration 模組:把 legacy 服務導入 k8s(學員 2026-07-09 點名新增)

Senior 面試常考「你會怎麼把一個現有服務搬進 k8s」,而且導入本身就是天然的 behavioral 素材(帶領導入 = senior 訊號)。掛進 capstone:給 shop platform 加一個「legacy 服務」(docker-compose 風格、設定寫死、狀態存本機檔案),演練完整導入流程:

1. Containerize:12-factor 盤點(設定外部化、log 進 stdout、無狀態化評估)。
2. 寫 manifests 接進平台:Service / Ingress / probe / resource 全套用前面所學(複利驗收點)。
3. 有狀態部分的搬遷策略:資料搬移、雙寫 vs 停機窗口的取捨。
4. Zero-downtime cutover:DNS / 流量逐步切換 + 每步驗證。
5. Rollback 計畫:切壞了怎麼退、退的前提是什麼。

定位:P5 之後、P6 之前(Helm/GitOps 都在手上才像真實導入)。產出英文 migration runbook 進 portfolio。

### 4.7 選修池 [FLEX](跑道盈餘的投資,由當時教練依 mock 結果挑)

不全上。P2a/P3 迷你 mock 與 P6 前段 mock 暴露哪塊弱、或目標公司 JD 點名哪塊,才排哪塊:

| 候選 | 面試會怎麼考 |
|------|-------------|
| Service mesh 概念(sidecar、mTLS、Istio) | 「Ingress 跟 service mesh 差在哪?什麼時候才真的需要 mesh?」 |
| Stateful workloads / operator 模式深化 | 「資料庫該不該跑在 k8s 上?operator 幫你做掉了什麼?」 |
| Multi-cluster 與 DR | 「一個 region 掛了,你的平台怎麼活下來?」 |
| Cost / FinOps(接 P3 Karpenter) | 「叢集帳單要砍 30%,你從哪下手、怎麼證明沒砍到可靠性?」 |

### 4.8 CKA sprint(2026-07-09 從 P6 副線升級為正式里程碑)

北極星仲裁下 CKA 本身不是目的,但履歷過篩有用,且考綱與 P5 高度重疊(kubeadm 叢集、etcd backup/restore、troubleshooting),邊際成本低,值得正式排入。

- 時點:P5 畢業後(約 2026 年 11-12 月),證書趕在投遞前到手。
- 形式:2-3 週 sprint,主練限時手速(正是平時課刻意降為副線的東西):kubectl 速查、kubeadm 建叢集與升級、etcd backup/restore 實作、故障題限時。
- 與主線的分工:原理已在 P0-P5 打穿,sprint 只補「速度與考試格式」,不重教概念。
- [FLEX] 報名日期由學員定,教練依考試日倒推 sprint 開始日。

## §5 里程碑與時間軸(面試窗口:2027 農曆新年,約 2 月中)

跑道約 30 週,遠多於主線所需,策略從「趕進度」改為「加深加廣」:主線照 scope-based 節奏走,多出來的時間投給 CKA、migration 模組、選修池與更長的 P6。

| 里程碑 | 預估堂數 | 日曆落點(依週 4-5 堂實測節奏推) |
|--------|---------|--------------------------------|
| P2a 畢業(NetPol + CNI 全鏈 + gate + 迷你 mock) | 4-5 | 2026 年 7 月中下旬 |
| P2b 畢業(含 EKS 首登 IRSA) | 5-6 | 8 月中 |
| P3 畢業(大 chaos + capacity + 迷你 mock) | 7-8 | 9 月中 |
| P4 畢業(SLO + trace) | 5-6 | 10 月上旬 |
| P5 畢業(GitOps 閉環 + EKS IaC) | 6-8 | 11 月上旬 |
| CKA sprint + 考試(§4.8) | 8-12 | 11-12 月 |
| Migration 模組(§4.6) | 3-4 | 12 月 |
| 選修池 + P6 面試衝刺(full mock 連發) | 10 起跳 | 12 月至 2027 年 1 月 |
| 開始投遞 | - | 2027 年 2 月(農曆新年前後),內含 3-4 週 buffer |

[FLEX] 日曆是估算不是承諾;每過一個 phase gate 重算一次並回寫本表。節奏掉了先吃 buffer 與選修池,再壓縮 migration,主線與 CKA 最後才動。

## §6 面試對齊地圖(哪個 phase 餵哪個 round)

| Senior SRE loop round | 餵它的來源 |
|-----------------------|-----------|
| Linux / 網路 troubleshooting 深挖 | P2a + foundations-linux-network + chaos-drills |
| k8s / 平台深挖(原理 why-chain) | P0-P3 + interview-bank Q-P |
| 大型故障 scenario / incident 處理 | P3 大 chaos + P4 SLO + 英文 runbook |
| System design(infra 味) | sd-coach 主責;P6 只補 k8s×SD 交集 |
| Coding / scripting | leetcode-coach 主責;[FLEX] 若 mock 顯示需要,P6 可加少量 ops scripting(log 解析、API 撈數據),不重造課程 |
| Behavioral / leadership | story-bank(M4 保底 mining)→ P6 STAR 英文提煉 |

邊界不變:SD 與 coding 不在本 skill 重造(memory [[parallel-tracks-coding-sd]])。

## §7 重規劃觸發器(給 Opus 4.8+)

1. 面試窗口已定為 2027 農曆新年(2026-07-09)。若窗口提前、或提早收到面試邀約 → 從新日期倒推重排:先砍選修池,再壓縮 migration 模組與 CKA sprint,最後才砍 P5 深度(etcd 運維、upgrade 策略降為口頭教材),北極星仲裁:面試贏。
2. 連續 2 個 gate 一次過且 scorecard 全綠 → 加速:合併 chunk、英文檔位提前一級。
3. 同一弱點 pattern(§2 W1-W3)跨兩個 phase 仍反覆 → 停進度,開 2-3 堂專項 drill,補完再走。
4. 節奏跌破每週 2 堂且持續兩週 → 縮 scope:P5 砍到「Helm + ArgoCD 最小閉環」,P4 SLO 只做一個服務。
5. 公司工作出現真實素材(incident、新專案)→ 機會主義吸收:當堂改題材,真實素材優先於教材。
6. 本檔任何估算與現場衝突 → 現場贏,回寫本檔並註記日期。

## §8 戰略級 park 事項(runtime 細節仍以 progress.md 為準)

- etcd Raft 深入:P5。
- metrics-server 重裝:P3 開場前置(kind 需 `--kubelet-insecure-tls`)。
- CKA:2026-07-09 已升級為正式里程碑,見 §4.8(不再是 P6 副線)。CKAD 不考,不排。
- 三分類牌(M2)首發:建議下堂(s15)A 段就上,拿 conntrack 07-09 到期重抽當開刀題。

## §9 Conditional sprint overlay(2026-07-17;§7.1 觸發器進入待命,邀約未確認前主線不重排)

學員 2026-07-16 投遞外部 consultant 職缺(雲端原廠、delivery 導向),可能 4-8 週內面試。
確認邀約才走 §7.1 倒推重排;等待期間掛 overlay:

- **題材偏向 EKS/AWS 面**:課表內容與順序不變,但例題與 drill 情境優先挑 EKS 相關 — P2a 進行中的
  CNI 正好接「CNI 與 VPC 的關係」;P2b 的 IRSA 權重加重;「客戶要把自建 k8s 搬上 EKS 怎麼規劃」
  當 scenario 題(對接 §4.6 migration 模組的思路,先口頭版)。
- **AWS 廣度散裝卡進 A 段抽考池**(不開新 chunk):VPC 設計、SG vs NACL、TGW、DX/VPN、
  landing zone 一句話。每張卡 30 秒層級,走既有 term 卡機制。
- **M4 story mining 頻率加倍**:consultant loop 的 behavioral 佔比 ~50%,Weekly Review 的
  10 分鐘挖礦改為每場都跑;raw 一行入帳即可,STAR 提煉不在本 repo 做。
- LC 維持一天一題;session 佔比調度由學員自行控制,本檔不管跨 coach 排程。
