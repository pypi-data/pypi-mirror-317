# Dell Unisphere Mock API

> **IMPORTANT DISCLAIMER**
> This codebase is entirely generated using artificial intelligence.
> Users shall use it at their own risk.
> The authors make no warranties about the completeness, reliability, and accuracy of this code.
> Any action you take upon this code is strictly at your own risk.

A FastAPI-based mock implementation of the Dell EMC Unisphere REST API for testing and development purposes.

[![Tests](https://github.com/nirabo/dell-unisphere-mock-api/actions/workflows/test.yml/badge.svg)](https://github.com/nirabo/dell-unisphere-mock-api/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/nirabo/dell-unisphere-mock-api/branch/master/graph/badge.svg)](https://codecov.io/gh/nirabo/dell-unisphere-mock-api)
[![PyPI version](https://badge.fury.io/py/dell-unisphere-mock-api.svg)](https://badge.fury.io/py/dell-unisphere-mock-api)
[![Python Version](https://img.shields.io/pypi/pyversions/dell-unisphere-mock-api.svg)](https://pypi.org/project/dell-unisphere-mock-api)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Features

- Mock implementation of Dell EMC Unisphere REST API endpoints
- Support for basic authentication and CSRF token management
- Comprehensive test suite with high coverage
- Storage resource management (pools, LUNs, filesystems, etc.)
- Pagination and sorting support
- Based on FastAPI for modern async API development
- Enforced code quality with pre-commit hooks

## Installation

### From PyPI

```bash
pip install dell-unisphere-mock-api
```

For development features:
```bash
pip install "dell-unisphere-mock-api[test,dev]"
```

### From Source

```bash
git clone https://github.com/nirabo/dell-unisphere-mock-api.git
cd dell-unisphere-mock-api
make venv  # Creates virtual environment and installs package in editable mode with dev tools
```

## Usage

### Running the Server

```bash
# If installed from PyPI
python -m dell_unisphere_mock_api

# If installed from source
make run
```

The server will start at `http://localhost:8000`

## Development

### Project Structure

```
dell_unisphere_mock_api/
├── core/           # Core functionality (auth, etc.)
├── models/         # Data models
├── routers/        # API route handlers
└── schemas/        # Pydantic schemas
```

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Style guide enforcement
- **MyPy**: Static type checking
- **Bandit**: Security checks
- **pre-commit**: Automated checks before commits

These tools are automatically installed when you run `make venv` and set up as pre-commit hooks.

### Common Tasks

```bash
make help          # Show all available commands
make test          # Run tests with coverage
make lint          # Run all linters
make format        # Format code with black and isort
make typecheck     # Run type checking
make security      # Run security checks
make clean         # Clean all build and test artifacts
make build         # Build source and wheel package
make release       # Upload to PyPI (maintainers only)
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality. They are automatically installed when you run `make venv`. The hooks include:

- Trailing whitespace removal
- End-of-file fixer
- YAML/TOML syntax checking
- Code formatting (black)
- Import sorting (isort)
- Style guide checking (flake8)
- Type checking (mypy)
- Security checks (bandit)

To manually run all checks:
```bash
make lint
```

### Testing

The project uses pytest for testing and includes:
- Unit tests for all components
- Integration tests based on Dell EMC Unisphere API tutorials
- Coverage reporting
- CI/CD integration with both GitHub Actions and GitLab CI

### CI/CD

The project is configured with:

#### GitHub Actions
- Runs tests on Python 3.12
- Automated testing on pull requests and master branch
- Coverage reporting via Codecov
- Dependency caching for faster builds
- Automated PyPI releases on tags
- Code quality checks using pre-commit

#### GitLab CI
- Parallel CI pipeline configuration
- Built-in coverage reporting
- Caching of pip packages and virtualenv
- Runs on merge requests and master branch
- Code quality checks using pre-commit

## API Documentation

When running locally, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make venv`)
4. Make your changes (hooks will ensure code quality)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
