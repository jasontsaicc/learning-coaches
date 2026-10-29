# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 52
- last_weekly_review: 49(WR10 於 s49 課尾壓縮版:NetworkPolicy DNS supported / RBAC watch 結論對判準錯 / Secret 分層冷測過)
- last_session_date: 2026-10-29
- warm_up_classification: mid
- target_role: 雙目標 NVIDIA Pre-Production Engineer + AWS ProServe DC Cloud Architect,兼顧台廠資深 SRE(2026-09-30,curriculum-plan §12);投遞最快 2027-01

## Current Session breakpoint

無(s52 正常收工)。下一堂:P3 C-3b KEDA lab(curriculum-plan §12.6);P2a/P2b Phase Gate 仍待考,學員挑時機;registry 16 張(s52 triage 到 15 後,學員選擇多留 5xx 卡);每堂無 G(§12.4)。

<!-- schema §3 = 恰好一行。敘事與次要待辦寫 session-log.md,長效教練紀律寫 session-log.md
     「教練執行紀律」,不要在這裡疊舊堂。s32 及更早斷點原文見 session-log.md 對應堂,
     s16-s26 疊層原文見 archive/breakpoint-history.md。 -->

## Phase status

- P0 心智模型: gate-passed(2026-06-22,legacy pre-Examiner)
- P1 核心物件 + 容器底層: gate-passed(2026-06-25,legacy pre-Examiner)
- P2a 網路深水區: in-progress(chunk 1 ✅ / chunk 2 ✅ / chunk 3 NetworkPolicy ✅ s48(lab Step 1-6 s46 + AND/OR 實測 + F/G s48) / chunk 4 零件 4-1~4-4 ✅,4-5 盲講式已於 2026-08-11 退役改情境排障題)
- P2b 儲存 + 權限: in-progress(C-1 ✅ s26,欠 `cg-demo` memory.max 讀數 / C-2 ✅ s29,欠 `reclaimPolicy: Delete` teardown 實證 / C-3 ✅ s31-32,step G 2/4 未過 / C-4 chunk 1-4 ✅ s33/s35/s36,4b 僅 supported,C-4 F/G 併入 s37 的 C-5 F/G;C-5 ✅ s37(chunk 3 supported、kind JWT 教練代跑);C-6 chunk 1 supported / 2 ✅ s38 / 3 ✅ supported s39,F ✅ s40,G 2/4 未過 s40)
- P3 調度 + 高並發 + 排障: in-progress(curriculum-plan §12.2 開場:kubeadm 3 台叢集 s45 建成,cp + w1/w2 + Calico;P2b 殘債壓課尾;C-1 scheduler ✅ s49;C-2 調度約束 ✅ supported s50,無 lab)
- P4 可觀測性工程: not-started
- P5 平台工程 / GitOps: not-started
- P6 面試衝刺: not-started

weak-topic flags(2026-08-03 啟用,P2a 帶 flag 前進、gate 未考,學員決定):
- 七站封包全旅程(4-5):盲講式退役,改以情境排障題驗收(curriculum-plan §10.2)
- chunk 3 NetworkPolicy 收尾:Step 5/6 ✅ s46;AND/OR 實測 ✅ s48(supported,OR 後果講不具體)
- 判準句 pattern(只給結論):跨七堂未愈,每堂續盯

## Mastery

<!-- schema §5 = level + last-updated 兩欄。每個 topic 的完整判準句、降級理由、冷測歷史、
     未升級的原因,全部逐字保存在 archive/progress-narrative-2026-09-07.md 的 Mastery 節;
     開課不讀,要教到那個 topic 或要判升降級時才拉那一段。 -->

- P0 apply→Running control flow: high (s10)
- P1 container = namespace+cgroup: high (s6)
- P1 probe(liveness vs readiness): high (s6)
- P1 Deployment/rollout: high (s6)
- P1 resource/QoS/OOM: high (s10)
- P2a Service/kube-proxy/DNAT/conntrack/CoreDNS 全鏈: high (s10)
- P2a Ingress(規則 vs controller、L7 純字串比對): med (s14)
- P2a L4 vs L7 判準: low-med (s18)
- P2a NetworkPolicy(白名單 + default-deny 翻轉 + 第四個引擎): med (s48)
- P2a conntrack 精度(table full 新舊連線): med (s18)
- P2a DNS 排障第一刀(先用 FQDN 二分): med (s13)
- P2a CNI 封包全鏈 data plane(veth/路由表/MASQUERADE/conntrack): low-med (s23)
- P2b 分層判準「關掉 API Server 還在不在」: med (s25)
- P2b C-1 三階梯壽命(可寫層 / emptyDir / PVC): med-high (s26)
- P2b C-1 可寫層 / overlayfs: med (s24)
- P2b C-1 PV/PVC 解耦: med (s25)
- P2b PID 1 signal 保護: med (s26)
- P2b EKS 儲存拓撲(EBS AZ-scoped / nodeAffinity / volumeBindingMode): med (s26)
- P2b C-3 StatefulSet identity(ordinal / per-replica PVC / per-Pod DNS): med-high (s32)
- P2b C-4 RBAC 四象限: low(scaffolded) (s33)
- P2b C-4 RBAC 兩地基性質(純 allow / SA 是 Pod 身分): low(scaffolded) (s33)
- P2b C-5 instance profile vs IRSA 爆炸半徑(粒度 = SA): med (s37)
- P2b C-5 IRSA 鏈(trust policy 比 sub vs permission policy): low(scaffolded) (s37)
- P2b C-6 Secret 分層(etcd 明文 / encryption at rest 擋備份 / RBAC 擋 API 讀者): med (s49)
- P2b C-6 env vs volume 輪替(啟動快照 vs kubelet 同步): med (s38)
- P2b C-6 PSS 兩個檢查點(admission 看 YAML / kubelet 看 image user): low(scaffolded) (s40)
- P3 kubeadm 叢集建置(init 產物 / static pod 由 kubelet 管 / join TLS bootstrap): low(supported) (s45)
- P3 無 CNI 因果鏈(Ready=False → not-ready taint → coredns Pending): low(supported) (s45)
- P3 bootstrap 元件不依賴自己(static pod / calico-node hostNetwork): low(supported) (s45)
- P3 C-1 scheduler(邊界 / FailedScheduling 判準 / preemption): low-med (s49)
- P3 C-2 調度約束(taint/affinity 專用節點、antiAffinity vs topologySpread、rollout 卡死): low(supported) (s50)
- P3 C-3 HPA(按比例擴 / 分母 requests / 盲區 / scaleDown 300s 窗口): low-med (s51)
- P3 C-4 VPA(updateMode / limit 等比例 / HPA 分母衝突 / 生產用 Off): low(supported) (s52)
- P1 kubectl debug / ephemeral container: low (2026-09-01,ad hoc 非主線,未經 gate)

## Scorecard history

<!-- schema §6 = date | context | score | top-improvement | best-moment | certifier。
     每場的完整維度符號與逐項評註逐字保存在 archive/progress-narrative-2026-09-07.md
     的 Scorecard history 節;Phase Gate 三振診斷或 trend tracking 時才拉。 -->

- 2026-10-16 | step G (s48, tier 2, 跨 ns podSelector 不通) | 3.5/4 | 被問「問題在哪」要講出具體多放行誰(哪個 ns 的哪些 Pod),不停在通則 | 根因一句到位:「from.podSelector 沒搭 namespaceSelector 只找 policy 同 ns 的 Pod」 | coach
- 2026-09-29 | step G (s40, tier 2, C-6 PSS Deployment 被擋) | 2/4 | 「先查 rs」的因為要講到機制:Pod 由 RS controller 建,被擋時錯誤只留在送請求的 RS event | 第一刀直接選 `kubectl get rs` → describe events | coach
- 2026-09-18 | step G (s37, tier 2, MTTR 未測故分母 3) | 2/3 | 機制那格要講出 JWT → STS 比 trust policy 的 sub → 臨時憑證,不能停在「SA 取得 assume 權限」 | F 段 3 副本題自己拿 IRSA(同一 role)對照舊做法(看在哪台 node) | coach
- 2026-08-28 | step G (s32, tier 2) | 2/4 | 排障題先強迫答「我這一發是第 1 步還是第 2 步」再給指令 | MTTR 第一題自帶完整判準句型,無提示正樣本第 6 次 | coach
- 2026-08-24 | step G (s30, tier 2) | 3/4 | 先用 direct-to-target 對照 bypass 嫌疑層,別第一刀就 describe pod | 自己修正成「繞過後正常只鎖定被繞過的整段路徑,不能直接定罪 Proxy」 | coach
- 2026-08-20 | 冷測三題 + F 段折算 (s28, tier 2) | 1/4 | 每給一個判準,當場接一題換皮應用題,答對才算給完 | 排障順序題把 `reboot` 排最後,restart-vs-採證這張卡首次做對 | coach
- 2026-08-10 | s27(F/G 未跑,學員疲勞收工) | 不計分 | — | — | coach(信度低,整堂教練帶著走,不宜當 tier 2 分數)
- 2026-08-06 | step G (s26, tier 2, 正式版一題) | 3/4 | F 段對新手開口就是三個名詞零機制,要先講機制再講名詞 | 誘答「不刪 pod 就永遠安全吧」沒點頭,拿三分鐘前發現的 tmpfs 反駁 | coach
- 2026-08-05 | WR9 主題1 + C-1 lab 折算 (s25, tier 2) | 2/4 | 排障「選指令」那步連三堂沒方向,改用三選一候選指令建立肌肉 | PVC Pending 預測自帶「因為」且主動追問「為什麼要這樣設計」 | coach
- 2026-08-04 | A 段冷測 + C-1 lab 折算 (s24, tier 2) | 1/4 | why-first 預測連跳三次;s25 起不給預測不給下一發指令 | 「Calico 上 apply 完的 NetworkPolicy,關掉 API Server 還擋得住嗎」無提示自答「可以,因為直接修改 kernel」 | coach
- 2026-08-03 | 盲測 #3 + lab 折算 (s23, tier 2) | 1/4 | 盲測格式紀律(口訣 + 七行)要當成硬規格 | 誘答咬住「NetworkPolicy 實際改 iptables filter table」+ tunl0 不是 veth | coach
- 2026-07-28 | step G 折算 (s22, tier 2, 盲測 #2 + F 段) | 1/4 | 「誰做的」欄要長在骨架裡,每站一個負責人 | F 段自組靜默無效鏈 + 站 7 無提示判準句 | coach
- 2026-07-23 | step G (s21, tier 2, 顧問情境模擬首場) | 0/4 | 判準句缺席:三次只給結論,第六堂同條 | 回程 conntrack 主動講出來,那是 gate 歷史漏點清單上的站 | coach(信度高,純冷測無鷹架)
- 2026-07-19 | weekly review (s18, tier 2) | 3/4 | 判準句慣性省略、只給結論(第五堂同條) | conntrack「去程改 Destination / 回程改 Source」自產 | coach
- 2026-07-17 | A 段 + chunk3 gate (s16, tier 2) | 1/4 | 判準/機制講不出:L4-L7 兩度結論對理由錯 | conntrack 去程/回程兩欄位自產(給框架不給答案) | coach(信度低,教練犯三錯,低分含教練污染)
- 2026-07-09 | step G (s14, tier 2) | 1/4 | 隱性會沒逼成顯性:結果預測準、why 講不出 | `/apiv2` catch-all 那刀自己串對沒鷹架 | coach
- 2026-06-29 | weekly review (s10, tier 2) | 4/4 | 盲講控制流易漏中間棒次,用五棒默數 | 封包全鏈無鷹架冷測 | coach
- 2026-06-25 | phase gate (P1, legacy) | 3/3 | 先跳結論要追問才補深度(連三堂同條) | 從 exit 0 反推「app 健康、被 probe 殺」 | coach
- 2026-06-24 | step G (s5, tier 1) | 3/3 | 主動吐「治本 vs 治標」別等追問 | 自己推出可壓縮/不可壓縮不對稱 | coach
- 2026-06-23 | step G (s4, tier 1) | 3/3 | 主動吐機制 + 挑經濟值 | 自己抓出「額外 8 → 總數 12」算錯 | coach
- 2026-06-22 | phase gate (P0, legacy) | 3/3 | etcd 只有 API Server 直接碰(口誤待修) | 五棒 + 演員 + scheduler/kubelet 分清 | coach
- 2026-06-18 | step G (s2, tier 1) | 3/3 | 用詞精準度 | 自創恆溫器比喻講 declarative | coach
- 2026-06-17 | step G (s1, tier 1) | 3/3 | 用詞精準度 | 底層原理/機制/自己的話全過 | coach

## Mistake Registry

<!-- 欄位:date | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     PROGRESS-SCHEMA §7 = 單行八欄。正解/判準句/L6 版/歷史重測/下次抽考題寫在 mistake-notes.md,
     依 `date | topic` 對應。開場不讀 mistake-notes.md;step A 抽考到哪張卡才拉哪一節。
     interval 2 = +2 天臨時複習格(口頭型 resolved,過了才進 3/7/14)。
     unresolved-session-count 於 2026-07-10 遷移時依複測紀錄初始化(近似值)。 -->

- 2026-10-29 | 4xx vs 5xx 是誰產生的(面試答不出) | 學員自述面試被問「K8s 遇到 5xx 怎麼辦」答不出、跟 404 混;s52 複習把 5xx 直接猜成 DB 問題 | 先分 4xx(請求不對)/ 5xx(伺服器錯),再看碼是誰產生的:500 = app,502/503/504 = ingress;P2a 404/502/503 階梯留存不足 | unresolved | 3 | 2026-11-01 | 0
- 2026-10-29 | VPA Auto 實際行為(驅逐時間 / 改 Pod 不改 Deployment) | F 追問尖峰會不會被砍答「9 點過 5 分鐘」(混成 HPA scaleDown 300s);「deploy YAML 沒變 = 沒生效?」答不確定,縮成二選一才答對 | Updater 自己決定驅逐時間,差距超出範圍就砍,可能落在尖峰;Admission 寫 Pod 不寫 Deployment,生效看 get pod | unresolved | 3 | 2026-11-01 | 0
- 2026-10-16 | 讀 FailedScheduling 判斷加 node 有沒有用 | `1 taint, 2 Insufficient memory` 答加 node 沒用(被 cp taint 行帶走) | 找 Insufficient = 容量問題;cp taint 行每次都在是背景 | unresolved | 14 | 2026-11-12 | 0
- 2026-10-12 | 下 kubectl 前先確認在跟哪個叢集講話 | bastion 上兩次 `kubectl get nodes` 打到 PROD atlas-aws-billing-prod(本意查 lab),第二次在教練提醒後 | prompt 雖顯示 context 但未看;唯讀無損,換成 delete/drain 即事故。對策:lab kubectl 一律在 cp session 跑 | unresolved | 3 | 2026-10-15 | 0
- 2026-09-30 | node Ready 是誰回報的(kubelet heartbeat 走 6443) | SG 缺 IPIP 預測 nodes NotReady,理由「etcd 和 calico 沒開」;提示後改答「metrics-server」 | Ready = kubelet → apiserver heartbeat,與 etcd(cp 本機)/ CNI 資料面 / metrics-server 無關;P0 symptom→棒次地圖留存不足 。10-12 再現:cp NotReady 答「node 跟 api server 不通」✗(那是 Unknown);直給 CNI 缺 → kubelet 回報 Ready=False → not-ready taint → coredns Pending,describe node 實證 | unresolved | 3 | 2026-10-15 | 2
- 2026-09-29 | 啟動前被擋 vs 啟動後自己死(CreateContainerConfigError vs CrashLoopBackOff) | 原版 nginx + runAsUser 1000,預測 STATUS 答 CreateContainerConfigError(同時自己填 kubelet 放行) | 沒用 STATUS 定位死在哪一棒:kubelet 放行 = 容器已啟動,綁 port 80 失敗 = 程序退出 = CrashLoopBackOff;反證後改對(supported),/root 寫檔換皮帶因為 ✅ | unresolved | 3 | 2026-10-02 | 0
- 2026-09-18 | IRSA trust vs permission policy | 首答「擋在 B policy」;誘答「改 SA annotation 就能讀別人的 S3」同意;F 段又同意「STS 看 policy 有無 s3:GetObject 就放行」 | RP2 驗身分(trust policy 比 JWT sub)與授權(permission policy)混成一步;annotation 只是申請單 | unresolved | 7 | 2026-10-16 | 0
- 2026-06-22 | probe 職責 | 把 readiness 的「準備好接流量」塞給 liveness | 兩種 probe 失敗後動作不同(重啟 vs 切流量) | unresolved | 7 | 2026-07-10 | 1
- 2026-06-27 | ClusterIP/kube-proxy/DNAT 全鏈(謎題B) | 「封包先去 ClusterIP 拿 IP」+ 手/名單混淆 | ClusterIP 不是地方;改寫在出發地本機 kernel | resolved | 14 | 2026-07-13 | 0
- 2026-06-28 | 叢集 DNS 排障 | nslookup NXDOMAIN 差點誤判 CoreDNS 壞 | 排障第一刀「先用 FQDN 二分」沒成肌肉 | unresolved | 3 | 2026-07-10 | 3
- 2026-07-06 | L4 vs L7 | 記成場景標籤(叢集內=L4、外部=L7) | 本質是轉發決定要讀到哪層資訊 | unresolved | 3 | 2026-07-22 | 3
- 2026-07-23 | 只給結論不給判準(pattern 卡,升級追蹤) | 同堂三次只給結論不 show work;2026-09-08 續犯(「因為是 get」=複述觀察非判準);09-25 續犯(「B 因為」後空白) | 輸出習慣不是能力;面試官無法區分會與猜對 | unresolved | 3 | 2026-11-01 | 7
- 2026-07-07 | Ingress 404 排障 | 差點改沒壞的規則;真兇是半死的 port-forward | 規則層全綠時兇手在你測試經過的那層 | parked(2026-07-16 ROI 篩:Q1 半 yes,但「port-forward 半死」是 lab 夾具產物、prod 不長這樣;同一判準已三種問法重問三次=題目壞掉。判準留檔備查,不再抽) | - | - | 3
- 2026-07-09 | no-Host→404 的 why | 結果預測對,講不出 curl 自動填 Host | 會用會預測不等於會講 why(隱性會) | resolved(2026-07-16 ROI 篩:Q1=no,curl 填 header 是 tool trivia,面試不考;學員答「沒帶 domain → Ingress 對應不上」= 機制正確,教練題目壞掉不是學員沒懂。結案) | - | - | 1
- 2026-08-06 | 排障:restart 排在採證前面(MTTR / 治標 vs 治本第三次同形狀) | 三台 node NotReady,三選一選 C 直接 restart | 「先試試」不是診斷;restart 清掉症狀也清掉證據 | unresolved | 3 | 2026-11-01 | 1
- 2026-08-06 | EKS 儲存拓撲:EBS AZ-scoped / nodeAffinity / volumeBindingMode(**學員主動提問引出**,ProServe 高權重) | 未答錯;Transfer 過但屬當堂鷹架下複述 | 需冷測驗留存 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-28 | 排障兩步:先鎖 fault domain 再查內部(MTTR 核心卡) | 同堂兩次先跳單一成員內部狀態 | 沒先問「這條路徑上有幾個東西」 | unresolved | 3 | 2026-08-31 | 0
- 2026-09-08 | RBAC 動詞看有無物件名字(get vs list vs watch) | Role 只給 get,預測 `kubectl get pods` 會成功,實測 403 cannot list | 把 kubectl 指令名字當成 RBAC 動詞 | parked(2026-09-15 ROI 篩:Q1 no,403 訊息本身就寫出 verb `cannot list`,背對照表 ROI 低;學員決定退役,判準留檔備查) | - | - | 0
- 2026-09-08 | `--list` 三分判準(只剩噪音 / 缺 resource / 缺動詞) | 首答把原本 403 訊息當成 `--list` 輸出,且用「會 403」當判準(兩種都 403) | 兩個不同指令的輸出混為一談 | parked(2026-09-15 ROI 篩:Q1 no,面試不考讀 `--list` 輸出;學員決定退役,判準留檔備查) | - | - | 0
- 2026-10-13 | default-deny 先死在 DNS 層 | 答「全部擋住」,提示後答連線層,連錯兩次直給;s48 F 段誘答「egress 只放 orders:5432 就能連」直接同意,Resolving 提示後仍答查 db ingress,二選一後自答補 53 | 沒把 DNS 查詢當成第一個 egress 封包 | unresolved | 3 | 2026-10-19 | 1

- 2026-10-28 | HPA 超標就 +1 顆 | 1 顆 250m/requests 200m/target 50% 預測連答「2 顆」「超過就多建立一 pod」 | HPA 按比例 ceil(current×current/target) 一次跳到需要的顆數(lab 實測 1→3→5) | unresolved | 3 | 2026-10-31 | 0

## Spaced-repetition queue

<!-- PROGRESS-SCHEMA §8 = item-ref | type | interval | next-review-date | status。
     檢視序:過期優先、interval 小者優先;step A 每堂 ~2 題上限。
     每張卡的重測歷史與下次抽考題在 mistake-notes.md;term 卡到期日在 term-registry.md。 -->
- mistake:Insufficient才是容量問題 | mistake | 14 | 2026-11-12 | active

- topic:P2a-chunk3-NetworkPolicy | topic | 3 | 2026-10-19 | active
- mistake:IRSA-trust-vs-permission | mistake | 7 | 2026-10-16 | active
- mistake:L4-vs-L7 | mistake | 3 | 2026-07-22 | active
- mistake:跨-node-走路由表-舊記錄 | mistake | - | 2026-08-09 | retired(s27 已執行,由上面的新列接手)
- mistake:restart排在採證前面(MTTR) | mistake | 3 | 2026-11-01 | active
- mistake:EKS儲存拓撲(EBS AZ/nodeAffinity/volumeBindingMode) | mistake | 3 | 2026-08-09 | active
- mistake:先鎖fault-domain再查內部(MTTR) | mistake | 7 | 2026-09-10 | active
- mistake:只給結論不給判準(pattern) | mistake | 3 | 2026-11-01 | active
- term:conntrack | term | 7 | 2026-07-26 | active
- mistake:probe-職責 | mistake | 3 | 2026-08-27 | active
- mistake:DNS-排障第一刀 | mistake | 3 | 2026-07-10 | active
- term:(07-10 到期各卡) | term | - | 2026-07-10 | active(見 term-registry.md)
- mistake:RBAC動詞-get-vs-list | mistake | - | 2026-09-11 | retired(2026-09-15 ROI 篩)
- mistake:--list-三分判準 | mistake | - | 2026-09-11 | retired(2026-09-15 ROI 篩)
- topic:C-6-Secrets(分層+輪替) | topic | 3 | 2026-09-24 | active
- topic:C-6-PSS(admission 看 YAML / kubelet 看 image user) | topic | 3 | 2026-09-30 | active
- mistake:啟動前被擋vs啟動後自己死 | mistake | 3 | 2026-10-02 | active
- topic:C-4-RBAC-最小權限+等價升權 | topic | 3 | 2026-09-16 | active(4b create pods=借SA 僅 supported,冷測換皮;併入 C-5)
- topic:P3-C2-調度約束 | topic | 3 | 2026-10-23 | active
- topic:P3-C3-HPA | topic | 3 | 2026-10-31 | active
- mistake:HPA超標就+1顆 | mistake | 3 | 2026-10-31 | active
- mistake:下kubectl前先確認context | mistake | 3 | 2026-10-15 | active
- mistake:node-Ready是kubelet回報 | mistake | 3 | 2026-10-15 | active
- mistake:default-deny先死在DNS層 | mistake | 3 | 2026-10-19 | active
- topic:P3-C4-VPA | topic | 3 | 2026-11-01 | active
- mistake:VPA-Auto實際行為 | mistake | 3 | 2026-11-01 | active
- mistake:4xx-vs-5xx誰產生 | mistake | 3 | 2026-11-01 | active

## Curiosity branch

- etcd Raft 深入 | 2026-06 | 面試不直接考實作、P5 etcd 運維會用到 | 想追 Raft 共識怎麼撐起 etcd,park 到 P5(見 curriculum P5 焦點)
- `kubectl patch` 為何印 `(no change)` 卻實際有改 | 2026-09-08 | 面試不考、不改善排障品質(Three Questions Q1/Q2 皆 no) | s35 現場撞到,已用 describe 驗出實際生效;kubectl client 端訊息機制,想追再追
- kubectl 指令 → HTTP 請求 → RBAC verb 對照、audit log 取證細節 | 2026-09-13 | 面試不考逐發請求,排障用 `auth can-i` 即可(Q1/Q2 皆 no,學員 s36 喊太細) | apply=get+create/patch、rollout status=get+list+watch、`-v=6` 可看;EKS 取證走 control plane logging `audit`

## Domain registries

- `term-registry.md`(同目錄):英文術語卡,18 張。欄位:EN term / 發音 / 英文定義 / 中文點破 / 學習日 / 下次抽考日。抽考雙向(見 language hook),3→7→14 節奏同引擎。
- `story-bank.md`(同目錄):behavioral 素材庫(非間隔複習型)。機會式一行入帳 + 每次 Weekly Review 保底挖 10 分鐘一則(M4);P6 提煉 STAR。
- `mistake-notes.md`(同目錄):**Mistake Registry 每張卡的內文**(正解 / 判準句 / L6 顧問版 / 歷史重測 / 下次抽考題),節標題 = registry 行的 `date | topic`。**開場不讀**;step A 抽考到哪張卡才拉哪一節。新的重測紀錄追加到那裡,不要寫回 registry 行底下。
- 其他 coach 讀取檔:`session-log.md`(歷史 session 敘事)、`environment.md`(機器/context 安全事實)、`curriculum-plan.md`(戰略層,advisory)。

## Examiner ledger

(空 — P0/P1 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。第一筆 Examiner 紀錄將是 P2a gate,預計 3-5 堂後。)
