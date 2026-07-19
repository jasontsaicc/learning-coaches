# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 18
- last_weekly_review: 18
- last_session_date: 2026-07-19
- warm_up_classification: mid(有地圖形狀,缺演員名字;P0 剛好,不加速)

## Current Session breakpoint

**s18 已收(2026-07-19,WR7 冷測專場,短堂)。三主題 3/3 過:L4-L7 新情境(postgres/redis,判準框架教練給)、conntrack 分工句收、三分類家族 counter 1/3。學員決策:lab Step 5+6 延後、綁一起做(6 驗收 5 不可拆)。s17「什麼都沒學到」已用冷測結果回應:s16/s17 的內容有留住。**

next(s19),順序:
1. step A 過期債(每堂 2 題上限,過期優先):07-20 到期的「出廠全通」確認快抽 + 「default-deny 分層」;更老的 YAML-validation / ImagePullBackOff 依序輪。
2. 07-22 冷測:靜默無效「一段話組裝版」、兩張名單「兩關檢查程序」、**L4-L7 無框架新情境(過了才推 7)**、三分類家族第 2 輪(換成員)。
3. lab **Step 5(業務洞:frontend egress + backend ingress 兩條,學員自寫)+ Step 6 驗收矩陣同一坐位收** → 3-3 gate → chunk 3 累積的 F/G 補跑。叢集 `kind-k8s-coach-p2a` 留著,policy 都在,可原地續跑。
4. pacing:冷測上限 15 分鐘;學員低電量改 micro-mode。bastion 待辦不變:砍 p0。

<details>
<summary>s17 舊斷點(已大部分消化,留參考)</summary>

**s17 已收(2026-07-19,家用 VM)。P2a chunk 3,lab 做到 Step 4 完(死法搬家實證收到)。**

叢集現況:家機 `kind-k8s-coach-p2a`(瘦身版 cp+1worker,Calico v3.28.2)留著沒砍;三層場景 + `default-deny-all` + `allow-dns` 都已 apply,Step 5 可原地續跑。labs/ 三檔(netpol-lab / default-deny / allow-dns)本機已重建;**更正:labs/ 是 .gitignore 刻意排除的本機暫存(不跨機同步,s16 沒有漏 commit),成品等 Step 6 完成後過價值門檻搬 `portfolio/k8s/manifests/netpol-demo/` 才 commit**。bastion 待辦不變:砍 p0。

next(s18),順序固定:
1. **Weekly Review 強制觸發(17-10=7),不可再延**。三主題:L4-vs-L7 新情境冷測(07-20 到期,禁 ALB/NLB 與 /admin 舊題)/ conntrack 分工句 / 三分類家族卡。
2. registry 07-22 三筆冷測:靜默無效「一段話組裝版」、兩張名單「兩關檢查程序」、YAML 藏寶圖(帶著 s17 四錯的記憶)。
3. lab Step 5 業務洞(frontend egress + backend ingress 兩條,學員自寫)→ Step 6 驗收矩陣 → 3-3 gate。F/G 兩段 chunk 3 至今未跑,Step 6 後補。
4. **pacing 鐵則(s17 教訓)**:學員低電量日改 micro-mode(一個單位就收),不要壓縮版全流程;開場前 15 分鐘只做冷測不排新內容。代打分界線驗證有效:**格式雜務可代打,決策點(如一張卡 vs 兩張卡)必須留給學員**。s17 尾學員情緒「什麼都沒學到」:成因=五連跳(WR 延後、Transfer 放掉、坑二重測放掉、YAML 代打、lab 一度喊跳)導致沒有任何一個「收攏時刻」;下堂開場用冷測結果直接回應這個感受,不辯論。

</details>

<details>
<summary>s16 舊斷點(已大部分消化,留參考)</summary>

**P2a chunk 3 NetworkPolicy,D 段 lab 做到 Step 3 收(2026-07-17)。** 叢集 `kind-k8s-coach-p2a`(Calico v3.28.2,podSubnet 192.168.0.0/16);frontend/backend/db 三層 + Service 已佈(labs/netpol-lab.yaml);`default-deny-all` 已 apply(labs/default-deny.yaml)。Step 3 分層實證已收:同一條 policy 兩種死法 — `curl http://db`=`Resolving timed out`(egress 53 被鎖,死在 DNS 層)vs `curl http://<podIP>:5678`=`Connection timed out`(跳過 DNS,死在連線層)。

next(s17):
1. **Weekly Review 觸發**(17-10≥7),取代正常 flow。WR6 三主題建議:NetworkPolicy default-deny(新)/ L4-vs-L7 判準(逾期+今日兩度失手)/ conntrack 分工句(未收)。
2. WR 後接 Step 4:開 DNS 洞(規格:egress to `namespaceSelector` kube-system + `podSelector` k8s-app=kube-dns,ports UDP/TCP 53)→ 重測應變 `Connection timed out`(死法從 DNS 層移到連線層)→ Step 5 開業務洞(兩邊都要開,ingress+egress 各一張名單)→ Step 6 驗收矩陣。
3. **chunk 3-2 語義三坑未教**(AND/OR 差一個 `-`、ingress/egress 兩張獨立名單、ipBlock),s16 因 pacing 砍掉,補在 Step 5 前。
4. **叢集待辦**:`kind delete cluster --name k8s-coach-p0`(指令已給學員,未執行)。兩叢集共 6 node 把 4 核心吃爆 → p2a control-plane `container runtime is down` NotReady(worker×2 正常,lab 不受影響)。砍掉 p0 後 control-plane 應自癒。shop 場景 manifests 在 `portfolio/k8s/manifests/ingress-lab/`,capstone 規劃是搬到 p2a 重佈。

⚠️ **s16 教練校準失誤三筆(不是學員的問題,寫下來防再犯)**:① 斷點明寫「開場少考、快進 hands-on」,實際整整一小時磨兩張複習卡 → 學員三度要求跳過。② 拿 chunk 4 未教內容(kubelet Ready 條件/CNI 合約)當 chunk 3 的 gate 題,學員答「不確定」是正確反應。③ session-log 教法備忘白紙黑字「學員偏好自己敲指令」,教練整堂搶鍵盤自己跑指令,學員當場糾正「要我自己裝才對」,並回頭要求「請說明前面做了什麼,前面是你做的,所以我不太瞭解」= 搶鍵盤直接造成理解斷層。s17 硬規則:**指令一律由學員敲,教練只給規格與判讀**;YAML 依 s13 慣例可給範本照打。

</details>

## Phase status

- P0 心智模型: gate-passed(2026-06-22;legacy,pre-Examiner,coach 認證)
- P1 核心物件 + 容器底層: gate-passed(2026-06-25;legacy,pre-Examiner,coach 認證)
- P2a 網路深水區: in-progress(chunk 1 Service/kube-proxy/CoreDNS ✅、chunk 2 Ingress ✅〔s16 補完 scale=0→503 實證,全畢業〕;chunk 3 NetworkPolicy in-progress〔3-1 概念 ✅ 教完但 gate 未過、3-2 語義三坑未教、3-3 lab 做到 Step 3〕;chunk 4 CNI+封包全鏈路 未開,s16 已埋伏筆〔無 CNI 叢集 node NotReady / CoreDNS Pending vs hostNetwork 元件照跑〕)
- P2b 儲存 + 權限: not-started
- P3 調度 + 高並發 + 排障: not-started
- P4 可觀測性工程: not-started
- P5 平台工程 / GitOps: not-started
- P6 面試衝刺: not-started

Weak-topic flags: 無(至今沒有帶 flag 過 gate 的紀錄)。

## Mastery

- P0 apply→Running control flow: high (s10)— 注意:盲講易漏中間棒次(WR#1 漏 scheduler),用「五棒默數」骨架
- P1 container = namespace+cgroup: high (s6)
- P1 probe(liveness vs readiness): high (s6;判斷句「would a restart fix this?」已多次過)
- P1 Deployment/rollout: high (s6)
- P1 resource/QoS/OOM(可壓縮 vs 不可壓縮): high (s10)
- P2a Service/kube-proxy/DNAT/conntrack/CoreDNS 全鏈: high (s10 二度無鷹架冷測封印;s15 注意:規則寫手一度答成 kubelet,鷹架後撈回 kube-proxy)
- P2a Ingress(規則 vs controller、L7 純字串比對): med (s14;結果預測準、why 第一輪講不出 = W1 隱性會,gate 已過但精度待固化)
- L4 vs L7 判準(讀不讀 HTTP 內容): **low-med** (s18 回升:postgres/redis 讀寫分流新情境兩題連過、「標籤貼反」未重現,且自產「要拆開的是 redis 的指令」;判準補完整為兩步〔①轉發決定要讀到哪層 ②要拆信則工具懂不懂該協定格式,L7=協定特定的翻譯官,nginx 只懂 HTTP〕— 但兩步框架為當堂教練所給,07-22 無框架新情境過了才 med。s16 降級紀錄:同一天內兩度失手且形狀相同=**結論對、判準錯**:① ALB/NLB 題,內容映射全對〔NLB=TCP/UDP/static IP/fast、ALB=path/TLS/HTTP〕但**L4/L7 標籤整個貼反**;② NetworkPolicy 擋 `/admin` 題,結論「做不到」對但理由答「NetworkPolicy 是針對 namespace」=非機制,且與當堂剛教的「namespace 不做隔離」打架。兩次都是教練直給錨點〔fast=少做事=低層;ALB=Application=L7;from/to 欄位清單裡沒有 path〕→ **直給不算過,未封印**。s17 WR 用新情境冷測)
- NetworkPolicy(白名單 + default-deny 翻轉 + 第四個引擎): low-med (s17:3-1 Recall ✅〔policyTypes 方向性重教一輪後情境題全對〕、坑一 AND/OR ✅〔含 batch-job 案例〕、坑三 ipBlock ✅;坑二兩張名單 ❌、3-1 Transfer 組裝 ❌,兩筆 07-22 冷測。Step 4 親手完成:allow-dns 一張卡決策自己做對,死法 Resolving→Connection 搬家實證)
- conntrack 精度(table full 新舊連線): med (s18 **分工句收**:「iptables 第一次決定、conntrack 之後記住」骨架自產,應用經一次追問補全〔第 50 個去程=查 conntrack 改 Destination、回程=改 Source 反向〕;07-26 抽完整版〔兩個詞+分工句+查誰〕過即封印。歷史:s15 重抽沒過、答案直給;s16 給框架後兩個詞自產)
- DNS 排障第一刀(先用 FQDN 二分): med (s13;需鷹架)

## Scorecard history

<!-- 轉換規則:原 ✅=1、🟡/❌=0,原符號保留在註記。legacy = pre-Examiner 時期由教學 coach 認證。 -->

- 2026-06-17 | step G (s1, tier 1) | 3/3 | 用詞精準度 | 底層原理/機制/自己的話全過 | coach
- 2026-06-18 | step G (s2, tier 1) | 3/3 | 用詞精準度 | 自創恆溫器比喻講 declarative | coach
- 2026-06-22 | phase gate (P0, legacy) | 3/3 | etcd 只有 API Server 直接碰(口誤待修) | 五棒+演員+scheduler/kubelet 分清 | coach
- 2026-06-23 | step G (s4, tier 1) | 3/3 | 主動吐機制+挑經濟值 | 自己抓出「額外8→總數12」算錯 | coach
- 2026-06-24 | step G (s5, tier 1) | 3/3 | 主動吐「治本vs治標」別等追問 | 自己推出可壓縮/不可壓縮不對稱 | coach
- 2026-06-25 | phase gate (P1, legacy) | 3/3 | 先跳結論要追問才補深度(連三堂同條) | 從 exit 0 反推「app 健康、被 probe 殺」 | coach
- 2026-06-29 | weekly review (s10, tier 2) | 4/4 | 盲講控制流易漏中間棒次→五棒默數 | 封包全鏈無鷹架冷測 | coach(MTTR 當日未演練,carry 前測✅)
- 2026-07-09 | step G (s14, tier 2) | 1/4 | 隱性會沒逼成顯性:結果預測準、why 講不出 | `/apiv2`→catch-all 那刀自己串對沒鷹架 | coach(原符號:原理🟡 機制✅ 自己的話🟡 MTTR🟡)
- 2026-07-19 | weekly review (s18, tier 2) | 3/4 | 判準句慣性省略、只給結論(第五堂同條);L4-L7 兩步框架仍靠教練給才套用 | conntrack「去程改 Destination/回程改 Source+都查 conntrack」自產;redis 題「要拆開的是 redis 的指令」自己的話 | coach(原理✅ 機制✅ 自己的話✅ MTTR 未演練=0;冷測專場,s17 低信度 1/4 之後的乾淨重測)
- 2026-07-17 | A 段+chunk3 gate (s16, tier 2) | 1/4 | 判準/機制講不出:L4-L7 兩度結論對理由錯;分工句未收 | conntrack 去程/回程兩欄位**自產**(給框架不給答案,s15 直給後蒸發,今日一次推出) | coach(原理❌ 機制🟡 自己的話❌ MTTR 未演練。**本場信度低**:教練犯三錯〔過度抽考/考未教內容/搶鍵盤〕,低分含教練污染,不宜單獨採信,s17 WR 重測)

## Mistake Registry

<!-- 欄位:date | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     interval 2 = +2 天臨時複習格(口頭型 resolved,過了才進 3/7/14)。
     unresolved-session-count 於遷移時依複測紀錄初始化(近似值)。 -->

- 2026-06-18 | YAML validation | `matchLabels` 打成 `metaLabels`,不會讀 strict decoding error | 不知道 unknown-field 路徑=藏寶圖、驗證發生在 API Server | unresolved | 7 | 2026-06-30 | 2
  - 正解:讀 `unknown field "A.B.C"` 完整路徑回檔案定位;selector 認親欄位是 `matchLabels` 且必須等於 template.metadata.labels。06-23 抽考需引導才答對「檢查在 API Server、與 etcd 無關」,推 +7。
- 2026-06-22 | probe 職責 | 把 readiness 的「準備好接流量」塞給 liveness,延伸成 liveness 查 DB | 沒抓住兩種 probe 失敗後動作不同(重啟 vs 切流量) | unresolved | 7 | 2026-07-10 | 1
  - 正解:判斷句「Would a restart fix this?」;liveness 查 DB → DB 一慢全 Pod 集體重啟雪崩 + reconnection 風暴。06-25、07-03 兩次抽考 PASS(07-03 自己講出正回饋迴圈+羊群效應,唯英文詞 thundering herd 忘了),推 +7。
- 2026-06-23 | ImagePullBackOff | image 打成 `ngimx:1.25`,apply 成功卻卡 ImagePullBackOff,不解 | 驗證有邊界:API Server 只驗語法,repo 存不存在要 kubelet 第 5 棒拉了才知 | unresolved | 7 | 2026-07-03 | 1
  - 正解:第一動作 `describe pod` 看 Events;分三類訊號:`i/o timeout`=網路/egress、`401`/`toomanyrequests`=認證限流、`repository does not exist`=名稱 tag 錯。06-26 抽考三類一次答全對推 +7;07-09 A 段重抽 2/3(漏 node 出網 i/o timeout,下次補)。
- 2026-06-27 | ClusterIP/kube-proxy/DNAT 全鏈(謎題B) | 「封包先去 ClusterIP 拿 IP」誤解 + 手(iptables)vs 名單(Endpoints)混 | ClusterIP 不是地方、封包從不拜訪它,改寫發生在出發地本機 kernel | resolved | 14 | 2026-07-13 | 0
  - 正解一句話:封包不去 ClusterIP;出發地本機 kernel 照 kube-proxy 寫的規則做 DNAT,把目的地換成 Endpoints 名單裡的真 Pod IP。06-28 D 段 iptables-save 實體追鏈 + F 段無鷹架 teach-back PASS;06-29 WR 二度冷測 PASS=封印,推 +14。下次抽全鏈精度:誰寫 resolv.conf=kubelet、KUBE-SVC 機率 LB 怎麼挑 SEP、conntrack 回程反向改寫。
- 2026-06-28 | 叢集 DNS 排障 | busybox nslookup NXDOMAIN 差點誤判 CoreDNS 壞 | 排障第一刀「先用 FQDN 二分伺服器壞 vs 發問端壞」沒長成肌肉 | unresolved | 3 | 2026-07-10 | 3
  - 正解:FQDN 通 → CoreDNS 沒事查 client/resolver;測叢集 DNS 用 netshoot 不用 busybox(musl search 處理不可靠);絕不因 nslookup 失敗就重啟 CoreDNS。07-01 抽考層級混淆(把 conntrack 拉進 DNS 題);07-07 提早再測第一刀一時忘記、給梯子後定位對 → 口頭型+需鷹架,拉回近期。
- 2026-07-03 | dry-run 兩層 + Service port | `--dry-run=client` 綠燈騙人;port vs targetPort 靜默不通 | client 只做本機淺檢查;strict decoding 在 API Server(server 端) | unresolved | 3 | 2026-07-17 | 3
  - 正解:驗 YAML 用 `--dry-run=server`;port=門牌、targetPort=container 實際聽的 port,填錯=DNAT 送到沒人聽的 port→connection refused。07-06 抽考半過:client=本機查語法✅,但 server dry-run 答成「走完 etcd 整個流程」=第三次在 etcd 角色滑掉(已釘:審查在櫃檯、落帳才算數;server dry-run=審完不落帳)。07-14 重抽半過:「不會碰 etcd」站住(三滑後首次)✅,但「停在哪一步」精準版沒自收、etcd 三分類(=資料)未自答即喊繼續,教練補完。07-17 只收精準版。
- 2026-07-14 | 規則/狀態/資料 三分類(W2 家族 pattern 卡,M2 追蹤用) | conntrack 初分類答「規則」;etcd 分類未自答 | 「事先寫好放著 vs 流量跑過才長出 vs 被查的名單」判準沒長成反射 | unresolved | 3 | 2026-07-22 | 1
  - 判準:規則=靜態宣告(iptables 規則、Ingress 物件、nginx.conf);狀態=runtime 記憶(conntrack);資料=被查名單(Endpoints、etcd 內容)。思想實驗:零流量的 node,iptables 規則在(kube-proxy 事先寫好)、conntrack 空。家族三連過才封印;s15 counter 0/3(conntrack 需鷹架、etcd 未自答)。**s18 counter 1/3**:零流量思想實驗三標籤全對(conntrack 站對「狀態」,s15 的洞未重現)+ 有無內容全對;判準句仍只給結論不口述(不在冷測逼組裝,組裝留 F 段)。07-22 換家族成員測第 2 輪(候選:CoreDNS 的 Corefile、Endpoints、kube-scheduler cache)。
- 2026-07-06 | L4 vs L7 | 記成場景標籤(叢集內=L4、外部=L7),信封題連卡兩次 | 本質=轉發決定需要讀到哪層資訊(信封 IP+port vs 拆信讀 Host/path) | unresolved | 3 | 2026-07-22 | 3
  - 正解:唯一判準「轉發決定需不需要讀 HTTP 內容?」;關鍵例:shop.com/ 與 /api 信封完全相同,不拆信物理上不可能分流=Ingress 存在理由;遷移:ALB(L7) vs NLB(L4) 同判準。
  - **07-17 同日兩度失手,形狀都是「結論對、判準錯」**(mastery 降 low)。① ALB/NLB 題:功能映射全對但 L4/L7 **標籤貼反**。錨點已給(未驗收):**自己寫的 "fast" 就是證明 — 快=做的事少=讀得淺=層數低=L4**;**A**LB=**A**pplication=應用層=L7、**N**LB=**N**etwork=L4,**AWS 把層數寫在名字裡**。② NetworkPolicy 擋 `/admin` 題:答「做不到」對,理由「NetworkPolicy 是針對 namespace」錯。錨點已給(未驗收):**`from`/`to` 底下能寫的欄位只有 podSelector / namespaceSelector / ipBlock / ports+protocol — 清單裡沒有 path、沒有 Host、沒有任何 HTTP 東西,因為它從沒拆過信**。兩次錨點皆教練直給 → 不算過。**s17 WR 用第三種新情境冷測(禁用 ALB/NLB 與 /admin 兩題)**。
  - **s18(07-19)WR 冷測:過,但帶星號**。postgres 讀寫分流題:結論 ✅、判準半(「沒辦法針對 SQL 內部分流」有指到讀內容方向);教練補完整兩步判準(①讀到哪層 ②工具懂不懂該協定,L7=協定特定翻譯官、nginx 只懂 HTTP 語,pgpool 懂 postgres 語所以做得到)後,redis key 前綴換皮題兩步全對、「要拆開的是 redis 的指令」自產。標籤貼反未重現。**框架教練給故不推 7;07-22 無框架第四情境(禁 postgres/redis)過了才封印**。
- 2026-07-17 | NetworkPolicy 出廠全通 | why-first 預測「陌生 tmp Pod 連不到 db」→ 實測**連得到**(回 `db`) | k8s 出廠預設全通、namespace 只是邏輯分組不做隔離(P1 已釘過、當堂教練又粗體講過 40 分鐘,仍預測錯) | unresolved | 3 | 2026-07-20 | 0
  - 正解:出廠任何 Pod 可連任何 Pod、跨 ns 亦然;NetworkPolicy=白名單宣告,**一旦有 policy 選中該 Pod,該方向即從全通翻轉成 default-deny**。生產起手式=每個 ns 先上空白名單(`podSelector: {}` + `policyTypes: [Ingress, Egress]` + 零 rule)再逐條開洞。**此條學員親手撞出(cheap→貴的轉換點),留存預期高,3 天後只做確認性快抽**。
- 2026-07-17 | default-deny 後的分層(DNS 層 vs 連線層) | 只答「連線不到」,未分辨死在哪一層 | 層級混淆家族(同 s11 把 conntrack 拉進 DNS 題、06-28 排障第一刀) | unresolved | 3 | 2026-07-20 | 0
  - 正解:`curl http://db` 有先後兩步 —— ① 問 CoreDNS(需 egress UDP/TCP **53**)② 建 TCP 連線。default-deny 鎖 egress **連 53 一起鎖**,所以死在第 ① 步,第 ② 步沒機會發生。實證(s16 親手):`curl http://db` → `curl: (28) **Resolving** timed out`;`curl http://192.168.46.66:5678`(餵 IP 跳過 DNS)→ `curl: (28) **Connection** timed out`。**同一條 policy 兩種死法,差別只在需不需要問名字**。prod 陷阱:app log 噴 `could not resolve host` → 全隊衝去查 CoreDNS,但 CoreDNS 好好的,是 policy 封了「去問路的那條路」。故 default-deny 第一個洞永遠是 DNS。
- 2026-07-19 | 兩張獨立名單(3-2 坑二) | 「只開 backend ingress,frontend curl backend 通嗎」答「可以吧」 | 規則剛教完但沒跑兩關檢查程序,憑感覺猜;學員隨後喊「直接說明」未自跑重測 | unresolved | 3 | 2026-07-22 | 0
  - 正解:A→B 要過兩關(A egress + B ingress),任一關無洞即 timeout;檢查程序=逐關問「這個 Pod 的這個方向名單上有洞嗎」。重測要看主動跑程序,不是背結論。對照:回程免開(conntrack stateful)當天答對。
- 2026-07-19 | NetworkPolicy 靜默無效(四引擎第四行) | Transfer 只給零件不組裝:「API Server 只驗 schema → 存 etcd → 無引擎編譯成 kernel 規則 = 靜默無效 = 安全假象」整條鏈講不出,③ 危險比較只答半邊 | 先跳結論等追問才補深度(第四堂同條)+ W1 隱性會;零件全對(apiserver/CNI/馬上發現)但拒組裝 | unresolved | 3 | 2026-07-22 | 0
  - 正解一段話:API Server 只驗 schema 不驗「有沒有引擎」,通過即存 etcd,`get netpol` 查的是 etcd 裡的宣告;沒有支援的 CNI 就沒人把宣告編譯成 kernel 過濾規則,物件永遠只是資料。Ingress 沒引擎=功能壞,使用者馬上叫;NetworkPolicy 沒引擎=安全假象,沒人叫,直到被入侵。**靜默失效比大聲失效危險**。s17 學員零件全掏出但三輪不組裝,喊繼續,冷測要求一段話完整版。
- 2026-07-07 | Ingress YAML schema | `backend.service` 寫成字串 + `pathType: prefix` 小寫;client dry-run 又給假安心 | service 是 object 型別;enum 大小寫敏感;decode 錯擋在第一個 | unresolved | 3 | 2026-07-10 | 1
  - 正解:一律 `--dry-run=server`;讀 `ValidationError(路徑)` / `cannot unmarshal ... type X` 定位;對照同檔已寫對的另一條規則照抄結構。
- 2026-07-07 | Ingress 404 排障 | 差點改沒壞的規則;真兇=被 Ctrl-C 打斷的半死 port-forward 回假 404 | 規則層全綠時兇手在「你測試所經過的那層」 | parked(2026-07-16 ROI 篩:Q1 半 yes,但「port-forward 半死」是 lab 夾具產物、prod 不長這樣;同一判準已三種問法重問三次=題目壞掉。判準留檔備查,不再抽) | - | - | 3
  - 正解:404 先分層(規則層 vs 後端層);port-forward 是會抖的除錯夾具,不可信就換乾淨再下結論;任何猜測(含教練的)先驗證再採信。07-09 G 段英文重測:方向對但「規則全綠後兇手在哪」連卡兩次、誤猜 nginx-ingress 本身 → 純口頭沒重現,+2 天格重抽。
- 2026-07-09 | no-Host→404 的 why | 結果預測對,但講不出「curl 自動拿 URL 主機名當 Host」那個字 | 會用/會預測 ≠ 會講 why(W1 隱性會) | resolved(2026-07-16 ROI 篩:Q1=no,curl 填 header 是 tool trivia,面試不考;學員答「沒帶 domain → Ingress 對應不上」= 機制正確,教練題目壞掉不是學員沒懂。結案) | - | - | 1
  - 正解三步:① curl 無 -H → Host 自動填 URL 主機名 ② 那串長 DNS ≠ `shop.com` ③ 字串比不上→無規則接→404。對照 `/apiv2`:Host 對但 Prefix 以斜線切段,`/apiv2`≠`/api` 段 → 掉 `/` catch-all → web。口頭型+需鷹架,+2 天格。

## Spaced-repetition queue

<!-- 檢視序:過期優先、interval 小者優先;step A 每堂 ~2 題上限。term 卡到期日在 term-registry.md。 -->

- mistake:YAML-validation | mistake | 7 | 2026-06-30(過期)| active
- mistake:ImagePullBackOff | mistake | 7 | 2026-07-03(過期;07-09 已重抽 2/3,補「node 出網 i/o timeout」那類即可)| active
- mistake:dry-run-兩層 | mistake | 3 | 2026-07-20(s16 未口頭抽,但**真場景實用一次**:自寫 default-deny 用 `--dry-run=server` 抓到自己的 apiVersion 錯並讀懂 `no matches for kind ... in version` → 工具已進肌肉,精準版仍未收)| active
- mistake:三分類-家族卡 | mistake | 3 | 2026-07-22(**s18 counter 1/3**:零流量思想實驗全對、conntrack 站對「狀態」;第 2 輪換家族成員)| active
- mistake:L4-vs-L7 | mistake | 3 | 2026-07-22(**s18 新情境過但框架教練給**:postgres/redis 兩題連過、標籤貼反未重現;07-22 無框架第四情境〔禁 postgres/redis〕過了才推 7)| active
- mistake:NetworkPolicy-出廠全通 | mistake | 3 | 2026-07-20(s16 預測錯→**親手撞出**,留存預期高,只做確認性快抽)| active
- mistake:default-deny-分層(DNS vs 連線)| mistake | 3 | 2026-07-20(s16 親手實證兩種 timeout;層級混淆家族)| active
- mistake:NetworkPolicy-靜默無效 | mistake | 3 | 2026-07-22(s17 Transfer 未過,考「一段話完整版」組裝,不考零件)| active
- mistake:兩張獨立名單 | mistake | 3 | 2026-07-22(s17 新場景重測,驗「兩關檢查程序」有沒有長成反射)| active
- term:conntrack | term | 7 | 2026-07-26(**s18 分工句收**:骨架〔規則管第一次、conntrack 管之後〕自產,應用一次追問補全〔去程改 Destination/回程改 Source、都查 conntrack〕;07-26 抽完整版〔兩個詞+分工句+查誰〕過即封印。歷史:s16 兩個詞給框架後自產;s15 直給後 3 天蒸發=「給框架 vs 給答案」對照組證據)| active
- mistake:probe-職責 | mistake | 7 | 2026-07-10 | active
- mistake:DNS-排障第一刀 | mistake | 3 | 2026-07-10 | active
- mistake:Ingress-YAML-schema | mistake | 3 | 2026-07-10 | active
- term:(07-10 到期各卡) | term | - | 2026-07-10 | active(見 term-registry.md)
<!-- 2026-07-16 移除兩張 +2 天口頭卡(404-排障-port-forward=parked、no-Host-404-why=resolved):過 ROI 篩不過 Q1,見 teaching-elements.md「ROI 篩」。 -->
- mistake:ClusterIP-全鏈(謎題B)| mistake | 14 | 2026-07-13 | active(resolved,考精度)

## Curiosity branch

- etcd Raft 深入 | 2026-06 | 面試不直接考實作、P5 etcd 運維會用到 | 想追 Raft 共識怎麼撐起 etcd,park 到 P5(見 curriculum P5 焦點)

## Domain registries

- `term-registry.md`(同目錄):英文術語卡,18 張。欄位:EN term / 發音 / 英文定義 / 中文點破 / 學習日 / 下次抽考日。抽考雙向(見 language hook),3→7→14 節奏同引擎。
- `story-bank.md`(同目錄):behavioral 素材庫(非間隔複習型)。機會式一行入帳 + 每次 Weekly Review 保底挖 10 分鐘一則(M4);P6 提煉 STAR。
- 其他 coach 讀取檔:`session-log.md`(歷史 session 敘事)、`environment.md`(機器/context 安全事實)、`curriculum-plan.md`(戰略層,advisory)。

## Examiner ledger

(空 — P0/P1 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。第一筆 Examiner 紀錄將是 P2a gate,預計 3-5 堂後。)
