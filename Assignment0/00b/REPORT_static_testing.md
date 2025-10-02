# Static Testing and Coverage Report

## Summary
- Repo URL: https://github.com/habodoni/SSW567 (branch: main)
- Static analyzer: Pylint 3.x
- Coverage tool: Coverage.py 7.x
- Results:
  - Pylint: 8.12/10 before fixes → 10.00/10 after fixes
  - Coverage: 98% total (tests already > 80%) before and after code cleanup

## Static Code Analysis
### Tool
- Pylint (run via: `python -m pylint Assignment0/00b/triangle.py`)

### Baseline Output (saved in `Assignment0/00b/pylint_baseline.txt`)
Key findings:
- C0114: Missing module docstring
- C0304: Missing final newline
- R0911: Too many return statements (7/6)

Overall score: 8.12/10

### Changes Applied
- Added module docstring to `triangle.py`.
- Refactored `classify_triangle` to reduce returns to a single return value variable.
- Ensured file ends with a newline.

### After Output (saved in `Assignment0/00b/pylint_after.txt`)
- No messages reported.
- Score: 10.00/10

Include screenshots of both baseline and after reports from the saved text files.

## Code Coverage
### Tool
- Coverage.py (run via: `python -m coverage run -m unittest -v Assignment0/00b/test_triangle.py` followed by `python -m coverage report -m`)

### Baseline Coverage (saved in `Assignment0/00b/coverage_baseline.txt`)
- Total coverage: 98%

### After Coverage (saved in `Assignment0/00b/coverage_after.txt`)
- Total coverage: 98%

Include screenshots of the coverage reports before and after.

## Tests
### Original Tests
- `test_equilateral`
- `test_isosceles`
- `test_scalene`
- `test_right`
- `test_isosceles_right`
- `test_float_right_tolerance`
- `test_not_a_triangle`
- `test_non_positive`

These tests already drove > 80% coverage and fully cover `triangle.py`.

### New Tests
- No new tests were required to exceed 80% coverage. Existing tests covered 100% of `triangle.py` lines.

## How to Reproduce Locally
- Environment: Python 3.13 (venv)
- Install tools:
  - `pip install pylint coverage`
- Run Pylint:
  - `python -m pylint Assignment0/00b/triangle.py`
- Run coverage:
  - `python -m coverage run -m unittest -v Assignment0/00b/test_triangle.py`
  - `python -m coverage report -m`

## Screenshots to Attach
1. Pylint baseline (from `pylint_baseline.txt`)
2. Coverage baseline (from `coverage_baseline.txt`)
3. Pylint after fixes (from `pylint_after.txt`)
4. Coverage after fixes (from `coverage_after.txt`)
