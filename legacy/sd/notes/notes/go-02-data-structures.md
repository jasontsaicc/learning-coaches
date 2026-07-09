# Go Day -4: Slices, Maps, Interfaces

> Status: ✅ Completed

---

## 📝 One-liner

Go 用 Slice 處理有序集合，Map 處理 key-value 查找，Interface 定義行為合約 — 三者是建構任何 System Design PoC 的基礎資料結構。

---

## Key Concepts

### 1. Array vs Slice

| | Array | Slice |
|--|-------|-------|
| 長度 | **固定**，宣告時決定 | **可變**，能伸縮 |
| 宣告 | `[3]string` | `[]string` |
| 用途 | 幾乎不用 | **99% 用這個** |

- `[]` 裡有數字 = Array，沒數字 = Slice
- 實際寫 Go 幾乎只用 Slice

### 2. Slice 三屬性：len, cap, append

| 屬性 | 意思 | 比喻 |
|------|------|------|
| **len** | 目前有幾個元素 | 貨架上有幾箱貨 |
| **cap** | 最多能放幾個（不用擴容） | 貨架總共幾格 |
| **append** | 加元素，滿了自動擴容（通常 2 倍） | 滿了自動換更大的貨架 |

```go
s := make([]int, 3, 5)  // len=3, cap=5
s = append(s, 10)        // len=4, cap=5 — still fits
s = append(s, 20, 30)    // len=6, cap=10 — auto expanded
```

### 3. Slice Gotcha — 切片共享記憶體

```go
a := []string{"go", "python", "java"}
b := a[0:2]    // b = ["go", "python"]
b[1] = "rust"  // a 也變成 ["go", "rust", "java"]!
```

- **Slice 切出來不是複製品，是指向同一塊記憶體**
- 比喻：放大鏡看原件，不是影印

### 4. Map — key-value 對照表

```go
ages := map[string]int{
    "Alice": 30,
    "Bob":   25,
}
ages["Charlie"] = 35      // add
delete(ages, "Bob")        // delete
fmt.Println(ages["Alice"]) // read → 30
```

| 特性 | 說明 |
|------|------|
| 無序 | 遍歷順序每次可能不同 |
| key 唯一 | 同 key 寫兩次，後蓋前 |
| 查不到 = zero value | `ages["Nobody"]` → `0` |

### 5. Comma Ok Pattern — 分辨「不存在」vs「值是 zero value」

```go
age, ok := ages["Bob"]     // age=0, ok=true  ← exists, value is 0
age, ok := ages["Nobody"]  // age=0, ok=false ← doesn't exist
```

- `ok == true` → key 存在
- `ok == false` → key 不存在

### 6. Interface — 行為合約

```go
type Store interface {
    Get(key string) (string, bool)
    Set(key string, value string)
    Delete(key string) bool
}
```

- Interface 只定義「要會做什麼」，不管「怎麼做」
- **隱式實現**：Go 不用寫 `implements`，method 都寫齊就自動滿足
- **全有或全無**：少一個 method 都不算

### 7. Map 必須初始化

```go
var m map[string]string  // m = nil
m["key"] = "val"         // 💥 panic!

m = make(map[string]string)  // ✅ init first
m["key"] = "val"             // safe
```

- `NewMemoryStore()` 的作用就是確保 map 已初始化，避免 nil panic

### 8. 回傳值括號規則

| 回傳幾個值 | 寫法 |
|-----------|------|
| 1 個 | `bool` — 不用括號 |
| 2 個以上 | `(string, bool)` — 要括號 |

---

## ⚖️ Trade-off

- Slice vs Map：Slice 有序、用 index 存取快；Map 無序、用 key 查找快。需要按順序 → Slice，需要快速查找 → Map
- Interface 隱式 vs 顯式實現：Go 的隱式實現更靈活（不用改舊 code），但缺點是不容易一眼看出誰實現了什麼 interface

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| `...` 像 Python 的 `for i in x`（迴圈） | `...` 是拆包（像 Python 的 `*`），把 slice 展開成個別元素 | 混淆了「遍歷」和「展開」，`...` 不是迴圈，是告訴 append 一顆一顆加 |
| `DeleteContact("Nobody")` 回傳 `nil` | 回傳 `!= nil`（有錯誤），因為 Nobody 不存在 | `nil` = 沒事，`!= nil` = 出事。搞反了 |
| Error Handling 完全忘記怎麼運作 | 每個 function 回傳 `(result, error)`，每步用 `if err != nil` 檢查 | 上次學過但沒內化，需要多練 |
| `NewMemoryStore()` 不知道在幹嘛（問了兩次） | 初始化 struct 內部的 map，避免 nil map panic | 不知道 Go 的 map 必須 `make` 才能寫入 |
| `data` 打成 `date` | 欄位名是 `data` | 粗心拼字錯誤 |
| 不確定為什麼 `Delete` 的 `bool` 不用括號 | 回傳 1 個值不用括號，2 個以上才要 `()` | 沒注意到 Go 的語法規則：多值回傳才加括號 |
| nil map 以為是 `{}`（空 map） | nil map 是 `nil`，不是空 map。讀 nil map 不會 panic，寫才會 | 沒區分「沒有桌子」(nil) 和「空桌子」(empty map) |
| Method 語法寫成 `func (s MemoryStore) Get() int` | 要 `func (s *MemoryStore) Get(key string) (string, bool)` — 指標 receiver + 參數 + 回傳都要跟 interface 一致 | 不熟悉 Go method 語法，receiver/參數/回傳三個都寫錯 |
| Set 寫成 `value = s.data[key]`（方向反了） | 應該是 `s.data[key] = value`，`=` 左邊是被改的目標 | 搞混了讀取和寫入的方向 |
| 宣告了變數 `val` 但沒用到 | Go 不允許 unused variable，不需要的值用 `_` 忽略 | 不知道 Go 的嚴格規則：宣告了就必須用 |
| `fmt.Println` 沒把變數放進去 | 要印變數就要放進 Println 的參數裡 | 語法不熟 |
| 用 `val, ok` 但沒先用 `:=` 宣告 | 變數要先用 `:=` 接住 function 回傳值才能用 | 忘了 Go 要先宣告變數 |
| Voice Drill: Q1 只講了 Slice，漏了 Map 和 Interface | 回答要涵蓋所有被問到的東西 | 練習時不夠完整 |
| Voice Drill: nil map 讀 vs 寫行為沒分清 | 讀 nil map → 回傳 zero value（不 panic），寫 nil map → panic | 只記得「不能用」但沒分清讀和寫的差異 |

---

## 📋 Exercise: KV Store（✅ 完成）

- [x] 實作 `Get`、`Set`、`Delete` 三個 method
- [x] 寫 `main()` 測試（3 場景：Set→Get、Get 不存在、Delete→Get 確認消失）
- [x] 確認滿足 `Store` interface
- Output: `projects/go-refresher/day02-data-structures/main.go`
