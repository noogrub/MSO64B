#!/usr/bin/env python3
"""Save a Tektronix MSO64B screen image using PyVISA."""

import argparse
import sys

from mso64b.config import (
    DEFAULT_LABEL,
    DEFAULT_RESOURCE,
    DEFAULT_SCOPE_DIR,
    DEFAULT_TIMEOUT_MS,
)
from mso64b.instrument import open_scope, query_identity, save_image
from mso64b.naming import build_scope_image_path, normalize_scope_path


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Save an MSO64B screen image on the scope filesystem."
    )
    parser.add_argument(
        "--resource",
        default=DEFAULT_RESOURCE,
        help=f"VISA resource string. Default: {DEFAULT_RESOURCE}"
    )
    parser.add_argument(
        "--scope-dir",
        default=DEFAULT_SCOPE_DIR,
        help=f"Scope-side output directory. Default: {DEFAULT_SCOPE_DIR}"
    )
    parser.add_argument(
        "--scope-path",
        default=None,
        help="Exact scope-side output path. Overrides --scope-dir and --label."
    )
    parser.add_argument(
        "--label",
        default=DEFAULT_LABEL,
        help=f"Label used for generated filenames. Default: {DEFAULT_LABEL}"
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

    if args.scope_path:
        scope_path = normalize_scope_path(args.scope_path)
    else:
        scope_path = build_scope_image_path(args.scope_dir, args.label)

    try:
        scope = open_scope(args.resource, args.timeout_ms)
        identity = query_identity(scope)
        print(f"Connected to: {identity}")

        command = f'SAVE:IMAGE "{scope_path}"'
        print(f"Sending: {command}")

        saved_scope_path = save_image(scope, scope_path)
        print("*OPC? response: 1")
        print(f"Saved screen image on scope: {saved_scope_path}")

    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
