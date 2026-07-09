# P2a chunk 1：Service / kube-proxy / CoreDNS(第一性原理 + 動手實證)

> 進度:**chunk 1 全畢業 ✅**(2026-06-28)。謎題 A/B/C + CoreDNS 全通,D 段 lab 在真叢集追完整 iptables 鏈、F 段無鷹架全鏈 teach-back 過。

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

## 謎題 C：conntrack(NAT 的記憶體)

去程 DNAT 把目的地 `ClusterIP → Pod-A IP` 改掉了。回程 Pod-A 回封包,來源是 Pod-A 真實 IP,但 client 當初是跟 ClusterIP 講話,收到陌生 IP 的回包會丟掉。
解法:kernel 在去程改寫時,把這條連線的對應記進 **conntrack table**;回程查表,反向把來源改回 ClusterIP,client 才認得。

- conntrack / iptables 都屬 **Linux kernel netfilter**,是 **node 層狀態,不是 k8s 物件**。`kubectl` 永遠看不到(沒有 `kubectl get conntrack`)。
- **table 滿了的症狀**:沒空間記新連線 → **新連線被 drop、舊連線不受影響**(間歇性 timeout、服務「偶爾連不上」,高 QPS/短連線最容易中)。
- **查法**(登進 node 用 Linux 工具):
  ```
  conntrack -C                                      # 目前筆數
  cat /proc/sys/net/netfilter/nf_conntrack_count    # 目前用量
  cat /proc/sys/net/netfilter/nf_conntrack_max      # 上限
  dmesg | grep -i conntrack                          # 滿了會印 "table full, dropping packet"
  ```
  治本:調大 `net.netfilter.nf_conntrack_max`,或減少短連線/用連線池。

## CoreDNS:名字 → ClusterIP

app 寫的是名字 `backend`,但 iptables 只認 IP。中間翻譯的就是 **CoreDNS**(叢集內建 DNS server,本身就是 kube-system 裡的幾個 Pod,透過 `kube-dns` 這個 Service 的 ClusterIP `10.96.0.10` 被存取)。

```
backend  --(CoreDNS)-->  ClusterIP 10.96.254.186  --(iptables DNAT)-->  真實 Pod IP
         名字→ClusterIP                            ClusterIP→Pod IP(本機)
```

- 每個 Pod 的 `/etc/resolv.conf` 由 **kubelet** 在建 Pod 時寫好,`nameserver` 指向 CoreDNS 的 ClusterIP。**注意:寫 resolv.conf 的是 kubelet,不是 CoreDNS**(CoreDNS 只負責「回答」)。
- 遞迴有趣點:連「查 DNS」本身都騎在同一套 Service + iptables DNAT 機制上。
- **跨 namespace** 要寫 FQDN:`service.namespace.svc.cluster.local`。

## 動手 lab 實證(kind 3 節點)

```
# 1. 安全鐵律: 確認打本地 kind 不是 prod
kubectl config current-context        # kind-k8s-coach-p0

# 2. apply backend(Deployment replicas=2 + ClusterIP Service)後驗證
kubectl get svc backend               # CLUSTER-IP 10.96.254.186 (虛擬, 屬 Service CIDR 10.96/12)
kubectl get endpoints backend         # 10.244.1.2:80,10.244.2.2:80 (2 個真 Pod IP, 屬 Pod CIDR 10.244/16)
kubectl get pods -l app=backend -o wide  # 對照: endpoints 2 IP = 這 2 隻 Pod 的 IP, 分屬 worker / worker2

# 3. 重頭戲: 進 node 本機追 iptables DNAT 鏈(kind node = docker 容器)
docker exec k8s-coach-p0-worker  iptables-save -t nat | grep 10.96.254.186
docker exec k8s-coach-p0-worker2 iptables-save -t nat | grep 10.96.254.186   # 兩台規則一致 = 去中心化
```

追到的完整鏈(白紙黑字):
```
KUBE-SERVICES  -d 10.96.254.186 --dport 80   -j KUBE-SVC-xxx     # 目的地是 ClusterIP → 跳此 Service 部門
KUBE-SVC-xxx   -m statistic --mode random --probability 0.5 -j KUBE-SEP-A   # 擲骰子 50% 挑分機 A
KUBE-SVC-xxx                                              -j KUBE-SEP-B   # fallback 接剩下 50%
KUBE-SEP-A     -j DNAT --to-destination 10.244.1.2:80     # ← 真正改寫目的地成 Pod IP 的那一刀
```
**鐵證**:ClusterIP 只是規則裡的比對字串,封包從不「拜訪」它;改寫(DNAT)發生在**出發地本機 kernel**。負載均衡是 **iptables 機率隨機**(2 後端→1/2 + fallback;N 後端→1/N、1/(N-1)…均分),不是聰明 LB(要聰明得換 IPVS 或上 L7)。

## 踩過的雷(D 段現場)

1. **busybox nslookup 被工具自己的 bug 騙**:`nslookup backend` 回 NXDOMAIN 差點以為 CoreDNS 壞,但 `nslookup backend.default.svc.cluster.local`(FQDN)立刻成功。根因是 busybox(musl)處理 `search` 清單不可靠,漏試 `default.svc.cluster.local`;glibc 真實 app 不會中。**教訓:DNS 失敗第一刀先用 FQDN 二分「伺服器壞 vs 發問端壞」**;測叢集 DNS 用 `nicolaka/netshoot`,別用 busybox。**絕不因 nslookup 失敗就亂砍 CoreDNS。**
2. **`options ndots:5` + 主機 search 網域漏進 Pod**:短名字(點<5)會把整串 search 網域一條條試過才放棄 → 高 QPS 變 DNS 延遲坑;主機的 `*.oraclevcn.com`/`*.ts.net` 漏進 Pod resolv.conf,沒中的查詢多繞外部 DNS。
3. **YAML 大小寫敏感**:Service `apiVersion: V1`(大寫 V)會被 API Server 退件,正解小寫 `v1`。

## 面試怎麼回答

**Q:一個 Pod 用名字連 `backend`,封包怎麼到後端 Pod?**
1. app 做 DNS 查詢,resolv.conf(kubelet 寫的)指向 CoreDNS ClusterIP。
2. CoreDNS 回 `backend` 的 ClusterIP。
3. 封包對 ClusterIP 送出,**還在本機 node kernel** 就撞上 kube-proxy 寫的 iptables 規則。
4. 規則機率挑一個 Endpoints 裡的健康 Pod,`DNAT` 改寫目的地成真實 Pod IP。
5. 封包經 CNI Pod 網路送達(可能在別台 node)。
6. (加分)conntrack 記住此次改寫,回程自動反向還原成 ClusterIP。

**Q:Service 背後有沒有一隻 process 在轉流量?** 沒有(iptables 模式)。Service = 散在每台 node iptables 裡的一堆規則,kube-proxy 只負責寫規則,流量走 kernel。
**Q:Service 怎麼做負載均衡?** iptables 機率隨機分流,各 endpoint 均分;要最少連線數那種智慧 LB 得換 IPVS 或上 L7。
**Q:CoreDNS 掛了會怎樣?** 全叢集名字解析失敗(connect by name 全爆),所以預設多副本 + 用 Service 做高可用。
