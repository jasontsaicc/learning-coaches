# P2a chunk 2 - Ingress (物件 vs 引擎 / L7 分流)

> session 12, 2026-07-03。D 段動手 lab 完成。

## 這是什麼?(一句話)

Ingress 物件是一張「寫著 host/path 導流規則的紙」,躺在 etcd 裡;真正讀這張紙、動手把 HTTP 流量按規則轉去不同後端的,是另外一個要你自己裝的程式 = Ingress Controller(這裡用 ingress-nginx)。

## 用什麼比喻理解?

佈告欄上的紙條 vs 接待員:

- 紙條(Ingress 物件)寫著「shop.com/api 的客人帶去 A 櫃檯,其他人帶去 B 櫃檯」。釘上去那一刻什麼都沒發生,紙不會自己動。
- 接待員(Controller = nginx Pod)站門口讀紙條、動手帶路。沒接待員,紙條就是廢紙。

這不是 Ingress 特有,是整個 k8s 的運作方式:每個物件都是死的 desired state,背後都要一個活的 controller 在 watch 它、reconcile 現實。Deployment 也是這樣,只是它的 controller 內建(kube-controller-manager 開機就跑),所以你從沒看過「沒引擎」的樣子。Ingress 的 controller 不內建、要自己裝,才第一次親眼看到「物件孤零零躺著、沒引擎」的中間狀態。

## Lab 親眼證的三件事

1. 物件 = 規則(資料):apply Ingress 但沒裝 controller → `kubectl get ingress` 的 ADDRESS 空、curl 不通。
2. Controller = 引擎:裝 ingress-nginx 後 → 它 watch 到 shop-ingress、開始按規則轉,curl 通。
3. L7 分流靠 Host + path 字串:同一個 ClusterIP、同一個 controller,只換 HTTP 的 `Host` header:
   - `Host: shop.com` + `/`    -> shop-web  ("I am the WEB homepage")
   - `Host: shop.com` + `/api` -> shop-api  ("I am the API backend")
   - 不帶 Host / 帶 `nope.com` -> HTTP 404
   最後兩個 404 證明 nginx 純粹拿 Host 字串比對規則表,不做 DNS、不 care 這個 domain 真不真實。

## 封包全鏈路(curl -> 後端 Pod)

```
curl -H "Host: shop.com" http://<controller-svc-dns>/api
  1) CoreDNS 把 svc 名字解析成 controller 的 ClusterIP
  2) kube-proxy 的 iptables 在本機 DNAT，ClusterIP -> controller Pod IP   <- chunk-1 那台機器
  3) nginx 讀 HTTP: Host=shop.com, path=/api -> 查規則表 -> 該給 shop-api
  4) nginx 直接連 shop-api 的 Pod IP (watch EndpointSlice)，這一跳繞過 backend Service / kube-proxy
```

分界:kube-proxy 管「怎麼到達一個 Service」(L4，ClusterIP/NodePort -> Pod IP 的 DNAT);ingress controller 管「到了之後按 HTTP 內容轉哪」(L7，Host + path)。兩者上下游、不是替代。controller 本身也是被 Service 對外暴露的,所以它反而是 kube-proxy 的客戶。

## 踩過什麼雷?

1. `--dry-run=client` 綠燈騙人:手打 YAML 有 `numer`(拼錯 number)、`pathType: prefix`(小寫)、欄位少縮一層,client dry-run 全放行印 `created`,實際 apply 失敗、`get ingress` 空的。client 只驗本地結構,strict decoding(unknown field 藏寶圖)在 server 端。擋 typo 要用 `--dry-run=server`。
2. `port` vs `targetPort`:兩個都是合法數字,schema 不擋。少寫 targetPort(預設=port=80,但 http-echo 聽 5678)或打錯數字 -> apply 成功但 curl connection refused。port=Service 門牌,targetPort=真正轉進 container 的 port。
3. LoadBalancer 型 Service 在 kind:EXTERNAL-IP 永遠 `<pending>`(沒有雲端 provisioner),所以 Ingress ADDRESS 一直空。不是壞掉,是環境限制。功能對不對看 curl,不看 ADDRESS。

## 面試怎麼回答?

- Q「有了 Ingress 還需要 Service 嗎?」需要。Ingress 規則的後端指的就是 Service,controller 自己也用 Service 對外暴露。
- Q「apply 一個 Ingress 物件,流量就會分流嗎?」不會。物件只是 etcd 裡的規則,要有 Ingress Controller(nginx/traefik 這種 Pod)在 watch 並實作 L7 routing 才會動。這是 k8s「物件=desired state / controller=reconcile 引擎」通用模型的一個特別直觀的例子,因為 Ingress controller 不內建、要自己裝。
- Q「裝了 Ingress,kube-proxy 還有用嗎?」有。要先進得了 controller,靠的是它自己的 Service(ClusterIP/NodePort),那是 kube-proxy 的 DNAT。只有 nginx->後端那一跳直連 Pod IP 繞過 kube-proxy。

## lab 檔

- `portfolio/manifests/ingress-lab/shop-backends.yaml` (兩個 http-echo 後端 + Service)
- `portfolio/manifests/ingress-lab/shop-ingress.yaml` (host shop.com, /->web /api->api)
