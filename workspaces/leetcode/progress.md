<!-- Schema: docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md 第 8 節。
     這個檔只回答「現在在哪」,不回答「你欠什麼」。
     不加到期日欄位、不加未結狀態、不加順延計數。重建前的舊 state 在 archive/pre-rebuild/。 -->

# leetcode

- 今天做到:2026-09-11。**#141 收掉了**:drill.py 冷寫走到階 3(dummy 問對了、
  兩指標起手式與 `while` 條件想不起來),對照打後 7/7 PASS,`return False` 縮排自己貼對
  (頭號慣犯這次沒中)。溫度計 ② 答「還是抓得到」**正確**,「多花步數」錯(同或更少)。
  **coach 的提示與 notes.md 原本寫錯**(說走 3 步會跳過 0),已模擬驗證並更正:
  差距在環上取模,任何 s>=2 都抓得到;用 2 的真正理由是 #142 環入口推導依賴 fast=2*slow。
  接著開 tree:**#226 龜模式全跑完**(拷問 ①②③④ + 溫度計 ②),drill.py 8/8 綠,五行冷寫一次過。
- **★ 2026-09-10 學員揭露:他是心盲症(aphantasia)患者,腦中無法產生視覺影像。**
  今天兩次卡住(委派、base case)都是補上圖之後當場通過。已寫進 `~/.claude/CLAUDE.md`、
  `engine/ENGINE.md` Locked 表、`leetcode-coach/SKILL.md`:**任何抽象機制都要真的畫出來,
  含看不見的部分(`None` 子節點、暫停中的 stack frame、被覆蓋前的舊值);「想像一下」是空指令,禁用。**
- 2026-09-10 #226 診斷:拷問 ① 三零件只講對 1 個(交換);base case 答成「沒有左右葉子就 return None」
  (少了 None 這一格的畫面);「委派」抽象問法問不出來,**指著具體的圖問「6 和 9 是誰換的」就出來了**,
  學員自己講出「把自己再當成 root」。拷問 ③ 兩個空格全對,**沒踩 tuple 拆兩行的坑**。
  溫度計 ② 不會 -> 要求逐格帶跑,補上第 05 節(看不見的 None + 7 格 call stack)。
- 前一場 2026-09-07。開場默寫(隔堂留存測)+ #141 圖解頁產出。留存測結果:#206 起手式
  三天前錯今天全對、loop 4 行順序全對、`return prev` 對;#21 (a)(b)(c) 對,**(d) 尾段
  `list1 or list2` 走到階 2 才出來(9/04 也沒出來,重複第 2 次,已升級到 my-common-bugs)**。
  學員自己問出「head 和 curr 是等於還是指向」,補上「看 `=` 左邊有沒有 `.`」判準
  (換標籤 vs 改物件內部),這條直接接到 #141 要用 `is` 不用 `==`。
- #141 開到拷問 ① 學員下班,圖解頁已產出交給他自讀。**下次直接從拷問 ② 起跑。**
- 模式:速刷 = 每題冷寫 → 卡住協定 → harness → 變形題。學員確認這個節奏 ok。
  診斷:零件(prev=None、存在改之前、dummy/tail 分工)分開問都懂,從空白頁組不起來;
  9/07 複測有改善,骨架默得出來,弱點收斂到「尾段 invariant」與「指標角色的精確描述」。
- **2026-09-10 續場(下班前)**:學員自主做完 #141 的隔堂留存測(卡住看答案,見上方),
  帶著這個結果進場。順手補了兩題 notes.md 跟 progress.md 沒同步的舊帳(#141/#226 進度欄位
  停在 09-07/教學當下,已補到跟這裡一致)。額外教學:`==` vs `is`(`ListNode` 沒宣告
  `__eq__`,`==` 預設退回比 identity,跟 `is` 一樣;學員原本以為 `==` 一定比 value,
  已澄清,寫進 #141 圖解頁「這次的釐清」)。開場默寫 `dfs(node)` 三零件模板**沒寫出來**,
  對照抄一次(第三層留存測第 2 次考,這次沒過,不記債)。
  接著開 **#104 Max Depth**:拷問① 學員先答「隨便選一邊 +1」,用具體反例
  (`2` 只有左小孩 `4`,選右邊漏算整條左邊)糾正成「取 max」,Socratic 帶出完整公式
  `max(left, right) + 1`。已組出完整函式,開始 dry run(1-2-3-4 樹),coach 畫出完整
  call stack 圖。**收在「`dfs(1)` 最後 `max(2,1)+1` 這兩個數字從哪來」這題,學員還沒
  答就下班,不記債,下次直接接著問。**

- **2026-09-11 #104 續場**:開場默寫(第三層留存測,`dfs` 模板第 3 次考)**沒過**,三格全錯:
  `if not root`(參數叫 `node`,在裡面檢查 `root` 會無限遞迴)、`return False`(型別錯,
  但 Python `bool` 是 `int` subclass 所以這題會意外跑對)、`dfa(left)`(拼字 + `left` 不在 scope)。
  對照抄一次,不記債。接著收 dry run:**「`max(2,1)` 的兩個數字從哪來」第一次答對一半**
  (`2` 對;`1` 指到 `dfs(2)` 那行的 `max(1,0)`,差一代輩分),narrowing 後答出 `dfs(3)` **正確**。
  結構重點已講明:`max(left,right)` 兩格被 `node.left` / `node.right` 綁死,孫子輩不會直接跳上來。
  **拷問 ② 不會**(`dfs(4)` return 之後控制權去哪),走卡住協定階 2 仍不會,學員主動要求 eli5。
  **→ 產出圖解頁**(見下方 URL),第 04 節用 **11 格分鏡**把整疊 call stack 畫出來:
  疊紙/撕紙兩種動作、暫停中 frame 卡在哪一行、`▢` 未填格、五個 `None` 子節點全部畫實。
  **升級 my-common-bugs 表二第 2 列**:「`return` 做的兩件事只認得第一件」(3 次,吸收原
  `print`/`return` 那列);表一「變數名手滑」3→4。
  **收在拷問 ③ 之前**(學員要先自讀圖解頁第 04 節)。下次從拷問 ③ 填空起跑,再走 ④ + 溫度計 ②。

## Pattern 狀態

| Pattern | 圖解看過 | 對照打過 | 自己寫出來 | 口訣 |
|---|---|---|---|---|
| Linked List 反轉(prev/curr/nxt) | ✓(notes) | ✓ | ✅ 9/07 隔堂冷默全對(起手式+4 行+return) | ✓ |
| Linked List 合併(dummy + tail) | ✓ | ✓ | 🟡 骨架冷默出來,尾段仍需階 2 提示 | ✓ |
| Fast-slow pointer(龜兔) | ✓(9/07 圖解頁) | ✓ 9/10 | 🟡 9/10 冷寫走到階 3;harness 7/7 綠 | ✓ |
| Tree DFS 遞迴(base/本層/委派) | ✓(9/10 圖解頁) | ✓ 9/10 | ✅ 9/10 #226 五行冷寫一次過 8/8;續場開場默寫沒過,對照抄一次 | ✓ |
| Tree DFS 吃下屬回傳值(#104 `max(left,right)+1`) | ✓ 9/11 圖解頁(11 格 call stack 分鏡) | | 🟡 公式靠階梯提示推出;dry run 數字出處答對;**call stack 控制權轉移仍要看圖才過** | ✓ 先問兩邊再算自己 |
| Heap k-way merge(每條一個 head) | ✓ | | ✓ | ✓ |
| Hashmap + 雙向鏈(LRU) | | | | |

## 做過

- **Layer 0 執行模型**:跑了概念 1(變數是貼標籤)、4(縮排歸誰管)、5(迴圈變數每圈重算)、
  7(node / pointer / `.next`)。概念 2(`//`)、3(list 方法名)、6(`while` 條件)當天跳過,
  linked list 用不到,卡到再翻。
- **#21 Merge Two Sorted Lists** — `linked-list/merge-two-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/0a337a0c-2d4f-47f1-b00a-712a79221119
  已完成:圖解頁、L6 面試逐字稿(含 code 對照表)、pytest harness;2026-08-31 學員回報早上完成。
  2026-09-04 速刷:冷寫卡在 loop body(有 dummy 沒 tail、把 tail 角色跟 #206 的 prev 混),
  逐塊補完 harness 10/10 綠(含 10 萬×2 + 節點重用)。變形題「尾段為何能整段掛」沒答出,已講。
- **#23 Merge K Sorted Lists** — `linked-list/merge-k-sorted-lists/`
  圖解頁:https://claude.ai/code/artifact/65a51c4d-d03a-4161-8140-0f8b9669254f
  首場產出:圖解頁、min-heap 主解、divide-and-conquer follow-up、L6 面試逐字稿(含 code 對照表)。
  2026-09-02 複盤:merge two → naive merge-one-by-one(TLE 原因)→ heap,拷問 ① 補上,
  學員獨立寫出 heap code(抓到漏 `import heapq`)。
- **#141 Linked List Cycle** — `linked-list/linked-list-cycle/`
  圖解頁:https://claude.ai/code/artifact/54ce4b5d-bf52-44e5-958b-a5f35f6f44fd(舊連結已失效,09-10 重發)
  2026-09-07:圖解頁產出(含 L6 逐字稿、逐輪模擬表、模板遷移表)。拷問 ① 未答(學員下班)。
  未做:solution.py、harness、拷問 ②③④、溫度計 ②。重點:換的是空間不是時間;
  差距每圈減 1 跳不過 0;`while fast and fast.next`;比指標用 `is`。
- **#226 Invert Binary Tree** — `tree/invert-binary-tree/`
  圖解頁:https://claude.ai/code/artifact/c1e8edb8-fa3c-45b7-a9c8-16735b026c16
  2026-09-10:遞迴教材(三零件、相信下屬、call stack 便條紙、迴圈 vs 遞迴對照表)、
  圖解頁、drill.py(8 組 case,空 stub 7/8 FAIL、參考解 8/8 PASS 已驗)、L6 逐字稿。
  2026-09-10 全跑完:拷問 ①②③④ + 溫度計 ②,drill.py 8/8 綠。
  第 05 節「逐格走一次」是為心盲症加的:看不見的 None 子節點圖 + 7 格 call stack。
- **#104 Maximum Depth of Binary Tree** — `tree/maximum-depth-of-binary-tree/`
  圖解頁:https://claude.ai/code/artifact/e77e837d-6fab-4986-98f9-02920132a8f5
  2026-09-10:Socratic 推出 `max(left,right)+1`,dry run 走一半。
  2026-09-11:dry run 收掉(數字出處答對);拷問 ② 不會 → 產出圖解頁(11 格 call stack
  分鏡 + L6 逐字稿 + 這次的釐清)、`drill.py`(9 組 case,空 stub 9/9 FAIL、參考解 9/9 PASS 已驗)。
  未做:拷問 ③④、溫度計 ②、solution.py。詳細記錄見該題 `notes.md`。
- **#146 LRU Cache** — `hashmap-doubly-linked-list/lru-cache/`
  圖解頁:https://claude.ai/code/artifact/69673f1c-d044-49b9-bb01-42082143e263
  本場產出:圖解頁(寄物間號碼牌比喻)、暴力解對照、L6 面試逐字稿(含 code 對照表)、pytest harness。
- **#206 Reverse Linked List** — `p3-binsearch-linkedlist/reverse-linked-list/`
  2026-08-03 首刷,2026-09-04 速刷:冷寫失敗(`prev = head` 起手錯、組不出 4 步順序),
  對照打 + 變形題(刪 `nxt = curr.next` 會斷鏈)過,清空重打 harness 8/8 綠(1 個手滑自抓)。
  缺 eli5 圖解頁 + L6 逐字稿。

## 接下來

1. **開場先問一句**:「圖解頁第 04 節讀了嗎」。讀過就直接進**拷問 ③**(填空:給三格骨架,
   挖掉 `return 0` 和 `return max(left,right)+1`),再走 ④(在 `drill.py` 冷寫,目標 9/9)
   + 溫度計 ②。變形題已備:「`+1` 拿掉會怎樣」「`max` 換成 `min` 會回什麼」
2. 開場默寫照常考 `dfs` 三格模板(第 4 次)。前兩次都沒過,這次重點看
   **煞車踩的是 `node` 不是 `root`**,以及煞車值有沒有寫 `0`
3. #104 收尾後補:`solution.py`、圖解頁「這次的釐清」再補一輪
3. 之後 #100 Same Tree / #543 Diameter,模板填空
4. Linked list 停在原地,不記債,隨時可回:#143 Reorder List、#146 LRU(拷問 ① 前)、
   #206 缺 eli5 圖解頁 + L6 逐字稿
