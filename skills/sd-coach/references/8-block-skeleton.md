# 8-Block Skeleton — Standard Whiteboard Template

Use this template as the **starting point** for EVERY system design diagram.

```
Client → DNS → LB → API Server → Cache → Database
                                ↘ Queue → Worker
```

## Rules

1. **Every diagram starts with these 8 blocks** — add more for the problem, never remove any
2. **Consistent layout** — readable by the interviewer in 5 seconds
3. **Annotate each arrow** with protocol/data: `HTTP`, `gRPC`, `async`, `pub/sub`
4. **Highlight the "interesting" blocks** for this specific problem (bold/color/star)

## Common Extensions

| Problem Type | Add These Blocks |
|---|---|
| Real-time (chat, notifications) | WebSocket Server, Presence Service |
| Search/Autocomplete | Search Index (Elasticsearch), Trie Service |
| Media (YouTube, Instagram) | Object Storage (S3), CDN, Transcoding Worker |
| Location-based (Uber, Yelp) | Geospatial Index, Location Service |
| Payment/Financial | Payment Gateway, Reconciliation Service, Audit Log |
| Feed/Timeline | Fan-out Service, Timeline Cache |

## Example: URL Shortener

```
Client → DNS → LB → API Server → Cache (Redis) → Database (PostgreSQL)
                         |                              |
                         ↓                              ↓
                   URL Generator              Analytics Worker
                   (base62 + collision check)  (click tracking)
```

Highlighted blocks: **API Server** (URL generation logic) and **Database** (schema design for short→long mapping).
