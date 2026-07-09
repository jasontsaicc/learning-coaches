# P3 調度與韌性: 扛住流量尖峰的部署設計 ⭐

> **如何使用此檔:** 這是 P3 階段(加重 phase)的教學素材庫,供 coach 在 C 段讀取並改編。
> 不要逐字唸稿,依學員反應選擇要深挖哪個切面。每個 chunk 通過 Feynman Gate 後再往下走。
> P3 起英文檔位升級:First-Principles Dive 段落直接用英文寫,教學時保持中文骨幹,
> 英文段落可以讓學員先讀再用中文複述(這本身就是 Say-it-in-English 的反向練習)。
> 學員歷史注意:P0 盲講曾漏 scheduler(session 10 Weekly Review 記錄在案),
> C-1 的誘答與追問優先往「scheduler 是哪一棒、做完什麼就收手」打。
> [RUNTIME: 開講前查 mistake-registry 與 progress.md 最新弱點,調整誘答選題]

---

## P3 學習藍圖

**目標**: 能在白板上設計一份「扛得住流量尖峰、計畫性變動不掉請求」的部署,並說清楚每個決策背後的機制。這是第一個直接對準 senior 面試白板題形狀的 phase。

**P3 中心問題**: 「流量在 10 分鐘內漲 10 倍,你的部署怎麼做到不掉請求?」

每個 chunk 都在回答這個問題的一塊拼圖:Pod 要被排到對的地方(C-1/C-2)、數量要自動長(C-3/C-4)、節點要跟得上(C-5)、計畫性變動不能自傷(C-6)、最後全部組起來(C-7)。

**學習路徑(Simon 切塊)**:

| Chunk | 主題 | 核心問題 | 屬性 |
|-------|------|---------|------|
| C-1 | Scheduler 內部機制 | Pending 的 Pod 在 scheduler 裡經歷了什麼? | keystone |
| C-2 | 調度約束工具箱 | 怎麼告訴 scheduler「該去哪 / 不該去哪 / 要打散」? | |
| C-3 | HPA 水平自動縮放 | 誰決定 replicas 該變多少?為什麼突刺會打穿它? | keystone ⭐ |
| C-4 | VPA 與 in-place resize | 改 Pod 的「大小」而非「數量」,和 HPA 怎麼共存? | |
| C-5 | Cluster Autoscaler vs Karpenter | Pod 沒地方跑,誰去生節點?要等多久? | |
| C-6 | PDB + drain + graceful shutdown | 計畫性變動怎麼一個請求都不掉? | keystone |
| C-7 | Capacity planning 總合設計 | 把 C-1 到 C-6 組成一份白板答案 | gate 總合 |

**環境前置**: `bash scripts/lab-cluster.sh up p0` 起 3 節點 kind cluster,context 是 `kind-k8s-coach-p0`。
**安全鐵律**: 每個 lab 動手前先 `kubectl config current-context`,確認輸出是 `kind-k8s-coach-p0` 才准 apply(機器上有公司 PROD EKS kubeconfig)。
**metrics-server 目前沒裝**(2026-06-28 叢集重建後消失,progress.md 有記),C-3 lab 的第一步就是重裝,步驟在 C-3。

---

## C-1: Scheduler 內部機制(keystone)

### 核心概念:P0 的三步直覺,現在打開引擎蓋

P0 學過 scheduler 的三步:Filter(過濾不合格 node)→ Score(打分)→ Bind(把 nodeName 寫回)。這是對的,但只是「一顆 Pod 進來怎麼處理」。真實 scheduler 還要回答:幾百顆 Pod 排隊時誰先?排不進去的 Pod 放哪?什麼時候重試?

```
                    scheduler 內部

  新 Pod ──> [activeQ 排隊中] ──pop──> 排程週期
                  ^    ^               Filter -> Score -> Reserve -> Bind
                  |    |                  |
                  |    |             全部 node 被刷掉
                  |    |                  v
             backoff到期  叢集有變化   [unschedulableQ 冷宮]
                  |    |                  |
             [backoffQ] <── 排程失敗後先進這裡(指數退避 1s,2s,4s...max 10s)
```

三條 queue 的分工:

- **activeQ**: 等著被排程的 Pod,priority 高的先出隊。
- **backoffQ**: 剛失敗的 Pod 先冷靜一下(指數退避),避免熱迴圈空轉。
- **unschedulableQ**: 確定目前排不進去的 Pod(例如所有 node 資源都不夠)。它不是每秒重試,而是等「叢集事件」喚醒:新 node 加入、某個 Pod 被刪、node label 變了,相關的 Pod 才被撈回 activeQ。

這個設計直接連回 P0 的 level-triggered 直覺:scheduler 不記「我試過幾次」的歷史來決定行為,它等狀態變化再看一次現況。

### Scheduler Framework:三步其實是十幾個擴充點

Filter/Score 不是寫死的兩個函式,而是一條 plugin pipeline。主要擴充點(面試講得出五六個就夠):

```
QueueSort -> PreFilter -> Filter -> PostFilter -> PreScore -> Score
          -> Reserve -> Permit -> PreBind -> Bind -> PostBind
                                    (失敗會觸發 preemption 的是 PostFilter)
```

預設 plugin 舉例(每個都同時掛在多個擴充點上):

| Plugin | 做什麼 | 掛在哪 |
|--------|--------|--------|
| NodeResourcesFit | requests 加總 ≤ allocatable 才過(回扣 P1:requests 是排程貨幣) | Filter + Score |
| ImageLocality | node 上已有這個 image 的給高分(省拉 image 時間) | Score |
| TaintToleration | node 有 taint 且 Pod 沒 toleration → 刷掉 | Filter + Score |
| PodTopologySpread | 檢查/偏好符合 topologySpreadConstraints | Filter + Score |
| InterPodAffinity | pod affinity/anti-affinity 規則 | Filter + Score |

### Preemption:資源不夠時,誰被犧牲?

Pod 全部 node 都過不了 Filter 時,PostFilter 階段啟動 preemption(前提:這個 Pod 的 priority 比較高):

1. 找一個 node:如果趕走一些低 priority 的 Pod,這個 Pod 就塞得下。
2. 挑犧牲者(victims):只挑 priority 比自己低的;盡量少殺;盡量不違反 PDB(best effort,不是保證,C-6 會回來咬這句)。
3. 犧牲者走 **graceful termination**:SIGTERM + `terminationGracePeriodSeconds`,不是瞬殺(回扣 P1 exit code 137 = 128+9 是 SIGKILL,graceful 走的是 SIGTERM=143 路徑)。
4. 高 priority Pod 拿到 `nominatedNodeName`,等空間騰出來後再走一次正常排程(不保證最後一定落在那台)。

### 動手觀察

```bash
kubectl config current-context
kubectl -n kube-system get pods -l component=kube-scheduler
kubectl create deployment sched-demo --image=nginx --replicas=3
kubectl get events --sort-by=.lastTimestamp | grep -i sched
kubectl get pod -l app=sched-demo -o wide
```

製造一顆永遠 Pending 的 Pod 看 unschedulableQ 的行為:給學員規格,他自己寫 YAML:「一個 Pod,requests.cpu 設 100(一百顆 CPU),故意排不進去」。

```bash
kubectl apply -f portfolio/manifests/pending-demo.yaml
kubectl describe pod pending-demo
```

看 Events 裡的 `0/3 nodes are available: 3 Insufficient cpu`。引導問題:「這顆 Pod 現在住在 scheduler 的哪條 queue?scheduler 是每秒重試它,還是在等什麼?」然後刪掉一個佔資源的 Pod 或加 node(思想實驗即可),問「什麼事件會把它撈回 activeQ?」

### First-Principles Dive(英文段)

The scheduler is a single-writer assignment service on top of the P0 watch pattern. It never talks to kubelet. Its entire job ends at one API call: writing `pod.spec.nodeName` through the API server (the Bind step). After that it forgets the Pod. The kubelet on the chosen node independently watches for Pods bound to it and takes over. This is the pipeline decoupling principle from P0: components coordinate through state in etcd, never through direct calls.

The queue design solves a classic systems problem: retry without busy-looping. A hot retry loop wastes CPU and hammers the API server; a fixed long retry interval makes scheduling sluggish. The answer is the same one TCP uses for congestion and clients use for rate-limited APIs: exponential backoff, plus event-driven wakeup so a Pod does not wait out its backoff when the world has already changed (a node just got freed). Compare: conntrack (P2a) also avoids recomputing per-packet by caching a decision; here the scheduler avoids recomputing per-second by sleeping until a relevant event.

**遷移題**: 「AWS SDK 對 API throttling 的重試策略也是 exponential backoff + jitter。scheduler 的 backoffQ 和它解的是同一個什麼問題?如果沒有 unschedulableQ、全部靠 backoff 重試,會發生什麼浪費?」

### 誘答彈藥(keystone 必備)

1. 「scheduler 選好 node 之後,會呼叫那台 node 的 kubelet 去啟動容器,確認啟動成功才處理下一顆 Pod。」
   (錯。Bind 只是把 nodeName 寫回 API Server,scheduler 就收手了;kubelet 自己 watch 到才動工。直打學員 P0 盲講漏 scheduler、以及「哪一棒做完什麼就交棒」的邊界。)
2. 「Pod 一直 Pending 是因為 scheduler 每秒都在重跑一次 Filter,只是每次都失敗。」
   (錯。排不進去的 Pod 進 unschedulableQ 等事件喚醒,不是熱迴圈。追問:那它怎麼知道該醒了?)
3. 「preemption 發生時,被犧牲的 Pod 會被立刻 SIGKILL,騰出空間愈快愈好。」
   (錯。victims 走 SIGTERM + grace period 的 graceful termination。回扣 P1:137 才是 SIGKILL。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 尖峰時大量 Pod Pending,老闆問「加了 HPA 為什麼還是沒擴起來」 |
| **生產怎麼做** | `kubectl describe pod` 看 Events 的 Filter 失敗訊息(`Insufficient cpu` / `didn't match node affinity` / `untolerated taint`),它會告訴你是哪個 plugin 刷掉了所有 node。這是 P3 版的 symptom→棒次地圖:Pending 永遠先問 scheduler 被什麼規則卡住 |
| **真實踩坑** | 平台團隊給關鍵服務設了高 priorityClass,尖峰時 preemption 把監控 agent(低 priority DaemonSet 以外的收集器)殺了,結果「服務活著但看不到 metrics」,排障時一片盲。教訓:priority 是雙面刃,誰會被犧牲要事先想 |
| **面試怎麼問** | 「Describe what happens inside the scheduler between a Pod being created and nodeName being set. What happens if no node fits?」 |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| preemption | /priˈemp.ʃən/ | Evicting lower-priority Pods to make room for a higher-priority pending Pod | 高優先 Pod 排不進去時,趕走低優先的騰位子,victims 仍走 graceful termination |
| backoff | /ˈbæk.ɒf/ | Retrying with exponentially increasing delays to avoid busy-looping | 失敗重試間隔指數拉長,省資源也給世界時間變化 |

---

## C-2: 調度約束工具箱(affinity / taints / topologySpread)

### 核心概念:兩種語氣,四樣工具

告訴 scheduler 去哪,有兩種語氣:

- **Pod 說「我想去/不想去」**: nodeSelector、nodeAffinity、podAffinity、podAntiAffinity。
- **Node 說「別來,除非你有通行證」**: taint(node 上的拒絕標記)+ toleration(Pod 的通行證)。

方向性是關鍵:**taint 是推力,affinity 才是拉力。toleration 只是「不被推走」,它不會把 Pod 吸過去。**

```
   nodeAffinity:   Pod ──想去──> Node          (拉力)
   taint:          Node ──推開──> 所有 Pod      (推力)
   toleration:     Pod 拿通行證,推力對它失效     (中和推力,不產生拉力)
   要「專用節點」= taint(別人進不來)+ nodeAffinity(自己人一定去)兩個一起用
```

taint 有三種 effect:`NoSchedule`(新的別來)、`PreferNoSchedule`(盡量別來)、`NoExecute`(已經在上面的也趕走)。

**複利回扣(P0 drill P0-2)**: 你做過 `kubectl cordon`,當時觀察到新 Pod 不再被排上去。現在揭底:cordon 就是把 node 標成 unschedulable,底層由系統加上 `node.kubernetes.io/unschedulable:NoSchedule` 這個 taint。你以為的「特殊指令」其實是同一套 taint 機制。node NotReady 時系統自動加的 `node.kubernetes.io/not-ready:NoExecute` 也是,這就是 node 掛掉後 Pod 會被驅逐重建的機制。

### nodeAffinity vs podAffinity:成本差一個量級

- **nodeAffinity**: 對每個候選 node,比對 node 自己的 label。成本 = O(nodes)。
- **podAffinity/antiAffinity**: 對每個候選 node,要看「這個 topology domain 裡跑著哪些 Pod、它們的 label 是什麼」。成本和叢集裡的 Pod 數相關,大叢集上是出名的排程慢速殺手(官方文件明寫不建議在數百節點以上重度使用)。

能用 node label 表達的就別用 podAffinity。

### 打散副本:podAntiAffinity vs topologySpreadConstraints

可用性設計的核心動作:別讓同一服務的副本擠在同一個故障域(node、AZ)。

- **podAntiAffinity(required)**: 硬互斥,「同 topology domain 內不准有第二顆」。3 副本 3 node 剛好;第 4 顆直接 Pending。表達力粗:只有「准/不准」。
- **topologySpreadConstraints**: 用 `maxSkew` 控「最多和最少的 domain 差幾顆」,能表達「盡量平均」。`topologyKey: topology.kubernetes.io/zone` 就是跨 AZ 打散,EKS 上這個 label 由雲端自動打在 node 上。`whenUnsatisfiable: ScheduleAnyway` 可以降級成軟性偏好。

現代預設選 topologySpread 打散、antiAffinity 留給「絕對不能同居」的場景(例如同一 quorum 的成員)。

### 動手觀察

```bash
kubectl config current-context
kubectl taint nodes k8s-coach-p0-worker dedicated=batch:NoSchedule
kubectl create deployment taint-demo --image=nginx --replicas=4
kubectl get pods -o wide
```

觀察:4 顆全部擠在 worker2(control-plane 本來就有自己的 taint,worker 被你 taint 了)。引導:「現在幫 Pod 加 toleration,再 scale 幾顆,新 Pod 會全部跑去 worker 嗎?」(不會,toleration 只是讓 worker 回到候選名單,Score 決定去哪。這一步直接驗證誘答 1。)

topologySpread 實驗規格(學員自己寫 YAML):Deployment 6 副本,`topologySpreadConstraints` 以 `kubernetes.io/hostname` 為 topologyKey、maxSkew 1、DoNotSchedule。觀察每台 node 分到 3/3(worker 還有 taint 時)或 2/2/2。

```bash
kubectl get pods -o wide | awk '{print $7}' | sort | uniq -c
kubectl taint nodes k8s-coach-p0-worker dedicated=batch:NoSchedule-
kubectl delete deployment taint-demo
```

### First-Principles Dive(英文段)

All four tools compile down to the same thing: extra predicates and scores inside the C-1 pipeline (TaintToleration, NodeAffinity, InterPodAffinity, PodTopologySpread plugins). There is no separate machinery; declaring intent on the Pod or the Node just changes what Filter rejects and what Score prefers.

The deeper principle is failure-domain isolation from distributed systems: replicas only buy availability if their failure modes are independent. Two replicas on one node share a kernel, a disk, a power supply; two replicas in one AZ share a data-center-level blast radius. Spreading is how you purchase independence, and the currency is scheduling flexibility (stricter spread = more Pending risk). `maxSkew` is literally a knob on that trade.

**遷移題**: 「RAID 1 把資料放兩顆碟、EKS 建議 node group 跨 3 個 AZ、etcd 要 3 節點跨 AZ(P0 學過 quorum)。這三件事和 topologySpread 共用哪一條原理?各自的『打散成本』是什麼?」

### 誘答彈藥

1. 「幫 Pod 加了 toleration 之後,它就會被排到有對應 taint 的節點上,所以 toleration 可以拿來做專用節點。」
   (錯。toleration 只是允許、不是吸引;Pod 可能照樣被排去沒 taint 的 node。專用節點 = taint + nodeAffinity 成對使用。)
2. 「cordon 和 taint 是兩套獨立機制,cordon 是比較高階的管理指令。」
   (錯。cordon 底層就是 unschedulable 的 NoSchedule taint,和 P0-2 drill 看到的行為同源。)
3. 「要把 6 個副本平均鋪在 3 個 AZ,用 required podAntiAffinity、topologyKey 設 zone 就行。」
   (錯。required antiAffinity 是「每 zone 最多 1 顆」,第 4 顆起全 Pending。平均打散要 topologySpread 的 maxSkew。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | EKS 上一次 AZ 故障,billing API 全掛,事後發現 8 個副本全在同一個 AZ |
| **生產怎麼做** | 關鍵服務標配:`topologySpreadConstraints` zone 級 maxSkew 1 + hostname 級 ScheduleAnyway;GPU/特殊機型用 taint+nodeAffinity 圈專用池。這些寫進部署範本讓所有團隊繼承,不是靠每個工程師記得 |
| **真實踩坑** | 給 GPU 節點只加了 taint 沒配 nodeAffinity,結果 GPU workload 有 toleration 卻被 Score 排去便宜的一般節點(那裡沒 GPU),Pod 起來就 crash。反過來的坑:required antiAffinity 寫死,rolling update 時 maxSurge 的新 Pod 沒地方放,更新卡死 |
| **面試怎麼問** | 「Taints and tolerations vs node affinity: which one repels, which one attracts? How would you build a dedicated node pool?」 |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| taint | /teɪnt/ | A node-side mark that repels Pods lacking a matching toleration | node 端的推力;toleration 只中和推力,不產生拉力 |
| topology spread | /təˈpɒl.ə.dʒi spred/ | Constraints that limit replica count skew across failure domains | 用 maxSkew 把副本鋪平在 node/AZ 等故障域上 |

---

## C-3: HPA 水平自動縮放(keystone ⭐,本 phase 主戰場)

### 核心概念:HPA 也是一個 reconcile loop

HPA 不是魔法,是 P0 的老朋友:一個 controller,desired state 是「metric 維持在 target」,actuator 是改 Deployment 的 replicas。

核心公式(必背,面試會叫你手算):

```
desiredReplicas = ceil( currentReplicas * currentMetric / targetMetric )
```

例:3 副本、target CPU 50%、當前平均 80% → ceil(3 * 80/50) = ceil(4.8) = 5。
比值在 1.0 ± 0.1 內(tolerance)就不動,避免為了 2% 的偏差抖動。

注意分母:CPU 的 `currentMetric` 是「用量佔 **requests** 的百分比」。requests 沒設好,HPA 的地基就是歪的(回扣 P1:requests 是一切資源機制的定價單位)。

### Metrics 資料鏈:數字從哪來

```
container (cgroup 統計)
   -> kubelet 內建 cAdvisor 蒐集 (node 本地)
   -> metrics-server 定期向每台 kubelet 抓 (預設 15s 一輪)
   -> 註冊成 metrics API (kubectl top 也是吃這個)
   -> HPA controller 每 15s 同步一次,套公式
   -> 改 Deployment.spec.replicas -> 後面就是 P0 五棒
```

metrics-server 只存最近一筆、放記憶體,不是監控系統;Prometheus 才是長期存放(P4 預告)。

### 為什麼 CPU-based HPA 對突刺流量反應慢(第一性拆解)

把延遲逐段加總,這是本 chunk 最重要的一張帳單:

```
流量開始暴漲
  + 0~15s   cAdvisor/metrics-server 還沒抓到新數字(取樣間隔)
  + 0~15s   HPA 還沒到下一次同步
  + 公式生效,replicas 改了(但這只是「願望」變了)
  + 秒級~分鐘級  新 Pod 排程 + 拉 image + 容器啟動 + readiness 過關(P1)
  + (最壞情況) node 不夠 -> 等 autoscaler 生節點,再加 1~5 分鐘(C-5)
  ≈ 從尖峰開始到新容量真正接流量:常見 1~3 分鐘,壞情況更久
```

而且 CPU 是落後指標:使用率飆高時,傷害已經在發生(排隊、latency 上升)。所以 senior 的答案永遠是「HPA 管趨勢,headroom 管突刺」(C-7 收斂)。

### Stabilization window:防抖動

流量鋸齒狀時,metric 在 target 上下穿梭,HPA 會加了又刪、刪了又加(flapping),每次都付出 P0 五棒 + 暖機的成本。解法是 `behavior.scaleDown.stabilizationWindowSeconds`(預設 300s):縮容時看「過去 5 分鐘窗口內的最大 desired 值」,只採最保守的那個。方向不對稱是刻意設計:**擴容要快(少擴的代價是掉請求),縮容要慢(少縮的代價只是多花錢)**。`behavior` 還能限速,例如「每分鐘最多砍 10% Pod」。

### Custom metrics 概念

CPU 不等於負載:queue consumer 的正確訊號是 queue depth,web 服務常是 RPS 或 p99 latency。這些走 custom/external metrics API(Prometheus Adapter 或 KEDA 轉接),HPA 公式不變,只是換了 metric 來源。優點:queue depth 是領先指標,比 CPU 更早看到尖峰。細節留到 P4 observability,這裡建立「訊號選對比調參重要」的觀念即可。

### 動手 Lab:裝 metrics-server + 打出一次 scale-up

**Step 0 安全檢查 + 重裝 metrics-server**(叢集 2026-06-28 重建後就沒了):

```bash
kubectl config current-context
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl -n kube-system patch deployment metrics-server --type=json -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deployment metrics-server
kubectl top nodes
```

kind 的 kubelet 用自簽憑證,不加 `--kubelet-insecure-tls` 這支旗標 metrics-server 會起不來(上一輪環境就是這樣裝的,progress.md 有記)。`kubectl top nodes` 有數字才算裝好。

**Step 1 部署目標服務**(規格,YAML 學員自己寫,存 `portfolio/manifests/hpa-demo.yaml`):
Deployment `php-apache`,image `registry.k8s.io/hpa-example`,1 副本,container port 80,requests.cpu `200m`、limits.cpu `500m`;外加同名 ClusterIP Service 打到它(P2a 肌肉記憶:寫完先 `kubectl get endpoints php-apache` 確認清單有 Pod IP)。

**Step 2 建 HPA 並預測**:

```bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
kubectl get hpa
```

先讓學員用公式預測:「如果壓到平均 CPU 250m(= requests 的 125%),desired 是多少?」(ceil(1 * 125/50) = 3)

**Step 3 施加負載,兩個 terminal 對照**:

```bash
kubectl run load-gen --rm -it --restart=Never --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://php-apache >/dev/null; done"
```

另一個 terminal:

```bash
kubectl get hpa php-apache -w
```

觀察重點:TARGETS 從 `<unknown>` 到數字要等一輪 metrics(親身體感取樣延遲);REPLICAS 跳上去的時間點 vs 你開始加壓的時間點,差距就是上面那張延遲帳單。Ctrl-C 停掉 load-gen 後,注意縮容**不會**馬上發生,盯著它等 stabilization window 過完(約 5 分鐘),這是親眼看 anti-flapping。

```bash
kubectl delete hpa php-apache
kubectl delete deployment php-apache
kubectl delete service php-apache
```

[RUNTIME: 若學員行有餘力,加碼實驗:把 requests.cpu 改成 100m 重跑,觀察同樣負載下 desired 翻倍,體感「分母是 requests」]

### First-Principles Dive(英文段)

HPA is a feedback controller, the same control-theory family as the thermostat from P0, but with two properties that make it harder: **dead time** and **actuator lag**. Dead time is the metrics pipeline delay (the controller observes the past, not the present). Actuator lag is Pod startup: changing `replicas` changes intent instantly, but capacity arrives only after scheduling, image pull, and readiness. In control terms, a controller with significant dead time reacting to a step input (traffic spike) will always overshoot or lag; no tuning of the target percentage fully removes this, because the delay is structural, not parametric.

The stabilization window is a low-pass filter on the controller output: it removes high-frequency oscillation (flapping) at the price of slower downscale response. The asymmetry (fast up, slow down) encodes a business judgment directly into the control loop: dropped requests cost more than idle Pods.

**遷移題**: 「冷氣壓縮機有『停機保護延遲』(關掉後幾分鐘內不准再啟動),防止頻繁啟停燒壞壓縮機。這對應 HPA 的哪個機制?兩者各自付出什麼代價換穩定?」

### 誘答彈藥(keystone 必備,至少埋一題)

1. 「突刺流量交給 HPA 就好,CPU 一超標它馬上就會加 Pod。」
   (錯。取樣延遲 + 同步週期 + Pod 啟動 + 可能還要等節點,結構性延遲 1~3 分鐘起跳,突刺早就打完了。HPA 抓趨勢,突刺靠 headroom。)
2. 「把 target CPU 從 50% 調低到 30%,HPA 就等於即時反應了。」
   (半錯,最值得辯的一題。調低 target = 平時多養 Pod = 用常態成本買緩衝,反應「延遲」一秒都沒少,只是尖峰打來時現有 Pod 撐得久一點。要學員分清「延遲」和「緩衝」是兩個變數。)
3. 「壓測停了 replicas 遲遲不掉,是 metrics-server 更新太慢,該把它的抓取間隔調短。」
   (錯。那是 scaleDown stabilization window 在防 flapping,刻意的。層級混淆誘答:資料鏈延遲是秒級,穩定窗是分鐘級,兩層別混。學員的層級混淆前科在 DNS vs NAT,這題同款。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | billing 平台月底出帳日流量規律性暴漲,HPA 每次都慢半拍,前 3 分鐘一堆 5xx |
| **生產怎麼做** | 三件組:HPA 管日常波動;出帳日是可預測尖峰,用 CronJob 或 scheduled scaling 提前把 minReplicas 抬高(predictive 勝 reactive);再配 C-7 的常態 headroom 吃突發。metric 若能改用「待出帳單佇列深度」這種領先指標更好 |
| **真實踩坑** | requests.cpu 設了 2 核但實際只用 100m,CPU 百分比永遠 5%,HPA 永遠不擴,尖峰直接躺平。根因不在 HPA,在 requests 亂設(分母壞掉)。反向坑:沒設 requests,percentage 型 HPA 直接不工作,`kubectl describe hpa` 會看到 FailedGetResourceMetric |
| **面試怎麼問** | 「Walk me through the HPA formula. Why does CPU-based HPA respond poorly to traffic spikes, and what would you do about it?」(第二問就是 C-7 的入口) |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| stabilization window | /ˌsteɪ.bəl.aɪˈzeɪ.ʃən ˈwɪn.doʊ/ | A look-back period where HPA picks the most conservative desired value to prevent flapping | 縮容前回看 5 分鐘取最保守值,防抖動的低通濾波 |
| cAdvisor | /siː.ædˈvaɪ.zər/ | The kubelet-embedded agent that collects container resource usage from cgroups | 內建在 kubelet 裡讀 cgroup 統計,metrics 資料鏈第一棒 |
| flapping | /ˈflæp.ɪŋ/ | Rapid oscillation between scale-up and scale-down around a threshold | 在門檻上下反覆加刪 Pod,每次都白付啟動成本 |

---

## C-4: VPA 與 in-place resize

### 核心概念:另一個縮放軸

HPA 動「數量」,VPA(Vertical Pod Autoscaler)動「大小」:觀察歷史用量,建議或直接改 requests/limits。適用場景:單體型、難水平擴的 workload(有狀態、單例 job),或用 `updateMode: "Off"` 純出建議、給人審(生產最常見的用法,拿來治 P1 學過的「requests 亂設」病)。

傳統 VPA 最大的痛:改 resources 要**重建 Pod**(cgroup 值在建立時定死)。**In-place pod resize**(K8s 1.33 起 beta 的 InPlacePodVerticalScaling)讓 kubelet 直接改運行中容器的 cgroup 上限,CPU 可以不重啟就調;回扣 P1:requests/limits 底下就是 cgroup 的數字,改數字本來就不必然要殺 process,重建只是舊實作的限制。memory 縮小仍然危險(已佔用的位元組無法壓縮,學員 session 10 親自推過這個第一性原理)。

### HPA/VPA 衝突

兩個 controller 讀同一個 CPU 訊號、動同一個 workload,會互相打架:VPA 看到 CPU 高 → 加大 requests → 百分比下降 → HPA 縮 replicas → 單 Pod 壓力回升 → VPA 再加大…兩個 reconcile loop 對同一個誤差訊號各自出手,系統震盪。規則:**同一個 metric 不能同時餵兩個 actuator**。共存的合法姿勢:HPA 用 custom metric(如 RPS),VPA 管 CPU/memory 定價。

**遷移題**: 「兩個恆溫器接同一間房,一個控冷氣一個控暖氣,設定溫度差 1 度,會發生什麼?這對應 HPA/VPA 衝突的哪個部分?」(控制迴路互相補償、能源白燒;對應同訊號雙 actuator 震盪。)

### 誘答彈藥

1. 「HPA 管數量、VPA 管大小,剛好互補,一起開最完整。」
   (預設錯。同吃 CPU 訊號會互打;只有訊號分離時才互補。)
2. 「有了 in-place resize,memory limit 也能隨便線上調了。」
   (半錯。調大可以;調小撞上不可壓縮性,已用掉的記憶體收不回來,縮過頭就是 OOM。回扣 P1 水龍頭 vs 水桶。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 全公司 requests 都是複製貼上的 500m/512Mi,沒人知道真實用量 |
| **生產怎麼做** | VPA `updateMode: Off` 全叢集鋪開當「建議引擎」,搭配 Prometheus 實際用量,季度性 rightsize;Goldilocks 這類工具就是把 VPA 建議做成看板 |
| **真實踩坑** | VPA 開 Auto 模式在低流量夜間縮小 requests,隔天早高峰 Pod 全是小杯,又觸發重建波(舊式 VPA 重建 = 全服務滾一輪),早上第一波流量最脆弱時自己滾自己 |
| **面試怎麼問** | 「Can HPA and VPA be used together on the same Deployment? What breaks?」 |

(本 chunk 無新術語卡,in-place resize 的錨點已用 cgroup/incompressible 舊卡覆蓋。)

---

## C-5: Cluster Autoscaler vs Karpenter(EKS 視角)

### 核心概念:第三層縮放,也是最慢的一層

HPA 加 replicas,但 node 塞滿時新 Pod 只能 Pending(C-1:NodeResourcesFit 刷掉所有 node)。誰去生新 node?兩派:

**Cluster Autoscaler(CA)**:按 **node group**(EKS = Auto Scaling Group)思考。看到 Pending Pod → 模擬「哪個 node group 加一台能救」→ 調 ASG desired count。限制:一個 group 內機型同質,想要多樣機型就要維護一堆 group;縮容保守,逐台檢查。

**Karpenter**(AWS 出品,學員公司 EKS 適用):跳過 node group 抽象,直接看 **Pending Pod 的總需求**(requests、affinity、topologySpread 全考慮),bin-packing 計算「什麼機型組合最省」,直接呼叫 EC2 Fleet 開機。快(省掉 ASG 這層)、機型彈性(spot/多機型混搭)、還有 consolidation(主動把碎片 node 上的 Pod 併一併、關掉空 node 省錢)。

```
HPA:       秒級決策 + Pod 啟動秒~分鐘級     (最快的一層)
CA:        Pending -> ASG -> EC2 -> bootstrap -> Ready,常見 2~5 分鐘
Karpenter: Pending -> EC2 Fleet 直開,常見 40s~2 分鐘
           (之後每顆 Pod 還要拉 image + readiness)
```

### 擴節點的時間成本 = 高並發設計的關鍵約束

這條要當鐵律記:**尖峰當下才開始生節點,一定來不及。** EC2 開機 + bootstrap + join cluster + image 拉取,最快也是分鐘級。所以扛尖峰設計裡,node autoscaler 的角色是「事後補地基」,不是「即時救火」。即時救火只能靠已經站著的容量(C-7 的 headroom / overprovisioning)。

### 動手觀察(kind 上做思想實驗 + 症狀辨認)

kind 沒有雲端 API,無法真擴節點,但可以精準製造「需要 autoscaler 的那個瞬間」:

```bash
kubectl config current-context
kubectl create deployment node-full --image=nginx --replicas=30
kubectl set resources deployment node-full --requests=cpu=500m
kubectl get pods | grep Pending | head -5
kubectl describe pod $(kubectl get pods -l app=node-full -o name | tail -1) | grep -A3 Events
```

看到 `0/3 nodes are available: 3 Insufficient cpu`:這一行就是 CA/Karpenter 的觸發訊號,兩者都是 watch 這種 Pending Pod 起跳的。引導:「如果這是 EKS + Karpenter,接下來 60 秒會發生什麼?列出時間軸。」

```bash
kubectl delete deployment node-full
```

[RUNTIME: EKS 選配 lab,依學員意願與時間。terraform 產生 `billing-dev-eks-karpenter` 測試 NodePool,指令只產生、學員親手跑,結束必附 terraform destroy + `aws ec2 describe-instances` 驗證無殘留]

### First-Principles Dive(英文段)

CA and Karpenter are both reconcile loops whose desired state is "no unschedulable Pods" and whose actuator is a cloud API. The interesting difference is where the abstraction boundary sits. CA delegates instance choice to a pre-defined group (ASG), so its decision space is "which group, how many": simple, but the group is a lossy abstraction that hides instance-type diversity. Karpenter collapses the abstraction and solves a small bin-packing problem per provisioning cycle: given these Pending Pods' requests and constraints, what is the cheapest set of instances that fits them? Removing an abstraction layer buys speed and precision at the cost of owning more decisions (Karpenter's NodePool config now encodes what the ASG used to).

This is a general infra pattern: every managed abstraction (ASG, node group) trades decision quality for operational simplicity. Senior engineers are paid to know when the abstraction's loss becomes the bottleneck.

**遷移題**: 「Lambda 冷啟動 vs 常駐 EC2、資料庫連線池 pre-warm vs 每次新建連線:這些和『節點供應時間成本』共用哪個底層 trade-off?」(容量的取得延遲 vs 閒置成本,答案永遠是分層:熱層吃突刺、冷層補趨勢。)

### 誘答彈藥

1. 「HPA 的 max 設大一點就能扛任何尖峰,反正 node 不夠 autoscaler 會自動加。」
   (錯。節點供應分鐘級,尖峰是秒級;autoscaler 補趨勢,補不了突刺。這題是 C-7 的門票。)
2. 「Karpenter 比 CA 快,是因為它程式寫得比較有效率。」
   (錯。是架構差異:跳過 node group/ASG 抽象層直接對 EC2 Fleet,還能跨機型 bin-packing。用詞精準度訓練:快在「少一層抽象」,不是「code 快」。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 公司 EKS 從 CA + 固定機型 node group 遷去 Karpenter |
| **生產怎麼做** | Karpenter NodePool 開多機型 + spot/on-demand 混合,關鍵服務用 nodeSelector 釘 on-demand;開 consolidation 但給 PDB 保護(C-6),不然它併節點時會滾動你的服務;帳單常見降 20~40%(spot + 碎片回收) |
| **真實踩坑** | Karpenter consolidation 半夜把低流量的 node 併掉,偏偏某服務沒設 PDB 也只有 1 副本,被搬遷瞬斷;白天大家只看到「服務凌晨閃斷之謎」。根因鏈:省錢功能 + 沒有可用性護欄 |
| **面試怎麼問** | 「Compare Cluster Autoscaler and Karpenter. Why is node provisioning time a design constraint for handling traffic spikes?」 |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| bin packing | /bɪn ˈpæk.ɪŋ/ | Fitting items of different sizes into the fewest containers | 把不同 requests 的 Pod 塞進最少/最便宜的機器組合,Karpenter 的核心計算 |
| consolidation | /kənˌsɒl.ɪˈdeɪ.ʃən/ | Actively repacking Pods onto fewer nodes and terminating the empty ones | Karpenter 主動併節點省錢;沒 PDB 護欄時它就是計畫性故障源 |

---

## C-6: PDB + drain + graceful shutdown(keystone)

### 核心概念:計畫性變動的「不掉請求」三件組

非計畫故障(node 暴斃)靠副本數和打散(C-2)。**計畫性變動**(升級 node、Karpenter 併機、rolling update)是自己動手殺 Pod,反而更常掉請求,因為人會太快。三件組:

1. **PDB(PodDisruptionBudget)**: 「同時最多倒幾顆」的預算。`minAvailable: 2` 或 `maxUnavailable: 1`。drain 用的 **Eviction API** 會先問 PDB,超出預算就拒絕驅逐(429),drain 卡住等待。注意分界:PDB 只管「自願中斷」(eviction),node 暴斃、OOM kill、直接 `kubectl delete pod` 都不歸它管;preemption 對 PDB 只是 best effort(C-1 埋的伏筆)。
2. **rolling update 參數(P1 學過)**: maxSurge/maxUnavailable 管的是「更新這個 Deployment 時」的節奏;PDB 管的是「外力驅逐時」的底線。兩套預算,別混。
3. **graceful shutdown**: 單顆 Pod 死得體面。這是本 chunk 的深水區,直接回扣 P2a。

### Pod 終止時序:那場 race condition

`kubectl delete pod`(或 eviction)之後,**兩條路徑同時起跑,互不等待**:

```
API Server 標記 Pod terminating
     |
     +── 路徑 A(資料面收斂,P2a 全鏈): Endpoints controller 把 Pod IP 移出
     |    EndpointSlice -> 每台 node 的 kube-proxy watch 到 -> 改寫 iptables
     |    (你在 P2a D 段親手追過的 KUBE-SVC/KUBE-SEP 鏈,現在是「拆規則」方向)
     |    傳播到全部 node 需要:非零的秒級時間
     |
     +── 路徑 B(殺程序): kubelet 先跑 preStop hook(如果有)
          -> SIGTERM -> 等 terminationGracePeriodSeconds(預設 30s)-> SIGKILL

race: 如果 app 收到 SIGTERM 立刻退出(路徑 B 秒完成),
      但某台 node 的 iptables 還沒更新(路徑 A 沒跑完),
      那台 node 上的新請求仍會被 DNAT 到已死的 Pod -> connection refused
```

**preStop sleep 的真正意義**:`preStop: exec: sleep 10` 把 SIGTERM 延後 10 秒,讓路徑 A 先跑完。在這 10 秒裡 Pod 還活著、還在正常服務,只是各 node 的轉發規則陸續把它移出名單。等 SIGTERM 真的到,已經沒有新請求進來,app 再把手上處理到一半的請求做完、優雅退出。

所以精確分工:**preStop sleep 擋「新請求還會進來」的 race;grace period 給「已收到的請求」時間做完。** 兩個機制,兩種請求。

app 端的責任:要會接 SIGTERM(開始拒新連線、排空中請求、關 DB 連線再退出)。app 無視 SIGTERM 的話,30 秒後 SIGKILL 硬殺,一切白搭。

### 完整的「不掉請求」故事(串 P1 + P2a + P3)

rolling update 一顆 Pod 的替換全程:新 Pod 起來 → readiness 過關(P1)→ 進 Endpoints、iptables 加規則(P2a)→ 開始接流量 → 舊 Pod 收到刪除 → preStop sleep 擋 race(本 chunk)→ SIGTERM 排空 → 退出;全程由 maxSurge/maxUnavailable(P1)控制節奏、PDB 保底線。這一串就是面試題「how do you achieve zero-downtime deployment」的完整答案。

### 動手 Lab:親手撞一次 PDB 卡 drain

規格(學員寫 YAML,存 `portfolio/manifests/pdb-demo.yaml`):Deployment `pdb-demo` 2 副本 nginx;PDB `minAvailable: 2` 對同一組 label(**故意設成無解**:2 副本要求永遠 2 顆活著)。

```bash
kubectl config current-context
kubectl apply -f portfolio/manifests/pdb-demo.yaml
kubectl get pdb
kubectl get pods -l app=pdb-demo -o wide
kubectl drain k8s-coach-p0-worker2 --ignore-daemonsets --delete-emptydir-data
```

觀察 drain 卡住,反覆吐 `Cannot evict pod as it would violate the pod's disruption budget`。引導:「誰在拒絕?拒絕的判斷依據是什麼?三個解法各自的代價?」(改 PDB 成 maxUnavailable:1 / 先 scale 到 3 副本 / 強制刪,只有最後一個會掉請求。)

```bash
kubectl patch pdb pdb-demo -p '{"spec":{"minAvailable":1,"maxUnavailable":null}}' --type=merge
kubectl get pods -l app=pdb-demo -o wide -w
kubectl uncordon k8s-coach-p0-worker2
kubectl delete -f portfolio/manifests/pdb-demo.yaml
```

drain 放行後注意:被驅逐的 Pod 是在別台 node 上**重建**(新名字新 IP),不是搬家。

[RUNTIME: 若時間夠,加做 preStop 對照組:同一 Service 下 rolling restart,一組無 preStop、一組 preStop sleep 10,用 while 迴圈 curl 對比錯誤數;完整劇本在 chaos-drills.md P3-4]

### First-Principles Dive(英文段)

The terminating-Pod race is a textbook eventual-consistency problem. Kubernetes has no distributed transaction that says "remove this backend from every node's forwarding table, then kill the process." Each kube-proxy converges independently through its own watch (the decentralized design you proved on P2a by diffing iptables across worker and worker2: no central chokepoint, therefore no central synchronization point either). The `preStop` sleep is not a hack; it is the standard technique for bridging asynchronous convergence: keep the old state serving until the new state has propagated, then transition. Load balancers call the same idea connection draining; DNS migrations do it by overlapping TTL windows. You cannot remove the race; you can only make the overlap longer than the propagation delay.

**遷移題**: 「換手機號碼時,你會讓舊號碼保留一個月轉接期,而不是當天停機。這對應 preStop sleep 的哪個部分?『轉接期要多長』對應 k8s 的哪個參數判斷?」

### 誘答彈藥(keystone 必備)

1. 「有 PDB 保護,drain 的時候 Pod 會被平滑地『搬』到別的 node,所以不會掉請求。」
   (錯兩層。Pod 從不搬家,是刪掉重建;PDB 也不保證不掉請求,只保證同時死的數量不超標。不掉請求要靠 readiness + preStop + grace period 整組。)
2. 「preStop sleep 是給 app 時間把手上的請求處理完。」
   (精度誘答,最值得辯。處理中的請求靠 SIGTERM 後的 grace period;preStop sleep 擋的是「iptables 還沒拆規則、新請求持續進來」的 race。答對這題 = P2a 真的打穿了。)
3. 「terminationGracePeriodSeconds 設 60,kubelet 就會等滿 60 秒才讓 Pod 消失。」
   (錯。那是上限不是定值;app 提早退出就提早結束。追問:那什麼情況會等好滿 60 秒還被 SIGKILL?)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | EKS 升級 node group,滾動換掉全部 node,期間 billing API 出現零星 502 |
| **生產怎麼做** | 全服務標配 PDB(maxUnavailable:1 或按容量算)+ preStop sleep 5~15s + app 實作 SIGTERM 排空 + ALB 端 deregistration delay 對齊 grace period。升級用「先擴後縮」姿勢降低風險窗 |
| **真實踩坑** | 兩個經典對撞:(a) 單副本服務 + minAvailable:1 的 PDB,node 升級 drain 永遠卡住,自動化 pipeline timeout 半夜叫醒 on-call;(b) 反過來沒設 PDB,Karpenter consolidation 一次驅逐同服務兩顆副本,可用性瞬間歸零。PDB 的兩個死法:設太緊卡運維,不設卡可用性 |
| **面試怎麼問** | 「A Pod receives SIGTERM during a rolling update but some clients still get connection errors. Walk me through the race and how you fix it.」(這題答不出 preStop 的人,P2a 就是沒學通) |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| eviction | /ɪˈvɪk.ʃən/ | The API-mediated, PDB-respecting way to remove a Pod from a node | 走 Eviction API 才問 PDB;直接 delete 不問。drain 用的是前者 |
| connection draining | /kəˈnek.ʃən ˈdreɪn.ɪŋ/ | Letting in-flight requests finish while refusing new ones before shutdown | 拒新、排舊、再退出;preStop+SIGTERM 組合的通用名字 |

---

## C-7: Capacity Planning 與扛尖峰設計(gate 總合)

### 核心概念:把 C-1 到 C-6 組成一份白板答案

面試白板題形狀:「Design a deployment on EKS that survives a 10x traffic spike without dropping requests.」答案骨架(這張圖就是 P3 的畢業考核物):

```
                     時間尺度分層(關鍵洞見:每層反應速度差一個量級)

   0 秒(尖峰當下) ── headroom:現有 Pod 的餘裕吃第一波
   │                  target CPU 50~60% 而非 90% = 常態就養著 2 倍空間
   │                  overprovisioning pause Pod(低 priority 佔位者)被 preempt 讓位
   │
   ~1 分鐘 ────────── HPA(C-3):metrics 鏈 + 公式,把 replicas 拉上去
   │                  訊號盡量用領先指標(RPS/queue depth)不是落後的 CPU
   │
   ~2-5 分鐘 ──────── Karpenter(C-5):Pending Pod 觸發生節點,補地基
   │
   全程護欄 ───────── topologySpread 跨 AZ(C-2)+ PDB(C-6)+ priorityClass(C-1)
                      + preStop/graceful(C-6)保證過程中不自傷
```

### requests 定價:capacity planning 的地基

- requests 是排程貨幣(P1 + C-1 NodeResourcesFit):全叢集的容量規劃就是「所有 Pod requests 加總 vs 所有 node allocatable 加總」的帳。
- 定價原則:requests 定在**常態尖峰值**(如 p95 用量),limits 給突發呼吸空間。CPU 可超賣(撞頂只是 throttle,可壓縮);memory 超賣是玩火(不可壓縮,撞頂即 OOM,學員 P1 親手做過 137)。
- 關鍵服務給 Guaranteed(requests==limits)買 QoS 最後生存權(P1 驅逐序:BestEffort 先死 → Burstable → Guaranteed)。

### headroom 與 overprovisioning

headroom = 付錢養著的閒置容量,是「結構性延遲買不掉,只能用容量預付」的直接結論(C-3/C-5)。兩種形態:

1. **Pod 級**: target utilization 設低(50% 而非 90%),每顆 Pod 常態有一倍餘裕。
2. **Node 級(overprovisioning pause Pod)**: 跑一組低 priorityClass 的佔位 Pod(pause image,requests 設實但什麼都不做)。平時佔住節點空間逼 Karpenter 多養一台;尖峰來時真 workload 排不下 → preemption(C-1)秒殺佔位者讓位 → 真 Pod 立刻有現成節點可上,同時佔位者 Pending 觸發 Karpenter 補新節點。等於把「生節點的 2 分鐘」預付掉了。

### priorityClass 保命線

尖峰極端時總有東西要犧牲,先用 priorityClass 寫好犧牲順序:核心交易鏈路(billing API、DB proxy)最高 → 一般服務 → batch/報表 → 佔位 Pod 最低(甚至負 priority)。沒寫的後果:preemption 隨機殺,可能殺掉你最不能死的(C-1 真實踩坑那條)。

### 動手:紙上演算(白板肌肉)

不動叢集,給學員一組數字自己算(面試現場就是這樣考):

> 服務常態 20 顆 Pod,每顆 requests.cpu 500m、常態用量 300m。node 是 4 vCPU(allocatable 約 3.5)。target CPU 60%。
> Q1: 常態需要幾台 node?(20*0.5 / 3.5 ≈ 3 台,留 daemonset 開銷算 4)
> Q2: 流量 3 倍,HPA 會把 replicas 推到多少?(currentMetric 300m/500m=60%,3 倍後 180% → ceil(20*180/60)=60 顆)
> Q3: 60 顆需要幾台 node?缺的節點誰補、要多久?這段時間誰在扛?
> [RUNTIME: 數字可換成學員公司 billing 平台的真實量級,他有 prod EKS 直覺]

### 誘答彈藥

1. 「requests 設小一點可以塞更多 Pod 省成本,反正尖峰時有 limits 可以爆。」
   (錯。requests 壓低 = 對 scheduler 謊報,node 實際超載,尖峰時全體 CPU throttle、memory 一撞就 OOM,而且 Burstable 在驅逐序前排。省的是帳面,付的是可用性。)
2. 「我們有 HPA + Karpenter 雙層自動化,所以不需要 headroom,那是浪費錢。」
   (錯,gate 級誘答。兩層都是分鐘級反應,秒級突刺只有站著的容量接得住。headroom 不是浪費,是結構性延遲的保險費。學員答這題要能把延遲帳單背出來。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 老闆:「雲帳單砍 30%,但月底出帳尖峰不准出事。」(billing 平台的真實張力) |
| **生產怎麼做** | 用數據談判:Prometheus 實際用量 → rightsize requests(VPA 建議模式,C-4)回收虛胖;非核心 batch 降 priority 擠進碎片時段;spot 跑無狀態;headroom 只保核心鏈路,以 priorityClass 分層而不是全叢集齊頭式。成本和韌性不是對立,是「把保險費花在刀口上」 |
| **真實踩坑** | 齊頭式砍 requests 20% 之後帳單真的降了,兩週後大促,node 超載、Burstable 大片被驅逐、雪崩。復盤發現砍掉的正是 headroom。財務看得到帳單,看不到沒發生的事故,這是 capacity planning 永遠的政治面 |
| **面試怎麼問** | 「Design for a 10x flash-sale spike on EKS. Walk me through pod-level, cluster-level, and process-level decisions, and what you monitor to know it works.」 |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| headroom | /ˈhed.ruːm/ | Pre-paid idle capacity that absorbs load faster than any autoscaler can react | 用常態成本預付「自動化來不及」的結構性延遲 |
| overcommit | /ˌoʊ.vər.kəˈmɪt/ | Scheduling more total limits than the node physically has, betting Pods don't peak together | 賭大家不同時用滿;CPU 可賭(throttle),memory 賭輸即 OOM |

---

## Chaos Drill Hooks(P3 特色:大型演練)

> 完整劇本歸 `references/chaos-drills.md` 的 P3 Drills 段。這裡是鉤子 + 劇本概要。
> **P3 與前面 phase 的差異**:前面的 drill 是單點故障;P3 是「複合場景 + 限時 + 產出 runbook」。
> **每個 drill 做完,學員要親手寫一份 runbook 進 `portfolio/runbooks/`**(格式:症狀 → 排查決策樹 → 止血 → 根因 → 治本 → 預防)。這是第一個夠格進 public repo 的主秀 artifact,面試可以直接秀。
> [RUNTIME: 四個 drill 不必全做,依學員弱點挑 2 個以上;P3-2 建議必做(對準 gate)]

- **P3-1 節點消失**(`docker stop` 一台 worker):考 node NotReady → NoExecute taint → Pod 驅逐重建的全鏈時間軸,和 topologySpread 有沒有真的買到可用性。對接 C-1/C-2。
- **P3-2 流量暴增**(load-gen 打到 HPA max 也不夠 + node 塞滿):考延遲帳單的現場辨認、Pending 排障(describe 讀 Filter 訊息)、以及「當下止血 vs 事後治本」的分層答案。對接 C-3/C-5/C-7。學員前科:先跳結論不講機制、治標治本要追問才補,這個 drill 明確要求 runbook 裡兩者分欄寫。
- **P3-3 OOM 雪崩**(一顆 memory leak Pod 沒設 limits 吃垮 node → node 級驅逐連鎖):考 P1 QoS 驅逐序的實戰版 + priorityClass 有無的差異。對接 C-7、回扣 P1 chunk 5。
- **P3-4 滾更出包 + PDB 卡 drain**(壞 image rolling update 卡住,同時平台要 drain node):兩個機制互鎖的複合故障,考 rollback(P1)+ PDB 三解法的代價判斷 + preStop race 的解釋。對接 C-6。

---

## P3 結束:30 分鐘迷你 Mock 劇本

> 教練扮面試官。P3 檔位:面試官問題用英文問,學員答英中混合皆可,答英文就給 English Polish。
> [RUNTIME: 依 mistake-registry 把學員 P3 期間掛過的點改編進追問]

**題目**: "Your team runs a billing API on EKS. Marketing launches a campaign and traffic will spike 10x for about 20 minutes, twice a day, starting next week. Design for it."

| 時間 | 段落 | 教練動作 | Pass 訊號 |
|------|------|---------|----------|
| 0-4 min | Requirements | 等他先問澄清問題(現在幾副本?尖峰可預測嗎?掉請求的代價?) | 不先跳解法,先問需求(打他「先跳結論」前科) |
| 4-14 min | 白板骨架 | 讓他畫 C-7 的時間尺度分層圖 | headroom/HPA/Karpenter 三層 + 各自反應時間量級正確 |
| 14-20 min | Deep dive | 挑兩層追問機制:「HPA 公式手算一題」「preStop sleep 在防什麼 race」 | 公式算對;race 講到 iptables 傳播,不是「給 app 時間」的模糊版 |
| 20-26 min | 誘答壓力測 | 丟一題 C-7 誘答(如「有雙層自動化就不需要 headroom」)看他敢不敢反駁 | 明確說「不對」並給延遲帳單論證(反脆弱訓練:不被面試官帶走) |
| 26-30 min | 收尾 | "Summarize your design in 60 seconds, in English." | 英文摘要點到三層 + 護欄,術語用對 |

---

## P3 畢業 Gate

**條件**: 白板(不看筆記)完成上面 mock 的完整設計題,並通過機制追問。

**考核格式**: 「10x 流量尖峰的部署設計」總合題 + 任兩個 chunk 的機制下鑽 + 一題誘答反駁。

**Pass 條件**:
- 說出時間尺度分層:headroom(秒級)/ HPA(分鐘級)/ node autoscaler(數分鐘級),並解釋為什麼每層的延遲是結構性的
- HPA 公式手算正確,說得出 metrics 資料鏈至少三棒(cAdvisor → metrics-server → HPA controller)
- 講清楚 Pod 終止的 race:Endpoints/iptables 傳播 vs SIGTERM,preStop sleep 和 grace period 的分工
- PDB 與 rolling update 參數的分界(誰管自願中斷、誰管更新節奏)
- scheduler 的收手邊界(Bind 寫完 nodeName 即止,kubelet 接棒):P0 舊傷必考
- 至少一題誘答當場抓出並講出為什麼錯

**Stretch(加分,不強求)**:
- 用控制理論詞彙描述 HPA(dead time / feedback / low-pass filter)
- 說出 Karpenter bin-packing 與 CA node group 的抽象層差異
- overprovisioning pause Pod + preemption 的組合拳完整講一遍

**Gate 失敗處理**: 見 SKILL.md Phase Gate Failure 協議。常見弱點預測:把「延遲」和「緩衝」混為一談(C-3 誘答 2)、preStop 講成「給 app 時間」的模糊版(C-6 誘答 2)。對症重練該 chunk,一週後冷測。

---

## Portfolio 整合(P3:第一批 public repo 主秀)

過價值門檻的 artifact(這個 phase 開始有面試能直接秀的東西):

1. **`portfolio/runbooks/`**: chaos drill 產出的 runbook,至少 2 份(P3-2 必含)。格式:症狀 → 決策樹 → 止血 → 根因 → 治本 → 預防。這是 SRE 面試的硬通貨,主秀 artifact。
2. **`portfolio/notes/p3-spike-design.md`**: C-7 的時間尺度分層圖 + 延遲帳單,學員自己畫自己寫(白板肌肉的存檔)。
3. **`portfolio/manifests/`**: hpa-demo.yaml、pdb-demo.yaml(含 preStop 對照組)。lab 副產品,過門檻但不是主秀。

不進 repo:C-1/C-2 的觀察型 lab 產物(taint-demo 等,太基礎,本機筆記即可)。

---

## P3 英文 Ramp

本 phase 檔位:First-Principles Dive 段落已直接用英文寫。教學時的用法:

- 讓學員先自己讀英文段,再用中文複述給教練聽(reading comprehension + 概念雙重驗收)。
- Say-it-in-English 抽考句(挑學員答得順的時機輕推,不硬逼,尊重他 2026-07-01 明說的中文為主偏好):
  - "The scheduler's job ends at Bind: it writes nodeName and never talks to kubelet."
  - "Tolerations permit, they don't attract. Attraction is node affinity's job."
  - "HPA has structural delay: metrics lag plus pod startup. Headroom absorbs what autoscaling can't."
  - "The preStop sleep keeps the Pod serving until every node's iptables has dropped it."
  - "Requests are the scheduling currency; lying to the scheduler means paying at peak time."
- mock 收尾的 60 秒英文摘要是本 phase 英文驗收的主戰場。

本 phase 術語卡總表(同步進 term-registry.md 做間隔抽考):

| Chunk | 術語 |
|-------|------|
| C-1 | preemption, backoff |
| C-2 | taint, topology spread |
| C-3 | stabilization window, cAdvisor, flapping |
| C-5 | bin packing, consolidation |
| C-6 | eviction, connection draining |
| C-7 | headroom, overcommit |

共 12 張,全部過「senior 面試會考或錨定底層機制」門檻(C-4 零卡:VPA 是工具名,in-place resize 的機制錨點已由 cgroup/incompressible 舊卡覆蓋)。
