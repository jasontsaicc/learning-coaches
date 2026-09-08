# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 35
- last_weekly_review: 34(WR9 於 s34 壓縮版跑完,三主題 blind recall 全過;下次 WR 於 s41)
- last_session_date: 2026-09-08
- warm_up_classification: mid
- target_role: 泛用大廠 senior DevOps/SRE。2026-08-21 確認無緊急面試,採 production depth + senior interview 雙軌;核心主題固定比較地端 K8s / 傳統 EKS / 高度託管 EKS(curriculum-plan §11)

## Current Session breakpoint

P2b C-4 RBAC, step D, chunk 3 ✅ 收尾(s35:`get` vs `list` 陷阱親手撞到 + `--list` 三分判準換皮獨立答對),下一步 chunk 4 最小權限設計方法論(爆炸半徑),再補 C-4 的 F/G 與到期冷測;s34/s35 完整交班見 session-log.md。

<!-- schema §3 = 恰好一行。敘事與次要待辦寫 session-log.md,長效教練紀律寫 session-log.md
     「教練執行紀律」,不要在這裡疊舊堂。s32 及更早斷點原文見 session-log.md 對應堂,
     s16-s26 疊層原文見 archive/breakpoint-history.md。 -->

## Phase status

- P0 心智模型: gate-passed(2026-06-22,legacy pre-Examiner)
- P1 核心物件 + 容器底層: gate-passed(2026-06-25,legacy pre-Examiner)
- P2a 網路深水區: in-progress(chunk 1 ✅ / chunk 2 ✅ / chunk 3 NetworkPolicy 剩 lab Step 5+6+gate+F/G / chunk 4 零件 4-1~4-4 ✅,4-5 盲講式已於 2026-08-11 退役改情境排障題)
- P2b 儲存 + 權限: in-progress(C-1 ✅ s26,欠 `cg-demo` memory.max 讀數 / C-2 ✅ s29,欠 `reclaimPolicy: Delete` teardown 實證 / C-3 ✅ s31-32,step G 2/4 未過 / C-4 chunk 1-3 ✅ s33/s35,chunk 4 未開始,C-4 的 F/G 未跑)
- P3 調度 + 高並發 + 排障: not-started
- P4 可觀測性工程: not-started
- P5 平台工程 / GitOps: not-started
- P6 面試衝刺: not-started

weak-topic flags(2026-08-03 啟用,P2a 帶 flag 前進、gate 未考,學員決定):
- 七站封包全旅程(4-5):盲講式退役,改以情境排障題驗收(curriculum-plan §10.2)
- chunk 3 NetworkPolicy 收尾:lab Step 5 兩條 policy + Step 6 驗收矩陣未做
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
- L4 vs L7 判準: low-med (s18)
- NetworkPolicy(白名單 + default-deny 翻轉 + 第四個引擎): low-med (s23)
- conntrack 精度(table full 新舊連線): med (s18)
- DNS 排障第一刀(先用 FQDN 二分): med (s13)
- P2a CNI 封包全鏈 data plane(veth/路由表/MASQUERADE/conntrack): low-med (s23)
- 分層判準「關掉 API Server 還在不在」: med (s25)
- P2b C-1 三階梯壽命(可寫層 / emptyDir / PVC): med-high (s26)
- P2b C-1 可寫層 / overlayfs: med (s24)
- P2b C-1 PV/PVC 解耦: med (s25)
- PID 1 signal 保護: med (s26)
- EKS 儲存拓撲(EBS AZ-scoped / nodeAffinity / volumeBindingMode): med (s26)
- P2b C-3 StatefulSet identity(ordinal / per-replica PVC / per-Pod DNS): med-high (s32)
- P2b C-4 RBAC 四象限: low(scaffolded) (s33)
- P2b C-4 RBAC 兩地基性質(純 allow / SA 是 Pod 身分): low(scaffolded) (s33)
- kubectl debug / ephemeral container: low (2026-09-01,ad hoc 非主線,未經 gate)

## Scorecard history

<!-- schema §6 = date | context | score | top-improvement | best-moment | certifier。
     每場的完整維度符號與逐項評註逐字保存在 archive/progress-narrative-2026-09-07.md
     的 Scorecard history 節;Phase Gate 三振診斷或 trend tracking 時才拉。 -->

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

- 2026-06-18 | YAML validation | `matchLabels` 打成 `metaLabels` | 不讀 strict decoding error;驗證在 API Server | unresolved | 7 | 2026-06-30 | 2
- 2026-06-22 | probe 職責 | 把 readiness 的「準備好接流量」塞給 liveness | 兩種 probe 失敗後動作不同(重啟 vs 切流量) | unresolved | 7 | 2026-07-10 | 1
- 2026-06-23 | ImagePullBackOff | image 打成 `ngimx:1.25`,apply 過卻卡住 | 驗證有邊界:repo 存不存在要 kubelet 拉了才知 | unresolved | 7 | 2026-07-03 | 1
- 2026-06-27 | ClusterIP/kube-proxy/DNAT 全鏈(謎題B) | 「封包先去 ClusterIP 拿 IP」+ 手/名單混淆 | ClusterIP 不是地方;改寫在出發地本機 kernel | resolved | 14 | 2026-07-13 | 0
- 2026-06-28 | 叢集 DNS 排障 | nslookup NXDOMAIN 差點誤判 CoreDNS 壞 | 排障第一刀「先用 FQDN 二分」沒成肌肉 | unresolved | 3 | 2026-07-10 | 3
- 2026-07-03 | dry-run 兩層 + Service port | `--dry-run=client` 綠燈騙人;port/targetPort 靜默不通 | strict decoding 在 API Server 不在 client | unresolved | 3 | 2026-07-17 | 3
- 2026-07-14 | 規則/狀態/資料 三分類(W2 家族 pattern 卡,M2 追蹤用) | conntrack 初分類答「規則」;etcd 未自答 | 規則/狀態/資料判準沒成反射 | unresolved | 3 | 2026-07-22 | 1
- 2026-07-06 | L4 vs L7 | 記成場景標籤(叢集內=L4、外部=L7) | 本質是轉發決定要讀到哪層資訊 | unresolved | 3 | 2026-07-22 | 3
- 2026-07-17 | NetworkPolicy 出廠全通 | 預測「陌生 Pod 連不到 db」,實測連得到 | 出廠全通;namespace 不做網路隔離 | unresolved | 3 | 2026-07-23 | 1
- 2026-07-23 | 跨 node 走路由表不是 iptables(層級混淆家族) | 問跨 node 第一個指令答 iptables,縮小重問答 resolv.conf | 改寫層(NAT)與轉送層(routing)混淆 | unresolved | 7 | 2026-09-10 | 0
- 2026-07-23 | kube-proxy 不在 Pod 啟動路徑上 | 把 kube-proxy 列為 kubelet 建 Pod 三件事之一 | 控制路徑 vs 資料路徑混淆 | unresolved | 3 | 2026-08-07 | 1
- 2026-07-23 | 只給結論不給判準(pattern 卡,升級追蹤) | 同堂三次只給結論不 show work;2026-09-08 續犯(「因為是 get」=複述觀察非判準) | 輸出習慣不是能力;面試官無法區分會與猜對 | unresolved | 3 | 2026-09-11 | 6
- 2026-07-17 | default-deny 後的分層(DNS 層 vs 連線層) | 只答「連線不到」,不分辨死在 DNS 層還是連線層 | 層級混淆;兩步都被鎖時不問哪步先發生 | unresolved | 3 | 2026-07-26 | 1
- 2026-07-28 | veth 誤記「跨 node 連線」 | 答「veth 是跨 node 的網卡連線」 | veth 只管 Pod netns 到 root netns 那段 | unresolved | 7 | 2026-08-10 | 1
- 2026-07-28 | iptables=一棟樓(nat 表/filter 表) | 幻影站 4 + 誘答「DNAT 做完才進 iptables」 | 把 iptables 當一站,不知 DNAT 就在 nat 表裡 | unresolved | 3 | 2026-07-31 | 0
- 2026-07-20 | CNI 基本合約 vs 選配 | 合約三件事兩輪講不出,把 NetworkPolicy 混進合約本體 | 新教內容首輪未固化 | unresolved | 3 | 2026-07-23 | 0
- 2026-07-19 | 兩張獨立名單(3-2 坑二) | 「只開 backend ingress,frontend curl 通嗎」答「可以吧」 | 規則剛教完沒跑兩關檢查程序,憑感覺猜 | unresolved | 3 | 2026-07-22 | 0
- 2026-07-19 | NetworkPolicy 靜默無效(四引擎第四行) | Transfer 只給零件不組裝整條鏈 | 先跳結論等追問才補深度 + 隱性會 | unresolved | 3 | 2026-07-22 | 0
- 2026-07-07 | Ingress YAML schema | `backend.service` 寫成字串 + `pathType: prefix` 小寫 | service 是 object 型別;enum 大小寫敏感 | unresolved | 3 | 2026-07-10 | 1
- 2026-07-07 | Ingress 404 排障 | 差點改沒壞的規則;真兇是半死的 port-forward | 規則層全綠時兇手在你測試經過的那層 | parked(2026-07-16 ROI 篩:Q1 半 yes,但「port-forward 半死」是 lab 夾具產物、prod 不長這樣;同一判準已三種問法重問三次=題目壞掉。判準留檔備查,不再抽) | - | - | 3
- 2026-07-09 | no-Host→404 的 why | 結果預測對,講不出 curl 自動填 Host | 會用會預測不等於會講 why(隱性會) | resolved(2026-07-16 ROI 篩:Q1=no,curl 填 header 是 tool trivia,面試不考;學員答「沒帶 domain → Ingress 對應不上」= 機制正確,教練題目壞掉不是學員沒懂。結案) | - | - | 1
- 2026-08-04 | 分層判準:關掉 API Server 還在不在(工具卡,層級混淆家族的解藥) | s25 冷測 4/5,cgroup memory limit 誤放右欄 | 同名詞的兩個分身(宣告 vs 執行體)沒分開 | unresolved | 3 | 2026-08-08 | 1
- 2026-08-05 | 誰把 limit 寫進 cgroup、什麼時候寫 | 答「scheduler 嗎」 | 控制面與 node 上元件職責混淆 | unresolved | 3 | 2026-08-08 | 0
- 2026-09-04 | 判準跑錯軸:RBAC 題答成 NetworkPolicy | 跨 ns RoleBinding 題結論對,理由給 NetworkPolicy | 物件存在範圍 vs 網路隔離兩軸混用 | unresolved | 3 | 2026-09-07 | 0
- 2026-09-03 | RWO 的 Once 數的是 node 不是 Pod | 共用 PVC 誘答答「RWO 應該是 POD」 | 把 volume 掛載限制記在 Pod 層,實際在 node 層 | unresolved | 3 | 2026-09-06 | 0
- 2026-08-05 | LVM 三層 + 擴容四步(學員課後自己要求復習,foundational pull) | Q1/Q2 結論皆對但兩題都只給結論 | 判準句慣性省略;LVM 的 PV 與 k8s 的 PV 同名不同物 | unresolved | 3 | 2026-08-08 | 0
- 2026-08-05 | PV ↔ PVC 是 1:1 獨佔 | 自曝「我以為是 PV 1:多」 | 「一份儲存給多人用」的直覺貼錯層 | unresolved | 3 | 2026-08-08 | 0
- 2026-08-04 | container 可寫層在硬碟不在 memory(overlayfs 三層) | 「process 死掉檔案去哪」答「存在 memory」 | 把 ephemeral 誤等於 in-memory | unresolved | 3 | 2026-08-07 | 0
- 2026-08-04 | emptyDir 綁 Pod 不綁 container | 「emptyDir 撐不撐得過 kill 1」答「不在了」 | 三層階梯中間一階沒有實體錨點 | unresolved | 3 | 2026-08-07 | 0
- 2026-08-06 | 排障:restart 排在採證前面(MTTR / 治標 vs 治本第三次同形狀) | 三台 node NotReady,三選一選 C 直接 restart | 「先試試」不是診斷;restart 清掉症狀也清掉證據 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | PID 1 的 signal 保護(kernel 層,新知識卡) | 未答錯,實驗意外撞出,全程教練驅動未經抽考 | 需抽考驗留存 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | Pod 不會「重啟」,只會被丟掉重建 | 答「pod 會重啟 or 調節 編排」,講不出誰在什麼條件動手 | 把 Pod 當會重啟的長壽物件而非可拋棄單位 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | 持久性看「掛在哪」不看名字(兩個分身判準第四次換皮) | 未答錯,`/proc/mounts` 撞出 emptyDir 在真磁碟、PVC 在 tmpfs | `PersistentVolume` 這名字沒有保證力 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | EKS 儲存拓撲:EBS AZ-scoped / nodeAffinity / volumeBindingMode(**學員主動提問引出**,ProServe 高權重) | 未答錯;Transfer 過但屬當堂鷹架下複述 | 需冷測驗留存 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-20 | 判準給完當場套用不上(pattern 卡,教學法層級) | 同堂兩次,判準給完 30 秒內套用不上 | 判準被當成聽過的一句話,不是拿來用的工具 | unresolved | 3 | 2026-08-23 | 0
- 2026-08-28 | StatefulSet 每個 replica 一份獨立資料(不是共用一份) | 3 開到 5 問幾份資料,答「still is 3 data」 | 把「每人一份儲存」誤讀成「大家共用一份」 | unresolved | 3 | 2026-09-04 | 0
- 2026-08-28 | 排障兩步:先鎖 fault domain 再查內部(MTTR 核心卡) | 同堂兩次先跳單一成員內部狀態 | 沒先問「這條路徑上有幾個東西」 | unresolved | 3 | 2026-08-31 | 0
- 2026-09-01 | 建 Pod 的權限 vs Pod 裡程式呼叫 API 的權限(誰用誰的身分) | 答「不會,因為根本沒有到建立 pod」 | controller 建 Pod 與 Pod 呼叫 API 誤用同一身分 | unresolved | 3 | 2026-09-04 | 0
- 2026-09-08 | RBAC 動詞看有無物件名字(get vs list vs watch) | Role 只給 get,預測 `kubectl get pods` 會成功,實測 403 cannot list | 把 kubectl 指令名字當成 RBAC 動詞 | unresolved | 3 | 2026-09-11 | 0
- 2026-09-08 | 成功訊息不保證做到你以為的事(pattern 卡,ops 判準,同堂三次) | `-n ALL` 查了不存在的 ns、`--as=$SA` 空變數沒假扮、`patched (no change)` | 不先驗證指令是否真的生效就改結論 | unresolved | 3 | 2026-09-11 | 0
- 2026-09-08 | `auth can-i --list` 不加 `--as` 問的是自己 | chunk 3 驗收給裸指令,無 `--as` 無 `-n`(同堂第二次) | 排障要問壞掉的身分,預設問的是自己 | unresolved | 3 | 2026-09-11 | 0
- 2026-09-08 | `--list` 三分判準(只剩噪音 / 缺 resource / 缺動詞) | 首答把原本 403 訊息當成 `--list` 輸出,且用「會 403」當判準(兩種都 403) | 兩個不同指令的輸出混為一談 | unresolved | 3 | 2026-09-11 | 0

## Spaced-repetition queue

<!-- PROGRESS-SCHEMA §8 = item-ref | type | interval | next-review-date | status。
     檢視序:過期優先、interval 小者優先;step A 每堂 ~2 題上限。
     每張卡的重測歷史與下次抽考題在 mistake-notes.md;term 卡到期日在 term-registry.md。 -->

- mistake:YAML-validation | mistake | 3 | 2026-08-08 | active
- mistake:ImagePullBackOff | mistake | 3 | 2026-08-09 | active
- mistake:dry-run-兩層 | mistake | 3 | 2026-08-09 | active
- mistake:三分類-家族卡 | mistake | 3 | 2026-07-22 | active
- mistake:L4-vs-L7 | mistake | 3 | 2026-07-22 | active
- mistake:NetworkPolicy-出廠全通 | mistake | 3 | 2026-07-23 | active
- mistake:default-deny-分層(DNS vs 連線) | mistake | 3 | 2026-08-06 | active
- mistake:跨-node-走路由表 | mistake | 3 | 2026-08-13 | active
- mistake:blackhole路由與本機/32 | mistake | 3 | 2026-08-13 | active
- mistake:跨-node-走路由表-舊記錄 | mistake | - | 2026-08-09 | retired(s27 已執行,由上面的新列接手)
- mistake:分層判準-關掉APIServer還在不在 | mistake | 3 | 2026-08-08 | active
- mistake:誰把limit寫進cgroup(kubelet不是scheduler) | mistake | 3 | 2026-08-08 | active
- mistake:LVM三層+擴容四步 | mistake | 3 | 2026-08-08 | active
- mistake:PV↔PVC是1:1獨佔 | mistake | 3 | 2026-08-08 | active
- mistake:可寫層在硬碟不在memory(overlayfs) | mistake | 7 | 2026-08-13 | active
- mistake:emptyDir-綁Pod不綁container | mistake | 7 | 2026-08-13 | active
- mistake:restart排在採證前面(MTTR) | mistake | 7 | 2026-08-27 | active
- mistake:scheduler當萬用嫌犯 | mistake | 3 | 2026-08-13 | active
- mistake:產生者vs消費者(排障找誰) | mistake | 3 | 2026-08-13 | active
- mistake:對照組判準(同層有好有壞) | mistake | 3 | 2026-08-23 | active
- mistake:active≠還在幹活(健康檢查三層) | mistake | 3 | 2026-08-27 | active
- mistake:DeadlineExceeded語義 | mistake | 7 | 2026-08-27 | active
- mistake:PID1-signal保護 | mistake | 3 | 2026-08-09 | active
- mistake:Pod不會重啟只會被丟掉重建 | mistake | 3 | 2026-08-09 | active
- mistake:持久性看掛在哪不看名字(tmpfs) | mistake | 3 | 2026-08-09 | active
- mistake:EKS儲存拓撲(EBS AZ/nodeAffinity/volumeBindingMode) | mistake | 3 | 2026-08-09 | active
- mistake:veth-誤記跨node連線 | mistake | 7 | 2026-08-10 | active
- mistake:iptables-一棟樓 | mistake | 3 | 2026-08-06 | active
- mistake:kube-proxy-不在-Pod-啟動路徑 | mistake | 3 | 2026-08-07 | active
- mistake:判準給完當場套用不上(pattern) | mistake | 3 | 2026-08-31 | active
- mistake:StatefulSet每個replica一份獨立資料 | mistake | 7 | 2026-09-10 | active
- mistake:RWO數的是node不是Pod | mistake | 3 | 2026-09-06 | active
- mistake:判準跑錯軸(RBAC答成NetworkPolicy) | mistake | 3 | 2026-09-07 | active
- mistake:先鎖fault-domain再查內部(MTTR) | mistake | 7 | 2026-09-10 | active
- mistake:只給結論不給判準(pattern) | mistake | 3 | 2026-09-04 | active
- mistake:建Pod的權限vs呼叫API的權限(誰用誰的身分) | mistake | 3 | 2026-09-04 | active
- mistake:NetworkPolicy-靜默無效 | mistake | 3 | 2026-07-31 | active
- mistake:CNI-合約三件事 | mistake | 3 | 2026-07-23 | active
- mistake:兩張獨立名單 | mistake | 3 | 2026-08-06 | active
- term:conntrack | term | 7 | 2026-07-26 | active
- mistake:probe-職責 | mistake | 3 | 2026-08-27 | active
- mistake:DNS-排障第一刀 | mistake | 3 | 2026-07-10 | active
- mistake:Ingress-YAML-schema | mistake | 3 | 2026-07-10 | active
- term:(07-10 到期各卡) | term | - | 2026-07-10 | active(見 term-registry.md)
- mistake:ClusterIP-全鏈(謎題B) | mistake | 14 | 2026-07-13 | active(resolved,考精度)
- mistake:RBAC動詞-get-vs-list | mistake | 3 | 2026-09-11 | active
- mistake:成功訊息不保證生效(pattern) | mistake | 3 | 2026-09-11 | active
- mistake:--list-要加---as | mistake | 3 | 2026-09-11 | active
- mistake:--list-三分判準 | mistake | 3 | 2026-09-11 | active

## Curiosity branch

- etcd Raft 深入 | 2026-06 | 面試不直接考實作、P5 etcd 運維會用到 | 想追 Raft 共識怎麼撐起 etcd,park 到 P5(見 curriculum P5 焦點)
- `kubectl patch` 為何印 `(no change)` 卻實際有改 | 2026-09-08 | 面試不考、不改善排障品質(Three Questions Q1/Q2 皆 no) | s35 現場撞到,已用 describe 驗出實際生效;kubectl client 端訊息機制,想追再追

## Domain registries

- `term-registry.md`(同目錄):英文術語卡,18 張。欄位:EN term / 發音 / 英文定義 / 中文點破 / 學習日 / 下次抽考日。抽考雙向(見 language hook),3→7→14 節奏同引擎。
- `story-bank.md`(同目錄):behavioral 素材庫(非間隔複習型)。機會式一行入帳 + 每次 Weekly Review 保底挖 10 分鐘一則(M4);P6 提煉 STAR。
- `mistake-notes.md`(同目錄):**Mistake Registry 每張卡的內文**(正解 / 判準句 / L6 顧問版 / 歷史重測 / 下次抽考題),節標題 = registry 行的 `date | topic`。**開場不讀**;step A 抽考到哪張卡才拉哪一節。新的重測紀錄追加到那裡,不要寫回 registry 行底下。
- 其他 coach 讀取檔:`session-log.md`(歷史 session 敘事)、`environment.md`(機器/context 安全事實)、`curriculum-plan.md`(戰略層,advisory)。

## Examiner ledger

(空 — P0/P1 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。第一筆 Examiner 紀錄將是 P2a gate,預計 3-5 堂後。)
