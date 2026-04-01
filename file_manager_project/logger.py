from __future__ import annotations

import logging
from pathlib import Path

from utils import BASE_DIR, ensure_base_dir


def get_logger() -> logging.Logger:
    ensure_base_dir()
    log_path: Path = BASE_DIR / "logs.txt"

    logger = logging.getLogger("sandbox_file_manager")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_action(action: str, filename: str) -> None:
    logger = get_logger()
    logger.info(f"{action}: {filename}")
