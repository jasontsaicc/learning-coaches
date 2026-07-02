# 跨 Phase 底層基礎: Linux + 網路

> **如何使用此檔:** 這是跨所有 phase 的底層原理參考文件。教學引擎在遇到「前置知識有洞」(Feynman Gate 第 3 次 fail)時讀取對應章節補底。
> 每一節標示「首次出現 phase」;coach 只在到達該 phase 時才深入該節。
> 五個章節皆已填完;各節仍標示「首次出現 phase」,coach 到該 phase 才深入該節。

---

## 目錄

| 章節 | 首次出現 | 狀態 |
|------|---------|------|
| 1. 控制理論(reconcile 的根源) | P0 | 已填 |
| 2. Linux namespace + cgroup(容器的本質) | P0/P1 | 已填(P0 直覺 + P1+ 深入動手) |
| 3. TCP 狀態機 | P2a | 已填 |
| 4. DNS 全解析 | P2a | 已填 |
| 5. Linux 性能排查(CPU/mem/IO/網路) | P3 | 已填 |

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

### P1+ 深入動手(補洞材料)

> **使用時機**:學員 P1 已畢業(QoS/OOM/exit 137/可壓縮 vs 不可壓縮都打穿了,見 progress.md session 5、10)。這節是「往下再一層」:當 Feynman Gate 在容器本質相關題第 3 次 fail,或學員主動想看 kernel 介面本體時才取用。
> [RUNTIME: 每個小節可獨立取用,依當下卡點挑一節,不要整段灌。]

#### 2.1 unshare:親手造一個 namespace

容器 runtime 做的第一步不是魔法,就是這組 syscall(`clone`/`unshare`)。在本機(host,不用 kind)直接做:

```
sudo unshare --pid --fork --mount-proc bash
ps aux          # 只看到 bash 和 ps 自己
echo $$         # 1:你就是這個小世界的 PID 1
exit
```

再造一個 uts namespace 感受「視角隔離」:

```
sudo unshare --uts bash
hostname lab-box    # 只改到這個 namespace 裡的 hostname
hostname            # lab-box
exit
hostname            # host 原名,完全沒被動到
```

一句話收束:`docker run` 的隔離 = 對新 process 呼叫這些 unshare,再 chroot 進 image 的 rootfs。

#### 2.2 /proc/PID/ns:namespace 的身分證

每個 process 屬於哪組 namespace,kernel 用 inode 編號標記:

```
ls -l /proc/$$/ns
readlink /proc/$$/ns/net    # 例: net:[4026531840]
```

判準:兩個 process 的 `ns/net` inode 相同 = 在同一個 network namespace。

k8s 接軌(回扣 P1 chunk 2 的 pause container):同一個 Pod 內各 container 的 `/proc/<pid>/ns/net` inode 全部相同,而且等於 pause container 的。pause 的唯一工作就是「抱著這組 namespace 不死」,app container 重啟時 Pod IP 不變的原因在此。

#### 2.3 nsenter:進到容器的 namespace(kubectl exec 的底層)

在 kind 上驗證(lab 前先確認 context):

```
kubectl config current-context    # 必須是 kind-k8s-coach-p0
kubectl run ns-demo --image=nginx --restart=Never
kubectl get pod ns-demo -o wide   # 記下落在哪個 node
docker exec -it <node名> bash     # kind 的 node 就是 docker container
crictl ps | grep ns-demo          # 找 container id
crictl inspect <cid> | grep -m1 '"pid"'   # 找 host 視角的 PID
nsenter -t <pid> -n ip addr       # 只進 net ns:看到 Pod 的 eth0 和 Pod IP
nsenter -t <pid> -n -p -m ps aux  # 進 net+pid+mnt:看到容器內的行程表
```

打穿:`kubectl exec` 走 API Server → 該 node 的 kubelet → CRI(containerd)→ runc exec,最後一步和 nsenter 用的是同一個 syscall:`setns()`。差別只在誰幫你找 PID、誰幫你接 stdio。

誘答彈藥(keystone):「kubectl exec 就是 ssh 進容器」。錯:容器裡通常沒有 sshd,也沒有走 22 port;是 node 上的 runtime 用 setns 把一個新 process 塞進該容器的 namespace 組。追問:「所以 exec 進去看到的網路,和容器 app 看到的一樣嗎?」(一樣,同一個 net ns,這正是 exec 能用來排障的理由。)

#### 2.4 cgroupfs 直接讀寫(v2 為主,v1 對照)

先確認版本(本機和 kind node 都是 v2):

```
stat -fc %T /sys/fs/cgroup    # cgroup2fs = v2 unified;tmpfs = v1
```

host 上手做一次 OOM 的最小重現(不經 k8s,直接對 kernel):

```
sudo mkdir /sys/fs/cgroup/labdemo
echo 50M | sudo tee /sys/fs/cgroup/labdemo/memory.max
sudo bash -c 'echo $$ > /sys/fs/cgroup/labdemo/cgroup.procs; python3 -c "x = bytearray(200*1024*1024)"'
# 直接被 OOM killer 殺;dmesg | tail 可看到 kill 紀錄
sudo rmdir /sys/fs/cgroup/labdemo
```

回扣學員 session 5 的 oom-demo lab(polinux/stress 要 150M、limit 100Mi):當時在 k8s 看到的 OOMKilled,本體就是 kubelet 請 runtime 寫進 `memory.max` 的那個數字。找出 Pod 的 cgroup 本體:

```
docker exec <node名> find /sys/fs/cgroup/kubepods.slice -name memory.max | head
docker exec <node名> cat <該路徑>    # 就是你 YAML 裡的 limits.memory
```

v1 對照表(舊 node、面試常考「你知道 v1 v2 差在哪」):

| 控制什麼 | cgroup v1 | cgroup v2 |
|---------|-----------|-----------|
| memory 上限 | `memory.limit_in_bytes` | `memory.max` |
| CPU 配額 | `cpu.cfs_quota_us` / `cpu.cfs_period_us` 兩檔 | `cpu.max`(一檔兩值,如 `20000 100000`)|
| CPU 權重(requests)| `cpu.shares`(1024 基準)| `cpu.weight`(100 基準)|
| 層級結構 | 每個 controller 一棵樹(mount 一堆)| 單一樹(unified hierarchy)|

#### 2.5 容器的 PID 1 問題(訊號、殭屍、為什麼要 tini)

kernel 對 PID 1 有特殊待遇,兩條都會咬人:

1. **訊號**:PID 1 對「沒有註冊 handler 的訊號」不套用預設行為,直接忽略(kernel 的保護,怕 init 被誤殺)。所以 app 當 PID 1 又沒寫 SIGTERM handler → `kubectl delete pod` 的 SIGTERM 石沉大海 → 卡滿 `terminationGracePeriodSeconds`(預設 30s)才被 SIGKILL。症狀:rollout 特別慢、Pod 長時間卡 Terminating。
2. **殭屍行程**:PID 1 要負責收養並 reap(`wait()`)孤兒行程。用 shell script 當 entrypoint、裡面 fork 一堆子程序的容器,子孫死了沒人收屍 → zombie 累積 → 撞 pids cgroup 上限,新 process fork 不出來。

tini / dumb-init 就是為此存在的極小 init:轉發訊號給子行程 + 負責 reap。`docker run --init` 塞的就是 tini。k8s 側的等價做法:image 的 ENTRYPOINT 用 tini 包住 app,或確保 app 自己 handle SIGTERM。

exit 137 的第二種死法(學員已把 137 = 128+9 = SIGKILL、OOMKilled 打穿,這裡補精度):同樣是 137,`describe` 的 Reason 是 `OOMKilled` 才是撞 memory limit;Reason 是 `Error` 且剛好發生在 delete/rollout 時,常是 grace period 到期的 SIGKILL,根因是上面第 1 條。一個數字,兩條路,靠 Reason 分流。

誘答彈藥(keystone):「容器裡 PID 1 收到 SIGTERM 一定會終止,因為 SIGTERM 的預設動作就是 terminate」。錯:預設動作對 PID 1 不適用,沒 handler 就是忽略。這題專打「背了 signal 表但沒打穿 PID 1 特例」的邊界。

#### 2.6 CPU throttle 的測量(cpu.stat)

throttle 是「可壓縮」資源的實體(回扣學員 session 5 自己推出的可壓縮 vs 不可壓縮):CPU 超過 limit 不會死,只會被 CFS 按 period(預設 100ms)扣住。證據在 cgroup 的 `cpu.stat`:

```
docker exec <node名> cat /sys/fs/cgroup/kubepods.slice/.../cpu.stat
# nr_periods 12345      經過幾個 100ms 週期
# nr_throttled 678      其中幾個週期配額被燒完、被扣住
# throttled_usec 900000 total 被扣住的時間(v1 叫 throttled_time,單位 ns)
```

throttle 率 = nr_throttled / nr_periods。Prometheus 對應指標:`container_cpu_cfs_throttled_periods_total`(P4 observability 會回收這條線)。

誘答彈藥:「CPU 平均使用率離 limit 還很遠,所以不可能被 throttle」。錯:配額是以 100ms 為單位結算的。多執行緒 app 在一個 period 的前 20ms 就把配額燒完,剩下 80ms 全體罰站,平均使用率看起來卻很低。這是 latency 尖刺查不到根因時的經典盲區,`throttled_usec` 一看就破。

術語卡(1 張):
`PID 1 (init process) | /ˌpiː aɪ ˈdiː wʌn/ | The first process in a PID namespace, responsible for reaping orphans; unhandled signals are ignored by the kernel. | 容器裡的老大:要收屍,且沒登記的訊號一律已讀不回。`

---

## 3. TCP 狀態機

> **首次出現: P2a(Service 內部機制、conntrack、TIME_WAIT、高並發 502)**
> 學員狀態:conntrack 基本原理、table full 症狀、查法(conntrack -L、nf_conntrack_count/_max、dmesg)在 P2a chunk 1 已畢業,別重教 what;本節 3.5 只做深化。
> [RUNTIME: 3.1-3.4 是新料;依學員當下的排障題挑切面,不用照順序走完。]

### 3.1 三次握手 + 四次揮手的狀態轉移

握手(注意 server 側兩個 queue,3.4 的主角在這裡登場):

```
Client                                    Server
CLOSED                                    LISTEN
   | ---------- SYN ---------->              |
SYN_SENT                              SYN_RECV(進 SYN backlog,半連線)
   | <------- SYN+ACK ---------              |
   | ---------- ACK ---------->        握手完成,搬進 accept queue
ESTABLISHED                           app 呼叫 accept() 後才真正拿到
                                      ESTABLISHED
```

揮手(誰先 close 誰付 TIME_WAIT 的帳):

```
主動關閉方                              被動關閉方
ESTABLISHED                             ESTABLISHED
   | ---------- FIN ---------->            |
FIN_WAIT_1                              CLOSE_WAIT(kernel 收到 FIN 了,
   | <--------- ACK -----------          但 app 還沒呼叫 close())
FIN_WAIT_2                                 |
   | <--------- FIN -----------         LAST_ACK(app 終於 close())
   | ---------- ACK ---------->            |
TIME_WAIT(停 2*MSL = 60s)              CLOSED
   v
CLOSED
```

排障判準(面試也愛考):
- CLOSE_WAIT 堆積 = 對面已說再見,你的 app 一直沒 `close()` = 幾乎必是 code bug(connection leak、忘記關 response body)。
- TIME_WAIT 堆積 = 你是主動關閉方,大量短連線的正常代價,不一定是 bug。

Say it in English: "A pile of CLOSE_WAIT means the application never called close(); a pile of TIME_WAIT just means this side closes connections first."

### 3.2 TIME_WAIT:存在理由與高並發影響

存在理由有兩個,少講一個就是半懂:
1. 最後那個 ACK 可能丟。丟了對方會重送 FIN,得有人留在原地重回 ACK,否則對方永遠關不掉。
2. 防止「上一條連線的迷路封包」污染同一組 4-tuple(src IP, src port, dst IP, dst port)的新連線。等 2*MSL 讓舊封包在網路上自然死亡。

高並發影響:TIME_WAIT 本身很便宜(一條約 0.2KB kernel 記憶體),真正的殺手是 port 耗盡。4-tuple 裡 client 的 ephemeral port 預設只有約 28000 個(`net.ipv4.ip_local_port_range` = 32768-60999),每條 TIME_WAIT 佔住一個 port 60 秒。算術:對同一個目的地,持續短連線的極限約 28000/60 ≈ 470 conn/s,超過就 `connect: cannot assign requested address`。

解法階梯(治本在前):
1. 治本:連線重用。HTTP keep-alive、connection pool,把「每請求一條連線」改掉。
2. `net.ipv4.tcp_tw_reuse=2`:client 側安全重用 TIME_WAIT port(靠 TCP timestamps 判斷)。
3. 放大 `ip_local_port_range`、增加來源 IP。

誘答彈藥(keystone):「TIME_WAIT 太多就開 `tcp_tw_recycle`,一次清光」。錯得很有歷史:tw_recycle 在 NAT 環境會亂丟合法封包(靠 per-IP timestamp 遞增假設,NAT 後多台機器共用一個 IP 就破功),kernel 4.12 起整個移除。k8s 節點全是 NAT 場景,這選項在雲環境是事故製造機。這題專打「背 sysctl 調優清單但不知道為什麼」。

k8s 接軌:Pod 出叢集的流量常被 SNAT 成 node IP,全 node 的 Pod 共享同一個 node IP 的 port 空間(而且是 conntrack 在挑 port),所以「單一 node 上大量 Pod 對同一外部 API 打短連線」會比你以為的更早撞牆。

### 3.3 ss 的讀法

```
ss -s                                      # 總覽:estab/timewait/synrecv 各幾條
ss -t state time-wait | wc -l              # 數某狀態的連線
ss -t state established '( dport = :443 )' # 過濾:對 443 的 established
ss -tnp | grep <pid>                       # 某 process 的連線(要 root 看全)
ss -lnt                                    # LISTEN sockets,下一節的主角
```

`ss -lnt` 有一個語義翻轉,不知道的人會讀錯(好誘答素材):

| 欄位 | 一般連線(ESTABLISHED)| LISTEN socket |
|------|--------------------|---------------|
| Recv-Q | 還沒被 app 讀走的 bytes | **accept queue 目前長度**(已完成握手、還沒被 accept 的連線數)|
| Send-Q | 還沒被對方 ACK 的 bytes | **accept queue 上限**(backlog)|

Recv-Q 貼近 Send-Q = accept queue 快滿 = 3.4 的案發現場。

### 3.4 SYN backlog 與 accept queue(高並發 502 的常見根因)

server 側其實有兩條隊伍,握手圖裡已見過:

```
SYN 進來
  → [SYN backlog]  半連線(SYN_RECV),上限 net.ipv4.tcp_max_syn_backlog
  → 握手完成,搬進
  → [accept queue] 全連線,上限 min(listen() 的 backlog 參數, net.core.somaxconn)
  → app 呼叫 accept() 取走,開始處理
```

兩種滿法,症狀不同:
- SYN backlog 滿:多半是 SYN flood 或握手洪峰。有 syncookies 頂著(`net.ipv4.tcp_syncookies=1` 是預設),通常不是 502 主因。
- accept queue 滿:kernel 對「已完成握手的新連線」直接丟棄(預設)或回 RST(`tcp_abort_on_overflow=1`)。client 視角:connect 成功了卻 timeout。nginx/ingress 視角:upstream timeout 或 connection reset → 對外吐 502/504。

根因幾乎都不是 queue 太小,是 app 取貨太慢:thread pool 卡死、GC pause、慢 SQL 把 worker 全佔住,accept() 沒人叫。查法:

```
ss -lnt                          # LISTEN 的 Recv-Q 逼近 Send-Q?
netstat -s | grep -i listen      # "times the listen queue overflowed" 累計數
```

誘答彈藥(keystone):「502 一直出現,把 somaxconn 從 128 調到 65535 就解決了」。半錯:queue 加大只是把等待搬進 kernel,latency 照樣爆,還讓問題更晚被看見。正解順序:先找 app 為什麼 accept 慢(治本),queue 大小只是給突發流量的緩衝(治標)。這題結構和學員 P1 的「memory leak 調大 limit」完全同構,可以拿來考遷移。

Say it in English: "502s under load are often an accept-queue overflow: the app stops calling accept() fast enough, the kernel drops fully-established connections, and the proxy in front reports a bad gateway."

### 3.5 conntrack 深化(接 chunk 1 已學的基礎)

前情提要(已畢業,不重教):conntrack 是 node kernel 的連線記帳本,DNAT 的回程改寫靠它;table full 時新連線被丟、既有連線照常;kubectl 永遠看不到它。以下是往下一層。

**條目生命週期與 timeout**。conntrack 的 TCP 狀態是「中間人的推斷版」狀態機:它看雙向封包,推斷連線走到哪,每個狀態掛不同 timeout:

```
sysctl net.netfilter.nf_conntrack_tcp_timeout_syn_sent      # 120s
sysctl net.netfilter.nf_conntrack_tcp_timeout_established   # 432000s = 5 天
sysctl net.netfilter.nf_conntrack_tcp_timeout_time_wait     # 120s
sysctl net.netfilter.nf_conntrack_udp_timeout               # 30s(單向)
sysctl net.netfilter.nf_conntrack_udp_timeout_stream        # 120s(雙向後)
```

兩個坑就藏在數字裡:
1. established 5 天:連線沒好好關(RST 在路上丟了、對端斷電),殭屍條目佔位 5 天才過期。長連線大戶 + 異常斷線 = table 慢性水腫。
2. UDP 沒有握手,每「一次」DNS 查詢就是一條 30s 的 conntrack 條目。搭配 §4 的 ndots 流量放大(一次解析 8+ 個 query),DNS 常是 table full 案發現場的頭號嫌犯。兩節要合起來看。

**TCP 狀態 vs conntrack 狀態的對應**:名字互相借用但不是同一張表。socket 狀態(`ss` 看的)只存在於連線兩端;conntrack 狀態(`conntrack -L` 看的)存在於路過的每個 NAT node。同一條連線,Pod 裡 `ss` 顯示 ESTABLISHED,node 上 `conntrack -L` 也有一條 ESTABLISHED,但那是兩個獨立的狀態機,可能失同步(例:conntrack 條目先過期,回程封包就變孤兒被丟,app 端看到的是莫名 timeout)。

```
conntrack -L -p tcp --state ESTABLISHED | head
conntrack -S        # per-CPU 統計:insert_failed、drop、early_drop
```

精準度補刀(學員 session 11 在「table full 時新 vs 舊」精度掉過,這是精準版):table full 時 kernel 先嘗試 early_drop,踢掉「未 assured」的條目(半開、單向、還沒確認雙向通的);踢不出位子才丟新封包。所以精確說法是:已確立(assured)的舊連線安全,犧牲的是新連線和半熟條目。「舊連線照常、新連線被丟」是這個機制的白話近似。

**NOTRACK 場景**:raw table 的 `-j CT --notrack` 讓指定流量完全跳過 conntrack。用在「高 QPS 且不需要 NAT」的流量:node-local DNS、LB 健康檢查、本機 loopback 洪流。代價要講得出來才算懂:notrack 的流量不能被 NAT(沒有記帳就無法回程改寫),iptables 的 `ESTABLISHED,RELATED` 這類 stateful 規則也對它失效。k8s 現成案例:NodeLocal DNSCache 自帶 NOTRACK 規則,同時解掉 conntrack 競態丟包和 table 佔用兩個問題(P2a chunk 4 / P3 會回收)。

誘答彈藥(keystone):「conntrack table 滿了,kernel 會踢掉最舊的 established 連線騰位子,所以老用戶會突然斷線」。錯:assured 條目不會被踢,early_drop 只動未 assured 的半熟條目,騰不出位子就丟新連線的封包,dmesg 出 `nf_conntrack: table full, dropping packet`。[RUNTIME: 這題直接對著 mistake-registry 的 07-04 冷測點打,學員答對就結案。]

術語卡(2 張):
`TIME_WAIT | /taɪm weɪt/ | The 2*MSL state held by whoever closes a TCP connection first, to retransmit the final ACK and absorb stray old packets. | 先說再見的人要在原地罰站 60 秒,替整條連線收尾。`
`accept queue | /əkˈsɛpt kjuː/ | The kernel queue holding fully-established connections waiting for the application to call accept(). | 握完手排隊等 app 取貨的隊伍;滿了就是 502 的地下室。`

---

## 4. DNS 全解析

> **首次出現: P2a(CoreDNS、Service discovery、Pod DNS 設定)**
> 學員狀態:CoreDNS 角色、resolv.conf 由 kubelet 注入、跨 ns 要 FQDN、排障階梯(svc+endpoints → CoreDNS 活著嗎 → 進 Pod 查)已在 chunk 1 畢業;D 段 lab 親手撞過 busybox nslookup 的坑(2026-06-28)。本節補的是叢集外的完整世界觀 + ndots + 層級分界。
> [RUNTIME: 4.6 是為 session 11 的層級混淆特製的,該誤解重演時優先取用。]

### 4.1 遞迴查詢完整路徑

叢集外的 DNS 世界長這樣:

```
app ──> stub resolver(app 所在機器的小跑腿,照 /etc/resolv.conf 辦事)
              |
              v
      recursive resolver(真正做苦工 + 快取的人,例: 8.8.8.8、公司內 DNS)
              |
              |  1. 問 root(.):「.com 歸誰管?」──> 回 TLD server 名單
              |  2. 問 TLD(.com):「example.com 歸誰管?」──> 回 authoritative 名單
              |  3. 問 authoritative:「www.example.com 的 A?」──> 回答案 + TTL
              v
       答案往回傳,recursive 快取一份(存活 TTL 秒)
```

分工一句話:stub 只會「轉問 + 等答案」;recursive 負責追根究柢;authoritative 是唯一有權給答案的源頭。

k8s 對應:Pod 的 stub resolver 指向 CoreDNS(resolv.conf 的 nameserver = CoreDNS 的 ClusterIP,chunk 1 學過)。CoreDNS 的雙重身分:對 `cluster.local` 它自己就是 authoritative(答案來自 watch API Server 的 Service/EndpointSlice);對外部域名它只是 forwarder,轉給上游(預設 node 的 resolv.conf 指到誰就轉給誰),不自己遞迴到 root。

誘答彈藥:「Pod 查 google.com 慢,因為 CoreDNS 要一路問 root → TLD → authoritative」。錯兩層:CoreDNS 是 forwarder 不做遞迴;而且查外部域名慢的頭號嫌犯根本不在這條路上,是 4.4 的 ndots。

### 4.2 Record 類型速覽

| 類型 | 內容 | k8s 現場 |
|------|------|---------|
| A | name → IPv4 | 一般 Service:`backend.default.svc.cluster.local` → ClusterIP;headless Service(clusterIP: None)→ 直接回每個 Pod IP(多筆 A)|
| AAAA | name → IPv6 | 多數 client 解析時 A、AAAA 各發一次,查詢量 x2(4.4 的放大器)|
| CNAME | name → 另一個 name | ExternalName Service 的本質就是一筆 CNAME |
| SRV | name → host + **port** + 權重 | 連 port 都要用 DNS 發現時用(etcd、StatefulSet 成員發現)|

### 4.3 TTL 與快取層級

每一層都可能存一份答案,排障時要知道「舊答案可能卡在哪一層」:

```
authoritative(定 TTL)
  → recursive resolver 快取(遵守 TTL)
  → OS 層快取(Linux 預設沒有;有 systemd-resolved / nscd 才有)
  → app 內部快取(最陰的一層:JVM 預設成功解析永久快取,IP 換了 app 不會知道)
```

兩個實戰點:
1. negative caching:NXDOMAIN 也會被快取(存活時間由該 zone SOA 的 minimum 值決定)。所以「域名打錯,改對了還繼續錯一陣子」是正常物理,不是靈異。
2. CoreDNS 的 cache plugin 預設 30s:改了 Service 之後最多有 30s 舊答案,加上 client 端自己的快取,層層相加。

### 4.4 k8s 接軌:search domain 與 ndots:5 的坑

Pod 裡的 resolv.conf(kubelet 注入,chunk 1 看過):

```
search default.svc.cluster.local svc.cluster.local cluster.local
nameserver 10.96.0.10
options ndots:5
```

規則:查詢名字裡的 dot 數「小於 ndots」→ 先把 search list 逐一接上去查,全部失敗才查原名。這讓 `backend` 這種短名能自動長成 `backend.default.svc.cluster.local`,是便利的來源;代價全算在外部域名頭上。

算給你看,Pod 裡查 `api.stripe.com`(2 個 dot < 5):

```
api.stripe.com.default.svc.cluster.local  → NXDOMAIN
api.stripe.com.svc.cluster.local          → NXDOMAIN
api.stripe.com.cluster.local              → NXDOMAIN
api.stripe.com                            → 才拿到答案
```

4 輪 x(A + AAAA)= 8 個 query,其中 6 個是注定失敗的白工。每個 UDP query 還是一條 conntrack 條目(§3.5),高 QPS 下這是延遲 + table 佔用的雙重放大器。

解法階梯:
1. FQDN 加尾點:`api.stripe.com.`(trailing dot = 絕對名,直接跳過 search list)。
2. Pod spec 的 `dnsConfig: options: [{name: ndots, value: "1"}]`:外部域名為主的 workload 適用。
3. NodeLocal DNSCache:每個 node 放一個 DNS 快取,順便 NOTRACK(§3.5 的回收點)。

誘答彈藥(keystone):「search domain 就是造成延遲的元凶,把它拿掉就好」。錯:search list 是 `backend`、`backend.other-ns` 這類短名能用的前提,拿掉會弄壞叢集內的服務發現慣例;真正的旋鈕是 ndots(或 trailing dot),讓外部域名不要陪跑。

### 4.5 排障工具的坑:busybox nslookup(學員親踩過)

回扣學員 2026-06-28 D 段 lab 現場 debug 的坑:busybox 內建的 nslookup(尤其 1.28.x)對 search domain 的處理有 bug、輸出還會把「server 反解失敗」印得像查詢失敗,誤報率高到不能當證據。工具選擇:

```
kubectl run dbg --rm -it --image=nicolaka/netshoot -- bash   # dig/host/ss/tcpdump 全有
dig backend.default.svc.cluster.local    # 注意:dig 預設不走 search list!
dig +search backend                      # 要模擬短名行為得加 +search
kubectl exec <pod> -- getent hosts backend   # 走完整 glibc 解析路徑,最貼近 app 真實行為
```

dig 預設不吃 search list 是第二個誤判源:`dig backend` 查不到不代表 app 查不到。要驗證「app 到底會怎麼解析」,`getent hosts` 最誠實。

### 4.6 DNS 解析層 vs 連線層的分界(專治層級混淆)

> 客製背景:學員 session 11 曾把 conntrack 誤拉進 NXDOMAIN 排障題(層級混淆),已當場拆解。此節是那次拆解的定稿版,重演時直接用。

一條請求的時間線,先後分明:

```
[解析層] app 問「backend 是誰」
   resolv.conf → CoreDNS → 拿到一個 IP
   這層的失敗長相:NXDOMAIN、SERVFAIL、DNS query timeout
─────────── 拿到 IP 之後,下面才開始 ───────────
[連線層] app 對那個 IP 發 SYN
   iptables DNAT → conntrack 記帳 → 到 Pod
   這層的失敗長相:connection refused、connection timeout、reset
```

分界判準一句話:**NXDOMAIN 是一個「成功送達的回答」,內容是查無此名。** 封包要能來回,你才拿得到 NXDOMAIN。所以看到 NXDOMAIN 的當下,已經證明到 CoreDNS 這段的連線層是通的,conntrack、DNAT、iptables 全部從嫌疑名單劃掉,往「名字對不對、search domain 展開成了什麼、Service 存不存在」查。

精確的例外(精準度上限,學員用詞精準是長期弱點,這句要能原樣說出):conntrack table full 或 UDP 競態可以害 DNS query「timeout」(封包層的失敗),但永遠製造不出 NXDOMAIN(內容層的回答)。症狀對照表:

| 症狀 | 層 | 往哪查 |
|------|-----|--------|
| NXDOMAIN | 解析層 | 名字拼寫、跨 ns 忘了 FQDN、search 展開、Service 在不在 |
| SERVFAIL | 解析層 | CoreDNS 本身或它的上游掛了 |
| DNS query timeout | 連線層(DNS 封包到不了或回不來)| CoreDNS Pod 活著嗎、conntrack、網路 |
| could not resolve host | 解析層的統稱 | 先分辨是 NXDOMAIN 還是 timeout 再走上兩行 |
| connection refused / timeout(已拿到 IP 後)| 連線層 | endpoints、DNAT、目標 Pod |

誘答彈藥(keystone):「Pod 查內部 Service 一直回 NXDOMAIN,可能是 conntrack table 滿了,先清 conntrack 看看」。錯:table 滿只能讓 query 無聲 timeout,能收到 NXDOMAIN 就代表 DNS 封包有去有回;這是解析層的內容問題。[RUNTIME: 此題即 session 11 原始混淆的重演版,對 07-08 冷測點使用。]

術語卡(2 張):
`ndots | /ˈɛn dɒts/ | The resolv.conf threshold: names with fewer dots are tried against the search list before being queried as-is. | 幾個點以下先當短名補全;k8s 設 5,外部域名因此陪跑好幾輪。`
`negative caching | /ˈnɛɡətɪv ˈkæʃɪŋ/ | Caching an NXDOMAIN answer for the time defined by the zone's SOA minimum, so repeated misses don't hammer upstream. | 「查無此名」也會被記住一陣子,改對了不會立刻好。`

---

## 5. Linux 性能排查(CPU/mem/IO/網路)

> **首次出現: P3(USE 方法論、Chaos drill 排查工具鏈)**
> 定位:這節不是教學主線,是 P3 chaos drill 的排查工具箱。**E 段 drill 卡住時,按資源類型跳查對應小節**:CPU → 5.2、Memory → 5.3、IO → 5.4、網路 → 5.5、k8s node 條件 → 5.6;完全沒頭緒就直接走 5.7 的 60 秒清單。
> 學員狀態:P1 已打穿 OOM/QoS/exit 137/可壓縮 vs 不可壓縮,P2a chunk 1 已畢業 conntrack。本節不重教這些 what,只接「站在 node 上怎麼查」的視角。學員是 DevOps、AWS 背景,雲上限速類的坑(EC2/EBS/ENA)可以直接對他的日常打。
> [RUNTIME: 依 drill 現場的症狀挑小節,不要整段灌;誘答題對著學員當下似懂非懂的邊界挑用。]

### 5.1 USE 方法論:排查的骨架

The USE method (Brendan Gregg) turns "the system is slow" into a finite checklist. For every resource, ask three questions: **Utilization** (how busy is it), **Saturation** (how much work is queued because the resource cannot keep up), and **Errors** (did anything fail outright). Coverage matters more than order: walk every resource, ask all three, and you either find the bottleneck or you have positively ruled that resource out. That "ruled out" is half the value; it stops the team from re-checking the same graph five times.

關鍵區分是 utilization 和 saturation 不是同一件事:100% utilization 只代表「沒閒著」,不必然有人在排隊;latency 的來源是 saturation(隊伍長度)。高速公路比喻:車流量滿(utilization 高)但還在時速 100 跑,乘客無感;一旦開始塞車回堵(saturation),行車時間才爆炸。

資源 × USE × 工具對照表(本節後續小節的地圖):

| 資源 | Utilization | Saturation | Errors |
|------|-------------|------------|--------|
| CPU | `mpstat -P ALL`(%usr+%sys)| `vmstat` 的 r 欄 > 核數、load average(要先扣掉 D state,見 5.2)| `dmesg`;容器視角看 `cpu.stat` 的 nr_throttled(§2.6)|
| Memory | `free -h` 的 available | `vmstat` 的 si/so(swap 進出)、kubelet MemoryPressure(5.6)| `dmesg` 的 oom-killer 段(5.3)|
| Disk IO | `iostat -x` 的 %util(注意 5.4 的語義陷阱)| `iostat -x` 的 await、aqu-sz | `dmesg` 的 IO error |
| 網路 NIC | `sar -n DEV` 的 rxkB/s、txkB/s 對頻寬 | `ss -lnt` 的 Recv-Q(accept queue,§3.3)| `sar -n EDEV` 的 drop/err;ENA `ethtool -S`(5.5)|
| conntrack | `nf_conntrack_count` / `_max` 比值 | count 逼近 max | `conntrack -S` 的 insert_failed、dmesg table full(§3.5)|

### 5.2 CPU:top / mpstat / pidstat 與 load average 的真義

`top` 先讀表頭那行 `%Cpu(s)`,五個關鍵字母:

- `us`(user)高:app 自己在燒,查哪個 process(pidstat)。
- `sy`(system)高:kernel 在燒,常見於 syscall 風暴、大量小封包、iptables/conntrack 開銷。
- `wa`(iowait):見下方迷思拆解。
- `si`(softirq)高:網路收包壓力大的訊號。
- `st`(steal):hypervisor 扣走的 CPU。AWS 場景直接命中:t 系列 instance CPU credit 燒完、或 shared host 吵鬧鄰居,node 裡看就是 st 升高。這是「機器裡怎麼查都查不到誰在用 CPU」的標準答案之一。

`mpstat -P ALL 1` 看各核是否均勻:一顆核 100%、其他全閒 = 單執行緒瓶頸或 IRQ 集中,平均值會把它藏起來。`pidstat 1` 逐 process 列 CPU(比 top 適合留紀錄貼進 incident timeline),`pidstat -t` 可再往 thread 拆。

Load average is the most misquoted number in Linux. It does not measure CPU busyness; it counts tasks that are either runnable (using or waiting for a CPU) or in **uninterruptible sleep, the D state**, which usually means waiting on disk or NFS I/O. So "load 30 on an 8-core box" has two very different readings: a genuine CPU pile-up, or dozens of processes stuck in D state behind a dying disk or a hung NFS mount while the CPUs sit idle. Split the two before acting: `ps -eo state,pid,comm | grep '^D'` lists the D-state suspects, and in `vmstat` the r column is the CPU queue while the b column is the uninterruptible queue.

%iowait 迷思要拆兩面:iowait 的定義是「CPU 沒事做,而且系統有未完成的 IO」,本質是 idle 的一種。所以(1)iowait 高不代表 CPU 有問題,代表 CPU 在等磁碟,該跳 5.4;(2)iowait 低不代表 IO 沒問題:只要 CPU 同時有別的活可幹,iowait 就被吃掉,IO 排隊照樣存在。IO 的判準以 `iostat` 的 await 為主,iowait 只是線索。

容器/cgroup 視角(回扣學員 P1 自己推出的可壓縮 vs 不可壓縮):node 整體 CPU 很閒、某個 Pod 卻 latency 尖刺,查該容器 cgroup 的 `cpu.stat`(nr_throttled / throttled_usec,查法與「平均使用率低照樣被 throttle」誘答已寫在 §2.6,直接跳)。throttle 就是可壓縮資源撞 limit 的實體:不死,罰站。

誘答彈藥(keystone):「load average 20、機器只有 8 核,顯然 CPU 不夠,先垂直擴容加 CPU」。錯:load 算的是 runnable + D state 的總和。先抓 D state:一批 process 卡 D = 磁碟或 NFS 的事,加 CPU 一點用都沒有。追問補刀:「vmstat 的 r 和 b 兩欄,哪欄對應你說的 CPU 不夠?」(r 是 CPU 隊、b 是 IO 隊,一眼分流。)

### 5.3 Memory:free 的誤會、OOM 日誌、slab

`free -h` 是新人誤報率最高的指令:看 free 欄快見底就喊記憶體不足。Linux 的設計是 unused RAM is wasted RAM:閒置記憶體會被拿去當 page cache(buff/cache 欄),誰要就還誰。真正「還能給 app 用」的是 **available** 欄(kernel 估算:free + 可回收的 cache/slab)。判斷記憶體壓力永遠看 available,free 小是常態不是病。

`/proc/meminfo` 關鍵欄位(free 就是讀它):

| 欄位 | 意義 | 排查訊號 |
|------|------|---------|
| MemAvailable | 可回收後真正能用的量 | 持續下探 = 真壓力 |
| Cached | page cache | 大 = 正常;被 IO 讀寫餵大 |
| Dirty | 已改還沒落盤的髒頁 | 持續高 = 寫入下不去,查 5.4 |
| AnonPages | process 的 heap/stack(無檔案後盾)| OOM 的主角,只能靠 swap 或殺人回收 |
| Slab(SReclaimable / SUnreclaim)| kernel 物件快取 | SUnreclaim 持續漲 = kernel 側洩漏 |

OOM 日誌怎麼讀(`dmesg -T | grep -i -A 30 oom-killer`),三段結構:

1. 開頭 `<process> invoked oom-killer`:誰申請記憶體時觸發的(不一定是被殺的那個)。
2. 中段看有沒有 cgroup 路徑:出現 `Memory cgroup out of memory` + kubepods 路徑 = **容器級 OOM**(撞自己的 memory.max,跟 node 餘量無關);沒有 cgroup、掃的是全機 = **node 級 OOM**。學員 session 5 已打穿這兩種 OOM 的概念,這裡是拿證據的位置:k8s `describe` 看到 OOMKilled 只是結論,dmesg 這段才是案發現場。
3. 結尾 process 表 + `oom_score_adj`,最後 `Killed process <pid> (<name>)`。oom_score_adj 是 kubelet 依 QoS 預先寫好的(Guaranteed -997、BestEffort 1000、Burstable 依 requests 折算),所以 kernel 殺人順序「近似」QoS 驅逐序;但它和 kubelet eviction 是兩條不同機制,5.6 分清楚。

slab 補一刀:dentry/inode cache、還有 conntrack 條目(§3.5 的記帳本本體)都住在 slab 裡。`slabtop` 看誰是大戶;SUnreclaim 一路漲 = kernel 側洩漏,任何 app 的 RSS 都看不到它,這是「所有 Pod 加總遠小於 node used」謎題的常見答案。

誘答彈藥(keystone):「node 上 free -h 的 free 只剩 200Mi,難怪這個 Pod 被 OOMKilled,node 記憶體不足了」。兩層錯:free 小多半只是 page cache 佔好佔滿,要看 available;而且容器級 OOMKilled 只跟自己 cgroup 的 memory.max 有關,node 剩多少無關。回扣學員 session 5 的 oom-demo lab:當時 node 明明有餘量,Pod 照樣 137。[RUNTIME: 學員對兩種 OOM 已熟,此題主要打 free/available 誤讀,別讓他覺得在重考舊題。]

### 5.4 IO:iostat 的 %util 陷阱與 await

`iostat -xz 1` 主要欄位:r/s、w/s(IOPS),rkB/s、wkB/s(吞吐),**r_await / w_await**(每個請求平均花的毫秒數,含排隊+服務),**aqu-sz**(平均在隊請求數),%util。

On modern SSD and NVMe, %util is the most misread column in iostat. It only means "the device had at least one request in flight during the sampling window". A device that serves many requests in parallel can sit at 100% util with plenty of headroom left. The honest saturation signals are latency and queue depth: rising await and a growing aqu-sz mean requests are waiting in line, and that queue is what your users feel.

await 要對 baseline 讀:本地 NVMe 常態是零點幾 ms,SATA SSD 個位數 ms,雲端網路盤(EBS gp3)個位數 ms。AWS 直球:EBS 每顆卷有 IOPS 和 throughput 上限(gp3 基準 3000 IOPS/125 MBps),打滿時 node 裡看到的樣子就是 await 飆高 + %util 貼 100,盤本身沒壞,是 quota 到頂。交叉驗證去 CloudWatch 看 VolumeQueueLength 和 throughput 曲線,這在 EKS node 上是高頻真實案件(gp2 時代 burst credit 耗盡的 IO 雪崩更是經典)。

抓兇手用 `iotop -oPa`(-o 只列活躍、-P 按 process、-a 累計量),或 `pidstat -d 1`。iowait 的正確理解已在 5.2 拆過:它是「CPU 閒著等 IO」的側寫,定罪還是靠 iostat 的 await/aqu-sz。

### 5.5 網路:sar / ss / tcpdump 最小工具組

`sar -n DEV 1` 看每張介面的 rxkB/s、txkB/s(對照頻寬上限算 utilization)和 rxpck/s(PPS);`sar -n EDEV 1` 看 drop 和 error(Errors 欄位的來源)。`sar -n TCP,ETCP 1` 的 retrans/s 是網路品質或對端過載的訊號,60 秒清單會再出現。

AWS 補刀(學員日常):EC2 每種 instance type 有頻寬、PPS、甚至 conntrack 條目數的 allowance,被 hypervisor 限速時 node 內的 sar 看不出「被扣掉的部分」。直接問 ENA driver:`ethtool -S eth0 | grep exceeded`,五個 `*_allowance_exceeded` 計數器(bw_in/bw_out/pps/conntrack/linklocal)有在漲就是撞雲上限額,和 §3.5 的 conntrack table full 是不同層的兩把刀,症狀卻很像(莫名丟包)。

`ss -s` 一眼總覽各 TCP 狀態的數量,判讀直接回扣 §3:CLOSE_WAIT 堆積 = app 沒 close()(code bug);TIME_WAIT 堆積 = 主動關閉方的短連線代價,警戒點是 ephemeral port 耗盡(§3.2);`ss -lnt` 的 Recv-Q 逼近 Send-Q = accept queue 快滿(§3.3、3.4 的 502 地下室)。conntrack 水位三件套照 §3.5:`nf_conntrack_count` vs `_max`、`conntrack -S` 的 insert_failed、dmesg 的 table full。

tcpdump 最小可用招式(三個習慣:`-nn` 不做反解、`-c` 限量、`-w` 存檔離線看):

```
tcpdump -i any -nn port 53 -c 20                    # 先抓 20 個就停,別讓終端被洪水淹
tcpdump -i eth0 -nn host 10.244.1.7 and port 8080   # host + port 縮小到一條對話
tcpdump -i any -nn -w /tmp/cap.pcap port 8080       # 存 pcap,拉回本機用 Wireshark 慢慢讀
```

`-nn` 不是裝酷:反解 hostname 本身會發 DNS query,一邊查 DNS 問題一邊污染現場。Pod 裡沒有 tcpdump 時兩條路:換 netshoot 除錯 Pod(§4.5),或在 node 上 `nsenter -t <pid> -n tcpdump ...`(§2.3 的招式原樣複用,進的是同一個 net namespace,看到的就是 Pod 的流量)。

### 5.6 k8s 節點視角:top node、pressure conditions、kubelet log

`kubectl top node` 看 node 層 CPU/memory 用量(百分比的分母是 allocatable)。環境注意:kind 叢集未裝 metrics-server,P3 HPA lab 前要裝且加 `--kubelet-insecure-tls`;裝好前這條指令只會回 error。

`kubectl describe node <node>` 排查看三塊:

1. **Conditions**:MemoryPressure / DiskPressure / PIDPressure。這三個是 kubelet eviction 機制的臉:kubelet 持續量測 node 資源,跌破 eviction threshold(例:`memory.available < 100Mi`)就把條件翻成 True,同時上 taint 擋新 Pod、開始驅逐現有 Pod。驅逐排序回扣學員 P1 的 QoS 驅逐序:先看「usage 是否超出 requests」再看 QoS,BestEffort 和超額的 Burstable 先走,Guaranteed 和沒超額的最後。
2. **Allocatable**:扣掉 system/kube reserved 後真正能分的量。
3. **Allocated resources**:所有 Pod requests 的加總(scheduler 只看這個,不看真實用量,P1 已打穿)。

Two different killers share this stage, and senior interviews love the distinction. **Kubelet eviction** is a userspace, proactive mechanism: it watches thresholds, ranks victims by QoS and usage over requests, and terminates Pods gracefully; the Pod status shows `Evicted`. The **kernel OOM killer** is the last resort when memory vanishes faster than kubelet can react: it SIGKILLs a process on the spot (exit 137, `OOMKilled`), guided by the `oom_score_adj` values kubelet pre-wrote for each QoS class (5.3). Same goal, different layer, different evidence: eviction leaves a message in `kubectl describe pod` and kubelet logs; the OOM killer leaves its confession in `dmesg`.

kubelet log 在哪看:systemd node 上 `journalctl -u kubelet`;kind 的 node 是 docker container,`docker exec <node名> journalctl -u kubelet | tail -50`;EKS node 用 SSM session 上去同樣 `journalctl -u kubelet`(或 CloudWatch agent 收走後在 console 查)。驅逐事件的 log 長相:`attempting to reclaim memory`、`must evict pod(s) to reclaim memory`。

誘答彈藥(keystone):「Pod 顯示 Evicted 和容器 OOMKilled 是同一回事,都是記憶體不夠被殺,查其中一個就好」。錯:Evicted 是 kubelet 在 userspace 的主動驅逐(graceful、按 QoS+超額排序、證據在 describe pod 和 kubelet log);OOMKilled 是 kernel OOM killer 的 SIGKILL(exit 137、證據在 dmesg)。一個 k8s 層、一個 kernel 層,連查證位置都不同。[RUNTIME: 學員 P1 已分清容器級 vs node 級 OOM,這題往第三層打:node 級裡面還分 kubelet eviction 和 kernel OOM killer 兩條路,對他的用詞精準度弱點正合適。]

### 5.7 60 秒排查清單(Brendan Gregg 風格)

Adapted from Brendan Gregg's "Linux performance analysis in 60 seconds": ten commands, coarse to fine. Run them in order before forming any theory, and let the numbers nominate the suspect; the list exists precisely so you do not jump to the tool that confirms your first guess.

| # | 指令 | 看什麼 |
|---|------|--------|
| 1 | `uptime` | load 三個數字(1/5/15 分)的趨勢:惡化中還是在退燒 |
| 2 | `dmesg -T \| tail -30` | oom-killer、conntrack table full、IO error:kernel 有話要說先聽完 |
| 3 | `vmstat 1 5` | r(CPU 隊)vs b(D state 隊)分流;si/so 有值 = 在 swap;us/sy/id/wa 比例 |
| 4 | `mpstat -P ALL 1 3` | 各核均勻嗎:單核 100% 會被平均值藏掉 |
| 5 | `pidstat 1 3` | 哪個 process 在燒 CPU(可留存的 top 替代品)|
| 6 | `iostat -xz 1 3` | await、aqu-sz 在排隊嗎;%util 語義陷阱見 5.4 |
| 7 | `free -h` | 看 available 不看 free;swap used 有沒有動 |
| 8 | `sar -n DEV 1 3` | NIC 吞吐對頻寬上限;搭 EDEV 看 drop |
| 9 | `sar -n TCP,ETCP 1 3` | active/passive(建線速率)、retrans/s(重傳 = 網路品質或對端滿了)|
| 10 | `top` | 收尾總覽,交叉驗證前九條指認的嫌疑人 |

k8s node 加映三條:`kubectl top node`(水位)、`kubectl describe node`(Conditions + Allocated resources)、`journalctl -u kubelet | tail`(驅逐與 runtime 錯誤)。

[RUNTIME: drill 現場學員卡住時,先讓他跑清單再問「哪一行數字不對勁」,練 evidence-first 的習慣;他先跳結論不講機制是已知弱點模式,別直接餵答案。]

術語卡(2 張):
`load average | /ləʊd ˈævərɪdʒ/ | The average number of tasks either runnable or in uninterruptible (D state) sleep, so it mixes CPU demand with disk/NFS wait. | 排隊的不只 CPU:卡在 D state 等 IO 的也算,高 load 先分流再動手。`
`kubelet eviction | /ˈkjuːblɪt ɪˈvɪkʃən/ | Kubelet's userspace mechanism that reclaims node resources by gracefully terminating Pods, ranked by QoS class and usage over requests. | node 缺資源時 kubelet 先客氣請人走;來不及收的才輪到 kernel OOM killer 動刀。`
