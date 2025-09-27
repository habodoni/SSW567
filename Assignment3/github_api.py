from __future__ import annotations
from typing import Iterable, List, Tuple, Optional, Dict, Any
import os
import time
import requests

class GitHubApiError(Exception):
    """Base class for GitHub API errors."""

class NotFound(GitHubApiError):
    """404 user or repo not found."""

class RateLimited(GitHubApiError):
    """Hit GitHub rate limit. Includes reset epoch."""
    def __init__(self, message: str, reset_epoch: Optional[int] = None):
        super().__init__(message)
        self.reset_epoch = reset_epoch

def _auth_headers(token: Optional[str]) -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "hw4a-tester"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def _next_link(link_header: Optional[str]) -> Optional[str]:
    # Parse RFC5988 Link header for rel="next"
    # Example: <https://api.github.com/...&page=2>; rel="next", <...>; rel="last"
    if not link_header:
        return None
    parts = [p.strip() for p in link_header.split(",")]
    for p in parts:
        if 'rel="next"' in p:
            start = p.find("<") + 1
            end = p.find(">", start)
            return p[start:end]
    return None

def _paged_get(session: requests.Session, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None) -> Iterable[Dict[str, Any]]:
    """
    Generator yielding items across all pages for a GitHub GET that returns a JSON array per page.
    Stops when there is no next link.
    """
    next_url = url
    params = dict(params or {})
    params.setdefault("per_page", 100)

    while next_url:
        resp = session.get(next_url, headers=headers, params=params if next_url == url else None, timeout=30)
        if resp.status_code == 404:
            raise NotFound(f"Resource not found: {next_url}")
        if resp.status_code == 403:
            # Could be rate limit. Try to surface reset time.
            reset = resp.headers.get("X-RateLimit-Reset")
            raise RateLimited("GitHub API rate limit exceeded or forbidden.", int(reset) if reset and reset.isdigit() else None)
        resp.raise_for_status()

        # Basic remaining-check (helpful diagnostics during tests)
        remaining = resp.headers.get("X-RateLimit-Remaining")
        if remaining is not None and remaining.isdigit() and int(remaining) <= 0:
            reset = resp.headers.get("X-RateLimit-Reset")
            raise RateLimited("Rate limit exhausted.", int(reset) if reset and reset.isdigit() else None)

        page = resp.json()
        if not isinstance(page, list):
            # Defensive: GitHub returns list here; if not, fail clearly.
            raise GitHubApiError(f"Expected a list JSON response at {next_url}")

        for item in page:
            yield item

        next_url = _next_link(resp.headers.get("Link"))

def get_user_repo_commit_counts(
    username: str,
    *,
    session: Optional[requests.Session] = None,
    token: Optional[str] = None,
    max_repos: Optional[int] = None
) -> List[Tuple[str, int]]:
    """
    Returns list of (repo_name, commit_count) for all public repos of `username`.
    - Handles pagination for repos and commits.
    - Uses per_page=100 for efficiency.
    - Optional `token` to raise rate limit to 5k/hr; can also read GITHUB_TOKEN env.
    - Optional `max_repos` for faster testing (limit number of repos processed).
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("username must be a non-empty string")

    token = token or os.getenv("GITHUB_TOKEN")
    close_session = False
    if session is None:
        session = requests.Session()
        close_session = True

    try:
        headers = _auth_headers(token)

        # 1) Get all repos
        repos_url = f"https://api.github.com/users/{username}/repos"
        repo_names: List[str] = []
        for repo in _paged_get(session, repos_url, headers):
            name = repo.get("name")
            if isinstance(name, str):
                repo_names.append(name)
            if max_repos is not None and len(repo_names) >= max_repos:
                break

        # 2) For each repo, count commits via paged commits API
        results: List[Tuple[str, int]] = []
        for repo_name in repo_names:
            commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
            count = 0
            for _ in _paged_get(session, commits_url, headers):
                count += 1
            results.append((repo_name, count))

        return results

    finally:
        if close_session:
            session.close()