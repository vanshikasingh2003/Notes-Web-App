from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent / "data"
BASE_DIR = BASE_DIR.resolve()


def ensure_base_dir() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_safe_path(raw_name: str) -> tuple[bool, Path | None, str]:
    name = raw_name.strip()
    if not name:
        return False, None, "Name cannot be empty."

    user_path = Path(name)

    if user_path.is_absolute():
        return False, None, "Absolute paths are not allowed."

    candidate = (BASE_DIR / user_path).resolve()

    try:
        candidate.relative_to(BASE_DIR)
    except ValueError:
        return False, None, "Invalid path. Operations are restricted to the data/ sandbox."

    return True, candidate, ""


def to_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(BASE_DIR))
    except ValueError:
        return str(path.resolve())
