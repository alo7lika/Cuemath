import csv, os, subprocess, sys, tempfile, unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "weekly_report.py")

class WeeklyReportTests(unittest.TestCase):
    def run_report(self, rows):
        with tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["signup_date", "source", "ai_test_attempted_at", "ai_test_passed_at", "cet_cleared_at", "induction_attended_at"])
            writer.writeheader(); writer.writerows(rows); path = f.name
        try:
            return subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True, check=True).stdout
        finally: os.unlink(path)

    def test_alias_and_unknown_source_do_not_crash(self):
        out = self.run_report([
            {"signup_date":"2026-09-01", "source":"facebook", "ai_test_attempted_at":"2026-09-01", "ai_test_passed_at":"2026-09-01", "cet_cleared_at":"2026-09-02", "induction_attended_at":"2026-09-07"},
            {"signup_date":"2026-09-02", "source":"New channel", "ai_test_attempted_at":"", "ai_test_passed_at":"", "cet_cleared_at":"", "induction_attended_at":""},
        ])
        self.assertIn("Meta", out); self.assertIn("New channel", out)

    def test_rates_use_ticket_denominators(self):
        out = self.run_report([
            {"signup_date":"2026-09-01", "source":"Meta", "ai_test_attempted_at":"2026-09-01", "ai_test_passed_at":"2026-09-01", "cet_cleared_at":"2026-09-02", "induction_attended_at":""},
            {"signup_date":"2026-09-02", "source":"Meta", "ai_test_attempted_at":"2026-09-02", "ai_test_passed_at":"", "cet_cleared_at":"", "induction_attended_at":""},
        ])
        self.assertIn("50.0%", out)  # one AI pass / two signups; one CET / one AI passer
        self.assertIn("100.0%", out)  # CET pass rate uses AI passers as denominator

if __name__ == "__main__": unittest.main()
