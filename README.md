# PBK to Mobileconfig Converter

A tool for converting Windows VPN connection profiles (`.pbk` files) to Apple configuration profiles (`.mobileconfig`).

## Features

- Converts Windows RAS VPN profiles to Apple configuration profiles
- Supports L2TP/IPSec, PPTP, and IKEv2 VPN types
- Preserves DNS settings, routes, and other connection properties
- Handles various text encodings in PBK files
- Command-line interface for easy integration
- Cross-platform support (Windows, macOS, Linux)

## Installation

### Using pip

```bash
pip install pbk2mobileconfig
```

### Using executable (Windows)

Download the latest release from the [releases page](https://github.com/chuikoffru/pbk2mobileconfig/releases).

## Usage

### Command Line

Basic usage:
```bash
pbk2mobileconfig input.pbk output.mobileconfig
```

Advanced options:
```bash
pbk2mobileconfig input.pbk output.mobileconfig --org "Your Organization" --identifier "com.example.vpn"
```

### Python API

```python
from pbk2mobileconfig import convert_pbk_to_mobileconfig

# Convert a single file
convert_pbk_to_mobileconfig("input.pbk", "output.mobileconfig")

# Convert with custom options
convert_pbk_to_mobileconfig(
    "input.pbk",
    "output.mobileconfig",
    organization="Your Organization",
    identifier="com.example.vpn"
)
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--org` | Organization name | "Organization" |
| `--identifier` | Profile identifier | "com.example.vpn" |
| `--removable` | Allow profile removal | True |
| `--description` | Profile description | "VPN Configuration" |

## Supported VPN Types

- L2TP/IPSec
- PPTP (legacy)
- IKEv2

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by the need to migrate VPN configurations between platforms
