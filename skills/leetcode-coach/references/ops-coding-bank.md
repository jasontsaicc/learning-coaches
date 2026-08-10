# Ops Coding Bank(骨架,內容待補)

<!-- 模組定位見 docs/plans/2026-08-11-module-roadmap.md。
     每月一次 LC 驗收場換成本檔題目:限時 30 分鐘、Python、pytest harness 驗收。
     考的是 SRE coding 輪的實務半場,不是算法。 -->

格式(每題):題目敘述 / 給定輸入(log 檔或 API spec)/ 驗收測資 / 評分維度(正確性、邊界、可讀性)/ 限時。

| # | 題型 | 核心肌肉 | 狀態 |
|---|------|---------|------|
| 1 | log 解析:從 nginx access log 找出 top-N 異常 IP 與時間分佈 | streaming 讀檔、dict 聚合、不整行防禦 | 待補 |
| 2 | API 批次工具:帶 retry + backoff + rate limit 的批次查詢 | 錯誤處理、冪等、退避 | 待補 |
| 3 | 併發抓取:N 個 endpoint 併發 health check 加逾時 | threading/asyncio 擇一、timeout 邊界 | 待補 |
| 4 | 設定檔 diff:兩份 YAML 找語意差異(忽略順序與註解) | 遞迴比較、正規化 | 待補 |
