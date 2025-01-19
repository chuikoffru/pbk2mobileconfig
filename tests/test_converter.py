"""
Tests for the VPN profile converter module.
"""
import uuid
import pytest
from pbk2mobileconfig.converter import VPNProfileConverter


def test_convert_l2tp_config():
    """Test converting L2TP VPN configuration."""
    converter = VPNProfileConverter(
        organization="Test Org",
        identifier="com.test.vpn"
    )

    vpn_config = {
        "Name": "Test VPN",
        "Type": "4",
        "PhoneNumber": "vpn.example.com",
        "UserName": "testuser",
        "IpDnsAddress": "8.8.8.8",
        "IpDns2Address": "8.8.4.4",
        "IpDnsSuffix": "example.com",
    }

    result = converter.convert_vpn_config(vpn_config)

    assert result["PayloadType"] == "com.apple.vpn.managed"
    assert result["VPNType"] == "L2TP"
    assert result["VPN"]["RemoteAddress"] == "vpn.example.com"
    assert result["DNS"]["ServerAddresses"] == ["8.8.8.8", "8.8.4.4"]
    assert result["DNS"]["SearchDomains"] == ["example.com"]


def test_generate_mobileconfig():
    """Test generating complete mobileconfig profile."""
    converter = VPNProfileConverter(
        organization="Test Org",
        identifier="com.test.vpn",
        removable=True
    )

    vpn_configs = [{
        "Name": "Test VPN",
        "Type": "4",
        "PhoneNumber": "vpn.example.com",
    }]

    result = converter.generate_mobileconfig(vpn_configs)

    assert result["PayloadType"] == "Configuration"
    assert result["PayloadIdentifier"] == "com.test.vpn"
    assert result["PayloadOrganization"] == "Test Org"
    assert result["PayloadRemovalDisallowed"] is False
    assert len(result["PayloadContent"]) == 1


def test_vpn_type_mapping():
    """Test VPN type mapping."""
    converter = VPNProfileConverter()
    
    assert converter._get_vpn_type("4") == "L2TP"
    assert converter._get_vpn_type("2") == "PPTP"
    assert converter._get_vpn_type("10") == "IKEv2"
    assert converter._get_vpn_type("999") == "L2TP"  # Default type


def test_empty_config_list():
    """Test generating mobileconfig with empty config list."""
    converter = VPNProfileConverter()
    result = converter.generate_mobileconfig([])
    assert len(result["PayloadContent"]) == 0
