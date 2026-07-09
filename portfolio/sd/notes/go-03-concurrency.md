# Go Day -3: Goroutines & Channels

> Status: ✅ Completed

---

## 📝 One-liner

Go 用 Goroutine 開輕量級線程同時做事，用 Channel 在線程間安全傳資料，用 WaitGroup/Mutex 做同步控制 — 是所有 System Design 並發場景的基礎。

---

## Key Concepts

### 1. Goroutine — 輕量級線程

- `go func()` 開一個新的 goroutine，不等它做完
- 比 OS thread 輕量（~2KB vs ~1MB），可以開幾千個
- `main()` 本身也是一個 goroutine，main 結束 = 整個程式結束，不會等其他 goroutine

```go
go cookNoodle("味噌")   // 丟出去，馬上跑下一行
```

比喻：老闆叫廚師煮麵，不等他煮完就下班了 → 廚師還沒煮完店就關了

### 2. sync.WaitGroup — 等所有工人做完

```go
var wg sync.WaitGroup
wg.Add(2)           // 登記要等 2 個人
go func() {
    defer wg.Done() // 做完說「我好了」，計數器 -1
}()
wg.Wait()           // 等到計數器歸零才繼續
```

| 方法 | 比喻 | 作用 |
|------|------|------|
| `Add(n)` | 老闆登記要等 n 個人 | 計數器 +n |
| `Done()` | 廚師喊「我好了」 | 計數器 -1 |
| `Wait()` | 老闆等到計數器歸零 | 阻塞直到全部完成 |

- WaitGroup 不需要 `make`，`var` 宣告就能用（zero value 可用）

### 3. Channel — goroutine 間的傳資料通道

```go
ch := make(chan string)       // 建立 channel
ch <- "味噌拉麵好了"           // 送進 channel
result := <-ch                // 從 channel 拿出
close(ch)                     // 關閉 channel（沒有更多資料了）
```

| 語法 | 方向 | 比喻 |
|------|------|------|
| `ch <- value` | 送進去 | 廚師放碗到取餐口 |
| `value := <-ch` | 拿出來 | 服務生從取餐口端走 |
| `close(ch)` | 關閉 | 廚師說「沒有了」 |

- Channel 是**阻塞**的：送的人等有人拿，拿的人等有人送
- `for msg := range ch` 會一直讀到 channel 被 close

### 4. 為什麼不用全域變數？

| | 全域變數 | Channel |
|--|---------|---------|
| 多人同時寫 | Race Condition（資料打架） | 安全，排隊一個一個來 |
| 時機控制 | 不知道對方什麼時候寫完 | 阻塞等待，自動同步 |

Go 名言：**"Don't communicate by sharing memory; share memory by communicating."**

### 5. sync.Mutex — 保護共用資料

```go
var mu sync.Mutex
mu.Lock()              // 上鎖
s.data[key] = value    // 安全操作
mu.Unlock()            // 解鎖
```

| 場景 | 用什麼 |
|------|--------|
| goroutine 之間**傳遞資料** | Channel |
| 多個 goroutine **保護共用資料** | Mutex |

### 6. defer — 結束前一定執行

```go
defer wg.Done()  // function 結束前才執行，不管中間有沒有出錯
```

- 比喻：離開房間前**一定要關燈**
- 比直接放最後一行更安全：中間出錯（panic）也會執行
- 多個 defer 的順序是 **LIFO**（後進先出，像疊盤子）

### 7. var vs := 的使用場景

| 寫法 | 適合場景 |
|------|---------|
| `var wg sync.WaitGroup` | struct 不需要初始值，zero value 就能用 |
| `ch := make(chan string)` | 需要 `make` 初始化的型別（channel, map, slice） |

---

## ⚖️ Trade-off

- Channel vs Mutex：Channel 適合傳遞資料（生產者-消費者），Mutex 適合保護共用資料（多人讀寫同一個 map）。能用 Channel 就用 Channel，更符合 Go 哲學。
- Goroutine 的代價：雖然輕量但不是免費。開太多 goroutine 仍會消耗記憶體和 scheduler 資源。

---

## 📋 Exercise: Producer-Consumer（✅ 完成）

- [x] Producer goroutine 送 5 個訂單到 channel
- [x] 2 個 Consumer goroutine 用 WaitGroup 同時搶訂單
- [x] 觀察到 Competing Consumers Pattern：每次跑分配不同
- Output: `projects/go-refresher/day03-concurrency/main.go`

### SD Connection
- Producer-Consumer = Message Queue 的核心模型（Phase 1 Day 10-11）
- Competing Consumers = SQS/Kafka consumer group 的自動負載均衡

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| for 迴圈用逗號 `,` 隔開 | Go 的 for 三段用分號 `;`：`for i := 0; i < 5; i++` | 混淆了其他語言的語法 |
| `close(CH)` 大寫 | Go 大小寫敏感，變數叫 `ch` 就要寫 `ch` | 粗心，同 Day -4 的 `data`/`date` 問題 |
| `main()` 不用加 `func` | Go 所有 function 都要 `func` 開頭 | 語法不熟 |
| `for range ch` 用 `()` 包 body | Go 用 `{}` 不是 `()`，`()` 是 function 參數用的 | 混淆了括號用途 |
| 程式碼可以放在 `func main()` 外面 | Go 所有可執行邏輯必須在 function 內 | 不清楚 Go 的程式結構規則 |
| `go func()` 匿名函數寫不出來 | 完整語法是 `go func() { ... }()`，最後的 `()` 是立刻執行 | 不熟悉匿名函數 + 立即執行的語法 |
| 不知道 `var` 和 `:=` 的差別 | `var` 用 zero value 初始化；`:=` 用右邊的值。struct 不需要初始值時慣例用 `var` | 沒注意到 Go 的兩種宣告方式適用不同場景 |
| 不知道 `defer` 是什麼 | `defer` = function 結束前一定執行，比放最後一行更安全（panic 也會執行） | 第一次接觸這個概念 |
| Voice Drill: thread 說成 threat | thread（線程）不是 threat（威脅） | 英文發音/拼字錯誤 |
| Voice Drill: Channel 只說了 what 沒說 why | 要講出為什麼不用全域變數（race condition） | 回答不完整，要包含原因 |
