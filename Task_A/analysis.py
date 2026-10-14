"""Reproducible funnel, version, device, and source analysis for Part A.
Run: python analysis.py candidates.csv
Uses Python's standard library only.
"""
import csv, sys
from collections import Counter, defaultdict
from datetime import date

FIELDS = ["ai_test_attempted_at", "ai_test_passed_at", "cet_cleared_at",
          "interview_at", "interview_cleared_at", "induction_attended_at"]

def pct(a, b): return 100*a/b if b else 0

def main(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    months = {m: [r for r in rows if r["signup_date"].startswith(m)] for m in ("2026-08", "2026-09")}
    print("PART A - cohort snapshot (cutoff 2026-10-05)")
    for m, rs in months.items():
        n = len(rs); print(f"\n{m}: signups={n}")
        prev = n
        for label, field in zip(("AI attempted", "AI passed", "CET cleared", "Interview booked", "Interview passed", "Induction attended"), FIELDS):
            count = sum(bool(r[field]) for r in rs)
            print(f"  {label:<19} {count:4d} ({pct(count,n):5.1f}% of signups; {pct(count,prev):5.1f}% of prior step)")
            prev = count
    print("\nImmediate AI test rates by month/version/device (pass / attempted)")
    for m in months:
        rs = months[m]
        groups = defaultdict(list)
        for r in rs: groups[(r["ai_test_version"] or "(blank)", r["device"])].append(r)
        for (version, device), group in sorted(groups.items()):
            attempted = sum(bool(r["ai_test_attempted_at"]) for r in group)
            passed = sum(bool(r["ai_test_passed_at"]) for r in group)
            print(f"  {m} {version:7} {device:7} n={len(group):4d} attempted={attempted:4d} pass={passed:4d} rate={pct(passed,attempted):5.1f}%")
    print("\nObserved induction conversion by source (descriptive; facebook kept distinct here)")
    for m, rs in months.items():
        groups = defaultdict(list)
        for r in rs: groups[r["source"] or "(blank)"].append(r)
        for source, group in sorted(groups.items()):
            attended = sum(bool(r["induction_attended_at"]) for r in group)
            print(f"  {m} {source or '(blank)':10} {attended:3d}/{len(group):4d} = {pct(attended,len(group)):5.2f}%")
    print("\nData note: induction conversion is right-censored at 2026-10-05; September has much shorter follow-up.")
    print("Reconcile facebook/Meta as an alias only for reporting; retain original value in source data.")

if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit("Usage: python analysis.py candidates.csv")
    main(sys.argv[1])
