# Teaching Elements

Domain content that fills Teaching Flow steps B, C, and E. The engine governs the
structure (scenario before terminology, principle before mechanism, one Feynman Gate
per chunk); these entries supply the content it pours into each step. This coach has no
lab-manager, so there is no Step D anywhere in this file; hands-on happens on the
whiteboard inside the Step E drills.

Case IDs (`CASE-1`..`CASE-6`) refer to `references/case-bank.md`; cite them by ID.

---

## Topic: Migration 三階段 (Assess / Mobilize / Migrate & Modernize)

### Step B (Scenario Intro)

讀 CASE-1 的 customer brief：製造業機房 12 個月後租約到期,200 台 VMware VM 要全搬,維運只有 3 人,客戶開口就是「全部搬上雲,越快越好」。先不給框架名詞,問學員一句:客戶要你「馬上開始搬」,你第一步真的會去排 VM 嗎?讓他自己撞上「我根本不知道這 200 台是什麼」這個牆。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈(先講,壓在任何 phase 名詞之前):**

遷移專案不是死在技術上,是死在未知上。真正炸掉專案的是「那台沒人記得在幹嘛的機器其實是 ERP 的授權伺服器」這種事,不是「VM 搬不動」。技術幾乎都有解;沒盤點清楚的相依關係沒有解。

從這個限制往下推:既然風險集中在未知,理性的做法是先花小錢買資訊,確定值得做、也知道怎麼做,再花大錢動手。三個階段就是這條「先買資訊、再買能力、最後才規模化花錢」的切法:

1. Assess 買的是資訊:盤點、相依分析、TCO,把未知變成已知,同時算出這件事划不划算。
2. Mobilize 買的是能力:把 landing zone、pilot 遷移、團隊 runbook 準備好,證明「搬得動」而且環境接得住。
3. Migrate & Modernize 才是規模化花錢:前兩階段把不確定性消掉後,分批(wave)把主體搬過去。

一句話:三階段的存在理由是「在承諾之前先花錢消滅未知」,不是專案管理的形式。學員若把 Assess 講成「填個表」就是沒抓到這條鏈。

**Chunks(每個 chunk 一道 Feynman Gate):**

1. Discovery 與 TCO:用工具(Application Discovery Service / MPA)抓出跑什麼、彼此怎麼呼叫、用多少資源,把 on-prem 現況變成一張相依圖 + 一份 TCO,當後面所有決策的底稿。
2. Business case:TCO 不是拿來看爽的,是拿來跟財務對「搬上雲到底省不省」。要能講出省在哪(退租機房、退 VMware 授權、right-size)、成本移到哪(雲月費)。
3. Landing zone 是 Mobilize 的交付物:Mobilize 的具體產出就是一個能接住 workload 的多帳號基座(接 Topic 4),不是一句口號。
4. Wave planning:用相依關係和風險把 200 台切成數個 wave,低耦合低風險先搬當暖身,ERP 這種核心且高耦合的往後排,讓團隊先在便宜的錯誤上學會流程。

### Step E (Drill)

給學員一張打散順序的 10 項活動清單(混雜例:跑 Discovery agent、簽 landing zone SCP baseline、切第一個 pilot wave、算 TCO、決定哪幾台 retire、設 Control Tower、跟財務過 business case、做 ERP cutover runbook、盤點相依、退機房租約)。要求:歸到 Assess / Mobilize / Migrate & Modernize 三格,並挑其中兩項替它的位置辯護(為什麼是這階段、放錯階段會怎樣)。答錯或說不出「為什麼不能更早/更晚」的,當場入 Mistake Registry。

---

## Topic: 7R 決策邏輯

### Step B (Scenario Intro)

回到 CASE-1 的 workload 清單:200 台裡有 ERP、MES、一堆內部系統、還有幾台沒人記得的機器。不給 7R 名詞,先丟一句:客戶時程壓到年底,你會對這 200 台一視同仁全部搬嗎?讓學員自己意識到「有些根本該關掉、有些不能動」,不同 workload 該有不同命運。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈:**

每一個 R 都是同一個 trade-off 的不同落點:現在多花多少遷移成本,換未來多少營運彈性。Refactor 未來最省最有彈性,但現在最貴最慢;Rehost 現在最快最省事,但把 on-prem 的包袱原封不動搬上雲。

關鍵推論:選哪個 R 是被 workload 的限制決定的,不是被偏好決定的。決定 R 的四個限制是授權(license)、耦合(coupling)、產品路線(roadmap)、合規(compliance)。同一套系統,授權很貴就往 repurchase 推、跟一堆東西糾纏就先別動、產品要收了就 retire。學員若說「我喜歡 refactor 因為比較雲原生」就是用偏好取代限制,直接壓這一點。

**Chunks:**

1. 七個 R 各配一個 canonical 例子:
   - Retire:那幾台沒人記得的機器,discovery 確認沒人用就砍。
   - Retain:還在折舊、或有合規理由不能上雲的主機,這輪不動。
   - Rehost(lift-and-shift):標準內部系統,用 MGN block-level 搬,先上去再說。
   - Relocate:整套 VMware 用 VMware Cloud on AWS 平移,不改 OS 層。
   - Replatform(lift-and-tinker):搬的同時把自管 DB 換成 RDS,小改不重寫。
   - Repurchase:自建郵件/CRM 直接換成 SaaS。
   - Refactor:單體重寫成雲原生,通常留給有 roadmap 撐、值得投資的核心。
2. 決策樹的順序:先問 retire(能不能不搬),再問 retain(該不該現在搬),剩下的才上「成本/彈性階梯」從 rehost 往 refactor 挑。順序很重要:先把不用搬的篩掉,才不會浪費力氣去 refactor 一台年底要退役的機器。

### Step E (Drill)

給 6 條一行 workload(例:跑在有授權專用機的 Oracle、沒人用的舊報表站、跟五個系統互叫的 ERP、自建的 wiki、明年要下線的活動網站、標準的內部 HR 系統),限面試時間內每條指一個 R + 一句話理由。評分看理由是否咬住 license / coupling / roadmap / compliance 其中之一,而不是憑感覺。理由講不出限制的入 Registry。

---

## Topic: 工具鏈 (MGN, DMS/SCT, DataSync/Snowball, Migration Hub)

### Step B (Scenario Intro)

讀 CASE-4:核心 on-prem Oracle 跑在有授權的專用機上,DBA 兩人熟 Oracle 但沒搬過雲,客戶想趁上雲甩掉授權包袱又怕搬壞。先問學員:你要怎麼把一個「不能停、不能掉資料」的資料庫搬到雲上,而且要能隨時切回來?讓他感覺到「搬資料」和「搬伺服器」是兩種問題。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈:**

每一個遷移工具本質上都是同一個問題:把資料從 A 搬到 B,而搬的過程 A 還在被寫入,所以一定存在一個「一致性窗口」,也就是 B 落後 A 多少。選工具就是在選「你的資料是什麼型態」乘上「你能容忍多大的落後」。

- 資料型態決定工具家族:整台機器的 block(MGN)、結構化資料庫(DMS + SCT)、檔案(DataSync)、大到走不動的離線批量(Snowball)。
- 可容忍的 lag 決定線上還線下:能接受持續同步趨近零就走線上 CDC;窗口太小、頻寬太細就走離線寄硬碟。

學員若把工具當成「AWS 剛好有這幾個服務」在背,就沒看到底層都是「data movement + consistency window」。

**Chunks:**

1. MGN 複製模型:在來源裝 agent 做 block-level 連續複製到雲上的 staging area,cutover 時用複製好的磁碟開機,把停機壓到一次重開。適合 rehost 整台伺服器。
2. DMS + SCT 的分工:SCT 先做 schema 評估與轉換(量化多少 schema / 預存程序能自動轉、多少要手改),DMS 做資料搬運,先 full load 再開 CDC 持續同步把 lag 收斂。異質遷移(Oracle → PostgreSQL)兩個都要;同質遷移可能只需要 DMS。
3. 線上 vs 線下的頻寬算術(Snowball 何時贏):傳輸時間 = 資料量 / (可用頻寬 × 利用率)。當這個時間長過「等 Snowball 寄來寄回」的幾天,就該走離線。範例:50 TB、500 Mbps 專線、抓 80% 有效利用 → 50×8×10¹² bit ÷ (500×10⁶×0.8) bps ≈ 10⁶ 秒 ≈ 11.6 天。線上要 12 天而 Snowball 幾天到手,離線就贏了。
4. Migration Hub:跨工具的儀表板,把 MGN / DMS 各自的進度收攏成一個 wave 視角,回頭接 Topic 1 的 wave planning。

### Step E (Drill)

給定三組(資料量、專線頻寬、可容忍停機窗口),例如「80 TB / 1 Gbps / 一週窗口」「2 TB Oracle / 200 Mbps / 2 小時窗口」「500 GB 檔案 / 100 Mbps / 一晚」。要學員替每組選傳輸路徑(MGN / DMS+CDC / DataSync / Snowball)並把算術寫出來證明選擇。只講結論不算給看的,入 Registry。

---

## Topic: Landing zone / multi-account

### Step B (Scenario Intro)

讀 CASE-2:銀行要把面向客戶的服務搬上雲,三條紅線是不准直接出公網、所有流量要可稽核留痕、客戶資料必須境內。先問學員:如果你把 workload、log、對外出口全塞進同一個 AWS 帳號,稽核員問「你怎麼保證誰都動不了 log」,你答得出來嗎?讓他撞上「單帳號沒有硬邊界」。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈:**

在 AWS 裡,account 是最強的隔離邊界。IAM policy 可以寫錯、可以被改,但跨帳號預設什麼都到不了對方;帳號邊界是預設拒絕、且被 AWS 底層強制的。既然帳號是最硬的隔離,那麼「怎麼切帳號」這件事本身就是在做安全設計,不是行政分類。

推論:把 log 放進一個沒人能登入寫入的獨立 log-archive 帳號,稽核留痕才有物理保證;把 workload 跟 security tooling 分帳號,炸一個不會連坐。Control Tower 就是這套多帳號基座的 paved road(自動拉起 Organizations、OU、baseline guardrail),讓你不用手工重造安全輪子。

學員若把 multi-account 講成「方便分帳單」就是沒抓到「帳號 = 隔離邊界 = 安全設計」這條鏈。

**Chunks:**

1. OU 結構:用 Organizations 把帳號按用途分組(workload / security / network / log-archive、prod 與 nonprod 分開),OU 是套用 guardrail 的單位。
2. SCP vs IAM:SCP 是組織層的「天花板」(能力上限,連 root 都壓得住),IAM 是帳號內的「授權」。SCP 拿掉能力、IAM 給予能力;兩者是 AND,不是替代。合規紅線用 SCP 鎖(例:禁用非核准 region),日常權限用 IAM 給。
3. 集中式 logging 與 egress:VPC Flow Logs / CloudTrail / firewall log 集中送 log-archive 帳號;對外流量收斂到集中 inspection/egress VPC,用 TGW 當 hub 串接,workload VPC 本身不開對外路由。
4. IaC baseline:landing zone 用 IaC(Control Tower + Terraform/CfCT)長出來且可重現,新帳號 vend 出來就自帶 guardrail,不是手點。

### Step E (Drill)

要學員在白板畫出一家銀行的 OU 樹,至少涵蓋 prod / nonprod / sandbox 三類,並說明帳號怎麼分(workload / security / network / log-archive)。接著挑兩條 SCP 並替它辯護:這條 SCP 擋住什麼、對應 CASE-2 哪條紅線、為什麼一定要在 SCP 層而不是 IAM 層。說不出「為什麼是 SCP 不是 IAM」的入 Registry。

---

## Topic: Hybrid connectivity + DNS (P1 內容第二輪)

### Step B (Scenario Intro)

讀 CASE-6:工廠產線 app 必須即時呼叫 VPC 裡的 API,p99 要 20ms 以內,超過產線節拍就被拖慢。app 留 on-prem、API 在雲上。這是同一批 hybrid 元件(TGW / DX / Resolver)的第二輪:第一輪學員已經知道它們「是什麼」,這輪的開場問法直接跳到「你要怎麼設計才守得住 20ms」,逼他從認識名詞進到做取捨。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈(second-pass rule):**

這是第二輪教學,規則是不再問「TGW / DX / Resolver 是什麼」,改問「什麼時候用、怎麼取捨」。每一個 hybrid 設計都是四個變數的乘積:頻寬 × 延遲一致性 × failover × 成本。你動任何一個都在別的上面付代價。

以 CASE-6 為例:要延遲一致(低抖動)就得上 DX 專線,但 DX 貴且單條沒有備援;加 VPN 當 failover 補上可用性,但 failover 走公網 IPSec,延遲會跳高、20ms 直接守不住,這是要當場對客戶講明的風險,不是等它發生。四個變數擺上桌一起權衡,才叫設計;只喊「DX 很快」是名詞層,沒過第二輪。

**Chunks:**

1. DX + VPN failover 設計:DX 走主線壓穩延遲與抖動,VPN 當備援。要講清楚 failover 後延遲從專線等級跳到公網 IPSec 等級,這是設計自帶的降級,不是故障。
2. Hybrid DNS 端到端解析路徑:on-prem 要解 VPC 內名稱走 Route 53 Resolver inbound endpoint,VPC 要解 on-prem 名稱走 outbound endpoint + forwarding rule。要能把「app 送出名字 → 誰回答 → 封包往哪走」整條畫出來,並確認解析本身不繞遠路。
3. MTU 暗坑:DX 支援 jumbo frame(9001),VPN 是 1500 且被 IPSec overhead 再吃掉一截。兩邊 MTU 不一致又沒處理,大封包會被分片,或撞上 PMTUD 黑洞(ICMP 被擋、封包默默卡死重傳)。這是 hybrid 延遲/卡頓問題的經典根因,面試官期待學員不用被問就先講。

### Step E (Drill)

要學員在白板畫出完整封包路徑:on-prem app → (DNS 解析:誰回答、走哪個 endpoint)→ DX/TGW → VPC → DB,把解析路徑也畫進去。畫完後,讓學員自己挑一個點把它弄壞(DX 斷掉 failover 到 VPN、Resolver rule 設錯、MTU mismatch),然後現場 troubleshoot:症狀會是什麼、先看哪裡、怎麼確認。挑不出斷點或排障方向錯的入 Registry。

底層 TCP/DNS 機制不在此重教(見文末 cross-reference);這裡只教 hybrid 設計取捨。

---

## Topic: Well-Architected as scoring frame

### Step B (Scenario Intro)

不需要新 case,拿學員剛答完的任何一題 CASE 答案當素材。開場一句:你剛剛那套設計,自己覺得漏了什麼?通常答不太出來,這正是 Well-Architected 要補的位置。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈:**

Well-Architected 不是一套架構,是一份 review checklist。它的用途是回頭掃「你的答案忘了什麼」,而人最常忘的是成本(cost)和維運(operational excellence),因為白板上先想到的都是功能與可用性。把 WA 當「要照著蓋的藍圖」是誤用;它是照妖鏡,不是模板。

學員若試圖「用五大支柱來設計」就是把工具用反了,壓這一點:先設計,再拿 WA 掃缺口。

**Chunks:**

1. 五大支柱各一行:Operational Excellence(跑起來怎麼運維、怎麼觀測)、Security(誰能碰什麼、資料怎麼保護)、Reliability(壞了怎麼恢復,對到 RTO/RPO)、Performance Efficiency(選對資源型別與規模)、Cost Optimization(有沒有在燒冤枉錢)。
2. 怎麼跑一遍 self-review:對著自己的答案,每個支柱問一句「這裡最弱的一點是什麼」,不求面面俱到,先抓出最痛的兩個洞。重點是養成交卷前自己先掃一遍的習慣。

### Step E (Drill)

要學員拿自己剛才任一題 CASE 的答案,套五大支柱各問一遍,找出至少兩個 gap(通常會落在 cost 或 ops),並說明補法。找不到 gap 或只會空喊「要更安全」講不出具體缺口的,入 Registry。

---

## Topic: 顧問溝通 (pushback)

### Step B (Scenario Intro)

讀 CASE-5:內部低流量應用,老闆聽完研討會回來堅持第一天就要 multi-region active-active,說這樣才叫雲原生。先問學員:你會照單全收把 active-active 畫出來嗎?讓他感覺到「客戶要的」跟「客戶該要的」不一樣,而你的價值在後者。

### Step C (Core Teaching: first principles + chunks)

**第一性推導鏈:**

顧問被付錢不是來照抄需求,是來「帶著數據跟客戶唱反調」。照單全收畫 active-active 很省事,但那是把判斷責任推回給客戶。真正的價值是:承認客戶的目標(可靠),然後用數字證明他選的手段(active-active)對這個目標是過度投資,再給一條更便宜、同樣達標的路。

四步結構(對到 Amazon LP 的 Have Backbone; Disagree and Commit 與 Earn Trust):

1. Acknowledge:先承認並釐清目標,把「要很可靠」翻成可量化的 RTO / RPO 數字。
2. Quantify:量化這個要求的代價(雙倍基礎成本、跨 region 資料一致性難題、維運與測試複雜度)。
3. Offer:提對著數字挑的替代方案(RTO 小時級 → backup-restore / pilot light 就夠;真要分鐘級才談 warm standby / active-active)。
4. Land on customer choice:講清每個選項的成本與風險,把拍板權留給客戶,而不是幫他決定或默默照做。

學員若直接開畫 active-active、或反過來硬否定客戶,都沒抓到「用數據反對、但把決定權還給客戶」這條鏈。

**Chunks:**

1. 四步結構本身:acknowledge → quantify → offer → land on choice,順序不能亂。先承認才聽得進去,先量化才有反對的底氣,先給替代才不是空反對,最後還權才叫 earn trust。
2. 用英文交付:這是英語口說練習點。要能用平穩、對事不對人的語氣講出四步,例句骨架如「I hear that reliability is the goal, so let's put a number on it...」「Active-active roughly doubles the baseline cost and adds cross-region consistency to solve; if your RTO is in hours, pilot light gets you there for a fraction...」「Here are the options with costs; the call is yours.」

### Step E (Drill)

要學員用英文做一段 2 分鐘的 pushback 交付,對象是 CASE-5 的老闆執念。評分看的是四步結構完不完整(有沒有先 acknowledge、有沒有拿數字 quantify、有沒有給對著 RTO/RPO 挑的替代方案、有沒有把決定權還回去),不評口音。跳過任一步或變成硬吵/照單全收的入 Registry。

---

## Cross-reference: 不在此教的底層主題

下列底層主題由 k8s-coach 的 foundations 檔擁有,本 coach 不重複教;學員需要補課時導向該檔對應章節:

檔案:`skills/k8s-coach/references/foundations-linux-network.md`

- TCP 狀態機與高並發:§3
- DNS 遞迴解析內部機制:§4
- conntrack 深化:§3.5
- OOM(cgroup OOM vs node eviction):§2.4
- Linux 性能排查方法論(USE / 60 秒清單):§5

本檔的 hybrid connectivity(Topic 5)只教雲端 hybrid 設計取捨;封包在 TCP/DNS 層的內部運作到上表章節讀。
