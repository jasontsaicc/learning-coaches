# Portfolio

## Workspace Directory

Progress file, registries, and in-progress work live in:

```
${CLAUDE_SKILL_DIR}/../../workspaces/k8s/
```

這個目錄是 git-tracked 學習狀態(跨機器同步:每堂課後 commit + push,開課前 pull)。內容:

- `progress.md`:engine 的進度檔。Schema engine-owned,定義在 `engine/PROGRESS-SCHEMA.md`,本 coach 不重定義。
- `term-registry.md`:domain registry(英文術語卡:EN term / 發音 / 英文定義 / 中文點破),沿用 PROGRESS-SCHEMA section 7 的 registry 欄位(interval、next-review-date、status)。抽考雙向,見 `language.md`。
- `story-bank.md`:domain registry(behavioral 素材,非間隔複習型)。學員提到真實工作經歷(prod incident、on-call、架構決策)→ 當場一行 raw 入帳,不打斷教學流;每次 Weekly Review 固定挖 10 分鐘一則保底。P6 才提煉 STAR:篩準是「衝突或壓力 / 學員自己的判斷 / 可量化結果」三佔其二;提煉時用課程學到的底層原理回注 Action 段。
- `session-log.md`:歷史 session 敘事紀錄(sessions 1-14 自 standalone 時期遷入,之後的 session 摘要續寫於此,progress.md 只留 schema 欄位)。
- `environment.md`:機器層事實(kubeconfig contexts 與安全清單、port 慣例、工具狀態、bastion 同步步驟)。
- `curriculum-plan.md`:戰略層規劃(advisory,見 `curriculum.md`)。
- `clusters/`:per-phase kind 設定檔;`notes/`:工作草稿;`labs/`:lab 暫存(gitignored)。

## Portfolio Directory

Artifacts that clear the quality bar ship to:

```
${CLAUDE_SKILL_DIR}/../../portfolio/k8s/
```

Recruiter-facing 展示區,與 workspace 分開。結構:`notes/`(學習筆記 + 踩坑,commit freely,連錯誤都有價值,不受門檻)、`manifests/`(P1-P2b 手寫物件)、`observability/`(P4 主秀)、`terraform-eks/`(P2b-P5 EKS IaC)、`gitops/`(P5 主秀)。

### Quality Bar(雙向反陷阱)

堵「懂原理但沒產出」,同時堵「public repo 塞太基礎的東西反而扣分」。展示型 artifact 過門檻才進 portfolio:問「senior 第一次看到這個,會加分嗎?」過不了的留 workspace。夠格展示的從 P3+ 長出;P0-P1 概念期常常沒有,空著正常。**別擅自重組學員目錄或搬檔**:提結構建議可以,實際搬檔讓學員自己動手。每堂結尾不強制 commit:有東西就 commit,沒有就只更新 progress.md。

## Capstone: shop platform(貫穿 P2a-P6 的持續演進平台)

s12 起的 shop-api / shop-web 不是丟棄式 lab,是一路長到 P6 的平台;每個 phase 在同一個平台上長一層,終點是 recruiter 可看的 production-like 平台 + 一條完整敘事:「我從零長出一個平台,每一層都能講到 kernel」。唯一硬要求是「同一個平台一路長」,不重開爐灶(細節 FLEX,見 curriculum-plan §4.1)。

## Per-Phase Artifacts

| Phase | shop platform 長出什麼 | artifact 落點 |
|-------|----------------------|----------------|
| P0 | 心智模型筆記(apply→Running 圖) | notes/(無展示型 artifact,正常) |
| P1 | probe / rollout / QoS-OOM 筆記與 manifests | notes/ + manifests/ |
| P2a | NetworkPolicy 隔離 api/web、Calico 叢集、封包全鏈路圖 | manifests/ + notes/ |
| P2b | api 掛 PVC(訂單資料)、最小權限 RBAC、EKS 首登:IRSA 讓 api 讀 S3 | manifests/ + terraform-eks/ |
| P3 | load generator、HPA、PDB、node 壓力大演練、capacity runbook(英文) | manifests/ + notes/ |
| P4 | Prometheus + SLO(api 可用性/延遲)、OTel 打通一條 trace | observability/(主秀) |
| P5 | Helm 化、ArgoCD 部署整個平台、EKS prod-grade terraform | gitops/ + terraform-eks/(主秀) |
| Migration 模組 | legacy 服務完整導入演練 + cutover | notes/(英文 migration runbook) |
| P6 | 平台本身變成 mock 與 behavioral 素材 | story-bank 提煉 |
