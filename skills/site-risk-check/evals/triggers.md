# Trigger evals

Ten prompts that SHOULD load this skill, five that should NOT.
Run these after any edit to `description`. Target: 9/10 fire, 0/5 false-fire.

## Should fire

1. "check my site before I launch"
2. "am I missing a privacy policy on kobistore.com?"
3. "what will get flagged on our website?"
4. "run an accessibility check on https://example.com"
5. "legal asked me to verify the site — can you produce something?"
6. "did anything change on the site since last month?"
7. "is this site ready to ship?"
8. "we added a TikTok pixel, are we gated behind consent?"
9. "quick compliance sanity check on the store"
10. "client handoff — anything on their site that could bite them?"

## Should NOT fire

1. "audit my site's SEO" → seo-audit
2. "why is my site slow?" → performance
3. "pentest this endpoint" → security
4. "review this privacy policy wording" → legal drafting, not a scan
5. "check my Python code for bugs" → unrelated

## How to run

Start a fresh session with only this skill installed, paste each prompt, record
whether the skill loaded. Adjust the `description` — quoted phrasings for misses,
the `Do NOT use` clause for false fires. Re-run.
