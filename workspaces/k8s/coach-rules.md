# 教練常駐規則(K8s)

<!-- 2026-09-09 自 session-log.md 逐字搬出,內容未改。每場 session 常駐讀取;
     session 敘事紀錄仍留在 session-log.md。 -->

## 學員背景與教法備忘

- 學員背景: DevOps 工程師,hands-on 有 (kubectl apply / 看 logs),底層理論弱;coding 初學。
- 教法備忘: 多用生活 analogy、用學員原話回扣、一次一個 chunk、語言要白。學員偏好自己敲指令,YAML 預設給規格。**(2026-07-19 s17 feedback)**:抽考改「情境/預測題+ASCII 圖上指認」格式,**一次只問一題**(塞多子題→學員只答第一個+煩躁);申論組裝只留 F 段、配學員自畫的圖;開場冷測上限 15 分鐘到點切新內容;格式雜務可代打、決策點留學員。學員用英文作答時附 `💬 English Polish`;教完流程主動附英文 mind map 供手抄默畫。**(2026-07-23 s21)**:面試目標確認為 **AWS Delivery Consultant (ProServe)** → **所有抽考包成客戶顧問情境**(「客戶遇到 X,你明天要進場」),不用「請解釋 Y」的問法;**每題正解後必附「L6 senior 會怎麼答」對照版**(開場宣告框架 → 每站掛怎麼查 → 假設排序 → 顧問層收尾);**判準句型專項**:學員固定只給結論不給判準(已跨五堂),每個答案強制「我看的是 X,**因為** [判準]」。story-bank 每堂機會式入帳(LP 佔 loop 近半)。
- 待補精準度:術語要用「DESIRED vs CURRENT」「reconcile loop 收斂」而非「監控數量」。**已補洞**:只有 API Server 直接讀寫 etcd,其他元件(controller/scheduler/kubelet)都透過 API Server 的 watch/update,不直接碰 etcd(P0 學員口誤「kubelet 寫回 etcd」)。
- symptom→棒次地圖已教: Pending=scheduler / ContainerCreating=kubelet 網路volume / ImagePullBackOff=runtime拉image / CrashLoopBackOff=容器或probe。
- P1 已澄清:Linux namespace(kernel 隔離視野)≠ k8s namespace(邏輯分組,**不做隔離**,擋網路要 NetworkPolicy)。學員自己問出這個撞名點,理解力好。
- ~~術語卡 kubeconfig / context / kind~~ **2026-06-22 移除**:學員指出定義型瑣碎詞/工具名面試不考,違反價值門檻(memory [[k8s-portfolio-value-gate]])。current-context 改記為 ops 安全習慣,不當卡。

## 教練執行紀律（長效，違反過就寫在這裡）

- **指令一律由學員敲，教練只給規格與判讀**（s16 搶鍵盤造成理解斷層，學員當場糾正；YAML 依 s13 慣例可給範本照打）。
- **why-first 硬規格：不給預測就不給下一發指令**（s24 訂，s25 實測有效，s27 教練沒執行，s28 起真的執行；學員答不出來就縮成二選一）。
- **不要拿未教內容當 gate 題**（s16：用 chunk 4 的 kubelet Ready / CNI 合約考 chunk 3，學員答「不確定」是正確反應）。
- **斷點寫了「開場少考快進 hands-on」就要照做**（s16 反例：整整一小時磨兩張複習卡，學員三度要求跳過）。
- **版面即認知負荷（s27 實證）**：教學段落與動手指令不同框、進度表最多 3 行、一則訊息只放一個動作。學員問「這到底在幹嘛」= 版面問題不是難度問題，簡化成三句話 + 一個動作即恢復。
- **決策癱瘓時直接代為收工**：學員答「不知道啦」這類訊號出現時不再丟選擇題，教練逕行決定收工並存檔（s27 正確處置）。
- **新內容排最前面，複習與冷測壓到課堂尾巴（2026-08-20 s28 學員拍板）**：舊順序把複習放開場、新內容排最後，疲勞時就被砍，P2b 因此 14 天沒推進。冷測不砍（隔堂測留存是唯一有效方法），只改排序。
- **每給一個判準句，立刻接一題只有換皮的應用題，答對才算給完（2026-08-20 s28 訂）**：s28 同堂兩次「判準給完 30 秒內套用不上」。隔堂測的是留存，當場測的是有沒有真的接收到。
- **開場叢集掛掉直接修、不當教材（2026-08-20 s28 訂）**：`for n in control-plane worker worker2; do docker exec k8s-coach-p2a-$n systemctl restart containerd; done`，25 秒。這個病看過六次，沒有新的教學價值。
- **任何查詢指令前必須先給完整情境與決策用途（2026-08-21 學員回饋）**：禁止只丟「跑這條、貼輸出」。固定四句：①現在看到的 symptom / 所在流程棒次；②這一發要驗證的 hypothesis；③為什麼這條指令能區分嫌犯；④輸出 A/B 各自導向哪個 next action。接著讓學員用一句話說「我現在要查 X，因為 Y」；說不出目的就補 context，不准靠複製貼上前進。純環境修復等非教材動作可明說「這不是教材，只是恢復 lab」後直接執行。

