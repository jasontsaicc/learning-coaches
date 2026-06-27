# 面試題庫

> **如何使用此檔:** 對應 Teaching Flow G 段(面試 Q&A,固定 5min,不可跳)。
> 每個 phase 結束前從這裡選題做 G 段模擬;P6 全力衝刺時密集使用。
> 題目標注「首見 phase」,G 段只用學員已學過的範圍。

---

## 題目分類

| 類別 | 說明 | 考察重點 |
|------|------|---------|
| **原理題** | 解釋機制、說清楚底層是什麼 | 能不能打穿到底層原理,不只是背 YAML 欄位 |
| **故障排除** | 給一個生產現象,問排查路徑和根因 | 排查思路的結構性(第一個指令是什麼,為什麼) |
| **k8s x system design** | k8s 機制和大系統設計的交集 | senior SRE 視角:能不能設計可靠的系統 |
| **CKA/CKAD 限時(副線)** | timed 操作題,手速 + 語法記憶 | P6 才密集練,前期不是重點 |

---

## 原理題

### Q-P-01: apply 到 Running 全流程(P0 核心 Gate 題)

**適用 phase**: P0+
**難度**: P0 畢業 Gate 必過

**題目**: 「從 `kubectl apply -f pod.yaml` 到 Pod 狀態顯示 Running,每一個參與的元件依序做了什麼?請盡可能詳細說明,包括 authn、authz、admission control 各是什麼時機,etcd 被寫了幾次,scheduler 怎麼選 node,kubelet 怎麼知道要啟動這個 Pod。」

**Pass 條件**:
- 點到所有元件: API server、etcd、scheduler、kubelet、CRI
- 正確描述 API server 三道關卡順序(authn → authz → admission)
- 說清楚 scheduler 是 watch 到 unscheduled pod 才動,不是被呼叫
- 說清楚 kubelet 也是 watch,不是輪詢
- 知道 etcd 被寫兩次(Pod 物件 + scheduler 填 nodeName)

**Stretch(加分不強求)**:
- 說出 level-triggered reconcile 在哪裡體現
- 說出 Raft quorum 為什麼讓 etcd 成為可靠的 source of truth

**Coach 引導方向**: 學員卡在某段時,問「那這個元件是怎麼知道有事情要做的?它是被叫,還是自己發現的?」

---

### Q-P-02: 宣告式 vs 命令式在 failure recovery 的差異

**適用 phase**: P0+
**難度**: P0 基礎題

**題目**: 「解釋 Kubernetes 為什麼選擇宣告式 API。命令式和宣告式在 failure recovery 上有什麼核心差異?」

**Pass 條件**:
- 能說出「宣告式 = 說目標態,系統自己搞定」
- 能說出「冪等性(idempotency)」的概念
- 能說出「reconcile loop 讓系統自癒」這個機制

**Stretch**: 能連到控制理論(setpoint + feedback loop)

---

### Q-P-03: etcd 和 Raft

**適用 phase**: P0+
**難度**: P0 基礎題

**題目**: 「etcd 在 Kubernetes 中扮演什麼角色?它用什麼機制保證高可用?為什麼 etcd 節點數一定要是奇數?」

**Pass 條件**:
- 說出 etcd 是 source of truth,所有 k8s 物件存在這裡
- 說出 Raft 讓多個節點保持一致
- 說出 quorum = 多數決,奇數節點才能有明確多數

**Stretch**: 「2 個 etcd 節點為什麼比 1 個還差?」(quorum = 2,任一個掛就停擺,相當於沒有容錯)

---

### Q-P-04: static pod 的設計哲學

**適用 phase**: P0+
**難度**: P0 進階題(Stretch)

**題目**: 「為什麼 Kubernetes control plane 的元件(api-server、etcd、scheduler、controller-manager)要用 static pod 的形式跑,而不是用 Deployment?」

**Pass 條件**:
- 指出「雞生蛋」問題: 如果用 Deployment 管 controller,controller 掛了誰來管 Deployment?
- 說出 static pod 由 kubelet 直接讀 manifest 啟動,不需要 API server 存活

---

### Q-P-05: 容器和 VM 的本質差異

**適用 phase**: P0/P1+
**難度**: P0/P1 基礎題

**題目**: 「容器和 VM 的隔離機制有什麼本質差別?Kubernetes 的 resource limits(CPU/memory)在 Linux 底層對應什麼機制?」

**Pass 條件**:
- 說出容器共用 host kernel,用 namespace(隔離視角)+ cgroup(限制資源)
- VM 用 hypervisor 做硬體虛擬化,kernel 完全隔離
- resource limits 對應 cgroup 的 `memory.limit_in_bytes` 和 `cpu.cfs_quota_us`

---

## 故障排除(Scenario-Based)

### Q-T-01: Pod 一直 Pending

**適用 phase**: P0/P1+
**難度**: P0/P1 基礎排障題

**題目**: 「你 `kubectl apply -f deployment.yaml` 之後,Pod 一直是 Pending 狀態。你的排查步驟是什麼?」

**理想回答結構**:
1. `kubectl describe pod <name>` 看 Events
2. 依 Events 線索分支:
   - `0/N nodes available` 開頭 → 資源不足/taint/affinity 設定
   - admission webhook 相關 → 查 webhook config
   - image 相關 → 查 registry/imagePullPolicy
3. 說出每個分支怎麼確認根因

**Coach 追問**: 「如果 Events 裡完全沒有訊息呢?你會怎麼做?」(期望: 看 scheduler log、確認 scheduler 是否存活)

---

### Q-T-02: controller 當機 10 分鐘後重啟

**適用 phase**: P0+
**難度**: P0 概念題(考 level-triggered 理解)

**題目**: 「controller 當機了 10 分鐘,這段期間有 3 個 Pod 掛掉。controller 重啟後,它需要知道『是哪 3 個 Pod、什麼時候掛的』嗎?為什麼?」

**Pass 條件**:
- 說出「不需要」,因為 level-triggered
- 說清楚: 重啟後重讀 etcd,發現 actual < desired,直接補起來
- 不需要重播事件歷史

---

## k8s x System Design 交集

### Q-SD-01: 多副本 scheduler 的 leader election

**適用 phase**: P0(Stretch)/P3+
**難度**: P0 Stretch,P3 正式題

**題目**: 「Kubernetes scheduler 為什麼要做 leader election?如果同時有兩個 scheduler 在跑,會有什麼問題?」

**Pass 條件**:
- 說出可能重複調度同一個 Pod 到兩個 node 的問題
- 說出 lease/leader election 確保同時只有一個 scheduler 做決策
- Stretch: 說出 leader election 本身也是 etcd 裡的一個物件

---

### Q-SD-02: 為什麼 etcd 要分開部署,不和 api-server 同主機(P2b+)

**適用 phase**: P2b+
**難度**: 中級

> (P2b 填更完整答案)

---

## CKA/CKAD 限時(副線,P6 才密集練)

> 以下題目不是主線教學,P6 才使用。記錄在此作為索引。

### Q-CKA-01: 快速建立 Pod/Deployment YAML

**題目**: 「在 2 分鐘內,不查文件,建立一個 3 replica 的 nginx Deployment,並 expose 為 ClusterIP Service port 80。」

```bash
kubectl create deployment nginx --image=nginx --replicas=3 --dry-run=client -o yaml > dep.yaml
kubectl apply -f dep.yaml
kubectl expose deployment nginx --port=80 --target-port=80
```

---

### Q-CKA-02: 找出哪個 node 資源最多可用

**題目**: 「不用第三方工具,快速看哪個 node 現在 allocatable CPU 最多。」

```bash
kubectl describe nodes | grep -A5 "Allocatable:"
kubectl top nodes
```

---

## 面試題維度對應 Scorecard

| Scorecard 維度 | 主要對應題目類別 |
|---------------|----------------|
| 能講清楚底層原理 | 原理題(Q-P-*) |
| 理解內部機制 | 原理題 + k8s x SD |
| 能用自己的話解釋 | 全部,但看敘述流暢度 |
| 故障排除速度 MTTR | 故障排除(Q-T-*) |
| 可觀測性設計 | P4+ 原理題(P4 填) |
| 能定義/解讀 SLO | P4+ 原理題(P4 填) |
