"""
Converter module for transforming Windows VPN configurations to Apple mobileconfig format.
"""

import uuid
from typing import Dict, Any, List


class VPNProfileConverter:
    """Converts Windows VPN configurations to Apple mobileconfig format."""

    def __init__(
        self,
        organization: str = "Organization",
        identifier: str = "com.example.vpn",
        removable: bool = True,
    ):
        """Initialize converter with basic profile settings."""
        self.organization = organization
        self.identifier = identifier
        self.removable = removable

    def convert_vpn_config(self, vpn_config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single VPN configuration to mobileconfig format."""
        vpn_type = self._get_vpn_type(vpn_config["Type"])
        payload_uuid = str(uuid.uuid4())

        # Base payload structure
        payload = {
            "PayloadType": "com.apple.vpn.managed",
            "PayloadVersion": 1,
            "PayloadIdentifier": f"{self.identifier}.{vpn_config['Name']}.{payload_uuid}",
            "PayloadUUID": payload_uuid,
            "PayloadDisplayName": vpn_config["Name"],
            "PayloadDescription": "Configures VPN settings",
            "PayloadOrganization": self.organization,
            "VPNType": vpn_type,
            "PayloadEnabled": True,
        }

        # Add type-specific configuration
        if vpn_type == "L2TP":
            self._add_l2tp_config(payload, vpn_config)
        elif vpn_type == "PPTP":
            self._add_pptp_config(payload, vpn_config)
        elif vpn_type == "IKEv2":
            self._add_ikev2_config(payload, vpn_config)

        # Add common settings
        self._add_common_settings(payload, vpn_config)

        return payload

    def generate_mobileconfig(
        self, vpn_configs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate complete mobileconfig profile from VPN configurations."""
        payload_content = [self.convert_vpn_config(config) for config in vpn_configs]
        root_uuid = str(uuid.uuid4())

        return {
            "PayloadContent": payload_content,
            "PayloadDisplayName": "VPN Configuration",
            "PayloadIdentifier": self.identifier,
            "PayloadRemovalDisallowed": not self.removable,
            "PayloadType": "Configuration",
            "PayloadUUID": root_uuid,
            "PayloadVersion": 1,
            "PayloadDescription": "VPN Configuration Profile",
            "PayloadOrganization": self.organization,
        }

    def _get_vpn_type(self, type_id: str) -> str:
        """Map Windows VPN type to Apple VPN type."""
        vpn_types = {
            "1": "PPTP",
            "2": "PPTP",
            "4": "L2TP",
            "8": "L2TP",
            "10": "IKEv2",
        }
        return vpn_types.get(type_id, "L2TP")

    def _add_l2tp_config(
        self, payload: Dict[str, Any], vpn_config: Dict[str, Any]
    ) -> None:
        """Add L2TP specific configuration."""
        payload.update(
            {
                "VPN": {
                    "RemoteAddress": vpn_config.get("PhoneNumber", ""),
                    "AuthenticationMethod": "Password",
                    "CommRemoteAddress": vpn_config.get("PhoneNumber", ""),
                    "AuthName": "",  # Will be filled by user
                    "AuthPassword": "",  # Will be filled by user
                    "SharedSecret": "",  # Will be filled by user
                    "TokenCard": False,
                    "DisconnectOnIdle": 0,
                    "EnableSplitTunneling": 1,
                    "ProtocolType": "L2TP",
                    "AuthEAPPlugins": [],
                    "AuthProtocol": ["Password"],
                    "UseExtendedAuthentication": int(
                        vpn_config.get("UseExtendedAuth", "1")
                    ),
                    "InterfaceTypeMatch": "Ethernet",
                    "EncryptionLevel": "Auto",
                },
                "IPSec": {
                    "AuthenticationMethod": "SharedSecret",
                    "SharedSecret": "",  # Will be filled by user
                    "LocalIdentifierType": "KeyID",
                    "RemoteAddress": vpn_config.get("PhoneNumber", ""),
                    "XAuthEnabled": 1,
                    "XAuthName": "",  # Will be filled by user
                    "XAuthPassword": "",  # Will be filled by user
                    "PromptForVPNPIN": False,
                },
                "PPP": {
                    "CommRemoteAddress": vpn_config.get("PhoneNumber", ""),
                    "AuthName": "",  # Will be filled by user
                    "AuthPassword": "",  # Will be filled by user
                    "TokenCard": False,
                    "CCPEnabled": 0,
                    "CCPMPPE40Enabled": 0,
                    "CCPMPPE128Enabled": 0,
                    "AuthProtocol": ["PAP", "CHAP", "MSCHAPv2"],
                    "DialMode": "Manual",
                    "IdleDisconnectEnabled": 0,
                    "LCPEchoEnabled": 1,
                    "LCPEchoFailure": 5,
                    "LCPEchoInterval": 30,
                },
            }
        )

    def _add_pptp_config(
        self, payload: Dict[str, Any], vpn_config: Dict[str, Any]
    ) -> None:
        """Add PPTP specific configuration."""
        # Implementation for PPTP
        pass

    def _add_ikev2_config(
        self, payload: Dict[str, Any], vpn_config: Dict[str, Any]
    ) -> None:
        """Add IKEv2 specific configuration."""
        # Implementation for IKEv2
        pass

    def _add_common_settings(
        self, payload: Dict[str, Any], vpn_config: Dict[str, Any]
    ) -> None:
        """Add common VPN settings."""
        # Add DNS settings if available
        dns_addresses = []
        if vpn_config.get("IpDnsAddress"):
            dns_addresses.append(vpn_config["IpDnsAddress"])
        if vpn_config.get("IpDns2Address"):
            dns_addresses.append(vpn_config["IpDns2Address"])

        if dns_addresses:
            payload["DNS"] = {
                "ServerAddresses": dns_addresses,
                "SupplementalMatchDomains": [],
            }

        if vpn_config.get("IpDnsSuffix"):
            if "DNS" not in payload:
                payload["DNS"] = {}
            payload["DNS"]["SearchDomains"] = [vpn_config["IpDnsSuffix"]]
            payload["DNS"]["SupplementalMatchDomains"] = [vpn_config["IpDnsSuffix"]]

        # Add IPv4 settings
        payload["IPv4"] = {
            "OverridePrimary": 1,
            "ConfigMethod": "Manual",
        }

        # Add split tunneling if configured
        payload["EnableSplitTunneling"] = True
