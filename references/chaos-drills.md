# Chaos Drill 故障注入腳本庫

> **如何使用此檔:** 對應 Teaching Flow E 段(故障注入 Drill)。每個 drill 是一個獨立的「弄壞→限時 debug」單元。
> 學員在 D 段看過正常狀態後,E 段注入故障,限時定位根因。
> 每次 drill 踩坑記進 `k8s-coach-workspace/mistake-registry.md`。

---

## Drill 格式範本

每個 drill 固定用以下結構撰寫,確保格式一致、Coach 可直接套用:

```
### [Drill ID]: [標題]

**適用 phase**: P?

**前置條件**: 學員已完成的 chunk + 環境狀態

**破壞腳本** (Coach 執行,學員觀察症狀):
[具體指令]

**預期症狀** (學員先描述看到什麼,不直接說根因):
[kubectl/log 會出現什麼]

**限時** (回合制,非分鐘):
[N 回合內定位根因;一個「回合」= 學員提出一個假設 + 驗證指令 + 觀察結果]

**引導問題** (Coach 用的 Socratic 問題):
[一步一步引導,不直接給答案]

**正解**:
- 根因: [底層發生什麼]
- 修法: [怎麼恢復]
- 驗證修好了: [確認指令]

**學到的底層原理**:
[這個 drill 連回哪個 OS/網路/控制理論原理]
```

---

## P0 Drills

### P0-1: 刪除 Static Pod Manifest,觀察 kubelet 反應

**適用 phase**: P0

**前置條件**: 學員已完成 C-2(Control Plane 拆解),知道 static pod 由 kubelet 直接管理,不需要 API server 存活。環境: `k8s-coach-p0` kind cluster 已起。

**破壞腳本** (Coach 執行,學員先不看):
```bash
# 進入 control plane 節點
docker exec -it k8s-coach-p0-control-plane bash

# 備份,然後移走 kube-scheduler 的 static pod manifest
cp /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/kube-scheduler.yaml.bak
rm /etc/kubernetes/manifests/kube-scheduler.yaml
```

**預期症狀**:
```
# 學員在另一個 terminal 觀察到:
kubectl get pods -n kube-system -w
# kube-scheduler-k8s-coach-p0-control-plane 消失
# (幾秒內,kubelet 偵測到 manifest 不見,移除 Pod)

# 嘗試建新 Pod:
kubectl run test-pending --image=nginx
kubectl get pod test-pending
# NAME           READY   STATUS    RESTARTS   AGE
# test-pending   0/1     Pending   0          30s
# (一直 Pending,沒有 scheduler 能分配 Node)

# 現有 Running Pod 不受影響
kubectl get pods -A
# 其他 Pod 還是 Running
```

**限時**: 5 回合內定位根因(「為什麼新 Pod Pending?」)

**引導問題** (Coach 用):
1. 「新 Pod 卡在 Pending。你先看什麼?」(期望: kubectl describe pod 看 Events)
2. 「Events 顯示什麼?能看到 scheduler 有沒有嘗試分配?」(期望: 看到 `0/1 nodes available: 1 node(s) had untolerated taint`)
3. 「現有 Pod 還在跑,這說明什麼?」(期望: 現有 Pod 不需要 scheduler,只有「新建的」才需要)
4. 「回頭想想,scheduler 是什麼角色?誰在管它?」(期望: scheduler 是 static pod,kubelet 管)
5. 「kubelet 怎麼知道要跑 scheduler?如果 manifest 消失了,kubelet 會怎樣?」(期望: level-triggered reconcile,manifest 沒了就移除 Pod)

**正解**:
- 根因: `/etc/kubernetes/manifests/kube-scheduler.yaml` 被刪除,kubelet 偵測到 manifest 消失(level-triggered reconcile),移除了 kube-scheduler static pod。沒有 scheduler,新 Pod 無法被分配 Node,永遠 Pending。
- 修法:
```bash
# 在 control plane 節點內
cp /tmp/kube-scheduler.yaml.bak /etc/kubernetes/manifests/kube-scheduler.yaml

# 幾秒後 scheduler 重起
kubectl get pods -n kube-system | grep scheduler
```
- 驗證修好了:
```bash
# test-pending 應該很快被調度並變 Running
kubectl get pod test-pending -w

# 清理
kubectl delete pod test-pending
```

**學到的底層原理**:
1. kubelet 的 reconcile loop(level-triggered): 不斷比對 `/etc/kubernetes/manifests/` 目錄和實際跑的 Pod,manifest 消失就移除 Pod,manifest 出現就建 Pod。
2. scheduler 和 kubelet 的職責分工: scheduler 只負責「哪個 Pod 去哪個 Node」;kubelet 負責「把分配給我的 Pod 實際跑起來」。scheduler 不在,kubelet 的 running Pod 不受影響,但新 Pod 永遠拿不到 nodeName。
3. static pod 的設計哲學: control plane 元件用 static pod 跑,就算 API server 掛了,kubelet 還能獨立管理這些 Pod(避免「雞生蛋」問題)。

---

### P0-2: Cordon 一個 Node,觀察調度行為

**適用 phase**: P0

**前置條件**: 學員已完成 C-3(apply→Running 全流程),知道 scheduler 的 Filter + Score + Bind 流程。環境: `k8s-coach-p0` kind cluster 已起(需有 worker node,即 kind config 設多 node)。

**破壞腳本** (Coach 執行):
```bash
# 確認目前節點
kubectl get nodes

# 將 worker node 標記為不可調度(cordon)
kubectl cordon k8s-coach-p0-worker
```

**預期症狀**:
```
# cordon 後立刻看到節點狀態:
kubectl get nodes
# NAME                            STATUS                     ROLES
# k8s-coach-p0-control-plane      Ready                      control-plane
# k8s-coach-p0-worker             Ready,SchedulingDisabled   <none>

# 建新 Deployment:
kubectl create deployment test-cordon --image=nginx --replicas=3
kubectl get pods -o wide

# 所有新 Pod 都跑在 control-plane node(或其他未 cordon 的 node)
# cordon 的 worker node 上沒有新 Pod 被調度

# 原本在 worker node 的 Pod 仍然在跑(cordon 不驅逐現有 Pod)
```

**限時**: 3 回合內說出「cordon 影響哪些 Pod,不影響哪些」

**引導問題**:
1. 「你看到 `SchedulingDisabled`,這代表什麼?」(期望: 這個 node 不再接受新 Pod 調度)
2. 「原本在這個 node 上的 Pod 怎麼了?」(期望: 還在跑,沒被動)
3. 「如果要把現有 Pod 也趕走,還需要做什麼?」(期望: drain)
4. 「想想 scheduler 的 Filter 步驟,cordon 在 Filter 層面做了什麼?」(期望: 在節點上加了 `node.kubernetes.io/unschedulable` taint,Pod 沒有對應 toleration 就被 Filter 掉)

**正解**:
- 根因: `kubectl cordon` 給節點加上 `node.kubernetes.io/unschedulable:NoSchedule` taint,同時設 `spec.unschedulable=true`。Scheduler 在 Filter 階段把這個 node 過濾掉,新 Pod 不會被分配來。但 cordon 不驅逐現有 Pod,現有 Pod 繼續跑。
- 修法:
```bash
kubectl uncordon k8s-coach-p0-worker
kubectl get nodes
```
- 驗證修好了:
```bash
# worker node 恢復 Ready 狀態
kubectl get nodes

# 清理
kubectl delete deployment test-cordon
```

**學到的底層原理**:
1. Taint/Toleration 是 scheduler Filter 的一環: cordon 本質上是加一個 system taint。理解了這個,之後學 taints/tolerations 就是同一個概念的延伸。
2. cordon vs drain 的差別: cordon = 封閉入口(不接新 Pod); drain = 封閉入口 + 驅逐現有 Pod(用於節點維護)。兩者都服務「安全下線節點」的場景,但力道不同。
3. Scheduler 的職責邊界: scheduler 只管「新 Pod 去哪」;已經 Running 的 Pod 由 kubelet 管,cordon 不讓 kubelet 做任何事。

---

## P1 Drills

> (P1 填): Pod probe 失敗觸發 CrashLoopBackOff、resource limits 觸發 OOM kill、image pull 失敗(ImagePullBackOff)等。

---

## P2a Drills

> (P2a 填): CoreDNS 掛掉觀察 Service discovery 失敗、kube-proxy 規則被清空觀察 Service 不通、NetworkPolicy 阻斷流量等。

---

## P3 Drills(大型故障演練)

> (P3 填): 節點突然消失、流量暴增觸發 HPA、OOM 雪崩連鎖反應、滾動更新出包緊急 rollback。產出 runbook 進 portfolio。
