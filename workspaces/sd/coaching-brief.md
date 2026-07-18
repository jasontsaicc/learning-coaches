# Coaching Brief — 作戰手冊（S1–S36 蒸餾，2026-07-03）

> 給 coach 每場開場讀的檔案。`progress.md` 記錄「發生了什麼」，這份記錄「怎麼教這個學生才有效」。
> 由 36 場筆記 + Mistake Registry + Scorecard History 全量分析蒸餾。證據都標 session 編號。

**一句話總結：** 知識吸收管道（推導、比喻、動手）已經很順；所有 chronic 弱點全在「輸出習慣與壓力反應」層（講不全、不收尾、見 2^n 就縮、要提示），而且每一個都已有被驗證有效的對治手法。執行紀律比教學創新重要。

**更深的診斷（S37 meta review）：** 五個弱點裡有四個（#1 結論不給論證、#3 capacity 凍結、#4 要提示、以及「危險感沒機制」pattern）共用同一底層機制 — **壓力下只輸出有把握的「結論」，把沒把握的「推導」吞回去或棄權**。教學段（無人盯）他每次都能推導；drill 段（被盯著）品質斷崖下跌。同一顆腦袋同一份知識，差別只在「有沒有人在看」。所以不是五套病，是一個 confidence-gating 輸出習慣戴五張面具。而面試官買的是推導不是答案 → 他正好把最值錢的藏起來。

**評分錨（2026-07-03，學生拍板）：tier-1 strong-hire bar。** 學生目標 = tier-1 大廠 offer，明確要求最嚴厲模式：不聽好聽話、每場打當前最弱點。落地規則：(1) scorecard 分數照課表機制打，但 feedback 必須指出距 tier-1 bar 的差距（「這在 Google 是 no-hire，因為…」）；(2) drill 壓力預設 L3 adversarial，不分 phase；(3) 失敗點不安慰帶過，直接變成下一輪 drill 目標；(4) safety valve 保留（2 次卡死 → 縮小問題再加壓）— 反脆弱是漸進加壓，不是壓斷。

**教學模式決定（S37，學生拍板）：轉 execution-heavy。** Phase 2 之後已無知識問題、只有執行問題；繼續 march 新 archetype = 餵已強的吸收肌肉、餓弱的輸出肌肉（drill 永遠是 A→H 最趕的最後一步）。改為「暫停新 archetype 幾場，插 Drill Gauntlet 純加壓 mock，把輸出習慣練到自動化」。學生自選首攻 **#1 結論不給論證**。詳見下方 [Execution-Heavy Mode]。

**Sprint overlay 生效中（2026-07-17 起，詳見 curriculum-plan.md 的 Conditional Sprint overlay）：** 學員已投遞外部 consultant 職缺，等待邀約期間每場 drill 加兩層外皮 — (1) 元件收尾追問 AWS 服務映射 + Well-Architected 支柱詞彙；(2) 題目用產業客戶情境開場（半導體/製造/FSI/公部門，考 clarify 約束的 discovery 流程）。佇列與 execution-heavy 三指標不變。

---

## 五個 chronic 弱點與對治協議（按優先序）

### 1. 給結論不給論證（S8→S36 主線）
- 診斷：把答案當通關密語，說出名詞就等確認。**不是知識缺口**：S31 要提示的內容暖身剛講過；S36 被追問後能完整補足。
- 規律：地基題做得到（S27/S28 連兩場 5/5），**新題型必回退**（S31 transfer、S36 首場 bar-raiser）。
- 協議：每個設計決策要一口氣講「選什麼 + why + 反面代價」才計分。初期給四格填空 scaffold（S33 驗證有效）再漸撤。**新 archetype 首場 drill 明示為習慣訓練場、第二場才計分。** Bar-raiser 追問當未達標的後果，不當教學手段（他自己要求的加壓，S36 起生效）。
- **關鍵機制（S37 新發現）：現行 drill 格式正在獎勵這個壞習慣。** 迴圈是「裸結論 → coach 追問 → 他補完 → 拿到分」＝ 大腦學到「terse-first 沒懲罰，反正追問會救我」。但真面試裡弱面試官不追問，signal 靜默流失。**斷這個迴圈的三條硬規則（execution-heavy 生效）：**
  1. **第一句就是評分句** — 評「第一次開口」，不是被追問後的版本。追問後才補完 = 那項不給分、整句重講。No partial credit。
  2. **裸結論直接打回，不接「為什麼？」**（那是獎勵）。改說「那是結論不是答案，重講，一口氣帶 why + 反面代價」。追問＝獎勵，打回＝懲罰，方向要反過來。
  3. **追蹤 unprompted-complete rate**（不追問就講完整的比例），這才是要動的數字，不是 drill 總分。句型當反射練：`I'd pick X over Y because [gain], the cost is [trade-off]`。

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

## Execution-Heavy Mode（S37 起生效，直到 unprompted 三項指標各 3 連達標）

**前提：** 知識夠了，缺的是「被盯著時穩定倒出來」的次數。教學重心從 acquisition 轉 execution。

**節奏：** 暫停「每場一個新 archetype」。改成 drill 為主。新 archetype 只在 Gauntlet 之間穿插、且只當「新的加壓舞台」用，不當學習目標。

**保底順序反轉（2026-07-07 跨專案過程分析）：** 時間不夠時先跑輸出段（drill、收尾儀式、逾期複習），新內容順延。歷史病灶是 Step D PoC 常跳、Step F drill 永遠最趕；輸出既然是瓶頸，就不准再讓輸出段當緩衝墊。一場只剩 20 分鐘就只做冷測與 drill，不開新 chunk。

**Drill Gauntlet（新 session 型態）：**
- 一整場不教新東西，連跑 2-3 場 bar-raiser mock，混合已學舊題（URL Shortener / Session Store / Rate Limiter / Snowflake / Distributed Cache）。
- 唯一目標：把「第一次開口就附論證 + 主動收尾監控 + capacity 不凍結」練成反射。
- 用上面 #1 的三條硬規則（第一句評分 / 裸結論打回 / 追蹤 unprompted rate）。

**三個要動的 unprompted 指標（每場記，目標各 3 連）：**
| 指標 | 定義 | 現況 |
|------|------|------|
| unprompted-argument | 不追問就講「選什麼+why+反面代價」的決策比例 | S8→S36 主線弱點，地基題可、新題回退 |
| unprompted-ops | 設計收尾不提醒就主動講監控句 | 4 場掛蛋（S26/30/34/36），現行 fix 無效 |
| no-freeze-capacity | 遇 2^n 不棄權、先寫拆解式 | S34/S36 兩次凍結 |

**監控焊進框架（修 #2 的新法，取代「純 ❌ 不提醒」）：** 4-step 升級成「4-step + 收尾儀式」。每個設計結尾強制跑 **3AM page test**：上線後半夜什麼會 page 我？SLI 是什麼？dashboard 三張圖？當硬性關卡，不是加分項。理由：他的 4-step 已自動化但框架有洞，監控飄在 Step 4 可有可無 → 補成第 5 步儀式，靠框架肌肉帶出來，不靠他記得。

**+2 天 re-check 格（修 #5(b) 強先驗劫持）：** base62→hash 兩次回退都在 resolved 後約 2 天，Box 1 隔天複習太快（假陽性）。強先驗劫持型概念（base62、未來 Kafka consumer group vs SQS、geohash vs hash、CRDT vs merge）進獨立「+2 天」複習格，不走一般 Leitner。

---

## 未命名 pattern 檢查表（分析新發現）

| Pattern | 證據 | 對治 |
|---------|------|------|
| **軸摺疊**：兩個獨立維度共現時融合成一軸 | 6+ 次：SQL/NoSQL×B-tree/LSM、O(N)儲存×O(N²)廣播、讀寫比×產量、salt×counter、sticky×Redis store、DECR×idempotency | 新主題凡有成對概念，讓他自己畫雙軸表擺放項目；一講成一軸立刻停下拆軸 |
| **危險感沒有機制**：聞得到風險但講不出失敗時間線 | clock skew「只覺得危險」(S36)、fetch-on-miss 隱藏前提 (S31) | 逼他用具體數字走一遍 failure timeline，每次都通（S36 毫秒數字、S31 一戳即通） |
| **機率/計數論證入口窄、通了遷移力強** | Quorum 鴿籠卡兩次、Bloom 全亮陷阱；但通了之後零提示連 Gossip | 實物比喻當入口（鴿籠/燈泡/蓋章），親手踩一次陷阱 |
| **當場 🟢 ≠ 留得住** | WR1: Caching 教完 🟢 實測 0/4；WR3: CAP 一週衰退 | 信 Leitner box 不信當場表現；危險感型概念複習要求敘述 failure timeline 而非定義 |
| **概念單鉤子（情境綁定）**：概念只掛在初次學習的情境，換場景撈不出 | Bloom S39：只掛「快取穿透」鉤子，LSM/SSTable 場景「沒有印象」+ FP/FN 嚴重性講反，Box 3→1；operational 知識掛「救火」腳本不掛「設計收尾」腳本，同一機制 | 新概念收尾必問「這概念還會在哪兩個場景出現?」多鉤子入庫；複習出題輪換情境，不用原始學習情境考 |

---

## 有效手法快取（直接複用）

- **比喻家族**（結構同構的日常實物才有效）：日期格式→bit ordering、鴿籠→quorum/過半票、銀行號碼牌→counter vs hash、集點卡→lazy refill、燈泡蓋章→Bloom、Tokyo/London→ordering、帶位員→LB、摩斯密碼→encoding、考試分數→SLI/SLO/SLA。
- **Scaffold 類型**：四格填空（講全論證）、thinking scaffold（卡住時）、拆次方（capacity）、回答模板「I'd pick X over Y because [gain], the cost is [trade-off]」。
- **讓 resolved 留住的三要素**（齊備幾乎不回退）：數字走機制 timeline + 對照表釘死相鄰概念 + 之後在新設計題實際調用一次。只口頭講對一次的必回退（base62 花了 4 輪才焊死）。
- **PoC = 最高強度固化**：「從我相信變程式證明」（S35 失敗注入仍 0 碰撞）。堅持手打，附帶 Go 語感。
- **被質疑後自修 > 直接糾正**：一句「半夜 Redis 重啟呢？」勝過整段講解（S34）。
- **架構圖先行（S44 學生自報+證據支持）**：機制類 drill 先把架構圖擺上桌再開問，drill＝指著圖講。證據：S42/S44 兩次純文字模式在同一主題（session store 殭屍/3AM）交白卷，S44 圖畫出後學生立刻問出理解型問題＋產出當日最佳英文句。填空給的是句子骨架，他缺的是空間骨架。複測形式改「白板默畫」（重畫圖驗留存，k8s coach s16 同款），取代文字填空。純詞彙映射層（migration 7 Rs 這類）維持表格式，不需圖。
- **Real-World Grounding 段（S41 學員點名「非常有幫助」並拍板為固定元素）**：每主題 gate 過後接「業界實際怎麼做」六格（演化梯／岔路／架構圖／工具對照含坑／職場攻防／面試一句）。對他特別有效的機制：把新概念掛回 DevOps 既有肌肉（Global Tables=LWW、denylist=CRL、pull=Prometheus scrape），正好對治「概念單鉤子」pattern。規格見 teaching-elements.md。

## 無效手法（別做）

機械式 gate 標籤（Recall/Transfer 點名，S36 學生反感已收回）／純理論深度（vnode 數學，催生 depth-ceiling）／抽象描述不給數字／英文為主模式（S27 閱讀疲勞切回繁中）／聽過一遍就往前走/**盲測或 drill 不給完整題目敘述**(S41 兩度炸鍋:任何 recall/drill/mock 開場必附完整面試題情境,clarify 要用具體數字回,考的是設計不是背題)。

## 強項槓桿（用強打弱）

1. **約束謎題自我推導**（最強）：S24 自推 stampede→CAP 鏈、S36 自推 Snowflake 三段。新主題一律用約束謎題開場（KGS 橋接法已驗證）。
2. **Security/攻擊者直覺**：S36 零提示 enumeration 洩漏營業額。可當監控盲點的橋（on-call/攻擊者視角 reframe）。
3. **跨主題連結力**：local Bloom→Gossip 零提示；自己歸納 lazy 哲學家族。
4. **誠實後設認知**：自己要求加壓、點名模糊處要求重講、不裝懂。
5. **回血能力**：Caching WR1 0/4 → WR4 6/6。

## 語言策略

繁中推理 + 英文 one-liner 口頭輸出雙軌（S27 定型）。English Polish 照舊。One-Liner Library（18 條）是現成口說素材，每場複習抽 2 條口頭背。壓力下英文詞彙 retrieval 會失敗（S19 想不起 encryption），one-liner 背誦是最便宜的補法。不逼回英文為主。
