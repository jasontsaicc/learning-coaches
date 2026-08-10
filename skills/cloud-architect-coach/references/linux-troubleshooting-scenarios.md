# Linux Troubleshooting Scenarios(骨架,內容待補)

<!-- 模組定位見 docs/plans/2026-08-11-module-roadmap.md。
     每個情境:一台壞機器 + 症狀描述,學員限時修復,修完講機制。
     ca 30 題題庫(linux-interview-bank.md / interview-simulations.md)當抽考池,本檔只放動手情境。 -->

格式(每個情境):症狀 / 環境準備腳本 / 預期排障路徑 / 考點機制 / 常見錯路 / 限時。

| # | 情境 | 考點 | 狀態 |
|---|------|------|------|
| 1 | 磁碟滿了但 `df` 說沒滿 | deleted-but-open fd、inode vs block | 待補 |
| 2 | load 高但 CPU idle | iowait、D state、`iostat` | 待補 |
| 3 | OOM killer 殺錯人 | oom_score、cgroup limit vs host | 待補 |
| 4 | 連線偶發 timeout | conntrack table、SYN backlog | 待補 |
| 5 | zombie 進程堆積 | wait/reap、PID 1 責任 | 待補 |
| 6 | DNS 每次都慢 5 秒 | resolv.conf timeout、UDP 丟包 | 待補 |
| 7 | 服務起不來:port already in use 但 `ss` 查無 | TIME_WAIT、SO_REUSEADDR、namespace | 待補 |
| 8 | 憑證換了但舊的還在用 | fd 快取、reload vs restart、`lsof` | 待補 |
