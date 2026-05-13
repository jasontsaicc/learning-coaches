# Day 14 — Security & Authentication (Part 3 / Session 21)

> Status: 🟢 **Complete** (All 8 chunks done)
> Date: 2026-05-13
> Phase 1
> **⬅️ Continued from [day14-security-auth-pt2.md](day14-security-auth-pt2.md)**

---

## Session 21 Coverage

- ✅ Chunk 6: OAuth 2.0 — Q2/Q3 resolved + Authorization Code Flow
- ✅ Chunk 7: Observability Mini for Security
- ✅ Chunk 8: Scale Trigger + DevOps Angle
- ✅ Step D: JWT PoC in Go (Light Code)
- ✅ Step E: Simon Drill (all 3 questions passed)

---

## Chunk 6: OAuth 2.0 (完整版)

### Q2 — 為什麼 Auth Server 跟 Resource Server 要分開？

**核心：signing capability isolation（簽名能力隔離）**

| Server | 持有的東西 | 被打下後的爆炸半徑 |
|--------|-----------|-----------------|
| Auth Server | private key（能 mint token） | 攻擊者可以偽造任意身份 |
| Resource Server | public key（只能 verify） | 攻擊者只能讀取那一個 service 的資料 |

把「能簽 token 的東西」跟「只驗 token 的東西」分開，Resource Server 被打下不會升級成身份系統淪陷。

---

### Q3 — 三個 Disaster 對應 OAuth 解法

| Disaster | 問題本質 | OAuth 解法 |
|----------|---------|-----------|
| No Scope | 密碼 = 全部存取權 | Access Token 帶 scope（只能讀 Drive，不能碰 Gmail） |
| No Revocation | 撤銷成本太高所以沒人做 | 短命 access token + 長命 refresh token → 撤銷從「核彈」變成「按鈕」 |
| Transitive Trust | 密碼給 A，A 洩漏給 B，鏈不可控 | 密碼只給 Auth Server（Google），第三方 app 只拿到有限 token |

**No Revocation 的深層理解**：本質不是「無法撤銷」，是「撤銷成本太高所以沒人做」。OAuth 的解法是把 credential 拆成兩層生命週期——短命的 stateless access token（換來效能）配上長命的 stateful refresh token（換來精準撤銷）。

---

### Authorization Code Flow

```
User → Client: "Login with Google"
Client → Auth Server: 302 redirect (scope, redirect_uri, state)
User → Auth Server: 登入並核准 scope
Auth Server → Client: redirect back with ?code=xxxxx   ← 短命 code
Client → Auth Server: POST /token (code + client_secret)   ← server-to-server
Auth Server → Client: { access_token, refresh_token }
```

**為什麼要多「code 換 token」這一步？**

核心 threat model：**Browser is hostile territory**

直接把 token 放在 redirect URL，會洩漏到：history、referrer header、browser extensions、access logs、XSS。

Code 只是一次性「取貨憑證」，真正的 token 交換在 **server-to-server**（帶 `client_secret`），不經過 browser。

**通用設計原則**：當你必須讓一個 valuable thing 經過你不能完全控制的通道時，不要傳這個 thing 本身，傳一個必須在安全通道才能兌換的 claim。

---

## Chunk 7: Observability Mini

| Element | Security 特定 |
|---------|--------------|
| SLIs | Auth success rate, token validation latency (P99), failed login rate |
| SLO target | Auth success rate ≥ 99.9%、token validation P99 < 50ms |
| Alerts | Failed login rate > 5% in 5 min → brute force；JWT validation error spike → key rotation issue |
| Dashboards | Login success/fail ratio、token issuance rate、4xx/5xx on auth endpoints |

**重要陷阱**：要同時 alert「failed login rate 太高」AND「failed login rate 突然是 0」。
「完全沒事」跟「完全死透」在這個指標上看起來一模一樣——都是 0。

---

## Chunk 8: Scale Trigger + DevOps

### Scale Trigger

| 規模 | 瓶頸 | 解法 |
|------|------|------|
| 單機 Auth Server | SPOF，Auth 掛全站掛 | Auth Server 水平擴展 + LB |
| JWT key rotation 麻煩 | 所有 RS 要同步 public key | JWKS endpoint（RS 自動 fetch 最新 public key） |
| 多 service 各自做 auth | 邏輯重複、不一致 | API Gateway 集中做 token validation |
| Session store 變瓶頸 | 單台 Redis 撐不住 | Redis Cluster + session replication |

**JWKS 設計精髓**：把「推送」變成「拉取」——RS 自己定期 fetch，不是 Auth Server 廣播。和 CDN pull vs push 是同一個設計模式。

### DevOps Angle

- **AWS Cognito**: managed Auth Server，不用自己維護 JWT signing、user pool、token rotation
- **OIDC**: OAuth 2.0 的 identity 延伸，多了 `id_token`（who you are，不只是 what you can do）
- **Secrets rotation**: `client_secret`、DB password 定期 rotate，用 AWS Secrets Manager 自動換

---

## Step D: JWT PoC (Light Code)

**專案位置**: `projects/day14-jwt/main.go`

核心：不用外部 library，只用標準庫手刻 JWT issue + validate。

```go
// issue: header.payload → HMAC-SHA256 with secret → append signature
// validate:
//   1. split by "."
//   2. re-compute signature, compare with hmac.Equal (not ==, timing attack)
//   3. base64-decode payload, unmarshal Claims
//   4. check Exp vs time.Now().Unix()
//   5. return Claims.Sub
```

**為什麼用 hmac.Equal 不用 ==？**
`==` 遇到第一個不同字元就 return（short-circuit），攻擊者可以量測 response time 逐漸猜出簽名。`hmac.Equal` 永遠花一樣的時間，timing attack 無效。

---

## Simon Drill 結果

| 題目 | 結果 |
|------|------|
| JWT 為什麼 stateless？ | ✅ |
| Refresh Token 存在理由？ | ✅ 「拆到兩個不同生命週期去解衝突」 |
| Authorization Code Flow 為什麼要繞一圈？ | ✅ 「Browser is hostile territory」 |

---

## 🔴 My Mistakes & Misconceptions

（本 session 主要是補上 Session 20 遺留的兩個洞）

| 錯誤 | 正確理解 |
|------|---------|
| OAuth Q2 說「不同 api」| 重點是 signing capability isolation，不是功能分工 |
| OAuth Q3 當初完全跳過 | 每個 OAuth 元件都對應一個 disaster，要建立「設計元件 = 對應一個痛點」的思維 |
| No Revocation 以為只是「無法撤銷」| 真正問題是「撤銷成本太高所以沒人做」，解法要讓撤銷變便宜 |

---

## 🗣️ English Practice

| My Answer | English Polish |
|-----------|---------------|
| 把能簽 token 的東西跟只驗 token 的東西分開，讓 Resource Server 不持有 private key | "We separate signing capability from verification capability — the Auth Server holds the private key and can mint tokens, while Resource Servers only hold the public key and can verify. A compromised Resource Server cannot issue new tokens, so the blast radius stays contained." |
| No Revocation 的本質不是無法撤銷，是撤銷成本太高所以沒人做 | "The real problem with No Revocation isn't that revocation is impossible — it's that the cost is so high that nobody does it. OAuth solves this by splitting credentials into two lifecycle layers: a short-lived stateless access token for speed, and a long-lived stateful refresh token for precise revocation." |
| browser is hostile territory | "The Authorization Code Flow exists because the browser is hostile territory. Any token in a redirect URL is exposed to history, referrer headers, extensions, and logs. By exchanging a short-lived code server-to-server, the actual token never touches the browser." |

---

## 🎤 How to Say It in Interview

**One-liner**: "Security in distributed systems means separating what can issue credentials from what can consume them — OAuth solves password-sharing disasters by introducing scoped, revocable access tokens exchanged through a trusted server-to-server flow."

**If asked about JWT vs Session**: "I'd ask about revocation requirements first. If we need sub-second revocation (banking, regulated industries), go stateful Session. If we need stateless horizontal scale across microservices, go JWT with short TTL plus refresh token for revocation."

**If asked about OAuth**: "OAuth solves three password-sharing disasters: no scope, no revocation, and transitive trust. The Authorization Code Flow specifically avoids putting tokens in the browser URL by using a short-lived code redeemed server-to-server."

---

## 📌 Key Vocab (Session 21 新增)

| 中文 | English |
|------|---------|
| 簽名能力隔離 | signing capability isolation |
| 時間側信道攻擊 | timing attack |
| 敵對環境 | hostile territory |
| 兌換憑證 | redemption claim / one-time code |
| 金鑰輪換 | key rotation |
| JWKS 端點 | JWKS endpoint (JSON Web Key Set) |
