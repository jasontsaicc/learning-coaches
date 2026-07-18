# Description-Triggering Eval: cloud-architect-coach

## 目的

驗證 `SKILL.md` frontmatter 的 `description` 欄位是否能正確觸發 cloud-architect-coach skill:
"Should Trigger" 的 prompt 應選中 cloud-architect-coach;"Should NOT Trigger" 的不應選中。

## 參考 description(來自 SKILL.md)

```
AWS ProServe Cloud Architect interview sprint coach (Feynman-based, 4-week plan, Traditional Chinese teaching with English mocks). Use PROACTIVELY when the user mentions the AWS Delivery Consultant / Cloud Architect / Professional Services interview, cloud migration methodology (7R, MAP, landing zone), AWS hybrid networking for interview prep (TGW, Direct Connect, hybrid DNS), Well-Architected case practice, consultant case mocks, or EC2/Linux interview question drills (linux-interview-bank). Also trigger on 上雲, 遷移案例, ProServe 面試, 雲端架構師面試.
```

## Should Trigger(應觸發 cloud-architect-coach)

1. 「幫我準備 AWS ProServe Cloud Architect 的面試」
2. 「練一個 migration case:客戶要把 200 台 VM 搬上 AWS」
3. 「考我 linux interview bank」
4. 「7R 是什麼?幫我複習遷移策略」
5. 「mock 一場 hybrid networking 的架構面試」

## Should NOT Trigger(不應觸發)

1. 「幫我修這個 k8s Pod CrashLoopBackOff」→ k8s-coach
2. 「教我 consistent hashing」→ sd-coach
3. 「幫公司規劃真實的上雲專案」→ 真實工程任務,非面試練習
4. 「想練 DevOps 英文口說」→ fsi-devops-english
5. 「寫一個 Terraform module 建 VPC」→ 執行任務,非學習
