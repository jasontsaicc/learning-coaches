# 學習進度卡 (斷點續傳)
<!-- 每次 session 開始前更新這裡,讓 Claude 快速掌握你的狀況,避免重複解釋背景 -->

## 基本資訊

| 欄位 | 內容 |
|------|------|
| 目前 phase | P0 心智模型 |
| 目前主題 | P0 心智模型 gate ✅ 口頭全流程過;待 D 段 kind lab + portfolio artifact |
| 上次 session 日期 | 2026-06-17 |
| session 累計次數 (session_count) | 1 |
| 上次 Weekly Review (last_weekly_review) | 0 |

## 診斷結果 (New Student Warm-Up)

程度: 中 (有地圖形狀,缺演員名字)。pacing = P0 剛好,不加速。

- 強: 已有 reconcile 直覺 (原話「比對現有環境進行更新」);知道 rolling update 替換 Pod。
- 洞 1: 用「下指令」框架 = 還停在 imperative 思維 (k8s 是 declarative)。
- 洞 2: 各步驟「誰做的」全省略 (API Server / etcd / controller / scheduler / kubelet 都沒提到)。
- 洞 3: 漏掉 Pod 怎麼被排到某台 node (scheduler 指派 + kubelet 啟動)。

## 未完成 lab

- [ ] (尚未開始 D 段 lab)

## 下一步

> 下次繼續: P0 chunk 1-5 全過 ✅,口頭畢業 gate 過 ✅。下一步 = D 段 kind lab(親眼看 apply→Running:lab-cluster.sh up p0 → apply → kubectl get events / describe 觀察五棒)+ 初始化 k8s-portfolio repo,把 apply→Running 流程圖當第一個 artifact commit。完成後 P0 才算完整畢業(每 phase 必出 artifact 鐵律)。
> 待補精準度:用詞「指令→願望/desired state」、收尾補「loop 閉合」。etcd Raft 深入 park 到 P5/foundations。

## 補充筆記

- 學員背景: DevOps 工程師,hands-on 有 (kubectl apply / 看 logs),底層理論弱;coding 初學。
- 教法備忘: 多用生活 analogy、用學員原話回扣、一次一個 chunk、語言要白。
- chunk map (P0): [1] declarative+reconcile → [2] API Server+etcd → [3] controller 怎麼 reconcile → [4] scheduler 指派 node → [5] kubelet 啟動容器。全部 ✅。
- session 1 scorecard (P0-P1): 底層原理 ✅ / 內部機制 ✅ / 自己的話 ✅。改進=用詞精準度。
- symptom→棒次地圖已教: Pending=scheduler / ContainerCreating=kubelet 網路volume / ImagePullBackOff=runtime拉image / CrashLoopBackOff=容器或probe。
