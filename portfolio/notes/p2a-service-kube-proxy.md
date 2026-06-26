# P2a chunk 1：Service / kube-proxy / DNAT(第一性原理)

> 進度:謎題 A ✅、謎題 B(DNAT/去中心化)概念已建但 Gate 未確認;conntrack、CoreDNS、動手 lab 待續。

## 為什麼需要 Service

Pod IP 是**短命的(ephemeral)**:reconcile 補新 Pod、滾動更新、節點掛掉重排 → IP 都會變。前端把 Pod IP **寫死必爆**。
解法:中間加一層**穩定的地址**,前端只認它,它指向後面變動的 Pod。這層就是 **Service**,固定地址叫 **ClusterIP**。

## 謎題 A：Service 怎麼知道後面有哪些健康 Pod

```
Service (selector: app=backend)
    │  一個 controller 跑 reconcile loop:
    │  盯「label 對得上 ✚ readiness 通過」的 Pod
    ▼
Endpoints / EndpointSlice   ← 健康 Pod 的 IP 清單(即時增減)
    │
    ▼
Pod  Pod  Pod   (真正幹活,IP 會變)
```

- Service 用 **label selector** 框 Pod(跟 Deployment 的 `matchLabels` 同一招)。
- **Endpoints / EndpointSlice** = 裝「目前健康可收流量的 Pod IP」的物件(`kubectl get endpoints`)。EndpointSlice 是現代版,把大清單切片以利大規模。
- 維護者是一個 controller 跑 **reconcile loop**,readiness probe 當閘門。
- **回扣 P1**:`rm /tmp/ready` → readiness 失敗 → controller 把該 Pod IP **從 Endpoints 撤掉** → 流量不進去,但 `RESTARTS` 0、仍 `Running`。當時看到的「endpoint 消失」就是這個。

## 謎題 B：ClusterIP 是虛擬的,封包怎麼真的到 Pod

**反直覺事實**:ClusterIP **沒綁在任何一張網卡上**,沒有任何機器「擁有」它。

- 若它是「一張虛擬網卡綁在 node-1」→ 所有流量先繞 node-1 = **瓶頸 + 單點故障**。所以 k8s 不這樣做。
- 真相:**kube-proxy 每台 node 都跑一隻**(DaemonSet),在**每台 node 的 kernel 寫 iptables 規則**:
  > 目的地 = ClusterIP 的封包 → 把目的地**改寫**成 Endpoints 裡某個真實 Pod IP。
- 這個改寫動作 = **DNAT(Destination NAT)**,在**封包出發的那台 node 本地**就做掉,不繞中央 → **去中心化、無瓶頸**。
- ClusterIP 不是「一個地方」,只是「每台 node 上都有的一條比對樣板」,哪都不在又無所不在。

```
前端 Pod (node-2) --目的地 ClusterIP 10.96.0.5-->
   │  node-2 本地 kernel iptables 規則攔截
   ▼  DNAT 改寫 → 10.244.2.7 (某真實 Pod IP,從 Endpoints 挑)
真實 Pod (可能在任何 node)
```

### 電話代表號比喻

| 電話 | k8s |
|------|-----|
| 公司代表號(對外不變) | ClusterIP |
| 員工分機(會異動) | 真實 Pod IP |
| 每支話機內建的自動轉接表 | kube-proxy 寫的 iptables 規則 |
| 撥代表號→話機當場轉接 | DNAT(本地改寫目的地) |
| 一個總機小姐坐中央轉接(會塞、會單點) | 舊式中央 LB = 瓶頸 |

k8s 把「轉接能力」複製進**每支話機**,各轉各的,不經中央。

## 易混淆

- **CNI ≠ kube-proxy**:CNI 給每個 Pod 一個**真實 IP**、讓 Pod 互通(pod network 底層);ClusterIP 的轉發是 **kube-proxy** 做的,兩回事。
- kube-proxy 是**寫規則**的人,不是**過流量**的人(流量走 kernel 的 iptables,不經 kube-proxy 進程)。

## 術語

| EN | 中文點破 |
|----|---------|
| DNAT | 改寫封包目的地 IP;ClusterIP→真實 Pod IP 的底層動作 |
| kube-proxy | 每 node 一隻,寫 iptables/ipvs 規則實作 ClusterIP 轉發,去中心化 |

## 待續

- **conntrack**:NAT 改了目的地,回程封包要能改回來 → kernel 需記住每條連線狀態。遷移題:conntrack table 滿了會怎樣?怎麼查?
- **CoreDNS**:service name → ClusterIP 的解析。
- **動手 lab**:apply backend Deployment + Service,`get svc`/`get endpoints`,scale 看 Endpoints 增減,`iptables-save | grep <clusterip>` 看 DNAT 規則。
