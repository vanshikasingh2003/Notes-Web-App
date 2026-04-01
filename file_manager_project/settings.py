from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import BASE_DIR, ensure_base_dir

DEFAULT_SETTINGS: dict[str, Any] = {
    "default_extension": ".txt",
    "show_hidden_files": False,
    "theme": "light",
}


def settings_path() -> Path:
    return BASE_DIR / "settings.json"


def load_settings() -> dict[str, Any]:
    ensure_base_dir()
    path = settings_path()

    if not path.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
    except (json.JSONDecodeError, OSError):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    merged = DEFAULT_SETTINGS.copy()
    merged.update(data)
    return merged


def save_settings(data: dict[str, Any]) -> None:
    ensure_base_dir()
    path = settings_path()
    path.write_text(json.dumps(data, indent=4), encoding="utf-8")
