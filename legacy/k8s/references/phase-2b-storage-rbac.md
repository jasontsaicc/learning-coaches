# P2b: 儲存與權限 (Storage + RBAC + IRSA + Secrets)

> **如何使用此檔:** 這是 P2b 階段的教學素材庫,供 coach 在 C 段(核心原理)讀取並改編。
> 不要逐字唸稿,依學員反應選擇要深挖哪個切面。這是彈藥庫,不是逐字稿。
> 每個 chunk 對應一個 Simon Method 的原子單位,通過 Feynman Gate 後再往下走。
> 學員已畢業:P0(五棒 control flow)、P1(container 本質/probe/rollout/QoS-OOM)、P2a(Service/kube-proxy/DNAT/conntrack/CoreDNS/Ingress)。
> 本檔大量回扣這些既有資產,標注處請務必用學員自己的原話與 lab 經驗當錨點。
> `[RUNTIME: ...]` 標記處依 mistake-registry 與學員當下狀態現場客製。

---

## P2b 學習藍圖

**目標**: 把「跑起來的 Pod」升級成「有狀態、有身分、權限剛好」的生產工作負載。

**P2b 中心問題**: Pod 是無狀態且不可信的:狀態放哪?權限怎麼給到剛好?

前半句接 P1(container = 一個被 namespace/cgroup 圈起來的 process,死了什麼都沒了),
後半句接 P0(API Server 三道關卡的第二關 authz,當時只點名沒打開)。P2b 就是把這兩個尾巴收掉。

**學習路徑(Simon 切塊)**:

| Chunk | 主題 | 核心問題 | Keystone |
|-------|------|---------|----------|
| C-1 | Volume / PV / PVC | 容器死了,資料為什麼會消失?怎麼讓它活下來? | |
| C-2 | StorageClass + CSI | 誰在「自動生出」磁碟?為什麼需要標準介面? | |
| C-3 | StatefulSet 儲存視角 | 為什麼資料庫不能用 Deployment 跑? | |
| C-4 | RBAC | 權限怎麼給到剛好,不多不少? | ⭐ |
| C-5 | IRSA | Pod 怎麼安全地拿到 AWS 權限? | ⭐(EKS 面試必考) |
| C-6 | Secrets + Pod Security | 機密怎麼存?Pod 怎麼被限制住? | |

**環境前置**: `scripts/lab-cluster.sh up p2b`(或沿用現有叢集)。
**安全鐵律**: 每個 lab 第一條指令都是 `kubectl config current-context`,必須看到 `kind-k8s-coach-p0` 才准 apply。機器上有公司 PROD EKS kubeconfig,這條不可省略。

---

## C-1: Volume / PV / PVC (狀態放哪?)

### 核心概念

先用 P1 的複利資產開場,讓學員自己推:

引導問題:「P1 你說過 container 是什麼?(一個被圈起來的 process)那 process 死掉,它寫在自己檔案系統裡的檔案去哪了?」

答案鏈:container 的可寫層(rootfs 上層)生命週期跟著 container。container 被 OOMKill、被 probe 殺、rollout 換掉,可寫層直接蒸發。這不是 bug,是 image 分層設計的本意:image 唯讀共用,每個 container 拿一層薄薄的可寫層。**所以「狀態」天生不能放 container 檔案系統。**

三層階梯(由短命到長命):

```
container 可寫層   活得跟 container 一樣短 (restart 就沒)
      |
   emptyDir       活得跟 Pod 一樣長 (container 重啟還在,Pod 刪了就沒)
      |
   PV (真磁碟)     活得比 Pod 長 (Pod 死了資料還在,新 Pod 接回來)
```

**PV/PVC 的解耦設計**(這是本 chunk 的靈魂):

- **PVC (PersistentVolumeClaim)**: 使用者(app team)宣告需求:「我要 10Gi、ReadWriteOnce」。不關心是 EBS 還是 NFS。
- **PV (PersistentVolume)**: 管理員(或系統)供給的一塊真磁碟的抽象。
- 生活比喻:PVC 是「租屋需求單」(兩房、近捷運),PV 是「房源」,binding 是「仲介配對」。房客不需要知道房子是誰蓋的。
- 這和 Pod/Node 的關係同構:你宣告 Pod 規格,scheduler 幫你配 Node。宣告需求 vs 供給資源的解耦,k8s 到處都是這個模式。

**Binding 是誰做的?** 又是 controller。PV controller 跑 reconcile loop:watch 到 Pending 的 PVC,找容量、accessModes、storageClassName 都匹配的 PV,把兩者互相寫上對方的名字(一對一綁定)。回扣 P0:學員 P0 原話「比對現有環境進行更新」,這裡是第 N 次見到同一個引擎。可以反問:「PVC 從 Pending 變 Bound,你猜背後是什麼機制?」讓他自己說出 reconcile。

### 動手觀察 (kind)

```bash
kubectl config current-context   # 必須是 kind-k8s-coach-p0
```

學員自己寫 YAML(給規格不給全文):

1. PV:1Gi、hostPath `/tmp/pv-demo`、`storageClassName: manual`、accessModes ReadWriteOnce
2. PVC:請求 500Mi、`storageClassName: manual`
3. `kubectl get pv,pvc` 看 STATUS 從 Available/Pending 變 Bound(注意:1Gi 的 PV 配 500Mi 的 PVC 也會綁,binding 是「找到夠大的」不是「剛剛好的」)
4. Pod 掛這個 PVC 到 `/data`,`kubectl exec` 進去寫一個檔
5. 刪掉 Pod,起一個新 Pod 掛同一個 PVC,檔案還在。**這一刻就是「狀態活得比 Pod 長」的實體證明。**

進 node 看底層(仿 P2a 追 iptables 的玩法):

```bash
kubectl get pod <pod> -o jsonpath='{.metadata.uid}'
docker exec k8s-coach-p0-worker ls /var/lib/kubelet/pods/<uid>/volumes/
docker exec k8s-coach-p0-worker findmnt | grep pv-demo
```

### 打穿底層 (First-Principles Dive)

**Pod 掛 volume,底層是 mount namespace + bind mount。**

P1 學過:container 有自己的 mount namespace,所以它「看到的檔案系統」和 host 不同。volume 掛載的機制是:

1. kubelet 在 **host** 上準備好目錄(`/var/lib/kubelet/pods/<uid>/volumes/...`),雲盤的話先 attach 再 mount 到這裡
2. 建 container 時,runtime 把這個 host 目錄 **bind mount** 進 container 的 mount namespace 指定路徑
3. bind mount = 同一塊 inode 資料出現在兩個路徑上,不是複製。container 死掉只是 mount namespace 消失,host 上那個目錄和資料原封不動

所以「volume 讓資料活下來」的第一性原理是:**資料根本不在 container 裡,一直都在 host(或雲盤)上,container 只是透過 bind mount「看見」它。**

這也解釋了為什麼 volume 定義在 Pod 層(`spec.volumes`)、掛載在 container 層(`volumeMounts`):同 Pod 的多個 container 可以 bind mount 同一個來源,這就是 sidecar 共享檔案的機制(回扣 P1 Pod 存在的理由:共享)。

**遷移題**: 「`docker run -v /host/path:/container/path` 和 k8s 的 volume,底層是同一個機制嗎?那 PV/PVC 多出來的那層抽象,解決了 docker -v 的什麼問題?」
(答案方向:同樣是 bind mount;多出來的是「需求與供給解耦」+ 生命週期管理 + 跨 node 的雲盤 attach,docker -v 把 host 路徑寫死在指令裡,換機器就爆,和 Pod IP 寫死必爆是同一類問題。)

### 誘答彈藥

- 「PVC 容量寫 500Mi,Pod 寫超過就會像 memory limit 一樣被 kill 掉。」
  (錯。回扣 P1 QoS/OOM 打層級混淆:memory limit 是 cgroup,超過是 kernel 殺 process;PVC 容量主要是 binding/供應的依據,寫滿磁碟得到的是 `ENOSPC` 寫入錯誤,process 不會被殺。local-path 這種 provisioner 甚至完全不強制配額。學員的層級混淆弱點正好往這打:cgroup 層 vs filesystem 層。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | billing 平台要跑一個需要落盤的元件(例如自建 Redis 或上傳暫存) |
| **生產怎麼做** | 幾乎不手建 PV。app team 只寫 PVC,由 StorageClass 動態供應(下一 chunk)。手建 PV 只出現在接既有 NFS/舊磁碟的場景 |
| **真實踩坑** | Pod 卡 `ContainerCreating`,describe 看到 `FailedMount`/`FailedAttachVolume`。常見根因:PVC 還在 Pending 沒綁上、或 RWO 卷已被另一個 node 上的 Pod 佔住(EBS 一次只能 attach 一台 node)。回扣 P0 symptom→棒次地圖:ContainerCreating = kubelet 段,volume 就是其中一種卡法 |
| **面試怎麼問** | 「PV 和 PVC 為什麼要拆成兩個物件?一個不行嗎?」(考解耦設計:使用者關心需求,管理員關心供給,和 Pod/Node 分工同構) |

**Say it in English**: "A volume is just a host directory bind-mounted into the container's mount namespace, so the data outlives the container."

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| bind mount | /baɪnd maʊnt/ | Making the same directory visible at another path without copying data | 同一塊資料掛到第二個路徑,volume 掛載的底層機制 |
| PersistentVolumeClaim | /pərˈsɪs.tənt ˈvɒl.juːm kleɪm/ | A user's request for storage, decoupled from how it is provided | 使用者的儲存需求單,不管磁碟從哪來 |

---

## C-2: StorageClass 動態供應 + CSI

### 核心概念

C-1 的問題:手建 PV 表示每次 app team 要磁碟,都得等管理員先去開一顆。100 個團隊怎麼辦?

**StorageClass = 儲存的「型錄」**:管理員定義一次「這種等級的磁碟怎麼生」(用哪個 provisioner、什麼參數、gp3 還是 io2),之後 PVC 只要指名型錄,磁碟自動生出來。

**誰生的?provisioner,而它又是一個 controller。**

這裡直接回扣學員 session 11 的高光時刻:他講 `type: LoadBalancer` 時把 provisioner 答成「controller」,當時判半對,因為 cloud-controller 就是跑 reconcile loop 去雲上生 LB。動態供應一模一樣:external-provisioner watch 到「指名我這個 StorageClass 的 Pending PVC」,呼叫後端(EBS API、local-path)創建磁碟,做出對應的 PV,綁定。

**把 P2a 的三合一對照表擴成四合一**(學員自己定型過前三行):

| 規則(資料) | 引擎(執行者) |
|------------|--------------|
| Service | kube-proxy 寫 iptables |
| type: LoadBalancer | cloud-controller 去雲上生 LB |
| Ingress 物件 | Ingress Controller (nginx Pod) |
| **StorageClass + PVC** | **CSI provisioner 去生磁碟** |

同一個問題可以再考一次(他 P2a 秒殺過的誘答變體):「apply 一個 PVC,磁碟就自動長出來嗎?」答案結構完全同構:物件只是宣告,要有引擎在跑才會動。kind 裡的引擎是 `local-path-provisioner`,EKS 裡是 EBS CSI driver(不裝 addon,PVC 永遠 Pending,這是 EKS 新手最常撞的牆)。

**CSI:為什麼要標準介面?**

歷史:早期每家儲存廠商的 driver 寫死在 k8s 核心程式碼裡(in-tree),後果:k8s 發版被廠商 bug 綁架、廠商修 driver 要等 k8s 發版、核心程式碼越長越肥。解法是把「k8s 如何操作儲存」定義成一組標準 gRPC 介面,driver 搬出去自己活(out-of-tree),誰實作這組介面誰就能接上。

**k8s 三大外掛介面(必背,senior 面試常考「k8s 的擴展性設計」)**:

| 介面 | 管什麼 | 誰在呼叫 | 實作例 |
|------|--------|---------|--------|
| CRI | 怎麼跑 container | kubelet | containerd, CRI-O |
| CNI | Pod 怎麼拿 IP、怎麼互通 | kubelet(建 Pod 時) | kindnet, Calico, VPC CNI |
| CSI | 磁碟怎麼生/掛/卸 | kubelet + controller | EBS CSI, local-path |

CRI 是 P0 術語卡舊識;CNI 是 P2a 拆過的誤會(CNI 管 Pod 真實 IP,不管 ClusterIP)。三者的共同設計哲學:**k8s 核心只定義介面和期望狀態,把「跟真實世界打交道」外包出去。** 這就是它能同時活在 AWS/GCP/地端的原因。

CSI driver 的標準長相(概念即可,不用背):controller plugin(集中跑,呼叫雲 API 開磁碟/attach)+ node plugin(DaemonSet,每台 node 跑,負責本機 mount)。對照 kube-proxy 也是每台 node 一份的去中心化模式。

### 動手觀察 (kind)

```bash
kubectl config current-context   # kind-k8s-coach-p0
kubectl get storageclass
# 預期: standard (default), provisioner=rancher.io/local-path, VolumeBindingMode=WaitForFirstConsumer
```

1. 學員寫一個 PVC 指名 `storageClassName: standard`(或不寫,吃 default),apply
2. `kubectl get pvc` 卡 **Pending**!describe 看到 `waiting for first consumer to be created before binding`
3. 引導問題:「磁碟為什麼故意不先生出來?」(見下方 WaitForFirstConsumer)
4. 起一個 Pod 掛它,幾秒內 PVC 變 Bound,`kubectl get pv` 看到自動生出來的 PV
5. 看引擎本人:`kubectl -n local-path-storage logs deploy/local-path-provisioner` 能看到它接單開磁碟的日誌
6. 刪 PVC,PV 跟著消失(reclaimPolicy: Delete)

### 打穿底層 (First-Principles Dive)

**WaitForFirstConsumer 存在的理由是「拓撲」,這題直通 EKS 生產。**

EBS 磁碟是 **AZ 級資源**:開在 us-east-1a 的卷只能 attach 給 1a 的 node。如果 PVC 一 apply 就立刻開卷(Immediate 模式),卷可能開在 1a,然後 scheduler 把 Pod 排去 1b 的 node,永遠掛不上。WaitForFirstConsumer 把順序反過來:先讓 scheduler 決定 Pod 去哪,再在同一個 AZ 開卷。**儲存供應必須知道調度結果,所以要等。**

這是一個分散式系統的通用課題:兩個資源分配器(scheduler 排 Pod、provisioner 開卷)各自最佳化會打架,解法是定序:讓一方先決定,另一方跟隨。

**遷移題**: 「一個 Deployment 3 副本掛同一個 RWO 的 EBS PVC,replicas 分散在 3 台 node。會發生什麼?錯誤會出現在哪一棒?」
(答案方向:RWO = 一次一台 node。第一個 Pod 掛上後,其他 node 的 Pod 卡 ContainerCreating,describe 看到 attach 失敗。這題同時是 C-3 的引子:Deployment 副本共搶一個 PVC 本身就是錯誤形狀。)

### 誘答彈藥

- 「PV 的 reclaimPolicy 設 Retain,所以刪掉 PVC 之後再建一個同名 PVC,會自動接回原來的資料。」
  (錯。Retain 的 PV 在 PVC 刪除後進 `Released` 狀態,上面還留著舊的 claimRef,**不會**被任何新 PVC 綁定;要管理員手動清 claimRef 或重建 PV 才能重用。Retain 保的是「資料不被自動刪掉」,不是「自動重連」。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | EKS 上第一次讓有狀態服務落地,要規劃 StorageClass |
| **生產怎麼做** | 裝 EBS CSI driver(EKS addon,driver 本身需要 AWS 權限,正好用 C-5 的 IRSA 給,伏筆)。StorageClass 用 gp3 + `WaitForFirstConsumer` + `allowVolumeExpansion: true`;資料庫級的 reclaimPolicy 用 Retain 防手滑 |
| **真實踩坑** | EKS 叢集升級到 1.23+ 後 PVC 全部 Pending:in-tree EBS provisioner 被移除,沒裝 EBS CSI addon,default StorageClass 指向一個不存在的引擎。describe PVC 看到 `waiting for a volume to be created either by external provisioner "ebs.csi.aws.com" or manually`。規則還在,引擎沒了 |
| **面試怎麼問** | 「解釋 dynamic provisioning 的流程,以及 WaitForFirstConsumer 解決什麼問題?」「CSI 為什麼存在?in-tree driver 有什麼問題?」 |

**Say it in English**: "A StorageClass is a template; an external provisioner watches for pending claims and creates the actual disk. Same rule-versus-engine pattern as Ingress and its controller."

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| dynamic provisioning | /daɪˈnæm.ɪk prəˈvɪʒ.ən.ɪŋ/ | Creating storage on demand when a claim references a StorageClass | PVC 指名型錄,磁碟自動生,不用管理員手開 |
| CSI | /siː es aɪ/ | Container Storage Interface: the standard gRPC API between Kubernetes and storage drivers | k8s 跟儲存廠商說話的標準介面,與 CRI/CNI 並列三大外掛口 |
| reclaim policy | /rɪˈkleɪm ˈpɒl.ə.si/ | What happens to the volume after its claim is deleted: Delete or Retain | 刪 PVC 後磁碟的下場:跟著刪,還是留下來等人工處理 |

---

## C-3: StatefulSet 儲存視角

> **注意:P1 沒教過 StatefulSet,不能假設學員會。** P1 只教了 Deployment/ReplicaSet/rollout。從「Deployment 哪裡不夠」長出來,不要從 StatefulSet 的 feature list 開始。

### 核心概念

引導問題(用 C-2 遷移題接棒):「你要在 k8s 跑一個 PostgreSQL 主從(1 primary + 2 replica)。用 Deployment replicas=3,會撞到哪些牆?」

讓學員自己撞,預期能撞出兩面,第三面通常要提示:

1. **儲存牆**: Deployment 的 Pod template 只能指同一個 PVC,3 副本搶一顆 RWO 磁碟(C-2 剛推過)。而且就算掛上了,3 個資料庫寫同一個資料目錄是資料損毀,不是高可用。**每個副本要有自己的、跟著自己走的磁碟。**
2. **身分牆**: Deployment 的 Pod 名帶隨機 hash(P1 lab 親眼看過族譜),3 個 Pod 可互換、無差別。但資料庫副本不可互換:primary 就是 primary,replica 要知道去哪找 primary 同步。**需要穩定、可預測的身分。**
3. **秩序牆**: 資料庫叢集啟動有順序(primary 先起來,replica 才能加入)。Deployment 全部一起噴出來。

StatefulSet 對三面牆的回答:

```
Deployment:  web-7d9c6b-x2kfp  web-7d9c6b-p8jw2  (隨機、可互換、共用儲存定義)
StatefulSet: db-0  db-1  db-2                    (固定序號、逐一啟動、每人一顆 PVC)
```

- **volumeClaimTemplates**: 不是「一個 PVC」而是「PVC 的模板」,每個副本序號生一個自己的 PVC(`data-db-0`、`data-db-1`...)。db-0 死掉重建,新的 db-0 **接回同一顆** `data-db-0`。身分和磁碟綁定,這是 StatefulSet 儲存視角的核心一句話。
- **穩定網路身分 = headless Service**: `clusterIP: None` 的 Service。回扣 P2a CoreDNS:一般 Service 的 DNS 回 ClusterIP,再由 iptables DNAT 到隨機一個 Pod;headless 沒有 ClusterIP、沒有 DNAT,CoreDNS 直接回 Pod IP,而且每個 Pod 有自己的穩定 DNS 名:`db-0.db-svc.ns.svc.cluster.local`。replica 設定檔裡寫 `db-0.db-svc` 就永遠指到 primary,不管它重建幾次、IP 換幾次。
- 回扣謎題B 誤解史的好機會:他曾誤以為「封包先去 ClusterIP」,headless 是最乾淨的反例,連 ClusterIP 都不存在,DNS 層直接給你 Pod IP,NAT 層完全不參與。可以反問:「headless Service 的流量會經過 iptables DNAT 嗎?」`[RUNTIME: 若謎題B 已冷測穩固,這題當快速 recall;若近期又晃,拉長講]`
- 為什麼隨機負載均衡對資料庫是錯的:寫入必須去 primary,DNAT 的機率輪盤會把寫入丟給 replica。**「無差別分流」正是無狀態服務要的、也正是有狀態服務不能要的。**

### 動手觀察 (kind)

```bash
kubectl config current-context   # kind-k8s-coach-p0
```

學員自己寫(給規格):headless Service(`clusterIP: None`, name `web-hl`)+ StatefulSet(nginx, replicas=2, volumeClaimTemplates 請求 100Mi、storageClassName standard)。

1. `kubectl get pods -w` 看啟動順序:web-0 Ready 之後 web-1 才開始(對照 Deployment 一起噴)
2. `kubectl get pvc`:看到 `www-web-0`、`www-web-1`,一人一顆
3. DNS 驗證:`kubectl run dnstest --rm -it --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- nslookup web-0.web-hl.default.svc.cluster.local`
   (**回扣 P2a busybox DNS 坑**:busybox 的 nslookup 行為怪,上次 D 段 lab 當場踩過,這次直接用 agnhost,並用 FQDN。也對照 `nslookup web-hl...` 回的是多筆 Pod IP 而不是一個 ClusterIP)
4. 在 web-0 的 volume 寫個檔,`kubectl delete pod web-0`,重建後名字還是 web-0、檔案還在(對照 P0 lab:Deployment 補的是「新尾碼新 IP」的陌生人;StatefulSet 補的是「同名同磁碟」的本人)
5. `kubectl scale statefulset web --replicas=1`,注意 **PVC `www-web-1` 不會被刪**:這是護欄,防止 scale 手滑毀資料;再 scale 回 2,web-1 接回舊磁碟

### 打穿底層 (First-Principles Dive)

**StatefulSet 沒有發明新機制,它是三個舊零件的組合**:controller reconcile(P0)+ per-replica PVC(C-1/C-2)+ DNS 命名約定(P2a CoreDNS)。它的 controller 和 Deployment 的差別只在 reconcile 策略:按序號逐一收斂、身分固定、儲存跟人。

**通用原理:pets vs cattle。** 無狀態副本是 cattle(編號無意義,死了換一頭);有狀態副本是 pet(有名字,death 之後要「復活本人」而不是「換一個」)。分散式系統裡一切「成員身分重要」的東西(資料庫、Kafka broker、etcd 節點)都是 pet。回扣 P0:etcd 自己就是最典型的例子,member list 裡每個成員有固定身分。

**遷移題**: 「Kafka broker 掛掉重啟後,為什麼必須用回同一個 broker id 和同一份磁碟?如果它變成一台全新空白的 broker 加入,叢集會發生什麼?」
(答案方向:partition 的 replica 分配記在 broker id 上;空白新人觸發全量資料重平衡,網路和磁碟 IO 風暴。StatefulSet 的「同名接回同磁碟」就是為了避免這種假性失憶。)

### 誘答彈藥

- 「headless Service 其實也有 ClusterIP,只是藏起來不顯示,流量還是走 DNAT。」
  (錯。`clusterIP: None` 是真的沒有,kube-proxy 不會為它寫任何 iptables 規則,CoreDNS 直接回 Pod IP,client 直連。這題是謎題B 的鏡像:當初誤以為封包會去 ClusterIP,現在反向驗證他知道 ClusterIP 只活在 iptables 規則裡,沒規則就沒這回事。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 團隊想把 PostgreSQL 搬進 EKS,你要給意見 |
| **生產怎麼做** | 誠實版:多數公司(包括 billing 這種錢相關系統)資料庫用 RDS,不進 k8s;進 k8s 的有狀態通常是 Kafka/Redis/ES 這類,而且用 operator(CRD + 專用 controller)而不是裸 StatefulSet,因為備份、failover、升級的 domain 邏輯 StatefulSet 不管 |
| **真實踩坑** | StatefulSet 更新卡死:web-1 新版起不來(CrashLoop),按序更新的 controller 就停在那,web-0 永遠等不到更新,而且 StatefulSet 沒有 `kubectl rollout undo` 的 maxSurge 彈性(不會多開一個)。修法:先修 image 或手動刪卡住的 Pod。對照 P1 rollout:Deployment 卡壞版至少舊 RS 還護著全量 |
| **面試怎麼問** | 「Deployment 和 StatefulSet 差在哪?什麼時候必須用後者?」追問:「headless Service 的 DNS 行為和一般 Service 差在哪?」(考的就是 ClusterIP/DNAT 有沒有真懂) |

**Say it in English**: "A StatefulSet gives each replica a stable name, its own PVC, and a stable DNS record via a headless Service, so a rebuilt pod gets its identity and data back."

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| headless service | /ˈhed.ləs ˈsɜː.vɪs/ | A Service with no ClusterIP; DNS returns the Pod IPs directly | 沒有虛擬 IP、沒有 DNAT,DNS 直接給 Pod 本人 |
| volumeClaimTemplates | (照拼讀) | A PVC template stamped out per replica so each pod keeps its own volume | 每個序號生一顆自己的 PVC,重建後接回本人磁碟 |

---

## C-4: RBAC ⭐ (keystone)

### 核心概念

回扣 P0 三道關卡:authn(你是誰)→ **authz(你能做什麼)** → admission(這樣做合規嗎)。P0 時第二關只點名沒打開,現在打開:k8s 的 authz 主力就是 RBAC。

**RBAC 管的是「對 API Server 的請求」,僅此而已。** 每個請求可拆成:誰(subject)+ 動詞(verb: get/list/watch/create/delete...)+ 名詞(resource: pods/secrets...)+ 在哪(namespace)。RBAC 回答:這個組合放行嗎?

**四象限(定義權限的物件 × 綁人的物件)**:

```
                 定義「能做什麼」          綁定「誰能做」
namespace 級     Role                    RoleBinding
cluster 級       ClusterRole             ClusterRoleBinding
```

三種合法組合(第四種不存在):

| 組合 | 效果 | 用途 |
|------|------|------|
| Role + RoleBinding | 某 ns 內的權限 | 最常見,團隊在自己 ns 內活動 |
| ClusterRole + ClusterRoleBinding | 全叢集權限 | 管理員、node 級元件 |
| ClusterRole + **RoleBinding** | 把叢集級「定義」限縮在一個 ns 內生效 | 定義寫一次,各 ns 重複綁。面試愛考這格 |
| ~~Role + ClusterRoleBinding~~ | 不合法 | ns 級定義無法放大成叢集級 |

第三格的存在理由:DRY。「pod-reader」這種通用角色定義一次(ClusterRole),20 個 ns 各自用 RoleBinding 綁,不用抄 20 份 Role。

**兩個地基性質(誘答都從這裡長出來)**:

1. **RBAC 只有 allow,沒有 deny。** 預設全拒絕,規則是純加法,多條規則取聯集。想「擋掉某人某事」的唯一方法是不給,不是寫 deny。(對照學員熟的 AWS IAM:IAM 有 explicit deny,RBAC 沒有,這是遷移時最容易帶錯的直覺。)
2. **ServiceAccount 是 Pod 的身分。** 人類用 kubeconfig cert 過 authn,Pod 用 SA。每個 ns 有 `default` SA,Pod 沒指定就吃它。Pod 裡的 app 要呼叫 k8s API(例如 operator、CI runner),權限就是「綁在它 SA 上的 Role 的聯集」。

**403 排障套路(直接給肌肉記憶)**:

```bash
# 錯誤訊息本身就是完整診斷: 誰 + 動詞 + 名詞 + 哪個 ns 全寫在裡面
# Error: User "system:serviceaccount:ci:deployer" cannot list resource "secrets" in namespace "prod"

kubectl auth can-i list secrets -n prod --as=system:serviceaccount:ci:deployer   # 重現: yes/no
kubectl get rolebinding,clusterrolebinding -A -o wide | grep deployer            # 它到底綁了什麼
kubectl describe role <role> -n prod                                             # 定義裡有沒有這個動詞+名詞
```

排障心法:403 是三段鏈(SA 存在嗎 → binding 綁對了嗎 → role 定義含這個 verb/resource 嗎),最常見的斷點是 binding 綁錯 namespace 或 subject 的 ns 寫錯。

### 動手觀察 (kind)

```bash
kubectl config current-context   # kind-k8s-coach-p0
kubectl create namespace rbac-lab
kubectl create serviceaccount ci-reader -n rbac-lab
```

學員自己寫 Role(rbac-lab ns、resources: pods、verbs: get,list)和 RoleBinding(綁 ci-reader)。然後:

```bash
kubectl auth can-i list pods -n rbac-lab --as=system:serviceaccount:rbac-lab:ci-reader     # yes
kubectl auth can-i list secrets -n rbac-lab --as=system:serviceaccount:rbac-lab:ci-reader  # no
kubectl auth can-i list pods -n default --as=system:serviceaccount:rbac-lab:ci-reader      # no (Role 是 ns 級!)
kubectl get secrets -n rbac-lab --as=system:serviceaccount:rbac-lab:ci-reader              # 親眼看 403 全文
kubectl auth can-i --list -n rbac-lab --as=system:serviceaccount:rbac-lab:ci-reader        # 這個身分的完整權限清單
```

重點體感:`--as` impersonation 讓你不用真的拿到對方 token 就能驗證權限,是排障第一工具。

### 打穿底層 (First-Principles Dive)

**最小權限(least privilege)不是 k8s 發明的,是安全工程的通用原理**:任何主體只該擁有完成其任務所需的最小權限集合。理由用爆炸半徑(blast radius)推:權限 = 憑證外洩或 app 被打穿時,攻擊者能做的事的上限。CI 的 SA 若有 cluster-admin,一次 supply-chain 攻擊等於整個叢集淪陷。

設計最小 RBAC 的思考順序(gate 會考這個,先給方法論):

1. 列出這個主體**實際會發的 API 請求**(部署工具要 create/patch deployments;唯讀 dashboard 要 get/list/watch)
2. 圈最小 namespace 範圍(能 Role 就不要 ClusterRole)
3. 動詞逐個給,不用 `*`;resource 逐個給,不用 `*`
4. 想清楚等價升權陷阱:給了 `create pods` 等於能掛任意 SA 跑任意 image(用別人的 SA 升權);給了 `get secrets` 等於能讀所有 token。**有些「小」權限其實是大權限的別名。**

**遷移題**: 「AWS IAM 和 k8s RBAC 都做 authz。列兩個設計上的相同點和兩個不同點。」
(方向:同:預設拒絕、least privilege、身分與策略解耦。異:IAM 有 explicit deny 且 deny 優先,RBAC 純 allow 聯集;IAM 有 condition/resource ARN 細粒度,RBAC 粒度到 resource type + resourceNames 為止。這題同時為 C-5 IRSA 鋪路:兩套權限系統即將被接起來。)

### 誘答彈藥(keystone 必備)

1. 「這個 Pod 的 SA 權限不夠,RBAC 拒絕之後 Pod 會被殺掉重啟,所以你會看到 CrashLoopBackOff。」
   (錯。RBAC 活在 API Server 的請求路徑上,只會讓**那一個 API 請求**收到 403;Pod 是 kubelet 在 node 上跑的 process,RBAC 碰不到它。Pod 會不會 crash 取決於 app 自己怎麼處理 403。這題打學員的層級混淆弱點:API 請求層 vs runtime 層,和他之前 DNS 層 vs NAT 層的混淆同型。)
2. 「要擋掉實習生刪 prod 的 deployment,最乾淨的做法是寫一條 deny 規則。」
   (錯。RBAC 沒有 deny。正解是檢查他現有的 binding,把給過頭的權限收掉。若真的需要 deny 語意,那是 admission 層的事,回扣 P0 第三關。)

`[RUNTIME: 依 mistake-registry 決定誘答埋在 F 段菜鳥口中還是 G 段面試官口中]`

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | billing 平台的 CI pipeline 要能部署到 EKS 的 `billing` ns |
| **生產怎麼做** | 專用 SA(不用 default!)+ Role 只給 `deployments/services/configmaps` 的 `get,list,create,patch` + RoleBinding 圈在 `billing` ns。RBAC YAML 進 Git 走 review,權限變更有 audit trail。人類的權限走 IAM→RBAC 映射(EKS access entries / aws-auth),群組對映 ClusterRole |
| **真實踩坑** | CI 突然全紅,錯誤 `cannot patch resource "deployments"`。根因:有人「整理」RBAC 時把 RoleBinding 的 subject namespace 寫錯(SA 在 `ci` ns,binding 寫成 `default`)。`kubectl auth can-i --as` 一分鐘定位。教訓:403 錯誤訊息四要素直接讀,不要瞎猜 |
| **面試怎麼問** | 「一個 in-cluster 的 controller 需要讀全叢集的 Pod 並只在自己 ns 寫 event,RBAC 怎麼設計?」(考 ClusterRole+ClusterRoleBinding 和 Role+RoleBinding 混搭)「RBAC 能不能 deny?」(考地基性質) |

**Say it in English**: "RBAC is default-deny and additive-only: permissions are the union of all bindings, and there is no deny rule. It only gates API requests; it never touches running pods."

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| ServiceAccount | /ˈsɜː.vɪs əˈkaʊnt/ | The in-cluster identity a Pod uses to talk to the API server | Pod 的身分證,人用 kubeconfig,Pod 用 SA |
| least privilege | /liːst ˈprɪv.əl.ɪdʒ/ | Granting only the minimum permissions required for the task | 權限給到剛好,上限=外洩時的爆炸半徑 |
| impersonation | /ɪmˌpɜː.sənˈeɪ.ʃən/ | Making an API call as another identity to test its permissions (--as) | 用 --as 假扮對方驗證權限,403 排障第一工具 |

---

## C-5: IRSA ⭐ (keystone,EKS 核心)

> 學員公司 prod 是 EKS(billing 平台),這章是他工作直接用得上、面試必被問的一章。kind 做不了完整 IRSA(需要 AWS OIDC 信任),lab 拆兩段:JWT 半段在 kind 親手摸,STS 半段標 EKS 選配或概念教學 `[RUNTIME: 依學員意願與當下進度決定開不開 EKS lab]`。

### 核心概念

問題設定:billing 的 Pod 要讀 S3。C-4 的 RBAC 管的是 k8s API,S3 是 **AWS API**,RBAC 管不到。Pod 怎麼拿 AWS 權限?

**舊做法(反面教材,先講它為什麼爛)**:node 的 instance profile。EC2 node 掛一個 IAM role,node 上**所有** Pod 透過 metadata service 共享這個 role。後果:billing Pod 要 S3、隔壁 log agent 要 CloudWatch、再隔壁要 DynamoDB,node role 變成三者聯集,**每個 Pod 都拿到全部**。爆炸半徑 = 整台 node 的權限總和,正面違反 C-4 剛學的 least privilege。權限的粒度錯了:粒度在 node,需求在 Pod。

**IRSA(IAM Roles for Service Accounts)= 把 IAM role 綁到 SA 上,粒度修正到 Pod 級。**

整條鏈(這是 gate 考題,每一棒都要能講):

```
1. EKS 叢集自帶一個 OIDC identity provider (發行者 iss = 叢集專屬 URL)
2. SA 加 annotation: eks.amazonaws.com/role-arn = <要扮演的 IAM role>
3. Pod 用這個 SA 起動時,EKS 的 mutating webhook (回扣 P0 admission!) 自動注入:
   - 一個 projected volume: 放一顆 SA token (OIDC JWT,有效期短,aud=sts.amazonaws.com)
   - 兩個 env: AWS_ROLE_ARN、AWS_WEB_IDENTITY_TOKEN_FILE
4. Pod 裡的 AWS SDK 看到這兩個 env,自動呼叫 STS AssumeRoleWithWebIdentity,附上 JWT
5. AWS 驗 JWT: 簽名對不對 (查叢集 OIDC provider 的公鑰)、iss 對不對、
   sub 是不是 trust policy 允許的 system:serviceaccount:<ns>:<sa>
6. 驗過 → STS 回一組臨時憑證 (有效期數小時,自動輪替) → SDK 拿去打 S3
```

一句話骨架:**k8s 發身分證(JWT),AWS 驗身分證換臨時通行證(STS)。** 全程沒有任何長期 access key 存在任何地方。

兩套權限系統的接點看清楚:k8s 這邊管「誰能用這個 SA」(RBAC + Pod spec),AWS 那邊管「這個 SA 能扮演哪個 role、role 能做什麼」(trust policy + IAM policy)。信任的橋是 OIDC:AWS 事先被告知「這個叢集發的 JWT 我認」。

**通用原理:這是 federated identity(聯邦身分),不是 k8s 或 AWS 的專利。** GitHub Actions 對 AWS 的 OIDC keyless auth、GCP 的 Workload Identity,全是同一個模式:與其把長期密鑰塞進去(會外洩、要輪替、審計困難),不如讓兩個系統建立信任關係,用短命令牌現場換臨時憑證。密鑰管理問題被轉化成信任關係管理問題。

補充一句(面試加分):2023 起 EKS 另有 **Pod Identity** 新機制(agent 模式,不用自管 OIDC provider + annotation),概念同樣是「SA 換臨時憑證」,IRSA 仍是存量主流,兩個名詞都認得即可。

### 動手觀察 (kind 半段: JWT 本人)

kind 沒有 AWS,但 SA token projection 是純 k8s 機制,鏈的前半段完全摸得到:

```bash
kubectl config current-context   # kind-k8s-coach-p0
kubectl create token default --audience=sts.amazonaws.com --duration=1h > /tmp/sa.jwt
cut -d. -f2 /tmp/sa.jwt | base64 -d 2>/dev/null | head -c 600
```

讀 payload,對著鏈講:`iss`(kind 裡是叢集內建 issuer;EKS 上就是那個 OIDC URL)、`sub` = `system:serviceaccount:default:default`(trust policy 核對的就是這個字串)、`aud` = 我們指定的 sts、`exp` 短時效。**學員親眼看到「SA token 就是一顆 JWT」,IRSA 的神秘感就拆掉一半。**

### EKS lab(選配)

`[RUNTIME: 學員點頭才開。terraform 只產生程式碼,由學員親手 plan/apply;資源命名一律 billing-dev-eks-* 前綴]`

規格:OIDC provider 資料源 + IAM role `billing-dev-eks-irsa-demo`(trust policy 限定 `sub = system:serviceaccount:demo:s3-reader`)+ 唯讀單一 bucket 的 policy;k8s 側 SA 加 annotation,起一個帶 aws cli 的 Pod 跑 `aws sts get-caller-identity`,看到 assumed-role 而不是 node role。**收尾必做**:`terraform destroy` + `aws iam list-roles` 確認清乾淨。

### 打穿底層 (First-Principles Dive)

**為什麼臨時憑證在安全上是質變,不只是量變?** 用故障模型推:長期 access key 外洩後,攻擊者可以無限期使用,直到有人「發現並主動撤銷」(平均發現時間以月計)。短命憑證外洩後,傷害窗口 = 剩餘有效期(小時級),而且切斷信任(改 trust policy / 刪 SA)立即止血。防禦從「依賴偵測」變成「依賴時間自動失效」,把人為反應速度從關鍵路徑上拿掉了。

**遷移題**: 「你們 CI 以前把 AWS access key 存在 GitHub secrets 裡。用今天的模式重新設計,GitHub Actions 的 OIDC 版本裡,誰對應 EKS 叢集的 OIDC provider?誰對應 SA?trust policy 核對什麼?」
(方向:GitHub 是 issuer;repo/branch 身分對應 SA;trust policy 核對 `sub` 形如 `repo:org/repo:ref:refs/heads/main`。同一個模式換皮,認出來就是把知識遷移成功。)

### 誘答彈藥(keystone 必備)

1. 「IRSA 底層其實就是 AWS 幫你把 access key 生好、存進一個 Secret 掛給 Pod,只是自動化了。」
   (錯。全鏈路沒有任何長期憑證、沒有 Secret 參與。Pod 裡只有一顆短命 JWT,憑證是 SDK 每次向 STS 現場換的臨時憑證。這誘答聽起來合理,因為「憑證放 Secret」是多數人既有直覺,正好埋在似懂非懂邊界。)
2. 「同一台 node 上的其他 Pod,反正共用 node,也拿得到這個 role 的權限。」
   (錯,那是舊做法 instance profile 的特性。IRSA 的 JWT 是 per-Pod projected volume,sub 綁死特定 SA,別的 Pod 沒有這顆 token,trust policy 也不認它的 SA。這題直接考「新舊兩代的爆炸半徑差異」有沒有真的分清。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | billing 平台的對帳 job 要讀 S3 帳單 bucket + 打 SQS |
| **生產怎麼做** | 一個 job 一個 SA 一個 IAM role,policy 收到單一 bucket/queue。EBS CSI driver、cluster-autoscaler、external-dns 這些叢集元件本身也各自走 IRSA(回扣 C-2 伏筆:CSI driver 開 EBS 卷的 AWS 權限就是這樣來的)。terraform 統一管 role + trust policy |
| **真實踩坑** | Pod 起來後打 AWS 全部 `AccessDenied`,查半天 IAM policy 沒錯。根因:SA annotation 的 role ARN 有 typo,webhook 沒注入或注入了錯的 ARN。排查順序:`kubectl describe sa` 看 annotation → 進 Pod `env | grep AWS` 看有沒有被注入 → `aws sts get-caller-identity` 看實際身分是誰(常見驚嚇:是 node role,表示 IRSA 根本沒生效而不是權限不夠) |
| **面試怎麼問** | 「解釋 IRSA 的完整原理,為什麼比 node instance profile 好?」(EKS 職缺幾乎必考)追問:「token 外洩了怎麼辦?爆炸半徑多大?」 |

**Say it in English**: "IRSA federates identity: the pod presents a short-lived OIDC token issued by the cluster, and STS exchanges it for temporary AWS credentials. No long-lived keys exist anywhere."

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| IRSA | /ˈɜːr.sə/ | IAM Roles for Service Accounts: pod-level AWS permissions via OIDC federation | 把 IAM role 綁到 SA,權限粒度從 node 修正到 Pod |
| OIDC | /oʊ aɪ diː siː/ | OpenID Connect: an identity layer where one system trusts tokens issued by another | 兩個系統的信任橋,AWS 靠它驗 k8s 發的 JWT |
| token projection | /ˈtoʊ.kən prəˈdʒek.ʃən/ | Mounting a short-lived, audience-bound service account JWT into a pod | 把短命、指定受眾的 SA JWT 掛進 Pod 的機制 |

---

## C-6: Secrets + Pod Security Standards

### 核心概念

兩個子題,共同主軸是「不可信的 Pod」:機密怎麼給它(Secrets),它的手腳怎麼綁住(PSS/securityContext)。

**Secrets:先拆掉最大的誤解。**

`kubectl get secret -o yaml` 看到的是 base64。**base64 是編碼(encoding),不是加密(encryption)**:無密鑰、可逆、`base64 -d` 一秒還原。它存在的理由只是讓二進位內容能塞進 YAML/JSON,和安全零關係。

那 Secret 比 ConfigMap 強在哪?誠實答案:預設下只強一點點,強的地方全在**周邊配套**:

1. RBAC 可以把 secrets 和 configmaps 分開授權(回扣 C-4:`get secrets` 是要省著給的大權限)
2. **etcd encryption at rest**:預設 etcd 裡的 Secret 也只是 base64(等下 lab 親眼看),要在 API Server 配 EncryptionConfiguration(aescbc / KMS)才會落盤加密。EKS 現在預設用 KMS envelope encryption 幫你做掉這層
3. kubelet 把 Secret volume 放 tmpfs(記憶體),不落 node 磁碟

**掛載方式與輪替差異(生產真坑)**:

| 掛法 | Secret 更新後 | 原因 |
|------|--------------|------|
| env var | **不會**更新,要重啟 Pod | env 是 process 啟動時一次性寫進去的(回扣 P1:container = process,env 是 exec 當下的快照) |
| volume 掛載 | 會,kubelet 週期性同步(分鐘級) | 檔案可以換,kubelet 用 symlink 原子切換 |
| volume + subPath | **不會** | subPath 是 bind mount 單一檔案,繞過了 symlink 機制 |

生產做法:機密真正的家在 AWS Secrets Manager / SSM Parameter Store(集中、可稽核、可自動輪替),用 **External Secrets Operator** 同步進 k8s Secret。ESO 又是一個 controller:watch ExternalSecret 物件(規則),去 AWS 拉值生出 k8s Secret(引擎)。四合一對照表可以再加一行了。而 ESO 去 AWS 拉值的權限,就是 C-5 的 IRSA:P2b 的所有章在這裡互相扣上。

**Pod Security:限制 Pod 能做什麼。**

`securityContext` 常用欄位(每個都回扣 P1 container = process):

- `runAsNonRoot: true`:container 裡的 root 就是 host kernel 眼中的 UID 0(除非 user ns 重映射),逃逸出去就是 root。強迫用普通 UID 跑
- `readOnlyRootFilesystem: true`:rootfs 唯讀,攻擊者無法寫入後門或改二進位;需要寫的地方明確給 emptyDir(回扣 C-1:反正狀態本來就不該放 rootfs,這個限制其實是免費的)
- `allowPrivilegeEscalation: false`:封掉 setuid 之類的提權路徑
- `capabilities: drop: [ALL]`:Linux 把 root 權力拆成數十個 capability(綁低埠、改網路、掛載...),全丟掉再按需加回。這是 kernel 的 per-process 旗標,又一次「container 的本質是 process」

**PSS(Pod Security Standards)= 三檔標準 + admission 執法**:

- 三檔:`privileged`(不設限)/ `baseline`(擋已知提權:hostPath、privileged、hostNetwork...)/ `restricted`(強制上面那組 securityContext 全家桶)
- 啟用方式是 namespace label:`pod-security.kubernetes.io/enforce=restricted`(另有 `warn`、`audit` 兩個模式,能先觀察再執法,生產漸進導入靠這個)
- 執法者是內建的 admission controller,**回扣 P0 第三關**:不合規的 Pod 在 API Server 就被退件,根本到不了 kubelet。可以考:「被 PSS 擋下的 Pod,會出現在 kubectl get pods 裡嗎?」(不會,create 請求直接 4xx;若是 Deployment 建的,看 ReplicaSet 的 events)

### 動手觀察 (kind)

```bash
kubectl config current-context   # kind-k8s-coach-p0
kubectl create secret generic db-cred --from-literal=password=S3cretPa55
kubectl get secret db-cred -o jsonpath='{.data.password}' | base64 -d; echo
```

**殺手級一幕:直接去 etcd 裡讀 Secret**(仿 P0 etcdctl 玩法,學員摸過這條指令):

```bash
docker exec k8s-coach-p0-control-plane etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key get /registry/secrets/default/db-cred
```

輸出裡密碼內容肉眼可辨(沒配 encryption at rest 的 kind 預設)。引導問題:「所以拿到 etcd 備份檔的人,拿到了什麼?」這一幕把「etcd encryption at rest 為什麼存在」從背誦變成體感。

PSS 執法現場:

```bash
kubectl create namespace pss-lab
kubectl label namespace pss-lab pod-security.kubernetes.io/enforce=restricted
kubectl -n pss-lab run naked-nginx --image=nginx   # 預期被拒
```

讀完整的拒絕訊息(它會逐條列出違規:allowPrivilegeEscalation、capabilities、runAsNonRoot、seccompProfile),然後學員照著訊息自己把 securityContext 補齊到過關(nginx 需要換 `nginxinc/nginx-unprivileged` 之類的非 root image,這本身就是教學點:restricted 不是加幾行 YAML 就完,image 也要配合)。

### 打穿底層 (First-Principles Dive)

**防禦縱深(defense in depth)**:本 chunk 每個機制單獨看都「不完整」,這是設計而不是缺陷。安全從來不是找一道完美的牆,而是疊多層失效不相關的牆:RBAC 擋 API 面、encryption at rest 擋離線拷貝面、ESO+輪替縮短憑證壽命面、PSS/securityContext 擋 runtime 提權面、(P2a 預告過的)NetworkPolicy 擋橫向移動面。攻擊者要全部同時穿過。面試被問「Secret 到底安不安全」,正確答案不是 yes/no,而是列出每一層各擋哪個威脅模型。

**遷移題**: 「12-factor 說 config 放 env var。但你今天學到 env 掛 Secret 不能輪替,而且 `kubectl describe pod` 和 crash dump 都可能把 env 洩出來。這兩個原則衝突嗎?你的取捨?」
(方向:12-factor 反對的是 config 寫死進 image/程式碼;在 k8s 語境,非機密 config 用 env/ConfigMap 沒問題,機密走 volume 掛載或 app 直連 Secrets Manager。原則要看它當年反對什麼,不是逐字執行。)

### 誘答彈藥

1. 「Secret 在 k8s 裡是加密存放的,你 get 出來看到亂碼就是加密後的樣子。」
   (錯,而且是本 chunk 必收的現成誘答。那是 base64,`| base64 -d` 一秒還原;etcd 裡預設也是 base64。要加密得配 encryption at rest,EKS 用 KMS。答這題時能不能主動區分 encoding vs encryption,就是精準度考點。)
2. 「Secret 改了值,Pod 裡用 env 讀的設定會自動跟著變,因為 k8s 是 declarative 的。」
   (錯。env 是 process 啟動瞬間的快照,改 Secret 不會重啟 process。volume 掛載才會被 kubelet 同步,subPath 又不會。「declarative 所以什麼都自動收斂」是過度泛化,reconcile 收斂的是 k8s 物件,不是 process 的記憶體。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | billing 平台的 DB 密碼、第三方金流 API key 怎麼管 |
| **生產怎麼做** | 真源放 AWS Secrets Manager(自動輪替)+ ESO 同步進叢集;EKS 開 KMS envelope encryption;RBAC 把 `get secrets` 收窄到極少數 SA;namespace 全面上 PSS `restricted`(先 warn 模式跑兩週看違規清單再 enforce);Git repo 裡永遠只有 ExternalSecret 物件,沒有 Secret 本體 |
| **真實踩坑** | 有人把含 Secret 的 YAML commit 進 Git,幾個月後 repo 轉 public,金鑰外洩。修復不是 `git rm`(歷史還在),要輪替金鑰 + 清 Git 歷史。這就是「Git 裡只放 ExternalSecret 引用」這條規矩的由來 |
| **面試怎麼問** | 「k8s Secret 安全嗎?說出它的弱點和你會加哪些層。」「Secret 用 env 和 volume 掛載差在哪?」(輪替差異是分水嶺題,答得出 subPath 例外就是有真的踩過) |

**Say it in English**: "Base64 is encoding, not encryption: anyone who can read the Secret object or the etcd backup can recover the value. Encryption at rest and RBAC are separate layers you must add."

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| encryption at rest | /ɪnˈkrɪp.ʃən æt rest/ | Encrypting data where it is stored, so a stolen disk or backup is unreadable | 落盤加密,偷走 etcd 備份也讀不出 Secret |
| capabilities | /ˌkeɪ.pəˈbɪl.ə.tiz/ | Fine-grained slices of root privilege assigned per process by the Linux kernel | root 權力被 kernel 拆成小塊,per-process 給,container 該全丟再按需加 |
| Pod Security Standards | (照拼讀) | Three built-in policy levels enforced at admission via namespace labels | 三檔安全標準,namespace label 啟用,admission 執法退件 |

---

## Chaos Drill Hooks (P2b)

> 完整劇本在 `references/chaos-drills.md`(P2b 區段),這裡只放鉤子。都是「先讓學員看症狀、限時定位」的 E 段用法。

- **P2b-1: PVC 卡 Pending**(C-2 後)。注入:storageClassName 打錯字 / 或 WaitForFirstConsumer 下只建 PVC 不建 Pod。考點:describe PVC 讀 events、分辨「引擎不存在」vs「引擎在等 consumer」兩種 Pending。回扣「規則 vs 引擎」。
- **P2b-2: RBAC 403**(C-4 後)。注入:把 CI SA 的 RoleBinding subject ns 改錯(或 Role 少一個 verb)。考點:403 訊息四要素直讀、`kubectl auth can-i --as` 重現、三段鏈(SA→binding→role)逐段排查。MTTR 計時。
- **P2b-3: IRSA token 拿不到 / AccessDenied**(C-5 後)。EKS 選配或桌演(tabletop)`[RUNTIME: 沒開 EKS lab 就用口頭排障走一遍鏈]`。注入:SA annotation ARN typo 或 trust policy sub 不符。考點:describe sa → Pod 內 `env | grep AWS` → `aws sts get-caller-identity` 分辨「IRSA 沒生效(還是 node role)」vs「role 權限不夠」,這是兩種完全不同的修法。

---

## P2b 畢業 Gate

**考核格式(照 SKILL.md 的 P2b gate 定義:設計最小權限 RBAC + 解釋 IRSA 怎麼把 IAM 接到 SA)**:

**第一題(設計題)**: 給場景:「billing ns 有一個對帳 CronJob,需要:讀自己 ns 的 ConfigMap、建立和查看自己的 Job Pod 的 log、讀 S3 帳單 bucket。請設計它的完整權限,k8s 側 + AWS 側。」白板作答,不查資料。

**第二題(原理題)**: 「從 Pod 起動到成功呼叫 S3,把 IRSA 整條鏈按順序講一遍,每一步指出是誰(哪個元件)做的。」(盲講,和 P0 五棒同格式;學員的已知弱點是盲講漏中間棒次,提醒他用固定骨架默數:OIDC provider → annotation → webhook 注入 → JWT → STS → 臨時憑證,六棒。)

**Pass 條件**:

- RBAC:選對象限(Role+RoleBinding 圈在 billing ns)、專用 SA 不用 default、verbs/resources 逐項給不用 `*`、能說出為什麼不給 `get secrets`
- 能講出 RBAC 只有 allow、預設拒絕、聯集這三個地基性質
- IRSA 六棒不漏,能明確說出「哪裡沒有長期憑證」以及 trust policy 核對的是 `sub`(SA 的完整身分字串)
- 能對比舊 node role 做法的爆炸半徑差異
- 至少抓出一題現場埋的誘答並講清為什麼錯 `[RUNTIME: 從 C-4/C-5/C-6 誘答庫抽,優先抽他前面答得最猶豫的那題]`

**Stretch(加分,不強求)**:

- 能主動提 PSS/securityContext 把 CronJob 的 Pod 也鎖住(答案完整度從「權限」擴到「防禦縱深」)
- 能說出 GitHub Actions OIDC 和 IRSA 是同一個模式(遷移成功的證據)

**Gate 失敗處理**: 見 SKILL.md Phase Gate Failure 協議。常見弱點預測:四象限的第三格(ClusterRole+RoleBinding)、IRSA 鏈中 webhook 注入這一棒被跳過。對症重練 C-4/C-5,進 mistake-registry 冷測。

---

## Portfolio 整合 (P2b)

過價值門檻才進 repo(回扣 2026-06-22 的雙價值門檻定案),本 phase 建議:

- `portfolio/manifests/p2b-rbac-minimal.yaml`: gate 第一題的最終答案(SA + Role + RoleBinding),附註解說明每個 verb 為什麼給。這是面試能直接拿出來講的 artifact
- `portfolio/manifests/p2b-statefulset-demo.yaml`: headless Service + StatefulSet + volumeClaimTemplates 的 lab 成品
- `portfolio/notes/p2b-storage-rbac-irsa.md`: 重點收 IRSA 六棒鏈路圖(學員自己畫 ASCII)+ Secret 掛載輪替對照表 + 403 排障三段鏈
- 太基礎不進 repo:單獨的 PV/PVC 練習 YAML、secret 建立指令(留本機筆記即可)
- 若開了 EKS lab:terraform 的 IRSA 模組進 `portfolio/terraform-eks/`(這是 showcase 級素材,P5 會再長大)

---

## P2b 英文 Ramp

檔位(P2a-P2b):中文為主,術語卡 + 每個機制一兩句英文短句(已嵌在各 chunk 的 Say it in English)。學員 2026-07-01 明說中文佔比多一些:Say-it-in-English 用「你能不能用英文把這句講給面試官」輕推,不硬逼。全部術語同步進 `k8s-coach-workspace/term-registry.md` 做間隔抽考。

本 phase 累積術語:

| Chunk | 術語 |
|-------|------|
| C-1 Volume/PV/PVC | bind mount, PersistentVolumeClaim |
| C-2 StorageClass/CSI | dynamic provisioning, CSI, reclaim policy |
| C-3 StatefulSet | headless service, volumeClaimTemplates |
| C-4 RBAC | ServiceAccount, least privilege, impersonation |
| C-5 IRSA | IRSA, OIDC, token projection |
| C-6 Secrets/PSS | encryption at rest, capabilities, Pod Security Standards |

英文放射狀 mind map 素材(供教完流程後給學員手抄默畫):中心 `Stateful & Secured Pod`,六條輻條 `bind mount → PV/PVC`、`StorageClass → provisioner (rule vs engine)`、`StatefulSet → stable identity + own PVC`、`RBAC → default-deny, allow-only, union`、`IRSA → JWT → STS → temp creds`、`Secret → base64 ≠ encryption, layers of defense`。
