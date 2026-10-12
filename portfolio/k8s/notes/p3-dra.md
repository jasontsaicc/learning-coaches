# P3 補充 - DRA(Dynamic Resource Allocation,GPU 怎麼被排程)

> 2026-10-12 補。DRA 在 Kubernetes v1.34 GA(`resource.k8s.io/v1`,預設開啟)。對齊 NVIDIA 目標與 §12 GPU 模組。

## 這是什麼?(一句話)

DRA 讓 Pod 用「描述需求」的方式要裝置(要哪種 GPU、多少記憶體、能不能共用),由 scheduler 挑出符合的那顆裝置並記下分配結果;舊的 device plugin 只能說「給我 1 個 `nvidia.com/gpu`」。

## 用什麼比喻理解?

- device plugin = 停車場只告訴你「還有 3 個空位」。你要大車位、要靠電梯,它答不出來。
- DRA = 停車場公布每一格的尺寸、位置、有沒有充電樁,你填需求單,管理員挑一格寫上你的名字。

## 兩種模型並排

```
device plugin(舊,仍可用)                   DRA(v1.34 GA)
kubelet ◄─ 回報 nvidia.com/gpu: 4            DRA driver ─► ResourceSlice(每顆裝置 + attributes:型號、記憶體...)
   │                                          admin    ─► DeviceClass(一類裝置,CEL selector)
   ▼                                          workload ─► ResourceClaim / ResourceClaimTemplate
scheduler 只會「數數字」                                     "要 1 顆 DeviceClass=gpu 且 memory >= 40Gi"
   4 - 1 = 3 ✓                                    │
                                                  ▼
Pod: resources.limits:                       scheduler 比對 ResourceSlice → 選定裝置
  nvidia.com/gpu: 1                            → 寫進 claim 的 status.allocation
  (哪一顆?scheduler 不知道,                     │
   kubelet 端才決定)                              ▼
                                             kubelet 叫 DRA driver prepare 那顆裝置 → 容器啟動
                                             Pod: spec.resourceClaims + containers[].resources.claims
```

關鍵差異:舊模型裡 scheduler 看到的是整數,「是哪一顆」在 node 上才決定;DRA 把「哪一顆」提前到 scheduler,所以能按屬性挑、能共用、能把分配結果當成 API 物件查。

## 跟你已經會的東西接上

- P0 五棒:DRA 多了一棒「scheduler 分配 claim」,kubelet 那棒多了「叫 driver prepare」。Pod 卡 Pending 時,除了 CPU/memory 不夠,還要查 claim 有沒有被分配。
- 「宣告 vs 執行體」判準:ResourceClaim 是宣告(在 etcd),driver prepare 出來的裝置設定是執行體(在 node)。

## 踩過什麼雷?(預先列,還沒親手踩)

- 以為 DRA 取代了 device plugin、GPU Operator 不能用:DRA 是新增的路,device plugin 照樣支援。
- 以為裝了 k8s v1.34+ 就能用:API 在,但還要裝對應廠商的 DRA driver(NVIDIA 的是 `k8s-dra-driver-gpu`),支援度看 driver 版本。
- Pod Pending 只查 node 資源:DRA 下也要 `kubectl get resourceclaim` 看分配狀態。

## 面試怎麼回答?

「device plugin 把 GPU 當成可數的 extended resource,scheduler 只會做減法,不知道是哪一顆,也表達不了型號、記憶體或共用。DRA 讓 driver 用 ResourceSlice 公布每顆裝置的屬性,workload 用 ResourceClaim 以 CEL 描述需求,scheduler 選定裝置並寫進 claim,kubelet 再呼叫 driver 準備。代價是多一個 driver 元件和更多 API 物件,所以只有需要按屬性挑、要共用或要細粒度切分時才值得換。」

來源:[Kubernetes v1.34: DRA has graduated to GA](https://kubernetes.io/blog/2025/09/01/kubernetes-v1-34-dra-updates/)
