# 踩坑登記簿 (間隔複習用)
<!-- 每次踩到坑就加一筆,定期回來抽考自己 -->

## 格式說明

每筆記錄用下方 block 格式。`下次抽考日` 建議設在 3 天後,複習後再往後推 7 天、14 天。

---

## 範例 (Example, 可刪除)

**日期:** 2026-06-16
**主題:** Pod 排程

**踩的坑:** `kubectl run nginx --image nginx` 後 Pod 一直是 `Pending`

**根因:** 叢集只有 control-plane 節點,但 control-plane 預設有 taint `node-role.kubernetes.io/control-plane:NoSchedule`,所以沒有可用的 worker 可以排程

**正確做法:** 建叢集時要帶至少一個 worker 節點 (例如 `lab-cluster.sh up p0` 帶 2 個 worker),或是手動 `kubectl taint` 移除 control-plane 的 taint

**下次抽考日:** 2026-06-19

---

<!-- 從這裡開始加你自己的踩坑記錄 -->

**日期:** 2026-06-18
**主題:** YAML 欄位拼錯 / 讀 validation error

**踩的坑:** Deployment apply 失敗 `strict decoding error: unknown field "spec.selector.matchLabels"`(把 `matchLabels` 打成 `metaLabels`)

**根因:** k8s 嚴格解碼,遇到不認識的欄位直接退件(防打錯字卻無聲失敗)。錯誤訊息的 `unknown field "A.B.C"` 是藏寶圖,完整路徑直指出錯的層級與欄位。

**正確做法:** 讀 `unknown field "路徑"` → 去檔案找該路徑那層,看欄位名「不是拼錯就是放錯層」。selector 認親的正確欄位是 `matchLabels`,且必須等於 template.metadata.labels。

**下次抽考日:** 2026-06-30 (2026-06-23 抽考過,需引導才答對「檢查在 API Server、與 etcd 無關」,推 +7)

---

**日期:** 2026-06-22
**主題:** P1 probe — liveness vs readiness 混淆

**踩的坑:** 認為 liveness probe 可以拿來檢查「service 準備好接新連線/請求了沒」(把 readiness 的職責塞給 liveness),延伸成「liveness 去 check DB 連線」。

**根因:** 沒抓住兩種 probe 的本質差別 = 失敗後的「動作」不同。liveness 失敗 → 重啟;readiness 失敗 → 切流量不重啟。檢查 DB 這種外部依賴若放 liveness,DB 一慢 → 全 Pod liveness 失敗 → 集體重啟 → CrashLoopBackOff 雪崩(且 reconnection 風暴可能把 DB 壓垮)。

**正確做法:** 判斷句「**Would a restart fix this?**」Yes(自己 deadlock/卡死)→ liveness 可管;No(DB/下游/外部依賴,重啟也修不好)→ 那是 readiness,頂多切流量等恢復。liveness 只檢查「我這個 process 還活著嗎」。

**下次抽考日:** 2026-07-10 (2026-06-25 抽考通過核心判斷句;**2026-07-03 再抽 PASS**:自己講出判斷句「重啟能不能解決」+ 正回饋迴圈(重啟修不好→持續重啟→DB 更重)+ 羊群效應「同時失效」概念,唯英文詞 thundering herd 忘了(概念本懂,已當場撈回)。推 +7)

---

**日期:** 2026-06-23
**主題:** P1 rollout — image 名稱打錯 → ImagePullBackOff

**踩的坑:** Deployment 的 image 打成 `ngimx:1.25`(n→m)。`kubectl apply` **成功**、Pod 也建了也排程了,但卡在 `ImagePullBackOff` / `ErrImagePull`。

**根因:** 驗證有邊界。`ngimx:1.25` 是**語法合法**的字串,API Server 無從得知這個 repo 不存在 → 不擋。真的去 registry 拉 image 的是 **kubelet,在第 5 棒(runtime pull)**,拉的那一刻才發現 `repository does not exist`。對比 `metaData` 這種 schema 錯,API Server apply 當場就退件。

**正確做法:** `ImagePullBackOff` 第一個動作 = `kubectl describe pod <name>` 看 Events。Events 會直接印 `Pulling image "ngimx:1.25"` + 拒絕原因,一眼看到打錯字。分辨三類:`i/o timeout`=網路/egress、`401`/`toomanyrequests`=認證/限流、`repository does not exist`/`not found`=名稱或 tag 打錯。

**下次抽考日:** 2026-07-03 (2026-06-26 抽考通過,三類根因訊號 repository-not-exist/connection-refused/401-toomanyrequests 一次答全對,推 +7)

---

**日期:** 2026-06-27
**主題:** P2a 謎題B — ClusterIP / kube-proxy / DNAT 整條串不起來(Teach the Rookie F 段挖出)

**踩的坑:** ✅ RESOLVED (2026-06-28)。原坑:教菜鳥 full teach-back 時開頭就說「封包先**去** clusterIP **拿到** ip」,代表腦中的圖還是「封包跑去 ClusterIP 這個地方、跟它要一個真實 IP」(像問路/打總機)。零件被逐一逼出來都認得,但**自己一口氣串整條時崩掉**。另外中途把「健康 Pod IP 名單」答成 `iptables`(把「做改寫的規則」跟「要挑的名單」混為一談)。
**2026-06-28 解坑:** D段 lab 親手 `docker exec <node> iptables-save` 追完整鏈(KUBE-SERVICES 比對目的地→KUBE-SVC 機率LB→KUBE-SEP `DNAT --to-destination PodIP`),worker/worker2 兩台規則一致 → 實體看到「ClusterIP 只是規則裡的比對字串、封包從不拜訪它、改寫發生在出發地本機」。F段壓軸無鷹架全鏈 teach-back PASS。

**根因:** 謎題B 的反直覺核心沒打穿:ClusterIP **不是一個地方、沒有任何機器擁有它、封包從不拜訪它**。真相是封包正常寫上目的地送出,**還沒離開出發那台 node**,本機 kernel 就照 kube-proxy 預寫的 iptables 規則當場 DNAT 改寫目的地。改寫沒有「去 ClusterIP 拿 IP」這一步,發生在**出發地本機**。

**正確做法:** 一句話骨幹 = 「封包**不去** ClusterIP;是**出發地本機 kernel** 照 **kube-proxy 寫的規則**做 **DNAT**,把目的地換成 **Endpoints** 名單裡的真 Pod IP」。分清:iptables 規則=做改寫的**手(動作)**;Endpoints=該挑哪個 Pod 的**名單(資料)**,由 controller reconcile loop 維護、readiness 當閘門。手 ≠ 名單。

**下次抽考日:** 2026-07-13 (2026-06-28 D段+F段首過 Gate ✅;**2026-06-29 Weekly Review #1 二度無鷹架冷測再 PASS**=徹底封印,推 +14。今日補兩洞:(a) resolv.conf 裡的 nameserver IP=**CoreDNS 的 ClusterIP**,不是 backend 的;他把「resolv.conf 給去哪問 / CoreDNS 給 backend 是誰」兩步壓成一步,已拆;(b) 回程 reverse-NAT 那張表名字想不起來→補 **conntrack**(概念本懂)。下次抽考改問全鏈精度:誰寫 resolv.conf=kubelet、KUBE-SVC 機率LB 怎麼挑一個 SEP、conntrack 回程反向改寫。)

---

**日期:** 2026-06-28
**主題:** P2a CoreDNS — busybox nslookup 測叢集 DNS 被工具自身的 bug 騙

**踩的坑:** `kubectl run dnstest --image=busybox:1.36 ... -- nslookup backend` 回 NXDOMAIN「server can't find backend.svc.cluster.local」,差點以為 CoreDNS 壞了。但同一個 Service 用 FQDN `nslookup backend.default.svc.cluster.local` 立刻解析成功(→ ClusterIP 10.96.254.186)。

**根因:** CoreDNS 與 Service 註冊**完全正常**,是 **busybox(musl libc)的 nslookup 處理 `search` 清單不可靠**,漏試了該試的 `backend.default.svc.cluster.local`(resolv.conf 第一條搜尋網域)。一個用 glibc 的真實 app 在同 namespace 寫 `backend` 會成功。另外兩個現象:`options ndots:5` → 短名字(點<5)會把整串 search 網域一條條試過才放棄(高 QPS 會變 DNS 延遲坑);主機的 `*.oraclevcn.com`/`*.ts.net` 漏進 Pod 的 search 清單,沒中的查詢多繞外部 DNS。

**正確做法:** DNS 解析失敗的排障第一刀 = **先用 FQDN 測一次**,把「伺服器壞 vs 發問端(client/search/工具)壞」二分:FQDN 通 → CoreDNS 沒事,往 client/resolver 查;FQDN 不通 → 才查 CoreDNS。別拿 busybox 測叢集 DNS,用 `nicolaka/netshoot`(正規 dig/nslookup)。絕不因 nslookup 失敗就亂砍/重啟 CoreDNS。

**下次抽考日:** 2026-07-10 (2026-07-01 抽考:一開始把 conntrack 誤拉進 DNS 題=層級混淆,拆解後守住「全名測得到→CoreDNS 沒壞→別重啟」,為什麼由教練補,推 +7 到 07-08。**2026-07-07 提早再測:核心第一刀『先用 FQDN 二分』一時忘記,給梯子後自己定位到「問題在 resolv/search 補全端」→ 口頭型 + 需鷹架,拉回近期 07-10**)

---

**日期:** 2026-07-03
**主題:** P2a Ingress lab — `--dry-run=client` 綠燈騙人 + port vs targetPort 靜默不通

**踩的坑:** 手打 shop-ingress.yaml 有多個 bug(`numer`拼錯 number、`pathType: prefix` 小寫、`name`/`port` 少縮一層掉到 `service:` 外)。`kubectl apply --dry-run=client` 卻印 `created (dry run)` 說沒事,實際 `kubectl apply` 失敗、`get ingress` 空的(沒建起來,還誤以為成功)。另外 backend Service 少寫 `targetPort`(預設=port=80,但 container 聽 5678)/ 或 targetPort 打錯數字(5680)→ apply 成功但 curl connection refused。

**根因:** ① `--dry-run=client` 只在本機做 YAML 解析 + 基本結構檢查,**不認 kind 的完整 schema**,unknown field / enum 大小寫一律放行。真正的 strict decoding(unknown field 藏寶圖,同 2026-06-18 那條坑)發生在 **API Server = server 端**。② `port`(Service 對外門牌)vs `targetPort`(真正轉進 container 的 port)兩個都是合法數字,schema 不會擋,只有真的 curl 下去才現形。targetPort 填錯 = kube-proxy 的 DNAT 把封包送到沒人聽的 port → connection refused。

**正確做法:** 擋 typo 的那關要用 `kubectl apply --dry-run=server`(或 CI 用 kubeconform 帶 schema),client 會漏。讀 server 噴的 `unknown field "spec.rules[0]...numer"` 完整路徑 → 回檔案定位那一層那個欄位改。記 port=門牌、targetPort=真正的 container port,不確定就 `kubectl get svc -o yaml` 對 container 實際 listen port。

**下次抽考日:** 2026-07-09 (2026-07-06 抽考:client=本機查語法 ✅ 有引導答出;但 server dry-run 答成「走完 etcd 整個流程」=第三次在 etcd 角色滑掉。已釘:審查在櫃檯、落帳才算數,dry-run=server=審完不落帳(strict decoding+admission 全走、唯獨不寫 etcd)。半過,拉近期重抽「停在哪之前」)

---

**日期:** 2026-07-06
**主題:** P2a — L4 vs L7 分不清(什麼時候 L4 夠、什麼時候必須 L7)

**踩的坑:** 全鏈複習時把 L4/L7 記成「場景標籤」,以為「叢集內=L4、外部=L7」是規則;被問「shop.com/ 和 shop.com/api 兩個外部請求的信封(IP+port)差在哪」連卡兩次,自陳「L4 和 L7 永遠搞不清楚」。

**根因:** 沒抓住 L4/L7 的本質差別 = **做轉發決定需要讀到哪一層的資訊**。L4 只看得到信封(IP + port);L7 要拆信讀 HTTP 內容(Host header、URL path)。跟流量從內或外來完全無關。

**正確做法:** 唯一判準:「轉發決定需不需要讀 HTTP 內容?」不需要 → L4 夠(叢集內 caller 已自己決定目的地 / 一個 LB 對一個 Service / 非 HTTP 協定如 MySQL 3306)。需要 → 必須 L7(一個入口按 Host/path 分流多後端、canary by header、TLS termination)。關鍵例:shop.com/ 與 /api 信封完全相同,唯一差異在信紙(path),不拆信物理上不可能分流 = Ingress 存在理由。可遷移:ALB(L7) vs NLB(L4) 選型同一條判準。

**下次抽考日:** 2026-07-09

---

**日期:** 2026-07-07
**主題:** Ingress YAML — service 寫成字串 + pathType 大小寫 + client dry-run 假安心

**踩的坑:** 手寫 ingress.yaml 兩個 schema 錯:① `backend.service: shop-api`(把 service 寫成字串,該是 object `service: {name, port}`)② `pathType: prefix`(小寫,enum 只收 `Exact`/`Prefix`/`ImplementationSpecific`)。而且 `kubectl apply --dry-run=client` 回 `created (dry run)` **說「過」**,騙人。

**根因:** ① `service` 是 `IngressServiceBackend` 型別(object),塞字串 → decode 失敗(server 報 `cannot unmarshal string into ... IngressServiceBackend`;decode 錯擋在第一個、後面的 enum 錯還驗不到)② enum 值**大小寫敏感**,`prefix` ≠ `Prefix` ③ `--dry-run=client` 只做本機淺檢查、**不驗型別/enum**;`--dry-run=server` 才把 YAML 塞進 API Server 的 Go struct 真驗。

**正確做法:** 驗 k8s YAML 一律用 `--dry-run=server`(client 給假安心)。讀 `ValidationError(...路徑...)` / `cannot unmarshal ... of type X` 括號裡的**路徑**=藏寶圖,直指錯的欄位與該有的型別(同 P1 `unknown field` 那招)。修法:對照同檔已寫對的另一條規則照抄結構(他 `/web` 寫對、`/api` 寫錯)。

**下次抽考日:** 2026-07-10

---

**日期:** 2026-07-07
**主題:** Ingress 404 排障 — 兇手是壞掉的 port-forward、不是規則

**踩的坑:** curl 走 Ingress 拿 404(還先回過空白)。差點以為 Ingress 規則寫錯、要去改 YAML。

**根因:** 規則其實全對。照 404 階梯查:`get ingress` ADDRESS=`localhost`(已認領)、`get ingressclass` `nginx` 存在、nginx.conf 有 `server_name shop.com` = **規則層全綠**。真兇是**被 `Ctrl-C` 打斷的那條 port-forward 半死**,回假 404 / 空白。換一條乾淨的(不同 port 8081)→ 全 200。

**正確做法:** ① 404 先分層:規則層(host/path/ingressClass 認領)vs 後端層(endpoints/port)。規則層全綠 → 兇手在「**你測試所經過的那層**」,不在規則,別去改沒壞的東西。② `kubectl port-forward` 是會抖的除錯夾具、不是正式流量;不可信就先換乾淨再下結論。③ 延伸:任何人的「猜測」(含教練猜 trailing slash)都要先驗證再採信。

**下次抽考日:** 2026-07-11 (2026-07-09 G 段英文重測:規則層先查✅方向對,但「規則全綠後兇手在哪」連卡兩次〔忘記兩條教訓 → 誤猜兇手是 nginx-ingress 本身〕,教練直接給。純口頭沒重現,拉近期重抽,重點考「兇手 = 壞掉的 port-forward / 測試路徑那層,不是規則」)

---

**日期:** 2026-07-09
**主題:** Ingress L7 分流 — no-Host → 404 講得出結果、講不出 why(F 段教菜鳥挖出)

**踩的坑:** D 段實測 no-Host curl → 404 預測正確,但 F 段教菜鳥要解釋「為什麼」時,第一輪只講得出「因為有 host 會查看 curl 自己帶的」= 半句話,講不出關鍵的那個字。被追問「curl 自己帶的 Host 到底是什麼字」時卡住(「有點不知道怎麼說」),縮小成填空題後才補出來。

**根因:** 「會用/會預測結果」≠「會講 why」。缺的那一步是把抽象的「Host 比對」落到具體字串:curl 不加 `-H` 時,自動拿 **URL 裡的主機名**當 Host 填入 = 那串長 DNS `ingress-nginx-controller.ingress-nginx.svc.cluster.local`,跟規則裡的 `shop.com` 是**不同的字** → 沒有規則認領 → nginx 回 404。L7 分流 = 純字串比對,字不對就打槍。

**正確做法:** 講這條 why 的骨架三步:① curl 無 `-H` → Host 自動填 URL 主機名 ② 那個字(長 DNS)≠ 規則的 `shop.com` ③ 字串比不上 → 沒規則接 → 404。對照 `/apiv2`:Host 帶對 `shop.com`、但 path `/apiv2` 不等於路徑段 `/api`(Prefix 以斜線切段),掉到 `/` catch-all → web。

**下次抽考日:** 2026-07-11 (口頭型 + 需鷹架才補出,設 +2 天格;過了才進 3/7/14)
