# Go Day -5: Types, Structs, Error Handling

---

## 📝 One-liner

Go 用 struct 把相關的資料組在一起，用 method 把行為綁在 struct 上，讓程式碼讀起來像自然語言。

---

## Key Concepts

### 1. Struct — 資料的藍圖

- Struct 定義「一個東西長什麼樣子」，像房子的藍圖
- 用 `type Name struct { ... }` 定義
- 用 `Name{field: value}` 建立實例（蓋出實際的房子）
- **藍圖 ≠ 房子**：`Contact` 是類型（藍圖），`c` 是變數（實際蓋好的房子）

```go
type Contact struct {
    Name      string
    Phone     string
    Emergency bool
}

c1 := Contact{Name: "Alice", Phone: "0912345678", Emergency: true}
```

### 2. Zero Value — Go 的安全預設

沒給值的欄位，Go 自動給 zero value：

| Type | Zero Value |
|------|-----------|
| `string` | `""` (空字串) |
| `bool` | `false` |
| `int` | `0` |
| pointer/slice/map | `nil` |

```go
c2 := Contact{Name: "Bob"}
// c2.Phone = ""    ← 不是 0，不是 nil
// c2.Emergency = false
```

### 3. Method vs Function

- **Function**: 獨立的，要把資料傳進去 → `Display(c1)`
- **Method**: 綁在 struct 上，struct 自己呼叫 → `c1.Display()`

判斷方式：`func` 跟 function 名字之間有 `(receiver)` → method

```go
// Function
func Display(c Contact) string { return c.Name + " - " + c.Phone }

// Method — 多了 receiver (c Contact)
func (c Contact) Display() string { return c.Name + " - " + c.Phone }
```

- Receiver 的變數名稱用 struct 名稱的**第一個小寫字母**（Go 慣例）
- `Contact` → `c`, `User` → `u`
- `alice.Display()` 時，method 裡的 `c` 就是 `alice` 自己

### 4. Value Receiver vs Pointer Receiver

Go 預設傳值是**複製**。兩種 receiver 的差別：

| Receiver | 比喻 | 改得到原件？ | 用在 |
|----------|------|------------|------|
| `(c Contact)` — Value | 影印文件來看，看完丟掉 | ❌ | 只讀（如 `Display`） |
| `(c *Contact)` — Pointer | 拿原件來改 | ✅ | 要修改（如 `UpdatePhone`） |

```go
// Value receiver — 只讀
func (c Contact) Display() string { return c.Name }

// Pointer receiver — 修改原件
func (c *Contact) UpdatePhone(newPhone string) { c.Phone = newPhone }
```

一句話：**要改資料 → `*`，只讀 → 不加**

### 5. Error Handling — 每一步都檢查

Go 不用 try/catch，而是**每個 function 回傳 `(result, error)` 兩個值**：

```go
c, err := FindContact("Alice", phonebook)
if err != nil {
    // 出事了，馬上處理
}
// 沒事，繼續用 c
```

- `nil` 是 error 的 zero value，代表「沒有錯誤」
- `err != nil` 代表「有錯誤」
- 比 try/catch 囉嗦，但好處是**永遠知道哪一步出錯**

回傳兩個值的寫法：

```go
func FindContact(name string, phonebook []Contact) (Contact, error) {
    for _, c := range phonebook {
        if c.Name == name {
            return c, nil  // 找到了，沒有錯誤
        }
    }
    return Contact{}, fmt.Errorf("contact %s not found", name)
    //     ^^^^^^^^^ zero value（空的 Contact）
}
```

### 6. `...` 展開運算符 — 拆箱

`...` 把一個 slice 拆開成一個一個的元素，像「拆包裹」：

```go
[Charlie, David]...  →  Charlie, David
// 一整包             →  拆成一個一個
```

用在 `append` 時：

```go
append(slice, item1, item2)       // ✅ 一個一個傳
append(slice, anotherSlice...)    // ✅ 用 ... 展開另一個 slice
append(slice, anotherSlice)       // ❌ 類型不對，slice 不是單一元素
```

`...` **不是語法糖**（有替代寫法的捷徑），而是語言必要功能 — 不知道 slice 長度時，沒有它做不到展開。相比之下，`:=` 是語法糖，因為可以用 `var x int = 5` 代替。

### 7. Slice 刪除 Pattern

從 slice 中刪除 index `i` 的元素：

```go
// 假設: [Alice, Bob, Charlie, David]，刪 Bob (i=1)
phonebook = append(phonebook[:i], phonebook[i+1:]...)
//                 ^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^
//                 Bob 前面: [Alice]  Bob 後面拆開: Charlie, David
//
// 結果: [Alice, Charlie, David]
```

- `phonebook[:i]` → 第一個參數是「容器」（箱子），本來就是 slice，不用 `...`
- `phonebook[i+1:]...` → 後面的參數是「要放進去的東西」，需要 `...` 拆開

### 8. 反轉 Error 檢查 Pattern

`AddContact` 用了一個實用技巧 — 反轉 `FindContact` 的錯誤邏輯：

```go
_, err := FindContact(name, phonebook)
if err == nil {  // 找得到 = 已存在 = 不能重複加
    return phonebook, fmt.Errorf("contact %s already exists", name)
}
```

本來 `FindContact` 的「找不到 = error」，反過來用「找得到 = error（重複）」。

### 9. 其他語法筆記

- `:=` → 短變數宣告（建立新變數，自動判斷類型）；`=` → 修改已存在的變數
- `!` → NOT（否定），`!true` = `false`，像電燈開關
- `_` → 忽略不需要的值（如 `for _, c := range`，不在乎 index）
- Go 大小寫敏感：struct 定義 `Name` 就要用 `c.Name`，不是 `c.name`
- 所有運算符必須用**英文符號**，中文的 `。` `！` Go 不認

---

## ⚖️ Trade-off

- **Method vs Function**：Method 讓程式碼更直覺（`c1.Display()`），但如果邏輯不屬於任何 struct，用 function 更合適
- **Error Handling**：Go 的 `if err != nil` 比 try/catch 囉嗦，但每一步都明確處理，不會漏掉錯誤
- **Value vs Pointer receiver**：Pointer 可以改原件但增加複雜度；Value 更安全但只能讀。SD PoC 中 pointer receiver 用得更多

---

## 🔴 My Mistakes & Misconceptions

### Session 1

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| `string` 的 zero value 是 `0` | `string` 的 zero value 是 `""` (空字串) | 混淆了 `int` 和 `string` 的 zero value，`0` 是數字類型的事 |
| `bool` 的 zero value 是 `true` | `bool` 的 zero value 是 `false` | Go 的哲學是安全預設，`false` 比 `true` 更安全 |
| 不懂 function 跟 method 的差別 | Method = Function + 綁定一個 receiver，看 `func` 後面有沒有 `(c Contact)` 來判斷 | 兩者都用 `func` 關鍵字，Go 故意不區分，只靠有無 receiver 決定 |
| 不懂 `(c Contact)` 裡 `c` 是什麼 | `c` 是代表「呼叫這個 method 的那個實例」的變數名，`c1.Display()` 時 `c` = `c1` | 以為 `Contact` 就夠了，沒想到需要一個變數名來在 method 內部存取欄位 |
| 為什麼 method 也用 `func` 開頭 | Go 認為 method 本質上就是 function，只是多綁了一個 receiver | 預期會有不同的關鍵字（像其他語言可能用 `def` 或在 class 內定義） |
| `c.name` 小寫存取欄位 | Go 大小寫敏感，struct 定義 `Name` 就要用 `c.Name` | 沒注意到 Go 的大小寫敏感，欄位名要跟定義完全一致 |
| 用 `=` 做比較 | `=` 是賦值，`==` 才是比較 | 其他語言（如 shell script）有時用 `=` 比較，Go 嚴格區分 |
| `return Contact` 回傳類型名稱 | 要回傳變數 `c`（實例），不是 `Contact`（類型） | 混淆了「藍圖」和「蓋好的房子」— 類型 vs 變數 |
| `return` 只回傳一個值 | function 簽名是 `(Contact, error)`，必須回傳兩個值 | 忘記 Go 的 error handling 慣例：找到回傳 `c, nil`，沒找到回傳 `Contact{}, error` |
| 用中文 `！` `。。。` 寫程式 | Go 只認英文符號 `!` `...` | 中文輸入法的符號 Go 不認，所有運算符都要用英文 |
| 以為 `UpdatePhone` 用 value receiver 就能改原件 | Value receiver 拿到的是複製品，改了不影響原件 | Go 預設是複製，要改原件必須用 `*Contact`（pointer receiver） |

### Session 2（複習）

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 忘記 Value Receiver 這個名詞 | 沒加 `*` 的 receiver 叫 Value Receiver — 拿複製品，只讀 | 只記得 Pointer Receiver 要加 `*`，沒把「不加 `*`」的情況命名記住 |
| 忘記 `Contact` 和 `c` 的差別 | `Contact` = 類型（分類牌），`c` = 變數（實際的那瓶可樂） | 上次學了但沒內化，需要重複練習 |

---

## 🧪 Session Quiz Results

| 題目 | 考點 | 結果 | 備註 |
|------|------|------|------|
| Q1: `User{Name: "Jason"}` 的 Age 和 Admin | Zero value | ✅ 一次過 | 已掌握 |
| Q2: Value receiver 能不能改原件 | Pointer receiver | ✅ 一次過 | 已掌握 |
| Q3: `u.name = name` + `return User` | 大小寫 + `==` + 類型 vs 變數 | ⚠️ 需提示 | 認得出錯誤但不能立即反應 |
| Q4: `return fmt.Errorf(...)` 少回傳值 | 回傳值數量 | ⚠️ 需引導 | 知道要回傳 2 個，但沒看出哪行少了 |

### 下次重點複習
- **類型 vs 變數**：`Contact`（藍圖）≠ `c`（實例）— 出現 3 次同樣的錯
- **回傳值數量**：簽名寫幾個就回傳幾個，成功和失敗都要
- **語法細節**：大小寫、`=` vs `==`、英文符號
- **`=` vs `==`**：CRUD 練習又犯了一次（`if err = nil`），要特別注意
- **`...` 語法**：append 接 slice 時要加 `...` 展開

### CRUD 練習新錯誤
| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| `if err = nil` 做比較 | 要用 `==`，`=` 是賦值 | 同一天第二次犯，`=` vs `==` 是最大痛點 |
| `err != nil` 代表找到重複 | `err == nil` 才是找到（沒錯誤 = 成功找到） | 混淆了 FindContact 的角度和 AddContact 的角度 |
| `append(phonebook[:i], phonebook[i+1:])` 不加 `...` | 要加 `...` 展開 slice | `append` 接 slice 需要 `...` 拆開，是固定語法 |
---

## 📌 面試怎麼回答

> **Q: Go 怎麼處理錯誤？跟其他語言有什麼不同？**
>
> Go 不用 try/catch，而是讓每個 function 回傳 `(result, error)` 兩個值。caller 每一步都必須用 `if err != nil` 檢查。這比 exception 囉嗦，但好處是 error handling 是 explicit 的 — 你永遠知道哪一步可能出錯，不會有隱藏的 exception 從第 10 層 stack 飛上來。

> **Q: Value receiver 跟 Pointer receiver 差在哪？**
>
> Value receiver 拿到的是複製品，只能讀；Pointer receiver 拿到的是原件的地址，可以修改。經驗法則：需要 mutate state 的用 pointer，純讀取的用 value。
