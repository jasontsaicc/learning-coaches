# #226 Invert Binary Tree

圖解頁:https://claude.ai/code/artifact/c1e8edb8-fa3c-45b7-a9c8-16735b026c16

模式:龜(遞迴是全新的招,不是任何 linked list 題的換皮)。
Tree pattern 的第一題,也是 Layer 0「遞迴」的教學載體(curriculum 把遞迴排在這裡教)。

## 這題的重點

- 遞迴三零件:base case / 這一層自己做的事 / 委派。寫完問「下屬都做對的話,我這層夠不夠?」
- **相信下屬(recursive leap of faith)**:不要在腦中往下追第二層。要驗的只有 invariant。
- **每個 frame 有自己的 local 變數**。這是學員常犯錯觀念第 1 名(「這行什麼時候被求值」,
  4 次跨題)的樹上版本。逐輪模擬表第 11 步是證據:`invert(4)` 停了 7 步,醒來時 root 還是 4。
- **樹一定要遞迴的理由**:linked list 每個 node 一條路,一個 `curr` 走得完;
  樹每個 node 兩條路,走了左邊右邊要有人記住 -> call stack 幫你記。
- 交換的是**指標**,動一根搬一整包子樹。同 #21「尾段可以整段掛」的直覺。
- `root.left, root.right = root.right, root.left` 不能拆兩行。
  **同 #206 `nxt = curr.next` 的雷家族:要覆蓋之前先存起來。**
  tuple assignment 安全是因為右邊整串先求值。
- 複雜度 O(n) time / **O(h) space,且要講出「這個空間是 call stack」**。說 O(1) 是扣分點。
- 遞迴不比較快。買到的是可讀性,付出的是 function call 開銷 + Python 遞迴上限 (~1000)。

## 模板遷移

`dfs(node)` 通用模板:base case 回什麼 / 這層用 left+right 拼什麼。
#104(回 0,`1+max`)、#100(回 True)、#543(回高度 + 全域最大)。
**#226 是模板最鬆的版本,它不用下屬的回傳值。#104 才開始真的吃「相信下屬」。**

## 檔案

- `drill.py` — 冷寫區 + 8 組 case(含空樹、單邊、滿樹 127 顆翻兩次回原狀)。
  空 stub = 7/8 FAIL,參考解 = 8/8 PASS,已驗。

## 進度

- 2026-09-10:圖解頁 + drill.py 產出。學員先自讀,拷問 ①②③④ + 溫度計 ② 全跑完,
  drill.py 8/8 綠。拷問 ① 三零件只講對 1 個,base case 少了「None 這一格」,指著
  具體圖問「6 和 9 是誰換的」才講出「委派」。第 05 節「逐格走一次」是為心盲症加的:
  看不見的 None 子節點圖 + 7 格 call stack。
