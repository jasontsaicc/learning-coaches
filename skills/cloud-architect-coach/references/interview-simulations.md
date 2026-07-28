# Interview Simulations (面試模擬素材)

> **用途**:每題三段:(A) 面試官怎麼問 (中英對照)、(B) 口語組織骨架、(C) L6 model answer (英文版 + 中文版)。對應 2026-07-29 的 input-first 語言改制 (見 `language.md`):學員答題用中文,英文版 model answer 當朗讀 / shadowing 的 input 素材,中文版是實際答題的目標形狀,術語一律留英文。
>
> **揭示順序 (coach 執行,不可跳)**:先用 (A) 提問 (預設英文問、中文重述一次) → 學員先自己答 (中文即可) → Feynman Gate 判定 → 才揭 (B) 骨架讓他重組一次 → 最後揭 (C):先朗讀英文版,再對照中文版收斂自己的講法。先看答案再答的,該題記 recognition-level,不算 pass。
>
> **覆蓋率**:全題庫收錄 (P0-1、P0-2、Core #1-20、#21-28 共 30 題),依題庫編號排序。新題目進 bank 時,本檔同步補模擬。

## 通用 30 秒骨架

面試口語答題的預設結構,四步,每步一兩句:

1. **一句定位**:這東西是什麼、解什麼問題。
2. **機制往下一層**:挑一條最核心的 how,不要全倒。
3. **實戰落點**:一個你真的操作過的例子或指令 (雲上場景加分)。
4. **停**:收尾丟一個鉤子 ("...which is why we usually see X"),讓面試官挑方向追問。不停等於自曝短板。

---

## SIM P0-1: IRQ / hardirq / softirq

**(A) 面試官怎麼問** (resume thread-pull 的自然入口,不會直接問名詞定義):

> EN: "I see you've handled EC2 performance issues. Here's one: a customer's instance shows low user CPU but one core is pegged at 100% softirq during traffic spikes, and latency goes up. Walk me through what's happening."
>
> 中文:「你履歷上處理過 EC2 效能問題。來一題:customer 的 instance 在流量尖峰時 user CPU 很低,但有一顆核的 softirq 打滿 100%,latency 跟著上升。帶我走一遍發生了什麼事。」

追問串:

- "What's the difference between the top half and bottom half of interrupt handling?"(中斷處理的上半部和下半部差在哪?)
- "Why doesn't Linux just handle everything in the interrupt handler?"(為什麼 Linux 不乾脆全部在 interrupt handler 裡做完?)
- "How would you confirm this on a live box?"(在一台跑著的機器上你怎麼證實這個判斷?)

**(B) 口語組織骨架**:

1. 定位:IRQ 是硬體叫 CPU 注意的機制;處理切兩半,hardirq 極短、softirq 扛重活。
2. 機制:hardirq 期間中斷是關的,拖久會漏事件,所以只收下、標記、排程;網路收包的重活跑在 NET_RX softirq,高流量下 NAPI 關掉逐包中斷改 polling。
3. 落點:`si` 高 + 單核打滿 = IRQ affinity 沒攤開;看 `/proc/softirqs` 和 `/proc/interrupts`。
4. 鉤子:單核瓶頸會被 CPU 平均值藏掉,所以要逐核看。

**(C) L6 model answer**:

英文版 (朗讀 / shadowing 用):

> "An interrupt is how hardware gets the CPU's attention. When a packet arrives, the NIC raises a hardware interrupt, and Linux splits the handling into two halves. The top half, the hardirq, runs with interrupts disabled, so it does the bare minimum: acknowledge the device and schedule the rest. The heavy lifting, pushing packets through the network stack, happens later in softirq context, that's the NET_RX you see. Under high traffic, the kernel switches to NAPI: it disables per-packet interrupts and polls in batches, otherwise you'd get an interrupt storm. So in this case, high softirq on one core tells me packet processing is pinned there, likely IRQ affinity isn't spread out. I'd check /proc/softirqs and /proc/interrupts per core, because a single saturated core hides behind a healthy CPU average."

中文版 (實際答題的目標形狀,術語留英文):

> 「Interrupt 就是硬體叫 CPU 注意的機制。封包到了,網卡發一個 hardware interrupt,Linux 把處理切成兩半:上半部 hardirq 是在關中斷的狀態下跑的,所以只做最少的事,跟裝置確認、把後續排程好就結束;真正的重活,把封包推過整個 network stack,是之後在 softirq context 裡做的,也就是你看到的 NET_RX。流量大的時候 kernel 會切到 NAPI:把逐包的 interrupt 關掉、改成批次 polling,不然會 interrupt storm。所以這個案例裡,一顆核 softirq 打滿,代表封包處理被釘在那顆核上,多半是 IRQ affinity 沒攤開。我會逐核去看 /proc/softirqs 跟 /proc/interrupts,因為單核飽和會被整機的 CPU 平均值藏掉。」

關鍵句型:"the top half does the bare minimum" / "the heavy lifting happens in softirq context" / "hides behind a healthy average"。

---

## SIM P0-2: 靜態連結 vs 動態 (共享) library

**(A) 面試官怎麼問** (從 container 經驗切入的 thread-pull):

> EN: "Your resume mentions building container images. Here's a classic: a binary built on Amazon Linux gets dropped into an Alpine image and fails with 'not found', even though the file is clearly right there. What's going on?"
>
> 中文:「你履歷上有做 container image。來個經典題:一個在 Amazon Linux 上編好的 binary 丟進 Alpine image,報 not found,但檔案明明就在那裡。發生了什麼事?」

追問串:

- "What's the actual difference between static and dynamic linking?"(static 和 dynamic linking 實際差在哪?)
- "What are the tradeoffs, why not just link everything statically?"(trade-off 是什麼?為什麼不全部 static?)
- "Why can a Go binary run in a scratch image with nothing else in it?"(為什麼 Go binary 可以跑在什麼都沒有的 scratch image 裡?)

**(B) 口語組織骨架**:

1. 定位:linking 決定 library 的機器碼什麼時候黏進來,static 是 link time 整包複製,dynamic 是 load time 由 `ld.so` 去找。
2. 機制:not found 報的不是你的 binary,是它指定的 interpreter/`.so` 不存在;Alpine 用 musl 不是 glibc。
3. 落點:`ldd` 看依賴;Go `CGO_ENABLED=0` 全靜態,所以能塞 scratch/distroless。
4. 鉤子:dynamic 的真正好處是補 CVE 只補一份 `.so`,不用重編所有程式。

**(C) L6 model answer**:

英文版:

> "Linking decides when library code gets glued into your program. Static linking copies the machine code into the binary at link time, so it's bigger but self-contained. Dynamic linking only records a dependency, 'I need libc.so.6', and at load time the dynamic linker, ld.so, finds it and maps it in. That Alpine failure is the classic symptom: the error isn't about your file, it's about the loader. Alpine ships musl instead of glibc, so the interpreter path baked into the binary points at something that doesn't exist. You can see all of this with ldd. The tradeoff: shared libraries save disk and memory and let you patch a CVE in one place without rebuilding every program, but you take on ABI compatibility risk at runtime. That's exactly why Go builds with CGO_ENABLED=0 are so popular in containers: fully static, so they run in scratch or distroless with no C library at all."

中文版:

> 「Linking 決定 library 的程式碼什麼時候黏進你的程式。Static linking 在 link time 就把機器碼整包複製進 binary,產物大但自帶所有依賴;dynamic linking 只留一個依賴記號,『我需要 libc.so.6』,load time 才由 dynamic linker,就是 ld.so,去找到並映射進來。Alpine 那個錯是經典症狀:報錯的不是你的檔案,是 loader。Alpine 用的是 musl 不是 glibc,binary 裡寫死的 interpreter 路徑指向一個不存在的東西。用 ldd 就能看到這整串依賴。Trade-off 是:shared library 省磁碟省記憶體,補一個 CVE 只要換一份 .so,不用重編所有程式;代價是 runtime 的 ABI 相容風險。這也是為什麼 Go 用 CGO_ENABLED=0 編出來的 binary 在 container 圈這麼受歡迎:完全 static,丟進 scratch 或 distroless 都能跑,連 C library 都不需要。」

關鍵句型:"the error isn't about your file, it's about the loader" / "patch a CVE in one place" / "fully static, so it runs in scratch"。

---

## SIM #1: EC2 開不了機怎麼查

**(A) 面試官怎麼問**:

> EN: "A customer patched the kernel on an EC2 instance, rebooted, and now it's unreachable: SSH times out, status check fails. There's no physical console to walk up to. How do you troubleshoot?"
>
> 中文:「customer 幫 EC2 更新了 kernel,重開機之後就連不上了:SSH timeout,status check 失敗。這台又沒有實體 console 可以走過去看。你怎麼查?」

追問串:

- "The console output shows a kernel panic. Now what?"(console output 顯示 kernel panic,接下來呢?)
- "How would a wrong /etc/fstab entry produce the same symptom?"(/etc/fstab 寫錯怎麼也會造成一樣的症狀?)
- "Walk me through the boot chain so I know you know where it can break."(把開機鏈走一遍,讓我知道你清楚它可能斷在哪。)

**(B) 口語組織骨架**:

1. 定位:連不上 ≠ 沒開機,先用 console output 和 screenshot 定位卡在開機鏈哪一環。
2. 機制:開機鏈 firmware (Nitro/UEFI) → GRUB → kernel → systemd,每環症狀不同:GRUB 壞沒選單、kernel panic、fstab 指到不存在的 UUID 卡在掛載。
3. 落點:救法是把 root volume 卸下、掛到 rescue instance 修 (GRUB、fstab、換回舊 kernel),修完掛回去。
4. 鉤子:雲上換 volume 後 UUID 變是 fstab 的經典雷。

**(C) L6 model answer**:

英文版:

> "With no physical console, my eyes are the EC2 console output and the instance screenshot, so I'd pull those first to localize where boot stopped. The boot chain is firmware, then GRUB, then the kernel, then systemd, and each stage fails differently: no GRUB menu means the bootloader is broken, a kernel panic points at the new kernel or initramfs, and hanging at mount time usually means /etc/fstab references a device or UUID that no longer exists. Since they just patched the kernel, my first hypothesis is a bad kernel or initramfs. The recovery path is the cloud version of pulling the disk: stop the instance, detach the root volume, attach it to a rescue instance, then either point GRUB back at the previous kernel or fix fstab, and reattach. And to make this a consulting answer: I'd tell the customer to bake AMIs and roll forward instead of patching in place, so a bad kernel becomes a rollback, not an outage."

中文版:

> 「沒有實體 console,我的眼睛就是 EC2 console output 和 instance screenshot,先抓這兩個,定位開機停在哪一環。開機鏈是 firmware → GRUB → kernel → systemd,每一環壞法不一樣:GRUB 選單出不來是 bootloader 壞;kernel panic 指向新 kernel 或 initramfs;卡在掛載通常是 /etc/fstab 指到一個已經不存在的 device 或 UUID。既然他剛更新 kernel,第一個假設就是 kernel 或 initramfs 壞了。救援路徑等於雲版的拔硬碟:停機、把 root volume 卸下、掛到一台 rescue instance,把 GRUB 指回舊 kernel 或把 fstab 修好,再掛回去。最後補一句 consultant 視角:我會建議 customer 改用 bake AMI、roll forward 的方式更新,這樣壞 kernel 是一次 rollback,不是一次 outage。」

關鍵句型:"my eyes are the console output" / "each stage fails differently" / "a rollback, not an outage"。

---

## SIM #2: cloud-init 與 user-data 的時機

**(A) 面試官怎麼問**:

> EN: "A customer put their bootstrap script in user-data. It worked on launch. Later they updated the script and rebooted the instance, and nothing happened. Why?"
>
> 中文:「customer 把 bootstrap script 放在 user-data,launch 的時候跑得好好的。後來他改了 script、把 instance 重開機,結果什麼都沒發生。為什麼?」

追問串:

- "How does cloud-init decide whether to run user-data?"(cloud-init 怎麼判斷要不要跑 user-data?)
- "Where do you look when a user-data script fails silently?"(user-data script 無聲失敗時你去哪裡看?)
- "What would you use instead if something must run on every boot?"(如果有東西每次開機都要跑,你會改用什麼?)

**(B) 口語組織骨架**:

1. 定位:user-data 預設只在第一次 boot 跑一次,reboot 不會重跑,這是設計不是 bug。
2. 機制:cloud-init 分階段 (init-local → init → config → final),user-data 落在 final;靠 instance-id 戳記判斷「是不是新機器」。
3. 落點:debug 看 `/var/log/cloud-init-output.log` (script 的 stdout/stderr);每次都要跑的東西寫 systemd unit。
4. 鉤子:「script 改了為什麼沒生效」是 support ticket 的常客,一句 per-instance semantics 就講穿。

**(C) L6 model answer**:

英文版:

> "That's by design. User-data runs once per instance, not once per boot. Cloud-init stamps the instance ID the first time it runs, and on every later boot it sees the same ID and skips the per-instance modules, which is where user-data lives. So editing the script and rebooting does nothing, the instance is not 'new' in cloud-init's eyes. For debugging, there are two logs: cloud-init.log is cloud-init's own execution, and cloud-init-output.log captures the stdout and stderr of your actual script, that's the one you usually want. If something genuinely needs to run on every boot, user-data is the wrong tool, I'd write a systemd unit, or explicitly mark the cloud-init module to run per-boot. And the pattern behind the question: launch-time bootstrap belongs in the AMI or user-data, recurring config belongs to the OS's own service manager."

中文版:

> 「這是設計,不是 bug。user-data 是 once per instance,不是 once per boot。cloud-init 第一次跑的時候會記下 instance-id,之後每次開機看到同一個 id,就跳過 per-instance 的模組,而 user-data 正好住在那裡。所以改了 script 再 reboot 什麼都不會發生,對 cloud-init 來說這台不是新機器。debug 有兩個 log:cloud-init.log 是 cloud-init 自己的執行紀錄,cloud-init-output.log 收你 script 的 stdout 和 stderr,通常要看的是後者。真的需要每次開機都跑的東西,user-data 是錯的工具,我會寫 systemd unit,或把該模組明確設成 per-boot。這題背後的 pattern 是:launch 時的 bootstrap 屬於 AMI 或 user-data,重複性的設定屬於 OS 自己的 service manager。」

關鍵句型:"once per instance, not once per boot" / "not 'new' in cloud-init's eyes" / "the wrong tool for recurring config"。

---

## SIM #3: EBS 放大了但 df 沒變

**(A) 面試官怎麼問**:

> EN: "A customer resized an EBS volume from 100 to 500 gigs in the console. df still says 100 and the disk is filling up. Talk me through what's missing."
>
> 中文:「customer 在 console 把 EBS volume 從 100G 放大到 500G,df 還是顯示 100G,磁碟快滿了。跟我講一遍還缺什麼。」

追問串:

- "Why doesn't the filesystem just see the new space automatically?"(為什麼 filesystem 不會自動看到新空間?)
- "What's different between ext4 and xfs here?"(ext4 和 xfs 在這裡差在哪?)
- "Can you do all of this online, or does it need downtime?"(這些能 online 做完嗎,還是要停機?)

**(B) 口語組織骨架**:

1. 定位:三層各自獨立:block device (EBS) → partition table → filesystem,放大只動了最底層。
2. 機制:partition 的邊界和 filesystem 的 superblock 不會自己知道下面變大了,要逐層往上告知。
3. 落點:`lsblk` 看斷層在哪,`growpart` 擴分割區,`resize2fs` (ext4) 或 `xfs_growfs` (xfs) 擴 filesystem,全程 online。
4. 鉤子:同一個「逐層擴」心智模型直接遷移到 LVM。

**(C) L6 model answer**:

英文版:

> "There are three independent layers here: the block device, the partition table, and the filesystem. Resizing in the console only grew the bottom layer, the EBS device. The partition still ends at its old boundary, and the filesystem's superblock still records the old size, neither of them gets notified automatically, you have to grow each layer up the stack. So: lsblk first, and you'll literally see the gap, a 500-gig device with a 100-gig partition on it. Then growpart to extend the partition, then the filesystem tool, resize2fs for ext4 or xfs_growfs for xfs, note that xfs_growfs takes the mount point, not the device. All of this is online on modern kernels, no downtime. The same mental model carries to LVM: physical volume, volume group, logical volume, filesystem, whenever storage grows, you walk each layer and tell it explicitly."

中文版:

> 「這裡有三層各自獨立的東西:block device、partition table、filesystem。console 上的 resize 只放大了最底層,EBS device 本身。partition 還停在舊的邊界,filesystem 的 superblock 也還記著舊的大小,它們不會被自動通知,要一層一層往上擴。所以先 lsblk,你會直接看到斷層:一個 500G 的 device 上面掛著 100G 的 partition。接著 growpart 擴分割區,再用 filesystem 的工具,ext4 是 resize2fs,xfs 是 xfs_growfs,注意 xfs_growfs 吃的是 mount point 不是 device。現代 kernel 上這整套都是 online 的,不用停機。同一個心智模型直接搬到 LVM:PV、VG、LV、filesystem,storage 一變大,就是逐層走上去、明確告訴每一層。」

關鍵句型:"three independent layers" / "neither gets notified automatically" / "walk each layer and tell it explicitly"。

---

## SIM #4: df 說滿但 du 找不到

**(A) 面試官怎麼問**:

> EN: "df reports the disk 95% full, but when the customer runs du over the whole filesystem it only accounts for 40%. Where did the space go?"
>
> 中文:「df 說磁碟用了 95%,但 customer 對整個 filesystem 跑 du,加起來只有 40%。空間跑去哪了?」

追問串:

- "Why does deleting a log file sometimes free no space?"(為什麼有時候刪了 log 檔,空間卻沒回來?)
- "What's the other classic cause, when df shows space free but writes still fail?"(另一個經典成因是什麼,df 明明有空間但寫入還是失敗?)
- "How do you recover without bouncing the whole service?"(不重啟整個 service 的話怎麼回收?)

**(B) 口語組織骨架**:

1. 定位:兩個帳本不一樣:df 讀 superblock 的記帳,du 走 directory tree 加總,兩者背離就是有檔案「沒有目錄項但還活著」。
2. 機制:`unlink` 只刪 directory entry,inode 和 data block 要等最後一個開著的 fd 關掉才釋放;deleted-but-open 的檔 du 看不到、df 算得到。
3. 落點:`lsof +L1` 抓元兇,truncate 或重啟該 process 回收;另一款是 inode 耗盡,`df -i` 一看便知。
4. 鉤子:最常見的真實案例就是 rm 掉一個正被寫的大 log。

**(C) L6 model answer**:

英文版:

> "df and du keep different books. df reads the filesystem superblock's accounting, du walks the directory tree and adds up what it can see. When they disagree like this, there's almost always a deleted-but-open file: someone removed a large log while a process still had it open. Unlink only removes the directory entry, the inode and its data blocks aren't freed until the last open file descriptor closes. So du can't see it anymore, but df still counts it. I'd run lsof +L1, which lists open files with zero links, find the process, and either truncate the file or restart that one process, no need to bounce the box. The other classic with a similar smell is inode exhaustion: df -h shows free blocks but writes fail, and df -i shows inodes at 100%, usually a directory with millions of tiny files. Either way, the fix for the log case long-term is logrotate with copytruncate or a proper reopen signal."

中文版:

> 「df 和 du 記的是兩本不同的帳。df 讀 filesystem superblock 的記帳,du 是走 directory tree 把看得到的加總。兩者差這麼多,幾乎一定是 deleted-but-open:有人把一個大 log 刪了,但還有 process 開著它。unlink 只刪掉 directory entry,inode 和 data block 要等最後一個開著的 fd 關閉才真正釋放,所以 du 看不到它了,df 還算著它。我會跑 lsof +L1,列出 link 數為零但還開著的檔,找到那個 process,把檔案 truncate 掉或只重啟那一個 process,不用動整台機器。另一個症狀很像的經典是 inode 耗盡:df -h 明明有空間但寫入失敗,df -i 一看 inode 100%,通常是某個目錄塞了幾百萬個小檔。log 這個案例的長期解是 logrotate 配 copytruncate 或正確的 reopen signal。」

關鍵句型:"df and du keep different books" / "deleted but still open" / "no need to bounce the box"。

---

## SIM #5: 服務開機自啟 + crash 自動重啟

**(A) 面試官怎麼問**:

> EN: "A customer's app on EC2 dies every few days and an engineer SSHes in to restart it manually. As their consultant, what's the right fix, and how does it actually work underneath?"
>
> 中文:「customer 的 app 在 EC2 上每隔幾天就掛掉,工程師都是 SSH 進去手動重啟。你是 consultant,正確的解法是什麼?底層又是怎麼運作的?」

追問串:

- "How does systemd know the service died, and how does it kill all its children on stop?"(systemd 怎麼知道 service 死了?stop 的時候怎麼連子 process 一起收乾淨?)
- "What stops a crashing service from restart-looping the machine to death?"(一個一直 crash 的 service,靠什麼避免無限重啟把機器打爆?)
- "Where do you look for why it keeps dying?"(它一直死的原因你去哪裡查?)

**(B) 口語組織骨架**:

1. 定位:手動重啟是 toil,正解是 systemd unit:`Restart=on-failure` + `enable` 開機自啟。
2. 機制:systemd 是 PID 1,用 cgroup 追蹤 service 派生的所有 process,所以偵測得到死亡、stop 也收得乾淨。
3. 落點:`StartLimitBurst`/`StartLimitIntervalSec` 防 restart storm;`journalctl -u <svc> -b` 查死因。
4. 鉤子:auto-restart 是止血,root cause (crash 本身) 還是要查,不然是把 pager 靜音而已。

**(C) L6 model answer**:

英文版:

> "Manual restarts are toil, so the right fix is to make the service manager own the lifecycle: a systemd unit with Restart=on-failure and an Install section, then systemctl enable --now. Underneath, systemd is PID 1 and it puts every service into its own cgroup, that's how it reliably tracks all the processes the service forks, knows when the main one exits, and can kill the whole group cleanly on stop, no orphans. Two details separate a junior from a senior answer here: first, StartLimitBurst and StartLimitInterval, so a service that's crashing instantly doesn't restart-loop and burn the box; second, auto-restart is mitigation, not a fix. I'd pull journalctl -u for the unit, find why it dies every few days, memory leak, unhandled error, whatever it is, because otherwise we've just muted the pager. On AWS I'd also point out: if this app matters, one instance with auto-restart is still one instance, the real answer is an ASG behind a health check."

中文版:

> 「手動重啟是 toil,正解是把生命週期交給 service manager:寫一個 systemd unit,Restart=on-failure,加 Install 段,然後 systemctl enable --now。底層機制是:systemd 是 PID 1,它把每個 service 放進自己的 cgroup,所以它能可靠追蹤 service fork 出去的所有 process,主程序退了它知道,stop 的時候也能把整組收乾淨,不留孤兒。這題 junior 和 senior 的分水嶺在兩個細節:第一,StartLimitBurst 和 StartLimitInterval,避免一個秒 crash 的 service 無限重啟把機器打爆;第二,auto-restart 是止血不是治病,我會用 journalctl -u 去查它每隔幾天死一次的原因,memory leak 也好、沒接的 error 也好,不查就只是把 pager 靜音了。AWS 視角再補一句:這個 app 如果重要,一台機器加 auto-restart 還是一台機器,真正的答案是 health check 後面掛 ASG。」

關鍵句型:"make the service manager own the lifecycle" / "mitigation, not a fix" / "we've just muted the pager"。

---

## SIM #6: SIGTERM vs SIGKILL 與優雅關機

**(A) 面試官怎麼問**:

> EN: "During Auto Scaling scale-in, a customer sees dropped requests and half-finished jobs. Walk me through graceful shutdown, from the process level all the way up to the load balancer."
>
> 中文:「Auto Scaling scale-in 的時候,customer 觀察到掉請求、工作做到一半被砍。從 process 層一路到 load balancer,把 graceful shutdown 講一遍。」

追問串:

- "What's the actual difference between SIGTERM and SIGKILL?"(SIGTERM 和 SIGKILL 實際差在哪?)
- "The app ignores SIGTERM. What happens to all these AWS draining features?"(app 沒接 SIGTERM 的話,AWS 這些 draining 機制會怎樣?)
- "Which AWS knobs are involved and in what order do they fire?"(牽涉到哪些 AWS 設定?它們的先後順序是什麼?)

**(B) 口語組織骨架**:

1. 定位:graceful shutdown 是三層的合作:LB 停止送新流量 → app 收尾 → 才真正終止。
2. 機制:SIGTERM 可被攔截,是「請收尾」;SIGKILL 由 kernel 直接砍,不可攔。app 要在 TERM 時停收新請求、排空手上的、關連線。
3. 落點:ALB deregistration delay 讓既有連線收尾,ASG lifecycle hook (`Terminating:Wait`) 給 drain 時間。
4. 鉤子:app 不接 TERM,整條鏈給的時間全白費,這是最常見的斷點。

**(C) L6 model answer**:

英文版:

> "Graceful shutdown is a three-party contract: the load balancer stops sending new work, the app finishes what it holds, and only then does the process die. At the bottom, the difference between the signals: SIGTERM is catchable, it's the polite 'please wrap up', the app's handler should stop accepting, drain in-flight requests, close connections, and exit. SIGKILL never reaches the process, the kernel just tears it down, so nothing gets to clean up. On AWS the sequence is: scale-in triggers target deregistration, the ALB's deregistration delay keeps existing connections alive while new ones stop; an ASG lifecycle hook in Terminating:Wait gives the instance a window to drain before termination proceeds. And here's the failure mode in this ticket: if the app never handles SIGTERM, all of that machinery buys nothing, the delay expires and connections get cut anyway. So my first check is literally whether the app has a TERM handler, that's the weakest link far more often than the AWS config."

中文版:

> 「graceful shutdown 是三方合約:load balancer 停止送新流量、app 把手上的做完、然後 process 才真正死。最底層是兩個 signal 的差別:SIGTERM 可以被攔截,是『請你收尾』,app 的 handler 應該停收新請求、排空 in-flight、關連線、退出;SIGKILL 根本到不了 process,kernel 直接拆掉,什麼清理都做不了。AWS 上的順序是:scale-in 觸發 target deregistration,ALB 的 deregistration delay 讓既有連線活著收尾、新連線不再進來;ASG 的 lifecycle hook 進 Terminating:Wait,給 instance 一段 drain 的時間窗才繼續終止。而這張 ticket 的 failure mode 就在:app 沒接 SIGTERM 的話,上面整套機制買到的時間全部白費,delay 一到連線照樣被硬斷。所以我第一件事就是查 app 到底有沒有 TERM handler,斷點在這裡的頻率遠高於 AWS 設定。」

關鍵句型:"a three-party contract" / "SIGKILL never reaches the process" / "all that machinery buys nothing"。

---

## SIM #7: 高並發調優 (ulimit / sysctl)

**(A) 面試官怎麼問**:

> EN: "A customer's load test hits a wall at a few thousand concurrent connections. Errors say 'too many open files', and later they see connection resets under burst. Which OS knobs matter here, and what do they actually control?"
>
> 中文:「customer 的 load test 卡在幾千個並發連線就上不去,錯誤是 too many open files,burst 的時候還會看到 connection reset。哪些 OS 參數有關?它們各自控制什麼?」

追問串:

- "Why does every connection consume a file descriptor?"(為什麼每條連線都吃一個 file descriptor?)
- "What exactly is somaxconn a queue of?"(somaxconn 排的到底是什麼隊?)
- "You raised all the limits and it still plateaus. What's your next hypothesis?"(參數全調大了還是上不去,下一個假設是什麼?)

**(B) 口語組織骨架**:

1. 定位:Unix 裡 socket 就是 fd,一條連線一個;預設 nofile 常只有 1024,高並發第一個撞的就是它。
2. 機制:somaxconn 是「握手完成、等 app accept」的 accept queue 上限,滿了就丟或 reset;出方向連線還會吃 ephemeral port。
3. 落點:`ulimit -n`、`net.core.somaxconn`、`ip_local_port_range`,永久設定進 `/etc/sysctl.d/`。
4. 鉤子:這些都是緩衝,真正的病常是 app accept 太慢,調參只是把水缸加大。

**(C) L6 model answer**:

英文版:

> "In Unix a socket is a file descriptor, so every connection consumes one, and the default nofile limit is often just 1024, that's the 'too many open files' wall right there, raise it with ulimit or the systemd unit's LimitNOFILE. The resets under burst point at the accept queue: somaxconn caps the queue of connections that have finished the three-way handshake and are waiting for the app to call accept. When it overflows, the kernel drops or resets, and clients see failures even though the box looks idle. For outbound-heavy workloads there's a third ceiling, the ephemeral port range. But I'd close with the important caveat: these knobs are buffers, not cures. If the queue keeps overflowing, the real question is why the app accepts so slowly, blocked event loop, slow downstream, whatever. Tuning sysctl just makes the bucket bigger; if water comes in faster than it leaves, the bucket still fills."

中文版:

> 「Unix 裡 socket 就是 file descriptor,一條連線吃一個,而 nofile 預設常常只有 1024,too many open files 撞的就是這道牆,用 ulimit 或 systemd unit 的 LimitNOFILE 調大。burst 時的 reset 指向 accept queue:somaxconn 限的是『三次握手已完成、在等 app 呼叫 accept』的那條隊,溢出時 kernel 就丟包或回 reset,機器看起來很閒 client 卻一直失敗。出方向為主的 workload 還有第三道天花板,ephemeral port range。但收尾我一定會補這個 caveat:這些參數是緩衝,不是解藥。隊伍一直溢出,真正該問的是 app 為什麼 accept 這麼慢,event loop 被卡住?下游太慢?調 sysctl 只是把水缸加大,水進得比出得快,缸再大還是會滿。」

關鍵句型:"a socket is a file descriptor" / "finished the handshake, waiting for accept" / "buffers, not cures"。

---

## SIM #8: EC2 時間同步

**(A) 面試官怎麼問**:

> EN: "A customer reports intermittent failures on a few instances: AWS API calls rejected with RequestTimeTooSkewed, and some TLS errors saying certificates aren't valid yet. What's your hypothesis?"
>
> 中文:「customer 回報幾台 instance 有間歇性怪病:呼叫 AWS API 被拒,錯誤是 RequestTimeTooSkewed,還有 TLS 報憑證『尚未生效』。你的假設是什麼?」

追問串:

- "Why do VM clocks drift more than physical ones?"(為什麼 VM 的時鐘比實體機更會漂?)
- "Why exactly does clock skew break SigV4 and TLS?"(時鐘偏移為什麼會弄壞 SigV4 和 TLS?)
- "What does AWS give you so instances can sync without internet access?"(AWS 給了什麼,讓 instance 不出網也能對時?)

**(B) 口語組織骨架**:

1. 定位:兩種症狀同一個根因:時鐘漂了。SigV4 簽章帶 timestamp,TLS 憑證驗 notBefore/notAfter,都是拿本機時間判的。
2. 機制:VM 時鐘漂因為 host 排程、CPU steal、tickless kernel;chrony 收斂大偏差比 ntpd 快。
3. 落點:對 Amazon Time Sync Service,link-local `169.254.169.123`,不用出網;`chronyc tracking` 看 offset。
4. 鉤子:第三個受害者是跨機 log 時序,incident 時查不了案。

**(C) L6 model answer**:

英文版:

> "Both symptoms share one root cause: the clock has drifted. SigV4 signatures embed a timestamp and AWS rejects requests when the skew is too large, that's RequestTimeTooSkewed verbatim. And TLS validates a certificate's notBefore and notAfter against local time, so a clock in the past says 'not valid yet'. VM clocks drift more than physical ones because the guest doesn't own the hardware: host scheduling, CPU steal, tickless kernels all let ticks slip. The fix on EC2 is chrony pointed at the Amazon Time Sync Service on the link-local address 169.254.169.123, which works with no internet access at all, and chrony converges large offsets much faster than old ntpd. I'd verify with chronyc tracking and chronyc sources. One more consequence worth naming: unsynced clocks scramble log ordering across machines, which quietly ruins incident forensics, so time sync belongs in the baseline image, not in the postmortem."

中文版:

> 「兩種症狀共用同一個根因:時鐘漂了。SigV4 簽章裡帶著 timestamp,偏移太大 AWS 直接拒收,錯誤訊息就叫 RequestTimeTooSkewed;TLS 驗憑證的 notBefore 和 notAfter 用的是本機時間,時鐘慢了就會說『尚未生效』。VM 的時鐘比實體機會漂,因為 guest 不擁有硬體:host 排程、CPU steal、tickless kernel 都會讓 tick 滑掉。EC2 上的解法是 chrony 對 Amazon Time Sync Service,link-local 的 169.254.169.123,完全不用出網,而且 chrony 收斂大偏差比舊的 ntpd 快得多。驗證用 chronyc tracking 和 chronyc sources。再點一個值得講的後果:時鐘不同步會把跨機的 log 時序打亂,incident 的時候查不了案,所以 time sync 該放在 baseline image 裡,而不是出現在 postmortem 裡。」

關鍵句型:"both symptoms share one root cause" / "the guest doesn't own the hardware" / "in the baseline image, not in the postmortem"。

---

## SIM #9: IMDS 與為什麼要 IMDSv2

**(A) 面試官怎麼問** (security bar 的常客):

> EN: "Every EC2 instance can hit 169.254.169.254 and read its own metadata, including IAM role credentials. Why was that a problem, and what does IMDSv2 change?"
>
> 中文:「每台 EC2 都能打 169.254.169.254 讀自己的 metadata,包含 IAM role 的憑證。這原本為什麼是個問題?IMDSv2 改了什麼?」

追問串:

- "Walk me through how an SSRF bug turns into stolen cloud credentials."(帶我走一遍,一個 SSRF 漏洞怎麼變成雲憑證外洩。)
- "How exactly does requiring a PUT first stop that?"(先要求一個 PUT 是怎麼擋掉它的?)
- "What's the hop limit for?"(hop limit 是在防什麼?)

**(B) 口語組織骨架**:

1. 定位:IMDSv1 是無認證的純 GET,「能讓 server 幫你發 request」就等於「能拿它的 IAM 憑證」,這正是 SSRF 的定義。
2. 機制:IMDSv2 改 session 導向:先 PUT 拿 token,之後每個 GET 都要帶;SSRF 通常只能誘發 GET,發不出帶自訂 header 的 PUT。
3. 落點:token TTL + hop limit 預設 1,token 出不了這台機器;帳號層面直接強制 v2。
4. 鉤子:Capital One 事件就是這條攻擊鏈,面試講得出真實案例分量不同。

**(C) L6 model answer**:

英文版:

> "The metadata service is how an instance learns about itself, and crucially it serves the temporary credentials for the instance's IAM role. IMDSv1 was an unauthenticated GET, and that interacts badly with SSRF: if my web app has a bug that lets an attacker make the server fetch an arbitrary URL, they point it at 169.254.169.254, read the role credentials, and now they hold my cloud permissions from anywhere. That's essentially the Capital One breach. IMDSv2 makes it session-oriented: you first PUT to get a token, with a required TTL header, and every subsequent GET must present that token. A typical SSRF primitive can only trigger GETs, it can't craft a PUT with custom headers, so the front door closes. On top of that the response hop limit defaults to one, so even a leaked token dies at the instance boundary, it can't be forwarded through a container or proxy. In practice I just enforce v2 account-wide, it's a metadata option and a config rule."

中文版:

> 「metadata service 是 instance 認識自己的管道,關鍵是它也發 instance IAM role 的臨時憑證。IMDSv1 是無認證的純 GET,這跟 SSRF 加起來就出事:如果我的 web app 有個漏洞,讓攻擊者能叫 server 去抓任意 URL,他就指向 169.254.169.254,把 role 憑證讀走,從此在任何地方擁有我的雲端權限。Capital One 那次外洩基本上就是這條鏈。IMDSv2 把它改成 session 導向:先發一個 PUT 拿 token,還必須帶 TTL header,之後每個 GET 都要出示這個 token。典型的 SSRF 原語只能誘發 GET,做不出帶自訂 header 的 PUT,前門就關上了。再加上 response 的 hop limit 預設是 1,就算 token 洩漏,它也出不了這台機器,沒辦法穿過 container 或 proxy 轉發。實務上我會直接在帳號層強制 v2,一個 metadata option 加一條 config rule 的事。」

關鍵句型:"an unauthenticated GET interacts badly with SSRF" / "the front door closes" / "dies at the instance boundary"。

---

## SIM #10: load average 高但 CPU 低

**(A) 面試官怎麼問**:

> EN: "An instance shows load average of 40 on 4 vCPUs, but CPU utilization is 10%. The customer wants to scale up the instance type. Is the box actually overloaded, and would bigger CPUs help?"
>
> 中文:「一台 4 vCPU 的 instance,load average 40,但 CPU 使用率只有 10%。customer 想直接升 instance type。這台機器真的過載嗎?加 CPU 有用嗎?」

追問串:

- "What does load average actually count?"(load average 到底在數什麼?)
- "What is the D state and why can't you kill those processes?"(D state 是什麼?為什麼那些 process kill 不掉?)
- "What's special about t-series instances in this picture?"(t 系列 instance 在這張圖裡有什麼特別?)

**(B) 口語組織骨架**:

1. 定位:load average 數的是 runnable + uninterruptible (D state) 的 task 數,不是 CPU 忙碌度,所以 load 高 CPU 低 = 一群 task 在等 IO。
2. 機制:D state 是卡在 kernel 裡等 IO 完成的 process,不可中斷、kill 不掉;成因常是磁碟壞、NFS 掛掉、EBS 出事。
3. 落點:`vmstat` 看 `r` (CPU 隊) vs `b` (IO 隊),`ps` 抓 D state;t 系列另查 CPU credit 和 `st` (steal)。
4. 鉤子:加 CPU 對 IO 瓶頸毫無幫助,先分診再開藥。

**(C) L6 model answer**:

英文版:

> "Bigger CPUs almost certainly won't help, because load average doesn't measure CPU. It counts tasks that are either runnable or in uninterruptible sleep, the D state, and D state means stuck in the kernel waiting for I/O, disk, NFS, an EBS volume having a bad day. So forty tasks of load with an idle CPU reads as: a crowd of processes queued on I/O, not on compute. I'd confirm with vmstat, comparing the r column, the CPU run queue, against b, tasks blocked on I/O, and grab the D-state processes with ps to see what they're waiting on. You can't kill a D-state process, which itself is a hint the wait is in kernel space. One cloud-specific branch: on t-series burstable instances, check whether CPU credits ran out, the steal column rising means the hypervisor is throttling you, and that presents its own kind of weirdness. So the consulting answer is: diagnose which queue is long before buying a bigger engine, the fix is likely EBS throughput, or the NFS mount, not vCPUs."

中文版:

> 「升 CPU 幾乎肯定沒用,因為 load average 量的不是 CPU。它數的是 runnable 加上 uninterruptible sleep,也就是 D state 的 task 數;D state 代表卡在 kernel 裡等 IO,磁碟、NFS、或某顆 EBS 出狀況。所以 load 40 配上很閒的 CPU,讀出來的意思是:一群 process 在排 IO 的隊,不是在搶運算。我會用 vmstat 確認,比較 r 欄,CPU 的 run queue,跟 b 欄,卡在 IO 的 task;再用 ps 抓出 D state 的 process 看它們在等什麼。D state 的 process kill 不掉,這本身就是線索,表示它卡在 kernel space。雲上還有一條分支要查:t 系列的 burstable instance,看 CPU credit 是不是燒完了,st 欄升高代表 hypervisor 在扣你的 CPU,那是另一種怪病。所以 consultant 的答案是:先分診哪條隊在排長龍,再決定開什麼藥,這病多半出在 EBS throughput 或 NFS,不在 vCPU。」

關鍵句型:"load average doesn't measure CPU" / "queued on I/O, not on compute" / "diagnose the queue before buying a bigger engine"。

---

## SIM #11: free 的 buff/cache 不是漏記憶體

**(A) 面試官怎麼問**:

> EN: "A customer files a ticket: 'Linux has a memory leak, free shows only 200 megs free out of 16 gigs, but our apps only use 4.' Do you tell them to add RAM?"
>
> 中文:「customer 開 ticket:『Linux 有 memory leak,16G 的機器 free 只剩 200MB,但我們的 app 只用 4G。』你會叫他加 RAM 嗎?」

追問串:

- "What is the page cache actually doing for them?"(page cache 實際上在幫他們做什麼?)
- "Which number tells you real memory pressure, and how is it estimated?"(哪個數字才代表真的記憶體壓力?它怎麼估出來的?)
- "What signals would make you agree the box really is short on memory?"(看到什麼訊號你才會同意這台真的缺記憶體?)

**(B) 口語組織骨架**:

1. 定位:那不是 leak,是 page cache:kernel 把沒人用的 RAM 拿來快取磁碟內容,unused RAM is wasted RAM。
2. 機制:cache 是可回收的,誰要就還誰;判斷壓力看 `available` 欄 (MemAvailable 的估算),不是 `free` 欄。
3. 落點:真缺的訊號是 `available` 持續下探 + `vmstat` 的 `si`/`so` 開始 swap;`free -h` 秒判。
4. 鉤子:這是 support 最高頻誤報之一,一句話能讓 customer 安心也建立信任。

**(C) L6 model answer**:

英文版:

> "No, and this is one of the most common false alarms in support. What they're seeing is the page cache: the kernel takes RAM nobody is using and caches disk contents in it, because unused RAM is wasted RAM. Reads that hit the cache skip the disk entirely, so this is the kernel actively making their I/O faster, for free. The key property is that cache memory is reclaimable, the moment an application needs it, the kernel hands it back. That's why the 'free' column is misleading and the 'available' column is the honest number, it's the kernel's estimate, MemAvailable, of how much memory could be allocated right now without swapping, counting the reclaimable cache. I'd only agree the box is short on RAM if available trends down persistently and vmstat starts showing si and so, actual swap-in and swap-out. Absent that, the answer to the ticket is one sentence: your memory isn't leaking, it's working."

中文版:

> 「不會,這是 support 最高頻的誤報之一。他們看到的是 page cache:kernel 把沒人用的 RAM 拿去快取磁碟內容,因為 unused RAM is wasted RAM,閒著的記憶體就是浪費的記憶體。讀取命中 cache 就完全不用碰磁碟,所以這其實是 kernel 在免費幫他們加速 IO。關鍵性質是 cache 可回收:application 一要,kernel 馬上還。這就是為什麼 free 欄會誤導,誠實的數字是 available 欄,它是 kernel 的估算值 MemAvailable,代表現在能分配多少記憶體而不觸發 swap,把可回收的 cache 算進去了。我只有在兩個訊號同時出現時才會同意這台真的缺 RAM:available 持續往下探,加上 vmstat 的 si 和 so 開始動,真的在 swap 了。沒有這些的話,這張 ticket 的回覆一句話就夠:你的記憶體不是在漏,是在幹活。」

關鍵句型:"unused RAM is wasted RAM" / "'available' is the honest number" / "your memory isn't leaking, it's working"。

---

## SIM #12: OOM killer 與洩漏排查

**(A) 面試官怎麼問**:

> EN: "A customer's database process vanished overnight. No crash log from the app itself. dmesg shows the oom-killer fired. Why does the kernel kill processes at all, why did it pick the database, and how do you find the real culprit?"
>
> 中文:「customer 的 database process 半夜消失了,app 自己沒留任何 crash log,dmesg 裡看到 oom-killer 出手。kernel 為什麼要殺 process?為什麼挑中 database?你怎麼找出真正的元兇?」

追問串:

- "How does the kernel choose the victim?"(kernel 怎麼挑犧牲者?)
- "How do you protect a critical process from the OOM killer, and what's the risk?"(怎麼保護關鍵 process 不被 OOM killer 殺?風險是什麼?)
- "How do you tell 'big but stable' apart from an actual leak?"(「大但穩定」和真的 leak 怎麼分?)

**(B) 口語組織骨架**:

1. 定位:Linux 允許 overcommit,真的兌現不了時 kernel 只能殺人止血,挑的是 `oom_score` 最高的,通常就是最大戶,database 常中獎。
2. 機制:`oom_score_adj` 可加權保護關鍵 process,代價是 kernel 會去殺別人;元兇是「持續成長的 RSS」,不一定是被殺的那個。
3. 落點:`dmesg -T` 看 oom 段的 per-process 記帳;`smaps_rollup` 追單 process 佔用;止血選項:加 swap、調 adj、修 leak。
4. 鉤子:被殺的是最大的,不一定是漏的,這個區分是 senior 的標誌。

**(C) L6 model answer**:

英文版:

> "Linux overcommits memory: it promises more than it has, betting processes won't all cash in at once. When the bet fails and there's truly nothing left, the kernel has to kill someone to keep the system alive, that's the OOM killer. It picks the victim by oom_score, which is dominated by memory footprint, so the database gets shot not because it misbehaved but because it was the biggest target, and that's the key distinction: the process killed is often not the process leaking. So in dmesg I'd read the OOM report's per-process table, it's a snapshot of everyone's RSS at the moment of the kill, and look for who had grown, then confirm by trending RSS over time, smaps_rollup gives the accurate per-process number. A leak grows without bound; a cache grows and plateaus. Mitigations while the fix lands: set oom_score_adj to steer the killer away from the database, accepting it'll kill something else, add swap as a shock absorber, and cap the suspect with a cgroup limit so it OOMs alone instead of taking the box hostage."

中文版:

> 「Linux 是 overcommit 的:它承諾的記憶體比實際有的多,賭大家不會同時兌現。賭輸、真的一點不剩的時候,kernel 只能殺一個 process 來保住系統,這就是 OOM killer。它用 oom_score 挑犧牲者,而分數主要由記憶體佔用決定,所以 database 被殺不是因為它做錯事,而是因為它是最大的目標。這裡有個關鍵區分:被殺的 process 常常不是在漏的那個。所以我會去 dmesg 讀 OOM 報告裡的 per-process 表,那是行刑當下所有人 RSS 的快照,找出誰一直在長,再用 smaps_rollup 對單一 process 做時間序列確認。leak 是無上限地長;cache 是長到一個高原就停。修好前的止血選項:oom_score_adj 把槍口從 database 移開,代價是 kernel 會去殺別人;加 swap 當避震器;用 cgroup limit 把嫌疑犯框起來,讓它自己 OOM,而不是挾持整台機器。」

關鍵句型:"betting processes won't all cash in at once" / "the biggest target, not the misbehaving one" / "a leak grows without bound, a cache plateaus"。

---

## SIM #13: strace vs lsof vs tcpdump

**(A) 面試官怎麼問**:

> EN: "An app on EC2 is hung, no logs, no errors. You've got strace, lsof, and tcpdump in your toolbox. How do you decide which one to reach for, and what does each actually see?"
>
> 中文:「EC2 上有個 app hang 住了,沒 log 沒 error。工具箱裡有 strace、lsof、tcpdump。你怎麼決定先用哪個?它們各自看得到什麼?」

追問串:

- "Where does each tool hook into the system?"(這三個工具各自掛在系統的哪個觀測點?)
- "What's the risk of strace on a busy production process?"(對 prod 上忙碌的 process 用 strace 有什麼風險?)
- "Give me a concrete flow: hung app, which tool first and what would you expect to see?"(給我一條具體流程:app hang 住,先用哪個、預期看到什麼?)

**(B) 口語組織骨架**:

1. 定位:先問「這是哪一層的問題」,再選工具:strace 看 process/kernel 邊界的 syscall,lsof 看開了哪些 fd,tcpdump 看線上真正跑的封包。
2. 機制:strace 用 ptrace 攔每個 syscall,目標會明顯變慢,prod 慎用;lsof 讀 `/proc/<pid>/fd`;tcpdump 用 AF_PACKET 從 link 層抓。
3. 落點:hang 住先 strace 看卡在哪個 syscall (read? connect? futex?),對到 fd 用 lsof 翻成人話,懷疑網路再 tcpdump 看 SYN 有去有回沒。
4. 鉤子:三層縮小法:syscall → fd → wire,一條線走完大部分 hang 案。

**(C) L6 model answer**:

英文版:

> "The question to ask first is which layer the problem lives in, because the three tools sit at three different observation points. strace watches the boundary between the process and the kernel, every syscall, it hooks in with ptrace, which also means the target slows down noticeably, so I'm careful attaching it to a hot production process. lsof reads /proc to show which file descriptors a process holds, files, sockets, pipes. tcpdump captures from the link layer, it shows what's actually on the wire, not what the app believes it sent. For a silent hang my flow is: strace the process first, a hung app is usually parked in one syscall, and which one is the verdict, blocked on read means waiting on some fd, connect means network, futex means a lock. Then lsof translates that fd number into a real thing, oh, it's a socket to the database. If it's network, tcpdump answers the final question: did the SYN go out, did anything come back. Syscall, then fd, then wire, three layers, each tool narrows the next."

中文版:

> 「第一個要問的是:這是哪一層的問題?因為三個工具掛在三個不同的觀測點。strace 看的是 process 和 kernel 的邊界,每一個 syscall,它用 ptrace 攔截,代價是目標會明顯變慢,所以對 prod 上忙碌的 process 我會很小心。lsof 讀 /proc,列出 process 手上開著的 fd:檔案、socket、pipe。tcpdump 從 link 層抓,看到的是線上真正跑的封包,不是 app 以為它送出去的東西。無聲 hang 的流程我會這樣走:先 strace,hang 住的 app 通常停在某一個 syscall 上,停在哪就是判決:卡在 read 是在等某個 fd,connect 是網路,futex 是鎖。接著用 lsof 把那個 fd 編號翻成人話:喔,是連到 database 的 socket。如果指向網路,tcpdump 回答最後一題:SYN 有出去嗎?有東西回來嗎?syscall、fd、wire,三層,每個工具幫下一個縮小範圍。」

關鍵句型:"three different observation points" / "what's actually on the wire, not what the app believes" / "each tool narrows the next"。

---

## SIM #14: Connection Refused vs Timeout

**(A) 面試官怎麼問**:

> EN: "A customer can't reach their app from another instance. Sometimes the error is 'connection refused' immediately, other times it just hangs and times out. What is the difference actually telling you?"
>
> 中文:「customer 從另一台 instance 連不到他的 app,有時候是秒回 connection refused,有時候是掛在那邊直到 timeout。這個差別實際上在告訴你什麼?」

追問串:

- "Who sends the RST in the refused case?"(refused 的情況下,RST 是誰回的?)
- "Why does a security group block look like a timeout instead of refused?"(為什麼被 security group 擋看起來是 timeout 而不是 refused?)
- "So given each symptom, where do you look first?"(所以兩種症狀各自先查哪裡?)

**(B) 口語組織骨架**:

1. 定位:快慢就是第一個線索:refused = 封包到了、被拒;timeout = 封包石沉大海。
2. 機制:打到沒有 listener 的 port,kernel 立刻回 RST,connect() 秒拿 ECONNREFUSED;SG 是 stateful allow-list,不放行的封包靜默丟棄、不回 RST,所以只能等逾時。
3. 落點:診斷分岔:快 = 到了主機,查 process 有沒有在聽 (`ss -ltn`);慢 = 半路被丟,查 SG/NACL/路由。
4. 鉤子:「refused 反而是好消息」,至少證明網路通了。

**(C) L6 model answer**:

英文版:

> "Speed is the first clue, because the two symptoms fail at different places. 'Connection refused' means the packet arrived: the kernel on the target host looked for a listener on that port, found none, and immediately sent back a RST, so connect() fails fast with ECONNREFUSED. Counterintuitively that's good news, the network path works, the problem is on the host, the service is down, crashed, or listening on the wrong port or interface, ss -ltn settles it. A hang that ends in timeout means the packet vanished en route, and in AWS the prime suspect is the security group: it's a stateful allow-list, and traffic it doesn't allow is silently dropped, no RST, no ICMP, nothing for the client to react to, so it waits. NACLs deny the same silent way, and a missing route behaves similarly. So my diagnostic fork is: fast failure, go look at the host; slow failure, go look at the path, security groups first."

中文版:

> 「快慢就是第一條線索,因為兩種症狀死在不同的地方。connection refused 代表封包到了:目標主機的 kernel 找那個 port 上的 listener,沒找到,立刻回一個 RST,所以 connect() 秒失敗,拿到 ECONNREFUSED。反直覺的是這其實是好消息,網路是通的,問題在主機上:service 掛了、crash 了、或聽錯 port 聽錯 interface,ss -ltn 一看就知道。掛到 timeout 則代表封包半路消失了,AWS 上頭號嫌疑人是 security group:它是 stateful 的 allow-list,不在放行清單的流量直接靜默丟棄,不回 RST、不回 ICMP,client 什麼都收不到,只能傻等。NACL 的 deny 也是同樣的無聲丟法,路由缺了行為也類似。所以我的診斷分岔是:快的失敗,去查主機;慢的失敗,去查路徑,security group 最先。」

關鍵句型:"speed is the first clue" / "counterintuitively, refused is good news" / "silently dropped, nothing for the client to react to"。

---

## SIM #15: SG vs NACL 的 stateful 差異

**(A) 面試官怎麼問**:

> EN: "People recite 'security groups are stateful, NACLs are stateless' in every AWS interview. Tell me what that actually means underneath. What is the state?"
>
> 中文:「每場 AWS 面試都有人背『SG 是 stateful,NACL 是 stateless』。跟我講這句話底層到底是什麼意思。那個 state 是什麼?」

追問串:

- "What's the Linux mechanism that does the same job?"(Linux 裡做同一件事的機制是什麼?)
- "Why do NACLs need the ephemeral port range opened for return traffic?"(為什麼 NACL 要為回程流量開 ephemeral port range?)
- "When would you actually use a NACL given SGs exist?"(有 SG 了,什麼情況你還會真的用 NACL?)

**(B) 口語組織骨架**:

1. 定位:state = 一本連線記帳本。SG 的 stateful 本質就是雲版 conntrack:記住「這條連線是誰發起的」,回程自動放行。
2. 機制:NACL 沒有這本帳,每個封包獨立判斷,所以回程的高位 ephemeral port (1024-65535) 要手動開,忘開是經典坑。
3. 落點:Linux 對應物就是 conntrack,`conntrack -L` 看得到;SG 掛在 ENI、NACL 掛在 subnet 邊界。
4. 鉤子:NACL 的實際用途是 subnet 級的粗粒度 deny (封 IP、封段),SG 做不到 deny。

**(C) L6 model answer**:

英文版:

> "The state is a connection-tracking table, a ledger. When you allow inbound 443 in a security group, the SG records each connection that comes in, five-tuple, direction, who initiated, and when the response goes back out, it matches the ledger and lets it through automatically, you never write an outbound rule for it. That's exactly what conntrack does in Linux, iptables' stateful firewalling, the cloud just runs the same idea at the ENI. A NACL has no ledger. It evaluates every packet in isolation at the subnet boundary, so a response packet is just 'some outbound packet to a high port' to it, and you're forced to open the ephemeral range, 1024 to 65535, for return traffic. Forgetting that is the classic NACL incident: inbound works, responses die. As for when I'd still use one: NACLs can deny, security groups can't, so they're the right tool for coarse subnet-level blocks, ban this IP range, quarantine this subnet, while SGs stay the fine-grained allow layer."

中文版:

> 「那個 state 是一張 connection tracking 表,一本記帳本。你在 SG 開放 inbound 443,SG 會把每條進來的連線記下來,五元組、方向、誰發起的;回應出去的時候,它對帳本比對得上,就自動放行,你從來不用為回程寫 outbound 規則。這正是 Linux 裡 conntrack 做的事,iptables 的 stateful 防火牆,雲只是把同一個概念跑在 ENI 上。NACL 沒有這本帳,它在 subnet 邊界對每個封包獨立判斷,所以一個回應封包在它眼裡只是『某個往高位 port 的 outbound 封包』,你被迫為回程開 ephemeral range,1024 到 65535。忘記開就是 NACL 的經典事故:進得來,回不去。至於什麼時候還會用 NACL:NACL 能 deny,SG 不能,所以 subnet 級的粗粒度封鎖,封一段 IP、隔離一個 subnet,是它的正職;SG 留在細粒度的 allow 層。」

關鍵句型:"the state is a ledger" / "evaluates every packet in isolation" / "NACLs can deny, security groups can't"。

---

## SIM #16: TCP 三次握手 + TCP vs UDP 的取捨

**(A) 面試官怎麼問**:

> EN: "Why does DNS run over UDP while your API runs over TCP? Walk me through what TCP's handshake buys you, and when you'd deliberately give it up."
>
> 中文:「為什麼 DNS 跑 UDP,你的 API 卻跑 TCP?TCP 的握手買到了什麼?什麼情況你會刻意放棄它?」

追問串:

- "Walk me through the three-way handshake and what state each side holds."(走一遍三次握手,兩邊各自持有什麼狀態?)
- "Why is a retry cheaper than a handshake for DNS?"(對 DNS 來說,為什麼重試比握手便宜?)
- "Where does QUIC fit in this picture?"(QUIC 在這張圖裡的位置是什麼?)

**(B) 口語組織骨架**:

1. 定位:TCP 買的是可靠、有序、壅塞控制,付的是握手 RTT 和兩端的連線狀態;UDP 什麼都不保證,也什麼都不收費。
2. 機制:SYN → SYN+ACK → ACK,雙方確認彼此收發能力並交換初始序號;之後 kernel 兩端都維護狀態機。
3. 落點:DNS 一問一答,丟了重問比建連便宜;即時音視訊遲到不如丟掉;QUIC 在 UDP 上自建更好的可靠層 + 0-RTT。
4. 鉤子:面試要的是「為什麼這個場景寧可 UDP」的推理,不是背定義。

**(C) L6 model answer**:

英文版:

> "TCP sells you three guarantees, delivery, ordering, and congestion control, and the price is a round trip of handshake before any data, plus connection state held on both ends. The handshake itself is SYN, SYN-ACK, ACK: each side proves it can both send and receive, and they exchange initial sequence numbers, which is what makes reliable ordering possible afterwards. Whether that price is worth paying depends on the traffic shape. DNS is one tiny question, one tiny answer: if the response is lost, just asking again is cheaper than having built a connection, so UDP wins. Real-time audio and video make the opposite trade for a different reason: a late packet is worse than a lost one, so TCP's retransmit-and-wait actively hurts. Your API wants every byte, in order, so TCP. And QUIC is the modern synthesis: it runs on UDP but rebuilds reliability and congestion control in user space, better, with stream multiplexing and 0-RTT, that's HTTP/3. The interview answer isn't the definitions, it's matching the guarantee to the workload."

中文版:

> 「TCP 賣你三個保證:送達、有序、壅塞控制;價格是資料開跑前的一個握手 RTT,加上兩端都要維護的連線狀態。握手本身是 SYN、SYN-ACK、ACK:雙方各自證明自己能收也能發,並交換初始序號,這是後面可靠排序的基礎。這個價格值不值,看流量的形狀。DNS 是一個小問題配一個小答案:回應丟了,再問一次比先建一條連線便宜,所以 UDP 贏。即時音視訊做的是反向 trade,理由不同:遲到的封包比丟掉的更糟,TCP 的重傳等待反而害事。你的 API 要求每個 byte 都到、都按順序,所以 TCP。QUIC 是現代的綜合體:跑在 UDP 上,但在 user space 重建了更好的可靠層和壅塞控制,加上 stream multiplexing 和 0-RTT,就是 HTTP/3。面試要的答案不是定義,是把保證對到 workload 上的那段推理。」

關鍵句型:"three guarantees, and the price" / "a late packet is worse than a lost one" / "matching the guarantee to the workload"。

---

## SIM #17: Routing:本機 ip route 與 VPC route table

**(A) 面試官怎麼問**:

> EN: "An instance in a private subnet can't reach the internet. Walk me through the full routing decision, from the process making the call down to where the packet leaves the VPC. Where can it break?"
>
> 中文:「private subnet 裡的一台 instance 連不上 internet。從 process 發出呼叫開始,到封包離開 VPC 為止,把完整的路由決策走一遍。哪些地方可能斷?」

追問串:

- "How does the host pick a route when multiple entries match?"(多條路由都吻合時,主機怎麼選?)
- "The host's default route looks fine. What's the next layer to check?"(本機 default route 沒問題,下一層查什麼?)
- "Why does the NAT gateway have to live in a public subnet?"(為什麼 NAT gateway 要放在 public subnet?)

**(B) 口語組織骨架**:

1. 定位:兩層路由疊起來:封包先過本機 routing table,出了主機再由 subnet 綁的 VPC route table 決定去向。
2. 機制:本機層 longest-prefix match 選路,`default via` 是兜底;VPC 層,private subnet 的 0.0.0.0/0 應指向 NAT gateway,NAT 所在的 public subnet 再指向 IGW。
3. 落點:`ip route get 8.8.8.8` 看本機這層;VPC 層查 subnet association 和那條 0.0.0.0/0;兩層都對才通。
4. 鉤子:「連不上外網」的病根分佈:本機 default route、subnet 路由、NAT 位置、還有 SG/NACL,一層層排除。

**(C) L6 model answer**:

英文版:

> "There are two routing layers stacked, and the packet has to win at both. First, on the host: the kernel walks the local routing table using longest-prefix match, the most specific route wins, and for an internet address that's usually the default route pointing at the subnet's gateway. I'd check that exact decision with ip route get 8.8.8.8, it tells you the chosen interface and next hop for that destination. Once the packet leaves the instance, the VPC takes over: the route table associated with the subnet decides where it goes, and a subnet is associated with exactly one route table. For a private subnet the 0.0.0.0/0 entry should point at a NAT gateway, and here's the classic misconfiguration: the NAT gateway itself must sit in a public subnet, one whose own route table points at the IGW, because the NAT gateway needs a path to the internet to do its job. So my checklist runs: host default route, subnet route table entry, NAT placement, and if all three pass, then it's not routing, I move to security groups and NACLs."

中文版:

> 「這裡有兩層路由疊在一起,封包兩層都要過關。第一層在主機上:kernel 用 longest-prefix match 走本機 routing table,最精確的路由贏,對一個 internet 位址來說通常落到 default route,指向 subnet 的 gateway。我會用 ip route get 8.8.8.8 直接看這個決策:這個目的地會走哪個 interface、下一跳是誰。封包出了 instance,換 VPC 接手:subnet 綁的那張 route table 決定它去哪,而一個 subnet 只綁一張 route table。private subnet 的 0.0.0.0/0 應該指向 NAT gateway,而經典的設定錯誤在這:NAT gateway 本身必須放在 public subnet,也就是它自己那張 route table 指向 IGW 的 subnet,因為 NAT gateway 要能出網才幫得了別人。所以我的 checklist 是:本機 default route、subnet 的路由條目、NAT 的位置;三關都過,那就不是路由的事,轉去查 SG 和 NACL。」

關鍵句型:"two routing layers stacked" / "the most specific route wins" / "the NAT gateway needs a path to the internet to do its job"。

---

## SIM #18: DNS 解析路徑 + VPC 裡誰回答

**(A) 面試官怎麼問**:

> EN: "In a VPC, when an application resolves a hostname, who actually answers? Walk me through the full path, and then tell me how it changes in a hybrid setup where on-prem and AWS need to resolve each other."
>
> 中文:「VPC 裡,application 解析一個 hostname 的時候,到底是誰在回答?把完整路徑走一遍,然後說說 hybrid 場景下,on-prem 和 AWS 要互相解析時,這條路怎麼變。」

追問串:

- "What is the .2 resolver and where does the address come from?"(.2 resolver 是什麼?那個位址怎麼來的?)
- "Why can't on-prem servers just query the .2 resolver directly?"(為什麼 on-prem 的機器不能直接查 .2 resolver?)
- "Inbound versus outbound resolver endpoints, which direction is which?"(inbound 和 outbound resolver endpoint,方向各是哪邊?)

**(B) 口語組織骨架**:

1. 定位:app 照 `/etc/resolv.conf` 問出去;VPC 裡預設的回答者是 AmazonProvidedDNS,住在 VPC CIDR base +2,俗稱 .2 resolver。
2. 機制:.2 resolver 兩件事都做:幫你遞迴解外部名字、回答 private hosted zone 的內部名字;但它只在 VPC 內可達。
3. 落點:hybrid 靠 Route 53 Resolver endpoints:inbound 讓 on-prem 查得到 AWS 的名字,outbound + forwarding rules 讓 VPC 查得到 on-prem 的名字。
4. 鉤子:hybrid DNS 是 migration 的必考件,cutover 期間兩邊名字都要活著。

**(C) L6 model answer**:

英文版:

> "The app itself just follows /etc/resolv.conf to its stub resolver, and in a VPC that points at the Amazon-provided DNS, which lives at the VPC CIDR base plus two, the so-called .2 resolver, in a 10.0.0.0/16 VPC that's 10.0.0.2. It wears two hats: for public names it does full recursion out to root, TLD, and authoritative servers on your behalf, and for names in a private hosted zone associated with the VPC, it answers directly. The catch that drives the hybrid design: it's only reachable from inside the VPC. So when on-prem needs to resolve AWS private names, you deploy Route 53 Resolver inbound endpoints, real ENIs with VPC IPs that on-prem DNS servers can forward to. The reverse direction uses outbound endpoints plus forwarding rules: queries for corp.example.com get forwarded from the VPC to the on-prem DNS servers. In a migration this is day-one plumbing, during cutover both estates must resolve each other continuously, and half the 'app is down' tickets in that window are actually DNS conditional forwarding gaps."

中文版:

> 「app 自己只是照 /etc/resolv.conf 去問 stub resolver,VPC 裡它預設指向 Amazon 提供的 DNS,住在 VPC CIDR base 加 2,俗稱 .2 resolver,10.0.0.0/16 的 VPC 就是 10.0.0.2。它戴兩頂帽子:對公網名字,它替你做完整遞迴,root、TLD、authoritative 一路問下去;對綁在這個 VPC 的 private hosted zone 裡的名字,它直接回答。驅動 hybrid 設計的關鍵限制是:它只在 VPC 內部可達。所以 on-prem 要解 AWS 的私有名字時,部署 Route 53 Resolver 的 inbound endpoint,那是真實的 ENI、有 VPC 的 IP,on-prem 的 DNS server 可以 forward 過來。反方向用 outbound endpoint 加 forwarding rules:對 corp.example.com 的查詢從 VPC 轉發到 on-prem 的 DNS server。在 migration 裡這是 day-one 的水電工程,cutover 期間兩邊的名字必須持續互解,那段時間一半的『app 掛了』ticket 其實是 DNS conditional forwarding 沒接好。」

關鍵句型:"it wears two hats" / "only reachable from inside the VPC" / "day-one plumbing, not an afterthought"。

---

## SIM #19: TLS 握手與憑證鏈驗證

**(A) 面試官怎麼問**:

> EN: "Your customer just migrated an internal API to AWS, and now clients fail with 'certificate verify failed'. Walk me through how certificate validation actually works, and what you'd check first."
>
> 中文:「customer 剛把一個內部 API 搬上 AWS,client 開始報 certificate verify failed。跟我講一遍憑證驗證實際上是怎麼運作的,以及你會先查什麼。」

追問串:

- "Where would you terminate TLS in their architecture, and why?"(在他們的架構裡你會把 TLS 終結在哪、為什麼?)
- "What happens if an intermediate CA cert is missing?"(缺了 intermediate CA 憑證會發生什麼事?)
- "The customer is a bank and requires encryption in transit end to end. Does terminating at the ALB satisfy that?"(customer 是銀行,要求 end-to-end 的傳輸加密,終結在 ALB 算滿足嗎?)

**(B) 口語組織骨架**:

1. 定位:client 要驗兩件事,這把 key 屬於這個 hostname、而且有人我信任的替它擔保。
2. 機制:從 leaf 憑證沿簽章往上驗到本機 trust store 的 root CA;同時查 SAN、有效期、撤銷。
3. 落點:verify failed 三大嫌疑,缺 intermediate、時鐘漂 (連 #8)、SAN 不含這個 hostname;`openssl s_client` 直接看鏈。
4. 鉤子:termination 位置是架構決策,ALB + ACM 省運維,FSI 要 re-encrypt 到後端。

**(C) L6 model answer**:

英文版:

> "Certificate validation answers two questions: does this public key really belong to this hostname, and does someone I trust vouch for it. The server sends a certificate chain. The client verifies each signature from the leaf up to a root CA in its local trust store, and along the way checks the hostname against the SAN, the validity dates, and revocation. The three usual suspects for 'verify failed' are a missing intermediate certificate, clock drift on the client, since validity is checked against local time, or a SAN that doesn't cover the internal hostname. I'd run openssl s_client and look at the chain directly. Architecture-wise I'd terminate at the ALB with an ACM certificate, so renewal is managed, and for a regulated customer I'd re-encrypt from the ALB to the targets so traffic is never in the clear."

中文版:

> 「憑證驗證要回答兩個問題:這把 public key 真的屬於這個 hostname 嗎?有沒有我信任的人替它擔保?Server 會送一條 certificate chain 過來,client 從 leaf 憑證開始,沿著每張憑證上的簽章一路驗到本機 trust store 裡的 root CA,過程中同時檢查 hostname 在不在 SAN、有效期、有沒有被撤銷。verify failed 的三大嫌疑:缺 intermediate 憑證、client 時鐘漂掉 (因為有效期是用本機時間判的)、或 SAN 沒涵蓋這個內部 hostname。我會直接用 openssl s_client 看鏈長什麼樣。架構上我會終結在 ALB 配 ACM 憑證,續期全託管;如果是受監理的 customer,ALB 到後端再 re-encrypt,讓流量全程沒有明文段。」

關鍵句型:"does someone I trust vouch for it" / "the three usual suspects are..." / "re-encrypt so traffic is never in the clear"。

---

## SIM #20: MTU 9001 vs 1500 與 PMTUD 黑洞

**(A) 面試官怎麼問**:

> EN: "After setting up a VPN to on-prem, a customer reports something weird: SSH login works fine, ping works, but copying any large file just hangs forever. Small API calls succeed, big responses stall. What's your hypothesis?"
>
> 中文:「customer 接好了到 on-prem 的 VPN,回報一個怪現象:SSH 登得進去、ping 也通,但複製大檔案就永遠卡住;小的 API 呼叫成功,大的回應停在半路。你的假設是什麼?」

追問串:

- "Why do small packets get through when big ones don't?"(為什麼小封包過得去,大封包過不去?)
- "Walk me through Path MTU Discovery and how it gets broken."(走一遍 Path MTU Discovery,以及它是怎麼被弄壞的。)
- "What are the fixes, short-term and proper?"(短期和正規的修法各是什麼?)

**(B) 口語組織骨架**:

1. 定位:「小的通、大的卡」是 MTU 問題的指紋:VPC 內 MTU 9001,VPN/DX 路徑常掉到 1500 以下 (封裝還要吃 overhead)。
2. 機制:封包帶 DF bit 超過路徑某段 MTU 時,該設備應回 ICMP type 3 code 4 叫來源縮小,這就是 PMTUD;防火牆把這個 ICMP 擋掉,大封包被丟又沒人通知,就成黑洞。
3. 落點:`ping -M do -s 1472` 逐步找真實 Path MTU;修法:放行 ICMP 3/4,或在邊界做 MSS clamp,或直接把介面 MTU 降到 1500。
4. 鉤子:症狀簽名值得背:SSH 通但 `ls` 大輸出卡死、TLS 握手成功但傳 body 逾時。

**(C) L6 model answer**:

英文版:

> "That symptom pattern, small packets fine, large transfers hang, is the fingerprint of a path MTU black hole. Inside a VPC the MTU is 9001, but the VPN path tops out at 1500 or less, since the tunnel encapsulation eats some bytes. Path MTU Discovery is supposed to handle this: packets go out with the DF bit set, and when one exceeds a link's MTU, that device sends back an ICMP 'fragmentation needed', type 3 code 4, telling the sender to shrink. The black hole appears when a firewall or security group drops that ICMP: the big packet is discarded, the notification never arrives, so the sender just retransmits the same too-big packet forever. That's exactly why SSH login works, tiny packets, but the file copy stalls, and why a TLS handshake succeeds while the response body times out. I'd confirm with ping -M do -s 1472, forcing DF at full 1500, and shrink until it passes to find the real path MTU. Fixes: allow ICMP type 3 code 4 through, that's the correct one, or clamp TCP MSS at the tunnel edge so both sides negotiate smaller segments up front."

中文版:

> 「這個症狀組合,小封包通、大傳輸卡,就是 path MTU 黑洞的指紋。VPC 內部 MTU 是 9001,但 VPN 路徑最多 1500 甚至更低,因為 tunnel 封裝還要吃掉一些 bytes。Path MTU Discovery 本來就是設計來處理這件事的:封包帶著 DF bit 出門,超過某段鏈路的 MTU 時,那台設備回一個 ICMP fragmentation needed,type 3 code 4,叫來源縮小。黑洞出現在防火牆或 SG 把這個 ICMP 擋掉的時候:大封包被丟了,通知又永遠到不了,來源就只會一直重傳同一顆過大的封包。這正好解釋了為什麼 SSH 登得進去,封包都很小,但複製檔案就停住;為什麼 TLS 握手成功,回應的 body 卻逾時。我會用 ping -M do -s 1472 驗證,帶 DF 打滿 1500,不通就往下縮,找出真實的 path MTU。修法:放行 ICMP type 3 code 4,這是正解;或在 tunnel 邊界做 TCP MSS clamp,讓兩端一開始就談一個比較小的 segment。」

關鍵句型:"the fingerprint of a path MTU black hole" / "the notification never arrives" / "clamp the MSS at the tunnel edge"。

---

## SIM #21: 公開金鑰密碼學 (RSA 憑證)

**(A) 面試官怎麼問**:

> EN: "Let's go one level down. HTTPS uses both asymmetric and symmetric encryption. Why both? What is the RSA key in a certificate actually used for?"
>
> 中文:「往下挖一層。HTTPS 同時用了非對稱和對稱加密,為什麼要兩種都用?憑證裡那把 RSA key 實際上是拿來做什麼的?」

追問串:

- "Why not encrypt everything with RSA?"(為什麼不全部用 RSA 加密就好?)
- "What's forward secrecy and why do we care?"(forward secrecy 是什麼、為什麼重要?)
- "So if I steal the server's private key today, can I decrypt traffic I captured last year?"(如果我今天偷到 server 的 private key,能解開去年錄下的流量嗎?)

**(B) 口語組織骨架**:

1. 定位:一對 keypair,public 加密 private 解;反向就是簽章,private 簽 public 驗。
2. 機制:非對稱運算貴,所以只用在握手 (驗身分、換 key),資料走 AES;現代 TLS 裡 RSA 幾乎只剩簽章,key exchange 走 ECDHE。
3. 落點:ECDHE 給 forward secrecy,session key 跟憑證的 key 脫鉤,私鑰洩漏不影響歷史流量。
4. 鉤子:憑證解決的其實是 binding 問題,key 誰都能生,CA 簽章綁定 key 和 hostname。

**(C) L6 model answer**:

英文版:

> "Asymmetric crypto gives you two things: anyone can encrypt to my public key but only I can decrypt, and the reverse gives you signatures, I sign with the private key and anyone can verify. But it's computationally expensive, maybe a thousand times slower than AES, so TLS only uses it during the handshake, to prove identity and agree on a session key, then all the actual data flows over symmetric encryption. In modern TLS the RSA key in the certificate is really just for signing. The key exchange itself uses ephemeral Diffie-Hellman, which buys you forward secrecy: the session keys aren't derived from the certificate's key, so even if the server's private key leaks later, captured traffic from last year stays unreadable. And the certificate itself exists to solve a binding problem: anyone can generate a key pair, the CA's signature is what ties this particular key to this particular hostname."

中文版:

> 「非對稱加密給你兩件事:任何人能用我的 public key 加密、只有我能解;反過來就是簽章,我用 private key 簽,任何人能驗。但它的運算成本很高,比 AES 慢幾個數量級,所以 TLS 只在握手階段用它,證明身分、談好 session key,之後資料全走對稱加密。現代 TLS 裡,憑證那把 RSA key 幾乎只剩簽章用途,key exchange 本身走 ephemeral Diffie-Hellman (ECDHE),換到的是 forward secrecy:session key 不是從憑證的 key 推導出來的,所以就算 server 的 private key 日後外洩,去年錄下的流量還是解不開。至於憑證本身,它解的其實是 binding 問題:keypair 誰都能生,CA 的簽章才把這把 key 跟這個 hostname 綁死在一起。」

關鍵句型:"it buys you forward secrecy" / "captured traffic stays unreadable" / "the CA's signature ties this key to this hostname"。

---

## SIM #22: OAuth 2.0

**(A) 面試官怎麼問** (DC loop 愛考「講給非技術人聽」):

> EN: "Your customer's PM asks: our mobile app needs to read users' Google Calendar. Why can't we just ask users for their Google password? Explain what OAuth does, in terms a PM would follow, then take me through the actual flow."
>
> 中文:「customer 的 PM 問你:我們的 mobile app 要讀使用者的 Google Calendar,為什麼不能直接跟使用者要 Google 密碼?先用 PM 聽得懂的方式解釋 OAuth 在做什麼,再帶我走一遍實際的 flow。」

追問串:

- "Why does the flow exchange a code instead of returning the token directly?"(為什麼 flow 要先換一個 code,而不是直接回 token?)
- "What's PKCE for?"(PKCE 是在防什麼?)
- "What happens if an access token is stolen?"(access token 被偷走會怎樣?)

**(B) 口語組織骨架**:

1. 定位:給密碼 = 交出全部權限還不能收回;OAuth 給一張限定 scope、可撤銷的 token,這是 delegated authorization。
2. 機制:authorization code flow,browser 拿 code (前信道),server 拿 code 換 token (後信道),token 不經過瀏覽器。
3. 落點:mobile/SPA 藏不住 secret,加 PKCE;token 是 bearer,所以短效 + scope 最小 + 全程 TLS。
4. 鉤子:machine-to-machine 是另一條 client credentials flow,沒有使用者角色。

**(C) L6 model answer**:

英文版:

> "For the PM version: asking for the password means the app holds the keys to the user's entire Google account, and the only way to revoke it is changing the password. OAuth replaces that with a valet key: the user approves a specific scope, calendar read-only, and Google issues the app a token limited to exactly that, revocable any time. Technically it's the authorization code flow: the app redirects the user to Google, the user logs in and consents there, so credentials never touch our app, and we get back a one-time code through the browser. Our backend then exchanges that code for the access token server to server. The token never passes through the browser, which matters because tokens are bearer credentials, whoever holds one can use it. For a mobile app there's no safe place for a client secret, so we add PKCE to stop code interception. And we keep tokens short-lived with minimal scope to bound the damage if one leaks."

中文版:

> 「先講 PM 版:跟使用者要密碼,等於 app 握著他整個 Google 帳號的鑰匙,而且唯一的撤銷方式是改密碼。OAuth 把它換成一把 valet key (代客泊車鑰匙):使用者只授權一個特定 scope,比如 calendar 唯讀,Google 發給 app 一張只能做這件事的 token,隨時可撤銷。技術上這是 authorization code flow:app 把使用者 redirect 到 Google,登入和同意都在 Google 那邊做,所以密碼從頭到尾不經過我們的 app;我們透過瀏覽器拿回一個一次性的 code,後端再用 server-to-server 的方式拿 code 換 access token。token 不走瀏覽器這點很關鍵,因為 token 是 bearer credential,誰拿到誰就能用。Mobile app 藏不住 client secret,所以加 PKCE 擋 code 被攔截;然後 token 保持短效、scope 最小,就算洩漏,damage 也被框住。」

關鍵句型:"a valet key, not the master key" / "credentials never touch our app" / "bound the damage if one leaks"。

---

## SIM #23: OIDC

**(A) 面試官怎麼問** (通常接在 OAuth 後面當追問):

> EN: "You said OAuth is about authorization. So after that flow, how does the app actually know who the user is? What does OIDC add?"
>
> 中文:「你剛說 OAuth 管的是 authorization。那 flow 跑完之後,app 到底怎麼知道使用者是誰?OIDC 加了什麼?」

追問串:

- "What's inside an id_token and how do you verify it without calling the IdP?"(id_token 裡面有什麼?不回呼 IdP 要怎麼驗它?)
- "What's the difference between the id_token and the access token, can I use the id_token to call an API?"(id_token 和 access token 差在哪?拿 id_token 去打 API 行不行?)

**(B) 口語組織骨架**:

1. 定位:OAuth 回答「能不能存取」,沒標準答案給「你是誰」;OIDC 在同一套 flow 加一張 id_token。
2. 機制:id_token 是 JWT,拿 IdP 的 JWKS 公鑰本地驗簽,再查 iss/aud/exp,不用回源。
3. 落點:id_token 給 client 認人,access token 給 API 授權,拿 id_token 打 API 是經典誤用。
4. 鉤子:本地驗證 = stateless,這是它能撐大規模的原因,也是 IRSA 這類 workload federation 的地基。

**(C) L6 model answer**:

英文版:

> "OAuth on its own tells the app what it can access, but nothing standard about who the user is. Apps used to hack around it by calling some profile API, every provider differently. OIDC standardizes it: on top of the same code flow, the IdP also returns an id_token, a JWT signed by the IdP. The app fetches the IdP's public keys from its JWKS endpoint and verifies the signature locally, then checks the issuer, the audience, that it was issued for this app specifically, and expiry. No callback to the IdP needed, which keeps it stateless and scalable. The division of labor matters: the id_token is for the client to establish identity, the access token is for calling APIs. Sending an id_token to an API is a classic mistake, the API should reject it because the audience is wrong."

中文版:

> 「OAuth 本身只告訴 app 它能存取什麼,對『使用者是誰』沒有標準答案,以前大家各自去打 provider 的 profile API 繞出來,每家都不一樣。OIDC 把這件事標準化:在同一套 code flow 上,IdP 多回一張 id_token,一個由 IdP 簽章的 JWT。App 從 IdP 的 JWKS endpoint 抓公鑰,在本地驗簽章,再檢查 iss 是誰發的、aud 是不是發給我這個 app、exp 過期沒。整個驗證不用回呼 IdP,所以是 stateless 的,撐得起規模。分工要講清楚:id_token 是給 client 確認身分用的,access token 才是拿去打 API 的;拿 id_token 去打 API 是經典誤用,API 應該因為 audience 不對直接拒絕。」

關鍵句型:"the division of labor matters" / "verified locally against the JWKS" / "the audience is wrong"。

---

## SIM #24: SAML vs OIDC

**(A) 面試官怎麼問** (migration 對話的真實形狀):

> EN: "Your customer runs AD FS with SAML for all their enterprise SSO. Their dev team wants everything on OIDC because it's modern. As their consultant, what do you tell them?"
>
> 中文:「customer 的企業 SSO 全跑在 AD FS + SAML 上,dev team 想全面換成 OIDC,理由是比較現代。你是他們的 consultant,你怎麼建議?」

追問串:

- "What does SAML not give you that they might need later?"(SAML 給不了、但他們之後可能需要的是什麼?)
- "They also need user accounts provisioned in the target apps before first login. Does SAML handle that?"(他們還需要在使用者第一次登入前就把帳號開好,SAML 管這塊嗎?)

**(B) 口語組織骨架**:

1. 定位:兩個都是 federation 協定,差在世代:SAML 是 XML + browser POST 的企業 SSO 老將,OIDC 是 JSON/REST,原生適合 API、mobile、machine。
2. 機制:選擇由對接方決定,不是技術品味,既有 IdP 只講 SAML 就走 SAML,新 workload 走 OIDC,兩者長期並存。
3. 落點:AWS 端 IAM Identity Center 兩條都吃,SAML 管登入斷言,SCIM 補 provisioning。
4. 鉤子:consultant 的答案是遷移路徑,不是二選一。

**(C) L6 model answer**:

英文版:

> "I'd reframe it: this isn't a religious choice, it's decided by what each side of the connection speaks. SAML and OIDC do the same job, federate identity from an IdP to an application, but SAML is XML posted through the browser, built for enterprise web SSO, and OIDC is JSON over REST, built with APIs, mobile, and machine workloads in mind. Their AD FS estate speaks SAML today and it works, ripping it out has real migration cost and zero user-facing benefit. So my recommendation is coexistence: keep SAML for the existing enterprise apps, adopt OIDC for new services, anything that needs tokens for API calls, and plan the IdP so it can issue both. One trap to flag: SAML only asserts identity at login time, it doesn't create accounts in advance. If they need provisioning, that's a separate protocol, SCIM, running alongside."

中文版:

> 「我會先把問題重新框一下:這不是信仰選擇,是由連線兩端各講什麼協定決定的。SAML 和 OIDC 做的是同一件事,把身分從 IdP federate 到應用;差別是 SAML 是 XML 靠瀏覽器 POST,為企業 web SSO 而生,OIDC 是 JSON over REST,天生適合 API、mobile 和 machine workload。他們的 AD FS 現在講 SAML 而且運作正常,整套拔掉有實打實的遷移成本,對使用者卻沒有任何體感收益。所以我的建議是並存:既有企業應用留在 SAML,新服務、需要 token 打 API 的走 OIDC,IdP 規劃成兩種都能發。有一個坑要主動點出來:SAML 只在登入當下傳身分斷言,不會提前幫你開帳號;要 provisioning 得靠另一個協定 SCIM 並行處理。」

關鍵句型:"it's decided by what each side speaks" / "coexistence, not a rip-and-replace" / "SAML asserts identity, it doesn't provision accounts"。

---

## SIM #25: AWS 身分對應 (Identity Center / Cognito / IRSA)

**(A) 面試官怎麼問** (幾乎必考的 migration 收尾題):

> EN: "After the migration, the customer asks: our 300 employees all log in through Active Directory today. How should they access AWS? And separately, their customer-facing app has two million end users. Same solution?"
>
> 中文:「migration 完成後,customer 問:我們 300 個員工現在都用 Active Directory 登入,以後要怎麼進 AWS?另外,他們對外的 app 有兩百萬 end user,用同一套解法嗎?」

追問串:

- "Where do temporary credentials come from in each case?"(這幾種情況下,臨時憑證各是從哪來的?)
- "Their EKS workloads also need to call S3. Long-lived access keys in a Secret?"(他們的 EKS workload 也要呼叫 S3,把 long-lived access key 塞進 Secret 行嗎?)
- "How does a pod prove its identity to AWS without any stored credential?"(pod 在不存任何憑證的情況下,要怎麼向 AWS 證明自己的身分?)

**(B) 口語組織骨架**:

1. 定位:先切人群,員工 (workforce) 走 IAM Identity Center,app 使用者 (customer) 走 Cognito,workload 走 IRSA,三個不混用。
2. 機制:底層同一招,federation → STS 換短效憑證,全程沒有 long-lived key。
3. 落點:員工鏈 = AD ↔ (AD Connector 或 Entra ID) ↔ Identity Center ↔ permission sets;IRSA = pod 的 SA token 是 OIDC JWT,`AssumeRoleWithWebIdentity` 換憑證。
4. 鉤子:秒答「不要 IAM user、不要 access key in Secret」展現 security bar。

**(C) L6 model answer**:

英文版:

> "First I'd split the populations, because AWS has a different front door for each. The 300 employees are workforce identity: I'd connect their AD to IAM Identity Center, either directly with AD Connector or through Entra ID, and map AD groups to permission sets across the accounts. They keep their existing login, and nobody gets an IAM user or a long-lived access key. The two million app users are customer identity, that's Cognito: a user pool handles sign-up and sign-in and acts as an OIDC provider, and if the app needs to touch AWS resources directly, an identity pool trades that in for scoped temporary credentials. And for the EKS workloads, definitely no access keys in Secrets. With IRSA the pod's service account token is itself an OIDC JWT, the cluster's OIDC provider is registered with IAM as a trusted issuer, and the pod calls AssumeRoleWithWebIdentity to get short-lived role credentials. Three different populations, but underneath it's the same pattern every time: federate, then exchange for temporary credentials through STS. Nothing long-lived, anywhere."

中文版:

> 「我會先把人群切開,因為 AWS 對每一族有不同的入口。300 個員工是 workforce identity:把他們的 AD 接上 IAM Identity Center,直接用 AD Connector 或走 Entra ID 都行,再把 AD group 映射到各帳號的 permission set。員工用原本的方式登入,沒有任何人拿到 IAM user 或 long-lived access key。兩百萬 app 使用者是 customer identity,那是 Cognito 的事:user pool 管註冊登入、本身就是一個 OIDC provider;app 要直接碰 AWS 資源的話,identity pool 把身分換成限定 scope 的臨時憑證。至於 EKS workload,絕對不要把 access key 塞進 Secret:IRSA 的做法是,pod 的 service account token 本身就是一張 OIDC JWT,cluster 的 OIDC provider 註冊進 IAM 當受信任的 issuer,pod 拿 token 呼叫 AssumeRoleWithWebIdentity 換短效的 role 憑證。三族人,底層其實是同一個 pattern:federation,然後透過 STS 換臨時憑證。任何地方都不留 long-lived credential。」

關鍵句型:"a different front door for each population" / "trades it in for scoped temporary credentials" / "nothing long-lived, anywhere"。

---

## SIM #26: KMS envelope encryption

**(A) 面試官怎麼問** (FSI 客戶對話的形狀):

> EN: "Your FSI customer's security team pushes back: 'KMS can only encrypt 4 kilobytes at a time, so how is AWS supposedly encrypting our terabyte database with it?' Explain envelope encryption to them."
>
> 中文:「FSI customer 的 security team 質疑:『KMS 一次只能加密 4KB,那 AWS 是怎麼用它加密我們 TB 級的 database 的?』跟他們解釋 envelope encryption。」

追問串:

- "Why doesn't the master key just leave KMS to do the work locally?"(為什麼不讓 master key 離開 KMS 到本地做事就好?)
- "What do you actually store next to the ciphertext?"(密文旁邊實際存的是什麼?)
- "What happens to all the data if the customer disables the KMS key?"(customer 把 KMS key 停用,所有資料會怎樣?)

**(B) 口語組織骨架**:

1. 定位:KMS key 從不加密資料本體,它加密的是「加密資料的那把 key」,兩層包裝,所以叫 envelope。
2. 機制:`GenerateDataKey` 拿 data key → 本地對稱加密資料 → 存密文 + 被包住的 data key;解密把包住的 data key 送回 KMS 拆開。
3. 落點:KMS key 不出 HSM,每次使用留 CloudTrail;key policy + IAM 雙重 gate。
4. 鉤子:停用 KMS key = 廢掉所有它包過的 data key,這就是 crypto-shredding,對法遵是 feature 不是 bug。

**(C) L6 model answer**:

英文版:

> "The 4-kilobyte limit is actually the design, not a limitation to work around. The KMS key never encrypts your data, it encrypts the key that encrypts your data. When a service needs to encrypt something big, it calls GenerateDataKey: KMS hands back a fresh symmetric data key twice, once in plaintext, once wrapped by the KMS key. The service encrypts the terabyte locally with the plaintext key, fast symmetric crypto, then throws the plaintext away and stores the wrapped copy right next to the ciphertext. Decryption reverses it: send the wrapped key to KMS, and only if the key policy and IAM both allow it, you get the plaintext key back for local use. That buys three things the security team cares about: the master key never leaves the HSM, every single use is a CloudTrail event, and revocation is instant, disable the KMS key and every data key it ever wrapped becomes garbage. That last one is crypto-shredding, and for a regulated customer it's a compliance feature: destroying one key provably destroys the data."

中文版:

> 「4KB 的上限其實就是設計本身,不是要繞過的限制。KMS key 從來不加密你的資料,它加密的是『加密你資料的那把 key』。服務要加密大東西時,呼叫 GenerateDataKey:KMS 回傳一把新的對稱 data key,給兩份,一份明文、一份被 KMS key 包住。服務用明文那份在本地加密整個 TB,走的是快速的對稱加密,然後把明文丟掉,把包住的那份跟密文存在一起。解密反過來:把包住的 data key 送回 KMS,key policy 和 IAM 兩道都放行,才拿回明文 key 在本地解。這買到 security team 在乎的三件事:master key 永遠不離開 HSM;每一次使用都是一筆 CloudTrail 事件;撤銷是即時的,停用 KMS key,它包過的所有 data key 瞬間變垃圾。最後這個就是 crypto-shredding,對受監理的 customer 來說是法遵 feature:銷毀一把 key,就可證明地銷毀了資料。」

關鍵句型:"it encrypts the key that encrypts your data" / "every single use is a CloudTrail event" / "destroying one key provably destroys the data"。

---

## SIM #27: At-rest 加密各服務落地

**(A) 面試官怎麼問**:

> EN: "The customer's policy says everything encrypted at rest, no exceptions. Across EBS, S3, and RDS, what does that actually take, and where are the traps in a migration?"
>
> 中文:「customer 的 policy 是 at rest 一律加密,無例外。對 EBS、S3、RDS,實際要做哪些事?migration 的時候坑在哪?」

追問串:

- "They have an unencrypted RDS running in prod already. Can you just flip encryption on?"(prod 已經有一台沒加密的 RDS,直接把加密打開行嗎?)
- "Their data lake does millions of S3 PUTs per hour with SSE-KMS. What breaks?"(data lake 每小時對 S3 做幾百萬次 PUT,用 SSE-KMS,什麼會壞?)
- "How do you make 'no exceptions' enforceable instead of a checklist?"(「無例外」怎麼從 checklist 變成強制的?)

**(B) 口語組織骨架**:

1. 定位:三個服務全是 envelope encryption 的應用,對 OS/app 透明;工作量不在打開,在邊角。
2. 機制:RDS 加密只能建庫時決定,事後要 snapshot → encrypted copy → restore,是一次 cutover;S3 SSE-KMS 高流量撞 KMS throttling,開 bucket key 聚合呼叫。
3. 落點:帳號層 EBS encryption by default;跨帳號分享加密 snapshot 要 key 授權。
4. 鉤子:enforcement 用 SCP + Config rule 做成不可關的地板,這才是 consultant 級答案。

**(C) L6 model answer**:

英文版:

> "Turning encryption on is the easy part, all three services ride on envelope encryption and it's transparent to the OS and the app. The real work is in the corners. EBS: set encryption-by-default at the account level so nobody can create an unencrypted volume even by accident. S3: choose between SSE-S3 and SSE-KMS, and if they want their own key with audit trails, it's SSE-KMS, but at data-lake volume every object operation hits the KMS API and you'll throttle, so enable S3 Bucket Keys to amortize those calls. RDS is the migration trap: encryption is decided at creation time and there is no flip-the-switch later. The path is snapshot, copy the snapshot with encryption, restore, and that's a cutover with downtime you must plan, not a checkbox. Related trap: sharing encrypted snapshots across accounts requires granting the target account use of the KMS key. And to make 'no exceptions' real, I wouldn't hand them a checklist, I'd land an SCP plus Config rules in the landing zone so unencrypted resources can't be created in the first place, prevention over detection."

中文版:

> 「把加密打開是最簡單的部分,三個服務底層都是 envelope encryption,對 OS 和 app 透明。真正的工作在邊角。EBS:在帳號層開 encryption-by-default,誰都不可能再手滑建出沒加密的 volume。S3:在 SSE-S3 和 SSE-KMS 之間選,要自己的 key、要 audit trail 就是 SSE-KMS,但 data lake 的量級下每個 object 操作都打 KMS API,一定撞 throttling,開 S3 Bucket Key 把呼叫攤平。RDS 是 migration 的坑:加密是建庫當下決定的,之後沒有開關可以撥。路徑是 snapshot → copy 時加密 → restore,那是一次要排停機窗口的 cutover,不是一個 checkbox。連帶的坑:加密 snapshot 跨帳號分享,要先把 KMS key 的使用權授給對方帳號。至於怎麼讓『無例外』成真:我不會給他們 checklist,我會在 landing zone 裡放 SCP 加 Config rule,讓沒加密的資源從一開始就建不出來,prevention over detection。」

關鍵句型:"the real work is in the corners" / "a cutover, not a checkbox" / "prevention over detection"。

---

## SIM #28: Secrets 管理

**(A) 面試官怎麼問** (discovery 階段的真實發現):

> EN: "During migration discovery you find database passwords hardcoded in config files on every server, some in the AMI itself. The customer asks what the target state should look like. What's your recommendation?"
>
> 中文:「migration discovery 的時候,你發現每台 server 的設定檔裡都硬編碼著 database 密碼,有些還烤在 AMI 裡。customer 問目標態應該長什麼樣。你的建議?」

追問串:

- "Secrets Manager or Parameter Store, how do you choose?"(Secrets Manager 還是 Parameter Store,怎麼選?)
- "How does the app get the secret at runtime without a new credential problem?"(app 在 runtime 怎麼拿到 secret,又不製造新的憑證問題?)
- "What does rotation look like without breaking the app?"(rotation 怎麼做才不會弄壞 app?)

**(B) 口語組織骨架**:

1. 定位:設定檔裡的密碼有三宗罪:不可稽核、不可輪換、跟著 AMI/repo 到處複製。目標態是 runtime 用 IAM 身分去取,密碼不落地。
2. 機制:Secrets Manager (內建 rotation、跨帳號、較貴) vs Parameter Store SecureString (便宜、無 rotation);底層都是 KMS。
3. 落點:取用鏈 = instance/task 的 role → GetSecretValue → 每次讀取留 CloudTrail;ECS/EKS 有原生注入。
4. 鉤子:這解的是「secret zero」問題:app 的身分本身由平台發 (role),所以不需要「用一個密碼去保護另一個密碼」。

**(C) L6 model answer**:

英文版:

> "Hardcoded passwords have three problems: you can't audit who read them, you can't rotate them without touching every server, and they replicate, into AMIs, into git history, into backups. The target state is that secrets live in a managed store encrypted with KMS, and the app fetches them at runtime using its platform identity. Between the two options: Parameter Store's SecureString is fine for plain config, but for database credentials I'd pick Secrets Manager, because built-in rotation is the point, it runs a Lambda that changes the database password on schedule, and the app never notices because it always fetches current. The elegant part is how it dodges the secret-zero problem: the app doesn't authenticate to the store with another password, its EC2 instance role or ECS task role or IRSA is its identity, issued by the platform as short-lived credentials. So the access chain is role, then GetSecretValue, and every read is a CloudTrail event. In the migration plan this lands in Mobilize: it's part of the landing zone baseline, and the config files get cleaned as each wave moves."

中文版:

> 「硬編碼的密碼有三宗罪:讀過的人無從稽核、要輪換就得碰每一台 server、而且它會自我複製,進 AMI、進 git history、進備份。目標態是:secret 放在用 KMS 加密的託管儲存裡,app 在 runtime 用它的平台身分去取。兩個選項之間:一般設定用 Parameter Store 的 SecureString 就夠,但 database 憑證我會選 Secrets Manager,因為內建 rotation 才是重點,它掛一個 Lambda 定期改掉 database 密碼,而 app 每次都拿最新版,完全無感。優雅的地方在它繞開了 secret zero 問題:app 不是用另一個密碼去跟儲存庫認證,EC2 instance role、ECS task role 或 IRSA 就是它的身分,由平台直接發短效憑證。所以整條取用鏈是 role → GetSecretValue,每一次讀取都是一筆 CloudTrail。放進 migration 計畫的話,這件事落在 Mobilize:是 landing zone baseline 的一部分,設定檔跟著每個 wave 搬遷時順手清掉。」

關鍵句型:"they replicate, into AMIs, into git history" / "rotation is the point" / "its role is its identity, no secret zero"。
