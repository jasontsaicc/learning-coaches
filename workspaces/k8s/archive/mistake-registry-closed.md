# Mistake Registry closed rows (K8s)

<!-- PROGRESS-SCHEMA §7: resolved / parked rows move here unchanged at step H. parked = failed
     the ENGINE.md Open cap ROI check; kept for reference, never reviewed. Card bodies stay in
     ../mistake-notes.md under the same `date | topic` heading. -->

## 2026-10-29 s52 triage (65 unresolved -> 15, student approved)

### Registry rows

- 2026-10-16 | Pending 時 FailedScheduling 是誰寫的 | 預測「scheduler 活著但全 node 不合」會 Events <none> ✗,實驗 From default-scheduler 推翻 | Event 由 scheduler 寫;有 = scheduler 活著被規則擋,<none> = 查 scheduler 本身 | parked | 3 | 2026-10-19 | 0
- 2026-10-16 | unschedulable Pod 何時被重排 | F 答「有個機制會去檢查」;s50 冷測結論對、因為答「會重試」 | 精準版:冷宮等叢集事件(node 加入、Pod 被刪)喚醒,不是輪詢 | parked | 3 | 2026-10-23 | 1
- 2026-10-16 | RBAC `-w` 需要 watch 的判準 | 結論對,因為答「風險不同」 | verb 由 API 請求形狀決定,不看指令名字 | parked | 3 | 2026-10-19 | 0
- 2026-10-12 | 誰是 bootstrap 元件不能依賴自己(calico-node hostNetwork / apiserver 靠 kubelet) | calico-node 為何用 node IP:「不知道該怎麼說」→ 縮小後答出 Pod IP 由 Calico 給,仍接不到「Calico 不能等自己」,直給 | 「負責建立 X 的元件不能依賴 X」規則未內化;apiserver 那題(B kubelet)二選一答對 | parked | 3 | 2026-10-15 | 0
- 2026-10-12 | static pod manifest 被移走 → Pod Pending 的因果 | 預測 Pending ✅,因為答「找不到設定 yaml」 | 沒接到 kubelet 停 scheduler static pod → 沒人填 nodeName;Pending + Events 空 = 懷疑 scheduler 本身 | parked | 3 | 2026-10-19 | 1
- 2026-10-12 | kubeadm 職責邊界 | 總結成「安裝每個節點需要的網路、憑證、依賴」 | 依賴是 Ansible 裝的、Pod 網路是 CNI;kubeadm 只產 certs/kubeconfig/static pod manifest 後退出 | parked | 3 | 2026-10-15 | 0
- 2026-10-06 | SG inbound 開在誰身上(listen 方 vs 發起方) | 6443 忘了 port 號;答「6443 三台都開,因為要互相溝通」;10250 二選一選「只開 cp-1,來源 worker」 | 用「誰發起連線」決定 inbound,沒看「冒號後面的 port 在誰身上 listen」;apiserver 只在 cp-1,kubelet 在每台。s42 同日:bastion→cp:22 SSH 事後解釋,首答只給 port,一階提示後答「listen 的 cp SG 過濾進來流量」✅ 帶判準;換皮 cp→bastion 給對 port+source(SG 優於 IP),未明講改哪個 SG(supported,未冷測) | parked | 3 | 2026-10-09 | 0
- 2026-09-30 | terraform 哪一步發現錯誤(validate / plan / apply) | 假 AMI 字串答「plan 發現」(兩次);換皮 data "aws_ami" 查不到又答「apply」 | plan 只 refresh 既有資源 + 讀 data 區塊;新 resource 參數要 apply 才送 AWS。學員二分法只有「plan 打不打 API」,沒分 data 查詢 vs resource 建立。10-06:預測 data 查 subnet「apply 才打」✗ → 假 subnet id 實驗 plan 報錯自己推翻;換皮 t3.meduim 打錯字答 apply + 因為 resource ✅(supported,未冷測) | parked | 3 | 2026-10-09 | 1
- 2026-09-29 | PSS 只檢查 Pod 不檢查 Deployment(產生者找錯人) | G 題 Deployment apply configured 但新 Pod 不出現,根因沒講出「PSS 擋的是 RS controller 建 Pod 的請求」;先查 rs 的因為只給「看不出來」 | 產生者 vs 消費者 + 成功訊息不保證生效 兩張舊卡同題重現 | parked | 3 | 2026-10-12 | 1
- 2026-09-26 | app 為什麼要 root | 猜 nginx 要 root 是因為「會改 kernel 的路由表」 | 把一般 app 要 root 的普通原因(綁 <1024 port、寫 root 擁有的目錄)跟 node 系統元件(CNI/kube-proxy 要 NET_ADMIN)混為一談 | parked | 3 | 2026-09-30 | 0
- 2026-09-25 | container 存取兩道門(namespace 視野 vs UID 身分) | 「UID 0 沒翻牆讀得到 node 的 /etc/shadow 嗎」答「可以,因為是 root」 | RP2 兩道獨立檢查混成一步(同 IRSA trust vs permission 形狀):只看 UID 欄,漏 mnt ns 決定看不看得到 | parked | 3 | 2026-09-28 | 0
- 2026-09-13 | 權限爆炸半徑跑錯判準軸 | 評 SA 外洩痛不痛時先看 ns 廣度(漏 resource 深度);評 secret 危險度跑到 base64 存法軸,不是「能否離開 RBAC 管轄」軸 | RP3 判準軸選錯:該問「憑證外洩後攻擊者碰得到的 ns×resource×verb 上限,以及能否跳出 RBAC 管轄」 | parked | 3 | 2026-10-12 | 3
- 2026-06-18 | YAML validation | `matchLabels` 打成 `metaLabels` | 不讀 strict decoding error;驗證在 API Server | parked | 7 | 2026-06-30 | 2
- 2026-06-23 | ImagePullBackOff | image 打成 `ngimx:1.25`,apply 過卻卡住 | 驗證有邊界:repo 存不存在要 kubelet 拉了才知 | parked | 7 | 2026-07-03 | 1
- 2026-07-03 | dry-run 兩層 + Service port | `--dry-run=client` 綠燈騙人;port/targetPort 靜默不通 | strict decoding 在 API Server 不在 client | parked | 3 | 2026-07-17 | 3
- 2026-07-14 | 規則/狀態/資料 三分類(W2 家族 pattern 卡,M2 追蹤用) | conntrack 初分類答「規則」;etcd 未自答 | 規則/狀態/資料判準沒成反射 | parked | 3 | 2026-07-22 | 1
- 2026-07-17 | NetworkPolicy 出廠全通 | 預測「陌生 Pod 連不到 db」,實測連得到 | 出廠全通;namespace 不做網路隔離 | parked | 3 | 2026-07-23 | 1
- 2026-07-23 | 跨 node 走路由表不是 iptables(層級混淆家族) | 問跨 node 第一個指令答 iptables,縮小重問答 resolv.conf | 改寫層(NAT)與轉送層(routing)混淆 | parked | 7 | 2026-09-10 | 0
- 2026-07-23 | kube-proxy 不在 Pod 啟動路徑上 | 把 kube-proxy 列為 kubelet 建 Pod 三件事之一 | 控制路徑 vs 資料路徑混淆 | parked | 3 | 2026-08-07 | 1
- 2026-07-17 | default-deny 後的分層(DNS 層 vs 連線層) | 只答「連線不到」,不分辨死在 DNS 層還是連線層 | 層級混淆;兩步都被鎖時不問哪步先發生 | parked | 3 | 2026-10-19 | 2
- 2026-07-28 | veth 誤記「跨 node 連線」 | 答「veth 是跨 node 的網卡連線」 | veth 只管 Pod netns 到 root netns 那段 | parked | 7 | 2026-08-10 | 1
- 2026-07-28 | iptables=一棟樓(nat 表/filter 表) | 幻影站 4 + 誘答「DNAT 做完才進 iptables」 | 把 iptables 當一站,不知 DNAT 就在 nat 表裡 | parked | 3 | 2026-07-31 | 0
- 2026-07-20 | CNI 基本合約 vs 選配 | 合約三件事兩輪講不出,把 NetworkPolicy 混進合約本體 | 新教內容首輪未固化 | parked | 3 | 2026-07-23 | 0
- 2026-07-19 | 兩張獨立名單(3-2 坑二) | 「只開 backend ingress,frontend curl 通嗎」答「可以吧」 | 規則剛教完沒跑兩關檢查程序,憑感覺猜 | parked | 3 | 2026-07-22 | 0
- 2026-07-19 | NetworkPolicy 靜默無效(四引擎第四行) | Transfer 只給零件不組裝整條鏈 | 先跳結論等追問才補深度 + 隱性會 | parked | 3 | 2026-07-22 | 0
- 2026-07-07 | Ingress YAML schema | `backend.service` 寫成字串 + `pathType: prefix` 小寫 | service 是 object 型別;enum 大小寫敏感 | parked | 3 | 2026-07-10 | 1
- 2026-08-04 | 分層判準:關掉 API Server 還在不在(工具卡,層級混淆家族的解藥) | s25 冷測 4/5,cgroup memory limit 誤放右欄 | 同名詞的兩個分身(宣告 vs 執行體)沒分開 | parked | 3 | 2026-08-08 | 1
- 2026-08-05 | 誰把 limit 寫進 cgroup、什麼時候寫 | 答「scheduler 嗎」 | 控制面與 node 上元件職責混淆 | parked | 3 | 2026-08-08 | 0
- 2026-09-04 | 判準跑錯軸:RBAC 題答成 NetworkPolicy | 跨 ns RoleBinding 題結論對,理由給 NetworkPolicy | 物件存在範圍 vs 網路隔離兩軸混用 | parked | 3 | 2026-09-07 | 0
- 2026-09-03 | RWO 的 Once 數的是 node 不是 Pod | 共用 PVC 誘答答「RWO 應該是 POD」 | 把 volume 掛載限制記在 Pod 層,實際在 node 層 | parked | 3 | 2026-09-06 | 0
- 2026-08-05 | LVM 三層 + 擴容四步(學員課後自己要求復習,foundational pull) | Q1/Q2 結論皆對但兩題都只給結論 | 判準句慣性省略;LVM 的 PV 與 k8s 的 PV 同名不同物 | parked | 3 | 2026-08-08 | 0
- 2026-08-05 | PV ↔ PVC 是 1:1 獨佔 | 自曝「我以為是 PV 1:多」 | 「一份儲存給多人用」的直覺貼錯層 | parked | 3 | 2026-08-08 | 0
- 2026-08-04 | container 可寫層在硬碟不在 memory(overlayfs 三層) | 「process 死掉檔案去哪」答「存在 memory」 | 把 ephemeral 誤等於 in-memory | parked | 3 | 2026-08-07 | 0
- 2026-08-04 | emptyDir 綁 Pod 不綁 container | 「emptyDir 撐不撐得過 kill 1」答「不在了」 | 三層階梯中間一階沒有實體錨點 | parked | 3 | 2026-08-07 | 0
- 2026-08-06 | PID 1 的 signal 保護(kernel 層,新知識卡) | 未答錯,實驗意外撞出,全程教練驅動未經抽考 | 需抽考驗留存 | parked | 3 | 2026-08-09 | 0
- 2026-08-06 | Pod 不會「重啟」,只會被丟掉重建 | 答「pod 會重啟 or 調節 編排」,講不出誰在什麼條件動手 | 把 Pod 當會重啟的長壽物件而非可拋棄單位 | parked | 3 | 2026-08-09 | 0
- 2026-08-06 | 持久性看「掛在哪」不看名字(兩個分身判準第四次換皮) | 未答錯,`/proc/mounts` 撞出 emptyDir 在真磁碟、PVC 在 tmpfs | `PersistentVolume` 這名字沒有保證力 | parked | 3 | 2026-08-09 | 0
- 2026-08-20 | 判準給完當場套用不上(pattern 卡,教學法層級) | 同堂兩次,判準給完 30 秒內套用不上 | 判準被當成聽過的一句話,不是拿來用的工具 | parked | 3 | 2026-08-23 | 0
- 2026-08-28 | StatefulSet 每個 replica 一份獨立資料(不是共用一份) | 3 開到 5 問幾份資料,答「still is 3 data」 | 把「每人一份儲存」誤讀成「大家共用一份」 | parked | 3 | 2026-09-04 | 0
- 2026-09-01 | 建 Pod 的權限 vs Pod 裡程式呼叫 API 的權限(誰用誰的身分) | 答「不會,因為根本沒有到建立 pod」 | controller 建 Pod 與 Pod 呼叫 API 誤用同一身分 | parked | 3 | 2026-09-04 | 0
- 2026-09-08 | 成功訊息不保證做到你以為的事(pattern 卡,ops 判準,同堂三次) | `-n ALL` 查了不存在的 ns、`--as=$SA` 空變數沒假扮、`patched (no change)` | 不先驗證指令是否真的生效就改結論 | parked | 3 | lab 中即測(2026-09-15 起不排卡) | 0
- 2026-09-08 | `auth can-i --list` 不加 `--as` 問的是自己 | chunk 3 驗收給裸指令,無 `--as` 無 `-n`(同堂第二次);09-15 首答「`--as` 用 role 去模擬」 | 排障要問壞掉的身分,預設問的是自己;Role 是權限清單不是身分 | parked | 3 | C-5 引子題 | 0
- 2026-10-13 | NetworkPolicy 只管 podSelector 選到的 Pod | 答「有一條 NP 被套用就以這條為主」,提示後自答;s48 換皮(prometheus 被 Ingress-only policy 選中,它打 web)答「不會通,因為被選中了」✗,方向提示後 ✅ | 把 policy 當 ns 級開關 / 選中就全擋,不看 policyTypes 方向 | parked | 3 | 2026-10-19 | 1
- 2026-10-13 | NetworkPolicy port 看 DNAT 後的 Pod port | ingress 先答 80;egress 又答 80,實驗 timeout 後自答 DNAT | Service port 被當成一路帶到 gate | parked | 3 | 2026-10-16 | 0
- 2026-10-13 | from 裡 `-` 的 AND/OR | B(OR)答「只要 ns=netpol-lab 就可以」,學員累直給;s47 A 預測 ✅ 帶因為、B 三顆全通結論對,壓測 y(ns other、app=prometheus)答「通,因為符合 app=prometheus」✗;s48 實測 y=FAIL 推翻,G 根因一句到位、AND 修法寫對(supported),追問兩個 `-` 後果只答「規則聯集」 | OR 要逐項算再相加;單獨 podSelector = policy 所在 ns;OR 的 blast radius 講不具體 | parked | 3 | 2026-10-19 | 2
- 2026-10-16 | NetworkPolicy stateful:回程封包靠 conntrack 放行 | prometheus 被 Ingress 全擋,預測它 curl web 拿不到 response(timeout),實測 200 | 把 policy 當成逐封包過濾,不知規則只檢查連線第一個封包 | parked | 3 | 2026-10-19 | 0
- 2026-10-20 | nodeAffinity 只有軟性 | 以為 nodeAffinity 沒對到就去別台、nodeSelector 才硬;F teach-back 又講成「Score 加分」,追問後改口 required | required=Filter 硬擋 Pending、preferred=Score;nodeSelector=required 簡化版 | parked | 3 | 2026-10-23 | 0
- 2026-10-20 | maxUnavailable 讀成不能砍 | surge=0/unavailable=1 答「跑不動,不能新增也不能砍」;填空答最少剩 1 顆(應 2) | maxUnavailable=可少幾顆,最少在跑 = replicas − maxUnavailable | parked | 3 | 2026-10-23 | 0
- 2026-10-20 | antiAffinity 能表達數量 | F 誘答「required antiAffinity zone 可把 6 副本平均 3 AZ」答「也行」,反證後想改成「no 3 pods」 | required antiAffinity 只有是非(每 domain 最多 1),數量只能 topologySpread maxSkew | parked | 3 | 2026-10-31 | 0
- 2026-10-20 | FailedScheduling 行對應修法 | `didn't match affinity/selector` 答修 toleration;`untolerated taint` 答加 label(兩向皆反,s49 同錯) | 照訊息關鍵字:taint 行→Pod 加 toleration;affinity/selector 行→node 加 label 或改 selector;Insufficient→容量 | parked | 7 | 2026-11-04 | 1
- 2026-10-28 | 調低 target 讓 HPA 變快 | F 誘答「target 50%→30% 解決前 1 分鐘 5xx」答「應該算對」 | 盲區延遲不變;調低 target 只是平常多開 Pod 買緩衝(延遲 vs 緩衝兩個變數) | parked | 3 | 2026-10-31 | 0

### Queue rows removed with them

- mistake:FailedScheduling是scheduler寫的 | mistake | 3 | 2026-10-19 | active
- mistake:unschedulable等事件喚醒 | mistake | 3 | 2026-10-23 | active
- mistake:RBAC-watch看請求形狀 | mistake | 3 | 2026-10-19 | active
- mistake:兩道門(namespace視野vsUID身分) | mistake | 3 | 2026-09-28 | active
- mistake:YAML-validation | mistake | 3 | 2026-08-08 | active
- mistake:ImagePullBackOff | mistake | 3 | 2026-08-09 | active
- mistake:dry-run-兩層 | mistake | 3 | 2026-08-09 | active
- mistake:三分類-家族卡 | mistake | 3 | 2026-07-22 | active
- mistake:NetworkPolicy-出廠全通 | mistake | 3 | 2026-07-23 | active
- mistake:default-deny-分層(DNS vs 連線) | mistake | 3 | 2026-10-19 | active
- mistake:跨-node-走路由表 | mistake | 3 | 2026-08-13 | active
- mistake:blackhole路由與本機/32 | mistake | 3 | 2026-08-13 | active
- mistake:分層判準-關掉APIServer還在不在 | mistake | 3 | 2026-08-08 | active
- mistake:誰把limit寫進cgroup(kubelet不是scheduler) | mistake | 3 | 2026-08-08 | active
- mistake:LVM三層+擴容四步 | mistake | 3 | 2026-08-08 | active
- mistake:PV↔PVC是1:1獨佔 | mistake | 3 | 2026-08-08 | active
- mistake:可寫層在硬碟不在memory(overlayfs) | mistake | 7 | 2026-08-13 | active
- mistake:emptyDir-綁Pod不綁container | mistake | 7 | 2026-08-13 | active
- mistake:scheduler當萬用嫌犯 | mistake | 3 | 2026-08-13 | active
- mistake:產生者vs消費者(排障找誰) | mistake | 3 | 2026-08-13 | active
- mistake:對照組判準(同層有好有壞) | mistake | 3 | 2026-08-23 | active
- mistake:active≠還在幹活(健康檢查三層) | mistake | 3 | 2026-08-27 | active
- mistake:DeadlineExceeded語義 | mistake | 7 | 2026-08-27 | active
- mistake:PID1-signal保護 | mistake | 3 | 2026-08-09 | active
- mistake:Pod不會重啟只會被丟掉重建 | mistake | 3 | 2026-08-09 | active
- mistake:持久性看掛在哪不看名字(tmpfs) | mistake | 3 | 2026-08-09 | active
- mistake:veth-誤記跨node連線 | mistake | 7 | 2026-08-10 | active
- mistake:iptables-一棟樓 | mistake | 3 | 2026-08-06 | active
- mistake:kube-proxy-不在-Pod-啟動路徑 | mistake | 3 | 2026-08-07 | active
- mistake:判準給完當場套用不上(pattern) | mistake | 3 | 2026-08-31 | active
- mistake:StatefulSet每個replica一份獨立資料 | mistake | 7 | 2026-09-10 | active
- mistake:RWO數的是node不是Pod | mistake | 3 | 2026-09-06 | active
- mistake:判準跑錯軸(RBAC答成NetworkPolicy) | mistake | 3 | 2026-09-07 | active
- mistake:建Pod的權限vs呼叫API的權限(誰用誰的身分) | mistake | 3 | 2026-09-04 | active
- mistake:NetworkPolicy-靜默無效 | mistake | 3 | 2026-07-31 | active
- mistake:CNI-合約三件事 | mistake | 3 | 2026-07-23 | active
- mistake:兩張獨立名單 | mistake | 3 | 2026-08-06 | active
- mistake:Ingress-YAML-schema | mistake | 3 | 2026-07-10 | active
- mistake:ClusterIP-全鏈(謎題B) | mistake | 14 | 2026-07-13 | active(resolved,考精度)
- mistake:成功訊息不保證生效(pattern) | mistake | 3 | 2026-09-11 | active(2026-09-15 起不排卡,lab 中即測)
- mistake:--list-要加---as | mistake | 3 | 2026-09-11 | active(09-15 supported 答對 A 框;C-5 引子題冷問)
- mistake:權限爆炸半徑跑錯判準軸 | mistake | 3 | 2026-10-12 | active(併入 C-5 IAM policy 收斂抽,不另開複習堂)
- mistake:PSS只查Pod不查Deployment | mistake | 3 | 2026-10-12 | active
- mistake:app為什麼要root(port<1024/root目錄) | mistake | 3 | 2026-09-30 | active
- mistake:nodeAffinity只有軟性 | mistake | 3 | 2026-10-23 | active
- mistake:maxUnavailable讀成不能砍 | mistake | 3 | 2026-10-23 | active
- mistake:antiAffinity能表達數量 | mistake | 3 | 2026-10-31 | active
- mistake:FailedScheduling行對應修法 | mistake | 7 | 2026-11-04 | active
- mistake:調低target讓HPA變快 | mistake | 3 | 2026-10-31 | active
