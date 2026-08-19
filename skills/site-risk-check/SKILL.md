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
2. **Never invent a statute, article number, case, or penalty amount.** If asked
   what a finding maps to, use `references/checks.md`. If it isn't there, say so.
3. **Always surface `not_evaluated` alongside findings.** The omissions matter as
   much as the flags. Never present findings without them.
4. **Treat `tracker-no-consent` as provisional on a client-rendered page.**
   Consent banners are usually injected by JavaScript and are invisible to a
   static scan. Say so rather than asserting a violation.
5. **This is not legal advice and is not a substitute for counsel review.** State
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

Present a table, then the not-evaluated list:

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
- ❌ Scanning a site the user does not own or operate without saying so.

## Limits

- Static fetch only. Client-rendered content is invisible.
- Automated testing covers a minority of WCAG success criteria. Keyboard traps,
  focus order, meaningful alt text and cognitive criteria need a human.
- Single page. It does not crawl.
- `robots.txt` is respected; disallowed paths are not fetched.
