# Portfolio

## Workspace Directory

Progress file, registries, and in-progress work live in:

`../../workspaces/k8s/`（相對於 coach 的 `SKILL.md`）

這個目錄是 git-tracked 學習狀態；跨機器同步依 SKILL.md Session Sync 的授權與保留本地變更規則。內容:

- `progress.md`:engine 的進度檔。Schema engine-owned,定義在 `engine/PROGRESS-SCHEMA.md`,本 coach 不重定義。
- `mistake-notes.md`:**熱檔但開場不讀**。Mistake Registry 每張卡的正解、判準句、L6 顧問版、歷史重測紀錄、下次抽考題,節標題 = registry 行的 `date | topic`。step A 抽考到哪張卡,才讀哪一節。
- `term-registry.md`:domain registry(英文術語卡:EN term / 發音 / 英文定義 / 中文點破),沿用 PROGRESS-SCHEMA section 7 的 registry 欄位(interval、next-review-date、status)。抽考雙向,見 `language.md`。
- `story-bank.md`:既有 behavioral 素材；固定挖故事已退役，沿用學員外部流程，不排 Weekly Review 保底或欠帳。學員要求 behavioral mock 時才取相關真實故事，區分團隊成果與個人判斷。
- `session-log.md`:**熱檔,只留最近幾堂 + 學員背景/教法備忘/教練執行紀律/chunk maps**。session 1-19 封存在 `archive/session-log-s01-s19.md`。
- `archive/`:冷檔,開課時不讀;Weekly Review trend tracking、Phase Gate 三振診斷、或要查某堂歷史時才讀。
  - `progress-narrative-2026-09-07.md`:2026-09-07 以前 progress.md 的 Phase status / Mastery /
    Scorecard history / Mistake Registry 敘事原文(逐字,未刪字)。要判 mastery 升降級、
    查某場 scorecard 的逐項評註、或查某張卡的完整歷史時才拉對應段。
  - `breakpoint-history.md`:2026-08-19 以前 progress.md 的 Current Session breakpoint 疊層原文(s16-s26,該區段當時已長成 263 行日誌,違反 schema §3)。
  - `session-log-s01-s19.md`:早期 session 敘事。
  - `pre-migration/`:standalone 時期的原始狀態檔,verbatim 保存,不再更新。

**寫入紀律**:`progress.md` 的 Current Session breakpoint 只留最新一堂(當前狀態 + 下一堂 resume,PROGRESS-SCHEMA §3),敘事寫 `session-log.md`,長效教練紀律寫 `session-log.md`「教練執行紀律」,不要在 breakpoint 疊舊堂。

**寫入紀律(Mastery / Scorecard,2026-09-07 加)**:`Mastery` 一個 topic 就是**一行 level + last-updated**(PROGRESS-SCHEMA §5),`Scorecard history` 一場就是**一行六欄**(§6)。降級理由、未升級的原因、冷測歷史、逐項維度評註一律寫 `session-log.md` 對應堂或 `archive/progress-narrative-*.md`,**不要在 Mastery 行的括號裡寫整段敘事**。由來:progress.md 2026-09-07 量到 27,373 字元,Mastery(5,937)+ Scorecard(4,976)+ Registry(7,762)佔全檔 68%,三節全部違反 schema 欄位定義。這是同一個病第三次發作(2026-08-19 在 breakpoint 區、2026-09-02 在 registry 區)。

**讀取紀律(2026-09-07 加)**:開場**不要整份讀 `progress.md`**。依 GOVERNANCE 的 context loading contract,先 `grep -n '^## '` 抓節標題,只讀 Meta + Current Session breakpoint;要選複習題才讀 Spaced-repetition queue 的到期列;要教某 topic 才讀該列 Mastery;Scorecard history 只在 step G / Weekly Review / Progress Report 讀。違反這條的代價實測:2026-09-07 開場整份讀完,光 repo 檔案就載入約 128 KB。

**寫入紀律(Mistake Registry,2026-09-02 加)**:registry 一張卡就是**一行八欄**(PROGRESS-SCHEMA §7),queue 一行五欄(§8)。正解、判準句、L6 版、重測歷史、下次抽考題一律寫 `mistake-notes.md` 對應節,**不要在 registry 行底下疊子項、不要在 queue 行尾疊括號**。這條的由來:progress.md 曾長到 84 KB / 40.8k tokens(36 條 registry 疊出 92 條子項),開場一次全讀但一堂只抽 2 到 3 張卡。同一個病 2026-08-19 已在 breakpoint 區發生過一次。
- `environment.md`:機器層事實(kubeconfig contexts 與安全清單、port 慣例、工具狀態、bastion 同步步驟)。
- `curriculum-plan.md`:戰略層規劃(advisory,見 `curriculum.md`)。
- `clusters/`:per-phase kind 設定檔;`notes/`:工作草稿;`labs/`:lab 暫存(gitignored)。

## Portfolio Directory

Artifacts that clear the quality bar ship to:

`../../portfolio/k8s/`（相對於 coach 的 `SKILL.md`）

Recruiter-facing 展示區,與 workspace 分開。結構:`notes/`(既有學習筆記 + 踩坑)、`manifests/`(P1-P2b 手寫物件)、`observability/`(P4 主秀)、`terraform-eks/`(P2b-P5 EKS IaC)、`gitops/`(P5 主秀)。新 flagship 證據依 governance promotion gate 晉升至 `portfolio/platform-eks/`；同步仍需授權。

### Quality Bar(雙向反陷阱)

展示型 artifact 必須通過 governance 的可重現、客觀驗證、trade-off 與限制門檻；未達門檻的留 workspace。**別擅自重組學員目錄或搬檔**。每堂結尾先更新學習狀態；commit/push 僅在學員授權時執行。

## Capstone: shop platform(貫穿 P2a-P6 的持續演進平台)

s12 起的 shop-api / shop-web 不是丟棄式 lab,是一路長到 P6 的平台;每個 phase 在同一個平台上長一層,終點是 recruiter 可看的 production-like 平台 + 一條完整敘事:「我從零長出一個平台,每一層都能講到 kernel」。唯一硬要求是「同一個平台一路長」,不重開爐灶(細節 FLEX,見 curriculum-plan §4.1)。

`portfolio/k8s/` 保留為 domain 素材庫。通過 `engine/GOVERNANCE.md` promotion gate 的
整合成果才晉升到 `portfolio/platform-eks/`;不為了路徑一致而搬動歷史檔案。本 coach
主要替 L6 matrix 產生 troubleshooting、technical depth、reliability 證據。

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
