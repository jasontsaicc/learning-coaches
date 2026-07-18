# Phase Gates

The engine enforces the 3-attempt cap and the failure protocol. This hook defines what
"pass" means for each phase: a concrete pass condition tied to observable student
behavior, not a time-on-task target. One section per curriculum phase.

## P0 意識定向 Gate

Pass condition:progress file 裡有一份 personalized thread-pull list(由 warm-up 的 resume
thread-pull 練習彙整而成),而且學員不看筆記就能講清楚 loop 的形狀:phone screen 跟 full
loop 的差別、full loop 約一半分數壓在 LP 上、每個面試官都打 LP。講不出這個形狀,代表還沒
搞清楚在測什麼,不能進 P1。

Suggested gate task(engine 可跨 attempt 換問法):「phone screen 跟 full loop 差在哪?這個
loop 最容易被技術強的人低估的一條線是什麼?」聽學員有沒有自己點出 LP 的權重。

## P1 Networking Gap-Scan Gate

Pass condition:gap-scan 十六題跑完,每一題標了 `pass` / `shaky` / `hole`;而且每一個
`shaky` 或 `hole` 的題目,要嘛在後面的 session 補完機制、重測過(retest 拿到 `pass`),
要嘛明確 park 起來並在 progress file 寫下 park 的理由。補完機制但沒重測不算過。

Suggested gate task:從當初標成 `shaky` / `hole` 的題目裡挑,換個情境重問,聽學員這次自己
講不講得到 "listen for" 那行的機制。

## P2 Migration Gate

Pass condition:對一個沒看過的 mini-case(coach 當場變化,不是 CASE-1..6),學員給得出三階段
plan(Assess / Mobilize / Migrate & Modernize)、並對每個 workload 選一個 R 且理由扣回這個
workload 的限制(licensing、耦合度、時程、成本),達到 tier-2 scorecard 的 pass。tier-2 的
migration judgment 維要過:選 R 有 workload-specific 的理由,而且不用追問就自己點出風險
(downtime、資料一致性、rollback)。

Suggested gate task:給一個兩三個 workload 的短 brief(例:一台吃授權的舊 DB 加兩台無狀態
web),要學員切 wave、逐 workload 說 R 與 why,再丟一個 cutover 的 follow-up 逼他守住。

## P3 Case Drills + Mocks Gate

Pass condition:兩場全英文 full mock 都達到 coach scorecard 的 hire bar,一場是 migration
case、一場是 hybrid-networking case,兩場都取自或改編自 CASE-1..6 並換過數字。hire bar 看
tier-3:除了前面的維,consultant delivery 要過:答案有結構、英文撐得住一通客戶電話、被反駁時
走 acknowledge → quantify → offer → land on customer choice 四步、交卷前自己跑一遍
Well-Architected self-review。

Suggested gate task:抽一個 CASE(migration 類)加一個 CASE(hybrid-networking 類),把數字
換掉當 mock 題,逐條對 Hire bar 打勾,再用該 case 的 Follow-up 收尾。

## Sidecar: Linux Interview Bank Gate

Pass condition:Priority 0 兩題與 Core 20 全部答得到 mechanism layer(講得出底下怎麼動,不是
背名詞);其中兩題 Priority 0(IRQ/softirq、static vs shared library)要間隔重測兩次,兩次都
達 mechanism layer 才算收。

Suggested gate task:Priority 0 兩題間隔重問(不是連兩次),Core 20 隨機抽問,聽學員這次是不是
自己講出機制、而不是想起上次被講過的答案。
