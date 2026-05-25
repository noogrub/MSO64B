#!/usr/bin/env python3
"""List or retrieve files from the Tektronix MSO64B using PyVISA."""

import argparse
import sys

from mso64b.config import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_RESOURCE,
    DEFAULT_SCOPE_DIR,
    DEFAULT_TIMEOUT_MS,
)
from mso64b.instrument import (
    build_local_output_path,
    list_files,
    open_scope,
    query_identity,
    retrieve_file,
    save_listing_files,
    write_bytes,
)
from mso64b.naming import normalize_scope_path, timestamp_string


def print_directory_entries(entries):
    if not entries:
        print("No files returned.")
        return

    for entry in entries:
        print(entry)


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
        default=DEFAULT_TIMEOUT_MS,
        help=f"VISA timeout in milliseconds. Default: {DEFAULT_TIMEOUT_MS}"
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        scope = open_scope(args.resource, args.timeout_ms)
        identity = query_identity(scope)
        print(f"Connected to: {identity}")

        if args.list:
            scope_dir = normalize_scope_path(args.scope_dir)
            print(f"Listing scope directory: {scope_dir}")

            entries = list_files(scope, scope_dir)
            print_directory_entries(entries)

            if args.save_list:
                text_path, json_path = save_listing_files(
                    args.output_dir,
                    args.resource,
                    scope_dir,
                    entries,
                    timestamp_string(),
                )
                print(f"Saved text listing: {text_path}")
                print(f"Saved JSON listing: {json_path}")

            return 0

        if not args.scope_path:
            print("ERROR: --scope-path is required unless --list is used.", file=sys.stderr)
            return 1

        scope_path = normalize_scope_path(args.scope_path)
        local_output_path = build_local_output_path(
            scope_path,
            args.output_dir,
            args.output,
        )

        command = f'FILESystem:READFile "{scope_path}"'
        print(f"Sending: {command}")

        file_bytes = retrieve_file(scope, scope_path)
        write_bytes(local_output_path, file_bytes)

        print(f"Retrieved {len(file_bytes)} bytes")
        print(f"Saved local file: {local_output_path}")

    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
