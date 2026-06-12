# SD Coach Response — Day 8: Database Selection (SQL vs NoSQL Concepts)

---

## Step A: Review (5 min)

Welcome back! You just wrapped up Day 6-7 on Caching & CDN. Before we move forward, let's make sure that knowledge is solid.

**What did we cover last time? What was the most important takeaway from caching and CDN?**

Go ahead — explain it in your own words.

---

*(Assuming the student gives a reasonable recap about cache layers, eviction policies, CDN edge caching, etc.)*

Good. I checked your progress and there are no unresolved mistakes from last session, so we're clear to move on.

One quick check: your session count is at 7, and your last weekly review hasn't happened yet. We're not at the 7-session threshold for a weekly review, so we'll proceed with new content today.

Let's get into databases.

---

## Step B: Introduction (3 min) — The Analogy

Imagine you're organizing a massive library.

**Option A: The Traditional Library (SQL).** Every book is catalogued with a strict system — author, title, ISBN, genre, shelf location. If you want to find a book, you look it up in the card catalog and follow a precise path. Adding a new book means filling out every field in the catalog. The system is rigid, but when you need to find something or cross-reference (e.g., "all books by Author X published after 2020"), it's incredibly powerful. The downside? If the library grows to 10 million books, that one giant card catalog becomes a bottleneck.

**Option B: The Bookstore Warehouse (NoSQL).** Books are just tossed into labeled bins — "Science Fiction," "Cookbooks," "2024 Arrivals." Each bin can have a different internal structure. You can throw in a magazine, a DVD, or a book — the bin doesn't care. Finding a specific item in a bin is fast if you know the bin. But cross-referencing across bins? That's on you, not the system.

Neither approach is "better." The right choice depends on **what questions you'll ask the data** and **how fast it needs to grow**.

That's what today is about: building a decision framework so you can confidently pick the right database in an interview — and explain WHY.

---

## Step C: Core Teaching (Feynman + Simon)

### Chunk Map

Here are today's core chunks. We'll work through them one at a time, and you need to pass a check on each before we move to the next.

```
☐ 1. SQL vs NoSQL vs NewSQL — What they are and when to use each
☐ 2. The Decision Framework — How to pick the right DB in an interview
☐ 3. Indexing: B-tree vs LSM-tree
☐ 4. Denormalization — Why break the rules?
☐ 5. Sharding intro — Horizontal partitioning
☐ 6. Connection Pooling — Why it matters at scale
☐ 7. Observability Mini — SLIs, SLOs, Alerts, Dashboards for databases
```

Let's start.

---

### Chunk 1: SQL vs NoSQL vs NewSQL — What They Are

**SQL (Relational Databases):** Think PostgreSQL, MySQL, Oracle.
- Data lives in **tables with rows and columns**
- Strict schema — every row has the same structure
- Supports **ACID transactions** (Atomicity, Consistency, Isolation, Durability)
- Powerful **JOINs** for querying across related tables
- Vertical scaling is the natural path (bigger machine)

**NoSQL (Non-Relational Databases):** Think DynamoDB, MongoDB, Cassandra, Redis.
- Data can be stored as **documents, key-value pairs, wide-columns, or graphs**
- Flexible schema — each record can have different fields
- Typically trades strict consistency for **availability and horizontal scalability**
- No JOINs (or very limited) — you design your data model around your **access patterns**

**NewSQL:** Think CockroachDB, Google Spanner, TiDB.
- SQL interface + ACID transactions, but with **horizontal scaling built in**
- Tries to give you the best of both worlds
- Trade-off: complexity, operational cost, and often higher latency than purpose-built NoSQL

Here's the comparison at a glance:

| Feature | SQL | NoSQL | NewSQL |
|---|---|---|---|
| **Schema** | Fixed (tables) | Flexible (document/KV/etc.) | Fixed (tables) |
| **Transactions** | Full ACID | Limited (per-partition or none) | Full ACID |
| **Scaling** | Vertical (primary) | Horizontal (native) | Horizontal (native) |
| **JOINs** | Native, powerful | Expensive or unavailable | Native |
| **Best for** | Complex queries, relationships, financial data | High throughput, flexible data, massive scale | Need SQL + scale (but accept complexity) |
| **Examples** | PostgreSQL, MySQL | DynamoDB, MongoDB, Cassandra, Redis | CockroachDB, Spanner |

**The key insight:** This is NOT about "SQL is old, NoSQL is new." It's about **matching the tool to the access pattern.** An e-commerce product catalog with flexible attributes? Maybe a document store. A banking ledger that needs cross-account transactions? SQL all the way. A chat app storing billions of messages? Wide-column NoSQL.

---

#### Feynman Gate — Chunk 1

**Stage 1 (Recall):**

In your own words, explain the core difference between SQL and NoSQL databases. Don't just list features — tell me *why* someone would pick one over the other.

---

*(Waiting for student response)*

---

**Stage 2 (Transfer):**

Here's a scenario: You're designing a system for an online marketplace. Users create product listings, and each product category has *completely different attributes* — a laptop has CPU, RAM, screen size; a shirt has size, color, material; a car has mileage, engine type, year.

You need to support:
- Searching products by attribute
- Displaying product details
- Processing purchase transactions (payment must be atomic)

Would you use SQL, NoSQL, or a combination? **Walk me through your reasoning.**

---

*(Waiting for student response)*

---

*(Assuming student passes both stages — mark chunk 1 complete)*

```
✅ 1. SQL vs NoSQL vs NewSQL — What they are and when to use each
☐ 2. The Decision Framework — How to pick the right DB in an interview
☐ 3. Indexing: B-tree vs LSM-tree
☐ 4. Denormalization — Why break the rules?
☐ 5. Sharding intro — Horizontal partitioning
☐ 6. Connection Pooling — Why it matters at scale
☐ 7. Observability Mini — SLIs, SLOs, Alerts, Dashboards for databases
```

---

### Chunk 2: The Decision Framework — How to Pick the Right DB in an Interview

In an interview, you will NOT say "I'll use PostgreSQL" and move on. You need to show your **reasoning process.** Here's the framework:

**Step 1 — Identify the access patterns:**
- Is it read-heavy or write-heavy?
- What's the read:write ratio? (e.g., 100:1 for a blog, 1:1 for a chat app)
- Are reads simple lookups (by key) or complex queries (JOINs, aggregations)?

**Step 2 — Identify the data characteristics:**
- Is the schema well-defined and stable, or does it evolve frequently?
- How are entities related? (heavy relationships = SQL shines)
- What's the data volume? (GB vs TB vs PB)

**Step 3 — Identify the consistency requirements:**
- Does this need strong consistency? (financial transactions, inventory counts)
- Can it tolerate eventual consistency? (social media feeds, analytics)
- Does it need transactions across multiple entities?

**Step 4 — Consider the operational reality:**
- What does your team know? (don't pick Cassandra if nobody has operated it)
- What does your cloud provider offer as managed services?
- What's the cost profile at your expected scale?

**The interview move:** In a real interview, say it out loud:

> "Let me think about the data access patterns first. We have [X reads/sec] and [Y writes/sec]. The data has [fixed/flexible] schema with [strong/weak] relationships. Given that, I'd lean toward [SQL/NoSQL] because [specific reason]. The trade-off is [what you give up]."

This demonstrates structured thinking — which is what interviewers are scoring.

Here's a quick decision tree you can keep in your head:

```
Need ACID transactions across entities?
  → YES → SQL (or NewSQL if you also need horizontal scale)
  → NO ↓

Schema is flexible / varies by record type?
  → YES → Document store (MongoDB, DynamoDB)
  → NO ↓

Read:write ratio heavily skewed to writes?
  → YES → Wide-column (Cassandra) or KV store
  → NO ↓

Need complex queries / JOINs / aggregations?
  → YES → SQL
  → NO → Key-value or Document store
```

**Warning:** This is a starting heuristic, not a law. Real-world systems often use **multiple databases** (polyglot persistence). A system might use PostgreSQL for user accounts + DynamoDB for session data + Redis for caching + Elasticsearch for search. That's normal and worth mentioning in interviews.

---

#### Feynman Gate — Chunk 2

**Stage 1 (Recall):**

Walk me through the decision framework. If someone hands you a new system to design, what are the 4 things you evaluate before picking a database? Explain each briefly.

---

*(Waiting for student response)*

---

**Stage 2 (Transfer):**

Here's the scenario: You're designing a **real-time leaderboard** for a mobile game with 5 million daily active users. The leaderboard shows the top 100 players globally, and each player can see their own rank. Scores update every few seconds during gameplay.

Using the decision framework, talk me through which database(s) you'd pick and WHY. I want to hear your reasoning process, not just the answer.

---

*(Waiting for student response)*

---

*(Assuming student passes both stages — mark chunk 2 complete)*

```
✅ 1. SQL vs NoSQL vs NewSQL — What they are and when to use each
✅ 2. The Decision Framework — How to pick the right DB in an interview
☐ 3. Indexing: B-tree vs LSM-tree
☐ 4. Denormalization — Why break the rules?
☐ 5. Sharding intro — Horizontal partitioning
☐ 6. Connection Pooling — Why it matters at scale
☐ 7. Observability Mini — SLIs, SLOs, Alerts, Dashboards for databases
```

---

### Chunk 3: Indexing — B-tree vs LSM-tree

This is the chunk that separates "I know SQL vs NoSQL" from "I actually understand WHY they perform differently." The secret is in how they organize data on disk.

**B-tree (used by PostgreSQL, MySQL InnoDB):**

Think of a B-tree like a phone book. The data is **sorted** and organized into a tree structure. When you search, you navigate from the root down to the leaf — like binary search but on disk pages.

- **Reads are fast:** O(log N) lookups. You walk down the tree.
- **Writes are slower:** Every write must find the right place in the sorted structure and update it *in place*. This means random I/O on disk.
- **Best for:** Read-heavy workloads. Traditional OLTP (e-commerce, banking).

```
          [50]
        /      \
     [20,30]   [70,80]
    /  |  \    /  |  \
  [10][25][35][60][75][90]   ← leaf nodes (actual data)
```

**LSM-tree (used by Cassandra, RocksDB, LevelDB, DynamoDB under the hood):**

Think of an LSM-tree like writing in a notebook. You just append new entries to the end — super fast. Periodically, you "compact" the notebook by merging and sorting pages in the background.

- **Writes are very fast:** Always sequential writes (append to an in-memory buffer called a "memtable," then flush to disk as sorted files called "SSTables").
- **Reads can be slower:** You might need to check multiple SSTables to find a value. Bloom filters help skip SSTables that definitely don't have your key.
- **Best for:** Write-heavy workloads. Logging, time-series, IoT data.

```
Write path:
  New data → Memtable (in-memory, sorted)
           → Full? Flush to SSTable on disk
           → Background compaction merges SSTables

Read path:
  Check Memtable → Check Bloom filter on each SSTable → Read from SSTable
```

Here's the comparison:

| | B-tree | LSM-tree |
|---|---|---|
| **Write speed** | Slower (random I/O, in-place update) | Faster (sequential I/O, append-only) |
| **Read speed** | Faster (single lookup path) | Slower (may check multiple SSTables) |
| **Write amplification** | Lower | Higher (compaction rewrites data) |
| **Space amplification** | Lower | Higher (multiple versions until compacted) |
| **Best for** | Read-heavy OLTP | Write-heavy workloads |
| **Used by** | PostgreSQL, MySQL | Cassandra, RocksDB, DynamoDB |

**The interview connection:** When an interviewer asks "Why Cassandra for this write-heavy system?" you can say:

> "Cassandra uses an LSM-tree storage engine, which means writes are sequential appends — much faster than B-tree's random I/O. That's ideal for our use case with [N] writes/sec. The trade-off is that reads may need to check multiple SSTables, but we can mitigate that with Bloom filters and proper compaction tuning."

That's a strong answer because it connects the database choice to the storage engine mechanics.

---

#### Feynman Gate — Chunk 3

**Stage 1 (Recall):**

Explain the difference between B-tree and LSM-tree indexing in your own words. Specifically: how does each handle writes, and why does that make one faster for writes than the other?

---

*(Waiting for student response)*

---

**Stage 2 (Transfer):**

You're building a system that ingests IoT sensor data — 500,000 writes per second from temperature sensors, and the primary read pattern is "give me the last 24 hours of data for sensor X." Reads happen maybe 1,000 times per second.

Based on what you just learned, which storage engine approach would you choose and WHY? What's the trade-off you're accepting?

---

*(Waiting for student response)*

---

*(Assuming student passes both stages — mark chunk 3 complete)*

```
✅ 1. SQL vs NoSQL vs NewSQL — What they are and when to use each
✅ 2. The Decision Framework — How to pick the right DB in an interview
✅ 3. Indexing: B-tree vs LSM-tree
☐ 4. Denormalization — Why break the rules?
☐ 5. Sharding intro — Horizontal partitioning
☐ 6. Connection Pooling — Why it matters at scale
☐ 7. Observability Mini — SLIs, SLOs, Alerts, Dashboards for databases
```

---

## What's Next

We've covered 3 of 7 chunks so far. The remaining chunks for today are:

- **Chunk 4:** Denormalization — when and why to break normal form
- **Chunk 5:** Sharding intro — horizontal partitioning strategies
- **Chunk 6:** Connection pooling — why it matters at scale
- **Chunk 7:** Observability Mini — SLIs, SLOs, Alerts, Dashboards for databases

We'll continue through each with the same Feynman Gate process, then move to Steps D through H (Hands-On, Simon Drill, Interview Drill, Notes, and Progress Update).

Ready to continue with Chunk 4?
