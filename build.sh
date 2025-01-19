#!/bin/bash

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# If tests pass, build the executable
if [ $? -eq 0 ]; then
    pyinstaller build.spec
    echo "Build completed successfully!"
else
    echo "Tests failed. Build aborted."
    exit 1
fi
