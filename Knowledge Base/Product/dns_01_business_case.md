# Business Case — DNS Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: DNS Providers*

---

## The Problem, Seen From Your Seat

Your customers do not buy a domain to manage DNS. They buy it to run email on Microsoft 365, a shop on Shopify, a site on a website builder. The moment they try to connect the domain to that service, the service sends them a list of records — 7 to 15 of them for Microsoft 365 — and points them at your control panel.

What happens next is visible in three places in your business:

| Where it shows up | What you see |
|-------------------|--------------|
| **Support queue** | "I added the records but email doesn't work" — wrong field, missing trailing dot, conflicting old record, SPF duplicated instead of merged. Long time-to-resolution because success can only be verified after propagation. |
| **Activation** | About half of users who attempt manual DNS setup fail and give up. The domain stays parked. |
| **Renewals** | Domains with no content renew at ~70%; domains with high content at ~90% (CENTR Domain Renewal Study 2024). Every domain that never gets connected is renewal risk. |

The root cause is structural, not educational. The service provider knows which records it needs; you hold the zone; the customer is left to translate between the two. No help article fixes that — Microsoft maintains 16 help sites for this step, 10 of them registrar-specific, and still sees ~50% failure. See [01 — Problem & Context](../01_Problem_and_Context.md).

---

## What Domain Connect Changes

The service provider publishes a template describing the records its service needs. You review and deploy it. When the customer clicks "Connect" at the service provider, they land on **your** login and **your** consent screen, see what will change, and approve. Your system writes the records — correctly, with conflict detection and SPF merging — in one atomic operation.

You stay in control of every step: which templates you accept, what the consent screen says, who is authenticated, and what is written to the zone.

---

## Value Levers

### 1. Support cost deflection

Third-party DNS setup tickets are repetitive, high-volume and slow to close. With a template-based flow there is no transcription step, so the most common error class — wrong value in the wrong field — cannot occur. Conflict detection removes the "records look right but the service still doesn't work" escalations caused by leftover records.

**What to measure:** tickets tagged as third-party DNS setup per 1,000 active zones, split by service (Microsoft 365, Google Workspace, Shopify…).

### 2. Activation and renewal

Customers who complete the connection have a working service on the domain. That is the population that renews at ~90% rather than ~70%. Domain Connect turns a 40-minute, failure-prone task into a few clicks at the exact moment the customer is most motivated.

**What to measure:** share of domains with at least one service connected within 30/90 days of registration; renewal rate of Domain Connect–connected domains vs. a comparable cohort.

### 3. Customer experience at the moment that matters

Service providers run discovery on every domain a customer enters. If you support Domain Connect and host their template, they show a "Connect automatically" button. If you don't, your customer gets the manual instructions — and an experience that compares badly with customers of providers who are live. In a commoditised DNS market, activation experience is one of the few visible differentiators.

### 4. Ecosystem reach without bilateral deals

One implementation gives you access to **{{ facts.templates }} templates from {{ facts.service_providers }} service providers**. Most can be deployed straight from the public repository after your own review — no contract, no integration project per partner. Each new service provider that publishes a template becomes available to your customers at the cost of a review.

### 5. Strategic options

Once the capability exists, it supports moves beyond basic service integration:

- **Sell-and-configure:** partner with a service provider so a domain registered inside their product is configured immediately — collapsing registration and activation into one session
- **Your own services:** your hosting, email or website-builder products can use Domain Connect as a *service provider* to connect domains hosted at other DNS providers
- **Registrar-level use cases** under discussion in the IETF: nameserver changes and DNSSEC bootstrapping (see [05 — Use Cases](../05_Use_Cases.md))

### 6. A standard, not a vendor feature

Domain Connect has run in production since 2016, and the IETF approved the DCONN working group in October 2025. The specification (`draft-ietf-dconn-domainconnect-04`) is on the Standards Track. You are investing in shared infrastructure, not in a partner's proprietary API.

---

## Size the Opportunity With Your Own Data

The knowledge base does not have a universal ROI figure, and you should not use someone else's. You can build a defensible estimate from data you already have.

### Step 1 — Find the demand in your zones

Scan your hosted zones for records that point at well-known services, for example MX records ending in `mail.protection.outlook.com` (Microsoft 365) or `google.com` / `googlemail.com` (Google Workspace), and CNAMEs to e-commerce or website-builder platforms. This tells you:

- which services your customers already connect to (and therefore which templates to deploy first)
- how many connections happen today *despite* the manual process

Cross-check against the [template repository](https://github.com/Domain-Connect/Templates) to see which of those services already have templates.

### Step 2 — Quantify the support cost

| Input | Source |
|-------|--------|
| A — Monthly tickets about configuring DNS for a third-party service | Ticketing system tags or keyword search |
| B — Fully loaded cost per ticket | Support finance |
| C — Share of A for services that have a template | Step 1 cross-check |
| D — Expected deflection for those services once live | Your assumption; validate with a pilot |

**Annual support saving ≈ A × 12 × B × C × D**

### Step 3 — Quantify the activation and renewal effect

| Input | Source |
|-------|--------|
| E — New registrations per year | Registration data |
| F — Share that never get a service connected | Zone scan: no records beyond defaults after N days |
| G — Share of F you expect to convert via Domain Connect | Your assumption; validate with a pilot |
| H — Renewal uplift for converted domains | Up to ~20 points per CENTR data; use your own cohort data where possible |
| I — Annual renewal revenue per domain | Finance |

**Additional annual renewal revenue ≈ E × F × G × H × I**

### Worked Example — 100,000 Zones

An illustrative DNS provider hosting **100,000 zones**. Every input is an assumption made up for the example; replace each one with your own data.

| Input | Conservative | Optimistic | Assumption |
|-------|-------------:|-----------:|------------|
| A — Monthly third-party DNS setup tickets | 200 | 200 | 2 per 1,000 zones |
| B — Cost per ticket | €25 | €25 | |
| C — Share for services with a template | 60% | 60% | Mostly Microsoft 365, Google Workspace, website builders |
| D — Deflection once live | 50% | 80% | |
| E — New registrations per year | 15,000 | 15,000 | 15% of the zone count |
| F — Share never connected | 60% | 60% | |
| G — Share of F converted via Domain Connect | 5% | 15% | |
| H — Renewal uplift for converted domains | 10 points | 20 points | CENTR gap is ~20 points |
| I — Annual renewal revenue per domain | €12 | €12 | |

| Result | Conservative | Optimistic |
|--------|-------------:|-----------:|
| Tickets avoided per year (A × 12 × C × D) | 720 | 1,152 |
| **Annual support saving** (A × 12 × B × C × D) | **€18,000** | **€28,800** |
| Domains converted per year (E × F × G) | 450 | 1,350 |
| Additional renewals (E × F × G × H) | 45 | 270 |
| **Additional annual renewal revenue** (E × F × G × H × I) | **€540** | **€3,240** |
| **Total per year** | **€18,540** | **€32,040** |

At this size the support saving dominates. The renewal figure covers one registration cohort for one year: each new cohort adds its own converted domains, and converted domains keep renewing in the following years, so the effect builds up over time. The activation lever also matters more than its renewal revenue suggests, because a connected domain is where your own hosting, email and upsell products land.

!!! tip "Keep the assumptions visible"
    D and G are the numbers your CFO will challenge. Put them in your proposal as explicit assumptions, propose a conservative and an optimistic case, and commit to validating them with a pilot on your top two or three templates.

---

## KPIs to Commit To

| KPI | Why it matters | When you can measure it |
|-----|----------------|-------------------------|
| Domain Connect apply requests per month | Adoption by service providers and customers | From launch |
| Consent completion rate (approved ÷ consent screens shown) | Quality of your consent UX | From launch |
| Apply success rate (records written ÷ approved) | Engine and conflict-handling quality | From launch |
| Third-party DNS setup tickets per 1,000 zones | Support deflection | 1–3 months after launch |
| Templates deployed / share of observed service demand covered | Catalogue coverage | Ongoing |
| Domains with a connected service within 90 days of registration | Activation | 3–6 months |
| Renewal rate of Domain Connect–connected domains vs. cohort | Revenue impact | After one renewal cycle |

---

## Why Now

- **The ecosystem is ready.** Templates for the services your customers use most are already written and reviewed.
- **Service providers already look for you.** Discovery runs on every domain they see; supporting it is what turns their "Connect automatically" button on for your customers.
- **The standards risk is gone.** With an IETF working group and a Standards Track draft, the "proprietary protocol" objection no longer applies.
- **The renewal pressure is real.** Median domain growth across CENTR30 registries fell from ~4% (2022) to near 0% (2025). Retention is where growth now comes from.

---

*Next: [Scope of Work](./dns_02_scope_of_work.md) · Back to: [Product Edition overview](../00_MASTER.md)*
