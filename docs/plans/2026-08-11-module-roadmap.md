# Module Roadmap 2026 H2(2026-08-11 拍板)

新模組一律不開新 coach、不開新週配額;材料掛既有 coach,檔期接力使用。
新 track 三問(缺一不開):對應哪個 loop round / 卡片級蓋不蓋得住 / 檔期從哪個 track 扣。

| 模組 | 場次 | 檔期 | 起跑 | 材料落點 |
|------|------|------|------|---------|
| Terraform senior fast path | 6 | 借 k8s 時段(P3 之後) | ~2026-10 | `skills/terraform-coach/references/curriculum.md`(已定稿) |
| Linux troubleshooting | 6-8 | 接 terraform 同時段 | ~2026-12 | `skills/cloud-architect-coach/references/linux-troubleshooting-scenarios.md` |
| Ops coding | 4(穿插) | 每月一次 LC 驗收場換題 | 2026-09 起 | `skills/leetcode-coach/references/ops-coding-bank.md` |
| AI infra capstone | lab 時段 | 取代 k8s P5 部分 lab | ~2027 Q1(第一輪走完後) | `portfolio/ai-infra/` |

## Linux troubleshooting(6-8 場)

- 對應 round:Google SRE 的 Linux internals / 現場排障輪(目前唯一無 track 覆蓋的 round;ca gap-scan 實測 1 pass / 10 shaky / 5 hole)。
- 形狀:壞機器情境動手排障(sad-servers 型),ca 30 題題庫當抽考池,不重教理論。
- 情境骨架已開檔(見材料落點),內容待補。
- 完成判準:8 個情境限時獨立修復 + Examiner 一場口試。

## Ops coding(4 場)

- 對應 round:Google SRE coding 輪的實務半場(log 解析、API 自動化、併發),與 LC 算法是不同肌肉。
- 形狀:限時實作,Python,LC 的 pytest harness 驗收。
- 題目骨架已開檔(見材料落點),內容待補。

## AI infra capstone(2027 Q1)

- 目的:career plan 槓鈴冒險端(AI infra 差異化),不對應現有 loop。
- 內容:self-hosted LLM inference on EKS/kind + autoscaling + observability + cost dashboard。
- 一魚三吃:k8s P4/P5 lab 素材、portfolio 主秀、AI-infra 履歷線。
- 落點 `portfolio/ai-infra/`(README 已建,結構待補)。

## 明確不開(重複投資)

security 專課(k8s §10.5 卡片級已蓋)、networking 專課(ca 題庫 + k8s P2a 已付清)、
DB 專課(sd + 卡片級蓋得住)、CKA(2027 投遞前再評)。
