"""
Parser module for reading and parsing Windows PBK files.
"""

import os
import configparser
from typing import Dict, Any, List
import chardet


class PBKParser:
    """Parser for Windows PBK (Phone Book) files."""

    def __init__(self, pbk_path: str):
        """Initialize parser with PBK file path."""
        self.pbk_path = pbk_path
        self.config = configparser.ConfigParser(strict=False)
        self.raw_content = ""
        self._additional_files = {}

    def read_file_safely(self, file_path: str) -> str:
        """Read file content with automatic encoding detection."""
        # Try UTF-8 first (most common)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            pass

        # Try common encodings
        encodings = [
            "latin-1",
            "cp1252",
            "iso-8859-1",
            "ascii",
            "utf-16-le",
            "utf-16-be",
        ]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue

        # Fallback to reading as binary and attempt to detect encoding
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
            detected = chardet.detect(raw_data)
            encoding = detected["encoding"]
            if encoding:
                return raw_data.decode(encoding)
        except Exception as e:
            raise ValueError(f"Error detecting encoding: {e}")

        raise ValueError(f"Could not read file {file_path} with any supported encoding")

    def _load_additional_files(self) -> None:
        """Load additional configuration files from the same directory."""
        base_dir = os.path.dirname(self.pbk_path)
        base_name = os.path.splitext(os.path.basename(self.pbk_path))[0]

        additional_extensions = [".cmp", ".cms", ".inf"]
        for ext in additional_extensions:
            path = os.path.join(base_dir, f"{base_name}{ext}")
            if os.path.exists(path):
                try:
                    content = self.read_file_safely(path)
                    self._additional_files[ext] = content
                except Exception:
                    pass

    def parse(self) -> List[Dict[str, Any]]:
        """Parse PBK file and return list of VPN configurations."""
        if not os.path.isfile(self.pbk_path):
            raise FileNotFoundError(f"File not found: {self.pbk_path}")

        # Read main PBK file
        self.raw_content = self.read_file_safely(self.pbk_path)

        # Load additional files
        self._load_additional_files()

        # Parse configuration
        if not self.raw_content.startswith("["):
            self.raw_content = "[DEFAULT]\n" + self.raw_content
        self.config.read_string(self.raw_content)

        vpn_configs = []

        # Extract phone number from the DEVICE section if present
        phone_number = ""
        for line in self.raw_content.splitlines():
            if line.startswith("PhoneNumber="):
                phone_number = line.split("=", 1)[1].strip()

        for section in self.config.sections():
            vpn_type = self.config.get(section, "Type", fallback="").strip()

            # Skip non-VPN sections
            if not vpn_type:
                continue

            # Create base VPN configuration
            vpn_config = {
                "Name": section,
                "Type": vpn_type,
                "PhoneNumber": phone_number,
                # Basic settings
                "UserName": self.config.get(section, "UserName", fallback="").strip(),
                "Password": self.config.get(section, "Password", fallback="").strip(),
                "SharedSecret": self.config.get(
                    section, "PreSharedKey", fallback=""
                ).strip(),
                # DNS settings
                "IpDnsAddress": self.config.get(
                    section, "IpDnsAddress", fallback=""
                ).strip(),
                "IpDns2Address": self.config.get(
                    section, "IpDns2Address", fallback=""
                ).strip(),
                "IpDnsSuffix": self.config.get(
                    section, "IpDnsSuffix", fallback=""
                ).strip(),
                # Device settings
                "Device": self.config.get(
                    section, "PreferredDevice", fallback=""
                ).strip(),
                # Authentication settings
                "UseExtendedAuth": self.config.get(
                    section, "UseExtendedAuthentication", fallback="1"
                ).strip(),
                "AuthRestrictions": self.config.get(
                    section, "AuthRestrictions", fallback=""
                ).strip(),
                # Encryption settings
                "DataEncryption": self.config.get(
                    section, "DataEncryption", fallback=""
                ).strip(),
                "EncryptionType": self.config.get(
                    section, "EncryptionType", fallback=""
                ).strip(),
                # Additional settings from CMS file if available
                "AdditionalSettings": self._parse_additional_settings(section),
            }

            # Add any section-specific settings
            for key, value in self.config.items(section):
                if key.lower() not in [k.lower() for k in vpn_config.keys()]:
                    vpn_config[key] = value.strip()

            vpn_configs.append(vpn_config)

        return vpn_configs

    def _parse_additional_settings(self, section: str) -> Dict[str, Any]:
        """Parse additional settings from CMS and other files."""
        settings = {}

        # Parse CMS file if available
        if ".cms" in self._additional_files:
            cms_config = configparser.ConfigParser(strict=False)
            try:
                cms_config.read_string(self._additional_files[".cms"])
                if cms_config.has_section(section):
                    settings.update(dict(cms_config.items(section)))
            except configparser.Error:
                pass

        return settings

    def get_vpn_type_name(self, type_id: str) -> str:
        """Convert numeric VPN type to string name."""
        vpn_types = {
            "1": "PPTP",
            "2": "PPTP",
            "4": "L2TP",
            "8": "L2TP",
            "10": "IKEv2",
        }
        return vpn_types.get(type_id, "Unknown")
