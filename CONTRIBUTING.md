# Contributing to PassForge

Thank you for your interest in making **PassForge** better!

We welcome contributions from everyone, whether it's reporting a bug, improving documentation, suggesting features, or submitting a Pull Request (PR).

## 1. Getting Started

### Prerequisites
*   Python 3.8 or higher
*   Git

### Clone the Repository
```bash
git clone https://github.com/krishnakanthb13/password_generator.git
cd password_generator
```

### Setup Virtual Environment
It is recommended to use a virtual environment for development:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .  # Link local package
```

## 2. Issues & Feature Requests

### Reporting Bugs
*   **Search**: Check existing issues before creating a new one.
*   **Template**: Use the provided issue template (if available).
*   **Details**: Include:
    *   PassForge version (`passforge --version`)
    *   Operating System
    *   Steps to reproduce
    *   Expected vs. actual behavior

### Suggesting Features
*   Describe the use case clearly.
*   Why is this feature useful?
*   How should the CLI syntax look? (e.g., `passforge my-feature --flag`)

## 3. Pull Requests

We follow standard GitHub flow:
1.  **Fork** the repository.
2.  Create a **branch** (`feature/new-command`, `fix/typo`).
3.  Make your changes.
4.  **Test** your changes locally (see Testing below).
5.  **Commit** with clear messages (`feat: add new generator`, `fix: correct entropy calc`).
6.  **Push** to your fork.
7.  Open a **Pull Request**.

### PR Guidelines
*   Keep PRs focused on a single change.
*   Update `README.md` if user-facing behavior changes.
*   Add unit tests for new logic.
*   Reference issue numbers (`Fixes #123`).

## 4. Testing

All new code must pass existing tests and include new tests if applicable.

### Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific file
python -m pytest tests/test_generator.py

# Check coverage
python -m pytest --cov=src
```

## 5. Coding Standards

*   **Style**: We follow **PEP 8**. Use `black` or `flake8` if possible.
*   **Type Hints**: Use Python type hints (`def func(a: int) -> str:`).
*   **Docstrings**: All public classes and functions must have docstrings (Google style).
*   **Imports**: Organized (STD lib -> Third party -> Local).

## 6. License

By contributing, you agree that your contributions will be licensed under the project's [license](LICENSE).
