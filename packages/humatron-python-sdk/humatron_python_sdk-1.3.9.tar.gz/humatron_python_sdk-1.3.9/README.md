# Humatron Python SDK Library

## Content

This project provides a Python SDK library designed for Humatron developers. The library includes:

- Worker developers section
- REST channel client developers section

### Worker developers section

- Request and Response Classes: Python classes for handling API interactions efficiently.
- Abstract Helper Classes: Simplify asynchronous logic processing.
- REST Utility Methods: Offer helpful functions for working with REST APIs.

### REST channel client developers section

- REST channel client synchronous and asynchronous implementations.

## Installation

```bash
pip install humatron-python-sdk
```

Depends on API section usage following libraries must be installed:

### Worker developers section

- `locked-dict`, version >= `2023.10.22`, mandatory.
    - `pip install locked-dict`.
- `flask`, version >= `3.0.3`, optional.
    - `pip install flask`.

### REST client developers section

- `requests`, version >= `2.32.3`, mandatory.
    - `pip install requests`.

## Usage

- Examples: Visit the examples section on the [Humatron website](https://humatron.ai) for practical use cases and
  demonstrations.
- Test Sections: Review the test sections in the documentation to understand how to implement and use the library's
  features.

## Library Release

- `rm -rf dist/*`
- `pip list --format=freeze > requirements.txt`
- `python setup.py sdist bdist_wheel`
- `twine upload --repository testpypi dist/*` or `twine upload --repository pypi dist/*`

## Documentation generation

- `./make-doc.sh <version>`

  Example: `./make-doc.sh 1.2.0`

<br />
<img src="https://humatron.ai/images/logo_64x64.png" alt="Humatron Logo">