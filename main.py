from pathlib import Path

BASE_DIR = Path("data").resolve()


def ensure_base_dir() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_safe_path(raw_name: str) -> tuple[bool, Path | None, str]:
    name = raw_name.strip()
    if not name:
        return False, None, "File name cannot be empty."

    if Path(name).is_absolute():
        return False, None, "Absolute paths are not allowed."

    candidate = (BASE_DIR / name).resolve()

    try:
        candidate.relative_to(BASE_DIR)
    except ValueError:
        return False, None, "Invalid path. Stay inside the project data folder."

    return True, candidate, ""


def readfileandfolder() -> None:
    ensure_base_dir()
    items = list(BASE_DIR.rglob("*"))

    print(f"\nFiles and folders inside: {BASE_DIR}")
    if not items:
        print("No files/folders found yet.")
        return

    for i, item in enumerate(items, start=1):
        marker = "[DIR]" if item.is_dir() else "[FILE]"
        print(f"{i}: {marker} {item.relative_to(BASE_DIR)}")


def createfile() -> None:
    try:
        readfileandfolder()
        name = input("\nPlease tell the name of the file: ")
        ok, p, err = get_safe_path(name)
        if not ok or p is None:
            print(err)
            return

        if p.exists():
            print("This file already exists.")
            return

        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8")

        text = input("Would you also like to add some text in the file? (Y/N): ")
        if text.strip().upper() == "Y":
            content = input("Please write the content: ")
            p.write_text(content, encoding="utf-8")

        print("File created successfully!")
    except Exception as err:
        print(f"An error occurred: {err}")


def readfile() -> None:
    try:
        readfileandfolder()
        name = input("\nEnter the name of the file you want to read: ")
        ok, p, err = get_safe_path(name)
        if not ok or p is None:
            print(err)
            return

        if not p.exists():
            print("File does not exist.")
            return

        if not p.is_file():
            print("Given path is a folder, not a file.")
            return

        content = p.read_text(encoding="utf-8")
        print("\n--- File Content Start ---")
        print(content)
        print("--- File Content End ---")
    except Exception as e:
        print(f"An error occurred: {e}")


def updatefile() -> None:
    try:
        readfileandfolder()
        name = input("\nEnter the name of the file you want to update: ")
        ok, p, err = get_safe_path(name)
        if not ok or p is None:
            print(err)
            return

        if not p.exists():
            print("File does not exist.")
            return

        if not p.is_file():
            print("Given path is a folder, not a file.")
            return

        content = input("Please type what you want to append: ")
        if not content.strip():
            print("Empty update skipped.")
            return

        existing = p.read_text(encoding="utf-8")
        prefix = "\n" if existing and not existing.endswith("\n") else ""
        p.write_text(existing + prefix + content, encoding="utf-8")
        print("Content has been successfully appended.")
    except Exception as e:
        print(f"An error occurred: {e}")


def deletefile() -> None:
    try:
        readfileandfolder()
        name = input("\nEnter the name of the file you want to delete: ")
        ok, p, err = get_safe_path(name)
        if not ok or p is None:
            print(err)
            return

        if not p.exists():
            print("File does not exist.")
            return

        if not p.is_file():
            print("Given path is a folder, not a file.")
            return

        p.unlink()
        print("File deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")


print("Press 1 for creating a file")
print("Press 2 for reading a file")
print("Press 3 for updating a file")
print("Press 4 for deleting a file")

try:
    check = int(input("Please tell your response: "))
except ValueError:
    print("Invalid choice. Please enter a number from 1 to 4.")
else:
    if check == 1:
        createfile()
    elif check == 2:
        readfile()
    elif check == 3:
        updatefile()
    elif check == 4:
        deletefile()
    else:
        print("Unknown option. Please choose between 1 and 4.")
