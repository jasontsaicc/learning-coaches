# SD Coach Response — Day 4 (Load Balancer), Phase 1

---

## Step A: Review

**Previously on ScaleUp...** You survived your first three days at the startup. You learned what SD interviews actually test, practiced back-of-envelope estimation, and built your 4-Step SD Interview Framework. In the Phase 0 Gate, you proved you could walk through a full design answer with structure. 小球 promoted you from the onboarding track — and now the real work begins.

---

(★‿★) "Welcome back. Before we jump in — quick check. Last session you learned the 4-Step Framework. What are the four steps, and why does the order matter?"

> *(Waiting for your answer.)*

Good — I need to hear you say it, not just nod. This framework is your skeleton for every design answer going forward. If you can't recall it cold, we fix that now before stacking new material on top.

---

## Step B: Introduction

*The Slack channel lights up at 9:07 AM.*

(◎\_◎;) 小杰: "@channel the product page is DOWN. Users are getting 502s. I'm going to spin up a BIGGER server — 64 cores should fix it."

(★‿★) 小球 glances at you and shakes her head slowly. "He's about to throw money at a problem that money can't solve. Come on — let me show you what's actually happening."

---

Here's the situation: ScaleUp just got featured on a tech blog. Traffic spiked 10x overnight. You have one application server. One. Every request hits that single server. When it maxes out — 502 errors, page timeouts, angry users, Karen's Slack messages in ALL CAPS.

小杰's instinct? **Vertical scaling** — get a bigger machine. But think about it this way:

> **Analogy:** Imagine a restaurant with one waiter. The restaurant gets a rave review and suddenly 200 people show up. Do you hire a superhuman waiter who can serve 200 tables? Or do you hire 10 normal waiters and put a host at the front door to seat people evenly?

That host at the front door? That's a **Load Balancer**.

A load balancer sits between clients and your servers. It distributes incoming traffic across multiple backend servers so no single server gets overwhelmed. It's the difference between "buy a bigger box" (vertical scaling) and "add more boxes" (horizontal scaling).

Today we're going to understand exactly how that host decides who gets the next customer.

---

## Step C: Core Teaching

### Chunk Map

Here's what we'll cover today:

```
[ ] 1. What is a Load Balancer — and why you can't skip it
[ ] 2. DNS Fundamentals — how clients find your servers in the first place
[ ] 3. DNS-based Load Balancing — the simplest form of traffic distribution
[ ] 4. L4 vs L7 Load Balancing — the critical distinction
[ ] 5. LB Algorithms — Round Robin, Least Connections, IP Hash, Weighted
[ ] 6. Observability Mini — SLIs, SLOs, Alerts, Dashboards for LBs
```

Let's go chunk by chunk. You don't move to the next one until you can explain the current one back to me.

---

### Chunk 1: What is a Load Balancer — and why you can't skip it

A Load Balancer (LB) is a component that sits between clients and a pool of backend servers. Its job:

1. **Distribute traffic** across multiple servers
2. **Detect failures** — if a server dies, stop sending traffic to it
3. **Enable horizontal scaling** — add/remove servers without clients knowing

Without a load balancer, you're stuck with one server. When it dies, everything dies. When it's overloaded, everyone suffers.

With a load balancer:
- Clients talk to ONE address (the LB's IP)
- The LB forwards requests to one of N healthy backend servers
- If a server goes down, the LB routes around it automatically

```
                    ┌──────────┐
                    │  Client  │
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │   Load   │
                    │ Balancer │
                    └──┬──┬──┬─┘
                       │  │  │
              ┌────────┘  │  └────────┐
              ▼           ▼           ▼
         ┌────────┐  ┌────────┐  ┌────────┐
         │Server 1│  │Server 2│  │Server 3│
         └────────┘  └────────┘  └────────┘
```

In system design interviews, load balancers appear in almost every single answer. They're fundamental infrastructure.

---

#### Feynman Gate — Chunk 1

(★‿★) 小球 leans back. "OK. 小杰 wants to just upgrade to a 64-core machine instead of using a load balancer. Explain to me — in your own words — what a load balancer does and why 小杰's approach has a ceiling."

> **[Recall]** Explain what a load balancer is and why vertical scaling alone isn't enough.

*(Waiting for your answer.)*

---

Once you answer that, here's the follow-up:

(★‿★) "Good. Now think about this: **what happens if the load balancer itself goes down?** You've just moved the single point of failure from the server to the LB. Isn't that worse?"

> **[Transfer]** If the LB is now the single entry point, haven't we just moved the single point of failure? How would you address this?

*(This tests whether you can think beyond the basic concept. The answer involves LB redundancy — active-passive or active-active pairs — but I want to see if you can reason your way there.)*

---

### Chunk 2: DNS Fundamentals — how clients find your servers

Before we can load-balance traffic, we need to understand how clients find your server in the first place. That's DNS — the Domain Name System.

When a user types `www.scaleup.com` in their browser, here's what actually happens:

```
1. Browser checks its local cache → miss
2. OS checks its cache (hosts file, resolver cache) → miss
3. Query goes to Recursive Resolver (usually ISP or 8.8.8.8)
4. Resolver asks Root nameserver → "Who handles .com?"
5. Resolver asks .com TLD nameserver → "Who handles scaleup.com?"
6. Resolver asks ScaleUp's Authoritative nameserver → "52.14.23.89"
7. Resolver caches the answer (respecting TTL) and returns it
8. Browser connects to 52.14.23.89
```

Key concepts:

| Concept | What it means | Why it matters for SD |
|---------|--------------|----------------------|
| **TTL** (Time To Live) | How long a DNS answer is cached (e.g., 300s = 5 min) | Low TTL = faster failover but more DNS queries. High TTL = fewer queries but slower failover. |
| **A Record** | Maps domain to IPv4 address | Your basic "where is this server" record |
| **CNAME** | Maps domain to another domain | `www.scaleup.com → lb.scaleup.com` |
| **NS Record** | Points to the authoritative nameserver | Defines who "owns" your DNS zone |

**The DevOps angle:** TTL is a trade-off lever. During a migration or incident, you want low TTL (30s) so changes propagate fast. During normal operation, high TTL (3600s) reduces DNS query load. But beware — some clients and libraries ignore TTL and cache forever. In production, you can't assume DNS propagation is instant.

---

#### Feynman Gate — Chunk 2

(★‿★) "Alright. Imagine Karen comes to you in a panic: 'We changed our server IP 10 minutes ago but half our users still can't reach the new server!' Explain to me — in your own words — why this is happening."

> **[Recall]** Explain the DNS resolution flow and why changing an IP doesn't instantly reach all users.

*(Waiting for your answer.)*

---

Then:

(★‿★) "Nice. Now here's the trade-off question: Karen says 'Just set TTL to 1 second so changes are always instant.' What's wrong with that idea?"

> **[Transfer]** What's the downside of setting DNS TTL extremely low? Why don't we just always use a 1-second TTL?

*(This tests whether you understand that low TTL increases DNS query volume — every single request needs a fresh lookup. At ScaleUp's scale with 100K users, that's a LOT of DNS queries hitting your nameserver. It's a classic speed-of-change vs query-load trade-off.)*

---

### Chunk 3: DNS-based Load Balancing

Now that you understand DNS, here's the simplest way to load-balance: **use DNS itself.**

Instead of returning one IP for `www.scaleup.com`, your DNS server returns multiple IPs — and the client picks one (usually the first). Or your DNS server rotates which IP it returns first.

**Three approaches:**

| Strategy | How it works | Best for |
|----------|-------------|----------|
| **Weighted** | Assign weights to IPs. Server with weight 70 gets 70% of DNS responses. | Servers with different capacities |
| **Latency-based** | Return the IP with lowest measured latency to the client's region | Global deployments, multi-region |
| **Failover** | Return primary IP. If health check fails, switch to secondary. | Active-passive HA setups |

**AWS example:** Route 53 gives you all three of these as routing policies out of the box.

**But DNS-based LB has serious limitations:**

1. **No real-time health checks** — DNS TTL means stale records can send traffic to dead servers for minutes
2. **Client caching** — you can't force clients to refresh. Some cache for hours.
3. **Coarse-grained** — you're balancing per DNS query, not per request. One client resolves once and sends 1000 requests to the same server.
4. **No session awareness** — DNS doesn't know about HTTP sessions, cookies, or application state

(◎\_◎;) 小杰 overhears this and says: "Wait, so DNS load balancing is kind of... unreliable? Why does anyone use it?"

(★‿★) 小球 to you: "Good question from 小杰 for once. Why WOULD you use DNS-based load balancing despite these limitations?"

The answer: DNS-based LB works at the **global level** — distributing users to the nearest data center or region. Then within each data center, a proper L4/L7 load balancer handles per-request distribution. They work at different layers of the stack.

```
User (Tokyo) ──DNS──→ Asia DC ──L7 LB──→ Server pool
User (NYC)   ──DNS──→ US-East DC ──L7 LB──→ Server pool
```

---

#### Feynman Gate — Chunk 3

(★‿★) "Explain DNS-based load balancing in your own words. What can it do, and what can't it do?"

> **[Recall]** Describe DNS-based load balancing — how it works and its key limitations.

*(Waiting for your answer.)*

---

Then:

(★‿★) "Scenario: ScaleUp is expanding. We have servers in Tokyo and Virginia. A user in Osaka types scaleup.com. Walk me through which DNS strategy you'd use and why — and what happens AFTER the DNS lookup to handle individual requests."

> **[Transfer]** Given a multi-region setup, which DNS strategy fits, and how does DNS-based LB work together with a per-request load balancer?

*(This tests the two-layer mental model: DNS for global routing, L4/L7 LB for per-request routing within a region.)*

---

We've covered 3 of 6 chunks. Here's your updated Chunk Map:

```
[✅] 1. What is a Load Balancer — and why you can't skip it
[✅] 2. DNS Fundamentals — how clients find your servers in the first place
[✅] 3. DNS-based Load Balancing — the simplest form of traffic distribution
[ ] 4. L4 vs L7 Load Balancing — the critical distinction
[ ] 5. LB Algorithms — Round Robin, Least Connections, IP Hash, Weighted
[ ] 6. Observability Mini — SLIs, SLOs, Alerts, Dashboards for LBs
```

(The checkmarks assume you passed the Feynman Gates above. If any gate answer was incomplete, we'd go back and re-teach that chunk with a different analogy before moving on.)

---

## What comes next

When you're ready, we'll continue with **Chunk 4: L4 vs L7 Load Balancing** — this is where 小杰 drops his hot take that "L7 is obviously better because it's a higher number" and 小球 has to set the record straight. This chunk directly addresses the common misconception flagged in the curriculum:

> **Common Misconception:** "L7 is always better than L4." No — L4 has lower latency and is better for non-HTTP protocols and raw throughput. L7 gives you content-based routing but adds processing overhead.

After that, LB Algorithms (Chunk 5) and the Observability Mini (Chunk 6) — then we move to hands-on practice.

Take your time with the Feynman Gates above. There's no rushing through understanding.

(★‿★) "Your turn. Start with Chunk 1 — what's a load balancer, and why is 小杰 wrong about the 64-core server?"
