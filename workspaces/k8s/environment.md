# Environment(機器與 context 事實)

<!-- coach 每次動手 lab 前讀這份;progress.md 不放機器細節。事實變了就地更新並註記日期。 -->

## ⚠️ kubectl context 安全鐵律

動手前必查 `kubectl config current-context`:

| Context | 意義 | 可以 lab? |
|---------|------|-----------|
| `kind-k8s-coach-p0`(家用 VM) | 本地 kind(lab-cluster.sh up 自動設) | ✅ |
| `kind`(公司 bastion,舊) | 本地 kind(bastion 上的叢集,已實體佐證:node 名 `k8s-coach-p0-worker`、Pod IP `10.244.x.x` kindnet 網段) | ✅ |
| `kind-k8s-coach-p2a`(公司 bastion,s20) | 本地 kind Calico 叢集(bastion 上也有 p2a;node `k8s-coach-p2a-worker`、Pod IP `192.168.46.x`、tunl0 IPIP) | ✅ |
| `eks` | **公司 PROD `billing-devops-prod-platform`**(kubeconfig `/home/ec2-user/.kube/eks/config.yaml`) | ❌ 絕對不碰 |

判準:context 是 `kind` 或 `kind-k8s-coach-*` 都安全;只有 `eks` 是公司 PROD。**別因 context 名叫 `kind` 就誤觸警報卡住學員**(2026-07-07 已確認)。

## 機器

- **家用 VM**(Oracle):kind 在 `~/.local/bin`;s12/s14 在這台。kind p0 叢集 3 節點(control-plane + worker×2)。
- **公司 bastion `billing-eks-bastion`**:s13 在這台;本地 kind context 叫 `kind`。

## 叢集與工具現況(2026-07-09)

- kind p0 三節點 Ready、CoreDNS 2 副本 Running、ingress-nginx controller Running(worker 已貼 `ingress-ready=true`)、Ingress `shop-ingress` 已 apply。
- **port-forward 用 8081**;舊 8080 那條壞掉(被 Ctrl-C 打斷回假 404),別用。叢集內測法可用 netshoot pod curl `ingress-nginx-controller.ingress-nginx.svc.cluster.local`(不依賴 port-forward)。
- **⚠️ metrics-server 缺**(隨舊叢集消失),P3 HPA 前要重裝(kind 需 `--kubelet-insecure-tls`)。
- chunk 3 NetworkPolicy 需要 **Calico** 叢集(kindnet 不支援 NetworkPolicy),要新建 `clusters/kind-p2a.yaml`(disableDefaultCNI)+ 裝 Calico。
- lab 檔位置:`portfolio/k8s/manifests/`(ingress-demo/、ingress-lab/ 兩份都在 repo)。
- (2026-07-14)bastion 的 kind 叢集(context `kind`)也有完整 shop 場景:shop-api/shop-web 各 2/2、shop-ingress(host shop.com)、ingress-nginx controller Running。chunk 2 補做兩台機器都能跑。

## 跨機器同步(git)

學習狀態(本目錄)與教材同在 `learning-coaches` repo(remote:github.com/jasontsaicc/learning-coaches):

- 開課前:`git pull`
- 每堂課後:commit(一行 subject、無 trailer)+ `git push`

### Bastion 一次性遷移步驟(舊 k8s-mastery-lab-skill repo 退役後)

```
git clone git@github.com:jasontsaicc/learning-coaches.git ~/go_senior_devops/learning-coaches
ln -sfn ~/go_senior_devops/learning-coaches/skills/k8s-coach ~/.claude/skills/k8s-coach
rm -rf <舊的 k8s-mastery-lab-skill clone>
kubectl config current-context   # 確認仍是 kind(bastion 本地叢集不受影響)
```

## bastion kubeconfig 坑(2026-08-04 排掉)

`kubectl get nodes` 噴 `invalid character '<' looking for beginning of value` 時,**不是叢集壞了**:

```
context kind → cluster kind-k8s-coach-p0(s21 已刪,條目不存在)
  → kubectl 退回內建預設 http://localhost:8080
  → 打到 gitlab-ci-dashboard(bastion 上長期 Up)
  → 收到 HTML → JSON parser 爆在 '<'
```

修法:`kubectl config use-context kind-k8s-coach-p2a`。孤兒 context 清除指令 `kubectl config delete-context kind`(2026-08-04 已給學員,**未確認是否執行**)。
排障順序記住:**先確認你在跟誰講話(context / server URL),再懷疑叢集。**

診斷指令注意:`docker ps --filter name=kind` **抓不到 p2a**(容器叫 `k8s-coach-p2a-*`,名字裡沒有 kind)。要用 `kind get clusters` 或不帶 filter 的 `docker ps -a`。

## bastion 叢集現況(2026-08-10,s27,**第五次故障;下課時仍未修好**)

- `kubectl get nodes`:**control-plane / worker `NotReady`,worker2 `Ready`**(24d,v1.32.2)。
- **根因已完整採證(s27,五次以來第一次證據齊全)**:

```
Ready  False  KubeletNotReady  container runtime is down     ← kubelet 活著、自己回報
MemoryPressure / DiskPressure / PIDPressure  全 False        ← kubelet 已排除三個嫌犯
NetworkUnavailable  False  CalicoIsUp                        ← CNI 沒事

宿主機:available 11Gi / 15Gi,load 0.54(4 核心),三個 node 容器全 Up 8 hours  ← 宿主機無罪
worker2 Ready 而另兩台 NotReady(同一台宿主機)                                 ← 對照組再確認一次

docker exec <node> systemctl is-active containerd kubelet   → 兩個都 active   ← 進程沒死
docker exec <node> journalctl -u kubelet | grep DeadlineExceeded
  → "StopPodSandbox from runtime service failed: rpc error: code = DeadlineExceeded"
  → "Skipping pod synchronization err=container runtime is down"  每 5 秒一次、連噴 8 小時
containerd 最後一行 log 停在 09:10(查看時 17:10)= 八小時全靜音
```

- **真兇 = containerd 的 CRI gRPC 卡住不回話(不是死掉)**,與 s21 同款。`Terminating` 卡住的 Pod(`cg-demo` / `vol-demo` / 三個舊殘骸)是同一個病的症狀,不是另一個問題。
- **`docker restart k8s-coach-p2a-worker k8s-coach-p2a-control-plane` 下完後仍 NotReady**(下課時)。
- ⚠️ **s28 建議直接重建,不要再修**:叢集已 24 天、containerd 第五次卡死(s21/s24/s25/s26/s27)。`kind delete cluster --name k8s-coach-p2a` → 用 `clusters/kind-p2a.yaml` 重建 → 重裝 Calico。每堂開場修 20 分鐘的成本已超過重建。
- 診斷順序(可直接重用):**node conditions → 宿主機資源 → 對照組〔壞幾台好幾台〕→ `systemctl is-active` → kubelet log 抓 `DeadlineExceeded`**。

## bastion 叢集現況(2026-08-06,s26 開場,**三台全 Ready**,已被上面取代)

- `kubectl get nodes` 三台 `Ready`(control-plane / worker / worker2,19d,v1.32.2)。
- **恢復原因 = 宿主機今早重開機**(`up 1:49`,所有容器 `Up 2 hours`),不是誰修好的。
- 當下資源健康:load average `0.56 / 1.07 / 1.15`(4 核心)、`available 12Gi` / 15Gi、swap 未用。
- ⚠️ **s25 那次 node 全倒的真兇未採證即被重開機洗掉,永遠查不到**。教學結論已給學員:restart/reboot 同時清掉症狀與證據,採證(node Conditions / kubelet log)必須排在 restart 前面。
- `gitlab-ci-dashboard` 仍在跑(Up 2 hours),就是 s24 那個吃掉 `localhost:8080` 的東西。孤兒 context `kind` 已清除(`kubectl config get-contexts` 只剩 `kind-k8s-coach-p2a`)。
- s26 新增物件:`vol-demo` Pod(釘 `nodeName: k8s-coach-p2a-worker`,同掛 emptyDir `/scratch` + `pvc-demo` `/data`,image busybox `sleep 86400`)。`pv-demo` / `pvc-demo` 仍 Bound;`cg-demo` 未再檢查(node 已 Ready,Pending 應已解除,s27 確認)。

### ⚠️ 兩份 repo clone(2026-08-06 發現)

bastion 上同時存在:

| 路徑 | 內容 |
|------|------|
| `~/jason/learning-coaches/` | s26 的 `labs/vol-demo.yaml` 寫在這裡;教練本次 session 的工作目錄 |
| `~/go_senior_devops/learning-coaches/` | s25 的 `labs/pv-demo.yaml` / `pvc-demo.yaml` / `cg-demo.yaml` 在這裡(environment.md 遷移步驟指定的路徑) |

`labs/` 是 gitignored 所以不影響跨機同步,但**兩邊都是 git clone,commit/push 前先確認在哪一份**。已告知學員。

### kind 特有陷阱:`/tmp` 是 tmpfs(2026-08-06)

kind 的 node image 把 `/tmp` 掛成 tmpfs。任何 hostPath 指到 `/tmp/...` 的 PV,**實體是記憶體,node 重開就沒**。s26 實證:`kubectl exec vol-demo -- cat /proc/mounts` 顯示 `/data`(hostPath `/tmp/pv-demo`)是 `tmpfs`,而 `/scratch`(emptyDir,在 `/var/lib/kubelet/...`)才是 `/dev/nvme0n1p1` xfs。

排障通則:**持久性看 `/proc/mounts` 實際掛什麼,不看物件叫什麼名字。**

### 從外面殺 container(PID 1 保護的繞法)

`kubectl exec <pod> -- kill 1` 殺不死 container(kernel 對 PID 1 的 signal 保護,同 namespace 內連 SIGKILL 都擋)。要模擬 container crash 必須從祖先 namespace 動手:

```
docker exec k8s-coach-p2a-worker sh -c 'crictl stop $(crictl ps -q --label io.kubernetes.pod.name=<pod-name>)'
```

## ⚠️ bastion 叢集舊現況(2026-08-05,已被上面取代)

- **worker 也倒了**。`kubectl describe pod` Events:`0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane}, 2 node(s) had untolerated taint {node.kubernetes.io/not-ready}` → **可排的 node = 0**,新 Pod 一律 Pending。
- 修復三發(s25 已給學員,**未執行未回報**):

```
kubectl get nodes
free -h; uptime; docker ps --format '{{.Names}}\t{{.Status}}'
docker restart k8s-coach-p2a-worker k8s-coach-p2a-worker2
```

- restart 無效就走 s21 診斷鏈:node Conditions → 宿主機資源 → `systemctl status containerd`(進程活著不代表沒塞住)→ kubelet log 找 `Status from runtime service failed: rpc DeadlineExceeded`。根因大機率仍是 4 核心資源競爭把 CRI gRPC 拖過 timeout。
- **PV/PVC 綁定不受影響**(s25 實證):node 全 NotReady,`pvc-demo` 照樣 `Bound` —— 媒合是 control plane 的帳本作業。只有「Pod 真的掛上去」才需要活的 node。
- s25 新增物件:`pv-demo`(1Gi / RWO / manual / hostPath `/tmp/pv-demo` / Retain)、`pvc-demo`(500Mi,Bound 到 pv-demo)、`cg-demo`(limit 64Mi,**Pending**)。lab 檔在 `workspaces/k8s/labs/`(gitignored)。

## bastion 叢集現況(2026-08-04,已被上面取代)

- `kind-k8s-coach-p2a` 三節點,Calico。control-plane 172.21.0.4 / worker 172.21.0.2 / **worker2 172.21.0.3 NotReady 已 17 天**(老毛病,lab 不受影響,未處理)。
- worker2 上三個 Terminating 殘骸(backend/db/frontend,11 天)未清。
- 活的 Pod 全在 worker:backend .91 / net-tool .92 / db .93 / frontend .94。net-tool = netshoot,`sleep` 到期自然重啟,約 2h 一次。
- bastion 上**沒有** p0 叢集(s21 已刪),context `kind` 是孤兒。

## 其他慣例

- EKS lab(P2b 起):terraform 指令由學員親手跑,命名 `billing-dev-eks-*`,每個 lab 必附 destroy + 驗證。
- commit 規則:user 全域禁止任何 trailer/Co-Authored-By,commit message 一行。
