# Phase Gates

The engine enforces the 3-attempt cap and the failure protocol; this file defines what
"pass" means per phase. Gates are scope-based, not timed: 判定靠「能不能講完 / 能不能在
限定回合內排查到位」,不靠分鐘數。P2a 與 P3 結束各加一次 30min 迷你 mock(見
`curriculum.md`),結果回饋進 gate 判定。

## P0 Gate - 心智模型

**Pass condition:** 能完整白板講出 apply→Running 的 control flow,不看資料。

**Examiner inputs:** the student's verbatim spoken/written walkthrough (no lab artifact for P0).

Specifically, the student must:
1. 講出完整鏈路:client → API server → etcd → controller → scheduler → kubelet → container runtime,不漏中間棒次(scheduler 是歷史盲點,特別驗)。
2. 解釋 declarative + reconcile loop:desired vs actual,誰在收斂、怎麼收斂。
3. 說出鏈路上任一元件掛掉的後果(抽一個問)。

## P1 Gate - 核心物件 + 容器底層

**Pass condition:** 混合故障在限定回合內定位根因(排障方向正確、第一刀選得對)。

**Examiner inputs:** the triage transcript (student's commands and reasoning per turn), the `kubectl` outputs (fenced), and the student's verbatim root-cause explanation.

Specifically, the student must:
1. 對一個注入的故障(probe 錯配 / OOMKilled / rollout 卡住類),第一個排查指令方向正確。
2. 在限定回合內從現象走到根因,講出「為什麼這個現象指向這個根因」。
3. 用 QoS / cgroup / namespace 層級解釋容器底層行為(e.g. 為什麼是這個 Pod 被 OOM kill)。

## P2a Gate - 網路深水區

**Pass condition:** 白板講完封包全鏈路 + 答出「conntrack 滿了怎麼查」。

**Examiner inputs:** the student's verbatim packet-path walkthrough (client → Ingress → Service → Pod, both directions where relevant), the conntrack answer, and any supporting lab output (fenced).

Specifically, the student must:
1. 講完封包路徑:外部 client → Ingress controller → Service(kube-proxy/iptables/conntrack)→ Pod,含 DNAT 與回程。
2. 分清「規則(iptables)/ 狀態(conntrack)/ 資料(Endpoints)」三者角色,不混淆。
3. 答出 conntrack table 滿了的症狀、查法(`conntrack -S`、dmesg)與處置方向。
4. 講出 NetworkPolicy 的 default-deny 語義與 CNI 為什麼要支援才有效。

## P2b Gate - 儲存 + 權限

**Pass condition:** 設計最小權限 RBAC + 解釋 IRSA 怎麼把 IAM 接到 ServiceAccount。

**Examiner inputs:** the student's RBAC manifests (fenced), the verbatim IRSA chain explanation, and the PV/PVC lab output (fenced).

Specifically, the student must:
1. 為一個給定情境寫出最小權限 Role/RoleBinding(不濫用 cluster-admin),並講出為什麼每條 rule 是必要的。
2. 解釋 IRSA 全鏈:ServiceAccount annotation → OIDC provider → STS AssumeRoleWithWebIdentity → Pod 拿到的臨時憑證。
3. 解釋 PV/PVC/StorageClass 的綁定流程與 CSI 在哪一層介入。

## P3 Gate - 調度 + 高並發 + 排障

**Pass condition:** 能設計扛流量尖峰的部署,並在大型 chaos drill 中限回合定位。

**Examiner inputs:** the student's deployment design (manifests or written spec, fenced), the capacity reasoning, and the large-drill triage transcript.

Specifically, the student must:
1. 設計含 HPA、PDB、resource requests/limits、topology spread 的部署,講出每個選擇的 why。
2. 講出 scheduler 的過濾/打分流程與 affinity/taint 的適用場景。
3. 在大型故障演練(節點掛 / 流量暴增 / OOM 雪崩擇一)中,限定回合內定位並提出止血 + 根治兩層處置。

## P4 Gate - 可觀測性工程

**Pass condition:** 能為服務定義 SLO 並實際追完一條 trace。

**Examiner inputs:** the student's SLO definition (written, fenced), the PromQL used, and the trace walkthrough (screenshot description or span list).

Specifically, the student must:
1. 為 shop platform 的 api 服務挑 SLI、定 SLO,並解釋 error budget 的行動含義。
2. 寫出對應的 PromQL 並解釋每一段在算什麼。
3. 用 OTel/Jaeger 追一條跨服務 trace,指出延遲花在哪個 span、為什麼。

## P5 Gate - 平台工程 / GitOps

**Pass condition:** 一個 commit 自動安全上線(GitOps 閉環),並能講出每一環的失敗模式。

**Examiner inputs:** the student's Helm chart / ArgoCD app definitions (fenced), the commit-to-deploy walkthrough, and the verbatim answers to failure-mode questions.

Specifically, the student must:
1. 展示 commit → ArgoCD sync → 上線的完整閉環,講出每一步誰在做事。
2. 答出 sync 失敗 / drift / rollback 的處置(ArgoCD 的 reconcile 跟 P0 的 reconcile loop 是同一個心智模型,要能自己點出來)。
3. 解釋 EKS prod-grade terraform 的關鍵設計(node group、IRSA、upgrade 策略)。

## P6 Gate - 面試衝刺

**Pass condition:** 通過 scenario mock(英文模式):原理 why-chain、故障 scenario、k8s×SD 交集、behavioral 各至少一題,達 60% threshold。

**Examiner inputs:** the full mock transcript (English), the scenario triage transcript, and the STAR-format behavioral answer.

Specifically, the student must:
1. 原理題:被 why-chain 連續追問 3 層不斷鏈。
2. 故障 scenario:限回合定位 + 講出止血/根治,全程英文。
3. Behavioral:一則 story-bank 提煉的 STAR 故事,含可量化結果。
4. Portfolio 完整(見 `portfolio.md`)才可進 gate。
