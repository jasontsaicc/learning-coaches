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

## ⚠️ bastion 叢集現況(2026-08-05,**叢集目前無法排任何 Pod**)

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
