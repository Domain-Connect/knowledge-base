# Service Provider CEO — "Half our customers were failing at the finish line"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

We had a churn problem that didn't look like a churn problem.

Our activation funnel looked reasonable on the surface. People were signing up. A portion of them completed domain setup. We were growing. But when we looked at 90-day and 180-day retention, there was a sharp cliff. Customers who never got their domain working were churning at dramatically higher rates than customers who did.

That sounds obvious in retrospect. But we'd been treating DNS configuration as a user education problem. Write better help articles. Make a video tutorial. Add inline guidance. We'd invested significantly in all of that. It didn't move the needle.

The reason it didn't move the needle became clear when I looked at what Microsoft had to do to solve the same problem for Microsoft 365. They maintain 16 separate help sites for domain DNS setup — 10 of them registrar-specific, because every registrar's DNS interface is different and every registrar's interface changes. They need 40 minutes of training time for a support agent to reliably walk a customer through setup. And even with all of that, about half of users who attempt it fail.

That's Microsoft. With their resources. The documentation problem is not solvable with documentation.

Our head of engineering introduced me to Domain Connect. The pitch was simple: instead of us telling customers how to configure DNS — and updating that documentation for every registrar, every time a registrar changes their UI — we define what DNS records we need in a JSON template, the DNS provider hosts that template and presents a consent screen, and the user clicks one button.

I asked about the ecosystem. At the time, around 20 DNS providers supported it. Between them, they covered roughly 35% of the .com zone. The biggest registrars — GoDaddy, IONOS, Cloudflare, WordPress.com — were already live.

I asked about the implementation cost. Template authoring was a day's work. URL signing was a week. Discovery flow integration was another week. The ongoing cost was relationship management with DNS providers to get our template deployed — not engineering.

We implemented it. The results for customers using DNS providers that had deployed our template were immediate and significant. Activation rates went up. DNS-related support tickets went down. The customers who went through the Domain Connect flow didn't come back with "my email isn't working" tickets, because the records were applied correctly the first time.

The remaining activation gap is customers using DNS providers that haven't deployed our template yet. That's the push we're making now — expanding the set of DNS providers that carry our template.

The lesson I'd share with other SaaS executives: DNS configuration is not a user education problem and it is not a documentation problem. It is an architectural problem. Your service knows what DNS records it needs. The DNS provider knows what records are in the customer's zone. The only reason the customer has to be in the middle, manually translating between the two, is that no one built a standard for them to communicate directly. Domain Connect is that standard.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
