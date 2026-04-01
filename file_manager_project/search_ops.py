from __future__ import annotations

from pathlib import Path

from logger import log_action
from utils import BASE_DIR, ensure_base_dir, to_relative


def searchfiles(pattern: str, show_hidden_files: bool = False) -> tuple[bool, list[str] | str]:
    ensure_base_dir()
    term = pattern.strip()
    if not term:
        return False, "Search pattern cannot be empty."

    results: list[Path] = []
    for item in BASE_DIR.rglob(term):
        if not show_hidden_files and item.name.startswith("."):
            continue
        results.append(item)

    if "*" not in term and "?" not in term and "[" not in term:
        lowered = term.lower()
        for item in BASE_DIR.rglob("*"):
            if not show_hidden_files and item.name.startswith("."):
                continue
            if lowered in item.name.lower() and item not in results:
                results.append(item)

    rels = sorted([to_relative(p) for p in results])
    log_action("SEARCH", term)
    return True, rels
