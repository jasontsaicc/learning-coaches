---
name: deep-dive-notes
description: 由淺到深講解一個技術主題，目標是大廠 DevOps/SRE 的深度：第一性原理 → 機制 → 取捨 → AWS 真實做法 → 規模化 → 故障與 on-call → 面試。產出 HTML artifact。所有 coach（k8s / sd / leetcode / terraform / ca）要產 HTML 頁面都走這個 skill。Use when the user types /deep-dive-notes <topic>, says eli5 太淺, asks to understand a topic deeply (原理、設計理念、業界/AWS 實務作法), or a coach needs an HTML page.
---

<!-- engine: standalone -->

# deep-dive-notes

Topic: $ARGUMENTS

## 讀者與目標
DevOps 工程師（Python / Shell / AWS / Linux / 網路基礎都會，不要解釋）。目標：大廠 DevOps/SRE 面試與實戰。
標準：讀完能在 design review 說出「為什麼這樣做、什麼時候會壞、AWS 上怎麼落地、規模大了要換什麼」。ELI5 等級的內容只留一張比喻圖。

心盲症：每一層都要有真的畫出來的圖（inline SVG 或 ASCII），連看不見的部分也要畫（空值、暫停狀態、被覆蓋前的舊值、封包沒到的那一段）。禁止「想像一下」。

ADHD：版面規則見下方「ADHD 版面」。chat 端一回合只給一張圖加一個問題。

## 路由
這是所有課程唯一的 HTML 頁面產生器。教學、出題、計分、寫 progress 仍歸各 coach（k8s-coach / sd-coach / leetcode-coach / terraform-coach / cloud-architect-coach）；coach 需要頁面時呼叫本 skill，並告知 coach 名（決定配色與存檔位置）。使用者直接呼叫時，依主題判斷屬於哪個 coach；都不屬於才用 `general`。

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

### 演算法題（leetcode-coach 呼叫時）

同樣七層，內容換成：

| 層 | 放什麼 | 預設 |
|---|---|---|
| 0 | 白話：這題在幹嘛，一句話加一張圖 | 展開 |
| 1 | 題型加 2 到 3 個秒認信號；暴力法長怎樣、為什麼慢（圖） | 展開 |
| 2 | 做法一步一步（圖，手動走一遍，無 code）；完整 code 逐行解釋；逐輪執行模擬表 | 圖展開，code 與模擬表摺疊 |
| 3 | 時間/空間複雜度，關鍵手法換掉了什麼；其他解法輸在哪 | 展開 |
| 4 | 這個 pattern 在真實系統哪裡出現（例：LRU → cache eviction）。沒有就一句帶過 | 展開 |
| 5 | 變形題與 follow-up | 摺疊 |
| 6 | 學員最可能犯的錯（從 `leetcode-coach/references/my-common-bugs.md` 撈）加 edge cases | 展開 |
| 7 | 口訣加模板；L6 面試逐字稿（說/想/寫，L4 vs L6 對照） | 摺疊 |
| 尾 | 「這次的釐清」：session 結束時補寫，格式 `✗ 我以為 / ✓ 其實是 / → 為什麼會搞混` | 摺疊 |

演算法題一次產出全部七層（不分批），學員先讀頁面再進對話。code 一律放 `<details>`，由學員決定何時展開。

## 節奏
預設分批產出同一個 HTML artifact（同一個檔案路徑重新 publish，URL 不變）：
1. 第一批：Layer 0–2。chat 裡問一個短問題，讓讀者用自己的話講 Layer 1 的核心限制。
2. 讀者回答後：先補他講錯的地方，再加 Layer 3–5。
3. 最後加 Layer 6–7。

- `$ARGUMENTS` 含 `all`：一次產出全部七層。
- 讀者說「從 N 開始」/「只要 N」：照做。

## ADHD 版面
規則改編自 `i-have-adhd` plugin（ayghri/i-have-adhd）。那個 skill 設了 `disable-model-invocation`，不能被其他 skill 呼叫，而且它管的是 chat 回覆，所以頁面版的規則寫在這裡。
- 頁首放進度條：`Layer 0 ✓ 1 ✓ 2 ● 3 ○ …`，加一句「讀完這頁你能 ___」。分批時每批都更新。
- 每層第一句是結論，接著是圖，最後才是說明。每層標預估閱讀時間（例：讀 3 分鐘）。
- 清單最多 5 項。超過就拆成「必看」和放進 `<details>` 的「之後再看」。
- 不放旁支：補充、歷史、冷知識一律收進 `<details>`。
- 頁尾放一個 2 分鐘內做得完的下一步（例：「回 chat 用一句話講 Layer 1 的限制」）。

## HTML 輸出
- 先 load `artifact-design`，再讀 `references/notebook-style.md`，照它的筆記風（霞鶩文楷、方格紙、螢光筆、貼膠帶的圖卡）和該 coach 的配色。
- 圖為主、字少。每層一段，標題寫層號和名稱。
- Layer 4 一定有 AWS 架構圖（SVG）和「服務 → 陷阱」表。Layer 5 一定有 evolution ladder 圖。（演算法題照上方對照表，不適用這條。）
- Layer 7 的 L4/L6 對照用 `<details>` 收起來，先讓讀者自己想。
- 每批 publish 後，把同一個 HTML 檔 `cp` 到 `../../portfolio/<coach>/notes/`（相對於本 SKILL.md 的實體目錄，即 learning-coaches repo 根目錄），覆蓋舊版（scratchpad 會隨 session 消失，學習地圖網站從這裡讀）。檔名照 `../../site/README.md` 的命名規則（例：`s40-pss-layers.html`、`day35-chat-system-layers.html`、leetcode 用 `<problem-slug>.html`），網站才會掛到對應 topic。`general` 不 cp。

## 主題頁面組（2026-10-29 學員拍板）
一個主題收尾時要有三種頁面，同一個檔名前綴（`../../site/README.md`），網站會掛在同一個 topic 下：

| 頁面 | 檔名 | 何時做 | 放什麼 |
|---|---|---|---|
| chunk 深入頁 | `<prefix>-<chunk>-layers.html` | 開課前預習（Layer 0–2），chunk 教完補滿 | 該 chunk 的七層。深入內容只住在這裡 |
| hub（主筆記） | `<prefix>-<topic>-hub.html` | 主題收尾 | 全貌圖；每個 chunk 一張圖 + 一句話 + 連結；錯題；面試重點。不複製 chunk 的深入內容（避免兩份不同步） |
| 面試頁 | `<prefix>-<topic>-mock-l6.html` | hub 之後 | 完整情境題 + 8 步：clarify → capacity → high-level → deep dive → 3AM → operate → cost → wrap。每步：面試官 / 想 / L6 怎麼說（`<details>` 收起）/ L4 vs L6 |

- hub 連到每個 chunk 頁與面試頁；面試頁連回 hub。
- 舊主題不回頭補。第一個範例：`day35-chat-system-hub.html`（收尾複習版，複製了較多 chunk 內容，之後的 hub 要更短）、`day35-chat-system-mock-l6.html`。

## 語言
繁體中文敘述，技術名詞保留英文。
