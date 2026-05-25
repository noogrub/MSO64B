#!/usr/bin/env python3
"""
Capture a Tektronix MSO64B screenshot over Ethernet.

This script asks the oscilloscope to save a PNG image on its local file system,
then reads that file back over the SCPI socket connection.

Example:
    python scripts/mso64b_screenshot.py --host 192.168.1.11 --output screenshots/probe_comp_ch2.png

The default TCP port for raw socket SCPI on many Tektronix instruments is 4000.
"""

import argparse
import os
import socket
import sys
import time


DEFAULT_SCOPE_IMAGE_PATH = "C:/CREATE_test.png"
PNG_SIGNATURE = bytes([137, 80, 78, 71, 13, 10, 26, 10])


def send_command(connection, command):
    if not command.endswith("\n"):
        command = command + "\n"
    connection.sendall(command.encode("ascii"))


def query_text(connection, command, timeout_seconds):
    send_command(connection, command)
    connection.settimeout(timeout_seconds)
    response = connection.recv(65536)
    return response.decode("utf-8", errors="replace").strip()


def read_until_timeout(connection, timeout_seconds):
    connection.settimeout(timeout_seconds)
    chunks = []

    while True:
        try:
            chunk = connection.recv(65536)
        except socket.timeout:
            break

        if not chunk:
            break

        chunks.append(chunk)

    return b"".join(chunks)


def strip_possible_scpi_block_header(data):
    """Remove a SCPI definite-length block header if the instrument sends one."""
    if len(data) < 2:
        return data

    if data[0:1] != b"#":
        return data

    digit_count_character = data[1:2]
    if not digit_count_character.isdigit():
        return data

    digit_count = int(digit_count_character.decode("ascii"))
    header_length = 2 + digit_count

    if len(data) < header_length:
        return data

    length_text = data[2:header_length].decode("ascii", errors="replace")
    if not length_text.isdigit():
        return data

    payload_length = int(length_text)
    payload_start = header_length
    payload_end = payload_start + payload_length

    if len(data) < payload_end:
        return data[payload_start:]

    return data[payload_start:payload_end]


def trim_to_png_payload(data):
    """Trim leading non-PNG bytes if the scope prepends text or status data."""
    png_start = data.find(PNG_SIGNATURE)
    if png_start < 0:
        return data
    return data[png_start:]


def capture_screenshot(hostname, port, output_path, scope_image_path, timeout_seconds, debug_enabled):
    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with socket.create_connection((hostname, port), timeout=timeout_seconds) as connection:
        connection.settimeout(timeout_seconds)

        identity = query_text(connection, "*IDN?", timeout_seconds)
        print(f"Connected to: {identity}")

        print(f"Saving image on scope as: {scope_image_path}")
        send_command(connection, f'SAVE:IMAGE "{scope_image_path}"')
        operation_complete = query_text(connection, "*OPC?", timeout_seconds)
        print(f"*OPC? response after SAVE:IMAGE: {operation_complete}")

        time.sleep(0.5)

        directory_listing = query_text(connection, "FILESystem:DIR?", timeout_seconds)
        if os.path.basename(scope_image_path) in directory_listing:
            print("Scope-side file is visible in FILESystem:DIR?.")
        else:
            print("WARNING: Scope-side file was not found in FILESystem:DIR?.", file=sys.stderr)

        print(f"Reading scope-side file: {scope_image_path}")
        send_command(connection, f'FILESystem:READFile "{scope_image_path}"')
        raw_data = read_until_timeout(connection, timeout_seconds)

    if debug_enabled:
        print(f"Raw bytes received after READFile: {len(raw_data)}")
        if raw_data:
            preview = raw_data[:32]
            print(f"First raw bytes: {preview!r}")

    image_data = strip_possible_scpi_block_header(raw_data)
    image_data = trim_to_png_payload(image_data)

    if debug_enabled:
        print(f"Bytes after header/PNG trimming: {len(image_data)}")
        if image_data:
            print(f"First trimmed bytes: {image_data[:32]!r}")

    if not image_data:
        raise RuntimeError("No image data was received from the oscilloscope.")

    if not image_data.startswith(PNG_SIGNATURE):
        raise RuntimeError("Received data does not start with a PNG signature.")

    with open(output_path, "wb") as output_file:
        output_file.write(image_data)

    return len(image_data)


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Capture a Tektronix MSO64B screen image over Ethernet."
    )
    parser.add_argument(
        "--host",
        required=True,
        help="MSO64B hostname or IP address."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Local PNG output path."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=4000,
        help="TCP port for raw socket SCPI. Default: 4000."
    )
    parser.add_argument(
        "--scope-path",
        default=DEFAULT_SCOPE_IMAGE_PATH,
        help=f"Temporary image path on the oscilloscope. Default: {DEFAULT_SCOPE_IMAGE_PATH}"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Socket timeout in seconds. Default: 10.0."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print byte counts and byte previews while debugging readback."
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        byte_count = capture_screenshot(
            args.host,
            args.port,
            args.output,
            args.scope_path,
            args.timeout,
            args.debug,
        )
    except (OSError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Saved {byte_count} bytes to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
