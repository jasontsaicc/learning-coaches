# Cross-Coach Root Patterns

本檔是既有 Mistake Registry 的治理 overlay，不取代或刪除任何原始紀錄。
截至 2026-08-21，canonical unresolved evidence 共 74 筆：K8s 30、SD 39、CA 5、
LeetCode 0。LeetCode 的 answer-debt 仍由其 retention/progress 檔管理，待形成 canonical
mistake 時才納入此數字。

## 七個 root patterns

| ID | Pattern | 判準 |
|---|---|---|
| RP1 | Layer and ownership | 先分辨 layer、control/data path、state owner 與執行者 |
| RP2 | Causal-chain assembly | 把零件組成 trigger → actor → state change → mechanism → evidence |
| RP3 | Criterion before conclusion | 先說判準與證據，再給結論；不能只猜 service/tool 名稱 |
| RP4 | Evidence before action | 先保留現場、縮小假設，再 restart／修改／重建 |
| RP5 | Cold transfer | 當堂答對不算 mastery；需相隔七天、無提示、換皮再現 |
| RP6 | Structured communication | 能以 context → constraint → decision → trade-off → risk 組裝輸出 |
| RP7 | Senior judgment | 主動涵蓋 SLO、成本、安全、blast radius、rollout/rollback 與組織影響 |

## Classification overlay

以下以 `workspace / topic` 指向原始 evidence。分類是多對一治理，不改動 progress.md
內原有的 `root-cause-tag`。一筆 evidence 只指定一個 primary pattern，避免重複計數。

### K8s（30）

- RP1（14）：YAML validation、probe 職責、ImagePullBackOff、dry-run 兩層 + Service port、L4 vs L7、跨 node 走路由表不是 iptables、kube-proxy 不在 Pod 啟動路徑上、default-deny 後的分層、veth 誤記跨 node、iptables=一棟樓、分層判準、誰把 limit 寫進 cgroup、PV↔PVC 1:1、container 可寫層。
- RP2（5）：規則/狀態/資料三分類、NetworkPolicy 靜默無效、emptyDir 綁 Pod、Pod 不會重啟、NAPI/CNI 類整鏈以 K8s 的 CNI 基本合約列代表。
- RP3（4）：叢集 DNS 排障、只給結論不給判準、兩張獨立名單、LVM 三層 + 擴容四步。
- RP4（1）：restart 排在採證前面。
- RP5（5）：NetworkPolicy 出廠全通、Ingress YAML schema、PID 1 signal 保護、持久性看掛在哪、EKS 儲存拓撲。
- RP6（1）：判準給完當場套用不上。
- RP7（0）：尚未形成獨立的 canonical mistake；由能力矩陣追蹤缺證據。

### System Design（39）

- RP1（4）：LB 狀態留在 server vs 搬出、MQ 邏輯歸屬 vs 部署單元、兩個 Redis 用途、API breaking vs non-breaking。
- RP2（7）：OAuth deny-list/TTL 組裝、Step 1 流程、拆小問題起手式、API mechanism、Session Revocation 組裝、工具選擇流程、capacity 場景轉算式。
- RP3（6）：trade-off 反面、循環論證、LB happy-path-only、DB selection、開放題 trade-off、先估量級再選工具。
- RP4（0）：目前沒有 canonical incident-action evidence。
- RP5（7）：deregistration delay、bulkhead、SSE vs push、LB 演算法名稱、LB trivia、OAuth 名稱、Observability 術語留存。
- RP6（8）：質疑題目正當性、跳題、棄權三筆、capacity freeze 兩筆、英文 retrieval、壓力下啟動能量。
- RP7（7）：P99 判讀、安全係數機制、Notification priority、operational 收尾兩筆、multi-region 傷害模型、設計收尾的 operational 機制。

### Cloud Architect（5）

- RP1（3）：refused vs timeout、subnet↔route-table binding、NAT gateway placement。
- RP2（1）：NAPI 收包整鏈。
- RP3（1）：Terragrunt rationale（工具名稱存在但機制／判準未交付）。
- RP4–RP7（0）：尚無 canonical mistake；不代表能力已通過，只代表未有此格式的失敗證據。

總計檢查：K8s 30 + SD 39 + CA 5 = 74。

## Active WIP（2026-08-21）

每條學習線最多三個 active patterns。`active` 決定近期出題優先級，不會改寫原始
Mistake Registry 的 unresolved 狀態。

| Track | Active（最多 3） | Backlog |
|---|---|---|
| K8s / platform | RP1、RP3、RP4 | RP2、RP5、RP6、RP7 |
| System Design | RP3、RP6、RP7 | RP1、RP2、RP4、RP5 |
| Cloud Architect | RP1、RP2、RP6 | RP3、RP4、RP5、RP7 |
| LeetCode / Ops coding | RP5、RP6 | RP1、RP2、RP3、RP4、RP7 |

## Review and resolution protocol

1. 每週最多測三個 root patterns；不逐筆掃完所有 evidence。
2. 新失敗若屬既有 pattern，只追加 evidence，不另創治理 pattern。
3. 同一 pattern 必須相隔至少七天、連續兩次無提示通過，其中一次是換 domain／換皮情境。
4. RP6 的第二次通過必須用英文；RP4 必須在 incident 中真的先採證，口頭背順序不算。
5. Pattern 通過後移出 active，但原始 mistake 仍按 engine schema 個別 resolve；overlay 不能代替 domain gate。
6. 若 active pattern 三個已滿，新 pattern 只能進 backlog；要提升前必須先移出一個現有 active。

## Next tests

- K8s RP1：陌生 EKS 網路症狀，先標 layer/owner 再選第一個指令。
- K8s RP3：回答必須包含「判斷、證據、排除項、下一步」。
- K8s RP4：限時 incident，第一次行動不得修改狀態。
- SD RP3/RP7：設計選擇主動補 trade-off、SLO、cost、rollback。
- SD/CA RP6：一場隔離式英文 mock，不提供 model answer 或句型提示。
