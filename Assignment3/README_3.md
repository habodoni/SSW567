# Assignment 3 – GitHub API (Tester's Mindset)

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/habodoni/SSW567/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/habodoni/SSW567/tree/main)

## How to Run

Follow these steps to set up and run the Assignment 3 GitHub API project:

### 1. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Or on Windows
# venv\Scripts\activate
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run the unit tests

```bash
python -m unittest -v
```

### 4. Run the program

Example usage:

```bash
python main.py richkempinski --max-repos 2
```

This will fetch repository and commit count information for the specified GitHub user, limiting the output to 2 repositories for demonstration purposes.

**Optional:** Set a GitHub personal access token to increase API rate limits:

```bash
export GITHUB_TOKEN=your_token_here
python main.py richkempinski --max-repos 2
```

## Reflection

Working on this assignment taught me valuable lessons about developing software with a tester's mindset. The key insight was designing code that is inherently testable from the ground up, rather than trying to retrofit tests afterward. By structuring the `github_api.py` module with dependency injection for the requests session, I could easily mock HTTP responses in my unit tests. This approach allowed me to test various scenarios such as successful API calls, pagination handling, rate limiting, and error conditions—without making actual network requests. Writing comprehensive unit tests that covered edge cases like empty repositories, user not found errors, and API rate limits helped me catch bugs early and build confidence in the code's correctness.

The biggest challenges I encountered were handling GitHub API pagination correctly and dealing with rate limits during development. Initially, I struggled with parsing the RFC5988 Link header format to detect when there were more pages of results. The rate limiting was particularly tricky because it required careful error handling and providing meaningful feedback to users about when they could retry. Additionally, I faced a CircleCI configuration issue where the build couldn't find the requirements.txt file in the correct path, which taught me about the importance of proper project structure and CI/CD configuration management.

Continuous Integration proved invaluable throughout this project by automatically running my test suite on every commit and ensuring that changes didn't break existing functionality. Having CircleCI automatically verify that my code passes all tests gives me confidence that the application works correctly across different environments. This automated testing approach catches integration issues that might not be apparent during local development, and the visible build status badge provides immediate feedback about the project's health. The CI pipeline serves as a safety net that proves correctness automatically, making it much easier to refactor code and add new features with confidence.
