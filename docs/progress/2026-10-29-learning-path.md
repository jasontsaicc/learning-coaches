# 2026-10-29 工作紀錄：SD / k8s 學習路徑

## 完成項目

- 盤點 SD、k8s 課綱和 HTML 筆記，整理 Phase → Node → Chunk 藍圖，記錄教材已齊、部分可用與待補範圍。
- SD 學習路徑依 10-29 方案 B 排列：Metrics & Logging → Top-K → Brownfield Migration → Deploy System → Distributed Cache → Payment → Ticket / Flash Sale → News Feed。
- k8s 學習路徑整理 P0–P6 與跨 coach Terraform 接力；P3 自動伸縮依序列出 HPA → VPA → KEDA → CA/Karpenter，保留選修與副線標記。
- 新增 `site/learning-paths.json` 作明確課程目錄資料。SD 42 個、k8s 34 個 node，各 node 有 chunks、教材連結與缺教材狀態。
- SD/k8s 課程頁加入 node 展開、chunk 筆記直連、目前單元定位、階段跳轉及路徑搜尋；舊筆記、練習題、地圖與記憶卡入口保留。
- Build 驗證目錄 ID 唯一、筆記連結位於匯出 allowlist，並只輸出由目前 breakpoint 導出的 node ID，不輸出 breakpoint 文字。
- 採用 Taste app-screen 流程規劃與檢視；目前課程路徑的 1440/768/390 畫面檢查為 0 FAIL，完整截圖已檢視。
- 更新 `site/README.md` 與前端規劃文件，記錄資料來源、互動方式、視覺選擇與驗收狀況。

## 驗證與部署

- `./scripts/lint-all.sh` 通過。
- Playwright 瀏覽器檢查通過：SD/k8s 所有 chunk 連結、鍵盤展開、手機版、搜尋、閱讀、練習、知識地圖、記憶卡及既有錯誤狀態。
- Taste inspector：0 FAIL / 4 WARN。長課程內容延伸到下方；保留練習卡與共用字體既有樣式。
- 部署至 Cloudflare Pages `learning-map`；`learn.jasondevops.space/data.json` 回應 302，確認 Access 登入保護仍啟用。
- 本機 learning-map 靜態服務亦已由更新後的 `site/dist` 提供內容。

## 產出位置

- `docs/plans/2026-10-29-sd-k8s-learning-path.md`
- `docs/plans/2026-10-29-learning-path-frontend.md`
- `site/learning-paths.json`
- `site/app.js`, `site/build.py`, `site/styles.css`
- `site/test_app.mjs`, `site/test_build.py`, `site/browser-check.mjs`

## 待辦

- 逐步補齊標示「部分教材」與「待補 HTML」的主題筆記。
- 本次未部署以外的變更；工作區 k8s progress 檔不在本次提交範圍。
