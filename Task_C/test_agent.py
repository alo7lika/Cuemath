import os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
from agent import lookup_for_email

class LookupGuardTests(unittest.TestCase):
    def test_sender_id_can_be_looked_up(self):
        result = lookup_for_email("C1", "C1", {"C1": {"candidate_id": "C1", "ai_test_passed_at": "2026-09-01"}})
        self.assertTrue(result["found"])
        self.assertEqual(result["ai_test_passed_at"], "2026-09-01")

    def test_friend_id_is_never_looked_up(self):
        result = lookup_for_email("C2", "C1", {"C1": {"candidate_id": "C1"}, "C2": {"candidate_id": "C2"}})
        self.assertFalse(result["found"])
        self.assertNotIn("candidate_id", result)

if __name__ == "__main__": unittest.main()
