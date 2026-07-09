# P5 平台工程 / GitOps: One Commit, Safely to Production

> **如何使用此檔:** 這是 P5 的教學素材庫,供 coach 在 C 段讀取並改編。
> 不要逐字唸稿,依學員反應選切面。每個 chunk 通過 Feynman Gate 再往下走。
> **English Ramp 檔位: P5 = 主教材大量英文(接近官方文件的語言),中文只做點破。**
> 本檔正文刻意用英文寫,它本身就是學員的閱讀材料與 Say-it-in-English 素材來源。
> 口頭教學仍照學員當下偏好調配(他在 P2a 曾明說中文為主);但 P5 起,朗讀、複述、
> Feynman teach-back 應大量切到英文,教練持續給 English Polish。
> 學員歷史已知的複利點都標了「回扣」;未知狀態用 [RUNTIME] 留白。

---

## P5 學習藍圖

**Goal**: Assemble everything from P0 to P4 into a platform where **one Git commit reaches
production automatically and safely**, and be able to operate that platform: upgrade it,
back it up, extend it, and explain every moving part at a senior interview.

**P5 中心問題**: Between `git push` and "the new version is safely serving production
traffic", what happens, which components make it automatic, and which make it *safe*?

這條中心軸也是全課程的收割點: P0 的 reconcile loop、P2a 的「物件=規則 / Controller=引擎」、
P2b 的 provisioner,在 P5 全部收斂成同一個心智模型的不同實例。教材裡標了「複利時刻」的段落,
教練的任務是讓學員**自己**說出這件事,不是替他說。

**學習路徑(Simon 切塊)**:

| Chunk | 主題 | 核心問題 | Keystone |
|-------|------|---------|----------|
| C-1 | Helm | How do we stamp out YAML at scale, and why is Helm *not* a controller? | |
| C-2 | GitOps / ArgoCD | What changes when Git becomes the desired state and a controller reconciles the cluster to it? | ✅ |
| C-3 | CRD + Operator | How do you teach the API server new object types, and give them their own reconcile loop? | ✅ |
| C-4 | Admission Webhooks | How do you intercept every API request, and what happens when the interceptor dies? | |
| C-5 | Cluster Upgrades | How do you replace the platform underneath running workloads? | |
| C-6 | etcd Operations | How do you back up, restore, and reason about the store everything depends on? | ✅ |
| C-7 | EKS Production Terraform | How do you make the cluster itself reproducible? | |
| C-8 | Progressive Delivery | How does a commit prove itself safe before taking all the traffic? | |

**環境前置**: `scripts/lab-cluster.sh up p5` 起 kind 3 節點。
**安全鐵律**: 每個 lab 動手前先 `kubectl config current-context`,確認是 `kind-k8s-coach-p0`
才 apply(機器上有公司 PROD EKS kubeconfig)。C-7 的 EKS lab 例外走 terraform,指令只產生、
學員親手執行,命名前綴 `billing-dev-eks-*`,結尾必跑 `terraform destroy` 並驗證。

---

## C-1: Helm, the YAML Factory (對照組)

### 核心概念

Helm solves a boring but real problem: you have 30 microservices whose manifests are 90%
identical, and 3 environments whose values differ. Copy-pasting YAML does not scale.

Three pieces:

- **Chart**: a directory of Go-templated manifests plus metadata. The blueprint.
- **Values**: the variables you inject per environment (`values.yaml`, `-f prod-values.yaml`, `--set`).
- **Release**: one installed instance of a chart in a cluster, with a name and a revision history.

```
   chart (templates/*.yaml)  +  values.yaml
                 |
                 v  helm render (client-side)
          plain Kubernetes YAML
                 |
                 v  helm sends it to the API server, records a release, and walks away
              cluster
```

中文點破: helm 是「產 YAML 的工具 + 記帳本」,render 完、apply 完就下班。
It has **no reconcile loop**. Nothing watches. This is the deliberate contrast that sets up C-2.

Where does the ledger live? Helm stores each revision as a Secret in the release namespace
(`sh.helm.release.v1.<name>.v<N>`), containing the fully rendered manifests. That is all
`helm rollback` does: re-apply the manifests recorded in an older revision.

`helm upgrade --atomic`: if the upgrade fails (a resource is rejected, or `--wait` times out
waiting for readiness), Helm automatically rolls back to the previous revision. Without it,
a half-failed upgrade leaves the release in `pending-upgrade` or `failed` state.

**Hooks 的坑** (pre-install / pre-upgrade / post-* Jobs):

- Hook resources are *not* part of the release. `helm uninstall` does not delete them unless
  you set `helm.sh/hook-delete-policy`.
- A pre-upgrade Job that already ran cannot be re-created with changed immutable fields; the
  upgrade dies with an immutability error. Common fix: delete-policy `before-hook-creation`.
- `--atomic` rollback does not "undo" what your hook Job *did* (a DB migration, for example).
  Helm can roll back YAML; it cannot roll back side effects.
- Anything under `crds/` is installed once and **never upgraded or deleted** by Helm. CRD
  lifecycle is on you (this becomes a real incident in C-3).

### 動手觀察

```bash
kubectl config current-context
helm create demo
helm template demo ./demo | head -40
helm install demo ./demo
kubectl get secret -l owner=helm
helm upgrade demo ./demo --set replicaCount=3
helm history demo
helm rollback demo 1
helm history demo
```

引導問題: 「`helm rollback` 為什麼快?它去哪裡拿舊 YAML?」(from the release Secret,
same reason P1 rollback 快是因為舊 ReplicaSet 留著: history is kept, not recomputed.)

### 打穿底層 (First-Principles Dive)

Templating is the classic configuration-management problem; Helm's Go templates play the
same role as Jinja2 in Ansible. The deeper point is *state tracking*: Helm tracks state
**client-side, per operation** (release secrets), while Kubernetes controllers track state
**server-side, continuously** (level-triggered reconcile, P0 C-1). Helm is edge: it acts at
the moment you run a command. If reality drifts afterwards, Helm neither knows nor cares.

**遷移題**: "Someone runs `kubectl delete deployment demo` on a Helm-installed release.
Will Helm re-create it? What *would* re-create it, and from which phase do you know that
component?" (Helm: no. A ReplicaSet's Pods would come back via the P0 reconcile loop, but
the Deployment object itself is gone until a human or a GitOps controller re-applies it.
回扣學員 P0 原話「比對現有環境進行更新」: helm 恰恰**不做**這件事。)

### 誘答彈藥 (輕量,對照組專用)

- 「Helm 會持續確保 chart 裡的資源存在;有人誤刪 Deployment,Helm 發現後會補回來。」
  錯: Helm has no running component in the cluster and no watch. It only acts when you run
  a command. 這題是 C-2 的鋪墊,學員若中招,C-2 的 ArgoCD 對照會特別有感。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 平台團隊維護一個 internal base chart,30 個服務只寫各自的 values |
| **生產怎麼做** | Chart 版本進 chart registry(OCI),values 分層: base values + per-env overrides。CI 跑 `helm template` + kubeconform 驗 schema,再交給 CD |
| **真實踩坑** | `helm upgrade` 卡死報 `another operation (install/upgrade/rollback) is in progress`: 上一次 upgrade 的 process 被 CI 砍掉,release 停在 `pending-upgrade`。解法: `helm rollback` 到上一個 deployed revision(或 `helm history` 找,不要直接刪 release secret 除非理解後果) |
| **面試怎麼問** | "Is Helm a controller? What happens if resources drift after `helm install`? How does `helm rollback` work internally?" |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| release | /rɪˈliːs/ | One installed instance of a chart, with a revision history stored as Secrets | chart 裝進 cluster 的一次實例 + 它的記帳本 |

---

## C-2: GitOps / ArgoCD (keystone, 全課程複利收割點)

### 核心概念

GitOps in one sentence: **Git holds the desired state; a controller in the cluster
continuously reconciles the live state toward it.**

Read that sentence again slowly. You have seen every word of it before.

```
        Git repo (desired state)          cluster (actual state)
              |                                  ^
              |   ArgoCD application controller  |
              +----> render manifests ---------->+
                     compare live vs rendered
                     diff != empty  => OutOfSync
                     (optionally) sync to converge
```

**複利時刻(教練必做,讓學員自己說)**: 先別解釋 ArgoCD 架構。把上圖遮住下半,只給
"Git = desired state, ArgoCD = a controller that watches it and converges the cluster",
然後問: 「這個模式你在哪裡見過?至少講三個。」預期他自己接出: P0 ReplicaSet controller
(DESIRED vs CURRENT)、P2a Ingress 物件 vs Ingress Controller(規則=資料 vs 執行=引擎)、
P2b/session 11 type:LoadBalancer 的 cloud-controller provisioner。然後要他把 session 11
定型的三合一對照表**親手加一列**:

| 規則(資料) | 引擎(執行者) |
|------------|--------------|
| Service/Endpoints | kube-proxy 寫 iptables |
| type: LoadBalancer spec | cloud controller 去雲上生 LB |
| Ingress 物件 | Ingress Controller (nginx Pod) |
| **Git repo 裡的 manifests** | **ArgoCD application controller** |

He should say the punchline himself: 這是同一個心智模型,只是 desired state 從 etcd 裡的
物件升級成整個 Git repo。[RUNTIME: 若他卡住,依 mistake-registry 選提示強度,先回放他
session 11 對照表原話再問。]

**The object model** (near-official language, worth reading aloud in English):

- **Application** (a CRD, foreshadowing C-3): binds a *source* (repoURL, path,
  targetRevision) to a *destination* (cluster, namespace), plus a syncPolicy.
- **AppProject**: the multi-tenancy boundary. Restricts which repos, destination clusters,
  namespaces, and resource kinds Applications in the project may use.

**Two independent axes** (學員弱點「用詞精準度」的高發區,先講清楚):

- **Sync status**: `Synced` / `OutOfSync`. Does live state match Git? A pure diff.
- **Health status**: `Healthy` / `Progressing` / `Degraded`. Is the workload actually OK?
  (Deployment available, Ingress has an address, etc.)

An app can be Synced and Degraded (Git says replicas: 3, live says replicas: 3, all Pods
CrashLoopBackOff). It can be OutOfSync and Healthy. 中文點破: 一軸問「跟 Git 一樣嗎」,
一軸問「活得好嗎」,兩軸獨立。

**Sync behavior**:

- Manual sync: ArgoCD only *reports* OutOfSync; a human clicks Sync.
- Automated sync: converge whenever Git changes.
- `selfHeal: true`: also converge when the *cluster* changes (someone kubectl edits).
- `prune: true`: delete live resources that are no longer in Git.
- **Sync waves**: `argocd.argoproj.io/sync-wave: "N"` annotation orders resources within a
  sync (wave 0 CRDs and namespaces, wave 1 databases, wave 2 apps). ArgoCD waits for each
  wave to be healthy before the next.
- **Resource hooks**: PreSync / Sync / PostSync / SyncFail, same idea as Helm hooks but
  executed by a controller that stays around.
- **App-of-apps**: a root Application whose source path contains *other Application
  manifests*. Sync the root once, and the controller fans out the whole platform. This is
  how you bootstrap a cluster from one commit.

### 動手觀察

```bash
kubectl config current-context
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd get pods
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

建一個 Application 指向公開範例 repo(guestbook),學員自己寫 YAML(給規格): source =
`https://github.com/argoproj/argocd-example-apps` path `guestbook` targetRevision `HEAD`,
destination = in-cluster + namespace `guestbook`, 先用 manual sync。然後:

```bash
kubectl -n argocd get applications
kubectl -n guestbook scale deployment guestbook-ui --replicas=3
kubectl -n argocd get application guestbook -o jsonpath='{.status.sync.status}'
```

親眼看 OutOfSync 出現。再開 automated + selfHeal,重做 scale,看它被**改回來**。
This single observation is the whole GitOps value proposition.

### 打穿底層 (First-Principles Dive)

1. **Level-triggered again** (P0 C-1 直接複利): ArgoCD polls the repo (default every 3
   minutes) *and* continuously compares live vs rendered. A Git webhook only makes it
   faster; losing the webhook loses nothing, because the loop looks at *state*, not events.
2. **Pull vs push CD**: classic CI-push (Jenkins runs kubectl with prod credentials) means
   cluster admin credentials live in the CI system, outside the cluster. GitOps pull means
   the agent runs *inside* the cluster and only needs read access to Git. Smaller blast
   radius, and the cluster can converge even when CI is down.
3. **Audit and rollback for free**: desired state history = `git log`. Rollback = `git
   revert`. Code review of production change = PR review. This is P0 C-0's "GitOps 的基礎"
   洞見兌現的地方。

**遷移題**: "Compare ArgoCD with Terraform as reconciliation systems. Where does each keep
desired state, where does each keep *its view of* actual state, and which one is
level-triggered?" (TF: desired = code, view of actual = state file, converges only when a
human/CI runs apply; drift persists silently until the next plan. ArgoCD: continuous loop.
這題同時鋪 C-7。)

### 誘答彈藥 (keystone 必備)

1. 「有人在 prod 上 `kubectl edit` 改了 Deployment 的 image。ArgoCD 尊重 cluster 裡的
   實際狀態,會把他的改動保留下來,只在下次 Git commit 時才動作。」
   錯,而且要逼他分層答: drift detection 立刻標 OutOfSync(比對是持續的);改動會不會被
   打回去取決於 syncPolicy: automated + selfHeal 會在幾分鐘內revert;manual sync 則保留
   到下次有人 sync。回扣 P0 phase-0 教材就埋過的坑: kubectl edit 的東西被 CD 蓋回去,
   根因是違反「Git 是 source of truth」。
2. 「ArgoCD 靠 Git webhook 觸發部署;webhook 掉了,那個 commit 就永遠不會被部署,除非
   有人手動 sync。」錯: webhook 只是加速,預設 3 分鐘 polling 照樣收斂。這就是 P0 C-1
   level-triggered vs edge-triggered 的原題換皮,學員若答不出,把 P0 那題「controller
   當機 10 分鐘」搬出來對照。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 公司要求所有 prod 變更可追溯、可 review、可一鍵回滾 |
| **生產怎麼做** | App-of-apps(或 ApplicationSet)bootstrap 整個 cluster;deploy = 對 env repo 開 PR 改 image tag;merge 後 ArgoCD 自動收斂;`git revert` 即 rollback。RBAC 用 AppProject 切租戶 |
| **真實踩坑** | 開了 automated + prune,有人重構 repo 把 manifests 搬目錄,舊 path 下「消失」的資源被 prune,prod 服務被刪。另一坑: HPA 管 replicas,Git 裡也寫死 replicas,兩個 controller 互相打架,app 永遠 OutOfSync。解法: Git 裡不寫 replicas 或用 `ignoreDifferences` |
| **面試怎麼問** | "Design a GitOps layout for 3 environments and 2 clusters. How do you handle secrets? What is the app-of-apps pattern for? What happens on manual cluster changes?" |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| GitOps | /ˈɡɪt.ɒps/ | Operating a system by storing desired state in Git and letting a controller reconcile toward it | Git 當 desired state,controller 負責收斂 |
| drift detection | /drɪft dɪˈtek.ʃən/ | Continuously diffing live cluster state against the rendered desired state | 持續比對「現場」vs「Git 渲染結果」,不同就標 OutOfSync |
| sync wave | /sɪŋk weɪv/ | An ordering annotation that makes ArgoCD apply resources in healthy-gated batches | 分批上,前一批健康了才上下一批 |

---

## C-3: CRD + Operator Pattern (keystone)

### 核心概念

先切層,這是學員已知弱點(層級混淆)的預防針:

- **CRD (CustomResourceDefinition)**: extends the **API layer**. You teach the API server a
  new object kind: its group, version, and an OpenAPI schema for validation. After that,
  etcd stores it, `kubectl get/apply/watch` work, RBAC applies. **Nothing acts on it yet.**
- **Operator**: extends the **control layer**. A custom controller (usually a Deployment in
  the cluster) that watches your custom resources and runs a domain-specific reconcile loop.

中文點破: CRD=在櫃檯登記一種新表格;operator=雇一個懂這種表格的承辦人。只交表格、
沒雇人,表格就躺在檔案室裡。這正是 P2a「apply Ingress 沒裝 controller 完全沒反應」的
同構事件,學員親手驗證過,直接回扣。

```
CRD applied ──> API server now accepts:   kind: PostgresCluster
                                              |
                                     stored in etcd, watchable
                                              |
              operator Pod  ── watch ────────+
                 |  reconcile: observe CR spec (desired)
                 |             observe StatefulSets/Secrets/backups (actual)
                 +──> create/repair until they match
```

An operator is literally you writing a new row of the student's 對照表: 規則=你的 CR,
引擎=你的 controller。ArgoCD's Application (C-2) is exactly this: a CRD plus a controller.
Point that out *after* he has drawn the operator loop himself.

**Finalizers and two-phase deletion** (名坑,必教):

Deletion in Kubernetes is not immediate. `kubectl delete` sets `metadata.deletionTimestamp`.
If `metadata.finalizers` is non-empty, the object stays in `Terminating` until every
controller responsible for a finalizer completes its cleanup (delete the cloud volume, the
external DNS record...) and removes its entry. Only when the list is empty does the API
server actually delete the object from etcd.

名坑: **namespace stuck in Terminating**. Classic cause: a custom resource inside the
namespace still carries a finalizer, but its operator was already uninstalled. Nobody is
left to remove the finalizer, so the CR never dies, so the namespace never dies. Second
classic cause: an aggregated API service (`kubectl get apiservice`) is unavailable, so the
namespace controller cannot even *list* all resource types to confirm the namespace is empty.

**When to write an operator (engineering judgment, senior 必考)**:

- Yes: the resource needs *operational knowledge* encoded: ordered failover, backup
  schedules, version migrations, re-election. Databases, message brokers, cert rotation.
- No: Deployment + Service + ConfigMap already express it; a Job or a Helm chart covers it;
  you cannot afford to maintain a controller (it is production software: it needs tests,
  RBAC review, upgrade path, on-call ownership).

### 動手觀察 (kind, 純 kubectl,不用寫 code)

```bash
kubectl config current-context
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/application/crontab-crd.yaml
kubectl get crd crontabs.stable.example.com
kubectl api-resources | grep crontab
```

自己寫一個 CronTab CR apply 進去,`kubectl get crontabs` 看到它: API server 全套服務
(storage/watch/RBAC)免費奉送,而且**什麼都不會發生**,因為沒有 controller。

Finalizer lab(打穿 Terminating 名坑):

```bash
kubectl patch crontab my-crontab --type merge -p '{"metadata":{"finalizers":["example.com/never-cleaned"]}}'
kubectl delete crontab my-crontab --wait=false
kubectl get crontab my-crontab -o jsonpath='{.metadata.deletionTimestamp}'
kubectl get crontab my-crontab
kubectl patch crontab my-crontab --type merge -p '{"metadata":{"finalizers":[]}}'
kubectl get crontab my-crontab
```

引導問題: 「deletionTimestamp 有了、物件還在,誰在等誰?」(API server 在等 finalizer
的主人來清理,而主人不存在: 這就是 prod namespace 卡 Terminating 的完整劇本。)

### 打穿底層 (First-Principles Dive)

1. **Generic API machinery**: the API server never hard-coded Pods. Storage, versioning,
   watch, admission all operate on generic objects driven by schemas. CRDs simply feed a
   new schema into machinery that was always generic. That is why you get watch and RBAC
   for free.
2. **Two-phase delete is a distributed-systems answer**: the object in etcd and the real
   things it owns (cloud disks, DNS records) live in *different systems*; you cannot delete
   both atomically. Mark-then-cleanup (tombstone + async GC) is the standard escape, the
   same shape as saga compensation in microservices.

**遷移題**: "Your team uninstalls the cert-manager Helm chart, and remember from C-1 that
Helm never touches `crds/`. What is left in the cluster? Later someone deletes those CRDs
by hand. What happens to the hundreds of Certificate objects?" (CRDs and CRs survived the
uninstall; deleting a CRD **cascade-deletes every CR instance of it**. If any carried
finalizers with no controller alive, they wedge in Terminating first.)

### 誘答彈藥 (keystone 必備)

1. 「刪 CRD 很安全,它只是刪 schema 定義;既有的 custom resource 實例還會留在 etcd,
   等你另外刪。」錯: 刪 CRD 會連坐刪光所有該類型的 CR。生產上這是「解安裝順序」事故的
   根源: 先刪 operator 再刪 CRD 又留 finalizer,三重卡死。
2. 「namespace 卡在 Terminating 表示 API server 還在慢慢刪裡面的 Pod,多等一下就好。」
   錯: 等待不是機制。要看 `kubectl get ns <ns> -o jsonpath='{.status.conditions}'` 指出
   哪種資源刪不掉,追到那個 CR 的 finalizer 與失蹤的 controller。強行清 namespace 的
   finalizer 是最後手段,代價是外部資源(雲碟、DNS)變孤兒。這題同時打學員「先跳結論、
   不講機制」的舊模式: 要求他講完整因果鏈再給處置。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你在 P4 用過 prometheus-operator 的 ServiceMonitor: 那就是 CRD + operator [RUNTIME: 依 P4 實際用過的 CRD 回扣] |
| **生產怎麼做** | 平台層大量站在 operator 上: cert-manager(Certificate)、prometheus-operator、Argo Rollouts(C-8)、Karpenter(NodePool)。自寫 operator 用 kubebuilder/controller-runtime,當正式軟體對待 |
| **真實踩坑** | 下線一個內部 chart 後,它的 namespace 卡 Terminating 三天。追查: chart 的 CR 帶 finalizer,operator Deployment 已被刪。清 finalizer 後 namespace 消失,但雲上留了兩顆沒人記得的 EBS volume,月底帳單才發現 |
| **面試怎麼問** | "What exactly does a CRD give you, and what does it not? Walk me through why a namespace gets stuck in Terminating. When would you write an operator instead of a Helm chart?" |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| CRD | /siː ɑːr diː/ | A schema that registers a new object kind with the API server | 教 API server 認一種新表格,只有 schema 沒有行為 |
| operator | /ˈɒp.ər.eɪ.tər/ | A custom controller encoding operational knowledge as a reconcile loop over custom resources | 自訂 controller 跑自訂 reconcile,把運維知識寫成程式 |
| finalizer | /ˈfaɪ.nəl.aɪ.zər/ | A marker that blocks actual deletion until its owning controller finishes cleanup and removes it | 刪除前的「等我清完外部資源」門閂,主人失蹤就卡 Terminating |

---

## C-4: Admission Webhooks (把 P0 埋的事故正式打穿)

### 核心概念

P0 C-3 學過 API server 三道關卡: authn → authz → **admission**。當時 admission 是黑盒;
現在打開: built-in admission plugins 之外,API server 可以把每個寫入請求**同步外呼**到
你的 HTTP service 徵詢意見。

```
 write request ──> authn ──> authz ──> mutating admission ──> (schema validation) ──> validating admission ──> etcd
                                        |                                              |
                                        v  HTTPS POST (AdmissionReview)                v
                                  your mutating webhook                        your validating webhook
                                  may PATCH the object                         may only say yes/no
```

- **Mutating** runs first and may modify the object (inject a sidecar, add default labels,
  set resource limits). Response carries a JSONPatch.
- **Validating** runs after mutation and may only accept or reject (with a message).
- Both are registered by `MutatingWebhookConfiguration` / `ValidatingWebhookConfiguration`
  objects: which resources/verbs to intercept (`rules`), which namespaces
  (`namespaceSelector`), where to call (a Service reference plus `caBundle`), and
  **`failurePolicy`**: what the API server does when your webhook is unreachable.
  `Ignore` = let the request through. `Fail` = reject the request.

**The classic outage, now formally**: phase-0 的「真實踩坑」埋過這一場,現在收割。
A webhook registered with `failurePolicy: Fail` on `CREATE pods` with no namespace
exclusions, and the webhook's own Deployment goes down (or its cert expires). Result:
**no Pod can be created anywhere in the cluster**, including the webhook's own replacement
Pod, including kube-system. The cluster is not down, but it can no longer change. Deadlock:
the fix (recreate the webhook Pod) is itself blocked by the broken webhook.

Escape path: `kubectl delete validatingwebhookconfiguration <name>`(configuration 物件的
增刪不經過它自己攔的規則),或先把 `failurePolicy` 改 `Ignore`,救回來再修 root cause。

**Cert 管理坑**: API server 只肯用 HTTPS 呼叫 webhook,並拿 configuration 裡的 `caBundle`
驗 server cert。cert 過期或 rotate 後 caBundle 沒更新,症狀完全等同 webhook 掛掉。生產
標配是 cert-manager 的 CA injector 自動同步 caBundle,不要手貼 base64。

### 動手觀察 (直接用 P2a 裝過的 ingress-nginx,它自帶 validating webhook)

```bash
kubectl config current-context
kubectl get validatingwebhookconfigurations
kubectl get validatingwebhookconfiguration ingress-nginx-admission -o jsonpath='{.webhooks[0].failurePolicy}'
kubectl get validatingwebhookconfiguration ingress-nginx-admission -o jsonpath='{.webhooks[0].rules}'
```

回扣 P2a chunk 2 lab: 學員裝 ingress-nginx 時其實就順手裝了一個 admission webhook,
它負責在 apply 階段擋掉語法錯的 Ingress(nginx reload 前就退件)。現在故意 apply 一個
snippet 非法的 Ingress 看它被 webhook 拒絕,錯誤訊息開頭是 `admission webhook ... denied
the request`。E 段接 Drill P5-2 把它弄癱。

### 打穿底層 (First-Principles Dive)

An admission webhook is the interceptor/middleware pattern (same shape as HTTP middleware
chains or DB triggers), with one brutal property: it is **synchronous and in-line**. You
have inserted an availability dependency into *every write* on the control plane. The
availability math is unforgiving: request success now requires `apiserver AND webhook`,
so the webhook's SLO directly caps the API's SLO. `failurePolicy` is exactly the
fail-open vs fail-closed choice from security engineering.

**遷移題**: "Your CI requires a status check from an external license-scanning service.
The service goes down for a day. Map fail-open vs fail-closed onto this, and onto
`failurePolicy`. Which would you choose for each, and why are the answers different?"

### 誘答彈藥

- 「`failurePolicy: Fail` 一定比較安全,寧可建不了 Pod 也不能放沒驗證過的東西進來,
  所以生產全部設 Fail 就對了。」分層拆: for a *security-enforcing* validating webhook,
  fail-closed 確實是對的預設,但代價必須用工程手段付掉: webhook 本體 HA(multi-replica,
  PDB)、`namespaceSelector` 排除 kube-system 和 webhook 自己的 namespace、timeout 調短。
  For convenience mutations(加 label、填 default),fail-closed 是拿全 cluster 可用性
  換低價值功能,該用 Ignore。一句「全設 Fail」正是「先跳結論不講 trade-off」的形狀,
  這是學員的已知舊模式,追問到他講出兩類 webhook 的差別為止。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 平台要求所有 Pod 不得用 `:latest`、必須有 resource limits |
| **生產怎麼做** | 用現成 policy engine(Kyverno / Gatekeeper,底層就是 admission webhook)而不是自寫;policy 先跑 audit/warn 模式一週,看 violation 報表,再轉 enforce |
| **真實踩坑** | 某 mutating webhook 的 cert 半夜過期,`failurePolicy: Fail`,全 cluster 建不了 Pod;HPA scale-out 全數失敗,早高峰直接過載。復盤: cert 沒接 cert-manager、webhook 沒排除 kube-system、沒有 webhook 可用性的 alert(P4 的 SLO 思維用在這裡) |
| **面試怎麼問** | "Mutating vs validating webhooks: order and capabilities? A webhook outage takes down Pod creation cluster-wide: walk me through the blast radius, the escape, and how you would have designed it to prevent this." |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| admission webhook | /ədˈmɪʃ.ən ˈweb.hʊk/ | An HTTP callback the API server consults synchronously before persisting a write | API server 寫 etcd 前的同步外呼關卡,可改可擋 |
| failurePolicy | /ˈfeɪl.jər ˈpɒl.ə.si/ | What the API server does with a request when the webhook is unreachable: Ignore or Fail | webhook 掛掉時放行還是全擋,fail-open vs fail-closed |

---

## C-5: Cluster Upgrade Strategy (senior 必考)

### 核心概念

Upgrading a cluster means replacing the platform underneath running workloads. The rules
that make this survivable:

**Version skew policy** (official numbers, worth memorizing):

- `kube-apiserver`: in an HA cluster, members may differ by at most **1 minor**.
- `kubelet`: may be up to **3 minors older** than kube-apiserver (2 before v1.28), and
  **never newer**. `kube-proxy` follows the same rule as kubelet.
- `kube-controller-manager` / `kube-scheduler`: not newer than apiserver, at most 1 older.
- `kubectl`: within one minor of the apiserver, either direction.

**升級順序由 skew policy 直接推出**(讓學員自己推,別直接給): everything is allowed to
be *older* than the API server but nothing may be *newer*. Therefore **control plane first,
nodes after**, and the control plane moves **one minor at a time** (because etcd/apiserver
HA members tolerate only 1 minor of spread, and API storage versions migrate per release).

**Node rollout**: for each node: `kubectl cordon` (stop new scheduling, P0 drill 做過)
then `kubectl drain --ignore-daemonsets` (evict Pods, **respecting PodDisruptionBudgets**),
upgrade or replace the node, uncordon. 回扣 P3 PDB: drain 就是 PDB 存在的理由,單副本
又掛 `maxUnavailable: 0` 的 PDB 會讓 drain 永遠卡住。[RUNTIME: 回放學員 P3 PDB lab 的
實際場景與他當時的用詞。]

**EKS 的版本**:

- Control plane upgrade is one API call, AWS rolls it for you, **and it is irreversible**:
  there is no downgrade. 這句要原文背: you cannot roll back a control plane upgrade.
  所以先升非 prod cluster,泡 soak time,再動 prod。
- Managed node groups: rolling update launches new nodes on the new AMI, cordons and drains
  old ones honoring PDBs (with a force option that stops honoring them), `maxUnavailable`
  tunable.
- **Addon compatibility**: vpc-cni, coredns, kube-proxy addons each have per-k8s-version
  compatibility ranges. Upgrading the control plane without checking addons is the top EKS
  upgrade incident source.
- Standard support per minor is 14 months; after that, extended support bills roughly 6x
  per cluster-hour. Fleets that never upgrade literally cost more.

**Blue-green cluster vs in-place 取捨**:

| | In-place upgrade | Blue-green (new cluster, shift traffic) |
|---|---|---|
| Cost | one cluster | double infra during migration |
| Rollback | control plane: none; nodes: partial | shift traffic back, real rollback |
| Risk shape | shared fate, one big change | migration complexity: state, DNS, IAM, stateful data |
| Fits | frequent small upgrades, mature PDB/probe hygiene | multi-minor jumps, low confidence, hard compliance windows |

GitOps 複利點: blue-green cluster 之所以在 GitOps 下變便宜,是因為 C-2 的 app-of-apps
可以把整個平台指到新 cluster 一鍵重生。這是「cluster 是牛不是寵物」的兌現。

### 動手觀察 (kind 不能原地升版,演練 drain 環節)

```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl create deployment upgrade-demo --image=nginx --replicas=2
kubectl create poddisruptionbudget upgrade-demo-pdb --selector=app=upgrade-demo --min-available=2
kubectl drain k8s-coach-p0-worker --ignore-daemonsets --delete-emptydir-data --timeout=60s
```

預期: drain 卡住,eviction 被 PDB 拒絕(`Cannot evict pod as it would violate the pod's
disruption budget`)。引導問題: 「這是 bug 還是 feature?誰在保護誰?」然後把 PDB 改成
`--min-available=1` 重跑,看 drain 過。結束 `kubectl uncordon` + 清理。

### 打穿底層 (First-Principles Dive)

Why does skew tolerance exist at all? Because the API is **versioned and negotiated**:
kubelet speaks to the apiserver through stable REST APIs, and objects in etcd carry
storage versions migrated release by release. Skew policy is an API compatibility
contract, the same discipline as rolling out a backward-compatible microservice API
(server upgrades first, clients lag). 這也是為什麼「node 比 control plane 新」被禁止:
client assuming features the server lacks breaks in undefined ways.

**遷移題**: "Your fleet runs kubelet 1.29 against an EKS 1.31 control plane, allowed by
skew. You now upgrade the control plane to 1.32. Is the fleet still compliant? Write the
ordering constraint as an inequality and derive the answer." (1.32 - 1.29 = 3, still legal
post-1.28, but you are at the edge: nodes must catch up before the *next* control plane
minor. 訓練他用規則推,不背案例。)

### 誘答彈藥 (輕量)

- 「既然 kubelet 容許落後 3 個 minor,那 control plane 可以直接從 1.28 跳 1.31,一次
  升三版最省事,node 反正在容許範圍內。」錯: skew 管的是 kubelet 對 apiserver 的
  *並存*,不解除 control plane 本身「一次一個 minor」的限制(HA apiserver 間 1 minor、
  etcd schema 與 API storage version 逐版遷移,EKS 也直接不讓你跳)。層級混淆的變形題:
  「並存容忍」和「升級步長」是兩條不同的規則。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你們的 billing prod EKS 停在即將 EOL 的版本,要規劃季度升級 |
| **生產怎麼做** | Runbook: 讀 release notes 找 API removals(`kubectl api-resources` + pluto/kubent 掃 deprecated API)→ 升 dev cluster → soak → 升 prod control plane → 升 addons(vpc-cni/coredns/kube-proxy 對相容表)→ managed node group 滾動 → 驗收 dashboard(P4)。全程 PDB 和 readiness probe(P1)是安全網 |
| **真實踩坑** | 升完 control plane 忘了 vpc-cni addon,新 node 起來 NotReady,Pod 卡 ContainerCreating(CNI 配不出 IP,回扣 P2a: CNI 管 Pod 拿真實 IP)。另一坑: 某 workload 單副本 + `minAvailable: 1` 的 PDB,node group 滾動卡死 6 小時 |
| **面試怎麼問** | "Walk me through upgrading a production EKS cluster by two minor versions. Order, blast radius, rollback story, and what version skew policy allows you to defer." |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| version skew policy | /ˈvɜː.ʃən skjuː ˈpɒl.ə.si/ | The supported version differences between control plane and node components | 誰可以比誰舊幾版的官方契約,升級順序由它推出 |
| drain | /dreɪn/ | Evicting all evictable Pods from a node, honoring PodDisruptionBudgets | 清空 node 上的 Pod,PDB 是它的煞車 |

---

## C-6: etcd Operations (keystone, P0 C-4 的還債點)

> P0 C-4 只給了 Raft 直覺(leader、quorum、多數決),progress.md 記過「etcd Raft 深入
> park 到 P5」。這裡還債: 先把 Raft 真正打穿,再做 snapshot/restore 演練。
> 順手釘一次 P0 的口誤補正: **只有 API server 直接讀寫 etcd**,其他元件全部透過
> API server 的 watch/update。備份 etcd = 備份整個 cluster 的唯一事實。

### 核心原理: Raft, properly this time

**Term (任期)**: a logical clock. Each election starts a new term; a term has at most one
leader. Every message carries the sender's term; a node seeing a higher term immediately
steps down to follower. Terms are how stale leaders discover they are stale.

**Leader election**: followers expect periodic heartbeats (AppendEntries) from the leader.
If a follower's randomized election timeout expires with no heartbeat, it increments the
term, becomes a candidate, votes for itself, and sends RequestVote to all peers. A node
grants at most **one vote per term**, and only to candidates whose log is at least as
up-to-date as its own. A candidate with votes from a **majority** becomes leader.
Randomized timeouts are the whole trick against split votes: 誰先醒誰先選,同時醒就流局
重來,遲早錯開。

**Log replication**: clients write to the leader only. The leader appends the entry to its
log, ships it via AppendEntries to followers, and **commits the entry once a majority has
persisted it**, then applies it to the state machine and answers the client. Followers
apply entries once the leader advertises the new commit index.

**Why must writes cross a majority?** Because any two majorities of the same cluster
**overlap in at least one node**. A future leader needs majority votes; the vote rule
rejects candidates with stale logs; the overlap node forces every possible new leader to
already hold every committed entry. Split brain is arithmetically impossible: two
concurrent leaders in one term would need two disjoint majorities. 中文點破: 「過半」
不是民主儀式,是讓任何兩個決策集合必然共享至少一個見證人。

```
 5 nodes, write W:
   leader ──AppendEntries──> f1 ✓   f2 ✓   f3 ✗(slow)   f4 ✗(dead)
   acks = leader+f1+f2 = 3 >= majority(3)  => W committed, client told "ok"
   any future election: winner needs 3 votes; every 3-node set contains f1, f2, or leader
   => W survives any legal leader change
```

**遷移題 (Raft)**: "In a 5-node cluster, a write is committed with acks from nodes
{L, A, B}. Immediately, L and A crash. Can the cluster elect a leader, and is the write
safe? Walk through the vote." (3 alive = majority; B holds W and the up-to-date-log rule
means C or D cannot beat B... 逼他發現只有 log 含 W 的節點能當選。)

### 運維面: snapshot / restore / quorum loss

**Snapshot save (kind 可直接做)**:

```bash
kubectl config current-context
docker exec k8s-coach-p0-control-plane etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /tmp/etcd-snap.db
docker exec k8s-coach-p0-control-plane etcdutl snapshot status /tmp/etcd-snap.db --write-out=table
```

**Restore 演練(時間旅行實驗,D 段主秀)**:

1. Snapshot 之後,故意建一個 marker: `kubectl create deployment after-snap --image=nginx`。
2. 停掉 etcd(static pod,P0 drill 的老朋友): 進 control-plane 容器
   `mv /etc/kubernetes/manifests/etcd.yaml /tmp/`,幾秒後 kubectl 全面失靈(親身體感:
   API server 沒有 etcd 就是一台失憶的櫃檯)。
3. Restore 到新資料目錄(flags 照抄 `/tmp/etcd.yaml` 裡的 name/initial-cluster):
   `etcdutl snapshot restore /tmp/etcd-snap.db --data-dir /var/lib/etcd-restored --name <node-name> --initial-cluster <name>=https://127.0.0.1:2380 --initial-advertise-peer-urls https://127.0.0.1:2380`
4. 把舊資料目錄移開、restored 目錄放回 `/var/lib/etcd`(或改 manifest 的 hostPath),
   `mv /tmp/etcd.yaml /etc/kubernetes/manifests/` 讓 kubelet 重拉 etcd。
5. 驗收: `kubectl get deployment after-snap` 應該 **NotFound**。整個 cluster 回到快照
   時刻。引導問題: 「哪些東西沒有回滾?」(node 上還在跑的 container、雲上資源: etcd
   只是事實記錄,不是世界本身。kubelet 的 reconcile 會把孤兒容器對齊回快照裡的 desired。)

**Quorum 損失恢復劇本(背下來,面試與真實事故同一份)**:

- Lost minority (1 of 3): cluster fine. Replace the member: `member remove` **first**,
  then `member add`, then start the new node. 順序有理由,見誘答 1。
- Lost majority (2 of 3): **no writes, no elections; the cluster is frozen, not merely
  degraded.** Reads may still serve stale data. Recovery is *disaster recovery*: restore
  the latest snapshot into a brand-new single-member cluster (`etcdutl snapshot restore`,
  or `--force-new-cluster` on a surviving member's data), then grow it back to 3. You
  accept data loss back to the snapshot point. This is why snapshot cadence is an SLO
  decision, not a chore. (P4 複利: RPO 就掛在 cron 間隔上。)

### 誘答彈藥 (keystone 必備)

1. 「5 節點掛了 2 台。為了安全,先趕快 `member add` 兩台新的補滿,再慢慢移除死掉的。」
   錯: membership 變更立即改變 quorum 分母。5 存 3,quorum=3,剛好活著;先 add 變 6 席,
   quorum=4,而新成員若起不來,你就在只有 3 票的情況下需要 4 票: 自己把自己推下懸崖。
   正確順序永遠是 **remove dead first, then add**。這是「聽起來更穩,數學上更危險」的
   標準誘答,打學員「覺得怪怪的但被帶走」的職場軟肋。
2. 「leader 把 entry 寫進自己的 log 就可以回覆 client 成功了,replication 給 follower
   是背景非同步做的,這樣延遲最低。」錯: committed 的定義就是「多數已持久化」。若 leader
   單獨確認後立刻斷電,新 leader 完全可能沒有這筆資料,「成功」的寫入蒸發。多數決不是
   效能取捨,是正確性的定義。(接 P0 quorum 直覺,現在他要能用 overlap 論證講完整。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 自建或混合環境的 etcd 運維(EKS 幫你管,但面試官不管你用 EKS) |
| **生產怎麼做** | Snapshot 每 4-6 小時 cron + 異地存放 + **定期演練 restore**(沒演練過的備份等於沒有);監控 `etcd_disk_wal_fsync_duration_seconds`(P0 踩過: disk latency 導致 leader 抖動)與 db size |
| **真實踩坑** | etcd db 超過 quota(預設 2GiB)觸發 NOSPACE alarm,全 cluster 進入唯讀,任何寫入報 `etcdserver: mvcc: database space exceeded`。解法: compact 舊 revision → defrag 每個成員 → `etcdctl alarm disarm`。根因常是某 controller 高頻更新同一物件把 revision 灌爆 |
| **面試怎麼問** | "You lose 2 of 3 etcd members. What still works, what does not, and exactly how do you recover? Why do writes require a majority: prove it, don't recite it." |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| term | /tɜːrm/ | Raft's logical clock; each term has at most one leader | 任期編號,讓過氣 leader 自己發現自己過氣 |
| log replication | /lɒɡ ˌrep.lɪˈkeɪ.ʃən/ | The leader ships log entries to followers and commits once a majority persists them | 寫入先進 leader 日誌,過半落盤才算數 |
| committed entry | /kəˈmɪt.ɪd ˈen.tri/ | A log entry persisted by a majority, guaranteed to survive any legal leader change | 已被多數見證的寫入,任何合法新 leader 都必然帶著它 |

---

## C-7: EKS Production Terraform (cluster 本身也要可重生)

### 核心概念

GitOps (C-2) answers "what runs *in* the cluster". Terraform answers "where did the
cluster itself come from". A production platform needs both, with a clean boundary:

- **Terraform**: VPC, EKS control plane, node groups / Karpenter, IAM/IRSA, and the
  bootstrap of ArgoCD itself.
- **ArgoCD**: everything above that line, driven by app-of-apps.

規則: 一個東西只能有一個 reconcile 主人。同一個資源被 TF 和 Argo 同時管,就是兩個
desired state 打架(C-2 真實踩坑 HPA vs Git 的同構放大版)。

**模組分層** (repo 骨架,學員親手建):

```
terraform-eks/
  modules/
    vpc/          # subnets, NAT, tags for LB discovery
    eks/          # control plane, OIDC provider, addons (vpc-cni/coredns/kube-proxy)
    nodegroup/    # managed node groups; or karpenter/ (NodePool + EC2NodeClass as IaC)
    irsa/         # per-app IAM roles bound to service accounts
  envs/
    dev/          # backend "s3" + terraform.tfvars, cluster name billing-dev-eks-lab
```

**State management**: state 是 Terraform 的「etcd」: 它對世界的唯一記憶。Remote backend
(S3 + state lock),per-env 隔離的 state file,絕不 commit 進 Git,絕不兩人同時 apply
(lock 的存在理由)。Plan on PR, apply on merge: TF 的變更也走 GitOps 精神,只是引擎是
CI 觸發的 one-shot,不是常駐 loop。

**Karpenter provisioner IaC 化**: NodePool/EC2NodeClass 是 CRD(C-3 複利: Karpenter 就是
一個 operator,規則=NodePool、引擎=Karpenter controller,學員 P2b 已推過 provisioner
模式)。它們的 YAML 進 Git 由 ArgoCD 管,Karpenter 本體與它的 IAM 由 Terraform 管:
恰好示範了那條邊界怎麼切。

[RUNTIME: 依學員公司 IaC 現況客製: 公司是否已有 Terraform、模組怎麼拆、state 放哪、
有沒有 Atlantis/CI pipeline。用他公司的真實結構當對照組來教,差異點就是討論題。]

### 動手 (EKS 選配 lab,契約規則: 指令只產生,學員親手跑)

規格(YAML/HCL 學員自己寫,教練給規格): 上面骨架的最小可行版,cluster 名
`billing-dev-eks-lab`,所有資源名前綴 `billing-dev-eks-*`,單一 managed node group,
2 台 t3.medium。學員親手: `terraform init` → `plan`(要求他先口頭預測 plan 會列出幾類
資源,再看)→ `apply` → `aws eks update-kubeconfig` 後 `kubectl get nodes`(此刻
current-context 是 EKS,提醒: 做完立刻切回)。

**必附的收尾(契約硬規定)**:

```bash
terraform destroy
aws eks list-clusters --query "clusters[?contains(@,'billing-dev-eks')]"
aws ec2 describe-instances --filters Name=tag:Name,Values=billing-dev-eks-* --query 'Reservations[].Instances[].State.Name'
kubectl config use-context kind-k8s-coach-p0
kubectl config current-context
```

### 打穿底層 (First-Principles Dive)

**Why does Terraform need a state file when kubectl does not?** Kubernetes has a server
holding desired state (etcd via API server) and controllers that diff continuously.
Terraform has no server: the cloud APIs it drives do not record "which tool owns this
resource", so TF must keep its own ledger mapping code to real resource IDs. Plan = diff
(code vs state vs refreshed reality), apply = one-shot converge. TF 是 edge-triggered 的
reconcile: 沒有人跑 plan,drift 就永遠潛伏。(C-2 遷移題在這裡收口。)

**遷移題**: "terraform destroy 卡住: VPC 刪不掉,報 dependency violation,殘留一堆 ENI
和一顆 ELB。但你的 .tf 裡根本沒寫 ENI 和 ELB,它們哪來的?" (它們是 cluster 裡的
controller 生的: vpc-cni 配的 ENI、Ingress/type:LoadBalancer 的 provisioner 生的 LB。
回扣 P2b: controller 在雲上創建的資源,Terraform 的 state 完全看不見。正確順序: 先刪
cluster 內會生雲資源的物件,等 controller 收斂完,再 destroy。)

### 誘答彈藥 (輕量)

- 「Terraform 也是 declarative,所以跟 ArgoCD 一樣,雲上有 drift 它會自動修回來。」
  錯: declarative 只保證「描述的是終態」,不保證「有人持續在收斂」。TF 的收斂只發生在
  有人跑 apply 的那一刻。Declarative 是語言性質,reconcile loop 是執行架構,兩層分開:
  又一題層級混淆疫苗。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 公司要能在新 region 兩天內重生整套平台(DR 演練要求) |
| **生產怎麼做** | Terraform 建 cluster + bootstrap ArgoCD,ArgoCD app-of-apps 拉起全部平台與應用: 兩層合起來,cluster 是可重印的,C-5 的 blue-green cluster 策略因此可行 |
| **真實踩坑** | CI 半路被砍,state lock 沒釋放,之後所有 plan 報 `Error acquiring the state lock`。解法: 確認沒有 apply 真的在跑,`terraform force-unlock <lock-id>`。粗暴刪 lock 而有人正在 apply = state 損毀,那是比事故更大的事故 |
| **面試怎麼問** | "Where do you draw the line between Terraform and GitOps? Why does Terraform need remote state and locking? How do you destroy a cluster cleanly when controllers created cloud resources behind Terraform's back?" |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| IRSA | /ˈɜːr.sə/ | IAM Roles for Service Accounts: binding an AWS IAM role to a Kubernetes service account via OIDC | 讓 Pod 拿自己的 IAM 角色,不共用 node 的大鑰匙 |
| state lock | /steɪt lɒk/ | A mutex preventing concurrent Terraform operations from corrupting the state file | 防止兩個 apply 同時改帳本把帳本撕爛 |

---

## C-8: Progressive Delivery (組裝 gate 的最後一塊)

### 核心概念

Everything so far gets the commit *to* production automatically. Progressive delivery
makes it **prove itself** before taking all the traffic.

**Argo Rollouts**: a Rollout CRD that replaces Deployment (C-3 複利: 這就是一個 operator,
規則=Rollout spec,引擎=rollouts controller;學員此刻應該能秒答「誰在執行」).

- **Canary**: steps of `setWeight` + `pause`, e.g. 10% → analyze → 50% → analyze → 100%.
  Without a mesh or traffic-shaping ingress, weight is approximated by pod count ratio;
  with ingress-nginx (P2a) or a mesh, it is real traffic percentage.
- **Blue-green**: `activeService` points at the old ReplicaSet, `previewService` at the
  new; promotion is a Service selector flip. Instant cutover, instant flip-back, double
  capacity while both run.
- **AnalysisTemplate**: the judge. A metric query (typically Prometheus) plus a success
  condition, run automatically between steps. Fail => automatic rollback (abort), no human
  in the loop.

**P4 複利(這一段是 SLO 的兌現)**: AnalysisTemplate 的 query 不該現場發明,直接用 P4
定義過的 SLI: error rate、p99 latency。Canary 健康的定義 = 「新版本沒有燒 error budget」。
[RUNTIME: 把 P4 學員實際建的 SLI/PromQL 原樣搬進 AnalysisTemplate,讓他認出自己的作品。]

**全景組裝圖(Phase Gate 的白板題,先在這裡建立)**:

```
 dev ── git push ──> CI: test + build image + push registry
                          |
                          v  bump image tag in env repo (PR -> review -> merge)
                     Git repo (desired state)                     ← C-2
                          |
                          v  ArgoCD detects, syncs (waves order the rollout objects)
                     Rollout controller starts canary             ← C-3/C-8
                          |
              10% traffic ──> AnalysisRun queries Prometheus      ← P4 SLO
                 |  pass                     |  fail
                 v                           v
             50% ... 100%             auto abort => old version
                          |
                     fully promoted; admission webhooks guarded every apply  ← C-4
                     the platform under it: upgradable (C-5), restorable (C-6),
                     reprintable (C-7)
```

One commit, automatically and safely to production. 這張圖 = P5 gate 本體。

### 動手觀察

```bash
kubectl config current-context
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl get crd rollouts.argoproj.io
```

學員自己寫一個最小 Rollout(給規格: 2 replicas,canary steps: setWeight 50 → pause 無限)
+ 對應 Service。apply 後改 image tag 觸發 rollout,觀察:

```bash
kubectl argo rollouts get rollout demo-rollout --watch
kubectl argo rollouts promote demo-rollout
```

看到「stuck at 50%, waiting for promotion」的瞬間,他就理解 pause 是人肉 analysis;
接著討論把人換成 AnalysisTemplate 的條件。(kind 上接 Prometheus 做完整 analysis 屬
stretch,依 P4 環境是否還在。)

### 打穿底層 (First-Principles Dive)

Progressive delivery is statistical risk control: a deploy is a hypothesis ("new version
is at least as good"), canary traffic is the sample, the analysis metric is the test.
Sample size matters: 10% of tiny traffic for 60 seconds may not surface a 1% error-rate
regression; too long, and you double resource cost and slow every release. 這與 P1
rollout 的 maxSurge/maxUnavailable 是同一類 trade-off,只是維度從「副本數」升級到
「流量 + 統計信心」。

**遷移題**: "P1 的 rolling update 也有 readiness probe 守門,為什麼還需要 canary +
analysis?" (Readiness answers "can this Pod serve *at all*"; analysis answers "is the new
version *as good as* the old under real traffic": 錯誤率上升 3 倍但仍 200 OK 的版本,
readiness 完全放行。兩道閘門在不同層。)

### 誘答彈藥 (輕量)

- 「Blue-green 比 canary 安全,因為可以瞬間切回舊版,所以風險是零。」錯: 切回的是
  *流量*,不是 *世界狀態*。新版本若已寫入不相容的資料(DB migration、cache 格式),
  flip back 之後舊版面對的是被污染的狀態;而且 100% 流量瞬間打到新版,沒有小樣本
  試錯,爆就是全爆。Canary 換的是「慢一點,但爆炸半徑小」。要他講出 state 這一層。

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你們的 billing 服務要在月結高峰期間也能安全發版 |
| **生產怎麼做** | Rollout canary 接 ingress-nginx traffic shaping,AnalysisTemplate 掛 P4 的 error-rate/latency SLI,失敗自動 abort + Slack 通知;月結凍結窗用 ArgoCD sync window 實作 |
| **真實踩坑** | AnalysisRun 一直 Inconclusive: Prometheus 在 canary 期間剛好被重啟,query 回空值。Rollout 停在中途不 promote 也不 abort,半夜 page。修法: 給 metric 設 `failureLimit`/`inconclusiveLimit` 與明確的空值語意,並把「判官本身的可用性」納入監控(C-4 webhook 的教訓同構: 判官也是依賴) |
| **面試怎麼問** | "Canary vs blue-green: tradeoffs, and when is each wrong? How do you make canary judgment automatic and what can go wrong with the judge itself?" |

### 術語卡

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| progressive delivery | /prəˈɡres.ɪv dɪˈlɪv.ər.i/ | Releasing gradually with automated, metric-based judgment gating each step | 小樣本試錯 + 指標自動判官,一步一關往前推 |
| analysis template | /əˈnæl.ə.sɪs ˈtem.plət/ | A reusable metric query plus success criteria that judges a rollout step | 把「canary 健不健康」寫成可執行的 SLO 判斷式 |

---

## Chaos Drill Hooks (P5)

> 完整劇本在 `references/chaos-drills.md`(P5 段)。這裡只留鉤子與時機。

- **Drill P5-1: ArgoCD OutOfSync 疑雲**(接 C-2 之後): 教練暗中 kubectl edit 某資源 +
  調整 syncPolicy,學員限時判讀: OutOfSync 是誰造成、selfHeal 會不會修、prune 開著會
  刪掉什麼。考點: sync vs health 兩軸、drift 的方向感。
- **Drill P5-2: Webhook 癱瘓,全 cluster 建不了 Pod**(接 C-4 之後): 把 ingress-nginx
  admission webhook 的 backing service 弄壞 + `failurePolicy: Fail`,學員限時從
  `admission webhook denied/timeout` 的報錯追到 configuration,執行逃生路徑。這是
  phase-0 埋的事故正式引爆。
- **Drill P5-3: Helm 升級出包,限時回滾**(接 C-1 之後): 灌一個帶壞 image + pre-upgrade
  hook 的 chart 升級,release 卡 pending-upgrade,學員限時用 `helm history`/`rollback`
  救回並解釋 atomic 為什麼救不了 hook 的副作用。

[RUNTIME: 依 mistake-registry,把學員 P5 期間答錯過的誘答改編成第四個突襲 drill。]

---

## P5 畢業 Gate

**考核格式**(全英文作答,P5 檔位): 白板 + 口述,三段連考。

1. **The pipeline**: draw and narrate the full path from `git push` to "safely serving
   prod", naming *every* reconcile loop involved (CI 除外至少四個: ArgoCD app controller、
   Rollout controller、ReplicaSet controller、kubelet;加分: Karpenter、cloud LB
   provisioner)。必答: 有人 kubectl edit prod 會發生什麼、由哪個設定決定。
2. **The judge and the guard**: explain how a canary is judged automatically (metric,
   source, failure semantics) and what happens cluster-wide when an admission webhook with
   `failurePolicy: Fail` dies, including the escape path.
3. **The bedrock**: 3-node etcd loses two members. What works, what does not, and recover
   it: narrate the snapshot/restore commands from memory (骨架即可,flags 可略), and prove
   with the majority-overlap argument why writes need quorum.

**Pass 條件**:

- 三段都能不看筆記講完,且「規則 vs 引擎」對照表能自己默寫到至少五列。
- kubectl edit drift 的答案分層(偵測 vs 修復、selfHeal 的角色),不是一句「會被改回去」。
- etcd 段的 quorum 論證用 overlap 講,不是背「多數決比較安全」。
- 至少抓出教練現場埋的兩題誘答之一(誘答從本檔各 chunk 題庫抽換皮)。
  [RUNTIME: 誘答選 mistake-registry 裡他曾中招的方向做冷測。]

**Stretch(加分,不強求)**:

- 5-node etcd 選舉全程推演(term、vote 規則、為什麼含 committed entry 的節點必當選)。
- 設計 app-of-apps + ApplicationSet 的多 cluster 佈局,並講 blue-green cluster 升級怎麼
  騎在這個佈局上。

**Gate 失敗處理**: 見 SKILL.md Phase Gate Failure 協議。常見弱點預測: pipeline 盲講漏
中間棒次(他 Weekly Review #1 的已知模式,提醒他用「數棒子」骨架: Git→Argo→Rollout→RS→
kubelet 默數到五)、etcd 論證退化成背誦。對症重練 C-2 / C-6。

---

## Portfolio 整合 (P5 = 主秀階段)

`gitops/` 與 `terraform-eks/` 是整個 portfolio 的主秀資料夾,P3 Weekly Review 時就預告過
「showcase 主秀待 P3+ 長出」,在這裡收割。過價值門檻才進 repo,教學廢料留本機。

- `portfolio/gitops/`: app-of-apps root + 子 Application 結構(哪怕只有兩個 app,結構
  要對)、一個帶 canary steps + AnalysisTemplate 的 Rollout、以及一篇 drift 事件的
  mini postmortem(P5-1 drill 的產出,含 timeline 與 root cause,面試直接可講)。
- `portfolio/terraform-eks/`: modules/envs 骨架 + README,README 必含: 架構圖、
  TF/ArgoCD 邊界的一段說明、以及 destroy 驗證的指令輸出證明(展示成本紀律,面試官
  對這個細節的評價高於多寫三個 module)。
- `portfolio/notes/p5-etcd-restore.md`: restore 演練的實錄(指令 + 「時間旅行」驗證
  結果 + quorum 恢復劇本)。這是 senior 面試的高頻彈藥,值得成文。

---

## P5 英文 Ramp

P5 檔位 = 主教材大量英文,本檔正文即閱讀材料。執行方式:

- **Read-aloud + teach-back in English**: 每個 chunk 挑一段官方文件語感的段落(建議:
  C-2 的 "Git holds the desired state..."、C-6 的 "Why must writes cross a majority")
  朗讀後用自己的英文重講,教練給 English Polish。
- **Say-it-in-English 必考句**(gate 前要能脫口而出):
  - "ArgoCD is just another reconcile loop; the desired state happens to live in Git."
  - "A CRD extends the API; an operator extends the control loop. Schema without a
    controller does nothing."
  - "failurePolicy is a fail-open versus fail-closed decision on every API write."
  - "A write is committed only once a majority has persisted it, because any two
    majorities overlap."
- **術語卡總結**(同步進 `workspaces/k8s/term-registry.md` 做間隔抽考):

| 主題 | 術語 |
|------|------|
| C-1 Helm | release |
| C-2 GitOps | GitOps, drift detection, sync wave |
| C-3 CRD/Operator | CRD, operator, finalizer |
| C-4 Webhook | admission webhook, failurePolicy |
| C-5 Upgrade | version skew policy, drain |
| C-6 etcd | term, log replication, committed entry |
| C-7 Terraform | IRSA, state lock |
| C-8 Delivery | progressive delivery, analysis template |

共 17 個術語。P6 mock 全英文,P5 是最後一個可以「中文兜底」的階段,教練把兜底次數
當成 P6 readiness 的觀測指標。
