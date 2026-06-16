# 跨 Phase 底層基礎: Linux + 網路

> **如何使用此檔:** 這是跨所有 phase 的底層原理參考文件。教學引擎在遇到「前置知識有洞」(Feynman Gate 第 3 次 fail)時讀取對應章節補底。
> 每一節標示「首次出現 phase」;coach 只在到達該 phase 時才深入該節。
> P0-P1 相關內容已填完;P1+/P2a+ 章節為樁(stub),後續 phase plan 時補齊。

---

## 目錄

| 章節 | 首次出現 | 狀態 |
|------|---------|------|
| 1. 控制理論(reconcile 的根源) | P0 | 已填 |
| 2. Linux namespace + cgroup(容器的本質) | P0/P1 | 已填(P0 直覺) |
| 3. TCP 狀態機 | P2a | P2a 填 |
| 4. DNS 全解析 | P2a | P2a 填 |
| 5. Linux 性能排查(CPU/mem/IO/網路) | P3 | P3 填 |

---

## 1. 控制理論(reconcile 的根源)

> **首次出現: P0 C-0 / C-1**

### 核心概念

控制理論(Control Theory)是工程學的一個分支,研究如何讓系統自動維持在「目標狀態」。

最簡單的模型是「恆溫器」:

```
目標溫度(setpoint) = 26°C
         |
         v
+------------------+
|   Controller     |  <-- 比較目標 vs 現實
|  (恆溫器內部)    |
+------------------+
    |           ^
    v           |
  加熱/制冷   量測現在溫度
  (actuator)  (sensor / feedback)
```

三個核心元素:
1. **Setpoint (設定點)**: 你要的目標態,k8s 裡對應 `desired state`(存在 etcd)
2. **Sensor / Feedback**: 觀察現在真實狀態,k8s 裡對應 controller 的 watch + list
3. **Actuator**: 採取行動縮小誤差,k8s 裡對應 controller 的 reconcile action

### Level-Triggered vs Edge-Triggered

這個概念來自 OS/嵌入式系統的中斷設計,k8s 明確選擇了 level-triggered:

| | Edge-Triggered(邊緣觸發) | Level-Triggered(水位觸發) |
|-|--------------------------|---------------------------|
| **觸發時機** | 事件發生的「瞬間」才反應 | 只要「當前狀態 != 目標狀態」就持續反應 |
| **錯過事件怎麼辦** | 永遠錯過,無法補救 | 不存在「錯過」的概念:重讀狀態就好 |
| **controller 重啟** | 中間發生的事件永遠丟失 | 重啟後重新讀 etcd,照樣能修復偏差 |
| **k8s 選哪個** | 不選 | 選這個 |

**關鍵洞見**: k8s 的自癒能力(self-healing)直接來自 level-triggered 的選擇。controller 掛掉重啟不需要「重播歷史事件」,只需要「看現在的狀態」。

### 為什麼「宣告式」和控制理論天作之合

宣告式 API 讓你描述「setpoint」;control loop 讓系統持續向 setpoint 靠近。
這兩者缺一不可:光有宣告式沒有 control loop,狀態就會飄移;光有 control loop 沒有宣告式,系統不知道目標是什麼。

**遷移到其他系統的能力**: Prometheus 的 alerting(閾值 = setpoint,alert = actuator)、ArgoCD(Git 裡的 manifest = setpoint,sync = actuator)、Kubernetes HPA(target CPU% = setpoint,scale = actuator)都是同一個模式。

---

## 2. Linux namespace + cgroup(容器的本質)

> **首次出現: P0 C-5(直覺建立); P1 深入動手**

### 核心直覺: 容器 = process + namespace + cgroup

容器不是「輕量 VM」,而是「有特殊 Linux 屬性的普通 process」。

```
Linux kernel(所有容器共用同一個 kernel)
    |
    +-- process A (PID 1234)
    |   namespace: 只看到自己的 PID 空間、網路介面、掛載點
    |   cgroup:    限制上限 = 500m CPU, 256Mi memory
    |   (這就是「container A」)
    |
    +-- process B (PID 5678)
        namespace: 只看到自己的 PID 空間、網路介面、掛載點
        cgroup:    限制上限 = 1 CPU, 512Mi memory
        (這就是「container B」)
```

和 VM 的核心差異:

| | VM | Container |
|-|----|-----------|
| **kernel** | 每個 VM 有自己的 kernel | 共用 host kernel |
| **隔離機制** | 硬體虛擬化(hypervisor) | Linux namespace + cgroup(軟體) |
| **安全隔離強度** | 強(kernel 漏洞影響有限) | 弱(kernel 漏洞影響所有容器) |
| **啟動速度** | 慢(秒到分鐘) | 快(毫秒) |
| **資源佔用** | 重 | 輕 |

### Linux Namespaces(看得到什麼)

每種 namespace 隔離一種「視角」:

| Namespace 類型 | 隔離的資源 | k8s 中的對應 |
|---------------|-----------|-------------|
| `pid` | Process ID 空間 | container 內的 `ps` 只看到自己的 process |
| `net` | 網路介面、路由表、iptables | 每個 Pod 有自己的虛擬網路介面 |
| `mnt` | 掛載點(mount point) | container 有自己的 rootfs |
| `uts` | hostname + domainname | container 內 `hostname` 看到 Pod name |
| `ipc` | System V IPC、POSIX message queue | Pod 內多個 container 共用 IPC namespace |
| `user` | UID/GID 映射 | rootless container 的基礎 |

**重要**: 同一個 Pod 內的多個 container **共用 network namespace**,這就是為什麼同 Pod 的 container 可以用 `localhost` 互相溝通。

### cgroups(能用多少)

cgroups(Control Groups)讓 kernel 可以限制並追蹤一組 process 的資源使用:

| cgroup 子系統 | 控制什麼 | k8s 的對應 |
|-------------|---------|-----------|
| `cpu` | CPU 時間配額(CFS scheduler) | `resources.requests.cpu` + `limits.cpu` |
| `memory` | 記憶體上限 | `resources.requests.memory` + `limits.memory` |
| `blkio` | 磁碟 IO 速率 | (k8s 預設不設,P3 進階主題) |
| `pids` | 最大 process 數量 | `spec.securityContext` 的一部分 |

**k8s resource 和 cgroup 的映射**:

```
Pod spec:                          Linux cgroup:
  resources:
    requests:
      cpu: "500m"      ----------> cpu.shares (相對權重)
      memory: "256Mi"  ----------> (requests 不設 cgroup 上限,只影響調度)
    limits:
      cpu: "1000m"     ----------> cpu.cfs_quota_us (硬上限,超過被 throttle)
      memory: "512Mi"  ----------> memory.limit_in_bytes (超過觸發 OOM killer)
```

**OOM killer 的運作**:
當 container 的記憶體超過 `limits.memory`,kernel 的 OOM killer 會 kill 這個 container 內的 process。kubelet 偵測到 OOM exit,依 `restartPolicy` 決定是否重啟。這就是 `OOMKilled` 狀態的根源。

### P1+ 深入動手(P1 填)

> (P1+ / P1 填): unshare、nsenter、cgroupfs 操作、/proc/PID/ns、容器 PID 1 問題、cgroup v1 vs v2 差異、CPU throttle 測量。

---

## 3. TCP 狀態機

> **首次出現: P2a(Service 內部機制、conntrack、TIME_WAIT)**

(P2a 填)

待補內容規劃:
- TCP 三次握手 + 四次揮手的狀態轉移圖
- `ss -s` / `ss -t state` 的讀法
- TIME_WAIT 的成因與在高並發場景的影響
- conntrack(connection tracking)的原理:NAT 需要 conntrack 記住「這個回包屬於哪個連線」
- conntrack table 滿了怎麼查 + 怎麼救

---

## 4. DNS 全解析

> **首次出現: P2a(CoreDNS、Service discovery、Pod DNS 設定)**

(P2a 填)

待補內容規劃:
- DNS 遞迴查詢完整路徑(stub resolver → recursive resolver → root → TLD → authoritative)
- k8s 的 DNS search domain:`svc.cluster.local`、`<namespace>.svc.cluster.local`
- CoreDNS 在 k8s 中的角色:cluster-internal DNS 服務
- Pod 的 `/etc/resolv.conf` 長什麼樣子,為什麼有 5 個 search domain
- ndots:5 的坑:外部 domain 查 5 次 NXDOMAIN 才 fallback,延遲影響
- 故障排查:`kubectl exec -- nslookup`、CoreDNS log

---

## 5. Linux 性能排查(CPU/mem/IO/網路)

> **首次出現: P3(USE/RED 方法論、Chaos drill 排查工具鏈)**

(P3 填)

待補內容規劃:
- USE 方法論(Utilization / Saturation / Errors)
- CPU 排查: `top`、`vmstat`、`perf top`、`mpstat`
- Memory 排查: `free -h`、`/proc/meminfo`、OOM 日誌、slab cache
- IO 排查: `iostat -x`、`iotop`、iowait vs wait
- 網路排查: `ss`、`netstat`、`tcpdump`、`sar -n DEV`
- k8s 節點排查: `kubectl top node`、`kubectl describe node`、kubelet log
