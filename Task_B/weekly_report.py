"""Weekly tutor-hiring report. Run: python weekly_report.py candidates.csv"""
import csv
import sys
from collections import defaultdict
from datetime import date

SOURCES = {"referral": "Referral", "linkedin": "LinkedIn", "job board": "Job board",
           "meta": "Meta", "facebook": "Meta"}

def week_of(day):
    d = date.fromisoformat(day)
    return date.fromordinal(d.toordinal() - d.weekday()).isoformat()

def pct(part, whole):
    return f"{100 * part / whole:.1f}%" if whole else "-"

def count(rows):
    c = {"signups": 0, "attempted": 0, "passed": 0, "cet": 0, "inducted": 0}
    for r in rows:
        c["signups"] += 1
        c["attempted"] += bool(r["ai_test_attempted_at"])
        c["passed"] += bool(r["ai_test_passed_at"])
        c["cet"] += bool(r["cet_cleared_at"])
        c["inducted"] += bool(r["induction_attended_at"])
    return c

def print_table(title, groups):
    print(f"\n{title}")
    print(f"{'':<12}{'Signups':>9}{'AI pass rate':>14}{'CET pass':>12}{'Inductions':>12}{'Conversion':>12}")
    for name in sorted(groups):
        c = count(groups[name])
        print(f"{name:<12}{c['signups']:>9}{pct(c['passed'], c['attempted']):>14}"
              f"{pct(c['cet'], c['passed']):>12}{c['inducted']:>12}{pct(c['inducted'], c['signups']):>12}")

def main(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    by_week, by_source = defaultdict(list), defaultdict(list)
    for r in rows:
        by_week[week_of(r["signup_date"])].append(r)
        raw = r["source"].strip()
        canonical = SOURCES.get(raw.casefold(), raw or "(blank)")
        by_source[canonical].append(r)
    print_table("By signup week (week starting)", by_week)
    print_table("By source", by_source)

if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit("Usage: python weekly_report.py candidates.csv")
    main(sys.argv[1])
