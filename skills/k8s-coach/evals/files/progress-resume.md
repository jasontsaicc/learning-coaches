# 學習進度卡 (斷點續傳)

## 基本資訊

| 欄位 | 內容 |
|------|------|
| 目前 phase | P1 核心物件 + 容器底層 |
| 目前主題 | Pod liveness / readiness probe |
| 上次 session 日期 | 2026-06-15 |
| session 累計次數 (session_count) | 4 |
| 上次 Weekly Review (last_weekly_review) | 0 |

## 未完成 lab

- [ ] probe-lab:設了 livenessProbe 後 Pod 一直被重啟,卡在「為什麼 readiness 一直 fail」的 step,還沒找到根因
- [ ] 還沒跑 E 段 chaos drill(故意把 probe 路徑設錯)

## 下一步

> 下次繼續:接續 probe chunk 3 — 釐清 liveness vs readiness 的語意差異(失敗各自會怎樣),再跑 readiness 失敗的 chaos drill

## 補充筆記

- liveness 失敗 → kubelet 重啟 container;readiness 失敗 → 從 Service endpoints 移除,但不重啟
- 還沒搞懂 initialDelaySeconds / periodSeconds 怎麼影響「重啟風暴」
- Term Registry 有 3 張卡今天到期要抽考:probe / endpoint / kubelet
