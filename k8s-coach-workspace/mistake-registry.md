# 踩坑登記簿 (間隔複習用)
<!-- 每次踩到坑就加一筆,定期回來抽考自己 -->

## 格式說明

每筆記錄用下方 block 格式。`下次抽考日` 建議設在 3 天後,複習後再往後推 7 天、14 天。

---

## 範例 (Example, 可刪除)

**日期:** 2026-06-16
**主題:** Pod 排程

**踩的坑:** `kubectl run nginx --image nginx` 後 Pod 一直是 `Pending`

**根因:** 叢集只有 control-plane 節點,但 control-plane 預設有 taint `node-role.kubernetes.io/control-plane:NoSchedule`,所以沒有可用的 worker 可以排程

**正確做法:** 建叢集時要帶至少一個 worker 節點 (例如 `lab-cluster.sh up p0` 帶 2 個 worker),或是手動 `kubectl taint` 移除 control-plane 的 taint

**下次抽考日:** 2026-06-19

---

<!-- 從這裡開始加你自己的踩坑記錄 -->

**日期:** 2026-06-18
**主題:** YAML 欄位拼錯 / 讀 validation error

**踩的坑:** Deployment apply 失敗 `strict decoding error: unknown field "spec.selector.matchLabels"`(把 `matchLabels` 打成 `metaLabels`)

**根因:** k8s 嚴格解碼,遇到不認識的欄位直接退件(防打錯字卻無聲失敗)。錯誤訊息的 `unknown field "A.B.C"` 是藏寶圖,完整路徑直指出錯的層級與欄位。

**正確做法:** 讀 `unknown field "路徑"` → 去檔案找該路徑那層,看欄位名「不是拼錯就是放錯層」。selector 認親的正確欄位是 `matchLabels`,且必須等於 template.metadata.labels。

**下次抽考日:** 2026-06-30 (2026-06-23 抽考過,需引導才答對「檢查在 API Server、與 etcd 無關」,推 +7)

---

**日期:** 2026-06-22
**主題:** P1 probe — liveness vs readiness 混淆

**踩的坑:** 認為 liveness probe 可以拿來檢查「service 準備好接新連線/請求了沒」(把 readiness 的職責塞給 liveness),延伸成「liveness 去 check DB 連線」。

**根因:** 沒抓住兩種 probe 的本質差別 = 失敗後的「動作」不同。liveness 失敗 → 重啟;readiness 失敗 → 切流量不重啟。檢查 DB 這種外部依賴若放 liveness,DB 一慢 → 全 Pod liveness 失敗 → 集體重啟 → CrashLoopBackOff 雪崩(且 reconnection 風暴可能把 DB 壓垮)。

**正確做法:** 判斷句「**Would a restart fix this?**」Yes(自己 deadlock/卡死)→ liveness 可管;No(DB/下游/外部依賴,重啟也修不好)→ 那是 readiness,頂多切流量等恢復。liveness 只檢查「我這個 process 還活著嗎」。

**下次抽考日:** 2026-06-25

---

**日期:** 2026-06-23
**主題:** P1 rollout — image 名稱打錯 → ImagePullBackOff

**踩的坑:** Deployment 的 image 打成 `ngimx:1.25`(n→m)。`kubectl apply` **成功**、Pod 也建了也排程了,但卡在 `ImagePullBackOff` / `ErrImagePull`。

**根因:** 驗證有邊界。`ngimx:1.25` 是**語法合法**的字串,API Server 無從得知這個 repo 不存在 → 不擋。真的去 registry 拉 image 的是 **kubelet,在第 5 棒(runtime pull)**,拉的那一刻才發現 `repository does not exist`。對比 `metaData` 這種 schema 錯,API Server apply 當場就退件。

**正確做法:** `ImagePullBackOff` 第一個動作 = `kubectl describe pod <name>` 看 Events。Events 會直接印 `Pulling image "ngimx:1.25"` + 拒絕原因,一眼看到打錯字。分辨三類:`i/o timeout`=網路/egress、`401`/`toomanyrequests`=認證/限流、`repository does not exist`/`not found`=名稱或 tag 打錯。

**下次抽考日:** 2026-06-26
