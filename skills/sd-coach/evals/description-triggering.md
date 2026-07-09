# Description-Triggering Eval: sd-coach

## 目的

驗證 `SKILL.md` frontmatter 的 `description` 欄位是否能正確觸發 sd-coach skill:
"Should Trigger" 的 prompt 應選中 sd-coach;"Should NOT Trigger" 的不應選中。

## 參考 description(來自 SKILL.md)

```
System Design interview coaching skill using Feynman + Simon learning methods. Guides students
through a structured curriculum covering core building blocks, distributed systems, and classic
SD problems with hands-on PoCs and mock interviews. Use PROACTIVELY when the user mentions system
design, SD interview prep, mock interviews, design exercises, or wants to learn/practice any
system design topic (caching, load balancing, databases, message queues, etc.). Also trigger when
the user asks to review SD concepts, do whiteboard practice, or prepare for tech interviews at
FAANG/big tech companies.
```

## Should Trigger(應觸發 sd-coach)

1. 「我想繼續 system design 的進度」
2. "Give me a mock SD interview question about caching."
3. 「教我 consistent hashing」(學習語境)
4. "How should I prepare for the Google system design round?"
5. 「今天來練 URL shortener 的設計」
6. "Let's do whiteboard practice for distributed systems."
7. 「教 Yuki 我剛學的東西」

## Should NOT Trigger(不應觸發)

1. 「幫我修這個 k8s Pod CrashLoopBackOff」→ k8s-coach
2. "Solve this LeetCode two-sum problem." → leetcode-coach(未來)
3. 「幫公司的 API 系統寫一份真的架構設計文件」→ 一般工程任務,非教學
4. "Set up a load balancer on AWS for my app."(執行任務,非學習)
5. 「想練 DevOps 英文口說」→ fsi-devops-english
