---
name: site-risk-check
description: Scans a live URL for the conditions that get sites flagged: missing privacy policy or terms, trackers firing before cookie consent, images without alt text, unlabeled form inputs, no HTTPS. Re-run to report only what changed. Use before launching, before handing a site to a client, when legal or compliance asks for evidence, or on a schedule to catch drift. Triggers on "check my site", "what will get flagged", "did anything change on the site", "am I missing a privacy policy", "accessibility check". Reports which checks ran and which could not be evaluated; never claims compliance. Do NOT use for SEO, performance, or penetration testing.
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

1. Confirm the URL. If the user names a site without a scheme, use `https://`.
2. Run `scripts/scan.py`. Use `--state` if the user has scanned this site before,
   or wants ongoing monitoring.
3. If the run reports the page is client-rendered, say plainly that most markup
   checks are unreliable and the result is a floor, not a picture.
4. Present findings grouped by severity. Lead with HIGH. Never dump raw JSON.
5. List what was not evaluated.
6. Offer the remediation steps from `references/remediation.md` for anything flagged.
7. If the user asks what a finding relates to legally, use `references/checks.md`
   and stay descriptive.

## Output format

Lead with the TLDR exposure table — a founder acts on money, not on severity
labels. `scan.py` emits it; reformat as Markdown:

| Issue | Cited under | Statutory ref | Typical resolution |
|---|---|---|---|
| Session-replay tools with no consent gate | CIPA (CA wiretapping) | $5,000 per violation* | $10,000–$50,000 |
| Trackers with no consent mechanism | CIPA / CCPA sharing | $5,000* / $2,663 | $10,000–$50,000 |
| **4 exposure groups** | | | **$17,000 – $90,000 illustrative** |

Then always, immediately below it:

> Grouped by claim family, not summed per finding. Statutory figures are maxima
> that are almost never awarded; ranges are commonly reported pre-suit settlement
> costs. This is a sense of scale, not an estimate for this site, and not a
> prediction that anything will be claimed. Remediation is typically a few hours.

Then the detail table, then the not-evaluated list:

| Severity | Finding | Fix |
|---|---|---|
| HIGH | Trackers present with no consent mechanism detected: Meta Pixel | Gate behind consent, or confirm the banner is client-injected |

Then:

> 16 checks run · 1 high, 5 medium, 3 low
> Not evaluated: contrast ratios, keyboard navigation, focus order, whether alt text is meaningful.
> Not legal advice.

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

## Limits

- Static fetch only. Client-rendered content is invisible.
- Automated testing covers a minority of WCAG success criteria. Keyboard traps,
  focus order, meaningful alt text and cognitive criteria need a human.
- Single page. It does not crawl.
- `robots.txt` is respected; disallowed paths are not fetched.
