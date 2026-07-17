# One-Liner Library (Pattern Quick-Answer Bank)

<!-- Domain registry(宣告於 leetcode-coach portfolio hook)。16 條,自 standalone
     session-progress-archive.md 的 Pattern One-Liner Library 遷入,內容 verbatim。
     用法:看到題目訊號,一句話說出 pattern + 為什麼 + 複雜度。抽考跟 Weekly Review
     走;滑掉 → progress.md 開 registry 條目。新條目在 pattern 收尾時產生。
     間隔複習欄位沿用 PROGRESS-SCHEMA section 7(3->7->14);migration 初始化:
     全部 interval 7、next-review 2026-07-17,首次 Weekly Review 抽考後個別調整。 -->

| Pattern | One-Liner |
|---------|-----------|
| Frequency Counter (Arrays & Hashing) | 用 hash map 計算字元頻率 — 一個 +1 一個 -1，全部歸零就一致 |
| Bucket Sort (Arrays & Hashing) | 用 Frequency Counter 數頻率，建 Bucket Array（index=頻率），從後往前掃取 top k — O(n) 不用排序 |
| Length-Prefix (Arrays & Hashing) | 每個字串前面加「長度#」，decode 時讀數字往後數字元 — 靠長度不靠分隔符，什麼字元都不怕 |
| HashSet per row/col/box (Arrays & Hashing) | 三組 HashSet 分別追蹤 row、col、3x3 box 出現過的數字，掃一次棋盤就能查重複 |
| Sequence Start Detection (Arrays & Hashing) | 丟進 set，只從起點 (num-1 不在 set) 開始往上數連續長度，每個數字最多碰一次，O(n) |
| Converging Two Pointers (Two Pointers) | 左右兩個指標從兩端往中間走，邊走邊對稱比較，遇標點/非字元跳過 — O(n) 時間 O(1) 空間 |
| Two Pointers + Greedy (Two Pointers) | 從兩端逼近，每輪移動「較矮的指標」— 因為動較高的會讓寬縮、高度被矮的卡住，永遠不可能更好；可安全 prune 一大堆 pair — O(n) 時間 O(1) 空間 |
| Two Pointers + Bounded Computation (Two Pointers) | 每位置水量 = `min(left_max, right_max) - h[i]`；左右指標逼近，每輪動較矮側並算水 — 較高側保證有牆，較矮側水量瓶頸鎖在自己的 max，現在就能算 — O(n) 時間 O(1) 空間 |
| Prefix Maximum DP (通用) | 邊掃邊記累積 max（或 min/sum/count），下一格直接從上一格累積 + 自己這格推出來 — 把 O(n²) 重複計算壓到 O(n) — 是 DP 最簡形式 |
| Monotonic Deque (Sliding Window) | deque 存「可能當 max 的候選 index」呈遞減排列；新元素進場時把右邊比它小的 pop 掉、過期的從左 popleft，最左永遠是當前窗戶 max；每元素一生進出各一次 → O(n) 攤還 |
| Stack 配對 (Stack) | 巢狀結構「最後開的最先關」= FILO；開括號 push、閉括號比對 stack 頂端配不配 (不配/空→False) 再 pop，掃完 stack 空才有效；計數器只管數量會漏型別+順序 (`([)]`)，所以要 Stack — O(n) 時間 O(n) 空間 |
| Stack 後綴求值 / RPN (Stack) | 數字 push 進 stack、運算子來就 pop 兩個 (先 pop=右、後 pop=左, FILO 鏡像) 算完 push 回去，掃完 stack 剩一個=答案；判運算子用白名單 (4 個固定) 別用 isdigit (負數會誤判)；除法 `int(l/r)` 向 0 取整非 `//` — O(n) 時間 O(n) 空間 |
| Monotonic Stack (Stack) | 維護「遞減的等待區」存還沒等到更大值的 index；新元素把頂端比它小的全 pop 掉並結算 (距離 = i - prev) 再 push 自己；存 index 不存值 (要算距離, 用 `temperatures[stack[-1]]` 回查)；每個 index 一進一出 → **O(n) 攤還** (同 #239 deque 論證) — O(n) 時間 O(n) 空間 |
| Largest Rectangle in Histogram (Stack) | 每根長條問「當最矮高度能拉多寬」= 往左右撞到比它矮的牆才停 (比它高的可鑽過去); 單調**遞增** stack 存 index, 新來的比隊尾矮就把高的 pop 結算 (**右牆 = 逼你離場的新人 i、左牆 = pop 後新隊尾 `stack[-1]`, 空則 -1**), `width = 右-左-1`, `area = heights[top]×width`; 收尾剩的右牆當 n; 每 index 一進一出 → **O(n) 攤還** (同 #739); pop「更矮」→遞增, 對比 #739 pop「更大」→遞減 = 完美鏡像 — O(n) 時間 O(n) 空間 |
| Stack + Sort 車隊 / Car Fleet (Stack) | `zip(position,speed)` 綁成車、按位置由大到小排 (靠終點先處理)；從前往後掃, 每台算到達時間 `(target-p)/s`, 比 stack 頂端**慢** (`time > stack[-1]`) → 追不到 → push 一坨新車隊, 否則被前面那坨吸收 (不動)；`len(stack)` = 車隊數；**只看頂端、從不 pop** (後車不可能讓前車消失) → 不用內層 while, 單向 for 即可 (跟 #739 monotonic stack 的差別); 其實一個變數記頂端就夠, stack 只是讓 len 數答案更直覺 — O(n log n) 時間 (排序主導) O(n) 空間 |
| Binary Search 標準模板 (Binary Search) | **前提不是「資料已排序」,是「捨棄的那半保證不含答案」** (sorted 只是取得該許可證最常見的手段;#153 旋轉陣列沒排序照樣能二分)。閉區間 `[l, r]`: `l=0, r=len-1`, `while l <= r`；`mid=(l+r)//2` (必用 `//` 整除當索引, `int//int` 回 **int**;`/` 回 float 而 float 不能當索引、也不自動轉)；`nums[mid]==target`→回 mid、`<target`→答案在右 `l=mid+1`、`>target`→在左 `r=mid-1`；沒找到跳出回 `-1` (**在迴圈外** — 「全部找完都沒有」只有迴圈跑完才成立)。三個死穴: ① `r=len-1` 不是 `len` (否則 target 比全部大時 mid 越界 IndexError;反例 `[1,2,3]` 找 5, 第 3 圈 `nums[3]` 💥) ② `while l<=r` 的 `=` 不能少 (縮到單一元素還要檢查, 少了 `[5]` 找 5 會漏) ③ `mid±1` 的 `+1/-1` 不能少 (跳過已比過的 mid + 保證每圈前進, `l=mid` 會死迴圈)；每圈砍半 → **O(log n)** 時間 O(1) 空間 (log 的正主: 100萬→20步) |
| 開閉區間配對規則 (Binary Search, 通用) | `while` 要不要加 `=`、`r` 要 `mid` 還是 `mid-1`, **是同一個決定**, 判準只有一句: **「mid 這一格檢查完之後還需要留著嗎?」** 不需要留 (有 target 可命中, 或它有證人證明出局) → 兩邊都跳過 mid (`l=mid+1` / `r=mid-1`) → 區間會縮成空的 → 配 `while l <= r` + 迴圈外 `return -1`。需要留 (沒 target 可命中, mid 自己可能就是答案) → `r=mid` 留住它 → 區間縮成單點 → 配 `while l < r` + 迴圈外 `return nums[l]`。**配錯就死**: `l<=r` 配 `r=mid` → `l==r` 時 `mid=l`, `r=mid=l` 區間不再變小 → **死迴圈**; `l<r` 配兩邊 `mid±1` → 可能把答案本人丟掉。#704/#74 走前者, #153 與所有「找邊界」題走後者 |
| Rotated Array 找最小值 / #153 (Binary Search) | 旋轉 = 把 sorted array 切一刀、後半段搬到前面 → 長相是 `[高的第一段][低的第二段]`, 結構保證 **第一段的每個元素 > 第二段的每個元素**; 找最小值 = 找斷崖底部 = 第二段的第一格。`nums[r]` 是免費地標 (**永遠落在尾段**), 拿 `nums[mid]` 跟它比: `nums[mid] > nums[r]` → mid 在第一段, **`nums[r]` 就是它的證人** (比它小) → 含 mid 的左半整塊安全丟掉 `l=mid+1`; 否則 mid 在第二段, **自己可能就是答案** → `r=mid` 不能丟。`while l<r` 收斂到單點, 回 `nums[l]`。**沒旋轉的特例自動答對** (整段遞增 → 每圈都往左收 → 收到 index 0), **零行特例** — 這就是「比 `nums[r]`」勝過「比 `nums[l]`」的理由 (比 `nums[l]` 得多寫 `if nums[l] < nums[r]: return nums[l]` 擋特例) — O(log n) 時間 O(1) 空間 |
