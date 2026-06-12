# Back-of-Envelope Estimation Cheatsheet

Use these numbers for quick calculations during SD interviews. Don't memorize blindly — understand the order of magnitude.

## Latency Numbers

| Operation | Time | Notes |
|-----------|------|-------|
| L1 cache reference | 0.5 ns | |
| L2 cache reference | 7 ns | |
| Main memory reference | 100 ns | |
| SSD random read | 150 μs | |
| HDD random read | 10 ms | ~100x slower than SSD |
| Network round trip (same datacenter) | 500 μs | |
| Network round trip (cross-continent) | 150 ms | |
| Read 1 MB from memory | 250 μs | |
| Read 1 MB from SSD | 1 ms | |
| Read 1 MB from HDD | 20 ms | |
| Read 1 MB from network | 10 ms | |

**Key insight**: Memory is ~1000x faster than disk. Network within a datacenter is fast; cross-region is slow.

## Powers of 2

| Power | Exact | Approx | Common Usage |
|-------|-------|--------|-------------|
| 2^10 | 1,024 | ~1 Thousand | 1 KB |
| 2^20 | 1,048,576 | ~1 Million | 1 MB |
| 2^30 | 1,073,741,824 | ~1 Billion | 1 GB |
| 2^40 | | ~1 Trillion | 1 TB |

## Quick Conversion

| Unit | Size |
|------|------|
| 1 char (ASCII) | 1 byte |
| 1 char (UTF-8, English) | 1 byte |
| 1 char (UTF-8, CJK) | 3 bytes |
| UUID | 16 bytes (128 bits) |
| IPv4 address | 4 bytes |
| Unix timestamp | 4 bytes (until 2038) / 8 bytes |
| Average tweet | ~300 bytes |
| Average URL | ~100 bytes |
| Average email | ~50 KB |
| Average image (compressed) | ~300 KB |
| Average HD video (1 min) | ~50 MB |

## Scale Rules of Thumb

| Metric | Value | Notes |
|--------|-------|-------|
| QPS a single web server handles | 1K-10K | Depends on complexity |
| QPS a single Redis instance handles | 100K+ | In-memory, single-threaded |
| QPS a single MySQL handles | 1K-5K | With proper indexing |
| Connections a single server holds | 10K-100K | C10K problem |
| 1 day in seconds | 86,400 | ~100K |
| 1 month in seconds | 2,592,000 | ~2.5M |
| 1 year in seconds | 31,536,000 | ~30M |

## Common Estimation Patterns

### Storage Estimation
```
Daily new data = DAU × actions_per_user × data_per_action
Monthly = Daily × 30
Yearly = Daily × 365
5-year = Yearly × 5 (common interview horizon)
```

### QPS Estimation
```
Average QPS = DAU × actions_per_user / 86,400
Peak QPS = Average QPS × 2~5 (typical peak factor)
```

### Bandwidth Estimation
```
Bandwidth = QPS × average_request_size
```

## Example: Estimate Twitter Scale

- 300M monthly active users, 50% daily → 150M DAU
- Each user: 2 tweets/day, 5 reads/day
- Write QPS: 150M × 2 / 86,400 ≈ 3,500 QPS
- Read QPS: 150M × 5 / 86,400 ≈ 8,700 QPS
- Peak read QPS: 8,700 × 3 ≈ 26,000 QPS
- Tweet size: 280 chars × 1 byte + metadata ≈ 500 bytes
- Daily storage: 150M × 2 × 500 bytes ≈ 150 GB/day
- Yearly storage: 150 GB × 365 ≈ 55 TB/year
