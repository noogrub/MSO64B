#!/usr/bin/env python3
"""
Send one SCPI command or query to a Tektronix MSO64B over Ethernet.

Examples:
    python scripts/mso64b_scpi.py --host 192.168.1.11 --command '*IDN?'
    python scripts/mso64b_scpi.py --host 192.168.1.11 --command 'SYSTEM:ERROR?'
"""

import argparse
import socket
import sys


def send_scpi(hostname, port, command, timeout_seconds):
    if not command.endswith("\n"):
        command = command + "\n"

    with socket.create_connection((hostname, port), timeout=timeout_seconds) as connection:
        connection.settimeout(timeout_seconds)
        connection.sendall(command.encode("ascii"))

        if "?" not in command:
            return ""

        response = connection.recv(4096)
        return response.decode("utf-8", errors="replace").strip()


def build_argument_parser():
    parser = argparse.ArgumentParser(description="Send one SCPI command to the MSO64B.")
    parser.add_argument("--host", required=True, help="MSO64B hostname or IP address.")
    parser.add_argument("--command", required=True, help="SCPI command or query to send.")
    parser.add_argument("--port", type=int, default=4000, help="TCP port. Default: 4000.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Socket timeout. Default: 5.0 seconds.")
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        response = send_scpi(args.host, args.port, args.command, args.timeout)
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if response:
        print(response)

    return 0


if __name__ == "__main__":
    sys.exit(main())
