# P6 面試衝刺: Interview Sprint 編排手冊

> **如何使用此檔:** 本檔性質和 P0-P5 不同:它不是概念教材,是「衝刺期的編排手冊」。
> P6 不教新知識(全 phase 零新術語卡)。所有 k8s 知識已凍結在 P0-P5 各 phase 檔,
> 這裡教的是怎麼把它們組裝成 45 分鐘的面試表現。
> 不要逐字唸稿:run sheet 是骨架,情境參數、追問深度、給不給臺階,依學員當場表現調。
> 題庫本體在 `references/interview-bank.md`,本檔只用題目 ID 對接,不重複收錄題目。
> 依 SKILL.md English Ramp 檔位:mock 劇本與 behavioral 全英文,編排說明用中文。

---

## P6 學習藍圖

**目標**: 通過大廠 senior DevOps/SRE 面試 loop。不是「知道更多」,是「在壓力下把已知的講成 senior 訊號」。

**P6 中心問題**: 同一份知識,mid-level 和 senior 的講法差在哪裡?

一句話版答案(貫穿全 phase,每次 mock 都用它復盤):senior 訊號 = 先框問題再動手、每個判斷都講機制、主動分治標與治本、被錯誤方向帶不走。這四條正好對著學員的四個歷史弱點模式打(見各 chunk 的客製 hook)。

**Chunk map**:

| Chunk | 主題 | 產出 |
|-------|------|------|
| C-1 | 衝刺編排(4-6 週節奏與配比) | 個人化 mock 課表 |
| C-2 | SRE incident scenario mock(keystone) | 2+ 場全英文 45min mock 過關 |
| C-3 | k8s × System Design 交集 | 3-4 題 SD 題能用 k8s 知識入場 |
| C-4 | Behavioral story bank 提煉(keystone) | 2-3 則 STAR 故事 drilled |
| C-5 | CKA/CKAD 限時副線 | 手速達標(明確標注:副線) |
| C-6 | English Polish 密集模式 | 全英文 mock 不降級 |

**前置條件**: P0-P5 各 phase Gate 已過。若有 phase 未畢業就進 P6,先回去補,衝刺期補概念是最貴的補法。

---

## C-1: 衝刺編排(倒數 4-6 週)

### 節奏骨架

以「一週三次 session、每次 60-90 分鐘」為預設密度。學員在職,低於這個密度肌肉長不出來,高於它會擠掉白天工作後的恢復。

| 週次 | 主軸 | 配比(scenario / SD / behavioral / CKA) |
|------|------|------------------------------------------|
| W1 | 摸底:每種 round 各打一場,建立 baseline | 40% / 20% / 20% / 20% |
| W2-W3 | 對弱項加壓:baseline 最紅的 round 佔一半 | [RUNTIME: 依 W1 摸底結果分配] |
| W4-W5 | 全 loop 模擬:一天連打 scenario + SD + behavioral,練體力與切換 | 35% / 30% / 25% / 10% |
| 最後一週 | 只復盤不加新 mock,掃 mistake-registry 殘留紅字,睡飽 | 復盤為主 |

`[RUNTIME: 依當時投遞狀態與目標公司清單客製]`:有確定 onsite 日期的公司,把該公司已知的 loop 結構(幾輪 scenario、有沒有 coding、SD 深度)反推回課表;沒有明確目標時照上表跑。

### 題庫對接(不重複收錄,用 ID)

| Round 類型 | interview-bank 分類 | 用法 |
|-----------|--------------------|------|
| 原理快問快答 | `Q-P-*` | 寄生在每次 session 的 A 段,抽 2 題冷測,英文作答 |
| scenario 排障 | `Q-T-*` + 本檔 C-2 run sheet | Q-T 當單題暖身,run sheet 當完整 45min 主菜 |
| system design | `Q-SD-*` + 本檔 C-3 | Q-SD 是切片題,C-3 是完整開放題 |
| CKA/CKAD | `Q-CKA-*` | 只在 C-5 副線時段用,不佔主線 |

`[RUNTIME: 屆時掃 interview-bank 全量。P2b-P5 教材建檔時會往題庫補題,P6 開跑前先盤點各分類存量,缺的當場補進題庫再用]`

### 客製 hook(學員歷史弱點 → 訓練配重)

- **盲講漏中間棒次**(Weekly Review #1 漏 scheduler):每場 mock 的 recap 段強制用固定骨架默數(控制流=五棒、封包=DNS→DNAT→回程三段)。骨架是他自己在 session 10 認可的解法,直接沿用。
- **先跳結論不講機制/治標治本**(session 4-6 連三堂同一條):C-2 rubric 把「未被追問就主動講 mitigation vs root fix」設為 senior 訊號硬條件。
- **被錯誤方向帶走**(memory: led-along-despite-doubt):每場 scenario mock 至少埋一次「面試官/隊友給錯誤引導」,見 C-2 追問樹的 planted-wrong-lead 節點。
- **用詞精準度**:English Polish 密集模式(C-6)全程開。
- `[RUNTIME: 開跑前掃 mistake-registry 所有未解 ❌ 與 🟡,直接變成 W1 摸底的出題來源]`

---

## C-2: SRE Incident Mock Run Sheets(keystone)

> 編排說明(中文):以下兩份 run sheet 全英文,對應真實 onsite 的 troubleshooting round。
> 母題取自學員親手做過的故障(P2a 網路、P1/P3 資源與擴縮),他有實體肌肉記憶,
> 衝刺期的任務是把肌肉記憶翻譯成英文口頭表現。
> 教練扮演面試官,嚴格照 expected behavior loop 推進;學員跳步就用追問拉回。
> 每層追問都標了 senior vs mid-level 訊號,復盤時逐層對照。
> 情境參數(服務名、版本、流量數字)每次換,防背稿。`[RUNTIME: 參數用學員當時 portfolio 裡的真實 manifest 改編]`

### Expected behavior loop(兩份 run sheet 共用)

```
clarify → hypothesize → verify → mitigate → root cause → prevent
   |          |            |         |           |          |
 blast     ranked      cheapest   stop the    mechanism   make it
 radius    by prior    check      bleeding    level       not recur
```

面試官的推進原則:學員每完成一步才餵下一塊資訊。學員跳步(最常見:聽完症狀直接報修法)就問 "Before we fix anything, what do you want to know first?" 拉回 clarify。

### Run Sheet A: Intermittent timeouts to an internal service(母題:P2a Service/kube-proxy/conntrack)

**Interviewer opening (read as-is):**

"Thanks for joining. This round is a production incident walkthrough. I'll play the on-call context: you can ask me anything you'd normally get from dashboards, logs, or teammates, and I'll tell you what you see. There's no trick; I want to watch how you think. Ready?

Here's the page: it's 14:20 on a weekday. The checkout team reports that calls from `checkout-api` to `payment-svc` (a ClusterIP service, 6 pods behind it) are failing intermittently. Roughly 1 in 10 new requests times out. It started about 30 minutes ago. No deploys today. Where do you want to start?"

**Facts the interviewer holds back until asked (drip-feed):**

- Existing long-lived connections are fine; only NEW connections fail. (Give only if the student asks "new vs existing connections?" or runs a repro test.)
- `kubectl get endpoints payment-svc` shows all 6 pod IPs. Probes green, RESTARTS 0.
- DNS resolves fine: `nslookup payment-svc` from an affected pod returns the ClusterIP instantly, every time.
- A batch job started ~40 min ago on the same nodes, opening thousands of short-lived outbound connections.
- `dmesg` on affected nodes: `nf_conntrack: table full, dropping packet`.
- `/proc/sys/net/netfilter/nf_conntrack_count` is at `nf_conntrack_max`.

**Root cause:** conntrack table exhaustion caused by the batch job. New connections get dropped at the netfilter layer; established flows keep working because their entries already exist.

**Planted wrong lead (mandatory, fires at layer 2):**

"One of your teammates on the call says: 'It's probably DNS being flaky again. Let's just restart CoreDNS.' Do you go with that?"

- **Senior signal:** refuses politely with a cheap discriminating test: "Let's verify first: run `nslookup` with the FQDN from an affected pod. If resolution succeeds consistently, DNS is not our layer and restarting CoreDNS just adds noise to the incident." Names the layer split: DNS resolution layer vs connection/NAT layer.
- **Mid-level signal:** goes along with the restart, or refuses without a test ("I don't think it's DNS" with no evidence).
- 客製 hook:這一節點直接復刻學員 session 11 的 busybox NXDOMAIN 坑(當時他把 conntrack 誤拉進 DNS 題=層級混淆,拆解後守住「先用 FQDN 測、測得到就別重啟 CoreDNS」)。他修好過一次,這裡驗證修得牢不牢。

**Follow-up tree (each layer: what to ask, senior vs mid signals):**

1. **Clarify.** Expected questions: blast radius (one service or many?), what changed (deploys? jobs? traffic?), new vs existing connections, error type (timeout vs connection refused vs 5xx).
   - Senior: asks "what changed in the last hour" even after hearing "no deploys" (deploys are not the only change; cron jobs, traffic shifts, node events count).
   - Mid: jumps straight to `kubectl get pods`.
2. **Hypothesize.** Expected: a ranked list across layers: app (pods unhealthy?) / service plumbing (endpoints, kube-proxy rules) / DNS / kernel-netfilter (conntrack) / node network.
   - Senior: says out loud which hypothesis is cheapest to falsify and starts there.
   - Mid: one hypothesis at a time, no ranking, no stated reason for the order.
3. **Verify.** The discriminating observations: endpoints full, probes green, DNS resolves → "the k8s object layer looks healthy, so I move below kubectl's visibility."
   - Senior: explicitly states "conntrack and iptables live in the node kernel; `kubectl` will never show them. I need `dmesg`, `conntrack -L`, or `/proc/sys/net/netfilter/nf_conntrack_count` vs `_max` on the node." (學員 session 9 的原坑:當時誤答 `kubectl get conntrack`。這句能不能自己講出來,是本 run sheet 的核心檢查點。)
   - Senior: predicts the symptom signature before checking: "table full drops NEW connections; established flows keep flowing since their entries exist. That matches 1-in-10 new-request timeouts." (session 11 精度掉的點:新 vs 舊連線誰遭殃,這裡冷測。)
   - Mid: keeps cycling `kubectl describe` / restarting pods when all objects are green.
4. **Mitigate.** Expected: stop the bleeding first: throttle or evict the batch job, and/or raise `nf_conntrack_max` as a temporary relief valve. States clearly this is a stopgap.
   - Senior: separates unprompted: "Raising the max is treating the symptom. The fix is capping the batch job's connection behavior (reuse connections, limit concurrency) or isolating it to dedicated nodes."
   - Mid: raises the sysctl and declares victory.
5. **Root cause narration.** One clean paragraph: packet path DNS → DNAT (kube-proxy-written iptables rules, rewritten on the source node, decentralized, no central hop through the ClusterIP) → conntrack records the rewrite so return traffic can be un-NATted → table full means the kernel cannot record new flows → drops.
   - Senior: the "no packet ever visits the ClusterIP" framing comes out naturally. (謎題B 三度封印檢查:P6 若再說出 "the packet first goes to the ClusterIP to get the real IP" 一律當場打斷重講。)
6. **Prevent.** Node-level alerting on `nf_conntrack_count / nf_conntrack_max` ratio, batch job resource/connection budgets, runbook entry.
   - Senior: mentions that this class of failure is invisible to k8s-native monitoring unless you export node kernel metrics (node-exporter conntrack collector).

**Scoring rubric (aligned to Tiered Scorecard P4+ dimensions):**

| Dimension | Senior bar for this run sheet |
|-----------|------------------------------|
| 能講清楚底層原理 | Explains conntrack's reason to exist (return-path un-NAT), not just its name |
| 理解內部機制 | DNAT on source node, decentralized; kernel layer vs k8s object layer split stated |
| 能用自己的話解釋 | Root cause narration is one coherent story, no memorized-list smell |
| 故障排除速度 (MTTR) | Reaches "below kubectl visibility" within ~3 information requests after objects check green; direction over speed |
| 可觀測性設計 | Prevent step includes a concrete metric + threshold, not "add monitoring" |
| 能定義/解讀 SLO | Quantifies impact early (error rate, affected fraction) and uses it to justify mitigation urgency |

Pass = 主維度 + 機制 + MTTR 三項達 senior bar,其餘至少 mid;planted-wrong-lead 節點必須用證據擋下,這項不達標整場直接判 retry。

---

### Run Sheet B: OOM cascade during month-end peak(母題:P1 QoS/OOM + P3 autoscaling)

**Interviewer opening (read as-is):**

"Same format as before. Here's the page: it's the last day of the month, 09:05, invoice-generation traffic is ramping. Pods of `billing-api` (a Deployment, 8 replicas) are restarting repeatedly. Customer-facing error rate is climbing past 2%. Your junior teammate already tried `kubectl rollout restart` and says 'it helped for five minutes'. Walk me through it."

**Facts held back until asked:**

- `kubectl get pods`: several pods with RESTARTS 3-6, STATUS cycling Running → OOMKilled → CrashLoopBackOff.
- `kubectl describe pod`: Last State: Terminated, Reason: OOMKilled, Exit Code: 137. Limits: memory 512Mi, requests 256Mi (Burstable).
- Node memory has plenty of headroom. (Discriminator: container-level OOM, not node-pressure eviction.)
- HPA exists but targets CPU at 70%; CPU is at 40%. Memory is the constraint, so HPA never fires.
- `kubectl top pod` history (via Prometheus): memory is a sawtooth that climbs to the limit over ~40 min under load, resets on restart, climbs again.
- Last deploy: 3 days ago, added an in-memory cache for invoice templates with no size bound.

**Root cause:** unbounded in-memory cache = memory leak pattern under peak load; container hits its own cgroup limit → kernel OOM-kills it (137 = 128+9, SIGKILL). HPA is blind to the constrained resource.

**Planted wrong lead (mandatory):**

"Your teammate says: 'Memory limit is clearly too small. Let's bump it to 2Gi and move on; we can't afford downtime on month-end.'"

- **Senior signal:** accepts it ONLY as a time-boxed stopgap and says why it's not the fix: "Memory is incompressible. The kernel can't shrink bytes already allocated; its only reclaim tool is killing the process. If this is a leak, 2Gi just moves the crash 3 hours later, possibly into a worse window. Bump it now to survive the peak, but the sawtooth-climbing-to-the-limit graph tells me we're feeding a leak, not fixing undersizing." Distinguishes leak (sawtooth keeps climbing to any ceiling) vs undersized (plateaus below a correct ceiling).
- **Mid-level signal:** bumps the limit and closes the incident, or refuses the bump entirely and lets the error rate burn while hunting the leak (missing the mitigate-first instinct).
- 客製 hook:這題是學員的招牌故事反打。他半年前面 AWS 被 OOM 題打掉,P1 chunk 5 + Weekly Review #1 已把 incompressible 第一性原理打穿(「水龍頭流速 vs 水桶存量」是他自己推出來的)。P6 驗證:壓力下還講得出 "the kernel's only reclaim tool for anonymous memory is killing the process" 嗎?

**Follow-up tree:**

1. **Clarify.** Expected: exit code / restart reason, container-level vs node-level OOM, what changed (deploy 3 days ago!), why did rollout restart "help for 5 minutes".
   - Senior: immediately reads "helped for five minutes" as a diagnostic clue (state resets on restart → accumulation problem), not as a failed fix to ignore.
   - Mid: ignores the teammate's data point.
2. **Hypothesize.** Leak vs undersized vs node pressure vs noisy neighbor.
   - Senior: names the discriminators up front: exit 137 + node headroom = container cgroup limit; sawtooth shape decides leak vs undersized.
   - Mid: "maybe not enough memory" with no shape analysis.
3. **Verify.** `describe` for Reason/ExitCode, memory graph shape, `kubectl logs --previous` for the victim's last words, deploy history diff.
   - Senior: asks for the trend graph before touching anything; connects the 3-day-old cache change to the 40-min climb.
   - Follow-up: "Why didn't HPA save you?" Senior: HPA fires on its configured metric only; CPU at 40% means it stays flat while memory burns. Scaling out would ALSO not fix a per-pod leak, only slow it (more replicas = same climb per pod under partitioned load). Mid: "HPA should have scaled" with no metric reasoning.
4. **Mitigate.** Time-boxed limit bump + replica bump to survive the peak; feature-flag or rollback the cache change if flaggable.
   - Senior: quantifies the time box ("2Gi buys us roughly 3-4x the climb window; that covers the peak until 14:00, then we ship the bounded cache").
5. **Root cause narration.** cgroup memory limit → kernel OOM killer scoped to the container → SIGKILL → 137; QoS Burstable; incompressible vs compressible resources (CPU throttles, memory kills); unbounded cache as the leak source.
   - Senior: unprompted 治標/治本 split: bump = stopgap, bounded cache + rightsized limit from real usage percentiles = fix.(session 4-6 連三堂的同一條改進點,這裡是最終驗收。)
6. **Prevent.** Working-set alerts at ~80% of limit with slope detection, memory-based HPA or KEDA where appropriate, load test the month-end profile, cache size bound in code review checklist.
   - Follow-up: "Would you make this pod Guaranteed QoS?" Senior: explains eviction ordering (BestEffort → Burstable → Guaranteed) and the deposit/contract intuition, then notes Guaranteed doesn't prevent container-level OOM at its own limit; it only changes node-pressure eviction priority. (兩種 OOM 的邊界=P1 D 段 lab 親手做過:node 有餘量照樣 OOMKilled。)

**Scoring rubric:** 同 Run Sheet A 的六維表,替換 senior bar 內容:

| Dimension | Senior bar for this run sheet |
|-----------|------------------------------|
| 能講清楚底層原理 | Incompressible resource first principles; why kill is the kernel's only move |
| 理解內部機制 | Container cgroup OOM vs node-pressure eviction 邊界;HPA metric blindness |
| 能用自己的話解釋 | Leak vs undersized 用圖形形狀講,不是背名詞 |
| 故障排除速度 (MTTR) | Exit code + node headroom + graph shape 三步內鎖定 container-level leak |
| 可觀測性設計 | Slope-based working-set alert,講得出為什麼絕對值閾值不夠 |
| 能定義/解讀 SLO | 用 error rate 與 peak window 推導 mitigation 的 time box |

**Retry 規則(兩份 run sheet 共用):** 沒過的 run sheet 進 mistake-registry,3 天後換參數重打(服務名、數字、紅鯡魚全換),不重打原題防背稿。

`[RUNTIME: P3/P4 教材建檔後,從其 E 段 chaos drill 再長 1-2 份新母題 run sheet(候選:scheduling 資源碎片、observability 告警風暴),沿用本節骨架與六維 rubric]`

---

## C-3: k8s × System Design 交集(全英文題幹)

> 編排說明(中文):純 SD 基本功(estimation、CAP、queue、cache 通用理論)外包給 `sd-coach`,
> 這裡只練一個角度:「k8s 深度知識怎麼變成 SD 面試的入場籌碼」。
> 每題 25-35 分鐘,白板為主,學員先講 3 分鐘 high-level 再深入。
> 判準:能不能把 P0-P5 的機制詞翻譯成 SD 語言(reconcile loop → control loop / convergence;
> Endpoints → service discovery;kube-proxy 三合一對照表 → data plane vs control plane)。

### SD-1: Design a multi-tenant internal platform on Kubernetes

**Prompt (English, read as-is):** "Your company has 40 product teams sharing infrastructure. Design an internal platform on Kubernetes where teams self-serve deployments without stepping on each other. Cover isolation, fairness, and the developer-facing API."

- **期待的架構要素:** tenancy model 選型(namespace-per-team vs cluster-per-team vs virtual cluster,講 trade-off 不是背答案);isolation 三層拆開講:調度公平(ResourceQuota/LimitRange)、網路(NetworkPolicy,default-deny + 白名單)、權限(RBAC 邊界);developer API(平台是 CRD + controller?還是 CI 產 YAML?);noisy neighbor 治理(QoS class 當 SD 語言用:誰先死是設計出來的,不是運氣)。
- **k8s 知識 → SD 語言:** 「k8s namespace 不做隔離,是邏輯分組」(P1 學員自己問出的撞名點)在這題是入場第一刀:senior 開場就劃清 namespace 給你分組與配額邊界,真隔離要 NetworkPolicy + RBAC + (必要時) node pool 各自疊上去。Reconcile loop 變成平台語言:平台 API 收 desired state,controller 收斂,這就是 self-serve 不需要 ops 值班審批的理由。
- **追問方向:** "A tenant's batch job starves another tenant's latency-sensitive service on the same node. Walk me through the exact mechanisms that decide who suffers."(QoS + requests/limits + 驅逐序,P1 chunk 5 直譯);"Why not just give every team its own cluster?"(成本、版本治理、平台團隊人力,考 trade-off 成熟度);"How does a team get a new capability, say a Redis, without a ticket?"(CRD/operator 思路,接 P0 controller 概念的複利)。

### SD-2: Run stateful workloads reliably on Kubernetes

**Prompt:** "Your team wants to move PostgreSQL and Kafka from EC2 onto your EKS clusters. Argue for or against, and design the reliable version if you proceed."

- **期待的架構要素:** 先講 stateless assumption 哪裡破(Pod ephemeral、IP 會變、restart = 換人):這正是 P2a Service 存在理由的反面;StatefulSet 給的三件事(stable identity、ordered rollout、per-replica PVC)與它不給的事(不會幫你做 failover 決策,那是 operator 的活);storage 層(EBS zonal 特性 → 跨 AZ failover 時 volume 跟不跟得走);與 managed service (RDS/MSK) 的 trade-off,senior 答案允許結論是 "don't"。
- **k8s 知識 → SD 語言:** reconcile loop 在 stateful 世界的危險面:P0 教材的真實踩坑(node 網路抖動、controller 時間差造成兩份 Pod 同時跑)在這裡升級成 SD 級別的 split-brain 論述;「level-triggered 自癒」對 stateless 是禮物、對單寫者資料庫是上膛的槍,講得出這個反轉就是 senior。
- **追問方向:** "A node running your Postgres primary goes unreachable for 90 seconds. Trace what Kubernetes does by default, and where that default hurts you."(Node controller 時間差 + PDB + fencing);"Why does Kafka tolerate k8s better than Postgres?"(replication protocol 自帶共識 vs 單寫者,可回扣 etcd/Raft quorum 直覺);"What does the operator actually do that a StatefulSet can't?"(把 domain 知識寫成 controller=P0 reconcile 概念的第三次複利)。

### SD-3: Design the deploy system for 200 microservices

**Prompt:** "Design the deployment system for an org running 200 microservices on Kubernetes. Requirements: a bad deploy should never take down more than a sliver of traffic, and rollback must be near-instant."

- **期待的架構要素:** 這題就是把 P5 progressive delivery 翻譯成 SD 答案:GitOps 作為 source of truth(P0 聲明式的 SD 版:Git state → controller 收斂,kubectl edit 被蓋回是 feature 不是 bug);rollout 策略階梯(rolling → blue/green → canary)與各自的成本;canary 的裁判是誰(metrics-based analysis,不是人盯 dashboard);rollback 為什麼快(舊 RS scale up 不重拉 image,P1 chunk 4 原話直接用);blast radius 控制(maxUnavailable、PDB、逐 cluster 推進波次)。
- **k8s 知識 → SD 語言:** maxSurge/maxUnavailable 從 YAML 欄位升格成 SD 語言的「可用性 vs 成本的兩顆旋鈕」;「驗證邊界」金句(schema 錯 API Server 當場擋,image 在不在只有 kubelet 拉了才知道)變成 deploy pipeline 的分層驗證論述:每一層盡早擋掉它能擋的錯。
- **追問方向:** "Your canary looks healthy but the full rollout melts down. What signals did the canary miss?"(流量形狀、cache 冷熱、規模效應);"Where does the human sit in this system?"(approval gate 放哪層、什麼情況自動 rollback);"200 services share this pipeline; one team's flaky metrics keep auto-rolling-back good deploys. Fix the system, not the team."(平台治理題,考 senior 的系統觀)。
- `[RUNTIME: 本題深度依 P5 實際完成度調整;若 P5 的 Argo Rollouts lab 有 portfolio artifact,面試練習時要求學員直接引用自己的 repo 當論據]`

### SD-4: Multi-region failover for the billing platform

**Prompt:** "Your billing platform runs in one AWS region on EKS. Design multi-region failover. Be explicit about what fails over automatically, what needs a human, and what data you're willing to lose."

- **期待的架構要素:** 先定 RTO/RPO 再畫圖(數字先於架構=senior 開場);分層 failover:DNS/global LB 層(health check 驅動)、無狀態層(兩邊常駐 vs 冷啟)、資料層(sync vs async replication 的 RPO 代價);k8s 的角色邊界要講清:cluster 是 region 內的自癒單位,跨 region 沒有神奇的 k8s 開關,是流量層 + 資料層的工程;控制面依賴盤點(image registry、CI、secrets 在 DR region 可不可用)。
- **k8s 知識 → SD 語言:** reconcile/level-triggered 的適用邊界再現:region 內 node 掛了 k8s 自己收斂,region 掛了收斂無從發生,「自癒的前提是 control plane 活著」這句話就是 P0 知識的 SD 天花板應用;etcd quorum 直覺遷移到「為什麼不能把一個 stretched cluster 橫跨兩個 region」(延遲打爆 leader election,P0 C-4 真實踩坑的放大版)。
- **追問方向:** "Why not one EKS cluster spanning regions?"(etcd/latency,見上);"During failover, a customer gets billed twice. Which layer failed?"(冪等性設計,回扣 P0 idempotency 第一性原理);"How do you TEST this without breaking prod?"(game day、依賴注入故障,接 chaos drill 的精神)。

---

## C-4: Behavioral Story Bank 提煉流程(keystone)

> 編排說明(中文):素材庫在 `k8s-coach-workspace/story-bank.md`。截至建檔日素材表為空,
> `[RUNTIME: P6 開跑第一堂,若 story bank 存量 < 5 則,先花 20 分鐘做「素材催收面談」:
> 順著他的 billing prod EKS 值班史問(半夜被 page 過嗎?推過什麼別人反對的改動?省過錢嗎?),
> 每挖到一件記一行 raw,再進提煉流程]`。已知可催收的種子:他半年前面 AWS 被 OOM 題打掉、
> 後來在本課程把 incompressible 原理打穿的完整弧線(成長型故事,適合 "biggest technical gap you closed")。

### 提煉 pipeline(每則素材走一遍)

```
raw 一行 → 門檻篩選 → STAR 英文化 → Action 回注原理 → mock 演練+追問 → status: drilled
```

**Step 1 篩選門檻(三佔二):** 衝突或壓力(半夜掛掉、期限、意見不合)/ 自己的判斷(不是照 runbook 走)/ 可量化結果(MTTR、成本、影響面)。流水帳不提煉,寧缺勿濫。

**Step 2 STAR 英文化:** Situation 兩句內講完 context(面試官不在乎你們的內部系統名);Task 一句,重點是 "my job specifically was...";Action 佔全故事 60%,全部用 "I" 不用 "we"(團隊貢獻可提,但你的那一刀要單獨成句);Result 帶數字,沒精確數字就給量級與比較基準。

**Step 3 Action 段回注底層原理(本課程對 behavioral 的複利,keystone 中的 keystone):** 當年的操作 + 現在的理解,兩層都講。範例形狀(英文示意,非範文):

> "At the time, my fix was bumping the memory limit, and it worked. What I understood later is WHY that was only a stopgap: memory is an incompressible resource; the kernel can't reclaim allocated bytes, so a leak will climb to any ceiling you set. The real fix was bounding the cache. Now when I size workloads I start from the working-set percentiles, not from the last crash."

這個「當年只會 X,現在能講出 X 底下的機制」結構,把 behavioral round 變成第二個技術訊號輸出口,senior 面試官對這個結構的辨識度極高。

**Step 4 mock 演練與追問:** behavioral 也有追問樹,常見三連:
- "So what would you do differently today?"(標準答案形狀:一個具體的技術或流程改變,不是 "communicate better" 這種空話)
- "What was the pushback and how did you handle it?"(考衝突處理的實感,答案要有對方的具體反對理由)
- "How did you know it worked?"(逼出量化驗證,答不出數字=故事白講)

### 常見 senior behavioral 題與好答案的形狀(不是範文,是結構)

**B-1: "Tell me about your worst production incident."**
好答案的形狀:症狀 → 你的第一個判斷(講出當下的 hypothesis ranking,哪怕排錯了)→ 轉折點(哪個觀察改變了方向)→ mitigation 與 root fix 分開講 → 事後改變了什麼系統性的東西(alert、runbook、架構),而不是「以後更小心」。地雷:把自己塑造成唯一英雄;沒有任何一步是錯的(太假);只有修復沒有預防。

**B-2: "Tell me about a time you disagreed with a teammate's technical direction."**
好答案的形狀:對方的方案先講到你自己都覺得有道理(steel-man)→ 你的疑慮是一個可驗證的具體點 → 你提議的 cheapest discriminating test → 結果(你對或你錯都行,你錯了的版本反而更 senior,重點是驗證行為本身)。
客製 hook:這題正對學員 memory [[led-along-despite-doubt]] 的職場弱點(覺得怪怪的但沒把握就被帶走)。C-2 run sheet 的 planted-wrong-lead 練的是當場行為,這題練的是把同一種行為講成故事。兩邊互相餵:mock 裡擋下錯誤引導的成功經驗,本身就能提煉成這題的素材。

**B-3: "Tell me about the biggest technical gap you've closed."**
好答案的形狀:承認 gap 的具體場景(被什麼問題打掉、什麼做不出來)→ 補洞的方法有結構(不是「我看了很多文件」,是「我從 kernel 層重學了資源模型,親手重現了 OOM」)→ 閉環證據(同類問題再來時的表現差異)。
客製 hook:學員的 AWS OOM 面試故事 + 本課程 P1 chunk 5 的弧線是這題的天然素材,Step 3 的範例形狀就是為它寫的。

---

## C-5: CKA/CKAD 限時副線

> **明確標注:這是副線。** 北極星是 senior 面試,不是證照。每週最多一個 30 分鐘時段,
> 主線(C-2/C-3/C-4)沒達標前不碰。證照的價值是逼手速與語法記憶,僅此而已。
> 對接題庫 `Q-CKA-*`(interview-bank),`[RUNTIME: P6 時掃題庫 CKA 分類存量,不足則補]`。

### 手速 drill 清單

環境鐵律不變:kind 叢集練,開打前 `kubectl config current-context` 確認是 `kind-k8s-coach-p0`(機器上有公司 PROD EKS kubeconfig)。

**Session 開頭 30 秒必做的環境設置:**

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
export now="--force --grace-period=0"
```

**Imperative 指令對照表(背到不用想):**

| 要生什麼 | 指令 |
|----------|------|
| Pod | `k run nginx --image=nginx $do > pod.yaml` |
| Deployment | `k create deployment web --image=nginx --replicas=3 $do > deploy.yaml` |
| Service (expose) | `k expose deployment web --port=80 --target-port=8080 $do > svc.yaml` |
| ConfigMap | `k create configmap app-config --from-literal=k=v $do > cm.yaml` |
| Secret | `k create secret generic db-pass --from-literal=pw=x $do > secret.yaml` |
| Job | `k create job backup --image=busybox $do > job.yaml -- /bin/sh -c "echo done"` |
| CronJob | `k create cronjob ping --image=busybox --schedule="*/5 * * * *" $do > cj.yaml -- /bin/sh -c "date"` |
| 快速刪 Pod | `k delete pod x $now` |
| 欄位語法查詢 | `k explain pod.spec.containers --recursive \| less`(比翻文件快) |
| 資源排序 | `k get pods -A --sort-by=.metadata.creationTimestamp` |

### 時間管理策略

- 每題先看配分:2 分題卡住 90 秒就 flag & skip,先掃完全卷再回頭。
- 考試給的 context 切換指令(每題開頭那行 `kubectl config use-context ...`)必須複製貼上執行,不手打。這是 current-context 肌肉記憶的考場版,學員 P0 就練過這條安全習慣,直接遷移。
- YAML 一律 `$do` 生成後改,零手寫。手寫 YAML 是這場考試最貴的浪費。
- 驗證習慣:每題收尾 `k get <resource>` 確認狀態再走,便宜的 3 秒保險。

---

## C-6: English Polish 密集模式

> 編排說明(中文):P6 的 mock 全英文,不降級。對齊 SKILL.md 的 English Polish 機制,
> 但從「學員用英文才觸發」升級為「每個回答都給」:mock 中即時只給一行潤飾,
> 復盤時才逐句對照。內容對錯仍走 rubric 判定,Polish 只管道地程度,兩者分開記。

### 運作規則

- Mock 進行中:學員每個完整回答後,教練夾一行 `💬 English Polish: "[native senior 版]"`,不打斷節奏、不講文法課。
- 復盤段:挑 3 個「意思對但講法洩底」的句子,並排原句 vs 潤飾版,讓學員朗讀潤飾版兩遍(口腔肌肉,不是眼睛)。
- 潤飾版優先用業界慣用詞:spin up、gets evicted、under memory pressure、blast radius、roll it back、page/get paged、post-mortem、stopgap。
- `[RUNTIME: 累積學員 mock 中的高頻錯誤,長出他個人的 top-10 修正清單,貼在每次 mock 開場複習 30 秒]`

### 常見中式英文修正清單(k8s 語境起手式)

| 學員容易講的 | Native senior 講法 |
|--------------|-------------------|
| control panel | control **plane**(session 7 已釘過,P6 抽查) |
| the pod is died / the pod is dead | the pod got killed / was OOMKilled / got evicted |
| the memory is full | the container hit its memory limit |
| k8s will help us to restart it | Kubernetes restarts it automatically / the kubelet restarts the container |
| I will check the log to find the reason | I'd start with the logs from the previous instance: `kubectl logs --previous` |
| the connection is not stable | requests are timing out intermittently / we're seeing intermittent connection failures |
| do a restart for the pod | bounce the pod / restart the deployment |
| the traffic will go to the ClusterIP first | the ClusterIP is virtual; the packet gets DNAT-ed on the source node(謎題B 的英文版守門) |
| open the port / open the firewall | allow the traffic in the NetworkPolicy / expose port 8080 on the service |
| this problem is because of... | the root cause is... / this traces back to... |
| we can make the limit bigger | we can raise the limit as a stopgap(順手把治標的定位講出來) |
| very serious problem | a Sev-1 / a customer-facing outage / high blast radius |

---

## Chaos Drill Hooks(P6)

P6 不出新 drill。C-2 run sheet 就是 chaos drill 的面試化形態:同一批母題(P2a 網路、P1 資源),從「親手弄壞親手修」升級為「口頭指揮 + 英文敘事」。需要重摸實體手感時,回收既有 drill ID(`references/chaos-drills.md` 的 P2a-*/P3-* 系列)在 kind 上重跑一次,再接 run sheet。`[RUNTIME: 依 mistake-registry 殘留紅字挑要重跑哪個 drill]`

---

## P6 畢業 Gate(= 課程總畢業)

**考核格式:** 一場完整 scenario mock(從 C-2 骨架選一份「沒打過的參數變體」,或 [RUNTIME] 新母題 run sheet),全英文 45 分鐘,教練全程面試官人格不出戲,不給臺階、不降級中文。

**Pass 條件(全部達成):**

- Run sheet 六維 rubric:主維度(底層原理)+ 內部機制 + MTTR 三項達 senior bar,其餘至少 mid。
- Planted-wrong-lead 節點用「便宜的驗證」擋下,不是硬拗也不是跟走。
- 未被追問就主動分治標/治本(這條是學員三個 session 的同一條改進點,Gate 不放水)。
- Behavioral:至少 2 則 story 達 `drilled`,現場抽 1 則講 + 吃 2 層追問不散架。
- SD:C-3 四題中抽 1 題,25 分鐘內講出「期待的架構要素」欄的多數要素,k8s 知識至少完成一次「YAML 欄位 → SD 語言」的升格。
- 全程英文,English Polish 需求密度明顯低於 W1 baseline(教練主觀判定,復盤時說明依據)。

**Stretch(加分,不強求):**

- 反問面試官一個高品質問題(考官視角:候選人會反問 blast radius 或 SLO 的,直接加分)。
- CKA 副線:一次 timed drill 全對(不影響 Gate 判定)。

**Gate 失敗處理:** 照 SKILL.md Phase Gate Failure 協議。P6 特有規則:失敗的維度直接映射回源頭 phase 檔(機制講不清 → 回對應 phase 的 C 段重打;英文散架 → C-6 加密 + `fsi-devops-english` 通勤加練;故事散架 → C-4 重提煉),修完 3 天後換參數重考,不重考原題。

---

## Portfolio 最終檢視(recruiter 視角)

> 編排說明:Gate 過了不是終點,repo 是履歷的一部分。用 recruiter/hiring manager 的眼睛走一遍
> `github.com/jasontsaicc/k8s-mastery-lab-skill` 的 `portfolio/`,90 秒內要能講出這個人 senior 在哪。

**檢視清單:**

- **60 秒測試:** README 開頭三行講清這個 repo 是什麼、最值得看的三個 artifact 是哪三個(直接放連結)。Recruiter 不會挖資料夾。
- **主秀排序:** showcase 級 artifact(observability dashboard、gitops、terraform-eks、run sheet 演練後的 postmortem 筆記)置頂;`[RUNTIME: 依 P3-P5 實際長出的 artifact 盤點,缺主秀就在 P6 前補,別讓 repo 只有概念筆記]`
- **踩坑筆記的定位:** `portfolio/notes/` 的錯誤紀錄是資產(「連錯誤都有價值」是學員自己的原話),但要有一篇 index 筆記把它們串成成長敘事,不是散裝。
- **一致性巡檢:** commit message 一行式全程遵守(學員全域規範);沒有半成品 manifest;每個 EKS 相關檔案帶 destroy 說明(專業訊號:這人不會留燒錢資源)。
- **面試引用演練:** 挑 2 個 artifact,練 30 秒英文介紹("In this repo I reproduced a conntrack exhaustion and wrote up the kernel-level root cause"),SD 與 behavioral round 都能引用。

---

## P6 英文 Ramp 段

P6 不加新術語卡(零張,本 phase 無新知識,這是設計不是遺漏)。英文工作全在 C-6 密集模式與全英文 mock 本體。Term Registry 既有到期卡照常在 A 段抽考,P6 期間全部用英文作答;衝刺結束前 registry 內不得有紅字。
