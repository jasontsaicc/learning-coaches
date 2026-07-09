# SD Interview Prep — Project Settings

> SD Coach skill (`sd-coach`) handles all teaching logic.
> This file only contains project-specific preferences that the skill doesn't know.

---

## Language Rules (English 70% / 繁中 30%)

- **AI output**: Default to English, switch to 繁中 only when needed for clarity
  - Concept explanations: English first — only use 繁中 for Feynman-style "白話解釋" when concept is hard to grasp
  - Questions to student: Primarily in English
  - Tables and comparisons: Headers in English, content bilingual
- **Student responses**: Try English first, fall back to 繁中 for unknown parts
  - AI should gently prompt: "Can you try explaining that in English?"
  - If student mixes 繁中 in their English response → that's OK and expected
  - **English Polish**: After each student response, AI provides:
    ```
    💬 English Polish: "[natural English version of what you said]"
    ```
  - Only show the polished version — don't explain grammar rules unless asked
- **Notes**: Section headers in English, content 以繁中為主 + 英文術語
  - 筆記是給自己複習用的，中文比重高一點提升複習意願
  - **必須包含 `🗣️ English Practice` section**：
    ```
    ## 🗣️ English Practice
    | My Answer | English Polish |
    |---|---|
    | 我的原始回答 | 優化過的面試建議回答 |
    ```
- **Technical terms**: Always English
- **Goal**: Build the habit of thinking and articulating SD concepts in English for interviews

---

## Project Structure

| Path | Purpose |
|------|---------|
| `progress.md` | 進度追蹤（skill 讀寫這個檔案）|
| `notes/` | 每日筆記 `dayXX-topic.md` |
| `projects/` | Go PoC 專案 |
| `docs/` | 規劃文件 |

這個 repo 只放學習產出。課綱與教學模板（`curriculum.md`、`story.md`、`notes-template.md` 等）屬於 skill，唯一來源是 `system-design-coach/references/`。不要在這裡放副本，之前放過一份，結果三個地方都有 curriculum，改課綱時分不清該動哪個。

---

## PoC 偏好

- 語言：Go（練語法 + 語感）
- 鼓勵手打 code，不要 copy-paste
- 預設 Full PoC（Go + Docker），沒環境時用 Light Code

---

## 舊版參考

`pre-skill` 分支保留了導入 skill 前的完整 CLAUDE.md 和 CURRICULUM.md。
