# P1 chunk 5 — resource / QoS / OOM

## requests vs limits

| | requests | limits |
|---|----------|--------|
| 角色 | 預訂量 + 排程依據 | 硬天花板 (hard cap) |
| 誰用 | scheduler:node 上所有 Pod 的 requests 加總 ≤ node allocatable | cgroup:kernel 強制執行 |
| 超賣 | 不能超賣 (scheduler 把關) | 可超賣 (賭不會同時衝頂) |

只設 limit、不設 request → k8s 自動補 request = limit。

## 可壓縮 vs 不可壓縮 (compressible / incompressible)

| | CPU | Memory |
|---|-----|--------|
| 本質 | 可壓縮,時間可以晚點給 | 不可壓縮,寫進去的 byte 收不回 |
| 撞 limit | throttle (節流變慢,不死) | OOMKilled (直接砍),exit 137 = 128+9 SIGKILL |

## 兩種 OOM (面試常挖坑)

| | 容器級 OOM | node 級 OOM / eviction |
|---|---|---|
| 觸發 | 撞自己 cgroup limit | 整台 node 記憶體快用光 |
| 誰動手 | kernel OOM killer | kubelet 驅逐 |
| 跟 node 剩多少有關 | 無關 | 直接相關 |
| 砍誰 | 超標那個容器 | 按 QoS class |

"node 還有記憶體卻 OOMKilled" = 容器級:撞自己 cgroup 天花板,與 node 餘量無關。

## QoS class + 驅逐順序

| class | 條件 | 驅逐順序 |
|-------|------|---------|
| Guaranteed | 每容器 cpu+mem 都設且 requests==limits | 最後砍 |
| Burstable | 有設但未達 Guaranteed | 中間 (超出自己 request 越多越先砍) |
| BestEffort | 完全沒設 | 最先砍 |

prod 關鍵服務 → requests==limits 釘成 Guaranteed,最不易被踢。

## 排障速查表 (CrashLoopBackOff 是現象,不是死因)

第一指令:`kubectl describe pod <name>`

| describe 看到 | 死因 | 下一步 |
|--------------|------|--------|
| Last State Reason: OOMKilled, Exit 137 | 記憶體爆 limit | 看 requests/limits + 記憶體趨勢 |
| Last State Reason: Error, Exit 1 | 程式 crash | `kubectl logs --previous` |
| Events: Liveness probe failed + Killing | probe 殺的 | 查 probe 設定 |
| Status: ImagePullBackOff | 沒起來 | 查 image 名稱 |

`kubectl logs <pod> --previous`:看上一個已死容器的遺言。RESTARTS>0 查死因一律加 `--previous`,否則在看新屍體找不到傷口。

## OOM 治本 vs 治標

確定 OOM 後別急著調大 limit。先分:
- 鋸齒一路爬到頂才被砍 → memory leak,調大 limit 只是延後 OOM (治標)。
- 爬到某水位平掉、穩定高於 limit → 真的設太小,調大才對。

## lab

`portfolio/manifests/oom-demo.yaml`:polinux/stress 要 150M、limit 100Mi → Burstable + OOMKilled + exit 137,node 記憶體仍充足。
