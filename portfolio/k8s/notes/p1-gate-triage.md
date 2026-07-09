# P1 畢業 Gate — on-call triage drill

一次 apply 三隻中性命名的故障 Pod,靠 `kubectl` 逐一定位根因(不看原始 YAML)。

## 三故障拆解

| 服務 | 現象 | 真正死因 | 底層機制 | 修法 |
|------|------|----------|----------|------|
| payment-api | ImagePullBackOff | tag `nginx:1.99` 不存在 | 驗證邊界:合法字串騙過 API Server,kubelet 第 5 棒拉 image 才發現 | 改對 tag |
| cache-worker | CrashLoop / exit 137 | 撞 memory limit | 不可壓縮資源 + cgroup 硬天花板 + kernel OOM killer | 先分 leak/rightsize 再決定 |
| web-frontend | CrashLoop / exit 0 | liveness probe 打 8080,nginx 聽 80 | probe 殺健康 app,SIGTERM 優雅退出 | 修 probe,不動 app |

## 速查表:exit code 講出死因 (CrashLoopBackOff 只是現象)

第一指令 `kubectl get pods`(看 STATUS + RESTARTS),再 `kubectl describe pod`(讀 Reason + Exit Code)。

| describe 看到 | 死因 | 下一步 |
|--------------|------|--------|
| Exit 137 / OOMKilled | 記憶體爆 limit,kernel 砍 | 看 requests/limits + 記憶體趨勢 |
| Exit 0 / Completed | app 健康,被 probe 殺 | 查 probe 設定,不要動 app |
| Exit 1 / Error | 程式啟動就 crash | `kubectl logs --previous` |
| ImagePullBackOff | 根本沒起來 | 看 Events 的 image 名稱 / auth |

關鍵領悟:exit 0 出現在 crash loop = 容器收到 SIGTERM 後乾淨退出,代表 app 沒壞,是設錯的 liveness probe 在殺一個健康的 Pod。

## liveness probe 不准碰外部依賴 (A 段複習)

判斷句:**Would a restart fix this?** 修得好(自己卡死)→ liveness;修不好(DB/下游)→ readiness。

把 DB 檢查放 liveness 的雪崩鏈:DB 變慢 → 全部 Pod 同時 liveness 失敗 → 同時 restart(thundering herd 羊群效應)→ 服務從「慢」跳級成 CrashLoopBackOff 全掛 → reconnection 風暴回壓本來只是慢的 DB → 正回饋越救越死。

## metrics-server on kind (踩坑)

`kubectl top` 不自己算,它問 `metrics.k8s.io` API,由 metrics-server 服務,metrics-server 去刮各 node 的 kubelet (cAdvisor)。kind 預設不裝 → 「Metrics API not available」。HPA (P3) 讀同一個 metrics-server。

裝法 + kind 專屬旗標:
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl patch deployment metrics-server -n kube-system --type=json -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
```
kind 的 kubelet 用自簽憑證,不加 `--kubelet-insecure-tls` 會 x509 報錯刮不到。patch 後要等 rollout + 首次 scrape,`apiservice v1beta1.metrics.k8s.io` 才會 Available,別 patch 完馬上 `top`。
