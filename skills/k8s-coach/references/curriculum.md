# Curriculum

8 個 phase。排課哲學:P0-P2b 概念打底(但每堂動手 + 故障注入)→ P3-P5 專案/實戰驅動 → P6 面試衝刺。**不要在 session 開始時一次讀完所有 references**,只在進到該 phase / 該段時讀對應檔。

每學員的戰略層規劃(面試窗口、里程碑時間軸、capstone 主線、選修池)在 `workspaces/k8s/curriculum-plan.md`,advisory 性質;runtime 真相以 progress.md 為準,衝突時現場贏、回寫該檔。

## Warm-Up Diagnostic (new students only)

新學員先給課程地圖(8 phases),再跑一個快速診斷抓程度,讓互動從第一分鐘開始:

- 用一個生產情境開問(e.g.「一個 Pod 一直 `CrashLoopBackOff`,你會怎麼開始查?」),聽 2-3 分鐘。
- 依回答分流:**強**(講得出排查路徑)→ P0 可加速;**中**(知道片段但無章法)→ P0 剛好;**白**(不知從何下手)→ 安撫,這正是 P0 要補的。
- 結果寫進 progress.md(engine schema 的 warm-up classification 欄位),作為 routing 與 pacing 依據。

## Phase Map

| Phase | 一句話焦點(往內部機制走) | 前置 | 教材 reference |
|-------|------------------------|------|----------------|
| **P0 心智模型** | 聲明式 / reconcile loop / control plane 拆解 / apply→Running 全流程 | 無(入門 phase) | `references/phase-0-mental-model.md` |
| **P1 核心物件 + 容器底層** | Pod/probe、Deployment/rollout、StatefulSet/Job、resource/QoS + namespace/cgroup/OOM | P0 gate | 無獨立教材檔;底層深化在 `references/foundations-linux-network.md` §2 |
| **P2a 網路深水區** ⭐ | Service/kube-proxy/CoreDNS、Ingress、NetworkPolicy、CNI + 封包全鏈路 | P1 gate | `references/phase-2a-networking.md` |
| **P2b 儲存 + 權限** | PV/PVC/CSI、StorageClass、RBAC/SA、IRSA、Secrets 管理、Pod Security Standards | P2a gate | `references/phase-2b-storage-rbac.md` |
| **P3 調度 + 高並發 + 排障** ⭐ | scheduler、affinity/taints、HPA/VPA/Karpenter、PDB、capacity planning | P2b gate | `references/phase-3-scheduling-resilience.md` |
| **P4 可觀測性工程** | 三本柱、Prometheus/PromQL、SLI/SLO/Error Budget、OTel/Jaeger | P3 gate | `references/phase-4-observability.md` |
| **P5 平台工程 / GitOps** | Helm、ArgoCD/GitOps、EKS prod terraform、progressive delivery、CRD/operator、admission webhook、cluster upgrade、etcd 運維(backup/restore/DR,含 Raft 深入) | P4 gate | `references/phase-5-platform-gitops.md` |
| **P6 面試衝刺** | SRE 故障 mock、k8s × system design 交集、behavioral story bank 提煉(STAR、英文版)、CKA/CKAD 限時(副線) | P5 gate | `references/phase-6-interview-sprint.md` |

⭐ = Linux/網路底層集中重練區。教材是彈藥庫不是逐字稿,runtime 以 progress.md 即時狀態決定怎麼用,檔內 `[RUNTIME: ...]` 標記處需現場客製。

## Cross-Phase References

| 檔案 | 內容 |
|------|------|
| `references/foundations-linux-network.md` | 跨 phase 底層:控制理論 / namespace+cgroup / TCP 狀態機 / DNS 全流程 / Linux 性能排查(USE + 60 秒清單) |
| `references/chaos-drills.md` | 故障注入劇本庫 20 drills(P0-P5,step E 用;P3 起附 runbook 產出要求) |
| `references/real-world-scenarios.md` | 現實場景庫 23 scenes(P0-P5,step B/C 四段式範本) |
| `references/term-glossary.md` | 英文術語總表 |
| `references/interview-bank.md` | 面試題庫:原理題 why-chain(Q-P)/ 故障排除(Q-T)/ k8s×SD(Q-SD)/ 誘答庫(P0-P5)/ Behavioral(Q-B)/ CKA 副線(Q-CKA) |

## Milestones Beyond the Phase Map

- **迷你 mock**:P2a 結束、P3 結束各插一次 30min 迷你 mock,提早用面試語境校準,結果回饋進 phase gate 判定。
- **CKA sprint**:P5 畢業後 2-3 週 sprint(kubeadm、etcd backup/restore、限時故障題),證書趕在投遞前到手;原理已在 P0-P5 打穿,sprint 只補速度與考試格式(curriculum-plan §4.8)。
- **Migration 模組**:P5 之後、P6 之前,把一個 legacy 服務完整導入 k8s(containerize → manifests → 有狀態搬遷 → zero-downtime cutover → rollback 計畫),產出英文 migration runbook(curriculum-plan §4.6)。
