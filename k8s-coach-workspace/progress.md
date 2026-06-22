# 學習進度卡 (斷點續傳)
<!-- 每次 session 開始前更新這裡,讓 Claude 快速掌握你的狀況,避免重複解釋背景 -->

## 基本資訊

| 欄位 | 內容 |
|------|------|
| 目前 phase | **P1 核心物件 + 容器底層**(P0 已畢業 2026-06-22)|
| 目前主題 | P1 chunk 1-3 ✅(container / Pod / probe,含 D+E 段 probe lab 全做完);下次接 chunk 4 Deployment/rollout |
| 上次 session 日期 | 2026-06-22 |
| session 累計次數 (session_count) | 3 |
| 上次 Weekly Review (last_weekly_review) | 0 |

## 診斷結果 (New Student Warm-Up)

程度: 中 (有地圖形狀,缺演員名字)。pacing = P0 剛好,不加速。

- 強: 已有 reconcile 直覺 (原話「比對現有環境進行更新」);知道 rolling update 替換 Pod。
- 洞 1: 用「下指令」框架 = 還停在 imperative 思維 (k8s 是 declarative)。
- 洞 2: 各步驟「誰做的」全省略 (API Server / etcd / controller / scheduler / kubelet 都沒提到)。
- 洞 3: 漏掉 Pod 怎麼被排到某台 node (scheduler 指派 + kubelet 啟動)。

## 未完成 lab

- [x] D 段 kind lab:apply hello-nginx → 用 `kubectl get events --sort-by` 看五棒 → delete pod 看 reconcile 自動補(新尾碼/新 IP)→ scale=0 證明改 DESIRED 才停。全做完。
- [x] **G 段 artifact 改為「不進 repo」**(2026-06-22 學員 feedback,見 memory [[k8s-portfolio-value-gate]]):P0 apply→Running 流程圖太基礎,放 public repo 反而扣分,學員已畫在私人筆記本即可。`~/jason/k8s-portfolio` 目前 0 commit、manifests/hello-nginx.yaml 仍 untracked(也太基礎,先不 commit);真正 portfolio 從 P3+ 長出。repo 無 remote、gh 未裝。

## 下一步

> 下次繼續(一句話):接 **P1 chunk 4 Deployment/rollout**(滾動更新怎麼零停機換 Pod、maxSurge/maxUnavailable、rollback)。phase-1 教材檔仍未建,從第一性原理教。
> 環境:kind 叢集 `k8s-coach-p0` 仍在;probe lab 物件若沒 delete 還在跑(probe-demo deploy+svc)。lab 檔 `~/jason/k8s-portfolio/probe-demo.yaml` 待搬 `~/jason/k8s-lab/`(基礎檔別留展示 repo)。學員偏好自己敲指令,YAML 預設給規格;他說「給我 YAML」就給完整範本讓他照打(見 memory)。學員用英文作答時附 `💬 English Polish`。
> commit 規則:user 全域禁止任何 trailer/Co-Authored-By,commit message 一行。
> 待補精準度:術語要用「DESIRED vs CURRENT」「reconcile loop 收斂」而非「監控數量」。**新補洞**:只有 API Server 直接讀寫 etcd,其他元件(controller/scheduler/kubelet)都透過 API Server 的 watch/update,不直接碰 etcd(P0 學員口誤「kubelet 寫回 etcd」)。etcd Raft 深入 park 到 P5/foundations。
> English Ramp:P1 仍維持「只做術語卡」(P0-P1 同一檔位),P2a 起才加英文短句。

## 補充筆記

- 學員背景: DevOps 工程師,hands-on 有 (kubectl apply / 看 logs),底層理論弱;coding 初學。
- 教法備忘: 多用生活 analogy、用學員原話回扣、一次一個 chunk、語言要白。
- chunk map (P0): [1] declarative+reconcile → [2] API Server+etcd → [3] controller 怎麼 reconcile → [4] scheduler 指派 node → [5] kubelet 啟動容器。全部 ✅。
- chunk map (P1): [1] container=namespace+cgroup 圈的行程(vs VM 共用 kernel)✅ → [2] Pod 為何存在(共享 network ns,pause container,sidecar,同生共死才放同 Pod)✅ → [3] probe ✅✅(D/E 段動手做完:busybox+exec probe 用 /tmp/ready /tmp/alive 信物,rm readiness→endpoint 消失但 RESTARTS 0、STATUS 仍 Running;rm liveness→RESTARTS+1 後 command 重 touch 自癒。學員兩次預測全中,還自己從「rm:No such file」反推出「尚未 restart」。偵測延遲=failureThreshold×periodSeconds=調校旋鈕,回扣 liveness 查 DB 雪崩。lab 檔在 k8s-portfolio/probe-demo.yaml 待搬去 ~/jason/k8s-lab/)→ [4] Deployment/rollout → [5] resource/QoS/OOM。
- P1 已澄清:Linux namespace(kernel 隔離視野)≠ k8s namespace(邏輯分組,**不做隔離**,擋網路要 NetworkPolicy)。學員自己問出這個撞名點,理解力好。
- session 1 scorecard (P0-P1): 底層原理 ✅ / 內部機制 ✅ / 自己的話 ✅。改進=用詞精準度。
- symptom→棒次地圖已教: Pending=scheduler / ContainerCreating=kubelet 網路volume / ImagePullBackOff=runtime拉image / CrashLoopBackOff=容器或probe。
- session 2 (2026-06-18) D段親手做完: kind 拆解(node=container)、kubeconfig/context 安全(他原本怕打到公司 prod EKS,已教 current-context 肌肉記憶)、Deployment→ReplicaSet→Pod 三層(從 pod 名 hash 看族譜)、reconcile 自癒、scale=0。
- session 2 scorecard (P0-P1): 底層原理 ✅(自己用恆溫器比喻 declarative)/ 內部機制 ✅ / 自己的話 ✅。改進=用詞精準度(同上)。
- session 3 (2026-06-22): P0 畢業 gate 通過(五棒+演員+scheduler/kubelet 分清);兩次 feedback 砍低價值產物(portfolio + 術語卡),skill 已加雙價值門檻。scorecard (P0-P1):底層原理 ✅ / 內部機制 ✅ / 自己的話 ✅。改進=etcd 只有 API Server 直接碰(口誤待修)。
- ~~術語卡 kubeconfig / context / kind~~ **2026-06-22 移除**:學員指出定義型瑣碎詞/工具名面試不考,違反新價值門檻(見 memory [[k8s-portfolio-value-gate]] 同源原則 + SKILL.md 術語卡)。current-context 改記為 ops 安全習慣,不當卡。
