# S31 — StatefulSet: Stable Identity, Storage, and DNS

## Mental model

```text
StatefulSet replica: db-0
        |
        +-- stable ordinal name: db-0
        +-- stable storage:      data-db-0
        +-- stable DNS name:     db-0.db-hl
        |
        `-- replaceable runtime state:
            Pod UID / Pod IP / node may change
```

一句話：StatefulSet 保留的是 logical identity 與 storage identity，不是同一具 Pod runtime。

## Why Deployment is not enough

Deployment 適合可互換的無狀態副本；資料庫會撞到三面牆：

1. **儲存**：每個 database replica 應有自己的資料目錄，不能讓多個獨立 process 共寫同一顆 PVC。
2. **身分**：primary 與 replica 不可隨機互換，需要固定、可預測的成員名稱。
3. **秩序**：有狀態叢集經常需要依序建立或停止成員。

StatefulSet 只提供 Kubernetes 層的身分、儲存與建立秩序；它不會自動設定 PostgreSQL primary/replication、資料同步、leader election、backup、failover 或 promotion。

## `volumeClaimTemplates`

`volumeClaimTemplates` 是每個 ordinal 的 PVC 模板：

```text
StatefulSet web + template www

web-0 -> www-web-0 -> PV A
web-1 -> www-web-1 -> PV B
```

- 刪除 Pod 時，PVC 預設保留。
- scale down 後再 scale up，相同 ordinal 會接回原 PVC。
- PVC 名稱由 template name、StatefulSet name 與 ordinal deterministic 地組成。
- `ReadWriteOnce` 主要表示單一 node 掛載，不等於單一 Pod；即使多個 DB Pod 能在同 node 共掛，並行修改同一 data directory 仍可能損毀資料。

## Headless Service

關鍵設定：

```yaml
spec:
  clusterIP: None
```

StatefulSet 同時引用 Service：

```yaml
spec:
  serviceName: web-hl
```

一般 Service：

```text
client -> ClusterIP -> iptables DNAT -> 任一 backend Pod
```

Headless Service：

```text
client asks CoreDNS for db-0.db-hl
-> CoreDNS returns db-0's current Pod IP
-> client connects directly to that Pod IP
```

CoreDNS 只回答 IP，不搬運 application traffic。Headless Service 沒有 ClusterIP，因此沒有 Service DNAT。只連共同名稱 `db-hl` 仍可能取得多個 Pod IP；若要指定 primary，應連 per-Pod DNS，例如 `db-0.db-hl`。

## Endpoints vs EndpointSlice

兩者都是 Service 的 runtime backend 名單，本身不搬運流量。

| API | 形狀 | 用途 |
|---|---|---|
| Endpoints | 每個 Service 一個完整物件 | 簡單、方便快速查看 |
| EndpointSlice | 一個 Service 可拆成多個 slice | 擴展性較好，能表達 address type、readiness、topology 等資訊 |

快速排障：

```bash
kubectl get ep web-hl
kubectl get endpointslice -l kubernetes.io/service-name=web-hl -o wide
```

`-l` 是 label selector，用來只顯示屬於 `web-hl` Service 的 EndpointSlice；不是語法必需，但能避免混入其他 Service。`-o wide` 也是選用，用來顯示更多欄位。

## Lab evidence

- Context: `kind-k8s-coach-p2a`
- `web-0` 與 `web-1` 均 Running。
- AGE 分別為 48s 與 37s，觀察到 `web-0` 先於 `web-1` 建立。
- `www-web-0` 與 `www-web-1` 各自 Bound 到不同 PV。
- Headless Service `web-hl` 的 `CLUSTER-IP` 為 `None`。
- EndpointSlice 包含 `192.168.46.86` 與 `192.168.20.210`，後續 `web-0` 重建後更新為 `192.168.46.90`。

`web-0` replacement 證據：

| 欄位 | 刪除前 | 重建後 | 結論 |
|---|---|---|---|
| Name | `web-0` | `web-0` | 穩定 ordinal identity |
| UID | `e8dd54a4-...` | `657cd3ca-...` | 新 Pod object |
| IP | `192.168.46.86` | `192.168.46.90` | runtime network identity 可變 |
| Node | `k8s-coach-p2a-worker` | 相同 | 本次剛好相同，非 StatefulSet 保證 |
| Data | `state survives pod replacement` | 仍可讀 | 接回同一 PVC/PV |

Per-Pod DNS lookup 因 `dnstest` 殘留而未完成；EndpointSlice 已驗證 Service 選到兩個 Pod，但 DNS lookup 本身仍標記為未直接驗證。

## Troubleshooting pattern

症狀：寫入有時成功、有時收到 replica read-only。

```text
app -> ordinary Service -> random backend
                       |-> primary: success
                       `-> replica: read-only
```

第一刀是檢查 Service 實際後端：

```bash
kubectl get endpointslice -l kubernetes.io/service-name=db -o wide
```

若 Service 同時選到 primary 與 replicas，修正不是只換成共同 headless 名稱，而是使用能指向 primary 的 per-Pod DNS，或交由真正了解資料庫角色與 failover 的 operator/proxy 管理。

## Mistakes corrected

- StatefulSet 不固定 Pod IP；固定的是 ordinal name 與 DNS-based addressing。
- Pod UID 不是 PID。UID 是 API object identity；PID 是 process identity。
- client 不使用模糊的「internal ID」找 Pod，而是透過固定 DNS 名稱取得目前的 Pod IP。
- CoreDNS 回答位址，client 才建立連線。
- StatefulSet 不會讓 PostgreSQL 自動成為 production-ready HA。

## Resume point

下次從 Interview Q&A 繼續：

> 把 PostgreSQL 從 Deployment 改成 StatefulSet，是否已經 production-ready HA？StatefulSet 解決了什麼，又沒有解決什麼？
