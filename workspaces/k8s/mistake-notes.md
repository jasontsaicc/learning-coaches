# Mistake Notes

<!-- progress.md 的 Mistake Registry 只存 PROGRESS-SCHEMA §7 的八個欄位。
     正解、判準句、L6 顧問版、歷史重測紀錄、下次抽考題寫在這裡,節標題 = registry 行的 `date | topic`。
     開場不讀這個檔;step A 抽考到哪張卡,才讀哪一節。新的重測紀錄追加到對應節,不要寫回 registry。 -->

## 2026-06-18 | YAML validation

- 正解:讀 `unknown field "A.B.C"` 完整路徑回檔案定位;selector 認親欄位是 `matchLabels` 且必須等於 template.metadata.labels。06-23 抽考需引導才答對「檢查在 API Server、與 etcd 無關」,推 +7。**s23 實戰現形**:allow-dns 重寫把 selector 塞進 ports 清單,dry-run 前自行「猜修」把 apiVersion 改成大寫 V1(`no matches for kind ... in version` 第二次親手撞,s16 同款),拿到錯誤後學員選擇跳過讀圖、教練代打。讀圖 rep 仍欠,WR9 用帶錯 YAML 現場讀圖。**s25 rep 首次自己讀圖過關**:`strict decoding error: unknown field "spec.sccessModes"`,教練只說「訊息把座標給你了」,學員**自己回檔案找到打錯的字並改對**,apply 成功 —— 建卡以來第一次不用代打。但同一段稍早學員說「直接給我 yaml」跳過自寫 PVC,rep 打折,故留 3 不推 7;08-08 換一個不同型別的錯(`cannot unmarshal` 或 enum 大小寫)再測一次,過了才 resolved。

## 2026-06-22 | probe 職責

- 正解:判斷句「Would a restart fix this?」;liveness 查 DB → DB 一慢全 Pod 集體重啟雪崩 + reconnection 風暴。06-25、07-03 兩次抽考 PASS(07-03 自己講出正回饋迴圈+羊群效應,唯英文詞 thundering herd 忘了),推 +7。

## 2026-06-23 | ImagePullBackOff

- 正解:第一動作 `describe pod` 看 Events;分三類訊號:`i/o timeout`=網路/egress、`401`/`toomanyrequests`=認證限流、`repository does not exist`=名稱 tag 錯。06-26 抽考三類一次答全對推 +7;07-09 A 段重抽 2/3(漏 node 出網 i/o timeout,下次補)。
- **s26 真場景現形但 rep 不算數**:`image: buybox` 打錯 → `ImagePullBackOff` → 三選一答 **C 正確**,但**要了兩次都沒貼 Events 關鍵字**。教練已當場點名「這題你不看 Events 也猜得到,因為是我先告訴你 image 打錯的」。**不推 interval,留 3**,08-09 換一個學員不知情的故障(建議用 `401` 或 `i/o timeout` 型),要求先貼 Events 再分類。顧問價值已教:三類的處理人不同(A 網路組 / B 平台憑證 / C 寫 YAML 的人),`describe pod` 第一眼就要分流到對的人。

## 2026-06-27 | ClusterIP/kube-proxy/DNAT 全鏈(謎題B)

- 正解一句話:封包不去 ClusterIP;出發地本機 kernel 照 kube-proxy 寫的規則做 DNAT,把目的地換成 Endpoints 名單裡的真 Pod IP。06-28 D 段 iptables-save 實體追鏈 + F 段無鷹架 teach-back PASS;06-29 WR 二度冷測 PASS=封印,推 +14。下次抽全鏈精度:誰寫 resolv.conf=kubelet、KUBE-SVC 機率 LB 怎麼挑 SEP、conntrack 回程反向改寫。

## 2026-06-28 | 叢集 DNS 排障

- 正解:FQDN 通 → CoreDNS 沒事查 client/resolver;測叢集 DNS 用 netshoot 不用 busybox(musl search 處理不可靠);絕不因 nslookup 失敗就重啟 CoreDNS。07-01 抽考層級混淆(把 conntrack 拉進 DNS 題);07-07 提早再測第一刀一時忘記、給梯子後定位對 → 口頭型+需鷹架,拉回近期。

## 2026-07-03 | dry-run 兩層 + Service port

- 正解:驗 YAML 用 `--dry-run=server`;port=門牌、targetPort=container 實際聽的 port,填錯=DNAT 送到沒人聽的 port→connection refused。07-06 抽考半過:client=本機查語法✅,但 server dry-run 答成「走完 etcd 整個流程」=第三次在 etcd 角色滑掉(已釘:審查在櫃檯、落帳才算數;server dry-run=審完不落帳)。07-14 重抽半過:「不會碰 etcd」站住(三滑後首次)✅,但「停在哪一步」精準版沒自收、etcd 三分類(=資料)未自答即喊繼續,教練補完。07-17 只收精準版。
- **s26 實戰現形 + 新形狀命名**。學員自寫 YAML 打成 `image: buybox`,教練明講「故意不改」→ 預測二選一「dry-run 會不會抓到」→ **答 B(綠燈)✅ 且實測綠燈 → apply 成功 → `ImagePullBackOff`**,分界線親手做出來。但追問「為什麼攔不到」→ 答「**因為 server dry-run 不會實際去查有沒有這個 image**」= **把「攔不到」換句話說,同義反覆,不是判準**。
- 新的檢驗法(已教,對治整個 pattern 家族):**判準句講完,對方有沒有拿到一個新事實?**「因為 A 不會做 B」沒有新事實;「誰做、在哪一棒」才有。
- 精準版:**image 存不存在只有 kubelet 在 node 上真的去拉時才知道;API Server 從頭到尾不碰 registry,它只驗 schema 和 admission。** 回扣 P0 五棒:`--dry-run=server` = 審完不落帳,連第 2 棒都沒走到;拉 image 是第 5 棒。留 3,08-09 抽精準版(要求答出「誰」與「第幾棒」)。

## 2026-07-14 | 規則/狀態/資料 三分類(W2 家族 pattern 卡,M2 追蹤用)

- 判準:規則=靜態宣告(iptables 規則、Ingress 物件、nginx.conf);狀態=runtime 記憶(conntrack);資料=被查名單(Endpoints、etcd 內容)。思想實驗:零流量的 node,iptables 規則在(kube-proxy 事先寫好)、conntrack 空。家族三連過才封印;s15 counter 0/3(conntrack 需鷹架、etcd 未自答)。**s18 counter 1/3**:零流量思想實驗三標籤全對(conntrack 站對「狀態」,s15 的洞未重現)+ 有無內容全對;判準句仍只給結論不口述(不在冷測逼組裝,組裝留 F 段)。07-22 換家族成員測第 2 輪(候選:CoreDNS 的 Corefile、Endpoints、kube-scheduler cache)。

## 2026-07-06 | L4 vs L7

- 正解:唯一判準「轉發決定需不需要讀 HTTP 內容?」;關鍵例:shop.com/ 與 /api 信封完全相同,不拆信物理上不可能分流=Ingress 存在理由;遷移:ALB(L7) vs NLB(L4) 同判準。
- **07-17 同日兩度失手,形狀都是「結論對、判準錯」**(mastery 降 low)。① ALB/NLB 題:功能映射全對但 L4/L7 **標籤貼反**。錨點已給(未驗收):**自己寫的 "fast" 就是證明 — 快=做的事少=讀得淺=層數低=L4**;**A**LB=**A**pplication=應用層=L7、**N**LB=**N**etwork=L4,**AWS 把層數寫在名字裡**。② NetworkPolicy 擋 `/admin` 題:答「做不到」對,理由「NetworkPolicy 是針對 namespace」錯。錨點已給(未驗收):**`from`/`to` 底下能寫的欄位只有 podSelector / namespaceSelector / ipBlock / ports+protocol — 清單裡沒有 path、沒有 Host、沒有任何 HTTP 東西,因為它從沒拆過信**。兩次錨點皆教練直給 → 不算過。**s17 WR 用第三種新情境冷測(禁用 ALB/NLB 與 /admin 兩題)**。
- **s18(07-19)WR 冷測:過,但帶星號**。postgres 讀寫分流題:結論 ✅、判準半(「沒辦法針對 SQL 內部分流」有指到讀內容方向);教練補完整兩步判準(①讀到哪層 ②工具懂不懂該協定,L7=協定特定翻譯官、nginx 只懂 HTTP 語,pgpool 懂 postgres 語所以做得到)後,redis key 前綴換皮題兩步全對、「要拆開的是 redis 的指令」自產。標籤貼反未重現。**框架教練給故不推 7;07-22 無框架第四情境(禁 postgres/redis)過了才封印**。

## 2026-07-17 | NetworkPolicy 出廠全通

- 正解:出廠任何 Pod 可連任何 Pod、跨 ns 亦然;NetworkPolicy=白名單宣告,**一旦有 policy 選中該 Pod,該方向即從全通翻轉成 default-deny**。生產起手式=每個 ns 先上空白名單(`podSelector: {}` + `policyTypes: [Ingress, Egress]` + 零 rule)再逐條開洞。**s20 重抽半過**:情境題(新 ns 無 policy 互打通不通)結論靠提示撈回、關鍵 why「podSelector 只在自己 ns 內選人,勢力範圍不跨 ns;from/to 名單可跨 ns=放行誰,podSelector=翻轉誰」沒站住 → 07-23 再抽(與 CNI 卡同天),過了才推 7。

## 2026-07-23 | 跨 node 走路由表不是 iptables(層級混淆家族)

- 正解:**`ip route`**。判準句「**iptables 管改寫成什麼,路由表管往哪裡送。改寫完之後,封包還是得問路。**」排障尺:跨 node 不通 → 拿目標 Pod IP 去路由表對網段,看那一行在不在、`via` 誰、走哪個 dev。s21 親手驗:`192.168.20.192/26 via 172.21.0.2 dev tunl0 proto bird onlink`(`via`=跨機器、`tunl0`=IPIP overlay、`proto bird`=Calico 的 BGP daemon 自動佈的,不是人寫的)。**此卡是 s20「排障尺」蒸發的直接證據**。**s22 重測未過**:同題再問答「查的是 svc」(第三種錯法,前兩種:iptables、resolv.conf),保姆級提示才到 route table;分工句無法自產,直給後二選一應用題(MASQUERADE 誰做/選介面誰做)2/2 過。病灶更新:**封包出 Pod 後仍用 k8s 物件思考,kernel 只認 iptables 規則/conntrack 表/路由表三樣**。**s24 四抽未過,答「會看 a 的 service, kubectl get svc」= 與 s22 完全相同的錯法,連錯法都不再進化**。加註:該題 `curl PodB-IP` 從頭到尾沒有 Service 參與,學員連「這條路徑上有沒有 Service」都沒判。08-07 五抽,改成兩段問:①這條路徑有哪些元件參與 ②第一個指令。

## 2026-07-23 | kube-proxy 不在 Pod 啟動路徑上

- 正解:Pod 啟動全程 **0 次 ClusterIP**(kubelet 連 kubeconfig 裡的真實 endpoint、拉 image 連 registry 真 IP、CNI 是本機執行 binary 不過網路、掛 volume 是本機檔案系統)。分工句:**「kube-proxy 管的是 Pod 出生之後拿 Service 名字互打那條路;Pod 怎麼出生跟它一點關係都沒有。」** 症狀對照:kube-proxy 掛=現有連線照跑、規則不再更新;CoreDNS 掛=新解析全滅。**s24 首次重抽未過**:答「CoreDNS 嗎」。新病灶命名:**把「kubelet 把 CoreDNS 的 ClusterIP 寫進 Pod 的 resolv.conf」誤當成「啟動過程打過它」——寫進去 ≠ 打過**。08-07 重抽,要求答 0 次 + 講四個啟動動作各自連誰。

## 2026-07-23 | 只給結論不給判準(pattern 卡,升級追蹤)

- 對治句型(每個答案強制):**「我看的是 X,因為 [判準]。」**「因為」後半句就是固定掉分的地方。歷史:s5、s14、s16、s18 scorecard 的「最該改進」都是這一條,s21 升級為獨立卡追蹤。ProServe 加權:顧問工作有一半是在客戶面前 show work,這條在目標職位上是重罪。**s22 混合訊號**:站 7「改 src,因為 Pod A 一開始就不認識 PodB-IP」= 首次無提示自發判準句(正樣本);但站 5 仍裸結論(「查的是 svc」無因為)。**s23 負樣本日**:整堂裸結論(「要開在 allow 上面」等)、AND/OR 的 B 選項後果半句被跳過(教練點名「junior/senior 分界線」),自發正樣本 0,連堂計數重置。**s24 混合**:負面=why-first 預測連跳三次、全堂極簡短答;正面=**「可以,因為直接修改 kernel」與「沒有,因為 CNI 不支援」兩題自帶因為**(pattern 卡第二次出現無提示正樣本,前一次是 s22 站 7)。08-06 續盯,重點改盯**預測題有沒有先講再按 Enter**,不只盯答案裡有沒有「因為」。
- **s26 明顯正向,但出現新形狀**。正面:預測題**全部作答無一跳過**(s24 連跳三次的洞補上);三句無鷹架機制句(「pod 沒有換 container 換掉只有 upperdir 換掉」/「因為路徑存在 container id 底下的資料夾」/ AZ 順序完整鏈)。負面兩處:① **同義反覆**(dry-run 題「因為它不會去查」= 把問題換句話說,已命名並給檢驗法「對方有沒有拿到一個新事實」)② **F 段獨白純結論**(對完全不懂容器的人只丟三個名詞加三句結論,機制要追問才出來)。
- 註:s26 的 EKS 順序題雖自帶「因為」,但屬**當堂剛教 + 教練指定「用順序講」的鷹架下複述,不計入無提示正樣本**。無提示正樣本累計:s22 站 7、s24 kernel 題、s25 PV/PVC 1:1、**s26 upperdir 句**。08-09 續盯,新增盯點=**有沒有同義反覆**。

## 2026-07-17 | default-deny 後的分層(DNS 層 vs 連線層)

- 正解:`curl http://db` 有先後兩步 —— ① 問 CoreDNS(需 egress UDP/TCP **53**)② 建 TCP 連線。default-deny 鎖 egress **連 53 一起鎖**,所以死在第 ① 步,第 ② 步沒機會發生。實證(s16 親手):`curl http://db` → `curl: (28) **Resolving** timed out`;`curl http://192.168.46.66:5678`(餵 IP 跳過 DNS)→ `curl: (28) **Connection** timed out`。**同一條 policy 兩種死法,差別只在需不需要問名字**。prod 陷阱:app log 噴 `could not resolve host` → 全隊衝去查 CoreDNS,但 CoreDNS 好好的,是 policy 封了「去問路的那條路」。故 default-deny 第一個洞永遠是 DNS。**s23 重抽仍未過**(首答「沒辦法跨 pod 溝通」只有結論;「DNS 查詢本身也是 egress 封包」要兩層梯子才到,timeout 種類講不出);但隨後 bastion lab 親手集齊兩死法(deny-all 下 Resolving → allow-dns 上線後 Connection),第一次帶著肌肉記憶離場。留 3,08-06 抽「兩步先後+兩種錯誤訊息關鍵字」。

## 2026-07-28 | veth 誤記「跨 node 連線」

- 正解+封印句:**veth=Pod 自家車道,每 Pod 一條、出門必走**;同 node 2 條(自家出+對方入)、跨 node 也 2 條(tunl0 是高速公路不是 veth);PodB 的 eth0 就是它自己 veth 的另一頭。發音 /viː eθ/。s22 鷹架下收。**s23 冷測過**(6 天留存):數字全對、tunl0 誘答咬住(「兩頭是 pod 跟 root netns」),推 7。但注意:同日盲測 #3 站 2/站 6(veth 的兩次出場)仍蒸發 = 零件會、放回旅程不會,08-10 抽「旅程內出場」版。

## 2026-07-28 | iptables=一棟樓(nat 表/filter 表)

- 正解:**iptables 是一棟樓不是一站:nat 表=改寫部門(DNAT/MASQUERADE),filter 表=查驗部門(felix 編譯的 NetworkPolicy)**。封包全程在樓裡換部門,沒有「出了 DNAT 才進 iptables」。高危:當日教兩次仍複發。**s23 半過**:換皮誘答咬住(「NetworkPolicy 是 CNI 功能但實際改 iptables filter table」,吞餌史終結);但分工句首答「**nat 管路由**」= 層級混淆家族又一新樣本(親戚:查 iptables/查 svc),重教後三表一句(nat 改寫/filter 過濾/路由選路)收。留 3,08-06 抽三表分工一句版 + 部門順序應用(nat 先於 filter → netpol 名單寫 targetPort 5678 不寫 Service port 80,s23 已教未驗)。

## 2026-07-20 | CNI 基本合約 vs 選配

- 正解:合約本體=**網卡、IP、路由**(管「通」,每家 CNI 必做,kubelet 建 Pod 時呼叫);NetworkPolicy 引擎=選配(管「擋」,Calico 有 kindnet 無)。hostNetwork=不蓋孤島直接住 node root netns,故不需 CNI(etcd/apiserver/kube-proxy 照跑=排障訊號「CNI 層壞 vs 整機壞」)。s19 亮點:hostNetwork 判準「需不需要獨立網路」學員自推。07-23 抽三件事+各自缺席的死法。

## 2026-07-19 | 兩張獨立名單(3-2 坑二)

- 正解:A→B 要過兩關(A egress + B ingress),任一關無洞即 timeout;檢查程序=逐關問「這個 Pod 的這個方向名單上有洞嗎」。重測要看主動跑程序,不是背結論。對照:回程免開(conntrack stateful)當天答對。**s23 重抽未過**:「開幾張名單」三層提示(門的比喻、deny-all 也鎖 backend)仍未自產兩道門,學員喊「說明一下」→ 直教兩道門模型。Step 5 兩條 policy(frontend-egress/backend-ingress)s24 學員自寫,寫對+驗收矩陣過 = 動手版過關;口頭版 08-06 再抽。

## 2026-07-19 | NetworkPolicy 靜默無效(四引擎第四行)

- 正解一段話:API Server 只驗 schema 不驗「有沒有引擎」,通過即存 etcd,`get netpol` 查的是 etcd 裡的宣告;沒有支援的 CNI 就沒人把宣告編譯成 kernel 過濾規則,物件永遠只是資料。Ingress 沒引擎=功能壞,使用者馬上叫;NetworkPolicy 沒引擎=安全假象,沒人叫,直到被入侵。**靜默失效比大聲失效危險**。s17 學員零件全掏出但三輪不組裝,喊繼續,冷測要求一段話完整版。**s22 F 段首次質變**:在菜鳥追問(「apply 會報錯嗎?」)下自組完整鏈 — 宣告 vs 引擎(agent/daemon 自答,felix 名字沒到但方向對)+ apply 不報錯 + 「預期 DB 有保護、實際沒有」安全假象自己的話講出。仍帶問題鷹架(追問結構了答案),07-31 一段話冷測版過才 resolved。

## 2026-07-07 | Ingress YAML schema

- 正解:一律 `--dry-run=server`;讀 `ValidationError(路徑)` / `cannot unmarshal ... type X` 定位;對照同檔已寫對的另一條規則照抄結構。

## 2026-07-07 | Ingress 404 排障

- 正解:404 先分層(規則層 vs 後端層);port-forward 是會抖的除錯夾具,不可信就換乾淨再下結論;任何猜測(含教練的)先驗證再採信。07-09 G 段英文重測:方向對但「規則全綠後兇手在哪」連卡兩次、誤猜 nginx-ingress 本身 → 純口頭沒重現,+2 天格重抽。

## 2026-07-09 | no-Host→404 的 why

- 正解三步:① curl 無 -H → Host 自動填 URL 主機名 ② 那串長 DNS ≠ `shop.com` ③ 字串比不上→無規則接→404。對照 `/apiv2`:Host 對但 Prefix 以斜線切段,`/apiv2`≠`/api` 段 → 掉 `/` catch-all → web。口頭型+需鷹架,+2 天格。

## 2026-08-04 | 分層判準:關掉 API Server 還在不在(工具卡,層級混淆家族的解藥)

- 判準:想像 etcd + API Server 被砍掉,node 上的 Pod 繼續跑,**誰還在?** 還在=kernel 的東西(iptables 規則、conntrack 表、路由表、veth/tunl0、cgroup、mount、namespace);消失=etcd 裡的資料(Service、Endpoints、Deployment、Pod 物件、NetworkPolicy 物件、PVC/PV、RBAC、Secret、ConfigMap)。**特例:RBAC 全程活在 API Server 的請求路徑上,kernel 一無所知**(C-4 再打開)。排障 payoff:症狀在 kernel 那欄就別再 `kubectl`,去 node 上用 `ip route` / `iptables-save` / `conntrack -L` / `findmnt`。
- **s25 升級成兩步版(取代單步版)**:**每個 k8s 資源都有兩個分身** —— Service 物件 / DNAT 規則、PVC 物件 / node 上的 mount、`resources.limits` / cgroup `memory.max`、NetworkPolicy 物件 / filter 表規則。**① 先問你講的是宣告還是執行體 ② 宣告在 etcd、執行體在 kernel。** 中間把宣告翻成執行體的是各種 controller/agent(kube-proxy、felix、kubelet)。定調句:**API Server 掛掉 = 沒有新的翻譯了,不是已經翻好的東西消失了。**
- s25 正面:**判準句本身無提示自產**(s24 收工回想答「不知道耶」的洞補上)。負面:首答用兩套詞(1、3 寫 kernel,2、4、5 寫「可以」)導致答案有兩種相反讀法 = pattern 卡「只給結論不給判準」的新形狀。08-08 抽兩步版:給一個名詞先問「宣告還是執行體」,再問住哪層。

## 2026-08-05 | 誰把 limit 寫進 cgroup、什麼時候寫

- 正解:**kubelet**(→ CRI/containerd → runc 實際寫)。判準句:**不在 node 上的元件碰不到 kernel** —— scheduler 只做一件事,從一堆 node 挑一台把 `spec.nodeName` 填進 Pod 物件,**它只改 etcd 的一個欄位,連 node 的門都沒進過**;API Server、controller-manager 同理。回扣 P0 五棒:第 3 棒之後才有人碰得到 kernel,而那個人只有 kubelet 那一路。
- 時機:**只在建立 container 的那一刻寫**,container 活著的期間數字就定死。所以「改了 limit 還是 OOMKilled」的完整診斷:① 改的是宣告 ② `kubectl get deploy -o yaml` 讀回來的還是宣告(等於查自己剛寫的字,證明不了現況)③ 舊 Pod 的 container 沒重建 → kubelet 沒有第二次寫的機會 ④ rollout 卡住的原因很多(quota / PDB / image / paused),但根因形狀只有一個:**宣告改了、執行體沒重生**。排障順序:`kubectl get pod <實際那顆> -o yaml` → 直接讀 node 上的 cgroup。
- L6 顧問版:"Editing the spec only changes the desired state. The limit doesn't reach the kernel until kubelet recreates the container, so I'd check the running pod, not the deployment."
- 延伸(s25 已答對,未單獨建卡):`/sys/fs/cgroup/memory.max` 讀出來是 `67108864` 不是 `64Mi` —— **cgroup 是 kernel 介面,介面只講 bytes**。**實際數字 s25 未讀到(Pod Pending),s26 補驗。**

## 2026-08-05 | LVM 三層 + 擴容四步(學員課後自己要求復習,foundational pull)

- 三層:**PV**(實體卷=一顆磁碟/分割區,被 LVM 徵收)→ **VG**(卷組=多個 PV 合成的池)→ **LV**(邏輯卷=從池切出來、檔案系統蓋在上面的假磁碟)。⚠️ **LVM 的 PV ≠ k8s 的 PV,同名不同物**。存在理由=實體磁碟大小固定、位置固定(分割區起訖寫死),**加一層間接層**,與 PVC↔PV 同手法。
- **擴容四步,一步都不能跳**:`pvcreate` → `vgextend` → `lvextend` → **`resize2fs`/`xfs_growfs`**。第 4 步最多人漏,因為**容量寫在檔案系統自己的 superblock 裡,下面那層變大它不知道**(症狀:`lvs` 變了、`df -h` 沒變)。`lvextend -r` 可一次做完 3+4,但要講得出是兩層。
- **雲上版**:EBS 自己能線上擴容 → LVM「湊出更大空間」的價值被吃掉,EKS 上多半直接 `mkfs` 在 `/dev/nvmeXn1` 上,沒有 LVM 那層。**但第 4 步永遠躲不掉**(EBS 100G→200G 後仍要 `xfs_growfs`,否則 `df -h` 不動)= EKS node 磁碟滿掉最常見的假故障。LVM 在雲上僅存兩用途:多顆 EBS 條帶化衝 IOPS、snapshot 一致性備份。
- **Q2(疊層題,學員答對且自帶機制)**:「k8s PV 底下是 LV,1:1 還成不成立?」→ 成立。學員自產「storage 的寫入沒辦法完美切開,寫到別人的會資料損毀」+ **未經提示自己接到「EKS 上不會靜態宣告 PV,CSI driver 收到 PVC 就生對應的 PV」**。精準版(教練補):**LVM 可以切,但切出來是兩個獨立 LV = 兩個獨立塊裝置 = 兩張 PV,切割發生在 k8s 看不到的下面一層。**
- Q1 順帶收:「EBS 改大重開機就生效?」→ 錯,**要擴的不是磁碟層是檔案系統層**。教練點名這是**「兩個分身」判準第三次換皮出現**(EBS 實際大小 vs 檔案系統以為的大小)。

## 2026-08-05 | PV ↔ PVC 是 1:1 獨佔

- 三層關係:**`StorageClass ─1:多→ PV ─1:1→ PVC ─1:多→ Pod`**。PV 被綁走即整張鎖死,`CLAIM` 欄只寫得下一個名字,多出來的容量誰也拿不走(s25 實證:PVC 要 500Mi,`get pvc` 的 CAPACITY 欄顯示 **1Gi**)。
- **為什麼是 1:1(第一性)**:PV 背後通常是**塊裝置**,檔案系統假設自己獨佔整個裝置(自管 inode/free block/journal),兩個互不知情的 fs 寫同一顆裝置 = 資料毀掉;k8s 這層沒有切割裝置的機制(那是 LVM/分割區的事)。**1:1 不是 k8s 訂的規矩,是塊裝置特性浮到 API 上。** 反之 NFS/EFS 是目錄樹不是塊裝置 → 天生能共用 → 才有 RWX。**能不能 RWX 取決於底層是塊還是檔案系統**(面試點)。
- **RWO 常見誤解**:RWO 限制的是 **node** 不是 Pod 數,同一台 node 上排十顆都掛得到。
- 實務註記:靜態供給才會有「1Gi 配 500Mi 浪費」的問題;動態供給(EKS + EBS CSI)PVC 要多少就開多少,結構上不存在。s25 Transfer 已過(含「因為」),**當堂過不算保留**,08-08 冷測。

## 2026-08-04 | container 可寫層在硬碟不在 memory(overlayfs 三層)

- 正解:container 的 `/` 是 kernel 用 overlayfs **疊**出來的,不是一顆真磁碟。`lowerdir`=image 的 N 層,唯讀,**所有用同 image 的 container 共用**;`upperdir`=可寫層,**每個 container 自己一層**;全部實體位置在 node 的 `/var/lib/containerd/...`(硬碟)。消失的原因不是 memory,是 **upperdir 綁在 container 上,container 一刪那層陪葬,image 層留著給下一個用**。s24 親手驗:寫檔 → `kill 1`(送 SIGTERM 給 PID 1 = 模擬 crash,Pod 不動)→ 名字 IP 不變、RESTARTS+1、`cat: can't open`。三個延伸面試點(100 個 Pod 不佔 100 份 image / 啟動快 / Dockerfile 裡 rm 不會讓 image 變小)當堂教,未抽。
- **s26 二度實證且機制自產**:`crictl stop` 換 container → `/root/f.txt` 消失,同時 emptyDir / PVC 兩層都活。學員無鷹架講出「**pod 沒有換,container 換掉,只有 upperdir 換掉**」,F 段追問下再產「**因為路徑存在 container id 底下的資料夾**」。精準版補完:**不是有人跑去刪那個檔案,是新 container 拿到一個全新的空 upperdir,舊那層跟舊 container 一起被丟掉。** 推 7,08-13 冷測連同三階梯一起抽。

## 2026-08-04 | emptyDir 綁 Pod 不綁 container

- 正解:**撐得過**。路徑判準最好記 —— 可寫層在 `/var/lib/**containerd**/.../snapshots/<id>/`,emptyDir 在 `/var/lib/**kubelet/pods/<pod-uid>**/volumes/`,**路徑裡就寫著它綁誰**。`kill 1` 換 container、Pod uid 不變 → emptyDir 還在;`delete pod` uid 消失 → 才沒。生產坑:`emptyDir: {medium: Memory}` 是 tmpfs 且**算進 Pod 的 memory limit**,往 `/dev/shm` 猛寫會 OOMKilled(看起來在寫檔,實際在吃 cgroup 配額);真實用途三個:Secret volume 本身就是 tmpfs(不落盤)、`/dev/shm` 預設只有 64Mi 要加大、暫存 scratch。**s25 必須動手驗**(口頭已錯一次,直給後沒接動手 = 依 s16 實證會蒸發)。
- **s26 動手驗過,翻正 ✅**:一顆 `vol-demo` Pod 三層同掛,`crictl stop` 換 container → emptyDir 檔案還在;`delete pod` → 沒了。機制自產「pod 沒有換 container 換掉只有 upperdir 換掉」,精準版補完「沒換的是 Pod UID」。推 7,08-13 冷測(問法:emptyDir 撐得過什麼、撐不過什麼、路徑判準)。

## 2026-08-06 | 排障:restart 排在採證前面(MTTR / 治標 vs 治本第三次同形狀)

- 正解:**採證(A/B)一定排在清理現場(C)前面**。restart/reboot 修的是症狀,而且把根因證據一起洗掉。學員自己的歷史就是證明:s21 倒 → restart → 好了 → 沒人知道為什麼;s24 倒 → 沒處理;s25 倒更慘 → 沒跑;s26 宿主機重開機 → 好了 → **s25 那次的真兇永遠查不到**。四次倒下,四次從零猜。
- 判準句:**能重現的東西可以晚點修,不能重現的東西必須當場採證。**
- L6 顧問版:"A restart clears the symptom and the evidence at the same time. I'd capture node conditions and kubelet logs first, then restart — otherwise the same incident comes back next week and we're starting from zero."
- 08-09 抽:給一個 node NotReady 情境,要他排出「先做什麼、再做什麼」的順序 + 講出為什麼 restart 不能第一個。

## 2026-08-06 | PID 1 的 signal 保護(kernel 層,新知識卡)

- 機制:**Linux kernel 對 PID 1 有特殊保護 —— 一個 signal 若沒有安裝 handler,PID 1 收到時不套用「預設動作」,直接忽略。** 一般 process 收 SIGTERM 無 handler = 終止;PID 1 = 什麼都不發生。原因:PID 1 是 init,init 死掉整個 PID namespace 崩掉。**這個保護連 SIGKILL 都算,只要 signal 來自同一個 PID namespace 內部**;只有祖先 namespace(node 那層)送得進去。s26 實證:`docker exec <node> crictl stop $(crictl ps -q --label io.kubernetes.pod.name=vol-demo)` 才殺得掉。
- 本例 PID 1 是 `sleep`,從不註冊 SIGTERM handler,所以 signal 被丟掉。(s24 net-tool 的 `kill 1` 有效 = 那顆 image 的 PID 1 不同,不是矛盾。)
- **三個生產對應(面試高頻)**:① `kubectl delete pod` 每次都等滿 30 秒 = kubelet 送 SIGTERM 被忽略 → 等 `terminationGracePeriodSeconds` 到期 → 從外面送 SIGKILL。② 每次 rollout 斷線 / 交易沒寫完 = app 從沒收到 SIGTERM,沒機會 graceful shutdown。③ Dockerfile 用 shell form(`CMD npm start`)→ PID 1 變 `/bin/sh`,**sh 不轉發 signal 給子行程** → 解法是 exec form(`CMD ["node","server.js"]`)或塞 `tini`/`dumb-init` 當 PID 1 負責轉發與收屍。
- 08-09 抽:「為什麼你的 Pod 刪除總是要等 30 秒?」+ 「同一個 container 裡 `kill -9 1` 殺不殺得掉?為什麼?」

## 2026-08-06 | Pod 不會「重啟」,只會被丟掉重建

- 正解:**Pod 沒有「重啟」這回事,它只會被丟掉、由 controller 生一顆全新的(新 UID)。** `RESTARTS` 那一欄數的是 **container** 的重啟次數,不是 Pod 的。學員自己 s26 的輸出就是證據:`RESTARTS 1 (5s ago) AGE 7m33s`(container 換了 Pod 沒換)vs delete 後 `AGE 3s`(全新 Pod)。
- **五種不需要任何人動手、Pod 就會消失的情況**:① node 掛掉/失聯 >5 分鐘 → node-lifecycle controller 標記刪除 ② node 記憶體或磁碟不足 → **kubelet 主動 evict** ③ `kubectl drain`(升級/縮容)④ 高優先級 Pod 進來 → scheduler **preemption** ⑤ HPA 縮容 / 任何一次 rollout。
- 定調句:**Pod 是牲口不是寵物(cattle, not pets)。你不刪它,叢集隨時會替你刪。** 推論:emptyDir 的正確定位只有 scratch space(快取、暫存、`/dev/shm`),跟你手不手動刪 Pod 無關。
- 08-09 抽:「不刪 Pod 的話,emptyDir 就安全嗎?」要他數出至少三種自動消失情境。

## 2026-08-06 | 持久性看「掛在哪」不看名字(兩個分身判準第四次換皮)

- 成因:kind 的 node image 把 `/tmp` 設成 tmpfs,而 `pv-demo` 的 hostPath 是 `/tmp/pv-demo` → 這張「持久卷」的實體是記憶體,node 一重開就沒。
- 封印句:**持久性由「它實際掛在什麼東西上」決定,不是由物件的名字決定。別信名字,去讀 `/proc/mounts`。**
- 這是 s24「可寫層存在 memory 就消失了」誤解的**鏡像**(那次是該在磁碟的以為在記憶體;這次是號稱持久的真的在記憶體)。兩次共同教訓同一句。
- 生產對應:`emptyDir: {medium: Memory}` 明著要 tmpfs,而且**算進 Pod 的 memory limit** —— 往 `/dev/shm` 猛寫會 OOMKilled,現象是「在寫檔」真相是「在吃記憶體配額」。s26 已親眼看過 tmpfs 在 `/proc/mounts` 的長相。
- 08-09 抽:給一個 PV YAML,問「這個 PV 是不是持久的?你怎麼確定?」(要答:看 hostPath/CSI 底下掛什麼,不是看 kind)

## 2026-08-06 | EKS 儲存拓撲:EBS AZ-scoped / nodeAffinity / volumeBindingMode(**學員主動提問引出**,ProServe 高權重)

- 第一性原理定調句:**儲存有位置,計算沒有。** scheduler 預設只看計算條件(資源/taint/affinity);一旦儲存進場,**位置必須被寫進 API 物件,否則 scheduler 一無所知**。
- 三方案對照:**hostPath** 位置沒寫 → scheduler 隨便排 → 資料「不見」(只能玩 lab);**local** volume 強制要求 `nodeAffinity`;**EBS CSI**(EKS 正解)由 driver 自動把 `topology.ebs.csi.aws.com/zone=<az>` 寫進 PV 的 `nodeAffinity` → Pod 只會排到那個 AZ。
- **`volumeBindingMode` 是第二層坑**:`Immediate`(預設)= PVC 一建立就在某 AZ 開好 EBS,Pod 後到若有別的限制 → `volume node affinity conflict` **永遠 Pending**(症狀很賊,新手去查 taint,根因是 StorageClass 少一行);**`WaitForFirstConsumer`** = 先讓 scheduler 決定 Pod 去哪,再在那個 AZ 開 EBS。**順序倒過來就對了。**
- 跨 AZ 共用只能 **EFS**:EBS 是塊裝置(fs 假設獨佔 → RWO、單 AZ),EFS 是 NFS 目錄樹(天生 RWX、跨 AZ)。回扣 s25 已收的「能不能 RWX 取決於底層是塊還是檔案系統」。
- 實務取捨:StatefulSet + EBS 的 Pod 被釘在 AZ,該 AZ 掛了就起不來 —— 這是**刻意接受**的設計,高可用交給 app 層跨 AZ 複製(Kafka/Cassandra/etcd),不是交給儲存層。
- L6 英文版:"EBS volumes are AZ-scoped, so the CSI driver stamps the zone into the PV's node affinity and the scheduler honours it. If you need shared access across AZs, that's an EFS conversation, not an EBS one."
- 08-09 換情境冷測(禁用「三個 AZ + Immediate」原題)。

## 2026-08-20 | 判準給完當場套用不上(pattern 卡,教學法層級)

- 對治規格(s29 起執行):**每給一個判準句,立刻接一題只有換皮的應用題,答對才算給完。** 不要等隔堂冷測才發現沒套用 —— 隔堂測的是留存,當場測的是「有沒有真的接收到」。
- 這條與既有的「只給結論不給判準」是**同一家族的兩端**:一端是講不出判準,一端是拿到判準不會用。兩端都通了才算會。

## 2026-08-28 | StatefulSet 每個 replica 一份獨立資料(不是共用一份)

- 正解:**5 份**。`volumeClaimTemplates` 給每個 ordinal **自己一顆空 PVC** → Pod 起來時 Redis process 掛到一個**空目錄** → 自己開一份新資料集。`redis-0/1/2` **從第一天起就是三個互不相識的 Redis**,不是「原本同步、後來沒跟上」。
- 判準句:**StatefulSet 給的是「每人一份儲存」,不是「大家共用一份資料」。複製(`replicaof` / streaming replication)是 application 自己的設定,k8s 從頭到尾沒碰過。**
- 學員自己講對的半邊(要保留):「不會 sync」正確 —— 但原因不是「新的沒跟上」,是**從來沒有人叫它們 sync 過**。
- 換皮應用(當堂已過):普通 ClusterIP 選到 5 顆 → `SET user:1` 到 server 1、`GET user:1` 打到 server 2 → 找不到。**機制這關過了,數量這關沒過。**
- L6 顧問版: "StatefulSet gives each replica its own identity and its own empty volume. It never configures replication — that's the database's job. Five replicas means five independent datasets until something inside Redis is told to replicate."
- 09-04 抽:換 Kafka 或 Elasticsearch 皮,問「N 個 replica 有幾份資料 + 誰負責讓它們一致」。

## 2026-08-28 | 排障兩步:先鎖 fault domain 再查內部(MTTR 核心卡)

- 判準句:**先鎖「流量打到幾個東西」,再查「那個東西內部怎麼了」。順序反過來,你會拿著單一顆的狀態去解釋一個分散問題。**
- 為什麼 B 先:症狀「寫入成功、讀取 miss」有兩個嫌犯 —— (1) 流量被打散到多個獨立實例 (2) replication 有設但壞了。`endpointslice` **一發同時鎖死 fault domain**(5 個 address = app 每次可能連到不同一顆);`info replication` 只看得到一顆,而且客戶可以合理反駁「那只是 redis-0 特別而已」。鎖完 domain 再用 C 確認根因。
- 指令:`kubectl get endpointslice -l kubernetes.io/service-name=<svc> -o wide`
- L6 顧問版: "Writes succeed and reads miss — that's a fan-out symptom, not a process symptom. My first check is the endpointslice: if the Service resolves to five addresses, the app is talking to five independent instances, and that alone explains it. Then I'd confirm with `info replication`. I want the fault domain before the internals."
- 這張卡與既有的「產生者 vs 消費者」「對照組判準」同屬**選第一發指令**家族,學員八堂以來的最大缺口。
- 08-31 抽:換第三種皮(建議 Elasticsearch 或 MySQL read replica),要學員**先講出「我這一發回答的是第 1 步還是第 2 步」**再給指令。
- **s32 第三次同形狀(2026-08-28)**:剛給完「先鎖 fault domain 再查內部」的兩步判準,**下一題換皮 Postgres 立刻又答「檢查 replicas 的 log」= 第 2 步**。梯子問「這是第幾步」後能正確複述順序,再給三選一才挑到 B。**證實診斷:不是記不住,是不會把剛拿到的判準當工具用。**
- **加碼規格(s33 起)**:排障題不直接問「第一發是什麼」,先強迫學員答「**我這一發回答的是第 1 步還是第 2 步**」,答完才給指令選項。把「用一次」變成強制動作,不是期待他自己想到。

## 2026-09-01 | 建 Pod 的權限 vs Pod 裡程式呼叫 API 的權限(誰用誰的身分)

- 正解:Pod 會正常建立、`Running`。建 Pod 是 kube-controller-manager 裡的控制器用**它自己的系統級身分**做的,跟 CronJob 宣告的那個 SA 完全無關;那個 SA 只在 **Pod 裡的程式自己呼叫 API** 時才用得到。比喻:建 Pod 像 HR 幫新人辦入職,不需要新人自己的識別證;403 發生在員工已經到職、自己拿識別證開某個門的那一刻。
- 判準句:**「誰建立」跟「誰呼叫」是兩個不同的身分,不要因為兩件事都跟同一個物件(Pod/SA)有關就假設是同一個人做的。**
- 09-04 抽:換皮(e.g. Deployment 的 SA 權限不夠,新副本會不會建立失敗)看是否自產「controller 用自己身分建物件,app 用宣告的 SA 呼叫 API」這條分工句。

---

## Queue notes(原本掛在 spaced-repetition queue 行尾的括號註記)

<!-- 這些是 2026-09-02 拆檔前寫在 queue 每一行括號裡的重測歷史,原文保留。
     新的重測紀錄請寫到上面對應的卡片節,不要再寫回 queue。 -->

- **mistake:YAML-validation**:**s25 讀圖 rep 首次自己過**:`unknown field "spec.sccessModes"` 自行定位改對;但同段跳過自寫 PVC,rep 打折不推 7。08-08 換 `cannot unmarshal` / enum 大小寫型再測
- **mistake:ImagePullBackOff**:**s26 真場景現形但 rep 不算數**:三選一答 C 正確,要了兩次沒貼 Events 關鍵字,且答案是我先告知才猜得到 → 不推 interval。08-09 換學員不知情的故障〔401 或 i/o timeout 型〕,要求先貼 Events 再分類
- **mistake:dry-run-兩層**:**s26 分界線親手做出來**〔dry-run 綠燈 → apply → ImagePullBackOff〕但判準是**同義反覆**,精準版未收。抽:誰知道 image 存不存在、在第幾棒。歷史:s16 未口頭抽,但**真場景實用一次**:自寫 default-deny 用 `--dry-run=server` 抓到自己的 apiVersion 錯並讀懂 `no matches for kind ... in version` → 工具已進肌肉,精準版仍未收
- **mistake:三分類-家族卡**:**s18 counter 1/3**:零流量思想實驗全對、conntrack 站對「狀態」;第 2 輪換家族成員
- **mistake:L4-vs-L7**:**s18 新情境過但框架教練給**:postgres/redis 兩題連過、標籤貼反未重現;07-22 無框架第四情境〔禁 postgres/redis〕過了才推 7
- **mistake:NetworkPolicy-出廠全通**:s20 重抽半過:結論靠提示、「podSelector 只在自家 ns 選人」why 沒站住;與 CNI 卡同天再抽
- **mistake:default-deny-分層(DNS vs 連線)**:**s23 口頭再未過**但 lab 兩死法親手集齊;抽「兩步先後+兩種 timeout 關鍵字」
- **mistake:跨-node-走路由表**:**s27 動手驗完成,s26 的債還清**:親手 `docker exec k8s-coach-p2a-worker ip route` 讀到 `192.168.20.192/26 via 172.21.0.4 dev tunl0 proto bird onlink`,三欄意義已教。**但 A/B/C 預測未答即按 Enter,rep 打折不推 7**。08-13 抽:那一行三個欄位各是什麼意思 + 為什麼要包 tunl0〔底層網路不認 Pod 網段〕+ EKS VPC CNI 為什麼不需要 overlay
- **mistake:blackhole路由與本機/32**:s27 意外彩蛋,**教練直給未抽考**:`blackhole <本機 Pod 網段>` + 本機 /32 `dev cali` 全缺 = 沒有 Pod 在跑的獨立證據。抽:blackhole 存在的理由〔無對應 Pod 的封包當場丟掉,否則走 default gw 繞回成迴圈〕
- **mistake:跨-node-走路由表-舊記錄**:**s26 直給正解、學員未動手**:已給「路徑上 CoreDNS/Service/kube-proxy 各零次」+ 七段 kernel 路徑 + `ip route` + 判準句,三選一預測題未作答即改議程。⚠️ 依學員自身資料「直給+無動手」必蒸發 → **s27 開場先動手 `docker exec k8s-coach-p2a-worker ip route` 讀那一行**,跑完才算有 rep
- **mistake:分層判準-關掉APIServer還在不在**:**s25 冷測 4/5**:判準句無提示自產 ✅、cgroup limit 誤放右欄 ❌。已升級成**兩步版**〔先問宣告還是執行體〕,08-08 抽兩步版
- **mistake:誰把limit寫進cgroup(kubelet不是scheduler)**:s25 新卡,答「scheduler 嗎」;判準句「不在 node 上的元件碰不到 kernel」+ 只在建 container 那刻寫
- **mistake:LVM三層+擴容四步**:s25 課後學員自己要求復習;兩題結論對但都只給結論,Q2 追一刀後機制自產並自接 EKS CSI。抽:三層各是什麼 + 擴容四步 + 為什麼第 4 步躲不掉
- **mistake:PV↔PVC是1:1獨佔**:s25 新卡,學員自曝以為 1:多;三層關係 + 塊裝置第一性 + RWO 限的是 node。Transfer 當堂過,冷測定升降
- **mistake:可寫層在硬碟不在memory(overlayfs)**:**s26 二度實證 + 機制無鷹架自產**「只有 upperdir 換掉」,推 7
- **mistake:emptyDir-綁Pod不綁container**:**s26 動手驗過翻正**:crictl stop 檔案在、delete pod 檔案沒,推 7。連同三階梯一起抽
- **mistake:restart排在採證前面(MTTR)**:**s28 過**:四選項排序 `reboot` 排最後,B/C 順序給成本對比後自己改對並自帶判準「比較簡單」。s21 以來第一次真的做對,推 7。歷史:**s27 真現場大幅正向但只算半過**:五次故障以來第一次採證完成才 restart,完整證據鏈成立〔conditions → 宿主機 → 對照組 → systemctl → kubelet log〕。**但每一發指令都是教練指定的,學員零自選** —— 順序學會了,選指令那一步沒動。不推 7。08-13 抽:給一個新的 node NotReady,要學員自己說出頭三發指令
- **mistake:scheduler當萬用嫌犯**:**s27 第 2 次**〔s25「誰把 limit 寫進 cgroup」→ 答 scheduler;s27「node NotReady 你要看哪個東西」→ 答 scheduler〕。判準句合併:**scheduler 只填 `spec.nodeName`,它是狀態的消費者不是產生者,而且從沒進過 node 的門**。抽:換第三個情境〔e.g. Pod 卡 ContainerCreating〕看還會不會答 scheduler
- **mistake:產生者vs消費者(排障找誰)**:s27 新卡,**教練直給未抽考**。`NotReady` 兩種產生者:`Ready=False`=kubelet 活著自己回報〔message 寫死因〕、`Ready=Unknown`=kubelet 失聯 40 秒 controller-manager 代筆,**看 `reason` 欄分辨**。抽:兩種怎麼分 + 為什麼不該問消費者
- **mistake:對照組判準(同層有好有壞)**:**s28 首抽半過**:ALB 三台兩壞情境,認出證據句「第三台完全正常」✅,判準句答不出喊「直接説明」;直給後的應用題**立刻選查 ALB access log = 剛砍掉的那層**。留 3,換第三種皮再抽。歷史:s27 新卡,**教練直給未抽考**。同一宿主機三台 node、worker2 Ready 另兩台 NotReady → 整個宿主機層一次排除。通用句:**同一層裡有的好有的壞,那一層以下全部無罪**。抽:換一個非 k8s 情境〔e.g. 三個 ECS task 一個正常〕看會不會用
- **mistake:active≠還在幹活(健康檢查三層)**:**s30 再未過**:`active` 首答成「程序正常」；已拆成 systemd unit active / socket listener / CRI 真回話三層並完整重教，尚未經無提示換皮驗收。s28 首抽亦未過。抽:`active` + socket exists + `crictl info` timeout，各層通過/失敗為何
- **mistake:DeadlineExceeded語義**:**s28 過**:二選一「不在家 vs 在家不接電話」答對「在家但是不接電話」,推 7。歷史:s27 新卡,**教練直給未抽考**。`DeadlineExceeded` = 對方還在但不理你;connection refused = 對方不在。**兩種病相反、查法相反**,回扣 CA session 已有的 refused-vs-timeout 卡〔跨 coach 同形狀,見 workspaces/ca〕。抽:兩個症狀各該先查哪一邊
- **mistake:PID1-signal保護**:s26 意外實證,`kill 1` 殺不死 container。**全程教練驅動未經抽考**。抽:Pod 刪除為什麼等 30 秒 + 同 namespace 內 `kill -9 1` 殺不殺得掉
- **mistake:Pod不會重啟只會被丟掉重建**:s26 F 段盲點,答「pod 會重啟 or 調節 編排」。抽:數出至少三種不需人動手 Pod 就消失的情境
- **mistake:持久性看掛在哪不看名字(tmpfs)**:s26 `/proc/mounts` 意外:emptyDir 在 xfs、PVC 在 tmpfs。兩個分身判準第四次換皮
- **mistake:EKS儲存拓撲(EBS AZ/nodeAffinity/volumeBindingMode)**:s26 學員主動提問引出;Transfer 過但屬當堂鷹架下複述。08-09 換情境冷測
- **mistake:veth-誤記跨node連線**:**s23 冷測過**:數字全對+tunl0 誘答咬住,推 7;但同日盲測站 2/6 仍蒸發,08-10 抽「旅程內出場」版
- **mistake:iptables-一棟樓**:**s23 半過**:換皮誘答咬住=吞餌史終結;但「nat 管路由」新錯法,重教後收。抽三表分工一句版+targetPort 5678 應用
- **mistake:kube-proxy-不在-Pod-啟動路徑**:**s24 首次重抽未過**,答「CoreDNS 嗎」= 寫進 resolv.conf ≠ 打過它
- **mistake:判準給完當場套用不上(pattern)**:**s32 第三次同形狀**:剛收到兩步判準,換皮題立刻又跳內部;梯子後能複述順序。加碼規格:排障題先問「我這一發是第 1 步還是第 2 步」再給指令選項。歷史:s28 新卡,同堂兩次
- **mistake:StatefulSet每個replica一份獨立資料**:s32 新卡,答「still is 3 data」。`volumeClaimTemplates` 給的是**空** PVC;複製是 application 的事。抽:換 Kafka/ES 皮問 N 個 replica 幾份資料 + 誰負責 sync
- **mistake:先鎖fault-domain再查內部(MTTR)**:s32 新卡,同堂兩次先跳內部。指令 `kubectl get endpointslice -l kubernetes.io/service-name=<svc> -o wide`。抽:換第三種皮,先問「第 1 步還是第 2 步」再給指令
- **mistake:只給結論不給判準(pattern)**:**s33 同一堂連中兩次**:C-4 四象限第三/四格問答,先答「不行的」「可以的」都要教練追問才補理由,最終補出的判準是對的(範圍/存在的機制),但預設反應仍是先吐結論。**s32 正樣本第 6 次**:MTTR 第一題無提示自帶完整句型「寫入成功 + 全 Running + RESTARTS 0,**所以**我看資料層」,推理方向正確,錯的是選指令不是想法;同堂另有「pod 層級 scale 不是服務層級 HA」分層判準。歷史:**s30 再現**:Proxy 換皮只答 `B`、RWO 題兩次只答「不能」，都需句型鷹架才補出判準；正樣本是後段能完整說出 bypass 對照只能鎖定整段路徑。留 3，下一次答案固定要求「判斷+因為+證據」
- **mistake:建Pod的權限vs呼叫API的權限(誰用誰的身分)**:s33 新卡,答「不會,因為根本沒有到建立 pod」。判準句:建立是 controller 自己的身分、呼叫是 Pod 裡程式的 SA。抽:換皮 Deployment 版
- **mistake:NetworkPolicy-靜默無效**:過期,s23 未抽;**s22 F 段質變**:追問下自組完整鏈含「安全假象」自己的話;一段話冷測版過才 resolved,s24/WR9 抽
- **mistake:CNI-合約三件事**:s19 新卡:網卡/IP/路由 + 各自缺席的死法;hostNetwork 判準已自推不用重考
- **mistake:兩張獨立名單**:**s23 重抽未過**,三層提示未自產、直教兩道門模型;s24 動手版〔Step 5 自寫兩條 policy + 矩陣〕+ 08-06 口頭版
- **term:conntrack**:**s18 分工句收**:骨架〔規則管第一次、conntrack 管之後〕自產,應用一次追問補全〔去程改 Destination/回程改 Source、都查 conntrack〕;07-26 抽完整版〔兩個詞+分工句+查誰〕過即封印。歷史:s16 兩個詞給框架後自產;s15 直給後 3 天蒸發=「給框架 vs 給答案」對照組證據
- **mistake:probe-職責**:**s30 半過**:readiness 失敗不 restart、退出 Service 流量答對；liveness 先答重啟整個 Pod，拆小後能說清只重啟失敗 container、Pod UID/sidecar 不變、`restartCount` 為 container 級。當堂重教不推 interval；換皮冷測「container vs Pod」

### 拆檔前留在 queue 區的註記

<!-- 2026-07-16 移除兩張 +2 天口頭卡(404-排障-port-forward=parked、no-Host-404-why=resolved):過 ROI 篩不過 Q1,見 teaching-elements.md「ROI 篩」。 -->

## 2026-09-03 | RWO 的 Once 數的是 node 不是 Pod

- 正解:`ReadWriteOnce` 限制的是**一個 node** 可讀寫掛載;**同一台 node 上多顆 Pod 可以一起掛同一個 RWO volume**,完全合法。要限制到單一 Pod 是 `ReadWriteOncePod`(1.29 GA)。
- 判準句:**RWO 的 "Once" 數的是 node,不是 Pod。要數 Pod 得用 ReadWriteOncePod。**
- 排障 payoff:5 顆 Pod 共用一個 RWO PVC,若 scheduler 剛好全排到同一台 node,**k8s 層不會擋**,直接進資料損毀。擋你的是運氣不是 API。
- 歷史:s25 已教過此點(「RWO 限制的是 node 不是 Pod 數已教」),s34 誘答題回退。09-06 抽:給「5 顆 Pod 共用一個 RWO PVC」情境,要求答出「什麼情況下 k8s 不會擋」。

## 2026-08-31 | 先鎖 fault domain 再查內部(MTTR)

- **s34 換皮首次通過**(s30 選 `describe pod`、s32 選「查 replica log」,同形狀連兩敗)。題目:checkout-api 3 replica / 3 node / ALB,5xx 從 0.1% 跳到 **33%**,p99 180ms→9.5s,3 顆全 Running RESTARTS 0,ALB target 全 healthy,24h 未 deploy。四選一答 **B(bypass ALB 與 Service 直打三顆做對照)✅**,而且**「33% 剛好是 1/3」的判準無提示自產**。
- 附帶收(A 選項的排除理由不成立,已當場補正):學員說「最近沒 deploy 所以砍掉看 log」= 錯的理由。正解:`kubectl logs deploy/x --tail=200` 的 `--all-pods` **預設 false**,撈的是 kubectl 隨機挑的**一顆**,且無 `--prefix` 連是哪顆都不顯示 → 33% 壞掉時**有 2/3 機率撈到健康那顆**,得出「應用層沒問題」的假結論。
- 新判準句:**有對照組價值的症狀,第一發不能用「會混樣本或隨機抽樣」的指令。`logs deploy/` 是抽樣,`logs -l app=x --prefix --all-pods` 才是普查。**
- 推 3 → 7,09-10 換皮再抽(建議換成「9 顆 replica、5xx 11%」型,考他會不會算出 1/9)。

## 2026-07-23 | 跨 node 走路由表不是 iptables(五抽首次通過)

- **s34 通過**。改用 mistake-notes 早就寫好的兩段問法:①這條路徑有哪些元件參與 ②第一個指令。
- 第 1 段:自答 `veth pair / tunl0 / route table / eth0` —— **五次以來第一次沒有跑到 iptables、resolv.conf、Service 去**(前四次錯法:iptables、resolv.conf、查 svc、kubectl get svc)。
- 唯一錯:順序把 `tunl0` 排在 `route table` 前面。一句追問「誰決定這個封包走 tunl0 不走 eth0」→ **自答 route table**,順序修正由學員自己做。
- 第 2 段:先給模糊的「看 route table？」,**自己收斂成 `ip route get 192.168.1.42`**。
- 補完的鏈(學員缺對面那一半 + filter table):Pod A eth0 → veth → root netns → route table 命中 `192.168.1.0/24 via <worker> dev tunl0` → tunl0 IPIP 封裝 → node eth0 → 對面 node eth0 → 對面 tunl0 解封裝 → 對面 route table → 對面 iptables filter(felix 的 NetworkPolicy)→ 對面 veth → Pod B eth0。
- 封印句:**iptables 管「改寫成什麼」,route table 管「往哪裡送」。tunl0 不是自己跑出來的,是 route table 那一行的 `dev` 欄位指定的。** 推 3 → 7,09-10 冷測第二次(過了才 resolved)。

## 2026-09-04 | StatefulSet 每個 replica 一份獨立資料

- **s34 換皮通過**(s32 答錯:「5 個 replica = 幾份資料」答 3)。題目:mysql StatefulSet,`volumeClaimTemplates` 20Gi,`replicas` 3 → `kubectl scale --replicas=5`。三問全對:**5 個 PVC / 100Gi / 新的兩顆沒有 mysql-0 的資料 / 一致性由 MySQL 自己的 replication 負責,不是 k8s**。
- 誘答(改成 5 顆共掛一個 100Gi PVC)**沒吞**:機制答「同時修改一份 data 會衝突」✅;但 k8s 層那半答錯(RWO 記成 Pod 層),另立卡見 `2026-09-03 | RWO 的 Once 數的是 node 不是 Pod`。
- 推 3 → 7,09-10 抽:換成「誰負責讓 mysql-3 追上 mysql-0 的資料」的顧問版問法。

## 2026-09-04 | 判準跑錯軸:RBAC 題答成 NetworkPolicy

- 題目:Role/RoleBinding 在 `rbac-lab`、ServiceAccount 在 `ci-system`,`subjects` 寫 `namespace: ci-system`。三選一問讀不讀得到 `rbac-lab` 的 Pod。
- 學員答 **A(讀得到)= 結論正確**,但理由是「namespace 只是邏輯隔離不是實際網路隔離,要使用 NetworkPolicy」—— **整個跑到另一條軸上**,而 s33 chunk 1 才剛教過「物件存在範圍」與「網路隔離」是兩個獨立軸。
- 拆法(有效,可重用):**要學員用自己 s24 造的分層判準回答兩個小問** ——「NetworkPolicy 的執行體在哪?」→ 自答 `iptables`;「RBAC 的執行體在哪?」→ 自答 `API Server`。兩問皆無提示答對,錯軸當場自己看見。
- 正解三條線:① `roleRef` 只能指向同 ns 的 Role ② `subjects` 是純字串比對名單,可跨 ns,名單上的 SA **不存在也照樣 apply 成功** ③ 生效範圍 = RoleBinding 所在的 ns。
- **封印句:subject 住哪不重要,RoleBinding 住哪才決定權限開在哪。**
- 反直覺 payoff:`ci-system/ci-reader` 拿到的是「讀 rbac-lab 的 Pod」,回自己家 `ci-system` 反而一顆都讀不到。所以 CI 吃 403 時「把 SA 搬到目標 ns」是白做工。
- 圖解頁:https://claude.ai/code/artifact/5a0f989c-a7f4-4668-bb7a-f5fa07b5d076
- 09-07 抽:換皮問「RoleBinding 在 A ns、Role 在 B ns」會怎樣(考 roleRef 那條線),要求先講執行體在哪一層再答。
