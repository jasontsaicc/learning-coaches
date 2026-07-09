# Teaching Elements

Domain content that fills Teaching Flow steps B, C, D, E, and F. The engine owns the step
structure and all gate mechanics; this file supplies the k8s-specific content poured into
each step. Per-topic material lives in the phase reference files (see `curriculum.md`);
this file defines the reusable templates and k8s-specific step content.

## Step B (Scenario Intro)

用真實生產情境開場(why this matters today)。完整場景庫在 `references/real-world-scenarios.md`(23 scenes,P0-P5),每景走四段式範本:

| 段 | 內容 |
|----|------|
| **情境** | 一個具體的生產場景(e.g.「線上服務半夜被擴容打爆」) |
| **生產怎麼做** | 業界實際的處理方式 / 標準配置 |
| **真實踩坑** | 這個機制常見的翻車點(對應 progress.md Mistake Registry) |
| **面試怎麼問** | 面試官會用什麼角度考這個點(對應 `references/interview-bank.md`) |

前兩段屬 step B,後兩段在 step C 收尾時帶到。

## Step C (Core Teaching: first principles + chunks)

k8s-coach 的加重項:每個 k8s 機制都要往下問一層「這底下其實是哪個 OS / 網路 / 分散式 / 控制理論原理?」打穿後必接遷移題。範本:

```
[k8s 機制] 底下其實是 [哪個 OS/網路/分散式/控制理論原理]
  → 一句話講清楚這個原理怎麼撐起這個機制
  → 遷移題:把原理推到一個新情境,問學員會怎樣 / 怎麼查
```

範例:Service 的 ClusterIP → kube-proxy 用 iptables/conntrack 轉發 virtual IP → 遷移題「conntrack table 滿了會怎樣?你怎麼查?」。跨 phase 底層原理(TCP/DNS/perf)集中在 `references/foundations-linux-network.md`。

**Transfer 題型(供 Feynman Gate 第二關使用,k8s 特化):**
- 遷移:「conntrack table 滿了會怎樣?你怎麼查?」
- 比較:「X 跟 Y 差在哪?什麼時候用哪個?」
- 反例:「拿掉這個元件會壞掉什麼?」
- 排障:「這個現象,你的第一個排查指令是什麼?為什麼?」
- **🎣 誘答(每個 keystone chunk 的 Transfer 至少一題)**:丟一個「聽起來合理、其實錯」的說法,埋在學員似懂非懂的邊界上,要他抓出來並講為什麼錯。沒抓到 = 那裡真的鬆,當場入 Mistake Registry;抓到 = 點名稱讚他守住判斷。專打「覺得怪怪的、但沒把握就被同事牽著走」的真實弱點。誘答題庫在 `references/interview-bank.md` 誘答庫區。範例:教完「kube-proxy 寫 iptables 規則」→ 誘答「所以 kube-proxy 是一直在搬封包的程式囉?」(錯,它只寫規則、kernel 才搬)。
- **Say it in English(偶爾)**:要求用一兩句英文講機制,寄生驗收(檔位規則見 `language.md`)。

**術語卡(每主題 0-3 張,寄生在 step C):**

```
EN term | 發音 | one-line English definition | 中文點破
```

同步寫進 `workspaces/k8s/term-registry.md` 進間隔抽考。**價值門檻:只給「面試官真的會考」或「能錨定一個底層機制」的術語做卡**(e.g. reconcile loop、conntrack、QoS class);定義型瑣碎詞、工具名、設定檔名稱不做卡。寧可 0 張,不塞低價值卡稀釋複習。

## Step D (Hands-On)

親手 apply / 觀察 / 改。叢集開關與驗證見 `lab-manager.md`;每個 phase 的具體 lab 在對應 phase reference 檔。

**Why-first 規則(每個實驗)**:按 Enter 前先講兩句 — 預測結果 + 一口氣講機制 why。結果只拿來驗證預講;預講不出來 = 當場入 Mistake Registry,不等 step F 才發現。這把「隱性會」(結果預測準但 why 講不出)在最便宜的時點逼成顯性。

## Step E (Drill)

k8s-coach 的 step E 是 **Chaos Drill:故意弄壞 → 限回合 debug**,訓練 senior SRE 的排障腦:

- 每個主題都附「先看正常 → 注入故障 → 限定回合內定位根因」。破壞劇本庫在 `references/chaos-drills.md`(20 drills,按需讀取)。
- 用 `scripts/lab-cluster.sh reset [phase]` 乾淨重來,給 drill 反覆摔。
- 判定用 scorecard 的 MTTR 維度(P2a 起):看回合數與排查方向(第一個指令選得對嗎),不是分鐘數。
- 卡住時不直接給答案,引導「這個現象,底層哪個環節最可能出問題?」
- 每次 drill 的踩坑 + 根因入 Mistake Registry,進間隔抽考。
- **P3 大型故障演練**:節點掛、流量暴增、OOM 雪崩、滾動更新出包,串起前面所有底層,產出 runbook + 演練紀錄進 portfolio。

**三分類牌(30 秒 drill,可掛 step A 複習或 step E 收尾)**:丟一個名詞問「規則(宣告)/ 狀態(runtime 記憶)/ 資料(被查的名單)?」題池:iptables 規則=規則、conntrack=狀態、Endpoints=資料、Ingress 物件=規則、nginx.conf=規則(render 產物)、etcd 內容=資料(desired)。同家族的坑在 Mistake Registry 合併成一張 pattern 卡追蹤,家族三連過才算封印。

**一句話精準版**:複習抽考過關不只看「對」,要收一句精準收尾(例:kube-proxy 只寫規則、kernel 搬封包)。說不出精準版 = 半過,拉回近期重抽。

## Step F Material (naive-but-deep question DNA)

engine 擁有 Teach-to-Learn 的整個 loop;這裡只供 k8s 的題材 DNA。菜鳥只問 naive-but-deep 的「為什麼」— 完全新人才會問、卻常把資深的人考倒的基礎問題,本質是 first-principles 探針的偽裝:往下追到 OS / 網路 / 分散式原語為止,不接受「k8s 就是這樣設計的」。

| 形狀 | k8s 範例(菜鳥口吻) | 戳破的東西 |
|------|---------------------|-----------|
| 小孩追問式 why-chain | 「為什麼 Pod 重啟 IP 就變了?IP 不能固定嗎?」→ 接著「那為什麼?」一路追 | Pod IP ephemeral 的本質 |
| 天真但深(隱藏假設) | 「為什麼不能直接 `kubectl delete pod` 就好,它自己會回來啊?」 | controller reconcile vs 手動的差別 |
| 故意丟錯誤誘答 | 「那我把 Service 的 IP 寫死在程式裡不就好了?」 | ClusterIP/DNS/Endpoint 動態性 |
| 邊界天真問 | 「conntrack 是什麼?為什麼它會滿?滿了關我什麼事?」 | NAT 狀態表、第一性原理 |
| 比較分不清 | 「liveness 跟 readiness 我看起來一樣欸,差在哪?拿掉一個會怎樣?」 | 兩種 probe 的語義後果 |

優先拿本堂 step E 剛排的障 / step C keystone chunk 當題材(剛親手修好被弄壞的叢集,趁記憶最燙被菜鳥逼問「為什麼會壞」)。
