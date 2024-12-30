# Social validator

![CI](https://github.com/flacy/social-validator/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Flacy/social-validator/graph/badge.svg?token=IX9AMG6L9F)](https://codecov.io/gh/Flacy/social-validator)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/social-validator)
![License](https://img.shields.io/github/license/flacy/social-validator)

### ❓ What's this
This is a library for validating data from social networks and messengers,
such as identifiers, usernames, etc.

### ⚡ Motivation
The motivation behind creating this library stemmed from the lack of a
centralized database containing restrictions for each service.
Often, validating data correctly requires thoroughly analyzing documentation
or manually testing validation.
This library aims to solve this problem but is currently available only for Python.

### 💽 Installation
You can use [pip](https://github.com/pypa/pip) or
[fext](https://github.com/fextpkg/cli) to install the library:
```shell
fext install social-validator
```

### ✨ Usage
The interface for validating the values of **each service** looks like this:
```python
from social_validator import telegram

# Functions starting with "is" are used for boolean value checking.
telegram.is_valid_id("test_user_id")  # True

# Functions starting with "validate" perform full-fledged validation,
# formatting and raising "social_validator.exceptions.ValidationError" if the
# validation fails.
telegram.validate_id("test_user_ID")  # "test_user_id"

# Note: Each validation function is based on a corresponding boolean check
# function, but not vice versa.
telegram.validate_command("cmd") and telegram.is_valid_command("cmd")
```
Documentation for each method is available via docstrings.
If you really need documentation as a separate page, please open issue.

### ⚠️ Roadmap
The project is under development and is moving to a stable version.
To track the status, you can [follow the link](https://github.com/users/Flacy/projects/1).

### 🛠️ Contributing
If you want to contribute to development, request a feature, or report a bug,
please open an [issue](https://github.com/Flacy/social-validator/issues)
with the appropriate label.