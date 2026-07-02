# Chaos Drill 故障注入腳本庫

> **如何使用此檔:** 對應 Teaching Flow E 段(故障注入 Drill)。每個 drill 是一個獨立的「弄壞→限時 debug」單元。
> 學員在 D 段看過正常狀態後,E 段注入故障,限時定位根因。
> 每次 drill 踩坑記進 `k8s-coach-workspace/mistake-registry.md`。

---

## Drill 格式範本

每個 drill 固定用以下結構撰寫,確保格式一致、Coach 可直接套用:

```
### [Drill ID]: [標題]

**適用 phase**: P?

**前置條件**: 學員已完成的 chunk + 環境狀態

**破壞腳本** (Coach 執行,學員觀察症狀):
[具體指令]

**預期症狀** (學員先描述看到什麼,不直接說根因):
[kubectl/log 會出現什麼]

**限時** (回合制,非分鐘):
[N 回合內定位根因;一個「回合」= 學員提出一個假設 + 驗證指令 + 觀察結果]

**引導問題** (Coach 用的 Socratic 問題):
[一步一步引導,不直接給答案]

**正解**:
- 根因: [底層發生什麼]
- 修法: [怎麼恢復]
- 驗證修好了: [確認指令]

**學到的底層原理**:
[這個 drill 連回哪個 OS/網路/控制理論原理]
```

---

## P0 Drills

### P0-1: 刪除 Static Pod Manifest,觀察 kubelet 反應

**適用 phase**: P0

**前置條件**: 學員已完成 C-2(Control Plane 拆解),知道 static pod 由 kubelet 直接管理,不需要 API server 存活。環境: `k8s-coach-p0` kind cluster 已起。

**破壞腳本** (Coach 執行,學員先不看):
```bash
# 進入 control plane 節點
docker exec -it k8s-coach-p0-control-plane bash

# 備份,然後移走 kube-scheduler 的 static pod manifest
cp /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/kube-scheduler.yaml.bak
rm /etc/kubernetes/manifests/kube-scheduler.yaml
```

**預期症狀**:
```
# 學員在另一個 terminal 觀察到:
kubectl get pods -n kube-system -w
# kube-scheduler-k8s-coach-p0-control-plane 消失
# (幾秒內,kubelet 偵測到 manifest 不見,移除 Pod)

# 嘗試建新 Pod:
kubectl run test-pending --image=nginx
kubectl get pod test-pending
# NAME           READY   STATUS    RESTARTS   AGE
# test-pending   0/1     Pending   0          30s
# (一直 Pending,沒有 scheduler 能分配 Node)

# 現有 Running Pod 不受影響
kubectl get pods -A
# 其他 Pod 還是 Running
```

**限時**: 5 回合內定位根因(「為什麼新 Pod Pending?」)

**引導問題** (Coach 用):
1. 「新 Pod 卡在 Pending。你先看什麼?」(期望: kubectl describe pod 看 Events)
2. 「Events 顯示什麼?能看到 scheduler 有沒有嘗試分配?」(期望: 看到 `0/1 nodes available: 1 node(s) had untolerated taint`)
3. 「現有 Pod 還在跑,這說明什麼?」(期望: 現有 Pod 不需要 scheduler,只有「新建的」才需要)
4. 「回頭想想,scheduler 是什麼角色?誰在管它?」(期望: scheduler 是 static pod,kubelet 管)
5. 「kubelet 怎麼知道要跑 scheduler?如果 manifest 消失了,kubelet 會怎樣?」(期望: level-triggered reconcile,manifest 沒了就移除 Pod)

**正解**:
- 根因: `/etc/kubernetes/manifests/kube-scheduler.yaml` 被刪除,kubelet 偵測到 manifest 消失(level-triggered reconcile),移除了 kube-scheduler static pod。沒有 scheduler,新 Pod 無法被分配 Node,永遠 Pending。
- 修法:
```bash
# 在 control plane 節點內
cp /tmp/kube-scheduler.yaml.bak /etc/kubernetes/manifests/kube-scheduler.yaml

# 幾秒後 scheduler 重起
kubectl get pods -n kube-system | grep scheduler
```
- 驗證修好了:
```bash
# test-pending 應該很快被調度並變 Running
kubectl get pod test-pending -w

# 清理
kubectl delete pod test-pending
```

**學到的底層原理**:
1. kubelet 的 reconcile loop(level-triggered): 不斷比對 `/etc/kubernetes/manifests/` 目錄和實際跑的 Pod,manifest 消失就移除 Pod,manifest 出現就建 Pod。
2. scheduler 和 kubelet 的職責分工: scheduler 只負責「哪個 Pod 去哪個 Node」;kubelet 負責「把分配給我的 Pod 實際跑起來」。scheduler 不在,kubelet 的 running Pod 不受影響,但新 Pod 永遠拿不到 nodeName。
3. static pod 的設計哲學: control plane 元件用 static pod 跑,就算 API server 掛了,kubelet 還能獨立管理這些 Pod(避免「雞生蛋」問題)。

---

### P0-2: Cordon 一個 Node,觀察調度行為

**適用 phase**: P0

**前置條件**: 學員已完成 C-3(apply→Running 全流程),知道 scheduler 的 Filter + Score + Bind 流程。環境: `k8s-coach-p0` kind cluster 已起(需有 worker node,即 kind config 設多 node)。

**破壞腳本** (Coach 執行):
```bash
# 確認目前節點
kubectl get nodes

# 將 worker node 標記為不可調度(cordon)
kubectl cordon k8s-coach-p0-worker
```

**預期症狀**:
```
# cordon 後立刻看到節點狀態:
kubectl get nodes
# NAME                            STATUS                     ROLES
# k8s-coach-p0-control-plane      Ready                      control-plane
# k8s-coach-p0-worker             Ready,SchedulingDisabled   <none>

# 建新 Deployment:
kubectl create deployment test-cordon --image=nginx --replicas=3
kubectl get pods -o wide

# 所有新 Pod 都跑在 control-plane node(或其他未 cordon 的 node)
# cordon 的 worker node 上沒有新 Pod 被調度

# 原本在 worker node 的 Pod 仍然在跑(cordon 不驅逐現有 Pod)
```

**限時**: 3 回合內說出「cordon 影響哪些 Pod,不影響哪些」

**引導問題**:
1. 「你看到 `SchedulingDisabled`,這代表什麼?」(期望: 這個 node 不再接受新 Pod 調度)
2. 「原本在這個 node 上的 Pod 怎麼了?」(期望: 還在跑,沒被動)
3. 「如果要把現有 Pod 也趕走,還需要做什麼?」(期望: drain)
4. 「想想 scheduler 的 Filter 步驟,cordon 在 Filter 層面做了什麼?」(期望: 在節點上加了 `node.kubernetes.io/unschedulable` taint,Pod 沒有對應 toleration 就被 Filter 掉)

**正解**:
- 根因: `kubectl cordon` 給節點加上 `node.kubernetes.io/unschedulable:NoSchedule` taint,同時設 `spec.unschedulable=true`。Scheduler 在 Filter 階段把這個 node 過濾掉,新 Pod 不會被分配來。但 cordon 不驅逐現有 Pod,現有 Pod 繼續跑。
- 修法:
```bash
kubectl uncordon k8s-coach-p0-worker
kubectl get nodes
```
- 驗證修好了:
```bash
# worker node 恢復 Ready 狀態
kubectl get nodes

# 清理
kubectl delete deployment test-cordon
```

**學到的底層原理**:
1. Taint/Toleration 是 scheduler Filter 的一環: cordon 本質上是加一個 system taint。理解了這個,之後學 taints/tolerations 就是同一個概念的延伸。
2. cordon vs drain 的差別: cordon = 封閉入口(不接新 Pod); drain = 封閉入口 + 驅逐現有 Pod(用於節點維護)。兩者都服務「安全下線節點」的場景,但力道不同。
3. Scheduler 的職責邊界: scheduler 只管「新 Pod 去哪」;已經 Running 的 Pod 由 kubelet 管,cordon 不讓 kubelet 做任何事。

---

## P1 Drills

> 共用安全鐵律:每個破壞腳本第一條指令都是 `kubectl config current-context`,輸出必須是 `kind-k8s-coach-p0` 才准往下。機器上有公司 PROD EKS kubeconfig,不確認就 apply 是本 repo 的第一大忌。

### P1-1: Liveness Probe 打錯 Port,殺掉健康的 App

**適用 phase**: P1(冷測複測用)

**前置條件**: 學員已完成 P1 chunk 3(probe)+ chunk 5(exit code 解讀)。**客製註記:學員在 P1 畢業 gate(session 6)親手排過同型題(web-frontend,liveness 打 8080 / nginx 聽 80,從 exit 0 反推「app 健康、被 probe 殺」是他的最佳時刻)。此 drill 定位是冷測複測:換皮重出,看他無鷹架能不能再走一次同樣的推理鏈。**

**破壞腳本** (Coach 執行,學員觀察症狀):
```bash
kubectl config current-context
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-checkout
spec:
  replicas: 1
  selector:
    matchLabels: {app: web-checkout}
  template:
    metadata:
      labels: {app: web-checkout}
    spec:
      containers:
      - name: nginx
        image: nginx:1.27
        livenessProbe:
          httpGet: {path: /, port: 8080}
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
EOF
```

**預期症狀** (學員先描述看到什麼,不直接說根因):
```
kubectl get pods -w
# web-checkout-xxx  1/1  Running  1 (20s ago)   # RESTARTS 每 ~20 秒 +1
# 幾輪後: CrashLoopBackOff

kubectl describe pod -l app=web-checkout
# Events: Liveness probe failed: Get "http://10.244.x.x:8080/": connect: connection refused
# Last State: Terminated / Reason: Completed / Exit Code: 0
```

**限時**: 3 回合內定位根因(複測題,比初見時的 5 回合緊)

**引導問題** (Coach 用的 Socratic 問題):
1. 「RESTARTS 在漲,先看什麼?」(期望: describe 讀 Events + Last State)
2. 「Exit Code 0 是什麼意思?誰會讓一個健康的行程用 0 退出?」(期望: app 正常收尾 = 收到 SIGTERM 優雅退出,不是 crash)
3. 「connection refused 是 app 死了,還是探測的地方根本沒人聽?」(期望: 對照 container port,發現 probe 打 8080、nginx 聽 80)
4. (若卡住)「~20 秒一次 restart,這個數字是哪兩個參數乘出來的?」(期望: failureThreshold 3 × periodSeconds 5 + initialDelay)

**正解**:
- 根因: livenessProbe 的 port(8080)和 nginx 實際監聽的 port(80)不一致。kubelet 每 5 秒探測一次,連續 3 次失敗後判定容器不健康,送 SIGTERM 殺容器。nginx 收到 SIGTERM 優雅退出,所以 Exit Code 0(不是 137)。app 從頭到尾都是健康的,是 probe 設定殺了它。
- 修法:
```bash
kubectl patch deployment web-checkout --type=json -p='[{"op":"replace","path":"/spec/template/spec/containers/0/livenessProbe/httpGet/port","value":80}]'
```
- 驗證修好了:
```bash
kubectl get pods -l app=web-checkout
# 新 Pod RESTARTS 停在 0,觀察 1-2 分鐘不再增加
kubectl delete deployment web-checkout
```

**學到的底層原理**:
1. probe 是 kubelet 在 node 上執行的,不是 API Server:探測結果和殺容器都發生在第 5 棒。
2. exit code 是屍檢第一刀:0 = 收 SIGTERM 優雅退出(被 probe 或 rollout 殺)、137 = 128+9 SIGKILL(OOM 或 grace period 到期硬殺)、1 = app 自己 crash。
3. liveness 的殺傷半徑:設錯的 liveness 是「自動化的自殺開關」,這也是為什麼 liveness 不該去查外部依賴(DB 掛 → 全部 Pod 被殺 → 重連風暴,回扣學員的 thundering herd 術語卡)。
4. 偵測延遲公式 failureThreshold × periodSeconds = 調校旋鈕(學員 P1 chunk 3 推過)。

---

### P1-2: OOMKilled 對照局:容器級 cgroup OOM vs Node 級 Eviction

**適用 phase**: P1

**前置條件**: 學員已完成 P1 chunk 5(requests/limits/QoS/兩種 OOM)。**客製註記:學員做過 oom-demo lab(polinux/stress 要 150M / limit 100Mi,親手讀出 OOMKilled + exit 137 + Burstable + node 仍有餘量)。此 drill 是變體:把他 session 5 只在概念層學過的「node 級驅逐」實體化,和容器級 OOM 並排對照。A 段可 blind:先只丟 describe 輸出,要他判斷是哪種機制殺的。**

**破壞腳本** (Coach 執行,學員觀察症狀):

A 段(容器級,複測,快速過):
```bash
kubectl config current-context
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: mem-eater-a
spec:
  containers:
  - name: stress
    image: polinux/stress
    command: ["stress", "--vm", "1", "--vm-bytes", "150M", "--vm-hang", "0"]
    resources:
      limits: {memory: "100Mi"}
EOF
```

B 段(node 級 eviction):kind node 看到的是宿主機的記憶體,真把記憶體吃爆會傷到宿主機。所以不真吃,改成把 kubelet 的 eviction 門檻調到荒謬高,讓 kubelet「以為」node 缺記憶體:
```bash
# 先放兩隻犧牲品到 worker2:一隻 BestEffort、一隻 Burstable
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: victim-besteffort
spec:
  nodeSelector: {kubernetes.io/hostname: k8s-coach-p0-worker2}
  containers:
  - name: sleep
    image: busybox
    command: ["sleep", "3600"]
---
apiVersion: v1
kind: Pod
metadata:
  name: victim-burstable
spec:
  nodeSelector: {kubernetes.io/hostname: k8s-coach-p0-worker2}
  containers:
  - name: sleep
    image: busybox
    command: ["sleep", "3600"]
    resources:
      requests: {memory: "10Mi"}
EOF

# 備份 kubelet config,把 memory.available 門檻插進 evictionHard 區塊
docker exec k8s-coach-p0-worker2 cp /var/lib/kubelet/config.yaml /var/lib/kubelet/config.yaml.bak
docker exec k8s-coach-p0-worker2 grep -A4 evictionHard /var/lib/kubelet/config.yaml
# 若已有 evictionHard 區塊(kind 預設有,nodefs/imagefs 0%),在區塊下插一行:
docker exec k8s-coach-p0-worker2 sed -i '/evictionHard:/a\  memory.available: "1000Gi"' /var/lib/kubelet/config.yaml
docker exec k8s-coach-p0-worker2 systemctl restart kubelet
```
(若 kubelet 起不來,`docker exec k8s-coach-p0-worker2 cp /var/lib/kubelet/config.yaml.bak /var/lib/kubelet/config.yaml` 還原再 restart。)

**預期症狀**:
```
# A 段:
kubectl get pod mem-eater-a
# STATUS: OOMKilled(或 CrashLoopBackOff),describe 看到 Exit Code 137

# B 段(kubelet restart 後 1-2 分鐘內):
kubectl describe node k8s-coach-p0-worker2 | grep -A2 MemoryPressure
# MemoryPressure  True
kubectl get pods
# victim-besteffort  0/1  Evicted(或 Failed)
kubectl describe pod victim-besteffort
# Status: Failed / Reason: Evicted
# Message: The node was low on resource: memory. ...
# node 還會多一個 taint: node.kubernetes.io/memory-pressure:NoSchedule
```

**限時**: A 段 2 回合(複測);B 段 4 回合(說出「誰殺的、依什麼順序、跟 A 段差在哪」)

**引導問題**:
1. (blind 開場)「這兩份 describe,一個 Reason: OOMKilled Exit 137,一個 Reason: Evicted。是同一個劊子手嗎?」(期望: 不是。kernel cgroup vs kubelet)
2. 「A 段那隻,node 記憶體明明還很多,為什麼死?」(期望: 撞自己的 cgroup limit,和 node 餘量無關,session 5 B段謎題原題)
3. 「B 段誰先死?為什麼是它?」(期望: BestEffort 先,QoS 驅逐序 BestEffort → Burstable → Guaranteed,沒繳訂金的先趕)
4. 「Evicted 的 Pod 有 exit code 137 嗎?」(期望: 沒有,eviction 是 kubelet 走 API 優雅刪 Pod,不是 kernel SIGKILL;兩種死法連屍體長相都不同)

**正解**:
- 根因: A = 容器記憶體超過自己的 cgroup limit,kernel 的 cgroup OOM killer 直接 SIGKILL(exit 137)。B = kubelet 的 eviction manager 認定 node memory.available 低於門檻(被我們造假),進入 MemoryPressure,按 QoS 順序驅逐 Pod 以自保。
- 修法:
```bash
docker exec k8s-coach-p0-worker2 cp /var/lib/kubelet/config.yaml.bak /var/lib/kubelet/config.yaml
docker exec k8s-coach-p0-worker2 systemctl restart kubelet
kubectl delete pod mem-eater-a victim-besteffort victim-burstable --force --grace-period=0
```
- 驗證修好了:
```bash
kubectl describe node k8s-coach-p0-worker2 | grep MemoryPressure
# MemoryPressure False,taint 消失
```

**學到的底層原理**:
1. 兩層防線兩個劊子手:cgroup limit 是 kernel 層合約(超過就地正法,exit 137);eviction 是 kubelet 層的 node 自保(走 API 刪 Pod,屍體是 Evicted 不是 137)。
2. QoS class 唯一發揮作用的時刻就是 node 級壓力:BestEffort 沒繳訂金先死,Guaranteed 有硬約定最後死(學員 session 10 自己講對過理由)。
3. 真實世界還有第三層:kubelet 來不及反應時,kernel 全域 OOM killer 會直接出手殺 node 上任何行程(含 kubelet 自己)。kind 上不演這層(會傷宿主機),思想實驗帶過:這就是為什麼 requests 要接近真實用量,讓 scheduler 別把 node 塞爆。

---

### P1-3: ImagePullBackOff 三選一 Blind 抽考

**適用 phase**: P1

**前置條件**: 學員已完成 P1 chunk 4(rollout / 驗證邊界)。**客製註記:學員 session 6 gate 排過 tag 不存在(nginx:1.99)、session 7 A 段抽考三類根因訊號全對(repo-not-exist / connection-refused / 401)。此 drill 設計成 blind 三選一:Coach 擲骰抽一個變體注入,學員只准看 kubectl 輸出,要在指定回合內講出是三類中的哪一類 + 證據字樣。[RUNTIME: 若 mistake-registry 顯示某類他答錯過,優先抽那類]**

**破壞腳本** (Coach 執行,擲骰抽一,學員不看):
```bash
kubectl config current-context
# V1: tag 不存在(registry 連得上,但沒這個版本)
kubectl run checkout-svc --image=nginx:1.99
# V2: registry 不通(TCP 層連不上)
kubectl run checkout-svc --image=127.0.0.1:5000/nginx:latest
# V3: 認證/授權被拒(連上了,HTTP 層說不行)
kubectl run checkout-svc --image=docker.io/library/internal-billing-api:latest
```

**預期症狀**:
```
kubectl get pod checkout-svc
# STATUS: ErrImagePull → ImagePullBackOff

kubectl describe pod checkout-svc   # 三個變體的 Events 關鍵字樣:
# V1: manifest for nginx:1.99 not found: manifest unknown
# V2: dial tcp 127.0.0.1:5000: connect: connection refused
# V3: pull access denied ... repository does not exist or may require 'docker login'
#     (401/unauthorized/denied/toomanyrequests 都算這一類:HTTP 層被拒)
```

**限時**: 每變體 2 回合(get 全景 + describe 讀 Events 就該收掉)

**引導問題**:
1. 「先回答一個二分題:kubelet 到底有沒有連上 registry?證據是哪個字?」(期望: connection refused = 沒連上;manifest unknown / denied = 連上了)
2. 「連上了的話,registry 說了什麼?404 跟 401 差在哪一層?」(期望: 404 = 名字空間裡沒這個 tag;401/denied = 有沒有先不告訴你,先驗明正身)
3. 「這個錯誤為什麼 kubectl apply 當下抓不到?」(期望: 驗證邊界,session 4 金句:schema 錯 API Server 當場擋,image 在不在只有 kubelet 第 5 棒去拉才知道)

**正解**:
- 根因: 三類分別是 tag 不存在(registry 回 manifest unknown)、registry TCP 不可達(dial timeout/refused)、HTTP 401/403 被拒(缺 imagePullSecrets、token 過期、或 rate limit toomanyrequests)。
- 修法: V1 改成存在的 tag;V2 修 registry 位址或網路;V3 建 docker-registry secret 並在 Pod spec 掛 imagePullSecrets。
- 驗證修好了:
```bash
kubectl delete pod checkout-svc
kubectl run checkout-svc --image=nginx:1.27 && kubectl get pod checkout-svc -w
kubectl delete pod checkout-svc
```

**學到的底層原理**:
1. 排障邏輯是二叉樹不是清單:第一刀切「TCP 有沒有通」,第二刀切「registry 回了什麼 HTTP 狀態」。這比背三種錯誤訊息可遷移(同一棵樹適用於任何 client 對 server 的故障)。
2. 驗證邊界:宣告式系統只在「碰到外部現實」的那一棒才發現外部錯誤。image 的外部現實在 kubelet/runtime。
3. BackOff 是指數退避(exponential backoff):失敗重試間隔翻倍,保護 registry 不被打爆。之後在 CrashLoopBackOff 看到的是同一個模式。

---

## P2a Drills

> 前置環境共通:kind 叢集已起,先 `kubectl config current-context` 確認是 `kind-k8s-coach-p0`(P2a-3 用 Calico 叢集 `kind-k8s-coach-p2a`,見 phase-2a 教材)。建議部署一組 backend Deployment(2 副本)+ ClusterIP Service + 一個 client Pod(nginx 或 agnhost,別用 busybox,學員踩過它的 nslookup 坑)。

### P2a-1: CoreDNS 副本縮到 0(名字死了,IP 還活著)

**適用 phase**: P2a

**前置條件**: 學員已畢業 chunk 1(Service/kube-proxy/CoreDNS)。client Pod 平常用 service 名字打 backend。

**破壞腳本** (Coach 執行,學員先不看):
```bash
kubectl -n kube-system scale deployment coredns --replicas=0
```

**預期症狀**:
```bash
# client Pod 內:
kubectl exec client -- curl -s --max-time 3 http://backend-svc
# curl: (6) Could not resolve host: backend-svc

# 但拿 Service 的 ClusterIP 直打:
kubectl get svc backend-svc -o wide
kubectl exec client -- curl -s --max-time 3 http://<ClusterIP>
# 正常回應!
```

**限時**: 4 回合內定位根因。

**引導問題** (Coach 用,對準學員的層級混淆前科):
1. 「兩個 curl,一個死一個活。它們走的路徑差在哪一段?」(期望: 名字→IP 是 DNS 層,IP→Pod 是 DNAT/連線層;死的只有 DNS 層)
2. 「所以問題在哪一層?conntrack 有嫌疑嗎?」(期望: 沒有,conntrack 在連線層,這題是解析層。答錯=層級混淆復發,記 registry)
3. 「DNS 層的下一步查什麼?」(期望: CoreDNS Pod 活著嗎 → `kubectl -n kube-system get pods -l k8s-app=kube-dns`)
4. 「resolv.conf 裡的 nameserver IP 還在嗎?為什麼 IP 在、解析卻死?」(期望: 那是 kube-dns Service 的 ClusterIP,Service 還在但 Endpoints 空了)

**正解**:
- 根因: CoreDNS 副本 0,kube-dns Service 的 Endpoints 清空。Pod 的 resolv.conf 指向的 ClusterIP 沒變,但 DNAT 找不到任何後端,DNS query 無人應答。IP 直連不經 DNS,完全不受影響。
- 修法: `kubectl -n kube-system scale deployment coredns --replicas=2`
- 驗證: `kubectl exec client -- nslookup backend-svc.default.svc.cluster.local` 恢復解析,curl 名字恢復通。

**學到的底層原理**:
1. 「連不上」永遠先切層:名字解析(DNS)、封包轉發(DNAT/路由)、應用回應(HTTP)是三段獨立的故障域。第一刀=「換 IP 直打通不通」。
2. DNS 掛掉的爆炸半徑:所有「用名字」的東西一起死,長得像全站故障,其實只壞了一層。
3. kube-dns 也只是一個 Service + Endpoints:整套 chunk 1 的機制(reconcile、Endpoints、DNAT)原封不動適用在 DNS 自己身上。

---

### P2a-2: 清空單一 node 的 KUBE-SERVICES 鏈(去中心化的實體證明)

**適用 phase**: P2a

**前置條件**: 學員已親手追過 iptables DNAT 鏈(session 9 D 段),知道每台 node 各有一份規則。本 drill 是該知識的複測。

**破壞腳本** (Coach 執行):
```bash
# 只在 worker 上清掉 KUBE-SERVICES 進入點(nat 表)
docker exec k8s-coach-p0-worker iptables -t nat -D PREROUTING -m comment --comment "kubernetes service portals" -j KUBE-SERVICES
docker exec k8s-coach-p0-worker iptables -t nat -D OUTPUT -m comment --comment "kubernetes service portals" -j KUBE-SERVICES
```

**預期症狀**:
```bash
# 跑在 worker 上的 Pod 打 Service:不通(ClusterIP 沒人改寫,封包射向不存在的虛擬 IP)
# 跑在 worker2 上的 Pod 打同一個 Service:正常
# 直打 Pod IP:兩台都通(DNAT 壞了,CNI 路由沒壞)
kubectl get pods -o wide   # 先確認 client 在哪台 node
```

**限時**: 5 回合內定位到「只有某台 node 的 DNAT 壞了」。

**引導問題**:
1. 「同一個 Service,A Pod 通、B Pod 不通。兩個 Pod 差在什麼?」(期望: 所在 node 不同)
2. 「這說明壞掉的東西是全叢集共享的,還是 per-node 的?」(期望: per-node → 指向每台 node 自己的 iptables 規則)
3. 「去哪確認?」(期望: `docker exec <node> iptables-save -t nat | grep KUBE-SERVICES`,兩台對比)
4. 「誰負責把規則寫回來?它多久會修?」(期望: 該 node 的 kube-proxy,reconcile 會補,但預設靠 sync 週期/事件觸發)

**正解**:
- 根因: worker 的 nat 表 PREROUTING/OUTPUT 不再跳 KUBE-SERVICES,該 node 上的封包不會被 DNAT,ClusterIP 變成死 IP。其他 node 各有自己的規則,不受影響。這就是「去中心化、無單點」的反面證明:壞也只壞一台。
- 修法: 重啟該 node 的 kube-proxy Pod 讓它重寫規則:`kubectl -n kube-system delete pod -l k8s-app=kube-proxy --field-selector spec.nodeName=k8s-coach-p0-worker`
- 驗證: 兩台 node `iptables-save -t nat | grep -c KUBE` 數量回到同一量級;worker 上的 Pod curl Service 恢復。

**學到的底層原理**:
1. kube-proxy 是「每台 node 一份」的規則寫手:故障域是 per-node。症狀呈現「部分 Pod 不通」時,先問「不通的 Pod 有什麼共同點」。
2. kube-proxy 也是 reconcile loop:刪掉它的 Pod,DaemonSet 補一個新的,新 Pod 啟動時全量重寫 iptables,這就是 level-triggered 的修復(不需要知道規則怎麼消失的)。
3. `kubectl` 看不到 iptables:又一次驗證「conntrack/iptables 是 node kernel 的東西,不是 k8s 物件」(學員 session 9 釘過的觀念)。

---

### P2a-3: default-deny 忘了開 DNS egress(和 P2a-1 撞症狀的對照題)

**適用 phase**: P2a(chunk 3 NetworkPolicy 之後;需 Calico 叢集 `kind-k8s-coach-p2a`)

**前置條件**: 學員已學 NetworkPolicy 語義,做過 default-deny lab。CoreDNS 健康。

**破壞腳本** (Coach 執行,偽裝成「上了一個安全需求」):
```bash
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: client-egress-lockdown
spec:
  podSelector:
    matchLabels:
      app: client
  policyTypes: ["Egress"]
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - port: 80
EOF
```

**預期症狀**:
```bash
kubectl exec client -- curl -s --max-time 3 http://backend-svc
# curl: (6) Could not resolve host: backend-svc   <-- 和 P2a-1 一模一樣!
kubectl exec client -- curl -s --max-time 3 http://<backend Pod IP>
# 直打 Pod IP 80 port:通!(policy 有允許到 backend 的 80)
```

**限時**: 5 回合。重點考「症狀同、根因異」的分辨。

**引導問題**:
1. 「症狀跟上次 CoreDNS 那題一樣。先照舊 SOP:CoreDNS Pod 活著嗎?Endpoints 有嗎?」(期望: 都健康 → 上次的根因排除,不能靠背答案)
2. 「解析是 client 發 UDP 53 到 CoreDNS。這條路上,最近有什麼改變?」(期望: 剛 apply 的 egress policy)
3. 「這條 policy 允許了什麼?沒允許什麼?」(期望: 只允許到 backend:80;egress 一旦有 policy 選中 Pod,沒列的全 deny,53 到 kube-system 沒開)
4. 「怎麼證明?」(期望: 拿掉 policy 或補 DNS egress 規則後立刻恢復)

**正解**:
- 根因: NetworkPolicy 是白名單語義:Pod 一旦被任何 Egress policy 選中,只有列出的目的地放行。DNS(UDP/TCP 53 到 kube-system 的 CoreDNS)沒列,解析全死。
- 修法: policy 補一段 egress 到 kube-system 的 53(namespaceSelector `kubernetes.io/metadata.name: kube-system` + port 53 UDP/TCP)。
- 驗證: curl 名字恢復;`kubectl exec client -- nslookup backend-svc` 通。

**學到的底層原理**:
1. 症狀不是根因:同一個 `Could not resolve host` 至少有三種根因(DNS server 死、UDP 53 被擋、resolv.conf 壞)。排查是走樹,不是背表。
2. default-deny 的第一受害者永遠是 DNS:這是生產上 NetworkPolicy 上線事故的第一名,任何 egress 白名單都要先想 DNS。
3. NetworkPolicy 由 CNI 執行:kindnet 會靜默忽略它(apply 成功≠生效),Calico 才會真的擋。「物件=規則,引擎=CNI」,又是規則 vs 引擎模式。

---

### P2a-4: Ingress 404 三段變體(排障階梯實戰)

**適用 phase**: P2a(chunk 2 Ingress lab 之後)

**前置條件**: ingress-nginx 已裝,學員做過 host/path 分流 lab。

**破壞腳本** (Coach 每輪挑一個變體,學員 blind):
```bash
# 變體 A:Ingress rule 的 host 改掉(shop.com -> shop.internal)
# 變體 B:backend service 名字改成不存在的(backend-svc -> backend-svv)
# 變體 C:把 backend Deployment 的 readiness 弄壞(Endpoints 變空)
kubectl edit ingress shop-ingress   # A/B 用 edit;C 用 patch probe
```

**預期症狀**:
```
A:curl -H "Host: shop.com" http://localhost:8080/api  -> 404(nginx default backend)
B:apply 時不報錯!curl -> 503
C:curl -> 503,Ingress/Service 設定看起來全對
```

**限時**: 每個變體 4 回合。

**引導問題**(排障階梯,由外往內):
1. 「404 和 503 分別是誰回的?」(期望: 都是 nginx(controller)回的,404=沒有 rule 匹配,503=rule 匹配了但沒有可用 upstream)
2. 「404 → 查什麼?」(期望: rule 的 host/path 跟請求對不對得上)
3. 「503 → 查什麼?」(期望: service 名字存在嗎 → `kubectl get svc`;Endpoints 有 IP 嗎 → `kubectl get endpoints`)
4. 變體 B 專用:「為什麼 apply 一個指向不存在 service 的 Ingress 不報錯?」(期望: 驗證邊界,API Server 只驗 schema,外部現實(service 存不存在)是 controller runtime 才碰到。回扣 P1 nginx:1.99 的同款金句)

**正解**:
- 根因: A=無 rule 匹配落到 default backend;B=upstream 不存在;C=upstream 存在但 Endpoints 空(readiness gate)。
- 修法: 對症修 host / service 名 / probe。
- 驗證: curl 回 200,`kubectl describe ingress` 的 backends 欄有 Pod IP。

**學到的底層原理**:
1. HTTP 狀態碼是 L7 引擎給的線索:404=路由層沒匹配、503=匹配了但後端池空。先讀狀態碼再動手,少走一半冤路。
2. Ingress 的資料鏈:rule → service 名 → Endpoints → Pod IP,nginx.conf 的 upstream 直接 render Endpoints(繞過 kube-proxy)。鏈上每一節都可能斷,排查就是沿鏈走。
3. readiness 的第三次出場:P1(RESTARTS 0 但被摘)、chunk 1(Endpoints 閘門)、這裡(503)。同一個機制,三種症狀面孔。

---

### P2a-5: conntrack 壓滿(理論實體化)

**適用 phase**: P2a(chunk 1 謎題C 之後任何時點;適合當複測)

**前置條件**: 學員已懂 conntrack 理論:「table full 時新連線被 drop、舊連線照常」(此精準度曾掉過,本 drill 就是實體化驗收)。

**破壞腳本** (Coach 執行,在 worker node 上把 conntrack 上限調到極小):
```bash
docker exec k8s-coach-p0-worker sysctl -w net.netfilter.nf_conntrack_max=128
# 然後從 client Pod 對 Service 開併發連線(client 需在 worker 上)
kubectl exec client -- sh -c 'for i in $(seq 1 200); do (curl -s -o /dev/null --max-time 2 http://backend-svc &) ; done; wait'
```

**預期症狀**:
```bash
# 部分 curl timeout / 失敗;既有連線(先開的)不受影響
docker exec k8s-coach-p0-worker dmesg | tail | grep conntrack
# nf_conntrack: nf_conntrack: table full, dropping packet
docker exec k8s-coach-p0-worker sh -c 'cat /proc/sys/net/netfilter/nf_conntrack_count /proc/sys/net/netfilter/nf_conntrack_max'
```

**限時**: 4 回合(理論已學過,考的是「第一個指令選對」)。

**引導問題**:
1. 「新連線失敗、舊連線正常。這個對比指紋指向哪個機制?」(期望: 連線追蹤表滿了,新 entry 進不來)
2. 「用什麼證明?在哪裡跑?」(期望: node 上(不是 kubectl!)看 count vs max、dmesg。`kubectl get conntrack` 不存在,學員 session 9 犯過)
3. 「為什麼 DNAT 一定需要這張表?」(期望: 回程封包要查表改回來源 IP,雙向改寫)
4. 「生產上的修法,治標和治本各是什麼?」(期望: 治標=調大 nf_conntrack_max;治本=找出誰在狂開短連線(timeout 過長/連線風暴),學員的「主動講治標治本」訓練點)

**正解**:
- 根因: conntrack table 滿,kernel 對「需要新建 entry 的封包」直接 drop;既有 entry 的封包照常轉發。
- 修法: `sysctl -w net.netfilter.nf_conntrack_max=131072`(還原);根因面檢討連線模式。
- 驗證: dmesg 不再出現 table full;curl 全數成功。

**學到的底層原理**:
1. 「新的死、舊的活」是一種故障指紋:資源池滿(conntrack、port、accept queue)都長這樣;反過來「全死」通常是路斷了。
2. conntrack 是 node kernel 的 netfilter 狀態,kubectl 永遠看不到;排查工位在 node,不在 API Server。
3. 這張表是 NAT 的必需品不是優化:沒有 entry,回程封包無法還原,連線必斷。

---

## P2b Drills

### P2b-1: PVC 永遠 Pending(三個變體)

**適用 phase**: P2b

**前置條件**: 學員已學 PV/PVC/StorageClass 動態供應。kind 內建 `standard` StorageClass(local-path,WaitForFirstConsumer)。

**破壞腳本** (Coach 挑一個變體):
```bash
# 變體 A:storageClassName 打錯(standard -> standrad)
# 變體 B:PVC 正確,但一直沒有 Pod 使用它(WaitForFirstConsumer 的「假故障」)
# 變體 C:叢集沒有 default StorageClass,PVC 又完全不寫 storageClassName
#   (Coach 先偷偷摘掉 default 註記:)
kubectl annotate sc standard storageclass.kubernetes.io/is-default-class-
kubectl apply -f pvc-demo.yaml
```

**預期症狀**:
```bash
kubectl get pvc
# NAME   STATUS    VOLUME   ...
# data   Pending
kubectl describe pvc data   # A: 沒有對應 provisioner 的事件;B: waiting for first consumer to be created
                            # C: Events 出現 no persistent volumes available for this claim and no storage class is set
```

**限時**: 4 回合。

**引導問題**:
1. 「PVC Pending,第一個指令?」(期望: describe 看 Events,和 Pod Pending 同一套肌肉)
2. 「Events 說 waiting for first consumer,這是故障嗎?」(期望: 不是,是 WaitForFirstConsumer 的正常行為:等 Pod 排定 node 才決定在哪供應)
3. 「如果 Events 什麼都沒有呢?」(期望: 查 StorageClass 名字存不存在:`kubectl get sc`;沒人認領的 PVC 永遠掛著)
4. 「為什麼打錯 SC 名字不會報錯?」(期望: 驗證邊界,schema 合法;SC 存不存在是 provisioner runtime 的外部現實)
5. (變體 C)「PVC 沒寫 storageClassName 時,平常為什麼還能動?今天為什麼不動?」(期望: 平常靠 default SC 的 admission 補值;`kubectl get sc` 看 NAME 旁的 `(default)` 標記不見了,沒 default 就沒人補、沒人認領)

**正解**:
- 根因: A=指向不存在的 StorageClass,沒有 provisioner 認領;B=非故障,binding 延遲到第一個 consumer 出現;C=沒有 default SC 可補值,PVC 的 storageClassName 為空,永遠沒有 provisioner 認領。
- 修法: A 改回正確 SC 名;B 建一個掛載該 PVC 的 Pod;C 恢復 default 註記 `kubectl annotate sc standard storageclass.kubernetes.io/is-default-class=true`(或 PVC 明寫 SC 名)。注意 default 補值發生在 PVC 建立當下(admission),先建的 PVC 不會回頭吃到,要重建。
- 驗證: `kubectl get pvc` 變 Bound,`kubectl get pv` 出現動態供應的 volume。

**學到的底層原理**:
1. PVC binding 也是 reconcile:PVC 是宣告,provisioner 是引擎;引擎不存在時宣告永遠懸置,和 Ingress 沒 controller 完全同構。
2. Pending 有兩種:真故障(沒人認領)與設計行為(等 consumer)。分辨靠 Events,不靠猜。
3. WaitForFirstConsumer 的存在理由:儲存有拓撲(EBS 綁 AZ),先排 Pod 再供應 volume 才不會供錯地方。

---

### P2b-2: RBAC 403(權限的最小反例)

**適用 phase**: P2b

**前置條件**: 學員已學 Role/RoleBinding/ServiceAccount 四象限。

**破壞腳本** (Coach 執行,建一個「看得到自己 namespace 的 Pod、卻拿不到 logs」的 SA):
```bash
kubectl create sa app-reader
kubectl create role pod-viewer --verb=get,list --resource=pods
kubectl create rolebinding app-reader-bind --role=pod-viewer --serviceaccount=default:app-reader
```

**預期症狀**:
```bash
kubectl auth can-i list pods --as=system:serviceaccount:default:app-reader          # yes
kubectl auth can-i get pods --subresource=log --as=system:serviceaccount:default:app-reader   # no
# 用該 SA 的應用呼叫 logs API 時收到:
# Error from server (Forbidden): pods "backend-xxx" is forbidden: User "system:serviceaccount:default:app-reader" cannot get resource "pods/log"
```

**限時**: 4 回合。

**引導問題**:
1. 「403 的錯誤訊息裡,資訊密度最高的是哪幾個字?」(期望: User 是誰、動詞、resource `pods/log`:subresource 是獨立授權點)
2. 「不用試錯,怎麼系統性確認這個 SA 能做什麼?」(期望: `kubectl auth can-i --list --as=system:serviceaccount:default:app-reader`)
3. 「修法是給 cluster-admin 嗎?」(期望: 不是,補 `pods/log` 這一個 subresource 就好,最小權限)
4. 「RBAC 擋下請求時,Pod 會被殺嗎?」(誘答複用:不會,RBAC 只活在 API Server 的 authz 關卡,跟 runtime 無關)

**正解**:
- 根因: `pods/log` 是 subresource,`get pods` 的授權不涵蓋它。
- 修法: role 的 resources 加 `pods/log`。
- 驗證: `kubectl auth can-i get pods --subresource=log --as=...` 變 yes。

**學到的底層原理**:
1. RBAC 是 allow-only 聯集:預設全拒,規則只加不減;排查方向永遠是「缺哪一條」,不是「哪一條擋了我」。
2. subresource(pods/log、pods/exec、deployments/scale)是常見盲點,也是最小權限設計的精度所在。
3. `--as` impersonation 是 RBAC 排障的正規工具:不用登入對方身分就能驗證權限,生產排查零風險。

---

### P2b-3: IRSA token 拿不到(EKS 限定,可桌演)

**適用 phase**: P2b。**kind 做不了**(沒有 OIDC provider 與 AWS STS),EKS lab 開了才實跑,否則當思想實驗桌演。

**前置條件**: 學員已學 IRSA 鏈(SA annotation → token projection → STS AssumeRoleWithWebIdentity)。

**破壞腳本**(兩個變體):
```
變體 A:SA 少了 eks.amazonaws.com/role-arn annotation
變體 B:annotation 正確,但 IAM role 的 trust policy 的 sub 條件寫錯 namespace
```

**預期症狀**:
```
A:Pod 內 AWS SDK 走 credential chain 找不到 web identity,fallback 到 node role(或直接 NoCredentialProviders)
B:STS 回 AccessDenied: Not authorized to perform sts:AssumeRoleWithWebIdentity
```

**限時**: 5 回合(桌演:口頭走完排查鏈)。

**引導問題**:
1. 「先分辨:是『沒拿到 token』還是『拿了 token 被 STS 拒絕』?」(期望: 看錯誤訊息來源,SDK 層 vs STS 層,又是切層)
2. 「A 的檢查點?」(期望: `kubectl get sa <name> -o yaml` 看 annotation;`kubectl exec` 進 Pod 看 `AWS_WEB_IDENTITY_TOKEN_FILE` 環境變數有沒有被 webhook 注入)
3. 「B 的檢查點?」(期望: IAM role trust policy 的 Condition:`sub` 必須是 `system:serviceaccount:<ns>:<sa>`,逐字比對)
4. 「為什麼隔壁舊服務都好好的?」(期望: 它們可能還在吃 node role,權限過大而不自知,順勢帶安全債討論)

**正解**:
- 根因: A=webhook 沒注入(annotation 缺);B=STS 信任鏈斷在 sub 比對。
- 修法: A 補 annotation 後重建 Pod(注入發生在 admission 時);B 修 trust policy。
- 驗證: Pod 內 `aws sts get-caller-identity` 回到預期的 role ARN。

**學到的底層原理**:
1. IRSA 是六棒接力(OIDC→annotation→webhook 注入→JWT→STS→臨時憑證),排障就是找斷在哪一棒,和 apply→Running 的排障思路同構。
2. annotation 生效時機在 admission(mutating webhook):改了 SA 要重建 Pod 才吃到,這是「宣告式但非即時」的典型。
3. credential chain 的 fallback 會遮蔽故障:拿不到 web identity 卻默默用 node role,功能正常、權限錯誤,是最危險的靜默失敗。

---

## P3 Drills(大型故障演練)

> P3 特色:多機制交織的複合事故,每個 drill 結束後學員要產出一頁 runbook(現象/止血/根因/預防)commit 進 `portfolio/`,這是第一批夠格進 public repo 的主秀 artifact。

### P3-1: 節點突然消失(5 分鐘的空窗期)

**適用 phase**: P3

**前置條件**: 學員已學 taints/tolerations 與 node lifecycle。backend Deployment 3 副本分佈在兩台 worker。

**破壞腳本**:
```bash
docker stop k8s-coach-p0-worker
```

**預期症狀**:
```bash
kubectl get nodes -w        # worker 約 40s 後變 NotReady
kubectl get pods -o wide -w # Pod 先變 Terminating/Unknown,但約 5 分鐘後才在別台重建
```

**限時**: 6 回合,重點是解釋「為什麼不是立刻重建」。

**引導問題**:
1. 「node NotReady 是誰判定的?依據什麼?」(期望: node controller,kubelet heartbeat/lease 停止)
2. 「Pod 為什麼不立刻搬走?」(期望: 預設 toleration `node.kubernetes.io/not-ready:NoExecute for 300s`,防網路抖動誤殺)
3. 「這 5 分鐘裡,流量發生什麼事?」(期望: Endpoints 摘除死 Pod 的時機、剩餘副本扛量,連到容量規劃)
4. 「哪些工作負載可以把 300s 調短?哪些不該?」(期望: 無狀態可以;StatefulSet 危險,腦裂風險)

**正解**:
- 根因: 非故障,是設計:tolerationSeconds 的取捨(誤殺 vs 恢復速度)。
- 修法: 對延遲敏感的 Deployment 設定較短的 not-ready toleration;或依賴多副本 + anti-affinity 讓單 node 消失不影響服務。
- 驗證: `docker start k8s-coach-p0-worker` 後 node 回 Ready,觀察 Pod 分佈重新收斂。

**學到的底層原理**:
1. 分散式系統無法區分「死了」和「慢了」:5 分鐘是 k8s 對這個不可判定問題給的預設答案,一切 failover 時間都是猜測與代價的平衡。
2. 故障恢復時間 = 偵測時間 + 決策延遲 + 重建時間,每段都可調,但都有反面代價。
3. runbook 重點:節點級故障先看「剩餘容量夠不夠」,再看「Pod 什麼時候會自己回來」,不要急著手動刪 Pod。

---

### P3-2: 流量暴增,HPA 追不上(延遲鏈解剖)

**適用 phase**: P3

**前置條件**: metrics-server 已裝(kind 需 `--kubelet-insecure-tls`),backend 設好 requests 與 HPA(target CPU 50%)。

**破壞腳本**:
```bash
# 用壓測 Pod 突發打滿 backend
kubectl run loadgen --image=busybox --restart=Never -- /bin/sh -c 'while true; do wget -q -O- http://backend-svc >/dev/null 2>&1; done'
# 可開多個 loadgen-2 loadgen-3 疊加
```

**預期症狀**:
```bash
kubectl get hpa -w    # TARGETS 飆高,REPLICAS 過一陣子才動
kubectl top pods      # CPU 撞頂,期間出現延遲/錯誤
```

**限時**: 6 回合,重點是把「慢」拆成具體的延遲鏈。

**引導問題**:
1. 「從 CPU 飆高到新 Pod 能接流量,中間有幾段延遲?」(期望: metrics 抓取間隔 → HPA sync 週期(15s)→ scale 決策(含 stabilization)→ 排程 → 拉 image → 啟動+readiness)
2. 「哪幾段你能調?代價是什麼?」(期望: 週期調短=控制面負擔、stabilization 調短=抖動、image 可預拉、readiness 可調)
3. 「如果尖峰是可預期的(行銷活動),還要靠 HPA 嗎?」(期望: 預先 scale/排程擴容,HPA 是反應式的,對已知事件用主動式)
4. 「node 資源不夠時這條鏈多出哪一段?」(期望: cluster autoscaler/Karpenter 開新機的分鐘級延遲)

**正解**:
- 根因: HPA 是反應式閉環,每段延遲疊加後對突刺天然慢半拍。
- 修法: 組合拳:合理 requests + 提前擴容 + maxSurge 快滾 + 必要時 overprovision placeholder。
- 驗證: 重跑壓測,觀察 scale-up 時間縮短、錯誤率不再出現。

**學到的底層原理**:
1. HPA 是控制理論的 feedback loop:量測有延遲、決策有阻尼(stabilization),突刺超過迴路頻寬就必然超調或跟丟。
2. 反應式(HPA)vs 主動式(預排容量)是兩種哲學,生產尖峰用後者兜底、前者收尾。
3. runbook 重點:壓力事件的時間線要標出每段延遲的實測值,下次才知道該優化哪段。

---

### P3-3: OOM 雪崩連鎖(一死全死的正回饋)

**適用 phase**: P3

**前置條件**: 學員 P1 已打穿單體 OOM;backend 3 副本、memory limit 偏緊、有持續流量(P3-2 的 loadgen 可複用)。

**破壞腳本**:
```bash
# 殺掉一個副本,讓流量壓到剩下兩個(記憶體隨連線數上升的 app 最佳;用 stress 模擬亦可)
kubectl delete pod <backend-pod-1>
```

**預期症狀**:
```bash
kubectl get pods -w
# 剩餘副本記憶體上升 -> OOMKilled -> 重啟 -> 流量又壓過來 -> 再 OOMKilled
# RESTARTS 連環上升,服務雪崩
```

**限時**: 6 回合。

**引導問題**:
1. 「第一隻 Pod 死掉後,系統對剩下的 Pod 做了什麼?」(期望: Endpoints 摘一個,流量全壓剩餘副本,per-Pod 負載上升)
2. 「這是正回饋還是負回饋?為什麼停不下來?」(期望: 正回饋:死越多、剩的壓力越大、死更快)
3. 「止血動作是什麼?」(期望: 先擴副本(稀釋負載)或先擋流量(rate limit/摘掉入口),不是調 limit:改 limit 要重建 Pod,雪崩中最危險)
4. 「事後預防的三道防線?」(期望: 容量 headroom(N-1 也扛得住)、HPA 及早擴、PDB 防維運誤觸發同款雪崩)

**正解**:
- 根因: 容量無 headroom,單副本死亡讓剩餘副本超載,OOM 正回饋。
- 修法: 止血=快速 scale up + 必要時流量降級;根治=requests/limits rightsize + N-1 容量原則。
- 驗證: 再殺一個 Pod,剩餘副本記憶體仍在安全水位,無連鎖。

**學到的底層原理**:
1. 雪崩=正回饋迴路:排障第一步是「打斷迴路」(加容量或減輸入),不是修單點。
2. 容量規劃的 N-1/N-2 原則:任何副本數的意義要用「死掉幾個之後還活著」來定義。
3. runbook 重點:雪崩中「調 limit + 滾動重建」是把剩餘容量再砍一刀的自殺操作,寫進 do-not 清單。

---

### P3-4: 滾動更新出包 + PDB 卡 drain(複合事故)

**適用 phase**: P3

**前置條件**: 學員已學 PDB;backend 4 副本、PDB minAvailable: 3、rolling update 進行中。

**破壞腳本**:
```bash
# 先滾一個壞 image(拉不起來),讓 rollout 卡在中間
kubectl set image deployment/backend app=nginx:9.99
# 同時模擬計畫中的節點維護
kubectl drain k8s-coach-p0-worker2 --ignore-daemonsets --delete-emptydir-data
```

**預期症狀**:
```bash
# rollout 卡住:新 RS 起不來,舊 RS 只剩 3 個健康
kubectl rollout status deployment/backend   # 不會結束
# drain 卡住:evict 一個舊 Pod 就會跌破 minAvailable 3
# error when evicting pod ... Cannot evict pod as it would violate the pod's disruption budget.
```

**限時**: 8 回合(複合事故,考拆解順序)。

**引導問題**:
1. 「兩件事卡住了。先修哪個?為什麼?」(期望: 先修 rollout:它是讓健康副本數見底的元兇;drain 只是被 PDB 正確擋下)
2. 「PDB 是壞人嗎?」(期望: 不是,它正在做它的工作:防止維運操作把服務打穿)
3. 「rollout 的止血指令?」(期望: `kubectl rollout undo deployment/backend`,舊 RS 還在、不重拉 image,秒回)
4. 「事後檢討:什麼流程規則能避免這種複合?」(期望: 變更凍結原則:rollout 進行中不做節點維護;或 drain 前先確認 rollout 全綠)

**正解**:
- 根因: 壞 image 讓可用副本貼著 PDB 下限,drain 的 eviction 被 PDB 拒絕,兩個操作互鎖。
- 修法: rollback 先恢復健康副本 → drain 自然放行 → 修好 image 再重新上。
- 驗證: rollout status 完成、drain 完成、`kubectl get pdb` 的 ALLOWED DISRUPTIONS 回正。

**學到的底層原理**:
1. PDB 是 eviction 的 admission 閘門:它擋的是「自願中斷」(drain/rollout),擋不住 OOM/節點死亡這種非自願中斷。
2. 複合事故的拆解原則:先恢復「可用容量」,再處理「計畫性操作」;順序反了就是把自己鎖死。
3. runbook 重點:每個維運動作前先看 `kubectl get pdb` 的 allowed disruptions,0 就代表現在動手必卡。

---

## P4 Drills

### P4-1: Alert 風暴(一個根因,五十條告警)

**適用 phase**: P4

**前置條件**: kube-prometheus-stack 已裝,預設 rules 全開。

**破壞腳本**:
```bash
# 重演 P3-1:停掉一台 worker,讓 node 級故障觸發整串告警
docker stop k8s-coach-p0-worker
```

**預期症狀**:
```
Alertmanager 短時間湧入:KubeNodeNotReady、KubePodNotReady x N、KubeDeploymentReplicasMismatch、TargetDown x N ...
```

**限時**: 5 回合,考的是「從告警堆裡找根因」而不是逐條處理。

**引導問題**:
1. 「50 條告警,先讀哪一條?」(期望: 找最上游/最接近 cause 的:NodeNotReady;其餘多是它的 symptom)
2. 「怎麼從告警的形狀判斷上下游?」(期望: 爆炸半徑:node 級 > workload 級 > Pod 級;時間戳:最早的通常最接近根因)
3. 「Alertmanager 有什麼機制讓這種風暴不吵死人?」(期望: grouping、inhibition(node 告警抑制其下 Pod 告警)、silence)
4. 「這次事件後,你會改哪條 rule?」(期望: 為 node 故障加 inhibition 規則;page 只留 symptom-based 的用戶面告警,cause 類降級為 ticket)

**正解**:
- 根因: 單一 node 故障;其餘告警是同一根因的多層投影。
- 修法: 恢復 node;告警工程面補 inhibition/grouping,分層 page vs ticket。
- 驗證: 重演一次 node 故障,收到的 page 數量從幾十條降到個位數。

**學到的底層原理**:
1. 告警的資訊價值 = 去重後的獨立根因數,不是條數;風暴時先做因果分層再動手。
2. inhibition 就是把「因果拓撲」教給 Alertmanager:上游紅了,下游閉嘴。
3. page 的黃金標準是 symptom-based(用戶受影響了嗎),cause-based 告警適合 dashboard/ticket,不適合半夜叫醒人。

---

### P4-2: Cardinality 爆炸(自己造出來的監控事故)

**適用 phase**: P4

**前置條件**: Prometheus 已裝,學員已學 TSDB 與 label 成本模型。

**破壞腳本**:
```bash
# 部署一個把 request_id 放進 label 的示範 exporter(教材附 demo app),或用 avalanche 之類的 flood 工具
# 效果:每次請求產生一條新 time series
```

**預期症狀**:
```bash
# Prometheus 記憶體持續上漲,查詢變慢
# 檢查 series 數量:
curl -s http://localhost:9090/api/v1/status/tsdb | jq '.data.headStats.numSeries'
# topk(10, count by (__name__)({__name__=~".+"}))  找出兇手 metric
```

**限時**: 5 回合。

**引導問題**:
1. 「Prometheus 記憶體漲,第一個假設是什麼?怎麼驗證?」(期望: series 暴增;查 tsdb status / topk count by __name__)
2. 「找到兇手 metric 後,怎麼看是哪個 label 出問題?」(期望: `count by (<label>)` 看基數分佈,找出無界 label)
3. 「為什麼 request_id/user_id 進 label 是災難,進 log 就沒事?」(期望: TSDB 每個 label 組合=一條獨立 series 常駐記憶體;log 是一次性寫入)
4. 「止血和根治?」(期望: 止血=relabel drop 該 label 或整個 target;根治=改 app 的 metric 設計,無界值進 log/trace)

**正解**:
- 根因: 無界 label 讓 series 數量隨流量線性成長,TSDB head 記憶體被吃穿。
- 修法: scrape config 加 metric_relabel_configs drop;app 端把高基數欄位移到 logs/traces。
- 驗證: numSeries 回落,記憶體曲線走平。

**學到的底層原理**:
1. metrics 便宜的前提是「基數有界」:label 的正確心智模型是維度(枚舉值),不是識別碼。
2. 三本柱的分工由基數決定:有界聚合進 metrics、無界明細進 logs、因果鏈進 traces。
3. 監控系統自己也是生產系統:它的容量事故一樣要有 runbook,而且它掛掉時你是瞎的。

---

## P5 Drills

### P5-1: ArgoCD OutOfSync(有人手改了 prod)

**適用 phase**: P5

**前置條件**: ArgoCD 已裝並管理 backend app(auto-sync 先關閉)。

**破壞腳本**:
```bash
# 模擬半夜救火的同事:直接改 live 狀態
kubectl scale deployment backend --replicas=1
```

**預期症狀**:
```
ArgoCD UI/CLI:app 變 OutOfSync,diff 顯示 replicas: live=1 vs git=3
```

**限時**: 4 回合。

**引導問題**:
1. 「OutOfSync 是誰發現的?它怎麼發現的?」(期望: ArgoCD 持續比對 Git(desired)與 cluster(live),就是 reconcile loop 的 diff 階段)
2. 「這個 diff 該 sync 掉(蓋回 Git 版)還是該保留?你怎麼判斷?」(期望: 先問「live 的改動是誰、為什麼」:救火降載可能是有意的,直接 sync 會把火重新點燃)
3. 「如果 auto-sync + selfHeal 開著,剛剛的手改會怎樣?」(期望: 幾分鐘內被自動蓋回,救火動作蒸發,這是 GitOps 紀律的雙面刃)
4. 「正確的救火流程是什麼?」(期望: 緊急手改可以,但立刻回填 Git(或用 ArgoCD 的參數 override),讓 Git 重新成為事實)

**正解**:
- 根因: live 與 Git 漂移(drift),ArgoCD 如實回報。
- 修法: 依情境:改動不該存在 → sync;改動是有意的 → 補 commit 進 Git 再 sync。
- 驗證: app 回到 Synced,Git log 留有那次救火的紀錄。

**學到的底層原理**:
1. GitOps = 把 reconcile loop 的 desired state 從 etcd 外移到 Git:ArgoCD 之於 Git,就像 controller 之於 etcd(P0 心智模型的複利)。
2. drift detection 的價值不在「擋人手改」,在「手改無所遁形」:audit 由系統保證,不靠自覺。
3. selfHeal 的取捨:一致性極強,但救火自由度為零;生產常見折衷是 auto-sync on、selfHeal off + 告警。

---

### P5-2: Validating Webhook 掛掉,全 cluster 建不了 Pod

**適用 phase**: P5

**前置條件**: 學員已學 admission webhook。部署一個 demo validating webhook(failurePolicy: Fail)後把它的 backend 弄死。

**破壞腳本**:
```bash
kubectl -n webhook-demo scale deployment webhook-server --replicas=0
# 然後嘗試任何 Pod 建立(直接建或由 Deployment 觸發)
kubectl run probe-victim --image=nginx
```

**預期症狀**:
```
Error from server (InternalError): Internal error occurred: failed calling webhook "validate.demo.io":
... connect: connection refused
# 不只你的 Pod:全 cluster 所有符合 webhook 規則的建立/更新全部被拒
```

**限時**: 5 回合(生產等級的緊急事故,考止血速度)。

**引導問題**:
1. 「錯誤訊息點名了 webhook。它在請求鏈的哪個位置?」(期望: API Server 的 admission 關卡,P0 三道關卡的第三道)
2. 「為什麼 webhook 死了會擋下全部,而不是放行?」(期望: failurePolicy: Fail:連不上=拒絕,fail-closed)
3. 「緊急止血指令?」(期望: 刪掉或暫時改掉該 ValidatingWebhookConfiguration:`kubectl get validatingwebhookconfigurations` → delete/patch failurePolicy=Ignore)
4. 「事後檢討:webhook 該怎麼部署才配得上 Fail?」(期望: 多副本 + PDB + 不依賴它自己守門的 namespace(排除 kube-system 與 webhook 自己),否則雞生蛋:webhook 死了連自己都救不回來)

**正解**:
- 根因: fail-closed 的 webhook 後端全滅,admission 鏈斷,API Server 拒絕所有受管請求。
- 修法: 止血=patch failurePolicy 或刪 configuration;恢復 webhook 後端;根治=HA 部署 + namespaceSelector 排除自救路徑。
- 驗證: `kubectl run probe-victim --image=nginx` 成功;webhook 恢復後再確認它真的在攔該攔的東西。

**學到的底層原理**:
1. fail-open vs fail-closed 是安全與可用的根本取捨:安全元件選 Fail 就必須用可用性工程(HA/PDB/排除自身)來還這筆債。
2. admission 是 API Server 的同步路徑:webhook 的延遲和可用性直接疊加在所有寫入操作上,它是全叢集的隱形單點。
3. runbook 重點:這類事故的第一分鐘不是修 webhook,是解除 fail-closed;先讓叢集能動,再修守門員。

---

### P5-3: Helm upgrade 壞版本與回滾(rollback 不是時光機)

**適用 phase**: P5

**前置條件**: backend 改用 helm chart 部署,已有 2-3 個 release 版本。

**破壞腳本**:
```bash
# 發一個壞 values 的版本(image tag 不存在 + 順手加了一個新 ConfigMap)
helm upgrade backend ./chart --set image.tag=9.99 --set extraConfig.enabled=true
```

**預期症狀**:
```bash
helm status backend        # deployed(helm 不等 Pod 健康,除非 --wait)
kubectl get pods           # 新 Pod ImagePullBackOff,舊 Pod 已被替換掉一部分
```

**限時**: 5 回合。

**引導問題**:
1. 「helm 說 deployed,Pod 卻在 BackOff。helm 的『成功』是什麼意思?」(期望: manifest 送進 API Server 成功;runtime 健康不歸它管,除非 --wait/--atomic)
2. 「回滾指令?回滾的單位是什麼?」(期望: `helm rollback backend <rev>`;單位是 release 的 manifest 快照,不是叢集狀態)
3. 「rollback 之後,那個新加的 ConfigMap 還在嗎?」(期望: helm 用三方 diff 處理,rollback 到沒有它的 revision 會刪掉它;但 hooks 建的東西、CRD、以及 helm 外的手改不在快照裡)
4. 「怎麼讓『壞版本上線』根本不發生?」(期望: --atomic(失敗自動回滾)+ CI 裡 helm diff/kubeval;更根本的是接 progressive delivery)

**正解**:
- 根因: helm 的成功語義是「提交成功」不是「運行健康」;不帶 --wait 的 upgrade 對壞 image 毫無防禦。
- 修法: `helm rollback backend <上一版>`;流程面補 --atomic 與 CI 驗證。
- 驗證: `helm history backend` 顯示 rollback 紀錄,Pod 全綠,多餘 ConfigMap 依 revision 內容正確清理。

**學到的底層原理**:
1. helm 是「產 YAML + 版本化快照」的工具,不是 controller:它沒有 reconcile loop,發完就走,和 ArgoCD 的本質差異在此。
2. rollback 的能力邊界由快照範圍決定:CRD、hook 產物、chart 外資源都在邊界外,回滾前要知道哪些東西回不去。
3. 發佈安全是縱深:--atomic(工具層)→ readiness+maxUnavailable(平台層)→ canary+SLO 閘門(交付層),P5 的 progressive delivery 就是最外層。
