# User: Skilled — "I was doing this for twelve clients. Then I wasn't."

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

Part of running a small web agency is that you become the de facto IT person for every client you build a site for. That means, among other things, that you end up configuring DNS.

For most clients, the domain is at whatever registrar they registered it with years ago — sometimes a decade ago — and they have no idea what the password is. Step one is account recovery. Step two is navigating to the DNS management panel, which looks completely different at GoDaddy versus IONOS versus Namecheap versus Google Domains versus whatever other registrar the client happens to use. Step three is applying the records the hosting platform or email provider requires.

I had a checklist. MX records for email, CNAME for the website, TXT for domain verification, SPF, DKIM. I knew the patterns. But every registrar's interface was subtly different. At one registrar the CNAME target needs a trailing dot; at another it doesn't. At one registrar TTL is a dropdown; at another it's a number field. At another the DNS management is buried three levels deep in a menu structure that changes every year.

I'd done this enough times to be fast. But "fast for a skilled person doing a manual process" is still fifteen to thirty minutes per client. And occasionally I'd make a mistake — a typo in an MX target, a priority value in the wrong field — and then I'd have to wait for propagation to confirm the error, fix it, and wait again.

Then a hosting platform we use for most of our client sites rolled out Domain Connect support.

The first time I saw the "Connect automatically" button, I assumed it was a marketing shortcut that would still require me to go do something in the DNS panel. I clicked it anyway. It redirected to the client's registrar — one I'd been configuring manually for years. A consent screen listed exactly what records would be created. I clicked Connect.

Done. No panel navigation. No field-by-field entry. No waiting to see if I'd made a typo.

I tried it with the next client. Different registrar, same result. Thirty seconds.

The implication took a moment to sink in. This wasn't just faster — it was categorically different. The per-registrar knowledge I'd accumulated, the checklists I'd built, the time I spent per client — all of it was addressing a problem that Domain Connect routes around entirely. The two systems that needed to talk to each other — the hosting platform and the DNS provider — were now talking to each other directly, with the client's consent. I was no longer the translator.

Not every client's registrar supports it yet. I still do manual DNS configuration for the registrars that haven't implemented Domain Connect. But for the ones that have, I've recovered meaningful time per client — time I now spend on work that actually requires my judgment.

The other thing I've noticed: I don't get "my website isn't loading" calls from clients whose domains I connected via Domain Connect. The records are applied correctly every time, automatically. The error mode that generated those calls — a typo I made in the DNS panel at midnight before a launch — simply doesn't happen anymore.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
