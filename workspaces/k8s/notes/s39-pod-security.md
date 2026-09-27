# s39 C-6 Pod Security: who the process is, where it can reach, who checks

Visual page: https://claude.ai/artifact/5BMgeH7bvfwwwJBwLopqvZ

## Take-away (3 lines)

```
1. root in a container = UID 0 on the node (one shared kernel)
2. PSS = guard at the API Server door. A non-compliant Pod never enters the cluster
3. Writing runAsNonRoot in YAML is not enough. The image must also run as non-root
```

## 1. Container root is host root

Same process, two views. The pid namespace renumbers the PID (visibility). The UID is not changed (identity).

```
 inside container (ps)          on the node (ps)
 PID  USER  CMD                 PID    USER  CMD
 1    root  nginx   ---------->  48213  root  nginx
      ^ renumbered                      ^ same UID
```

User namespaces can map 0 inside to 100000 outside, but Kubernetes does not turn it on by default (`hostUsers: false`).

## 2. Two doors

```
 door 1: can it reach the file?    door 2: is it allowed?
 (mount namespace)                 (UID vs file rwx)
 root only helps at door 2. If door 1 blocks, root is useless.
```

|                  | inside container          | escaped                  |
|------------------|---------------------------|--------------------------|
| UID 0 (root)     | cannot read (door 1)      | CAN read  <- the danger  |
| UID 1000         | cannot read (door 1)      | cannot read (door 2)     |

Column A is the same for root and non-root. `runAsNonRoot` only changes column B.

## 3. Container escape and assume breach

Escape (翻牆) = the process gets outside its namespaces and reaches the node.

| Hole | Example | Can we stop it? |
|---|---|---|
| kernel bug | one kernel shared by all containers | wait for patch |
| runtime bug | runc CVE-2019-5736: root in container overwrites host runc | wait for patch |
| our own config | `hostPath: /`, `privileged: true`, `hostPID` | yes, most common |

Assume breach: the wall will break one day. Decide what the attacker holds after it breaks. Non-root = intern badge, cannot open the node's safe.

## 4. PSS vs Kyverno

Both sit at the Admission step of the API Server.

```
 kubectl apply -> [AuthN who] -> [AuthZ RBAC] -> [Admission: PSS / Kyverno] -> etcd -> kubelet
```

| | PSS | Kyverno |
|---|---|---|
| Source | built in | installed separately (runs as Pods) |
| Rules | 3 fixed levels: privileged / baseline / restricted | write your own |
| Turn on | namespace label `pod-security.kubernetes.io/enforce=restricted` | ClusterPolicy objects |
| Example | "no root" | "image must come from our ECR" |

PSS also has `warn` and `audit` modes: see who would fail before you enforce.

## 5. Lab: two checkpoints (home VM, `kind-k8s-coach-p2a`)

```
 try 1: naked nginx
   -> Error from server (Forbidden): violates PodSecurity "restricted:latest":
      allowPrivilegeEscalation, capabilities, runAsNonRoot, seccompProfile
   -> stopped at admission. get pods shows nothing.

 try 2: same image nginx + 4 securityContext fields
   -> pod/dressed-nginx created                     (admission passed)
   -> STATUS CreateContainerConfigError
   -> Events, source = kubelet:
      container has runAsNonRoot and image will run as root

 try 3: image nginxinc/nginx-unprivileged
   -> Running,  id -> uid=101(nginx)
```

```
 (1) API Server admission          (2) kubelet on the node
     reads the YAML only               opens the image, checks the real user
     "runAsNonRoot written" OK         "image runs as root" FAIL
```

## 6. Why does an app want root?

Not for routing tables. That is CNI / kube-proxy work (needs `NET_ADMIN`, lives in `kube-system` with privileged PSS).

A normal app like nginx wants root for two plain reasons:

1. bind port 80 (ports below 1024 need root or `CAP_NET_BIND_SERVICE`)
2. write root-owned dirs like `/var/cache/nginx`

Fix: non-root image (`nginx-unprivileged` listens on 8080, `USER 101`), or `runAsUser` + `emptyDir` on the paths it writes.

## 7. Traps

| Trap | Truth |
|---|---|
| `pod/... created` means it runs | It only passed admission. Check `get pod` |
| Deployment Pods rejected by PSS | `get pods` shows nothing, rollout stuck 0/3. Look at `kubectl describe rs` events |
| nginx needs root to change routes | Port 80 + root-owned dirs |
| root reads the node file without escaping | Door 1 blocks first |
| After hardening: `(13: Permission denied)` | non-root user writing a root dir |
| After hardening: `(30: Read-only file system)` | `readOnlyRootFilesystem`, mount an `emptyDir` |

## 教別人版

- **這是什麼?** 讓 Pod 就算被攻破、翻出 container,手上也只有普通人的權限;PSS 是在叢集門口強制這件事的警衛。
- **用什麼比喻?** node 是一棟大樓。container 是鎖住的會議室(namespace = 走得到哪),UID 是識別證(打得開哪個保險箱)。PSS 是大樓門口檢查制服的警衛,kubelet 是會議室門口再看一次真實識別證的人。
- **踩過什麼雷?** 以為 root 沒翻牆也讀得到 node 檔案;以為 `created` 就是跑起來;以為 nginx 要 root 是改路由表;YAML 寫了 non-root 但 image 還是 root。
- **面試怎麼回答?** "Containers share the host kernel, so root inside is UID 0 on the node. Namespaces limit what a process can see, not who it is. If it escapes, it's root on the host. So I set runAsNonRoot, drop all capabilities, block privilege escalation, and enforce the restricted Pod Security Standard at admission. The image also has to support non-root, or the kubelet refuses to start it."

## Mind map

```
                          Pod Security
                               |
        +----------------------+----------------------+
        |                      |                      |
   Who is it?             Where can it go?        Who checks?
        |                      |                      |
   UID 0 = node root      namespace = wall        admission (PSS/Kyverno)
   runAsNonRoot           escape: kernel bug,       reads YAML
   caps drop ALL            runc bug, hostPath    kubelet
   no privilege escal.    assume breach             reads image user
                                                  -> CreateContainerConfigError
```

## Next

- C-6 F/G (not run yet).
- Tail cold tests: IRSA trust vs permission, blast radius axis.
- Lab leftovers (home VM): ns `pss-lab`, Pod `dressed-nginx`.
