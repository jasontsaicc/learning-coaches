# P1 筆記:Container / Pod / Probe (2026-06-22)

## P0 收尾(心智模型)

- apply→Running 五棒:API Server 寫 etcd → controller 看 desired 建 Pod → scheduler 綁 node → kubelet 起 runtime → 回報狀態
- 精準度:**只有 API Server 直接讀寫 etcd**,其他元件(controller/scheduler/kubelet)走 API Server 的 watch/update。etcd 掛了 → `kubectl get` 也讀不到

## 1. Container 是什麼

- = 被 **namespace + cgroup** 圈起來的**普通 Linux 行程**,不是 VM
- 共用 host kernel(VM 有獨立 kernel)→ 啟動快、省資源
- namespace = 能**看到**什麼(隔離視野);cgroup = 能**用**多少(限制資源)
- Linux namespace ≠ k8s namespace:後者只是**邏輯分組**(套 RBAC/quota),**不做隔離**;擋網路要 NetworkPolicy

## 2. Pod 是什麼

- 一組**共享 network namespace** 的 container:同 IP、可用 localhost 互通
- pause container 先佔住 network ns,其他 container 加入它
- 各自獨立:filesystem(MNT)、cgroup
- sidecar 模式:log/metric/proxy 跟 app 同 Pod,走 localhost
- 規則:**同生共死**(一起 scale/重啟/綁同 node)才放同 Pod;能各自 scale 就拆(app 和 DB 不放同 Pod)

## 3. Probe(本日重點)

| | readiness 壞掉 | liveness 壞掉 |
|---|---|---|
| RESTARTS | `0` 不重啟 | `+1` 重啟 |
| STATUS | Running | Running(重啟後) |
| READY | `0/1` 卡住 | `0/1` → 自己回 `1/1` |
| endpoints | 被移除 → **切流量** | 短暫移除,恢復後回來 |
| 會自己好嗎 | 不會,要修根因 | 會(只要重啟能解決) |

- startup probe:慢啟動 app 的緩刑,啟動完才開始跑 liveness(避免被誤殺)
- **偵測延遲 = failureThreshold × periodSeconds** = probe 的調校旋鈕;設太敏感 → 一點抖動就誤判狂重啟
- **liveness 不要查下游依賴(DB)**:DB 一抖 → 全 Pod liveness 同時失敗 → 集體重啟 → 雪崩。判斷句:**Would a restart fix this?** Yes 才放 liveness
- **Running ≠ Ready**:Pod 可以 Running 但 `0/1`(NotReady),被踢出 endpoints。線上「Running 卻連不到」第一個查 readiness + endpoints

## Lab 實測(probe-demo:busybox + exec probe,信物 /tmp/ready /tmp/alive)

- `rm /tmp/ready` → READY `0/1`、STATUS Running、RESTARTS `0`、endpoints 空(切流量但不重啟);手動 `touch` 才回名單
- `rm /tmp/alive` → RESTARTS `+1`,重啟後 container command 重新 touch → 自癒回 `1/1`

## 今天的踩坑(留著,有價值)

1. `matchLabels` 又打成 `matchLables`(selector 欄位,兩週內第二次)→ dry-run 噴 `unknown field "..."` 直指位置。要變肌肉記憶,apply 前先 `--dry-run=client`
2. 一開始把 readiness 的職責(能不能接新請求)塞給 liveness → 自己推出「重啟修不好變慢的 DB」後修正
3. liveness 重啟不是瞬間:`Ctrl+C` 太早看不到;`rm: No such file` 反而證明「容器還沒 restart」

## English Polish 收藏

- containers in the same Pod **share a single network namespace**, so they **get the same IP** and **talk over localhost**
- **co-locate containers** in one Pod for sidecar use cases (**ship logs**, **scrape metrics**)
- the pod **gets removed from the Service endpoints** until it becomes ready again
- a liveness probe should only answer one question: **is this process still alive?**
