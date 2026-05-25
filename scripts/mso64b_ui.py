#!/usr/bin/env python3
"""Local Flask UI for the CREATE MSO64B."""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flask import Flask, redirect, render_template, request, send_from_directory, url_for

from mso64b.config import (
    DEFAULT_LABEL,
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
    save_image,
    write_bytes,
)
from mso64b.naming import build_scope_image_path, normalize_scope_path, scope_basename


app = Flask(
    __name__,
    template_folder=str(REPO_ROOT / "templates"),
    static_folder=str(REPO_ROOT / "static"),
)

RESOURCE = DEFAULT_RESOURCE
SCOPE_DIR = DEFAULT_SCOPE_DIR
OUTPUT_DIR = DEFAULT_OUTPUT_DIR
TIMEOUT_MS = DEFAULT_TIMEOUT_MS


def get_scope():
    return open_scope(RESOURCE, TIMEOUT_MS)


def get_local_images():
    image_dir = REPO_ROOT / OUTPUT_DIR

    if not image_dir.is_dir():
        return []

    image_files = []
    for filename in sorted(os.listdir(image_dir), reverse=True):
        lower_filename = filename.lower()
        if lower_filename.endswith((".png", ".jpg", ".jpeg")):
            image_files.append(filename)

    return image_files


@app.route("/")
def index():
    message = request.args.get("message", "")
    error = request.args.get("error", "")

    identity = "Not connected"
    scope_files = []
    try:
        scope = get_scope()
        identity = query_identity(scope)
        scope_files = list_files(scope, SCOPE_DIR)
    except Exception as exception:
        error = str(exception)

    return render_template(
        "index.html",
        identity=identity,
        scope_dir=SCOPE_DIR,
        scope_files=scope_files,
        local_images=get_local_images(),
        default_label=DEFAULT_LABEL,
        message=message,
        error=error,
    )


@app.route("/capture", methods=["POST"])
def capture():
    label = request.form.get("label", DEFAULT_LABEL)
    scope_path = build_scope_image_path(SCOPE_DIR, label)

    try:
        scope = get_scope()
        save_image(scope, scope_path)
        file_bytes = retrieve_file(scope, scope_path)

        local_output_path = build_local_output_path(
            scope_path,
            str(REPO_ROOT / OUTPUT_DIR),
            output_path=None,
        )
        write_bytes(local_output_path, file_bytes)

        message = f"Captured and retrieved {scope_basename(scope_path)}"
        return redirect(url_for("index", message=message))

    except Exception as exception:
        return redirect(url_for("index", error=str(exception)))


@app.route("/retrieve", methods=["POST"])
def retrieve():
    filename = request.form.get("filename", "").strip()
    if not filename:
        return redirect(url_for("index", error="No filename selected."))

    scope_path = normalize_scope_path(SCOPE_DIR)
    if not scope_path.endswith("/"):
        scope_path = scope_path + "/"
    scope_path = scope_path + filename

    try:
        scope = get_scope()
        file_bytes = retrieve_file(scope, scope_path)

        local_output_path = build_local_output_path(
            scope_path,
            str(REPO_ROOT / OUTPUT_DIR),
            output_path=None,
        )
        write_bytes(local_output_path, file_bytes)

        message = f"Retrieved {filename}"
        return redirect(url_for("index", message=message))

    except Exception as exception:
        return redirect(url_for("index", error=str(exception)))


@app.route("/img/<path:filename>")
def image_file(filename):
    return send_from_directory(str(REPO_ROOT / OUTPUT_DIR), filename)


def main():
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
