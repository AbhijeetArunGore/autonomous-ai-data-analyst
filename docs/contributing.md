# Contributing Guidelines

Thank you for contributing to **AI Data Analyst OS**!

## Code & Commit Standards
- We enforce **Conventional Commits**: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `perf:`, `security:`, `ci:`, `chore:`.
- Python code must follow PEP8, formatted with `black` and linted with `ruff`.
- All agent logic must include unit tests under `backend/tests`.

## Development Workflow
1. Fork and clone the repository.
2. Install dependencies: `pip install -e .[dev]`
3. Run test suite: `pytest`
4. Submit pull requests against `main`.
