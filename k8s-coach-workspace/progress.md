# 學習進度卡 (斷點續傳)
<!-- 每次 session 開始前更新這裡,讓 Claude 快速掌握你的狀況,避免重複解釋背景 -->

## 基本資訊

| 欄位 | 內容 |
|------|------|
| 目前 phase | **P2a 網路深水區**(P1 已畢業 2026-06-25,P0 2026-06-22)|
| 目前主題 | **P2a chunk 1 進行中**(Service/kube-proxy/CoreDNS)。謎題A(Service→Endpoints→reconcile)✅;謎題B(ClusterIP虛擬→kube-proxy iptables DNAT→去中心化)C段已講,Feynman Gate **未確認**(學員停在電話比喻 mapping);conntrack/CoreDNS/D段lab **未做** |
| 上次 session 日期 | 2026-06-26 |
| session 累計次數 (session_count) | 7 |
| 上次 Weekly Review (last_weekly_review) | 0 |

## 診斷結果 (New Student Warm-Up)

程度: 中 (有地圖形狀,缺演員名字)。pacing = P0 剛好,不加速。

- 強: 已有 reconcile 直覺 (原話「比對現有環境進行更新」);知道 rolling update 替換 Pod。
- 洞 1: 用「下指令」框架 = 還停在 imperative 思維 (k8s 是 declarative)。
- 洞 2: 各步驟「誰做的」全省略 (API Server / etcd / controller / scheduler / kubelet 都沒提到)。
- 洞 3: 漏掉 Pod 怎麼被排到某台 node (scheduler 指派 + kubelet 啟動)。

## 未完成 lab

- [x] D 段 kind lab:apply hello-nginx → 用 `kubectl get events --sort-by` 看五棒 → delete pod 看 reconcile 自動補(新尾碼/新 IP)→ scale=0 證明改 DESIRED 才停。全做完。
- [x] **架構定案(2026-06-22):全部一個 repo = 本 skill repo `k8s-mastery-lab-skill`(= `~/jason/k8s-coach`,remote 已設,push 正常)**。學習產出放 `portfolio/`(notes/ 筆記+踩坑、manifests/ 練習)。舊的獨立 `~/jason/k8s-portfolio` 已刪除合併。見 memory [[k8s-portfolio-value-gate]]。P0 apply→Running 圖太基礎,學員畫私人筆記本即可,不進 repo。

## 下一步

> 下次繼續(一句話):**P2a chunk 1 接 謎題B 收尾** —— 先讓學員把電話比喻 mapping 回 k8s(代表號=ClusterIP / 分機=Pod IP / 每支話機的轉接表=kube-proxy iptables 規則 / 總機小姐=中央LB瓶頸)確認 DNAT+去中心化過 Feynman Gate,再教 **conntrack**(NAT 要記住連線狀態才能轉回程封包;遷移題「conntrack table 滿了會怎樣?怎麼查?」)+ **CoreDNS**(service name→ClusterIP 解析),然後 **D段 kind lab**(apply backend Deployment+Service,`get svc`/`get endpoints` 看 ClusterIP 與清單,scale 看 Endpoints 增減,`iptables-save | grep <clusterip>` 看 DNAT 規則)。phase-2a 教材檔仍未建,從第一性原理教。English Ramp 已進「加英文短句」檔位,但學員今天偏中文,下次溫和要 Say-it-in-English。EKS P2a 起可進場(terraform 指令由 user 親手跑,命名 `billing-dev-eks-*`)。
> ⚠️ **安全鐵律(2026-06-25 現場抓到)**:user 的 `KUBECONFIG=/home/ec2-user/.kube/eks/config.yaml`,**current-context 預設是 `eks` → 指向公司 PROD `billing-devops-prod-platform`**!本地 kind 的 context 名叫 **`kind`**(cluster=`kind-k8s-coach-p0`)。每次動手 lab 前先叫他 `kubectl config use-context kind` + `current-context` 確認回 `kind` 才 apply,否則打到 prod。
> 環境:kind 叢集 `k8s-coach-p0` 仍在(3 節點:control-plane + worker + worker2,健康)。**metrics-server 已裝**(2026-06-25,kind 需 `--kubelet-insecure-tls` 旗標跳過自簽憑證驗證,patch 後等 rollout+首次 scrape 才 `apiservice v1beta1.metrics.k8s.io` Available;`kubectl top` 可用,P3 HPA 有得吃)。殘留 `rollout-demo`(4/4 Running,無妨)、`hello-nginx`(0/0)。**P1 Gate 三隻故障 Pod**(payment-api/cache-worker/web-frontend)還在跑,清理:`kubectl --context kind delete pod payment-api cache-worker web-frontend`。Gate manifest 在 scratchpad `p1-gate-chaos.yaml`(非 portfolio)。lab 檔在 `portfolio/manifests/`。學員偏好自己敲指令,YAML 預設給規格。學員用英文作答時附 `💬 English Polish`;教完流程主動附英文 mind map 供手抄默畫。
> commit 規則:user 全域禁止任何 trailer/Co-Authored-By,commit message 一行。
> 待補精準度:術語要用「DESIRED vs CURRENT」「reconcile loop 收斂」而非「監控數量」。**新補洞**:只有 API Server 直接讀寫 etcd,其他元件(controller/scheduler/kubelet)都透過 API Server 的 watch/update,不直接碰 etcd(P0 學員口誤「kubelet 寫回 etcd」)。etcd Raft 深入 park 到 P5/foundations。
> English Ramp:P1 仍維持「只做術語卡」(P0-P1 同一檔位),P2a 起才加英文短句。

## 補充筆記

- 學員背景: DevOps 工程師,hands-on 有 (kubectl apply / 看 logs),底層理論弱;coding 初學。
- 教法備忘: 多用生活 analogy、用學員原話回扣、一次一個 chunk、語言要白。
- chunk map (P0): [1] declarative+reconcile → [2] API Server+etcd → [3] controller 怎麼 reconcile → [4] scheduler 指派 node → [5] kubelet 啟動容器。全部 ✅。
- chunk map (P1): [1] container=namespace+cgroup 圈的行程(vs VM 共用 kernel)✅ → [2] Pod 為何存在(共享 network ns,pause container,sidecar,同生共死才放同 Pod)✅ → [3] probe ✅✅(D/E 段動手做完:busybox+exec probe 用 /tmp/ready /tmp/alive 信物,rm readiness→endpoint 消失但 RESTARTS 0、STATUS 仍 Running;rm liveness→RESTARTS+1 後 command 重 touch 自癒。學員兩次預測全中,還自己從「rm:No such file」反推出「尚未 restart」。偵測延遲=failureThreshold×periodSeconds=調校旋鈕,回扣 liveness 查 DB 雪崩。lab 檔在 portfolio/manifests/probe-demo.yaml)→ [4] Deployment/rollout ✅✅(見下 session 4)→ [5] resource/QoS/OOM ✅✅(見下 session 5)。
- chunk map (P2a): [1] Service/kube-proxy/CoreDNS → 謎題A Service→Endpoints(selector+reconcile+readiness)✅ / 謎題B ClusterIP→kube-proxy iptables DNAT 去中心化 🟡(C段講完,Gate未確認)/ conntrack ⬜ / CoreDNS ⬜ / D段lab ⬜。後續 chunk: [2] Ingress [3] NetworkPolicy [4] CNI+封包全鏈路。
- session 7 (2026-06-26): **P2a chunk 1 開講(Service/kube-proxy)**,C段概念為主,**無 lab/E/F**(學員下班喊停,Gap Mode 存點,不逼 F)。A段抽考:ImagePullBackOff 三類根因訊號(repo-not-exist/connection-refused/401-toomanyrequests)一次答全對推07-03;API Server 英文抽考過(櫃檯比喻+唯一碰etcd,唯一錯 control panel→**plane** 已釘,推07-03);P0 etcd 口誤補正(scheduler/kubelet 透過 API Server 不直接寫 etcd,答對)。**今日主線(全程 Feynman 引導他自己推)**:① Service 為何存在=Pod IP ephemeral 寫死必爆(秒答)② Service 用 label selector 框 Pod(遷移 P1 matchLabels,他自己答 label)③ Endpoints/EndpointSlice=健康 Pod IP 清單,controller 跑 reconcile loop 維護、readiness 當閘門 → **回扣 P1 probe lab「rm readiness→從 Endpoints 消失但 RESTARTS 0」完美解釋**(reconcile 第3次出現=複利伏線)④ ClusterIP 是虛擬 IP、沒綁任何網卡 ⑤ 思想實驗「若綁 node-1 一張網卡」→ 他自己答出**瓶頸點**+單點 ⑥ 揭曉 kube-proxy 每台 node 都跑+寫 iptables 規則,封包出發 node 本地就 **DNAT 改寫目的地** → 去中心化無瓶頸。**卡點**:DNAT/去中心化他說「有點不太懂」,給電話代表號比喻(代表號=ClusterIP/分機=PodIP/話機轉接表=iptables規則/總機小姐=中央LB瓶頸),要他 mapping 回來時喊下班 → **Feynman Gate 卡在這未確認,下次先收這個**。學員 CNI 誤會已拆(CNI 管 Pod 拿真實 IP/Pod 互通,非 ClusterIP)。新術語卡2張:DNAT、kube-proxy。筆記 portfolio/notes/p2a-service-kube-proxy.md。
- session 6 (2026-06-25): **P1 畢業 Gate PASS → P1 全畢業**。On-call triage drill:一次 apply 三隻混合故障 Pod(中性命名,blind),他用 `get pods`(全景:STATUS+RESTARTS)→ `describe`(讀 Reason/Exit Code/Events)逐一拆。三隻全定位正確:payment-api=ImagePullBackOff(tag `nginx:1.99` 不存在,驗證邊界:kubelet 第5棒才發現)/ cache-worker=OOMKilled exit137(撞 cgroup mem limit)/ web-frontend=CrashLoop 但 **exit 0 Completed**(liveness probe 打 8080、nginx 聽 80 → probe 殺健康 app,SIGTERM 優雅退出;他從 exit0 反推「app 健康、被 probe 殺」=最佳時刻)。A 段抽考 probe 坑通過(自己講出「羊群效應/thundering herd」+ reconnection 風暴回壓 DB 正回饋,推 +7 到 07-02)。**改進(連續第三 session 同一條)**:先跳結論/修法,要追問才補深度(治標 vs 治本、exit0 意義)→ 帶進 P2a:講完現象+根因主動接「修法+治標/治本+先驗證什麼」。治標 vs 治本他能分(leak 鋸齒爬頂 vs rightsize 平台水位,A=leak B=可調大,工具 kubectl top/Prometheus → 預告 P4)。scorecard P0-P1 全 ✅。新術語卡:thundering herd。mind map(describe 速查表放射狀)已給他手抄默畫。
- session 5 (2026-06-24): **chunk 5 resource/QoS/OOM 全做完(C+D+E+F+G)**。requests=預訂+排程依據(scheduler 加總≤allocatable,不可超賣)/ limits=cgroup 硬天花板(可超賣)。**核心第一性原理:可壓縮(CPU,撞 limit→throttle 變慢)vs 不可壓縮(memory,撞 limit→OOMKilled exit137=128+9 SIGKILL)**,學員自己推出這不對稱(他坦言半年前面 AWS EC2 support 被問 OOM 答不出沒上,今天破了)。**兩種 OOM**:容器級(撞自己 cgroup limit,與 node 餘量無關=B段謎題)vs node 級(kubelet 按 QoS 驅逐)。QoS:Guaranteed(requests==limits)>Burstable>BestEffort,只設 limit 會被自動補成 Guaranteed。D 段 lab oom-demo.yaml(polinux/stress 要150M/limit100Mi)親手重現 OOMKilled+exit137+Burstable+node 仍有餘量,三題全自己讀對。E 段 chaos:CrashLoopBackOff 是現象不是死因→describe 速查表(OOMKilled137 / Error1 / probe / ImagePull);教 `kubectl logs --previous`(他沒用過)。Round2 senior 判斷:leak 調大 limit 只是治標(鋸齒爬頂 vs 平台水位分辨)他自己講出。F 段 mock 兩段全對。scorecard 全 ✅。改進=主動吐「治本vs治標」別等追問。筆記 portfolio/notes/p1-resource-qos-oom.md。新術語卡 3 張:compressible/incompressible/OOMKilled。
- session 4 (2026-06-23): **chunk 4 Deployment/rollout 全做完(C+D+E+F+G)**。教完:Deployment 管 RS 不管 Pod、翹翹板兩 RS、maxSurge(額外上限)/maxUnavailable(可用下限)公式、零停機正解=maxUnavailable:0+maxSurge:1/25%、死鎖 maxSurge:0+maxUnavailable:0 被 apply 退件、rollback 快=舊 RS 留著 scale up 不重拉 image、revision history/CHANGE-CAUSE。**驗證邊界金句**:schema 錯 API Server 當場擋,外部現實(image 在不在)只有 kubelet 第 5 棒拉才知。D 段 lab rollout-demo replicas=4 maxSurge1 maxUnavailable1 minReadySeconds10:正常 rollout→rollback→壞部署(nginx:9.99)卡死幾何 3 好+2 壞=5、3 舊 Pod 全程沒倒。**現場 free chaos**:image 打成 ngimx → ImagePullBackOff,學員自己讀 Events 抓到根因(進 mistake-registry)。F 段 mock(零停機策略+保護+rollback):骨架全對,A1 自己抓出「額外8→總數12」算錯;senior 補刀=別等被追問才講機制、選經濟配置別報 maxSurge:8。scorecard 全 ✅。改進=主動吐機制+挑經濟值。筆記 portfolio/notes/p1-deployment-rollout.md。
- P1 已澄清:Linux namespace(kernel 隔離視野)≠ k8s namespace(邏輯分組,**不做隔離**,擋網路要 NetworkPolicy)。學員自己問出這個撞名點,理解力好。
- session 1 scorecard (P0-P1): 底層原理 ✅ / 內部機制 ✅ / 自己的話 ✅。改進=用詞精準度。
- symptom→棒次地圖已教: Pending=scheduler / ContainerCreating=kubelet 網路volume / ImagePullBackOff=runtime拉image / CrashLoopBackOff=容器或probe。
- session 2 (2026-06-18) D段親手做完: kind 拆解(node=container)、kubeconfig/context 安全(他原本怕打到公司 prod EKS,已教 current-context 肌肉記憶)、Deployment→ReplicaSet→Pod 三層(從 pod 名 hash 看族譜)、reconcile 自癒、scale=0。
- session 2 scorecard (P0-P1): 底層原理 ✅(自己用恆溫器比喻 declarative)/ 內部機制 ✅ / 自己的話 ✅。改進=用詞精準度(同上)。
- session 3 (2026-06-22): P0 畢業 gate 通過(五棒+演員+scheduler/kubelet 分清);兩次 feedback 砍低價值產物(portfolio + 術語卡),skill 已加雙價值門檻。scorecard (P0-P1):底層原理 ✅ / 內部機制 ✅ / 自己的話 ✅。改進=etcd 只有 API Server 直接碰(口誤待修)。
- ~~術語卡 kubeconfig / context / kind~~ **2026-06-22 移除**:學員指出定義型瑣碎詞/工具名面試不考,違反新價值門檻(見 memory [[k8s-portfolio-value-gate]] 同源原則 + SKILL.md 術語卡)。current-context 改記為 ops 安全習慣,不當卡。
