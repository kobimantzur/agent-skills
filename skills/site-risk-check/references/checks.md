# What each check relates to

Descriptive only. This file names the standard or regime a condition is
commonly discussed under. It does not assert that a finding is a violation,
and it contains no penalty amounts, case citations, or article numbers.
If someone needs that, they need a lawyer, not this file.

| Code | Condition | Commonly discussed under |
|---|---|---|
| `missing-doc` (privacy policy) | No privacy policy linked | General privacy regimes (EU GDPR, California CCPA/CPRA, and most US state privacy laws) expect a published notice describing data collection |
| `missing-doc` (terms) | No terms of service linked | Contract formation and limitation-of-liability practice |
| `missing-doc` (cookie policy) | No cookie policy linked | EU ePrivacy Directive and GDPR guidance on cookie disclosure |
| `missing-doc` (accessibility statement) | No accessibility statement | EN 301 549 (EU public sector), and common practice in US ADA Title III demand-letter defense |
| `missing-doc` (refund/returns) | No refund or returns policy | Consumer protection regimes; also a Shopify and payment-processor requirement |
| `missing-doc` (contact/imprint) | No contact or imprint | German Impressumspflicht; EU e-Commerce Directive identification duties |
| `cookie-no-consent` | Server sets cookies before consent | ePrivacy Directive; prior-consent guidance from EU DPAs |
| `tracker-no-consent` | Analytics or ad pixels load with no consent gate | ePrivacy + GDPR; also the basis of US state wiretapping-style pixel claims |
| `img-alt` | Images without alt attributes | WCAG 2.2 SC 1.1.1 (Non-text Content), Level A |
| `html-lang` | No lang attribute on `<html>` | WCAG 2.2 SC 3.1.1 (Language of Page), Level A |
| `input-label` | Form inputs with no programmatic label | WCAG 2.2 SC 1.3.1, 4.1.2, Level A |
| `empty-control` | Links or buttons with no accessible name | WCAG 2.2 SC 2.4.4, 4.1.2, Level A |
| `no-h1` | No `<h1>` on the page | WCAG 2.2 SC 1.3.1 practice; also SEO |
| `target-blank` | `target="_blank"` without `rel="noopener"` | Security practice (reverse tabnabbing), not an accessibility criterion |
| `no-https` | Not served over TLS | Security-of-processing expectations under most privacy regimes |
| `no-hsts` | No HSTS header | Transport security hardening practice |

## What this tool does not check

Automated tooling covers a minority of WCAG success criteria. Not covered here:

- Colour contrast ratios
- Keyboard operability and focus order
- Whether alt text is *meaningful* rather than merely present
- Reading order and heading hierarchy semantics
- Screen-reader behaviour
- Motion, timing, and cognitive criteria
- Anything below the homepage — this scans one page
- Anything rendered client-side

A clean report from this tool means the listed conditions were not detected on
one statically-fetched page. It does not mean the site is accessible, nor that
it satisfies any legal obligation.
