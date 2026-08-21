# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 29
- last_weekly_review: 18(**WR9 於 s25 開跑,s26/s27/s28/s29 均未跑,第五度未完成**;s28 的冷測三題只算壓縮版複習,不推進 last_weekly_review)
- last_session_date: 2026-08-21
- warm_up_classification: mid(有地圖形狀,缺演員名字;P0 剛好,不加速)
- **target_role: AWS Delivery Consultant(ProServe),2026-07-23 學員確認**。全部抽考包成客戶顧問情境、每題附 L6 範例答法(memory `aws-delivery-consultant-target` / `aws-mock-and-l6-answer-format`);戰略重排見 curriculum-plan §9。

## Current Session breakpoint

**s29 已收(2026-08-21,context `kind-k8s-coach-p2a`)。C-2 三個概念 chunk Recall + Transfer 已過，hands-on 主鏈完成，停在 reclaimPolicy teardown 尚未執行。** ① StorageClass 動態供應：能用「只有 rule 沒有 engine」解釋無 CSI provisioner 時 PVC Pending；EKS CSI controller Running + PVC Pending 情境先查 IAM，守住 `Running` 不等於功能正常。② WaitForFirstConsumer：能推出「EBS 不能跨 AZ attach → scheduler 先確定 Pod/node AZ → provisioner 同 AZ 建 EBS」；一度把既有 EBS 重新調度誤答成 WFFC，重教建立前定序 vs 建立後 PV nodeAffinity 後換皮通過。③ CSI 分工：能指出 attach 後仍需 node 端 kernel mount；Transfer 首答錯選 `get pvc` 查 mount，重教「PVC Bound 是控制面帳本、Pod Events 是 node 執行證據」後改選 `describe pod` 通過。④ Hands-on：安全 context 已驗；`standard`=`rancher.io/local-path`/`WaitForFirstConsumer`/`Delete`；自寫 PVC 時 `PersistenVolumeClaim` typo 由 server dry-run 抓出並修正；PVC 單獨 Pending 且 Events 明示 waiting for first consumer；自寫 Pod 的 `image:` 空格修正後，why-first 正確排出 scheduler→provisioner→Bound→mount；實測 Pod Running、PVC/PV Bound、`/data/message.txt`=`hello-from-storage`；provisioner log 明示在 worker 的 `/var/local-path-provisioner/...` 建卷與 `ProvisioningSucceeded`。⑤ `Immediate` AGE 判讀首答反了，重教後換皮通過。⑥ reclaimPolicy 一度誤以為 EBS 應保留，重教後正確以 PV 的 `persistentVolumeReclaimPolicy: Delete` 判定 PV 與後端資料皆刪。**next(s30)：不要重教；先讓學員執行已預測完成的 teardown：`kubectl delete pod sc-demo` → `kubectl delete pvc sc-demo` → `kubectl get pv`，再看 provisioner deletion log，完成 C-2 hands-on checkpoint；之後才跑 s28 遺留 G 題，冷測置尾。**

**s28 已收(2026-08-20,公司 bastion,context `kind-k8s-coach-p2a`)。距 s27 隔 10 天,走 Comeback Protocol。學員趕下班,G 段要求直接給正解後收工。**

本堂事實:

- **開場環境**:三台 NotReady、`crictl` 三台全 SLOW(containerd **第六次**卡死)。學員明說「你直接檢查環境」→ 鍵盤鐵律例外條款觸發,教練代跑。08-10 精準修法 `systemctl restart containerd` ×3,25 秒三台 Ready、Pod 未重排。宿主機 load 5.97/4 核心,兇手是**別人在跑 terraform/terragrunt**(同 s21 terraboard 形狀)。
- **冷測三題**:Q1 對照組(ALB 三台兩壞)**半過** —— 認出證據句「第三台完全正常」✅,判準句答不出、喊「直接説明」,直給;隨後應用題**立刻選 A(查 ALB access log)= 剛砍掉的那層**。Q2 `active`≠活著 **未過** —— 首答跑去講 DB(講別人壞不是講它自己壞)、二答「不是網絡嗎」,機制直給;接的 liveness 二選一**又選 `pgrep`**,梯子縮到最小才走通。中途 **liveness/readiness 動作對調**(答「繼續導入流量」),且答案兩種讀法要教練追問才定案(s25 同形狀第二次)。Q3 排障順序 **過**。
- ✅ **本堂最大正樣本:`restart` 排在採證前面這張卡,s21 以來第一次真的做對**。四動作排序把 `reboot` 排最後;B/C 初答倒置,給成本對比後自己改對並自帶判準「**比較簡單**」= pattern 卡無提示正樣本第 5 次(前四次:s22 站 7、s24 kernel 題、s25 PV/PVC、s26 upperdir)。
- ⚠️ **本堂主訊號(教學法層級,比知識點重要):判準句給完 30 秒內,下一題就套用不上,同堂兩次同形狀。** 不是記不住(兩次都能複述),是**沒把剛拿到的判準當工具用**。診斷:直給之後少了「當場用一次」那一步。已建 pattern 卡。
- **F 段跑了但散掉**:獨白首句「active 代表 process **順利執行**」= 把「存在」講成「順利執行」,正是整堂的病;第二輪出現與主題無關的碎片(「repo 的 parameter-store JSON」)→ 判定負荷/分心訊號,依安全閥縮成二選一「不在家 vs 在家但不接電話」→ **答對**,`DeadlineExceeded` vs `connection refused` 當場收。
- **G 段未作答**(學員趕時間),正解與 L6 版已給,**原題留 s29 重用**。
- **Scorecard tier2 1/4**(原理🟡 機制❌ 自己的話❌ MTTR✅)。
- 未跑:WR9(第四度)、story-bank(連八堂)、C-2 StorageClass。

next(s29),順序 —— ⚠️ **2026-08-20 學員拍板改制:新內容排最前面,複習/冷測壓到課堂尾巴**。理由:P2b 自 s26(08-06)起 14 天沒推進,每堂開場被「修叢集 + 複習」吃掉,新內容排最後就在疲勞時被砍;面試窗口約 09 中旬,舊節奏推不完。**冷測不砍**(隔堂測留存是唯一有效方法),只改排序,吃掉的是複習時間不是課程時間。學員選項 A(冷測留課堂尾巴)勝出,B(非同步冷測)未採用。

1. **開場先講今天做哪 3 件事,一次只推一件**(s28 照做有效,續用)。叢集若掛,直接下 `for n in control-plane worker worker2; do docker exec k8s-coach-p2a-$n systemctl restart containerd; done`,**不當教材、不排障**。
2. **主秀先跑:C-2 StorageClass / 動態供給 / CSI**(P2b;s26 已把 EBS CSI 概念鋪好)。
3. **G 段**:s28 未答的原題直接重用(12 個 Pod、3 個延遲 30 秒、`RESTARTS` 全 0、`exec: pgrep` probe;同時考對照組 + active≠活著 + 選指令)。
4. **尾巴才做冷測,3 題上限**:① 對照組判準一句版(換第三種皮)② `active` 為什麼不等於服務活著 ③ **liveness vs readiness 各自的動作(s28 退步卡,必抽)**。
5. ⚠️ **對治 s28 主訊號的硬規格:每給一個判準句,立刻接一題只有換皮的應用題,答對才算給完。** 不要等隔堂才發現沒套用。
6. **叢集**:9 天大、containerd 第六次(這次三台全 SLOW)。修法成熟但每堂都要修 → 評估改單節點 kind 降負載,或上課前避開跑 terraform。

<!-- schema: PROGRESS-SCHEMA.md §3 = 當前狀態 + 下一堂 resume,只留最新一堂。
     s26 及更早的斷點原文封存於 archive/breakpoint-history.md(冷檔,一字未刪);
     長效教練紀律在 session-log.md「教練執行紀律」。 -->

## Phase status

- P0 心智模型: gate-passed(2026-06-22;legacy,pre-Examiner,coach 認證)
- P1 核心物件 + 容器底層: gate-passed(2026-06-25;legacy,pre-Examiner,coach 認證)
- P2a 網路深水區: in-progress(chunk 1 Service/kube-proxy/CoreDNS ✅、chunk 2 Ingress ✅;chunk 3 NetworkPolicy in-progress〔3-1/3-2 教完;lab Step 4 於 s23 bastion 側重建完成(allow-dns + 兩死法實證),Step 5 兩道門模型已教、兩條 policy 未寫,剩 Step 5+6+gate+F/G〕;chunk 4 in-progress〔**4-1 CNI 合約 ✅ s19、4-2 veth ✅ s20、4-3 路由 ✅ s20、4-4 MASQUERADE ✅ s20**;**4-5 七站骨架盲講 ❌ s21 冷測 0/4 未過**〕。四塊零件備妥但串不起來;**4-5 背誦式重測已於 2026-08-11 退役,P2a gate 答案卷改情境排障題形式(curriculum-plan §10.2)**)
- P2b 儲存 + 權限: **in-progress**。**C-1 Volume/PV/PVC ✅ 完成(s26)**:三階梯壽命表一顆 `vol-demo` Pod 全部親手實證(L1 可寫層 / L2 emptyDir / L3 PVC,換 container 與 delete pod 兩種情境四格全驗),預測全中、機制自產(「pod 沒有換 container 換掉只有 upperdir 換掉」);執行體肉身摸到(`/proc/mounts` + node 上 `ls /tmp/pv-demo/`)。附帶收:PID 1 signal 保護、hostPath PV 落在 tmpfs 的意外、EBS AZ-scoped + `nodeAffinity` + `volumeBindingMode`。**C-1 唯一殘留**:`cg-demo` 的 `/sys/fs/cgroup/memory.max` 實際數字未讀到(s25 Pending,node 已修好,s27 補)。**C-2 StorageClass / dynamic provisioning / CSI 概念三 chunk ✅(s29)，hands-on 主鏈 ✅；只剩 `reclaimPolicy: Delete` teardown 實證。**
- P3 調度 + 高並發 + 排障: not-started
- P4 可觀測性工程: not-started
- P5 平台工程 / GitOps: not-started
- P6 面試衝刺: not-started

Weak-topic flags(**2026-08-03 首次啟用**,P2a 帶 flag 前進、gate 未考,學員決定):
- **七站封包全旅程**(4-5):盲測最佳 5/7,站 2/6 蒸發、「誰做的」缺席。**2026-08-11 改制(學員拍板,curriculum-plan §10.2):背誦式盲講全面退役**,不再進 step A / gate / WR;能力改以情境排障題驗收(「流量進不到 Pod,查給我看」型,併入 P3 排障 drill 與 P6 mock)。
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
- P2a CNI 封包全鏈 data plane(veth/路由表/MASQUERADE/conntrack): **low-med** (**s21 降級**:無鷹架七站冷測 0/4,只吐出 3 個碎片〔CoreDNS 的 ClusterIP / kube-proxy iptables / 回程 conntrack〕,漏 veth 出 Pod、過濾層、跨 node 路由、抵達對面 node。追問跨 node 第一個指令 → 答 iptables → 縮小重問 → 答 resolv.conf〔跨層〕。**s20 自己推出的排障尺「跨 node 不通查對面網段那行」三天後完全蒸發**。診斷:零件記憶 ≠ 旅程記憶,四塊各自驗過但從未串講。事後給正解 + L6 範例後親手 `ip route` 挑對 `192.168.20.192/26 via 172.21.0.2 dev tunl0`。s20 原始紀錄:一堂三 chunk 全親手驗:veth ifindex 兩頭互指、路由表三岔路〔via/dev 尺〕、MASQUERADE 換臉規則自讀出「Pod 打 Pod 不換」。排障尺〔跨 node 不通查對面網段那行〕經三段逼問鎖精準;conntrack 治標/治本仍需扶〔調 max=治標歸錯邊,s5/s6 老條〕。**未經無鷹架冷測**;(2026-08-11 改制)升 high 判準改為情境排障題過關,盲講退役。**s22 重建**:鷹架版七站全走完;無鷹架盲測 #2 5/7 未過(幻影站 4 DNAT 重複+站 6 進門蒸發,兩錯輕提示下自我診斷)但 vs s21 的 3 碎片是實質進步;四動詞口訣「問名→改寫→放行→送達」取代四層名詞;s23 開場冷測 #3 定升降。**s23 盲測 #3:3.5/7 未過**(6 天留存:站 2/站 6 蒸發=veth 的兩次出場、七行紀律垮、「誰做的」只剩站 1;幻影站 4 未復發、kube-proxy 不碰封包的存疑自發。當日重建:veth 卡冷測過、站 6 當場重組成功。盲測 #4 s24 開場)

- **分層判準「關掉 API Server 還在不在」**(對治層級混淆家族): med (s24 新造工具,當堂 3/3 過且兩題無提示自答〔「沒有,因為 CNI 不支援」「可以,因為直接修改 kernel」〕。左欄=kernel 真東西〔iptables/conntrack/路由表/veth/cgroup/mount/namespace〕,右欄=etcd 資料〔Service/Deployment/PVC/NetworkPolicy/RBAC/Secret〕;RBAC 是特例〔純 API Server 層,kernel 一無所知〕已埋未教。**s25 隔堂冷測:判準句無提示自產 ✅**(補上 s24 收工回想時的「不知道耶」),分欄 4/5;唯一錯 cgroup memory limit〔自述「我在想的是 yaml 的 limit」〕。**卡升級成兩步版**:每個 k8s 資源都有兩個分身,先問「宣告還是執行體」再判層。維持 med,08-08 抽兩步版)
- **P2b C-1 三階梯壽命(可寫層 / emptyDir / PVC)**: **med-high** (s26 一顆 Pod 四格全實證,兩次預測全中,機制無鷹架自產「pod 沒有換 container 換掉只有 upperdir 換掉」、精準版補「沒換的是 Pod UID」;F 段追問下再產「因為路徑存在 container id 底下的資料夾」。**s24 答錯的 emptyDir 那階已翻正並有肌肉記憶**。未升 high 的理由:F 段獨白純結論無機制、`delete pod` 那格的「因為」偏薄、當堂過不算保留,08-13 冷測定升降)
- **PID 1 signal 保護**: med (s26 意外實證:`kubectl exec -- kill 1` → `RESTARTS 0`、檔案全在。kernel 對 PID 1 不套用無 handler 的預設動作,同 namespace 內連 SIGKILL 都擋,只有祖先 namespace 殺得掉〔`crictl stop` 實證〕。三個生產對應已教:30 秒 grace period、rollout 硬殺斷線、Dockerfile shell form → `tini`。**全程教練驅動,學員只跑指令,未經任何抽考**,08-09 首抽)
- **EKS 儲存拓撲(EBS AZ-scoped / nodeAffinity / volumeBindingMode)**: med (s26 學員**主動提問**引出。定調句「儲存有位置,計算沒有;位置必須寫進 API 物件否則 scheduler 一無所知」。Transfer 過:`Immediate` 先開 EBS 後排 Pod → `volume node affinity conflict` 永遠 Pending,順序倒過來就是 `WaitForFirstConsumer`。⚠️ **當堂剛教的鷹架下複述**,08-09 換情境冷測)
- **P2b C-1 可寫層 / overlayfs**: med (s24 親手實證:讀 `/proc/mounts` 認出 lowerdir 15 層共用 vs upperdir 1 層獨有、全在 `/var/lib/containerd`;`kill 1` 三個預測全中。起手誤答「存在 memory」= 結論對機制錯。**emptyDir 綁 Pod uid 那一階口頭未過且 s25 仍未動手**。判準句:路徑裡就寫著它綁誰)
- **P2b C-1 PV/PVC 解耦**: med (s25 親手:PVC `Pending` → `get pv` 空 → 認出靜態供給痛點 → apply PV → 立刻 `Bound`。三實證:CAPACITY 顯示 1Gi 不是 500Mi〔capacity 是下限、綁定不切割〕、**node 全 NotReady 照樣 Bound**〔媒合是 control plane 帳本作業〕、Retain 已埋。Transfer 過且自帶「因為」+ 自己追問設計理由。誤解「PV 1:多」已當場更正為三層關係 `SC 1:多 PV 1:1 PVC 1:多 Pod`;RWO 限制的是 node 不是 Pod 數已教。**當堂過不算保留**,08-08 冷測。實體掛載那一階〔Pod 掛 PVC → 刪 Pod → 檔案還在 → `findmnt`〕未做)

## Scorecard history

<!-- 轉換規則:原 ✅=1、🟡/❌=0,原符號保留在註記。legacy = pre-Examiner 時期由教學 coach 認證。 -->

- 2026-08-20 | 冷測三題 + F 段折算 (s28, tier 2) | 1/4 | **判準句給完 30 秒內套用不上**(Q1 剛砍掉 ALB 層→立刻選查 ALB log;Q2 剛講完 systemctl 只驗第 1 層→立刻選 pgrep probe)。對策:每給一個判準,當場接一題換皮應用題,答對才算給完 | **排障順序題把 `reboot` 排最後**,restart-vs-採證這張卡 s21 以來第一次真的做對,而且 B/C 順序自己改對還自帶判準「比較簡單」 | coach(原理🟡〔Q3 成本判準自產,Q1/Q2 判準全部直給〕 機制❌〔active≠活著未過、liveness/readiness 動作對調〕 自己的話❌〔F 段獨白首句就把「存在」講成「順利執行」,第二段散掉〕 MTTR✅〔Q3 過〕。**G 未作答**(學員趕時間),不折算)
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
- 2026-08-05 | WR9 主題1 + C-1 lab 折算 (s25, tier 2) | 2/4 | **排障的「選指令」那一步**:Pending 問「你的第一個排查指令是什麼」→ 「不知道 直接開始今天的課程吧 拖太久了」,連三堂沒給出任何方向。注意學員**願意跑教練指定的指令、不願意自己選指令** → s26 起改用三選一候選指令建立肌肉,不再問開放式 | 「pvc-demo-2 會是什麼狀態?」→ **「pending 因為沒有 PV 了,因為 PV to PVC 是一對一的,所以就算 PV 有 1G、目前一個 PVC 使用 500,剩下的 500 也不能拿出來使用」**,判準句自帶「因為」且**主動追問「為什麼要這樣設計」**,是 pattern 卡第三次無提示正樣本 | coach(原理✅〔分層判準句無提示自產,補上 s24 收工說不出來的洞〕 機制🟡〔「誰把 limit 寫進 cgroup」答 scheduler = 控制面元件碰不到 kernel 的大破口;但 PV/PVC 媒合機制與靜態供給痛點自己認出〕 自己的話✅ MTTR❌。**G 未跑、F 未跑(連五堂)**,以 WR9 主題1 + PV/PVC lab 折算)
- 2026-08-10 | **s27 無 scorecard(F/G 未跑,學員疲勞收工)** | 不計分 | — | — | coach(僅記可引用事實,不折算分數:**MTTR 有真實正樣本但摻教練驅動** —— 五次故障以來第一次採證先於 restart、完整證據鏈成立,**但每一發指令都是教練指定,學員零自選**;答題面兩次錯〔scheduler 當萬用嫌犯第 2 次、NotReady 產生者選 A〕;why-first 連跳 3 次。**信度低,不宜當 tier 2 分數採用**:整堂是教練帶著走的排障示範,不是學員獨立表現)
- 2026-08-06 | step G (s26, tier 2, **正式版一題**,自 s21 以來首次) | **3/4 — 通過(自 s18 以來首次)** | **F 段獨白**:對「完全沒碰過容器」的新同事開口就是 container/emptydir/pv 三個名詞 + 三句結論,零機制;機制被追問就出得來 = 差的是「先講機制再講名詞」。顧問工作一半是對非專家講話,這條在 ProServe 直接可見 | **誘答那一題**:菜鳥說「不刪 pod 就永遠安全吧」,沒點頭,而且拿三分鐘前才意外發現的 tmpfs 當武器反駁 = 當堂新知識立刻遷移成防禦 | coach(原理✅〔「pod 沒有換 container 換掉只有 upperdir 換掉」無鷹架自產〕 機制✅〔WaitForFirstConsumer 順序完整鏈〕 自己的話✅〔三句無鷹架機制句〕 MTTR🟡〔G 段方向對「查 Pod 生命週期不查 code」= 連四堂 ❌ 後首次回升,但漏掉「凌晨兩三點」決定性線索,且**整堂沒主動說出過任何一個指令**,開場還選「先 restart 試試」〕。F 段已跑、G 段正式版已跑,無折算)
- 2026-07-28 | step G 折算 (s22, tier 2, 盲測 #2 + F 段) | 1/4 | 「誰做的」欄要長在骨架裡,每站一個負責人;iptables=一棟樓(nat 改寫/filter 過濾)當日教過仍吞誘答 | F 段自組靜默無效鏈「不會報錯,但預期 DB 有保護、實際沒有」+ 站 7 無提示判準句「改 src 因為 Pod A 不認識 PodB-IP」 | coach(原理🟡 機制🟡 自己的話✅ MTTR❌。盲測純冷信度高;F 段帶問題鷹架)
- 2026-07-23 | step G (s21, tier 2, **AWS Delivery Consultant 面試模擬首場**) | 0/4 | 判準句缺席:三次只給結論(kube-proxy yes/no、選路由那行、CIDR「不用特別算」),第六堂同條 | 回程 conntrack 主動講出來,無提示,而且那是 gate 歷史漏點清單上的站 | coach(原理❌ 機制❌ 自己的話❌ MTTR❌。七站只給 3 碎片;MTTR 兩次選錯指令且第二次跨層到 DNS。**信度高**:純冷測、教練全程未給鷹架)
- 2026-07-17 | A 段+chunk3 gate (s16, tier 2) | 1/4 | 判準/機制講不出:L4-L7 兩度結論對理由錯;分工句未收 | conntrack 去程/回程兩欄位**自產**(給框架不給答案,s15 直給後蒸發,今日一次推出) | coach(原理❌ 機制🟡 自己的話❌ MTTR 未演練。**本場信度低**:教練犯三錯〔過度抽考/考未教內容/搶鍵盤〕,低分含教練污染,不宜單獨採信,s17 WR 重測)

## Mistake Registry

<!-- 欄位:date | topic | what-was-wrong | root-cause-tag | status | interval | next-review-date | unresolved-session-count
     interval 2 = +2 天臨時複習格(口頭型 resolved,過了才進 3/7/14)。
     unresolved-session-count 於遷移時依複測紀錄初始化(近似值)。 -->

- 2026-06-18 | YAML validation | `matchLabels` 打成 `metaLabels`,不會讀 strict decoding error | 不知道 unknown-field 路徑=藏寶圖、驗證發生在 API Server | unresolved | 7 | 2026-06-30 | 2
  - 正解:讀 `unknown field "A.B.C"` 完整路徑回檔案定位;selector 認親欄位是 `matchLabels` 且必須等於 template.metadata.labels。06-23 抽考需引導才答對「檢查在 API Server、與 etcd 無關」,推 +7。**s23 實戰現形**:allow-dns 重寫把 selector 塞進 ports 清單,dry-run 前自行「猜修」把 apiVersion 改成大寫 V1(`no matches for kind ... in version` 第二次親手撞,s16 同款),拿到錯誤後學員選擇跳過讀圖、教練代打。讀圖 rep 仍欠,WR9 用帶錯 YAML 現場讀圖。**s25 rep 首次自己讀圖過關**:`strict decoding error: unknown field "spec.sccessModes"`,教練只說「訊息把座標給你了」,學員**自己回檔案找到打錯的字並改對**,apply 成功 —— 建卡以來第一次不用代打。但同一段稍早學員說「直接給我 yaml」跳過自寫 PVC,rep 打折,故留 3 不推 7;08-08 換一個不同型別的錯(`cannot unmarshal` 或 enum 大小寫)再測一次,過了才 resolved。
- 2026-06-22 | probe 職責 | 把 readiness 的「準備好接流量」塞給 liveness,延伸成 liveness 查 DB | 沒抓住兩種 probe 失敗後動作不同(重啟 vs 切流量) | unresolved | 7 | 2026-07-10 | 1
  - 正解:判斷句「Would a restart fix this?」;liveness 查 DB → DB 一慢全 Pod 集體重啟雪崩 + reconnection 風暴。06-25、07-03 兩次抽考 PASS(07-03 自己講出正回饋迴圈+羊群效應,唯英文詞 thundering herd 忘了),推 +7。
- 2026-06-23 | ImagePullBackOff | image 打成 `ngimx:1.25`,apply 成功卻卡 ImagePullBackOff,不解 | 驗證有邊界:API Server 只驗語法,repo 存不存在要 kubelet 第 5 棒拉了才知 | unresolved | 7 | 2026-07-03 | 1
  - 正解:第一動作 `describe pod` 看 Events;分三類訊號:`i/o timeout`=網路/egress、`401`/`toomanyrequests`=認證限流、`repository does not exist`=名稱 tag 錯。06-26 抽考三類一次答全對推 +7;07-09 A 段重抽 2/3(漏 node 出網 i/o timeout,下次補)。
  - **s26 真場景現形但 rep 不算數**:`image: buybox` 打錯 → `ImagePullBackOff` → 三選一答 **C 正確**,但**要了兩次都沒貼 Events 關鍵字**。教練已當場點名「這題你不看 Events 也猜得到,因為是我先告訴你 image 打錯的」。**不推 interval,留 3**,08-09 換一個學員不知情的故障(建議用 `401` 或 `i/o timeout` 型),要求先貼 Events 再分類。顧問價值已教:三類的處理人不同(A 網路組 / B 平台憑證 / C 寫 YAML 的人),`describe pod` 第一眼就要分流到對的人。
- 2026-06-27 | ClusterIP/kube-proxy/DNAT 全鏈(謎題B) | 「封包先去 ClusterIP 拿 IP」誤解 + 手(iptables)vs 名單(Endpoints)混 | ClusterIP 不是地方、封包從不拜訪它,改寫發生在出發地本機 kernel | resolved | 14 | 2026-07-13 | 0
  - 正解一句話:封包不去 ClusterIP;出發地本機 kernel 照 kube-proxy 寫的規則做 DNAT,把目的地換成 Endpoints 名單裡的真 Pod IP。06-28 D 段 iptables-save 實體追鏈 + F 段無鷹架 teach-back PASS;06-29 WR 二度冷測 PASS=封印,推 +14。下次抽全鏈精度:誰寫 resolv.conf=kubelet、KUBE-SVC 機率 LB 怎麼挑 SEP、conntrack 回程反向改寫。
- 2026-06-28 | 叢集 DNS 排障 | busybox nslookup NXDOMAIN 差點誤判 CoreDNS 壞 | 排障第一刀「先用 FQDN 二分伺服器壞 vs 發問端壞」沒長成肌肉 | unresolved | 3 | 2026-07-10 | 3
  - 正解:FQDN 通 → CoreDNS 沒事查 client/resolver;測叢集 DNS 用 netshoot 不用 busybox(musl search 處理不可靠);絕不因 nslookup 失敗就重啟 CoreDNS。07-01 抽考層級混淆(把 conntrack 拉進 DNS 題);07-07 提早再測第一刀一時忘記、給梯子後定位對 → 口頭型+需鷹架,拉回近期。
- 2026-07-03 | dry-run 兩層 + Service port | `--dry-run=client` 綠燈騙人;port vs targetPort 靜默不通 | client 只做本機淺檢查;strict decoding 在 API Server(server 端) | unresolved | 3 | 2026-07-17 | 3
  - 正解:驗 YAML 用 `--dry-run=server`;port=門牌、targetPort=container 實際聽的 port,填錯=DNAT 送到沒人聽的 port→connection refused。07-06 抽考半過:client=本機查語法✅,但 server dry-run 答成「走完 etcd 整個流程」=第三次在 etcd 角色滑掉(已釘:審查在櫃檯、落帳才算數;server dry-run=審完不落帳)。07-14 重抽半過:「不會碰 etcd」站住(三滑後首次)✅,但「停在哪一步」精準版沒自收、etcd 三分類(=資料)未自答即喊繼續,教練補完。07-17 只收精準版。
  - **s26 實戰現形 + 新形狀命名**。學員自寫 YAML 打成 `image: buybox`,教練明講「故意不改」→ 預測二選一「dry-run 會不會抓到」→ **答 B(綠燈)✅ 且實測綠燈 → apply 成功 → `ImagePullBackOff`**,分界線親手做出來。但追問「為什麼攔不到」→ 答「**因為 server dry-run 不會實際去查有沒有這個 image**」= **把「攔不到」換句話說,同義反覆,不是判準**。
  - 新的檢驗法(已教,對治整個 pattern 家族):**判準句講完,對方有沒有拿到一個新事實?**「因為 A 不會做 B」沒有新事實;「誰做、在哪一棒」才有。
  - 精準版:**image 存不存在只有 kubelet 在 node 上真的去拉時才知道;API Server 從頭到尾不碰 registry,它只驗 schema 和 admission。** 回扣 P0 五棒:`--dry-run=server` = 審完不落帳,連第 2 棒都沒走到;拉 image 是第 5 棒。留 3,08-09 抽精準版(要求答出「誰」與「第幾棒」)。
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
  - **s26 明顯正向,但出現新形狀**。正面:預測題**全部作答無一跳過**(s24 連跳三次的洞補上);三句無鷹架機制句(「pod 沒有換 container 換掉只有 upperdir 換掉」/「因為路徑存在 container id 底下的資料夾」/ AZ 順序完整鏈)。負面兩處:① **同義反覆**(dry-run 題「因為它不會去查」= 把問題換句話說,已命名並給檢驗法「對方有沒有拿到一個新事實」)② **F 段獨白純結論**(對完全不懂容器的人只丟三個名詞加三句結論,機制要追問才出來)。
  - 註:s26 的 EKS 順序題雖自帶「因為」,但屬**當堂剛教 + 教練指定「用順序講」的鷹架下複述,不計入無提示正樣本**。無提示正樣本累計:s22 站 7、s24 kernel 題、s25 PV/PVC 1:1、**s26 upperdir 句**。08-09 續盯,新增盯點=**有沒有同義反覆**。
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

- 2026-08-04 | 分層判準:關掉 API Server 還在不在(工具卡,層級混淆家族的解藥) | s25 冷測 4/5:cgroup memory limit 誤放右欄,自述「我在想的是 yaml 的 limit」 | 同一個名詞的兩個分身(宣告 vs 執行體)沒有分開 | unresolved | 3 | 2026-08-08 | 1
  - 判準:想像 etcd + API Server 被砍掉,node 上的 Pod 繼續跑,**誰還在?** 還在=kernel 的東西(iptables 規則、conntrack 表、路由表、veth/tunl0、cgroup、mount、namespace);消失=etcd 裡的資料(Service、Endpoints、Deployment、Pod 物件、NetworkPolicy 物件、PVC/PV、RBAC、Secret、ConfigMap)。**特例:RBAC 全程活在 API Server 的請求路徑上,kernel 一無所知**(C-4 再打開)。排障 payoff:症狀在 kernel 那欄就別再 `kubectl`,去 node 上用 `ip route` / `iptables-save` / `conntrack -L` / `findmnt`。
  - **s25 升級成兩步版(取代單步版)**:**每個 k8s 資源都有兩個分身** —— Service 物件 / DNAT 規則、PVC 物件 / node 上的 mount、`resources.limits` / cgroup `memory.max`、NetworkPolicy 物件 / filter 表規則。**① 先問你講的是宣告還是執行體 ② 宣告在 etcd、執行體在 kernel。** 中間把宣告翻成執行體的是各種 controller/agent(kube-proxy、felix、kubelet)。定調句:**API Server 掛掉 = 沒有新的翻譯了,不是已經翻好的東西消失了。**
  - s25 正面:**判準句本身無提示自產**(s24 收工回想答「不知道耶」的洞補上)。負面:首答用兩套詞(1、3 寫 kernel,2、4、5 寫「可以」)導致答案有兩種相反讀法 = pattern 卡「只給結論不給判準」的新形狀。08-08 抽兩步版:給一個名詞先問「宣告還是執行體」,再問住哪層。
- 2026-08-05 | 誰把 limit 寫進 cgroup、什麼時候寫 | 「客戶改了 limit 但 Pod 還在 OOMKilled,誰負責把新數字寫進 cgroup?」→ 答 **「scheduler 嗎」** | 控制面元件與 node 上元件的職責混淆(層級混淆家族);不知道 cgroup 只在建 container 那一刻寫 | unresolved | 3 | 2026-08-08 | 0
  - 正解:**kubelet**(→ CRI/containerd → runc 實際寫)。判準句:**不在 node 上的元件碰不到 kernel** —— scheduler 只做一件事,從一堆 node 挑一台把 `spec.nodeName` 填進 Pod 物件,**它只改 etcd 的一個欄位,連 node 的門都沒進過**;API Server、controller-manager 同理。回扣 P0 五棒:第 3 棒之後才有人碰得到 kernel,而那個人只有 kubelet 那一路。
  - 時機:**只在建立 container 的那一刻寫**,container 活著的期間數字就定死。所以「改了 limit 還是 OOMKilled」的完整診斷:① 改的是宣告 ② `kubectl get deploy -o yaml` 讀回來的還是宣告(等於查自己剛寫的字,證明不了現況)③ 舊 Pod 的 container 沒重建 → kubelet 沒有第二次寫的機會 ④ rollout 卡住的原因很多(quota / PDB / image / paused),但根因形狀只有一個:**宣告改了、執行體沒重生**。排障順序:`kubectl get pod <實際那顆> -o yaml` → 直接讀 node 上的 cgroup。
  - L6 顧問版:"Editing the spec only changes the desired state. The limit doesn't reach the kernel until kubelet recreates the container, so I'd check the running pod, not the deployment."
  - 延伸(s25 已答對,未單獨建卡):`/sys/fs/cgroup/memory.max` 讀出來是 `67108864` 不是 `64Mi` —— **cgroup 是 kernel 介面,介面只講 bytes**。**實際數字 s25 未讀到(Pod Pending),s26 補驗。**
- 2026-08-05 | LVM 三層 + 擴容四步(學員課後自己要求復習,foundational pull) | Q1/Q2 結論皆對但**兩題都只給結論**(Q1「需要 resize」、Q2「還是成立」),追一刀後 Q2 機制自產 | 判準句慣性省略(pattern 卡);LVM 的 PV 與 k8s 的 PV 同名不同物 | unresolved | 3 | 2026-08-08 | 0
  - 三層:**PV**(實體卷=一顆磁碟/分割區,被 LVM 徵收)→ **VG**(卷組=多個 PV 合成的池)→ **LV**(邏輯卷=從池切出來、檔案系統蓋在上面的假磁碟)。⚠️ **LVM 的 PV ≠ k8s 的 PV,同名不同物**。存在理由=實體磁碟大小固定、位置固定(分割區起訖寫死),**加一層間接層**,與 PVC↔PV 同手法。
  - **擴容四步,一步都不能跳**:`pvcreate` → `vgextend` → `lvextend` → **`resize2fs`/`xfs_growfs`**。第 4 步最多人漏,因為**容量寫在檔案系統自己的 superblock 裡,下面那層變大它不知道**(症狀:`lvs` 變了、`df -h` 沒變)。`lvextend -r` 可一次做完 3+4,但要講得出是兩層。
  - **雲上版**:EBS 自己能線上擴容 → LVM「湊出更大空間」的價值被吃掉,EKS 上多半直接 `mkfs` 在 `/dev/nvmeXn1` 上,沒有 LVM 那層。**但第 4 步永遠躲不掉**(EBS 100G→200G 後仍要 `xfs_growfs`,否則 `df -h` 不動)= EKS node 磁碟滿掉最常見的假故障。LVM 在雲上僅存兩用途:多顆 EBS 條帶化衝 IOPS、snapshot 一致性備份。
  - **Q2(疊層題,學員答對且自帶機制)**:「k8s PV 底下是 LV,1:1 還成不成立?」→ 成立。學員自產「storage 的寫入沒辦法完美切開,寫到別人的會資料損毀」+ **未經提示自己接到「EKS 上不會靜態宣告 PV,CSI driver 收到 PVC 就生對應的 PV」**。精準版(教練補):**LVM 可以切,但切出來是兩個獨立 LV = 兩個獨立塊裝置 = 兩張 PV,切割發生在 k8s 看不到的下面一層。**
  - Q1 順帶收:「EBS 改大重開機就生效?」→ 錯,**要擴的不是磁碟層是檔案系統層**。教練點名這是**「兩個分身」判準第三次換皮出現**(EBS 實際大小 vs 檔案系統以為的大小)。
- 2026-08-05 | PV ↔ PVC 是 1:1 獨佔 | 學員自曝「我以為是 PV 1:多」 | 「一份儲存給多人用」的直覺貼錯層(該直覺屬於 PVC→Pod,不屬於 PV↔PVC) | unresolved | 3 | 2026-08-08 | 0
  - 三層關係:**`StorageClass ─1:多→ PV ─1:1→ PVC ─1:多→ Pod`**。PV 被綁走即整張鎖死,`CLAIM` 欄只寫得下一個名字,多出來的容量誰也拿不走(s25 實證:PVC 要 500Mi,`get pvc` 的 CAPACITY 欄顯示 **1Gi**)。
  - **為什麼是 1:1(第一性)**:PV 背後通常是**塊裝置**,檔案系統假設自己獨佔整個裝置(自管 inode/free block/journal),兩個互不知情的 fs 寫同一顆裝置 = 資料毀掉;k8s 這層沒有切割裝置的機制(那是 LVM/分割區的事)。**1:1 不是 k8s 訂的規矩,是塊裝置特性浮到 API 上。** 反之 NFS/EFS 是目錄樹不是塊裝置 → 天生能共用 → 才有 RWX。**能不能 RWX 取決於底層是塊還是檔案系統**(面試點)。
  - **RWO 常見誤解**:RWO 限制的是 **node** 不是 Pod 數,同一台 node 上排十顆都掛得到。
  - 實務註記:靜態供給才會有「1Gi 配 500Mi 浪費」的問題;動態供給(EKS + EBS CSI)PVC 要多少就開多少,結構上不存在。s25 Transfer 已過(含「因為」),**當堂過不算保留**,08-08 冷測。
- 2026-08-04 | container 可寫層在硬碟不在 memory(overlayfs 三層) | 「process 死掉檔案去哪」答「存在 memory 就消失了」= 結論對機制錯 | 把 ephemeral 誤等於 in-memory;沒有「可寫層是硬碟上一個目錄」的實體概念 | unresolved | 3 | 2026-08-07 | 0
  - 正解:container 的 `/` 是 kernel 用 overlayfs **疊**出來的,不是一顆真磁碟。`lowerdir`=image 的 N 層,唯讀,**所有用同 image 的 container 共用**;`upperdir`=可寫層,**每個 container 自己一層**;全部實體位置在 node 的 `/var/lib/containerd/...`(硬碟)。消失的原因不是 memory,是 **upperdir 綁在 container 上,container 一刪那層陪葬,image 層留著給下一個用**。s24 親手驗:寫檔 → `kill 1`(送 SIGTERM 給 PID 1 = 模擬 crash,Pod 不動)→ 名字 IP 不變、RESTARTS+1、`cat: can't open`。三個延伸面試點(100 個 Pod 不佔 100 份 image / 啟動快 / Dockerfile 裡 rm 不會讓 image 變小)當堂教,未抽。
  - **s26 二度實證且機制自產**:`crictl stop` 換 container → `/root/f.txt` 消失,同時 emptyDir / PVC 兩層都活。學員無鷹架講出「**pod 沒有換,container 換掉,只有 upperdir 換掉**」,F 段追問下再產「**因為路徑存在 container id 底下的資料夾**」。精準版補完:**不是有人跑去刪那個檔案,是新 container 拿到一個全新的空 upperdir,舊那層跟舊 container 一起被丟掉。** 推 7,08-13 冷測連同三階梯一起抽。
- 2026-08-04 | emptyDir 綁 Pod 不綁 container | 「emptyDir 撐不撐得過 kill 1」答「不在了」;同時不知道 `kill 1` 是什麼 | 三層階梯的中間一階沒有實體錨點,只有教練口頭列表 | unresolved | 3 | 2026-08-07 | 0
  - 正解:**撐得過**。路徑判準最好記 —— 可寫層在 `/var/lib/**containerd**/.../snapshots/<id>/`,emptyDir 在 `/var/lib/**kubelet/pods/<pod-uid>**/volumes/`,**路徑裡就寫著它綁誰**。`kill 1` 換 container、Pod uid 不變 → emptyDir 還在;`delete pod` uid 消失 → 才沒。生產坑:`emptyDir: {medium: Memory}` 是 tmpfs 且**算進 Pod 的 memory limit**,往 `/dev/shm` 猛寫會 OOMKilled(看起來在寫檔,實際在吃 cgroup 配額);真實用途三個:Secret volume 本身就是 tmpfs(不落盤)、`/dev/shm` 預設只有 64Mi 要加大、暫存 scratch。**s25 必須動手驗**(口頭已錯一次,直給後沒接動手 = 依 s16 實證會蒸發)。
  - **s26 動手驗過,翻正 ✅**:一顆 `vol-demo` Pod 三層同掛,`crictl stop` 換 container → emptyDir 檔案還在;`delete pod` → 沒了。機制自產「pod 沒有換 container 換掉只有 upperdir 換掉」,精準版補完「沒換的是 Pod UID」。推 7,08-13 冷測(問法:emptyDir 撐得過什麼、撐不過什麼、路徑判準)。

- 2026-08-06 | 排障:restart 排在採證前面(MTTR / 治標 vs 治本第三次同形狀) | 三台 node NotReady,三選一(A 看 node Conditions / B 看宿主機 / C 直接 restart)→ **選 C,理由「看起來是 notready 先重啟試試」** | 「先試試」不是診斷;不知道 restart 會同時清掉症狀與證據 | unresolved | 3 | 2026-08-09 | 0
  - 正解:**採證(A/B)一定排在清理現場(C)前面**。restart/reboot 修的是症狀,而且把根因證據一起洗掉。學員自己的歷史就是證明:s21 倒 → restart → 好了 → 沒人知道為什麼;s24 倒 → 沒處理;s25 倒更慘 → 沒跑;s26 宿主機重開機 → 好了 → **s25 那次的真兇永遠查不到**。四次倒下,四次從零猜。
  - 判準句:**能重現的東西可以晚點修,不能重現的東西必須當場採證。**
  - L6 顧問版:"A restart clears the symptom and the evidence at the same time. I'd capture node conditions and kubelet logs first, then restart — otherwise the same incident comes back next week and we're starting from zero."
  - 08-09 抽:給一個 node NotReady 情境,要他排出「先做什麼、再做什麼」的順序 + 講出為什麼 restart 不能第一個。

- 2026-08-06 | PID 1 的 signal 保護(kernel 層,新知識卡) | 學員未答錯,是實驗意外撞出來:`kubectl exec vol-demo -- kill 1` → `RESTARTS 0`、檔案全在,container 根本沒死 | 全程教練驅動,學員只跑指令,**未經任何抽考** | unresolved | 3 | 2026-08-09 | 0
  - 機制:**Linux kernel 對 PID 1 有特殊保護 —— 一個 signal 若沒有安裝 handler,PID 1 收到時不套用「預設動作」,直接忽略。** 一般 process 收 SIGTERM 無 handler = 終止;PID 1 = 什麼都不發生。原因:PID 1 是 init,init 死掉整個 PID namespace 崩掉。**這個保護連 SIGKILL 都算,只要 signal 來自同一個 PID namespace 內部**;只有祖先 namespace(node 那層)送得進去。s26 實證:`docker exec <node> crictl stop $(crictl ps -q --label io.kubernetes.pod.name=vol-demo)` 才殺得掉。
  - 本例 PID 1 是 `sleep`,從不註冊 SIGTERM handler,所以 signal 被丟掉。(s24 net-tool 的 `kill 1` 有效 = 那顆 image 的 PID 1 不同,不是矛盾。)
  - **三個生產對應(面試高頻)**:① `kubectl delete pod` 每次都等滿 30 秒 = kubelet 送 SIGTERM 被忽略 → 等 `terminationGracePeriodSeconds` 到期 → 從外面送 SIGKILL。② 每次 rollout 斷線 / 交易沒寫完 = app 從沒收到 SIGTERM,沒機會 graceful shutdown。③ Dockerfile 用 shell form(`CMD npm start`)→ PID 1 變 `/bin/sh`,**sh 不轉發 signal 給子行程** → 解法是 exec form(`CMD ["node","server.js"]`)或塞 `tini`/`dumb-init` 當 PID 1 負責轉發與收屍。
  - 08-09 抽:「為什麼你的 Pod 刪除總是要等 30 秒?」+ 「同一個 container 裡 `kill -9 1` 殺不殺得掉?為什麼?」

- 2026-08-06 | Pod 不會「重啟」,只會被丟掉重建 | F 段菜鳥追問「pod 不是我建的嗎?我不刪它,它為什麼會自己不見?」→ 答 **「pod 會重啟 or 調節 編排」** = 方向對,講不出誰在什麼條件下動手 | 把 Pod 當成一個會重啟的長壽物件(寵物),而不是可拋棄的一次性單位 | unresolved | 3 | 2026-08-09 | 0
  - 正解:**Pod 沒有「重啟」這回事,它只會被丟掉、由 controller 生一顆全新的(新 UID)。** `RESTARTS` 那一欄數的是 **container** 的重啟次數,不是 Pod 的。學員自己 s26 的輸出就是證據:`RESTARTS 1 (5s ago) AGE 7m33s`(container 換了 Pod 沒換)vs delete 後 `AGE 3s`(全新 Pod)。
  - **五種不需要任何人動手、Pod 就會消失的情況**:① node 掛掉/失聯 >5 分鐘 → node-lifecycle controller 標記刪除 ② node 記憶體或磁碟不足 → **kubelet 主動 evict** ③ `kubectl drain`(升級/縮容)④ 高優先級 Pod 進來 → scheduler **preemption** ⑤ HPA 縮容 / 任何一次 rollout。
  - 定調句:**Pod 是牲口不是寵物(cattle, not pets)。你不刪它,叢集隨時會替你刪。** 推論:emptyDir 的正確定位只有 scratch space(快取、暫存、`/dev/shm`),跟你手不手動刪 Pod 無關。
  - 08-09 抽:「不刪 Pod 的話,emptyDir 就安全嗎?」要他數出至少三種自動消失情境。

- 2026-08-06 | 持久性看「掛在哪」不看名字(兩個分身判準第四次換皮) | 學員未答錯,是 `/proc/mounts` 意外撞出來:`/scratch`(emptyDir,號稱短命)→ `/dev/nvme0n1p1` **xfs 真實磁碟**;`/data`(PVC,號稱持久)→ **tmpfs 記憶體** | `PersistentVolume` 這個名字沒有任何保證力,保證來自底下掛的東西 | unresolved | 3 | 2026-08-09 | 0
  - 成因:kind 的 node image 把 `/tmp` 設成 tmpfs,而 `pv-demo` 的 hostPath 是 `/tmp/pv-demo` → 這張「持久卷」的實體是記憶體,node 一重開就沒。
  - 封印句:**持久性由「它實際掛在什麼東西上」決定,不是由物件的名字決定。別信名字,去讀 `/proc/mounts`。**
  - 這是 s24「可寫層存在 memory 就消失了」誤解的**鏡像**(那次是該在磁碟的以為在記憶體;這次是號稱持久的真的在記憶體)。兩次共同教訓同一句。
  - 生產對應:`emptyDir: {medium: Memory}` 明著要 tmpfs,而且**算進 Pod 的 memory limit** —— 往 `/dev/shm` 猛寫會 OOMKilled,現象是「在寫檔」真相是「在吃記憶體配額」。s26 已親眼看過 tmpfs 在 `/proc/mounts` 的長相。
  - 08-09 抽:給一個 PV YAML,問「這個 PV 是不是持久的?你怎麼確定?」(要答:看 hostPath/CSI 底下掛什麼,不是看 kind)

- 2026-08-06 | EKS 儲存拓撲:EBS AZ-scoped / nodeAffinity / volumeBindingMode(**學員主動提問引出**,ProServe 高權重) | 未答錯;Transfer 過但屬當堂剛教的鷹架下複述 | 需冷測驗留存 | unresolved | 3 | 2026-08-09 | 0
  - 第一性原理定調句:**儲存有位置,計算沒有。** scheduler 預設只看計算條件(資源/taint/affinity);一旦儲存進場,**位置必須被寫進 API 物件,否則 scheduler 一無所知**。
  - 三方案對照:**hostPath** 位置沒寫 → scheduler 隨便排 → 資料「不見」(只能玩 lab);**local** volume 強制要求 `nodeAffinity`;**EBS CSI**(EKS 正解)由 driver 自動把 `topology.ebs.csi.aws.com/zone=<az>` 寫進 PV 的 `nodeAffinity` → Pod 只會排到那個 AZ。
  - **`volumeBindingMode` 是第二層坑**:`Immediate`(預設)= PVC 一建立就在某 AZ 開好 EBS,Pod 後到若有別的限制 → `volume node affinity conflict` **永遠 Pending**(症狀很賊,新手去查 taint,根因是 StorageClass 少一行);**`WaitForFirstConsumer`** = 先讓 scheduler 決定 Pod 去哪,再在那個 AZ 開 EBS。**順序倒過來就對了。**
  - 跨 AZ 共用只能 **EFS**:EBS 是塊裝置(fs 假設獨佔 → RWO、單 AZ),EFS 是 NFS 目錄樹(天生 RWX、跨 AZ)。回扣 s25 已收的「能不能 RWX 取決於底層是塊還是檔案系統」。
  - 實務取捨:StatefulSet + EBS 的 Pod 被釘在 AZ,該 AZ 掛了就起不來 —— 這是**刻意接受**的設計,高可用交給 app 層跨 AZ 複製(Kafka/Cassandra/etcd),不是交給儲存層。
  - L6 英文版:"EBS volumes are AZ-scoped, so the CSI driver stamps the zone into the PV's node affinity and the scheduler honours it. If you need shared access across AZs, that's an EFS conversation, not an EBS one."
  - 08-09 換情境冷測(禁用「三個 AZ + Immediate」原題)。

- 2026-08-20 | 判準給完當場套用不上(pattern 卡,教學法層級) | 同一堂兩次:① 剛證明「ALB 那層無罪」→ 下一題立刻選「查 ALB access log」② 剛講完「`systemctl` 只驗第 1 層」→ liveness 二選一立刻選 `pgrep`(第 1 層) | 判準被當成「聽過的一句話」而不是「拿來用的工具」;直給之後少了「當場用一次」那一步 | unresolved | 3 | 2026-08-23 | 0
  - 對治規格(s29 起執行):**每給一個判準句,立刻接一題只有換皮的應用題,答對才算給完。** 不要等隔堂冷測才發現沒套用 —— 隔堂測的是留存,當場測的是「有沒有真的接收到」。
  - 這條與既有的「只給結論不給判準」是**同一家族的兩端**:一端是講不出判準,一端是拿到判準不會用。兩端都通了才算會。

## Spaced-repetition queue

<!-- 檢視序:過期優先、interval 小者優先;step A 每堂 ~2 題上限。term 卡到期日在 term-registry.md。 -->

- mistake:YAML-validation | mistake | 3 | 2026-08-08(**s25 讀圖 rep 首次自己過**:`unknown field "spec.sccessModes"` 自行定位改對;但同段跳過自寫 PVC,rep 打折不推 7。08-08 換 `cannot unmarshal` / enum 大小寫型再測)| active
- mistake:ImagePullBackOff | mistake | 3 | 2026-08-09(**s26 真場景現形但 rep 不算數**:三選一答 C 正確,要了兩次沒貼 Events 關鍵字,且答案是我先告知才猜得到 → 不推 interval。08-09 換學員不知情的故障〔401 或 i/o timeout 型〕,要求先貼 Events 再分類)| active
- mistake:dry-run-兩層 | mistake | 3 | 2026-08-09(**s26 分界線親手做出來**〔dry-run 綠燈 → apply → ImagePullBackOff〕但判準是**同義反覆**,精準版未收。抽:誰知道 image 存不存在、在第幾棒。歷史:s16 未口頭抽,但**真場景實用一次**:自寫 default-deny 用 `--dry-run=server` 抓到自己的 apiVersion 錯並讀懂 `no matches for kind ... in version` → 工具已進肌肉,精準版仍未收)| active
- mistake:三分類-家族卡 | mistake | 3 | 2026-07-22(**s18 counter 1/3**:零流量思想實驗全對、conntrack 站對「狀態」;第 2 輪換家族成員)| active
- mistake:L4-vs-L7 | mistake | 3 | 2026-07-22(**s18 新情境過但框架教練給**:postgres/redis 兩題連過、標籤貼反未重現;07-22 無框架第四情境〔禁 postgres/redis〕過了才推 7)| active
- mistake:NetworkPolicy-出廠全通 | mistake | 3 | 2026-07-23(s20 重抽半過:結論靠提示、「podSelector 只在自家 ns 選人」why 沒站住;與 CNI 卡同天再抽)| active
- mistake:default-deny-分層(DNS vs 連線)| mistake | 3 | 2026-08-06(**s23 口頭再未過**但 lab 兩死法親手集齊;抽「兩步先後+兩種 timeout 關鍵字」)| active
- mistake:跨-node-走路由表 | mistake | 3 | 2026-08-13(**s27 動手驗完成,s26 的債還清**:親手 `docker exec k8s-coach-p2a-worker ip route` 讀到 `192.168.20.192/26 via 172.21.0.4 dev tunl0 proto bird onlink`,三欄意義已教。**但 A/B/C 預測未答即按 Enter,rep 打折不推 7**。08-13 抽:那一行三個欄位各是什麼意思 + 為什麼要包 tunl0〔底層網路不認 Pod 網段〕+ EKS VPC CNI 為什麼不需要 overlay)| active
- mistake:blackhole路由與本機/32 | mistake | 3 | 2026-08-13(s27 意外彩蛋,**教練直給未抽考**:`blackhole <本機 Pod 網段>` + 本機 /32 `dev cali` 全缺 = 沒有 Pod 在跑的獨立證據。抽:blackhole 存在的理由〔無對應 Pod 的封包當場丟掉,否則走 default gw 繞回成迴圈〕)| active
- mistake:跨-node-走路由表-舊記錄 | mistake | - | 2026-08-09(**s26 直給正解、學員未動手**:已給「路徑上 CoreDNS/Service/kube-proxy 各零次」+ 七段 kernel 路徑 + `ip route` + 判準句,三選一預測題未作答即改議程。⚠️ 依學員自身資料「直給+無動手」必蒸發 → **s27 開場先動手 `docker exec k8s-coach-p2a-worker ip route` 讀那一行**,跑完才算有 rep)| retired(s27 已執行,由上面的新列接手)
- mistake:分層判準-關掉APIServer還在不在 | mistake | 3 | 2026-08-08(**s25 冷測 4/5**:判準句無提示自產 ✅、cgroup limit 誤放右欄 ❌。已升級成**兩步版**〔先問宣告還是執行體〕,08-08 抽兩步版)| active
- mistake:誰把limit寫進cgroup(kubelet不是scheduler)| mistake | 3 | 2026-08-08(s25 新卡,答「scheduler 嗎」;判準句「不在 node 上的元件碰不到 kernel」+ 只在建 container 那刻寫)| active
- mistake:LVM三層+擴容四步 | mistake | 3 | 2026-08-08(s25 課後學員自己要求復習;兩題結論對但都只給結論,Q2 追一刀後機制自產並自接 EKS CSI。抽:三層各是什麼 + 擴容四步 + 為什麼第 4 步躲不掉)| active
- mistake:PV↔PVC是1:1獨佔 | mistake | 3 | 2026-08-08(s25 新卡,學員自曝以為 1:多;三層關係 + 塊裝置第一性 + RWO 限的是 node。Transfer 當堂過,冷測定升降)| active
- mistake:可寫層在硬碟不在memory(overlayfs)| mistake | 7 | 2026-08-13(**s26 二度實證 + 機制無鷹架自產**「只有 upperdir 換掉」,推 7)| active
- mistake:emptyDir-綁Pod不綁container | mistake | 7 | 2026-08-13(**s26 動手驗過翻正**:crictl stop 檔案在、delete pod 檔案沒,推 7。連同三階梯一起抽)| active
- mistake:restart排在採證前面(MTTR)| mistake | 7 | 2026-08-27(**s28 過**:四選項排序 `reboot` 排最後,B/C 順序給成本對比後自己改對並自帶判準「比較簡單」。s21 以來第一次真的做對,推 7。歷史:**s27 真現場大幅正向但只算半過**:五次故障以來第一次採證完成才 restart,完整證據鏈成立〔conditions → 宿主機 → 對照組 → systemctl → kubelet log〕。**但每一發指令都是教練指定的,學員零自選** —— 順序學會了,選指令那一步沒動。不推 7。08-13 抽:給一個新的 node NotReady,要學員自己說出頭三發指令)| active
- mistake:scheduler當萬用嫌犯 | mistake | 3 | 2026-08-13(**s27 第 2 次**〔s25「誰把 limit 寫進 cgroup」→ 答 scheduler;s27「node NotReady 你要看哪個東西」→ 答 scheduler〕。判準句合併:**scheduler 只填 `spec.nodeName`,它是狀態的消費者不是產生者,而且從沒進過 node 的門**。抽:換第三個情境〔e.g. Pod 卡 ContainerCreating〕看還會不會答 scheduler)| active
- mistake:產生者vs消費者(排障找誰) | mistake | 3 | 2026-08-13(s27 新卡,**教練直給未抽考**。`NotReady` 兩種產生者:`Ready=False`=kubelet 活著自己回報〔message 寫死因〕、`Ready=Unknown`=kubelet 失聯 40 秒 controller-manager 代筆,**看 `reason` 欄分辨**。抽:兩種怎麼分 + 為什麼不該問消費者)| active
- mistake:對照組判準(同層有好有壞) | mistake | 3 | 2026-08-23(**s28 首抽半過**:ALB 三台兩壞情境,認出證據句「第三台完全正常」✅,判準句答不出喊「直接説明」;直給後的應用題**立刻選查 ALB access log = 剛砍掉的那層**。留 3,換第三種皮再抽。歷史:s27 新卡,**教練直給未抽考**。同一宿主機三台 node、worker2 Ready 另兩台 NotReady → 整個宿主機層一次排除。通用句:**同一層裡有的好有的壞,那一層以下全部無罪**。抽:換一個非 k8s 情境〔e.g. 三個 ECS task 一個正常〕看會不會用)| active
- mistake:active≠還在幹活(健康檢查三層) | mistake | 3 | 2026-08-23(**s28 首抽未過**:首答跑去講 DB(講別人壞不是講它自己)、二答「不是網絡嗎」,機制直給;接的 liveness 二選一又選 `pgrep`。梯子縮到最小(pgrep 對 hang 住的 process 找不找得到)才走通。留 3。歷史:s27 新卡,**教練直給未抽考**。`systemctl is-active containerd kubelet` 兩個都 active,node 仍說 `container runtime is down`;kubelet log `StopPodSandbox ... DeadlineExceeded`,containerd 八小時零 log。三層:進程存在 / 有在聽 / **真的回得了話**。封印句:**塞住的服務跟死掉的服務,`systemctl` 分不出來**。抽:接到「liveness probe 只檢查 PID 會漏掉什麼」)| active
- mistake:DeadlineExceeded語義 | mistake | 7 | 2026-08-27(**s28 過**:二選一「不在家 vs 在家不接電話」答對「在家但是不接電話」,推 7。歷史:s27 新卡,**教練直給未抽考**。`DeadlineExceeded` = 對方還在但不理你;connection refused = 對方不在。**兩種病相反、查法相反**,回扣 CA session 已有的 refused-vs-timeout 卡〔跨 coach 同形狀,見 workspaces/ca〕。抽:兩個症狀各該先查哪一邊)| active
- mistake:PID1-signal保護 | mistake | 3 | 2026-08-09(s26 意外實證,`kill 1` 殺不死 container。**全程教練驅動未經抽考**。抽:Pod 刪除為什麼等 30 秒 + 同 namespace 內 `kill -9 1` 殺不殺得掉)| active
- mistake:Pod不會重啟只會被丟掉重建 | mistake | 3 | 2026-08-09(s26 F 段盲點,答「pod 會重啟 or 調節 編排」。抽:數出至少三種不需人動手 Pod 就消失的情境)| active
- mistake:持久性看掛在哪不看名字(tmpfs)| mistake | 3 | 2026-08-09(s26 `/proc/mounts` 意外:emptyDir 在 xfs、PVC 在 tmpfs。兩個分身判準第四次換皮)| active
- mistake:EKS儲存拓撲(EBS AZ/nodeAffinity/volumeBindingMode)| mistake | 3 | 2026-08-09(s26 學員主動提問引出;Transfer 過但屬當堂鷹架下複述。08-09 換情境冷測)| active
- mistake:veth-誤記跨node連線 | mistake | 7 | 2026-08-10(**s23 冷測過**:數字全對+tunl0 誘答咬住,推 7;但同日盲測站 2/6 仍蒸發,08-10 抽「旅程內出場」版)| active
- mistake:iptables-一棟樓 | mistake | 3 | 2026-08-06(**s23 半過**:換皮誘答咬住=吞餌史終結;但「nat 管路由」新錯法,重教後收。抽三表分工一句版+targetPort 5678 應用)| active
- mistake:kube-proxy-不在-Pod-啟動路徑 | mistake | 3 | 2026-08-07(**s24 首次重抽未過**,答「CoreDNS 嗎」= 寫進 resolv.conf ≠ 打過它)| active
- mistake:判準給完當場套用不上(pattern)| mistake | 3 | 2026-08-23(s28 新卡,同堂兩次。對治:給完判準當場接換皮應用題)| active
- mistake:只給結論不給判準(pattern)| mistake | 3 | 2026-08-23(**s28 混合**:正面=Q3 自帶判準「比較簡單」〔無提示正樣本第 5 次〕;負面=Q1 判準句喊「直接説明」。歷史:⚠️ **s27 倒退**:why-first 預測**連跳 3 次**〔`free -h`、`ip route` A/B/C〕,全部未答即按 Enter,s26 的正向沒延續。註:s27 教練也沒執行 s24 訂的硬規格〔不給預測就不給下一發指令〕,是雙方各一半。08-13 續盯)| active
- mistake:NetworkPolicy-靜默無效 | mistake | 3 | 2026-07-31(過期,s23 未抽;**s22 F 段質變**:追問下自組完整鏈含「安全假象」自己的話;一段話冷測版過才 resolved,s24/WR9 抽)| active
- mistake:CNI-合約三件事 | mistake | 3 | 2026-07-23(s19 新卡:網卡/IP/路由 + 各自缺席的死法;hostNetwork 判準已自推不用重考)| active
- mistake:兩張獨立名單 | mistake | 3 | 2026-08-06(**s23 重抽未過**,三層提示未自產、直教兩道門模型;s24 動手版〔Step 5 自寫兩條 policy + 矩陣〕+ 08-06 口頭版)| active
- term:conntrack | term | 7 | 2026-07-26(**s18 分工句收**:骨架〔規則管第一次、conntrack 管之後〕自產,應用一次追問補全〔去程改 Destination/回程改 Source、都查 conntrack〕;07-26 抽完整版〔兩個詞+分工句+查誰〕過即封印。歷史:s16 兩個詞給框架後自產;s15 直給後 3 天蒸發=「給框架 vs 給答案」對照組證據)| active
- mistake:probe-職責 | mistake | 3 | 2026-08-23(⚠️ **s28 退步,interval 從 7 重置**:「liveness 拿到 exit 0 之後 kubelet 做什麼」→ 答「**繼續導入流量**」= readiness 的動作。P1 已封印的東西在疲勞下對調。抽:兩種 probe 失敗/通過後各自的動作,一句一個)| active
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
