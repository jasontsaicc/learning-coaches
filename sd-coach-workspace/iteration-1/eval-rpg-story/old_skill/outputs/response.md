# SD Coach — Day 4: Load Balancer & Reverse Proxy (Part 1)

## Step A: Review (Phase 0 Recap)

Welcome back! You've passed the Phase 0 Gate — congrats on getting through the thinking framework. Before we move into Phase 1, let me check what stuck.

**Quick recall check:**

Last session (Day 3), we covered the 4-Step SD Interview Framework and practiced a dry run with "Design a URL Shortener."

Can you tell me: **What are the 4 steps of the SD interview framework, and roughly how much time would you spend on each in a 45-minute interview?**

*(Waiting for student response...)*

*Expected answer: Clarify Requirements (0-5 min) → High-Level Design (5-15 min) → Deep Dive (15-35 min) → Scale & Trade-offs (35-45 min). If the student can't recall, we'd review before proceeding.*

Great — you've got that framework locked in. From now on, we'll use it every single session during the Interview Drill. Today we enter **Phase 1: Core Building Blocks.** This is where we start learning the actual pieces you'll use to build any system.

---

## Step B: Introduction (Analogy)

Let me paint you a picture.

Imagine you own a wildly popular restaurant. On opening night, you have **one waiter** serving every table. The first 10 customers? Fine. But by table 30, orders are piling up, food is cold, and people are walking out.

So what do you do? You hire **more waiters**. But now you have a new problem — when a customer walks in the door, who decides which waiter takes them? You need a **host at the front door**.

That host is a **Load Balancer**.

The host looks at all the waiters, sees who's busy and who's free, and routes the next customer to the best available waiter. If a waiter calls in sick (server goes down), the host stops sending customers to them. If you hire a new waiter (add a server), the host starts including them automatically.

That's the core idea: **a Load Balancer sits between your users and your servers, distributing traffic so no single server gets overwhelmed.**

But before the customer even gets to the restaurant, they need to **find** the restaurant. They Google the address, and their phone's GPS routes them there. In the internet world, that's **DNS** — the Domain Name System. DNS turns a name like `www.myapp.com` into an actual IP address that your browser can connect to.

So today's story is: **DNS helps users find your service, and the Load Balancer decides which server handles their request.**

Let's break this down chunk by chunk.

---

## Step C: Core Teaching

Here's your **Chunk Map** for Day 4:

```
☐ 1. DNS Fundamentals — how names become addresses
☐ 2. DNS-Based Load Balancing — your first layer of distribution
☐ 3. L4 vs L7 Load Balancing — two very different approaches
☐ 4. LB Algorithms — Round Robin, Least Connections, IP Hash, Weighted
☐ 5. Observability Mini — SLIs, SLOs, Alerts, Dashboards for LBs
```

We'll tackle each one and I'll check your understanding before we move on. Let's go.

---

### Chunk 1: DNS Fundamentals — How Names Become Addresses

When you type `www.google.com` into your browser, your computer has no idea where that is. It's like saying "take me to John's house" — you need an address. DNS is the phone book of the internet. It translates human-readable names into IP addresses (like `142.250.80.46`).

**The DNS resolution flow** works like this:

```
You type www.google.com
  ↓
1. Browser cache — "Have I looked this up recently?" → if yes, done
  ↓ (miss)
2. OS cache — your computer's local resolver
  ↓ (miss)
3. Recursive Resolver (usually your ISP) — "Let me go find this for you"
  ↓
4. Root Name Server — "I don't know google.com, but .com is handled by this server"
  ↓
5. TLD Name Server (.com) — "google.com? Talk to Google's authoritative server"
  ↓
6. Authoritative Name Server — "www.google.com = 142.250.80.46. Here you go."
  ↓
Answer flows back through the chain, cached at each level
```

Three key concepts to remember:

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **TTL (Time To Live)** | How long (in seconds) a DNS answer can be cached before it expires | Low TTL = faster failover but more DNS queries. High TTL = fewer queries but slower updates when you change IPs. |
| **A Record** | Maps a domain name to an IPv4 address | The most basic record type. `www.myapp.com → 1.2.3.4` |
| **CNAME Record** | Maps a domain name to another domain name (alias) | `www.myapp.com → myapp.us-east-1.elb.amazonaws.com` — useful when your actual address changes (like cloud LB endpoints). |

Other record types you'll see: **AAAA** (IPv6), **MX** (mail), **NS** (nameserver delegation), **TXT** (verification/metadata).

**The DevOps angle:** In production, DNS TTL is a critical operational lever. When you're doing a migration or failover, a TTL of 300 seconds (5 min) means it could take 5 minutes for traffic to shift. During an emergency, that's an eternity. Many teams set low TTLs (30-60s) on records that might need fast changes, at the cost of more DNS traffic.

---

#### Feynman Gate — Chunk 1

**Stage 1 (Recall):**

In your own words, walk me through what happens when you type a URL into your browser and hit enter — specifically the DNS part. Don't worry about HTTP yet, just how the name gets resolved to an IP address.

*(Waiting for student response...)*

*Pass criteria: Student describes a multi-step lookup — browser/OS cache first, then recursive resolver, eventually reaching an authoritative server. Mentions that answers get cached. Doesn't need to name every server type, but should convey the hierarchical lookup concept.*

**Stage 2 (Transfer):**

Here's a scenario: You're running a service on AWS, and you need to migrate it from `us-east-1` to `eu-west-1`. Your DNS TTL is currently set to 86400 seconds (24 hours). What's the problem, and how would you fix it?

*(Waiting for student response...)*

*Pass criteria: Student recognizes that with a 24-hour TTL, clients will keep using the old cached IP for up to 24 hours after the migration. The fix is to lower the TTL well in advance of the migration (e.g., drop it to 60s a day before), do the migration, verify, then raise TTL again. This shows they understand TTL as more than a definition — they can apply it to a real operational problem.*

**Chunk 1: ✅ (assuming pass)**

---

### Chunk 2: DNS-Based Load Balancing — Your First Layer of Distribution

Here's the thing — DNS itself can act as a simple load balancer. When a client asks "what's the IP for `www.myapp.com`?", the authoritative DNS server doesn't have to return just one IP. It can return **multiple IPs**, or it can **choose which IP to return** based on rules.

There are three main DNS-based load balancing strategies:

**1. Weighted DNS**
```
www.myapp.com → 70% chance: 1.2.3.4 (primary data center)
                30% chance: 5.6.7.8 (secondary data center)
```
You assign weights to each IP. This is useful for gradual traffic shifting — like a canary deployment where you send 5% of traffic to the new version.

**2. Latency-Based DNS**
```
User in Tokyo → resolved to: 10.0.1.1 (ap-northeast-1)
User in London → resolved to: 10.0.2.1 (eu-west-1)
```
The DNS provider measures latency from the user's resolver to each endpoint and returns the fastest one. AWS Route 53 does this natively.

**3. Failover DNS**
```
Primary: 1.2.3.4 (us-east-1) — health check: healthy ✅
Secondary: 5.6.7.8 (us-west-2) — standby
→ Returns 1.2.3.4

If primary fails health check:
→ Returns 5.6.7.8
```
DNS health checks poll your servers. If the primary fails, DNS automatically returns the backup IP.

**The catch with DNS-based load balancing:** It's coarse-grained. You can't make per-request decisions. Once a client gets an IP, it caches it for the TTL duration and keeps going to that same server. You can't do things like "route this specific API call to the server with the least load." For that, you need a real load balancer — which is our next chunk.

**Think of it this way:** DNS-based LB is like the airport's flight display board telling you which terminal to go to. It gets you to the right building. But once you're inside the terminal, the gate agent (the actual LB) decides which boarding lane you use.

---

#### Feynman Gate — Chunk 2

**Stage 1 (Recall):**

Explain the three DNS-based load balancing strategies in your own words. For each one, give me a one-sentence description of when you'd use it.

*(Waiting for student response...)*

*Pass criteria: Student can name and describe weighted (traffic splitting/canary), latency-based (multi-region, lowest latency), and failover (DR/high availability). Doesn't need exact terminology but should convey the use case for each.*

**Stage 2 (Transfer):**

You're building a global service with data centers in US, Europe, and Asia. You're using DNS-based latency routing to send users to their closest data center. A customer in Singapore reports that they're being routed to the US data center instead of Asia. What are two possible reasons this might be happening?

*(Waiting for student response...)*

*Pass criteria: Student thinks about how DNS-based latency routing actually works. Possible answers include: (1) The user's recursive resolver (ISP DNS) might be located in the US, so the latency measurement points to the US endpoint. (2) The Asia data center might be failing health checks, so DNS is falling back to the US. Other valid answers: caching of a stale DNS response, misconfigured routing policy. The key is that the student understands DNS routing isn't based on the user's actual location — it's based on the resolver's location and latency measurements.*

**Chunk 2: ✅ (assuming pass)**

---

### Chunk 3: L4 vs L7 Load Balancing — Two Very Different Approaches

This is one of the most important distinctions in system design interviews.

Load balancers can operate at different layers of the network stack. The two you need to know are **Layer 4 (Transport)** and **Layer 7 (Application)**.

Think of it like mail sorting:

- **L4 (Layer 4)** is like a mail sorting machine that reads only the **address on the envelope** — it doesn't open the envelope. It routes based on IP address and port number. It's fast because it doesn't inspect the contents.

- **L7 (Layer 7)** is like a mail clerk who **opens the envelope, reads the letter**, and then routes it to the right department based on what the letter says. It can route based on the URL path, HTTP headers, cookies, or even the request body.

Here's a concrete comparison:

| Aspect | L4 Load Balancer | L7 Load Balancer |
|--------|-----------------|-----------------|
| **What it sees** | IP addresses + port numbers (TCP/UDP) | Full HTTP request (URL, headers, cookies, body) |
| **Routing decisions** | Source/destination IP, port | URL path (`/api` vs `/static`), host header, cookie value |
| **Performance** | Faster — no packet inspection | Slower — must parse HTTP (but still very fast in practice) |
| **TLS termination** | Passes through (or terminates, but can't inspect) | Terminates TLS, can inspect decrypted traffic |
| **Protocol support** | Any TCP/UDP protocol (HTTP, gRPC, database, custom) | HTTP/HTTPS only (some support gRPC, WebSocket) |
| **Use cases** | Raw throughput, non-HTTP protocols, simple distribution | Content-based routing, A/B testing, canary deployments, API gateway |
| **AWS equivalent** | NLB (Network Load Balancer) | ALB (Application Load Balancer) |

> ⚠️ **Common Misconception:** "L7 is always better than L4."
>
> **No.** L4 has lower latency and is better for non-HTTP protocols (databases, game servers, custom TCP) and raw throughput scenarios. L7 gives you content-based routing but adds processing overhead. **Choose based on what you need, not which layer number is higher.**

**When to use which — a simple decision tree:**

```
Do you need to route based on URL path, headers, or cookies?
  → YES → L7
  → NO  →
    Is the traffic non-HTTP (database, game server, gRPC passthrough)?
      → YES → L4
      → NO  →
        Do you need maximum throughput / minimum latency?
          → YES → L4
          → NO  → Either works; L7 gives you more flexibility for the future
```

**Real-world example:** Netflix uses L4 (NLB) for their video streaming traffic (pure TCP throughput matters) but L7 (ALB) for their API and web app (they need content-based routing, A/B testing, etc.).

---

#### Feynman Gate — Chunk 3

**Stage 1 (Recall):**

Explain the difference between L4 and L7 load balancing in your own words. What does each one "see" about the incoming traffic?

*(Waiting for student response...)*

*Pass criteria: Student conveys that L4 works at the transport layer (IP + port, doesn't look at content), while L7 works at the application layer (reads HTTP details like URL, headers, cookies). Should mention the trade-off: L4 is faster/simpler, L7 is more flexible.*

**Stage 2 (Transfer):**

You're designing a system that has two kinds of traffic:
1. A REST API serving JSON (`api.myapp.com/v1/users`)
2. A real-time gaming server using a custom TCP protocol on port 9000

You need a load balancer for each. Which type (L4 or L7) would you choose for each, and why?

*(Waiting for student response...)*

*Pass criteria: (1) REST API → L7, because you might want to route based on URL paths (e.g., `/v1/` vs `/v2/`), inspect headers, do A/B testing, and it's HTTP traffic. (2) Gaming server → L4, because it's a custom TCP protocol (not HTTP), so an L7 LB can't parse it. L4 just forwards TCP packets based on IP/port without needing to understand the protocol. Bonus if they mention L4 also gives lower latency, which matters for gaming.*

**Chunk 3: ✅ (assuming pass)**

---

## What's Next

We've covered 3 out of 5 chunks for today. Here's where we stand:

```
✅ 1. DNS Fundamentals — how names become addresses
✅ 2. DNS-Based Load Balancing — your first layer of distribution
✅ 3. L4 vs L7 Load Balancing — two very different approaches
☐ 4. LB Algorithms — Round Robin, Least Connections, IP Hash, Weighted
☐ 5. Observability Mini — SLIs, SLOs, Alerts, Dashboards for LBs
```

Next up is **Chunk 4: LB Algorithms** — this is where we get into the actual decision-making logic: how does the load balancer pick which server gets the next request? Then we'll wrap the core teaching with the Observability Mini before moving into Hands-On and Interview Drill.

Ready to continue?
