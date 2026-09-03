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

## 家用 VM 叢集現況(2026-09-02,s34 開場實測,**兩台 Ready**)

主機 `jasonarmvm2`,context `kind-k8s-coach-p2a`,`kind get clusters` 只有這一座。

| 項目 | 實測值 |
|---|---|
| node | `k8s-coach-p2a-control-plane` + `k8s-coach-p2a-worker`,**兩台 Ready** |
| 版本 / 年齡 | **v1.30.0**,45d |
| CNI | Calico(`calico-node` ×2 + `calico-kube-controllers`) |
| podCIDR | control-plane `192.168.0.0/24`、worker `192.168.1.0/24` |
| s32 殘留物件 | **全部不存在**(`web` / `sc-demo` / `dnstest` / `pvc-dyn` 都查無) |

⚠️ **與 2026-08-28 的 s32 紀錄對不上**:那筆記的是「三台、v1.32.2、16d」外加一批殘留物件,
這台今天量到的是兩台 v1.32 以下的 45d 叢集且殘留物全無。可能是 s32 那筆其實記的是 bastion,
或這座叢集後來被重建過。**未追查,以本節實測值為準。**

- 影響:**C-2 的 `reclaimPolicy: Delete` teardown 實證失去現場**(`sc-demo` PVC 沒了),要重做得重建物件。
- 這台只有兩台 node,跨 node 封包題仍做得起來(worker ↔ control-plane),但少一個對照組。
- 修 containerd 卡死沿用 08-10 精準版,節點名照這台只有兩個:

```
for n in control-plane worker; do docker exec k8s-coach-p2a-$n systemctl restart containerd; done
```

- ⚠️ **單節點 kind 的評估仍未做**(s29 起掛著)。

## bastion 叢集現況(2026-08-20,s28 開場,**containerd 第六次卡死 → 已修復三台 Ready**)

- 開場:三台全 `NotReady`(9d),一行對照跑出來**三台都 `SLOW`**(不是只有 worker2)。
- 修法照 08-10 精準版,三台各一發,25 秒全回 `Ready`,Pod 未重排:

```
for n in control-plane worker worker2; do docker exec k8s-coach-p2a-$n systemctl restart containerd; done
```

- **當下宿主機 load 5.97 / 4 核心**,`ps -eo pcpu,pmem,etime,comm --sort=-pcpu | head` 抓到 **terraform 69% + terragrunt 20%**(別的工作在跑)。→ **根因不變:這台 4 核心 bastion 只要有人跑重活,containerd 的 CRI 就會被拖過 kubelet 的健康檢查 timeout,而且負載退了它不會自己恢復。**
- 結論:`gitlab-ci-dashboard` 退場沒有根治,因為競爭者換人就會再犯。**s29 評估:改用單節點 kind 叢集(少兩個 node 的 containerd/kubelet)或上課前避開跑 terraform。**

## bastion 叢集現況(2026-08-10 晚,**p2a 已重建 + 三台 Ready**)

- 舊叢集已 `kind delete`,用 `clusters/kind-p2a.yaml` 重建(control-plane + worker ×2,disableDefaultCNI,podSubnet `192.168.0.0/16`),Calico `v3.28.2` 已裝。三台 `Ready`,kube-system 全 `Running`。
- ⚠️ **重建後 11 分鐘 worker2 立刻復發同一個病** —— 所以**根因不是叢集老舊**,是這台 bastion(4 核心)在 Calico 啟動尖峰(load 一度 5.05)把 worker2 的 containerd 拖過 kubelet 的健康檢查 timeout,而且**負載退下去之後 containerd 不會自己恢復**。

### 三個可重用的東西(2026-08-10 新 + s27 診斷順序,價值最高)

**1. 一行分辨「containerd 是慢還是死」** —— 好壞 node 對照跑,秒判:

```
for n in worker worker2; do printf "%s: " $n; docker exec k8s-coach-p2a-$n sh -c 'timeout 2 crictl info >/dev/null 2>&1 && echo FAST || echo SLOW'; done
```

實測:`worker: FAST` / `worker2: SLOW` —— 同一台宿主機、同一個 image、同樣 11 分鐘壽命。`systemctl is-active` 兩台都是 `active`,分不出來;**這一行分得出來**。2 秒是照 kubelet 健康檢查的量級取的。

**2. 精準修法:重啟 containerd 就好,不用重啟整個 node 容器**

```
docker exec k8s-coach-p2a-worker2 systemctl restart containerd
```

25 秒後 CRI 回 `FAST`、node 回 `Ready`,**Pod 不用重排、其他 node 不受影響**。比 `docker restart <node>` 影響面小得多。

**對應的 kubelet log 訊號**(worker2 復發時):

```
kubelet.go:2993 "Container runtime sanity check failed" err="rpc error: code = DeadlineExceeded"
kubelet.go:2412 "Skipping pod synchronization" err="container runtime is down"
containerd: level=warning msg="container event discarded"     ← 事件消費者跟不上,contention 的徵兆
```

**降低復發**:Calico 剛裝完那 5 分鐘是尖峰,不要同時做別的事。

**`gitlab-ci-dashboard` 已退場(2026-08-10,學員確認不再使用)**:`docker stop` + `docker update --restart=no`。它原本是 `restart=always`,這就是每次宿主機重開它都自己回來、長期跟叢集搶 4 核心的原因(也是 s24 吃掉 `localhost:8080` 的那個)。容器保留未 `docker rm`。**現在這台 bastion 上只有三個 kind node 在跑。**


**3. 診斷順序(s27 採證實績,可直接重用)**

`node conditions` → 宿主機資源 → 對照組〔壞幾台好幾台〕→ `systemctl is-active` → kubelet log 抓 `DeadlineExceeded`。
真兇多半是 **containerd 的 CRI gRPC 卡住不回話,不是死掉** —— `systemctl is-active` 兩台都回 `active`,分不出來,要靠上面第 1 條的對照跑法。

## ⚠️ 兩份 repo clone(2026-08-06 發現)

bastion 上同時存在:

| 路徑 | 內容 |
|------|------|
| `~/jason/learning-coaches/` | s26 的 `labs/vol-demo.yaml` 寫在這裡;教練本次 session 的工作目錄 |
| `~/go_senior_devops/learning-coaches/` | s25 的 `labs/pv-demo.yaml` / `pvc-demo.yaml` / `cg-demo.yaml` 在這裡(environment.md 遷移步驟指定的路徑) |

`labs/` 是 gitignored 所以不影響跨機同步,但**兩邊都是 git clone,commit/push 前先確認在哪一份**。已告知學員。

## kind 特有陷阱:`/tmp` 是 tmpfs(2026-08-06)

kind 的 node image 把 `/tmp` 掛成 tmpfs。任何 hostPath 指到 `/tmp/...` 的 PV,**實體是記憶體,node 重開就沒**。s26 實證:`kubectl exec vol-demo -- cat /proc/mounts` 顯示 `/data`(hostPath `/tmp/pv-demo`)是 `tmpfs`,而 `/scratch`(emptyDir,在 `/var/lib/kubelet/...`)才是 `/dev/nvme0n1p1` xfs。

排障通則:**持久性看 `/proc/mounts` 實際掛什麼,不看物件叫什麼名字。**

## 從外面殺 container(PID 1 保護的繞法)

`kubectl exec <pod> -- kill 1` 殺不死 container(kernel 對 PID 1 的 signal 保護,同 namespace 內連 SIGKILL 都擋)。要模擬 container crash 必須從祖先 namespace 動手:

```
docker exec k8s-coach-p2a-worker sh -c 'crictl stop $(crictl ps -q --label io.kubernetes.pod.name=<pod-name>)'
```

## 其他慣例

- EKS lab(P2b 起):terraform 指令由學員親手跑,命名 `billing-dev-eks-*`,每個 lab 必附 destroy + 驗證。
- commit 規則:user 全域禁止任何 trailer/Co-Authored-By,commit message 一行。
