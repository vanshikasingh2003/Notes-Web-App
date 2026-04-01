from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Tuple

from logger import log_action
from utils import BASE_DIR, ensure_base_dir, get_safe_path, to_relative


def readfileandfolder(show_hidden_files: bool = False) -> list[Path]:
    ensure_base_dir()
    items = sorted(BASE_DIR.rglob("*"))
    if not show_hidden_files:
        items = [p for p in items if not p.name.startswith(".")]
    return items


def createfile(raw_name: str, initial_content: str = "") -> tuple[bool, str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if p.exists():
        return False, "File already exists."

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(initial_content, encoding="utf-8")
    log_action("CREATE_FILE", to_relative(p))
    return True, f"File created: {to_relative(p)}"


def readfile(raw_name: str) -> tuple[bool, str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if not p.exists():
        return False, "File does not exist."

    if not p.is_file():
        return False, "Path is a directory, not a file."

    content = p.read_text(encoding="utf-8")
    log_action("READ_FILE", to_relative(p))
    return True, content


def updatefile(raw_name: str, append_content: str) -> tuple[bool, str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if not p.exists():
        return False, "File does not exist."

    if not p.is_file():
        return False, "Path is a directory, not a file."

    if not append_content.strip():
        return False, "Nothing to append."

    existing = p.read_text(encoding="utf-8")
    prefix = "\n" if existing and not existing.endswith("\n") else ""
    new_text = existing + prefix + append_content
    p.write_text(new_text, encoding="utf-8")
    log_action("UPDATE_FILE", to_relative(p))
    return True, "File updated successfully."


def deletefile(raw_name: str) -> tuple[bool, str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if not p.exists():
        return False, "File does not exist."

    if not p.is_file():
        return False, "Path is a directory, not a file."

    p.unlink()
    log_action("DELETE_FILE", to_relative(p))
    return True, "File deleted successfully."


def fileinfo(raw_name: str) -> tuple[bool, dict[str, str] | str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if not p.exists():
        return False, "Path does not exist."

    stat = p.stat()
    info = {
        "name": p.name,
        "size_bytes": str(stat.st_size),
        "last_modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "extension": p.suffix if p.is_file() else "",
        "absolute_path": str(p.resolve()),
        "relative_path": to_relative(p),
        "type": "directory" if p.is_dir() else "file",
    }
    return True, info
