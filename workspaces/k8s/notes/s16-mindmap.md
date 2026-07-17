# s16 思維導圖(2026-07-17)白板默畫用

兩根脊椎撐起今天全部內容。先默畫脊椎,再往下長枝。

---

## 脊椎 1:規則 vs 引擎(同一個模式,第四次出現)

```
        規則(宣告,躺在 etcd)        引擎(執行者)              引擎的產出
        ─────────────────────       ──────────────           ──────────────
   1.   Service                 →   kube-proxy           →   iptables DNAT 規則
   2.   type: LoadBalancer      →   cloud controller     →   雲上的 LB
   3.   Ingress                 →   Ingress controller   →   nginx.conf
   4.   NetworkPolicy           →   CNI (Calico felix)   →   node iptables/eBPF
                                    ▲ 今天新增
```

**沒引擎會怎樣 = 這張表的殺手級推論**

```
   Ingress 沒 controller    →  功能不通,ADDRESS 空   →  【吵】馬上發現
   NetworkPolicy 沒 CNI 支援 →  安全假象,以為擋了其實全通 →  【安靜】可能永遠不知道
                                                            ▲ 最危險的一個
```

- `kubectl get netpol` 看到的是 **etcd 裡的規則**,證明不了 **kernel 裡有沒有引擎**
- kind 預設的 **kindnet 不實作 NetworkPolicy**:apply 成功、物件在、零報錯、**完全無效**
- 驗證的唯一方法:**不要看,去測** —— 起一個不該通的 Pod,curl 它

---

## 脊椎 2:分層 —— 「誰在說話?」

同一個問句,今天用了三次。

### 2-1 Ingress 回應碼(chunk 2 收尾實證)

```
   curl -H "Host: shop.com" /api   →  503   規則層接住了,但 Endpoints 空 → 【後端層】在說話
   curl -H "Host: shop.com" /web   →  200   兩層都活著
   curl (不帶 Host) /api           →  404   沒有規則接得住 → 【規則層】在說話
```

**503 vs 404 差在「規則層有沒有接住」,跟後端死沒死無關。**
prod 看到 503 的第一秒:規則沒問題,去看 Endpoints。

### 2-2 default-deny 之後的 curl(chunk 3 實證)

```
   curl http://db                  →  curl: (28) Resolving timed out    → 死在【DNS 層】
   curl http://192.168.46.66:5678  →  curl: (28) Connection timed out   → 死在【連線層】
                ▲ 餵 IP = 跳過 DNS,才走得到第二步
```

`curl http://db` 有先後兩步:
1. 問 CoreDNS「db 是誰?」→ 需要 egress **UDP/TCP 53**
2. 建 TCP 連線

default-deny 鎖 egress **連 53 一起鎖** → 死在第 1 步,**第 2 步沒機會發生**。

**prod 陷阱**:app log 噴 `could not resolve host` → 全隊衝去查 CoreDNS → **CoreDNS 好好的**,
是 policy 封了「去問路的那條路」。**故 default-deny 的第一個洞永遠是 DNS。**

### 2-3 L4 vs L7(唯一判準)

```
   判準只有一句:【轉發(或阻擋)的決定,需不需要讀 HTTP 內容?】

        需要讀  →  拆信  →  L7  →  ALB (Application LB)  →  Host / path / TLS
        不用讀  →  只看信封 →  L4  →  NLB (Network LB)     →  IP / port / 快

   兩個自我檢查:
   ① 「fast」就是證明:快 = 做的事少 = 讀得淺 = 層數低 = L4
   ② AWS 把層數寫在名字裡:【A】LB = 【A】pplication = 應用層 = L7
```

**NetworkPolicy = L3/L4** → 擋不了 `/admin`。證據是欄位清單(見下)。

---

## 枝 A:NetworkPolicy 本體

```
   出廠預設 = 【全通】
      任何 Pod → 任何 Pod,跨 namespace 也一樣
      ⚠ namespace 是【資料夾,不是牆】(P1 已釘:k8s namespace 不做網路隔離)
      實證:一個沒 label、沒身分的 tmp Pod,一行指令直接讀到 db

   NetworkPolicy = 白名單宣告 + 【翻轉】
      一旦有任何 policy 選中某 Pod → 該 Pod 在該方向從全通【翻轉】成 default-deny
      不是「加一條擋掉 X」,是「加一條放行 X,順便擋掉全世界」

   default-deny 起手式(生產標準,八行)
      podSelector: {}              ← 空的 = 選中 ns 內所有 Pod
      policyTypes: [Ingress, Egress]
      (一條 rule 都不寫)            ← 空白名單 = 誰都不放行
      → 再逐條開洞,第一條永遠是 DNS
```

**能寫的欄位,全部就這些(這張清單就是 L3/L4 的證明)**

```
   from / to:
     - podSelector        { matchLabels }     標籤
     - namespaceSelector  { matchLabels }     標籤
     - ipBlock            { cidr, except }    IP 網段
     ports:
     - protocol / port                        協定 + port 號碼

   清單到此為止。沒有 path、沒有 Host、沒有任何 HTTP 東西
   → 因為它【從來沒有拆過信】
```

---

## 枝 B:conntrack / DNAT(A 段複習,已封印推 +7)

```
   封包的信封上【只有兩個欄位】:來源 | 目的地   ← 答案空間只有 2 個選項

   去程   web Pod(10.244.1.5) → ClusterIP(10.96.100.231)
          ClusterIP 是【假的,全叢集沒人擁有它】 → 【非改不可】
          → 改【目的地】,換成真 Pod IP (DNAT)
          來源是真的、能用 → 【不用改】(注意:不是「不能改」,SNAT 場景真的會改,P3 再碰)

   回程   api Pod(10.244.2.7) → web Pod
          web 當初打的是 10.96.100.231,收到陌生 IP 回話會【丟掉】
          → 改【來源】,改回 ClusterIP

   分工句(尚未收,下堂補):
          kube-proxy【只寫規則】,kernel【搬封包】
          去程【查規則】(iptables),回程【查帳本】(conntrack)
```

---

## 枝 C:CNI 伏筆(chunk 4 從這裡開始)

關掉 CNI 的乾淨叢集長這樣 —— 這個畫面只有裝 CNI 前看得到:

```
   node × 3          NotReady    ← kubelet 回報 Ready 的條件之一 = 網路外掛就緒
   CoreDNS           Pending     ← 普通 Pod,需要 CNI 發 IP 才排得出去

   etcd              Running  ┐
   kube-apiserver    Running  ├─ hostNetwork:直接用 node 自己的網路
   kube-proxy        Running  ┘  【根本不需要 CNI 發 IP】

   → 誰需要 CNI、誰不需要,一眼分邊。這就是 CNI 合約的證據。
```

---

## 默畫檢查表(白板練習目標)

蓋住上面,白板上默畫出這些才算過:

- [ ] 四個引擎的表(規則 / 引擎 / 產出,三欄全填)
- [ ] 「沒引擎」兩種後果:誰吵、誰安靜、哪個危險、為什麼
- [ ] 503 / 404 / 200 各是誰在說話
- [ ] `Resolving timed out` vs `Connection timed out` 差在哪一步
- [ ] L4/L7 判準那一句 + ALB/NLB 對應(不准查)
- [ ] default-deny 八行 YAML(不准看檔)
- [ ] `from` 底下能寫的四種欄位 → 推出「為什麼擋不了 /admin」
- [ ] 封包兩個欄位 → 去程改什麼、回程改什麼、為什麼是那個
- [ ] 無 CNI 叢集:誰死誰活、為什麼

**卡住的項目直接記下來,下堂 Weekly Review 從那裡開始。**
