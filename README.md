# Agent Skills

Skills for Claude Code, Codex, Gemini CLI, Cursor, and anything else that reads
`SKILL.md`. No dependencies, no API keys, no paid services.

| Skill | What it does |
|---|---|
| [site-risk-check](skills/site-risk-check) | Scan a live URL for the conditions that get sites flagged — missing policies, trackers before consent, accessibility gaps. Re-run to see only what changed. |

## Install

```bash
git clone https://github.com/kobimantzur/agent-skills.git && cd skills && ./install.sh
```

Symlinks every skill into `~/.claude/skills`, `~/.agents/skills`, and
`~/.codex/skills` — whichever exist. `git pull` updates them all.

Claude Code plugin install:

```bash
claude plugin marketplace add kobimantzur/agent-skills
```

Or copy a single skill folder into wherever your agent reads skills from.

## site-risk-check

```bash
python3 skills/site-risk-check/scripts/scan.py https://example.com
```

```
SITE RISK CHECK — https://example.com
Scanned 2026-08-19T15:05:05+00:00  ·  static scan

FINDINGS
  [HIGH] Trackers present with no consent mechanism detected: Meta Pixel
         → Gate these behind a consent banner, or confirm the banner is
           injected client-side (this scan cannot see that).
  [MED ] 14 of 22 <img> tags have no alt attribute
         → Add alt text. Decorative images take alt="".

16 checks run  ·  1 high, 1 medium, 0 low

NOT EVALUATED
  · Contrast ratios, keyboard navigation, focus order, and whether alt text
    is meaningful all require a human or a rendered scan.
```

Recurring — report only what changed:

```bash
python3 skills/site-risk-check/scripts/scan.py https://example.com --state .last-scan.json
```

Exits `1` on any HIGH finding, so it can gate CI.

### What it checks

Policy links (privacy, terms, cookies, accessibility, refunds, contact) ·
trackers loading without a consent mechanism · cookies set before consent ·
missing `alt` attributes · missing `lang` · unlabeled form inputs · empty
links and buttons · missing `<h1>` · `target="_blank"` without `noopener` ·
HTTPS and HSTS.

### What it does not check

Static fetch only — client-rendered content is invisible. Automated testing
covers a minority of WCAG success criteria; contrast, keyboard operability,
focus order, and whether alt text is *meaningful* all need a human. It scans
one page and does not crawl.

**Every report states which checks ran and which could not be evaluated. It
does not determine legal compliance and is not legal advice.**

## License

MIT
