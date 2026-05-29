import unittest

import claude_review


SAMPLE_DIFF = """diff --git a/app.py b/app.py
index 1111111..2222222 100644
--- a/app.py
+++ b/app.py
@@ -1,2 +1,4 @@
 print("hello")
+API_KEY = "not-a-real-test-token"
+eval(user_input)
"""


class ClaudeReviewTests(unittest.TestCase):
    def test_parse_pr_url(self):
        self.assertEqual(
            claude_review.parse_pr_url("https://github.com/example/project/pull/42"),
            ("example", "project", "42"),
        )

    def test_summarize_diff_counts_files_and_additions(self):
        stats = claude_review.summarize_diff(SAMPLE_DIFF)
        self.assertEqual(stats.files, ["app.py"])
        self.assertEqual(stats.additions, 2)
        self.assertEqual(stats.deletions, 0)
        self.assertEqual(stats.hunks, 1)

    def test_risk_detection_finds_security_patterns(self):
        stats = claude_review.summarize_diff(SAMPLE_DIFF)
        risks = {risk.title for risk in claude_review.find_risks(stats)}
        self.assertIn("Possible secret added", risks)
        self.assertIn("Dynamic code execution", risks)

    def test_render_review_has_required_sections(self):
        stats = claude_review.summarize_diff(SAMPLE_DIFF)
        output = claude_review.render_review("https://github.com/example/project/pull/42", stats)
        self.assertIn("## Summary", output)
        self.assertIn("## Identified Risks", output)
        self.assertIn("## Improvement Suggestions", output)
        self.assertIn("## Confidence:", output)


if __name__ == "__main__":
    unittest.main()
