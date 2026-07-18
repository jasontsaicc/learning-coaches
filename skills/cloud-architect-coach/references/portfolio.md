# Portfolio

## Workspace Directory

進度檔、盤點紀錄與 in-progress 練習都放在:

```
${CLAUDE_SKILL_DIR}/../../workspaces/ca/
```

這個目錄是 git-tracked 學習狀態,跨機器同步:每堂課後 commit + push,開課前 pull。內容:

- `progress.md`:engine 的進度檔。Schema engine-owned,定義在 `engine/PROGRESS-SCHEMA.md`,本 coach 不重定義。domain registry(term/command)若要開,沿用 schema section 7 的 registry 欄位。
- gap-scan 紀錄:P1 十六題的盤點結果,每題標 `pass` / `shaky` / `hole`(題庫在 `references/gap-scan-aws-networking.md`)。`shaky`/`hole` 的重測結果也記在這,phase gate 對照。
- thread-pull list:warm-up 的 resume thread-pull 練習彙整成的清單(履歷每行預測會被追問什麼)。往下餵 linux-interview-bank 的練習優先序。
- mock scorecards:每場 case mock 與 full mock 的 coach scorecard 逐場紀錄(維度見 `references/scorecard-dims.md`),用來看 hire bar 的趨勢。

## Artifacts

清得過 quality bar、值得留下的產出:

- 寫過 mock review 的 case 書面答案:mock 講完、拿 coach scorecard 對過弱點後改寫定稿的版本,不是初稿。
- final pre-interview one-page crib:面試前最後一張紙,把 thread-pull list、parked holes(盤點時沒補完、決定先擱著的洞)、weak-point retest log(補完機制重測拿到 `pass` 的紀錄)收斂成一頁。

Weekly Review 的 artifact audit(engine)對照這兩項:該有的不在,就是該補的債。
