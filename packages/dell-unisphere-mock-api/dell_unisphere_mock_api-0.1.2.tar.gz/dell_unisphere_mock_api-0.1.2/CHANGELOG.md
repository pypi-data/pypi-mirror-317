# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2024-12-23

### Added
- User management endpoints:
  - GET /api/types/user/instances for listing users
  - GET /api/instances/user/{user_id} for specific user details
- Comprehensive test suite for user endpoints
- Response format matching Dell Unisphere API specification

## [0.1.0] - 2024-12-23

### Added
- Initial project structure with FastAPI framework
- Basic authentication system with CSRF token support
- Storage resource management endpoints:
  - Pool listing with pagination and sorting
  - LUN operations (create, read, update, delete)
  - Filesystem operations
  - NAS server management
  - Disk and disk group handling
- Comprehensive test suite with pytest
- CI/CD setup:
  - GitHub Actions workflow
  - GitLab CI pipeline
  - Codecov integration
- Code quality tools:
  - Pre-commit hooks configuration
  - Black code formatting
  - isort import sorting
  - Flake8 style checking
  - MyPy type checking
  - Bandit security scanning
- API documentation:
  - Swagger UI integration
  - ReDoc support
- Project documentation:
  - README with setup and usage instructions
  - Contributing guidelines
  - License information

[0.1.0]: https://github.com/nirabo/dell-unisphere-mock-api/releases/tag/v0.1.0
