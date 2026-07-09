# P0 心智模型：`kubectl apply` 到 Pod `Running` 全流程

> 自學用參考圖。回家照著默畫,目標：不看圖也能畫出五棒 + 講出每棒做什麼。

## 圖一：接力賽視角（記順序用，先背這張）

```
 ①          ②           ③              ④             ⑤
kubectl --> API     --> etcd  --> controller --> scheduler --> kubelet --> runtime
 apply      Server      存          看desired,     挑 node:       叫 runtime:
 (你的願望)  (唯一前門)   desired     建 Pod 物件    filter+score   拉image>起容器>跑probe
                                                                      |
                                                                      v
                                                       回報 actual=Running >> 寫回 etcd
                                                       desired(3)==actual(3) >> loop 閉合
```

## 圖二：Hub 視角（記架構用，重點是「萬物經過 API Server」）

```
        CONTROL PLANE  (大腦團隊 / 只搬帳本,從不碰容器)
   +-------------------------------------------------------+
   |                                                       |
   |   controller          scheduler        (其他 controller)
   |   建 Pod 物件          挑 node              ...        |
   |       \                  |                  /         |
   |        \                 |                 /          |
   |         v                v                v           |
   |        +---------------------------+   +---------+    |
   |        |        API Server         |<->|  etcd   |    |
   |        |       (唯一前門/守門人)     |   | (帳本)  |    |
   |        +---------------------------+   +---------+    |
   |              ^                ^                       |
   +--------------|----------------|------------------------+
                  | (1) apply      | (4)(5) kubelet 也只跟
                  |                |      API Server 講話
              +-------+        +-----------------------------+
              |kubectl|        |  WORKER NODE                |
              | (你)  |        |   +---------+               |
              +-------+        |   | kubelet |--> containerd |
                               |   +---------+   拉image     |
                               |                 起容器      |
                               |                 跑 probe    |
                               +-----------------------------+
```

重點：controller / scheduler / kubelet **彼此不直接對話**,全部只跟 API Server 讀寫。

## 五棒對照表

| # | 演員 | 在哪 | 做什麼 | 交給下一棒 |
|---|------|------|--------|-----------|
| 1 | kubectl | 你的電腦 | 送出 desired state(願望)| 給 API Server |
| 2 | API Server | control plane | 唯一前門,驗證後寫進 etcd | 存進 etcd |
| 3 | controller | control plane | 看 desired vs actual,建 Pod 物件 | 留下沒分配 node 的「孤兒 Pod」 |
| 4 | scheduler | control plane | filter(能不能放)+ score(放哪好)| 寫綁定 Pod->Node |
| 5 | kubelet | worker node | 叫 runtime 拉 image、起容器、跑 probe | 回報 actual=Running |

## 三個必記心法

1. **declarative**：你宣告「要長怎樣(desired state)」,不是「下指令」。
2. **reconcile loop 無所不在**：controller / scheduler / kubelet 全都在跑「量 → 比 → 修」的迴圈。學會一個,全部秒懂。
3. **只有 kubelet 碰容器**：control plane(API Server/etcd/controller/scheduler)整段只在搬帳本記錄,手上沒沾過容器。

## 排障金鑰：狀態 -> 壞在哪一棒

| Pod 狀態 | 壞在哪一棒 | 方向 |
|----------|-----------|------|
| `Pending` | scheduler | 沒 node 合格(CPU/taint/selector)|
| `ContainerCreating` 太久 | kubelet | 網路 / volume / CNI 起不來 |
| `ImagePullBackOff` | kubelet -> runtime | image 名字錯 / 沒權限拉 |
| `CrashLoopBackOff` | kubelet -> 你的程式 | 容器一起來就掛 / probe 一直失敗 |

第一個指令通常是 `kubectl describe pod <name>` 看 events,或 `kubectl logs <name>`。
