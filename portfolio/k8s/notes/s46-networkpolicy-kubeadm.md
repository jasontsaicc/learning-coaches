# s46 NetworkPolicy 白名單實測(kubeadm,2026-10-13)

<!-- topic: P2a NetworkPolicy(白名單 + default-deny 翻轉 + 第四個引擎) -->

kubeadm 3 台叢集 + Calico v3.33.0,ns `netpol-lab`。frontend、db 在 w2,backend 在 w1,frontend → backend 封包真的走 VPC。Manifests:`portfolio/k8s/manifests/netpol-lab/`。

## 套用順序與結果

| 步驟 | 檔案 | `curl http://backend`(從 frontend) |
|---|---|---|
| 1-2 場景,沒有 policy | `scene.yaml` | `backend`(全通) |
| 3 default-deny | `default-deny.yaml` | `Resolving timed out` |
| 4 開 DNS | `allow-dns.yaml` | `Connection timed out` |
| 5 frontend egress 寫 80 | `frontend-egress.yaml` | `Connection timed out` |
| 5 frontend egress 改 5678 | `frontend-egress.yaml` | `backend` |

## 驗收矩陣

| 來源 → 目的 | 結果 | 擋住的門 |
|---|---|---|
| frontend → backend | 通 | |
| backend → db | 通 | |
| frontend → db | 斷 | frontend egress + db ingress |
| tmp(netpol-lab,無 label)→ backend | 斷 | tmp egress(被 default-deny 選中)+ backend ingress |
| tmp(default ns)→ backend | 斷 | 只有 backend ingress |

## 判準

- policy 只管 `podSelector` 選到的 Pod。沒被任何 policy 選到 = 進出全開。多條選到同一 Pod,白名單相加。
- `podSelector: {}` 選中 ns 內所有 Pod,包括之後才建立的 Pod。
- 兩端都被選中時,A → B 要 A 的 egress 和 B 的 ingress 都放行。同 AWS 跨帳號 assume role:呼叫方 identity policy + 目標 trust policy。
- 用名字連線時,DNS 查詢是第一個 egress 封包。egress 全擋時先死在 DNS。
- policy 丟封包不回應,錯誤是 timeout 不是 refused。看關鍵字分層:`Resolving` = DNS,`Connection` = 連線。
- 封包進 node kernel 先做 kube-proxy DNAT,之後 Calico 才檢查。ingress 和 egress 都寫 Pod 的 targetPort(5678),不是 Service port(80)。寫錯不報錯,只是永遠對不到。

## from 裡的 `-`:AND vs OR

```yaml
# A:同一個項目 = AND
from:
- namespaceSelector: {matchLabels: {team: ops}}
  podSelector: {matchLabels: {app: monitor}}

# B:兩個項目 = OR
from:
- namespaceSelector: {matchLabels: {team: ops}}
- podSelector: {matchLabels: {app: monitor}}
```

| | 放行 |
|---|---|
| A | `team=ops` ns 裡有 `app=monitor` 的 Pod |
| B | `team=ops` ns 的所有 Pod,加上 policy 所在 ns 裡 `app=monitor` 的 Pod |

單獨的 `podSelector` 指 policy 所在的 ns。B 比 A 多放行一整個 ns,apply 不報錯。本堂只講解,尚未實測。

## 測試技巧

http-echo image 沒有 curl。用 `kubectl run tester --labels app=backend --image=curlimages/curl` 冒充 backend:policy 只認 label。反過來說,能在 ns 裡建 Pod 的人就能貼任何 label 繞過白名單,要靠 RBAC 或 admission 限制。
