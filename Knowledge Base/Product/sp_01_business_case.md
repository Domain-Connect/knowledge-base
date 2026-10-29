# Business Case — Service Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: Service Providers*

---

## The Problem, Seen From Your Seat

Your customer has signed up, maybe paid, maybe built a site or set up mailboxes. The last step before your product delivers value is connecting their domain — and that step happens outside your product, in a DNS control panel you do not control and cannot see.

It shows up in your business in four places:

| Where it shows up | What you see |
|-------------------|--------------|
| **Activation funnel** | A sharp drop at the "connect your domain" step. About half of users fail manual DNS setup (Microsoft 365 data). |
| **Support queue** | "My email doesn't work", "my site isn't loading" — usually a record entered wrong, missing, or conflicting with an old one, at a registrar you cannot log into. |
| **Documentation** | Registrar-specific instructions that go stale whenever a registrar changes its UI. Microsoft maintains 16 help sites for this step, 10 of them registrar-specific. |
| **Retention** | Customers who never get their domain working get little value from your product, and churn. |

This is not a documentation problem you can write your way out of. If Microsoft, with 16 help sites and a 40-minute training for support agents, still sees ~50% failure, the issue is structural: you know what records are needed, the DNS provider holds the zone, and the customer is left to translate. See [01 — Problem & Context](../01_Problem_and_Context.md).

---

## What Domain Connect Changes

You describe the records your service needs in a **template** and publish it. When a customer enters their domain, your product checks whether their DNS provider supports Domain Connect and has your template. If so, you show **"Connect automatically"**. The customer logs in at their DNS provider, sees what will change, approves, and returns to your product with DNS configured exactly as specified.

Where Domain Connect is not available, the customer gets your existing manual instructions. Nothing gets worse.

---

## Value Levers

### 1. Activation at the domain step

For customers on supporting DNS providers, the domain step changes from a manual, error-prone task to a few clicks. The records are written exactly as your template defines them — no typos, no missing trailing dots, no duplicated SPF records.

**What to measure:** completion rate of the domain step, split by Domain Connect vs. manual, and by DNS provider.

### 2. Time to value

Customers connect in the same session, while they are motivated, instead of leaving to find their registrar login, opening a ticket, or coming back days later.

**What to measure:** time from signup to domain verified; share of customers verified within 24 hours.

### 3. Support deflection

The tickets that come from manual setup — wrong record, missing record, conflict with an old record, SPF overwritten — largely disappear for Domain Connect connections. The DNS provider handles conflicts and SPF merging.

**What to measure:** DNS-related tickets per 1,000 domain connections, Domain Connect vs. manual.

### 4. Less documentation to maintain

Customers on supporting DNS providers no longer need registrar-specific instructions. Your help content shrinks to a fallback for the long tail, and stops breaking every time a registrar redesigns its control panel.

### 5. Reach without bilateral deals

Your template, once published and deployed, works with any DNS provider that adopts it. New DNS providers joining the ecosystem can deploy your existing template — your coverage grows without a new integration on your side.

### 6. More options in the product

- **Subdomain or apex setups, with or without email** — record groups let one template support several configurations
- **Multi-step flows** such as verify-then-configure, and ongoing DNS updates, via the asynchronous (OAuth) flow
- **Sell-and-configure:** partner with a registrar so a customer can buy a domain inside your product and have it configured immediately (see [05 — Use Cases](../05_Use_Cases.md))

### 7. A standard, not a vendor API

One integration against an IETF Standards Track protocol, instead of a different API per registrar. Microsoft 365, Google Workspace, Apple iCloud+, Shopify and Squarespace are among the {{ facts.service_providers }} service providers that already use it.

---

## Size the Opportunity With Your Own Data

The knowledge base does not have a universal ROI figure, and you should not use someone else's. You can build a defensible estimate from data you already have.

### Step 1 — Measure your addressable share

The single most important number is how many of *your* customers are on a DNS provider that supports Domain Connect. You can measure it directly: take a sample of customer domains and look up `_domainconnect.<domain>` as a TXT record. Where the record exists, the DNS provider supports Domain Connect. Group the results by DNS provider to see where your customers are — and which providers to approach first.

### Step 2 — Quantify the funnel effect

| Input | Source |
|-------|--------|
| A — Customers attempting the domain step per year | Product analytics |
| B — Current completion rate of the domain step | Product analytics |
| C — Share of customers on supporting DNS providers | Step 1 |
| D — Expected completion rate via Domain Connect | Your assumption; validate with a pilot |
| E — Value of an activated customer (e.g. first-year revenue or LTV difference between activated and non-activated) | Finance / retention analysis |

**Additional activated customers per year ≈ A × C × (D − B)**  
**Value ≈ additional activated customers × E**

### Step 3 — Quantify support and documentation savings

| Input | Source |
|-------|--------|
| F — DNS-related tickets per year | Ticketing system tags |
| G — Fully loaded cost per ticket | Support finance |
| H — Expected deflection for Domain Connect connections | Your assumption; validate with a pilot |
| I — Annual effort to maintain registrar-specific documentation | Docs / support team |

**Annual saving ≈ F × C × H × G + share of I no longer needed**

### Worked Example — 100 Domain Configurations a Day

An illustrative service provider where **100 customers a day** reach the domain step. Every input is an assumption made up for the example; replace each one with your own data.

| Input | Conservative | Optimistic | Assumption |
|-------|-------------:|-----------:|------------|
| A — Customers attempting the domain step per year | 36,500 | 36,500 | 100 a day × 365 |
| B — Current completion rate | 50% | 50% | In line with the Microsoft 365 failure rate |
| C — Share on supporting DNS providers | 40% | 40% | Measure it in Step 1 |
| D — Completion rate via Domain Connect | 70% | 85% | |
| E — Value of an activated customer | €60 | €60 | First-year margin |
| F — DNS-related tickets per year | 7,300 | 7,300 | 20% of attempts |
| G — Cost per ticket | €20 | €20 | |
| H — Deflection for Domain Connect connections | 50% | 80% | |
| I — Annual registrar-specific documentation effort | €20,000 | €20,000 | Share no longer needed: 25% / 40% |

| Result | Conservative | Optimistic |
|--------|-------------:|-----------:|
| Attempts on supporting DNS providers (A × C) | 14,600 | 14,600 |
| Additional activated customers per year (A × C × (D − B)) | 2,920 | 5,110 |
| **Activation value** (× E) | **€175,200** | **€306,600** |
| Tickets avoided per year (F × C × H) | 1,460 | 2,336 |
| Support saving (F × C × H × G) | €29,200 | €46,720 |
| Documentation saving (share of I) | €5,000 | €8,000 |
| **Annual saving** | **€34,200** | **€54,720** |
| **Total per year** | **€209,400** | **€361,320** |

Activation dominates: 8–14 more of the 100 customers reaching the domain step each day end up with a working domain. C is the multiplier on everything, which is why Step 1 comes first, and it grows as more DNS providers deploy your template.

!!! tip "Keep the assumptions visible"
    D and H are the numbers your CFO will challenge. Put them in your proposal as explicit assumptions with a conservative and an optimistic case, and commit to measuring them on the first DNS providers that deploy your template. Because the manual path stays in place as a fallback, you will have a built-in control group.

---

## KPIs to Commit To

| KPI | Why it matters | When you can measure it |
|-----|----------------|-------------------------|
| Share of domain attempts where Domain Connect is offered | Effective coverage (DNS provider support × template deployed) | From launch |
| Click-through on "Connect automatically" | UX quality on your side | From launch |
| Domain Connect completion rate (returned and verified ÷ started) | End-to-end quality, including the DNS provider's consent flow | From launch |
| Domain step completion: Domain Connect vs. manual | Core activation lift | 1 month |
| DNS-related tickets per 1,000 connections, by path | Support deflection | 1–3 months |
| Number of DNS providers with your template deployed | Coverage growth | Ongoing |
| Retention of customers who connected via Domain Connect | Long-term value | 3–6 months |

---

## Why Now

- **The coverage is there.** {{ facts.dns_providers }} DNS providers, including the largest consumer registrars, already support it.
- **Your peers are there.** {{ facts.service_providers }} service providers have templates; customers increasingly expect one-click setup.
- **The standards risk is gone.** An IETF working group and a Standards Track draft mean one integration with a long future.
- **It is a contained investment.** You keep your manual path, so you can start with one template and one DNS provider and grow from measured results.

---

*Next: [Scope of Work](./sp_02_scope_of_work.md) · Back to: [Product Edition overview](../00_MASTER.md)*
