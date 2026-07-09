# Day 02: Back-of-Envelope Estimation

> Status: ✅ Completed

---

## 📝 One-liner

Back-of-envelope estimation 讓你用簡單的數學快速算出系統的 QPS 和 Storage，用數字驅動設計決策而不是憑感覺。

---

## Key Concepts

### 1. Powers of 2 — 資料大小單位

每加 10 次方，跳一個單位：

| Power | 值 | 單位 |
|---|---|---|
| 2^10 | ~1 Thousand | 1 KB |
| 2^20 | ~1 Million | 1 MB |
| 2^30 | ~1 Billion | 1 GB |
| 2^40 | ~1 Trillion | 1 TB |

常見資料大小：

| 東西 | 大小 |
|---|---|
| 一則 Tweet（280 字） | ~300 Bytes |
| 一張壓縮照片 | ~300 KB |
| 一分鐘 720p 影片 | ~5 MB |

### 2. Latency Numbers — 延遲量級

| 操作 | 延遲 | 比喻 |
|---|---|---|
| RAM access | ~100 ns | 走到隔壁房間 |
| SSD random read | ~100 μs | 走到隔壁棟大樓 |
| 同機房網路 round trip | ~0.5 ms | 走路到對面街 |
| HDD seek | ~10 ms | 開車到隔壁城市 |

**核心結論：Memory 比 HDD 快 10 萬倍，比 SSD 快 1,000 倍。這就是 Cache（Redis）有用的原因。**

### 3. QPS 估算公式

```
QPS = DAU × 每人每天操作次數 / 100K（86,400 秒簡化）
Peak QPS = QPS × 3
```

### 4. Storage 估算公式

```
Daily Storage = 每天新增筆數 × 每筆大小
Total Storage = Daily Storage × 天數
```

### 5. 面試心算技巧

| 技巧 | 説明 |
|---|---|
| 86,400 → **100K** | 一天的秒數簡化 |
| 365 天 → **400 天** | 一年天數簡化 |
| M / K = K | 單位約分（100M / 100K = 1K） |
| Bytes × M = MB | 單位捷徑 |
| 1,000 MB = 1 GB | 換算 |
| 1M MB = 1 TB | 換算 |

**重點：速度 > 精確度。量級對就好，不需要精確到個位數。**

---

## 📋 Exercise: URL Shortener Estimation（✅ 完成）

已知：100M DAU, 每人每天建立 1 個短網址, 讀寫比 100:1, 每筆 ~200 Bytes, 保留 5 年

| 項目 | 計算 | 答案 |
|---|---|---|
| Write QPS | 100M × 1 / 100K | **1K** |
| Read QPS | 1K × 100 | **100K** |
| Daily Storage | 100M × 200 Bytes = 20,000 MB | **20 GB** |
| 5 年 Total Storage | 20 GB × 2,000 天 | **40 TB** |

### 數字驅動設計決策

- Read QPS 100K → 需要 cache（單台 DB 扛不住）
- Write QPS 1K → 相對低，DB 寫入壓力不大
- 40 TB 5 年 → 一台機器存得下，但要考慮 backup 和 replication

---

## ⚖️ Trade-off

- 簡化計算犧牲精確度，但面試時間有限，量級對就夠
- 過度精確反而浪費時間，面試官要的是 sense 不是答案

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 100 萬則 Tweet（300 Bytes）= GB 等級 | 300 Bytes × 1M = 300 MB，是 MB 等級 | 沒用捷徑（Bytes × M = MB），直覺高估了 |
| 100M × 200 Bytes = 2 TB | 100M × 200 Bytes = 20,000 MB = 20 GB | 單位換算搞混，忘了 1,000 MB = 1 GB |
| 面試沒有計算機就算不出來 | 用簡化技巧（100K 秒、約分、湊整數）可以心算 | 以為要精確計算，其實只需要量級對 |
