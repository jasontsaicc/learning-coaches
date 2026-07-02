# 現實世界場景庫

> **如何使用此檔:** 對應 Teaching Flow C 段的「現實世界這樣做」固定教學元件。
> 每個場景用四段式範本(情境/生產怎麼做/真實踩坑/面試怎麼問)呈現,讓抽象機制接地氣。
> Coach 在 C 段原理講完後,拉出對應場景強化「為什麼面試官問這個」的動機感。
> [RUNTIME: 各場景的公司/人物/數字皆可抽換;若學員 story-bank 有對應的真實事件,優先用他自己的事件講。]

---

## 四段式範本(格式定義)

每個場景固定四段,**按序呈現**:

| 段 | 功能 | 說明 |
|----|------|------|
| **情境** | 開場脈絡 | 一個具體的生產場景,讓學員感受到「這不是玩具題」 |
| **生產怎麼做** | 業界正解 | 實際生產環境的處理方式/標準配置,連結到剛學的機制 |
| **真實踩坑** | 強化記憶的反例 | 這個機制最常見的翻車點,對應 Mistake Registry |
| **面試怎麼問** | 北極星連結 | 面試官會用什麼角度考這個點,對應 interview-bank.md |

使用時可選擇「全部呈現」或「只用情境引入,讓學員猜後三段」(後者適合 Feynman Gate 驗收)。

---

## P0 場景

### S-P0-1: 為什麼要用宣告式/GitOps 心智

**適用 chunk**: C-0 聲明式 vs 命令式

| 段 | 內容 |
|----|------|
| **情境** | 凌晨 2 點,你接到 on-call alert:生產 cluster 的某個 Deployment 只剩 1 個 replica 在跑,但 SLA 要求至少 3 個。你打開 kubectl 一看,replica 確實只有 1 個,但你明明記得昨天設了 3 個。到底發生了什麼? |
| **生產怎麼做** | 生產環境一律採用「Git 是唯一 source of truth」的宣告式管理: 所有 k8s manifest 放 Git repo,透過 ArgoCD 或 Flux 做 GitOps 同步。修改只能 commit 到 Git,由 CD 系統 apply 到 cluster。任何人直接 `kubectl edit` 或 `kubectl scale` 的修改,下次同步時都會被蓋回 Git 的版本。replica 數量只要看 Git 的 `replicas: 3`,就知道「正確答案」。 |
| **真實踩坑** | 有人(可能是你自己)在凌晨處理緊急事件時,用 `kubectl scale deployment --replicas=1` 降流量(命令式操作),解決了當下的問題,但忘記把 Git 的 YAML 也改回來。CD 系統在幾分鐘後同步,看到 Git 說「3 個」,把 cluster 改回 3 個。但如果 CD 同步是 manual 觸發或 interval 很長,這個「暗地裡縮減 replica」的狀態就會持續一陣子,等到 alert 觸發你才發現。根本原因: 命令式操作不留記錄、不 code review、不可 audit trail。 |
| **面試怎麼問** | 「解釋 GitOps 的核心原則是什麼。如果有人直接 `kubectl edit` 改了 production cluster,GitOps 系統會怎麼處理?你覺得這是好事還是壞事?」 |

---

### S-P0-2: Pod Pending 怎麼查

**適用 chunk**: C-3 apply→Running 全流程

| 段 | 內容 |
|----|------|
| **情境** | 你 `kubectl apply -f deployment.yaml` 之後等了 2 分鐘,Pod 還是 Pending。老闆在旁邊看,你要快速找到根因。 |
| **生產怎麼做** | 標準排查路徑(3 步走): (1) `kubectl describe pod <name>` 看 Events 欄位。Events 會告訴你是哪個元件卡住了。(2) 依 Events 的線索分支: Scheduler 輸出「0/N nodes available」→ 看資源/taint/affinity 設定;Admission webhook 相關訊息 → 看 webhook 配置;Image 相關 → 看 registry 設定和 imagePullPolicy。(3) 確認根因後修,再觀察 `kubectl get pod -w` 看狀態轉移。 |
| **真實踩坑** | 踩坑一: resources.requests 設太高,cluster 沒有足夠資源。Events 會顯示 `0/3 nodes are available: 3 Insufficient cpu`。新人常以為是網路問題或 image 問題,其實是 requests 設錯。踩坑二: Admission webhook 的 `failurePolicy: Fail` 加上 webhook 服務掛掉,導致所有 Pod 被拒絕建立。Events 裡有 webhook timeout 訊息。最危險的是這個問題會波及整個 cluster,不只是你的 Pod。修法: `kubectl get mutatingwebhookconfigurations` 找到問題 webhook,暫時 disable 或改 `failurePolicy: Ignore`。 |
| **面試怎麼問** | 「你的 Pod 一直在 Pending 狀態。第一個下的指令是什麼?看到什麼資訊你會往哪個方向查?」(典型 scenario-based 故障排除題,考排查思路的結構性) |

---

## P1 場景

### S-P1-1: 新人把 CrashLoopBackOff 當根因回報

**適用 chunk**: P1-5 資源/QoS/OOM(describe 速查表),也可在 On-call triage drill 前後用

| 段 | 內容 |
|----|------|
| **情境** | 團隊新人在 incident channel 貼:「找到了,根因是 CrashLoopBackOff」,然後開始查「how to fix CrashLoopBackOff」。主管在旁邊 cue 你:「你覺得呢?」PM 在等一個「多久修好」的答案。 |
| **生產怎麼做** | 先講清楚:CrashLoopBackOff 是 kubelet 的重啟退避策略,是「一直死」這個現象的名字,不是死因。標準路徑就是學員已內化的 describe 速查表:`kubectl describe pod` 看 Last State 的 Exit Code + Reason,分四路:OOMKilled/137(撞 cgroup limit)、Error/1(app 自己 crash,接 `kubectl logs --previous` 看上一世遺言)、probe 殺的(Events 有 Liveness probe failed,exit 常是 0 或 SIGTERM)、ImagePull 類另一族。incident report 要寫到 exit code 層級,「根因: CrashLoopBackOff」這種回報在 postmortem review 會被打回票。 |
| **真實踩坑** | 兩個經典:(1) 新人 `kubectl logs` 看到空輸出就說「沒有 log」,不知道容器已重啟、要 `--previous` 才看得到死前輸出。(2) 回報只寫現象,PM 追問「所以要改什麼?」答不出,整個 incident 的信任感就掉了。senior 跟 junior 的差距常常就在:同一個 describe 輸出,一個只唸狀態,一個能指出下一步驗證什麼。 |
| **面試怎麼問** | 「Pod 在 CrashLoopBackOff,你的排查步驟是什麼?」隱藏考點就是你會不會先說「這是現象不是根因」再展開 exit code 分流。答題直接把 describe 速查表講成決策樹就是 senior 答案。 |

---

### S-P1-2: OOMKilled 之後,要不要跟主管要資源

**適用 chunk**: P1-5 資源/QoS/OOM(leak 鋸齒 vs rightsize,學員 session 6 已能分辨,此場景往溝通面加壓)

| 段 | 內容 |
|----|------|
| **情境** | billing 的某個 API 服務每天半夜被 OOMKilled 一次,早上自己恢復。主管問:「把 limit 從 512Mi 調到 1Gi 就好了吧?要不要順便把 node 加大?」加資源就是加成本,這句話你要怎麼接。 |
| **生產怎麼做** | 先拿曲線再開口:`kubectl top` 只有當下值,要看 Prometheus 的 `container_memory_working_set_bytes` 幾天的走勢。兩種形狀兩種答案:鋸齒爬頂(每次重啟歸零、然後單調往上爬到 limit)= memory leak,加 limit 只是把爆炸時間往後延,治標;平台水位貼頂(一開始就穩定在高位)= 需求真的就這麼大,rightsize 調 limit 是治本。跟主管溝通的 senior 格式:曲線截圖 + 兩案成本(加資源 = 每月多少 node 費用、leak 照樣爆只是變慢;修 leak = 後端工程時間)+ 你的建議 + 短期止血(先調大爭取時間,同時開 ticket 修 leak,並講明這是治標)。 |
| **真實踩坑** | 直接調大 limit 收工,兩週後又 OOM,而且更痛:leak 累積更久才死,死的時候 in-flight request 更多。另一坑:只調 limit 沒同步調 requests,QoS 與排程依據沒跟上,node 超賣更兇,換來 node 級驅逐。回扣學員自己的話:「鋸齒爬頂 vs 平台水位」,他在 P1 畢業 drill 已能分 A=leak B=可調大。 |
| **面試怎麼問** | 「服務一直 OOMKilled,把 memory limit 加大就解決了嗎?」考的是治標/治本判斷 + 你怎麼證明是哪一種。追問常是「你怎麼跟不懂 k8s 的主管解釋要不要加資源」,考溝通。 |

---

### S-P1-3: 週五下午的滾動更新卡死

**適用 chunk**: P1-4 Deployment/rollout(學員親手做過 nginx:9.99 壞 image lab,3 好 + 2 壞 = 5 的幾何)

| 段 | 內容 |
|----|------|
| **情境** | 週五 16:30 release,`kubectl rollout status` 停在「2 out of 5 new replicas have been updated」十分鐘不動。後端同事跑來問「是不是 k8s 壞了,線上是不是掛了」,聲音已經開始緊張。 |
| **生產怎麼做** | 第一句話先安撫且是真的:舊 Pod 還活著,線上流量沒斷。這是 maxSurge/maxUnavailable 的幾何保證(學員 lab 親眼看過:replicas=4、surge 1、unavailable 1,壞 image 卡在 3 好 + 2 壞,3 個舊 Pod 全程沒倒)。然後 `kubectl describe pod` 新 RS 的 Pod,看到 ImagePullBackOff,tag 打錯。止血 = `kubectl rollout undo`,秒回,因為舊 RS 還在、只是 scale up,不用重拉 image。事後修流程:image tag 由 CI pipeline 產生不准手打;CD 加 `kubectl rollout status --timeout=300s` 當卡關,並設 `progressDeadlineSeconds` 讓卡死的 rollout 會標成 Failed。 |
| **真實踩坑** | 恐慌操作二連:(1) 對壞 Pod 狂 `kubectl delete pod`,RS 再拉起來還是同一個壞 image,白忙。(2) 更糟的是 delete 整個 Deployment 重建,這才真的把服務打斷,把「沒有影響線上的部署事故」升級成「線上事故」。另一坑:progressDeadlineSeconds 沒設,rollout 永遠卡住不報錯,CD dashboard 綠色,大家以為部署完成,其實新版只上了一半。 |
| **面試怎麼問** | 「rolling update 卡在一半,現有用戶流量會受影響嗎?你怎麼判斷、怎麼止血?」進階追問:「為什麼 rollback 那麼快?」(舊 RS 留著)以及「maxSurge:0 + maxUnavailable:0 會怎樣?」(apply 直接退件,學員學過的死鎖題)。 |

---

### S-P1-4: liveness probe 把健康的服務打掛

**適用 chunk**: P1-3 probe(學員 session 6 drill 親手解過 exit 0 被 probe 殺;thundering herd 是他的術語卡)

| 段 | 內容 |
|----|------|
| **情境** | DB 網路抖了 30 秒。DB 恢復之後,API 服務反而全面 5xx 了十分鐘。事後看 `kubectl get pods`:所有 API Pod 的 RESTARTS 在同一分鐘齊步 +1。翻 code 發現 liveness probe 打的 `/healthz` 裡面會 ping DB。 |
| **生產怎麼做** | 原則一句話:liveness 只回答「這個 process 還活著嗎」,不准檢查依賴;依賴健康(DB、下游 API)放 readiness,fail 了只是從 Endpoints 摘掉不接流量,不殺人。因為 liveness 查 DB 的後果是:DB 抖 → 全部 Pod liveness fail → kubelet 齊殺 → DB 剛恢復就迎來全部 Pod 同時重建 connection pool 的 thundering herd → DB 再倒 → 正回饋循環。學員在 P1 A 段抽考自己講出過這條鏈(reconnection 風暴回壓 DB)。另外調 failureThreshold × periodSeconds 給依賴抖動留緩衝,這是他 probe lab 學過的偵測延遲旋鈕。 |
| **真實踩坑** | 特徵指紋要認得:exit code 0 或 SIGTERM(app 是被優雅賜死的,不是自己 crash)、全部 Pod RESTARTS 同步上升、Events 裡 Liveness probe failed。學員 drill 裡的 web-frontend 就是這型:probe 打 8080、nginx 聽 80,他從 exit 0 反推「app 健康、被 probe 殺」是當時的最佳時刻,此場景是同一把刀的放大版:單 Pod 誤殺 → 全叢集雪崩。 |
| **面試怎麼問** | 「liveness 跟 readiness 差在哪?health check endpoint 該不該檢查資料庫?」以及 scenario 版:「DB 抖 30 秒,服務掛 10 分鐘,可能發生了什麼?」能主動講出正回饋/thundering herd 這層就是 senior 訊號。 |

---

## P2a 場景

### S-P2a-1: 「payment-svc 連不上」的分層排查

**適用 chunk**: P2a-1 Service/kube-proxy/CoreDNS(學員親手追過 KUBE-SERVICES→KUBE-SVC→KUBE-SEP DNAT 鏈)

| 段 | 內容 |
|----|------|
| **情境** | 後端同事丟一句「呼叫 payment-svc 一直連不上,你們網路是不是壞了」就把球踢過來。你要在不重啟任何東西的前提下,十分鐘內定位在哪一層。 |
| **生產怎麼做** | 由上往下分層,每一步只驗證一層:(1) `kubectl get svc payment-svc` + `kubectl get endpoints payment-svc`,Endpoints 空 = selector 打錯或 readiness 沒過(回扣學員 P1 probe lab:rm readiness 後 Pod 從 Endpoints 消失但 RESTARTS 0),八成的案子死在這層。(2) Endpoints 有 IP → 從 client Pod 直接 `curl <PodIP>:<port>` 繞過 Service,測 Pod 本身。(3) PodIP 通、ClusterIP 不通 → 才輪到 kube-proxy/iptables 層:`docker exec <node> iptables-save | grep <svc>` 追 DNAT 鏈(學員 D 段親手追過,worker/worker2 規則一致)。(4) 名字解不出來 → 那是 DNS 層(CoreDNS),跟 NAT 層是兩件事,錯誤訊息會告訴你:could not resolve host = DNS 層,connection refused = 已連到但對方沒聽這個 port,timeout 才輪到懷疑網路。 |
| **真實踩坑** | 最常見根因其實在最上層:Service 的 `targetPort` 跟容器實際聽的 port 對不上,或 selector 的 label 打錯一個字。但人的直覺是先懷疑最神秘的層,跑去重啟 CoreDNS、懷疑 CNI,兩小時後才回頭看 Endpoints 是空的。這正是學員自己的弱點模式(層級混淆:busybox NXDOMAIN 題他曾把 conntrack 拉進 DNS 題),此場景就是那個坑的職場放大版。 |
| **面試怎麼問** | 「Pod A 打 Service B 不通,講你的排查路徑,並且每一步說明你在驗證哪一層。」考的是排查有沒有結構,亂槍打鳥 vs 分層收斂,一聽就分 junior/senior。 |

---

### S-P2a-2: 呼叫外部 API 莫名慢 2 秒:ndots:5 偵探劇

**適用 chunk**: P2a-1 CoreDNS(學員已懂 resolv.conf 由 kubelet 注入、指向 CoreDNS ClusterIP;busybox DNS 坑親手撞過)

| 段 | 內容 |
|----|------|
| **情境** | 後端回報:呼叫第三方支付 API `api.stripe.com`,p50 正常,p99 卻多出 2 到 4 秒,而且只在 k8s 裡發生,同一段 code 在本機跑完全正常。PM 已經開始問「要不要換一家支付供應商」。 |
| **生產怎麼做** | 進 Pod 看 `cat /etc/resolv.conf`:kubelet 注入的不只 nameserver(CoreDNS 的 ClusterIP,學員 Weekly Review 補過這洞),還有 `search default.svc.cluster.local svc.cluster.local cluster.local` 和 `ndots:5`。`api.stripe.com` 只有 2 個點,小於 5,所以 resolver 會先依序試 `api.stripe.com.default.svc.cluster.local`、`api.stripe.com.svc.cluster.local`... 全部吃 NXDOMAIN 之後才查原名,每輪還是 A + AAAA 兩發。平常只是浪費幾發查詢,一旦 UDP 丟包,預設 5 秒 timeout,p99 那 2 到 5 秒就是這裡來的。修法看情境:FQDN 加結尾點 `api.stripe.com.`(直接跳過 search list)、pod `dnsConfig` 把 ndots 調 1 或 2、或叢集級上 NodeLocal DNSCache。 |
| **真實踩坑** | 偵探劇的誤導線:大家先查應用層(TLS handshake?connection pool?),tcpdump 盯半夜。其實看 CoreDNS metrics(`coredns_dns_requests_total`)會發現大量 `.svc.cluster.local` 結尾的 NXDOMAIN 查詢,量是正常的好幾倍,一眼破案。另一條學員親身撞過的支線:busybox/alpine 的 resolver 行為跟 glibc 不同,用 busybox nslookup 驗證 DNS 問題本身就可能誤診。 |
| **面試怎麼問** | 「在 k8s 裡呼叫外部 API 偶爾多 2 到 5 秒,DNS 方向你會查什麼?ndots 是什麼、為什麼預設是 5?」後半題很少人答得出來(因為要讓 `service.ns` 這種短名字能解析,search list 才存在),答出來就是懂原理不是背 workaround。 |

---

### S-P2a-3: default-deny NetworkPolicy 忘了開 DNS egress

**適用 chunk**: P2a-3 NetworkPolicy(注意:kind 預設 kindnet 不支援 NetworkPolicy,lab 要先裝 Calico)

| 段 | 內容 |
|----|------|
| **情境** | 資安稽核要求生產 namespace 上 default-deny。週三晚上 apply 上去,凌晨兩點 on-call 被叫醒:該 namespace 所有服務互叫全掛,錯誤訊息清一色 `could not resolve host`。 |
| **生產怎麼做** | default-deny 之後要逐條開白名單,而第一條永遠是 egress 到 kube-system 的 CoreDNS(UDP/TCP 53)。因為所有服務發現都先過 DNS:名字解不掉,看起來像「全網斷線」,其實只斷了一層。上線流程也有正解:先在 staging 套用、開著 flow 觀察工具(Calico flow logs / Cilium Hubble)跑幾天,確認沒有誤殺的 flow 再上 prod,而且分 namespace 灰度,不要一發全上。 |
| **真實踩坑** | 這題症狀的誤導性極強:錯誤是 DNS 解析失敗,照症狀查會去看 CoreDNS 本身(它好好的),甚至半夜重啟 CoreDNS(學員在 busybox 坑學過的紀律:先用 FQDN 測,測得到就別重啟 CoreDNS)。真正原因在連線層:policy 把「到 DNS server 的封包」擋在出門口。這是學員層級混淆弱點的鏡像題:上次是把連線層拉進 DNS 題,這次是 DNS 症狀、根因在連線層。附帶一坑:在 kindnet 這種不支援 NetworkPolicy 的 CNI 上 apply,policy 默默不生效,你以為有防護其實是裸奔,比報錯更危險。 |
| **面試怎麼問** | 「上了 default-deny 之後全部服務掛掉,錯誤都是 DNS 解析失敗,為什麼?你的第一條 allow 規則會開什麼?」再追:「你怎麼安全地在 prod 導入 default-deny?」考變更管理,不只考語法。 |

---

### S-P2a-4: finance 問「為什麼我們有 12 台 NLB」

**適用 chunk**: P2a-2 Ingress(學員 session 11 自己從 Service type 階梯推出 Ingress 兩個第一性理由:省 LB + L4 到 L7)

| 段 | 內容 |
|----|------|
| **情境** | 月底成本審查,finance 拿著 AWS 帳單問:「這 12 台 NLB 是什麼?一台每月 20 鎂起跳還有 LCU 流量費。」查了一下,是每個微服務各開一個 `type: LoadBalancer`,歷史共業,沒人整理。 |
| **生產怎麼做** | 這正是 Ingress 存在的第一性理由,學員自己推過:N 個服務 = N 台 L4 LB,錢和管理面都線性爆;而且 NLB 是 L4,看不到 URL path(學員自答的最關鍵一刀),想按 path 分流根本做不到。整併方案:1 台 LB 進 Ingress Controller(ingress-nginx 或 AWS ALB Controller),按 host/path 分流到各 Service。遷移是逐服務把 `type: LoadBalancer` 改回 ClusterIP + 加一條 Ingress rule,DNS 逐個切,不是 big bang。跟 finance 回報的格式:現況成本、整併後成本(1 台 ALB + controller 的運算資源)、遷移工時,讓他拿得到數字。 |
| **真實踩坑** | 整併的代價要講清楚:所有服務共享一個入口,Ingress Controller 變成 blast radius,它一掛全部服務入口全掛。所以 controller 本身要多副本、放 PDB、資源給足,別省錯地方。遷移期另一坑:舊 NLB 刪太快,外部 DNS TTL 還指著舊 LB,用戶端斷線,正確順序是先切 DNS、等 TTL 過、觀察舊 LB 流量歸零才刪。 |
| **面試怎麼問** | 「LoadBalancer Service 跟 Ingress 差在哪?什麼時候該用哪個?」senior 版會加成本角度和 blast radius trade-off。誘答彈藥:「apply 了 Ingress 物件流量就會自動分流」,學員 session 11 已反殺過這題(物件=規則,controller=引擎),可拿來冷測。 |

---

## P2b 場景

### S-P2b-1: 新叢集第一顆 PVC 永遠 Pending

**適用 chunk**: P2b 儲存(StorageClass / dynamic provisioning)

| 段 | 內容 |
|----|------|
| **情境** | 新開的 EKS 叢集,第一次部署一個帶 PVC 的服務。Pod Pending,PVC 也 Pending,`kubectl describe pvc` 只淡淡一句 `no persistent volumes available for this claim and no storage class is set`。同一份 manifest 在舊叢集跑得好好的。 |
| **生產怎麼做** | 先 `kubectl get storageclass`:看有沒有名字旁邊帶 `(default)` 標記的。dynamic provisioning 的鏈路是 PVC → StorageClass → provisioner(CSI controller)去雲上開 volume → 綁 PV,又是一個 reconcile loop,跟 `type: LoadBalancer` 由 cloud-controller 去雲上生 LB 是同一個模式(學員 session 11 推過,複利回扣)。EKS 上還有前置:1.23 之後 EBS CSI driver 是要自己裝的 addon,而且 controller 需要 IAM 權限(IRSA)。另外 `WaitForFirstConsumer` 的 Pending 是正常等待(等 Pod 排定 node 才決定 volume 開在哪個 AZ),別誤判成故障,看 describe 訊息分辨。 |
| **真實踩坑** | 兩個具體坑:(1) EKS 沒裝 EBS CSI driver,PVC 永遠 Pending,錯誤訊息不會直說「你沒裝 driver」,新叢集初始化 checklist 漏這項很常見。(2) StorageClass 存在但沒有 `storageclass.kubernetes.io/is-default-class: "true"` annotation,manifest 又沒寫 `storageClassName`,兩邊互等。反向坑:兩個 SC 都標 default,不同版本行為不同,依賴 default 本身就是脆弱設定,生產 manifest 應明寫 storageClassName。 |
| **面試怎麼問** | 「PVC 一直 Pending,你會查哪些東西?從 PVC 到雲上真的長出一顆 EBS volume,中間的鏈路是什麼?」考你是背 kubectl 指令還是懂 provisioning 的 reconcile 鏈。 |

---

### S-P2b-2: 上線前夜的 403,同事說「給 cluster-admin 不就好了」

**適用 chunk**: P2b RBAC(最小權限的職場拉扯)

| 段 | 內容 |
|----|------|
| **情境** | 新服務明天上線,今晚整測時 log 噴 `configmaps is forbidden: User "system:serviceaccount:payments:default" cannot list resource "configmaps"`。後端同事說:「上次那個服務也是這樣,直接綁 cluster-admin 五分鐘搞定,先上線再說。」deadline 壓著,你要當場做決定。 |
| **生產怎麼做** | 技術上正解很小:建專屬 ServiceAccount(別用 default SA),開一個 Role(resources: configmaps,verbs: get/list/watch)+ RoleBinding,限在該 namespace,用 `kubectl auth can-i list configmaps --as=system:serviceaccount:payments:payment-api` 驗證,前後十五分鐘。職場拉扯的正面回法:cluster-admin 不是快,是把風險記在別人帳上,服務一旦被打穿等於整個 cluster 淪陷,資安稽核也過不了,到時回頭拆權限的成本遠大於今晚這十五分鐘。senior 的系統性解法是把最小權限做成 template/module,讓「做對」跟「圖方便」一樣便宜,下個服務就不會再吵這題。 |
| **真實踩坑** | 403 的錯誤訊息其實把答案寫在臉上:哪個 SA、哪個 verb、哪個 resource、哪個 API group,全都在那一行裡,但新人常跳過去查網路、查 Service。另一坑:所有 Pod 都用 namespace 的 default SA,你給 default SA 開權限,等於整個 namespace 的 Pod 都拿到,權限邊界名存實亡。還有 Role 與 ClusterRole 綁錯範圍,cluster-scoped 資源(node、PV)用 Role 開永遠 403。 |
| **面試怎麼問** | 「一個服務需要讀 Secret,你怎麼設計 RBAC?」以及 behavioral 混合版:「同事說給 cluster-admin 比較快,你怎麼回?」考 least privilege 原則加上你能不能在 deadline 壓力下守住底線又不擋人上線。這題對學員是弱點正中(覺得怪怪的但被同事帶走的職場模式),可搭配誘答演練。 |

---

### S-P2b-3: IRSA token 拿不到,但隔壁舊服務「好好的」

**適用 chunk**: P2b IRSA / Pod 身分(對照 node instance role 的安全債)

| 段 | 內容 |
|----|------|
| **情境** | 新服務要上傳 S3,在 EKS 上一直 `AccessDenied`。詭異的是同一台 node 上的舊服務上傳同一個 bucket 完全正常。後端說「那就照舊服務的設定抄一份」,但你查了舊服務,它的 SA 什麼 annotation 都沒有。 |
| **生產怎麼做** | 先揭穿「舊服務好好的」的真相:它靠的是 node instance role,整台 node 上任何 Pod 都共享那組 AWS 權限,這是安全債不是設定範本。IRSA 的鏈路:SA 加 annotation `eks.amazonaws.com/role-arn` → EKS 的 mutating webhook 在 Pod 建立時注入 projected token 和環境變數(AWS_ROLE_ARN、AWS_WEB_IDENTITY_TOKEN_FILE)→ SDK 用 token 打 STS AssumeRoleWithWebIdentity 換臨時憑證。排查三步:`kubectl describe sa` 看 annotation、exec 進 Pod 看那兩個 env 和 `/var/run/secrets/eks.amazonaws.com/` 有沒有 token、IAM role trust policy 的 OIDC condition 裡 `sub` 是否精確等於 `system:serviceaccount:<ns>:<sa>`。 |
| **真實踩坑** | 最常見:annotation 加了但 Pod 沒重建。token 注入是 admission webhook 在 Pod 建立當下做的,對已在跑的 Pod 補 annotation 不會生效,要 rollout restart。第二名:trust policy 的 sub 寫錯 namespace 或 SA 名,STS 回 AccessDenied 但訊息很隱晦。長期的痛:當你開始收斂 node role 權限(還安全債),會陸續有服務莫名壞掉,因為它們多年來偷偷依賴 node role,從來沒人宣告過這個依賴。 |
| **面試怎麼問** | 「EKS 上 Pod 要存取 AWS API,有哪幾種給權限的方式?為什麼 node instance role 是反模式?IRSA 底層怎麼運作?」最後一問要能講到 OIDC + projected token + STS,這是 senior 跟「會抄 annotation」的分水嶺。 |

---

## P3 場景

### S-P3-1: 行銷活動 10 點開跑,HPA 10 點 05 分才醒

**適用 chunk**: HPA / capacity planning

| 段 | 內容 |
|----|------|
| **情境** | 行銷部禮拜三在群組丟一句「明天早上 10 點發 push notification,預計百萬用戶」。你想:有 HPA,沒事。隔天 10:00 流量瞬間十倍,10:00 到 10:05 之間錯誤率 8%,10:05 之後 HPA 擴出來的 Pod 才陸續接住流量。事後 PM 問:「我們不是有自動擴容嗎?」 |
| **生產怎麼做** | 把「HPA 從偵測到接客」的延遲鏈攤開:metrics 抓取間隔 + HPA sync 週期 + stabilization + 排程 + 開新 node(分鐘級)+ 拉 image + readiness。對可預期尖峰,標準做法是主動式:活動前 30 分鐘手動或排程把 replicas 拉到預估值(或用 CronJob 改 HPA minReplicas),HPA 只負責收尾和意外加碼。搭配 image 預拉與 overprovision placeholder Pod 縮短 node 冷啟動。 |
| **真實踩坑** | 團隊把 HPA target CPU 從 50% 調到 30% 想「更靈敏」,結果平時 replicas 多一倍(成本翻倍),尖峰照樣慢 5 分鐘,因為瓶頸根本不在閾值,在延遲鏈的結構(反應式系統天生慢半拍)。另一坑:壓測時 requests 設太低,HPA 看到的 CPU% 分母失真,擴容數量全錯。 |
| **面試怎麼問** | 「已知明天有 10 倍流量尖峰,你怎麼設計?」只答 HPA 的是 mid-level;senior 會分「可預期用主動式、不可預期用反應式」,並能講出 scale-up 延遲鏈的每一段。 |

---

### S-P3-2: 財務要砍 30% 成本,spot 上線第一週就驅逐潮

**適用 chunk**: taints / topologySpread / PDB

| 段 | 內容 |
|----|------|
| **情境** | 主管拿著 AWS 帳單說 node 成本要降三成,你把一半 workload 搬上 spot instance。第一週某天下午 AWS 回收了同一個 AZ 的一批 spot,backend 六個副本瞬間死四個,剩兩個被流量壓到 OOM,雪崩 20 分鐘。 |
| **生產怎麼做** | spot 是拿「隨時被收走」換折扣,防禦要一起買:topologySpreadConstraints 把副本打散到多 AZ / 多 node group;關鍵服務保底副本放 on-demand(用 nodeAffinity 分層);PDB 設下限;Karpenter/CA 對 spot 中斷訊號(2 分鐘警告)提前補機。成本會議上你要能講「省 30% 的代價是需要這四道防禦,工程成本大約 X」。 |
| **真實踩坑** | 只搬 workload 不做打散,六個副本被 bin packing 塞在同一台便宜大機上,一次回收全滅。另一坑:PDB minAvailable 設太高(=副本數),spot 回收時 eviction 全被擋,結果不是優雅遷移而是 2 分鐘後被硬拔,比沒有 PDB 更慘。 |
| **面試怎麼問** | 「你會怎麼在 k8s 上安全地用 spot instance 省成本?」考的是可用性與成本的取捨設計,senior 訊號是主動講出 blast radius 控制(打散 + 分層 + 預警處理)。 |

---

### S-P3-3: 一個 Pod 死掉,五分鐘後整個服務死掉

**適用 chunk**: OOM 雪崩 / capacity headroom

| 段 | 內容 |
|----|------|
| **情境** | 深夜 on-call,告警:backend 一個副本 OOMKilled。你想「會自己回來」就繼續睡。十分鐘後全服務 5xx:剩餘副本接手死者的流量後記憶體也撞頂,一個接一個 OOMKilled,重啟回來又立刻被壓死。RESTARTS 像跳表一樣漲。 |
| **生產怎麼做** | 認出這是正回饋雪崩,止血目標是「打斷迴路」:立刻 scale up 稀釋每副本負載(新 Pod 起得來,因為它們分到的流量較小),必要時在入口降級/限流。絕不在雪崩中改 limit:那會觸發滾動重建,把僅存容量再砍一刀。事後用 N-1 原則重算容量:任何一個副本死掉,剩下的仍在安全水位。 |
| **真實踩坑** | 值班的人看到 OOMKilled 就反射性調大 memory limit 然後 apply,滾動重建讓可用副本瞬間更少,雪崩加速。另一坑:HPA 是看 CPU 的,這場雪崩瓶頸在 memory,HPA 全程沒動,「有 HPA 就不會雪崩」是錯覺。 |
| **面試怎麼問** | 「服務發生連鎖 OOM,你先做什麼?」考止血順序與正回饋的識別;追問「為什麼不先調 limit」直接分出有沒有真的處理過雪崩。 |

---

### S-P3-4: 維護窗口三小時,drain 卡在第一台就過不去

**適用 chunk**: PDB / drain / 變更管理

| 段 | 內容 |
|----|------|
| **情境** | 週末凌晨的核准維護窗口,要滾動重開 12 台 node 打 kernel patch。第一台 `kubectl drain` 就掛著不動:某團隊的服務 3 副本、PDB minAvailable: 3,eviction 永遠被拒。窗口三小時,照這速度天亮也做不完,而那個團隊沒人接電話。 |
| **生產怎麼做** | drain 前先體檢:`kubectl get pdb -A` 掃 ALLOWED DISRUPTIONS 為 0 的服務,提前協調(加副本讓 PDB 有預算,或該團隊簽核短時降級)。制度面:平台規範 PDB 必須留至少 1 個 disruption 預算(minAvailable < replicas),CI 對「預算為零」的 PDB 擋下或告警。維護 SOP 裡寫明卡住時的 escalation 路徑與授權(誰可以決定強制繼續)。 |
| **真實踩坑** | 用 `--disable-eviction` 或直接刪 Pod 硬幹繞過 PDB,結果那個服務其實是有狀態的,瞬間跌破 quorum,把「合規的維護」變成「自製的事故」。PDB 擋你,通常是它在替一個你不了解的服務工作。 |
| **面試怎麼問** | 「drain 被 PDB 卡住,你怎麼處理?」mid-level 答技術繞法;senior 先問「這個 PDB 在保護什麼」,並談維護前置檢查與跨團隊協調,這題一半是考組織能力。 |

---

## P4 場景

### S-P4-1: SLO 設 99.99,兩週後沒人理告警了

**適用 chunk**: SLI/SLO / Error Budget

| 段 | 內容 |
|----|------|
| **情境** | 新來的主管說「我們要世界級可靠性」,availability SLO 從 99.9 拉到 99.99。error budget 從每月 43 分鐘變 4.3 分鐘,一次普通的 deploy 抖動就燒光。第三週開始 burn rate 告警天天響,on-call 從緊張變麻木,真正的故障混在裡面沒人看。 |
| **生產怎麼做** | SLO 用數據談不用形容詞談:先量現狀(過去 90 天實際 availability)、問使用者感知(billing 的客戶分得出 99.9 和 99.99 嗎?)、算成本曲線(多一個 9,架構費用大約 10 倍:多 region、去單點、演練)。SLO 是產品決策,由工程與 PM 用 error budget 的語言協商:「budget 燒完就凍結 feature 發版,你要這個交換嗎?」告警用 multi-window burn rate,不用單點閾值。 |
| **真實踩坑** | 把 SLO 當 KPI 拿去考核,團隊開始不敢發版(發版是 budget 最大消耗者),交付速度掉一半,可靠性沒變好,這是 error budget 設計初衷的完全反面:budget 存在就是要被花的,花在有價值的變更上。 |
| **面試怎麼問** | 「PM 要求 99.99% availability,你怎麼回應?」senior 訊號:不直接答應也不直接拒絕,用成本曲線 + 使用者感知 + error budget 談判,把「要幾個 9」變成商業決策。 |

---

### S-P4-2: 後端說「我的服務 p50 只有 20ms」,但用戶就是覺得慢

**適用 chunk**: tracing / p99 排查

| 段 | 內容 |
|----|------|
| **情境** | 客服回報結帳偶爾轉圈 3 秒。你問後端,每個團隊都拿自家 dashboard 自證清白:API gateway p50 18ms、orders 22ms、billing 31ms。單看都很快,用戶就是慢。會議開了兩次,大家開始互相懷疑對方的監控。 |
| **生產怎麼做** | 平均數自證清白是經典陷阱,慢藏在 p99 和「串聯放大」裡:一個請求串五個服務,每個 p99 300ms,湊齊的機率不低。正解是抓一條真實慢請求的 trace(用 trace ID 從 gateway 一路看 waterfall),延遲在哪個 span、是 server 處理慢還是兩個 span 之間的 gap(網路/佇列/連線池等待)。tail sampling 設定「latency > 1s 必留」,慢請求永遠有 trace 可查。 |
| **真實踩坑** | trace 在某個服務斷鏈(它沒傳 traceparent header),waterfall 到一半變黑洞,排查卡死。context propagation 是 tracing 的生命線,一個中間服務忘了傳,整條鏈作廢。第二坑:只看 p50/p99 純數字不看分佈,雙峰分佈(快取命中 vs 未命中)被平均數完全遮蔽。 |
| **面試怎麼問** | 「每個服務的監控都正常,但整體 p99 很差,怎麼查?」考分位數的組合效應與 trace 實戰;追問「span 之間的 gap 代表什麼」分辨有沒有真的讀過 waterfall。 |

---

### S-P4-3: 告警一天 200 條,真故障來的那天沒人點開

**適用 chunk**: 告警工程

| 段 | 內容 |
|----|------|
| **情境** | 接手一個老系統,Slack 告警頻道一天 200 條,大家都靜音了。某天資料庫連線池耗盡,告警確實發了,混在 200 條裡,45 分鐘後才有人發現,是客戶先打電話進來的。postmortem 上主管問:「為什麼有告警還漏?」你知道真正的答案是:告警太多等於沒有告警。 |
| **生產怎麼做** | 告警減法(Via Negativa 的實戰):盤點 30 天內每條 rule 的觸發次數與「觸發後有人採取行動的比例」,行動率趨近零的告警砍掉或降級成 dashboard/ticket。page 只留 symptom-based(用戶正在受影響:SLO burn rate、入口錯誤率),cause-based(CPU 高、磁碟 80%)全部降級。每條 page 必附 runbook 連結,做不到就不配當 page。 |
| **真實踩坑** | 砍告警時遇到「這條當年抓過一次事故」的阻力,誰都不敢刪,告警只增不減。解法是拿數據說話:這條 rule 三年觸發 400 次、其中 399 次無行動,留著它的代價是每天訓練大家忽略告警頻道。另一坑:砍完沒建 SLO-based 告警就真的瞎了,減法要跟 symptom-based 重建一起做。 |
| **面試怎麼問** | 「你接手一個告警疲勞嚴重的系統,怎麼改善?」senior 訊號:有具體的審計方法(行動率)、敢砍、並用 symptom-based + runbook 重建,而不是「調整閾值」這種和稀泥答案。 |

---

## P5 場景

### S-P5-1: 半夜救火手改了 prod,早上 ArgoCD 把火點回來

**適用 chunk**: ArgoCD / GitOps 紀律

| 段 | 內容 |
|----|------|
| **情境** | 凌晨兩點下游壅塞,值班同事 `kubectl scale --replicas=1` 降載止血,回去睡了。早上九點 ArgoCD 定時 sync,看 Git 說 replicas: 6,盡責地把它調回去,下游瞬間再次被打爆。第二次事故的根因,是第一次事故的修復。 |
| **生產怎麼做** | GitOps 的鐵律:cluster 不是事實,Git 才是,任何手改都活不過下一次 sync。緊急手改可以(先救人),但 SOP 必須包含「止血後 15 分鐘內回填 Git」(哪怕是一個 hotfix commit 直接 push main)。auto-sync + selfHeal 的環境更嚴格:手改幾分鐘內就被蓋回,救火只能走 Git 或暫停該 app 的 sync(`argocd app set --sync-policy none`),事後恢復。 |
| **真實踩坑** | 團隊剛導入 ArgoCD 時最常見的信任危機就是這種「系統自己把設定改回去了」的鬼故事,被當成 ArgoCD 的 bug 回報。其實是舊習慣(kubectl 直改)撞上新契約(Git 是唯一事實)。導入期要配 drift 告警而不是靜默 selfHeal,讓每次手改都被看見、被討論,習慣才換得過來。 |
| **面試怎麼問** | 「GitOps 環境下怎麼處理緊急手動變更?」考的是紀律與現實的折衷;senior 能講出「先止血、立刻回填、必要時暫停 sync」的完整流程,以及 selfHeal 開關的取捨。 |

---

### S-P5-2: webhook 掛了,整個 cluster 連 Pod 都建不出來

**適用 chunk**: admission webhook / fail-closed

| 段 | 內容 |
|----|------|
| **情境** | 安全團隊上了一個 image 掃描的 validating webhook(failurePolicy: Fail)。某天它依賴的掃描服務掛了,從那一刻起全 cluster 所有 Pod 建立/更新被拒,包括 HPA 擴容、node 故障後的重建、甚至你想部署修復用的工具。告警雪片般飛來,每個團隊都以為是自己的問題。 |
| **生產怎麼做** | 認出指紋:多團隊同時回報「建不了 Pod」+ 錯誤訊息都是 `failed calling webhook`,直指 admission 層。止血第一,不是修 webhook:`kubectl get validatingwebhookconfigurations` 找到兇手,patch failurePolicy=Ignore 或暫時刪除 configuration,先讓叢集恢復呼吸,再修掃描服務。 |
| **真實踩坑** | webhook 的 namespaceSelector 沒排除 kube-system 和它自己的 namespace:掃描服務想自我重啟時,也被自己的 webhook 擋下,完美的自鎖。fail-closed 的安全元件必須 HA 部署 + PDB + 排除自救路徑,否則它就是全叢集寫入路徑上的隱形單點。postmortem 的重點不是「掃描服務為什麼掛」,是「單一元件為什麼有能力凍結整個 cluster」。 |
| **面試怎麼問** | 「全 cluster 突然建不了任何 Pod,排查思路?」senior 會很快切到 admission 層(因為爆炸半徑是「所有寫入」);追問 failurePolicy 的取捨可以分出誰真的設計過 webhook。 |

---

### S-P5-3: cluster 升級後,一半的 Ingress 無聲消失

**適用 chunk**: cluster upgrade / API deprecation

| 段 | 內容 |
|----|------|
| **情境** | EKS 從舊版升級(拖了太久不得不升,跨過移除 v1beta1 的版本線)。control plane 升級一鍵完成,看起來風平浪靜。兩小時後陸續有服務對外 404:所有還用 `networking.k8s.io/v1beta1` 寫的 Ingress 在新版 API Server 眼裡不存在,GitOps repo 裡的 YAML apply 也開始報錯。而 EKS control plane 升級不可逆,沒有回頭路。 |
| **生產怎麼做** | 升級是專案不是按鈕:先跑 API deprecation 掃描(`kubectl-convert`、pluto、kube-no-trouble)盤出所有將被移除的 API 使用者,全部遷完才動手。順序鐵律:control plane 先、node 後,版本 skew 不超過官方支援範圍;addon(CNI/CoreDNS/kube-proxy)相容性矩陣逐一核對。生產前先在 staging 叢集全程彩排,大版本用藍綠 cluster(新叢集就緒後切流量)換取可回退性。 |
| **真實踩坑** | 「拖延升級」本身就是最大的坑:一次跨兩三個版本,deprecated API、addon 相容性、CNI 行為變化全部疊在同一晚爆發,排查時分不清哪個變化造成哪個故障。小步快跑(每季一版)讓每次升級的變化量可控,這是把「大爆炸風險」攤平成「例行維運」。 |
| **面試怎麼問** | 「你怎麼規劃生產 k8s 叢集的版本升級?」幾乎是 senior 必考題;訊號在於有沒有 deprecation 掃描、skew policy、staging 彩排、回退策略這套完整流程,而不是「就點升級然後觀察」。 |
