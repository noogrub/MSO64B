
#!/usr/bin/env python3
"""
List or retrieve files from the Tektronix MSO64B using PyVISA.

Listing uses the documented SCPI command:

    FILESystem:DIR?

Retrieval uses the documented SCPI command:

    FILESystem:READFile "<scope-side path>"

Retrieved files and saved listings are written under img/ by default. The img/
directory is ignored by git.
"""

import argparse
import datetime
import json
import os
import sys

import pyvisa


DEFAULT_RESOURCE = "TCPIP::192.168.1.11::INSTR"
DEFAULT_SCOPE_DIR = "C:/"
DEFAULT_OUTPUT_DIR = "img"


def normalize_scope_path(path):
    return path.replace("\\", "/")


def scope_basename(scope_path):
    normalized_path = normalize_scope_path(scope_path)
    return normalized_path.rstrip("/").split("/")[-1]


def build_output_path(scope_path, output_dir, output_path):
    if output_path:
        return output_path

    filename = scope_basename(scope_path)
    if not filename:
        filename = "mso64b_retrieved_file.bin"

    return os.path.join(output_dir, filename)


def parse_directory_listing(raw_listing):
    entries = []

    if not raw_listing:
        return entries

    for item in raw_listing.split(","):
        clean_item = item.strip().strip('"')
        if clean_item:
            entries.append(clean_item)

    return entries


def print_directory_entries(entries):
    if not entries:
        print("No files returned.")
        return

    for entry in entries:
        print(entry)


def timestamp_string():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def build_listing_paths(output_dir):
    timestamp = timestamp_string()
    text_path = os.path.join(output_dir, f"{timestamp}_mso64b_directory_listing.txt")
    json_path = os.path.join(output_dir, f"{timestamp}_mso64b_directory_listing.json")
    return text_path, json_path


def write_listing_files(output_dir, resource_name, scope_dir, entries):
    os.makedirs(output_dir, exist_ok=True)

    text_path, json_path = build_listing_paths(output_dir)

    with open(text_path, "w", encoding="utf-8", newline="\n") as text_file:
        for entry in entries:
            text_file.write(entry + "\n")

    listing_record = {
        "resource": resource_name,
        "scope_dir": scope_dir,
        "files": entries,
    }

    with open(json_path, "w", encoding="utf-8", newline="\n") as json_file:
        json.dump(listing_record, json_file, indent=2)
        json_file.write("\n")

    return text_path, json_path


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="List or retrieve files from the MSO64B filesystem."
    )
    parser.add_argument(
        "--resource",
        default=DEFAULT_RESOURCE,
        help=f"VISA resource string. Default: {DEFAULT_RESOURCE}"
    )
    parser.add_argument(
        "--scope-dir",
        default=DEFAULT_SCOPE_DIR,
        help=f"Scope-side directory for --list. Default: {DEFAULT_SCOPE_DIR}"
    )
    parser.add_argument(
        "--scope-path",
        default=None,
        help="Scope-side file path to retrieve, for example C:/file.png"
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Local output directory. Default: {DEFAULT_OUTPUT_DIR}"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Exact local output path. Overrides --output-dir."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List files in --scope-dir instead of retrieving a file."
    )
    parser.add_argument(
        "--save-list",
        action="store_true",
        help="When used with --list, save the listing as text and JSON under --output-dir."
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

    if args.list:
        scope_dir = normalize_scope_path(args.scope_dir)
        print(f"Listing scope directory: {scope_dir}")
        scope.write(f'FILESystem:CWD "{scope_dir}"')
        raw_listing = scope.query("FILESystem:DIR?").strip()

        entries = parse_directory_listing(raw_listing)
        print_directory_entries(entries)

        if args.save_list:
            text_path, json_path = write_listing_files(
                args.output_dir,
                args.resource,
                scope_dir,
                entries,
            )
            print(f"Saved text listing: {text_path}")
            print(f"Saved JSON listing: {json_path}")

        return 0

    if not args.scope_path:
        print("ERROR: --scope-path is required unless --list is used.", file=sys.stderr)
        return 1

    scope_path = normalize_scope_path(args.scope_path)
    local_output_path = build_output_path(scope_path, args.output_dir, args.output)

    output_directory = os.path.dirname(local_output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    command = f'FILESystem:READFile "{scope_path}"'
    print(f"Sending: {command}")
    scope.write(command)

    file_bytes = scope.read_raw()

    if not file_bytes:
        print("ERROR: No bytes were returned by FILESystem:READFile.", file=sys.stderr)
        return 1

    with open(local_output_path, "wb") as output_file:
        output_file.write(file_bytes)

    print(f"Retrieved {len(file_bytes)} bytes")
    print(f"Saved local file: {local_output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
