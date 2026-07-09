# P0 心智模型: Kubernetes Control Plane 內部機制

> **如何使用此檔:** 這是 P0 階段的教學素材庫,供 coach 在 C 段(核心原理)讀取並改編。
> 不要逐字唸稿,而是依學員反應選擇要深挖哪個切面。
> 每個 chunk 對應一個 Simon Method 的原子單位,通過 Feynman Gate 後再往下走。

---

## P0 學習藍圖

**目標**: 建立 k8s 的「系統性心智模型」,而不是學更多 kubectl 指令。

**P0 中心問題**: `kubectl apply -f pod.yaml` 之後到 Pod Running,中間發生了什麼?

這個問題是 P0 的貫穿軸。每個 chunk 都是在回答這個問題的一個層次。

**學習路徑(Simon 切塊)**:

| Chunk | 主題 | 核心問題 |
|-------|------|---------|
| C-0 | 聲明式 vs 命令式 | 為什麼 k8s 選擇聲明式? |
| C-1 | Reconcile Loop | k8s 如何讓「期望」變成「現實」? |
| C-2 | Control Plane 拆解 | 每個元件負責什麼? |
| C-3 | apply→Running 全流程 | 把 C-0 到 C-2 串起來(P0 核心) |
| C-4 | etcd 與 Raft 共識 | 為什麼 etcd 是 source of truth? |
| C-5 | namespace 與 cgroup 初探 | 容器的本質是什麼? |

**環境前置**: 用 `scripts/lab-cluster.sh up p0` 起 `k8s-coach-p0` kind cluster。

---

## C-0: 聲明式 vs 命令式

### 核心概念

**命令式(Imperative)**: 你告訴系統「做什麼、怎麼做」,step by step。
**聲明式(Declarative)**: 你告訴系統「我要的終態是什麼」,怎麼達到由系統決定。

類比: 命令式像是給廚師菜譜(先炒蔥、再加蒜、翻炒 30 秒),聲明式像是點菜(我要宮保雞丁)。

```bash
# 命令式: 告訴系統一步一步怎麼做
kubectl run nginx --image=nginx
kubectl scale deployment nginx --replicas=3

# 聲明式: 告訴系統「我要的狀態」
kubectl apply -f nginx-deployment.yaml
# --- nginx-deployment.yaml ---
# apiVersion: apps/v1
# kind: Deployment
# spec:
#   replicas: 3        # 宣告「我要 3 個」,由系統搞定
#   template:
#     spec:
#       containers:
#       - image: nginx  # 宣告「用這個 image」
```

### 為什麼宣告式更好? (先讓學員想,不要直接說答案)

引導問題: 「如果你用命令式跑了 `scale --replicas=3`,然後其中一個 Pod 掛了,k8s 需要你再下一次指令嗎?聲明式呢?」

關鍵洞見:

1. **冪等性(Idempotency)**: 同一份 YAML apply 100 次,結果相同。命令式的「加 2 個 replica」就不是冪等的。
2. **自癒能力**: 聲明式告訴系統「目標態」,系統持續比對「目標」和「現實」,不一樣就修。這就是下一個 chunk 的主角,reconcile loop。
3. **GitOps 的基礎**: YAML 是版本控制友好的聲明,可以 git diff、code review、rollback。

### 打穿底層 (First-Principles Dive)

**k8s 聲明式背後是控制理論(Control Theory)的核心思想**: 系統存在一個「設定點(setpoint)」和「反饋迴路(feedback loop)」。控制器持續觀察真實狀態,和設定點比較,計算誤差,然後採取行動縮小誤差。這就是暖氣的恆溫器、工廠的 PID controller、以及 k8s 的 reconcile loop。

**遷移題**: 「你在家裡設了冷氣 26 度。冷氣是命令式還是聲明式的思維?它的『reconcile loop』是什麼?」

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你的公司把部署腳本從 ansible playbook(命令式)遷移到 k8s YAML(聲明式) |
| **生產怎麼做** | 所有 k8s 物件以 YAML 存在 Git repo,CD 系統(ArgoCD)把 Git state 同步到 cluster。整個部署流程是「我 commit 了 YAML → 系統自己搞定」 |
| **真實踩坑** | 用 `kubectl edit` 直接改 cluster 上的物件 → 下次 CD 同步時被蓋回去,手動改的東西消失。根因: 違反聲明式的「Git 是 source of truth」原則 |
| **面試怎麼問** | 「解釋 Kubernetes 為什麼選擇聲明式 API。命令式和聲明式在 failure recovery 上有什麼差異?」 |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| declarative | /ˈdek.lər.ə.tɪv/ | You specify the desired end state; the system figures out how to get there | 說「要什麼」,不說「怎麼做」 |
| idempotent | /aɪˈdem.pə.tənt/ | Applying the same operation multiple times produces the same result | 重複做不會產生副作用,apply 100 次等於 apply 1 次 |
| desired state | /dɪˈzaɪərd steɪt/ | The configuration you declared, stored in etcd | 你宣告的理想終態,存在 etcd 裡 |

---

## C-1: Reconcile Loop (協調迴路)

### 核心概念

Reconcile loop 是整個 k8s 的驅動引擎,概念極其簡單:

```
while true:
    actual_state  = observe_cluster()      # 現在實際是什麼?
    desired_state = read_from_etcd()       # 我們要的是什麼?
    diff = desired_state - actual_state    # 差了哪裡?
    if diff != empty:
        reconcile(diff)                    # 採取行動縮小差距
    sleep(interval)
```

這個迴路由 controller 實作。k8s 裡有很多 controller(Deployment Controller、ReplicaSet Controller、Node Controller...),每個負責一種物件,但都跑同一個邏輯。

### Level-Triggered vs Edge-Triggered (打穿底層)

這是 k8s 設計的關鍵原則之一,來自 OS/嵌入式系統的概念:

**Edge-Triggered (邊緣觸發)**: 事件發生的「瞬間」才反應。如果錯過這個瞬間,就永遠錯過了。
例: 傳統事件驅動系統: 「Pod 死了」這個事件只發送一次,如果 controller 當時當機,事件永遠丟失。

**Level-Triggered (水位觸發)**: 只要「當前狀態」和「目標狀態」不一致,就持續採取行動。不管是怎麼變成這個狀態的。
例: k8s 的 reconcile loop: controller 重啟後,重新讀 etcd,發現 actual 跟 desired 不符,照樣修。不需要重播事件歷史。

**k8s 用 level-triggered,這讓系統天然地具備自癒能力**,因為 controller 崩潰重啟後照樣能工作。

**遷移題**: 「如果 controller 當機了 10 分鐘,這 10 分鐘內有 3 個 Pod 掛掉了。controller 重啟後,它需要知道是哪 3 個 Pod、什麼時候掛的嗎?為什麼?」

### 動手觀察 Reconcile Loop

```bash
# 先建一個 Deployment
kubectl create deployment demo --image=nginx --replicas=3

# 觀察 Pod 狀態
kubectl get pods -w

# 在另一個 terminal,手動刪一個 Pod
kubectl delete pod <pod-name>

# 觀察: k8s 幾秒內重建一個新 Pod
# 這就是 ReplicaSet Controller 的 reconcile 在運作
```

引導問題: 「你剛才刪了一個 Pod,k8s 怎麼知道要重建?它在哪裡查到『我需要 3 個 replica』這個資訊?」
(答案: etcd。這就帶出下一個 chunk。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 生產 cluster 的某個 node 突然重啟,上面有 5 個 Pod |
| **生產怎麼做** | Node Controller 發現 node 不可達,把 Pod 標為 Unknown。一定時間後(預設 5 分鐘),Deployment/ReplicaSet controller 偵測 actual < desired,在其他 node 重建 Pod |
| **真實踩坑** | Node 網路抖動 10 秒,controller 還不知道 node 掛了,但 kubelet 已經開始重啟 Pod。再過幾分鐘 Node Controller 才把 Pod 驅逐。這段時間可能有兩份 Pod 同時跑(特別危險的是 StatefulSet)。理解 reconcile loop 的時間差才能正確設計 Pod Disruption Budget |
| **面試怎麼問** | 「k8s 的 controller 是 event-driven 還是 reconcile-based?兩者差在哪?為什麼 k8s 選後者?」 |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| reconcile | /ˈrek.ən.saɪl/ | The act of bringing actual state in line with desired state | 把「現實」調整到符合「理想」 |
| controller | /kənˈtroʊ.lər/ | A control loop that watches desired state and acts to achieve it | 跑 reconcile loop 的元件,每種物件有自己的 controller |
| level-triggered | /ˈlev.əl ˈtrɪɡ.ərd/ | Responds to the current state, not to events that caused it | 看「現在是什麼狀態」,不管「之前發生什麼事」 |
| watch | /wɒtʃ/ | A long-lived API request that streams state changes from etcd | 對 API server 發的長連線,etcd 有變化時立刻推送 |

---

## C-2: Control Plane 拆解

### 先建直覺: 叢集是誰在掌舵?

把 k8s cluster 想成一間公司:

- **API Server**: 前台接待 + 所有文件歸檔,唯一的溝通入口
- **etcd**: 公司的檔案室,所有狀態都存在這
- **Scheduler**: HR + 排班系統,決定哪個 Pod 去哪個 Node
- **Controller Manager**: 很多部門主管的集合體,每個主管負責一種物件讓它保持正確狀態
- **kubelet**: 現場領班,在每個 Node 上執行被分配的工作

### 各元件職責

**kube-apiserver**:
- 唯一的 API 入口點(所有 `kubectl` 指令、所有 controller、所有 kubelet 都通過它)
- 負責 authn(你是誰?) / authz(你能做什麼?) / admission(這個請求合法嗎?)
- 收到合法請求後,把狀態寫入 etcd

**etcd**:
- 分散式 key-value store,k8s 的唯一 source of truth
- 所有 k8s 物件(Pod、Service、ConfigMap...)都存在這裡
- 任何元件要讀叢集狀態,都從 etcd(通過 API server)讀

**kube-scheduler**:
- 只做一件事: 決定沒有 Node 的 Pod(unscheduled Pod)要跑在哪個 Node
- 怎麼決定: 過濾(filter)掉不符合條件的 Node,然後從剩下的中依分數選最佳
- 決定後: 把 `pod.spec.nodeName` 寫入 API server(etcd)

**kube-controller-manager**:
- 不是一個 controller,而是很多 controller 打包成一個 process
- 裡面有: ReplicaSet Controller、Deployment Controller、Node Controller、Namespace Controller...
- 每個 controller 跑自己的 reconcile loop

**kubelet**:
- 在每個 worker node 上跑,是 node 上 k8s 的代理人
- 不斷向 API server watch 分配給自己 node 的 Pod
- 發現有 Pod 被分配過來 → 呼叫 CRI(Container Runtime Interface)拉 image、啟動 container
- 定期回報 Pod 狀態到 API server(etcd)

### 動手: 親眼看到這些元件

```bash
# 看 control plane 元件(以 static pod 方式運行)
kubectl -n kube-system get pods

# 預期看到類似:
# kube-apiserver-k8s-coach-p0-control-plane
# etcd-k8s-coach-p0-control-plane
# kube-scheduler-k8s-coach-p0-control-plane
# kube-controller-manager-k8s-coach-p0-control-plane
# coredns-...
```

```bash
# 進 control plane 容器看 static pod manifests
docker exec -it k8s-coach-p0-control-plane ls /etc/kubernetes/manifests/

# 預期看到:
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml
```

```bash
# 看看 kube-apiserver 的啟動參數(真實生產用的 flag)
docker exec -it k8s-coach-p0-control-plane cat /etc/kubernetes/manifests/kube-apiserver.yaml
```

引導問題: 「為什麼 control plane 的元件要用 static pod 的方式跑?如果 control plane 元件是 Deployment,誰來管 Deployment controller 本身?」
(這是雞生蛋問題。static pod 由 kubelet 直接管,不需要 API server 存活。)

```bash
# 看 etcd 裡有什麼(需要 etcdctl)
# 這只是觀察,不修改任何東西
docker exec -it k8s-coach-p0-control-plane etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key get /registry --prefix --keys-only 2>/dev/null | head -30

# 會看到 /registry/pods/default/... /registry/deployments/... 等等
# 這就是 etcd 裡的 k8s 物件
```

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | EKS/GKE/AKS(托管 k8s)和自建 k8s 的差異 |
| **生產怎麼做** | 托管 k8s 把 control plane(API server / etcd / scheduler / controller-manager)交給雲端廠商管。你只負責 worker node。這就是為什麼 EKS 不收 worker node 費用裡的 control plane 費用(AWS 另外收 $0.10/hr per cluster) |
| **真實踩坑** | etcd 備份沒做好,然後 etcd volume 壞掉,整個叢集的狀態消失。自建 k8s 一定要做 etcd snapshot 備份(EKS 幫你管)。踩坑版: 恢復 etcd 時 certificate 過期,要先更新 cert 才能恢復 |
| **面試怎麼問** | 「kube-scheduler 和 kubelet 的職責分界在哪?scheduler 決定 Pod 跑在哪個 node,kubelet 怎麼知道要啟動這個 Pod?」 |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| control plane | /kənˈtroʊl pleɪn/ | The set of components that manage the overall state of the cluster | 掌舵的那一層:api-server、etcd、scheduler、controller-manager |
| kubelet | /ˈkjuːb.lɪt/ | The node agent that ensures containers are running as specified | 每個 Node 上的現場代理人,負責實際跑 container |
| static pod | /ˈstæt.ɪk pɒd/ | A pod managed directly by kubelet from a local manifest file, without API server | kubelet 直接讀磁碟 YAML 啟動的 Pod,不需要 API server 存活 |
| CRI | /siː ɑːr aɪ/ | Container Runtime Interface: the API between kubelet and the container runtime | kubelet 跟 container runtime(containerd/CRI-O)說話的標準介面 |

---

## C-3: apply→Running 全流程 (P0 核心)

> **這是 P0 的畢業考核中心。** 學員要能從記憶中白板畫出這個流程,並解釋每個步驟。

### 全流程圖

```
kubectl apply -f pod.yaml
       |
       v
+----------------+
|   API Server   |  <-- 1. 收到請求
| (authn/authz/  |
|  admission)    |
+-------+--------+
        |  2. 驗證通過,寫入 etcd
        v
+-------+--------+
|      etcd      |  <-- pod 物件寫入,nodeName 為空
+-------+--------+
        |  3. API server 通知 watcher
        v
+-------+--------+
|   Scheduler    |  <-- 4. 發現 unscheduled Pod
|                |       過濾 + 打分 + 選 Node
+-------+--------+
        |  5. 把 nodeName 寫回 etcd
        v
+-------+--------+
|      etcd      |  <-- pod.spec.nodeName = "node-1"
+-------+--------+
        |  6. kubelet 的 watch 發現新分配
        v
+-------+--------+
|     kubelet    |  <-- 7. 通知 CRI 拉 image / 啟動 container
|   (on node-1)  |
+-------+--------+
        |  8. container 啟動
        v
+-------+--------+
|  Container     |  <-- 9. kubelet 回報狀態到 API server
|  Runtime (CRI) |
+----------------+
        |  10. etcd 更新 pod status: Running
        v
   Pod: Running ✓
```

### 每個步驟的細節

**步驟 1-2: kubectl → API Server → etcd**

`kubectl apply` 序列化 YAML 成 protobuf / JSON,發 HTTP PATCH/POST 到 API server。

API Server 做三件事:
- **authn (Authentication)**: 你是誰? 讀你的 kubeconfig cert、token 或 service account
- **authz (Authorization)**: 你被允許這樣做嗎? 對照 RBAC rules
- **admission control**: 這個請求合規嗎? (Mutating Webhook 可改請求、Validating Webhook 可拒絕請求。例: `LimitRanger` 幫沒設 resources 的 Pod 加預設值、`PodSecurity` 拒絕 privileged Pod)

通過後寫 etcd,Pod 物件存在了,但 `nodeName` 是空的。

**步驟 3-5: Scheduler 選 Node**

Scheduler watch API server(實際是 watch etcd 的變化),看到一個 `nodeName` 為空的新 Pod,開始工作:

1. **Filter**: 過濾掉不符合的 Node(資源不夠、有 taint 但 Pod 沒 toleration、nodeSelector 不符合...)
2. **Score**: 對剩下的 Node 打分(資源最充裕、最能滿足 affinity 規則的得高分...)
3. **Bind**: 把選好的 `nodeName` 通過 API server 寫回 etcd

**步驟 6-9: kubelet 啟動 Container**

worker node 上的 kubelet 一直 watch API server,看到有 Pod 被分配到自己這個 node,開始工作:

1. 呼叫 CRI(通常是 containerd)拉 image(先查本地 cache,沒有才去 registry 拉)
2. CRI 呼叫 OCI runtime(通常是 runc)創建 container
3. Container 起來了,kubelet 定期向 API server 回報 Pod 的 status
4. API server 把 status 更新到 etcd

**步驟 10: Pod status = Running**

此時 `kubectl get pod` 看到 Running。

### 動手追蹤這個流程

```bash
# 開兩個 terminal

# Terminal 1: 監控事件流
kubectl get events --watch

# Terminal 2: apply 一個 Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: trace-demo
spec:
  containers:
  - name: nginx
    image: nginx:alpine
EOF

# 觀察 Terminal 1 的事件:
# Scheduled   Successfully assigned default/trace-demo to k8s-coach-p0-worker
# Pulling     Pulling image "nginx:alpine"
# Pulled      Successfully pulled image
# Created     Created container nginx
# Started     Started container nginx
```

```bash
# 看 scheduler 選了哪個 node
kubectl get pod trace-demo -o wide

# 追蹤完整的 status 變化
kubectl describe pod trace-demo
```

```bash
# 清理
kubectl delete pod trace-demo
```

### 打穿底層 (Full Flow)

整個 apply→Running 流程打穿到三個底層原理:

1. **分散式系統的 Watch Pattern**: kubelet 和 scheduler 不是輪詢(polling)API server,而是用 long-lived HTTP connection watch。API server 把 etcd 的變化推送給 watcher。這是「推」而非「拉」,減少輪詢延遲和 CPU 浪費。

2. **Pipeline 設計**: 每個元件只做好自己的一件事,通過 API server 解耦。scheduler 不需要知道 kubelet 的存在,kubelet 不需要知道 scheduler 的存在。它們都只和 etcd(via API server)說話。

3. **冪等性保證**: 整個流程每一步都是冪等的。如果 scheduler 崩潰,重啟後重新 watch,再次發現沒有 nodeName 的 Pod,重新調度。不會雙重調度,因為 scheduler 用 lease 做 leader election,同時只有一個 scheduler 在運作。

**遷移題**: 「如果 scheduler 當機了,新建的 Pod 會怎樣?現有的 Running Pod 會受影響嗎?」

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 生產環境 Pod 卡在 Pending 不動 |
| **生產怎麼做** | 看 `kubectl describe pod <name>` 的 Events 欄位。Scheduler 卡住了? 找 "0/3 nodes are available" 這樣的訊息。Admission webhook 拒絕了? 看 Events 裡有沒有 webhook 相關的訊息。Image 拉不到? Events 裡會有 `Failed to pull image` |
| **真實踩坑** | Admission webhook 的 timeout 設太短,且沒設 `failurePolicy: Ignore`,導致 Pod 全部被 webhook 拒絕,整個 cluster 無法建 Pod。排查方向: `kubectl get validatingwebhookconfigurations` 和 `kubectl get mutatingwebhookconfigurations`,找 `failurePolicy: Fail` 的 webhook |
| **面試怎麼問** | (P0 畢業 Gate 的題目形式)「從 `kubectl apply` 到 Pod Running,每個元件依序做了什麼?authn、authz、admission control 各是什麼時機?kubelet 怎麼知道要啟動 Pod?」 |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| scheduler | /ˈʃɛd.juː.lər/ | The control-plane component that assigns unbound Pods to Nodes | 決定 Pod 去哪個 Node |
| admission control | /ədˈmɪʃ.ən kənˈtroʊl/ | API server plugin chain that validates and mutates requests before persisting | API server 的關卡,可以改或拒絕你送進來的物件 |
| authn | /ˌɔːˌθen.tɪˈkeɪʃ.ən/ | Authentication: verifying the identity of the request sender | 確認「你是誰」 |
| authz | /ˌɔːˌθər.ɪˈzeɪʃ.ən/ | Authorization: deciding if the authenticated identity is permitted to do this | 確認「你能不能做這件事」 |
| unscheduled pod | /ʌnˈʃɛd.juːld pɒd/ | A Pod with no nodeName set yet, waiting to be assigned by the scheduler | 還沒被分配 Node 的 Pod,scheduler 的工作對象 |

---

## C-4: etcd 與 Raft 共識初探

### 為什麼 k8s 需要 etcd?

簡單問: 「k8s 不能直接把狀態存在 API server 的記憶體裡嗎?」

如果存記憶體:
- API server 重啟 → 所有狀態消失
- 多個 API server 副本 → 狀態不一致,哪個是對的?
- 沒有 audit trail,無法回放歷史

所以需要一個專門的「狀態儲存」:持久化、高可用、強一致。這就是 etcd。

### etcd 是什麼

etcd 是一個分散式 key-value store,設計目標:

1. **強一致(Strong Consistency)**: 任何讀取都能讀到最新被確認的寫入
2. **高可用(High Availability)**: 多個節點,少數節點掛掉還能運作
3. **Watch 機制**: 客戶端可以訂閱 key 的變化(k8s 的 watch 就是基於此)

k8s 用 etcd 儲存所有物件: `/registry/pods/default/my-pod`, `/registry/deployments/default/nginx`...

### Raft: etcd 高可用的秘密

etcd 用 **Raft** 共識算法讓多個節點保持一致。

核心概念(不深入,P0 只需要直覺):

**Leader 選舉**: 多個 etcd 節點中,選出一個 Leader 負責處理所有寫入。其他是 Follower。

**Quorum (法定人數)**: 一筆寫入只有在**多數節點確認**後才算成功。
- 3 個節點: quorum = 2(能容忍 1 個節點掛掉)
- 5 個節點: quorum = 3(能容忍 2 個節點掛掉)

```
             [Leader]
             etcd-0
            /        \
        confirm      confirm
          /                \
   [Follower]          [Follower]
    etcd-1               etcd-2

寫入流程:
1. 客戶端(API server)寫到 Leader
2. Leader 把寫入複製給所有 Follower
3. 收到多數確認(2/3 or 3/5)才回應「成功」
```

**為什麼這很重要**: 如果 etcd 不用多數決,可能發生腦裂(split-brain): 兩個節點以為自己是 Leader,寫入互相衝突,狀態不一致。Raft 的 quorum 機制讓這不可能發生。

### 動手: 看 etcd cluster 狀態

```bash
# 進入 control plane 容器
docker exec -it k8s-coach-p0-control-plane bash

# 查看 etcd 成員(kind 的 etcd 是單節點,生產是 3 或 5 節點)
etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key member list

# 看 etcd 的健康狀態
etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key endpoint health
```

### 打穿底層 (First-Principles Dive)

**etcd 背後的通用原理是分散式共識(Distributed Consensus)問題**: 多個節點如何就「同一個值」達成一致?這是分散式系統的核心問題,Raft 是解法之一(另一個是 Paxos,更難理解)。

Raft 解決的問題在很多地方都用到: 資料庫的 replication(CockroachDB、TiDB)、分散式 lock、leader election。理解 Raft 讓你能遷移到任何需要分散式共識的場景。

**遷移題**: 「為什麼生產 etcd 要至少 3 個節點?2 個不行嗎?」
(答案: 2 個節點時 quorum = 2,任何一個掛掉,系統就停擺。還不如 1 個節點,至少不浪費資源。3 個節點才能容忍 1 個掛掉。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 自建 k8s 的 etcd 規劃 |
| **生產怎麼做** | 生產 etcd 通常 3 或 5 個節點,跨 AZ 部署。定期做 snapshot 備份(每 4-6 小時)。etcd 節點要用 SSD,etcd 對 disk latency 非常敏感(latency 過高會導致 leader election timeout,整個 cluster 抖動) |
| **真實踩坑** | etcd 節點的磁碟 IOPS 不夠(用了 HDD 或 network volume 而非 SSD),導致 leader election 不斷發生。表現: `kubectl` 很慢、偶爾 timeout、cluster 狀態抖動。排查方向: `etcdctl endpoint status` 看 latency,以及 etcd 的 Prometheus metric `etcd_disk_wal_fsync_duration_seconds` |
| **面試怎麼問** | 「etcd 用什麼機制保證高可用?什麼是 quorum?為什麼 etcd 節點數一定要是奇數?」 |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| etcd | /ˈɛt.siː.diː/ | The distributed key-value store that holds all Kubernetes cluster state | k8s 的唯一 source of truth,所有物件存在這 |
| Raft | /ræft/ | A consensus algorithm that ensures multiple nodes agree on the same state | 讓多個 etcd 節點保持一致的算法 |
| quorum | /ˈkwɔːr.əm/ | The minimum number of nodes that must agree for an operation to succeed | 法定人數,多數決,3 節點的 quorum = 2 |
| source of truth | /sɔːrs ɒv truːθ/ | The authoritative store that all components read from to know the real state | 唯一的權威狀態來源,k8s 裡是 etcd |

---

## C-5: namespace 與 cgroup 初探 (容器底層)

> **P0 只做「建立直覺」**,不深入。P1 才會用 hands-on 實際操作 namespace 和 cgroup。
> 目的: 讓學員不再把容器當「輕量版 VM」,而是理解「容器就是有特殊 Linux 屬性的 process」。

### 核心直覺: 容器不是 VM

**VM 的隔離**: 真正的硬體虛擬化,有自己的 kernel,完全隔離。
**容器的隔離**: 共用同一個 Linux kernel,用 kernel 的兩個機制做「看起來隔離」的效果。

這兩個機制:
- **Linux namespaces**: 隔離「看得到什麼」(process、網路、檔案系統、hostname...)
- **cgroups (control groups)**: 限制「能用多少」(CPU、記憶體、磁碟 IO...)

```
主機 kernel
    |
    +-- container A (pid namespace: 只看到自己的 process)
    |       (net namespace: 自己的網路介面)
    |       (cgroup: 最多 500m CPU, 256Mi memory)
    |
    +-- container B (pid namespace: 只看到自己的 process)
            (net namespace: 自己的網路介面)
            (cgroup: 最多 1 CPU, 512Mi memory)
```

### 動手: 容器是一個 process

```bash
# 在 kind cluster 的 worker node 上
docker exec -it k8s-coach-p0-worker bash

# 看所有跑在這個 node 的 container
crictl ps

# 挑一個 container ID,看它的 PID
crictl inspect <container-id> | grep -i pid

# 在 host 上用這個 PID 找到它
ps aux | grep <pid>
# 它就是一個普通的 Linux process!
```

引導問題: 「這個 container 裡的 process 在 host 上是什麼?它和普通 process 的差異是什麼?」
(答案: 它就是一個 process,差異只有它的 namespace 和 cgroup 屬性被設定了。)

### 打穿底層 (First-Principles Dive)

**這個直覺為 P1 的所有內容打底**:

- `resources.requests/limits` in Pod spec → 底下就是 cgroup 的設定(`cpu.shares`, `memory.limit_in_bytes`)
- Pod 的網路隔離 → 底下是 network namespace + veth pair
- `kubectl exec` 進 container → 底下是 `nsenter` 進入那個 process 的 namespace

**遷移題**: 「如果容器共用 host 的 kernel,而 kernel 有個嚴重漏洞,這對容器的安全隔離有什麼影響?和 VM 比起來呢?」

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 一個 Pod 把整個 Node 的記憶體吃光,導致其他 Pod 被 OOM kill |
| **生產怎麼做** | 一定要幫 Pod 設 `resources.limits.memory`。這讓 kubelet 替每個 container 建立 cgroup,限制記憶體上限。超過上限 → kernel OOM killer 只 kill 這個 container,不影響別人 |
| **真實踩坑** | 只設 `requests` 沒設 `limits`,Pod 跑到後來把 Node 的記憶體吃光。OOM killer 開始隨機 kill process,包括其他 Pod 的 container、甚至可能 kill kubelet 本身,導致整個 Node 失去聯繫 |
| **面試怎麼問** | 「容器和 VM 的隔離機制有什麼本質差別?k8s 的 resource limits 底下對應 Linux 的哪個機制?」 |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| Linux namespace | /ˈlɪnʌks ˈneɪm.speɪs/ | A kernel feature that isolates system resources, giving each container its own view | 讓 container「看不到」host 和其他 container 的資源 |
| cgroup | /ˈsiː.ɡruːp/ | Control Groups: a kernel feature that limits and accounts for resource usage | 限制 container「能用多少」CPU 和記憶體 |
| OOM killer | /oʊ oʊ ɛm ˈkɪlər/ | The Linux kernel mechanism that kills processes when memory is exhausted | 記憶體不夠時,kernel 選一個 process 殺掉 |
| CRI | /siː ɑːr aɪ/ | Container Runtime Interface: the API kubelet uses to manage containers | kubelet 和 container runtime 說話的標準介面(containerd, CRI-O) |

---

## Chaos Drill Hooks (P0)

> 完整腳本在 `references/chaos-drills.md`。這裡是 P0 適用的兩個場景鉤子。

### Drill P0-1: 刪除 Static Pod Manifest,觀察 kubelet 反應

**場景**: Static pod 的 manifest 被刪除了,觀察 kubelet 怎麼反應。

```bash
# 進入 control plane node
docker exec -it k8s-coach-p0-control-plane bash

# 備份並移走 kube-scheduler 的 manifest
cp /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/kube-scheduler.yaml.bak
rm /etc/kubernetes/manifests/kube-scheduler.yaml

# 觀察: scheduler Pod 消失了
# (在另一個 terminal 跑 kubectl get pods -n kube-system -w)
```

引導問題給學員: 「scheduler 消失了。如果現在建一個新的 Pod,它會發生什麼?現有的 Running Pod 會怎樣?」

```bash
# 測試: 建一個新 Pod
kubectl run test-pod --image=nginx
kubectl get pod test-pod  # 預期: Pending (沒有 scheduler 可以分配)

# 現有 Pod 不受影響,因為 reconcile 只在物件狀態改變時啟動

# 恢復
cp /tmp/kube-scheduler.yaml.bak /etc/kubernetes/manifests/kube-scheduler.yaml
# 幾秒後 scheduler 恢復,test-pod 被調度並進入 Running
kubectl delete pod test-pod
```

**學習點**: Static pod 的 manifest 消失,kubelet 就移除那個 Pod。manifest 恢復,kubelet 重建。這是 kubelet 直接管理 static pod 的 reconcile loop。

### Drill P0-2: Cordon 一個 Node,觀察調度行為

**場景**: 一個 node 被標記為不可調度,觀察新 Pod 的去向。

```bash
# 看目前有哪些 node
kubectl get nodes

# cordon 一個 worker node(標記為不可調度)
kubectl cordon k8s-coach-p0-worker

# 建幾個新 Pod
kubectl create deployment test-cordon --image=nginx --replicas=3

# 觀察: 新 Pod 只會跑在 control-plane node(或其他未被 cordon 的 node)
kubectl get pods -o wide
```

引導問題: 「cordon 只影響新 Pod 還是也影響現有 Pod?如果要把現有 Pod 也趕走,該怎麼做?」
(答案: cordon 只影響新調度,不動現有 Pod。drain 才會驅逐現有 Pod。)

```bash
# 清理
kubectl delete deployment test-cordon
kubectl uncordon k8s-coach-p0-worker
```

---

## P0 畢業 Gate

**條件**: 學員能不看任何筆記,白板畫出以下完整流程並口頭解釋每個步驟。

**考核格式**: 「從 `kubectl apply -f pod.yaml` 到 Pod 狀態變成 Running,每個參與的元件依序做了什麼?包括 authn/authz/admission、etcd 寫了幾次、scheduler 怎麼選 node、kubelet 怎麼啟動 container。」

**Pass 條件**:
- 所有元件都點到(API server、etcd、scheduler、kubelet、CRI)
- 正確描述 API server 的三道關卡(authn、authz、admission)
- 說得清楚 scheduler 是 watch 到 unscheduled pod 才開始工作,不是被 API server「呼叫」
- 知道 kubelet 是通過 watch 發現被分配到自己 node 的 Pod
- 知道整個過程 etcd 被寫了兩次(第一次存 Pod 物件,第二次 scheduler 更新 nodeName)

**Stretch (加分,不強求)**:
- 能說出 level-triggered 和 reconcile loop 在哪裡體現
- 能說出 Raft quorum 為什麼讓 etcd 成為可靠的 source of truth

**Gate 失敗處理**: 見 SKILL.md Phase Gate Failure 協議。通常弱點是 scheduler 和 kubelet 的分工,或 API server 的 admission control 細節。對症重練 C-2/C-3。

---

## Portfolio 整合 (P0 第一堂)

**P0 的第一堂要初始化 `k8s-portfolio` repo**:

```bash
# 在本機建立 portfolio repo
mkdir k8s-portfolio
cd k8s-portfolio
git init
git checkout -b main

# 建立目錄結構
mkdir -p manifests observability terraform-eks gitops

# 第一個 artifact: apply→Running 流程圖
# 學員親手把上面的 ASCII 圖抄進去,並加上自己的注解
# 這個動作讓學員「主動輸出」,強化記憶,也是面試作品
cat > manifests/README.md << 'EOF'
# K8s Apply→Running Flow

[學員自己補充白板圖和注解]
EOF

git add .
git commit -m "init: k8s-portfolio, P0 apply-to-running diagram"
```

**P0 的唯一必出 artifact**: `kubectl apply` 到 Pod Running 的流程圖,含每個元件的職責說明。這是學員自己用 Mermaid 或 ASCII art 畫的,commit 到 `k8s-portfolio/manifests/README.md`。

---

## P0 英文 Ramp (術語卡總結)

P0 階段只做術語卡(EN term + 發音 + 英文定義 + 中文點破),全部同步進 `workspaces/k8s/term-registry.md`。

本 phase 累積的術語:

| 主題 | 術語 |
|------|------|
| C-0 宣告式 | declarative, idempotent, desired state |
| C-1 Reconcile | reconcile, controller, level-triggered, watch |
| C-2 Control Plane | control plane, kubelet, static pod, CRI |
| C-3 Apply 流程 | scheduler, admission control, authn, authz, unscheduled pod |
| C-4 etcd | etcd, Raft, quorum, source of truth |
| C-5 容器底層 | Linux namespace, cgroup, OOM killer, CRI |

共 20 個術語,陸續進 term-registry.md 做間隔抽考。
