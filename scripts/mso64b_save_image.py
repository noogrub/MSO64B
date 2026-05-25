
#!/usr/bin/env python3
"""
Save a Tektronix MSO64B screen image using PyVISA.

The script creates a unique scope-side PNG filename by default:

    C:/YYYYMMDD-HHMMSS_mso64b_<label>.png

It uses the documented SCPI method:

    SAVE:IMAGE "<scope-side path>"
    *OPC?

The image is saved on the oscilloscope filesystem. Use
scripts/mso64b_retrieve_file.py to list or retrieve saved files.
"""

import argparse
import datetime
import re
import sys

import pyvisa


DEFAULT_RESOURCE = "TCPIP::192.168.1.11::INSTR"
DEFAULT_SCOPE_DIR = "C:/"
DEFAULT_LABEL = "screen"


def sanitize_label(label):
    cleaned_label = re.sub(r"[^A-Za-z0-9_.-]+", "-", label.strip())
    cleaned_label = cleaned_label.strip("-._")
    if not cleaned_label:
        return DEFAULT_LABEL
    return cleaned_label


def build_scope_path(scope_dir, label):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_label = sanitize_label(label)

    normalized_scope_dir = scope_dir.replace("\\", "/")
    if not normalized_scope_dir.endswith("/"):
        normalized_scope_dir = normalized_scope_dir + "/"

    filename = f"{timestamp}_mso64b_{safe_label}.png"
    return normalized_scope_dir + filename


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
        default=10000,
        help="VISA timeout in milliseconds. Default: 10000"
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.scope_path:
        scope_path = args.scope_path.replace("\\", "/")
    else:
        scope_path = build_scope_path(args.scope_dir, args.label)

    resource_manager = pyvisa.ResourceManager("@py")
    scope = resource_manager.open_resource(args.resource)
    scope.timeout = args.timeout_ms

    identity = scope.query("*IDN?").strip()
    print(f"Connected to: {identity}")

    command = f'SAVE:IMAGE "{scope_path}"'
    print(f"Sending: {command}")
    scope.write(command)

    operation_complete = scope.query("*OPC?").strip()
    print(f"*OPC? response: {operation_complete}")

    if operation_complete != "1":
        print("ERROR: SAVE:IMAGE did not report completion.", file=sys.stderr)
        return 1

    print(f"Saved screen image on scope: {scope_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
