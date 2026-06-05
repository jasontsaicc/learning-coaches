# Todo — leetcode-coach skill 改進

## 目標（來自使用者）
- 教學深度：面試導向，足夠應付 Google 面試，不過度挖深
- 解答取向：用最直覺的路徑走到**最佳解**，禁止為炫技而優化，好懂優先
- 視覺化：解說時多用圖
- 節奏：加「快速模式」（可跳 mock + 簡化 gate）
- 筆記：加圖解區

## 計畫（修正：不做圖庫，改當場畫）
- [x] ~~新建 diagram-library~~ → 取消（罐頭圖不如用真實數字當場畫）
- [x] 1. 改 `SKILL.md`
  - [x] Core Teaching Methods 加「Draw to Teach」小節 + 3 個風格範例
  - [x] Step C / Step E：強制用學生當下數字畫圖
  - [x] 深度校準：最直覺路徑走到最優、Google bar 非 research bar
  - [x] 加 Fast Mode（routing #6 + Fast Mode 小節）
  - [x] Key Principles 更新（#3 改 clearest optimal、新增 #4 畫圖）
  - [x] Step H：把圖存進筆記
- [x] 2. `pattern-cheatsheet.md`：不動
- [x] 3. 改 `references/notes-template.md`：加 `🖼️ 圖解` 區
- [x] 4. 驗證：Two Sum live demo（Step C/E 圖 + 深度校準 + Fast Mode）→ 使用者 OK
- [x] 5. 完成

## Review
改動摘要：
- SKILL.md 509 → 572 行
- 新增「Draw to Teach」教學法 + 3 個 ASCII 風格範例（Two Sum hashmap、Two Pointers、Sliding Window）
- Step C/E 強制「用真實數字畫圖、至少 2-3 步變化」
- Step E 加深度校準 blockquote：達最優 Big-O 但走最直覺路徑、跳過 research-grade 微優化
- 新增 Fast Mode（保留教學+畫圖，跳 mock + 簡化 gate；Phase Gate 永遠跑完整）
- notes-template 加 🖼️ 圖解 區
