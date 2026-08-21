# S29 — Dynamic Storage

## Whiteboard mind map

```text
                 Kubernetes Storage
                         |
       +-----------------+-----------------+
       |                 |                 |
   Key Objects         Workflow            CSI
       |                 |                 |
StorageClass          PVC Created      Controller
= Template                |            = Create Disk
                         PV
PVC = Request              |           Node Plugin
                     PVC Bound          = Mount Disk
PV = Storage               |
                         Pod
```

```text
WaitForFirstConsumer
Pod chooses AZ -> Create EBS in the same AZ
```

```text
Troubleshooting
PVC Pending -> describe PVC
PVC Bound + Pod stuck -> describe Pod
```

```text
Rule   = StorageClass + PVC
Engine = Provisioner
```

## Key ideas

- `StorageClass` 是儲存型錄，PVC 是需求，provisioner 才是實際建立儲存的 engine。
- EBS 不能跨 AZ attach。`WaitForFirstConsumer` 先等 scheduler 選定 node/AZ，再於同 AZ 建 EBS。
- CSI controller plugin 負責 create/delete/attach；CSI node plugin 負責 node 上的 mount/unmount。
- `attach != mount`：attach 讓 node 看見 block device；mount 才讓 Pod 看見 filesystem。
- PVC `Bound` 只是 control-plane 綁定證據；Pod 卡 `ContainerCreating` 時用 `kubectl describe pod` 查 `FailedMount`。
- `persistentVolumeReclaimPolicy: Delete` 會刪除 PV 與後端儲存；`Retain` 會留下資料等待人工處理。

## Lab evidence

```text
PVC Pending
-> waiting for first consumer
-> Create Pod
-> Provisioner creates PV
-> PVC Bound
-> Pod Running
-> Read hello-from-storage
```

- Context: `kind-k8s-coach-p2a`
- StorageClass: `standard`
- Provisioner: `rancher.io/local-path`
- Binding mode: `WaitForFirstConsumer`
- Reclaim policy: `Delete`
- Provisioner log showed `ProvisioningSucceeded` and the physical node path under `/var/local-path-provisioner/`.

## Next action

Verify cleanup:

```bash
kubectl delete pod sc-demo
kubectl delete pvc sc-demo
kubectl get pv
```

