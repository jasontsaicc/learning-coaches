# P4 可觀測性工程: Metrics, SLOs, and Tracing

> **如何使用此檔:** 這是 P4 階段的教學素材庫,供 coach 在 C 段(核心原理)讀取並改編。
> 不要逐字唸稿,依學員反應選擇要深挖哪個切面。
> 每個 chunk 對應一個 Simon Method 的原子單位,通過 Feynman Gate 後再往下走。
> 英文檔位:半英半中。核心原理段落以英文為主,中文做點破與過渡。學員用英文覆述時給 English Polish。
> 客製基準:學員已在 session 6 被預告過「治本要靠 Prometheus 看水位」;P1 的 OOM/probe lab 和 P2a 的 conntrack 都是本 phase 的現成素材,能回扣就回扣。
> `[RUNTIME: ...]` 標記處依 mistake-registry 與學員當下狀態現場客製。

---

## P4 學習藍圖

**目標**: 從「會看 kubectl top 和 logs」升級到「能設計一套讓自己在事故中 5 分鐘內定位問題的觀測系統」,並能在 senior 面試講清楚 SLO 與 error budget 的取捨邏輯。

**P4 中心問題**: 系統出事時,你怎麼在 5 分鐘內知道「哪裡壞、多嚴重、影響誰」?

這三個子問題正好對應本 phase 的三大支柱:

- 哪裡壞 → metrics 縮小範圍 + trace 定位到 span(C-2/C-3/C-5)
- 多嚴重 → SLO 與 error budget 燃燒速度(C-4)
- 影響誰 → user-facing SLI,而不是 CPU 使用率(C-1/C-4)

**學習路徑(Simon 切塊)**:

| Chunk | 主題 | 核心問題 | Keystone |
|-------|------|---------|----------|
| C-1 | 三種訊號的本質 | metrics/logs/traces 各自回答什麼問題?成本差在哪? | |
| C-2 | Prometheus 架構 | 為什麼 pull?Prometheus 怎麼「自動」找到 Pod? | ✅ |
| C-3 | PromQL 與資料模型 | counter 重啟歸零為什麼沒關係?p99 是怎麼算出來的? | ✅ |
| C-4 | SLI/SLO/Error Budget | 為什麼不追 100%?error budget 是什麼貨幣? | ✅ |
| C-5 | OpenTelemetry 與 tracing | 一個 request 跨 5 個服務,因果鏈怎麼串起來? | |
| C-6 | 告警工程 | 為什麼告警越多反而越危險? | |

**環境前置**: `bash scripts/lab-cluster.sh up p0` 起 3 節點 kind。每個 lab 開頭先跑 `kubectl config current-context`,確認是 `kind-k8s-coach-p0` 才准 apply(機器上有公司 PROD EKS kubeconfig,鐵律不變)。

---

## C-1: 三種訊號的本質差異 (Metrics / Logs / Traces)

### 核心概念

Three signal types answer three different questions:

- **Metrics**: "How is the system doing, as a number over time?" Pre-aggregated counters and gauges, sampled at intervals. You lose individual events but keep the shape of the system.
- **Logs**: "What exactly happened in this one event?" Full detail per event, nothing aggregated. You keep everything and pay for everything.
- **Traces**: "Where did this one request spend its time, across services?" A causal chain of timed operations, stitched together by a shared trace ID.

中文點破:metrics 是「儀表板上的指針」,logs 是「行車記錄器的完整錄影」,traces 是「一件包裹的物流追蹤條碼」。你不會用錄影帶去看時速,也不會用時速表去查某一次擦撞的細節。

### 成本模型 (這才是選型的第一性原理)

The real difference is not "which is better", it's what each one costs as the system scales:

- **Metrics are cheap because they aggregate.** 1 request or 1 million requests: `http_requests_total` is still one time series, a few bytes per scrape. Cost scales with the number of *series*, not the number of *events*.
- **Logs are expensive because they don't.** Cost scales linearly with traffic. Double the requests, double the log volume, double the storage bill. 這就是為什麼生產環境的 log 都要談 retention 和 sampling。
- **Traces sit in between.** Per-request detail like logs, but you sample (keep 1% or only the slow/error ones), so cost is tunable. Their unique value: causality across service boundaries, which neither metrics nor logs give you.

**高基數(cardinality)是三者的分水嶺**: the moment you want per-user, per-request, per-order detail, you have left metrics territory. Metrics aggregate over labels; if a label has a million possible values, you get a million series and the cheap tool becomes the expensive one. Per-entity questions belong to logs and traces. 這條線記住了,C-2 的生產翻車坑就只是它的具體案例。

回扣學員歷史:session 6 他自己分出「leak 鋸齒爬頂 vs rightsize 平台水位」兩種 memory 曲線,那就是 metrics 的用法(看形狀、看趨勢);而當時要查「是哪個 request 把記憶體吃爆」就得下到 logs/heap dump,metrics 給不了。當時教練說「工具是 kubectl top / Prometheus,P4 見」,本 chunk 就是兌現。

### 打穿底層 (First-Principles Dive)

Why can't one signal do it all? Because of an information-theory tradeoff: **you cannot keep full per-event detail and pay aggregate prices.** Every observability system picks a point on the curve: metrics throw away identity to keep cost flat; logs keep identity and pay linear cost; traces keep identity for a *sample* of events. Vendors selling "one tool for everything" are selling three storage engines in one bill.

**遷移題**: 你的手機帳單有「本月總通話分鐘數」(metrics)、「通話明細清單」(logs)。如果電信商要查「為什麼你打給客服的那通電話轉接了 4 次、每段等多久」,那是哪種訊號?為什麼前兩者都答不了這題?

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 公司要導入 observability,老闆問「我們已經有 CloudWatch Logs 了,為什麼還要裝 Prometheus?」 |
| **生產怎麼做** | 分層:metrics(Prometheus/CloudWatch Metrics)做告警和 dashboard,logs(CloudWatch Logs/Loki)做事後鑑識,traces(X-Ray/Jaeger/Tempo)做跨服務延遲歸因。告警永遠掛在 metrics 上,因為便宜、快、可聚合 |
| **真實踩坑** | 團隊把告警建在 log 掃描上(CloudWatch Logs metric filter 掃 "ERROR" 字串),流量成長 10 倍後掃描費用爆炸,而且 log 延遲讓告警晚 3-5 分鐘才響。根因:用線性成本的訊號做本該用聚合訊號做的事 |
| **面試怎麼問** | "Walk me through the three pillars of observability. When would you reach for each one, and what drives the cost of each?" |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| cardinality | /ˌkɑːr.dɪˈnæl.ə.ti/ | The number of unique time series produced by all label value combinations | label 所有取值組合出的序列數,metrics 成本的真正單位 |

---

## C-2: Prometheus 架構 (keystone)

### 核心概念: pull model 的存在理由

Prometheus does not wait for apps to send data. It **scrapes**: every 15-30s it makes an HTTP GET to each target's `/metrics` endpoint and stores what it reads.

Why pull instead of push? The deepest reason:

**In a push model, silence is ambiguous.** If a service stops sending metrics, is it dead, or just quiet, or is the network broken? You cannot tell. **In a pull model, a failed scrape is itself a signal.** Prometheus records `up == 0` for that target the moment the GET fails. The monitoring system knows the target is unreachable *because it went and checked*.

中文點破:push 是「員工自己回報平安」,人不回報你不知道是忙還是出事;pull 是「主管定時點名」,沒應答本身就是資訊。`up` 這個 metric 不是誰送出來的,是 Prometheus 每次 scrape 自己寫下的點名結果。

其他 pull 的紅利:target 端只要開一個 HTTP endpoint,無狀態、不用設定「要送去哪」;你可以隨時用 `curl http://pod-ip:port/metrics` 手動看同一份資料,debug 極度直觀。

### Service Discovery: 回扣 P0 的 watch

Pods come and go, IPs change (P2a 第一課:Pod IP is ephemeral)。Prometheus 的 scrape 名單怎麼跟得上?

**Kubernetes service discovery: Prometheus opens a watch against the API Server**, exactly the same long-lived watch mechanism kubelet and scheduler use (P0 C-3). When Endpoints/Pods change, the API Server streams the change, and Prometheus updates its target list within seconds. No config reload, no restart.

這是你第四次遇到 watch 了:kubelet watch 自己的 Pod、scheduler watch unscheduled Pod、Endpoints controller watch Pod 變化、現在 Prometheus watch scrape targets。k8s 生態的「自動跟上變化」全是同一招。

kube-prometheus-stack 再包一層:你 apply 一個 `ServiceMonitor` 物件(宣告「幫我 scrape 符合這個 label 的 Service」),Prometheus Operator watch 到它,轉譯成 scrape config。回扣 session 11 的三合一對照表:ServiceMonitor 是「規則=資料」,Operator 與 Prometheus 是「執行=引擎」,和 kube-proxy/Ingress Controller 是同一個模式,apply 物件本身不會有任何東西動起來,是引擎讀了物件才動。

### Exporter 模式與 TSDB 一句話

- **Exporter**: for software that can't expose `/metrics` itself (Linux kernel, MySQL, Redis), you run a sidecar-ish translator. `node_exporter` reads `/proc` and `/sys` and serves them as metrics. 學員在 P2a 手摸過的 `/proc/sys/net/netfilter/nf_conntrack_count`,node_exporter 就是幫你定時去讀它的那個人。
- **TSDB**: Prometheus stores (series → [(timestamp, value), ...]) on local disk, compressed to ~1-2 bytes per sample. Memory cost is dominated by the *number of active series*, not the number of samples. 這句是下面翻車坑的伏筆。

### Cardinality 爆炸: 生產最常見的翻車

C-1 畫的那條線,生產裡最常這樣被踩穿:某工程師想 debug,在 app metrics 加了 label `user_id`(或 `request_id`、`order_id`、完整 URL path 含參數)。

The math: `http_requests_total` with labels `{method, path, code}` might be 200 series. Add `user_id` with 500k users: **200 × 500,000 = 100 million series.** Prometheus memory usage explodes, scrapes slow down, then OOMKilled. 而且死的是監控系統本身:你在最需要眼睛的時候把眼睛弄瞎了。

Rule of thumb: a label is safe when its value set is **small and bounded** (method, status code, node name). Anything user-generated or unbounded (IDs, emails, raw paths) never goes in a label. 那種需求用 logs/traces 接(C-1 的分水嶺)。

查案指令(lab 會用到): `prometheus_tsdb_head_series` 看總序列數,`topk(10, count by (__name__)({__name__=~".+"}))` 抓出最肥的 metric。

### 動手 Lab: kube-prometheus-stack on kind

3 節點 kind 資源有限,用精簡 values。先寫 values 檔到 `portfolio/manifests/kps-values-kind.yaml`:

```yaml
# kps-values-kind.yaml: slim profile for a 3-node kind cluster
prometheus:
  prometheusSpec:
    retention: 6h
    scrapeInterval: 30s
    resources:
      requests: {cpu: 200m, memory: 512Mi}
      limits: {memory: 1Gi}
    # let Prometheus pick up ServiceMonitors/rules outside the helm release
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false
alertmanager:
  alertmanagerSpec:
    resources:
      requests: {cpu: 25m, memory: 64Mi}
      limits: {memory: 128Mi}
grafana:
  adminPassword: coach-lab
  resources:
    requests: {cpu: 50m, memory: 128Mi}
    limits: {memory: 256Mi}
prometheusOperator:
  resources:
    requests: {cpu: 50m, memory: 128Mi}
    limits: {memory: 256Mi}
```

步驟(指令單行;學員自己敲):

```bash
kubectl config current-context   # 必須是 kind-k8s-coach-p0
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kps prometheus-community/kube-prometheus-stack -n monitoring --create-namespace -f portfolio/manifests/kps-values-kind.yaml
kubectl -n monitoring get pods -w   # 等全部 Running,約 2-3 分鐘
kubectl -n monitoring get svc       # 找出 prometheus 和 grafana 的 svc 名
kubectl -n monitoring port-forward svc/kps-kube-prometheus-stack-prometheus 9090:9090
# 另一個 terminal:
kubectl -n monitoring port-forward svc/kps-grafana 3000:80   # 帳號 admin / coach-lab
```

觀察重點(讓學員自己發現,別先講):

1. Prometheus UI → Status → Targets。**kind 上 kube-scheduler、kube-controller-manager、etcd 的 target 是紅的(down)**,因為它們只綁 127.0.0.1。這不是壞掉,是最好的活教材:scrape 失敗 → `up == 0` → pull model 的「點名沒應答就是訊號」親眼看到了。在 Graph 頁查 `up`,對照哪些是 0。
2. Status → Service Discovery:看 k8s SD 發現了哪些 Pod/Endpoints,對回 watch 機制。
3. 查 `prometheus_tsdb_head_series`,記下健康基線(之後 chaos drill P4-2 會回來比對)。
4. 刪一個被 scrape 的 Pod(例如先 apply 一個帶 ServiceMonitor 的 demo app),看 target 列表幾秒內自動更新:SD 的 watch 在動,不用 reload。

### 誘答彈藥 (keystone 必備)

1. 「Prometheus 是 pull,所以 target 掛掉的瞬間我們就量不到它了,這是 pull model 的監控盲區;push model 才不會有盲區。」
   (錯。恰好相反:pull 之下 scrape 失敗立刻產生 `up == 0`,盲區變成明確訊號;push 之下 target 死掉只是「沒資料來」,和「它很閒」無法區分。學員剛在 lab 親眼看過紅色 target。)
2. 「Pod 會換 IP,所以每次 rolling update 完要 reload Prometheus 設定,不然 scrape 名單是舊的。」
   (錯。k8s SD 是對 API Server 的 watch,target 名單自動跟上,這正是 P0 watch 機制的第四次出場。answer 要能點出 watch 這個字。)
3. 「反正 Prometheus 是資料庫,把 user_id 放進 label 存起來,之後查誰的請求慢很方便。」
   (錯,而且是生產最常見翻車。TSDB 記憶體成本掛在 active series 數上,unbounded label 讓序列數乘上使用者數,監控系統自己 OOM。per-user 的問題屬於 logs/traces。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 公司 EKS 上要導 kube-prometheus-stack,SRE 問你「Prometheus 的 HA 和長期儲存怎麼辦?」 |
| **生產怎麼做** | 單台 Prometheus 是 SPOF 且 local TSDB 不適合放年度資料。常見解:跑兩台相同設定的 Prometheus(彼此獨立 scrape,告警去重靠 Alertmanager),長期儲存用 remote write 出去(Thanos/Mimir/AMP,AWS 上常直接用 Amazon Managed Prometheus)。EKS 上 control plane metrics 由 AWS 代管,你 scrape 不到 etcd,這點和 kind lab 看到的紅 target 成因不同但症狀像 |
| **真實踩坑** | 某次上線後 Prometheus 每 2 小時 OOMKilled 一次。查 `prometheus_tsdb_head_series` 從 30 萬爬到 800 萬:新版本 app 把完整 URL(含 query string 的 session token)當 label。修法:先 metric_relabel_configs 把該 label drop 掉止血(治標),再改 app 程式碼移除該 label(治本) |
| **面試怎麼問** | "Why does Prometheus use a pull model? What breaks first when metric cardinality explodes, and how do you find the offending metric?" |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| scrape | /skreɪp/ | Prometheus's periodic HTTP GET to a target's /metrics endpoint | 定時點名;失敗本身就寫成 up=0 |
| exporter | /ɪkˈspɔːr.tər/ | A translator process that exposes third-party or kernel stats as Prometheus metrics | 幫不會說 metrics 的軟體(kernel/MySQL)代言的翻譯官 |

---

## C-3: PromQL 與資料模型 (keystone)

### 核心概念: 三種 metric type 的第一性

**Gauge**: a value that can go up and down. Memory in use, queue length, `nf_conntrack_entries`. You read it directly; its current value is the answer.

**Counter**: a value that only goes up. Total requests served, total errors, total bytes. Why monotonic-only? Because it's just an in-memory integer the process increments; it never subtracts. 那重啟歸零怎麼辦?

**This is the key design insight**: Prometheus decided counters may reset to zero, and pushed the complexity into the query engine. `rate()` scans the window; whenever the value *decreases*, it knows a reset happened (counters can't legally go down) and compensates. So instrumentation stays dead simple (`counter++`), and restart-correctness is solved once, in one place, for everyone.

為什麼不乾脆讓 app 自己算好「每秒請求數」用 gauge 送?Because a pre-computed rate is baked to one window; a raw counter lets you compute rate over *any* window at query time, and a missed scrape only widens the sample gap instead of corrupting the number. 原始資料進庫、聚合留到查詢時,這是所有 TSDB 的共同哲學。

**Histogram**: for latency you want percentiles, but you can't average percentiles across Pods. Prometheus 的解法:把 latency 切進固定邊界的桶,每個桶是一個 counter(`le` label = "less than or equal"),桶是**累積式**的:`le="0.5"` 包含所有 ≤0.5s 的請求。Counters aggregate cleanly across Pods, so histograms do too. 這是「用一堆 counter 假裝成分佈」的技巧。

### rate() vs irate()

- `rate(x[5m])`: average per-second increase over the whole 5m window. Smooth, stable. **Use for alerting and dashboards.**
- `irate(x[5m])`: per-second increase between the *last two samples* only. Twitchy, reacts instantly, and just as instantly un-reacts. 只適合看即時尖峰,掛到告警上會又叫又停(flapping)。

### histogram_quantile: p99 是怎麼「算」出來的

```
buckets (cumulative counters):
  le="0.1"   ->  900     900 requests took <= 0.1s
  le="0.5"   ->  990      90 more took 0.1s ~ 0.5s
  le="1.0"   ->  998       8 more took 0.5s ~ 1.0s
  le="+Inf"  -> 1000       2 took over 1s

p99 = the latency of the 990th request (out of 1000)
    -> falls exactly at the le="0.5" boundary here
```

一般情況第 990 名落在某個桶的中間,Prometheus 只知道「它在 0.1s 到 0.5s 之間」,於是**在桶內做線性插值**:assume requests are evenly spread inside the bucket, and interpolate. So `histogram_quantile(0.99, ...)` is an **estimate**, and its error is bounded by your bucket boundaries. 桶切得粗,p99 就可能差很遠;真實值 120ms 可能被報成 300ms,只因為桶是 0.1 和 0.5。

打穿一層:this is a fundamental storage tradeoff, not a Prometheus quirk. Exact percentiles require keeping every observation (that's logs territory, linear cost). Histograms compress the distribution into k counters, paying with precision. 面試講到「p99 是估計值、精度由 bucket 邊界決定」就是 senior 訊號。

標準寫法(注意 `by (le)`,le 不能被聚合掉):

```promql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### by / without 聚合

`sum(rate(http_requests_total[5m]))` 全部加成一個數。`by (code)` 保留 code 維度,`without (instance)` 丟掉 instance 維度、其餘保留。經驗法則:dashboard 用 `by` 明確留你要看的維度;寫 recording rule 用 `without` 比較不會意外丟掉之後想要的 label。

### 常用告警寫法(附解讀)

```promql
# 1. Symptom: error ratio over 1% (SLI-shaped, C-4 的主角)
sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.01
# 解讀: 用比率不用絕對數。「每分鐘 50 個錯誤」在尖峰是雜訊、在半夜是災難,比率才可比

# 2. Symptom: p99 latency over 500ms
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 0.5
# 解讀: 平均值會騙人(見誘答 2),尾端延遲才是使用者的真實體驗

# 3. Cause->symptom bridge: container restarting repeatedly
increase(kube_pod_container_status_restarts_total[15m]) > 3
# 解讀: 回扣 P1,OOMKilled(137)/壞 probe/CrashLoop 全會推高這個 counter
# 用 increase 不用原始值: RESTARTS 累積 47 次不代表現在有事,15 分鐘內 +3 才代表正在壞

# 4. Saturation: conntrack table nearing capacity (回扣 P2a 謎題C)
node_nf_conntrack_entries / node_nf_conntrack_entries_limit > 0.8
# 解讀: 學員在 P2a 學過 table full 時「舊連線照常、新連線被 drop」,
# 這種「滿了才爆」的資源必須在 80% 就告警,爆了才知道就晚了。gauge 直接比,不需要 rate

# 5. Meta-monitoring: target down
up == 0
# 解讀: pull model 的點名結果。實務會加 for: 5m 抗抖動,並注意它是 cause-based,
# 適合 ticket 不適合半夜 page(C-6 會展開)
```

### 誘答彈藥 (keystone 必備)

1. 「counter 重啟會歸零,統計就不準了,所以重要數據應該用 gauge 自己維護,app 重啟前存起來。」
   (錯。`rate()` 偵測到數值下降即視為 reset 並補償,重啟正確性在查詢引擎統一解掉;要 app 自己持久化 counter 反而把每個 app 都變成有狀態的複雜體。)
2. 「p99 500ms 太誇張了吧,我看平均 latency 才 80ms,系統明明很健康。」
   (錯,average 和 tail 是兩件事:1% 的請求慢到 5 秒,平均值幾乎不動,但那 1% 在高流量下就是每分鐘幾百個真實使用者。回 C-1:metrics 聚合丟掉了個體,percentile 就是為了把「最慘的那群人」找回來。)
3. 「告警要即時,所以查詢全部用 irate,rate 是 5 分鐘平均太鈍了。」
   (錯。irate 只看最後兩個樣本,尖峰一過立刻回落,告警會 flapping;告警要的是「持續存在的狀態」,rate + for 才對。這也是 level-triggered 思想的回聲:看狀態,不追瞬間。)
4. 「histogram_quantile 算出 p99=470ms,這就是精確的第 99 百分位。」
   (錯,是桶內線性插值的估計值,誤差由 bucket 邊界決定。能講出「為什麼是估計、怎麼縮小誤差=調 bucket」才算打穿。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你把告警 `rate(errors[5m]) > 10` 上線,PM 問「10 是怎麼來的?」你答不出來 |
| **生產怎麼做** | 閾值不拍腦袋:先出 recording rule 記錄比率,觀察 2-4 週的正常分佈,再依 SLO 反推閾值(C-4 的 burn rate 就是系統化解法)。所有 PrometheusRule 進 Git 走 PR,reviewer 會問的第一題就是「這個閾值的依據?」 |
| **真實踩坑** | 告警寫 `http_requests_total{code="500"} > 100`:counter 原始值只會一直漲,上線第二天永久 firing,團隊直接靜音,三週後真事故沒人看。counter 幾乎永遠要包 rate/increase 再用 |
| **面試怎麼問** | "Your service restarts wipe the request counter. Why do Prometheus graphs still show correct rates? How does histogram_quantile actually compute p99, and when is it wrong?" |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| counter reset | /ˈkaʊn.tər ˈriː.set/ | A counter dropping to zero on process restart, detected and compensated by rate() | 重啟歸零不是 bug,rate 看到下降就知道是 reset |
| quantile | /ˈkwɒn.taɪl/ | The value below which a given fraction of observations fall | p99=99% 的請求比這個值快;尾端體驗的量尺 |

---

## C-4: SLI / SLO / Error Budget (keystone, senior 面試核心)

### 第一性: 為什麼不追 100%

Two independent reasons, both worth saying in an interview:

1. **Cost grows exponentially, not linearly.** Each extra nine roughly means: another AZ, another region, another on-call rotation, another layer of redundancy. 99.9 → 99.99 is not "0.09% better", it's often 10x the engineering cost.
2. **Users can't tell the difference past a point.** Your user reaches you through their ISP, their WiFi, their phone. If the path to you is 99.5% reliable, they physically cannot perceive whether you are 99.99% or 99.999%. Reliability beyond the noise floor of the access path is money spent on something nobody can feel.

中文點破:可靠性是有邊際效益遞減的商品,而且買它的貨幣是「工程速度」。100% 的真實含義是「永遠不准改任何東西」,那生意就死了。

### SLI: 選一個使用者感覺得到的比率

An SLI (Service Level Indicator) is a **ratio of good events over total events, measured where the user is**:

```
SLI = good events / total events

availability SLI: non-5xx responses / all responses
latency SLI:      responses faster than 300ms / all responses
```

選 SLI 的紀律:必須是 user-facing。CPU 使用率、memory 水位、Pod 重啟次數都不是 SLI,它們是 cause,使用者感覺不到 CPU 80%,只感覺得到「頁面轉圈圈」。用學員自家的 billing 平台造句:billing API 的 SLI 可以是「成功回應且 <500ms 的請求比率」,而「EKS node CPU < 70%」永遠不是 SLI。

**SLO** (Objective) 就是給 SLI 定的目標值加時間窗:"99.9% of billing API requests succeed, measured over 30 days."

### Error Budget: 可以花的失敗額度

SLO 99.9% over 30 days 換算:

```
30 days = 43,200 minutes
budget  = 0.1% x 43,200 = 43.2 minutes of full outage per month
```

**The reframe that makes this a senior topic**: the budget is not a shame quota, it's a *spending account*. Deploys, risky migrations, chaos drills: all of them spend budget. Budget left = ship faster. Budget gone = freeze features, spend the sprint on reliability. 這讓「要不要上這個版」從 Dev 和 SRE 的意氣之爭,變成看帳本說話的談判:error budget 是發版速度與可靠性之間的談判貨幣。面試官問 "how do you balance velocity and reliability" 時,這就是標準答案的骨架。

### Multi-window burn rate alert: 為什麼單一閾值又吵又慢

Naive alert: "error rate > 0.1% for 5 minutes". Two failure modes:

- **Too noisy**: a 6-minute blip at 0.12% pages you at 3am, but it only spent ~0.3% of the monthly budget. Nobody needed to wake up.
- **Too slow**: a slow leak at 0.3% error rate never looks dramatic in any 5-minute window, but it silently eats the whole month's budget in 10 days.

The fix: alert on **burn rate** = how fast you're consuming budget, relative to the "spend it exactly in 30 days" pace (burn rate 1 = 剛好月底花完).

```
page:   burn rate >= 14.4 over 1h  AND  over 5m    (2% of monthly budget gone in 1h)
ticket: burn rate >= 1    over 3d  AND  over 1h    (slow leak, fix in working hours)
```

Two windows per alert 的理由:長窗(1h)證明「這不是抖動,已經燒掉有感額度」,短窗(5m)證明「現在還在燒」,兩者 AND 起來,修好後告警立刻收聲,也不會被 6 分鐘的 blip 叫醒。這是對「又吵又慢」兩個病根各下一味藥。

### 誘答彈藥 (keystone 必備)

1. 「SLO 當然越高越好,能設 99.99 就不要設 99.9,對使用者更負責。」
   (錯,本 chunk 的中心誘答。三刀:成本每加一個 9 近似 10 倍;使用者隔著 99.5% 的最後一哩路感覺不到差異;SLO 越緊 error budget 越小 = 發版空間越小,你其實是拿全公司的迭代速度去買沒人感覺得到的 9。SLO 是商業決策,不是工程美德競賽。)
2. 「這個月 error budget 還剩 90%,代表系統很穩,監控可以少看一點。」
   (半錯得很陰險:剩 90% 不是「少看」的理由,而是「可以花」的訊號,該拿去做風險較高的部署、演練、依賴升級。budget 剩太多有時反而代表你太保守,迭代速度輸給對手。)
3. 「我們的 SLI 用 node CPU 使用率,超過 80% 就算違反 SLO。」
   (錯在選材:CPU 是 cause 不是 user-facing symptom。CPU 90% 而使用者無感=沒事;CPU 30% 但下游 DB 死鎖=使用者全掛。SLI 必須量測使用者的體驗面。這題和 C-6 的 symptom vs cause 同源。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你提議給公司 billing API 定 SLO,PM 說「我們對客戶承諾 99.95 uptime,SLO 就寫 99.95」 |
| **生產怎麼做** | 分清 SLA(對外合約,違反要賠錢)和 SLO(內部目標)。SLO 必須比 SLA 嚴,中間留緩衝:SLA 99.95 的話 SLO 常設 99.97-99.99 的某個實測可達值,先看 6 個月歷史 SLI 再定,不是抄合約數字 |
| **真實踩坑** | 團隊定了 99.99 的 SLO 但歷史資料只做得到 99.9:第一週 budget 就燒穿,告警常駐 firing,兩週後全員把 SLO 告警當壁紙。SLO 定超過實力=直接摧毀告警的公信力,比不定還糟 |
| **面試怎麼問** | "Define SLI, SLO, and error budget for a payments API. Your PM wants five nines; talk me through the pushback. Why do burn-rate alerts use two windows?" |

`[RUNTIME: 學員公司 billing 平台的真實 SLA/告警現況可挖出來當本 chunk 的案例素材,值得的話進 story-bank 與面試 STAR 故事]`

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| SLO | /es el oʊ/ | A target value for an SLI over a time window, set below your SLA | 內部可靠性目標;比對外合約(SLA)嚴一截 |
| error budget | /ˈer.ər ˈbʌdʒ.ɪt/ | The allowed amount of unreliability implied by the SLO: 1 minus the target | 可以花的失敗額度;發版與可靠性的談判貨幣 |
| burn rate | /bɜːrn reɪt/ | How fast the error budget is being consumed relative to the SLO period pace | 燒錢速度;14.4 倍=1 小時燒掉月額度 2% |

---

## C-5: OpenTelemetry 與 Distributed Tracing

### 核心概念: span/trace 模型

A **span** is one timed operation: name, start time, duration, attributes, and a parent span ID. A **trace** is the tree of spans sharing one trace ID, telling the causal story of a single request:

```
trace 4bf92f... : POST /checkout                    total 812ms
|-- api-gateway: handle request       [0ms   .. 812ms]
    |-- billing-svc: POST /charge     [10ms  .. 790ms]
    |   |-- db: SELECT account        [15ms  ..  35ms]
    |   |-- payment-gw: HTTP call     [40ms  .. 780ms]   <- 兇手在這
    |-- notify-svc: send email        [791ms .. 810ms]
```

Metrics 告訴你 p99 變慢了(多嚴重),trace 告訴你這 812ms 花在誰身上(哪裡壞)。這正是中心問題「5 分鐘內定位」的最後一塊拼圖。

點破學員的老朋友:P2a 排障時他把 conntrack 誤拉進 DNS 題(層級混淆)。Trace waterfall 是治這個病的工具化解法:每一段時間都被迫歸屬到明確的一層(app span、DB span、或 span 之間的 gap=網路/排隊),想混層都混不了。

### Context Propagation 打穿: traceparent 怎麼跨服務

The hard problem: service B must know "this incoming request belongs to trace 4bf92f, my parent is span 00f067". 這個資訊不會自己長腳,it travels **inside the request itself**, as the W3C `traceparent` HTTP header:

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             ^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^ ^^
          version          trace-id                parent span-id  flags(sampled?)
```

Each hop: SDK reads the header, creates a child span, and writes a *new* header (same trace ID, its own span ID as the new parent) into every outgoing call. 一棒接一棒,每一棒都要「讀進來、傳出去」。

**為什麼斷鏈(broken trace)**: any hop that fails to relay the header snaps the chain. 常見四種:

1. 中間有個服務沒裝 instrumentation(收到 header 但呼叫下游時沒帶出去)。
2. 出了 HTTP 的世界:丟進 message queue、cron job 撿起來做,header 沒被塞進 message 屬性裡。
3. Async/thread pool:span context 存在 thread-local,任務切到另一條 thread 時 context 沒跟過去。
4. 新舊標準混用:一邊講 W3C traceparent、一邊講 Zipkin B3 header,雞同鴨講。

盲講這條鏈時用「讀 header → 開 child span → 寫新 header 給下游」三步當骨架默數,和 P0 五棒同一招(學員盲講容易漏中間棒次,Weekly Review #1 已驗證過這個弱點)。

### OTel SDK vs Collector 分工

- **SDK (in-process)**: creates spans, manages context propagation, batches and exports. App 只依賴中立的 OTel API,不綁任何 vendor。
- **Collector (out-of-process)**: receives OTLP from all apps, then processes (batch, retry, drop noisy attributes, tail sampling) and exports to any backend (Jaeger, Tempo, X-Ray, vendor SaaS).

分工的理由一句話:app 團隊管「產生訊號」,平台團隊管「訊號去哪、留多少」;換 backend 或改 sampling 是改 Collector 設定,幾十個 app 一行程式碼都不用動。這又是解耦 pipeline,和 P0「元件只做自己的事、透過中介解耦」同構。

### Sampling: head vs tail

Tracing 每個 request 都全存 = logs 級的線性成本,所以要抽樣:

- **Head sampling**: decide at the *start* of the trace (e.g. keep 1%). Cheap, decided by SDK, but it's blind: the slow, broken 1‰ you care about most is almost never in the sample.
- **Tail sampling**: Collector buffers the whole trace, decides at the *end*: keep all errors, all >1s traces, plus 1% of the boring ones. Exactly the interesting ones survive. 代價:Collector 要有記憶體 buffer 整條 trace,而且同一 trace 的所有 span 必須路由到同一台 Collector(load balancing by trace ID),架構複雜一級。

### 動手 Lab: Jaeger + HotROD,追一條 p99 慢請求

HotROD 是 Jaeger 官方的教學 app(叫車服務,內建故意做壞的效能問題),一個 image 搞定,適合 kind。

規格(YAML 學員自己寫,放 `portfolio/manifests/`):

- Deployment `jaeger`:image `jaegertracing/all-in-one:1.57`,單副本,port 16686(UI)與 4318(OTLP HTTP)。in-memory 儲存,夠 lab 用。
- Service `jaeger`:ClusterIP,曝 16686 與 4318。
- Deployment `hotrod`:image `jaegertracing/example-hotrod:1.57`,args `["all"]`,env `OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318`,port 8080。
- Service `hotrod`:ClusterIP,曝 8080。

```bash
kubectl config current-context   # kind-k8s-coach-p0 才准動
kubectl apply -f portfolio/manifests/   # 學員寫好的 jaeger + hotrod
kubectl port-forward svc/hotrod 8080:8080
kubectl port-forward svc/jaeger 16686:16686   # 另一個 terminal
```

追查流程(這就是 Phase Gate 的「追一條 trace」預演):

1. 開 http://localhost:8080,連按同一顆叫車按鈕 10-20 次(製造併發),注意 UI 顯示的 latency 越按越糟。
2. 開 Jaeger UI(16686):Service 選 `frontend`,Min Duration 填 `800ms`,Find Traces:這就是「從 p99 撈個體」的動作,metrics 給閾值、trace 給樣本。
3. 點開最慢的一條,讀 waterfall:找最長的 span,以及 span 之間的空隙(gap = 沒被 instrument 的等待:排隊、鎖、網路)。
4. HotROD 埋的其中一個病根:mysql span 一次比一次長,span 的 log/attributes 裡直接寫著 lock 等待。說出「哪一層、為什麼、治標與治本各是什麼」才算完成。
5. 收尾必做:講出這條 trace 的 traceparent 是怎麼從 frontend 傳到 mysql span 的(讀→開→寫三步)。

### 誘答彈藥

1. 「trace 上 billing-svc 呼叫 payment-gw 的 client span 花了 740ms,所以是 payment-gw 服務慢,找他們team。」
   (陷阱在層級:要對照 payment-gw 的 server span。若 server span 只有 30ms,時間其實花在兩個 span 之間的 gap:連線建立、TLS、排隊、DNS、conntrack 之類的網路層(P2a 的世界)。client span 長 ≠ 對方 app 慢。這題直打學員的層級混淆弱點。)
2. 「為了省成本 sampling 設 1% head sampling 就好,反正出事的 trace 總會被抽到幾條。」
   (錯。事故常集中在 0.1% 的請求,1% 盲抽幾乎必漏;錯誤與慢請求要靠 tail sampling 的規則保全。能講出 tail 的代價(buffer + 同 trace 同 Collector)才算完整。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 微服務化半年後,「這個 API 慢」的 Slack 訊息平均要 4 個 team 互踢兩天才有結論 |
| **生產怎麼做** | 全鏈路上 OTel auto-instrumentation(Java agent / Python sitecustomize,不用改業務碼),Collector 做 tail sampling(errors + slow 全留),trace ID 印進 access log 讓三種訊號互相跳轉。「慢」的爭論從開會變成貼一條 trace URL |
| **真實踩坑** | 導入後發現所有 trace 都在 API gateway 就斷頭:gateway 的 header allowlist 沒放行 `traceparent`,下游全部變成孤兒 trace(每個服務自己開新 trace ID)。查斷鏈永遠先抓「誰吃掉了 header」 |
| **面試怎麼問** | "How does trace context cross service boundaries? Name three ways a trace breaks. Head vs tail sampling: what do you trade?" |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| span | /spæn/ | One timed operation in a trace, carrying a parent reference and attributes | trace 樹上的一節;有始有終有爸爸 |
| context propagation | /ˈkɒn.tekst ˌprɒp.əˈɡeɪ.ʃən/ | Passing trace identity across process boundaries, e.g. via the W3C traceparent header | 因果鏈的接力棒;斷鏈=有人沒把棒交出去 |
| tail sampling | /teɪl ˈsɑːm.plɪŋ/ | Deciding which traces to keep after they complete, so errors and slow ones survive | 看完再決定留誰;精準但要 buffer 整條 trace |

---

## C-6: 告警工程與 on-call 現實

### 核心概念: alert fatigue 是系統性風險

The failure mode is human, not technical: **every false page trains the on-call to ignore pages.** After two weeks of noise, the real incident gets the same mute button. 告警的殺傷力不在漏報,在「狼來了」把人的注意力預算燒光。這和 error budget 同構:on-call 的信任也是一種 budget,誤報在花它。

Via Negativa 優先:一個健康的告警系統,第一步通常是刪告警,不是加告警。每條 page 級告警要能通過三問:它代表使用者正在痛嗎?需要「現在、這個人」處理嗎?有明確的下一步動作嗎?三者缺一,降級成 ticket 或刪掉。

### Symptom-based vs cause-based

- **Symptom-based**: alert on what users feel: error ratio, p99 latency, SLO burn rate. 病人發燒了。
- **Cause-based**: alert on internal states: CPU 80%, Pod restarted, disk 70%, `up == 0`. 某台儀器讀數怪怪的。

原則:**page on symptoms, use causes as diagnosis context.** Causes without symptoms are tickets at best:Pod 重啟 3 次但 SLI 無感,代表 k8s 的 reconcile 把它救回來了(P0 的自癒在幫你值班),半夜叫醒人類幹嘛?反過來,症狀告警天然涵蓋你沒想到的故障:你不可能為每種 cause 寫一條規則,但任何 cause 最終都會流到 error ratio 或 latency 上。

回扣學員親手做過的案例:P1 session 6 那隻 web-frontend(probe 打錯 port,健康 app 被反覆殺)。Cause-based 視角看到的是 RESTARTS 猛跳;symptom-based 視角看到的是該服務的成功率歸零。兩個訊號都在,但該把人叫醒的理由是後者,前者是叫醒之後用來縮小範圍的線索。

### Runbook 文化與告警的完整定義

生產裡一條合格的告警不是一句 PromQL,是一個四件套:

1. expression + for(規則本體)
2. severity(page / ticket)
3. summary annotation(一句人話:什麼壞了、影響誰)
4. **runbook_url**:點開就有「怎麼確認、怎麼止血、怎麼根治、什麼時候升級(escalate)」

Runbook 的核心價值是把 3am 的認知負荷降到最低:凌晨三點的你智商只剩六成,靠的是白天的你寫好的檢查清單。針對學員的長期改進項(連三個 session 被點名「先跳結論、要追問才講治標治本」):寫 runbook 時強制自己分「止血(治標)」與「根治(治本)」兩欄,把這個思考結構固化成肌肉記憶,面試答 incident 題時同樣的骨架直接複用。

### On-call 的現實

What a sane on-call setup looks like: one primary + one secondary, pages go through escalation (5 min no-ack then escalate), a hard rule that every page gets one of three outcomes: fix it, downgrade the alert, or delete the alert. Post-incident review 是 blameless 的:追問的是「系統為什麼讓這個錯誤可能發生」,不是「誰手滑」。

Alertmanager 在這層的三個武器:grouping(同源告警合併成一則通知)、inhibition(node 掛了就抑制它身上 30 個 Pod 的告警,只留根因)、silence(維護窗先靜音,帶到期時間)。Chaos drill P4-1 會親手用到這三個。

`[RUNTIME: 學員是接 on-call 的 DevOps。開講前先挖他的真實 on-call 經驗:被 page 過最冤的一次、最近一次半夜告警、公司現在的告警走什麼(CloudWatch alarm? PagerDuty?)。真實案例直接當本 chunk 的教材,好的進 story-bank 做面試 STAR 素材]`

### 誘答彈藥

1. 「告警寧可多不可少,多裝幾條總是安全的,大不了多看幾眼。」
   (錯。每條誤報都在消耗 on-call 的信任額度,雜訊多到一個程度,真告警會被連坐靜音;「多看幾眼」在 3am 不存在。告警系統的健康指標之一是 page 的 actionable 比率,不是條數。)
2. 「`up == 0` 是最重要的告警,任何 target 掛掉都該立刻 page。」
   (陷阱:up 是 cause-based。單一 Pod 的 target 掛掉,若副本與 SLI 無感,是 ticket 不是 page;但「全部 target 同時 up==0」又另當別論(監控自己瞎了)。能分層處理才是 senior 答案。)

### 現實世界這樣做

| 段 | 內容 |
|----|------|
| **情境** | 你入職新團隊,發現 Slack #alerts 頻道每天 200+ 則,全員已讀不回 |
| **生產怎麼做** | 告警考古:拉一個月的告警統計,按「有無人動作」分類;無動作的一律降級或刪除;剩下的補 runbook;page 級全部改掛 SLO burn rate。一個季度把 page 從每週 40 則壓到 5 則以下,才談得上 on-call 品質 |
| **真實踩坑** | node 掛掉一台,瞬間湧出 87 條告警(node 上每個 Pod、每個 target、每條依賴各自尖叫),on-call 在雜訊裡找根因找了 40 分鐘。修法:Alertmanager 按 node/namespace grouping + 用 inhibition 讓 node-down 抑制下游告警。這正是 drill P4-1 的劇本 |
| **面試怎麼問** | "Symptom-based vs cause-based alerting: give examples of each. A node dies and 80 alerts fire; how do you engineer that down to one page?" |

### 術語卡 (Key Terms)

| EN term | 發音 | One-line English definition | 中文點破 |
|---------|------|----------------------------|---------|
| alert fatigue | /əˈlɜːrt fəˈtiːɡ/ | Desensitization from noisy alerts, causing real incidents to be ignored | 狼來了效應;誤報在燒 on-call 的信任額度 |
| symptom-based alerting | /ˈsɪmp.təm beɪst/ | Paging on user-visible degradation instead of internal component states | 對「使用者在痛」告警,cause 留作診斷線索 |

---

## Chaos Drill Hooks (P4)

> 完整劇本歸 `references/chaos-drills.md`,用 drill ID 對接(P4 樁位若尚未建立,coach 依此鉤子現場展開,事後回填該檔)。

### Drill P4-1: Alert 風暴(對接 chaos-drills.md `P4-1`)

鉤子:在 monitoring stack 正常運作下,`docker stop` 掉一台 kind worker(或 drain 後 stop),瞬間引爆數十條告警(node down、Pod 消失、targets down、KubeXXX 系列全響)。限時任務:在告警海裡 (1) 找出唯一的根因告警 (2) 用 Alertmanager 的 grouping/inhibition/silence 把雜訊壓掉 (3) 說出哪幾條該永久降級。驗收點:C-6 的 symptom vs cause 分層要在嘴上用出來。結束 `docker start` 恢復並確認告警自動 resolve。

### Drill P4-2: Cardinality 爆炸(對接 chaos-drills.md `P4-2`)

鉤子:部署一個故意帶 `request_id` label 的 demo app(或用 script 對 pushgateway/自製 exporter 灌高基數序列),配 ServiceMonitor 讓 Prometheus 吃進去。學員任務:從「Prometheus 記憶體上漲、UI 變鈍」的症狀出發,用 `prometheus_tsdb_head_series` 對比 C-2 lab 記下的基線,再用 `topk(10, count by (__name__)({__name__=~".+"}))` 揪出兇手 metric,講出止血(drop label / 刪 target)與根治(改 instrumentation)。回扣 C-1 的分水嶺一句話收尾。

---

## P4 畢業 Gate

**考核形式**(兩關,對應 gate 定義「能定義 SLO 並追一條 trace」):

**第一關:SLO 設計答辯(白板 + 口頭,SLO 說明至少一半用英文講)**

以他自家 billing API(或 coach 指定的服務)為題,不看筆記完成:

1. 選出 1 個 availability SLI + 1 個 latency SLI,寫成 good/total 比率,並說明為什麼是 user-facing。
2. 定 SLO 目標值與時間窗,答辯「為什麼不是 99.99」(coach 扮 PM 施壓,學員要用成本曲線 + 使用者感知下限 + error budget 換發版速度三個論點推回來)。
3. 換算 30 天 error budget 成分鐘數,寫出 fast/slow 兩組 multi-window burn rate 告警,解釋雙窗各自防什麼。

**第二關:trace 追殺(kind lab 實作,限時 15 分鐘)**

在 HotROD lab 上,coach 指定一個「p99 變慢」的症狀,學員要:

1. 在 Jaeger 用 min duration 撈出慢 trace 樣本。
2. 讀 waterfall 定位到具體 span 或 gap,說出是哪一層(app/DB/網路排隊)。
3. 主動講完「根因 + 止血 + 根治 + 先驗證什麼」四段,不等追問(長期改進項的驗收點)。
4. 口頭走一遍 traceparent 從入口到兇手 span 的傳遞鏈(讀→開→寫,不漏棒)。

**Pass 條件**:

- SLI 選的是 user-facing 比率,且能當場駁倒「CPU 當 SLI」和「SLO 越高越好」兩個誘答。
- error budget 分鐘數換算正確,雙窗 burn rate 的「防吵/防慢」各自講對。
- trace 關在時限內定位正確層級,traceparent 鏈完整不斷棒。
- 全程至少一半英文完成第一關的說明(P4 English Ramp 檔位驗收)。

**Stretch(加分,不強求)**:

- 講出 histogram_quantile 為什麼是估計值,以及 bucket 邊界怎麼影響 SLO latency SLI 的量測。
- 用 tail sampling 的取捨,解釋生產環境怎麼保證「事故 trace 一定還在」。

**Gate 失敗處理**: 見 SKILL.md Phase Gate Failure 協議。`[RUNTIME: 常見弱點依 mistake-registry 對症;若第一關卡在英文表達而非概念,拆開重測:先中文過概念,再單獨補英文覆述]`

---

## Portfolio 整合 (P4)

**observability/ 是 portfolio 的主秀資料夾**(session 10 稽核時已預留的 showcase 位,P4 起正式長內容)。過價值門檻的 artifact:

```
portfolio/observability/
  slo/billing-api-slo.md        # 第一關產出: SLI 定義、SLO 目標與理由、budget 換算、burn rate 告警設計
  alerts/slo-burn-rate.yaml     # PrometheusRule: multi-window burn rate(附註解說明雙窗)
  alerts/platform-baseline.yaml # C-3 那 5 條基線告警,每條帶一行 rationale 註解
  dashboards/slo-overview.json  # Grafana dashboard export: SLI 曲線 + budget 餘額 + burn rate
  runbooks/high-error-rate.md   # 一份合格 runbook 樣本: 確認/止血/根治/升級 四段
portfolio/manifests/
  kps-values-kind.yaml          # 精簡 values(環境配置,放 manifests 不算主秀)
  jaeger.yaml / hotrod.yaml     # C-5 lab 學員自己寫的
portfolio/notes/
  p4-*.md                       # 學習筆記照舊
```

價值門檻判斷:SLO 文件、burn rate rule、runbook 樣本是面試能直接攤開講的東西,必進 repo;port-forward 截圖、Prometheus UI 操作步驟之類的過程記錄留本機筆記即可。

---

## P4 英文 Ramp

P4 檔位:半英半中(本檔核心原理段已直接用英文寫)。驗收方式從「Say-it-in-English 輕推」升級為「關鍵概念預設用英文講,卡住才切中文」。學員曾明說偏好中文佔比多一些:概念第一次學用中文打通沒問題,但每個 chunk 的 Feynman Gate 至少一題要求英文作答,並照慣例給 English Polish。`[RUNTIME: 依學員當下英文信心調整推壓力度,連兩次卡殼就退回中文過概念、英文單獨補]`

**本 phase 必須能用英文一句話講出的命題**(gate 前逐條抽):

1. "Metrics are cheap because they aggregate; logs are expensive because they don't; high cardinality is the line between them."
2. "In a pull model, a failed scrape is itself a signal: that's the up metric."
3. "rate() treats any counter decrease as a restart and compensates, so instrumentation stays a dumb increment."
4. "histogram_quantile interpolates inside a bucket, so p99 is an estimate bounded by your bucket boundaries."
5. "An error budget is the amount of failure you're allowed to spend; it prices the tradeoff between shipping fast and staying reliable."
6. "Burn-rate alerts use a long window to prove it matters and a short window to prove it's still happening."
7. "Trace context crosses services inside the request, as the W3C traceparent header; any hop that drops it breaks the chain."
8. "Page on symptoms; use causes to diagnose."

**術語卡總表**(同步進 `workspaces/k8s/term-registry.md` 做間隔抽考):

| 主題 | 術語 |
|------|------|
| C-1 三訊號 | cardinality |
| C-2 Prometheus | scrape, exporter |
| C-3 PromQL | counter reset, quantile |
| C-4 SLO | SLO, error budget, burn rate |
| C-5 Tracing | span, context propagation, tail sampling |
| C-6 告警 | alert fatigue, symptom-based alerting |

共 13 張,全部過「senior 面試會考或錨定底層機制」門檻。
