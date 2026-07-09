# 面試題庫

> **如何使用此檔:** 對應 Teaching Flow G 段(面試 Q&A,固定 5min,不可跳)。
> 每個 phase 結束前從這裡選題做 G 段模擬;P6 全力衝刺時密集使用。
> 題目標注「首見 phase」,G 段只用學員已學過的範圍。

---

## 題目分類

| 類別 | 說明 | 考察重點 |
|------|------|---------|
| **原理題** | 解釋機制、說清楚底層是什麼 | 能不能打穿到底層原理,不只是背 YAML 欄位 |
| **故障排除** | 給一個生產現象,問排查路徑和根因 | 排查思路的結構性(第一個指令是什麼,為什麼) |
| **k8s x system design** | k8s 機制和大系統設計的交集 | senior SRE 視角:能不能設計可靠的系統 |
| **CKA/CKAD 限時(副線)** | timed 操作題,手速 + 語法記憶 | P6 才密集練,前期不是重點 |
| **誘答庫** | 似是而非的完整說法,要學員抓錯並講清楚錯在哪一層 | 反脆弱:不被聽起來合理的錯誤說法帶走(學員真實職場弱點) |
| **Behavioral(Q-B-*)** | senior 面試 behavioral 題,英文題幹 | 敘事結構 + 判斷力,素材從 `workspaces/k8s/story-bank.md` 提煉 |

---

## 原理題

### Q-P-01: apply 到 Running 全流程(P0 核心 Gate 題)

**適用 phase**: P0+
**難度**: P0 畢業 Gate 必過

**題目**: 「從 `kubectl apply -f pod.yaml` 到 Pod 狀態顯示 Running,每一個參與的元件依序做了什麼?請盡可能詳細說明,包括 authn、authz、admission control 各是什麼時機,etcd 被寫了幾次,scheduler 怎麼選 node,kubelet 怎麼知道要啟動這個 Pod。」

**Pass 條件**:
- 點到所有元件: API server、etcd、scheduler、kubelet、CRI
- 正確描述 API server 三道關卡順序(authn → authz → admission)
- 說清楚 scheduler 是 watch 到 unscheduled pod 才動,不是被呼叫
- 說清楚 kubelet 也是 watch,不是輪詢
- 知道 etcd 被寫兩次(Pod 物件 + scheduler 填 nodeName)

**Stretch(加分不強求)**:
- 說出 level-triggered reconcile 在哪裡體現
- 說出 Raft quorum 為什麼讓 etcd 成為可靠的 source of truth

**Coach 引導方向**: 學員卡在某段時,問「那這個元件是怎麼知道有事情要做的?它是被叫,還是自己發現的?」

---

### Q-P-02: 宣告式 vs 命令式在 failure recovery 的差異

**適用 phase**: P0+
**難度**: P0 基礎題

**題目**: 「解釋 Kubernetes 為什麼選擇宣告式 API。命令式和宣告式在 failure recovery 上有什麼核心差異?」

**Pass 條件**:
- 能說出「宣告式 = 說目標態,系統自己搞定」
- 能說出「冪等性(idempotency)」的概念
- 能說出「reconcile loop 讓系統自癒」這個機制

**Stretch**: 能連到控制理論(setpoint + feedback loop)

---

### Q-P-03: etcd 和 Raft

**適用 phase**: P0+
**難度**: P0 基礎題

**題目**: 「etcd 在 Kubernetes 中扮演什麼角色?它用什麼機制保證高可用?為什麼 etcd 節點數一定要是奇數?」

**Pass 條件**:
- 說出 etcd 是 source of truth,所有 k8s 物件存在這裡
- 說出 Raft 讓多個節點保持一致
- 說出 quorum = 多數決,奇數節點才能有明確多數

**Stretch**: 「2 個 etcd 節點為什麼比 1 個還差?」(quorum = 2,任一個掛就停擺,相當於沒有容錯)

---

### Q-P-04: static pod 的設計哲學

**適用 phase**: P0+
**難度**: P0 進階題(Stretch)

**題目**: 「為什麼 Kubernetes control plane 的元件(api-server、etcd、scheduler、controller-manager)要用 static pod 的形式跑,而不是用 Deployment?」

**Pass 條件**:
- 指出「雞生蛋」問題: 如果用 Deployment 管 controller,controller 掛了誰來管 Deployment?
- 說出 static pod 由 kubelet 直接讀 manifest 啟動,不需要 API server 存活

---

### Q-P-05: 容器和 VM 的本質差異

**適用 phase**: P0/P1+
**難度**: P0/P1 基礎題

**題目**: 「容器和 VM 的隔離機制有什麼本質差別?Kubernetes 的 resource limits(CPU/memory)在 Linux 底層對應什麼機制?」

**Pass 條件**:
- 說出容器共用 host kernel,用 namespace(隔離視角)+ cgroup(限制資源)
- VM 用 hypervisor 做硬體虛擬化,kernel 完全隔離
- resource limits 對應 cgroup 的 `memory.limit_in_bytes` 和 `cpu.cfs_quota_us`

---

> **Why-chain 追問樹說明(Q-P-06 起)**: 每題附面試官往下追問的 2-3 層。每層標注 mid-level 常見的答法(在這層背不動)和 senior 訊號(答出什麼代表打穿了)。Coach 用法: 學員答完表層就往下一層追,追到他卡住的那層,那層就是下次 C 段要補的洞。[RUNTIME: 追問深度依學員當下狀態調整,連卡兩層就收手,回 phase 檔重打]

### Q-P-06: node 有餘量還是 OOMKilled(P1 翻身題)

**適用 phase**: P1+
**難度**: P1 核心題(學員曾在 AWS 面試被 OOM 考倒,session 5 打穿,這是他的翻身題)

**題目**: 「一個 Pod 被 OOMKilled,但 `kubectl top node` 顯示這台 node 還有 4GB 空閒記憶體。解釋為什麼會這樣,以及 QoS 分級在什麼時候才會介入。」

**Why-chain 追問樹**:
- **L1**: 為什麼 node 有餘量還會 OOM?
  - mid 常答「記憶體不夠了」(不夠: 沒分清是誰的記憶體不夠)
  - senior 訊號: 容器級 OOM 是撞自己的 cgroup memory limit,kernel OOM killer 在 cgroup 範圍內動手,和 node 剩多少完全無關
- **L2**: 為什麼 memory 撞 limit 是被殺,CPU 撞 limit 只是變慢?
  - mid 常背「CPU 可壓縮、memory 不可壓縮」但講不出為什麼(這層背不動)
  - senior 訊號: CPU 是流速,少給幾個 cycle 程式只是慢;memory 是已經佔住的位元組,kernel 沒辦法沒收一半,唯一回收手段就是殺掉整個 process,所以是 SIGKILL、exit 137(128+9)
- **L3**: 那 QoS 什麼時候上場?
  - senior 訊號: QoS 管的是另一套機制,node 級 memory pressure 時 kubelet eviction 按 BestEffort → Burstable → Guaranteed 順序驅逐。兩種 OOM 是兩套獨立機制: kernel cgroup OOM killer(容器撞自己天花板)vs kubelet eviction(node 自保)

**客製 hook**: 學員 session 5 親手做過 oom-demo lab(stress 要 150M / limit 100Mi,node 仍有餘量),session 10 Weekly Review 用「水龍頭流速 vs 水桶存量」自己推出第一性原理。冷測先讓他講,卡在 L2 才回扣比喻。

---

### Q-P-07: 三種 probe 的語義與反噬

**適用 phase**: P1+
**難度**: P1 核心題

**題目**: 「liveness、readiness、startup probe 各自 fail 的後果是什麼?什麼情境下 liveness probe 反而會把整個系統搞垮?」

**Why-chain 追問樹**:
- **L1**: fail 的後果分別是什麼?
  - mid 常把 liveness/readiness 對調,或答「都會重啟」(這層背不動的比例意外地高)
  - senior 訊號: readiness fail = 從 Endpoints 摘除、不接流量、RESTARTS 不動;liveness fail = kill + restart、RESTARTS +1;startup fail = 還在寬限期,壓住另外兩種 probe
- **L2**: 誰在執行 probe?誰把 Pod 從 Endpoints 摘掉?
  - mid 答「k8s 會處理」(演員全省略)
  - senior 訊號: kubelet 在 Pod 所在 node 上打 probe、更新 Pod ready condition;endpoint controller watch 到 condition 變化,更新 EndpointSlice。兩個演員,兩棒
- **L3**: liveness 搞垮系統的情境?
  - senior 訊號: liveness 去檢查外部依賴(例如 DB)。DB 一慢,所有 Pod 同時 probe fail、同時被重啟,重啟後同時重連 DB,thundering herd 反過來把 DB 壓死,正回饋雪崩。所以 liveness 只該檢查「我自己還活著」

**客製 hook**: 回扣學員 P1 probe lab(rm readiness 後 Pod 從 Endpoints 消失但 RESTARTS 0)+ session 6 畢業 gate 的 web-frontend(probe 殺健康 app,他從 exit 0 反推)。L3 的 thundering herd 是他自己講出過的詞,可要求英文重講一次。

---

### Q-P-08: rolling update 卡死幾何

**適用 phase**: P1+
**難度**: P1 進階題

**題目**: 「replicas=4、maxSurge=1、maxUnavailable=1 的 Deployment 開始 rolling update,新版 image 拉不下來。此刻叢集上會停在幾個舊 Pod、幾個壞 Pod?為什麼 rollback 會很快?」

**Why-chain 追問樹**:
- **L1**: 卡死時的幾何?
  - mid 常亂猜或答「全部卡住」(算不出來 = 只背過參數名)
  - senior 訊號: 用兩條約束推,總數上限 4+1=5、可用下限 4-1=3,所以停在 3 舊(可用)+ 2 新(ImagePullBackOff),不會再前進也不會再殺舊的
- **L2**: 為什麼 rollback 快?
  - mid 答「k8s 有歷史紀錄」(對但沒打穿)
  - senior 訊號: 舊 ReplicaSet 一直留著(scale 到 0 不是刪掉),rollback 只是把舊 RS scale 回來;image 還在 node 上,不用重拉。翹翹板倒回去而已
- **L3**: 為什麼 API Server 不在 apply 時就擋下壞 image?
  - senior 訊號: 驗證邊界。schema 錯 admission 當場退件;但「image 存不存在」是外部世界的事實,只有 kubelet 第五棒真的去拉才知道。宣告式系統只能驗證格式,不能驗證現實

**客製 hook**: 學員 session 4 lab 親手做出過 3 好 + 2 壞;「驗證邊界」金句是他學過的原話。可換參數冷測(replicas=6、maxSurge=2)。

---

### Q-P-09: ClusterIP 封包之旅(P2a 核心 Gate 題)

**適用 phase**: P2a+
**難度**: P2a 畢業 Gate 必過

**題目**: 「Pod 打某個 Service 的 ClusterIP,這個封包實際上經歷了什麼?ClusterIP 到底是哪台機器的 IP?」

**Why-chain 追問樹**:
- **L1**: kube-proxy 做什麼?
  - mid 常答「轉發封包」(= 錯,這層就分出高下)
  - senior 訊號: kube-proxy 只寫 iptables 規則,搬封包的是 kernel(netfilter)。kube-proxy 掛掉,既有規則照常工作,新 Service 才不會生效
- **L2**: 封包在哪裡被改寫?
  - mid 常答「封包先送到 ClusterIP 那邊再轉發」(= 以為 ClusterIP 有實體,經典誤解)
  - senior 訊號: 在出發 node 本地就被 DNAT。iptables 鏈 KUBE-SERVICES → KUBE-SVC(機率選一個 backend)→ KUBE-SEP(DNAT 改目的地成 PodIP)。ClusterIP 是虛擬 IP,沒綁任何網卡,從來不會出現在 wire 上
- **L3**: 回程封包為什麼回得來?
  - mid 在這層卡住(沒想過回程問題)
  - senior 訊號: conntrack。kernel 的連線追蹤表記住這條連線的 NAT 映射,回程封包來源從 PodIP 反改寫回 ClusterIP,client 才認得這是同一條連線的回覆

**客製 hook**: 學員的謎題 B,session 8 崩過、session 9 D 段用 `docker exec <node> iptables-save` 親手追完整鏈、session 10 冷測二度封印。G 段可當保底自信題暖場,或換皮考: 「NodePort 進來的封包走的是同一條鏈嗎?」

---

### Q-P-10: CoreDNS、search domain 與 ndots

**適用 phase**: P2a+
**難度**: P2a 進階題

**題目**: 「Pod 裡的 app 連 `backend` 這個短名字,DNS 解析是誰做的?為什麼查一個外部域名有時會先打出好幾個失敗的 DNS query?為什麼 busybox 裡 nslookup 行為會怪怪的?」

**Why-chain 追問樹**:
- **L1**: 誰在解析?
  - mid 答「k8s 內建 DNS」(講不出實體在哪)
  - senior 訊號: CoreDNS 是 kube-system 裡的幾個 Pod;kubelet 起容器時把 resolv.conf 的 nameserver 指到 CoreDNS 的 ClusterIP。所以「DNS 查詢本身也走一次 Service/DNAT」
- **L2**: 為什麼多發好幾個 query?
  - mid 不知道 ndots(這層背不動)
  - senior 訊號: resolv.conf 有 search domain 列表 + `ndots:5`。少於 5 個點的名字先被展開成 `backend.default.svc.cluster.local` 等候選逐一嘗試;查外部域名(如 api.stripe.com,3 個點)也會先走一輪 search 全吃 NXDOMAIN 才查原名,流量和延遲都放大
- **L3**: busybox 為什麼怪?
  - senior 訊號: musl/busybox 的 resolver 實作和 glibc 不同,對 search/ndots 語義支援不完整。排障原則: 先用 FQDN 測,把 search 展開這個變因收掉;FQDN 通就不是 CoreDNS 死了,別急著重啟它

**客製 hook**: 學員 session 9 D 段親手撞過 busybox DNS 坑並當場 debug。L3 之後可追加一刀釣層級混淆: 「這題跟 conntrack 有沒有關係?」(session 11 他把 conntrack 誤拉進 NXDOMAIN,DNS 解析層 vs NAT 連線層要分開)

---

### Q-P-11: NetworkPolicy 的真實語義

**適用 phase**: P2a+(chunk 3 後)
**難度**: P2a 進階題

**題目**: 「NetworkPolicy 的預設行為是什麼?我 apply 了一個只 select `app=web` 的 ingress policy,其他沒被任何 policy 選中的 Pod 網路會變怎樣?」

**Why-chain 追問樹**:
- **L1**: 預設語義?
  - mid 常答「就是防火牆,沒寫的都擋」(= 錯,語義反了)
  - senior 訊號: 沒被任何 policy select 的 Pod 全通(default allow);一旦被 select,立刻進白名單模式,只有列出的來源放行。所以 default-deny 要自己寫一條空 selector 的 policy
- **L2**: 誰在執行這些規則?
  - mid 答「k8s 執行」(規則 vs 引擎混淆,這層背不動)
  - senior 訊號: NetworkPolicy 物件只是意圖(規則),引擎是 CNI plugin(Calico、Cilium)。kindnet 不支援,apply 了完全沒反應,不報錯也不生效
- **L3**: CNI 底層怎麼做到的?
  - senior 訊號: CNI 把 policy 編譯成每台 node kernel 裡的 iptables/eBPF 規則,和 kube-proxy 的 DNAT 同一層(netfilter),不是有個中央防火牆盒子在過濾

**客製 hook**: 這題就是驗學員 session 11 定型的「物件=規則 vs controller=引擎」三合一對照表能不能遷移到第四例(kube-proxy / cloud LB controller / Ingress controller / CNI)。L2 答出來 = pattern 已內化。

---

### Q-P-12: 封包全鏈路盲講

**適用 phase**: P2a+(chunk 4 收官)
**難度**: P2a 綜合題(Weekly Review 冷測款)

**題目**: 「從 Pod A 裡的 app 呼叫 `http://backend/api` 到收到 response,把整條鏈講完: DNS、DNAT、跨 node、回程。每一步發生在哪一層?」

**Why-chain 追問樹**:
- **L1**: 能不能分層講完不漏棒?
  - mid 常把 DNS 解析層和 NAT 連線層混在一起講,或漏掉回程
  - senior 訊號: 明確兩段式。第一段解析(resolv.conf → CoreDNS → 拿到 ClusterIP),第二段連線(本地 iptables DNAT → CNI 路由跨 node 到 PodIP → 回程 conntrack 反改寫)
- **L2**: resolv.conf 裡的 nameserver IP 是什麼?
  - mid 答「backend 的 IP」(把「去哪問」和「答案是什麼」壓成一步)
  - senior 訊號: 那是 CoreDNS 自己的 ClusterIP。兩步分開: resolv.conf 告訴你去哪問,CoreDNS 的回答才是 backend 的 ClusterIP
- **L3**: CNI 和 kube-proxy 的分工邊界在哪?
  - senior 訊號: CNI 負責 Pod 拿到真實 IP + Pod 對 Pod 可達(路由/overlay);kube-proxy 只管 Service 這層抽象的 DNAT。證據: 繞過 Service 直接 curl PodIP 照樣通,那是 CNI 的功勞

**客製 hook**: 學員 session 10 Weekly Review 無鷹架講過全鏈 PASS。L2 正是他當時被抓的洞(resolv.conf 的 IP 是 CoreDNS 的 ClusterIP),冷測重點放這。

---

### Q-P-13: RBAC 最小權限設計

**適用 phase**: P2b+
**難度**: P2b 核心題

**題目**: 「要給 CI pipeline 一個能 deploy 到 staging namespace 的權限,你會怎麼設計 RBAC?為什麼不直接給 cluster-admin,反正只是 staging?」

**Why-chain 追問樹**:
- **L1**: 用哪些元件組出來?
  - mid 只講「開個 service account 綁權限」(元件名對,設計缺席)
  - senior 訊號: ServiceAccount + Role(namespace 範圍,不用 ClusterRole)+ RoleBinding;verbs/resources 列到最小(get/list/create/update/patch on deployments/services,不給 delete secrets)
- **L2**: 「我加一條規則 deny 掉危險操作」行不行?
  - mid 順著答「可以」(這層背不動: RBAC 模型理解錯)
  - senior 訊號: RBAC 沒有 deny,只有 allow 的聯集。權限只能從零往上加,審查一個 SA 的實際權限要看它所有 binding 的總和,這也是為什麼亂綁 ClusterRoleBinding 很難清
- **L3**: 不給 cluster-admin 的真正理由?
  - senior 訊號: blast radius。CI 的 token 會躺在 CI 系統裡,洩漏是遲早要假設的事。cluster-admin token 洩漏 = 全叢集淪陷(含所有 Secrets);namespace-scoped 洩漏只傷 staging。最小權限不是形式主義,是在設計「洩漏之後會發生什麼」

---

### Q-P-14: IRSA 六棒鏈

**適用 phase**: P2b+
**難度**: P2b 核心題(EKS 實戰)

**題目**: 「EKS 上一個 Pod 要讀 S3,不放 access key。IRSA 是怎麼讓它拿到 AWS 權限的?把整條鏈從頭講到尾。」

**Why-chain 追問樹**:
- **L1**: 大方向?
  - mid 答「ServiceAccount 綁一個 IAM role」一句帶過(方向對,鏈全空)
  - senior 訊號: 能主動展開「誰發 token、誰驗 token、誰換憑證」三個問題
- **L2**: 六棒鏈完整版?(mid 通常在第 3-4 棒斷掉)
  - senior 訊號,依序: ① SA 標 role-arn annotation → ② mutating webhook 幫 Pod 注入 env + projected SA token(volume)→ ③ kubelet 定期輪替這個短效 token → ④ AWS SDK 憑 token 呼叫 STS AssumeRoleWithWebIdentity → ⑤ STS 拿 token 去 cluster 的 OIDC provider 驗簽、比對 trust policy 的 sub(namespace:sa 名)→ ⑥ 發短效 AWS 憑證給 Pod
- **L3**: 這比 node instance profile 好在哪?
  - mid 說「比較安全」(講不出為何)
  - senior 訊號: instance profile 是 node 粒度,同 node 上所有 Pod 共用同一份權限;IRSA 把身分縮到 Pod/SA 粒度,且 token 短效可輪替。多租戶 node 上這是質的差別

**客製 hook**: 學員公司 prod EKS(billing 平台)。G 段可加一問: 「你們家 workload 現在拿 AWS 權限是哪種方式?回去查得到嗎?」把題目接回他真實環境。

---

### Q-P-15: Secret、base64 與 etcd

**適用 phase**: P2b+
**難度**: P2b 基礎題(誘答高發區)

**題目**: 「k8s Secret 和 ConfigMap 差在哪?base64 是加密嗎?那 Secret 到底哪裡比較安全?」

**Why-chain 追問樹**:
- **L1**: base64 是什麼?
  - mid 有時真的答「有編碼保護」(這層直接見真章)
  - senior 訊號: base64 是編碼不是加密,`base64 -d` 一行解回。Secret 和 ConfigMap 在資料保護上幾乎是同一種東西
- **L2**: 那差異到底在哪?
  - senior 訊號: 差在周邊機制,RBAC 可以把 secrets 的 get/list 單獨授權(和 configmaps 分開)、kubelet 只把 Secret 發給真的用到它的 node、掛載走 tmpfs 不落磁碟、可以對 secrets 資源單獨開 encryption at rest
- **L3**: 真正的要害在哪?
  - senior 訊號: etcd。預設 Secret 在 etcd 裡就是 base64 明文,偷到一份 etcd snapshot = 偷到全叢集 secrets。所以要開 EncryptionConfiguration(EKS 用 KMS envelope encryption),而且 etcd 本身的存取要單獨收緊(接 Q-SD-02)

---

### Q-P-16: HPA 算法與延遲鏈

**適用 phase**: P3+
**難度**: P3 核心題

**題目**: 「HPA 是怎麼算出該有幾個 replica 的?從 CPU 開始飆到新 Pod 真的能接流量,中間隔著哪些延遲?」

**Why-chain 追問樹**:
- **L1**: 算法?
  - mid 答「超過 80% 就加一個」(= 錯,不是逐步加)
  - senior 訊號: `desired = ceil(current × currentMetric / targetMetric)`,按比例一次算到位;還知道百分比是相對 resources.requests,沒設 requests 的 Pod HPA 根本算不了
- **L2**: 延遲鏈?
  - mid 只想到「起 Pod 要時間」(漏掉整條 pipeline)
  - senior 訊號: metrics scrape 間隔 → HPA sync period(預設 15s)→ 建 Pod → scheduler → 沒位子的話 cluster autoscaler 開新 node(分鐘級)→ image pull → app 啟動 → readiness 過了才進 Endpoints。全鏈加起來輕鬆超過一分鐘
- **L3**: 所以秒級尖峰怎麼辦?
  - senior 訊號: 承認 HPA 是反應式的,尖峰當下救不了;要 pre-scale、降低 target 留 headroom、queue 削峰、load shedding(展開在 Q-P-18 / Q-SD-03)

**客製 hook**: 學員 kind 叢集 metrics-server 未裝(P3 lab 前要裝,`--kubelet-insecure-tls`),「HPA targets `<unknown>`」他大概率會親手撞到,考前先做 Q-T-07 對應 drill 效果最好。

---

### Q-P-17: drain、PDB 與它管不到的事

**適用 phase**: P3+
**難度**: P3 核心題

**題目**: 「`kubectl drain` 一個 node 時實際發生什麼?PDB 在裡面扮演什麼角色?PDB 擋得住 OOM kill 嗎?」

**Why-chain 追問樹**:
- **L1**: drain 的機制?
  - mid 答「把 Pod 搬走」(= 錯,沒有搬移這回事)
  - senior 訊號: cordon(標記不可調度)+ 對每個 Pod 呼叫 eviction API。Pod 是被刪掉,再由 controller 在別的 node 重建,狀態不會跟著走
- **L2**: PDB 的精確語義?
  - mid 答「保護 Pod 不被動到」(語義過強,這層背不動)
  - senior 訊號: PDB 只約束 voluntary disruption 的併發度。minAvailable 不滿足時 eviction API 回 429,drain 會停下來等;等到其他副本 ready 了才繼續。它是「慢慢來」不是「不准動」
- **L3**: involuntary 呢?
  - senior 訊號: OOM kill、node 硬體掛掉、kernel panic 不走 eviction API,PDB 完全管不到。所以 PDB 是維運操作的安全帶,不是可用性保證;真正的可用性要靠副本數 + topology spread

---

### Q-P-18: 扛 10 倍尖峰

**適用 phase**: P3+
**難度**: P3 綜合題(機制版;開放設計版見 Q-SD-03)

**題目**: 「你的服務平常 10 個 Pod,促銷開始 60 秒內流量變 10 倍。只靠 HPA 會發生什麼?你會怎麼補?」

**Why-chain 追問樹**:
- **L1**: 只靠 HPA 的結局?
  - mid 答「HPA 會自動擴容,沒問題」(對 HPA 的信仰,這層見真章)
  - senior 訊號: 引用延遲鏈(Q-P-16)推出結論,擴容分鐘級,尖峰秒級,新 Pod ready 之前現有 10 個 Pod 已經被打爆,可能還因 OOM/probe fail 連環倒,越倒越少
- **L2**: 有哪些補法?
  - senior 訊號: 分成三類講,(a) 事前: 尖峰可預測就 pre-scale(排程調 minReplicas)、降 target utilization 留 headroom、overprovisioning placeholder Pod 先佔位;(b) 門口: rate limit / load shedding,寧可拒絕部分請求也不全倒;(c) 中間: queue 削峰,把同步尖峰變非同步背壓
- **L3**: 怎麼選?代價是什麼?
  - senior 訊號: 主動講 tradeoff,headroom 是拿錢換反應時間;判斷標準是尖峰可不可預測。可預測(促銷有排程)用 pre-scale 最便宜;不可預測用 headroom + shedding。能講出「這是容量規劃問題,不是 autoscaling 參數問題」= 到位

---

### Q-P-19: PriorityClass 與 preemption

**適用 phase**: P3+
**難度**: P3 進階題

**題目**: 「PriorityClass 和 preemption 怎麼運作?什麼情況下 scheduler 會殺掉正在跑的 Pod?把所有服務都設最高 priority 會怎樣?」

**Why-chain 追問樹**:
- **L1**: 機制?
  - mid 答「優先級高的先被排程」(只講了一半)
  - senior 訊號: 排程順序只是其一;關鍵是 Pending 的高優先 Pod 找不到位子時,scheduler 會挑一台 node 驅逐較低優先的 Pod 騰位(preemption),受害者走 graceful termination
- **L2**: 這和 QoS eviction 是同一件事嗎?
  - mid 常混為一談(這層背不動)
  - senior 訊號: 兩套獨立機制。preemption 是 scheduler 為了「排程騰位」,看 priority;node-pressure eviction 是 kubelet 為了「node 自保」,看 QoS + 實際用量。觸發者、目的、依據全都不同
- **L3**: 全設最高會怎樣?
  - senior 訊號: priority 是相對值,全部最高 = 等於沒設,訊號歸零。正解是分級(系統元件 > 核心業務 > batch/best-effort),必要時用 `preemptionPolicy: Never` 做「高優先但不搶人」的班次

---

> **P4/P5 題幹改用英文**(English Ramp 檔位: P4 半英半中、P5 大量英文)。面試現場就是英文,題幹先習慣;why-chain 注解仍用中文點破。

### Q-P-20: SLO、error budget 與 burn rate

**適用 phase**: P4+
**難度**: P4 核心題

**題目 (EN)**: "Your service has a 99.9% availability SLO over a 30-day window. What is the error budget in concrete terms? What does a burn rate of 14.4 mean, and how would you design alerting around it?"

**Why-chain 追問樹**:
- **L1**: error budget 具體是多少?拿來幹嘛?
  - mid 背「允許的 downtime」但算不出數字,也講不出用途
  - senior 訊號: 0.1% × 30 天 ≈ 43 分鐘。budget 是「可以花的失敗額度」,用途是決策工具,budget 還有剩就繼續出貨,燒完就凍結 release 修可靠性。SLO 不是越高越好,是可靠性和迭代速度的匯率
- **L2**: burn rate 14.4 是什麼?
  - mid 在這層背不動(沒操作過 multi-window alert)
  - senior 訊號: burn rate = 燒 budget 的速度倍數(1 = 剛好 30 天燒完)。14.4 表示照這速度 1 小時燒掉約 2% 的月度 budget,這是 Google SRE 的 page 門檻之一;實務用 multi-window multi-burn-rate(如 5m+1h 快窗抓急性出血、6h+3d 慢窗抓慢性滲漏),兼顧快叫和不吵
- **L3**: 為什麼不直接對 CPU 高告警?
  - senior 訊號: alert on symptoms, not causes。CPU 高但 SLI 正常 = 不用半夜叫人;SLI 壞了才是用戶真的痛。資源類指標降級成 dashboard/ticket

---

### Q-P-21: histogram_quantile 是估計值

**適用 phase**: P4+
**難度**: P4 進階題

**題目 (EN)**: "Your Grafana panel shows `histogram_quantile(0.99, ...)` = 4.7s, but no single request actually took 4.7s. How is that possible? What decides the accuracy of this number?"

**Why-chain 追問樹**:
- **L1**: 為什麼會有「不存在的數字」?
  - mid 以為 p99 是從真實樣本裡挑出來的精確值(這層直接見真章)
  - senior 訊號: Prometheus histogram 只存每個 bucket 的計數,不存原始樣本。p99 是在「p99 落點所在的 bucket」內做線性內插估出來的,本來就是估計值
- **L2**: 精度由什麼決定?
  - senior 訊號: bucket 邊界。p99 落在一個 2s-8s 的寬 bucket 裡,內插誤差就是秒級。要在 SLO 門檻附近把 bucket 切密(例如 SLO 是 300ms,就在 200ms-500ms 之間多切幾刀),量測工具要跟著 SLO 設計
- **L3**: 那為什麼不用精確的 percentile?
  - senior 訊號: 分散式聚合的 tradeoff。histogram 的 bucket 計數可以跨 instance 相加再算 quantile;而 percentile 本身不可平均(平均 10 台機器各自的 p99 是數學錯誤),summary 類型的 quantile 無法聚合。犧牲單機精度,換取全服務視角

---

### Q-P-22: 斷掉的 trace

**適用 phase**: P4+
**難度**: P4 進階題

**題目 (EN)**: "In your tracing UI, service A's span is there, but the downstream call to service B is missing: the trace is broken. Where can the break happen, and in what order would you debug it?"

**Why-chain 追問樹**:
- **L1**: 第一反應猜哪裡?
  - mid 常答「collector 掛了吧」(治標式亂槍,collector 掛是全斷不是單邊斷)
  - senior 訊號: 最常見是 context propagation 斷了,`traceparent` header 沒被帶到 B。典型斷點: 自建 thread pool / queue 換了執行緒或行程(context 是 thread/task local 的)、用了沒 instrument 的 HTTP client、中間 proxy 把 header 剝掉
- **L2**: 排查順序?
  - senior 訊號: 沿著 header 走一遍,先在 B 的入口(access log 暫時 dump header)確認 traceparent 有沒有到 → 到了,查 B 的 SDK 有沒有 extract(版本/設定)→ 再查 sampling 決策 → 最後才輪到 export/collector。分層收斂,不是重啟 collector 碰運氣
- **L3**: 為什麼 sampling 決策要跟著 header 傳?
  - senior 訊號: head-based sampling 由最上游決定「這條要不要採」並隨 header 傳下去,全鏈才一致;各服務自己丟銅板就會出現半條 trace。tail-based 能按結果挑(只留 error/慢的),代價是要 buffer 全量 span,成本高一個量級

**客製 hook**: L1 的「collector 掛了」是治標當治本的變形(學員已知弱點模式),他若先答這個,追問「單邊斷和全斷的差別」讓他自己收回。

---

### Q-P-23: GitOps 與 drift

**適用 phase**: P5+
**難度**: P5 核心題

**題目 (EN)**: "Someone runs `kubectl edit deploy` directly in prod and changes the image tag. In a GitOps setup with Argo CD, what happens next? And why is this model better than a CI pipeline that runs `kubectl apply`?"

**Why-chain 追問樹**:
- **L1**: 接下來會發生什麼?
  - mid 答「Argo 會警告」就停(只知道紅燈,不知道機制)
  - senior 訊號: controller 持續 diff desired state(Git)vs live state(cluster),標記 OutOfSync;開了 selfHeal 就直接改回 Git 的版本。手改必被吃掉,Git 是唯一事實來源,這不是 bug 是 feature
- **L2**: pull model 好在哪?
  - mid 講不出和 CI push 的本質差異(這層背不動)
  - senior 訊號: 兩點。安全面,cluster credential 留在 cluster 內,CI 系統不需要拿 admin kubeconfig(對照 Q-P-13 的 blast radius);行為面,push 是一次性 apply、跑完就走,pull 是常駐 reconcile loop、持續收斂,和 P0 的 controller 是同一個模式
- **L3**: 什麼東西不該直接進 GitOps repo?
  - senior 訊號: 兩個經典。secrets 明文不能進 Git(要 sealed-secrets / external-secrets 間接引用);HPA 會動 replicas,Git 裡寫死 replicas 會和 HPA 打架、永遠 OutOfSync,要 ignoreDifferences 或乾脆不在 Git 管這個欄位

---

### Q-P-24: Operator 到底是什麼

**適用 phase**: P5+
**難度**: P5 核心題

**題目 (EN)**: "What exactly is a Kubernetes operator? How is it different from a Helm chart, and when would you actually write one instead of using Helm?"

**Why-chain 追問樹**:
- **L1**: 定義?
  - mid 答「安裝複雜軟體的工具」(和 Helm 分不開,這層見真章)
  - senior 訊號: operator = CRD(把你的領域概念變成 API 物件)+ 自訂 controller(對它跑 reconcile loop)。本質是把 runbook 裡的人工運維判斷寫成常駐程式
- **L2**: 和 Helm 的分界線?
  - senior 訊號: Helm 是安裝期的模板引擎,render 完 YAML 交給 cluster 就離場,day-2 不歸它管;operator 是 runtime 常駐,持續觀察並收斂,能做 failover、backup 排程、有順序的版本升級這種「裝完之後的事」。一句話: Helm 管出生,operator 管人生
- **L3**: 寫 reconcile 的鐵律?
  - senior 訊號: level-triggered + 冪等。每次醒來只看「現況 vs 期望」推一步,不能依賴「我收過什麼 event」,因為 controller 可能睡過頭(當機重啟)。答得出這個 = P0 的 Q-T-02 真的內化了

**客製 hook**: L3 直接回扣學員 P0 的 level-triggered 理解(controller 當機 10 分鐘那題),看他能不能自己把兩題接起來。

---

### Q-P-25: Cluster 升級順序與 version skew

**適用 phase**: P5+
**難度**: P5 核心題(運維判斷)

**題目 (EN)**: "Walk me through upgrading a production cluster from 1.29 to 1.31. In what order do you upgrade components, and why can't you jump two minor versions at once?"

**Why-chain 追問樹**:
- **L1**: 順序?
  - mid 答「都升到最新就好」(沒有順序概念,這層見真章)
  - senior 訊號: 一次只跨一個 minor(1.29→1.30→1.31);每一輪都是 control plane 先、node 後;HA control plane 逐台滾動
- **L2**: 為什麼是這個順序?
  - mid 背得出順序但講不出理由(這層背不動)
  - senior 訊號: version skew policy。kubelet 可以比 apiserver 舊(舊版容忍到 N-1/N-2,新版到 N-3),但絕不能比 apiserver 新,所以永遠先升 control plane;HA 下 apiserver 彼此之間最多差 1 個 minor,這就是不能跳版的硬約束
- **L3**: 升級前的風險清單?
  - senior 訊號: 查 API deprecation/removal(舊 API 版本會直接消失,manifest 會 apply 不進去)、staging 先演練、node 升級 = drain(PDB 和單副本服務先體檢,接 Q-P-17)、CNI/CoreDNS/addon 相容矩陣要對版本

**客製 hook**: 學員公司 prod EKS,EKS 升級(control plane 由 AWS 管、node group 自己滾)是他真實會遇到的事,G 段可請他對照 EKS 的流程差異。

---

### Q-P-26: etcd quorum 與災難復原

**適用 phase**: P5+
**難度**: P5 核心題(P0 Q-P-03 的實戰放大版)

**題目 (EN)**: "You run a 3-node etcd cluster. One node's disk dies. Then a second one dies. What is the state of your Kubernetes cluster at each step, and how do you recover from each?"

**Why-chain 追問樹**:
- **L1**: 每一步的 quorum 數學?
  - mid 背「要奇數台」但推不動具體情境
  - senior 訊號: 3 台 quorum=2。掛 1 台照常讀寫(還有多數);掛 2 台剩 1 台,湊不出多數,etcd 拒絕寫入
- **L2**: etcd 不能寫,叢集會怎樣?
  - mid 答「整個叢集掛掉」(過度悲觀,這層背不動)
  - senior 訊號: 資料面和控制面分開講。現有 Pod 照跑、Service 的 iptables 規則還在、流量照走;但 API 寫入失敗、controller 無法收斂、Pod 掛了沒人補、自癒全停。一句話: 控制面腦死,資料面殘存
- **L3**: 兩種情境的 recover 判斷?
  - senior 訊號: 掛 1 台 = quorum 還在,補一台新 member 讓它同步即可,絕對不要 restore;quorum 全失才動 `etcdctl snapshot restore`(它會建一個新 cluster,revision 重置,client 的 watch/resourceVersion 快取全部作廢)。所以 snapshot 要定期做 + 放異地,而且要演練過才算有備份

**客製 hook**: L2 就是 phase-6 那句「自癒的前提是 control plane 活著」的實體版;學員 P0 已有 quorum 概念,這題考的是往生產運維的延伸。etcd Raft 深入原本 park 到 P5,這題就是收割點。

---

## 故障排除(Scenario-Based)

### Q-T-01: Pod 一直 Pending

**適用 phase**: P0/P1+
**難度**: P0/P1 基礎排障題

**題目**: 「你 `kubectl apply -f deployment.yaml` 之後,Pod 一直是 Pending 狀態。你的排查步驟是什麼?」

**理想回答結構**:
1. `kubectl describe pod <name>` 看 Events
2. 依 Events 線索分支:
   - `0/N nodes available` 開頭 → 資源不足/taint/affinity 設定
   - admission webhook 相關 → 查 webhook config
   - image 相關 → 查 registry/imagePullPolicy
3. 說出每個分支怎麼確認根因

**Coach 追問**: 「如果 Events 裡完全沒有訊息呢?你會怎麼做?」(期望: 看 scheduler log、確認 scheduler 是否存活)

---

### Q-T-02: controller 當機 10 分鐘後重啟

**適用 phase**: P0+
**難度**: P0 概念題(考 level-triggered 理解)

**題目**: 「controller 當機了 10 分鐘,這段期間有 3 個 Pod 掛掉。controller 重啟後,它需要知道『是哪 3 個 Pod、什麼時候掛的』嗎?為什麼?」

**Pass 條件**:
- 說出「不需要」,因為 level-triggered
- 說清楚: 重啟後重讀 etcd,發現 actual < desired,直接補起來
- 不需要重播事件歷史

---

### Q-T-03: CrashLoopBackOff 但 Exit Code 0

**適用 phase**: P1+
**難度**: P1 進階排障題
**對應 drill**: chaos-drills.md P1-1(可先做 drill 再考,或反過來考完再 drill 冷測)

**題目**: 「一個 web Pod 在 CrashLoopBackOff,RESTARTS 一直加。describe 看到 Exit Code 0、Reason: Completed。app 團隊說程式碼沒改過。你的排查路徑?」

**理想回答結構**:
1. 先解讀訊號: exit 0 = 程式優雅退出,不是 crash。「健康的程式不會自己走,是有人請它走」→ 誰送的 SIGTERM?
2. `kubectl describe` 看 Events: 找 `Liveness probe failed`
3. 對照 probe 設定(port/path)vs 容器實際 listen 的 port
4. 主動講治標 vs 治本: 治本 = 修 probe 設定;順帶檢查偵測延遲(failureThreshold × periodSeconds)是否合理

**Coach 追問**: 「如果 Exit Code 是 137 而不是 0,你的分支怎麼走?」(期望: 137=128+9 SIGKILL,查 OOMKilled 或 liveness 超時強殺,和 exit 0 的推理完全不同路)

---

### Q-T-04: Service 不通但 PodIP 直連通

**適用 phase**: P2a+
**難度**: P2a 核心排障題
**對應 drill**: chaos-drills.md P2a-1~P2a-5 中的 Service/Endpoints 斷鏈類(可先做 drill 再考)

**題目**: 「app 連 `backend` Service 一直 timeout,但直接 `curl <PodIP>:8080` 是通的。排查路徑?」

**理想回答結構**:
1. PodIP 通 = CNI 層沒事,問題鎖定在「名字到 PodIP」中間的某層,分層排查
2. DNS 層: 進 Pod `nslookup backend.<ns>.svc.cluster.local`(用 FQDN 收斂變因),解不出來走 CoreDNS 支線
3. Service 層: `kubectl get endpoints backend`,是空的就查兩個嫌犯,selector 和 Pod label 對不上、或 readiness 沒過被閘門擋住
4. NAT 層: endpoints 有東西還不通,上 node `iptables-save | grep <ClusterIP>` 看 DNAT 鏈在不在(kube-proxy 死了規則不更新)
5. Policy 層: 有沒有 NetworkPolicy select 到 client 或 backend

**Coach 追問**: 「endpoints 是空的,兩個最可能的原因?各用哪個指令確認?」(期望: label 對照用 `kubectl get pods --show-labels` vs svc selector;readiness 用 describe pod 看 condition)

**客製 hook**: 這題就是學員 P2a chunk 1 全部知識的排障化。他答 DNS 層時若把 conntrack 扯進來,就是 session 11 的層級混淆復發,當場抓。

---

### Q-T-05: DNS 間歇性失敗,重啟 CoreDNS 短暫好轉

**適用 phase**: P2a+
**難度**: P2a 進階排障題(治標 vs 治本考點)
**對應 drill**: chaos-drills.md P2a-1~P2a-5 中的 CoreDNS/DNS 類(可先做 drill 再考)

**題目**: 「叢集內 app 間歇性報 `could not resolve host`。有人重啟 CoreDNS 之後好了幾小時又復發,提議寫個 cron 定期重啟。你怎麼接手?」

**理想回答結構**:
1. 先定層: resolve 失敗 = DNS 解析層,不要碰 conntrack/NAT/iptables 那條線
2. 拆「重啟會好轉」的訊號: 說明 CoreDNS 本體活著時也會被打掛,嫌犯是負載(ndots 放大的 query 量)、CoreDNS 資源 limit 太小被 throttle/OOM、或 upstream DNS 不穩
3. 排查: CoreDNS pod 的 restarts/資源用量 → CoreDNS log(開 log plugin 短暫觀察)→ 量 query 型態(是不是一堆 search 展開的 NXDOMAIN)
4. 明確講: cron 重啟是治標,根因沒除;治本可能是調 ndots/用 FQDN、給 CoreDNS 加資源或副本、或 NodeLocal DNSCache

**Coach 追問**: 「重啟會短暫好轉,這個事實本身告訴你什麼?」(期望: 排除設定錯誤類根因,指向累積型問題,負載、記憶體、連線堆積)

---

### Q-T-06: IRSA 設了但 Pod 拿不到 S3

**適用 phase**: P2b+
**難度**: P2b 核心排障題
**對應 drill**: chaos-drills.md P2b-1~P2b-3 中的 IRSA 類(可先做 drill 再考)

**題目**: 「同事說 IRSA 都設好了,但 Pod 讀 S3 還是報錯。你要到的第一個資訊是什麼?排查路徑?」

**理想回答結構**:
1. 先要錯誤訊息原文,分兩類縮一半範圍: `NoCredentialProviders` / `Unable to locate credentials` = 憑證鏈前段斷(token 根本沒注入或 SDK 沒讀到);`AccessDenied` = 身分拿到了但權限不夠(IAM policy / trust policy 後段)
2. 沿六棒鏈逐棒驗: SA 有沒有 role-arn annotation → Pod 裡有沒有 `AWS_WEB_IDENTITY_TOKEN_FILE` env 和 projected token(webhook 有沒有動到這個 Pod,注意 Pod 要在 SA 標好之後重建)→ trust policy 的 sub 條件是不是精確等於 `system:serviceaccount:<ns>:<sa>` → cluster OIDC provider 有沒有建 → role 上的 permission policy
3. 講出最常見的兩個坑: annotation 加了但 Pod 沒重建;trust policy 的 namespace/SA 名打錯一個字

**Coach 追問**: 「哪一棒斷掉會是 NoCredentialProviders,哪一棒斷是 AccessDenied?」(期望: 能把錯誤類型映射回鏈上的位置,這就是 senior 和照 checklist 亂試的差別)

---

### Q-T-07: HPA 顯示 targets `<unknown>`

**適用 phase**: P3+
**難度**: P3 基礎排障題
**對應 drill**: chaos-drills.md P3-1~P3-4 中的 HPA/metrics 類(可先做 drill 再考)

**題目**: 「`kubectl get hpa` 顯示 TARGETS 是 `<unknown>/80%`,replica 完全不動。排查路徑?」

**理想回答結構**:
1. `<unknown>` = HPA 拿不到指標,問題在 metrics pipeline 不在算法,先驗 `kubectl top pods` 動不動
2. top 不動 → metrics-server 沒裝或沒起來(`kubectl get apiservice v1beta1.metrics.k8s.io` / `-n kube-system get deploy metrics-server`)
3. top 會動但 HPA 還是 unknown → Pod 沒設 `resources.requests`(HPA 的百分比是相對 requests,沒分母就算不出來);多容器 Pod 每個容器都要設
4. describe hpa 看 Events,訊息會直接指向哪一段

**Coach 追問**: 「為什麼沒設 requests 連百分比都算不出來?」(期望: target 80% 是「用量 / requests」,分母不存在)

**客製 hook**: 學員 kind 叢集 metrics-server 未裝(2026-06-28 重建後消失),這題他八成會在 P3 lab 開場親手撞到,先撞再考效果最好;kind 裝 metrics-server 要 `--kubelet-insecure-tls`。

---

### Q-T-08: drain 卡住不動

**適用 phase**: P3+
**難度**: P3 核心排障題
**對應 drill**: chaos-drills.md P3-1~P3-4 中的 PDB/drain 類(可先做 drill 再考)

**題目**: 「維護窗口內 `kubectl drain node-2` 卡在 `evicting pod payments/api-xxx` 十分鐘不動。為什麼?你有哪些選項,各自代價?」

**理想回答結構**:
1. 定位: `kubectl get pdb -n payments`,看 ALLOWED DISRUPTIONS 是不是 0(eviction API 一直收 429,drain 在重試等待)
2. 追為什麼是 0: replicas=1 配 minAvailable=1(數學上永遠不允許中斷)、或其他副本 not ready 撐不起 minAvailable
3. 選項與代價: (a) 治本,先把 Deployment scale up 讓 PDB 有餘裕,等新副本 ready 再 drain;(b) 修好 not ready 的副本;(c) 硬繞(`--disable-eviction` 直接刪),等於毀約,服務可能中斷,只有真緊急才用且要說出口
4. senior 加分: 主動講「這暴露的是配置矛盾,單副本 + minAvailable=1 本來就 drain 不了,upgrade 前就該體檢」

**Coach 追問**: 「如果這是 3 AM 的緊急 kernel patch,你選哪個?白天例行維護又選哪個?」(期望: 判斷力隨情境切換,而不是背一個標準答案)

---

### Q-T-09: 用戶喊慢但 p99 好好的

**適用 phase**: P4+
**難度**: P4 綜合排障題
**對應 drill**: chaos-drills.md P4-1~P4-2(可先做 drill 再考)

**題目**: 「客服回報一批用戶抱怨結帳很慢,但 Grafana 上該服務的 p99 latency 一條平線,毫無異常。你怎麼查?」

**理想回答結構**:
1. 先質疑量測而不是質疑用戶: 儀表板沒異常 ≠ 沒問題,列出量測會說謊的方式
2. 嫌犯清單: (a) histogram bucket 上限太低,慢請求全堆在最大 bucket,quantile 被 clamp 在上限,再慢也畫不出來(接 Q-P-21);(b) 量測點位置,server-side 量的不含 LB 排隊/TLS/重試,client 感受的是全程;(c) 聚合稀釋,全體 p99 平,但某個分群(單一 AZ、單一大客戶、某個 endpoint)炸了被平均蓋掉
3. 動作: 拿一個具體用戶案例走 trace(P4 的 trace 派上用場)、按維度切開 latency(by pod / by endpoint / by client)、對照 client 端指標或 LB access log
4. 治本: 修 bucket 邊界對齊 SLO、補 client-side SLI

**Coach 追問**: 「bucket 最大邊界 5s,實際有請求跑了 30s,面板上 p99 會顯示多少?」(期望: 頂多 5s 上下,永遠不會超過最大有限 bucket,這就是平線的成因)

---

### Q-T-10: Argo CD 永遠 OutOfSync

**適用 phase**: P5+
**難度**: P5 核心排障題
**對應 drill**: chaos-drills.md P5-1~P5-3 中的 GitOps drift 類(可先做 drill 再考)

**題目**: 「一個 app 在 Argo CD 上永遠 OutOfSync,手動 sync 變綠,幾十秒後又紅回來。沒有人在手改。排查路徑?」

**理想回答結構**:
1. 推理: sync 完馬上又 drift = cluster 裡有另一個 controller 持續改 live state,和 Git 打架
2. 定位: 看 Argo 的 diff,鎖定是哪個欄位在跳。經典嫌犯: HPA 在改 `spec.replicas`、mutating webhook 在注入 sidecar/預設值、其他 operator 在回寫欄位
3. 治本 vs 治標: 開 auto-sync + selfHeal 蓋回去是治標而且更糟(和 HPA 進入拔河,replicas 反覆橫跳);治本是讓兩邊管轄權分家,Git 不管這個欄位(replicas 從 manifest 拿掉)或 Argo 配 `ignoreDifferences`
4. senior 加分: 一句話點破「這不是 bug,是兩個 reconcile loop 對同一欄位有不同 desired state,分權才是正解」

**Coach 追問**: 「為什麼開 selfHeal 反而更糟?具體會看到什麼現象?」(期望: HPA scale 到 5,Argo 蓋回 3,HPA 再拉到 5,Pod 數量鋸齒震盪,服務容量忽高忽低)

---

## k8s x System Design 交集

### Q-SD-01: 多副本 scheduler 的 leader election

**適用 phase**: P0(Stretch)/P3+
**難度**: P0 Stretch,P3 正式題

**題目**: 「Kubernetes scheduler 為什麼要做 leader election?如果同時有兩個 scheduler 在跑,會有什麼問題?」

**Pass 條件**:
- 說出可能重複調度同一個 Pod 到兩個 node 的問題
- 說出 lease/leader election 確保同時只有一個 scheduler 做決策
- Stretch: 說出 leader election 本身也是 etcd 裡的一個物件

---

### Q-SD-02: 為什麼 etcd 要分開部署,不和 api-server 同主機(P2b+)

**適用 phase**: P2b+(資安面);P5 再考一次(運維面)
**難度**: 中級

**題目**: 「生產環境為什麼常把 etcd 和 api-server 分開部署,或至少給 etcd 獨立磁碟?放同一台會有什麼具體風險?」

**Pass 條件**:
- 效能面: etcd 每筆寫入要 fsync WAL 到磁碟才算 commit,對 disk latency 極度敏感;api-server/log/監控 agent 搶同一顆磁碟的 IO,fsync 變慢 → Raft heartbeat 超時 → leader election 亂跳 → 整個叢集寫入抖動。一台 node 的磁碟繁忙放大成全叢集控制面故障
- 故障域: api-server 是 stateless,多副本、隨便死隨便補;etcd 是 stateful 的 source of truth,兩者的生命週期、保護等級、備份策略完全不同,不該綁在同一個故障域
- 安全面: etcd 裡有全叢集資料含所有 Secrets(回扣 Q-P-15 L3),主機被入侵的 blast radius 不一樣,etcd 主機要收到最緊

**Stretch**: 說出 etcd 官方對 disk 的量級要求(WAL fsync 毫秒級,建議 SSD/獨立盤),或講出「managed control plane(EKS)就是把這整組煩惱外包」的 tradeoff。

**Coach 追問**: 「監控上你會先看哪個指標判斷 etcd 磁碟不行了?」(期望方向: etcd_disk_wal_fsync_duration / backend_commit_duration,或退一步答「etcd 自己的 slow request 警告 log」)

---

### Q-SD-03: 促銷尖峰的整體設計(開放題)

**適用 phase**: P3+
**難度**: P3 綜合設計題(Q-P-18 的開放版,一個考機制、這題考設計對話)

**題目**: 「設計題: 一個促銷活動服務跑在 EKS 上,平時 1k RPS,活動開始 60 秒內衝到 10k RPS,5 分鐘後回落。預算有限。給我你的整體設計。」

**Pass 條件**:
- 開場先問對問題: 尖峰可預測嗎(促銷有排程 = 可預測)、哪些請求可以降級、SLO 是什麼。先問再設計是 senior 訊號
- 分層設計: 門口(CDN/cache 吃掉靜態流量、rate limit/load shedding 保底)、中間(queue 削峰,把下單從同步變非同步)、運算層(pre-scale 排程調 minReplicas + HPA 收尾、留 headroom)、韌性(PDB + topology spread,擴容期間別被一台 node 拖死)
- 誠實面對延遲鏈: 能主動講「HPA + cluster autoscaler 是分鐘級,60 秒尖峰只能靠事前容量和門口防禦」
- 成本意識: pre-scale 只在活動窗口,平時縮回;headroom 是拿錢換反應時間,講得出這筆帳

**Coach 追問**: 「活動開始 30 秒,DB 連線數打滿了,你的設計裡哪一層在保護 DB?」(期望: queue/背壓 + 連線池上限,而不是「再加 Pod」,加 Pod 只會把 DB 壓得更死)

---

### Q-SD-04: Region 掛掉怎麼辦(multi-cluster HA)

**適用 phase**: P5+
**難度**: 高(senior 判斷題,考 push back 能力)

**題目 (EN)**: "Your billing platform runs on a single EKS cluster in one region. The business asks for 'zero downtime even if the whole region goes down.' What do you propose, and what do you push back on?"

**Pass 條件**:
- 先劃清 k8s 自癒的邊界: reconcile 的前提是 control plane 活著;region 掛掉,收斂無從發生,k8s 不會救你(P0 知識的 SD 天花板應用)
- 否決 stretched cluster: 把一個 etcd cluster 橫跨兩個 region,延遲會打爆 heartbeat/leader election(Q-SD-02 的放大版),正解是每 region 一個獨立 cluster
- 指出真正的難點在資料層不在運算層: 運算層多開一份 cluster 很簡單;billing 是強一致業務,跨區複寫的 RPO/RTO、failover 時的資料完整性才是要花錢花人的地方
- push back 部分: 「zero downtime」要翻譯成具體 SLO 和預算,active-active 和 warm standby 價差一個量級;先問業務願意為最後一個 9 付多少錢

**Coach 追問**: 「DNS failover 切過去了,但舊 region 其實只是網路分區沒有真死,兩邊同時在寫,billing 會發生什麼?」(期望: split-brain 意識,講出 fencing/單邊寫入仲裁的必要)

**客製 hook**: billing 平台就是學員公司的真實場景,答完可請他評估自家目前在哪一級(single region? 有沒有跨區備份?)。

---

### Q-SD-05: 30 個微服務的部署管線設計

**適用 phase**: P5+
**難度**: 高(GitOps 綜合)

**題目 (EN)**: "Design the deployment pipeline for about 30 microservices on EKS: from a merged PR to production, including progressive delivery and a rollback story."

**Pass 條件**:
- CI/CD 分權: CI 只負責 build/test/推 image;CD 是 cluster 內的 GitOps controller pull(Argo CD),CI 不持有 cluster credential(回扣 Q-P-23 L2)
- desired state 唯一來源: 環境晉升(dev → staging → prod)靠 Git PR 改 image tag/values,不靠人手 kubectl;審計紀錄天然存在 Git history
- progressive delivery: canary(Argo Rollouts),推進與否用 metric gate 綁 SLI(接 P4,burn rate 異常自動暫停),不是靠人盯 dashboard
- rollback story: `git revert` + controller 收斂 = 宣告式 rollback,快且可審計;講得出「舊 RS 還在所以 k8s 層 rollback 也快」(Q-P-08)更好
- secrets 不進 Git: external-secrets/sealed-secrets 一句帶到即可

**Stretch**: 30 個服務的規模問題,app-of-apps / ApplicationSet 模板化,避免 30 份複製貼上的 pipeline。

---

## CKA/CKAD 限時(副線,P6 才密集練)

> 以下題目不是主線教學,P6 才使用。記錄在此作為索引。

### Q-CKA-01: 快速建立 Pod/Deployment YAML

**題目**: 「在 2 分鐘內,不查文件,建立一個 3 replica 的 nginx Deployment,並 expose 為 ClusterIP Service port 80。」

```bash
kubectl create deployment nginx --image=nginx --replicas=3 --dry-run=client -o yaml > dep.yaml
kubectl apply -f dep.yaml
kubectl expose deployment nginx --port=80 --target-port=80
```

---

### Q-CKA-02: 找出哪個 node 資源最多可用

**題目**: 「不用第三方工具,快速看哪個 node 現在 allocatable CPU 最多。」

```bash
kubectl describe nodes | grep -A5 "Allocatable:"
kubectl top nodes
```

---

### Q-CKA-03: 安全下線一個 node 維護

**適用 phase**: P6(概念在 P3 已學,這裡練手速)
**難度**: CKA 標配

**題目**: 「3 分鐘內: 把 worker node 下線維護,盡量不中斷服務,維護完恢復。」

```bash
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
# ...維護...
kubectl uncordon <node>
```

**手感備忘**: 忘了 `--ignore-daemonsets` 會直接報錯不動;drain 卡住先 `kubectl get pdb -A`(對接 Q-T-08 的原理,考場上別跟 PDB 耗,看清楚題目要求)。

---

### Q-CKA-04: etcd snapshot 備份與還原

**適用 phase**: P6(原理在 P5 Q-P-26,這裡練指令)
**難度**: CKA 必考,失分重災區

**題目**: 「對 control plane 上的 etcd 做一次 snapshot 存到 /backup/snap.db,然後演示怎麼從它還原。」

```bash
# 備份(三張證書去 /etc/kubernetes/pki/etcd/ 找)
ETCDCTL_API=3 etcdctl snapshot save /backup/snap.db --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key
ETCDCTL_API=3 etcdctl snapshot status /backup/snap.db

# 還原到新 data dir(restore 不需要證書,讀的是本地檔案)
ETCDCTL_API=3 etcdctl snapshot restore /backup/snap.db --data-dir /var/lib/etcd-restore

# 把 etcd static pod manifest 的 hostPath volume 改指到 /var/lib/etcd-restore
# (/etc/kubernetes/manifests/etcd.yaml,kubelet 會自動重建 etcd)
```

**手感備忘**: save 要證書、restore 不用,兩者常被搞混;restore 完沒改 manifest 的 hostPath = 白做。

---

### Q-CKA-05: RBAC 快速授權並驗證

**適用 phase**: P6(原理在 P2b Q-P-13)
**難度**: CKA 標配

**題目**: 「2 分鐘內: 在 staging namespace 建一個 SA `ci-deployer`,給它管理 deployments 和 services 的權限(不含刪除),並驗證權限生效。」

```bash
kubectl create serviceaccount ci-deployer -n staging
kubectl create role deployer -n staging --verb=get,list,watch,create,update,patch --resource=deployments,services
kubectl create rolebinding ci-deployer-binding -n staging --role=deployer --serviceaccount=staging:ci-deployer

# 驗證(兩題都要會)
kubectl auth can-i update deployments -n staging --as=system:serviceaccount:staging:ci-deployer   # yes
kubectl auth can-i delete deployments -n staging --as=system:serviceaccount:staging:ci-deployer   # no
```

**手感備忘**: `--as=system:serviceaccount:<ns>:<sa>` 這串格式要背熟;考場全用 imperative 指令,別手寫 YAML。

---

### Q-CKA-06: default-deny NetworkPolicy + 放行白名單

**適用 phase**: P6(原理在 P2a Q-P-11)
**難度**: CKA 進階(YAML 要能默寫)

**題目**: 「在 prod namespace 做 default-deny ingress,然後只允許帶 `app=frontend` label 的 Pod 連到 `app=api` 的 8080。」

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {}          # empty selector = select all pods in ns
  policyTypes: ["Ingress"]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: ["Ingress"]
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

**手感備忘**: `podSelector: {}` 是「全選」不是「全不選」(語義考點,對接 Q-P-11 L1);本機 kind 練這題要先裝 Calico(kindnet 不支援,apply 了不生效)。

---

## 誘答庫(似是而非說法清單)

> **用法**: 誘答 = 聽起來合理其實錯的完整說法,埋在學員似懂非懂的邊界,要他抓出來並講清楚「為什麼錯、錯在哪一層」。這是學員最愛也最需要的機制(真實職場弱點: 覺得怪怪的但沒把握就被同事帶走)。
> 使用紀律: 每個 keystone chunk 的 Gate 至少埋 1 條;不要預告「這是誘答」,自然地當成教練的口誤或「同事的說法」丟出來;學員若順著接走,停下來拆,那正是要加壓的點。
> 標注「已用過」的條目 = 學員反殺過,冷測可換皮重複使用。
> [RUNTIME: 優先從 mistake-registry 裡學員最近錯過的層級挑條目;學員連兩條被帶走就降階,先回 phase 檔補 C 段]

### P0

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P0-a | 「kubectl apply 會把指令發給 scheduler,由 scheduler 負責執行部署」 | apply 只是把 desired state 寫進 API Server/etcd 就結束了;scheduler 是自己 watch 到 unscheduled Pod 才動,沒有人「呼叫」它 | 控制流方向(推 vs watch),imperative 思維殘留 |
| P0-b | 「controller 當機期間掛掉的 Pod 事件會遺失,重啟後補不回來,要人工對帳」 | level-triggered: controller 重啟後重讀現況,actual < desired 直接補,不需要事件歷史 | edge vs level 語義 |
| P0-c | 「kubelet 發現 Pod 掛了,會把狀態直接寫回 etcd」 | 只有 API Server 直接讀寫 etcd;kubelet 走 API Server 更新 status | 元件職責邊界(學員 P0 曾口誤此處,已釘正,冷測可重複使用) |
| P0-d | 「etcd 跑 2 台比 1 台更可靠,至少有備援」 | 2 台 quorum=2,任一台掛就無法寫入,可用性反而比 1 台差;容錯數沒有增加 | quorum 數學 |

### P1

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P1-a | 「Pod 被 OOMKilled 就是 node 記憶體不夠了,加 node 就好」 | 容器級 OOM 是撞自己的 cgroup limit,和 node 餘量無關;加 node 完全治不到 | 兩種 OOM 機制混淆 + 治標當治本 |
| P1-b | 「liveness probe fail 會把 Pod 從 Service 摘掉,readiness fail 會觸發重啟」 | 語義整組對調: readiness 管 Endpoints 進出,liveness 管殺與重啟 | probe 語義 |
| P1-c | 「memory leak 導致 OOMKilled?把 limit 調大一倍,問題就解決了」 | leak 是鋸齒爬頂,limit 調大只是延後炸點;治本是修 leak,調大只買時間且要說清楚是買時間 | 治標 vs 治本(學員 session 5/6 已能分辨,冷測用) |
| P1-d | 「只設 limits 沒設 requests 的 Pod 是 BestEffort,最先被驅逐」 | 只設 limits 時 requests 自動補成等於 limits,結果是 Guaranteed,驅逐順位最安全,和說法完全相反 | QoS 判定規則(學員 session 5 學過此規則) |

### P2a

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P2a-a | 「kube-proxy 是一個一直在轉發封包的 proxy 程式,它掛了 Service 立刻全斷」 | kube-proxy 只寫 iptables 規則,搬封包的是 kernel;它掛了既有規則照常工作,新變更才不生效 | 規則 vs 引擎(**已用過**: session 8 學員反殺成功,冷測可換皮重複使用) |
| P2a-b | 「apply 了 Ingress 物件,流量就會自動按 path 分流了」 | Ingress 物件只是規則,沒有 Ingress Controller 這個引擎,apply 了完全沒反應 | 物件=規則 vs controller=引擎(**已用過**: session 11 學員秒殺,冷測可換皮,例如換成 NetworkPolicy 版) |
| P2a-c | 「Pod IP 反正查得到,把它寫死在程式 config 裡,少一層 Service 還比較快」 | Pod IP 是 ephemeral,重建就換;Service/DNS 那層抽象就是為此存在;省掉的那層「開銷」是本地 DNAT,幾乎免費 | 抽象層存在理由(**已用過**: SKILL.md 範例,冷測可重複使用) |
| P2a-d | 「封包會先送到 ClusterIP 那裡,拿到真正的 Pod IP 之後再轉過去」 | ClusterIP 沒有實體、不綁網卡,封包在出發 node 本地就被 DNAT 改寫,從頭到尾沒有「先去 ClusterIP」這一站 | NAT 層機制(學員本人的歷史誤解,session 8 崩過、已雙重封印;高價值冷測題) |
| P2a-e | 「Pod 內 nslookup 一直 NXDOMAIN,先查 conntrack table 是不是滿了」 | NXDOMAIN 是 DNS 解析層的回答(名字查不到),conntrack 是連線/NAT 層;table 滿的症狀是新連線建不起來,不是解析失敗 | 層級混淆: DNS 解析層 vs NAT 連線層(學員 session 11 現場犯過,拆解後守住;冷測重點) |

### P2b

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P2b-a | 「Secret 是 base64 加密存放的,比 ConfigMap 安全就在這裡」 | base64 是編碼不是加密,一行指令解回;真正差異在 RBAC 分權/tmpfs/encryption at rest 這些周邊機制 | 編碼 vs 加密 |
| P2b-b | 「這個 SA 權限太大,我們加一條 RBAC 規則把危險操作 deny 掉」 | RBAC 沒有 deny,只有 allow 的聯集;要縮權只能重設它的 binding,不能疊一條負向規則 | RBAC 授權模型 |
| P2b-c | 「IRSA 就是把 AWS access key 存進 Secret,Pod 掛載進去用」 | IRSA 整條鏈就是為了消滅長效 key: projected SA token 短效輪替,用 STS AssumeRoleWithWebIdentity 換臨時憑證 | 憑證機制(答對六棒鏈的人不會被這句帶走) |
| P2b-d | 「Pod 放在不同 namespace 就互相連不到了,等於網路隔離」 | k8s namespace 是邏輯分組,不做網路隔離;跨 ns 用 FQDN 照連;要擋流量得用 NetworkPolicy | namespace 語義(學員 P1 自己問出過這個撞名點,冷測可用) |

### P3

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P3-a | 「CPU 一超標 HPA 就會馬上加 Pod,尖峰交給它就好」 | HPA 反應是分鐘級(metrics scrape → sync period → 起 Pod → readiness),秒級尖峰打進來時新 Pod 還沒出生 | 延遲鏈被無視(對接 Q-P-16/18) |
| P3-b | 「設了 PDB,drain 和 OOM 都動不了我的 Pod,可用性穩了」 | PDB 只約束 voluntary eviction(drain 這類);OOM/node 掛是 involuntary,PDB 管不到;而且 PDB 是「等」不是「禁止」 | PDB 語義過度延伸(對接 Q-P-17) |
| P3-c | 「requests 設小一點,scheduler 就能塞更多 Pod,整體使用率更高,沒有代價」 | requests 低報 = node 超賣,實際用量一上來就 node pressure → eviction/CPU 爭搶;省下的是紙面資源,付出的是穩定性 | 排程帳面 vs 實際用量 |
| P3-d | 「把所有服務的 PriorityClass 都設最高,大家都安全」 | priority 是相對值,全高等於全平,訊號歸零;真出事時 scheduler 反而失去分流依據 | 相對值 vs 絕對值(對接 Q-P-19 L3) |

### P4

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P4-a | 「Grafana 上的 p99 是 4.7s,表示真的有請求跑了 4.7s,去 trace 它」 | histogram_quantile 是 bucket 內插的估計值,4.7s 可能根本不存在於任何真實請求;先看 bucket 邊界再說 | 估計值當精確值(對接 Q-P-21) |
| P4-b | 「SLO 99.9% 的意思就是: 可用率一掉到 99.9% 以下就告警叫人」 | SLO 是月度預算不是即時門檻;正確做法是對 burn rate 告警(燒太快才叫人),瞬間掉一下可能連 budget 的零頭都沒花到 | SLO vs alert 門檻混淆(對接 Q-P-20) |
| P4-c | 「trace 在 B 服務斷掉,八成是 collector 掛了,重啟一下」 | collector 掛是全斷不是單邊斷;單邊斷幾乎都是 propagation(header 沒帶過去)或 SDK 沒 extract | 層級混淆 + 治標當治本(對接 Q-P-22) |
| P4-d | 「node CPU 90% 了,快設個告警半夜叫人」 | alert on symptoms not causes: CPU 高但 SLI 正常不值得叫醒人;資源指標進 dashboard/ticket,page 留給 SLO burn | 告警哲學 |

### P5

| # | 誘答說法 | 為什麼錯 | 錯在哪一層 |
|---|---------|---------|-----------|
| P5-a | 「我們有 GitOps 啊,CI pipeline 最後一步就是 kubectl apply」 | 那是 push model 的 CI/CD;GitOps 的要件是 cluster 內 controller 持續 pull + diff + 收斂,有 drift detection,credential 不出 cluster | 一次性 apply vs 常駐 reconcile(對接 Q-P-23) |
| P5-b | 「operator 就是比較高級的 Helm chart,都是拿來裝軟體的」 | Helm 是安裝期模板,render 完離場;operator 是 CRD + 常駐 controller,管 day-2(failover/backup/升級步驟) | 安裝期 vs runtime(對接 Q-P-24) |
| P5-c | 「升級 cluster 就全部元件一起拉到最新版,一次到位最省事」 | version skew 硬約束: control plane 先、一次一個 minor;kubelet 不能比 apiserver 新;跳版會直接踩 API removal | 升級順序與 skew policy(對接 Q-P-25) |
| P5-d | 「3 台 etcd 掛了 1 台,趕快用 snapshot restore 回來」 | quorum 還在(2/3),補一台新 member 就好;restore 會建新 cluster、revision 重置,quorum 未失時 restore 是自殘 | 恢復手段選錯檔位(對接 Q-P-26 L3) |

---

## Behavioral(Q-B-*)

> **用法**: 題幹全英文(senior 面試現場就是英文)。每題給「好答案的形狀」(結構要點,不是範文,素材必須是學員自己的);追問方向給 Coach 加壓用。
> **素材流水線**: 平時把事件存進 `workspaces/k8s/story-bank.md`(P3 起隨手記),P6 照 `references/phase-6-interview-sprint.md` C-4 的 STAR 提煉流程 drill 成 2-3 則主力故事,一則故事通常可以覆蓋 2-3 題。
> [RUNTIME: mock 時先看 story-bank.md 當下有什麼素材,挑最貼的題;素材空的題先當「回去補故事」的作業,不硬掰]

### Q-B-01: Biggest incident you handled

**適用 phase**: P6(素材蒐集從 P3 起)
**難度**: senior 必考,幾乎每輪都有

**題目 (EN)**: "Tell me about the most serious production incident you've handled. Walk me through it."

**好答案的形狀**:
- 開場一句話講 impact(誰受影響、多久、多嚴重),不要從技術細節開場
- timeline 有結構: 怎麼偵測到 → 第一個 triage 判斷(以及為什麼先看那裡)→ 止血(治標,先恢復服務)→ 根因(治本)→ postmortem action(至少一條真的落地的)
- 主詞是 I 不是 we: 面試官要的是你的決策點,不是團隊流水帳
- 主動講治標/治本的切換時機(這是學員練了三個 session 的肌肉,behavioral 版要能用英文講)

**追問方向**: "What would you do differently?" / "How did you decide to mitigate first instead of debugging?" / 挑 timeline 最模糊的一步要細節(模糊處通常是背來的)

**素材對接**: story-bank.md 的 incident 類素材 → C-4 STAR 提煉。

---

### Q-B-02: A technical decision you pushed back on

**適用 phase**: P6
**難度**: senior 分水嶺題

**題目 (EN)**: "Tell me about a time you pushed back on a technical decision. What happened?"

**好答案的形狀**:
- 先把對方的方案講得公道(steelman),證明你真的理解才反對,不是反射性唱反調
- 反對的依據是資料或機制,不是資歷或直覺: 「我量了 X」「這會在 Y 層炸」
- 講清楚結局的兩種都可接受: 說服成功(用什麼證據)或被否決但你 disagree and commit(以及後來驗證了誰對)
- 收在關係沒壞: push back 是對事,講得出對方後來怎麼看你

**追問方向**: "What if they were more senior than you?" / "Have you ever pushed back and been wrong?"(直接橋接到 Q-B-03)

**素材對接**: story-bank.md → C-4。**客製 hook**: 這題正對學員的真實弱點(覺得怪怪的但沒把握就被同事帶走,memory 有記)。mock 時 Coach 加壓問「當下你其實不確定,你怎麼決定要不要開口」,他答得出「用機制推、不用氣勢賭」才算過;誘答訓練(抓錯並講清楚錯在哪層)就是這題的日常肌肉。

---

### Q-B-03: A time you were wrong

**適用 phase**: P6
**難度**: 中,但答壞率高(挑太小的錯 = 逃避)

**題目 (EN)**: "Tell me about a time you were confidently wrong about something technical."

**好答案的形狀**:
- 挑一個真的有後果的錯,不要挑「我有次打錯字」這種安全牌(面試官看的就是你敢不敢挑真的)
- 講清楚當時為什麼那麼有把握(錯誤的心智模型是什麼)、什麼證據打醒你
- 重點放在事後系統性的改變: 不是「我以後會更小心」,而是流程/驗證習慣怎麼改了
- 語氣自然,不表演自責

**追問方向**: "How did you find out you were wrong?" / "What do you do differently now before you commit to a position?"

**素材對接**: story-bank.md(mistake-registry 裡的大條目也是素材源)→ C-4。**客製 hook**: 學員的「封包先去 ClusterIP」誤解史就是這題的完美模板形狀,錯誤心智模型 → 親手追 iptables 鏈的證據 → 從此先驗機制再下結論。真面試要用工作素材,但敘事骨架先拿這個練。

---

### Q-B-04: Conflict over a technical choice

**適用 phase**: P6
**難度**: senior 必考

**題目 (EN)**: "Tell me about a conflict you had with a teammate over a technical choice. How was it resolved?"

**好答案的形狀**:
- 衝突要具體(兩個方案各是什麼、各自的代價),別退成「我們溝通後就好了」
- 展示你把爭論從立場拉回判準: 先協議「用什麼標準選」(效能?維運成本?rollback 難度?),再讓方案去比
- 有一個降級手段: 時間箱實驗、PoC、找資料,而不是開會互耗
- 結局講事實(選了哪個、後來如何),輸了也可以是好故事

**追問方向**: "What was the other person's strongest argument?" / "If you could redo it, what would you change about how you handled the disagreement, not the decision?"

**素材對接**: story-bank.md → C-4。和 Q-B-02 共用素材時注意角度不同: B-02 主線是你的判斷與勇氣,B-04 主線是化解過程。

---

### Q-B-05: A risky change you shipped safely

**適用 phase**: P6
**難度**: senior 加分題(SRE 面尤其愛問)

**題目 (EN)**: "Tell me about a risky change you had to ship to production. How did you make it safe?"

**好答案的形狀**:
- 先定義風險在哪(blast radius 是什麼、最壞情況長怎樣),證明你 ship 之前就想過失敗
- 安全機制講成一條鏈: staging 演練 → 灰度/canary → 可觀測(盯哪個指標判斷成敗)→ rollback 方案先準備好且演練過
- 至少一個「事前準備真的派上用場」或「主動放棄/延期」的細節,證明機制不是擺設
- 對接 k8s 語彙自然加分: maxUnavailable、PDB、metric gate、git revert(P1/P3/P5 的知識在這題變成敘事材料)

**追問方向**: "What was your rollback trigger, specifically?" / "What would have happened if you did nothing and just YOLO'd it?"(考他能不能量化風險)

**素材對接**: story-bank.md → C-4;P5 的 GitOps/upgrade lab 產出(如 cluster 升級演練)可以直接長成這題的素材。

---

### Q-B-06: Reliability improvement nobody asked for

**適用 phase**: P6
**難度**: senior 訊號題(考 ownership)

**題目 (EN)**: "Tell me about a time you improved reliability or a process proactively, when no ticket or manager asked you to."

**好答案的形狀**:
- 起點是你自己發現的訊號(重複的 toil、驚險的 near-miss、沒人看的告警),不是被指派
- 講清楚你怎麼賣: 用數據或一次具體事故說服團隊值得投資
- 成果可量測: MTTR 降多少、告警量降多少、少了哪類 oncall page
- 主動講機會成本: 為什麼這件事值得擠掉排程內的工作

**追問方向**: "How did you get buy-in?" / "How do you decide which of these side quests are worth your time?"

**素材對接**: story-bank.md → C-4。學員的 k8s 學習本身若在公司落地(例如替 billing 平台補了 PDB 體檢或 runbook),就是這題的現成素材,P3+ 開始留意記錄。

---

## 面試題維度對應 Scorecard

| Scorecard 維度 | 主要對應題目類別 |
|---------------|----------------|
| 能講清楚底層原理 | 原理題(Q-P-*) |
| 理解內部機制 | 原理題 + k8s x SD |
| 能用自己的話解釋 | 全部,但看敘述流暢度 |
| 故障排除速度 MTTR | 故障排除(Q-T-*) |
| 可觀測性設計 | P4 原理題(Q-P-20 ~ Q-P-22)+ Q-T-09 |
| 能定義/解讀 SLO | Q-P-20 + Q-SD-05 的 metric gate 段 |
