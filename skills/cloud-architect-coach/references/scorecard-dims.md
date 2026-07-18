# Scorecard Dimensions

These dimensions stack on the engine's Tiered Scorecard frame (defined in ENGINE.md).
The 60% pass threshold and the cumulative-tier structure are the engine's and are not
redefined here. Each tier adds dimensions on top of all previous tiers; the primary
dimension is present at every tier. Tiers map to curriculum phases: Tier 1 = P0-P1,
Tier 2 = P2, Tier 3 = P3.

## Primary (always-on) dimension

**Trade-off tied to constraint:學員推薦一個做法時,講的是一條對著客戶限制的取捨,不是報一個服務名。**

Pass:理由扣回客戶講出來的限制,並帶出這個選擇放棄了什麼。例:「peering 到第三個
VPC 就失去 transitive routing,所以用 TGW」。

Fail:只丟服務名或結論。例:「用 TGW」。答案正確但講不出為什麼、代價是什麼,這一維不過。

這一維在每個 tier 都在。它是顧問職的底層訊號:客戶付錢買的是判斷,不是名詞。

## Tier 1 (P0-P1) dimensions

1. Trade-off tied to constraint(primary)
2. **Mechanism accuracy**:networking 的答案要講到封包 / DNS / TLS 這一層的行為,不停在
   服務名。判準對到 `references/gap-scan-aws-networking.md` 每題後面的 "listen for" 那行:
   那行列的機制,學員要自己講出來才算數(例:Connection Refused = 活著的主機回你 RST,
   Timeout = SG/NACL 靜默丟包)。

## Tier 2 (P2): adds migration judgment

3. **Migration judgment**:對著一個 workload 選對那個 R,理由是這個 workload 的限制
   (licensing、耦合度、時程、成本),不是背 7R 的定義。

Pass:選 R 有 workload-specific 的理由,而且不用 coach 追問就自己點出風險:downtime、
資料一致性、rollback 怎麼辦。

Fail:選了 R 但理由通用、換個 workload 也照抄;或風險要被問才想到。

## Tier 3 (P3): adds consultant delivery

4. **Consultant delivery**:答案能像對客戶交付一樣講出來。四個一起看:

- 答案有講明的結構(先講什麼、再講什麼),不是想到哪講到哪。
- 英文清楚到能撐一通客戶電話,對事不對人。
- 反對客戶時走 pushback 的四步,見 `teaching-elements.md` topic 7:acknowledge →
  quantify → offer → land on customer choice,順序不能亂,不硬吵也不照單全收。
- 交卷前自己跑一遍 Well-Architected self-review,對著五大支柱抓出自己答案最痛的兩個洞,
  尤其 cost 跟 operational excellence 這兩個白板上最常漏的。
