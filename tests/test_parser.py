"""
Tests for the PBK parser module.
"""
import os
import pytest
from pbk2mobileconfig.parser import PBKParser


def test_parse_basic_pbk(tmp_path):
    """Test parsing a basic PBK file."""
    # Create a test PBK file
    pbk_content = """[Test VPN]
Type=4
PhoneNumber=vpn.example.com
UserName=testuser
IpDnsAddress=8.8.8.8
IpDns2Address=8.8.4.4
IpDnsSuffix=example.com
"""
    pbk_file = tmp_path / "test.pbk"
    pbk_file.write_text(pbk_content)

    # Parse the file
    parser = PBKParser(str(pbk_file))
    configs = parser.parse()

    # Verify the results
    assert len(configs) == 1
    config = configs[0]
    assert config["Name"] == "Test VPN"
    assert config["Type"] == "4"
    assert config["PhoneNumber"] == "vpn.example.com"
    assert config["IpDnsAddress"] == "8.8.8.8"
    assert config["IpDns2Address"] == "8.8.4.4"
    assert config["IpDnsSuffix"] == "example.com"


def test_parse_nonexistent_file():
    """Test parsing a non-existent file."""
    with pytest.raises(FileNotFoundError):
        parser = PBKParser("nonexistent.pbk")
        parser.parse()


def test_parse_empty_file(tmp_path):
    """Test parsing an empty file."""
    # Create an empty file
    pbk_file = tmp_path / "empty.pbk"
    pbk_file.write_text("")

    parser = PBKParser(str(pbk_file))
    configs = parser.parse()
    assert len(configs) == 0


def test_get_vpn_type_name():
    """Test VPN type name mapping."""
    parser = PBKParser("dummy.pbk")
    assert parser.get_vpn_type_name("4") == "L2TP"
    assert parser.get_vpn_type_name("2") == "PPTP"
    assert parser.get_vpn_type_name("10") == "IKEv2"
    assert parser.get_vpn_type_name("999") == "Unknown"
