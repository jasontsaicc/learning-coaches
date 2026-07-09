# Mind Map (S33 / WR4) — hand-write, simple English

> Copy onto paper. Few words, key points only. Practice writing English while you do.

---

## 1. URL Shortener

```
   URL SHORTENER  (read-heavy KV)
     |
     +- generate > counter -> base62 -> "e7K3mQ"  (no collision)
     +- store    > NoSQL KV  (source of truth, durable)
     +- serve    > cache hit = fast / miss -> DB  (no invalidation)
     +- scale    > 1 counter = SPOF -> ID range / Snowflake
     +- track    > click -> queue -> worker  (async)
```

## 2. Encode vs Hash vs Encrypt

```
   TRANSFORM DATA  (3 different jobs)
     |
     +- encoding   > base62/64 : change format, no key, anyone reverses
     +- hashing    > MD5/SHA   : fingerprint, no key, nobody reverses
     +- encryption > AES/RSA   : secret, needs KEY, only key opens
     |
     => store password = HASHING (salted + slow, bcrypt)
        why: only VERIFY, never RECOVER
```

## 3. Caching

```
   CACHING
     |
     +- when  > read-heavy + hot keys
     +- trade > +fast / -small, costly, volatile
     +- size  > 80/20 -> hot 20%  (1TB -> 256GB)
     +- write > DELETE cache, not update  (avoid race)
     +- fail  > stampede / penetration(Bloom) / avalanche(random TTL)
```

## Bonus: the chain to remember

```
   penetration -> Bloom filter -> works BECAUSE no false negative
               -> "definitely not in" is 100% safe to reject
```
