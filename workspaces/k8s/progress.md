# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 15
- last_weekly_review: 10
- last_session_date: 2026-07-14
- warm_up_classification: mid(有地圖形狀,缺演員名字;P0 剛好,不加速)

## Current Session breakpoint

P2a, step D 前置(chunk 2 補做 30 秒), next: 學員先答 why-first 預測題(已出題未答:`kubectl scale deploy shop-api --replicas=0` 後,叢集內 `curl -H "Host: shop.com" http://ingress-nginx-controller.ingress-nginx.svc.cluster.local/api` 回幾?為何不是 404?正解:503=規則層有接但 Endpoints 空、是後端層在說話;404=規則層沒接)→ 跑指令驗證 → `--replicas=1` 復原 → 建 `clusters/kind-p2a.yaml`(disableDefaultCNI)、down p0 / up p2a、裝 Calico → chunk 3 C 段,教材 `references/phase-2a-networking.md` C-3。s16 A 段:cap 2 張、過期+interval 小者優先(07-11 兩張 +2 天口頭卡最急;07-17 有 conntrack 兩個詞+分工句、dry-run 精準版、三分類家族卡)。s15 pacing 訊號:學員趕收工、輸出推兩次即收、兩卡皆未全過 → s16 開場少考,快進 hands-on。

## Phase status

- P0 心智模型: gate-passed(2026-06-22;legacy,pre-Examiner,coach 認證)
- P1 核心物件 + 容器底層: gate-passed(2026-06-25;legacy,pre-Examiner,coach 認證)
- P2a 網路深水區: in-progress(chunk 1 Service/kube-proxy/CoreDNS ✅、chunk 2 Ingress ✅;chunk 3 NetworkPolicy、chunk 4 CNI+封包全鏈路 未開)
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
- L4 vs L7 判準(讀不讀 HTTP 內容): med (s14;07-06 坑,07-09 到期)
- conntrack 精度(table full 新舊連線): med (s15 重抽沒過:三分類經思想實驗後自答「狀態」✅,但去程=目的地/回程=來源 四輪未自產、答案直給;07-17 只考兩個詞+分工句)
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
- 2026-07-14 | 規則/狀態/資料 三分類(W2 家族 pattern 卡,M2 追蹤用) | conntrack 初分類答「規則」;etcd 分類未自答 | 「事先寫好放著 vs 流量跑過才長出 vs 被查的名單」判準沒長成反射 | unresolved | 3 | 2026-07-17 | 1
  - 判準:規則=靜態宣告(iptables 規則、Ingress 物件、nginx.conf);狀態=runtime 記憶(conntrack);資料=被查名單(Endpoints、etcd 內容)。思想實驗:零流量的 node,iptables 規則在(kube-proxy 事先寫好)、conntrack 空。家族三連過才封印;s15 counter 0/3(conntrack 需鷹架、etcd 未自答)。
- 2026-07-06 | L4 vs L7 | 記成場景標籤(叢集內=L4、外部=L7),信封題連卡兩次 | 本質=轉發決定需要讀到哪層資訊(信封 IP+port vs 拆信讀 Host/path) | unresolved | 3 | 2026-07-09 | 1
  - 正解:唯一判準「轉發決定需不需要讀 HTTP 內容?」;關鍵例:shop.com/ 與 /api 信封完全相同,不拆信物理上不可能分流=Ingress 存在理由;遷移:ALB(L7) vs NLB(L4) 同判準。
- 2026-07-07 | Ingress YAML schema | `backend.service` 寫成字串 + `pathType: prefix` 小寫;client dry-run 又給假安心 | service 是 object 型別;enum 大小寫敏感;decode 錯擋在第一個 | unresolved | 3 | 2026-07-10 | 1
  - 正解:一律 `--dry-run=server`;讀 `ValidationError(路徑)` / `cannot unmarshal ... type X` 定位;對照同檔已寫對的另一條規則照抄結構。
- 2026-07-07 | Ingress 404 排障 | 差點改沒壞的規則;真兇=被 Ctrl-C 打斷的半死 port-forward 回假 404 | 規則層全綠時兇手在「你測試所經過的那層」 | unresolved | 2 | 2026-07-11 | 2
  - 正解:404 先分層(規則層 vs 後端層);port-forward 是會抖的除錯夾具,不可信就換乾淨再下結論;任何猜測(含教練的)先驗證再採信。07-09 G 段英文重測:方向對但「規則全綠後兇手在哪」連卡兩次、誤猜 nginx-ingress 本身 → 純口頭沒重現,+2 天格重抽。
- 2026-07-09 | no-Host→404 的 why | 結果預測對,但講不出「curl 自動拿 URL 主機名當 Host」那個字 | 會用/會預測 ≠ 會講 why(W1 隱性會) | unresolved | 2 | 2026-07-11 | 1
  - 正解三步:① curl 無 -H → Host 自動填 URL 主機名 ② 那串長 DNS ≠ `shop.com` ③ 字串比不上→無規則接→404。對照 `/apiv2`:Host 對但 Prefix 以斜線切段,`/apiv2`≠`/api` 段 → 掉 `/` catch-all → web。口頭型+需鷹架,+2 天格。

## Spaced-repetition queue

<!-- 檢視序:過期優先、interval 小者優先;step A 每堂 ~2 題上限。term 卡到期日在 term-registry.md。 -->

- mistake:YAML-validation | mistake | 7 | 2026-06-30(過期)| active
- mistake:ImagePullBackOff | mistake | 7 | 2026-07-03(過期;07-09 已重抽 2/3,補「node 出網 i/o timeout」那類即可)| active
- mistake:dry-run-兩層 | mistake | 3 | 2026-07-17(s15 半過:etcd 不碰✅,停在哪步精準版沒自收)| active
- mistake:三分類-家族卡 | mistake | 3 | 2026-07-17(s15 首發 counter 0/3)| active
- mistake:L4-vs-L7 | mistake | 3 | 2026-07-09(過期)| active
- term:conntrack | term | 3 | 2026-07-17(s15 沒過:分類「狀態」✅,兩個詞沒自產,見 term-registry)| active
- mistake:probe-職責 | mistake | 7 | 2026-07-10 | active
- mistake:DNS-排障第一刀 | mistake | 3 | 2026-07-10 | active
- mistake:Ingress-YAML-schema | mistake | 3 | 2026-07-10 | active
- term:(07-10 到期各卡) | term | - | 2026-07-10 | active(見 term-registry.md)
- mistake:404-排障-port-forward | mistake | 2 | 2026-07-11 | active
- mistake:no-Host-404-why | mistake | 2 | 2026-07-11 | active
- mistake:ClusterIP-全鏈(謎題B)| mistake | 14 | 2026-07-13 | active(resolved,考精度)

## Curiosity branch

- etcd Raft 深入 | 2026-06 | 面試不直接考實作、P5 etcd 運維會用到 | 想追 Raft 共識怎麼撐起 etcd,park 到 P5(見 curriculum P5 焦點)

## Domain registries

- `term-registry.md`(同目錄):英文術語卡,18 張。欄位:EN term / 發音 / 英文定義 / 中文點破 / 學習日 / 下次抽考日。抽考雙向(見 language hook),3→7→14 節奏同引擎。
- `story-bank.md`(同目錄):behavioral 素材庫(非間隔複習型)。機會式一行入帳 + 每次 Weekly Review 保底挖 10 分鐘一則(M4);P6 提煉 STAR。
- 其他 coach 讀取檔:`session-log.md`(歷史 session 敘事)、`environment.md`(機器/context 安全事實)、`curriculum-plan.md`(戰略層,advisory)。

## Examiner ledger

(空 — P0/P1 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。第一筆 Examiner 紀錄將是 P2a gate,預計 3-5 堂後。)
