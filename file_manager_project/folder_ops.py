from __future__ import annotations

from logger import log_action
from utils import get_safe_path, to_relative


def createfolder(raw_name: str) -> tuple[bool, str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if p.exists():
        return False, "Folder already exists."

    p.mkdir(parents=True, exist_ok=False)
    log_action("CREATE_FOLDER", to_relative(p))
    return True, f"Folder created: {to_relative(p)}"


def deletefolder(raw_name: str) -> tuple[bool, str]:
    ok, p, err = get_safe_path(raw_name)
    if not ok or p is None:
        return False, err

    if not p.exists():
        return False, "Folder does not exist."

    if not p.is_dir():
        return False, "Path is a file, not a folder."

    try:
        p.rmdir()
    except OSError:
        return False, "Folder is not empty. Remove files/subfolders first."

    log_action("DELETE_FOLDER", to_relative(p))
    return True, "Folder deleted successfully."


def renameitem(raw_old: str, raw_new: str) -> tuple[bool, str]:
    ok_old, old_path, err_old = get_safe_path(raw_old)
    if not ok_old or old_path is None:
        return False, err_old

    ok_new, new_path, err_new = get_safe_path(raw_new)
    if not ok_new or new_path is None:
        return False, err_new

    if not old_path.exists():
        return False, "Source item does not exist."

    if new_path.exists():
        return False, "Destination already exists."

    new_path.parent.mkdir(parents=True, exist_ok=True)
    old_path.rename(new_path)
    log_action("RENAME", f"{to_relative(old_path)} -> {to_relative(new_path)}")
    return True, "Item renamed successfully."
