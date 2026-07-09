# Go Day -1: Testing & Docker

> Status: ✅ Completed

---

## 📝 One-liner

`go test` 搭配 table-driven test 把手動測試自動化，Docker multi-stage build 把 Go app 打包成超小 image — 這是部署的標準流程。

---

## Key Concepts

### 1. Table-driven Test（Go 慣例）

把所有 test case 放在一個 slice of struct，用 for loop + `t.Run` 跑：

```go
tests := []struct {
    name     string
    input    string
    expected string
}{
    {"case1", "a", "A"},
    {"case2", "b", "B"},   // 最後一行也要逗號
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        // 測試邏輯
        if got != tt.expected {
            t.Errorf("got %v, want %v", got, tt.expected)
        }
    })
}
```

| 規則 | 說明 |
|------|------|
| 檔名 | `*_test.go` |
| 函數名 | `TestXxx(t *testing.T)` — 大寫 T 開頭 |
| 執行 | `go test -v ./...` |
| 失敗回報 | `t.Errorf(...)` |

**好處：** 加新 case 只加一行，`t.Run(name)` 失敗時直接顯示哪個 case。

### 2. Benchmark

```go
func BenchmarkSet(b *testing.B) {
    for i := 0; i < b.N; i++ {   // b.N 由 Go 自動決定
        // 要測的操作
    }
}
```

```bash
go test -bench=. -benchmem
```

### 3. context.Context

**一句話：** context = 可以被取消的工作單，一路傳下去讓每一層都知道「還做不做」。

| 功能 | 比喻 | 用法 |
|------|------|------|
| 取消信號 | 老闆說不用做了 | `ctx.Done()` |
| 截止時間 | 5 點前要完成 | `context.WithTimeout()` |
| 附帶資訊 | 工作單備註 VIP | `context.WithValue()` |

```go
// HTTP handler 裡每個 request 自帶 context
ctx := r.Context()  // 客人斷線 → ctx 取消 → 下游停手
```

**規則：** context 永遠是函數第一個參數。

### 4. Dockerfile — Multi-stage Build

```dockerfile
# Stage 1: Build（有 compiler，編譯用）
FROM golang:1.25 AS builder
WORKDIR /app
COPY go.mod ./
COPY *.go ./
RUN go build -o server .

# Stage 2: Run（只放執行檔）
FROM alpine:latest
COPY --from=builder /app/server /server
CMD ["/server"]
```

| | 單 stage | Multi-stage |
|---|---|---|
| Image 大小 | ~800MB | ~15MB |
| 安全性 | 含 compiler + source code | 只有執行檔 |

**重點：** Dockerfile 裡 Go 版本要 ≥ go.mod 裡的版本，否則 build 失敗。

### 5. Docker Compose

```yaml
services:
  kvstore:
    build: .
    ports:
      - "8090:8090"   # host:container
```

```bash
docker-compose up --build    # 建置 + 啟動
docker-compose down          # 停止 + 清除
```

---

## ⚖️ Trade-off

- Table-driven test 適合**同一個函數、不同輸入**的場景。如果測試邏輯差異很大（如 setup 不同），不適合硬塞進同一個 table。
- Multi-stage build 的 Alpine image 很小，但如果 app 用到 CGO（C library），Alpine 可能缺 shared library，需要改用 `debian` base image。

---

## 📋 Exercise: KV Store Testing & Docker（✅ 完成）

- [x] Table-driven test — 8 個 case 覆蓋 set/get/delete/overwrite/not-found
- [x] Benchmark for Set operation
- [x] main.go — HTTP server 啟動
- [x] Dockerfile — multi-stage build
- [x] docker-compose.yml
- [x] `go test -v` 全部 PASS
- [x] `docker build` 成功
- Output: `projects/go-refresher/day05-testing-docker/`

### SD Connection
- Testing 是每個 PoC 的品質保證，面試時說「我有寫 test」加分
- Docker 是部署的標準，SD 面試討論 deployment 一定會提到 containerization

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 直接寫 get case，不用先 set | store 是空的，要先 set 才有資料可以 get | 沒想到 test case 是按順序跑的，共用同一個 store |
| `{"get age", "get", "name", "", "age", true}` | key 應該是 `"age"` 不是 `"name"`，expectedVal 是 `""`，expectedOk 是 `false` | 混淆了 key 欄位和 expectedVal 欄位，不存在的 key 回 false 不是 true |
| `{"set bob", "set", "name", "Bob", true}` 只填 5 個欄位 | struct 有 6 個欄位，set 不檢查的欄位也要填零值 `"", false` | 沒數清楚 struct 的欄位數量 |
| `http.HandleFunc(pattern string, handler func(...))` | 呼叫函數要傳實際的值：`http.HandleFunc("/keys/", store.handleKeys)` | 把函數呼叫寫成了函數定義（寫型別而不是傳值） |
| `fmt.Prontln`、`http.ListenAndServer`、`http:.` | `Println`、`ListenAndServe`、`http.` | 拼字粗心，需要注意函數名稱拼寫 |
| `"/keys"` 路徑不用尾巴 `/` | `"/keys/"` 要有尾巴 `/`，不然 `/keys/name` 匹配不到 | Go 的路由匹配是 prefix match，少了 `/` 會影響子路徑 |
| 不知道 ctx 是什麼 | ctx 是 `context.Context` 的慣用變數名縮寫，就像 `s` 代表 store | 第一次看到 ctx 這個縮寫，不知道它是變數名不是關鍵字 |
| `FROM golang:1.23` 可以 build go 1.25 的程式 | Dockerfile 的 Go 版本要 ≥ go.mod 的版本 | Go 1.21+ 把 go.mod 版本當最低需求，版本不夠直接拒絕 build |
| Voice drill 不知道怎麼組織回答 | 先說 what（定義），再說 why（為什麼用），最後 how（怎麼用） | 面試回答要有結構，不能只說 how |
