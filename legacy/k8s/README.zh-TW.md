**[English](README.md)** | **[繁體中文](README.zh-TW.md)**

# k8s-coach：Kubernetes / SRE 深度學習 Skill

> 不是背 YAML，不是刷 CKA 題庫。
> 你的 AI 化身蘇格拉底式導師，把每個 k8s 機制打穿到底層的 OS、網路、分散式系統原理，然後讓你在真實叢集裡親手除錯。

一個給 Claude Code 使用的 AI 教練 skill，讓 AI 成為你的 Kubernetes / SRE 面試教練。費曼學習法、第一性原理推導、動手 chaos drill。與 `sd-coach`、`leetcode-coach` 同家族。

---

## 北極星

**通過大廠 senior DevOps / SRE 面試，拿到外商 offer。**

「打穿底層原理」(OS、網路、分散式系統、控制理論) 是手段，不是目的。課程裡每個取捨都回頭問同一個問題：這對面試和 package 有幫助嗎？

---

## 8 個 Phase 課程地圖

| Phase | 一句話焦點 |
|-------|-----------|
| **P0 心智模型** | 聲明式 API、reconcile loop、control plane 拆解、apply 到 Running 全流程 |
| **P1 核心物件 + 容器底層** | Pod/probe、Deployment/rollout、StatefulSet/Job、resource/QoS、namespace/cgroup/OOM |
| **P2a 網路深水區** | Service/kube-proxy/CoreDNS、Ingress、NetworkPolicy、CNI、封包全鏈路 |
| **P2b 儲存 + 權限** | PV/PVC/CSI、StorageClass、RBAC/ServiceAccount、IRSA |
| **P3 調度 + 高並發 + 排障** | scheduler、affinity/taints、HPA/VPA/Karpenter、PDB、capacity planning |
| **P4 可觀測性工程** | 三本柱、Prometheus/PromQL、SLI/SLO/Error Budget、OTel/Jaeger |
| **P5 平台工程 / GitOps** | Helm、ArgoCD/GitOps、EKS prod Terraform、progressive delivery |
| **P6 面試衝刺** | SRE 故障 mock、k8s x system design 交集、CKA/CKAD 限時練習 (副線) |

**MVP 現況：** P0 已上線 (reference 教材完整)。P1 到 P6 為後續計畫，會逐步增加。

---

## 安裝

前置：`kind`、`kubectl`、一把已註冊在 GitHub 帳號的 SSH key。

```bash
git clone git@github.com:jasontsaicc/k8s-mastery-lab-skill.git ~/jason/k8s-coach
mkdir -p ~/.claude/skills && ln -s ~/jason/k8s-coach ~/.claude/skills/k8s-coach
```

symlink 把 repo 掛上 Claude Code 的 skill 路徑，skill 才讀得到 `k8s-coach-workspace/progress.md`。

### 跨機器同步

session 狀態 (`progress.md`、mistake/term registry、叢集設定) 都進 git。換另一台 VM 續傳：上課前 `git pull`，下課後 `git commit` + `git push`。一律先 pull 再開工，兩台才不會分岔。

---

## 如何開始

1. 在此目錄開啟 Claude Code (或任何 `k8s-coach` 在 skill 路徑上的地方)。
2. 說：**「開始學 Kubernetes」** 或 **「start k8s-coach」**。
3. Skill 讀取 `k8s-coach-workspace/progress.md` 後自動分流：全新學員暖身、從斷點續傳、或每週回顧。

---

## Lab 環境

本機叢集用 `kind` 跑，透過一支腳本統一管理：

```bash
scripts/lab-cluster.sh up p0      # 開 P0 lab 叢集
scripts/lab-cluster.sh reset p0   # 摔壞後乾淨重建 (chaos drill 用)
scripts/lab-cluster.sh down p0    # 關掉叢集
scripts/lab-cluster.sh status     # 列出所有 k8s-coach-* 叢集
```

EKS 在 P2a (雲端整合主題) 才進場。Terraform 指令以 code block 產出讓你自行執行，skill 本身不直接動雲端資源。

---

## Workspace 與 Portfolio

| 路徑 | 用途 |
|------|------|
| `k8s-coach-workspace/` | 本機 session 狀態：進度、斷點、mistake registry、term registry、叢集設定 |
| `k8s-portfolio/` (獨立 repo) | Public artifact repo：manifests、runbook、SLO dashboard、GitOps 設定，recruiter 看得到的作品 |

Portfolio 在第一堂 P0 初始化。每堂結束都 `git commit` 到 `k8s-portfolio`，確保每次學習都有具體產出。

---

## 為什麼不一樣

**動手 + chaos drill，不是背 YAML。**

每個主題走這個循環：

1. **推導** 機制背後的 OS / 網路 / 分散式系統原理。
2. **Lab** 在真實 `kind` 叢集裡親手操作、觀察現象。
3. **弄壞** (chaos drill) 再限時 debug 到根因。
4. **教回來** (Feynman Gate) 用自己的話解釋才能過關往下。
5. **面試 drill** (每堂固定 5 分鐘，不可跳過) 持續校準北極星。

每堂結束都 commit portfolio，把理解轉成可展示的產出。

---

## 專案結構

```
k8s-coach/
├── SKILL.md                          # 教學引擎：routing、flow、gates、protocols
├── scripts/
│   └── lab-cluster.sh                # Lab 叢集生命週期管理 (kind)
├── references/
│   └── phase-0-mental-model.md       # P0 教材 (MVP 已上線)
├── k8s-coach-workspace/              # 本機 session 狀態 (不進 portfolio repo)
└── evals/                            # Skill 驗證測試案例
```

---

## License

MIT
