# P2a 補充 - Gateway API(Ingress 的接班人)

> 2026-10-12 補。起因:ingress-nginx 已於 2026-03 退役(不再發版、不再出 security fix),Kubernetes 官方建議改用 Gateway API。

## 這是什麼?(一句話)

Gateway API 是一組 CRD(GatewayClass / Gateway / HTTPRoute ...),把 Ingress 一張紙拆成三張,分給三種角色各管各的;跟 Ingress 一樣,物件只是規則,要另外裝 controller(implementation)才會動。

## 跟你已經會的 Ingress 對照

你在 P2a chunk 2 證過的「物件 = 規則、controller = 引擎」完全沿用。變的是那張紙被拆開了:

```
Ingress(一張紙,所有人改同一張)          Gateway API(三張紙,三種角色)
┌──────────────────────────────┐          ┌───────────────────────────────┐
│ ingressClassName: nginx      │  ──────► │ GatewayClass   (infra 供應商) │ cluster-scoped
│                              │          │  "由哪個 controller 實作"     │
│ tls / 入口 port              │  ──────► │ Gateway        (platform/SRE) │ listener: port、protocol、TLS
│                              │          │  "門開在哪、收誰的 route"     │
│ rules: host + path → backend │  ──────► │ HTTPRoute      (app 團隊)     │ host / path / header 比對
│ annotations: 各家方言        │          │  "我的流量怎麼分"             │ backendRefs 可帶 weight
└──────────────────────────────┘          └───────────────────────────────┘
                                             跨 namespace 指 backend → 對方要給 ReferenceGrant
```

| 你在 Ingress 學到的 | Gateway API 的對應 |
|---|---|
| ADDRESS 空 = 沒 controller 認領 | Gateway / HTTPRoute 的 status conditions 沒有 `Accepted` / `Programmed` |
| L7 純字串比對 Host + path | HTTPRoute `matches`:hostname、path、header、query,規格內建 |
| 權重、header 路由要寫 nginx annotation | `backendRefs[].weight`、header match 進了標準規格,換 controller 不用改 |
| controller 不內建,要自己裝 | CRD 本身也不內建:先裝 Gateway API CRD,再裝 implementation |

## 踩過什麼雷?(預先列,還沒親手踩)

- 以為 Ingress API 被砍:退役的是 ingress-nginx 這個 controller 專案,Ingress 物件本身還在。
- 以為舊叢集馬上壞:既有部署照跑,風險是面向 internet 的元件從此沒 security patch。
- annotation 不會跟著搬:`nginx.ingress.kubernetes.io/*` 是方言,轉換工具 `ingress2gateway` 只能轉有標準對應的部分,其餘要人工對照。
- HTTPRoute apply 成功不等於生效(你的「成功訊息不保證做到」卡):要看 route 的 `status.parents` 有沒有被 Gateway `Accepted`、`ResolvedRefs` 是否為 True。

## AWS 上怎麼做

EKS 常見組合是 AWS Load Balancer Controller(Gateway → ALB/NLB)或 VPC Lattice 的 Gateway API controller。兩者對 Gateway API 各資源的支援度不同,選型時查當下版本的文件,不要憑記憶。

## 面試怎麼回答?

「ingress-nginx 退役後,我會把新入口放在 Gateway API。核心機制跟 Ingress 一樣是 controller reconcile 規則物件,差別是角色分離:platform 管 Gateway(port、TLS),app 團隊只能動自己的 HTTPRoute,跨 namespace 要 ReferenceGrant 授權。權重、header 路由進了標準規格,不再綁某家 controller 的 annotation。遷移我會先盤點 annotation 依賴,再用 ingress2gateway 轉、雙軌跑、切 DNS。」

來源:[Ingress NGINX Retirement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)、[Gateway API](https://gateway-api.sigs.k8s.io/)
