#!/usr/bin/env python3
"""
site-risk-check — scan a live URL for conditions commonly cited in
accessibility and privacy complaints.

Python standard library only. No pip install, no API keys, no paid services.

Usage:
    python3 scan.py https://example.com
    python3 scan.py https://example.com --json
    python3 scan.py https://example.com --state .last-scan.json   # diff mode

Limits (reported in every run, never hidden):
  * Static fetch only. Client-rendered content is invisible to this scan.
  * Automated checks cover a minority of WCAG success criteria. Keyboard
    traps, focus order, meaningful alt text and cognitive criteria all
    require a human.
  * This is not legal advice.
"""
import argparse, json, re, ssl, sys, time
import urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (compatible; site-risk-check/0.1; +https://github.com/kobimantzur/skills)"
TIMEOUT = 15
MAXBYTES = 2_000_000

HIGH, MED, LOW = "HIGH", "MED", "LOW"


def fetch(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.status, dict(r.headers), r.read(MAXBYTES).decode("utf-8", "ignore"), r.url


def robots_allows(url):
    """Best-effort robots.txt check. Fail open — we fetch one page as a browser would."""
    p = urllib.parse.urlparse(url)
    try:
        _, _, body, _ = fetch(f"{p.scheme}://{p.netloc}/robots.txt", timeout=6)
    except Exception:
        return True
    agent_all, disallow = False, []
    for line in body.splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            agent_all = v == "*"
        elif k == "disallow" and agent_all and v:
            disallow.append(v)
    path = p.path or "/"
    return not any(path.startswith(d) for d in disallow)


POLICIES = [
    ("privacy policy", r"privacy[-_/ ]?(policy|notice|statement)", HIGH),
    ("terms of service", r"terms[-_/ ]?(of[-_/ ]?(service|use)|and[-_/ ]?conditions)|\bterms\b", MED),
    ("cookie policy", r"cookie[-_/ ]?(policy|notice|statement)", MED),
    ("refund / returns policy", r"(refund|return|shipping)[-_/ ]?policy", LOW),
    ("accessibility statement", r"accessibility[-_/ ]?(statement|policy)", MED),
    ("contact / imprint", r"\b(contact[-_/ ]?us|imprint|impressum)\b", LOW),
]

CONSENT = (r"cookie[-_ ]?(consent|banner|notice|preferences)|cookiebot|onetrust|"
           r"klaro|osano|cookieyes|termly|iubenda|usercentrics|didomi|quantcast|complianz")

TRACKERS = [
    ("Google Analytics", r"google-analytics\.com|googletagmanager\.com|gtag\s*\("),
    ("Meta Pixel", r"connect\.facebook\.net|fbevents\.js|fbq\s*\("),
    ("TikTok Pixel", r"analytics\.tiktok\.com"),
    ("LinkedIn Insight", r"snap\.licdn\.com"),
    ("Hotjar", r"static\.hotjar\.com"),
    ("Microsoft Clarity", r"clarity\.ms"),
    ("Reddit Pixel", r"redditstatic\.com/ads"),
    ("Pinterest Tag", r"pintrk\s*\("),
    ("X / Twitter Pixel", r"static\.ads-twitter\.com"),
    ("Klaviyo", r"static\.klaviyo\.com"),
]


def strip_noise(html):
    """Remove script/style/comments so markup checks don't match code samples."""
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", "", html, flags=re.S | re.I)
    return html


def scan(url):
    started = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    findings, skipped, checks_run = [], [], 0

    def flag(sev, code, msg, fix=""):
        findings.append({"sev": sev, "code": code, "msg": msg, "fix": fix})

    if not robots_allows(url):
        return {"url": url, "scanned_at": started,
                "error": "robots.txt disallows this path — not scanned."}

    try:
        status, hdr, raw, final = fetch(url)
    except urllib.error.HTTPError as e:
        return {"url": url, "scanned_at": started, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"url": url, "scanned_at": started, "error": f"{type(e).__name__}: {e}"}

    html = strip_noise(raw)
    low_raw, low = raw.lower(), html.lower()

    # --- is this page even server-rendered? ---
    text_len = len(re.sub(r"<[^>]+>", " ", html).split())
    spa = text_len < 120
    if spa:
        skipped.append("Page appears client-rendered (%d words in static HTML). "
                       "Markup checks below are unreliable; a rendered scan is required." % text_len)

    # --- policy documents ---
    for name, pat, sev in POLICIES:
        checks_run += 1
        if not re.search(pat, low_raw):
            flag(sev, "missing-doc", f"No link to {name} found on this page",
                 f"Add a footer link to your {name}.")

    # --- consent vs trackers ---
    checks_run += 1
    has_consent = bool(re.search(CONSENT, low_raw))
    present = [n for n, p in TRACKERS if re.search(p, low_raw)]
    if present and not has_consent:
        flag(HIGH, "tracker-no-consent",
             "Trackers present with no consent mechanism detected: " + ", ".join(present),
             "Gate these behind a consent banner, or confirm the banner is "
             "injected client-side (this scan cannot see that).")
        if spa or "consent" not in low_raw:
            skipped.append("Consent banners are usually injected by JavaScript. "
                           "A 'tracker-no-consent' flag here may be a false positive — "
                           "verify with a rendered scan before acting.")

    checks_run += 1
    sc = hdr.get("Set-Cookie", "")
    if sc and not has_consent:
        flag(HIGH, "cookie-no-consent",
             "Server sets cookies on first request with no consent mechanism detected",
             "Restrict non-essential cookies until consent is given.")

    # --- accessibility: the machine-checkable subset ---
    checks_run += 1
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    noalt = [i for i in imgs if not re.search(r"\balt\s*=", i, re.I)]
    if noalt:
        flag(MED, "img-alt", f"{len(noalt)} of {len(imgs)} <img> tags have no alt attribute",
             "Add alt text. Decorative images take alt=\"\".")

    checks_run += 1
    if not re.search(r"<html[^>]+\blang\s*=", html, re.I):
        flag(MED, "html-lang", "<html> has no lang attribute",
             'Set <html lang="en"> (or the correct language).')

    checks_run += 1
    inputs = re.findall(r"<input\b[^>]*>", html, re.I)
    real = [i for i in inputs
            if not re.search(r'type\s*=\s*["\']?(hidden|submit|button|image|reset)', i, re.I)]
    unlabeled = [i for i in real if not re.search(r"aria-label|aria-labelledby|\bid\s*=", i, re.I)]
    if unlabeled:
        flag(MED, "input-label",
             f"{len(unlabeled)} of {len(real)} form inputs have no id or aria-label to bind a <label>",
             "Give each input an id and a matching <label for=...>, or an aria-label.")

    checks_run += 1
    empties = re.findall(r"<(button|a)\b[^>]*>\s*</\1>", html, re.I)
    if empties:
        flag(MED, "empty-control", f"{len(empties)} empty <a>/<button> elements have no accessible name",
             "Add visible text, or aria-label if the control is icon-only.")

    checks_run += 1
    if not re.search(r"<h1[\s>]", html, re.I):
        flag(LOW, "no-h1", "No <h1> element on this page",
             "Give every page one <h1> describing its purpose.")

    checks_run += 1
    if re.search(r'<a\b[^>]*target\s*=\s*["\']?_blank', html, re.I) and \
       not re.search(r"rel\s*=\s*[\"']?[^\"'>]*noopener", html, re.I):
        flag(LOW, "target-blank", "Links open in a new tab without rel=\"noopener\"",
             'Add rel="noopener noreferrer" to target="_blank" links.')

    # --- transport ---
    checks_run += 1
    if urllib.parse.urlparse(final).scheme != "https":
        flag(HIGH, "no-https", "Site is not served over HTTPS", "Enable TLS and redirect http to https.")
    checks_run += 1
    if "Strict-Transport-Security" not in hdr:
        flag(LOW, "no-hsts", "No Strict-Transport-Security header", "Add an HSTS header.")

    skipped.append("Contrast ratios, keyboard navigation, focus order, and whether "
                   "alt text is meaningful all require a human or a rendered scan.")

    return {
        "url": final, "scanned_at": started, "status": status,
        "trackers": present, "consent_detected": has_consent,
        "checks_run": checks_run, "findings": findings, "not_evaluated": skipped,
        "counts": {s: sum(1 for f in findings if f["sev"] == s) for s in (HIGH, MED, LOW)},
    }


def render(r, prev=None):
    if "error" in r:
        return f"site-risk-check — {r['url']}\n  Could not scan: {r['error']}\n"
    L = [f"SITE RISK CHECK — {r['url']}", f"Scanned {r['scanned_at']}  ·  static scan", ""]
    keys = {(f["code"], f["msg"]) for f in r["findings"]}
    old = {(f["code"], f["msg"]) for f in (prev or {}).get("findings", [])}

    if prev:
        new, fixed = keys - old, old - keys
        L.append(f"CHANGES SINCE {prev.get('scanned_at', 'last run')}")
        if not new and not fixed:
            L.append("  Nothing changed.")
        for f in r["findings"]:
            if (f["code"], f["msg"]) in new:
                L.append(f"  NEW    [{f['sev']:4}] {f['msg']}")
        for c, m in sorted(fixed):
            L.append(f"  FIXED         {m}")
        L.append("")

    if r["findings"]:
        L.append("FINDINGS")
        for sev in (HIGH, MED, LOW):
            for f in r["findings"]:
                if f["sev"] == sev:
                    L.append(f"  [{sev:4}] {f['msg']}")
                    if f["fix"]:
                        L.append(f"         → {f['fix']}")
    else:
        L.append("FINDINGS\n  None on the checks below.")

    c = r["counts"]
    L += ["", f"{r['checks_run']} checks run  ·  {c[HIGH]} high, {c[MED]} medium, {c[LOW]} low",
          "", "NOT EVALUATED"]
    L += [f"  · {s}" for s in r["not_evaluated"]]
    L += ["", "This scan checks a defined list of conditions and reports what it could",
          "not check. It does not determine legal compliance and is not legal advice."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Scan a live URL for commonly-flagged conditions.")
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    ap.add_argument("--state", metavar="PATH", help="compare against, then update, this state file")
    a = ap.parse_args()

    url = a.url if "://" in a.url else "https://" + a.url
    result = scan(url)

    prev = None
    if a.state:
        try:
            prev = json.load(open(a.state))
        except (OSError, ValueError):
            prev = None

    print(json.dumps(result, indent=2) if a.json else render(result, prev))

    if a.state and "error" not in result:
        with open(a.state, "w") as f:
            json.dump(result, f, indent=1)

    sys.exit(1 if result.get("counts", {}).get(HIGH) else 0)


if __name__ == "__main__":
    main()
