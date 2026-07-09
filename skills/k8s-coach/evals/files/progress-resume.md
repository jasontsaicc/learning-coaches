# progress

<!-- Eval fixture: mid-P1 student with a live breakpoint. Engine schema (engine/PROGRESS-SCHEMA.md). -->

## Meta

- session_count: 4
- last_weekly_review: 0
- last_session_date: 2026-06-15
- warm_up_classification: mid

## Current Session breakpoint

P1, step C, chunk 3 (probe), next: 釐清 liveness vs readiness 語意差異(失敗各自會怎樣),然後跑 readiness 失敗的 chaos drill(step E,故意把 probe 路徑設錯);probe-lab 上次卡在「為什麼 readiness 一直 fail」未找到根因。

## Phase status

- P0 心智模型: gate-passed
- P1 核心物件 + 容器底層: in-progress(chunk 3 probe 進行中)
- P2a 之後: not-started

## Mastery

- P0 apply→Running control flow: med (s3)
- P1 container/namespace/cgroup: med (s4)

## Scorecard history

- 2026-06-15 | step G (s4, tier 1) | 2/3 | 用詞精準度 | 自己推出 probe 需要獨立於 app 邏輯 | coach

## Mistake Registry

- 2026-06-15 | probe 語意 | 以為 readiness 失敗也會重啟 container | 兩種 probe 失敗後動作不同(重啟 vs 切流量) | unresolved | 3 | 2026-06-18 | 1
  - 備註:liveness 失敗 → kubelet 重啟 container;readiness 失敗 → 從 Service endpoints 移除,不重啟。還沒搞懂 initialDelaySeconds / periodSeconds 怎麼影響「重啟風暴」。

## Spaced-repetition queue

- term:probe | term | 3 | 2026-06-18(今天到期)| active
- term:endpoint | term | 3 | 2026-06-18(今天到期)| active
- term:kubelet | term | 3 | 2026-06-18(今天到期)| active
- mistake:probe-語意 | mistake | 3 | 2026-06-18 | active

## Curiosity branch

(none)

## Domain registries

- `term-registry.md`:3 張卡(probe / endpoint / kubelet),今天到期要抽考。

## Examiner ledger

(empty)
