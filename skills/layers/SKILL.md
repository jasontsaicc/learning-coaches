---
name: layers
description: 由淺到深講解一個技術主題，目標是大廠 DevOps/SRE 的深度：第一性原理 → 機制 → 取捨 → AWS 真實做法 → 規模化 → 故障與 on-call → 面試。產出 HTML artifact。Use when the user types /layers <topic>, says eli5 太淺, or asks to understand a topic deeply (原理、設計理念、業界/AWS 實務作法).
---

<!-- engine: standalone -->

# layers

Topic: $ARGUMENTS

## 讀者與目標
DevOps 工程師（Python / Shell / AWS / Linux / 網路基礎都會，不要解釋）。目標：大廠 DevOps/SRE 面試與實戰。
標準：讀完能在 design review 說出「為什麼這樣做、什麼時候會壞、AWS 上怎麼落地、規模大了要換什麼」。ELI5 等級的內容只留一張比喻圖。

心盲症：每一層都要有真的畫出來的圖（inline SVG 或 ASCII），連看不見的部分也要畫（空值、暫停狀態、被覆蓋前的舊值、封包沒到的那一段）。禁止「想像一下」。

## 路由
主題屬於 k8s、system design、leetcode、AWS ProServe 面試演練 → 改用 k8s-coach / sd-coach / leetcode-coach / cloud-architect-coach。layers 只負責「把一個主題講透」，不出題、不計分、不寫 progress。

## 七層

| 層 | 名稱 | 必須回答 |
|---|---|---|
| 0 | 一張圖 | 一個比喻 + 一張圖。最多 3 句。 |
| 1 | 第一性原理 | 它解決什麼無法迴避的問題？受什麼物理/數學/經濟限制（光速延遲、CAP、磁碟 IOPS、成本）？拿掉它會怎樣？ |
| 2 | 機制 | 用真實名詞講運作。畫流程與狀態變化，附真實數字（latency、大小、timeout 預設值）。 |
| 3 | 取捨 | 為什麼這樣設計？被淘汰的替代方案輸在哪？付出什麼代價？ |
| 4 | AWS 怎麼做 | 對應的 AWS 服務與設定、架構圖、quota/限制、成本模型。每個服務附一個常見陷阱。非 AWS 主題就寫「生產環境怎麼部署」。 |
| 5 | 規模化 | Evolution ladder：小團隊 → 成長期 → 大廠，每一級換掉什麼、為什麼換。業界兩條常見路線比較。 |
| 6 | 故障與 on-call | 怎麼壞、會看到什麼（log、CloudWatch/Prometheus metric、指令輸出）、第一個查的指令、怎麼止血、SLO 怎麼定。有公開 postmortem 就引用（給名稱與連結），不確定就不引用。 |
| 7 | 面試 | 一題大廠會問的題目 + L4 回答 vs L6 回答對照（L6 多了什麼：取捨、數字、故障模式）。 |

規則：
- 每層明確連回上一層：「因為 Layer 1 的限制 X，所以 Layer 3 選了 Y，所以 AWS 上用 Z」。
- 事實要具體：服務名、參數名、預設值、數字。不確定的 AWS 參數或 quota 先查文件（WebSearch / WebFetch），查不到就標「需確認」，不要猜。
- 職場真實面：誰會為這件事吵架（Dev vs SRE vs 財務）、PR / design review 會被問什麼。放在 Layer 4–6 裡，一兩句就好。

## 節奏
預設分批產出同一個 HTML artifact（同一個檔案路徑重新 publish，URL 不變）：
1. 第一批：Layer 0–2。chat 裡問一個短問題，讓讀者用自己的話講 Layer 1 的核心限制。
2. 讀者回答後：先補他講錯的地方，再加 Layer 3–5。
3. 最後加 Layer 6–7。

- `$ARGUMENTS` 含 `all`：一次產出全部七層。
- 讀者說「從 N 開始」/「只要 N」：照做。

## HTML 輸出
- 先 load `artifact-design`，再套 memory 的 D 筆記風（霞鶩文楷、方格紙、螢光筆、貼膠帶的圖卡）。
- 圖為主、字少。每層一段，標題寫層號和名稱。
- Layer 4 一定有 AWS 架構圖（SVG）和「服務 → 陷阱」表。Layer 5 一定有 evolution ladder 圖。
- Layer 7 的 L4/L6 對照用 `<details>` 收起來，先讓讀者自己想。

## 語言
繁體中文敘述，技術名詞保留英文。chat 回覆結尾照 CLAUDE.md 附 Native English block。
