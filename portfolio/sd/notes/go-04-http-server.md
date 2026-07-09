# Go Day -2: HTTP Server & JSON

> Status: ✅ Completed

---

## 📝 One-liner

Go 用 `net/http` 幾行就能開一個 HTTP server，搭配 JSON encode/decode 就能建出 REST API — 這是每個 System Design PoC 的骨架。

---

## Key Concepts

### 1. 最小 HTTP Server

```go
http.HandleFunc("/path", handler)     // 註冊路徑 + handler
http.ListenAndServe(":8090", nil)     // 啟動 server
```

### 2. Handler 參數

```go
func handler(w http.ResponseWriter, r *http.Request) {
//            ↑ 寫回應給客人          ↑ 讀客人的請求
}
```

| 參數 | 作用 | 比喻 |
|------|------|------|
| `w http.ResponseWriter` | 寫回應 | 便當盒，裝好送出去 |
| `r *http.Request` | 讀請求 | 客人的點餐單 |

### 3. HTTP Method — 用 switch 判斷

```go
switch r.Method {
case "GET":     // 讀取
case "PUT":     // 寫入/更新
case "DELETE":  // 刪除
default:        // 不支援
    w.WriteHeader(http.StatusMethodNotAllowed)  // 405
}
```

### 4. JSON Encode / Decode

| 方向 | 函數 | 比喻 |
|------|------|------|
| Go → JSON（寫回應） | `json.NewEncoder(w).Encode(data)` | 打包便當送出去 |
| JSON → Go（讀請求） | `json.NewDecoder(r.Body).Decode(&input)` | 拆開外送盒取出內容 |

- **Decode 要 `&`**：因為要修改 input（填入資料），需要 pointer
- **Encode 不用 `&`**：只讀資料，不需要改

### 5. Struct Tag — JSON 欄位對應

```go
type SetValue struct {
    Value string `json:"value"`   // backtick ` 不是單引號 '
}
```

- backtick 在鍵盤左上角（`~` 同一個鍵）
- `json:"value"` 冒號後**不能有空格**

### 6. HTTP Status Code

| Code | 常數 | 意思 | KV Store 場景 |
|------|------|------|--------------|
| 200 | `http.StatusOK` | 成功 | Get/Set/Delete 成功 |
| 404 | `http.StatusNotFound` | 找不到 | key 不存在 |
| 400 | `http.StatusBadRequest` | 請求格式錯 | JSON 解析失敗 |
| 405 | `http.StatusMethodNotAllowed` | 方法不支援 | 用了 PATCH 等不支援的 method |

### 7. URL 路徑解析

```go
key := strings.TrimPrefix(r.URL.Path, "/keys/")
// /keys/name → "name"
// /keys/age  → "age"
```

### 8. CLI 操作

```bash
# 啟動 server
go run main.go        # 開發用，直接跑
go build -o server && ./server   # 先編譯再跑

# curl 測試（另開 terminal）
curl -X PUT http://localhost:8090/keys/name -d '{"value":"Jason"}'
curl http://localhost:8090/keys/name
curl -X DELETE http://localhost:8090/keys/name
curl -v http://localhost:8090/keys/name    # -v 顯示 status code

# 背景執行（同一個 terminal）
go run main.go &    # & 放背景
kill %1             # 停止
```

---

## ⚖️ Trade-off

- `net/http` 簡單但功能基本（沒有路由參數如 `/keys/:key`），複雜 API 會用 gin 或 chi 等框架。但 SD PoC 用 `net/http` 就夠了，不需要額外依賴。
- JSON 用 `map[string]string` 快速方便，但大型專案應該定義 response struct 確保型別安全。

---

## 📋 Exercise: KV Store REST API（✅ 完成）

- [x] MemoryStore struct + Get/Set/Delete methods
- [x] HTTP handler with switch on GET/PUT/DELETE
- [x] JSON encode/decode
- [x] curl 測試全部通過（PUT → GET → GET 404 → DELETE → GET 404）
- Output: `projects/go-refresher/day04-http-server/main.go`

### SD Connection
- 這個 REST API 骨架是每個 Phase 3 PoC 的起點
- handler + switch + JSON = 所有 SD PoC 的標準模式

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| Struct tag 用單引號 `'json:"value"'` | 要用 backtick `` `json:"value"` `` | 不知道 backtick 這個符號，混淆了單引號和 backtick |
| `json: "value"` 冒號後有空格 | `json:"value"` 冒號後不能有空格 | Go struct tag 的格式很嚴格 |
| `r *http.Response` | `r *http.Request`，Response 是回應，Request 才是請求 | Response 和 Request 搞反了 |
| `store.handlekeys` 小寫 k | `store.handleKeys` 大寫 K，Go 大小寫敏感 | 反覆犯的大小寫問題 |
| `s.set()` 小寫 s | `s.Set()` 大寫 S | 同上 |
| `"status： ok"` 中文冒號 + ok 沒引號 | `"status": "ok"` 英文冒號 + ok 要引號 | 中文符號問題再次出現，JSON 的 value 也要引號 |
| `StatusFound` 是 404 | `StatusFound` 是 302（重導向），`StatusNotFound` 才是 404 | 沒注意到 Found = 找到，NotFound = 找不到 |
| DELETE 不用 `return` | 404 之後要 `return`，否則繼續往下跑會回應兩次 | 跟 GET 一樣，錯誤處理後要立刻結束 |
| `json.NewEncoder("status": "deleted")` | 完整寫法是 `json.NewEncoder(w).Encode(map[string]string{"status": "deleted"})` | 語法不熟，漏了 `(w)` 和 `.Encode(...)` |
| 不知道 Marshal/Unmarshal 是什麼 | Marshal = Go → JSON（打包），Unmarshal = JSON → Go（拆包）。Encode/Decode 是同義詞 | 第一次接觸這個術語 |
| 不知道 Decode 為什麼要 `&` | `&` 取 pointer，Decode 要修改 struct（填入資料），所以需要原件地址 | pointer 的應用場景不熟，統一規則：要改加 `&`，只讀不加 |
| `if !ok -> w.WriteHeader(...)` 寫在一行 | Go 用 `if !ok { ... }` 大括號包 block，每個動作獨立一行 | 不熟悉 Go 的 if 語法結構 |
| Voice Drill: handler 沒說「是什麼」只說「怎麼寫」 | 回答要先定義（what），再說細節（how） | 面試回答要先給 one-liner 定義 |
| Voice Drill: 漏了 Decode 和 `&` 的解釋 | 要完整涵蓋被問到的所有部分 | 回答不完整 |
