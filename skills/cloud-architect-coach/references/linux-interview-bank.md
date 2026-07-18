# Linux Interview Bank (CA sidecar)

> **用途**：這是課綱的側料 (sidecar),不是 CA 主線。學員是 DevOps,前一份 AWS Support (EC2/Linux) 面試被問到 kernel 深處失分過;ProServe CA loop 的面試官會順著履歷上的 Linux/EC2 經歷往下挖 (resume thread-pull),這份 bank 是那種追問的保險。排課:2 個 session,穿插在 P2/P3 之間,不佔主線時數。
>
> **回答格式**:每題三層,由淺入深。
> - **(1) 指令層**:面試當下先給得出來的操作答案。
> - **(2) 機制層**:再往下一層的原理,答得出這層才叫懂。
> - **(3) 動手驗證**:一條能在機器上跑、親眼看到現象的指令。
>
> 機制層已經寫在 k8s-coach `references/foundations-linux-network.md` 的題目,直接連過去 (§3 TCP、§3.5 conntrack、§4 DNS、§2.4 cgroup OOM),只補雲上的 delta,不重抄。

---

## Priority 0: 上次真實失分題

> 這兩題是學員上一份面試的真實失分點,依 spec 間隔重測兩次,先於 Core 20。

### P0-1. IRQ / hardirq / softirq

- **(1) 指令層**:硬體 (網卡、磁碟) 要 CPU 注意時發 IRQ (中斷)。處理分兩半:hardirq 是「上半部」,越快越好,只做最緊急的事 (收下封包、標記) 就回;剩下的重活丟給 softirq「下半部」在稍後跑。網路收包就跑在 `NET_RX` softirq 這個 context 裡。
- **(2) 機制層**:上半部要關中斷,拖太久會漏掉後續中斷,所以設計上盡量短。網路走 NAPI:第一個封包觸發 hardirq,然後關掉該裝置的中斷、改用 `NET_RX` softirq 用 polling 一次收一批,高流量下避免「一封包一中斷」的風暴 (interrupt storm)。softirq 收完包、過 netfilter,就會碰到學員已經熟的 conntrack 記帳 (foundations §3.5):conntrack 就是在這個 softirq 路徑上被查詢/建立的,所以 `si` (softirq CPU) 飆高常和 conntrack、大量小封包同源。
- **(3) 動手驗證**:`cat /proc/softirqs` 看每顆 CPU 的 `NET_RX`/`NET_TX` 計數 (一直漲代表網路收發壓力);`cat /proc/interrupts | head` 看硬體中斷的分佈,判斷中斷是否集中在單顆核 (IRQ affinity 沒攤開,單核 `si` 100% 會被平均值藏掉,接 foundations §5.2)。

### P0-2. 靜態連結 vs 動態 (共享) library

- **(1) 指令層**:靜態連結 (static) 在 **link time** 把 library 的機器碼整包複製進執行檔,產物大但自帶所有依賴、搬到哪都能跑。動態 (shared) 只在執行檔裡留一個「我需要 libc.so.6」的記號,**load time** 才由 dynamic linker (`ld.so`) 去找、映射進記憶體。`ldd <binary>` 列出一個動態執行檔要載哪些 `.so`。
- **(2) 機制層**:動態連結省磁碟/記憶體 (多個 process 共用同一份 `.so`)、library 修安全漏洞不用重編所有程式;代價是執行時得找得到、且 ABI 要相容。找的順序:`RPATH`/`RUNPATH` → `LD_LIBRARY_PATH` → `ld.so.cache` (`/etc/ld.so.conf`) → 預設路徑。DevOps 最常撞的實體是 **glibc vs musl**:Alpine image 用 musl libc,拿 glibc 環境編的 binary 丟進 Alpine 會 `not found` 或詭異 crash,因為動態依賴的 `.so` 根本不是同一套 C library。所以 Go 靜態編 (`CGO_ENABLED=0`) 的 image 能塞進 `scratch`/`distroless`,就是把動態依賴這條路整個拔掉。
- **(3) 動手驗證**:`ldd /bin/ls` 看它動態依賴哪些 `.so` (會看到 `libc.so.6`、`ld-linux-*.so`)。對照:`file /bin/ls` 顯示 `dynamically linked`;靜態編的 binary 會顯示 `statically linked` 且 `ldd` 回 `not a dynamic executable`。

---

## Core 20 (CA framing)

### A. EC2 系統管理

### 1. EC2 開不了機怎麼查

- **(1) 指令層**:先看 EC2 console 的 system log 和 instance screenshot,判斷卡在哪一環;救不回就把根 volume 卸下、掛到一台 rescue instance 上修 (壞掉的 `/etc/fstab`、GRUB、kernel)。
- **(2) 機制層**:開機鏈 firmware (Nitro/UEFI) → bootloader (GRUB) → kernel → init/systemd。卡在不同環症狀不同:GRUB 沒選單 = bootloader 壞;kernel panic = kernel/initramfs 壞;卡在 systemd 掛載 = `/etc/fstab` 指到不存在的 device 或 UUID (雲上換 volume 後 UUID 變是經典)。
- **(3) 動手驗證**:`aws ec2 get-console-output --instance-id i-xxx` 抓 boot log;`aws ec2 get-console-screenshot --instance-id i-xxx` 抓卡住畫面。

### 2. cloud-init 與 user-data 的時機

- **(1) 指令層**:user-data script 預設只在 instance **第一次 boot** 由 cloud-init 執行一次,不是每次開機都跑。要每次跑得改 cloud-init 設定或自己寫 systemd unit。
- **(2) 機制層**:cloud-init 分階段跑 (init-local → init → config → final),user-data 的 script 落在 final。它靠一個 instance-id 戳記判斷「這台是不是新的」來決定要不要重跑。日誌在 `/var/log/cloud-init.log` (cloud-init 自己) 和 `/var/log/cloud-init-output.log` (你的 script 的 stdout/stderr,debug user-data 看這個)。
- **(3) 動手驗證**:`cloud-init status --long`;`cat /var/log/cloud-init-output.log`。

### 3. EBS 放大了但 df 沒變

- **(1) 指令層**:EBS 卷在 console 放大後,OS 端要兩步:`growpart` 擴分割區,再 `resize2fs` (ext4) 或 `xfs_growfs` (xfs) 擴 filesystem。
- **(2) 機制層**:三層獨立:block device (EBS) → partition table → filesystem。放大 EBS 只改最底層 device 的大小,partition 的邊界和 filesystem 的 superblock 不會自己知道多出來的空間,要逐層往上告知。
- **(3) 動手驗證**:`lsblk` 看 device 已變大、partition 還沒;`growpart /dev/nvme0n1 1` 後 `resize2fs /dev/nvme0n1p1`;`df -h` 確認。

### 4. df 說滿但 du 找不到

- **(1) 指令層**:兩種常見成因。一是 deleted-but-open file:檔案被 `rm` 了但還有 process 開著它,空間沒還 (`lsof +L1` 抓),重啟該 process 或截斷即可回收。二是 inode 耗盡:block 還有空間但 inode 用光,`df -i` 一看便知 (小檔海量的目錄常撞)。
- **(2) 機制層**:`unlink` 只刪掉 directory entry,inode 和它的 data block 要等最後一個開著的 fd 關閉才真正釋放。`df` 讀 filesystem superblock 的記帳 (含這些未釋放的 block),`du` 走 directory tree 加總 (看不到已無目錄項的檔),所以兩者背離。
- **(3) 動手驗證**:`df -h; df -i; lsof +L1`。

### 5. 服務開機自啟 + crash 自動重啟

- **(1) 指令層**:寫 systemd unit,`Restart=on-failure`,`[Install] WantedBy=multi-user.target`,`systemctl enable --now <svc>`。
- **(2) 機制層**:systemd 是 PID 1,用 cgroup 追蹤一個 service 派生的所有 process (所以 stop 能連子孫一起收)。`Restart=` 決定 crash 後行為 (`on-failure`/`always`);`StartLimitBurst`/`StartLimitIntervalSec` 防止壞掉的 service 無限快速重啟 (restart storm) 把機器打爆。
- **(3) 動手驗證**:`systemctl status <svc>`;`journalctl -u <svc> -b` 看這次開機以來的 log。

### 6. SIGTERM vs SIGKILL 與優雅關機

- **(1) 指令層**:SIGTERM (15) 可被 app 攔截,是「請你收尾」;SIGKILL (9) 由 kernel 直接砍,不可攔不可忽略,是「立刻死」。優雅關機要 app 自己在收到 TERM 時停收新請求、排掉手上的、關連線再退。
- **(2) 機制層**:對應到雲上的下線流程。ASG lifecycle hook (`Terminating:Wait`) 給你一段時間 drain;ALB 的 deregistration delay (connection draining) 讓 target 移出後仍等既有連線收尾才真正斷。app 若不接 SIGTERM,這些機制給的時間就白費,連線被硬斷。(容器裡 PID 1 對沒註冊 handler 的訊號直接忽略,見 foundations §2.5。)
- **(3) 動手驗證**:`kill -l` 列訊號編號;shell 裡 `trap 'echo caught TERM' TERM; sleep 60 &` 再 `kill -TERM` 該 pid,觀察被攔截;`kill -9` 則無聲直接死。

### 7. 高並發調優 (ulimit / sysctl)

- **(1) 指令層**:每條連線佔一個 fd,先放大 `ulimit -n` (nofile);accept queue 上限調 `net.core.somaxconn`;來源 port 不夠調 `net.ipv4.ip_local_port_range`。sysctl 讀 `sysctl <key>`,臨時寫 `sysctl -w key=value`,永久寫 `/etc/sysctl.d/*.conf` 再 `sysctl --system`。
- **(2) 機制層**:預設 nofile 常是 1024,高並發 server 一下就撞 `too many open files`。somaxconn 是「握完手等 app accept」的隊伍上限,接 foundations §3.4 的 accept queue (滿了對外吐 502)。這些都是治標的緩衝,真正的病常是 app accept 太慢 (§3.4)。
- **(3) 動手驗證**:`sysctl net.core.somaxconn`;`ulimit -n`;`cat /proc/sys/fs/file-nr` 看全機已開/上限。

### 8. EC2 時間同步

- **(1) 指令層**:用 chrony 對 Amazon Time Sync Service (link-local `169.254.169.123`),不需出網。
- **(2) 機制層**:VM 的時鐘會漂 (host 排程、CPU steal、tickless kernel)。漂掉的後果很實際:TLS 憑證的 notBefore/notAfter 驗證失敗、SigV4 簽章因時間差過大被 AWS 拒 (`RequestTimeTooSkewed`)、跨機 log 時序亂掉查不了案。chrony 比舊的 ntpd 更能快速收斂大偏差。
- **(3) 動手驗證**:`chronyc tracking` (看 offset 和 stratum);`chronyc sources` (確認在對 `169.254.169.123`)。

### 9. IMDS 與為什麼要 IMDSv2

- **(1) 指令層**:instance metadata 在 link-local `169.254.169.254`。IMDSv2 是 session 導向:先 `PUT` 拿一個 token,之後每個 `GET` 都要帶這個 token。
- **(2) 機制層**:IMDSv1 是無認證的純 `GET`,只要能讓 server 幫你發一個 request 到那個 IP,就能撈到掛在該 instance 的 IAM role 臨時憑證 → 這正是 SSRF (Server-Side Request Forgery) 的金礦,一個有 SSRF 漏洞的 app 就能外洩雲憑證。IMDSv2 用「要先 PUT 拿 token」擋掉單純的 GET-based SSRF,再用 token 的 TTL 和預設 hop limit=1 (`X-aws-ec2-metadata-token-ttl-seconds`) 防止 token 被轉發出 instance。
- **(3) 動手驗證**:`TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")` 再 `curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/`。

### B. 效能與排查

### 10. load average 高但 CPU 低

- **(1) 指令層**:load 高、`%CPU` 低 → 十之八九是 iowait / D state (等磁碟或 NFS);在 t 系列 instance 上還要多看一項:CPU credit 是否燒完。
- **(2) 機制層**:load average 算的是 runnable + uninterruptible (D state) 的 task 總數,不是 CPU 忙碌度 (接 foundations §5.2)。一批 process 卡 D state = 底層 IO 出事,加 CPU 沒用。雲上 delta:t2/t3/t4g 是 burstable,CPU credit 耗盡後被降到 baseline，`top` 表頭 `st` (steal) 升高就是被 hypervisor 扣了 CPU。
- **(3) 動手驗證**:`uptime`;`ps -eo state,pid,comm | grep '^D'` 抓 D state 嫌犯;`vmstat 1 3` 看 `r` (CPU 隊) vs `b` (IO 隊)。credit 去 CloudWatch 看 `CPUCreditBalance`。

### 11. free -h 的 buff/cache 不是漏記憶體

- **(1) 指令層**:`buff/cache` 大不代表 leak,那是 page cache,誰要就還誰。判斷記憶體壓力看 `available` 欄,不是 `free` 欄。
- **(2) 機制層**:機制完整寫在 foundations §5.3 (unused RAM is wasted RAM、MemAvailable 的估算)。單機 delta:沒有 cgroup limit 兜著時,是全機視角在搶 page cache,不像容器有 `memory.max` 硬切;真壓力的訊號是 `available` 持續下探 + `vmstat` 的 `si/so` 開始 swap。
- **(3) 動手驗證**:`free -h`;`grep -i avail /proc/meminfo`。

### 12. OOM killer 與洩漏排查

- **(1) 指令層**:先找誰在漲 (RSS 持續成長的 process)、看 `dmesg` 的 oom-killer 段確認是誰被殺、為何被殺;止血手段是加 swap、調 `oom_score_adj`、或修 leak。
- **(2) 機制層**:cgroup 級 OOM (撞 `memory.max`) 的機制連 foundations §2.4。單機視角的 delta:node 級 OOM 掃的是全機記憶體,kernel 依每個 process 的 `oom_score` (受 `oom_score_adj` 加權) 挑犧牲者,和 cgroup 餘量無關;要定位是誰吃記憶體,用 `smaps_rollup` 看單 process 的實際佔用,`free`/`available` 看全機水位。
- **(3) 動手驗證**:`dmesg -T | grep -i -A5 oom-killer`;`cat /proc/<pid>/oom_score`;`grep -i rss /proc/<pid>/smaps_rollup`。

### 13. strace vs lsof vs tcpdump 各看哪一層

- **(1) 指令層**:strace 看 syscall (process 和 kernel 的邊界);lsof 看某 process 開了哪些 fd (檔案、socket、pipe);tcpdump 看實際在網路上跑的封包 (wire)。卡住先問「這是哪一層的問題」再選工具。
- **(2) 機制層**:三者掛在不同觀測點。strace 用 `ptrace` 攔截每個 syscall (代價:目標會變慢,別在 prod 高負載對關鍵 process 亂 attach);lsof 讀 `/proc/<pid>/fd`;tcpdump 用 `AF_PACKET` socket 從 link 層抓封包。app 卡住 → strace 看它卡在哪個 syscall (read? connect? futex?);連不上 → tcpdump 看 SYN 有沒有出去、有沒有回。
- **(3) 動手驗證**:`strace -f -e trace=network -p <pid>`;`lsof -p <pid>`;`tcpdump -i any -nn port 443 -c 5`。

### C. 網路 (單機接雲層)

### 14. Connection Refused vs Timeout

- **(1) 指令層**:Refused = 對方那個 port 沒人在聽,kernel 立刻回 RST,失敗得很快;Timeout = 封包石沉大海 (雲上 SG 靜默丟包、沒有路由、或 app 收了不回),要等到逾時。快慢就是第一個線索。
- **(2) 機制層**:OS 層,收到打到「沒有 listener 的 port」的封包,kernel 回 RST → 對端 `connect()` 立即拿到 `ECONNREFUSED`。雲層,Security Group 是 stateful allow-list,不在允許清單的封包直接丟棄、**不回 RST**,所以症狀是 timeout 而非 refused (NACL deny 同樣是丟)。這個「refused 快、SG 丟包慢」的對照能直接把嫌疑分到 OS 還是雲設定。(對照 foundations §4.6 解析層 vs 連線層的分界。)
- **(3) 動手驗證**:`nc -zv <host> <port>` 或 `curl -v telnet://<host>:<port>`,看是即時 refused 還是掛著 timeout。

### 15. SG vs NACL 的 stateful 差異 = conntrack

- **(1) 指令層**:Security Group 是 stateful (放行一個方向,回程自動放行);NACL 是 stateless (進、出要各自開規則,回程得手動放行 ephemeral port range 1024-65535)。
- **(2) 機制層**:SG 的 stateful 本質就是雲版的 conntrack (連線記帳本),機制完整寫在 foundations §3.5。雲上 delta:SG 因為有這本帳,你只寫「允許 443 進」它就記得這條連線、自動放回程;NACL 沒有這本帳,每個封包獨立判斷,所以才要你把回程的高位 port 手動開出來。忘了開回程 ephemeral range 是 NACL 的經典坑。
- **(3) 動手驗證**:概念題為主。本機類比 conntrack 記帳本:`conntrack -L | head` (需 `conntrack-tools`),看 kernel 怎麼記住雙向連線。

### 16. TCP 三次握手 + TCP vs UDP 的取捨

- **(1) 指令層**:三次握手 SYN → SYN+ACK → ACK 建連 (狀態轉移完整見 foundations §3.1)。TCP 可靠、有序、有壅塞控制,代價是握手與狀態成本;UDP 無連線、無保證、輕量。
- **(2) 機制層**:狀態機接 foundations §3,這裡補 when-to-choose 這層。選 UDP 的場景:能容忍或自建可靠層的,如 DNS 查詢 (一來一回,重試比握手便宜)、即時音視訊 (遲到的封包不如丟掉)、QUIC/HTTP3 (在 UDP 上自己實作更好的壅塞控制與 0-RTT)。選 TCP:要求可靠有序的檔案傳輸、一般 API。面試想聽你講出「為什麼這個場景寧可 UDP」,不是背定義。
- **(3) 動手驗證**:`ss -tan state established | head` 看 TCP 連線;`ss -uan` 看 UDP socket。

### 17. Routing:主機的 ip route 與其上的 VPC route table

- **(1) 指令層**:本機 `ip route` 看 routing table,`default via <gw>` 是預設閘道;封包出了本機之後,還有 VPC route table 這一層決定它去哪。
- **(2) 機制層**:兩層路由疊起來。封包先在本機查 routing table,longest-prefix match 決定走哪個介面、下一跳給誰。進了 VPC,封包所屬 subnet 綁的 route table 再決定去 IGW (公網)、NAT gateway (私網出網)、TGW、或 VPC peering。「instance 出得去嗎」這問題要兩層都查:本機 default route 對不對 + subnet route table 有沒有那條路。
- **(3) 動手驗證**:`ip route get 8.8.8.8` (看這個目的地會走哪條路、哪個介面);`ip route` 看整張表。

### 18. DNS 解析路徑 + VPC 裡誰回答

- **(1) 指令層**:app 照 `/etc/resolv.conf` 問 stub resolver → recursive resolver → 一路 root/TLD/authoritative (完整路徑見 foundations §4.1)。在 VPC 裡,預設回答的是 AmazonProvidedDNS。
- **(2) 機制層**:一般遞迴路徑接 foundations §4。雲上 delta:VPC 內建的 DNS resolver 固定在 VPC CIDR 的 base +2 (例如 `10.0.0.0/16` 就是 `10.0.0.2`),也叫 `.2 resolver`;instance 的 resolv.conf 預設指向它。它幫你遞迴解外部名字、也回答 private hosted zone 的內部名字;要和 on-prem 互解 (hybrid) 就靠 Route 53 Resolver inbound/outbound endpoint。DNS 出事的解析層 vs 連線層分界見 foundations §4.6。
- **(3) 動手驗證**:`cat /etc/resolv.conf` (看 nameserver 是不是 `.2`);`dig +trace example.com` 看逐層遞迴。

### 19. TLS 握手與憑證鏈驗證

- **(1) 指令層**:ClientHello/ServerHello 協商 TLS 版本與 cipher suite → server 送憑證鏈 → client 驗證憑證 → 交換金鑰 → 之後切成對稱加密傳資料。
- **(2) 機制層**:憑證鏈驗證 = 從 server 的 leaf 憑證,靠每張憑證上的簽章,一路往上驗到本機 trust store 裡信任的 root CA;同時檢查 hostname 在不在 SAN、有沒有過期、有沒有被撤銷 (CRL/OCSP)。TLS 1.3 把握手壓成 1-RTT。常見雷:少裝中間 CA (intermediate) → 鏈斷;或機器時鐘錯 (見第 8 題) → 憑證被判「還沒生效/已過期」而驗證失敗。
- **(3) 動手驗證**:`openssl s_client -connect <host>:443 -servername <host> </dev/null | openssl x509 -noout -dates -subject -issuer`。

### 20. MTU 9001 vs 1500 與 PMTUD 黑洞

- **(1) 指令層**:VPC 內部支援 jumbo frame (MTU 9001),但一出 IGW、或跨 VPN/DX 的某些路徑會降到 1500。MTU 不匹配、又剛好有防火牆擋掉關鍵 ICMP,就會出現 PMTUD 黑洞:小封包 (ping、握手) 通,大封包 (實際 payload) 無聲卡住。
- **(2) 機制層**:封包設了 DF (Don't Fragment) bit 又超過路徑上某段 MTU 時,那台設備該回一個 ICMP `type 3 code 4` (fragmentation needed) 告訴來源「縮小封包」,這就是 Path MTU Discovery。若 SG/NACL/防火牆把這個 ICMP 擋掉,大封包被丟又沒人通知來源 → 連線建得起來、一傳大資料就 hang。症狀:SSH 登入 OK 但 `ls` 大輸出卡死、TLS 握手成功但傳 body 逾時。
- **(3) 動手驗證**:`ip link show eth0 | grep -o 'mtu [0-9]*'` 看本機 MTU;`ping -M do -s 1472 <host>` 帶 DF 打滿 1500 (1472 payload + 8 ICMP + 20 IP),不通就縮 `-s` 找出真正能過的 Path MTU。

---

## Appendix: Support-loop 逐字稿原題 (降權)

> 這些是本 bank 作者當年真實 AWS Support 面試的逐字稿原題,保留做覆蓋率盤點用,**只列題目、不寫答案**:能力點多半已被上面 Core 20 或 foundations 涵蓋,重演時直接指過去。降權原因:CA loop 的重心在架構與客戶對話,這批純 Linux 事實題只在履歷被 thread-pull 時才會碰到。

- 查 kernel / shell 版本 (`uname -r`、`echo $SHELL`)。→ 對照 P0-2 動態連結、Core #1 開機鏈。
- `chmod` 與 755 是什麼意思 (rwx 三組、owner/group/other)。
- 為什麼對目錄要加 `-R` (遞迴)。
- `/etc/hosts` 的角色與它在解析路徑裡的位置。→ foundations §4。
- `/etc/fstab` 自動掛載的欄位含義。→ Core #1 (fstab 壞導致開不了機)。
- LVM 是什麼、好處、擴充流程。→ Core #3 (層層擴容的同構思路)。
- 怎麼讀 `df -h`。→ Core #4。
- 不刪資料就把空間放大。→ Core #3。
- `sysctl` 怎麼看/改 (TCP 記憶體、open-file limit)。→ Core #7。
- 完整開機到 login 的順序。→ Core #1、foundations §2.5 (PID 1)。
- 為什麼 BIOS 交棒給 GRUB、GRUB 的工作是什麼。→ Core #1。
- TCP vs UDP。→ Core #16、foundations §3。
- 三次握手與逾時行為。→ Core #16、foundations §3.1、§3.4。
- `route` / `netstat` 看 routing table。→ Core #17 (現代用 `ip route` / `ss`)。
- ping 觸發的 DNS 路徑、`resolv.conf`、`8.8.8.8` 怎麼運作。→ Core #18、foundations §4。
- OOM killer 的成因與止血。→ Core #12、foundations §2.4、§5.3。
- crash 後該看哪些 log (`/var/log/messages`、syslog) 與 `journalctl` 用法。→ Core #5 (`journalctl -u`)。
- 服務停掉時 Connection Refused 的機制。→ Core #14。
