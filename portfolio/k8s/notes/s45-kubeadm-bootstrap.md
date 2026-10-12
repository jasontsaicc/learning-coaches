# s45 kubeadm 叢集建置(2026-10-12)

3 台 t3.medium Ubuntu 24.04:cp / w1 / w2。Ansible 準備 node,kubeadm 建叢集,Calico v3.33.0 當 CNI。

## 建置順序

| 步驟 | 誰做 | 產物 |
|---|---|---|
| kernel module、sysctl、swap、containerd | Ansible `node-prep.yml` | node 能跑 container |
| pkgs.k8s.io v1.36 repo + kubelet/kubeadm/kubectl + hold | Ansible `node-prep.yml` | 3 台 v1.36.5,版本鎖住 |
| `kubeadm init --pod-network-cidr=192.168.0.0/16` | kubeadm(cp) | certs、kubeconfig、static pod manifest |
| `kubectl apply -f calico.yaml` | Calico | Pod 網路,node 變 Ready |
| `kubeadm join` | kubeadm(w1/w2) | worker 拿到 kubelet 憑證 |

## Version skew

| 情況 | 結果 |
|---|---|
| cp v1.37 + kubelet v1.36 | 允許。新版看得懂舊版,kubelet 最多舊 3 個 minor |
| cp v1.36 + kubelet v1.37 | 不允許。舊 API server 看不懂新欄位 |

`apt-mark hold` 防止單台 node 被 `apt upgrade` 偷升。repo 網址寫死 `v1.36`,最多只升 patch。

## kubeadm 只產設定檔,然後退出

```
kubeadm init
  ├─ certs       /etc/kubernetes/pki
  ├─ kubeconfig  admin.conf / kubelet.conf
  └─ manifests   /etc/kubernetes/manifests/{etcd,kube-apiserver,kube-controller-manager,kube-scheduler}.yaml
                     │
                     ▼ kubelet 讀這個目錄
                 static pod(kubelet 直接叫 containerd 跑)
```

- 依賴套件是 Ansible 裝的,Pod 網路是 CNI 給的,都不是 kubeadm。
- apiserver crash:kubelet 重拉。controller-manager 不行,因為它要透過 API server 才看得到東西。
- manifest 被移走:kubelet 停掉那個 static pod。移走 scheduler → 新 Pod 沒人填 `nodeName` → `Pending`,Events 是空的。

## 沒有 CNI 時的因果鏈

```
沒有 CNI 設定
  → kubelet 回報 Ready=False(cni plugin not initialized)
  → node 自動加 taint node.kubernetes.io/not-ready:NoSchedule
  → scheduler 不排 coredns
  → coredns NODE=<none>,STATUS=Pending
```

- `NotReady`:kubelet 有回報,內容是「我沒準備好」。
- `Unknown`:kubelet 連不到 API server,沒有回報。
- 如果沒有 taint,coredns 會排上去,卡在 `ContainerCreating`(kubelet 拿不到 Pod IP)。
- `node-role.kubernetes.io/control-plane:NoSchedule` 是 kubeadm 加的,裝完 CNI 還在,coredns 有 toleration。

驗證:

```bash
kubectl describe node <cp> | grep -iE 'taints|cni|not-ready' -A1
```

## 誰用 node IP,誰用 Pod IP

| Pod | IP | 原因 |
|---|---|---|
| etcd、apiserver、controller-manager、scheduler、kube-proxy、calico-node | node IP | `hostNetwork`,不需要 CNI |
| coredns、calico-kube-controllers | `192.168.x.x` | 一般 Pod,IP 由 Calico 給 |

規則:**負責建立 X 的元件,不能依賴 X。**

| 元件 | 不能依賴 | 改用 |
|---|---|---|
| kube-apiserver | controller(要透過 API server) | kubelet + static pod |
| calico-node | CNI 給的 Pod IP(它自己就是 CNI) | hostNetwork |

## join 的雙向驗證

| 參數 | 誰驗證誰 |
|---|---|
| `--token` | cp 驗證 worker 有權加入 |
| `--discovery-token-ca-cert-hash` | worker 驗證 cp 的 CA 指紋,防假 cp |

成功後 kubelet 送 CSR,拿到 cp CA 簽的憑證(TLS bootstrap)。token 預設 24 小時過期,過期在 cp 上跑 `kubeadm token create --print-join-command`。

## 陷阱

- bastion 的預設 context 是 PROD EKS。lab 的 kubectl 一律在 cp 的 ssh session 跑。
- 在 bastion 跑 `kubectl get nodes` 看到 `10.89.x.x`、`-eks-` 版本、Amazon Linux,就是打到 prod。
