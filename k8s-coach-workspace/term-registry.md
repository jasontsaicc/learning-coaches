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
| API Server | /ˌeɪ.piːˈaɪ ˈsɝː.vɚ/ | The single front door to the cluster; every component reads and writes state only through it. | 唯一入口/守門人,萬物皆透過它,彼此不直接溝通 | 2026-06-17 | 2026-06-20 |
| etcd | /ˈet.siː.diː/ | The cluster's key-value store; the single source of truth holding the desired state. | 叢集的帳本/唯一真相,掛了等於叢集失憶 | 2026-06-17 | 2026-06-20 |
| controller | /kənˈtroʊl.ɚ/ | A control-plane component running a reconcile loop: it watches desired state and drives actual state to match. | reconcile loop 的主人,k8s 自動化的執行單位 | 2026-06-17 | 2026-06-20 |
| scheduler | /ˈsked.juː.lɚ/ | A control-plane component that assigns each unscheduled Pod to a suitable node via filter then score. | 幫孤兒 Pod 挑 node 的排程器,挑完只寫綁定(透過 API Server)、不啟動容器 | 2026-06-17 | 2026-07-01 |
| Pending | /ˈpen.dɪŋ/ | A Pod phase meaning it is accepted but not yet scheduled onto a node. | 已被接受但還沒排到 node 的狀態,常因 scheduler filter 找不到機器 | 2026-06-17 | 2026-06-20 |
| compressible resource | /kəmˈpres.ə.bəl/ | A resource you can throttle without killing the workload: give it less and it just runs slower (CPU). | 可壓縮資源(CPU),給少一點只是變慢、不會死,所以超 limit 是 throttle | 2026-06-24 | 2026-06-27 |
| incompressible resource | /ˌɪn.kəmˈpres.ə.bəl/ | A resource that can't be reclaimed once handed out: you either have the byte or you don't (memory), so exceeding the limit means the process gets killed. | 不可壓縮資源(memory),還不回來,超 limit 只能砍 → OOMKilled | 2026-06-24 | 2026-06-27 |
| OOMKilled | /ˌoʊ.oʊˈem kɪld/ | A container killed by the kernel's OOM killer (exit code 137 = SIGKILL) for exceeding its cgroup memory limit. | 容器吃爆自己 cgroup 的 memory limit,被 kernel OOM killer 砍,exit 137 | 2026-06-24 | 2026-06-27 |

<!-- 2026-06-22 移除 kubeconfig / context / kind 三張卡:定義型瑣碼詞/工具名,面試不考,違反價值門檻(見 SKILL.md 術語卡)。current-context 改記為 ops 安全習慣,不當單字卡。 -->
<!-- ops 安全習慣(非術語卡): `kubectl config current-context` = 動手前先確認指到哪個叢集,避免誤打 prod EKS。 -->

