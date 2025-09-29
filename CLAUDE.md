# Claude Code Development Guide

This file contains information for Claude Code to help with development tasks for the Channel Advisor API Python project.

## Project Overview

This is a strongly typed Pydantic-based Python API client for Channel Advisor with built-in pagination, retries, and AI-enhanced product data capabilities.

## Development Commands

### Testing
```bash
# Run full test suite with coverage
make test

# Runs: pytest --cov --cov-branch --cov-report=xml --cov-report=term-missing:skip-covered
```

### Code Quality
```bash
# Run linting (flake8)
make lint

# Auto-fix formatting and imports
make fix

# Combines fix + lint
make lint-fix
```

### Versioning
```bash
# Check what version changes would be made (dry run)
make version-noop

# Create new version using semantic-release
make version
```

## Code Standards

- **Linting**: Use `flake8` for code linting (configured in `.flake8`)
- **Formatting**: Use `black` with 120 character line length
- **Import Management**: `autoflake` removes unused imports and variables
- **Testing**: `pytest` with coverage reporting required
- **Type Hints**: Full type annotation required (Pydantic models)

## Project Structure

```
channel_advisor_api/
├── models/           # Pydantic models and API wrappers
├── utils/           # Utility functions (logger, AWS helpers)
└── __init__.py
```

## Development Workflow

1. **Create Feature Branch**: Create a branch from `main`
2. **Implement Changes**: Follow coding standards, add tests
3. **Run Quality Checks**: `make lint-fix` and `make test`
4. **Create Pull Request**: Submit PR against `main` branch
5. **Merge**: After approval, merge triggers automatic PyPI deployment via GitHub Actions

## Environment Setup

Required environment variables for development:
```bash
CA_REFRESH_TOKEN=your_refresh_token
CA_APPLICATION_ID=your_application_id
CA_SHARED_SECRET=your_shared_secret
```

## Key Dependencies

- **pydantic**: Type validation and serialization
- **requests**: HTTP client for Channel Advisor API
- **aws-lambda-powertools**: AWS integration utilities

## Testing Guidelines

- Write tests for all new functionality
- Maintain test coverage (current config reports missing coverage)
- Use pytest fixtures for reusable test setup
- Mock external API calls in tests

## Deployment

- Automatic deployment to PyPI via GitHub Actions on merge to main
- Semantic versioning handled by `semantic-release`
- Version bumps automatically update `pyproject.toml` and `__init__.py`