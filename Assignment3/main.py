import argparse
from github_api import get_user_repo_commit_counts, RateLimited, NotFound

def main():
    parser = argparse.ArgumentParser(description="List repos and commit counts for a GitHub user.")
    parser.add_argument("username", help="GitHub username (e.g., richkempinski)")
    parser.add_argument("--max-repos", type=int, default=None, help="Limit number of repos (useful for demos/tests)")
    args = parser.parse_args()

    try:
        pairs = get_user_repo_commit_counts(args.username, max_repos=args.max_repos)
    except NotFound:
        print(f"User not found: {args.username}")
        return 1
    except RateLimited as e:
        more = f" (resets at epoch {e.reset_epoch})" if e.reset_epoch else ""
        print(f"Rate limited{more}. Try again later or set GITHUB_TOKEN.")
        return 2

    if not pairs:
        print(f"No public repos found for {args.username}.")
        return 0

    for repo, n in pairs:
        print(f"Repo: {repo} Number of commits: {n}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())