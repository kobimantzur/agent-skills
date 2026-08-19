---
name: site-risk-check
description: Checks whether a website is legally covered against the complaints and demand letters sites actually receive: trackers and session recording running without consent, missing privacy or cookie policies, accessibility gaps. Detects the business profile, confirms which countries it sells to, then shows exposure only for regimes that apply there. Re-run to report only what changed. Triggers on "check my site", "am I legally covered", "could I get sued over my website", "what will get flagged", "accessibility check", "am I missing a privacy policy", "GDPR check". Reports which checks ran and which could not be evaluated; never claims compliance. Do NOT use for SEO, performance, or penetration testing.
license: MIT
---

# Site Risk Check

Scans a live URL for conditions commonly cited in accessibility and privacy
complaints. Static fetch, Python standard library, no API keys, no paid services.

## Quick start

```bash
python3 scripts/scan.py https://example.com
```

Recurring use — report only what changed:

```bash
python3 scripts/scan.py https://example.com --state .last-scan.json
```

JSON for piping into a report:

```bash
python3 scripts/scan.py https://example.com --json
```

Exit code is `1` when any HIGH finding is present, `0` otherwise, so it can gate CI.

## Hard rules

These are not stylistic preferences. Breaking them turns a helpful report into a
liability for whoever relies on it.

1. **Never state or imply that a site is compliant, legal, safe, or passing.**
   Report what was checked, what was flagged, and what could not be evaluated.
2. **Never invent a statute, article number, case, or penalty amount.** Figures
   come only from `references/exposure.md`; mappings only from `references/checks.md`.
   If it isn't in those files, say it isn't known.
3. **Always surface `not_evaluated` alongside findings.** The omissions matter as
   much as the flags. Never present findings without them.
4. **Treat `tracker-no-consent` as provisional on a client-rendered page.**
   Consent banners are usually injected by JavaScript and are invisible to a
   static scan. Say so rather than asserting a violation.
5. **Dollar ranges are scale, never prediction.** Present the TLDR exposure table
   as "what this kind of finding typically costs to resolve", never as "your fine
   is $X". Group by claim family — never sum a figure per finding. Always carry
   the caveat that statutory maxima are almost never awarded.
6. **This is not legal advice and is not a substitute for counsel review.** State
   that in every report you produce.

## Workflow

This is a two-pass flow. Never show exposure figures before the user has
confirmed which countries they sell to — the regimes that apply are entirely
different for an Israeli store versus a Californian one.

### Pass 1 — scan, then work out where they sell

1. If no URL was given, ask for one: *"What site should I check?"*
2. Run the scan:
   ```bash
   python3 scripts/scan.py https://SITE --state .last-scan.json
   ```
3. **Work out the markets from the site itself before asking the user anything.**
   `scan.py` already tries: Shopify and most storefronts render a country
   selector listing every market they ship to, and that is a better source than
   the user, who often does not know what their own storefront offers. Check
   `profile.detected_markets` and `profile.market_evidence`.

4. **If markets were detected**, state them with the evidence and let the user
   correct rather than supply:

   > The storefront's country selector ships to 28 countries, including the US,
   > the UK and 15 EU/EEA countries, plus Israel. So I'm checking against
   > Israeli, California, US federal and EU/UK rules. Tell me if that's wrong.

   Then continue to Pass 2 without waiting. Do not block on confirmation when
   the evidence is strong — only when it is absent or contradictory.

5. **If no markets could be detected** — no country selector, a single-market
   store, a non-ecommerce site, or a client-rendered page the scan could not
   read — then ask, and say why you are asking:

   > I couldn't tell from the page which countries you sell to, and that decides
   > which laws apply. Which of these apply? `IL` (Israel), `US-CA` (California),
   > `US` (rest of the United States), `EU` (EU/EEA/UK).

   Do not guess, and never infer markets from the base country alone — where a
   store is hosted says nothing about where it ships.

6. Show the rest of the detected profile so the user can correct it: platform,
   base country, currencies, languages, and what is running on the page
   (ad pixels, session replay, chat, subscription apps).

### Pass 2 — report against the confirmed markets

5. Re-run with the confirmed markets:
   ```bash
   python3 scripts/scan.py https://SITE --markets IL,US-CA
   ```
6. Lead with the exposure section, then the findings, then what was not checked.
7. If the page is client-rendered, say plainly that the markup checks are
   unreliable and the result is a floor, not a picture.
8. Offer remediation from `references/remediation.md`, ordered by how much each
   fix removes. One fix usually clears several findings — say which.

## Producing evidence for a legal or compliance team

When the user says the output is for legal, counsel, an auditor, or a compliance
review, produce a dated document rather than a terminal summary:

- Header: URL, UTC timestamp, scan type (static), tool version.
- The full list of checks run — the negative space is the evidence.
- Findings by severity.
- Checks not evaluated, stated as limitations.
- A sign-off line: `Run by ____ on ____. Static scan. Rendered scan not performed.`
- Closing: not legal advice, not a substitute for counsel review.

Offer to write it to a Markdown file so it can be exported to PDF.

## Antipatterns

- ❌ "Your site is GDPR compliant." → ✅ "No consent-related conditions flagged among the checks run."
- ❌ Reporting findings without the not-evaluated list.
- ❌ Asserting a consent violation on a page the scan could not render.
- ❌ Citing a specific article, fine, or case the references do not contain.
- ❌ "Your fine will be $47,500." → ✅ "Findings in this group typically resolve at $10,000–$50,000 pre-suit."
- ❌ Summing a dollar figure per finding — inflates by 3-5x and is indefensible.
- ❌ Scanning a site the user does not own or operate without saying so.
- ❌ Asking the user for markets without first trying to detect them from the page.
- ❌ Showing exposure figures when markets are neither detected nor confirmed.
- ❌ Assuming markets from the detected base country — where a store is hosted
     says nothing about where it ships.
- ❌ Citing California law at a store that does not sell to California.

## Limits

- Static fetch only. Client-rendered content is invisible.
- Automated testing covers a minority of WCAG success criteria. Keyboard traps,
  focus order, meaningful alt text and cognitive criteria need a human.
- Single page. It does not crawl.
- `robots.txt` is respected; disallowed paths are not fetched.
