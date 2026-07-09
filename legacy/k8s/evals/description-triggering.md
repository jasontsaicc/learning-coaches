# Description-Triggering Eval: k8s-coach

## 目的

驗證 `SKILL.md` frontmatter 的 `description` 欄位是否能正確觸發 k8s-coach skill。

具體來說: 當 skill router 看到以下 "Should Trigger" 的 prompt 時，應該選中 k8s-coach；看到 "Should NOT Trigger" 的 prompt 時，不應選中 k8s-coach。

## 參考 description（來自 SKILL.md 第 3 行）

```
Kubernetes/SRE deep-learning coach (hands-on, first-principles, Feynman-method, Traditional Chinese).
Use PROACTIVELY when the user wants to learn or practice k8s/kubernetes, prepare for big-tech DevOps/SRE
interviews, debug or troubleshoot k8s (故障排除/troubleshooting), or study EKS, networking
(CNI/Service/Ingress), scheduling, autoscaling, 高並發/high-concurrency, observability/可觀測性, or
CKA/CKAD. Drills cluster internals via local kind and EKS.
```

## Should Trigger (應觸發 k8s-coach)

| # | Prompt | 觸發理由 |
|---|--------|---------|
| 1 | 我想開始學 k8s | 明確說要「學 k8s」，符合 learn or practice k8s |
| 2 | 幫我準備 SRE 面試 | 符合 prepare for big-tech DevOps/SRE interviews |
| 3 | EKS 上高並發怎麼扛 | 符合 EKS + 高並發/high-concurrency |
| 4 | 我的 Pod 一直 CrashLoopBackOff 怎麼查 | 符合 debug or troubleshoot k8s / 故障排除 |
| 5 | 想搞懂 kube-proxy 底層 | kube-proxy 是 k8s networking 底層元件，符合 first-principles |
| 6 | 練一下 CKA 故障題 | 符合 CKA/CKAD 準備 |
| 7 | CNI 是什麼，flannel 和 calico 有什麼差別 | 符合 networking (CNI/Service/Ingress) |
| 8 | 我想知道 HPA 和 VPA 怎麼運作 | 符合 autoscaling 主題 |

## Should NOT Trigger (不應觸發 k8s-coach)

| # | Prompt | 說明 | 預期走向 |
|---|--------|------|---------|
| 1 | 幫我寫一題 leetcode，找二叉樹最大深度 | LeetCode 演算法題，與 k8s 無關 | leetcode-coach |
| 2 | 純粹做一次 terraform import，把 S3 bucket 導入 state | 這是 IaC 操作執行，不是 k8s 學習或 k8s 故障排查 | 直接操作，非 coaching |
| 3 | 幫我 review 這個 PR，看 Go code 有沒有問題 | Code review 任務，非 k8s 學習或 troubleshooting | code-review |
| 4 | 解釋一下 system design 的 CAP theorem | CAP theorem 是分散式系統基礎理論，非 k8s 特定，也不是 SRE 面試準備 | sd-coach |

## How to Run

### 手動驗證步驟

對每條 prompt，在已載入 k8s-coach skill 的 Claude Code session 中輸入 prompt：

1. **Should Trigger 測試**: 輸入各 prompt，觀察 Claude 是否自動呼叫 `Skill(k8s-coach)`。
2. **Should NOT Trigger 測試**: 輸入各 prompt，確認 Claude 不呼叫 `Skill(k8s-coach)`，而是走其他路徑。

### Pass Criteria

- Should Trigger (8 條): **全部** route 到 k8s-coach (8/8)
- Should NOT Trigger (4 條): **全部** 不 route 到 k8s-coach (4/4)

任何一條 Should Trigger 沒觸發，或任何一條 Should NOT Trigger 誤觸發，視為 FAIL，需要修改 description。

### 常見失敗原因

- description 太寬泛: Should NOT Trigger 的 prompt 被誤抓 (false positive)
- description 太窄: Should Trigger 的 prompt 沒被抓到 (false negative)
- 關鍵詞缺失: 如 description 沒有 "CKA" 則 prompt #6 可能 miss
