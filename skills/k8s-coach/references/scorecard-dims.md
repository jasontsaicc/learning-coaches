# Scorecard Dimensions

These dimensions stack on the engine's Tiered Scorecard frame (defined in ENGINE.md).
The 60% pass threshold is the engine's and is not redefined here. Each tier adds
dimensions on top of all previous tiers; the primary dimension is present at every tier.

## Primary (always-on) dimension

**能講清楚底層原理(不是「會不會配 YAML」)。**

Pass:能把機制講到底層依據(OS/網路/分散式/控制理論),說出「為什麼是這樣設計」。
Fail:YAML 配得出來、流程背得出來,但答不出「為什麼」或講錯底層機制。

**Rubric note(一句話精準版)**:複習抽考與 gate 的 pass 要求收一句精準收尾(例:「kube-proxy 只寫規則、kernel 搬封包」),不是方向對就好。說不出精準版 = 半過,拉近期重測。這條對治「精度衰減」(講對過的東西回測時滑掉)。

## Tier 1 (P0-P1)

Dimensions in use:
1. 能講清楚底層原理(primary)
2. 理解內部機制
3. 能用自己的話解釋

## Tier 2 (P2a-P3)

Adds: **故障排除速度 (MTTR)** — SRE 面試核心訊號。

MTTR = 從現象到定位根因的**回合數與方向正確性**(第一個排查指令選得對嗎),不是分鐘數。對應 step E Chaos Drill 的限回合 debug。

## Tier 3 (P4+)

Adds: **可觀測性設計** 與 **能定義 / 解讀 SLO**。

Pass:能為服務挑對 SLI、定出合理 SLO,並解讀 error budget 的行動含義。
Fail:能背三本柱名詞但設計不出對應到業務的量測。

## Feedback Footer

每次 scorecard 後固定附:

```
💡 最該改進:[一個具體可行的建議]
🌟 最佳時刻:[一個做得好的點]
```
