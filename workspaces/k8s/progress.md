# progress

<!-- Engine-owned schema: engine/PROGRESS-SCHEMA.md. Converted 2026-07-10 from the
     standalone k8s-coach 4-file workspace (originals verbatim in archive/pre-migration/).
     Session narratives live in session-log.md; machine/context facts in environment.md;
     strategic plan in curriculum-plan.md. -->

## Meta

- session_count: 34
- last_weekly_review: 34(**WR9 於 s34 壓縮版跑完,連續八度延期終結**。三主題 blind recall 全過:先鎖 fault-domain(換皮首過)、StatefulSet 每 replica 一份資料(換皮首過)、跨 node 走路由表(五抽首過)。下次 WR 於 s41。)
- last_session_date: 2026-09-03
- warm_up_classification: mid(有地圖形狀,缺演員名字;P0 剛好,不加速)
- **target_role: 泛用大廠 senior DevOps/SRE；2026-08-21 確認目前無緊急面試，採 production depth + senior interview 雙軌**。每個核心主題固定比較地端 Kubernetes、傳統 EKS 與高度託管 EKS，並同時要求 hands-on evidence 與 scenario answer；見 curriculum-plan §11。

## Current Session breakpoint

**s34 收工(2026-09-04 凌晨,家用 VM `jasonarmvm2`,context `kind-k8s-coach-p2a`,兩台 node Ready v1.30.0 45d)**:①**WR9 壓縮版跑完,連續八度延期終結**,三主題 blind recall 全過(先鎖 fault-domain 換皮首過、StatefulSet 每 replica 一份資料換皮首過、跨 node 走路由表五抽首過)。②**C-4 chunk 3 動手完成**:`rbac-lab` ns + `ci-reader` SA 在這台重建(s33 那份在 bastion),Role `pod-reader` + RoleBinding `ci-reader-can-read-pods` 學員對照打完成並 apply 成功,`auth can-i --as` 三發預測全中。

**next(s35),順序:**

1. **C-4 chunk 3 收尾**:`auth can-i --list` 的三種診斷結果只教完表格,**未驗收**。用一個真的壞掉的情境(建議:verbs 只給 `get` 不給 `list`,讓學員自己用 `--list` 判出是哪一種),過了 chunk 3 才算 done。
2. **C-4 chunk 4**:最小權限設計方法論(爆炸半徑思維),keystone 收尾。
3. **C-4 的 F/G 未跑**(連續第幾堂待查),chunk 4 完再一起補。
4. 冷測到期:09-06 RWO 數的是 node 不是 Pod;09-09 fault-domain 換皮(9 顆 replica / 5xx 11% 型);09-10 跨 node 路由第二次冷測、StatefulSet 顧問版、fault-domain。
5. C-2 `reclaimPolicy: Delete` teardown 實證仍欠(s32 現場已被叢集重建洗掉,要重建物件)。
6. 單節點 kind 評估仍掛著;story-bank 連十三堂未挖。

本堂教練失誤(要改):**教完 `auth can-i` 單題問法就直接要求組 403 排障鏈**,學員當場反映「沒有教啊」且反映正確。組鏈之前要先把工具教齊。

本堂新增筆記(已併入 Mistake Registry / mistake-notes):

- **新卡 RWO 的 Once 數的是 node 不是 Pod**:共用 PVC 誘答題答「RWO 應該是 POD」,s25 教過的點回退。RWOP 才是限單一 Pod(1.29 GA)。
- **判準跑錯軸**:跨 ns RoleBinding 預測題答 A(對),但理由給「namespace 只是邏輯隔離不是網路隔離,要用 NetworkPolicy」= s33 chunk 1 剛教過的「兩個獨立軸」一堂就混用。用學員自己的 s24 分層判準拆掉(NetworkPolicy 執行體在 iptables、RBAC 執行體在 API Server),兩問皆自答。
- **`logs deploy/x` 是抽樣不是普查**:`--all-pods` 預設 false,撈的是 kubectl 隨機挑的一顆且無 `--prefix`。33% 故障率下有 2/3 機率撈到健康那顆。
- 學員自己抓到 DNS-1123 違規(物件名不准底線);`roleRef.name: Required value` 由 server dry-run 抓出,學員自行補回。
- 圖解頁產出:**RBAC 的三條線** https://claude.ai/code/artifact/5a0f989c-a7f4-4668-bb7a-f5fa07b5d076(roleRef 不能跨 ns / subjects 可以跨 / 生效範圍看 RoleBinding 住哪)。

<!-- schema: PROGRESS-SCHEMA.md §3 = 當前狀態 + 下一堂 resume,只留最新一堂。
     s32 及更早的斷點原文已收錄於 session-log.md「Session 紀錄」對應堂;
     長效教練紀律在 session-log.md「教練執行紀律」。 -->

## Phase status

- P0 心智模型: gate-passed(2026-06-22;legacy,pre-Examiner,coach 認證)
- P1 核心物件 + 容器底層: gate-passed(2026-06-25;legacy,pre-Examiner,coach 認證)
- P2a 網路深水區: in-progress(chunk 1 Service/kube-proxy/CoreDNS ✅、chunk 2 Ingress ✅;chunk 3 NetworkPolicy in-progress〔3-1/3-2 教完;lab Step 4 於 s23 bastion 側重建完成(allow-dns + 兩死法實證),Step 5 兩道門模型已教、兩條 policy 未寫,剩 Step 5+6+gate+F/G〕;chunk 4 in-progress〔**4-1 CNI 合約 ✅ s19、4-2 veth ✅ s20、4-3 路由 ✅ s20、4-4 MASQUERADE ✅ s20**;**4-5 七站骨架盲講 ❌ s21 冷測 0/4 未過**〕。四塊零件備妥但串不起來;**4-5 背誦式重測已於 2026-08-11 退役,P2a gate 答案卷改情境排障題形式(curriculum-plan §10.2)**)
- P2b 儲存 + 權限: **in-progress**。**C-1 Volume/PV/PVC ✅ 完成(s26)**:三階梯壽命表一顆 `vol-demo` Pod 全部親手實證(L1 可寫層 / L2 emptyDir / L3 PVC,換 container 與 delete pod 兩種情境四格全驗),預測全中、機制自產(「pod 沒有換 container 換掉只有 upperdir 換掉」);執行體肉身摸到(`/proc/mounts` + node 上 `ls /tmp/pv-demo/`)。附帶收:PID 1 signal 保護、hostPath PV 落在 tmpfs 的意外、EBS AZ-scoped + `nodeAffinity` + `volumeBindingMode`。**C-1 唯一殘留**:`cg-demo` 的 `/sys/fs/cgroup/memory.max` 實際數字未讀到(s25 Pending,node 已修好,s27 補)。**C-2 StorageClass / dynamic provisioning / CSI 概念三 chunk ✅(s29)，hands-on 主鏈 ✅；只剩 `reclaimPolicy: Delete` teardown 實證。** **C-3 StatefulSet 內容段結案（s31 三 chunk + hands-on + E + F，s32 補完 G）**：identity/storage/DNS 三面牆與 `volumeClaimTemplates`、headless Service、EndpointSlice 全部教完並有 lab 證據；step G Tier 2 **2/4 未通過**（MTTR 失分），內容不重教、MTTR 留 registry 續盯。**C-4 RBAC 開講（s33）**：chunk 1(四象限)、chunk 2(純 allow / SA 是 Pod 身分)Recall+Transfer 皆過(含 ELI5 鷹架，過程撞出兩個新混淆已教正)；chunk 3(403 排障 + impersonation)動手才開始(ns/SA 建好，YAML 未寫)；chunk 4(最小權限設計方法論)未開始。
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

- **P2b C-3 StatefulSet identity(ordinal / per-replica PVC / per-Pod DNS)**: med-high (s31 lab 全實證 + **s32 三天冷測無提示過**:`delete redis-0` 的「保證一樣=storage+名稱 / 會變=UID+IP」兩欄全對;PDB 誘答「pod 層級 scale ≠ 服務層級 HA」自帶分層判準咬住;ClusterIP fan-out 機制「set 到 server 1、get 指向 server 2」無鷹架自產。**未升 high 的理由**:「5 個 replica = 幾份資料」答 3,誤以為原本 3 顆共用一份 —— per-replica 空 PVC 這個第一性沒站住。09-04 換皮抽「N 個 replica 幾份資料 + 誰負責 sync」)

- **kubectl debug / ephemeral container(P1 應用,ad hoc 非正式堂)**: low (2026-09-01,實際工作觸發:ecr-uat pod 測 DB 連線,非 s33 主線、未排入 curriculum、未經 gate。Recall 過〔exec 受限於 image 裝了什麼工具,minimal image 沒 curl/nc〕;Transfer 過但需鷹架〔先答「像 sidecar」方向對但機制沒點出,誤答 cgroup 後才收斂到 network namespace〕。機制句:同 pod 內所有 container(不論原生宣告或後補的 ephemeral container)共用同一個 network namespace,這就是 debug container 能看到跟 app 一樣的 IP/route 的原因;ephemeral container API 2022(1.25)才 GA,GA 前只能靠 sidecar 在 pod 建立時就寫進去。**acquire tier,尚未冷測**,下次自然遇到再測是否保留。)

- **P2b C-4 RBAC 四象限(Role/ClusterRole × RoleBinding/ClusterRoleBinding,三種合法組合)**: low(scaffolded)(s33 新教。Recall 需 ELI5 鷹架(大樓公佈欄比喻)才收斂,自產終版判準「Role 只印一份沒辦法擴大生效範圍,ClusterRole 印每份可以縮小生效範圍」;Transfer(反向,ClusterRole+RoleBinding 為什麼合法)無鷹架自答「每個大樓都一張,所以可以限定一棟大樓」✅。核心混淆已教正:namespace 對「物件存在範圍」是硬邊界(etcd key 結構),跟「namespace 不做網路隔離」是兩個獨立軸。**未冷測**,09-04 起換情境驗。)
- **P2b C-4 RBAC 兩地基性質(純 allow 無 deny / SA 是 Pod 身分)**: low(scaffolded)(s33 新教。性質一 Recall 帶因果過(「反正預設是 deny」);性質二誘答(403 會不會讓 Pod CrashLoopBackOff)最終答對且抓住「兩條路不相通」機制,用 ELI5 artifact 鞏固。**換皮應用題撞出新混淆**:把「controller 建 Pod 用自己系統身分」跟「Pod 裡程式呼叫 API 用宣告的 SA」搞混,已教正(見 Mistake Registry)。**未冷測**,09-04 起換情境驗。)

## Scorecard history

<!-- 轉換規則:原 ✅=1、🟡/❌=0,原符號保留在註記。legacy = pre-Examiner 時期由教學 coach 認證。 -->

- 2026-08-28 | step G (s32, tier 2, StatefulSet≠HA 顧問情境) | **2/4 未通過** | **判準給完當場套用不上，同形狀第三次**：剛收到「先鎖 fault domain 再查內部」，換皮 Postgres 題立刻又選「檢查 replica 的 log」。對策：排障題先強迫答「我這一發是第 1 步還是第 2 步」再給指令 | **MTTR 第一題自帶完整判準句型**「寫入成功 + 全 Running + RESTARTS 0，所以我看資料層」= 無提示正樣本第 6 次，且砍掉 process 層的推理方向正確 | coach(原理🟡〔delete pod 不變/會變冷測全對，但「5 顆 = 幾份資料」答 3〕 機制✅〔ClusterIP fan-out「set 到 server 1、get 指向 server 2」無鷹架自產〕 自己的話✅〔PDB 誘答「pod 層級的 scale 不是 redis 服務層級的 HA」咬住〕 MTTR❌〔兩次第一發選內部不選 fault domain〕)
- 2026-08-24 | step G (s30, tier 2) | 3/4 | 第一刀選 `kubectl describe pod`，沒有直接驗證 30 秒 request timeout；下次先用 direct-to-target 對照 bypass 嫌疑層 | 能用自己的話修正成「繞過後正常只鎖定被繞過的整段路徑，不能直接定罪 Proxy」 | coach(原理✅ 機制✅ 自己的話✅ MTTR❌)
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
     PROGRESS-SCHEMA §7 = 單行八欄。正解/判準句/L6 版/歷史重測/下次抽考題寫在 mistake-notes.md,
     依 `date | topic` 對應。開場不讀 mistake-notes.md;step A 抽考到哪張卡才拉哪一節。
     interval 2 = +2 天臨時複習格(口頭型 resolved,過了才進 3/7/14)。
     unresolved-session-count 於 2026-07-10 遷移時依複測紀錄初始化(近似值)。 -->

- 2026-06-18 | YAML validation | `matchLabels` 打成 `metaLabels`,不會讀 strict decoding error | 不知道 unknown-field 路徑=藏寶圖、驗證發生在 API Server | unresolved | 7 | 2026-06-30 | 2
- 2026-06-22 | probe 職責 | 把 readiness 的「準備好接流量」塞給 liveness,延伸成 liveness 查 DB | 沒抓住兩種 probe 失敗後動作不同(重啟 vs 切流量) | unresolved | 7 | 2026-07-10 | 1
- 2026-06-23 | ImagePullBackOff | image 打成 `ngimx:1.25`,apply 成功卻卡 ImagePullBackOff,不解 | 驗證有邊界:API Server 只驗語法,repo 存不存在要 kubelet 第 5 棒拉了才知 | unresolved | 7 | 2026-07-03 | 1
- 2026-06-27 | ClusterIP/kube-proxy/DNAT 全鏈(謎題B) | 「封包先去 ClusterIP 拿 IP」誤解 + 手(iptables)vs 名單(Endpoints)混 | ClusterIP 不是地方、封包從不拜訪它,改寫發生在出發地本機 kernel | resolved | 14 | 2026-07-13 | 0
- 2026-06-28 | 叢集 DNS 排障 | busybox nslookup NXDOMAIN 差點誤判 CoreDNS 壞 | 排障第一刀「先用 FQDN 二分伺服器壞 vs 發問端壞」沒長成肌肉 | unresolved | 3 | 2026-07-10 | 3
- 2026-07-03 | dry-run 兩層 + Service port | `--dry-run=client` 綠燈騙人;port vs targetPort 靜默不通 | client 只做本機淺檢查;strict decoding 在 API Server(server 端) | unresolved | 3 | 2026-07-17 | 3
- 2026-07-14 | 規則/狀態/資料 三分類(W2 家族 pattern 卡,M2 追蹤用) | conntrack 初分類答「規則」;etcd 分類未自答 | 「事先寫好放著 vs 流量跑過才長出 vs 被查的名單」判準沒長成反射 | unresolved | 3 | 2026-07-22 | 1
- 2026-07-06 | L4 vs L7 | 記成場景標籤(叢集內=L4、外部=L7),信封題連卡兩次 | 本質=轉發決定需要讀到哪層資訊(信封 IP+port vs 拆信讀 Host/path) | unresolved | 3 | 2026-07-22 | 3
- 2026-07-17 | NetworkPolicy 出廠全通 | why-first 預測「陌生 tmp Pod 連不到 db」→ 實測**連得到**(回 `db`) | k8s 出廠預設全通、namespace 只是邏輯分組不做隔離(P1 已釘過、當堂教練又粗體講過 40 分鐘,仍預測錯) | unresolved | 3 | 2026-07-23 | 1
- 2026-07-23 | 跨 node 走路由表不是 iptables(層級混淆家族) | 「封包怎麼從 node1 到 node2?第一個指令是什麼」→ 答「查 iptables」;縮小重問「node1 怎麼知道這個 IP 在哪台機器」→ 答「查 resolv.conf」 | 改寫層(NAT)與轉送層(routing)混為一談;第二次還跨到解析層 | unresolved | 7 | 2026-09-10 | 0
- 2026-07-23 | kube-proxy 不在 Pod 啟動路徑上 | ① 把 kube-proxy 列為 kubelet 建 Pod 的三件事之一 ② 「Pod 啟動過程有封包打 ClusterIP 嗎」答 yes | 控制路徑 vs 資料路徑混淆;規則 vs 引擎家族 | unresolved | 3 | 2026-08-07 | 1
- 2026-07-23 | 只給結論不給判準(pattern 卡,升級追蹤) | 同一堂三次:kube-proxy 題只答 yes、選路由那行不給計算、CIDR 直接說「不用特別算」 | 輸出習慣問題不是能力問題:算得出來但不 show work,面試官無法區分「會」與「猜對」 | unresolved | 3 | 2026-07-26 | 5
- 2026-07-17 | default-deny 後的分層(DNS 層 vs 連線層) | 只答「連線不到」,未分辨死在哪一層;**s21 重抽未過**:情境題答「這問題應該是 app 層」,縮小到圖上指認又答「被鎖的是連線那步」(漏掉①先發生) | 層級混淆家族(同 s11 把 conntrack 拉進 DNS 題、06-28 排障第一刀);s21 新形狀=**兩步都被鎖時不問哪一步先發生** | unresolved | 3 | 2026-07-26 | 1
- 2026-07-28 | veth 誤記「跨 node 連線」 | 自我盤點答「veth 是跨 node 的網卡連線」;同/跨 node 各經過幾條 veth 數不出 | 零件定義衰減:veth 只管 Pod netns→node root netns 那一段,跟跨不跨 node 無關 | unresolved | 7 | 2026-08-10 | 1
- 2026-07-28 | iptables=一棟樓(nat 表/filter 表) | 盲測幻影站 4「DNAT 到 node iptables 出去」+ F 段誘答吞餌「DNAT 做完才進 iptables,對」— 同一病灶當日兩現 | 把 iptables 當成旅程中的「一站」,不知 DNAT 就發生在 iptables nat 表裡、守衛在 filter 表裡 | unresolved | 3 | 2026-07-31 | 0
- 2026-07-20 | CNI 基本合約 vs 選配 | Recall 合約三件事兩輪講不出,答成「建立網路 networkpolicy 嗎」= 把選配(NetworkPolicy 引擎)混進合約本體 | 新教內容首輪未固化 + chunk 3 靜默無效的 CNI 印象蓋過合約本體 | unresolved | 3 | 2026-07-23 | 0
- 2026-07-19 | 兩張獨立名單(3-2 坑二) | 「只開 backend ingress,frontend curl backend 通嗎」答「可以吧」 | 規則剛教完但沒跑兩關檢查程序,憑感覺猜;學員隨後喊「直接說明」未自跑重測 | unresolved | 3 | 2026-07-22 | 0
- 2026-07-19 | NetworkPolicy 靜默無效(四引擎第四行) | Transfer 只給零件不組裝:「API Server 只驗 schema → 存 etcd → 無引擎編譯成 kernel 規則 = 靜默無效 = 安全假象」整條鏈講不出,③ 危險比較只答半邊 | 先跳結論等追問才補深度(第四堂同條)+ W1 隱性會;零件全對(apiserver/CNI/馬上發現)但拒組裝 | unresolved | 3 | 2026-07-22 | 0
- 2026-07-07 | Ingress YAML schema | `backend.service` 寫成字串 + `pathType: prefix` 小寫;client dry-run 又給假安心 | service 是 object 型別;enum 大小寫敏感;decode 錯擋在第一個 | unresolved | 3 | 2026-07-10 | 1
- 2026-07-07 | Ingress 404 排障 | 差點改沒壞的規則;真兇=被 Ctrl-C 打斷的半死 port-forward 回假 404 | 規則層全綠時兇手在「你測試所經過的那層」 | parked(2026-07-16 ROI 篩:Q1 半 yes,但「port-forward 半死」是 lab 夾具產物、prod 不長這樣;同一判準已三種問法重問三次=題目壞掉。判準留檔備查,不再抽) | - | - | 3
- 2026-07-09 | no-Host→404 的 why | 結果預測對,但講不出「curl 自動拿 URL 主機名當 Host」那個字 | 會用/會預測 ≠ 會講 why(W1 隱性會) | resolved(2026-07-16 ROI 篩:Q1=no,curl 填 header 是 tool trivia,面試不考;學員答「沒帶 domain → Ingress 對應不上」= 機制正確,教練題目壞掉不是學員沒懂。結案) | - | - | 1
- 2026-08-04 | 分層判準:關掉 API Server 還在不在(工具卡,層級混淆家族的解藥) | s25 冷測 4/5:cgroup memory limit 誤放右欄,自述「我在想的是 yaml 的 limit」 | 同一個名詞的兩個分身(宣告 vs 執行體)沒有分開 | unresolved | 3 | 2026-08-08 | 1
- 2026-08-05 | 誰把 limit 寫進 cgroup、什麼時候寫 | 「客戶改了 limit 但 Pod 還在 OOMKilled,誰負責把新數字寫進 cgroup?」→ 答 **「scheduler 嗎」** | 控制面元件與 node 上元件的職責混淆(層級混淆家族);不知道 cgroup 只在建 container 那一刻寫 | unresolved | 3 | 2026-08-08 | 0
- 2026-09-04 | 判準跑錯軸:RBAC 題答成 NetworkPolicy | 跨 ns RoleBinding 預測題結論 A 正確,但理由給「namespace 只是邏輯隔離不是網路隔離,要用 NetworkPolicy」 | s33 chunk 1 剛教過「物件存在範圍」與「網路隔離」是兩個獨立軸,一堂就混用;結論對判準錯(s16 同形狀) | unresolved | 3 | 2026-09-07 | 0
- 2026-09-03 | RWO 的 Once 數的是 node 不是 Pod | 共用 PVC 誘答題答「RWO 應該是 POD 所以只能一個」;s25 已教過「RWO 限制的是 node 不是 Pod 數」,回退 | 層級/擁有者混淆(RP1):把 volume 的掛載限制記在 Pod 這層,實際限制在 node 這層 | unresolved | 3 | 2026-09-06 | 0
- 2026-08-05 | LVM 三層 + 擴容四步(學員課後自己要求復習,foundational pull) | Q1/Q2 結論皆對但**兩題都只給結論**(Q1「需要 resize」、Q2「還是成立」),追一刀後 Q2 機制自產 | 判準句慣性省略(pattern 卡);LVM 的 PV 與 k8s 的 PV 同名不同物 | unresolved | 3 | 2026-08-08 | 0
- 2026-08-05 | PV ↔ PVC 是 1:1 獨佔 | 學員自曝「我以為是 PV 1:多」 | 「一份儲存給多人用」的直覺貼錯層(該直覺屬於 PVC→Pod,不屬於 PV↔PVC) | unresolved | 3 | 2026-08-08 | 0
- 2026-08-04 | container 可寫層在硬碟不在 memory(overlayfs 三層) | 「process 死掉檔案去哪」答「存在 memory 就消失了」= 結論對機制錯 | 把 ephemeral 誤等於 in-memory;沒有「可寫層是硬碟上一個目錄」的實體概念 | unresolved | 3 | 2026-08-07 | 0
- 2026-08-04 | emptyDir 綁 Pod 不綁 container | 「emptyDir 撐不撐得過 kill 1」答「不在了」;同時不知道 `kill 1` 是什麼 | 三層階梯的中間一階沒有實體錨點,只有教練口頭列表 | unresolved | 3 | 2026-08-07 | 0
- 2026-08-06 | 排障:restart 排在採證前面(MTTR / 治標 vs 治本第三次同形狀) | 三台 node NotReady,三選一(A 看 node Conditions / B 看宿主機 / C 直接 restart)→ **選 C,理由「看起來是 notready 先重啟試試」** | 「先試試」不是診斷;不知道 restart 會同時清掉症狀與證據 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | PID 1 的 signal 保護(kernel 層,新知識卡) | 學員未答錯,是實驗意外撞出來:`kubectl exec vol-demo -- kill 1` → `RESTARTS 0`、檔案全在,container 根本沒死 | 全程教練驅動,學員只跑指令,**未經任何抽考** | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | Pod 不會「重啟」,只會被丟掉重建 | F 段菜鳥追問「pod 不是我建的嗎?我不刪它,它為什麼會自己不見?」→ 答 **「pod 會重啟 or 調節 編排」** = 方向對,講不出誰在什麼條件下動手 | 把 Pod 當成一個會重啟的長壽物件(寵物),而不是可拋棄的一次性單位 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | 持久性看「掛在哪」不看名字(兩個分身判準第四次換皮) | 學員未答錯,是 `/proc/mounts` 意外撞出來:`/scratch`(emptyDir,號稱短命)→ `/dev/nvme0n1p1` **xfs 真實磁碟**;`/data`(PVC,號稱持久)→ **tmpfs 記憶體** | `PersistentVolume` 這個名字沒有任何保證力,保證來自底下掛的東西 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-06 | EKS 儲存拓撲:EBS AZ-scoped / nodeAffinity / volumeBindingMode(**學員主動提問引出**,ProServe 高權重) | 未答錯;Transfer 過但屬當堂剛教的鷹架下複述 | 需冷測驗留存 | unresolved | 3 | 2026-08-09 | 0
- 2026-08-20 | 判準給完當場套用不上(pattern 卡,教學法層級) | 同一堂兩次:① 剛證明「ALB 那層無罪」→ 下一題立刻選「查 ALB access log」② 剛講完「`systemctl` 只驗第 1 層」→ liveness 二選一立刻選 `pgrep`(第 1 層) | 判準被當成「聽過的一句話」而不是「拿來用的工具」;直給之後少了「當場用一次」那一步 | unresolved | 3 | 2026-08-23 | 0
- 2026-08-28 | StatefulSet 每個 replica 一份獨立資料(不是共用一份) | 「StatefulSet redis replicas 從 3 開到 5,有幾份資料?」→ 答 **「still is 3 data, new replicas will not sync」** = 以為原本 3 顆共用一份、新的沒跟上 | 把「每人一份儲存」誤讀成「大家共用一份資料」;不知道 `volumeClaimTemplates` 給的是**空** PVC | unresolved | 3 | 2026-09-04 | 0
- 2026-08-28 | 排障兩步:先鎖 fault domain 再查內部(MTTR 核心卡) | 同一堂兩次先跳內部:① Redis 題三選一選 C(`redis-cli info replication`,單顆內部)不選 B(`endpointslice`,流量打到幾個東西)② 換皮 Postgres 題答「檢查 replicas 的 log」 | 拿單一成員的內部狀態去解釋一個**分散**問題;沒有先問「這條路徑上有幾個東西」 | unresolved | 3 | 2026-08-31 | 0
- 2026-09-01 | 建 Pod 的權限 vs Pod 裡程式呼叫 API 的權限(誰用誰的身分) | C-4 換皮應用題(CronJob 的 SA 沒有 `list configmaps` 權限,問 Pod 會不會變 CrashLoopBackOff)→ 答「不會,因為根本沒有到建立 pod」 | 把「controller 建 Pod」跟「Pod 裡程式自己呼叫 API」當成同一件事、用同一個身分;層級混淆家族(RP1)新成員 | unresolved | 3 | 2026-09-04 | 0

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

## Curiosity branch

- etcd Raft 深入 | 2026-06 | 面試不直接考實作、P5 etcd 運維會用到 | 想追 Raft 共識怎麼撐起 etcd,park 到 P5(見 curriculum P5 焦點)

## Domain registries

- `term-registry.md`(同目錄):英文術語卡,18 張。欄位:EN term / 發音 / 英文定義 / 中文點破 / 學習日 / 下次抽考日。抽考雙向(見 language hook),3→7→14 節奏同引擎。
- `story-bank.md`(同目錄):behavioral 素材庫(非間隔複習型)。機會式一行入帳 + 每次 Weekly Review 保底挖 10 分鐘一則(M4);P6 提煉 STAR。
- `mistake-notes.md`(同目錄):**Mistake Registry 每張卡的內文**(正解 / 判準句 / L6 顧問版 / 歷史重測 / 下次抽考題),節標題 = registry 行的 `date | topic`。**開場不讀**;step A 抽考到哪張卡才拉哪一節。新的重測紀錄追加到那裡,不要寫回 registry 行底下。
- 其他 coach 讀取檔:`session-log.md`(歷史 session 敘事)、`environment.md`(機器/context 安全事實)、`curriculum-plan.md`(戰略層,advisory)。

## Examiner ledger

(空 — P0/P1 為 pre-Examiner 時期由教學 coach 認證,見 Scorecard history 的 legacy 列。第一筆 Examiner 紀錄將是 P2a gate,預計 3-5 堂後。)
