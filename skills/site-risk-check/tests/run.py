#!/usr/bin/env python3
"""Run scan.py over every saved fixture and print a code matrix.

    python3 tests/run.py              # show matrix
    python3 tests/run.py --snapshot   # record current output as expected
    python3 tests/run.py --check      # fail if output drifted from snapshot

Fixtures are saved HTML. Add one with:
    python3 scripts/scan.py https://site.com --save tests/fixtures/site.html
"""
import json, os, sys, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import scan as S

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "expected.json")


def run_all():
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "fixtures", "*.html"))):
        name = os.path.basename(f)[:-5]
        html = open(f, encoding="utf-8", errors="ignore").read()
        r = S.scan("https://" + name.replace("_", "."), offline=html)
        out[name] = sorted(f["code"] for f in r.get("findings", []))
    return out


def matrix(res):
    codes = sorted({c for v in res.values() for c in v})
    w = max(len(c) for c in codes) + 2
    names = list(res)
    print(" " * w + "".join(f"{n[:11]:>13}" for n in names))
    for c in codes:
        row = "".join(f"{res[n].count(c) or '·':>13}" for n in names)
        print(f"{c:<{w}}" + row)
    print()
    for n in names:
        print(f"  {n:<16} {len(res[n])} findings")


if __name__ == "__main__":
    res = run_all()
    if "--snapshot" in sys.argv:
        json.dump(res, open(SNAP, "w"), indent=1)
        print(f"snapshot written: {SNAP}")
    elif "--check" in sys.argv:
        try:
            exp = json.load(open(SNAP))
        except OSError:
            sys.exit("no snapshot — run --snapshot first")
        bad = False
        for k in sorted(set(exp) | set(res)):
            a, b = exp.get(k, []), res.get(k, [])
            if a != b:
                bad = True
                print(f"DRIFT {k}\n  was: {a}\n  now: {b}")
        print("no drift" if not bad else "")
        sys.exit(1 if bad else 0)
    else:
        matrix(res)
