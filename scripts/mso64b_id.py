#!/usr/bin/env python3
"""
Query a Tektronix MSO64B oscilloscope identity over Ethernet.

This script sends the SCPI command *IDN? and prints the response.

Example:
    python scripts/mso64b_id.py --host 192.168.1.50

The default TCP port for raw socket SCPI on many Tektronix instruments is 4000.
"""

import argparse
import socket
import sys


def query_scope_identity(hostname, port, timeout_seconds):
    """Return the oscilloscope response to the SCPI *IDN? command."""
    command = b"*IDN?\n"

    with socket.create_connection((hostname, port), timeout=timeout_seconds) as connection:
        connection.settimeout(timeout_seconds)
        connection.sendall(command)
        response = connection.recv(4096)

    return response.decode("utf-8", errors="replace").strip()


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Query a Tektronix MSO64B identity string over Ethernet."
    )
    parser.add_argument(
        "--host",
        required=True,
        help="MSO64B hostname or IP address."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=4000,
        help="TCP port for raw socket SCPI. Default: 4000."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Socket timeout in seconds. Default: 5.0."
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        identity = query_scope_identity(args.host, args.port, args.timeout)
    except socket.timeout:
        print("ERROR: Timed out waiting for the MSO64B response.", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"ERROR: Could not communicate with the MSO64B: {error}", file=sys.stderr)
        return 1

    print(identity)
    return 0


if __name__ == "__main__":
    sys.exit(main())
