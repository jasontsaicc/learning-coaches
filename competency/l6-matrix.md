# Senior/L6 Evidence Matrix

這張表是所有 coach 共用的 readiness projection，不取代各 domain 的 progress、
scorecard 或 Examiner ledger。它只引用已存在的證據；沒有隔離評量的能力不得因為
「上過課」而升級。

## 評分尺度

| 分數 | 可接受的證據 |
|---|---|
| 0 | 沒有證據，或只有教材／筆記 |
| 1 | 在明顯提示、範例或逐步鷹架下完成 |
| 2 | 在單一熟悉情境中無提示完成 |
| 3 | 能遷移到陌生情境，主動說明 constraint、trade-off 與 failure mode |
| 4 | 能處理模糊性與跨團隊影響，包含 rollout、rollback、量化結果與長期機制 |

`confidence` 衡量證據品質，不是能力高低：`low` 表示主要來自教學 session，
`medium` 表示有冷測或限時練習，`high` 必須有 Examiner 或等價的隔離評量。

## Current baseline（2026-08-21）

| Competency | Required evidence | Current evidence | Score | Confidence | Next evidence |
|---|---|---|---:|---|---|
| Troubleshooting | 45 分鐘陌生 incident，先採證再干預 | K8s s27–s28 已完成故障採證鏈，restart-vs-採證首次過 | 2 | medium | 限時陌生 incident，coach 不提示 |
| Architecture judgment | 有明確限制的 system/platform design review | SD 已有多題設計與 trade-off 記錄，但 P3 尚在進行 | 2 | medium | 45 分鐘 platform design critique |
| Reliability | SLI/SLO、error budget、alert、runbook 與演練 | 有 observability 筆記；K8s P4 尚未開始 | 1 | low | 為 shop platform 定義並實測一組 SLO/alert |
| Delivery and migration | rollout、rollback、blast radius 與 cutover evidence | K8s rollout lab 與 migration 課綱存在，完整 migration artifact 尚無 | 1 | low | platform-eks staged rollout + rollback drill |
| Security | threat model、identity boundary、policy-as-code evidence | NetworkPolicy lab 進行中；IRSA/policy gate 尚未完成 | 1 | low | threat model + IRSA + 一條會擋錯的 policy |
| Cost and capacity | 有單位的 capacity model、成本估算與可靠性取捨 | SD capacity 正在冷測；尚無 portfolio cost model | 1 | low | platform monthly estimate + load-test decision |
| Technical depth | 無提示 causal chain，能連到 observable evidence | K8s 多個底層 lab 已完成，但 assembly 類錯誤仍活躍 | 2 | medium | 陌生跨層情境的 Examiner 口試 |
| Leadership and influence | 真實 STAR：跨團隊、衝突、量化影響、制度化 | story-bank 素材存在但尚未形成驗收證據 | 1 | low | 一題英文 behavioral mock + thread-pull |
| English communication | 45–60 分鐘英文 mock，追問下仍能維持結構 | 各 coach 有 ramp，CA 尚無 scorecard | 1 | low | isolated English architecture mock |
| Coding and automation | 限時獨立實作、測試、複雜度與操作價值 | LC 有 green harness；多題仍有 answer-debt | 1 | low | Ops coding 陌生題限時完成 |

## Evidence update rules

1. 只在新的 scorecard、Examiner verdict、冷測、可執行 artifact 或真實工作證據出現時更新。
2. 當堂教完後答對只能記 acquisition，不能單獨提高到 2 分。
3. 分數升到 3 前，至少要有一個換皮或跨 domain 情境；升到 4 前必須有組織影響證據。
4. 每兩週 review 一次；一次只選最低分且最接近目標面試輪的 1–2 項補證據。
5. Domain mastery 與本表矛盾時，以較低者為準，直到 Examiner 或隔離評量解除差異。

## Current priority

本輪只追三項：Troubleshooting、Technical depth、English communication。其餘保留在
readiness backlog，透過 `portfolio/platform-eks/` 的後續里程碑逐步產生證據，不另開課。
