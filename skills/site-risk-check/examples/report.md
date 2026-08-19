# Example report

Run against a real site with no consent mechanism:

```
SITE RISK CHECK — https://avorioatelier.com
Scanned 2026-08-19T22:37:52+00:00  ·  static scan

FINDINGS
  [HIGH] Trackers present with no consent mechanism detected: Meta Pixel
         → Gate these behind a consent banner, or confirm the banner is injected client-side (this scan cannot see that).
  [HIGH] Session-replay tools record keystrokes and clicks with no consent gate detected: Hotjar, Inspectlet
         → Load these only after consent. Under California's wiretapping statute (CIPA), session replay is the most frequently litigated web condition.
  [MED ] No link to cookie policy found on this page
         → Add a footer link to your cookie policy.
  [MED ] No 'Do Not Sell or Share My Personal Information' or 'Your Privacy Choices' link found
         → California requires a clear opt-out link on the homepage for businesses that sell or share personal information — ad pixels commonly count as sharing.
  [MED ] 1 of 47 <img> tags have no alt attribute
         → Add alt text. Decorative images take alt="".
  [LOW ] No link to contact / imprint found on this page
         → Add a footer link to your contact / imprint.
  [LOW ] No sign the site honours the Global Privacy Control browser signal
         → California requires honouring GPC as a valid opt-out. Most consent platforms support it once enabled — confirm it is switched on.
  [LOW ] No 'notice at collection' language found on this page
         → California expects notice of the categories collected and the purpose, at or before the point of collection.
  [LOW ] No Strict-Transport-Security header
         → Add an HSTS header.

TLDR — WHAT EACH FINDING IS CITED UNDER, AND WHAT IT TYPICALLY COSTS TO RESOLVE

  ISSUE                                         CITED UNDER               STATUTORY REF           TYPICAL RESOLUTION
  --------------------------------------------------------------------------------------------------------------------
  Session-replay tools record keystrokes and c  CIPA (CA wiretapping)     $5,000 per violation*   $10,000-$50,000
  Trackers present with no consent mechanism d  CIPA / CCPA sharing       $5,000* / $2,663        $10,000-$50,000
  No 'Do Not Sell or Share My Personal Informa  CCPA / CPRA               $2,663 per violation    $2,000-$10,000
  1 of 47 <img> tags have no alt attribute      ADA Title III / Unruh     fees + injunction       $5,000-$25,000
  No link to cookie policy found on this page   Consumer protection       varies                  $0-$5,000
  No sign the site honours the Global Privacy   CCPA / CPRA               $2,663 per violation    $2,000-$10,000
  No 'notice at collection' language found on   CCPA / CPRA               $2,663 per violation    $2,000-$10,000
  --------------------------------------------------------------------------------------------------------------------

  Exposure groups (4): CA privacy notice, accessibility, consumer protection, privacy/tracking
  ILLUSTRATIVE RANGE IF CHALLENGED ON ALL GROUPS: $17,000 - $90,000

  How to read this. A business receives demand letters, not one claim per
  finding — so groups are counted once at their worst case, not summed per
  row. Statutory figures are maxima that are almost never awarded; the ranges
  are commonly reported pre-suit settlement costs for small and mid-sized
  businesses. This is a sense of scale, NOT an estimate of what this site
  would pay, and not a prediction that anything will be claimed at all.
  * Courts disagree whether CIPA's $5,000 is per violation or per action.

  Remediation for everything above is typically a few hours of work. That
  asymmetry is the point of this table. See references/exposure.md.


24 checks run  ·  2 high, 3 medium, 4 low

NOT EVALUATED
  · Contrast ratios, keyboard navigation, focus order, and whether alt text is meaningful all require a human or a rendered scan.

This scan checks a defined list of conditions and reports what it could
not check. It does not determine legal compliance and is not legal advice.

```
