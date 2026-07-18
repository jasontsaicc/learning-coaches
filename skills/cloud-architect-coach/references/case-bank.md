# Case Bank

> **用途**：P2 Migration 與 P3 Case Drills + Mocks 的白板案例素材。每個 case 有三塊：
> - **Customer brief**：coach 逐字讀給學生的客戶開場白，用客戶第一人稱、帶具體數字。學生聽完要主動追問缺的條件，不能直接開畫架構。
> - **Hire bar**：一個 hire-bar 答案必須涵蓋的骨架。這是評分基準,不是逐字答案;學生要用自己的話展開並帶 trade-off。缺其中一條就是 no-hire 訊號。
> - **Follow-up**：面試官的標準追問。學生的第一版答案守不住這一擊,分數就上不去。
>
> 使用方式:coach 讀 brief、學生口頭設計 10-15 分鐘、coach 用 Hire bar 逐條打勾、最後丟 Follow-up 逼學生守住。Well-Architected 五大支柱只當評分視角,不當上課主題。

---

## CASE-1 製造業 DC exit

**Customer brief**（逐字讀）:
「我們是一家傳統製造業,自建機房跑了十幾年。現在機房的租約再 12 個月到期,房東不續約,所以年底前所有東西都要搬走。我們大概有 200 台 VM,全部跑在 VMware 上面,裡面有 ERP、MES、一堆內部系統,還有幾台沒人記得在幹嘛但也不敢關。我的維運團隊只有 3 個人,平常光是救火就忙不完。我要的很簡單:全部搬上雲,越快越好,不要出事。你會怎麼幫我規劃?」

**Hire bar**:
- 先講三階段框架:Assess(盤點與相依分析)、Mobilize(landing zone 與 pilot 遷移)、Migrate & Modernize(分批搬),而且明確把 discovery 放第一步,不能一聽到「全部搬」就開始排 VM。
- Wave planning:用相依關係和風險把 200 台切成數個 wave,低風險、低耦合的先搬當暖身,ERP 這種核心且高耦合的往後排。
- 7R 判斷:承認這種時程壓力下主體是 rehost 為主、少量 replatform,而不是全部 refactor。關鍵是主動點出「那幾台沒人記得的機器」是 retire 候選,discovery 階段就要決定砍掉還是搬。
- 工具:server 遷移點名 MGN(Application Migration Service),做 block-level replication + cutover,不是手動重灌。
- 主動點出 VMware licensing:on-prem 的 VMware 授權在搬上雲後怎麼算(retire 掉授權成本 vs 用 VMware Cloud on AWS 過渡),把授權當成 rehost/replatform 的決策變數之一。

**Follow-up**:「ERP 那個 wave,客戶說完全不能停機,你的 cutover 怎麼做到 zero downtime?」

---

## CASE-2 金融業 compliance

**Customer brief**(逐字讀):
「我們是一家銀行,要把一個面向客戶的線上服務搬上雲。但這是受監管的環境,有幾條是不能踩的紅線:第一,不准有任何流量直接出公網,對外連線一定要走受控出口;第二,所有進出的流量都要能被檢查、留紀錄,監理單位隨時會來查;第三,客戶資料必須留在境內,不能跑到其他 region。我知道雲很方便,但如果過不了稽核,方便對我沒有意義。這個 landing zone 你會怎麼設計?」

**Hire bar**:
- Multi-account landing zone:用 Control Tower / Organizations 分帳號(workload、security、network、log-archive 分離),不是所有東西擠一個帳號。
- 集中式 egress + inspection:出口流量收斂到集中的 inspection VPC / egress VPC,用 Network Firewall 或第三方 appliance 做流量檢查,workload VPC 本身不開對外路由。點出 TGW 當作 hub 串接的角色。
- 私有連線:對外與對內走 DX(Direct Connect)私有連線而非公網,說明 private VIF / VPC endpoint 讓流量不落公網。
- Hybrid DNS:Route 53 Resolver inbound/outbound endpoint 讓 on-prem 與 VPC 的名稱解析互通,並確保解析路徑本身也在受控範圍內。
- 稽核留痕:VPC Flow Logs、CloudTrail、Network Firewall log 集中送到 log-archive 帳號,資料留境內 region,並講出資料落地的 region 綁定怎麼保證。

**Follow-up**:「稽核員問你:你怎麼證明『沒有任何一個封包是沒被檢查就出去的』?拿得出證據嗎?」

---

## CASE-3 帳單爆炸

**Customer brief**(逐字讀):
「半年前我們做完 lift-and-shift,把所有東西從機房搬上雲,搬的時候一切順利。問題是帳單。當初的 business case 抓的預算,現在實際帳單是它的 3 倍。財務每個月看到帳單就來問我到底發生什麼事,我也答不太出來。我不想聽『雲本來就貴』這種話,我要知道錢花在哪、哪些是浪費、怎麼修。你會從哪裡開始查?」

**Hire bar**:
- 結構化的成本檢視流程,不是東砍一刀西砍一刀:先用 Cost Explorer / CUR 按帳號、service、tag 拆解,找出成本大頭再動手。
- Right-sizing 要有證據:看 CloudWatch 使用率(CPU、memory、network)佐證,而不是憑感覺調小;lift-and-shift 常見的是 on-prem 規格直接照搬造成 over-provision。
- 承諾折扣:對穩定的基載用 Savings Plans / Reserved Instances,並講出 coverage 與 commitment 的 trade-off(綁太多失去彈性)。
- Storage 分層稽核:S3 lifecycle 到 IA / Glacier、砍掉沒掛載的 EBS 與過期 snapshot、gp2 換 gp3。
- 點出 lift-and-shift 的隱形陷阱:NAT Gateway 的資料處理費、跨 AZ / 跨 region data transfer、公網流出費,這幾項在 lift-and-shift 後常常是沒人看到的黑洞。
- Tagging for allocation:把成本歸屬做起來(tag policy + cost allocation tag),並且把整件事框成「維運流程要長出成本治理」,不是這次砍完就結束。

**Follow-up**:「CFO 拍板下一季要砍 40%,你第一刀先砍哪裡?怎麼確定砍下去不會弄壞線上?」

---

## CASE-4 Oracle 遷移

**Customer brief**(逐字讀):
「我們有一套核心的 on-prem Oracle 資料庫,跑在一台有授權的專用設備上,那台設備和 Oracle 的授權每年都是一筆很痛的錢。DBA 團隊只有 2 個人,他們對 Oracle 很熟,但沒碰過雲上的資料庫遷移。我想趁這次上雲把這個授權包袱處理掉,但又怕搬壞。你會怎麼評估、怎麼搬?」

**Hire bar**:
- 先評估再談搬法:用 SCT(Schema Conversion Tool)做 assessment,量化有多少 schema / 預存程序 / proprietary 功能能自動轉、多少要手改,產出一份 assessment report 當決策依據。
- Replatform vs repurchase 的辯論,而且以授權成本當主軸:留 Oracle 引擎搬到 RDS for Oracle 時要分清授權模式,SE2 有 License Included(AWS 把授權包進時數費,客戶得以擺脫原本的 Oracle 合約),EE 只能 BYOL(授權包袱還在);另一條是 repurchase 改用 Aurora PostgreSQL / RDS PostgreSQL(徹底擺脫授權但要付出 schema 轉換與應用改動成本),把每條路的 license 帳算給客戶看。
- Cutover 用 DMS + CDC:先做 full load 再開 CDC 持續同步,把停機壓到最小,並且一定要有 rollback 計畫(來源保持可用、驗證失敗就切回)。
- 主動談 downtime window:cutover 需要多長的凍結窗口、跟業務怎麼協商、驗證(資料筆數、checksum、應用煙霧測試)排在窗口裡的哪一段。

**Follow-up**:「CDC lag 一直降不到零,cutover 窗口只有 2 小時,現在要你當場決定 go 還是 no-go,你怎麼判斷?」

---

## CASE-5 多region 執念

**Customer brief**(逐字讀):
「我們有一個內部用的應用,使用者是公司內部同仁,流量其實不大,尖峰也就幾百個人在用。但我上面的老闆聽了一場研討會回來,堅持這個系統從第一天就要做 multi-region active-active,他說這樣才叫『雲原生』、才夠可靠。我需要你幫我把這個架構設計出來。」

**Hire bar**:
- 不是照單全收畫 active-active,而是走四步 pushback:
  1. 先承認並釐清目標:問出真正的 RTO / RPO 數字(能容忍停多久、能容忍掉多少資料),把「要很可靠」翻譯成可量化的指標。
  2. 量化 active-active 的代價:雙倍以上的基礎成本、資料雙向同步的一致性難題(衝突解決、跨 region 延遲)、維運與測試複雜度暴增。
  3. 提對應實際數字的替代方案:如果 RTO 是小時級,backup-restore 或 pilot light 就夠;真的需要分鐘級才談 warm standby / active-active,方案要對著 RTO/RPO 挑,不是對著口號挑。
  4. 把決策權留給客戶:講清楚每個選項的成本與風險,讓客戶(和他老闆)在知情下拍板,而不是幫他決定或默默照做。
- 核心是展現 consultant 的判斷力:能對著低流量內部系統指出 active-active 是 over-engineering,同時不否定客戶的可靠性訴求。

**Follow-up**:「客戶說『錢不是問題,老闆就是要 active-active』,你還怎麼接?」

---

## CASE-6 Hybrid 延遲敏感

**Customer brief**(逐字讀):
「我們工廠有一套跑在產線上的應用,它必須即時呼叫一個放在 VPC 裡的 API,而且延遲要求很硬:p99 要在 20 毫秒以內,超過的話產線的節拍就會被拖慢。應用留在廠內 on-prem,API 在雲上,這條 hybrid 的連線你會怎麼設計才守得住這個延遲?」

**Hire bar**:
- 主線用 DX(Direct Connect)走專線把延遲與抖動壓穩,VPN 當 failover 備援,並講清楚 failover 時延遲會跳高(走公網 IPSec),這本身就是風險。
- Latency budget 的算術:把 20ms 拆開,光纖來回的傳播延遲(和廠到 DX location 的物理距離綁定)、設備轉發、API 本身處理時間各佔多少,證明 20ms 到底守不守得住,而不是嘴上說「DX 很快」。
- Hybrid DNS 解析路徑:Route 53 Resolver endpoint 讓 on-prem 解析 VPC 內名稱,並確認解析本身不會繞遠路或增加延遲。
- 主動點出 MTU mismatch:DX(支援 jumbo frame 9001)與 VPN(1500 且有 IPSec overhead)MTU 不同,若沒處理會造成分片或 PMTUD 黑洞,這是 hybrid 延遲問題的經典暗坑,面試官想看你不用被問就先講。

**Follow-up**:「上線後 p99 好好的維持了好幾週,某天突然開始出現數秒級的尖刺,你先去哪裡找?」(期待方向:是不是 DX 掛了 failover 到 VPN 路徑、或是 PMTUD 黑洞造成大封包卡住重傳)
