from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pbk2mobileconfig",
    version="0.1.0",
    author="OpenHands",
    author_email="openhands@all-hands.dev",
    description="Convert Windows VPN profiles to Apple configuration profiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pbk2mobileconfig",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/pbk2mobileconfig/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "chardet>=5.0.0",
        "plistlib",
        "configparser",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.9",
            "pyinstaller>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pbk2mobileconfig=pbk2mobileconfig.cli:main",
        ],
    },
)
