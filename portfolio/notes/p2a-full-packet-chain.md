# P2a 全鏈整合筆記:一個請求的完整旅程

> 整合 chunk 1 (Service/kube-proxy/CoreDNS) + chunk 2 (Ingress)。
> 2026-07-06 整理。

## 這是什麼?(一句話)

一個請求從「只有名字」到「打進某個 Pod」,會依序經過名字層 (DNS) 和轉發層 (DNAT / L7 routing);叢集內走 L4 那套,外部進來多套一層 L7。

## 用什麼比喻理解?

- CoreDNS = 電話簿:查「shop-api 的號碼是多少」,查完就退場。
- ClusterIP = 公司代表號:沒有任何一支實體話機是這個號碼。
- kube-proxy = 在每台分機旁貼轉接表的人:只貼表,不接電話。
- iptables/DNAT = 話機底下的自動轉接:你撥代表號,話機自己改撥某支分機。
- conntrack = 通話記錄:對方回電時知道要顯示成代表號。
- Ingress 物件 = 櫃檯的分流告示(一張紙);Ingress Controller = 真的站在櫃檯看單子分流的人。

## 旅程 A:叢集內 Pod → Service(L4)

1. app 打 `http://shop-api:5678`,只有名字。
2. glibc resolver 查 `/etc/resolv.conf`(kubelet 建 Pod 時注入):
   `nameserver = CoreDNS 的 ClusterIP`,search list + `ndots:5`(短名補全成 FQDN)。
3. CoreDNS(kube-system Pods,watch API Server)回答 Service 的 ClusterIP。
   DNS 工作到此結束:只管名字 → IP。
4. app 對 ClusterIP 發 TCP。ClusterIP 是虛擬的:沒網卡綁它、封包永遠不會「拜訪」它。
5. 封包還沒離開本機,node kernel 按 kube-proxy 預寫的 iptables 規則:
   `KUBE-SERVICES`(比對 dst)→ `KUBE-SVC-xxx`(機率式挑後端)→ `KUBE-SEP-xxx`(DNAT 改寫成真 Pod IP:targetPort)。
   kube-proxy 只寫規則,搬封包的是 kernel。
6. 挑誰的名單 = Endpoints/EndpointSlice,controller reconcile 維護,readiness probe 當閘門。
7. conntrack 記下這筆 NAT;回程封包 src=PodIP 反向改寫回 ClusterIP,client 才認得。
8. 改寫後封包經 CNI 送達目標 Pod。每台 node 規則相同 = 去中心化,無中央瓶頸。

## 旅程 B:外部使用者 → shop.com(L7 疊在 L4 上)

1. 瀏覽器查 shop.com:外部 DNS(跟 CoreDNS 無關)→ 雲 LB 或 node IP。
2. 進叢集第一站 = ingress-nginx controller 的 Service(LoadBalancer/NodePort)。
   NodePort 是 kube-proxy 開的門:「進得了 nginx」靠 L4 那套。
3. nginx Pod(Ingress Controller = 引擎)watch Ingress 物件(= 規則),轉成自己的設定。
   沒 controller,Ingress 物件是躺著的紙(lab 實證:ADDRESS 空、不轉流量)。
4. nginx 讀 Host header + URL path,純字串比對(L7,與 DNS 無關,
   所以 `curl -H "Host: shop.com"` 偽造字串就能測;no-host/wrong-host 對照組 404)。
5. nginx 自己看 Endpoints 直接打後端 Pod IP(這一跳繞過 kube-proxy;
   但進門那段靠 kube-proxy,「kube-proxy 關掉沒差」是半真陷阱)。

## 分工表

| 角色 | 一句話 | 層 |
|------|--------|-----|
| /etc/resolv.conf | 「該去問誰」的紙條,kubelet 寫,指向 CoreDNS | 名字層 |
| CoreDNS | 叢集電話簿:名字 → ClusterIP | 名字層 |
| Service / ClusterIP | 穩定虛擬門牌(規則資料,不是地方) | L4 |
| Endpoints | 健康 Pod IP 名單(controller 維護,readiness 閘門) | L4 資料 |
| kube-proxy | 每台 node 的規則寫手,只寫不搬 | L4 |
| iptables / DNAT | kernel 的手:出發地本機改寫目的地 | L4 |
| conntrack | NAT 記憶:回程反向改寫;滿了 → 新連線 drop、舊連線照常 | L4 |
| Ingress 物件 | L7 分流規則(紙) | L7 資料 |
| Ingress Controller | 收 HTTP、比對 Host+path、轉發的引擎 | L7 |
| CNI | Pod 拿真實 IP、Pod 互通的地基 | L3 |

## 兩條鐵律

1. 名字層 vs 轉發層分開:DNS 只管名字→IP;DNAT 只管 IP→Pod。
   排障先分層:resolve 失敗查 DNS 段;連上但 refused 查轉發段(targetPort 坑)。
2. 規則(資料)vs 引擎(執行者):Service/Ingress 物件是規則;
   kube-proxy+kernel、nginx controller 是引擎。同一模式出現三次
   (kube-proxy / cloud LB provisioner / Ingress Controller)。

## 踩過什麼雷?(對應 mistake-registry)

- 以為「封包先去 ClusterIP 拿 IP」:錯,改寫發生在出發地本機 kernel。
- 把 Endpoints(名單)跟 iptables(手)混為一談。
- busybox nslookup 的 search list bug 誤判 CoreDNS 壞掉:先用 FQDN 測,分「伺服器壞 vs 發問端壞」。
- `--dry-run=client` 綠燈騙人:本機不認完整 schema;strict decoding 在 API Server(server 端)。
  dry-run=server 走完所有檢查但不寫 etcd(dry = 演練不落盤)。
- Service `port`(門牌)vs `targetPort`(container 真正聽的 port):填錯 apply 成功、curl refused。

## 面試怎麼回答?(30 秒版)

"In-cluster, a client resolves the service name through CoreDNS (the nameserver in
resolv.conf, injected by kubelet) and gets a virtual ClusterIP. No machine owns that IP.
The packet gets DNAT'ed on the source node by iptables rules that kube-proxy pre-programs,
picking a healthy Pod IP from Endpoints; conntrack remembers the mapping for the return
path. For external traffic, an Ingress controller like nginx sits behind a LoadBalancer or
NodePort service and does L7 routing by Host header and path; the Ingress object is just
rules, the controller is the engine that actually forwards."
