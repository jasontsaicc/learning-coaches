# Breakpoint History（原文封存）

<!-- 2026-08-19 自 progress.md 的 Current Session breakpoint 區段整段搬出,一字未改、未刪、未重排。
     搬出理由:該區段違反 PROGRESS-SCHEMA.md §3(應為當前狀態一行 + 下一場 resume),
     已長成 s16-s26 的疊層日誌(263 行),每堂開課都整份進 context。
     本檔是冷檔:只在 Weekly Review、Phase Gate 三振診斷、或要查某堂當時原始存檔時才讀。
     內含的長效教練紀律已另抄一份到 session-log.md「教練執行紀律」。 -->

<details>
<summary>s26 斷點(已消化,留參考)</summary>

**s26 已收(2026-08-06,公司 bastion,context `kind-k8s-coach-p2a`)。C-1 三階梯壽命表全部親手實證收工,scorecard 3/4 = 自 s18 以來首次通過。WR9 第二度中斷(學員兩次要求「直接開始今天的課程」「我的意思是繼續昨天的 storage」),`last_weekly_review` 仍是 18。F 段連五堂債本堂還掉;G 段跑了一題正式版。story-bank 連六堂未挖。**

本堂事實:

- **叢集自癒,但真兇永遠查不到了**。`up 1:49` + 所有容器 `Up 2 hours` = 宿主機今早重開機;load `0.56/1.07/1.15`(4 核心)、`available 12Gi`,資源健康。開場 MTTR 三選一(A 看 node Conditions / B 看宿主機 / C 直接 restart)→ **學員選 C,理由「看起來是 notready 先重啟試試」**。已教:restart 同時清掉症狀與證據,s21→s24→s25→s26 四次倒下四次從零猜。回扣 s5/s6「治標 vs 治本歸錯邊」第三次同形狀,新卡入帳。
- **WR9 主題 2(跨-node 路由)直給正解,學員未動手**。已給:路徑上 CoreDNS/Service/kube-proxy **各零次參與**、七段 kernel 路徑、判準句「iptables 管改寫成什麼,路由表管往哪裡送」、第一個指令 `ip route`。三選一預測題已出(A 無 via / B `via ... dev tunl0` / C via ClusterIP),**學員未作答即要求改上 storage**。⚠️ **依學員自己的資料「直給+無動手」必蒸發,s27 開場必須用 `docker exec ... ip route` 補一次動手驗**。
- **YAML 動手鏈(高密度,一條龍)**:學員自寫 `vol-demo.yaml` → 縮排跑掉要求代打 → 教練修縮排(`volumes` 掉進 `volumeMounts` 清單裡、list item 欄位少一層),**並明講故意不改 `image: buybox`**(不玩猜謎)。接著:`--dry-run=server` 預測二選一 → **答 B(綠燈)✅** → 實測綠燈 → apply → `ImagePullBackOff`。**dry-run 兩層卡當場現形。**
- **dry-run 判準半過**:問「為什麼 dry-run 攔不到」→ 答「因為 server dry-run 不會實際去查有沒有這個 image」= **把「攔不到」換句話說,同義反覆**。教練當場命名這個新形狀並給檢驗法:**判準句講完,對方有沒有拿到一個新事實?** 精準版已給(image 存不存在只有 kubelet 第 5 棒拉的時候才知道;API Server 從頭到尾不碰 registry)。
- **ImagePullBackOff 三類訊號:選 C 正確但未貼關鍵字**。教練已點名「這題你不看 Events 也猜得到,因為是我先告訴你 image 打錯」→ 學員仍未貼輸出。**rep 不算數,卡不推。**
- ⚠️ **`kill 1` 沒殺死 container(本堂最大意外,價值最高)**:`kubectl exec vol-demo -- kill 1` 後 `RESTARTS 0`、L1 檔案還在。根因=**Linux kernel 對 PID 1 的 signal 保護:沒有安裝 handler 的 signal,PID 1 不套用預設動作,直接忽略**;而且**同 PID namespace 內連 SIGKILL 都被擋**,只有祖先 namespace 送得進去。`sleep` 從不註冊 SIGTERM handler,所以整個 signal 被丟掉。(註:s24 net-tool 的 `kill 1` 有效,image 的 PID 1 不同。)已教三個生產對應:`delete pod` 等滿 30 秒 grace period 之謎、rollout 斷線/交易沒寫完、Dockerfile shell form 讓 `/bin/sh` 當 PID 1 不轉發 signal → `tini`/`dumb-init` 的存在理由。改用 `docker exec <node> crictl stop $(crictl ps -q --label io.kubernetes.pod.name=vol-demo)` 從祖先 namespace 殺,實驗才做成 —— **這一步本身就是 PID 1 那條的實證**。
- **三階梯壽命表全部實證收下(C-1 完成)**。一顆 `vol-demo` Pod 同時掛三層(`/root` 可寫層 / `/scratch` emptyDir / `/data` PVC),預測全中:

| 層 | 換 container | `delete pod` | 實體路徑 |
|----|-------------|-------------|---------|
| L1 可寫層 | ❌ 死 | ❌ 死 | `/var/lib/containerd/.../snapshots/` |
| L2 emptyDir | ✅ 活 | ❌ 死 | `/var/lib/kubelet/pods/<pod-uid>/volumes/` |
| L3 PVC→PV | ✅ 活 | ✅ 活 | `/tmp/pv-demo/` |

  證據:`RESTARTS 1 (5s ago)` + `AGE 7m33s`(Pod 沒換)vs delete 後 `AGE 3s`(全新 Pod)。**s24 答錯的 emptyDir 那階今天翻過來,而且機制自產**:「pod 沒有換 container 換掉只有 upperdir 換掉」。精準版補完:沒換的是 **Pod UID**。
- ⚠️ **意外發現:這張「持久卷」其實是記憶體**。`/proc/mounts` 讀出 `/scratch` → `/dev/nvme0n1p1` **xfs 真實磁碟**,`/data` → **tmpfs**。因為 kind node image 把 `/tmp` 設成 tmpfs,而 `pv-demo` 的 hostPath 是 `/tmp/pv-demo`。**號稱短命的落在硬碟、號稱持久的落在記憶體。** 封印句:**持久性由「實際掛在什麼東西上」決定,不是由物件名字決定;別信名字,去讀 `/proc/mounts`。** 這是 s24「可寫層存在 memory」誤解的**鏡像**(那次是該在磁碟的以為在記憶體,這次是該在磁碟的真的在記憶體)。node 上 `ls -l /tmp/pv-demo/` 拿到 `-rw-r--r-- 1 root root 7 f.txt` = 執行體肉身摸到。
- **學員主動提出 EKS 跨 AZ EBS 問題(高價值,第二次自接雲上)**。已教:EBS **AZ-scoped**(物理事實)→ EBS CSI driver 自動把 `topology.ebs.csi.aws.com/zone` 寫進 PV 的 `nodeAffinity` → scheduler 讀得到 → 只排到那個 AZ。三方案對照(hostPath 不寫位置=只能玩 lab / `local` 強制 nodeAffinity / EBS CSI 自動寫)。第一性原理定調句:**儲存有位置,計算沒有;位置必須被寫進 API 物件,否則 scheduler 一無所知。** 第二層 `volumeBindingMode`:`Immediate` 先開 EBS 後排 Pod → `volume node affinity conflict` 永遠 Pending;`WaitForFirstConsumer` 把順序倒過來 = 正解。跨 AZ 共用只能 EFS(回扣 s25 已答對的「塊裝置 vs 目錄樹決定能不能 RWX」)。
- **Transfer 過(EKS 順序題)**:「因為 StorageClass 使用 immediate 所以 pvc 建立立刻選一個 az 建立 EBS,但是可能在建立 pod 有設定指定的 az 所以永遠 pending」。⚠️ **但這是當堂剛教 + 教練指定「用順序講」的鷹架下複述,不計入 pattern 卡正樣本**。
- **F 段跑了(連五堂債還掉)**。獨白:三階梯結構全對、壽命全對,**但對一個「完全沒碰過容器」的人開口就是 container/emptydir/pv 三個名詞加三句結論,零機制**。追問後機制出來:「因為路徑存在 container id 底下的資料夾」= 昨天判準句內化成自己的話。**誘答咬住**(「不刪 pod 就永遠安全吧」→ 沒點頭,用當天新學的 tmpfs 反駁)。
- **F 段盲點入帳**:「pod 不是我建的嗎?我不刪它,它為什麼會自己不見?」→ 答「pod 會重啟 or 調節 編排」= 方向對、講不出誰在什麼條件動手。已直給正解:**Pod 沒有「重啟」這回事,只會被丟掉重建**;五種自動消失情境(node 失聯 5min / kubelet evict / drain / preemption / HPA 縮容 or rollout);`RESTARTS` 欄數的是 container 不是 Pod(用他自己今天的兩段輸出當證據);定調句 **cattle not pets**。
- **G 段跑了正式版一題(自 s21 以來首次)**。顧問情境:EKS 影像處理服務寫 emptyDir,**凌晨兩三點**任務失敗找不到中間檔、重跑正常。學員答「檢查中間是不是 pod 有重啟 or 切換 az」= **方向對(查 Pod 生命週期不查 code),連四堂 MTTR ❌ 之後首次回升**;但漏掉「凌晨兩三點」這個決定性線索,也沒給出任何指令。正解已給:Cluster Autoscaler/Karpenter 低流量縮容或 spot 回收 → drain → Pod 重排 → emptyDir 空;第一個指令 `kubectl get events -A --sort-by=.lastTimestamp | grep -iE 'evict|drain|scale|preempt'` 對時間戳;修法 = 中間產物搬 PVC/S3 或加 `cluster-autoscaler.kubernetes.io/safe-to-evict: false`。L6 英文版已給。
- pacing:**本堂學員動能明顯高於 s24/s25** —— 全程跟著跑指令、預測題全部作答、主動提 EKS 問題。但兩次改變議程(跳 WR)、兩次只給結論被追問。**有效做法**:三選一預測(全部作答)、明講「我故意沒改這個字」不玩猜謎(學員沒抗拒)、意外結果當場轉成教材(PID 1、tmpfs)。**無效做法**:要他貼 Events 關鍵字(要了兩次沒給)、開放式「第一個動作是什麼」(仍只給方向不給指令)。
- 環境:`vol-demo.yaml` 寫在 `~/jason/learning-coaches/workspaces/k8s/labs/`,昨天的 `pv-demo/pvc-demo/cg-demo.yaml` 在 `~/go_senior_devops/learning-coaches/workspaces/k8s/labs/` —— **bastion 上有兩份 repo clone**,labs 是 gitignored 不影響同步,已告知學員。

next(s27),順序:

1. **開場動手補 `ip route`**(不抽考、直接動手):`docker exec k8s-coach-p2a-worker ip route` → 挑出去 worker2 Pod 網段那一行 → 讀 `via` / `dev tunl0`。s26 只有直給,依學員自身資料必蒸發。跑完才算這張五抽卡有 rep。
2. **C-1 最後一塊:`cg-demo` 讀 `/sys/fs/cgroup/memory.max` 拿 `67108864`**(node 已 Ready,Pending 應已解除;先 `kubectl get pod cg-demo`)。配「誰把 limit 寫進 cgroup=kubelet 不是 scheduler」那張新卡一起收。
3. **C-2 開課:StorageClass 動態供給 / CSI**。s26 已把 EBS CSI / nodeAffinity / `volumeBindingMode` 講到位,C-2 是它的地面版,銜接順。capstone:api 掛 PVC。
4. **WR9 第三度嘗試**:已中斷兩次。建議**不要再排成開場關卡**(兩次都被跳過),改成拆散寄生 —— 每堂 A 段動手驗一張過期卡,artifact audit 單獨找一堂做。若學員自己要求 WR 再整堂跑。
5. **story-bank 連六堂未挖**,s27 保底一則(LP 佔 loop 近半)。
6. pacing:延續三選一 + 意外結果轉教材。**MTTR 下一階**:學員已能講方向,缺的是「方向 → 指令」那一步。s27 起問法改成「你要看的是哪一個東西?」(答:Events / node 生命週期)再問「那個東西用什麼指令看?」,兩段式把指令逼出來。

</details>

<details>
<summary>s25 斷點(已消化,留參考)</summary>

**s25 已收(2026-08-05,公司 bastion)。WR9 開跑第 1 題就收到大魚(分層判準判準句自產=昨天的洞補上),但 WR9 只跑完 1/3 主題即中斷,`last_weekly_review` 不推進。C-1 PV/PVC 收尾:PV+PVC 親手 apply、Bound 實證、Transfer 過(今天最好的一次回答)。⚠️ 叢集三台 node 全排不出 Pod,修復指令已給、學員未執行。F/G 連五堂未跑;story-bank 連五堂未挖。**

本堂事實:

- **WR9 未完成,只跑了主題 1**。已跑:分層判準卡盲測 + Transfer + 一次 MTTR 排障。**未跑**:主題 2(跨-node-走路由表,四連錯最高優先)、主題 3(kube-proxy-不在-Pod-啟動路徑)、Mistake Registry sweep、quick drill、**artifact audit**。依 `weekly-review.md`「WR 中斷則下堂從未完成的步驟續跑」,s26 從主題 2 接。
- **分層判準卡:判準句自產 ✅,分欄 4/5,Transfer ❌**。① 判準句「如果沒有 API Server 能不能使用」**無提示自己講出來** —— 昨天收工回想時答「不知道耶」,今天補上,**這是本堂最重要的正樣本**。② 但首答用了兩套詞(1、3 寫「kernel」,2、4、5 寫「可以」),兩種讀法答案完全相反,教練當場點名這是 pattern 卡「只給結論不給判準」穿新衣服;釐清為讀法 B 後 4/5。③ 唯一錯的是 **cgroup memory limit**,學員自述「我在想的是 cgroup,那應該是 yaml 的 limit 沒錯」= 把兩個分身當成一個。
- **卡升級成兩步版(重要,取代原單步版)**:**每個 k8s 資源都有兩個分身** —— 宣告(etcd)vs 執行體(kernel)。Service 物件 / kube-proxy 的 DNAT 規則、PVC 物件 / node 上的 mount、`resources.limits` / cgroup `memory.max`、NetworkPolicy 物件 / filter 表規則。判準第一步變成「**你問的是宣告還是執行體**」,第二步才是「宣告在 etcd、執行體在 kernel」。定調句:**API Server 掛掉 = 沒有新的翻譯了,不是已經翻好的東西消失了。**
- **Transfer 未過,新病灶**:「誰把新的 limit 寫進 cgroup、什麼時候寫」→ 答 **「scheduler 嗎」**。正解 kubelet(→CRI→runc)。判準句:**不在 node 上的元件碰不到 kernel**(scheduler 只填 `spec.nodeName`,連 node 的門都沒進過)。時機:**只在建立 container 那一刻寫**,所以改 limit 不重建 Pod = kernel 數字不變。已回扣 P0 五棒,新卡入帳。
- **cgroup 動手驗未完成**:`cg-demo`(limit 64Mi)apply 後 **Pending**。三選一預測題經一層梯子後答對 B(`67108864`),封印句「cgroup 是 kernel 介面,介面只講 bytes」已給,但**實際數字沒讀到**,s26 補。
- ⚠️ **叢集大故障(比昨天嚴重)**:`describe pod` Events = `0/3 nodes are available: 1 node(s) had untolerated taint node-role.kubernetes.io/control-plane, 2 node(s) had untolerated taint node.kubernetes.io/not-ready`。**worker 也倒了**(昨天只有 worker2),等於能排的 node 掛零。修復三發(`kubectl get nodes` / `free -h; uptime; docker ps` / `docker restart k8s-coach-p2a-worker k8s-coach-p2a-worker2`)**已給,學員未執行未回報**。s26 開場第一件事,不修就沒有任何 lab。
- **MTTR 連三堂未過**:Pending 的第一個排查指令問「你會下什麼」→ 答「不知道 直接開始今天的課程吧 拖太久了」。正解 `kubectl describe pod` 看 Events 已直給(理由:scheduler 排不進去一定把原因寫在 Events)。注意學員**願意跑教練指定的指令,但不願意自己選指令** —— 排障訓練的缺口精確落在「選指令」這一步。
- **YAML 藏寶圖 rep 首次自己讀圖過關**(06-18 卡,unresolved 至今):`strict decoding error: unknown field "spec.sccessModes"` → 教練只說「訊息把座標給你了」,學員**自己回檔案找到打錯的字並改對** apply 成功。這是這張卡自建卡以來第一次不用代打。但同一段稍早學員說「**直接給我 yaml**」跳過自寫 PVC,rep 打了折。
- **PV/PVC 收尾(C-1 第三階)**:PVC `Pending` → `get pv` = No resources found → 認出**靜態供給的痛點**(沒人擺貨需求單就永遠掛著)→ apply `pv-demo` → 立刻 `Bound`。三個實證收下:① PVC 的 CAPACITY 欄顯示 **1Gi 不是 500Mi**(capacity 是下限、綁定不切割)② **三台 node 全 NotReady 照樣 Bound** = 媒合是 control plane 帳本作業,不需要 node ③ `RECLAIM POLICY: Retain` 已埋未教。
- **學員自曝誤解「PV 1:多」** → 三層關係表釐清:`StorageClass ─1:多→ PV ─1:1→ PVC ─1:多→ Pod`。順帶收 RWO 常見誤解(**RWO 限制的是 node 不是 Pod 數**,同 node 多顆都掛得到)。
- **學員主動要求「重新幫我整理,使用第一性原理開始」= 高價值訊號**。重整版從一個物理事實長出來(overlayfs upperdir 綁 container)→ 三階梯壽命表(路徑裡就寫著它綁誰)→ 為什麼拆兩個物件(知識不對稱/解耦,同構 Pod↔scheduler)→ 媒合三條件。**重整後學員立刻 Transfer 過**,證明「亂了就重砌地基」比繼續往前推有效。
- **Transfer 過(本堂最佳)**:「pvc-demo-2 會怎樣」→ 「pending 因為沒有 PV 了,因為 PV to PVC 是一對一的,所以就算 PV 有 1G、目前一個 PVC 使用 500,剩下的 500 也不能拿出來使用」+ **自己追問「為什麼要這樣設計」與「一般都宣告一樣的空間嗎」**。判準句自帶「因為」= pattern 卡第三次無提示正樣本(前兩次 s22 站 7、s24 kernel 題)。已回答:1:1 是**塊裝置**的物理特性上浮(檔案系統假設獨佔裝置);RWX 只有目錄樹型(NFS/EFS)做得到;實務上動態供給讓這個浪費結構上不存在。
- pacing:學員兩次喊停(「拖太久了」「直接給我 yaml」)。低電量 + 想要進度感。**有效做法記錄**:三選一縮小(cgroup 數字題,一層梯子就答對)、第一性原理重砌(重整後立刻過)。**無效做法**:要他自己選排查指令(直接喊跳過)。

next(s26),順序:

1. **開場先修叢集**(不修就沒 lab):三發修復指令重跑,`kubectl get nodes` 三台 Ready 才往下。若 restart 無效,走 s21 那條診斷鏈(node Conditions → 宿主機資源 → containerd active? → kubelet log 找 `rpc DeadlineExceeded`),根因大機率仍是 4 核心資源競爭。
2. **WR9 續跑(從主題 2 接)**:跨-node-走路由表(**改兩段問法**:①這條路徑有哪些元件參與 ②第一個指令)、kube-proxy-不在-Pod-啟動路徑。接 registry sweep(11 張過期)+ **artifact audit**(P2a 只有 notes,manifests 未落地)。跑完才把 `last_weekly_review` 設成 26。
3. **C-1 最後兩塊動手債**:① `cg-demo` 讀 `/sys/fs/cgroup/memory.max` 拿到 `67108864`(node 修好即可跑)② **emptyDir 第二階必須動手驗**(口頭已錯一次,直給後沒接動手 = 依 s16 實證會蒸發):同一顆 Pod 掛 emptyDir 寫檔 → `kill 1` → 檔案還在 → `delete pod` → 檔案沒了。③ Pod 掛 `pvc-demo` 寫檔 → 刪 Pod 重建 → 檔案還在 → 進 node `findmnt` 看 bind mount 本體。
4. **F/G 連五堂債**:F 段材料現成且燙(菜鳥題:「為什麼 container 死了檔案就沒了?硬碟又沒壞」/「PV 為什麼不能兩個人分著用?」);G 段正式版自 s21 起未跑。story-bank 保底一則。
5. pacing:延續「三選一縮小」與「亂了就重砌第一性原理」;**排障訓練改法** —— 不再問開放式「你會下什麼指令」,改成給 3 個候選指令二選一/三選一,先建立選指令的肌肉再放開。

</details>

<details>
<summary>s24 斷點(已消化,留參考)</summary>

**s24 已收(2026-08-04,公司 bastion,context `kind-k8s-coach-p2a`)。P2b 開跑,C-1 第一階親手拆完(overlayfs 可寫層);A 段兩張過期卡雙雙未過;中段被叢集環境故障吃掉一大段。F/G 連四堂未跑(本堂學員下班收工,非跳過);story-bank 連四堂未挖。**

本堂事實:

- **A 段兩題全未過**。① kube-proxy 不在 Pod 啟動路徑(07-26 過期):答「CoreDNS 嗎」= 把「kubelet 把 CoreDNS ClusterIP **寫進** resolv.conf」誤當成「啟動過程**打過**它」。② 跨-node-走路由表(07-31 過期):答「會看 a 的 service, kubectl get svc」= **第四種錯法,且與 s22 完全相同**(史:iptables → resolv.conf → 查 svc → 查 svc)。當場合併診斷:兩題都用 k8s 物件回答 kernel 的問題。
- **新工具卡「關掉 API Server 還在不在」**(教練當堂造,對治層級混淆家族)。左欄 kernel 真東西(iptables/conntrack/路由表/veth/cgroup/mount/namespace)vs 右欄 etcd 資料(Service/Deployment/PVC/NetworkPolicy/RBAC/Secret)。**學員 3/3 過**,其中第三題「沒有,因為 CNI 不支援」與追加 Transfer「Calico 上 apply 完關掉 API Server 擋不擋得住 = 可以,因為直接修改 kernel」**皆無提示自答**,是本堂最硬的正樣本,也是靜默無效卡的鏡像驗證。RBAC 特例(完全不在 kernel)已埋,C-4 再開。
- **C-1 第一階親手拆完(可寫層)**。誤答「存在 memory 就消失了」= 結論對機制錯(pattern 第七堂)→ 直給正解 + 親手驗:`kubectl exec net-tool -- cat /proc/mounts | grep -w overlay` 讀出 lowerdir 15 層(image,共用)/ upperdir 212(可寫,獨有)/ 全部在 `/var/lib/containerd`。接著寫檔 → `kill 1` → **三個預測全中**(名字 IP 不變、RESTARTS 11→12、檔案消失)。封印句:**同一個 Pod,`kill 1` 換掉的是 container,新 container 拿到全新空 upperdir**。順帶收三個面試點(image 共用 / 啟動快 / rm 不會變小)。
- **emptyDir 第二階口頭未過**:問「emptyDir 撐不撐得過 kill 1」答「不在了」(錯,綁 Pod uid 不綁 container)。同時暴露**不知道 `kill 1` 是什麼**(= 送 SIGTERM 給 PID 1,回扣 P1 PID namespace)。已直給正解 + 路徑判準(`/var/lib/containerd/...` vs `/var/lib/kubelet/pods/<uid>/...`,**路徑裡就寫著它綁誰**)。**未親手驗證**,s25 補。
- **why-first 預測連跳三次**:context 要三次才給、`kill 1` 三題只答 2(第 3 題縮小成二選一才答「container」)、emptyDir 題只回問不預測。這是本堂最該改的一條。
- **環境故障吃掉中段(教練驅動,學員未提診斷方向)**:`kubectl get nodes` 噴 `invalid character '<'`。鏈路:context `kind` 指向已刪的 cluster `kind-k8s-coach-p0` → kubectl 退回預設 `localhost:8080` → 打到 `gitlab-ci-dashboard`(Up)→ 收到 HTML。修法:`use-context kind-k8s-coach-p2a`;孤兒 context `kind` 已給刪除指令(未確認是否執行)。**教練自己下錯一發 `docker ps --filter name=kind`(p2a 容器名不含 kind,空結果不能證明沒叢集),已當場更正。**
- 叢集現況:`kind-k8s-coach-p2a` 三節點,**worker2 NotReady 17 天**(老毛病)+ 三個 11 天 Terminating 殘骸(backend/db/frontend on worker2),lab 不受影響未處理。活的 Pod 全在 worker:backend .91 / net-tool .92 / db .93 / frontend .94。net-tool RESTARTS 12(`sleep` 到期自然重啟,約 2h 一次)。
- ROI 篩判定:`--` 分界線 s23 教過今天又問 → Q1「面試官會考 `--` 嗎」= no,**tool trivia 不進格子**,當場結案(已第二次口頭解釋,連同 pipe 在哪執行一起講清)。

- **收工後即時回想(同堂 20 分鐘後,高價值資料)**:問「今天學到什麼」三題。① 可寫層:答「container 由很多 layer 組成,寫的檔案在最上層」= **講得出結構,講不出「那層綁 container」**,半過。② `kill 1` vs `delete pod` 差別:答「kill 1 是模擬 crash」= 那是定義不是差別,半過。③ 分層判準叫什麼:**「不知道耶,我大概知道怎麼分但不知道判斷標準」= 未過**。⚠️ 同一堂內用該判準答對三題(含無提示的「因為直接修改 kernel」),二十分鐘後說不出判準本身 —— **W1 隱性會的最乾淨一次實證,而且證實「當堂過不算過」**。s25 開場第一題就是它。

**球已出未答(s25 開場直接接)**:PV/PVC 解耦已教完(需求單 vs 房源、binding、與 Pod/scheduler 同構),PV 完整 YAML 已給(`pv-demo`,1Gi,hostPath `/tmp/pv-demo`,storageClassName manual),**PVC 規格已給、學員未寫**(`pvc-demo`、500Mi、RWO、manual)。未答的預測題:**1Gi 的 PV 配 500Mi 的 PVC 綁不綁得起來?剩下 500Mi 會怎樣?**

next(s25),順序:

1. **WR9 觸發(25-18=7),不可延**。佇列嚴重積壓(11 張過期,最舊 06-30)。三主題建議:跨-node-走路由表(四連錯,最高優先)、kube-proxy-不在-Pod-啟動路徑、default-deny-分層。**Artifact audit 順便跑**(P2a 只有 notes,manifests 未落地)。
2. WR 後接 **C-1 收尾**:PVC 自寫 → server dry-run → `get pv,pvc` 看 Bound → Pod 掛 PVC 寫檔 → 刪 Pod 重建 → 檔案還在(第三階實證)→ 進 node `findmnt` 看 bind mount 本體。emptyDir 第二階順道用同一顆 Pod 驗(`kill 1` 檔案還在)。
3. **F/G 連四堂債**:s25 F 段用 C-1 材料跑(菜鳥題材:「為什麼 container 死了檔案就沒了?硬碟又沒壞」);G 段正式版仍欠。story-bank 保底一則。
4. pacing:本堂學員答覆極簡短、連跳預測題 = 低電量訊號。s25 開場先做一件事就好,不要 WR + 新內容全塞。**why-first 預測改成硬規格**:不給預測就不給下一發指令(本堂已實測有效,縮小成二選一學員就答得出來)。

</details>

<details>
<summary>s23 斷點(已消化,留參考)</summary>

**s23 已收(2026-08-03,公司 bastion,非家機)。盲測 #3 未過(3.5/7,6 天留存)→ 到期卡重建(veth 過、iptables 半)→ 學員要求換新內容 → lab 重啟:allow-dns 於 bastion 重建、兩種死法親手集齊。F/G 未跑(學員跳過 F,連三堂債);story-bank 連三堂未挖。**

本堂事實:

- **盲測 #3(3.5/7,未過)**:站 2 veth 出發、站 6 抵達整站蒸發(站 6 連兩次盲測丟失);站 3/4 壓成一團;「誰做的」只出現在站 1;四動詞口訣未用;七行紀律垮(碎片式交卷)。正面:**幻影站 4 未復發**;「應該不是 kube-proxy 改 kernel」自我存疑方向正確(kube-proxy 只寫規則不碰封包)。已給 L6 顧問版範例(定調句「名字解析完之後,封包的一生都在 kernel 裡」)。
- **veth 卡冷測過**(3→7,08-10):數字對(同/跨 node 都 2 條)、tunl0 誘答咬住(「兩頭是 pod 跟 root netns」)。站 6 用 veth+本機路由表當場重組成功(kernel 查 `/32 dev cali` 那行選 veth)。
- **iptables-一棟樓半過**(留 3,08-06):換皮誘答咬住(「NetworkPolicy 是 CNI 功能但實際改 iptables filter table」= 真進步,上次同日吞餌兩次);但分工句首答「**nat 管路由**」= 層級混淆家族新樣本,重教後三表(nat 改寫/filter 過濾/路由選路)收。08-06 重抽三表分工一句版。
- **default-deny-分層未過**(留 3,08-06):首答「沒辦法跨 pod 溝通」只有結論;兩層梯子才到「DNS 查詢本身也是 egress」;但隨後 **lab 親手集齊兩種死法**(deny-all 下 `Resolving timed out` → allow-dns 上線後 `Connection timed out`),死亡搬家親眼驗證,bastion 側完成(s16 是家機)。
- **兩張名單卡未過**(留 3,08-06):「開幾張名單」答不出兩道門,三層提示後仍要求「說明一下」→ 直接教兩道門模型 + 檢查程序(逐 Pod 逐方向問名單)。net-tool(無業務標籤)已就位當陌生人測試員。
- **YAML 藏寶圖卡未做完整 rep**:allow-dns 重寫時 selector 塞進 ports 清單 + 自行誤改 apiVersion 成大寫 V1(`no matches for kind ... in version` 親手撞第二次);學員選擇跳過讀圖,教練代打修檔(格式雜務代打條款)。卡照舊 unresolved。
- **只給結論 pattern:負樣本日**。B 選項後果半句被跳過、「要開在 allow 上面」、多題裸結論。連兩堂正樣本目標中斷,重新計數。
- 環境:**學員實際在 bastion**(斷點原以為家機)。worker2 NotReady(s16/s21 同款老毛病)+ 10 天 Terminating 殘骸,lab 不受影響,未處理。三層 Pod 全在 worker(backend .84/db .85/frontend .83)。新 Pod:net-tool(netshoot,`run=net-tool`)。`labs/allow-dns.yaml` 已重建並 apply(寫法 A,AND 語義學員選對)。
- 順手教學:http-echo 極簡 image 無 curl(distroless 概念)、`--` 分界線與 `-sS`(Unix 通用約定)、**DNAT 先於 filter → NetworkPolicy 名單要寫 targetPort 5678 不是 Service port 80**(接一棟樓的部門順序,已教未驗)。

**⚠️ 2026-08-03 課後學員決定(明確二次要求,教練已陳明 engine 條款後定案):跳過 P2a phase gate,s24 直接開 P2b。** P2a 記為 not-certified 帶 flag 前進;gate 沒有取消,只是延後 — **P6 面試衝刺前必須補考**(面試官必考封包旅程,躲不掉的是面試不是教練)。盲測 #N 制度廢止;七站材料改由 spaced-rep 卡與 WR9 自然到期,不再當開場關卡。

next(s24)= **P2b 開課(儲存 + 權限:PV/PVC/CSI、StorageClass、RBAC/SA、IRSA、Secrets、PSS)**,順序:

1. **P2b chunk 1 開課**(讀 `references/phase-2b-storage-rbac.md` 排 chunk map)。新 phase 新氣象,開場不抽考、直接進場景。capstone 銜接:api 掛 PVC(訂單資料)+ 最小權限 RBAC + EKS 首登 IRSA(對 Delivery Consultant 目標是高權重段)。
2. A 段輕量(2 題上限,誠實執行不加碼):08-06 到期批挑 2(iptables 三表分工一句版、兩張名單口頭版優先)。P2a 舊卡照 3/7/14 節奏走,WR9(s25 觸發,25-18=7)清算過期佇列。
3. **P2a 未收殘局(flag,擇機補)**:lab Step 5 兩條 YAML + Step 6 驗收矩陣(規格已留檔:app 標籤、TCP 5678、frontend-client 合法/net-tool 陌生人);3-3 gate;**P2a phase gate(P6 前必補)**。
4. F/G 連三堂債:s24 F 段用 P2b 新內容跑(新材料應比舊材料好啟動);story-bank 連三堂未挖,s24 保底一則。
5. pacing:延續「少抽考多動手」;P2b 是概念+動手 phase,錯峰規則生效(新難主題堂英文降回術語卡)。

</details>

<details>
<summary>s22 斷點(已消化,留參考)</summary>

**s22 已收(2026-07-28,家用 VM)。七站重建日:鷹架版全站走完 → 無鷹架盲測 #2 未過但大進步(3 碎片→5/7)→ F 段 Teach-to-Learn 首跑(三 chunk 的債開始還)。面試時間軸確認:已投遞、抓 1.5 個月(~2026-09 中旬),curriculum-plan §9 已補倒推註記。**

本堂事實:

- **盲測 #2(5/7,未過)**:幻影站 4(DNAT 重複出場)+ 站 6 進門整站蒸發,兩錯在輕提示下**自我診斷**修正;「誰做的」欄多數缺席;Service 思維滲入(「按照什麼 service 進去嗎」)。學員拒背「四層框架」名詞(合理,教練發明的鷹架)→ 改**四動詞口訣「問名→改寫→放行→送達」**,只保順序不背名詞。
- **F 段亮點**:monologue 開場自帶顧問框架(「講這個是為了排障時定位哪一站出事」);靜默無效鏈在追問下首次自組(「不會報錯,但預期 DB 有保護、實際上並沒有」)。
- **F 段兩洞**:① 守衛站在無壓力敘述時**第二次蒸發**(追問才補回);② 誘答吞餌「DNAT 做完才進 iptables」— 當日已教(站 4 幻影修正)仍複發 → 新卡 iptables-一棟樓。
- A 段偵察挖出 veth 誤記「跨 node 連線」→ 車道比喻重教,封印句「veth=Pod netns→node root netns,每 Pod 一條、出門必走、同跨 node 都 2 條」鷹架下收到,新卡 07-31 冷測。
- 跨-node-走路由表卡**重測未過**(第三種錯法:查 svc;史料:iptables、resolv.conf),保姆級提示才到 route table;分工句無法自產,直給後二選一應用 2/2。
- 站 7 亮點:「改 src,**因為** Pod A 一開始就不認識 PodB-IP」— 判準句首次無提示自發(pattern 卡首見正樣本)。
- DNAT 拼成 DANT×3 已糾。教學回饋:recall 不得用 session 編號錨定,一律內容錨定(已入 memory)。

next(s23),順序:

1. **開場冷測:七站盲測 #3(gate 答案卷)**。四動詞口訣開頭、七行、每行含「誰做的」。3 天後還在才算真保留;過了才進 P2a phase gate(Examiner 首用)。
2. A 段債(2 題上限):kube-proxy-不在-Pod-啟動路徑(07-26 到期,s22 未抽)、default-deny-分層(07-26,s21 未過那張)。07-31 批(veth、iptables-一棟樓、跨-node-路由)到期再排。
3. 盲測 #3 過 → phase gate 準備 or lab Step 5+6(家機 p2a 叢集狀態先驗,`allow-dns` 在家機應仍在,bastion 側才是被砍過的)。
4. story-bank 挖礦 s22 未做(債,連兩堂欠);G 段正式版仍欠(s22 以盲測 #2+F 段折算 1/4)。
5. pacing:s22 學員主動選加碼 F 段且全程有輸出,無低電量訊號;但同材料當日三過(鷹架+盲測+F)已到邊際,s23 換冷測+新內容配比。

</details>

<details>
<summary>s21 斷點(已消化,留參考)</summary>

**s21 已收(2026-07-23,公司 bastion)。三件大事:① 職涯目標確認為 AWS Delivery Consultant,教學格式改制 ② 叢集舊帳爆掉並修好 ③ 4-5 七站冷測 0/4 未過。**

**① 目標與格式改制(最高優先,影響往後每一堂)**:學員確認面試職缺是 **AWS Delivery Consultant (ProServe)**,並要求(a)全部問題用該職位的面試情境模擬、(b)每題附 **L6 senior 範例答法**、(c)**加速課程**。已寫入 memory 兩張卡 + curriculum-plan §9。含意:Amazon LP 佔 loop 近半 → story-bank 從「P6 提煉」提前到每堂機會式入帳;全英文 loop → English ramp 需提前;技術主線不變但 EKS/IRSA/migration 權重拉高。

**② 環境修復(舊帳,s16 拖到今天)**:p2a 兩台 worker 全 NotReady,Reason `container runtime is down`。診斷鏈:node Conditions(排除 mem/disk)→ 宿主機資源(15Gi 剩 9.8Gi,**記憶體不是兇手,推翻 s16 假設**)→ containerd `active (running)`(進程活著)→ kubelet log `Status from runtime service failed: rpc DeadlineExceeded`(真兇)。根因=4 核心上跑 6 個 kind node + terraboard 重啟迴圈,CRI gRPC 被拖過 timeout。修法:學員親手 `kind delete cluster --name k8s-coach-p0` + `docker stop terraboard` + `docker restart` 兩台 worker → 三台全 Ready。**教學價值高**:故障點(worker NotReady)與根因(隔壁叢集搶資源)不在同一個叢集裡。註:worker/worker2 的 node IP 重啟後變動(現 worker=172.21.0.4)。lab 三層 Pod 全部復活在 worker2(frontend .210 / backend .209 / db .211),舊 Terminating 殘骸未清。**`allow-dns` netpol 已不存在,只剩 `default-deny-all`**。

**③ 4-5 七站骨架冷測:0/4,明確未過。** 學員只給出 3 個碎片(CoreDNS 的 ClusterIP / kube-proxy iptables / 回程 conntrack),漏掉 veth 出 Pod、過濾層、**跨 node 路由**、抵達 node2。追問「封包怎麼從 node1 到 node2、第一個指令是什麼」→ 答「查 iptables」→ 縮小重問 → 答「查 resolv.conf」(跨層到 DNS)。**結論:s19/s20 親手驗過的四塊零件,三天後無鷹架組裝不起來 = 會用 ≠ 會講,隔堂冷測的價值當場實證。** 事後給正解七站表 + L6 級範例答法(含間歇性假設排序:conntrack table full / ENA `conntrack_allowance_exceeded` / DNS UDP 競態 / rollout endpoint 過時),學員親手 `docker exec ... ip route` 摸到第 5 站,自己挑對 `192.168.20.192/26 via 172.21.0.2 dev tunl0` 那一行(但判準要追兩次才給,且最後答「不用特別算」= 拒絕 show work)。

next(s22),順序:
1. **開場即改制**:A 段抽考一律包成 AWS Delivery Consultant 客戶情境,答完給 L6 對照版。順手挖一則 story-bank raw(LP 佔比高,每堂都挖)。
2. **4-5 七站重測(第 2 次)**,這是 P2a gate 的答案卷,沒過不進 gate。重點盯第 2/4/5/6 站(今天全漏)與「每站誰做的」。要求先宣告四層框架再走路徑。
3. **判準句型專項**:學員今天三次只給結論不給判準(第六、七堂同條)。強制句型「我看的是 X,**因為** [判準]」,每個答案都要有「因為」後半句。
4. step A 過期債(每堂 2 題):07-22 一批(靜默無效一段話組裝版、兩張名單兩關檢查程序、L4-L7 無框架新情境、三分類第 2 輪)、07-23(CNI 合約三件事、出廠全通重抽,今日均未跑)、以及 06-30/07-03/07-10 的長期積欠。**佇列嚴重積壓,WR8 在 s25 觸發時要清一次。**
5. chunk 3+4 F/G 累積債仍未跑;lab Step 5+6 未動(叢集已就緒,`allow-dns` 需重建)。
6. **加速課程的處理**:學員要求加速,但今日冷測 0/4。正確做法是**重新配重不是趕進度**(P2b IRSA / P5 EKS terraform / migration 拉高,P3/P4 深度可修剪),並確認面試日期才能倒推。**s22 開場先問面試時間點。**
7. pacing:今日出現慢下訊號(回答變短、貼回原文、「不用特別算」),已縮 scope 收場。

</details>

<details>
<summary>s20 斷點(已消化,留參考)</summary>

**s20 已收(2026-07-20,公司 bastion,一日三 chunk 紮實堂)。C-4 封包全鏈四塊本堂全收:4-2 veth pair、4-3 node 路由表、4-4 MASQUERADE(4-1 CNI 合約 s19 已收)。全程學員親手敲指令、教練只給規格與判讀(鍵盤鐵律遵守)。開場給了 4-1 CNI 左→右英文思維導圖複習(學員白板用),NIC 一詞當場問答補上。**

亮點:① 4-2 net-tool 第一次 `sleep 3600` 睡滿變 Completed、if11 被 Calico 拆掉→意外教到 CNI「拆」條款(建/拆/重建全看過),重建 if12/.80 實證 Pod IP ephemeral;ifindex 兩頭互指 3↔12 親手驗 veth。② 4-3 兩預測都對(同 node=/32 dev cali 無 via、跨 node=via nodeIP dev tunl0),Transfer 排障尺三段逼問後鎖精準。③ 4-4 誘答題「重啟 kube-proxy 清 conntrack」抓對兩刀半:症狀→conntrack✅、conntrack 是 kernel 表跟 kube-proxy process 無關✅、治標/治本歸錯邊需扶正(調 max=治標、找洩漏源=治本,s5/s6 老改進項復現)。

next(s21),順序:
1. step A 過期債(每堂 2 題上限,過期優先):07-20 到期「出廠全通」(s20 半過,結論靠提示、why 沒站住,已改掛 07-23)、「default-deny 分層」(s20 動手版學員喊跳過未跑);07-22 到期一批(見下)。
2. **4-5 七站骨架盲講冷測**(gate 答案卷,要求白板默數 1-7 一站不跳;C-4 四塊已備妥,這是把它們串成一條旅程)。留意謎題B 舊誤解(封包「先去 ClusterIP」)是否借屍還魂、第 1 站與第 3 站是否壓成一步。
3. 07-22 冷測:靜默無效「一段話組裝版」、兩張名單「兩關檢查程序」、**L4-L7 無框架新情境(禁 postgres/redis,過了才推 7)**、三分類家族第 2 輪(換成員);07-23 CNI 合約三件事快抽 + 出廠全通重抽。
4. **chunk 3+4 F/G 累積債補跑**(F Teach-to-Learn、G Interview Q&A 自 chunk 3 起未跑)。
5. lab **Step 5+Step 6 同一坐位收**(學員決策延後綁一起,6 驗收 5 不可拆;net-tool if12/.80 可當測試客戶端)→ 3-3 gate → **P2a phase gate(Examiner 首用)**。
6. pacing:冷測上限 15 分鐘;低電量改 micro-mode。**學員本堂數次要求「拉高整理/講學習價值/畫思維導圖」= 教學價值敏感度高,每個 chunk 先給面試/排障 payoff 再動手,效果好,續用**。bastion 待辦不變:砍 p0(仍未執行,worker2 因資源不足 NotReady,lab 不受影響)。

<details>
<summary>s19 斷點(已消化,留參考)</summary>

**s19 micro 已收(2026-07-20)。chunk 4-1「CNI 是一紙合約」過:hostNetwork 判準(「需不需要獨立網路」)學員自推 ✅;合約三件事 Recall 卡兩輪、把選配 NetworkPolicy 混進合約本體 → 簡化重教後預測題(漏路由=timeout)過。新 registry 卡 07-23。**

</details>

<details>
<summary>s18 斷點(已消化,留參考)</summary>

**s18 已收(2026-07-19,WR7 冷測專場,短堂)。三主題 3/3 過:L4-L7 新情境(postgres/redis,判準框架教練給)、conntrack 分工句收、三分類家族 counter 1/3。學員決策:lab Step 5+6 延後、綁一起做(6 驗收 5 不可拆)。s17「什麼都沒學到」已用冷測結果回應:s16/s17 的內容有留住。**

</details>

<details>
<summary>s17 舊斷點(已大部分消化,留參考)</summary>

**s17 已收(2026-07-19,家用 VM)。P2a chunk 3,lab 做到 Step 4 完(死法搬家實證收到)。**

叢集現況:家機 `kind-k8s-coach-p2a`(瘦身版 cp+1worker,Calico v3.28.2)留著沒砍;三層場景 + `default-deny-all` + `allow-dns` 都已 apply,Step 5 可原地續跑。labs/ 三檔(netpol-lab / default-deny / allow-dns)本機已重建;**更正:labs/ 是 .gitignore 刻意排除的本機暫存(不跨機同步,s16 沒有漏 commit),成品等 Step 6 完成後過價值門檻搬 `portfolio/k8s/manifests/netpol-demo/` 才 commit**。bastion 待辦不變:砍 p0。

next(s18),順序固定:
1. **Weekly Review 強制觸發(17-10=7),不可再延**。三主題:L4-vs-L7 新情境冷測(07-20 到期,禁 ALB/NLB 與 /admin 舊題)/ conntrack 分工句 / 三分類家族卡。
2. registry 07-22 三筆冷測:靜默無效「一段話組裝版」、兩張名單「兩關檢查程序」、YAML 藏寶圖(帶著 s17 四錯的記憶)。
3. lab Step 5 業務洞(frontend egress + backend ingress 兩條,學員自寫)→ Step 6 驗收矩陣 → 3-3 gate。F/G 兩段 chunk 3 至今未跑,Step 6 後補。
4. **pacing 鐵則(s17 教訓)**:學員低電量日改 micro-mode(一個單位就收),不要壓縮版全流程;開場前 15 分鐘只做冷測不排新內容。代打分界線驗證有效:**格式雜務可代打,決策點(如一張卡 vs 兩張卡)必須留給學員**。s17 尾學員情緒「什麼都沒學到」:成因=五連跳(WR 延後、Transfer 放掉、坑二重測放掉、YAML 代打、lab 一度喊跳)導致沒有任何一個「收攏時刻」;下堂開場用冷測結果直接回應這個感受,不辯論。

</details>

<details>
<summary>s16 舊斷點(已大部分消化,留參考)</summary>

**P2a chunk 3 NetworkPolicy,D 段 lab 做到 Step 3 收(2026-07-17)。** 叢集 `kind-k8s-coach-p2a`(Calico v3.28.2,podSubnet 192.168.0.0/16);frontend/backend/db 三層 + Service 已佈(labs/netpol-lab.yaml);`default-deny-all` 已 apply(labs/default-deny.yaml)。Step 3 分層實證已收:同一條 policy 兩種死法 — `curl http://db`=`Resolving timed out`(egress 53 被鎖,死在 DNS 層)vs `curl http://<podIP>:5678`=`Connection timed out`(跳過 DNS,死在連線層)。

next(s17):
1. **Weekly Review 觸發**(17-10≥7),取代正常 flow。WR6 三主題建議:NetworkPolicy default-deny(新)/ L4-vs-L7 判準(逾期+今日兩度失手)/ conntrack 分工句(未收)。
2. WR 後接 Step 4:開 DNS 洞(規格:egress to `namespaceSelector` kube-system + `podSelector` k8s-app=kube-dns,ports UDP/TCP 53)→ 重測應變 `Connection timed out`(死法從 DNS 層移到連線層)→ Step 5 開業務洞(兩邊都要開,ingress+egress 各一張名單)→ Step 6 驗收矩陣。
3. **chunk 3-2 語義三坑未教**(AND/OR 差一個 `-`、ingress/egress 兩張獨立名單、ipBlock),s16 因 pacing 砍掉,補在 Step 5 前。
4. **叢集待辦**:`kind delete cluster --name k8s-coach-p0`(指令已給學員,未執行)。兩叢集共 6 node 把 4 核心吃爆 → p2a control-plane `container runtime is down` NotReady(worker×2 正常,lab 不受影響)。砍掉 p0 後 control-plane 應自癒。shop 場景 manifests 在 `portfolio/k8s/manifests/ingress-lab/`,capstone 規劃是搬到 p2a 重佈。

⚠️ **s16 教練校準失誤三筆(不是學員的問題,寫下來防再犯)**:① 斷點明寫「開場少考、快進 hands-on」,實際整整一小時磨兩張複習卡 → 學員三度要求跳過。② 拿 chunk 4 未教內容(kubelet Ready 條件/CNI 合約)當 chunk 3 的 gate 題,學員答「不確定」是正確反應。③ session-log 教法備忘白紙黑字「學員偏好自己敲指令」,教練整堂搶鍵盤自己跑指令,學員當場糾正「要我自己裝才對」,並回頭要求「請說明前面做了什麼,前面是你做的,所以我不太瞭解」= 搶鍵盤直接造成理解斷層。s17 硬規則:**指令一律由學員敲,教練只給規格與判讀**;YAML 依 s13 慣例可給範本照打。

</details>
