# P2a 網路深水區: 封包的完整旅程

> **如何使用此檔:** 這是 P2a 階段的教學素材庫,供 coach 在 C 段(核心原理)讀取並改編。
> 不要逐字唸稿,依學員反應選擇要深挖哪個切面。這是彈藥庫,不是逐字稿。
> 學員目前就在本 phase:C-1 已全畢業(只做複習錨點),C-2 概念已教完(session 11),下一步是 C-2 的 D 段 lab。
> 每個 chunk 對應一個 Simon Method 原子單位,通過 Feynman Gate(Recall + Transfer,keystone 必含誘答)再往下走。
> 安全鐵律:每個 lab 開頭必跑 `kubectl config current-context`,確認不是公司 PROD EKS context。

---

## P2a 學習藍圖

**目標**: 把 k8s 網路從「一堆物件名詞」變成「一條可以在白板上走完的封包路徑」。學完後,任何網路故障都能先答「封包死在哪一站、哪一層」。

**P2a 中心問題**: `Pod A 執行 curl http://backend-svc/api`,封包從離開 Pod A 到回應回來,每一站是誰、在哪一層、做了什麼?

這條問題貫穿全 phase:C-1 給了 DNS 與 DNAT 兩站,C-2 加上南北向入口,C-3 加上防火牆檢查點,C-4 把所有站串成完整旅程(畢業 gate)。

**學習路徑(Simon 切塊)**:

| Chunk | 主題 | 核心問題 | 狀態 |
|-------|------|---------|------|
| C-1 | Service / kube-proxy / CoreDNS | 名字怎麼變成 IP、虛擬 IP 怎麼變成真 Pod IP? | 已畢業,複習錨點 |
| C-2 | Ingress(keystone) | 外部流量怎麼按 host/path 分流進來? | C 段已教,待 D 段 lab |
| C-3 | NetworkPolicy(keystone) | 誰能跟誰講話,由誰執行? | 未教 |
| C-4 | CNI + 封包全鏈路(keystone, gate 核心) | 封包物理上怎麼從 A 走到 B? | 未教 |
| C-5 | EKS VPC CNI 對照(選配) | 雲上跟 kind 差在哪? | 選配 |

**環境**: 本機 kind 3 節點,`bash scripts/lab-cluster.sh up p0`,context 是 `kind-k8s-coach-p0`。C-3/C-4 的 Calico lab 要另開 p2a 叢集(見 C-3 lab 前置)。

---

## C-1 複習錨點: Service / kube-proxy / CoreDNS(已畢業,不重教)

> 本節只供 A 段複習抽考與後續 chunk 回扣。學員已親手驗證以下每一條,直接引用他的鐵證,不重教。

**學員已親手驗證的事實(2026-06-28 D 段 lab + 兩次無鷹架冷測)**:

- 用 `docker exec <node> iptables-save` 追完整鏈:`KUBE-SERVICES`(比對 ClusterIP:port)→ `KUBE-SVC-*`(statistic random 機率負載均衡)→ `KUBE-SEP-*`(DNAT `--to-destination PodIP:port`)。
- worker 與 worker2 規則完全一致:證明 DNAT 發生在封包出發的 node 本機,去中心化、無中央 LB 瓶頸。
- ClusterIP 是虛擬 IP,沒綁任何網卡,封包從頭到尾沒有「去過」ClusterIP(謎題B 已雙重封印:session 9 有鷹架過、session 9 D 段實體鐵證、session 10 冷測二度 PASS)。
- conntrack 記住 DNAT 映射,回程封包來源被反向改寫回 ClusterIP,client 才認得。conntrack 是 node kernel netfilter 的表,不是 k8s 物件,`kubectl` 永遠看不到。
- conntrack table full:新連線被 drop,既有連線照常(這條精準度曾掉過,抽考排程 07-04,見下方彈藥)。
- CoreDNS 是叢集 DNS server(kube-system 的 Pod);Pod 的 `/etc/resolv.conf` 由 kubelet 注入,nameserver 指向 CoreDNS 的 ClusterIP(不是 backend 的 IP,這兩步他曾壓成一步,已拆開)。
- 跨 namespace 要 FQDN `service.ns.svc.cluster.local`;busybox 的 nslookup 有假陽性坑(他當場撞過、當場 debug)。
- DNS 排障階梯:`get svc` + `get endpoints` → CoreDNS Pod 活著嗎 → 進問題 Pod 用 FQDN nslookup;測得到就不要反射性重啟 CoreDNS。

**A 段抽考彈藥**(挑 1 題,別全上):

1. conntrack table full 的精準版:「哪種連線受影響、哪種不受?查哪兩個檔案?」(答:新連線 drop、舊連線照常;`/proc/sys/net/netfilter/nf_conntrack_count` vs `nf_conntrack_max`;`dmesg` 找 table full)。
2. 層級混淆疫苗(他 session 11 曾把 conntrack 誤拉進 NXDOMAIN 題):「Pod 報 could not resolve host,conntrack 有嫌疑嗎?」(答:沒有,那是 DNS 解析層;conntrack 在連線/NAT 層,解析都還沒完成)。抽考排程 07-08。
3. 「kube-proxy 掛了,現有連線會斷嗎?新的 Service 會通嗎?」(答:規則已寫進 kernel,現有與新連線照走既有規則;但 Endpoints 變化不再更新,新 Service 不通。回扣「寫規則 vs 搬封包」)。

`[RUNTIME: A 段抽考依 mistake-registry 到期項與學員當下狀態挑選;電話總機比喻(代表號=ClusterIP/分機=PodIP/話機轉接表=iptables)是他的原生錨點,回扣時直接用他的原話]`

---

## C-2 Ingress: 南北向 L7 路由(keystone)

### 已定型的心智模型(session 11 已教,速記供回扣)

學員已全程自己推出 Service type 階梯,不重教,只列錨點:

- NodePort 三痛點:醜網址(IP:3xxxx)、client 綁死單一 node IP 成單點、port 範圍受限。
- `type: LoadBalancer`:cloud controller 跑 reconcile loop 去雲上開 LB(他自己遷移回 P0 controller 模式)。痛點 A:N 個服務 = N 台 LB 的成本;痛點 B:L4 看不到 URL path(他自答的最關鍵一刀)。
- Ingress 的兩個第一性理由:一台 LB 進來按 host/path 分流(省 LB)+ 從 L4 升到 L7。
- 三合一對照表(他的定型模型):kube-proxy、cloud controller、Ingress controller 都是「規則=資料,Controller=引擎」同一個模式。
- keystone 誘答「apply Ingress 物件流量就自動分流嗎」已用過且秒殺,**不要重複**。

### 加深 1: pathType 與 IngressClass

**pathType 三種值**:

- `Exact`:整串完全相等才 match。`/api` 不 match `/api/`。
- `Prefix`:以 `/` 切段後逐段比對的前綴。`/api` match `/api`、`/api/v1`,但**不 match `/apiv2`**(不是字串前綴,是路徑段前綴)。
- `ImplementationSpecific`:交給 controller 自己定義(nginx 拿去做 regex 之類)。面試與生產都建議顯式寫 Prefix/Exact。

**IngressClass**:一個 cluster 可以同時跑多個 controller(例如 nginx 管內部、ALB 管外部)。Ingress 物件用 `spec.ingressClassName` 指定「這條規則歸哪個引擎管」。controller 只 reconcile 自己 class 的物件。沒寫 ingressClassName 且沒有 default class(`ingressclass.kubernetes.io/is-default-class` annotation)時,**沒有任何引擎認領這條規則,靜默不生效**,這是生產最常見的「Ingress 沒反應」根因之一。

### 加深 2: defaultBackend 與 TLS 終止

- `defaultBackend`:所有規則都沒 match 到時的兜底 Service。沒設的話 nginx controller 回自己的 404 頁(response header 有 `nginx`,這是排障線索:404 是引擎回的,不是你的 app 回的)。
- **TLS 終止(TLS termination)**:憑證以 `kubernetes.io/tls` type 的 Secret 掛在 Ingress 的 `spec.tls`,controller 在自己這站解掉 HTTPS,往後端送的是明文 HTTP(叢集內)。好處:憑證集中管理一份,backend Pod 完全不用碰憑證。controller 靠 SNI(client hello 裡的 hostname)決定回哪張憑證。若合規要求全程加密,才做 re-encrypt 或 mTLS(P4 再展開)。

### 加深 3: Controller 怎麼把 Ingress 變成 nginx.conf

回扣他的三合一表,把「引擎」內部打開:

```
watch API Server (Ingress / Service / EndpointSlice / Secret)
        |
        v
   內部 model(host -> path -> 後端 Pod IP 名單)
        |
        v
   render 出 nginx.conf(server block = host, location = path)
        |
        v
   驗證 + reload nginx(endpoint 名單變化走 lua 動態更新,不用 reload)
```

兩個磨精準的點:

1. 這就是 reconcile loop,只是 desired state 是 Ingress+Endpoints,actual state 是 nginx.conf。P0 複利第 N 次出現。
2. nginx controller 預設**不經過 ClusterIP**,直接把上游設成 Pod IP,但名單來自 EndpointSlice。所以 Service 物件仍然是靈魂:readiness 閘門照樣生效(回扣他 P1 probe lab:rm readiness 後 Pod 從 Endpoints 消失,Ingress 後端名單同步少一個)。

### 404 / 502 / 503 排障階梯(先分層,再動手)

| 症狀 | 誰回的 | 根因層 | 先查什麼 |
|------|--------|--------|---------|
| 404 | nginx 引擎自己 | 規則層:host 不 match(忘了帶 Host header)、path 不 match(Prefix 語義)、ingressClassName 沒人認領 | `kubectl get ingress`(ADDRESS 有沒有)、`describe ingress`、curl 帶不帶 `-H "Host:"` 的差異 |
| 503 | nginx 引擎 | 後端名單層:Service 存在但 Endpoints 空(replicas=0、selector 錯、readiness 全紅) | `kubectl get endpoints <svc>` |
| 502 | nginx 引擎 | 後端連線層:有 Pod IP 但連不上(Service targetPort 錯、app 沒聽那個 port、NetworkPolicy 擋住) | `kubectl exec` 進 controller Pod curl Pod IP 直測 |
| 連 404 都拿不到 | 沒人回 | 入口層:controller 沒裝/沒 Ready、port-forward 斷了 | `kubectl get pods -n ingress-nginx` |

教學句:404 是「規則沒對上」,502/503 是「規則對上了但後端有事」。先分這兩層,再往下挖。這直接對接他的層級混淆弱點:別讓他一看 404 就去查 Pod。

### D 段 lab: 親手讓規則長出引擎(下次 session 主菜)

> 學員偏好自己敲指令、YAML 給規格自己寫。lab 檔放 `portfolio/manifests/`。
> 全 lab 重點體驗:**先 apply 規則、親眼看它完全沒反應,再裝引擎、看它活過來**。

**Step 0 安全確認**

```bash
kubectl config current-context
```

必須是 `kind-k8s-coach-p0`。不是就停,跑 `kubectl config use-context kind-k8s-coach-p0`。

**Step 1 佈兩個後端**(給規格,他自己寫 YAML)

- Deployment `shop-api`:image `hashicorp/http-echo`,args `-text=api`、`-listen=:5678`,replicas 2。
- Deployment `shop-web`:同上但 `-text=web`。
- 各配一個 ClusterIP Service,port 80 → targetPort 5678。
- 驗證:`kubectl get endpoints shop-api shop-web` 都要有 Pod IP(回扣 C-1:Endpoints 是健康名單)。

**Step 2 先 apply Ingress,見證「沒有引擎的規則」**(給規格)

- `ingressClassName: nginx`;host `shop.com`;path `/api`(Prefix)→ shop-api:80;path `/web`(Prefix)→ shop-web:80。

```bash
kubectl get ingress
kubectl describe ingress shop-ingress
```

觀察點:ADDRESS 欄永遠空白,Events 一片安靜,什麼都沒發生。API Server 只驗 schema 存 etcd,沒有引擎來認領。讓學員自己說出為什麼(他 session 11 已推過,這裡是實體驗證)。

**Step 3 裝 ingress-nginx controller**

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/kind/deploy.yaml
kubectl get pods -n ingress-nginx
```

controller Pod 會卡 **Pending**。這是刻意留的 P0 複利點:讓他自己 `describe` 找根因(nodeSelector 要求 `ingress-ready=true` 的 node,scheduler filter 階段全滅)。然後:

```bash
kubectl label node k8s-coach-p0-worker ingress-ready=true
kubectl wait -n ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s
```

**Step 4 親眼看 reconcile 產物**

```bash
kubectl get ingress
kubectl exec -n ingress-nginx deploy/ingress-nginx-controller -- grep -c "shop.com" /etc/nginx/nginx.conf
```

ADDRESS 出現了;nginx.conf 裡長出了 `shop.com` 的 server block。規則(etcd 裡的資料)被引擎 render 成了設定檔。

**Step 5 實測分流**

```bash
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80 &
curl -s -H "Host: shop.com" http://127.0.0.1:8080/api
curl -s -H "Host: shop.com" http://127.0.0.1:8080/web
curl -s http://127.0.0.1:8080/api
curl -s -H "Host: shop.com" http://127.0.0.1:8080/apiv2
```

預期:前兩個分別回 `api`、`web`;第三個 404(沒帶 Host,L7 靠 header 分流的實證);第四個 404(**Prefix 是路徑段前綴不是字串前綴**,現場驗證加深 1)。

叢集內替代測法(順便運動一次 CoreDNS):

```bash
kubectl run tmp-curl --rm -it --image=curlimages/curl --restart=Never -- curl -s -H "Host: shop.com" http://ingress-nginx-controller.ingress-nginx/api
```

**Step 6 排障階梯實體化(選做,時間夠才上)**

```bash
kubectl scale deploy shop-api --replicas=0
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: shop.com" http://127.0.0.1:8080/api
kubectl scale deploy shop-api --replicas=2
```

預期 503(Endpoints 空)。對照 404 的規則層,讓排障表活起來。

**清理**:`kill %1`(port-forward)、保留 manifests 進 portfolio,controller 可留著給 chaos drill P2a-4 用。

`[RUNTIME: Step 3 的 Pending 若學員自己秒解就不停留;Step 6 依當日剩餘體力取捨]`

### 打穿底層(First-Principles Dive)

Ingress controller 的本質是**反向代理(reverse proxy)+ 設定檔生成器**。反向代理是比 k8s 老二十年的技術:nginx/HAProxy 收下 TCP 連線、讀完 HTTP header、再以自己為 client 向後端另開一條連線。所以經過 Ingress 的是**兩段獨立的 TCP 連線**,這解釋了:為什麼 backend 看到的 source IP 是 controller Pod 的 IP(除非傳 `X-Forwarded-For`)、為什麼 TLS 可以在中間終止、為什麼 502 是「第二段連線失敗」。

**遷移題**:「公司地端機房沒有 k8s,用一台 nginx 檔在 20 個 web app 前面。跟 Ingress controller 差在哪?」(答:能力一模一樣;差在設定檔誰維護。地端是人手改 nginx.conf 再 reload;Ingress 是把設定變成 API 物件,controller 自動 render。又是 declarative vs imperative,P0 複利。)

### 誘答彈藥(挑 1-2 題,已用過的「apply 就自動分流」禁用)

1. 「`pathType: Prefix` 的 `/api` 也會 match `/apiv2`,因為 Prefix 就是字串前綴嘛。」(錯:以 `/` 切段比對,`/apiv2` 的第一段是 `apiv2` 不是 `api`。lab Step 5 剛好埋了實證。)
2. 「有了 Ingress 直接把流量打到 Pod,Service 跟 Endpoints 就沒用了,可以刪掉。」(半錯最毒:nginx 確實預設直連 Pod IP 繞過 ClusterIP,但 Pod IP 名單正是從 EndpointSlice 來的,Service/readiness 仍是靈魂。磨「繞過轉發路徑」與「繞過控制資料」的差別。)
3. 「curl 回 404,代表 backend Pod 掛了,先去 restart Pod。」(錯:404 是引擎的規則層,backend 掛是 502/503。打他「先跳結論」的老毛病。)
4. 「TLS 憑證要掛在每個 backend Pod 上,Ingress 只是轉發。」(錯:TLS 終止在 controller,Secret 掛 Ingress,backend 收明文。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 公司 billing 平台 EKS 上,幾十個微服務要對外,不可能一服務一台 ALB |
| **生產怎麼做** | 裝 AWS Load Balancer Controller,Ingress 物件 reconcile 成 ALB 的 listener rules;一台 ALB 承載多服務的 host/path 分流。憑證在 ACM,annotation 掛上去 |
| **真實踩坑** | Ingress 寫好 apply 完流量進不來,查半天發現 `ingressClassName` 沒寫,而 cluster 裡沒有 default IngressClass:沒有任何 controller 認領,物件靜默躺在 etcd。症狀是「一切看起來都對但完全沒反應」,跟沒裝 controller 一模一樣 |
| **面試怎麼問** | 「NodePort、LoadBalancer、Ingress 什麼時候用哪個?Ingress controller 內部怎麼運作?404 跟 502 你分別先查什麼?」 |

### 術語卡(Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| reverse proxy | /rɪˈvɜːrs ˈprɒk.si/ | A server that accepts client connections and opens separate connections to backends on their behalf | 幫後端擋在前面收連線的中間人,經過它=兩段獨立 TCP |
| TLS termination | /tiː el es ˌtɜː.mɪˈneɪ.ʃən/ | Decrypting HTTPS at the proxy so backends receive plain HTTP | HTTPS 在入口就解掉,憑證集中管一份,後端不用碰 |

(Ingress Controller 卡 session 11 已建,07-04 抽,不重建。)

---

## C-3 NetworkPolicy: 叢集內防火牆(keystone)

### 核心概念

k8s 網路的出廠預設是**全通**:任何 Pod 可以連任何 Pod,跨 namespace 也一樣(回扣 P1 已澄清的點:k8s namespace 只是邏輯分組,不做網路隔離)。billing 平台的 db Pod 出廠就裸奔在所有 Pod 面前。

NetworkPolicy 是**白名單宣告**:一旦有任何 policy 選中某個 Pod,該 Pod 在該方向(ingress/egress)就從全通翻轉成 default-deny,只有名單上的例外放行。

```
出廠:  frontend ---> backend ---> db     (誰都能連誰,含隔壁 ns 的陌生 Pod)

上了 policy 之後:
        frontend ---> backend   OK  (名單上)
        陌生 Pod  -X-> backend       (不在名單,丟棄)
        backend  ---> db        OK
        frontend -X-> db             (跳層存取被擋)
```

**default-deny 起手式**(生產標準做法):每個 namespace 先上一條「空白名單」,再逐條開洞。

- `podSelector: {}`:選中 ns 內所有 Pod。
- `policyTypes: [Ingress, Egress]` 且不寫任何 rule:兩個方向全鎖。

### 語義規則(這是本 chunk 的考點密集區)

1. **多條 rule 之間是 OR**:`ingress:` 陣列裡每個元素獨立放行,任一條 match 就通。
2. **同一個 from 元素內的 podSelector + namespaceSelector 是 AND**;拆成兩個元素就變 OR。YAML 差一個 `-` 語義天差地遠:

```yaml
# AND: 「prod namespace 裡的 app=frontend」才放行
- from:
  - namespaceSelector: { matchLabels: { env: prod } }
    podSelector: { matchLabels: { app: frontend } }

# OR: 「prod ns 的任何 Pod」或「任何 ns 的 frontend」都放行(範圍大很多)
- from:
  - namespaceSelector: { matchLabels: { env: prod } }
  - podSelector: { matchLabels: { app: frontend } }
```

3. **ingress 和 egress 是兩張獨立白名單**:A 連 B,要 A 的 egress 允許到 B,**且** B 的 ingress 允許來自 A,兩邊都過才通。開了一邊忘另一邊是最常見翻車。
4. **ipBlock**:對 cluster 外的 CIDR(例如 RDS 的網段)用,支援 `except` 挖洞。
5. **回程不用另外開**:policy 作用在「連線」不在「封包」,底層靠 conntrack 認得 established 連線的回程(回扣 C-1:又是那張 kernel 的連線表,第三次出現)。
6. **DNS 大坑**:上了 default-deny egress 後,連 CoreDNS 的 UDP/TCP 53 也被鎖。app 症狀是「could not resolve host」,死在 DNS 解析層,不是連線層。這正是學員的層級混淆弱點,lab 會親手撞一次。

### NetworkPolicy 是宣告,CNI 才是執行者

三合一對照表加開第四行(用他自己的定型模型):

| 規則(資料) | 引擎(執行者) | 引擎的產出 |
|------------|--------------|-----------|
| Service | kube-proxy | iptables DNAT 規則 |
| type: LoadBalancer | cloud controller | 雲上的 LB |
| Ingress | Ingress controller | nginx.conf |
| **NetworkPolicy** | **CNI plugin(Calico 的 felix)** | **node 上的 iptables/eBPF 過濾規則** |

關鍵事實:**kind 預設的 kindnet 不實作 NetworkPolicy**。apply 會成功(API Server 只驗 schema)、物件躺在 etcd、`kubectl get netpol` 看得到,但沒有任何引擎把它變成 kernel 規則,**靜默完全無效,不會有任何報錯**。這是四個引擎裡「沒引擎」後果最危險的一個:Ingress 沒引擎是功能不通(馬上發現),NetworkPolicy 沒引擎是**安全假象**(以為擋了其實全通)。

### D 段 lab: Calico + default-deny(給規格,學員自己寫 YAML)

**前置:開 p2a 叢集**(kindnet 換 Calico 不能原地換,要新叢集)

先建 `workspaces/k8s/clusters/kind-p2a.yaml`:

```yaml
# P2a: no default CNI, install Calico for NetworkPolicy + packet-path labs
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: k8s-coach-p2a
networking:
  disableDefaultCNI: true
  podSubnet: "192.168.0.0/16"
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

```bash
bash scripts/lab-cluster.sh down p0
bash scripts/lab-cluster.sh up p2a
kubectl config current-context
kubectl get nodes
```

context 應為 `kind-k8s-coach-p2a`。**觀察點(教學金礦)**:nodes 全部 **NotReady**、CoreDNS Pending。`kubectl describe node` 找到 `network plugin not ready`:沒有 CNI,kubelet 沒辦法給 Pod 接網線,這裡先感受 CNI 的存在,C-4 再打開它。

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.2/manifests/calico.yaml
kubectl get nodes -w
```

Calico 起來後 nodes 轉 Ready。CNI 就位,叢集才算活。

**Step 1 佈場景**:三個 Deployment,labels 分別 `app=frontend`、`app=backend`、`app=db`(image 可用 `hashicorp/http-echo` 各自 `-text`),各配 ClusterIP Service。

**Step 2 基線測試**(先證明全通):

```bash
kubectl run tmp --rm -it --image=curlimages/curl --restart=Never -- curl -s -m 2 http://backend
```

frontend 裡 exec curl backend、db 也通。陌生 Pod(tmp)也通:出廠裸奔的實證。

**Step 3 default-deny**(規格:podSelector `{}`、policyTypes 兩個方向、無 rule)→ 重測:全斷,連 `curl http://backend` 的**名字解析都失敗**(could not resolve host)。停在這裡讓學員自己分層:死在 DNS 層還是連線層?為什麼?(egress 53 被鎖,還沒輪到連線。)

**Step 4 開 DNS 洞**(規格:egress to `namespaceSelector` match `kubernetes.io/metadata.name: kube-system` + `podSelector` match `k8s-app: kube-dns`,ports UDP/TCP 53)→ 重測:名字解得開了,但連線 timeout。又一次分層:現在死在哪層?

**Step 5 開業務洞**:backend 的 ingress 允許來自 `app=frontend`;frontend 的 egress 允許到 `app=backend` port 5678。兩條都上才通(語義規則 3 的實證)。db 只允許來自 backend。

**Step 6 驗收矩陣**:frontend→backend 通、tmp→backend 斷、frontend→db 斷、backend→db 通。manifests 進 `portfolio/manifests/`。

`[RUNTIME: Step 3/4 的分層追問是本 lab 靈魂,依他答題狀況決定要不要再壓;若卡兩次退回 ASCII 圖]`

### 打穿底層(First-Principles Dive)

NetworkPolicy 的執行面就是 C-1 看過的同一套 netfilter:felix 把 policy 編譯成 iptables 規則(或 eBPF 程式)掛在 node 上,對每條**新連線**做判定,判定過了就交給 conntrack 記住,後續封包走快速路徑。所以 policy 生效「對連線」而非「對封包」,回程免開洞。這跟雲上 Security Group(stateful firewall)是同一個原理,他天天在 AWS 用的東西底層是一家人。

**遷移題**:「AWS Security Group 也是白名單、也不用開回程。SG 綁在 ENI 上,NetworkPolicy 綁在 Pod label 上。哪個模型在 Pod 大量生滅的環境更好用?為什麼?」(答:label selector 天生跟著 Pod 走,IP/網卡層的規則要一直追著動態 IP 改;宣告式 selector 又是 desired state 思維。)

### 誘答彈藥(挑 1-2 題)

1. 「我 apply NetworkPolicy 成功、`get netpol` 也看得到,所以已經生效了,kindnet 上也一樣。」(錯:API Server 只驗 schema。沒有支援的 CNI 就是安全假象,靜默無效。這題打「四引擎」模型的第四行。)
2. 「default-deny 只需要擋 ingress,egress 是出去的流量,不用管。」(錯:資安上 egress 管的是資料外洩與橫向移動的第二步;語義上 A→B 要兩邊白名單都過。)
3. 「from 裡把 namespaceSelector 跟 podSelector 寫在同一個元素,跟拆成兩個元素效果一樣。」(錯:AND vs OR,差一個 `-` 白名單範圍差一個量級。)
4. 「上了 default-deny 之後服務連不上,是 conntrack 表被清掉了。」(錯:層級混淆疫苗,若 Step 3 他自己分層分得漂亮,這題可省。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 資安稽核要求 billing 平台的 db 層只能被 backend 存取 |
| **生產怎麼做** | 每個 namespace 標配 default-deny(ingress+egress),app 上線的 PR 必須同時附 NetworkPolicy;CI 用 conftest/OPA 檢查「新 Deployment 必有對應 policy」 |
| **真實踩坑** | 上了 default-deny egress 忘開 DNS,全 ns 的 app 同時報 could not resolve host。on-call 以為 CoreDNS 掛了去重啟(沒用),其實 CoreDNS 好好的,是 policy 把去程 53 鎖了。分層判斷:先問「解析層還是連線層」,再問「這層的路上誰能擋」 |
| **面試怎麼問** | 「k8s 預設 Pod 之間網路是什麼行為?怎麼做隔離?NetworkPolicy 由誰執行?如果 CNI 不支援會發生什麼?」 |

### 術語卡(Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| default deny | /dɪˈfɔːlt dɪˈnaɪ/ | A baseline policy that blocks all traffic unless explicitly allowed | 先全鎖再開洞,白名單思維的起手式 |
| east-west traffic | /iːst west ˈtræf.ɪk/ | Traffic between services inside the cluster, as opposed to north-south traffic entering or leaving | 叢集內服務互打=東西向;進出叢集=南北向(Ingress 管南北,NetworkPolicy 主場在東西) |

---

## C-4 CNI 與封包全鏈路(keystone,phase gate 核心)

### 核心概念: CNI 是一紙合約

CNI(Container Network Interface)不是某個軟體,是一紙**合約**:kubelet 建 Pod 時,呼叫 node 上的 CNI plugin 執行檔,合約要求它做三件事:給 Pod 的 network namespace 一張網卡、配一個 IP、把路由接好,讓這個 IP 全叢集可達。kindnet、Calico、AWS VPC CNI 都是不同的履約方式。

回扣 P1:Pod 的網路隔離=Linux network namespace。CNI 做的事,就是把一個孤島 netns 接進世界。

### veth pair 與同 node 通訊

veth pair 是 kernel 的虛擬網卡對,**一條網線的兩頭**:一頭塞進 Pod 的 netns(叫 eth0),另一頭留在 node 的 root netns。封包從一頭進、另一頭出。

```
node root netns
+---------------------------------------------+
|   +--------+        +--------+              |
|   | Pod A  |        | Pod B  |              |
|   | eth0   |        | eth0   |   <- netns 內|
|   +---|----+        +---|----+              |
|       | veth pair       | veth pair         |
|   veth-a            veth-b      <- root 側  |
|       |                 |                   |
|   [bridge 或 node 路由表把兩頭接起來]        |
+---------------------------------------------+
```

同 node 的 Pod A → Pod B:出 A 的 eth0 → veth-a 冒出在 root netns → 查 node 路由/bridge → 進 veth-b → B 的 eth0。全程沒出過這台機器,純 kernel 轉發。

### 跨 node: 直接路由 vs overlay

Pod IP 是叢集私有的,外面的路由器不認得。跨 node 有兩條路:

**直接路由(kindnet、Calico BGP 模式)**:每台 node 的路由表寫明「別台 node 的 Pod 網段,下一跳是那台 node 的真 IP」。封包原封不動,靠路由表接力。前提:node 之間的網路允許這些封包直跑(同 L2 或路由器配合)。

```
node1 路由表:  192.168.2.0/24 via <node2 真 IP>
封包:  [src: PodA-IP, dst: PodB-IP]  -> 直接送到 node2 -> node2 認得自己的 Pod 網段 -> 進 veth
```

**overlay(VXLAN / Calico 預設 IPIP)**:node 之間的網路不配合時,把整個 Pod 封包**塞進另一個封包**(encapsulation):外層是 node IP 對 node IP,內層才是 Pod 對 Pod。到了對面 node 拆封,像包裹裡再裝一個包裹。代價:每包多幾十 bytes 的 header(MTU 要扣)、封裝拆封的 CPU。

```
overlay:  [外層 src: node1-IP, dst: node2-IP | 內層 src: PodA-IP, dst: PodB-IP]
```

### 出 cluster: SNAT / MASQUERADE

Pod 要 curl 外面的網站:Pod IP 是私有的,對方回包時根本路由不回來。所以封包離開叢集前,node 的 iptables `POSTROUTING` 鏈做 **MASQUERADE**(動態版 SNAT):把 source 從 Pod IP 換成 node IP。回程再靠誰改回來?conntrack。跟 C-1 的 DNAT 是同一張表的鏡像操作:DNAT 改目的地、SNAT 改來源,conntrack 兩邊都記帳。

### 動手觀察(p2a Calico 叢集;規則同前,先 current-context)

```bash
kubectl run net-a --image=nginx --restart=Never
kubectl get pod net-a -o wide
kubectl exec net-a -- ip addr show eth0
```

記下 eth0 的 `@ifNN` 編號,去該 node 找網線另一頭:

```bash
docker exec k8s-coach-p2a-worker ip link | grep "^NN:"
```

看到 `cali...` 開頭的介面:veth pair 的 root 側,親眼摸到那條網線。

```bash
docker exec k8s-coach-p2a-worker ip route
```

觀察:本機 Pod 是一條條 `/32` 走 cali 介面;別台 node 的 Pod 網段走 `tunl0`(Calico 預設 IPIP overlay)。對照組:p0 叢集的 kindnet 是 `10.244.x.0/24 via <node IP>` 直接路由,兩種模式都親眼看過。

```bash
docker exec k8s-coach-p2a-worker iptables -t nat -S POSTROUTING | grep -i masq
docker exec k8s-coach-p2a-worker cat /proc/sys/net/netfilter/nf_conntrack_count
docker exec k8s-coach-p2a-worker cat /proc/sys/net/netfilter/nf_conntrack_max
```

MASQUERADE 規則與 conntrack 水位,gate 要考的查法先摸一遍(有 conntrack-tools 的機器可再用 `conntrack -L`)。

### 冷測劇本: 封包的完整旅程(gate 答案卷)

> 學員的已知弱點是「盲講漏中間棒次」(Weekly Review #1 結論:給固定骨架默數)。
> 這是 P2a 版的「五棒」:**七站骨架**,要求他白板默數 1 到 7,一站都不准跳。
> 場景:Pod A(node1)執行 `curl http://backend-svc/api`,backend Pod 在 node2。

| 站 | 層 | 發生什麼 | 誰做的 |
|----|-----|---------|--------|
| 1 名字 | DNS 解析層 | 查 `/etc/resolv.conf`(kubelet 注入,nameserver=CoreDNS 的 ClusterIP),問 CoreDNS 拿到 backend-svc 的 ClusterIP | CoreDNS |
| 2 出發 | Pod netns | 封包 [src: PodA-IP, dst: ClusterIP] 從 eth0 出去,經 veth pair 冒出在 node1 root netns | kernel |
| 3 改寫 | NAT 層 | 命中 KUBE-SERVICES → KUBE-SVC(機率選一個 SEP)→ DNAT 成 [dst: PodB-IP];conntrack 記下這筆映射 | kube-proxy 寫的規則,kernel 執行 |
| 4 防火牆 | 過濾層 | 若有 NetworkPolicy,felix 編譯的規則在此判定新連線放不放行 | CNI |
| 5 跨機 | 路由層 | node1 查路由:PodB 網段 → 直接路由下一跳 node2,或塞進 VXLAN/IPIP 外層封包 | CNI 佈的路由 |
| 6 抵達 | Pod netns | node2 拆封(若 overlay)→ 查本機路由 → veth → backend Pod eth0,app 收到 request | kernel |
| 7 回程 | NAT 層 | 回包 [src: PodB-IP] 在 node1 被 conntrack 反查、src 改回 ClusterIP,Pod A 的 TCP 對得上號 | conntrack |

變體(gate 會抽):

- **同 node**:第 5 站退化成本機 veth 對接,其他不變。
- **南北向**:external client → LB → Ingress controller Pod(TLS 終止、讀 Host/path)→ controller 以自己為 client 直連 backend Pod IP(名單來自 EndpointSlice)→ 兩段獨立 TCP。
- **出 cluster**:Pod → 外部 API,第 3 站沒有 DNAT(目的地不是 ClusterIP),出 node 前 POSTROUTING MASQUERADE 換 src 為 node IP,回程 conntrack 改回來。
- **conntrack 滿了**:症狀=新連線失敗、舊連線照常;查 `nf_conntrack_count` vs `nf_conntrack_max`、`dmesg | grep conntrack` 找 table full;治標=調大 max,治本=找連線洩漏源(短連線風暴、time-wait 堆積)。要求他主動講治標/治本,不等追問(session 5/6 的同一條改進項)。

`[RUNTIME: 冷測時注意謎題B 舊誤解(封包「先去 ClusterIP」)是否借屍還魂;第 1 站與第 3 站之間是否又壓成一步(session 10 抓過);依 mistake-registry 決定抽哪個變體]`

### 打穿底層(First-Principles Dive)

整個 C-4 沒有任何 k8s 發明的技術:veth、bridge、路由表、VXLAN、NAT、conntrack 全是 Linux kernel 既有能力,CNI 只是「按合約把它們佈署好」的腳本。所以 k8s 網路排障的終極武器是 Linux 網路排障那一套(ip route、tcpdump、conntrack),kubectl 只能看到宣告層。

**遷移題**:「家裡的路由器讓十台裝置共用一個對外 IP,跟 Pod 出 cluster 的 MASQUERADE 是不是同一件事?你家路由器的 conntrack 滿了會有什麼症狀?」(答:一模一樣,NAT + 連線表;症狀也一樣,新連線開不了、已開的照用。BT 下載器開太多連線把家用路由器打掛,就是 conntrack table full 的居家版。)

### 誘答彈藥(挑 1-2 題)

1. 「跨 node 的 Pod 通訊,封包要經過 control plane 轉發,因為叢集狀態在那裡。」(錯:control plane 只管宣告與規則下發,data plane 是純 kernel 路由,API Server 掛了現有流量照跑。打 control/data plane 層級混淆。)
2. 「Pod 連外部 API,對方 log 看到的來源 IP 是 Pod IP。」(kind/多數自建:錯,MASQUERADE 換成 node IP。伏筆:C-5 的 EKS VPC CNI 裡這句反而常是對的,同一題兩個答案,磨「先問環境再下結論」。)
3. 「conntrack 滿了,重啟 kube-proxy 清一清就好。」(錯兩層:conntrack 是 kernel 表跟 kube-proxy process 無關;而且就算清了,連線洩漏源還在,治標都算不上。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 生產叢集某台 node 上的 Pod 全部間歇性連線失敗,其他 node 正常 |
| **生產怎麼做** | 先分層:DNS 解得開嗎(解析層)→ 同 node Pod 互 curl 通嗎(本機 veth/bridge)→ 跨 node 通嗎(路由/overlay)→ 出 cluster 通嗎(SNAT)。一層層夾出死在哪站 |
| **真實踩坑** | 換了 CNI 或調了 VXLAN 之後 MTU 沒扣封裝 header,小封包全通、大封包全掛(SSL handshake 過、傳大 payload 卡死)。症狀詭異到像玄學,根因是 overlay 多包一層的那幾十 bytes。查法:`ip link` 看 MTU、ping 帶 `-s 1450 -M do` 測分段 |
| **面試怎麼問** | 「兩個 Pod 在不同 node,封包怎麼過去的?overlay 跟直接路由差在哪、各付什麼代價?Pod 出 cluster 時 source IP 是什麼?」 |

### 術語卡(Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| veth pair | /viː eθ peər/ | A virtual cable with two ends: one inside the Pod's netns, one on the node | 一條虛擬網線的兩頭,Pod 的 eth0 就是其中一頭 |
| VXLAN | /viː eks læn/ | An overlay protocol that wraps L2 frames inside UDP packets between nodes | 封包裡再包封包,讓 Pod 網段跑在不配合的實體網路上 |
| MASQUERADE | /ˌmæs.kəˈreɪd/ | Dynamic source NAT that rewrites outgoing packets to use the node's IP | 出門前把 src 從 Pod IP 換成 node IP,回程靠 conntrack 換回來 |

---

## C-5 選配: EKS VPC CNI 對照(公司 prod 對接)

> 選配,concept 對照為主。學員公司 prod 是 EKS billing 平台,這節讓 kind 所學直接翻譯成他天天面對的環境。

同一紙 CNI 合約,AWS 的履約方式完全不同:

| 面向 | kind(kindnet/Calico) | EKS(VPC CNI) |
|------|----------------------|---------------|
| Pod IP 來源 | 叢集私有網段(node 外不可達) | **直接從 VPC subnet 拿真 IP**(掛在 node ENI 的 secondary IP) |
| 跨 node | 直接路由或 overlay | 不需要:VPC 路由天生認得 Pod IP,無 overlay、無封裝稅 |
| Pod 連外的 src IP | MASQUERADE 成 node IP | VPC 內看到的就是 Pod IP(出 VPC 才 SNAT/NAT GW) |
| Pod 密度上限 | 幾乎只受資源限制 | **受 instance type 的 ENI 數 × 每 ENI IP 數限制**(例 m5.large 約 29 個 Pod;prefix delegation 可放寬) |
| NetworkPolicy | 看 CNI(kindnet 不支援) | VPC CNI 近版原生支援(舊叢集常另裝 Calico) |
| Ingress 引擎 | ingress-nginx | AWS Load Balancer Controller:Ingress → ALB,target-type ip 直接把 Pod ENI IP 註冊進 target group |

面試高頻陷阱:「EKS node 明明還有 CPU/memory,Pod 卻 Pending」,根因常是 ENI/IP 額度吃滿,scheduler 的 filter 卡在 node 的 pods allocatable 上限。這把 C-4(IP 從哪來)跟 P0(scheduler filter)接在一起。

**選配 EKS lab**:terraform 只產生、由學員親手執行;命名一律 `billing-dev-eks-*`;結束必跑 `terraform destroy` 並用 `aws eks list-clusters` 驗證清乾淨。`[RUNTIME: 是否開這個 lab 依學員時間與 AWS 帳單意願,concept 對照講完就有 80% 價值]`

---

## P2a 迷你 mock(30 分鐘,phase 收尾用)

**形式**:全程學員講、coach 只追問。20 分鐘技術 + 5 分鐘 English 輕推 + 5 分鐘回饋。從題目池挑 2 大題 + 1 快問,`[RUNTIME: 依 mistake-registry 挑他最弱的組合]`。

**題目池**:

| # | 題目 | 判定要點 |
|---|------|---------|
| 1 | 白板:Pod A curl backend-svc(跨 node),封包全旅程 | 七站不漏(骨架默數);DNS 層與 NAT 層分開;回程 conntrack 主動講;「封包去 ClusterIP」誤解不得復發 |
| 2 | 為什麼會有 Ingress?從 NodePort 一路推 | 三痛點 → LB 成本 + L4 限制 → 省 LB + L7;「規則 vs 引擎」模式主動出現 |
| 3 | 排障:curl 走 Ingress 拿 404;換個情境拿 502 | 先分層(規則層 vs 後端層)再動手;404 先查 host/path/class,502 先查 endpoints/port;不准先跳 restart |
| 4 | 上了 default-deny 之後全 ns 的 app 報 could not resolve host | 秒定位 DNS egress;講出「CoreDNS 本身沒事,別重啟」;主動補治標(開 53)與治本(default-deny 標配含 DNS 洞) |
| 5 | conntrack table full:症狀、查法、治標治本 | 新連線 vs 舊連線精準;count/max/dmesg 三查法;主動分治標治本 |
| 6 | kube-proxy 掛掉 vs CoreDNS 掛掉,各影響什麼? | 規則已在 kernel(現有流量照跑)vs 新解析全死;層級各自講對 |
| 7 | (English, 輕推)Explain in English: what does an Ingress controller do? | 講出 watch / render config / reload 任兩個即可,給 English Polish 不扣分 |

**判定**:2 大題全過 + 快問過 = mock PASS。任何一題暴露的洞,進 mistake-registry 排 gate 前重測。

---

## Chaos Drill Hooks (P2a)

> 完整劇本歸 `references/chaos-drills.md`(P2a 段待填,用以下 ID 對接)。E 段限時 debug 用,一次一個。

| Drill ID | 一句話場景 | 對接 chunk |
|----------|-----------|-----------|
| P2a-1 | CoreDNS 副本清零,服務名全滅,考解析層定位 | C-1 |
| P2a-2 | 清空 node 上的 KUBE- 鏈,Service 不通但 Pod IP 直連通,考 NAT 層定位 | C-1/C-4 |
| P2a-3 | NetworkPolicy 誤封(selector 打錯字),單一服務被隔離,考白名單語義 | C-3 |
| P2a-4 | Ingress 404(ingressClassName 沒人認領或 path 語義錯),考規則層 vs 後端層 | C-2 |
| P2a-5 | conntrack 壓滿(調小 nf_conntrack_max + 連線風暴),考新舊連線症狀與水位查法 | C-1/C-4 |

---

## P2a 畢業 Gate

**條件**:不看筆記,白板走完封包全旅程,並當場處理一個變體追問。

**考核格式**:「Pod A 在 node1 執行 `curl http://backend-svc/api`,backend 在 node2。從敲下 Enter 到收到 response,把每一站畫出來講清楚:誰解析、誰改寫、誰放行、封包怎麼過機器、回程怎麼對上號。」接著抽一個變體:同 node / 南北向(經 Ingress)/ 出 cluster / conntrack 滿了怎麼查。

**Pass 條件**:

- 七站骨架完整,不漏中間棒次(特別是第 4 站防火牆與第 7 站回程,學員的歷史漏點模式)
- DNS 解析層、NAT 連線層、過濾層、路由層分得乾淨,不互相污染(他的層級混淆弱點,gate 必驗)
- 每一站講得出「誰做的」:CoreDNS / kube-proxy 寫規則 kernel 執行 / CNI / conntrack
- 「規則=資料 vs Controller=引擎」模式能套到 Service、Ingress、NetworkPolicy 三者
- conntrack 滿了:症狀精準(新 drop 舊照常)+ 三查法 + 主動講治標治本
- 誘答抽一題(從 C-2/C-3/C-4 彈藥庫選未用過的),要抓出錯並講清楚為什麼錯

**Stretch(加分,不強求)**:

- 講出 overlay 的 MTU 代價與症狀(小包通大包掛)
- EKS VPC CNI 對照:同一題「Pod 連外 src IP 是什麼」在兩個環境的不同答案
- iptables 模式在幾千 Service 時的線性掃描問題,IPVS/eBPF 是什麼思路(點到即可,P5 展開)

**Gate 失敗處理**:見 SKILL.md Phase Gate Failure 協議。依死在哪一站對症回 C-2/C-3/C-4 重練,進 mistake-registry 排冷測,不硬闖。

---

## Portfolio 整合(P2a)

過價值門檻才進 repo(見 memory k8s-portfolio-value-gate),太基礎的留本機筆記:

- `portfolio/notes/p2a-packet-journey.md`:學員親手畫的七站全旅程圖 + 每站註解 + 變體(南北向/出 cluster)。這是 P2a 的核心 artifact,面試白板題的底稿,值得 commit。
- `portfolio/manifests/ingress-demo/`:兩後端 + Ingress 規則 + 404/502/503 排障筆記(具體症狀對根因,不是教學搬運)。
- `portfolio/manifests/netpol-demo/`:default-deny + DNS 洞 + 業務洞的完整組合,附「kindnet 靜默無效」的踩坑記錄。
- 不進 repo:ingress-nginx/Calico 的安裝指令(工具操作,無面試價值)、單純抄教材的對照表。

---

## P2a 英文 Ramp

> P2a 檔位:中文為主,術語卡 + 每個機制一兩句英文短句(Say-it-in-English 驗收用)。
> 學員 session 11 明說要中文佔比多:輕推不硬逼,他用英文作答時給 English Polish。

**本 phase 術語卡**(同步進 term-registry.md 做間隔抽考):

| Chunk | 術語 |
|-------|------|
| C-1(已建卡) | DNAT, kube-proxy, conntrack, Ingress Controller |
| C-2 | reverse proxy, TLS termination |
| C-3 | default deny, east-west traffic |
| C-4 | veth pair, VXLAN, MASQUERADE |

**Say-it-in-English 短句庫**(每機制一到兩句,驗收時抽念 + 自己重講一遍):

- Service: "A Service gives a stable virtual IP; kube-proxy programs iptables rules so the kernel rewrites the destination to a real Pod IP on the source node."
- Ingress: "An Ingress is just data; the Ingress controller watches it and renders the rules into nginx config, routing by host and path at layer 7."
- 404 vs 502: "A 404 means my routing rule didn't match; a 502 means the rule matched but the backend connection failed."
- NetworkPolicy: "Network policies are allow-lists enforced by the CNI plugin; without a supporting CNI they silently do nothing."
- default deny: "We start from default deny and open explicit holes, including DNS egress to CoreDNS."
- Packet path: "Cross-node Pod traffic is plain Linux networking: veth pairs, route tables, and either direct routing or an overlay like VXLAN."
- SNAT: "When a Pod leaves the cluster, the node masquerades the source IP, and conntrack rewrites the reply on the way back."
- conntrack full: "When the conntrack table is full, existing connections keep working but new ones get dropped."

`[RUNTIME: 短句抽哪幾句依當週術語卡到期排程;他若主動全英文作答,給 English Polish 後順勢多推一句,不硬逼]`
