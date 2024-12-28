# Test Common Utils

A collection of common utilities including a configurable logger with type hints and Pydantic integration.

## Installation

You can install this package directly from GitHub using pip:

```bash
pip install git+https://github.com/YOUR_USERNAME/test-common-utils.git
```

Or add it to your project's requirements.txt:

```
git+https://github.com/YOUR_USERNAME/test-common-utils.git
```

To install a specific version:

```bash
pip install git+https://github.com/YOUR_USERNAME/test-common-utils.git@v0.1.2
```

## Usage

### Logger

```python
from test_common_utils.utils import create_logger

# Basic usage
logger = create_logger(name="my_app")
logger.info("Hello, world!")

# Custom configuration
logger = create_logger(
    name="my_app",
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/test-common-utils.git
cd test-common-utils

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy src tests
```

### Version Management

To bump the version:

```bash
# Bump patch version (0.1.0 -> 0.1.1)
./scripts/bump_version.py patch

# Bump minor version (0.1.0 -> 0.2.0)
./scripts/bump_version.py minor

# Bump major version (0.1.0 -> 1.0.0)
./scripts/bump_version.py major
```

### CI/CD

The project uses GitHub Actions for:
- Running tests on Python 3.8, 3.9, 3.10, and 3.11
- Code quality checks (black, ruff, mypy)
- Automatic publishing to PyPI when a version tag is pushed

To release a new version:
1. Bump the version using the script
2. Push the changes and tags
3. The CI/CD pipeline will automatically publish to PyPI 