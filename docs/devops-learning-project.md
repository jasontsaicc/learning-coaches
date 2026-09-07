# Jason 的 DevOps／SRE 與 AWS Delivery Consultant 學習專案

更新：2026-09-07。這是個人規劃與排課參考；實際能力與斷點仍以 domain progress 和新評量為準。
本次只修改課程／skills，不改 `workspaces/`、不重置進度、不代做 lab。

## 目標與可用條件

- **目前主力：K8s＋SD**，持續往 Senior DevOps／SRE 前進；AWS ProServe Delivery Consultant 保留為未來求職目標，不另外新增每週 CA 主課。
- 學員確認 AWS 申請在第一階段被拒，尚未進面試；拒絕原因未知。不能把拒信解讀為技術、英文或年齡不合格，也不能倒推為下述現行 JD 的年資要求所致。
- 長期追求 senior／L6 的判斷與影響力；不把所有公司的 L6 視為同一職級，也不把課堂分數換算成錄取或定級。
- 學員自述 35 歲，TPI 系統工程師約 2 年、ECV DevOps 1 年多；履歷列 TPI 2022-12 至 2025-03、ECV 2025-04 至今。年齡不作能力評分或衝刺期限。
- 無預定面試日期。每週可用時間尚未確認：先以 **6 小時／週、兩週試行** 估算，再按實際可持續負荷調整。
- 履歷已列 Solutions Architect – Professional、DevOps Engineer – Professional、Security – Specialty。先補可展示的交付能力；暫不增加證照主線。

履歷來源：使用者提供的 `../job-applications/aws-proserve-tw/resume.md`（相對 repository root）。
此檔只保存規劃所需的摘要，不複製聯絡資料或客戶識別資訊；不更動外部申請資料。
履歷是自述材料，數字、個人 ownership、證照有效性及成果歸因都尚未在本次獨立驗證。

## 職缺校準：同一個底盤，兩種交付方式

2026-09-07 查到的 [AWS 台灣 Delivery Consultant 職缺，Job 10471890](https://amazon.jobs/en/jobs/10471890/delivery-consultant-cloud-architect-professional-services-taiwan)
要求 hands-on production delivery、AWS、程式語言、IaC、CI/CD，以及中英文溝通；該職缺列出
5+ 年相關經驗與 3+ 年雲端經驗。你已述的 IT 年資仍低於它的 5 年條件，雲端年資需按實際
經歷核對。這是特定 JD 的資格差距，不代表所有 Delivery Consultant 職缺門檻相同，也不能
靠 lab 補成工作年資。投遞前依當時 JD 與 recruiter 確認職級和條件；公開職稱未證實內部 L6。

| 面試方向 | 共用能力 | 額外需要交付的證據 |
|---|---|---|
| AWS Delivery Consultant | Linux/networking、AWS、coding、IaC、delivery、reliability | discovery 問題、migration waves、cutover/rollback、風險溝通、handover、真實客戶協作 |
| Senior DevOps／SRE | 同上 | 陌生 incident、SLI/SLO、error budget、capacity、故障模型、toil reduction、設計辯證 |

[Google 的 SRE 職涯介紹](https://sre.google/careers/)強調可靠性、效率與跨組織合作，可作能力方向，
不能當作特定面試輪次。[Amazon Sr. SDE 準備頁](https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep)
可供 coding／design 練習參考，**不移植它的輪數、LP 比重到 Delivery Consultant**。
實際 interview loop 以目標職缺的 recruiter 說明為準。

## 現況判讀與課程取捨

| 已有材料 | 現在能合理判斷 | 接下來驗什麼 |
|---|---|---|
| 履歷：跨帳號遷移、4 套 EKS、1,500+ AWS resources 的 Terraform/Terragrunt 管理 | 有值得深挖的 production 經歷；不應整套從 provider/resource 入門重教 | ownership、state/import/locking、identity、cutover、失敗時的邊界 |
| 履歷：pipeline 由 6h 至 1h、覆蓋約 70% 專案、權限分層 | 可串成 delivery＋influence 主故事 | 時間的起訖、樣本期間、採用分母、排除其他改善因素、rollout/rollback |
| 履歷：FSI Outposts、AWS SA 協作、presales/PoC | 已有與 ProServe 貼近的客戶場景 | 客戶限制、自己與 SA 的分工、hybrid 故障時證據、handover 與結果 |
| K8s s34：RBAC 動手、故障域換皮初次通過，C-4 未收完 | 動手能學進去，角色／層次與判準仍需冷測 | `get`/`list` 權限故障、最小權限與 RBAC/IAM/NetworkPolicy 邊界 |
| SD s50：Chat message flow 尚有斷點；過往論證與 operational 收尾不穩 | 題材覆蓋已多；不能再把所有缺口都稱為「只有輸出問題」 | 新機制先教；熟悉設計在無提示下給 why、反面代價、capacity、SLO |
| LeetCode 2026-09-04：#206/#21 看懂零件但冷寫 loop 卡住 | green harness 與看解後完成不足以證明獨立 coding | 隔堂 blank-page 實作＋小變形，Ops coding 補錯誤處理與測試 |
| CA：July gap-scan／Linux assembly 記錄、無完整 scorecard | 資料較舊，不能把所有舊錯都當目前弱點，也不能直接視為已修復 | 未來需要時挑與履歷相關的 hybrid/networking 小題重新取證 |

`competency/l6-matrix.md` 基準為 2026-08-21；它的 coding「answer-debt」敘述已落後於
standalone rebuild。保留原始評分，報告時標示過時；下次有獨立證據才更新，不因本次讀履歷升分。

保留：Feynman 推導、圖解、學員自己操作、冷測、陌生情境、獨立 Phase Gate。
調整：以 K8s＋SD 固定時段為主；Terraform 有實作需求才拉進來，CA 只作未來的情境 overlay，相同能力只教一次。
暫緩：新證照、第二個 flagship、已會工具的整章重教、與近期案例無關的 kernel 細節。
LeetCode 沿用 standalone 節奏，不加入 engine 的債務／複習 gate。

## 一個主專案：把既有 shop platform 做成交付案例

沿用 `portfolio/platform-eks/`，以「既有服務需要安全遷移與穩定交付」作教學情境。
這是 **lab 模擬案**；企業規模、預算、RTO/RPO 由案例明列假設，不偽裝成真客戶成果。
EKS 是現有實作載體；ADR 必須能比較 ECS/VM 等選項，說明什麼條件下不應選 Kubernetes。

| 階段 | 內容與課程來源 | 可驗收產出／退出條件 |
|---|---|---|
| A 基線與需求（先做） | K8s 既有素材＋SD scope clarification；M0 | 新環境重現 shop、smoke test；一頁 scope/assumptions、dependencies、成功條件與責任分工 |
| B 安全與可重建交付 | 收 K8s RBAC 斷點，Terraform 針對 state/identity 快路徑；M1/M2 | 最小權限正反測試；可重跑 IaC、drift/plan 解讀、state 失敗情境、威脅邊界 |
| C 可觀測與故障處理 | K8s P3/P4＋SD capacity/SLO；M3/M5 | 一個真正連到使用者結果的 SLI/SLO；load test、actionable alert、runbook、陌生故障採證與恢復 |
| D 交付與遷移 | CI/CD/GitOps＋CA migration；M4，延伸 M5 | staged rollout/rollback 實證；migration wave、資料一致性驗證、cutover go/no-go、backup/restore 與 handover |
| E 獨立 review | CA/SD/K8s；M6 | 英文 architecture review、SRE incident、customer objection；能用證據回應風險與反面代價 |

這是依賴順序，不是五個固定期限；階段可能跨多個兩週週期。先補 prerequisite，再進相關
實作，不為了「做完專案」由教練把 code 全寫完。純 Linux/networking drill 也服務同一案例：
DNS、routing、TCP、TLS、process、disk/memory 問題依觀察進入，不另開百科課。

本機 kind 先驗證原理；只有 AWS integration 的差異才用隔離 lab。課程保留現有 context
安全與 EKS/IaC 人工執行界限。尚無雲端預算，不在本規劃建立資源；實作時先列預估、清除與查空步驟。
不設定虛構的 AWS 價格或承諾現有 kind 配置能證明所有雲端能力。

作品集最終只需要一個能讀懂的入口，以及實際產出的 deployment/verification、ADR、SLO/runbook、
postmortem、migration/handover。文件以英文收斂；scratch 留 domain workspace。
每個 promoted artifact 必須有重現步驟、客觀結果、trade-off、限制，遵守既有 promotion gate。
內容課與作品集共用證據，避免再寫一份同內容筆記。尚未存在的產出維持 planned。

## 用真實工作累積 senior scope

Lab 能證明機制與操作，跨團隊影響要由工作證據支持。在正常工作授權範圍內，挑一項
能延伸既有責任的改善：pipeline template adoption、IaC drift 處理、alert 品質或交付 handover。
先界定問題與 baseline，邀相關使用者 review，小範圍 rollout，再看改善是否持續。
不為學習直接修改客戶 production，也不把團隊成果全歸給自己。

| 履歷素材 | AWS 顧問追問 | SRE／Senior 追問 |
|---|---|---|
| 跨帳號／EKS migration | 客戶為什麼遷移？scope、wave、stakeholder 與驗收怎麼定？ | identity/data/DNS 依賴？哪一步不可逆？怎麼偵測與 rollback？ |
| 1,500+ 資源 IaC | 如何分批導入又保留稽核與交接？ | state ownership、locking、drift、import、blast radius 怎麼處理？ |
| 6h→1h pipeline | 如何取得採用？70% 的分母是什麼？如何處理異議？ | baseline、failure rate、manual toil、部署失敗與 rollback 時間？ |
| Outposts／FSI | 哪些是業務／法遵限制？自己、AWS SA、客戶各負責什麼？ | service link／DNS／網路故障時，誰可採證？失效與復原邊界？ |

先整理上述 4 個真實故事，不新增故事數量 KPI。每個只補：我的角色、限制、備選方案、
我的決策、結果的量測方式、失敗與改善、他人如何採用。既有 behavioral／英文材料仍在
外部流程管理；本 repo 只引用需要的摘要，不重建資料庫。沒有數字就寫未量測，不補造。

## 每週安排：先試兩週

暫定 6 小時，**不是已確認的可用時間**：

| 時段 | 長度 | 內容 |
|---|---:|---|
| Platform A | 75 分 | 一個必要機制＋學員實作，K8s 或 Terraform 當次擇一 |
| Platform B | 75 分 | 同一能力的故障／交付驗證；穿插 Linux/networking |
| SD | 60 分 | 先續既有 Chat breakpoint；已學過的再做 design/incident case，不強制全 mock |
| Coding ×3 | 每次 25 分 | 暫定 2 次 LeetCode＋1 次 Ops coding；依目標 JD 再調比重 |
| 英文／履歷追問 ×2 | 每次 20 分 | 可選的短練習，用本週已熟悉成果；沿用外部英文流程，不另開 CA 課 |
| 整理／雙週檢視 | 35 分 | 一份 evidence 的差異更新；檢視週以 review 取代整理 |

完整版本合計 360 分鐘；可選時段不做就留作休息，不要求補滿。若只有 3–4 小時，保留一個 K8s sitting、SD 與短 coding，其他輪流；
若有 8–10 小時，增加學員實作與陌生測試，不增加平行課程。取消一次時段就順延 breakpoint，
不追回所有日曆欠課。Engine 的 session count／Weekly Review 機制照舊，雙週規劃不重跑同一評量。

**第 1 週**：Platform A 接 K8s C-4 chunk 3 的 `get` vs `list` 故障，再按進度做 chunk 4。
Platform B 先收該單位必要 F/G；有餘裕才做 M0 inventory/smoke。SD 接 s50 Chat message flow，
先弄清 DB 儲存與 message delivery、元件責任及失敗情境；需要的新機制先教，再讓學員說取捨。
Coding 先隔堂驗 #206/#21，Ops 題可用小型 log summarizer（malformed input／測試／complexity）。

**第 2 週**：以第 1 週產出決定繼續 M0 還是 M1；讓相同 RBAC 原理換 namespace／identity 重測。
SD 仍依 Chat breakpoint 前進，完成相關機制後，換成丟訊息／重送／部分故障的 SRE 設計追問，
把 capacity、failure mode 與 observability 用在同一系統，不為週表擅自結案。
CA 目前不重啟。未來可每四場 SD 擇一加 customer discovery／handover 視角，或收到邀約再調整；
這是建議頻率，並非新增必修。真要重啟 CA 時才依 engine Comeback 處理時間間隔，不掃完所有 July 舊題。
第二週結尾用實際負荷和證據校準後續兩週。

## 適合你的教學模式

1. **Learn**：一個完整情境、可理解的圖、一個 worked example。新工具先教用途與結果判準，
   再讓你組 troubleshooting chain；不把「還沒教」判成你的錯。
2. **Practice**：你先預測、自己操作、解讀結果。指令先交代 context/hypothesis/why/decision，
   一次一個動作；coach 不搶鍵盤。逐步撤掉範例，從補半張圖到陌生情境。
3. **Retain/transfer**：隔堂冷寫、相隔至少七天的留存與換情境取證。當堂看解後完成只算 acquisition。
   K8s 保留新內容優先、短複習置尾的個人決定；普通 sitting 不清空全部 unresolved。
4. **Assess**：只有已教過的能力做獨立 mock；先保留你的第一版答案，feedback 後補對另外記。
   需要補教就結束該次 scored attempt，再切 Learn。Phase Gate 保留獨立 Examiner。
5. **Close**：同一單位保留 F（teach-back）與 G（interview），可跨 sitting；喊停先存 breakpoint。
   繁中推理＋英文技術詞，熟悉案例逐步轉英文，不靠術語背誦假裝英文能交付。

一次普通教學回覆只放一個解釋／圖或一個動作／問題；完整範例照給，不固定裁成幾百字而
破壞理解。完整逐字稿、長對照與擴展閱讀按需要提供，不在每輪重複產生。
不使用「這在 Google 一定 no-hire」等沒有公司評分依據的斷言；明確指出本課程哪項證據不足。

## 驗收與投遞準備

每兩週只挑 1–2 個能力缺口。記錄 **題數與提示程度**，不要只寫一個漂亮百分比：

- 獨立完成度：冷題幾題／無提示幾題；若樣本只有 2 題就寫 1/2，不宣稱穩定 50%。
- 口述品質：首答是否有選擇、why、代價，以及題目相關的 operational 收尾。
- 操作能力：有沒有先採證；能否重現、解釋與恢復；測試結果和學員操作分開於 coach 演示。
- 交付品質：artifacts 能否由他人重現；哪些是模擬、哪些有真實工作歸因。
- 負荷：實際小時、是否被複習或長回答擠掉 hands-on；下輪只做一項節奏調整。

投遞前做一次無提示的履歷追問、customer migration case、SRE incident/design，以及目標
JD 所需 coding。可以分天；實際時限按 recruiter 資訊，未知時自訂練習時限並標示。
以現有 rubric 記錄，不宣稱它是 AWS 的 hiring bar；公司資格條件與能力準備分開檢視。
依缺口選要投的職缺與 scope，而不是等所有課全部結束。L6 的跨團隊 ownership、影響與
長期機制要由真實工作案例支持，不能靠單人 lab 或證照直接證明。

## Skills 的 token 改善與驗證

已確認的靜態放大點：`ENGINE.md` 約 33 KB；K8s/SD progress 約 44/32 KB；四個 engine coach
入口要求讀全 hooks，且 engine 再重複要求。K8s 的入口＋engine＋governance＋8 hooks 在修改前
為 **74,641 bytes**；加 progress、curriculum-plan、root-patterns 全檔為 **146,792 bytes**。
這是「整檔讀取路徑」的 byte 基線，不是實際消耗、最低必要量或每次對話的 token 數。

本次改用治理層的 action→context 表：

- 四個 coach 收窄觸發範圍；學習規劃不自動進課程，普通 coding／infra 修改不因關鍵字開課。
- hooks 是索引；上課只載當步教材，lab 才載環境與 lab-manager，評分才載 scorecard，Phase Gate 才載 Examiner。
- progress、plan、教學備忘先看標題，再讀完整相關區段；選複習題前仍檢查相關 queue／unresolved，避免只讀前幾行漏規則。
- engine 仍保留完整教學與安全契約；本次不做高風險的核心規則大幅摘要。已在 context 中且未改的檔案不反覆讀。
- 規劃書僅規劃／readiness review 才讀；不把新文件變成所有 coach 的開場稅。
- LeetCode 已有按需讀取和獨立 loop，保留其流程；不為整齊重構。

驗證包含既有 lint/lab checks、獨立路由情境檢查，以及靜態讀取 bytes 比較。
行為情境：15 分鐘續課、只規劃不開課、一般練習 vs Phase Gate、無日期雙職涯規劃。
lint 驗證結構，不等於證明模型一定遵循指令。若要量化成本，在接下來同類 3–5 場記錄 host
可提供的 input/output/cache token 與 loaded sections；沒有 telemetry 就只報 bytes/files。
不宣稱本次已達某個 token 節省百分比；全域技能注入／宿主行為不在本 repo 修改範圍。

2026-09-07 驗證結果：`./scripts/lint-all.sh` 全通過（包含三組 lab scripts），四個變更
入口通過 skill frontmatter validator，`git diff --check` 通過。一次獨立基線路由評估與一次
修改後情境評估，確認短續課按需載入、規劃不開課、K8s/SD 主線及 Examiner 認證界限；
這是有限的路由檢查，尚未完成真實多場教學成本 A/B。開場規則的靜態比對若只含
入口/engine/governance 與 teaching-elements/portfolio 全檔，修改後約 62 KB；不含實際
課題、安全環境、語言、state 讀取，因此不拿這個數字宣稱整場節省比例。

## 尚待校準

每週可持續投入時間，以及履歷四個主案例中你最能獨立講清楚的一個。這兩點用來調整份量
與第一個 thread-pull；不妨礙先沿現有 K8s 斷點與共用主專案開始。
