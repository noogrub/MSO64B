#!/usr/bin/env python3
"""
Capture a Tektronix MSO64B screen image using PyVISA.

This script follows the documented SCPI method through a VISA resource:

1. Connect to the oscilloscope.
2. Query *IDN?.
3. Save the current screen image on the scope with SAVE:IMAGE.
4. Wait for completion with *OPC?.

The script intentionally leaves the image on the scope filesystem. A later script
can add file readback once that procedure is documented and tested cleanly.
"""

import argparse
import sys

import pyvisa


DEFAULT_RESOURCE = "TCPIP::192.168.1.11::INSTR"
DEFAULT_SCOPE_PATH = "C:/CREATE_test.png"


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Use PyVISA to ask the MSO64B to save a screen image on the scope."
    )
    parser.add_argument(
        "--resource",
        default=DEFAULT_RESOURCE,
        help=f"VISA resource string. Default: {DEFAULT_RESOURCE}"
    )
    parser.add_argument(
        "--scope-path",
        default=DEFAULT_SCOPE_PATH,
        help=f"Scope-side image path. Default: {DEFAULT_SCOPE_PATH}"
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=10000,
        help="VISA timeout in milliseconds. Default: 10000"
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    resource_manager = pyvisa.ResourceManager("@py")
    scope = resource_manager.open_resource(args.resource)
    scope.timeout = args.timeout_ms

    identity = scope.query("*IDN?").strip()
    print(f"Connected to: {identity}")

    command = f'SAVE:IMAGE "{args.scope_path}"'
    print(f"Sending: {command}")
    scope.write(command)

    operation_complete = scope.query("*OPC?").strip()
    print(f"*OPC? response: {operation_complete}")

    if operation_complete != "1":
        print("ERROR: SAVE:IMAGE did not report completion.", file=sys.stderr)
        return 1

    print(f"Saved screen image on scope: {args.scope_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
