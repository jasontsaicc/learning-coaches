# Portfolio

本目錄的主線是 `platform-eks`。既有 `k8s/`、`sd/` 是學習成果與可重用素材庫，
不刪除、不為了改目錄而搬檔；新產出只有通過客觀驗收後才晉升到主線作品。

## Flagship structure

1. `platform-eks/`：唯一 active flagship。整合 K8s、Terraform、GitOps、security、observability、cost 與 rollout/rollback。
2. `incidents/`：從 platform 故障演練衍生的 evidence package；在第一場演練前不預建空內容。
3. `ai-infra/`：未來作為 platform workload，維持 parked，直到 platform 的基線、SLO 與部署閉環完成。

## Promotion rule

一份產出必須至少包含可重現步驟、客觀測試結果、設計取捨與已知限制，才能從既有
素材庫晉升到 flagship。只有筆記、截圖或當堂跟做結果，不算 portfolio evidence。

Readiness 由 `competency/l6-matrix.md` 投影；學習弱點由
`workspaces/shared/root-patterns.md` 治理。Portfolio 不自行宣告 mastery。
