# Hand-Write Map (S33 / WR4) — simple English for notebook

> Copy these by hand. Simple English on purpose: practice writing + memory.

---

## 1. URL Shortener — Architecture

```
URL SHORTENER   (a very read-heavy key-value system)

WRITE  (create a short link)
  User: "shorten this long URL"
    |
    v
  App Server  -->  KGS / Counter   (gives one unique number)
    |
    v
  base62 encode  -->  "e7K3mQ"   (7 chars, never collides)
    |
    v
  NoSQL KV DB:  store  e7K3mQ = longURL   (source of truth, durable)
    |
    v
  return the short link

READ  (open a short link)
  User: GET /e7K3mQ
    |
    v
  App Server  -->  Cache?
                    | hit  -> return longURL   (fast)
                    | miss -> NoSQL KV DB -> longURL -> fill cache
    |
    v
  301 redirect to longURL
  (cache needs NO invalidation: the mapping never changes)

ANALYTICS  (count clicks)
  click  -->  Message Queue  -->  Worker  -->  Analytics DB
             (async, do not slow down the redirect)
```

Key idea: codes are **encoded from a unique counter**, NOT hashed, so they cannot collide.

---

## 2. Encode vs Hash vs Encrypt  (today's biggest idea)

```
They look similar but do 3 totally different jobs:

  ENCODING          |  HASHING          |  ENCRYPTION
  base62 / base64   |  MD5 / SHA        |  AES / RSA
  change the format |  make fingerprint |  keep it secret
  NO key            |  NO key           |  needs a KEY
  anyone reverses   |  nobody reverses  |  only key holder reverses
  no collision      |  can collide      |  -
  "shorten /        |  "compare,        |  "lock it, need
   transport"       |   not recover"    |   the key to open"

  Store a password = HASHING  (salted + slow, e.g. bcrypt / argon2)
  Why: you only need to VERIFY it, never RECOVER it.
       one-way storage protects users if the DB leaks.
```

Note: base64 was never "cracked". It is reversible **by design** (like Morse code), because it was never meant to hide anything.

---

## 3. Caching — Quick Map

```
WHEN:       read-heavy + hot keys
TRADE-OFF:  + fast, + less DB load
            - expensive, small, volatile (lost on crash)
SIZE:       80/20 rule -> cache the hot 20% only
            ~  items x size   (1TB data -> open ~256GB)
INVALIDATE: on write, DELETE the cache entry (do not update)
            -> avoids a race condition

FAILURE MODES (3):
  stampede     : hot key expires  -> floods DB  -> single-flight lock
  penetration  : ask a missing key-> floods DB  -> Bloom filter
  avalanche    : many keys expire -> floods DB  -> random TTL

TODAY'S CHAIN (connect the dots):
  penetration -> Bloom filter -> works BECAUSE no false negative
              -> "definitely not in" is 100% safe to reject
```
