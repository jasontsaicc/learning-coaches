# Environment(機器與 context 事實)

<!-- coach 每次動手 lab 前讀這份;progress.md 不放機器細節。事實變了就地更新並註記日期。 -->

## ⚠️ kubectl context 安全鐵律

動手前必查 `kubectl config current-context`:

| Context | 意義 | 可以 lab? |
|---------|------|-----------|
| `kind-k8s-coach-p0`(家用 VM) | 本地 kind(lab-cluster.sh up 自動設) | ✅ |
| `kind`(公司 bastion) | 本地 kind(bastion 上的叢集,已實體佐證:node 名 `k8s-coach-p0-worker`、Pod IP `10.244.x.x` kindnet 網段) | ✅ |
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

## 其他慣例

- EKS lab(P2b 起):terraform 指令由學員親手跑,命名 `billing-dev-eks-*`,每個 lab 必附 destroy + 驗證。
- commit 規則:user 全域禁止任何 trailer/Co-Authored-By,commit message 一行。
