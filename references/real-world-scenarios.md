# 現實世界場景庫

> **如何使用此檔:** 對應 Teaching Flow C 段的「現實世界這樣做」固定教學元件。
> 每個場景用四段式範本(情境/生產怎麼做/真實踩坑/面試怎麼問)呈現,讓抽象機制接地氣。
> Coach 在 C 段原理講完後,拉出對應場景強化「為什麼面試官問這個」的動機感。

---

## 四段式範本(格式定義)

每個場景固定四段,**按序呈現**:

| 段 | 功能 | 說明 |
|----|------|------|
| **情境** | 開場脈絡 | 一個具體的生產場景,讓學員感受到「這不是玩具題」 |
| **生產怎麼做** | 業界正解 | 實際生產環境的處理方式/標準配置,連結到剛學的機制 |
| **真實踩坑** | 強化記憶的反例 | 這個機制最常見的翻車點,對應 Mistake Registry |
| **面試怎麼問** | 北極星連結 | 面試官會用什麼角度考這個點,對應 interview-bank.md |

使用時可選擇「全部呈現」或「只用情境引入,讓學員猜後三段」(後者適合 Feynman Gate 驗收)。

---

## P0 場景

### S-P0-1: 為什麼要用宣告式/GitOps 心智

**適用 chunk**: C-0 聲明式 vs 命令式

| 段 | 內容 |
|----|------|
| **情境** | 凌晨 2 點,你接到 on-call alert:生產 cluster 的某個 Deployment 只剩 1 個 replica 在跑,但 SLA 要求至少 3 個。你打開 kubectl 一看,replica 確實只有 1 個,但你明明記得昨天設了 3 個。到底發生了什麼? |
| **生產怎麼做** | 生產環境一律採用「Git 是唯一 source of truth」的宣告式管理: 所有 k8s manifest 放 Git repo,透過 ArgoCD 或 Flux 做 GitOps 同步。修改只能 commit 到 Git,由 CD 系統 apply 到 cluster。任何人直接 `kubectl edit` 或 `kubectl scale` 的修改,下次同步時都會被蓋回 Git 的版本。replica 數量只要看 Git 的 `replicas: 3`,就知道「正確答案」。 |
| **真實踩坑** | 有人(可能是你自己)在凌晨處理緊急事件時,用 `kubectl scale deployment --replicas=1` 降流量(命令式操作),解決了當下的問題,但忘記把 Git 的 YAML 也改回來。CD 系統在幾分鐘後同步,看到 Git 說「3 個」,把 cluster 改回 3 個。但如果 CD 同步是 manual 觸發或 interval 很長,這個「暗地裡縮減 replica」的狀態就會持續一陣子,等到 alert 觸發你才發現。根本原因: 命令式操作不留記錄、不 code review、不可 audit trail。 |
| **面試怎麼問** | 「解釋 GitOps 的核心原則是什麼。如果有人直接 `kubectl edit` 改了 production cluster,GitOps 系統會怎麼處理?你覺得這是好事還是壞事?」 |

---

### S-P0-2: Pod Pending 怎麼查

**適用 chunk**: C-3 apply→Running 全流程

| 段 | 內容 |
|----|------|
| **情境** | 你 `kubectl apply -f deployment.yaml` 之後等了 2 分鐘,Pod 還是 Pending。老闆在旁邊看,你要快速找到根因。 |
| **生產怎麼做** | 標準排查路徑(3 步走): (1) `kubectl describe pod <name>` 看 Events 欄位。Events 會告訴你是哪個元件卡住了。(2) 依 Events 的線索分支: Scheduler 輸出「0/N nodes available」→ 看資源/taint/affinity 設定;Admission webhook 相關訊息 → 看 webhook 配置;Image 相關 → 看 registry 設定和 imagePullPolicy。(3) 確認根因後修,再觀察 `kubectl get pod -w` 看狀態轉移。 |
| **真實踩坑** | 踩坑一: resources.requests 設太高,cluster 沒有足夠資源。Events 會顯示 `0/3 nodes are available: 3 Insufficient cpu`。新人常以為是網路問題或 image 問題,其實是 requests 設錯。踩坑二: Admission webhook 的 `failurePolicy: Fail` 加上 webhook 服務掛掉,導致所有 Pod 被拒絕建立。Events 裡有 webhook timeout 訊息。最危險的是這個問題會波及整個 cluster,不只是你的 Pod。修法: `kubectl get mutatingwebhookconfigurations` 找到問題 webhook,暫時 disable 或改 `failurePolicy: Ignore`。 |
| **面試怎麼問** | 「你的 Pod 一直在 Pending 狀態。第一個下的指令是什麼?看到什麼資訊你會往哪個方向查?」(典型 scenario-based 故障排除題,考排查思路的結構性) |

---

## P1 場景

> (P1 填): CrashLoopBackOff 排查流程、OOMKilled 根因追蹤、Deployment 滾動更新卡住的處理、StatefulSet headless service 的使用場景。

---

## P2a 場景

> (P2a 填): Service ClusterIP 不通怎麼查(kube-proxy/iptables 視角)、CoreDNS 5-second timeout 坑(ndots)、NetworkPolicy 意外封鎖流量、Ingress 404 排查路徑。

---

## P2b 場景

> (P2b 填): PVC 一直 Pending(StorageClass 沒設 default)、RBAC 403 Forbidden 排查、IRSA Token 拿不到(annotation 沒設)。

---

## P3 場景

> (P3 填): HPA 在流量尖峰前反應太慢(scale-up 速度調整)、節點資源耗盡觸發 eviction、滾動更新出包緊急 rollback、PDB 讓 drain 卡住。

---

## P4 場景

> (P4 填): SLO 設定太緊導致 Error Budget 燒光(on-call 壓力)、分散式追蹤找到 p99 latency 根因、Alertmanager 告警太吵怎麼降噪。

---

## P5 場景

> (P5 填): GitOps sync 失敗排查(ArgoCD OutOfSync)、Helm upgrade 出問題回滾、progressive delivery canary 異常中止。
