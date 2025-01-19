# Contributing to PBK to Mobileconfig Converter

We love your input! We want to make contributing to PBK to Mobileconfig Converter as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/chuikoffru/pbk2mobileconfig.git
cd pbk2mobileconfig
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests
```bash
pytest
```

## Code Style
We use black for code formatting and flake8 for linting:
```bash
black .
flake8
```

## Project Structure

```
pbk2mobileconfig/
├── src/
│   └── pbk2mobileconfig/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       ├── converter.py    # Main conversion logic
│       └── parser.py       # PBK file parser
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   └── test_parser.py
├── docs/
├── README.md
└── setup.py
```

## Adding New VPN Types

1. Update the parser in `parser.py` to handle the new VPN type
2. Add conversion logic in `converter.py`
3. Add tests in `tests/`
4. Update documentation

## License
By contributing, you agree that your contributions will be licensed under its MIT License.

## References

- [Apple Configuration Profile Reference](https://developer.apple.com/business/documentation/Configuration-Profile-Reference.pdf)
- [Windows RAS API Documentation](https://docs.microsoft.com/en-us/windows/win32/rras/remote-access-service-functions)
