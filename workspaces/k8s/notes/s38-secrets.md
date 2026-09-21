# s38 C-6 Secrets: where it lives, who it stops, how it rotates

## 1. Secret is not encrypted by default

- `kubectl get secret -o yaml` shows base64. base64 is encoding, not encryption.
- In etcd the value is stored as raw bytes. Lab proof (kind, no encryption config):

```
kubectl -n kube-system exec etcd-k8s-coach-p2a-control-plane -- etcdctl ... get /registry/secrets/default/db-cred | strings
password
S3cretPa55        <- plain text on disk
```

```
 user sees              API Server             etcd disk
 UzNjcmV0UGE1NQ== <---  base64 only for  <---  S3cretPa55
                        JSON output
```

## 2. Each layer stops a different person

```
 vault      = etcd
 vault key  = KMS / EncryptionConfiguration key (API Server holds it)
 teller     = API Server
 ID check   = RBAC

 Developer / CI SA --"give me db-cred"--> API Server
                                           1. RBAC allows get secrets
                                           2. decrypt with KMS
 Developer / CI SA <------ S3cretPa55 -----+

 Thief with etcd backup file --> no key --> cannot read
```

| Threat | Layer that stops it | Fix |
|---|---|---|
| Stolen disk / etcd backup | encryption at rest | EKS: on by default (1.28+), can use own KMS key. On-prem: write `EncryptionConfiguration`, off by default |
| Stolen SA token with `get secrets` | RBAC | shrink blast radius: `resourceNames`, or no `get secrets` at all |

Rule: KMS does not help against a valid token. The API Server decrypts for anyone RBAC allows.

## 3. Rotation: env vs volume

| Mount | After Secret update | Why |
|---|---|---|
| env var | old value, restart Pod | env is written into process memory once at start |
| volume | new file in ~1 min | kubelet syncs the file |
| volume + `subPath` | old value | bind mount of one file, kubelet does not swap it |

Lab proof after update: `env=S3cretPa55`, `file=N3wPa55`.

Trap: app reads the file once at startup and keeps it in a variable = still a snapshot.
Fix: app re-reads on auth failure, or `kubectl rollout restart deployment/<name>`.
Same as ECS: task definition `secrets` from SSM are read at task start only.

## Mind map

```
                         K8s Secret
                             |
        +--------------------+---------------------+
        |                    |                     |
   Where it lives       Who it stops          How it rotates
        |                    |                     |
   etcd = plain text    backup thief          env = snapshot
   base64 = display     -> encryption at rest    (restart Pod)
   only                    (KMS / EncConfig)   volume = kubelet sync
                        token thief              (~1 min)
                        -> RBAC blast radius   subPath = no sync
                           (resourceNames)     app reads once
                                                 = snapshot too
```

## Next

- C-6 chunk 3: securityContext + Pod Security Standards (`pss-lab`, enforce=restricted).
- Lab leftovers: `db-cred` Secret and `cred-demo` Pod in `default`.
