# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 24
- last_weekly_review: 18
- last_session_date: 2026-08-04
- warm_up_classification: mid(有地圖形狀,缺演員名字;P0 剛好,不加速)
- **target_role: AWS Delivery Consultant(ProServe),2026-07-23 學員確認**。全部抽考包成客戶顧問情境、每題附 L6 範例答法(memory `aws-delivery-consultant-target` / `aws-mock-and-l6-answer-format`);戰略重排見 curriculum-plan §9。

## Current Session breakpoint

**s24 已收(2026-08-04,公司 bastion,context `kind-k8s-coach-p2a`)。P2b 開跑,C-1 第一階親手拆完(overlayfs 可寫層);A 段兩張過期卡雙雙未過;中段被叢集環境故障吃掉一大段。F/G 連四堂未跑(本堂學員下班收工,非跳過);story-bank 連四堂未挖。**

本堂事實:

- **A 段兩題全未過**。① kube-proxy 不在 Pod 啟動路徑(07-26 過期):答「CoreDNS 嗎」= 把「kubelet 把 CoreDNS ClusterIP **寫進** resolv.conf」誤當成「啟動過程**打過**它」。② 跨-node-走路由表(07-31 過期):答「會看 a 的 service, kubectl get svc」= **第四種錯法,且與 s22 完全相同**(史:iptables → resolv.conf → 查 svc → 查 svc)。當場合併診斷:兩題都用 k8s 物件回答 kernel 的問題。
- **新工具卡「關掉 API Server 還在不在」**(教練當堂造,對治層級混淆家族)。左欄 kernel 真東西(iptables/conntrack/路由表/veth/cgroup/mount/namespace)vs 右欄 etcd 資料(Service/Deployment/PVC/NetworkPolicy/RBAC/Secret)。**學員 3/3 過**,其中第三題「沒有,因為 CNI 不支援」與追加 Transfer「Calico 上 apply 完關掉 API Server 擋不擋得住 = 可以,因為直接修改 kernel」**皆無提示自答**,是本堂最硬的正樣本,也是靜默無效卡的鏡像驗證。RBAC 特例(完全不在 kernel)已埋,C-4 再開。
- **C-1 第一階親手拆完(可寫層)**。誤答「存在 memory 就消失了」= 結論對機制錯(pattern 第七堂)→ 直給正解 + 親手驗:`kubectl exec net-tool -- cat /proc/mounts | grep -w overlay` 讀出 lowerdir 15 層(image,共用)/ upperdir 212(可寫,獨有)/ 全部在 `/var/lib/containerd`。接著寫檔 → `kill 1` → **三個預測全中**(名字 IP 不變、RESTARTS 11→12、檔案消失)。封印句:**同一個 Pod,`kill 1` 換掉的是 container,新 container 拿到全新空 upperdir**。順帶收三個面試點(image 共用 / 啟動快 / rm 不會變小)。
- **emptyDir 第二階口頭未過**:問「emptyDir 撐不撐得過 kill 1」答「不在了」(錯,綁 Pod uid 不綁 container)。同時暴露**不知道 `kill 1` 是什麼**(= 送 SIGTERM 給 PID 1,回扣 P1 PID namespace)。已直給正解 + 路徑判準(`/var/lib/containerd/...` vs `/var/lib/kubelet/pods/<uid>/...`,**路徑裡就寫著它綁誰**)。**未親手驗證**,s25 補。
- **why-first 預測連跳三次**:context 要三次才給、`kill 1` 三題只答 2(第 3 題縮小成二選一才答「container」)、emptyDir 題只回問不預測。這是本堂最該改的一條。
- **環境故障吃掉中段(教練驅動,學員未提診斷方向)**:`kubectl get nodes` 噴 `invalid character '<'`。鏈路:context `kind` 指向已刪的 cluster `kind-k8s-coach-p0` → kubectl 退回預設 `localhost:8080` → 打到 `gitlab-ci-dashboard`(Up)→ 收到 HTML。修法:`use-context kind-k8s-coach-p2a`;孤兒 context `kind` 已給刪除指令(未確認是否執行)。**教練自己下錯一發 `docker ps --filter name=kind`(p2a 容器名不含 kind,空結果不能證明沒叢集),已當場更正。**
- 叢集現況:`kind-k8s-coach-p2a` 三節點,**worker2 NotReady 17 天**(老毛病)+ 三個 11 天 Terminating 殘骸(backend/db/frontend on worker2),lab 不受影響未處理。活的 Pod 全在 worker:backend .91 / net-tool .92 / db .93 / frontend .94。net-tool RESTARTS 12(`sleep` 到期自然重啟,約 2h 一次)。
- ROI 篩判定:`--` 分界線 s23 教過今天又問 → Q1「面試官會考 `--` 嗎」= no,**tool trivia 不進格子**,當場結案(已第二次口頭解釋,連同 pipe 在哪執行一起講清)。

**球已出未答(s25 開場直接接)**:PV/PVC 解耦已教完(需求單 vs 房源、binding、與 Pod/scheduler 同構),PV 完整 YAML 已給(`pv-demo`,1Gi,hostPath `/tmp/pv-demo`,storageClassName manual),**PVC 規格已給、學員未寫**(`pvc-demo`、500Mi、RWO、manual)。未答的預測題:**1Gi 的 PV 配 500Mi 的 PVC 綁不綁得起來?剩下 500Mi 會怎樣?**

next(s25),順序:

1. **WR9 觸發(25-18=7),不可延**。佇列嚴重積壓(11 張過期,最舊 06-30)。三主題建議:跨-node-走路由表(四連錯,最高優先)、kube-proxy-不在-Pod-啟動路徑、default-deny-分層。**Artifact audit 順便跑**(P2a 只有 notes,manifests 未落地)。
2. WR 後接 **C-1 收尾**:PVC 自寫 → server dry-run → `get pv,pvc` 看 Bound → Pod 掛 PVC 寫檔 → 刪 Pod 重建 → 檔案還在(第三階實證)→ 進 node `findmnt` 看 bind mount 本體。emptyDir 第二階順道用同一顆 Pod 驗(`kill 1` 檔案還在)。
3. **F/G 連四堂債**:s25 F 段用 C-1 材料跑(菜鳥題材:「為什麼 container 死了檔案就沒了?硬碟又沒壞」);G 段正式版仍欠。story-bank 保底一則。
4. pacing:本堂學員答覆極簡短、連跳預測題 = 低電量訊號。s25 開場先做一件事就好,不要 WR + 新內容全塞。**why-first 預測改成硬規格**:不給預測就不給下一發指令(本堂已實測有效,縮小成二選一學員就答得出來)。

<details>
<summary>s23 斷點(已消化,留參考)</summary>

**s23 已收(2026-08-03,公司 bastion,非家機)。盲測 #3 未過(3.5/7,6 天留存)→ 到期卡重建(veth 過、iptables 半)→ 學員要求換新內容 → lab 重啟:allow-dns 於 bastion 重建、兩種死法親手集齊。F/G 未跑(學員跳過 F,連三堂債);story-bank 連三堂未挖。**

本堂事實:

- **盲測 #3(3.5/7,未過)**:站 2 veth 出發、站 6 抵達整站蒸發(站 6 連兩次盲測丟失);站 3/4 壓成一團;「誰做的」只出現在站 1;四動詞口訣未用;七行紀律垮(碎片式交卷)。正面:**幻影站 4 未復發**;「應該不是 kube-proxy 改 kernel」自我存疑方向正確(kube-proxy 只寫規則不碰封包)。已給 L6 顧問版範例(定調句「名字解析完之後,封包的一生都在 kernel 裡」)。
- **veth 卡冷測過**(3→7,08-10):數字對(同/跨 node 都 2 條)、tunl0 誘答咬住(「兩頭是 pod 跟 root netns」)。站 6 用 veth+本機路由表當場重組成功(kernel 查 `/32 dev cali` 那行選 veth)。
- **iptables-一棟樓半過**(留 3,08-06):換皮誘答咬住(「NetworkPolicy 是 CNI 功能但實際改 iptables filter table」= 真進步,上次同日吞餌兩次);但分工句首答「**nat 管路由**」= 層級混淆家族新樣本,重教後三表(nat 改寫/filter 過濾/路由選路)收。08-06 重抽三表分工一句版。
- **default-deny-分層未過**(留 3,08-06):首答「沒辦法跨 pod 溝通」只有結論;兩層梯子才到「DNS 查詢本身也是 egress」;但隨後 **lab 親手集齊兩種死法**(deny-all 下 `Resolving timed out` → allow-dns 上線後 `Connection timed out`),死亡搬家親眼驗證,bastion 側完成(s16 是家機)。
- **兩張名單卡未過**(留 3,08-06):「開幾張名單」答不出兩道門,三層提示後仍要求「說明一下」→ 直接教兩道門模型 + 檢查程序(逐 Pod 逐方向問名單)。net-tool(無業務標籤)已就位當陌生人測試員。
- **YAML 藏寶圖卡未做完整 rep**:allow-dns 重寫時 selector 塞進 ports 清單 + 自行誤改 apiVersion 成大寫 V1(`no matches for kind ... in version` 親手撞第二次);學員選擇跳過讀圖,教練代打修檔(格式雜務代打條款)。卡照舊 unresolved。
- **只給結論 pattern:負樣本日**。B 選項後果半句被跳過、「要開在 allow 上面」、多題裸結論。連兩堂正樣本目標中斷,重新計數。
- 環境:**學員實際在 bastion**(斷點原以為家機)。worker2 NotReady(s16/s21 同款老毛病)+ 10 天 Terminating 殘骸,lab 不受影響,未處理。三層 Pod 全在 worker(backend .84/db .85/frontend .83)。新 Pod:net-tool(netshoot,`run=net-tool`)。`labs/allow-dns.yaml` 已重建並 apply(寫法 A,AND 語義學員選對)。
- 順手教學:http-echo 極簡 image 無 curl(distroless 概念)、`--` 分界線與 `-sS`(Unix 通用約定)、**DNAT 先於 filter → NetworkPolicy 名單要寫 targetPort 5678 不是 Service port 80**(接一棟樓的部門順序,已教未驗)。

**⚠️ 2026-08-03 課後學員決定(明確二次要求,教練已陳明 engine 條款後定案):跳過 P2a phase gate,s24 直接開 P2b。** P2a 記為 not-certified 帶 flag 前進;gate 沒有取消,只是延後 — **P6 面試衝刺前必須補考**(面試官必考封包旅程,躲不掉的是面試不是教練)。盲測 #N 制度廢止;七站材料改由 spaced-rep 卡與 WR9 自然到期,不再當開場關卡。

next(s24)= **P2b 開課(儲存 + 權限:PV/PVC/CSI、StorageClass、RBAC/SA、IRSA、Secrets、PSS)**,順序:

1. **P2b chunk 1 開課**(讀 `references/phase-2b-storage-rbac.md` 排 chunk map)。新 phase 新氣象,開場不抽考、直接進場景。capstone 銜接:api 掛 PVC(訂單資料)+ 最小權限 RBAC + EKS 首登 IRSA(對 Delivery Consultant 目標是高權重段)。
2. A 段輕量(2 題上限,誠實執行不加碼):08-06 到期批挑 2(iptables 三表分工一句版、兩張名單口頭版優先)。P2a 舊卡照 3/7/14 節奏走,WR9(s25 觸發,25-18=7)清算過期佇列。
3. **P2a 未收殘局(flag,擇機補)**:lab Step 5 兩條 YAML + Step 6 驗收矩陣(規格已留檔:app 標籤、TCP 5678、frontend-client 合法/net-tool 陌生人);3-3 gate;**P2a phase gate(P6 前必補)**。
4. F/G 連三堂債:s24 F 段用 P2b 新內容跑(新材料應比舊材料好啟動);story-bank 連三堂未挖,s24 保底一則。
5. pacing:延續「少抽考多動手」;P2b 是概念+動手 phase,錯峰規則生效(新難主題堂英文降回術語卡)。

</details>

<details>
<summary>s22 斷點(已消化,留參考)</summary>

**s22 已收(2026-07-28,家用 VM)。七站重建日:鷹架版全站走完 → 無鷹架盲測 #2 未過但大進步(3 碎片→5/7)→ F 段 Teach-to-Learn 首跑(三 chunk 的債開始還)。面試時間軸確認:已投遞、抓 1.5 個月(~2026-09 中旬),curriculum-plan §9 已補倒推註記。**

本堂事實:

- **盲測 #2(5/7,未過)**:幻影站 4(DNAT 重複出場)+ 站 6 進門整站蒸發,兩錯在輕提示下**自我診斷**修正;「誰做的」欄多數缺席;Service 思維滲入(「按照什麼 service 進去嗎」)。學員拒背「四層框架」名詞(合理,教練發明的鷹架)→ 改**四動詞口訣「問名→改寫→放行→送達」**,只保順序不背名詞。
- **F 段亮點**:monologue 開場自帶顧問框架(「講這個是為了排障時定位哪一站出事」);靜默無效鏈在追問下首次自組(「不會報錯,但預期 DB 有保護、實際上並沒有」)。
- **F 段兩洞**:① 守衛站在無壓力敘述時**第二次蒸發**(追問才補回);② 誘答吞餌「DNAT 做完才進 iptables」— 當日已教(站 4 幻影修正)仍複發 → 新卡 iptables-一棟樓。
- A 段偵察挖出 veth 誤記「跨 node 連線」→ 車道比喻重教,封印句「veth=Pod netns→node root netns,每 Pod 一條、出門必走、同跨 node 都 2 條」鷹架下收到,新卡 07-31 冷測。
- 跨-node-走路由表卡**重測未過**(第三種錯法:查 svc;史料:iptables、resolv.conf),保姆級提示才到 route table;分工句無法自產,直給後二選一應用 2/2。
- 站 7 亮點:「改 src,**因為** Pod A 一開始就不認識 PodB-IP」— 判準句首次無提示自發(pattern 卡首見正樣本)。
- DNAT 拼成 DANT×3 已糾。教學回饋:recall 不得用 session 編號錨定,一律內容錨定(已入 memory)。

next(s23),順序:

1. **開場冷測:七站盲測 #3(gate 答案卷)**。四動詞口訣開頭、七行、每行含「誰做的」。3 天後還在才算真保留;過了才進 P2a phase gate(Examiner 首用)。
2. A 段債(2 題上限):kube-proxy-不在-Pod-啟動路徑(07-26 到期,s22 未抽)、default-deny-分層(07-26,s21 未過那張)。07-31 批(veth、iptables-一棟樓、跨-node-路由)到期再排。
3. 盲測 #3 過 → phase gate 準備 or lab Step 5+6(家機 p2a 叢集狀態先驗,`allow-dns` 在家機應仍在,bastion 側才是被砍過的)。
4. story-bank 挖礦 s22 未做(債,連兩堂欠);G 段正式版仍欠(s22 以盲測 #2+F 段折算 1/4)。
5. pacing:s22 學員主動選加碼 F 段且全程有輸出,無低電量訊號;但同材料當日三過(鷹架+盲測+F)已到邊際,s23 換冷測+新內容配比。

</details>

<details>
<summary>s21 斷點(已消化,留參考)</summary>

**s21 已收(2026-07-23,公司 bastion)。三件大事:① 職涯目標確認為 AWS Delivery Consultant,教學格式改制 ② 叢集舊帳爆掉並修好 ③ 4-5 七站冷測 0/4 未過。**

**① 目標與格式改制(最高優先,影響往後每一堂)**:學員確認面試職缺是 **AWS Delivery Consultant (ProServe)**,並要求(a)全部問題用該職位的面試情境模擬、(b)每題附 **L6 senior 範例答法**、(c)**加速課程**。已寫入 memory 兩張卡 + curriculum-plan §9。含意:Amazon LP 佔 loop 近半 → story-bank 從「P6 提煉」提前到每堂機會式入帳;全英文 loop → English ramp 需提前;技術主線不變但 EKS/IRSA/migration 權重拉高。

**② 環境修復(舊帳,s16 拖到今天)**:p2a 兩台 worker 全 NotReady,Reason `container runtime is down`。診斷鏈:node Conditions(排除 mem/disk)→ 宿主機資源(15Gi 剩 9.8Gi,**記憶體不是兇手,推翻 s16 假設**)→ containerd `active (running)`(進程活著)→ kubelet log `Status from runtime service failed: rpc DeadlineExceeded`(真兇)。根因=4 核心上跑 6 個 kind node + terraboard 重啟迴圈,CRI gRPC 被拖過 timeout。修法:學員親手 `kind delete cluster --name k8s-coach-p0` + `docker stop terraboard` + `docker restart` 兩台 worker → 三台全 Ready。**教學價值高**:故障點(worker NotReady)與根因(隔壁叢集搶資源)不在同一個叢集裡。註:worker/worker2 的 node IP 重啟後變動(現 worker=172.21.0.4)。lab 三層 Pod 全部復活在 worker2(frontend .210 / backend .209 / db .211),舊 Terminating 殘骸未清。**`allow-dns` netpol 已不存在,只剩 `default-deny-all`**。

**③ 4-5 七站骨架冷測:0/4,明確未過。** 學員只給出 3 個碎片(CoreDNS 的 ClusterIP / kube-proxy iptables / 回程 conntrack),漏掉 veth 出 Pod、過濾層、**跨 node 路由**、抵達 node2。追問「封包怎麼從 node1 到 node2、第一個指令是什麼」→ 答「查 iptables」→ 縮小重問 → 答「查 resolv.conf」(跨層到 DNS)。**結論:s19/s20 親手驗過的四塊零件,三天後無鷹架組裝不起來 = 會用 ≠ 會講,隔堂冷測的價值當場實證。** 事後給正解七站表 + L6 級範例答法(含間歇性假設排序:conntrack table full / ENA `conntrack_allowance_exceeded` / DNS UDP 競態 / rollout endpoint 過時),學員親手 `docker exec ... ip route` 摸到第 5 站,自己挑對 `192.168.20.192/26 via 172.21.0.2 dev tunl0` 那一行(但判準要追兩次才給,且最後答「不用特別算」= 拒絕 show work)。

next(s22),順序:
1. **開場即改制**:A 段抽考一律包成 AWS Delivery Consultant 客戶情境,答完給 L6 對照版。順手挖一則 story-bank raw(LP 佔比高,每堂都挖)。
2. **4-5 七站重測(第 2 次)**,這是 P2a gate 的答案卷,沒過不進 gate。重點盯第 2/4/5/6 站(今天全漏)與「每站誰做的」。要求先宣告四層框架再走路徑。
3. **判準句型專項**:學員今天三次只給結論不給判準(第六、七堂同條)。強制句型「我看的是 X,**因為** [判準]」,每個答案都要有「因為」後半句。
4. step A 過期債(每堂 2 題):07-22 一批(靜默無效一段話組裝版、兩張名單兩關檢查程序、L4-L7 無框架新情境、三分類第 2 輪)、07-23(CNI 合約三件事、出廠全通重抽,今日均未跑)、以及 06-30/07-03/07-10 的長期積欠。**佇列嚴重積壓,WR8 在 s25 觸發時要清一次。**
5. chunk 3+4 F/G 累積債仍未跑;lab Step 5+6 未動(叢集已就緒,`allow-dns` 需重建)。
6. **加速課程的處理**:學員要求加速,但今日冷測 0/4。正確做法是**重新配重不是趕進度**(P2b IRSA / P5 EKS terraform / migration 拉高,P3/P4 深度可修剪),並確認面試日期才能倒推。**s22 開場先問面試時間點。**
7. pacing:今日出現慢下訊號(回答變短、貼回原文、「不用特別算」),已縮 scope 收場。

</details>

<details>
<summary>s20 斷點(已消化,留參考)</summary>

**s20 已收(2026-07-20,公司 bastion,一日三 chunk 紮實堂)。C-4 封包全鏈四塊本堂全收:4-2 veth pair、4-3 node 路由表、4-4 MASQUERADE(4-1 CNI 合約 s19 已收)。全程學員親手敲指令、教練只給規格與判讀(鍵盤鐵律遵守)。開場給了 4-1 CNI 左→右英文思維導圖複習(學員白板用),NIC 一詞當場問答補上。**

亮點:① 4-2 net-tool 第一次 `sleep 3600` 睡滿變 Completed、if11 被 Calico 拆掉→意外教到 CNI「拆」條款(建/拆/重建全看過),重建 if12/.80 實證 Pod IP ephemeral;ifindex 兩頭互指 3↔12 親手驗 veth。② 4-3 兩預測都對(同 node=/32 dev cali 無 via、跨 node=via nodeIP dev tunl0),Transfer 排障尺三段逼問後鎖精準。③ 4-4 誘答題「重啟 kube-proxy 清 conntrack」抓對兩刀半:症狀→conntrack✅、conntrack 是 kernel 表跟 kube-proxy process 無關✅、治標/治本歸錯邊需扶正(調 max=治標、找洩漏源=治本,s5/s6 老改進項復現)。

next(s21),順序:
1. step A 過期債(每堂 2 題上限,過期優先):07-20 到期「出廠全通」(s20 半過,結論靠提示、why 沒站住,已改掛 07-23)、「default-deny 分層」(s20 動手版學員喊跳過未跑);07-22 到期一批(見下)。
2. **4-5 七站骨架盲講冷測**(gate 答案卷,要求白板默數 1-7 一站不跳;C-4 四塊已備妥,這是把它們串成一條旅程)。留意謎題B 舊誤解(封包「先去 ClusterIP」)是否借屍還魂、第 1 站與第 3 站是否壓成一步。
3. 07-22 冷測:靜默無效「一段話組裝版」、兩張名單「兩關檢查程序」、**L4-L7 無框架新情境(禁 postgres/redis,過了才推 7)**、三分類家族第 2 輪(換成員);07-23 CNI 合約三件事快抽 + 出廠全通重抽。
4. **chunk 3+4 F/G 累積債補跑**(F Teach-to-Learn、G Interview Q&A 自 chunk 3 起未跑)。
5. lab **Step 5+Step 6 同一坐位收**(學員決策延後綁一起,6 驗收 5 不可拆;net-tool if12/.80 可當測試客戶端)→ 3-3 gate → **P2a phase gate(Examiner 首用)**。
6. pacing:冷測上限 15 分鐘;低電量改 micro-mode。**學員本堂數次要求「拉高整理/講學習價值/畫思維導圖」= 教學價值敏感度高,每個 chunk 先給面試/排障 payoff 再動手,效果好,續用**。bastion 待辦不變:砍 p0(仍未執行,worker2 因資源不足 NotReady,lab 不受影響)。

<details>
<summary>s19 斷點(已消化,留參考)</summary>

**s19 micro 已收(2026-07-20)。chunk 4-1「CNI 是一紙合約」過:hostNetwork 判準(「需不需要獨立網路」)學員自推 ✅;合約三件事 Recall 卡兩輪、把選配 NetworkPolicy 混進合約本體 → 簡化重教後預測題(漏路由=timeout)過。新 registry 卡 07-23。**

</details>

<details>
<summary>s18 斷點(已消化,留參考)</summary>

**s18 已收(2026-07-19,WR7 冷測專場,短堂)。三主題 3/3 過:L4-L7 新情境(postgres/redis,判準框架教練給)、conntrack 分工句收、三分類家族 counter 1/3。學員決策:lab Step 5+6 延後、綁一起做(6 驗收 5 不可拆)。s17「什麼都沒學到」已用冷測結果回應:s16/s17 的內容有留住。**

</details>

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
- P2a 網路深水區: in-progress(chunk 1 Service/kube-proxy/CoreDNS ✅、chunk 2 Ingress ✅;chunk 3 NetworkPolicy in-progress〔3-1/3-2 教完;lab Step 4 於 s23 bastion 側重建完成(allow-dns + 兩死法實證),Step 5 兩道門模型已教、兩條 policy 未寫,剩 Step 5+6+gate+F/G〕;chunk 4 in-progress〔**4-1 CNI 合約 ✅ s19、4-2 veth ✅ s20、4-3 路由 ✅ s20、4-4 MASQUERADE ✅ s20**;**4-5 七站骨架盲講 ❌ s21 冷測 0/4 未過**〕。四塊零件備妥但串不起來,4-5 重測過了才進 phase gate)
- P2b 儲存 + 權限: **in-progress(s24 開跑)**。C-1 Volume/PV/PVC in-progress:第一階「可寫層綁 container」✅ 親手實證(overlay 三層 + kill 1);第二階 emptyDir ❌ 口頭未過、未動手;第三階 PV/PVC 概念已教、**PVC YAML 球已出未答**。C-2 起未開。
- P3 調度 + 高並發 + 排障: not-started
- P4 可觀測性工程: not-started
- P5 平台工程 / GitOps: not-started
- P6 面試衝刺: not-started

Weak-topic flags(**2026-08-03 首次啟用**,P2a 帶 flag 前進、gate 未考,學員決定):
- **七站封包全旅程**(4-5):盲測最佳 5/7,站 2/6 蒸發、「誰做的」缺席。P6 前 phase gate 必補;spaced-rep 卡照常到期。
- **chunk 3 NetworkPolicy 收尾**:lab Step 5 兩條 policy + Step 6 驗收矩陣未做(規格已留檔);兩張名單口頭版未過。
- **判準句 pattern**(只給結論):跨七堂未愈,ProServe 加權重罪,每堂續盯。

## Mastery

- P0 apply→Running control flow: high (s10)— 注意:盲講易漏中間棒次(WR#1 漏 scheduler),用「五棒默數」骨架
- P1 container = namespace+cgroup: high (s6)
- P1 probe(liveness vs readiness): high (s6;判斷句「would a restart fix this?」已多次過)
- P1 Deployment/rollout: high (s6)
- P1 resource/QoS/OOM(可壓縮 vs 不可壓縮): high (s10)
- P2a Service/kube-proxy/DNAT/conntrack/CoreDNS 全鏈: high (s10 二度無鷹架冷測封印;s15 注意:規則寫手一度答成 kubelet,鷹架後撈回 kube-proxy)
- P2a Ingress(規則 vs controller、L7 純字串比對): med (s14;結果預測準、why 第一輪講不出 = W1 隱性會,gate 已過但精度待固化)
- L4 vs L7 判準(讀不讀 HTTP 內容): **low-med** (s18 回升:postgres/redis 讀寫分流新情境兩題連過、「標籤貼反」未重現,且自產「要拆開的是 redis 的指令」;判準補完整為兩步〔①轉發決定要讀到哪層 ②要拆信則工具懂不懂該協定格式,L7=協定特定的翻譯官,nginx 只懂 HTTP〕— 但兩步框架為當堂教練所給,07-22 無框架新情境過了才 med。s16 降級紀錄:同一天內兩度失手且形狀相同=**結論對、判準錯**:① ALB/NLB 題,內容映射全對〔NLB=TCP/UDP/static IP/fast、ALB=path/TLS/HTTP〕但**L4/L7 標籤整個貼反**;② NetworkPolicy 擋 `/admin` 題,結論「做不到」對但理由答「NetworkPolicy 是針對 namespace」=非機制,且與當堂剛教的「namespace 不做隔離」打架。兩次都是教練直給錨點〔fast=少做事=低層;ALB=Application=L7;from/to 欄位清單裡沒有 path〕→ **直給不算過,未封印**。s17 WR 用新情境冷測)
- NetworkPolicy(白名單 + default-deny 翻轉 + 第四個引擎): low-med (s17:3-1 Recall ✅〔policyTypes 方向性重教一輪後情境題全對〕、坑一 AND/OR ✅〔含 batch-job 案例〕、坑三 ipBlock ✅;坑二兩張名單 ❌、3-1 Transfer 組裝 ❌,兩筆 07-22 冷測。Step 4 親手完成:allow-dns 一張卡決策自己做對,死法 Resolving→Connection 搬家實證。**s23 bastion 側重演**:allow-dns 重寫 apply、兩死法親手集齊、坑一 AND 二選一又選對;但坑二兩張名單三層提示仍未自產,直教兩道門模型;新知識點「netpol 看的是 DNAT 後的 targetPort」已教未驗)
- conntrack 精度(table full 新舊連線): med (s18 **分工句收**:「iptables 第一次決定、conntrack 之後記住」骨架自產,應用經一次追問補全〔第 50 個去程=查 conntrack 改 Destination、回程=改 Source 反向〕;07-26 抽完整版〔兩個詞+分工句+查誰〕過即封印。歷史:s15 重抽沒過、答案直給;s16 給框架後兩個詞自產)
- DNS 排障第一刀(先用 FQDN 二分): med (s13;需鷹架)
- P2a CNI 封包全鏈 data plane(veth/路由表/MASQUERADE/conntrack): **low-med** (**s21 降級**:無鷹架七站冷測 0/4,只吐出 3 個碎片〔CoreDNS 的 ClusterIP / kube-proxy iptables / 回程 conntrack〕,漏 veth 出 Pod、過濾層、跨 node 路由、抵達對面 node。追問跨 node 第一個指令 → 答 iptables → 縮小重問 → 答 resolv.conf〔跨層〕。**s20 自己推出的排障尺「跨 node 不通查對面網段那行」三天後完全蒸發**。診斷:零件記憶 ≠ 旅程記憶,四塊各自驗過但從未串講。事後給正解 + L6 範例後親手 `ip route` 挑對 `192.168.20.192/26 via 172.21.0.2 dev tunl0`。s20 原始紀錄:一堂三 chunk 全親手驗:veth ifindex 兩頭互指、路由表三岔路〔via/dev 尺〕、MASQUERADE 換臉規則自讀出「Pod 打 Pod 不換」。排障尺〔跨 node 不通查對面網段那行〕經三段逼問鎖精準;conntrack 治標/治本仍需扶〔調 max=治標歸錯邊,s5/s6 老條〕。**未經無鷹架冷測**,4-5 七站盲講過了才升 high。**s22 重建**:鷹架版七站全走完;無鷹架盲測 #2 5/7 未過(幻影站 4 DNAT 重複+站 6 進門蒸發,兩錯輕提示下自我診斷)但 vs s21 的 3 碎片是實質進步;四動詞口訣「問名→改寫→放行→送達」取代四層名詞;s23 開場冷測 #3 定升降。**s23 盲測 #3:3.5/7 未過**(6 天留存:站 2/站 6 蒸發=veth 的兩次出場、七行紀律垮、「誰做的」只剩站 1;幻影站 4 未復發、kube-proxy 不碰封包的存疑自發。當日重建:veth 卡冷測過、站 6 當場重組成功。盲測 #4 s24 開場)

- **分層判準「關掉 API Server 還在不在」**(對治層級混淆家族): med (s24 新造工具,當堂 3/3 過且兩題無提示自答〔「沒有,因為 CNI 不支援」「可以,因為直接修改 kernel」〕。左欄=kernel 真東西〔iptables/conntrack/路由表/veth/cgroup/mount/namespace〕,右欄=etcd 資料〔Service/Deployment/PVC/NetworkPolicy/RBAC/Secret〕;RBAC 是特例〔純 API Server 層,kernel 一無所知〕已埋未教。**當堂教當堂過不算保留**,08-07 冷測定升降)
- **P2b C-1 可寫層 / overlayfs**: med (s24 親手實證:讀 `/proc/mounts` 認出 lowerdir 15 層共用 vs upperdir 1 層獨有、全在 `/var/lib/containerd`;`kill 1` 三個預測全中。起手誤答「存在 memory」= 結論對機制錯。**emptyDir 綁 Pod uid 那一階口頭未過且未動手**,PV/PVC 第三階未做。判準句:路徑裡就寫著它綁誰)

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
- 2026-08-03 | 盲測 #3 + lab (s23, tier 2) | 1/4 | 「誰做的」與判準句整堂缺席,兩道門檢查程序三層提示未自產;盲測格式紀律(口訣+七行)要當成硬規格 | 換皮誘答咬住「NetworkPolicy 實際改 iptables filter table」+ tunl0 不是 veth 咬住;兩死法 Resolving→Connection 親手集齊 | coach(原理🟡 機制✅ 自己的話❌ MTTR🟡〔讀 no matches for kind 有方向但誤修大寫 V、跳過讀圖〕。G 未跑,盲測+lab 折算;F 學員跳過)
- 2026-08-04 | A 段冷測 + C-1 lab 折算 (s24, tier 2) | 1/4 | **why-first 預測連跳三次**(context 要三次才給、kill 1 三題只答 2、emptyDir 題只回問不預測):預測是最便宜的抓漏點,跳過等於把錯誤延後到冷測才發現。s25 起改硬規格,不給預測不給下一發指令 | 「Calico 上 apply 完的 NetworkPolicy,關掉 API Server 還擋不擋得住?」答**「可以,因為直接修改 kernel」,無提示自答**,是本堂最硬的一題,也是靜默無效卡的鏡像正樣本 | coach(原理🟡〔「存在 memory」機制錯、emptyDir 綁誰答錯,但 overlay 圖看懂後能自推 upperdir 綁 container〕 機制✅〔分層判準兩題無提示自答〕 自己的話❌〔全堂極簡短答,判準句缺席〕 MTTR❌〔HTML error 排障全程教練驅動,學員未提任何診斷方向〕。**G 未跑、F 未跑**,以 A 段冷測 + lab 折算)
- 2026-07-28 | step G 折算 (s22, tier 2, 盲測 #2 + F 段) | 1/4 | 「誰做的」欄要長在骨架裡,每站一個負責人;iptables=一棟樓(nat 改寫/filter 過濾)當日教過仍吞誘答 | F 段自組靜默無效鏈「不會報錯,但預期 DB 有保護、實際沒有」+ 站 7 無提示判準句「改 src 因為 Pod A 不認識 PodB-IP」 | coach(原理🟡 機制🟡 自己的話✅ MTTR❌。盲測純冷信度高;F 段帶問題鷹架)
- 2026-07-23 | step G (s21, tier 2, **AWS Delivery Consultant 面試模擬首場**) | 0/4 | 判準句缺席:三次只給結論(kube-proxy yes/no、選路由那行、CIDR「不用特別算」),第六堂同條 | 回程 conntrack 主動講出來,無提示,而且那是 gate 歷史漏點清單上的站 | coach(原理❌ 機制❌ 自己的話❌ MTTR❌。七站只給 3 碎片;MTTR 兩次選錯指令且第二次跨層到 DNS。**信度高**:純冷測、教練全程未給鷹架)
- 2026-07-17 | A 段+chunk3 gate (s16, tier 2) | 1/4 | 判準/機制講不出:L4-L7 兩度結論對理由錯;分工句未收 | conntrack 去程/回程兩欄位**自產**(給框架不給答案,s15 直給後蒸發,今日一次推出) | coach(原理❌ 機制🟡 自己的話❌ MTTR 未演練。**本場信度低**:教練犯三錯〔過度抽考/考未教內容/搶鍵盤〕,低分含教練污染,不宜單獨採信,s17 WR 重測)

## Mistake Registry

<!-- 欄位:date | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     interval 2 = +2 天臨時複習格(口頭型 resolved,過了才進 3/7/14)。
     unresolved-session-count 於遷移時依複測紀錄初始化(近似值)。 -->

- 2026-06-18 | YAML validation | `matchLabels` 打成 `metaLabels`,不會讀 strict decoding error | 不知道 unknown-field 路徑=藏寶圖、驗證發生在 API Server | unresolved | 7 | 2026-06-30 | 2
  - 正解:讀 `unknown field "A.B.C"` 完整路徑回檔案定位;selector 認親欄位是 `matchLabels` 且必須等於 template.metadata.labels。06-23 抽考需引導才答對「檢查在 API Server、與 etcd 無關」,推 +7。**s23 實戰現形**:allow-dns 重寫把 selector 塞進 ports 清單,dry-run 前自行「猜修」把 apiVersion 改成大寫 V1(`no matches for kind ... in version` 第二次親手撞,s16 同款),拿到錯誤後學員選擇跳過讀圖、教練代打。讀圖 rep 仍欠,WR9 用帶錯 YAML 現場讀圖。
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
- 2026-07-17 | NetworkPolicy 出廠全通 | why-first 預測「陌生 tmp Pod 連不到 db」→ 實測**連得到**(回 `db`) | k8s 出廠預設全通、namespace 只是邏輯分組不做隔離(P1 已釘過、當堂教練又粗體講過 40 分鐘,仍預測錯) | unresolved | 3 | 2026-07-23 | 1
  - 正解:出廠任何 Pod 可連任何 Pod、跨 ns 亦然;NetworkPolicy=白名單宣告,**一旦有 policy 選中該 Pod,該方向即從全通翻轉成 default-deny**。生產起手式=每個 ns 先上空白名單(`podSelector: {}` + `policyTypes: [Ingress, Egress]` + 零 rule)再逐條開洞。**s20 重抽半過**:情境題(新 ns 無 policy 互打通不通)結論靠提示撈回、關鍵 why「podSelector 只在自己 ns 內選人,勢力範圍不跨 ns;from/to 名單可跨 ns=放行誰,podSelector=翻轉誰」沒站住 → 07-23 再抽(與 CNI 卡同天),過了才推 7。
- 2026-07-23 | 跨 node 走路由表不是 iptables(層級混淆家族) | 「封包怎麼從 node1 到 node2?第一個指令是什麼」→ 答「查 iptables」;縮小重問「node1 怎麼知道這個 IP 在哪台機器」→ 答「查 resolv.conf」 | 改寫層(NAT)與轉送層(routing)混為一談;第二次還跨到解析層 | unresolved | 3 | 2026-08-07 | 1
  - 正解:**`ip route`**。判準句「**iptables 管改寫成什麼,路由表管往哪裡送。改寫完之後,封包還是得問路。**」排障尺:跨 node 不通 → 拿目標 Pod IP 去路由表對網段,看那一行在不在、`via` 誰、走哪個 dev。s21 親手驗:`192.168.20.192/26 via 172.21.0.2 dev tunl0 proto bird onlink`(`via`=跨機器、`tunl0`=IPIP overlay、`proto bird`=Calico 的 BGP daemon 自動佈的,不是人寫的)。**此卡是 s20「排障尺」蒸發的直接證據**。**s22 重測未過**:同題再問答「查的是 svc」(第三種錯法,前兩種:iptables、resolv.conf),保姆級提示才到 route table;分工句無法自產,直給後二選一應用題(MASQUERADE 誰做/選介面誰做)2/2 過。病灶更新:**封包出 Pod 後仍用 k8s 物件思考,kernel 只認 iptables 規則/conntrack 表/路由表三樣**。**s24 四抽未過,答「會看 a 的 service, kubectl get svc」= 與 s22 完全相同的錯法,連錯法都不再進化**。加註:該題 `curl PodB-IP` 從頭到尾沒有 Service 參與,學員連「這條路徑上有沒有 Service」都沒判。08-07 五抽,改成兩段問:①這條路徑有哪些元件參與 ②第一個指令。
- 2026-07-23 | kube-proxy 不在 Pod 啟動路徑上 | ① 把 kube-proxy 列為 kubelet 建 Pod 的三件事之一 ② 「Pod 啟動過程有封包打 ClusterIP 嗎」答 yes | 控制路徑 vs 資料路徑混淆;規則 vs 引擎家族 | unresolved | 3 | 2026-08-07 | 1
  - 正解:Pod 啟動全程 **0 次 ClusterIP**(kubelet 連 kubeconfig 裡的真實 endpoint、拉 image 連 registry 真 IP、CNI 是本機執行 binary 不過網路、掛 volume 是本機檔案系統)。分工句:**「kube-proxy 管的是 Pod 出生之後拿 Service 名字互打那條路;Pod 怎麼出生跟它一點關係都沒有。」** 症狀對照:kube-proxy 掛=現有連線照跑、規則不再更新;CoreDNS 掛=新解析全滅。**s24 首次重抽未過**:答「CoreDNS 嗎」。新病灶命名:**把「kubelet 把 CoreDNS 的 ClusterIP 寫進 Pod 的 resolv.conf」誤當成「啟動過程打過它」——寫進去 ≠ 打過**。08-07 重抽,要求答 0 次 + 講四個啟動動作各自連誰。
- 2026-07-23 | 只給結論不給判準(pattern 卡,升級追蹤) | 同一堂三次:kube-proxy 題只答 yes、選路由那行不給計算、CIDR 直接說「不用特別算」 | 輸出習慣問題不是能力問題:算得出來但不 show work,面試官無法區分「會」與「猜對」 | unresolved | 3 | 2026-07-26 | 5
  - 對治句型(每個答案強制):**「我看的是 X,因為 [判準]。」**「因為」後半句就是固定掉分的地方。歷史:s5、s14、s16、s18 scorecard 的「最該改進」都是這一條,s21 升級為獨立卡追蹤。ProServe 加權:顧問工作有一半是在客戶面前 show work,這條在目標職位上是重罪。**s22 混合訊號**:站 7「改 src,因為 Pod A 一開始就不認識 PodB-IP」= 首次無提示自發判準句(正樣本);但站 5 仍裸結論(「查的是 svc」無因為)。**s23 負樣本日**:整堂裸結論(「要開在 allow 上面」等)、AND/OR 的 B 選項後果半句被跳過(教練點名「junior/senior 分界線」),自發正樣本 0,連堂計數重置。**s24 混合**:負面=why-first 預測連跳三次、全堂極簡短答;正面=**「可以,因為直接修改 kernel」與「沒有,因為 CNI 不支援」兩題自帶因為**(pattern 卡第二次出現無提示正樣本,前一次是 s22 站 7)。08-06 續盯,重點改盯**預測題有沒有先講再按 Enter**,不只盯答案裡有沒有「因為」。
- 2026-07-17 | default-deny 後的分層(DNS 層 vs 連線層) | 只答「連線不到」,未分辨死在哪一層;**s21 重抽未過**:情境題答「這問題應該是 app 層」,縮小到圖上指認又答「被鎖的是連線那步」(漏掉①先發生) | 層級混淆家族(同 s11 把 conntrack 拉進 DNS 題、06-28 排障第一刀);s21 新形狀=**兩步都被鎖時不問哪一步先發生** | unresolved | 3 | 2026-07-26 | 1
  - 正解:`curl http://db` 有先後兩步 —— ① 問 CoreDNS(需 egress UDP/TCP **53**)② 建 TCP 連線。default-deny 鎖 egress **連 53 一起鎖**,所以死在第 ① 步,第 ② 步沒機會發生。實證(s16 親手):`curl http://db` → `curl: (28) **Resolving** timed out`;`curl http://192.168.46.66:5678`(餵 IP 跳過 DNS)→ `curl: (28) **Connection** timed out`。**同一條 policy 兩種死法,差別只在需不需要問名字**。prod 陷阱:app log 噴 `could not resolve host` → 全隊衝去查 CoreDNS,但 CoreDNS 好好的,是 policy 封了「去問路的那條路」。故 default-deny 第一個洞永遠是 DNS。**s23 重抽仍未過**(首答「沒辦法跨 pod 溝通」只有結論;「DNS 查詢本身也是 egress 封包」要兩層梯子才到,timeout 種類講不出);但隨後 bastion lab 親手集齊兩死法(deny-all 下 Resolving → allow-dns 上線後 Connection),第一次帶著肌肉記憶離場。留 3,08-06 抽「兩步先後+兩種錯誤訊息關鍵字」。
- 2026-07-28 | veth 誤記「跨 node 連線」 | 自我盤點答「veth 是跨 node 的網卡連線」;同/跨 node 各經過幾條 veth 數不出 | 零件定義衰減:veth 只管 Pod netns→node root netns 那一段,跟跨不跨 node 無關 | unresolved | 7 | 2026-08-10 | 1
  - 正解+封印句:**veth=Pod 自家車道,每 Pod 一條、出門必走**;同 node 2 條(自家出+對方入)、跨 node 也 2 條(tunl0 是高速公路不是 veth);PodB 的 eth0 就是它自己 veth 的另一頭。發音 /viː eθ/。s22 鷹架下收。**s23 冷測過**(6 天留存):數字全對、tunl0 誘答咬住(「兩頭是 pod 跟 root netns」),推 7。但注意:同日盲測 #3 站 2/站 6(veth 的兩次出場)仍蒸發 = 零件會、放回旅程不會,08-10 抽「旅程內出場」版。
- 2026-07-28 | iptables=一棟樓(nat 表/filter 表) | 盲測幻影站 4「DNAT 到 node iptables 出去」+ F 段誘答吞餌「DNAT 做完才進 iptables,對」— 同一病灶當日兩現 | 把 iptables 當成旅程中的「一站」,不知 DNAT 就發生在 iptables nat 表裡、守衛在 filter 表裡 | unresolved | 3 | 2026-07-31 | 0
  - 正解:**iptables 是一棟樓不是一站:nat 表=改寫部門(DNAT/MASQUERADE),filter 表=查驗部門(felix 編譯的 NetworkPolicy)**。封包全程在樓裡換部門,沒有「出了 DNAT 才進 iptables」。高危:當日教兩次仍複發。**s23 半過**:換皮誘答咬住(「NetworkPolicy 是 CNI 功能但實際改 iptables filter table」,吞餌史終結);但分工句首答「**nat 管路由**」= 層級混淆家族又一新樣本(親戚:查 iptables/查 svc),重教後三表一句(nat 改寫/filter 過濾/路由選路)收。留 3,08-06 抽三表分工一句版 + 部門順序應用(nat 先於 filter → netpol 名單寫 targetPort 5678 不寫 Service port 80,s23 已教未驗)。
- 2026-07-20 | CNI 基本合約 vs 選配 | Recall 合約三件事兩輪講不出,答成「建立網路 networkpolicy 嗎」= 把選配(NetworkPolicy 引擎)混進合約本體 | 新教內容首輪未固化 + chunk 3 靜默無效的 CNI 印象蓋過合約本體 | unresolved | 3 | 2026-07-23 | 0
  - 正解:合約本體=**網卡、IP、路由**(管「通」,每家 CNI 必做,kubelet 建 Pod 時呼叫);NetworkPolicy 引擎=選配(管「擋」,Calico 有 kindnet 無)。hostNetwork=不蓋孤島直接住 node root netns,故不需 CNI(etcd/apiserver/kube-proxy 照跑=排障訊號「CNI 層壞 vs 整機壞」)。s19 亮點:hostNetwork 判準「需不需要獨立網路」學員自推。07-23 抽三件事+各自缺席的死法。
- 2026-07-19 | 兩張獨立名單(3-2 坑二) | 「只開 backend ingress,frontend curl backend 通嗎」答「可以吧」 | 規則剛教完但沒跑兩關檢查程序,憑感覺猜;學員隨後喊「直接說明」未自跑重測 | unresolved | 3 | 2026-07-22 | 0
  - 正解:A→B 要過兩關(A egress + B ingress),任一關無洞即 timeout;檢查程序=逐關問「這個 Pod 的這個方向名單上有洞嗎」。重測要看主動跑程序,不是背結論。對照:回程免開(conntrack stateful)當天答對。**s23 重抽未過**:「開幾張名單」三層提示(門的比喻、deny-all 也鎖 backend)仍未自產兩道門,學員喊「說明一下」→ 直教兩道門模型。Step 5 兩條 policy(frontend-egress/backend-ingress)s24 學員自寫,寫對+驗收矩陣過 = 動手版過關;口頭版 08-06 再抽。
- 2026-07-19 | NetworkPolicy 靜默無效(四引擎第四行) | Transfer 只給零件不組裝:「API Server 只驗 schema → 存 etcd → 無引擎編譯成 kernel 規則 = 靜默無效 = 安全假象」整條鏈講不出,③ 危險比較只答半邊 | 先跳結論等追問才補深度(第四堂同條)+ W1 隱性會;零件全對(apiserver/CNI/馬上發現)但拒組裝 | unresolved | 3 | 2026-07-22 | 0
  - 正解一段話:API Server 只驗 schema 不驗「有沒有引擎」,通過即存 etcd,`get netpol` 查的是 etcd 裡的宣告;沒有支援的 CNI 就沒人把宣告編譯成 kernel 過濾規則,物件永遠只是資料。Ingress 沒引擎=功能壞,使用者馬上叫;NetworkPolicy 沒引擎=安全假象,沒人叫,直到被入侵。**靜默失效比大聲失效危險**。s17 學員零件全掏出但三輪不組裝,喊繼續,冷測要求一段話完整版。**s22 F 段首次質變**:在菜鳥追問(「apply 會報錯嗎?」)下自組完整鏈 — 宣告 vs 引擎(agent/daemon 自答,felix 名字沒到但方向對)+ apply 不報錯 + 「預期 DB 有保護、實際沒有」安全假象自己的話講出。仍帶問題鷹架(追問結構了答案),07-31 一段話冷測版過才 resolved。
- 2026-07-07 | Ingress YAML schema | `backend.service` 寫成字串 + `pathType: prefix` 小寫;client dry-run 又給假安心 | service 是 object 型別;enum 大小寫敏感;decode 錯擋在第一個 | unresolved | 3 | 2026-07-10 | 1
  - 正解:一律 `--dry-run=server`;讀 `ValidationError(路徑)` / `cannot unmarshal ... type X` 定位;對照同檔已寫對的另一條規則照抄結構。
- 2026-07-07 | Ingress 404 排障 | 差點改沒壞的規則;真兇=被 Ctrl-C 打斷的半死 port-forward 回假 404 | 規則層全綠時兇手在「你測試所經過的那層」 | parked(2026-07-16 ROI 篩:Q1 半 yes,但「port-forward 半死」是 lab 夾具產物、prod 不長這樣;同一判準已三種問法重問三次=題目壞掉。判準留檔備查,不再抽) | - | - | 3
  - 正解:404 先分層(規則層 vs 後端層);port-forward 是會抖的除錯夾具,不可信就換乾淨再下結論;任何猜測(含教練的)先驗證再採信。07-09 G 段英文重測:方向對但「規則全綠後兇手在哪」連卡兩次、誤猜 nginx-ingress 本身 → 純口頭沒重現,+2 天格重抽。
- 2026-07-09 | no-Host→404 的 why | 結果預測對,但講不出「curl 自動拿 URL 主機名當 Host」那個字 | 會用/會預測 ≠ 會講 why(W1 隱性會) | resolved(2026-07-16 ROI 篩:Q1=no,curl 填 header 是 tool trivia,面試不考;學員答「沒帶 domain → Ingress 對應不上」= 機制正確,教練題目壞掉不是學員沒懂。結案) | - | - | 1
  - 正解三步:① curl 無 -H → Host 自動填 URL 主機名 ② 那串長 DNS ≠ `shop.com` ③ 字串比不上→無規則接→404。對照 `/apiv2`:Host 對但 Prefix 以斜線切段,`/apiv2`≠`/api` 段 → 掉 `/` catch-all → web。口頭型+需鷹架,+2 天格。

- 2026-08-04 | 分層判準:關掉 API Server 還在不在(工具卡,層級混淆家族的解藥) | (新卡,當堂 3/3 過,尚未冷測) | 對治「用 k8s 物件回答 kernel 問題」的通病 | unresolved | 3 | 2026-08-07 | 0
  - 判準:想像 etcd + API Server 被砍掉,node 上的 Pod 繼續跑,**誰還在?** 還在=kernel 的東西(iptables 規則、conntrack 表、路由表、veth/tunl0、cgroup、mount、namespace);消失=etcd 裡的資料(Service、Endpoints、Deployment、Pod 物件、NetworkPolicy 物件、PVC/PV、RBAC、Secret、ConfigMap)。**特例:RBAC 全程活在 API Server 的請求路徑上,kernel 一無所知**(C-4 再打開)。排障 payoff:症狀在 kernel 那欄就別再 `kubectl`,去 node 上用 `ip route` / `iptables-save` / `conntrack -L` / `findmnt`。08-07 冷測:給 5 個名詞分兩欄 + 講判準。
- 2026-08-04 | container 可寫層在硬碟不在 memory(overlayfs 三層) | 「process 死掉檔案去哪」答「存在 memory 就消失了」= 結論對機制錯 | 把 ephemeral 誤等於 in-memory;沒有「可寫層是硬碟上一個目錄」的實體概念 | unresolved | 3 | 2026-08-07 | 0
  - 正解:container 的 `/` 是 kernel 用 overlayfs **疊**出來的,不是一顆真磁碟。`lowerdir`=image 的 N 層,唯讀,**所有用同 image 的 container 共用**;`upperdir`=可寫層,**每個 container 自己一層**;全部實體位置在 node 的 `/var/lib/containerd/...`(硬碟)。消失的原因不是 memory,是 **upperdir 綁在 container 上,container 一刪那層陪葬,image 層留著給下一個用**。s24 親手驗:寫檔 → `kill 1`(送 SIGTERM 給 PID 1 = 模擬 crash,Pod 不動)→ 名字 IP 不變、RESTARTS+1、`cat: can't open`。三個延伸面試點(100 個 Pod 不佔 100 份 image / 啟動快 / Dockerfile 裡 rm 不會讓 image 變小)當堂教,未抽。
- 2026-08-04 | emptyDir 綁 Pod 不綁 container | 「emptyDir 撐不撐得過 kill 1」答「不在了」;同時不知道 `kill 1` 是什麼 | 三層階梯的中間一階沒有實體錨點,只有教練口頭列表 | unresolved | 3 | 2026-08-07 | 0
  - 正解:**撐得過**。路徑判準最好記 —— 可寫層在 `/var/lib/**containerd**/.../snapshots/<id>/`,emptyDir 在 `/var/lib/**kubelet/pods/<pod-uid>**/volumes/`,**路徑裡就寫著它綁誰**。`kill 1` 換 container、Pod uid 不變 → emptyDir 還在;`delete pod` uid 消失 → 才沒。生產坑:`emptyDir: {medium: Memory}` 是 tmpfs 且**算進 Pod 的 memory limit**,往 `/dev/shm` 猛寫會 OOMKilled(看起來在寫檔,實際在吃 cgroup 配額);真實用途三個:Secret volume 本身就是 tmpfs(不落盤)、`/dev/shm` 預設只有 64Mi 要加大、暫存 scratch。**s25 必須動手驗**(口頭已錯一次,直給後沒接動手 = 依 s16 實證會蒸發)。

## Spaced-repetition queue

<!-- 檢視序:過期優先、interval 小者優先;step A 每堂 ~2 題上限。term 卡到期日在 term-registry.md。 -->

- mistake:YAML-validation | mistake | 7 | 2026-06-30(過期)| active
- mistake:ImagePullBackOff | mistake | 7 | 2026-07-03(過期;07-09 已重抽 2/3,補「node 出網 i/o timeout」那類即可)| active
- mistake:dry-run-兩層 | mistake | 3 | 2026-07-20(s16 未口頭抽,但**真場景實用一次**:自寫 default-deny 用 `--dry-run=server` 抓到自己的 apiVersion 錯並讀懂 `no matches for kind ... in version` → 工具已進肌肉,精準版仍未收)| active
- mistake:三分類-家族卡 | mistake | 3 | 2026-07-22(**s18 counter 1/3**:零流量思想實驗全對、conntrack 站對「狀態」;第 2 輪換家族成員)| active
- mistake:L4-vs-L7 | mistake | 3 | 2026-07-22(**s18 新情境過但框架教練給**:postgres/redis 兩題連過、標籤貼反未重現;07-22 無框架第四情境〔禁 postgres/redis〕過了才推 7)| active
- mistake:NetworkPolicy-出廠全通 | mistake | 3 | 2026-07-23(s20 重抽半過:結論靠提示、「podSelector 只在自家 ns 選人」why 沒站住;與 CNI 卡同天再抽)| active
- mistake:default-deny-分層(DNS vs 連線)| mistake | 3 | 2026-08-06(**s23 口頭再未過**但 lab 兩死法親手集齊;抽「兩步先後+兩種 timeout 關鍵字」)| active
- mistake:跨-node-走路由表 | mistake | 3 | 2026-08-07(**s24 四抽未過**,答「查 svc」= 與 s22 完全相同的錯法。WR9 最高優先,改兩段問法)| active
- mistake:分層判準-關掉APIServer還在不在 | mistake | 3 | 2026-08-07(s24 新工具卡,當堂 3/3 過;當堂過不算保留,冷測定升降)| active
- mistake:可寫層在硬碟不在memory(overlayfs)| mistake | 3 | 2026-08-07(s24 新卡,親手驗過 kill 1)| active
- mistake:emptyDir-綁Pod不綁container | mistake | 3 | 2026-08-07(s24 口頭未過且未動手,**s25 必須動手驗**)| active
- mistake:veth-誤記跨node連線 | mistake | 7 | 2026-08-10(**s23 冷測過**:數字全對+tunl0 誘答咬住,推 7;但同日盲測站 2/6 仍蒸發,08-10 抽「旅程內出場」版)| active
- mistake:iptables-一棟樓 | mistake | 3 | 2026-08-06(**s23 半過**:換皮誘答咬住=吞餌史終結;但「nat 管路由」新錯法,重教後收。抽三表分工一句版+targetPort 5678 應用)| active
- mistake:kube-proxy-不在-Pod-啟動路徑 | mistake | 3 | 2026-08-07(**s24 首次重抽未過**,答「CoreDNS 嗎」= 寫進 resolv.conf ≠ 打過它)| active
- mistake:只給結論不給判準(pattern)| mistake | 3 | 2026-08-06(**s23 負樣本日**,連堂計數重置;08-06 續盯)| active
- mistake:NetworkPolicy-靜默無效 | mistake | 3 | 2026-07-31(過期,s23 未抽;**s22 F 段質變**:追問下自組完整鏈含「安全假象」自己的話;一段話冷測版過才 resolved,s24/WR9 抽)| active
- mistake:CNI-合約三件事 | mistake | 3 | 2026-07-23(s19 新卡:網卡/IP/路由 + 各自缺席的死法;hostNetwork 判準已自推不用重考)| active
- mistake:兩張獨立名單 | mistake | 3 | 2026-08-06(**s23 重抽未過**,三層提示未自產、直教兩道門模型;s24 動手版〔Step 5 自寫兩條 policy + 矩陣〕+ 08-06 口頭版)| active
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
