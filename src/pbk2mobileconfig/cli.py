"""
Command-line interface for pbk2mobileconfig converter.
"""

import argparse
import sys
import plistlib
from typing import Optional
from .parser import PBKParser
from .converter import VPNProfileConverter


def main(args: Optional[list] = None) -> int:
    """Main entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        description="Convert Windows VPN profiles (.pbk) to Apple configuration profiles (.mobileconfig)"
    )
    parser.add_argument("input", help="Input .pbk file path")
    parser.add_argument("output", help="Output .mobileconfig file path")
    parser.add_argument(
        "--org", help="Organization name for the profile", default="Organization"
    )
    parser.add_argument(
        "--identifier",
        help="Profile identifier (e.g., com.example.vpn)",
        default="com.example.vpn",
    )
    parser.add_argument(
        "--removable",
        help="Allow profile to be removed",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--description", help="Profile description", default="VPN Configuration"
    )

    args = parser.parse_args(args)

    try:
        # Parse PBK file
        pbk_parser = PBKParser(args.input)
        vpn_configs = pbk_parser.parse()

        if not vpn_configs:
            print("No VPN configurations found in the input file.")
            return 1

        # Convert configurations
        converter = VPNProfileConverter(
            organization=args.org, identifier=args.identifier, removable=args.removable
        )
        mobileconfig = converter.generate_mobileconfig(vpn_configs)

        # Save mobileconfig file
        with open(args.output, "wb") as f:
            plistlib.dump(mobileconfig, f)

        print(f"Successfully converted {len(vpn_configs)} VPN configuration(s).")
        print(f"Output saved to: {args.output}")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
