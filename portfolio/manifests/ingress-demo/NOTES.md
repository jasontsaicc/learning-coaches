# ingress-demo: Ingress host/path 路由 + 排障筆記

兩個 http-echo 後端(shop-api / shop-web),一條 Ingress 按 path 分流(`shop.com/api`→shop-api、`shop.com/web`→shop-web),引擎 ingress-nginx。

## 檔案
- `backends.yaml` — 兩個 Deployment(replicas 2)+ ClusterIP Service(port 80 → targetPort 5678)
- `ingress.yaml` — Ingress 物件,`ingressClassName: nginx`,兩條 Prefix path

## 建置關鍵步驟
1. `kubectl apply -f backends.yaml`;`get endpoints` 確認每個 Service 掛 2 個 Pod IP。
2. `kubectl apply -f ingress.yaml`(裝 controller 前):`get ingress` 的 ADDRESS 空、`describe` Events `<none>` = 規則進 etcd 但沒引擎執行。
3. 裝 ingress-nginx controller(kind provider deploy.yaml)→ controller Pod 卡 `Pending`。
4. 根因:controller 有 `Node-Selectors: ingress-ready=true`,沒 node 貼 → scheduler filter 全刷掉。`kubectl label node <worker> ingress-ready=true` → 自動排上、Running(改 desired state,不用 delete pod)。
5. `grep -c shop /etc/nginx/nginx.conf`(controller Pod 內)> 0 = 規則已 render 成 nginx.conf。

## 踩坑 → 根因

### YAML schema:client dry-run 給假安心
- `backend.service` 寫成字串(`service: shop-api`)→ decode 失敗,該是 object `service: {name, port}`。
- `pathType: prefix` 小寫 → enum 只收 `Exact`/`Prefix`/`ImplementationSpecific`(大小寫敏感)。
- `--dry-run=client` **回 created**、`--dry-run=server` 才擋。**驗 k8s YAML 一律 server 端**;讀 `ValidationError(...路徑...)` 括號路徑直指錯的欄位。

### 404 排障:兇手是 port-forward,不是規則
curl 走 Ingress 拿 404(甚至先回空白),差點去改 Ingress YAML。照階梯查:

| 查 | 結果 | 判定 |
|----|------|------|
| `get ingress` ADDRESS | `localhost` | 引擎已認領 ✅ |
| `get ingressclass` | `nginx` 存在 | class 對上 ✅ |
| `grep server_name shop` nginx.conf | 有 | 規則已 render ✅ |

規則層**全綠** → 真兇是**被 Ctrl-C 打斷的舊 port-forward 半死**回假 404。換乾淨 port-forward(不同 port）→ 全 200。

**教訓**:404 = 引擎回的「規則層沒對上」(host / path / ingressClass 認領);502/503 才是後端層。規則層全綠時,兇手在「你測試所經過的那層」——`kubectl port-forward` 是會抖的除錯夾具,不可信就換乾淨再下結論,別去改沒壞的規則。

## 待補(下次)
- 分流 body 確認、負向 case:不帶 Host header → 404(L7 靠 header 分流);`/apiv2` → 404(Prefix 是路徑段前綴,`apiv2` 第一段 ≠ `api`)。
- `scale deploy shop-api --replicas=0` → 503(Endpoints 空 = 後端層,對照 404 規則層)。
