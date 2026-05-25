"""Filename helpers for MSO64B captures."""

import datetime
import re


DEFAULT_LABEL = "screen"


def sanitize_label(label):
    """Return a filesystem-safe label using ASCII letters, digits, dot, dash, and underscore."""
    cleaned_label = re.sub(r"[^A-Za-z0-9_.-]+", "-", label.strip())
    cleaned_label = cleaned_label.strip("-._")

    if not cleaned_label:
        return DEFAULT_LABEL

    return cleaned_label


def timestamp_string():
    """Return a sortable local timestamp string."""
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def normalize_scope_path(path):
    """Normalize scope paths to forward slashes."""
    return path.replace("\\", "/")


def build_scope_image_path(scope_dir, label):
    """Build a unique scope-side image path."""
    normalized_scope_dir = normalize_scope_path(scope_dir)

    if not normalized_scope_dir.endswith("/"):
        normalized_scope_dir = normalized_scope_dir + "/"

    safe_label = sanitize_label(label)
    filename = f"{timestamp_string()}_mso64b_{safe_label}.png"

    return normalized_scope_dir + filename


def scope_basename(scope_path):
    """Return the final path component from a scope-side path."""
    normalized_path = normalize_scope_path(scope_path)
    return normalized_path.rstrip("/").split("/")[-1]
