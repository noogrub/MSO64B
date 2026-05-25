"""PyVISA control functions for the Tektronix MSO64B."""

import json
import os

import pyvisa

from mso64b.config import DEFAULT_RESOURCE, DEFAULT_TIMEOUT_MS
from mso64b.naming import normalize_scope_path, scope_basename


def open_scope(resource=DEFAULT_RESOURCE, timeout_ms=DEFAULT_TIMEOUT_MS):
    """Open the MSO64B through pyvisa-py and return the scope resource."""
    resource_manager = pyvisa.ResourceManager("@py")
    scope = resource_manager.open_resource(resource)
    scope.timeout = timeout_ms
    return scope


def query_identity(scope):
    """Return the instrument identity string."""
    return scope.query("*IDN?").strip()


def save_image(scope, scope_path):
    """Save the current MSO64B screen image to a scope-side path."""
    normalized_scope_path = normalize_scope_path(scope_path)
    command = f'SAVE:IMAGE "{normalized_scope_path}"'
    scope.write(command)

    operation_complete = scope.query("*OPC?").strip()
    if operation_complete != "1":
        raise RuntimeError(f"SAVE:IMAGE did not report completion: {operation_complete}")

    return normalized_scope_path


def parse_directory_listing(raw_listing):
    """Parse the comma-separated directory listing returned by FILESystem:DIR?."""
    entries = []

    if not raw_listing:
        return entries

    for item in raw_listing.split(","):
        clean_item = item.strip().strip('"')
        if clean_item:
            entries.append(clean_item)

    return entries


def list_files(scope, scope_dir):
    """Return file/directory names from a scope-side directory."""
    normalized_scope_dir = normalize_scope_path(scope_dir)
    scope.write(f'FILESystem:CWD "{normalized_scope_dir}"')
    raw_listing = scope.query("FILESystem:DIR?").strip()
    return parse_directory_listing(raw_listing)


def retrieve_file(scope, scope_path):
    """Retrieve a file from the scope and return its bytes."""
    normalized_scope_path = normalize_scope_path(scope_path)
    command = f'FILESystem:READFile "{normalized_scope_path}"'
    scope.write(command)

    file_bytes = scope.read_raw()
    if not file_bytes:
        raise RuntimeError("No bytes were returned by FILESystem:READFile.")

    return file_bytes


def build_local_output_path(scope_path, output_dir, output_path=None):
    """Build a local path for a retrieved scope-side file."""
    if output_path:
        return output_path

    filename = scope_basename(scope_path)
    if not filename:
        filename = "mso64b_retrieved_file.bin"

    return os.path.join(output_dir, filename)


def write_bytes(local_output_path, file_bytes):
    """Write bytes to a local path, creating the parent directory if needed."""
    output_directory = os.path.dirname(local_output_path)

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with open(local_output_path, "wb") as output_file:
        output_file.write(file_bytes)

    return local_output_path


def save_listing_files(output_dir, resource_name, scope_dir, entries, timestamp):
    """Save a directory listing as text and JSON-compatible data files."""
    os.makedirs(output_dir, exist_ok=True)

    text_path = os.path.join(output_dir, f"{timestamp}_mso64b_directory_listing.txt")
    json_path = os.path.join(output_dir, f"{timestamp}_mso64b_directory_listing.json")

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
