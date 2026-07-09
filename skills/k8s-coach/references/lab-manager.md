# Lab Manager: lab-cluster.sh

統一管 lab 叢集生命週期,降低操作摩擦。地端用 `kind`(已驗證 VM 規格夠用);教學時引導學員用這支腳本,不用每次手敲 `kind create`。

## Environment Setup

`kind` 已裝在 `~/.local/bin`。叢集設定檔在 `workspaces/k8s/clusters/kind-<phase>.yaml`(per-phase);機器層細節(kubeconfig contexts、port 慣例、metrics-server 狀態)見 `workspaces/k8s/environment.md`。

```
scripts/lab-cluster.sh <up|down|status|reset> [phase]
```

| 指令 | 作用 |
|------|------|
| `up [phase]` | 依 `workspaces/k8s/clusters/kind-<phase>.yaml` 開叢集(無設定檔則開預設單節點) |
| `down [phase]` | 刪掉該叢集 |
| `status` | 列出所有 `k8s-coach-*` 叢集 |
| `reset [phase]` | down 再 up,乾淨重來,給 Chaos Drill 反覆摔壞用 |

Step D 開場通常先 `up [phase]`;step E drill 摔壞後可 `reset [phase]`。

## Context Safety (iron rule)

**動手前必查 `kubectl config current-context`。** 只有 `kind` / `kind-k8s-coach-*` context 是安全的 lab 目標;`eks` context = 公司 PRODUCTION,絕不當 lab 用。每台機器的實際 context 清單記在 `workspaces/k8s/environment.md`。

## EKS Labs (P2b 起,雲端整合主題)

- EKS 的 `terraform apply` / `destroy` **只產生指令,由學員親手執行**;coach 不直接動雲端資源。
- 命名 / tag 前綴一律 `billing-dev-eks-*`,用現有 dev VPC、自建專用 subnet(additive,不改既有 subnet)。
- 每個 EKS lab **必附 `terraform destroy` + 驗證指令**,防遺留燒錢資源。

## Verification

每個 lab step 用客觀輸出驗證,不接受自報:

- 叢集就緒:`kubectl get nodes` 全部 `Ready`。
- Pod 狀態:`kubectl get pod -n <ns> -o jsonpath='{.status.phase}'` 回 `Running`;故障情境用 `kubectl get events` / `kubectl describe` 確認預期的失敗訊號(e.g. `CrashLoopBackOff`、`OOMKilled`)。
- 網路類 lab:`curl` 實際打通(或預期地失敗,如 NetworkPolicy 擋掉後 timeout)。
- EKS 資源:destroy 後用對應 `aws` CLI 查詢確認為空。

## Teardown

- 課後 kind 叢集可留(不燒錢);要乾淨環境就 `lab-cluster.sh down [phase]`。
- Chaos drill 弄壞的叢集一律 `reset [phase]`,不留半壞狀態過夜。
- EKS lab 當堂 destroy + 驗證,絕不過夜。
