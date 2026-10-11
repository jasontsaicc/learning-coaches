# 2026-10-11 K8s deep-dive 筆記工作紀錄

用 `deep-dive-notes` skill，依 `workspaces/k8s` 的 progress、mistake-notes、session log
與 `skills/k8s-coach/references/` 產出 HTML 筆記（七層：圖 → 原理 → 機制 → 取捨 → AWS →
規模化 → on-call → 面試），筆記風照 skill 的 `references/notebook-style.md`。

## 完成

| 範圍 | 檔案（`portfolio/k8s/notes/`） | 掛載 |
|---|---|---|
| 章節 P0–P6（8 份） | `p0-chapter-*.html` … `p6-chapter-*.html` | 各 phase |
| P0 topic（4 份） | `p0-reconcile-loop.html`、`p0-apiserver-request-chain.html`、`p0-etcd-raft.html` | P0 phase（無 Mastery 行） |
| | `s10-apply-to-running.html`、`s25-declaration-vs-executor.html` | 各自 topic |
| P1 topic（5 份） | `s6-container-namespace-cgroup.html`、`s6-probe.html`、`s6-deployment-rollout.html`、`s10-resource-qos-oom.html`、`s26-pid1-signal.html` | 各自 topic |

- P0–P2b 章節有「我的錯題軌跡」，取自 Mistake Registry 的改寫，不貼 session log 原文。
  P3 部分取自 kubeadm lab（s41–s44）；P4–P6 是預習頁，P6 用的是輸出 pattern 卡。
- story-bank、career 內容不進筆記（網站不得顯示）。
- 章節表的「topic 深入」欄已連到對應筆記；P2a 以後仍標「待寫」。

## 網站變更：筆記可指定單一 topic

`s<N>-` 前綴會掛到同 session 的所有 topic，而 9 個 session 被 2–3 個 topic 共用。
改為 HTML 筆記可寫 `<meta name="topic" content="<Mastery 完整 label>">`，優先於檔名規則；
label 對不到時 build 失敗。改動在 `site/build.py` 的 `note_target()`，
`site/test_build.py` 加了正反兩個 case，`site/README.md` 掛載表加一列（commit `534c853`）。

## 驗證

- `./scripts/lint-all.sh` ALL PASS；`python3 site/build.py` 成功。
- 從 `site/dist/data.json` 確認：7 個 meta 筆記各只掛在自己的 topic；
  同 session 的其他 topic（例 s10 的 P2a 全鏈）沒有被掛上。
- 引用的公開事故已查證原文或可靠轉述：OpenAI 2024-12、Reddit Pi-Day 2023、
  Slack 2021-01、Tesla/RedLock 2018、2i2c cgroup v2 OOM。
- 未做瀏覽器截圖檢查；SVG 在手機寬度可能有標籤重疊。

## 已知限制

- 少數預設值依記憶撰寫、未逐一對文件：workqueue 退避 5ms–1000s、
  `--concurrent-replicaset-syncs` 5、ALB healthy threshold 5、controller-manager `--kube-api-qps` 20。
- 每份筆記都是獨立 HTML（約 20–45 KB），CSS 重複；改版要逐份重產。
- claude.ai artifact 版本與 repo 檔案是兩份；repo 是網站的來源。

## 下一步

1. 使用者先在學習地圖看過 P0、P1 的實際畫面，回饋版面、深度、長度。
2. 依回饋續寫 P2a topic（7 個），再 P2b。
3. PID 1、probe 兩份的「下次抽考題」可交給 k8s-coach step A 使用。
