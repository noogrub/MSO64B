#!/usr/bin/env python3
"""
One-step PyVISA test for saving an MSO64B screen image on the scope.

This script uses pyvisa-py with the VISA resource discovered on the CREATE bench:
    TCPIP::192.168.1.11::INSTR

It does not read the image back to the computer. It only tests whether the scope
accepts SAVE:IMAGE and completes the operation.
"""

import argparse
import sys

import pyvisa


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Use PyVISA to ask the MSO64B to save a screen image on the scope."
    )
    parser.add_argument(
        "--resource",
        default="TCPIP::192.168.1.11::INSTR",
        help="VISA resource string. Default: TCPIP::192.168.1.11::INSTR"
    )
    parser.add_argument(
        "--scope-path",
        default="C:/CREATE_test.png",
        help="Scope-side image path. Default: C:/CREATE_test.png"
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

    print("SAVE:IMAGE completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
