# 英文術語總表

> **如何使用此檔:** 這是跨所有 phase 的術語 master list。
> Teaching Flow C 段每做一張術語卡,同步把術語加進來(格式如下)。
> 間隔複習的詳細追蹤(學習日/下次抽考日)放在 `workspaces/k8s/term-registry.md`;
> 本檔是「定義的唯一正確來源」,term-registry.md 是「抽考排程的追蹤簿」。
>
> 使用規則: 新術語先查本檔有沒有;有的話用本檔定義,不要另起一個版本(避免定義分歧)。

---

## 欄位說明

| 欄位 | 說明 |
|------|------|
| **EN term** | 英文原文,k8s/SRE 官方用詞 |
| **發音** | IPA 音標 |
| **One-line English definition** | 用最簡單的英文說清楚這個詞的本質,面試可直接用 |
| **中文點破** | 一句話抓住精髓,不是翻譯,是「懂了就不忘」的點破 |
| **首見 phase** | 術語首次在哪個 phase 被引入 |

---

## P0 術語 (C-0 宣告式)

| EN term | 發音 | One-line English definition | 中文點破 | 首見 phase |
|---------|------|----------------------------|---------|-----------|
| declarative | /ˈdek.lər.ə.tɪv/ | You specify the desired end state; the system figures out how to get there | 說「要什麼」,不說「怎麼做」 | P0 |
| idempotent | /aɪˈdem.pə.tənt/ | Applying the same operation multiple times produces the same result as applying it once | 重複做不會產生副作用:apply 100 次等於 apply 1 次 | P0 |
| desired state | /dɪˈzaɪərd steɪt/ | The configuration you declared in your manifest, persisted in etcd as the target | 你宣告的理想終態,存在 etcd 裡 | P0 |

---

## P0 術語 (C-1 Reconcile Loop)

| EN term | 發音 | One-line English definition | 中文點破 | 首見 phase |
|---------|------|----------------------------|---------|-----------|
| reconcile | /ˈrek.ən.saɪl/ | The act of comparing actual state to desired state and taking actions to eliminate the difference | 把「現實」調整到符合「理想」,差多少就修多少 | P0 |
| controller | /kənˈtroʊ.lər/ | A control loop that continuously watches desired state and acts to achieve it | 跑 reconcile loop 的元件,每種 k8s 物件類型有自己的 controller | P0 |
| level-triggered | /ˈlev.əl ˈtrɪɡ.ərd/ | Responds to the current state of the world, not to the events that caused that state | 看「現在是什麼狀態」,不管「之前發生什麼事」,controller 重啟不丟狀態 | P0 |
| watch | /wɒtʃ/ | A long-lived API request to the API server that streams state changes as they happen | 對 API server 的長連線訂閱,etcd 有變化時即時推送給 watcher | P0 |

---

## P0 術語 (C-2 Control Plane)

| EN term | 發音 | One-line English definition | 中文點破 | 首見 phase |
|---------|------|----------------------------|---------|-----------|
| control plane | /kənˈtroʊl pleɪn/ | The set of components that make global decisions about the cluster and detect/respond to cluster events | 掌舵那一層: api-server + etcd + scheduler + controller-manager | P0 |
| kubelet | /ˈkjuːb.lɪt/ | The node agent that ensures containers described in PodSpecs are running and healthy | 每個 Node 上的現場代理人,負責把 Pod 實際跑起來並回報狀態 | P0 |
| static pod | /ˈstæt.ɪk pɒd/ | A pod managed directly by kubelet from a local manifest file, independent of the API server | kubelet 直讀磁碟 YAML 啟動的 Pod,api-server 掛了也能活著 | P0 |
| CRI | /siː ɑːr aɪ/ | Container Runtime Interface: the plugin API between kubelet and the container runtime (containerd, CRI-O) | kubelet 和 container runtime 說話的標準介面,kubelet 不綁死某一個 runtime | P0 |

---

## P0 術語 (C-3 apply 到 Running 流程)

| EN term | 發音 | One-line English definition | 中文點破 | 首見 phase |
|---------|------|----------------------------|---------|-----------|
| scheduler | /ˈʃɛd.juː.lər/ | The control-plane component that watches for newly created Pods with no assigned node and assigns them a node | 決定每個新 Pod 去哪個 Node 跑,只做這一件事 | P0 |
| admission control | /ədˈmɪʃ.ən kənˈtroʊl/ | A plugin chain in the API server that validates and mutates requests before objects are persisted | API server 的關卡鏈:可以修改(mutate)或拒絕(validate)送進來的物件 | P0 |
| authn | /ˌɔːˌθen.tɪˈkeɪʃ.ən/ | Authentication: verifying the identity of the entity making the request | 確認「你是誰」(身份驗證) | P0 |
| authz | /ˌɔːˌθər.ɪˈzeɪʃ.ən/ | Authorization: deciding whether the authenticated entity is permitted to perform the requested action | 確認「你能不能做這件事」(授權) | P0 |
| unscheduled pod | /ʌnˈʃɛd.juːld pɒd/ | A Pod that has been created but has no `spec.nodeName` assigned yet; the scheduler's work target | 已建立但還沒被分配 Node 的 Pod,scheduler 的工作對象 | P0 |

---

## P0 術語 (C-4 etcd)

| EN term | 發音 | One-line English definition | 中文點破 | 首見 phase |
|---------|------|----------------------------|---------|-----------|
| etcd | /ˈɛt.siː.diː/ | The distributed key-value store that holds all Kubernetes cluster state | k8s 的唯一 source of truth,所有 k8s 物件都存在這裡 | P0 |
| Raft | /ræft/ | A consensus algorithm that ensures all nodes in a distributed system agree on the same sequence of state changes | 讓多個 etcd 節點保持一致的算法,解決「多個節點誰說了算」的問題 | P0 |
| quorum | /ˈkwɔːr.əm/ | The minimum number of nodes that must agree for an operation to be committed (majority = floor(N/2) + 1) | 法定人數,多數決: 3 節點 quorum = 2,能容忍 1 個掛掉 | P0 |
| source of truth | /sɔːrs ɒv truːθ/ | The authoritative data store that all components reference to determine the real, desired state | 唯一的權威狀態來源,k8s 裡是 etcd,誰都得聽它的 | P0 |

---

## P0 術語 (C-5 容器底層)

| EN term | 發音 | One-line English definition | 中文點破 | 首見 phase |
|---------|------|----------------------------|---------|-----------|
| Linux namespace | /ˈlɪnʌks ˈneɪm.speɪs/ | A kernel feature that isolates a set of system resources so each container gets its own view | 讓 container「看不到」host 和其他 container 的資源:PID/net/mnt/uts 各一套 | P0 |
| cgroup | /ˈsiː.ɡruːp/ | Control Groups: a Linux kernel mechanism that limits, accounts for, and isolates resource usage of process groups | 限制 container「能用多少」CPU 和記憶體,k8s resource limits 的底層實現 | P0 |
| OOM killer | /oʊ oʊ ɛm ˈkɪlər/ | The Linux kernel mechanism that selects and kills processes when the system runs out of memory | 記憶體耗盡時,kernel 選一個 process 殺掉;container 超過 memory limit 就會被它選中 | P0 |

---

## P1 術語(P1 填)

> (P1 填): liveness probe, readiness probe, startup probe, QoS class (Guaranteed/Burstable/BestEffort), CFS scheduler, OOM score, PID 1 problem, init container, sidecar.

---

## P2a 術語(P2a 填)

> (P2a 填): kube-proxy, iptables, IPVS, conntrack, ClusterIP, NodePort, LoadBalancer, Ingress, CNI, veth pair, bridge, overlay network, CIDR, CoreDNS, ndots, TIME_WAIT.

---

## P2b 術語(P2b 填)

> (P2b 填): PersistentVolume, PersistentVolumeClaim, StorageClass, CSI, RBAC, ServiceAccount, ClusterRole, RoleBinding, IRSA, OIDC.

---

## P3+ 術語(P3 以後填)

> (P3+ 填): affinity, anti-affinity, taint, toleration, topologySpreadConstraint, HPA, VPA, Karpenter, PodDisruptionBudget, bin-packing, node pressure, eviction, USE method, RED method.
