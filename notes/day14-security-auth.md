# Day 14 — Security & Authentication

> Status: 🟡 **In Progress** (Session 19, Chunks 1-4 done; Chunks 5-8 + Drill pending)
> Date: 2026-04-27 (Session 19 start)
> Phase 1

---

## One-liner

Security & Auth 不是「best practices 清單」，而是**每一層機制都對應一個具體的物理威脅** — HTTPS 防竊聽、bcrypt+salt 防 DB 外洩、JWT 防 DB 被打爆、Refresh token 防 stolen JWT 長期有效。

## 🔗 Derivation Insight

- **Physical constraint:** HTTP 明文傳輸（任何節點都看得到）+ DB 可能被 breach + 每 request 查 DB 太慢 + token 盜用風險
- **My derivation:** 公共 WiFi 登入銀行 → 密碼明文被竊聽 → 需要 HTTPS → 但 server 拿到密碼怎麼存？明文存 → DB breach 全洩 → 需要 hash → SHA-256 太快可被暴力破解 + 同密碼同 hash → 加 salt + 用 slow hash (bcrypt) → 每 request 都 verify 太慢且重複曝光 → 用 token (JWT)
- **Surprise:** 「對 password 而言 hash 越慢越好」是反直覺的 — 這就是 **asymmetric cost**：合法 user 100ms 不痛，攻擊者 1B candidates × 100ms = 3 年。**Slowness 本身就是 security feature**。

---

## 核心概念整理

### Chunk 1: HTTPS / TLS — 加密 the wire

**Physical threat:** HTTP 明文傳輸 → public WiFi 上任何人（包含 router owner）用 packet sniffer (Wireshark) 抓封包 → 看到密碼。這是經典的 **Man-in-the-Middle (MITM) attack**。

**Solution:** HTTPS = HTTP + TLS

| TLS 提供 | 防什麼 |
|----------|--------|
| **Encryption** | WiFi owner 抓到的是亂碼，不是密碼 |
| **Authentication** | Browser 驗 cert，確認真的在跟 bank.com 講話（防假網站）|
| **Integrity** | 偵測中途有人竄改流量 |

**為什麼 Chrome 把 HTTP 標 "Not Secure"：** 這不是潔癖，是物理威脅。Public WiFi MITM 太容易了，攻擊者甚至能架 fake hotspot 「Starbucks_FREE」騙人連。

---

### Chunk 2: Password Storage — bcrypt + salt

**Physical threat:** DB 被 breach 一次，所有 user 的密碼都洩漏。

**Step 1 — 為什麼 hash：**

| 機制 | 是否可逆？ | 用途 |
|------|------------|------|
| **Encryption** (TLS) | ✅ Yes (with key) | Data in transit — 兩端都要讀得到 |
| **Hashing** (bcrypt) | ❌ No — one way | 密碼 — server 只需 verify，永遠不需 recover |

**Step 2 — 但只用 SHA-256 還不夠，兩個問題：**

#### Problem 1: Same password = Same hash → Rainbow table 攻擊

```
sha256("password123") = "ef92b778..."  // Alice 和 Bob 都用 password123
                                       // → 同 hash → 攻擊者用公開 rainbow table 直接查
```

**Solution: Salt**（每個 user 一組隨機字串）

```
sha256("password123" + "alice_random_8VxR") = "9c4a7..."
sha256("password123" + "bob_random_p2KnQ")  = "f1d33..."
                                              ↑ 完全不同
```

#### Problem 2: SHA-256 太快 → 暴力破解快

```
GPU 跑 SHA-256: ~10 BILLION hashes/sec
→ 攻擊者拿到 hashed DB，每秒試 100 億組密碼 → 弱密碼幾秒就破
```

**Solution: 用慢的 hash function**

| Hash | 速度 | 用途 |
|------|------|------|
| SHA-256 / MD5 | 微秒級 | ❌ 不適合密碼 |
| **bcrypt / scrypt / Argon2** | ~100ms（可調 cost factor）| ✅ 密碼 |

**核心 insight: Asymmetric Cost**
- 合法 user login：100ms 完全感覺不到
- 攻擊者 brute force：100ms × 10 億 candidates = **3 年**（不是 1 秒）
- bcrypt 的 cost factor 可調：硬體變快了就把 12 → 13（work doubles）→ 永遠維持 100ms

**最終流程：**
```
user_input → HTTPS → bcrypt(password + salt, cost=12) → 存 hash + salt 到 DB
```

---

### Chunk 3: JWT Mechanics — 自包含的身份證明

**Physical threat:** 每 API request 都重新 verify password
1. **Performance**: bcrypt 100ms × 100 req/min → server CPU 爆掉
2. **Security**: 密碼曝光 100 次 → 任一 request 被 log/leak → 全完

**Solution:** 登入用密碼（昂貴但少），後續用 token（便宜且可驗證）

**JWT 結構：3 段用 `.` 串接**

```
HEADER  .  PAYLOAD  .  SIGNATURE
  ↓         ↓           ↓
metadata  claims      proof
```

```json
// HEADER
{ "alg": "HS256", "typ": "JWT" }

// PAYLOAD (claims)
{
  "sub": "user_42",     // who (subject) — 取代 DB lookup
  "exp": 1714280000,    // when expires (Unix timestamp)
  "iat": 1714276400,    // issued at
  "role": "customer"
}

// SIGNATURE
HMACSHA256( base64(HEADER) + "." + base64(PAYLOAD), SERVER_SECRET )
```

**為什麼 server 可以信任 JWT 而不查 DB：**

```
產生有效 signature 需要 server secret
        ↓
只有 real server 有那把 secret
        ↓
所以 signature 驗過 = 這個 JWT 是 real server 發出的 → trust the claims
```

**這就是 stateless auth** — server 不存 session，純靠數學驗證。

#### HS256 vs RS256（面試加分點）

| 算法 | Key 機制 | 適用 |
|------|----------|------|
| **HS256** (HMAC) | Shared secret — 簽和驗用同一把 | Single-service simplicity |
| **RS256** (RSA) | Private key 簽 + Public key 驗 | Cross-service（其他 service 拿 public key 驗就好，不能拿來簽）|

#### Mini Code (Go)

```go
// JWT verify — 微秒級，no DB lookup
func verifyJWT(tokenString string, secret []byte) (string, error) {
    token, err := jwt.Parse(tokenString, func(t *jwt.Token) (any, error) {
        return secret, nil
    })
    if err != nil || !token.Valid {
        return "", errors.New("invalid token")
    }
    claims := token.Claims.(jwt.MapClaims)
    if float64(time.Now().Unix()) > claims["exp"].(float64) {
        return "", errors.New("token expired")
    }
    return claims["sub"].(string), nil
}
```

---

### Chunk 4: JWT 的詛咒 — Refresh Token 模式

**JWT 的 superpower：stateless，不查 DB。**
**JWT 的 curse：因為 stateless，server 無法主動撤銷 token。**

#### 情境

```
Day 1: Alice login → JWT exp = 7 days
Day 3: Alice 筆電被偷
Day 3: Alice 打客服「立刻登出我！」
        → Server: "我什麼都沒存…stolen JWT 還能用 4 天" 🔥
```

#### 業界解法：Access Token + Refresh Token

| | **Access Token (JWT)** | **Refresh Token (opaque)** |
|---|---|---|
| TTL | 5-15 分鐘 | 7-30 天 |
| 狀態 | Stateless（純驗 sig）| **Stateful**（存 DB）|
| 用途 | 每次 API call | 換新 access token |
| 被偷的 blast radius | 限定 15 分鐘 | 可立刻撤銷 |

#### Flow

```
1. Login         → server 發 { access (15m), refresh (30d) }
2. 每次 API call → 帶 access token（快、no DB）
3. Access 過期   → client 用 refresh token 換新 access
                   （這時才 hit DB — 但只每 15 分鐘一次）
4. Logout        → server 從 DB 刪 refresh token
                   → 下次 refresh 失敗 → user 真的出去了
5. 筆電被偷      → admin 刪 refresh token → 最多 15 分鐘曝光
```

#### 為什麼 15 分鐘？

不是隨便挑的數字 — 這是 **acceptable blast radius**。
- **金融類**（銀行、payment）：5 分鐘
- **一般消費 App**：15-60 分鐘

**面試話術：** 被問「access token TTL 多久？」直接答：
> "15 minutes — it balances UX (don't refresh too often) with security (limit damage from theft)."

---

## 🔴 My Mistakes & Misconceptions

| What I Thought / Got Stuck On | Reality | Why |
|---|---|---|
| 急著答「JWT 簽章」沒先講清楚 problem | 應該先用 2 個原因（performance / security exposure）說明為什麼不能每 request 重驗密碼，再導出 token 的需要 | WR2 找出的老問題：**WHAT 知道，WHY 講不出**。直接講答案 ≠ 理解 |
| 解釋 JWT 信任機制只說「server verifies signature」 | 真正的 WHY 是 3 步邏輯：(1) 產生 sig 需要 secret (2) 只有 server 有 secret (3) 因此 sig 驗過 = real server 發的 | 描述 HOW（流程）≠ 解釋 WHY（信任的根據）|
| 想不起來 "encryption" 英文 | encryption（n.）/ encrypted（adj.）/ eavesdropping（n.竊聽）| 純英文詞彙缺口 — interview 直接卡 |
| Brute-force 速度問題完全不知道 | SHA-256 在 GPU 上每秒 ~100 億次 → 弱密碼秒破 → 所以 password hash 要刻意慢（bcrypt）| 沒接觸過 password security 的數量級 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "Authentication has multiple layers, each addressing a specific threat. HTTPS protects the wire from MITM. bcrypt with salt protects passwords from DB breaches. JWT lets us verify identity without hitting the DB on every request. Refresh tokens fix JWT's revocation gap."

**When asked "How do you store passwords?":**
> "Hash with bcrypt and a per-user salt, with a cost factor around 12 — that gives ~100ms per verify. The slowness is a feature: invisible to legitimate users, but exponentially expensive for brute-force attackers. The salt ensures identical passwords produce different hashes, defeating rainbow tables."

**When asked "Why JWT?":**
> "JWT is stateless — the server verifies the signature with a secret only it knows, so the claims inside (user_id, expiration) can be trusted without a DB lookup. This scales well in microservices because each service can verify independently."

**When asked "What are JWT's downsides?":**
> "Hard to revoke. Once issued, it's valid until expiration. The fix is short-lived access tokens (~15 min) paired with long-lived refresh tokens stored server-side — refresh tokens are revocable, so we cap the damage from a stolen access token to 15 minutes."

**When asked "HS256 or RS256?":**
> "HS256 for single-service simplicity — same secret signs and verifies. RS256 for multi-service architectures — private key signs, public key verifies, so other services can verify independently without sharing the signing key."

**Asymmetric cost — for bonus points:**
> "Most security mechanisms apply asymmetric cost — they're cheap for legitimate users but expensive for attackers. bcrypt cost factor, rate limiting, CAPTCHA, TLS handshake — same philosophy."

---

## 🗣️ English Practice — Session 19

| My Answer | English Polish |
|-----------|----------------|
| 1. anyone 2. wifi owner because http is no encry(加密) 3. 被竊取 | On public WiFi, anyone on the same network — including the router owner — can sniff packets. Since HTTP is unencrypted plain text, they can see my username and password directly, and steal my credentials. |
| https or tls? | We solve the eavesdropping problem with HTTPS, which is HTTP layered over TLS. TLS encrypts the channel, so even if someone sniffs the WiFi, they only see encrypted bytes. |
| user enter password > https > hash store in DB | The user enters the password, sends it over HTTPS, and the server hashes it before storing. Even if attackers dump the DB, they can't recover the original password. |
| 加 user 的專屬識別碼 打亂 hash 過的值 | We add a unique random salt to each user's password before hashing, so identical passwords produce different hashes. |
| 不知道（brute force speed problem） | I'm not sure — could you walk me through it? |
| 對 password 而言 hash 越慢越好 防止被快速測試破解, bcrypt 速度慢一點對 user 體感差異不大但是對暴力破解就是指數的時間, salt 就算 user 設置一樣的密碼 hash 結果也不一樣 | For password hashing, slower is better. SHA-256 is too fast — bcrypt is intentionally ~100ms, which is invisible to users but exponentially expensive for brute-force attackers. Salt ensures identical passwords produce different hashes, so cracking one user doesn't crack everyone. |
| server 壓力爆炸, 密碼外洩, 應該只有登入使用帳密, request 帶入不同的驗證方式 | Two problems: server load explodes from running bcrypt on every request, and the password gets re-exposed in every API call. So we should only use the password at login, and switch to a different credential — like a token — for subsequent requests. |
| 1. server secret / private key 2. only the real server 3. the real server | To produce a valid signature, you need the server secret. Only the real server has that secret. So if the signature verifies, the JWT must have been issued by the real server — therefore the claims can be trusted without a DB lookup. |
| JWT 是 stateless token 所以 server 不保存 session, 只要 token 沒有過期是合法的 就可以使用 | JWT is stateless — the server doesn't store session state. As long as the token is unexpired and the signature is valid, the server accepts it. There's no central record to delete, so revocation is hard. |
| A leaked access token is still dangerous, but a short TTL limits the attacker window | A leaked access token is still dangerous, but a short TTL limits the attacker's window. After 15 minutes, they'd need a refresh token to get a new access token — and if we've revoked the refresh token, the attacker is locked out. |

---

## 📌 Key Vocab (English Practice — 易卡的詞)

| 中文 | English | 例句 |
|------|---------|------|
| 加密 | encryption / encrypt | "TLS encrypts the channel." |
| 解密 | decryption / decrypt | "Only the holder of the private key can decrypt." |
| 雜湊 | hashing / hash | "Hash the password with bcrypt." |
| 鹽值 | salt | "A unique salt per user." |
| 簽章 | signature / sign | "The server signs the JWT with HS256." |
| 驗證 | verify / verification | "Verify the signature using the secret." |
| 撤銷 | revoke / revocation | "Hard to revoke a JWT." |
| 暴力破解 | brute force | "bcrypt's slowness defeats brute force." |
| 竊聽 | eavesdrop / sniff | "An attacker can sniff packets on public WiFi." |
| 中間人攻擊 | Man-in-the-Middle (MITM) | "MITM is easy on public WiFi." |
| 不可逆 | one-way / irreversible | "Hashing is one-way." |
| 不對稱成本 | asymmetric cost | "Security relies on asymmetric cost." |

---

## 🎯 Next Session Plan (繼續 Day 14)

- [ ] **Chunk 5**: JWT vs Session — 3-scenario quiz (banking / microservices / single-server VM)
- [ ] **Chunk 6**: OAuth 2.0 flow basics（信任委託，不是 login button）
- [ ] **Chunk 7**: Observability Mini for Security（auth failure rate、token issuance rate、suspicious IP patterns）
- [ ] **Chunk 8**: Scale Trigger + DevOps Angle（Cognito/OIDC、secrets rotation、key management）
- [ ] **Step D Hands-On**: PoC — implement JWT issue + verify in Go (Light Code tier)
- [ ] **Step E**: Simon Drill (covered chunks)
- [ ] **Step F**: Interview Drill — design the auth system for ScaleUp
- [ ] **Step G**: Finalize this notes file (mark 🟢 Complete)
- [ ] **Step H**: Update progress.md, scorecard, one-liners

**Resume cue:** "Last time you nailed the JWT derivation. We stopped at the Session vs JWT scenario quiz — let's pick up there."
