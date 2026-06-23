# P1 筆記:Deployment / Rolling Update / Rollback (2026-06-23)

## 核心機制:Deployment 不直接管 Pod,管 ReplicaSet

```
Deployment → ReplicaSet → Pod
```

- 改 image = 改 desired state → Deployment **新建一個 RS**,玩翹翹板:新 RS 0→N、舊 RS N→0
- 任何一刻兩邊加起來都有 Pod 在服務 → 不中斷
- 跑完舊 RS 縮到 0 **但不刪除** → 這就是 rollback 的退路
- Pod 名中間那段 hash = 它的 ReplicaSet 名;rolling update 時看得到兩組 hash

## 兩個旋鈕(面試必考)

| 旋鈕 | 管什麼 | 公式 |
|------|--------|------|
| `maxSurge` | 過程中最多比 desired **多**幾個(額外,不是總數)| 總數上限 = replicas + maxSurge |
| `maxUnavailable` | 過程中最多容忍幾個**不可用** | 可用數下限 = replicas - maxUnavailable |

- 兩個都可寫數字或百分比,**預設都 25%**
- `maxUnavailable` 守的是「**服務中(READY)的數量**」,不是物件總數(Terminating 的還算一行)
- **零停機正解**:`maxUnavailable: 0` + `maxSurge: 1`(或 25%)→ 先擴後縮(surge first)、慢速金絲雀、只要 25% 額外資源
- `maxSurge: 8` 這種大數字能動但浪費:等於 4 個新的一次全開(big-bang),要 2 倍資源、無 canary 緩衝
- **死鎖**:`maxSurge: 0` + `maxUnavailable: 0` → 不能多生也不能先砍 → k8s **apply 直接退件** `may not be 0 when maxSurge is 0`(又一次 fail loud)

## Rollback

- `kubectl rollout undo deployment/<name>` → 退回上一版
- **為什麼快**:不是重新部署,是把留著的舊 RS 重新 scale up → 不用重拉 image,容器秒起
- `kubectl rollout history` 看版本史;`CHANGE-CAUSE` 預設 `<none>`,真實環境加 annotation `kubectl.kubernetes.io/change-cause` 才看得懂每版改啥

## 驗證有邊界(面試金句)

- schema/語法錯(`metaData` 打錯)→ **API Server apply 當場退件**(fail loud)
- 外部現實(image 不存在、DNS 解不到、下游不通)→ API Server **無從得知**,只有 **kubelet 第 5 棒真的去拉**才爆 → 表現為 ImagePullBackOff
- 一句話:API Server 只驗證「字串語法」,「repo 存不存在」是 runtime 才知道的事

## Lab 實測(rollout-demo:nginx,replicas=4,maxSurge=1,maxUnavailable=1,minReadySeconds=10)

- 正常 rollout v1.25→v1.26:`get pods -w` 看到總數摸到 5、分批換(年齡 37s/21s 落差 = minReadySeconds 在踩節奏)
- rollback：連續 `get rs` 抓到舊 RS 0→4 復活、新 RS 4→0 縮回,幾乎瞬間
- **壞部署 drill**(`set image web=nginx:9.99`):卡死幾何 = **3 好(Running)+ 2 壞(ImagePullBackOff)= 5 總數**
  - 砍 1 舊(用掉 maxUnavailable）+ 生 2 新填滿天花板(maxSurge）→ 兩旋鈕同時頂死 → rollout 凍住
  - `rollout status` 永遠 `Waiting...`;3 個舊 Pod 全程沒重啟(年齡 5m+ vs undo 補的 13s)→ 用戶零感知
  - 急救 `rollout undo` 中止壞部署

## 今天的踩坑(留著,有價值)

1. image 打成 `ngimx:1.25`(n→m)→ ImagePullBackOff。**apply 不擋(字串語法合法),第 5 棒 kubelet 拉才爆**。`describe pod` 看 Events 一眼看到 `Pulling image "ngimx:1.25"` + `repository does not exist`
2. `set image` 改 image 會造成 YAML 檔與 cluster drift(檔還是舊值)→ 真實環境別用 imperative 改線上,走 GitOps

## English Polish 收藏

- we do a **rolling update**: spin up new pods, drain old ones gradually, so the service **never drops to zero**
- set `maxUnavailable: 0` for a **zero-downtime** deploy; it **surges up first** before retiring old pods
- a bad image just **stalls the rollout**; the old pods **keep serving**, users don't notice
- `rollout undo` is fast because it **scales the old ReplicaSet back up**, no image re-pull
- the API Server only validates **syntax**; whether the image actually exists is **only knowable at pull time**
