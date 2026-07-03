# 術語登記簿 (英文術語間隔複習用)
<!-- 每次學到新術語就加一行,定期抽考自己能不能用英文解釋它 -->
<!-- 下次抽考日建議: 學習後 3 天,答對後推 7 天,再答對推 14 天 -->

| 術語 (EN) | 發音 | 一句英文定義 | 中文點破 | 學習日 | 下次抽考日 |
|-----------|------|-------------|---------|--------|-----------|
| declarative | /dɪˈkler.ə.tɪv/ | You describe the desired end state; the system figures out how to get there. | 你只宣告「最終要長怎樣」,不管「怎麼做到」,k8s 的核心世界觀 | 2026-06-17 | 2026-06-20 |
| imperative | /ɪmˈper.ə.tɪv/ | You command each step explicitly to reach a result. | 命令式,你親自管每一步,跟 declarative 相反 | 2026-06-17 | 2026-06-20 |
| reconcile loop | /ˈrek.ən.saɪl luːp/ | A controller's continuous loop that compares the desired state with the actual state and takes action to close the gap. | 「差距偵測 + 自動修正」的無限迴圈,是 Kubernetes 一切自動化的底層引擎 | 2026-06-17 | 2026-06-27 |
| desired state | /dɪˈzaɪərd steɪt/ | The end state you declare you want; controllers work to make the actual state match it. | 你宣告「想要的樣子」,是 reconcile loop 比對的基準 | 2026-06-17 | 2026-06-20 |
| control plane | /kənˈtroʊl pleɪn/ | The set of components that manage the cluster and make global decisions (API Server, etcd, scheduler, controllers). | 叢集的「大腦團隊」,負責管理與決策,不是單一元件 | 2026-06-17 | 2026-07-01 |
| API Server | /ˌeɪ.piːˈaɪ ˈsɝː.vɚ/ | The single front door to the cluster; every component reads and writes state only through it. | 唯一入口/守門人,萬物皆透過它,彼此不直接溝通 | 2026-06-17 | 2026-07-10 (2026-07-03 抽考:內容窗口+唯一碰etcd 對,但用中文答沒用英文;學員反問「為何這樣設計」自己推出攻擊面/介面抽象化,教練補第三層「集中把關」=RBAC/admission/schema 只驗一次。推+7,**下次逼英文作答**) |
| etcd | /ˈet.siː.diː/ | The cluster's key-value store; the single source of truth holding the desired state. | 叢集的帳本/唯一真相,掛了等於叢集失憶 | 2026-06-17 | 2026-06-20 |
| controller | /kənˈtroʊl.ɚ/ | A control-plane component running a reconcile loop: it watches desired state and drives actual state to match. | reconcile loop 的主人,k8s 自動化的執行單位 | 2026-06-17 | 2026-06-20 |
| scheduler | /ˈsked.juː.lɚ/ | A control-plane component that assigns each unscheduled Pod to a suitable node via filter then score. | 幫孤兒 Pod 挑 node 的排程器,挑完只寫綁定(透過 API Server)、不啟動容器 | 2026-06-17 | 2026-07-01 |
| Pending | /ˈpen.dɪŋ/ | A Pod phase meaning it is accepted but not yet scheduled onto a node. | 已被接受但還沒排到 node 的狀態,常因 scheduler filter 找不到機器 | 2026-06-17 | 2026-06-20 |
| compressible resource | /kəmˈpres.ə.bəl/ | A resource you can throttle without killing the workload: give it less and it just runs slower (CPU). | 可壓縮資源(CPU),給少一點只是變慢、不會死,所以超 limit 是 throttle | 2026-06-24 | 2026-07-06 (WR#1 第一性原理打穿,水龍頭流速比喻) |
| incompressible resource | /ˌɪn.kəmˈpres.ə.bəl/ | A resource that can't be reclaimed once handed out: you either have the byte or you don't (memory), so exceeding the limit means the process gets killed. | 不可壓縮資源(memory),還不回來,超 limit 只能砍 → OOMKilled | 2026-06-24 | 2026-07-06 (WR#1 第一性原理打穿,水桶存量比喻) |
| OOMKilled | /ˌoʊ.oʊˈem kɪld/ | A container killed by the kernel's OOM killer (exit code 137 = SIGKILL) for exceeding its cgroup memory limit. | 容器吃爆自己 cgroup 的 memory limit,被 kernel OOM killer 砍,exit 137 | 2026-06-24 | 2026-07-06 (WR#1 概念盲講 PASS) |
| thundering herd | /ˈθʌn.dər.ɪŋ hɝːd/ | Many clients hit the same resource at the exact same moment and overwhelm it (e.g. all pods restart and reconnect to one DB at once). | 羊群效應:大量請求同時湧向同一資源把它壓垮(如全 Pod 同時重連 DB);錨定 liveness 誤設→集體重啟雪崩 | 2026-06-25 | 2026-07-07 (2026-07-03 抽考:概念「同時失效壓垮」PASS,但英文詞想不起來→教練給。概念穩、英文詞需再刷,拉近期) |
| DNAT | /ˌdiːˈnæt/ | Destination NAT: rewriting a packet's destination IP. kube-proxy uses it so a packet sent to a virtual ClusterIP gets its destination rewritten to a real Pod IP. | 改寫封包的「目的地 IP」。ClusterIP 虛擬不存在於任何網卡,封包在出發 node 本地被 DNAT 成某個真實 Pod IP,這就是 Service 能轉發的底層 | 2026-06-26 | 2026-07-06 (WR#1 概念盲講 PASS) |
| kube-proxy | /kjuːb ˈprɑːk.si/ | A per-node DaemonSet that programs iptables/IPVS rules in each node's kernel to implement Service ClusterIP routing (no central proxy, no bottleneck). | 每台 node 跑一隻,在本地 kernel 寫 iptables/ipvs 規則實作 ClusterIP 轉發;去中心化、無中央瓶頸;注意它「寫規則」不是「過流量」 | 2026-06-26 | 2026-07-06 (WR#1 概念盲講 PASS) |
| conntrack | /ˈkɒn.træk/ | The Linux kernel netfilter table that remembers each NAT'd connection so reply packets can be rewritten back. When it fills up, NEW connections get dropped while existing ones keep working. | NAT 的「記憶體」:去程 DNAT 改了 A→B 就記一筆,回程才反向改回去;table full=新連線被 drop、舊連線不受影響;屬 node kernel 層,kubectl 看不到(查法 conntrack -L / nf_conntrack_count vs _max / dmesg) | 2026-06-28 | 2026-07-04 (2026-07-01 英文抽考:概念+記錄映射方向對,英文可用;但「table full 新 vs 舊」精度掉了→復述問題沒定案,教練直接補「舊連線照常/新連線被 drop」。近期再抽) |

| Ingress Controller | /ˈɪn.ɡres kənˈtroʊl.ɚ/ | The actual running pod (e.g. nginx/traefik) that watches Ingress objects and does the real L7 routing; the Ingress object itself is just rules. | Ingress 物件只是規則,Controller 才是真的收 HTTP、看 URL、轉發的引擎;沒裝它 Ingress 等於白寫 | 2026-07-01 | 2026-07-04 |

<!-- 2026-06-22 移除 kubeconfig / context / kind 三張卡:定義型瑣碼詞/工具名,面試不考,違反價值門檻(見 SKILL.md 術語卡)。current-context 改記為 ops 安全習慣,不當單字卡。 -->
<!-- ops 安全習慣(非術語卡): `kubectl config current-context` = 動手前先確認指到哪個叢集,避免誤打 prod EKS。 -->

