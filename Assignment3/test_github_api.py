import os
import sys
import unittest

# Allow running this test from repo root by adding this directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))
from github_api import get_user_repo_commit_counts, NotFound, RateLimited

class TestGitHubApi(unittest.TestCase):
    """Live integration tests against GitHub API for HW03a (no mocks)."""

    def test_happy_path_live_user(self):
        out = get_user_repo_commit_counts("richkempinski", max_repos=2)
        # Expect at least one repo; do not assert exact counts as they change
        self.assertIsInstance(out, list)
        self.assertTrue(len(out) >= 1)
        name, count = out[0]
        self.assertIsInstance(name, str)
        self.assertIsInstance(count, int)

    def test_live_user_limited_repos(self):
        out = get_user_repo_commit_counts("richkempinski", max_repos=1)
        self.assertEqual(len(out), 1)

    def test_user_not_found(self):
        with self.assertRaises(NotFound):
            get_user_repo_commit_counts("this-user-does-not-exist-xyz-abc-123")

    def test_rate_limited_env_note(self):
        # Not asserting RateLimited here because we don't want to burn quota.
        # Instead, verify that code can run with a token if provided.
        token = os.getenv("GITHUB_TOKEN")
        if token:
            out = get_user_repo_commit_counts("richkempinski", max_repos=1)
            self.assertTrue(len(out) == 1)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            get_user_repo_commit_counts("")

if __name__ == "__main__":
    unittest.main()