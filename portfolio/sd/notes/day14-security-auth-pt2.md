# Day 14 — Security & Authentication (Part 2)

> Status: 🟡 **In Progress** (Session 20 — Chunk 5 ✅ + Chunk 6 partial; Chunks 7-8 + Drill pending)
> Date: 2026-05-06
> Phase 1
> **⬅️ Continued from [day14-security-auth.md](day14-security-auth.md)** (Session 19: Chunks 1-4)

---

## Today's Focus

- ✅ Chunk 5: JWT vs Session — 3-scenario decision matrix
- 🟡 Chunk 6: OAuth 2.0 — 4 actors framework introduced; Q2/Q3 of Feynman check + Authorization Code Flow pending

---

## 🔗 Insight from Today

**Stateless vs Stateful 是 SD 反覆出現的軸線。** 今天用在 auth (JWT vs Session)，但同樣的選擇邏輯會在 caching (write-through vs write-back)、LB (sticky vs round robin)、DB replication 重複出現。**Centralized state 在 distributed system 是地獄起點**：所有依賴它的 component 都被它的故障半徑連坐。

**JWT vs Session 不是「新 vs 舊」，是「我有什麼問題要解，這個工具解的問題我有沒有」。** 看到 "auth" 直接想 JWT 是流行病。Senior 訊號 = 看 problem，不看 buzzword。

---

## Chunk 5: JWT vs Session — 3 個情境的判斷矩陣

### 判斷的核心 — JWT 三個 selling points

| JWT 解的問題 | 物理痛點 |
|---|---|
| **(1) Stateless verify** | 避免每 request 重打中央 store |
| **(2) Cross-service trust** | N 個 service 共享身份 |
| **(3) Decentralized auth** | Auth service 掛了不要全平台垮 |

題目就是「對著情境檢查這三個問題存不存在」。

---

### Scenario A — 銀行（Monolith + 1 秒撤銷需求）

| 欄位 | 答案 |
|---|---|
| Choice | **Session** |
| Why | 法規要求 1 秒內踢出 user，stateless 唯一能做的就是等 token 過期。Stateful store 才能立刻刪 |
| Trade-off | 每 request +1ms Redis lookup，加上要營運 Redis (HA、failover、monitoring、backup) |

**進階加分**: 也可以講 Hybrid (極短 TTL 30s JWT + Redis refresh)，但銀行因法規寫死 1 秒，多數選純 Session 求穩。

---

### Scenario B — Microservices 平台（10+ services, polyglot）

| 欄位 | 答案 |
|---|---|
| Choice | **Hybrid (JWT base + RS256 + stateful Refresh Token)** |
| Why | Session 會逼所有 service query 同一個 Redis = **centralized state** → 強耦合、SPOF、latency 累加。JWT 讓每個 service 本地驗 sig，無 network round trip |
| Trade-off | Key management (透過 JWKS 分發 public key)、clock skew (各 service 自己驗 `exp`)、algorithm confusion 攻擊 (e.g., `alg: none`)、**claim staleness** (token 裡的 role 可能 5 分鐘前就 demote 了) |

#### Session 在 microservices 的 4 個物理問題

| 問題 | 物理原因 | 影響 |
|---|---|---|
| **SPOF** | Redis 掛 = 10 個 service 全部不能驗身份 | 整個平台 down |
| **Latency 累加** | 一個 request 過 3 個 service = 3 次 Redis round trip | 純 auth 就吃 3ms |
| **Polyglot 痛苦** | Go/Java/Python 各自的 Redis client + session 序列化方式不同 | 改 schema 要 10 個 service 一起重部署 |
| **Coupling** | 所有 service 都綁 Redis schema | 失去 microservices 獨立部署的最大好處 |

#### HS256 vs RS256 — 為什麼是 RS256？

關鍵動詞區分：**verify vs sign**。

```
HS256 (對稱)：10 個 service 都有 SECRET → 任一被 hack 都能簽假 JWT → 10 個 attack surface
RS256 (非對稱)：Auth service 有 private key 簽，其他 service 只有 public key 驗
              → 被 hack 的 service 只能驗，不能偽造 → attack surface 縮回 1
```

**這就是 principle of least privilege**：給每個 component 剛好夠用的權限，不多。

---

### Scenario C — 個人 blog（單機 + 100 users/day + solo dev）

| 欄位 | 答案 |
|---|---|
| Choice | **Session**（cookie + Postgres row，根本不需 Redis） |
| Why | JWT 的三個 selling points 在這場景**全部不存在**。沒中央 store 壓力可解、沒跨 service 信任問題、沒 scale 顧慮。**KISS + YAGNI** |
| Trade-off | 綁定單機，無法水平擴展。但 100 users/day 根本壓不到，這個 cost 在此場景不痛 |

#### JWT 在這裡帶來的不必要成本

- Secret 管理（環境變數、rotation 邏輯）
- TTL 取捨（要選多久？寫死哪？）
- Revocation 自己補（blacklist / refresh token 一條都不能少）
- Debug 困難（base64 token 眼睛看不出，要寫 decode tool）
- 時鐘問題（即使單機也要驗 `exp`）

#### 反例 vs 正解

> ❌ "我用 JWT 因為以後可能變 microservices"
> ✅ 等真的要拆 service 那天再換 JWT。**簡單的東西容易換**，複雜的東西很難拆。

#### 面試加分句（先發制人講未來路線）

> "If the project ever needs horizontal scaling or microservices, migrating from Session to JWT later is straightforward — the auth flow is encapsulated in middleware."

---

### Chunk 5 Takeaway

```
A 考 revocation         → Session
B 考 distribution        → JWT (RS256 + Hybrid)
C 考 engineering judgment → Session (KISS/YAGNI)
```

**面試最常踩的雷**: 看到 "auth" 直接講 JWT 是流行病。Senior 訊號 = 看 problem，不看 buzzword。

---

## Chunk 6 (partial): OAuth 2.0 — 信任委託，不是登入按鈕

### 核心本質

OAuth 不是 "Sign in with Google" 按鈕。那只是副作用之一。OAuth 真正要解的是 **delegated authorization** — 讓 user 把「有限的、可撤銷的權限」委託給第三方 app，**完全不用把密碼交出去**。

關鍵三個字: **delegated** (委託)、**limited** (有限)、**revocable** (可撤銷)。

---

### 為什麼需要 OAuth — 兩個天真方案的 disaster

#### 方案 1: 把 Google 密碼給 ScaleUp → 三個具體 disaster

| 問題 | 物理現實 | 後果 |
|---|---|---|
| **No Scope Control** | 密碼 = 全權帳號。ScaleUp 拿到後可以讀 Gmail、刪 Drive、改 password | 「我只要寫 Drive」變成「整個 Google 帳號交給你」 |
| **No Revocation** | 撤銷 ScaleUp 權限只能改 Google 密碼，但這樣**所有裝置都被登出** | 撤銷代價爆炸大 |
| **Transitive Trust** | ScaleUp DB 被 hack → 攻擊者拿到 Google 密碼 → 攻擊者擁有整個 Google 生態 | ScaleUp 的洞 = Google 的洞 = 整個人生的洞 |

#### 方案 2: 手動 export → upload → 不能 automate、產品死

---

### OAuth 的四個角色 (一定要能背)

```
┌─────────────────┐         ┌─────────────────┐
│  Resource Owner │         │      Client     │
│    = the user   │         │   = ScaleUp app │
└────────┬────────┘         └────────┬────────┘
         │  consent / login           │  redirect 流程
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  Authorization  │ ───→    │ Resource Server │
│     Server      │  token  │ = Drive API     │
│  = Google login │         │                 │
└─────────────────┘         └─────────────────┘
```

| 角色 | 中文 | 在故事裡是 |
|---|---|---|
| **Resource Owner** | 資源擁有者 | User (擁有 Google Drive 的人) |
| **Client** | 第三方應用 | ScaleUp (想代理 user 寫 Drive 的 app) |
| **Authorization Server** | 授權伺服器 | Google login + 同意畫面 |
| **Resource Server** | 資源伺服器 | Google Drive API (實際存資料) |

**關鍵物理特性**: User 的密碼從頭到尾**只在 user 跟 Google 之間**流動，**ScaleUp 永遠看不到**。

---

### ⚠️ 待釐清（下次 session 補）

- [ ] **Q2 沒答出 WHY**: 為什麼 Auth Server 跟 Resource Server 要分開？
  - 預期答案: **blast radius separation** — auth server 被 hack 可以發任何人的 token；資料 server 被 hack 只是資料外洩。Security posture 不同 → 邏輯切開即使在同一公司內
- [ ] **Q3 跳過**: 三個 disaster 對應 OAuth 怎麼解
  - No Scope Control → token 帶 scope (e.g., `drive.file` 只能寫自己 app 建的 file)
  - No Revocation → token 跟密碼**獨立**，撤 token 不影響 password
  - Transitive Trust → token 有 TTL (e.g., 1 hour)，被偷的 blast radius 限定
- [ ] **Authorization Code Flow 全流程**: 為什麼中間要繞一圈 code 不直接給 token？
  - 預期答案: browser/URL 是 untrusted channel；code 沒 client_secret 換不了 token

---

## 🔴 My Mistakes & Misconceptions (Session 20)

| What I Thought / Got Stuck On | Reality | Why |
|---|---|---|
| Scenario A 答 Session 對，但 trade-off 說「more mantion more infra」沒講清楚是 HA / failover / monitoring / backup | 面試版：「we have to operate the session store, including HA, failover, monitoring, and backups」 | 抽象詞 (infra) 要拆成具體可被檢驗的營運項目 |
| Scenario B 直接跳到答案 (Hybrid) + 列 trade-off，沒講為什麼 base 是 JWT 不是 Session | 必須先論證「為什麼選 JWT 為 base」(centralized state 的痛) 再論 RS256，再論 Hybrid 加 refresh 補 revocation | WR2 老問題重現：**WHAT 知道，WHY 跳過**。Trade-off 列得再精，沒 WHY 就像「我選 Redis 因為它有 cluster mode」 |
| Q2 OAuth「為什麼 Auth Server 跟 Resource Server 要分開」答「不同 api」 | WHY 是 **blast radius separation**：Auth Server 被 hack = 可發任何人的 token；Resource Server 被 hack = 只是資料外洩。Security posture 不同 → 邏輯切開即使在同一公司內 | 描述「現象」≠ 解釋「為什麼設計成這樣」 |
| Q3 三個 disaster 對應 OAuth 解法 — 跳過沒答 | A. No Scope → token 帶 scope；B. No Revocation → token 獨立於密碼；C. Transitive Trust → token 有 TTL，blast radius 限定 | 還沒建立「設計每個元件對應一個痛點」的對照感 |

---

## 🎤 How to Say It in Interview

### JWT vs Session 三情境

**Bank monolith:**
> "Session, because the regulator requires forced logout within one second. Only a stateful store like Redis lets us delete the session record instantly. The trade-off is per-request Redis lookup latency (~1ms) and the operational cost of running the store: HA, failover, monitoring, and backups."

**Microservices:**
> "Hybrid: short-TTL JWT access tokens signed with RS256, plus stateful refresh tokens in the auth service's database. Session would centralize state in Redis, creating coupling, a single point of failure, and per-request latency multiplied across service hops. JWT eliminates the shared store: each service verifies the signature locally with the public key. RS256 specifically — because with HS256, every service holds the same secret to verify, so any compromised service can forge tokens for any user. RS256 splits the keys: only the auth service holds the private key. Trade-offs are key management via JWKS, clock skew, algorithm confusion attacks, and claim staleness."

**Side-project blog:**
> "Session, because none of JWT's selling points apply at this scale: no shared store to bypass, no other services to verify across, no scale concern. JWT would only add cost — secret management, TTL tuning, debugging base64 tokens, clock-skew handling, and rolling my own revocation logic — all paid by a solo developer. KISS and YAGNI: a sessions table in Postgres plus an HttpOnly cookie is fifty lines of Go. If the project ever needs horizontal scaling, migrating to JWT later is straightforward."

### OAuth 2.0 essence

> "OAuth 2.0 is delegated authorization. The user delegates a limited, revocable permission to a third-party app, without ever sharing the password. Four actors: Resource Owner (the user), Client (the app), Authorization Server (issues tokens), Resource Server (serves the data). The user's password only flows between the user and the Authorization Server — the Client never sees it."

---

## 🗣️ English Practice — Session 20

| My Answer | English Polish |
|-----------|----------------|
| A i'd choice Session because the bank need in 1sec block the user so use session is google but the trade off is every request need to serssion store check and need more mantion more infra (redis) | I'd choose **Session** for the bank scenario. The regulator requires forced logout within 1 second, and only a stateful store like Redis lets us delete the session record instantly. The trade-off is two-fold: every request now incurs a Redis lookup (adding ~1ms of latency), and we have to operate the session store itself, including HA, failover, monitoring, and backups. |
| Hybrid (短效 JWT access + stateful refresh token) Trade-off: Key management、clock skew、algorithm confusion、claim staleness | I'd choose **Hybrid**: short-TTL JWT access tokens for stateless per-request verification, plus stateful refresh tokens for revocation. The trade-offs are key management (distributing the verification key to all services), clock skew (each service validates `exp` against its own clock), algorithm confusion attacks, and **claim staleness** (a JWT carries a snapshot of the user's permissions that may be outdated by the time it's verified). |
| 因為 Session 會大量去打 session store 例如 redis 造成強耦合, 以及大量的 redis 壓力 | In microservices, Session forces every service to query a shared store like Redis. That centralizes state across the platform, causing tight coupling, a single point of failure, and per-request latency that multiplies across service hops. |
| RS256 的非對稱的 不會因為有 10 個 service 其中一個泄露 全部被攻擊 | With RS256, only the auth service holds the private signing key, while every other service holds the verify-only public key. Even if one of the ten services is compromised, attackers can only verify, not forge, so the blast radius doesn't fan out. |
| KISS 不要搞自己 都在同一臺 user 也不多 | I'd choose Session — KISS and YAGNI. With one server and only ~100 users a day, none of JWT's selling points apply, so adding JWT would be over-engineering. |
| Secret 管理, debug, 同步 | The unnecessary costs JWT brings here include secret management, harder debugging because tokens are opaque base64 strings, clock-skew handling, and having to roll my own revocation logic. |
| 第三方授權 | OAuth 2.0 is delegated authorization — letting a user grant a limited, revocable permission to a third-party app, without sharing the password. |
| 不同 api | The Authorization Server and Resource Server are split for **blast-radius separation**: the auth server's compromise lets attackers issue tokens for anyone, while the resource server's compromise only leaks the data it holds. Different security postures justify keeping them logically separate, even within the same company. |

---

## 📌 Key Vocab (Session 20 新增)

| 中文 | English | 例句 |
|------|---------|------|
| 委託授權 | delegated authorization | "OAuth is fundamentally about delegated authorization." |
| 信任傳染 | transitive trust | "Sharing your password creates transitive trust." |
| 有限的 | scoped / limited | "OAuth grants scoped access tokens, not full credentials." |
| 過時的宣告 | claim staleness | "Short TTLs mitigate claim staleness." |
| 演算法混淆攻擊 | algorithm confusion attack | "RS256-to-HS256 is a known algorithm confusion attack." |
| 故障範圍隔離 | blast radius separation | "Splitting auth and resource servers gives blast-radius separation." |
| 過度工程 | over-engineering | "JWT here would be over-engineering." |

---

## 🎯 Next Session Plan (繼續 Day 14)

- [ ] **Chunk 6 finish**: 答 Q2 + Q3 (blast radius separation / OAuth 解三個 disaster) + Authorization Code Flow 全流程 + 為什麼要繞一圈 code
- [ ] **Chunk 7**: Observability Mini for Security（auth failure rate、token issuance rate、suspicious IP patterns）
- [ ] **Chunk 8**: Scale Trigger + DevOps Angle（Cognito/OIDC、secrets rotation、key management）
- [ ] **Step D Hands-On**: PoC — implement JWT issue + verify in Go (Light Code tier)
- [ ] **Step E**: Simon Drill (covered chunks)
- [ ] **Step F**: Interview Drill — design the auth system for ScaleUp
- [ ] **Step G**: Finalize this notes file (mark 🟢 Complete)
- [ ] **Step H**: Update progress.md, scorecard, one-liners

**Resume cue**: "Last time you nailed JWT vs Session 三情境 (Chunk 5 ✅) and got the four OAuth actors. We stopped before Q2/Q3 of the OAuth Feynman check. Let's pick up there."
