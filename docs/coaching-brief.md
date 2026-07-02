# Coaching Brief — 作戰手冊（S1–S36 蒸餾，2026-07-03）

> 給 coach 每場開場讀的檔案。`progress.md` 記錄「發生了什麼」，這份記錄「怎麼教這個學生才有效」。
> 由 36 場筆記 + Mistake Registry + Scorecard History 全量分析蒸餾。證據都標 session 編號。

**一句話總結：** 知識吸收管道（推導、比喻、動手）已經很順；所有 chronic 弱點全在「輸出習慣與壓力反應」層（講不全、不收尾、見 2^n 就縮、要提示），而且每一個都已有被驗證有效的對治手法。執行紀律比教學創新重要。

---

## 五個 chronic 弱點與對治協議（按優先序）

### 1. 給結論不給論證（S8→S36 主線）
- 診斷：把答案當通關密語，說出名詞就等確認。**不是知識缺口**：S31 要提示的內容暖身剛講過；S36 被追問後能完整補足。
- 規律：地基題做得到（S27/S28 連兩場 5/5），**新題型必回退**（S31 transfer、S36 首場 bar-raiser）。
- 協議：每個設計決策要一口氣講「選什麼 + why + 反面代價」才計分。初期給四格填空 scaffold（S33 驗證有效）再漸撤。**新 archetype 首場 drill 明示為習慣訓練場、第二場才計分。** Bar-raiser 追問當未達標的後果，不當教學手段（他自己要求的加壓，S36 起生效）。

### 2. Operational 監控盲點（S26/S30/S34/S36 四次掛蛋）
- 診斷：知識在（本業 DevOps；S12 能畫 3AM debug tree、S35 PoC 主動建監控表），**retrieval framing 問題**：監控知識掛在「救火」腳本，沒掛在「設計收尾」腳本。提醒一次只維持 1-2 場（S27/S28 ✅ 之後又掉）。
- 協議：drill 不喊結束、沒主動講監控句 = 該項直接 ❌，不提醒。開場預告一次「收尾是你的責任」之後全靠他。Reframe 話術：「這系統上線後，半夜 3 點什麼會 page 你？」調用 on-call 肌肉。追蹤連續達成場數，目標 3 連。

### 3. Capacity 2^n 凍結（S34、S36）
- 診斷：不是數學能力（Day 2 通過、S24/S33 都算對），是「指數記號」單點恐懼 + drill 壓力下快速棄權。兩次凍結都在 drill，從未在教學段發生。
- 協議：錨點卡固定五條：62≈2⁶、2¹⁰=1024、2^n=1024×2^(n-10)、2³⁰≈10億、86400≈100K。規則：不准說放棄，必須先寫下拆解式。每場 drill 塞一題 2^n 心算，3 連無凍結才撤。預測觸發點：CMS 參數（Day 56-57）、chat fanout、geo cell 數。

### 4. 主動要提示而非先嘗試（與 #1 同根）
- 診斷：verification-seeking 不是 knowledge-seeking，不耐受持球狀態。S34 起未再出現，但需持續。
- 協議：一律回「先丟一個答案」；只給 thinking scaffold（結構不給內容，S32 驗證）；善用他 hint-response 強項——**把提示換成反問挑戰，他吃挑戰不吃提示**（S31/S34 被 challenge 一次即自修正）。

### 5. 術語滑動（兩種機制，分開治）
- (a) **語音近似對**（L2 語音編碼弱）：least robin、offline/offset、most-least-excely、CAP 字母掉。概念通常對、純標籤滑。治法：口頭念全名 + 成對術語對照表。與英文拼字錯誤同源（dulicate、prosses、mantion）。
- (b) **強先驗劫持**（回退聚集的真正機制）：base62→「hash」回退兩次、都在 resolved 後約 2 天（S32→33、S34→35）；Redis 當 truth 回退兩次；traceroute 當 tracing。共通點：新概念旁邊站著表面相似的舊 DevOps 直覺。治法：resolved 不可只憑口頭答對，必須 (1) 對照表 (2) 機制數字走一遍 (3) **+2 天窗口主動 re-check**。新主題備課先預掃「哪個新概念會被他的舊直覺劫持」。已知未來雷點：Kafka consumer group vs SQS、geohash vs hash、CRDT vs merge。

---

## 未命名 pattern 檢查表（分析新發現）

| Pattern | 證據 | 對治 |
|---------|------|------|
| **軸摺疊**：兩個獨立維度共現時融合成一軸 | 6+ 次：SQL/NoSQL×B-tree/LSM、O(N)儲存×O(N²)廣播、讀寫比×產量、salt×counter、sticky×Redis store、DECR×idempotency | 新主題凡有成對概念，讓他自己畫雙軸表擺放項目；一講成一軸立刻停下拆軸 |
| **危險感沒有機制**：聞得到風險但講不出失敗時間線 | clock skew「只覺得危險」(S36)、fetch-on-miss 隱藏前提 (S31) | 逼他用具體數字走一遍 failure timeline，每次都通（S36 毫秒數字、S31 一戳即通） |
| **機率/計數論證入口窄、通了遷移力強** | Quorum 鴿籠卡兩次、Bloom 全亮陷阱；但通了之後零提示連 Gossip | 實物比喻當入口（鴿籠/燈泡/蓋章），親手踩一次陷阱 |
| **當場 🟢 ≠ 留得住** | WR1: Caching 教完 🟢 實測 0/4；WR3: CAP 一週衰退 | 信 Leitner box 不信當場表現；危險感型概念複習要求敘述 failure timeline 而非定義 |

---

## 有效手法快取（直接複用）

- **比喻家族**（結構同構的日常實物才有效）：日期格式→bit ordering、鴿籠→quorum/過半票、銀行號碼牌→counter vs hash、集點卡→lazy refill、燈泡蓋章→Bloom、Tokyo/London→ordering、帶位員→LB、摩斯密碼→encoding、考試分數→SLI/SLO/SLA。
- **Scaffold 類型**：四格填空（講全論證）、thinking scaffold（卡住時）、拆次方（capacity）、回答模板「I'd pick X over Y because [gain], the cost is [trade-off]」。
- **讓 resolved 留住的三要素**（齊備幾乎不回退）：數字走機制 timeline + 對照表釘死相鄰概念 + 之後在新設計題實際調用一次。只口頭講對一次的必回退（base62 花了 4 輪才焊死）。
- **PoC = 最高強度固化**：「從我相信變程式證明」（S35 失敗注入仍 0 碰撞）。堅持手打，附帶 Go 語感。
- **被質疑後自修 > 直接糾正**：一句「半夜 Redis 重啟呢？」勝過整段講解（S34）。

## 無效手法（別做）

機械式 gate 標籤（Recall/Transfer 點名，S36 學生反感已收回）／純理論深度（vnode 數學，催生 depth-ceiling）／抽象描述不給數字／英文為主模式（S27 閱讀疲勞切回繁中）／聽過一遍就往前走。

## 強項槓桿（用強打弱）

1. **約束謎題自我推導**（最強）：S24 自推 stampede→CAP 鏈、S36 自推 Snowflake 三段。新主題一律用約束謎題開場（KGS 橋接法已驗證）。
2. **Security/攻擊者直覺**：S36 零提示 enumeration 洩漏營業額。可當監控盲點的橋（on-call/攻擊者視角 reframe）。
3. **跨主題連結力**：local Bloom→Gossip 零提示；自己歸納 lazy 哲學家族。
4. **誠實後設認知**：自己要求加壓、點名模糊處要求重講、不裝懂。
5. **回血能力**：Caching WR1 0/4 → WR4 6/6。

## 語言策略

繁中推理 + 英文 one-liner 口頭輸出雙軌（S27 定型）。English Polish 照舊。One-Liner Library（18 條）是現成口說素材，每場複習抽 2 條口頭背。壓力下英文詞彙 retrieval 會失敗（S19 想不起 encryption），one-liner 背誦是最便宜的補法。不逼回英文為主。
