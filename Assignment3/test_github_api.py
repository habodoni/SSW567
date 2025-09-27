import unittest
from unittest.mock import MagicMock
import requests
from github_api import get_user_repo_commit_counts, NotFound, RateLimited

class TestGitHubApi(unittest.TestCase):
    def _make_session(self, pages):
        """
        Create a fake session where .get returns a sequence of responses.
        `pages` is a list of dicts:
           {"status": 200, "json": [...], "headers": {"Link": "...", "X-RateLimit-Remaining": "10"}}
        Each call to get() returns the next page. If Link contains rel="next", _paged_get will call again.
        """
        session = requests.Session()
        get_mock = MagicMock()
        def _resp_builder(page):
            resp = MagicMock()
            resp.status_code = page.get("status", 200)
            resp.headers = page.get("headers", {})
            def raise_for_status():
                if resp.status_code >= 400:
                    raise requests.HTTPError(f"{resp.status_code}")
            resp.raise_for_status = raise_for_status
            resp.json = MagicMock(return_value=page.get("json", []))
            return resp

        responses = [ _resp_builder(p) for p in pages ]
        get_mock.side_effect = responses
        session.get = get_mock
        return session

    def test_happy_path_single_repo_single_page_commits(self):
        # repos page (single page, no Link)
        repos_page = {
            "status": 200,
            "json": [{"name": "hellogitworld"}],
            "headers": {"X-RateLimit-Remaining": "50"}
        }
        # commits page (single page, 3 commits)
        commits_page = {
            "status": 200,
            "json": [{}, {}, {}],
            "headers": {"X-RateLimit-Remaining": "49"}
        }
        session = self._make_session([repos_page, commits_page])
        out = get_user_repo_commit_counts("richkempinski", session=session)
        self.assertEqual(out, [("hellogitworld", 3)])

    def test_repos_pagination_and_commit_pagination(self):
        # repos: 2 pages -> repoA, repoB
        repos_page1 = {
            "status": 200,
            "json": [{"name": "A"}],
            "headers": {
                "Link": '<https://api.github.com/users/u/repos?page=2>; rel="next", <...>; rel="last"',
                "X-RateLimit-Remaining": "50"
            }
        }
        repos_page2 = {
            "status": 200,
            "json": [{"name": "B"}],
            "headers": {"X-RateLimit-Remaining": "49"}
        }
        # commits for A: 2 pages (2 + 1 commits)
        commits_A_1 = {
            "status": 200,
            "json": [{}, {}],
            "headers": {
                "Link": '<https://api.github.com/repos/u/A/commits?page=2>; rel="next"',
                "X-RateLimit-Remaining": "48"
            }
        }
        commits_A_2 = {"status": 200, "json": [{}], "headers": {"X-RateLimit-Remaining": "47"}}
        # commits for B: single page (0 commits)
        commits_B = {"status": 200, "json": [], "headers": {"X-RateLimit-Remaining": "46"}}

        session = self._make_session([repos_page1, repos_page2, commits_A_1, commits_A_2, commits_B])
        out = get_user_repo_commit_counts("u", session=session)
        self.assertEqual(sorted(out), [("A", 3), ("B", 0)])

    def test_user_not_found(self):
        not_found = {"status": 404, "json": [], "headers": {}}
        session = self._make_session([not_found])
        with self.assertRaises(NotFound):
            get_user_repo_commit_counts("nope", session=session)

    def test_rate_limited(self):
        limited = {
            "status": 403,
            "json": {"message": "API rate limit exceeded"},
            "headers": {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1700000000"}
        }
        session = self._make_session([limited])
        with self.assertRaises(RateLimited):
            get_user_repo_commit_counts("someone", session=session)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            get_user_repo_commit_counts("")

if __name__ == "__main__":
    unittest.main()