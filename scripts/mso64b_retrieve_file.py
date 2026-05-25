#!/usr/bin/env python3
"""
Retrieve a file from the Tektronix MSO64B using PyVISA.

This script follows the documented SCPI file transfer command:

    FILESystem:READFile "<scope-side path>"

The file contents are returned through the VISA interface and written to a local
file. By default, the local file is written under img/, which is ignored by git.
"""

import argparse
import os
import sys

import pyvisa


DEFAULT_RESOURCE = "TCPIP::192.168.1.11::INSTR"
DEFAULT_SCOPE_PATH = "C:/CREATE_test.png"
DEFAULT_OUTPUT_PATH = "img/CREATE_test.png"


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Retrieve a file from the MSO64B filesystem using PyVISA."
    )
    parser.add_argument(
        "--resource",
        default=DEFAULT_RESOURCE,
        help=f"VISA resource string. Default: {DEFAULT_RESOURCE}",
    )
    parser.add_argument(
        "--scope-path",
        default=DEFAULT_SCOPE_PATH,
        help=f"Scope-side file path. Default: {DEFAULT_SCOPE_PATH}",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Local output path. Default: {DEFAULT_OUTPUT_PATH}",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=10000,
        help="VISA timeout in milliseconds. Default: 10000",
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    output_directory = os.path.dirname(args.output)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    resource_manager = pyvisa.ResourceManager("@py")
    scope = resource_manager.open_resource(args.resource)
    scope.timeout = args.timeout_ms

    identity = scope.query("*IDN?").strip()
    print(f"Connected to: {identity}")

    command = f'FILESystem:READFile "{args.scope_path}"'
    print(f"Sending: {command}")
    scope.write(command)

    file_bytes = scope.read_raw()

    if not file_bytes:
        print("ERROR: No bytes were returned by FILESystem:READFile.", file=sys.stderr)
        return 1

    with open(args.output, "wb") as output_file:
        output_file.write(file_bytes)

    print(f"Retrieved {len(file_bytes)} bytes")
    print(f"Saved local file: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
