# Day 04-05: Load Balancer & Reverse Proxy

> Status: ✅ 完成

---

## 📝 One-liner

Load Balancer 把流量分配到多台 backend server，達成 high availability、horizontal scalability、零停機部署。

## ⚖️ Trade-off

- 選 L7 (ALB) 而不是 L4 (NLB)：因為 microservices 需要 path-based routing（`/users → user-service`），代價是多了 HTTP parsing 的 latency
- 選 Least Connections 而不是 Round Robin：當 request 處理時間差異大時，動態分配比固定輪流好
- DNS-based LB 只適合 global routing：TTL cache 導致 stale IP，region 內還是需要 ALB/NLB

## 📈 Scale trigger

超過 10K QPS + microservices 架構 → 需要兩層 load balancing：DNS（Route 53）做 region routing，ALB 做 service routing。

## 🔧 DevOps angle

- ALB target group health check：`/health` endpoint，interval 30s，unhealthy threshold 3 次
- Connection draining（deregistration delay）：預設 300s，API response < 5s 的話設 30s 就夠
- NLB 支援 Elastic IP（固定 IP），ALB 不行
- Route 53 weighted routing 做 canary deployment（90/10 流量分配）

---

## 核心概念

### LB 解決的 3 個問題

| 問題 | 沒有 LB | 有 LB |
|------|---------|-------|
| Single Point of Failure | Server 掛 = 全掛 | LB 把流量導到健康的 server |
| Scalability 上限 | Vertical scaling 有天花板 | Horizontal scaling，加 server 就好 |
| 部署要停機 | Deploy = downtime | Rolling update + connection draining |

### Reverse Proxy vs Forward Proxy

| | Forward Proxy | Reverse Proxy |
|---|---|---|
| 位置 | Client 前面 | Server 前面 |
| 保護誰 | Client（隱藏 client IP） | Server（隱藏 server IP） |
| 例子 | VPN、公司 proxy | Nginx、ALB |

> LB 是 Reverse Proxy 的一種**功能**。

### DNS 基礎

**查詢流程：**
```
Browser Cache → OS Cache → Recursive Resolver → Root Server → TLD (.com) → Authoritative NS → 拿到 IP
```

一層一層往下問，像問路一樣：「我不知道，但你可以去問那個人。」

**Record 類型：**

| Record | 用途 | 例子 |
|--------|------|------|
| A | 域名 → IPv4 | `google.com → 142.250.80.46` |
| AAAA | 域名 → IPv6 | `google.com → 2607:f8b0:...` |
| CNAME | 域名 → 另一個域名（別名） | `www.google.com → google.com` |

**TTL trade-off：** 短 TTL = failover 快但 DNS query 多。長 TTL = query 少但換 IP 生效慢。

### DNS-Based Load Balancing（Route 53）

| Policy | 怎麼選 | 用途 |
|--------|--------|------|
| Simple | 隨機回傳 IP | 最基本 |
| Weighted | 按權重比例 | Canary deployment |
| Latency-based | 離 user 最近的 region | Multi-region 架構 |
| Failover | Primary 掛了 → 切 Secondary | Disaster recovery |
| Geolocation | 按 user 所在國家 | GDPR 合規 |

**限制：** TTL cache 住舊 IP → server 掛了 client 還繼續連。DNS-based LB 只做 global routing，region 內要靠 ALB/NLB。

### L4 vs L7 Load Balancing

| | L4（NLB） | L7（ALB） |
|---|---|---|
| 看什麼 | IP + Port（TCP/UDP） | HTTP headers、URL、cookies |
| 速度 | 快（不解析 HTTP） | 慢一點（要解析內容） |
| 路由方式 | 按 connection | 按 path、header、host |
| 適用場景 | 高 throughput、gRPC、遊戲 | Microservices、SSL termination |
| 比喻 | 郵局看地址分信 | 秘書看內容轉給對的部門 |

### LB Algorithms（記法：RWLI）

| Algorithm | 怎麼分配 | 最適合 |
|-----------|---------|--------|
| **R**ound Robin | 輪流 | Server 規格一樣，request 差不多 |
| **W**eighted Round Robin | 按權重輪流 | Server 規格不同 |
| **L**east Connections | 看當下最少連線的 | Request 處理時間差異大 |
| **I**P Hash | hash(client IP) → 固定 server | 需要 session affinity |

> 面試 tip：先說 Round Robin 夠用，如果 response time 差異大再換 Least Connections — 展現 trade-off 思維。

### Health Checks、Sticky Sessions、Connection Draining

**Health Checks：** LB 定期戳 `/health`，連續 3 次失敗 → 標記 unhealthy → 停止導流量。

**Sticky Sessions：** 用 cookie（SERVERID=A）讓同一個 user 永遠到同一台 server。缺點：server 掛了 session 全丟。**更好的做法：external session store（Redis）→ stateless approach。**

**Connection Draining：** 下線 server 時，先停新 request，等現有 request 處理完（30-300s）才移除。

---

## 📡 Observability Mini

| 項目 | 定義 |
|------|------|
| SLI | Backend healthy target 百分比 |
| SLO | 99.95% availability |
| Alert | 5xx error rate 的 burn-rate |
| Dashboard | Active connections、request rate、response time（P50/P99） |

---

## Day 5 PoC 實驗紀錄

### 架構
```
Client → Nginx L4 (port 8082) → app1, app2, app3
Client → Nginx L7 (port 8081) → app1, app2, app3
```
- Go app：3 個 endpoint（`/`, `/health`, `/metrics`）+ failure injection（`FAIL_RATE` env var）
- 程式碼：`projects/load-balancer/`

### 實驗 1：L7 Path Routing ✅
- L7 打 `/api` → response header 有 `X-Route: api-backend`（Nginx `location /api` 加的）
- L4 打 `/api` → **沒有** `X-Route` header
- **結論**：L4 用 `stream` block，只看 TCP，不拆 HTTP → 無法做 path routing。L7 用 `http` block，能看 URL path。

### 實驗 2：Failure Injection ✅
- 設定 app1 `FAIL_RATE=0.5`（50% 回 500）
- Nginx **仍然把 request 分給 app1** — 因為預設只做 TCP health check，不看 HTTP status code
- **結論**：Nginx 預設不會因 500 移除 server。Production 要設 health check path + unhealthy threshold（ALB 會做）

### 實驗 3：Load Test ✅
- 用 `hey` 壓測：`~/go/bin/hey -n 1000 -c 50 http://localhost:<port>/`
- 結果：

| Metric | L4 (port 8082) | L7 (port 8081) |
|--------|---------------|----------------|
| Requests/sec | ~4,465 | ~2,317 |
| Avg latency | ~9.6ms | ~20.1ms |
| P99 latency | ~32ms | ~59ms |

- **結論**：L4 約 2x faster，因為不需要 parse HTTP。L7 較慢但能做 path-based routing。
- **Trade-off**：速度 vs 路由能力。Microservices 需要 L7，pure TCP throughput 用 L4。

---

## 🗣️ English Practice

| My Answer | English Polish |
|---|---|
| LB is put on front server can let client don't need know all server ip, can hide protect server, and can make HA | A Load Balancer sits in front of the servers so clients don't need to know individual server IPs. It hides and protects backend servers, enables high availability, and allows dynamic horizontal scaling. |
| forward proxy is protect client like VPN can hide client ip, reverse proxy can hide server ip, protect server ip address | A forward proxy protects the client by hiding the client's IP — like a VPN. A reverse proxy protects the server by hiding the server's IP address. |
| deploying a new version and want 10% traffic first, like canary release can use Route 53 weighted set DNS base LB | For deploying a new version with only 10% of traffic, like a canary release, I would use Route 53 weighted routing to set up DNS-based load balancing — 90% weight to the old version, 10% to the new version. |
| microservices I would like use L7 LB, because need use path routing | For microservices, I would use an L7 load balancer because we need path-based routing to direct requests to different services. |
| like game server and is million level connections and latency need very fast I would like use L4 LB | For a game server handling millions of concurrent TCP connections with ultra-low latency requirements, I would use an L4 load balancer since we don't need HTTP parsing. |
| use sticky session in cookie write serverid or can use external session store like Redis, this is the stateless approach | Two solutions: use sticky sessions with a server ID cookie to pin users to the same server, or better — use an external session store like Redis so all servers share session state. The Redis approach is the stateless design, which is preferred. |
| if need use path routing like microservice need use L7 | If we need path-based routing, like in a microservices architecture, we need to use L7. |
| L4 ok i get it like aws nlb | L4 supports static IP — like AWS NLB which supports Elastic IP. |
| sticky sessions can keep user on the same backend, but can use external session store like redis let client always to same session store do stateless | Sticky sessions keep users on the same backend, but if that server goes down, the session is lost. A better approach is using an external session store like Redis so all servers share state — this is the stateless design. |

---

## 🔴 My Mistakes & Misconceptions

| What I Thought | Reality | Why I Was Wrong |
|---|---|---|
| 說成 "least robin" | Round Robin 和 Least Connections 是兩個獨立 algorithm | 沒把四個名字記清楚，用 RWLI 記法：Round Robin → Weighted → Least Connections → IP Hash |
| Request 處理時間不同 → 用 Weighted Round Robin | Weighted 是給 server 規格不同用的（靜態），處理時間不同要用 Least Connections（動態） | 混淆了「server 能力不同」和「request 負載不同」兩種情境 |
| Simon Drill 完全想不起 LB Algorithms | 四個 algorithm 各有明確 use case，要記住名字 + 適用場景 | 只理解了概念但沒記住名字，recall 時腦袋一片空白 |
| DNS-based LB 缺點想不起來 | TTL cache 導致 stale IP，DNS 沒有 real-time health check | 只記住了 Route 53 的 routing policies，沒記住 limitation |
| 8.8.8.8 是 ISP 的 DNS | 8.8.8.8 是 Google Public DNS resolver，ISP 有自己的 resolver | 混淆了 recursive resolver 的來源，8.8.8.8 是公開的，ISP resolver 是另一個 |
| Sticky session 和 Redis 是同一種做法 | Sticky session 用 cookie 綁定 server（有風險），Redis 是 external store 做 stateless（替代方案）| 兩個是相反的策略，不是同一件事 |
| Sticky session 唯一風險是 session loss | 還有 uneven load distribution — heavy users 被 pin 住導致某些 server 過載 | 只想到 server 掛掉的情況，沒想到 load imbalance |
