# s49 Scheduler 與 Pending 排障(kubeadm,2026-10-16)

<!-- topic: P3 C-1 scheduler(邊界 / FailedScheduling 判準 / preemption) -->

kubeadm 3 台叢集(cp + w1/w2,t3.medium 2 vCPU)。

## 實測

| 操作 | `describe` Events | 結論 |
|---|---|---|
| Pod requests `cpu: "100"` | `FailedScheduling` From `default-scheduler`:`1 untolerated taint, 2 Insufficient cpu`,`Preemption is not helpful` | scheduler 活著,被規則擋 |
| `mv kube-scheduler.yaml /tmp/` 後建 nginx Pod | `Pending`,`<none>` | 沒人寫 Event,scheduler 不在 |
| 放回 manifest | 30s 內原 Pod 排到 w1,未重建 | scheduler 啟動後 list 所有 nodeName 空的 Pod |

## 判準

- scheduler 只做到 Bind(把 `nodeName` 寫回 API Server)。容器起不來查 kubelet,不查 scheduler。
- Pending 先看 Events:有 `FailedScheduling` 讀 Message 找規則;`<none>` 先查 scheduler 本身。
- Message 找 `Insufficient <resource>` 才是容量問題,加 node 有用。cp 的 `untolerated taint` 每次都在,當背景。
- 排不進去的 Pod 等叢集事件(node 加入、Pod 刪除、label 改)才重排,不輪詢。
- preemption 只踢 priority 較低的 Pod,走 SIGTERM + grace period;踢完單一 node 仍塞不下就不踢。一顆 Pod 只能放一台 node,資源不跨 node 相加。
- Karpenter 讀 Pending Pod 的需求開 node;Bind 仍由 scheduler 做。
